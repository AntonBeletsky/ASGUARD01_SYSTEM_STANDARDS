# Containerization Guide — v4
## Widget Standard: HTML · CSS · JavaScript
### No Spaghetti · No jQuery · No ID/Class JS Hooks · Secure · Fast

---

## Priority Order (read this before everything else)

The rules in this guide are arranged in a strict hierarchy. When two rules conflict — the one ranked higher wins.

```
1. DATA ATTRIBUTES  — absolute foundation        ← inviolable, overridden by nothing
2. CODE CLEANLINESS — structure, isolation, readability ← applies everywhere unless it conflicts with #3
3. SECURITY         — XSS, pollution, escaping   ← overrides any "convenience" from #2
4. PERFORMANCE      — no Violation, no thrashing ← final audit, does not reshape architecture
```

Containerization sits **above** this chain — it defines the shape of a widget. Everything else operates inside that shape.

---

## Law Zero: JS operates exclusively through data attributes

This is the only rule with no exceptions. Violating it invalidates the entire widget.

```html
<!-- ✅ CORRECT — JS hook via data attribute -->
<button class="btn btn-primary" data-action="send">Send</button>
<div class="msg-list"           data-ref="messages"></div>
<li  class="ord-item"           data-id="order-42" data-state="active"></li>

<!-- ❌ FORBIDDEN — class as JS hook -->
<button class="btn btn-primary js-send-btn">Send</button>

<!-- ❌ FORBIDDEN — id as JS hook -->
<button id="send-btn" class="btn btn-primary">Send</button>

<!-- ❌ FORBIDDEN — jQuery -->
$('#send-btn').on('click', handler);
$('.js-send-btn').show();
```

### data attribute reference table

| Attribute | Purpose | Example |
|---|---|---|
| `data-ref` | DOM reference — cached in constructor once | `data-ref="send-btn"` |
| `data-action` | Delegated event handler trigger | `data-action="send"` |
| `data-id` | Record identifier | `data-id="order-42"` |
| `data-state` | JS-driven state, also consumed by CSS | `data-state="active"` |

### The only legal exceptions for `id`

`id` is allowed **only** in two situations — both exclusively for HTML/ARIA, never for JS queries:

```html
<!-- ✅ ARIA reference — id is semantically required here -->
<div role="dialog" aria-labelledby="modal-title-id" hidden>
  <h2 id="modal-title-id">Confirm deletion</h2>
</div>

<!-- ✅ Anchor link -->
<h2 id="section-payments">Payments</h2>
<a href="#section-payments">Go to payments</a>
```

JS never looks up these elements via `getElementById` — it finds them through `data-ref` or through the `aria-labelledby` attribute value.

### Forbidden query methods

```js
// ❌ ALL OF THESE ARE FORBIDDEN
document.getElementById('anything')
document.querySelector('.some-class')
document.querySelector('#some-id')
document.getElementsByClassName('something')
$('#anything')
$('.anything')

// ✅ ONLY THESE ARE ALLOWED
this._root.querySelector('[data-ref="name"]')    // via data-ref
this._root.querySelector('[data-action="name"]') // via data-action
e.target.closest('[data-action]')                // in delegation handlers
document.querySelectorAll('.widget-container')   // bootstrap all instances — by container CSS class
document.getElementById(id)                      // only for ARIA/anchors, never for logic
```

---

## 1. File Structure

Each widget is a self-contained HTML file. Section order is fixed:

```
<style>
  /* 0. Tokens (CSS custom properties)  */
  /* 1. Container layout                */
  /* 2. Child elements                  */
  /* 3. Modal(s)                        */
  /* 4. States                          */
  /* 5. Animations (@keyframes)         */
  /* 6. Responsive (@media)             */
</style>

<section class="widget-container">
  <!-- widget markup -->

  <!-- Modals — always inside the container, before the closing tag -->
  <div class="wgt-modal-overlay" data-ref="modal-confirm"
       role="dialog" aria-modal="true" aria-labelledby="wgt-modal-title" hidden>
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
   *   ├── static FORBIDDEN_KEYS
   *   ├── static config props
   *   ├── static seed data
   *   ├── constructor
   *   │     ├── find root (silent return)
   *   │     ├── $ / $$ helpers
   *   │     ├── cache DOM refs via data-ref
   *   │     ├── validate & init state
   *   │     ├── AbortController
   *   │     └── _render() + _bind()
   *   ├── _render() methods
   *   ├── _handle() action methods
   *   ├── _bind() — one listener + switch
   *   ├── _esc() — XSS escaping
   *   ├── destroy()
   *   └── static _validate()
   */

  /* 2. INIT — DOMContentLoaded, one line */
</script>
```

