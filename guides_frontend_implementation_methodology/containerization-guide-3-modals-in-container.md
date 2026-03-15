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
| 11 | Config and seed data as `static` class properties | INIT stays one line; everything self-contained |
| 12 | Constructor signature `(selector, opts = {})` | Minimal call; overrides only when needed |
| 13 | Modals live inside the container | Modals consume container tokens; placing them outside breaks CSS scoping |

---

## 1. File Structure

Each widget is a self-contained HTML file (or separate HTML + CSS + JS when extracted for production). Section order is fixed:

```
<style>
  /* 0. Tokens (CSS custom properties)  */
  /* 1. Container layout                */
  /* 2. Child elements (sections)       */
  /* 3. Modal(s)                        */
  /* 4. States                          */
  /* 5. Animations (@keyframes)         */
  /* 6. Responsive (@media)             */
</style>

<section class="widget-container">
  <!-- widget markup -->

  <!-- Modals live here — display:none until activated -->
  <div class="wgt-modal-overlay" data-ref="modal-confirm" aria-modal="true" role="dialog" aria-labelledby="wgt-modal-title" hidden>
    <div class="wgt-modal">
      <h2 id="wgt-modal-title" class="wgt-modal__title"></h2>
      <p  class="wgt-modal__body"></p>
      <div class="wgt-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Confirm</button>
      </div>
    </div>
  </div>
</section>

<script>
  /* 1. CLASS
   *   ├── static config props
   *   ├── static seed data
   *   ├── constructor
   *   ├── render methods
   *   ├── action methods
   *   ├── event binding
   *   ├── helpers
   *   ├── destroy()
   *   └── static _validate()
   */

  /* 2. INIT — DOMContentLoaded  */
</script>
```

**Key change from older versions:** there is no standalone `CONFIG` block above the class. All constants and seed data live as `static` properties inside the class. The `INIT` block is always a single line.

**Modal placement rule:** modals are part of the widget markup and must sit **inside** the container element. They are hidden by default (`hidden` attribute + CSS). Because modals consume the container's CSS custom properties (tokens), placing them outside the container — e.g. appended to `<body>` — breaks token resolution and violates CSS scoping (rule 3).

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

If an `id` is required for a Bootstrap component or ARIA reference (`aria-labelledby`, `aria-activedescendant`), that is an accepted exception — but JS initialization still goes through the class selector.

### 2.2 JS hooks via `data-*`

Classes are for styling. `data-*` attributes are for JS. Never use `querySelector('.btn-primary')` for logic:

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
| `data-action` | Delegated event handler trigger | `data-action="send"` |
| `data-id` | Record identifier | `data-id="order-42"` |
| `data-state` | Reflects JS-driven state, also used in CSS | `data-state="active"` |

**`data-ref` does not conflict between widgets.** All lookups go through `$('[data-ref="..."]')` where `$` is scoped to `this._root`. Two widgets on the same page with identical `data-ref` values will never interfere — each controller can only see inside its own container.

### 2.3 Modals

Modals are a first-class part of the widget's markup. They live inside the container, at the bottom of it, before the closing tag:

```html
<section class="orders-container">

  <!-- ... main widget markup ... -->

  <!-- ✅ Modal inside container — tokens resolve correctly, CSS is scoped -->
  <div class="ord-modal-overlay" data-ref="modal-delete" role="dialog"
       aria-modal="true" aria-labelledby="ord-modal-title" hidden>
    <div class="ord-modal">
      <h2 id="ord-modal-title" class="ord-modal__title">Delete order?</h2>
      <p  class="ord-modal__body">This action cannot be undone.</p>
      <div class="ord-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Confirm</button>
      </div>
    </div>
  </div>

</section>

<!-- ⚠️  wrong — modal outside container: tokens break, styles leak -->
<div class="ord-modal-overlay" ...>...</div>
```

