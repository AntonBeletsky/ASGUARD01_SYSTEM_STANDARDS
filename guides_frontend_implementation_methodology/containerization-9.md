# Containerization Guide — v9
## Widget Standard: HTML · CSS · JavaScript
### No Spaghetti · No jQuery · No ID/Class JS Hooks · Secure · Fast

---

## Changelog v8 → v9

- **§4.1** — class structure template updated: `static DEFAULTS` added, `_readDataAttrs()` added to constructor flow and class skeleton
- **§4.2** — NEW: Three-Layer Configuration System — full reference for `static DEFAULTS` → constructor `opts` → `_readDataAttrs()` chain
  - **§4.2.1** Overview and resolution order
  - **§4.2.2** Layer 1 — static DEFAULTS
  - **§4.2.3** Layer 2 — constructor opts
  - **§4.2.4** Layer 3 — `_readDataAttrs()` method
  - **§4.2.5** Type coercion rules for data attribute values
  - **§4.2.6** Naming config data attributes
- **§4.3–§4.11** — old §4.2–§4.10 renumbered to make room for §4.2
- **§1 File Structure** — `<script>` template updated: how-to comment block added before the class
- **§8 Pre-Commit Checklist** — new CONFIG section added

---

## Changelog v7 → v8

- **§6.1** — clarified that `new WidgetController(...)` without assignment is the recommended default; assignment to a `const` is an allowed variation when the instance needs to be referenced later
- **§6.2** — expanded: assignment pattern with constructor parameters documented explicitly
- **§8 Pre-Commit Checklist** — INIT item updated to reflect both patterns

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
<button class="btn btn-primary"  data-action="send">Send</button>
<div class="messages-list"       data-ref="messages-list"></div>
<li  class="orders-item"         data-id="order-42" data-state="active"></li>

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
  <div class="widget-modal-overlay" data-ref="modal-confirm"
       role="dialog" aria-modal="true" aria-labelledby="widget-modal-title" hidden>
    <div class="widget-modal">
      <h2 id="widget-modal-title" class="widget-modal__title"></h2>
      <p  class="widget-modal__body"></p>
      <div class="widget-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Confirm</button>
      </div>
    </div>
  </div>
</section>

<script>
  /*
   * ═══════════════════════════════════════════════════════════════════
   *  HOW TO CONFIGURE [WidgetName]
   * ═══════════════════════════════════════════════════════════════════
   *
   *  Configuration has THREE layers. Each layer overrides the previous.
   *  All three are optional — the widget always has safe built-in defaults.
   *
   *  ─────────────────────────────────────────────────────────────────
   *  LAYER 1 — BUILT-IN DEFAULTS  (inside the class, always present)
   *  ─────────────────────────────────────────────────────────────────
   *  static DEFAULTS = { delay: 1000, loop: false, … }
   *
   *  Always present. Used when nothing else is provided.
   *  Edit these only to change the global baseline for every instance.
   *
   *  ─────────────────────────────────────────────────────────────────
   *  LAYER 2 — CONSTRUCTOR OPTIONS  (JS, passed at init time)
   *  ─────────────────────────────────────────────────────────────────
   *  new WidgetController('.widget-container', { delay: 500, loop: true })
   *
   *  Overrides built-in defaults for a specific instance.
   *  Use for: callbacks, non-serializable values, programmatic init.
   *  Note: data attributes (Layer 3) will still override these.
   *
   *  ─────────────────────────────────────────────────────────────────
   *  LAYER 3 — DATA ATTRIBUTES  (HTML, on the container element)
   *  ─────────────────────────────────────────────────────────────────
   *  <section class="widget-container"
   *           data-widget-delay="250"
   *           data-widget-loop="true">
   *
   *  Read once in the constructor via _readDataAttrs().
   *  Overrides BOTH built-in defaults AND constructor options.
   *  Use for: CMS-driven config, per-instance HTML markup config.
   *  See §4.2 for full naming and type-coercion rules.
   *
   *  ─────────────────────────────────────────────────────────────────
   *  RESOLUTION ORDER  (rightmost wins):
   *
   *    static DEFAULTS  →  constructor opts  →  data attributes
   *    (lowest priority)                        (highest priority)
   *
   *  IMPLEMENTATION — constructor runs these three steps in order:
   *    1. this._cfg = { ...WidgetController.DEFAULTS }
   *    2. this._cfg = { ...this._cfg, ...opts }
   *    3. this._cfg = { ...this._cfg, ...this._readDataAttrs() }
   * ═══════════════════════════════════════════════════════════════════
   */

  /* 1. CLASS
   *   ├── static FORBIDDEN_KEYS
   *   ├── static DEFAULTS             ← built-in config defaults (Layer 1)
   *   ├── static config props
   *   ├── static seed data
   *   ├── constructor
   *   │     ├── find root (silent return)
   *   │     ├── $ / $$ helpers
   *   │     ├── _cfg: merge DEFAULTS → opts → _readDataAttrs()
   *   │     ├── cache DOM refs via data-ref
   *   │     ├── validate & init state
   *   │     ├── AbortController          ← this._ac = new AbortController()
   *   │     └── _render() + _bind()
   *   ├── _readDataAttrs()             ← reads data-[widget]-* from root (Layer 3)
   *   ├── _render() methods
   *   ├── _handle() action methods
   *   ├── _bind() — one listener + switch, ALL via signal
   *   ├── _esc() — XSS escaping
   *   ├── destroy()                    ← this._ac.abort()
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
<button class="btn btn-primary"   data-action="send">Send</button>
<div class="orders-list"          data-ref="items-list"></div>
<li  class="orders-item"          data-id="order-42" data-state="new"></li>

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
  <div class="orders-modal-overlay" data-ref="modal-delete"
       role="dialog" aria-modal="true" aria-labelledby="orders-modal-title" hidden>
    <div class="orders-modal">
      <h2 id="orders-modal-title" class="orders-modal__title">Delete order?</h2>
      <p  class="orders-modal__body">This action cannot be undone.</p>
      <div class="orders-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Confirm</button>
      </div>
    </div>
  </div>

</section>

<!-- ❌ wrong — outside container: tokens break, styles leak -->
<div class="orders-modal-overlay">...</div>
```

Why inside: CSS custom properties are inherited down the DOM tree. A modal outside the container cannot see `--orders-*` tokens declared on `.orders-container`. Additionally, the CSS scoping rule (§3.1) requires every selector to begin with the container class — impossible to satisfy from outside.

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
.orders-container .orders-card        { }
.orders-container .orders-card:hover  { }
.orders-container .orders-modal       { }

/* ❌ wrong — styles leak onto the entire page */
.orders-card  { }
.orders-modal { }
```

Modals are not exempt. `position: fixed` does not waive the scoping rule:

```css
/* ✅ correct — scoped even though visually full-screen */
.orders-container .orders-modal-overlay { position: fixed; inset: 0; }

