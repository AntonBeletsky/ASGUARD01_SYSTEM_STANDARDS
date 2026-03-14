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

---

## 1. File Structure

Each widget is a self-contained HTML file (or separate HTML + CSS + JS when extracted for production). Section order is fixed:

```
<style>
  /* 0. Tokens (CSS custom properties)  */
  /* 1. Container layout                */
  /* 2. Child elements (sections)       */
  /* 3. States                          */
  /* 4. Animations (@keyframes)         */
  /* 5. Responsive (@media)             */
</style>

<section class="widget-container">
  <!-- widget markup -->
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

### 2.3 ARIA

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

All child classes get a unique short prefix that abbreviates the container name:

```css
/* container: .messages-container */
/* prefix:     msg-               */

.messages-container .msg-bubble  { }
.messages-container .msg-input   { }
.messages-container .msg-sidebar { }
```

Format: `[prefix]-[element]` or `[prefix]-[element]--[modifier]` (BEM-like).

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

All `@keyframes` blocks are collected in a dedicated section (`4. Animations`) — never inlined inside child-element sections.

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

    // 1d. Options with static defaults
    this._delay = opts.delay ?? WidgetController.DELAY_MS;

    // 1e. Data — opts override → static seed → validate
    const raw  = opts.data ?? WidgetController.SEED_DATA;
    const data = raw.filter(d => WidgetController._validate(d));

    // 1f. State — single source of truth
    this._state = {
      items:    data,
      activeId: null,
      loading:  false,
    };

    // 1g. AbortController for event listeners
    this._ac = new AbortController();

    // 1h. Boot
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
    this._render(); // always re-derive UI from state
  }

  /** @private */
  _submit() { }

  // ─── 4. EVENTS ─────────────────────────────────────────────
  /** @private */
  _bind() {
    const sig = { signal: this._ac.signal };

    // One delegated listener on root covers ALL [data-action] children,
    // including elements added dynamically after init.
    this._root.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      switch (btn.dataset.action) {
        case 'send':   this._submit(); break;
        case 'remove': this._remove(btn.dataset.id); break;
        case 'back':   this._handleBack(); break;
      }
    }, sig);

    this._input.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this._submit(); }
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
    return !Object.keys(obj).some(k => forbidden.includes(k));
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

### 4.8 AbortController for events

Every `addEventListener` call receives `{ signal: this._ac.signal }`. `destroy()` removes them all:

```js
_bind() {
  const sig = { signal: this._ac.signal };

  this._root.addEventListener('click',   this._onClick,  sig);
  this._root.addEventListener('keydown', this._onKey,    sig);
  window.addEventListener('resize',      this._onResize, sig);
  // ^ window listeners are also removed on abort()
}

destroy() {
  this._ac.abort(); // removes every listener registered with this signal
}
```

### 4.9 Event delegation

One listener on the root covers all `[data-action]` targets, including elements added dynamically:

```js
// ✅ correct — one listener, works for future elements too
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  switch (btn.dataset.action) {
    case 'send':   this._submit(); break;
    case 'remove': this._remove(btn.dataset.id); break;
    case 'back':   this._handleBack(); break;
  }
}, { signal: this._ac.signal });

// ⚠️  wrong — one listener per element, breaks on dynamic content,
//              signal not passed = listener leaks on destroy()
this._sendBtn.addEventListener('click', () => this._submit());
this._backBtn.addEventListener('click', () => this._handleBack());
```

Inline `click` handlers on individual buttons are only acceptable for `keydown` / `input` events where delegation is not practical.

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

### 4.10 XSS protection

User-supplied text — `textContent` only. Server/API metadata in `innerHTML` — always through `_esc()`:

```js
// ✅ correct
bubble.textContent = userMessage;                           // no XSS possible
li.innerHTML = `<span>${this._esc(apiData.name)}</span>`;  // metadata escaped

// ⚠️  dangerous
bubble.innerHTML = userMessage;
li.innerHTML = `<span>${apiData.name}</span>`;
```

### 4.11 Prototype pollution guard

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

Because all DOM lookups are scoped to `this._root`, multiple instances of the same widget never interfere — even with identical `data-ref` values inside each one.

---

## 6. Naming Conventions

### 6.1 Classes and files

| What | Convention | Example |
|---|---|---|
| ES6 class | PascalCase + `Controller` suffix | `MessagesController` |
| CSS container | kebab-case + `-container` suffix | `.messages-container` |
| CSS child prefix | short kebab | `msg-` |
| BEM modifier | `[prefix]-[element]--[modifier]` | `.msg-msg--sent` |
| HTML file | `feature-hash.html` | `correspondence-4e.html` |
| Instance variable | camelCase | `const messagesController` |

### 6.2 `data-*` attributes

| Purpose | Attribute | Example |
|---|---|---|
| DOM reference (cached in constructor) | `data-ref` | `data-ref="send-btn"` |
| Action trigger (delegated handler) | `data-action` | `data-action="send"` |
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

CSS
  [ ] Section 0 — tokens declared on the container
  [ ] Every child selector starts with .widget-container
  [ ] BEM modifiers used alongside Bootstrap classes, not instead of them
  [ ] BEM modifier CSS does not duplicate what Bootstrap already provides
  [ ] No !important inside modifier rules
  [ ] @keyframes names carry the widget prefix
  [ ] All @keyframes collected in a dedicated Animations section
  [ ] @media breakpoints match the design system

JS
  [ ] No loose constants above the class — everything is static
  [ ] Seed data assigned as WidgetController.SEED_DATA after class body
  [ ] Constructor signature is (selector, opts = {})
  [ ] Silent return if container is not found
  [ ] $ / $$ helpers declared in constructor, scoped to this._root
  [ ] DOM references cached via data-ref in constructor, nowhere else
  [ ] opts resolved with static defaults (opts.delay ?? ClassName.DELAY_MS)
  [ ] Data validated inside constructor, not in INIT
  [ ] All internal properties use _ prefix
  [ ] State is the single source of truth — never read state from DOM
  [ ] AbortController: this._ac in constructor, signal passed to every addEventListener
  [ ] destroy() calls this._ac.abort()
  [ ] All delegated actions go through one root click listener + switch
  [ ] Complex action handlers extracted to named _handleXxx() methods
  [ ] User text via textContent, never innerHTML
  [ ] Metadata escaped via _esc() before innerHTML
  [ ] External data validated via static _validate()

INIT
  [ ] DOMContentLoaded wraps init
  [ ] Init is a single line: new WidgetController('.widget-container')
  [ ] No data filtering, no option assembly in INIT — all inside constructor
```