---

## 2. HTML

### 2.1 Container

Semantic tag, class only — no `id` on the root element:

```html
<!-- ✅ correct -->
<section class="orders-container" aria-label="Order list">

<!-- ❌ wrong — id creates a global coupling with JS -->
<section id="orders-module" class="orders-container">
```

### 2.2 JS hooks — data attributes only

Class is for CSS. `data-ref` / `data-action` is for JS. They never mix:

```html
<!-- ✅ correct — hooks are separated from styles -->
<button class="btn btn-primary" data-action="send">Send</button>
<div class="ord-list"           data-ref="list"></div>
<li  class="ord-item"           data-id="order-42" data-state="new"></li>

<!-- ❌ wrong — class carries double responsibility -->
<button class="btn btn-primary js-send-btn">Send</button>

<!-- ❌ wrong — id as JS hook -->
<button id="send-btn" class="btn btn-primary">Send</button>
```

### 2.3 Modals — inside the container only

Modals live **inside** the container, before the closing tag. Placement outside is a violation:

```html
<section class="orders-container">

  <!-- ... main widget markup ... -->

  <!-- ✅ correct — modal inside, tokens are inherited -->
  <div class="ord-modal-overlay" data-ref="modal-delete"
       role="dialog" aria-modal="true" aria-labelledby="ord-modal-title" hidden>
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

<!-- ❌ wrong — outside container: tokens break, styles leak -->
<div class="ord-modal-overlay">...</div>
```

Why inside: CSS custom properties are inherited down the DOM tree. A modal outside the container cannot see `--ord-*` tokens declared on `.orders-container`. Additionally, the CSS scoping rule (§3.1) requires every selector to begin with the container class — impossible to satisfy from outside.

`position: fixed` behaves the same regardless of DOM position — the modal will still cover the full screen.

### 2.4 ARIA

Minimum required:

```html
<!-- Interactive lists -->
<ul role="listbox" aria-label="Order list" aria-activedescendant="">
  <li role="option" aria-selected="false" tabindex="0" id="item-1">...</li>
</ul>

<!-- Live regions — updates announced by screen readers -->
<div role="log" aria-live="polite" aria-atomic="false">
  <!-- dynamically appended messages -->
</div>

<!-- Modal dialog -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title-id" hidden>
  <h2 id="modal-title-id">Confirm deletion</h2>
</div>
```

Keyboard for listbox: `↑↓` move focus, `Home`/`End` jump to ends, `Enter`/`Space` activate.
Keyboard for modal: `Escape` closes, focus returns to the trigger element.

---

## 3. CSS

### 3.1 Scoping — the cardinal rule

**Every CSS selector in a widget must begin with the container class name. No exceptions:**

```css
/* ✅ correct — styles are isolated */
.orders-container .ord-card        { }
.orders-container .ord-card:hover  { }
.orders-container .ord-modal       { }

/* ❌ wrong — styles leak onto the entire page */
.ord-card  { }
.ord-modal { }
```

Modals are not exempt. `position: fixed` does not waive the scoping rule:

```css
/* ✅ correct — scoped even though visually full-screen */
.orders-container .ord-modal-overlay { position: fixed; inset: 0; }

/* ❌ wrong — leaks globally */
.ord-modal-overlay { position: fixed; inset: 0; }
```

### 3.2 Class naming — prefix

All child classes get a unique short prefix abbreviated from the container name:

```css
/* container: .messages-container → prefix: msg- */
.messages-container .msg-bubble  { }
.messages-container .msg-input   { }

/* BEM modifier: [prefix]-[element]--[modifier] */
.messages-container .msg-bubble--sent { }
.messages-container .msg-bubble--recv { }

/* container: .orders-container → prefix: ord- */
.orders-container .ord-modal-overlay { }
.orders-container .ord-modal         { }
.orders-container .ord-modal__title  { }
```