**Why inside?**
- The modal overlay uses `position: fixed` with `z-index`. This works whether the element is inside or outside the container — a fixed element escapes the normal document flow regardless.
- CSS custom properties (tokens) are inherited down the DOM tree. A modal outside the container cannot inherit `--ord-*` tokens declared on `.orders-container`.
- Scoping rule (§3.1) requires every selector to begin with the container class. Modals placed outside would require un-scoped selectors, which is a violation.

**`hidden` attribute vs `display: none`:** Use the HTML `hidden` attribute as the initial state. JS toggles it via `el.hidden = true / false`. The CSS declaration `display: none` for `[hidden]` is already in every browser's default stylesheet — no extra CSS needed to hide them initially.

**One overlay per modal type.** If a widget needs multiple distinct confirmation flows, use one overlay per type, each with its own `data-ref`:

```html
<div data-ref="modal-delete" ...>...</div>
<div data-ref="modal-archive" ...>...</div>
```

**Avoid generic/shared modal singletons** inside a widget. Shared modals require runtime mutation of their content and add hidden coupling between action handlers.

### 2.4 ARIA

Minimum required for accessibility:

```html
<!-- Interactive lists — listbox pattern -->
<ul role="listbox" aria-label="Order list" aria-activedescendant="">
  <li role="option" aria-selected="false" tabindex="0" id="item-1">...</li>
</ul>

<!-- Live regions — updates announced by screen readers -->
<div role="log" aria-live="polite" aria-atomic="false">
  <!-- chat messages appended dynamically -->
</div>

<!-- Status badges -->
<span aria-live="polite" aria-label="Order status">Delivered</span>

<!-- Modal dialog -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title-id" hidden>
  <h2 id="modal-title-id">Confirm deletion</h2>
  ...
</div>
```

Keyboard navigation for listbox: `↑↓` move focus, `Home`/`End` jump to ends, `Enter`/`Space` activate.

Modal keyboard: `Escape` closes; focus is trapped inside while open; focus returns to the trigger element on close.

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

**Modals are no exception.** Even though the modal overlay uses `position: fixed`, its CSS selectors must still start with the container class:

```css
/* ✅ correct — scoped even though visually full-screen */
.orders-container .ord-modal-overlay { }
.orders-container .ord-modal         { }
.orders-container .ord-modal__title  { }

/* ⚠️  wrong — breaks scoping, leaks globally */
.ord-modal-overlay { }
.ord-modal { }
```

### 3.2 Class naming — prefix

All child classes get a unique short prefix that abbreviates the container name:

```css
/* container: .messages-container */
/* prefix:     msg-               */

.messages-container .msg-bubble  { }
.messages-container .msg-input   { }
.messages-container .msg-sidebar { }
```

Format: `[prefix]-[element]` or `[prefix]-[element]--[modifier]` (BEM-like).

Modal sub-elements follow the same convention:

```css
/* container: .orders-container */
/* prefix:     ord-             */

.orders-container .ord-modal-overlay   { }   /* full-screen backdrop */
.orders-container .ord-modal           { }   /* dialog card          */
.orders-container .ord-modal__title    { }
.orders-container .ord-modal__body     { }
.orders-container .ord-modal__actions  { }
```

### 3.3 States via `data-state`

For states toggled by JS — prefer `data-state` over modifier classes. The state is then visible directly in the HTML without inspecting computed classes:

```css
/* ✅ preferred — state is readable in the DOM */
.orders-container .order-card[data-state="cancelled"] .stepper-dot {
  background: var(--bs-danger);
}

/* also acceptable — BEM modifier */
.orders-container .order-card--cancelled .stepper-dot {
  background: var(--bs-danger);
}
```

In JS, always set both the Bootstrap class (for built-in styling) **and** `data-state` (for CSS hooks):

```js
el.classList.toggle('active', isActive);   // Bootstrap visual
el.dataset.state = isActive ? 'active' : '';  // CSS hook
```

### 3.4 CSS custom properties (tokens)

Widget tokens are scoped CSS variables declared on the container — section `0` of the stylesheet. This is the only place where design values live. Child rules consume tokens, never raw values:

```css
/* --- 0. Tokens --- */
.messages-container {
  --msg-bubble-radius:      0.75rem;
  --msg-bubble-sent-bg:     var(--bs-primary);
  --msg-bubble-sent-color:  #fff;
  --msg-bubble-recv-bg:     var(--bs-body-secondary);
  --msg-bubble-recv-color:  var(--bs-body-color);
  --msg-active-accent:      var(--bs-primary);
  --msg-input-max-height:   96px;
  --msg-anim-duration:      120ms;
}
```

Tokens can be overridden from outside without `!important`:

```css
/* Customise a single instance on the page */
.messages-container {
  --msg-bubble-sent-bg: #6f42c1;
}
```

**Token inheritance and modals.** Because modals are inside the container, they automatically inherit all container tokens. This is a key reason for the inside-container placement rule:

```css
/* ✅ Modal reads container token — works because modal is a descendant */
.orders-container .ord-modal {
  border-color: var(--ord-accent);       /* inherited from .orders-container */
  border-radius: var(--ord-card-radius); /* inherited from .orders-container */
}

/* ⚠️  If the modal were outside the container, these tokens would be undefined */
```

#### Token + Bootstrap coexistence rule

When a design system (Bootstrap) already provides a class that handles base styling — use it. Add BEM modifier classes alongside for token-driven overrides, but **never drop the Bootstrap class**:

```js
// ✅ correct — Bootstrap provides base colour + theme adaptation;
//              BEM modifier exposes token hook for external override
isSent
  ? 'bg-primary text-white msg-msg--sent'
  : 'bg-body-secondary text-body msg-msg--recv'

// ⚠️  wrong — Bootstrap class removed, dark-mode adaptation lost,
//              hardcoded colour (#fff) breaks theming
isSent ? 'msg-msg--sent' : 'msg-msg--recv'
```

The corresponding CSS modifier then only overrides what it needs to — it does **not** duplicate properties already handled by Bootstrap:

```css
/* ✅ correct — token hook only, no duplicate border-radius / padding */
.messages-container .msg-msg--sent {
  background: var(--msg-bubble-sent-bg);
  color:      var(--msg-bubble-sent-color);
}

/* ⚠️  wrong — duplicates rounded-3, and !important breaks overridability */
.messages-container .msg-msg--sent {
  background:    var(--msg-bubble-sent-bg);
  border-radius: var(--msg-bubble-radius) !important;
}
```

### 3.5 Modal styles — dedicated CSS section

Modal styles go in section `3` of the stylesheet (between child elements and states). The overlay uses `position: fixed` to cover the viewport; the dialog card is centered inside it:

```css
/* --- 3. Modals --- */

/* Backdrop */
.orders-container .ord-modal-overlay {
  position:        fixed;
  inset:           0;
  z-index:         1050;               /* above Bootstrap dropdowns (1000) */
  display:         flex;
  align-items:     center;
  justify-content: center;
  background:      rgba(0, 0, 0, .45);
}

/* [hidden] suppresses the overlay — no extra class needed */
.orders-container .ord-modal-overlay[hidden] {
  display: none;
}

/* Dialog card */
.orders-container .ord-modal {
  background:    var(--bs-body-bg);
  border-radius: var(--ord-card-radius, .5rem);
  box-shadow:    0 8px 32px rgba(0, 0, 0, .18);
  padding:       1.5rem;
  width:         min(480px, 90vw);
  max-height:    90vh;
  overflow-y:    auto;
}

.orders-container .ord-modal__title   { font-size: 1.125rem; font-weight: 600; margin-bottom: .5rem; }
.orders-container .ord-modal__body    { color: var(--bs-secondary-color); margin-bottom: 1.5rem; }
.orders-container .ord-modal__actions { display: flex; gap: .5rem; justify-content: flex-end; }
```

