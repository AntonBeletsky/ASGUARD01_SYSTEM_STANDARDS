# HTML + CSS Naming Conventions — The Complete Guide

> Covers W3C standards, BEM, SMACSS, OOCSS, ITCSS, Atomic CSS, Tailwind, CSS Modules, and modern HTML5/CSS3 best practices.

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
10. [BEM Methodology](#10-bem-methodology)
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
- **Use hyphens as separators** — `user-profile`, not `userProfile` or `user_profile` (in HTML and plain CSS). Exception: BEM uses double underscores and double hyphens.
- **Be descriptive, not presentational** — `btn-primary` over `btn-blue`, `alert-error` over `alert-red`.
- **Separate structure from style from behavior** — HTML = content, CSS = presentation, JS = behavior. Never mix.
- **Avoid ID selectors in CSS** — IDs are for JavaScript hooks and fragment links, not styling.
- **Mobile-first** — write base styles for mobile, override with `min-width` media queries.
- **Follow a methodology** — BEM is the most widely adopted. Pick one and stick to it project-wide.
- **Semantic HTML first** — use the right element before adding classes: `<nav>`, `<article>`, `<button>`, `<header>`.
- **No inline styles** — except for dynamic values injected via JS/CSS custom properties.

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
    class="form__input"
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
- JavaScript anchor points
- Form label associations (`for` / `id`)
- Fragment links (`#section`)
- ARIA references (`aria-labelledby`, `aria-describedby`)

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
<div id="the-really-long-section-that-describes-everything">...</div> <!-- too long -->
```

### ID naming patterns

| Purpose | Example |
|---------|---------|
| Page sections | `#hero`, `#about`, `#services`, `#contact` |
| Modal dialogs | `#modal-login`, `#modal-confirm-delete` |
| Form elements | `#input-email`, `#input-password`, `#select-country` |
| Form labels & errors | `#label-email`, `#error-email`, `#hint-password` |
| Navigation | `#nav-main`, `#nav-breadcrumb` |
| Skip links | `#main-content`, `#main-nav` |
| ARIA targets | `#description-{context}`, `#title-{context}` |

---

## 4. HTML — Class Names

Use **kebab-case**. Classes are the primary styling hook.

### General rules

```html
<!-- ✅ Good — kebab-case, semantic, methodology-based (BEM here) -->
<nav class="nav nav--primary">
    <ul class="nav__list">
        <li class="nav__item nav__item--active">
            <a class="nav__link" href="/">Home</a>
        </li>
    </ul>
</nav>

<div class="card card--featured">
    <img class="card__image" src="..." alt="...">
    <div class="card__body">
        <h2 class="card__title">Title</h2>
        <p class="card__description">Description text.</p>
    </div>
    <div class="card__footer">
        <button class="btn btn--primary">Read more</button>
    </div>
</div>

<!-- ❌ Bad -->
<div class="Card">...</div>              <!-- PascalCase -->
<div class="cardItem">...</div>          <!-- camelCase -->
<div class="card_item">...</div>         <!-- underscore (unless BEM modifier) -->
<div class="red-box big">...</div>       <!-- presentational, vague -->
<div class="div1">...</div>              <!-- meaningless -->
<div class="style1">...</div>            <!-- meaningless -->
```

### Semantic class naming (no methodology)

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

<!-- ✅ State classes — adjective or verb -->
<li class="is-active">
<div class="is-open">
<button class="is-loading">
<input class="is-invalid">
<div class="is-hidden">
<button class="is-disabled">
<li class="is-selected">
<div class="is-expanded">
<div class="is-collapsed">
<div class="has-error">
<div class="has-children">

<!-- ✅ Modifier classes — descriptive adjective -->
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

Use **`data-kebab-case`**. For passing data to JavaScript without IDs or classes:

```html
<!-- ✅ Good — data-{component}-{property} pattern -->
<div
    class="carousel"
    data-carousel
    data-autoplay="true"
    data-interval="5000"
    data-slides-per-view="3"
>
    <div class="carousel__slide" data-slide-index="0">...</div>
    <div class="carousel__slide" data-slide-index="1">...</div>
</div>

<button
    class="btn btn--danger"
    data-action="delete"
    data-confirm="Are you sure?"
    data-target="#item-42"
    data-item-id="42"
    data-item-type="user"
>
    Delete
</button>

<form
    data-validate
    data-submit-url="/api/contact"
    data-success-message="Thanks!"
>
    <input
        type="email"
        data-validate-rule="email"
        data-validate-required="true"
        data-error-message="Please enter a valid email"
    >
</form>

<!-- ✅ JS hooks — data-js-{component} separates JS from CSS hooks -->
<div class="modal" data-js-modal data-js-modal-id="login">...</div>
<button data-js-toggle="modal" data-js-target="login">Sign in</button>


<!-- ❌ Bad -->
<div data-myData="value">        <!-- camelCase in HTML attribute -->
<div data-MyComponent="true">   <!-- PascalCase -->
<div data-d="42">               <!-- cryptic -->
<div dataId="42">               <!-- missing 'data-' prefix -->
```

### Common data attribute patterns

```html
<!-- Component config -->
data-{component}                        <!-- presence = initialized -->
data-{component}-{option}="value"       <!-- component options -->
data-{component}-{sub-component}        <!-- sub-component reference -->

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
/* ✅ Best — class selectors */
.nav {}
.nav__item {}
.btn--primary {}

/* ✅ Acceptable — element selectors for base styles */
a {}
button {}
input {}
h1, h2, h3 {}

/* ⚠️ Use sparingly — attribute selectors */
[type="text"] {}
[aria-expanded="true"] {}
[data-theme="dark"] {}

/* ⚠️ Avoid — ID selectors in CSS (use for JS only) */
#header {}          /* high specificity, hard to override */
#main-nav {}

/* ❌ Never — inline styles */
<div style="color: red">

/* ❌ Avoid — overly qualified selectors */
div.card {}         /* why div? just .card */
ul.nav__list {}     /* just .nav__list */
header nav {}       /* too coupled to HTML structure */
```

### State selectors — use `.is-*` or `.has-*` classes + `:pseudo-classes`

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

/* ✅ JS-controlled state classes */
.modal.is-open {}
.nav__item.is-active {}
.btn.is-loading {}
.form__input.is-invalid {}
.accordion.is-expanded {}
.sidebar.is-hidden {}

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
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);

    /* Z-index (see Section 19) */
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
/* ✅ Scope custom properties to component for easy theming */
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

