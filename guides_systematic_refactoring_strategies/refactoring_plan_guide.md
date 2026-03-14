# Refactoring Plan Guide
> Corporate standard for structured, auditable, machine-readable refactoring instructions.
> Version 1.0.0

---

## 1. Purpose

This standard defines the format, structure, and process for creating refactoring plans at any scale — from fixing a single CSS class to restructuring a module's architecture.

Goals:
- Make every plan verifiable before execution
- Eliminate ambiguity in "before / after" descriptions
- Ensure full traceability of every change
- Enable partial application and rollback
- Establish the audit as a mandatory separate phase

---

## 2. When to Use This Format

| Situation | Use plan |
|---|---|
| 1–2 line fix in a single file | ❌ Not required |
| Changes across 2+ files | ✅ Required |
| Changes touch HTML + CSS + JS simultaneously | ✅ Required |
| Changes affect shared / system styles | ✅ Required |
| Changes affect a public class API or data-attributes | ✅ Required |
| Task is split across multiple people | ✅ Required |

---

## 3. Plan Lifecycle

```
DRAFT → AUDIT → APPROVED → IN PROGRESS → DONE / ROLLED BACK
```

| Status | Description |
|---|---|
| `draft` | Plan written, not yet reviewed |
| `audit` | Conflict and dependency check in progress |
| `approved` | Passed audit, ready to execute |
| `in_progress` | Execution started, some items completed |
| `done` | All items completed and verified |
| `rolled_back` | Reverted — reason recorded in `rollback_reason` |

---

## 4. JSON Plan Structure

### 4.1 Root Object

```json
{
  "plan": {
    "meta": { ... },
    "scope": { ... },
    "audit": { ... },
    "blocks": [ ... ],
    "verification": { ... }
  }
}
```

### 4.2 `meta` Object — Required

```json
"meta": {
  "id": "rfc-2025-001",
  "title": "Short descriptive title of the task",
  "status": "draft | audit | approved | in_progress | done | rolled_back",
  "version": "1.0.0",
  "created": "2025-10-14",
  "updated": "2025-10-14",
  "author": "name or team",
  "reviewer": "name or team | null",
  "rollback_reason": null
}
```

**Rules:**
- `id` — unique, format `rfc-YYYY-NNN`
- `version` — semantic versioning of the plan itself
- `rollback_reason` — filled only when status is `rolled_back`
- `reviewer` — required when status is `approved` or higher

### 4.3 `scope` Object — Required

```json
"scope": {
  "files": [
    "path/to/file.html",
    "path/to/file.css",
    "path/to/file.js"
  ],
  "components": ["MessagesController", ".messages-container"],
  "excluded": ["customer-account-orders.js"],
  "breaking_change": false
}
```

**Rules:**
- `files` — exact paths, not patterns
- `excluded` — explicitly list what is NOT being touched, especially when non-obvious
- `breaking_change` — `true` if the plan changes a public API, data-attributes used externally, or CSS classes used by other components

### 4.4 `audit` Object — Required, filled after review

```json
"audit": {
  "status": "passed | failed | partial",
  "conducted_by": "name | null",
  "conducted_at": "2025-10-14 | null",
  "findings": [
    {
      "item_id": "html-2",
      "severity": "critical | warning | info",
      "description": "Description of the finding",
      "resolution": "How it was addressed in the plan"
    }
  ]
}
```

**Rules:**
- `findings` may be an empty array — meaning no issues found
- `critical` severity blocks `approved` status until resolved
- `warning` is documented but does not block
- `info` is an observation with no required action

### 4.5 `blocks` Array — Main Plan Body

```json
"blocks": [
  {
    "block": "HTML | CSS | JS | CONFIG | OTHER",
    "file": "path/to/file",
    "changes": [ ... ]
  }
]
```

**Rules:**
- One `block` = one file
- If the same file type appears in multiple files — create separate block entries
- Block order = application order

### 4.6 `change` Object — Unit of Change

```json
{
  "id": "html-1",
  "title": "Short description of the change",
  "status": "pending | done | skipped",
  "risk": "low | medium | high",
  "dependencies": [],
  "was": "exact code fragment to be replaced",
  "now": "exact code fragment that replaces it",
  "why": "rationale — what was wrong and why this solution is correct",
  "notes": "optional remarks, edge cases, what to verify after"
}
```