**`position: fixed` + scoped selectors — no conflict.** A `position: fixed` element escapes its ancestor's layout, but it still inherits CSS custom properties from its DOM ancestors. The container class prefix in the selector is required for scoping; it does not restrict the visual positioning.

### 3.6 Animations

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

All `@keyframes` blocks are collected in a dedicated section (`5. Animations`) — never inlined inside child-element sections.

Animate only `transform` and `opacity` — these run on the compositor thread and cause no reflow.

Modal open/close animation example:

```css
@keyframes ord-modal-in {
  from { opacity: 0; transform: scale(.95); }
  to   { opacity: 1; transform: scale(1);   }
}

.orders-container .ord-modal {
  animation: ord-modal-in 150ms ease-out both;
}
```

### 3.7 Responsive

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

All config, seed data, and logic live inside the class. Nothing leaks to the module scope.

```js
class WidgetController {

  // ─── 0. STATIC CONFIG ──────────────────────────────────────
  static DELAY_MS        = 1000;
  static MAX_PREVIEW     = 38;
  static FORBIDDEN_KEYS  = Object.freeze(['__proto__', 'constructor', 'prototype']);

  // ─── 0b. STATIC SEED DATA ──────────────────────────────────
  // Assigned after class body — see §4.10
  // static SEED_DATA = [...];

  // ─── 1. CONSTRUCTOR ────────────────────────────────────────
  /**
   * @param {string} selector - Root element selector, e.g. '.widget-container'
   * @param {Object} [opts]
   * @param {Array}  [opts.data]  - Data override; defaults to WidgetController.SEED_DATA
   * @param {number} [opts.delay] - Delay override; defaults to WidgetController.DELAY_MS
   */
  constructor(selector, opts = {}) {

    // 1a. Find container — silent exit if not found
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // 1b. Scope helpers (created once, used everywhere)
    const $ = sel => this._root.querySelector(sel);
    const $$ = sel => [...this._root.querySelectorAll(sel)];

    // 1c. Cache DOM references via data-ref
    this._list    = $('[data-ref="list"]');
    this._input   = $('[data-ref="input"]');
    this._sendBtn = $('[data-ref="send-btn"]');

    // 1d. Cache modal references (inside container, same $ scope)
    this._modalDelete = $('[data-ref="modal-delete"]');

    // 1e. Options with static defaults
    this._delay = opts.delay ?? WidgetController.DELAY_MS;

    // 1f. Data — opts override → static seed → validate
    const raw  = opts.data ?? WidgetController.SEED_DATA;
    const data = raw.filter(d => WidgetController._validate(d));

    // 1g. State — single source of truth
    this._state = {
      items:    data,
      activeId: null,
      loading:  false,
      modal:    null,   // { type: 'delete', targetId: '...' } | null
    };

    // 1h. AbortController for event listeners
    this._ac = new AbortController();

    // 1i. Boot
    this._render();
    this._bind();
  }

  // ─── 2. RENDER ─────────────────────────────────────────────
  /** @private */
  _render() { }

  /** @private */
  _renderItem(item) { }

  // ─── 3. ACTIONS ────────────────────────────────────────────
  /** @private */
  _select(id) {
    this._state.activeId = id;
    this._render();
  }

  /** @private */
  _submit() { }

  // ─── 4. EVENTS ─────────────────────────────────────────────
  /** @private */
  _bind() {
    const sig = { signal: this._ac.signal };

    this._root.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      switch (btn.dataset.action) {
        case 'send':          this._submit(); break;
        case 'remove':        this._handleRemove(btn.dataset.id); break;
        case 'back':          this._handleBack(); break;
        case 'modal-cancel':  this._closeModal(); break;
        case 'modal-confirm': this._handleModalConfirm(); break;
      }
    }, sig);

    this._input?.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this._submit(); }
    }, sig);

    // Close modal on Escape
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && this._state.modal) this._closeModal();
    }, sig);
  }

  // ─── 5. HELPERS ────────────────────────────────────────────

  /** @private */
  _scrollBottom() {
    this._messages.scrollTop = this._messages.scrollHeight;
  }

  /**
   * @param {string} s
   * @param {number} maxLen
   * @returns {string}
   * @private
   */
  _cut(s, maxLen) {
    return s.length > maxLen ? s.slice(0, maxLen) + '…' : s;
  }

  /**
   * Escapes all 7 OWASP-recommended HTML chars.
   * Use for metadata fields in innerHTML. User text always uses textContent.
   * @param {string} s
   * @returns {string}
   * @private
   */
  _esc(s) {
    return String(s ?? '')
      .replace(/&/g,  '&amp;')
      .replace(/</g,  '&lt;')
      .replace(/>/g,  '&gt;')
      .replace(/"/g,  '&quot;')
      .replace(/'/g,  '&#x27;')
      .replace(/\//g, '&#x2F;')
      .replace(/`/g,  '&#x60;');
  }

  // ─── 6. LIFECYCLE ──────────────────────────────────────────

  /**
   * Removes all event listeners. Call when the widget is unmounted.
   */
  destroy() {
    this._ac.abort();
  }

  // ─── 7. STATIC ─────────────────────────────────────────────

  /**
   * Guards against prototype pollution.
   * Validates both the object and any nested arrays.
   * @param {Object} obj
   * @returns {boolean}
   */
  static _validate(obj) {
    const forbidden = WidgetController.FORBIDDEN_KEYS;
    if (!obj || typeof obj !== 'object') return false;
    if (Object.keys(obj).some(k => forbidden.includes(k))) return false;
    for (const key of Object.keys(obj)) {
      if (Array.isArray(obj[key])) {
        for (const child of obj[key]) {
          if (!WidgetController._validate(child)) return false;
        }
      }
    }
    return true;
  }
}

