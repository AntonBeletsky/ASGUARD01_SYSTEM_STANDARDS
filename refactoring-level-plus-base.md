# Refactoring Level+ — AI-Assisted Code Quality Guide

> **Purpose**: A structured, repeatable workflow for refactoring legacy projects into production-grade, enterprise-quality code using AI assistance. The goal is not just "make it work" — it's *make it excellent*.

---

## Table of Contents

1. [Overview](#overview)
2. [Phase 0 — Input & Context Collection](#phase-0--input--context-collection)
3. [Phase 1 — System Analysis](#phase-1--system-analysis)
4. [Phase 2 — Pre-Refactor Planning](#phase-2--pre-refactor-planning)
5. [Phase 3 — Technology Stack Decision](#phase-3--technology-stack-decision)
6. [Phase 4 — UI/UX Standards Audit](#phase-4--uiux-standards-audit)
7. [Phase 5 — Mobile & Responsive Adaptation](#phase-5--mobile--responsive-adaptation)
8. [Phase 6 — Accessibility (a11y)](#phase-6--accessibility-a11y)
9. [Phase 7 — W3C Standards Compliance](#phase-7--w3c-standards-compliance)
10. [Phase 8 — Lifecycle & State Analysis](#phase-8--lifecycle--state-analysis)
11. [Phase 9 — Documentation & Comments](#phase-9--documentation--comments)
12. [Phase 10 — Conflict Detection & Design System Safety](#phase-10--conflict-detection--design-system-safety)
13. [Phase 11 — Execution ("делай" / "do it")](#phase-11--execution-делай--do-it)
14. [Phase 12 — Enterprise Production Checklist](#phase-12--enterprise-production-checklist)
15. [Communication Protocol](#communication-protocol)

---

## Overview

This guide defines a **multi-phase AI-assisted refactoring workflow**. Each phase has a clear input, analysis step, and output. AI acts as a senior engineer and code reviewer — it **listens first, analyzes deeply, and only acts on explicit instruction**.

**Core philosophy:**
- `READ → ANALYZE → PLAN → CONFIRM → EXECUTE`
- Never refactor blindly. Always understand *why* before *how*.
- Every decision must be justified by code quality, standards, or user value.

---

## Phase 0 — Input & Context Collection

### What the user does:
- Shares **screenshots** of the running application
- Shares **source code** (paste, upload, or link)

### What the AI does:
1. **Acknowledge receipt** — confirm what was received (screenshots + code)
2. **Do nothing else yet** — no suggestions, no refactoring, no opinions
3. Wait for explicit instruction to proceed

### Rule:
> "While I haven't written **делай** / **do it** — AI only collects and reads."

---

## Phase 1 — System Analysis

Triggered by: *"Conduct a full system analysis"*

The AI performs a complete audit of the provided code and screenshots.

### 1.1 Code Analysis

| Dimension | What to look for |
|---|---|
| **Architecture** | Separation of concerns, coupling, cohesion |
| **Patterns** | Anti-patterns, spaghetti code, god objects |
| **Dependencies** | Outdated libraries, jQuery vs. modern JS |
| **Data flow** | How data moves through the app |
| **Error handling** | Missing try/catch, unchecked nulls, silent failures |
| **Performance** | N+1 queries, blocking operations, memory leaks |
| **Security** | XSS vectors, unvalidated input, exposed secrets |
| **Testability** | Pure functions, side effects, mocking surface |

### 1.2 Screenshot Analysis

- Map UI to underlying code structures
- Identify inconsistencies between visual state and logic
- Note UX anti-patterns visible in the interface
- Spot layout issues, broken responsiveness, accessibility failures

### 1.3 Output format:

```
## System Analysis Report

### What the project does
[1-3 sentences describing the application's purpose]

### Tech stack detected
[List technologies, versions if visible]

### Critical issues (must fix)
[Numbered list]

### Code quality issues (should fix)
[Numbered list]

### Observations (nice to fix)
[Numbered list]

### What works well (keep it)
[Numbered list]
```

---

## Phase 2 — Pre-Refactor Planning

Triggered by: *"How would you refactor this project?"* / *"But don't refactor yet"*

### Goal: Produce a refactoring plan — not code.

The AI must:

1. **Analyze the project's purpose and tasks** — what problem does it solve?
2. **Propose a target architecture** — what should it look like after refactoring?
3. **Define technology choices** — why Bootstrap 5? why ES6+ instead of jQuery?
4. **List every change** — what gets removed, replaced, rewritten, restructured
5. **Estimate risk** — what could break during refactoring?

### Output format:

```
## Refactoring Plan

### Project purpose (re-confirmed)
[...]

### Proposed stack
- HTML5 + Bootstrap 5.x (CSS framework)
- Vanilla ES6+ (no jQuery)
- [Other libs if justified]

### Why this stack
[Technical justification — performance, bundle size, maintainability, standards]

### Changes summary
| Old | New | Reason |
|---|---|---|
| jQuery $.ajax | fetch() / async-await | Native, no dep |
| jQuery DOM | document.querySelector | Native ES6 |
| Custom CSS grid | Bootstrap Grid | Consistency |

### Risk areas
[...]

### Files affected
[...]
```

---

## Phase 3 — Technology Stack Decision

### Bootstrap 5 + ES6 — Why this combination:

**Bootstrap 5:**
- No jQuery dependency (unlike Bootstrap 4)
- Mobile-first grid system
- Design system tokens (CSS variables)
- Accessible components out of the box
- Widely maintained, W3C compatible

**ES6+ (no jQuery):**
- Native browser APIs are mature and fast
- Smaller bundle (no 30KB jQuery)
- Better IDE support and type inference
- Async/await instead of callback hell
- Modules (`import`/`export`) for clean architecture

### Migration map (jQuery → ES6):

```javascript
// BEFORE (jQuery)
$(document).ready(function() { ... });
$('#btn').click(function() { ... });
$.ajax({ url: '/api', success: function(data) { ... } });
$('.item').addClass('active');
$('#modal').show();

// AFTER (ES6)
document.addEventListener('DOMContentLoaded', () => { ... });
document.getElementById('btn').addEventListener('click', () => { ... });
const data = await fetch('/api').then(r => r.json());
document.querySelector('.item').classList.add('active');
const modal = new bootstrap.Modal(document.getElementById('modal'));
modal.show();
```

---

## Phase 4 — UI/UX Standards Audit

### Checklist before any UI refactor:

**Visual consistency:**
- [ ] Single color palette (use Bootstrap CSS variables or custom `--bs-*` overrides)
- [ ] Consistent spacing scale (Bootstrap's `m-*`, `p-*` or custom rem scale)
- [ ] Typography hierarchy (h1-h6 meaningful, not decorative)
- [ ] Icon system consistent (one library: Bootstrap Icons, Heroicons, etc.)
- [ ] Button states defined (default, hover, focus, disabled, loading)

**UX flows:**
- [ ] User goals are achievable in ≤3 clicks
- [ ] Error states are visible and informative
- [ ] Loading states prevent confusion
- [ ] Success feedback is explicit
- [ ] Destructive actions require confirmation

**Forms:**
- [ ] Labels always present (not placeholder-as-label)
- [ ] Validation messages inline and specific
- [ ] Required fields marked
- [ ] Autocomplete attributes set

---

## Phase 5 — Mobile & Responsive Adaptation

### Bootstrap 5 breakpoints:

| Name | Size | Use case |
|---|---|---|
| `xs` | < 576px | Small phones |
| `sm` | ≥ 576px | Phones landscape |
| `md` | ≥ 768px | Tablets |
| `lg` | ≥ 992px | Laptops |
| `xl` | ≥ 1200px | Desktops |
| `xxl` | ≥ 1400px | Large screens |

### Rules for responsive refactor:

1. **Mobile-first** — start with `col-12`, add larger breakpoints as needed
2. **No fixed widths in pixels** — use `%`, `vw`, Bootstrap columns
3. **Touch targets** — minimum `44×44px` (WCAG 2.5.5)
4. **Font sizes** — minimum `16px` body, `14px` secondary, never below `12px`
5. **Viewport meta** — always present:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```
6. **Images** — always `img-fluid` or `max-width: 100%`
7. **Tables** — wrap in `table-responsive` for horizontal scroll
8. **Navigation** — collapses to hamburger on mobile (`navbar-toggler`)
9. **Modals** — full-screen on `xs`, centered on larger screens
10. **Test on real devices** — not just browser DevTools resize

---

## Phase 6 — Accessibility (a11y)

### WCAG 2.1 AA — Required standards:

**Perceivable:**
- [ ] All images have `alt` text (empty `alt=""` for decorative)
- [ ] Color is not the only means of conveying information
- [ ] Text contrast ratio ≥ 4.5:1 (normal text), ≥ 3:1 (large text)
- [ ] Content doesn't rely on audio/visual alone

**Operable:**
- [ ] All functionality keyboard-accessible (`Tab`, `Enter`, `Escape`, arrows)
- [ ] No keyboard traps
- [ ] Skip navigation link (`<a class="visually-hidden-focusable" href="#main">`)
- [ ] Focus visible at all times (`outline` not removed without replacement)
- [ ] Touch targets ≥ 44×44px

**Understandable:**
- [ ] `lang` attribute on `<html>`
- [ ] Form labels programmatically associated (`for` + `id`)
- [ ] Error messages describe the problem, not just "invalid"
- [ ] Consistent navigation across pages

**Robust:**
- [ ] Valid HTML (passes W3C validator)
- [ ] ARIA used correctly (`role`, `aria-label`, `aria-describedby`, `aria-live`)
- [ ] No ARIA on elements that already have semantic meaning
- [ ] Works with VoiceOver, NVDA, screen readers

### Bootstrap 5 a11y helpers:
```html
<!-- Visually hidden but screen-reader accessible -->
<span class="visually-hidden">Loading...</span>

<!-- Skip link -->
<a class="visually-hidden-focusable" href="#main-content">Skip to main content</a>

<!-- ARIA live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true" class="visually-hidden" id="status"></div>
```

---

## Phase 7 — W3C Standards Compliance

### HTML5:
- [ ] `<!DOCTYPE html>` present
- [ ] `<html lang="en">` (or correct locale)
- [ ] `<meta charset="UTF-8">`
- [ ] `<title>` meaningful and unique per page
- [ ] Semantic elements used (`<header>`, `<main>`, `<nav>`, `<article>`, `<section>`, `<footer>`)
- [ ] No deprecated tags (`<center>`, `<font>`, `<b>` for styling)
- [ ] No inline styles (except dynamic/JS-driven)
- [ ] Valid nesting (no `<div>` inside `<p>`, no block inside inline)

### CSS3:
- [ ] CSS variables for theming (`--primary-color`, `--spacing-unit`)
- [ ] No `!important` (except Bootstrap overrides with justification)
- [ ] BEM or scoped class naming to avoid Bootstrap conflicts
- [ ] Media queries mobile-first (`min-width`, not `max-width`)
- [ ] No vendor prefixes without autoprefixer

### JavaScript (ES6+):
- [ ] `'use strict'` or ES modules (implicit strict)
- [ ] `const`/`let` — never `var`
- [ ] Arrow functions for callbacks
- [ ] Async/await for async operations
- [ ] Proper error handling (`try/catch` in every async function)
- [ ] Event delegation where appropriate
- [ ] No global namespace pollution
- [ ] No `eval()`, no `innerHTML` with user data (XSS)

---

## Phase 8 — Lifecycle & State Analysis

Before refactoring, map the application's lifecycle:

### Application states:

```
[Initial Load]
     ↓
[Idle / Default State]
     ↓          ↓
[User Action]  [System Event]
     ↓
[Loading State]  ← show spinner, disable UI
     ↓
[Success State]  ← show result, enable UI
[Error State]    ← show error, offer retry
     ↓
[Updated State]  ← reflect changes
```

### What to document per state:
- What is visible/hidden?
- What is enabled/disabled?
- What data is present?
- What transitions are possible?
- What triggers the transition?

### State management in ES6 (no framework):

```javascript
/**
 * Application State Manager
 * Single source of truth for UI state
 */
const AppState = (() => {
  let state = {
    status: 'idle', // idle | loading | success | error
    data: null,
    error: null,
  };

  const listeners = new Set();

  return {
    get: () => ({ ...state }),
    set(patch) {
      state = { ...state, ...patch };
      listeners.forEach(fn => fn(state));
    },
    subscribe(fn) {
      listeners.add(fn);
      return () => listeners.delete(fn); // unsubscribe
    },
  };
})();
```

---

## Phase 9 — Documentation & Comments

### Comment quality standards:

**BAD comments:**
```javascript
// increment i
i++;

// check if user exists
if (user) { ... }

// loop through items
items.forEach(item => { ... });
```

**GOOD comments:**
```javascript
/**
 * Fetches paginated user list from API.
 * Retries once on 503 (service unavailable).
 *
 * @param {number} page - 1-based page index
 * @param {number} limit - Items per page (max 100)
 * @returns {Promise<{users: User[], total: number}>}
 * @throws {ApiError} On non-retryable HTTP errors
 */
async function fetchUsers(page, limit) { ... }
```

### JSDoc rules:
- Every exported function: `@param`, `@returns`, `@throws`
- Every class: description + constructor params
- Every constant with non-obvious value: inline explanation
- Complex algorithms: explain *why*, not *what*

### HTML comments:
```html
<!-- ============================================================
     SECTION: User Dashboard Header
     Purpose: Displays greeting, avatar, and quick actions
     ============================================================ -->
<header class="dashboard-header" role="banner">
```

### CSS comments:
```css
/* ==========================================================================
   COMPONENT: Status Badge
   Variants: .badge--success | .badge--warning | .badge--error
   Note: Overrides Bootstrap .badge — scoped to .app-status-badge parent
   ========================================================================== */
```

---

## Phase 10 — Conflict Detection & Design System Safety

### The problem:
Bootstrap has its own class names, CSS variables, and JS plugins. Custom code must coexist without breaking the Bootstrap design system.

### Rules:

**1. Never override Bootstrap globals without scoping:**
```css
/* BAD — breaks Bootstrap system-wide */
.btn { background: red; }

/* GOOD — scoped to your component */
.app-hero .btn { background: var(--app-primary); }
```

**2. Use custom prefix for your classes:**
```css
/* Your classes: app-*, page-*, u-* */
.app-card { ... }
.page-header { ... }
.u-text-balance { text-wrap: balance; }
```

**3. Override Bootstrap via CSS variables (not selectors):**
```css
/* GOOD — uses Bootstrap's own token system */
:root {
  --bs-primary: #your-color;
  --bs-border-radius: 0.5rem;
  --bs-font-sans-serif: 'Your Font', sans-serif;
}
```

**4. Wrap custom sections in containers:**
```html
<div class="app-wrapper">
  <!-- Your custom components here -->
  <!-- Bootstrap classes still work inside -->
</div>
```

**5. Check Bootstrap JS plugin conflicts:**
```javascript
// Bootstrap plugins are on the bootstrap global
const myModal = new bootstrap.Modal(el, options);

// Never re-init if already initialized
if (!bootstrap.Modal.getInstance(el)) {
  new bootstrap.Modal(el, options);
}
```

**6. Audit checklist before shipping:**
- [ ] Run Bootstrap's grid in DevTools — check no custom CSS breaks it
- [ ] Test all Bootstrap interactive components (modal, dropdown, tooltip, collapse)
- [ ] Verify `--bs-*` variable overrides don't cascade unexpectedly
- [ ] Check z-index stack — modals, dropdowns, tooltips must layer correctly

---

## Phase 11 — Execution ("делай" / "do it")

This phase begins **only** when the user writes the explicit trigger word.

### What the AI produces:

A **self-contained Bootstrap 5 HTML page** that is:

- Single `.html` file (HTML + `<style>` + `<script>`)
- Bootstrap 5 via CDN (no build step required)
- ES6+ JavaScript (no jQuery, no Babel needed for modern browsers)
- Full implementation of everything analyzed in Phases 1-10
- All comments in **English** per enterprise standard
- Production-ready, not a prototype

### File structure (single file):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta & SEO -->
  <!-- Bootstrap 5 CSS CDN -->
  <!-- Custom CSS variables & overrides -->
  <!-- Component styles (scoped, prefixed) -->
</head>
<body>
  <!-- Skip navigation (a11y) -->
  <!-- ARIA live region (a11y) -->

  <!-- Application markup -->
  <!-- Semantic HTML5 structure -->
  <!-- Bootstrap components -->
  <!-- Custom components (app-* prefix) -->

  <!-- Bootstrap 5 JS CDN -->
  <!-- Application JS (ES6 modules or IIFE) -->
</body>
</html>
```

---

## Phase 12 — Enterprise Production Checklist

Before declaring the refactor complete:

### Code quality:
- [ ] Zero `console.log` in production code
- [ ] All `TODO` comments have ticket references
- [ ] No commented-out dead code
- [ ] No hardcoded URLs, credentials, or magic numbers
- [ ] Constants extracted and named

### Performance:
- [ ] Images optimized and lazy-loaded (`loading="lazy"`)
- [ ] No render-blocking scripts (use `defer` or place before `</body>`)
- [ ] Bootstrap loaded from CDN (cached across sites)
- [ ] CSS critical path minimal

### Security:
- [ ] No `innerHTML` with user-controlled data
- [ ] Forms have CSRF protection (if server-side)
- [ ] External links have `rel="noopener noreferrer"`
- [ ] `Content-Security-Policy` header defined

### Accessibility:
- [ ] Passes axe DevTools or Wave audit
- [ ] Keyboard navigation fully functional
- [ ] Screen reader tested

### Standards:
- [ ] HTML passes W3C Markup Validator
- [ ] CSS passes W3C CSS Validator
- [ ] No JS errors in browser console

### Browser compatibility:
- [ ] Chrome, Firefox, Safari, Edge — latest 2 versions
- [ ] iOS Safari, Android Chrome

---

## Communication Protocol

| Trigger | AI action |
|---|---|
| User sends screenshot | Acknowledge receipt, do nothing |
| User sends code | Acknowledge receipt, do nothing |
| *"analyze the code"* | Run Phase 1, output report |
| *"how would you refactor"* | Run Phase 2, output plan only |
| *"UI/UX standards"* | Run Phase 4 audit |
| *"mobile adaptation"* | Run Phase 5 analysis |
| *"a11y"* | Run Phase 6 audit |
| *"lifecycle / states"* | Run Phase 8 analysis |
| *"docs / comments"* | Run Phase 9 review |
| *"conflicts / design system"* | Run Phase 10 audit |
| **"делай" / "do it"** | Execute Phase 11 — produce full code |
| *"Enterprise Production"* | Run Phase 12 checklist against output |

---

*Guide version: 1.0 — Refactoring Level+*  
*Language: English (code & comments) / Russian (user communication)*  
*Stack: Bootstrap 5 + ES6+ | No jQuery | No build tools required*
