# Containerization — Orchestration — v2
## Multiple Widgets on a Page: Declarations, Init, and Cross-Widget Communication

> This document does not repeat the containerization rules.
> It assumes every widget on this page follows containerization-11.md.
> The subject here is: how independent, isolated widgets coexist and communicate on the same page.

---

## Changelog v1 → v2

- Updated reference from `containerization-10.md` → `containerization-11.md` throughout.
- **§2 Orchestrator CSS** — `@keyframes` example name updated; confirmed no `__` usage was present.
- **§10 Naming Conventions** — table note added: all child class names follow flat kebab-case per v11; `__` is forbidden in orchestrator stylesheets as well.

---

## What Orchestration Is

Each widget is a sealed unit. It owns its DOM, its state, its listeners. It does not know what else is on the page. Orchestration is everything that happens **outside** those sealed units:

- declaring multiple containers in HTML
- booting them in the correct order
- routing messages between them
- managing their lifecycle as a group

Orchestration never reaches inside a widget. It speaks to widgets only through the interfaces they expose: constructor options (Layer 2) and custom DOM events.

---

## The Orchestrator Is Also a Container

A page orchestrator is not a loose script floating above the widgets. It is itself a container — it has a CSS class, scoped styles, and a controller class that follows the same constructor shape as any widget.

The difference between an orchestrator and a widget:

| | Widget controller | Orchestrator controller |
|---|---|---|
| Has `_state` | ✅ yes — owns data | ❌ no — owns no data |
| Has `_render()` | ✅ yes — owns DOM output | ❌ no — owns no DOM output |
| Has `data-ref` cache | ✅ yes — for its own children | ❌ no — its children are widget containers |
| Has `_bind()` | ✅ yes — user events | ✅ yes — cross-widget custom events |
| Has `destroy()` | ✅ yes — own AC | ✅ yes — own AC + child widget destroy |
| Has CSS | ✅ yes — full widget styles | ✅ yes — layout and tokens only |
| Found by | CSS class selector | CSS class selector |
| Instantiated in INIT | `new WidgetController('.widget-container')` | `new PageController('.page-container')` |

Everything else is the same. The orchestrator is a first-class container.

---

## 1. Orchestrator — HTML

The orchestrator container wraps all widget containers it coordinates. It follows the same naming rules as any widget: full word(s) + a meaningful suffix.

Recommended suffixes:
- `-page` — page-level orchestrator, wraps the entire page content
- `-panel` — section-level orchestrator, wraps a group of widgets within a larger page

```html
<!-- ✅ correct — orchestrator as a proper semantic container -->
<div class="checkout-page" aria-label="Checkout">

  <section class="cart-container"    aria-label="Shopping cart">    <!-- cart widget -->    </section>
  <section class="summary-container" aria-label="Order summary">    <!-- summary widget --> </section>
  <section class="promo-container"   aria-label="Promo code">       <!-- promo widget -->   </section>

</div>

<!-- ✅ correct — section-level orchestrator (panel within a larger page) -->
<div class="catalog-panel" aria-label="Product catalog">

  <section class="filters-container"    aria-label="Filters">          <!-- filters widget -->    </section>
  <section class="products-container"   aria-label="Products">         <!-- products widget -->   </section>
  <section class="pagination-container" aria-label="Pagination">       <!-- pagination widget --> </section>

</div>

<!-- ❌ wrong — no container class on the orchestrator, widgets are floating -->
<div>
  <section class="cart-container">    </section>
  <section class="summary-container"> </section>
</div>

<!-- ❌ wrong — id on the orchestrator root -->
<div id="checkout" class="checkout-page">
  ...
</div>

<!-- ❌ wrong — data-ref on the orchestrator root (it is found by CSS class, not data attribute) -->
<div class="checkout-page" data-ref="checkout-root">
  ...
</div>
```

---

## 2. Orchestrator — CSS

The orchestrator's stylesheet follows the same six-section order as any widget. The key difference: it contains **layout and tokens only** — it never styles widget internals.