// Seed data assigned after class declaration — keeps the class body readable
WidgetController.SEED_DATA = [
  // { id, ...fields }
];
```

### 4.2 Silent return — mandatory

The widget may be included on pages where its container does not exist. Never throw:

```js
// ✅ correct — no console noise on unrelated pages
this._root = document.querySelector(selector);
if (!this._root) return;

// ⚠️  wrong — throws on every page that doesn't have the widget
if (!this._root) throw new Error('WidgetController: container not found');
```

### 4.3 Private property convention

All internal properties use `_`. Public API methods carry no prefix:

```js
// ✅ internal — _ makes it immediately clear
this._root    = ...
this._state   = ...
this._sendBtn = ...

// ✅ public API — no prefix, callable by external code
controller.destroy()
controller.setItems(items)

// ⚠️  wrong — indistinguishable from public API
this.root  = ...
this.state = ...
```

### 4.4 DOM helpers `$` / `$$`

Declared in the constructor, scoped to `this._root`. They cannot reach outside the widget:

```js
// ✅ declare once, use everywhere inside the class
const $ = sel => this._root.querySelector(sel);
const $$ = sel => [...this._root.querySelectorAll(sel)];

this._form  = $('[data-ref="form"]');
this._items = $$('[data-ref="item"]');

// ⚠️  wrong — leaks out of scope, repetitive
this._form = document.querySelector('[data-ref="form"]');
```

Because modals are inside the container, the same `$` helper finds them. No `document.querySelector` needed:

```js
// ✅ correct — modal is inside this._root, $ finds it naturally
this._modalConfirm = $('[data-ref="modal-confirm"]');

// ⚠️  wrong — reaches outside the widget scope
this._modalConfirm = document.querySelector('[data-ref="modal-confirm"]');
```

`$$` also future-proofs dynamic content — the query runs at call time, not at cache time.

### 4.5 Static config and seed data

Config constants and mock/seed data belong inside the class as `static` properties — not as loose `const` declarations above the class. This keeps the module scope clean and the `INIT` block minimal:

```js
class OrdersController {
  static DELAY_MS       = 1000;
  static MAX_PREVIEW    = 38;
  static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
}

