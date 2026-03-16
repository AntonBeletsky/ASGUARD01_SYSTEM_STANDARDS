/*
╔══════════════════════════════════════════════════════════════════════════════╗
║         JSON SELECTOR PROTOCOL GUIDE v1.0                                    ║
║   Component Development & Refactoring Standard for AI-Assisted Development   ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROBLEM:
AI modifies HTML selectors but forgets to update CSS and JS that depend on them.
Result: Broken selectors, inconsistent naming, maintenance nightmares.

SOLUTION:
Maintain a comprehensive JSON "Component Map" that tracks ALL selector
relationships, element names, variables, and data attributes in one place.
Before any refactoring, validate changes against this map.

*/

// ============================================================================
// SECTION 1: COMPONENT SELECTOR MAP (component.selectors.json)
// ============================================================================

{
  "componentName": "Button",
  "version": "2.1.0",
  "lastModified": "2024-03-16T10:30:00Z",
  "modifiedBy": "claude-ai-v1",
  
  // ========================================================================
  // SECTION 1.1: HTML SELECTORS (All DOM query paths)
  // ========================================================================
  "selectors": {
    
    // Root element - the component wrapper
    "root": {
      "selector": ".button",
      "type": "class",
      "element": "button",
      "required": true,
      "description": "Main button component wrapper",
      "usedIn": {
        "css": ["Button.css:2"],
        "js": ["Button.js:12", "Button.js:45"],
        "html": ["Button.html:1"]
      }
    },

    // Element: icon inside button
    "icon": {
      "selector": ".button__icon",
      "type": "class",
      "element": "svg|img|i",
      "required": false,
      "parent": ".button",
      "description": "Icon element inside button",
      "usedIn": {
        "css": ["Button.css:28", "Button.css:35"],
        "js": ["Button.js:18"],
        "html": ["Button.html:3"]
      }
    },

    // Element: text content
    "text": {
      "selector": ".button__text",
      "type": "class",
      "element": "span",
      "required": false,
      "parent": ".button",
      "description": "Text label inside button",
      "usedIn": {
        "css": ["Button.css:42"],
        "js": ["Button.js:55"],
        "html": ["Button.html:4"]
      }
    },

    // Modifier: primary variant
    "variantPrimary": {
      "selector": ".button--primary",
      "type": "class",
      "appliedTo": ".button",
      "required": false,
      "description": "Blue primary button style",
      "usedIn": {
        "css": ["Button.css:50", "Button.css:58"],
        "js": ["Button.js:72"],
        "html": ["Button.html:1"]
      }
    },

    // Modifier: secondary variant
    "variantSecondary": {
      "selector": ".button--secondary",
      "type": "class",
      "appliedTo": ".button",
      "required": false,
      "description": "Gray secondary button style",
      "usedIn": {
        "css": ["Button.css:66"],
        "js": null,
        "html": ["Button.html:8"]
      }
    },

    // State: disabled button
    "disabled": {
      "selector": ".button--disabled",
      "type": "class",
      "appliedTo": ".button",
      "required": false,
      "altSelector": "button:disabled",
      "description": "Button disabled state",
      "usedIn": {
        "css": ["Button.css:78", "Button.css:85"],
        "js": ["Button.js:92", "Button.js:110"],
        "html": null
      }
    },

    // State: loading
    "loading": {
      "selector": ".button--loading",
      "type": "class",
      "appliedTo": ".button",
      "required": false,
      "description": "Loading/spinner animation state",
      "usedIn": {
        "css": ["Button.css:120"],
        "js": ["Button.js:88"],
        "html": null
      }
    }
  },

  // ========================================================================
  // SECTION 1.2: DATA ATTRIBUTES (Data binding)
  // ========================================================================
  "dataAttributes": {
    "buttonAction": {
      "attribute": "data-action",
      "element": ".button",
      "type": "string",
      "examples": ["submit", "close", "open-modal"],
      "description": "Action type for button",
      "usedIn": {
        "js": ["Button.js:15", "App.js:42"],
        "html": ["Button.html:1"]
      }
    },

    "buttonId": {
      "attribute": "data-button-id",
      "element": ".button",
      "type": "string|number",
      "examples": ["submit-btn", "open-modal-btn"],
      "description": "Unique button identifier",
      "usedIn": {
        "js": ["Button.js:22"],
        "html": ["Button.html:1"]
      }
    },

    "loading": {
      "attribute": "data-loading",
      "element": ".button",
      "type": "boolean",
      "values": ["true", "false"],
      "description": "Loading state indicator",
      "usedIn": {
        "js": ["Button.js:85"],
        "html": null
      }
    }
  },

  // ========================================================================
  // SECTION 1.3: ARIA ATTRIBUTES (Accessibility)
  // ========================================================================
  "ariaAttributes": {
    "label": {
      "attribute": "aria-label",
      "element": ".button",
      "type": "string",
      "required": true,
      "description": "Accessible label for screen readers",
      "usedIn": {
        "js": ["Button.js:25"],
        "html": ["Button.html:2"]
      }
    },

    "busy": {
      "attribute": "aria-busy",
      "element": ".button",
      "type": "boolean",
      "values": ["true", "false"],
      "setBy": "JavaScript when loading",
      "usedIn": {
        "js": ["Button.js:89"]
      }
    },

    "disabled": {
      "attribute": "aria-disabled",
      "element": ".button",
      "type": "boolean",
      "values": ["true", "false"],
      "description": "Alternative to disabled attribute",
      "usedIn": {
        "js": ["Button.js:98"]
      }
    }
  },

  // ========================================================================
  // SECTION 1.4: CSS VARIABLES (Theme values)
  // ========================================================================
  "cssVariables": {
    "primaryColor": {
      "variable": "--button-primary-bg",
      "scope": ".button--primary",
      "values": ["#007bff", "#0056b3"],
      "description": "Primary button background color",
      "usedIn": {
        "css": ["Button.css:50", "Button.css:58"]
      }
    },

    "primaryHover": {
      "variable": "--button-primary-hover",
      "scope": ".button--primary",
      "values": ["#0056b3"],
      "description": "Primary button hover state color",
      "usedIn": {
        "css": ["Button.css:58"]
      }
    },

    "padding": {
      "variable": "--button-padding",
      "scope": ".button",
      "values": ["12px 24px"],
      "description": "Default button padding",
      "usedIn": {
        "css": ["Button.css:8"]
      }
    },

    "borderRadius": {
      "variable": "--button-border-radius",
      "scope": ".button",
      "values": ["4px"],
      "description": "Button corner rounding",
      "usedIn": {
        "css": ["Button.css:12"]
      }
    }
  },

  // ========================================================================
  // SECTION 1.5: JAVASCRIPT VARIABLES (Class properties)
  // ========================================================================
  "jsVariables": {
    "element": {
      "variable": "this.element",
      "type": "HTMLElement",
      "description": "Reference to DOM button element",
      "initialized": "constructor(element)",
      "usedIn": ["Button.js:5", "Button.js:15", "Button.js:42"]
    },

    "isDisabled": {
      "variable": "this.isDisabled",
      "type": "boolean",
      "default": false,
      "description": "Internal disabled state flag",
      "modified": ["disable()", "enable()"],
      "usedIn": ["Button.js:8", "Button.js:92", "Button.js:110"]
    },

    "listeners": {
      "variable": "this.unlistenClick",
      "type": "function",
      "description": "Callback to remove click listener",
      "createdIn": "init()",
      "calledIn": "destroy()",
      "usedIn": ["Button.js:18", "Button.js:125"]
    }
  },

  // ========================================================================
  // SECTION 1.6: METHOD SIGNATURES
  // ========================================================================
  "methods": {
    "constructor": {
      "signature": "constructor(element: HTMLElement)",
      "returns": "void",
      "description": "Initialize button component",
      "calls": ["init()"],
      "usedIn": ["Button.js:4"]
    },

    "init": {
      "signature": "init(): void",
      "description": "Setup listeners and state",
      "creates": ["unlistenClick"],
      "usedIn": ["Button.js:11"]
    },

    "disable": {
      "signature": "disable(): void",
      "description": "Disable button",
      "modifies": [".button--disabled", "aria-disabled"],
      "usedIn": ["App.js:55"]
    },

    "enable": {
      "signature": "enable(): void",
      "description": "Enable button",
      "modifies": [".button--disabled", "aria-disabled"],
      "usedIn": ["App.js:62"]
    },

    "setLoading": {
      "signature": "setLoading(isLoading: boolean): void",
      "description": "Show/hide loading state",
      "modifies": [".button--loading", "aria-busy"],
      "usedIn": ["App.js:75"]
    },

    "destroy": {
      "signature": "destroy(): void",
      "description": "Cleanup listeners",
      "calls": ["unlistenClick()"],
      "usedIn": ["App.js:120"]
    }
  },

  // ========================================================================
  // SECTION 1.7: EVENT DEFINITIONS
  // ========================================================================
  "events": {
    "clicked": {
      "eventName": "button:clicked",
      "emittedBy": "handleClick()",
      "payload": {
        "buttonElement": "HTMLElement",
        "buttonId": "string",
        "timestamp": "number"
      },
      "listenedBy": ["App.js:42", "Analytics.js:15"],
      "description": "Fired when button is clicked"
    },

    "loaded": {
      "eventName": "button:loaded",
      "emittedBy": "setLoading(false)",
      "payload": {
        "buttonId": "string"
      },
      "listenedBy": ["App.js:88"],
      "description": "Fired when loading completes"
    }
  },

  // ========================================================================
  // SECTION 1.8: DEPENDENCIES GRAPH
  // ========================================================================
  "dependencies": {
    "internal": [
      "DOM.js (utility)",
      "EventBus.js (event system)"
    ],
    "external": null,
    "imports": {
      "CSS": ["Button.css:1"],
      "JS": []
    }
  },

  // ========================================================================
  // SECTION 1.9: VALIDATION RULES (For AI refactoring safety)
  // ========================================================================
  "validationRules": [
    {
      "rule": "selector-consistency",
      "description": "If .button selector changes, update all references",
      "checkpoints": [
        "CSS: .button {} definition",
        "HTML: <button class=\"button\">",
        "JS: querySelector('.button')",
        "JS: this.element check",
        "Docs: README.md references"
      ]
    },
    {
      "rule": "bem-structure",
      "description": "Child elements must use BEM format",
      "pattern": ".{componentName}__{elementName}",
      "examples": [".button__icon", ".button__text"],
      "allowed": true,
      "checkpoints": ["CSS definitions", "HTML structure", "JS queries"]
    },
    {
      "rule": "modifier-independence",
      "description": "Modifiers must not conflict with states",
      "examples": {
        "correct": ".button--primary, .button--disabled",
        "incorrect": ".button--primary--disabled"
      }
    },
    {
      "rule": "aria-sync",
      "description": "ARIA attributes must sync with CSS classes",
      "sync": {
        "disabled": ["aria-disabled", ".button--disabled"],
        "loading": ["aria-busy", ".button--loading"]
      }
    },
    {
      "rule": "data-attr-usage",
      "description": "Use data-* for JS queries, not classes",
      "correct": "querySelector('[data-action=\"submit\"]')",
      "incorrect": "querySelector('.submit-action')"
    }
  ],

  // ========================================================================
  // SECTION 1.10: REFACTORING HISTORY (Audit trail)
  // ========================================================================
  "history": [
    {
      "date": "2024-03-16T10:30:00Z",
      "author": "claude-ai-v1",
      "type": "creation",
      "changes": "Initial component map created"
    },
    {
      "date": "2024-03-15T09:00:00Z",
      "author": "claude-ai-v0.9",
      "type": "refactoring",
      "changes": [
        {
          "from": ".btn",
          "to": ".button",
          "reason": "BEM naming standardization",
          "affectedFiles": ["Button.css", "Button.js", "Button.html"],
          "validated": true
        }
      ]
    }
  ]
}


