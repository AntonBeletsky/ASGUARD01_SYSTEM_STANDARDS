# Containerization Guide — v8 · Many Containers
## Extension: Multiple Independent Widgets on One Page

> This document extends `containerization-8.md`.
> All base rules apply in full. This file defines what changes and what is added
> when a page hosts **two or more independent containers simultaneously**.

---

## What "many containers" means

**Single-container page** — one widget, one controller, one `<style>`, one `<script>`:

```
page.html
  └── <style>          ← orders widget CSS
  └── <section>        ← .orders-container
  └── <script>         ← OrdersController class + INIT
```

**Many-containers page** — N independent widgets, each fully isolated:

```
page.html
  ├── <style>          ← orders widget CSS        (widget A)
  ├── <style>          ← newsletters widget CSS   (widget B)
  ├── <style>          ← mysizes widget CSS       (widget C)
  │
  ├── <section>        ← .orders-container        (widget A)
  ├── <section>        ← .newsletters-container   (widget B)
  ├── <section>        ← .mysizes-container       (widget C)
  │
  ├── <script>         ← OrdersController class   (widget A)
  ├── <script>         ← NewslettersController    (widget B)
  ├── <script>         ← MySizesController        (widget C)
  │
  └── <script>         ← INIT (single block, all widgets)
```

Each widget is an island. It does not know about the others. It cannot
reach into them. Adding or removing one widget does not touch any other.

---

## Priority Order (inherited, applies per widget)

```
1. DATA ATTRIBUTES  — absolute foundation
2. CODE CLEANLINESS — structure, isolation, readability
3. SECURITY         — XSS, pollution, escaping
4. PERFORMANCE      — final audit
```

On a many-containers page the same chain applies independently inside
every widget. There is no cross-widget hierarchy.

---

## 1. File Structure

### 1.1 Section order on the page

The page is divided into three major blocks, in this exact order:

```
────────────────────────────────────────
  BLOCK 1 — STYLES (one <style> per widget)
────────────────────────────────────────
  BLOCK 2 — HTML (one container element per widget)
────────────────────────────────────────
  BLOCK 3 — SCRIPTS (one <script> per widget, then one shared INIT)
────────────────────────────────────────
```

```html
<!-- ═══════════════════ BLOCK 1 — STYLES ═══════════════════ -->

<style>
  /* ── Widget A: orders ─────────────────────────────────── */
  /* 0. Tokens   1. Container   2. Children   3. Modals
     4. States   5. Animations  6. Responsive              */
</style>

<style>
  /* ── Widget B: newsletters ────────────────────────────── */
  /* same section order */
</style>

<style>
  /* ── Widget C: mysizes ────────────────────────────────── */
  /* same section order */
</style>


<!-- ══════════════════ BLOCK 2 — HTML ══════════════════════ -->

<section class="orders-container" aria-label="...">
  <!-- orders markup + modals -->
</section>

<section class="newsletters-container" aria-label="...">
  <!-- newsletters markup + modals -->
</section>

<section class="mysizes-container" aria-label="...">
  <!-- mysizes markup + modals -->
</section>


<!-- ════════════════ BLOCK 3 — SCRIPTS ═════════════════════ -->

<script>
  /* OrdersController class */
</script>

<script>
  /* NewslettersController class */
</script>

<script>
  /* MySizesController class */
</script>

<script>
  /* INIT — one DOMContentLoaded, all widgets */
  document.addEventListener('DOMContentLoaded', () => {
    new OrdersController('.orders-container');
    new NewslettersController('.newsletters-container');
    new MySizesController('.mysizes-container');
  });
</script>
```

### 1.2 One `<style>` per widget — mandatory

Mixing styles from two widgets into one `<style>` block is a violation:

```html
<!-- ❌ FORBIDDEN — two widgets in one style block -->
<style>
  .orders-container { ... }
  .newsletters-container { ... }
</style>

<!-- ✅ correct — each widget owns its style block -->
<style>
  /* orders */
  .orders-container { ... }
</style>

<style>
  /* newsletters */
  .newsletters-container { ... }
</style>
```

**Why:** widget files are often extracted into separate files and included
via server-side templates. When CSS lives in separate `<style>` blocks the
extraction is a cut-paste operation. When styles are merged, extraction
requires grep and manual editing.

### 1.3 One `<script>` per widget class — mandatory

Same rule for JS. The shared INIT block is the only permitted exception:

```html
<!-- ❌ FORBIDDEN — two classes in one script block -->
<script>
  class OrdersController { ... }
  class NewslettersController { ... }
</script>

<!-- ✅ correct — each class in its own block -->
<script>
  class OrdersController { ... }
</script>

<script>
  class NewslettersController { ... }
</script>

<script>
  /* INIT — the only block that may reference multiple controllers */
  document.addEventListener('DOMContentLoaded', () => {
    new OrdersController('.orders-container');
    new NewslettersController('.newsletters-container');
  });
</script>
```

---

## 2. HTML

### 2.1 Container isolation