**Rules for `id`:**
- Format `{block_type}-{N}` — e.g. `html-1`, `css-3`, `js-2`
- Unique across the entire plan, not just within a block
- N is sequential starting from 1, continuous across the whole plan

**Rules for `was` / `now`:**
- Must be exact code copied from the real file, never written from memory
- If the change is a deletion — `now` = `"/* deleted */"`
- If the change is a pure addition (nothing replaced) — `was` = `"/* new addition */"`
- If no change applies — `was` and `now` = `"/* no changes */"`, `status` = `"skipped"`
- Surrounding lines included for orientation context must be wrapped in `// [context]`
- Line breaks encoded as `\n`, indentation preserved

**Rules for `risk`:**
- `low` — isolated change, no external dependencies
- `medium` — touches shared styles, data-attributes, or classes used in JS
- `high` — changes a public API, breaking change, or affects multiple components

**Rules for `dependencies`:**
- Array of `id` values of other changes that must be applied first
- Example: `"dependencies": ["html-1"]` — apply this item only after html-1
- Empty array = no dependencies, can be applied in any order

**Rules for `status`:**
- `pending` — not yet applied
- `done` — applied and verified
- `skipped` — intentionally omitted, reason recorded in `notes`

### 4.7 `verification` Object — Post-execution Checklist

```json
"verification": {
  "manual": [
    "Open Messages tab, select a thread — counter displays correctly",
    "Send a message — typing indicator appears and disappears",
    "Check dark theme — bubble backgrounds are correct",
    "Check mobile view — column switcher works"
  ],
  "automated": [
    "npm run lint:css",
    "npm run test:unit -- messages"
  ]
}
```

**Rules:**
- `manual` — specific user actions, not vague phrases like "test the feature"
- `automated` — real runnable commands
- If no automated tests exist — `"automated": []`, do not remove the key

---

## 5. Full Plan Example