// ============================================================================
// SECTION 2: QUICK REFERENCE CHECKLIST
// ============================================================================

/*
BEFORE MAKING ANY CHANGE, CHECK:

[ ] 1. SELECTORS
    [ ] Is selector used in CSS?
    [ ] Is selector used in JS (querySelector)?
    [ ] Is selector used in HTML?
    [ ] Are there child element selectors?

[ ] 2. DATA ATTRIBUTES
    [ ] Update data-* in HTML
    [ ] Update querySelector in JS
    [ ] Update in tests

[ ] 3. CSS CLASSES
    [ ] Update all CSS rules
    [ ] Update modifier rules
    [ ] Update state rules
    [ ] Update media queries

[ ] 4. JAVASCRIPT
    [ ] Update querySelector calls
    [ ] Update class names in classList.add/remove
    [ ] Update in initialization
    [ ] Update in event handlers
    [ ] Update in tests

[ ] 5. ARIA ATTRIBUTES
    [ ] Update attribute names
    [ ] Update in JS setters
    [ ] Update in CSS ::before/::after if used

[ ] 6. VARIABLES
    [ ] Update CSS variable names
    [ ] Update all CSS references
    [ ] Update in theme files

[ ] 7. DOCUMENTATION
    [ ] Update README
    [ ] Update API docs
    [ ] Update JSDoc comments
    [ ] Update this selector map

[ ] 8. VALIDATION
    [ ] Run unit tests
    [ ] Check console for errors
    [ ] Verify in browser
    [ ] Check accessibility (ARIA)
*/