Each container is a standalone semantic element. Containers are siblings —
never nested inside each other:

```html
<!-- ✅ correct — siblings, flat hierarchy -->
<section class="orders-container"       aria-label="Order list">...</section>
<section class="newsletters-container"  aria-label="Newsletters">...</section>
<section class="mysizes-container"      aria-label="My sizes">...</section>

<!-- ❌ FORBIDDEN — nested containers -->
<section class="orders-container">
  <section class="newsletters-container">...</section>
</section>
```

### 2.2 Container class uniqueness

Each container class is unique across the entire page. Two different widget
types must never share a container class:

```html
<!-- ❌ FORBIDDEN — two different widgets, same container class -->
<section class="widget-container" data-widget="orders">...</section>
<section class="widget-container" data-widget="newsletters">...</section>

<!-- ✅ correct — each widget has its own unique container class -->
<section class="orders-container">...</section>
<section class="newsletters-container">...</section>
```

**Why:** CSS selectors, JS bootstrap queries, and CSS token scopes all
depend on the container class being unique per widget type.

### 2.3 Modals inside their own container

Modals always live inside the container that owns them.
A modal from widget A must not be placed inside widget B's container or
at the top level of the page:

```html
<!-- ✅ correct — each modal inside its own container -->
<section class="orders-container">
  <ul class="orders-list" data-ref="orders-list">...</ul>

  <div class="orders-modal-overlay" data-ref="modal-delete"
       role="dialog" aria-modal="true"
       aria-labelledby="orders-modal-title" hidden>
    <div class="orders-modal">
      <h2 id="orders-modal-title" class="orders-modal__title">Delete order?</h2>
      ...
    </div>
  </div>
</section>

<section class="newsletters-container">
  <ul class="newsletters-list" data-ref="newsletters-list">...</ul>

  <div class="newsletters-modal-overlay" data-ref="modal-unsubscribe"
       role="dialog" aria-modal="true"
       aria-labelledby="newsletters-modal-title" hidden>
    <div class="newsletters-modal">
      <h2 id="newsletters-modal-title" class="newsletters-modal__title">Unsubscribe?</h2>
      ...
    </div>
  </div>
</section>

<!-- ❌ FORBIDDEN — modal outside its container -->
<section class="orders-container">...</section>
<div class="orders-modal-overlay">...</div>  <!-- outside! tokens break, scope violated -->
```

### 2.4 `data-ref` — local to each container

`data-ref` values are scoped to their container by the `$` helper.
The same value may appear in two different containers without conflict:

```html
<!-- ✅ correct — same data-ref value, different containers -->
<section class="orders-container">
  <ul data-ref="items-list">...</ul>       <!-- found only by OrdersController -->
</section>

<section class="newsletters-container">
  <ul data-ref="items-list">...</ul>       <!-- found only by NewslettersController -->
</section>
```

This is safe because `$('[data-ref="items-list"]')` inside each controller
resolves against `this._root`, not `document`.

### 2.5 `id` attributes — must carry widget prefix

`id` is global in the DOM. On a many-containers page, two widgets without
prefixed ids will collide:

```html
<!-- ❌ FORBIDDEN — generic ids collide when both widgets are on the same page -->
<div role="dialog" aria-labelledby="modal-title">
  <h2 id="modal-title">Delete order?</h2>       <!-- widget A -->
</div>

<div role="dialog" aria-labelledby="modal-title">
  <h2 id="modal-title">Unsubscribe?</h2>        <!-- widget B — COLLISION -->
</div>

<!-- ✅ correct — prefixed ids, no collision -->
<div role="dialog" aria-labelledby="orders-modal-title">
  <h2 id="orders-modal-title">Delete order?</h2>
</div>

<div role="dialog" aria-labelledby="newsletters-modal-title">
  <h2 id="newsletters-modal-title">Unsubscribe?</h2>
</div>
```

### 2.6 Custom `data-*` attributes — must carry widget prefix

Custom data attributes are also global. Without a widget prefix they
collide between containers on the same page:

```html
<!-- ❌ FORBIDDEN — unprefixed custom attribute collides globally -->
<li class="orders-item"       data-priority="high">...</li>
<li class="newsletters-item"  data-priority="high">...</li>  <!-- same attribute name → ambiguous -->

<!-- ✅ correct — widget prefix prevents collision -->
<li class="orders-item"       data-orders-priority="high">...</li>
<li class="newsletters-item"  data-newsletters-priority="high">...</li>
```

---

## 3. CSS

### 3.1 Scoping — reinforced for multi-container pages

The base rule from §3.1 of `containerization-8.md` becomes the first line
of defence against cross-widget style leaks.

Every selector must start with its own container class.
No selector in widget A may start with widget B's container class:

```css
/* ✅ correct — each widget's rules start with its own container class */

/* orders.css block */
.orders-container .orders-item          { }
.orders-container .orders-modal-overlay { }

/* newsletters.css block */
.newsletters-container .newsletters-item          { }
.newsletters-container .newsletters-modal-overlay { }


/* ❌ FORBIDDEN — selector crosses widget boundary */
.orders-container .newsletters-item { }
```

