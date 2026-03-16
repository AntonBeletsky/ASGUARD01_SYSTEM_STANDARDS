# Clean Code: HTML, CSS & JavaScript
> A practical guide. No fluff, no academic theory — just rules, anti-patterns, and working examples.

---

## Table of Contents

1. [Why Clean Code Is Survival, Not Aesthetics](#1-why-clean-code-is-survival-not-aesthetics)
2. [HTML — Structure and Meaning](#2-html--structure-and-meaning)
3. [CSS — Order and Encapsulation](#3-css--order-and-encapsulation)
4. [JavaScript — Logic Without Chaos](#4-javascript--logic-without-chaos)
5. [How HTML + CSS + JS Work Together](#5-how-html--css--js-work-together)
6. [Universal Clean Code Rules](#6-universal-clean-code-rules)
7. [Red Flags — Refactor These Now](#7-red-flags--refactor-these-now)
8. [Pre-Commit Checklist](#8-pre-commit-checklist)

---

## 1. Why Clean Code Is Survival, Not Aesthetics

Dirty code isn't just ugly. It causes real, measurable problems:

| Problem | Symptom |
|---|---|
| Global selectors | Two widgets on one page → both break |
| Styles and logic share the same class | Rename a CSS class → JS silently dies |
| State stored in the DOM | Duplicate an element → duplicate the bugs |
| Per-element event listeners | Add an element dynamically → no reaction |
| 200-line functions | Change one thing → break three others |
| Magic numbers and strings | `if (status === 3)` — what is 3? |

The goal of clean code: **any developer — including you in six months — can understand what's happening without opening the debugger**.

---

## 2. HTML — Structure and Meaning

### Rule 1: HTML describes content and structure, not styles or behavior

HTML answers **what this is**, not how it looks or what it does.

```html
<!-- 🍝 Bad: hardcoded style, zero semantics, inline handler -->
<div style="color: red; font-weight: bold; cursor: pointer;" onclick="doSomething()">
  Click me
</div>

<!-- ✅ Good: structure + semantics, everything else lives outside -->
<button type="button" class="alert-btn" data-js="dismiss-alert">
  Dismiss
</button>
```

### Rule 2: Use semantic tags

Every tag carries meaning. Screen readers, search engines, and your teammates will thank you.

```html
<!-- 🍝 Bad: divs all the way down -->
<div class="header">
  <div class="nav">
    <div class="nav-item">Home</div>
  </div>
</div>
<div class="main-content">
  <div class="article">
    <div class="article-title">Hello</div>
    <div class="article-body">...</div>
  </div>
</div>

<!-- ✅ Good: tags speak for themselves -->
<header>
  <nav>
    <a href="/">Home</a>
  </nav>
</header>
<main>
  <article>
    <h1>Hello</h1>
    <p>...</p>
  </article>
</main>
```

**Semantics cheat sheet:**

| Tag | When to use |
|---|---|
| `<header>` | Page or section header |
| `<nav>` | Navigation links |
| `<main>` | Primary page content (one per page) |
| `<section>` | Thematically distinct block with a heading |
| `<article>` | Self-contained content (post, product card) |
| `<aside>` | Side content related to the main content |
| `<footer>` | Page or section footer |
| `<button>` | An action — always `<button>`, never `<div>` |
| `<a>` | Navigation — always `<a>`, never `<button>` |
| `<figure>` + `<figcaption>` | Image with a caption |

### Rule 3: Attributes — every one earns its place

```html
<!-- 🍝 Bad: missing context, broken accessibility -->
<img src="photo.jpg">
<input type="text">
<button>Submit</button>

<!-- ✅ Good -->
<img src="photo.jpg" alt="Portrait of user John Doe" width="300" height="300">

<input
  type="email"
  id="user-email"
  name="email"
  autocomplete="email"
  required
  aria-label="Email address"
  placeholder="you@example.com"
>

<button type="submit" aria-label="Submit registration form">
  Submit
</button>
```

**Non-negotiable attributes:**
- `alt` on every `<img>` (empty `alt=""` for decorative images)
- `type` on every `<button>` — `button`, `submit`, or `reset`
- `for` on every `<label>`, pointing to its input's `id`
- `lang` on the `<html>` element

### Rule 4: Don't overuse IDs

An ID is a global identifier. There should be exactly **one** on the page. This makes components non-repeatable by definition.

```html
<!-- 🍝 Bad: ID used as both a CSS hook and a JS hook -->
<div id="wishlist-items" class="wishlist">...</div>

<!-- ✅ Good: ID only when you genuinely need one global reference
     (anchor links, ARIA attributes). For JS — use data-js. -->
<div class="wishlist" data-js="wishlist" aria-label="Your wishlist">...</div>
```

### Rule 5: Separate CSS hooks from JS hooks

```html
<!-- 🍝 Bad: one attribute does everything -->
<button class="btn btn-primary delete-btn">Delete</button>
<!-- Rename .delete-btn in CSS → JS breaks silently -->

<!-- ✅ Good: explicit separation of concerns -->
<button class="btn btn-primary" data-js="delete-btn">Delete</button>
<!-- class → CSS only. data-js → JS only. Fully independent. -->
```

---

## 3. CSS — Order and Encapsulation

### Rule 1: One class, one responsibility

```css
/* 🍝 Bad: one class does everything */
.card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  color: red;        /* this is an error state */
  font-size: 11px;   /* this is typography variant */
  opacity: 0.5;      /* this is a disabled state */
}

/* ✅ Good: base class + modifiers */
.card {
  background: white;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.card--error    { color: red; }
.card--small    { font-size: 11px; }
.card--disabled { opacity: 0.5; pointer-events: none; }
```

### Rule 2: CSS variables for everything that repeats

```css
/* 🍝 Bad: magic values scattered everywhere */
.btn        { background: #2563eb; border-radius: 6px; }
.badge      { background: #2563eb; }
.link       { color: #2563eb; }
.input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}

/* ✅ Good: one source of truth for every design token */
:root {
  /* Colors */
  --color-primary:       #2563eb;
  --color-primary-light: rgba(37, 99, 235, 0.15);
  --color-error:         #dc2626;
  --color-success:       #16a34a;
  --color-text:          #111827;
  --color-text-muted:    #6b7280;
  --color-bg:            #ffffff;
  --color-border:        #e5e7eb;

  /* Border radius */
  --radius-sm:  4px;
  --radius-md:  8px;
  --radius-lg:  16px;
  --radius-full: 9999px;

  /* Spacing */
  --space-xs:   4px;
  --space-sm:   8px;
  --space-md:   16px;
  --space-lg:   24px;
  --space-xl:   40px;

  /* Typography */
  --font-size-sm:   13px;
  --font-size-base: 16px;
  --font-size-lg:   20px;
  --font-size-xl:   28px;

  /* Motion */
  --transition-base: 150ms ease;
  --transition-slow: 300ms ease;
}

.btn        { background: var(--color-primary); border-radius: var(--radius-md); }
.badge      { background: var(--color-primary); }
.link       { color: var(--color-primary); }
.input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
```

### Rule 3: Consistent property order within a block

Not random. Read top to bottom: **where is it? → how big? → what's inside? → decorations.**

```css
.component {
  /* 1. Positioning (affects others) */
  position: relative;
  top: 0;
  z-index: 10;

  /* 2. Box model (own size and spacing) */
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 400px;
  padding: var(--space-md);
  margin: 0 auto;

  /* 3. Typography */
  font-size: var(--font-size-base);
  font-weight: 500;
  line-height: 1.5;
  color: var(--color-text);

  /* 4. Visual */
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  /* 5. Behavior */
  cursor: pointer;
  transition: box-shadow var(--transition-base);
  overflow: hidden;
}
```

### Rule 4: Declare all states explicitly, and keep them together

```css
/* All states of one component — in one place */
.btn                      { /* base */ }
.btn:hover                { /* hover */ }
.btn:focus-visible        { /* keyboard focus — NOT :focus */ }
.btn:active               { /* press */ }
.btn:disabled,
.btn[aria-disabled="true"] { /* disabled */ }
.btn.is-loading           { /* async in-flight */ }
.btn.is-error             { /* error state */ }
```

### Rule 5: Don't fight specificity — stay flat

```css
/* 🍝 Bad: specificity wars */
div.container > ul > li.item .title { color: red; }
#main .sidebar .widget h2.title     { color: blue !important; }

/* ✅ Good: flat specificity, max one level of nesting */
.card-title        { color: var(--color-text); }
.card-title--error { color: var(--color-error); }

/* !important is allowed only in utility classes, nowhere else */
.visually-hidden {
  position: absolute !important;
  width: 1px !important;
  clip: rect(0 0 0 0) !important;
  overflow: hidden !important;
}
```

### Rule 6: Mobile-first media queries

```css
/* 🍝 Bad: desktop-first — you override everything on mobile */
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; gap: 12px; }
}

/* ✅ Good: mobile-first — you only add what's needed at larger sizes */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-sm);
}
@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-lg);
  }
}
```

---

## 4. JavaScript — Logic Without Chaos

### Rule 1: Functions do one thing

A function's name should completely describe what it does. If you need the word "and" — that's two functions.

```js
// 🍝 Bad: one function does everything
function handleSubmit() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  if (!name || !email) {
    document.getElementById('error').textContent = 'Fill all fields';
    document.getElementById('error').style.display = 'block';
    return;
  }
  fetch('/api/submit', { method: 'POST', body: JSON.stringify({ name, email }) })
    .then(r => r.json())
    .then(data => {
      document.getElementById('form').style.display = 'none';
      document.getElementById('success').style.display = 'block';
      document.getElementById('success').textContent = `Welcome, ${data.name}!`;
    });
}

// ✅ Good: each function has one job
function getFormData(els) {
  return {
    name:  els.nameInput.value.trim(),
    email: els.emailInput.value.trim(),
  };
}

function validateFormData({ name, email }) {
  if (!name)                    return 'Name is required';
  if (!email)                   return 'Email is required';
  if (!email.includes('@'))     return 'Email is invalid';
  return null; // null = valid
}

function showError(els, message) {
  els.errorMsg.textContent = message;
  els.errorMsg.hidden = false;
}

function showSuccess(els, userName) {
  els.form.hidden = true;
  els.successMsg.textContent = `Welcome, ${userName}!`;
  els.successMsg.hidden = false;
}

async function submitFormData(data) {
  const response = await fetch('/api/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function handleSubmit(els) {
  const data  = getFormData(els);
  const error = validateFormData(data);
  if (error) { showError(els, error); return; }

  try {
    const result = await submitFormData(data);
    showSuccess(els, result.name);
  } catch (err) {
    showError(els, 'Something went wrong. Please try again.');
    console.error('[handleSubmit] failed:', err);
  }
}
```

### Rule 2: Naming is documentation

```js
// 🍝 Bad: cryptic names
const d   = new Date();
const u   = getUser();
const arr = users.filter(x => x.a === true);
function proc(i) { ... }
let flag = false;

// ✅ Good: name = intent
const createdAt   = new Date();
const currentUser = getUser();
const activeUsers = users.filter(user => user.isActive);
function processPayment(invoice) { ... }
let isMenuOpen = false;

// Booleans — always is/has/can/should
let isLoading   = false;
let hasErrors   = false;
let canSubmit   = true;
let shouldRetry = false;

// Arrays — always plural
const users   = [];
const prices  = [];
const options = [];

// Functions — verb + noun
function fetchUserProfile(userId) { ... }
function updateCartTotal(items) { ... }
function validateEmailFormat(email) { ... }
function renderProductCard(product) { ... }
```

### Rule 3: No magic values

```js
// 🍝 Bad: what is 3? what is 'A'?
if (user.role === 3) { ... }
if (order.status === 'A') { ... }
setTimeout(cleanup, 5000);

// ✅ Good: named constants
const USER_ROLES = {
  GUEST: 1,
  USER:  2,
  ADMIN: 3,
};

const ORDER_STATUS = {
  PENDING:   'P',
  ACTIVE:    'A',
  COMPLETED: 'C',
  CANCELLED: 'X',
};

const CLEANUP_DELAY_MS = 5_000;

if (user.role === USER_ROLES.ADMIN) { ... }
if (order.status === ORDER_STATUS.ACTIVE) { ... }
setTimeout(cleanup, CLEANUP_DELAY_MS);
```

### Rule 4: Early return instead of nested ifs

```js
// 🍝 Bad: pyramid of doom
function processOrder(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.user) {
        if (order.user.isVerified) {
          // real logic is buried 4 levels deep
          submitOrder(order);
        } else {
          showError('User not verified');
        }
      } else {
        showError('No user attached');
      }
    } else {
      showError('Cart is empty');
    }
  } else {
    showError('No order');
  }
}

// ✅ Good: guard clauses — exit early on errors
function processOrder(order) {
  if (!order)                   return showError('No order');
  if (order.items.length === 0) return showError('Cart is empty');
  if (!order.user)              return showError('No user attached');
  if (!order.user.isVerified)   return showError('User not verified');

  // real logic — no longer buried
  submitOrder(order);
}
```

### Rule 5: Handle errors everywhere something can fail

```js
// 🍝 Bad: fetch with no error handling
async function loadProducts() {
  const data = await fetch('/api/products').then(r => r.json());
  renderProducts(data);
}

// ✅ Good
async function loadProducts(els) {
  els.spinner.hidden = false;
  els.errorMsg.hidden = true;

  try {
    const response = await fetch('/api/products');

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const products = await response.json();

    if (!Array.isArray(products)) {
      throw new TypeError('Expected an array of products');
    }

    renderProducts(els, products);

  } catch (err) {
    // User sees: a clear, friendly message
    els.errorMsg.textContent = 'Failed to load products. Please refresh.';
    els.errorMsg.hidden = false;

    // Dev sees: full context for debugging
    console.error('[loadProducts] failed:', err);

  } finally {
    els.spinner.hidden = true;
  }
}
```

### Rule 6: Immutable data updates

```js
// 🍝 Bad: mutating data directly
function addToCart(cart, product) {
  cart.items.push(product);        // mutates the array
  cart.total += product.price;     // mutates the object
  return cart;                     // returns the same reference
}

function removeFromCart(cart, productId) {
  const index = cart.items.findIndex(i => i.id === productId);
  cart.items.splice(index, 1);     // mutation
}

// ✅ Good: always return a new object
function addToCart(cart, product) {
  return {
    ...cart,
    items: [...cart.items, product],
    total: cart.total + product.price,
  };
}

function removeFromCart(cart, productId) {
  const newItems = cart.items.filter(item => item.id !== productId);
  return {
    ...cart,
    items: newItems,
    total: newItems.reduce((sum, item) => sum + item.price, 0),
  };
}

// Usage
let cart = { items: [], total: 0 };
cart = addToCart(cart, { id: '1', name: 'Shoes', price: 99 });
cart = removeFromCart(cart, '1');
```

---

## 5. How HTML + CSS + JS Work Together

This is the most important section. Most "spaghetti" is born exactly here.

### Three layers, three responsibilities

```
HTML  →  Structure and semantics. What it is and what it's made of.
CSS   →  Appearance. How it looks in every state.
JS    →  Behavior. What happens when the user does something.
```

Each layer mutates the DOM in its own specific way:

```
HTML              — sets the initial structure
CSS classes       — control visual state (is-open, has-error, is-loading)
data-* attributes — hooks for JS (data-js, data-action, data-id)
JS                — adds/removes CSS state classes, reads data attributes
```

### Pattern: CSS controls visibility, JS controls classes

```css
/* CSS defines all states */
.dropdown__menu           { display: none; }
.dropdown__menu.is-open   { display: block; }

.form__error              { display: none; }
.form__error.is-visible   { display: block; color: var(--color-error); }

.btn.is-loading           { pointer-events: none; opacity: 0.7; }
.btn.is-loading::after    { content: '...'; }
```

```js
// JS only toggles classes — never writes to style directly
function toggleDropdown(els) {
  const isOpen = els.menu.classList.toggle('is-open');
  els.toggle.setAttribute('aria-expanded', isOpen);
}

function showFieldError(fieldEl, message) {
  const errorEl = fieldEl
    .closest('.form__field')
    .querySelector('[data-js="field-error"]');
  errorEl.textContent = message;
  errorEl.classList.add('is-visible');
  fieldEl.setAttribute('aria-invalid', 'true');
}

function setButtonLoading(btnEl, isLoading) {
  btnEl.classList.toggle('is-loading', isLoading);
  btnEl.disabled = isLoading;
}
```

**The rule:** JS never writes `element.style.display = 'none'`. It only adds or removes classes.

### Pattern: state in JS, render in one place

```js
// ✅ The single function that ever writes to the DOM
function render(state, els) {
  els.list.innerHTML = state.items.map(item => `
    <li class="wishlist__item"
        data-js="wishlist-item"
        data-item-id="${item.id}">
      <span class="wishlist__item-name">${escapeHtml(item.name)}</span>
      <button class="btn btn--icon" data-js="remove-btn"
              aria-label="Remove ${escapeHtml(item.name)}">×</button>
    </li>
  `).join('');

  els.emptyMsg.hidden     = state.items.length > 0;
  els.counter.textContent = state.items.length;
  els.counter.hidden      = state.items.length === 0;
}

// Any change: update state → call render()
function removeItem(state, id) {
  return { ...state, items: state.items.filter(item => item.id !== id) };
}
```

### Pattern: full component encapsulation

```js
function createWishlist(rootEl) {
  // 1. All DOM queries — once, in one place
  const els = {
    list:      rootEl.querySelector('[data-js="wishlist-list"]'),
    emptyMsg:  rootEl.querySelector('[data-js="empty-msg"]'),
    counter:   rootEl.querySelector('[data-js="counter"]'),
    selectAll: rootEl.querySelector('[data-js="select-all-btn"]'),
  };

  // 2. State lives in JS, not in the DOM
  let state = {
    items:    [],
    selected: new Set(),
  };

  // 3. render() is the only function that writes to the DOM
  function render() {
    els.list.innerHTML = state.items.map(item => `
      <li data-js="wishlist-item"
          data-item-id="${item.id}"
          aria-selected="${state.selected.has(item.id)}">
        <span>${escapeHtml(item.name)}</span>
        <button data-js="remove-btn">Remove</button>
      </li>
    `).join('');

    els.emptyMsg.hidden     = state.items.length > 0;
    els.counter.textContent = state.items.length;
  }

  // 4. Delegated events — one listener handles everything
  els.list.addEventListener('click', (e) => {
    const removeBtn = e.target.closest('[data-js="remove-btn"]');
    if (removeBtn) {
      const itemEl = removeBtn.closest('[data-js="wishlist-item"]');
      setState({ items: state.items.filter(i => i.id !== itemEl.dataset.itemId) });
      return;
    }

    const itemEl = e.target.closest('[data-js="wishlist-item"]');
    if (itemEl) toggleSelected(itemEl.dataset.itemId);
  });

  els.selectAll?.addEventListener('click', () => {
    setState({ selected: new Set(state.items.map(i => i.id)) });
  });

  // 5. State always updated through one function
  function setState(patch) {
    state = { ...state, ...patch };
    render();
  }

  function toggleSelected(id) {
    const next = new Set(state.selected);
    next.has(id) ? next.delete(id) : next.add(id);
    setState({ selected: next });
  }

  // 6. Public API — only expose what callers actually need
  return {
    setItems:       (items) => setState({ items }),
    getSelectedIds: ()      => [...state.selected],
    clearSelection: ()      => setState({ selected: new Set() }),
  };
}

// Bootstrap — works for any number of instances on the page
document.querySelectorAll('[data-js="wishlist"]').forEach(el => {
  el._wishlist = createWishlist(el);
});
```

---

## 6. Universal Clean Code Rules

### DRY — Don't Repeat Yourself

```js
// 🍝 Bad: same logic copy-pasted three times
saveBtn.addEventListener('click', async () => {
  saveBtn.disabled = true;
  saveBtn.textContent = 'Saving...';
  await saveData();
  saveBtn.disabled = false;
  saveBtn.textContent = 'Save';
});

publishBtn.addEventListener('click', async () => {
  publishBtn.disabled = true;
  publishBtn.textContent = 'Publishing...';
  await publishData();
  publishBtn.disabled = false;
  publishBtn.textContent = 'Publish';
});

// ✅ Good: shared pattern extracted into a function
async function withLoadingState(btnEl, loadingText, action) {
  const originalText = btnEl.textContent;
  btnEl.disabled     = true;
  btnEl.textContent  = loadingText;

  try {
    await action();
  } finally {
    btnEl.disabled    = false;
    btnEl.textContent = originalText;
  }
}

saveBtn.addEventListener('click', () =>
  withLoadingState(saveBtn, 'Saving...', saveData)
);
publishBtn.addEventListener('click', () =>
  withLoadingState(publishBtn, 'Publishing...', publishData)
);
```

### YAGNI — You Aren't Gonna Need It

Don't write code "for the future". Write code for the task in front of you right now.

```js
// 🍝 Bad: an abstraction nobody asked for
class UniversalDataFetcherWithRetryAndCachingAndTransformationPipeline {
  constructor(options = {}) { ... }
  setTransformer(fn) { ... }
  setCacheTTL(ms) { ... }
  // 200 lines of code, used in exactly one place
}

// ✅ Good: solve the problem that exists today
async function fetchProducts() {
  const response = await fetch('/api/products');
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}
// Add complexity when a real need appears
```

### KISS — Keep It Simple, Stupid

```js
// 🍝 Bad: needlessly clever one-liner
const getDiscount = (price, type, code, isHoliday, years) =>
  ((code ? PROMOS[code] ?? 0 : 0) +
  (type === 'premium' ? (years > 2 ? 0.15 : 0.10) : 0) +
  (isHoliday ? 0.05 : 0)) * price;

// ✅ Good: explicit, readable, debuggable
function getDiscount(price, { userType, promoCode, isHoliday, memberYears }) {
  let discount = 0;

  if (promoCode && PROMOS[promoCode]) {
    discount += PROMOS[promoCode];
  }

  if (userType === 'premium') {
    discount += memberYears > 2 ? 0.15 : 0.10;
  }

  if (isHoliday) {
    discount += 0.05;
  }

  return price * discount;
}
```

### Comments — explain *why*, not *what*

```js
// 🍝 Bad: comment just repeats the code
// Increment counter by 1
counter++;

// Check if price equals zero
if (price === 0) { ... }

// ✅ Good: comment explains non-obvious reasoning
// Safari doesn't support :focus-visible natively before 15.4.
// We add the class manually via JS for cross-browser consistency.
input.addEventListener('focus', () => input.classList.add('js-focus-visible'));

// 100ms delay: without it the popover closes before the trigger's
// click handler fires (browser event order: blur fires before click).
setTimeout(() => closePopover(), 100);
```

---

## 7. Red Flags — Refactor These Now

Search your codebase for these patterns with grep or your editor's global search:

```bash
# Global ID queries
grep -r "getElementById" src/

# Global document queries
grep -r "document\.querySelector" src/

# Direct style writes
grep -r "\.style\." src/

# Inline handlers in HTML
grep -r "onclick=" templates/
grep -r "onchange=" templates/

# innerHTML without escaping (XSS risk)
grep -r "innerHTML" src/

# console.log left in production code
grep -r "console\.log" src/

# Untracked TODOs
grep -r "TODO\|FIXME\|HACK\|XXX" src/
```

| What you found | What to do |
|---|---|
| `document.getElementById` | Wrap in `init(rootEl)`, replace with `rootEl.querySelector('[data-js=...]')` |
| `element.style.display = 'none'` | Replace with `element.hidden = true` or a CSS class |
| `onclick="..."` in HTML | Remove it, wire up `addEventListener` in JS |
| `innerHTML = userInput` | Sanitize with `escapeHtml()` or use `textContent` |
| Function longer than 50 lines | Break it into smaller, named functions |
| Variable named `data`, `item`, `obj`, `temp` | Rename to something that describes its contents |
| Three or more levels of nested `if` | Refactor to guard clauses |

---

## 8. Pre-Commit Checklist

### HTML
- [ ] Semantic tags used correctly and purposefully
- [ ] Every `<img>` has an `alt` attribute
- [ ] Every `<button>` has a `type` attribute
- [ ] Every `<input>` has an associated `<label>` (explicit or `aria-label`)
- [ ] All IDs are unique on the page
- [ ] CSS classes and `data-js` attributes are separate concerns
- [ ] No `onclick`, `onchange`, or `onfocus` attributes in the markup

### CSS
- [ ] Repeating values extracted into CSS variables
- [ ] No magic numbers or hardcoded color hex values
- [ ] `!important` absent (except utility classes)
- [ ] All component states declared: hover, focus, active, disabled, error
- [ ] Specificity stays flat — max 1–2 levels of nesting
- [ ] `focus-visible` used instead of `focus` for keyboard styles

### JavaScript
- [ ] No `document.getElementById` / `document.querySelector` outside `init` functions
- [ ] All DOM queries done once at init time, collected in `els = { ... }`
- [ ] No `element.style.X` writes — only class toggling
- [ ] No state read from the DOM (`textContent`, attributes)
- [ ] State lives in JS variables, not in HTML
- [ ] `render()` is the single function that writes to the DOM
- [ ] Event listeners use delegation on stable parent elements
- [ ] Every `async` / `fetch` call has `try/catch`
- [ ] No magic strings or numbers — named constants only
- [ ] Functions are ≤ 30–40 lines and do one thing
- [ ] No `console.log` in production-bound code

### General
- [ ] Code reads without comments (names make intent clear)
- [ ] Comments explain *why*, not *what*
- [ ] No commented-out dead code
- [ ] No TODO without a linked ticket in the tracker
- [ ] Git diff reviewed — no accidental deletions, no whitespace-only noise

---

*Clean code isn't about beauty. It's about making sure the next person — or you in six months — doesn't spend an hour figuring out what's going on before they can change a single line.*
