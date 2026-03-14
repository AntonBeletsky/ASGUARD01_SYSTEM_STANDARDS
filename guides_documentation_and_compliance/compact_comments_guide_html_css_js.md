# Compact Comments Guide — HTML / CSS / JS
### For Envato Template Marketplace

> **Core rule:** Comments explain *why*, not *what*. Code is self-documenting — comments add context.

---

## PART 1 — HTML COMMENTS

### 1.1 Block Hierarchy (3 levels only)

#### Level 1 — Major page section
One-line banner. Used for: `header`, `footer`, `sidebar`, `modal`, top-level page sections.

```html
<!-- ============================================================ HEADER START -->
<header class="site-header">
    ...
</header>
<!-- ============================================================== HEADER END -->
```

#### Level 2 — Component inside a section
No border lines. Used for named components: nav, search, hero, card grid, etc.

```html
<!-- NAV: Desktop only — offcanvas used on mobile (<992px) -->
<nav class="main-nav d-none d-lg-flex">
    ...
</nav><!-- /main-nav -->
```

#### Level 3 — Inline note
Single line, only when the markup is non-obvious.

```html
<!-- Aria-live: announces cart count to screen readers -->
<span class="cart-count" aria-live="polite">0</span>
```

---

### 1.2 Closing Tag Rule

Add `<!-- /selector -->` for any block that is **longer than ~30 lines** or deeply nested.
Keep it on the same line as the closing tag.

```html
<div class="product-card">
    ...
</div><!-- /product-card -->

<section class="shop-grid">
    ...
</section><!-- /shop-grid -->
```

Do **not** repeat the full banner comment at the end — one `<!-- /selector -->` is enough.

---

### 1.3 Special Flags

Use consistent prefixes. One line per flag.

```html
<!-- TODO: Replace placeholder with real product image -->
<!-- FIXME: Overlap issue on viewport <375px -->
<!-- HACK: Extra wrapper required for Safari flex bug -->
<!-- NOTE: data-bs-dismiss must stay — needed for modal close -->
<!-- WARNING: Do not remove aria-modal, required for a11y -->
```

---

### 1.4 Responsive One-liners

```html
<!-- Grid: lg=3col / md=2col / sm=1col -->
<div class="row">
    <div class="col-lg-4 col-md-6 col-12">...</div>
</div>

<!-- Desktop nav — hidden on mobile, see offcanvas-nav below -->
<nav class="d-none d-lg-block">...</nav>
```

---

### 1.5 What NOT to Comment

```html
<!-- BAD: states the obvious -->
<!-- Navigation -->
<nav>...</nav>

<!-- BAD: mirrors class name -->
<!-- Product card -->
<div class="product-card">...</div>

<!-- GOOD: adds context that isn't visible in the code -->
<!-- Nav: hidden until scroll passes 80px (see main.js → stickyNav) -->
<nav class="sticky-nav hidden">...</nav>
```

---

### 1.6 Disabled / Deprecated Code

```html
<!-- DISABLED: Feature flag off — enable in settings.js
<section class="coming-soon">...</section>
-->

<!-- DEPRECATED: Remove after v2.1 release
<div class="legacy-banner">...</div>
-->
```

---

---

## PART 2 — CSS COMMENTS

### 2.1 File Table of Contents

Place at the very top of every CSS file. Update when adding sections.

```css
/* ============================================================
   TABLE OF CONTENTS
   1. Variables & Reset
   2. Typography
   3. Layout & Grid
   4. Header
   5. Navigation
   6. Hero
   7. Product Cards
   8. Sidebar
   9. Footer
   10. Utilities
   11. Responsive
   ============================================================ */
```

---

### 2.2 Section Dividers

One divider style for major sections (matches TOC entries).

```css
/* ============================================================
   4. HEADER
   ============================================================ */

.site-header { ... }
```

For subsections within a section — a shorter divider:

```css
/* --- Header: Sticky behavior --- */

.site-header.sticky { ... }
```

---

### 2.3 CSS Variables Block

Document each token. Group logically.

```css
/* ============================================================
   1. VARIABLES & RESET
   ============================================================ */

:root {
    /* Brand */
    --color-primary:   #0d6efd;   /* Main accent */
    --color-secondary: #6c757d;   /* Muted text, borders */

    /* Typography */
    --font-base:  'Inter', sans-serif;
    --font-size:  16px;
    --line-height: 1.6;

    /* Layout */
    --container-max: 1200px;
    --gap:           1.5rem;

    /* Z-index scale */
    --z-dropdown: 100;
    --z-sticky:   200;
    --z-modal:    300;
    --z-toast:    400;
}
```

---

### 2.4 Magic Numbers

Always explain bare numbers — a future dev will thank you.

```css
/* 80px = header height; keeps content below sticky bar */
.page-content {
    padding-top: 80px;
}

/* 999 = above Bootstrap modals (z-index 1050 is for BS, this layer is below) */
.custom-overlay {
    z-index: 999;
}

/* 0.98 = subtle press feedback without layout shift */
.btn:active {
    transform: scale(0.98);
}
```

---

### 2.5 Browser Hacks

```css
/* HACK: IE11 — flex gap not supported, using margin fallback */
.card-grid > * {
    margin-right: 1rem;
}

/* HACK: Safari — min-height on flex column requires explicit height */
.sidebar {
    height: 1px; /* triggers correct flex behavior in Safari */
    min-height: 100vh;
}
```

---

### 2.6 Keyframes & Animations

