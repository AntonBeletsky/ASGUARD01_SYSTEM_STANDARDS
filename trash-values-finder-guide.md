# trash-values-finder-guide.md

> AI guide: finding dead code, broken chains, and refactoring artifacts in CSS / JS / TS projects.
> The goal is not just to find "unused" things — it's to reconstruct the logical chain: where it came from, where it was going, why it's still there.

---

## Philosophy: think in chains, not files

Every entity in code is a node in a logical chain:

```
declaration → passing → usage → effect
```

Dead code is a chain with a break. A refactoring artifact is a chain that was renamed at one end but not the other. The AI's job: find the break, understand which end it's on, and decide — fix or delete.

**Three outcomes for every finding:**
1. **Rename** — the name changed in one place but not the other
2. **Delete** — the entity genuinely does nothing, no incoming references
3. **Keep** — the finding is a false positive (dynamic reference, external API, planned future use)

---

## Part 1. CSS — classes and selectors

### 1.1 Algorithm for finding dead classes

**Step 1. Collect all declared classes from CSS / SCSS / Less**

Parse accounting for nesting (SCSS `&-modifier`), pseudo-classes (`:hover`, `::before`), and media queries. You only need "root" class names — strip pseudo-elements and combinators.

```
Pattern: /\.([a-zA-Z_-][a-zA-Z0-9_-]*)/g
```

Exclude from the "declared" list:
- Classes inside `@keyframes`
- Classes inside comments
- Vendor-prefixed system selectors (`:root`, `*`, `html`, `body`)

**Step 2. Collect all class usages from templates / JS**

Check ALL of these sources:

| Source | What to look for |
|---|---|
| HTML attribute | `class="..."`, `className="..."` |
| JSX dynamic | `className={styles.foo}`, `` className={`btn ${mod}`} `` |
| JS DOM API | `classList.add/remove/toggle/replace/contains(...)` |
| JS strings | `querySelector('.foo')`, `getElementsByClassName('foo')` |
| CSS Modules | `styles.foo`, `styles['foo-bar']` |
| Template literals | `` `icon icon-${name}` `` → flag: dynamic, do not touch |
| Data-attribute triggers | `[data-class="foo"]` in JS |
| Tests | `getByRole`, `getByTestId`, `.toHaveClass('foo')` |

**Step 3. Build the matrix**

```
for each class from CSS:
  if no match found in templates/JS → deletion candidate
  if only match is inside a comment → deletion candidate
  if match is inside a template literal → FLAG: dynamic, skip
```

**Step 4. Verify before deleting**

Before removing a class, ask:
- Is it a utility class (`.mt-4`, `.hidden`, `.sr-only`)? → probably needed, search HTML
- Is it a CSS-only state (`.is-open`, `.active`)? → may be toggled via JS `.className =`
- Is it from a design system / third-party library? → do not touch
- Is there a similar name with a typo (`.buttton`, `.primray`)? → suggest rename

---

### 1.2 Class rename artifacts

**Symptom:** old name in CSS, new name in template (or vice versa).

**Detection algorithm:**

1. Find a class used in JS/HTML that has no matching rule in CSS → candidate: "used but not declared"
2. Find a class declared in CSS with no match in JS/HTML → candidate: "declared but not used"
3. Apply Levenshtein distance or semantic comparison between the two lists:
   - `.btn-primary` (CSS) ↔ `.buttonPrimary` (JS) — rename artifact
   - `.card__header` (CSS) ↔ `.card-header` (JS) — BEM → kebab convention change
   - `.isActive` (CSS) ↔ `.is-active` (JS) — camelCase → kebab

**Rename rules:**
- If CSS is one file but JS has many references → rename in CSS
- If CSS is generated (CSS Modules, Tailwind JIT) → rename in JS
- Always rename atomically: find all occurrences via `grep -rn "name" src/`

---

### 1.3 CSS custom properties (variables)

**Collecting declarations:**
```
Pattern: /--([\w-]+)\s*:/g  →  inside :root, :host, or any block
```