// ============================================================================
// SECTION 3: USAGE WORKFLOW FOR AI
// ============================================================================

/*
STEP 1: LOAD THE MAP
────────────────────
Before any work, load component.selectors.json to understand all dependencies.

Example AI Internal Monologue:
"I'm refactoring Button component. Let me check the map..."
- Button.js: queries .button (root)
- Button.js: queries .button__icon (child)
- Button.css: has .button--primary, .button--disabled
- Need to update: HTML, CSS, JS, tests

STEP 2: PLAN CHANGES
────────────────────
List ALL files that will be modified:

Change: Rename .button__icon to .button__icon-wrapper
Files to update:
  - Button.html (4 occurrences)
  - Button.css (3 rules)
  - Button.js (1 querySelector)
  - Button.test.js (2 tests)
  - component.selectors.json (icon entry)

STEP 3: MAKE CHANGES
────────────────────
Only modify files listed in Step 2.

STEP 4: VALIDATE AGAINST MAP
─────────────────────────────
After changes, verify:
  1. Check CSS: New selector exists in CSS
  2. Check JS: querySelector matches new selector
  3. Check HTML: class attribute matches new selector
  4. Check usedIn: All locations updated in map

STEP 5: UPDATE THE MAP
──────────────────────
Update component.selectors.json with:
  - New selector values
  - Updated usedIn references
  - New history entry

STEP 6: VERIFY COMPLETENESS
────────────────────────────
Run validation:
  - All usedIn locations have matching code
  - No orphaned selectors
  - No undefined references
*/


