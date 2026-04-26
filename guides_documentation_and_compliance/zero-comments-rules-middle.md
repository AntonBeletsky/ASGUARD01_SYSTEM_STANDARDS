# Zero-Level Documentation Standards — Middle Grade
### One comment per logical unit. No walls. No silence.

> **Research basis:** Envato/ThemeForest author requirements, idiomatic-css (necolas),
> CSS Guidelines (cssguidelin.es), Google JavaScript Style Guide, JSDoc 3 standard,
> WordPress Coding Standards (CSS + JS), and the internal full/lite guides.

---

## 1. Core Principle

**Comment density = one block per logical unit.**

A "logical unit" is any named section, component, class, public method, or non-obvious
pattern. Everything inside that unit that is self-explanatory gets no comment.
Everything that isn't obvious gets one inline note — one line, one sentence.

```
                   ┌─────────────────────────────────────────────┐
  zero-comments    │  Comments only on tricky inline lines        │  ← too sparse
  -lite.md         │  Large sections uncommented                  │
                   └─────────────────────────────────────────────┘

                   ┌─────────────────────────────────────────────┐
  THIS GUIDE  →    │  Header block per section / component        │  ← target
                   │  JSDoc per public method                     │
                   │  One-line "why" on non-obvious properties    │
                   └─────────────────────────────────────────────┘

                   ┌─────────────────────────────────────────────┐
  zero-comments    │  Multi-line block per individual property    │  ← too dense
  -rules.md        │  Paragraph explanations everywhere           │
                   └─────────────────────────────────────────────┘
```

---

## 2. Comment Decision Tree

Before writing any comment, run this check:

```
Is this a section / component boundary?
  └─ YES → Write a section header (see §6)

Is this a class or public method?
  └─ YES → Write a JSDoc block (see §3.1 – 3.2)

Is the code self-evident from its name and structure?
  └─ YES → Write nothing

Does this line use a non-obvious pattern, browser workaround,
performance tradeoff, or security measure?
  └─ YES → Write one inline comment explaining WHY (not WHAT)

Everything else → no comment needed
```

---

## 3. JavaScript

### 3.1 Class Header (JSDoc)

Every class gets a single JSDoc block. Max 3 lines of description.
Include `@param` only for constructor arguments that are not obvious from the name.

```js
/**
 * Controls tab navigation and URL-hash-based deep linking for the account page.
 * Replaces default Bootstrap tab behavior to support direct URL access and
 * browser back/forward navigation.
 *
 * @param {string} selector - CSS selector for the root container element.
 */
class AccountPageController {
```

---

### 3.2 Public Methods (JSDoc)

Public methods that form the component's API get a JSDoc block.
One-sentence description + `@param` / `@returns` only when the types or purpose
are not obvious from the name.

```js
/**
 * Activates the tab matching the given id and updates the URL hash.
 *
 * @param {string} tabId - Must match the `id` of a `.tab-pane` element.
 */
navigate(tabId) {

/**
 * Removes all event listeners and resets component state.
 * Call this before removing the component from the DOM.
 */
destroy() {
```

Private and internal helper methods get **no JSDoc** — use a single `//` line
only if the logic is non-obvious.

```js
// Normalize the hash value: strip leading "#" and decode URI encoding.
_parseHash(raw) {
```

---

### 3.3 Section Headers

Every logical block inside a class gets a section header. No description needed —
the header name is enough. Use the dash-bar format for visual scanning.

```js
class AccountPageController {

  // ─── STATIC CONFIGURATION ────────────────────────────────────────────
  // ─── CONSTRUCTOR ─────────────────────────────────────────────────────
  // ─── PRIVATE STATE ───────────────────────────────────────────────────
  // ─── EVENT BINDING ───────────────────────────────────────────────────
  // ─── ROUTING ─────────────────────────────────────────────────────────
  // ─── RENDERING ───────────────────────────────────────────────────────
  // ─── PUBLIC API ──────────────────────────────────────────────────────
  // ─── TEARDOWN ────────────────────────────────────────────────────────
}
```

---

### 3.4 Inline "Why" Comments

One line only. Explains the architectural decision, not the syntax.

```js
// ─── STATIC CONFIGURATION ────────────────────────────────────────────

// Guards against Prototype Pollution when merging external data objects.
static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);


// ─── CONSTRUCTOR ─────────────────────────────────────────────────────

// AbortController lets all listeners be removed in one call during teardown.
this._ac = new AbortController();

const sig = { signal: this._ac.signal };

// ─── EVENT BINDING ───────────────────────────────────────────────────

// Event Delegation: one listener on the parent handles all current and future items.
this._list.addEventListener('click', this._onItemClick.bind(this));

// Scoped to this._root so identical components on the same page don't interfere.
this._q = (sel) => this._root.querySelector(sel);

// ─── ROUTING ─────────────────────────────────────────────────────────

// Reacts to browser back/forward navigation via the URL hash.
window.addEventListener('hashchange', () => this._handleHash(), sig);

// ─── TEARDOWN ────────────────────────────────────────────────────────

// Calling abort() removes every listener registered with this._ac.signal.
this._ac.abort();
```