/* ❌ wrong — leaks globally */
.orders-modal-overlay { position: fixed; inset: 0; }
```

### 3.2 Class naming — full words, no abbreviations

All child classes use the container's full word(s) as a prefix — never a 2–3 letter abbreviation:

```css
/* ✅ correct — container: .messages-container, children use full word */
.messages-container .messages-bubble  { }
.messages-container .messages-input   { }

/* BEM modifier: [container-word]-[element]--[modifier] */
.messages-container .messages-bubble--sent { }
.messages-container .messages-bubble--recv { }

/* ✅ correct — container: .orders-container */
.orders-container .orders-modal-overlay { }
.orders-container .orders-modal         { }
.orders-container .orders-modal__title  { }

/* ❌ wrong — abbreviated prefix, unreadable out of context */
.messages-container .msg-bubble  { }
.orders-container   .ord-modal   { }
```

**Rule:** if someone reads `.orders-item` without context they understand it instantly.
If they read `.ord-i` — they have to open the file and guess.

### 3.3 States via `data-state`

JS-driven states go through `data-state`, not modifier classes:

```css
/* ✅ preferred — state is readable directly in the HTML */
.orders-container .orders-item[data-state="cancelled"] .stepper-dot {
  background: var(--bs-danger);
}

/* also acceptable — BEM modifier */
.orders-container .orders-item--cancelled .stepper-dot {
  background: var(--bs-danger);
}
```

In JS, set both — Bootstrap class for visuals and `data-state` for CSS hooks:

```js
el.classList.toggle('active', isActive);
el.dataset.state = isActive ? 'active' : '';
```

### 3.4 CSS custom properties (tokens)

Tokens are declared on the container — section `0` of the stylesheet. Child rules consume tokens, never raw values.
Token names use the same full-word prefix as the container:

```css
/* --- 0. Tokens --- */
.orders-container {
  --orders-accent:      var(--bs-primary);
  --orders-card-radius: .5rem;
  --orders-anim-dur:    150ms;
}

/* Child rules — tokens only */
.orders-container .orders-card {
  border-radius: var(--orders-card-radius);
  border-color:  var(--orders-accent);
}

/* Modal inherits tokens automatically — it is inside the container */
.orders-container .orders-modal {
  border-radius: var(--orders-card-radius);
}
```

Bootstrap classes are never dropped — BEM modifiers only add what Bootstrap does not already cover:

```css
/* ✅ correct — token hook only, no Bootstrap duplication */
.messages-container .messages-bubble--sent {
  background: var(--messages-bubble-sent-bg);
  color:      var(--messages-bubble-sent-color);
}

/* ❌ wrong — abbreviated tokens + !important */
.messages-container .msg-bubble--sent {
  background:    var(--msg-bubble-sent-bg);
  border-radius: var(--msg-bubble-radius) !important;
  padding:       .5rem 1rem !important;
}
```

### 3.5 Modal styles — section 3

```css
/* --- 3. Modals --- */

.orders-container .orders-modal-overlay {
  position:        fixed;
  inset:           0;
  z-index:         1050;               /* above Bootstrap dropdowns (1000) */
  display:         flex;
  align-items:     center;
  justify-content: center;
  background:      rgba(0, 0, 0, .45);
}

.orders-container .orders-modal-overlay[hidden] {
  display: none;
}

.orders-container .orders-modal {
  background:    var(--bs-body-bg);
  border-radius: var(--orders-card-radius, .5rem);
  box-shadow:    0 8px 32px rgba(0, 0, 0, .18);
  padding:       1.5rem;
  width:         min(480px, 90vw);
  max-height:    90vh;
  overflow-y:    auto;
  animation:     orders-modal-in var(--orders-anim-dur, 150ms) ease-out both;
}

.orders-container .orders-modal__title   { font-size: 1.125rem; font-weight: 600; margin-bottom: .5rem; }
.orders-container .orders-modal__body    { color: var(--bs-secondary-color); margin-bottom: 1.5rem; }
.orders-container .orders-modal__actions { display: flex; gap: .5rem; justify-content: flex-end; }
```

### 3.6 Animations

`@keyframes` names must carry the widget's full word prefix — keyframe names are global:

```css
/* --- 5. Animations --- */

/* ✅ correct — full word prefix prevents name collisions */
@keyframes orders-modal-in {
  from { opacity: 0; transform: scale(.95); }
  to   { opacity: 1; transform: scale(1);   }
}

/* ❌ wrong — abbreviated, may collide with another widget on the same page */
@keyframes ord-mi { }

/* ❌ wrong — generic name, guaranteed to collide eventually */
@keyframes modal-in { }
```

Animate only `transform` and `opacity` — these run on the compositor thread with no reflow or repaint.

### 3.7 Inline styles — forbidden

`style=` attributes are forbidden in HTML and in JS template strings. All visual state goes through CSS classes or `data-state`.

```html
<!-- ❌ FORBIDDEN — inline style in HTML -->
<span class="material-symbols-rounded" style="font-size: 18px;">edit</span>

<!-- ✅ correct — CSS class -->
<span class="material-symbols-rounded orders-icon-sm">edit</span>
```

```js
// ❌ FORBIDDEN — inline style in JS template
return `<div style="font-size:.6rem;line-height:1.1">${label}</div>`;

// ✅ correct — CSS class in template
return `<div class="orders-stepper-label-mobile">${this._esc(label)}</div>`;

// ❌ FORBIDDEN — style property assignment in JS
icon.style.fontVariationSettings = `'FILL' ${fill},'wght' 400`;