### 3.2 CSS tokens — no cross-widget references

Tokens are declared on their own container. Widget B must never consume
widget A's tokens:

```css
/* ✅ correct — widget A consumes only its own tokens */
.orders-container {
  --orders-accent:      var(--bs-primary);
  --orders-card-radius: .5rem;
}
.orders-container .orders-card {
  border-radius: var(--orders-card-radius);
}

/* ✅ correct — widget B consumes only its own tokens */
.newsletters-container {
  --newsletters-accent:  var(--bs-success);
  --newsletters-radius:  .375rem;
}
.newsletters-container .newsletters-card {
  border-radius: var(--newsletters-radius);
}

/* ❌ FORBIDDEN — widget B reads widget A's token */
.newsletters-container .newsletters-card {
  border-radius: var(--orders-card-radius);
}
```

If two widgets need the same visual value, each declares its own token
that points to the same Bootstrap variable. They stay independent:

```css
/* ✅ correct — two tokens, same resolved value, each owned by its widget */
.orders-container       { --orders-radius:      .5rem; }
.newsletters-container  { --newsletters-radius: .5rem; }
```

### 3.3 `@keyframes` — widget prefix is critical on shared pages

Keyframe names are global. On a many-containers page two widgets with
identically named keyframes produce a silent collision — the second
`@keyframes` declaration wins and both animations break unpredictably:

```css
/* ❌ FORBIDDEN — generic name, guaranteed collision when both widgets are present */
@keyframes modal-in { from { opacity: 0; } to { opacity: 1; } }   /* widget A */
@keyframes modal-in { from { opacity: 0; } to { opacity: 1; } }   /* widget B — overwrites A */

/* ✅ correct — full widget prefix, no collision */
@keyframes orders-modal-in      { from { opacity: 0; } to { opacity: 1; } }
@keyframes newsletters-modal-in { from { opacity: 0; } to { opacity: 1; } }
```

### 3.4 Style block comment header — required

Each `<style>` block must begin with a one-line comment naming the widget:

```html
<style>
  /* ── Widget: orders ──────────────────────────────────── */

  /* 0. Tokens */
  .orders-container { ... }

  /* 1. Container layout */
  /* 2. Child elements */
  /* 3. Modals */
  /* 4. States */
  /* 5. Animations */
  /* 6. Responsive */
</style>

<style>
  /* ── Widget: newsletters ─────────────────────────────── */

  /* 0. Tokens */
  .newsletters-container { ... }
  ...
</style>
```

The comment header makes the file scannable and matches the extraction
boundary when widgets are split into separate files.

---

## 4. JavaScript

### 4.1 Class names — globally unique

JS class names live in the global scope of the page. Two controllers with
the same class name produce a silent overwrite — the second declaration
replaces the first:

```js
// ❌ FORBIDDEN — same class name for two different widgets
class WidgetController { ... }  // widget A — defines the class
class WidgetController { ... }  // widget B — silently overwrites widget A

// ✅ correct — each widget has a unique, descriptive class name
class OrdersController       { ... }
class NewslettersController  { ... }
class MySizesController      { ... }
```

### 4.2 Static properties — no cross-class references

Static properties (`FORBIDDEN_KEYS`, `SEED_DATA`, config constants) are
namespaced to their class. Widget B must never reference widget A's statics:

```js
// ❌ FORBIDDEN — cross-class static reference
class NewslettersController {
  constructor() {
    const raw = opts.data ?? OrdersController.SEED_DATA;  // borrows A's seed data
  }
}

// ✅ correct — each class owns its statics
class OrdersController {
  static SEED_DATA = [];
}

class NewslettersController {
  static SEED_DATA = [];
}
```

### 4.3 `this._root` — the isolation boundary

Every JS query inside a widget resolves against `this._root`, not against
`document`. This is the mechanical guarantee that widget A's JS cannot
touch widget B's DOM, even when both have identically named `data-ref`
values.

```js
// ✅ correct — $ scoped to this._root, physically cannot escape
class OrdersController {
  constructor(selector) {
    this._root = document.querySelector(selector);
    if (!this._root) return;

    const $ = sel => this._root.querySelector(sel);

    this._itemsList  = $('[data-ref="items-list"]');  // orders' list only
    this._deleteModal = $('[data-ref="modal-delete"]'); // orders' modal only
  }
}

class NewslettersController {
  constructor(selector) {
    this._root = document.querySelector(selector);
    if (!this._root) return;

    const $ = sel => this._root.querySelector(sel);

    this._itemsList      = $('[data-ref="items-list"]');      // newsletters' list only
    this._unsubscribeModal = $('[data-ref="modal-unsubscribe"]'); // newsletters' modal only
  }
}
```

### 4.4 `AbortController` — one per widget instance

Each widget instance has its own `this._ac`. Calling `destroy()` on
widget A does not affect widget B's listeners:

```js
// ✅ correct — independent AbortControllers
const ordersController       = new OrdersController('.orders-container');
const newslettersController  = new NewslettersController('.newsletters-container');

ordersController.destroy();       // removes ONLY orders listeners
newslettersController.destroy();  // removes ONLY newsletters listeners
```

This works automatically because each instance creates `this._ac = new AbortController()`
in its own constructor.

### 4.5 `Escape` key listener — widget-scoped state check

Each widget registers its own `document` keydown listener for `Escape`.
The handler checks its own modal state, so only the widget that currently
has an open modal will respond:

```js
// ✅ correct — each widget guards its own state
// In OrdersController._bind():
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && this._state.modal) this._closeModal();
}, sig);

// In NewslettersController._bind():
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && this._state.modal) this._closeModal();
}, sig);
```

If both widgets' modals are somehow open simultaneously, each `Escape`
handler checks only its own `this._state.modal` and closes only its own
modal. There is no cross-widget interference.

### 4.6 Script block comment header — required

Each `<script>` block must begin with a comment naming the widget,
mirroring the CSS convention:

```html
<script>
  /* ── Widget: orders ──────────────────────────────────── */

  class OrdersController {
    /* ... */
  }

  OrdersController.SEED_DATA = [];
</script>

<script>
  /* ── Widget: newsletters ─────────────────────────────── */

  class NewslettersController {
    /* ... */
  }

  NewslettersController.SEED_DATA = [];
</script>
```

---

## 5. Initialization (INIT)

### 5.1 Single `DOMContentLoaded` — all widgets

All widgets are initialized inside a single `DOMContentLoaded` listener.
One listener per widget is a violation:

```js
// ❌ FORBIDDEN — one DOMContentLoaded per widget
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container');
});
document.addEventListener('DOMContentLoaded', () => {
  new NewslettersController('.newsletters-container');
});

// ✅ correct — one shared listener, all widgets inside
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container');
  new NewslettersController('.newsletters-container');
  new MySizesController('.mysizes-container');
});
```

### 5.2 INIT block placement — last `<script>` on the page

The shared INIT block is always the last `<script>`. It must appear after
all widget `<script>` blocks, because it references their classes:

```html
<!-- widget scripts first -->
<script>/* OrdersController */</script>
<script>/* NewslettersController */</script>
<script>/* MySizesController */</script>

<!-- INIT last -->
<script>
  document.addEventListener('DOMContentLoaded', () => {
    new OrdersController('.orders-container');
    new NewslettersController('.newsletters-container');
    new MySizesController('.mysizes-container');
  });
</script>
```

### 5.3 Silent return — mandatory for all widgets

Every widget must use the silent return pattern. A missing container for
one widget must not prevent the others from initializing:

```js
// ✅ correct — silent return, other widgets are unaffected
constructor(selector, opts = {}) {
  this._root = document.querySelector(selector);
  if (!this._root) return;   // graceful — does not throw, does not block
  // ...
}

// ❌ WRONG — throwing blocks all subsequent new calls in DOMContentLoaded
constructor(selector) {
  this._root = document.querySelector(selector);
  if (!this._root) throw new Error('container not found');  // kills the entire INIT block
}
```

### 5.4 Multiple instances of the same widget type

When the same widget type appears more than once on the page (e.g., two
independent order lists), use `querySelectorAll` + `forEach`:

```js
document.addEventListener('DOMContentLoaded', () => {
  // Two separate instances — each is fully independent
  document.querySelectorAll('.orders-container').forEach(el => {
    new OrdersController(el);
  });

  // Other widget types use their own selectors
  new NewslettersController('.newsletters-container');
  new MySizesController('.mysizes-container');
});
```

The constructor accepts both a CSS selector string and a DOM element:

```js
constructor(selectorOrElement, opts = {}) {
  this._root = typeof selectorOrElement === 'string'
    ? document.querySelector(selectorOrElement)
    : selectorOrElement;
  if (!this._root) return;
  // ...
}
```

This allows the bare `new Controller('.selector')` form and the
`querySelectorAll` + `forEach` form to both work without modification.

### 5.5 INIT comment header — required

The shared INIT block must be labeled:

```html
<script>
  /* ── INIT ────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', () => {
    new OrdersController('.orders-container');
    new NewslettersController('.newsletters-container');
    new MySizesController('.mysizes-container');
  });
</script>
```

---

## 6. Namespace Isolation — full reference

This table shows every namespace that must be unique and how widget
prefix isolation applies to each on a many-containers page.

| Namespace | Scope | Isolation mechanism | Risk if not prefixed |
|---|---|---|---|
| CSS class | page-global | `.orders-` prefix on all classes | Style leaks between widgets |
| CSS custom property | inherited from container | `--orders-` prefix on all tokens | Token value overwritten by another widget |
| `@keyframes` name | page-global | `orders-` prefix on keyframe name | Animation overwritten by another widget |
| `id` attribute | page-global | `orders-` prefix on every `id` | ARIA labelledby points to wrong element |
| Custom `data-*` name | page-global | `data-orders-` prefix | Attribute misread by wrong widget |
| JS class name | page-global | `OrdersController` — full word | Second class declaration silently overwrites first |
| JS static property | class-scoped | inherited from class isolation | N/A once class names are unique |
| `data-ref` value | container-scoped via `$` helper | `this._root.querySelector` | Safe — reuse allowed across containers |
| `data-action` value | container-scoped via `e.target.closest` | delegation on `this._root` | Safe — reuse allowed across containers |