```css
<style>
  /* ─── 0. Tokens ─────────────────────────────────────────────────── */
  /* Page-level design tokens. Child widgets inherit these             */
  /* automatically via CSS custom property cascade.                    */
  /* Token names follow the orchestrator's full word prefix.           */

  .checkout-page {
    --checkout-gap:       1.5rem;
    --checkout-col-main:  1fr;
    --checkout-col-aside: 360px;
    --checkout-radius:    .5rem;
  }

  /* ─── 1. Container layout ───────────────────────────────────────── */
  /* Arranges direct children — the widget containers.                 */
  /* Never reaches inside a widget container.                          */

  .checkout-page {
    display:               grid;
    grid-template-columns: var(--checkout-col-main) var(--checkout-col-aside);
    grid-template-rows:    auto 1fr auto;
    gap:                   var(--checkout-gap);
    align-items:           start;
    padding:               var(--checkout-gap);
  }

  /* ─── 2. Widget container placement ─────────────────────────────── */
  /* Only grid/flex positioning of the container box itself.           */
  /* Internal widget layout is each widget's own responsibility.       */

  .checkout-page .cart-container {
    grid-column: 1;
    grid-row:    1 / 3;
  }

  .checkout-page .summary-container {
    grid-column: 2;
    grid-row:    1;
  }

  .checkout-page .promo-container {
    grid-column: 2;
    grid-row:    2;
    align-self:  start;
  }

  /* ─── 3. Modals ─────────────────────────────────────────────────── */
  /* Orchestrators rarely have their own modals.                       */
  /* If present, follow the same modal rules as any widget.            */

  /* ─── 4. States ─────────────────────────────────────────────────── */
  /* Orchestrator-level states: loading, complete, error, etc.         */
  /* Set via this._root.dataset.state in the orchestrator's methods.   */

  .checkout-page[data-state="loading"] .cart-container,
  .checkout-page[data-state="loading"] .summary-container {
    pointer-events: none;
    opacity:        .5;
  }

  .checkout-page[data-state="complete"] .promo-container {
    display: none;
  }

  /* ─── 5. Animations ─────────────────────────────────────────────── */
  /* @keyframes names carry the orchestrator's full word prefix.       */

  @keyframes checkout-page-fade-in {
    from { opacity: 0; }
    to   { opacity: 1; }
  }

  .checkout-page {
    animation: checkout-page-fade-in 200ms ease both;
  }

  /* ─── 6. Responsive ─────────────────────────────────────────────── */

  @media (max-width: 768px) {
    .checkout-page {
      grid-template-columns: 1fr;
    }

    .checkout-page .cart-container,
    .checkout-page .summary-container,
    .checkout-page .promo-container {
      grid-column: 1;
      grid-row:    auto;
    }
  }
</style>
```

**What the orchestrator's CSS must not do:**

```css
/* ❌ wrong — reaching into widget internals from the orchestrator */
.checkout-page .cart-item        { border-radius: .5rem; }
.checkout-page .summary-total    { font-size: 1.5rem; }
.checkout-page .promo-input      { border-color: red; }

/* ✅ correct — only the container box itself is positioned */
.checkout-page .cart-container    { grid-column: 1; }
.checkout-page .summary-container { grid-column: 2; }
```

**Token inheritance:** child widgets can consume orchestrator tokens by referencing them in their own token declarations:

```css
/* inside cart widget stylesheet */
.cart-container {
  --cart-radius: var(--checkout-radius, .5rem); /* falls back if not inside checkout-page */
}
```

---

## 3. Orchestrator — JS

The controller follows the same constructor shape as any widget. It receives a selector, finds its root, sets up `AbortController`, and wires its listeners in `_bind()`.

What it does **not** have: `_state`, `_render()`, `data-ref` caches for its own children.