// ✅ correct — data-state drives CSS font-variation-settings
btn.dataset.state = saved ? 'saved' : '';
// CSS: .widget-container .wishlist-btn[data-state="saved"] .icon { font-variation-settings: 'FILL' 1, ... }
```

**One exception only:** dynamic CSS custom property values set via `el.style.setProperty()` after `innerHTML` injection, when the value cannot be known at build time:

```js
// ✅ only legal use of .style in JS — dynamic token value after render
el.style.setProperty('--orders-fill-percent', pct + '%');
// CSS: .orders-track-fill { width: var(--orders-fill-percent, 0%); }
```

This pattern is only valid when: (1) the value is numeric and dynamic, (2) it feeds a CSS custom property, (3) it is called as a post-render step, not inline in a template.

---

## 4. JavaScript

### 4.1 Class structure

```js
class WidgetController {

  // ─── 0. STATIC CONFIG ──────────────────────────────────────
  static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);

  // Built-in defaults — Layer 1 of the three-layer config system (§4.2).
  // These are the baseline values used when no constructor opts
  // and no data attributes are provided.
  static DEFAULTS = {
    delay:   1000,
    loop:    false,
    showNav: true,
    // ... add all configurable options here
  };

  static MAX_PREVIEW = 38;

  // ─── 1. CONSTRUCTOR ────────────────────────────────────────
  constructor(selector, opts = {}) {

    // 1a. Find container — silent exit if not found
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // 1b. Helpers — scoped to this._root, cannot reach outside
    const $ = sel => this._root.querySelector(sel);
    const $$ = sel => [...this._root.querySelectorAll(sel)];

    // 1c. Three-layer config resolution (see §4.2 for full reference)
    //     Each layer overrides the previous. Data attributes win.
    this._cfg = {
      ...WidgetController.DEFAULTS,   // Layer 1: built-in defaults
      ...opts,                        // Layer 2: constructor options
      ...this._readDataAttrs(),       // Layer 3: data attributes (highest priority)
    };

    // 1d. Cache DOM references via data-ref — once, here, nowhere else
    this._itemsList = $('[data-ref="items-list"]');
    this._textInput = $('[data-ref="text-input"]');
    this._sendBtn   = $('[data-ref="send-btn"]');

    // 1e. Modals — same $ helper, they are inside the container
    this._deleteModal = $('[data-ref="modal-delete"]');

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

    // 1h. AbortController — one abort() removes ALL listeners
    this._ac = new AbortController();

    // 1i. Boot
    this._render();
    this._bind();
  }

  // ─── 2. CONFIG ─────────────────────────────────────────────

  // Reads data-[widget]-* attributes from the container root.
  // Called in the constructor as Layer 3 of config resolution.
  // Returns only the keys that are actually present in the HTML —
  // absent attributes do not override constructor opts or DEFAULTS.
  // See §4.2 for full naming rules and type-coercion patterns.
  _readDataAttrs() {
    const ds  = this._root.dataset;
    const out = {};
    if (ds.widgetDelay   !== undefined) out.delay   = Number(ds.widgetDelay) || WidgetController.DEFAULTS.delay;
    if (ds.widgetLoop    !== undefined) out.loop    = ds.widgetLoop === 'true';
    if (ds.widgetShowNav !== undefined) out.showNav = ds.widgetShowNav !== 'false';
    // ... add one line per configurable attribute
    return out;
  }

  // ─── 3. RENDER ─────────────────────────────────────────────

  _render() {
    // All rendering is derived from this._state
    // Never read state back from the DOM
    this._renderList();
    this._renderModal();
  }

  _renderList() {
    // ✅ user text → textContent only
    // ✅ API / server data in innerHTML → always through _esc()
    this._itemsList.innerHTML = this._state.items.map(item => `
      <li class="orders-item"
          data-id="${this._esc(item.id)}"
          data-state="${this._esc(item.status)}">
        <span class="orders-item__name">${this._esc(item.name)}</span>
        <button class="btn btn-sm btn-danger" data-action="remove" data-id="${this._esc(item.id)}">
          Remove
        </button>
      </li>
    `).join('');
  }

  _renderModal() {
    // Modal visibility derived from state — never from DOM
    const { modal } = this._state;
    this._deleteModal.hidden = modal?.type !== 'delete';
    if (modal?.type === 'delete') {
      // textContent — because targetId is user-supplied data
      this._deleteModal.querySelector('[data-ref="modal-body"]')
        .textContent = `Delete order #${modal.targetId}?`;
    }
  }

  // ─── 4. ACTIONS ────────────────────────────────────────────

  _handleRemove(id) {
    this._lastFocused = document.activeElement;
    this._state.modal = { type: 'delete', targetId: id };
    this._renderModal();
    this._deleteModal.querySelector('button').focus();
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

  // ─── 5. EVENTS ─────────────────────────────────────────────

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

    // passive + signal — both in one options object (see §4.8)
    this._root.addEventListener('scroll', this._onScroll.bind(this),
      { signal: this._ac.signal, passive: true });

    this._textInput?.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this._submit(); }
    }, sig);

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && this._state.modal) this._closeModal();
    }, sig);
  }

  // ─── 6. HELPERS ────────────────────────────────────────────

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

  // ─── 7. LIFECYCLE ──────────────────────────────────────────

  destroy() {
    this._ac.abort(); // removes every listener registered with this signal
  }

  // ─── 8. STATIC ─────────────────────────────────────────────

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

---

### 4.2 Three-Layer Configuration System

This section is the complete reference for how widget configuration works. Read §4.1 first to see the pattern in context.

#### 4.2.1 Overview and resolution order

A widget has three sources of configuration. They are applied in sequence inside the constructor — each one overrides the previous:

```
┌──────────────────────────────────────────────────────────┐
│  static DEFAULTS      ←  built into the class            │
│         ↓  overridden by                                 │
│  constructor opts     ←  passed at new WidgetController()│
│         ↓  overridden by                                 │
│  _readDataAttrs()     ←  read from HTML data-* attributes│
└──────────────────────────────────────────────────────────┘
              rightmost layer always wins
```

The three layers are not conflicting systems — they are complementary. A CMS-placed HTML attribute overrides a developer-set JS option, which overrides the global baseline. All three remain in the codebase simultaneously.

Inside the constructor the merge is one expression:

```js
this._cfg = {
  ...WidgetController.DEFAULTS,   // Layer 1
  ...opts,                        // Layer 2
  ...this._readDataAttrs(),       // Layer 3
};
```

`_readDataAttrs()` only returns keys for attributes that are **actually present** in the HTML. Absent attributes produce no key — they do not silently overwrite Layer 2 values with `undefined`.

#### 4.2.2 Layer 1 — static DEFAULTS

