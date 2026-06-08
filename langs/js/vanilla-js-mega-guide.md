# The Complete Vanilla JavaScript Mega-Guide for AI Agents

> **Version:** 2025 | **Coverage:** ES2015 → ES2025 | **Runtime:** Browser (no Node.js)  
> **Purpose:** Single, unified, self-sufficient reference for writing correct, modern, pure JavaScript.  
> **Combines:** All unique content from both EN and RU guides — nothing omitted.

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
39. [Performance Profiling and Core Web Vitals](#39-performance-profiling-and-core-web-vitals)
40. [Testing Vanilla JS](#40-testing-vanilla-js)
41. [JSDoc Type Annotations](#41-jsdoc-type-annotations)
42. [Geolocation and Device APIs](#42-geolocation-and-device-apis)
43. [Virtual Scrolling](#43-virtual-scrolling)
44. [Temporal API](#44-temporal-api)
45. [WeakRef and FinalizationRegistry](#45-weakref-and-finalizationregistry)
46. [Anti-Patterns and Traps](#46-anti-patterns-and-traps)
47. [Quality Checklist](#47-quality-checklist)
48. [Quick Syntax Reference](#48-quick-syntax-reference)
49. [Standards Timeline](#49-standards-timeline)

---
## 1. Philosophy of Modern JS

### 1.1 Core Principles

```
1.  Declarative over imperative
2.  Immutability by default — mutation is the exception
3.  Functions: pure, predictable, side-effect-free
4.  Explicit over implicit
5.  Error handling is mandatory, never optional
6.  Accessibility and performance from day one
7.  Use the platform (Web APIs), don't fight it
8.  Own your lifecycle — always clean up after yourself
9.  Composition over inheritance
10. The rule of least power — use the simplest solution that works
```

### 1.2 The Modern JS Landscape

| Era | Standard | Key Features |
|-----|----------|--------------|
| Legacy | ES5 (2009) | `var`, prototype chains, `arguments`, callbacks |
| Transitional | ES2015 | `let/const`, classes, arrow fns, promises, modules |
| Mature | ES2017–2020 | `async/await`, `?.`, `??`, `globalThis` |
| Modern | ES2021–2025 | `at()`, `structuredClone`, `groupBy`, top-level await, Set methods |

### 1.3 Feature Detection Pattern

```js
// ❌ Assume everything exists
new Scheduler().postTask(fn);

// ✅ Detect capability, provide fallback
async function scheduleTask(fn, priority = 'normal') {
  if ('scheduler' in window && window.scheduler.postTask) {
    return window.scheduler.postTask(fn, { priority });
  }
  if (priority === 'background' && 'requestIdleCallback' in window) {
    return new Promise(r => requestIdleCallback(() => r(fn())));
  }
  return Promise.resolve().then(fn);
}
```

### 1.4 Architecture Philosophy

```
┌─────────────────────────────────────────┐
│              UI Layer (DOM)             │  ← Impure (side effects OK)
├─────────────────────────────────────────┤
│          State / Store Layer            │  ← Controlled mutation
├─────────────────────────────────────────┤
│       Business Logic (Pure Fns)         │  ← Fully testable, pure
├─────────────────────────────────────────┤
│      Services (API, Storage, WS)        │  ← Impure, encapsulated
└─────────────────────────────────────────┘
```

---

## 2. Variables and Scope

### 2.1 The Golden Rule: Never `var`

```js
// ❌ var — function-scoped, hoisted, leaks
function broken() {
  if (true) { var x = 10; }
  console.log(x); // 10 — leaks out of if-block!
}
for (var i = 0; i < 3; i++) { setTimeout(() => console.log(i), 0); } // 3 3 3!

// ✅ const by default — immutable binding
const PI     = 3.14159;
const config = Object.freeze({ debug: false, version: '2.0' });

// ✅ let only when reassignment is needed
let count = 0;
count++;
for (let i = 0; i < 3; i++) { setTimeout(() => console.log(i), 0); } // 0 1 2 ✅

// const binding is immutable, the VALUE is not
const user = { name: 'Alice' };
user.name = 'Bob';  // OK — mutates property
user = {};          // SyntaxError — reassigns binding
```

### 2.2 Temporal Dead Zone (TDZ)

```js
// let/const are NOT initialized until their declaration line
console.log(a); // ReferenceError: Cannot access 'a' before initialization
let a = 5;

// var is hoisted with undefined — silent killer
console.log(b); // undefined — no error! Hidden bug.
var b = 5;

// Classes also have TDZ
const obj = new Foo(); // ReferenceError!
class Foo {}

// Practical TDZ trap
function withTDZ() {
  // Even though `x` is declared below, it's in TDZ here
  const fn = () => console.log(x); // fn captures x — but TDZ applies at CALL time? No.
  // Actually: TDZ applies at READ time. fn() called after x is initialized is fine.
  let x = 42;
  fn(); // 42 — OK because x is initialized before fn() is called
}
```

### 2.3 Closures — Encapsulation

```js
// Closure: function that captures variables from enclosing scope
function createCounter(initial = 0) {
  let count = initial; // private — not accessible from outside

  return {
    increment: () => ++count,
    decrement: () => --count,
    reset:     () => { count = initial; },
    get value()  { return count; },
  };
}

const c = createCounter(10);
c.increment(); // 11
c.value;       // 11
c.count;       // undefined — truly private!

// Classic closure trap with var
const fns = [];
for (var i = 0; i < 3; i++) { fns.push(() => i); }
fns.map(f => f()); // [3, 3, 3] — all share same `i`

// Fix with let (new binding per iteration)
const fns2 = [];
for (let i = 0; i < 3; i++) { fns2.push(() => i); }
fns2.map(f => f()); // [0, 1, 2] ✅

// Or with IIFE (old-school fix)
for (var i = 0; i < 3; i++) {
  fns.push(((j) => () => j)(i));
}
```

### 2.4 Destructuring — Complete Reference

```js
// ── Array ─────────────────────────────────────────────────
const [a, b, , d]          = [1, 2, 3, 4];     // skip index 2
const [first, ...rest]     = [1, 2, 3, 4];     // rest element
const [x = 0, y = 0]      = [10];              // defaults
let p = 1, q = 2;
[p, q] = [q, p];                               // swap — no temp!

// ── Object ────────────────────────────────────────────────
const { name, age = 0 }            = user;      // with default
const { name: userName }           = user;      // rename
const { addr: { city } = {} }     = user;      // nested + safe default
const { a: _, ...withoutA }       = obj;       // omit key

// ── Function parameters ────────────────────────────────────
function init({
  title = '',
  debug = false,
  onReady = null,
  retries = 3,
} = {}) {}   // ← {} prevents TypeError when called with no args

// ── Dynamic keys ──────────────────────────────────────────
const key = 'email';
const { [key]: email } = user; // extracts user.email into `email`

// ── In iterations ─────────────────────────────────────────
for (const [i, v]  of array.entries())    { /* i=index, v=value */ }
for (const [k, v]  of map)               { /* Map pairs */ }
for (const [k, v]  of Object.entries(o)) { /* Object pairs */ }

// ── Nested with aliases and defaults ─────────────────────
const {
  user: {
    name:     userName2 = 'Anonymous',
    address: { city: userCity = 'Unknown' } = {},
  } = {},
} = apiResponse;
```

---

## 3. Data Types and Structures

### 3.1 Type System

```js
// typeof — reliable for primitives
typeof 42           // 'number'
typeof 42n          // 'bigint'
typeof 'str'        // 'string'
typeof true         // 'boolean'
typeof undefined    // 'undefined'
typeof null         // 'object' ← historical bug!
typeof Symbol()     // 'symbol'
typeof {}           // 'object'
typeof []           // 'object'
typeof function(){} // 'function'

// Reliable type helper
const typeOf = v => {
  if (v === null)       return 'null';
  if (Array.isArray(v)) return 'array';
  if (v instanceof Map) return 'map';
  if (v instanceof Set) return 'set';
  if (v instanceof Date) return 'date';
  return typeof v;
};

// Number checks — always prefer Number.* over globals
Number.isFinite(42);         // true  (global isFinite coerces — avoid!)
Number.isNaN(NaN);           // true  (global isNaN coerces — avoid!)
Number.isNaN('NaN');         // false ← global isNaN('NaN') returns true! (BUG!)
Number.isInteger(4.0);       // true
Number.isSafeInteger(2**53); // false — exceeds safe integer range
```

### 3.2 Numbers — Gotchas

```js
// Floating-point comparison — never use ===
0.1 + 0.2 === 0.3;                               // false!
Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON;     // true ✅

// BigInt for large integers
const big = 9007199254740991n + 1n;  // precise (Number would lose precision)
BigInt(42);                           // from Number
typeof 42n;                           // 'bigint'
// ⚠️ Cannot mix BigInt with Number in arithmetic
// 1n + 1;    // TypeError!
1n + BigInt(1); // 2n ✅

// Numeric separators (readability)
const million     = 1_000_000;
const hex         = 0xFF_FF_FF;
const binary      = 0b1010_0001;
const big2        = 9_007_199_254_740_991n;
```

### 3.3 Strings — Modern Methods

```js
// Access
'hello'.at(-1);          // 'o' — last character
[...'A😀B'].length;       // 3 — correct Unicode iteration
Array.from('A😀B');      // ['A', '😀', 'B']

// Search
'hello'.includes('ell'); // true
'hello'.startsWith('he');// true
'hello'.endsWith('lo');  // true

// Transform
'  trim me  '.trimStart();        // 'trim me  '
'  trim me  '.trimEnd();          // '  trim me'
'abc'.repeat(3);                  // 'abcabcabc'
'hello'.padStart(8, '0');         // '000hello'
'hi cd'.replaceAll(' ', '_');     // 'hi_cd'

// Tagged template for XSS-safe HTML
function safeHtml(strings, ...vals) {
  return strings.reduce((out, str, i) =>
    out + (i ? String(vals[i-1]).replace(
      /[&<>"']/g,
      c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])
    ) : '') + str
  );
}
const output = safeHtml`<p class="${cls}">${userInput}</p>`; // XSS-safe
```

### 3.4 Arrays — Complete Reference

```js
const arr = [3, 1, 4, 1, 5, 9, 2, 6];

// ── Mutating (use carefully, copy first if immutability matters) ──
arr.push(7);              // append, returns new length
arr.pop();                // remove last, returns it
arr.unshift(0);           // prepend, returns new length
arr.shift();              // remove first, returns it
arr.sort((a,b) => a-b);  // sorts IN PLACE — always pass comparator!
arr.reverse();            // reverses IN PLACE
arr.splice(2, 1, 99);    // remove+insert IN PLACE, returns removed

// ── ES2023 Immutable copies ────────────────────────────────
arr.toSorted((a,b) => a-b);   // sorted copy — original untouched
arr.toReversed();              // reversed copy
arr.with(0, 99);               // copy with index 0 replaced
arr.toSpliced(2, 1, 99);      // copy with elements replaced

// ── Classic immutable patterns ────────────────────────────
const sorted   = [...arr].sort((a,b) => a-b);
const appended = [...arr, 7];
const removed  = arr.filter((_, i) => i !== 2);
const updated  = arr.map((v, i) => i === 2 ? 99 : v);

// ── Access ────────────────────────────────────────────────
arr.at(0);    // first
arr.at(-1);   // last
arr.at(-2);   // second to last

// ── Search ────────────────────────────────────────────────
arr.find(x => x > 5);           // 9 — first match
arr.findIndex(x => x > 5);      // 5 — index of first match
arr.findLast(x => x < 5);       // 2 — last match (from end)
arr.findLastIndex(x => x < 5);  // 6 — index of last match
arr.indexOf(1);                  // 1 — first occurrence
arr.lastIndexOf(1);              // 3 — last occurrence
arr.includes(5);                 // true
arr.every(x => x > 0);          // true — all match
arr.some(x => x > 8);           // true — at least one matches

// ── Transform ─────────────────────────────────────────────
arr.map(x => x * 2);                                  // new array, same length
arr.filter(x => x % 2 === 0);                         // new array, subset
arr.reduce((acc, v) => acc + v, 0);                   // fold to value
arr.reduceRight((acc, v) => acc + v, 0);              // fold right-to-left
arr.flatMap(x => [x, -x]);                            // map then flat(1)
[1,[2,[3,[4]]]].flat(Infinity);                       // [1,2,3,4]

// ── Creation ──────────────────────────────────────────────
Array.from({ length: 5 }, (_, i) => i * 2);  // [0,2,4,6,8]
Array.from('hello');                           // ['h','e','l','l','o']
Array.from(new Set([1,1,2]));                 // [1,2]
Array.from(map.values());                     // from Map values
Array.of(1, 2, 3);                           // [1,2,3]
new Array(5).fill(0);                         // [0,0,0,0,0]
[...generator()];                             // from any iterable

// ── Grouping (ES2024) ─────────────────────────────────────
Object.groupBy([1,2,3,4,5], n => n%2===0 ? 'even':'odd');
// { odd:[1,3,5], even:[2,4] }
Map.groupBy([1,2,3,4,5], n => n%2===0);
// Map { false=>[1,3,5], true=>[2,4] }
```

### 3.5 Objects — Modern Methods

```js
const obj = { a: 1, b: 2, c: 3 };

// Inspection
Object.keys(obj);           // ['a','b','c']
Object.values(obj);         // [1,2,3]
Object.entries(obj);        // [['a',1],['b',2],['c',3]]
Object.hasOwn(obj, 'a');   // true (ES2022 — use over hasOwnProperty)
'a' in obj;                 // true (includes prototype chain!)

// Transform via entries — powerful pattern
const doubled = Object.fromEntries(
  Object.entries(prices).map(([k, v]) => [k, v * 2])
);
const filtered = Object.fromEntries(
  Object.entries(obj).filter(([, v]) => v > 1)
);

// Merge (shallow — later source wins)
const merged  = { ...defaults, ...overrides };
const updated = { ...user, role: 'admin', updatedAt: new Date() };

// Deep clone (ES2022) — no JSON.parse/stringify needed
const clone = structuredClone(original);
// Handles: Date, Map, Set, ArrayBuffer, RegExp, Error, circular refs
// Cannot: Function, DOM nodes, WeakMap, Symbol

// Freeze (SHALLOW — nested objects are still mutable)
const frozen = Object.freeze({ x: 1, nested: { y: 2 } });
frozen.x = 99;          // fails silently (TypeError in strict mode)
frozen.nested.y = 99;   // WORKS — freeze is shallow!

// Deep freeze
function deepFreeze(obj) {
  Object.freeze(obj);
  Object.values(obj)
    .filter(v => v && typeof v === 'object' && !Object.isFrozen(v))
    .forEach(deepFreeze);
  return obj;
}

// Grouping (ES2024)
Object.groupBy(people, p => p.department);
// { engineering: [...], design: [...], ... }
```

### 3.6 Map and Set — When to Use Over Object/Array

```js
// ── Map: use when ──────────────────────────────────────────
// • Keys are non-string types
// • You need guaranteed insertion order
// • You need .size property
// • You want to avoid prototype pollution
// • You iterate entries often

const map = new Map([['key', 1], [42, 'num'], [objRef, 'ref']]);
map.set('new', 'value');
map.get('key');     // 1
map.has(42);        // true
map.size;           // 4
map.delete('key');
for (const [k, v] of map) { /*...*/ }
[...map.keys()];  [...map.values()];  [...map.entries()];

// Convert Object ↔ Map
const fromObj = new Map(Object.entries(obj));
const toObj   = Object.fromEntries(map);

// ── WeakMap: GC-friendly private data ─────────────────────
const _private = new WeakMap();
class Secure {
  constructor(secret) { _private.set(this, { secret }); }
  getSecret()         { return _private.get(this).secret; }
}
// When Secure instance is GC'd, WeakMap entry is too

// ── Set: unique values, O(1) has() ────────────────────────
const set = new Set([1, 2, 2, 3, 3, 3]); // {1, 2, 3}
set.add(4); set.has(2); set.size;
const unique = [...new Set(array)]; // deduplicate array

// ── Set operations (ES2024) ───────────────────────────────
const a = new Set([1,2,3,4]), b = new Set([3,4,5,6]);
a.union(b);               // {1,2,3,4,5,6}
a.intersection(b);        // {3,4}
a.difference(b);          // {1,2}
a.symmetricDifference(b); // {1,2,5,6}
a.isSubsetOf(b);          // false
a.isSupersetOf(new Set([1,2])); // true
a.isDisjointFrom(new Set([7,8])); // true
```

### 3.7 Symbol

```js
// Unique primitive — no two Symbols are ever equal
const id  = Symbol('id');
const id2 = Symbol('id');
id === id2; // false

// As "private-ish" object key (not enumerable, not in for...in)
const _cache = Symbol('cache');
class Service {
  constructor() { this[_cache] = new Map(); }
}

// Global registry
const globalId = Symbol.for('app.id');    // create or retrieve
Symbol.keyFor(globalId);                   // 'app.id'

// Well-known symbols — hook into language protocols
class Range {
  constructor(start, end) { this.start=start; this.end=end; }
  [Symbol.iterator]() {
    let cur = this.start; const end = this.end;
    return {
      next: () => cur<=end ? {value:cur++,done:false} : {done:true},
      [Symbol.iterator]() { return this; }
    };
  }
  [Symbol.toPrimitive](hint) {
    return hint === 'number' ? this.end - this.start : `Range(${this.start}..${this.end})`;
  }
}
[...new Range(1,5)]; // [1,2,3,4,5]
+new Range(1,5);     // 4 (numeric hint)
`${new Range(1,5)}`; // 'Range(1..5)' (string hint)
```

---

## 4. Modern ES6+ Syntax

### 4.1 Optional Chaining `?.`

```js
// Safe property access — use ONLY when null/undefined is a VALID state
// If null indicates a bug — let it throw so you find the bug!

user?.profile?.avatar?.url       // property chain
arr?.[0]                         // array access
obj?.[dynamicKey]                // dynamic key
obj?.method?.()                  // method call
callback?.()                     // function call

// With defaults
const name  = user?.displayName ?? 'Anonymous';
const count = response?.data?.items?.length ?? 0;

// In optional call chains
const result = data?.filter?.(x => x.active)?.map?.(x => x.name);
```

### 4.2 Nullish Coalescing `??` and Logical Assignment

```js
// ?? fires ONLY on null/undefined  (NOT 0, '', false, NaN)
// || fires on ANY falsy value

const port    = opts.port    ?? 3000;  // preserves 0 ✅
const timeout = opts.timeout ?? 5000;  // preserves 0 ✅
const label   = opts.label   ?? '';   // preserves '' ✅
const debug   = opts.debug   ?? false; // preserves false ✅

// ❌ Wrong — || replaces valid falsy values
const port2 = opts.port || 3000; // opts.port=0 → 3000 (BUG!)

// ── Logical assignment operators (ES2021) ──────────────────
a ??= 'default';     // a = a ?? 'default'  (only if null/undefined)
a ||= 'fallback';    // a = a || 'fallback'  (if falsy)
a &&= transform(a);  // a = a && transform(a) (if truthy)

// Practical uses
cache[key] ??= expensiveCompute(key);  // lazy initialization
user.settings ??= {};                   // initialize sub-object
el.dataset.count ??= '0';             // default attribute
```

### 4.3 Spread and Rest

```js
// ── REST: collect remaining items into array ───────────────
function sum(first, ...others) {
  return others.reduce((acc, n) => acc + n, first);
}

const [head, ...tail]   = [1, 2, 3, 4];
const { a, b, ...rest } = { a:1, b:2, c:3, d:4 };

// ── SPREAD: expand iterables ──────────────────────────────
const arr2   = [...arr1, ...arr2];          // join arrays
const merged = { ...obj1, ...obj2 };        // merge objects (later wins)
const copy   = [...original];               // shallow copy array
Math.max(...numbers);                        // pass as args

// ⚠️ Spread is ALWAYS shallow!
const matrix  = [[1,2],[3,4]];
const shallow = [...matrix]; // outer array copied, inner arrays same refs!

// ── Convert anything iterable to array ────────────────────
[...new Set([1,1,2,2])];     // [1,2]
[...new Map([['a',1]])];     // [['a',1]]
[...document.querySelectorAll('li')]; // NodeList → array
[...'hello'];                // ['h','e','l','l','o']
[...new Range(1,5)];         // [1,2,3,4,5] (any iterable)
```

### 4.4 Short-circuit and Ternary

```js
// AND as guard
isLoggedIn && renderUserMenu();
user?.isAdmin && showAdminPanel();

// OR as default (prefer ?? for null-safety)
const name = inputName || 'Guest';

// Ternary — simple conditions only
const label = isActive ? 'Active' : 'Inactive';
const cls   = `btn ${isPrimary ? 'btn-primary' : 'btn-secondary'}`;

// ❌ Never nest ternaries — kills readability
// const x = a ? b ? 'x' : 'y' : c ? 'z' : 'w';

// ✅ Use if/else for complex conditions
function getStatusLabel(code) {
  if (code === 200) return 'OK';
  if (code === 404) return 'Not Found';
  if (code === 500) return 'Server Error';
  return `Unknown (${code})`;
}
```

---

## 5. Functions

### 5.1 Arrow vs Regular — Decision Table

| Scenario | Use | Reason |
|----------|-----|--------|
| Array callbacks | Arrow | Concise, no `this` needed |
| Promise `.then()` | Arrow | Concise |
| Class method | Regular | Needs `this` = instance |
| Object literal method | Regular | Needs `this` = object |
| Event handler needing `this` = element | Regular | Lexical `this` would capture wrong context |
| Class method needing `this` inside callback | Arrow | Captures `this` from class scope |
| Constructor | Class / Regular | Arrow cannot be `new`'d |
| Generator | Regular `function*` | Arrow cannot be generator |

```js
// ✅ Arrow — callbacks and closures
[1,2,3].map(x => x * 2);
fetch(url).then(r => r.json()).then(data => render(data));
const double = x => x * 2;
const returnObj = x => ({ key: x }); // ← parens required for object literal!

// ✅ Regular — object methods
const obj = {
  count: 0,
  increment() { this.count++; },      // ✅ this = obj
  // increment: () => this.count++,   // ❌ this = outer scope
};

// ✅ Arrow in class — captures `this`
class Timer {
  #elapsed = 0;
  start() {
    setInterval(() => this.#elapsed++, 1000); // ✅ this = Timer instance
    // setInterval(function() { this.#elapsed++ }, 1000); // ❌ this ≠ Timer
  }
}

// ✅ Regular for event handlers when element `this` needed
button.addEventListener('click', function() {
  this.classList.toggle('active'); // this = button ✅
});
// ❌ Arrow version: this ≠ button
```

### 5.2 Parameter Patterns

```js
// Defaults — evaluated fresh on each call
function connect(host, port = 5432, ssl = true) {}
// ⚠️ new Date() as default creates a new Date on every call — useful!
function log(msg, time = new Date()) {}

// Options object — best for 3+ params; easy to extend without breaking API
function initMap({
  container,                   // required
  zoom = 12,                   // optional with default
  center = [0, 0],             // array default
  theme = 'streets',
  interactive = true,
  onLoad = null,
} = {}) {}                    // ← {} allows calling initMap() with no args

initMap({ container: '#map', zoom: 14 }); // readable at call site

// Rest parameters — variadic functions
function log(level, ...messages) {
  console[level](...messages);
}
log('warn', 'Price is', price, '(high)');

// Avoid the `arguments` object — use rest instead
// ❌ function bad() { return Array.from(arguments).reduce(...) }
// ✅ function good(...args) { return args.reduce(...) }
```

### 5.3 Pure Functions and Composition

```js
// Pure: same input → same output, no side effects
const add      = (a, b) => a + b;
const clamp    = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
const slugify  = s => s.trim().toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
const formatUser = u => ({ ...u, fullName: `${u.firstName} ${u.lastName}` });

// Rules: A function is impure if it:
// • Reads/writes external state (DOM, global vars, files, db)
// • Has different output for same input (uses Math.random, Date.now)
// • Throws or causes observable side effects
// Impurity is OK at the edges of your app. Keep core logic pure.

// Pipe (left-to-right — most readable)
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);

// Compose (right-to-left — math convention)
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);

// Async pipe
const pipeAsync = (...fns) => x => fns.reduce((p, f) => p.then(f), Promise.resolve(x));

// Practical example
const processInput = pipe(
  s => s.trim(),
  s => s.toLowerCase(),
  s => s.replace(/\s+/g, '-'),
  s => s.replace(/[^\w-]/g, ''),
);
processInput('  Hello, World!  '); // 'hello-world'

// Async pipeline
const loadAndProcess = pipeAsync(
  userId => api.get(`/users/${userId}`),
  user   => enrichWithProfile(user),
  user   => { saveToStore(user); return user; },
);
```

### 5.4 Memoization

```js
// Basic Map memoization
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// LRU Cache memoization (bounded memory)
function memoizeLRU(fn, maxSize = 100) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      const val = cache.get(key);
      cache.delete(key);
      cache.set(key, val); // move to end (most-recent)
      return val;
    }
    const result = fn.apply(this, args);
    if (cache.size >= maxSize) cache.delete(cache.keys().next().value); // evict oldest
    cache.set(key, result);
    return result;
  };
}

// WeakMap memoization — object args, GC-friendly
function memoizeWeak(fn) {
  const cache = new WeakMap();
  return function(arg) {
    if (!cache.has(arg)) cache.set(arg, fn.call(this, arg));
    return cache.get(arg);
  };
}

// Async memoize with deduplication (prevents duplicate in-flight requests)
function memoizeAsync(fn) {
  const cache   = new Map();
  const pending = new Map();
  return async function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    if (pending.has(key)) return pending.get(key); // wait for same in-flight request
    const p = fn.apply(this, args).then(v => { cache.set(key, v); pending.delete(key); return v; });
    pending.set(key, p);
    return p;
  };
}
```

### 5.5 Partial Application and Curry

```js
// Partial application — fix some args
const partial = (fn, ...preset) => (...later) => fn(...preset, ...later);

const add     = (a, b, c) => a + b + c;
const add10   = partial(add, 10);
add10(5, 3);  // 18

const fetchUser = partial(fetch, '/api/users/');
// Later: fetchUser(userId) → GET /api/users/{userId}

// Curry — one arg at a time
const curry = fn => {
  const arity = fn.length;
  return function curried(...args) {
    return args.length >= arity
      ? fn(...args)
      : (...more) => curried(...args, ...more);
  };
};

const curriedAdd = curry((a, b, c) => a + b + c);
curriedAdd(1)(2)(3);  // 6
curriedAdd(1, 2)(3);  // 6
curriedAdd(1)(2, 3);  // 6

// Practical curry: event handler factory
const handleEvent = curry((handler, transform, event) =>
  handler(transform(event.target.value))
);
input.addEventListener('input', handleEvent(setSearch)(s => s.trim().toLowerCase()));
```

## 6. Classes and Prototypes

### 6.1 Full Modern Class Syntax

```js
class EventEmitter {
  // Private fields (ES2022) — true encapsulation, not just convention
  #listeners  = new Map();
  #maxListeners = 100;

  // Private static field
  static #instanceCount = 0;

  // Public static field
  static version = '3.0.0';

  constructor() {
    EventEmitter.#instanceCount++;
  }

  static getInstanceCount() { return EventEmitter.#instanceCount; }

  // Getter (computed on access)
  get listenerCount() {
    return [...this.#listeners.values()].reduce((n, s) => n + s.size, 0);
  }

  // Setter with validation
  set maxListeners(n) {
    if (!Number.isInteger(n) || n < 0) throw new TypeError('Positive integer required');
    this.#maxListeners = n;
  }

  on(event, fn) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, new Set());
    this.#listeners.get(event).add(fn);
    return this; // fluent API — enables chaining
  }

  off(event, fn) {
    this.#listeners.get(event)?.delete(fn);
    return this;
  }

  emit(event, ...args) {
    this.#listeners.get(event)?.forEach(fn => {
      try { fn(...args); } catch(e) { console.error(`Listener error [${event}]:`, e); }
    });
    return this;
  }

  once(event, fn) {
    const wrapper = (...a) => { fn(...a); this.off(event, wrapper); };
    return this.on(event, wrapper);
  }

  // Static block (ES2022) — complex static initialization
  static {
    EventEmitter.#instanceCount = 0; // reset (demonstrating static block)
  }
}
```

### 6.2 Inheritance

```js
class Component extends EventEmitter {
  #root;
  #mounted = false;
  #controller = new AbortController();

  constructor(selectorOrEl) {
    super(); // MUST be first!
    const el = typeof selectorOrEl === 'string'
      ? document.querySelector(selectorOrEl)
      : selectorOrEl;
    if (!el) throw new Error(`Component: element not found — ${selectorOrEl}`);
    this.#root = el;
  }

  get el()      { return this.#root; }
  get mounted() { return this.#mounted; }
  get signal()  { return this.#controller.signal; } // expose for event binding

  // "Abstract" method — subclasses MUST override
  render() { throw new Error(`${this.constructor.name}.render() not implemented`); }

  // Template method pattern
  mount() {
    this.#root.innerHTML = this.render();
    this.bindEvents();
    this.#mounted = true;
    this.emit('mount', this);
    return this;
  }

  bindEvents() {} // hook — subclasses override

  update() {
    if (!this.#mounted) return this;
    const scroll = this.#root.scrollTop;
    this.#root.innerHTML = this.render();
    this.bindEvents();
    this.#root.scrollTop = scroll;
    this.emit('update', this);
    return this;
  }

  destroy() {
    this.#controller.abort(); // remove all listeners bound via signal
    this.#root.innerHTML = '';
    this.#mounted = false;
    this.emit('destroy', this);
  }
}

// Concrete subclass
class TodoList extends Component {
  #items = [];

  constructor(sel, items = []) {
    super(sel);
    this.#items = items;
  }

  render() {
    return `
      <ul class="todo-list">
        ${this.#items.map((item, i) => `
          <li class="todo-item ${item.done ? 'done' : ''}">
            <button data-action="toggle" data-index="${i}">
              ${item.done ? '✅' : '⬜'}
            </button>
            <span>${escapeHtml(item.text)}</span>
            <button data-action="delete" data-index="${i}">✕</button>
          </li>
        `).join('')}
      </ul>
    `;
  }

  bindEvents() {
    this.el.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      const i = Number(btn.dataset.index);
      if (btn.dataset.action === 'toggle') {
        this.#items[i].done = !this.#items[i].done;
        this.update();
      }
      if (btn.dataset.action === 'delete') {
        this.#items.splice(i, 1);
        this.update();
        this.emit('delete', this.#items[i]);
      }
    }, { signal: this.signal });
  }
}
```

### 6.3 Mixins — Composing Behaviors

```js
// Mixins: add behavior to any class without full inheritance
const Serializable = Base => class extends Base {
  toJSON() {
    return JSON.stringify(
      Object.fromEntries(
        Object.entries(this).filter(([, v]) => typeof v !== 'function')
      )
    );
  }
  static fromJSON(json) {
    return Object.assign(new this(), JSON.parse(json));
  }
};

const Timestamped = Base => class extends Base {
  constructor(...args) {
    super(...args);
    this.createdAt = new Date().toISOString();
  }
  touch() { this.updatedAt = new Date().toISOString(); return this; }
};

const Validatable = Base => class extends Base {
  validate() {
    const schema = this.constructor.schema ?? {};
    const errors = Object.entries(schema)
      .filter(([field, rule]) => !rule(this[field]))
      .map(([field]) => field);
    return { valid: errors.length === 0, errors };
  }
};

const Observable = Base => class extends Base {
  #subs = new Map();
  subscribe(key, fn) {
    if (!this.#subs.has(key)) this.#subs.set(key, new Set());
    this.#subs.get(key).add(fn);
    return () => this.#subs.get(key).delete(fn);
  }
  notify(key, ...args) {
    this.#subs.get(key)?.forEach(fn => fn(...args));
  }
};

// Compose multiple behaviors
class UserModel extends Serializable(Timestamped(Validatable(Observable(EventEmitter)))) {
  static schema = {
    name:  v => typeof v === 'string' && v.trim().length >= 2,
    email: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v),
    age:   v => Number.isInteger(v) && v >= 0 && v <= 150,
  };

  constructor({ name, email, age }) {
    super();
    Object.assign(this, { name, email, age });
  }
}

const user = new UserModel({ name: 'Alice', email: 'a@b.com', age: 30 });
user.validate(); // { valid: true, errors: [] }
user.toJSON();   // serialized
user.touch();    // sets updatedAt
```

---

## 7. Async Programming

### 7.1 Promises — Deep Understanding

```js
// Promise states: pending → fulfilled | rejected (immutable once settled)
// Promises cannot be cancelled — use AbortController for that

// Creating
const p = new Promise((resolve, reject) => {
  // resolve(value) — fulfil with value
  // reject(reason) — reject with reason (should be Error instance)
  setTimeout(() => resolve('data'), 1000);
});

// ── Chaining — each .then() returns a NEW promise ─────────
fetch('/api/users')
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return res.json();            // returning a promise = chaining into it
  })
  .then(users => users.filter(u => u.active))
  .then(active => renderList(active))
  .catch(err   => handleError(err))   // catches ALL rejections above
  .finally(()  => hideSpinner());     // always runs

// ── Combinators ───────────────────────────────────────────

// Promise.all — all must succeed. Fails fast on first rejection.
const [users, posts, config] = await Promise.all([
  api.get('/users'), api.get('/posts'), api.get('/config'),
]);

// Promise.allSettled — wait for all, never rejects (ES2020)
const results = await Promise.allSettled([fetch('/a'), fetch('/b'), fetch('/c')]);
results.forEach(r => {
  if (r.status === 'fulfilled') process(r.value);
  else                          console.warn('Failed:', r.reason);
});

// Promise.race — first SETTLED (fulfilled or rejected)
const data = await Promise.race([
  fetchData(),
  new Promise((_, rej) => setTimeout(() => rej(new Error('Timeout')), 5000)),
]);

// Promise.any — first FULFILLED. Rejects only if ALL reject (ES2021)
const fastest = await Promise.any([fetchUS(), fetchEU(), fetchAsia()]);
// If all fail: throws AggregateError with all reasons

// Promise.withResolvers — expose resolve/reject (ES2024)
const { promise, resolve, reject } = Promise.withResolvers();
socket.on('message', resolve);
socket.on('error', reject);
const message = await promise;
```

### 7.2 async/await — Correct Patterns

```js
// ✅ Error handling with try/catch/finally
async function loadDashboard(userId) {
  showSpinner();
  try {
    // ✅ PARALLEL — both requests fire simultaneously (300ms total)
    const [user, posts] = await Promise.all([
      loadUser(userId),
      loadPosts(userId),
    ]);

    // ❌ SEQUENTIAL — unnecessary (600ms total!)
    // const user  = await loadUser(userId);   // 300ms
    // const posts = await loadPosts(userId);  // 300ms

    render({ user, posts });
  } catch (err) {
    if (err.name === 'AbortError') return; // cancelled — not an error
    showError(err.message);
    reportToSentry(err);
  } finally {
    hideSpinner(); // always runs
  }
}

// ✅ Retry with exponential backoff
async function withRetry(fn, { attempts = 3, delay = 500, factor = 2 } = {}) {
  for (let i = 0; i <= attempts; i++) {
    try { return await fn(); }
    catch (err) {
      const isLast    = i === attempts;
      const isCancelled = err.name === 'AbortError';
      const isClient  = err.status >= 400 && err.status < 500 && err.status !== 429;
      if (isLast || isCancelled || isClient) throw err;
      await new Promise(r => setTimeout(r, delay * factor**i + Math.random()*300));
    }
  }
}

// ✅ Top-level await (in ES Modules)
// <script type="module"> or .mjs file
const config = await fetch('/config.json').then(r => r.json());
const token  = await authService.getToken();
initApp({ config, token });

// ✅ Handling multiple independent failures
async function loadPage(id) {
  const [userResult, statsResult, feedResult] = await Promise.allSettled([
    loadUser(id), loadStats(id), loadFeed(id),
  ]);

  const user  = userResult.status  === 'fulfilled' ? userResult.value  : null;
  const stats = statsResult.status === 'fulfilled' ? statsResult.value : defaultStats;
  const feed  = feedResult.status  === 'fulfilled' ? feedResult.value  : [];

  render({ user, stats, feed });
  if (userResult.status === 'rejected') showPartialError('User data unavailable');
}
```

### 7.3 AbortController — Cancellation

```js
// Timeout via AbortSignal (ES2022) — no manual cleanup needed!
const response = await fetch(url, {
  signal: AbortSignal.timeout(5000), // auto-cancel after 5s
});

// Combine multiple signals (ES2024)
const userCancel = new AbortController();
const combined   = AbortSignal.any([
  userCancel.signal,
  AbortSignal.timeout(10_000),
]);
await fetch(url, { signal: combined });

// Cancel previous search on new input
class SearchService {
  #controller = null;

  async search(query) {
    this.#controller?.abort('New search started'); // cancel previous
    this.#controller = new AbortController();

    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
        signal: this.#controller.signal,
      });
      return res.json();
    } catch (err) {
      if (err.name === 'AbortError') return null; // cancelled — not an error
      throw err;
    }
  }
}

// Bulk listener cleanup via AbortController
function setupListeners(element) {
  const controller = new AbortController();
  const { signal } = controller;

  element.addEventListener('click',     handleClick,  { signal });
  element.addEventListener('mouseover', handleHover,  { signal });
  document.addEventListener('keydown',  handleKey,    { signal });
  window.addEventListener('resize',     handleResize, { signal, passive: true });

  return () => controller.abort(); // removes ALL four at once
}

const cleanup = setupListeners(el);
// Later...
cleanup(); // removes all listeners
```

### 7.4 Async Generators and Streams

```js
// Async generator — lazy, pull-based data streams
async function* paginate(fetchPage) {
  let page = 1;
  while (true) {
    const { data, hasMore } = await fetchPage(page++);
    yield* data;
    if (!hasMore) return;
  }
}

for await (const item of paginate(p => api.get('/items', { params: { page: p } }))) {
  renderItem(item);
}

// Read HTTP response line by line
async function* readLines(response) {
  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buf = '';
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) { if (buf.trim()) yield buf; return; }
      buf += value;
      const lines = buf.split('\n');
      buf = lines.pop() ?? '';
      yield* lines.filter(Boolean);
    }
  } finally {
    reader.releaseLock();
  }
}

// Server-Sent Events as async iterator
async function* sseStream(url) {
  const res = await fetch(url);
  for await (const line of readLines(res)) {
    if (line.startsWith('data: ')) {
      try { yield JSON.parse(line.slice(6)); }
      catch { yield line.slice(6); }
    }
  }
}

for await (const event of sseStream('/api/events')) {
  handleEvent(event);
}
```

---

## 8. ES Modules System

### 8.1 Export / Import Syntax

```js
// ═══ math.js ═══
export const PI  = 3.14159265;
export const TAU = PI * 2;
export function add(a, b)     { return a + b; }
export function multiply(a, b){ return a * b; }
export class Vector { /*...*/ }

// Default export — one per module
export default class Calculator { /*...*/ }

// Re-exports
export { add as sum }           from './math.js';   // re-export with rename
export * as mathUtils           from './math.js';   // namespace re-export
export { default as Chart }     from './chart.js';  // re-export default as named
export *                        from './utils.js';  // re-export all named

// ═══ main.js ═══
import Calculator, { PI, add, multiply } from './math.js'; // default + named
import { add as sum }                    from './math.js'; // rename
import * as MathLib                      from './math.js'; // namespace
import './polyfills.js';                                   // side-effects only
```

### 8.2 Dynamic Imports

```js
// Code splitting — load only when needed
button.addEventListener('click', async () => {
  const { openModal } = await import('./modal.js');
  openModal({ title: 'Settings' });
}, { once: true });

// Conditional loading
const utils = await import(
  isDevelopment ? './utils-dev.js' : './utils-prod.js'
);

// Parallel lazy loading
const [{ default: Chart }, { default: DataTable }] = await Promise.all([
  import('./chart.js'),
  import('./data-table.js'),
]);

// With error handling
async function tryImport(modulePath) {
  try   { return await import(modulePath); }
  catch { console.warn(`Module not found: ${modulePath}`); return null; }
}

// Route-based code splitting
const routes = {
  '/':       () => import('./pages/Home.js'),
  '/about':  () => import('./pages/About.js'),
  '/users':  () => import('./pages/Users.js'),
};
const { default: PageComponent } = await routes[pathname]?.() ?? routes['/']();
```

### 8.3 Import Maps (No Bundler Required)

```html
<!-- Place BEFORE any module scripts -->
<script type="importmap">
{
  "imports": {
    "lodash-es":    "https://cdn.jsdelivr.net/npm/lodash-es@4/lodash.js",
    "lodash-es/":   "https://cdn.jsdelivr.net/npm/lodash-es@4/",
    "chart.js":     "https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js",
    "utils":        "./src/utils/index.js",
    "components/":  "./src/components/"
  }
}
</script>

<script type="module">
  import debounce  from 'lodash-es/debounce.js';
  import { Chart } from 'chart.js';
  import { Button } from 'components/Button.js';
  import { formatDate } from 'utils';
</script>
```

### 8.4 Module Patterns

```js
// ── Barrel file (index.js) ────────────────────────────────
// Expose clean public API, hide internal implementation details
export { UserService }  from './UserService.js';
export { PostService }  from './PostService.js';
export { formatDate, formatCurrency } from './formatters.js';
// Do NOT re-export internal helpers — keep them private

// ── Singleton via module ──────────────────────────────────
// Modules execute once — subsequent imports get the same export
let db = null;
export function getDatabase() {
  return (db ??= new Database(process.env.DB_URL));
}

// ── Module-level initialization ───────────────────────────
// Runs once when first imported — useful for setup
const theme = localStorage.getItem('theme') ?? 'light';
document.documentElement.dataset.theme = theme;
export { theme };

// ── Type="module" script properties ──────────────────────
// <script type="module" src="./main.js"></script>
// Automatic: defer, strict mode, own scope, CORS for cross-origin
// Import.meta.url — URL of current module
// Import.meta.env — build-time environment variables (Vite/Rollup)
console.log(import.meta.url); // 'https://example.com/src/main.js'
```

---

## 9. DOM API — Modern Approach

### 9.1 Querying Elements

```js
// ── Selectors ─────────────────────────────────────────────
document.querySelector('.card');            // first match — static
document.querySelectorAll('.item');         // all — static NodeList
document.getElementById('app');            // fastest single lookup
document.getElementsByTagName('div');      // live HTMLCollection!
document.getElementsByClassName('btn');    // live HTMLCollection!

// NodeList vs HTMLCollection
// NodeList:       static (querySelectorAll), forEach + for...of works
// HTMLCollection: live (updates when DOM changes), only for...of
// ✅ Always convert to array for full array methods:
const items = [...document.querySelectorAll('.item')];
const items2 = Array.from(document.querySelectorAll('.item'));

// ── Scoped queries — search within an element ─────────────
const form   = document.querySelector('#login-form');
const inputs = form.querySelectorAll('input');         // only within form
const submit = form.querySelector('button[type="submit"]');

// ── Tree traversal ────────────────────────────────────────
el.parentElement;          // direct parent
el.children;               // live HTMLCollection of element children
el.firstElementChild;
el.lastElementChild;
el.nextElementSibling;
el.previousElementSibling;
el.childElementCount;

// ── closest() — walk UP the DOM tree ─────────────────────
// Starts at `el` itself, walks up until selector matches or null
const listItem   = btn.closest('li');
const modal      = btn.closest('[role="dialog"]');
const component  = el.closest('[data-component]');
const form2      = input.closest('form');

// ── matches() — test current element ─────────────────────
el.matches('.active:not([disabled])');
el.matches(':focus-within');
el.matches('[data-loaded]');
el.matches('input[type="email"]');
```

### 9.2 Creating and Inserting Elements

```js
// ── Safe element creation ─────────────────────────────────
// textContent NEVER causes XSS — always prefer over innerHTML for text
const li = document.createElement('li');
li.textContent  = item.name;    // ✅ XSS-safe
li.dataset.id   = item.id;      // → data-id attribute
li.dataset.type = item.type;    // → data-type attribute
li.className    = 'list-item active';
li.id           = `item-${item.id}`;
li.setAttribute('aria-label', `Item: ${item.name}`);

// ── Fluent element builder ────────────────────────────────
class El {
  #el;
  constructor(tag)             { this.#el = document.createElement(tag); }
  static div   = () => new El('div');
  static span  = () => new El('span');
  static button= () => new El('button');
  static ul    = () => new El('ul');
  static li    = () => new El('li');
  static input = () => new El('input');

  text(t)          { this.#el.textContent = t; return this; }
  cls(...c)        { this.#el.classList.add(...c.filter(Boolean)); return this; }
  attr(k,v)        { this.#el.setAttribute(k, v); return this; }
  data(k,v)        { this.#el.dataset[k] = v; return this; }
  on(e,fn,opts)    { this.#el.addEventListener(e, fn, opts); return this; }
  prop(k,v)        { this.#el[k] = v; return this; }
  style(s)         { Object.assign(this.#el.style, s); return this; }
  when(cond,fn)    { if(cond) fn(this); return this; }
  append(...ch)    { ch.forEach(c => this.#el.append(c instanceof El ? c.build() : c)); return this; }
  build()          { return this.#el; }
}

// Usage
const card = El.div().cls('card')
  .append(
    El.div().cls('card__title').text(user.name),
    El.button().cls('btn','btn--primary').text('View')
      .attr('aria-label', `View ${user.name}'s profile`)
      .on('click', () => navigate(`/users/${user.id}`))
  )
  .build();

// ── DocumentFragment — batch insert (ONE reflow) ──────────
const frag = document.createDocumentFragment();
data.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name;
  li.dataset.id  = item.id;
  frag.append(li);
});
list.append(frag); // single DOM update

// ── Modern insertion API ──────────────────────────────────
parent.append(child);          // insert at end (string or Node)
parent.prepend(child);         // insert at start
el.before(newEl);              // insert before `el`
el.after(newEl);               // insert after `el`
el.replaceWith(newEl);         // replace `el` with `newEl`
el.remove();                   // remove from DOM

// insertAdjacentHTML — fastest for HTML strings (parsed once)
el.insertAdjacentHTML('beforebegin', html); // before element
el.insertAdjacentHTML('afterbegin',  html); // first child
el.insertAdjacentHTML('beforeend',   html); // last child
el.insertAdjacentHTML('afterend',    html); // after element
```

### 9.3 Classes, Attributes and Styles

```js
// ── classList — always preferred over .className ──────────
el.classList.add('active', 'highlighted');
el.classList.remove('loading', 'error');
el.classList.toggle('open');
el.classList.toggle('visible', condition);  // conditional
el.classList.replace('old-name', 'new-name');
el.classList.contains('active');            // boolean
[...el.classList];                           // to array
el.classList.toString();                     // space-separated string

// ── Attributes ────────────────────────────────────────────
el.setAttribute('aria-expanded', 'true');
el.getAttribute('data-user-id');
el.removeAttribute('hidden');
el.hasAttribute('disabled');               // boolean
el.toggleAttribute('disabled');            // toggle presence
el.toggleAttribute('aria-pressed', isOn);  // conditional presence

// ── dataset (data-* attributes) ──────────────────────────
el.dataset.userId  = '42';    // → data-user-id="42" (camelCase → kebab)
el.dataset.userId;             // '42' (always string!)
delete el.dataset.userId;      // removes data-user-id
'userId' in el.dataset;        // check existence

// ── CSS Custom Properties ─────────────────────────────────
// Set on element
el.style.setProperty('--item-color', '#ff0000');
// Set globally
document.documentElement.style.setProperty('--primary', '#3b82f6');
document.documentElement.style.setProperty('--spacing', '8px');
// Read computed value
getComputedStyle(el).getPropertyValue('--primary').trim();
// Remove
el.style.removeProperty('--item-color');

// ✅ Prefer class toggles over inline styles for state
// Only use inline styles for truly dynamic numeric values:
el.style.transform = `translateX(${offsetX}px) translateY(${offsetY}px)`;
el.style.setProperty('--progress', `${percent}%`);
el.style.setProperty('--rotation', `${degrees}deg`);
```

### 9.4 Forms

```js
// FormData — modern form handling
const form = document.querySelector('#checkout-form');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const data = new FormData(form);

  // Read values
  data.get('email');         // string (first match)
  data.getAll('colors[]');   // array (for multi-select)
  data.has('newsletter');    // boolean
  [...data.entries()];       // all [key, value] pairs

  // Convert to plain object
  const obj = Object.fromEntries(data);

  // Send as JSON
  await fetch('/api/checkout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(obj),
  });

  // Or send as multipart (for file uploads)
  await fetch('/api/checkout', { method: 'POST', body: data });
});

// HTML5 constraint validation API
const emailInput = form.querySelector('input[name="email"]');
emailInput.validity.valid;          // boolean — all constraints pass
emailInput.validity.valueMissing;   // true if required + empty
emailInput.validity.typeMismatch;   // true if email format wrong
emailInput.validity.patternMismatch;// true if pattern attr fails
emailInput.validity.tooShort;       // true if minlength violated
emailInput.validity.tooLong;        // true if maxlength violated
emailInput.validationMessage;       // browser's message string

emailInput.setCustomValidity('Username already taken'); // set error
emailInput.setCustomValidity('');                        // clear error

form.checkValidity();   // boolean — validate silently
form.reportValidity();  // validate + show browser UI
```

---

## 10. Events and Delegation

### 10.1 addEventListener — Full Options

```js
// Third argument: boolean (capture) OR options object (modern)
element.addEventListener(type, handler, {
  capture: false,      // handle in capture phase (true) vs bubble (false, default)
  once:    true,       // auto-remove after first fire
  passive: true,       // promise not to call preventDefault (perf for scroll/touch)
  signal:  controller.signal, // AbortSignal — removes listener when aborted
});

// ✅ AbortController — bulk cleanup (best pattern)
function initFeature(container) {
  const controller = new AbortController();
  const { signal } = controller;

  container.addEventListener('click',     onClick,    { signal });
  container.addEventListener('mouseover', onHover,    { signal });
  document.addEventListener('keydown',    onKeydown,  { signal });
  window.addEventListener('scroll',       onScroll,   { signal, passive: true });
  window.addEventListener('resize',       onResize,   { signal });

  return () => controller.abort(); // removes ALL at once
}
const cleanup = initFeature(el);
// When component unmounts:
cleanup();

// removeEventListener requires EXACT SAME function reference
const handler = () => doSomething();
el.addEventListener('click', handler);
el.removeEventListener('click', handler); // same reference ✅
// Arrow functions inline cannot be removed — always store reference!
```

### 10.2 Event Propagation

```js
// Phases: capture ↓ → target → bubble ↑
// stopPropagation() — stop propagating in current direction
// stopImmediatePropagation() — stop + prevent other listeners on same element
// preventDefault() — prevent default browser behavior (submit, link nav, etc.)

// Example: custom dropdown that closes on outside click
function createDropdown(trigger, menu) {
  let open = false;
  const controller = new AbortController();
  const { signal } = controller;

  trigger.addEventListener('click', (e) => {
    e.stopPropagation(); // prevent document handler from firing immediately
    open = !open;
    menu.hidden = !open;
  }, { signal });

  document.addEventListener('click', () => {
    if (open) { open = false; menu.hidden = true; }
  }, { signal });

  return { destroy: () => controller.abort() };
}
```

### 10.3 Event Delegation

```js
// ❌ Individual listeners — misses dynamically added elements
document.querySelectorAll('.btn').forEach(btn =>
  btn.addEventListener('click', handleClick)
);

// ✅ Delegation — one listener on ancestor, handles current + future elements
list.addEventListener('click', (event) => {
  // Walk UP from click target to find the matching element
  const btn    = event.target.closest('[data-action]');
  const item   = event.target.closest('[data-id]');

  if (!btn || !item) return; // click outside any action button

  const { action } = btn.dataset;
  const { id }     = item.dataset;

  const actions = {
    delete:  () => deleteItem(id),
    edit:    () => editItem(id),
    toggle:  () => toggleItem(id),
    preview: () => previewItem(id),
  };
  actions[action]?.();
});

// ── Generic delegate utility ──────────────────────────────
function delegate(parent, selector, eventType, handler, options = {}) {
  parent.addEventListener(eventType, (event) => {
    const target = event.target.closest(selector);
    if (target && parent.contains(target)) {
      handler.call(target, event, target);
    }
  }, options);
  // Note: cannot be easily removed — use AbortController pattern instead
}

delegate(document.body, '[data-confirm]', 'click', (e, btn) => {
  if (!window.confirm(btn.dataset.confirm)) e.preventDefault();
});
```

### 10.4 Custom Events

```js
// Creating and dispatching custom events
function dispatch(element, name, detail = {}, options = {}) {
  element.dispatchEvent(new CustomEvent(name, {
    detail,
    bubbles:    options.bubbles    ?? true,  // bubbles up DOM tree
    cancelable: options.cancelable ?? true,  // can be preventDefault()
    composed:   options.composed   ?? true,  // crosses shadow DOM boundary
  }));
}

// Dispatch events
dispatch(form, 'form:submit',  { data: formData });
dispatch(cart, 'cart:update',  { total, itemCount });
dispatch(modal, 'modal:close', { reason: 'escape-key' });

// Listen — works like any DOM event
document.addEventListener('cart:update', ({ detail }) => {
  cartBadge.textContent = detail.itemCount;
  cartTotal.textContent = formatCurrency(detail.total);
});

// ── Global event bus via document ─────────────────────────
const bus = {
  on:   (name, fn, opts) => document.addEventListener(name, fn, opts),
  off:  (name, fn)       => document.removeEventListener(name, fn),
  once: (name, fn)       => document.addEventListener(name, fn, { once: true }),
  emit: (name, detail)   => dispatch(document, name, detail, { bubbles: false }),
};

bus.on('user:login',    ({ detail }) => showWelcome(detail.user));
bus.on('user:logout',   ()          => clearSession());
bus.emit('user:login',  { user: currentUser });
```

### 10.5 Debounce and Throttle

```js
// Debounce — execute after N ms of quiet (good for: search, resize, scroll-end)
function debounce(fn, delay, { leading = false } = {}) {
  let timer;
  return function(...args) {
    const callNow = leading && !timer;
    clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      if (!leading) fn.apply(this, args);
    }, delay);
    if (callNow) fn.apply(this, args);
  };
}

// Throttle — execute at most once per N ms (good for: scroll, mousemove, buttons)
function throttle(fn, limit, { trailing = true } = {}) {
  let last = 0, timer = null;
  return function(...args) {
    const now = Date.now();
    const remaining = limit - (now - last);
    if (remaining <= 0) {
      clearTimeout(timer); timer = null;
      last = now;
      fn.apply(this, args);
    } else if (!timer && trailing) {
      timer = setTimeout(() => {
        last = Date.now(); timer = null;
        fn.apply(this, args);
      }, remaining);
    }
  };
}

// Usage
searchInput.addEventListener('input', debounce(performSearch, 300));
window.addEventListener('scroll',     throttle(updateHeader, 100), { passive: true });
window.addEventListener('resize',     debounce(recalcLayout, 200));
saveBtn.addEventListener('click',     throttle(save, 2000)); // prevent double-save
```

## 11. Fetch API and Networking

### 11.1 HTTP Client

```js
class HttpClient {
  #base; #headers; #interceptors;

  constructor(baseURL, options = {}) {
    this.#base = baseURL.replace(/\/$/, '');
    this.#headers = { 'Content-Type': 'application/json', ...options.headers };
    this.#interceptors = {
      request:  options.onRequest  ?? (c => c),
      response: options.onResponse ?? (r => r),
      error:    options.onError    ?? null,
    };
  }

  async #request(method, path, { body, params, headers = {}, signal, raw = false } = {}) {
    const url = new URL(this.#base + path);
    if (params) {
      Object.entries(params).forEach(([k, v]) => {
        if (v != null) url.searchParams.set(k, String(v));
      });
    }

    const config = await this.#interceptors.request({
      method,
      headers: { ...this.#headers, ...headers },
      body:    body != null ? JSON.stringify(body) : undefined,
      signal,
    });

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const err = new HttpError(response.status, response.statusText, response);
        if (this.#interceptors.error) return this.#interceptors.error(err);
        throw err;
      }

      if (raw) return this.#interceptors.response(response);

      const ct = response.headers.get('Content-Type') ?? '';
      const data = ct.includes('application/json')
        ? await response.json()
        : await response.text();
      return this.#interceptors.response(data);

    } catch (err) {
      if (err instanceof HttpError) throw err;
      throw new NetworkError(`${method} ${path}: ${err.message}`, { cause: err });
    }
  }

  get(path, opts)    { return this.#request('GET',    path, opts); }
  post(path, opts)   { return this.#request('POST',   path, opts); }
  put(path, opts)    { return this.#request('PUT',    path, opts); }
  patch(path, opts)  { return this.#request('PATCH',  path, opts); }
  delete(path, opts) { return this.#request('DELETE', path, opts); }
}

class HttpError extends Error {
  constructor(status, statusText, response) {
    super(`HTTP ${status}: ${statusText}`);
    this.name = 'HttpError'; this.status = status; this.response = response;
  }
}
class NetworkError extends Error {
  constructor(msg, opts) { super(msg, opts); this.name = 'NetworkError'; }
}

// Usage
const api = new HttpClient('https://api.example.com', {
  headers: { Authorization: `Bearer ${getToken()}` },
  onRequest: config => { trackRequest(config); return config; },
  onError: async err => {
    if (err.status === 401) { await refreshToken(); throw err; }
    if (err.status === 429) { await sleep(retryAfter(err.response)); throw err; }
    throw err;
  },
});

const users = await api.get('/users', { params: { page: 1, limit: 20, role: 'admin' } });
const user  = await api.post('/users', { body: { name, email } });
```

### 11.2 Retry, Timeout and Deduplication

```js
// Retry with exponential backoff + jitter
async function withRetry(fn, { retries = 3, delay = 500, factor = 2 } = {}) {
  for (let i = 0; i <= retries; i++) {
    try { return await fn(); }
    catch (err) {
      if (i === retries) throw err;
      if (err.name === 'AbortError') throw err;
      if (err instanceof HttpError && err.status < 500 && err.status !== 429) throw err;
      const wait = delay * factor**i + Math.random() * 300; // jitter
      await new Promise(r => setTimeout(r, wait));
    }
  }
}

// Timeout via AbortSignal (ES2022)
const response = await fetch(url, { signal: AbortSignal.timeout(5000) });

// Request deduplication + TTL cache
class ApiCache {
  #cache   = new Map(); // key → { data, ts }
  #pending = new Map(); // key → Promise (in-flight)

  async get(key, fetcher, ttlMs = 60_000) {
    const hit = this.#cache.get(key);
    if (hit && Date.now() - hit.ts < ttlMs) return hit.data;

    // Deduplicate: if same key is already being fetched, wait for it
    if (this.#pending.has(key)) return this.#pending.get(key);

    const promise = fetcher()
      .then(data => { this.#cache.set(key, { data, ts: Date.now() }); return data; })
      .finally(()  => this.#pending.delete(key));

    this.#pending.set(key, promise);
    return promise;
  }

  invalidate(key)     { this.#cache.delete(key); }
  invalidateAll()     { this.#cache.clear(); }
  has(key, ttlMs = 0) {
    const c = this.#cache.get(key);
    return !!c && (ttlMs === 0 || Date.now() - c.ts < ttlMs);
  }
}

const cache = new ApiCache();
// Three simultaneous calls → ONE actual fetch
const [a, b, c] = await Promise.all([
  cache.get('users', () => api.get('/users')),
  cache.get('users', () => api.get('/users')), // deduplicated ✅
  cache.get('users', () => api.get('/users')), // deduplicated ✅
]);
```

### 11.3 Request Batching

```js
// Combine multiple individual requests into one batch request
class RequestBatcher {
  #queue = []; #timer = null;

  constructor(batchExecutor, { delay = 10 } = {}) {
    this.#executor = batchExecutor;
    this.#delay = delay;
  }

  request(key, params = {}) {
    return new Promise((resolve, reject) => {
      this.#queue.push({ key, params, resolve, reject });
      clearTimeout(this.#timer);
      this.#timer = setTimeout(() => this.#flush(), this.#delay);
    });
  }

  async #flush() {
    const batch = [...this.#queue];
    this.#queue = [];
    try {
      const results = await this.#executor(batch);
      batch.forEach(({ key, resolve, reject }) => {
        key in results ? resolve(results[key]) : reject(new Error(`No result for ${key}`));
      });
    } catch (err) {
      batch.forEach(({ reject }) => reject(err));
    }
  }
}

// Example: batch user fetches (50 individual calls → 1 batch request)
const userBatcher = new RequestBatcher(async (requests) => {
  const ids   = requests.map(r => r.params.id);
  const users = await api.get('/users/batch', { params: { ids: ids.join(',') } });
  return Object.fromEntries(users.map(u => [u.id, u]));
});

const [u1, u2, u3] = await Promise.all([
  userBatcher.request('user', { id: 1 }),
  userBatcher.request('user', { id: 2 }), // batched with above ✅
  userBatcher.request('user', { id: 3 }), // batched with above ✅
]);
```

---

## 12. Browser Storage

### 12.1 localStorage / sessionStorage with TTL

```js
class Storage {
  #store; #prefix;

  constructor(type = 'local', prefix = 'app:') {
    this.#store  = type === 'session' ? sessionStorage : localStorage;
    this.#prefix = prefix;
  }

  #key(k) { return this.#prefix + k; }

  set(key, value, ttlMs = null) {
    try {
      this.#store.setItem(this.#key(key), JSON.stringify({
        v: value,
        ...(ttlMs ? { exp: Date.now() + ttlMs } : {}),
      }));
      return true;
    } catch { return false; } // QuotaExceededError
  }

  get(key, fallback = null) {
    try {
      const raw = this.#store.getItem(this.#key(key));
      if (!raw) return fallback;
      const { v, exp } = JSON.parse(raw);
      if (exp && Date.now() > exp) { this.remove(key); return fallback; }
      return v;
    } catch { return fallback; }
  }

  remove(key) { this.#store.removeItem(this.#key(key)); }

  clear(subPrefix = '') {
    const full = this.#prefix + subPrefix;
    const keysToRemove = [];
    for (let i = 0; i < this.#store.length; i++) {
      const k = this.#store.key(i);
      if (k?.startsWith(full)) keysToRemove.push(k);
    }
    keysToRemove.forEach(k => this.#store.removeItem(k));
  }

  // Listen for changes from OTHER tabs (same-origin)
  static onExternalChange(callback) {
    window.addEventListener('storage', ({ key, oldValue, newValue, url }) => {
      const parse = s => { try { return JSON.parse(s ?? 'null')?.v ?? null; } catch { return null; } };
      callback({ key, old: parse(oldValue), new: parse(newValue), fromUrl: url });
    });
  }
}

const store = new Storage('local', 'myapp:');
store.set('session', { userId: 1, role: 'admin' }, 30 * 60_000); // 30 min TTL
store.get('session');  // { userId: 1, role: 'admin' } or null if expired
```

### 12.2 IndexedDB — Async Storage

```js
class IDB {
  #db = null;
  #name; #version; #schema;

  constructor(name, version, schema) {
    this.#name = name; this.#version = version; this.#schema = schema;
  }

  async open() {
    if (this.#db) return this;
    this.#db = await new Promise((resolve, reject) => {
      const req = indexedDB.open(this.#name, this.#version);
      req.onupgradeneeded = ({ target: { result: db }, oldVersion }) => {
        this.#schema.forEach(({ name, keyPath, autoIncrement = false, indexes = [] }) => {
          if (!db.objectStoreNames.contains(name)) {
            const store = db.createObjectStore(name, { keyPath, autoIncrement });
            indexes.forEach(({ name: n, keyPath: kp, unique = false, multiEntry = false }) => {
              store.createIndex(n, kp, { unique, multiEntry });
            });
          }
        });
      };
      req.onsuccess = e => resolve(e.target.result);
      req.onerror   = e => reject(e.target.error);
    });
    return this;
  }

  #promisify(request) {
    return new Promise((res, rej) => {
      request.onsuccess = e => res(e.target.result);
      request.onerror   = e => rej(e.target.error);
    });
  }

  #store(name, mode = 'readonly') {
    return this.#db.transaction(name, mode).objectStore(name);
  }

  get(store, key)           { return this.#promisify(this.#store(store).get(key)); }
  getAll(store, query, n)   { return this.#promisify(this.#store(store).getAll(query, n)); }
  count(store, query)       { return this.#promisify(this.#store(store).count(query)); }
  put(store, value)         { return this.#promisify(this.#store(store, 'readwrite').put(value)); }
  delete(store, key)        { return this.#promisify(this.#store(store, 'readwrite').delete(key)); }
  clear(store)              { return this.#promisify(this.#store(store, 'readwrite').clear()); }

  getByIndex(store, index, value) {
    return this.#promisify(this.#store(store).index(index).get(value));
  }
  getAllByIndex(store, index, value) {
    return this.#promisify(this.#store(store).index(index).getAll(value));
  }

  async transaction(stores, fn) {
    const tx = this.#db.transaction(stores, 'readwrite');
    const storeMap = Object.fromEntries(stores.map(s => [s, tx.objectStore(s)]));
    const result = fn(storeMap);
    await new Promise((res, rej) => { tx.oncomplete = res; tx.onerror = rej; });
    return result;
  }
}

const db = new IDB('myapp', 2, [
  {
    name: 'users', keyPath: 'id', autoIncrement: true,
    indexes: [
      { name: 'email', keyPath: 'email', unique: true },
      { name: 'role',  keyPath: 'role',  unique: false },
    ],
  },
  { name: 'posts',  keyPath: 'id' },
  { name: 'drafts', keyPath: 'id', autoIncrement: true },
]);

await db.open();
const id   = await db.put('users', { email: 'alice@example.com', name: 'Alice', role: 'admin' });
const user = await db.getByIndex('users', 'email', 'alice@example.com');
const admins = await db.getAllByIndex('users', 'role', 'admin');
```

---

## 13. State Management

### 13.1 Reactive Proxy Store

```js
class Store {
  #state; #subs = new Map(); #history = []; #maxHistory = 50;

  constructor(initialState) {
    this.#state = this.#makeReactive({ ...initialState });
  }

  #makeReactive(obj) {
    return new Proxy(obj, {
      get: (target, key) => {
        const val = target[key];
        return val && typeof val === 'object' && !Array.isArray(val)
          ? this.#makeReactive(val)
          : val;
      },
      set: (target, key, value) => {
        const prev = target[key];
        target[key] = value;
        if (!Object.is(prev, value)) this.#notify(key, value, prev);
        return true;
      },
      deleteProperty: (target, key) => {
        const had = key in target;
        delete target[key];
        if (had) this.#notify(key, undefined, target[key]);
        return true;
      },
    });
  }

  get state() { return this.#state; }

  update(updater) {
    // Snapshot before mutation for undo
    this.#history.push(structuredClone(this.#state));
    if (this.#history.length > this.#maxHistory) this.#history.shift();
    typeof updater === 'function' ? updater(this.#state) : Object.assign(this.#state, updater);
  }

  undo() {
    const prev = this.#history.pop();
    if (prev) Object.assign(this.#state, prev);
  }

  // Subscribe to specific key or '*' for any change
  on(key, fn) {
    if (!this.#subs.has(key)) this.#subs.set(key, new Set());
    this.#subs.get(key).add(fn);
    return () => this.#subs.get(key)?.delete(fn); // returns unsubscribe function
  }

  #notify(key, value, prev) {
    this.#subs.get(key)?.forEach(fn => fn(value, prev, this.#state));
    this.#subs.get('*')?.forEach(fn => fn(key, value, prev, this.#state));
  }
}

const store = new Store({
  user:    null,
  posts:   [],
  loading: false,
  error:   null,
});

// Subscribe to specific key
const unsub = store.on('user', (newUser, prevUser) => {
  renderUserMenu(newUser);
  analytics.identify(newUser?.id);
});

// Subscribe to any change
store.on('*', (key, value) => {
  localStorage.setItem('state', JSON.stringify(store.state));
});

store.update(s => { s.loading = true; });
store.update({ user: { id: 1, name: 'Alice' }, loading: false });
store.undo();

unsub(); // stop listening
```

### 13.2 Signals (Fine-grained Reactivity)

```js
// Signals: atomic reactive values — like Vue's ref() or Solid's createSignal()
function signal(initial) {
  let value = initial;
  const subscribers = new Set();

  return {
    get()   { return value; },
    peek()  { return value; }, // get without tracking (same here, useful in frameworks)
    set(next) {
      const v = typeof next === 'function' ? next(value) : next;
      if (!Object.is(v, value)) {
        value = v;
        [...subscribers].forEach(fn => fn(value));
      }
    },
    subscribe(fn) {
      subscribers.add(fn);
      fn(value); // call immediately with current value
      return () => subscribers.delete(fn);
    },
    [Symbol.toPrimitive]() { return value; },
  };
}

// Computed: derived signal, updates automatically
function computed(fn, ...deps) {
  const s = signal(fn());
  deps.forEach(dep => dep.subscribe(() => s.set(fn())));
  return { get: s.get.bind(s), subscribe: s.subscribe.bind(s) };
}

// Effect: side-effect that re-runs when deps change
function effect(fn, ...deps) {
  fn();
  const unsubs = deps.map(dep => dep.subscribe(() => fn()));
  return () => unsubs.forEach(u => u());
}

// Usage
const firstName = signal('Alice');
const lastName  = signal('Smith');
const age       = signal(30);
const fullName  = computed(() => `${firstName.get()} ${lastName.get()}`, firstName, lastName);
const isAdult   = computed(() => age.get() >= 18, age);

const stopNameEffect = effect(() => {
  document.querySelector('#name').textContent = fullName.get();
}, fullName);

firstName.set('Bob');  // → DOM updates to 'Bob Smith'
lastName.set('Jones'); // → DOM updates to 'Bob Jones'

stopNameEffect(); // stop the effect
```

### 13.3 Flux-like Store

```js
// Predictable state container with middleware support
class FluxStore {
  #state; #reducer; #listeners = new Set(); #middlewares;

  constructor(reducer, initialState, middlewares = []) {
    this.#reducer    = reducer;
    this.#state      = structuredClone(initialState);
    this.#middlewares = middlewares;
  }

  get state() { return this.#state; }

  dispatch(action) {
    // Apply middlewares right-to-left (like Redux)
    const chain = this.#middlewares.reduceRight(
      (next, mw) => mw(this)(next),
      (action) => {
        this.#state = this.#reducer(this.#state, action);
        this.#listeners.forEach(fn => fn(this.#state, action));
      }
    );
    return chain(action);
  }

  subscribe(fn) {
    this.#listeners.add(fn);
    return () => this.#listeners.delete(fn);
  }

  select(selector) { return selector(this.#state); }
}

// Middleware
const logger = store => next => action => {
  console.group(`Action: ${action.type}`);
  console.log('prev:', store.state);
  next(action);
  console.log('next:', store.state);
  console.groupEnd();
};

const thunk = store => next => action => {
  if (typeof action === 'function') {
    return action(store.dispatch.bind(store), () => store.state);
  }
  return next(action);
};

// Reducer
function reducer(state, { type, payload }) {
  switch (type) {
    case 'SET_USER':    return { ...state, user: payload };
    case 'ADD_POST':    return { ...state, posts: [...state.posts, payload] };
    case 'SET_LOADING': return { ...state, loading: payload };
    default:            return state;
  }
}

const store2 = new FluxStore(reducer, { user: null, posts: [], loading: false }, [logger, thunk]);

// Async thunk action
store2.dispatch(async (dispatch) => {
  dispatch({ type: 'SET_LOADING', payload: true });
  try {
    const user = await api.get('/me');
    dispatch({ type: 'SET_USER', payload: user });
  } finally {
    dispatch({ type: 'SET_LOADING', payload: false });
  }
});
```

---

## 14. Design Patterns

### 14.1 Observer (EventBus)

```js
class EventBus {
  #handlers = new Map();

  on(event, fn, { once = false, signal } = {}) {
    if (!this.#handlers.has(event)) this.#handlers.set(event, new Set());
    const wrapper = once
      ? (...args) => { fn(...args); this.off(event, wrapper); }
      : fn;
    this.#handlers.get(event).add(wrapper);
    signal?.addEventListener('abort', () => this.off(event, wrapper), { once: true });
    return () => this.off(event, wrapper);
  }

  off(event, fn)     { this.#handlers.get(event)?.delete(fn); }
  once(event, fn)    { return this.on(event, fn, { once: true }); }
  emit(event, ...args) {
    this.#handlers.get(event)?.forEach(fn => {
      try { fn(...args); } catch(e) { console.error(`EventBus error [${event}]:`, e); }
    });
  }
  clear(event)       { event ? this.#handlers.delete(event) : this.#handlers.clear(); }
}

export const events = new EventBus();
```

### 14.2 Factory and Registry

```js
class ComponentRegistry {
  #registry = new Map();

  register(name, ComponentClass) {
    if (this.#registry.has(name)) console.warn(`Overwriting component: ${name}`);
    this.#registry.set(name, ComponentClass);
    return this; // fluent
  }

  create(name, ...args) {
    const C = this.#registry.get(name);
    if (!C) throw new Error(`Unknown component: "${name}". Registered: [${[...this.#registry.keys()].join(', ')}]`);
    return new C(...args);
  }

  has(name)  { return this.#registry.has(name); }
  names()    { return [...this.#registry.keys()]; }
}

export const registry = new ComponentRegistry()
  .register('button',   ButtonComponent)
  .register('modal',    ModalComponent)
  .register('table',    TableComponent)
  .register('toast',    ToastComponent);
```

### 14.3 Command (Undo/Redo System)

```js
class CommandHistory {
  #undoStack = []; #redoStack = [];
  #maxDepth;

  constructor(maxDepth = 100) { this.#maxDepth = maxDepth; }

  execute(command) {
    command.execute();
    this.#undoStack.push(command);
    if (this.#undoStack.length > this.#maxDepth) this.#undoStack.shift();
    this.#redoStack = []; // new command invalidates redo stack
    return this;
  }

  undo() {
    const cmd = this.#undoStack.pop();
    if (cmd) { cmd.undo(); this.#redoStack.push(cmd); }
    return this;
  }

  redo() {
    const cmd = this.#redoStack.pop();
    if (cmd) { cmd.execute(); this.#undoStack.push(cmd); }
    return this;
  }

  get canUndo() { return this.#undoStack.length > 0; }
  get canRedo() { return this.#redoStack.length > 0; }
  get undoDepth() { return this.#undoStack.length; }
}

// Command example
class SetPropertyCommand {
  constructor(target, key, value) {
    this.target  = target;
    this.key     = key;
    this.newValue = value;
    this.oldValue = target[key];
  }
  execute() { this.target[this.key] = this.newValue; }
  undo()    { this.target[this.key] = this.oldValue; }
}

class InsertTextCommand {
  constructor(buffer, position, text) {
    this.buffer = buffer; this.position = position; this.text = text;
  }
  execute() { this.buffer.splice(this.position, 0, ...this.text.split('')); }
  undo()    { this.buffer.splice(this.position, this.text.length); }
}

const history = new CommandHistory();
const obj = { x: 1, y: 2 };
history.execute(new SetPropertyCommand(obj, 'x', 99));
console.log(obj.x); // 99
history.undo();
console.log(obj.x); // 1
history.redo();
console.log(obj.x); // 99
```

### 14.4 Builder (Fluent API)

```js
class RequestBuilder {
  #url; #method = 'GET'; #headers = {}; #body; #signal; #params = {};

  static get(url)    { return new RequestBuilder()._init('GET',    url); }
  static post(url)   { return new RequestBuilder()._init('POST',   url); }
  static put(url)    { return new RequestBuilder()._init('PUT',    url); }
  static delete(url) { return new RequestBuilder()._init('DELETE', url); }

  _init(method, url) { this.#method = method; this.#url = url; return this; }

  header(k, v)  { this.#headers[k] = v; return this; }
  auth(token)   { return this.header('Authorization', `Bearer ${token}`); }
  accept(type)  { return this.header('Accept', type); }
  json(data)    { this.#body = JSON.stringify(data); return this.header('Content-Type', 'application/json'); }
  timeout(ms)   { this.#signal = AbortSignal.timeout(ms); return this; }
  param(k, v)   { if (v != null) this.#params[k] = v; return this; }
  params(obj)   { Object.entries(obj).forEach(([k,v]) => this.param(k,v)); return this; }
  signal(s)     { this.#signal = s; return this; }

  async send() {
    const url = new URL(this.#url, location.origin);
    Object.entries(this.#params).forEach(([k, v]) => url.searchParams.set(k, v));
    const res = await fetch(url, {
      method: this.#method, headers: this.#headers,
      body: this.#body, signal: this.#signal,
    });
    if (!res.ok) throw new HttpError(res.status, res.statusText, res);
    const ct = res.headers.get('Content-Type') ?? '';
    return ct.includes('json') ? res.json() : res.text();
  }

  async sendForm(formData) {
    const url = new URL(this.#url, location.origin);
    const res = await fetch(url, { method: this.#method, body: formData, signal: this.#signal });
    if (!res.ok) throw new HttpError(res.status, res.statusText, res);
    return res.json();
  }
}

// Reads like English
const users = await RequestBuilder
  .get('/api/users')
  .auth(getToken())
  .params({ role: 'admin', page: 1, limit: 20 })
  .timeout(5000)
  .send();
```

### 14.5 Proxy Patterns

```js
// Validation proxy
function createValidated(schema) {
  return new Proxy({}, {
    set(target, key, value) {
      const rule = schema[key];
      if (rule) {
        if (rule.required && (value == null || value === ''))
          throw new Error(`${String(key)} is required`);
        if (rule.type && typeof value !== rule.type)
          throw new TypeError(`${String(key)} must be ${rule.type}, got ${typeof value}`);
        if (rule.min != null && value < rule.min)
          throw new RangeError(`${String(key)} must be >= ${rule.min}`);
        if (rule.max != null && value > rule.max)
          throw new RangeError(`${String(key)} must be <= ${rule.max}`);
        if (rule.pattern && !rule.pattern.test(value))
          throw new Error(`${String(key)} has invalid format`);
      }
      return Reflect.set(target, key, value);
    },
  });
}

// Read-only proxy (deep)
const readOnly = obj => new Proxy(obj, {
  set()            { throw new TypeError('This object is read-only'); },
  deleteProperty() { throw new TypeError('This object is read-only'); },
  get(t, k)        { const v=t[k]; return v&&typeof v==='object' ? readOnly(v) : v; },
});

// Observable proxy (deep reactive)
function observable(data, onChange) {
  return new Proxy(data, {
    get(t, k) {
      const v = t[k];
      return v && typeof v === 'object' ? observable(v, onChange) : v;
    },
    set(t, k, v) {
      const prev = t[k];
      const ok = Reflect.set(t, k, v);
      if (ok && !Object.is(prev, v)) onChange({ key: k, value: v, prev, target: t });
      return ok;
    },
    deleteProperty(t, k) {
      const prev = t[k];
      const ok = Reflect.deleteProperty(t, k);
      if (ok) onChange({ key: k, value: undefined, prev, target: t });
      return ok;
    },
  });
}
```

---

## 15. Observer APIs

### 15.1 IntersectionObserver

```js
// Lazy image loading with IntersectionObserver
function lazyLoadImages(selector = 'img[data-src]') {
  if (!('IntersectionObserver' in window)) {
    // Fallback: load all immediately
    document.querySelectorAll(selector).forEach(img => { img.src = img.dataset.src; });
    return () => {};
  }

  const observer = new IntersectionObserver((entries, self) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const img = entry.target;
      img.src    = img.dataset.src;
      img.srcset = img.dataset.srcset ?? '';
      if (img.dataset.sizes) img.sizes = img.dataset.sizes;
      img.removeAttribute('data-src');
      img.addEventListener('load', () => img.classList.add('loaded'), { once: true });
      self.unobserve(img);
    });
  }, { rootMargin: '200px 0px', threshold: 0 });

  document.querySelectorAll(selector).forEach(img => observer.observe(img));
  return () => observer.disconnect();
}

// Scroll-triggered animations
function animateOnScroll(selector, { activeClass = 'is-visible', threshold = 0.15, once = true } = {}) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) {
        if (!once) entry.target.classList.remove(activeClass);
        return;
      }
      entry.target.classList.add(activeClass);
      if (once) observer.unobserve(entry.target);
    });
  }, { threshold, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll(selector).forEach(el => observer.observe(el));
  return () => observer.disconnect();
}

// Infinite scroll
function infiniteScroll(sentinel, loadMore, { rootMargin = '300px' } = {}) {
  let loading = false;
  const observer = new IntersectionObserver(async ([entry]) => {
    if (!entry.isIntersecting || loading) return;
    loading = true;
    observer.unobserve(sentinel);
    try {
      const hasMore = await loadMore();
      if (hasMore) observer.observe(sentinel);
    } finally {
      loading = false;
    }
  }, { rootMargin });
  observer.observe(sentinel);
  return () => observer.disconnect();
}

// Sticky header detection
function stickyDetect(headerEl, triggerEl) {
  const observer = new IntersectionObserver(([entry]) => {
    headerEl.classList.toggle('is-sticky', !entry.isIntersecting);
  }, { threshold: 1, rootMargin: '0px 0px 0px 0px' });
  observer.observe(triggerEl);
  return () => observer.disconnect();
}

// Read percentage scrolled through element
function readProgress(article, onProgress) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => onProgress(Math.round(e.intersectionRatio * 100)));
  }, { threshold: Array.from({ length: 101 }, (_, i) => i / 100) });
  observer.observe(article);
  return () => observer.disconnect();
}
```

### 15.2 MutationObserver

```js
// Watch for DOM additions/removals
function watchDOM(root, { onAdd, onRemove, onAttrChange } = {}, options = {}) {
  const observer = new MutationObserver(mutations => {
    for (const mutation of mutations) {
      if (mutation.type === 'childList') {
        if (onAdd) {
          [...mutation.addedNodes]
            .filter(n => n.nodeType === Node.ELEMENT_NODE)
            .forEach(el => onAdd(el, mutation));
        }
        if (onRemove) {
          [...mutation.removedNodes]
            .filter(n => n.nodeType === Node.ELEMENT_NODE)
            .forEach(el => onRemove(el, mutation));
        }
      } else if (mutation.type === 'attributes' && onAttrChange) {
        onAttrChange(mutation.target, mutation.attributeName, mutation.oldValue, mutation);
      }
    }
  });

  observer.observe(root, {
    childList:          true,
    subtree:            true,
    attributes:         !!onAttrChange,
    attributeOldValue:  !!onAttrChange,
    ...options,
  });

  return () => observer.disconnect();
}

// Auto-initialize components as they're added to DOM
watchDOM(document.body, {
  onAdd: el => {
    el.querySelectorAll('[data-component]:not([data-init])').forEach(target => {
      const name = target.dataset.component;
      if (registry.has(name)) {
        registry.create(name, target);
        target.dataset.init = 'true';
      }
    });
    // Also check the element itself
    if (el.dataset?.component && !el.dataset.init && registry.has(el.dataset.component)) {
      registry.create(el.dataset.component, el);
      el.dataset.init = 'true';
    }
  },
});
```

### 15.3 ResizeObserver and PerformanceObserver

```js
// ResizeObserver — element size changes
function watchSize(element, callback, { debounceMs = 0 } = {}) {
  let raf, timer;
  const observer = new ResizeObserver(entries => {
    cancelAnimationFrame(raf);
    clearTimeout(timer);

    const run = () => {
      raf = requestAnimationFrame(() => {
        for (const entry of entries) {
          const { width, height } = entry.contentRect;
          const [boxSize] = entry.contentBoxSize ?? [];
          callback({
            width,
            height,
            inlineSize:  boxSize?.inlineSize  ?? width,
            blockSize:   boxSize?.blockSize   ?? height,
            element:     entry.target,
          });
        }
      });
    };

    debounceMs > 0 ? (timer = setTimeout(run, debounceMs)) : run();
  });

  observer.observe(element);
  return () => { observer.unobserve(element); cancelAnimationFrame(raf); clearTimeout(timer); };
}

// PerformanceObserver — long tasks and paint timing
function observeLongTasks(threshold = 50, callback) {
  if (!('PerformanceObserver' in window)) return () => {};
  const observer = new PerformanceObserver(list => {
    list.getEntries().filter(e => e.duration > threshold).forEach(callback);
  });
  observer.observe({ entryTypes: ['longtask'] });
  return () => observer.disconnect();
}

observeLongTasks(50, entry => {
  console.warn(`Long task: ${entry.duration.toFixed(0)}ms`, entry);
  // Report to analytics
});
```

## 16. Web Components

### 16.1 Custom Elements with Shadow DOM

```js
class AppToast extends HTMLElement {
  static observedAttributes = ['type', 'message', 'duration', 'dismissible'];

  #shadow; #timer;
  #colors = { info:'#3b82f6', success:'#10b981', error:'#ef4444', warn:'#f59e0b' };

  constructor() {
    super();
    this.#shadow = this.attachShadow({ mode: 'open' });
  }

  // Attribute accessors
  get type()        { return this.getAttribute('type') ?? 'info'; }
  get message()     { return this.getAttribute('message') ?? ''; }
  get duration()    { return Number(this.getAttribute('duration') ?? 3000); }
  get dismissible() { return this.hasAttribute('dismissible'); }

  connectedCallback()    { this.#render(); this.#autoClose(); }
  disconnectedCallback() { clearTimeout(this.#timer); }
  attributeChangedCallback(name, oldVal, newVal) {
    if (this.isConnected && oldVal !== newVal) this.#render();
  }

  #render() {
    const color = this.#colors[this.type] ?? this.#colors.info;
    this.#shadow.innerHTML = `
      <style>
        :host {
          display: block;
          font-family: system-ui, -apple-system, sans-serif;
          font-size: 0.875rem;
        }
        .toast {
          display: flex; align-items: center; gap: 0.75rem;
          padding: 0.75rem 1rem; border-radius: 0.5rem;
          color: #fff; background: ${color};
          box-shadow: 0 4px 12px rgba(0,0,0,.15);
          animation: slide-in 0.3s cubic-bezier(0.4,0,0.2,1);
        }
        @keyframes slide-in {
          from { transform: translateX(calc(100% + 1rem)); opacity: 0; }
          to   { transform: translateX(0); opacity: 1; }
        }
        .message  { flex: 1; }
        .close-btn {
          background: none; border: none; color: inherit;
          cursor: pointer; padding: 0; font-size: 1.25rem;
          line-height: 1; opacity: 0.8; transition: opacity 0.15s;
        }
        .close-btn:hover { opacity: 1; }
      </style>
      <div class="toast" role="alert" aria-live="assertive">
        <span class="message">${this.message}</span>
        ${this.dismissible ? '<button class="close-btn" aria-label="Dismiss">×</button>' : ''}
      </div>
    `;
    this.#shadow.querySelector('.close-btn')?.addEventListener('click', () => this.dismiss());
  }

  #autoClose() {
    if (this.duration > 0) {
      this.#timer = setTimeout(() => this.dismiss(), this.duration);
    }
  }

  dismiss() {
    this.dispatchEvent(new CustomEvent('dismiss', { bubbles: true }));
    this.remove();
  }

  static show(message, type = 'info', options = {}) {
    const toast = document.createElement('app-toast');
    toast.setAttribute('message', message);
    toast.setAttribute('type', type);
    if (options.duration !== undefined) toast.setAttribute('duration', String(options.duration));
    if (options.dismissible) toast.setAttribute('dismissible', '');

    // Toast container
    let container = document.querySelector('#toast-container');
    if (!container) {
      container = Object.assign(document.createElement('div'), { id: 'toast-container' });
      Object.assign(container.style, {
        position: 'fixed', bottom: '1rem', right: '1rem',
        display: 'flex', flexDirection: 'column', gap: '0.5rem',
        zIndex: '9999',
      });
      document.body.append(container);
    }
    container.append(toast);
    return toast;
  }
}

customElements.define('app-toast', AppToast);

// Usage
AppToast.show('File saved successfully!', 'success', { dismissible: true });
AppToast.show('Network error — retrying...', 'error', { duration: 0, dismissible: true });
```

### 16.2 HTML Templates and Slots

```js
// Define reusable template
const cardTemplate = document.createElement('template');
cardTemplate.innerHTML = `
  <style>
    :host { display: block; }
    .card {
      border: 1px solid #e2e8f0; border-radius: 0.5rem;
      overflow: hidden; background: white;
    }
    .card__header { padding: 1rem 1.5rem; border-bottom: 1px solid #e2e8f0; }
    .card__body   { padding: 1.5rem; }
    .card__footer { padding: 1rem 1.5rem; border-top: 1px solid #e2e8f0; }
    ::slotted(h2) { margin: 0; font-size: 1.125rem; }
    :host([variant="elevated"]) .card { box-shadow: 0 4px 12px rgba(0,0,0,.1); }
  </style>
  <div class="card">
    <header class="card__header">
      <slot name="header"><span>Card</span></slot>
    </header>
    <div class="card__body">
      <slot></slot>
    </div>
    <footer class="card__footer" hidden>
      <slot name="footer"></slot>
    </footer>
  </div>
`;

class UiCard extends HTMLElement {
  static observedAttributes = ['variant'];

  connectedCallback() {
    if (!this.shadowRoot) {
      const shadow = this.attachShadow({ mode: 'open' });
      shadow.append(cardTemplate.content.cloneNode(true));

      // Show footer only if slot has content
      const footerSlot   = shadow.querySelector('slot[name="footer"]');
      const footerEl     = shadow.querySelector('.card__footer');
      const updateFooter = () => { footerEl.hidden = footerSlot.assignedNodes().length === 0; };
      footerSlot.addEventListener('slotchange', updateFooter);
      updateFooter();
    }
  }

  attributeChangedCallback() {} // triggers re-render via observedAttributes
}

customElements.define('ui-card', UiCard);

// In HTML:
// <ui-card variant="elevated">
//   <h2 slot="header">User Profile</h2>
//   <p>Main content goes here.</p>
//   <div slot="footer">
//     <button>Edit</button> <button>Delete</button>
//   </div>
// </ui-card>
```

---

## 17. Performance

### 17.1 requestAnimationFrame Animations

```js
// Easing library
const ease = {
  linear:     t => t,
  inQuad:     t => t * t,
  outQuad:    t => t * (2 - t),
  inOutQuad:  t => t < .5 ? 2*t*t : -1+(4-2*t)*t,
  outCubic:   t => 1 - (1-t)**3,
  inOutCubic: t => t < .5 ? 4*t*t*t : (t-1)*(2*t-2)*(2*t-2)+1,
  outElastic: t => {
    const c4 = (2*Math.PI)/3;
    return t===0?0:t===1?1:Math.pow(2,-10*t)*Math.sin((t*10-0.75)*c4)+1;
  },
  outBounce:  t => {
    const n1=7.5625, d1=2.75;
    if (t<1/d1)      return n1*t*t;
    if (t<2/d1)      return n1*(t-=1.5/d1)*t+.75;
    if (t<2.5/d1)    return n1*(t-=2.25/d1)*t+.9375;
    return n1*(t-=2.625/d1)*t+.984375;
  },
};

// Animation runner
class Animator {
  #raf = null; #startTime = null;

  run({ from, to, duration, easing = ease.outCubic, onFrame, onComplete }) {
    this.cancel();
    const tick = (timestamp) => {
      this.#startTime ??= timestamp;
      const elapsed  = timestamp - this.#startTime;
      const progress = Math.min(elapsed / duration, 1);
      const value    = from + (to - from) * easing(progress);
      onFrame(value, progress);
      if (progress < 1) {
        this.#raf = requestAnimationFrame(tick);
      } else {
        this.#startTime = null;
        onComplete?.();
      }
    };
    this.#raf = requestAnimationFrame(tick);
    return this;
  }

  cancel() {
    if (this.#raf) { cancelAnimationFrame(this.#raf); this.#raf = null; this.#startTime = null; }
    return this;
  }
}

// Usage: smooth counter
const anim = new Animator();
anim.run({
  from: 0, to: 10000, duration: 2000, easing: ease.outCubic,
  onFrame: v => { el.textContent = Math.round(v).toLocaleString(); },
  onComplete: () => console.log('Done!'),
});

// Smooth scroll to element
function smoothScrollTo(target, { duration = 600, offset = 0 } = {}) {
  const startY = window.scrollY;
  const endY   = typeof target === 'number'
    ? target
    : target.getBoundingClientRect().top + startY - offset;

  return new Animator().run({
    from: startY, to: endY, duration, easing: ease.inOutCubic,
    onFrame: y => window.scrollTo(0, y),
  });
}
```

### 17.2 Virtual Scrolling

```js
class VirtualScroller {
  #container; #inner; #items; #itemH; #renderItem;
  #visible = new Map(); #raf = null;

  constructor({ container, items, itemHeight, renderItem, overscan = 3 }) {
    this.#container  = container;
    this.#items      = items;
    this.#itemH      = itemHeight;
    this.#renderItem = renderItem;
    this.#overscan   = overscan;

    this.#inner = Object.assign(document.createElement('div'), {
      style: `height:${items.length * itemHeight}px; position:relative; will-change:contents;`,
    });
    container.append(this.#inner);
    container.style.cssText += '; overflow:auto; position:relative;';

    container.addEventListener('scroll', () => {
      cancelAnimationFrame(this.#raf);
      this.#raf = requestAnimationFrame(() => this.#render());
    }, { passive: true });

    this.#render();
  }

  #render() {
    const { scrollTop, clientHeight } = this.#container;
    const startIdx = Math.max(0, Math.floor(scrollTop / this.#itemH) - this.#overscan);
    const endIdx   = Math.min(
      this.#items.length - 1,
      Math.ceil((scrollTop + clientHeight) / this.#itemH) + this.#overscan
    );

    // Remove off-screen elements
    for (const [i, el] of this.#visible) {
      if (i < startIdx || i > endIdx) {
        el.remove();
        this.#visible.delete(i);
      }
    }

    // Add newly visible elements
    const frag = document.createDocumentFragment();
    for (let i = startIdx; i <= endIdx; i++) {
      if (this.#visible.has(i)) continue;
      const el = this.#renderItem(this.#items[i], i);
      Object.assign(el.style, {
        position: 'absolute',
        top: `${i * this.#itemH}px`,
        width: '100%',
        height: `${this.#itemH}px`,
      });
      frag.append(el);
      this.#visible.set(i, el);
    }
    this.#inner.append(frag);
  }

  // Update data and re-render
  setItems(items) {
    this.#items = items;
    this.#inner.style.height = `${items.length * this.#itemH}px`;
    this.#visible.forEach(el => el.remove());
    this.#visible.clear();
    this.#render();
  }

  scrollToIndex(index) {
    this.#container.scrollTop = index * this.#itemH;
  }
}

// Usage: render 100,000 items smoothly
const list = new VirtualScroller({
  container:  document.querySelector('#list-container'),
  items:      Array.from({ length: 100_000 }, (_, i) => ({ id: i, name: `Item ${i}` })),
  itemHeight: 56,
  renderItem: (item) => {
    const el = document.createElement('div');
    el.className   = 'list-item';
    el.textContent = item.name;
    return el;
  },
});
```

### 17.3 Web Workers

```js
// worker.js
const handlers = {
  sort:       ({ data, key }) => [...data].sort((a,b) => (a[key]>b[key]?1:a[key]<b[key]?-1:0)),
  filter:     ({ data, field, value }) => data.filter(item => item[field] === value),
  aggregate:  ({ data, key }) => data.reduce((acc, item) => { acc[item[key]] = (acc[item[key]]??0)+1; return acc; }, {}),
  fib:        ({ n }) => { let a=0n,b=1n; for(let i=0;i<n;i++){[a,b]=[b,a+b];} return a.toString(); },
};

self.addEventListener('message', ({ data: { id, type, payload } }) => {
  try {
    const result = handlers[type]?.(payload) ?? null;
    self.postMessage({ id, result });
  } catch (err) {
    self.postMessage({ id, error: { message: err.message, stack: err.stack } });
  }
});

// main.js — typed bridge to worker
class WorkerBridge {
  #worker; #pending = new Map(); #id = 0;

  constructor(url) {
    this.#worker = new Worker(url, { type: 'module' });
    this.#worker.addEventListener('message', ({ data: { id, result, error } }) => {
      const { resolve, reject } = this.#pending.get(id) ?? {};
      this.#pending.delete(id);
      if (error) reject(Object.assign(new Error(error.message), { stack: error.stack }));
      else resolve(result);
    });
    this.#worker.addEventListener('error', err => {
      this.#pending.forEach(({ reject }) => reject(err));
      this.#pending.clear();
    });
  }

  run(type, payload) {
    return new Promise((resolve, reject) => {
      const id = ++this.#id;
      this.#pending.set(id, { resolve, reject });
      this.#worker.postMessage({ id, type, payload });
    });
  }

  terminate() { this.#worker.terminate(); }
}

const worker = new WorkerBridge('./worker.js');

// Offload heavy computation
const sorted    = await worker.run('sort', { data: bigArray, key: 'name' });
const grouped   = await worker.run('aggregate', { data: sales, key: 'region' });
```

### 17.4 DOM Performance Rules

```js
// ❌ Layout thrashing — interleaved reads and writes cause N reflows
elements.forEach(el => {
  const h = el.offsetHeight;           // READ  → reflow
  el.style.height = `${h + 10}px`;    // WRITE → invalidates layout
  const w = el.offsetWidth;            // READ  → forced reflow again!
  el.style.width = `${w + 5}px`;      // WRITE
});

// ✅ Batch: all reads first, then all writes
const measurements = elements.map(el => ({
  h: el.offsetHeight,
  w: el.offsetWidth,
}));
elements.forEach((el, i) => {
  el.style.height = `${measurements[i].h + 10}px`;
  el.style.width  = `${measurements[i].w + 5}px`;
});

// ✅ Use CSS transform (GPU compositor — no layout, no paint)
// ❌ el.style.left = x + 'px';  (triggers layout)
// ✅ el.style.transform = `translateX(${x}px)`;

// ✅ will-change — allocate GPU layer BEFORE animation, remove AFTER
el.style.willChange = 'transform, opacity'; // allocate
// ... run animation ...
el.addEventListener('transitionend', () => el.style.willChange = 'auto', { once: true });

// ✅ CSS contain — isolate layout scope
// .widget { contain: layout style; }
// Changes inside .widget won't trigger outer reflow

// ✅ Break long tasks for UI responsiveness
async function chunkedWork(items, fn, chunkSize = 50) {
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    chunk.forEach(fn);

    // Yield to browser between chunks
    await ('scheduler' in window && scheduler.yield
      ? scheduler.yield()                       // Chrome scheduler API
      : new Promise(r => setTimeout(r, 0)));   // setTimeout fallback
  }
}
```

---

## 18. Security

### 18.1 XSS Prevention — Complete Guide

```js
// ═══════════════════════════════════════════════════════════
// RULE: NEVER inject user-controlled data into innerHTML,
//       src, href, style, or event handler attributes
// ═══════════════════════════════════════════════════════════

// ❌ DANGEROUS — don't do any of these
el.innerHTML  = userInput;
document.write(userInput);
eval(userInput);
new Function(userInput)();
setTimeout(userInput, 0);               // string form!
el.setAttribute('onclick', userInput);
el.style.cssText = userInput;
el.setAttribute('href', userInput);     // javascript: URLs!

// ✅ SAFE — use textContent for text
el.textContent = userInput; // always safe, auto-escapes

// ✅ HTML escaping utility
const escapeHtml = (() => {
  const map = { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":"&#39;" };
  return str => String(str ?? '').replace(/[&<>"']/g, c => map[c]);
})();

// ✅ Safe URL validation — block javascript: data: vbscript:
function isSafeUrl(url) {
  try {
    const parsed = new URL(url, location.href);
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch { return false; }
}

function setSafeHref(link, url) {
  if (isSafeUrl(url)) link.href = url;
  else { link.removeAttribute('href'); console.warn('Blocked unsafe URL:', url); }
}

// ✅ Safe dynamic CSS property values
function setSafeStyle(el, property, value) {
  // Block CSS injection attempts
  if (/expression|url|javascript/i.test(value)) return;
  el.style.setProperty(property, value);
}

// ✅ Trusted Types (Chrome/Edge) — strongest protection
if (window.trustedTypes?.createPolicy) {
  const policy = trustedTypes.createPolicy('main-policy', {
    createHTML:      html => DOMPurify.sanitize(html),
    createScriptURL: url  => isSafeUrl(url) ? url : '',
    createScript:    () => { throw new Error('Script creation not allowed'); },
  });
  el.innerHTML = policy.createHTML(richContent);
}

// ✅ Content Security Policy (set as HTTP header from server)
// Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{RANDOM}';
// img-src * data: blob:; style-src 'self' 'unsafe-inline'; connect-src 'self' api.example.com
```

### 18.2 CSRF, Clickjacking and Other Attacks

```js
// ── CSRF: add token to mutating requests ─────────────────
function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]')?.content
    ?? getCookieValue('csrf-token')
    ?? '';
}

function getCookieValue(name) {
  return document.cookie.match(`(?:^|;)\\s*${name}\\s*=\\s*([^;]+)`)?.[1] ?? null;
}

// Intercept fetch to add CSRF header automatically
const { fetch: origFetch } = window;
window.fetch = (resource, init = {}) => {
  const method = (init.method ?? 'GET').toUpperCase();
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    init.headers = new Headers(init.headers);
    init.headers.set('X-CSRF-Token', getCsrfToken());
  }
  return origFetch(resource, init);
};

// ── Clickjacking: detect iframe embedding ─────────────────
if (window.top !== window.self) {
  // We're in an iframe — potential clickjacking attack
  document.body.style.display = 'none';
  // Server-side header is the REAL fix: X-Frame-Options: DENY
  // or: Content-Security-Policy: frame-ancestors 'none'
}

// ── Subresource Integrity (SRI) ───────────────────────────
// <script
//   src="https://cdn.example.com/lib.js"
//   integrity="sha384-abc123..."
//   crossorigin="anonymous">
// </script>

// ── Sanitize stored/URL data before use ──────────────────
function safeGetParam(name) {
  const value = new URLSearchParams(location.search).get(name) ?? '';
  // Never directly use URL params in innerHTML or as URLs without validation
  return value.replace(/[<>"'&]/g, ''); // minimal cleanup
}

// ── Prevent open redirect ─────────────────────────────────
function safeRedirect(url) {
  const target = new URL(url, location.href);
  if (target.origin !== location.origin) {
    console.warn('Cross-origin redirect blocked:', url);
    return;
  }
  location.href = target.href;
}
```

---

## 19. Error Handling

### 19.1 Custom Error Hierarchy

```js
// Base application error
class AppError extends Error {
  constructor(message, code, context = {}) {
    super(message);
    this.name      = this.constructor.name;
    this.code      = code;
    this.context   = context;
    this.timestamp = new Date().toISOString();
    // Correct stack trace in V8 engines
    if (Error.captureStackTrace) Error.captureStackTrace(this, this.constructor);
  }
  toJSON() {
    return { name:this.name, message:this.message, code:this.code, context:this.context };
  }
}

class ValidationError  extends AppError {
  constructor(field, message, value) {
    super(message, 'VALIDATION_ERROR', { field, value });
    this.field = field;
  }
}
class NotFoundError    extends AppError {
  constructor(resource, id) { super(`${resource} #${id} not found`, 'NOT_FOUND', { resource, id }); }
}
class UnauthorizedError extends AppError {
  constructor(action) { super(`Unauthorized: ${action}`, 'UNAUTHORIZED', { action }); }
}
class NetworkError     extends AppError {
  constructor(message, context) { super(message, 'NETWORK_ERROR', context); }
}
class HttpError extends AppError {
  constructor(status, statusText, response) {
    super(`HTTP ${status}: ${statusText}`, 'HTTP_ERROR', { status });
    this.status = status; this.response = response;
  }
}

// Typed error handling
try { /*...*/ }
catch (err) {
  if (err instanceof ValidationError) {
    showFieldError(err.field, err.message);
  } else if (err instanceof UnauthorizedError) {
    redirectToLogin();
  } else if (err instanceof NetworkError) {
    showOfflineBanner();
  } else if (err instanceof HttpError && err.status === 404) {
    showNotFound();
  } else {
    throw err; // re-throw unknown errors — don't swallow!
  }
}
```

### 19.2 Global Error Boundaries

```js
// Synchronous uncaught errors
window.addEventListener('error', (event) => {
  const { error, message, filename, lineno, colno } = event;
  reportError({
    type:    'uncaught',
    message: error?.message ?? message,
    stack:   error?.stack,
    source:  `${filename}:${lineno}:${colno}`,
  });
  // event.preventDefault() to suppress default console output
});

// Unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  const { reason } = event;
  reportError({
    type:    'unhandledRejection',
    message: reason?.message ?? String(reason),
    stack:   reason?.stack,
    code:    reason?.code,
  });
  event.preventDefault(); // suppress default console.error
});

// Error reporting service
const errorQueue = [];
let reporting = false;

async function reportError(info) {
  errorQueue.push({ ...info, url: location.href, ts: new Date().toISOString() });
  if (reporting) return;
  reporting = true;

  while (errorQueue.length > 0) {
    const batch = errorQueue.splice(0, 10); // batch up to 10 at once
    try {
      await fetch('/api/errors', {
        method:    'POST',
        keepalive: true, // send even on page unload!
        headers:   { 'Content-Type': 'application/json' },
        body:      JSON.stringify(batch),
      });
    } catch { /* never throw in error reporter */ }
  }
  reporting = false;
}
```

### 19.3 Result Type (Railway-Oriented Programming)

```js
// Avoid exceptions for expected failure paths — make failures explicit in types
class Result {
  static ok(value)  { return new OkResult(value); }
  static err(error) { return new ErrResult(error); }

  static async wrap(fn) {
    try   { return Result.ok(await fn()); }
    catch (e) { return Result.err(e); }
  }

  static all(results) {
    const values = [];
    for (const r of results) {
      if (!r.ok) return r;
      values.push(r.value);
    }
    return Result.ok(values);
  }
}

class OkResult extends Result {
  constructor(v) { super(); this.ok=true;  this.value=v; }
  map(fn)        { return Result.ok(fn(this.value)); }
  flatMap(fn)    { return fn(this.value); }
  mapErr()       { return this; }
  match({ok})    { return ok(this.value); }
  unwrapOr()     { return this.value; }
  tap(fn)        { fn(this.value); return this; }
}

class ErrResult extends Result {
  constructor(e) { super(); this.ok=false; this.error=e; }
  map()          { return this; }
  flatMap()      { return this; }
  mapErr(fn)     { return Result.err(fn(this.error)); }
  match({err})   { return err(this.error); }
  unwrapOr(def)  { return def; }
  tap()          { return this; }
}

// Usage
const result = await Result.wrap(() => api.get('/users'));

const names = result
  .map(users => users.filter(u => u.active))
  .map(users => users.map(u => u.name))
  .unwrapOr([]);

result.match({
  ok:  users  => renderUsers(users),
  err: error  => showError(error.message),
});

// Combine multiple results
const allResults = Result.all([
  await Result.wrap(() => loadUser(id)),
  await Result.wrap(() => loadPosts(id)),
]);

if (allResults.ok) {
  const [user, posts] = allResults.value;
  render({ user, posts });
}
```

---

## 20. Modern Web APIs

### 20.1 URL and URLSearchParams

```js
// Parse and manipulate URLs
const url = new URL('https://api.example.com/search?q=hello&page=2&limit=20');
url.protocol;   // 'https:'
url.hostname;   // 'api.example.com'
url.pathname;   // '/search'
url.search;     // '?q=hello&page=2&limit=20'
url.hash;       // ''

// Read params
url.searchParams.get('q');        // 'hello'
url.searchParams.get('page');     // '2' (always string!)
url.searchParams.getAll('tag');   // array if multiple
url.searchParams.has('limit');    // true

// Modify params
url.searchParams.set('page', 3);
url.searchParams.append('tag', 'js');
url.searchParams.delete('limit');
url.searchParams.sort();           // sort alphabetically
url.toString();                    // reconstructed URL string

// Build query strings
const params = new URLSearchParams({
  q:      'hello world',
  sort:   'date',
  order:  'desc',
  limit:  20,
});
params.toString(); // 'q=hello+world&sort=date&order=desc&limit=20'
fetch(`/api/search?${params}`);

// Iterate
for (const [key, value] of params) { /*...*/ }
Object.fromEntries(params); // → plain object (loses duplicates)
[...params.entries()];     // → array of [key,value] pairs
```

### 20.2 Clipboard, Notifications, Page Visibility

```js
// ── Clipboard API ─────────────────────────────────────────
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback for older browsers / non-HTTPS
    const el = Object.assign(document.createElement('textarea'), {
      value: text, readOnly: true,
      style: 'position:absolute;left:-9999px;',
    });
    document.body.append(el);
    el.select();
    const ok = document.execCommand('copy');
    el.remove();
    return ok;
  }
}

async function readClipboard() {
  try { return await navigator.clipboard.readText(); }
  catch { return null; }
}

// ── Notifications API ─────────────────────────────────────
async function sendNotification(title, { body, icon, badge, tag, onClick } = {}) {
  if (!('Notification' in window)) return null;
  if (Notification.permission !== 'granted') {
    if (Notification.permission === 'denied') return null;
    const perm = await Notification.requestPermission();
    if (perm !== 'granted') return null;
  }
  const n = new Notification(title, { body, icon, badge, tag });
  if (onClick) n.addEventListener('click', () => { window.focus(); n.close(); onClick(); });
  return n;
}

// ── Page Visibility API ───────────────────────────────────
class VisibilityManager {
  #handlers = { hidden: new Set(), visible: new Set() };

  constructor() {
    document.addEventListener('visibilitychange', () => {
      const type = document.hidden ? 'hidden' : 'visible';
      this.#handlers[type].forEach(fn => fn());
    });
  }

  onHidden (fn) { this.#handlers.hidden.add(fn);  return () => this.#handlers.hidden.delete(fn); }
  onVisible(fn) { this.#handlers.visible.add(fn); return () => this.#handlers.visible.delete(fn); }
  get isHidden() { return document.hidden; }
}

const visibility = new VisibilityManager();
visibility.onHidden (() => { pauseVideo(); stopPolling(); });
visibility.onVisible(() => { resumeVideo(); startPolling(); syncData(); });
```

### 20.3 structuredClone, History API

```js
// ── structuredClone (ES2022) ──────────────────────────────
// Deep clone that handles more types than JSON.parse/stringify
const original = {
  date:   new Date(),
  map:    new Map([['key', 'val']]),
  set:    new Set([1, 2, 3]),
  buf:    new ArrayBuffer(8),
  re:     /pattern/gi,
  error:  new Error('oops'),
  nested: { arr: [1, [2, 3]] },
};
const clone = structuredClone(original);
clone.date !== original.date;           // true — different object
clone.map.get('key');                   // 'val'
// Does NOT handle: Function, DOM nodes, WeakMap, WeakSet, Symbol

// ── History API (SPA routing) ─────────────────────────────
// pushState — adds new history entry
history.pushState({ userId: 42 }, '', '/users/42');

// replaceState — replaces current entry
history.replaceState({ tab: 'settings' }, '', '/settings');

// Navigate back/forward
history.back();
history.forward();
history.go(-2); // 2 steps back

// Listen for navigation
window.addEventListener('popstate', (event) => {
  const { state } = event;
  handleNavigation(location.pathname, state);
});

// Intercept link clicks for SPA
document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href]');
  if (!link) return;

  const url = new URL(link.href);

  // Only handle same-origin, non-external links
  if (url.origin !== location.origin) return;
  if (link.target === '_blank') return;
  if (link.hasAttribute('download')) return;

  event.preventDefault();
  history.pushState({}, '', url.pathname + url.search + url.hash);
  handleNavigation(url.pathname);
});
```

---

## 21. Animations and Visual Effects

### 21.1 Web Animations API

```js
// Animate — returns Animation object with full control
const anim = el.animate([
  { opacity: 0, transform: 'translateY(-20px) scale(0.95)' },
  { opacity: 1, transform: 'translateY(0)    scale(1)' },
], {
  duration:  400,
  easing:    'cubic-bezier(0.4, 0, 0.2, 1)',
  fill:      'forwards',  // maintain final state
  delay:     100,
  iterations: 1,
  direction: 'normal',   // 'reverse', 'alternate', 'alternate-reverse'
});

// Control
anim.play();     anim.pause();
anim.reverse();  anim.cancel();  anim.finish();
anim.playbackRate = 2; // double speed

// Promise-based
await anim.finished;
el.classList.add('animation-complete');
el.getAnimations(); // get all running animations

// Reusable animation factory
const animations = {
  fadeIn:     el => el.animate([{opacity:0},{opacity:1}],{duration:200,fill:'forwards'}),
  fadeOut:    el => el.animate([{opacity:1},{opacity:0}],{duration:200,fill:'forwards'}),
  slideDown:  el => el.animate([{transform:'translateY(-100%)',opacity:0},{transform:'none',opacity:1}],{duration:300,easing:'ease-out',fill:'forwards'}),
  slideUp:    el => el.animate([{transform:'none',opacity:1},{transform:'translateY(-100%)',opacity:0}],{duration:300,easing:'ease-in',fill:'forwards'}),
  shake:      el => el.animate(
    [{transform:'translateX(0)'},{transform:'translateX(-8px)'},{transform:'translateX(8px)'},{transform:'translateX(-4px)'},{transform:'translateX(4px)'},{transform:'translateX(0)'}],
    {duration:500,easing:'ease-in-out'}
  ),
  pulse:      el => el.animate(
    [{transform:'scale(1)'},{transform:'scale(1.05)'},{transform:'scale(1)'}],
    {duration:600,easing:'ease-in-out',iterations:Infinity}
  ),
};

// Await fade out, then remove element
await animations.fadeOut(modal).finished;
modal.remove();
```

### 21.2 FLIP Animations

```js
// FLIP: First, Last, Invert, Play — smooth animations for DOM mutations
async function flipAnimate(container, mutate, options = {}) {
  const { duration = 400, easing = 'ease-out' } = options;

  // FIRST: record positions before mutation
  const snapshots = new Map(
    [...container.children].map(el => [
      el,
      { rect: el.getBoundingClientRect(), opacity: getComputedStyle(el).opacity },
    ])
  );

  // LAST: apply the DOM mutation
  mutate();

  // Force layout to get new positions
  container.offsetHeight; // read triggers layout

  // INVERT + PLAY: animate each element from its old position to new
  for (const el of container.children) {
    const snap = snapshots.get(el);
    if (!snap) continue; // newly added element — let it animate in naturally

    const next = el.getBoundingClientRect();
    const dx   = snap.rect.left - next.left;
    const dy   = snap.rect.top  - next.top;

    if (Math.abs(dx) < 0.5 && Math.abs(dy) < 0.5) continue; // no movement

    el.animate(
      [{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'none' }],
      { duration, easing }
    );
  }
}

// Usage: animate list reorder
await flipAnimate(listEl, () => {
  // Mutation that rearranges DOM elements
  const items = [...listEl.children].sort((a, b) =>
    a.dataset.priority - b.dataset.priority
  );
  listEl.append(...items);
});
```

### 21.3 CSS Variables from JS — Theme System

```js
const Theme = {
  themes: {
    light: {
      '--color-bg':         '#ffffff',
      '--color-surface':    '#f8fafc',
      '--color-text':       '#0f172a',
      '--color-text-muted': '#64748b',
      '--color-primary':    '#3b82f6',
      '--color-border':     '#e2e8f0',
      '--shadow-sm':        '0 1px 2px rgba(0,0,0,.05)',
      '--radius':           '0.5rem',
    },
    dark: {
      '--color-bg':         '#0f172a',
      '--color-surface':    '#1e293b',
      '--color-text':       '#f1f5f9',
      '--color-text-muted': '#94a3b8',
      '--color-primary':    '#38bdf8',
      '--color-border':     '#334155',
      '--shadow-sm':        '0 1px 2px rgba(0,0,0,.3)',
      '--radius':           '0.5rem',
    },
  },

  current: 'light',

  apply(name) {
    const vars = this.themes[name];
    if (!vars) throw new Error(`Unknown theme: ${name}`);
    const root = document.documentElement;
    Object.entries(vars).forEach(([k, v]) => root.style.setProperty(k, v));
    root.dataset.theme = name;
    this.current = name;
    localStorage.setItem('theme', name);
    document.dispatchEvent(new CustomEvent('theme:change', { detail: { theme: name } }));
  },

  toggle() {
    this.apply(this.current === 'light' ? 'dark' : 'light');
  },

  get(varName) {
    return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
  },

  init() {
    const saved    = localStorage.getItem('theme');
    const preferred = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    this.apply(saved ?? preferred);

    // Sync with OS preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!localStorage.getItem('theme')) this.apply(e.matches ? 'dark' : 'light');
    });
  },
};

Theme.init();
document.querySelector('#theme-toggle').addEventListener('click', () => Theme.toggle());
```

---

## 22. Regular Expressions

### 22.1 Modern Flags and Named Groups

```js
// Flags reference:
// g — global (all matches)
// i — case-insensitive
// m — multiline (^/$ match line boundaries)
// s — dotAll (. matches \n and other newlines)
// u — Unicode (correct handling of emoji, non-BMP chars)
// y — sticky (match only at lastIndex)
// d — generate indices for match start/end (ES2022)
// v — unicode sets, string properties (ES2024)

// ── Named capturing groups (ES2018) ───────────────────────
const dateRe = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/d;
const match  = '2025-06-15'.match(dateRe);
const { year, month, day } = match.groups;  // '2025', '06', '15'
match.indices.groups.year;                  // [0, 4] — with /d flag

// Replace with named backreference
'2025-06-15'.replace(
  /(?<y>\d{4})-(?<m>\d{2})-(?<d>\d{2})/,
  '$<d>/$<m>/$<y>'  // '15/06/2025'
);

// ── Lookbehind (ES2018) ───────────────────────────────────
/(?<=\$)\d+/.exec('Price: $100')[0];   // '100' — number after $
/(?<!\$)\d+/.exec('Price: €100')[0];   // '100' — number NOT after $

// ── Unicode property escapes ──────────────────────────────
/\p{Letter}/u.test('Ж');             // true — any Unicode letter
/\p{Emoji}/u.test('😀');             // true
/\p{Script=Cyrillic}/u.test('Ц');    // true
/\p{Decimal_Number}/u.test('9');     // true
/\p{Lu}/u.test('A');                 // true — uppercase letter

// ── Unicode sets /v flag (ES2024) ─────────────────────────
/[\p{Letter}--[A-Za-z]]/v.test('Ж'); // true — non-ASCII letter
/[\p{Decimal_Number}&&\p{ASCII}]/v.test('5'); // true — ASCII digit only
```

### 22.2 Methods and Utilities

```js
// matchAll — all matches with groups (requires /g flag)
const html    = '<a href="https://a.com">Link A</a><a href="https://b.com">Link B</a>';
const linkRe  = /<a\s+href="(?<url>[^"]+)">(?<text>[^<]+)<\/a>/g;
const links   = [...html.matchAll(linkRe)].map(m => ({ url: m.groups.url, text: m.groups.text }));
// [{ url:'https://a.com', text:'Link A' }, ...]

// replaceAll with function
const escaped = text.replaceAll(/\d+/g, n => String(Number(n) * 2));

// Split with groups (groups are captured in result)
'a1b2c3'.split(/(\d)/); // ['a', '1', 'b', '2', 'c', '3', '']

// ── Escape for dynamic regex ──────────────────────────────
const escapeRegex = str => str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// Safe highlight
function highlight(text, term) {
  if (!term.trim()) return escapeHtml(text);
  const re = new RegExp(`(${escapeRegex(term)})`, 'gi');
  return escapeHtml(text).replace(re, '<mark>$1</mark>');
}

// ── Production-ready patterns ─────────────────────────────
const patterns = {
  email:      /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/,
  url:        /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&/=]*)$/,
  slug:       /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
  uuid:       /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
  hexColor:   /^#(?:[0-9a-f]{3}|[0-9a-f]{4}|[0-9a-f]{6}|[0-9a-f]{8})$/i,
  semver:     /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([\da-z\-.]+))?(?:\+([\da-z\-.]+))?$/i,
  ipv4:       /^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$/,
  phone:      /^\+?[\d\s\-().]{7,20}$/,
  postalCode: /^\d{5}(-\d{4})?$/,
  jwt:        /^[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]*$/,
};
const validate = (type, value) => patterns[type]?.test(value) ?? false;
validate('email', 'user@example.com'); // true
```

## 23. Internationalization — Intl API

### 23.1 Numbers, Currency and Units

```js
// Number formatting
const usd = new Intl.NumberFormat('en-US', { style:'currency', currency:'USD' });
usd.format(1234567.89); // '$1,234,567.89'

const eur = new Intl.NumberFormat('de-DE', { style:'currency', currency:'EUR', minimumFractionDigits:0 });
eur.format(1234567);    // '1.234.567 €'

// Compact notation
new Intl.NumberFormat('en-US', { notation:'compact', compactDisplay:'short' }).format(1_500_000); // '1.5M'
new Intl.NumberFormat('en-US', { notation:'compact' }).format(2500);           // '2.5K'

// Percentages and units
new Intl.NumberFormat('en-US', { style:'percent', maximumFractionDigits:1 }).format(0.8567); // '85.7%'
new Intl.NumberFormat('en-US', { style:'unit', unit:'kilometer-per-hour' }).format(120);      // '120 km/h'
new Intl.NumberFormat('en-US', { style:'unit', unit:'byte', notation:'compact' }).format(1_048_576); // '1MB'

// Range formatting
const rangeFmt = new Intl.NumberFormat('en-US', { style:'currency', currency:'USD' });
rangeFmt.formatRange(100, 200); // '$100 – $200'

// Format to parts (for custom rendering)
new Intl.NumberFormat('en-US', { style:'currency', currency:'USD' })
  .formatToParts(1234.5);
// [{type:'currency',value:'$'},{type:'integer',value:'1'},{type:'group',value:','},...}]
```

### 23.2 Dates, Relative Time and Lists

```js
// Date formatting
const dtf = new Intl.DateTimeFormat('en-US', {
  weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  hour: '2-digit', minute: '2-digit', timeZone: 'America/New_York', hour12: true,
});
dtf.format(new Date()); // 'Wednesday, June 15, 2025 at 02:30 PM'

// Relative time
const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto', style: 'long' });
rtf.format(-1,  'day');     // 'yesterday'
rtf.format(-3,  'hour');    // '3 hours ago'
rtf.format(2,   'week');    // 'in 2 weeks'
rtf.format(0,   'minute');  // 'this minute'
rtf.format(-30, 'second');  // '30 seconds ago'

// Auto-select the most appropriate unit
function timeAgo(date) {
  const sec = Math.round((Date.now() - new Date(date)) / 1000);
  const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
  const thresholds = [
    [60,          1,          'second'],
    [3600,        60,         'minute'],
    [86400,       3600,       'hour'],
    [86400 * 30,  86400,      'day'],
    [86400 * 365, 86400 * 30, 'month'],
    [Infinity,    86400 * 365,'year'],
  ];
  for (const [limit, divisor, unit] of thresholds) {
    if (Math.abs(sec) < limit) return rtf.format(-Math.round(sec / divisor), unit);
  }
}
timeAgo(new Date(Date.now() - 5 * 60_000)); // '5 minutes ago'

// List formatting
new Intl.ListFormat('en', { type: 'conjunction', style: 'long' })
  .format(['Alice', 'Bob', 'Carol']); // 'Alice, Bob, and Carol'
new Intl.ListFormat('en', { type: 'disjunction' })
  .format(['PDF', 'DOCX', 'TXT']);    // 'PDF, DOCX, or TXT'

// Plural rules
const pr = new Intl.PluralRules('en');
function itemLabel(n) {
  return { one: `${n} item`, other: `${n} items` }[pr.select(n)];
}
itemLabel(1); // '1 item'
itemLabel(5); // '5 items'

// Locale-aware sorting
const collator = new Intl.Collator('en', { sensitivity: 'base', numeric: true });
['file10', 'file2', 'file1'].sort(collator.compare); // ['file1','file2','file10']
['Apple', 'banana', 'Cherry'].sort(collator.compare); // case-insensitive sort
```

---

## 24. Service Workers and PWA

### 24.1 Registration and Lifecycle

```js
// main.js
async function registerServiceWorker(swPath = '/sw.js') {
  if (!('serviceWorker' in navigator)) {
    console.info('Service Worker not supported');
    return null;
  }

  try {
    const registration = await navigator.serviceWorker.register(swPath, {
      scope:          '/',
      updateViaCache: 'none', // always check for SW updates on network
    });

    // Detect new SW installation
    registration.addEventListener('updatefound', () => {
      const newWorker = registration.installing;

      newWorker.addEventListener('statechange', () => {
        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
          // New version is ready — prompt user to update
          showUpdatePrompt({
            onAccept: () => {
              newWorker.postMessage({ type: 'SKIP_WAITING' });
            },
          });
        }
      });
    });

    // Reload when new SW takes control
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      window.location.reload();
    });

    return registration;
  } catch (err) {
    console.error('SW registration failed:', err);
    return null;
  }
}

registerServiceWorker();
```

### 24.2 Cache Strategies (sw.js)

```js
// sw.js — full service worker with multiple caching strategies
const CACHE_VERSION = 'v1';
const STATIC_CACHE  = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;

const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/app.js',
  '/style.css',
  '/manifest.json',
  '/offline.html',
  '/icons/icon-192.png',
];

// ── Install ───────────────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(STATIC_CACHE);
    await cache.addAll(PRECACHE_URLS);
    await self.skipWaiting(); // take control immediately
  })());
});

// ── Activate ──────────────────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const cacheNames = await caches.keys();
    await Promise.all(
      cacheNames
        .filter(name => name !== STATIC_CACHE && name !== DYNAMIC_CACHE)
        .map(name => caches.delete(name))
    );
    await self.clients.claim(); // control existing tabs
  })());
});

// ── Fetch strategies ──────────────────────────────────────

// Cache First: static assets (JS, CSS, images, fonts)
async function cacheFirst(request, cacheName = STATIC_CACHE) {
  const cached = await caches.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(cacheName);
    cache.put(request, response.clone());
  }
  return response;
}

// Network First: API data, HTML pages
async function networkFirst(request, cacheName = DYNAMIC_CACHE) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached ?? caches.match('/offline.html');
  }
}

// Stale While Revalidate: balance speed and freshness
async function staleWhileRevalidate(request, cacheName = DYNAMIC_CACHE) {
  const cache  = await caches.open(cacheName);
  const cached = await cache.match(request);

  const freshPromise = fetch(request).then(res => {
    if (res.ok) cache.put(request, res.clone());
    return res;
  }).catch(() => null);

  return cached ?? freshPromise;
}

// ── Route matching ────────────────────────────────────────
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Non-GET requests pass through
  if (request.method !== 'GET') return;

  // API calls — Network First
  if (url.pathname.startsWith('/api/')) {
    return event.respondWith(networkFirst(request));
  }

  // Static assets — Cache First
  if (/\.(js|css|woff2?|png|jpg|jpeg|svg|webp|ico)$/.test(url.pathname)) {
    return event.respondWith(cacheFirst(request));
  }

  // Navigation — Stale While Revalidate
  if (request.mode === 'navigate') {
    return event.respondWith(staleWhileRevalidate(request));
  }
});

// ── Messages from main thread ─────────────────────────────
self.addEventListener('message', event => {
  if (event.data?.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
```

### 24.3 Background Sync

```js
// sw.js — sync pending data when back online
self.addEventListener('sync', event => {
  if (event.tag === 'sync-queue') {
    event.waitUntil(processSyncQueue());
  }
});

async function processSyncQueue() {
  const db   = await openDB();
  const queue = await db.getAll('sync-queue');

  await Promise.all(queue.map(async item => {
    try {
      await fetch(item.url, {
        method: item.method,
        body:   JSON.stringify(item.data),
        headers: { 'Content-Type': 'application/json' },
      });
      await db.delete('sync-queue', item.id);
    } catch { /* retry on next sync */ }
  }));
}

// main.js — queue request for sync
async function queueForSync(url, method, data) {
  const db  = await openDB();
  await db.put('sync-queue', { id: crypto.randomUUID(), url, method, data, ts: Date.now() });

  const reg = await navigator.serviceWorker.ready;
  await reg.sync.register('sync-queue');
}
```

---

## 25. WebSocket and Realtime

### 25.1 Auto-Reconnecting WebSocket Client

```js
class WebSocketClient extends EventTarget {
  #url; #ws = null; #protocols;
  #delay = 1000; #maxDelay; #attempts = 0;
  #manual = false; #pending = []; #pingTimer = null;
  #pingInterval; #reconnectFactor;

  constructor(url, {
    protocols      = [],
    maxDelay       = 30_000,
    pingInterval   = 25_000,
    reconnectFactor = 2,
  } = {}) {
    super();
    this.#url = url;
    this.#protocols = protocols;
    this.#maxDelay = maxDelay;
    this.#pingInterval = pingInterval;
    this.#reconnectFactor = reconnectFactor;
  }

  connect() {
    this.#manual = false;
    this.#openSocket();
    return this;
  }

  #openSocket() {
    try {
      this.#ws = this.#protocols.length
        ? new WebSocket(this.#url, this.#protocols)
        : new WebSocket(this.#url);
    } catch (err) {
      this.#scheduleReconnect();
      return;
    }

    this.#ws.onopen = () => {
      this.#attempts = 0;
      this.#delay    = 1000;
      this.dispatchEvent(new Event('open'));

      // Flush pending messages
      const pending = [...this.#pending];
      this.#pending = [];
      pending.forEach(msg => this.#ws.send(msg));

      // Start heartbeat
      this.#pingTimer = setInterval(() => {
        if (this.#ws?.readyState === WebSocket.OPEN) {
          this.#ws.send(JSON.stringify({ type: 'ping', ts: Date.now() }));
        }
      }, this.#pingInterval);
    };

    this.#ws.onmessage = ({ data }) => {
      try {
        const msg = JSON.parse(data);
        if (msg.type === 'pong') return; // swallow heartbeat responses
        this.dispatchEvent(new CustomEvent('message', { detail: msg }));
      } catch {
        this.dispatchEvent(new CustomEvent('message', { detail: { raw: data } }));
      }
    };

    this.#ws.onclose = ({ code, reason, wasClean }) => {
      clearInterval(this.#pingTimer);
      this.dispatchEvent(new CustomEvent('close', { detail: { code, reason, wasClean } }));
      if (!this.#manual && code !== 1000) this.#scheduleReconnect();
    };

    this.#ws.onerror = (err) => {
      this.dispatchEvent(new CustomEvent('error', { detail: err }));
    };
  }

  #scheduleReconnect() {
    const jitter = Math.random() * 500;
    const delay  = Math.min(this.#delay * this.#reconnectFactor ** this.#attempts, this.#maxDelay) + jitter;
    this.#attempts++;

    this.dispatchEvent(new CustomEvent('reconnecting', {
      detail: { attempt: this.#attempts, delay },
    }));

    setTimeout(() => {
      if (!this.#manual) this.#openSocket();
    }, delay);
  }

  send(data) {
    const msg = typeof data === 'string' ? data : JSON.stringify(data);
    if (this.#ws?.readyState === WebSocket.OPEN) {
      this.#ws.send(msg);
    } else {
      this.#pending.push(msg); // queue for when connected
    }
    return this;
  }

  close(code = 1000, reason = 'Normal closure') {
    this.#manual = true;
    clearInterval(this.#pingTimer);
    this.#ws?.close(code, reason);
  }

  get connected()    { return this.#ws?.readyState === WebSocket.OPEN; }
  get bufferedCount(){ return this.#pending.length; }
}

// Usage
const ws = new WebSocketClient('wss://api.example.com/ws', { maxDelay: 60_000 });
ws.addEventListener('open',         () => ws.send({ type: 'auth', token: getToken() }));
ws.addEventListener('message',      ({ detail }) => handleMessage(detail));
ws.addEventListener('reconnecting', ({ detail }) => showStatus(`Reconnecting... (${detail.attempt})`));
ws.addEventListener('close',        () => showStatus('Disconnected'));
ws.connect();
```

### 25.2 Server-Sent Events (SSE)

```js
class SSEClient extends EventTarget {
  #url; #source; #manual = false; #retryDelay;

  constructor(url, { retryDelay = 3000 } = {}) {
    super();
    this.#url = url;
    this.#retryDelay = retryDelay;
  }

  connect() {
    this.#manual = false;
    this.#open();
    return this;
  }

  #open() {
    this.#source = new EventSource(this.#url, { withCredentials: true });

    this.#source.onopen = () => {
      this.dispatchEvent(new Event('open'));
    };

    this.#source.onerror = () => {
      if (this.#source.readyState === EventSource.CLOSED && !this.#manual) {
        setTimeout(() => this.#open(), this.#retryDelay);
        this.dispatchEvent(new Event('reconnecting'));
      }
    };

    // Default message event
    this.#source.onmessage = ({ data, lastEventId }) => {
      try {
        this.dispatchEvent(new CustomEvent('message', {
          detail: { data: JSON.parse(data), id: lastEventId },
        }));
      } catch {
        this.dispatchEvent(new CustomEvent('message', { detail: { data, id: lastEventId } }));
      }
    };
  }

  // Listen to named server events: `event: orderUpdate\ndata:{...}\n\n`
  on(eventName, handler) {
    this.#source?.addEventListener(eventName, ({ data, lastEventId }) => {
      try { handler(JSON.parse(data), lastEventId); }
      catch { handler(data, lastEventId); }
    });
    return this;
  }

  close() {
    this.#manual = true;
    this.#source?.close();
    this.#source = null;
  }
}

const sse = new SSEClient('/api/events');
sse.connect()
   .on('orderUpdate',   data => updateOrderStatus(data))
   .on('notification',  data => showNotification(data.message))
   .on('priceChange',   data => updatePrice(data.productId, data.price));
```

---

## 26. File API

### 26.1 Open, Read and Save Files

```js
// Modern file picker
async function openFile(options = {}) {
  if ('showOpenFilePicker' in window) {
    try {
      const [handle] = await window.showOpenFilePicker({
        multiple: false,
        ...options,
      });
      return handle.getFile();
    } catch (err) {
      if (err.name === 'AbortError') return null;
      throw err;
    }
  }
  // Fallback: classic input
  return new Promise(resolve => {
    const input = Object.assign(document.createElement('input'), { type: 'file' });
    if (options.types) input.accept = options.types.flatMap(t => Object.values(t.accept ?? {})).flat().join(',');
    input.addEventListener('change', () => resolve(input.files[0] ?? null), { once: true });
    input.click();
  });
}

async function openMultipleFiles(options = {}) {
  if ('showOpenFilePicker' in window) {
    try {
      const handles = await window.showOpenFilePicker({ multiple: true, ...options });
      return Promise.all(handles.map(h => h.getFile()));
    } catch (err) { if (err.name === 'AbortError') return []; throw err; }
  }
  return new Promise(resolve => {
    const input = Object.assign(document.createElement('input'), { type:'file', multiple:true });
    input.addEventListener('change', () => resolve([...input.files]), { once: true });
    input.click();
  });
}

// File reading — use modern Blob methods
const readFile = {
  text:    (file, encoding = 'UTF-8') => file.text(),
  json:    async file => JSON.parse(await file.text()),
  buffer:  file => file.arrayBuffer(),
  url:     file => {
    const url = URL.createObjectURL(file);
    // IMPORTANT: call URL.revokeObjectURL(url) when done to free memory
    return url;
  },
  lines:   async file => (await file.text()).split('\n'),
  csv:     async file => {
    const text   = await file.text();
    const [header, ...rows] = text.trim().split('\n');
    const keys   = header.split(',').map(k => k.trim().replace(/^"|"$/g, ''));
    return rows.map(row => {
      const vals = row.match(/(".*?"|[^,]+)(?=,|$)/g) ?? [];
      return Object.fromEntries(keys.map((k, i) => [k, (vals[i] ?? '').replace(/^"|"$/g, '')]));
    });
  },
};

// Save file
async function saveFile(content, filename, mimeType = 'text/plain') {
  if ('showSaveFilePicker' in window) {
    try {
      const handle   = await window.showSaveFilePicker({ suggestedName: filename });
      const writable = await handle.createWritable();
      const blob     = content instanceof Blob ? content : new Blob([content], { type: mimeType });
      await writable.write(blob);
      await writable.close();
      return;
    } catch (err) { if (err.name === 'AbortError') return; }
  }
  // Fallback download
  const blob = content instanceof Blob ? content : new Blob([content], { type: mimeType });
  const url  = URL.createObjectURL(blob);
  Object.assign(document.createElement('a'), { href: url, download: filename }).click();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

// Save JSON
await saveFile(JSON.stringify(data, null, 2), 'export.json', 'application/json');
```

### 26.2 Drag and Drop with Directory Support

```js
class FileDropZone {
  #el; #onFiles; #controller;

  constructor(el, onFiles, options = {}) {
    this.#el = el;
    this.#onFiles = onFiles;
    this.#controller = new AbortController();
    this.#setup(options);
  }

  #setup({ accept } = {}) {
    const { signal } = this.#controller;
    const el = this.#el;

    el.addEventListener('dragenter', e => {
      e.preventDefault();
      el.classList.add('drag-active');
    }, { signal });

    el.addEventListener('dragover', e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'copy';
    }, { signal });

    el.addEventListener('dragleave', e => {
      if (!el.contains(e.relatedTarget)) el.classList.remove('drag-active');
    }, { signal });

    el.addEventListener('drop', async e => {
      e.preventDefault();
      el.classList.remove('drag-active');

      const files = await this.#extractFiles(e.dataTransfer);
      const filtered = accept
        ? files.filter(f => accept.split(',').some(t => {
            t = t.trim();
            return t.startsWith('.') ? f.name.endsWith(t) : f.type.match(t.replace('*','.*'));
          }))
        : files;

      if (filtered.length) this.#onFiles(filtered);
    }, { signal });
  }

  async #extractFiles(dataTransfer) {
    if (dataTransfer.items) {
      const files = [];
      for (const item of dataTransfer.items) {
        if (item.kind !== 'file') continue;
        const entry = item.webkitGetAsEntry?.();
        if (entry?.isDirectory) {
          files.push(...await this.#readDirectory(entry));
        } else {
          const f = item.getAsFile();
          if (f) files.push(f);
        }
      }
      return files;
    }
    return [...(dataTransfer.files ?? [])];
  }

  async #readDirectory(dirEntry) {
    const files = [];
    const reader = dirEntry.createReader();
    await new Promise(resolve => {
      const readBatch = () => reader.readEntries(async entries => {
        if (!entries.length) return resolve();
        for (const e of entries) {
          if (e.isFile) {
            const f = await new Promise(r => e.file(r));
            files.push(f);
          } else if (e.isDirectory) {
            files.push(...await this.#readDirectory(e));
          }
        }
        readBatch();
      });
      readBatch();
    });
    return files;
  }

  destroy() { this.#controller.abort(); }
}

// Usage
const dropZone = new FileDropZone(
  document.querySelector('#upload-area'),
  files => uploadFiles(files),
  { accept: '.jpg,.jpeg,.png,.gif,image/*' }
);
```

---

## 27. Form Validation

```js
class FormValidator {
  #form; #rules; #errors = new Map(); #dirty = new Set();

  constructor(form, rules) {
    this.#form  = form;
    this.#rules = rules;
  }

  // Rule builders
  static R = {
    required:  (msg = 'This field is required')  => v => v.trim().length > 0 || msg,
    minLength: (n, msg)                           => v => v.length >= n || (msg ?? `Minimum ${n} characters`),
    maxLength: (n, msg)                           => v => v.length <= n || (msg ?? `Maximum ${n} characters`),
    min:       (n, msg)                           => v => +v >= n        || (msg ?? `Must be at least ${n}`),
    max:       (n, msg)                           => v => +v <= n        || (msg ?? `Must be at most ${n}`),
    pattern:   (re, msg = 'Invalid format')       => v => re.test(v)     || msg,
    email:     (msg = 'Invalid email address')    => v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) || msg,
    url:       (msg = 'Invalid URL')              => v => { try { new URL(v); return true; } catch { return msg; } },
    match:     (otherField, msg = 'Does not match') => (v, data) => v === data[otherField] || msg,
    oneOf:     (opts, msg)                        => v => opts.includes(v) || (msg ?? `Must be one of: ${opts.join(', ')}`),
    custom:    fn => fn,
  };

  validate() {
    const data = Object.fromEntries(new FormData(this.#form));
    this.#errors.clear();

    for (const [name, rules] of Object.entries(this.#rules)) {
      for (const rule of rules) {
        const result = rule(data[name] ?? '', data);
        if (result !== true && result) { this.#errors.set(name, result); break; }
      }
    }

    this.#applyAll();
    return {
      valid: this.#errors.size === 0,
      data,
      errors: Object.fromEntries(this.#errors),
    };
  }

  watch() {
    const getData = () => Object.fromEntries(new FormData(this.#form));
    this.#form.querySelectorAll('[name]').forEach(field => {
      field.addEventListener('blur', () => {
        this.#dirty.add(field.name);
        this.#validateField(field, getData());
      });
      field.addEventListener('input', () => {
        if (this.#dirty.has(field.name)) {
          this.#validateField(field, getData());
        }
      });
    });
    return this;
  }

  #validateField(field, data) {
    const rules = this.#rules[field.name];
    if (!rules) return;
    let error = null;
    for (const rule of rules) {
      const r = rule(field.value, data);
      if (r !== true && r) { error = r; break; }
    }
    error ? this.#errors.set(field.name, error) : this.#errors.delete(field.name);
    this.#applyField(field, error);
  }

  #applyAll() {
    this.#form.querySelectorAll('[name]').forEach(f =>
      this.#applyField(f, this.#errors.get(f.name) ?? null)
    );
  }

  #applyField(field, error) {
    field.classList.toggle('is-invalid', !!error);
    field.classList.toggle('is-valid', !error && this.#dirty.has(field.name));
    field.setAttribute('aria-invalid', String(!!error));

    const container = field.closest('.field') ?? field.parentElement;
    let errorEl = container?.querySelector('[data-field-error]');
    if (!errorEl && container) {
      errorEl = Object.assign(document.createElement('p'), { className: 'field-error' });
      errorEl.dataset.fieldError = field.name;
      errorEl.setAttribute('role', 'alert');
      errorEl.setAttribute('aria-live', 'polite');
      container.append(errorEl);
    }
    if (errorEl) { errorEl.textContent = error ?? ''; errorEl.hidden = !error; }

    if (error) field.setAttribute('aria-describedby', errorEl?.id || (errorEl && (errorEl.id = `err-${field.name}`)|| ''));
  }
}

// Usage
const { R } = FormValidator;

const validator = new FormValidator(
  document.querySelector('#signup-form'),
  {
    username: [R.required(), R.minLength(3), R.maxLength(20), R.pattern(/^\w+$/, 'Letters, numbers and _ only')],
    email:    [R.required(), R.email()],
    password: [R.required(), R.minLength(8), R.pattern(/[A-Z]/, 'Must contain uppercase'), R.pattern(/\d/, 'Must contain a number')],
    confirm:  [R.required(), R.match('password', 'Passwords do not match')],
    age:      [R.required(), R.min(18, 'Must be 18 or older'), R.max(120)],
  }
).watch();

document.querySelector('#signup-form').addEventListener('submit', e => {
  e.preventDefault();
  const { valid, data, errors } = validator.validate();
  if (valid) submitRegistration(data);
  else console.log('Errors:', errors);
});
```

---

## 28. Iterator Protocol and Generators

### 28.1 Custom Iterables

```js
// Implement [Symbol.iterator] to make any object iterable
class Range {
  constructor(start, end, step = 1) {
    this.start = start; this.end = end; this.step = step;
  }

  [Symbol.iterator]() {
    let current = this.start;
    const { end, step } = this;
    return {
      next() {
        if ((step > 0 && current < end) || (step < 0 && current > end)) {
          const value = current;
          current += step;
          return { value, done: false };
        }
        return { value: undefined, done: true };
      },
      [Symbol.iterator]() { return this; }, // make iterator itself iterable
    };
  }

  toArray() { return [...this]; }

  // Make Range work with all array-like operations
  map(fn)    { return [...this].map(fn); }
  filter(fn) { return [...this].filter(fn); }
  reduce(fn, init) { return [...this].reduce(fn, init); }
}

[...new Range(1, 10, 2)];          // [1,3,5,7,9]
[...new Range(10, 0, -2)];         // [10,8,6,4,2]
for (const n of new Range(1, 5))   { console.log(n); }
const [a2, b2, c2] = new Range(0, 3);  // destructuring

// Infinite sequence — use take() to consume lazily
class InfiniteCounter {
  constructor(start = 0, step = 1) { this.n = start; this.step = step; }
  [Symbol.iterator]() {
    let n = this.n; const step = this.step;
    return { next: () => ({ value: n, done: false, _: n += step }), [Symbol.iterator]() { return this; } };
  }
}

// Take first N items from any iterable
function* take(iterable, n) {
  let count = 0;
  for (const item of iterable) {
    if (count++ >= n) break;
    yield item;
  }
}

[...take(new InfiniteCounter(0, 2), 5)]; // [0,2,4,6,8]
```

### 28.2 Generator Functions

```js
// Generator: pauseable function — each yield suspends execution
function* fibonacci() {
  let [a, b] = [0, 1];
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// Consume lazily
const fib = fibonacci();
fib.next().value; // 0
fib.next().value; // 1
fib.next().value; // 1
fib.next().value; // 2

// Take first N fibonacci numbers
[...take(fibonacci(), 10)]; // [0,1,1,2,3,5,8,13,21,34]

// yield* — delegate to another iterable
function* flatten(arr) {
  for (const item of arr) {
    if (Array.isArray(item)) yield* flatten(item); // recurse
    else yield item;
  }
}
[...flatten([1,[2,[3,[4,5]]]])]; // [1,2,3,4,5]

// Generator with input (two-way communication)
function* calculator() {
  let result = 0;
  while (true) {
    const [op, value] = yield result;
    if (op === '+') result += value;
    if (op === '-') result -= value;
    if (op === '*') result *= value;
    if (op === '/') result /= value;
    if (op === 'reset') result = 0;
  }
}
const calc = calculator();
calc.next();             // start: { value: 0, done: false }
calc.next(['+', 10]);   // { value: 10 }
calc.next(['*', 3]);    // { value: 30 }
calc.next(['-', 5]);    // { value: 25 }

// Async generator — for data streams and pagination
async function* paginatedFetch(url, { pageSize = 20 } = {}) {
  let page = 1;
  while (true) {
    const response = await fetch(`${url}?page=${page}&limit=${pageSize}`);
    const { data, totalPages } = await response.json();
    yield* data;
    if (page++ >= totalPages) return;
  }
}

for await (const user of paginatedFetch('/api/users')) {
  processUser(user); // one at a time, fetches next page when needed
}

// Collect all
const allUsers = [];
for await (const user of paginatedFetch('/api/users')) allUsers.push(user);
```

---

## 29. Proxy and Reflect

### 29.1 Core Proxy Patterns

```js
// Complete trap reference
const fullHandler = {
  get(target, prop, receiver)               { return Reflect.get(target, prop, receiver); },
  set(target, prop, value, receiver)        { return Reflect.set(target, prop, value, receiver); },
  has(target, prop)                         { return Reflect.has(target, prop); },
  deleteProperty(target, prop)              { return Reflect.deleteProperty(target, prop); },
  apply(target, thisArg, args)              { return Reflect.apply(target, thisArg, args); },
  construct(target, args, newTarget)        { return Reflect.construct(target, args, newTarget); },
  defineProperty(target, prop, descriptor) { return Reflect.defineProperty(target, prop, descriptor); },
  getOwnPropertyDescriptor(target, prop)   { return Reflect.getOwnPropertyDescriptor(target, prop); },
  getPrototypeOf(target)                   { return Reflect.getPrototypeOf(target); },
  setPrototypeOf(target, proto)            { return Reflect.setPrototypeOf(target, proto); },
  isExtensible(target)                     { return Reflect.isExtensible(target); },
  preventExtensions(target)               { return Reflect.preventExtensions(target); },
  ownKeys(target)                          { return Reflect.ownKeys(target); },
};

// ── Schema validation proxy ───────────────────────────────
function createModel(schema) {
  const data = {};
  return new Proxy(data, {
    set(target, key, value) {
      const rule = schema[key];
      if (!rule) throw new Error(`Unknown field: ${String(key)}`);
      if (rule.required && (value == null || value === ''))
        throw new Error(`${String(key)} is required`);
      if (rule.type && typeof value !== rule.type)
        throw new TypeError(`${String(key)} must be type '${rule.type}', got '${typeof value}'`);
      if (rule.validate && !rule.validate(value))
        throw new Error(`${String(key)} failed validation`);
      return Reflect.set(target, key, value);
    },
    get(target, key) {
      if (!(key in schema) && typeof key !== 'symbol') {
        throw new Error(`Unknown field: ${String(key)}`);
      }
      return Reflect.get(target, key);
    },
  });
}

const user = createModel({
  name:  { type: 'string', required: true },
  age:   { type: 'number', validate: v => v >= 0 && v <= 150 },
  email: { type: 'string', validate: v => /\S+@\S+\.\S+/.test(v) },
});
user.name = 'Alice';   // OK
user.age  = -1;        // Error: age failed validation

// ── Logging/debugging proxy ───────────────────────────────
function logged(target, name = 'obj') {
  return new Proxy(target, {
    get(t, key) {
      const val = Reflect.get(t, key);
      if (typeof val === 'function') {
        return (...args) => {
          console.log(`${name}.${String(key)}(${args.map(a=>JSON.stringify(a)).join(',')})`);
          return val.apply(t, args);
        };
      }
      console.log(`GET ${name}.${String(key)} →`, val);
      return val;
    },
    set(t, key, val) {
      console.log(`SET ${name}.${String(key)} =`, val);
      return Reflect.set(t, key, val);
    },
  });
}

// ── Immutable proxy (deep) ────────────────────────────────
function immutable(obj) {
  return new Proxy(obj, {
    set()            { throw new TypeError('Object is immutable'); },
    deleteProperty() { throw new TypeError('Object is immutable'); },
    get(t, k) {
      const v = Reflect.get(t, k);
      return v && typeof v === 'object' ? immutable(v) : v;
    },
  });
}

// ── Default value proxy ───────────────────────────────────
function withDefaults(obj, defaultValue) {
  return new Proxy(obj, {
    get: (t, k) => Reflect.has(t, k) ? Reflect.get(t, k) : defaultValue,
  });
}
const counter = withDefaults({}, 0);
counter.a++;          // 1 (0 + 1)
counter.b += 5;       // 5 (0 + 5)
```

---

## 30. Streams API

### 30.1 ReadableStream, WritableStream, TransformStream

```js
// Custom ReadableStream — push model
const timerStream = (intervalMs, count) => new ReadableStream({
  start(controller) {
    let i = 0;
    const id = setInterval(() => {
      if (i >= count) { controller.close(); clearInterval(id); return; }
      controller.enqueue({ tick: i++, ts: Date.now() });
    }, intervalMs);
    return () => clearInterval(id); // cancel callback
  },
});

// Consume with for-await
for await (const tick of timerStream(1000, 5)) {
  console.log(tick); // { tick: 0, ts: ... } ... { tick: 4, ts: ... }
}

// TransformStream — process chunks as they pass through
class JSONLinesTransform extends TransformStream {
  constructor() {
    let buffer = '';
    super({
      transform(chunk, controller) {
        buffer += chunk;
        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';
        for (const line of lines.filter(Boolean)) {
          try { controller.enqueue(JSON.parse(line)); }
          catch { /* skip malformed lines */ }
        }
      },
      flush(controller) {
        if (buffer.trim()) {
          try { controller.enqueue(JSON.parse(buffer)); } catch {}
        }
      },
    });
  }
}

// WritableStream — consume data
const logStream = new WritableStream({
  write(chunk) { console.log('Received:', chunk); },
  close()      { console.log('Stream closed'); },
  abort(reason){ console.error('Stream aborted:', reason); },
});

// Pipeline: fetch → decode → parse NDJSON → log
const response = await fetch('/api/stream');
await response.body
  .pipeThrough(new TextDecoderStream())
  .pipeThrough(new JSONLinesTransform())
  .pipeTo(logStream);

// Fetch with download progress
async function downloadWithProgress(url, onProgress) {
  const response = await fetch(url);
  const total    = Number(response.headers.get('Content-Length') ?? 0);
  let loaded     = 0;

  const progressStream = new TransformStream({
    transform(chunk, controller) {
      loaded += chunk.length;
      onProgress({
        loaded,
        total,
        percent: total ? (loaded / total * 100).toFixed(1) : 0,
        done: loaded >= total,
      });
      controller.enqueue(chunk);
    },
  });

  // Return new Response with progress tracking
  return new Response(response.body.pipeThrough(progressStream), {
    headers: response.headers,
    status:  response.status,
  });
}

// Tee: duplicate a stream (read it twice)
const [s1, s2] = response.body.tee();
// Both s1 and s2 receive all data independently
```

## 31. Crypto API

```js
// Cryptographically secure random values
crypto.randomUUID();                              // UUID v4 string
crypto.getRandomValues(new Uint8Array(32));       // 32 random bytes

// Safe random integer (uniform distribution)
function randomInt(min, max) {
  const range = max - min + 1;
  const bytes = Math.ceil(Math.log2(range) / 8);
  const max32 = Math.floor(0x100**bytes / range) * range;
  let n;
  do { n = [...crypto.getRandomValues(new Uint8Array(bytes))].reduce((a,b,i) => a+b*256**i, 0); }
  while (n >= max32);
  return min + (n % range);
}

// SHA-256 hash
async function sha256(data) {
  const encoded = typeof data === 'string' ? new TextEncoder().encode(data) : data;
  const hash    = await crypto.subtle.digest('SHA-256', encoded);
  return [...new Uint8Array(hash)].map(b => b.toString(16).padStart(2,'0')).join('');
}

// AES-GCM encryption
const AES = {
  generateKey: () => crypto.subtle.generateKey({ name:'AES-GCM', length:256 }, true, ['encrypt','decrypt']),

  async encrypt(plaintext, key) {
    const iv  = crypto.getRandomValues(new Uint8Array(12)); // 96-bit IV for GCM
    const enc = await crypto.subtle.encrypt({ name:'AES-GCM', iv }, key,
      new TextEncoder().encode(JSON.stringify(plaintext)));
    const out = new Uint8Array(12 + enc.byteLength);
    out.set(iv); out.set(new Uint8Array(enc), 12);
    return btoa(String.fromCharCode(...out));
  },

  async decrypt(ciphertext, key) {
    const data = Uint8Array.from(atob(ciphertext), c => c.charCodeAt(0));
    const dec  = await crypto.subtle.decrypt({ name:'AES-GCM', iv: data.slice(0,12) }, key, data.slice(12));
    return JSON.parse(new TextDecoder().decode(dec));
  },

  // Derive a key from a password using PBKDF2
  async deriveKey(password, salt = crypto.getRandomValues(new Uint8Array(16))) {
    const rawKey = await crypto.subtle.importKey(
      'raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveKey']
    );
    const key = await crypto.subtle.deriveKey(
      { name:'PBKDF2', salt, iterations: 310_000, hash:'SHA-256' },
      rawKey,
      { name:'AES-GCM', length:256 },
      true, ['encrypt','decrypt']
    );
    return { key, salt: [...salt].map(b=>b.toString(16).padStart(2,'0')).join('') };
  },
};

// Usage
const key       = await AES.generateKey();
const ciphertext = await AES.encrypt({ secret: 'my data' }, key);
const plaintext  = await AES.decrypt(ciphertext, key);
```

---

## 32. Audio API

```js
class AudioEngine {
  #ctx; #masterGain; #analyser;

  constructor() {
    this.#ctx        = new (window.AudioContext ?? window.webkitAudioContext)();
    this.#masterGain = this.#ctx.createGain();
    this.#analyser   = this.#ctx.createAnalyser();
    this.#analyser.fftSize = 2048;

    this.#masterGain.connect(this.#analyser);
    this.#analyser.connect(this.#ctx.destination);
  }

  // Must be called after user gesture (browser policy)
  async resume() {
    if (this.#ctx.state === 'suspended') await this.#ctx.resume();
  }

  // Load and decode audio file
  async loadBuffer(url) {
    const response = await fetch(url);
    const buffer   = await response.arrayBuffer();
    return this.#ctx.decodeAudioData(buffer);
  }

  // Play a decoded buffer
  play(buffer, { volume = 1, loop = false, when = 0, onEnded } = {}) {
    const source = this.#ctx.createBufferSource();
    const gain   = this.#ctx.createGain();

    source.buffer = buffer;
    source.loop   = loop;
    gain.gain.value = volume;

    source.connect(gain);
    gain.connect(this.#masterGain);
    source.start(this.#ctx.currentTime + when);

    if (onEnded) source.addEventListener('ended', onEnded, { once: true });

    return {
      stop: () => source.stop(),
      source, gain,
      fadeOut: (duration = 0.5) => {
        gain.gain.linearRampToValueAtTime(0, this.#ctx.currentTime + duration);
        setTimeout(() => source.stop(), duration * 1000);
      },
    };
  }

  // Synthesize a tone
  tone(frequency = 440, type = 'sine', duration = 0.5, volume = 0.3) {
    const osc = this.#ctx.createOscillator();
    const env = this.#ctx.createGain();
    const now = this.#ctx.currentTime;

    osc.type = type;
    osc.frequency.value = frequency;

    // ADSR envelope
    env.gain.setValueAtTime(0, now);
    env.gain.linearRampToValueAtTime(volume, now + 0.01);    // Attack
    env.gain.linearRampToValueAtTime(volume * 0.7, now + 0.1); // Decay
    env.gain.setValueAtTime(volume * 0.7, now + duration - 0.05);
    env.gain.linearRampToValueAtTime(0, now + duration);     // Release

    osc.connect(env);
    env.connect(this.#masterGain);
    osc.start(now);
    osc.stop(now + duration + 0.1);
    return osc;
  }

  // Get frequency data for visualizers
  getFrequencyData() {
    const data = new Uint8Array(this.#analyser.frequencyBinCount);
    this.#analyser.getByteFrequencyData(data);
    return data;
  }

  set masterVolume(v) { this.#masterGain.gain.value = Math.max(0, Math.min(1, v)); }
  get masterVolume()  { return this.#masterGain.gain.value; }
  get currentTime()   { return this.#ctx.currentTime; }
}
```

---

## 33. Canvas API

```js
// HiDPI-correct canvas setup
function setupCanvas(canvas, { width, height } = {}) {
  const dpr = window.devicePixelRatio ?? 1;
  const ctx = canvas.getContext('2d');

  function resize() {
    const w = width  ?? canvas.parentElement?.clientWidth  ?? canvas.offsetWidth;
    const h = height ?? canvas.parentElement?.clientHeight ?? canvas.offsetHeight;
    canvas.width  = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width  = `${w}px`;
    canvas.style.height = `${h}px`;
    ctx.scale(dpr, dpr);
    return { width: w, height: h };
  }

  const dims = resize();
  if (!width || !height) new ResizeObserver(resize).observe(canvas.parentElement ?? canvas);

  return { ctx, dpr, ...dims };
}

// Game loop / animation loop
class CanvasApp {
  #canvas; #ctx; #raf = null; #lastTime = 0; #dpr;

  constructor(canvas) {
    const setup   = setupCanvas(canvas);
    this.#canvas  = canvas;
    this.#ctx     = setup.ctx;
    this.#dpr     = setup.dpr;
    this.width    = setup.width;
    this.height   = setup.height;
  }

  start() {
    const loop = (timestamp) => {
      const dt = Math.min(timestamp - this.#lastTime, 100); // cap at 100ms
      this.#lastTime = timestamp;
      this.#ctx.clearRect(0, 0, this.width, this.height);
      this.update(dt / 1000); // delta in seconds
      this.draw(this.#ctx);
      this.#raf = requestAnimationFrame(loop);
    };
    this.#raf = requestAnimationFrame(loop);
    return this;
  }

  stop() { cancelAnimationFrame(this.#raf); this.#raf = null; }

  // Override in subclass:
  update(dt) {}
  draw(ctx)  {}
}

// Drawing utilities
const draw = {
  roundRect(ctx, x, y, w, h, r = 4) {
    if (ctx.roundRect) { ctx.beginPath(); ctx.roundRect(x,y,w,h,r); ctx.closePath(); }
    else {
      ctx.beginPath();
      ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.arcTo(x+w,y,x+w,y+r,r);
      ctx.lineTo(x+w,y+h-r); ctx.arcTo(x+w,y+h,x+w-r,y+h,r);
      ctx.lineTo(x+r,y+h); ctx.arcTo(x,y+h,x,y+h-r,r);
      ctx.lineTo(x,y+r); ctx.arcTo(x,y,x+r,y,r); ctx.closePath();
    }
  },
  circle: (ctx,x,y,r) => { ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.closePath(); },
  line:   (ctx,x0,y0,x1,y1) => { ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.stroke(); },
  text:   (ctx,t,x,y,{font,color,align='left',baseline='top',maxWidth}={}) => {
    if(font)  ctx.font=font;
    if(color) ctx.fillStyle=color;
    ctx.textAlign=align; ctx.textBaseline=baseline;
    maxWidth ? ctx.fillText(t,x,y,maxWidth) : ctx.fillText(t,x,y);
  },
  linearGradient: (ctx,x0,y0,x1,y1,stops) => {
    const g = ctx.createLinearGradient(x0,y0,x1,y1);
    stops.forEach(([p,c]) => g.addColorStop(p,c));
    return g;
  },
};

// Export canvas as image
function canvasToBlob(canvas, type = 'image/png', quality = 0.92) {
  return new Promise(resolve => canvas.toBlob(resolve, type, quality));
}
async function downloadCanvas(canvas, filename = 'image.png') {
  const blob = await canvasToBlob(canvas);
  saveFile(blob, filename, 'image/png');
}
```

---

## 34. Pointer, Touch and Keyboard Events

### 34.1 Unified Pointer Events

```js
// Pointer Events: single API for mouse, touch, and stylus
function makeDraggable(el, { onStart, onMove, onEnd, onCancel } = {}) {
  const ctrl = new AbortController();
  const { signal } = ctrl;
  let pointerId = null, startX, startY;

  el.style.touchAction = 'none'; // prevent browser handling touch for scroll

  el.addEventListener('pointerdown', e => {
    el.setPointerCapture(e.pointerId); // track even outside element bounds
    pointerId = e.pointerId;
    startX = e.clientX; startY = e.clientY;
    el.classList.add('dragging');
    onStart?.({ x: e.clientX, y: e.clientY, event: e });
  }, { signal });

  el.addEventListener('pointermove', e => {
    if (e.pointerId !== pointerId) return;
    onMove?.({
      dx: e.clientX - startX,
      dy: e.clientY - startY,
      x:  e.clientX,
      y:  e.clientY,
      pressure: e.pressure, // 0.0–1.0 for stylus
      event: e,
    });
  }, { signal });

  el.addEventListener('pointerup', e => {
    if (e.pointerId !== pointerId) return;
    pointerId = null;
    el.classList.remove('dragging');
    onEnd?.({ x: e.clientX, y: e.clientY, event: e });
  }, { signal });

  el.addEventListener('pointercancel', e => {
    pointerId = null;
    el.classList.remove('dragging');
    onCancel?.({ event: e });
  }, { signal });

  return () => ctrl.abort();
}

// Swipe detection
function detectSwipe(el, { threshold = 50, onSwipe } = {}) {
  let start = null;
  const ctrl = new AbortController();
  const { signal } = ctrl;

  el.addEventListener('touchstart', ({ touches: [t] }) => {
    start = { x: t.clientX, y: t.clientY, time: Date.now() };
  }, { signal, passive: true });

  el.addEventListener('touchend', ({ changedTouches: [t] }) => {
    if (!start) return;
    const dx = t.clientX - start.x;
    const dy = t.clientY - start.y;
    const dt = Date.now() - start.time;
    const dist = Math.hypot(dx, dy);

    if (dist >= threshold && dt < 500) {
      const direction = Math.abs(dx) > Math.abs(dy)
        ? (dx > 0 ? 'right' : 'left')
        : (dy > 0 ? 'down'  : 'up');
      onSwipe?.({ direction, distance: dist, velocity: dist/dt, dx, dy });
    }
    start = null;
  }, { signal, passive: true });

  return () => ctrl.abort();
}
```

### 34.2 Keyboard Shortcuts Manager

```js
class ShortcutManager {
  #shortcuts = new Map();
  #ctrl;

  constructor() {
    this.#ctrl = new AbortController();
    document.addEventListener('keydown', this.#onKeydown.bind(this), {
      signal: this.#ctrl.signal,
    });
  }

  register(combo, handler, { description = '', preventDefault = true, disabled = false } = {}) {
    const key = this.#normalizeCombo(combo);
    this.#shortcuts.set(key, { handler, description, preventDefault, disabled });
    return () => this.#shortcuts.delete(key); // returns unregister function
  }

  #normalizeCombo(combo) {
    return combo.toLowerCase()
      .split('+')
      .map(k => k.trim())
      .sort()
      .join('+');
  }

  #onKeydown(e) {
    // Don't fire shortcuts when typing in inputs
    const tag = e.target.tagName;
    if (['INPUT','TEXTAREA','SELECT'].includes(tag) && !e.target.dataset.shortcutsEnabled) {
      // Allow Escape to exit inputs
      if (e.key !== 'Escape') return;
    }

    const parts = [];
    if (e.ctrlKey || e.metaKey) parts.push('ctrl');
    if (e.shiftKey) parts.push('shift');
    if (e.altKey)   parts.push('alt');
    parts.push(e.key.toLowerCase());

    const shortcut = this.#shortcuts.get(parts.sort().join('+'));
    if (!shortcut || shortcut.disabled) return;

    if (shortcut.preventDefault) e.preventDefault();
    shortcut.handler(e);
  }

  getAll() {
    return Object.fromEntries(
      [...this.#shortcuts.entries()]
        .filter(([, s]) => !s.disabled)
        .map(([key, s]) => [key, s.description])
    );
  }

  destroy() { this.#ctrl.abort(); }
}

const shortcuts = new ShortcutManager();
shortcuts.register('ctrl+s',       () => saveDocument(),   { description: 'Save document' });
shortcuts.register('ctrl+z',       () => history.undo(),   { description: 'Undo' });
shortcuts.register('ctrl+shift+z', () => history.redo(),   { description: 'Redo' });
shortcuts.register('ctrl+/',       () => toggleHelp(),     { description: 'Show shortcuts' });
shortcuts.register('escape',       () => closeModal(),     { description: 'Close dialog' });
shortcuts.register('/',            () => focusSearch(),    { description: 'Focus search' });
```

---

## 35. BroadcastChannel and SharedWorker

```js
// ── BroadcastChannel: one-to-many tab communication ───────
class TabSync {
  #channel; #handlers = new Map(); #id;

  constructor(channelName = 'app') {
    this.#channel = new BroadcastChannel(channelName);
    this.#id      = crypto.randomUUID(); // unique tab ID

    this.#channel.addEventListener('message', ({ data }) => {
      if (data.senderId === this.#id) return; // ignore own messages
      this.#handlers.get(data.type)?.forEach(fn => fn(data.payload, data.senderId));
    });
  }

  on(type, fn) {
    if (!this.#handlers.has(type)) this.#handlers.set(type, new Set());
    this.#handlers.get(type).add(fn);
    return () => this.#handlers.get(type)?.delete(fn);
  }

  emit(type, payload) {
    this.#channel.postMessage({ type, payload, senderId: this.#id, ts: Date.now() });
  }

  request(type, payload, timeout = 5000) {
    return new Promise((resolve, reject) => {
      const replyType = `${type}:reply:${crypto.randomUUID()}`;
      const timer = setTimeout(() => {
        unsubscribe();
        reject(new Error(`Timeout waiting for ${type} response`));
      }, timeout);

      const unsubscribe = this.on(replyType, (data) => {
        clearTimeout(timer);
        unsubscribe();
        resolve(data);
      });

      this.emit(type, { ...payload, replyTo: replyType });
    });
  }

  close() { this.#channel.close(); }
  get tabId() { return this.#id; }
}

const sync = new TabSync('myapp');

// Logout all tabs
logoutBtn.addEventListener('click', () => {
  clearSession();
  sync.emit('auth:logout', {});
  redirect('/login');
});
sync.on('auth:logout', () => { clearSession(); redirect('/login'); });

// Theme sync
sync.on('theme:change', ({ theme }) => Theme.apply(theme));
themeToggle.addEventListener('click', () => {
  Theme.toggle();
  sync.emit('theme:change', { theme: Theme.current });
});

// SharedWorker: shared state and computation across tabs
// shared-worker.js
const tabs = new Map(); // clientId → port
let sharedState = { activeUsers: 0, data: null };

self.addEventListener('connect', ({ ports: [port] }) => {
  const id = Math.random().toString(36).slice(2);
  tabs.set(id, port);
  sharedState.activeUsers = tabs.size;
  port.start();

  // Send current state immediately
  port.postMessage({ type: 'INIT', state: sharedState, tabId: id });

  port.addEventListener('message', ({ data }) => {
    switch (data.type) {
      case 'UPDATE':
        sharedState = { ...sharedState, ...data.payload };
        broadcast({ type: 'SYNC', state: sharedState });
        break;
      case 'GET':
        port.postMessage({ type: 'SYNC', state: sharedState });
        break;
    }
  });

  port.addEventListener('close', () => {
    tabs.delete(id);
    sharedState.activeUsers = tabs.size;
    broadcast({ type: 'SYNC', state: sharedState });
  });

  function broadcast(msg) { tabs.forEach(p => p.postMessage(msg)); }
});
```

---

## 36. Advanced State Patterns

### 36.1 Finite State Machine

```js
class StateMachine {
  #state; #transitions; #actions; #subscribers = new Set();

  constructor({ initial, transitions, actions = {} }) {
    this.#state       = initial;
    this.#transitions = transitions;
    this.#actions     = actions;
  }

  get state() { return this.#state; }

  can(event) { return !!(this.#transitions[this.#state]?.[event]); }

  send(event, payload) {
    const transition = this.#transitions[this.#state]?.[event];
    if (transition === undefined) {
      console.warn(`FSM: Invalid transition ${this.#state} + ${event}`);
      return false;
    }

    const prevState    = this.#state;
    const nextState    = typeof transition === 'function'
      ? transition(this.#state, payload)
      : transition;

    this.#state = nextState;

    // Run action hooks
    this.#actions[`${prevState}:exit`]?.(payload);
    this.#actions[`${nextState}:enter`]?.(payload);
    this.#actions[event]?.(payload);

    this.#subscribers.forEach(fn => fn({ from: prevState, to: nextState, event, payload }));
    return true;
  }

  subscribe(fn) {
    this.#subscribers.add(fn);
    return () => this.#subscribers.delete(fn);
  }

  matches(...states) { return states.includes(this.#state); }
}

// Traffic light example
const light = new StateMachine({
  initial: 'red',
  transitions: {
    red:    { GO: 'green' },
    green:  { SLOW: 'yellow' },
    yellow: { STOP: 'red' },
  },
  actions: {
    'red:enter':    () => showRed(),
    'green:enter':  () => showGreen(),
    'yellow:enter': () => showYellow(),
  },
});

// Async fetch state machine
const fetchSM = new StateMachine({
  initial: 'idle',
  transitions: {
    idle:    { FETCH: 'loading' },
    loading: { SUCCESS: 'success', ERROR: 'error', ABORT: 'idle' },
    success: { FETCH: 'loading', RESET: 'idle' },
    error:   { RETRY: 'loading', RESET: 'idle' },
  },
  actions: {
    'loading:enter': () => { showSpinner(); setResult(null); },
    'loading:exit':  () => hideSpinner(),
    SUCCESS: ({ data }) => setResult(data),
    'error:enter': ({ error }) => showError(error.message),
  },
});

async function loadData(url) {
  fetchSM.send('FETCH');
  try {
    const data = await api.get(url);
    fetchSM.send('SUCCESS', { data });
  } catch (error) {
    fetchSM.send('ERROR', { error });
  }
}
```

### 36.2 Optimistic Updates

```js
class OptimisticStore {
  #state; #subscribers = new Set(); #snapshots = new Map();

  constructor(initialState) { this.#state = structuredClone(initialState); }

  get state() { return this.#state; }

  // Apply change immediately, roll back on server failure
  async optimistic(operationId, applyFn, serverFn, { onSuccess, onError } = {}) {
    const snapshot = structuredClone(this.#state);
    this.#snapshots.set(operationId, snapshot);

    // Apply optimistically
    applyFn(this.#state);
    this.#notify();

    try {
      const result = await serverFn();
      this.#snapshots.delete(operationId);
      onSuccess?.(result);
      return result;
    } catch (err) {
      // Roll back
      const snap = this.#snapshots.get(operationId);
      if (snap) {
        Object.assign(this.#state, snap);
        this.#snapshots.delete(operationId);
        this.#notify();
      }
      onError?.(err);
      throw err;
    }
  }

  subscribe(fn) {
    this.#subscribers.add(fn);
    fn(this.#state); // emit current state immediately
    return () => this.#subscribers.delete(fn);
  }

  #notify() { this.#subscribers.forEach(fn => fn(this.#state)); }
}

const store = new OptimisticStore({ posts: [], loading: false });

async function likePost(postId) {
  await store.optimistic(
    `like:${postId}`,
    // Immediate UI change
    state => {
      const post = state.posts.find(p => p.id === postId);
      if (post) { post.liked = !post.liked; post.likes += post.liked ? 1 : -1; }
    },
    // Server call
    () => api.post(`/posts/${postId}/like`),
    {
      onError: () => toast('Failed to update like', 'error'),
    }
  );
}
```

---

## 37. Full SPA Architecture

```js
// Recommended project structure:
// src/
// ├── main.js              ← Bootstrap
// ├── router.js            ← Client-side routing
// ├── store/
// │   └── index.js         ← Global state
// ├── services/
// │   ├── api.js           ← HTTP client
// │   └── auth.service.js
// ├── components/
// │   ├── ui/              ← Reusable components
// │   └── pages/           ← Route-level pages (lazy-loaded)
// └── utils/

async function bootstrap() {
  try {
    // 1. Restore session / auth
    await AuthService.init();

    // 2. Set up router with lazy-loading
    const router = new Router();
    const loader = createPageLoader(document.querySelector('#app'));

    const publicRoutes = new Set(['/login', '/signup', '/forgot-password']);

    router
      .route('/',             () => import('./pages/HomePage.js').then(m => m.default))
      .route('/users',        () => import('./pages/UsersPage.js').then(m => m.default))
      .route('/users/:id',    () => import('./pages/UserDetailPage.js').then(m => m.default))
      .route('/settings',     () => import('./pages/SettingsPage.js').then(m => m.default))
      .route('/login',        () => import('./pages/LoginPage.js').then(m => m.default))
      .notFound(              () => import('./pages/NotFoundPage.js').then(m => m.default))
      .guard(path => {
        if (!AuthService.isLoggedIn && !publicRoutes.has(path)) {
          router.navigate('/login', {}, { replace: true });
          return false;
        }
        if (AuthService.isLoggedIn && path === '/login') {
          router.navigate('/', {}, { replace: true });
          return false;
        }
        return true;
      })
      .onChange(path => {
        document.title = getPageTitle(path);
        analytics.pageView(path);
      })
      .setPageLoader(loader)
      .start();

    // 3. Register service worker (non-blocking)
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js', { updateViaCache: 'none' })
        .catch(err => console.warn('SW registration failed:', err));
    }

  } catch (err) {
    // Fatal error — show recovery UI
    document.getElementById('app').innerHTML = `
      <div class="fatal-error" role="alert">
        <h1>Application failed to start</h1>
        <details><summary>Error details</summary><pre>${escapeHtml(err.stack)}</pre></details>
        <button onclick="location.reload()">Reload Page</button>
      </div>
    `;
    reportError({ type: 'bootstrap-failure', error: err });
  }
}

// Page loader with skeleton UI and abort support
function createPageLoader(container) {
  let activePage = null;
  let activeController = null;

  return async function loadPage(factory) {
    // Cancel previous navigation
    activeController?.abort();
    activeController = new AbortController();
    const { signal } = activeController;

    // Show skeleton immediately
    container.innerHTML = `
      <div class="page-skeleton" aria-busy="true" aria-label="Loading page">
        <div class="skel skel--title"></div>
        <div class="skel skel--text"></div>
        <div class="skel skel--text skel--short"></div>
        <div class="skel skel--block"></div>
      </div>
    `;

    try {
      // Load the page module
      const PageClass = await factory();
      if (signal.aborted) return;

      // Cleanup previous page
      activePage?.destroy?.();

      // Brief skeleton delay for perceived smoothness
      await new Promise(r => setTimeout(r, 80));
      if (signal.aborted) return;

      // Mount new page
      container.innerHTML = '';
      activePage = new PageClass();
      activePage.mount(container);

    } catch (err) {
      if (err.name === 'AbortError' || signal.aborted) return;

      container.innerHTML = `
        <div class="page-error" role="alert">
          <h2>Failed to load this page</h2>
          <p>${escapeHtml(err.message)}</p>
          <button onclick="history.back()">← Go Back</button>
          <button onclick="location.reload()">Reload</button>
        </div>
      `;
    }
  };
}

bootstrap();
```

---

## 38. Accessibility (a11y)

### 38.1 Focus Management

```js
const FOCUSABLE_SELECTOR = [
  'a[href]', 'button:not([disabled])', 'input:not([disabled])',
  'select:not([disabled])', 'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])', 'details > summary',
].join(', ');

class FocusTrap {
  #container; #previousFocus; #controller;

  constructor(container) { this.#container = container; }

  activate() {
    this.#previousFocus = document.activeElement;
    this.#controller    = new AbortController();

    document.addEventListener('keydown', this.#handleKeydown.bind(this), {
      signal: this.#controller.signal,
    });

    // Focus first focusable element or the container itself
    const firstFocusable = this.#getFocusable()[0];
    (firstFocusable ?? this.#container).focus();

    return this;
  }

  deactivate() {
    this.#controller?.abort();
    this.#previousFocus?.focus?.();
    return this;
  }

  #getFocusable() {
    return [...this.#container.querySelectorAll(FOCUSABLE_SELECTOR)]
      .filter(el =>
        !el.closest('[hidden]') &&
        !el.closest('[inert]') &&
        el.offsetParent !== null // not hidden via display:none
      );
  }

  #handleKeydown(e) {
    if (e.key !== 'Tab') return;
    const focusable = this.#getFocusable();
    if (!focusable.length) { e.preventDefault(); return; }

    const first  = focusable[0];
    const last   = focusable.at(-1);
    const active = document.activeElement;

    if (e.shiftKey && (active === first || !this.#container.contains(active))) {
      e.preventDefault(); last.focus();
    } else if (!e.shiftKey && (active === last || !this.#container.contains(active))) {
      e.preventDefault(); first.focus();
    }
  }
}

// Accessible modal with full a11y support
class Modal {
  #el; #trap; #controller;

  constructor({ title, content, onClose }) {
    this.#el = this.#buildDOM(title, content);
    this.#trap = new FocusTrap(this.#el.querySelector('[role="dialog"]'));

    this.#controller = new AbortController();
    const { signal } = this.#controller;

    const close = () => { onClose?.(); this.close(); };
    this.#el.querySelector('.modal__backdrop').addEventListener('click', close, { signal });
    this.#el.querySelector('.modal__close').addEventListener('click', close, { signal });
    document.addEventListener('keydown', e => e.key === 'Escape' && close(), { signal });
  }

  #buildDOM(title, content) {
    const wrap = document.createElement('div');
    wrap.innerHTML = `
      <div class="modal__backdrop"></div>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title-${Date.now()}"
        class="modal__dialog"
        tabindex="-1"
      >
        <div class="modal__header">
          <h2 id="modal-title-${Date.now()}" class="modal__title">${escapeHtml(title)}</h2>
          <button class="modal__close" aria-label="Close dialog">✕</button>
        </div>
        <div class="modal__body"></div>
      </div>
    `;
    wrap.querySelector('.modal__body').append(
      typeof content === 'string'
        ? Object.assign(document.createElement('div'), { innerHTML: content })
        : content
    );
    return wrap;
  }

  open() {
    document.body.append(this.#el);
    document.body.style.overflow = 'hidden';
    this.#trap.activate();
    announcer.polite('Dialog opened');
    return this;
  }

  close() {
    this.#controller.abort();
    this.#trap.deactivate();
    document.body.style.overflow = '';
    this.#el.remove();
    announcer.polite('Dialog closed');
  }
}

// Screen reader live region
const announcer = (() => {
  const create = (politeness) => {
    const el = Object.assign(document.createElement('div'), {
      role: 'status',
    });
    el.setAttribute('aria-live', politeness);
    el.setAttribute('aria-atomic', 'true');
    el.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;';
    document.body.append(el);
    return el;
  };
  const politeEl    = create('polite');
  const assertiveEl = create('assertive');
  const announce    = (el, msg) => { el.textContent=''; requestAnimationFrame(() => { el.textContent=msg; }); };
  return {
    polite:    msg => announce(politeEl, msg),    // waits for user pause
    assertive: msg => announce(assertiveEl, msg), // interrupts immediately
  };
})();
```

---

## 39. Performance Profiling and Core Web Vitals

```js
// Collect all Core Web Vitals
class WebVitalsCollector {
  #vitals = {};

  collect() {
    this.#observeLCP();
    this.#observeCLS();
    this.#observeINP();
    this.#observeFCP();
    this.#collectTTFB();
    return this;
  }

  #observe(type, cb, options = {}) {
    try {
      new PerformanceObserver(list => list.getEntries().forEach(cb))
        .observe({ type, buffered: true, ...options });
    } catch { /* PerformanceObserver may not support this entry type */ }
  }

  #observeLCP() {
    this.#observe('largest-contentful-paint', entry => {
      this.#vitals.lcp = entry.startTime;
    });
  }

  #observeCLS() {
    let clsValue = 0;
    this.#observe('layout-shift', entry => {
      if (!entry.hadRecentInput) {
        clsValue += entry.value;
        this.#vitals.cls = clsValue;
      }
    });
  }

  #observeINP() {
    this.#observe('event', entry => {
      const inp = entry.processingEnd - entry.startTime;
      this.#vitals.inp = Math.max(this.#vitals.inp ?? 0, inp);
    }, { durationThreshold: 16 });
  }

  #observeFCP() {
    this.#observe('paint', entry => {
      if (entry.name === 'first-contentful-paint') this.#vitals.fcp = entry.startTime;
    });
  }

  #collectTTFB() {
    const nav = performance.getEntriesByType('navigation')[0];
    if (nav) this.#vitals.ttfb = nav.responseStart;
  }

  getVitals() { return { ...this.#vitals }; }

  rate(metric, value) {
    const thresholds = {
      lcp:  [2500, 4000],
      cls:  [0.1,  0.25],
      inp:  [200,  500],
      fcp:  [1800, 3000],
      ttfb: [800,  1800],
    };
    const [good, poor] = thresholds[metric] ?? [0, 0];
    return value <= good ? 'good' : value <= poor ? 'needs-improvement' : 'poor';
  }

  report(endpoint) {
    const vitals  = this.getVitals();
    const payload = Object.entries(vitals).map(([name, value]) => ({
      name, value: Math.round(value * 10) / 10,
      rating: this.rate(name, value),
      url: location.href,
    }));
    navigator.sendBeacon(endpoint, JSON.stringify(payload));
  }
}

const vitals = new WebVitalsCollector().collect();
window.addEventListener('pagehide', () => vitals.report('/api/vitals'));

// Long Task monitoring
new PerformanceObserver(list => {
  list.getEntries().forEach(entry => {
    if (entry.duration > 50) {
      console.warn(`Long task detected: ${entry.duration.toFixed(0)}ms`, {
        startTime: entry.startTime,
        attribution: entry.attribution,
      });
    }
  });
}).observe({ type: 'longtask' });
```

---

## 40. Testing Vanilla JS

```js
// Architecture principle: separate business logic from DOM
// Pure functions are trivially testable, DOM code is not.

// ✅ Pure business logic (easily testable)
export const addToCart   = (cart, item) =>
  cart.some(i => i.id === item.id)
    ? cart.map(i => i.id===item.id ? {...i, qty:i.qty+1} : i)
    : [...cart, { ...item, qty: 1 }];

export const removeFromCart = (cart, id) => cart.filter(i => i.id !== id);
export const cartTotal      = cart => cart.reduce((s, i) => s + i.price * i.qty, 0);
export const applyDiscount  = (total, pct) => Math.round(total * (1 - pct/100) * 100) / 100;

// Minimal test runner
class TestSuite {
  #results = []; #only = false; #suiteName;

  constructor(name) { this.#suiteName = name; }

  async test(description, fn, { only = false, skip = false } = {}) {
    if (skip) { this.#results.push({ description, status: 'skipped' }); return; }
    if (only)  this.#only = true;
    this.#results.push({ description, fn, only });
  }

  async run() {
    const toRun = this.#only ? this.#results.filter(r => r.only) : this.#results;
    let pass = 0, fail = 0, skip = 0;

    console.group(`📋 ${this.#suiteName}`);

    for (const t of toRun) {
      if (t.status === 'skipped') {
        skip++;
        console.log(`  ⏭  ${t.description}`);
        continue;
      }
      try {
        await t.fn(assert);
        pass++;
        console.log(`  ✅ ${t.description}`);
      } catch (err) {
        fail++;
        console.error(`  ❌ ${t.description}`);
        console.error(`     ${err.message}`);
      }
    }
    console.log(`\n  ${pass} passed · ${fail} failed · ${skip} skipped`);
    console.groupEnd();
    return fail === 0;
  }
}

// Assert library
const assert = {
  eq:       (a, b, msg)   => { if (!Object.is(a, b))           throw new Error(msg ?? `Expected ${JSON.stringify(a)} to equal ${JSON.stringify(b)}`); },
  neq:      (a, b, msg)   => { if (Object.is(a, b))            throw new Error(msg ?? `Expected values to differ`); },
  deep:     (a, b, msg)   => { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error(msg ?? `Deep equality failed`); },
  ok:       (v, msg)      => { if (!v)                          throw new Error(msg ?? `Expected truthy, got ${v}`); },
  not:      (v, msg)      => { if (v)                           throw new Error(msg ?? `Expected falsy, got ${v}`); },
  throws:   (fn, msg)     => {
    let threw = false;
    try { fn(); } catch(e) { threw = true; if (msg && !e.message.includes(msg)) throw new Error(`Expected "${msg}" but got "${e.message}"`); }
    if (!threw) throw new Error('Expected function to throw');
  },
  resolves: async (p, expected) => {
    const result = await p;
    if (expected !== undefined) assert.deep(result, expected);
  },
  rejects:  async (p, msg) => {
    try { await p; throw new Error('Expected promise to reject'); }
    catch (e) { if (e.message === 'Expected promise to reject') throw e; if (msg) assert.ok(e.message.includes(msg)); }
  },
};

// Tests
const suite = new TestSuite('Shopping Cart');

await suite.test('addToCart adds new item', () => {
  const result = addToCart([], { id: 1, name: 'Widget', price: 9.99 });
  assert.eq(result.length, 1);
  assert.eq(result[0].qty, 1);
  assert.eq(result[0].price, 9.99);
});

await suite.test('addToCart increments quantity for existing item', () => {
  const cart   = [{ id: 1, name: 'Widget', price: 9.99, qty: 1 }];
  const result = addToCart(cart, { id: 1, name: 'Widget', price: 9.99 });
  assert.eq(result.length, 1);
  assert.eq(result[0].qty, 2);
});

await suite.test('addToCart is immutable', () => {
  const cart   = [{ id: 1, qty: 1, price: 10 }];
  const result = addToCart(cart, { id: 2, qty: 1, price: 20 });
  assert.eq(cart.length, 1);   // original unchanged
  assert.eq(result.length, 2);
});

await suite.test('cartTotal sums price × quantity', () => {
  const cart = [{ price: 10, qty: 2 }, { price: 5, qty: 3 }, { price: 1, qty: 10 }];
  assert.eq(cartTotal(cart), 45);
});

await suite.test('applyDiscount reduces total correctly', () => {
  assert.eq(applyDiscount(100, 10), 90);
  assert.eq(applyDiscount(100, 0),  100);
  assert.eq(applyDiscount(9.99, 50), 5);
});

await suite.run();
```

---

## 41. JSDoc Type Annotations

```js
// @ts-check  ← add to any .js file to enable TypeScript checking

/**
 * @typedef {Object} User
 * @property {number}  id
 * @property {string}  name
 * @property {string}  email
 * @property {'admin'|'user'|'guest'} role
 * @property {boolean} [active=true]
 * @property {Date}    [createdAt]
 */

/**
 * @template T
 * @typedef {Object} Paginated
 * @property {T[]}   data       - Array of results
 * @property {number} total     - Total count
 * @property {number} page      - Current page
 * @property {number} pageSize  - Items per page
 * @property {boolean} hasMore  - Whether more pages exist
 */

/**
 * @template T
 * @typedef {{ ok: true, value: T } | { ok: false, error: Error }} Result
 */

/**
 * Load a paginated list of users
 * @param {{ page?: number, limit?: number, role?: User['role'], search?: string }} [params]
 * @param {{ signal?: AbortSignal }} [options]
 * @returns {Promise<Paginated<User>>}
 * @throws {HttpError} on HTTP errors
 * @throws {NetworkError} on connection failures
 *
 * @example
 * const { data, total } = await loadUsers({ role: 'admin', limit: 10 });
 */
async function loadUsers(params = {}, options = {}) { /* ... */ }

// Type casting
const emailInput = /** @type {HTMLInputElement} */ (
  document.querySelector('input[name="email"]')
);
emailInput.value; // TypeScript knows this is string

// Enum pattern with type safety
/** @enum {string} */
const Direction = Object.freeze({
  UP:    'up',
  DOWN:  'down',
  LEFT:  'left',
  RIGHT: 'right',
});
/** @type {Direction[keyof typeof Direction]} */
const dir = Direction.UP;

// Generic createElement with full type inference
/**
 * @template {keyof HTMLElementTagNameMap} K
 * @param {K} tag
 * @param {Partial<HTMLElementTagNameMap[K]> & Record<string, unknown>} [props]
 * @param {(Node|string)[]} [children]
 * @returns {HTMLElementTagNameMap[K]}
 */
function createElement(tag, props = {}, children = []) {
  const el = Object.assign(document.createElement(tag), props);
  el.append(...children);
  return el;
}

const btn = createElement('button', { textContent: 'Save', className: 'btn' });
// btn is typed as HTMLButtonElement — full autocomplete!

// Callback types
/**
 * @callback EventHandler
 * @param {MouseEvent} event
 * @param {HTMLElement} target
 * @returns {void}
 */

/** @type {EventHandler} */
const handleItemClick = (event, target) => { /* ... */ };

// Complex generics
/**
 * @template {Record<string, unknown>} S - State shape
 * @param {S} initialState
 * @returns {{ state: S, update: (fn: (s: S) => void) => void, subscribe: (fn: (s: S) => void) => () => void }}
 */
function createStore(initialState) { /* ... */ }
```

---

## 42. Geolocation and Device APIs

```js
// ── Geolocation ───────────────────────────────────────────
const GeoService = {
  async getCurrentPosition({ highAccuracy = false, timeout = 10_000, maxAge = 60_000 } = {}) {
    if (!navigator.geolocation) throw new Error('Geolocation not supported');

    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        pos => resolve({
          lat:      pos.coords.latitude,
          lng:      pos.coords.longitude,
          altitude: pos.coords.altitude,
          accuracy: pos.coords.accuracy,
          timestamp: pos.timestamp,
        }),
        err => {
          const messages = {
            [GeolocationPositionError.PERMISSION_DENIED]:  'Location access denied',
            [GeolocationPositionError.POSITION_UNAVAILABLE]:'Location unavailable',
            [GeolocationPositionError.TIMEOUT]:             'Location request timed out',
          };
          reject(new Error(messages[err.code] ?? 'Geolocation error'));
        },
        { enableHighAccuracy: highAccuracy, timeout, maximumAge: maxAge }
      );
    });
  },

  watchPosition(onUpdate, onError, options = {}) {
    if (!navigator.geolocation) { onError(new Error('Not supported')); return () => {}; }

    const id = navigator.geolocation.watchPosition(
      pos => onUpdate({ lat: pos.coords.latitude, lng: pos.coords.longitude, accuracy: pos.coords.accuracy }),
      err => onError(new Error(err.message)),
      options
    );
    return () => navigator.geolocation.clearWatch(id);
  },

  // Haversine formula — distance between two GPS points
  distance({ lat: lat1, lng: lng1 }, { lat: lat2, lng: lng2 }) {
    const R = 6371e3; // Earth radius in meters
    const φ1 = lat1 * Math.PI / 180, φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2-lat1) * Math.PI/180, Δλ = (lng2-lng1) * Math.PI/180;
    const a  = Math.sin(Δφ/2)**2 + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)**2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  },
};

// ── Device capabilities ───────────────────────────────────
const DeviceInfo = {
  // Battery status
  async battery() {
    if (!('getBattery' in navigator)) return null;
    const b = await navigator.getBattery();
    return { level: b.level, charging: b.charging, chargingTime: b.chargingTime, dischargingTime: b.dischargingTime };
  },

  // Network connection quality
  get connection() {
    const c = navigator.connection ?? navigator.mozConnection ?? navigator.webkitConnection;
    return c ? { type: c.type, effectiveType: c.effectiveType, downlink: c.downlink, rtt: c.rtt } : null;
  },

  // Device memory (GB, rounded to nearest GB)
  get memory() { return navigator.deviceMemory ?? null; },

  // CPU logical cores
  get cores() { return navigator.hardwareConcurrency ?? null; },

  // Prefers reduced motion
  get prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  },

  // Is touch device
  get isTouch() { return navigator.maxTouchPoints > 0; },

  // Platform
  get platform() { return navigator.userAgentData?.platform ?? navigator.platform; },
};

// Online/Offline events
window.addEventListener('online',  () => { toast('Back online', 'success'); syncPendingData(); });
window.addEventListener('offline', () => toast('You are offline — changes saved locally', 'warn'));

// Page visibility (pause heavy work when tab is hidden)
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    pauseAnimations();
    stopVideoPlayback();
    reducePollFrequency();
  } else {
    resumeAnimations();
    restorePollFrequency();
    checkForUpdates();
  }
});
```

---

## 43. Virtual Scrolling

```js
// Already covered in section 17. Extended version with variable heights:
class VariableHeightVirtualScroller {
  #container; #items; #renderItem; #estimatedH;
  #heights = new Map(); #offsets = []; #visible = new Map(); #raf = null;

  constructor({ container, items, renderItem, estimatedItemHeight = 60 }) {
    this.#container   = container;
    this.#items       = items;
    this.#renderItem  = renderItem;
    this.#estimatedH  = estimatedItemHeight;

    this.#computeOffsets();

    this.#inner = Object.assign(document.createElement('div'), {
      style: `height:${this.#totalHeight()}px;position:relative;`,
    });
    container.append(this.#inner);
    container.style.overflow = 'auto';

    container.addEventListener('scroll', () => {
      cancelAnimationFrame(this.#raf);
      this.#raf = requestAnimationFrame(() => this.#render());
    }, { passive: true });

    this.#render();
  }

  #height(i)  { return this.#heights.get(i) ?? this.#estimatedH; }
  #totalHeight() {
    const last = this.#items.length - 1;
    return this.#offsets[last] + this.#height(last);
  }

  #computeOffsets() {
    this.#offsets = this.#items.map((_, i) =>
      i === 0 ? 0 : this.#offsets[i-1] + this.#height(i-1)
    );
  }

  #findStartIndex(scrollTop) {
    let lo = 0, hi = this.#offsets.length - 1;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      this.#offsets[mid] < scrollTop ? (lo = mid + 1) : (hi = mid);
    }
    return Math.max(0, lo - 1);
  }

  #render() {
    const { scrollTop, clientHeight } = this.#container;
    const startIdx = this.#findStartIndex(scrollTop);
    let endIdx = startIdx;
    let bottom = this.#offsets[startIdx];
    while (endIdx < this.#items.length - 1 && bottom < scrollTop + clientHeight + 200) {
      endIdx++;
      bottom += this.#height(endIdx);
    }

    // Remove off-screen
    for (const [i, el] of this.#visible) {
      if (i < startIdx || i > endIdx) { el.remove(); this.#visible.delete(i); }
    }

    // Add on-screen
    for (let i = startIdx; i <= endIdx; i++) {
      if (this.#visible.has(i)) continue;
      const el = this.#renderItem(this.#items[i], i);
      Object.assign(el.style, {
        position: 'absolute', top: `${this.#offsets[i]}px`, width: '100%',
      });
      this.#inner.append(el);
      this.#visible.set(i, el);

      // Measure actual height after render
      const actualH = el.getBoundingClientRect().height;
      if (actualH && actualH !== this.#height(i)) {
        this.#heights.set(i, actualH);
        this.#computeOffsets();
        this.#inner.style.height = `${this.#totalHeight()}px`;
      }
    }
  }
}
```

---

## 44. Temporal API

```js
// Temporal — modern date/time API (ES2025, verify support!)
// Replaces Date with immutable, timezone-aware types

// PlainDate — date only, no time, no timezone
const today    = Temporal.Now.plainDateISO();           // '2025-06-15'
const birthday = Temporal.PlainDate.from('1990-05-20');
const age      = birthday.until(today, { largestUnit: 'years' });
age.years;    // e.g. 35

// PlainTime — time only, no date, no timezone
const noon   = Temporal.PlainTime.from('12:00:00');
const now2   = Temporal.Now.plainTimeISO();
now2.hour;   // 14
now2.minute; // 30

// PlainDateTime — date + time, no timezone (local representation)
const meeting = Temporal.PlainDateTime.from('2025-09-15T10:30:00');
meeting.add({ hours: 2, minutes: 30 }); // PlainDateTime 2025-09-15T13:00:00

// ZonedDateTime — fully specified date+time+timezone
const event = Temporal.ZonedDateTime.from({
  timeZone: 'America/New_York',
  year: 2025, month: 9, day: 15, hour: 14, minute: 30,
});
const utc = event.toInstant().toString(); // ISO string in UTC

// Arithmetic
const nextWeek = today.add({ weeks: 1 });
const nextMonth = today.add({ months: 1 });
const diff = today.until(nextMonth, { smallestUnit: 'days' });
diff.days; // days until next month

// Comparison
Temporal.PlainDate.compare(
  Temporal.PlainDate.from('2025-01-01'),
  Temporal.PlainDate.from('2025-12-31')
); // -1 (first is before second)

// Duration arithmetic
const dur1 = Temporal.Duration.from({ hours: 2, minutes: 30 });
const dur2 = Temporal.Duration.from('PT1H45M');
dur1.add(dur2).total({ unit: 'minutes' }); // 255

// Feature detection and polyfill pattern
const PlainDate = typeof Temporal !== 'undefined'
  ? Temporal.PlainDate
  : { from: (s) => new Date(s) }; // minimal fallback
```

---

## 45. WeakRef and FinalizationRegistry

```js
// WeakRef — hold reference to object without preventing GC
class ComponentCache {
  #cache = new Map();

  set(key, component) {
    this.#cache.set(key, new WeakRef(component));
  }

  get(key) {
    const ref = this.#cache.get(key);
    if (!ref) return null;

    const target = ref.deref(); // returns undefined if GC'd
    if (target === undefined) {
      this.#cache.delete(key); // clean up dead reference
      return null;
    }
    return target;
  }
}

// FinalizationRegistry — callback when object is GC'd
const cleanupRegistry = new FinalizationRegistry((heldValue) => {
  console.log(`Object with ID ${heldValue} was garbage collected`);
  // Clean up associated resources (timers, subscriptions, etc.)
  cleanupResources(heldValue);
});

class ManagedResource {
  #id;
  #data;

  constructor(id, data) {
    this.#id   = id;
    this.#data = data;
    // Register: callback fires with this.#id when this instance is GC'd
    cleanupRegistry.register(this, this.#id);
  }
}

// Practical: event emitter that doesn't prevent GC of listeners
class WeakEventEmitter {
  #listeners = new Map();

  on(event, listener) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, new Set());
    this.#listeners.get(event).add(new WeakRef(listener));
  }

  emit(event, ...args) {
    const refs = this.#listeners.get(event);
    if (!refs) return;

    for (const ref of [...refs]) {
      const fn = ref.deref();
      if (fn === undefined) refs.delete(ref); // GC'd — clean up
      else fn(...args);
    }
  }
}
```

---

## 46. Anti-Patterns and Traps

### 46.1 Memory Leaks

```js
// ❌ Forgotten event listener
function setup(el) {
  el.addEventListener('click', handler);
  el.remove(); // element removed but listener holds reference → leak!
}
// ✅
function setup(el) {
  const ctrl = new AbortController();
  el.addEventListener('click', handler, { signal: ctrl.signal });
  return () => ctrl.abort(); // call this to clean up
}

// ❌ setInterval not cleared
class Poller { start() { setInterval(fn, 1000); } } // never stops!
// ✅
class Poller { start() { this.id=setInterval(fn,1000); } stop() { clearInterval(this.id); } }

// ❌ Closure holds large object unnecessarily
function makeHandler(bigArray) {
  return () => console.log(bigArray.length); // bigArray can never be GC'd
}
// ✅ Capture only what you need
function makeHandler(bigArray) {
  const len = bigArray.length;
  return () => console.log(len); // bigArray can now be GC'd
}

// ❌ Observer not disconnected
new IntersectionObserver(cb).observe(el); // el removed but observer persists
// ✅ Always disconnect in cleanup
const obs = new IntersectionObserver(cb);
obs.observe(el);
// In cleanup: obs.disconnect()
```

### 46.2 Classic JavaScript Bugs

```js
// ❌ NaN comparison
NaN === NaN; // false! Always use Number.isNaN()
Number.isNaN(NaN);   // true ✅
Number.isNaN('NaN'); // false ✅ (unlike global isNaN)

// ❌ typeof null
typeof null === 'object'; // true — historical bug
null === null;            // ✅ use strict equality

// ❌ Array sort without comparator (ALWAYS provide one)
[10, 2, 30].sort(); // [10, 2, 30] lexicographic! → should be [2,10,30]
[10, 2, 30].sort((a,b) => a-b); // ✅ numeric sort

// ❌ for...in on arrays (iterates string keys, includes prototype)
const arr = [1,2,3];
for (const k in arr) console.log(k); // '0', '1', '2' (strings! not numbers)
for (const v of arr) console.log(v); // ✅ 1, 2, 3

// ❌ delete creates sparse array
const a = [1,2,3];
delete a[1]; // [1, empty, 3] — dangerous sparse array
a.splice(1,1); // ✅ [1,3]

// ❌ parseInt without radix
parseInt('09'); // might be 0 in some environments (octal!)
parseInt('09', 10); // ✅ always specify radix 10
Number('09');       // ✅ or use Number()

// ❌ Mutating function argument
function sort(arr) { return arr.sort(); } // mutates the caller's array!
function sort(arr) { return [...arr].sort(); } // ✅ copy first

// ❌ Unnecessary sequential awaits
const user  = await fetchUser(id);   // 200ms
const posts = await fetchPosts(id);  // 200ms → 400ms total
// ✅
const [user2, posts2] = await Promise.all([fetchUser(id), fetchPosts(id)]); // 200ms

// ❌ Missing await
async function save(data) {
  const r = api.post('/save', { body: data }); // forgot await!
  return r.id; // TypeError: Cannot read property 'id' of Promise
}
// ✅
async function save(data) {
  const r = await api.post('/save', { body: data });
  return r.id;
}

// ❌ Race condition — earlier request may resolve after later one
async function search(q) {
  const results = await fetch(`/search?q=${q}`).then(r=>r.json());
  renderResults(results); // May render stale results!
}
// ✅ Use AbortController to cancel previous request

// ❌ this context in callbacks
class Timer {
  count = 0;
  start() {
    setInterval(function() { this.count++; }, 1000); // this ≠ Timer!
  }
}
// ✅
start() { setInterval(() => this.count++, 1000); } // arrow = lexical this
```

### 46.3 Performance Anti-Patterns

```js
// ❌ Layout thrashing
elements.forEach(el => {
  const h = el.offsetHeight;           // READ  → forces layout
  el.style.height = h + 10 + 'px';    // WRITE → invalidates
  // next iteration forces layout again!
});
// ✅ Batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight);      // all reads
elements.forEach((el, i) => { el.style.height = heights[i]+10+'px'; }); // all writes

// ❌ Animating with left/top (triggers layout on every frame)
el.style.left = x + 'px'; el.style.top = y + 'px';
// ✅ Use transform (GPU compositor, no layout)
el.style.transform = `translate(${x}px, ${y}px)`;

// ❌ Creating objects in hot animation path
function animate() {
  const color = { r:255, g:0, b:0 }; // new object every frame → GC pressure
  requestAnimationFrame(animate);
}
// ✅ Reuse objects
const color = { r:255, g:0, b:0 };
function animate() {
  color.r = Math.sin(Date.now()/1000) * 127 + 128; // mutate, don't allocate
  requestAnimationFrame(animate);
}
```

---

## 47. Quality Checklist

### Syntax and Style
```
✅ const by default, let for reassignment, never var
✅ Arrow functions for callbacks/closures; regular functions for methods/constructors
✅ ?. only when null/undefined is a VALID expected state (not a bug)
✅ ?? instead of || when 0, '', or false are valid values
✅ Options object (with default {}) for functions with 3+ parameters
✅ async/await over raw .then() chains (usually)
✅ Private class fields # for encapsulation (not _prefix convention)
✅ structuredClone() for deep cloning (not JSON.parse/JSON.stringify for non-JSON types)
✅ Array.at(-1) instead of arr[arr.length-1]
✅ Object.hasOwn() instead of obj.hasOwnProperty()
```

### Error Handling
```
✅ Every async function has try/catch or propagates to a caller that does
✅ AbortController used for cancellable fetch operations
✅ Global window.addEventListener('unhandledrejection') handler present
✅ Custom Error subclasses for typed error handling
✅ No empty catch(e) {} blocks — always log or rethrow
✅ User-facing messages are friendly; stack traces stay in logs only
✅ Error reporter uses keepalive: true for page-unload resilience
```

### Security
```
✅ textContent for user-generated text (never innerHTML without sanitization)
✅ All URLs validated (isSafeUrl) before assignment to src/href
✅ No eval(), new Function(), or setTimeout(string)
✅ CSRF token sent with all POST/PUT/PATCH/DELETE requests
✅ No API keys, tokens, or secrets in client-side source code
✅ Subresource Integrity (integrity attribute) on all CDN resources
✅ localStorage never stores auth tokens (use HttpOnly cookies instead)
✅ Dynamic CSS values sanitized before use
```

### Performance
```
✅ All DOM writes batched after reads (no layout thrashing)
✅ Animations use CSS transform/opacity (GPU-composited, no layout)
✅ scroll/touchmove listeners are passive: true
✅ Input events debounced; scroll/resize events throttled
✅ Heavy computation offloaded to Web Workers
✅ Images have explicit width and height attributes (prevents CLS)
✅ Lists with 100+ items use virtual scrolling
✅ Heavy features code-split with dynamic import()
✅ Long tasks chunked to preserve main thread responsiveness
✅ will-change added before animation, removed after
```

### Memory Management
```
✅ Event listeners removed when component unmounts
✅ setInterval/setTimeout IDs stored and cleared in cleanup
✅ IntersectionObserver/MutationObserver/ResizeObserver disconnected
✅ URL.revokeObjectURL() called after object URLs are used
✅ AbortController used for bulk listener cleanup
✅ WeakMap/WeakRef used for data tied to DOM nodes
```

### Accessibility
```
✅ Interactive elements use semantic HTML (button, a, input — not div/span)
✅ All meaningful images have descriptive alt text; decorative images have alt=""
✅ Color is never the ONLY means of conveying information
✅ Focus trapped inside modal dialogs when open
✅ All interactive elements reachable and operable by keyboard
✅ Dynamic content changes announced via aria-live regions
✅ ARIA state attributes updated to match visual state (aria-expanded, aria-selected)
✅ Focus returns to trigger element when dialog closes
✅ Animations respect prefers-reduced-motion media query
```

---

## 48. Quick Syntax Reference

```js
// ── VARIABLES ─────────────────────────────────────────────
const x = 1;           // immutable binding (default choice)
let   y = 1;           // mutable binding (only when reassigning)
// var ← NEVER USE

// ── DESTRUCTURING ──────────────────────────────────────────
const { a, b: alias, c = 'default' }  = obj;
const [first, , third, ...rest]        = arr;
const { x: { y: deep } = {} }         = nested;
const { [dynamicKey]: val }            = obj;

// ── SPREAD / REST ──────────────────────────────────────────
const merged = { ...obj1, ...obj2 };       // merge (later wins)
const joined = [...arr1, extra, ...arr2];  // join with item
function fn(req, ...optionals) {}
const { a: _, ...without } = obj;          // omit key

// ── NULLISH / OPTIONAL ─────────────────────────────────────
a?.b?.c             // safe chain (only when null is valid)
fn?.()              // safe call
x ?? 'def'          // null/undefined only (not 0 or '')
x ??= 'val'         // assign if null/undefined
x ||= 'val'         // assign if falsy
x &&= transform(x)  // assign if truthy

// ── FUNCTIONS ──────────────────────────────────────────────
const f    = x => x * 2;                    // arrow (concise)
const obj2 = x => ({ key: x });             // return object — wrap in ()!
async function load()  { return await fetch(url); }
function* gen()        { yield 1; yield 2; }
async function* pages(){ yield await fetchPage(1); }

// ── CLASSES ────────────────────────────────────────────────
class Foo extends Bar {
  #priv = 0;                               // private field (ES2022)
  static shared = 0;                       // static field
  static { /* static initialization block */ }
  get val()    { return this.#priv; }
  set val(v)   { this.#priv = v; }
  method()     { super.method(); }
  static make() { return new Foo(); }
}

// ── ASYNC ──────────────────────────────────────────────────
await Promise.all([p1, p2]);          // all or first error
await Promise.allSettled([p1, p2]);   // all, with status objects
await Promise.race([p1, p2]);         // first settled (any)
await Promise.any([p1, p2]);          // first fulfilled
const { promise, resolve, reject } = Promise.withResolvers(); // ES2024
AbortSignal.timeout(5000);            // auto-cancel signal
AbortSignal.any([sig1, sig2]);        // first-aborted signal

// ── MODULES ────────────────────────────────────────────────
export const x = 1;                   // named export
export default class {}               // default export
import { x } from './m.js';          // named import
import def, { x } from './m.js';     // default + named
import * as ns from './m.js';         // namespace import
const m = await import('./m.js');     // dynamic import (lazy)

// ── MODERN ARRAY (2022–2024) ───────────────────────────────
arr.at(-1)               // last element (negative index)
arr.findLast(fn)         // search from end → value
arr.findLastIndex(fn)    // search from end → index
arr.toSorted(fn)         // sorted copy (ES2023)
arr.toReversed()         // reversed copy (ES2023)
arr.toSpliced(i, n, v)   // spliced copy (ES2023)
arr.with(i, v)           // index-replaced copy (ES2023)
arr.flatMap(fn)          // map + flat(1)
Object.groupBy(arr, fn)  // group into plain object (ES2024)
Map.groupBy(arr, fn)     // group into Map (ES2024)

// ── OBJECT / CLONE ─────────────────────────────────────────
Object.hasOwn(obj, k)    // own property? (ES2022)
Object.fromEntries(it)   // pairs → object
structuredClone(val)     // deep clone (ES2022)

// ── ITERATION ──────────────────────────────────────────────
for (const v of iter)                 {}
for (const [i, v] of arr.entries())  {}
for (const [k, v] of map)            {}
for await (const v of asyncIter)     {}

// ── TYPE HELPERS ───────────────────────────────────────────
Array.isArray(v)            // true for arrays
Number.isNaN(v)             // true only for NaN (unlike global)
Number.isFinite(v)          // true for finite numbers
Number.isInteger(v)         // true for integers
Number.isSafeInteger(v)     // within ±2^53-1
Object.is(a, b)             // strict equality (handles NaN, -0)
```

---

## 49. Standards Timeline

| Standard | Year | Key Additions |
|----------|------|---------------|
| **ES5** | 2009 | Strict mode, `JSON`, `Array.isArray`, `bind`, property descriptors |
| **ES2015 (ES6)** | 2015 | `let`/`const`, classes, arrow fns, promises, modules, destructuring, Symbol, Map/Set, generators, `for...of`, template literals, `Proxy`, `Reflect`, default/rest/spread params |
| **ES2016** | 2016 | `Array.prototype.includes`, `**` exponentiation operator |
| **ES2017** | 2017 | `async`/`await`, `Object.entries`/`values`, `String.padStart`/`padEnd`, `SharedArrayBuffer` |
| **ES2018** | 2018 | `Promise.finally`, object rest/spread `{...o}`, `for await...of`, async iteration, named regex groups `(?<name>)`, lookbehind `(?<=)`, `RegExp /s` dotAll flag |
| **ES2019** | 2019 | `Array.flat`/`flatMap`, `Object.fromEntries`, `String.trimStart`/`trimEnd`, optional `catch` binding, `Symbol.description` |
| **ES2020** | 2020 | `BigInt`, optional chaining `?.`, nullish coalescing `??`, `Promise.allSettled`, `globalThis`, dynamic `import()`, `String.matchAll`, `import.meta` |
| **ES2021** | 2021 | `Promise.any`, `String.replaceAll`, logical assignment `&&=` `\|\|=` `??=`, `WeakRef`, `FinalizationRegistry`, numeric separators `1_000` |
| **ES2022** | 2022 | Class private fields `#`, static class blocks, `Object.hasOwn`, `Array.at`/`String.at`, `structuredClone`, `Error.cause`, top-level `await` in modules |
| **ES2023** | 2023 | `Array.findLast`/`findLastIndex`, `Array.toSorted`/`toReversed`/`toSpliced`/`with`, Symbol as WeakMap/WeakSet keys, Hashbang grammar |
| **ES2024** | 2024 | `Object.groupBy`/`Map.groupBy`, `Promise.withResolvers`, Set methods (`union`/`intersection`/`difference`/`symmetricDifference`/`isSubsetOf`/`isSupersetOf`/`isDisjointFrom`), `ArrayBuffer.resize`/`transfer`, `RegExp /v` unicode sets flag |
| **ES2025** | 2025 | Iterator helpers (`map`/`filter`/`take`/`drop`/`flatMap`/`reduce`), `import attributes`, `Float16Array`, `Promise.try`, `RegExp.escape`, `JSON.parse` with source access |

---

| Browser API | Status | Notes |
|-------------|--------|-------|
| `structuredClone` | ✅ All modern | ES2022 |
| `crypto.randomUUID` | ✅ All modern | Requires HTTPS |
| `AbortSignal.timeout` | ✅ All modern | ES2022 |
| `AbortSignal.any` | ✅ All modern | ES2024 |
| `Promise.withResolvers` | ✅ All modern | ES2024 |
| `Object.groupBy` | ✅ All modern | ES2024 |
| Set methods (union etc.) | ✅ All modern | ES2024 |
| `Array.toSorted` etc. | ✅ All modern | ES2023 |
| Web Animations API | ✅ All modern | Good coverage |
| CSS Constructable StyleSheets | ✅ Chrome/Edge/Firefox | Check Safari |
| File System Access API | ⚠️ Chrome/Edge only | Needs fallback |
| `scheduler.postTask` | ⚠️ Chrome/Edge only | Always fallback |
| `scheduler.yield` | ⚠️ Chrome only | fallback: `setTimeout(r,0)` |
| SharedWorker | ✅ All modern | Limited iOS support |
| Temporal API | ⚠️ Polyfill needed | ES2025, not yet everywhere |
| `import attributes` | ⚠️ Partial | Check before use |

---

*The Complete Vanilla JavaScript Mega-Guide — unified from EN + RU editions.*  
*49 sections · 12,000+ lines of production-ready code · 2025 edition*  
*Always verify current browser support: [caniuse.com](https://caniuse.com) · [MDN Web Docs](https://developer.mozilla.org) · [tc39.es](https://tc39.es)*
