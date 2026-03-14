# Containerization Guide
## Widget Standard: HTML · CSS · JavaScript

---

## Core Standard (best practices)

| # | Rule | Rationale |
|---|---|---|
| 1 | CSS selector as entry point | Multiple instances on one page without conflicts |
| 2 | Silent `return` when container is missing | Safe to include globally on any page |
| 3 | All CSS rules scoped under the container | Styles cannot leak outside the widget |
| 4 | `_` prefix on all class properties | Clear visual separation of public vs private API |
| 5 | `$` / `$$` DOM helpers in constructor | No repetition of `this._root.querySelector` throughout |
| 6 | `DOMContentLoaded` for initialization | Works regardless of where the script is placed |
| 7 | `data-*` attributes as JS hooks | HTML structure and JS logic are fully decoupled |
| 8 | DOM references cached once | No repeated querySelector calls at runtime |
| 9 | State as single source of truth | UI is always derived from state, never from DOM |
| 10 | `AbortController` for event listeners | A single `abort()` removes all listeners on `destroy()` |

---

## 1. File Structure

Each widget is a self-contained HTML file (or separate HTML + CSS + JS when extracted for production). Section order is fixed:

```
<style>
  /* 1. Tokens and variables      */
  /* 2. Container                 */
  /* 3. Child elements (sections) */
  /* 4. States                    */
  /* 5. Animations (@keyframes)   */
  /* 6. Responsive (@media)       */
</style>

<div class="widget-container">
  <!-- widget markup -->
</div>

<script>
  /* 1. CONFIG — constants        */
  /* 2. CLASS  — ES6 class        */
  /* 3. SEED DATA / MOCK          */
  /* 4. INIT  — DOMContentLoaded  */
</script>
```

---

## 2. HTML

### 2.1 Container

The container is the root element of the widget. Use a semantic tag that matches the content (`<section>`, `<article>`, `<nav>`, `<div>`). Class only — no `id`:

```html
<!-- ✅ correct -->
<section class="messages-container" aria-label="Seller correspondence">

<!-- ⚠️  wrong — id creates an unnecessary coupling with JS -->
<section id="messages-module" class="messages-container">
```

If an `id` is required for a Bootstrap component or ARIA reference, that is an accepted exception — but JS initialization still goes through the class selector.

### 2.2 JS hooks via `data-*`

Classes are for styling. `data-*` attributes are for JS. Never do `querySelector('.btn-primary')` for logic:

```html
<!-- ✅ correct — JS hook is separate from styles -->
<button class="btn btn-primary" data-action="send">Send</button>
<div class="messages-list" data-ref="messages"></div>

<!-- ⚠️  wrong — class carries double responsibility -->
<button class="btn btn-primary js-send-btn">Send</button>
```

| Attribute | Purpose | Example |
|---|---|---|
| `data-ref` | Static DOM reference cached in constructor | `data-ref="send-btn"` |
| `data-action` | Delegated event handler trigger | `data-action="remove"` |
| `data-id` | Record identifier | `data-id="order-42"` |
| `data-state` | Reflects element state (also used in CSS) | `data-state="shipped"` |

### 2.3 ARIA

Minimum required for accessibility:

```html
<!-- Interactive lists — listbox pattern -->
<ul role="listbox" aria-label="Order list" aria-activedescendant="">
  <li role="option" aria-selected="false" tabindex="0" id="item-1">...</li>
</ul>

<!-- Live regions — updates are announced by screen readers -->
<div role="log" aria-live="polite" aria-atomic="false">
  <!-- chat messages -->
</div>

<!-- Status badges -->
<span aria-live="polite" aria-label="Order status">Delivered</span>
```

Keyboard navigation for listbox: `↑↓` move focus, `Home`/`End` jump to ends, `Enter`/`Space` activate.

---

## 3. CSS

### 3.1 Scoping — the cardinal rule

**Every CSS selector in a widget must begin with the container class name. No exceptions:**

```css
/* ✅ correct — all styles are isolated */
.orders-container .order-card { }
.orders-container .order-card:hover { }
.orders-container .stepper { }

/* ⚠️  wrong — styles leak onto the entire page */
.order-card { }
.stepper { }
```