`static DEFAULTS` is a plain object on the class. It defines every configurable option with its baseline value. It is the single source of truth for what options exist and what they default to.

```js
static DEFAULTS = {
  delay:     1000,    // ms — debounce / animation delay
  loop:      false,   // boolean opt-in: false when absent
  showNav:   true,    // boolean opt-out: true when absent
  mode:      'page',  // enum: 'page' | 'single'
  opacity:   1,       // float 0–1
};
```

Rules for `static DEFAULTS`:
- Every key that appears in `_readDataAttrs()` or that can be passed via `opts` **must** be listed here.
- Values must be the correct JS type — booleans as `true`/`false`, numbers as numbers, never strings.
- Names are camelCase — identical to the property names used in `this._cfg` throughout the class.

#### 4.2.3 Layer 2 — constructor opts

`opts` is the second argument to the constructor. It is an optional plain object with the same keys as `static DEFAULTS`. The constructor spreads it over the defaults, so only the keys provided are changed.

```js
// ✅ Pass only the options you want to override — the rest come from DEFAULTS
new OrdersController('.orders-container', { delay: 500 });

// ✅ Multiple overrides
new OrdersController('.orders-container', { delay: 500, loop: true, mode: 'single' });

// ✅ No opts — DEFAULTS apply entirely (data attributes still run in Layer 3)
new OrdersController('.orders-container');
```

Use Layer 2 for options that **cannot go into HTML** — callbacks and non-serializable values:

```js
// ✅ Functions must come via opts — they cannot be expressed as data attributes
new OrdersController('.orders-container', {
  onDelete: (id) => console.log('Deleted', id),
  renderItem: (item) => `<li>${item.name}</li>`,
});
```

Note: if a data attribute is also present for the same key, the data attribute (Layer 3) will win and override this value.

#### 4.2.4 Layer 3 — `_readDataAttrs()`

`_readDataAttrs()` is a private method that reads `this._root.dataset` and returns a plain object. It is called last in the config merge, so its values have the highest priority.

**Critical rule:** only include a key in the return object if the corresponding attribute is **actually present**. Use `!== undefined` to check. An absent attribute must not produce any key — otherwise it would overwrite a Layer 2 value with the default.

```js
_readDataAttrs() {
  const ds  = this._root.dataset;
  const out = {};

  // Each line: check presence → coerce type → assign to output object
  if (ds.widgetDelay   !== undefined) out.delay   = Number(ds.widgetDelay) || WidgetController.DEFAULTS.delay;
  if (ds.widgetLoop    !== undefined) out.loop    = ds.widgetLoop === 'true';
  if (ds.widgetShowNav !== undefined) out.showNav = ds.widgetShowNav !== 'false';
  if (ds.widgetMode    !== undefined) out.mode    = ['page','single'].includes(ds.widgetMode)
                                                      ? ds.widgetMode
                                                      : WidgetController.DEFAULTS.mode;
  if (ds.widgetOpacity !== undefined) out.opacity = Math.min(1, Math.max(0,
                                                      parseFloat(ds.widgetOpacity) || 1));
  return out;
}
```

HTML usage — one attribute per option, on the container:

```html
<!-- Override just the options you need — the rest are inherited from DEFAULTS or opts -->
<section class="orders-container"
         data-orders-delay="250"
         data-orders-loop="true">
</section>

<!-- Override nothing — DEFAULTS (then opts) apply fully -->
<section class="orders-container">
</section>
```

#### 4.2.5 Type coercion rules for data attribute values

All `dataset` values are strings. `_readDataAttrs()` must convert them explicitly. The patterns below cover every common type.

**String** — no conversion needed:

```js
if (ds.widgetMode !== undefined) out.mode = ds.widgetMode ?? WidgetController.DEFAULTS.mode;
```

**Number** — use `Number()` with a fallback:

```js
// ?? falls back only on null/undefined — preserves intentional 0
if (ds.widgetDelay !== undefined) out.delay = Number(ds.widgetDelay) || WidgetController.DEFAULTS.delay;
```

**Boolean** — compare the string explicitly. Never use `Boolean()`:

```js
// ❌ WRONG — any non-empty string is truthy, including "false"
out.loop = Boolean(ds.widgetLoop); // "false" → true — BUG

// ✅ opt-in: absent or "false" → false; only "true" → true
if (ds.widgetLoop !== undefined) out.loop = ds.widgetLoop === 'true';

// ✅ opt-out: absent or "true" → true; only "false" → false
if (ds.widgetShowNav !== undefined) out.showNav = ds.widgetShowNav !== 'false';
```

Choose **opt-in** (`=== 'true'`) when `static DEFAULTS` value is `false`.
Choose **opt-out** (`!== 'false'`) when `static DEFAULTS` value is `true`.

**Enum** — validate against the allowed list, fall back to the default:

```js
if (ds.widgetMode !== undefined) {
  const allowed = ['page', 'single'];
  out.mode = allowed.includes(ds.widgetMode)
    ? ds.widgetMode
    : WidgetController.DEFAULTS.mode;
  if (!allowed.includes(ds.widgetMode)) {
    console.warn(`[WidgetController] Invalid data-widget-mode="${ds.widgetMode}". Using: "${WidgetController.DEFAULTS.mode}".`);
  }
}
```

**Float** — use `parseFloat` with range clamping:

```js
if (ds.widgetOpacity !== undefined) {
  const val = parseFloat(ds.widgetOpacity);
  out.opacity = isNaN(val) ? WidgetController.DEFAULTS.opacity : Math.min(1, Math.max(0, val));
}
```

**Array** — split on a delimiter, map to the correct type:

```js
// data-widget-breakpoints="320,768,1024"
if (ds.widgetBreakpoints !== undefined) {
  out.breakpoints = ds.widgetBreakpoints.split(',').map(Number).filter(Boolean);
}
```

**Summary table:**

| Type | Pattern | Note |
|---|---|---|
| String | `ds.widgetFoo ?? DEFAULTS.foo` | No conversion |
| Number | `Number(ds.widgetFoo) \|\| DEFAULTS.foo` | Guards NaN |
| Boolean opt-in | `ds.widgetFoo === 'true'` | Default is `false` |
| Boolean opt-out | `ds.widgetFoo !== 'false'` | Default is `true` |
| Enum | `allowed.includes(v) ? v : DEFAULTS.foo` | Warn on invalid |
| Float | `Math.min(max, Math.max(min, parseFloat(v)))` | Clamp to range |
| Array | `v.split(',').map(Number).filter(Boolean)` | CSV format |