---

### 3.5 Component Entry Point

```js
// Initialize once the DOM is ready.
document.addEventListener('DOMContentLoaded', () => {
  new AccountPageController('.account-page-container');
});
```

---

### 3.6 What Gets No Comment

```js
this._activeTab = null;            // ← obvious from name
this._root = document.querySelector(selector);   // ← obvious
el.classList.add('is-active');     // ← self-evident
return this._activeTab;            // ← trivial getter body
```

---

## 4. CSS

### 4.1 File Header

Every CSS file starts with a one-block header: what this file covers and any
dependency notes.

```css
/**
 * Account Page — Layout and component styles.
 * Depends on: bootstrap.min.css (grid, utilities), tokens.css (CSS variables).
 * Custom properties defined in :root below override Bootstrap defaults.
 */
```

---

### 4.2 Section Headers

Use the same dash-bar format as JS. Every major section gets one.
Standard order for a page-level stylesheet:

```css
/* ─── THEME TOKENS ──────────────────────────────────────────────────── */
/* ─── RESET & BASE ──────────────────────────────────────────────────── */
/* ─── LAYOUT ────────────────────────────────────────────────────────── */
/* ─── COMPONENT: SIDEBAR ────────────────────────────────────────────── */
/* ─── COMPONENT: TAB NAVIGATION ─────────────────────────────────────── */
/* ─── COMPONENT: MODAL ──────────────────────────────────────────────── */
/* ─── RESPONSIVE: TABLET (max 1199px) ───────────────────────────────── */
/* ─── RESPONSIVE: MOBILE (max 767px) ────────────────────────────────── */
/* ─── ACCESSIBILITY ─────────────────────────────────────────────────── */
/* ─── PRINT ─────────────────────────────────────────────────────────── */
```

---

### 4.3 Component Block Header

Each component section starts with a two-line block: what it is and one key
behavioral note (if any). Skip the note line if there's nothing to say.

```css
/* ─── COMPONENT: SIDEBAR ────────────────────────────────────────────── */
/* Vertical navigation panel. Switches to a horizontal scroll layout
   on mobile — see the Responsive section below. */

.sidebar { ... }
.sidebar__nav { ... }
```

```css
/* ─── THEME TOKENS ──────────────────────────────────────────────────── */
/* Override these variables in your own stylesheet to retheme the entire
   component. All color values in this file reference these tokens. */

:root {
  --primary:   #4F46E5;
  --surface:   #FFFFFF;
  --text:      #1C1C1E;
  --radius-md: 8px;
}
```

---

### 4.4 Inline Property Notes

Use inline comments only for non-obvious values or intentional overrides.
Keep to the end of the line or the line above — never a paragraph.

```css
.sidebar {
  position: sticky;
  top: 72px;                 /* Offset clears the fixed top navigation bar. */
  overflow-y: auto;
  scrollbar-width: thin;     /* Firefox only; Chrome uses ::-webkit-scrollbar below. */
}

/* ─── Z-INDEX STACK ─────────────────────────────────────────────────── */
/* Layering order (low → high): backdrop → modal → tooltip.
   Matches Bootstrap defaults so third-party overlays stay in context. */
.modal-backdrop { z-index: 1040; }
.modal          { z-index: 1050; }
.tooltip        { z-index: 1070; }
```

---

### 4.5 Responsive Blocks

State *what changes* and *at what breakpoint* in the section header.
No need to repeat it on every rule inside.

```css
/* ─── RESPONSIVE: MOBILE (max 767px) ────────────────────────────────── */
/* Sidebar collapses into a swipeable horizontal scroll nav. */

@media (max-width: 767.98px) {
  .sidebar {
    position: static;
    flex-direction: row;
    overflow-x: auto;
    overflow-y: hidden;
  }
}
```

---

### 4.6 Accessibility Block

```css
/* ─── ACCESSIBILITY ─────────────────────────────────────────────────── */
/* Disables animations for users with the OS reduced-motion preference.
   Follows WCAG 2.1 guideline 2.3.3. */

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

### 4.7 What Gets No Comment

```css
.btn { display: inline-flex; }      /* ← obvious */
.is-hidden { display: none; }       /* ← obvious */
h1, h2, h3 { line-height: 1.2; }   /* ← obvious */
```

---

## 5. HTML

### 5.1 Root Container

One comment per component root. Covers: what it is, how JS finds it,
and any routing or behavioral note that affects the whole component.

```html
<!--
  Customer Account Page — root element.
  Hooked by AccountPageController via the .account-page-container class.
  Uses a custom JS router (not Bootstrap tabs) so tabs are reachable via URL hash.
-->
<div class="account-page-container">
```

---

### 5.2 Major Layout Regions

Comment only the outermost wrapper of each region — not every div inside.

```html
<!-- Sidebar navigation — becomes a horizontal scroll strip on mobile. -->
<aside class="sidebar">

<!-- Main content area — tab panels are rendered here by AccountPageController. -->
<main class="content-area">