```js
class CheckoutPageController {

  // ─── 0. STATIC CONFIG ──────────────────────────────────────
  // Add static DEFAULTS only if the orchestrator itself accepts
  // configuration via data attributes (e.g. feature flags).
  // Most orchestrators have no DEFAULTS.

  // ─── 1. CONSTRUCTOR ────────────────────────────────────────
  constructor(selector, opts = {}) {

    // 1a. Find own root — same silent return as any widget
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // 1b. Instantiate child widgets
    //     Pass selector strings — each widget finds its own root.
    //     opts slices allow the caller to configure individual widgets
    //     without the orchestrator knowing what those options mean.
    this._cart    = new CartController('.cart-container',       opts.cart    ?? {});
    this._summary = new SummaryController('.summary-container', opts.summary ?? {});
    this._promo   = new PromoController('.promo-container',     opts.promo   ?? {});

    // 1c. No _state here.
    //     If page-level state is needed (e.g. current step), use a plain scalar:
    // this._step = 'cart';
    //     Never use a reactive state object — the orchestrator does not render.

    // 1d. AbortController — for the orchestrator's own listeners only
    this._ac = new AbortController();

    // 1e. Wire cross-widget communication
    this._bind();
  }

  // ─── 2. EVENTS — cross-widget wiring ───────────────────────
  _bind() {
    const sig = { signal: this._ac.signal };

    // promo applied → summary recalculates
    document.addEventListener('promo:applied', e => {
      this._summary.applyDiscount(e.detail.code, e.detail.discount);
    }, sig);

    // cart changed → summary re-totals
    document.addEventListener('cart:changed', e => {
      this._summary.refresh(e.detail.items);
    }, sig);

    // summary confirmed → page enters loading state
    document.addEventListener('summary:confirmed', () => {
      this._root.dataset.state = 'loading';
    }, sig);
  }

  // ─── 3. LIFECYCLE ──────────────────────────────────────────

  destroy() {
    // Destroy child widgets first — they remove their own listeners
    this._cart?.destroy();
    this._summary?.destroy();
    this._promo?.destroy();

    // Remove orchestrator's own listeners last
    this._ac.abort();
  }
}
```

---

## 4. INIT

The orchestrator is initialized exactly like any widget — one line inside `DOMContentLoaded`.

```js
// ✅ bare new — recommended when the instance is not referenced later
document.addEventListener('DOMContentLoaded', () => {
  new CheckoutPageController('.checkout-page');
});

// ✅ assigned — when destroy() must be called from outside (e.g. SPA router)
document.addEventListener('DOMContentLoaded', () => {
  const checkoutPage = new CheckoutPageController('.checkout-page');
});

// ✅ with Layer 2 opts — forwarding config to child widgets
document.addEventListener('DOMContentLoaded', () => {
  new CheckoutPageController('.checkout-page', {
    cart:    { data: window.__cartData },
    summary: { currency: 'USD' },
  });
});

// ❌ wrong — wiring logic in INIT, bypasses the orchestrator class
document.addEventListener('DOMContentLoaded', () => {
  const cart    = new CartController('.cart-container');
  const summary = new SummaryController('.summary-container');
  document.addEventListener('cart:changed', e => summary.refresh(e.detail.items));
});
```

---

## 5. Forwarding Config to Child Widgets

The orchestrator receives `opts` and forwards slices to each child. Children never know the orchestrator exists — they only see their own `opts`.

```js
constructor(selector, opts = {}) {
  this._root = document.querySelector(selector);
  if (!this._root) return;

  // read orchestrator-level data attributes if any
  const currency = this._root.dataset.checkoutCurrency ?? 'USD';

  // forward separate slices — child widgets are unaware of each other
  this._cart    = new CartController('.cart-container',       { currency, ...opts.cart    });
  this._summary = new SummaryController('.summary-container', { currency, ...opts.summary });
  this._promo   = new PromoController('.promo-container',     {           ...opts.promo   });

  this._ac = new AbortController();
  this._bind();
}
```

HTML for orchestrator-level config:

```html
<!-- orchestrator reads data-checkout-* via this._root.dataset -->
<div class="checkout-page"
     data-checkout-currency="USD"
     aria-label="Checkout">

  <section class="cart-container">    </section>
  <section class="summary-container"> </section>
  <section class="promo-container">   </section>

</div>
```

---

## 6. Nested Orchestrators

A page can have an orchestrator at page level and one or more orchestrators at panel level. Each is a container in its own right. They follow the same nesting rules as widgets within an orchestrator.

### HTML

```html
<div class="account-page" aria-label="My account">

  <!-- panel orchestrator — coordinates filters + orders + pagination -->
  <div class="orders-panel" aria-label="My orders">
    <section class="filters-container"    aria-label="Filters">    </section>
    <section class="orders-container"     aria-label="Orders">     </section>
    <section class="pagination-container" aria-label="Pagination"> </section>
  </div>

  <!-- standalone widget — no coordination needed -->
  <section class="mysizes-container" aria-label="My sizes"> </section>

</div>
```

### CSS

```css
/* page orchestrator — positions its direct children */
.account-page {
  --account-gap: 2rem;

  display: grid;
  grid-template-columns: 1fr 320px;
  gap: var(--account-gap);
}

.account-page .orders-panel       { grid-column: 1; }
.account-page .mysizes-container  { grid-column: 2; }

/* panel orchestrator — positions its direct children */
.orders-panel {
  --orders-panel-gap: 1rem;

  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: var(--orders-panel-gap);
}

.orders-panel .filters-container    { grid-row: 1; }
.orders-panel .orders-container     { grid-row: 2; }
.orders-panel .pagination-container { grid-row: 3; }
```

### JS

```js
class AccountPageController {

  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;

    // panel orchestrator — owns its own widget group
    this._ordersPanel = new OrdersPanelController('.orders-panel');

    // standalone widget
    this._mysizes = new MySizesController('.mysizes-container');

    this._ac = new AbortController();
    this._bind();
  }

  _bind() {
    const sig = { signal: this._ac.signal };

    // account-level wiring: mysizes change → orders panel refilters
    document.addEventListener('mysizes:saved', e => {
      // calls a public method on the panel orchestrator — not on its internal widgets
      this._ordersPanel.applySize(e.detail.size);
    }, sig);
  }

  destroy() {
    this._ordersPanel.destroy();
    this._mysizes.destroy();
    this._ac.abort();
  }
}

class OrdersPanelController {

  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;

    this._filters    = new FiltersController('.filters-container');
    this._orders     = new OrdersController('.orders-container');
    this._pagination = new PaginationController('.pagination-container');

    this._ac = new AbortController();
    this._bind();
  }

  _bind() {
    const sig = { signal: this._ac.signal };

    document.addEventListener('filters:changed', e => {
      this._orders.filter(e.detail.criteria);
      this._pagination.reset();
    }, sig);

    document.addEventListener('pagination:page-changed', e => {
      this._orders.loadPage(e.detail.page);
    }, sig);
  }

  // Public method — called by the parent orchestrator, not by external code
  applySize(size) {
    this._filters.setSize(size);
  }

  destroy() {
    this._filters.destroy();
    this._orders.destroy();
    this._pagination.destroy();
    this._ac.abort();
  }
}
```

**Rule:** a parent orchestrator calls public methods on its direct child orchestrator. It never bypasses it to call methods on the child orchestrator's internal widgets.

```js
// ✅ correct — parent calls the child orchestrator's public API
this._ordersPanel.applySize(e.detail.size);

// ❌ wrong — parent bypasses the child orchestrator
this._ordersPanel._filters.setSize(e.detail.size);
```

---

## 7. Cross-Widget Communication

### 7.1 The rule

Widgets communicate exclusively through **custom DOM events on `document`**. A widget never imports, references, or calls another widget's instance directly.