#### 4.2.6 Naming config data attributes

Config attributes follow the same prefix and casing rules as all other custom data attributes (§7.2) — with one additional constraint: the attribute name must correspond to a key in `static DEFAULTS`.

**Format:** `data-{widget}-{option}` where `{option}` maps to a camelCase key in `DEFAULTS`.

```
HTML attribute (kebab)          →  dataset key (camelCase)  →  this._cfg key
────────────────────────────────────────────────────────────────────────────
data-orders-delay               →  dataset.ordersDelay      →  this._cfg.delay
data-orders-loop                →  dataset.ordersLoop       →  this._cfg.loop
data-orders-show-nav            →  dataset.ordersShowNav    →  this._cfg.showNav
data-orders-arrow-opacity       →  dataset.ordersArrowOpacity → this._cfg.arrowOpacity
```

**Never use uppercase in attribute names.** `data-ordersLoop` is parsed as `dataset.ordersloop` — the camelCase mapping breaks:

```html
<!-- ❌ Wrong — uppercase breaks dataset auto-mapping -->
<section data-ordersLoop="true">

<!-- ✅ Correct — kebab in HTML, camelCase auto-mapped in JS -->
<section data-orders-loop="true">
```

**Callbacks and functions cannot go in data attributes** — they must be passed via Layer 2 (constructor opts):

```js
// ❌ Cannot put a function in HTML
// data-orders-on-delete="???"

// ✅ Callbacks always via constructor opts
new OrdersController('.orders-container', {
  onDelete: (id) => myApi.delete(id),
});
```

---

### 4.3 Silent return — mandatory

```js
// ✅ correct — safe to include on any page
this._root = document.querySelector(selector);
if (!this._root) return;

// ❌ wrong — throws on every page that does not have this widget
if (!this._root) throw new Error('container not found');
```

---

### 4.4 `$` / `$$` helpers

Declared in the constructor, scoped to `this._root`. They physically cannot reach outside:

```js
const $ = sel => this._root.querySelector(sel);
const $$ = sel => [...this._root.querySelectorAll(sel)];

// ✅ All queries go through the helpers, using descriptive ref names
this._itemsList  = $('[data-ref="items-list"]');
this._deleteModal = $('[data-ref="modal-delete"]');

// ❌ Forbidden — reaches outside the container
this._itemsList  = document.querySelector('[data-ref="items-list"]');
this._deleteModal = document.getElementById('modal-delete');
```

---

### 4.5 State as single source of truth

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

---

### 4.6 XSS — the rule security overrides convenience

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

---

### 4.7 Prototype pollution — guard in the constructor

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

---

### 4.8 AbortController — mandatory, no exceptions

Every widget that registers `addEventListener` **must** use `AbortController`. This is not optional.

**Why:** widgets are mounted inside tab layouts. Without cleanup, each mount cycle stacks a new set of listeners on top of the previous ones. After N tab switches there are N copies of every handler running simultaneously — memory leak and logic bugs.

#### 4.8.1 Placement in the constructor

`this._ac` is declared **after** state, **before** `_bind()`:

```js
constructor(selector, opts = {}) {
  this._root = document.querySelector(selector);
  if (!this._root) return;

  // DOM refs, config setup, state setup ...

  this._state = { ... };           // state first
  this._ac = new AbortController(); // AC after state, before _bind
  this._render();
  this._bind();
}
```

Never declare `this._ac` after `_bind()` — listeners registered before `_ac` exists cannot be tracked.

#### 4.8.2 `sig` — declare once, use everywhere

Declare `const sig` as the **first line** of `_bind()`. Pass it to every listener:

```js
_bind() {
  const sig = { signal: this._ac.signal }; // ← first line, always

  this._root.addEventListener('click',   e => { ... }, sig);
  this._root.addEventListener('keydown', e => { ... }, sig);
  document.addEventListener('keydown',   e => { ... }, sig);
  modal.addEventListener('hidden.bs.modal', () => { ... }, sig);
}
```

#### 4.8.3 Combining with `passive`

`passive` and `signal` go in the **same options object**. Never pass them separately:

```js
// ✅ correct — one options object
this._root.addEventListener('scroll', handler, {
  signal:  this._ac.signal,
  passive: true,
});

// ❌ wrong — sig does not contain passive, passive does not contain signal
this._root.addEventListener('scroll', handler, sig);                // missing passive
this._root.addEventListener('scroll', handler, { passive: true });  // missing signal
```

#### 4.8.4 Legal exception — `{ once: true }`

Listeners with `{ once: true }` are self-removing after the first fire. Signal is not required, but allowed:

```js
// ✅ legal — once:true is self-removing, no memory leak
picker.addEventListener('animationend', () => {
  picker.classList.remove('is-invalid');
}, { once: true });

// ✅ also legal — belt and suspenders
picker.addEventListener('animationend', () => {
  picker.classList.remove('is-invalid');
}, { once: true, signal: this._ac.signal });

// Rule: { once: true } without signal is OK. Everything else requires signal.
```

#### 4.8.5 `document.addEventListener` — signal is critical

Global listeners are the most dangerous. They have no natural cleanup boundary:

```js
// ❌ FORBIDDEN — global listener with no cleanup
document.addEventListener('click', e => { ... });
document.addEventListener('keydown', e => { ... });

// ✅ correct — signal removes them on destroy()
const sig = { signal: this._ac.signal };
document.addEventListener('click', e => { ... }, sig);
document.addEventListener('keydown', e => { ... }, sig);
```

#### 4.8.6 Anti-patterns

```js
// ❌ AC declared but destroy() never called — abort() never fires, AC is useless
constructor() {
  this._ac = new AbortController();
  this._bind();
}
// destroy() is missing

// ❌ destroy() exists but no signal on listeners — abort() has nothing to cancel
_bind() {
  this._root.addEventListener('click', handler); // no sig
}
destroy() { this._ac.abort(); } // aborts nothing

// ❌ new AbortController() per method — cannot abort from destroy()
_initSection() {
  const ac = new AbortController(); // local AC, not stored
  el.addEventListener('click', handler, { signal: ac.signal });
  // ac is lost after method returns — impossible to call ac.abort() later
}

// ❌ sig declared but not passed to multiline listener
_bind() {
  const sig = { signal: this._ac.signal };
  this._root.addEventListener('click', e => {
    // ... many lines ...
  }); // ← closing paren without sig!
}
```

