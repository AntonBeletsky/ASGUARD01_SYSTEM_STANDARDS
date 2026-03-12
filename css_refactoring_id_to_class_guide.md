# CSS Refactoring Guide: `#id` → `.class`

> **Goal:** Migrate all `id`-based styling to `class`-based styling without breaking JS selectors,
> event listeners, form labels, anchor links, or ARIA attributes.

---

## Table of Contents

1. [Why Bother?](#1-why-bother)
2. [Before You Touch Anything](#2-before-you-touch-anything)
3. [Audit Phase — Find Every ID](#3-audit-phase--find-every-id)
4. [Classify Each ID](#4-classify-each-id)
5. [Naming Convention](#5-naming-convention)
6. [Step-by-Step Refactor](#6-step-by-step-refactor)
   - 6.1 [HTML](#61-html)
   - 6.2 [CSS](#62-css)
   - 6.3 [JavaScript](#63-javascript)
7. [Comment Convention](#7-comment-convention)
8. [Specificity Traps & How to Avoid Them](#8-specificity-traps--how-to-avoid-them)
9. [IDs You Must Keep](#9-ids-you-must-keep)
10. [Automated Helpers](#10-automated-helpers)
11. [QA Checklist](#11-qa-checklist)
12. [Real-World Example — Before & After](#12-real-world-example--before--after)

---

## 1. Why Bother?

| Problem with IDs | Result |
|---|---|
| Specificity `0-1-0-0` overrides almost everything | Causes impossible-to-debug cascade wars |
| Must be **unique** per page | Breaks reusable components |
| Tightly couples styling to JS/anchor hooks | One rename breaks three systems at once |
| Can't compose — one element, one ID | Classes compose freely |

**Rule of thumb:** IDs are for JS hooks, form labels, anchor links, and ARIA.  
Classes are for styling. Never mix the two roles onto a single `id`.

---

## 2. Before You Touch Anything

### 2.1 Snapshot the current state

```bash
# Visual regression baseline (requires Node)
npx percy snapshot index.html

# Or just take full-page screenshots manually — cheap but good enough
```

### 2.2 Freeze your test suite

Make sure all existing unit / integration / e2e tests pass **before** you start.  
Every green test that breaks during refactoring is a clear signal you missed something.

### 2.3 Create a feature branch

```bash
git checkout -b refactor/id-to-class
```

Commit after each logical chunk (one component, one section) — not at the end.  
Granular commits make bisecting easy if something silently breaks.

---

## 3. Audit Phase — Find Every ID

Run all four searches and collect results into a spreadsheet or a plain text file.

### 3.1 HTML ids
```bash
grep -rn 'id="' src/ --include="*.html"
```

### 3.2 CSS id selectors
```bash
grep -rn '#[a-zA-Z]' src/ --include="*.css"
# Also check SCSS/Less if applicable
grep -rn '#[a-zA-Z]' src/ --include="*.scss"
```

### 3.3 JS getElementById / querySelector('#…')
```bash
grep -rEn 'getElementById|querySelector\s*\(\s*['"](#[^'"]+)['"]\s*\)' src/ --include="*.js"
```

### 3.4 HTML references to IDs (labels, anchors, ARIA)
```bash
grep -rEn '(for|href|aria-labelledby|aria-describedby|aria-controls)="[^"]*[a-zA-Z][^"]*"' src/ --include="*.html"
```

---

## 4. Classify Each ID

For every ID found, assign one of four categories:

| Category | Description | Action |
|---|---|---|
| **A — Style only** | Used in CSS, never in JS/labels/anchors | Replace with class, remove id |
| **B — JS only** | Used in `getElementById` / `querySelector`, never in CSS | Keep id, add `data-` attribute as better practice |
| **C — Both** | Used in CSS **and** JS | Add class for styling, keep id for JS, add comment |
| **D — Structural** | `for=`, `href=#`, `aria-*` | Must keep id, optionally add class for styling |

---

## 5. Naming Convention

When creating the replacement class name, follow this pattern:

```
#{old-id}  →  .{old-id}          # simplest — just swap the sigil
#mainNav   →  .main-nav           # convert camelCase to kebab-case
#hdrLogo   →  .header__logo       # optionally adopt BEM
```

**Avoid** adding a suffix like `-class` or `-style` — it's noise.  
If the ID name was bad (e.g., `#div2`), use this as an opportunity to rename properly.

---

## 6. Step-by-Step Refactor

Work **one component at a time.** Complete all three layers (HTML → CSS → JS) before moving on.

### 6.1 HTML

**Category A (style only) — remove id, add class:**

```html
<!-- BEFORE -->
<nav id="main-nav">…</nav>

<!-- AFTER -->
<nav class="main-nav">…</nav>
```

**Category B (JS only) — keep id, optionally add data attribute:**

```html
<!-- BEFORE -->
<button id="submit-btn">Send</button>

<!-- AFTER — id kept for JS; no styling role -->
<!-- [JS] #submit-btn → used by submitForm() in form.js -->
<button id="submit-btn">Send</button>
```

**Category C (both) — keep id for JS, add class for styling:**

```html
<!-- BEFORE -->
<header id="site-header">…</header>

<!-- AFTER -->
<!-- [JS] #site-header → used by stickyHeader() in ui.js -->
<header id="site-header" class="site-header">…</header>
```

**Category D (structural) — keep id, add class if styling needed:**

```html
<!-- BEFORE -->
<input id="email-field" type="email">
<label for="email-field">Email</label>

<!-- AFTER — id required for label association -->
<!-- [A11Y] #email-field → bound to <label for="email-field"> -->
<input id="email-field" class="form__input" type="email">
<label for="email-field" class="form__label">Email</label>
```

---

### 6.2 CSS

**Simple replacement — Category A:**

```css
/* BEFORE */
#main-nav {
  display: flex;
  background: #1a1a2e;
}

/* AFTER */
.main-nav {
  display: flex;
  background: #1a1a2e;
}
```

**Nested selectors — watch specificity:**

```css
/* BEFORE */
#main-nav li a {
  color: white;
}

/* AFTER */
.main-nav li a {        /* specificity drops from 0-1-0-2 to 0-0-1-2 — fine */
  color: white;
}
```

**Category C — remove id selector, class already added in HTML:**

```css
/* BEFORE */
#site-header {
  position: sticky;
  top: 0;
}

/* AFTER — id kept in HTML for JS; styling moves to class */
/* [JS] .site-header mirrors #site-header — do not rename without updating ui.js */
.site-header {
  position: sticky;
  top: 0;
}
```

**Never leave orphaned id selectors in CSS** after the HTML id is gone —  
they are dead code and will confuse the next developer.

---

### 6.3 JavaScript

JavaScript is the riskiest layer. **Do not change JS during the CSS/HTML pass.**  
JS should be its own follow-up commit.

#### Option A — Keep getElementById (safest, zero JS risk)

If the id is kept in HTML (Category B, C, D), JS needs zero changes.

```js
// No change needed — id still exists in HTML
const btn = document.getElementById('submit-btn');
```

#### Option B — Migrate to querySelector + data attribute (cleaner long-term)

Add a `data-` attribute to the element, then update JS:

```html
<!-- HTML -->
<button id="submit-btn" data-action="submit" class="btn btn--primary">Send</button>
```

```js
// JS — before
const btn = document.getElementById('submit-btn');

// JS — after (id can now be removed from HTML once this lands)
const btn = document.querySelector('[data-action="submit"]');
```

#### Option C — Switch to querySelector('.class') — use carefully

Only do this if the element is guaranteed to be unique on the page.  
If the class might appear on multiple elements, `querySelector` returns only the first.

```js
// BEFORE
const nav = document.getElementById('main-nav');

// AFTER — safe only if .main-nav appears exactly once per page
const nav = document.querySelector('.main-nav');

// SAFER for collections
const navItems = document.querySelectorAll('.main-nav__item');
```

---

## 7. Comment Convention

Use these standard comment tags consistently across HTML and CSS:

### HTML

```html
<!-- [JS] #{id} → {function/file that uses it} -->
<!-- [A11Y] #{id} → bound to {label/aria attribute} -->
<!-- [ANCHOR] #{id} → used as href="#..." in {location} -->
```

### CSS

```css
/* [JS] .{class} mirrors #{id} — do not rename without updating {file.js} */
/* [A11Y] .{class} — structural; id kept on element for {reason} */
```

### Examples

```html
<!-- [JS] #modal-overlay → toggleModal() in modal.js -->
<div id="modal-overlay" class="modal-overlay"></div>

<!-- [A11Y] #search-input → bound to <label for="search-input"> -->
<input id="search-input" class="search__input" type="search">
```

```css
/* [JS] .modal-overlay mirrors #modal-overlay — do not rename without updating modal.js */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 0.5);
}
```

---

## 8. Specificity Traps & How to Avoid Them

### The core math

```
#id       →  specificity (0, 1, 0, 0)   =  100
.class    →  specificity (0, 0, 1, 0)   =  10
element   →  specificity (0, 0, 0, 1)   =  1
```

When you replace `#id` with `.class`, specificity **drops by 90 points**.  
Any existing rule that was previously losing to the id will now win — **potentially breaking layout.**

### How to detect this before it breaks production

```bash
# Find every CSS rule that targets both a class and the ID you're replacing
grep -n '\.some-class' styles.css   # check for rules that may now override yours
```

### Common trap — third-party overrides

```css
/* A library adds this — it was always losing to your #id rule. After refactor it wins. */
.some-class { color: red !important; }   /* previously overridden by #id, now it wins */
```

**Fix:** Increase your selector specificity just enough:

```css
/* Option 1 — add element type */
header.site-header { … }

/* Option 2 — add a parent context */
.page-wrapper .site-header { … }

/* Option 3 — only if necessary, never preferred */
.site-header.site-header { … }   /* doubles specificity cleanly, no !important */
```

**Never use `!important` to compensate for lost specificity** — it creates the same problem one level up.

---

## 9. IDs You Must Keep

Never remove these:

| Use Case | Example | Why |
|---|---|---|
| `<label for="">` binding | `<input id="email">` | Accessibility — clicking label focuses input |
| In-page anchor links | `<section id="contact">` | `href="#contact"` navigation breaks |
| `aria-labelledby` / `aria-describedby` | `<div id="tooltip-text">` | Screen readers rely on this |
| `aria-controls` | `<div id="menu">` | ARIA widget pattern |
| JS that you choose not to migrate yet | `<div id="app">` | Don't change JS and HTML in the same commit |

You can add a class **alongside** these ids for styling, but the id stays.

---

## 10. Automated Helpers

### VSCode — multi-file rename

1. `Ctrl+Shift+H` (Find & Replace in files)
2. Search: `id="main-nav"` → Replace: `id="main-nav" class="main-nav"`
3. Repeat for CSS: `#main-nav` → `.main-nav`

Use **regex mode** for bulk patterns:

```
Search:  id="([a-z-]+)"
Replace: id="$1" class="$1"
```

> This adds a matching class to every id — useful for Category C elements.  
> Then manually remove the id from Category A elements.

### ESLint (to prevent future id-for-styling)

```json
{
  "rules": {
    "no-restricted-syntax": [
      "warn",
      {
        "selector": "CallExpression[callee.property.name='getElementById']",
        "message": "Prefer querySelector('[data-*]') over getElementById for new code."
      }
    ]
  }
}
```

### Stylelint — ban id selectors in CSS

```json
{
  "rules": {
    "selector-id-pattern": null,
    "selector-max-id": [0, { "message": "Use classes for styling, not IDs." }]
  }
}
```

---

## 11. QA Checklist

Run through this after every component refactor, not just at the end.

### Visual

- [ ] No layout shifts compared to baseline screenshots
- [ ] Hover / focus / active states still work
- [ ] Responsive breakpoints unchanged
- [ ] Animations / transitions intact

### Functional

- [ ] All JS event listeners fire correctly
- [ ] Form submissions work
- [ ] Modal open / close / focus-trap works
- [ ] Dropdowns, accordions, tabs — all toggle correctly
- [ ] In-page anchor links (`href="#section"`) scroll correctly

### Accessibility

- [ ] `<label for="">` still focuses the correct input
- [ ] Screen reader announces correct labels (test with VoiceOver / NVDA)
- [ ] `aria-controls`, `aria-labelledby`, `aria-describedby` still resolve

### Code hygiene

- [ ] No orphaned `#id` selectors left in CSS
- [ ] No `getElementById` pointing to a removed id
- [ ] All `[JS]` and `[A11Y]` comments are in place
- [ ] Stylelint and ESLint pass with zero new errors

---

## 12. Real-World Example — Before & After

### Before

**HTML**
```html
<header id="site-header">
  <nav id="main-nav">
    <ul>
      <li><a href="#about" id="nav-about">About</a></li>
    </ul>
  </nav>
  <button id="menu-toggle">☰</button>
</header>

<section id="about">
  <h2>About Us</h2>
</section>
```

**CSS**
```css
#site-header {
  position: sticky;
  top: 0;
  background: #1a1a2e;
}

#main-nav {
  display: flex;
  gap: 1rem;
}

#menu-toggle {
  display: none;
  background: transparent;
  border: none;
}

@media (max-width: 768px) {
  #menu-toggle { display: block; }
  #main-nav    { display: none; }
  #main-nav.open { display: flex; flex-direction: column; }
}
```

**JavaScript**
```js
const toggle = document.getElementById('menu-toggle');
const nav    = document.getElementById('main-nav');

toggle.addEventListener('click', () => {
  nav.classList.toggle('open');
});
```

---

### After

**HTML**
```html
<!-- [JS] #site-header → stickyHeader() in header.js -->
<header id="site-header" class="site-header">

  <!-- [JS] #main-nav → menuToggle() in header.js -->
  <nav id="main-nav" class="main-nav">
    <ul>
      <!-- [ANCHOR] #about → href="#about" below -->
      <li><a href="#about" class="nav__link">About</a></li>
    </ul>
  </nav>

  <!-- [JS] #menu-toggle → menuToggle() in header.js -->
  <button id="menu-toggle" class="menu-toggle">☰</button>

</header>

<!-- [ANCHOR] #about → linked from nav above -->
<section id="about" class="about-section">
  <h2>About Us</h2>
</section>
```

**CSS**
```css
/* [JS] .site-header mirrors #site-header — do not rename without updating header.js */
.site-header {
  position: sticky;
  top: 0;
  background: #1a1a2e;
}

.main-nav {
  display: flex;
  gap: 1rem;
}

.menu-toggle {
  display: none;
  background: transparent;
  border: none;
}

@media (max-width: 768px) {
  .menu-toggle { display: block; }
  .main-nav    { display: none; }
  .main-nav.open { display: flex; flex-direction: column; }
}
```

**JavaScript** *(unchanged — ids still present in HTML)*
```js
// No changes needed in this pass.
// JS still targets ids; ids are still in the HTML.
// Migrate to data-attributes in a separate follow-up commit if desired.
const toggle = document.getElementById('menu-toggle');
const nav    = document.getElementById('main-nav');

toggle.addEventListener('click', () => {
  nav.classList.toggle('open');   // .open class — already was a class, stays a class
});
```

---

## Summary — The Three Rules

1. **IDs for identity, classes for styling.** If an ID serves both roles today, add a class and keep the ID.
2. **Change HTML and CSS together, JS separately.** Never leave CSS selectors pointing at removed IDs, but don't touch JS in the same commit.
3. **Comment every ID that JS or accessibility depends on** — in both HTML and CSS — so the next developer knows it's load-bearing.