```js
// ✅ correct — widget emits, does not care who listens
document.dispatchEvent(new CustomEvent('cart:item-added', {
  detail: { itemId: '42', quantity: 1 },
  bubbles: false,
}));

// ✅ correct — orchestrator listens and routes to the right widget
document.addEventListener('cart:item-added', e => {
  this._summary.refresh(e.detail);
}, { signal: this._ac.signal });

// ❌ wrong — widget holds a direct reference to another widget
this._summary._updateTotal(item.price);

// ❌ wrong — querying another widget's DOM
document.querySelector('.cart-container [data-ref="badge"]').textContent = count;
```

### 7.2 Event naming

Format: `[widget]:[verb]-[noun]`

| ✅ Correct | ❌ Wrong |
|---|---|
| `cart:item-added` | `itemAdded`, `cartUpdate` |
| `filters:changed` | `filtersChange`, `fc` |
| `promo:applied` | `promo-applied`, `promoOk` |
| `pagination:page-changed` | `pageChanged`, `pg` |
| `mysizes:saved` | `sizesSave`, `ms` |

### 7.3 Event payload

`detail` is a plain serializable object. No DOM nodes, no class instances, no functions.

```js
// ✅ correct — serializable primitives and plain objects
document.dispatchEvent(new CustomEvent('cart:item-added', {
  detail: { itemId: '42', quantity: 1, price: 29.99 },
}));

// ❌ wrong — DOM node in detail
document.dispatchEvent(new CustomEvent('cart:item-added', {
  detail: { element: this._itemEl },
}));

// ❌ wrong — callback in detail
document.dispatchEvent(new CustomEvent('cart:item-added', {
  detail: { onUndo: () => this._undo() },
}));
```

### 7.4 Listener cleanup

All `document` listeners registered inside a widget or orchestrator must use `this._ac.signal`.

```js
// inside CartController._bind() — removed when cart.destroy() is called
document.addEventListener('promo:applied', e => {
  this._applyDiscount(e.detail.code, e.detail.discount);
}, { signal: this._ac.signal });

// inside CheckoutPageController._bind() — removed when checkoutPage.destroy() is called
document.addEventListener('cart:changed', e => {
  this._summary.refresh(e.detail.items);
}, { signal: this._ac.signal });
```

---

## 8. Lifecycle

### 8.1 Static page — no teardown needed

Full page navigations discard all listeners. `destroy()` is never called.

```js
document.addEventListener('DOMContentLoaded', () => {
  new CheckoutPageController('.checkout-page');
});
```

### 8.2 SPA navigation — destroy on unmount

```js
const page = new CheckoutPageController('.checkout-page');

// before route change — cascades through all child widgets
page.destroy();
```

### 8.3 Tab panels — destroy on hide, recreate on show

```js
_switchTo(tabName) {
  // one destroy() on the orchestrator tears down all its child widgets
  if (this._active) {
    this._active.destroy();
    this._active = null;
  }

  this._root.querySelectorAll('[data-ref^="tab-"]').forEach(panel => {
    panel.hidden = panel.dataset.ref !== `tab-${tabName}`;
  });

  switch (tabName) {
    case 'checkout': this._active = new CheckoutPageController('.checkout-page'); break;
    case 'account':  this._active = new AccountPageController('.account-page');  break;
  }
}
```

One `destroy()` on the page orchestrator cascades through every child widget automatically.

---

## 9. Anti-Patterns

### 9.1 Widget-to-widget direct reference

```js
// ❌ wrong — CartController holds a reference to SummaryController
class CartController {
  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;
    this._summary = opts.summaryController; // injected external instance
  }
  _handleItemAdded(item) {
    this._summary._updateTotal(item.price); // calls private method of another widget
  }
}

// ✅ correct — emit and let the orchestrator route
class CartController {
  _handleItemAdded(item) {
    document.dispatchEvent(new CustomEvent('cart:item-added', {
      detail: { price: item.price },
    }));
  }
}
```

### 9.2 Global widget registry

```js
// ❌ wrong
window.__widgets = window.__widgets || {};
window.__widgets.cart = this; // inside CartController constructor
window.__widgets.cart._updateBadge(); // uncontrolled external access

// ✅ correct — orchestrator holds references privately
class CheckoutPageController {
  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;
    this._cart    = new CartController('.cart-container');
    this._summary = new SummaryController('.summary-container');
    // ...
  }
}
```