---

### 4.9 Listeners outside `_bind()`

When a widget has helper methods that register their own listeners (e.g., `_initPasswordVisibility()`, `#setupEventListeners()`), they must use the same `this._ac`:

```js
// ✅ correct — uses the shared this._ac
_initPasswordVisibility() {
  const sig = { signal: this._ac.signal };
  this._root.querySelectorAll('[data-action="toggle-password"]').forEach(btn => {
    btn.addEventListener('click', () => { ... }, sig);
  });
}

// ❌ wrong — local AbortController, cannot be aborted from destroy()
_initPasswordVisibility() {
  const localAc = new AbortController();
  btn.addEventListener('click', handler, { signal: localAc.signal });
}
```

Rule: **one `this._ac` per widget instance.** All listeners share the same signal. `destroy()` aborts all of them at once.

---

### 4.10 Lifecycle — `destroy()` contract

`destroy()` is the last method in the class body. It is the public API for cleanup:

```js
// ✅ correct placement — last method before closing brace
class OrdersController {
  constructor() { ... }
  _render()  { ... }
  _bind()    { ... }
  _esc()     { ... }

  destroy() {
    this._ac.abort();
  }
}
```

`destroy()` must contain only `this._ac.abort()`. Do not add manual `removeEventListener` calls — if every listener uses the signal, `abort()` handles all of them. Manual `removeEventListener` alongside `abort()` is redundant and a sign that some listeners are missing `signal`.

```js
// ❌ wrong — manual removeEventListener means some listeners don't have signal
destroy() {
  this._ac.abort();
  this._sendBtn.removeEventListener('click', this._handleSend); // why is this here?
}

// ✅ correct — abort() is sufficient because ALL listeners use signal
destroy() {
  this._ac.abort();
}
```

---

### 4.11 Event delegation — prefer over per-element listeners

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

Delegation also solves the per-element listener problem in `forEach`:

```js
// ❌ wrong — N listeners on N cards, all need manual cleanup
items.forEach(item => {
  const card = this._buildCard(item);
  card.addEventListener('click', () => this._handleCardClick(item.id));
  this._list.appendChild(card);
});

// ✅ correct — one delegated listener covers all current and future cards
this._root.addEventListener('click', e => {
  const card = e.target.closest('[data-id]');
  if (!card) return;
  this._handleCardClick(card.dataset.id);
}, { signal: this._ac.signal });
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

`passive` and `signal` must always be combined in one options object:

```js
// ❌ BAD — browser waits for handler → [Violation]; signal missing
this._root.addEventListener('scroll', handler);
window.addEventListener('touchstart', handler);

// ✅ GOOD — passive + signal together, never separate
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
// ❌ BAD — potentially 3 separate reflows; also violates §3.7 (inline style)
el.style.width  = '100px';
el.style.height = '100px';
el.style.color  = 'red';

// ✅ GOOD — one reflow, no style= violation
el.classList.add('is-active');
// CSS: .widget-container .el.is-active { width: 100px; height: 100px; color: red; }
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

### 6.1 Standard pattern — recommended default

The recommended form is a bare `new` with no assignment. All logic lives in the constructor; INIT contains nothing except `new`:

```js
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container');
});
```

`DOMContentLoaded` fires when the DOM is fully parsed regardless of `<script>` placement.

### 6.2 Allowed variation — assignment to `const`

Assigning the instance to a `const` is permitted when the instance needs to be referenced after initialization — for example, to call `destroy()` from outside, or to pass the controller to another module. In all other cases prefer the bare `new` form.

```js
// ✅ allowed — instance is needed later (e.g. destroy() called on navigation)
document.addEventListener('DOMContentLoaded', () => {
  const ordersController = new OrdersController('.orders-container');
});

// ✅ allowed — with constructor parameters (Layer 2 opts)
document.addEventListener('DOMContentLoaded', () => {
  const ordersController = new OrdersController('.orders-container', { data: apiData, delay: 500 });
});

// ✅ bare new — preferred when the reference is not needed
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container', { data: apiData, delay: 500 });
});
```

**Rule:** the variable name must match the controller name in camelCase — `ordersController` for `OrdersController`, `messagesController` for `MessagesController`. No logic other than `new` belongs in the INIT block regardless of which form is used.

### 6.3 Multiple instances

```js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.orders-container').forEach(el => {
    new OrdersController(el);
  });
});
```

All DOM lookups are scoped to `this._root` — multiple instances on one page never conflict, even with identical `data-ref` values inside each one. Each instance reads its own data attributes independently in `_readDataAttrs()`, so each can have different configuration through HTML alone.

---

## 7. Naming Conventions

### 7.1 Classes and files

**Core rule: names must be readable words, not letter soup.**
Use 1–2 real words. Never abbreviate to 2–3 random letters.

| What | Convention | ✅ Correct | ❌ Wrong |
|---|---|---|---|
| ES6 class | PascalCase + `Controller` | `OrdersController` | `OrdCtrl` |
| CSS container | full word(s) + `-container` | `.orders-container` | `.ord-c` |
| CSS child class | full word(s), kebab-case | `.orders-item`, `.orders-card` | `.ord-i`, `.o-c` |
| BEM modifier | `[word]-[element]--[modifier]` | `.orders-item--cancelled` | `.ord-i--cncl` |
| Modal overlay | `[word]-modal-overlay` | `.orders-modal-overlay` | `.ord-mo` |
| CSS token prefix | full container word | `--orders-accent` | `--ord-a` |
| `@keyframes` name | full word(s) + description | `orders-modal-in` | `ord-mi` |
| HTML file | `feature.html` | `orders.html` | `ord-4f.html` |

**Length guideline:** 1–2 words is ideal. 3 words is the hard ceiling.
`newsletter-item` ✅ — `nl-i` ❌ — `newsletter-subscription-list-item` ❌

**Examples by widget:**

