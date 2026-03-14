# Enterprise Bootstrap 5 Refactoring Guide
> Based on the Account Tab refactoring case study.  
> From broken legacy HTML → production-ready, self-contained component.

---

## Table of Contents

1. [Phase 0 — Before You Touch Any Code](#phase-0--before-you-touch-any-code)
2. [Phase 1 — Deep Analysis](#phase-1--deep-analysis)
3. [Phase 2 — Structural Planning](#phase-2--structural-planning)
4. [Phase 3 — HTML Skeleton](#phase-3--html-skeleton)
5. [Phase 4 — CSS Layer](#phase-4--css-layer)
6. [Phase 5 — JavaScript Architecture](#phase-5--javascript-architecture)
7. [Phase 6 — Sub-module: Toast Notifications](#phase-6--sub-module-toast-notifications)
8. [Phase 7 — Sub-module: Form State Machine](#phase-7--sub-module-form-state-machine)
9. [Phase 8 — Sub-module: CRUD with Modal](#phase-8--sub-module-crud-with-modal)
10. [Phase 9 — Security & Edge Cases](#phase-9--security--edge-cases)
11. [Phase 10 — Accessibility Audit](#phase-10--accessibility-audit)
12. [Phase 11 — Final Checklist](#phase-11--final-checklist)
13. [Anti-Pattern Reference](#anti-pattern-reference)

---

## Phase 0 — Before You Touch Any Code

Before writing a single line, answer these four questions in writing.
This is not optional — the answers directly shape every decision that follows.

### Q1: What is the business purpose of this component?

Identify what real user problem it solves.

```
Example answer (Account Tab):
"This is a user account management panel. It has two jobs:
 1. Let the user view and edit their profile data.
 2. Let the user manage saved delivery addresses (add, edit, remove)."
```

### Q2: What are all the UI states?

List every possible visual state the component can be in.

```
Example answer (Account Tab):

Personal Data form:
  - VIEW   → all fields readonly, only Edit button visible
  - EDIT   → fields unlocked, Save + Cancel visible, password toggle appears
  - SAVING → Save button shows spinner, fields locked

Each Address Card:
  - VIEW   → input readonly, only Edit + Remove visible
  - EDIT   → input editable, Save + Cancel visible

Modal:
  - HIDDEN  → default
  - VISIBLE → shows address label + value in body text, Confirm active
```

### Q3: What is currently broken or missing?

Write a bug list before touching anything.

```
Example list (Account Tab):
  [BUG-1]  readonly="true" — invalid HTML, must be boolean readonly
  [BUG-2]  Remove button has no context — modal doesn't know which address to delete
  [BUG-3]  Add Address button has zero JS implementation
  [BUG-4]  Modal is nested inside accordion-body — z-index/overflow issue
  [BUG-5]  No Cancel button on Personal Data form — user cannot escape edit mode
  [BUG-6]  Password fields always visible — should be hidden until needed
  [BUG-7]  Two separate accordion components — no unified open/close behaviour
  [BUG-8]  No validation before Save
  [BUG-9]  No user feedback after any action (no toast, no visual confirmation)
  [BUG-10] 14 lines of duplicated card HTML — not data-driven
```

### Q4: What must NOT change?

Identify what must be preserved (visual intent, Bootstrap usage, feature scope).

```
Example answer (Account Tab):
  - Must stay Bootstrap 5 (no Tailwind, no custom grid)
  - Must keep accordion layout for both sections
  - Must keep the two-column card layout for addresses on desktop
  - Must keep the remove confirmation modal pattern
  - No backend integration required — stubs are acceptable
```

---

## Phase 1 — Deep Analysis

Systematically audit the existing code across four dimensions.

### 1.1 Business Logic Audit

Read every element and ask: "what job does this do?"

| Element | Intended Job | Actually Working? |
|---|---|---|
| `accordion-button` | Open/close section | ✅ Yes (Bootstrap handles it) |
| Edit button | Switch form to edit mode | ❌ No JS attached |
| Save button | Commit changes | ❌ No JS attached |
| Remove button | Delete address | ❌ Broken — no context passed |
| Add button | Create new card | ❌ No JS attached |

### 1.2 State Management Audit

Trace every interactive element and ask: "what happens when I click this?"

```
Audit method: read the HTML top to bottom.
For every button, input, and link — write down:
  - What does it show/hide?
  - What data does it read/write?
  - What happens after?

If the answer is "nothing" or "unclear" → add to bug list.
```

### 1.3 Structural / Bootstrap Audit

Check for these specific Bootstrap misuse patterns:

```
☐ Are modals at body level? (not nested inside cards/accordions)
☐ Is there one accordion with multiple items, or multiple accordions?
☐ Are readonly attributes correct? (boolean, not readonly="true")
☐ Are form elements using Bootstrap's own classes? (form-control, form-label)
☐ Are grids using g-* for gutters on the row, not mb-* on columns?
☐ Is data-bs-parent used on the collapse elements (not the accordion wrapper)?
```

### 1.4 Code Quality Audit

```
☐ Count duplicated HTML blocks — if the same structure repeats 3+ times,
  it must become a function or template.
☐ Find all inline styles — eliminate or justify each one.
☐ Find phantom/typo classes (like "roundedd") — remove all.
☐ Check for empty attributes (style="", class="") — clean all.
☐ Check for missing aria-* attributes on interactive elements.
☐ Check for missing aria-hidden="true" on decorative icons.
```

---

## Phase 2 — Structural Planning

Plan the output before writing HTML.

### 2.1 Decide the Component Boundary

Decide what is "inside" this component and what belongs outside.

```
Rule: Modals always go OUTSIDE the component, at body level.

Reason: Bootstrap modals use position:fixed and high z-index.
If a modal is inside an element with overflow:hidden or a
stacking context (like an accordion), it will be clipped or
appear behind other elements.

Pattern:
  <section id="my-component">
    ... all component HTML ...
  </section>

  <!-- OUTSIDE the component: -->
  <div class="modal fade" id="my-modal"> ... </div>
  <div id="toast-container"> ... </div>
```

### 2.2 Plan the JavaScript Sub-modules

Split logic by responsibility. Never write one giant script.

```
For the Account Tab, the split was:

  AccountToast       → shows ephemeral feedback toasts
  AccountPersonal    → personal data form state machine
  AccountAddresses   → address CRUD + modal lifecycle

Each module has:
  - init()           → called once on DOMContentLoaded
  - private methods  → prefixed with _ to signal internal use
  - its own state    → no shared mutable variables between modules
```

### 2.3 Plan the Data Store

If the component renders a list of items, define the data shape first.

```javascript
// Define the shape before building the UI
const addressStore = [
  { id: 1, label: 'Home', value: '1234 Main St, City, State' },
  { id: 2, label: 'Work', value: '5678 Elm St, City, State'  },
];
// id     → unique key for remove/edit operations
// label  → displayed as card heading
// value  → the address string in the input
```

**Rule:** The UI is always derived from the store. Never read values
from the DOM as the source of truth — always read from the store.

### 2.4 Plan State Transitions

Draw the state machine before writing any JS.

```
Personal Data Form:

  [VIEW] ──── click Edit ───────────────► [EDIT]
  [EDIT] ──── click Cancel ─────────────► [VIEW]  (values restored from snapshot)
  [EDIT] ──── click Save (invalid) ────► [EDIT]  (validation error shown)
  [EDIT] ──── click Save (valid) ──────► [SAVING] ──── API completes ──► [VIEW]

Address Card:

  [VIEW] ──── click Edit ───────────────► [EDIT]
  [EDIT] ──── click Cancel ─────────────► [VIEW]  (value restored from snapshot)
  [EDIT] ──── click Save (empty) ───────► [EDIT]  (inline error shown)
  [EDIT] ──── click Save (valid) ───────► [VIEW]  (store updated)
  [VIEW] ──── click Remove ─────────────► Modal shown
  Modal  ──── click Confirm ────────────► item removed from store → re-render
  Modal  ──── click Cancel/X ───────────► pendingId cleared, modal closed
```

---

## Phase 3 — HTML Skeleton

Build the HTML in this exact order. Do not write JS yet.

### 3.1 Component Root

Use a `<section>` (not `<div>`) for a major UI region.
Give it an `id` that matches the tab system and an `aria-labelledby`.

```html
<section
  class="container-fluid p-3"
  id="tab-content-account"
  aria-labelledby="account-panel-heading"
>
  <h2 class="fs-4 fw-semibold" id="account-panel-heading">Account</h2>

  <!-- accordion goes here -->

</section>
```

### 3.2 Unified Accordion

One accordion, multiple items. Never use separate accordion components
for sections that belong to the same panel.

```html
<div class="accordion" id="accountAccordion">

  <!-- Item 1 -->
  <div class="accordion-item rounded-3 mb-2 border">
    <h2 class="accordion-header" id="hdg-personal">
      <button
        class="accordion-button collapsed"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#col-personal"
        aria-expanded="false"
        aria-controls="col-personal"
      >
        <i class="fa-regular fa-user me-2" aria-hidden="true"></i>
        Personal Data
      </button>
    </h2>
    <div
      id="col-personal"
      class="accordion-collapse collapse"
      aria-labelledby="hdg-personal"
      data-bs-parent="#accountAccordion"  ← THIS links it to the group
    >
      <div class="accordion-body">
        <!-- form goes here -->
      </div>
    </div>
  </div>

  <!-- Item 2 (same pattern) -->

</div>
```

**Key rules:**
- `data-bs-parent` goes on the `collapse` div, NOT on the `accordion-item`
- Each `accordion-button` gets `aria-controls` matching its target ID
- Each `accordion-collapse` gets `aria-labelledby` matching its header ID

### 3.3 Form Fields

Use correct boolean attributes. Use semantic autocomplete values.

```html
<!-- CORRECT -->
<input type="text" class="form-control" id="inp-first-name"
       value="John" readonly autocomplete="given-name" />

<!-- WRONG — never do this -->
<input type="text" class="form-control" id="firstName"
       value="John" readonly="true" />
```

### 3.4 Button Groups (View/Edit mode)

Design buttons for both states in the HTML. JS only toggles `d-none`.

```html
<!-- All three exist in DOM. JS shows/hides them. -->
<div class="d-flex gap-2" id="personal-btn-group">

  <!-- Visible in VIEW mode -->
  <button type="button" class="btn btn-outline-primary flex-fill"
          id="btn-personal-edit">
    <i class="fa-regular fa-pen-to-square me-1" aria-hidden="true"></i> Edit
  </button>

  <!-- Visible in EDIT mode (hidden by default) -->
  <button type="button" class="btn btn-success flex-fill d-none"
          id="btn-personal-save">
    <i class="fa-solid fa-floppy-disk me-1" aria-hidden="true"></i> Save
  </button>
  <button type="button" class="btn btn-outline-secondary flex-fill d-none"
          id="btn-personal-cancel">
    Cancel
  </button>

</div>
```

### 3.5 Modal (at body level)

Place modals after the closing `</section>` tag, never inside it.

```html
</section>  ← component ends here

<!-- Modal lives at body level -->
<div class="modal fade" id="modal-remove-address"
     tabindex="-1"
     aria-labelledby="modal-remove-label"
     aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content rounded-3 border-0 shadow">
      <div class="modal-header border-0">
        <h5 class="modal-title" id="modal-remove-label">Remove Address</h5>
        <button type="button" class="btn-close"
                data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <!-- JS writes the specific address text here before showing -->
        <p id="modal-remove-message"></p>
      </div>
      <div class="modal-footer border-0">
        <button type="button" class="btn btn-outline-secondary"
                data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-danger"
                id="btn-confirm-remove">Remove</button>
      </div>
    </div>
  </div>
</div>

<!-- Toast container also at body level -->
<div id="acc-toast-container" aria-live="polite" aria-atomic="true"></div>
```

---

## Phase 4 — CSS Layer

**Core rule: Write ZERO CSS that Bootstrap already provides.**

Before writing any custom CSS, ask: "Is there a Bootstrap utility for this?"
If yes — use the utility. If no — write the custom rule with a comment explaining why.

### 4.1 What belongs in custom CSS

Only these categories justify custom CSS:

| Category | Example | Why Bootstrap can't do it |
|---|---|---|
| CSS custom properties (tokens) | `--acc-transition: 0.22s ease` | Bootstrap doesn't expose animation tokens |
| Transitions on state changes | `input { transition: background-color 0.2s }` | No Bootstrap utility for transition on specific properties |
| Hover effects with transform | `card:hover { transform: translateY(-2px) }` | No Bootstrap utility for translateY hover |
| Keyframe animations | `@keyframes save-pulse { ... }` | Not provided by Bootstrap |
| Fixed positioning with specific z-index | Toast container at `z-index: 1090` | Needs to be above Bootstrap modal (1055) |

### 4.2 The correct CSS file structure

```css
/* ============================================================
   COMPONENT NAME — Custom CSS
   Only rules that Bootstrap cannot provide natively.
   ============================================================ */

/* ── Design tokens ── */
:root {
  --acc-transition : 0.22s ease;
  --acc-radius     : 0.5rem;
  --acc-shadow-card: 0 2px 8px rgba(0,0,0,.07);
  --acc-shadow-lift: 0 6px 20px rgba(0,0,0,.12);
}

/* ── Rule: what it does + WHY Bootstrap can't handle it ── */
.acc-field {
  /* Smooth visual transition when toggling readonly state.
     Bootstrap has no utility for property-specific transitions. */
  transition: background-color var(--acc-transition),
              border-color     var(--acc-transition);
}

.acc-field[readonly] {
  /* Read-only visual treatment.
     Bootstrap's form-control-plaintext changes layout too aggressively;
     we want the field border to remain but appear muted. */
  background-color: var(--bs-tertiary-bg);
  border-color    : transparent;
  cursor          : default;
}
```

### 4.3 CSS anti-patterns to eliminate

```css
/* ❌ Bootstrap has p-3 */
.my-card { padding: 16px; }

/* ❌ Bootstrap has d-flex align-items-center */
.vcenter { display: flex; align-items: center; }

/* ❌ Bootstrap has fw-bold */
.bold-text { font-weight: 700; }

/* ❌ Bootstrap has rounded-3 */
.rounded { border-radius: 0.5rem; }

/* ❌ Never fight Bootstrap with !important */
.accordion-item { border: none !important; }
```

---

## Phase 5 — JavaScript Architecture

### 5.1 The IIFE wrapper

All code lives inside a single IIFE. Zero global variables.

```javascript
/* ============================================================
   COMPONENT NAME — ES6+ Module-style IIFE
   Zero jQuery. Zero global namespace pollution.

   Sub-modules:
     ModuleA  — description
     ModuleB  — description
   ============================================================ */
(() => {
  'use strict';

  // sub-modules defined here

  document.addEventListener('DOMContentLoaded', () => {
    ModuleA.init();
    ModuleB.init();
  });

})();
```

### 5.2 Sub-module structure

Every sub-module follows this exact template:

```javascript
const ModuleName = {

  // ── Private state ──────────────────────────────────────
  _state    : 'default',   // prefix _ = private by convention
  _snapshot : new Map(),

  // ── Public entry point ─────────────────────────────────
  /**
   * Initialize the module. Called once on DOMContentLoaded.
   * Binds all event listeners.
   */
  init() {
    const btn = document.getElementById('my-btn');
    if (!btn) return;  // Guard: element might not exist on this page

    btn.addEventListener('click', () => this._handleClick());
  },

  // ── Private methods ────────────────────────────────────
  /**
   * JSDoc for every method: what it does, params, returns.
   * @param {string} value - Description
   * @returns {boolean}
   */
  _handleClick() {
    // implementation
  },
};
```

### 5.3 Event delegation pattern

For dynamic lists (like address cards), always use delegation.
**Never** rebind individual listeners after each re-render.

```javascript
// ❌ WRONG — binds to each card individually,
//            breaks after re-render, leaks memory
document.querySelectorAll('.addr-edit-btn').forEach(btn => {
  btn.addEventListener('click', handler);
});

// ✅ CORRECT — single listener on stable parent container,
//              works for dynamically added cards
grid.addEventListener('click', (e) => {
  const btn = e.target.closest('button[data-action]');
  if (!btn) return;

  const card      = btn.closest('[data-address-id]');
  const addressId = card ? parseInt(card.dataset.addressId, 10) : null;

  switch (btn.dataset.action) {
    case 'edit'  : this._enterEdit(card);            break;
    case 'save'  : this._saveEdit(card, addressId);  break;
    case 'cancel': this._cancelEdit(card);           break;
    case 'remove': this._requestRemove(addressId);   break;
  }
});
```

---

## Phase 6 — Sub-module: Toast Notifications

Every mutating action (save, add, remove) must give the user feedback.
Build a reusable toast factory as the first sub-module.

```javascript
const AccountToast = {
  /**
   * Show a self-dismissing Bootstrap toast.
   * @param {string} message
   * @param {'success'|'danger'|'warning'} [type='success']
   */
  show(message, type = 'success') {
    const container = document.getElementById('acc-toast-container');
    if (!container) return;

    const iconMap = {
      success : 'fa-circle-check text-success',
      danger  : 'fa-circle-xmark text-danger',
      warning : 'fa-triangle-exclamation text-warning',
    };

    const toastEl = document.createElement('div');
    toastEl.className = 'toast align-items-center border-0 shadow-sm mb-2';
    toastEl.setAttribute('role', type === 'danger' ? 'alert' : 'status');
    toastEl.setAttribute('aria-live', type === 'danger' ? 'assertive' : 'polite');
    toastEl.setAttribute('aria-atomic', 'true');
    toastEl.innerHTML = `
      <div class="d-flex">
        <div class="toast-body d-flex align-items-center gap-2">
          <i class="fa-solid ${iconMap[type]}" aria-hidden="true"></i>
          ${message}
        </div>
        <button type="button" class="btn-close me-2 m-auto"
                data-bs-dismiss="toast" aria-label="Close"></button>
      </div>`;

    container.appendChild(toastEl);

    const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
    toast.show();

    // Remove from DOM after hiding to prevent accumulation
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
  },
};
```

**Usage throughout all other modules:**
```javascript
AccountToast.show('Address saved successfully.');
AccountToast.show('Passwords do not match.', 'danger');
AccountToast.show('Please verify your input.', 'warning');
```

---

## Phase 7 — Sub-module: Form State Machine

### 7.1 The snapshot pattern (Cancel support)

Before unlocking fields, snapshot the current values.
On Cancel, restore from snapshot.

```javascript
_enterEditMode() {
  // 1. Take snapshot BEFORE unlocking anything
  this._snapshot.clear();
  this._profileFieldIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) this._snapshot.set(id, el.value);
  });

  // 2. Unlock fields
  this._setFieldsReadonly(this._profileFieldIds, false);

  // 3. Show edit-mode buttons
  document.getElementById('btn-edit')  .classList.add('d-none');
  document.getElementById('btn-save')  .classList.remove('d-none');
  document.getElementById('btn-cancel').classList.remove('d-none');
},

_handleCancel() {
  // Restore from snapshot
  this._snapshot.forEach((value, id) => {
    const el = document.getElementById(id);
    if (el) el.value = value;
  });

  this._returnToViewMode();
},
```

### 7.2 The async save pattern (with spinner)

```javascript
async _handleSave() {
  // 1. Validate first — abort if invalid
  if (!this._validate()) return;

  // 2. Show spinner, disable button
  const btn = document.getElementById('btn-save');
  btn.disabled = true;
  btn.innerHTML = `
    <span class="spinner-border spinner-border-sm me-1"
          role="status" aria-hidden="true"></span>
    Saving…`;

  // 3. API call (replace setTimeout with real fetch())
  await new Promise(resolve => setTimeout(resolve, 800));

  // 4. Restore button, switch to view mode
  btn.disabled  = false;
  btn.innerHTML = `<i class="fa-solid fa-floppy-disk me-1"
                      aria-hidden="true"></i> Save`;
  this._returnToViewMode();

  AccountToast.show('Saved successfully.');
},
```

### 7.3 The readonly toggle utility

```javascript
/**
 * Set or remove the readonly attribute on a list of inputs.
 * @param {string[]} ids
 * @param {boolean}  readonly
 */
_setFieldsReadonly(ids, readonly) {
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (readonly) {
      el.setAttribute('readonly', '');      // boolean attribute — no value
    } else {
      el.removeAttribute('readonly');
    }
  });
},
```

---

## Phase 8 — Sub-module: CRUD with Modal

### 8.1 Data-driven rendering

Never duplicate HTML. Render all list items from a data array.

```javascript
// The store is the source of truth
_store: [
  { id: 1, label: 'Home', value: '1234 Main St...' },
  { id: 2, label: 'Work', value: '5678 Elm St...'  },
],
_nextId: 3,  // Auto-increment counter

// One render function, called after every mutation
_renderGrid() {
  const grid = document.getElementById('address-grid');
  grid.innerHTML = '';

  if (this._store.length === 0) {
    grid.innerHTML = `<div class="col-12">
      <p class="text-center text-body-secondary py-3">No addresses yet.</p>
    </div>`;
    return;
  }

  this._store.forEach(address => {
    const col = document.createElement('div');
    col.className = 'col-12 col-md-6';
    col.innerHTML = this._buildCardHTML(address);  // template function
    grid.appendChild(col);
  });

  // Bind events AFTER render (or use delegation on stable parent)
  this._bindCardButtons(grid);
},
```

### 8.2 Safe HTML generation (XSS prevention)

When injecting user-controlled strings into `innerHTML`, always escape.

```javascript
/**
 * Escape HTML special characters to prevent XSS injection.
 * @param {string} str
 * @returns {string}
 */
_escapeHTML(str) {
  return String(str)
    .replace(/&/g,  '&amp;')
    .replace(/</g,  '&lt;')
    .replace(/>/g,  '&gt;')
    .replace(/"/g,  '&quot;')
    .replace(/'/g,  '&#39;');
},

// Usage in template function:
_buildCardHTML(address) {
  return `
    <div class="card" data-address-id="${address.id}">
      <input value="${this._escapeHTML(address.value)}" readonly />
      ...
    </div>`;
},
```

### 8.3 The correct Remove → Modal flow

The modal must know WHICH item to delete. Use a pending ID field.

```javascript
_pendingRemoveId: null,

// Step 1: User clicks Remove
_requestRemove(addressId) {
  // Store the ID BEFORE showing modal
  this._pendingRemoveId = addressId;

  // Populate modal with specific address info (user clarity)
  const address = this._store.find(a => a.id === addressId);
  const msg = document.getElementById('modal-remove-message');
  if (msg && address) {
    msg.textContent = `Remove "${address.label}" — ${address.value}?`;
  }

  // Show modal via Bootstrap API (not data-bs-toggle on button)
  const modalEl = document.getElementById('modal-remove-address');
  bootstrap.Modal.getOrCreateInstance(modalEl).show();
},

// Step 2: User clicks Confirm in modal
_executeRemove() {
  if (this._pendingRemoveId === null) return;

  // Mutate store
  this._store = this._store.filter(a => a.id !== this._pendingRemoveId);
  this._pendingRemoveId = null;

  // Close modal
  const modalEl = document.getElementById('modal-remove-address');
  bootstrap.Modal.getInstance(modalEl)?.hide();

  // Re-render from updated store
  this._renderGrid();
  AccountToast.show('Address removed.');
},

// Safety: clear pending ID if modal dismissed without confirming
_bindModalConfirm() {
  document.getElementById('btn-confirm-remove')
    .addEventListener('click', () => this._executeRemove());

  document.getElementById('modal-remove-address')
    .addEventListener('hidden.bs.modal', () => {
      this._pendingRemoveId = null;  // Always clear on close
    });
},
```

### 8.4 Add new item with validation

```javascript
_bindAddButton() {
  const btn   = document.getElementById('btn-add-address');
  const input = document.getElementById('inp-new-address');

  const attemptAdd = () => {
    const trimmed = input.value.trim();

    // Validate: not empty
    if (!trimmed) {
      input.classList.add('is-invalid');
      input.focus();
      return;
    }

    input.classList.remove('is-invalid');

    // Add to store
    this._store.push({
      id    : this._nextId++,
      label : `Address ${this._store.length + 1}`,
      value : trimmed,
    });

    input.value = '';       // Clear field
    this._renderGrid();     // Re-render
    AccountToast.show('New address added.');
  };

  btn.addEventListener('click', attemptAdd);

  // Enter key support
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      attemptAdd();
    }
  });
},
```

---

## Phase 9 — Security & Edge Cases

### 9.1 XSS prevention checklist

```
☐ Every string from user input injected into innerHTML is passed
  through _escapeHTML() before insertion.

☐ Strings set via .textContent or .value are safe (browser handles escaping).

☐ data-* attributes set from user input are escaped in the template function.
```

### 9.2 Empty state handling

```javascript
// Every list render function must handle the empty case
if (this._store.length === 0) {
  container.innerHTML = `
    <p class="text-body-secondary text-center py-4">
      No items yet.
    </p>`;
  return;
}
```

### 9.3 Null-safe DOM access

```javascript
// Every getElementById can return null if the element doesn't exist.
// Guard all critical operations.

const btn = document.getElementById('btn-save');
if (!btn) return;   // ← guard before using

// For optional chaining on method calls:
bootstrap.Modal.getInstance(modalEl)?.hide();  // ← safe even if no instance
```

### 9.4 Preventing double-submission

```javascript
async _handleSave() {
  const btn = document.getElementById('btn-save');

  btn.disabled = true;   // ← prevent double-click
  // ... async work ...
  btn.disabled = false;  // ← re-enable after completion
},
```

---

## Phase 10 — Accessibility Audit

Run this checklist on the finished HTML before considering it done.

### 10.1 Semantic structure

```
☐ Major regions use <section>, <nav>, <header>, <main> — not bare <div>
☐ Headings (h1–h6) are used in logical order, not for visual sizing
☐ Forms have an aria-label or are labelled by a visible heading
☐ Lists of items (address cards) have aria-label on their container
```

### 10.2 Interactive elements

```
☐ Every <button> has descriptive text or aria-label
☐ Buttons that repeat (e.g., "Edit" on each card) have unique
  aria-label values: "Edit Home address", "Edit Work address"
☐ Icon-only buttons (trash icon) have aria-label explaining action
☐ Decorative icons have aria-hidden="true"
☐ All form inputs have a visible <label> with correct for= attribute
```

### 10.3 Live regions

```
☐ The address grid has aria-live="polite" so screen readers
  announce when cards are added or removed
☐ The toast container has aria-live="polite" (or "assertive" for errors)
☐ Error toasts use role="alert" for immediate announcement
```

### 10.4 Form attributes

```
☐ Inputs use autocomplete values where applicable:
    given-name, family-name, email, tel, username,
    current-password, new-password
☐ Required fields have aria-required="true"
☐ Fields with hints use aria-describedby pointing to the hint element
☐ Validation error messages use .invalid-feedback and are
  connected via the Bootstrap is-invalid class on the input
```

### 10.5 Bootstrap-specific

```
☐ accordion-button has aria-expanded and aria-controls
☐ accordion-collapse has aria-labelledby pointing to its header
☐ modal has aria-labelledby pointing to its title
☐ modal has tabindex="-1" (required for Bootstrap to manage focus)
☐ btn-close elements have aria-label="Close"
```

---

## Phase 11 — Final Checklist

Before the file is considered production-ready, verify every item.

### HTML

```
☐ All readonly inputs use boolean readonly (not readonly="true")
☐ No inline style="" attributes (empty or otherwise)
☐ No phantom/non-existent CSS classes
☐ No duplicate IDs on the page
☐ Unique label-for / input-id pairs (no ID conflicts between cards)
☐ Modal is at body level
☐ Toast container is at body level
☐ All <i> icons have aria-hidden="true"
```

### CSS

```
☐ Every custom CSS rule has a comment explaining why Bootstrap can't handle it
☐ No !important rules
☐ No pixel values that duplicate Bootstrap spacing tokens
☐ CSS custom properties defined in :root for reusable values
☐ Transition/animation-only rules separated from layout rules
```

### JavaScript

```
☐ Entire script is wrapped in an IIFE with 'use strict'
☐ Zero jQuery — all DOM via vanilla ES6+
☐ Zero global variables
☐ Every public function has a JSDoc comment
☐ Every module has a single init() method
☐ Event delegation used for dynamically rendered lists
☐ Snapshot pattern implemented for all Cancel operations
☐ _escapeHTML() called on all user strings injected into innerHTML
☐ Async save shows spinner + disables button during operation
☐ Modal pending ID cleared on both Confirm and Dismiss
☐ All getElementById calls guarded against null
☐ DOMContentLoaded wraps all init() calls
```

### Bootstrap

```
☐ data-bs-parent on collapse divs (not on accordion wrapper)
☐ Bootstrap Modal controlled via JS API (getOrCreateInstance / getInstance)
  for programmatic show/hide — not data-bs-toggle on remove buttons
  (because context must be set before modal opens)
☐ Bootstrap Toast created and shown programmatically
☐ No custom CSS that overrides Bootstrap's own component styles
```

---

## Anti-Pattern Reference

Quick reference — things to catch and fix immediately.

| Found in code | Fix |
|---|---|
| `readonly="true"` | → `readonly` |
| `style=""` (empty) | → remove entirely |
| `class="roundedd"` (typo) | → remove |
| Multiple `accordion` divs for one panel | → merge into one with multiple items |
| Modal inside accordion-body | → move to body level |
| `data-bs-toggle="modal"` on Remove button | → use Bootstrap JS API after setting context |
| Same "Edit" label on every card's button | → add unique `aria-label` per card |
| `document.querySelectorAll` + forEach addEventListener on list items | → use event delegation on parent |
| Reading form values from DOM as source of truth | → maintain a data store, render from it |
| User string injected into innerHTML without escaping | → pass through `_escapeHTML()` |
| No Cancel button in edit forms | → always provide a Cancel with snapshot restore |
| Password fields always visible | → hide in collapsible sub-section, show only in edit mode |
| No feedback after mutations | → every add/save/remove calls `AccountToast.show()` |
| `let i = 0` style variable names in handlers | → descriptive names: `addressId`, `trimmedValue` |
| One giant `DOMContentLoaded` handler with all logic | → split into named sub-modules with `init()` |

---

*This guide reflects the patterns applied in the Account Tab refactoring.
Apply the same phases to any Bootstrap 5 component of equivalent complexity.*