// ============================================================================
// SECTION 4: VALIDATION SCRIPT (For AI to run)
// ============================================================================

/*
VALIDATION PSEUDO-CODE (Use before committing changes):

function validateComponentMap(files, mapJson) {
  const errors = [];

  // Check 1: All selectors exist in code
  for (const [key, selector] of Object.entries(mapJson.selectors)) {
    if (!selector.usedIn.css && !selector.usedIn.js && !selector.usedIn.html) {
      errors.push(`ORPHANED: ${selector.selector} not used anywhere`);
    }
  }

  // Check 2: All usedIn references exist
  for (const [key, selector] of Object.entries(mapJson.selectors)) {
    for (const file of selector.usedIn.css || []) {
      if (!findInFile(files, file, selector.selector)) {
        errors.push(`BROKEN: ${selector.selector} referenced in ${file} but not found`);
      }
    }
    for (const file of selector.usedIn.js || []) {
      if (!findInFile(files, file, selector.selector)) {
        errors.push(`BROKEN: ${selector.selector} referenced in ${file} but not found`);
      }
    }
  }

  // Check 3: Class consistency
  for (const [key, selector] of Object.entries(mapJson.selectors)) {
    if (selector.type === 'class') {
      const count = countOccurrences(files, selector.selector);
      if (count === 0) {
        errors.push(`UNUSED: ${selector.selector}`);
      }
    }
  }

  // Check 4: ARIA sync
  for (const [key, aria] of Object.entries(mapJson.ariaAttributes)) {
    const correspondingSelector = mapJson.selectors[aria.element];
    if (correspondingSelector && aria.sync) {
      // Verify sync
    }
  }

  return {
    isValid: errors.length === 0,
    errors: errors
  };
}
*/


// ============================================================================
// SECTION 5: EXAMPLE REFACTORING SCENARIO
// ============================================================================