### 3.3 States via `data-state`

JS-driven states go through `data-state`, not modifier classes:

```css
/* ✅ preferred — state is readable directly in the HTML */
.orders-container .ord-item[data-state="cancelled"] .stepper-dot {
  background: var(--bs-danger);
}

/* also acceptable — BEM modifier */
.orders-container .ord-item--cancelled .stepper-dot {
  background: var(--bs-danger);
}
```

In JS, set both — Bootstrap class for visuals and `data-state` for CSS hooks:

```js
el.classList.toggle('active', isActive);
el.dataset.state = isActive ? 'active' : '';
```

### 3.4 CSS custom properties (tokens)

Tokens are declared on the container — section `0` of the stylesheet. Child rules consume tokens, never raw values:

```css
/* --- 0. Tokens --- */
.orders-container {
  --ord-accent:       var(--bs-primary);
  --ord-card-radius:  .5rem;
  --ord-anim-dur:     150ms;
}

/* Child rules — tokens only */
.orders-container .ord-card {
  border-radius: var(--ord-card-radius);
  border-color:  var(--ord-accent);
}

/* Modal inherits tokens automatically — it is inside the container */
.orders-container .ord-modal {
  border-radius: var(--ord-card-radius);
}
```

Bootstrap classes are never dropped — BEM modifiers only add what Bootstrap does not already cover:

```css
/* ✅ correct — token hook only, no Bootstrap duplication */
.messages-container .msg-bubble--sent {
  background: var(--msg-bubble-sent-bg);
  color:      var(--msg-bubble-sent-color);
}

/* ❌ wrong — duplicates Bootstrap + !important */
.messages-container .msg-bubble--sent {
  background:    var(--msg-bubble-sent-bg);
  border-radius: var(--msg-bubble-radius) !important;
  padding:       .5rem 1rem !important;
}
```

### 3.5 Modal styles — section 3

```css
/* --- 3. Modals --- */

.orders-container .ord-modal-overlay {
  position:        fixed;
  inset:           0;
  z-index:         1050;               /* above Bootstrap dropdowns (1000) */
  display:         flex;
  align-items:     center;
  justify-content: center;
  background:      rgba(0, 0, 0, .45);
}

.orders-container .ord-modal-overlay[hidden] {
  display: none;
}

.orders-container .ord-modal {
  background:    var(--bs-body-bg);
  border-radius: var(--ord-card-radius, .5rem);
  box-shadow:    0 8px 32px rgba(0, 0, 0, .18);
  padding:       1.5rem;
  width:         min(480px, 90vw);
  max-height:    90vh;
  overflow-y:    auto;
  animation:     ord-modal-in var(--ord-anim-dur, 150ms) ease-out both;
}

.orders-container .ord-modal__title   { font-size: 1.125rem; font-weight: 600; margin-bottom: .5rem; }
.orders-container .ord-modal__body    { color: var(--bs-secondary-color); margin-bottom: 1.5rem; }
.orders-container .ord-modal__actions { display: flex; gap: .5rem; justify-content: flex-end; }
```

### 3.6 Animations

`@keyframes` names must carry the widget prefix — keyframe names are global:

```css
/* --- 5. Animations --- */

/* ✅ correct — prefix prevents name collisions */
@keyframes ord-modal-in {
  from { opacity: 0; transform: scale(.95); }
  to   { opacity: 1; transform: scale(1);   }
}

/* ❌ wrong — may collide with another widget on the same page */
@keyframes modal-in { }
```

Animate only `transform` and `opacity` — these run on the compositor thread with no reflow or repaint.

---

## 4. JavaScript

### 4.1 Class structure

