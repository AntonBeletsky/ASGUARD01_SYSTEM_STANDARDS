# Universal Theme HTML Guide — Bootstrap 5.3
> How to write HTML and CSS so your site works perfectly on **any** light or dark theme — without hardcoded colors.

---

## 1. The Core Principle: Never Hardcode Colors

Bootstrap 5.3 ships with a full token system that automatically adapts to the active theme (`light`, `dark`, or any custom one). The rule is simple:

| ❌ Hardcoded — breaks on theme change | ✅ Adaptive — works on any theme |
|---|---|
| `bg-white` | `bg-body` |
| `bg-dark` | `bg-body-tertiary` |
| `text-dark` | `text-body` |
| `text-white` | `text-body-emphasis` |
| `style="color:#212529"` | `style="color: var(--bs-body-color)"` |
| `style="background:#fff"` | `style="background: var(--bs-body-bg)"` |

The theme is controlled by a single attribute on `<html>`:

```html
<html data-bs-theme="light">   <!-- or "dark", or any custom value -->
```

Switching themes is one attribute change. If your HTML uses adaptive classes and variables — everything updates instantly.

---

## 2. The `data-bs-theme` System

### Global theme
```html
<html lang="en" data-bs-theme="dark">
```

### Per-component theme (scoped)
Any element can override the theme for itself and its children:
```html
<nav class="navbar" data-bs-theme="dark">...</nav>
<div class="card" data-bs-theme="light">...</div>
```

### Toggle with JS (one-liner)
```js
const html = document.documentElement;
html.setAttribute('data-bs-theme',
  html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark'
);
```

### Respect OS preference automatically
```js
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
document.documentElement.setAttribute('data-bs-theme', prefersDark ? 'dark' : 'light');
```

---

## 3. Adaptive Background Classes

Use these instead of `bg-white`, `bg-dark`, `bg-light`:

| Class | Adapts? | Use for |
|---|---|---|
| `bg-body` | ✅ | Main page background, cards, panels |
| `bg-body-secondary` | ✅ | Slightly offset backgrounds, sidebars |
| `bg-body-tertiary` | ✅ | Subtle sections, table stripes, headers |
| `bg-primary` | ✅* | Primary brand color (uses theme vars) |
| `bg-primary-subtle` | ✅ | Tinted primary bg (alerts, badges, tags) |
| `bg-secondary-subtle` | ✅ | Muted secondary tint |
| `bg-success-subtle` | ✅ | Success tint |
| `bg-danger-subtle` | ✅ | Error/danger tint |
| `bg-warning-subtle` | ✅ | Warning tint |
| `bg-info-subtle` | ✅ | Info tint |
| `bg-dark` | ⚠️ | Fixed dark — use only intentionally |
| `bg-white` | ⚠️ | Fixed white — avoid for surfaces |
| `bg-black` | ⚠️ | Fixed black — decorative only |
| `bg-transparent` | ✅ | Always transparent |

> **`bg-body` is your default surface.** It equals `--bs-body-bg`, which switches automatically.

---

## 4. Adaptive Text Classes

| Class | Adapts? | Use for |
|---|---|---|
| `text-body` | ✅ | Default body text |
| `text-body-secondary` | ✅ | Muted/secondary text (replaces `text-muted`) |
| `text-body-tertiary` | ✅ | Placeholder, disabled-like text |
| `text-body-emphasis` | ✅ | Strong/heading text, max contrast |
| `text-primary` | ✅ | Primary brand text |
| `text-primary-emphasis` | ✅ | Dark-adjusted primary text |
| `text-secondary-emphasis` | ✅ | Dark-adjusted secondary text |
| `text-success-emphasis` | ✅ | Success text (for subtle bg contexts) |
| `text-danger-emphasis` | ✅ | Danger text (for subtle bg contexts) |
| `text-warning-emphasis` | ✅ | Warning text (for subtle bg contexts) |
| `text-info-emphasis` | ✅ | Info text (for subtle bg contexts) |
| `text-muted` | ⚠️ | Deprecated in 5.3, use `text-body-secondary` |
| `text-dark` | ⚠️ | Fixed dark — breaks on dark theme |
| `text-white` | ⚠️ | Fixed white — use only on intentionally dark surfaces |

---

## 5. Adaptive Border Classes

| Class | Adapts? | Notes |
|---|---|---|
| `border` | ✅ | Uses `--bs-border-color` |
| `border-primary` | ✅ | Brand border |
| `border-primary-subtle` | ✅ | Tinted, for subtle bg cards |
| `border-secondary-subtle` | ✅ | |
| `border-success-subtle` | ✅ | |
| `border-danger-subtle` | ✅ | |
| `border-warning-subtle` | ✅ | |
| `border-info-subtle` | ✅ | |
| `border-light` | ⚠️ | Fixed light color |
| `border-dark` | ⚠️ | Fixed dark color |

---

## 6. The Subtle Color Trio Pattern

Bootstrap 5.3 introduces a powerful 3-part system for semantic sections. Use all three together:

```html
<!-- ✅ Correct: alert-style box that works on any theme -->
<div class="p-3 rounded
            text-primary-emphasis
            bg-primary-subtle
            border border-primary-subtle">
  This adapts to light and dark automatically.
</div>

<!-- Works for all semantic colors: -->
<!-- text-{color}-emphasis + bg-{color}-subtle + border-{color}-subtle -->
<!-- Colors: primary, secondary, success, danger, warning, info, light, dark -->
```

---

## 7. Key CSS Custom Properties (Variables)

Use these in your own CSS instead of hardcoded values.

### Background tokens
```css
background-color: var(--bs-body-bg);          /* Main surface */
background-color: var(--bs-secondary-bg);     /* Offset surface */
background-color: var(--bs-tertiary-bg);      /* Subtle surface */
```

### Text tokens
```css
color: var(--bs-body-color);            /* Default text */
color: var(--bs-secondary-color);       /* Muted text */
color: var(--bs-tertiary-color);        /* Even more muted */
color: var(--bs-emphasis-color);        /* Maximum contrast text */
```

### Border tokens
```css
border-color: var(--bs-border-color);           /* Default border */
border-color: var(--bs-border-color-translucent); /* Subtle border */
```

### Brand color tokens
```css
color: var(--bs-primary);
color: var(--bs-secondary);
color: var(--bs-success);
color: var(--bs-danger);
color: var(--bs-warning);
color: var(--bs-info);
```

### Semantic emphasis + subtle tokens (dark-mode aware)
```css
/* These flip values in dark mode automatically */
color: var(--bs-primary-text-emphasis);
background-color: var(--bs-primary-bg-subtle);
border-color: var(--bs-primary-border-subtle);

/* Same pattern for: secondary, success, danger, warning, info */
```

### Typography tokens
```css
font-family: var(--bs-font-sans-serif);
font-family: var(--bs-font-monospace);
font-size: var(--bs-body-font-size);      /* 1rem */
font-weight: var(--bs-body-font-weight);
line-height: var(--bs-body-line-height);
```

### Link tokens
```css
color: var(--bs-link-color);
color: var(--bs-link-hover-color);
```

### Component tokens
```css
/* Border radius */
border-radius: var(--bs-border-radius);       /* 0.375rem */
border-radius: var(--bs-border-radius-sm);
border-radius: var(--bs-border-radius-lg);
border-radius: var(--bs-border-radius-xl);
border-radius: var(--bs-border-radius-xxl);
border-radius: var(--bs-border-radius-pill);

/* Border */
border-width: var(--bs-border-width);         /* 1px */
border-style: var(--bs-border-style);         /* solid */

/* Shadow */
box-shadow: var(--bs-box-shadow);
box-shadow: var(--bs-box-shadow-sm);
box-shadow: var(--bs-box-shadow-lg);
```

---

## 8. Writing Theme-Safe Custom CSS

```css
/* ✅ Theme-safe custom component */
.my-panel {
  background-color: var(--bs-body-bg);
  color: var(--bs-body-color);
  border: var(--bs-border-width) var(--bs-border-style) var(--bs-border-color);
  border-radius: var(--bs-border-radius);
  box-shadow: var(--bs-box-shadow-sm);
}

.my-panel-muted-text {
  color: var(--bs-secondary-color);
}

.my-panel-heading {
  color: var(--bs-emphasis-color);
}

/* ✅ Semi-transparent overlay using RGB vars */
.my-overlay {
  background-color: rgba(var(--bs-body-bg-rgb), 0.85);
}

/* ✅ Adding a custom theme (any number of themes!) */
[data-bs-theme="ocean"] {
  --bs-body-bg: #0a192f;
  --bs-body-color: #ccd6f6;
  --bs-primary: #64ffda;
  /* override any other BS variable here */
}
```

---

## 9. Component Cheatsheet — Adaptive vs. Hardcoded

### Navbar
```html
<!-- ✅ Adaptive -->
<nav class="navbar bg-body-tertiary">...</nav>

<!-- ✅ Scoped dark navbar regardless of page theme -->
<nav class="navbar bg-dark" data-bs-theme="dark">...</nav>
```

### Card
```html
<!-- ✅ Card inherits bg-body, borders adapt -->
<div class="card">
  <div class="card-body">
    <h5 class="card-title text-body-emphasis">Title</h5>
    <p class="card-text text-body-secondary">Muted description</p>
  </div>
</div>
```

### Alert (fully adaptive)
```html
<div class="alert alert-primary" role="alert">...</div>
<!-- All .alert-{color} variants adapt automatically in 5.3 -->
```

### Badge
```html
<span class="badge text-bg-primary">Primary</span>    <!-- adaptive -->
<span class="badge text-bg-secondary">Secondary</span>
<span class="badge text-bg-success">Success</span>
```

### Table
```html
<table class="table">...</table>             <!-- adaptive -->
<table class="table table-striped">...</table>
<!-- Avoid: table-dark on individual rows if the page theme should control it -->
```