```json
{
  "plan": {
    "meta": {
      "id": "rfc-2025-001",
      "title": "Messages tab — align with account page design system",
      "status": "approved",
      "version": "1.0.0",
      "created": "2025-10-14",
      "updated": "2025-10-14",
      "author": "frontend-team",
      "reviewer": "lead-dev",
      "rollback_reason": null
    },

    "scope": {
      "files": [
        "source/shop/customer-account/customer-account.html",
        "source/shop/customer-account/customer-account.css",
        "source/shop/customer-account/customer-account-messages.js"
      ],
      "components": ["MessagesController", ".messages-container", "#tab-correspondence"],
      "excluded": [
        "customer-account-orders.js",
        "customer-account-wishlist.js",
        "shared account layout (sidebar, .account-content-area)"
      ],
      "breaking_change": false
    },

    "audit": {
      "status": "passed",
      "conducted_by": "lead-dev",
      "conducted_at": "2025-10-14",
      "findings": [
        {
          "item_id": "html-2",
          "severity": "critical",
          "description": "The plan proposed creating a new tab-header inside the section, but one already exists above #tab-correspondence. Would have resulted in a duplicate heading.",
          "resolution": "Change reformulated: card-header is deleted entirely, [data-ref=thread-count] is moved into the already existing tab-header."
        }
      ]
    },

    "blocks": [
      {
        "block": "HTML",
        "file": "source/shop/customer-account/customer-account.html",
        "changes": [
          {
            "id": "html-1",
            "title": "Remove card classes from section.messages-container",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "<section class=\"messages-container card shadow-none shadow-md-sm d-flex flex-column overflow-hidden rounded-0 rounded-md-3\" aria-label=\"Seller Correspondence\">",
            "now": "<section class=\"messages-container d-flex flex-column overflow-hidden\" aria-label=\"Seller Correspondence\">",
            "why": "card, shadow-none, shadow-md-sm, rounded-0, rounded-md-3 create a nested card inside .account-content-area which is already a card. No other tab creates its own card wrapper.",
            "notes": null
          },
          {
            "id": "html-2",
            "title": "Delete card-header, move [data-ref=thread-count] into existing tab-header",
            "status": "pending",
            "risk": "medium",
            "dependencies": [],
            "was": "// [context] existing tab-header:\n<span class=\"text-muted small fw-bold\">Support &amp; Sellers</span>\n\n// card-header to be deleted:\n<div class=\"card-header d-flex align-items-center gap-2 py-2\">\n  <span class=\"fw-semibold\">Correspondence</span>\n  <span class=\"badge text-bg-secondary ms-auto\" data-ref=\"thread-count\" aria-live=\"polite\" aria-label=\"Total threads\">0 threads</span>\n</div>",
            "now": "// tab-header with thread counter moved in:\n<span class=\"text-muted small fw-bold\" data-ref=\"thread-count\" aria-live=\"polite\" aria-label=\"Total threads\">Support &amp; Sellers</span>\n\n// card-header deleted entirely",
            "why": "The heading already exists in tab-header above the section. card-header duplicates it and introduces a Bootstrap card pattern into a non-card context. JS queries [data-ref=thread-count] by attribute via querySelector — DOM position does not matter. _syncThreadCount() will overwrite the text on initialisation.",
            "notes": "Initial text 'Support & Sellers' is preserved — JS will overwrite it with '10 threads' on DOMContentLoaded."
          },
          {
            "id": "html-3",
            "title": "Remove bg-body-tertiary from nav.msg-sidebar",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "<nav class=\"msg-sidebar col-12 col-md-4 d-flex flex-column border-end bg-body-tertiary h-100\" aria-label=\"Seller threads\">",
            "now": "<nav class=\"msg-sidebar col-12 col-md-4 d-flex flex-column border-end h-100\" aria-label=\"Seller threads\">",
            "why": "bg-body-tertiary adds a third background layer inside the content area. Column separation is already handled by border-end.",
            "notes": null
          },
          {
            "id": "html-4",
            "title": "Remove bg-body-secondary and fix py-2 to py-3 on chat header",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "<div class=\"border-bottom px-3 py-2 bg-body-secondary d-flex align-items-center gap-2\">",
            "now": "<div class=\"border-bottom px-3 py-3 d-flex align-items-center gap-2\">",
            "why": "bg-body-secondary creates an extra background layer. py-2 does not match the vertical rhythm of the project.",
            "notes": null
          },
          {
            "id": "html-5",
            "title": "Remove bg-body-secondary from input bar",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "<div class=\"border-top p-2 d-flex gap-2 align-items-end bg-body-secondary\">",
            "now": "<div class=\"border-top p-2 d-flex gap-2 align-items-end\">",
            "why": "Same issue as html-4 — unnecessary background layer on the bottom input panel.",
            "notes": null
          }
        ]
      },

      {
        "block": "CSS",
        "file": "source/shop/customer-account/customer-account.css",
        "changes": [
          {
            "id": "css-1",
            "title": "Delete media block with border-radius !important",
            "status": "pending",
            "risk": "low",
            "dependencies": ["html-1"],
            "was": "@media (min-width: 768px) {\n  .messages-container {\n    border-radius: var(--bs-card-border-radius) !important;\n  }\n}",
            "now": "/* deleted */",
            "why": "This block compensated for rounded-0 on the card. After html-1 there is no card — nothing to compensate. !important is not used anywhere in the project's shared styles.",
            "notes": null
          },
          {
            "id": "css-2",
            "title": "Remove !important from mobile display:none switchers",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "@media (max-width: 767.98px) {\n  .messages-container.msg-mob-chat .msg-sidebar {\n    display: none !important;\n  }\n}\n@media (max-width: 767.98px) {\n  .messages-container:not(.msg-mob-chat) .msg-panel {\n    display: none !important;\n  }\n}",
            "now": "@media (max-width: 767.98px) {\n  .messages-container.msg-mob-chat .msg-sidebar {\n    display: none;\n  }\n}\n@media (max-width: 767.98px) {\n  .messages-container:not(.msg-mob-chat) .msg-panel {\n    display: none;\n  }\n}",
            "why": "Selector specificity (0,3,0) already overrides Bootstrap utilities (0,1,0) without !important. Unnecessary !important makes future overrides harder.",
            "notes": null
          },
          {
            "id": "css-3",
            "title": "Fix incorrect Bootstrap token in --msg-bubble-recv-bg",
            "status": "pending",
            "risk": "low",
            "dependencies": [],
            "was": "--msg-bubble-recv-bg: var(--bs-body-secondary);",
            "now": "--msg-bubble-recv-bg: var(--bs-secondary-bg);",
            "why": "var(--bs-body-secondary) is a color token (text color), not a background. var(--bs-secondary-bg) is the correct Bootstrap background token. In dark theme the received bubble was getting the wrong color.",
            "notes": "Difference is minimal in light theme. Verify in dark theme."
          }
        ]
      },

      {
        "block": "JS",
        "file": "source/shop/customer-account/customer-account-messages.js",
        "changes": [
          {
            "id": "js-1",
            "title": "No changes required",
            "status": "skipped",
            "risk": "low",
            "dependencies": [],
            "was": "/* no changes */",
            "now": "/* no changes */",
            "why": "All JS bindings use data-ref attributes which are preserved across all plan items. _syncThreadCount() will overwrite the content of [data-ref=thread-count] on initialisation regardless of the element's position in the DOM.",
            "notes": "Block included to explicitly confirm that JS has been audited and requires no changes."
          }
        ]
      }
    ],

    "verification": {
      "manual": [
        "Open Messages tab — 'MESSAGES' heading and thread counter appear on the same line",
        "Thread counter shows the correct number (10 threads)",
        "Select a thread — seller name, order ID and status badge appear in the chat header",
        "Send a message — typing indicator appears, disappears, bot reply arrives",
        "Check light theme — backgrounds inside Messages match .account-content-area background",
        "Check dark theme — received bubbles have correct background (not a text color token)",
        "Narrow window to 767px — only the sidebar is visible",
        "Select a thread on mobile — switches to chat panel, Back button appears",
        "Press Back — returns to sidebar"
      ],
      "automated": []
    }
  }
}
```