```css
/* Fade-in slide: used on modal and toast entry */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* PERFORMANCE: transform+opacity only — avoids layout/paint reflow */
.modal-enter {
    animation: fadeSlideUp 0.25s ease forwards;
}
```

---

### 2.7 Media Query Labels

```css
/* Responsive: tablet → mobile (<768px) */
@media (max-width: 767px) {
    .main-nav { display: none; }        /* replaced by offcanvas */
    .hero-title { font-size: 1.75rem; } /* scale down from 2.5rem desktop */
}

/* Responsive: large desktop (>1400px) */
@media (min-width: 1400px) {
    .container { max-width: 1320px; }
}
```

---

### 2.8 What NOT to Comment

```css
/* BAD: restates property */
color: red; /* sets color to red */

/* BAD: obvious selector */
/* Button styles */
.btn { ... }

/* GOOD: explains the constraint */
/* Keeps button text on one line — design requires no wrapping in nav */
.nav .btn {
    white-space: nowrap;
}
```

---

---

## PART 3 — JAVASCRIPT COMMENTS

### 3.1 File / Module Header

Use at the top of every JS file.

```js
/**
 * cart.js — Shopping cart logic
 *
 * Handles: add/remove items, quantity update, local storage sync,
 *          and cart count badge in the header.
 *
 * Depends on: utils.js (formatPrice), main.js (showToast)
 */
```

---

### 3.2 Section Dividers

```js
/* ============================================================
   CART STATE
   ============================================================ */

/* --- Helpers --- */

/* --- DOM Bindings --- */
```

---

### 3.3 JSDoc for Functions

Write JSDoc for every exported or public function. Keep descriptions one line if possible.

```js
/**
 * Add a product to the cart.
 * @param {string} id        - Product ID
 * @param {number} qty       - Quantity to add (default: 1)
 * @param {Object} [options] - { silent: bool } — skip toast notification
 * @returns {Object} Updated cart state
 */
function addToCart(id, qty = 1, options = {}) {
    ...
}
```

For private/internal helpers — a single-line comment is enough:

```js
// Recalculate total price from current cart array
function calcTotal(cart) { ... }
```

---

### 3.4 Inline Logic Comments

Only comment what the code cannot express by itself.

```js
// Debounce: prevents API call on every keystroke, fires after 350ms idle
const onSearch = debounce(fetchResults, 350);

// Fallback: IntersectionObserver not supported in older Safari — load all
if (!('IntersectionObserver' in window)) {
    loadAllImages();
    return;
}

// Bitwise right shift — faster integer floor for hot render loop
const mid = (lo + hi) >> 1;
```

---

### 3.5 Special Flags

Same prefix convention as HTML.

```js
// TODO: Replace localStorage with IndexedDB for large carts
// FIXME: Race condition when user clicks Add twice rapidly
// HACK: Timeout needed — Bootstrap modal transition fires before DOM settles
// NOTE: formatPrice expects cents, not dollars (100 = $1.00)
// WARNING: Do not mutate cartState directly — use setCart() to trigger re-render
// PERF: Avoid calling this inside scroll event — use requestAnimationFrame
```

---

### 3.6 Event Listener Blocks

```js
/* --- Event Bindings --- */

document.querySelector('.add-to-cart').addEventListener('click', addToCart);
document.querySelector('.remove-item').addEventListener('click', removeItem);
// Delegated: handles dynamically added wishlist buttons
document.querySelector('.product-grid').addEventListener('click', onWishlistToggle);
```

---

### 3.7 Config / Constants Block

```js
/* ============================================================
   CONFIG
   ============================================================ */

const CONFIG = {
    API_BASE:    '/api/v1',
    TIMEOUT:     8000,      // ms — abort request if exceeded
    PAGE_SIZE:   20,        // products per page
    STORAGE_KEY: 'ec_cart', // localStorage prefix
};
```

---

### 3.8 What NOT to Comment

```js
// BAD: narrates the code
let i = 0; // initialize counter
i++;       // increment

// BAD: restates function name
// Get user
function getUser() { ... }

// GOOD: explains the why
// Start at 1 — skip the sticky header row when iterating table rows
for (let i = 1; i < rows.length; i++) { ... }
```

---

---

## Quick Reference Card

| Situation | HTML | CSS | JS |
|---|---|---|---|
| Major section open | `<!-- === NAME START -->` | `/* === N. NAME === */` | `/* === NAME === */` |
| Major section close | `<!-- === NAME END -->` | *(no closer needed)* | *(no closer needed)* |
| Closing tag hint | `</div><!-- /class -->` | — | — |
| Subsection | `<!-- Name: note -->` | `/* --- name --- */` | `/* --- name --- */` |
| Inline note | `<!-- short why -->` | `/* why */` | `// why` |
| Public function | — | — | `/** JSDoc */` |
| Private helper | — | — | `// one-liner` |
| Flags | `<!-- TODO/FIXME/HACK/NOTE/WARNING -->` | `/* HACK/NOTE */` | `// TODO/FIXME/HACK/NOTE/WARNING/PERF` |
| Magic number | — | `/* N = reason */` | `// reason` |
| Disabled code | `<!-- DISABLED: reason ... -->` | `/* DISABLED: ... */` | `// DISABLED: ...` |

---

> **Envato reviewer tip:** Well-structured section comments in HTML are the first thing reviewers scan.
> Level 1 banners + closing `<!-- /selector -->` tags make template structure immediately readable.
> In CSS, a TOC + variable docs alone will push documentation score above average.