### Modal
```html
<!-- Modal adapts automatically — no extra classes needed -->
<div class="modal-content">
  <div class="modal-header">
    <h5 class="modal-title">Title</h5>
  </div>
</div>
```

### Form controls
```html
<!-- ✅ All form controls adapt automatically -->
<input type="text" class="form-control" placeholder="Adaptive input">
<select class="form-select">...</select>
<textarea class="form-control">...</textarea>
```

---

## 10. The RGB Variable Trick

Bootstrap exposes every color as an `*-rgb` twin, enabling `rgba()` with opacity — including adaptive colors:

```css
/* Semi-transparent adaptive surface */
background-color: rgba(var(--bs-body-bg-rgb), 0.9);

/* Semi-transparent primary */
background-color: rgba(var(--bs-primary-rgb), 0.15);

/* Semi-transparent border */
border-color: rgba(var(--bs-emphasis-color-rgb), 0.1);
```

This is how Bootstrap builds subtle tints internally, and you can use it freely.

---

## 11. What to Avoid — Anti-patterns

```html
<!-- ❌ Never do this — hardcoded, breaks dark theme -->
<div style="background-color: #ffffff; color: #212529;">...</div>

<!-- ❌ Hardcoded utility classes -->
<div class="bg-white text-dark">...</div>
<div class="bg-light text-dark">...</div>

<!-- ❌ Deprecated in 5.3 -->
<p class="text-muted">...</p>     <!-- use text-body-secondary -->

<!-- ❌ Mixing text-white with adaptive backgrounds -->
<div class="bg-body text-white">...</div>   <!-- white text on white bg in light mode -->
```

---

## 12. Applying Theme to Non-`<html>` Elements

> **Important:** When you scope a theme to an element (not `<html>` or `<body>`), add `.text-body` and `.bg-body` to force the text and background since HTML elements don't inherit them automatically.

```html
<!-- Scoped dark section inside a light-mode page -->
<section data-bs-theme="dark" class="bg-body text-body p-4">
  <p>This section is dark, rest of page is light.</p>
</section>
```

---

## 13. Quick Decision Reference

**Which class should I use?**

```
Need a background for a content surface?
  → bg-body

Need a slightly offset background (sidebar, header)?
  → bg-body-secondary  or  bg-body-tertiary

Need a semantic tinted background (alert, tag, notice)?
  → bg-{color}-subtle  +  text-{color}-emphasis  +  border-{color}-subtle

Need regular paragraph text?
  → text-body  (or nothing — it's the default)

Need muted / secondary text?
  → text-body-secondary

Need strong heading text?
  → text-body-emphasis

Need a border that adapts?
  → border  (default)  or  border-{color}-subtle

Need a custom CSS color value?
  → var(--bs-body-color), var(--bs-body-bg), etc.
```

---

## 14. Full Custom Theme Skeleton

```css
/* mytheme.css — loaded after bootstrap.css */
[data-bs-theme="mytheme"] {
  color-scheme: light;   /* tell browser: light or dark */

  /* Surface hierarchy */
  --bs-body-bg:             #f0f4f8;
  --bs-body-bg-rgb:         240, 244, 248;
  --bs-secondary-bg:        #dce3ea;
  --bs-tertiary-bg:         #c8d2db;

  /* Text hierarchy */
  --bs-body-color:          #1a202c;
  --bs-body-color-rgb:      26, 32, 44;
  --bs-secondary-color:     rgba(26, 32, 44, 0.65);
  --bs-tertiary-color:      rgba(26, 32, 44, 0.4);
  --bs-emphasis-color:      #000;

  /* Brand */
  --bs-primary:             #5a67d8;
  --bs-primary-rgb:         90, 103, 216;

  /* Borders */
  --bs-border-color:        #b2bec3;
  --bs-border-color-translucent: rgba(26, 32, 44, 0.15);

  /* Links */
  --bs-link-color:          #5a67d8;
  --bs-link-hover-color:    #434190;
}
```

Switch to it with:
```html
<html data-bs-theme="mytheme">
```

Or toggle it per-section:
```html
<div data-bs-theme="mytheme" class="bg-body text-body">...</div>
```

---

## Summary

| Goal | Use |
|---|---|
| Adaptive page background | `bg-body` / `var(--bs-body-bg)` |
| Offset section background | `bg-body-secondary` or `bg-body-tertiary` |
| Semantic tinted background | `bg-{color}-subtle` |
| Default text | `text-body` / `var(--bs-body-color)` |
| Muted text | `text-body-secondary` |
| Strong text | `text-body-emphasis` |
| Semantic text (on subtle bg) | `text-{color}-emphasis` |
| Border | `border` or `border-{color}-subtle` |
| Theme switching | `data-bs-theme="light\|dark\|custom"` on any element |
| Custom CSS colors | Always use `var(--bs-*)` tokens |
| Semi-transparent | `rgba(var(--bs-*-rgb), 0.5)` |
