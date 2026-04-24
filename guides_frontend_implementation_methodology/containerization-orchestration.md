# Containerization — Orchestration
## Multiple Widgets on a Page: Declarations, Init, and Cross-Widget Communication

> This document does not repeat the containerization rules.
> It assumes every widget on this page follows containerization-10.md.
> The subject here is: how independent, isolated widgets coexist and communicate on the same page.

---

## What Orchestration Is

Each widget is a sealed unit. It owns its DOM, its state, its listeners. It does not know what else is on the page. Orchestration is everything that happens **outside** those sealed units:

- declaring multiple containers in HTML
- booting them in the correct order
- routing messages between them
- managing their lifecycle as a group

Orchestration never reaches inside a widget. It speaks to widgets only through the interfaces they expose: constructor options (Layer 2) and custom DOM events.

---

## 1. Declarative Container Layout

### 1.1 Independent widgets — no communication

The simplest case. Each widget does its own thing. They share a page but have no relationship.

```html
<main class="page-layout">

  <section class="orders-container" aria-label="Order list">
    <!-- orders widget markup -->
  </section>

  <section class="newsletters-container" aria-label="Newsletter subscriptions">
    <!-- newsletters widget markup -->
  </section>

  <section class="mysizes-container" aria-label="My sizes">
    <!-- mysizes widget markup -->
  </section>

</main>
```

```js
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container');
  new NewslettersController('.newsletters-container');
  new MySizesController('.mysizes-container');
});
```

No orchestration layer needed. Each controller boots, runs, and cleans up independently.

---

### 1.2 Multiple instances of the same widget

Same class, different containers, different config per instance via data attributes.

```html
<section class="products-container"
         data-products-layout="grid"
         data-products-limit="12"
         aria-label="Featured products">
  <!-- products widget markup -->
</section>

<section class="products-container"
         data-products-layout="list"
         data-products-limit="5"
         aria-label="Recently viewed">
  <!-- products widget markup -->
</section>
```

```js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.products-container').forEach(el => {
    new ProductsController(el);
  });
});
```

Each instance reads its own `data-products-*` attributes in `_readDataAttrs()`. They never share state.

---

### 1.3 Widgets that need to communicate — sibling layout

Siblings are declared at the same level. Neither owns the other. Communication goes through a shared custom event on `document`.

```html
<div class="page-checkout">

  <section class="cart-container" aria-label="Shopping cart">
    <!-- cart widget markup -->
  </section>

  <section class="summary-container" aria-label="Order summary">
    <!-- summary widget markup -->
  </section>

  <section class="promo-container" aria-label="Promo code">
    <!-- promo widget markup -->
  </section>

</div>
```

```js
document.addEventListener('DOMContentLoaded', () => {
  new CartController('.cart-container');
  new SummaryController('.summary-container');
  new PromoController('.promo-container');
});
```

---

### 1.4 Primary widget with a dependent satellite

The satellite exists to react to the primary widget's output. Its container sits adjacent in the DOM.

```html
<div class="page-catalog">

  <section class="filters-container" aria-label="Product filters">
    <!-- filters widget markup -->
  </section>

  <section class="catalog-container" aria-label="Product catalog">
    <!-- catalog widget markup -->
  </section>

</div>
```

```js
document.addEventListener('DOMContentLoaded', () => {
  new FiltersController('.filters-container');
  new CatalogController('.catalog-container');
  // FiltersController emits 'filters:changed' on document
  // CatalogController listens for 'filters:changed' and re-fetches
});
```

---

### 1.5 Page orchestrator — explicit coordination

When coordination logic is non-trivial, it lives in a dedicated `PageController`. The page controller owns no DOM of its own — it holds references to widget instances and wires them together.

```html
<div class="page-dashboard">

  <section class="stats-container"      aria-label="Statistics">   </section>
  <section class="activity-container"   aria-label="Recent activity"> </section>
  <section class="notifications-container" aria-label="Notifications"> </section>

</div>
```

```js
document.addEventListener('DOMContentLoaded', () => {
  new DashboardPageController();
});
```

```js
class DashboardPageController {

  constructor() {
    this._stats         = new StatsController('.stats-container');
    this._activity      = new ActivityController('.activity-container');
    this._notifications = new NotificationsController('.notifications-container');

    this._bind();
  }

  _bind() {
    document.addEventListener('stats:period-changed', e => {
      this._activity.refresh(e.detail.period);
    });

    document.addEventListener('notifications:cleared', () => {
      this._stats.refresh();
    });
  }

  destroy() {
    this._stats.destroy();
    this._activity.destroy();
    this._notifications.destroy();
  }
}
```

`DashboardPageController` knows about the widgets. The widgets do not know about `DashboardPageController` or each other.

---

## 2. Cross-Widget Communication

### 2.1 The rule

Widgets communicate exclusively through **custom DOM events on `document`**. A widget never imports, references, or calls another widget's instance directly.

