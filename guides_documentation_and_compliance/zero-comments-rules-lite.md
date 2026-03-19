# Zero-Level Documentation Standards (Client-Facing Comments)

## 1. Core Philosophy

**"Zero-Level Documentation"** means that the code itself, augmented by its comments, is the primary and only documentation the buyer needs to understand, customize, and extend the template. 

Comments in the codebase must be written for the **end-buyer** (a third-party developer). They must **never** contain our internal studio jargon, protocol names, or development rules. The buyer does not know what "containerization-8" or "Law Zero" means. To them, it's just a well-architected HTML/CSS/JS template.

---

## 2. The Golden Rules

### 2.1. No Internal Jargon
Never reference internal documentation, guides, or rules.
- ❌ **BAD:** `// Scoped helper according to containerization-8 §4.3`
- ✅ **GOOD:** `// Scoped DOM selector utility to restrict queries to this component's tree`

### 2.2. Clarify Custom Mechanics over Frameworks
If we use Vanilla JS to override or enhance a framework (like Bootstrap), explain *why* we are doing it in standard web development terms.
- ❌ **BAD:** `// Overriding href because hook via data-target is required by Law Zero`
- ✅ **GOOD:** `// Using a custom Vanilla JS router instead of default Bootstrap behavior to support Deep Linking via URL hash.`

### 2.3. Explain "Why" and the "Value"
Help the buyer understand the architectural decisions. Use industry-standard terms like "Memory Safety", "Prototype Pollution", or "Event Delegation".
- ❌ **BAD:** `// signal is critical here (§4.7.5)`
- ✅ **GOOD:** `// Tie all event listeners to the AbortController's signal for memory safety and clean teardown.`

### 2.4. Avoid Ambiguous Terminology
Be careful with industry words that have double meanings in our context. For example, "Bootstrap" is a UI framework, so do not use it to describe the "bootstrapping" (initialization) process of a script.
- ❌ **BAD:** `// Bootstrap — CSS class selector, one line`
- ✅ **GOOD:** `// Initialize the component once the DOM is ready`

---

## 3. Implementation Examples

### 3.1. JavaScript

**❌ Internal/Development State:**
```javascript
// ─── 0. STATIC CONFIG ────────────────────────────────────────
static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);

// AbortController — declared after state, before _bind (§4.7.1)
this._ac = new AbortController();

// Global hashchange — signal is critical here (§4.7.5)
window.addEventListener('hashchange', () => this._handleHash(), sig);

// Bootstrap — CSS class selector, one line, no logic (§6.1)
document.addEventListener('DOMContentLoaded', () => {
    new OverviewController('.overview-container');
});
```

**✅ Zero-Level Documentation (Client-Facing):**
```javascript
// ─── STATIC CONFIGURATION ────────────────────────────────────────
// Utility to sanitize external data objects, preventing prototype pollution
static FORBIDDEN_KEYS = Object.freeze(['__proto__', 'constructor', 'prototype']);

// AbortController used to cleanly remove event listeners during teardown
this._ac = new AbortController();

// Listen for browser URL hash changes (back/forward button compatibility)
window.addEventListener('hashchange', () => this._handleHash(), sig);

// Initialize the controller once the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new OverviewController('.overview-container');
});
```

### 3.2. HTML

**❌ Internal/Development State:**
```html
<!--
    Account Page — root container.
    Scoped by AccountPageController (.account-page-container selector).
    No id on this element — JS finds it by CSS class (containerization-8 §6.1).
-->
```

**✅ Zero-Level Documentation (Client-Facing):**
```html
<!--
    Customer Account Layout
    The root element is hooked by AccountPageController via the .account-page-container class.
    This component uses a custom JavaScript routing approach rather than default Bootstrap behavior 
    to support Deep Linking (direct access to tabs via URL hash).
-->
```

### 3.3. CSS

**❌ Internal/Development State:**
```css
/* --- Mobile: Sidebar Becomes Horizontal Scroll Nav --- */
@media (max-width: 991.98px) { ... }

/* --- Accessibility: Reduced Motion (shared elements) --- */
/* (Must not use !important per §3.7) */
```

**✅ Zero-Level Documentation (Client-Facing):**
```css
/* --- Responsive Layout: Mobile Navigation --- */
/* Converts the vertical sidebar into a swipeable horizontal layout on mobile screens */
@media (max-width: 991.98px) { ... }

/* --- Accessibility Enhancements --- */
/* Disables sweeping animations for users preferring reduced motion */
```

---

## 4. Checklist for Review

When preparing a file for production/sale, ask yourself:
1. Are there any `§` symbols or rule numbers? *(Must be 0)*
2. Are there any mentions of `containerization`, `Law Zero`, or other internal guidelines? *(Must be 0)*
3. If I am a Junior Developer buying this template, do these comments help me understand how to modify the widget? *(Must be Yes)*
4. Are structural blocks clearly defined? *(e.g., `// ─── EVENT BINDING ───`)*
