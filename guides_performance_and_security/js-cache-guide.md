# JavaScript Caching & Performance Optimization — Complete Guide

A comprehensive reference of every major caching and memoization pattern in JS,
with real-world examples, tradeoffs, and when to use each one.

---

## Table of Contents

1. [DOM Read Caching](#1-dom-read-caching)
2. [Computed Value Caching (Memoization)](#2-computed-value-caching-memoization)
3. [Generic Memoize Wrapper](#3-generic-memoize-wrapper)
4. [requestAnimationFrame Throttle](#4-requestanimationframe-throttle)
5. [Debounce & Throttle](#5-debounce--throttle)
6. [Event Delegation](#6-event-delegation)
7. [WeakMap / WeakRef Caching](#7-weakmap--weakref-caching)
8. [Module-level Singleton Cache](#8-module-level-singleton-cache)
9. [LRU Cache](#9-lru-cache)
10. [Lazy Initialization](#10-lazy-initialization)
11. [Selector Cache](#11-selector-cache)
12. [Style / Class Cache](#12-style--class-cache)
13. [Fetch / Network Response Cache](#13-fetch--network-response-cache)
14. [Web Worker Offloading](#14-web-worker-offloading)
15. [Object Pool (Reuse Instead of Create)](#15-object-pool-reuse-instead-of-create)
16. [Virtual List / Windowing](#16-virtual-list--windowing)
17. [ResizeObserver Cache](#17-resizeobserver-cache)
18. [IntersectionObserver Cache](#18-intersectionobserver-cache)
19. [Batch DOM Writes (Write Queue)](#19-batch-dom-writes-write-queue)
20. [Read–Write Separation (Layout Thrashing Prevention)](#20-readwrite-separation-layout-thrashing-prevention)
21. [Derived State Cache](#21-derived-state-cache)
22. [Symbol / Key Interning](#22-symbol--key-interning)
23. [Cache Invalidation Strategies](#23-cache-invalidation-strategies)
24. [Quick Reference Table](#24-quick-reference-table)

---

## 1. DOM Read Caching

**Problem:** Reading layout properties (`offsetWidth`, `offsetLeft`, `scrollHeight`,
`getBoundingClientRect`, `getComputedStyle`) forces the browser to flush pending
style/layout work — a **forced reflow**. Doing this inside a loop or on every event
is the #1 cause of jank.

**Rule:** Read once, store the result, reuse the stored value until you know it changed.

```js
// ❌ BAD — forces a reflow on every iteration
for (let i = 0; i < items.length; i++) {
  items[i].style.width = container.offsetWidth / items.length + 'px';
  //                      ^^^^^^^^^^^^^^^^^^^ read inside write loop = thrashing
}

// ✅ GOOD — one read, many writes
const slotWidth = container.offsetWidth / items.length; // read once
for (let i = 0; i < items.length; i++) {
  items[i].style.width = slotWidth + 'px';              // pure writes
}
```

### Class-level DOM cache with invalidation flag

```js
class Carousel {
  #cachedWidth = 0;

  #itemWidth() {
    if (this.#cachedWidth) return this.#cachedWidth;         // cache hit
    this.#cachedWidth = this.items[1].offsetLeft             // cache miss — read DOM
                      - this.items[0].offsetLeft;
    return this.#cachedWidth;
  }

  onResize() {
    this.#cachedWidth = 0; // invalidate — next call re-reads DOM
  }
}
```

### What triggers a forced reflow (read these, cache their results)

| Property / Method | Notes |
|---|---|
| `el.offsetWidth / offsetHeight` | Including padding + border |
| `el.offsetTop / offsetLeft` | Relative to offsetParent |
| `el.scrollWidth / scrollHeight` | Full content size |
| `el.scrollTop / scrollLeft` | Current scroll position |
| `el.getBoundingClientRect()` | Full box — very expensive |
| `el.clientWidth / clientHeight` | Viewport-relative size |
| `window.getComputedStyle(el)` | Computed CSS values |
| `el.focus()` | Can also trigger layout |

---

## 2. Computed Value Caching (Memoization)

**Problem:** A function does heavy computation (sorting, filtering, parsing, math)
and gets called repeatedly with the same inputs.

**Solution:** Store input → output in a Map. Return the stored result if input matches.

```js
// Pure function — expensive, called often with repeated args
function computeLayout(itemCount, containerWidth) {
  // imagine heavy math here
  return { columns: Math.floor(containerWidth / 220), itemCount };
}

// Memoized version
const layoutCache = new Map();

function computeLayoutCached(itemCount, containerWidth) {
  const key = `${itemCount}:${containerWidth}`;
  if (layoutCache.has(key)) return layoutCache.get(key); // cache hit
  const result = computeLayout(itemCount, containerWidth);
  layoutCache.set(key, result);
  return result;
}
```

**When to use:** Pure functions (same input always gives same output), called
frequently with a small set of distinct inputs.

**When NOT to use:** Side-effectful functions, functions that depend on external
mutable state, or functions called with an unbounded variety of inputs
(cache grows without bound — use LRU instead, see §9).

---

## 3. Generic Memoize Wrapper

A reusable utility you can drop onto any pure function:

```js
function memoize(fn, keyFn = (...args) => JSON.stringify(args)) {
  const cache = new Map();
  return function (...args) {
    const key = keyFn(...args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Usage
const expensiveFilter = memoize((list, query) =>
  list.filter(item => item.name.includes(query))
);
```

**Custom key function** matters — `JSON.stringify` is safe but slow for large objects.
Prefer a hand-crafted key when arguments are large or contain arrays/objects:

```js
// Fast key for (number, number) args
const cachedWidth = memoize(computeWidth, (count, w) => `${count}|${w}`);
```

---

## 4. requestAnimationFrame Throttle

**Problem:** `scroll`, `mousemove`, `pointermove` events fire dozens of times per
second — far more often than the screen redraws (60–120 fps). Running heavy logic
on every event wastes CPU.

**Solution:** Use a boolean flag so only one rAF callback is queued per frame.

```js
let rafPending = false;

element.addEventListener('scroll', () => {
  if (rafPending) return;          // already queued for this frame
  rafPending = true;
  requestAnimationFrame(() => {
    rafPending = false;
    doExpensiveWork();             // runs at most once per frame
  });
}, { passive: true });
```

**Why `{ passive: true }`?** Tells the browser "this handler will never call
`preventDefault()`", so it can start scrolling immediately without waiting for JS.
Always add it to `scroll`, `touchstart`, `touchmove`, `wheel` handlers unless you
actually need to prevent the default.

### rAF class pattern

```js
class Scroller {
  #rafId = 0;

  #onScroll = () => {
    cancelAnimationFrame(this.#rafId);         // cancel previous if still pending
    this.#rafId = requestAnimationFrame(() => {
      this.#update();
    });
  };

  bind() {
    window.addEventListener('scroll', this.#onScroll, { passive: true });
  }

  destroy() {
    window.removeEventListener('scroll', this.#onScroll);
    cancelAnimationFrame(this.#rafId);
  }
}
```

---

## 5. Debounce & Throttle

Two classic time-based rate-limiting patterns.

### Debounce — wait until the user *stops*

Fires once after N ms of silence. Use for: search input, resize end, form validation.

```js
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

const onResizeEnd = debounce(() => {
  cachedWidth = 0;           // invalidate DOM cache
  rebuild();
}, 150);

window.addEventListener('resize', onResizeEnd);
```

### Throttle — fire at most once per N ms

Fires on the leading edge, then ignores calls until the cooldown passes.
Use for: scroll progress, drag-and-drop, rate-limited API calls.

```js
function throttle(fn, limit) {
  let lastCall = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastCall < limit) return;
    lastCall = now;
    return fn.apply(this, args);
  };
}

const onScroll = throttle(() => updateProgressBar(), 16); // ~60fps cap
window.addEventListener('scroll', onScroll, { passive: true });
```

### Debounce vs Throttle vs rAF

| Pattern | Fires | Best for |
|---|---|---|
| **rAF** | Once per screen frame (~16ms) | Visual updates synced to paint |
| **Throttle** | Once per fixed interval | API calls, analytics, drag |
| **Debounce** | Once after silence | Search, resize-end, save |

---

## 6. Event Delegation

**Problem:** Attaching a listener to each of 1000 list items wastes memory and
slows down DOM mutations (add/remove item → add/remove listener).

**Solution:** Attach one listener to the parent. The event bubbles up from the
actual target — inspect `e.target` to determine which item was clicked.

```js
// ❌ BAD — 1000 listeners
items.forEach(item => {
  item.addEventListener('click', handleClick);
});

// ✅ GOOD — 1 listener
list.addEventListener('click', e => {
  const item = e.target.closest('[data-item-id]');
  if (!item) return;
  handleClick(item.dataset.itemId);
});
```

**Bonus:** Works automatically for dynamically added items — no need to rebind.

---

## 7. WeakMap / WeakRef Caching

**Problem:** Caching DOM nodes or objects in a regular `Map` prevents garbage
collection — memory leak.

**Solution:** Use `WeakMap` — keys are held weakly, so the entry is automatically
removed when the node is GC'd.

```js
const dimensionCache = new WeakMap();

function getDimensions(el) {
  if (dimensionCache.has(el)) return dimensionCache.get(el); // cache hit

  const rect = el.getBoundingClientRect();
  dimensionCache.set(el, rect);
  return rect;
}

// When `el` is removed from DOM and has no other references,
// the WeakMap entry is automatically garbage-collected.
```

### WeakRef — hold a reference without preventing GC

```js
class Tooltip {
  #targetRef;

  constructor(target) {
    this.#targetRef = new WeakRef(target); // won't keep target alive
  }

  show() {
    const target = this.#targetRef.deref(); // null if GC'd
    if (!target) return;
    // position tooltip relative to target
  }
}
```

**Use WeakMap/WeakRef when:** caching per-DOM-node data, per-object metadata,
plugin state attached to third-party objects.

---

## 8. Module-level Singleton Cache

**Problem:** Parsing config, building a regex, reading a constant — done once but
called from many places.

**Solution:** Store the result at module scope. It's computed once on first import.

```js
// config.js
const _parsedConfig = JSON.parse(document.getElementById('app-config').textContent);

export function getConfig(key) {
  return _parsedConfig[key]; // always uses the pre-parsed object
}
```

```js
// patterns.js — compile regex once, reuse
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export const isEmail = str => EMAIL_RE.test(str);
```

---

## 9. LRU Cache

**Problem:** Memoization with unbounded Map grows forever. Need a fixed-size cache
that evicts the least-recently-used entry.

```js
class LRU {
  #map;
  #max;

  constructor(max = 100) {
    this.#max = max;
    this.#map = new Map();
  }

  get(key) {
    if (!this.#map.has(key)) return undefined;
    // Re-insert to mark as recently used
    const value = this.#map.get(key);
    this.#map.delete(key);
    this.#map.set(key, value);
    return value;
  }

  set(key, value) {
    if (this.#map.has(key)) this.#map.delete(key);
    else if (this.#map.size >= this.#max) {
      // Delete oldest entry (first key in insertion-order Map)
      this.#map.delete(this.#map.keys().next().value);
    }
    this.#map.set(key, value);
  }

  has(key) { return this.#map.has(key); }
}

// Usage
const cache = new LRU(50);

function expensiveRender(id) {
  if (cache.has(id)) return cache.get(id);
  const result = heavyCompute(id);
  cache.set(id, result);
  return result;
}
```

**Use when:** Input variety is unbounded (user IDs, search queries, URLs).

---

## 10. Lazy Initialization

**Problem:** An object/value is expensive to create, but might never be needed.
Don't pay the cost upfront.

```js
class Analytics {
  #chart = null; // not created yet

  get chart() {
    if (!this.#chart) {
      this.#chart = new HeavyChartLibrary('#canvas'); // created on first access
    }
    return this.#chart;
  }
}

// Chart is only initialized when first accessed
analytics.chart.render(data);
```

### Lazy module loading

```js
let heavyModule = null;

async function runHeavyTask() {
  if (!heavyModule) {
    heavyModule = await import('./heavy-module.js'); // loaded once, cached
  }
  return heavyModule.run();
}
```

---

## 11. Selector Cache

**Problem:** `document.querySelector()` traverses the DOM every call — expensive
inside event handlers or animation loops.

```js
// ❌ BAD — DOM traversal on every frame
function update() {
  document.querySelector('.progress-bar').style.width = getProgress() + '%';
}

// ✅ GOOD — query once, reuse the reference
const progressBar = document.querySelector('.progress-bar');

function update() {
  progressBar.style.width = getProgress() + '%';
}
```

### Dynamic selector cache (query-by-need)

```js
const elCache = new Map();

function $(selector, root = document) {
  if (!elCache.has(selector)) {
    elCache.set(selector, root.querySelector(selector));
  }
  return elCache.get(selector);
}

// Clear cache when DOM changes significantly
function clearElCache() { elCache.clear(); }
```

---

## 12. Style / Class Cache

**Problem:** Reading `el.style.color` or `getComputedStyle(el).color` every frame
to check if a value changed before updating — still triggers style recalculation.

**Solution:** Track the last applied value yourself, skip the DOM write if unchanged.

```js
class Animator {
  #lastWidth = null;

  setWidth(el, w) {
    if (w === this.#lastWidth) return; // skip redundant DOM write
    this.#lastWidth = w;
    el.style.width = w + 'px';
  }
}
```

### CSS variable batching

Write CSS variables on a root element instead of inline styles on many nodes.
One write propagates to all children via inheritance:

```js
// ❌ BAD — write to 200 child elements
items.forEach((el, i) => { el.style.opacity = opacities[i]; });

// ✅ GOOD — write one variable, use it in CSS with calc() or per-item var
document.documentElement.style.setProperty('--base-opacity', 0.5);
// CSS: .item { opacity: var(--base-opacity); }
```

---

## 13. Fetch / Network Response Cache

### In-memory fetch dedup

Prevents duplicate in-flight requests for the same URL:

```js
const fetchCache  = new Map(); // url → Promise
const resultCache = new Map(); // url → parsed data

async function fetchOnce(url) {
  if (resultCache.has(url)) return resultCache.get(url); // already done
  if (fetchCache.has(url))  return fetchCache.get(url);  // in-flight — share Promise

  const promise = fetch(url)
    .then(r => r.json())
    .then(data => {
      resultCache.set(url, data);
      fetchCache.delete(url);
      return data;
    });

  fetchCache.set(url, promise);
  return promise;
}
```

### Cache-Control headers (HTTP cache)

Let the server drive browser caching — no JS needed:

```
Cache-Control: max-age=3600          → cache for 1 hour
Cache-Control: no-cache              → revalidate every time
Cache-Control: immutable             → never recheck (for hashed assets)
ETag / If-None-Match                 → 304 Not Modified if unchanged
```

### Service Worker cache (offline + stale-while-revalidate)

```js
// sw.js
const CACHE = 'v1';

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => {
      const network = fetch(e.request).then(res => {
        caches.open(CACHE).then(c => c.put(e.request, res.clone()));
        return res;
      });
      return cached || network; // serve cache instantly, update in background
    })
  );
});
```

---

## 14. Web Worker Offloading

**Problem:** Heavy computation (parsing, sorting, image processing) blocks the
main thread, freezing animations and user input.

**Solution:** Run it in a Worker. The result is sent back via message — main thread
stays free.

```js
// worker.js
self.onmessage = ({ data }) => {
  const result = heavySort(data.items); // runs off main thread
  self.postMessage(result);
};

// main.js
const worker = new Worker('./worker.js');
const workerCache = new Map();

function sortItems(items) {
  const key = JSON.stringify(items);
  if (workerCache.has(key)) return Promise.resolve(workerCache.get(key));

  return new Promise(resolve => {
    worker.onmessage = ({ data }) => {
      workerCache.set(key, data);
      resolve(data);
    };
    worker.postMessage({ items });
  });
}
```

---

## 15. Object Pool (Reuse Instead of Create)

**Problem:** Creating and destroying many short-lived objects (particles, list rows,
event objects) causes GC pressure and frame drops.

**Solution:** Pre-allocate a pool of objects. Return used ones to the pool instead
of discarding.

```js
class Pool {
  #free = [];
  #create;

  constructor(factory, initialSize = 10) {
    this.#create = factory;
    for (let i = 0; i < initialSize; i++) {
      this.#free.push(factory());
    }
  }

  acquire() {
    return this.#free.length ? this.#free.pop() : this.#create();
  }

  release(obj) {
    this.reset(obj);           // clear state before reuse
    this.#free.push(obj);
  }

  reset(obj) {
    // Override to zero-out object fields
    Object.keys(obj).forEach(k => { obj[k] = null; });
  }
}

// Usage — particle system
const pool = new Pool(() => ({ x: 0, y: 0, vx: 0, vy: 0, life: 0 }), 200);

function spawnParticle(x, y) {
  const p = pool.acquire();
  p.x = x; p.y = y; p.life = 1;
  return p;
}

function killParticle(p) {
  pool.release(p); // returned to pool, not GC'd
}
```

---

## 16. Virtual List / Windowing

**Problem:** Rendering 10,000 DOM nodes at once is slow to paint and scroll,
even if most are off-screen.

**Solution:** Only render the nodes currently visible in the viewport. Reuse DOM
nodes as the user scrolls (same concept as Object Pool, applied to the DOM).

```js
class VirtualList {
  #rowHeight;
  #visibleCount;
  #nodes   = [];
  #dataCache = new Map(); // index → pre-rendered HTML string

  constructor({ container, rowHeight, data }) {
    this.container  = container;
    this.#rowHeight = rowHeight;
    this.data       = data;
    this.#visibleCount = Math.ceil(container.clientHeight / rowHeight) + 2;

    this.#allocateNodes();
    this.#renderWindow(0);

    container.addEventListener('scroll', () => {
      const startIndex = Math.floor(container.scrollTop / rowHeight);
      this.#renderWindow(startIndex);
    }, { passive: true });
  }

  #allocateNodes() {
    for (let i = 0; i < this.#visibleCount; i++) {
      const el = document.createElement('div');
      el.style.position = 'absolute';
      el.style.height   = this.#rowHeight + 'px';
      this.container.appendChild(el);
      this.#nodes.push(el);
    }
  }

  #renderWindow(startIndex) {
    this.#nodes.forEach((el, i) => {
      const dataIndex = startIndex + i;
      if (dataIndex >= this.data.length) { el.style.display = 'none'; return; }

      el.style.display = '';
      el.style.top     = dataIndex * this.#rowHeight + 'px';

      if (!this.#dataCache.has(dataIndex)) {
        this.#dataCache.set(dataIndex, this.#renderItem(this.data[dataIndex]));
      }
      el.innerHTML = this.#dataCache.get(dataIndex); // cache hit = no template work
    });
  }

  #renderItem(item) {
    return `<span>${item.name}</span><span>$${item.price}</span>`;
  }
}
```

---

## 17. ResizeObserver Cache

**Problem:** `window.resize` fires for any window size change — even unrelated to
the element you care about. Multiple handlers all re-read dimensions.

**Solution:** Use `ResizeObserver` — fires only when the observed element's size
actually changes. Cache the reported size.

```js
class SizeTracker {
  #cache = new WeakMap();
  #ro;

  constructor() {
    this.#ro = new ResizeObserver(entries => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        this.#cache.set(entry.target, { width, height }); // update cache
        this.#onSizeChange(entry.target, width, height);
      }
    });
  }

  observe(el) { this.#ro.observe(el); }

  getSize(el) {
    // Return cached size — zero DOM reads
    return this.#cache.get(el) ?? { width: el.offsetWidth, height: el.offsetHeight };
  }

  #onSizeChange(el, w, h) { /* rebuild layout, etc. */ }
}
```

---

## 18. IntersectionObserver Cache

**Problem:** Checking if elements are visible by reading `getBoundingClientRect()`
on scroll is expensive.

**Solution:** `IntersectionObserver` reports visibility changes asynchronously,
off the main thread.

```js
const visibilityCache = new WeakMap(); // el → boolean

const io = new IntersectionObserver(entries => {
  entries.forEach(e => visibilityCache.set(e.target, e.isIntersecting));
}, { threshold: 0 });

function isVisible(el) {
  if (!visibilityCache.has(el)) io.observe(el); // start tracking
  return visibilityCache.get(el) ?? false;       // return last known state
}
```

---

## 19. Batch DOM Writes (Write Queue)

**Problem:** Many parts of the code write to the DOM independently, triggering
multiple layouts per frame.

**Solution:** Collect all writes, flush them in a single rAF.

```js
const writeQueue = [];
let flushScheduled = false;

function scheduleWrite(fn) {
  writeQueue.push(fn);
  if (flushScheduled) return;
  flushScheduled = true;
  requestAnimationFrame(() => {
    flushScheduled = false;
    // Reads first — one batch
    // (if reads need to happen before writes, do them before this flush)
    while (writeQueue.length) writeQueue.shift()();
  });
}

// Usage from anywhere in the codebase
scheduleWrite(() => { el.style.transform = `translateX(${x}px)`; });
scheduleWrite(() => { badge.textContent  = count; });
// Both writes happen in the same rAF — one layout
```

---

## 20. Read–Write Separation (Layout Thrashing Prevention)

**Problem:** Interleaving reads and writes forces the browser to recalculate layout
between each pair.

```
read  → browser flushes layout ↓
write → layout is dirty        ↓
read  → browser flushes again  ↓  ← thrashing
write → dirty again            ↓
```

**Solution:** Do ALL reads first, then ALL writes.

```js
// ❌ BAD — read, write, read, write
boxes.forEach(box => {
  const h = box.offsetHeight;     // read  → flush
  box.style.height = h * 2 + 'px'; // write → dirty
});

// ✅ GOOD — read all, then write all
const heights = boxes.map(box => box.offsetHeight); // reads — one flush
boxes.forEach((box, i) => {
  box.style.height = heights[i] * 2 + 'px';         // writes — no extra flush
});
```

FastDOM library formalizes this pattern if you need it across a large codebase.

---

## 21. Derived State Cache

**Problem:** UI state that's computed from other state gets recalculated on every
render, even when the source data hasn't changed.

```js
class Store {
  #items    = [];
  #filter   = '';
  #filtered = null; // derived state cache
  #total    = null;

  setItems(items) {
    this.#items    = items;
    this.#filtered = null; // invalidate derived caches
    this.#total    = null;
  }

  setFilter(f) {
    this.#filter   = f;
    this.#filtered = null; // only filtered list is stale
  }

  get filteredItems() {
    if (this.#filtered === null) {
      this.#filtered = this.#items.filter(i => i.name.includes(this.#filter));
    }
    return this.#filtered; // cached until setItems/setFilter called
  }

  get total() {
    if (this.#total === null) {
      this.#total = this.#items.reduce((s, i) => s + i.price, 0);
    }
    return this.#total;
  }
}
```

This is essentially what `useMemo` does in React, or `computed` in Vue.

---

## 22. Symbol / Key Interning

**Problem:** Building the same string key repeatedly with string concatenation
creates many short-lived string allocations.

```js
// ❌ BAD — allocates a new string on every call
function getCached(type, id) {
  return cache.get(type + ':' + id);
}

// ✅ GOOD — interned keys via a Map-of-Maps (no string allocation)
const cache = new Map(); // type → Map(id → value)

function getCached(type, id) {
  let inner = cache.get(type);
  if (!inner) { inner = new Map(); cache.set(type, inner); }
  return inner.get(id);
}
```

For very hot paths, a Map-of-Maps avoids string concatenation and hashing of
the combined key entirely.

---

## 23. Cache Invalidation Strategies

Caching is only half the problem — knowing when to clear it is the other half.

### Time-based (TTL)

```js
class TTLCache {
  #store = new Map();
  #ttl;

  constructor(ttl = 5000) { this.#ttl = ttl; }

  set(key, value) {
    this.#store.set(key, { value, expires: Date.now() + this.#ttl });
  }

  get(key) {
    const entry = this.#store.get(key);
    if (!entry) return undefined;
    if (Date.now() > entry.expires) { this.#store.delete(key); return undefined; }
    return entry.value;
  }
}
```

### Version / generation counter

```js
class VersionedCache {
  #cache   = new Map();
  #version = 0;

  invalidate() { this.#version++; }

  set(key, value) { this.#cache.set(key, { value, ver: this.#version }); }

  get(key) {
    const e = this.#cache.get(key);
    return e?.ver === this.#version ? e.value : undefined;
  }
}
```

### Event-driven invalidation

```js
const cache = new Map();

document.addEventListener('cart:updated', () => {
  cache.delete('cart-total');
  cache.delete('cart-items');
});
```

### Dependency tracking (fine-grained)

Each cache entry declares what it depends on. When a dependency changes,
only affected entries are cleared:

```js
const deps  = new Map(); // key → Set of dependency names
const cache = new Map();

function setWithDeps(key, value, dependsOn = []) {
  cache.set(key, value);
  deps.set(key, new Set(dependsOn));
}

function invalidateDep(depName) {
  for (const [key, depSet] of deps) {
    if (depSet.has(depName)) cache.delete(key);
  }
}

// Usage
setWithDeps('user-header', renderHeader(user), ['user.name', 'user.avatar']);

// When user's name changes:
invalidateDep('user.name'); // only 'user-header' cleared, not 'user-settings'
```

---

## 24. Quick Reference Table

| Pattern | Solves | Key API / Technique | Invalidate on |
|---|---|---|---|
| DOM Read Cache | Layout thrashing | Class field + flag | Resize / DOM mutation |
| Memoization | Repeated pure computation | `Map` keyed by args | Never (pure) or explicit |
| Generic memoize | Any pure function | Wrapper + `Map` | Manual / TTL |
| rAF Throttle | scroll/mousemove spam | `requestAnimationFrame` + flag | Per frame auto |
| Debounce | Resize-end, search input | `setTimeout` reset | Auto after silence |
| Throttle | Scroll progress, drag | Time delta check | Auto on interval |
| Event Delegation | Many listeners | `closest()` on parent | Never (DOM-based) |
| WeakMap Cache | Per-node metadata | `WeakMap` | Auto GC |
| WeakRef | Optional object reference | `WeakRef.deref()` | Auto GC |
| Singleton | One-time parsing / compile | Module-level const | Never |
| LRU | Unbounded input variety | Map + eviction | On capacity |
| Lazy Init | Maybe-never-needed resource | Getter + null check | Manual |
| Selector Cache | Repeated `querySelector` | `Map` of selector → el | DOM change |
| Style Write Cache | Redundant DOM writes | Last-value field | Value change |
| Fetch Dedup | Duplicate network calls | `Map` of url → Promise | Response received |
| Service Worker | Offline / stale-while-revalidate | Cache API | Version bump |
| Web Worker | Main thread blocking | `postMessage` + `Map` | Data change |
| Object Pool | GC pressure from many objects | Pre-allocated array | On release |
| Virtual List | 10k+ DOM nodes | Windowing + DOM reuse | Scroll position |
| ResizeObserver Cache | Repeated size reads | `WeakMap` + observer | Resize event |
| IntersectionObserver Cache | Visibility checks on scroll | `WeakMap` + observer | IO callback |
| Write Queue | Multiple scattered DOM writes | rAF flush queue | Per frame |
| Read–Write Separation | Interleaved layout thrashing | Group reads, then writes | N/A |
| Derived State Cache | Recomputing from unchanged data | Null flag per computed value | Source mutation |
| TTL Cache | Stale data tolerance | `Map` + `Date.now()` | Expiry time |
| Version Cache | Bulk invalidation | Generation counter | `invalidate()` call |
| Map-of-Maps | Key string allocation | Nested `Map` | Manual |

---

*Remember: measure first (`performance.mark`, Chrome DevTools Performance tab,
`console.time`). Cache only what profiling shows is actually slow.*