`data-ref` and `data-action` values are the only identifiers that do **not**
require a widget prefix, because they are queried through `this._root` and
are therefore already scoped to their container.

---

## 7. Anti-Patterns

### 7.1 Shared state object

```js
// ❌ FORBIDDEN — loose variable above any class, shared by all widgets
const sharedState = { activeUser: null };

class OrdersController {
  constructor() {
    sharedState.activeUser = ...;  // mutates a global — other widgets see the change
  }
}
```

Each widget owns its state entirely inside `this._state`. No widget reads
or writes another widget's state object.

### 7.2 Cross-container DOM queries

```js
// ❌ FORBIDDEN — widget A queries widget B's container
class OrdersController {
  _syncWithNewsletters() {
    const nl = document.querySelector('.newsletters-container');  // crosses the boundary
    nl.querySelector('[data-ref="items-list"]');
  }
}
```

If two widgets need to communicate, they do so through a shared data layer
(an external store, a custom event on `document`, or a parent module) —
never through direct DOM queries into each other's containers.

### 7.3 Shared AbortController across widgets

```js
// ❌ FORBIDDEN — one AbortController for multiple widget instances
const globalAc = new AbortController();

new OrdersController('.orders-container',       { ac: globalAc });
new NewslettersController('.newsletters-container', { ac: globalAc });

globalAc.abort();  // removes ALL listeners from ALL widgets at once
```

Each controller owns `this._ac`. `destroy()` on one widget must not
affect any other.

### 7.4 Styles in shared `<style>` block

```html
<!-- ❌ FORBIDDEN — two widgets share one <style> block -->
<style>
  .orders-container { ... }
  .newsletters-container { ... }
</style>
```

### 7.5 Multiple `DOMContentLoaded` blocks

```js
// ❌ FORBIDDEN — split INIT
document.addEventListener('DOMContentLoaded', () => { new OrdersController(...); });
document.addEventListener('DOMContentLoaded', () => { new NewslettersController(...); });
```

### 7.6 Generic unprefixed `@keyframes`

```css
/* ❌ FORBIDDEN — no prefix, collides with any other widget that defines modal-in */
@keyframes modal-in { from { opacity: 0; } to { opacity: 1; } }

/* ✅ correct */
@keyframes orders-modal-in      { from { opacity: 0; } to { opacity: 1; } }
@keyframes newsletters-modal-in { from { opacity: 0; } to { opacity: 1; } }
```

---

## 8. Worked Example — Three Widgets on One Page