```js
// ✅ correct — widget emits, does not care who listens
document.dispatchEvent(new CustomEvent('cart:item-added', {
  detail: { itemId: '42', quantity: 1 },
  bubbles: false,
}));

// ✅ correct — another widget listens, does not care who emitted
document.addEventListener('cart:item-added', e => {
  this._updateTotal(e.detail.itemId, e.detail.quantity);
}, { signal: this._ac.signal });

// ❌ wrong — widget holds a direct reference to another widget
this._summary = window.summaryController; // global coupling
this._summary._updateTotal(itemId, qty);  // reaches into internals

// ❌ wrong — widget queries another widget's DOM
const badge = document.querySelector('.cart-container [data-ref="badge"]');
```

### 2.2 Event naming

Format: `[widget]:[verb]-[noun]`

| ✅ Correct | ❌ Wrong |
|---|---|
| `cart:item-added` | `itemAdded` |
| `filters:changed` | `filtersUpdate` |
| `promo:applied` | `promo-applied` |
| `notifications:cleared` | `clear` |

Full widget word, no abbreviations. Same naming rule as classes and data attributes.

### 2.3 Event payload — `detail`

`detail` is a plain serializable object. No DOM nodes, no class instances, no functions.

```js
// ✅ correct — serializable primitives and plain objects
document.dispatchEvent(new CustomEvent('cart:item-added', {
  detail: { itemId: '42', quantity: 1, price: 29.99 },
}));

// ❌ wrong — DOM node in detail
document.dispatchEvent(new CustomEvent('cart:item-added', {
  detail: { element: this._itemEl },  // DOM reference leaks widget internals
}));

// ❌ wrong — function in detail
document.dispatchEvent(new CustomEvent('cart:item-added', {
  detail: { onUndo: () => this._undo() }, // tight coupling
}));
```

### 2.4 Listener cleanup

Custom event listeners on `document` registered inside a widget **must** use `this._ac.signal`. The orchestrator's listeners go in its own `_bind()` and are removed in its own `destroy()`.

```js
// inside CartController._bind()
document.addEventListener('promo:applied', e => {
  this._applyDiscount(e.detail.code, e.detail.discount);
}, { signal: this._ac.signal }); // ← removed when cart.destroy() is called

// inside DashboardPageController._bind()
document.addEventListener('stats:period-changed', e => {
  this._activity.refresh(e.detail.period);
}); // ← removed when dashboardPageController.destroy() is called
```

---

## 3. Init Order and Dependencies

### 3.1 Independent widgets — order does not matter

```js
document.addEventListener('DOMContentLoaded', () => {
  // any order is fine — they share no state
  new HeaderController('.header-container');
  new CartController('.cart-container');
  new SearchController('.search-container');
});
```

### 3.2 Dependent widgets — emitter first, listener second

The widget that emits events should be initialized before the widget that listens, to avoid missed events during boot.

```js
document.addEventListener('DOMContentLoaded', () => {
  // FiltersController emits 'filters:changed'
  // CatalogController listens for 'filters:changed'
  new FiltersController('.filters-container'); // emitter first
  new CatalogController('.catalog-container'); // listener second
});
```

### 3.3 Page orchestrator — widgets inside, wiring after

When using a `PageController`, widgets are instantiated inside its constructor before `_bind()` runs. This guarantees all instances exist before any event wiring.

```js
constructor() {
  // 1. Instantiate all widgets
  this._filters = new FiltersController('.filters-container');
  this._catalog = new CatalogController('.catalog-container');
  this._pagination = new PaginationController('.pagination-container');

  // 2. Wire coordination — all instances guaranteed to exist
  this._bind();
}
```

### 3.4 Conditional init — widget may not be on the page

Every widget's constructor already handles a missing container with a silent return. Init is always safe to call unconditionally:

```js
document.addEventListener('DOMContentLoaded', () => {
  // safe on every page — missing containers are ignored
  new CartController('.cart-container');
  new WishlistController('.wishlist-container');
  new RecentlyViewedController('.recently-viewed-container');
});
```

No `if (document.querySelector('.cart-container'))` guards needed in INIT. The constructor handles it.

---

## 4. Lifecycle Management

### 4.1 Static page — no teardown needed

On pages that are never unmounted (full page navigations), `destroy()` is never called. The browser discards all listeners on unload.

```js
document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container');
  new SummaryController('.summary-container');
  // destroy() never called — full navigation handles cleanup
});
```

### 4.2 SPA navigation — destroy on unmount

When widgets are mounted inside a SPA that swaps content without a full page reload, each mounted widget must be destroyed before the content is replaced.

```js
// mount
const controllers = [
  new OrdersController('.orders-container'),
  new SummaryController('.summary-container'),
];

// unmount — before swapping content
controllers.forEach(c => c.destroy());
```

### 4.3 Tab panels — destroy on hide, recreate on show

Widgets inside tabs stack listeners on every show if not destroyed on hide.

```html
<div class="tab-panel" data-ref="tab-orders"   hidden> <section class="orders-container">  </section> </div>
<div class="tab-panel" data-ref="tab-messages" hidden> <section class="messages-container"></section> </div>
```