/*
SCENARIO: Rename .button__icon to .button__icon-container

STEP 1: IDENTIFY CHANGES
─────────────────────────
From component.selectors.json, icon selector:
  {
    "selector": ".button__icon",
    "usedIn": {
      "css": ["Button.css:28", "Button.css:35"],
      "js": ["Button.js:18"],
      "html": ["Button.html:3"]
    }
  }

Changes needed in 3 files.

STEP 2: MAKE CHANGES
─────────────────────
File 1: Button.html (line 3)
  BEFORE: <svg class="button__icon">
  AFTER:  <svg class="button__icon-container">

File 2: Button.css (lines 28, 35)
  BEFORE: .button__icon { ... }
  AFTER:  .button__icon-container { ... }

File 3: Button.js (line 18)
  BEFORE: this.icon = DOM.query('.button__icon');
  AFTER:  this.icon = DOM.query('.button__icon-container');

STEP 3: UPDATE MAP
──────────────────
component.selectors.json:
  {
    "icon": {
      "selector": ".button__icon-container",  // ← CHANGED
      "usedIn": {
        "css": ["Button.css:28", "Button.css:35"],
        "js": ["Button.js:18"],
        "html": ["Button.html:3"]
      }
    }
  }

Add to history:
  {
    "date": "2024-03-16T11:00:00Z",
    "author": "claude-ai-v1",
    "type": "refactoring",
    "changes": [
      {
        "from": ".button__icon",
        "to": ".button__icon-container",
        "reason": "Clearer naming to indicate container role",
        "affectedFiles": ["Button.css", "Button.js", "Button.html"],
        "validated": true
      }
    ]
  }

STEP 4: VALIDATE
────────────────
✓ All CSS rules updated
✓ All JS queries updated
✓ All HTML classes updated
✓ Map reflects all changes
✓ No orphaned selectors
✓ All usedIn references accurate
*/


// ============================================================================
// SECTION 6: INTEGRATION WITH AI WORKFLOW
// ============================================================================

/*
INSTRUCTION FOR AI SYSTEMS:

1. BEFORE STARTING WORK
   - Load component.selectors.json
   - Understand full selector graph
   - Identify all dependencies

2. WHEN MODIFYING CODE
   - Reference the map for all selector usages
   - Update the map simultaneously
   - Never change selectors without updating map

3. WHEN RENAMING ANYTHING
   - Create change entry in history
   - List all affected files
   - Validate completeness before submitting

4. RESPONSE FORMAT (For code changes)
   {
     "changes": [
       {
         "file": "Button.js",
         "line": 18,
         "before": ".button__icon",
         "after": ".button__icon-container",
         "reason": "..."
       }
     ],
     "mapUpdates": [
       {
         "selector": "icon",
         "change": "selector value",
         "oldValue": ".button__icon",
         "newValue": ".button__icon-container"
       }
     ],
     "validationResult": {
       "isValid": true,
       "errors": []
     }
  }

5. SAFETY CHECKS
   [ ] All selectors found in code files
   [ ] No breaking references
   [ ] ARIA sync maintained
   [ ] CSS and JS consistency
   [ ] Test updates included
*/


// ============================================================================
// SECTION 7: MULTI-COMPONENT SYSTEM MAP
// ============================================================================

/*
For a complete design system, create: design-system.map.json

{
  "designSystem": "MyDS",
  "version": "1.0.0",
  "components": [
    {
      "name": "Button",
      "path": "components/Button/component.selectors.json",
      "version": "2.1.0"
    },
    {
      "name": "Input",
      "path": "components/Input/component.selectors.json",
      "version": "1.5.0"
    },
    {
      "name": "Modal",
      "path": "components/Modal/component.selectors.json",
      "version": "2.0.0"
    }
  ],
  "sharedVariables": {
    "colors": "colors.css",
    "typography": "typography.css",
    "spacing": "spacing.css"
  },
  "eventBus": {
    "location": "utils/EventBus.js",
    "events": [
      {
        "name": "button:clicked",
        "emittedBy": "Button",
        "listenedBy": ["Modal", "App"]
      },
      {
        "name": "modal:opened",
        "emittedBy": "Modal",
        "listenedBy": ["App"]
      }
    ]
  }
}
*/

// ============================================================================
// END OF JSON SELECTOR PROTOCOL GUIDE v1.0
// ============================================================================