```html
<!-- ═══════════════════════ BLOCK 1 — STYLES ════════════════════════ -->

<style>
  /* ── Widget: orders ──────────────────────────────────────────────── */

  /* 0. Tokens */
  .orders-container {
    --orders-accent:      var(--bs-primary);
    --orders-card-radius: .5rem;
    --orders-anim-dur:    150ms;
  }

  /* 1. Container layout */
  .orders-container { display: flex; flex-direction: column; gap: 1rem; }

  /* 2. Child elements */
  .orders-container .orders-list  { list-style: none; padding: 0; margin: 0; }
  .orders-container .orders-item  { display: flex; align-items: center; gap: .5rem; }

  /* 3. Modals */
  .orders-container .orders-modal-overlay {
    position: fixed; inset: 0; z-index: 1050;
    display: flex; align-items: center; justify-content: center;
    background: rgba(0,0,0,.45);
  }
  .orders-container .orders-modal-overlay[hidden] { display: none; }
  .orders-container .orders-modal {
    background: var(--bs-body-bg);
    border-radius: var(--orders-card-radius);
    padding: 1.5rem; width: min(480px, 90vw);
    animation: orders-modal-in var(--orders-anim-dur) ease-out both;
  }

  /* 4. States */
  .orders-container .orders-item[data-state="cancelled"] { opacity: .5; }

  /* 5. Animations */
  @keyframes orders-modal-in {
    from { opacity: 0; transform: scale(.95); }
    to   { opacity: 1; transform: scale(1);   }
  }

  /* 6. Responsive */
  @media (max-width: 576px) {
    .orders-container .orders-item { flex-direction: column; align-items: flex-start; }
  }
</style>

<style>
  /* ── Widget: newsletters ──────────────────────────────────────────── */

  /* 0. Tokens */
  .newsletters-container {
    --newsletters-accent: var(--bs-success);
    --newsletters-radius: .375rem;
    --newsletters-anim-dur: 120ms;
  }

  /* 1. Container layout */
  .newsletters-container { display: flex; flex-direction: column; gap: .75rem; }

  /* 2. Child elements */
  .newsletters-container .newsletters-list    { list-style: none; padding: 0; margin: 0; }
  .newsletters-container .newsletters-channel { display: flex; align-items: center; }

  /* 3. Modals */
  .newsletters-container .newsletters-modal-overlay {
    position: fixed; inset: 0; z-index: 1050;
    display: flex; align-items: center; justify-content: center;
    background: rgba(0,0,0,.45);
  }
  .newsletters-container .newsletters-modal-overlay[hidden] { display: none; }
  .newsletters-container .newsletters-modal {
    background: var(--bs-body-bg);
    border-radius: var(--newsletters-radius);
    padding: 1.5rem; width: min(480px, 90vw);
    animation: newsletters-modal-in var(--newsletters-anim-dur) ease-out both;
  }

  /* 4. States */
  .newsletters-container .newsletters-channel[data-state="subscribed"] { font-weight: 600; }

  /* 5. Animations */
  @keyframes newsletters-modal-in {
    from { opacity: 0; transform: scale(.95); }
    to   { opacity: 1; transform: scale(1);   }
  }
</style>

<style>
  /* ── Widget: mysizes ──────────────────────────────────────────────── */

  /* 0. Tokens */
  .mysizes-container {
    --mysizes-accent: var(--bs-info);
    --mysizes-radius: .25rem;
  }

  /* 1. Container layout */
  .mysizes-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; }

  /* 2. Child elements */
  .mysizes-container .mysizes-card  { padding: 1rem; border-radius: var(--mysizes-radius); }
  .mysizes-container .mysizes-label { font-size: .75rem; color: var(--bs-secondary-color); }
</style>


<!-- ═══════════════════════ BLOCK 2 — HTML ══════════════════════════ -->

<section class="orders-container" aria-label="Order list">

  <header class="orders-header">
    <h2 class="orders-title">Orders</h2>
  </header>

  <ul class="orders-list"
      data-ref="orders-list"
      role="listbox"
      aria-label="Orders"
      aria-activedescendant=""
      aria-live="polite">
  </ul>

  <!-- Modal — inside orders-container -->
  <div class="orders-modal-overlay"
       data-ref="modal-delete"
       role="dialog"
       aria-modal="true"
       aria-labelledby="orders-modal-title"
       hidden>
    <div class="orders-modal">
      <h2 id="orders-modal-title" class="orders-modal__title">Delete order?</h2>
      <p  class="orders-modal__body"  data-ref="modal-body"></p>
      <div class="orders-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Delete</button>
      </div>
    </div>
  </div>

</section>


<section class="newsletters-container" aria-label="Newsletter subscriptions">

  <header class="newsletters-header">
    <h2 class="newsletters-title">Newsletters</h2>
  </header>

  <ul class="newsletters-list"
      data-ref="newsletters-list"
      role="listbox"
      aria-label="Channels"
      aria-activedescendant="">
  </ul>

  <!-- Modal — inside newsletters-container -->
  <div class="newsletters-modal-overlay"
       data-ref="modal-unsubscribe"
       role="dialog"
       aria-modal="true"
       aria-labelledby="newsletters-modal-title"
       hidden>
    <div class="newsletters-modal">
      <h2 id="newsletters-modal-title" class="newsletters-modal__title">Unsubscribe?</h2>
      <p  class="newsletters-modal__body"  data-ref="modal-body"></p>
      <div class="newsletters-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Keep</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Unsubscribe</button>
      </div>
    </div>
  </div>

</section>


<section class="mysizes-container" aria-label="My sizes">

  <div data-ref="sizes-grid">
    <!-- rendered by MySizesController -->
  </div>

</section>


<!-- ═══════════════════════ BLOCK 3 — SCRIPTS ════════════════════════ -->

<script>
  /* ── Widget: orders ──────────────────────────────────────────────── */

  class OrdersController {

    static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
    static SEED_DATA       = [];

    constructor(selectorOrElement, opts = {}) {
      this._root = typeof selectorOrElement === 'string'
        ? document.querySelector(selectorOrElement)
        : selectorOrElement;
      if (!this._root) return;

      const $ = sel => this._root.querySelector(sel);

      this._ordersList  = $('[data-ref="orders-list"]');
      this._deleteModal = $('[data-ref="modal-delete"]');
      this._modalBody   = $('[data-ref="modal-body"]');

      const raw  = opts.data ?? OrdersController.SEED_DATA;
      const data = raw.filter(d => OrdersController._validate(d));

      this._state = { items: data, modal: null };
      this._ac    = new AbortController();

      this._render();
      this._bind();
    }

    _render()        { this._renderList(); this._renderModal(); }

    _renderList() {
      this._ordersList.innerHTML = this._state.items.map(item => `
        <li class="orders-item"
            data-id="${this._esc(item.id)}"
            data-state="${this._esc(item.status)}"
            role="option" aria-selected="false" tabindex="0">
          <span class="orders-item__name">${this._esc(item.name)}</span>
          <button class="btn btn-sm btn-danger"
                  data-action="modal-open-delete"
                  data-id="${this._esc(item.id)}">Remove</button>
        </li>
      `).join('');
    }

    _renderModal() {
      const { modal } = this._state;
      this._deleteModal.hidden = modal?.type !== 'delete';
      if (modal?.type === 'delete') {
        this._modalBody.textContent = `Delete order #${modal.targetId}?`;
      }
    }

    _handleOpenDelete(id) {
      this._lastFocused = document.activeElement;
      this._state.modal = { type: 'delete', targetId: id };
      this._renderModal();
      this._deleteModal.querySelector('button').focus();
    }

    _handleModalConfirm() {
      const { modal } = this._state;
      if (modal?.type === 'delete') {
        this._state.items = this._state.items.filter(i => i.id !== modal.targetId);
        this._renderList();
      }
      this._closeModal();
    }

    _closeModal() {
      this._state.modal = null;
      this._renderModal();
      this._lastFocused?.focus();
    }

    _bind() {
      const sig = { signal: this._ac.signal };

      this._root.addEventListener('click', e => {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        switch (btn.dataset.action) {
          case 'modal-open-delete': this._handleOpenDelete(btn.dataset.id); break;
          case 'modal-cancel':      this._closeModal();                     break;
          case 'modal-confirm':     this._handleModalConfirm();             break;
        }
      }, sig);

      document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && this._state.modal) this._closeModal();
      }, sig);
    }

    _esc(s) {
      return String(s ?? '')
        .replace(/&/g,  '&amp;').replace(/</g,  '&lt;') .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;').replace(/'/g,  '&#x27;')
        .replace(/\//g, '&#x2F;').replace(/`/g,  '&#x60;');
    }

    destroy() { this._ac.abort(); }

    static _validate(obj) {
      const forbidden = OrdersController.FORBIDDEN_KEYS;
      if (!obj || typeof obj !== 'object') return false;
      if (Object.keys(obj).some(k => forbidden.includes(k))) return false;
      for (const key of Object.keys(obj)) {
        if (Array.isArray(obj[key])) {
          for (const child of obj[key]) {
            if (!OrdersController._validate(child)) return false;
          }
        }
      }
      return true;
    }
  }