---

## 6. ID Naming Conventions

```
rfc-YYYY-NNN        — plan id
html-N              — HTML change
css-N               — CSS change
js-N                — JS change
config-N            — config files (.env, package.json, etc.)
other-N             — everything else
```

N is sequential starting from 1, continuous across the entire plan.

---

## 7. `was` / `now` Quality Rules

| Requirement | Rule |
|---|---|
| Source | Code copied from the real file, never written from memory |
| Context | Adjacent lines included for orientation must be wrapped in `// [context]` |
| Deletion | `now` = `"/* deleted */"` |
| Addition | `was` = `"/* new addition */"` |
| No change | `was` and `now` = `"/* no changes */"`, `status` = `"skipped"` |
| Formatting | Line breaks as `\n`, indentation preserved |

---

## 8. Audit Rules

The audit is a mandatory step between `draft` and `approved`. It must be conducted by someone other than the plan author, or by the author after a break of at least 1 hour.

The audit checks:

1. **DOM dependencies** — all `data-ref`, `id`, `class` values used in JS exist in the `now` version of the HTML
2. **CSS dependencies** — all classes from `was` CSS are not used by other components outside the scope
3. **Application order** — `dependencies` are filled correctly, no circular dependencies exist
4. **Breaking changes** — if a public API or cross-component classes are changed, `breaking_change: true`
5. **Duplication** — `now` does not create elements that already exist in the DOM

Every finding is recorded in `audit.findings`. Critical findings must be resolved in the plan before status is changed to `approved`.

---

## 9. Partial Application and Rollback

**Partial application:**
Each `change` is independent when `dependencies: []`. Any subset of items can be applied by setting the rest to `status: "skipped"` with the reason in `notes`.

**Rollback:**
The `was` field in every item is the rollback instruction. Apply in reverse order, respecting `dependencies`. After rollback set `meta.status: "rolled_back"` and fill `meta.rollback_reason`.

---

## 10. Plan Versioning

When the plan is modified after creation — increment `meta.version`:
- Patch (`1.0.0` → `1.0.1`) — typo fixes, `notes` clarifications
- Minor (`1.0.0` → `1.1.0`) — new `change` items added
- Major (`1.0.0` → `2.0.0`) — scope revised, already completed items changed, approach reconsidered

Always update `meta.updated` on every modification.