**Collecting usages:**
```
Pattern 1 (CSS):    /var\(--([\w-]+)/g
Pattern 2 (JS get): /getPropertyValue\(['"`]--([\w-]+)/g
Pattern 3 (JS set): /setProperty\(['"`]--([\w-]+)/g
Pattern 4 (JS read): /style\.--([\w-]+)/g  ← rare but possible
```

**Three types of problems:**

```
A. Declared, never used:
   :root { --old-brand-color: #ff0000; }  ← nobody calls it
   → Delete

B. Used, never declared:
   color: var(--button-hover-color);  ← not in :root
   → Find where it should have come from (rename?) or add it

C. Overridden, but the override is never read:
   :root { --gap: 1rem; }
   .card { --gap: 2rem; color: var(--gap); }  ← --gap = 2rem here
   .sidebar { color: var(--gap); }             ← --gap = 1rem here (correct, but check intent)
```

**Special case — cascading override:**
The variable is "used", but its local override inside a component is never read by anyone → dead override.

---

## Part 2. JavaScript / TypeScript

### 2.1 Dead variables and constants

**Level 1 — local variables**

```javascript
// Declared, assigned, never read:
const result = fetchData();  // result never appears below

// Re-assigned without the first value being read:
let config = defaultConfig;
config = userConfig;  // first assignment is dead
```

Algorithm:
1. Find all `const/let/var` declarations in scope
2. For each — find all reads (not assignments) within that scope
3. If zero reads → dead variable

**Level 2 — exported constants**

```typescript
// constants.ts
export const API_TIMEOUT = 5000;      // used
export const OLD_API_URL = '/api/v1'; // imported nowhere
export const MAX_RETRIES = 3;         // used
```

Algorithm:
1. Collect all `export const/function/class` from the file
2. Grep the whole project for `import { OLD_API_URL }` or `constants.OLD_API_URL`
3. No matches → dead export

**Exceptions — do not delete without extra verification:**
- `export default` — may be used via dynamic import
- Re-exports (`export { x } from './x'`) — may be part of the public API
- Constants in `index.ts` / `public-api.ts` — these are library interfaces
- Variables prefixed with `_` — explicitly marked as intentionally unused

---

### 2.2 Dead functions

**Search patterns:**

```
1. Declared, never called:
   function formatDate(d) { ... }  // no formatDate( anywhere in the project

2. Called, but return value always ignored:
   validateInput(data);  // returns boolean that nobody reads
   → not dead, but suspicious — may be an effect function, may be a bug

3. No-op wrapper:
   const getUser = (id) => fetchUser(id);  // just proxies
   → deletion candidate + replace all calls with fetchUser(id) directly

4. Duplicate function:
   function parseDate(s) { ... }       // 40 lines
   function parseDateString(s) { ... } // 38 lines, does the same thing
   → find, compare, keep one
```

**Algorithm for dead functions:**
1. Collect all function declarations (including arrow functions assigned to variables)
2. For each — search for `functionName(` across the project (excluding the declaration itself)
3. Account for passing as an argument: `arr.map(formatDate)` → alive
4. Account for object spread: `{ ...helpers, formatDate }` → alive
5. Check tests: `describe('formatDate', ...)` → alive (covered by tests)

---

### 2.3 Dead imports

**Simple case:**
```javascript
import { formatDate, parseDate } from './utils';
// parseDate is never used in this file
```

**Complex case — side-effect imports:**
```javascript
import './polyfills';          // side-effect, do not touch
import 'reflect-metadata';     // side-effect for decorators, do not touch
import styles from './Card.module.css';  // used via styles.xxx
```

**Algorithm:**
1. For each named import → search for usages in the file body
2. For default imports → same
3. Side-effect imports (no `{...}` and no `x from`) → always flag as "verify manually", never auto-delete
4. Type-only imports (`import type { Foo }`) → dead if the type is never used in an annotation

---

### 2.4 TypeScript — dead types and interfaces

```typescript
// Declared, never used:
interface OldUserShape {
  id: number;
  name: string;
}

// Used only inside the file where it's declared — fine
// Exported but never imported anywhere — deletion candidate

// Partial artifact — fields that never exist on real objects:
interface User {
  id: number;
  name: string;
  legacyToken?: string;  // optional, never assigned anywhere
}
```

**Algorithm for interface fields:**
1. Find all places where the `User` type is used
2. Find all assignments of `legacyToken` → if zero → dead field
3. Find all reads of `user.legacyToken` → if zero → confirmed dead

---

### 2.5 Dead conditional branches

```javascript
// Constant condition:
const DEBUG = false;
if (DEBUG) {
  console.log('...');  // never executes
}

// Condition always true by types:
function process(items: string[]) {
  if (items === null) { ... }  // string[] can never be null in TS strict mode
}

// Unreachable default:
type Status = 'active' | 'inactive';
switch (status) {
  case 'active': ...
  case 'inactive': ...
  default:
    throw new Error('Unknown');  // never reached if union is exhaustive
}
```

**Algorithm:**
1. Find `if (CONSTANT_NAME)` where the constant is explicitly `true` or `false`
2. Find comparisons that TypeScript types make impossible
3. Mark `default` in a switch as "verify" when the union type is fully exhausted

---

## Part 3. Logical chains — end-to-end analysis

### 3.1 What is a logical chain

It is the complete path of data or a dependency from its source to its effect:

```
Example 1 — prop-drilling chain:
  API response → parseUser() → User type → UserCard props → avatar prop → <img src>

Example 2 — CSS chain:
  design token (--color-brand) → button.css → .btn-primary → <button class="btn-primary"> → visible color

Example 3 — event chain:
  click → handleClick() → dispatch(updateUser) → reducer → state.user → re-render
```

A **chain break** is the point where data "drops": assigned but never read further, or read from a source that doesn't exist.

---

### 3.2 Chain reconstruction algorithm

For any suspicious entity (class, variable, function):

```
1. WHERE does it come from?
   - Declared locally
   - Imported
   - Received as a prop / argument
   - Retrieved from an API / store

2. WHERE does it go?
   - Passed further (into a function, component, DOM)
   - Returned from a function
   - Assigned to another variable
   - Used in a condition
   - Rendered / applied

3. IS THERE AN EFFECT?
   - Mutates DOM / styles
   - Fires a request
   - Mutates state
   - Logs / emits metrics
   - Returns a value that someone reads
```

**Conclusion:**
- If answers to 2 and 3 are "nowhere" and "no" → delete
- If answer to 1 is "from nowhere" but 2 and 3 are present → find the source (rename artifact)
- If chain exists but is tangled → rename refactor, not deletion

---

### 3.3 Patterns specific to AI refactoring

AI refactoring produces characteristic artifacts. Know their patterns:

**Pattern 1: Rename on one end only**
```css
/* original */ .card-wrapper { ... }
/* AI renamed in JS */ → className="cardContainer"
/* CSS unchanged  */ .card-wrapper { ... }   ← dead
/* CSS never created */ .cardContainer { ... } ← missing
```

**Pattern 2: Inlined function left behind**
```javascript
// AI inlined the logic of parseDate into 3 places
// but the original parseDate function was never removed
function parseDate(s) { ... }  // dead
```

**Pattern 3: Wrapper variable chain**
```javascript
const userData = user;           // original name
const currentUser = userData;    // AI added
const activeUser = currentUser;  // AI added again
// activeUser is used everywhere below
// userData and currentUser are dead intermediaries
```

**Pattern 4: Duplicated type**
```typescript
// original
type ApiUser = { id: string; name: string; }
// AI created a new one
interface User { id: string; name: string; }
// both exist, only User is used
// ApiUser — dead type
```

**Pattern 5: Zombie comment**
```javascript
// TODO: remove after migration to v2
const legacyAdapter = ...  // migration happened long ago, legacy lives on
```

---

### 3.4 Decision matrix

| Situation | Action |
|---|---|
| Declared, zero usages, simple case | Delete |
| Declared, zero usages, exported | Check public API → delete if not API |
| Used, not declared | Find similar name → rename, or add declaration |
| Two similar names, one dead | Levenshtein / semantics → propose merge |
| Dynamic name (`styles[name]`, template literal) | Flag as "dynamic" → do not touch, note in report |
| Side-effect import | Do not touch → flag for review |
| Dead branch with `console.log` / `debugger` | Delete with confidence |
| Dead branch with business logic | Propose only, do not auto-delete |
| Type / interface with no usages | Check re-export → delete if none |
| CSS variable with no usages | Delete if not in a public design token file |

---

## Part 4. Instructions for the AI agent

### 4.1 File analysis order

```
1. Identify file type: CSS / SCSS / TS / JS / JSX / TSX / HTML
2. Extract all entities with their position (line:column)
3. For each entity — classify:
   a. Declared only
   b. Used only
   c. Both declared and used
   d. Neither (inside a comment / string literal)
4. Build a list of candidates with their problem type
5. For each candidate — run the checks from Parts 1–3
6. Produce a report with action: delete | rename | investigate | keep
```

### 4.2 Report format

For each finding, output this structure:

```
FINDING:    <entity name>
TYPE:       css-class | css-var | js-var | js-function | ts-type | js-import
FILE:       path/to/file.css:42
PROBLEM:    unused | missing | renamed | duplicated | dead-branch
CHAIN:      <source> → <destination> → <effect>  (or "chain does not close")
ACTION:     delete | rename <old> → <new> | investigate
REASON:     <one sentence explaining why>
CONFIDENCE: high | medium | low
```

Example:

```
FINDING:    .card-wrapper
TYPE:       css-class
FILE:       src/components/Card/Card.module.css:17
PROBLEM:    unused
CHAIN:      Card.module.css → [no incoming references]
ACTION:     investigate → likely rename .card-wrapper → .cardContainer
REASON:     Card.tsx uses styles.cardContainer, but only .card-wrapper is declared in CSS — classic rename artifact
CONFIDENCE: high
```

---

### 4.3 Check priority order

Run checks in this order (simplest to most complex):

```
1. Dead imports (safest to delete)
2. Local variables with no reads
3. CSS classes with no HTML/JS usages
4. CSS variables with no var(...)
5. Exported functions with no external calls
6. Exported types with no imports
7. Dead conditional branches
8. Duplicate functions / types
```

---

### 4.4 What to NEVER delete automatically

```
- Anything tagged @public, @api, @deprecated (scheduled for removal)
- Side-effect imports (import 'x')
- Variables prefixed with _ (intentionally unused)
- Classes that may arrive from outside (SSR, CMS, markdown)
- Dynamically constructed names (template literals, computed property names)
- *.d.ts files entirely (type declarations)
- Re-exports in index.ts / public-api.ts
- Anything in node_modules, dist, build
- Configuration objects (may be read via reflection)
- Classes used in e2e tests (data-testid — do not touch even if absent from unit tests)
```

---

### 4.5 Grep commands for manual verification

When confidence is `medium` or `low` — provide the user with commands to verify:

```bash
# Find all usages of a class
grep -rn "card-wrapper" src/ --include="*.{js,jsx,ts,tsx,html,vue,svelte}"

# Find all imports of a symbol
grep -rn "import.*formatDate" src/

# Find all var() calls for a CSS variable
grep -rn "var(--color-brand)" src/

# Find all calls to a function
grep -rn "parseDate(" src/ --include="*.{js,ts,jsx,tsx}"

# Find similar names (for rename artifacts)
grep -rn "cardContainer\|card-container\|card_container\|cardWrapper\|card-wrapper" src/

# Check if an export is used outside its module
grep -rn "from.*utils" src/ | grep "OLD_API_URL"
```

---

## Part 5. Pre-deletion checklist

Before removing any entity, verify:

- [ ] Project-wide search (`grep -rn`) returned zero results
- [ ] Entity is not part of the public API (`index.ts`, `package.json` exports)
- [ ] No dynamic references exist (template literals, `require(variable)`)
- [ ] Not referenced in tests (unit, e2e, storybook)
- [ ] Not referenced in documentation (README, JSDoc, comments)
- [ ] Git blame shows it was not added very recently (may have uncommitted usages)
- [ ] Build passes after deletion (`npm run build` / `tsc --noEmit`)
- [ ] All tests are green after deletion

---

## Appendix: quick regex patterns

```
CSS classes (declared):         /(?<![a-zA-Z0-9_-])\.([a-zA-Z_-][a-zA-Z0-9_-]*)\s*[{,]/g
CSS variables (declaration):    /--([\w-]+)\s*:/g
CSS variables (usage):          /var\(--([\w-]+)/g
JS named import:                /import\s*\{([^}]+)\}/g
JS default import:              /import\s+(\w+)\s+from/g
TS interface / type:            /(?:interface|type)\s+(\w+)/g
JS function declaration:        /function\s+(\w+)\s*\(/g
JS arrow function in const:     /const\s+(\w+)\s*=\s*(?:async\s*)?\(/g
JS class declaration:           /class\s+(\w+)/g
Dead branch (constant bool):    /if\s*\(\s*(true|false)\s*\)/g
Unused assignment:              /(?:const|let|var)\s+(\w+)\s*=(?!=)/g  + check reads
```

---

*Version: 1.0 | Purpose: instruction set for an AI agent working with legacy or AI-refactored codebases*