</script>

<script>
  /* ── Widget: newsletters ──────────────────────────────────────────── */

  class NewslettersController {

    static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
    static SEED_DATA       = [];

    constructor(selectorOrElement, opts = {}) {
      this._root = typeof selectorOrElement === 'string'
        ? document.querySelector(selectorOrElement)
        : selectorOrElement;
      if (!this._root) return;

      const $ = sel => this._root.querySelector(sel);

      this._channelsList     = $('[data-ref="newsletters-list"]');
      this._unsubscribeModal = $('[data-ref="modal-unsubscribe"]');
      this._modalBody        = $('[data-ref="modal-body"]');

      const raw  = opts.data ?? NewslettersController.SEED_DATA;
      const data = raw.filter(d => NewslettersController._validate(d));

      this._state = { channels: data, modal: null };
      this._ac    = new AbortController();

      this._render();
      this._bind();
    }

    _render()          { this._renderChannels(); this._renderModal(); }

    _renderChannels() {
      this._channelsList.innerHTML = this._state.channels.map(ch => `
        <li class="newsletters-channel"
            data-id="${this._esc(ch.id)}"
            data-state="${ch.subscribed ? 'subscribed' : 'unsubscribed'}"
            role="option" aria-selected="${ch.subscribed}" tabindex="0">
          <span class="newsletters-channel__name">${this._esc(ch.name)}</span>
          <button class="btn btn-sm btn-outline-danger"
                  data-action="modal-open-unsubscribe"
                  data-id="${this._esc(ch.id)}">Unsubscribe</button>
        </li>
      `).join('');
    }

    _renderModal() {
      const { modal } = this._state;
      this._unsubscribeModal.hidden = modal?.type !== 'unsubscribe';
      if (modal?.type === 'unsubscribe') {
        this._modalBody.textContent = `Unsubscribe from ${modal.channelName}?`;
      }
    }

    _handleOpenUnsubscribe(id) {
      const channel = this._state.channels.find(c => c.id === id);
      if (!channel) return;
      this._lastFocused = document.activeElement;
      this._state.modal = { type: 'unsubscribe', targetId: id, channelName: channel.name };
      this._renderModal();
      this._unsubscribeModal.querySelector('button').focus();
    }

    _handleModalConfirm() {
      const { modal } = this._state;
      if (modal?.type === 'unsubscribe') {
        const ch = this._state.channels.find(c => c.id === modal.targetId);
        if (ch) ch.subscribed = false;
        this._renderChannels();
      }
      this._closeModal();
    }

    _closeModal() {
      this._state.modal = null;
      this._renderModal();
      this._lastFocused?.focus();
    }

    _bind() {
      const sig = { signal: this._ac.signal };

      this._root.addEventListener('click', e => {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        switch (btn.dataset.action) {
          case 'modal-open-unsubscribe': this._handleOpenUnsubscribe(btn.dataset.id); break;
          case 'modal-cancel':           this._closeModal();                          break;
          case 'modal-confirm':          this._handleModalConfirm();                  break;
        }
      }, sig);

      document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && this._state.modal) this._closeModal();
      }, sig);
    }

    _esc(s) {
      return String(s ?? '')
        .replace(/&/g,  '&amp;').replace(/</g,  '&lt;') .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;').replace(/'/g,  '&#x27;')
        .replace(/\//g, '&#x2F;').replace(/`/g,  '&#x60;');
    }

    destroy() { this._ac.abort(); }

    static _validate(obj) {
      const forbidden = NewslettersController.FORBIDDEN_KEYS;
      if (!obj || typeof obj !== 'object') return false;
      if (Object.keys(obj).some(k => forbidden.includes(k))) return false;
      return true;
    }
  }