// Large data arrays are assigned after the class body for readability
OrdersController.SEED_DATA = [ /* ... */ ];
```

Internal references use `WidgetController.PROP_NAME`, never a bare identifier:

```js
// ✅ correct
this._delay = opts.delay ?? MessagesController.DELAY_MS;
const preview = this._cut(text, MessagesController.MAX_PREVIEW);

// ⚠️  wrong — bare name only works if const lives in outer scope
this._delay = opts.delay ?? DELAY_MS;
```

### 4.6 Constructor signature

Always `(selector, opts = {})`. The selector is required; everything else is optional with a static default:

```js
// ✅ minimal call — all defaults applied
new MessagesController('.messages-container');

// ✅ override only what you need
new MessagesController('.messages-container', { delay: 500 });
new MessagesController('.messages-container', { data: apiData });

// ⚠️  wrong — forces caller to know internal defaults
new MessagesController({ selector: '.messages-container', delay: 1000, data: SEED });

// ⚠️  wrong — passing default back to constructor is noise
new MessagesController('.messages-container', { delay: MessagesController.DELAY_MS });
```

Data validation (prototype pollution guard) runs inside the constructor, not in the `INIT` block:

```js
constructor(selector, opts = {}) {
  // ...
  const raw  = opts.data ?? WidgetController.SEED_DATA;
  const data = raw.filter(d => WidgetController._validate(d)); // ← inside, not outside
  // ...
}
```

### 4.7 State as single source of truth

The UI is always a projection of state. Never read state back from the DOM:

```js
// ✅ correct — update state first, then render
_select(id) {
  this._state.activeId = id;
  this._render();
}

// ⚠️  wrong — reading state from the DOM
_select(id) {
  const current = this._root.querySelector('.active')?.dataset.id;
  // ...logic driven by DOM instead of state
}
```

**Modal state follows the same rule.** The modal's visibility is derived from `this._state.modal`, never read from the DOM:

```js
// ✅ correct — modal visibility is derived from state
_renderModal() {
  const { modal } = this._state;
  this._modalDelete.hidden = modal?.type !== 'delete';
  if (modal?.type === 'delete') {
    this._modalDelete.querySelector('[data-ref="modal-body"]')
      .textContent = `Delete order #${this._esc(modal.targetId)}?`;
  }
}

// ⚠️  wrong — reading modal state from the DOM
_handleModalConfirm() {
  const isOpen = !this._modalDelete.hidden; // DOM as source of truth
}
```

### 4.8 Modal open / close pattern

Open by writing to state and re-rendering. Close the same way. Never manipulate `hidden` directly outside `_renderModal()`:

```js
// ✅ open a modal
_handleRemove(id) {
  this._state.modal = { type: 'delete', targetId: id };
  this._renderModal();
  // Optionally trap focus
  this._modalDelete.querySelector('button').focus();
}

// ✅ close any modal
_closeModal() {
  this._state.modal = null;
  this._renderModal();
  // Return focus to the element that opened the modal
  this._lastFocused?.focus();
}

// ✅ confirm action
_handleModalConfirm() {
  const { modal } = this._state;
  if (modal?.type === 'delete') this._delete(modal.targetId);
  this._closeModal();
}
```

Store the trigger element before opening so focus can be restored on close:

```js
_handleRemove(id) {
  this._lastFocused = document.activeElement;
  this._state.modal = { type: 'delete', targetId: id };
  this._renderModal();
}
```

### 4.9 AbortController for events

Every `addEventListener` call receives `{ signal: this._ac.signal }`. `destroy()` removes them all:

```js
_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click',   this._onClick,  sig);
  this._root.addEventListener('keydown', this._onKey,    sig);
  window.addEventListener('resize',      this._onResize, sig);
  // ^ window listeners are also removed on abort()

  // Escape key for modal close — on document, also covered by the signal
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && this._state.modal) this._closeModal();
  }, sig);
}

