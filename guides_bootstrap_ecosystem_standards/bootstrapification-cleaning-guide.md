# Bootstrapification & Cleaning Guide
### From Custom CSS to Enterprise-Grade Bootstrap Code

---

## Table of Contents

1. [Philosophy](#1-philosophy)
2. [CSS Architecture](#2-css-architecture)
3. [Typography & Spacing](#3-typography--spacing)
4. [Colors & Theming](#4-colors--theming)
5. [Icons](#5-icons)
6. [Layout & Grid](#6-layout--grid)
7. [Components](#7-components)
8. [Responsive Design](#8-responsive-design)
9. [JavaScript Architecture](#9-javascript-architecture)
10. [Forms & Inputs](#10-forms--inputs)
11. [Inline Styles](#11-inline-styles)
12. [Accessibility](#12-accessibility)
13. [Performance & Head Cleanup](#13-performance--head-cleanup)
14. [Naming Conventions](#14-naming-conventions)
15. [Audit Checklist](#15-audit-checklist)

---

## 1. Philosophy

### Core Principle
Bootstrap is a design system, not just a CSS reset. Bootstrapification means **trusting the system** — using its variables, utilities, components, and breakpoints instead of reinventing them.

### The Three Questions
Before writing any custom CSS, ask:
1. **Does Bootstrap already have this?** (utility class, component, variable)
2. **Can I achieve this by combining Bootstrap utilities?**
3. **If I must write custom CSS, am I scoping it correctly?**

### What "Enterprise Bootstrap" Means
- No inline styles
- No magic numbers (hardcoded `px`, `rem`, `rgba` values — use CSS variables)
- CSS scoped to a container, never global
- JS encapsulated in a class, never global functions/state
- Every breakpoint intentionally handled
- Semantic HTML with proper ARIA

---

## 2. CSS Architecture

### 2.1 Scope Everything to a Container

The container selector should reflect your component's actual context — a dashboard widget, a product page, a checkout form, a sidebar. The rule is the same: **every custom CSS rule must be prefixed by the component root selector.**

**❌ Before — global selectors leak everywhere:**
```css
.card { border-radius: 12px; }
.meta-label { font-size: .67rem; }
.stepper { position: relative; }
.sidebar-item { padding: .5rem 1rem; }
```

**✅ After — scoped to your component root:**
```css
/* e.g. a product page */
.product-page .card { border-radius: 12px; }
.product-page .meta-label { font-size: .67rem; }

/* e.g. a checkout flow */
.checkout-flow .stepper { position: relative; }

/* e.g. a dashboard sidebar */
.dashboard-sidebar .sidebar-item { padding: .5rem 1rem; }
```

The root selector name comes from your component — `.user-profile`, `.analytics-widget`, `.invoice-view`, `.settings-panel`. There is no universal name — **derive it from what you're building.**

Why: prevents style collisions when the component is embedded in a larger page or CMS.

---

### 2.2 Remove Dead CSS

Common dead rules to hunt and delete:

```css
/* Empty rulesets */
.my-component {}

/* Commented-out blocks left in production */
/* .old-card { background: red; } */

/* Classes that no longer exist in HTML */
.legacy-wrapper { display: flex; }

/* Duplicate declarations */
.btn-custom { color: #fff; font-weight: 600; color: #fff; } /* color twice */
```

---

### 2.3 Replace Hardcoded Values with Bootstrap Variables

**❌ Before:**
```css
.card { border-color: #dee2e6; background: #fff; border-radius: 8px; }
.text-muted-custom { color: #6c757d; }
.shadow-hover:hover { box-shadow: 0 2px 16px rgba(0,0,0,.07); }
```

**✅ After:**
```css
.card {
  border-color: var(--bs-border-color);
  background: var(--bs-body-bg);
  border-radius: var(--bs-border-radius);
}
.text-muted-custom { color: var(--bs-secondary-color); }
.shadow-hover:hover { box-shadow: var(--bs-box-shadow-sm); }
```

**Full reference of Bootstrap 5 CSS variables to use:**
```
--bs-body-bg          --bs-body-color        --bs-border-color
--bs-primary          --bs-secondary         --bs-success
--bs-danger           --bs-warning           --bs-info
--bs-primary-rgb      --bs-body-bg           --bs-border-radius
--bs-border-radius-pill  --bs-border-radius-lg  --bs-box-shadow
--bs-box-shadow-sm    --bs-secondary-color   --bs-tertiary-color
--bs-gray-100 … --bs-gray-900
```

---

### 2.4 Know Your Theme Variables

**Critical trap:** a theme may override Bootstrap defaults. Always check:

```css
/* Default Bootstrap: --bs-light = #f8f9fa */
/* Custom theme may have: --bs-light = #ffffff */
```

If `--bs-light` equals `#fff` in the theme, then `bg-light` hover is invisible. Fix:
```css
/* ❌ Invisible hover in dark-primary themes */
.toggle:hover { background: var(--bs-light); }

/* ✅ Reliable */
.toggle:hover { background: var(--bs-gray-100); }
```

---

## 3. Typography & Spacing

### 3.1 Replace Custom Font Sizes with Bootstrap Utilities

**❌ Before — scattered inline and custom sizes:**
```css
.meta-value { font-size: .875rem; }
.sub-text { font-size: .78rem; }
.tiny { font-size: .72rem; }
```
```html
<div style="font-size:.8rem;">Name</div>
```

**✅ After — Bootstrap scale:**

| Custom size | Bootstrap class |
|-------------|----------------|
| `.875rem` | `fs-6` or `small` |
| `.75–.8rem` | `small` |
| `.67–.72rem` | `small` + custom if truly needed |
| `1.25rem` | `fs-5` |
| `1.5rem` | `fs-4` / `h4` |

```html
<div class="small fw-semibold">Name</div>
<div class="small text-secondary">Subtitle</div>
```

---

### 3.2 Replace Custom Spacing with Bootstrap Spacing Scale

**❌ Before:**
```css
.card-body { padding: 20px 24px; }
.section { margin-bottom: 1.1rem; }
.group { margin-top: .4rem; }
```

**✅ After:**
```html
<div class="p-3 p-md-4">      <!-- 16px / 24px -->
<div class="mb-4">             <!-- 1.5rem -->
<div class="mt-2">             <!-- 0.5rem -->
```

Bootstrap spacing scale (`$spacer = 1rem`):
```
0 = 0      1 = .25rem   2 = .5rem   3 = 1rem
4 = 1.5rem   5 = 3rem
```

---

### 3.3 Replace Custom Font Weight with Utilities

**❌ Before:**
```css
.label { font-weight: 600; }
.title { font-weight: 700; }
.hint  { font-weight: 400; }
```

**✅ After:**
```html
<span class="fw-semibold">Label</span>   <!-- 600 -->
<span class="fw-bold">Title</span>       <!-- 700 -->
<span class="fw-normal">Hint</span>      <!-- 400 -->
```

---

### 3.4 Monospace Fonts

**❌ Before — hardcoded inline:**
```html
<span style="font-family:'JetBrains Mono',monospace;">TRK000001</span>
```

**✅ After — Bootstrap utility:**
```html
<span class="font-monospace">TRK000001</span>
```

---

## 4. Colors & Theming

### 4.1 Replace Custom Color Classes with Bootstrap Contextual Utilities

**❌ Before:**
```css
.status-badge { background: #4bbf73; color: #fff; }
.badge-warning { background: #f0ad4e; color: #fff; }
```

**✅ After:**
```html
<span class="badge text-bg-success">Delivered</span>
<span class="badge text-bg-warning">Shipped</span>
<span class="badge text-bg-info">Processing</span>
<span class="badge text-bg-danger">Cancelled</span>
```

---

### 4.2 Text Colors

**❌ Before:**
```css
.text-muted-light { color: rgba(0,0,0,.45); }
.text-hint { color: #919aa1; }
```

**✅ After:**
```html
<span class="text-secondary">...</span>    <!-- secondary text -->
<span class="text-body-tertiary">...</span> <!-- dimmer text (BS5.3+) -->
<span class="text-muted">...</span>         <!-- muted (legacy alias) -->
```

---

### 4.3 Background Colors

**❌ Before:**
```css
.info-icon { background: rgba(var(--bs-primary-rgb), .1); }
.section-bg { background: #f7f7f9; }
```

**✅ After:**
```html
<div class="bg-primary-subtle text-primary">...</div>
<div class="bg-body-tertiary">...</div>
<div class="bg-light">...</div>
```

---

### 4.4 Animation Colors — Match the Actual Element Color

A subtle but common bug: animations use a different color variable than the element they animate.

**❌ Before — element is `--bs-info` colored, pulse uses `--bs-primary`:**
```css
.dot--active { border-color: var(--bs-info); }

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(var(--bs-primary-rgb), .35); }
}
```

**✅ After — consistent:**
```css
.dot--active { border-color: var(--bs-info); }

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(var(--bs-info-rgb), .35); }
}
```

---

## 5. Icons

### 5.1 Replace Font Awesome with a Single Icon Library

Mixing icon libraries is a common legacy issue. Standardize on one.

**❌ Before — Font Awesome scattered inline:**
```html
<i class="fas fa-location-dot fa-xs"></i>
<i class="fas fa-credit-card me-2"></i>
<i class="fas fa-truck"></i>
<i class="fas fa-circle-check fa-2x text-secondary mb-3 d-block"></i>
```

**✅ After — Material Symbols (or Bootstrap Icons), unified:**
```html
<span class="material-symbols-rounded">location_on</span>
<span class="material-symbols-rounded">credit_card</span>
<span class="material-symbols-rounded">local_shipping</span>
<span class="material-symbols-rounded">check_circle</span>
```

Remove the Font Awesome `<link>` from `<head>` entirely once migrated.

---

### 5.2 Use Bootstrap's Built-in Chevron Instead of a Custom One

Bootstrap renders a chevron automatically on `.accordion-button` via `::after` pseudo-element. It handles open/close state on its own.

**❌ Before — custom icon with manual rotation CSS:**
```html
<button class="toggle" aria-expanded="false">
  <span class="my-chevron">▼</span> Section Title
</button>
```
```css
.my-chevron { transition: transform .2s; }
.toggle[aria-expanded="true"] .my-chevron { transform: rotate(180deg); }
```

**✅ After — Bootstrap does it automatically:**
```html
<button class="accordion-button collapsed" type="button"
        data-bs-toggle="collapse" data-bs-target="#section-1">
  Section Title
</button>
```

No custom CSS needed. Bootstrap applies the chevron and rotation via its own styles.

---

### 5.3 Sizing Icons with Bootstrap

**❌ Before — inline style:**
```html
<span class="material-symbols-rounded" style="font-size:1.1rem">search</span>
```

**✅ After — Bootstrap font-size utilities:**
```html
<span class="material-symbols-rounded fs-5">search</span>
```

---

## 6. Layout & Grid

### 6.1 Replace `d-flex` with `row`/`col` When Content Can Wrap

`d-flex` with multiple children is fine for simple cases. But when items need responsive wrapping, `row`/`col` is more powerful and explicit.

**❌ Before — text wraps badly on mobile:**
```html
<div class="d-flex gap-3 align-items-start">
  <div class="flex-shrink-0"><!-- image --></div>
  <div class="flex-grow-1" style="min-width:0;"><!-- text --></div>
  <div class="text-end flex-shrink-0"><!-- price --></div>
</div>
```

**✅ After — price drops to its own row on mobile:**
```html
<div class="row g-2 align-items-start">
  <div class="col-auto"><!-- image --></div>
  <div class="col mw-0"><!-- text --></div>
  <div class="col-12 col-sm-auto text-sm-end"><!-- price --></div>
</div>
```

---

### 6.2 Never Use `w-100` on Flex Children Without Thinking

`w-100` on a flex child forces full width and can break sibling layout.

**❌ Problem:**
```html
<div class="d-flex">
  <span class="badge w-100">Status</span>  <!-- stretches to full width -->
</div>
```

**✅ Fix — use `flex-shrink-0` instead:**
```html
<div class="d-flex align-items-center gap-2">
  <div class="flex-grow-1 mw-0 text-truncate">Reference ID or long label</div>
  <span class="badge rounded-pill flex-shrink-0">Status</span>
</div>
```

---

### 6.3 Toolbar with Filters + Search Pattern

When a toolbar has a scrollable filter row and a search field, use `flex-lg-row` (not `flex-md-row`) to prevent overlap on medium screens:

**❌ Before — breaks at 768–900px:**
```html
<div class="d-flex flex-md-row gap-3 align-items-md-center">
  <nav><!-- 5 filter pills --></nav>
  <div class="ms-md-auto" style="min-width:260px"><!-- search --></div>
</div>
```

**✅ After — stacks until 992px:**
```html
<div class="d-flex flex-column flex-lg-row gap-3 align-items-lg-center">
  <nav><!-- 5 filter pills --></nav>
  <div class="ms-lg-auto ord-search-wrap"><!-- search --></div>
</div>
```

---

### 6.4 Horizontally Scrollable Nav (Mobile Tabs/Pills)

**❌ Before — tabs overflow and clip:**
```html
<ul class="nav nav-pills gap-1">...</ul>
```

**✅ After — swipeable, no scrollbar visible:**
```html
<ul class="nav nav-pills flex-nowrap gap-1 filter-scroll">...</ul>
```
```css
.filter-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.filter-scroll::-webkit-scrollbar { display: none; }
```

---

### 6.5 `mw-0` on Flex Children with `text-truncate`

Bootstrap's `text-truncate` only works when the parent has a defined width. In flexbox, add `mw-0` (min-width: 0) to the flex child:

**❌ Truncation doesn't work:**
```html
<div class="d-flex">
  <div class="text-truncate">Very long text that won't truncate...</div>
</div>
```

**✅ Works:**
```html
<div class="d-flex">
  <div class="text-truncate mw-0">Very long text that truncates...</div>
</div>
```

---

## 7. Components

### 7.1 Badges — Use Bootstrap Variants, Not Custom Classes

**❌ Before:**
```css
.status-badge {
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .05em;
  padding: .28em .7em;
  border-radius: var(--bs-border-radius-pill);
}
.status-delivered { background: #4bbf73; color: #fff; }
.status-shipped   { background: #f0ad4e; color: #fff; }
```

**✅ After:**
```html
<span class="badge rounded-pill text-bg-success">Delivered</span>
<span class="badge rounded-pill text-bg-warning">Shipped</span>
```

---

### 7.2 Vertical Alignment of Inline Badges

Badges next to text default to `baseline` alignment — they visually sit too low.

**❌ Looks misaligned:**
```html
All <span class="badge">4</span>
```

**✅ Fix with `align-middle`:**
```html
All <span class="badge align-middle">4</span>
```

---

### 7.3 Accordion — Use Native Bootstrap, Not Custom Collapse

**❌ Before — custom button, custom chevron, custom open state:**
```html
<div class="item-card">
  <button class="my-toggle" data-bs-toggle="collapse" data-bs-target="#body-1">
    <div class="header-content">...</div>
    <span class="my-chevron">▾</span>
  </button>
  <div id="body-1" class="collapse">...</div>
</div>
```
```css
.my-chevron { transition: transform .2s; }
.my-toggle[aria-expanded="true"] .my-chevron { transform: rotate(180deg); }
```

**✅ After — Bootstrap accordion handles everything:**
```html
<div class="accordion-item border rounded-3 mb-3">
  <h2 class="accordion-header">
    <button class="accordion-button collapsed rounded-3" type="button"
            data-bs-toggle="collapse" data-bs-target="#body-1">
      <div class="flex-grow-1">Header content</div>
    </button>
  </h2>
  <div id="body-1" class="accordion-collapse collapse">
    <div class="accordion-body">Body content</div>
  </div>
</div>
```

Bootstrap applies the chevron `::after`, handles `aria-expanded`, handles `collapsed` class toggle — no custom CSS needed.

---

### 7.4 Suppress Unwanted Accordion Styles

When using `accordion-button` outside a full accordion wrapper, some default styles may intrude (background color on open, box-shadow on focus). Suppress only what actually conflicts:

```css
.my-component .accordion-button {
  box-shadow: none;          /* removes focus ring */
  background: transparent;   /* no blue tint when open */
}
.my-component .accordion-button:not(.collapsed) {
  color: inherit;            /* don't change text color when open */
}
```

---

### 7.5 Input Groups — Keep the Border Unified

A common mistake splits the border between `input-group-text` and `form-control`, creating a visual seam.

**❌ Before — invisible seam:**
```html
<div class="input-group input-group-sm">
  <span class="input-group-text bg-white border-end-0">🔍</span>
  <input class="form-control border-start-0 ps-0" placeholder="Search...">
</div>
```

**✅ After — pill shape, unified background:**
```html
<div class="input-group">
  <span class="input-group-text bg-body-tertiary border-end-0 rounded-start-pill px-3 text-secondary">
    <span class="material-symbols-rounded">search</span>
  </span>
  <input type="search" class="form-control bg-body-tertiary border-start-0 rounded-end-pill"
         placeholder="Search…">
</div>
```

Add focus state that transitions the whole group together:
```css
.search-wrap .input-group:focus-within .input-group-text,
.search-wrap .input-group:focus-within .form-control {
  border-color: var(--bs-primary);
  background-color: var(--bs-body-bg) !important;
}
```

---

### 7.6 Empty States — Use Bootstrap Structure

**❌ Before — custom CSS:**
```css
.empty-state { text-align: center; padding: 3rem 1rem; }
.empty-state i { font-size: 2rem; color: #aaa; display: block; margin-bottom: 1rem; }
```

**✅ After — Bootstrap utilities only:**
```html
<div class="text-center py-5 px-3 border border-2 border-dashed rounded-3">
  <span class="material-symbols-rounded fs-1 text-secondary d-block mb-3">inbox</span>
  <h5 class="fw-semibold mb-1">Nothing here yet</h5>
  <p class="text-secondary small mb-0">Your purchases will appear here.</p>
</div>
```

---

## 8. Responsive Design

### 8.1 Mobile-First Breakpoint Strategy

Always build mobile-first and add complexity upward:

```
xs  (default, 0px+)   → base styles, single column
sm  (576px+)          → minor adjustments
md  (768px+)          → 2-column layouts
lg  (992px+)          → full desktop layout, horizontal toolbars
xl  (1200px+)         → max-width constraints
```

**Rule of thumb:** if something breaks between `md` and `lg`, push the breakpoint up to `lg` rather than hacking at `md`.

---

### 8.2 Long Strings — Always Add `text-break`

Any user-generated or system-generated string without spaces will overflow: identifiers, codes, URLs, emails, file paths, addresses.

```html
<!-- Tracking / reference code -->
<a class="text-break">REF-2024-000000001</a>

<!-- File path -->
<span class="text-break">/var/www/uploads/2024/clients/documents/report.pdf</span>

<!-- Email address -->
<span class="text-break">very.long.email@subdomain.company.example.com</span>

<!-- Street address -->
<div class="text-break">123 Very Long Avenue Name, Apartment 4B, City Name, ST 00000</div>
```

---

### 8.3 Truncation vs Breaking

Choose the right tool:

| Scenario | Use |
|----------|-----|
| Single line, cut with `…`, hover for full | `text-truncate` + `title="full value"` + `mw-0` on parent |
| Multi-line, must show full value | `text-break` |
| Fixed container, content must not wrap | `text-nowrap` |
| Table cell overflow | `text-truncate` + fixed column width |

---

### 8.4 Cards That Stack Properly on Mobile

**❌ Before — 4 columns crammed on mobile:**
```html
<div class="d-flex justify-content-between">
  <div>Date: Jan 15</div>
  <div>Amount: $1,359</div>
  <div>Items: 4</div>
  <div>Ref: INV-2024-482... <span class="badge">Active</span></div>
</div>
```

**✅ After — Bootstrap grid, intentional stacking:**
```html
<div class="row g-2 align-items-center">
  <div class="col-6 col-md-3">Date</div>
  <div class="col-6 col-md-2">Amount</div>
  <div class="col-md-2 d-none d-md-block">Items</div>
  <div class="col-12 col-md-5 d-flex justify-content-between justify-content-md-end gap-2">
    <div class="text-md-end mw-0">
      <div class="text-truncate small" title="{{ item.ref }}">{{ item.ref }}</div>
    </div>
    <span class="badge rounded-pill flex-shrink-0 text-bg-success">Active</span>
  </div>
</div>
```

---

### 8.5 Stepper / Progress Indicators on Small Screens

Labels next to step dots run out of space fast. Strategy:

```html
<!-- Full label on sm+ -->
<div class="stepper-label d-none d-sm-block">Step Label</div>

<!-- Abbreviated label on mobile — shorter font size keeps it within the dot column -->
<div class="stepper-label d-sm-none" style="font-size:.6rem;line-height:1.1">Step Label</div>

<!-- Date / timestamp only on sm+ -->
<div class="stepper-date d-none d-sm-block">Jan 15</div>
```

---

## 9. JavaScript Architecture

### 9.1 Global Functions → Encapsulated Class

**❌ Before — global state, global functions, ad-hoc init:**
```js
const State = { filter: 'all', search: '' };
let debounce;

function render() { ... }
function renderItem(item) { ... }
function getFiltered() { ... }

setTimeout(() => {
  counter.textContent = DATA.length;
  render();
}, 500);
```

**✅ After — class with private state, named after your component:**
```js
// Name the class after what it controls:
// ProductListController, InvoiceTableController,
// UserDashboardController, TicketQueueController, etc.

class ProductListController {
  static STATUS_CFG = { ... };
  static EMPTY_STATES = { ... };

  constructor(containerSelector) {
    this.container = document.querySelector(containerSelector);
    this.state = { filter: 'all', search: '' };
    this.debounce = null;
    this._bindEvents();
    this._render();
  }

  _render() { ... }
  _renderItem(item) { ... }
  _getFiltered() { ... }
  _bindEvents() { ... }
}

document.addEventListener('DOMContentLoaded', () => {
  new ProductListController('.product-list-container');
});
```

Benefits: no global scope pollution, multiple instances possible, testable, replaceable.

---

### 9.2 Static Config Belongs in the Class

**❌ Before — config objects scattered inside render functions:**
```js
function renderEmpty(filter) {
  const messages = {
    all:      { icon: 'fa-box-open',    title: 'Nothing here' },
    active:   { icon: 'fa-hourglass',   title: 'Nothing active' },
    archived: { icon: 'fa-archive',     title: 'Nothing archived' },
  };
  // ...
}
```

**✅ After — static class property, defined once, used anywhere:**
```js
class MyController {
  // All static config at the top of the class, named for your domain
  static EMPTY_STATES = {
    all:      { icon: 'inbox',         title: 'Nothing here yet',   sub: 'Items will appear here.' },
    active:   { icon: 'hourglass_top', title: 'Nothing active',     sub: 'Active items show here.' },
    archived: { icon: 'inventory_2',   title: 'Nothing archived',   sub: 'Archived items show here.' },
  };

  static TYPE_CFG = {
    info:    { badge: 'text-bg-info',    icon: 'info'         },
    warning: { badge: 'text-bg-warning', icon: 'warning'      },
    error:   { badge: 'text-bg-danger',  icon: 'error'        },
    success: { badge: 'text-bg-success', icon: 'check_circle' },
  };
}
```

Any configuration that is fixed at design time — statuses, types, empty states, icon maps, label maps — belongs as a static property, not inside a function.

---

### 9.3 Hoist Repeated Calculations

If the same derived value is computed in multiple render functions, calculate it once at the top level and pass it down as an argument.

**❌ Before — same calculation repeated in multiple render functions:**
```js
function renderView(item) {
  renderHeader(item);   // computes subtotal internally
  // ...
  `${item.lines.reduce((s, l) => s + l.qty, 0)}` // computed again inline
  // ...
}
function renderHeader(item) {
  const qty = item.lines.reduce((s, l) => s + l.qty, 0); // and again here
}
```

**✅ After — calculate once, pass down:**
```js
_renderView(item) {
  const totalQty = item.lines.reduce((s, l) => s + l.qty, 0);
  return `
    ...${this._renderHeader(item, totalQty)}...
    ...<span class="badge">${totalQty}</span>...
  `;
}
_renderHeader(item, totalQty) { /* uses passed value */ }
```

This applies to any repeated derivation: totals, formatted dates, computed labels, filtered counts.

---

### 9.4 Derive Labels from Config, Not Manual String Manipulation

**❌ Before — manual capitalize, badge class hardcoded inline:**
```js
const label = item.status[0].toUpperCase() + item.status.slice(1);
// badge class decided by scattered if/else or switch
```

**✅ After — single config object drives both label and badge:**
```js
// Example for a task manager
static STATUS_CFG = {
  draft:      { badge: 'text-bg-secondary', label: 'Draft'      },
  active:     { badge: 'text-bg-info',      label: 'Active'     },
  completed:  { badge: 'text-bg-success',   label: 'Completed'  },
  blocked:    { badge: 'text-bg-danger',    label: 'Blocked'    },
};

// Example for a support ticket system
static STATUS_CFG = {
  open:       { badge: 'text-bg-info',      label: 'Open'       },
  pending:    { badge: 'text-bg-warning',   label: 'Pending'    },
  resolved:   { badge: 'text-bg-success',   label: 'Resolved'   },
  closed:     { badge: 'text-bg-secondary', label: 'Closed'     },
};

// Usage is always the same pattern regardless of domain
const { badge, label } = this._getCfg(item.status);
```

The config object is the single source of truth for any entity that has statuses, types, or categories. The same pattern applies to priority levels, user roles, document states, payment methods — any enumerable domain value.

---

### 9.5 Query Scope — Always Within the Component Container

**❌ Before — queries the entire document, breaks with multiple instances:**
```js
document.querySelectorAll('#filter-tabs .nav-link')
document.querySelector('#search-input')
document.querySelector('#submit-btn')
```

**✅ After — scoped to component root:**
```js
this.container.querySelectorAll('[data-filter]')
this.container.querySelector('[data-search]')
this.container.querySelector('[data-submit]')
```

This is critical when the same component appears more than once on a page (e.g. multiple tables, widgets, or modals). Always query within `this.container`.

---

## 10. Forms & Inputs

### 10.1 Always Use Semantic Input Types

```html
<!-- ❌ Generic -->
<input type="text" placeholder="Search...">

<!-- ✅ Semantic — mobile shows search keyboard, gets clear button -->
<input type="search" placeholder="Search…">

<!-- ✅ Other semantic types -->
<input type="email">
<input type="tel">
<input type="number">
<input type="url">
```

### 10.2 Debounce Search Inputs

```js
// ❌ Re-renders on every single keystroke
input.addEventListener('input', () => this._render());

// ✅ Debounced — waits 280ms after last keystroke
input.addEventListener('input', e => {
  clearTimeout(this.debounce);
  this.debounce = setTimeout(() => {
    this.state.search = e.target.value;
    this._render();
  }, 280);
});
```

---

## 11. Inline Styles

### 11.1 The Zero Inline Style Rule

Every inline style in a template is a code smell. They cannot be overridden by themes, cannot be responsive, and pollute the DOM.

**Full replacement map for common offenders:**

| Inline style | Bootstrap class |
|---|---|
| `style="font-size:.875rem"` | `small` or `fs-6` |
| `style="font-size:.72rem"` | `small` |
| `style="font-weight:600"` | `fw-semibold` |
| `style="font-weight:700"` | `fw-bold` |
| `style="color:#6c757d"` | `text-secondary` |
| `style="min-width:0"` | `mw-0` (custom) or Bootstrap's `min-w-0` |
| `style="white-space:nowrap"` | `text-nowrap` |
| `style="text-align:center"` | `text-center` |
| `style="display:none"` | `d-none` |
| `style="font-family:'JetBrains Mono',monospace"` | `font-monospace` |
| `style="text-overflow:ellipsis"` | `text-truncate` |
| `style="word-break:break-word"` | `text-break` |
| `style="opacity:.5"` | `opacity-50` |
| `style="cursor:pointer"` | handled by button/a tag |

---

## 12. Accessibility

### 12.1 ARIA on Interactive Elements

```html
<!-- Filter tabs — any tabbed interface -->
<ul role="tablist">
  <li role="presentation">
    <button role="tab" aria-selected="true" data-filter="all">All</button>
  </li>
  <li role="presentation">
    <button role="tab" aria-selected="false" data-filter="active">Active</button>
  </li>
</ul>

<!-- Live region for any dynamically updated list or result set -->
<div id="results-list" role="list" aria-live="polite"></div>

<!-- Any collapse/expand toggle -->
<button data-bs-toggle="collapse" aria-expanded="false" aria-controls="panel-1">
  Toggle Section
</button>
```

### 12.2 `title` Attribute on Truncated Text

When using `text-truncate`, always add the full value as `title` for tooltip accessibility:

```html
<!-- Any long identifier, name, or path that gets truncated -->
<div class="text-truncate mw-0" title="{{ item.fullName }}">
  {{ item.fullName }}
</div>

<div class="text-truncate mw-0" title="{{ file.path }}">
  {{ file.path }}
</div>
```

### 12.3 `loading="lazy"` on Images

```html
<!-- ❌ -->
<img src="photo.jpg" alt="Photo">

<!-- ✅ Descriptive alt, lazy loading -->
<img src="photo.jpg" alt="{{ item.name }}" loading="lazy">
<img src="avatar.jpg" alt="Profile photo of {{ user.name }}" loading="lazy">
<img src="thumbnail.jpg" alt="{{ article.title }} cover image" loading="lazy">
```

---

## 13. Performance & Head Cleanup

### 13.1 Remove Dead `<link>` Tags

```html
<!-- ❌ Commented-out link still parsed -->
<!-- <link href="https://cdn.../bootstrap.min.css" rel="stylesheet"> -->

<!-- ❌ Hardcoded local path — breaks in every environment except dev machine -->
<link rel="stylesheet" href="C:/GitHub/project/assets/bootstrap/css/bootstrap.min.css">

<!-- ✅ CDN with integrity -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-..." crossorigin="anonymous">
```

### 13.2 Load Only What You Use

**❌ Loading two icon fonts:**
```html
<link href=".../font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded..." rel="stylesheet">
```

Pick one and delete the other.

### 13.3 Skeleton Loaders — Use Bootstrap

**❌ Before — custom shimmer animation:**
```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}
```

This is fine to keep if Bootstrap's `placeholder` utility doesn't match the design. But if it does:

**✅ Bootstrap placeholder:**
```html
<p class="placeholder-glow">
  <span class="placeholder col-6"></span>
  <span class="placeholder col-4"></span>
</p>
```

---

## 14. Naming Conventions

### 14.1 Prefixed BEM for Custom Classes

When custom CSS is unavoidable, use a component prefix derived from your component's name. The prefix should be short, meaningful, and unique within the project.

**❌ Generic — could conflict with anything:**
```css
.card { }
.meta-label { }
.stepper { }
.sidebar-item { }
```

**✅ Prefixed — scoped, clear, collision-safe:**
```css
/* Orders page → prefix: ord- */
.ord-card { }
.ord-meta-label { }
.ord-stepper { }

/* Invoice view → prefix: inv- */
.inv-card { }
.inv-line-item { }
.inv-total-row { }

/* User profile → prefix: prof- */
.prof-avatar { }
.prof-stats-grid { }

/* Analytics dashboard → prefix: dash- */
.dash-widget { }
.dash-chart-wrap { }
.dash-kpi-label { }

/* Settings panel → prefix: cfg- */
.cfg-section { }
.cfg-toggle-row { }
```

**The rule:** your prefix comes from the context you're building. There is no universal prefix — derive it from the feature, page, or component name. One or two syllables, kebab-case, followed by a dash.

### 14.2 Private Methods in JS Classes

Prefix private methods with `_` to signal intent. Name the class and its methods after your actual domain:

```js
// Name reflects what it controls
class InvoiceTableController {
  // Public API — callable from outside
  refresh() { this._render(); }
  setFilter(f) { this.state.filter = f; this._render(); }

  // Private implementation — internal only
  _render() { }
  _renderRow(item) { }
  _renderEmpty() { }
  _bindEvents() { }
  _getFiltered() { }
  _esc(str) { }
  _fmtCurrency(n, cur) { }
  _fmtDate(s) { }
}

// Other examples of well-named controllers:
class UserListController { ... }
class DashboardWidgetController { ... }
class TicketQueueController { ... }
class MediaGalleryController { ... }
```

---

## 15. Audit Checklist

Use this checklist on any legacy Bootstrap project before calling it "clean":

### HTML
- [ ] No inline `style=""` attributes in templates
- [ ] No commented-out `<link>` or `<script>` tags in `<head>`
- [ ] No hardcoded local file paths (`C:/`, `/Users/`, `../../../`)
- [ ] All images have `alt` and `loading="lazy"`
- [ ] Interactive elements have correct ARIA roles and attributes
- [ ] `title` on all `text-truncate` elements

### CSS
- [ ] All rules scoped to `.component-container`
- [ ] No empty rulesets `{}`
- [ ] No hardcoded hex/rgb values — using `var(--bs-*)` instead
- [ ] No custom classes that duplicate Bootstrap utilities
- [ ] Hover states actually visible (not `--bs-light` = white on white)
- [ ] Animation colors match the element they animate
- [ ] No dead/unused CSS classes
- [ ] No `!important` except to override Bootstrap's own `!important`

### JavaScript
- [ ] No global functions or state
- [ ] Logic encapsulated in a class
- [ ] Static config in `static` class properties
- [ ] DOM queries scoped to `this.container`
- [ ] No repeated calculations (hoist to parent caller)
- [ ] No manual string capitalize — use config label
- [ ] Search inputs debounced

### Responsive
- [ ] Tested at 320px (iPhone SE / 4)
- [ ] Tested at 768px (iPad / medium)
- [ ] Tested at 992px (tablet landscape)
- [ ] Tested at 1280px+ (desktop)
- [ ] Long strings have `text-break` or `text-truncate`
- [ ] Horizontal scroll nav has touch scroll + hidden scrollbar
- [ ] Badge siblings in flex rows have `flex-shrink-0`

### Bootstrap-specific
- [ ] Icons: single library, no mixing
- [ ] Badges use `text-bg-*` variants
- [ ] Accordion uses native `accordion-button` (no custom chevron)
- [ ] Input groups: unified border, no `border-end-0` seam hacks
- [ ] Filter/tab pills: proper `role="tablist"` + `role="tab"` + `aria-selected`
- [ ] Inline badge alignment uses `align-middle`
- [ ] `font-monospace` instead of inline font-family

---

*This guide reflects patterns identified through Bootstrap 5 codebase analysis and iterative refactoring of real production components across multiple domains. Apply it incrementally — prioritize visual bugs and accessibility first, then architecture, then cleanup.*
