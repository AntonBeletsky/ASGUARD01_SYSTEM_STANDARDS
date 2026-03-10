# JavaScript Performance Guide: Writing Violation-Free, Production-Ready Code

> A comprehensive reference for engineers who need to understand, prevent, and eliminate `[Violation]`, `[Intervention]`, and performance warnings in JavaScript — built on W3C, WHATWG, and Chromium standards.

---

## Table of Contents

1. [Understanding Browser Violations](#1-understanding-browser-violations)
2. [The Main Thread & Event Loop](#2-the-main-thread--event-loop)
3. [Long Tasks & Forced Synchronous Layouts](#3-long-tasks--forced-synchronous-layouts)
4. [Scroll, Touch & Input Handlers](#4-scroll-touch--input-handlers)
5. [requestAnimationFrame & Visual Updates](#5-requestanimationframe--visual-updates)
6. [Timers: setTimeout & setInterval](#6-timers-settimeout--setinterval)
7. [DOM Manipulation Patterns](#7-dom-manipulation-patterns)
8. [Memory Management & Leaks](#8-memory-management--leaks)
9. [Network & Resource Loading](#9-network--resource-loading)
10. [Web Workers & Off-Thread Computation](#10-web-workers--off-thread-computation)
11. [Async Patterns & Microtasks](#11-async-patterns--microtasks)
12. [Rendering Pipeline & CSS Performance](#12-rendering-pipeline--css-performance)
13. [Observers API (Intersection, Resize, Mutation)](#13-observers-api)
14. [Performance Measurement & Profiling](#14-performance-measurement--profiling)
15. [React & Framework-Specific Patterns](#15-react--framework-specific-patterns)
16. [Service Workers & Caching Strategies](#16-service-workers--caching-strategies)
17. [Production Checklist](#17-production-checklist)

---

## 1. Understanding Browser Violations

### What Are Violations?

Browser violations are warnings emitted when JavaScript code performs operations that block the main thread or degrade user experience. They appear in DevTools console as:

```
[Violation] 'click' handler took 200ms
[Violation] Forced reflow while executing JavaScript took 50ms
[Violation] Added non-passive event listener to a scroll-blocking event
[Intervention] Modified page load behavior: 'text/javascript' is not a valid MIME type
```

### Violation Categories

| Violation Type | Threshold | Root Cause |
|---|---|---|
| Long Task | > 50ms | Blocking main thread |
| Input Handler | > 100ms | Slow event callbacks |
| Scroll Handler | any | Missing `passive: true` |
| Forced Reflow | > 10ms | Read-after-write DOM access |
| rAF Handler | > 16ms | Too much work per frame |
| Timer Violation | configurable | Slow `setTimeout` callbacks |

### The Core Rule

```
The main thread must always be free to respond within 50ms (RAIL model).
Any synchronous work > 50ms is a Long Task and causes jank.
```

---

## 2. The Main Thread & Event Loop

### How the Event Loop Works

```
┌─────────────────────────────────────────────┐
│                 Call Stack                   │
│  (synchronous JS execution — blocks all)     │
└────────────────────┬────────────────────────┘
                     │ empties
                     ▼
┌─────────────────────────────────────────────┐
│              Microtask Queue                 │
│  Promise.then, queueMicrotask, MutationObs   │
│  (ALL microtasks drain before next task)     │
└────────────────────┬────────────────────────┘
                     │ drains
                     ▼
┌─────────────────────────────────────────────┐
│               Task Queue (Macrotasks)        │
│  setTimeout, setInterval, I/O, MessageChannel│
│  (one task per loop iteration)               │
└────────────────────┬────────────────────────┘
                     │ one task
                     ▼
┌─────────────────────────────────────────────┐
│          Rendering (if needed)               │
│  Style → Layout → Paint → Composite         │
└─────────────────────────────────────────────┘
```

### Blocking vs Non-Blocking

```javascript
// ❌ VIOLATION: Synchronous loop blocking the main thread
function processLargeDataset(items) {
  const results = [];
  for (let i = 0; i < items.length; i++) {
    results.push(heavyComputation(items[i])); // blocks for 300ms total
  }
  return results;
}

// ✅ CORRECT: Yield back to event loop using scheduler
async function processLargeDataset(items) {
  const results = [];
  const CHUNK_SIZE = 100;

  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    for (const item of chunk) {
      results.push(heavyComputation(item));
    }
    // Yield to the event loop after each chunk
    await yieldToMain();
  }
  return results;
}

// The correct way to yield to the main thread
function yieldToMain() {
  // scheduler.yield() is the modern standard (Chrome 115+)
  if ('scheduler' in window && 'yield' in scheduler) {
    return scheduler.yield();
  }
  // Fallback: MessageChannel has higher priority than setTimeout(0)
  return new Promise(resolve => {
    const { port1, port2 } = new MessageChannel();
    port1.onmessage = resolve;
    port2.postMessage(null);
  });
}
```

### Measuring Long Tasks

```javascript
// Use PerformanceObserver to detect Long Tasks in production
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.warn(`[LongTask] duration=${entry.duration.toFixed(1)}ms`, entry);
    // Report to your analytics
    reportToAnalytics({ type: 'long-task', duration: entry.duration });
  }
});

observer.observe({ type: 'longtask', buffered: true });
```

---

## 3. Long Tasks & Forced Synchronous Layouts

### What Is Forced Synchronous Layout (FSL)?

FSL occurs when JavaScript writes to the DOM and then immediately reads a layout property, forcing the browser to synchronously recalculate layout.

```javascript
// ❌ VIOLATION: Forced reflow in a loop — "Layout Thrashing"
function badResizeElements(elements) {
  for (const el of elements) {
    const width = el.offsetWidth;        // READ  → forces layout
    el.style.width = (width * 2) + 'px'; // WRITE → invalidates layout
  }
  // Each iteration: write then immediately read = forced reflow
}

// ✅ CORRECT: Batch reads, then batch writes (FastDOM pattern)
function goodResizeElements(elements) {
  // Phase 1: Batch ALL reads
  const widths = elements.map(el => el.offsetWidth);

  // Phase 2: Batch ALL writes
  elements.forEach((el, i) => {
    el.style.width = (widths[i] * 2) + 'px';
  });
}
```

### Properties That Trigger Layout

Reading any of these after a DOM write causes forced layout:

```javascript
// LAYOUT-TRIGGERING PROPERTIES (avoid reading after writes):
const layoutTriggers = [
  // Box model
  'offsetTop', 'offsetLeft', 'offsetWidth', 'offsetHeight', 'offsetParent',
  'clientTop', 'clientLeft', 'clientWidth', 'clientHeight',
  'scrollTop', 'scrollLeft', 'scrollWidth', 'scrollHeight',

  // Computed geometry
  'getBoundingClientRect()',
  'getClientRects()',
  'computedStyleMap()',
  'getComputedStyle()',

  // Focus
  'focus()',

  // Form
  'select()',

  // Scroll
  'scrollIntoView()',
  'scrollIntoViewIfNeeded()',
];
```

### FastDOM Pattern

```javascript
// FastDOM-style batching for production use
class DOMScheduler {
  #reads = [];
  #writes = [];
  #scheduled = false;

  read(fn) {
    this.#reads.push(fn);
    this.#schedule();
  }

  write(fn) {
    this.#writes.push(fn);
    this.#schedule();
  }

  #schedule() {
    if (this.#scheduled) return;
    this.#scheduled = true;
    requestAnimationFrame(() => this.#flush());
  }

  #flush() {
    // Execute all reads first
    const reads = this.#reads.splice(0);
    const writes = this.#writes.splice(0);

    reads.forEach(fn => fn());   // All reads together
    writes.forEach(fn => fn());  // All writes together

    this.#scheduled = false;

    // If new tasks were queued during flush, schedule again
    if (this.#reads.length || this.#writes.length) {
      this.#schedule();
    }
  }
}

const dom = new DOMScheduler();

// Usage
dom.read(() => {
  const height = element.clientHeight; // safe read
  dom.write(() => {
    element.style.transform = `translateY(${height}px)`; // safe write
  });
});
```

---

## 4. Scroll, Touch & Input Handlers

### The Passive Event Listener Violation

```
[Violation] Added non-passive event listener to a scroll-blocking 'touchstart' event.
Consider marking event handler as 'passive' to make the page more responsive.
```

This violation occurs because scroll-related events (`touchstart`, `touchmove`, `wheel`, `mousewheel`) block scrolling until the handler returns. Browsers must wait to see if `preventDefault()` is called.

```javascript
// ❌ VIOLATION: Blocking scroll
window.addEventListener('touchstart', handler);
window.addEventListener('wheel', handler);

// ✅ CORRECT: Non-blocking passive listener
window.addEventListener('touchstart', handler, { passive: true });
window.addEventListener('wheel', handler, { passive: true });
window.addEventListener('touchmove', handler, { passive: true });

// ⚠️ Only use non-passive when you NEED to call preventDefault()
// e.g., custom scroll containers or drag-and-drop
element.addEventListener('touchmove', (e) => {
  e.preventDefault(); // Prevent native scroll (requires non-passive)
  handleDrag(e);
}, { passive: false }); // explicit non-passive
```

### Throttle & Debounce Scroll Handlers

```javascript
// ❌ VIOLATION: Heavy work in scroll handler (fires 60+ times/sec)
window.addEventListener('scroll', () => {
  updateStickyNav();        // Reads layout → forced reflow
  updateParallaxElements(); // DOM writes
  checkVisibility();        // More layout reads
}, { passive: true });

// ✅ CORRECT: Use rAF to throttle scroll work to once per frame
function createRAFThrottled(fn) {
  let rafId = null;
  return function (...args) {
    if (rafId) return; // Skip if already scheduled
    rafId = requestAnimationFrame(() => {
      fn.apply(this, args);
      rafId = null;
    });
  };
}

const throttledScrollHandler = createRAFThrottled(() => {
  // All DOM reads and writes happen inside rAF — safe
  const scrollY = window.scrollY;
  updateStickyNav(scrollY);
  updateParallaxElements(scrollY);
});

window.addEventListener('scroll', throttledScrollHandler, { passive: true });

// ✅ ALTERNATIVE: Debounce for "scroll end" detection
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

const onScrollEnd = debounce(() => {
  // Heavy work that only needs to run when scrolling stops
  lazyLoadImages();
  updateAnalytics();
}, 150);

window.addEventListener('scroll', onScrollEnd, { passive: true });
```

### Input Handler Violations

```javascript
// ❌ VIOLATION: 'click' handler took 250ms
button.addEventListener('click', async () => {
  const data = await fetchData();   // ✓ async — ok
  processLargeArray(data);          // ✗ synchronous heavy work
  updateManyDOMElements(data);      // ✗ hundreds of DOM writes
});

// ✅ CORRECT: Immediate feedback, defer heavy work
button.addEventListener('click', async () => {
  // 1. Immediate visual feedback (< 1ms)
  button.disabled = true;
  showSpinner();

  // 2. Async fetch (non-blocking)
  const data = await fetchData();

  // 3. Yield before heavy processing
  await yieldToMain();

  // 4. Process in chunks
  const results = await processInChunks(data);

  // 5. Update UI
  renderResults(results);
  hideSpinner();
  button.disabled = false;
});
```

---

## 5. requestAnimationFrame & Visual Updates

### When to Use rAF

```javascript
// rAF runs BEFORE the browser paints — it's for visual updates ONLY
// Budget: 16.67ms per frame (60fps), 8.33ms (120fps)

// ✅ CORRECT uses of rAF
requestAnimationFrame(() => {
  // Animation updates
  element.style.transform = `translateX(${x}px)`;

  // Canvas rendering
  ctx.drawImage(sprite, x, y);

  // Reading layout for the CURRENT frame only
  const rect = element.getBoundingClientRect();
  updateOverlay(rect);
});

// ❌ WRONG: Using rAF for non-visual work
requestAnimationFrame(() => {
  processData(largeArray);       // Not visual — use setTimeout or Worker
  sendAnalyticsEvent();          // Not visual — use queueMicrotask or idle callback
  updateLocalStorage();          // Not visual — use idle callback
});
```

### The Animation Loop Pattern

```javascript
class AnimationLoop {
  #rafId = null;
  #lastTime = 0;
  #running = false;

  start() {
    if (this.#running) return;
    this.#running = true;
    this.#rafId = requestAnimationFrame(this.#loop.bind(this));
  }

  stop() {
    this.#running = false;
    if (this.#rafId !== null) {
      cancelAnimationFrame(this.#rafId);
      this.#rafId = null;
    }
  }

  #loop(timestamp) {
    if (!this.#running) return;

    const delta = timestamp - this.#lastTime;
    this.#lastTime = timestamp;

    // Skip frames where delta is too large (tab was hidden)
    if (delta < 200) {
      this.update(delta, timestamp);
      this.render();
    }

    this.#rafId = requestAnimationFrame(this.#loop.bind(this));
  }

  update(delta, timestamp) {
    // Override in subclass: update game/animation state
  }

  render() {
    // Override in subclass: DOM/canvas writes only
  }
}

// Page Visibility API: pause animations when tab is hidden
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    loop.stop(); // Don't burn CPU when tab is hidden
  } else {
    loop.start();
  }
});
```

### rAF Scheduling Budget

```javascript
// Measure your rAF work to stay under budget
function timedRaf(label, fn) {
  requestAnimationFrame(() => {
    const start = performance.now();
    fn();
    const duration = performance.now() - start;

    if (duration > 10) { // Warning at 10ms (leaving 6ms buffer)
      console.warn(`[rAF Budget] ${label} took ${duration.toFixed(2)}ms — risk of dropped frames`);
    }
  });
}
```

---

## 6. Timers: setTimeout & setInterval

### Timer Violation Pattern

```
[Violation] 'setTimeout' handler took 180ms
```

```javascript
// ❌ VIOLATION: Heavy synchronous work inside timer
setTimeout(() => {
  const result = processEntireDataset(items); // blocks for 180ms
  updateUI(result);
}, 0);

// ✅ CORRECT: Chunk work inside timer callbacks
setTimeout(async () => {
  const result = await processInChunks(items); // non-blocking
  updateUI(result);
}, 0);
```

### Minimum Timer Resolution

```javascript
// Browsers clamp minimum setTimeout delay:
// - Active tab: ~4ms minimum
// - Background tab: ~1000ms (1 second) — important for timers!
// - Throttled (low-power): ~125ms

// ❌ DO NOT use setTimeout(fn, 0) for animation
// Use requestAnimationFrame instead:
setTimeout(() => element.style.opacity = '1', 0); // wrong — may cause flicker

requestAnimationFrame(() => {
  element.style.opacity = '1'; // correct — syncs with paint
});

// ✅ For truly deferred low-priority work, use requestIdleCallback
requestIdleCallback((deadline) => {
  while (deadline.timeRemaining() > 0 && tasks.length > 0) {
    tasks.shift()(); // Run tasks while browser is idle
  }
}, { timeout: 2000 }); // Ensure execution within 2s max
```

### setInterval Pitfalls

```javascript
// ❌ PROBLEM: setInterval doesn't account for execution time
// If handler takes 50ms and interval is 100ms, next run starts 100ms after START
// This can cause overlapping executions and drift

let intervalId = setInterval(() => {
  slowOperation(); // 50ms — causes overlap if interval < 50ms
}, 30); // 30ms < 50ms execution = OVERLAP

// ✅ CORRECT: Use recursive setTimeout for precision
function scheduleNext() {
  setTimeout(async () => {
    await slowOperation();
    scheduleNext(); // Schedule next AFTER completion
  }, 30);
}
scheduleNext();

// ✅ ALWAYS clean up timers to prevent memory leaks
class PollingManager {
  #timerId = null;

  start(fn, interval) {
    this.stop(); // Clear any existing timer
    const poll = async () => {
      await fn();
      this.#timerId = setTimeout(poll, interval);
    };
    this.#timerId = setTimeout(poll, interval);
  }

  stop() {
    if (this.#timerId !== null) {
      clearTimeout(this.#timerId);
      this.#timerId = null;
    }
  }
}
```

---

## 7. DOM Manipulation Patterns

### Document Fragment for Batch Inserts

```javascript
// ❌ VIOLATION: Inserting elements one-by-one causes multiple reflows
function badRenderList(items) {
  const ul = document.getElementById('list');
  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.name;
    ul.appendChild(li); // triggers reflow on each append
  });
}

// ✅ CORRECT: Use DocumentFragment to batch insertions
function goodRenderList(items) {
  const ul = document.getElementById('list');
  const fragment = document.createDocumentFragment();

  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.name;
    fragment.appendChild(li); // no reflow — fragment is off-DOM
  });

  ul.appendChild(fragment); // single reflow
}

// ✅ EVEN BETTER: innerHTML with sanitization for large lists
function fastRenderList(items) {
  const ul = document.getElementById('list');
  // Build HTML string (fastest for large datasets)
  const html = items.map(item =>
    `<li data-id="${escapeHtml(item.id)}">${escapeHtml(item.name)}</li>`
  ).join('');
  ul.innerHTML = html; // single parse + render
}

// Always sanitize user data to prevent XSS
function escapeHtml(str) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  return String(str).replace(/[&<>"']/g, m => map[m]);
}
```

### Virtual DOM Reconciliation (Manual)

```javascript
// Efficient DOM diffing without a framework
function patchList(container, newItems, getKey) {
  const oldNodes = new Map();

  // Index existing nodes by key
  Array.from(container.children).forEach(node => {
    oldNodes.set(node.dataset.key, node);
  });

  const fragment = document.createDocumentFragment();

  for (const item of newItems) {
    const key = getKey(item);
    let node = oldNodes.get(key);

    if (node) {
      // Update existing node
      updateNode(node, item);
      oldNodes.delete(key);
    } else {
      // Create new node
      node = createNode(item);
    }
    fragment.appendChild(node);
  }

  // Remove nodes no longer in list
  oldNodes.forEach(node => node.remove());

  container.appendChild(fragment);
}
```

### CSS Class Toggling vs Inline Styles

```javascript
// ❌ BAD: Multiple inline style changes = multiple reflows
function showError(el) {
  el.style.color = 'red';
  el.style.border = '1px solid red';
  el.style.background = '#fff0f0';
  el.style.padding = '8px';
}

// ✅ GOOD: Single class toggle = one style recalculation
// (CSS handles the rest in the stylesheet)
function showError(el) {
  el.classList.add('has-error'); // single operation
}

// ✅ ALSO GOOD: cssText for multiple inline changes
function showError(el) {
  el.style.cssText = 'color: red; border: 1px solid red; background: #fff0f0; padding: 8px;';
}
```

---

## 8. Memory Management & Leaks

### Common Leak Patterns

```javascript
// ❌ LEAK #1: Event listeners not removed
class Component {
  constructor() {
    // Closure captures `this` → prevents GC
    document.addEventListener('keydown', (e) => this.handleKey(e));
    window.addEventListener('resize', () => this.handleResize());
    // These are NEVER removed — leak on every Component instantiation
  }
}

// ✅ CORRECT: Store references and remove on cleanup
class Component {
  #handleKey;
  #handleResize;

  constructor() {
    // Bind once so we can remove the same reference later
    this.#handleKey = this.handleKey.bind(this);
    this.#handleResize = this.handleResize.bind(this);

    document.addEventListener('keydown', this.#handleKey);
    window.addEventListener('resize', this.#handleResize);
  }

  destroy() {
    document.removeEventListener('keydown', this.#handleKey);
    window.removeEventListener('resize', this.#handleResize);
  }

  handleKey(e) { /* ... */ }
  handleResize() { /* ... */ }
}

// ✅ MODERN: AbortController for declarative cleanup
class Component {
  #abortController = new AbortController();

  constructor() {
    const { signal } = this.#abortController;
    document.addEventListener('keydown', this.handleKey.bind(this), { signal });
    window.addEventListener('resize', this.handleResize.bind(this), { signal });
    // All listeners removed when signal is aborted
  }

  destroy() {
    this.#abortController.abort(); // removes ALL listeners at once
  }
}
```

```javascript
// ❌ LEAK #2: Timers holding references
class Ticker {
  start() {
    this.timer = setInterval(() => {
      this.update(); // `this` is kept alive by the closure
    }, 1000);
  }
  // If destroy() is never called, `this` is never GC'd
}

// ✅ CORRECT
class Ticker {
  #timer = null;

  start() {
    this.#timer = setInterval(() => this.update(), 1000);
  }

  destroy() {
    clearInterval(this.#timer);
    this.#timer = null;
  }
}
```

```javascript
// ❌ LEAK #3: Detached DOM nodes kept in closures
let cachedElement = null;

function cacheElement() {
  cachedElement = document.getElementById('modal');
}

function removeModal() {
  document.getElementById('modal').remove();
  // cachedElement still holds reference → memory leak!
  // The element is removed from DOM but NOT garbage collected
}

// ✅ CORRECT: Use WeakRef for optional caches
let cachedRef = null;

function cacheElement() {
  const el = document.getElementById('modal');
  cachedRef = new WeakRef(el); // doesn't prevent GC
}

function getElement() {
  return cachedRef?.deref(); // returns undefined if GC'd
}
```

### WeakMap & WeakSet for Associated Data

```javascript
// ❌ BAD: Regular Map keeps DOM nodes alive
const elementData = new Map();

function attachData(el, data) {
  elementData.set(el, data); // el is never GC'd even after removal
}

// ✅ GOOD: WeakMap allows GC when element is removed
const elementData = new WeakMap();

function attachData(el, data) {
  elementData.set(el, data); // el can be GC'd when removed from DOM
}
```

---

## 9. Network & Resource Loading

### Avoid Blocking Resource Loading

```html
<!-- ❌ BAD: Render-blocking scripts in <head> -->
<head>
  <script src="analytics.js"></script>
  <script src="app.js"></script>
</head>

<!-- ✅ CORRECT: defer for execution-order-dependent scripts -->
<head>
  <script src="app.js" defer></script>
</head>

<!-- ✅ CORRECT: async for independent scripts (analytics, ads) -->
<head>
  <script src="analytics.js" async></script>
</head>

<!-- ✅ CORRECT: module scripts are deferred by default -->
<script type="module" src="main.js"></script>
```

### Resource Hints

```html
<!-- Preconnect: establish early TCP/TLS to critical origins -->
<link rel="preconnect" href="https://api.example.com">
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>

<!-- Preload: force high-priority fetch for critical resources -->
<link rel="preload" href="/critical.css" as="style">
<link rel="preload" href="/hero-font.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/hero-image.webp" as="image">

<!-- Prefetch: low-priority fetch for next-page resources -->
<link rel="prefetch" href="/next-page-bundle.js">

<!-- DNS prefetch: resolve DNS for third-party domains -->
<link rel="dns-prefetch" href="https://cdn.example.com">
```

### Fetch Patterns

```javascript
// ✅ Abort fetch requests to prevent stale updates
class DataFetcher {
  #abortController = null;

  async fetch(url) {
    // Cancel any in-flight request
    this.#abortController?.abort();
    this.#abortController = new AbortController();

    try {
      const response = await fetch(url, {
        signal: this.#abortController.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (err) {
      if (err.name === 'AbortError') return null; // Expected — not an error
      throw err;
    }
  }
}

// ✅ Parallel fetching (don't await sequentially when independent)
async function loadDashboard(userId) {
  // ❌ Sequential — takes sum of all durations
  // const user = await fetchUser(userId);
  // const posts = await fetchPosts(userId);
  // const stats = await fetchStats(userId);

  // ✅ Parallel — takes max duration
  const [user, posts, stats] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchStats(userId),
  ]);

  return { user, posts, stats };
}
```

---

## 10. Web Workers & Off-Thread Computation

### Moving Heavy Work Off the Main Thread

```javascript
// ❌ VIOLATION: Heavy computation on main thread
function calculatePrimes(max) {
  // This blocks the UI for potentially seconds
  const sieve = new Uint8Array(max + 1);
  // ... Sieve of Eratosthenes
  return primes;
}

// ✅ CORRECT: Run in a Web Worker
// worker.js
self.onmessage = function({ data: { max } }) {
  const primes = calculatePrimes(max);
  self.postMessage({ primes });
};

// main.js
class PrimeWorker {
  #worker;
  #pendingResolvers = new Map();
  #requestId = 0;

  constructor() {
    this.#worker = new Worker('/worker.js');
    this.#worker.onmessage = ({ data }) => {
      const resolve = this.#pendingResolvers.get(data.id);
      if (resolve) {
        resolve(data.primes);
        this.#pendingResolvers.delete(data.id);
      }
    };
  }

  calculate(max) {
    return new Promise((resolve) => {
      const id = this.#requestId++;
      this.#pendingResolvers.set(id, resolve);
      this.#worker.postMessage({ id, max });
    });
  }

  destroy() {
    this.#worker.terminate();
  }
}
```

### Transferable Objects (Zero-Copy)

```javascript
// ❌ SLOW: Serializing large buffers (copies data)
const largeArray = new Float64Array(1_000_000);
worker.postMessage({ data: largeArray }); // copies 8MB!

// ✅ FAST: Transfer ownership (zero-copy, O(1))
worker.postMessage({ data: largeArray }, [largeArray.buffer]);
// largeArray.buffer is now NEUTERED — main thread can't access it

// Worker sends back result as transferable too:
self.onmessage = ({ data }) => {
  const result = processData(data.data);
  self.postMessage({ result }, [result.buffer]); // transfer back
};
```

### SharedArrayBuffer & Atomics

```javascript
// For true shared memory between main thread and workers
// Requires Cross-Origin Isolation (COOP + COEP headers)

const sharedBuffer = new SharedArrayBuffer(4);
const sharedArray = new Int32Array(sharedBuffer);

// Worker can read/write without transfer
worker.postMessage({ buffer: sharedBuffer });

// Atomic operations for thread-safe access
Atomics.store(sharedArray, 0, 42);
const value = Atomics.load(sharedArray, 0);
Atomics.add(sharedArray, 0, 1); // thread-safe increment

// Wait/notify for worker synchronization
// In worker (blocks worker thread, NOT main thread)
Atomics.wait(sharedArray, 0, 0); // wait until index 0 !== 0

// In main thread
Atomics.notify(sharedArray, 0); // wake up waiting worker
```

---

## 11. Async Patterns & Microtasks

### Microtask Queue Starvation

```javascript
// ❌ DANGER: Infinite microtask loop — starves the event loop
async function infiniteRecursion() {
  await Promise.resolve(); // queues a microtask
  infiniteRecursion();     // immediately queues another
  // The event loop NEVER gets to run tasks or render!
}

// ❌ ALSO DANGEROUS: Synchronous promise resolution flood
function queueMillion() {
  for (let i = 0; i < 1_000_000; i++) {
    Promise.resolve().then(() => {}); // 1M microtasks before next task
  }
}

// ✅ CORRECT: Use macrotask scheduling for deferred work
async function deferredWork() {
  await new Promise(resolve => setTimeout(resolve, 0)); // macrotask
  // Now other tasks can run between iterations
  doWork();
}
```

### async/await Best Practices

```javascript
// ✅ Use Promise.allSettled for operations that can independently fail
async function fetchMultiple(urls) {
  const results = await Promise.allSettled(urls.map(url => fetch(url)));

  return results.map((result, i) => ({
    url: urls[i],
    success: result.status === 'fulfilled',
    data: result.status === 'fulfilled' ? result.value : null,
    error: result.status === 'rejected' ? result.reason : null,
  }));
}

// ✅ Race with timeout for reliability
function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms)
  );
  return Promise.race([promise, timeout]);
}

// ✅ Retry with exponential backoff
async function fetchWithRetry(url, options = {}) {
  const { retries = 3, backoff = 300 } = options;

  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      return await fetch(url);
    } catch (err) {
      if (attempt === retries - 1) throw err;
      await new Promise(r => setTimeout(r, backoff * 2 ** attempt));
    }
  }
}
```

---

## 12. Rendering Pipeline & CSS Performance

### Understanding the Pipeline

```
JavaScript → Style → Layout → Paint → Composite
              ↑          ↑        ↑          ↑
           cheapest   expensive  medium   cheapest

Composite-only properties (no Layout or Paint):
  transform, opacity → GPU-accelerated → FREE

Paint-triggering properties (skips Layout):
  color, background-color, box-shadow, border-radius

Layout-triggering properties (most expensive):
  width, height, padding, margin, top, left, font-size
```

### CSS Containment

```css
/* Tell the browser: this element is isolated from the rest of the page */
/* Allows browser to skip layout/paint work outside the container */

.card {
  contain: layout style; /* Layout changes inside don't affect outside */
}

.widget {
  contain: strict; /* Full containment — layout, style, paint, size */
}

/* content-visibility: auto — skip rendering off-screen content */
.long-list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px; /* Estimated size while off-screen */
}
```

```javascript
// ✅ Animate with transform instead of position properties
// ❌ Triggers Layout + Paint + Composite (expensive)
element.style.left = `${x}px`;
element.style.top = `${y}px`;

// ✅ Triggers Composite only (cheapest)
element.style.transform = `translate(${x}px, ${y}px)`;

// ✅ will-change hints compositor to promote element to its own layer
// Use SPARINGLY — each layer uses GPU memory
element.style.willChange = 'transform';
// Apply before animation starts, remove after
element.addEventListener('animationend', () => {
  element.style.willChange = 'auto';
});
```

### CSS Animations vs JS Animations

```javascript
// ✅ CSS Animations: compositor-thread, no JS required
// styles.css:
// .slide-in { animation: slideIn 300ms ease-out forwards; }
// @keyframes slideIn { from { transform: translateX(-100%); } to { transform: translateX(0); } }

element.classList.add('slide-in'); // trigger via class only

// ✅ Web Animations API: programmatic + compositor-thread
const animation = element.animate([
  { transform: 'translateX(-100%)', opacity: 0 },
  { transform: 'translateX(0)', opacity: 1 },
], {
  duration: 300,
  easing: 'ease-out',
  fill: 'forwards',
});

animation.onfinish = () => {
  element.style.transform = 'translateX(0)';
  element.style.opacity = '1';
};

// Cancel or pause as needed
animation.pause();
animation.cancel();
```

---

## 13. Observers API

### IntersectionObserver (Replace Scroll-Based Visibility)

```javascript
// ❌ OLD: Scroll-based visibility check (causes forced reflow!)
window.addEventListener('scroll', () => {
  elements.forEach(el => {
    const rect = el.getBoundingClientRect(); // forced layout read
    if (rect.top < window.innerHeight) {
      el.classList.add('visible');
    }
  });
}, { passive: true });

// ✅ CORRECT: IntersectionObserver — no scroll handler, no reflow
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // stop watching once visible
    }
  });
}, {
  root: null,          // viewport
  rootMargin: '0px 0px -100px 0px', // trigger 100px before edge
  threshold: 0.1,      // 10% visibility threshold
});

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});
```

### ResizeObserver (Replace Window Resize)

```javascript
// ❌ OLD: window resize (fires too often, layout thrashing)
window.addEventListener('resize', () => {
  updateChartSize(); // reads element dimensions → forced reflow
});

// ✅ CORRECT: ResizeObserver — fires only when element size changes
const resizeObserver = new ResizeObserver((entries) => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    updateChart(entry.target, width, height);
  }
});

resizeObserver.observe(chartContainer);

// Cleanup
resizeObserver.disconnect();
```

### MutationObserver (Replace DOM Polling)

```javascript
// ❌ BAD: Polling for DOM changes
const interval = setInterval(() => {
  if (document.querySelector('.dynamic-element')) {
    handleElement();
    clearInterval(interval);
  }
}, 100);

// ✅ CORRECT: MutationObserver — event-driven, no polling
const mutationObserver = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    for (const node of mutation.addedNodes) {
      if (node.matches?.('.dynamic-element')) {
        handleElement(node);
        mutationObserver.disconnect();
        return;
      }
    }
  }
});

mutationObserver.observe(document.body, {
  childList: true,
  subtree: true,
  // Only observe what you need — broad observation is expensive
  // attributes: false,    // don't watch attributes
  // characterData: false, // don't watch text changes
});
```

---

## 14. Performance Measurement & Profiling

### User Timing API

```javascript
// Mark and measure your own operations
performance.mark('data-fetch-start');

const data = await fetchData();

performance.mark('data-fetch-end');
performance.measure('data-fetch', 'data-fetch-start', 'data-fetch-end');

const [measure] = performance.getEntriesByName('data-fetch');
console.log(`Fetch took: ${measure.duration.toFixed(2)}ms`);

// Clean up marks
performance.clearMarks();
performance.clearMeasures();
```

### Web Vitals Monitoring

```javascript
// Core Web Vitals: LCP, CLS, INP (replaced FID in 2024)
import { onLCP, onCLS, onINP, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics({ name, delta, value, id, rating }) {
  navigator.sendBeacon('/analytics', JSON.stringify({
    metric: name,
    value: Math.round(name === 'CLS' ? delta * 1000 : delta),
    id,
    rating, // 'good' | 'needs-improvement' | 'poor'
  }));
}

onLCP(sendToAnalytics);   // Largest Contentful Paint  (<2.5s good)
onCLS(sendToAnalytics);   // Cumulative Layout Shift   (<0.1 good)
onINP(sendToAnalytics);   // Interaction to Next Paint (<200ms good)
onFCP(sendToAnalytics);   // First Contentful Paint
onTTFB(sendToAnalytics);  // Time to First Byte
```

### PerformanceObserver for Production Monitoring

```javascript
class PerformanceMonitor {
  #observers = [];

  init() {
    // Long Tasks
    this.#observe('longtask', (entries) => {
      entries.forEach(entry => {
        if (entry.duration > 100) {
          this.report('critical-long-task', entry);
        }
      });
    });

    // Layout Shifts
    this.#observe('layout-shift', (entries) => {
      entries.forEach(entry => {
        if (!entry.hadRecentInput && entry.value > 0.01) {
          this.report('layout-shift', entry);
        }
      });
    });

    // Resource Timing
    this.#observe('resource', (entries) => {
      entries.forEach(entry => {
        if (entry.duration > 1000) { // > 1s
          this.report('slow-resource', { name: entry.name, duration: entry.duration });
        }
      });
    });
  }

  #observe(type, callback) {
    try {
      const observer = new PerformanceObserver((list) => {
        callback(list.getEntries());
      });
      observer.observe({ type, buffered: true });
      this.#observers.push(observer);
    } catch {
      // Some metrics not available in all browsers
    }
  }

  report(type, data) {
    // Send to your monitoring system (Datadog, New Relic, etc.)
    queueMicrotask(() => {
      navigator.sendBeacon('/perf', JSON.stringify({ type, data, url: location.href }));
    });
  }

  destroy() {
    this.#observers.forEach(o => o.disconnect());
  }
}
```

---

## 15. React & Framework-Specific Patterns

### React Concurrent Features

```jsx
import { useState, useTransition, useDeferredValue, useCallback, memo } from 'react';

// ✅ useTransition: mark state updates as non-urgent
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    setQuery(e.target.value); // Urgent: update input immediately

    startTransition(() => {
      // Non-urgent: search can be interrupted by user input
      setResults(searchDatabase(e.target.value));
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  );
}

// ✅ useDeferredValue: defer expensive renders
function ResultsList({ query }) {
  const deferredQuery = useDeferredValue(query);
  // deferredQuery lags behind query — React renders the stale version
  // while computing the new one, preventing input blocking
  const results = useMemo(() => expensiveFilter(data, deferredQuery), [deferredQuery]);

  return <ul>{results.map(r => <li key={r.id}>{r.name}</li>)}</ul>;
}
```

### React Memoization

```jsx
// ✅ memo: skip re-render when props haven't changed
const ExpensiveComponent = memo(({ data, onAction }) => {
  return <div>{/* expensive render */}</div>;
}, (prevProps, nextProps) => {
  // Custom comparison (return true to SKIP re-render)
  return prevProps.data.id === nextProps.data.id;
});

// ✅ useCallback: stable function references
function Parent() {
  const [count, setCount] = useState(0);

  // Without useCallback: new function every render → child re-renders
  // With useCallback: same reference → child skips re-render (if memo'd)
  const handleClick = useCallback((id) => {
    setCount(prev => prev + 1);
    doSomethingWith(id);
  }, []); // stable — no dependencies change

  return <ExpensiveComponent data={data} onAction={handleClick} />;
}

// ✅ useMemo: memoize expensive computations
function DataTable({ rawData, filters }) {
  const processedData = useMemo(() => {
    return rawData
      .filter(row => matchesFilters(row, filters))
      .sort((a, b) => a.date - b.date)
      .map(row => transformRow(row));
  }, [rawData, filters]); // only recompute when these change

  return <Table data={processedData} />;
}
```

### React: Avoiding Common Re-render Causes

```jsx
// ❌ COMMON MISTAKE: Object/array literals in JSX
function Parent() {
  return (
    <Child
      style={{ padding: 8 }}    // new object every render
      items={[1, 2, 3]}          // new array every render
      config={{ theme: 'dark' }} // new object every render
    />
  );
  // Even if Child is memo'd, it will ALWAYS re-render
}

// ✅ CORRECT: Define outside component or useMemo/useCallback
const CHILD_STYLE = { padding: 8 };
const CHILD_ITEMS = [1, 2, 3];
const CHILD_CONFIG = { theme: 'dark' };

function Parent() {
  return (
    <Child
      style={CHILD_STYLE}
      items={CHILD_ITEMS}
      config={CHILD_CONFIG}
    />
  );
}
```

---

## 16. Service Workers & Caching Strategies

### Cache-First Strategy

```javascript
// service-worker.js
const CACHE_NAME = 'app-v1';
const STATIC_ASSETS = ['/index.html', '/main.js', '/styles.css'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting(); // Activate immediately
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(names =>
      Promise.all(
        names
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name)) // Delete old caches
      )
    )
  );
  self.clients.claim(); // Take control immediately
});

self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Cache-first for static assets
  if (STATIC_ASSETS.some(path => request.url.includes(path))) {
    event.respondWith(
      caches.match(request).then(cached =>
        cached || fetch(request).then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
          return response;
        })
      )
    );
    return;
  }

  // Network-first for API calls
  if (request.url.includes('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
          return response;
        })
        .catch(() => caches.match(request)) // Fallback to cache if offline
    );
  }
});
```

---

## 17. Production Checklist

### Pre-Deployment Performance Audit

```
MAIN THREAD
[ ] No synchronous operations > 50ms in event handlers
[ ] All scroll/touch event listeners use { passive: true }
[ ] No forced synchronous layout (reads after writes in loops)
[ ] Heavy computations moved to Web Workers
[ ] requestAnimationFrame used for all visual updates
[ ] requestIdleCallback used for non-urgent work
[ ] scheduler.yield() or MessageChannel used for chunking

MEMORY
[ ] All event listeners have corresponding removeEventListener / AbortController
[ ] All timers have corresponding clearTimeout / clearInterval
[ ] WeakRef/WeakMap used for element-associated data
[ ] No detached DOM nodes held in closures
[ ] Worker.terminate() called when workers are no longer needed

DOM
[ ] DOM reads/writes are batched (reads first, then writes)
[ ] DocumentFragment used for bulk DOM insertions
[ ] CSS classes used instead of multiple inline style mutations
[ ] Virtual/recycled lists used for large datasets (> 100 items)

NETWORK
[ ] Critical scripts use defer or async
[ ] Key resources preloaded with <link rel="preload">
[ ] Fetch requests are cancelable via AbortController
[ ] Independent async operations use Promise.all, not sequential await

RENDERING
[ ] Animations use transform/opacity (compositor-only properties)
[ ] will-change used sparingly and removed after animation
[ ] CSS contain applied to isolated components
[ ] content-visibility: auto on long lists

MEASUREMENT
[ ] Long Task observer active in production
[ ] Core Web Vitals (LCP, CLS, INP) tracked and reported
[ ] Performance marks/measures around critical user flows
[ ] Lighthouse CI integrated into CI/CD pipeline
```

### Lighthouse CI Integration

```yaml
# .github/workflows/perf.yml
name: Performance Audit
on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v11
        with:
          urls: |
            http://localhost:3000
          budgetPath: ./lighthouse-budget.json
          uploadArtifacts: true

# lighthouse-budget.json
# {
#   "budgets": [{
#     "resourceSizes": [{ "resourceType": "script", "budget": 300 }],
#     "timings": [
#       { "metric": "interactive", "budget": 3000 },
#       { "metric": "first-contentful-paint", "budget": 1500 }
#     ]
#   }]
# }
```

---

## Quick Reference: Violation → Fix

| Violation Message | Fix |
|---|---|
| `'click' handler took Xms` | Move heavy work off main thread; use `yieldToMain()` |
| `Forced reflow while executing JavaScript` | Batch reads before writes; use FastDOM pattern |
| `Added non-passive event listener to scroll-blocking event` | Add `{ passive: true }` option |
| `'setTimeout' handler took Xms` | Chunk work; use `async/await` + `yieldToMain()` |
| `requestAnimationFrame handler took Xms` | Reduce work per frame; move non-visual work out of rAF |
| `Long Task` in DevTools | Use `PerformanceObserver` to find source; chunk or offload |
| `[Intervention] Your page does not scroll smoothly` | Remove/passify scroll event handlers |
| Layout Thrashing in Timeline | Separate read and write phases |

---

*Based on: RAIL Model (Google), W3C Long Tasks API, WHATWG HTML Living Standard, Web Vitals initiative, Chrome DevTools Violations documentation, MDN Web Performance Guide.*