destroy() {
  this._ac.abort(); // removes every listener registered with this signal
}
```

### 4.10 Event delegation

One listener on the root covers all `[data-action]` targets, including elements added dynamically. Modal actions use the same mechanism — they are inside the container and therefore inside the root listener's scope:

```js
// ✅ correct — one listener, covers both widget and modal actions
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  switch (btn.dataset.action) {
    case 'send':          this._submit(); break;
    case 'remove':        this._handleRemove(btn.dataset.id); break;
    case 'back':          this._handleBack(); break;
    case 'modal-cancel':  this._closeModal(); break;
    case 'modal-confirm': this._handleModalConfirm(); break;
  }
}, { signal: this._ac.signal });

// ⚠️  wrong — separate listener on the modal button, leaks on destroy()
this._modalConfirmBtn.addEventListener('click', () => this._handleModalConfirm());
```

#### Extract inline handlers to named methods

When a delegated action has more than 2–3 lines of logic, extract it to a named private method. This keeps `_bind()` readable and the logic testable in isolation:

```js
// ✅ correct — logic in a named method
case 'back': this._handleBack(); break;

_handleBack() {
  this._root.classList.remove('msg-mob-chat');
  this._state.activeId = null;
  this._renderMessages();
  // ...
}

// ⚠️  wrong — complex logic buried inside _bind()
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (btn?.dataset.action === 'back') {
    this._root.classList.remove('msg-mob-chat');
    this._state.activeId = null;
    // ... 10 more lines
  }
});
```

### 4.11 XSS protection

User-supplied text — `textContent` only. Server/API metadata in `innerHTML` — always through `_esc()`:

```js
// ✅ correct
bubble.textContent = userMessage;                           // no XSS possible
li.innerHTML = `<span>${this._esc(apiData.name)}</span>`;  // metadata escaped

// ⚠️  dangerous
bubble.innerHTML = userMessage;
li.innerHTML = `<span>${apiData.name}</span>`;
```

### 4.12 Prototype pollution guard

`_validate()` is a `static` method. It checks both top-level keys and nested arrays. It is called inside the constructor, not in `INIT`:

```js
static _validate(obj) {
  const forbidden = WidgetController.FORBIDDEN_KEYS;
  if (!obj || typeof obj !== 'object') return false;
  if (Object.keys(obj).some(k => forbidden.includes(k))) return false;
  // Validate nested message/item arrays too
  for (const key of Object.keys(obj)) {
    if (Array.isArray(obj[key])) {
      for (const child of obj[key]) {
        if (!WidgetController._validate(child)) return false;
      }
    }
  }
  return true;
}
```

---

## 5. Initialization

### 5.1 Standard pattern — always one line

```js
document.addEventListener('DOMContentLoaded', () => {
  new MessagesController('.messages-container');
});
```

`DOMContentLoaded` fires when the DOM is fully parsed, regardless of `<script>` placement. Data validation and defaults are handled by the constructor — `INIT` has no business logic.

### 5.2 With overrides

```js
document.addEventListener('DOMContentLoaded', () => {
  new MessagesController('.messages-container', { data: apiData, delay: 500 });
});
```

### 5.3 Multiple instances on one page

```js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.messages-container').forEach(el => {
    new MessagesController(`#${el.id}`);
  });
});
```

Because all DOM lookups are scoped to `this._root`, multiple instances of the same widget never interfere — even with identical `data-ref` values inside each one. Each instance also has its own modal elements, so modals from different instances never collide.

---

## 6. Naming Conventions

### 6.1 Classes and files

| What | Convention | Example |
|---|---|---|
| ES6 class | PascalCase + `Controller` suffix | `MessagesController` |
| CSS container | kebab-case + `-container` suffix | `.messages-container` |
| CSS child prefix | short kebab | `msg-` |
| BEM modifier | `[prefix]-[element]--[modifier]` | `.msg-msg--sent` |
| Modal overlay | `[prefix]-modal-overlay` | `.ord-modal-overlay` |
| Modal dialog | `[prefix]-modal` | `.ord-modal` |
| HTML file | `feature-hash.html` | `correspondence-4e.html` |
| Instance variable | camelCase | `const messagesController` |

### 6.2 `data-*` attributes

| Purpose | Attribute | Example |
|---|---|---|
| DOM reference (cached in constructor) | `data-ref` | `data-ref="send-btn"` |
| Action trigger (delegated handler) | `data-action` | `data-action="send"` |
| Modal open trigger | `data-action` | `data-action="modal-open-delete"` |
| Modal cancel button | `data-action` | `data-action="modal-cancel"` |
| Modal confirm button | `data-action` | `data-action="modal-confirm"` |
| Record identifier | `data-id` | `data-id="order-42"` |
| JS-driven element state (also drives CSS) | `data-state` | `data-state="active"` |

### 6.3 Static properties

| What | Convention | Example |
|---|---|---|
| Config constant | SCREAMING_SNAKE | `static DELAY_MS = 1000` |
| Frozen list | SCREAMING_SNAKE | `static FORBIDDEN_KEYS = Object.freeze([...])` |
| Seed data array | SCREAMING_SNAKE | `static SEED_DATA = [...]` (or assigned after class body) |

---

## 7. New Widget Checklist

```
HTML
  [ ] Container uses a semantic tag, class only (no id)
  [ ] DOM references use data-ref, actions use data-action
  [ ] JS-driven states use data-state
  [ ] data-id on all list items
  [ ] ARIA: role, aria-label, aria-live where applicable
  [ ] Keyboard navigation implemented for interactive lists
  [ ] Modals placed inside the container, before closing tag
  [ ] Each modal has role="dialog", aria-modal="true", aria-labelledby, hidden
  [ ] Modal buttons use data-action="modal-cancel" / "modal-confirm"