```
Widget: newsletters
  Container:  .newsletters-container
  Children:   .newsletters-item, .newsletters-channel, .newsletters-footer
  Modal:      .newsletters-modal-overlay, .newsletters-modal
  Tokens:     --newsletters-accent, --newsletters-radius
  Keyframes:  newsletters-modal-in
  Class:      NewslettersController
  File:       newsletters.html

Widget: orders
  Container:  .orders-container
  Children:   .orders-item, .orders-card, .orders-header
  Modal:      .orders-modal-overlay, .orders-modal
  Tokens:     --orders-accent, --orders-card-radius
  Keyframes:  orders-modal-in
  Class:      OrdersController
  File:       orders.html

Widget: mysizes
  Container:  .mysizes-container
  Children:   .mysizes-field, .mysizes-card, .mysizes-footer
  Modal:      .mysizes-modal-overlay, .mysizes-modal
  Tokens:     --mysizes-accent, --mysizes-radius
  Keyframes:  mysizes-modal-in
  Class:      MySizesController
  File:       mysizes.html
```

### 7.2 data attributes — attribute names

Standard attributes are fixed. Custom attributes follow the same prefix rule as classes: full widget word, never an abbreviation.

| What | Convention | ✅ Correct | ❌ Wrong |
|---|---|---|---|
| DOM reference | `data-ref` (fixed name) | `data-ref="items-list"` | `data-ref="il"` |
| Action trigger | `data-action` (fixed name) | `data-action="remove-item"` | `data-action="ri"` |
| Record identifier | `data-id` (fixed name) | `data-id="order-42"` | — |
| JS-driven state | `data-state` (fixed name) | `data-state="active"` | — |
| Config attribute | `data-[widget]-[option]` | `data-orders-delay="500"` | `data-ord-d="500"` |
| Custom attribute | `data-[widget]-[description]` | `data-orders-priority="high"` | `data-ord-p="h"` |
| Custom attribute | kebab-case, full words | `data-messages-direction="sent"` | `data-msg-dir="s"` |

**Custom attributes must carry the widget's full word prefix** — just like CSS classes and tokens.
They are global in the DOM; without a prefix they collide between widgets on the same page.

```html
<!-- ✅ correct — widget prefix prevents collisions -->
<li class="orders-item"
    data-id="${orderId}"
    data-state="active"
    data-orders-priority="high">...</li>

<!-- ❌ wrong — custom attribute has no prefix, collides globally -->
<li class="orders-item" data-priority="high">...</li>
```

### 7.2.1 data attribute — value naming

Values follow the same full-word, kebab-case rule. They are also read by CSS selectors — abbreviated values make CSS unreadable.

| Attribute | Value convention | ✅ Correct | ❌ Wrong |
|---|---|---|---|
| `data-ref` | noun or noun-noun, kebab-case | `"items-list"`, `"send-btn"`, `"modal-delete"` | `"il"`, `"sb"`, `"md"` |
| `data-action` | verb-noun, kebab-case | `"remove-item"`, `"open-modal"`, `"modal-cancel"` | `"ri"`, `"om"`, `"mc"` |
| `data-action` (modal) | `modal-` prefix + verb | `"modal-open-delete"`, `"modal-cancel"`, `"modal-confirm"` | `"mod"`, `"mc"` |
| `data-state` | adjective or noun, single word | `"active"`, `"cancelled"`, `"loading"`, `"empty"` | `"act"`, `"cncl"` |
| `data-id` | follows the record's own ID format | `"order-42"`, `"user-7"` | — |
| config `data-[widget]-*` | full readable word(s), kebab | `"page"`, `"true"`, `"false"`, `"250"` | `"pg"`, `"t"`, `"f"` |
| custom `data-*` | adjective or noun, kebab-case | `"high"`, `"sent"`, `"in-progress"` | `"h"`, `"s"`, `"ip"` |

**Rule:** if a CSS selector uses the value, the value must read like English:

```css
/* ✅ readable — value is a real word */
.orders-container .orders-item[data-state="cancelled"] { }
.orders-container .orders-item[data-orders-priority="high"] { }

/* ❌ unreadable — value is an abbreviation */
.orders-container .orders-item[data-state="cncl"] { }
.orders-container .orders-item[data-ord-p="h"] { }
```

**`data-action` value pattern:**

```
remove-item      → verb-noun
toggle-filter    → verb-noun
modal-open-delete  → modal- prefix + verb + noun (opens a specific modal)
modal-cancel       → modal- prefix + verb (standard cancel, no suffix needed)
modal-confirm      → modal- prefix + verb (standard confirm, no suffix needed)
```

### 7.3 id — naming

`id` is allowed **only** for ARIA references and anchor links (see Law Zero). Even in these two cases the name must follow a strict convention — `id` values are global; a collision silently breaks ARIA or navigation.

**Core rule: names must be readable words, not letter soup. Same as classes.**

| What | Convention | ✅ Correct | ❌ Wrong |
|---|---|---|---|
| Modal title (ARIA) | `[widget]-modal-[description]` | `orders-modal-title` | `omt`, `modal-title`, `mdt` |
| Section anchor | `[widget]-section-[description]` | `orders-section-payments` | `sec-pay`, `s-p` |
| List item (ARIA) | `[widget]-item-[record-id]` | `orders-item-42` | `oi42`, `itm-42` |
| Dialog heading | `[widget]-[dialog-name]-title` | `newsletters-confirm-title` | `nct`, `confirm-title` |

**Every `id` carries the widget's full word prefix** — the same prefix used for classes, tokens, and custom data attributes. Generic names like `modal-title` or `section-header` will collide between widgets.

```html
<!-- ✅ correct — widget prefix, full readable words -->
<div role="dialog" aria-modal="true"
     aria-labelledby="orders-modal-title" hidden>
  <h2 id="orders-modal-title">Delete order?</h2>
</div>

<h2 id="orders-section-payments">Payments</h2>
<a href="#orders-section-payments">Go to payments</a>

<!-- ❌ wrong — no widget prefix, collides globally -->
<div role="dialog" aria-labelledby="modal-title">
  <h2 id="modal-title">Delete order?</h2>
</div>

<!-- ❌ wrong — abbreviated -->
<h2 id="ord-s-pay">Payments</h2>

<!-- ❌ wrong — id used as a JS hook (Law Zero violation) -->
<button id="send-btn" class="btn btn-primary">Send</button>
```

**Length guideline:** same as classes — 1–3 words after the widget prefix.
`orders-modal-title` ✅ — `omt` ❌ — `orders-delete-confirmation-dialog-heading-label` ❌

**Examples by widget:**