<!-- Sticky action bar — always visible at the bottom on mobile viewports. -->
<div class="action-bar">
```

---

### 5.3 data-* Attributes as Public API

When a component reads `data-*` attributes as configuration, document them
on the element that owns them — one line per attribute.

```html
<!--
  Navigation trigger.
  data-target: id of the .tab-pane this button activates (must match exactly).
  data-track:  optional analytics event label sent on click.
-->
<button class="nav-btn" data-target="overview" data-track="tab_overview">
  Overview
</button>
```

---

### 5.4 ARIA Attributes Toggled by JS

If JS toggles an ARIA attribute, say so — otherwise the static value looks like a bug.

```html
<!--
  aria-expanded is toggled to "true"/"false" by SidebarController on open/close.
  aria-controls links this button to the panel it reveals for screen readers.
-->
<button class="sidebar-toggle"
        aria-expanded="false"
        aria-controls="sidebar-panel">
  Menu
</button>
```

---

### 5.5 Third-Party Embed Wrappers

```html
<!-- Stripe payment form mount point — content is injected by Stripe.js. -->
<div id="stripe-card-element"></div>
```

---

### 5.6 What Gets No Comment

```html
<header class="site-header">       <!-- ← obvious -->
<footer class="site-footer">       <!-- ← obvious -->
<ul class="nav-list">              <!-- ← obvious -->
<p class="hero__subtitle">         <!-- ← obvious -->
```

---

## 6. Section Header Format Reference

Consistent across JS, CSS, and HTML (adapted per syntax).

### JavaScript
```js
// ─── SECTION NAME ──────────────────────────────────────────────────── //
```
*(trailing `//` optional — use it only if your editor highlights it better)*

### CSS
```css
/* ─── SECTION NAME ────────────────────────────────────────────────── */
```

### HTML
```html
<!-- ═══ SECTION NAME ════════════════════════════════════════════════ -->
```
*(Use `═` only for top-level page regions in large HTML files — not inside components)*

**Minimum line length:** fill to column ~72 so headers stand out on scroll.
**Casing:** ALL CAPS for section names, Title Case for component names after the colon.

---

## 7. Comment Density Summary

| Location | Comment type | Required? |
|---|---|---|
| JS class | JSDoc block (1–3 lines + `@param`) | Always |
| JS public method | JSDoc block (1 line + `@param`/`@returns` if non-obvious) | Always |
| JS private method | `//` one line — only if logic is non-obvious | When non-obvious |
| JS section boundary | `// ─── NAME ───` header | Always |
| JS non-obvious line | `//` inline "why" | When non-obvious |
| CSS file | File header block | Always |
| CSS section boundary | `/* ─── NAME ─── */` header | Always |
| CSS component block | 1–2 line description block | Always |
| CSS non-obvious property | Inline `/* why */` | When non-obvious |
| HTML component root | 1–3 line description block | Always |
| HTML major layout region | 1-line description | Always |
| HTML data-* config | One line per attribute | When non-obvious |
| HTML ARIA toggled by JS | 1–2 line note | Always |

---

## 8. Pre-Release Checklist

### Remove
- [ ] `§` symbols and internal rule numbers
- [ ] Names like `Law Zero`, `containerization-N`, `hook-protocol`
- [ ] Changelog language: `updated`, `fixed`, `v2.1`, `TEMP`, `refactored`
- [ ] Internal TODOs: `// TODO: refactor this`, `// FIXME: workaround`
- [ ] Sequential numbering: `// 1.`, `// Step 3`
- [ ] Comments that paraphrase the code (`// loop through items`)

### Verify
- [ ] Every class has a JSDoc block
- [ ] Every public method has a JSDoc block
- [ ] Every section boundary has a header
- [ ] Every component root in HTML has a description block
- [ ] Inline "why" comments use industry terms (Memory Safety, Event Delegation, etc.)
- [ ] The word `Bootstrap` refers only to the CSS framework — never to initialization
- [ ] All `data-*` attributes that JS reads are documented on their element
- [ ] All ARIA attributes toggled by JS have a note explaining the JS behavior
- [ ] No comment block exceeds 3 lines (except class-level JSDoc)

### The Test

> You are a junior developer. You bought the template.
> You open an unfamiliar file and read only the comments — not the code.
>
> **Can you answer these?**
> 1. What does this component/section do?
> 2. Why was this pattern used?
> 3. Where do I change X?
>
> If the answer to any question is *no* — add or rewrite the comment.
> If the comment answers none of them — delete it.

---

## 9. Quick Reference

```
ALWAYS COMMENT                          NEVER COMMENT
──────────────────────────────────      ──────────────────────────────────
Class and public method headers         Self-evident variable names
Section / component boundaries          Trivial getters and setters
Component root elements in HTML         Obvious loop bodies
Non-obvious patterns (why, not what)    Standard HTML structure elements
data-* attributes read by JS            Code that reads like plain English
ARIA attributes toggled by JS           Internal rules or version history
```

---

*"One comment per logical unit. Written for the buyer, not the author. Explains why, not what."*