```js
class WidgetController {

  // ─── 0. STATIC CONFIG ──────────────────────────────────────
  static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
  static DELAY_MS       = 1000;
  static MAX_PREVIEW    = 38;

  // ─── 1. CONSTRUCTOR ────────────────────────────────────────
  constructor(selector, opts = {}) {

    // 1a. Find container — silent exit if not found
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // 1b. Helpers — scoped to this._root, cannot reach outside
    const $ = sel => this._root.querySelector(sel);
    const $$ = sel => [...this._root.querySelectorAll(sel)];

    // 1c. Cache DOM references via data-ref — once, here, nowhere else
    this._list    = $('[data-ref="list"]');
    this._input   = $('[data-ref="input"]');
    this._sendBtn = $('[data-ref="send-btn"]');

    // 1d. Modals — same $ helper, they are inside the container
    this._modalDelete = $('[data-ref="modal-delete"]');

    // 1e. Options with static defaults
    this._delay = opts.delay ?? WidgetController.DELAY_MS;

    // 1f. Data — validate before use
    const raw  = opts.data ?? WidgetController.SEED_DATA;
    const data = raw.filter(d => WidgetController._validate(d));

    // 1g. State — single source of truth
    this._state = {
      items:    data,
      activeId: null,
      loading:  false,
      modal:    null,  // { type: 'delete', targetId: '...' } | null
    };

    // 1h. AbortController — one abort() kills all listeners
    this._ac = new AbortController();

    // 1i. Boot
    this._render();
    this._bind();
  }

  // ─── 2. RENDER ─────────────────────────────────────────────

  _render() {
    // All rendering is derived from this._state
    // Never read state back from the DOM
    this._renderList();
    this._renderModal();
  }

  _renderList() {
    // ✅ user text → textContent only
    // ✅ API / server data in innerHTML → always through _esc()
    this._list.innerHTML = this._state.items.map(item => `
      <li class="ord-item"
          data-id="${this._esc(item.id)}"
          data-state="${this._esc(item.status)}">
        <span class="ord-item__name">${this._esc(item.name)}</span>
        <button class="btn btn-sm btn-danger" data-action="remove" data-id="${this._esc(item.id)}">
          Remove
        </button>
      </li>
    `).join('');
  }

  _renderModal() {
    // Modal visibility derived from state — never from DOM
    const { modal } = this._state;
    this._modalDelete.hidden = modal?.type !== 'delete';
    if (modal?.type === 'delete') {
      // textContent — because targetId is user-supplied data
      this._modalDelete.querySelector('[data-ref="modal-body"]')
        .textContent = `Delete order #${modal.targetId}?`;
    }
  }

  // ─── 3. ACTIONS ────────────────────────────────────────────

  _handleRemove(id) {
    this._lastFocused = document.activeElement;
    this._state.modal = { type: 'delete', targetId: id };
    this._renderModal();
    this._modalDelete.querySelector('button').focus();
  }

  _handleModalConfirm() {
    const { modal } = this._state;
    if (modal?.type === 'delete') this._deleteItem(modal.targetId);
    this._closeModal();
  }

  _closeModal() {
    this._state.modal = null;
    this._renderModal();
    this._lastFocused?.focus();
  }

  _deleteItem(id) {
    this._state.items = this._state.items.filter(i => i.id !== id);
    this._renderList();
  }

  // ─── 4. EVENTS ─────────────────────────────────────────────

  _bind() {
    const sig = { signal: this._ac.signal };

    // One listener on the root — covers widget and modals alike
    this._root.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;

      switch (btn.dataset.action) {
        case 'send':          this._submit(); break;
        case 'remove':        this._handleRemove(btn.dataset.id); break;
        case 'modal-cancel':  this._closeModal(); break;
        case 'modal-confirm': this._handleModalConfirm(); break;
      }
    }, sig);

    // passive: true — scroll must never be blocked
    this._root.addEventListener('scroll', this._onScroll.bind(this),
      { signal: this._ac.signal, passive: true });

    this._input?.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this._submit(); }
    }, sig);

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && this._state.modal) this._closeModal();
    }, sig);
  }

  // ─── 5. HELPERS ────────────────────────────────────────────

  /**
   * Escapes all 7 OWASP-recommended HTML characters.
   * Required for all external data in innerHTML — both user input AND server data.
   * User text that goes into textContent does not need this.
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

  _cut(s, maxLen) {
    return s.length > maxLen ? s.slice(0, maxLen) + '…' : s;
  }

  _throttle(fn, limit) {
    let last = 0;
    return (...args) => {
      const now = Date.now();
      if (now - last >= limit) { last = now; fn(...args); }
    };
  }

  // ─── 6. LIFECYCLE ──────────────────────────────────────────

  destroy() {
    this._ac.abort(); // removes every listener registered with this signal
  }

  // ─── 7. STATIC ─────────────────────────────────────────────

  /**
   * Guards against prototype pollution.
   * Called inside the constructor, not in INIT.
   * Validates the object and any nested arrays recursively.
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

// Seed data assigned after the class body — keeps the class itself readable
WidgetController.SEED_DATA = [];
```

### 4.2 Silent return — mandatory

```js
// ✅ correct — safe to include on any page
this._root = document.querySelector(selector);
if (!this._root) return;

// ❌ wrong — throws on every page that does not have this widget
if (!this._root) throw new Error('container not found');
```

### 4.3 `$` / `$$` helpers

Declared in the constructor, scoped to `this._root`. They physically cannot reach outside:

```js
const $ = sel => this._root.querySelector(sel);
const $$ = sel => [...this._root.querySelectorAll(sel)];

// ✅ All queries go through the helpers
this._list  = $('[data-ref="list"]');
this._modal = $('[data-ref="modal-delete"]');

// ❌ Forbidden — reaches outside the container
this._list  = document.querySelector('[data-ref="list"]');
this._modal = document.getElementById('modal-delete');
```

### 4.4 State as single source of truth

The UI is a projection of state. Never read state from the DOM:

```js
// ✅ correct — update state, then render
_select(id) {
  this._state.activeId = id;
  this._render();
}

// ❌ wrong — reading state from the DOM
_select(id) {
  const current = this._root.querySelector('[data-state="active"]')?.dataset.id;
}
```

### 4.5 XSS — the rule security overrides convenience

```js
// ✅ user text — textContent ONLY
bubble.textContent = userMessage;

// ✅ API / server data in innerHTML — ONLY through _esc()
li.innerHTML = `
  <span class="name">${this._esc(apiData.name)}</span>
  <span class="date">${this._esc(apiData.date)}</span>
`;

// ❌ FORBIDDEN — raw innerHTML with any external data
bubble.innerHTML = userMessage;
li.innerHTML = `<span>${apiData.name}</span>`;

// ❌ FORBIDDEN — even if it looks safe
container.innerHTML = serverRenderedHtml;
```

The rule: if the data did not originate in your code — it goes through `_esc()` or `textContent`.

### 4.6 Prototype pollution — guard in the constructor

`_validate()` runs inside the constructor before any data reaches state. No logic lives in the INIT block:

```js
// ✅ correct — validation inside the constructor
constructor(selector, opts = {}) {
  const raw  = opts.data ?? WidgetController.SEED_DATA;
  const data = raw.filter(d => WidgetController._validate(d));
  this._state = { items: data, ... };
}

// ❌ wrong — logic in INIT
document.addEventListener('DOMContentLoaded', () => {
  const safeData = rawData.filter(d => validate(d)); // logic does not belong here
  new OrdersController('.orders-container', { data: safeData });
});
```

### 4.7 AbortController — cleanup in one call

Every `addEventListener` is registered with `{ signal: this._ac.signal }`. `destroy()` is one line:

```js
_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click',   handler, sig);
  this._root.addEventListener('keydown', handler, sig);
  window.addEventListener('resize',      handler, sig);
  document.addEventListener('keydown',   handler, sig);

  // scroll and touch — passive: true is mandatory
  this._root.addEventListener('scroll', handler, { ...sig, passive: true });
}

destroy() {
  this._ac.abort(); // all listeners above removed simultaneously
}
```

### 4.8 Event delegation

One listener on the root via `e.target.closest('[data-action]')` covers the entire widget including modals and dynamically added elements:

```js
// ✅ correct — one listener, everything through switch
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  switch (btn.dataset.action) {
    case 'send':          this._submit(); break;
    case 'remove':        this._handleRemove(btn.dataset.id); break;
    case 'modal-cancel':  this._closeModal(); break;
    case 'modal-confirm': this._handleModalConfirm(); break;
  }
}, { signal: this._ac.signal });

// ❌ wrong — separate listeners on individual elements
this._sendBtn.addEventListener('click', () => this._submit());
this._modalConfirmBtn.addEventListener('click', () => this._handleModalConfirm());
```

Complex logic is extracted to a named method, never left inline:

```js
// ✅ correct
case 'remove': this._handleRemove(btn.dataset.id); break;

_handleRemove(id) {
  this._lastFocused = document.activeElement;
  this._state.modal = { type: 'delete', targetId: id };
  this._renderModal();
}

// ❌ wrong — logic buried inside the switch
case 'remove': {
  const focused = document.activeElement;
  this._state.modal = { type: 'delete', targetId: btn.dataset.id };
  this._renderModal();
  // ... 10 more lines
  break;
}
```

---

## 5. Performance — final audit

This section does not reshape the architecture. It is a checklist applied after the code is written according to the rules above.

### 5.1 Layout Thrashing

Never read geometry immediately after writing styles in the same loop:

```js
// ❌ BAD — forced reflow on every iteration
items.forEach(el => {
  el.style.width = '100px';
  const h = el.offsetHeight; // reading after writing → forced reflow
  el.style.height = h * 2 + 'px';
});

// ✅ GOOD — all reads first, then all writes
const heights = items.map(el => el.offsetHeight); // all reads at once
items.forEach((el, i) => {
  el.style.width  = '100px';
  el.style.height = heights[i] * 2 + 'px';        // all writes at once
});
```

Properties that trigger forced reflow when read:
`offsetTop`, `offsetHeight`, `scrollTop`, `clientWidth`, `getBoundingClientRect()`, `getComputedStyle()`.

### 5.2 Passive listeners for scroll and touch

```js
// ❌ BAD — browser waits for handler to finish before scrolling → [Violation]
this._root.addEventListener('scroll', handler);
window.addEventListener('touchstart', handler);

// ✅ GOOD — browser scrolls immediately, does not wait
this._root.addEventListener('scroll',    handler, { signal: this._ac.signal, passive: true });
window.addEventListener('touchstart',    handler, { signal: this._ac.signal, passive: true });
window.addEventListener('touchmove',     handler, { signal: this._ac.signal, passive: true });
```

### 5.3 Throttle for high-frequency events

```js
// scroll, mousemove, resize can fire hundreds of times per second
_bind() {
  this._root.addEventListener('scroll',
    this._throttle(this._onScroll.bind(this), 16),
    { signal: this._ac.signal, passive: true }); // ~60fps
}
```

### 5.4 Styles via classList

```js
// ❌ BAD — potentially 3 separate reflows
el.style.width  = '100px';
el.style.height = '100px';
el.style.color  = 'red';

// ✅ GOOD — one reflow
el.classList.add('is-active');
// CSS: .widget-container .el.is-active { width: 100px; height: 100px; color: red; }

// or as one assignment
el.style.cssText = 'width:100px; height:100px; color:red';
```

### 5.5 Batch DOM insertions

```js
// ❌ BAD — reflow on every appendChild
items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name;
  this._list.appendChild(li);
});

// ✅ GOOD — one reflow
// Option 1: innerHTML (recommended — simpler and equally fast)
this._list.innerHTML = items.map(item =>
  `<li data-id="${this._esc(item.id)}">${this._esc(item.name)}</li>`
).join('');

// Option 2: DocumentFragment (use when existing listeners must be preserved)
const frag = document.createDocumentFragment();
items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item.name; // textContent is safe without _esc()
  frag.appendChild(li);
});
this._list.appendChild(frag);
```

---

## 6. Initialization

### 6.1 Standard pattern — always one line

```js
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container');
});
```

`DOMContentLoaded` fires when the DOM is fully parsed regardless of `<script>` placement. All logic lives in the constructor. INIT contains nothing except `new`.

### 6.2 With overrides

```js
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container', { data: apiData, delay: 500 });
});
```

### 6.3 Multiple instances

```js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.orders-container').forEach(el => {
    new OrdersController(el);
  });
});
```

All DOM lookups are scoped to `this._root` — multiple instances on one page never conflict, even with identical `data-ref` values inside each one.

---

## 7. Naming Conventions

### 7.1 Classes and files

| What | Convention | Example |
|---|---|---|
| ES6 class | PascalCase + `Controller` | `OrdersController` |
| CSS container | kebab + `-container` | `.orders-container` |
| CSS child prefix | short kebab | `ord-` |
| BEM modifier | `[prefix]-[el]--[mod]` | `.ord-item--cancelled` |
| Modal overlay | `[prefix]-modal-overlay` | `.ord-modal-overlay` |
| HTML file | `feature-hash.html` | `orders-4f.html` |

### 7.2 data attributes

| Purpose | Attribute | Example |
|---|---|---|
| DOM reference (cached in constructor) | `data-ref` | `data-ref="send-btn"` |
| Action trigger | `data-action` | `data-action="send"` |
| Open a modal | `data-action` | `data-action="modal-open-delete"` |
| Cancel a modal | `data-action` | `data-action="modal-cancel"` |
| Confirm a modal | `data-action` | `data-action="modal-confirm"` |
| Record identifier | `data-id` | `data-id="order-42"` |
| JS-driven state (also a CSS hook) | `data-state` | `data-state="active"` |

### 7.3 Static properties

| What | Convention | Example |
|---|---|---|
| Config constant | SCREAMING_SNAKE | `static DELAY_MS = 1000` |
| Frozen list | SCREAMING_SNAKE | `static FORBIDDEN_KEYS = Object.freeze([...])` |
| Seed data | SCREAMING_SNAKE | `static SEED_DATA = [...]` |

---

## 8. Pre-Commit Checklist

### Law Zero (data attributes)
- [ ] No `getElementById` in any JS file (except ARIA / anchor links)
- [ ] No `querySelector('.class')` for logic
- [ ] No `querySelector('#id')` for logic
- [ ] No `getElementsByClassName`
- [ ] No jQuery (`$`, `jQuery`)
- [ ] No `js-*` classes in HTML
- [ ] All JS hooks are exclusively `data-ref`, `data-action`, `data-id`, `data-state`
- [ ] `document.querySelector` is used only for bootstrap initialization by the container CSS class

### HTML
- [ ] Container uses a semantic tag, class only (no `id`)
- [ ] Modals placed inside the container, before the closing tag
- [ ] Every modal has `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, `hidden`
- [ ] ARIA: `role`, `aria-label`, `aria-live` where applicable
- [ ] Keyboard navigation implemented for interactive lists

### CSS
- [ ] Every selector starts with the container class
- [ ] Section 0 — tokens declared on the container
- [ ] Modal styles in section 3
- [ ] `@keyframes` names carry the widget prefix
- [ ] All `@keyframes` collected in section 5
- [ ] No `!important` inside modifier rules
- [ ] Animations use only `transform` and `opacity`

### JS — architecture
- [ ] No loose constants above the class — everything is `static`
- [ ] Constructor signature is `(selector, opts = {})`
- [ ] Silent return when container is not found
- [ ] `$` / `$$` helpers declared in constructor, scoped to `this._root`
- [ ] DOM references cached via `data-ref` in constructor, nowhere else
- [ ] State is the single source of truth — DOM is never read as a data source
- [ ] Modal visibility derived from `this._state.modal`, not from DOM
- [ ] One root click listener + switch for all `[data-action]`
- [ ] Complex handlers extracted to named `_handleXxx()` methods
- [ ] `AbortController` in constructor, signal passed to every `addEventListener`
- [ ] `destroy()` calls `this._ac.abort()`
- [ ] `_closeModal()` restores focus to `this._lastFocused`

### JS — security
- [ ] User text via `textContent` only, never `innerHTML`
- [ ] All data in `innerHTML` goes through `_esc()` without exception
- [ ] External data validated via `static _validate()` inside the constructor
- [ ] `FORBIDDEN_KEYS` includes `__proto__`, `constructor`, `prototype`

### JS — performance
- [ ] No geometry reads after style writes in the same loop (Layout Thrashing)
- [ ] `scroll`, `touchstart`, `touchmove` use `passive: true`
- [ ] `scroll`, `mousemove`, `resize` use throttle / debounce
- [ ] Styles changed via `classList` or `cssText`, not via `.style.*` one property at a time
- [ ] No `[Violation]` warnings in the browser console

### INIT
- [ ] `DOMContentLoaded` wraps initialization
- [ ] Initialization is one line: `new WidgetController('.widget-container')`
- [ ] No logic in INIT — everything lives in the constructor