.btn--secondary {
    --btn-bg: transparent;
    --btn-color: var(--color-primary);
    --btn-border: var(--color-primary);
}

.btn--large {
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

## 10. BEM Methodology

**Block Element Modifier** — the most widely adopted CSS naming system.

### Syntax

```
.block {}
.block__element {}
.block--modifier {}
.block__element--modifier {}
```

### Rules

- **Block** — standalone component. Noun: `.card`, `.nav`, `.btn`, `.modal`.
- **Element** — part of a block, no standalone meaning. Noun: `.card__title`, `.nav__item`.
- **Modifier** — variant or state. Adjective/noun: `.card--featured`, `.btn--primary`.
- **Double underscore** `__` separates block from element.
- **Double hyphen** `--` separates block/element from modifier.
- **Never nest beyond one level** — `.card__header__title` is WRONG → use `.card__title` instead.

```html
<!-- ✅ BEM in action -->

<!-- Card component -->
<div class="card card--featured">
    <img class="card__image" src="..." alt="...">
    <div class="card__body">
        <span class="card__tag">Technology</span>
        <h2 class="card__title">Article Title</h2>
        <p class="card__excerpt">Short description...</p>
    </div>
    <div class="card__footer">
        <time class="card__date">Jan 15, 2025</time>
        <a class="card__link btn btn--sm" href="#">Read more</a>
    </div>
</div>

<!-- Navigation -->
<nav class="nav">
    <ul class="nav__list">
        <li class="nav__item nav__item--active">
            <a class="nav__link" href="/">Home</a>
        </li>
        <li class="nav__item nav__item--has-dropdown">
            <a class="nav__link nav__link--parent" href="/products">
                Products
            </a>
            <ul class="nav__dropdown">
                <li class="nav__dropdown-item">
                    <a class="nav__dropdown-link" href="/products/web">Web</a>
                </li>
            </ul>
        </li>
    </ul>
</nav>

<!-- Form -->
<form class="form">
    <div class="form__group form__group--required">
        <label class="form__label" for="input-email">Email</label>
        <input
            class="form__input form__input--error"
            id="input-email"
            type="email"
        >
        <span class="form__error">Invalid email address.</span>
    </div>
    <button class="form__submit btn btn--primary">Submit</button>
</form>
```

```css
/* ✅ BEM CSS */

/* Block */
.card {
    background: white;
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow);
    overflow: hidden;
}

/* Block modifier */
.card--featured {
    border: 2px solid var(--color-primary);
}

/* Elements */
.card__image {
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: cover;
}

.card__body {
    padding: var(--space-4);
}

.card__title {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-bold);
    margin: 0 0 var(--space-2);
}

/* Element modifier */
.card__title--large {
    font-size: var(--font-size-2xl);
}
```

### BEM — common mistakes

```html
<!-- ❌ Nesting beyond one level -->
<div class="card__body__title">          <!-- WRONG -->
<div class="card__body__footer__link">   <!-- WRONG -->

<!-- ✅ Flatten the structure -->
<div class="card__title">
<div class="card__footer-link">


<!-- ❌ Modifier without block class -->
<div class="card--featured">             <!-- WRONG — missing base .card -->

<!-- ✅ Always include base class too -->
<div class="card card--featured">


<!-- ❌ Using state classes instead of BEM modifiers for permanent variants -->
<button class="btn is-primary">          <!-- mix of approaches -->

<!-- ✅ BEM for variants, is-* for JS states -->
<button class="btn btn--primary">                <!-- variant = BEM modifier -->
<button class="btn btn--primary is-loading">     <!-- state = is-* class -->
```

---

## 11. SMACSS Methodology

**Scalable and Modular Architecture for CSS** — categorizes CSS into 5 types:

```
Base       — element defaults (no class)
Layout     — l- prefix
Module     — no prefix (component)
State      — is- prefix
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

/* Module — reusable components, no prefix */
.nav {}
.card {}
.btn {}
.modal {}
.badge {}

/* State — is- prefix, JS-controlled states */
.is-active {}
.is-hidden {}
.is-loading {}
.is-expanded {}
.is-invalid {}
.is-disabled {}
.has-error {}
.has-overlay {}

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
.media__image {}
.media__body {}

.flag {}                /* like media but vertically centered */
.flag__image {}
.flag__body {}

/* ✅ Skin — visual appearance */
.box {}                 /* generic content box */
.box--rounded {}
.box--shadowed {}
.box--bordered {}

/* ✅ Separate: don't tie skin to container */
/* ❌ Bad OOCSS — skin depends on location */
.sidebar .widget { background: white; }
.footer .widget { background: gray; }

/* ✅ Good OOCSS — reusable skin classes */
.widget {}
.widget--light { background: white; }
.widget--dark { background: gray; }
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
6. Components    — UI components (BEM)
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
.o-ratio__content { position: absolute; inset: 0; }

/* 6. Components — c- prefix (or no prefix with BEM) */
/* _components.card.css, _components.nav.css */
.c-card {}      /* or just .card {} if no prefix */
.c-btn {}
.c-nav {}

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

/* Modifier — still camelCase */
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

// ✅ SCSS with BEM using & operator
.card {
    background: white;
    border-radius: var(--border-radius-lg);

    // BEM modifier
    &--featured {
        border: 2px solid var(--color-primary);
    }

    // BEM elements
    &__image {
        width: 100%;
        object-fit: cover;
    }

    &__body {
        padding: var(--space-4);
    }

    &__title {
        font-size: var(--font-size-xl);

        // Modifier on element
        &--large {
            font-size: var(--font-size-2xl);
        }
    }

    // State
    &.is-loading {
        opacity: 0.6;
    }

    // Responsive inside component
    @include respond-to('md') {
        display: grid;
        grid-template-columns: 1fr 2fr;
    }
}

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

Use **kebab-case** for keyframe names:

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

@keyframes slide-in-up {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes slide-out-left {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(-100%); opacity: 0; }
}

@keyframes scale-in {
    from { transform: scale(0.9); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-8px); }
    75% { transform: translateX(8px); }
}

@keyframes skeleton-loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}


/* ✅ Animation custom properties */
:root {
    --animation-fade-in: fade-in 200ms ease forwards;
    --animation-slide-up: slide-in-up 300ms ease forwards;
    --animation-spin: spin 1s linear infinite;
    --animation-pulse: pulse 2s ease-in-out infinite;
}

/* ✅ Usage */
.modal {
    animation: var(--animation-fade-in);
}

.spinner {
    animation: var(--animation-spin);
}

/* ✅ Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

---

## 18. CSS — Media Queries & Breakpoints

Use **named breakpoints via CSS custom properties or Sass variables**:

```css
/* ✅ Breakpoint naming — t-shirt sizes (most common) */
:root {
    --bp-xs: 480px;    /* Extra small phones */
    --bp-sm: 640px;    /* Small phones */
    --bp-md: 768px;    /* Tablets */
    --bp-lg: 1024px;   /* Laptops */
    --bp-xl: 1280px;   /* Desktops */
    --bp-2xl: 1536px;  /* Large desktops */
}

/* ✅ Mobile-first — min-width */
/* Base: mobile styles */
.container {
    width: 100%;
    padding: 0 var(--space-4);
}

/* ✅ sm+ */
@media (min-width: 640px) {
    .container { padding: 0 var(--space-6); }
}

/* ✅ md+ */
@media (min-width: 768px) {
    .container { max-width: 768px; margin: 0 auto; }
}

/* ✅ lg+ */
@media (min-width: 1024px) {
    .container { max-width: 1024px; }
}

/* ✅ xl+ */
@media (min-width: 1280px) {
    .container { max-width: 1280px; }
}


/* ✅ Feature queries */
@supports (display: grid) {
    .layout { display: grid; }
}

@supports (backdrop-filter: blur(10px)) {
    .glass { backdrop-filter: blur(10px); }
}

/* ✅ User preference queries */
@media (prefers-color-scheme: dark) { ... }
@media (prefers-reduced-motion: reduce) { ... }
@media (prefers-contrast: high) { ... }
@media (prefers-reduced-data: reduce) { ... }
@media print { ... }
```

---

## 19. CSS — Z-index Scale

Never use magic numbers. Use a named scale:

```css
:root {
    --z-below:    -1;    /* Behind everything */
    --z-base:      0;    /* Default flow */
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
    <div class="form__group">
        <label class="form__label" for="input-full-name">
            Full name
            <span class="form__required" aria-hidden="true">*</span>
        </label>
        <input
            class="form__input"
            id="input-full-name"
            type="text"
            name="full_name"
            autocomplete="name"
            required
            aria-required="true"
            aria-describedby="hint-full-name error-full-name"
        >
        <span class="form__hint" id="hint-full-name">
            Enter your first and last name.
        </span>
        <span class="form__error" id="error-full-name" role="alert" aria-live="polite">
            <!-- Error message injected by JS -->
        </span>
    </div>

    <div class="form__group">
        <label class="form__label" for="input-email">Email address</label>
        <input
            class="form__input"
            id="input-email"
            type="email"
            name="email"
            autocomplete="email"
            required
            aria-required="true"
            aria-describedby="error-email"
        >
        <span class="form__error" id="error-email" role="alert" aria-live="polite"></span>
    </div>

    <div class="form__group">
        <label class="form__label" for="select-subject">Subject</label>
        <select
            class="form__select"
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

    <div class="form__group">
        <label class="form__label" for="textarea-message">Message</label>
        <textarea
            class="form__textarea"
            id="textarea-message"
            name="message"
            rows="5"
            required
            aria-describedby="hint-message"
        ></textarea>
        <span class="form__hint" id="hint-message">Minimum 20 characters.</span>
    </div>

    <div class="form__group form__group--checkbox">
        <input
            class="form__checkbox"
            id="check-newsletter"
            type="checkbox"
            name="newsletter"
            value="1"
        >
        <label class="form__label form__label--checkbox" for="check-newsletter">
            Subscribe to newsletter
        </label>
    </div>

    <div class="form__actions">
        <button class="btn btn--primary" type="submit">Send message</button>
        <button class="btn btn--ghost" type="reset">Clear</button>
    </div>
</form>
```

---

## 25. Naming Anti-patterns

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
<div class="alert alert--error">
<div class="card">
<div class="heading-large">
<aside class="sidebar">
<aside class="sidebar--secondary">
<button class="btn btn--success">
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
<div class="card__inner">
<div class="section-outer">
<div class="form-field">
<div class="nav__item">
```

### ❌ Using IDs for styling

```css
/* ❌ Bad — high specificity, breaks cascade */
#header { background: blue; }
#main-nav a { color: white; }
#sidebar { width: 280px; }

/* ✅ Good — use classes */
.site-header { background: blue; }
.main-nav__link { color: white; }
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

### ❌ Nested BEM elements

```html
<!-- ❌ Bad — double nesting -->
<div class="card__body__title">
<div class="nav__list__item__link">

<!-- ✅ Good — flat BEM -->
<div class="card__title">
<div class="nav__link">
```

---

## 26. Quick Reference Cheatsheet

| Item | Convention | Example |
|------|-----------|---------|
| HTML tag | lowercase | `<div>`, `<section>`, `<nav>` |
| HTML attribute | lowercase kebab | `aria-label`, `data-user-id` |
| ID | kebab-case | `#user-profile`, `#modal-login` |
| Class (general) | kebab-case | `.user-card`, `.nav-item` |
| BEM Block | kebab-case noun | `.card`, `.nav`, `.btn` |
| BEM Element | `block__element` | `.card__title`, `.nav__item` |
| BEM Modifier | `block--modifier` | `.card--featured`, `.btn--primary` |
| BEM Element Modifier | `block__el--modifier` | `.nav__item--active` |
| State class | `.is-*` or `.has-*` | `.is-active`, `.has-error` |
| Layout class (SMACSS) | `.l-*` | `.l-container`, `.l-grid` |
| Object class (ITCSS) | `.o-*` | `.o-stack`, `.o-media` |
| Utility class | `.u-*` or abbreviation | `.u-hidden`, `.sr-only` |
| JS hook | `data-js-*` | `data-js-modal`, `data-js-toggle` |
| Custom property | `--kebab-case` | `--color-primary`, `--space-4` |
| Semantic token | `--{category}-{name}` | `--color-text-primary` |
| Primitive token | `--palette-{color}-{scale}` | `--palette-blue-500` |
| CSS component var | `--{block}-{property}` | `--btn-bg`, `--card-padding` |
| SCSS variable | `$kebab-case` | `$color-primary` |
| SCSS mixin | `@mixin kebab-case` | `@mixin flex-center` |
| SCSS function | `@function kebab-case` | `@function rem()` |
| SCSS placeholder | `%kebab-case` | `%visually-hidden` |
| Keyframe | kebab-case verb | `fade-in`, `slide-in-up`, `spin` |
| CSS Modules class | camelCase | `.cardWrapper`, `.navItem` |
| Web component | `hyphenated-name` | `<user-card>`, `<nav-bar>` |
| File (CSS) | kebab-case | `_components.card.scss` |
| File (SCSS partial) | `_underscore-prefix` | `_variables.scss` |
| Breakpoint | t-shirt size | `xs`, `sm`, `md`, `lg`, `xl`, `2xl` |
| Z-index | named scale | `--z-modal`, `--z-tooltip` |
| Boolean attr | no value | `checked`, `disabled`, `required` |

---

## 27. References & Further Reading

| Resource | URL |
|----------|-----|
| **W3C HTML Living Standard** | https://html.spec.whatwg.org |
| **MDN Web Docs — HTML** | https://developer.mozilla.org/en-US/docs/Web/HTML |
| **MDN Web Docs — CSS** | https://developer.mozilla.org/en-US/docs/Web/CSS |
| **BEM Official Documentation** | https://getbem.com |
| **SMACSS** | http://smacss.com |
| **ITCSS (Harry Roberts)** | https://csswizardry.com/2018/11/itcss-and-bem/ |
| **Every Layout** | https://every-layout.dev |
| **CSS Custom Properties** | https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties |
| **Tailwind CSS** | https://tailwindcss.com |
| **CSS Modules** | https://github.com/css-modules/css-modules |
| **Sass / SCSS Docs** | https://sass-lang.com/documentation/ |
| **W3C ARIA Authoring Practices** | https://www.w3.org/WAI/ARIA/apg/ |
| **Google HTML/CSS Style Guide** | https://google.github.io/styleguide/htmlcssguide.html |
| **Airbnb CSS/Sass Style Guide** | https://github.com/airbnb/css |
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
        "stylelint-selector-bem-pattern",
        "stylelint-order"
    ],
    "rules": {
        "selector-class-pattern": "^([a-z][a-z0-9]*)(-[a-z0-9]+)*(__[a-z0-9]+(-[a-z0-9]+)*)?(--[a-z0-9]+(-[a-z0-9]+)*)?$",
        "custom-property-pattern": "^([a-z][a-z0-9]*)(-[a-z0-9]+)*$",
        "selector-id-pattern": "^[a-z][a-z0-9-]*$",
        "color-no-invalid-hex": true,
        "declaration-no-important": [true, { "severity": "warning" }],
        "selector-max-id": 0,
        "order/properties-order": ["position", "top", "right", "bottom", "left",
            "z-index", "display", "flex", "grid", "width", "height",
            "margin", "padding", "background", "border", "color",
            "font", "transition", "animation"]
    }
}
```

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

*Last updated: 2026 — Based on HTML Living Standard, CSS Cascade Level 5, BEM, ITCSS, SMACSS*
