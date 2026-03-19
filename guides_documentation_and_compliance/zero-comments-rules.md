# Code Comments: The Complete Guide
### Write comments like a product, not like a dev log

---

## The Core Idea

Comments are part of your product's interface. The person reading them is not you — it's a developer who bought your template, cloned your library, or joined your team cold. They have zero context about your internal decisions, your tooling, your naming conventions, or your history.

**Every comment must answer one of these questions:**
- What does this block do?
- Why was this decision made?
- How do I customize this for my needs?

If a comment doesn't answer at least one of those — delete it.

---

## Part 1 — The Three Types of Garbage Comments

### 1.1 Numbered Comments and Internal References

AI tools and developers under deadline pressure tend to leave things like this:

```js
// 1. Updated modal logic
// 2. Fixed padding issue
// 3. Refactored per Law Zero §4.7

// Bootstrap — CSS class selector, one line (§6.1)
document.addEventListener('DOMContentLoaded', () => { ... });
```

**Why this is bad:** The buyer opens the file and sees `§4.7`, `Law Zero`, `containerization-8`. They have no idea what any of it means. It looks like leftover noise from someone else's system. Trust in the product drops immediately.

---

### 1.2 Changelog Comments

Git exists for history. Comments are not a changelog.

```js
// v2.1 — added animation support
// v2.3 — fixed Safari bug
// TODO: refactor this mess
// TEMP: workaround until API is fixed
// Updated: 2024-03-15 — changed to flex layout
// Removed old jQuery version
```

**Why this is bad:** "TODO: refactor this mess" tells the buyer the code is unfinished. "TEMP workaround" raises the question: *is this safe to ship?* These comments create anxiety, not value.

---

### 1.3 Captain Obvious Comments

The most common type of useless comment — paraphrasing the code in plain English.

```js
// Loop through items
for (let i = 0; i < items.length; i++) {

  // Check if item is active
  if (items[i].active) {

    // Add to result array
    result.push(items[i]);
  }
}
```

**Why this is bad:** The code already says this. These comments add zero value and drown out the comments that actually matter.

---

## Part 2 — The Philosophy

| ❌ Comment for the developer | ✅ Comment for the buyer |
|---|---|
| Describes the development process | Explains the architectural decision |
| Contains internal references | Uses standard industry terms |
| Records who changed what and when | Explains *why*, not *who* |
| Paraphrases the code | Helps with customization |
| Tracks version history | Describes the current product state |

> **The test:** *"If a junior developer bought this template, opened the file, and read this comment — would they understand what it does, why it's built this way, and how to change it?"*
>
> If the answer is no — rewrite the comment.

---

## Part 3 — The Ten Rules

**Rule 1 — No internal references**
No `§` symbols, no rule numbers, no internal protocol names, no guide titles. The buyer doesn't know them and never will.

**Rule 2 — No changelog in comments**
No `updated`, `fixed`, `v2.1`, `removed`, `added`. That's what Git is for. Code is read in its current state, not its history.

**Rule 3 — No sequential numbering**
Don't number comments `// 1.`, `// 2.`, `// Step 3`. If sequence matters, use section headers or JSDoc.

**Rule 4 — Don't paraphrase the code**
If the comment repeats what the code already says — delete it. A comment is only needed when it adds something the code cannot express on its own.

**Rule 5 — Explain WHY, not WHAT**
*What* is visible in the code. *Why* is invisible. Explain the architectural choice, the browser limitation, the performance tradeoff, the security requirement.

**Rule 6 — Use industry-standard terms**
Memory Safety, Event Delegation, Prototype Pollution, Deep Linking, Lazy Loading, Race Condition — these are words the buyer knows. Use them.

**Rule 7 — Watch out for words with double meanings**
`Bootstrap` is a UI framework, not an init process. `Hook` could mean a React Hook or an HTML attribute. `Signal` could mean an AbortSignal or a reactive primitive. When in doubt, add context.

**Rule 8 — Section headers are for navigation**
Use block dividers like `// ─── EVENT BINDING ───` to structure large files. They let the buyer jump to what they need without reading everything.

**Rule 9 — Don't comment the obvious**
`const MAX = 100` doesn't need `// Maximum value`. Comment only where there's a non-obvious choice or an important constraint.

