# Refactoring Level+ Pro
## AI-Assisted Code Quality Guide — Enterprise Edition

> **Purpose**: A structured, repeatable workflow for refactoring legacy projects into
> production-grade, enterprise-quality code using AI assistance.
> The goal is not just "make it work" — it's *make it excellent, maintainable, and conflict-free*.

> **Version**: 2.0 Pro — based on Containerization v4, Compact Comments Guide, Clean Code standards.

---

## Table of Contents

1. [Core Philosophy](#1-core-philosophy)
2. [Conflict Resolution Priority — The Hierarchy](#2-conflict-resolution-priority--the-hierarchy)
3. [JS Rendering Decision Tree — When JS is Actually Needed](#3-js-rendering-decision-tree--when-js-is-actually-needed)
4. [Phase 0 — Input & Context Collection](#4-phase-0--input--context-collection)
5. [Phase 1 — System Analysis](#5-phase-1--system-analysis)
6. [Phase 2 — Pre-Refactor Planning](#6-phase-2--pre-refactor-planning)
7. [Phase 3 — Containerization Architecture](#7-phase-3--containerization-architecture)
8. [Phase 4 — Static HTML+CSS First](#8-phase-4--static-htmlcss-first)
9. [Phase 5 — JS Layer (Only When Justified)](#9-phase-5--js-layer-only-when-justified)
10. [Phase 6 — UI/UX Standards Audit](#10-phase-6--uiux-standards-audit)
11. [Phase 7 — Mobile & Responsive Adaptation](#11-phase-7--mobile--responsive-adaptation)
12. [Phase 8 — Accessibility (a11y)](#12-phase-8--accessibility-a11y)
13. [Phase 9 — W3C Standards Compliance](#13-phase-9--w3c-standards-compliance)
14. [Phase 10 — Lifecycle & State Analysis](#14-phase-10--lifecycle--state-analysis)
15. [Phase 11 — Documentation & Comments](#15-phase-11--documentation--comments)
16. [Phase 12 — Bootstrap Conflict Detection](#16-phase-12--bootstrap-conflict-detection)
17. [Phase 13 — Execution ("делай" / "do it")](#17-phase-13--execution-делай--do-it)
18. [Phase 14 — Enterprise Production Checklist](#18-phase-14--enterprise-production-checklist)
19. [Communication Protocol](#19-communication-protocol)

---

## 1. Core Philosophy

```
READ → ANALYZE → CLASSIFY → PLAN → CONFIRM → EXECUTE
```

- Never refactor blindly. Always understand *why* before *how*.
- **Static by default. Dynamic only when required.**
- Every JS line must earn its place — if CSS/HTML can do it, they do it.
- Every decision must be justified by code quality, standards, or user value.
- Containerization is the shape of everything — all rules operate inside that shape.

---

## 2. Conflict Resolution Priority — The Hierarchy

When two rules conflict, the **higher rank always wins**. No exceptions.

```
┌─────────────────────────────────────────────────────────────┐
│  RANK 0 — CONTAINERIZATION                                  │
│  Defines the shape of every component. Inviolable.          │
│  → Widget = self-contained container, scoped CSS, scoped JS │
├─────────────────────────────────────────────────────────────┤
│  RANK 1 — DATA ATTRIBUTES  (Law Zero)                       │
│  JS operates exclusively through data-* attributes.         │
│  No class hooks. No id hooks. No jQuery.                    │
├─────────────────────────────────────────────────────────────┤
│  RANK 2 — CODE CLEANLINESS                                  │
│  Structure, isolation, readability, naming conventions.     │
│  Applies everywhere unless it conflicts with RANK 3.        │
├─────────────────────────────────────────────────────────────┤
│  RANK 3 — SECURITY                                          │
│  XSS prevention, input validation, namespace protection.    │
│  Overrides any "convenience" shortcuts from RANK 2.         │
├─────────────────────────────────────────────────────────────┤
│  RANK 4 — PERFORMANCE                                       │
│  No layout thrashing, passive listeners, throttle/debounce. │
│  Final audit — does not reshape architecture.               │
└─────────────────────────────────────────────────────────────┘
```

### How to apply the hierarchy in practice

**Scenario A — Class name conflicts with Bootstrap:**
> RANK 0 wins → scope all custom selectors to the container class.
> Never override Bootstrap globals without container scoping.

**Scenario B — Readable code vs. Security:**
> RANK 3 wins → use `_esc()` even if it makes the template less "elegant".
> Never use `innerHTML` with user data, even "just this once".

**Scenario C — Performance optimization breaks isolation:**
> RANK 0 wins → keep the container boundary intact.
> Optimize inside the container, not by breaking it open.

**Scenario D — Convenience shortcut (class as JS hook):**
> RANK 1 wins → use `data-action` / `data-ref` regardless of how "simpler" the class hook seems.

---

## 3. JS Rendering Decision Tree — When JS is Actually Needed

Before writing a single line of JS, apply this decision tree.
**The default answer is always "static HTML+CSS first".**

```
┌─────────────────────────────────────────────────────────┐
│  Does this feature require JS?                          │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │ Can CSS alone do it?  │
         │ (:hover, :focus,      │
         │  :checked, :target,   │
         │  CSS animations,      │
         │  CSS Grid/Flex)       │
         └───────────┬───────────┘
                     │
           ┌─────────┴──────────┐
          YES                   NO
           │                    │
    ✅ USE CSS            ┌──────▼──────────────────┐
    No JS needed          │ Can HTML alone do it?   │
                          │ (<details>/<summary>,   │
                          │  <dialog>, <progress>,  │
                          │  form validation,       │
                          │  <input type="*">)      │
                          └──────┬──────────────────┘
                                 │
                       ┌─────────┴──────────┐
                      YES                   NO
                       │                    │
               ✅ USE HTML            ┌──────▼────────────────────────┐
               No JS needed           │ Does it require:              │
                                      │ - User interaction + response │
                                      │ - Dynamic data (API/fetch)    │
                                      │ - State that changes at runtime│
                                      │ - DOM updates based on logic  │
                                      │ - Browser API (storage, etc.) │
                                      └──────┬────────────────────────┘
                                             │
                                   ┌─────────┴──────────┐
                                  YES                    NO
                                   │                     │
                            ✅ USE JS            🚫 JUSTIFY IT
                            Containerization     Write out why
                            v4 pattern           JS is needed
                            applies              before coding
```

### Static HTML+CSS — What never needs JS:

| Feature | Static solution |
|---|---|
| Dropdown menu (hover) | CSS `:hover` + `visibility` |
| Accordion | `<details>` + `<summary>` |
| Tabs (basic) | CSS `:target` or `:checked` hack |
| Tooltip | CSS `[data-tooltip]:hover::after` |
| Modal (simple) | `<dialog>` + CSS, or `:target` |
| Image gallery | CSS Grid + `:focus-within` |
| Sticky header | CSS `position: sticky` |
| Smooth scroll | CSS `scroll-behavior: smooth` |
| Dark mode toggle | CSS `prefers-color-scheme` |
| Form validation (basic) | HTML5 `required`, `pattern`, `type` |
| Loading spinner | CSS `@keyframes` animation |
| Responsive nav | CSS + Bootstrap collapse (data-bs-*) |
| Progress bar (static) | `<progress>` element |
| Card hover effects | CSS `transform`, `transition` |
| Grid layout | CSS Grid / Bootstrap Grid |

### Bootstrap data-attributes — What Bootstrap handles without custom JS:

```html
<!-- Modal — no custom JS required -->
<button data-bs-toggle="modal" data-bs-target="#myModal">Open</button>

<!-- Collapse — no custom JS required -->
<button data-bs-toggle="collapse" data-bs-target="#collapseEl">Toggle</button>

<!-- Tooltip — only Bootstrap init needed, no custom logic -->
<span data-bs-toggle="tooltip" title="Tooltip text">Hover me</span>

<!-- Dropdown — no custom JS required -->
<button data-bs-toggle="dropdown">Menu</button>

<!-- Tab navigation — no custom JS required -->
<button data-bs-toggle="tab" data-bs-target="#tab1">Tab 1</button>
```

> **Rule:** Bootstrap's own `data-bs-*` system is not JS — it's declarative HTML.
> Use it freely. Only write a `<script>` block when Bootstrap + CSS cannot handle the requirement.

### When JS rendering IS justified:

- Rendering a list from fetched API data
- Real-time search/filter of items
- Form with complex multi-step validation logic
- Shopping cart / state that persists across interactions
- Dynamic content that changes based on user choices
- Infinite scroll / pagination
- Real-time updates (websocket, polling)
- Complex form state (show/hide fields based on other fields)
- Data visualization (charts, graphs)
- Drag-and-drop interactions

---

## 4. Phase 0 — Input & Context Collection

### What the user does:
- Shares **screenshots** of the running application
- Shares **source code** (paste, upload, or link)

### What the AI does:
1. Acknowledge receipt — confirm what was received
2. **Do nothing else** — no suggestions, no refactoring, no opinions
3. Wait for explicit instruction to proceed

> **Rule:** Until the user writes **"делай"** / **"do it"** — AI only collects and reads.

---

## 5. Phase 1 — System Analysis

*Triggered by: "conduct a full system analysis" / "проведи анализ"*

### 1.1 Code Analysis

| Dimension | What to look for |
|---|---|
| **Architecture** | Separation of concerns, coupling, cohesion |
| **Containerization** | Are widgets self-contained? CSS scoped? No global leaks? |
| **JS necessity** | Is JS used where CSS/HTML would suffice? |
| **Data attributes** | Are `data-*` used for JS hooks, or classes/ids? |
| **jQuery** | Any jQuery remaining? Map migration path. |
| **Patterns** | Anti-patterns, spaghetti, god objects |
| **Data flow** | How data moves through the app |
| **Error handling** | Missing try/catch, unchecked nulls, silent failures |
| **Performance** | Layout thrashing, blocking ops, memory leaks |
| **Security** | XSS vectors, unvalidated input, innerHTML misuse |

### 1.2 Screenshot Analysis

- Map UI elements to code structures
- Identify inconsistencies between visual state and logic
- Classify each UI component: **static** or **dynamic**?
- Note UX anti-patterns, layout issues, a11y failures

### 1.3 Analysis Output Format

```
## System Analysis Report

### What the project does
[1-3 sentences]

### Tech stack detected
[Technologies, versions if visible]

### Component classification
| Component | Type | JS needed? | Reason |
|---|---|---|---|
| Hero banner | static | No | CSS-only layout |
| Search bar | dynamic | Yes | Live API filter |
| Nav menu | semi-static | No | Bootstrap collapse |
| Cart counter | dynamic | Yes | State changes at runtime |

### Critical issues (must fix)
[Numbered list — blocking issues]

### Code quality issues (should fix)
[Numbered list]

### Observations (nice to fix)
[Numbered list]

### What works well (keep it)
[Numbered list]
```

---

## 6. Phase 2 — Pre-Refactor Planning

*Triggered by: "how would you refactor" — output plan only, no code*

The AI must produce a refactoring plan with:

1. **Project purpose** — what problem does it solve?
2. **Component map** — which components are static vs. dynamic
3. **Target architecture** — container structure per component
4. **Technology choices** — justify every dependency
5. **Change list** — what gets removed, replaced, rewritten
6. **Risk assessment** — what could break

### Output Format

```
## Refactoring Plan

### Project purpose (re-confirmed)
[...]

### Component map
| Component | Current | Target | JS? |
|---|---|---|---|
| Header | jQuery soup | Static HTML+CSS | No |
| Search | jQuery + id hooks | ES6 + data-attrs | Yes — API call |
| Modal | Bootstrap 4 + jQuery | Bootstrap 5 data-bs-* | No |

### Proposed stack
- HTML5 semantic structure
- Bootstrap 5.x (CSS + declarative JS via data-bs-*)
- Vanilla ES6+ (no jQuery) — only where JS is genuinely needed
- Containerization v4 — one class per widget, scoped everything

### Changes summary
| Old | New | Reason |
|---|---|---|
| jQuery $.ajax | fetch() / async-await | Native, no dep |
| $('.js-hook') | [data-action] / [data-ref] | Law Zero |
| #id for JS | data-ref="name" | No global id hooks |
| Global CSS | .container-class selector | Scoped, no leaks |
| Modal outside container | Modal inside container | Token inheritance |

### Risk areas
[...]
```

---

## 7. Phase 3 — Containerization Architecture

**This phase defines the shape of every component. It runs before any code is written.**

### 3.1 Container Rules

Every component = one self-contained container:

```html
<!-- Semantic tag, class only — no id on root -->
<section class="orders-container" aria-label="Order list">

  <!-- Component markup using Bootstrap classes freely -->
  <div class="row g-3">
    <div class="col-md-6">
      <!-- Bootstrap grid works inside the container -->
    </div>
  </div>

  <!-- Modals: ALWAYS inside the container, before closing tag -->
  <div class="ord-modal-overlay"
       data-ref="modal-delete"
       role="dialog"
       aria-modal="true"
       aria-labelledby="ord-modal-title"
       hidden>
    <div class="ord-modal">
      <h2 id="ord-modal-title" class="ord-modal__title">Delete order?</h2>
      <p  class="ord-modal__body">This action cannot be undone.</p>
      <div class="ord-modal__actions">
        <button class="btn btn-secondary" data-action="modal-cancel">Cancel</button>
        <button class="btn btn-danger"    data-action="modal-confirm">Confirm</button>
      </div>
    </div>
  </div>

</section><!-- /orders-container -->
```

### 3.2 CSS Scoping Rule

Every selector starts with the container class. No exceptions.

```css
/* ✅ CORRECT — scoped to container */
.orders-container .ord-item { ... }
.orders-container .ord-item--cancelled { ... }
.orders-container .btn { ... }       /* safe Bootstrap override, scoped */

/* ❌ WRONG — global leak */
.ord-item { ... }
.btn { background: red; }            /* breaks Bootstrap everywhere */
```

### 3.3 CSS Token Scope

Tokens declared on the container — child elements inherit automatically:

```css
.orders-container {
  /* --- Tokens --- */
  --ord-color-new:       #0d6efd;
  --ord-color-cancelled: #dc3545;
  --ord-radius:          0.5rem;
  --ord-gap:             1rem;

  /* --- Layout --- */
  display: flex;
  flex-direction: column;
  gap: var(--ord-gap);
}
```

### 3.4 Naming Conventions

| What | Convention | Example |
|---|---|---|
| ES6 class | PascalCase + `Controller` | `OrdersController` |
| CSS container | kebab + `-container` | `.orders-container` |
| CSS child prefix | short kebab (2-4 chars) | `ord-` |
| BEM modifier | `[prefix]-[el]--[mod]` | `.ord-item--cancelled` |
| Modal overlay | `[prefix]-modal-overlay` | `.ord-modal-overlay` |
| CSS tokens | `--[prefix]-[name]` | `--ord-color-new` |
| `data-ref` | kebab name | `data-ref="send-btn"` |
| `data-action` | kebab verb | `data-action="modal-open-delete"` |
| `data-state` | kebab state | `data-state="active"` |

### 3.5 Law Zero — JS via Data Attributes Only

```html
<!-- ✅ CORRECT -->
<button class="btn btn-primary" data-action="send">Send</button>
<div    class="ord-list"        data-ref="list"></div>
<li     class="ord-item"        data-id="order-42" data-state="new"></li>

<!-- ❌ FORBIDDEN — class as JS hook -->
<button class="btn btn-primary js-send-btn">Send</button>

<!-- ❌ FORBIDDEN — id as JS hook -->
<button id="send-btn" class="btn btn-primary">Send</button>
```

```js
// ✅ ALLOWED query methods (all scoped to this._root)
this._root.querySelector('[data-ref="name"]')
this._root.querySelector('[data-action="name"]')
e.target.closest('[data-action]')
document.querySelectorAll('.widget-container')   // bootstrap all instances

// ❌ FORBIDDEN
document.getElementById('anything')
document.querySelector('.some-class')            // for JS logic
document.querySelector('#some-id')
$('#anything') / $('.anything')                  // jQuery
```

`id` is allowed **only** for ARIA references and anchor links — never for JS queries.

---

## 8. Phase 4 — Static HTML+CSS First

**Before touching JS, build the maximum possible in static HTML+CSS.**

### 4.1 Audit Questions (per component)

For every UI element, ask in order:

1. Does this work with pure HTML semantics? → use it
2. Does this work with CSS (`:hover`, `:focus`, `:checked`, `:target`)? → use it
3. Does Bootstrap's `data-bs-*` handle this declaratively? → use it
4. Only if all three answers are NO → write JS

### 4.2 CSS-Only Patterns Preferred

```css
/* ✅ Hover reveal — no JS */
.orders-container .ord-item__actions {
  opacity: 0;
  transition: opacity 0.2s ease;
}
.orders-container .ord-item:hover .ord-item__actions,
.orders-container .ord-item:focus-within .ord-item__actions {
  opacity: 1;
}

/* ✅ State-based styling via data-state — driven by JS but styled in CSS */
.orders-container .ord-item[data-state="cancelled"] {
  opacity: 0.5;
  text-decoration: line-through;
}

/* ✅ Loading state — CSS animation, no JS animation code */
.orders-container[data-state="loading"] .ord-list {
  pointer-events: none;
  opacity: 0.6;
}

/* ✅ Empty state — CSS only */
.orders-container .ord-list:empty::after {
  content: 'No orders yet.';
  display: block;
  text-align: center;
  color: var(--bs-secondary);
  padding: 2rem;
}
```

### 4.3 Bootstrap Declarative Features (No Custom JS)

```html
<!-- Accordion — Bootstrap handles, no JS written -->
<div class="accordion" id="faqAccordion">
  <div class="accordion-item">
    <h2 class="accordion-header">
      <button class="accordion-button" type="button"
              data-bs-toggle="collapse"
              data-bs-target="#faq1">
        Question 1
      </button>
    </h2>
    <div id="faq1" class="accordion-collapse collapse show">
      <div class="accordion-body">Answer 1</div>
    </div>
  </div>
</div>

<!-- Offcanvas nav — Bootstrap handles, no JS written -->
<button data-bs-toggle="offcanvas" data-bs-target="#mobileNav">Menu</button>
<div class="offcanvas offcanvas-start" id="mobileNav">...</div>

<!-- Tooltip — only Bootstrap init, no custom logic -->
<!-- JS needed only for: document.querySelectorAll('[data-bs-toggle="tooltip"]')
                         .forEach(el => new bootstrap.Tooltip(el)) -->
```

---

## 9. Phase 5 — JS Layer (Only When Justified)

*This phase runs only for components that passed the decision tree in §3 and require dynamic behavior.*

### 5.1 Controller Structure (Containerization v4)

```js
/**
 * OrdersController — manages the orders widget.
 *
 * Handles: list rendering, status updates, delete confirmation modal.
 * Depends on: Bootstrap 5 (CSS only, no BS JS plugins used here)
 *
 * @class OrdersController
 */
class OrdersController {

  /* ============================================================
     CONFIG
     ============================================================ */

  /** Keys blocked from user-supplied objects to prevent prototype pollution. */
  static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);

  /** Delay before auto-clearing status messages (ms). */
  static STATUS_CLEAR_MS = 3000;

  /** Seed / initial data — used when no external data is provided. */
  static SEED_DATA = [];

  /* ============================================================
     CONSTRUCTOR
     ============================================================ */

  /**
   * @param {string|Element} selector - Container CSS class or DOM element
   * @param {Object}         [opts]   - { data: Array } override seed data
   */
  constructor(selector, opts = {}) {
    // Find root — silent return if container not in DOM
    this._root = typeof selector === 'string'
      ? document.querySelector(selector)
      : selector;
    if (!this._root) return;

    // Scoped DOM helpers — all queries stay inside the container
    this.$ = (s) => this._root.querySelector(s);
    this.$$ = (s) => this._root.querySelectorAll(s);

    // Cache DOM refs via data-ref — only here, never elsewhere
    this._refs = {
      list:   this.$('[data-ref="list"]'),
      status: this.$('[data-ref="status"]'),
      modal:  this.$('[data-ref="modal-delete"]'),
    };

    // Validate & initialise state
    const raw = OrdersController._validate(opts.data ?? OrdersController.SEED_DATA);
    this._state = {
      orders: raw,
      modal:  null,      // { targetId } or null
      status: 'idle',    // idle | loading | error
    };

    // AbortController — single point of cleanup
    this._ac = new AbortController();
    this._lastFocused = null;

    // Render + bind
    this._render();
    this._bind();
  }

  /* ============================================================
     RENDER
     ============================================================ */

  /** Render the full list based on current state. */
  _render() {
    const { orders } = this._state;

    // Empty state handled by CSS :empty — no JS needed
    this._refs.list.innerHTML = orders.map(o => `
      <li class="ord-item" data-id="${this._esc(o.id)}" data-state="${this._esc(o.status)}">
        <span class="ord-item__name">${this._esc(o.name)}</span>
        <span class="ord-item__status">${this._esc(o.status)}</span>
        <button class="btn btn-sm btn-outline-danger ord-item__del"
                data-action="remove" data-id="${this._esc(o.id)}"
                aria-label="Delete order ${this._esc(o.name)}">
          Delete
        </button>
      </li>`
    ).join('');
  }

  /** Sync modal visibility to state — DOM reflects state, not vice versa. */
  _renderModal() {
    const open = !!this._state.modal;
    this._refs.modal.hidden = !open;
    if (open) {
      // Trap focus inside modal
      this._refs.modal.querySelector('[data-action="modal-cancel"]').focus();
    }
  }

  /* ============================================================
     HANDLERS
     ============================================================ */

  /** @param {string} id - Order id to stage for deletion */
  _handleRemove(id) {
    this._lastFocused = document.activeElement;
    this._state.modal  = { targetId: id };
    this._renderModal();
  }

  /** Confirmed deletion from modal. */
  _handleModalConfirm() {
    const { targetId } = this._state.modal;
    this._state.orders = this._state.orders.filter(o => o.id !== targetId);
    this._closeModal();
    this._render();
  }

  /** Close modal, restore focus. */
  _closeModal() {
    this._state.modal = null;
    this._renderModal();
    this._lastFocused?.focus();
  }

  /* ============================================================
     BIND — one delegated listener, one switch
     ============================================================ */

  _bind() {
    // Single delegated click listener for all [data-action] elements
    this._root.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      switch (btn.dataset.action) {
        case 'remove':        return this._handleRemove(btn.dataset.id);
        case 'modal-confirm': return this._handleModalConfirm();
        case 'modal-cancel':  return this._closeModal();
      }
    }, { signal: this._ac.signal });

    // Escape key closes modal
    this._root.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this._state.modal) this._closeModal();
    }, { signal: this._ac.signal });
  }

  /* ============================================================
     UTILITIES
     ============================================================ */

  /**
   * XSS escaping — all user/API data goes through this before innerHTML.
   * @param {*} str - Value to escape
   * @returns {string}
   */
  _esc(str) {
    return String(str ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /** Throttle — prevents high-frequency event handlers from hammering the DOM. */
  _throttle(fn, ms) {
    let last = 0;
    return (...args) => {
      const now = Date.now();
      if (now - last < ms) return;
      last = now;
      fn.apply(this, args);
    };
  }

  /** Remove all event listeners via AbortController. */
  destroy() {
    this._ac.abort();
  }

  /* ============================================================
     STATIC VALIDATION
     ============================================================ */

  /**
   * Validate external data — block prototype pollution.
   * @param {Array} data - Raw external data array
   * @returns {Array} Sanitised data
   */
  static _validate(data) {
    if (!Array.isArray(data)) return [];
    return data.filter(item => {
      if (typeof item !== 'object' || item === null) return false;
      return !OrdersController.FORBIDDEN_KEYS.some(k => k in item);
    });
  }
}

/* ============================================================
   INIT — DOMContentLoaded, one line
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  new OrdersController('.orders-container');
});
```

### 5.2 JS Performance Rules

```js
// ✅ Batch DOM reads before writes — no layout thrashing
const heights = items.map(el => el.offsetHeight);       // all reads
items.forEach((el, i) => { el.style.height = heights[i] * 2 + 'px'; }); // all writes

// ✅ Passive listeners for scroll/touch
this._root.addEventListener('scroll', handler,
  { signal: this._ac.signal, passive: true });

// ✅ Throttle for high-frequency events (~60fps)
this._root.addEventListener('scroll',
  this._throttle(this._onScroll.bind(this), 16),
  { signal: this._ac.signal, passive: true });

// ✅ State via classList / data-state — single reflow
el.classList.add('is-active');
el.dataset.state = 'cancelled';

// ✅ Batch DOM insertions — one reflow
this._refs.list.innerHTML = items.map(i => `<li>${this._esc(i.name)}</li>`).join('');
```

---

## 10. Phase 6 — UI/UX Standards Audit

### Visual Consistency Checklist

- [ ] Single color palette — Bootstrap CSS variables (`--bs-*`) or scoped container tokens (`--prefix-*`)
- [ ] Consistent spacing scale — Bootstrap `m-*`, `p-*` or custom `rem` scale
- [ ] Typography hierarchy — `h1`–`h6` meaningful, not decorative
- [ ] Icon system — one library only (Bootstrap Icons, Heroicons, etc.)
- [ ] Button states defined — default, hover, focus, disabled, loading
- [ ] No mixed visual languages — either Bootstrap native or fully custom, not half-half

### UX Flow Checklist

- [ ] User goals achievable in ≤3 clicks
- [ ] Error states visible and informative (not just "error occurred")
- [ ] Loading states prevent double-submit confusion
- [ ] Success feedback is explicit
- [ ] Destructive actions require confirmation modal
- [ ] Empty states have helpful messaging (not blank screens)

### Form Checklist

- [ ] Labels always present — never placeholder-as-label
- [ ] Validation messages inline and specific
- [ ] Required fields marked (`required` attr + visual indicator)
- [ ] `autocomplete` attributes set
- [ ] Submit button disabled during loading

---

## 11. Phase 7 — Mobile & Responsive Adaptation

### Bootstrap 5 Breakpoints

| Name | Min width | Typical use |
|---|---|---|
| `xs` | < 576px | Small phones |
| `sm` | ≥ 576px | Phones landscape |
| `md` | ≥ 768px | Tablets |
| `lg` | ≥ 992px | Laptops |
| `xl` | ≥ 1200px | Desktops |
| `xxl` | ≥ 1400px | Large screens |

### Rules

1. **Mobile-first** — start `col-12`, add breakpoints as needed
2. **No fixed pixel widths** — use `%`, `vw`, Bootstrap columns, `min()`, `clamp()`
3. **Touch targets** — minimum `44×44px` (WCAG 2.5.5)
4. **Font sizes** — minimum `16px` body, never below `12px`
5. **Viewport meta** — always: `<meta name="viewport" content="width=device-width, initial-scale=1">`
6. **Images** — always `img-fluid` or `max-width: 100%` + `height: auto`
7. **Tables** — wrap in `<div class="table-responsive">`
8. **Navigation** — Bootstrap `navbar-toggler` + offcanvas on mobile
9. **Containers are responsive by default** — no extra media queries needed for layout if grid is used correctly
10. **Test on real devices** — not only DevTools

---

## 12. Phase 8 — Accessibility (a11y)

### WCAG 2.1 AA — Required

**Perceivable:**
- [ ] All images have `alt` text (`alt=""` for decorative)
- [ ] Color not sole conveyor of information
- [ ] Contrast ratio ≥ 4.5:1 (normal), ≥ 3:1 (large text / UI components)
- [ ] No content relying on sensory characteristics alone

**Operable:**
- [ ] All functionality keyboard-accessible (`Tab`, `Enter`, `Escape`, arrows)
- [ ] No keyboard traps
- [ ] Skip navigation: `<a class="visually-hidden-focusable" href="#main-content">Skip to main</a>`
- [ ] Focus always visible (never `outline: none` without replacement)
- [ ] Touch targets ≥ 44×44px

**Understandable:**
- [ ] `<html lang="en">` (or correct locale)
- [ ] Form labels associated (`for` + `id`, or `aria-label`)
- [ ] Error messages describe the problem specifically
- [ ] Consistent navigation structure

**Robust:**
- [ ] Valid HTML (W3C validator)
- [ ] ARIA used correctly — no ARIA on elements with native semantics that already cover the role
- [ ] ARIA live regions for dynamic content: `aria-live="polite"` / `aria-live="assertive"`
- [ ] Modal: `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, focus trap, Escape closes

### Key Bootstrap a11y Helpers

```html
<!-- Visually hidden, screen-reader accessible -->
<span class="visually-hidden">Loading, please wait</span>

<!-- Focusable skip link -->
<a class="visually-hidden-focusable" href="#main-content">Skip to main content</a>

<!-- ARIA live region — dynamic status updates -->
<div data-ref="status"
     aria-live="polite"
     aria-atomic="true"
     class="visually-hidden"></div>
```

---

## 13. Phase 9 — W3C Standards Compliance

### HTML5

- [ ] `<!DOCTYPE html>` present
- [ ] `<html lang="en">` correct locale
- [ ] `<meta charset="UTF-8">`
- [ ] `<title>` meaningful and unique per page
- [ ] Semantic elements: `<header>`, `<main>`, `<nav>`, `<article>`, `<section>`, `<footer>`, `<aside>`
- [ ] No deprecated tags: `<center>`, `<font>`, `<b>` for styling purpose
- [ ] No inline styles (except JS-driven dynamic values)
- [ ] Valid nesting — no block inside inline, no `<div>` inside `<p>`

### CSS3

- [ ] CSS variables for all tokens (`--prefix-name`)
- [ ] No `!important` (except Bootstrap override, scoped + commented)
- [ ] BEM or scoped class naming — no global leaks
- [ ] Media queries mobile-first (`min-width`)
- [ ] Animations: `transform` + `opacity` only (GPU-composited, no layout reflow)

### JS ES6+

- [ ] ES modules or IIFE — no global namespace pollution
- [ ] `const`/`let` — never `var`
- [ ] Arrow functions for callbacks
- [ ] `async`/`await` for all async operations
- [ ] `try`/`catch` in every async function
- [ ] Event delegation via `[data-action]`
- [ ] No `eval()`, no `innerHTML` with unescaped user data
- [ ] No jQuery

---

## 14. Phase 10 — Lifecycle & State Analysis

Map the application's full lifecycle before writing state management.

### State Map

```
[Initial Load]
      ↓
[Idle / Default]   ← data rendered, UI responsive
      ↓                   ↓
[User Action]    [System Event / Timer]
      ↓
[Loading]   ← spinner shown, UI disabled, submit locked
      ↓               ↓
[Success]        [Error]
      ↓               ↓
[Updated State]  [Error State shown, retry offered]
      ↓
[Back to Idle]
```

### Per-State Documentation

For every state, document:
- What is visible / hidden?
- What is enabled / disabled?
- What data is present?
- What transitions are possible?
- What triggers each transition?

### Container-Level State via `data-state`

```html
<!-- State on the container — CSS responds automatically -->
<section class="orders-container" data-state="loading">
```

```css
/* CSS handles state visuals — no JS style manipulation */
.orders-container[data-state="loading"] .ord-list {
  opacity: 0.5;
  pointer-events: none;
}
.orders-container[data-state="loading"] .ord-spinner {
  display: block;
}
.orders-container[data-state="error"] .ord-error-msg {
  display: block;
}
```

```js
// JS only sets the data-state — CSS does the rest
this._root.dataset.state = 'loading';
this._root.dataset.state = 'idle';
```

---

## 15. Phase 11 — Documentation & Comments

*Based on Compact Comments Guide — HTML/CSS/JS.*

### HTML Comments — 3 Levels Only

```html
<!-- ============================================================ HEADER START -->
<header class="site-header" role="banner">

  <!-- NAV: Desktop only — offcanvas used on mobile (<992px) -->
  <nav class="main-nav d-none d-lg-flex" aria-label="Main navigation">

    <!-- Aria-live: announces cart count to screen readers -->
    <span class="cart-count" aria-live="polite">0</span>

  </nav><!-- /main-nav -->

</header>
<!-- ============================================================== HEADER END -->
```

### CSS Comments

```css
/* ============================================================
   TABLE OF CONTENTS
   0. Tokens & Reset
   1. Container Layout
   2. Child Elements
   3. Modals
   4. States
   5. Animations (@keyframes)
   6. Responsive (@media)
   ============================================================ */

/* ============================================================
   0. TOKENS & RESET
   ============================================================ */

.orders-container {
  --ord-color-new:       #0d6efd;   /* new order accent */
  --ord-color-cancelled: #dc3545;   /* cancelled state */
  --ord-radius:          0.5rem;    /* consistent rounding */
  --ord-gap:             1rem;      /* internal spacing */
}

/* 80px = header height; keeps content below sticky bar */
.page-content { padding-top: 80px; }

/* HACK: Safari — min-height on flex column requires explicit height */
.orders-container { height: 1px; min-height: 300px; }
```

### JS Comments

```js
/**
 * cart.js — Shopping cart logic
 *
 * Handles: add/remove items, quantity update, localStorage sync,
 *          and cart count badge in the header.
 *
 * Depends on: utils.js (formatPrice), main.js (showToast)
 */

/**
 * Add a product to the cart.
 * @param {string} id        - Product ID
 * @param {number} qty       - Quantity to add (default: 1)
 * @param {Object} [options] - { silent: bool } — skip toast notification
 * @returns {Object} Updated cart state
 */
function addToCart(id, qty = 1, options = {}) { ... }

// Debounce: prevents API call on every keystroke, fires after 350ms idle
const onSearch = debounce(fetchResults, 350);

// TODO: Replace localStorage with IndexedDB for large carts
// FIXME: Race condition when user clicks Add twice rapidly
// HACK: Timeout needed — Bootstrap modal transition fires before DOM settles
// NOTE: formatPrice expects cents, not dollars (100 = $1.00)
// WARNING: Do not mutate cartState directly — use setCart() to trigger re-render
// PERF: Avoid calling this inside scroll — use requestAnimationFrame
```

---

## 16. Phase 12 — Bootstrap Conflict Detection

### The Problem

Bootstrap has its own class names, CSS variables, and JS plugins. Custom code must coexist without breaking the Bootstrap design system.

### Conflict Resolution Rules (ranked by Hierarchy from §2)

**Rule 1 — Never override Bootstrap globals (RANK 0)**
```css
/* ❌ FORBIDDEN — breaks Bootstrap globally */
.btn { background: red; }

/* ✅ CORRECT — scoped override, RANK 0 compliant */
.orders-container .btn { background: var(--ord-btn-bg); }
```

**Rule 2 — Prefix all custom classes**
```css
/* Custom classes: [prefix]-*, u-* */
.ord-card { ... }
.u-text-balance { text-wrap: balance; }
/* Never: .card, .modal, .btn — these are Bootstrap territory */
```

**Rule 3 — Override Bootstrap tokens via CSS variables**
```css
/* ✅ Override via token layer — not by targeting Bootstrap selectors */
.orders-container {
  --bs-primary: #your-color;      /* scoped to this container */
  --bs-border-radius: 0.5rem;
}
/* Or globally if intentional: */
:root { --bs-primary: #your-color; }
```

**Rule 4 — Modal inside container (RANK 0)**
```html
<!-- ✅ Inside — inherits container tokens, stays scoped -->
<section class="orders-container">
  <div class="ord-modal-overlay" ...>...</div>
</section>

<!-- ❌ Outside — tokens broken, CSS scoping violated -->
<div class="ord-modal-overlay" ...>...</div>
<section class="orders-container">...</section>
```

**Rule 5 — Z-index stack awareness**

```css
/* Document your z-index choices */
.orders-container {
  --z-dropdown: 100;
  --z-sticky:   200;
  --z-modal:    300;    /* Bootstrap modals are 1055, ours are below */
  --z-toast:    400;
}
/* Bootstrap z-index reference:
   Dropdown:  1000
   Sticky:    1020
   Fixed:     1030
   Backdrop:  1040
   Modal:     1055
   Popover:   1070
   Tooltip:   1080
*/
```

**Rule 6 — Bootstrap JS plugin conflict check**
```js
// Check before initialising — never double-init
if (!bootstrap.Modal.getInstance(el)) {
  new bootstrap.Modal(el, options);
}
// Use Bootstrap's own API — never hide/show modals via CSS directly
const modal = bootstrap.Modal.getInstance(el);
modal?.hide();
```

### Pre-Ship Conflict Checklist

- [ ] Bootstrap grid tested in DevTools — no custom CSS breaks it
- [ ] All Bootstrap interactive components work: modal, dropdown, tooltip, collapse, offcanvas, tab
- [ ] `--bs-*` variable overrides do not cascade unexpectedly into unrelated components
- [ ] Z-index stack tested — modals layer over dropdowns, tooltips over modals
- [ ] No `!important` in custom rules except scoped + documented Bootstrap overrides
- [ ] Custom `@keyframes` names carry widget prefix (not `fadeIn` — that could conflict)

---

## 17. Phase 13 — Execution ("делай" / "do it")

**This phase begins ONLY when the user writes the explicit trigger.**

### What the AI produces

A self-contained Bootstrap 5 HTML file that is:

- **Single `.html` file** — HTML + `<style>` + `<script>` (zero build step)
- **Bootstrap 5 via CDN** — no npm, no webpack
- **Static-first** — maximum of the UI in pure HTML+CSS+Bootstrap declarative
- **ES6+ JS only where genuinely needed** — Containerization v4 pattern
- **All comments in English** — per enterprise standard, Compact Comments Guide format
- **Production-ready** — not a prototype

### Output file structure

```
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- ============================================================ META START -->
  <!-- Charset, viewport, title, description, OG tags           -->
  <!-- ============================================================== META END -->

  <!-- Bootstrap 5 CSS CDN -->

  <style>
    /* ============================================================
       TABLE OF CONTENTS
       0. Tokens & Reset
       1. [Component] Container
       2. [Component] Children
       3. [Component] Modal
       4. States
       5. Animations
       6. Responsive
       ============================================================ */
  </style>
</head>
<body>

  <!-- Skip navigation (a11y) -->
  <a class="visually-hidden-focusable" href="#main-content">Skip to main content</a>

  <!-- ============================================================ HEADER START -->
  <header class="site-header" role="banner">...</header>
  <!-- ============================================================== HEADER END -->

  <!-- ============================================================ MAIN START -->
  <main id="main-content" role="main">

    <!-- [Widget]: static section — HTML+CSS only, no JS -->
    <section class="widget-a-container" aria-label="...">
      ...
    </section><!-- /widget-a-container -->

    <!-- [Widget]: dynamic section — JS Controller -->
    <section class="widget-b-container" aria-label="...">
      <!-- markup -->
      <!-- modal inside container -->
    </section><!-- /widget-b-container -->

  </main>
  <!-- ============================================================== MAIN END -->

  <!-- ============================================================ FOOTER START -->
  <footer class="site-footer" role="contentinfo">...</footer>
  <!-- ============================================================= FOOTER END -->

  <!-- Bootstrap 5 JS CDN (defer) -->

  <script>
    /**
     * main.js — Application entry point
     *
     * Static components: no init needed.
     * Dynamic components: initialised below on DOMContentLoaded.
     */

    /* [WidgetBController] — only exists because: [reason JS is needed] */
    class WidgetBController { ... }

    document.addEventListener('DOMContentLoaded', () => {
      new WidgetBController('.widget-b-container');
    });
  </script>

</body>
</html>
```

---

## 18. Phase 14 — Enterprise Production Checklist

### Code Quality
- [ ] Zero `console.log` in production code
- [ ] All `TODO` comments have context/reason
- [ ] No commented-out dead code
- [ ] No hardcoded URLs, credentials, or magic numbers (use `static CONFIG = { ... }`)
- [ ] Constants named and documented

### Static vs. Dynamic Audit
- [ ] Every `<script>` block justified — could this be CSS/HTML instead?
- [ ] Bootstrap `data-bs-*` used for all Bootstrap-handleable interactions
- [ ] CSS `:empty`, `:hover`, `:focus-within`, `data-state` used for state visuals
- [ ] No JS for pure visual transitions (use CSS `transition` / `@keyframes`)

### Containerization Compliance
- [ ] Every component has a scoped container class
- [ ] Every CSS selector starts with the container class
- [ ] All JS hooks are `data-ref` / `data-action` / `data-id` / `data-state`
- [ ] No `getElementById`, `querySelector('.class')`, `$('#id')` for logic
- [ ] Modals inside their parent container
- [ ] CSS tokens (`--prefix-name`) declared on the container element
- [ ] `@keyframes` names carry widget prefix

### Performance
- [ ] Images lazy-loaded (`loading="lazy"`)
- [ ] Scripts non-blocking (`defer` or before `</body>`)
- [ ] Bootstrap from CDN (cached across sites)
- [ ] No layout thrashing (all reads before writes)
- [ ] `scroll`, `touchstart`, `touchmove` listeners are `passive: true`
- [ ] `scroll`, `mousemove`, `resize` are throttled / debounced
- [ ] Styles via `classList` or `dataset.state`, not individual `.style.*`

### Security
- [ ] All `innerHTML` content passes through `_esc()`
- [ ] User input via `textContent` only where possible
- [ ] External data validated via `static _validate()`
- [ ] `FORBIDDEN_KEYS` blocks: `__proto__`, `constructor`, `prototype`
- [ ] External links have `rel="noopener noreferrer"`
- [ ] No `eval()` usage

### Accessibility
- [ ] Passes axe DevTools or Wave audit (zero critical violations)
- [ ] Full keyboard navigation functional
- [ ] Screen reader tested (VoiceOver / NVDA)
- [ ] Skip link present and functional
- [ ] All form fields labelled
- [ ] ARIA live regions announce dynamic changes

### W3C Standards
- [ ] HTML passes W3C Markup Validator
- [ ] CSS passes W3C CSS Validator
- [ ] Zero JS errors in browser console

### Bootstrap Design System
- [ ] No global Bootstrap selector overrides
- [ ] All BS interactive components functional (modal, dropdown, tooltip, collapse)
- [ ] Z-index stack correct
- [ ] `--bs-*` overrides scoped appropriately

### Browser Compatibility
- [ ] Chrome, Firefox, Safari, Edge — latest 2 versions
- [ ] iOS Safari 15+, Android Chrome

---

## 19. Communication Protocol

| User trigger | AI action |
|---|---|
| Sends screenshot | Acknowledge receipt, do nothing |
| Sends code | Acknowledge receipt, do nothing |
| *"analyze"* / *"проведи анализ"* | Phase 1 — System Analysis report |
| *"how would you refactor"* / *"как бы ты отрефакторил"* | Phase 2 — Plan only, no code |
| *"what needs JS"* / *"нужен ли js"* | Apply §3 Decision Tree to each component |
| *"containerization"* / *"контейнеризация"* | Phase 3 — Container architecture plan |
| *"static first"* | Phase 4 — identify what can be HTML+CSS only |
| *"UI/UX"* | Phase 6 audit |
| *"mobile"* / *"адаптация"* | Phase 7 analysis |
| *"a11y"* / *"доступность"* | Phase 8 audit |
| *"lifecycle"* / *"состояния"* | Phase 10 analysis |
| *"docs"* / *"комментарии"* | Phase 11 review |
| *"conflicts"* / *"конфликты бустрапа"* | Phase 12 audit |
| **"делай"** / **"do it"** | Phase 13 — produce full production HTML file |
| *"Enterprise Production"* | Phase 14 — run full checklist against output |

---

*Guide version: 2.0 Pro*
*Based on: Containerization v4 · Compact Comments Guide · Clean Code HTML/CSS/JS*
*Stack: Bootstrap 5 + ES6+ | No jQuery | Static-first | No build tools required*
*Language: English (all code and comments)*
