# Refactoring Level+ No-JS — Pro
## AI-Assisted Code Quality Guide — Static HTML + CSS Edition (Pro)

> **Purpose**: A structured workflow for refactoring static projects with full
> Containerization v4 CSS architecture — product catalogs, landing pages,
> presentation pages — where content is fixed and no runtime data changes are needed.
>
> **Core rule**: Bootstrap JS CDN is always connected and must never be broken.
> Custom `<script>` blocks are forbidden. Everything Bootstrap can do natively —
> Bootstrap does. You never write JS for it.

> **Version**: 2.0 No-JS Pro — derived from Refactoring Level+ Pro v2.0

---

## Table of Contents

1. [Core Philosophy](#1-core-philosophy)
2. [Iron Laws](#2-iron-laws)
3. [Conflict Resolution Priority — The Hierarchy](#3-conflict-resolution-priority--the-hierarchy)
4. [Phase 0 — Input & Context Collection](#4-phase-0--input--context-collection)
5. [Phase 1 — System Analysis](#5-phase-1--system-analysis)
6. [Phase 2 — Pre-Refactor Planning](#6-phase-2--pre-refactor-planning)
7. [Phase 3 — Technology Stack](#7-phase-3--technology-stack)
8. [Phase 4 — Containerization Architecture (CSS-only)](#8-phase-4--containerization-architecture-css-only)
9. [Phase 5 — CSS-Only Interaction Patterns](#9-phase-5--css-only-interaction-patterns)
10. [Phase 6 — UI/UX Standards Audit](#10-phase-6--uiux-standards-audit)
11. [Phase 7 — Mobile & Responsive Adaptation](#11-phase-7--mobile--responsive-adaptation)
12. [Phase 8 — Accessibility (a11y)](#12-phase-8--accessibility-a11y)
13. [Phase 9 — W3C Standards Compliance](#13-phase-9--w3c-standards-compliance)
14. [Phase 10 — Documentation & Comments](#14-phase-10--documentation--comments)
15. [Phase 11 — Bootstrap Conflict Detection](#15-phase-11--bootstrap-conflict-detection)
16. [Phase 12 — Execution ("делай" / "do it")](#16-phase-12--execution-делай--do-it)
17. [Phase 13 — Enterprise Production Checklist](#17-phase-13--enterprise-production-checklist)
18. [Communication Protocol](#18-communication-protocol)

---

## 1. Core Philosophy

```
READ → ANALYZE → CLASSIFY → PLAN → CONFIRM → EXECUTE
```

- Never refactor blindly. Always understand *why* before *how*.
- **Bootstrap does its job. You don't rewrite what Bootstrap already solves.**
- Static by default. Custom JS only when HTML + CSS + Bootstrap genuinely cannot do it.
- Containerization is the shape of every component — all rules operate inside that shape.
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
║  dropdown, offcanvas, carousel, modal, tab, alert) work      ║
║  through data-bs-* attributes.                               ║
║  Do not touch, wrap, override, or replicate their JS logic.  ║
║  If a Bootstrap component stops working — that is a bug.     ║
╠══════════════════════════════════════════════════════════════╣
║  IRON LAW 2 — NO CUSTOM SCRIPT BLOCKS                       ║
║                                                              ║
║  No <script> tag with custom logic.                          ║
║  No inline JS (onclick="", onload="", href="javascript:").   ║
║  No .js files.                                               ║
║  If a feature requires custom JS — it does not belong        ║
║  in a No-JS project. Redesign with CSS/HTML or escalate      ║
║  to the Pro guide with JS enabled.                           ║
╠══════════════════════════════════════════════════════════════╣
║  IRON LAW 3 — BOOTSTRAP HANDLES BOOTSTRAP                   ║
║                                                              ║
║  Never replace a working Bootstrap component with            ║
║  a custom CSS-only hack if Bootstrap already solves it.      ║
║  data-bs-toggle, data-bs-target, data-bs-dismiss — these     ║
║  are the correct tools. Use them as-is.                      ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 3. Conflict Resolution Priority — The Hierarchy

When two rules conflict, the **higher rank always wins**. No exceptions.

```
┌─────────────────────────────────────────────────────────────┐
│  RANK 0 — CONTAINERIZATION                                  │
│  Defines the shape of every component. Inviolable.          │
│  → Widget = self-contained container, scoped CSS            │
│  → No JS containers in No-JS projects                       │
├─────────────────────────────────────────────────────────────┤
│  RANK 1 — IRON LAWS (Bootstrap JS integrity)                │
│  Bootstrap JS CDN always present. Never broken.             │
│  No custom <script>. Bootstrap handles Bootstrap.           │
├─────────────────────────────────────────────────────────────┤
│  RANK 2 — CODE CLEANLINESS                                  │
│  Structure, isolation, readability, naming conventions.     │
│  Applies everywhere unless it conflicts with RANK 3.        │
├─────────────────────────────────────────────────────────────┤
│  RANK 3 — PERFORMANCE                                       │
│  GPU-composited animations, lazy images, no CLS.            │
│  Final audit — does not reshape architecture.               │
└─────────────────────────────────────────────────────────────┘
```

> **Note on Security rank:** Since there is no custom JS, the XSS / injection
> security surface does not exist in this project. Security concerns reduce to
> HTML structure hygiene (no inline styles, valid nesting) and external link safety
> (`rel="noopener noreferrer"`).

### Applying the hierarchy in practice

**Scenario A — Custom class conflicts with Bootstrap `.card`:**
> RANK 0 wins → scope all custom selectors to container class.
> `.cat-container .card { ... }` not `.card { ... }`.

**Scenario B — "Clever" CSS hack vs. Bootstrap component:**
> RANK 1 wins → if Bootstrap already solves it with `data-bs-*`, use Bootstrap.
> Never replace a working Bootstrap accordion with a CSS `:checked` trick.

**Scenario C — Visual effect requires `display: none` on Bootstrap component:**
> RANK 1 wins → never hide Bootstrap components with CSS alone.
> Control them through their own `data-bs-*` API.

---

## 4. Phase 0 — Input & Context Collection

### What the user does:
- Shares **screenshots** of the running page
- Shares **source code** (paste, upload, or link)

### What the AI does:
1. Acknowledge receipt — confirm what was received
2. **Do nothing else** — no suggestions, no refactoring, no opinions
3. Wait for explicit instruction to proceed

> **Rule:** Until the user writes **"делай"** / **"do it"** — AI only collects and reads.

---

## 5. Phase 1 — System Analysis

*Triggered by: "analyze" / "проведи анализ"*

### 1.1 Code Analysis

| Dimension | What to look for |
|---|---|
| **Custom JS presence** | Any `<script>`, inline handlers, `.js` files — flag every instance |
| **Bootstrap JS integrity** | CDN present? `data-bs-*` components functional? |
| **Unnecessary JS** | Features done in JS that CSS or Bootstrap already solves |
| **Containerization** | Are components self-contained? CSS scoped? No global leaks? |
| **CSS quality** | Global leaks, missing scoping, Bootstrap selector conflicts |
| **HTML semantics** | Semantic tags, ARIA, heading hierarchy |
| **Performance** | Render-blocking resources, large images without lazy, CLS risk |
| **Accessibility** | Missing alt, contrast, keyboard navigation |

### 1.2 Screenshot Analysis

- Map every UI element — static content or interactive?
- For every interactive element: Bootstrap declarative or CSS handles it?
- Classify components: pure static / CSS-interactive / Bootstrap-interactive
- Note layout issues, broken responsiveness, a11y failures

### 1.3 Analysis Output Format

```
## System Analysis Report

### What the project does
[1-3 sentences]

### Tech stack detected
[Technologies + versions]

### Custom JS inventory
| File / Block | What it does | Replacement | Priority |
|---|---|---|---|
| main.js: scroll handler | Adds .sticky class | CSS position:sticky | Must remove |
| inline onclick | Opens accordion | Bootstrap collapse | Must remove |

### Component classification
| Component | Type | Handled by |
|---|---|---|
| Hero banner | Static | HTML + CSS |
| Mobile nav | BS-interactive | data-bs-toggle="collapse" |
| FAQ section | CSS-interactive | <details>/<summary> |
| Image slider | BS-interactive | data-bs-ride="carousel" |
| Filter sidebar | BS-interactive | data-bs-toggle="offcanvas" |

### Bootstrap JS status
[CDN present? Any broken data-bs-* components?]

### Critical issues (must fix)
[Numbered list]

### Code quality issues (should fix)
[Numbered list]

### What works well (keep it)
[Numbered list]
```

---

## 6. Phase 2 — Pre-Refactor Planning

*Triggered by: "how would you refactor" — output plan only, no code*

The AI must produce:

1. **Project purpose** — what does this page display?
2. **JS elimination map** — each custom JS piece → CSS/Bootstrap replacement
3. **Container map** — one container per component, with prefix and scope
4. **Bootstrap components map** — which Bootstrap components activate where
5. **CSS-only patterns** — where pure CSS handles interaction
6. **Change list** — what gets removed, replaced, restructured
7. **Risk** — what Bootstrap behavior could break during CSS cleanup

### Output Format

```
## Refactoring Plan

### Project purpose
[...]

### JS elimination map
| Current JS | Replacement | Action |
|---|---|---|
| Sticky nav handler | CSS position:sticky | Delete JS block |
| Custom tab logic | Bootstrap nav-tabs | data-bs-toggle="tab" |
| Accordion JS | <details>/<summary> | Delete JS block |
| Carousel init | Bootstrap carousel | data-bs-ride="carousel" |

### Container map
| Component | Container class | CSS prefix | Bootstrap used? |
|---|---|---|---|
| Product catalog | .cat-container | cat- | Grid only |
| Site header | .site-header | hdr- | Navbar collapse |
| Filter panel | inside .cat-container | cat- | Offcanvas |
| FAQ | .faq-container | faq- | No (details/summary) |

### CSS-only patterns
| Feature | Technique |
|---|---|
| Card hover lift | :hover + transform + transition |
| FAQ | <details> + <summary> |
| Filter toggle | :checked + ~ sibling selector |
| Fade-in grid | @keyframes + animation-delay |

### Risk areas
[Components that could accidentally break during CSS refactor]
```

---

## 7. Phase 3 — Technology Stack

### Stack: Bootstrap 5 CSS + Bootstrap 5 JS CDN. No custom JS.

```html
<!-- Bootstrap 5 CSS — always first stylesheet -->
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      integrity="sha384-QWTKZyjpPbgXjNCM/X1EBk0VCnEYIKJ2NLfCBfVEBSH7SkSBCYHPSFGJ7pHB3Kn"
      crossorigin="anonymous">

<!-- Custom scoped styles — after Bootstrap CSS, never before -->
<style>
  /* Containerization v4 CSS — scoped, prefixed, no global leaks */
</style>

<!-- Bootstrap 5 JS Bundle — always last, before </body> -->
<!-- IRON LAW 1: Required. Never remove. Never move to <head>. -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmFLpQiHPEELnAXEWTdLB4k1S3p"
        crossorigin="anonymous"></script>

<!-- NO custom <script> block. Iron Law 2. -->
```

### Why Bootstrap JS CDN is always included

Bootstrap's interactive components (`navbar`, `collapse`, `carousel`, `tooltip`,
`offcanvas`, `tab`, `dropdown`, `modal`, `alert dismiss`) require Bootstrap's own JS.
Removing the CDN tag silently breaks every one of them with no console error.
Even on a "purely static" page, Bootstrap JS must be present to keep the design system intact.

---

## 8. Phase 4 — Containerization Architecture (CSS-only)

**This phase defines the shape of every component. Runs before any code is written.**

In the No-JS edition, Containerization applies to **CSS and HTML only**.
There are no JS Controllers, no `data-ref`, no `data-action`, no event listeners.
The container is a CSS scope boundary — nothing more.

### 4.1 Container Rules

```html
<!-- Semantic tag, class only — no id on root -->
<section class="cat-container" aria-label="Product catalog">

  <!-- Bootstrap grid works freely inside the container -->
  <div class="row g-4">
    <div class="col-6 col-md-4 col-lg-3">
      <article class="cat-card">
        ...
      </article><!-- /cat-card -->
    </div>
  </div>

  <!-- Bootstrap offcanvas — inside container, before closing tag -->
  <!-- Keeps token inheritance, satisfies scoping rule -->
  <div class="offcanvas offcanvas-start cat-offcanvas"
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
      <!-- static filter content -->
    </div>
  </div>

</section><!-- /cat-container -->
```

### 4.2 CSS Scoping Rule (RANK 0 — inviolable)

Every custom selector starts with the container class. No exceptions.

```css
/* ✅ CORRECT — scoped, cannot leak into other components */
.cat-container .cat-card { ... }
.cat-container .cat-card:hover { ... }
.cat-container .btn { ... }           /* safe Bootstrap override, scoped */
.cat-container .offcanvas { ... }     /* Bootstrap component override, scoped */

/* ❌ WRONG — global leak, violates RANK 0 */
.cat-card { ... }
.btn { background: red; }
```

### 4.3 CSS Token Scope

Tokens declared on the container — child elements inherit automatically.
Bootstrap's own tokens (`--bs-*`) can be safely overridden here without global side effects.

```css
.cat-container {
  /* ============================================================
     TOKENS — declared here, inherited by all children
     ============================================================ */

  /* Brand */
  --cat-color-primary:   #2d6a4f;
  --cat-color-secondary: #52b788;

  /* Card */
  --cat-card-radius:     0.75rem;
  --cat-card-shadow:     0 2px 12px rgba(0, 0, 0, 0.08);
  --cat-card-shadow-hover: 0 8px 24px rgba(0, 0, 0, 0.14);

  /* Layout */
  --cat-gap:             1.5rem;
  --cat-img-ratio:       4 / 3;

  /* Bootstrap token overrides — scoped to this container only */
  --bs-primary:          var(--cat-color-primary);
  --bs-border-radius:    var(--cat-card-radius);
}
```

### 4.4 Naming Conventions

| What | Convention | Example |
|---|---|---|
| CSS container | kebab + `-container` | `.cat-container` |
| CSS child prefix | short kebab (2-4 chars) | `cat-` |
| BEM element | `[prefix]-[block]__[element]` | `.cat-card__name` |
| BEM modifier | `[prefix]-[block]--[modifier]` | `.cat-card--featured` |
| CSS token | `--[prefix]-[name]` | `--cat-card-radius` |
| Bootstrap override (scoped) | `.container-class .bs-component { }` | `.cat-container .btn { }` |

### 4.5 No data-ref / data-action in No-JS Projects

```html
<!-- ✅ CORRECT for No-JS — Bootstrap declarative attributes only -->
<button class="btn btn-outline-secondary"
        data-bs-toggle="offcanvas"
        data-bs-target="#filterPanel">
  Filters
</button>

<!-- ❌ NOT NEEDED — data-ref and data-action are JS hooks, have no purpose here -->
<button class="btn btn-outline-secondary"
        data-action="open-filter"
        data-ref="filter-btn">
  Filters
</button>
```

---

## 9. Phase 5 — CSS-Only Interaction Patterns

**The complete interaction toolkit for No-JS static pages.**

### 5.1 Hover & Focus States

```css
/* ============================================================
   CARD: Hover interactions — CSS only
   ============================================================ */

/* Lift on hover — no JS */
.cat-container .cat-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.cat-container .cat-card:hover,
.cat-container .cat-card:focus-within {
  transform: translateY(-4px);
  box-shadow: var(--cat-card-shadow-hover);
}

/* Reveal action layer on hover — no JS */
.cat-container .cat-card__actions {
  opacity: 0;
  transition: opacity 0.2s ease;
}
.cat-container .cat-card:hover .cat-card__actions,
.cat-container .cat-card:focus-within .cat-card__actions {
  opacity: 1;
}

/* Button press feedback */
.cat-container .btn:active {
  transform: scale(0.97);
}
```

### 5.2 Native HTML: `<details>` / `<summary>`

Use when Bootstrap accordion is unavailable or overkill (e.g., FAQ outside catalog context).

```html
<!-- ✅ Accessible, keyboard-friendly, zero JS -->
<details class="faq-container__item">
  <summary class="faq-container__question">
    What is the return policy?
  </summary>
  <div class="faq-container__answer">
    <p>You may return any item within 30 days of purchase.</p>
  </div>
</details><!-- /faq-container__item -->
```

```css
/* Style <details> to match design — preserve native functionality */
.faq-container .faq-container__item {
  border-bottom: 1px solid var(--bs-border-color);
}
.faq-container .faq-container__question {
  padding: 1rem 0;
  cursor: pointer;
  list-style: none;           /* remove default marker */
  font-weight: 600;
}
/* Custom marker via pseudo-element */
.faq-container .faq-container__question::after {
  content: '+';
  float: right;
  transition: transform 0.2s ease;
}
.faq-container .faq-container__item[open] .faq-container__question::after {
  transform: rotate(45deg);
}
```

### 5.3 CSS :target for Panels

```css
.cat-container .cat-panel {
  display: none;
}
.cat-container .cat-panel:target {
  display: block;
}
```

```html
<a href="#size-guide" class="btn btn-link cat-card__guide-link">Size guide</a>

<div id="size-guide" class="cat-panel cat-container__size-guide">
  <div class="card card-body">
    <h3>Size Guide</h3>
    <!-- static table -->
    <a href="#" class="btn btn-sm btn-secondary mt-2">Close</a>
  </div>
</div>
```

### 5.4 CSS :checked for Toggles

```css
/* Visually hidden but keyboard-accessible checkbox */
.cat-container .cat-filter__toggle {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

/* Collapsed state */
.cat-container .cat-filter__panel {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.35s ease;
}

/* Expanded state — triggered by :checked */
.cat-container .cat-filter__toggle:checked ~ .cat-filter__panel {
  max-height: 800px;
}

/* Label styling reflects state */
.cat-container .cat-filter__label::after {
  content: ' ▼';
  font-size: 0.75em;
  transition: transform 0.2s ease;
  display: inline-block;
}
.cat-container .cat-filter__toggle:checked ~ .cat-filter__label::after {
  transform: rotate(180deg);
}
```

### 5.5 Bootstrap Components — Declarative Usage (No Custom JS)

```html
<!-- ============================================================
     PATTERN: Bootstrap components via data-bs-* only
     Iron Law 3: Bootstrap handles Bootstrap. No custom JS.
     ============================================================ -->

<!-- Navbar with mobile collapse -->
<nav class="navbar navbar-expand-lg hdr-navbar" aria-label="Main navigation">
  <div class="container-xl">
    <a class="navbar-brand hdr-navbar__brand" href="/">Brand</a>
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
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link" href="/catalog">Catalog</a>
        </li>
      </ul>
    </div>
  </div>
</nav>

<!-- Product carousel -->
<div id="heroCarousel"
     class="carousel slide cat-hero__carousel"
     data-bs-ride="carousel"
     data-bs-interval="6000">
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="0"
            class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="1"
            aria-label="Slide 2"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="hero-1.jpg" class="d-block w-100 img-fluid cat-hero__img"
           alt="Summer collection — bright floral patterns"
           loading="eager" width="1200" height="500">
    </div>
    <div class="carousel-item">
      <img src="hero-2.jpg" class="d-block w-100 img-fluid cat-hero__img"
           alt="Autumn collection — earth tones and layers"
           loading="lazy" width="1200" height="500">
    </div>
  </div>
  <button class="carousel-control-prev" type="button"
          data-bs-target="#heroCarousel" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous slide</span>
  </button>
  <button class="carousel-control-next" type="button"
          data-bs-target="#heroCarousel" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next slide</span>
  </button>
</div>

<!-- Offcanvas filter panel — opened by trigger outside the container -->
<button class="btn btn-outline-secondary cat-toolbar__filter-btn"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#filterPanel"
        aria-controls="filterPanel">
  <span aria-hidden="true">⚙</span> Filters
</button>

<!-- Offcanvas panel — place inside the container for token inheritance -->
<div class="offcanvas offcanvas-start cat-offcanvas"
     id="filterPanel"
     tabindex="-1"
     aria-labelledby="filterPanelLabel">
  <div class="offcanvas-header">
    <h2 class="offcanvas-title cat-offcanvas__title" id="filterPanelLabel">
      Filter Products
    </h2>
    <button type="button"
            class="btn-close"
            data-bs-dismiss="offcanvas"
            aria-label="Close filter panel"></button>
  </div>
  <div class="offcanvas-body cat-offcanvas__body">
    <!-- static checkboxes — form submits to server, no JS filter needed -->
    <form method="get" action="/catalog">
      <fieldset>
        <legend class="cat-offcanvas__legend">Category</legend>
        <div class="form-check">
          <input class="form-check-input" type="checkbox"
                 id="cat-shoes" name="category" value="shoes">
          <label class="form-check-label" for="cat-shoes">Shoes</label>
        </div>
      </fieldset>
      <button type="submit" class="btn btn-primary w-100 mt-3">Apply filters</button>
    </form>
  </div>
</div>
```

### 5.6 CSS Animations

```css
/* ============================================================
   ANIMATIONS — transform + opacity only (GPU composited)
   PERFORMANCE: No layout/paint properties (width, height, top, left)
   ============================================================ */

@keyframes cat-fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Grid item entry animation */
.cat-container .cat-card-wrapper {
  animation: cat-fade-in 0.35s ease both;
}

/* Stagger — CSS only, 4 columns × 3 rows covered */
.cat-container .cat-card-wrapper:nth-child(1)  { animation-delay: 0.04s; }
.cat-container .cat-card-wrapper:nth-child(2)  { animation-delay: 0.08s; }
.cat-container .cat-card-wrapper:nth-child(3)  { animation-delay: 0.12s; }
.cat-container .cat-card-wrapper:nth-child(4)  { animation-delay: 0.16s; }
.cat-container .cat-card-wrapper:nth-child(n+5) { animation-delay: 0.20s; }

/* Respect user system preference — always */
@media (prefers-reduced-motion: reduce) {
  .cat-container .cat-card-wrapper {
    animation: none;
  }
}
```

---

## 10. Phase 6 — UI/UX Standards Audit

### Visual Consistency

- [ ] Single color palette — container tokens (`--cat-*`) + Bootstrap `--bs-*` overrides
- [ ] Consistent spacing — Bootstrap `m-*`, `p-*` or custom `rem` scale via tokens
- [ ] Typography hierarchy — `h1`–`h6` meaningful, not decorative
- [ ] One icon library only
- [ ] Hover/focus states defined for all interactive elements
- [ ] No mixed visual language — Bootstrap native or fully custom, not half-half

### UX Flow

- [ ] Key information visible without scrolling on desktop (above the fold)
- [ ] Product cards show: image, name, price, primary CTA
- [ ] Empty states have messaging — no blank sections
- [ ] No dead `href="#"` links in production
- [ ] Filter form submits to server — static page has no client-side filtering

### Forms (if present)

- [ ] Labels always present — never placeholder as label
- [ ] `required` fields marked with attribute and visual indicator
- [ ] `autocomplete` attributes set
- [ ] HTML5 validation: `type`, `pattern`, `minlength`, `maxlength`

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
2. **No fixed pixel widths** — `%`, `vw`, Bootstrap columns, `min()`, `clamp()`
3. **Touch targets** — minimum `44×44px` (WCAG 2.5.5)
4. **Font sizes** — minimum `16px` body, never below `12px`
5. **Viewport meta** — always:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1">
   ```
6. **Images** — `img-fluid` + `loading="lazy"` + explicit `width`/`height` + meaningful `alt`
7. **Tables** — wrap in `<div class="table-responsive">`
8. **Navigation** — Bootstrap `navbar-toggler` + `navbar-expand-lg`
9. **Product grid** — `col-6 col-md-4 col-lg-3` standard catalog pattern
10. **Bootstrap offcanvas for filters** — solves mobile filter panel without custom JS
11. **Test on real devices** — not only DevTools

---

## 12. Phase 8 — Accessibility (a11y)

### WCAG 2.1 AA — Required

**Perceivable:**
- [ ] All images have `alt` text (`alt=""` for decorative)
- [ ] Color not the sole conveyor of information
- [ ] Contrast ratio ≥ 4.5:1 (normal), ≥ 3:1 (large text / UI)
- [ ] No content relying on sensory characteristics alone

**Operable:**
- [ ] All interactive elements keyboard-reachable (`Tab`, `Enter`, `Space`)
- [ ] No keyboard traps
- [ ] Skip navigation: `<a class="visually-hidden-focusable" href="#main-content">Skip to main</a>`
- [ ] Focus always visible — never `outline: none` without visible replacement
- [ ] Touch targets ≥ 44×44px

**Understandable:**
- [ ] `<html lang="en">` (or correct locale)
- [ ] Form labels associated: `for` + `id`, or `aria-label`
- [ ] Link text descriptive — not "click here" or "read more" without context

**Robust:**
- [ ] Valid HTML (W3C validator — zero errors)
- [ ] Bootstrap ARIA managed by Bootstrap — never manually override `aria-expanded`,
      `aria-controls`, `aria-hidden` on Bootstrap components
- [ ] `<details>`/`<summary>` correct for custom accordions

### Product Card Pattern

```html
<article class="col-6 col-md-4 col-lg-3 cat-card-wrapper"
         aria-label="Blue Running Shoes">
  <div class="cat-card">

    <!-- Image link is decorative duplicate of text link below — hide from AT -->
    <a href="/product/blue-shoes"
       class="cat-card__img-link"
       tabindex="-1"
       aria-hidden="true">
      <img src="shoes.jpg"
           alt=""
           class="cat-card__img img-fluid"
           loading="lazy"
           width="400" height="300">
    </a>

    <div class="cat-card__body">
      <h3 class="cat-card__name">
        <!-- Main link — this is what keyboard and AT users interact with -->
        <a href="/product/blue-shoes" class="cat-card__link stretched-link">
          Blue Running Shoes
        </a>
      </h3>
      <p class="cat-card__price">
        <span class="visually-hidden">Price:</span>
        <span aria-hidden="true">$</span>89.99
      </p>
      <p class="cat-card__category">
        <span class="visually-hidden">Category:</span>Running
      </p>
    </div>

  </div>
</article><!-- /cat-card-wrapper -->
```

---

## 13. Phase 9 — W3C Standards Compliance

### HTML5

- [ ] `<!DOCTYPE html>` present
- [ ] `<html lang="en">` correct locale
- [ ] `<meta charset="UTF-8">`
- [ ] `<title>` meaningful and unique
- [ ] Semantic tags: `<header>`, `<main>`, `<nav>`, `<article>`, `<section>`, `<footer>`
- [ ] Product items use `<article>` (standalone meaningful unit)
- [ ] No deprecated tags: `<center>`, `<font>`, `<b>` for styling
- [ ] No inline styles (except CSS custom property overrides)
- [ ] Valid nesting

### CSS3

- [ ] CSS variables for all tokens (`--prefix-name`) declared on container
- [ ] No `!important` except scoped Bootstrap overrides (commented + justified)
- [ ] All custom selectors start with container class — no global leaks
- [ ] Media queries mobile-first (`min-width`)
- [ ] Animations use `transform` + `opacity` only (GPU composited, no layout reflow)
- [ ] `prefers-reduced-motion` respected for every animation

### No Custom JS = No JS Compliance Issues

Since there is no custom JS, the following are automatically satisfied:
- No XSS via `innerHTML`
- No prototype pollution
- No event listener memory leaks
- No layout thrashing
- No unhandled promise rejections
- No `console.log` in production

---

## 14. Phase 10 — Documentation & Comments

*Based on Compact Comments Guide — HTML/CSS only edition.*

### HTML Comments — 3 Levels

```html
<!-- ============================================================ CATALOG START -->
<section class="cat-container" aria-label="Product catalog">

  <!-- Toolbar: filter trigger + sort controls -->
  <div class="cat-toolbar">
    ...
  </div><!-- /cat-toolbar -->

  <!-- Grid: lg=4col / md=3col / sm=2col / xs=1col -->
  <div class="row g-4" role="list" aria-label="Product list">

    <!-- Product card — repeat for each item -->
    <article class="col-6 col-md-4 col-lg-3 cat-card-wrapper" role="listitem">
      ...
    </article><!-- /cat-card-wrapper -->

  </div>

  <!-- NOTE: Offcanvas filter inside container — required for token inheritance -->
  <div class="offcanvas offcanvas-start cat-offcanvas" id="filterPanel" ...>
    ...
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
   2. Toolbar
   3. Product Card
   4. Offcanvas Filter
   5. Pagination
   6. Animations (@keyframes)
   7. Responsive (@media)
   ============================================================ */

/* ============================================================
   0. TOKENS & RESET
   ============================================================ */

.cat-container {
  --cat-card-radius:  0.75rem;          /* card rounding — matches design spec */
  --cat-card-shadow:  0 2px 8px rgba(0, 0, 0, 0.08);
  --cat-card-shadow-hover: 0 8px 24px rgba(0, 0, 0, 0.14);
  --cat-gap:          1.5rem;           /* grid spacing */
  --cat-img-ratio:    4 / 3;            /* product image aspect ratio */

  /* Bootstrap token overrides — scoped to this container only */
  --bs-primary:        #2d6a4f;
  --bs-border-radius:  var(--cat-card-radius);
}

/* --- Product Card --- */

/* 4px lift + shadow increase — design spec: card hover interaction */
.cat-container .cat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--cat-card-shadow-hover);
}

/* HACK: Safari — aspect-ratio on img requires explicit height reset */
.cat-container .cat-card__img {
  height: auto;
}

/* ============================================================
   6. ANIMATIONS
   ============================================================ */

/* PERFORMANCE: transform + opacity only — GPU layer, zero layout reflow */
@keyframes cat-fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### No Custom JS = No JSDoc

There are no functions, classes, or modules to document.
HTML and CSS comments are the only documentation layer.
Flag lines: `TODO`, `FIXME`, `HACK`, `NOTE`, `WARNING` — same conventions as JS guides,
applied in HTML and CSS comments only.

---

## 15. Phase 11 — Bootstrap Conflict Detection

### Conflict Resolution Rules (by Hierarchy)

**RANK 0 — Container scoping (inviolable)**
```css
/* ❌ FORBIDDEN — global Bootstrap override */
.btn { background: red; }
.card { border-radius: 0; }
.offcanvas { width: 400px; }

/* ✅ CORRECT — scoped to container */
.cat-container .btn { background: var(--cat-btn-bg); }
.cat-container .card { border-radius: var(--cat-card-radius); }
.cat-container .cat-offcanvas { width: 360px; }
```

**RANK 1 — Never break Bootstrap JS (Iron Law 1)**
```html
<!-- ❌ FORBIDDEN — removes attributes Bootstrap JS reads -->
<button data-bs-toggle="collapse">  <!-- missing data-bs-target -->

<!-- ❌ FORBIDDEN — manually setting Bootstrap-managed ARIA -->
<button data-bs-toggle="collapse" aria-expanded="true">
<!-- Bootstrap sets aria-expanded itself. Initial value must be "false" for collapsed. -->

<!-- ✅ CORRECT -->
<button data-bs-toggle="collapse"
        data-bs-target="#target"
        aria-controls="target"
        aria-expanded="false">
```

```css
/* ❌ FORBIDDEN — hides Bootstrap component with CSS, breaks JS state */
#filterPanel { display: none !important; }

/* ✅ CORRECT — Bootstrap manages its own visibility via the hidden attribute
   and aria-hidden. Never override with CSS. */
```

**Prefix safety**
```css
/* Never use Bootstrap class names as your component names */
/* ❌ Collides: .card, .badge, .carousel, .offcanvas, .collapse, .modal */
/* ✅ Safe:     .cat-card, .cat-badge, .cat-carousel-wrapper */
```

**Z-index reference**
```css
/* Bootstrap z-index stack — never conflict unintentionally:
   Dropdown:  1000  |  Sticky: 1020  |  Fixed:   1030
   Backdrop:  1040  |  Modal:  1055  |  Popover: 1070  |  Tooltip: 1080
*/
.cat-container .cat-overlay { z-index: 900; } /* below all Bootstrap layers */
```

### Pre-Ship Bootstrap Verification

- [ ] All `data-bs-*` components functional: navbar, collapse, carousel, offcanvas, tab, tooltip
- [ ] `--bs-*` variable overrides scoped — not cascading into unrelated sections
- [ ] No custom CSS targets Bootstrap's internal classes without container scope
- [ ] Bootstrap JS bundle `<script>` tag present before `</body>`
- [ ] No `!important` overriding Bootstrap component visibility or display
- [ ] No custom CSS changes Bootstrap component dimensions in ways that break layout

---

## 16. Phase 12 — Execution ("делай" / "do it")

**This phase begins ONLY when the user writes the explicit trigger.**

### What the AI produces

A self-contained Bootstrap 5 static HTML file:

- **Single `.html` file** — HTML + `<style>` only
- **Bootstrap 5 CSS CDN** — first stylesheet, always
- **Bootstrap 5 JS Bundle CDN** — last tag before `</body>` *(Iron Law 1)*
- **No custom `<script>` block** *(Iron Law 2)*
- **Containerization v4 CSS** — every component scoped, prefixed, no global leaks
- **All comments in English** — Compact Comments Guide format, HTML+CSS only
- **Production-ready** — not a prototype

### Output File Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- ============================================================ META START -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="[SEO description]">
  <title>[Meaningful page title]</title>
  <!-- Open Graph tags for social sharing -->
  <meta property="og:title" content="[Title]">
  <meta property="og:description" content="[Description]">
  <meta property="og:type" content="website">
  <!-- ============================================================== META END -->

  <!-- Bootstrap 5 CSS — design system foundation, always first -->
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        integrity="sha384-QWTKZyjpPbgXjNCM/X1EBk0VCnEYIKJ2NLfCBfVEBSH7SkSBCYHPSFGJ7pHB3Kn"
        crossorigin="anonymous">

  <style>
    /* ============================================================
       TABLE OF CONTENTS
       0. Global Tokens & Reset
       1. Site Header
       2. [Component A] Container
       3. [Component B] Container
       4. Site Footer
       5. Utilities
       6. Responsive (@media)
       ============================================================ */

    /* Each component section follows Containerization v4 structure:
       0. Tokens (--prefix-*)
       1. Container layout
       2. Child elements
       3. States (:hover, :focus, :checked, :target, [open])
       4. Animations (@keyframes) with prefix
       5. Responsive for this component
    */
  </style>
</head>
<body>

  <!-- Skip navigation — always first element in <body> -->
  <a class="visually-hidden-focusable" href="#main-content">Skip to main content</a>

  <!-- ============================================================ HEADER START -->
  <header class="site-header" role="banner">
    <!-- Bootstrap navbar — Iron Law 3: Bootstrap handles collapse logic -->
    <nav class="navbar navbar-expand-lg hdr-navbar" aria-label="Main navigation">
      ...
    </nav>
  </header>
  <!-- ============================================================== HEADER END -->

  <!-- ============================================================== MAIN START -->
  <main id="main-content" role="main">

    <!-- [Component A]: Static — HTML + CSS only -->
    <section class="[prefix]-container" aria-label="[Accessible name]">
      <!--
        Bootstrap grid freely used inside.
        All Bootstrap interactive elements via data-bs-* only.
        No custom JS. No inline handlers.
        Offcanvas/modals placed inside container before closing tag.
      -->
    </section><!-- /[prefix]-container -->

    <!-- [Component B]: Bootstrap interactive — data-bs-* only -->
    <section class="[prefix2]-container" aria-label="[Accessible name]">
      ...
    </section><!-- /[prefix2]-container -->

  </main>
  <!-- ================================================================ MAIN END -->

  <!-- ============================================================ FOOTER START -->
  <footer class="site-footer" role="contentinfo">
    ...
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

  <!-- IRON LAW 2 — No custom <script> block. -->

</body>
</html>
```

---

## 17. Phase 13 — Enterprise Production Checklist

### Iron Laws Verification (run first — blocks everything else)
- [ ] Bootstrap JS CDN `<script>` present before `</body>` — **Iron Law 1**
- [ ] Zero custom `<script>` blocks in file — **Iron Law 2**
- [ ] Zero inline JS: no `onclick`, `onload`, `href="javascript:..."` — **Iron Law 2**
- [ ] All Bootstrap `data-bs-*` components tested and functional — **Iron Law 3**
- [ ] Bootstrap-managed ARIA not manually overridden — **Iron Law 3**

### Containerization Compliance (RANK 0)
- [ ] Every component has a scoped container class
- [ ] Every custom CSS selector starts with the container class — zero global leaks
- [ ] CSS tokens (`--prefix-name`) declared on the container element
- [ ] Custom class names use project prefix — no collision with Bootstrap names
- [ ] Offcanvas/modal panels placed inside their parent container
- [ ] `@keyframes` names carry the widget prefix (not generic `fadeIn`)

### HTML Quality
- [ ] Valid HTML (W3C Markup Validator — zero errors)
- [ ] Semantic structure: `<header>`, `<main>`, `<footer>`, `<nav>`, `<article>`
- [ ] All images have meaningful `alt` text
- [ ] Skip navigation link present and functional
- [ ] `<html lang="en">` set
- [ ] No deprecated tags

### CSS Quality
- [ ] Valid CSS (W3C CSS Validator — zero errors)
- [ ] No `!important` except scoped Bootstrap overrides (commented + justified)
- [ ] `prefers-reduced-motion` handled for every animation
- [ ] Media queries mobile-first (`min-width`)
- [ ] Animations use `transform` + `opacity` only

### Bootstrap Design System
- [ ] Bootstrap grid intact — no custom CSS breaks column behavior
- [ ] All interactive Bootstrap components functional
- [ ] `--bs-*` overrides scoped to containers — not cascading globally
- [ ] Z-index stack correct
- [ ] Bootstrap CDN SRI integrity hashes present on both CSS and JS tags

### Accessibility
- [ ] Passes axe DevTools or Wave (zero critical violations)
- [ ] Keyboard navigation: Tab reaches all interactive elements
- [ ] All form fields have associated labels
- [ ] Contrast ratio ≥ 4.5:1 verified
- [ ] `<details>`/`<summary>` patterns keyboard-accessible

### Performance
- [ ] Hero/above-fold images: `loading="eager"` (not lazy)
- [ ] All below-fold images: `loading="lazy"`
- [ ] All images have explicit `width` + `height` (prevents CLS)
- [ ] Bootstrap CSS + JS from CDN with SRI hashes
- [ ] No render-blocking resources in `<head>` beyond Bootstrap CSS
- [ ] No unused `@keyframes` or dead CSS rules

### Browser Compatibility
- [ ] Chrome, Firefox, Safari, Edge — latest 2 versions
- [ ] iOS Safari 15+, Android Chrome

---

## 18. Communication Protocol

| User trigger | AI action |
|---|---|
| Sends screenshot | Acknowledge receipt, do nothing |
| Sends code | Acknowledge receipt, do nothing |
| *"analyze"* / *"проведи анализ"* | Phase 1 — System Analysis report |
| *"how would you refactor"* | Phase 2 — Plan only, no code |
| *"what can be CSS"* / *"убери js"* | Phase 5 — CSS/Bootstrap replacement map |
| *"containerization"* | Phase 4 — container architecture plan |
| *"UI/UX"* | Phase 6 audit |
| *"mobile"* / *"адаптация"* | Phase 7 analysis |
| *"a11y"* / *"доступность"* | Phase 8 audit |
| *"docs"* / *"комментарии"* | Phase 10 review |
| *"conflicts"* / *"конфликты"* | Phase 11 audit |
| **"делай"** / **"do it"** | Phase 12 — produce full static HTML file |
| *"Enterprise Production"* | Phase 13 — full checklist against output |

---

*Guide version: 2.0 No-JS Pro*
*Derived from: Refactoring Level+ Pro v2.0*
*Based on: Containerization v4 · Compact Comments Guide · Clean Code HTML/CSS*
*Stack: Bootstrap 5 CSS + Bootstrap 5 JS CDN | No custom JS | No build tools*
*Language: English (all code and comments)*