```
Widget: orders
  ARIA modal title:  id="orders-modal-title"
  ARIA modal body:   id="orders-modal-body"
  Section anchor:    id="orders-section-payments"
  List item (ARIA):  id="orders-item-42"

Widget: newsletters
  ARIA modal title:  id="newsletters-modal-title"
  Section anchor:    id="newsletters-section-channels"

Widget: mysizes
  ARIA modal title:  id="mysizes-modal-title"
  Section anchor:    id="mysizes-section-measurements"
```

### 7.4 JS variables and properties

Same rule: real words, not initials. Short is fine — cryptic is not.

| What | Convention | ✅ Correct | ❌ Wrong |
|---|---|---|---|
| Cached DOM ref | camelCase, describes the element | `this._itemsList` | `this._il` |
| Cached DOM ref | camelCase, describes the element | `this._sendBtn` | `this._sb` |
| State object key | camelCase noun | `this._state.activeId` | `this._state.aid` |
| Config object key | camelCase noun, matches DEFAULTS | `this._cfg.showNav` | `this._cfg.sn` |
| Private method | `_` + verb + noun | `_handleRemove()` | `_hr()` |
| Helper variable | noun or verb+noun | `const items`, `const filtered` | `const d`, `const tmp` |

### 7.5 Static properties

| What | Convention | Example |
|---|---|---|
| Config defaults | SCREAMING_SNAKE, object | `static DEFAULTS = { delay: 1000, loop: false }` |
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
- [ ] Container class name is a full readable word, not a 2–3 letter abbreviation
- [ ] Child class names are full words — not `ord-item` but `orders-item`
- [ ] Modals placed inside the container, before the closing tag
- [ ] Every modal has `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, `hidden`
- [ ] ARIA: `role`, `aria-label`, `aria-live` where applicable
- [ ] Keyboard navigation implemented for interactive lists
- [ ] No `style=` attributes anywhere in HTML

### data attributes — naming
- [ ] `data-ref` values are full readable words in kebab-case — not `"il"` but `"items-list"`
- [ ] `data-action` values follow `verb-noun` pattern — not `"ri"` but `"remove-item"`
- [ ] `data-action` modal values use `modal-` prefix — `"modal-open-delete"`, `"modal-cancel"`, `"modal-confirm"`
- [ ] `data-state` values are full adjectives or nouns — not `"cncl"` but `"cancelled"`
- [ ] Custom `data-*` attributes carry the widget's full word prefix — not `data-priority` but `data-orders-priority`
- [ ] Custom `data-*` values are full readable words in kebab-case
- [ ] Config `data-[widget]-*` attributes match keys defined in `static DEFAULTS`

### id — naming
- [ ] `id` is used only for ARIA references and anchor links — never as a JS hook
- [ ] Every `id` carries the widget's full word prefix — not `"modal-title"` but `"orders-modal-title"`
- [ ] `id` values are full readable words in kebab-case — not `"omt"` but `"orders-modal-title"`
- [ ] Pattern: ARIA modal title → `[widget]-modal-title`, anchor → `[widget]-section-[description]`
- [ ] No generic unprefixed ids (`modal-title`, `section-header`, `dialog-label`) anywhere in the widget

### CSS
- [ ] Every selector starts with the container class
- [ ] Section 0 — tokens declared on the container
- [ ] Token names use full container word — not `--ord-accent` but `--orders-accent`
- [ ] Modal styles in section 3
- [ ] `@keyframes` names carry the widget's full word prefix
- [ ] All `@keyframes` collected in section 5
- [ ] No `!important` inside modifier rules
- [ ] Animations use only `transform` and `opacity`
- [ ] No `style=` attributes in HTML templates or JS template strings

### JS — configuration (§4.2)
- [ ] `static DEFAULTS` is present and lists every configurable option with its baseline value
- [ ] `_readDataAttrs()` method exists and is called third in the constructor config merge
- [ ] Config merge follows the order: `{ ...DEFAULTS, ...opts, ..._readDataAttrs() }`
- [ ] `_readDataAttrs()` uses `!== undefined` guard — absent attributes produce no key
- [ ] Boolean opt-in uses `=== 'true'`, boolean opt-out uses `!== 'false'` — never `Boolean()`
- [ ] Enum values are validated against an allowed list with a fallback to `DEFAULTS`
- [ ] Number values are protected against `NaN` with a fallback to `DEFAULTS`
- [ ] Config data attribute names follow `data-[widget]-[option]` format
- [ ] How-to comment block is present above the class in the `<script>` tag
- [ ] Callbacks and non-serializable options are passed via constructor `opts`, not data attributes

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
- [ ] `AbortController` declared in constructor after state, before `_bind()`
- [ ] `const sig = { signal: this._ac.signal }` is the first line of `_bind()`
- [ ] Every `addEventListener` (except `DOMContentLoaded`) passes `signal`
- [ ] `passive: true` listeners combine `signal` and `passive` in one options object
- [ ] `{ once: true }` listeners are exempt from signal requirement
- [ ] No `addEventListener` in helper methods uses a local `AbortController`
- [ ] `destroy()` contains only `this._ac.abort()` — no manual `removeEventListener`
- [ ] `destroy()` is the last method in the class body
- [ ] `_closeModal()` restores focus to `this._lastFocused`

### JS — security
- [ ] User text via `textContent` only, never `innerHTML`
- [ ] All data in `innerHTML` goes through `_esc()` without exception
- [ ] No `style=` attributes injected via JS template strings
- [ ] `el.style.*` assignments forbidden — use `classList` or `el.style.setProperty()` for CSS tokens only
- [ ] External data validated via `static _validate()` inside the constructor
- [ ] `FORBIDDEN_KEYS` includes `__proto__`, `constructor`, `prototype`

### JS — performance
- [ ] No geometry reads after style writes in the same loop (Layout Thrashing)
- [ ] `scroll`, `touchstart`, `touchmove` use `{ signal: this._ac.signal, passive: true }`
- [ ] `scroll`, `mousemove`, `resize` use throttle / debounce
- [ ] Styles changed via `classList` or CSS custom properties via `setProperty`, not via `.style.*`
- [ ] No `[Violation]` warnings in the browser console

### INIT
- [ ] `DOMContentLoaded` wraps initialization
- [ ] Initialization is `new WidgetController('.widget-container')` (bare form, recommended) or `const widgetController = new WidgetController(...)` (when the instance is referenced later)
- [ ] No logic in INIT — everything lives in the constructor
