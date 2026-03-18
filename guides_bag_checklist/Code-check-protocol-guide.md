# 🔬 CODE CHECK PROTOCOL GUIDE
### Complete Systematic Protocol for HTML · CSS · JavaScript Code Auditing

> **Purpose:** This guide is a step-by-step protocol for AI assistants. Input — source code (HTML/CSS/JS). Output — a full bug report with concrete fixes for every issue found.

---

## 📋 TABLE OF CONTENTS

1. [Methodology](#1-methodology)
2. [Block A — HTML Structure & Semantics](#2-block-a--html-structure--semantics)
3. [Block B — HTML Attributes & Values](#3-block-b--html-attributes--values)
4. [Block C — HTML Forms](#4-block-c--html-forms)
5. [Block D — Images & Media](#5-block-d--images--media)
6. [Block E — Accessibility (A11y)](#6-block-e--accessibility-a11y)
7. [Block F — HTML Performance & Security](#7-block-f--html-performance--security)
8. [Block G — CSS Architecture & Organization](#8-block-g--css-architecture--organization)
9. [Block H — CSS Selectors & Specificity](#9-block-h--css-selectors--specificity)
10. [Block I — CSS Custom Properties & Design Tokens](#10-block-i--css-custom-properties--design-tokens)
11. [Block J — Units & Values](#11-block-j--units--values)
12. [Block K — Flexbox & Grid](#12-block-k--flexbox--grid)
13. [Block L — Responsive Design](#13-block-l--responsive-design)
14. [Block M — CSS Performance & Animation](#14-block-m--css-performance--animation)
15. [Block N — CSS Anti-patterns](#15-block-n--css-anti-patterns)
16. [Block O — JS Syntax & Modern Standards](#16-block-o--js-syntax--modern-standards)
17. [Block P — Naming Conventions](#17-block-p--naming-conventions)
18. [Block Q — Functions & Design Principles](#18-block-q--functions--design-principles)
19. [Block R — Async Code & Error Handling](#19-block-r--async-code--error-handling)
20. [Block S — DOM & Events](#20-block-s--dom--events)
21. [Block T — JavaScript Security](#21-block-t--javascript-security)
22. [Block U — JS Performance](#22-block-u--js-performance)
23. [Block V — Modularity & Code Organization](#23-block-v--modularity--code-organization)
24. [Block W — Comments & Documentation](#24-block-w--comments--documentation)
25. [Block X — Testability & Code Quality](#25-block-x--testability--code-quality)
26. [Final Report Template](#26-final-report-template)
27. [Quick Scan Checklist](#27-quick-scan-checklist)

---

## 1. METHODOLOGY

### How the AI should work with code

**Step 1 — Initial scan**
Before detailed analysis, get a quick overview:
- Project type (landing / dashboard / form / portfolio / e-commerce / SPA)
- CSS methodology (BEM, Tailwind, CSS Modules, plain CSS, utility-first)
- Frameworks and libraries in use
- Codebase size and complexity

**Step 2 — Block-by-block analysis**
Go through each block (A→X) systematically, logging every issue found.

**Step 3 — Classify every bug**

| Severity | Symbol | Description |
|----------|--------|-------------|
| Critical | 🔴 CRITICAL | Broken functionality, security vulnerability, data loss, XSS/injection |
| High | 🟠 HIGH | Serious behavioral bug, memory leak, significant performance degradation |
| Medium | 🟡 MEDIUM | Standards violation, maintainability issue, unreliable code |
| Low | 🟢 LOW | Style inconsistency, minor deviation, polish and refactor |

**Step 4 — Form concrete fixes**
For every bug — provide a specific code fix, not an abstract suggestion.

**Step 5 — Final report**
Structured output using the template from section 26.

---

## 2. BLOCK A — HTML STRUCTURE & SEMANTICS

### A1. DOCTYPE and Document Base

**What to check:**
```
❌ Missing <!DOCTYPE html> — browser enters Quirks Mode
❌ Legacy DOCTYPE: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
❌ <html> without lang attribute
❌ Missing <meta charset="UTF-8">
❌ charset not the FIRST element in <head>
❌ Missing viewport meta tag
❌ Empty or generic <title>
```

**Fix:**
```html
<!-- ❌ BUG: no DOCTYPE, no lang, no charset -->
<html>
  <head><title>Page</title></head>
</html>

<!-- ✅ CORRECT -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meaningful Page Title — Brand Name</title>
  </head>
  <body>...</body>
</html>
```

---

### A2. Semantic HTML Tags

**What to check:**

| Tag | Correct use | Common mistake |
|-----|-------------|----------------|
| `<header>` | Page or section header | `<div class="header">` |
| `<nav>` | Navigation blocks | `<div class="menu">` |
| `<main>` | Primary unique content | Often missing entirely |
| `<article>` | Self-contained content unit | `<div class="post">` |
| `<section>` | Thematic group with a heading | Used as generic `<div>` |
| `<aside>` | Related side content | Used for layout columns |
| `<footer>` | Page or section footer | `<div class="footer">` |
| `<figure>` | Media with caption | Image in plain `<div>` |
| `<time>` | Dates and times | `<span>` for dates |
| `<address>` | Author contact info | Generic paragraph |
| `<mark>` | Highlighted/relevant text | `<span class="highlight">` |
| `<abbr>` | Abbreviations | Plain text without title |

**Nesting violations — critical errors:**
```html
<!-- ❌ CRITICAL: block element inside inline -->
<span><div>Content</div></span>
<p><ul><li>Item</li></ul></p>        <!-- ul/ol cannot be inside p -->

<!-- ❌ CRITICAL: button inside a or a inside button -->
<a href="/"><button>Go</button></a>

<!-- ❌ HIGH: heading order skipped -->
<h1>Title</h1>
<h3>Subtitle</h3>  <!-- h2 was skipped -->

<!-- ❌ HIGH: multiple <h1> on one page -->
<h1>Main Title</h1>
<h1>Another H1</h1>  <!-- only one h1 per page -->

<!-- ✅ CORRECT -->
<main>
  <article>
    <h1>Page Title</h1>
    <section>
      <h2>Section Heading</h2>
      <h3>Sub-section</h3>
    </section>
  </article>
</main>
```

---

### A3. Duplicate IDs and Div Soup

**What to check:**
```
❌ Same id="" on multiple elements — id must be globally unique
❌ Deeply nested divs with no semantic purpose (div soup)
❌ Empty containers with no content and no functional role
❌ Table used for layout (not for tabular data)
```

**Fix:**
```html
<!-- ❌ BUG: duplicate IDs -->
<div id="card">...</div>
<div id="card">...</div>

<!-- ✅ CORRECT: use class for repeating patterns -->
<div class="card">...</div>
<div class="card">...</div>

<!-- ❌ BUG: div soup -->
<div><div><div><div>Content</div></div></div></div>

<!-- ✅ CORRECT -->
<section class="hero">
  <p>Content</p>
</section>
```

---

## 3. BLOCK B — HTML ATTRIBUTES & VALUES

### B1. Attribute Quoting and Format

**What to check:**
```
❌ Mixed quote styles: src='img.jpg' alt="photo"
❌ Unquoted attributes: <input type=text>
❌ Boolean attribute with redundant value: disabled="disabled"
❌ Uppercase tag or attribute names: <INPUT TYPE="TEXT">
```

**Fix:**
```html
<!-- ❌ MEDIUM: mixed quoting -->
<img src='photo.jpg' alt="Photo">

<!-- ❌ MEDIUM: boolean with value -->
<input type="checkbox" disabled="disabled" checked="checked">

<!-- ✅ CORRECT: double quotes everywhere, boolean without value -->
<input type="checkbox" disabled checked>

<!-- ✅ Recommended attribute order -->
<!-- id → class → type/name → href/src → alt → data-* → aria-* -->
<img id="hero" class="hero__img" src="hero.jpg" alt="Hero banner"
     width="1200" height="600" loading="lazy">
```

---

### B2. Required Attributes Per Element

| Element | Required attributes | Why |
|---------|--------------------|----|
| `<img>` | `alt`, `width`, `height` | Accessibility + no CLS |
| `<input>` | `type` | Default is `text`, unexpected behavior |
| `<a>` | `href` | Without it, not a link |
| `<form>` | `action`, `method` | Explicit GET/POST |
| `<script src>` | `defer` or `async` | Avoid parser blocking |
| `<iframe>` | `title` | Required for screen readers |
| `<button>` inside `<form>` | `type` | Default is `submit`, often unintended |

```html
<!-- ❌ HIGH: button without type submits the form unintentionally -->
<form>
  <button>Cancel</button>  <!-- submits the form! -->
</form>

<!-- ✅ CORRECT -->
<form>
  <button type="button" onclick="cancel()">Cancel</button>
  <button type="submit">Submit</button>
</form>
```

---

### B3. External Links Security

```html
<!-- ❌ HIGH: tabnapping vulnerability -->
<a href="https://external.com" target="_blank">Link</a>

<!-- ✅ CORRECT -->
<a href="https://external.com" target="_blank" rel="noopener noreferrer">Link</a>

<!-- ❌ CRITICAL: javascript: href -->
<a href="javascript:doSomething()">Click</a>

<!-- ✅ CORRECT -->
<button type="button">Click</button>
<!-- use addEventListener — no inline handlers -->
```

---

## 4. BLOCK C — HTML FORMS

### C1. Label Association

**What to check:**
```
❌ Input without any label — completely inaccessible
❌ Label not linked to input (missing for + id pair)
❌ Placeholder used as the only label
❌ Required fields without required attribute
❌ Error messages not linked via aria-describedby
```

**Fix:**
```html
<!-- ❌ CRITICAL: no label -->
<input type="email" placeholder="Enter email">

<!-- ❌ HIGH: label not linked -->
<label>Email</label>
<input type="email">

<!-- ✅ CORRECT: full accessible form field -->
<div class="field">
  <label for="email">
    Email <span aria-hidden="true">*</span>
  </label>
  <input
    type="email"
    id="email"
    name="email"
    autocomplete="email"
    required
    aria-required="true"
    aria-describedby="email-error"
    placeholder="you@example.com"
  >
  <span id="email-error" role="alert" class="field__error" aria-live="polite"></span>
</div>
```

---

### C2. Input Types

```html
<!-- ❌ MEDIUM: wrong input types — use text for everything -->
<input type="text" name="email">
<input type="text" name="phone">

<!-- ✅ Correct types + inputmode + autocomplete -->
<input type="email"    name="email"    autocomplete="email">
<input type="tel"      name="phone"    autocomplete="tel"              inputmode="tel">
<input type="url"      name="website"  autocomplete="url">
<input type="number"   name="quantity" min="1" max="99"               inputmode="numeric">
<input type="search"   name="q"        role="searchbox">
<input type="password" name="password" autocomplete="current-password">
<input type="date"     name="dob"      autocomplete="bday">
```

---

## 5. BLOCK D — IMAGES & MEDIA

### D1. Image Requirements

```html
<!-- ❌ CRITICAL: no alt -->
<img src="photo.jpg">

<!-- ❌ HIGH: no dimensions — CLS (Core Web Vital) -->
<img src="photo.jpg" alt="Team photo">

<!-- ✅ CORRECT: full image declaration -->
<img
  src="photo-800.jpg"
  srcset="photo-400.jpg 400w,
          photo-800.jpg 800w,
          photo-1600.jpg 1600w"
  sizes="(max-width: 600px) 100vw,
         (max-width: 1024px) 50vw,
         800px"
  alt="Our team at the 2024 annual meetup"
  width="800"
  height="600"
  loading="lazy"
  decoding="async"
>

<!-- ✅ Decorative image — empty alt -->
<img src="wave.svg" alt="" aria-hidden="true">
```

---

### D2. SVG Standards

```html
<!-- ❌ MEDIUM: no viewBox — doesn't scale -->
<svg width="24" height="24"><path d="..."/></svg>

<!-- ✅ Decorative SVG icon -->
<svg viewBox="0 0 24 24" width="24" height="24"
     aria-hidden="true" focusable="false">
  <path d="..."/>
</svg>

<!-- ✅ Meaningful standalone SVG -->
<svg viewBox="0 0 200 100" role="img" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">Monthly Revenue</title>
  <desc id="chart-desc">Revenue grew from $10k to $50k over 6 months</desc>
</svg>
```

---

### D3. Video and Audio

```html
<!-- ❌ HIGH: autoplays with sound — fails in most browsers -->
<video src="promo.mp4" autoplay></video>

<!-- ✅ CORRECT -->
<video
  src="promo.mp4"
  controls
  preload="none"
  poster="poster.jpg"
  muted
  playsinline
>
  <track kind="subtitles" src="en.vtt" srclang="en" label="English" default>
  <p>Your browser doesn't support video. <a href="promo.mp4">Download</a></p>
</video>
```

---

## 6. BLOCK E — ACCESSIBILITY (A11Y)

### E1. ARIA Rules

```html
<!-- ❌ HIGH: div pretending to be a button -->
<div class="btn" onclick="submit()">Submit</div>

<!-- ✅ Native button — keyboard, focus, semantics included -->
<button type="button" class="btn">Submit</button>

<!-- ❌ HIGH: icon button with no accessible name -->
<button><svg>...</svg></button>

<!-- ✅ CORRECT -->
<button aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<!-- ✅ Expandable widget -->
<button aria-expanded="false" aria-controls="menu-list" id="menu-btn">
  Navigation
</button>
<ul id="menu-list" role="list" hidden>...</ul>

<!-- ✅ Live region for dynamic content -->
<div aria-live="polite" aria-atomic="true" class="sr-only" id="status"></div>
```

---

### E2. Keyboard Navigation

**What to check:**
```
❌ outline: none without :focus-visible replacement
❌ Custom interactive elements not reachable by Tab
❌ Modal/dialog doesn't trap focus
❌ No skip navigation link
❌ tabindex values > 0 (breaks natural order)
❌ Dropdown/modal not closeable by Escape
```

```html
<!-- ✅ Skip link — first interactive element on page -->
<a href="#main-content" class="skip-link">Skip to main content</a>
<main id="main-content" tabindex="-1">...</main>
```

```css
/* ❌ CRITICAL: removes focus for everyone */
:focus { outline: none; }

/* ✅ Remove for mouse, keep for keyboard */
:focus:not(:focus-visible) { outline: none; }
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
  border-radius: 3px;
}
```

---

### E3. Color and Contrast (WCAG 2.1 AA)

| Text type | Minimum ratio | Recommended |
|-----------|--------------|-------------|
| Regular text (< 18px / < 14px bold) | 4.5:1 | 7:1 |
| Large text (≥ 18px / ≥ 14px bold) | 3:1 | 4.5:1 |
| UI components, icons, borders | 3:1 | — |

```html
<!-- ❌ HIGH: error indicated only by color (red border) -->
<input type="text" class="error">

<!-- ✅ CORRECT: color + icon + text -->
<div class="field field--error">
  <input type="text" aria-invalid="true" aria-describedby="field-error">
  <span id="field-error" class="field__error" role="alert">
    <svg aria-hidden="true"><!-- error icon --></svg>
    This field is required
  </span>
</div>
```

---

## 7. BLOCK F — HTML PERFORMANCE & SECURITY

### F1. Resource Loading

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Preconnect to critical origins -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Preload critical resources -->
  <link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/images/hero.jpg" as="image">

  <!-- CSS -->
  <link rel="stylesheet" href="/css/critical.css">

  <!-- Scripts — always defer or async -->
  <script src="/js/app.js" defer></script>
  <script src="/js/analytics.js" async></script>

  <!-- Prefetch next pages -->
  <link rel="prefetch" href="/about/">
</head>
```

**What to check:**
```
❌ <script src> in <head> without defer or async — blocks parsing
❌ CSS via @import — extra round-trip
❌ No preload for LCP image
❌ No preload for critical fonts
❌ Inline event handlers onclick="..."
❌ Inline styles style="..."
```

---

### F2. HTML Security

```html
<!-- ✅ Content Security Policy -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'; style-src 'self'">

<!-- ❌ CRITICAL: javascript: href — XSS vector -->
<a href="javascript:doSomething()">Click</a>

<!-- ❌ HIGH: data: URL — XSS vector -->
<img src="data:image/svg+xml,<svg><script>alert(1)</script></svg>">
```

---

## 8. BLOCK G — CSS ARCHITECTURE & ORGANIZATION

### G1. Methodology Consistency

| Methodology | Core principle | Violation signal |
|-------------|---------------|-----------------|
| BEM | `.block__element--modifier` | Classes like `.header-title-blue-big` |
| SMACSS | Base / Layout / Module / State / Theme | No layer separation |
| ITCSS | Inverted triangle specificity | Utilities before components |
| Utility-first | Single-purpose classes | Mixed with custom BEM |

**ITCSS layer order:**
```css
/* 1. Settings   — variables, tokens */
/* 2. Tools      — mixins, functions */
/* 3. Generic    — box-sizing reset, normalize */
/* 4. Elements   — bare tag styles (a, p, h1) */
/* 5. Objects    — layout patterns (.container, .grid) */
/* 6. Components — visual components (.card, .btn) */
/* 7. Utilities  — overrides (.sr-only, .visually-hidden) */
```

---

### G2. Property Order

```css
.element {
  /* 1. Positioning */
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  z-index: var(--z-raised);

  /* 2. Box model */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-4) var(--space-6);
  overflow: hidden;

  /* 3. Typography */
  font-family: var(--font-sans);
  font-size: var(--text-base);
  font-weight: 400;
  line-height: 1.6;
  color: var(--color-text);

  /* 4. Visual */
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);

  /* 5. Animation */
  transform: translateY(0);
  transition: transform 0.2s ease-out, opacity 0.2s ease-out;
}
```

---

## 9. BLOCK H — CSS SELECTORS & SPECIFICITY

### H1. Specificity Rules

| Selector | Specificity | Recommendation |
|----------|------------|---------------|
| `!important` | ∞ | ❌ Only in utilities |
| `#id` | (1,0,0) | ❌ Never in CSS |
| `.class`, `[attr]`, `:pseudo-class` | (0,1,0) | ✅ Primary tool |
| `element` (div, p) | (0,0,1) | ✅ Base styles only |
| `*` universal | (0,0,0) | ⚠️ Reset only |

```css
/* ❌ MEDIUM: ID selector */
#header { background: blue; }

/* ❌ MEDIUM: nesting > 3 levels */
.nav .nav__list .nav__item .nav__link:hover span { color: red; }

/* ❌ HIGH: !important outside utility */
.card { background: white !important; }

/* ❌ LOW: element+class redundancy */
div.container { max-width: 1200px; }

/* ✅ CORRECT */
.container { max-width: 1200px; }
.nav__link:hover { color: var(--color-primary); }

/* ✅ !important only in utilities */
.visually-hidden {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  clip: rect(0, 0, 0, 0) !important;
  overflow: hidden !important;
}
```

---

## 10. BLOCK I — CSS CUSTOM PROPERTIES & DESIGN TOKENS

### I1. Complete Token System

**What to check:**
```
❌ Color values hardcoded everywhere (#3498db appears 23 times)
❌ Spacing values are magic numbers: margin: 13px, padding: 7px
❌ Border-radius inconsistent without a scale
❌ Box-shadow values duplicated
❌ z-index war: 9999, 99999, 999999
```

```css
:root {
  /* ── Color palette ── */
  --color-primary-50:  #eff6ff;
  --color-primary-500: #3b82f6;   /* main */
  --color-primary-700: #1d4ed8;
  --color-neutral-50:  #f8fafc;
  --color-neutral-900: #0f172a;

  /* ── Semantic colors ── */
  --color-bg:           var(--color-neutral-50);
  --color-text:         var(--color-neutral-900);
  --color-text-muted:   #475569;
  --color-border:       #e2e8f0;
  --color-accent:       var(--color-primary-500);
  --color-accent-hover: var(--color-primary-700);
  --color-success: #065f46;
  --color-warning: #92400e;
  --color-danger:  #991b1b;

  /* ── Dark mode ── */
  @media (prefers-color-scheme: dark) {
    --color-bg:      #0f172a;
    --color-text:    #f1f5f9;
    --color-border:  #334155;
  }

  /* ── Typography ── */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.25rem;
  --text-xl:   1.5rem;
  --text-2xl:  2rem;
  --text-3xl:  2.5rem;
  --text-4xl:  3rem;

  /* ── Spacing (8px grid) ── */
  --space-1:  4px;   --space-2:  8px;   --space-3:  12px;
  --space-4:  16px;  --space-6:  24px;  --space-8:  32px;
  --space-12: 48px;  --space-16: 64px;  --space-24: 96px;

  /* ── Border radius ── */
  --radius-sm:   4px;  --radius-md:   8px;
  --radius-lg:   12px; --radius-xl:   16px;
  --radius-full: 9999px;

  /* ── Shadows ── */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.18);
  --shadow-xl: 0 16px 48px rgba(0,0,0,0.22);

  /* ── Z-index system ── */
  --z-base: 0; --z-raised: 10; --z-dropdown: 100;
  --z-sticky: 200; --z-modal: 400; --z-toast: 500; --z-tooltip: 600;

  /* ── Transitions ── */
  --ease-out:    cubic-bezier(0, 0, 0.2, 1);
  --ease-in:     cubic-bezier(0.4, 0, 1, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --duration-fast:   150ms;
  --duration-normal: 250ms;
  --duration-slow:   400ms;
}
```

---

## 11. BLOCK J — UNITS & VALUES

| Unit | Use for | Mistake |
|------|---------|---------|
| `rem` | Font sizes, spacing | `px` for font-size on body |
| `em` | Component-relative spacing | Global layout |
| `px` | Borders, shadows, breakpoints | Font sizes |
| `%` | Column widths, flex basis | Heights |
| `dvh` / `svh` | Mobile viewport height | `vh` on mobile |
| `fr` | Grid columns | `%` in grid with gap |
| `ch` | Prose max-width | `px` for text width |
| `clamp()` | Fluid typography | Media queries for font-size |

```css
/* ❌ MEDIUM: px font-size ignores accessibility settings */
body { font-size: 16px; }
h1   { font-size: 32px; }

/* ✅ rem + clamp */
body { font-size: 1rem; }
h1   { font-size: clamp(1.5rem, 4vw, 3rem); }

/* ❌ MEDIUM: 0 with unit — verbose */
margin: 0px; padding: 0rem;
/* ✅ */ margin: 0; padding: 0;

/* ❌ HIGH: vh breaks on mobile (address bar shifts layout) */
.hero { height: 100vh; }
/* ✅ dvh = dynamic viewport height */
.hero { height: 100dvh; }
/* With fallback: */
.hero { height: 100vh; height: 100dvh; }

/* ❌ MEDIUM: % in grid with gap causes overflow */
.grid { display: grid; grid-template-columns: repeat(3, 33.33%); gap: 20px; }
/* ✅ fr handles gap automatically */
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }

/* ✅ ch for prose width */
.prose { max-width: 65ch; }
```

---

## 12. BLOCK K — FLEXBOX & GRID

### K1. Flexbox Bugs

```css
/* ❌ HIGH: text truncation doesn't work in flex items */
.flex-item {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  /* won't work — flex items have implicit min-width: auto */
}

/* ✅ CORRECT: min-width: 0 is the key fix */
.flex-item {
  min-width: 0;           /* allows shrinking below content size */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ❌ MEDIUM: icons shrink unexpectedly */
.card__icon { /* no flex-shrink: 0 */ }
/* ✅ */ .card__icon { flex-shrink: 0; }

/* ✅ Multi-line text truncation */
.truncate-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

---

### K2. Grid Bugs

```css
/* ✅ auto-fill vs auto-fit */
/* auto-fill: keeps empty tracks */
/* auto-fit: collapses empty tracks (items stretch to fill) */
.grid { grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }

/* ✅ Responsive grid — no media queries needed */
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(280px, 100%), 1fr));
  gap: var(--space-6);
}

/* ✅ Equal-height cards */
.cards { display: grid; align-items: stretch; }
.card  { display: flex; flex-direction: column; }
.card__body { flex: 1; }

/* ✅ Named template areas */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 280px 1fr;
  min-height: 100dvh;
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

---

## 13. BLOCK L — RESPONSIVE DESIGN

### L1. Mobile-First

```css
/* ✅ Mobile-first breakpoints */
:root {
  --bp-sm: 600px; --bp-md: 768px;
  --bp-lg: 1024px; --bp-xl: 1280px; --bp-2xl: 1536px;
}

/* Base: mobile */
.component { display: block; padding: var(--space-4); }

@media (min-width: 768px) {
  .component { display: grid; grid-template-columns: 1fr 1fr; }
}
@media (min-width: 1024px) {
  .component { grid-template-columns: 1fr 1fr 1fr; }
}

/* ✅ No horizontal scroll */
html { overflow-x: hidden; }
*, *::before, *::after { box-sizing: border-box; }
img, video, svg { max-width: 100%; height: auto; }

/* ✅ Touch targets */
@media (pointer: coarse) {
  button, a, [role="button"] {
    min-height: 44px;
    min-width: 44px;
  }
}
```

---

### L2. Container Queries

```css
/* ✅ Component adapts to its container, not the viewport */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card { flex-direction: row; }
  .card__image { width: 160px; flex-shrink: 0; }
}
```

---

## 14. BLOCK M — CSS PERFORMANCE & ANIMATION

### M1. Expensive Animations

```css
/* ❌ HIGH: triggers reflow on every frame */
.el { transition: left 0.3s, margin-top 0.3s, width 0.3s; }

/* ✅ Compositor-only — GPU-accelerated, no reflow */
.el { transition: transform 0.3s var(--ease-out), opacity 0.3s var(--ease-out); }
/* Replace left: 100px → transform: translateX(100px) */

/* ✅ will-change only when animation is about to happen */
.card:hover { will-change: transform; }
/* NOT on every .card — creates GPU layers for all cards */

/* ✅ MANDATORY: prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration:        0.01ms !important;
    animation-iteration-count: 1      !important;
    transition-duration:       0.01ms !important;
    scroll-behavior:           auto   !important;
  }
}
```

---

### M2. CSS Performance

```css
/* ✅ contain isolates reflow to the component */
.card-list-item {
  contain: layout paint style;
}

/* ✅ Font loading */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}

/* ✅ content-visibility for long pages */
.below-fold-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

---

## 15. BLOCK N — CSS ANTI-PATTERNS

```css
/* ❌ CRITICAL: missing global reset */
/* ✅ MANDATORY */
*, *::before, *::after { box-sizing: border-box; }

/* ❌ MEDIUM: float-based clearfix */
.clearfix::after { content: ""; display: table; clear: both; }
/* ✅ Modern: flexbox or grid */
.container { display: flex; flex-wrap: wrap; gap: var(--space-4); }

/* ❌ LOW: manual vendor prefixes */
-webkit-transform: translateX(10px);
-moz-transform: translateX(10px);
transform: translateX(10px);
/* ✅ Use Autoprefixer in build pipeline */

/* ❌ MEDIUM: hacky absolute centering */
.center { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); }
/* ✅ Modern centering */
.center-parent { display: grid; place-items: center; }
```

---

## 16. BLOCK O — JS SYNTAX & MODERN STANDARDS

### O1. Variable Declarations

```javascript
// ❌ CRITICAL: var — hoisting, function scope, no block scope
var count = 0;
for (var i = 0; i < 10; i++) { /* i leaks outside loop */ }

// ❌ HIGH: let for non-changing values
let MAX_ITEMS = 100;

// ❌ CRITICAL: implicit global
function setup() { userName = 'Alice'; } // creates window.userName

// ✅ CORRECT
const MAX_ITEMS = 100;
let count = 0;  // only let when value actually changes
function setup() { const userName = 'Alice'; }
```

---

### O2. Modern Syntax

```javascript
// ❌ HIGH: string concatenation
var msg = 'Hello, ' + name + '! You have ' + count + ' messages.';
// ✅ Template literal
const msg = `Hello, ${name}! You have ${count} messages.`;

// ❌ MEDIUM: && chain
const city = user && user.address && user.address.city;
// ✅ Optional chaining
const city = user?.address?.city;

// ❌ MEDIUM: || breaks on 0, "", false
const timeout = options.timeout || 5000;  // 0 → uses 5000 (wrong!)
// ✅ ?? — only null/undefined triggers fallback
const timeout = options.timeout ?? 5000;

// ❌ MEDIUM: Object.assign for clone
const merged = Object.assign({}, defaults, options);
// ✅ Spread
const merged = { ...defaults, ...options };

// ❌ MEDIUM: for...in on arrays
for (const i in items) { /* iterates prototype chain too */ }
// ✅ for...of
for (const item of items) { }

// ✅ Destructuring
const { name, email, role = 'user' } = userData;
const [first, second, ...rest] = items;
```

---

## 17. BLOCK P — NAMING CONVENTIONS

| Entity | Convention | Example |
|--------|-----------|---------|
| Variables, functions | `camelCase` | `getUserData`, `isLoading` |
| Classes, constructors | `PascalCase` | `UserService`, `EventEmitter` |
| Compile-time constants | `SCREAMING_SNAKE` | `MAX_RETRY_COUNT` |
| Private class fields | `#field` | `#cache`, `#state` |
| Boolean variables | `is/has/can/should` prefix | `isVisible`, `hasError` |
| Event handlers | `handle` + Event | `handleClick`, `handleSubmit` |
| Async functions | verb + noun | `fetchUser`, `loadConfig` |
| Module files | `kebab-case` | `user-service.js` |

```javascript
// ❌ BAD: uninformative
const d = new Date();
function fn(x) { return x * 2; }
const loading = false;

// ✅ GOOD: self-documenting
const createdAt = new Date();
function doubleValue(value) { return value * 2; }
const isLoading = false;
const isFormValid = validate(form);
```

---

## 18. BLOCK Q — FUNCTIONS & DESIGN PRINCIPLES

### Q1. Single Responsibility

```javascript
// ❌ HIGH: function does too many things
function processUser(userData) {
  if (!userData.email) throw new Error('No email');
  userData.name = userData.name.trim().toLowerCase();
  db.save(userData);
  emailService.send(userData.email, 'Welcome!');
}

// ✅ One function, one job
function validateUser(user) {
  if (!user.email) throw new ValidationError('email', 'Required');
  if (!user.name)  throw new ValidationError('name', 'Required');
}
function normalizeUser(user) {
  return { ...user, name: user.name.trim().toLowerCase() };
}
async function createUser(userData) {
  validateUser(userData);
  const user = normalizeUser(userData);
  await db.save(user);
  await emailService.sendWelcome(user.email);
  return user;
}

// ❌ MEDIUM: magic numbers
if (users.length > 50) { paginate(); }
setTimeout(refresh, 3600000);

// ✅ Named constants
const MAX_USERS_PER_PAGE = 50;
const ONE_HOUR_MS = 60 * 60 * 1000;
```

---

### Q2. Early Return Pattern

```javascript
// ❌ MEDIUM: arrow-shaped nesting
function processOrder(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.payment) {
        if (order.payment.isValid) {
          return completeOrder(order);
        } else { return { error: 'Invalid payment' }; }
      } else { return { error: 'No payment' }; }
    } else { return { error: 'Empty cart' }; }
  } else { return { error: 'No order' }; }
}

// ✅ Early return — linear, readable
function processOrder(order) {
  if (!order)                 return { error: 'No order' };
  if (!order.items.length)    return { error: 'Empty cart' };
  if (!order.payment)         return { error: 'No payment' };
  if (!order.payment.isValid) return { error: 'Invalid payment' };
  return completeOrder(order);
}
```

---

## 19. BLOCK R — ASYNC CODE & ERROR HANDLING

### R1. Async/Await Standards

```javascript
// ❌ CRITICAL: callback hell
getUser(id, (err, user) => {
  getOrders(user.id, (err, orders) => {
    getPayments(orders[0].id, (err, payments) => { /* ... */ });
  });
});

// ❌ HIGH: unhandled rejection — no .catch()
fetch('/api/data').then(res => res.json()).then(render);

// ❌ HIGH: sequential awaits when parallel is fine
const user   = await getUser(id);
const config = await getConfig();    // waits for user unnecessarily

// ✅ Parallel when no dependency
const [user, config] = await Promise.all([getUser(id), getConfig()]);

// ✅ Full async with error handling
async function loadDashboard(userId) {
  try {
    const [user, orders] = await Promise.all([
      fetchUser(userId),
      fetchOrders(userId),
    ]);
    return { user, orders };
  } catch (error) {
    logger.error('Dashboard load failed', { userId, error });
    throw new AppError('Failed to load dashboard', { cause: error });
  }
}
```

---

### R2. Custom Error Classes

```javascript
// ✅ Error hierarchy
class AppError extends Error {
  constructor(message, { code = 'UNKNOWN_ERROR', cause, context } = {}) {
    super(message);
    this.name    = this.constructor.name;
    this.code    = code;
    this.cause   = cause;
    this.context = context;
  }
}

class ValidationError extends AppError {
  constructor(field, message) {
    super(message, { code: 'VALIDATION_ERROR', context: { field } });
  }
}

class NetworkError extends AppError {
  constructor(url, status) {
    super(`Request to ${url} failed with ${status}`, {
      code: 'NETWORK_ERROR', context: { url, status }
    });
  }
}

// Usage — catch by type
try {
  await fetchUser(id);
} catch (error) {
  if (error instanceof NotFoundError) return res.status(404).json({ error: error.message });
  if (error instanceof NetworkError)  return res.status(502).json({ error: 'Upstream error' });
  throw error;
}
```

---

## 20. BLOCK S — DOM & EVENTS

### S1. DOM Query Caching

```javascript
// ❌ HIGH: DOM query inside loop — N queries per render
function updateItems(items) {
  items.forEach(item => {
    const list = document.getElementById('list'); // queried N times!
    list.appendChild(createItem(item));
  });
}

// ✅ Cache once, use DocumentFragment for batch insert
function updateItems(items) {
  const list = document.getElementById('list');
  const fragment = document.createDocumentFragment();
  items.forEach(item => fragment.appendChild(createItem(item)));
  list.appendChild(fragment);
}
```

---

### S2. Event Delegation

```javascript
// ❌ HIGH: N listeners for N items
document.querySelectorAll('.action-btn').forEach(btn => {
  btn.addEventListener('click', handleAction);
});

// ✅ One listener on the parent
document.getElementById('action-list').addEventListener('click', (event) => {
  const btn = event.target.closest('.action-btn');
  if (!btn) return;
  handleAction(btn.dataset.action);
});

// ✅ AbortController — clean removal of all listeners
class Component {
  #controller = new AbortController();

  mount() {
    const { signal } = this.#controller;
    window.addEventListener('resize',   this.#onResize,  { signal });
    document.addEventListener('click',  this.#onClick,   { signal });
    document.addEventListener('keydown', this.#onKeydown, { signal });
  }

  unmount() {
    this.#controller.abort(); // removes ALL listeners at once
  }

  #onResize  = debounce(() => this.#recalculate(), 250);
  #onKeydown = (e) => { if (e.key === 'Escape') this.#close(); };
}
```

---

### S3. Layout Thrashing

```javascript
// ❌ HIGH: interleaved reads and writes
elements.forEach(el => {
  const h = el.offsetHeight;          // read → forces layout
  el.style.height = (h + 10) + 'px'; // write → invalidates
});

// ✅ All reads, then all writes
const heights = elements.map(el => el.offsetHeight); // all reads
elements.forEach((el, i) => {
  el.style.height = (heights[i] + 10) + 'px';        // all writes
});
```

---

## 21. BLOCK T — JAVASCRIPT SECURITY

### T1. XSS Vulnerabilities

```javascript
// ❌ CRITICAL: innerHTML with user data
element.innerHTML = comment.text;
element.innerHTML = `<div>${post.body}</div>`;

// ❌ CRITICAL: eval
eval(userCode);
new Function(userCode)();
setTimeout(userString, 1000); // string arg = eval!

// ❌ CRITICAL: document.write
document.write('<script>' + code + '</script>');

// ✅ textContent — automatic escaping
element.textContent = comment.text;

// ✅ createElement — safe DOM building
function createPost(post) {
  const article = document.createElement('article');
  const h2 = document.createElement('h2');
  h2.textContent = post.title;  // safe
  const p = document.createElement('p');
  p.textContent = post.body;    // safe
  article.append(h2, p);
  return article;
}

// ✅ DOMPurify — only when HTML is truly needed
element.innerHTML = DOMPurify.sanitize(richText, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
  ALLOWED_ATTR: ['href'],
});
```

---

### T2. Other Security Issues

```javascript
// ❌ CRITICAL: secrets in client JS — visible in DevTools
const API_KEY = 'sk-1234567890abcdef';  // never do this

// ❌ HIGH: sensitive data in localStorage (XSS can read it)
localStorage.setItem('authToken', token);
// ✅ Use HttpOnly cookies (server-side, inaccessible from JS)

// ❌ HIGH: prototype pollution
function merge(target, source) {
  for (let key in source) { target[key] = source[key]; } // __proto__ attack
}
// ✅ Safe merge using own keys only
function safeMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (Object.hasOwn(source, key)) target[key] = source[key];
  }
  return target;
}

// ❌ MEDIUM: console.log in production
console.log('User data:', userData);
// ✅ Strip with build tools or conditional
if (import.meta.env.DEV) console.log('User data:', userData);
```

---

## 22. BLOCK U — JS PERFORMANCE

### U1. Event Optimization

```javascript
// ✅ Throttle — limit call frequency (scroll)
function throttle(fn, delay) {
  let lastCall = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastCall >= delay) { lastCall = now; return fn(...args); }
  };
}
window.addEventListener('scroll', throttle(updateStickyHeader, 16));

// ✅ Debounce — call after pause (resize, input)
function debounce(fn, delay) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), delay); };
}
window.addEventListener('resize', debounce(recalculateLayout, 250));
searchInput.addEventListener('input', debounce(search, 300));

// ✅ IntersectionObserver — visibility without scroll listener
const observer = new IntersectionObserver(
  ([entry]) => { if (entry.isIntersecting) loadContent(entry.target); },
  { threshold: 0.1, rootMargin: '50px' }
);
lazyElements.forEach(el => observer.observe(el));
```

---

### U2. Memory Leaks

```javascript
// ❌ HIGH: setInterval never cleared
class Poller {
  start() { setInterval(() => this.fetch(), 5000); } // interval ID lost!
}

// ✅ Store and clear
class Poller {
  #intervalId = null;
  start() { this.#intervalId = setInterval(() => this.#fetch(), 5000); }
  stop()  { clearInterval(this.#intervalId); this.#intervalId = null; }
}

// ❌ HIGH: Map holds DOM nodes — prevents GC
const data = new Map();
data.set(domNode, { clicks: 0 });  // domNode removed but Map keeps it alive

// ✅ WeakMap — GC can collect when node is removed
const data = new WeakMap();
data.set(domNode, { clicks: 0 });

// ❌ MEDIUM: closure captures large object unnecessarily
function createHandler(response) {
  return () => console.log(response.data.users[0].name); // holds all of response
}
// ✅ Capture only what you need
function createHandler(response) {
  const username = response.data.users[0].name;
  return () => console.log(username);
}
```

---

## 23. BLOCK V — MODULARITY & CODE ORGANIZATION

```javascript
// ❌ HIGH: global namespace pollution
window.myApp = {};
window.myApp.utils = { formatDate: () => {} };

// ❌ MEDIUM: default export without name (can't tree-shake)
export default function() { ... }

// ✅ Named exports — tree-shakeable
export function formatDate(date, locale = 'en-US') {
  return new Intl.DateTimeFormat(locale).format(date);
}
export function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(amount);
}

// ✅ Circular imports — always an architecture bug, refactor
// A → B → A creates tight coupling and runtime errors

// ✅ Recommended structure
// src/
//   components/   Button.js, Modal.js, Card.js
//   services/     api.js, auth.js, storage.js
//   utils/        format.js, validate.js, dom.js
//   constants/    routes.js, config.js, events.js
//   hooks/        useUser.js, useScroll.js  (React)
//   types/        user.ts, api.ts           (TypeScript)
```

---

## 24. BLOCK W — COMMENTS & DOCUMENTATION

```javascript
// ❌ LOW: obvious comment
i++;  // increment i
return null;  // return null

// ❌ LOW: dead code in production
// const oldFunction = () => { /* 200 lines */ };

// ❌ MEDIUM: vague TODO
// TODO: fix this

// ✅ WHY comments — explain non-obvious reasoning
// Debounce 300ms because Safari fires resize twice when
// the address bar shows/hides on scroll
window.addEventListener('resize', debounce(recalculate, 300));

// ✅ TODO with full context
// TODO(alex, 2025-06): Replace with Intl.Segmenter when Safari ships it
// Tracked: https://github.com/org/repo/issues/1234

// ✅ JSDoc for public API
/**
 * Calculates final price after discount and tax.
 * NOTE: Tax applied AFTER discount — per accounting requirements.
 *
 * @param {number} price    - Base price
 * @param {number} discount - Discount percentage (0–100)
 * @param {number} taxRate  - Tax rate percentage
 * @returns {number} Final price rounded to 2 decimal places
 * @throws {RangeError} If discount or taxRate outside 0–100
 *
 * @example
 * calculateTotal(100, 20, 10) // → 88.00
 */
function calculateTotal(price, discount, taxRate) {
  if (discount < 0 || discount > 100) throw new RangeError('discount must be 0–100');
  const discounted = price * (1 - discount / 100);
  return Math.round(discounted * (1 + taxRate / 100) * 100) / 100;
}
```

---

## 25. BLOCK X — TESTABILITY & CODE QUALITY

```javascript
// ❌ HIGH: untestable — creates dependencies internally
function sendReport(userId) {
  const db     = new Database();     // can't mock
  const mailer = new EmailService(); // can't mock
  const user   = db.findById(userId);
  mailer.send(user.email, 'report');
}

// ✅ Dependency injection — fully testable
async function sendReport(userId, { db, mailer }) {
  const user = await db.findById(userId);
  await mailer.send(user.email, 'report');
}
// Test: await sendReport(1, { db: mockDb, mailer: mockMailer });

// ❌ HIGH: pure logic mixed with side effects
function getDiscount(cart) {
  const discount = cart.total > 100 ? 0.1 : 0; // pure
  logger.log('discount', discount);             // side effect mixed in
  return discount;
}

// ✅ Separate pure computation from side effects
function calculateDiscount(cartTotal) { // pure — easy to test
  return cartTotal > 100 ? 0.1 : 0;
}
async function applyDiscount(cart) {   // impure — orchestrates
  const discount = calculateDiscount(cart.total);
  logger.log('discount', discount);
  return discount;
}

// ✅ Pure utility functions — always testable
const clamp    = (val, min, max) => Math.min(Math.max(val, min), max);
const groupBy  = (arr, key) => arr.reduce((acc, item) => {
  (acc[item[key]] ??= []).push(item); return acc;
}, {});
```

---

## 26. FINAL REPORT TEMPLATE

```
═══════════════════════════════════════════════════════════════════════
              CODE CHECK REPORT — [Project Name / URL]
═══════════════════════════════════════════════════════════════════════

SUMMARY
───────────────────────────────────────────────────────────────────────
Date:              [date]
Files reviewed:    HTML: X  |  CSS: X  |  JS: X
Lines of code:     ~XXXX
Bugs found:        [total]
  🔴 CRITICAL: X
  🟠 HIGH:     X
  🟡 MEDIUM:   X
  🟢 LOW:      X

CRITICAL BUGS — Fix immediately
───────────────────────────────────────────────────────────────────────
[ID: C-001]  🔴 CRITICAL
Block:     T1 — XSS Security
File:      src/components/Comment.js, line 47
Problem:   innerHTML with user-supplied data — XSS vulnerability
Before:    element.innerHTML = comment.text;
After:     element.textContent = comment.text;
           // or DOMPurify.sanitize() if HTML is genuinely needed

[ID: C-002]  🔴 CRITICAL
Block:     O1 — Variable Declarations
File:      src/app.js, lines 12, 34, 67, 91
Problem:   var throughout — hoisting bugs and scope leaks
Before:    var userName = getUser().name;
After:     const userName = getUser().name;
Notes:     Run eslint --fix with no-var rule to bulk-fix

HIGH BUGS
───────────────────────────────────────────────────────────────────────
[ID: H-001]  🟠 HIGH
Block:     E1 — Accessibility
File:      index.html, lines 23–31
Problem:   Search form has no label — inaccessible to screen readers
Before:    <input type="search" placeholder="Search...">
After:     <label for="search" class="visually-hidden">Search</label>
           <input type="search" id="search" placeholder="Search...">

[ID: H-002]  🟠 HIGH
Block:     R1 — Async/Await
File:      src/services/api.js, line 78
Problem:   fetch() with no .catch() — unhandled rejection in production
Before:    fetch('/api/data').then(res => res.json()).then(render);
After:     fetch('/api/data')
             .then(res => { if (!res.ok) throw new Error(res.status); return res.json(); })
             .then(render)
             .catch(err => { logger.error(err); showErrorToast(); });

MEDIUM BUGS
───────────────────────────────────────────────────────────────────────
[ID: M-001]  🟡 MEDIUM
...

LOW PRIORITY
───────────────────────────────────────────────────────────────────────
[ID: L-001]  🟢 LOW
...

SYSTEM RECOMMENDATIONS
───────────────────────────────────────────────────────────────────────
1. Add ESLint: no-var, prefer-const, no-eval, no-unused-vars, eqeqeq
2. Add Stylelint: stylelint-config-standard
3. Set up Prettier for consistent formatting
4. Add husky + lint-staged for pre-commit checks
5. Replace all hardcoded values with CSS Custom Properties
6. Add DOMPurify for any innerHTML usage
7. Consider TypeScript for larger service modules

═══════════════════════════════════════════════════════════════════════
```

---

## 27. QUICK SCAN CHECKLIST

### HTML
- [ ] `<!DOCTYPE html>` — first line of document
- [ ] `<html lang="en">` — language set
- [ ] `<meta charset="UTF-8">` — first in `<head>`
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- [ ] `<title>` — meaningful, not empty
- [ ] Only one `<h1>` per page
- [ ] Headings h1→h2→h3 without skipping levels
- [ ] Semantic tags: `header`, `main`, `footer`, `nav`, `article`, `section`
- [ ] No `<div>` where a semantic tag fits
- [ ] No block element inside inline (`<div>` inside `<span>`)
- [ ] No `<button>` inside `<a>` or vice versa
- [ ] All IDs unique within the document
- [ ] All `<img>` have `alt` (empty `alt=""` for decorative)
- [ ] All `<img>` have `width` and `height` (CLS prevention)
- [ ] `loading="lazy"` on images below the fold
- [ ] All `target="_blank"` have `rel="noopener noreferrer"`
- [ ] All `<input>` have explicit `type`
- [ ] All inputs/selects/textareas linked to a `<label>`
- [ ] CSS in `<head>`, JS with `defer` or `async`
- [ ] No `style="..."` inline attributes
- [ ] No `onclick="..."` inline event attributes

### CSS
- [ ] `*, *::before, *::after { box-sizing: border-box; }` global reset
- [ ] One CSS methodology chosen and applied consistently
- [ ] No ID selectors (`#id`) in CSS
- [ ] No `!important` outside utility classes
- [ ] Selector nesting ≤ 3 levels
- [ ] CSS Custom Properties for all repeating values
- [ ] Property order: positioning → box model → typography → visual → animation
- [ ] No `px` for `font-size` — use `rem`
- [ ] `0` without units (not `0px`, not `0rem`)
- [ ] `fr` in grid instead of `%` with `gap`
- [ ] `min-width: 0` on flex children containing truncated text
- [ ] `dvh` instead of `vh` for mobile viewports
- [ ] No `@import` in CSS files
- [ ] `@media (prefers-reduced-motion: reduce)` wraps all animations
- [ ] Only `transform` and `opacity` animated (not `width`/`top`/`left`)
- [ ] No horizontal scroll on 320px viewport

### JavaScript
- [ ] No `var` — only `const` and `let`
- [ ] `'use strict'` or ES Modules
- [ ] No string concatenation — use template literals
- [ ] Optional chaining `?.` instead of `&&` chains
- [ ] Nullish coalescing `??` instead of `||` for defaults
- [ ] `camelCase` for variables/functions, `PascalCase` for classes
- [ ] Booleans use `is`/`has`/`can`/`should` prefix
- [ ] One function, one job (SRP)
- [ ] No more than 3 parameters per function
- [ ] Early return instead of deep nesting
- [ ] No magic numbers — named constants only
- [ ] No duplicated code (DRY)
- [ ] All `async` functions wrapped in `try/catch`
- [ ] No unhandled Promise rejections
- [ ] No `innerHTML` with user-supplied data
- [ ] No `eval()`, `new Function()`, `document.write()`
- [ ] No API keys or secrets in client-side JS
- [ ] No `console.log` in production
- [ ] No global variables (`window.xxx`)
- [ ] DOM queries cached outside loops
- [ ] Event delegation for dynamic lists
- [ ] `AbortController` used to clean up listeners
- [ ] `debounce` on `input`/`resize`, `throttle` on `scroll`
- [ ] `IntersectionObserver` for visibility detection
- [ ] `DocumentFragment` for batch DOM insertions

---

*Code Check Protocol Guide v1.0 · HTML + CSS + JavaScript · 25 blocks · 150+ checks*