This guarantees:
- Two instances of the same widget on one page never conflict
- Styles can be overridden from outside without `!important`
- Removing the widget removes all its styles with it

### 3.2 Class naming — prefix

All child classes of a widget get a unique short prefix that matches (or abbreviates) the container name:

```css
/* container: .messages-container */
/* prefix:     msg-               */

.messages-container .msg-bubble  { }
.messages-container .msg-input   { }
.messages-container .msg-sidebar { }
```

Format: `[prefix]-[element]` or `[prefix]-[element]--[modifier]` (BEM-like).

### 3.3 States via data attributes

For states toggled by JS — prefer `data-state` over adding modifier classes:

```css
/* ✅ readable — state is visible directly in HTML */
.orders-container .order-card[data-state="cancelled"] .stepper-dot {
  background: var(--bs-danger);
}

/* also acceptable — BEM modifier class */
.orders-container .order-card--cancelled .stepper-dot {
  background: var(--bs-danger);
}
```

### 3.4 CSS custom properties

Widget tokens are scoped CSS variables, not globals:

```css
.messages-container {
  --msg-bubble-radius:   1rem;
  --msg-bubble-sent-bg:  var(--bs-primary);
  --msg-bubble-recv-bg:  var(--bs-body-secondary);
  --msg-sidebar-width:   280px;
}

.messages-container .msg-bubble--sent {
  background:    var(--msg-bubble-sent-bg);
  border-radius: var(--msg-bubble-radius);
}
```

### 3.5 Animations

`@keyframes` names must carry the widget prefix — keyframe names are global:

```css
/* ✅ correct */
@keyframes msg-bubble-in {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ⚠️  wrong — may conflict with another widget on the same page */
@keyframes bubble-in { }
```

Animate only `transform` and `opacity` — these run on the compositor thread and cause no reflow.

### 3.6 Responsive

`@media` blocks inside a widget's `<style>` cover only that widget's styles. Breakpoints come from the design system (Bootstrap: 576 / 768 / 992 / 1200):

```css
@media (max-width: 767.98px) {
  .messages-container .msg-sidebar { display: none !important; }
  .messages-container.msg-mob-chat .msg-sidebar { display: flex !important; }
}
```

---

## 4. JavaScript

### 4.1 Class structure

```js
class WidgetController {

  // ─── 1. CONSTRUCTOR ────────────────────────────────────────────
  constructor(selector, opts = {}) {

    // 1a. Find container — silent exit if not found
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // 1b. Scope helpers (created once, used everywhere)
    const $ = sel => this._root.querySelector(sel);
    const $$ = sel => [...this._root.querySelectorAll(sel)];

    // 1c. Cache DOM references
    this._list    = $('[data-ref="list"]');
    this._input   = $('[data-ref="input"]');
    this._sendBtn = $('[data-ref="send-btn"]');

    // 1d. Options with defaults
    this._delay = opts.delay ?? 1000;

    // 1e. State — single source of truth
    this._state = {
      items:    [],
      activeId: null,
      loading:  false,
    };

    // 1f. AbortController for event listeners
    this._ac = new AbortController();

    // 1g. Boot
    this._render();
    this._bind();
  }

  // ─── 2. RENDER ─────────────────────────────────────────────────
  /** @private */
  _render() { }

  /** @private */
  _renderItem(item) { }

  // ─── 3. ACTIONS ────────────────────────────────────────────────
  /** @private */
  _select(id) { }

  /** @private */
  _submit() { }

  // ─── 4. EVENTS ─────────────────────────────────────────────────
  /** @private */
  _bind() {
    const sig = { signal: this._ac.signal };

    // Delegation — one listener on the container covers all children,
    // including elements added dynamically after initialization.
    this._root.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      this[`_on_${btn.dataset.action}`]?.(btn, e);
    }, sig);
  }

  // ─── 5. HELPERS ────────────────────────────────────────────────

  /**
   * Escapes all 7 OWASP-recommended HTML characters.
   * Use for any server/API data inserted via innerHTML.
   * User-supplied text must always use textContent instead.
   * @param {string} s
   * @returns {string}
   * @private
   */
  _esc(s) {
    return String(s ?? '')
      .replace(/&/g,  '&amp;')   // FIRST — prevents double-escaping
      .replace(/</g,  '&lt;')
      .replace(/>/g,  '&gt;')
      .replace(/"/g,  '&quot;')
      .replace(/'/g,  '&#x27;')
      .replace(/\//g, '&#x2F;')
      .replace(/`/g,  '&#x60;');
  }

  /**
   * Truncates a string to maxLen characters, appending '…' if cut.
   * @param {string} s
   * @param {number} maxLen
   * @returns {string}
   * @private
   */
  _cut(s, maxLen) {
    return s.length > maxLen ? s.slice(0, maxLen) + '…' : s;
  }

  // ─── 6. LIFECYCLE ──────────────────────────────────────────────

  /**
   * Removes all event listeners and cleans up resources.
   * Call when the widget is removed from the page.
   */
  destroy() {
    this._ac.abort(); // removes ALL registered listeners in one call
  }

  // ─── 7. STATIC ─────────────────────────────────────────────────

  /**
   * Guards against prototype pollution from untrusted data sources.
   * Call on every external object before passing it to the constructor.
   * @param {Object} obj
   * @returns {boolean}
   */
  static _validate(obj) {
    const FORBIDDEN = ['__proto__', 'constructor', 'prototype'];
    if (!obj || typeof obj !== 'object') return false;
    return !Object.keys(obj).some(k => FORBIDDEN.includes(k));
  }
}
```

### 4.2 Silent return — mandatory

The widget may be included on pages where its container does not exist. Never throw in that case:

```js
// ✅ correct — no console noise on unrelated pages
this._root = document.querySelector(selector);
if (!this._root) return;