**Rule 10 — TODOs must be buyer-facing**
If you leave a TODO, it must be useful to the buyer: `// TODO: Replace with your own API endpoint`. Internal TODOs (`// TODO: refactor this`) must be removed before shipping.

---

## Part 4 — JavaScript Patterns

### 4.1 Component Initialization

The word `Bootstrap` means the CSS framework Bootstrap. Never use it to describe a script's startup process.

```js
// ❌ BAD
// Bootstrap — CSS class selector, one line, no logic (§6.1)
document.addEventListener('DOMContentLoaded', () => {
  new OverviewController('.overview-container');
});

// ✅ GOOD
// Initialize the controller once the DOM is ready.
document.addEventListener('DOMContentLoaded', () => {
  new OverviewController('.overview-container');
});
```

---

### 4.2 AbortController and Memory Management

Explain *why* the AbortController exists — this is a non-obvious pattern for many developers.

```js
// ❌ BAD
// AbortController — declared after state, before _bind (§4.7.1)
this._ac = new AbortController();

// Global hashchange — signal is critical here (§4.7.5)
window.addEventListener('hashchange', () => this._handleHash(), {
  signal: this._ac.signal
});

// ✅ GOOD
// AbortController used to cleanly remove all event listeners
// when the component is destroyed — call this._ac.abort() in teardown.
this._ac = new AbortController();

// Passing the signal ties this listener to the controller.
// When abort() is called, the listener is automatically removed
// without needing to keep a reference to the handler function.
window.addEventListener('hashchange', () => this._handleHash(), {
  signal: this._ac.signal
});
```

---

### 4.3 Prototype Pollution Prevention

This is a non-obvious security pattern. Explain what it protects against and why.

```js
// ❌ BAD
// ─── 0. STATIC CONFIG ────────────────────────────
// Forbidden keys list (§3.2)
static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);

// ✅ GOOD
// ─── STATIC CONFIGURATION ────────────────────────
// Sanitize external data objects to prevent Prototype Pollution:
// these keys, if merged into a plain object, would let an attacker
// inject properties onto the global Object prototype.
static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);
```

---

### 4.4 Custom Router Overriding Framework Defaults

If you're overriding Bootstrap or another framework's default behavior — explain it in industry terms.

```js
// ❌ BAD
// Overriding href because hook via data-target is required by Law Zero
el.addEventListener('click', (e) => {
  e.preventDefault();
  this._router.navigate(el.dataset.target);
});

// ✅ GOOD
// Using a custom Vanilla JS router instead of default Bootstrap tab behavior
// to support Deep Linking: tabs are directly accessible via URL hash,
// enabling browser back/forward navigation and shareable URLs.
el.addEventListener('click', (e) => {
  e.preventDefault();
  this._router.navigate(el.dataset.target);
});
```

---

### 4.5 Event Delegation

Explain the performance decision and its reason.

```js
// ❌ BAD
// Attach to parent (updated v2.3)
this._list.addEventListener('click', this._onItemClick.bind(this));

// ✅ GOOD
// Event Delegation: the listener is on the parent container, not on each item.
// This handles dynamically added items without rebinding,
// and prevents memory leaks from an unbounded number of listeners.
this._list.addEventListener('click', this._onItemClick.bind(this));
```

---

### 4.6 Scoped DOM Queries

Explain why queries are scoped to a container instead of hitting the whole document.

```js
// ❌ BAD
// Scoped helper (containerization-8 §4.3)
_find(selector) {
  return this._root.querySelector(selector);
}

// ✅ GOOD
// Scoped DOM query helper — restricts all queries to this component's
// root element to avoid conflicts with other components on the same page.
_find(selector) {
  return this._root.querySelector(selector);
}
```

---

### 4.7 Teardown / Destroy

Always comment the teardown method so the buyer knows how to clean up.

```js
// ❌ BAD
destroy() {
  this._ac.abort(); // cleanup
}

// ✅ GOOD
// Tears down the component: aborts all event listeners registered
// via this._ac.signal. Call this before removing the element from the DOM
// to prevent memory leaks.
destroy() {
  this._ac.abort();
}
```

---

## Part 5 — CSS Patterns

### 5.1 Media Queries

Explain what happens to the layout — not just "mobile".

