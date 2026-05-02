# HTML + CSS Naming Conventions — The Complete Guide

> Covers W3C standards, SMACSS, OOCSS, ITCSS, Atomic CSS, Tailwind, CSS Modules, and modern HTML5/CSS3 best practices.
> **BEM (`block__element--modifier`) is explicitly FORBIDDEN in this guide. See §10 and §25.**

---

## Table of Contents

1. [General Principles](#1-general-principles)
2. [HTML — Elements & Structure](#2-html--elements--structure)
3. [HTML — IDs](#3-html--ids)
4. [HTML — Class Names](#4-html--class-names)
5. [HTML — Data Attributes](#5-html--data-attributes)
6. [HTML — ARIA Attributes](#6-html--aria-attributes)
7. [HTML — Custom Elements (Web Components)](#7-html--custom-elements-web-components)
8. [CSS — Selectors](#8-css--selectors)
9. [CSS — Custom Properties (Variables)](#9-css--custom-properties-variables)
10. [Flat Container-Scoped Naming (replaces BEM)](#10-flat-container-scoped-naming-replaces-bem)
11. [SMACSS Methodology](#11-smacss-methodology)
12. [OOCSS Methodology](#12-oocss-methodology)
13. [ITCSS Architecture](#13-itcss-architecture)
14. [Utility / Atomic CSS](#14-utility--atomic-css)
15. [CSS Modules](#15-css-modules)
16. [SCSS / Sass Conventions](#16-scss--sass-conventions)
17. [CSS — Keyframes & Animations](#17-css--keyframes--animations)
18. [CSS — Media Queries & Breakpoints](#18-css--media-queries--breakpoints)
19. [CSS — Z-index Scale](#19-css--z-index-scale)
20. [CSS — Color Naming](#20-css--color-naming)
21. [CSS — Spacing & Sizing Scales](#21-css--spacing--sizing-scales)
22. [CSS — Typography Scale](#22-css--typography-scale)
23. [File & Directory Structure](#23-file--directory-structure)
24. [HTML — Forms](#24-html--forms)
25. [Naming Anti-patterns](#25-naming-anti-patterns)
26. [Quick Reference Cheatsheet](#26-quick-reference-cheatsheet)
27. [References & Further Reading](#27-references--further-reading)

---

## 1. General Principles

- **Use lowercase everywhere** — HTML attributes, class names, IDs, CSS properties, custom properties.
- **Use hyphens as separators** — `user-profile`, not `userProfile` or `user_profile`. No double underscores (`__`), no double hyphens (`--`) as structural separators.
- **Be descriptive, not presentational** — `btn-primary` over `btn-blue`, `alert-error` over `alert-red`.
- **Separate structure from style from behavior** — HTML = content, CSS = presentation, JS = behavior. Never mix.
- **Avoid ID selectors in CSS** — IDs are for JavaScript anchors, ARIA references, and fragment links only. Never for styling.
- **Mobile-first** — write base styles for mobile, override with `min-width` media queries.
- **Flat, container-scoped naming** — scope child selectors via CSS descendant rules from the container class. No BEM-style `__` nesting in class names.
- **States via `data-state`** — JS-driven visual state is expressed through `data-state` attributes consumed by CSS attribute selectors. Not via modifier classes.
- **Semantic HTML first** — use the right element before adding classes: `<nav>`, `<article>`, `<button>`, `<header>`.
- **No inline styles** — except dynamic values set via `el.style.setProperty()` for CSS custom properties only.

---

## 2. HTML — Elements & Structure

### Use semantic elements

```html
<!-- ✅ Good — semantic structure -->
<header>
    <nav aria-label="Main navigation">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
        </ul>
    </nav>
</header>

<main>
    <article>
        <header>
            <h1>Article Title</h1>
            <time datetime="2025-01-15">January 15, 2025</time>
        </header>
        <section>
            <h2>Section Heading</h2>
            <p>Content paragraph.</p>
        </section>
        <footer>
            <address>Author name</address>
        </footer>
    </article>

    <aside>
        <h2>Related articles</h2>
    </aside>
</main>

<footer>
    <p>&copy; 2025 Company Name</p>
</footer>


<!-- ❌ Bad — div soup -->
<div class="header">
    <div class="nav">
        <div class="nav-item"><a href="/">Home</a></div>
    </div>
</div>
<div class="content">
    <div class="article">
        <div class="title">Article Title</div>
    </div>
</div>
```

### Element attribute ordering — be consistent

```html
<!-- ✅ Recommended attribute order -->
<input
    class="form-input"
    id="email"
    type="email"
    name="email"
    value=""
    placeholder="Enter your email"
    autocomplete="email"
    required
    aria-required="true"
    aria-describedby="email-error"
/>

<!-- Order: class → id → type → name → value → other → aria → data -->
```

### Boolean attributes — no value needed

```html
<!-- ✅ Good -->
<input type="checkbox" checked>
<input type="text" disabled>
<button type="submit" disabled>Submit</button>
<details open>...</details>
<video autoplay muted loop>...</video>

<!-- ❌ Redundant -->
<input type="checkbox" checked="checked">
<input type="text" disabled="disabled">
```

---

## 3. HTML — IDs

Use **kebab-case**. IDs must be **unique per page**. Use for:
- ARIA references (`aria-labelledby`, `aria-describedby`)
- Form label associations (`for` / `id`)
- Fragment links (`#section`)
- Anchor points

**IDs are never used as JavaScript hooks.** JS locates elements via `data-ref` and `data-action`.

```html
<!-- ✅ Good — kebab-case, descriptive, semantic purpose -->
<section id="about-us">...</section>
<section id="contact-form">...</section>
<h2 id="pricing-heading">Pricing</h2>
<input id="user-email" type="email">
<label for="user-email">Email address</label>
<div id="modal-confirm-delete" role="dialog" aria-labelledby="modal-title">
    <h2 id="modal-title">Confirm deletion</h2>
</div>
<span id="email-error" role="alert">Invalid email format</span>

<!-- ❌ Bad -->
<section id="About_Us">...</section>       <!-- mixed case + underscore -->
<div id="div1">...</div>                   <!-- meaningless -->
<section id="s1">...</section>             <!-- cryptic -->
<div id="emailInputField">...</div>        <!-- camelCase -->
<button id="send-btn">Send</button>        <!-- id used as JS hook — FORBIDDEN -->
```

### Widget component IDs — always carry the widget prefix

When working inside a widget/component, all IDs must carry the widget's full-word prefix to prevent collisions across components on the same page:

```html
<!-- ✅ Pattern: [widget]-[purpose] -->
<div role="dialog" aria-labelledby="orders-modal-title" hidden>
    <h2 id="orders-modal-title">Delete order?</h2>
</div>
<h2 id="orders-section-payments">Payments</h2>

<!-- ❌ Wrong — generic unprefixed IDs collide across widgets -->
<h2 id="modal-title">Delete order?</h2>
<h2 id="section-payments">Payments</h2>
```

### ID naming patterns

| Purpose | Example |
|---------|---------|
| Page sections | `#hero`, `#about`, `#services`, `#contact` |
| Modal dialogs | `#orders-modal-title`, `#newsletters-modal-body` |
| Form elements | `#input-email`, `#input-password`, `#select-country` |
| Form labels & errors | `#label-email`, `#error-email`, `#hint-password` |
| Navigation | `#nav-main`, `#nav-breadcrumb` |
| Skip links | `#main-content`, `#main-nav` |
| ARIA targets | `#[widget]-modal-title`, `#[widget]-section-[name]` |

---

## 4. HTML — Class Names

Use **kebab-case**. Classes are the primary styling hook. Classes are **never** used as JS hooks.

### General rules

```html
<!-- ✅ Good — flat kebab-case, semantic, container-scoped -->
<nav class="nav nav-primary">
    <ul class="nav-list">
        <li class="nav-item" data-state="active">
            <a class="nav-link" href="/">Home</a>
        </li>
    </ul>
</nav>

<div class="card card-featured">
    <img class="card-image" src="..." alt="...">
    <div class="card-body">
        <h2 class="card-title">Title</h2>
        <p class="card-description">Description text.</p>
    </div>
    <div class="card-footer">
        <button class="btn btn-primary">Read more</button>
    </div>
</div>

<!-- ❌ Bad -->
<div class="Card">...</div>              <!-- PascalCase -->
<div class="cardItem">...</div>          <!-- camelCase -->
<div class="card__body">...</div>        <!-- BEM double underscore — FORBIDDEN -->
<div class="card--featured">...</div>   <!-- BEM double hyphen — FORBIDDEN -->
<div class="red-box big">...</div>       <!-- presentational, vague -->
<div class="div1">...</div>              <!-- meaningless -->
<div class="js-send-btn">...</div>       <!-- class used as JS hook — FORBIDDEN -->
```

### Semantic class naming

```html
<!-- ✅ Component classes — noun -->
<div class="card">
<nav class="breadcrumb">
<form class="contact-form">
<aside class="sidebar">
<section class="hero">
<footer class="site-footer">
<header class="site-header">
<ul class="tag-list">
<div class="modal">
<div class="tooltip">
<div class="dropdown">
<div class="pagination">
<div class="avatar">
<div class="badge">
<div class="chip">
<div class="toast">
<div class="spinner">
<div class="skeleton">
<table class="data-table">

<!-- ✅ State — use data-state attribute, not modifier classes -->
<li data-state="active">
<div data-state="open">
<button data-state="loading">
<input data-state="invalid">
<div data-state="hidden">
<li data-state="selected">
<div data-state="expanded">

<!-- ✅ Modifier classes for variants — single hyphen, descriptive adjective -->
<button class="btn btn-primary">
<button class="btn btn-large">
<button class="btn btn-outline">
<div class="alert alert-error">
<div class="alert alert-success">
<div class="card card-horizontal">
<div class="card card-featured">
```

---

## 5. HTML — Data Attributes

Use **`data-kebab-case`**. Data attributes serve two purposes:

1. **JS hooks** — `data-ref`, `data-action`, `data-id`, `data-state` (see Law Zero)
2. **Configuration** — passing component config from HTML to JS

```html
<!-- ✅ Good — data-{component}-{property} pattern for config -->
<div
    class="carousel"
    data-carousel-autoplay="true"
    data-carousel-interval="5000"
    data-carousel-slides-per-view="3"
>
    <div class="carousel-slide" data-slide-index="0">...</div>
    <div class="carousel-slide" data-slide-index="1">...</div>
</div>

<!-- ✅ JS hooks — data-ref / data-action / data-id / data-state -->
<button
    class="btn btn-danger"
    data-action="delete"
    data-id="42"
    data-item-type="user"
>
    Delete
</button>

<div class="messages-list" data-ref="messages-list"></div>
<li class="orders-item" data-id="order-42" data-state="active"></li>

<!-- ✅ data-state drives CSS — no modifier class needed -->
<button class="btn btn-primary" data-state="loading">...</button>
<!-- CSS: .btn[data-state="loading"] { opacity: .6; pointer-events: none; } -->

<!-- ❌ Bad -->
<div data-myData="value">        <!-- camelCase in HTML attribute -->
<div data-MyComponent="true">   <!-- PascalCase -->
<div data-d="42">               <!-- cryptic -->
<div dataId="42">               <!-- missing 'data-' prefix -->
```

### Law Zero: JS operates exclusively through data attributes

This is the fundamental separation rule — classes are for CSS, data attributes are for JS:

| Attribute | Purpose | Example |
|---|---|---|
| `data-ref` | DOM reference — cached in constructor once | `data-ref="send-btn"` |
| `data-action` | Delegated event handler trigger | `data-action="send"` |
| `data-id` | Record identifier | `data-id="order-42"` |
| `data-state` | JS-driven state, also consumed by CSS | `data-state="active"` |

### Common data attribute patterns

```html
<!-- Component config -->
data-{component}-{option}="value"       <!-- component options -->

<!-- Actions -->
data-action="submit|delete|toggle"
data-confirm="Confirmation message"
data-target="#selector"

<!-- State tracking -->
data-state="loading|success|error|idle"
data-theme="dark|light"
data-locale="en-US"

<!-- Analytics -->
data-track-event="click"
data-track-category="navigation"
data-track-label="main-cta"
```

---

## 6. HTML — ARIA Attributes

Use for accessibility when native semantics aren't enough:

```html
<!-- ✅ Landmark roles -->
<nav aria-label="Main navigation">
<nav aria-label="Breadcrumb">
<main aria-label="Main content">
<aside aria-label="Related articles">
<section aria-labelledby="section-heading-id">

<!-- ✅ Button states -->
<button
    aria-expanded="false"
    aria-controls="dropdown-menu"
    aria-haspopup="true"
>
    Menu
</button>

<!-- ✅ Dialog / modal -->
<div
    role="dialog"
    aria-modal="true"
    aria-labelledby="dialog-title"
    aria-describedby="dialog-description"
>
    <h2 id="dialog-title">Confirm Action</h2>
    <p id="dialog-description">This cannot be undone.</p>
</div>

<!-- ✅ Form inputs -->
<label for="input-email">Email</label>
<input
    id="input-email"
    type="email"
    aria-required="true"
    aria-invalid="false"
    aria-describedby="input-email-error input-email-hint"
>
<span id="input-email-hint">We'll never share your email.</span>
<span id="input-email-error" role="alert" aria-live="polite"></span>

<!-- ✅ Loading states -->
<div aria-live="polite" aria-atomic="true" aria-busy="true">
    Loading data...
</div>

<!-- ✅ Visually hidden (accessible text) -->
<button class="btn-icon">
    <svg aria-hidden="true" focusable="false">...</svg>
    <span class="sr-only">Close menu</span>
</button>
```

---

## 7. HTML — Custom Elements (Web Components)

Custom element names **must contain a hyphen** (HTML spec requirement):

```html
<!-- ✅ Good — must have at least one hyphen -->
<user-card data-user-id="42"></user-card>
<nav-bar></nav-bar>
<modal-dialog></modal-dialog>
<date-picker></date-picker>
<data-table></data-table>
<infinite-scroll></infinite-scroll>
<lazy-image src="..." alt="..."></lazy-image>
<color-picker></color-picker>
<app-header></app-header>
<app-footer></app-footer>
<my-component></my-component>

<!-- ✅ With prefix for org/project (avoids future HTML element collisions) -->
<acme-button variant="primary">Click</acme-button>
<acme-modal id="login-modal"></acme-modal>

<!-- ❌ Bad -->
<usercard></usercard>     <!-- no hyphen — treated as unknown inline element -->
<UserCard></UserCard>     <!-- PascalCase — not valid HTML -->
<user_card></user_card>   <!-- underscore -->
```

---

## 8. CSS — Selectors

### Selector specificity guidelines

```css
/* ✅ Best — class selectors, container-scoped */
.orders-container .nav-item {}
.orders-container .btn-primary {}

/* ✅ Acceptable — element selectors for base styles */
a {}
button {}
input {}
h1, h2, h3 {}

/* ⚠️ Use sparingly — attribute selectors */
[type="text"] {}
[aria-expanded="true"] {}
[data-theme="dark"] {}

/* ✅ State via data-state — preferred over modifier classes */
.nav-item[data-state="active"] {}
.btn[data-state="loading"] {}
.form-input[data-state="invalid"] {}

/* ⚠️ Avoid — ID selectors in CSS (use for JS only) */
#header {}          /* high specificity, hard to override */

/* ❌ Never — inline styles */
/* <div style="color: red"> */

/* ❌ Avoid — overly qualified selectors */
div.card {}         /* why div? just .card */
ul.nav-list {}      /* just .nav-list */
header nav {}       /* too coupled to HTML structure */
```

### State selectors — `data-state` + `:pseudo-classes`

```css
/* ✅ CSS pseudo-classes for native states */
.btn:hover {}
.btn:focus {}
.btn:active {}
.btn:disabled {}
.input:focus-visible {}
.link:visited {}
.item:first-child {}
.item:last-child {}
.item:nth-child(2n) {}

/* ✅ data-state for JS-controlled states */
.modal[data-state="open"] {}
.nav-item[data-state="active"] {}
.btn[data-state="loading"] {}
.form-input[data-state="invalid"] {}
.accordion[data-state="expanded"] {}
.sidebar[data-state="hidden"] {}

/* ✅ Attribute state selectors */
[aria-expanded="true"] {}
[aria-hidden="true"] {}
[data-state="loading"] {}
[data-theme="dark"] {}
```

---

## 9. CSS — Custom Properties (Variables)

Use **`--kebab-case`** with a naming system:

### Basic pattern

```css
:root {
    /* ✅ Pattern: --{category}-{property}-{variant/scale} */

    /* Colors */
    --color-primary: #2563eb;
    --color-primary-light: #3b82f6;
    --color-primary-dark: #1d4ed8;
    --color-secondary: #7c3aed;
    --color-neutral-100: #f3f4f6;
    --color-neutral-500: #6b7280;
    --color-neutral-900: #111827;
    --color-success: #16a34a;
    --color-warning: #d97706;
    --color-error: #dc2626;
    --color-info: #0284c7;

    /* Typography */
    --font-sans: 'Inter', system-ui, sans-serif;
    --font-serif: 'Merriweather', Georgia, serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

    --font-size-xs: 0.75rem;      /* 12px */
    --font-size-sm: 0.875rem;     /* 14px */
    --font-size-base: 1rem;       /* 16px */
    --font-size-lg: 1.125rem;     /* 18px */
    --font-size-xl: 1.25rem;      /* 20px */
    --font-size-2xl: 1.5rem;      /* 24px */
    --font-size-3xl: 1.875rem;    /* 30px */
    --font-size-4xl: 2.25rem;     /* 36px */

    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;

    --line-height-tight: 1.25;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.75;

    /* Spacing */
    --space-1: 0.25rem;   /* 4px */
    --space-2: 0.5rem;    /* 8px */
    --space-3: 0.75rem;   /* 12px */
    --space-4: 1rem;      /* 16px */
    --space-5: 1.25rem;   /* 20px */
    --space-6: 1.5rem;    /* 24px */
    --space-8: 2rem;      /* 32px */
    --space-10: 2.5rem;   /* 40px */
    --space-12: 3rem;     /* 48px */
    --space-16: 4rem;     /* 64px */
    --space-20: 5rem;     /* 80px */
    --space-24: 6rem;     /* 96px */

    /* Border */
    --border-width: 1px;
    --border-width-2: 2px;
    --border-color: var(--color-neutral-200);
    --border-radius-sm: 0.25rem;
    --border-radius: 0.375rem;
    --border-radius-md: 0.5rem;
    --border-radius-lg: 0.75rem;
    --border-radius-xl: 1rem;
    --border-radius-full: 9999px;

    /* Shadow */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);

    /* Z-index scale */
    --z-below: -1;
    --z-base: 0;
    --z-raised: 10;
    --z-dropdown: 100;
    --z-sticky: 200;
    --z-overlay: 300;
    --z-modal: 400;
    --z-popover: 500;
    --z-toast: 600;
    --z-tooltip: 700;

    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-base: 200ms ease;
    --transition-slow: 300ms ease;
    --transition-slower: 500ms ease;

    /* Layout */
    --container-sm: 640px;
    --container-md: 768px;
    --container-lg: 1024px;
    --container-xl: 1280px;
    --container-2xl: 1536px;
    --container-padding: var(--space-4);
}
```

### Component-scoped variables

```css
/* ✅ Scope custom properties to container for easy theming */
/* Pattern: --{widget}-{property} */
.orders-container {
    --orders-accent: var(--color-primary);
    --orders-card-radius: var(--border-radius-lg);
    --orders-anim-dur: 150ms;
}

.btn {
    --btn-bg: var(--color-primary);
    --btn-color: white;
    --btn-border: transparent;
    --btn-padding-x: var(--space-4);
    --btn-padding-y: var(--space-2);
    --btn-font-size: var(--font-size-base);
    --btn-border-radius: var(--border-radius);
    --btn-transition: background-color var(--transition-fast);

    background-color: var(--btn-bg);
    color: var(--btn-color);
    padding: var(--btn-padding-y) var(--btn-padding-x);
    font-size: var(--btn-font-size);
    border-radius: var(--btn-border-radius);
    transition: var(--btn-transition);
}

.btn-secondary {
    --btn-bg: transparent;
    --btn-color: var(--color-primary);
    --btn-border: var(--color-primary);
}

.btn-large {
    --btn-padding-x: var(--space-6);
    --btn-padding-y: var(--space-3);
    --btn-font-size: var(--font-size-lg);
}


/* ✅ Dark mode via CSS variables */
[data-theme="dark"] {
    --color-primary: #3b82f6;
    --color-neutral-100: #1f2937;
    --color-neutral-900: #f9fafb;
    --border-color: #374151;
}

@media (prefers-color-scheme: dark) {
    :root {
        --color-primary: #3b82f6;
        --bg-color: #0f172a;
        --text-color: #f1f5f9;
    }
}
```

---

## 10. Flat Container-Scoped Naming (replaces BEM)

> **BEM (`block__element--modifier`) is FORBIDDEN.** Double underscores `__` and double hyphens `--` as structural separators are not allowed anywhere in class names. See §25 for the full anti-pattern breakdown.

### The problem with BEM

BEM was designed to solve CSS scoping in a pre-component era. It encodes parent-child relationships directly into class name strings, producing verbose, brittle names like `.card__body__title` and coupling CSS structure tightly to HTML structure. Modern tools (component frameworks, CSS Modules, container scoping) solve this problem better.

### The approved approach: flat kebab-case + container scoping

Every widget/component has a **root container class**. All child styles are scoped to it via CSS descendant selectors. Child class names are flat, readable kebab-case words — no `__` separator.

### Three legal patterns for child element naming

#### Pattern A — Descendant selector (preferred for widget internals)

The container class scopes the child. The child has a simple, generic class name that only means something inside the container:

```html
<section class="orders-container">
    <ul class="items-list" data-ref="items-list">
        <li class="orders-item" data-id="42" data-state="active">
            <span class="name">Order #42</span>
            <span class="status">Active</span>
            <button class="btn btn-sm btn-danger" data-action="remove">Remove</button>
        </li>
    </ul>
</section>
```

```css
/* ✅ Every selector starts with the container class */
.orders-container .items-list    { list-style: none; padding: 0; }
.orders-container .orders-item   { display: flex; gap: 1rem; padding: .75rem; }
.orders-container .name          { font-weight: 600; }
.orders-container .status        { color: var(--color-text-secondary); }

/* ✅ State via data-state attribute selector */
.orders-container .orders-item[data-state="active"]    { border-left: 3px solid var(--color-success); }
.orders-container .orders-item[data-state="cancelled"] { opacity: .5; }
```

#### Pattern B — Flat prefixed class (preferred for reusable child components)

Prefix the child class with the widget name. The child is still standalone but carries the widget namespace:

```html
<section class="orders-container">
    <div class="orders-modal" data-ref="modal-delete" hidden>
        <h2 class="orders-modal-title" id="orders-modal-title">Delete order?</h2>
        <p class="orders-modal-body">This cannot be undone.</p>
        <div class="orders-modal-actions">
            <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
            <button class="btn btn-danger" data-action="modal-confirm">Confirm</button>
        </div>
    </div>
</section>
```

```css
.orders-container .orders-modal         { background: white; border-radius: .5rem; padding: 1.5rem; }
.orders-container .orders-modal-title   { font-size: 1.125rem; font-weight: 600; }
.orders-container .orders-modal-body    { color: var(--color-text-secondary); margin-bottom: 1rem; }
.orders-container .orders-modal-actions { display: flex; gap: .5rem; justify-content: flex-end; }
```

#### Pattern C — Descendant + meaningful child class (preferred for shared sub-components)

The child element appears inside the container, styled via ancestor chain without a prefix:

```html
<div class="card card-featured">
    <img class="card-image" src="..." alt="...">
    <div class="card-body">
        <h2 class="card-title">Title</h2>
        <p class="card-description">Description text.</p>
    </div>
    <div class="card-footer">
        <button class="btn btn-primary">Read more</button>
    </div>
</div>
```

```css
.card              { background: white; border-radius: var(--border-radius-lg); box-shadow: var(--shadow); }
.card-featured     { border: 2px solid var(--color-primary); }
.card-image        { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.card-body         { padding: var(--space-4); }
.card-title        { font-size: var(--font-size-xl); font-weight: var(--font-weight-bold); }
.card-description  { color: var(--color-text-secondary); }
.card-footer       { padding: var(--space-4); border-top: 1px solid var(--border-color); }
```

### Pattern decision table

| Situation | Use pattern | Example |
|---|---|---|
| Widget internals scoped to one container | A (descendant) | `.orders-container .items-list` |
| Modal inside a widget | B (prefixed) | `.orders-modal-title` |
| Reusable card / button / badge | C (flat prefixed) | `.card-title`, `.btn-primary` |
| Shared generic internals (`.title`, `.body`) | A (always scoped) | `.orders-modal .title` |

### States: `data-state` is the only mechanism

BEM modifier classes (`.card--featured`, `.btn--loading`) are **not used for JS-driven states**. Visual state is expressed via the `data-state` attribute, which CSS reads as an attribute selector:

```html
<!-- ✅ State via data-state -->
<li class="orders-item" data-state="active">...</li>
<button class="btn btn-primary" data-state="loading">...</button>
<input class="form-input" data-state="invalid">

<!-- ❌ FORBIDDEN — BEM modifier for state -->
<li class="orders-item orders-item--active">...</li>
<button class="btn btn--loading">...</button>
<input class="form-input form-input--invalid">
```

```css
/* ✅ State styles — attribute selectors */
.orders-item[data-state="active"]    { border-left: 3px solid var(--color-success); }
.btn[data-state="loading"]           { opacity: .6; pointer-events: none; }
.form-input[data-state="invalid"]    { border-color: var(--color-error); }

/* ❌ FORBIDDEN — BEM modifier states */
.orders-item--active    { ... }
.btn--loading           { ... }
.form-input--invalid    { ... }
```

### Variant modifier classes: single hyphen only

Permanent visual variants (not JS-driven) use a **single-hyphen** modifier class alongside the base class:

```html
<!-- ✅ Variant via single-hyphen modifier -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-large">Large</button>
<div class="alert alert-error">Error</div>
<div class="card card-featured">Featured</div>

<!-- ❌ FORBIDDEN — double-hyphen BEM modifier -->
<button class="btn btn--primary">Primary</button>
<div class="card card--featured">Featured</div>
```

### Full navigation example (no BEM)

```html
<!-- ✅ Navigation using flat container-scoped naming -->
<nav class="site-nav" aria-label="Main navigation">
    <ul class="nav-list">
        <li class="nav-item" data-state="active">
            <a class="nav-link" href="/">Home</a>
        </li>
        <li class="nav-item" data-has-dropdown>
            <a class="nav-link nav-link-parent" href="/products">Products</a>
            <ul class="nav-dropdown">
                <li class="nav-dropdown-item">
                    <a class="nav-dropdown-link" href="/products/web">Web</a>
                </li>
            </ul>
        </li>
    </ul>
</nav>
```

```css
.site-nav               { background: white; border-bottom: 1px solid var(--border-color); }
.site-nav .nav-list     { display: flex; list-style: none; margin: 0; padding: 0; }
.site-nav .nav-item     { position: relative; }
.site-nav .nav-link     { display: block; padding: var(--space-3) var(--space-4); }
.site-nav .nav-item[data-state="active"] .nav-link { color: var(--color-primary); font-weight: 600; }
.site-nav .nav-dropdown { position: absolute; top: 100%; left: 0; background: white; box-shadow: var(--shadow-lg); }
.site-nav .nav-dropdown-item { list-style: none; }
.site-nav .nav-dropdown-link { display: block; padding: var(--space-2) var(--space-4); }
```

### CSS custom tokens — always prefixed with widget name

Token names declared on a widget container must carry the widget's full-word prefix to prevent collisions:

```css
/* ✅ Correct — full word prefix */
.orders-container {
    --orders-accent: var(--color-primary);
    --orders-card-radius: .5rem;
    --orders-anim-dur: 150ms;
}

/* ❌ Wrong — abbreviated, collides with other widgets */
.orders-container {
    --ord-accent: var(--color-primary);
    --cr: .5rem;
}
```

---

## 11. SMACSS Methodology

**Scalable and Modular Architecture for CSS** — categorizes CSS into 5 types:

```
Base       — element defaults (no class)
Layout     — l- prefix
Module     — no prefix (component)
State      — data-state attribute (not is- class)
Theme      — theme- prefix
```

```css
/* Base — element defaults, no class selectors */
*, *::before, *::after { box-sizing: border-box; }
body { font-family: var(--font-sans); }
a { color: var(--color-primary); }
img { max-width: 100%; }

/* Layout — l- prefix, major structural regions */
.l-container { max-width: 1280px; margin: 0 auto; }
.l-grid { display: grid; }
.l-sidebar { display: grid; grid-template-columns: 280px 1fr; }
.l-stack { display: flex; flex-direction: column; }
.l-cluster { display: flex; flex-wrap: wrap; }

/* Module — reusable components, flat kebab-case */
.nav {}
.card {}
.btn {}
.modal {}
.badge {}

/* State — data-state attribute selectors, not .is-* classes */
[data-state="active"] {}
[data-state="hidden"] {}
[data-state="loading"] {}
[data-state="expanded"] {}
[data-state="invalid"] {}

/* Theme — overrides for theming */
.theme-dark {}
.theme-light {}
```

---

## 12. OOCSS Methodology

**Object-Oriented CSS** — separates **structure** from **skin**, and **container** from **content**:

```css
/* ✅ Structure — layout, sizing, spacing */
.media {}               /* structure: image + text side by side */
.media-image {}
.media-body {}

.flag {}                /* like media but vertically centered */
.flag-image {}
.flag-body {}

/* ✅ Skin — visual appearance */
.box {}                 /* generic content box */
.box-rounded {}
.box-shadowed {}
.box-bordered {}

/* ✅ Separate: don't tie skin to container */
/* ❌ Bad OOCSS — skin depends on location */
.sidebar .widget { background: white; }
.footer .widget { background: gray; }

/* ✅ Good OOCSS — reusable skin classes */
.widget {}
.widget-light { background: white; }
.widget-dark { background: gray; }
```

---

## 13. ITCSS Architecture

**Inverted Triangle CSS** — organizes styles from generic to specific. Layers go from low specificity to high:

```
1. Settings      — variables, config (no CSS output)
2. Tools         — mixins, functions (no CSS output)
3. Generic       — resets, normalize
4. Elements      — bare HTML elements
5. Objects       — layout patterns (OOCSS)
6. Components    — UI components (flat container-scoped naming)
7. Utilities     — helpers, overrides
```

```css
/* 1. Settings */
/* _settings.colors.css, _settings.typography.css */
:root {
    --color-primary: #2563eb;
}

/* 2. Tools (SCSS) */
/* _tools.mixins.scss, _tools.functions.scss */

/* 3. Generic */
/* _generic.reset.css, _generic.box-sizing.css */
*, *::before, *::after { box-sizing: border-box; }

/* 4. Elements */
/* _elements.headings.css, _elements.links.css */
h1, h2, h3, h4, h5, h6 { font-weight: var(--font-weight-bold); }
a { color: var(--color-primary); text-decoration: underline; }

/* 5. Objects — o- prefix */
/* _objects.container.css, _objects.grid.css */
.o-container { max-width: 1280px; margin: 0 auto; padding: 0 var(--space-4); }
.o-grid { display: grid; gap: var(--space-4); }
.o-stack { display: flex; flex-direction: column; gap: var(--space-4); }
.o-cluster { display: flex; flex-wrap: wrap; gap: var(--space-2); }
.o-media { display: flex; gap: var(--space-4); align-items: flex-start; }
.o-ratio { position: relative; }
.o-ratio-content { position: absolute; inset: 0; }

/* 6. Components — flat container-scoped naming */
/* _components.card.css, _components.nav.css */
.card {}
.btn {}
.nav {}

/* 7. Utilities — u- prefix */
/* _utilities.spacing.css, _utilities.text.css */
.u-hidden { display: none !important; }
.u-sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
.u-text-center { text-align: center !important; }
.u-mt-auto { margin-top: auto !important; }
```

---

## 14. Utility / Atomic CSS

Utility-first (like Tailwind) uses small, single-purpose classes directly in HTML:

```html
<!-- ✅ Utility-first (Tailwind-style) -->
<div class="flex flex-col gap-4 p-6 bg-white rounded-xl shadow-md">
    <h2 class="text-xl font-bold text-gray-900">Card Title</h2>
    <p class="text-sm text-gray-600 leading-relaxed">Description text here.</p>
    <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
        Read more
    </button>
</div>
```

### Custom utility classes (hand-written)

```css
/* ✅ Pattern: .{property-abbreviation}-{value} */

/* Display */
.d-none        { display: none; }
.d-block       { display: block; }
.d-flex        { display: flex; }
.d-grid        { display: grid; }
.d-inline      { display: inline; }
.d-inline-flex { display: inline-flex; }

/* Flexbox */
.flex-col      { flex-direction: column; }
.flex-wrap     { flex-wrap: wrap; }
.items-center  { align-items: center; }
.items-start   { align-items: flex-start; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.flex-1        { flex: 1; }
.flex-auto     { flex: auto; }

/* Spacing */
.m-0     { margin: 0; }
.mt-1    { margin-top: var(--space-1); }
.mt-2    { margin-top: var(--space-2); }
.mt-4    { margin-top: var(--space-4); }
.mb-4    { margin-bottom: var(--space-4); }
.mx-auto { margin-inline: auto; }
.p-4     { padding: var(--space-4); }
.px-4    { padding-inline: var(--space-4); }
.py-2    { padding-block: var(--space-2); }
.gap-4   { gap: var(--space-4); }

/* Typography */
.text-sm   { font-size: var(--font-size-sm); }
.text-base { font-size: var(--font-size-base); }
.text-lg   { font-size: var(--font-size-lg); }
.text-xl   { font-size: var(--font-size-xl); }
.font-bold { font-weight: var(--font-weight-bold); }
.text-center { text-align: center; }
.truncate  { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* Visibility */
.hidden    { display: none !important; }
.invisible { visibility: hidden; }
.sr-only   {
    position: absolute; width: 1px; height: 1px;
    padding: 0; margin: -1px; overflow: hidden;
    clip: rect(0,0,0,0); white-space: nowrap; border: 0;
}
```

---

## 15. CSS Modules

Used in React, Vue, etc. Class names are **camelCase** (becomes JS object property):

```css
/* UserCard.module.css */

/* ✅ camelCase — accessed as styles.cardWrapper */
.cardWrapper {
    display: flex;
    flex-direction: column;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.cardHeader {
    padding: 16px;
    border-bottom: 1px solid #eee;
}

.cardTitle {
    font-size: 1.25rem;
    font-weight: 700;
    color: #111;
}

.cardBody {
    padding: 16px;
}

/* Modifier — still camelCase, no double-hyphen */
.cardFeatured {
    border: 2px solid #2563eb;
}

.isLoading {
    opacity: 0.6;
    pointer-events: none;
}
```

```jsx
// In React
import styles from './UserCard.module.css';

function UserCard({ user, isFeatured }) {
    return (
        <div className={`${styles.cardWrapper} ${isFeatured ? styles.cardFeatured : ''}`}>
            <div className={styles.cardHeader}>
                <h2 className={styles.cardTitle}>{user.name}</h2>
            </div>
            <div className={styles.cardBody}>...</div>
        </div>
    );
}
```

---

## 16. SCSS / Sass Conventions

```scss
// ✅ Variables — kebab-case (before custom properties era)
$color-primary: #2563eb;
$font-sans: 'Inter', system-ui, sans-serif;
$space-4: 1rem;
$border-radius: 0.375rem;

// ✅ Mixins — kebab-case verb phrase
@mixin flex-center {
    display: flex;
    align-items: center;
    justify-content: center;
}

@mixin respond-to($breakpoint) {
    @if $breakpoint == 'md' {
        @media (min-width: 768px) { @content; }
    } @else if $breakpoint == 'lg' {
        @media (min-width: 1024px) { @content; }
    }
}

@mixin truncate-text($lines: 1) {
    @if $lines == 1 {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    } @else {
        display: -webkit-box;
        -webkit-line-clamp: $lines;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
}

// ✅ Functions — kebab-case
@function rem($px) {
    @return #{$px / 16}rem;
}

@function spacing($multiplier) {
    @return #{$multiplier * 0.25}rem;
}

// ✅ Placeholders — kebab-case with % prefix
%visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

%clearfix {
    &::after {
        content: '';
        display: table;
        clear: both;
    }
}

// ✅ SCSS with flat container-scoped naming (no BEM & operator nesting)
.card {
    background: white;
    border-radius: var(--border-radius-lg);

    // ✅ Variant — single hyphen modifier as sibling rule
    &.card-featured {
        border: 2px solid var(--color-primary);
    }

    // ✅ State via data-state
    &[data-state="loading"] {
        opacity: 0.6;
    }

    // ✅ Responsive inside component
    @include respond-to('md') {
        display: grid;
        grid-template-columns: 1fr 2fr;
    }
}

// ✅ Child elements — descendant rules, no & __ nesting
.card-image {
    width: 100%;
    object-fit: cover;
}

.card-body {
    padding: var(--space-4);
}

.card-title {
    font-size: var(--font-size-xl);
}

.card-title-large {
    font-size: var(--font-size-2xl);
}

// ❌ FORBIDDEN — BEM element nesting with & __
// .card {
//     &__image { ... }   ← FORBIDDEN
//     &__body  { ... }   ← FORBIDDEN
//     &--featured { ... } ← FORBIDDEN
// }

// ✅ File naming — partial files start with underscore
// _variables.scss
// _mixins.scss
// _functions.scss
// _reset.scss
// _typography.scss
// _components.card.scss
// _components.nav.scss
// main.scss (imports all partials)
```

---

## 17. CSS — Keyframes & Animations

Use **kebab-case** for keyframe names. For widget components, **always prefix keyframe names with the widget name** — keyframe names are global and will collide across widgets:

```css
/* ✅ Keyframe naming — verb or descriptive noun */
@keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fade-out {
    from { opacity: 1; }
    to { opacity: 0; }
}

@keyframes slide-in-right {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
}

@keyframes slide-out-left {
    from { transform: translateX(0); }
    to { transform: translateX(-100%); }
}

@keyframes scale-in {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* ✅ Widget-prefixed keyframes — mandatory inside widget scopes */
@keyframes orders-modal-in {
    from { opacity: 0; transform: scale(.95); }
    to   { opacity: 1; transform: scale(1);   }
}

/* ❌ Wrong — abbreviated, may collide */
@keyframes ord-mi { }

/* ❌ Wrong — generic, guaranteed collision */
@keyframes modal-in { }
```

```css
/* ✅ Usage */
.spinner {
    animation: spin 1s linear infinite;
}

.modal {
    animation: scale-in var(--transition-base) ease-out both;
}

/* ✅ Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

Animate only `transform` and `opacity` wherever possible — these properties run on the compositor thread with no reflow or repaint cost.

---

## 18. CSS — Media Queries & Breakpoints

Use a consistent **t-shirt size** breakpoint scale. Write **mobile-first** (`min-width`):

```css
/* ✅ Define breakpoints as custom properties or SCSS variables */
:root {
    --bp-sm:  640px;
    --bp-md:  768px;
    --bp-lg:  1024px;
    --bp-xl:  1280px;
    --bp-2xl: 1536px;
}

/* ✅ Mobile-first — min-width overrides */
.card {
    flex-direction: column;    /* mobile default */
}

@media (min-width: 768px) {
    .card {
        flex-direction: row;   /* md and up */
    }
}

@media (min-width: 1024px) {
    .card {
        max-width: 900px;      /* lg and up */
    }
}

/* ✅ Semantic names for breakpoints in SCSS */
@mixin respond-to($bp) {
    @if $bp == 'sm'  { @media (min-width: 640px)  { @content; } }
    @if $bp == 'md'  { @media (min-width: 768px)  { @content; } }
    @if $bp == 'lg'  { @media (min-width: 1024px) { @content; } }
    @if $bp == 'xl'  { @media (min-width: 1280px) { @content; } }
    @if $bp == '2xl' { @media (min-width: 1536px) { @content; } }
}

/* ✅ Media query naming convention — inside component files */
.hero {
    padding: var(--space-8) var(--space-4);    /* xs */

    @include respond-to('md') {
        padding: var(--space-16) var(--space-8);
    }

    @include respond-to('lg') {
        padding: var(--space-24) var(--space-16);
    }
}
```

---

## 19. CSS — Z-index Scale

Never use magic numbers. Declare a scale as custom properties:

```css
:root {
    --z-below:    -1;    /* Behind everything (bg layers) */
    --z-base:      0;    /* Default stacking context */
    --z-raised:   10;    /* Slightly elevated (cards on hover) */
    --z-dropdown: 100;   /* Dropdown menus */
    --z-sticky:   200;   /* Sticky headers/navbars */
    --z-overlay:  300;   /* Page overlays / backdrops */
    --z-modal:    400;   /* Modal dialogs */
    --z-popover:  500;   /* Popovers (date pickers, selects) */
    --z-toast:    600;   /* Toast notifications */
    --z-tooltip:  700;   /* Tooltips (always on top) */
}

/* ✅ Usage */
.dropdown-menu {
    z-index: var(--z-dropdown);
}

.modal-backdrop {
    z-index: var(--z-overlay);
}

.modal-dialog {
    z-index: var(--z-modal);
}

.toast-container {
    z-index: var(--z-toast);
}

/* ❌ Bad — magic numbers */
.dropdown { z-index: 9; }
.modal { z-index: 9999; }
.tooltip { z-index: 99999; }
```

---

## 20. CSS — Color Naming

Two-tier system: **primitive tokens** → **semantic tokens**:

```css
:root {
    /* Tier 1 — Primitive (raw values, never used directly in components) */
    --palette-blue-50: #eff6ff;
    --palette-blue-100: #dbeafe;
    --palette-blue-400: #60a5fa;
    --palette-blue-500: #3b82f6;
    --palette-blue-600: #2563eb;
    --palette-blue-700: #1d4ed8;
    --palette-blue-900: #1e3a8a;

    --palette-red-50: #fef2f2;
    --palette-red-500: #ef4444;
    --palette-red-700: #b91c1c;

    --palette-green-50: #f0fdf4;
    --palette-green-500: #22c55e;
    --palette-green-700: #15803d;

    --palette-gray-50: #f9fafb;
    --palette-gray-100: #f3f4f6;
    --palette-gray-200: #e5e7eb;
    --palette-gray-500: #6b7280;
    --palette-gray-700: #374151;
    --palette-gray-900: #111827;

    /* Tier 2 — Semantic (purposeful, used in components) */
    --color-brand:              var(--palette-blue-600);
    --color-brand-hover:        var(--palette-blue-700);
    --color-brand-light:        var(--palette-blue-50);

    --color-success:            var(--palette-green-500);
    --color-success-bg:         var(--palette-green-50);
    --color-error:              var(--palette-red-500);
    --color-error-bg:           var(--palette-red-50);
    --color-warning:            #f59e0b;
    --color-warning-bg:         #fffbeb;
    --color-info:               var(--palette-blue-500);
    --color-info-bg:            var(--palette-blue-50);

    --color-text-primary:       var(--palette-gray-900);
    --color-text-secondary:     var(--palette-gray-500);
    --color-text-disabled:      var(--palette-gray-300);
    --color-text-inverse:       white;
    --color-text-link:          var(--palette-blue-600);
    --color-text-link-hover:    var(--palette-blue-700);

    --color-bg-page:            white;
    --color-bg-subtle:          var(--palette-gray-50);
    --color-bg-muted:           var(--palette-gray-100);
    --color-bg-inverse:         var(--palette-gray-900);

    --color-border:             var(--palette-gray-200);
    --color-border-strong:      var(--palette-gray-400);
    --color-border-focus:       var(--palette-blue-500);
}
```

---

## 21. CSS — Spacing & Sizing Scales

```css
/* ✅ 4px base grid scale (most common) */
:root {
    --space-px: 1px;
    --space-0:  0;
    --space-1:  0.25rem;   /*  4px */
    --space-2:  0.5rem;    /*  8px */
    --space-3:  0.75rem;   /* 12px */
    --space-4:  1rem;      /* 16px */
    --space-5:  1.25rem;   /* 20px */
    --space-6:  1.5rem;    /* 24px */
    --space-7:  1.75rem;   /* 28px */
    --space-8:  2rem;      /* 32px */
    --space-9:  2.25rem;   /* 36px */
    --space-10: 2.5rem;    /* 40px */
    --space-11: 2.75rem;   /* 44px */
    --space-12: 3rem;      /* 48px */
    --space-14: 3.5rem;    /* 56px */
    --space-16: 4rem;      /* 64px */
    --space-20: 5rem;      /* 80px */
    --space-24: 6rem;      /* 96px */
    --space-28: 7rem;      /* 112px */
    --space-32: 8rem;      /* 128px */

    /* Semantic spacing aliases */
    --space-page-padding:   var(--space-4);
    --space-section:        var(--space-16);
    --space-component:      var(--space-6);
    --space-element:        var(--space-4);
    --space-tight:          var(--space-2);
}
```

---

## 22. CSS — Typography Scale

```css
:root {
    /* Fluid typography (clamp) — scales between viewport sizes */
    --text-xs:   clamp(0.694rem, 0.66rem + 0.17vw, 0.75rem);
    --text-sm:   clamp(0.833rem, 0.79rem + 0.21vw, 0.875rem);
    --text-base: clamp(1rem, 0.96rem + 0.22vw, 1.125rem);
    --text-lg:   clamp(1.2rem, 1.13rem + 0.35vw, 1.375rem);
    --text-xl:   clamp(1.44rem, 1.35rem + 0.46vw, 1.625rem);
    --text-2xl:  clamp(1.728rem, 1.59rem + 0.69vw, 2rem);
    --text-3xl:  clamp(2.074rem, 1.89rem + 0.92vw, 2.5rem);
    --text-4xl:  clamp(2.488rem, 2.22rem + 1.34vw, 3rem);
    --text-5xl:  clamp(2.986rem, 2.6rem + 1.93vw, 3.75rem);

    /* Named semantic aliases */
    --text-caption:     var(--text-xs);
    --text-body-sm:     var(--text-sm);
    --text-body:        var(--text-base);
    --text-body-lg:     var(--text-lg);
    --text-subtitle:    var(--text-xl);
    --text-title-sm:    var(--text-2xl);
    --text-title:       var(--text-3xl);
    --text-title-lg:    var(--text-4xl);
    --text-display:     var(--text-5xl);
}
```

---

## 23. File & Directory Structure

### Flat (small projects)

```
css/
  reset.css
  variables.css
  typography.css
  layout.css
  components.css
  utilities.css
  main.css

html/
  index.html
  about.html
  contact.html
```

### ITCSS / SMACSS (medium to large projects)

```
src/
  styles/
    settings/
      _colors.scss
      _typography.scss
      _spacing.scss
      _breakpoints.scss

    tools/
      _mixins.scss
      _functions.scss

    generic/
      _reset.scss
      _box-sizing.scss
      _normalize.scss

    elements/
      _headings.scss
      _links.scss
      _lists.scss
      _tables.scss
      _forms.scss
      _images.scss

    objects/
      _container.scss
      _grid.scss
      _stack.scss
      _cluster.scss
      _media.scss

    components/
      _button.scss
      _card.scss
      _nav.scss
      _modal.scss
      _form.scss
      _table.scss
      _badge.scss
      _avatar.scss
      _dropdown.scss
      _pagination.scss
      _breadcrumb.scss
      _toast.scss
      _tooltip.scss
      _spinner.scss
      _skeleton.scss

    utilities/
      _display.scss
      _spacing.scss
      _typography.scss
      _color.scss
      _accessibility.scss

    main.scss       ← imports all partials in order
```

### Component co-location (React / Vue)

```
src/
  components/
    Button/
      Button.tsx
      Button.module.css
      Button.test.tsx
      index.ts
    Card/
      Card.tsx
      Card.module.css
      index.ts
    Modal/
      Modal.tsx
      Modal.module.css
      index.ts
```

---

## 24. HTML — Forms

Consistent naming is critical for accessibility and UX:

```html
<!-- ✅ Well-structured form -->
<form
    id="form-contact"
    class="form"
    action="/api/contact"
    method="post"
    novalidate
    data-js-validate
>
    <!-- Group: label + input + hint + error -->
    <div class="form-group">
        <label class="form-label" for="input-full-name">
            Full name
            <span class="form-required" aria-hidden="true">*</span>
        </label>
        <input
            class="form-input"
            id="input-full-name"
            type="text"
            name="full_name"
            autocomplete="name"
            required
            aria-required="true"
            aria-describedby="hint-full-name error-full-name"
            data-ref="input-full-name"
        >
        <span class="form-hint" id="hint-full-name">
            Enter your first and last name.
        </span>
        <span class="form-error" id="error-full-name" role="alert" aria-live="polite">
            <!-- Error message injected by JS -->
        </span>
    </div>

    <div class="form-group">
        <label class="form-label" for="input-email">Email address</label>
        <input
            class="form-input"
            id="input-email"
            type="email"
            name="email"
            autocomplete="email"
            required
            aria-required="true"
            aria-describedby="error-email"
        >
        <span class="form-error" id="error-email" role="alert" aria-live="polite"></span>
    </div>

    <div class="form-group">
        <label class="form-label" for="select-subject">Subject</label>
        <select
            class="form-select"
            id="select-subject"
            name="subject"
            required
        >
            <option value="">Choose a subject...</option>
            <option value="general">General inquiry</option>
            <option value="support">Technical support</option>
            <option value="billing">Billing</option>
        </select>
    </div>

    <div class="form-group">
        <label class="form-label" for="textarea-message">Message</label>
        <textarea
            class="form-textarea"
            id="textarea-message"
            name="message"
            rows="5"
            required
            aria-describedby="hint-message"
        ></textarea>
        <span class="form-hint" id="hint-message">Minimum 20 characters.</span>
    </div>

    <div class="form-group form-group-checkbox">
        <input
            class="form-checkbox"
            id="check-newsletter"
            type="checkbox"
            name="newsletter"
            value="1"
        >
        <label class="form-label form-label-checkbox" for="check-newsletter">
            Subscribe to newsletter
        </label>
    </div>

    <div class="form-actions">
        <button class="btn btn-primary" type="submit">Send message</button>
        <button class="btn btn-ghost" type="reset">Clear</button>
    </div>
</form>
```

---

## 25. Naming Anti-patterns

### ❌ BEM (`block__element--modifier`) — FORBIDDEN

BEM is the primary anti-pattern in this guide. It is completely prohibited:

```html
<!-- ❌ FORBIDDEN — BEM double underscore element separator -->
<div class="card__body">
<div class="card__title">
<div class="nav__item">
<a class="nav__link">
<div class="form__group">
<input class="form__input">

<!-- ❌ FORBIDDEN — BEM double hyphen modifier separator -->
<div class="card card--featured">
<button class="btn btn--primary">
<div class="nav__item nav__item--active">
<input class="form__input form__input--error">

<!-- ❌ FORBIDDEN — BEM nested elements (double nesting) -->
<div class="card__body__title">
<div class="nav__list__item__link">

<!-- ✅ Correct — flat kebab-case + container scoping -->
<div class="card card-featured">
    <div class="card-body">
        <h2 class="card-title">Title</h2>
    </div>
</div>

<nav class="site-nav">
    <ul class="nav-list">
        <li class="nav-item" data-state="active">
            <a class="nav-link" href="/">Home</a>
        </li>
    </ul>
</nav>
```

```css
/* ❌ FORBIDDEN — BEM in CSS */
.card__body { }
.card__title { }
.card--featured { }
.nav__item--active { }

/* ✅ Correct — flat + descendant scoping */
.card-body { }
.card-title { }
.card-featured { }
.nav-item[data-state="active"] { }
.site-nav .nav-item[data-state="active"] { }
```

**Why BEM is forbidden:**
- `__` encodes parent-child relationships into string names, coupling CSS to HTML structure
- `--` modifier syntax for states is superseded by `data-state` attribute selectors, which are cleaner and JS-friendly
- BEM produces verbose, hard-to-read class strings (`.site-header__nav__item--has-dropdown--active`)
- Container-scoped descendant selectors achieve the same isolation without abusing class name syntax
- The `stylelint-selector-bem-pattern` plugin actively enforces patterns that conflict with modern component architecture

### ❌ Classes used as JS hooks

```html
<!-- ❌ FORBIDDEN — class double-duty as JS hook -->
<button class="btn btn-primary js-send-btn">Send</button>
<div class="modal js-modal">...</div>
<input class="form-input js-validate-email">

<!-- ✅ Correct — data attributes for JS, classes for CSS only -->
<button class="btn btn-primary" data-action="send">Send</button>
<div class="modal" data-ref="modal-login">...</div>
<input class="form-input" data-validate-rule="email">
```

### ❌ IDs used as JS hooks

```html
<!-- ❌ FORBIDDEN — id as JS hook -->
<button id="send-btn" class="btn btn-primary">Send</button>
<!-- In JS: document.getElementById('send-btn') — FORBIDDEN -->

<!-- ✅ Correct — data-ref for JS -->
<button class="btn btn-primary" data-ref="send-btn">Send</button>
<!-- In JS: this._root.querySelector('[data-ref="send-btn"]') -->
```

### ❌ Presentational class names

```html
<!-- ❌ Bad — tied to visual appearance, not semantics -->
<div class="red-text">
<div class="blue-box">
<div class="big-font">
<div class="left-sidebar">
<div class="float-right">
<button class="green-button">

<!-- ✅ Good — semantic names -->
<div class="alert alert-error">
<div class="card">
<div class="heading-large">
<aside class="sidebar">
<aside class="sidebar-secondary">
<button class="btn btn-success">
```

### ❌ Overly generic names

```html
<!-- ❌ Vague — what does "box" mean? -->
<div class="box">
<div class="wrapper">
<div class="container2">
<div class="inner">
<div class="outer">
<div class="holder">
<div class="wrap">
<div class="item">     <!-- every element is an "item" -->
<div class="thing">

<!-- ✅ Specific -->
<div class="modal">
<div class="page-wrapper">
<div class="content-container">
<div class="card-inner">
<div class="section-outer">
<div class="form-field">
<div class="nav-item">
```

### ❌ Using IDs for styling

```css
/* ❌ Bad — high specificity, breaks cascade */
#header { background: blue; }
#main-nav a { color: white; }
#sidebar { width: 280px; }

/* ✅ Good — use classes */
.site-header { background: blue; }
.main-nav-link { color: white; }
.sidebar { width: 280px; }
```

### ❌ camelCase / PascalCase in HTML/CSS

```html
<!-- ❌ Bad -->
<div class="userCard">
<div class="UserProfile">
<div class="navBar">
<section id="aboutUs">

<!-- ✅ Good -->
<div class="user-card">
<div class="user-profile">
<div class="nav-bar">
<section id="about-us">
```

### ❌ Magic z-index values

```css
/* ❌ Bad */
.modal { z-index: 9999; }
.tooltip { z-index: 99999; }
.overlay { z-index: 9998; }

/* ✅ Good */
.modal { z-index: var(--z-modal); }
.tooltip { z-index: var(--z-tooltip); }
.overlay { z-index: var(--z-overlay); }
```

### ❌ Abbreviated / cryptic class and token names

```html
<!-- ❌ Wrong — cryptic abbreviations -->
<div class="ord-item">
<div class="nwsl-hdr">
<span class="ord-st-badge">

<!-- ✅ Correct — full readable words -->
<div class="orders-item">
<div class="newsletters-header">
<span class="orders-status-badge">
```

```css
/* ❌ Wrong — abbreviated tokens */
.orders-container { --ord-accent: blue; --cr: .5rem; }

/* ✅ Correct — full word prefix */
.orders-container { --orders-accent: blue; --orders-card-radius: .5rem; }
```

---

## 26. Quick Reference Cheatsheet

| Item | Convention | Example |
|------|-----------|---------|
| HTML tag | lowercase | `<div>`, `<section>`, `<nav>` |
| HTML attribute | lowercase kebab | `aria-label`, `data-user-id` |
| ID | kebab-case | `#user-profile`, `#orders-modal-title` |
| Class (general) | kebab-case | `user-card`, `nav-item` |
| Component class | kebab-case noun | `.card`, `.nav`, `.btn` |
| Variant modifier | `base-modifier` (single hyphen) | `.card-featured`, `.btn-primary` |
| State | `data-state` attribute | `data-state="active"` |
| State CSS | attribute selector | `.nav-item[data-state="active"]` |
| JS hook | `data-ref` / `data-action` | `data-ref="send-btn"`, `data-action="send"` |
| Child element (scoped) | descendant selector | `.orders-container .items-list` |
| Child element (prefixed) | `widget-child` flat | `.orders-modal-title` |
| Container token | `--{widget}-{property}` | `--orders-accent`, `--orders-card-radius` |
| State class | `.is-*` or `.has-*` (SMACSS only) | `.is-active`, `.has-error` |
| Layout class (SMACSS) | `.l-*` | `.l-container`, `.l-grid` |
| Object class (ITCSS) | `.o-*` | `.o-stack`, `.o-media` |
| Utility class | `.u-*` or abbreviation | `.u-hidden`, `.sr-only` |
| Custom property | `--kebab-case` | `--color-primary`, `--space-4` |
| Semantic token | `--{category}-{name}` | `--color-text-primary` |
| Primitive token | `--palette-{color}-{scale}` | `--palette-blue-500` |
| CSS component var | `--{block}-{property}` | `--btn-bg`, `--card-padding` |
| SCSS variable | `$kebab-case` | `$color-primary` |
| SCSS mixin | `@mixin kebab-case` | `@mixin flex-center` |
| SCSS function | `@function kebab-case` | `@function rem()` |
| SCSS placeholder | `%kebab-case` | `%visually-hidden` |
| Keyframe (global) | kebab-case verb | `fade-in`, `slide-in-up`, `spin` |
| Keyframe (widget) | `{widget}-kebab-case` | `orders-modal-in` |
| CSS Modules class | camelCase | `.cardWrapper`, `.navItem` |
| Web component | `hyphenated-name` | `<user-card>`, `<nav-bar>` |
| File (CSS) | kebab-case | `_components.card.scss` |
| File (SCSS partial) | `_underscore-prefix` | `_variables.scss` |
| Breakpoint | t-shirt size | `xs`, `sm`, `md`, `lg`, `xl`, `2xl` |
| Z-index | named scale | `--z-modal`, `--z-tooltip` |
| Boolean attr | no value | `checked`, `disabled`, `required` |
| **BEM `__` element** | **❌ FORBIDDEN** | ~~`.card__title`~~ |
| **BEM `--` modifier** | **❌ FORBIDDEN** | ~~`.btn--primary`~~ |
| **Class as JS hook** | **❌ FORBIDDEN** | ~~`.js-send-btn`~~ |

---

## 27. References & Further Reading

| Resource | URL |
|----------|-----|
| **W3C HTML Living Standard** | https://html.spec.whatwg.org |
| **MDN Web Docs — HTML** | https://developer.mozilla.org/en-US/docs/Web/HTML |
| **MDN Web Docs — CSS** | https://developer.mozilla.org/en-US/docs/Web/CSS |
| **SMACSS** | http://smacss.com |
| **Every Layout** | https://every-layout.dev |
| **CSS Custom Properties** | https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties |
| **Tailwind CSS** | https://tailwindcss.com |
| **CSS Modules** | https://github.com/css-modules/css-modules |
| **Sass / SCSS Docs** | https://sass-lang.com/documentation/ |
| **W3C ARIA Authoring Practices** | https://www.w3.org/WAI/ARIA/apg/ |
| **Google HTML/CSS Style Guide** | https://google.github.io/styleguide/htmlcssguide.html |
| **Every Layout (CSS layout patterns)** | https://every-layout.dev |
| **CSS Architecture (Harry Roberts)** | https://cssguidelin.es |
| **Open Props (CSS vars system)** | https://open-props.style |

### Recommended linting tools

```json
// .stylelintrc.json
{
    "extends": [
        "stylelint-config-standard",
        "stylelint-config-standard-scss"
    ],
    "plugins": [
        "stylelint-order"
    ],
    "rules": {
        "selector-class-pattern": "^[a-z][a-z0-9]*(-[a-z0-9]+)*$",
        "custom-property-pattern": "^([a-z][a-z0-9]*)(-[a-z0-9]+)*$",
        "selector-id-pattern": "^[a-z][a-z0-9-]*$",
        "color-no-invalid-hex": true,
        "declaration-no-important": [true, { "severity": "warning" }],
        "selector-max-id": 0,
        "selector-no-qualifying-type": [true, { "ignore": ["attribute"] }],
        "order/properties-order": ["position", "top", "right", "bottom", "left",
            "z-index", "display", "flex", "grid", "width", "height",
            "margin", "padding", "background", "border", "color",
            "font", "transition", "animation"]
    }
}
```

> **Note:** The pattern `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` enforces single-hyphen kebab-case and explicitly rejects double-underscore (`__`) and double-hyphen (`--`) BEM separators. The `stylelint-selector-bem-pattern` plugin is not used and should not be added.

```json
// .htmlhintrc
{
    "doctype-first": true,
    "doctype-html5": true,
    "attr-lowercase": true,
    "attr-value-double-quotes": true,
    "tag-self-close": false,
    "id-class-ad-disabled": true,
    "id-unique": true,
    "src-not-empty": true,
    "alt-require": true,
    "space-tab-mixed-disabled": "space",
    "id-class-value": "dash"
}
```

---

*Last updated: 2026 — Based on HTML Living Standard, CSS Cascade Level 5, ITCSS, SMACSS. BEM removed as of this revision — see §10 and §25.*