### 9.3 Logic in INIT

```js
// ❌ wrong — coordination logic in INIT
document.addEventListener('DOMContentLoaded', () => {
  const cart    = new CartController('.cart-container');
  const summary = new SummaryController('.summary-container');
  document.addEventListener('cart:item-added', e => {
    summary._updateTotal(e.detail.price); // belongs in CheckoutPageController._bind()
  });
});

// ✅ correct
document.addEventListener('DOMContentLoaded', () => {
  new CheckoutPageController('.checkout-page');
});
```

### 9.4 Parent bypasses child orchestrator

```js
// ❌ wrong — AccountPageController reaches past OrdersPanelController
this._ordersPanel._filters.setSize(size); // internals of the panel

// ✅ correct — calls the panel's public method
this._ordersPanel.applySize(size);
```

### 9.5 Widget instantiated inside another widget

```js
// ❌ wrong — OrdersController creates PaginationController
class OrdersController {
  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;
    this._pagination = new PaginationController('.pagination-container'); // wrong
  }
}

// ✅ correct — the orchestrator owns both
class OrdersPanelController {
  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;
    this._orders     = new OrdersController('.orders-container');
    this._pagination = new PaginationController('.pagination-container');
    this._ac = new AbortController();
    this._bind();
  }
}
```

---

## 10. Naming Conventions

| What | Convention | ✅ Correct | ❌ Wrong |
|---|---|---|---|
| Page orchestrator class | PascalCase + `PageController` | `CheckoutPageController` | `CheckoutCtrl`, `ChPgCO` |
| Panel orchestrator class | PascalCase + `PanelController` | `OrdersPanelController` | `OrdersPanel`, `OPC` |
| Page container CSS class | full word(s) + `-page` | `.checkout-page` | `.co-p`, `.chk-pg` |
| Panel container CSS class | full word(s) + `-panel` | `.orders-panel` | `.ord-p`, `.op` |
| CSS token prefix | full container word | `--checkout-gap` | `--co-gap` |
| Child class naming | flat kebab-case only — no `__` | `.checkout-page .cart-container` | `.checkout-page .cart__container` |
| Custom event name | `[widget]:[verb]-[noun]` | `cart:item-added` | `itemAdded`, `ci` |

---

## 11. Summary: Responsibility Map

```
┌────────────────────────────────────────────────────────────────────┐
│  INIT  (DOMContentLoaded — one line, no logic)                     │
│  new CheckoutPageController('.checkout-page')                      │
└──────────────────────────┬─────────────────────────────────────────┘
                           │
         ┌─────────────────▼──────────────────────┐
         │  Page Orchestrator  .checkout-page      │
         │  CheckoutPageController                 │
         │                                         │
         │  CSS  — layout grid, tokens             │
         │  JS   — constructor(selector, opts)     │
         │         silent return                   │
         │         instantiates child widgets      │
         │         _bind() — cross-widget events   │
         │         destroy() — children + own AC   │
         │         NO _state, NO _render()         │
         └───┬────────────┬────────────┬───────────┘
             │            │            │
    ┌────────▼───┐ ┌──────▼─────┐ ┌───▼──────────┐
    │  Widget    │ │  Widget    │ │  Widget      │
    │  .cart-    │ │  .summary- │ │  .promo-     │
    │  container │ │  container │ │  container   │
    │            │ │            │ │              │
    │  CSS full  │ │  CSS full  │ │  CSS full    │
    │  owns DOM  │ │  owns DOM  │ │  owns DOM    │
    │  owns state│ │  owns state│ │  owns state  │
    │  emits     │ │  emits     │ │  emits       │
    └─────┬──────┘ └─────┬──────┘ └──────┬───────┘
          │              │               │
          └──────────────▼───────────────┘
                      document
              custom events — the only legal
              cross-widget communication channel
              payload: plain serializable objects
```