```css
/* ❌ BAD */
/* Mobile sidebar fix (v1.4) */
@media (max-width: 991.98px) {
  .sidebar { flex-direction: row; overflow-x: auto; }
}

/* ✅ GOOD */
/* Responsive Layout: Mobile Navigation */
/* Converts the vertical sidebar into a swipeable horizontal scroll nav
   on screens narrower than 992px (Bootstrap's lg breakpoint). */
@media (max-width: 991.98px) {
  .sidebar { flex-direction: row; overflow-x: auto; }
}
```

---

### 5.2 Accessibility — Reduced Motion

```css
/* ❌ BAD */
/* Accessibility: Reduced Motion (shared elements) */
/* (Must not use !important per §3.7) */
@media (prefers-reduced-motion: reduce) {
  * { animation: none; transition: none; }
}

/* ✅ GOOD */
/* Accessibility: Reduced Motion */
/* Disables animations for users who have enabled the reduced motion
   preference in their OS accessibility settings.
   Follows WCAG 2.1 guideline 2.3.3 (Animation from Interactions). */
@media (prefers-reduced-motion: reduce) {
  * { animation: none; transition: none; }
}
```

---

### 5.3 CSS Custom Properties (Theme Tokens)

Explain that these are intentionally overridable — that's the whole point.

```css
/* ❌ BAD */
/* Theme colors — 1 */
:root {
  --primary: #4F46E5;
  --surface: #FFFFFF;
  --text: #1C1C1E;
}

/* ✅ GOOD */
/* ─── THEME TOKENS ──────────────────────────────────────────── */
/* Override these variables in your own stylesheet to retheme the
   entire component without touching any component-level CSS.
   All colors in this file reference these tokens — never raw hex values. */
:root {
  --primary: #4F46E5;
  --surface: #FFFFFF;
  --text: #1C1C1E;
}
```

---

### 5.4 z-index Stack

Arbitrary z-index values are confusing without context. Document the stacking order.

```css
/* ❌ BAD */
.modal-backdrop { z-index: 1040; } /* bootstrap z */
.modal          { z-index: 1050; }
.tooltip        { z-index: 1070; }

/* ✅ GOOD */
/* ─── Z-INDEX STACK ─────────────────────────────────────────── */
/* Layering order (low → high): backdrop → modal → tooltip.
   Values match Bootstrap's defaults so third-party components
   stay in the expected stacking context. */
.modal-backdrop { z-index: 1040; }
.modal          { z-index: 1050; }
.tooltip        { z-index: 1070; }
```

---

## Part 6 — HTML Patterns

### 6.1 Root Container

Explain how JS finds the component and why a class is used instead of an id.

```html
<!-- ❌ BAD -->
<!--
  Account Page — root container.
  Scoped by AccountPageController (.account-page-container selector).
  No id on this element — JS finds it by CSS class (containerization-8 §6.1).
-->
<div class="account-page-container">

<!-- ✅ GOOD -->
<!--
  Customer Account Layout
  Root element for AccountPageController.
  Uses a CSS class (not an id) so multiple instances can coexist on a page.
  This component uses a custom JS router instead of default Bootstrap tab
  behavior to support Deep Linking: tabs are accessible via URL hash.
-->
<div class="account-page-container">
```

---

### 6.2 data-attributes as Public API

`data-*` attributes are the component's public API. Document what each one does.

```html
<!-- ❌ BAD -->
<!-- nav item, law-zero hook -->
<button class="nav-btn" data-target="overview">Overview</button>

<!-- ✅ GOOD -->
<!--
  Navigation trigger.
  data-target: the id of the section this button activates.
  Must match the id attribute of the corresponding .tab-pane element.
-->
<button class="nav-btn" data-target="overview">Overview</button>
```

---

### 6.3 ARIA Attributes

Document *why* specific ARIA attributes are present — especially when they're toggled by JS.

```html
<!-- ❌ BAD -->
<button aria-expanded="false" aria-controls="menu-1">Menu</button>

<!-- ✅ GOOD -->
<!--
  aria-expanded is toggled by MenuController on open/close.
  aria-controls links this button to the menu panel it controls,
  enabling screen readers to announce the relationship.
-->
<button aria-expanded="false" aria-controls="menu-1">Menu</button>
```

---

## Part 7 — Section Headers

For large files, use block dividers. They replace a table of contents and let the buyer jump to what they need.

### JavaScript Standard

