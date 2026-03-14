# Good Code Style Methodology
### A Complete Guide to Production-Grade Vanilla HTML/CSS/JS

> Derived from real-world analysis of three production-quality UI modules:  
> a Correspondence widget, an Orders tracker, and a Wishlist manager.  
> Every rule here is grounded in concrete code evidence, not abstract theory.

---

## Table of Contents

1. [Philosophy](#1-philosophy)
2. [File & Module Structure](#2-file--module-structure)
3. [CSS Architecture](#3-css-architecture)
4. [Design Tokens (CSS Custom Properties)](#4-design-tokens-css-custom-properties)
5. [HTML Authoring](#5-html-authoring)
6. [JavaScript Class Design](#6-javascript-class-design)
7. [State Management](#7-state-management)
8. [DOM References & Queries](#8-dom-references--queries)
9. [Event Handling](#9-event-handling)
10. [Rendering Strategy](#10-rendering-strategy)
11. [Security](#11-security)
12. [Accessibility (A11Y)](#12-accessibility-a11y)
13. [Performance](#13-performance)
14. [Animation](#14-animation)
15. [Responsive Design](#15-responsive-design)
16. [Component Lifecycle](#16-component-lifecycle)
17. [Data Validation](#17-data-validation)
18. [Code Documentation](#18-code-documentation)
19. [Framework Integration Discipline (Bootstrap)](#19-framework-integration-discipline-bootstrap)
20. [Naming Conventions](#20-naming-conventions)
21. [Anti-Patterns to Avoid](#21-anti-patterns-to-avoid)
22. [Quick Reference Checklist](#22-quick-reference-checklist)

---

## 1. Philosophy

Before any rule, understand the four pillars this methodology rests on:

**Isolation** — A module must never leak styles or behavior into the rest of the page. Everything is scoped. A stranger can drop your component anywhere and it will not break their page or be broken by it.

**Explicit over implicit** — Contracts between layers (CSS ↔ JS, state ↔ DOM) are documented inline, not assumed. A developer reading only the CSS file can still understand which elements JavaScript will touch.

**UI derives from state, never from DOM** — The DOM is an output, not a source of truth. Never read state back from the DOM. Write state, then re-render.

**Minimum effective code** — Use the framework (Bootstrap, etc.) for everything it can do. Write custom code only where the framework genuinely cannot cover it, and document why.

---

## 2. File & Module Structure

### 2.1 Single-file self-contained modules

Each UI widget lives in one file: styles in `<style>`, markup in `<body>`, logic in `<script>`. This makes the component portable and reviewable without chasing imports.

```html
<head>
  <!-- External dependencies (CDN with SRI hashes) -->
  <link href="bootstrap.min.css" rel="stylesheet"
    integrity="sha384-..." crossorigin="anonymous" />

  <style>
    /* All custom styles for this module only */
  </style>
</head>

<body>
  <!-- Markup for this module -->

  <script>
    'use strict';
    /* All logic for this module */
  </script>
</body>
```

### 2.2 Always declare `'use strict'`

Place `'use strict'` at the top of every `<script>` block. It eliminates silent errors and enforces cleaner variable scoping.

### 2.3 CSS Table of Contents

Every stylesheet section begins with a numbered Table of Contents comment. A reader can scan the entire CSS in seconds.

```css
/* ============================================================
   MESSAGE MODULE — Custom Styles

   TABLE OF CONTENTS
   0. Tokens (CSS custom properties)
   1. Module layout
   2. Sidebar
   3. Message stream
   4. Message bubbles
   5. Typing indicator
   6. Input textarea
   7. Animations (@keyframes)
   8. Mobile overrides
   ============================================================ */
```

Each section is then separated by a matching header comment:

```css
/* --- 3. Message stream ---
 * flex: 1 1 0 + min-height: 0: standard pattern for a scrollable flex child.
 * Without min-height: 0 the item won't shrink past its content size. */
```

This is not decorative — the comment explains *why* the rule exists, not just *what* it does.

---

## 3. CSS Architecture

### 3.1 Scope everything under a root container class

Never write a bare selector like `.sidebar` or `.card`. Always prefix with the module's root class.

```css
/* ✗ Bad — will collide with anything on the page named .sidebar */
.sidebar { ... }

/* ✓ Good — collision-safe, grep-able, instantly identifies the module */
.messages-container .msg-sidebar { ... }
.orders-container .order-card { ... }
.wishlist-view .wishlist-view--card { ... }
```

This pattern gives you BEM-level isolation without BEM's verbose syntax, because the root class acts as a namespace.

### 3.2 Prefix all module classes

Every class that belongs to a module carries a short prefix: `msg-`, `ord-`, `wl-`. This makes global search reliable and collisions impossible.

```css
/* Prefix pattern */
.msg-bubble { }      /* messaging module */
.ord-filter-scroll { } /* orders module */
.wl-grid-col-min { }   /* wishlist module */
```

### 3.3 Custom CSS only where Bootstrap (or your framework) cannot

If Bootstrap has a utility for it, use that utility. If not, write a custom rule and leave a comment explaining why Bootstrap cannot handle it.

```css
/* max-width as percentage on inline flex children — no Bootstrap utility exists */
.messages-container .msg-msg {
  max-width: 88%;
}

/* auto-fill grid columns — Bootstrap's col-* grid cannot replicate this without JS */
.wishlist-container.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--wl-grid-col-min), 1fr));
}
```

Without this discipline, custom CSS bloats uncontrollably.

### 3.4 `data-state` attributes for CSS state hooks

Use `data-state` attributes to drive visual state changes via CSS attribute selectors, instead of toggling modifier classes.

```css
/* ✓ Reads like a state machine */
.msg-seller-item[data-state="active"] {
  border-left: 3px solid var(--msg-active-accent);
}
.msg-seller-item:not([data-state="active"]) {
  border-left: 3px solid transparent;
}
```

```js
// JS writes state, CSS reads it
el.dataset.state = isActive ? 'active' : '';
```

This separates concerns cleanly: CSS handles appearance, JS handles state transitions.

### 3.5 Never use `!important` except for hard overrides at media query boundaries

`!important` is acceptable in exactly one case: when overriding a utility that was set for a lower breakpoint and must be reversed at a higher one.

```css
/* Restoring card border-radius on desktop that was set to 0 for mobile */
@media (min-width: 768px) {
  .messages-container {
    border-radius: var(--bs-card-border-radius) !important;
  }
}
```

Document it. Undocumented `!important` is a code smell.

---

## 4. Design Tokens (CSS Custom Properties)

### 4.1 Define all configurable values as tokens on the root element

Every "magic number" that could ever need customization goes into a CSS custom property scoped to the module root.

```css
.messages-container {
  --msg-bubble-radius: 0.75rem;
  --msg-bubble-sent-bg: var(--bs-primary);
  --msg-bubble-sent-color: #fff;
  --msg-bubble-recv-bg: var(--bs-body-secondary);
  --msg-bubble-recv-color: var(--bs-body-color);
  --msg-sidebar-width: 33.333%;
  --msg-active-accent: var(--bs-primary);
  --msg-input-max-height: 96px;
  --msg-anim-duration: 120ms;
}
```

### 4.2 Consumers override tokens, not internals

This is the key benefit: an external team can restyle your entire component by overriding tokens, without touching internal CSS rules and without needing `!important`.

```css
/* External override — one block, zero !important */
.messages-container {
  --msg-bubble-sent-bg: #6f42c1;
  --msg-anim-duration: 200ms;
}
```

### 4.3 Tokens reference framework variables where possible

```css
--msg-bubble-sent-bg: var(--bs-primary);    /* inherits Bootstrap theme */
--msg-bubble-recv-bg: var(--bs-body-secondary); /* adapts to dark mode automatically */
```

This means your component gets dark mode support for free, without a single `@media (prefers-color-scheme)` rule.

### 4.4 Read tokens from JS when needed

```js
// Read the CSS token at runtime — single source of truth
const maxH = parseInt(
  getComputedStyle(this._root).getPropertyValue('--msg-input-max-height'), 10
) || 96;
```

Never hardcode a value in JS that already lives in CSS as a token.

---

## 5. HTML Authoring

### 5.1 The `[JS]` annotation convention

Every HTML element that JavaScript will reference or mutate gets a `[JS]` comment above it describing what JS will do to it. This is the most unusual and most valuable practice in this codebase.

```html
<!-- [JS] .messages-container
     · this._root = querySelector('.messages-container')  — constructor entry point
     · classList.add('msg-mob-chat')                      — _select() on mobile
     · classList.remove('msg-mob-chat')                   — back-btn handler -->
<section class="messages-container ...">
```

```html
<!-- [JS] [data-ref=thread-count]
     · this._threadCount.textContent = '${n} threads'  — _syncThreadCount() -->
<span class="badge" data-ref="thread-count" aria-live="polite">0 threads</span>
```

The format is consistent: `[JS]` tag → selector → `·` per operation → method name.

### 5.2 `data-ref` for JS bindings, classes for styles

Classes belong to CSS. `data-ref` attributes belong to JavaScript. They are never interchangeable.

```html
<!-- CSS targets .msg-messages for layout -->
<!-- JS targets [data-ref="messages"] for DOM manipulation -->
<div data-ref="messages" class="msg-messages p-3 d-flex flex-column gap-2">
```

**Why?** Renaming a CSS class never breaks JS. Restructuring JS never changes visual styling. The layers are fully decoupled.

### 5.3 `data-action` for event targets

Elements that trigger actions carry `data-action` attributes. A single delegated listener on the root handles all actions via a `switch`.

```html
<button data-ref="send-btn" data-action="send">Send</button>
<button data-ref="back-btn" data-action="back">← Back</button>
```

```js
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  switch (btn.dataset.action) {
    case 'send': this._send(); break;
    case 'back': this._handleBack(); break;
  }
}, sig);
```

### 5.4 `data-id` for record identifiers

Data identifiers that drive business logic are stored in `data-id`, separate from `data-ref` (DOM reference) and `data-state` (visual state) and `data-action` (event target).

```html
<li data-id="seller-5" data-ref="seller-item" data-state="active">
```

Each `data-*` attribute has one job. Never overload a single attribute to carry multiple meanings.

### 5.5 Inline comments describe layout intent

HTML structural comments are not filler. They explain the layout decision:

```html
<!-- MODULE BODY: two-column flex layout -->
<div class="card-body p-0 row g-0 overflow-hidden flex-grow-1">

  <!-- LEFT COLUMN: Seller list
       [CSS] .msg-sidebar — hidden when .msg-mob-chat on root (mobile chat view) -->
  <nav class="msg-sidebar col-12 col-md-4 ...">
```

A developer reading the HTML knows immediately: this is a two-column layout, the left column is a nav, and its visibility is controlled by a CSS class on the root.

---

## 6. JavaScript Class Design

### 6.1 One class per module

Each widget is one ES6 class. The class encapsulates all state, all DOM references, and all behavior for that widget.

```js
class MessagesController { ... }
class OrdersController { ... }
class WishlistController { ... }
```

### 6.2 Constructor is the wiring step only

The constructor does four things: guard against missing root, cache DOM references, set initial state, and bind events. It does not render business UI — that happens in dedicated `_render*()` methods called from the constructor.

```js
constructor(selector, opts = {}) {
  // 1. Guard
  this._root = document.querySelector(selector);
  if (!this._root) return;

  // 2. Scoped DOM helpers
  const $ = sel => this._root.querySelector(sel);

  // 3. Cache refs
  this._list    = $('[data-ref="seller-list"]');
  this._input   = $('[data-ref="input"]');
  this._sendBtn = $('[data-ref="send-btn"]');
  // ...

  // 4. State
  this._state = { threads, activeId: null, msgs: {}, typing: false };

  // 5. AbortController for cleanup
  this._ac = new AbortController();

  // 6. Initial render + event binding
  this._renderSidebar();
  this._bindEvents();
  this._syncThreadCount();
}
```

### 6.3 Static configuration lives in static class properties

All configuration constants are declared as static class properties, not scattered as `const` variables.

```js
class MessagesController {
  static DELAY_MS          = 900;
  static PREVIEW_MAX_CHARS = 60;
  static FORBIDDEN_KEYS    = ['__proto__', 'constructor', 'prototype'];

  static STATUS_CFG = {
    processing: { badge: 'text-bg-info',    label: 'Processing' },
    shipped:    { badge: 'text-bg-warning',  label: 'Shipped'    },
    delivered:  { badge: 'text-bg-success',  label: 'Delivered'  },
    cancelled:  { badge: 'text-bg-danger',   label: 'Cancelled'  },
  };
}
```

Advantages: discoverable, overridable by subclasses, namespaced to the class, not polluting the module scope.

### 6.4 All instance methods are private by convention

Methods that are not part of the public API are prefixed with `_`. The public API is minimal: `constructor`, `destroy`, and whatever the consumer needs to call.

```js
// Public API
constructor(selector, opts) { ... }
destroy() { ... }

// Private implementation
_renderSidebar() { ... }
_renderMessages() { ... }
_bubble(msg) { ... }
_select(threadId) { ... }
_send() { ... }
_bindEvents() { ... }
_handleBack() { ... }
_scrollBottom() { ... }
_syncThreadCount() { ... }
_cut(s, maxLen) { ... }
_esc(s) { ... }
```

### 6.5 Guard at the top, not at the bottom

Every method that could be called with invalid input guards at the very first line:

```js
_select(threadId) {
  const thread = this._state.threads.find(t => t.id === threadId);
  if (!thread) return;  // ← guard: bail immediately on invalid input
  // ... rest of method
}

_send() {
  const text = this._input.value.trim();
  if (!text || !this._state.activeId || this._state.typing) return; // ← multi-condition guard
  // ...
}
```

This keeps the happy path unindented and readable.

---

## 7. State Management

### 7.1 Single source of truth

All mutable state lives in `this._state`. The DOM is always derived from state, never the other way around.

```js
this._state = {
  threads,              // original data
  activeId: null,       // which thread is selected
  msgs: {},             // mutable message history per thread
  typing: false,        // is the bot currently "typing"?
};
```

### 7.2 Update state first, then update the DOM

```js
// ✓ Correct order
this._state.msgs[id].push(msg);           // 1. State update
this._messages.appendChild(this._bubble(msg)); // 2. DOM update
```

If you need to debug or serialize state, it is always accurate. The DOM is just a view.

### 7.3 Derive, don't duplicate

UI labels, badge classes, and display text are derived from state at render time, not stored separately.

```js
// Derive from state.status at render time
const cfg = OrdersController.STATUS_CFG[order.status]
         || { badge: 'text-bg-secondary', label: order.status };
```

Never store `badgeClass` or `displayLabel` in state — they are derivable and would create synchronization bugs.

---

## 8. DOM References & Queries

### 8.1 Scoped query helpers, declared once

At the top of the constructor, create scoped `$` and `$$` helpers:

```js
const $ = sel => this._root.querySelector(sel);
const $$ = sel => [...this._root.querySelectorAll(sel)];
```

Every query in the class runs through these helpers. There is never a `document.querySelector` anywhere — that would break isolation.

### 8.2 Cache all refs in the constructor

Every element the class will touch is cached in `this._*` during construction. No repeated DOM queries inside render loops or event handlers.

```js
// Cache once
this._list        = $('[data-ref="seller-list"]');
this._messages    = $('[data-ref="messages"]');
this._input       = $('[data-ref="input"]');
this._sendBtn     = $('[data-ref="send-btn"]');
this._backBtn     = $('[data-ref="back-btn"]');
this._empty       = $('[data-ref="empty"]');
this._sellerName  = $('[data-ref="seller-name"]');
this._orderId     = $('[data-ref="order-id"]');
this._statusBadge = $('[data-ref="status-badge"]');
this._threadCount = $('[data-ref="thread-count"]');
```

### 8.3 `getElementById` only for ARIA relationships

`getElementById` is reserved for elements that need a globally unique ID for ARIA purposes (e.g., `aria-activedescendant`, `aria-labelledby`). Everything else uses `data-ref`.

```js
// Only appropriate use of getElementById — resolving ARIA relationship
const li = document.getElementById(`msg-seller-item-${threadId}`);
```

---

## 9. Event Handling

### 9.1 Delegated listeners on stable parents

Never attach click listeners to dynamically created elements. Attach one delegated listener to the nearest stable ancestor and use `closest()` to identify the target.

```js
// One listener on the root covers all [data-action] elements,
// including ones created dynamically after init.
this._root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  switch (btn.dataset.action) {
    case 'send': this._send(); break;
    case 'back': this._handleBack(); break;
  }
}, sig);
```

### 9.2 AbortController for clean listener removal

Register all listeners with the same `AbortSignal`. Cleanup becomes one line.

```js
// Construction
this._ac = new AbortController();
const sig = { signal: this._ac.signal };

this._root.addEventListener('click', handler, sig);
this._list.addEventListener('keydown', handler, sig);
this._input.addEventListener('input', handler, sig);

// Destruction — removes every listener registered with this signal
destroy() {
  this._ac.abort();
}
```

Never maintain an array of `[element, event, handler]` tuples for manual cleanup.

### 9.3 Keyboard navigation follows ARIA patterns

Keyboard handling is implemented according to the WAI-ARIA Authoring Practices Guide. The pattern is cited in the comment.

```js
// ARIA Listbox pattern: https://www.w3.org/WAI/ARIA/apg/patterns/listbox/
this._list.addEventListener('keydown', e => {
  const items = [...this._list.querySelectorAll('[data-id]')];
  const cur = document.activeElement.closest('[data-id]');
  const idx = items.indexOf(cur);

  switch (e.key) {
    case 'ArrowDown': e.preventDefault(); items[Math.min(idx + 1, items.length - 1)]?.focus(); break;
    case 'ArrowUp':   e.preventDefault(); items[Math.max(idx - 1, 0)]?.focus(); break;
    case 'Home':      e.preventDefault(); items[0]?.focus(); break;
    case 'End':       e.preventDefault(); items[items.length - 1]?.focus(); break;
    case 'Enter':
    case ' ':         e.preventDefault(); if (cur) this._select(cur.dataset.id); break;
  }
}, sig);
```

Always `e.preventDefault()` for handled keyboard events to prevent browser defaults (scrolling on arrow keys, page scroll on space).

### 9.4 Modifier keys are explicit

```js
// Enter sends. Shift+Enter inserts newline. Explicit, readable.
this._input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this._send(); }
}, sig);
```

Never check `e.keyCode` — use `e.key`.

---

## 10. Rendering Strategy

### 10.1 Full rebuild vs. surgical update — choose consciously

Full rebuild (`innerHTML = ''` → re-render) is used for initial render and for state changes that affect many elements. Surgical update (`textContent = ...` on a single element) is used for small, frequent changes.

Always document the choice:

```js
/**
 * Updates only the preview span of a single sidebar item.
 * Used after bot reply to avoid a full _renderSidebar() rebuild.
 */
_updateSidebarItem(threadId) {
  const previewEl = li.querySelector('[data-ref="preview"]');
  if (previewEl) previewEl.textContent = preview; // textContent: plain text, no HTML
}
```

### 10.2 `textContent` for user content, `innerHTML` for structural HTML only

This is a security rule as much as a style rule (see Security section). But as a rendering rule: if a value is a plain string from user input or data, always use `textContent`. Only use `innerHTML` to inject structural HTML that you control.

```js
// ✓ User-provided text — always textContent
bbl.textContent = text;

// ✓ Structured template with escaped data — innerHTML is acceptable
li.innerHTML = `
  <span class="fw-semibold">${this._esc(t.sellerName)}</span>
  <span class="badge">${t.resolved ? '&#10004; resolved' : '&#9679; open'}</span>
`;
```

### 10.3 Preserve elements across full rebuilds

Elements that should survive a re-render (like an "empty state" placeholder) are preserved by moving them, not recreating them.

```js
_renderMessages() {
  this._messages.innerHTML = '';

  if (!activeId) {
    this._empty.style.display = '';         // restore visibility
    this._messages.appendChild(this._empty); // move, not recreate
    return;
  }
  this._empty.style.display = 'none';       // hide during active thread
  // ... render messages
}
```

### 10.4 String-based templates for repeated list items

When rendering lists via innerHTML, use template literals with escaped values. Keep the HTML in one readable block:

```js
return `
  <div class="stepper-step ${this._esc(cls)}">
    <div class="stepper-dot">${iconHtml}</div>
    <div class="stepper-label fw-semibold">${this._esc(s.label)}</div>
    <div class="stepper-date text-secondary">${s.date ? this._esc(this._fmtShort(s.date)) : ''}</div>
  </div>`;
```

Align indentation to the HTML structure. Escape every dynamic value.

---

## 11. Security

### 11.1 Escape all 7 OWASP characters before `innerHTML`

Any user-supplied or external data going into `innerHTML` must be escaped. The canonical escape function covers all 7 OWASP-recommended characters:

```js
_esc(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')   // FIRST — prevents double-escaping
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')  // closes </script> tags inside attributes
    .replace(/`/g, '&#x60;'); // closes template literals inside attributes
}
```

`&` must be replaced first. Replacing it last would double-escape already-escaped sequences.

### 11.2 User message text always uses `textContent`

For message bubble content — the highest-risk injection vector — use `textContent` unconditionally, with no escaping needed:

```js
// SECURITY: plain text — any HTML in `text` renders as literal characters
bbl.textContent = text;
```

### 11.3 Mark security decisions in comments

```js
// SECURITY: textContent — plain text only, no HTML structure needed
const previewEl = li.querySelector('[data-ref="preview"]');
if (previewEl) previewEl.textContent = preview;
```

```html
<!-- SECURITY: metadata inserted via innerHTML only after _esc() -->
li.innerHTML = `<span>${this._esc(t.sellerName)}</span>`;
```

Security comments are not optional. They prove the decision was deliberate, and they remind future editors to maintain the pattern.

### 11.4 Validate external data against prototype pollution

Any data passed in from outside (API responses, consumer options) must be validated before use:

```js
static FORBIDDEN_KEYS = ['__proto__', 'constructor', 'prototype'];

static _validateThread(thread) {
  const forbidden = MessagesController.FORBIDDEN_KEYS;
  if (Object.keys(thread).some(k => forbidden.includes(k))) return false;
  if (Array.isArray(thread.messages)) {
    for (const msg of thread.messages) {
      if (Object.keys(msg).some(k => forbidden.includes(k))) return false;
    }
  }
  return true;
}

// In constructor — filter before use
const threads = raw.filter(t => MessagesController._validateThread(t));
```

### 11.5 Use CDN integrity hashes (SRI)

External resources loaded from CDN carry Subresource Integrity hashes:

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
  rel="stylesheet"
  integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
  crossorigin="anonymous" />
```

This prevents supply-chain attacks where a CDN is compromised.

---

## 12. Accessibility (A11Y)

### 12.1 ARIA roles on all interactive containers

Every interactive region carries an explicit ARIA role and label:

```html
<ul role="listbox" aria-label="Select a seller conversation" aria-activedescendant="">
<li role="option" aria-selected="false" tabindex="0">
<div role="log" aria-live="polite" aria-atomic="false" aria-label="Message history">
<div role="region" aria-label="Chat messages">
```

### 12.2 Dynamic content uses `aria-live`

Any region where content updates without a page reload declares how screen readers should handle it:

```html
<!-- Thread count badge: polite = announced after current speech finishes -->
<span aria-live="polite" data-ref="thread-count">0 threads</span>

<!-- Message log: polite + atomic=false = each new message announced separately -->
<div role="log" aria-live="polite" aria-atomic="false">

<!-- Typing indicator: announced when it appears -->
<div aria-live="polite" aria-label="Seller is typing">
```

Use `aria-live="polite"` by default. Use `aria-live="assertive"` only for critical errors.

### 12.3 `aria-activedescendant` tracks focus in composite widgets

In a listbox pattern, the `aria-activedescendant` on the container points to the active item's ID:

```js
// Sync after selection
this._list.setAttribute('aria-activedescendant', `msg-seller-item-${threadId}`);

// Clear on back navigation
this._list.setAttribute('aria-activedescendant', '');
```

### 12.4 `aria-selected` mirrors visual state

```js
this._list.querySelectorAll('[role=option]').forEach(el => {
  const isThis = el.dataset.id === threadId;
  el.setAttribute('aria-selected', String(isThis)); // must be string "true"/"false"
  el.dataset.state = isThis ? 'active' : '';
});
```

### 12.5 Message bubbles are individually labeled

```js
bbl.setAttribute('role', 'article');
bbl.setAttribute('aria-label', `${isSent ? 'You' : 'Seller'}: ${text}`);
```

A screen reader user navigating through messages hears "You: Hello" or "Seller: Hi there" for each bubble.

### 12.6 `focus-visible` for keyboard users only

```css
.order-toggle:focus-visible {
  outline: 2px solid var(--bs-primary);
  outline-offset: -2px;
}
```

Use `:focus-visible` (not `:focus`) so keyboard users see the outline but mouse users do not.

### 12.7 Restore focus after state transitions

After navigating back from a chat view to the sidebar:

```js
_handleBack() {
  // ...
  this._list.querySelector('[data-id]')?.focus(); // return focus to first list item
}
```

Never leave focus stranded on a hidden or removed element.

---

## 13. Performance

### 13.1 Cache DOM references — never query in loops

All DOM references are cached in the constructor. Render methods use the cached references:

```js
// ✓ Read from cache, not the DOM
this._messages.appendChild(this._bubble(msg));
this._messages.scrollTop = this._messages.scrollHeight;

// ✗ Never do this inside a render loop
document.querySelector('.msg-messages').appendChild(...);
```

### 13.2 Surgical updates over full rebuilds for small changes

```js
// ✓ Update one element after a bot reply
_updateSidebarItem(threadId) {
  const previewEl = li.querySelector('[data-ref="preview"]');
  if (previewEl) previewEl.textContent = preview;
}

// ✗ Never do a full sidebar rebuild for a single preview change
this._renderSidebar(); // rebuilds all N items when 1 changed
```

### 13.3 Animate with compositor-only properties

Only `opacity` and `transform` are guaranteed to stay on the GPU compositor thread. Any other animated property risks triggering layout and paint.

```css
/* ✓ compositor-only — no reflow, no repaint */
@keyframes msg-bubble-in {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ✓ removal animation — same principle */
@keyframes wl-remove {
  to { opacity: 0; transform: translateX(-8px); }
}
```

### 13.4 Double `requestAnimationFrame` for forced paint triggers

When triggering a CSS transition on an element that was just added to the DOM, the browser may batch the addition and the style change together, preventing the transition from firing. Use double `rAF` to ensure the browser has committed a paint before the style change:

```js
_animateFill(orderId) {
  const fill = this.container.querySelector(`#fill-${orderId}`);
  if (!fill) return;
  const pct = parseFloat(fill.dataset.pct || 0);
  requestAnimationFrame(() =>
    requestAnimationFrame(() => {
      fill.style.width = pct + '%'; // triggers CSS transition after 2 frames
    })
  );
}
```

### 13.5 Debounce or guard repeated actions

```js
_send() {
  // Guard prevents duplicate sends while bot is typing
  if (!text || !this._state.activeId || this._state.typing) return;
  // ...
}
```

### 13.6 Hide scroll chrome on filter bars

Horizontal filter scroll areas hide the scrollbar for a cleaner look without losing scroll functionality:

```css
.ord-filter-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;          /* Firefox */
  -ms-overflow-style: none;       /* IE/Edge */
}
.ord-filter-scroll::-webkit-scrollbar {
  display: none;                  /* Chrome/Safari */
}
```

---

## 14. Animation

### 14.1 Entrance animations are class-driven

Add an animation class to every newly appended element. The animation fires automatically on insertion:

```css
.wishlist-container .wishlist-view--card {
  animation: wl-appear 0.2s ease both;
}
```

No JS required to trigger — just append the element with the class already present.

### 14.2 Exit animations with `forwards` fill and then DOM removal

```css
@keyframes wl-remove {
  to { opacity: 0; transform: translateX(-8px); }
}
.wishlist-container .wishlist-view--card.removing {
  animation: wl-remove .35s ease forwards; /* forwards: hold final state */
}
```

```js
card.classList.add('removing');
card.addEventListener('animationend', () => card.remove(), { once: true });
```

The `{ once: true }` ensures the handler auto-removes after firing.

### 14.3 Staggered animations via `animation-delay`

```css
.msg-dot:nth-child(1) { animation-delay: 0s; }
.msg-dot:nth-child(2) { animation-delay: .2s; }
.msg-dot:nth-child(3) { animation-delay: .4s; }
```

### 14.4 Keyframe names carry the module prefix

Keyframe names are global. Prefix them like classes:

```css
@keyframes msg-bubble-in { ... }   /* not "bubbleIn" */
@keyframes msg-dot-bounce { ... }  /* not "bounce" */
@keyframes wl-remove { ... }
@keyframes wl-appear { ... }
```

### 14.5 Animation duration in tokens

```css
.messages-container {
  --msg-anim-duration: 120ms;
}

.messages-container .msg-msg-anim {
  animation: msg-bubble-in var(--msg-anim-duration) ease both;
}
```

Consumers can slow down or disable animations by overriding the token.

---

## 15. Responsive Design

### 15.1 Mobile-first, breakpoint-up

Base styles target mobile. Enhancements are added at `min-width` breakpoints:

```css
/* Base (mobile): edge-to-edge, full viewport */
.messages-container {
  height: 100dvh;
}

/* Desktop enhancement */
@media (min-width: 768px) {
  .messages-container {
    height: calc(100vh - 2rem);
    min-height: 400px;
    border-radius: var(--bs-card-border-radius) !important;
  }
}
```

### 15.2 Use `dvh` for mobile, `vh` for desktop

`100dvh` accounts for mobile browser chrome (address bar shrink/expand). `100vh` does not. Use `dvh` for full-screen elements on mobile:

```css
.messages-container {
  height: 100dvh;           /* mobile: handles address bar resize */
}
@media (min-width: 768px) {
  .messages-container {
    height: calc(100vh - 2rem); /* desktop: stable chrome, dvh not needed */
  }
}
```

### 15.3 Mobile panel switching via CSS class on root

On mobile, a class on the root element toggles which panel is visible. No JS `display` manipulation:

```css
@media (max-width: 767.98px) {
  /* Default: show sidebar, hide chat panel */
  .messages-container:not(.msg-mob-chat) .msg-panel {
    display: none !important;
  }
  /* After selection: hide sidebar, show chat panel */
  .messages-container.msg-mob-chat .msg-sidebar {
    display: none !important;
  }
}
```

```js
// JS only toggles the class; CSS handles the rest
this._root.classList.add('msg-mob-chat');
```

This means CSS has full control of the visual output. JS only manages the state flag.

### 15.4 CSS Grid auto-fill for adaptive layouts

```css
.wishlist-container.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--wl-grid-col-min), 1fr));
  gap: 12px;
}

/* Token adjusts column width on small phones without a new grid rule */
@media (max-width: 575px) {
  .wishlist-container.grid-view {
    grid-template-columns: repeat(auto-fill, minmax(var(--wl-grid-col-min-sm), 1fr));
  }
}
```

### 15.5 `min-height: 0` on flex scrollable children

A scrollable flex child requires `min-height: 0`. Without it, the item will not shrink past its content size and the scroll will never activate:

```css
.messages-container .msg-messages {
  overflow-y: auto;
  flex: 1 1 0;     /* flex-grow: 1, flex-shrink: 1, flex-basis: 0 */
  min-height: 0;   /* REQUIRED: allows shrinking below content size */
}
```

---

## 16. Component Lifecycle

### 16.1 Silent guard in constructor

If the root selector matches nothing, exit silently. The component is safe to include on any page even if its container is absent:

```js
constructor(selector, opts = {}) {
  this._root = document.querySelector(selector);
  if (!this._root) return; // selector not found — no-op, safe to include globally
  // ...
}
```

### 16.2 `destroy()` is mandatory on every class

Every class exposes a `destroy()` method that removes all event listeners and cleans up resources:

```js
destroy() {
  this._ac.abort(); // removes all listeners registered with this._ac.signal
}
```

Callers invoke it when the widget is unmounted, the user navigates away, or the container is removed from the DOM.

### 16.3 Initialize inside `DOMContentLoaded`

```js
document.addEventListener('DOMContentLoaded', () => {
  new MessagesController('.messages-container');
});
```

Never initialize before the DOM is ready.

### 16.4 Pass options as a single `opts` object with defaults

```js
constructor(selector, opts = {}) {
  this._delay = opts.delay ?? MessagesController.DELAY_MS;
  const raw = opts.threads ?? MessagesController.SEED_THREADS;
}
```

Never use positional parameters beyond the selector. An options object is extensible without breaking existing callers.

---

## 17. Data Validation

### 17.1 Validate all external input before it enters state

```js
const threads = raw.filter(t => MessagesController._validateThread(t));
```

Validation is a static method — it can be tested independently of the class instance.

### 17.2 `??` for defaults, not `||`

```js
// ✓ ?? — only falls through on null/undefined
this._delay = opts.delay ?? MessagesController.DELAY_MS;

// ✗ || — falls through on any falsy value (0, '', false)
this._delay = opts.delay || MessagesController.DELAY_MS;
```

`??` respects intentional `0` or `false` values from the consumer.

### 17.3 Configuration objects use lookup tables over switch/if-else chains

```js
// ✓ O(1) lookup, easily extensible, declarative
const cfg = OrdersController.STATUS_CFG[order.status]
         || { badge: 'text-bg-secondary', label: order.status };

// ✗ O(n) chain, fragile, hard to extend
if (status === 'processing') { badge = 'text-bg-info'; label = 'Processing'; }
else if (status === 'shipped') { ... }
```

---

## 18. Code Documentation

### 18.1 JSDoc on every public and notable private method

```js
/**
 * Creates and initialises the Correspondence Module.
 *
 * @param {string} selector - CSS selector of the root element.
 *                            If the selector matches nothing, exits silently.
 * @param {Object} [opts]
 * @param {Thread[]} [opts.threads] - Thread data. Defaults to MessagesController.SEED_THREADS.
 * @param {number}   [opts.delay]   - Bot response delay ms. Defaults to MessagesController.DELAY_MS.
 *
 * @example
 * new MessagesController('.messages-container');
 * new MessagesController('.messages-container', { threads: apiData, delay: 500 });
 */
constructor(selector, opts = {}) { ... }
```

```js
/**
 * Escapes all 7 OWASP-recommended HTML chars to prevent XSS via innerHTML.
 * & replaced first to avoid double-escaping.
 *
 * @param {string} s - Raw string to escape
 * @returns {string} HTML-safe string for innerHTML insertion
 * @private
 */
_esc(s) { ... }
```

### 18.2 Section dividers in long JS files

```js
/* ============================================================
   RENDER — SIDEBAR
   Full rebuild on init. After bot reply, _updateSidebarItem()
   refreshes only the affected preview span (avoids full rebuild).
   ============================================================ */
```

These banners act like chapter headings. A developer can scan a 1000-line file and jump to the right section in seconds.

### 18.3 `[JS]` cross-references in CSS comments

Every CSS rule that JavaScript interacts with is annotated with a `[JS]` comment describing the interaction. See Section 5.1 for the full pattern.

```css
/* [JS] .msg-seller-item — created in _renderSidebar(); data-state="active" toggled in _select()
 * Active item accent — no Bootstrap utility for conditional border-left */
.messages-container .msg-seller-item[data-state="active"] {
  border-left: 3px solid var(--msg-active-accent);
}
```

### 18.4 Cite specifications in keyboard handling

```js
/* ARIA Listbox keyboard nav
 * idx === -1 when focus is outside the list: ArrowDown lands on items[0] — intentional.
 * Spec: https://www.w3.org/WAI/ARIA/apg/patterns/listbox/ */
```

Linking to the spec is not boilerplate — it proves the implementation is correct and tells the next developer where to check.

### 18.5 Comment the non-obvious, not the obvious

```js
// ✓ Explains a subtle behavior
// guard: prevent duplicate indicators
this._removeTyping();

// ✓ Explains why a double rAF is necessary
requestAnimationFrame(() => requestAnimationFrame(() => { fill.style.width = pct + '%'; }));

// ✗ Explains something the code already says
// Set the value
this._input.value = '';
```

---

## 19. Framework Integration Discipline (Bootstrap)

### 19.1 Use Bootstrap utilities for spacing, color, flex, typography

```html
<!-- ✓ Bootstrap handles all of this -->
<div class="d-flex align-items-center gap-2 px-3 py-2 bg-body-secondary border-bottom">
  <span class="fw-semibold small text-truncate">Seller Name</span>
  <span class="badge text-bg-success flex-shrink-0">✔ Resolved</span>
</div>
```

### 19.2 Combine Bootstrap and BEM modifier classes intentionally

```js
bbl.className = [
  'msg-msg msg-msg-anim text-break',        // module class + animation class + Bootstrap utility
  'px-3 py-2 rounded-3 small',             // Bootstrap utilities
  isSent
    ? 'bg-primary text-white msg-msg--sent' // Bootstrap colour + BEM modifier for token hook
    : 'bg-body-secondary text-body msg-msg--recv',
].join(' ');
```

The BEM modifier (`msg-msg--sent`) exists solely to expose a CSS variable hook. Bootstrap provides the actual colour.

### 19.3 `currentColor` for theme-adaptive icons

```css
.msg-dot {
  background: currentColor; /* inherits text-secondary, adapts to light/dark theme */
}
```

Never hardcode a colour when `currentColor` will inherit the right value from Bootstrap's theme.

### 19.4 Bootstrap 5.2+ combined utilities

Prefer `text-bg-{color}` over separate `bg-{color} text-{color}` pairs. The combined utility handles text contrast automatically:

```js
// ✓ Bootstrap 5.2+: combined bg + accessible text colour
this._statusBadge.className = 'badge text-bg-success flex-shrink-0';

// ✗ Older pattern: manual contrast management
this._statusBadge.className = 'badge bg-success text-white flex-shrink-0';
```

---

## 20. Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Module root class | descriptive noun + `-container` or `-view` | `.messages-container`, `.wishlist-view` |
| Module CSS prefix | 2-4 char abbreviation + `-` | `msg-`, `ord-`, `wl-` |
| CSS state modifier | `--` suffix (BEM-ish) | `.msg-msg--sent`, `.stepper-step--done` |
| CSS token | `--{prefix}-{property}` | `--msg-bubble-radius`, `--wl-img-h` |
| JS DOM ref attribute | `data-ref="..."` | `data-ref="send-btn"` |
| JS action attribute | `data-action="..."` | `data-action="send"` |
| JS state attribute | `data-state="..."` | `data-state="active"` |
| JS record ID attribute | `data-id="..."` | `data-id="seller-5"` |
| JS instance property | `this._camelCase` | `this._sendBtn`, `this._state` |
| JS static config | `SCREAMING_SNAKE_CASE` | `DELAY_MS`, `FORBIDDEN_KEYS`, `STATUS_CFG` |
| JS private method | `_camelCase` | `_renderSidebar()`, `_bindEvents()` |
| Keyframe name | `{prefix}-{description}` | `msg-bubble-in`, `wl-remove` |
| Element ID for ARIA | `{prefix}-{element}-{id}` | `msg-seller-item-${t.id}` |
| CSS section comment | `/* --- N. Section Name --- */` | `/* --- 4. Message bubbles ---` |

---

## 21. Anti-Patterns to Avoid

### 21.1 Reading state from the DOM

```js
// ✗ Never read state back from the DOM
const isActive = li.classList.contains('active');

// ✓ Read from the state object
const isActive = t.id === this._state.activeId;
```

### 21.2 `document.querySelector` inside a class

```js
// ✗ Leaks outside the module scope
document.querySelector('.msg-messages').appendChild(bubble);

// ✓ Use the scoped helper or cached ref
this._messages.appendChild(bubble);
```

### 21.3 Inline styles for state-driven appearance

```js
// ✗ Mixing style into JS
el.style.borderLeft = '3px solid blue';

// ✓ Toggle a data attribute; let CSS handle the rest
el.dataset.state = 'active';
```

### 21.4 Hardcoding values that are in tokens

```js
// ✗ Hardcoded — won't respect the CSS token
const maxH = 96;

// ✓ Read from the token
const maxH = parseInt(
  getComputedStyle(this._root).getPropertyValue('--msg-input-max-height'), 10
) || 96;
```

### 21.5 Attaching listeners to dynamic elements

```js
// ✗ Listeners are lost when the element is removed and recreated
items.forEach(item => item.addEventListener('click', handler));

// ✓ Delegated listener on the stable parent
this._list.addEventListener('click', e => {
  const item = e.target.closest('[data-id]');
  if (item) this._select(item.dataset.id);
}, sig);
```

### 21.6 Leaving commented-out dead code in production

```css
/* ✗ Dead code with no explanation */
.order-card {
  /*border-radius: 12px;*/
  overflow: hidden;
}
.order-toggle:hover {
  /*background: var(--bs-gray-100);*/
}
```

Either delete it or replace it with a comment explaining why it was removed and when it might return.

### 21.7 Animating layout-triggering properties

```css
/* ✗ Triggers layout — expensive */
@keyframes bad {
  from { width: 0; height: 0; margin-top: 10px; }
}

/* ✓ Compositor-only — no layout, no paint */
@keyframes good {
  from { opacity: 0; transform: scale(0.95); }
}
```

---

## 22. Quick Reference Checklist

Use this before marking a component as done.

### CSS
- [ ] All selectors scoped under the module root class
- [ ] All module classes carry the module prefix
- [ ] CSS custom properties defined for all configurable values
- [ ] Custom rules only where the framework cannot cover it, with a comment explaining why
- [ ] `data-state` attributes used for CSS state hooks (not classes)
- [ ] `[JS]` annotations on all CSS rules touched by JavaScript
- [ ] CSS Table of Contents in the file header
- [ ] All `@keyframes` names carry the module prefix
- [ ] Animations use only `opacity` and `transform`
- [ ] `dvh` used for mobile full-screen heights, `vh` for desktop

### HTML
- [ ] `[JS]` comments above every JS-referenced element
- [ ] `data-ref` for JS bindings (not classes or IDs)
- [ ] `data-action` for event targets
- [ ] `data-id` for record identifiers
- [ ] `data-state` for visual state hooks
- [ ] ARIA roles and labels on all interactive elements
- [ ] `aria-live` regions for dynamic content
- [ ] SRI integrity hashes on all CDN resources

### JavaScript
- [ ] `'use strict'` at the top
- [ ] One class per module
- [ ] Constructor: guard → DOM helpers → cache refs → state → AbortController → render → bind
- [ ] All configurable values in static class properties
- [ ] `data-ref` used for DOM selection, not classes
- [ ] Delegated event listeners on stable parents
- [ ] All listeners registered with `AbortController` signal
- [ ] `destroy()` method implemented
- [ ] State updated before DOM
- [ ] DOM never read back for state
- [ ] `textContent` for user data, `innerHTML` only for structural HTML with escaped values
- [ ] `_esc()` called on every dynamic value in `innerHTML`
- [ ] `??` for defaults, not `||`
- [ ] Prototype pollution validation on external data
- [ ] `DOMContentLoaded` wrapping the initialization call
- [ ] JSDoc on all public methods and significant private methods
- [ ] Section divider comments separating logical groups
- [ ] ARIA keyboard patterns cited with spec URL

### Security
- [ ] All 7 OWASP characters escaped before `innerHTML`
- [ ] User input always via `textContent`
- [ ] External data validated against prototype pollution
- [ ] SRI hashes on CDN resources
- [ ] Security decisions annotated with `// SECURITY:` comments

### Accessibility
- [ ] All interactive elements keyboard-reachable (`tabindex="0"` or naturally focusable)
- [ ] `role` and `aria-label` on all composite widgets
- [ ] `aria-selected` synced with visual selection state
- [ ] `aria-activedescendant` updated on selection
- [ ] Focus restored after state transitions (back navigation, dialog close)
- [ ] `:focus-visible` used, not `:focus`
- [ ] `aria-live="polite"` on dynamic content regions

---

*This guide reflects the methodology as observed across the three source modules. The goal is not rules for their own sake, but code that any competent developer can read, extend, and safely modify six months after it was written.*
