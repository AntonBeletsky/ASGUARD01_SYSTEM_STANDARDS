# No Selector Spaghetti in Vanilla JS
> A complete guide to writing clean, maintainable, modern vanilla JavaScript without turning your codebase into a tangled mess of global selectors, fragile IDs, and event handler chaos.

---

## Table of Contents

1. [What Is Selector Spaghetti?](#1-what-is-selector-spaghetti)
2. [Rule 1 — Separate Style Hooks from Logic Hooks](#2-rule-1--separate-style-hooks-from-logic-hooks)
3. [Rule 2 — Never Query Globally When You Can Query Locally](#3-rule-2--never-query-globally-when-you-can-query-locally)
4. [Rule 3 — Use Event Delegation, Not Per-Element Listeners](#4-rule-3--use-event-delegation-not-per-element-listeners)
5. [Rule 4 — Encapsulate with the Module Pattern](#5-rule-4--encapsulate-with-the-module-pattern)
6. [Rule 5 — Initialize Once, Scope Everything](#6-rule-5--initialize-once-scope-everything)
7. [Rule 6 — Never Scatter DOM Queries Across Functions](#7-rule-6--never-scatter-dom-queries-across-functions)
8. [Rule 7 — Clean Up After Yourself](#8-rule-7--clean-up-after-yourself)
9. [Rule 8 — Data Flow: State First, DOM Second](#9-rule-8--data-flow-state-first-dom-second)
10. [Rule 9 — Dynamic Elements & Lifecycle](#10-rule-9--dynamic-elements--lifecycle)
11. [Rule 10 — Communicating Between Modules Without Coupling](#11-rule-10--communicating-between-modules-without-coupling)
12. [Putting It All Together — Real-World Example](#12-putting-it-all-together--real-world-example)
13. [Cheat Sheet](#13-cheat-sheet)

---

## 1. What Is Selector Spaghetti?

Selector spaghetti is what happens when your JavaScript reaches into the DOM in an uncontrolled, scattered way:

```js
// 🍝 Classic spaghetti
document.getElementById('submit-btn').addEventListener('click', () => {
  const name = document.getElementById('user-name').value;
  const email = document.getElementById('user-email').value;
  document.getElementById('result-msg').textContent = `Hello ${name}`;
  document.getElementById('submit-btn').disabled = true;
});
```

### Why this hurts you

| Symptom | Consequence |
|---|---|
| IDs scattered everywhere | Rename one ID → script silently breaks |
| Global `document.getElementById` | Duplicate a widget → both break |
| Logic mixed with structure | Can't move a component to another page |
| Event listeners on every element | Memory leaks, lost listeners on dynamic content |
| No clear ownership | Nobody knows which script "owns" which element |

---

## 2. Rule 1 — Separate Style Hooks from Logic Hooks

**Never use the same attribute for both CSS and JS.**

```html
<!-- 🍝 Bad: JS and CSS share the same hook -->
<button id="submit-btn" class="btn btn-primary">Submit</button>
```

```html
<!-- ✅ Good: clear separation of concerns -->
<button class="btn btn-primary" data-js="submit-btn">Submit</button>
```

### The convention

- `class` / `id` → **CSS only**. Style whatever you want, rename freely.
- `data-js="..."` → **JS only**. When a dev sees this, they know: "don't remove this, it's wired to a script."

### Selecting by data-js

```js
// Single element
const btn = container.querySelector('[data-js="submit-btn"]');

// Multiple elements
const items = container.querySelectorAll('[data-js="list-item"]');
```

This contract makes refactoring safe. You can redesign the entire CSS without touching JS, and restructure JS without worrying about breaking styles.

---

## 3. Rule 2 — Never Query Globally When You Can Query Locally

`document.getElementById()` and `document.querySelector()` reach into the **entire page**. This is the root cause of conflicts when you have multiple widgets, multiple instances, or a growing codebase.

```js
// 🍝 Bad: global reach
const form = document.querySelector('.checkout-form');
const input = document.getElementById('email');
const btn = document.getElementById('submit');
```

```js
// ✅ Good: find root first, query locally from there
function initCheckout(rootEl) {
  const input = rootEl.querySelector('[data-js="email-input"]');
  const btn   = rootEl.querySelector('[data-js="submit-btn"]');
  const msg   = rootEl.querySelector('[data-js="status-msg"]');

  // everything scoped to rootEl — you can have 10 checkouts on one page
}

// Call for each instance
document.querySelectorAll('[data-js="checkout-form"]').forEach(initCheckout);
```

### Why this scales

- Two instances of the same widget on one page? No conflicts.
- Move the widget to a different page? Copy the HTML block, JS works automatically.
- Unit test? Pass a fake DOM node as `rootEl`.

---

## 4. Rule 3 — Use Event Delegation, Not Per-Element Listeners

Attaching a listener to every button, every card, every item is a classic mistake.

```js
// 🍝 Bad: listener on every item
document.querySelectorAll('[data-js="delete-btn"]').forEach(btn => {
  btn.addEventListener('click', handleDelete);
});
// New items added later? They have no listener. Silent failure.
```

```js
// ✅ Good: one listener on the stable parent
function initList(rootEl) {
  rootEl.addEventListener('click', (e) => {
    const deleteBtn = e.target.closest('[data-js="delete-btn"]');
    if (deleteBtn) handleDelete(deleteBtn);

    const editBtn = e.target.closest('[data-js="edit-btn"]');
    if (editBtn) handleEdit(editBtn);
  });
}
```

### `closest()` is your best friend

`e.target.closest('[data-js="..."]')` walks up the DOM tree from the clicked element and finds the matching ancestor. This means clicks on child elements (icons, spans inside buttons) are handled correctly.

### When NOT to delegate

- Events that don't bubble: `focus`, `blur`, `scroll` (use `focusin`/`focusout` instead, or capture phase)
- Highly performance-critical handlers on very deep trees (rare in practice)

---

## 5. Rule 4 — Encapsulate with the Module Pattern

Each widget/component should be a self-contained unit. The cleanest approach in modern vanilla JS is a factory function.

```js
// wishlist.js

function createWishlist(rootEl) {
  // 1. Query all needed elements once, at init time
  const list       = rootEl.querySelector('[data-js="wishlist-list"]');
  const selectAll  = rootEl.querySelector('[data-js="select-all-btn"]');
  const deleteBtn  = rootEl.querySelector('[data-js="delete-selected-btn"]');
  const counter    = rootEl.querySelector('[data-js="selected-count"]');

  // 2. Private state — nobody outside can touch this
  let selectedIds = new Set();

  // 3. Private functions
  function updateCounter() {
    counter.textContent = selectedIds.size;
  }

  function handleItemToggle(itemEl) {
    const id = itemEl.dataset.itemId;
    if (selectedIds.has(id)) {
      selectedIds.delete(id);
      itemEl.setAttribute('aria-selected', 'false');
    } else {
      selectedIds.add(id);
      itemEl.setAttribute('aria-selected', 'true');
    }
    updateCounter();
  }

  // 4. Delegated event on the list
  list.addEventListener('click', (e) => {
    const item = e.target.closest('[data-js="wishlist-item"]');
    if (item) handleItemToggle(item);
  });

  selectAll.addEventListener('click', () => {
    list.querySelectorAll('[data-js="wishlist-item"]').forEach(item => {
      selectedIds.add(item.dataset.itemId);
      item.setAttribute('aria-selected', 'true');
    });
    updateCounter();
  });

  // 5. Public API — only expose what callers actually need
  return {
    getSelectedIds: () => [...selectedIds],
    clearSelection: () => {
      selectedIds.clear();
      list.querySelectorAll('[data-js="wishlist-item"]')
          .forEach(item => item.setAttribute('aria-selected', 'false'));
      updateCounter();
    }
  };
}

// Entry point
document.querySelectorAll('[data-js="wishlist"]').forEach(el => {
  const wishlist = createWishlist(el);
  // optionally store instance: el._wishlist = wishlist;
});
```

### What you get

- Zero global variables
- All DOM queries happen **once**, at init time (performance win)
- Multiple instances work independently
- `selectedIds` is truly private — no accidental mutation from outside

---

## 6. Rule 5 — Initialize Once, Scope Everything

All DOM queries should live in one place: the **init block** of your module. Never query the DOM inside event handlers or loop bodies.

```js
// 🍝 Bad: querying inside handlers
document.addEventListener('click', (e) => {
  if (e.target.matches('[data-js="toggle"]')) {
    // hitting the DOM every single click
    const menu = document.querySelector('[data-js="dropdown-menu"]');
    menu.classList.toggle('is-open');
  }
});
```

```js
// ✅ Good: query once, reuse the reference
function initDropdown(rootEl) {
  const toggle = rootEl.querySelector('[data-js="toggle"]');
  const menu   = rootEl.querySelector('[data-js="dropdown-menu"]');

  toggle.addEventListener('click', () => {
    menu.classList.toggle('is-open');        // cheap: reference already held
    toggle.setAttribute('aria-expanded',
      menu.classList.contains('is-open'));
  });
}
```

---

## 7. Rule 6 — Never Scatter DOM Queries Across Functions

If your module has 10 functions and each one calls `querySelector`, that's spaghetti at the function level.

```js
// 🍝 Bad: DOM queries all over the place
function showError() {
  document.querySelector('[data-js="error-msg"]').classList.remove('hidden');
}
function hideError() {
  document.querySelector('[data-js="error-msg"]').classList.add('hidden');
}
function getInputValue() {
  return document.querySelector('[data-js="email-input"]').value;
}
```

```js
// ✅ Good: query at the top, pass references down
function initContactForm(rootEl) {
  // All queries in one place — like a manifest of what this module needs
  const els = {
    input:    rootEl.querySelector('[data-js="email-input"]'),
    errorMsg: rootEl.querySelector('[data-js="error-msg"]'),
    submitBtn: rootEl.querySelector('[data-js="submit-btn"]'),
  };

  function showError(msg) {
    els.errorMsg.textContent = msg;
    els.errorMsg.classList.remove('hidden');
  }

  function hideError() {
    els.errorMsg.classList.add('hidden');
  }

  function getInputValue() {
    return els.input.value.trim();
  }

  // ...
}
```

The `els` object acts as a **local DOM registry** — one glance tells you everything the module touches.

---

## 8. Rule 7 — Clean Up After Yourself

Leaked event listeners are a slow-motion memory leak, especially in SPAs or when widgets are destroyed and recreated.

```js
// ✅ Always return a destroy function from your module
function createTooltip(rootEl) {
  const trigger = rootEl.querySelector('[data-js="tooltip-trigger"]');
  const box     = rootEl.querySelector('[data-js="tooltip-box"]');

  function show() { box.classList.add('is-visible'); }
  function hide() { box.classList.remove('is-visible'); }

  trigger.addEventListener('mouseenter', show);
  trigger.addEventListener('mouseleave', hide);
  trigger.addEventListener('focus', show);
  trigger.addEventListener('blur', hide);

  // Return cleanup — caller is responsible for calling this on teardown
  return {
    destroy() {
      trigger.removeEventListener('mouseenter', show);
      trigger.removeEventListener('mouseleave', hide);
      trigger.removeEventListener('focus', show);
      trigger.removeEventListener('blur', hide);
    }
  };
}

// Usage
const tooltip = createTooltip(someEl);

// When the component is removed from the page:
tooltip.destroy();
```

### AbortController — the modern cleanup approach

```js
function initSearch(rootEl) {
  const input = rootEl.querySelector('[data-js="search-input"]');
  const ac = new AbortController();
  const { signal } = ac;

  input.addEventListener('input', handleInput, { signal });
  document.addEventListener('keydown', handleKeydown, { signal });
  window.addEventListener('resize', handleResize, { signal });

  // One call removes ALL listeners registered with this signal
  return { destroy: () => ac.abort() };
}
```

`AbortController` is the cleanest modern pattern — one `abort()` nukes every listener at once, no bookkeeping.

---

## 9. Rule 8 — Data Flow: State First, DOM Second

The DOM is a **view**. Don't use it as your source of truth.

```js
// 🍝 Bad: reading state from the DOM
function getCartTotal() {
  let total = 0;
  document.querySelectorAll('[data-js="cart-item"]').forEach(item => {
    total += parseFloat(item.querySelector('[data-js="item-price"]').textContent);
  });
  return total;
}
```

```js
// ✅ Good: state lives in JS, DOM reflects it
function createCart(rootEl) {
  // Source of truth: a plain JS array
  let items = [];

  function render() {
    const listEl = rootEl.querySelector('[data-js="cart-list"]');
    const totalEl = rootEl.querySelector('[data-js="cart-total"]');

    listEl.innerHTML = items.map(item => `
      <li data-js="cart-item" data-item-id="${item.id}">
        <span>${item.name}</span>
        <span data-js="item-price">${item.price.toFixed(2)}</span>
        <button data-js="remove-btn">×</button>
      </li>
    `).join('');

    totalEl.textContent = items
      .reduce((sum, item) => sum + item.price, 0)
      .toFixed(2);
  }

  function addItem(item) {
    items = [...items, item];  // immutable update
    render();
  }

  function removeItem(id) {
    items = items.filter(item => item.id !== id);
    render();
  }

  // Delegated listener — works for dynamically rendered items too
  rootEl.addEventListener('click', (e) => {
    const removeBtn = e.target.closest('[data-js="remove-btn"]');
    if (removeBtn) {
      const itemEl = removeBtn.closest('[data-js="cart-item"]');
      removeItem(itemEl.dataset.itemId);
    }
  });

  return { addItem, removeItem, getItems: () => [...items] };
}
```

### The rule

- **Write** state → call `render()` → DOM updates
- **Read** state → read from JS variables, never from DOM attributes/text

---

## 10. Rule 9 — Dynamic Elements & Lifecycle

When elements are added/removed from the DOM at runtime, you need a consistent pattern to wire them up without re-scanning the entire document.

### Pattern: init-on-insert

```js
// A generic helper that initializes a module for each matching element
function initAll(selector, factory) {
  document.querySelectorAll(selector).forEach(el => {
    if (el._initialized) return;   // guard against double-init
    el._initialized = true;
    const instance = factory(el);
    el._destroy = instance?.destroy;  // store cleanup if provided
  });
}

// Use MutationObserver to catch elements added later (e.g. from AJAX)
const observer = new MutationObserver(() => {
  initAll('[data-js="wishlist"]', createWishlist);
  initAll('[data-js="dropdown"]', createDropdown);
  initAll('[data-js="tooltip"]', createTooltip);
});

observer.observe(document.body, { childList: true, subtree: true });

// First run on page load
initAll('[data-js="wishlist"]', createWishlist);
initAll('[data-js="dropdown"]', createDropdown);
initAll('[data-js="tooltip"]', createTooltip);
```

### Pattern: destroy-on-remove

```js
const removalObserver = new MutationObserver((mutations) => {
  mutations.forEach(mutation => {
    mutation.removedNodes.forEach(node => {
      if (node.nodeType !== Node.ELEMENT_NODE) return;
      // Clean up the removed node itself
      node._destroy?.();
      // Clean up any descendants
      node.querySelectorAll?.('[data-js]').forEach(el => el._destroy?.());
    });
  });
});

removalObserver.observe(document.body, { childList: true, subtree: true });
```

---

## 11. Rule 10 — Communicating Between Modules Without Coupling

Two modules should **never** import or call each other directly. That creates tight coupling — the exact thing we're trying to avoid.

### Pattern: Custom Events (pub/sub via the DOM)

```js
// cart.js — publishes an event
function createCart(rootEl) {
  function removeItem(id) {
    items = items.filter(item => item.id !== id);
    render();

    // Announce what happened — anyone can listen, cart doesn't care who
    rootEl.dispatchEvent(new CustomEvent('cart:updated', {
      bubbles: true,
      detail: { items: [...items], total: getTotal() }
    }));
  }
}

// order-summary.js — subscribes, no reference to cart module
document.addEventListener('cart:updated', (e) => {
  updateSummaryDisplay(e.detail.items, e.detail.total);
});
```

### Pattern: A simple EventBus

```js
// event-bus.js
const EventBus = {
  _handlers: {},

  on(event, handler) {
    if (!this._handlers[event]) this._handlers[event] = [];
    this._handlers[event].push(handler);
  },

  off(event, handler) {
    this._handlers[event] = (this._handlers[event] || [])
      .filter(h => h !== handler);
  },

  emit(event, data) {
    (this._handlers[event] || []).forEach(h => h(data));
  }
};

export default EventBus;

// In cart.js
import EventBus from './event-bus.js';
EventBus.emit('cart:updated', { items, total });

// In order-summary.js
import EventBus from './event-bus.js';
EventBus.on('cart:updated', ({ items, total }) => {
  updateSummaryDisplay(items, total);
});
```

Both modules depend only on `EventBus`, never on each other.

---

## 12. Putting It All Together — Real-World Example

A filterable product list with search, category filter, and cart integration.

```html
<!-- HTML -->
<section data-js="product-catalog">
  <input type="text" data-js="search-input" placeholder="Search...">

  <div data-js="filter-bar">
    <button data-js="filter-btn" data-category="all" aria-pressed="true">All</button>
    <button data-js="filter-btn" data-category="shoes" aria-pressed="false">Shoes</button>
    <button data-js="filter-btn" data-category="bags" aria-pressed="false">Bags</button>
  </div>

  <div data-js="product-grid"></div>
  <p data-js="empty-state" hidden>No products found.</p>
</section>
```

```js
// product-catalog.js
import EventBus from './event-bus.js';

function createProductCatalog(rootEl, allProducts) {
  // --- Elements (queried once) ---
  const els = {
    searchInput: rootEl.querySelector('[data-js="search-input"]'),
    filterBar:   rootEl.querySelector('[data-js="filter-bar"]'),
    grid:        rootEl.querySelector('[data-js="product-grid"]'),
    emptyState:  rootEl.querySelector('[data-js="empty-state"]'),
  };

  // --- State ---
  let state = {
    query:    '',
    category: 'all',
  };

  // --- Pure filter logic (no DOM) ---
  function filterProducts(products, { query, category }) {
    return products.filter(p => {
      const matchesQuery    = p.name.toLowerCase().includes(query.toLowerCase());
      const matchesCategory = category === 'all' || p.category === category;
      return matchesQuery && matchesCategory;
    });
  }

  // --- Render ---
  function render() {
    const visible = filterProducts(allProducts, state);

    els.grid.innerHTML = visible.map(p => `
      <article data-js="product-card" data-product-id="${p.id}">
        <h3>${p.name}</h3>
        <p>$${p.price.toFixed(2)}</p>
        <button data-js="add-to-cart-btn">Add to cart</button>
      </article>
    `).join('');

    els.emptyState.hidden = visible.length > 0;

    // Update filter button states
    els.filterBar.querySelectorAll('[data-js="filter-btn"]').forEach(btn => {
      btn.setAttribute('aria-pressed', btn.dataset.category === state.category);
    });
  }

  // --- State updaters ---
  function setState(patch) {
    state = { ...state, ...patch };
    render();
  }

  // --- Events ---
  // Search
  els.searchInput.addEventListener('input', (e) => {
    setState({ query: e.target.value });
  });

  // Filter buttons — delegated
  els.filterBar.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-js="filter-btn"]');
    if (btn) setState({ category: btn.dataset.category });
  });

  // Add to cart — delegated on grid
  els.grid.addEventListener('click', (e) => {
    const addBtn = e.target.closest('[data-js="add-to-cart-btn"]');
    if (!addBtn) return;

    const card = addBtn.closest('[data-js="product-card"]');
    const product = allProducts.find(p => p.id === card.dataset.productId);

    if (product) {
      EventBus.emit('cart:add', product);  // talk to cart without coupling
    }
  });

  // --- Init ---
  render();

  // --- Cleanup ---
  const ac = new AbortController();
  // (attach listeners with { signal: ac.signal } for full cleanup support)

  return {
    destroy: () => ac.abort()
  };
}

// Bootstrap
const catalogEl = document.querySelector('[data-js="product-catalog"]');
if (catalogEl) {
  createProductCatalog(catalogEl, window.PRODUCTS_DATA);
}
```

---

## 13. Cheat Sheet

### ✅ DO

```
data-js="..."          → hook for JS, never touched by CSS
container.querySelector → always scope to a root element
e.target.closest(...)  → safe delegation that handles nested clicks
AbortController        → clean up all listeners in one shot
state → render()       → DOM is always derived from JS state
CustomEvent / EventBus → loose coupling between modules
factory function       → one function = one encapsulated component
els = { ... }          → gather all DOM refs in one place at init
```

### ❌ DON'T

```
document.getElementById(...)          → global reach, breaks on duplicates
querySelector inside event handlers   → repeated DOM hits, performance waste
listener on every list item           → breaks for dynamic content
reading state from DOM attributes     → DOM is not a database
importing one module directly into another → tight coupling
no cleanup / no destroy()             → memory leaks in long-running pages
mixing CSS classes with JS logic      → rename CSS = break JS
```

### Quick decision table

| Question | Answer |
|---|---|
| Where do I query the DOM? | Once, at init, into an `els` object |
| How do I handle list items? | Delegate to the stable parent container |
| Where does my state live? | JS variables inside the factory function |
| How do two modules talk? | CustomEvent or EventBus — never direct import |
| How do I mark a JS hook? | `data-js="..."` attribute |
| How do I scope a module? | Pass `rootEl`, query everything from it |
| How do I clean up? | `AbortController.abort()` or `removeEventListener` |

---

*Keep your selectors close, your state in JS, and your modules ignorant of each other. That's it.*
