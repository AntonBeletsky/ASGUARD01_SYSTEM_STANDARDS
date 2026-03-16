// ============================================================================
// AI VALIDATION & REFACTORING CHECKLIST
// ============================================================================

/*
CRITICAL: Read this BEFORE making ANY changes to component code.

This document helps AI avoid the most common mistakes:
1. Changing selector in HTML but not in CSS
2. Renaming class but forgetting querySelector
3. Breaking ARIA sync
4. Missing data-attribute updates
5. Orphaned CSS rules
*/

// ============================================================================
// SECTION 1: PRE-MODIFICATION CHECKLIST
// ============================================================================

BEFORE YOU START:
─────────────────

□ Load component.selectors.json
□ Identify ALL files you will modify
□ List the exact change (e.g., ".button__icon" → ".button__icon-wrapper")
□ Check the "usedIn" array for all occurrences
□ Count occurrences in code files to verify completeness

EXAMPLE:
  Change: .button__icon → .button__icon-wrapper
  
  usedIn from JSON:
    css: ["Button.css:28", "Button.css:35"]
    js: ["Button.js:18"]
    html: ["Button.html:3"]
  
  Verification:
    Button.css line 28: ✓ Found (.button__icon {)
    Button.css line 35: ✓ Found (.button__icon::before)
    Button.js line 18:  ✓ Found (querySelector('.button__icon'))
    Button.html line 3: ✓ Found (class="button__icon")
  
  Status: ALL FOUND → Safe to proceed


// ============================================================================
// SECTION 2: SELECTOR MODIFICATION RULES
// ============================================================================

RULE 1: CLASS SELECTORS (.className)
──────────────────────────────────────
When changing: .button → .btn

Files to update:
  ✓ CSS - All .button { } rules
  ✓ CSS - All .button:hover, .button:focus rules
  ✓ CSS - All .button__* child selectors
  ✓ CSS - All .button--* modifier selectors
  ✓ JS - All querySelector('.button')
  ✓ JS - All classList.add('button')
  ✓ JS - All classList.remove('button')
  ✓ HTML - All class="button" attributes
  ✓ Tests - All selector references
  ✓ JSON - The selectors entry

Validation:
  • Count occurrences in code = count in JSON
  • No mixed usage (.button and .btn in same file)
  • ARIA attributes updated if needed


RULE 2: DATA ATTRIBUTES (data-*)
─────────────────────────────────
When changing: data-button-id → data-id

Files to update:
  ✓ HTML - All data-button-id="..." attributes
  ✓ JS - All querySelector('[data-button-id="..."]')
  ✓ JS - All getAttribute('data-button-id')
  ✓ JS - All dataset.buttonId references
  ✓ JSON - The dataAttributes entry

Validation:
  • Both HTML attribute name AND value must match JS query
  • camelCase in JS (dataset.buttonId) = kebab-case in HTML (data-button-id)
  • All query selectors updated


RULE 3: ARIA ATTRIBUTES (aria-*)
─────────────────────────────────
When changing: aria-label → aria-label (usually NOT renamed)

Files to update:
  ✓ HTML - aria-label="..." or aria-labelledby="..."
  ✓ JS - All setAttribute('aria-label', value)
  ✓ JS - All getAttribute('aria-label')
  ✓ JS - All removeAttribute('aria-label')
  ✓ JSON - The ariaAttributes entry

Critical Syncs:
  • aria-invalid must match .input--error state
  • aria-hidden must match .modal--open state
  • aria-busy must match .button--loading state
  • aria-disabled must match .button--disabled state

Validation:
  • Check CSS rule that sets class state
  • Check JS code that sets ARIA attribute
  • Both must happen in same method/listener


RULE 4: CSS VARIABLE NAMES (--custom-props)
─────────────────────────────────────────────
When changing: --button-primary-bg → --primary-bg

Files to update:
  ✓ CSS - All var(--button-primary-bg) usages
  ✓ CSS - All definition lines
  ✓ Config files if variables are defined there
  ✓ JSON - The cssVariables entry

Validation:
  • Variable must be defined before used
  • All var(--button-primary-bg) replaced
  • No mismatched property names


RULE 5: JAVASCRIPT VARIABLES (this.property)
──────────────────────────────────────────────
When changing: this.isDisabled → this.disabled

Files to update:
  ✓ JS - All this.isDisabled = ... assignments
  ✓ JS - All if (this.isDisabled) conditions
  ✓ JS - All return statements using this.isDisabled
  ✓ Tests - All references to this.isDisabled
  ✓ JSON - The jsVariables entry

Validation:
  • Property must be initialized in constructor
  • All references updated consistently
  • Type remains the same


// ============================================================================
// SECTION 3: CRITICAL SYNC MATRIX
// ============================================================================

These four things MUST stay in sync:

┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ HTML            │ CSS             │ JS              │ JSON            │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ class="button"  │ .button {       │ querySelector  │ selectors.root  │
│                 │   ...           │   ('.button')   │   .selector     │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ class="button   │ .button--       │ classList.add   │ selectors.*     │
│ button--primary"│ primary {       │   ('button--    │ appliedTo       │
│                 │   ...           │   primary')     │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ data-action=    │ [data-action]   │ getAttribute    │ dataAttributes  │
│ "submit"        │ selector        │   ('data-      │ .attribute      │
│                 │                 │   action')      │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ aria-label=     │ (not directly)  │ setAttribute    │ ariaAttributes  │
│ "..."           │                 │   ('aria-      │ .attribute      │
│                 │                 │   label', ...)  │                 │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

Broken Sync Example:
  HTML: class="button__text" ✓
  CSS: .button__text { } ✓
  JS: querySelector('.button-text') ✗ MISMATCH
  JSON: "selector": ".button__text" ✓
  
  Result: Text won't be found in JS → Error!


// ============================================================================
// SECTION 4: MODIFICATION RESPONSE FORMAT
// ============================================================================

When you complete ANY change, provide this structure:

{
  "changeDescription": "What was changed and why",
  
  "affectedFiles": [
    {
      "file": "Button.html",
      "lineNumber": 3,
      "before": "<svg class=\"button__icon\">",
      "after": "<svg class=\"button__icon-wrapper\">",
      "reason": "Clearer semantic naming"
    },
    {
      "file": "Button.css",
      "lineNumber": 28,
      "before": ".button__icon {",
      "after": ".button__icon-wrapper {",
      "reason": "Match HTML change"
    },
    {
      "file": "Button.js",
      "lineNumber": 18,
      "before": "this.icon = DOM.query('.button__icon');",
      "after": "this.icon = DOM.query('.button__icon-wrapper');",
      "reason": "Match HTML selector"
    }
  ],

  "jsonUpdates": [
    {
      "path": "selectors.icon.selector",
      "oldValue": ".button__icon",
      "newValue": ".button__icon-wrapper"
    },
    {
      "path": "selectors.icon.usedIn.css",
      "oldValue": ["Button.css:28", "Button.css:35"],
      "newValue": ["Button.css:28", "Button.css:35"]
    }
  ],

  "historyEntry": {
    "date": "2024-03-16T11:30:00Z",
    "author": "claude-ai-v1",
    "type": "refactoring",
    "changes": [
      {
        "from": ".button__icon",
        "to": ".button__icon-wrapper",
        "reason": "Clearer semantic naming",
        "affectedFiles": ["Button.html", "Button.css", "Button.js"],
        "validated": true
      }
    ]
  },

  "validationResults": {
    "allSelectorsFound": true,
    "allReferencesUpdated": true,
    "noOrphanedSelectors": true,
    "ariaSyncMaintained": true,
    "errors": []
  }
}


// ============================================================================
// SECTION 5: COMMON MISTAKES TO AVOID
// ============================================================================

MISTAKE 1: Only updating one location
─────────────────────────────────────
❌ Wrong:
  Changed HTML: class="button__icon-wrapper"
  Forgot CSS: Still has .button__icon { }
  Result: Styles don't apply!

✓ Right:
  Use usedIn from JSON to find ALL locations
  Update EVERY location mentioned


MISTAKE 2: Mismatching kebab-case and camelCase
─────────────────────────────────────────────────
❌ Wrong:
  HTML: data-button-id="123"
  JS: getAttribute('data-button_id') // underscore!
  Result: Always returns undefined!

✓ Right:
  HTML: data-button-id (always kebab-case)
  JS: dataset.buttonId (always camelCase)
  Both refer to same attribute


MISTAKE 3: Breaking ARIA sync
──────────────────────────────
❌ Wrong:
  JS code: classList.add('button--disabled')
  But forgot: setAttribute('aria-disabled', 'true')
  Result: CSS changes but screen reader sees wrong state!

✓ Right:
  Always update both:
    classList.add('button--disabled')
    setAttribute('aria-disabled', 'true')


MISTAKE 4: Partial selector matching
─────────────────────────────────────
❌ Wrong:
  Find and replace ".button" everywhere
  This also replaces ".button__icon" → ".btn__icon" ✗
  
✓ Right:
  Be specific with regex or full selectors:
    Search: ^\.button$ (exact match)
    Or list each exact selector from JSON


MISTAKE 5: Forgetting test updates
───────────────────────────────────
❌ Wrong:
  Updated component code
  Forgot to update test selectors
  Result: Tests fail even though code is correct!

✓ Right:
  After changing selectors, update:
    querySelector in tests
    Mock selectors
    Assertion selectors


MISTAKE 6: Not updating documentation
──────────────────────────────────────
❌ Wrong:
  Code: class="button__icon-wrapper"
  Docs: "Use .button__icon for icons"
  Result: Confusing developers!

✓ Right:
  Update README and JSDoc comments too


// ============================================================================
// SECTION 6: STEP-BY-STEP REFACTORING WORKFLOW
// ============================================================================

STEP 1: LOAD & ANALYZE
──────────────────────
[] Load component.selectors.json
[] Read the selector you want to change
[] Note all usedIn locations
[] Count total occurrences

Example:
  Changing: .button__icon
  Occurrences: CSS (2), JS (1), HTML (1) = Total 4


STEP 2: VERIFY IN CODE
──────────────────────
[] Open each file mentioned in usedIn
[] Physically count occurrences in code
[] Verify they match the JSON count

Example:
  CSS line 28: .button__icon { ✓
  CSS line 35: .button__icon::before ✓
  JS line 18: querySelector('.button__icon') ✓
  HTML line 3: class="button__icon" ✓
  Total: 4 ✓ MATCHES


STEP 3: MAKE CHANGES
────────────────────
[] Update HTML file
[] Update CSS file
[] Update JS file
[] Update tests if they exist


STEP 4: UPDATE JSON
───────────────────
[] Update selector value
[] Update usedIn line numbers if changed
[] Add history entry
[] Run validation check


STEP 5: FINAL VALIDATION
────────────────────────
[] Search for old selector name in all files - should find 0
[] Search for new selector name in all files - should match JSON count
[] Check CSS for orphaned rules
[] Run tests if available
[] Verify ARIA attributes still sync


STEP 6: REPORT CHANGES
──────────────────────
[] Provide response in format from SECTION 4
[] List all files modified
[] Show before/after
[] Confirm validation passed


// ============================================================================
// SECTION 7: QUICK REFERENCE - WHAT BREAKS EASILY
// ============================================================================

┌──────────────────────┬─────────────────────────────────────────────────┐
│ What Changed         │ Places to Update                                │
├──────────────────────┼─────────────────────────────────────────────────┤
│ .button              │ CSS (all rules), JS (all querySelector),        │
│ (root class)         │ HTML (all class), Tests, Docs, JSON             │
├──────────────────────┼─────────────────────────────────────────────────┤
│ .button__icon        │ CSS (.button__icon {}), JS (querySelector),     │
│ (element class)      │ HTML (class), Tests, JSON                       │
├──────────────────────┼─────────────────────────────────────────────────┤
│ .button--primary     │ CSS (.button--primary {}), HTML (class),        │
│ (modifier)           │ Tests, JSON                                     │
├──────────────────────┼─────────────────────────────────────────────────┤
│ data-button-id       │ HTML (attribute), JS (getAttribute,             │
│ (data attr)          │ querySelector), Tests, JSON                     │
├──────────────────────┼─────────────────────────────────────────────────┤
│ aria-label           │ HTML (attribute), JS (setAttribute),            │
│ (aria attr)          │ Tests, JSON                                     │
├──────────────────────┼─────────────────────────────────────────────────┤
│ --button-primary-bg  │ CSS (all var() usages), Config files,           │
│ (CSS variable)       │ JSON                                            │
├──────────────────────┼─────────────────────────────────────────────────┤
│ this.isDisabled      │ JS (all assignments and usages), Tests,         │
│ (JS variable)        │ JSON                                            │
└──────────────────────┴─────────────────────────────────────────────────┘


// ============================================================================
// SECTION 8: VALIDATION CHECKLIST (Final)
// ============================================================================

After making changes, go through this:

SELECTORS:
  □ Old selector doesn't exist anymore (grep returns 0)
  □ New selector exists in exactly expected locations
  □ Count matches JSON usedIn array

CSS:
  □ All .old-selector rules deleted
  □ All .new-selector rules present
  □ No orphaned rules
  □ :hover, :focus, ::before states updated

JAVASCRIPT:
  □ All querySelector('.old') replaced
  □ All querySelector('.new') present
  □ All classList.add('old') replaced
  □ All classList.remove('old') replaced
  □ All dataset references correct (camelCase)

HTML:
  □ All class="old" replaced
  □ All class="new" present
  □ All data-attributes use kebab-case
  □ All aria-attributes present and correct

SYNC:
  □ CSS class and JS class match
  □ data-attribute HTML and JS query match
  □ aria-attribute set in both HTML and JS
  □ CSS variables defined and used

TESTS:
  □ querySelector selectors updated
  □ Class name assertions updated
  □ All tests pass

DOCUMENTATION:
  □ README updated
  □ JSDoc comments updated
  □ JSON map updated

SAFETY:
  □ No console errors
  □ Component still renders
  □ Interactions still work
  □ No broken ARIA

═══════════════════════════════════════════════════════════════════════════════
FINAL CHECK: Can you trace the selector from HTML → CSS → JS and back? ✓
═══════════════════════════════════════════════════════════════════════════════