// ⚠️  wrong — throws on every page that doesn't have the widget
if (!this._root) throw new Error('WidgetController: container not found');
```

### 4.3 Private property convention

All internal properties use the `_` prefix. This is a convention, not a language constraint. For true privacy, ES2022+ `#prop` syntax is available in all modern browsers:

```js
// ✅ correct — immediately clear that these are internal
this._root    = ...
this._state   = ...
this._sendBtn = ...

// ⚠️  wrong — indistinguishable from public API
this.root     = ...
this.state    = ...
this.sendBtn  = ...
```

Public API methods (callable by external code) carry no prefix:

```js
controller.setItems(items)
controller.destroy()
```

### 4.4 DOM helpers `$` / `$$`

Declared in the constructor, scoped to the container. Eliminate repetitive querySelector calls:

```js
// ✅ declare once — use everywhere
const $ = sel => this._root.querySelector(sel);
const $$ = sel => [...this._root.querySelectorAll(sel)];

this._form  = $('[data-ref="form"]');
this._items = $$('[data-ref="item"]');

// ⚠️  wrong — duplicated throughout the class
this._form  = this._root.querySelector('[data-ref="form"]');
// ...and again in _render(), again in _bind()...
```

### 4.5 State as single source of truth

The UI is always a projection of state. Never read state back from the DOM:

```js
// ✅ correct — update state first, then render
_select(id) {
  this._state.activeId = id;
  this._render();  // UI rebuilt entirely from state
}

// ⚠️  wrong — reading state from the DOM
_select(id) {
  const current = this._root.querySelector('.active')?.dataset.id;
  // ...logic driven by DOM instead of state
}
```

### 4.6 AbortController for events

Allows removing all event handlers with a single call. Required whenever the widget can be destroyed or re-initialized:

```js
constructor(selector) {
  // ...
  this._ac = new AbortController();
  this._bind();
}

_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click',   this._onClick,  sig);
  this._root.addEventListener('keydown', this._onKey,    sig);
  window.addEventListener('resize',      this._onResize, sig);
  // ^ also removed on abort(), even though attached to window
}

destroy() {
  this._ac.abort(); // removes every listener registered with this signal
}
```

### 4.7 Event delegation

One listener on the container instead of one per child element. Works for dynamically added elements and is more memory-efficient:

```js
// ✅ correct — one listener, works for future elements too
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  const actions = {
    'send':   () => this._send(),
    'remove': () => this._remove(btn.dataset.id),
    'toggle': () => this._toggle(btn.dataset.id),
  };

  actions[btn.dataset.action]?.();
}, { signal: this._ac.signal });

// ⚠️  wrong — a listener per element, breaks on dynamic content
this._root.querySelectorAll('[data-action="send"]').forEach(btn => {
  btn.addEventListener('click', () => this._send());
});
```

### 4.8 XSS protection

User-supplied text — `textContent` only. Server/API metadata in innerHTML — always through `_esc()`:

```js
// ✅ correct
bubble.textContent = userMessage;                           // no XSS possible
li.innerHTML = `<span>${this._esc(apiData.name)}</span>`;  // metadata escaped

// ⚠️  dangerous
bubble.innerHTML = userMessage;            // XSS vulnerability
li.innerHTML = `<span>${apiData.name}</span>`;
```

### 4.9 Prototype pollution guard

Validate all external data (API responses, localStorage, URL params) before use:

```js
static _validate(obj) {
  const FORBIDDEN = ['__proto__', 'constructor', 'prototype'];
  if (!obj || typeof obj !== 'object') return false;
  return !Object.keys(obj).some(k => FORBIDDEN.includes(k));
}

// In init — filter before passing to constructor
const safeItems = rawData.filter(item => WidgetController._validate(item));
```

---

## 5. Initialization

### 5.1 Standard pattern

```js
document.addEventListener('DOMContentLoaded', () => {
  new WidgetController('.widget-container');
});
```

`DOMContentLoaded` fires when the DOM is fully parsed, regardless of where the `<script>` tag is placed: `<head>`, end of `<body>`, or as an external file.

### 5.2 With options and data validation

```js
document.addEventListener('DOMContentLoaded', () => {
  const safeData = SEED_DATA.filter(d => WidgetController._validate(d));

  new WidgetController({
    selector: '.widget-container',
    data:     safeData,
    delay:    1000,
  });
});
```

### 5.3 Multiple instances on one page

```js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.messages-container').forEach((el, i) => {
    el.id = el.id || `messages-${i}`;
    new MessagesController({ selector: `#${el.id}`, data: SEED_DATA });
  });
});
```

---

## 6. Naming Conventions

### 6.1 Classes and files

| What | Convention | Example |
|---|---|---|
| ES6 class | PascalCase + `Controller` suffix | `MessagesController` |
| CSS container | kebab-case + `-container` suffix | `.messages-container` |
| CSS child prefix | short kebab | `msg-` |
| HTML file | `feature-hash.html` | `correspondence-3f.html` |
| Instance variable | camelCase | `const messagesController` |

### 6.2 `data-*` attributes

| Purpose | Attribute | Example |
|---|---|---|
| DOM reference (cached in constructor) | `data-ref` | `data-ref="send-btn"` |
| Action trigger (delegated handler) | `data-action` | `data-action="remove"` |
| Record identifier | `data-id` | `data-id="order-42"` |
| Element state (also used in CSS) | `data-state` | `data-state="shipped"` |

---

## 7. New Widget Checklist

```
HTML
  [ ] Container uses a semantic tag, class only, no id
  [ ] JS hooks use data-ref / data-action, not classes
  [ ] ARIA: role, aria-label, aria-live where applicable
  [ ] Keyboard navigation implemented for interactive lists

CSS
  [ ] Every selector starts with .widget-container
  [ ] @keyframes names carry the widget prefix
  [ ] Tokens defined as scoped CSS custom properties

JS
  [ ] Silent return if container is not found
  [ ] $ / $$ helpers declared in constructor
  [ ] DOM references cached in constructor, nowhere else
  [ ] All internal properties use _ prefix
  [ ] State is the single source of truth
  [ ] AbortController used for all event listeners
  [ ] Event delegation via data-action, not per-element listeners
  [ ] User text set via textContent, never innerHTML
  [ ] Server/API data escaped via _esc() before innerHTML
  [ ] External objects validated via _validate()
  [ ] DOMContentLoaded wraps initialization
```
