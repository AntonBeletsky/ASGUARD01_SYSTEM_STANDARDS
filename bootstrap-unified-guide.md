# Bootstrap Unified HTML Template Development Guide

> **Core Philosophy:** Prefer Bootstrap utility classes over custom CSS. Accept minor visual approximations (e.g., `p-2` ≈ 8px instead of an exact 7px) in exchange for consistency, maintainability, and design system coherence. Pixel-perfect custom values are the exception, not the rule.

---

## Table of Contents

1. [Why Utility-First?](#1-why-utility-first)
2. [Spacing System](#2-spacing-system)
3. [Typography](#3-typography)
4. [Colors & Backgrounds](#4-colors--backgrounds)
5. [Layout & Grid](#5-layout--grid)
6. [Flexbox & Alignment](#6-flexbox--alignment)
7. [Sizing (Width & Height)](#7-sizing-width--height)
8. [Borders & Rounded Corners](#8-borders--rounded-corners)
9. [Shadows & Opacity](#9-shadows--opacity)
10. [Display & Visibility](#10-display--visibility)
11. [Position & Z-Index](#11-position--z-index)
12. [Components — Bootstrap vs Custom](#12-components--bootstrap-vs-custom)
13. [When Custom CSS Is Acceptable](#13-when-custom-css-is-acceptable)
14. [Decision Tree](#14-decision-tree)
15. [Anti-Patterns to Avoid](#15-anti-patterns-to-avoid)
16. [Code Review Checklist](#16-code-review-checklist)

---

## 1. Why Utility-First?

Writing custom CSS for every spacing, color, or size decision creates fragmented stylesheets that are hard to maintain. Bootstrap's utility classes enforce a consistent design token system across the entire project.

**Trade-off you must accept:**

| Scenario | Custom CSS | Bootstrap Utility |
|---|---|---|
| You need exactly `17px` padding | `padding: 17px` | `p-2` (= `8px`) or `p-3` (= `16px`) |
| You need exactly `#3a7bd5` blue | `color: #3a7bd5` | `text-primary` (theme blue) |
| You need `font-size: 13px` | `font-size: 13px` | `small` or `fs-6` (≈ `12–14px`) |

Choosing `p-3` over a custom `17px` is **correct behavior**. The goal is system-level consistency, not pixel-level fidelity.

---

## 2. Spacing System

Bootstrap uses a scale of `0–5` (and `auto`) based on a `$spacer` variable (default: `1rem = 16px`).

### Scale Reference

| Class suffix | Value | Pixels (default) |
|---|---|---|
| `0` | `0` | `0px` |
| `1` | `0.25rem` | `4px` |
| `2` | `0.5rem` | `8px` |
| `3` | `1rem` | `16px` |
| `4` | `1.5rem` | `24px` |
| `5` | `3rem` | `48px` |
| `auto` | `auto` | — |

### Padding Classes

```html
<!-- All sides -->
<div class="p-3">...</div>

<!-- Top / Bottom -->
<div class="pt-2 pb-4">...</div>

<!-- Start (left) / End (right) -->
<div class="ps-3 pe-2">...</div>

<!-- Horizontal axis (x) -->
<div class="px-4">...</div>

<!-- Vertical axis (y) -->
<div class="py-2">...</div>
```

### Margin Classes

Same syntax — replace `p` with `m`:

```html
<div class="mt-3 mb-2 mx-auto">...</div>
```

### Negative Margins (Bootstrap 5)

```html
<div class="mt-n2">...</div>  <!-- -0.5rem -->
```

### Rule: Picking the Closest Value

When a design spec says `17px`:
- `p-2` = `8px` (too small)
- `p-3` = `16px` ✅ **use this — closest match**
- `p-4` = `24px` (too large)

Always round to the nearest Bootstrap step. Document the deviation in a comment if the spec is strict.

---

## 3. Typography

### Font Size

```html
<p class="fs-1">Largest (2.5rem)</p>
<p class="fs-2">fs-2 (2rem)</p>
<p class="fs-3">fs-3 (1.75rem)</p>
<p class="fs-4">fs-4 (1.5rem)</p>
<p class="fs-5">fs-5 (1.25rem)</p>
<p class="fs-6">fs-6 (1rem)</p>
```

### Font Weight & Style

```html
<span class="fw-bold">Bold</span>
<span class="fw-semibold">Semibold</span>
<span class="fw-normal">Normal</span>
<span class="fw-light">Light</span>
<span class="fst-italic">Italic</span>
<span class="fst-normal">Normal style</span>
```

### Text Alignment

```html
<p class="text-start">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-end">Right aligned</p>
```

### Text Transform

```html
<span class="text-uppercase">uppercase</span>
<span class="text-lowercase">LOWERCASE</span>
<span class="text-capitalize">capitalize first letter</span>
```

### Line Height

```html
<p class="lh-1">Line height 1</p>
<p class="lh-sm">Small (1.25)</p>
<p class="lh-base">Base (1.5)</p>
<p class="lh-lg">Large (2)</p>
```

### Text Decoration

```html
<a class="text-decoration-none">No underline</a>
<span class="text-decoration-underline">Underlined</span>
<span class="text-decoration-line-through">Strikethrough</span>
```

### Truncation

```html
<p class="text-truncate" style="max-width: 200px;">Long text that will be cut off</p>
```

> **Note:** `text-truncate` is one case where an inline `max-width` is acceptable — it requires a constraint to work.

---

## 4. Colors & Backgrounds

### Text Colors

```html
<p class="text-primary">Primary</p>
<p class="text-secondary">Secondary</p>
<p class="text-success">Success (green)</p>
<p class="text-danger">Danger (red)</p>
<p class="text-warning">Warning (yellow)</p>
<p class="text-info">Info (cyan)</p>
<p class="text-light">Light</p>
<p class="text-dark">Dark</p>
<p class="text-muted">Muted (gray)</p>
<p class="text-white">White</p>
<p class="text-body">Body color</p>
```

### Background Colors

```html
<div class="bg-primary">Primary background</div>
<div class="bg-secondary">Secondary background</div>
<div class="bg-success">Success background</div>
<div class="bg-danger">Danger background</div>
<div class="bg-warning">Warning background</div>
<div class="bg-info">Info background</div>
<div class="bg-light">Light background</div>
<div class="bg-dark">Dark background</div>
<div class="bg-white">White background</div>
<div class="bg-transparent">Transparent</div>
```

### Background + Text Together

Use `text-bg-*` shorthand (Bootstrap 5.2+):

```html
<span class="text-bg-primary p-2">Primary badge</span>
<span class="text-bg-danger p-2">Danger badge</span>
```

### Background Gradient

```html
<div class="bg-primary bg-gradient">Gradient primary</div>
```

### Opacity on Colors (Bootstrap 5.1+)

```html
<div class="text-primary text-opacity-75">75% opacity text</div>
<div class="bg-success bg-opacity-25">25% opacity background</div>
```

---

## 5. Layout & Grid

### Container Types

```html
<!-- Fixed-width breakpoint containers -->
<div class="container">...</div>

<!-- Full-width at all breakpoints -->
<div class="container-fluid">...</div>

<!-- Fluid up to a breakpoint, then fixed -->
<div class="container-sm">...</div>
<div class="container-md">...</div>
<div class="container-lg">...</div>
<div class="container-xl">...</div>
<div class="container-xxl">...</div>
```

### Breakpoints Reference

| Breakpoint | Class infix | Width |
|---|---|---|
| X-Small | *(none)* | `< 576px` |
| Small | `sm` | `≥ 576px` |
| Medium | `md` | `≥ 768px` |
| Large | `lg` | `≥ 992px` |
| X-Large | `xl` | `≥ 1200px` |
| XX-Large | `xxl` | `≥ 1400px` |

### Grid System

Bootstrap grid is 12 columns. Always wrap `col-*` inside a `row`, and `row` inside a `container`.

```html
<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 col-lg-4">Column 1</div>
    <div class="col-12 col-md-6 col-lg-4">Column 2</div>
    <div class="col-12 col-md-12 col-lg-4">Column 3</div>
  </div>
</div>
```

### Auto-layout Columns

```html
<!-- Equal width -->
<div class="row">
  <div class="col">Auto</div>
  <div class="col">Auto</div>
</div>

<!-- One column takes fixed width, others fill -->
<div class="row">
  <div class="col">Fill</div>
  <div class="col-4">Fixed 4</div>
  <div class="col">Fill</div>
</div>
```

### Row Gutters

```html
<!-- Horizontal + vertical gutter -->
<div class="row g-3">...</div>

<!-- Horizontal gutter only -->
<div class="row gx-4">...</div>

<!-- Vertical gutter only -->
<div class="row gy-2">...</div>

<!-- No gutters -->
<div class="row g-0">...</div>
```

### Column Offset

```html
<div class="row">
  <div class="col-md-4 offset-md-4">Centered column</div>
</div>
```

---

## 6. Flexbox & Alignment

### Enable Flex

```html
<div class="d-flex">...</div>
<div class="d-inline-flex">...</div>
```

### Flex Direction

```html
<div class="d-flex flex-row">Horizontal (default)</div>
<div class="d-flex flex-column">Vertical</div>
<div class="d-flex flex-row-reverse">Reversed horizontal</div>
<div class="d-flex flex-column-reverse">Reversed vertical</div>
```

### Justify Content (main axis)

```html
<div class="d-flex justify-content-start">Left</div>
<div class="d-flex justify-content-center">Center</div>
<div class="d-flex justify-content-end">Right</div>
<div class="d-flex justify-content-between">Space between</div>
<div class="d-flex justify-content-around">Space around</div>
<div class="d-flex justify-content-evenly">Space evenly</div>
```

### Align Items (cross axis)

```html
<div class="d-flex align-items-start">Top</div>
<div class="d-flex align-items-center">Middle</div>
<div class="d-flex align-items-end">Bottom</div>
<div class="d-flex align-items-stretch">Stretch (default)</div>
<div class="d-flex align-items-baseline">Baseline</div>
```

### Align Self (individual item)

```html
<div class="d-flex" style="height: 100px;">
  <div class="align-self-start">Top item</div>
  <div class="align-self-center">Middle item</div>
  <div class="align-self-end">Bottom item</div>
</div>
```

### Flex Wrap

```html
<div class="d-flex flex-wrap">Wrap</div>
<div class="d-flex flex-nowrap">No wrap</div>
```

### Flex Fill & Grow/Shrink

```html
<div class="d-flex">
  <div class="flex-fill">Takes equal share</div>
  <div class="flex-fill">Takes equal share</div>
</div>

<div class="flex-grow-1">Grows to fill</div>
<div class="flex-shrink-0">Will not shrink</div>
```

### Gap (Bootstrap 5)

```html
<div class="d-flex gap-3">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

> **Prefer `gap-*` over individual margins on flex children.** It's cleaner and doesn't require removing margin from the last child.

---

## 7. Sizing (Width & Height)

### Width

```html
<div class="w-25">25% width</div>
<div class="w-50">50% width</div>
<div class="w-75">75% width</div>
<div class="w-100">100% width</div>
<div class="w-auto">Auto width</div>
<div class="mw-100">Max-width 100%</div>
```

### Height

```html
<div class="h-25">25% height</div>
<div class="h-50">50% height</div>
<div class="h-75">75% height</div>
<div class="h-100">100% height</div>
<div class="h-auto">Auto height</div>
<div class="mh-100">Max-height 100%</div>
```

### Viewport Units

```html
<div class="min-vw-100">Min viewport width 100</div>
<div class="min-vh-100">Min viewport height 100</div>
<div class="vw-100">Viewport width 100</div>
<div class="vh-100">Viewport height 100</div>
```

---

## 8. Borders & Rounded Corners

### Adding Borders

```html
<div class="border">All sides</div>
<div class="border-top">Top only</div>
<div class="border-end">Right only</div>
<div class="border-bottom">Bottom only</div>
<div class="border-start">Left only</div>
```

### Removing Borders

```html
<div class="border border-0">No borders</div>
<div class="border border-top-0">No top border</div>
```

### Border Colors

```html
<div class="border border-primary">Primary border</div>
<div class="border border-danger">Danger border</div>
<div class="border border-success">Success border</div>
```

### Border Width (Bootstrap 5.1+)

```html
<div class="border border-1">1px</div>
<div class="border border-2">2px</div>
<div class="border border-3">3px</div>
<div class="border border-4">4px</div>
<div class="border border-5">5px</div>
```

### Rounded Corners

```html
<div class="rounded">All corners</div>
<div class="rounded-top">Top corners</div>
<div class="rounded-end">Right corners</div>
<div class="rounded-bottom">Bottom corners</div>
<div class="rounded-start">Left corners</div>
<div class="rounded-circle">Circle (50%)</div>
<div class="rounded-pill">Pill shape</div>
<div class="rounded-0">No rounding</div>
```

### Rounded Size

```html
<div class="rounded-1">Small (0.25rem)</div>
<div class="rounded-2">Default (0.375rem)</div>
<div class="rounded-3">Large (0.5rem)</div>
<div class="rounded-4">Larger (1rem)</div>
<div class="rounded-5">Largest (2rem)</div>
```

---

## 9. Shadows & Opacity

### Box Shadow

```html
<div class="shadow-none">No shadow</div>
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Regular shadow</div>
<div class="shadow-lg">Large shadow</div>
```

### Opacity

```html
<div class="opacity-100">100% (fully visible)</div>
<div class="opacity-75">75%</div>
<div class="opacity-50">50%</div>
<div class="opacity-25">25%</div>
<div class="opacity-0">0% (invisible)</div>
```

---

## 10. Display & Visibility

### Display Values

```html
<div class="d-none">Hidden</div>
<div class="d-block">Block</div>
<div class="d-inline">Inline</div>
<div class="d-inline-block">Inline block</div>
<div class="d-flex">Flex</div>
<div class="d-grid">Grid</div>
<div class="d-table">Table</div>
```

### Responsive Display

```html
<!-- Hidden on mobile, visible from md up -->
<div class="d-none d-md-block">...</div>

<!-- Visible on mobile only -->
<div class="d-block d-md-none">...</div>

<!-- Flex only on lg+ -->
<div class="d-none d-lg-flex">...</div>
```

### Visibility (keeps space)

```html
<div class="visible">Visible</div>
<div class="invisible">Invisible but occupies space</div>
```

### Print Utilities

```html
<div class="d-print-none">Hidden when printing</div>
<div class="d-none d-print-block">Only visible when printing</div>
```

---

## 11. Position & Z-Index

### Position Values

```html
<div class="position-static">Static (default)</div>
<div class="position-relative">Relative</div>
<div class="position-absolute">Absolute</div>
<div class="position-fixed">Fixed</div>
<div class="position-sticky">Sticky</div>
```

### Edge Positioning

Use with `position-absolute` or `position-fixed`:

```html
<div class="position-absolute top-0 start-0">Top left</div>
<div class="position-absolute top-0 end-0">Top right</div>
<div class="position-absolute bottom-0 start-0">Bottom left</div>
<div class="position-absolute bottom-0 end-0">Bottom right</div>
<div class="position-absolute top-50 start-50 translate-middle">Center</div>
```

### Sticky Positioning

```html
<div class="sticky-top">Sticks to top</div>
<div class="sticky-bottom">Sticks to bottom</div>

<!-- Responsive sticky -->
<div class="sticky-sm-top">Sticky from sm up</div>
<div class="sticky-md-top">Sticky from md up</div>
```

### Fixed Positioning

```html
<nav class="fixed-top">Always at top</nav>
<footer class="fixed-bottom">Always at bottom</footer>
```

### Z-Index

```html
<div class="z-0">z-index: 0</div>
<div class="z-1">z-index: 1</div>
<div class="z-2">z-index: 2</div>
<div class="z-3">z-index: 3</div>
<div class="z-n1">z-index: -1</div>
```

### Overflow

```html
<div class="overflow-auto">Auto scroll</div>
<div class="overflow-hidden">Hidden overflow</div>
<div class="overflow-visible">Visible</div>
<div class="overflow-scroll">Always scroll</div>
<div class="overflow-x-auto">Horizontal auto</div>
<div class="overflow-y-hidden">Vertical hidden</div>
```

---

## 12. Components — Bootstrap vs Custom

For all standard UI components, **always use Bootstrap's built-in components** before reaching for custom HTML+CSS.

### Buttons

```html
<!-- ✅ Use Bootstrap button classes -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-outline-secondary">Outline</button>
<button class="btn btn-sm btn-danger">Small danger</button>
<button class="btn btn-lg btn-success">Large success</button>

<!-- ❌ Do NOT invent custom button styles -->
<button style="background: blue; padding: 8px 16px; border-radius: 4px;">...</button>
```

### Cards

```html
<div class="card shadow-sm">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Title</h5>
    <p class="card-text text-muted">Some text.</p>
    <a href="#" class="btn btn-primary">Action</a>
  </div>
  <div class="card-footer text-muted small">Footer</div>
</div>
```

### Alerts

```html
<div class="alert alert-success alert-dismissible fade show" role="alert">
  <strong>Success!</strong> Operation completed.
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

### Badges

```html
<span class="badge text-bg-primary">New</span>
<span class="badge rounded-pill text-bg-danger">99+</span>
```

### Navigation

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container">
    <a class="navbar-brand fw-bold" href="#">Brand</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="#">About</a></li>
      </ul>
    </div>
  </div>
</nav>
```

### Tables

```html
<table class="table table-striped table-hover table-bordered align-middle">
  <thead class="table-dark">
    <tr>
      <th>Name</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Item 1</td>
      <td><span class="badge text-bg-success">Active</span></td>
    </tr>
  </tbody>
</table>
```

### Forms

```html
<form>
  <div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" class="form-control" id="email" placeholder="you@example.com">
    <div class="form-text text-muted">We'll never share your email.</div>
  </div>
  <div class="mb-3">
    <label for="select" class="form-label">Option</label>
    <select class="form-select" id="select">
      <option>Choose...</option>
    </select>
  </div>
  <div class="mb-3 form-check">
    <input type="checkbox" class="form-check-input" id="agree">
    <label class="form-check-label" for="agree">I agree</label>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Modals

```html
<!-- Trigger -->
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
  Open Modal
</button>

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">Content goes here.</div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button class="btn btn-primary">Save</button>
      </div>
    </div>
  </div>
</div>
```

### List Groups

```html
<ul class="list-group">
  <li class="list-group-item active">Active item</li>
  <li class="list-group-item">Regular item</li>
  <li class="list-group-item list-group-item-success">Success item</li>
  <li class="list-group-item d-flex justify-content-between align-items-center">
    With badge
    <span class="badge text-bg-primary rounded-pill">14</span>
  </li>
</ul>
```

---

## 13. When Custom CSS Is Acceptable

Custom CSS is allowed in limited, well-defined scenarios. Always add a comment explaining why Bootstrap couldn't handle it.

### Acceptable Custom CSS Cases

```css
/* Specific brand color not covered by Bootstrap theme */
.brand-logo { color: #FF6B35; }

/* Background image — no Bootstrap utility for this */
.hero-section {
  background-image: url('/img/hero.jpg');
  background-size: cover;
  background-position: center;
}

/* CSS animation/transition not in Bootstrap */
.fade-slide {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

/* Specific pixel dimensions required by a third-party embed */
.map-embed { height: 400px; }

/* Custom scrollbar styling */
.custom-scroll::-webkit-scrollbar { width: 4px; }
```

### NOT Acceptable Custom CSS

```css
/* ❌ Bootstrap has p-3 for this */
.my-card { padding: 16px; }

/* ❌ Bootstrap has text-center */
.center-text { text-align: center; }

/* ❌ Bootstrap has d-flex align-items-center */
.vcenter { display: flex; align-items: center; }

/* ❌ Bootstrap has fw-bold */
.bold { font-weight: bold; }

/* ❌ Bootstrap has bg-primary text-white */
.blue-box { background-color: #0d6efd; color: white; }
```

### Custom CSS File Structure

When custom CSS is needed, place it in a dedicated file and keep it minimal:

```
/css/
  bootstrap.min.css   ← never edit this
  custom.css          ← your overrides and additions only
```

---

## 14. Decision Tree

Use this process every time you add a style:

```
Need to style an element?
        │
        ▼
Does Bootstrap have a utility class for it?
        │
   YES  │  NO
        │   └─► Does Bootstrap have a component for it?
        │              │
        │         YES  │  NO
        │              │   └─► Is it a brand/theme value?
        │              │              │
        │              │         YES  │  NO
        │              │              │   └─► Write custom CSS with comment
        │              │              │
        │              │         Use CSS custom property
        │              │         or SCSS variable override
        │              │
        │         Use Bootstrap component
        │         + utility modifier classes
        │
   Use Bootstrap utility class
```

---

## 15. Anti-Patterns to Avoid

### 1. Inline Styles for Layout

```html
<!-- ❌ Bad -->
<div style="margin-top: 16px; display: flex; align-items: center;">

<!-- ✅ Good -->
<div class="mt-3 d-flex align-items-center">
```

### 2. Duplicating Bootstrap in Custom CSS

```css
/* ❌ Bad — Bootstrap already does this */
.my-flex { display: flex; }
.my-center { text-align: center; }
.my-bold { font-weight: 700; }
```

### 3. Overriding Bootstrap with !important

```css
/* ❌ Bad — symptom of fighting the framework */
.card { padding: 20px !important; }

/* ✅ Good — use Bootstrap's own utilities */
```
```html
<div class="card p-4">...</div>
```

### 4. Mixing Grid Systems

```html
<!-- ❌ Bad — don't mix Bootstrap grid with custom float/flex wrappers -->
<div class="row">
  <div style="width: 50%; float: left;">...</div>
</div>

<!-- ✅ Good -->
<div class="row">
  <div class="col-md-6">...</div>
</div>
```

### 5. Hardcoding Breakpoint Pixel Values

```css
/* ❌ Bad — hardcoded breakpoints create drift from Bootstrap */
@media (max-width: 768px) { ... }

/* ✅ Good — use Bootstrap SCSS variables if using Sass */
@include media-breakpoint-down(md) { ... }
```

### 6. Empty Wrapper Divs with Only Custom Classes

```html
<!-- ❌ Bad -->
<div class="section-wrapper content-block outer-container">
  <div class="inner-block">...</div>
</div>

<!-- ✅ Good — use Bootstrap semantics directly -->
<section class="container py-5">
  <div class="row g-4">...</div>
</section>
```

---

## 16. Code Review Checklist

Before merging any HTML template, verify:

**Spacing & Layout**
- [ ] All padding/margin uses `p-*` / `m-*` utilities, not inline styles
- [ ] Grid uses `container > row > col-*` structure
- [ ] Gutters use `g-*`, `gx-*`, or `gy-*` on `row`

**Typography**
- [ ] Font sizes use `fs-*` classes, not `style="font-size"`
- [ ] Font weights use `fw-*` classes
- [ ] Text alignment uses `text-start/center/end`

**Colors**
- [ ] Text colors use `text-*` semantic classes
- [ ] Backgrounds use `bg-*` classes
- [ ] No raw hex colors in inline styles unless brand-specific and documented

**Components**
- [ ] Buttons use `btn btn-*` (no custom button styles)
- [ ] Forms use `form-control`, `form-select`, `form-label`
- [ ] No custom modal/tooltip/dropdown implementations when Bootstrap provides them

**Custom CSS**
- [ ] Every custom CSS rule has a comment explaining why Bootstrap couldn't handle it
- [ ] No `!important` overrides
- [ ] No duplicates of Bootstrap utility behavior

**Responsiveness**
- [ ] Layout tested at `xs`, `md`, and `xl` breakpoints
- [ ] `d-none d-*-block` patterns used for responsive show/hide
- [ ] No hardcoded pixel widths on layout containers

---

*This guide should be treated as a living document. Update it when Bootstrap is upgraded or when the team establishes new conventions.*
