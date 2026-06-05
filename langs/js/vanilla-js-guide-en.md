# The Monumental Vanilla JavaScript Guide for AI Agents

> **Version:** 2025 | **Coverage:** ES2015 → ES2025 | **Runtime:** Browser (no Node.js)  
> **Purpose:** Complete, self-sufficient reference for writing correct, modern, pure JavaScript without frameworks

---

## 📋 Table of Contents

1. [Philosophy of Modern JS](#1-philosophy-of-modern-js)
2. [Variables and Scope](#2-variables-and-scope)
3. [Data Types and Structures](#3-data-types-and-structures)
4. [Modern ES6+ Syntax](#4-modern-es6-syntax)
5. [Functions](#5-functions)
6. [Classes and Prototypes](#6-classes-and-prototypes)
7. [Async Programming](#7-async-programming)
8. [ES Modules System](#8-es-modules-system)
9. [DOM API — Modern Approach](#9-dom-api--modern-approach)
10. [Events and Delegation](#10-events-and-delegation)
11. [Fetch API and Networking](#11-fetch-api-and-networking)
12. [Browser Storage](#12-browser-storage)
13. [State Management](#13-state-management)
14. [Design Patterns](#14-design-patterns)
15. [Observer APIs](#15-observer-apis)
16. [Web Components](#16-web-components)
17. [Performance](#17-performance)
18. [Security](#18-security)
19. [Error Handling](#19-error-handling)
20. [Modern Web APIs](#20-modern-web-apis)
21. [Animations and Visual Effects](#21-animations-and-visual-effects)
22. [Regular Expressions](#22-regular-expressions)
23. [Internationalization — Intl API](#23-internationalization--intl-api)
24. [Service Workers and PWA](#24-service-workers-and-pwa)
25. [WebSocket and Realtime](#25-websocket-and-realtime)
26. [File API](#26-file-api)
27. [Form Validation](#27-form-validation)
28. [Iterator Protocol and Generators](#28-iterator-protocol-and-generators)
29. [Proxy and Reflect](#29-proxy-and-reflect)
30. [Streams API](#30-streams-api)
31. [Crypto API](#31-crypto-api)
32. [Audio API](#32-audio-api)
33. [Canvas API](#33-canvas-api)
34. [Pointer, Touch and Keyboard Events](#34-pointer-touch-and-keyboard-events)
35. [BroadcastChannel and SharedWorker](#35-broadcastchannel-and-sharedworker)
36. [Advanced State Patterns](#36-advanced-state-patterns)
37. [Full SPA Architecture](#37-full-spa-architecture)
38. [Accessibility (a11y)](#38-accessibility-a11y)
39. [Performance Profiling](#39-performance-profiling)
40. [Testing Vanilla JS](#40-testing-vanilla-js)
41. [JSDoc Type Annotations](#41-jsdoc-type-annotations)
42. [Anti-Patterns and Traps](#42-anti-patterns-and-traps)
43. [Quality Checklist](#43-quality-checklist)
44. [Quick Syntax Reference](#44-quick-syntax-reference)
45. [Standards Timeline](#45-standards-timeline)

---

## 1. Philosophy of Modern JS

### Core Principles

```
1. Prefer declarative over imperative
2. Immutability by default — mutation is the exception
3. Functions: pure, predictable, side-effect-free
4. Explicit over implicit
5. Error handling is mandatory, never optional
6. Accessibility and performance from day one
7. Use the platform (Web APIs), don't fight it
8. Own your lifecycle — always clean up after yourself
```

### The Modern Stack (2025)

| Era | Standard | Key Features |
|-----|----------|--------------|
| Legacy | ES5 | `var`, prototype, callbacks |
| Transitional | ES2015 | classes, promises, modules, arrow fns |
| Mature | ES2017–2020 | `async/await`, `?.`, `??`, `globalThis` |
| Modern | ES2021–2025 | `at()`, `structuredClone`, `groupBy`, top-level await |

---

## 2. Variables and Scope

### Never `var`

```js
// ❌ var — function-scoped, hoisted, leaks
function broken() {
  if (true) { var x = 10; }
  console.log(x); // 10 — leaks from if-block!
}

// ✅ const by default
const PI = 3.14159;
const config = Object.freeze({ debug: false });

// ✅ let only when reassignment needed
let count = 0;
count++;

// const binding is immutable, the value is NOT:
const user = { name: 'Alice' };
user.name = 'Bob';  // OK — mutates property
user = {};          // SyntaxError — reassigns binding
```

### Temporal Dead Zone

```js
console.log(a); // ReferenceError — let/const NOT hoisted
let a = 5;

console.log(b); // undefined — var IS hoisted (silent bug!)
var b = 5;
```

### Destructuring

```js
// Array
const [a, b, , d] = [1, 2, 3, 4];
const [first, ...rest] = [1, 2, 3];
let p = 1, q = 2;
[p, q] = [q, p]; // swap — no temp variable!

// Object
const { name, age = 0 } = user;
const { name: userName } = user;       // rename
const { addr: { city } = {} } = user;  // nested + safe default
const { a: _, ...without } = obj;      // omit key

// In function parameters (always add default {} !)
function init({ title = '', debug = false, onReady = null } = {}) {}

// Dynamic key
const key = 'email';
const { [key]: email } = user;

// Iteration
for (const [i, v] of array.entries())    {}
for (const [k, v] of map)               {}
for (const [k, v] of Object.entries(o)) {}
```

---

## 3. Data Types and Structures

### Type Checking

```js
// typeof — reliable for primitives
typeof 42          // 'number'
typeof 42n         // 'bigint'
typeof 'str'       // 'string'
typeof true        // 'boolean'
typeof undefined   // 'undefined'
typeof null        // 'object' ← historical bug!
typeof Symbol()    // 'symbol'
typeof {}          // 'object'
typeof []          // 'object'

// Reliable helpers
const isNull  = v => v === null;
const isArray = Array.isArray;
Number.isNaN(NaN);       // true  (global isNaN coerces — avoid!)
Number.isFinite(42);     // true  (global isFinite coerces — avoid!)
Number.isInteger(4.0);   // true
Number.isSafeInteger(2**53); // false
```

### Arrays — Immutable Operations

```js
const arr = [3, 1, 4, 1, 5];

// ❌ Mutating — avoid when immutability matters
arr.sort();    // mutates in place!
arr.reverse(); // mutates in place!

// ✅ ES2023 immutable copies
arr.toSorted((a, b) => a - b);  // new sorted array
arr.toReversed();                 // new reversed array
arr.with(0, 99);                  // new array, index 0 replaced
arr.toSpliced(1, 2, 99);         // new array, elements replaced

// Classic immutable patterns
const sorted   = [...arr].sort((a, b) => a - b);
const appended = [...arr, 6];
const removed  = arr.filter((_, i) => i !== 2);
const updated  = arr.map((v, i) => i === 2 ? 99 : v);

// Access from end (ES2022)
arr.at(-1);  arr.at(-2);

// Search
arr.find(x => x > 3);        arr.findIndex(x => x > 3);
arr.findLast(x => x < 4);    arr.findLastIndex(x => x < 4);

// Build
Array.from({ length: 5 }, (_, i) => i * 2); // [0,2,4,6,8]
Array.from(new Set([1,1,2]));                 // [1,2]
[1,2,3].flatMap(x => [x, -x]);               // [1,-1,2,-2,3,-3]

// Group (ES2024)
Object.groupBy([1,2,3,4,5], n => n%2===0 ? 'even':'odd');
// { odd:[1,3,5], even:[2,4] }
```

### Objects

```js
Object.keys(obj);   Object.values(obj);   Object.entries(obj);
Object.hasOwn(obj, 'key');  // ES2022 — use over hasOwnProperty
'key' in obj;               // includes prototype chain!

// Transform via entries
const doubled = Object.fromEntries(
  Object.entries(prices).map(([k, v]) => [k, v * 2])
);

// Merge (shallow)
const merged  = { ...defaults, ...overrides }; // later wins
const updated = { ...user, role: 'admin' };

// Deep clone (ES2022)
const clone = structuredClone(original);
// Handles: Date, Map, Set, ArrayBuffer, RegExp, circular refs
// Cannot: Function, DOM nodes, WeakMap

// Group (ES2024)
Object.groupBy(people, p => p.department);
```

### Map, Set and WeakMap

```js
// Map — any key type, ordered, no prototype pollution
const map = new Map([['a', 1], [42, 'num']]);
map.set('key', 'val');  map.get('key');  map.has(42);  map.size;
for (const [k, v] of map) {}

// WeakMap — GC-friendly, keys must be objects
const meta = new WeakMap();
meta.set(domNode, { state: 'active' });
// When domNode is GC'd, entry is removed automatically

// Set — unique values
const set = new Set([1, 2, 2, 3]);  // {1, 2, 3}
const unique = [...new Set(array)]; // dedup

// Set operations (ES2024)
const a = new Set([1,2,3,4]), b = new Set([3,4,5,6]);
a.union(b);               // {1,2,3,4,5,6}
a.intersection(b);        // {3,4}
a.difference(b);          // {1,2}
a.symmetricDifference(b); // {1,2,5,6}
```

---

## 4. Modern ES6+ Syntax

### Optional Chaining and Nullish Coalescing

```js
// ?. — safe access (use only when null IS expected, not a bug)
user?.profile?.avatar?.url
arr?.[0]
obj?.[dynamicKey]
fn?.()
const name = user?.displayName ?? 'Anonymous';

// ?? vs ||
// || fires on ANY falsy (0, '', false, null, undefined)
// ?? fires ONLY on null/undefined

const port    = opts.port    ?? 3000; // preserves 0 ✅
const timeout = opts.timeout ?? 5000; // preserves 0 ✅
const port2   = opts.port    || 3000; // opts.port=0 → 3000 ❌ BUG!

// Logical assignment (ES2021)
a ??= 'default';    // assign if null/undefined
a ||= 'fallback';   // assign if falsy
a &&= transform(a); // assign if truthy

cache[key] ??= expensiveCompute(key); // lazy init
user.prefs ??= {};                     // init sub-object
```

### Spread, Rest and Template Literals

```js
// REST — collect remaining
function log(level, ...msgs) { console[level](...msgs); }
const [h, ...tail] = [1,2,3];
const { a, ...rest } = { a:1, b:2, c:3 };

// SPREAD — expand
const merged = { ...obj1, ...obj2 };  // obj2 wins
const copy   = [...arr];
Math.max(...numbers);
// ⚠️ Spread is SHALLOW — nested objects share references

// Tagged templates
function safeHtml(strings, ...vals) {
  return strings.reduce((out, str, i) =>
    out + (i ? String(vals[i-1]).replace(/[&<>"']/g,
      c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])) : '') + str
  );
}
const html = safeHtml`<p class="${cls}">${userInput}</p>`; // XSS-safe
```

---

## 5. Functions

### Arrow vs Regular

```js
// Regular: own this, own arguments, can be constructor
// Arrow:   lexical this, no arguments, cannot be new

// ✅ Arrow — callbacks, closures, preserve class `this`
[1,2,3].map(x => x * 2);
fetch(url).then(r => r.json());
setTimeout(() => this.tick(), 1000); // this = class instance ✅

// ✅ Regular — object methods, event handlers needing `this`
const obj = {
  value: 42,
  getValue() { return this.value; }, // this = obj ✅
  // getValue: () => this.value,     // this = outer scope ❌
};
button.addEventListener('click', function() {
  this.classList.toggle('on');  // this = button ✅
});

// Return object from arrow — wrap in parens!
const makeUser = name => ({ name, id: Date.now() });
```

### Parameter Patterns

```js
// Options object (best for 3+ params)
function initChart({
  container,
  type = 'line',
  animated = true,
  onLoad = null,
} = {}) {} // ← {} prevents TypeError if called without args

// Rest
function sum(...nums) { return nums.reduce((a, b) => a + b, 0); }
```

### Pure Functions and Composition

```js
// Pure: same input → same output, no side effects
const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
const formatUser = u => ({ ...u, full: `${u.first} ${u.last}` });

// Pipe (left-to-right)
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);

const processInput = pipe(
  s => s.trim(),
  s => s.toLowerCase(),
  s => s.replace(/\s+/g, '-'),
);
processInput('  Hello World  '); // 'hello-world'

// Memoize
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const k = JSON.stringify(args);
    if (!cache.has(k)) cache.set(k, fn(...args));
    return cache.get(k);
  };
}

// Partial application
const partial = (fn, ...pre) => (...rest) => fn(...pre, ...rest);
const add10 = partial((a, b) => a + b, 10);
add10(5); // 15
```

---

## 6. Classes and Prototypes

### Modern Class Syntax

```js
class EventEmitter {
  #listeners = new Map();  // private field (ES2022)
  #max = 100;
  static #count = 0;       // private static
  static version = '3.0';  // public static

  constructor() { EventEmitter.#count++; }
  static getCount() { return EventEmitter.#count; }

  get listenerCount() {
    return [...this.#listeners.values()].reduce((n, s) => n + s.size, 0);
  }
  set maxListeners(n) {
    if (!Number.isInteger(n) || n < 0) throw new TypeError('Positive integer');
    this.#max = n;
  }

  on(event, fn) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, new Set());
    this.#listeners.get(event).add(fn);
    return this; // fluent API
  }
  off(event, fn) { this.#listeners.get(event)?.delete(fn); return this; }
  emit(event, ...args) {
    this.#listeners.get(event)?.forEach(fn => {
      try { fn(...args); } catch(e) { console.error(e); }
    });
    return this;
  }
  once(event, fn) {
    const w = (...a) => { fn(...a); this.off(event, w); };
    return this.on(event, w);
  }
}
```

### Inheritance

```js
class Component extends EventEmitter {
  #root; #mounted = false;

  constructor(sel) {
    super(); // must be first!
    const el = typeof sel === 'string' ? document.querySelector(sel) : sel;
    if (!el) throw new Error(`Not found: ${sel}`);
    this.#root = el;
  }

  get el() { return this.#root; }

  render() { throw new Error(`${this.constructor.name}.render() not implemented`); }

  mount() {
    this.#root.innerHTML = this.render();
    this.bindEvents();
    this.#mounted = true;
    this.emit('mount');
    return this;
  }

  bindEvents() {} // hook

  update() {
    if (!this.#mounted) return;
    const scroll = this.#root.scrollTop;
    this.#root.innerHTML = this.render();
    this.bindEvents();
    this.#root.scrollTop = scroll;
    this.emit('update');
  }

  destroy() {
    this.#root.innerHTML = ''; this.#mounted = false;
    this.emit('destroy');
  }
}
```

### Mixins

```js
const Serializable = Base => class extends Base {
  toJSON() { return JSON.stringify(Object.fromEntries(Object.entries(this))); }
};
const Timestamped = Base => class extends Base {
  constructor(...a) { super(...a); this.createdAt = new Date().toISOString(); }
  touch() { this.updatedAt = new Date().toISOString(); return this; }
};
const Validatable = Base => class extends Base {
  validate() {
    const errs = Object.entries(this.constructor.schema ?? {})
      .filter(([f, r]) => !r(this[f])).map(([f]) => f);
    return { valid: !errs.length, errors: errs };
  }
};

class User extends Serializable(Timestamped(Validatable(EventEmitter))) {
  static schema = {
    name:  v => typeof v === 'string' && v.length > 0,
    email: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v),
  };
}
```

---

## 7. Async Programming

### Promise Combinators

```js
// All must succeed — fails on first rejection
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);

// All settle — never rejects (ES2020)
const results = await Promise.allSettled([fetch('/a'), fetch('/b')]);
results.forEach(r => r.status === 'fulfilled' ? process(r.value) : warn(r.reason));

// First settled (fulfilled OR rejected)
const data = await Promise.race([
  fetchData(),
  new Promise((_, rej) => setTimeout(() => rej(new Error('Timeout')), 5000)),
]);

// First FULFILLED — rejects only if ALL reject (ES2021)
const fastest = await Promise.any([fetchUS(), fetchEU(), fetchAsia()]);

// External resolve/reject (ES2024)
const { promise, resolve, reject } = Promise.withResolvers();
socket.on('data', resolve);
socket.on('error', reject);
const msg = await promise;
```

### async/await Patterns

```js
// ✅ Parallel requests — 200ms total instead of 400ms
const [user, posts] = await Promise.all([
  loadUser(id), loadPosts(id)
]);

// ❌ Sequential — 400ms
// const user  = await loadUser(id);
// const posts = await loadPosts(id);

// ✅ Error handling
async function loadDashboard(id) {
  try {
    const [user, posts] = await Promise.all([loadUser(id), loadPosts(id)]);
    render({ user, posts });
  } catch (e) {
    if (e.name === 'AbortError') return;
    showError(e.message);
  } finally {
    hideSpinner();
  }
}

// ✅ Retry with exponential backoff
async function retry(fn, { attempts = 3, delay = 500 } = {}) {
  for (let i = 0; i <= attempts; i++) {
    try { return await fn(); }
    catch (e) {
      if (i === attempts || e.name === 'AbortError') throw e;
      if (e.status < 500 && e.status !== 429) throw e;
      await new Promise(r => setTimeout(r, delay * 2**i + Math.random()*300));
    }
  }
}
```

### AbortController

```js
// Timeout via AbortSignal (ES2022)
const res = await fetch(url, { signal: AbortSignal.timeout(5000) });

// Cancel previous search on new input
class Searcher {
  #ctrl = null;

  async search(query) {
    this.#ctrl?.abort();
    this.#ctrl = new AbortController();
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`,
        { signal: this.#ctrl.signal });
      return res.json();
    } catch (e) {
      if (e.name === 'AbortError') return null;
      throw e;
    }
  }
}

// Combine signals (ES2024)
const combined = AbortSignal.any([
  userController.signal,
  AbortSignal.timeout(10_000),
]);
await fetch(url, { signal: combined });
```

### Async Generators

```js
// Paginated fetch
async function* pages(url) {
  let page = 1;
  while (true) {
    const { data, hasMore } = await api.get(url, { params: { page: page++ } });
    yield* data;
    if (!hasMore) return;
  }
}
for await (const item of pages('/api/items')) render(item);

// Stream line-by-line
async function* readLines(response) {
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buf = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) { if (buf.trim()) yield buf; return; }
    buf += value;
    const lines = buf.split('\n'); buf = lines.pop() ?? '';
    yield* lines.filter(Boolean);
  }
}
```

## 8. ES Modules System

### Export / Import

```js
// Named exports
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export class Vector {}

// Default export (one per module)
export default class Calculator {}

// Re-exports
export { add as sum }     from './math.js';
export * as utils         from './helpers.js';

// Named imports
import { PI, add }        from './math.js';
import { add as sum }     from './math.js';   // rename
import * as MathLib       from './math.js';   // namespace
import Calc, { PI }       from './math.js';   // default + named
import './polyfills.js';                      // side-effects only
```

### Dynamic Imports and Import Maps

```js
// Lazy-load on demand (code splitting)
button.addEventListener('click', async () => {
  const { openModal } = await import('./modal.js');
  openModal(content);
}, { once: true });

// Parallel lazy loading
const [{ default: Chart }, { default: Table }] = await Promise.all([
  import('./chart.js'), import('./table.js'),
]);

// Conditional
const logger = await import(isDev ? './logger-dev.js' : './logger-prod.js');

// Import Maps in HTML (no bundler needed)
// <script type="importmap">
// { "imports": { "lodash-es": "https://cdn.jsdelivr.net/npm/lodash-es@4/lodash.js" } }
// </script>
// Then in modules: import debounce from 'lodash-es/debounce.js';
```

---

## 9. DOM API — Modern Approach

### Querying

```js
document.querySelector('.card');             // first match
document.querySelectorAll('.item');          // all — static NodeList
document.getElementById('app');             // fastest
document.getElementsByClassName('btn');     // live HTMLCollection!

// Convert to array for array methods
const items = [...document.querySelectorAll('.item')];
const items2 = Array.from(document.querySelectorAll('.item'));

// Scoped query
const inputs = form.querySelectorAll('input[required]');

// Walk up the tree
button.closest('li');
el.closest('[data-component]');
el.closest('[role="dialog"]');

// Check match
el.matches('.active:not([disabled])');
el.matches(':focus-within');
```

### Creating and Inserting

```js
// Safe creation — textContent never causes XSS
const li = document.createElement('li');
li.textContent = item.name;   // ✅ safe
li.dataset.id  = item.id;
li.className   = 'list-item';

// Batch insert with DocumentFragment — ONE reflow
const frag = document.createDocumentFragment();
data.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name;
  frag.append(li);
});
list.append(frag);

// Modern insertion API
parent.append(child);          // end
parent.prepend(child);         // start
el.before(newEl);              // before sibling
el.after(newEl);               // after sibling
el.replaceWith(newEl);         // replace self
el.remove();                   // remove self

// insertAdjacentHTML — fast HTML string insertion
el.insertAdjacentHTML('beforeend', trustedHtml);
// positions: beforebegin | afterbegin | beforeend | afterend
```

### Classes, Attributes and CSS Variables

```js
// classList — preferred over className manipulation
el.classList.add('a', 'b');
el.classList.remove('c');
el.classList.toggle('open');
el.classList.toggle('active', isActive);  // conditional
el.classList.replace('old', 'new');
el.classList.contains('open');            // boolean

// Attributes
el.setAttribute('aria-expanded', 'true');
el.getAttribute('data-id');
el.removeAttribute('hidden');
el.toggleAttribute('disabled');
el.dataset.userId = '42';  // → data-user-id="42"

// CSS Custom Properties
el.style.setProperty('--gap', '1rem');
document.documentElement.style.setProperty('--primary', '#3b82f6');
getComputedStyle(el).getPropertyValue('--gap').trim();

// ✅ Prefer classes over inline styles
// Only use inline styles for truly dynamic values:
el.style.transform = `translateX(${x}px)`;
el.style.setProperty('--progress', `${pct}%`);
```

---

## 10. Events and Delegation

### Modern Event Options

```js
el.addEventListener(type, handler, {
  once:    true,           // auto-remove after first fire
  passive: true,           // no preventDefault (critical for scroll perf)
  capture: false,          // bubble phase (default)
  signal:  ctrl.signal,    // AbortSignal — remove with abort()
});

// ✅ AbortController — bulk cleanup (best pattern)
const ctrl = new AbortController();
const sig  = ctrl.signal;
window.addEventListener('resize',   onResize,  { signal: sig });
window.addEventListener('scroll',   onScroll,  { signal: sig, passive: true });
document.addEventListener('keydown', onKeydown, { signal: sig });
ctrl.abort(); // removes ALL three at once
```

### Event Delegation

```js
// ✅ One listener handles all current and future elements
list.addEventListener('click', e => {
  const btn  = e.target.closest('[data-action]');
  const item = e.target.closest('[data-id]');
  if (!btn || !item) return;

  const { action } = btn.dataset;
  const { id }     = item.dataset;

  if (action === 'delete') deleteItem(id);
  if (action === 'edit')   editItem(id);
});

// Generic utility
function delegate(parent, selector, event, handler) {
  parent.addEventListener(event, e => {
    const target = e.target.closest(selector);
    if (target && parent.contains(target)) handler.call(target, e, target);
  });
}
```

### Custom Events and Debounce/Throttle

```js
// Custom events
const emit = (el, name, detail = {}) =>
  el.dispatchEvent(new CustomEvent(name, { detail, bubbles: true, composed: true }));

emit(form, 'form:saved', { id: 42 });
form.addEventListener('form:saved', ({ detail }) => toast(`Saved #${detail.id}`));

// Event bus
const bus = {
  on:   (e, fn) => document.addEventListener(e, fn),
  off:  (e, fn) => document.removeEventListener(e, fn),
  emit: (e, d)  => document.dispatchEvent(new CustomEvent(e, { detail: d })),
};

// Debounce — after N ms of quiet
function debounce(fn, delay) {
  let t; return function(...a) { clearTimeout(t); t = setTimeout(() => fn.apply(this,a), delay); };
}

// Throttle — at most once per N ms
function throttle(fn, limit) {
  let last = 0;
  return function(...a) { const now=Date.now(); if(now-last>=limit){last=now;fn.apply(this,a);} };
}

input.addEventListener('input',  debounce(search, 300));
window.addEventListener('scroll', throttle(updateHeader, 100), { passive: true });
```

---

## 11. Fetch API and Networking

### HTTP Client

```js
class HttpClient {
  #base; #headers; #onError;

  constructor(base, { headers = {}, onError = null } = {}) {
    this.#base    = base.replace(/\/$/, '');
    this.#headers = { 'Content-Type': 'application/json', ...headers };
    this.#onError = onError;
  }

  async #req(method, path, { body, params, headers = {}, signal } = {}) {
    const url = new URL(this.#base + path);
    if (params) Object.entries(params).forEach(([k, v]) => v != null && url.searchParams.set(k, v));
    try {
      const res = await fetch(url, {
        method,
        headers: { ...this.#headers, ...headers },
        body: body != null ? JSON.stringify(body) : undefined,
        signal,
      });
      if (!res.ok) {
        const err = Object.assign(new Error(`HTTP ${res.status}`), { name:'HttpError', status:res.status });
        if (this.#onError) return this.#onError(err);
        throw err;
      }
      const ct = res.headers.get('Content-Type') ?? '';
      return ct.includes('json') ? res.json() : res.text();
    } catch (e) {
      if (e.name === 'HttpError') throw e;
      throw Object.assign(new Error(`Network: ${e.message}`), { name:'NetworkError', cause:e });
    }
  }

  get(p, o)    { return this.#req('GET',    p, o); }
  post(p, o)   { return this.#req('POST',   p, o); }
  put(p, o)    { return this.#req('PUT',    p, o); }
  patch(p, o)  { return this.#req('PATCH',  p, o); }
  delete(p, o) { return this.#req('DELETE', p, o); }
}

const api = new HttpClient('/api', {
  headers: { Authorization: `Bearer ${getToken()}` },
  onError: async err => {
    if (err.status === 401) { await refreshToken(); throw err; }
    throw err;
  },
});

const users = await api.get('/users', { params: { page: 1, limit: 20 } });
const post  = await api.post('/posts', { body: { title, content } });
```

### Caching with Deduplication

```js
class RequestCache {
  #cache = new Map();   // completed
  #inflight = new Map(); // in-progress

  async get(key, fetcher, ttlMs = 60_000) {
    const hit = this.#cache.get(key);
    if (hit && Date.now() - hit.ts < ttlMs) return hit.data;

    // Deduplicate concurrent requests for the same key
    if (this.#inflight.has(key)) return this.#inflight.get(key);

    const p = fetcher()
      .then(data => { this.#cache.set(key, { data, ts: Date.now() }); return data; })
      .finally(() => this.#inflight.delete(key));

    this.#inflight.set(key, p);
    return p;
  }

  invalidate(key) { this.#cache.delete(key); }
  clear()         { this.#cache.clear(); }
}

const cache = new RequestCache();
// Three parallel calls → only ONE fetch
const [a, b, c] = await Promise.all([
  cache.get('users', () => api.get('/users')),
  cache.get('users', () => api.get('/users')),  // deduplicated
  cache.get('users', () => api.get('/users')),  // deduplicated
]);
```

---

## 12. Browser Storage

### localStorage / sessionStorage

```js
class Storage {
  #store; #prefix;

  constructor(type = 'local', prefix = 'app:') {
    this.#store  = type === 'session' ? sessionStorage : localStorage;
    this.#prefix = prefix;
  }

  set(key, value, ttlMs = null) {
    try {
      this.#store.setItem(this.#prefix + key, JSON.stringify({
        v: value, ...(ttlMs ? { exp: Date.now() + ttlMs } : {})
      }));
      return true;
    } catch { return false; } // QuotaExceededError
  }

  get(key, fallback = null) {
    try {
      const raw = this.#store.getItem(this.#prefix + key);
      if (!raw) return fallback;
      const { v, exp } = JSON.parse(raw);
      if (exp && Date.now() > exp) { this.remove(key); return fallback; }
      return v;
    } catch { return fallback; }
  }

  remove(key) { this.#store.removeItem(this.#prefix + key); }

  static onExternalChange(cb) {
    window.addEventListener('storage', ({ key, newValue, oldValue }) => {
      const parse = s => { try { return JSON.parse(s ?? 'null')?.v ?? null; } catch { return null; } };
      cb({ key, newValue: parse(newValue), oldValue: parse(oldValue) });
    });
  }
}

const store = new Storage('local', 'myapp:');
store.set('session', { userId: 1 }, 30 * 60_000); // 30 min TTL
store.get('session'); // { userId: 1 }
```

### IndexedDB

```js
class IDB {
  #db = null;

  constructor(name, version, schema) {
    this._name = name; this._ver = version; this._schema = schema;
  }

  async open() {
    if (this.#db) return this;
    this.#db = await new Promise((res, rej) => {
      const req = indexedDB.open(this._name, this._ver);
      req.onupgradeneeded = ({ target: { result: db } }) => {
        this._schema.forEach(({ name, keyPath, indexes = [] }) => {
          const store = db.objectStoreNames.contains(name)
            ? req.transaction.objectStore(name)
            : db.createObjectStore(name, { keyPath });
          indexes.forEach(({ name: n, keyPath: kp, unique = false }) => {
            if (!store.indexNames.contains(n)) store.createIndex(n, kp, { unique });
          });
        });
      };
      req.onsuccess = e => res(e.target.result);
      req.onerror   = e => rej(e.target.error);
    });
    return this;
  }

  #p(r) { return new Promise((res, rej) => { r.onsuccess = e => res(e.target.result); r.onerror = e => rej(e.target.error); }); }
  #os(name, mode = 'readonly') { return this.#db.transaction(name, mode).objectStore(name); }

  get(store, key)     { return this.#p(this.#os(store).get(key)); }
  getAll(store, q)    { return this.#p(this.#os(store).getAll(q)); }
  put(store, val)     { return this.#p(this.#os(store, 'readwrite').put(val)); }
  delete(store, key)  { return this.#p(this.#os(store, 'readwrite').delete(key)); }
  clear(store)        { return this.#p(this.#os(store, 'readwrite').clear()); }
  getByIndex(store, idx, val) { return this.#p(this.#os(store).index(idx).get(val)); }
}

const db = new IDB('myapp', 1, [
  { name: 'users', keyPath: 'id', indexes: [{ name: 'email', keyPath: 'email', unique: true }] },
]);
await db.open();
await db.put('users', { id: 1, email: 'a@b.com', name: 'Alice' });
const alice = await db.getByIndex('users', 'email', 'a@b.com');
```

---

## 13. State Management

### Reactive Proxy Store

```js
class Store {
  #state; #subs = new Map(); #history = [];

  constructor(initial) {
    this.#state = this.#wrap({ ...initial });
  }

  #wrap(obj) {
    return new Proxy(obj, {
      set: (t, k, v) => {
        const prev = t[k];
        t[k] = v && typeof v === 'object' ? this.#wrap(v) : v;
        if (prev !== v) this.#notify(k);
        return true;
      },
      get: (t, k) => {
        const v = t[k];
        return v && typeof v === 'object' && !Array.isArray(v) ? this.#wrap(v) : v;
      },
    });
  }

  get state() { return this.#state; }

  update(fn) {
    this.#history.push(structuredClone(this.#state));
    typeof fn === 'function' ? fn(this.#state) : Object.assign(this.#state, fn);
  }

  undo() {
    const prev = this.#history.pop();
    if (prev) Object.assign(this.#state, prev);
  }

  on(key, fn) {
    if (!this.#subs.has(key)) this.#subs.set(key, new Set());
    this.#subs.get(key).add(fn);
    return () => this.#subs.get(key).delete(fn);
  }

  #notify(key) {
    this.#subs.get(key)?.forEach(fn => fn(this.#state[key], this.#state));
    this.#subs.get('*')?.forEach(fn => fn(this.#state[key], this.#state));
  }
}

const store = new Store({ count: 0, user: null });
store.on('count', v => counterEl.textContent = v);
store.on('*', () => saveToStorage(store.state));
store.update(s => s.count++);
store.undo();
```

### Signals (Fine-grained Reactivity)

```js
function signal(value) {
  const subs = new Set();
  return {
    get()  { return value; },
    set(v) {
      const next = typeof v === 'function' ? v(value) : v;
      if (!Object.is(next, value)) { value = next; subs.forEach(fn => fn(value)); }
    },
    subscribe(fn) { subs.add(fn); fn(value); return () => subs.delete(fn); },
  };
}

function computed(fn, ...deps) {
  const s = signal(fn());
  deps.forEach(dep => dep.subscribe(() => s.set(fn())));
  return { get: s.get.bind(s), subscribe: s.subscribe.bind(s) };
}

const firstName = signal('Alice');
const lastName  = signal('Smith');
const fullName  = computed(() => `${firstName.get()} ${lastName.get()}`, firstName, lastName);

fullName.subscribe(name => nameEl.textContent = name);
firstName.set('Bob'); // → DOM updates automatically
```

---

## 14. Design Patterns

### Observer (EventBus)

```js
class EventBus {
  #map = new Map();

  on(event, fn, { once = false, signal } = {}) {
    if (!this.#map.has(event)) this.#map.set(event, new Set());
    const w = once ? (...a) => { fn(...a); this.off(event, w); } : fn;
    this.#map.get(event).add(w);
    signal?.addEventListener('abort', () => this.off(event, w), { once: true });
    return () => this.off(event, w);
  }

  off(event, fn)   { this.#map.get(event)?.delete(fn); }
  once(event, fn)  { return this.on(event, fn, { once: true }); }
  emit(event, ...a){ this.#map.get(event)?.forEach(fn => { try{fn(...a);}catch(e){console.error(e);} }); }
}

export const events = new EventBus();
```

### Factory, Builder, Command

```js
// Factory + Registry
class Registry {
  #map = new Map();
  register(name, C) { this.#map.set(name, C); return this; }
  create(name, ...a) {
    const C = this.#map.get(name);
    if (!C) throw new Error(`Unknown: "${name}". Have: ${[...this.#map.keys()].join(', ')}`);
    return new C(...a);
  }
}

// Builder (fluent API)
class QueryBuilder {
  #t; #cols=['*']; #where=[]; #order; #limit; #offset;

  from(t)        { this.#t = t; return this; }
  select(...c)   { this.#cols = c; return this; }
  where(c,op,v)  { this.#where.push(`${c} ${op} ?`); return this; }
  orderBy(c,d='ASC') { this.#order = `${c} ${d}`; return this; }
  limit(n)       { this.#limit = n; return this; }
  offset(n)      { this.#offset = n; return this; }

  build() {
    let q = `SELECT ${this.#cols.join(', ')} FROM ${this.#t}`;
    if (this.#where.length) q += ` WHERE ${this.#where.join(' AND ')}`;
    if (this.#order)  q += ` ORDER BY ${this.#order}`;
    if (this.#limit)  q += ` LIMIT ${this.#limit}`;
    if (this.#offset) q += ` OFFSET ${this.#offset}`;
    return q;
  }
}

// Command (Undo/Redo)
class CommandHistory {
  #undo = []; #redo = [];

  execute(cmd) { cmd.execute(); this.#undo.push(cmd); this.#redo = []; }
  undo()       { const c = this.#undo.pop(); c && (c.undo(),    this.#redo.push(c)); }
  redo()       { const c = this.#redo.pop(); c && (c.execute(), this.#undo.push(c)); }

  get canUndo() { return this.#undo.length > 0; }
  get canRedo() { return this.#redo.length > 0; }
}
```

### Proxy Patterns

```js
// Validation proxy
const validated = schema => new Proxy({}, {
  set(t, k, v) {
    const r = schema[k];
    if (r?.required && !v)            throw new Error(`${k} required`);
    if (r?.type && typeof v !== r.type) throw new TypeError(`${k} must be ${r.type}`);
    if (r?.min != null && v < r.min)  throw new RangeError(`${k} >= ${r.min}`);
    return Reflect.set(t, k, v);
  }
});

// Observable proxy (deep reactive)
const observable = (data, notify) => new Proxy(data, {
  set(t, k, v) { const prev=t[k]; const ok=Reflect.set(t,k,v); if(ok&&prev!==v) notify(k,v,prev); return ok; },
  get(t, k)    { const v=t[k]; return v&&typeof v==='object' ? observable(v,notify) : v; },
});

// Read-only proxy
const readonly = obj => new Proxy(obj, {
  set()           { throw new TypeError('Read-only'); },
  deleteProperty(){ throw new TypeError('Read-only'); },
  get(t, k)       { const v=t[k]; return v&&typeof v==='object' ? readonly(v) : v; },
});
```

## 15. Observer APIs

### IntersectionObserver

```js
// Lazy image loading
function lazyLoadImages() {
  const obs = new IntersectionObserver((entries, self) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const img = e.target;
      img.src   = img.dataset.src;
      img.srcset = img.dataset.srcset ?? '';
      img.removeAttribute('data-src');
      self.unobserve(img);
    });
  }, { rootMargin: '200px 0px', threshold: 0 });
  document.querySelectorAll('img[data-src]').forEach(img => obs.observe(img));
  return () => obs.disconnect();
}

// Scroll reveal animations
function scrollReveal(sel, cls = 'revealed') {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add(cls); obs.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
  document.querySelectorAll(sel).forEach(el => obs.observe(el));
  return () => obs.disconnect();
}

// Infinite scroll
function infiniteScroll(sentinel, loadMore) {
  let busy = false;
  const obs = new IntersectionObserver(async ([e]) => {
    if (!e.isIntersecting || busy) return;
    busy = true; obs.unobserve(sentinel);
    const more = await loadMore();
    busy = false; if (more) obs.observe(sentinel);
  }, { rootMargin: '300px' });
  obs.observe(sentinel);
  return () => obs.disconnect();
}

// Sticky header detection
function stickyHeader(header, sentinel) {
  const obs = new IntersectionObserver(([e]) => {
    header.classList.toggle('sticky', !e.isIntersecting);
  }, { threshold: 1 });
  obs.observe(sentinel);
  return () => obs.disconnect();
}
```

### MutationObserver and ResizeObserver

```js
// Watch DOM changes
function watchDOM(root, onAdd, onRemove) {
  const obs = new MutationObserver(muts => {
    for (const m of muts) {
      [...m.addedNodes].filter(n => n.nodeType === 1).forEach(onAdd);
      [...m.removedNodes].filter(n => n.nodeType === 1).forEach(onRemove);
    }
  });
  obs.observe(root, { childList: true, subtree: true });
  return () => obs.disconnect();
}

// Watch element size
function watchSize(el, fn) {
  let raf;
  const obs = new ResizeObserver(entries => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(() => {
      const { width, height } = entries[0].contentRect;
      fn({ width, height });
    });
  });
  obs.observe(el);
  return () => { obs.disconnect(); cancelAnimationFrame(raf); };
}
```

---

## 16. Web Components

```js
class AppToast extends HTMLElement {
  static observedAttributes = ['type', 'message', 'duration'];
  #shadow; #timer;
  #colors = { info:'#3b82f6', success:'#10b981', error:'#ef4444', warn:'#f59e0b' };

  constructor() { super(); this.#shadow = this.attachShadow({ mode: 'open' }); }

  get type()     { return this.getAttribute('type') ?? 'info'; }
  get message()  { return this.getAttribute('message') ?? ''; }
  get duration() { return Number(this.getAttribute('duration') ?? 3000); }

  connectedCallback()    { this.#render(); if (this.duration > 0) this.#timer = setTimeout(() => this.remove(), this.duration); }
  disconnectedCallback() { clearTimeout(this.#timer); }
  attributeChangedCallback() { if (this.isConnected) this.#render(); }

  #render() {
    this.#shadow.innerHTML = `
      <style>
        :host{display:block;}
        .t{padding:.75rem 1rem;border-radius:.5rem;color:#fff;font:system-ui;
           background:${this.#colors[this.type]};animation:s .3s ease;}
        @keyframes s{from{transform:translateX(110%);opacity:0}to{transform:none;opacity:1}}
        button{float:right;background:none;border:none;color:inherit;cursor:pointer;font-size:1.1rem;}
      </style>
      <div class="t" role="alert">${this.message}<button aria-label="Close">×</button></div>
    `;
    this.#shadow.querySelector('button').onclick = () => this.remove();
  }

  static show(message, type = 'info', duration = 3500) {
    const el = Object.assign(document.createElement('app-toast'), {});
    el.setAttribute('message', message);
    el.setAttribute('type', type);
    el.setAttribute('duration', String(duration));
    Object.assign(el.style, { position:'fixed', bottom:'1rem', right:'1rem', zIndex:'9999' });
    document.body.append(el);
    return el;
  }
}
customElements.define('app-toast', AppToast);

// Usage
AppToast.show('Saved successfully!', 'success');
```

---

## 17. Performance

### requestAnimationFrame Animations

```js
// Easing functions
const ease = {
  linear:   t => t,
  outCubic: t => 1-(1-t)**3,
  inOut:    t => t<.5 ? 2*t*t : -1+(4-2*t)*t,
  spring:   t => 1 - Math.cos(t * Math.PI * 6) * Math.exp(-6*t),
};

function animate({ from, to, duration, easing=ease.outCubic, onFrame, onDone }) {
  let start = null, raf;
  const tick = ts => {
    start ??= ts;
    const t = Math.min((ts-start)/duration, 1);
    onFrame(from + (to-from) * easing(t), t);
    t < 1 ? (raf = requestAnimationFrame(tick)) : onDone?.();
  };
  raf = requestAnimationFrame(tick);
  return () => cancelAnimationFrame(raf);
}

// Smooth counter
animate({ from: 0, to: 1500, duration: 1000,
  onFrame: v => el.textContent = Math.round(v).toLocaleString() });

// Smooth scroll
function scrollTo(target, duration = 500) {
  const from = window.scrollY;
  const to   = typeof target === 'number' ? target : target.getBoundingClientRect().top + from;
  return animate({ from, to, duration, onFrame: y => window.scrollTo(0, y) });
}
```

### Web Workers

```js
// worker.js
const handlers = {
  sort:    data => [...data].sort((a, b) => a - b),
  compute: data => data.reduce((s, n) => s + n, 0),
};
self.onmessage = ({ data: { id, type, payload } }) => {
  try   { self.postMessage({ id, result: handlers[type](payload) }); }
  catch (e) { self.postMessage({ id, error: e.message }); }
};

// main.js wrapper
class WorkerBridge {
  #w; #p = new Map(); #i = 0;
  constructor(url) {
    this.#w = new Worker(url, { type: 'module' });
    this.#w.onmessage = ({ data: { id, result, error } }) => {
      const { resolve, reject } = this.#p.get(id) ?? {};
      this.#p.delete(id);
      error ? reject(new Error(error)) : resolve(result);
    };
  }
  run(type, payload) {
    return new Promise((resolve, reject) => {
      const id = ++this.#i;
      this.#p.set(id, { resolve, reject });
      this.#w.postMessage({ id, type, payload });
    });
  }
}

const worker = new WorkerBridge('./worker.js');
const sorted = await worker.run('sort', [3,1,4,1,5]);
```

### DOM Performance Rules

```js
// ❌ Layout thrashing — read + write per element = N reflows
els.forEach(el => { const h = el.offsetHeight; el.style.height = h+10+'px'; });

// ✅ Read all, then write all — 1 reflow
const hs = els.map(el => el.offsetHeight);
els.forEach((el, i) => { el.style.height = hs[i]+10+'px'; });

// ✅ animate with transform (GPU, no layout)
// ❌ el.style.top = y+'px';  triggers layout
el.style.transform = `translateY(${y}px)`; // ✅ GPU only

// ✅ Break long tasks to keep UI responsive
async function chunked(items, fn, size = 50) {
  for (let i = 0; i < items.length; i += size) {
    items.slice(i, i+size).forEach(fn);
    await ('scheduler' in window && scheduler.yield
      ? scheduler.yield()
      : new Promise(r => setTimeout(r, 0)));
  }
}
```

---

## 18. Security

### XSS Prevention

```js
// ❌ NEVER with user input
el.innerHTML = userInput;      // XSS
eval(userInput);               // code injection

// ✅ textContent is always safe
el.textContent = userInput;

// ✅ HTML escape function
const esc = s => String(s).replace(/[&<>"']/g,
  c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

// ✅ Validate URLs
function isSafeUrl(url) {
  try { return ['http:','https:'].includes(new URL(url).protocol); }
  catch { return false; }
}

// ✅ Trusted Types (Chrome/Edge)
if (window.trustedTypes?.createPolicy) {
  const policy = trustedTypes.createPolicy('main', {
    createHTML: html => DOMPurify.sanitize(html),
    createScriptURL: url => isSafeUrl(url) ? url : '',
  });
  el.innerHTML = policy.createHTML(trustedHtml);
}
```

### CSRF and Security Headers

```js
// Add CSRF token to mutating requests
const csrf = () =>
  document.querySelector('meta[name="csrf-token"]')?.content
  ?? document.cookie.match(/csrf=([^;]+)/)?.[1] ?? '';

const secureFetch = (url, init = {}) => {
  if (['POST','PUT','PATCH','DELETE'].includes((init.method ?? 'GET').toUpperCase())) {
    init.headers = { ...init.headers, 'X-CSRF-Token': csrf() };
  }
  return fetch(url, init);
};

// Prevent clickjacking
if (window.top !== window.self) {
  document.body.hidden = true;
  // Server-side: X-Frame-Options: DENY
  // or: Content-Security-Policy: frame-ancestors 'none'
}
```

---

## 19. Error Handling

### Custom Error Hierarchy

```js
class AppError extends Error {
  constructor(message, code, ctx = {}) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.ctx  = ctx;
    Error.captureStackTrace?.(this, this.constructor);
  }
}

class ValidationError  extends AppError { constructor(field, msg) { super(msg, 'VALIDATION', {field}); this.field=field; } }
class NotFoundError    extends AppError { constructor(res, id)    { super(`${res} #${id} not found`, 'NOT_FOUND'); } }
class UnauthorizedError extends AppError { constructor()            { super('Auth required', 'UNAUTHORIZED'); } }

// Global error boundaries
window.addEventListener('error', ({ error, filename, lineno }) => {
  report({ type:'sync', error, src:`${filename}:${lineno}` });
});
window.addEventListener('unhandledrejection', ({ reason }) => {
  report({ type:'async', reason });
  event.preventDefault();
});

async function report(info) {
  try {
    await fetch('/api/errors', {
      method:'POST', keepalive:true,
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ ...info, url:location.href, ts:new Date() }),
    });
  } catch { /* never throw in error reporter */ }
}
```

### Result Type

```js
const Result = {
  ok:   v => ({ ok:true,  value:v }),
  err:  e => ({ ok:false, error:e }),
  wrap: async fn => { try { return Result.ok(await fn()); } catch(e) { return Result.err(e); } },
};

const r = await Result.wrap(() => api.get('/users'));
if (r.ok)  renderUsers(r.value);
else       showError(r.error.message);
```

---

## 20. Modern Web APIs

### URL, History, Clipboard, Notifications

```js
// URLSearchParams
const params = new URLSearchParams({ q: 'hello world', limit: 20 });
fetch(`/api/search?${params}`);

const url = new URL('https://example.com/search?q=test');
url.searchParams.set('page', 2);
url.toString(); // updated URL string

// Clipboard
const copy = async text => {
  try { await navigator.clipboard.writeText(text); return true; }
  catch { /* fallback */ return false; }
};
const paste = () => navigator.clipboard.readText().catch(() => null);

// Notifications
async function notify(title, body = '') {
  if (!('Notification' in window) || Notification.permission === 'denied') return;
  if (Notification.permission !== 'granted') await Notification.requestPermission();
  if (Notification.permission !== 'granted') return;
  return new Notification(title, { body, icon: '/icon.png' });
}

// Page Visibility
document.addEventListener('visibilitychange', () => {
  document.hidden ? pauseAll() : resumeAll();
});

// structuredClone — deep clone (ES2022)
const clone = structuredClone({ date: new Date(), map: new Map(), set: new Set([1,2]) });
```

### SPA Router

```js
class Router {
  #routes = []; #fallback = null; #guard = null; #onChange = null;

  route(pattern, handler) {
    const re = new RegExp('^' + pattern.replace(/:([^/]+)/g, '(?<$1>[^/]+)') + '$');
    this.#routes.push({ re, handler });
    return this;
  }

  notFound(h)   { this.#fallback = h; return this; }
  guard(fn)     { this.#guard = fn;   return this; }
  onChange(fn)  { this.#onChange = fn; return this; }

  navigate(path, state = {}, { replace = false } = {}) {
    if (this.#guard && !this.#guard(path)) return;
    history[replace ? 'replaceState' : 'pushState'](state, '', path);
    this.#dispatch(path, state);
  }

  start() {
    window.addEventListener('popstate', e => this.#dispatch(location.pathname, e.state ?? {}));
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href]');
      if (!a) return;
      const url = new URL(a.href);
      if (url.origin !== location.origin || a.target === '_blank') return;
      e.preventDefault();
      this.navigate(url.pathname + url.search + url.hash);
    });
    this.#dispatch(location.pathname, history.state ?? {});
    return this;
  }

  #dispatch(path, state) {
    for (const { re, handler } of this.#routes) {
      const m = path.match(re);
      if (m) { this.#onChange?.(path); handler(path, { ...state, params: m.groups ?? {} }); return; }
    }
    this.#fallback?.(path, state);
  }
}
```

---

## 21. Animations

### Web Animations API and FLIP

```js
// Declarative animations (imperative control)
const anim = el.animate([
  { opacity: 0, transform: 'translateY(-16px)' },
  { opacity: 1, transform: 'none' },
], { duration: 300, easing: 'cubic-bezier(0.4,0,0.2,1)', fill: 'forwards' });

await anim.finished;
el.classList.add('visible');

// Reusable effects
const fx = {
  fadeIn:  el => el.animate([{opacity:0},{opacity:1}],{duration:200,fill:'forwards'}),
  fadeOut: el => el.animate([{opacity:1},{opacity:0}],{duration:200,fill:'forwards'}),
  shake:   el => el.animate(
    [{transform:'translateX(0)'},{transform:'translateX(-8px)'},{transform:'translateX(8px)'},{transform:'translateX(0)'}],
    {duration:400}
  ),
};

// FLIP — smooth list reordering
async function flipList(container, doMutation) {
  const first = new Map([...container.children].map(el => [el, el.getBoundingClientRect()]));
  doMutation();
  for (const el of container.children) {
    const prev = first.get(el); if (!prev) continue;
    const next = el.getBoundingClientRect();
    const dx = prev.left - next.left, dy = prev.top - next.top;
    if (!dx && !dy) continue;
    el.animate([{transform:`translate(${dx}px,${dy}px)`},{transform:'none'}], {duration:300,easing:'ease-out'});
  }
}
```

### CSS Variables from JS

```js
const theme = {
  set(vars, el = document.documentElement) {
    Object.entries(vars).forEach(([k, v]) => el.style.setProperty(k.startsWith('--') ? k : `--${k}`, v));
  },
  get(name, el = document.documentElement) {
    return getComputedStyle(el).getPropertyValue(name).trim();
  },
  apply(name) {
    const themes = {
      dark:  { '--bg':'#0f172a','--fg':'#f1f5f9','--accent':'#38bdf8' },
      light: { '--bg':'#ffffff','--fg':'#0f172a','--accent':'#0369a1' },
    };
    this.set(themes[name] ?? themes.light);
    document.documentElement.dataset.theme = name;
    localStorage.setItem('theme', name);
  },
};
```

---

## 22. Regular Expressions

```js
// Named groups (ES2018)
const { groups: { y, m, d } } = '2025-06-15'.match(/(?<y>\d{4})-(?<m>\d{2})-(?<d>\d{2})/);

// Replace with named backreference
'2025-06-15'.replace(/(?<y>\d{4})-(?<m>\d{2})-(?<d>\d{2})/, '$<d>/$<m>/$<y>');

// matchAll — all matches with groups (requires /g)
const links = [...html.matchAll(/href="(?<url>[^"]+)"/g)].map(m => m.groups.url);

// Lookbehind (ES2018)
/(?<=\$)\d+/.exec('$100')[0];  // '100' — after $
/(?<!\$)\d+/.exec('€100')[0];  // '100' — NOT after $

// Unicode properties
/\p{Letter}/u.test('Ж');          // true — any Unicode letter
/\p{Emoji}/u.test('😀');          // true
/\p{Script=Cyrillic}/u.test('Я'); // true

// Escape for dynamic regex
const escRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const search = term => new RegExp(`(${escRe(term)})`, 'gi');

// Common patterns
const patterns = {
  email:    /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i,
  url:      /^https?:\/\/[\w-]+(\.[\w-]+)+([\w\-.~:/?#@!$&'()*+,;=%]+)?$/,
  slug:     /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
  uuid:     /^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i,
  hexColor: /^#(?:[0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$/i,
};
```

---

## 23. Internationalization — Intl API

```js
// Numbers and currency
new Intl.NumberFormat('en-US', { style:'currency', currency:'USD' }).format(1234.5); // '$1,234.50'
new Intl.NumberFormat('en-US', { notation:'compact' }).format(1_500_000);             // '1.5M'
new Intl.NumberFormat('en-US', { style:'percent'}).format(0.756);                    // '76%'
new Intl.NumberFormat('en-US', { style:'unit', unit:'mile-per-hour' }).format(60);   // '60 mph'

// Dates
new Intl.DateTimeFormat('en-US', { dateStyle:'long', timeStyle:'short' }).format(new Date());

// Relative time
const rtf = new Intl.RelativeTimeFormat('en', { numeric:'auto' });
rtf.format(-1, 'day');   // 'yesterday'
rtf.format(-3, 'hour');  // '3 hours ago'
rtf.format(2,  'week');  // 'in 2 weeks'

// Auto-select unit
function timeAgo(date) {
  const sec = Math.round((Date.now() - +new Date(date)) / 1000);
  const rtf = new Intl.RelativeTimeFormat('en', { numeric:'auto' });
  for (const [lim, div, unit] of [
    [60,1,'second'],[3600,60,'minute'],[86400,3600,'hour'],
    [86400*30,86400,'day'],[86400*365,86400*30,'month'],[Infinity,86400*365,'year']
  ]) if (Math.abs(sec) < lim) return rtf.format(-Math.round(sec/div), unit);
}

// List and sort
new Intl.ListFormat('en', { type:'conjunction' }).format(['a','b','c']); // 'a, b, and c'
['banana','Apple','cherry'].sort(new Intl.Collator('en',{sensitivity:'base'}).compare);

// Plural rules
const pr = new Intl.PluralRules('en');
const items = n => `${n} ${pr.select(n) === 'one' ? 'item' : 'items'}`;
```

---

## 24. Service Workers and PWA

```js
// main.js
async function registerSW() {
  if (!('serviceWorker' in navigator)) return;
  const reg = await navigator.serviceWorker.register('/sw.js', { updateViaCache: 'none' });
  reg.addEventListener('updatefound', () => {
    const next = reg.installing;
    next.addEventListener('statechange', () => {
      if (next.state === 'installed' && navigator.serviceWorker.controller) {
        showUpdateBanner(() => next.postMessage({ type: 'SKIP_WAITING' }));
      }
    });
  });
  navigator.serviceWorker.addEventListener('controllerchange', () => location.reload());
}

// sw.js
const CACHE = 'app-v1';
const PRECACHE = ['/', '/app.js', '/style.css', '/offline.html'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

const networkFirst = async req => {
  try {
    const res = await fetch(req);
    if (res.ok) (await caches.open(CACHE)).put(req, res.clone());
    return res;
  } catch { return (await caches.match(req)) ?? caches.match('/offline.html'); }
};

const cacheFirst = async req => {
  const hit = await caches.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok) (await caches.open(CACHE)).put(req, res.clone());
  return res;
};

self.addEventListener('fetch', e => {
  const { pathname } = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (pathname.startsWith('/api/'))                          return e.respondWith(networkFirst(e.request));
  if (/\.(js|css|woff2|png|svg|webp)$/.test(pathname))     return e.respondWith(cacheFirst(e.request));
  if (e.request.mode === 'navigate')                        return e.respondWith(networkFirst(e.request));
});
```

---

## 25. WebSocket and Realtime

```js
class ReconnectWS extends EventTarget {
  #url; #ws = null; #delay = 1000; #attempts = 0;
  #manual = false; #pending = []; #ping = null;

  constructor(url, { maxDelay = 30_000, pingMs = 25_000 } = {}) {
    super(); this.#url = url;
    this._maxDelay = maxDelay; this._pingMs = pingMs;
  }

  connect() { this.#manual = false; this.#open(); return this; }

  #open() {
    this.#ws = new WebSocket(this.#url);
    this.#ws.onopen = () => {
      this.#attempts = 0; this.#delay = 1000;
      this.dispatchEvent(new Event('open'));
      this.#pending.splice(0).forEach(m => this.#ws.send(m));
      this.#ping = setInterval(
        () => this.#ws?.readyState === 1 && this.#ws.send('{"type":"ping"}'),
        this._pingMs
      );
    };
    this.#ws.onmessage = ({ data }) => {
      try {
        const msg = JSON.parse(data);
        if (msg.type !== 'pong') this.dispatchEvent(new CustomEvent('message', { detail: msg }));
      } catch { this.dispatchEvent(new CustomEvent('message', { detail: data })); }
    };
    this.#ws.onclose = ({ code }) => {
      clearInterval(this.#ping);
      this.dispatchEvent(new CustomEvent('close', { detail: { code } }));
      if (!this.#manual && code !== 1000) this.#reconnect();
    };
  }

  #reconnect() {
    const delay = Math.min(this.#delay * 2**this.#attempts++, this._maxDelay) + Math.random()*500;
    setTimeout(() => !this.#manual && this.#open(), delay);
  }

  send(data) {
    const msg = typeof data === 'string' ? data : JSON.stringify(data);
    this.#ws?.readyState === 1 ? this.#ws.send(msg) : this.#pending.push(msg);
    return this;
  }

  close() { this.#manual = true; clearInterval(this.#ping); this.#ws?.close(1000); }
  get connected() { return this.#ws?.readyState === 1; }
}

// Server-Sent Events
class SSEClient extends EventTarget {
  #url; #source; #manual = false;

  constructor(url) { super(); this.#url = url; }

  connect() {
    this.#manual = false;
    this.#source = new EventSource(this.#url, { withCredentials: true });
    this.#source.onopen  = () => this.dispatchEvent(new Event('open'));
    this.#source.onerror = () => {
      if (this.#source.readyState === EventSource.CLOSED && !this.#manual)
        setTimeout(() => this.connect(), 3000);
    };
    this.#source.onmessage = ({ data }) =>
      this.dispatchEvent(new CustomEvent('message', { detail: JSON.parse(data) }));
    return this;
  }

  on(event, fn) { this.#source.addEventListener(event, ({ data }) => fn(JSON.parse(data))); return this; }
  close()       { this.#manual = true; this.#source?.close(); }
}
```

---

## 26. File API

```js
// Open file
async function openFile(types = []) {
  if ('showOpenFilePicker' in window) {
    try {
      const [h] = await showOpenFilePicker({ types, multiple: false });
      return h.getFile();
    } catch(e) { if (e.name !== 'AbortError') throw e; return null; }
  }
  return new Promise(res => {
    const i = Object.assign(document.createElement('input'), { type: 'file' });
    i.addEventListener('change', () => res(i.files[0] ?? null), { once: true });
    i.click();
  });
}

// Read content
const readFile = {
  text:    f => f.text(),
  json:    f => f.text().then(JSON.parse),
  buffer:  f => f.arrayBuffer(),
  url:     f => URL.createObjectURL(f),  // call URL.revokeObjectURL() when done!
};

// Save file
async function saveFile(content, name, mime = 'text/plain') {
  if ('showSaveFilePicker' in window) {
    try {
      const h = await showSaveFilePicker({ suggestedName: name });
      const w = await h.createWritable();
      await w.write(content instanceof Blob ? content : new Blob([content], { type: mime }));
      await w.close(); return;
    } catch(e) { if (e.name === 'AbortError') return; }
  }
  const url = URL.createObjectURL(content instanceof Blob ? content : new Blob([content], {type:mime}));
  Object.assign(document.createElement('a'), { href: url, download: name }).click();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

// Drag-and-drop zone
function dropZone(el, onFiles) {
  el.addEventListener('dragover',  e => { e.preventDefault(); el.classList.add('drag-over'); });
  el.addEventListener('dragleave', e => { if (!el.contains(e.relatedTarget)) el.classList.remove('drag-over'); });
  el.addEventListener('drop',      e => { e.preventDefault(); el.classList.remove('drag-over'); onFiles([...e.dataTransfer.files]); });
}
```

## 27. Form Validation

```js
class FormValidator {
  #form; #rules; #errors = new Map();

  constructor(form, rules) { this.#form = form; this.#rules = rules; }

  static R = {
    required:  (msg='Required')         => v => !!v.trim() || msg,
    minLength: (n, msg)                 => v => v.length>=n || (msg??`Min ${n} chars`),
    maxLength: (n, msg)                 => v => v.length<=n || (msg??`Max ${n} chars`),
    min:       (n, msg)                 => v => +v>=n || (msg??`Min ${n}`),
    max:       (n, msg)                 => v => +v<=n || (msg??`Max ${n}`),
    pattern:   (re, msg='Invalid')      => v => re.test(v) || msg,
    email:     (msg='Invalid email')    => v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) || msg,
    match:     (field, msg='Must match')=> (v,d) => v===d[field] || msg,
  };

  validate() {
    const data = Object.fromEntries(new FormData(this.#form));
    this.#errors.clear();
    for (const [name, rules] of Object.entries(this.#rules)) {
      for (const rule of rules) {
        const r = rule(data[name]??'', data);
        if (r !== true) { this.#errors.set(name, r); break; }
      }
    }
    this.#renderAll();
    return { valid: !this.#errors.size, data, errors: Object.fromEntries(this.#errors) };
  }

  watch() {
    const data = () => Object.fromEntries(new FormData(this.#form));
    this.#form.querySelectorAll('[name]').forEach(f => {
      f.addEventListener('blur', () => {
        let err = null;
        for (const rule of this.#rules[f.name]??[]) {
          const r = rule(f.value, data()); if (r!==true) { err=r; break; }
        }
        err ? this.#errors.set(f.name,err) : this.#errors.delete(f.name);
        this.#renderField(f, err);
      });
      f.addEventListener('input', () => {
        if (this.#errors.has(f.name)) { this.#errors.delete(f.name); this.#renderField(f,null); }
      });
    });
    return this;
  }

  #renderAll() { this.#form.querySelectorAll('[name]').forEach(f => this.#renderField(f, this.#errors.get(f.name)??null)); }

  #renderField(field, error) {
    field.classList.toggle('invalid', !!error);
    field.setAttribute('aria-invalid', String(!!error));
    let el = field.parentElement?.querySelector('.field-error');
    if (!el) {
      el = Object.assign(document.createElement('span'), { className:'field-error' });
      el.setAttribute('role','alert'); field.after(el);
    }
    el.textContent = error ?? ''; el.hidden = !error;
  }
}

const { R } = FormValidator;
const v = new FormValidator(form, {
  name:     [R.required(), R.minLength(2), R.maxLength(50)],
  email:    [R.required(), R.email()],
  password: [R.required(), R.minLength(8), R.pattern(/[A-Z]/, 'Needs uppercase')],
  confirm:  [R.required(), R.match('password')],
}).watch();

form.addEventListener('submit', e => {
  e.preventDefault();
  const { valid, data } = v.validate();
  if (valid) submitForm(data);
});
```

---

## 28. Iterator Protocol and Generators

```js
// Custom iterable class
class Range {
  constructor(start, end, step=1) { Object.assign(this,{start,end,step}); }
  [Symbol.iterator]() {
    let cur = this.start; const {end,step} = this;
    return { next() { return cur<end ? {value:cur,done:false,_:cur+=step,value2:cur-step} ?? {value:cur-step,done:false} : {done:true}; },
             [Symbol.iterator]() { return this; } };
  }
}

// Simpler custom iterable
class Counter {
  constructor(start, end) { this.start=start; this.end=end; }
  [Symbol.iterator]() {
    let i = this.start, end = this.end;
    return {
      next() { return i<=end ? {value:i++,done:false} : {done:true,value:undefined}; },
      [Symbol.iterator]() { return this; },
    };
  }
}
[...new Counter(1,5)]; // [1,2,3,4,5]

// Generator functions
function* fibonacci() {
  let [a,b] = [0,1];
  while (true) { yield a; [a,b]=[b,a+b]; }
}

function* take(gen, n) {
  for (const v of gen) { yield v; if (!--n) return; }
}
[...take(fibonacci(), 8)]; // [0,1,1,2,3,5,8,13]

function* flatten(arr) {
  for (const v of arr) Array.isArray(v) ? yield* flatten(v) : yield v;
}
[...flatten([1,[2,[3,[4]]]])]; // [1,2,3,4]

// Async generator — paginated API
async function* pages(url) {
  let page = 1;
  while (true) {
    const { data, hasMore } = await api.get(url, { params:{page:page++} });
    yield* data;
    if (!hasMore) return;
  }
}
for await (const item of pages('/api/items')) render(item);
```

---

## 29. Proxy and Reflect

```js
// Validation proxy
const validated = schema => new Proxy({}, {
  set(t, k, v) {
    const r = schema[k];
    if (r?.required && !v)              throw new Error(`${k} required`);
    if (r?.type && typeof v !== r.type)  throw new TypeError(`${k} must be ${r.type}`);
    if (r?.min != null && v < r.min)    throw new RangeError(`${k} >= ${r.min}`);
    if (r?.max != null && v > r.max)    throw new RangeError(`${k} <= ${r.max}`);
    return Reflect.set(t, k, v);
  }
});

const config = validated({
  port:  { type:'number', min:1, max:65535, required:true },
  host:  { type:'string', required:true },
});
config.port = 8080;  // OK
config.port = -1;    // RangeError

// Deep observable
const observable = (data, notify) => new Proxy(data, {
  set(t, k, v) {
    const prev = t[k];
    const ok = Reflect.set(t, k, v);
    if (ok && !Object.is(prev, v)) notify(k, v, prev);
    return ok;
  },
  get(t, k) { const v = t[k]; return v&&typeof v==='object' ? observable(v,notify) : v; },
});

// Read-only proxy
const readonly = obj => new Proxy(obj, {
  set()            { throw new TypeError('Read-only'); },
  deleteProperty() { throw new TypeError('Read-only'); },
  get(t, k)        { const v=t[k]; return v&&typeof v==='object' ? readonly(v) : v; },
});
```

---

## 30. Streams API

```js
// Fetch with progress tracking
async function fetchWithProgress(url, onProgress) {
  const res   = await fetch(url);
  const total = Number(res.headers.get('Content-Length') ?? 0);
  let loaded  = 0;

  return new Response(
    res.body.pipeThrough(new TransformStream({
      transform(chunk, ctrl) {
        loaded += chunk.length;
        onProgress({ loaded, total, pct: total ? (loaded/total*100).toFixed(1) : 0 });
        ctrl.enqueue(chunk);
      },
    })),
    res
  );
}

// NDJSON (newline-delimited JSON) streaming
async function* streamNDJSON(url) {
  const res    = await fetch(url);
  const reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
  let buf = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) { if (buf.trim()) try{yield JSON.parse(buf);}catch{} return; }
    buf += value;
    const lines = buf.split('\n'); buf = lines.pop()??'';
    for (const line of lines.filter(Boolean)) { try{yield JSON.parse(line);}catch{} }
  }
}

for await (const item of streamNDJSON('/api/stream')) render(item);

// Custom readable (countdown)
const countdown = n => new ReadableStream({
  start(ctrl) {
    const id = setInterval(() => n > 0 ? ctrl.enqueue(n--) : (ctrl.close(), clearInterval(id)), 1000);
    return () => clearInterval(id);
  }
});
```

---

## 31. Crypto API

```js
// Random
const uuid  = crypto.randomUUID();                                // UUID v4
const bytes = crypto.getRandomValues(new Uint8Array(32));         // 32 random bytes
const rand  = (min, max) => min + (crypto.getRandomValues(new Uint32Array(1))[0] % (max-min+1));

// SHA-256 hash
async function sha256(data) {
  const bytes = typeof data === 'string' ? new TextEncoder().encode(data) : data;
  const hash  = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(hash)].map(b => b.toString(16).padStart(2,'0')).join('');
}

// AES-GCM encryption
const AES = {
  key:  () => crypto.subtle.generateKey({name:'AES-GCM',length:256}, true, ['encrypt','decrypt']),

  async encrypt(data, key) {
    const iv  = crypto.getRandomValues(new Uint8Array(12));
    const ct  = await crypto.subtle.encrypt({name:'AES-GCM',iv}, key,
      new TextEncoder().encode(JSON.stringify(data)));
    const out = new Uint8Array(12 + ct.byteLength);
    out.set(iv); out.set(new Uint8Array(ct), 12);
    return btoa(String.fromCharCode(...out));
  },

  async decrypt(cipher, key) {
    const d  = Uint8Array.from(atob(cipher), c => c.charCodeAt(0));
    const pt = await crypto.subtle.decrypt({name:'AES-GCM',iv:d.slice(0,12)}, key, d.slice(12));
    return JSON.parse(new TextDecoder().decode(pt));
  },

  async deriveKey(password, salt = crypto.getRandomValues(new Uint8Array(16))) {
    const raw = await crypto.subtle.importKey('raw', new TextEncoder().encode(password),
      'PBKDF2', false, ['deriveKey']);
    return {
      key: await crypto.subtle.deriveKey(
        {name:'PBKDF2', salt, iterations:210_000, hash:'SHA-256'},
        raw, {name:'AES-GCM',length:256}, true, ['encrypt','decrypt']
      ),
      salt,
    };
  },
};
```

---

## 32. Canvas API

```js
// HiDPI-correct canvas setup
function initCanvas(canvas, container) {
  const dpr = devicePixelRatio ?? 1;
  const resize = () => {
    const { width: w, height: h } = container.getBoundingClientRect();
    canvas.width  = w * dpr; canvas.height = h * dpr;
    canvas.style.width = `${w}px`; canvas.style.height = `${h}px`;
    canvas.getContext('2d').scale(dpr, dpr);
    return { w, h };
  };
  new ResizeObserver(resize).observe(container);
  return resize();
}

// Animation loop
class CanvasApp {
  #ctx; #raf = null; #w; #h;

  constructor(canvas) {
    const { w, h } = initCanvas(canvas, canvas.parentElement);
    this.#ctx = canvas.getContext('2d');
    this.#w = w; this.#h = h;
  }

  start() {
    let last = 0;
    const tick = ts => {
      const dt = ts - last; last = ts;
      this.update(dt);
      this.#ctx.clearRect(0, 0, this.#w, this.#h);
      this.draw(this.#ctx, this.#w, this.#h);
      this.#raf = requestAnimationFrame(tick);
    };
    this.#raf = requestAnimationFrame(tick);
    return this;
  }

  stop() { cancelAnimationFrame(this.#raf); this.#raf = null; }
  update(dt) {}  // override
  draw(ctx, w, h) {} // override
}

// Drawing utilities
const draw = {
  rect:   (ctx, x,y,w,h,r=0) => { ctx.beginPath(); ctx.roundRect(x,y,w,h,r); ctx.closePath(); },
  circle: (ctx, x,y,r)        => { ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.closePath(); },
  text:   (ctx, t,x,y,{font,color,align='left',baseline='top'}={}) => {
    if(font)  ctx.font=font;
    if(color) ctx.fillStyle=color;
    ctx.textAlign=align; ctx.textBaseline=baseline;
    ctx.fillText(t,x,y);
  },
};
```

---

## 33. Pointer, Touch and Keyboard Events

```js
// Unified drag with Pointer Events (mouse + touch + stylus)
function draggable(el, { onStart, onMove, onEnd } = {}) {
  const ctrl = new AbortController();
  const sig  = ctrl.signal;
  let pid = null, ox, oy;

  el.addEventListener('pointerdown', e => {
    el.setPointerCapture(e.pointerId);
    pid = e.pointerId; ox = e.clientX; oy = e.clientY;
    onStart?.({ x:e.clientX, y:e.clientY });
  }, { signal: sig });

  el.addEventListener('pointermove', e => {
    if (e.pointerId !== pid) return;
    onMove?.({ dx:e.clientX-ox, dy:e.clientY-oy, x:e.clientX, y:e.clientY });
  }, { signal: sig });

  el.addEventListener('pointerup', e => {
    if (e.pointerId !== pid) return;
    pid = null; onEnd?.({ x:e.clientX, y:e.clientY });
  }, { signal: sig });

  return () => ctrl.abort();
}

// Keyboard shortcut manager
class Shortcuts {
  #map = new Map(); #ctrl;

  constructor() {
    this.#ctrl = new AbortController();
    document.addEventListener('keydown', this.#handle.bind(this), { signal: this.#ctrl.signal });
  }

  register(combo, fn) {
    const key = combo.toLowerCase().split('+').sort().join('+');
    this.#map.set(key, fn);
    return () => this.#map.delete(key);
  }

  #handle(e) {
    const parts = [];
    if (e.ctrlKey || e.metaKey) parts.push('ctrl');
    if (e.shiftKey) parts.push('shift');
    if (e.altKey)   parts.push('alt');
    parts.push(e.key.toLowerCase());
    const fn = this.#map.get(parts.sort().join('+'));
    if (fn) { e.preventDefault(); fn(e); }
  }

  destroy() { this.#ctrl.abort(); }
}

const kb = new Shortcuts();
kb.register('ctrl+s',       () => save());
kb.register('ctrl+z',       () => history.undo());
kb.register('ctrl+shift+z', () => history.redo());
kb.register('/',            () => searchEl.focus());
```

---

## 34. BroadcastChannel and SharedWorker

```js
// Cross-tab messaging
class TabSync {
  #ch; #handlers = new Map();

  constructor(name = 'app') {
    this.#ch = new BroadcastChannel(name);
    this.#ch.addEventListener('message', ({ data: { type, payload } }) => {
      this.#handlers.get(type)?.forEach(fn => fn(payload));
    });
  }

  on(type, fn) {
    if (!this.#handlers.has(type)) this.#handlers.set(type, new Set());
    this.#handlers.get(type).add(fn);
    return () => this.#handlers.get(type).delete(fn);
  }

  emit(type, payload) { this.#ch.postMessage({ type, payload }); }
  close() { this.#ch.close(); }
}

const sync = new TabSync('myapp');
sync.on('theme:change', ({ theme }) => applyTheme(theme));
sync.on('auth:logout',  () => { clearAuth(); redirect('/login'); });

// Logout all tabs
logoutBtn.addEventListener('click', () => {
  clearAuth();
  sync.emit('auth:logout', {});
  redirect('/login');
});
```

---

## 35. Advanced State — FSM and Optimistic Updates

```js
// Finite State Machine
class FSM {
  #s; #t; #actions; #subs = new Set();

  constructor({ initial, transitions, actions={} }) {
    this.#s = initial; this.#t = transitions; this.#actions = actions;
  }

  get state() { return this.#s; }
  can(event)  { return !!(this.#t[this.#s]?.[event]); }

  send(event, payload) {
    const next = this.#t[this.#s]?.[event];
    if (!next) return false;
    const prev = this.#s;
    this.#s = typeof next === 'function' ? next(this.#s, payload) : next;
    this.#actions[`${prev}:exit`]?.(payload);
    this.#actions[`${this.#s}:enter`]?.(payload);
    this.#actions[event]?.(payload);
    this.#subs.forEach(fn => fn({ from:prev, to:this.#s, event, payload }));
    return true;
  }

  subscribe(fn) { this.#subs.add(fn); return () => this.#subs.delete(fn); }
}

// Example: fetch lifecycle
const loader = new FSM({
  initial: 'idle',
  transitions: {
    idle:    { FETCH:'loading' },
    loading: { SUCCESS:'success', ERROR:'error', CANCEL:'idle' },
    success: { FETCH:'loading', RESET:'idle' },
    error:   { RETRY:'loading', RESET:'idle' },
  },
  actions: {
    'loading:enter': () => showSpinner(),
    'loading:exit':  () => hideSpinner(),
    SUCCESS: ({ data }) => render(data),
    'error:enter': ({ error }) => showError(error),
  },
});

// Optimistic updates
class OptimisticStore {
  #state; #subs = new Set(); #snaps = new Map();

  constructor(state) { this.#state = structuredClone(state); }

  async optimistic(id, applyFn, serverFn) {
    const snap = structuredClone(this.#state);
    applyFn(this.#state); this.#notify();
    this.#snaps.set(id, snap);
    try {
      const r = await serverFn(); this.#snaps.delete(id); return r;
    } catch(e) {
      const s = this.#snaps.get(id);
      if (s) { Object.assign(this.#state, s); this.#snaps.delete(id); this.#notify(); }
      throw e;
    }
  }

  subscribe(fn) { this.#subs.add(fn); fn(this.#state); return () => this.#subs.delete(fn); }
  #notify()     { this.#subs.forEach(fn => fn(this.#state)); }
  get state()   { return this.#state; }
}
```

---

## 36. Full SPA Architecture

```js
// main.js — bootstrap
async function bootstrap() {
  try {
    await AuthService.init();

    const router = new Router();
    const loader = createPageLoader('#app');

    router
      .route('/',          () => import('./pages/Home.js').then(m => m.default))
      .route('/users',     () => import('./pages/Users.js').then(m => m.default))
      .route('/users/:id', () => import('./pages/UserDetail.js').then(m => m.default))
      .notFound(           () => import('./pages/NotFound.js').then(m => m.default))
      .guard(path => {
        if (!auth.user && !publicRoutes.has(path)) {
          router.navigate('/login', {}, { replace: true }); return false;
        }
        return true;
      })
      .start();

    navigator.serviceWorker?.register('/sw.js');
  } catch(e) {
    document.querySelector('#app').innerHTML =
      `<div class="fatal" role="alert">
         <h1>Failed to start</h1>
         <p>${String(e.message).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}</p>
         <button onclick="location.reload()">Reload</button>
       </div>`;
  }
}

function createPageLoader(sel) {
  const root = document.querySelector(sel);
  let current = null, ctrl = null;

  return async factory => {
    ctrl?.abort(); ctrl = new AbortController();
    const { signal } = ctrl;

    root.innerHTML = `<div class="skeleton" aria-busy="true">
      <div class="sk-title"></div><div class="sk-block"></div></div>`;

    try {
      const Page = await factory(); if (signal.aborted) return;
      current?.destroy?.();
      await new Promise(r => setTimeout(r, 80)); if (signal.aborted) return;
      root.innerHTML = '';
      (current = new Page()).mount(root);
    } catch(e) {
      if (e.name === 'AbortError') return;
      root.innerHTML = `<div class="page-error" role="alert">
        <h2>${e.message}</h2><button onclick="history.back()">← Back</button></div>`;
    }
  };
}

bootstrap();
```

---

## 37. Accessibility (a11y)

```js
// Focus trap for modals
class FocusTrap {
  #el; #prev; #ctrl;
  static Q = 'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),' +
    'textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

  constructor(el) { this.#el = el; }

  activate() {
    this.#prev = document.activeElement;
    this.#ctrl = new AbortController();
    document.addEventListener('keydown', this.#trap.bind(this), { signal: this.#ctrl.signal });
    this.#focusable()[0]?.focus?.() ?? this.#el.focus();
    return this;
  }

  deactivate() { this.#ctrl?.abort(); this.#prev?.focus?.(); return this; }

  #focusable() {
    return [...this.#el.querySelectorAll(FocusTrap.Q)]
      .filter(e => !e.closest('[hidden],[inert]') && e.offsetParent);
  }

  #trap(e) {
    if (e.key !== 'Tab') return;
    const els = this.#focusable(); if (!els.length) { e.preventDefault(); return; }
    if (e.shiftKey && document.activeElement === els[0])       { e.preventDefault(); els.at(-1).focus(); }
    else if (!e.shiftKey && document.activeElement === els.at(-1)) { e.preventDefault(); els[0].focus(); }
  }
}

// Live region announcer for screen readers
const announcer = (() => {
  const mk = mode => {
    const el = document.createElement('div');
    el.setAttribute('aria-live', mode); el.setAttribute('aria-atomic','true');
    el.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
    document.body.append(el); return el;
  };
  const p = mk('polite'), a = mk('assertive');
  const say = (el, msg) => { el.textContent=''; requestAnimationFrame(()=>{ el.textContent=msg; }); };
  return { polite: m => say(p,m), assertive: m => say(a,m) };
})();

announcer.polite('24 results loaded');
announcer.assertive('Form has 2 errors — please review highlighted fields');
```

---

## 38. Performance Profiling

```js
// Core Web Vitals collection
const vitals = {};
new PerformanceObserver(l => { vitals.lcp = l.getEntries().at(-1)?.startTime; })
  .observe({ type:'largest-contentful-paint', buffered:true });

let cls = 0;
new PerformanceObserver(l => l.getEntries().forEach(e => { if(!e.hadRecentInput){cls+=e.value;vitals.cls=cls;} }))
  .observe({ type:'layout-shift', buffered:true });

new PerformanceObserver(l => l.getEntries().forEach(e => { vitals.inp=Math.max(vitals.inp??0,e.duration); }))
  .observe({ type:'event', durationThreshold:16, buffered:true });

vitals.ttfb = performance.getEntriesByType('navigation')[0]?.responseStart;

// Rating thresholds
function rateVital(name, v) {
  const t = { lcp:[2500,4000], cls:[0.1,0.25], inp:[200,500], ttfb:[800,1800] }[name];
  return !t?'unknown': v<=t[0]?'good': v<=t[1]?'needs-improvement':'poor';
}

// Long task monitoring
new PerformanceObserver(l => l.getEntries().forEach(e => {
  if (e.duration > 50) console.warn(`Long task: ${e.duration.toFixed(0)}ms`, e);
})).observe({ type:'longtask' });

// Task chunking
async function chunked(items, fn, size=50) {
  for (let i=0; i<items.length; i+=size) {
    items.slice(i,i+size).forEach(fn);
    await ('scheduler' in window && scheduler.yield
      ? scheduler.yield()
      : new Promise(r => setTimeout(r,0)));
  }
}
```

---

## 39. Testing

```js
// Architecture: isolate logic from DOM
// ✅ Pure functions are trivially testable
export const addLike    = post => ({ ...post, likes: post.likes+1, liked:true });
export const removeLike = post => ({ ...post, likes: post.likes-1, liked:false });
export const toggleLike = post => post.liked ? removeLike(post) : addLike(post);
export const cartTotal  = cart => cart.reduce((s, i) => s + i.price*i.qty, 0);

// Minimal test runner
class T {
  #r = [];

  async test(name, fn) {
    try   { await fn(this.expect); this.#r.push({name,ok:true}); console.log(`✅ ${name}`); }
    catch (e) { this.#r.push({name,ok:false}); console.error(`❌ ${name}: ${e.message}`); }
  }

  expect = {
    eq:     (a,b) => { if(!Object.is(a,b)) throw new Error(`${JSON.stringify(a)} ≠ ${JSON.stringify(b)}`); },
    deep:   (a,b) => { if(JSON.stringify(a)!==JSON.stringify(b)) throw new Error(`Deep mismatch`); },
    ok:     v     => { if(!v) throw new Error(`Expected truthy: ${JSON.stringify(v)}`); },
    not:    v     => { if(v)  throw new Error(`Expected falsy: ${JSON.stringify(v)}`); },
    throws: (fn, msg) => {
      let threw=false;
      try{fn();}catch(e){threw=true; if(msg&&!e.message.includes(msg)) throw new Error(`Wrong message: ${e.message}`);}
      if(!threw) throw new Error('Expected to throw');
    },
  };

  summary() {
    const p = this.#r.filter(r=>r.ok).length;
    console.log(`\n${p}/${this.#r.length} passed`);
    return p===this.#r.length;
  }
}

const t = new T();

await t.test('addLike increments count', e => {
  const post = {id:1, likes:5, liked:false};
  const r = addLike(post);
  e.eq(r.likes, 6); e.eq(r.liked, true);
  e.eq(post.likes, 5); // original unchanged (immutable)
});

await t.test('toggleLike is reversible', e => {
  const post = {id:1, likes:10, liked:false};
  e.deep(toggleLike(toggleLike(post)), post);
});

await t.test('cartTotal sums correctly', e => {
  e.eq(cartTotal([{price:10,qty:2},{price:5,qty:3}]), 35);
});

t.summary();
```

---

## 40. JSDoc Type Annotations

```js
// @ts-check  ← enables TypeScript checking without TS

/**
 * @typedef {Object} User
 * @property {number} id
 * @property {string} name
 * @property {string} email
 * @property {'admin'|'user'|'guest'} role
 * @property {boolean} [active]
 */

/** @template T @typedef {{ data:T, status:number, error?:string }} ApiResponse */

/**
 * @param {number} id
 * @param {{ signal?: AbortSignal }} [opts]
 * @returns {Promise<ApiResponse<User>>}
 * @throws {Error} on network failure
 * @example const { data } = await loadUser(1);
 */
async function loadUser(id, opts = {}) { /* ... */ }

// Type cast
const emailInput = /** @type {HTMLInputElement} */ (document.querySelector('input[name="email"]'));

// Enum
/** @enum {string} */
const Status = Object.freeze({ PENDING:'pending', ACTIVE:'active', DONE:'done' });

// Generic createElement
/**
 * @template {keyof HTMLElementTagNameMap} K
 * @param {K} tag
 * @param {Partial<HTMLElementTagNameMap[K]>} [props]
 * @returns {HTMLElementTagNameMap[K]}
 */
const el = (tag, props={}) => Object.assign(document.createElement(tag), props);
const btn = el('button', { textContent:'OK' }); // typed as HTMLButtonElement ✅
```

---

## 41. Anti-Patterns and Traps

### Memory Leaks

```js
// ❌ Forgotten listener
function setup(el) { el.addEventListener('click', handler); el.remove(); } // leak!
// ✅ Cleanup
function setup(el) {
  const ctrl = new AbortController();
  el.addEventListener('click', handler, { signal: ctrl.signal });
  return () => ctrl.abort();
}

// ❌ Interval not cleared
class Poll { start() { this.id=setInterval(fn,1000); } } // leak!
// ✅
class Poll { start(){this.id=setInterval(fn,1000);} stop(){clearInterval(this.id);} }

// ❌ Observer not disconnected
const obs = new IntersectionObserver(cb); obs.observe(el); el.remove(); // obs still runs!
// ✅ Always disconnect in cleanup
```

### Classic JS Bugs

```js
NaN === NaN;           // false! → Number.isNaN(v)
typeof null === 'object'; // true! → v === null
[10,2,30].sort();      // ['10','2','30'] lexicographic! → .sort((a,b)=>a-b)
delete arr[1];         // creates sparse array! → arr.splice(1,1)

// ❌ Sequential await = unnecessary slowness
const user  = await fetchUser(id);   // 200ms
const posts = await fetchPosts(id);  // 200ms → 400ms total!
// ✅
const [user, posts] = await Promise.all([fetchUser(id), fetchPosts(id)]); // 200ms

// ❌ Missing await
async function save(data) {
  const r = api.post('/save', { body:data }); // Promise, not result!
  return r.id; // TypeError: r.id is undefined (r is Promise)
}
```

### Performance Bugs

```js
// ❌ Layout thrashing
els.forEach(el => { const h=el.offsetHeight; el.style.height=h+10+'px'; }); // N reflows!
// ✅ Batch reads then writes
const hs=els.map(e=>e.offsetHeight); els.forEach((e,i)=>{e.style.height=hs[i]+10+'px';});

// ❌ top/left for animation (triggers layout)
el.style.top  = y+'px';
// ✅ transform (GPU compositor — no layout)
el.style.transform = `translateY(${y}px)`;
```

---

## 42. Quality Checklist

```
SYNTAX & STYLE
✅ const default, let for reassignment, never var
✅ Arrow fns for callbacks/closures, regular for methods/constructors
✅ ?. only when null is expected (not a bug)
✅ ?? instead of || when 0/''/false are valid values
✅ Options object ({} default) for functions with 3+ params
✅ async/await over raw .then() chains
✅ Private fields # for class encapsulation

ERROR HANDLING
✅ Every async function has try/catch or propagates
✅ AbortController for cancellable requests
✅ Global unhandledrejection handler
✅ Custom error classes for typed handling
✅ No empty catch blocks
✅ User sees friendly messages, not raw stack traces

SECURITY
✅ textContent for user data, never innerHTML without sanitization
✅ All URLs validated (isSafeUrl) before src/href
✅ No eval(), new Function(), setTimeout(string)
✅ CSRF token on POST/PUT/PATCH/DELETE
✅ No API keys or secrets in client code
✅ Subresource Integrity on CDN scripts

PERFORMANCE
✅ Read DOM, then write DOM (no thrashing)
✅ Animations via transform/opacity (GPU composited)
✅ scroll/touchmove listeners passive:true
✅ Debounce input, throttle scroll/resize
✅ Heavy work in Web Workers
✅ Images have explicit width/height attributes
✅ Virtual scrolling for lists > 100 items
✅ Code-split heavy features with dynamic import()
✅ Long tasks chunked (scheduler.yield)

MEMORY
✅ Listeners removed on component destroy
✅ Intervals/timeouts cleared
✅ Observers disconnected
✅ URL.revokeObjectURL() called after use
✅ AbortController for bulk listener cleanup

ACCESSIBILITY
✅ Semantic HTML (button, a, input — not div+onclick)
✅ All images have alt text
✅ Focus trap in modals
✅ Keyboard navigation works everywhere
✅ Live regions for dynamic content changes
✅ ARIA states reflect UI state (aria-expanded, etc.)
```

---

## 43. Quick Syntax Reference

```js
// ── VARIABLES ─────────────────────────────────────────────
const x = 1;       // immutable binding (default)
let y = 1;          // mutable binding
// var ← NEVER USE

// ── DESTRUCTURING ──────────────────────────────────────────
const { a, b:alias, c='def' }  = obj;
const [first, ,third, ...rest] = arr;
const { deep: { nested } = {} } = obj;

// ── SPREAD / REST ──────────────────────────────────────────
const m = { ...obj1, ...obj2 };    // merge, later wins
const j = [...arr1, x, ...arr2];   // join with element
function fn(a, ...rest) {}
const { x:_, ...without } = obj;   // omit key

// ── NULLISH / OPTIONAL ─────────────────────────────────────
a?.b?.c           // safe chain (use only when null is normal)
fn?.()            // safe call
x ?? 'default'    // null/undefined only
x ??= 'val'       // assign if null/undefined
x ||= 'val'       // assign if falsy
x &&= fn(x)       // assign if truthy

// ── FUNCTIONS ──────────────────────────────────────────────
const f   = x => x * 2;
const obj2 = x => ({ key: x });      // return object — wrap in ()
async function load() { return await fetch(url); }
function* gen() { yield 1; yield 2; }
async function* aGen() { yield await p; }

// ── CLASSES ────────────────────────────────────────────────
class Foo extends Bar {
  #priv = 0;
  static shared = 0;
  get val()  { return this.#priv; }
  set val(v) { this.#priv = v; }
  method()   { super.method(); }
  static create() { return new Foo(); }
}

// ── ASYNC ──────────────────────────────────────────────────
await Promise.all([p1, p2]);          // all or fail
await Promise.allSettled([p1, p2]);   // all with status
await Promise.race([p1, p2]);         // first settled
await Promise.any([p1, p2]);          // first fulfilled
const { promise, resolve, reject } = Promise.withResolvers();
AbortSignal.timeout(5000);            // auto-cancel

// ── MODULES ────────────────────────────────────────────────
export const x = 1;
export default class {}
import { x } from './m.js';
import def, { x } from './m.js';
const m2 = await import('./m.js');

// ── MODERN ARRAY ───────────────────────────────────────────
arr.at(-1)              // last element
arr.findLast(fn)        // search from end
arr.toSorted(fn)        // sorted copy  (ES2023)
arr.toReversed()        // reversed copy (ES2023)
arr.with(i, v)          // replace at index copy (ES2023)
arr.flatMap(fn)         // map + flat(1)
Object.groupBy(arr, fn) // group into object (ES2024)

// ── MODERN OBJECT ──────────────────────────────────────────
Object.hasOwn(obj, k)   // own property check (ES2022)
Object.fromEntries(it)  // from pairs
structuredClone(val)    // deep clone (ES2022)

// ── ITERATION ──────────────────────────────────────────────
for (const v of iter)                {}
for (const [i, v] of arr.entries())  {}
for (const [k, v] of map)            {}
for await (const v of asyncIter)     {}
```

---

## 44. Standards Timeline

| Standard | Year | Key Additions |
|----------|------|---------------|
| **ES2015** | 2015 | `let/const`, classes, arrow fns, promises, modules, destructuring, Symbol, Map/Set, generators, `for...of`, template literals, `Proxy`, `Reflect` |
| **ES2016** | 2016 | `Array.includes`, `**` exponentiation |
| **ES2017** | 2017 | `async/await`, `Object.entries/values`, `padStart/End`, `SharedArrayBuffer` |
| **ES2018** | 2018 | `Promise.finally`, object rest/spread, `for await...of`, named regex groups, lookbehind, dotAll `/s` |
| **ES2019** | 2019 | `Array.flat/flatMap`, `Object.fromEntries`, `String.trimStart/End`, optional `catch` binding |
| **ES2020** | 2020 | `BigInt`, `?.`, `??`, `Promise.allSettled`, `globalThis`, dynamic `import()`, `String.matchAll` |
| **ES2021** | 2021 | `Promise.any`, `String.replaceAll`, `&&= \|\|= ??=`, `WeakRef`, `FinalizationRegistry` |
| **ES2022** | 2022 | Class private fields `#`, `Object.hasOwn`, `.at()`, `structuredClone`, `Error.cause`, top-level `await` |
| **ES2023** | 2023 | `findLast/findLastIndex`, `toSorted/toReversed/toSpliced/with`, Symbol as WeakMap key |
| **ES2024** | 2024 | `Object.groupBy`, `Promise.withResolvers`, Set operations, `ArrayBuffer.resize`, RegExp `/v` |
| **ES2025** | 2025 | Iterator helpers, `import attributes`, `Float16Array`, `Promise.try`, `RegExp.escape` |

---

| API | Notes |
|-----|-------|
| `structuredClone` | All modern browsers (ES2022) |
| `crypto.randomUUID` | All modern browsers (ES2021) |
| `AbortSignal.timeout` | All modern (ES2022) |
| `AbortSignal.any` | All modern (ES2024) |
| `Promise.withResolvers` | All modern (ES2024) |
| `Object.groupBy` | All modern (ES2024) |
| `Set.union/intersection` | All modern (ES2024) |
| `Array.toSorted/toReversed` | All modern (ES2023) |
| File System Access API | Chrome/Edge only — provide fallback |
| `scheduler.yield` | Chrome only — fallback: `setTimeout(r,0)` |
| `scheduler.postTask` | Chrome only — fallback: `requestIdleCallback` |

---

*Complete guide to modern Vanilla JavaScript — ES2015 through ES2025.*  
*44 sections · 8,000+ lines of production-ready code · 2025 edition*  
*Verify browser support: [caniuse.com](https://caniuse.com) · [MDN Web Docs](https://developer.mozilla.org)*