</script>

<script>
  /* ── Widget: mysizes ──────────────────────────────────────────────── */

  class MySizesController {

    static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
    static SEED_DATA       = [];

    constructor(selectorOrElement, opts = {}) {
      this._root = typeof selectorOrElement === 'string'
        ? document.querySelector(selectorOrElement)
        : selectorOrElement;
      if (!this._root) return;

      const $ = sel => this._root.querySelector(sel);

      this._sizesGrid = $('[data-ref="sizes-grid"]');

      const raw  = opts.data ?? MySizesController.SEED_DATA;
      const data = raw.filter(d => MySizesController._validate(d));

      this._state = { sizes: data };
      this._ac    = new AbortController();

      this._render();
      this._bind();
    }

    _render() {
      this._sizesGrid.innerHTML = this._state.sizes.map(s => `
        <div class="mysizes-card">
          <span class="mysizes-label">${this._esc(s.label)}</span>
          <span class="mysizes-value">${this._esc(s.value)}</span>
        </div>
      `).join('');
    }

    _bind() {
      const sig = { signal: this._ac.signal };

      this._root.addEventListener('click', e => {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        // future actions handled here
      }, sig);
    }

    _esc(s) {
      return String(s ?? '')
        .replace(/&/g,  '&amp;').replace(/</g,  '&lt;') .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;').replace(/'/g,  '&#x27;')
        .replace(/\//g, '&#x2F;').replace(/`/g,  '&#x60;');
    }

    destroy() { this._ac.abort(); }

    static _validate(obj) {
      const forbidden = MySizesController.FORBIDDEN_KEYS;
      if (!obj || typeof obj !== 'object') return false;
      if (Object.keys(obj).some(k => forbidden.includes(k))) return false;
      return true;
    }
  }
</script>

<script>
  /* ── INIT ──────────────────────────────────────────────────────────── */

  document.addEventListener('DOMContentLoaded', () => {
    new OrdersController('.orders-container');
    new NewslettersController('.newsletters-container');
    new MySizesController('.mysizes-container');
  });
</script>
```

---

## 9. Pre-Commit Checklist — Many Containers Extension

This checklist supplements §8 of `containerization-8.md`.
Run both checklists when working on a many-containers page.

### Page structure
- [ ] Styles block comes before HTML block, HTML block before scripts block
- [ ] Each widget has its own `<style>` block — no two widgets share one
- [ ] Each widget class is in its own `<script>` block — no two classes share one
- [ ] INIT block is the last `<script>` on the page
- [ ] INIT contains exactly one `DOMContentLoaded` listener — no per-widget listeners

### HTML isolation
- [ ] Containers are siblings — never nested inside each other
- [ ] Each container class is unique across the page — no two widgets share a container class
- [ ] Every `id` carries the widget's full word prefix — checked across ALL widgets on the page for collisions
- [ ] Custom `data-*` attribute names carry the widget prefix — checked for collision with other widgets
- [ ] Modals are inside their own container — not at the page level or inside another widget

### CSS isolation
- [ ] Every `@keyframes` name carries the widget prefix — checked across ALL style blocks for collision
- [ ] CSS token names carry the widget prefix — checked across ALL style blocks
- [ ] No selector in widget A starts with widget B's container class
- [ ] No widget B rule consumes widget A's CSS custom properties
- [ ] Each `<style>` block starts with a `/* ── Widget: name ── */` comment

### JS isolation
- [ ] All controller class names are unique across the page
- [ ] No controller's static property references another controller's class
- [ ] No controller's method queries outside `this._root`
- [ ] Each controller has its own `this._ac` — no shared AbortController
- [ ] Constructor accepts both a selector string and a DOM element (for `querySelectorAll` bootstrap)
- [ ] Each `<script>` block starts with a `/* ── Widget: name ── */` comment
- [ ] INIT block starts with a `/* ── INIT ── */` comment

### INIT
- [ ] One `DOMContentLoaded` covers all widgets
- [ ] `new Widget('.container')` uses silent return — no widget throws on missing container
- [ ] Same-type multiple instances use `querySelectorAll + forEach` pattern
