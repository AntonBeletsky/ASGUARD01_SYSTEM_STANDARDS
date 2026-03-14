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
7. [CSS Grid Utilities](#7-css-grid-utilities)
8. [Sizing (Width & Height)](#8-sizing-width--height)
9. [Borders & Rounded Corners](#9-borders--rounded-corners)
10. [Shadows & Opacity](#10-shadows--opacity)
11. [Display & Visibility](#11-display--visibility)
12. [Position & Z-Index](#12-position--z-index)
13. [Interactive Components](#13-interactive-components)
14. [Components — Bootstrap vs Custom](#14-components--bootstrap-vs-custom)
15. [Icons](#15-icons)
16. [Accessibility (a11y)](#16-accessibility-a11y)
17. [SCSS Theming & Variable Overrides](#17-scss-theming--variable-overrides)
18. [CSS Custom Properties (Runtime Theming)](#18-css-custom-properties-runtime-theming)
19. [Bootstrap Utility API — Extending the System](#19-bootstrap-utility-api--extending-the-system)
20. [Page & Section Patterns](#20-page--section-patterns)
21. [Responsive Patterns](#21-responsive-patterns)
22. [Class Naming Conventions](#22-class-naming-conventions)
23. [JavaScript Initialization Patterns](#23-javascript-initialization-patterns)
24. [When Custom CSS Is Acceptable](#24-when-custom-css-is-acceptable)
25. [Decision Tree](#25-decision-tree)
26. [Anti-Patterns to Avoid](#26-anti-patterns-to-avoid)
27. [Code Review Checklist](#27-code-review-checklist)

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

## 7. CSS Grid Utilities

Bootstrap 5 includes CSS Grid support as an opt-in layer on top of the flexbox grid. Use it when you need named areas, dense packing, or true 2D layouts.

### Enable CSS Grid Mode

```html
<!-- Replace .row with .row.row-cols-* or use the grid class -->
<div class="grid">
  <div class="g-col-6">Half width</div>
  <div class="g-col-6">Half width</div>
</div>
```

### Column Spans

```html
<div class="grid">
  <div class="g-col-4">4 of 12</div>
  <div class="g-col-8">8 of 12</div>
  <div class="g-col-12">Full width</div>
</div>
```

### Responsive Column Spans

```html
<div class="grid">
  <div class="g-col-12 g-col-md-6 g-col-lg-4">Responsive</div>
  <div class="g-col-12 g-col-md-6 g-col-lg-4">Responsive</div>
  <div class="g-col-12 g-col-md-12 g-col-lg-4">Responsive</div>
</div>
```

### Column Start (Explicit Placement)

```html
<div class="grid">
  <div class="g-col-3 g-start-2">Starts at column 2</div>
  <div class="g-col-4 g-start-7">Starts at column 7</div>
</div>
```

### Row Columns (Uniform Grid)

When all columns should be equal — use `row-cols-*` on a `.row`:

```html
<!-- Always 2 columns -->
<div class="row row-cols-2 g-3">
  <div class="col"><div class="card">...</div></div>
  <div class="col"><div class="card">...</div></div>
  <div class="col"><div class="card">...</div></div>
  <div class="col"><div class="card">...</div></div>
</div>

<!-- Responsive: 1 → 2 → 3 → 4 -->
<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-xl-4 g-4">
  <div class="col">...</div>
</div>
```

> **Rule:** Use `row-cols-*` for card grids and uniform item layouts. Use `col-*` when columns have different sizes.

---

## 8. Sizing (Width & Height)

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

## 9. Borders & Rounded Corners

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

## 10. Shadows & Opacity

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

## 11. Display & Visibility

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

## 12. Position & Z-Index

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

---

## 13. Interactive Components

All Bootstrap interactive components are driven by `data-bs-*` attributes — no custom JavaScript needed for standard behavior.

### Accordion

```html
<div class="accordion" id="faq">
  <div class="accordion-item">
    <h2 class="accordion-header">
      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#q1">
        Question 1
      </button>
    </h2>
    <div id="q1" class="accordion-collapse collapse show" data-bs-parent="#faq">
      <div class="accordion-body">Answer content here.</div>
    </div>
  </div>
  <div class="accordion-item">
    <h2 class="accordion-header">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#q2">
        Question 2
      </button>
    </h2>
    <div id="q2" class="accordion-collapse collapse" data-bs-parent="#faq">
      <div class="accordion-body">Answer content here.</div>
    </div>
  </div>
</div>
```

### Tabs

```html
<!-- Tab nav -->
<ul class="nav nav-tabs" id="myTabs" role="tablist">
  <li class="nav-item" role="presentation">
    <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab1" role="tab">Tab 1</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab2" role="tab">Tab 2</button>
  </li>
</ul>

<!-- Tab content -->
<div class="tab-content pt-3">
  <div class="tab-pane fade show active" id="tab1" role="tabpanel">Content 1</div>
  <div class="tab-pane fade" id="tab2" role="tabpanel">Content 2</div>
</div>
```

### Pills Navigation

```html
<ul class="nav nav-pills gap-1">
  <li class="nav-item">
    <a class="nav-link active" href="#">Active</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="#">Link</a>
  </li>
  <li class="nav-item">
    <a class="nav-link disabled">Disabled</a>
  </li>
</ul>
```

### Tooltips

Tooltips require JavaScript initialization. Use `data-bs-toggle="tooltip"` and init on page load:

```html
<button class="btn btn-secondary" data-bs-toggle="tooltip" data-bs-placement="top" title="Tooltip text">
  Hover me
</button>
```

```javascript
// Initialize all tooltips on the page
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
```

### Popovers

```html
<button class="btn btn-lg btn-danger" data-bs-toggle="popover" data-bs-title="Popover title"
  data-bs-content="This is the body content of the popover.">
  Click me
</button>
```

```javascript
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
popoverTriggerList.forEach(el => new bootstrap.Popover(el));
```

### Toasts (Notifications)

```html
<!-- Toast container — always position-fixed -->
<div class="toast-container position-fixed bottom-0 end-0 p-3">
  <div id="liveToast" class="toast" role="alert">
    <div class="toast-header">
      <span class="bg-primary rounded me-2" style="width:16px;height:16px;display:inline-block;"></span>
      <strong class="me-auto">Notification</strong>
      <small class="text-muted">just now</small>
      <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
    </div>
    <div class="toast-body">File saved successfully.</div>
  </div>
</div>
```

```javascript
// Show a toast programmatically
const toast = new bootstrap.Toast(document.getElementById('liveToast'));
toast.show();
```

### Offcanvas (Drawer/Sidebar)

```html
<!-- Trigger -->
<button class="btn btn-primary" data-bs-toggle="offcanvas" data-bs-target="#sidebar">
  Open Sidebar
</button>

<!-- Offcanvas panel -->
<div class="offcanvas offcanvas-start" tabindex="-1" id="sidebar">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title">Sidebar</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
  </div>
  <div class="offcanvas-body">
    <p>Sidebar content here.</p>
  </div>
</div>
```

Placement options: `offcanvas-start` (left), `offcanvas-end` (right), `offcanvas-top`, `offcanvas-bottom`.

### Dropdowns

```html
<div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown">
    Actions
  </button>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="#">Edit</a></li>
    <li><a class="dropdown-item" href="#">Duplicate</a></li>
    <li><hr class="dropdown-divider"></li>
    <li><a class="dropdown-item text-danger" href="#">Delete</a></li>
  </ul>
</div>
```

### Progress Bars

```html
<!-- Basic -->
<div class="progress" style="height: 8px;">
  <div class="progress-bar" style="width: 65%"></div>
</div>

<!-- Labeled + colored -->
<div class="progress mb-2">
  <div class="progress-bar bg-success" style="width: 40%">40%</div>
</div>

<!-- Striped + animated -->
<div class="progress">
  <div class="progress-bar progress-bar-striped progress-bar-animated bg-warning" style="width: 75%"></div>
</div>

<!-- Stacked (multiple segments) -->
<div class="progress">
  <div class="progress-bar bg-success" style="width: 30%">30%</div>
  <div class="progress-bar bg-warning" style="width: 20%">20%</div>
  <div class="progress-bar bg-danger" style="width: 10%">10%</div>
</div>
```

> **Note:** `style="width: X%"` is the Bootstrap-endorsed way to set progress — it's dynamic data, not a design value, so inline style is acceptable here.

### Spinners (Loading States)

```html
<!-- Border spinner (default) -->
<div class="spinner-border text-primary" role="status">
  <span class="visually-hidden">Loading...</span>
</div>

<!-- Growing spinner -->
<div class="spinner-grow text-success" role="status">
  <span class="visually-hidden">Loading...</span>
</div>

<!-- Small variants -->
<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>

<!-- Button with spinner -->
<button class="btn btn-primary" disabled>
  <span class="spinner-border spinner-border-sm me-2" role="status"></span>
  Saving...
</button>
```

### Collapse (Toggle Any Content)

```html
<a class="btn btn-outline-primary" data-bs-toggle="collapse" href="#details">
  Show Details
</a>

<div class="collapse mt-2" id="details">
  <div class="card card-body">
    Hidden content revealed on toggle.
  </div>
</div>
```

### Breadcrumb

```html
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="#">Home</a></li>
    <li class="breadcrumb-item"><a href="#">Products</a></li>
    <li class="breadcrumb-item active" aria-current="page">Item Name</li>
  </ol>
</nav>
```

### Pagination

```html
<nav aria-label="Page navigation">
  <ul class="pagination justify-content-center">
    <li class="page-item disabled">
      <a class="page-link">Previous</a>
    </li>
    <li class="page-item active"><a class="page-link" href="#">1</a></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item">
      <a class="page-link" href="#">Next</a>
    </li>
  </ul>
</nav>
```

---

## 14. Components — Bootstrap vs Custom

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

## 15. Icons

Bootstrap does not bundle icons — use **Bootstrap Icons** (official), or any SVG icon library.

### Bootstrap Icons (Recommended)

Install via CDN:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
```

Usage:
```html
<!-- Inline icon -->
<i class="bi bi-house-door-fill"></i>

<!-- Icon with color and size via Bootstrap utilities -->
<i class="bi bi-check-circle-fill text-success fs-4"></i>
<i class="bi bi-exclamation-triangle text-warning fs-5 me-2"></i>

<!-- Icon in a button -->
<button class="btn btn-primary d-flex align-items-center gap-2">
  <i class="bi bi-upload"></i>
  Upload File
</button>

<!-- Icon-only button (always include sr-only label) -->
<button class="btn btn-outline-danger" aria-label="Delete item">
  <i class="bi bi-trash3" aria-hidden="true"></i>
</button>

<!-- Icon in a badge -->
<span class="badge text-bg-info">
  <i class="bi bi-bell-fill me-1"></i>3
</span>

<!-- Icon with text — align using flex -->
<span class="d-inline-flex align-items-center gap-1">
  <i class="bi bi-person-circle"></i>
  Profile
</span>
```

### Icon Sizing

Never set `width`/`height` on icon fonts — use Bootstrap font-size utilities:

```html
<i class="bi bi-star fs-1"></i>  <!-- Largest -->
<i class="bi bi-star fs-4"></i>  <!-- Medium -->
<i class="bi bi-star fs-6"></i>  <!-- Small -->
```

### SVG Icons (Inline)

For single-color SVGs that need to inherit color:

```html
<svg class="text-primary" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
  <!-- path data -->
</svg>
```

> **Rule:** Always use `fill="currentColor"` so the icon inherits the `text-*` color class.

---

## 16. Accessibility (a11y)

Bootstrap provides helpers for accessible markup. Always use them — they are part of the unified system.

### Visually Hidden (Screen Reader Only)

```html
<!-- Element invisible to eyes but announced by screen readers -->
<span class="visually-hidden">Loading, please wait</span>

<!-- Same but only hidden when not focused (useful for skip links) -->
<a class="visually-hidden-focusable" href="#main-content">Skip to main content</a>
```

### Focus Ring

Bootstrap manages focus styles. Never disable them. To show focus ring programmatically:
```html
<button class="btn btn-primary focus-ring">Always shows ring</button>
```

### ARIA Roles in Bootstrap Components

Every Bootstrap interactive component requires proper ARIA. Bootstrap provides this by default — don't remove it:

```html
<!-- Alert with role -->
<div class="alert alert-warning" role="alert">Warning message</div>

<!-- Modal with aria-labelledby -->
<div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="myModalLabel">Modal Title</h5>
        ...
      </div>
    </div>
  </div>
</div>

<!-- Tabs with role="tablist" -->
<ul class="nav nav-tabs" role="tablist">
  <li class="nav-item" role="presentation">
    <button class="nav-link active" role="tab" aria-selected="true" aria-controls="panel1">Tab 1</button>
  </li>
</ul>
```

### Color Contrast

Bootstrap's semantic colors (primary, success, danger, etc.) are WCAG AA compliant by default. When customizing theme colors, verify contrast using `text-bg-*` combos:

```html
<!-- text-bg-* auto-adjusts text color for contrast -->
<div class="text-bg-primary p-3">Always readable</div>
<div class="text-bg-warning p-3">Always readable</div>
```

### Disabled States

```html
<!-- Use disabled attribute for native elements -->
<button class="btn btn-primary" disabled>Disabled</button>
<input class="form-control" disabled>

<!-- Use aria-disabled for non-native elements -->
<a class="btn btn-secondary disabled" aria-disabled="true" tabindex="-1">Link button</a>
```

### Form Accessibility

```html
<div class="mb-3">
  <!-- Always link label to input via for/id -->
  <label for="username" class="form-label">Username</label>
  <input type="text" class="form-control" id="username"
    aria-describedby="usernameHelp" required>
  <div id="usernameHelp" class="form-text">3–20 characters, letters and numbers only.</div>
</div>

<!-- Validation state with aria -->
<div class="mb-3">
  <label for="email" class="form-label">Email</label>
  <input type="email" class="form-control is-invalid" id="email" aria-describedby="emailError">
  <div id="emailError" class="invalid-feedback">Please enter a valid email address.</div>
</div>
```

---

## 17. SCSS Theming & Variable Overrides

The correct way to customize Bootstrap is to override SCSS variables **before** importing Bootstrap. Never edit `bootstrap.scss` directly.

### File Structure

```
/scss/
  _variables-override.scss   ← your custom variables
  _custom-components.scss    ← truly custom styles
  main.scss                  ← entry point
```

### main.scss

```scss
// 1. Override variables first
@import "variables-override";

// 2. Import Bootstrap
@import "bootstrap/scss/bootstrap";

// 3. Your custom additions last
@import "custom-components";
```

### Common Variable Overrides

```scss
// _variables-override.scss

// ─── Brand Colors ────────────────────────────────
$primary:   #5C6BC0;   // Override primary color
$secondary: #546E7A;
$success:   #26A69A;
$danger:    #EF5350;
$warning:   #FFA726;

// ─── Typography ──────────────────────────────────
$font-family-base: 'Inter', system-ui, sans-serif;
$font-size-base:   1rem;        // 16px
$line-height-base: 1.6;
$headings-font-weight: 600;

// ─── Spacing ─────────────────────────────────────
// Changing $spacer scales ALL p-*, m-*, gap-* utilities
$spacer: 1rem;   // default; change to 0.875rem for tighter UI

// ─── Border ──────────────────────────────────────
$border-radius:    0.375rem;
$border-radius-sm: 0.25rem;
$border-radius-lg: 0.75rem;
$border-radius-pill: 50rem;
$border-color:     #dee2e6;

// ─── Shadows ─────────────────────────────────────
$box-shadow:    0 2px 8px rgba(0, 0, 0, 0.08);
$box-shadow-sm: 0 1px 4px rgba(0, 0, 0, 0.06);
$box-shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);

// ─── Grid ────────────────────────────────────────
$grid-gutter-width: 1.5rem;
$container-padding-x: 1.5rem;

// ─── Components ──────────────────────────────────
$card-border-radius:     0.75rem;
$card-box-shadow:        $box-shadow;
$btn-border-radius:      0.375rem;
$btn-padding-y:          0.5rem;
$btn-padding-x:          1.25rem;
$navbar-padding-y:       1rem;
$input-border-radius:    0.375rem;
$modal-border-radius:    1rem;
$badge-border-radius:    0.375rem;

// ─── Z-index stack ───────────────────────────────
$zindex-dropdown:  1000;
$zindex-sticky:    1020;
$zindex-fixed:     1030;
$zindex-modal:     1055;
$zindex-tooltip:   1080;
```

### Extending the Color Map

To add custom semantic colors that generate full utility classes (`text-brand`, `bg-brand`, `btn-brand`, `alert-brand`):

```scss
// Add to $theme-colors before Bootstrap import
$theme-colors: map-merge(
  $theme-colors,
  (
    "brand":   #5C6BC0,
    "neutral": #78909C,
  )
);
```

This auto-generates: `btn-brand`, `text-brand`, `bg-brand`, `border-brand`, `alert-brand`, `badge text-bg-brand`.

### Enabling Optional Features

```scss
// Enable negative margin utilities (m-n*)
$enable-negative-margins: true;

// Enable CSS Grid utilities
$enable-cssgrid: true;

// Disable rounded corners globally
$enable-rounded: false;

// Disable shadows globally
$enable-shadows: false;

// Disable gradients
$enable-gradients: false;

// Enable smooth scroll
$enable-smooth-scroll: true;
```

---

## 18. CSS Custom Properties (Runtime Theming)

Bootstrap 5.2+ exposes all component styles as CSS custom properties. Use these for runtime theming (e.g., dark mode, user-customizable themes) without recompiling SCSS.

### Available CSS Variables

Bootstrap sets these on `:root` or scoped to components:

```css
:root {
  --bs-primary: #0d6efd;
  --bs-primary-rgb: 13, 110, 253;
  --bs-body-bg: #fff;
  --bs-body-color: #212529;
  --bs-border-color: #dee2e6;
  --bs-border-radius: 0.375rem;
  --bs-font-sans-serif: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
```

### Runtime Theme Override

```css
/* Override per page, per component, or on :root */
[data-theme="dark"] {
  --bs-body-bg: #1a1a2e;
  --bs-body-color: #e0e0e0;
  --bs-border-color: #444;
}

/* Override per component */
.my-card {
  --bs-card-bg: #f8f9fa;
  --bs-card-border-color: transparent;
  --bs-card-border-radius: 1rem;
}
```

### Dark Mode (Bootstrap 5.3+)

Bootstrap 5.3 ships with a built-in dark mode. Toggle it with a `data-bs-theme` attribute:

```html
<!-- Whole page dark -->
<html data-bs-theme="dark">

<!-- Single component dark -->
<div class="card" data-bs-theme="dark">
  <div class="card-body">Dark card in a light page</div>
</div>

<!-- Toggle via JS -->
<button onclick="document.documentElement.setAttribute('data-bs-theme',
  document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark')">
  Toggle Dark Mode
</button>
```

---

## 19. Bootstrap Utility API — Extending the System

When you need a utility class that Bootstrap doesn't provide, use the Utility API to generate it — don't write raw CSS.

### Basic Custom Utility

```scss
// In your SCSS, after Bootstrap import
@import "bootstrap/scss/utilities/api";

$utilities: map-merge(
  $utilities,
  (
    // Add cursor utilities
    "cursor": (
      property: cursor,
      values: auto pointer grab not-allowed wait,
    ),

    // Add letter-spacing utilities
    "letter-spacing": (
      property: letter-spacing,
      class: ls,
      values: (
        tight:  -0.025em,
        normal:  0,
        wide:    0.05em,
        wider:   0.1em,
      ),
    ),

    // Add aspect-ratio utilities
    "aspect-ratio": (
      property: aspect-ratio,
      class: ratio,
      values: (
        "1x1":   1 / 1,
        "16x9":  16 / 9,
        "4x3":   4 / 3,
      ),
    ),
  )
);
```

This generates: `.cursor-pointer`, `.ls-tight`, `.ls-wide`, `.ratio-16x9`, etc.

### Making Utilities Responsive

```scss
"cursor": (
  property: cursor,
  responsive: true,   // ← generates .cursor-pointer, .cursor-md-pointer, etc.
  values: auto pointer grab not-allowed,
),
```

### Making Utilities Support State Variants

```scss
"cursor": (
  property: cursor,
  state: hover focus,  // ← generates .hover-cursor-pointer, .focus-cursor-pointer
  values: auto pointer grab,
),
```

### Disabling Unused Utilities (Bundle Optimization)

```scss
// Disable utilities you never use to reduce CSS output
$utilities: map-merge(
  $utilities,
  (
    "float": null,           // Remove float utilities
    "vertical-align": null,  // Remove vertical-align utilities
  )
);
```

---

## 20. Page & Section Patterns

Reusable markup patterns for common page structures. Always built from Bootstrap classes.

### Hero Section

```html
<section class="py-5 py-lg-6 bg-light">
  <div class="container">
    <div class="row align-items-center g-5">
      <div class="col-12 col-lg-6">
        <span class="badge text-bg-primary mb-3">New Release</span>
        <h1 class="display-4 fw-bold lh-sm mb-3">Headline that sells your product</h1>
        <p class="lead text-muted mb-4">Supporting copy that explains what this is and why it matters.</p>
        <div class="d-flex flex-column flex-sm-row gap-3">
          <a href="#" class="btn btn-primary btn-lg px-4">Get Started</a>
          <a href="#" class="btn btn-outline-secondary btn-lg px-4">Learn More</a>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <img src="hero.png" class="img-fluid rounded-3 shadow-lg" alt="Product screenshot">
      </div>
    </div>
  </div>
</section>
```

### Feature Grid

```html
<section class="py-5">
  <div class="container">
    <h2 class="text-center fw-bold mb-2">Features</h2>
    <p class="text-center text-muted mb-5">What makes this different</p>
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div class="col">
        <div class="card h-100 border-0 shadow-sm">
          <div class="card-body p-4">
            <div class="text-primary mb-3 fs-2">
              <i class="bi bi-lightning-charge-fill"></i>
            </div>
            <h5 class="card-title fw-semibold">Feature Title</h5>
            <p class="card-text text-muted">Short description of this feature and its benefit.</p>
          </div>
        </div>
      </div>
      <!-- Repeat .col items -->
    </div>
  </div>
</section>
```

### Stats Row

```html
<section class="py-5 bg-primary text-white">
  <div class="container">
    <div class="row row-cols-2 row-cols-md-4 g-4 text-center">
      <div class="col">
        <div class="fs-1 fw-bold">99%</div>
        <div class="opacity-75 small">Uptime SLA</div>
      </div>
      <div class="col">
        <div class="fs-1 fw-bold">50K+</div>
        <div class="opacity-75 small">Active Users</div>
      </div>
      <div class="col">
        <div class="fs-1 fw-bold">120ms</div>
        <div class="opacity-75 small">Avg Response</div>
      </div>
      <div class="col">
        <div class="fs-1 fw-bold">4.9★</div>
        <div class="opacity-75 small">User Rating</div>
      </div>
    </div>
  </div>
</section>
```

### Sidebar + Content Layout

```html
<div class="container py-4">
  <div class="row g-4">

    <!-- Sidebar -->
    <div class="col-12 col-lg-3">
      <div class="sticky-top pt-3" style="top: 80px;">
        <nav class="nav flex-column nav-pills gap-1">
          <a class="nav-link active" href="#">Overview</a>
          <a class="nav-link" href="#">Settings</a>
          <a class="nav-link" href="#">Billing</a>
          <a class="nav-link text-danger" href="#">Danger Zone</a>
        </nav>
      </div>
    </div>

    <!-- Main Content -->
    <div class="col-12 col-lg-9">
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-header bg-transparent border-bottom fw-semibold py-3">
          Section Title
        </div>
        <div class="card-body p-4">
          Content here.
        </div>
      </div>
    </div>

  </div>
</div>
```

### Empty State

```html
<div class="text-center py-5 px-3">
  <i class="bi bi-inbox text-muted" style="font-size: 3rem;"></i>
  <h5 class="mt-3 fw-semibold">No items yet</h5>
  <p class="text-muted mb-4">Get started by creating your first item.</p>
  <a href="#" class="btn btn-primary">
    <i class="bi bi-plus-circle me-2"></i>Create Item
  </a>
</div>
```

### Data Table with Actions

```html
<div class="card border-0 shadow-sm">
  <div class="card-header bg-transparent d-flex justify-content-between align-items-center py-3">
    <h6 class="mb-0 fw-semibold">Users</h6>
    <button class="btn btn-sm btn-primary">
      <i class="bi bi-plus-lg me-1"></i>Add User
    </button>
  </div>
  <div class="table-responsive">
    <table class="table table-hover align-middle mb-0">
      <thead class="table-light text-muted small text-uppercase">
        <tr>
          <th class="ps-4">Name</th>
          <th>Role</th>
          <th>Status</th>
          <th class="pe-4 text-end">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="ps-4">
            <div class="d-flex align-items-center gap-2">
              <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center"
                style="width:36px;height:36px;font-size:.85rem;">JD</div>
              <div>
                <div class="fw-semibold">Jane Doe</div>
                <div class="small text-muted">jane@example.com</div>
              </div>
            </div>
          </td>
          <td><span class="text-muted small">Admin</span></td>
          <td><span class="badge text-bg-success-subtle border border-success-subtle text-success rounded-pill">Active</span></td>
          <td class="pe-4 text-end">
            <div class="dropdown">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
                Actions
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#">Edit</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item text-danger" href="#">Remove</a></li>
              </ul>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="card-footer bg-transparent d-flex justify-content-between align-items-center py-3">
    <span class="text-muted small">Showing 1–10 of 48</span>
    <nav><ul class="pagination pagination-sm mb-0">
      <li class="page-item disabled"><a class="page-link">Prev</a></li>
      <li class="page-item active"><a class="page-link" href="#">1</a></li>
      <li class="page-item"><a class="page-link" href="#">2</a></li>
      <li class="page-item"><a class="page-link" href="#">Next</a></li>
    </ul></nav>
  </div>
</div>
```

---

## 21. Responsive Patterns

### Mobile-First Mindset

Always write base styles for mobile, then add `*-md-*`, `*-lg-*` classes to progressively enhance:

```html
<!-- ❌ Wrong — desktop-first, doesn't work on mobile -->
<div class="row">
  <div class="col-4">...</div>
</div>

<!-- ✅ Right — mobile full width, desktop 4 columns -->
<div class="row">
  <div class="col-12 col-md-4">...</div>
</div>
```

### Responsive Text Size

```html
<h1 class="display-6 display-md-4 display-lg-2">Scales with viewport</h1>

<!-- Or use fs-* with breakpoints -->
<p class="fs-6 fs-md-5 fs-lg-4">Growing text</p>
```

### Responsive Spacing

```html
<!-- Tight on mobile, generous on desktop -->
<section class="py-4 py-md-5 py-lg-6">...</section>
<div class="p-3 p-md-4 p-lg-5">...</div>
```

### Responsive Flex Direction

```html
<!-- Stack on mobile, side-by-side on desktop -->
<div class="d-flex flex-column flex-md-row gap-3">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Responsive Button Group

```html
<!-- Stack buttons on mobile, inline on sm+ -->
<div class="d-grid d-sm-flex gap-2">
  <button class="btn btn-primary">Primary Action</button>
  <button class="btn btn-outline-secondary">Secondary</button>
</div>
```

### Responsive Table

For tables on small screens, always wrap in `.table-responsive`:

```html
<div class="table-responsive">
  <table class="table">...</table>
</div>

<!-- Responsive at specific breakpoint -->
<div class="table-responsive-md">
  <table class="table">...</table>
</div>
```

### Hiding/Showing by Breakpoint

```html
<!-- Desktop nav: visible md+, hidden on mobile -->
<nav class="d-none d-md-flex">...</nav>

<!-- Mobile hamburger: visible on mobile, hidden md+ -->
<button class="d-md-none">☰</button>

<!-- Print-only element -->
<div class="d-none d-print-block">...</div>
```

---

## 22. Class Naming Conventions

When you do write custom classes (for the cases where Bootstrap falls short), follow these naming rules to keep custom code harmonious with Bootstrap.

### BEM for Custom Components

```html
<!-- Block: .card-profile -->
<!-- Element: .card-profile__avatar, .card-profile__name -->
<!-- Modifier: .card-profile--featured -->

<div class="card card-profile card-profile--featured">
  <img class="card-profile__avatar" src="..." alt="">
  <div class="card-body">
    <h5 class="card-profile__name">Jane Doe</h5>
  </div>
</div>
```

### Namespace Custom Classes

Prefix all your custom classes to distinguish them from Bootstrap classes:

```html
<!-- Use a project prefix, e.g. "app-" -->
<div class="app-hero">
<div class="app-sidebar">
<div class="app-data-table">
```

This prevents future Bootstrap updates from accidentally overriding your styles.

### Never Name Classes by Appearance

```html
<!-- ❌ Bad — brittle, breaks when design changes -->
<div class="blue-box big-text right-column">

<!-- ✅ Good — semantic, stable -->
<div class="app-promo-banner fs-5 col-md-4">
```

### Modifier Classes via Bootstrap + Custom Combo

Extend Bootstrap components rather than replacing them:

```html
<!-- ✅ Bootstrap base + custom modifier -->
<button class="btn btn-primary app-btn--rounded-full px-5">

<!-- ✅ Card with custom visual variant -->
<div class="card app-card--glass border-0">
```

---

## 23. JavaScript Initialization Patterns

### Initialize All at Once (Simple Projects)

```javascript
// Initialize all tooltips
document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));

// Initialize all popovers
document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => new bootstrap.Popover(el));
```

### Programmatic Control

```javascript
// Modal
const modal = new bootstrap.Modal('#myModal', { backdrop: 'static' });
modal.show();
modal.hide();
modal.toggle();

// Toast
const toast = new bootstrap.Toast('#myToast', { delay: 3000, autohide: true });
toast.show();

// Offcanvas
const drawer = new bootstrap.Offcanvas('#sidebar');
drawer.show();
drawer.hide();

// Collapse
const collapse = new bootstrap.Collapse('#details', { toggle: false });
collapse.show();
collapse.hide();

// Tab
const tab = new bootstrap.Tab('#my-tab');
tab.show();
```

### Event Listeners

Bootstrap fires events you can hook into:

```javascript
// React when modal finishes opening
document.getElementById('myModal').addEventListener('shown.bs.modal', () => {
  document.querySelector('#myModal input').focus();
});

// React when tab changes
document.getElementById('myTabs').addEventListener('shown.bs.tab', event => {
  console.log('Active tab:', event.target.dataset.bsTarget);
});

// React when toast hides
document.getElementById('myToast').addEventListener('hidden.bs.toast', () => {
  // Clean up
});
```

### Lazy Initialization (Performance)

For pages with many interactive elements, initialize only when needed:

```javascript
// Initialize tooltip only on hover (avoids initializing 100 tooltips at page load)
document.addEventListener('mouseover', function(e) {
  if (e.target.dataset.bsToggle === 'tooltip' && !e.target._bsTooltip) {
    new bootstrap.Tooltip(e.target).show();
  }
});
```

---

## 24. When Custom CSS Is Acceptable

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

## 25. Decision Tree

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

## 26. Anti-Patterns to Avoid

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

## 27. Code Review Checklist

Before merging any HTML template, verify:

**Spacing & Layout**
- [ ] All padding/margin uses `p-*` / `m-*` utilities, not inline styles
- [ ] Grid uses `container > row > col-*` structure
- [ ] Gutters use `g-*`, `gx-*`, or `gy-*` on `row`
- [ ] `gap-*` used on flex/grid parents instead of margin on children

**Typography**
- [ ] Font sizes use `fs-*` classes, not `style="font-size"`
- [ ] Font weights use `fw-*` classes
- [ ] Text alignment uses `text-start/center/end`
- [ ] Line height uses `lh-*` where needed

**Colors**
- [ ] Text colors use `text-*` semantic classes
- [ ] Backgrounds use `bg-*` classes
- [ ] Combined bg+text uses `text-bg-*` where possible
- [ ] No raw hex colors in inline styles unless brand-specific and documented

**Components**
- [ ] Buttons use `btn btn-*` (no custom button styles)
- [ ] Forms use `form-control`, `form-select`, `form-label`
- [ ] No custom modal/tooltip/dropdown/accordion/tabs implementations when Bootstrap provides them
- [ ] Tooltips and popovers are JavaScript-initialized

**Interactive Components**
- [ ] Loading states use `spinner-border` or `spinner-grow`
- [ ] Notifications use Bootstrap `toast` component
- [ ] Drawers/panels use Bootstrap `offcanvas`
- [ ] Toggle content uses Bootstrap `collapse`

**Icons**
- [ ] Icons sized via `fs-*` utilities, not `width`/`height` attributes
- [ ] Icon-only buttons have `aria-label` and `aria-hidden="true"` on the icon
- [ ] SVG icons use `fill="currentColor"`

**Accessibility**
- [ ] All form inputs have associated `<label>` elements
- [ ] Interactive elements have proper `aria-*` attributes
- [ ] Focus styles are not suppressed with `outline: none`
- [ ] `visually-hidden` used for screen-reader-only text (not `display: none`)
- [ ] `disabled` attribute on native elements; `aria-disabled` on non-native

**Theming & SCSS**
- [ ] No direct edits to `bootstrap.min.css`
- [ ] Variable overrides placed before Bootstrap import in SCSS
- [ ] New semantic colors added via `$theme-colors` map-merge
- [ ] New utility classes use the Utility API, not hand-written CSS

**Responsiveness**
- [ ] Base styles written mobile-first
- [ ] Layout tested at `xs`, `md`, and `xl` breakpoints
- [ ] `d-none d-*-block` patterns used for responsive show/hide
- [ ] Tables wrapped in `.table-responsive`
- [ ] No hardcoded pixel widths on layout containers

**Custom CSS**
- [ ] Every custom CSS rule has a comment explaining why Bootstrap couldn't handle it
- [ ] All custom classes use a project namespace prefix (e.g. `app-`)
- [ ] No `!important` overrides of Bootstrap utilities
- [ ] No duplicates of Bootstrap utility behavior
- [ ] Custom class names are semantic, not appearance-based (no `.blue-box`)

---

*This guide should be treated as a living document. Update it when Bootstrap is upgraded or when the team establishes new conventions.*