CSS
  [ ] Section 0 — tokens declared on the container
  [ ] Every child selector starts with .widget-container (modals included)
  [ ] Modal styles in dedicated section 3 (Modals)
  [ ] Modal overlay uses position: fixed; modal card uses container tokens
  [ ] BEM modifiers used alongside Bootstrap classes, not instead of them
  [ ] BEM modifier CSS does not duplicate what Bootstrap already provides
  [ ] No !important inside modifier rules
  [ ] @keyframes names carry the widget prefix
  [ ] All @keyframes collected in section 5 (Animations)
  [ ] @media breakpoints match the design system

JS
  [ ] No loose constants above the class — everything is static
  [ ] Seed data assigned as WidgetController.SEED_DATA after class body
  [ ] Constructor signature is (selector, opts = {})
  [ ] Silent return if container is not found
  [ ] $ / $$ helpers declared in constructor, scoped to this._root
  [ ] DOM references cached via data-ref in constructor, nowhere else
  [ ] Modal references cached via data-ref using the same $ helper
  [ ] opts resolved with static defaults (opts.delay ?? ClassName.DELAY_MS)
  [ ] Data validated inside constructor, not in INIT
  [ ] All internal properties use _ prefix
  [ ] State is the single source of truth — never read state from DOM
  [ ] Modal visibility derived from this._state.modal, not from DOM
  [ ] _closeModal() restores focus to this._lastFocused
  [ ] AbortController: this._ac in constructor, signal passed to every addEventListener
  [ ] Escape key listener uses the same AbortController signal
  [ ] destroy() calls this._ac.abort()
  [ ] All delegated actions go through one root click listener + switch
  [ ] Modal actions (modal-cancel, modal-confirm) handled in the same switch
  [ ] Complex action handlers extracted to named _handleXxx() methods
  [ ] User text via textContent, never innerHTML
  [ ] Metadata escaped via _esc() before innerHTML
  [ ] External data validated via static _validate()

INIT
  [ ] DOMContentLoaded wraps init
  [ ] Init is a single line: new WidgetController('.widget-container')
  [ ] No data filtering, no option assembly in INIT — all inside constructor
```
