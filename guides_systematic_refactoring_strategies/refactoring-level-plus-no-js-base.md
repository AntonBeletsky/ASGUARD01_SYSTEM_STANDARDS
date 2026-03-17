# Refactoring Level+ No-JS — Base
## AI-Assisted Code Quality Guide — Static HTML + CSS Edition

> **Purpose**: A structured workflow for refactoring static projects — product catalogs,
> landing pages, presentation pages, templates where content is fixed and no runtime
> data changes are needed.
>
> **Core rule**: Bootstrap JS CDN is always connected and must never be broken.
> Custom `<script>` blocks are forbidden unless explicitly justified.
> Everything Bootstrap can do natively — Bootstrap does. You don't write JS for it.

> **Version**: 1.0 No-JS Base — derived from Refactoring Level+ Base v1.0

---

## Table of Contents

1. [Core Philosophy](#1-core-philosophy)
2. [Iron Laws](#2-iron-laws)
3. [Phase 0 — Input & Context Collection](#3-phase-0--input--context-collection)
4. [Phase 1 — System Analysis](#4-phase-1--system-analysis)
5. [Phase 2 — Pre-Refactor Planning](#5-phase-2--pre-refactor-planning)
6. [Phase 3 — Technology Stack](#6-phase-3--technology-stack)
7. [Phase 4 — CSS-Only Interaction Patterns](#7-phase-4--css-only-interaction-patterns)
8. [Phase 5 — UI/UX Standards Audit](#8-phase-5--uiux-standards-audit)
9. [Phase 6 — Mobile & Responsive Adaptation](#9-phase-6--mobile--responsive-adaptation)
10. [Phase 7 — Accessibility (a11y)](#10-phase-7--accessibility-a11y)
11. [Phase 8 — W3C Standards Compliance](#11-phase-8--w3c-standards-compliance)
12. [Phase 9 — Documentation & Comments](#12-phase-9--documentation--comments)
13. [Phase 10 — Bootstrap Conflict Detection](#13-phase-10--bootstrap-conflict-detection)
14. [Phase 11 — Execution ("делай" / "do it")](#14-phase-11--execution-делай--do-it)
15. [Phase 12 — Production Checklist](#15-phase-12--production-checklist)
16. [Communication Protocol](#16-communication-protocol)

---

## 1. Core Philosophy

```
READ → ANALYZE → PLAN → CONFIRM → EXECUTE
```

- Never refactor blindly. Always understand *why* before *how*.
- **Bootstrap does its job. You don't rewrite what Bootstrap already solves.**
- Static by default. Custom JS only when HTML + CSS + Bootstrap cannot do it.
- Every decision must be justified by code quality, standards, or user value.

---

## 2. Iron Laws

These laws have no exceptions. Violating any one of them invalidates the output.

```
╔══════════════════════════════════════════════════════════════╗
║  IRON LAW 1 — NEVER BREAK BOOTSTRAP JS                      ║
║                                                              ║
║  Bootstrap JS CDN is always included. Always.               ║
║  Bootstrap's own components (navbar, collapse, tooltip,      ║
║  dropdown, offcanvas, carousel) work through data-bs-*       ║
║  attributes — do not touch, wrap, or override their JS.      ║
║  If a Bootstrap component stops working — that is a bug.     ║
╠══════════════════════════════════════════════════════════════╣
║  IRON LAW 2 — NO CUSTOM SCRIPT BLOCKS                       ║
║                                                              ║
║  No <script> tag with custom logic.                          ║
║  No inline JS (onclick="", onload="", href="javascript:").   ║
║  No .js files.                                               ║
║  If a feature requires custom JS — it does not belong        ║
║  in a No-JS project. Redesign with CSS or escalate           ║
║  to the Pro guide.                                           ║
╠══════════════════════════════════════════════════════════════╣
║  IRON LAW 3 — BOOTSTRAP HANDLES BOOTSTRAP                   ║
║                                                              ║
║  Never replace a working Bootstrap component with            ║
║  a custom CSS-only hack if Bootstrap already solves it.      ║
║  data-bs-toggle, data-bs-target, data-bs-dismiss — these     ║
║  are the correct tools. Use them as-is.                      ║
╚══════════════════════════════════════════════════════════════╝
```

### What "No Custom JS" means in practice

| Situation | Correct approach |
|---|---|
| Mobile nav toggle | Bootstrap `navbar-toggler` + `data-bs-toggle="collapse"` |
| Accordion / FAQ | Bootstrap `accordion` + `data-bs-toggle="collapse"` |
| Image carousel | Bootstrap `carousel` + `data-bs-ride="carousel"` |
| Tabs | Bootstrap `nav-tabs` + `data-bs-toggle="tab"` |
| Tooltip | Bootstrap `data-bs-toggle="tooltip"` (CDN auto-init) |
| Offcanvas menu | Bootstrap `data-bs-toggle="offcanvas"` |
| Dismiss alert | Bootstrap `data-bs-dismiss="alert"` |
| Hover effect | CSS `:hover` + `transition` |
| Simple accordion (no BS) | HTML `<details>` + `<summary>` |
| Show/hide on click | CSS `:target` or `<details>` |
| Form validation (basic) | HTML5 `required`, `pattern`, `type`, `minlength` |
| Sticky header | CSS `position: sticky` |
| Smooth scroll | CSS `scroll-behavior: smooth` |
| Loading animation | CSS `@keyframes` |
| Dark/light preference | CSS `prefers-color-scheme` |

---

## 3. Phase 0 — Input & Context Collection

### What the user does:
- Shares **screenshots** of the running page
- Shares **source code** (paste, upload, or link)

### What the AI does:
1. Acknowledge receipt — confirm what was received
2. **Do nothing else** — no suggestions, no refactoring, no opinions
3. Wait for explicit instruction to proceed

> **Rule:** Until the user writes **"делай"** / **"do it"** — AI only collects and reads.

---

## 4. Phase 1 — System Analysis

*Triggered by: "analyze" / "проведи анализ"*

### 1.1 Code Analysis

| Dimension | What to look for |
|---|---|
| **Custom JS presence** | Any `<script>`, inline handlers, `.js` files — flag every instance |
| **Bootstrap JS integrity** | Is Bootstrap CDN present? Are `data-bs-*` components functional? |
| **Unnecessary JS** | Features handled by JS that CSS or Bootstrap already solves |
| **Architecture** | Separation of concerns, coupling, cohesion |
| **CSS quality** | Global leaks, missing scoping, Bootstrap selector conflicts |
| **HTML semantics** | Correct semantic tags, ARIA, heading hierarchy |
| **Performance** | Render-blocking resources, oversized images, unused CSS |
| **Accessibility** | Missing alt, contrast issues, keyboard navigation |

### 1.2 Screenshot Analysis

- Map every UI element — is it static content or interactive?
- For every interactive element: can Bootstrap declarative or CSS handle it?
- Note layout issues, broken responsiveness, a11y failures

### 1.3 Analysis Output Format

```
## System Analysis Report

### What the project does
[1-3 sentences]

### Tech stack detected
[Technologies + versions if visible]

### Custom JS inventory
| File / Block | What it does | Replacement | Priority |
|---|---|---|---|
| main.js: navbar scroll | Adds .sticky class | CSS position:sticky | Must remove |
| inline onclick | Opens accordion | Bootstrap collapse | Must remove |

### Bootstrap JS status
[Is CDN present? Are data-bs-* components working? Any broken components?]

### Critical issues (must fix)
[Numbered list]

### Code quality issues (should fix)
[Numbered list]

### What works well (keep it)
[Numbered list]
```

---

## 5. Phase 2 — Pre-Refactor Planning

*Triggered by: "how would you refactor" — output plan only, no code*

The AI must produce:

1. **Project purpose** — what does this page display?
2. **JS elimination map** — each piece of custom JS → what replaces it
3. **Bootstrap components map** — which Bootstrap components to use and where
4. **CSS-only patterns** — where pure CSS solves the interaction
5. **Change list** — what gets removed, replaced, restructured
6. **Risk assessment** — what Bootstrap behavior could be accidentally broken

### Output Format

```
## Refactoring Plan

### Project purpose
[...]

### JS elimination map
| Current JS | Replacement | How |
|---|---|---|
| Sticky nav scroll handler | CSS position:sticky | Delete JS block |
| Tab switching logic | Bootstrap nav-tabs | data-bs-toggle="tab" |
| Custom accordion | <details>/<summary> | Delete JS block |
| Carousel init code | Bootstrap carousel | data-bs-ride="carousel" |

### Bootstrap components to activate
| Component | Where | Attribute |
|---|---|---|
| Navbar collapse | Mobile menu | data-bs-toggle="collapse" |
| Offcanvas | Filters sidebar | data-bs-toggle="offcanvas" |
| Carousel | Hero banner | data-bs-ride="carousel" |

### CSS-only patterns
| Feature | CSS technique |
|---|---|
| Hover card effect | :hover + transform + transition |
| Active nav highlight | :target selector |
| Simple FAQ | <details> + <summary> |

### Risk areas
[Bootstrap components that might break during CSS cleanup]
```

---

## 6. Phase 3 — Technology Stack

### Stack: Bootstrap 5 CSS + Bootstrap 5 JS CDN. No custom JS.

```html
<!-- Bootstrap 5 CSS — always, first stylesheet -->
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      integrity="sha384-QWTKZyjpPbgXjNCM/X1EBk0VCnEYIKJ2NLfCBfVEBSH7SkSBCYHPSFGJ7pHB3Kn"
      crossorigin="anonymous">

<!-- Custom styles — always after Bootstrap CSS, never before -->
<style>
  /* Your scoped overrides here */
</style>

<!-- Bootstrap 5 JS Bundle (includes Popper) — always, last tag before </body> -->
<!-- IRON LAW 1: This tag is required. Never remove it. Never move it to <head>. -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmFLpQiHPEELnAXEWTdLB4k1S3p"
        crossorigin="anonymous"></script>

<!-- NO custom <script> block after this. This is a No-JS project. -->
```

### Why Bootstrap JS CDN is always included

Bootstrap's interactive components — `navbar`, `collapse`, `carousel`, `tooltip`,
`offcanvas`, `tab`, `dropdown`, `modal`, `alert dismiss` — require Bootstrap's own JS.
Removing the CDN tag silently breaks every one of these components with no console error.
Even on a "purely static" page, Bootstrap JS must be present to keep the design system intact.

### Why no custom JS

- A product catalog displays fixed data — it does not process or fetch it
- Navigation, accordions, carousels are solved by Bootstrap's declarative system
- Custom JS adds maintenance burden, security surface, and page weight
- CSS handles all visual state: `:hover`, `:focus`, `:active`, `transition`, `@keyframes`
- HTML5 handles basic form validation natively

---

## 7. Phase 4 — CSS-Only Interaction Patterns

**The complete toolkit for static pages. Apply these before considering anything else.**

### 4.1 Hover & Focus States

```css
/* Card hover — lift effect, no JS */
.cat-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.cat-container .cat-card:hover,
.cat-container .cat-card:focus-within {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* Button press feedback */
.cat-container .btn:active {
  transform: scale(0.97);
}

/* Reveal action layer on card hover */
.cat-container .cat-card__actions {
  opacity: 0;
  transition: opacity 0.2s ease;
}
.cat-container .cat-card:hover .cat-card__actions,
.cat-container .cat-card:focus-within .cat-card__actions {
  opacity: 1;
}
```

### 4.2 Native HTML Interactive Elements

```html
<!-- Accordion — zero JS, fully accessible, keyboard-friendly -->
<details class="cat-faq__item">
  <summary class="cat-faq__question">What is the return policy?</summary>
  <p class="cat-faq__answer">You may return any item within 30 days.</p>
</details><!-- /cat-faq__item -->

<!-- Progress bar — semantic HTML, no JS -->
<progress class="cat-progress" value="65" max="100" aria-label="65% complete">
  65%
</progress>

<!-- Form validation — HTML5 native, no JS -->
<input type="email"
       name="email"
       required
       pattern="[^@]+@[^@]+\.[^@]+"
       autocomplete="email"
       aria-describedby="email-hint"
       placeholder="your@email.com">
<span id="email-hint" class="form-text">We never share your email.</span>
```

### 4.3 CSS :target for Show/Hide Panels

```css
/* Panel visible only when URL hash matches its id */
.cat-panel {
  display: none;
}
.cat-panel:target {
  display: block;
}
```

```html
<a href="#info-panel" class="btn btn-outline-primary">Show details</a>

<div id="info-panel" class="cat-panel">
  <p>Panel content here.</p>
  <a href="#" class="btn btn-sm btn-secondary">Close</a>
</div>
```

### 4.4 CSS :checked for Filter Toggles

```css
/* Toggle via hidden checkbox — no JS */
.cat-toggle__input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.cat-toggle__panel {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.cat-toggle__input:checked ~ .cat-toggle__panel {
  max-height: 600px; /* generous max for variable content */
}
```

```html
<input type="checkbox" id="filter-toggle" class="cat-toggle__input">
<label for="filter-toggle" class="btn btn-outline-secondary">
  Show Filters
</label>
<div class="cat-toggle__panel">
  <!-- static filter checkboxes, no JS -->
</div>
```

### 4.5 Bootstrap Components — Declarative Only (No Custom JS)

```html
<!-- Mobile navigation — Bootstrap handles all toggle/collapse logic -->
<nav class="navbar navbar-expand-lg" aria-label="Main navigation">
  <button class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNav"
          aria-controls="mainNav"
          aria-expanded="false"
          aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="mainNav">
    <!-- nav items -->
  </div>
</nav>

<!-- Product image carousel — Bootstrap handles all slide logic -->
<div id="productCarousel"
     class="carousel slide"
     data-bs-ride="carousel"
     data-bs-interval="5000">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="product-1.jpg"
           class="d-block w-100 img-fluid"
           alt="Product front view"
           loading="lazy"
           width="800" height="600">
    </div>
    <div class="carousel-item">
      <img src="product-2.jpg"
           class="d-block w-100 img-fluid"
           alt="Product side view"
           loading="lazy"
           width="800" height="600">
    </div>
  </div>
  <button class="carousel-control-prev" type="button"
          data-bs-target="#productCarousel" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button"
          data-bs-target="#productCarousel" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

<!-- Offcanvas filter sidebar — Bootstrap handles open/close/backdrop -->
<button class="btn btn-outline-secondary"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#filterPanel"
        aria-controls="filterPanel">
  Filters
</button>
<div class="offcanvas offcanvas-start"
     id="filterPanel"
     aria-labelledby="filterPanelLabel">
  <div class="offcanvas-header">
    <h2 class="offcanvas-title" id="filterPanelLabel">Filters</h2>
    <button type="button"
            class="btn-close"
            data-bs-dismiss="offcanvas"
            aria-label="Close filters"></button>
  </div>
  <div class="offcanvas-body">
    <!-- static checkboxes — no JS needed -->
  </div>
</div>
```

### 4.6 CSS Animations

```css
/* PERFORMANCE: transform + opacity only — GPU composited, no layout reflow */

@keyframes cat-fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.cat-container .cat-card {
  animation: cat-fade-in 0.3s ease both;
}

/* Stagger grid items — CSS only, no JS */
.cat-container .cat-card:nth-child(1) { animation-delay: 0.05s; }
.cat-container .cat-card:nth-child(2) { animation-delay: 0.10s; }
.cat-container .cat-card:nth-child(3) { animation-delay: 0.15s; }
.cat-container .cat-card:nth-child(4) { animation-delay: 0.20s; }

/* Always respect user system preference */
@media (prefers-reduced-motion: reduce) {
  .cat-container .cat-card {
    animation: none;
  }
}
```

---

## 8. Phase 5 — UI/UX Standards Audit

### Visual Consistency

- [ ] Single color palette — Bootstrap `--bs-*` tokens or scoped container tokens
- [ ] Consistent spacing — Bootstrap `m-*`, `p-*` or custom `rem` scale
- [ ] Typography hierarchy — `h1`–`h6` meaningful, not decorative
- [ ] One icon library only (Bootstrap Icons, Heroicons, etc.)
- [ ] Hover/focus states defined for all interactive elements
- [ ] No mixed visual language — either Bootstrap native or fully custom, not half-half

### UX Flow

- [ ] Key information visible without scrolling on desktop
- [ ] Product cards show: image, name, price, primary action
- [ ] Empty states have messaging — no blank sections
- [ ] No dead links, no placeholder `href="#"` in production

### Forms (if present)

- [ ] Labels always present — never placeholder as label
- [ ] `required` fields marked visually and with `required` attribute
- [ ] `autocomplete` attributes set
- [ ] HTML5 validation attributes used: `type`, `pattern`, `minlength`, `maxlength`

---

## 9. Phase 6 — Mobile & Responsive Adaptation

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
5. **Viewport meta** — always:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```
6. **Images** — `img-fluid` + `loading="lazy"` + explicit `width`/`height` + meaningful `alt`
7. **Tables** — wrap in `<div class="table-responsive">`
8. **Navigation** — Bootstrap `navbar-toggler` for mobile collapse
9. **Product grid** — `col-6 col-md-4 col-lg-3` standard catalog pattern
10. **Test on real devices** — not only DevTools

---

## 10. Phase 7 — Accessibility (a11y)

### WCAG 2.1 AA — Required

**Perceivable:**
- [ ] All images have `alt` text (`alt=""` for decorative images)
- [ ] Color not the sole conveyor of information
- [ ] Contrast ratio ≥ 4.5:1 (normal text), ≥ 3:1 (large text / UI components)
- [ ] No content relying on sensory characteristics alone

**Operable:**
- [ ] All interactive elements keyboard-reachable (`Tab`, `Enter`, `Space`)
- [ ] No keyboard traps
- [ ] Skip navigation: `<a class="visually-hidden-focusable" href="#main-content">Skip to main</a>`
- [ ] Focus always visible — never `outline: none` without replacement
- [ ] Touch targets ≥ 44×44px

**Understandable:**
- [ ] `<html lang="en">` (or correct locale)
- [ ] Form labels associated via `for` + `id`, or `aria-label`
- [ ] Link text descriptive — no "click here", no "read more" without context

**Robust:**
- [ ] Valid HTML (W3C validator — zero errors)
- [ ] Bootstrap ARIA managed by Bootstrap itself — do not override `aria-expanded`,
      `aria-controls`, `aria-hidden` on Bootstrap components
- [ ] `<details>`/`<summary>` used correctly for custom accordions

### Product Card Pattern

```html
<!-- Correct accessible product card -->
<article class="cat-card-wrapper col-6 col-md-4 col-lg-3">
  <div class="cat-card">
    <a href="/product/blue-shoes" class="cat-card__img-link" tabindex="-1" aria-hidden="true">
      <img src="shoes.jpg"
           alt="Blue running shoes, side view"
           class="cat-card__img img-fluid"
           loading="lazy"
           width="400" height="300">
    </a>
    <div class="cat-card__body">
      <h3 class="cat-card__name">
        <a href="/product/blue-shoes" class="cat-card__link">Blue Running Shoes</a>
      </h3>
      <p class="cat-card__price">
        <span class="visually-hidden">Price:</span>$89.99
      </p>
    </div>
  </div>
</article><!-- /cat-card-wrapper -->
```

---

## 11. Phase 8 — W3C Standards Compliance

### HTML5

- [ ] `<!DOCTYPE html>` present
- [ ] `<html lang="en">` correct locale
- [ ] `<meta charset="UTF-8">`
- [ ] `<title>` meaningful and unique
- [ ] Semantic tags used: `<header>`, `<main>`, `<nav>`, `<article>`, `<section>`, `<footer>`
- [ ] Product items use `<article>` (standalone) or `<li>` (list context)
- [ ] No deprecated tags: `<center>`, `<font>`, `<b>` for styling
- [ ] No inline styles (except CSS custom property overrides)
- [ ] Valid nesting

### CSS3

- [ ] CSS variables for all tokens (`--prefix-name`)
- [ ] No `!important` except scoped Bootstrap overrides (commented + justified)
- [ ] All custom selectors start with the container class — no global leaks
- [ ] Media queries mobile-first (`min-width`)
- [ ] Animations use `transform` + `opacity` only (GPU composited, no layout reflow)
- [ ] `prefers-reduced-motion` respected for all animations

### No Custom JS = No JS Compliance Issues

Since there is no custom JavaScript, the following are automatically satisfied:
- No XSS via `innerHTML`
- No prototype pollution risk
- No event listener memory leaks
- No layout thrashing
- No unhandled promise rejections
- No `console.log` in production

---

## 12. Phase 9 — Documentation & Comments

### HTML Comments — 3 Levels

```html
<!-- ============================================================ CATALOG START -->
<section class="cat-container" aria-label="Product catalog">

  <!-- Grid: lg=4col / md=3col / sm=2col / xs=1col -->
  <div class="row g-4">

    <!-- Product card — repeat pattern for each item -->
    <article class="col-6 col-md-4 col-lg-3">
      ...
    </article>

  </div>

</section>
<!-- ============================================================== CATALOG END -->
```

### CSS Comments

```css
/* ============================================================
   TABLE OF CONTENTS
   0. Tokens & Reset
   1. Container Layout
   2. Product Card
   3. Filters
   4. Pagination
   5. Animations (@keyframes)
   6. Responsive (@media)
   ============================================================ */

/* ============================================================
   0. TOKENS & RESET
   ============================================================ */

.cat-container {
  --cat-card-radius:  0.75rem;          /* card corner rounding */
  --cat-card-shadow:  0 2px 8px rgba(0, 0, 0, 0.08);
  --cat-gap:          1.5rem;           /* grid gap */
  --cat-img-ratio:    4 / 3;            /* product image aspect ratio */
}

/* --- Card: hover state --- */

/* 4px lift — matches design spec for card interaction */
.cat-container .cat-card:hover {
  transform: translateY(-4px);
}

/* HACK: Safari — aspect-ratio on img requires explicit height reset */
.cat-container .cat-card__img {
  height: auto; /* overrides Safari's incorrect intrinsic sizing */
}
```

### No Custom JS = No JSDoc

There are no functions, classes, or modules to document.
HTML and CSS comments are the only documentation layer in a No-JS project.

---

## 13. Phase 10 — Bootstrap Conflict Detection

### The Problem

Bootstrap has its own class names, CSS variables, and JS behavior.
Custom CSS must coexist without breaking Bootstrap's design system or its component logic.

### Conflict Resolution Rules

**Rule 1 — Never override Bootstrap globals (Iron Law 1)**
```css
/* ❌ FORBIDDEN — breaks Bootstrap system-wide */
.btn { background: red; }
.card { border-radius: 0; }

/* ✅ CORRECT — scoped to your container */
.cat-container .btn { background: var(--cat-btn-bg); }
.cat-container .card { border-radius: var(--cat-card-radius); }
```

**Rule 2 — Prefix all custom classes**
```css
/* Custom prefix: cat-  (or your project prefix) */
.cat-card { ... }
.cat-grid { ... }
.cat-badge { ... }
/* NEVER use: .card, .badge, .btn — Bootstrap's namespace */
```

**Rule 3 — Override Bootstrap tokens via CSS variables, not selectors**
```css
/* Scoped token override — only affects this container */
.cat-container {
  --bs-primary:        #2d6a4f;
  --bs-border-radius:  0.75rem;
}
```

**Rule 4 — Never manually set Bootstrap-managed ARIA attributes**
```html
<!-- ✅ CORRECT — Bootstrap sets aria-expanded automatically on toggle -->
<button data-bs-toggle="collapse"
        data-bs-target="#nav"
        aria-expanded="false">

<!-- ❌ FORBIDDEN — setting aria-expanded="true" breaks Bootstrap's state machine -->
<button data-bs-toggle="collapse"
        data-bs-target="#nav"
        aria-expanded="true">
```

**Rule 5 — Never hide Bootstrap JS components with CSS alone**
```css
/* ❌ FORBIDDEN — carousel still initialises but renders broken */
#productCarousel { display: none; }

/* ✅ CORRECT — control Bootstrap components through their own API:
   data-bs-ride="false" to disable autoplay
   data-bs-interval="false" to stop cycling         */
```

**Rule 6 — Z-index awareness**
```css
/* Bootstrap z-index reference — never conflict unintentionally:
   Dropdown:  1000
   Sticky:    1020
   Fixed:     1030
   Backdrop:  1040
   Modal:     1055
   Popover:   1070
   Tooltip:   1080
*/
/* Custom overlays stay below 1000 or explicitly above 1080 with justification */
.cat-container .cat-overlay { z-index: 900; }
```

### Pre-Ship Bootstrap Verification

- [ ] All `data-bs-*` components functional: navbar collapse, carousel, offcanvas, accordion, tooltip
- [ ] `--bs-*` variable overrides scoped — not cascading into unrelated components
- [ ] No custom CSS targets Bootstrap's internal classes without container scope
- [ ] Bootstrap JS bundle `<script>` tag present before `</body>`
- [ ] No `!important` overriding Bootstrap component visibility

---

## 14. Phase 11 — Execution ("делай" / "do it")

**This phase begins ONLY when the user writes the explicit trigger.**

### What the AI produces

A self-contained Bootstrap 5 static HTML file:

- **Single `.html` file** — HTML + `<style>` only
- **Bootstrap 5 CSS CDN** — always first stylesheet
- **Bootstrap 5 JS Bundle CDN** — always last tag before `</body>` *(Iron Law 1)*
- **No custom `<script>` block** — Bootstrap JS handles all declarative interactions
- **All comments in English** — Compact Comments Guide format
- **Production-ready** — not a prototype

### Output File Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- ============================================================ META START -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="[Page description — used by search engines]">
  <title>[Meaningful page title]</title>
  <!-- ============================================================== META END -->

  <!-- Bootstrap 5 CSS — design system foundation, always first -->
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        integrity="sha384-QWTKZyjpPbgXjNCM/X1EBk0VCnEYIKJ2NLfCBfVEBSH7SkSBCYHPSFGJ7pHB3Kn"
        crossorigin="anonymous">

  <style>
    /* ============================================================
       TABLE OF CONTENTS
       0. Tokens & Reset
       1. [Section] Container
       2. [Section] Components
       3. Animations (@keyframes)
       4. Responsive (@media)
       ============================================================ */

    /* 0. TOKENS */
    /* 1. LAYOUT */
    /* 2. COMPONENTS */
    /* 3. ANIMATIONS */
    /* 4. RESPONSIVE */
  </style>
</head>
<body>

  <!-- Skip navigation — always first element in <body> (a11y) -->
  <a class="visually-hidden-focusable" href="#main-content">Skip to main content</a>

  <!-- ============================================================ HEADER START -->
  <header class="site-header" role="banner">
    <nav class="navbar navbar-expand-lg" aria-label="Main navigation">
      <!-- Bootstrap navbar — data-bs-toggle handles mobile collapse, no JS needed -->
    </nav>
  </header>
  <!-- ============================================================== HEADER END -->

  <!-- ============================================================== MAIN START -->
  <main id="main-content" role="main">

    <!-- [Section]: static content — HTML + CSS only -->
    <section class="[prefix]-container" aria-label="[Accessible section name]">
      <!--
        Bootstrap grid inside the container — works normally.
        All interactive Bootstrap elements use data-bs-* attributes.
        No custom JS. No inline handlers.
      -->
    </section><!-- /[prefix]-container -->

  </main>
  <!-- ================================================================ MAIN END -->

  <!-- ============================================================ FOOTER START -->
  <footer class="site-footer" role="contentinfo">
    <!-- Static footer -->
  </footer>
  <!-- ============================================================== FOOTER END -->

  <!-- ============================================================
       IRON LAW 1 — Bootstrap JS Bundle.
       NEVER remove this tag. NEVER move it to <head>.
       Required for: navbar, collapse, carousel, offcanvas,
                     tooltip, dropdown, tab, modal, alert dismiss.
       ============================================================ -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
          integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmFLpQiHPEELnAXEWTdLB4k1S3p"
          crossorigin="anonymous"></script>

  <!-- NO custom <script> block — this is a No-JS project. -->

</body>
</html>
```

---

## 15. Phase 12 — Production Checklist

### Iron Laws Verification (run first)
- [ ] Bootstrap JS CDN `<script>` tag present before `</body>` — **Iron Law 1**
- [ ] Zero custom `<script>` blocks in the file — **Iron Law 2**
- [ ] Zero inline JS: no `onclick`, `onload`, `href="javascript:..."` — **Iron Law 2**
- [ ] All Bootstrap `data-bs-*` components tested and functional — **Iron Law 3**

### HTML Quality
- [ ] Valid HTML (W3C Markup Validator — zero errors)
- [ ] Semantic structure: `<header>`, `<main>`, `<footer>`, `<nav>`, `<article>`
- [ ] All images have meaningful `alt` text
- [ ] Skip navigation link present and functional
- [ ] `<html lang="en">` set

### CSS Quality
- [ ] Valid CSS (W3C CSS Validator — zero errors)
- [ ] All selectors scoped to container class — no global leaks
- [ ] No Bootstrap global overrides without container scope
- [ ] Custom classes use project prefix — no collision with Bootstrap names
- [ ] No `!important` except scoped + commented Bootstrap overrides
- [ ] `prefers-reduced-motion` handled for all animations

### Bootstrap Design System
- [ ] Bootstrap grid intact — no custom CSS breaks column behavior
- [ ] All interactive Bootstrap components functional: navbar, collapse, carousel, offcanvas, tab
- [ ] `--bs-*` variable overrides correctly scoped
- [ ] Z-index stack correct — no custom overlays conflicting with Bootstrap layers
- [ ] Bootstrap ARIA attributes not manually overridden

### Accessibility
- [ ] Passes axe DevTools or Wave (zero critical violations)
- [ ] Keyboard navigation: Tab reaches all interactive elements
- [ ] All form fields have associated labels
- [ ] Contrast ratio ≥ 4.5:1 verified

### Performance
- [ ] All images below the fold have `loading="lazy"`
- [ ] All images have explicit `width` + `height` (prevents layout shift / CLS)
- [ ] Bootstrap CSS + JS loaded from CDN (cached across sites)
- [ ] No render-blocking resources in `<head>` beyond Bootstrap CSS
- [ ] No unused `@keyframes` or dead CSS rules

### Browser Compatibility
- [ ] Chrome, Firefox, Safari, Edge — latest 2 versions
- [ ] iOS Safari 15+, Android Chrome

---

## 16. Communication Protocol

| User trigger | AI action |
|---|---|
| Sends screenshot | Acknowledge receipt, do nothing |
| Sends code | Acknowledge receipt, do nothing |
| *"analyze"* / *"проведи анализ"* | Phase 1 — System Analysis report |
| *"how would you refactor"* | Phase 2 — Plan only, no code |
| *"what can be CSS"* / *"убери js"* | Phase 4 — CSS-only replacement map |
| *"UI/UX"* | Phase 5 audit |
| *"mobile"* / *"адаптация"* | Phase 6 analysis |
| *"a11y"* / *"доступность"* | Phase 7 audit |
| *"docs"* / *"комментарии"* | Phase 9 review |
| *"conflicts"* / *"конфликты"* | Phase 10 audit |
| **"делай"** / **"do it"** | Phase 11 — produce full static HTML file |
| *"Production"* | Phase 12 — full checklist against output |

---

*Guide version: 1.0 No-JS Base*
*Derived from: Refactoring Level+ Base v1.0*
*Stack: Bootstrap 5 CSS + Bootstrap 5 JS CDN | No custom JS | No build tools*
*Language: English (all code and comments)*