```js
class ModalController {

  // ─── STATIC CONFIGURATION ─────────────────────────────────────────
  // ...

  // ─── CONSTRUCTOR ──────────────────────────────────────────────────
  // ...

  // ─── PRIVATE STATE ────────────────────────────────────────────────
  // ...

  // ─── EVENT BINDING ────────────────────────────────────────────────
  // ...

  // ─── RENDERING ────────────────────────────────────────────────────
  // ...

  // ─── PUBLIC API ───────────────────────────────────────────────────
  // ...

  // ─── TEARDOWN ─────────────────────────────────────────────────────
  // ...
}
```

### CSS Standard

```css
/* ─── RESET & BASE ───────────────────────────────────────────────── */
/* ─── THEME TOKENS ───────────────────────────────────────────────── */
/* ─── LAYOUT ─────────────────────────────────────────────────────── */
/* ─── COMPONENT: SIDEBAR ─────────────────────────────────────────── */
/* ─── COMPONENT: MODAL ───────────────────────────────────────────── */
/* ─── RESPONSIVE LAYOUT: TABLET ──────────────────────────────────── */
/* ─── RESPONSIVE LAYOUT: MOBILE ──────────────────────────────────── */
/* ─── ACCESSIBILITY ──────────────────────────────────────────────── */
/* ─── PRINT ──────────────────────────────────────────────────────── */
```

---

## Part 8 — Pre-Release Checklist

Go through every file with this list before publishing.

### What to remove

- [ ] All `§` symbols and rule numbers
- [ ] Internal system names: `Law Zero`, `containerization-N`, `hook-protocol`, etc.
- [ ] Changelog language: `updated`, `fixed`, `refactored`, `removed`, `added`
- [ ] Version markers: `v1.2`, `v2.3 —`, `since v1`
- [ ] Dated edits: `2024-03-15`, `March update`
- [ ] Internal TODOs: `// TODO: refactor`, `// FIXME: temp workaround`
- [ ] Sequential numbering: `// 1.`, `// Step 2.`, `// 3.`
- [ ] Captain Obvious comments that paraphrase the code

### What to verify

- [ ] Does the word `Bootstrap` refer only to the CSS framework, never to initialization?
- [ ] Is every `signal`, `hook`, or `target` reference unambiguous without internal knowledge?
- [ ] Do all remaining TODOs explain what the *buyer* needs to do?
- [ ] Do files longer than ~100 lines have section headers?
- [ ] Is every non-obvious architectural choice explained with an industry-standard term?

### The final test

> Imagine you're a junior developer. You bought the template, opened an unfamiliar file, and started reading the comments.
>
> **Can you answer these three questions?**
> 1. What does this block of code do?
> 2. Why was it built this way?
> 3. How do I change it to fit my needs?
>
> If the answer to any of them is *no* — rewrite the comment.

---

## Part 9 — Terminology Reference

| Instead of this | Write this | Why |
|---|---|---|
| `Bootstrap` (init) | `Initialize` / `Set up` | Bootstrap is a CSS framework name |
| `signal critical (§4.7.5)` | `Memory Safety` / `clean teardown` | Explains the real problem |
| `hook via data-target` | `Deep Linking via URL hash` | Standard routing pattern |
| `containerization-8` | `Scoped DOM selector` | Understandable without context |
| `Law Zero override` | `Custom Vanilla JS router` | Describes the actual solution |
| `§6.1 class selector` | `CSS class-based component binding` | Standard practice, readable |
| `FORBIDDEN_KEYS (§3.2)` | `Prototype Pollution prevention` | Known security vulnerability name |
| `_ac teardown` | `AbortController for memory safety` | Standard Web API pattern |
| `shared elements` | `applies to all animated elements` | Describes scope, not internals |
| `updated v2.3` | *(delete it)* | Git is the history, not comments |

---

## Quick Reference Card

```
ALWAYS                              NEVER
──────────────────────────────      ──────────────────────────────
Explain WHY a decision was made     Reference internal rules or §
Use industry-standard terms         Number your comments 1, 2, 3
Document the public API             Write changelog in comments
Describe customization points       Paraphrase what the code says
Write for a buyer, not yourself     Leave internal TODOs in
Add section headers to large files  Use "Bootstrap" for init logic
Keep TODOs buyer-facing             Leave version history inline
```

---

*"Code is read once when written. Comments are read every time someone needs to change something. Write them for a person, not for a log."*