```js
class TabsController {

  constructor(selector) {
    this._root = document.querySelector(selector);
    if (!this._root) return;

    this._active = null; // currently mounted widget controller
    this._ac = new AbortController();
    this._bind();
  }

  _bind() {
    this._root.addEventListener('click', e => {
      const tab = e.target.closest('[data-action="switch-tab"]');
      if (!tab) return;
      this._switchTo(tab.dataset.tab);
    }, { signal: this._ac.signal });
  }

  _switchTo(tabName) {
    // destroy previous widget before hiding its panel
    if (this._active) {
      this._active.destroy();
      this._active = null;
    }

    // show selected panel
    this._root.querySelectorAll('[data-ref^="tab-"]').forEach(panel => {
      panel.hidden = panel.dataset.ref !== `tab-${tabName}`;
    });

    // mount fresh widget instance
    this._active = this._mount(tabName);
  }

  _mount(tabName) {
    switch (tabName) {
      case 'orders':   return new OrdersController('.orders-container');
      case 'messages': return new MessagesController('.messages-container');
      default:         return null;
    }
  }

  destroy() {
    if (this._active) this._active.destroy();
    this._ac.abort();
  }
}
```

### 4.4 Page orchestrator lifecycle

`DashboardPageController.destroy()` destroys every widget it owns.

```js
destroy() {
  this._stats.destroy();
  this._activity.destroy();
  this._notifications.destroy();
  // no this._ac.abort() needed if the page controller has no own listeners
  // add this._ac = new AbortController() + this._ac.abort() if it does
}
```

---

## 5. Anti-Patterns

### 5.1 Widget-to-widget direct reference

```js
// ❌ wrong — CartController reaches into SummaryController
class CartController {
  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;

    this._summary = opts.summaryController; // external instance injected
  }

  _handleItemAdded(item) {
    this._summary._updateTotal(item.price); // calling private method of another widget
  }
}

// ✅ correct — CartController emits, SummaryController listens independently
class CartController {
  _handleItemAdded(item) {
    document.dispatchEvent(new CustomEvent('cart:item-added', {
      detail: { price: item.price },
    }));
  }
}
```

### 5.2 Global widget registry

```js
// ❌ wrong — widgets register themselves globally
window.__widgets = window.__widgets || {};
window.__widgets.cart = this; // inside CartController constructor

// later, somewhere else:
window.__widgets.cart._updateBadge(); // uncontrolled external access

// ✅ correct — orchestrator holds references privately
class CheckoutPageController {
  constructor() {
    this._cart    = new CartController('.cart-container');
    this._summary = new SummaryController('.summary-container');
  }
}
```

### 5.3 Logic in INIT

```js
// ❌ wrong — coordination logic leaks into INIT
document.addEventListener('DOMContentLoaded', () => {
  const cart    = new CartController('.cart-container');
  const summary = new SummaryController('.summary-container');

  document.addEventListener('cart:item-added', e => {
    summary._updateTotal(e.detail.price); // logic does not belong here
  });
});

// ✅ correct — logic lives in the orchestrator or inside the listening widget
document.addEventListener('DOMContentLoaded', () => {
  new CheckoutPageController(); // wiring is inside the class
});
```

### 5.4 Querying another widget's DOM from outside

```js
// ❌ wrong — reading DOM that belongs to another widget
const cartBadge = document.querySelector('.cart-container [data-ref="badge"]');
cartBadge.textContent = newCount;

// ✅ correct — emit an event; the widget updates its own DOM
document.dispatchEvent(new CustomEvent('cart:count-changed', {
  detail: { count: newCount },
}));
// CartController listens and updates this._badge.textContent internally
```

### 5.5 Initializing a widget inside another widget's constructor

```js
// ❌ wrong — OrdersController creates a child widget, coupling them tightly
class OrdersController {
  constructor(selector, opts = {}) {
    this._root = document.querySelector(selector);
    if (!this._root) return;

    this._pagination = new PaginationController('.pagination-container'); // wrong
  }
}

// ✅ correct — orchestrator owns both, wires via events
class OrdersPageController {
  constructor() {
    this._orders     = new OrdersController('.orders-container');
    this._pagination = new PaginationController('.pagination-container');
    this._bind();
  }

  _bind() {
    document.addEventListener('pagination:page-changed', e => {
      this._orders.loadPage(e.detail.page);
    });
  }

  destroy() {
    this._orders.destroy();
    this._pagination.destroy();
  }
}
```

---

## 6. Summary: Responsibility Map

```
┌─────────────────────────────────────────────────────────────────┐
│  DOMContentLoaded / PageController                              │
│  ─ instantiates widgets                                         │
│  ─ wires cross-widget events                                    │
│  ─ calls destroy() on unmount                                   │
├─────────────────────────────────────────────────────────────────┤
│  WidgetController (e.g. CartController)                         │
│  ─ owns its container DOM                                       │
│  ─ manages its own state                                        │
│  ─ emits custom events on document                              │
│  ─ listens to events from other widgets via signal              │
│  ─ never references another widget instance                     │
│  ─ never touches another widget's DOM                           │
├─────────────────────────────────────────────────────────────────┤
│  document (custom events)                                       │
│  ─ the only legal channel between widgets                       │
│  ─ payload: plain serializable objects in detail                │
└─────────────────────────────────────────────────────────────────┘
```
