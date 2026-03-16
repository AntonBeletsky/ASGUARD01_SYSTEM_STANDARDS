# AI Despaghettization Refactoring Guide
> A step-by-step protocol for using AI to audit, map, plan, and safely refactor selector spaghetti out of a vanilla JS codebase — without breaking anything.

---

## Table of Contents

1. [Overview: The Four-Phase Protocol](#1-overview-the-four-phase-protocol)
2. [Phase 1 — Selector Audit: Build the JSON Map](#2-phase-1--selector-audit-build-the-json-map)
3. [Phase 2 — Refactoring Plan](#3-phase-2--refactoring-plan)
4. [Phase 3 — The Temp Status Map](#4-phase-3--the-temp-status-map)
5. [Phase 5 — The Final Checklist](#5-phase-4--the-final-checklist)
6. [AI Prompts Reference](#6-ai-prompts-reference)

---

## 1. Overview: The Four-Phase Protocol

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1          PHASE 2          PHASE 3        PHASE 4   │
│                                                              │
│  Audit &     →   Refactoring  →   Live Status →  Final      │
│  JSON Map        Plan             Tracking        Checklist  │
│                                                              │
│  selector-       refactor-        temp_status-    done.md   │
│  map.json        plan.json        map.json                  │
└─────────────────────────────────────────────────────────────┘
```

Each phase produces a file. The files are the contract between you and the AI — they make the process auditable, resumable, and safe.

> **Key principle:** The AI never touches code until Phase 1 and Phase 2 are fully complete and you have approved the plan. Audit first. Refactor second.

---

## 2. Phase 1 — Selector Audit: Build the JSON Map

### What to give the AI

Paste all your JS files (or a single concatenated dump). Then use this prompt:

---

### 📋 Prompt: Generate Selector Map

```
You are a senior JS refactoring engineer.

Analyze the following JavaScript code and produce a complete JSON selector map.

For every DOM query found (getElementById, querySelector, querySelectorAll,
getElementsByClassName, getElementsByTagName, $(), jQuery calls, or any
attribute/class/id string used to find an element), output one entry.

Output ONLY valid JSON. No prose. No markdown fences.

Schema for each entry:
{
  "id": "SEL-001",                        // auto-incremented, SEL-NNN
  "selector": "#submit-btn",              // the raw selector string
  "type": "id | class | attribute | tag | jquery",
  "query_method": "getElementById | querySelector | querySelectorAll | etc",
  "file": "checkout.js",                  // filename
  "line": 42,                             // line number
  "context": "handleSubmit()",            // enclosing function or scope
  "used_for": "event | read | write | toggle | existence-check",
  "coupled_to_css": true | false,         // is this selector also in a CSS file?
  "is_global_query": true | false,        // document.X vs container.X
  "instances_on_page": 1,                 // how many matching elements exist (if known)
  "risk": "low | medium | high",          // your assessment: how risky to touch this
  "notes": ""                             // anything unusual
}

[PASTE YOUR CODE HERE]
```

---

### Example output: `selector-map.json`

```json
{
  "generated_at": "2024-01-15T10:30:00Z",
  "total_selectors": 24,
  "high_risk_count": 5,
  "files_analyzed": ["checkout.js", "wishlist.js", "cart.js"],
  "selectors": [
    {
      "id": "SEL-001",
      "selector": "#submit-btn",
      "type": "id",
      "query_method": "getElementById",
      "file": "checkout.js",
      "line": 12,
      "context": "initCheckout()",
      "used_for": "event",
      "coupled_to_css": false,
      "is_global_query": true,
      "instances_on_page": 1,
      "risk": "medium",
      "notes": "Also referenced in checkout.css as #submit-btn { color: red }"
    },
    {
      "id": "SEL-002",
      "selector": "#submit-btn",
      "type": "id",
      "query_method": "getElementById",
      "file": "checkout.js",
      "line": 47,
      "context": "handleSuccess()",
      "used_for": "write",
      "coupled_to_css": false,
      "is_global_query": true,
      "instances_on_page": 1,
      "risk": "medium",
      "notes": "Duplicate query — same element grabbed again in a different function"
    },
    {
      "id": "SEL-003",
      "selector": ".wishlist-item",
      "type": "class",
      "query_method": "querySelectorAll",
      "file": "wishlist.js",
      "line": 8,
      "context": "top-level script",
      "used_for": "event",
      "coupled_to_css": true,
      "is_global_query": true,
      "instances_on_page": null,
      "risk": "high",
      "notes": "Called at top level, not inside any init function. Dynamic items added later won't be caught."
    },
    {
      "id": "SEL-004",
      "selector": "#cart-total",
      "type": "id",
      "query_method": "querySelector",
      "file": "cart.js",
      "line": 33,
      "context": "updateTotal()",
      "used_for": "write",
      "coupled_to_css": false,
      "is_global_query": true,
      "instances_on_page": 1,
      "risk": "low",
      "notes": ""
    },
    {
      "id": "SEL-005",
      "selector": ".item-price",
      "type": "class",
      "query_method": "querySelectorAll",
      "file": "cart.js",
      "line": 55,
      "context": "getTotal()",
      "used_for": "read",
      "coupled_to_css": true,
      "is_global_query": true,
      "instances_on_page": null,
      "risk": "high",
      "notes": "DOM used as data source — reads textContent to calculate total. Violates state-first rule."
    }
  ]
}
```

### After you get the map

Before moving to Phase 2, review it manually:

- [ ] Does the count look right? Scan your files and spot-check a few entries.
- [ ] Are any selectors missing? (AI can miss dynamic strings like `'#' + id`)
- [ ] Mark any entries the AI got wrong — edit the JSON directly.
- [ ] Note all `"risk": "high"` entries — they need special attention in the plan.

---

## 3. Phase 2 — Refactoring Plan

Feed the completed `selector-map.json` back to the AI and ask for a plan.

---

### 📋 Prompt: Generate Refactoring Plan

```
You are a senior JS refactoring engineer.

Below is a selector-map.json produced by auditing a vanilla JS codebase.
Produce a refactoring plan as a JSON file called refactor-plan.json.

Rules:
- Group selectors into modules. A module = one factory function per logical widget/feature.
- For each selector, specify the exact refactoring action.
- Order items by dependency — things that other things depend on come first.
- Flag items that require HTML changes (adding data-js attributes).
- Never suggest removing a selector that has coupled_to_css: true without a CSS note.
- For high-risk items, add an explicit rollback note.
- Output ONLY valid JSON. No prose. No markdown fences.

Schema:

{
  "plan_version": "1.0",
  "created_at": "",
  "source_map": "selector-map.json",
  "modules": [
    {
      "module_id": "MOD-001",
      "module_name": "checkout",
      "root_selector": "[data-js='checkout-form']",
      "files_affected": ["checkout.js", "checkout.html"],
      "items": [
        {
          "sel_id": "SEL-001",
          "action": "replace-with-data-js | wrap-in-init | add-delegation | extract-to-state | scope-to-root | merge-duplicate",
          "from": "#submit-btn",
          "to": "[data-js='submit-btn']",
          "requires_html_change": true,
          "html_change_description": "Add data-js='submit-btn' to the button element",
          "move_query_to": "initCheckout() els object",
          "priority": 1,
          "estimated_effort": "trivial | small | medium | large",
          "rollback_note": ""
        }
      ]
    }
  ],
  "global_changes": [
    {
      "change_id": "GLB-001",
      "description": "Wrap all top-level scripts in DOMContentLoaded or init functions",
      "affects_files": ["wishlist.js"],
      "priority": 1
    }
  ],
  "deferred": [
    {
      "sel_id": "SEL-XXX",
      "reason": "Too risky to touch right now — third-party dependency",
      "revisit_when": ""
    }
  ]
}

[PASTE selector-map.json HERE]
```

---

### Example output: `refactor-plan.json`

```json
{
  "plan_version": "1.0",
  "created_at": "2024-01-15T11:00:00Z",
  "source_map": "selector-map.json",
  "modules": [
    {
      "module_id": "MOD-001",
      "module_name": "checkout",
      "root_selector": "[data-js='checkout-form']",
      "files_affected": ["checkout.js", "checkout.html"],
      "items": [
        {
          "sel_id": "SEL-001",
          "action": "replace-with-data-js",
          "from": "#submit-btn",
          "to": "[data-js='submit-btn']",
          "requires_html_change": true,
          "html_change_description": "Add data-js='submit-btn' to <button id='submit-btn'>",
          "move_query_to": "initCheckout() — els object, line 5",
          "priority": 1,
          "estimated_effort": "trivial",
          "rollback_note": "Revert HTML attribute and querySelector string. CSS uses class .btn-submit, not #submit-btn, so no CSS rollback needed."
        },
        {
          "sel_id": "SEL-002",
          "action": "merge-duplicate",
          "from": "second getElementById('#submit-btn') in handleSuccess()",
          "to": "Reuse els.submitBtn already defined in initCheckout()",
          "requires_html_change": false,
          "html_change_description": "",
          "move_query_to": "delete the query, pass els.submitBtn as argument or close over it",
          "priority": 2,
          "estimated_effort": "trivial",
          "rollback_note": "Restore original getElementById call if closure causes issues."
        }
      ]
    },
    {
      "module_id": "MOD-002",
      "module_name": "wishlist",
      "root_selector": "[data-js='wishlist']",
      "files_affected": ["wishlist.js", "wishlist.html"],
      "items": [
        {
          "sel_id": "SEL-003",
          "action": "add-delegation",
          "from": "querySelectorAll('.wishlist-item') with per-item listeners at top level",
          "to": "Single delegated listener on [data-js='wishlist'] root",
          "requires_html_change": true,
          "html_change_description": "Add data-js='wishlist' to wrapper div. Add data-js='wishlist-item' to each item. Keep .wishlist-item class for CSS.",
          "move_query_to": "createWishlist(rootEl) factory function",
          "priority": 1,
          "estimated_effort": "small",
          "rollback_note": "HIGH RISK. If delegation breaks, restore forEach loop. Verify e.target.closest() works with your item's inner HTML structure."
        }
      ]
    },
    {
      "module_id": "MOD-003",
      "module_name": "cart",
      "root_selector": "[data-js='cart']",
      "files_affected": ["cart.js", "cart.html"],
      "items": [
        {
          "sel_id": "SEL-004",
          "action": "scope-to-root",
          "from": "document.querySelector('#cart-total')",
          "to": "rootEl.querySelector('[data-js=\"cart-total\"]')",
          "requires_html_change": true,
          "html_change_description": "Add data-js='cart-total' to the total element",
          "move_query_to": "createCart(rootEl) — els object",
          "priority": 2,
          "estimated_effort": "trivial",
          "rollback_note": ""
        },
        {
          "sel_id": "SEL-005",
          "action": "extract-to-state",
          "from": "Reading .item-price textContent to calculate total",
          "to": "Maintain items[] array in JS state. Calculate total from array. DOM only renders.",
          "requires_html_change": false,
          "html_change_description": "",
          "move_query_to": "N/A — query is deleted entirely, replaced by state",
          "priority": 1,
          "estimated_effort": "medium",
          "rollback_note": "HIGH RISK. Significant logic change. Ensure items[] is populated correctly on init by reading existing DOM once at startup, then state takes over."
        }
      ]
    }
  ],
  "global_changes": [
    {
      "change_id": "GLB-001",
      "description": "Wrap all top-level code in factory functions. Remove all top-level querySelector/getElementById calls.",
      "affects_files": ["wishlist.js", "cart.js"],
      "priority": 1
    },
    {
      "change_id": "GLB-002",
      "description": "Add bootstrap block at bottom of each file: document.querySelectorAll('[data-js=...']').forEach(init...)",
      "affects_files": ["checkout.js", "wishlist.js", "cart.js"],
      "priority": 3
    }
  ],
  "deferred": []
}
```

### Review the plan before touching any code

- [ ] Does every `sel_id` in the plan correspond to an entry in `selector-map.json`?
- [ ] Are high-risk items clearly flagged with `rollback_note`?
- [ ] Does the priority order make sense? (Globals first, then per-module)
- [ ] Are HTML changes listed completely?
- [ ] Do you agree with the module grouping?

Edit the plan JSON freely. This is your spec, not the AI's.

---

## 4. Phase 3 — The Temp Status Map

Once the plan is approved, create `temp_status-map.json`. This file lives in your repo root during the refactor and is updated after every item is completed.

---

### 📋 Prompt: Generate Initial Status Map

```
Given this refactor-plan.json, generate an initial temp_status-map.json.

Every item from the plan (both module items and global_changes) gets one status entry.
Initial status for all items is "pending".

Output ONLY valid JSON. No prose. No markdown fences.

Schema per entry:
{
  "item_id": "SEL-001",              // or GLB-001 etc.
  "module": "checkout",
  "description": "one-line human summary of what needs to happen",
  "status": "pending | in-progress | done | skipped | blocked",
  "changed_files": [],               // filled in when done
  "html_changed": false,             // true if HTML was modified
  "tested": false,                   // true after manual smoke test
  "notes": "",
  "blocked_reason": "",              // filled if status = blocked
  "completed_at": ""                 // ISO timestamp when done
}

[PASTE refactor-plan.json HERE]
```

---

### Example: `temp_status-map.json`

```json
{
  "refactor_session": "checkout-wishlist-cart-despaghettization",
  "started_at": "2024-01-15T12:00:00Z",
  "last_updated": "2024-01-15T14:22:00Z",
  "total_items": 7,
  "done": 3,
  "in_progress": 1,
  "pending": 2,
  "blocked": 0,
  "skipped": 1,
  "items": [
    {
      "item_id": "GLB-001",
      "module": "global",
      "description": "Wrap all top-level code in factory functions",
      "status": "done",
      "changed_files": ["wishlist.js", "cart.js"],
      "html_changed": false,
      "tested": true,
      "notes": "Moved 3 top-level calls into createWishlist() and createCart()",
      "blocked_reason": "",
      "completed_at": "2024-01-15T12:45:00Z"
    },
    {
      "item_id": "SEL-001",
      "module": "checkout",
      "description": "Replace #submit-btn with data-js='submit-btn', scope to rootEl",
      "status": "done",
      "changed_files": ["checkout.js", "checkout.html"],
      "html_changed": true,
      "tested": true,
      "notes": "",
      "blocked_reason": "",
      "completed_at": "2024-01-15T13:10:00Z"
    },
    {
      "item_id": "SEL-002",
      "module": "checkout",
      "description": "Remove duplicate getElementById in handleSuccess(), reuse els.submitBtn",
      "status": "done",
      "changed_files": ["checkout.js"],
      "html_changed": false,
      "tested": true,
      "notes": "",
      "blocked_reason": "",
      "completed_at": "2024-01-15T13:15:00Z"
    },
    {
      "item_id": "SEL-003",
      "module": "wishlist",
      "description": "Replace per-item listeners with delegated click on root; add data-js attrs",
      "status": "in-progress",
      "changed_files": ["wishlist.js"],
      "html_changed": true,
      "tested": false,
      "notes": "JS done, HTML change still pending",
      "blocked_reason": "",
      "completed_at": ""
    },
    {
      "item_id": "SEL-004",
      "module": "cart",
      "description": "Scope #cart-total query to rootEl, replace with data-js attr",
      "status": "pending",
      "changed_files": [],
      "html_changed": false,
      "tested": false,
      "notes": "",
      "blocked_reason": "",
      "completed_at": ""
    },
    {
      "item_id": "SEL-005",
      "module": "cart",
      "description": "Extract total calculation from DOM into JS state array",
      "status": "blocked",
      "changed_files": [],
      "html_changed": false,
      "tested": false,
      "notes": "",
      "blocked_reason": "Waiting for SEL-004 to be done first — need rootEl in place",
      "completed_at": ""
    },
    {
      "item_id": "GLB-002",
      "module": "global",
      "description": "Add bootstrap blocks at bottom of each module file",
      "status": "skipped",
      "changed_files": [],
      "html_changed": false,
      "tested": false,
      "notes": "Team decided to use a separate init.js file instead",
      "blocked_reason": "",
      "completed_at": ""
    }
  ]
}
```

### Workflow during refactoring

After completing each item, ask the AI:

```
Update temp_status-map.json:
- Set item SEL-003 to "done"
- changed_files: ["wishlist.js", "wishlist.html"]
- html_changed: true
- tested: true
- completed_at: [now]
- Update the top-level counters accordingly

Output only the updated JSON.
```

The status map is your **single source of truth** for where the refactor stands. If you stop mid-session, you can resume by feeding it back to the AI.

---

## 5. Phase 4 — The Final Checklist

Run this checklist only when `temp_status-map.json` shows zero `pending` or `in-progress` items (blocked and skipped items need explicit sign-off).

---

### 📋 Prompt: Generate Final Verification Report

```
You are a QA engineer reviewing a completed JS refactoring.

Given:
1. The original selector-map.json (before refactor)
2. The completed temp_status-map.json
3. The final JS and HTML files (paste below)

Produce a final-checklist.json that verifies every item was handled correctly.

For each check, output: pass | fail | warning | skipped
If fail or warning, include a specific description of what's wrong.

Output ONLY valid JSON. No prose. No markdown fences.

[PASTE ALL THREE]
```

---

### The Full Final Checklist

Even without AI, run through this manually:

#### 🔍 Selector Hygiene

- [ ] **No `getElementById` remains** in any JS file (unless third-party or explicitly deferred)
- [ ] **No `document.querySelector` remains** — all queries go through a `rootEl`
- [ ] **No `querySelectorAll` with per-element `addEventListener`** — replaced by delegation
- [ ] **No selector strings appear twice** in the same module — duplicates merged into `els`
- [ ] **No CSS class used as a JS hook** — all JS hooks are `data-js="..."` attributes
- [ ] **No `#id` selectors in JS** — replaced with `data-js` or scoped queries

#### 🏗 Module Structure

- [ ] **Every module is a factory function** — `function createX(rootEl) { ... }`
- [ ] **Every module queries DOM once** — `els = { ... }` object at the top of the factory
- [ ] **Every module returns a public API** or at minimum a `destroy()` method
- [ ] **No logic runs at top level** — all code is inside functions
- [ ] **Bootstrap block exists** — `document.querySelectorAll(...).forEach(createX)`

#### 🎯 Event Handling

- [ ] **All list/dynamic item events are delegated** — listener on stable parent, not on items
- [ ] **`e.target.closest(...)` used** for delegation — not `e.target.matches()` alone
- [ ] **No inline `onclick` attributes** in HTML — all wired in JS
- [ ] **Focus/blur events use `focusin`/`focusout`** if delegated (they bubble; `focus`/`blur` don't)

#### 🗂 State Management

- [ ] **No state read from the DOM** — no reading `textContent`, `value`, or attributes to derive state
- [ ] **State lives in JS variables** inside the factory closure
- [ ] **`render()` is the only function that writes to DOM** — state change → render()
- [ ] **State updates use immutable patterns** — `items = [...items, newItem]` not `items.push()`

#### 🔌 Module Communication

- [ ] **No module imports another module's internals directly**
- [ ] **Cross-module communication uses CustomEvent or EventBus**
- [ ] **Event names are namespaced** — `cart:updated`, not just `updated`
- [ ] **Event payloads are plain data** — no DOM nodes passed between modules

#### 🧹 Cleanup

- [ ] **Every module with dynamic listeners has a `destroy()` method**
- [ ] **`AbortController` used** for multi-listener cleanup where possible
- [ ] **`MutationObserver` disconnected** when no longer needed
- [ ] **No zombie listeners** — if an element is removed from DOM, its listeners are gone too

#### 🏷 HTML Contracts

- [ ] **Every `data-js` attribute is documented** — in a comment, a README, or this checklist
- [ ] **No `data-js` attribute removed** without updating the corresponding JS
- [ ] **CSS classes not duplicated as `data-js` values** — separation maintained
- [ ] **All HTML changes from `refactor-plan.json`** are applied and verified

#### 🔁 Regression Verification

- [ ] **All features smoke-tested manually** — click every button, trigger every state
- [ ] **Multiple instances tested** — if a widget can appear twice, load a test page with two of them
- [ ] **Dynamic content tested** — add items after page load, verify listeners fire
- [ ] **Keyboard navigation tested** — if it worked before, it still works
- [ ] **Console is clean** — no `Cannot read properties of null`, no `undefined is not a function`
- [ ] **Network tab clean** — no unexpected extra requests from broken logic

#### 📁 Artifact Cleanup

- [ ] **`temp_status-map.json` archived** or deleted — not left in repo root
- [ ] **`selector-map.json` and `refactor-plan.json`** moved to `/docs/refactoring/` or deleted
- [ ] **No commented-out old code** left behind (`// const btn = document.getElementById(...)`)
- [ ] **Git diff reviewed** — no accidental deletions, no stray whitespace-only changes

---

### Example output: `final-checklist.json`

```json
{
  "generated_at": "2024-01-15T16:00:00Z",
  "overall_status": "pass_with_warnings",
  "source_map": "selector-map.json",
  "status_map": "temp_status-map.json",
  "checks": [
    {
      "check_id": "CHK-001",
      "category": "selector_hygiene",
      "description": "No getElementById remains in JS files",
      "result": "pass",
      "detail": ""
    },
    {
      "check_id": "CHK-002",
      "category": "selector_hygiene",
      "description": "No document.querySelector remains",
      "result": "fail",
      "detail": "cart.js line 88: document.querySelector('.flash-message') — not in original selector map, added during refactor. Needs scoping."
    },
    {
      "check_id": "CHK-003",
      "category": "module_structure",
      "description": "All modules are factory functions",
      "result": "pass",
      "detail": ""
    },
    {
      "check_id": "CHK-004",
      "category": "state_management",
      "description": "No state read from DOM",
      "result": "warning",
      "detail": "SEL-005 was marked done but cart.js still reads el.dataset.price in one place (line 112). May be intentional — verify."
    },
    {
      "check_id": "CHK-005",
      "category": "cleanup",
      "description": "All modules have destroy() method",
      "result": "pass",
      "detail": ""
    },
    {
      "check_id": "CHK-006",
      "category": "html_contracts",
      "description": "All data-js attributes from plan are present in HTML",
      "result": "pass",
      "detail": ""
    },
    {
      "check_id": "CHK-007",
      "category": "regression",
      "description": "No console errors on smoke test",
      "result": "pass",
      "detail": ""
    }
  ],
  "fails": 1,
  "warnings": 1,
  "passes": 5,
  "verdict": "Fix CHK-002 before merging. Review CHK-004 warning with team."
}
```

---

## 6. AI Prompts Reference

Quick copy-paste prompts for each phase.

### Generate selector map from code
```
Analyze this JS code and produce selector-map.json.
Output ONLY valid JSON, no prose, no fences.
[schema as above]
[PASTE CODE]
```

### Generate refactoring plan from map
```
Given this selector-map.json, produce refactor-plan.json.
Group into modules. Order by dependency. Flag HTML changes and high-risk items.
Output ONLY valid JSON, no prose, no fences.
[PASTE selector-map.json]
```

### Generate initial status map
```
Given this refactor-plan.json, produce temp_status-map.json with all items set to "pending".
Output ONLY valid JSON, no prose, no fences.
[PASTE refactor-plan.json]
```

### Update status after completing an item
```
Update temp_status-map.json:
- item_id: [SEL-XXX]
- status: done
- changed_files: [list]
- html_changed: true/false
- tested: true
- notes: [anything notable]
- completed_at: [ISO timestamp]
Update the top-level counters.
Output ONLY the full updated JSON, no prose.
[PASTE current temp_status-map.json]
```

### Mark item as blocked
```
Update temp_status-map.json:
- item_id: [SEL-XXX]
- status: blocked
- blocked_reason: [reason]
Output ONLY the full updated JSON.
[PASTE current temp_status-map.json]
```

### Run final verification
```
You are a QA engineer. Given the original selector-map.json, the completed
temp_status-map.json, and the final source files, produce final-checklist.json.
For each check: pass | fail | warning | skipped.
For fails and warnings include specific file + line references.
Output ONLY valid JSON, no prose, no fences.
[PASTE all three]
```

### Resume after a break
```
I'm resuming a refactoring session. Here is my current temp_status-map.json.
Tell me: what is the next pending item to work on, what exactly needs to be done,
and what files I'll need to touch.
[PASTE temp_status-map.json]
```

---

*Audit first. Plan second. Track everything. Verify at the end. In that order, always.*
