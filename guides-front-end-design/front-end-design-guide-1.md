# Front-End Design Guide
## A Complete System of Design and Layout Principles

> This document is a system of principles, not a collection of solutions.
> Every principle is a verification question you can ask about any interface.
> Specific implementations change (frameworks, design tokens, component libraries) —
> principles do not.

---

## Document Structure

```
I.    Perception            — how the brain processes visual information
II.   Hierarchy             — order of importance and attention
III.  Typography            — text as a system
IV.   Color                 — a semantic layer, not decoration
V.    Space                 — grid, rhythm, density
VI.   Component             — the unit of interface
VII.  Interaction           — states, feedback, animation
VIII. Accessibility         — not an option, a requirement
IX.   CSS Architecture      — the structure of style code
X.    Component Engineering — isolation, state, security
XI.   Information Architecture — content structure and navigation
XII.  Responsive Design     — adapting to any screen and container
XIII. Usability Heuristics  — practical principles of ease of use
XIV.  Design Systems        — scaling design as an engineering discipline
XV.   Specialized Patterns  — forms, tables, dashboards, e-commerce
XVI.  Verification          — how to audit any UI
```

---

## I. Perception

Design is the management of attention. Everything else is secondary.

### I.1 Pre-attentive Attributes

The brain processes certain visual properties before conscious perception (~150–200 ms).
These are the most powerful tools of hierarchy:

| Attribute | Strength | Application |
|---|---|---|
| Color (hue) | High | Status indicators, category tags |
| Size | High | Heading levels, importance signals |
| Contrast (luminance) | High | Primary vs. secondary content |
| Motion | Very High | System alerts, progress indicators |
| Shape | Medium | Icons, buttons vs. input fields |
| Orientation | Medium | Arrows, dividers |
| Position | Medium | Navigation, labels |

**Rule:** do not combine more than 2–3 pre-attentive attributes to emphasize a single element.
When everything shouts, nothing does.

### I.2 Gestalt Laws

The brain automatically groups visual elements. Violating these laws creates
cognitive dissonance — the interface feels "uncomfortable" for no obvious reason.

**Proximity**
Elements placed close together are perceived as a group.
→ The gap between groups must be larger than the gap within a group.
→ Check: remove colors and borders — does grouping survive through spacing alone?

**Similarity**
Elements sharing the same properties are perceived as related.
→ Same function = same appearance. Different function = different appearance.
→ Violation: a button and a text link look identical — their function becomes ambiguous.

**Common Region**
Elements inside the same container are perceived as a group.
→ Every additional container (border, background) fires a cognitive signal: "boundary here."
→ Unnecessary containers = unnecessary cognitive effort. Minimize.

**Continuity**
The eye follows a line or curve.
→ Horizontal rows read left to right. Vertical columns read top to bottom.
→ A broken Tab order violates the continuity law in the accessibility domain.

**Closure**
The brain completes unfinished shapes.
→ Slightly clipped content (peek pattern) signals that scrolling is possible.
→ Structure can be communicated with fewer borders.

**Figure-Ground**
An element is perceived either as an object (figure) or as context (ground).
→ Modals work by suppressing the ground (overlay).
→ Cards work by lifting off the ground (shadow or contrast).

**Focal Point**
An element that breaks the pattern immediately captures attention.
→ This is the CTA principle: one point of contrast against a calm background.

### I.3 Scanning Patterns

**F-pattern** (text-heavy interfaces, lists):
The user makes a horizontal sweep at the top, then moves vertically down the left edge,
with short horizontal "probes" further down.
→ Critical information belongs in the first words of each paragraph and the first lines of the page.

**Z-pattern** (sparse interfaces, landing pages):
The eye travels the Z diagonal — top-left → top-right → bottom-left → bottom-right.
→ Logo on the left, CTA on the right, logical connections along the diagonal.

**Gutenberg Diagram** (complex layouts with multiple blocks):
The primary optical area (top-left) and the terminal area (bottom-right) are the strongest zones.
→ Content entry and the final CTA belong in these zones.

### I.4 Working Memory

Human working memory holds 4 ± 1 meaningful units at once (Cowan, 2001).
The classic "7 ± 2" (Miller) applies chunking — grouping items into units.

**Rules:**
- Show no more than 5–7 options in a single menu without sub-groups.
- Group related form fields into labeled semantic blocks.
- Pagination exists for cognitive relief, not only for performance.
- **Hick's Law:** decision time grows logarithmically with the number of options.
  `T = a + b × log₂(n + 1)`
  → Progressive disclosure is the primary tool against Hick's Law.

---

## II. Hierarchy

Hierarchy answers one question: "what should the user notice first?"

### II.1 Visual Weight

Visual weight is the relative "heaviness" of an element in perception.
It is controlled in decreasing order of power:

```
Size > Contrast > Color Saturation > Shape > Texture > Position
```

**The Single Dominant principle:**
At every visual level (page → section → card → row) there must be
one and only one heaviest element.
Two equally dominant elements cancel each other out and destroy hierarchy.

**The 3-Second Rule:**
Close your eyes. Open them for 3 seconds. Close. What did you retain?
If you retained 3+ distinct things — hierarchy is not established.

### II.2 Types of Hierarchy

**Informational hierarchy:** what matters more semantically.
**Visual hierarchy:** what is more prominent perceptually.
**Functional hierarchy:** primary → secondary → tertiary actions.

All three must align. If the most important information is visually weaker than
secondary content — that is a violation.

### II.3 Action Hierarchy

Any interface has at most three levels of actions:

| Level | Example | Visual Treatment |
|---|---|---|
| Primary | "Pay", "Create" | Filled button, high contrast |
| Secondary | "Edit", "Filter" | Outlined / ghost button |
| Tertiary | "Cancel", "Details" | Text link or icon button |

**Rule:** there must not be two primary actions on the same screen.
If two actions feel equally important — one of them is not actually primary.

### II.4 Progressive Disclosure

Show only what is needed right now. Everything else — on demand.

```
Level 0: always visible          — core content
Level 1: one click to open       — additional options, filters
Level 2: requires explicit intent — advanced settings, fine details
```

Violation: showing everything at once (toolbar with 12+ options, form with 20+ fields).
Solution: accordion, dropdown, offcanvas, drawer, modal — all are progressive disclosure structures.

---

## III. Typography

Typography is not font selection. It is a system of relationships between text elements.

### III.1 Modular Scale

Text sizes must form a mathematical progression.
Standard ratios:

| Name | Ratio | Best For |
|---|---|---|
| Major Second | 1.125 | Dense UI (tables, dashboards) |
| Minor Third | 1.2 | Most components |
| Major Third | 1.25 | Documents, articles |
| Perfect Fourth | 1.333 | Landing pages, marketing |
| Golden Ratio | 1.618 | Large headings, hero sections |

**Rule:** no more than 3–4 size levels in a single component.
More levels → hierarchy breaks down.

### III.2 Line Height (Leading)

```
Body text:        line-height 1.4–1.6
Headings:         line-height 1.1–1.25
Captions, meta:   line-height 1.3–1.4
```

Too tight: text suffocates. Too loose: paragraphs lose cohesion.

### III.3 Measure (Line Length)

The optimal line length is 45–75 characters for body text.
Below 45: the eye wraps too frequently — fatiguing.
Above 75–85: the eye loses the line on return.

Tool: `max-width: 65ch` physically constrains measure in CSS.

### III.4 Typographic Rhythm

Vertical rhythm is a consistent vertical spacing step based on a base unit.
If the base unit = 4px:

```
Margin between paragraphs: 16px (4 × 4)
Margin below a heading:    24px (6 × 4)
Card padding:              16px or 24px
```

Chaotic vertical spacing is the most common sign of an absent system.

### III.5 Typographic Contrast — Beyond Size

Contrast is achieved through combinations of: size / weight / style / color / capitalization.
You do not need to increase size to emphasize — changing weight alone is sufficient.

**Check:** remove size differences. Does hierarchy survive through weight and color?
If not — the system is incomplete.

### III.6 Semantic Text Roles

Every text element belongs to a defined role. Roles must be visually distinguishable
and semantically consistent throughout the interface:

| Role | HTML | Typical Use |
|---|---|---|
| Display / Hero | `<h1>` | Page-level titles, hero text |
| Heading | `<h2>`–`<h4>` | Section and card titles |
| Body | `<p>` | Main readable content |
| Label | `<label>`, `<dt>` | Field labels, metadata keys |
| Caption | `<figcaption>`, `<small>` | Image captions, helper text |
| Code | `<code>`, `<pre>` | Technical content |
| Overline | `<span>` (utility class) | Category labels above headings |

**Rule:** a role must not be used for its visual appearance but for its semantic meaning.
Using `<h3>` because it looks the right size is a violation. Set the size via CSS.

---

## IV. Color

Color is the last tool of hierarchy, not the first.

### IV.1 WCAG Contrast

Every text element against its background must pass contrast verification:

| Content Type | Minimum (AA) | Recommended (AAA) |
|---|---|---|
| Body text (< 18pt) | 4.5 : 1 | 7 : 1 |
| Large text (≥ 18pt or ≥ 14pt bold) | 3 : 1 | 4.5 : 1 |
| UI components (borders, icons) | 3 : 1 | — |
| Decorative elements | — | — |

Formula: `contrast ratio = (L1 + 0.05) / (L2 + 0.05)`, where L = relative luminance.

### IV.2 Color as a Semantic Layer

Color must carry functional meaning, not just aesthetic value:

```
Reserved status semantics:
  Green  → success, availability, positive state
  Red    → error, danger, destructive action
  Yellow → warning, pending state
  Blue   → information, link, interactive element

Brand color → identity elements (logo, primary CTA)
```

**Color independence rule:** information must not be conveyed by color alone.
Remove color — meaning must survive through shape, text, or icon.
(Violation: a red/green dot with no label — invisible to color-blind users.)

### IV.3 Palette Discipline

**The 60-30-10 rule:**
- 60% — dominant neutral (backgrounds, surfaces)
- 30% — secondary (text, borders, dividers)
- 10% — accent (CTA, active states, links)

More than 3–4 distinct colors in a component signals an absent system.

### IV.4 Color Token Architecture

Color must never be hardcoded. The three-level token system:

```
Level 1 — Primitives (raw palette):
  --color-blue-500: #3B82F6
  --color-red-500:  #EF4444

Level 2 — Semantic tokens (what it means):
  --color-primary:  var(--color-blue-500)
  --color-error:    var(--color-red-500)
  --color-text:     var(--color-neutral-900)
  --color-surface:  var(--color-neutral-0)

Level 3 — Component tokens (where it is used):
  --btn-primary-bg:     var(--color-primary)
  --input-error-border: var(--color-error)
```

Switching themes = changing level 2 only. Components are untouched.

### IV.5 Themes

A theme is a named set of semantic token overrides. The component layer is unaware of the active theme.

```css
/* Light theme (default) */
:root {
  --color-surface:    #ffffff;
  --color-text:       #111827;
  --color-primary:    #3B82F6;
}

/* Dark theme */
[data-theme="dark"] {
  --color-surface:    #111827;
  --color-text:       #F9FAFB;
  --color-primary:    #60A5FA;
}

/* Brand override */
[data-theme="brand-green"] {
  --color-primary:    #16A34A;
}
```

**Rule:** `prefers-color-scheme` sets the default; `data-theme` on `<html>` allows user override.
Never read `prefers-color-scheme` in JavaScript to conditionally change colors — use CSS.

---

## V. Space

### V.1 The Base Unit

All spacing must be a multiple of a single base unit.
Standard: 4px or 8px.

```
Scale on a 4px base:
  xs:  4px   — tight gaps, thin dividers
  sm:  8px   — inner element padding (icon button)
  md:  16px  — card padding, group gaps
  lg:  24px  — between component sections
  xl:  32px  — between major blocks
  2xl: 48px  — between page sections
  3xl: 64px+ — hero sections, large separations
```

**Check:** does every margin and padding divide evenly by the base unit?
If not — there are magic numbers in the code.

### V.2 White Space as an Active Element

White space is not emptiness — it is an active design element.
Functions of white space:
- Creates groups (proximity)
- Gives important content room to breathe
- Improves text readability
- Signals quality (luxury perception)

**Common mistake:** "fill the empty space" with additional elements.
Correct approach: first ask — why does this element exist, not where to put it.

### V.3 Content Density

Interfaces vary in density by task type:

| Type | Density | Examples |
|---|---|---|
| Content consumption | Low | Articles, product pages |
| Data monitoring | High | Dashboards, data tables |
| Data entry | Medium | Forms |
| Navigation | Medium | Menus, catalogs |

Density must be consistent within a component type. You cannot mix a sparse header
with a dense main content area.

### V.4 The Grid

The grid is not a constraint — it is an alignment system.

**Columns:** contain content. Width is percentage-based or fixed.
**Gutters:** spacing between columns. Fixed (px), not percentage-based.
**Margins:** spacing from the viewport edge. Adapt at breakpoints.

**Alignment principle:** every element aligns to at least one grid axis.
A randomly positioned element is an error.

### V.5 Optical vs Mathematical Alignment

Mathematical alignment places elements on the same axis.
Optical alignment corrects for perceptual illusions created by shape.

```
Icons next to text: visually center on the text cap-height, not the bounding box.
Rounded elements: need 1–2px inward compensation — their corners are invisible.
All-caps text: needs less letter-spacing than lowercase for the same optical density.
```

**Rule:** mathematical alignment is the starting point. Optical correction is the refinement.
Never skip mathematical alignment — optical corrections are small adjustments, not substitutes.

---

## VI. Component

A component is a self-contained unit of interface. It solves one problem and is unaware of the outside context.

### VI.1 Atomic Design

```
Atoms      — base HTML elements: button, input, icon, label
Molecules  — groups of atoms: search bar (input + button + icon)
Organisms  — groups of molecules: header, form, review card
Templates  — arrangement of organisms: page layout
Pages      — templates with real content
```

**Rule:** a component must not "know" where on the page it lives.
Violation: `margin-top: 40px` inside a component — that is knowledge of external context.

### VI.2 Component Isolation

**CSS isolation:** all component styles are scoped to its root element.
```css
/* Correct: */
.card { ... }
.card__title { ... }

/* Incorrect: */
h2 { color: blue; } /* global side effect */
```

**JS isolation (Law Zero):** a component does not use global ID hooks.
```js
// Incorrect:
document.getElementById('submit-btn')

// Correct:
this.root.querySelector('[data-action="submit"]')
```

**Namespace isolation:** all custom data attributes, CSS variables, and classes carry a component prefix.
```
Bad:  data-filter="5"          --color-primary
Good: data-reviews-filter="5"  --reviews-star-color
```

### VI.3 The Component State Machine

Every interactive component is a finite state machine. States must be explicit and complete:

```
Required states for most components:
  idle       — resting, initial state
  hover      — cursor over the element
  focus      — keyboard focus
  active     — pressed / interacting
  disabled   — unavailable
  loading    — awaiting a response
  error      — something went wrong
  success    — completed / confirmed
  empty      — no data to display
```

**Rule:** if a state is visually indistinguishable from another — it is not implemented,
it is merely absent. Violation: a disabled button looks the same as an active one.

### VI.4 Component API Design

A component's API is its contract with the rest of the system.
Well-designed APIs are explicit, minimal, and composable.

**Props (attributes / parameters):**
```
Required props:    carry no default — a missing value is an error.
Optional props:    always have a sensible default.
Boolean props:     presence = true (disabled, readonly, required).
Enum props:        use a closed set of string values (size="sm"|"md"|"lg").
```

**Variants vs modifiers:**
```
Variant   — a distinct visual identity (primary, secondary, ghost, destructive).
            Variants are mutually exclusive.
Modifier  — adjusts one dimension (size, density, shape).
            Modifiers can be combined.

Bad:  <Button type="large-primary-rounded" />
Good: <Button variant="primary" size="lg" shape="rounded" />
```

**Slots / children:**
A component accepts content through a slot when the inner structure varies.
A component accepts data through props when the inner structure is fixed.

### VI.5 Responsive Design

A component must work correctly across a range of container sizes, not only at fixed breakpoints.
Mobile-first: start from the smallest container, expand with `min-width`.

```css
/* Incorrect — desktop-first: */
.grid { display: grid; grid-template-columns: 1fr 1fr 1fr; }
@media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }

/* Correct — mobile-first: */
.grid { display: grid; grid-template-columns: 1fr; }
@media (min-width: 768px) { .grid { grid-template-columns: 1fr 1fr 1fr; } }
```

---

## VII. Interaction

### VII.1 Laws of Interaction

**Fitts's Law:**
Time to acquire a target = f(distance / target size).
→ Minimum interactive element sizes:
  - Apple HIG: 44 × 44 pt
  - Google Material: 48 × 48 dp
  - WCAG 2.5.5 (AAA): 44 × 44 CSS px
→ Frequently used elements must be large and close.
→ Destructive actions (delete, remove) must be small and distant.

**Hick's Law:**
Already described in section I.4. Applied to interaction:
→ A toolbar with 10+ options is a violation. Solution: grouping + progressive disclosure.
→ A form with 15+ fields is a violation. Solution: steps (wizard), logical sections.

**Serial Position Effect:**
The first and last items in a list are best remembered (primacy + recency effects).
→ CTA button at the end of a form is correct (recency).
→ The most important menu item belongs first or last.

### VII.2 Feedback

Nielsen's Heuristic #1: visibility of system status.
Every user action must have an immediate, visible response:

```
< 100ms    — "instant" — no additional visual feedback needed
100–300ms  — visual feedback required (hover state, ripple effect)
300–1000ms — loading indicator required (spinner, skeleton screen)
> 1s       — progress bar + ability to cancel
> 10s      — notification + ability to leave and return
```

**Types of feedback:**
- Color / icon — immediate (hover, pressed state)
- Microanimation — confirms the action (like, add to cart)
- Toast / snackbar — async result (saved, network error)
- Skeleton screen — content loading
- Progress bar — long operations

### VII.3 Animation

Animation must be motivated. Every animation answers the question: "what does it explain?"

**Functions of animation:**
1. Orientation — shows where an element came from / went (modal, drawer)
2. Relationship — shows the connection between states (expand, accordion)
3. Confirmation — confirms completion of an action (checkmark, shake on error)
4. Preloading — makes waiting tolerable (skeleton, spinner)
5. Delight — adds character (bounce, spring — only where contextually appropriate)

**Animation parameters:**
```
Micro-interactions (hover, toggle):  100–200ms,  ease-in-out
Element entrance:                    200–300ms,  ease-out
Element exit:                        150–200ms,  ease-in
Complex transitions (page):          300–500ms,  custom spring
```

Longer than 500ms — animation stops feeling responsive.
Animation without function (for its own sake) is parasitic.

**prefers-reduced-motion:** all animations must be suppressible:
```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

### VII.4 Microinteraction Anatomy (Dan Saffer)

```
Trigger   — what initiates the interaction (click, hover, data load)
Rules     — what happens (logic)
Feedback  — how it is shown (visual, sound, haptics)
Loops     — does it repeat, when does it end
```

A good microinteraction is transparent — users do not think about it, they simply feel that
"everything works correctly."

### VII.5 Form Interaction

Forms are the highest-friction point in any interface. Every field is a cost; minimize cost.

**Field design rules:**
- Each field has a visible label — never rely on placeholder text as the only label.
- Placeholder text is an example, not a label: it disappears on input and breaks recall.
- Group related fields visually and semantically (`<fieldset>` + `<legend>`).
- Show optional fields, not required ones — default expectation is required.
- Input type must match the data: `type="email"`, `type="tel"`, `type="number"`.

**Validation strategy:**
```
On submit:       always validate the entire form.
Inline (live):   only after the user has left the field (blur), not while typing.
Inline (error):  re-validate on input after an error has been shown — give immediate relief.
```

**Error messages must be:**
1. Specific — "Email must include @" not "Invalid email."
2. Located — directly below the offending field, not in a summary banner alone.
3. Actionable — tell the user what to do, not just what went wrong.
4. Polite — never blame the user ("You entered the wrong date").

**Input assistance:**
- Autocomplete: use correct `autocomplete` attribute values (`name`, `email`, `current-password`).
- Masks: format as the user types for structured data (phone, card numbers) — only when format is unambiguous.
- Inline constraints: show character limits, allowed formats, and password strength before submission.

### VII.6 Error Recovery

An error that cannot be undone is a design failure, not a user failure.

```
Undo:           preferred over confirmation dialogs for reversible actions.
Confirmation:   for irreversible, high-impact actions only (delete, payment).
                Must describe what will be lost, not just ask "Are you sure?"
Retry:          network errors must always offer a retry path.
Autosave:       long forms must save state periodically — never lose user work.
```

**Confirmation dialog anatomy:**
```
Title:   "Delete 'Project Alpha'?" — specific, not generic.
Body:    "This will permanently remove all files and cannot be undone."
Actions: [Cancel] [Delete] — destructive action on the right, lower visual weight.
```

**Rule:** the cancel action must always be easier to reach than the destructive action.

---

## VIII. Accessibility

Accessibility is not a feature. It is a baseline quality requirement, like the absence of compile errors.

### VIII.1 The Four WCAG Principles (POUR)

**Perceivable:**
- Alt text for images
- Captions for video
- Sufficient color contrast
- Text is not embedded in images

**Operable:**
- All functionality is accessible via keyboard
- No focus traps (except modals — where they are correct)
- Sufficient time to interact
- No flashing content > 3 times/sec

**Understandable:**
- Page language is declared (`lang="en"`)
- Component behavior is predictable
- Form errors describe the problem and the solution
- All fields have labels

**Robust:**
- Valid HTML
- Compatibility with assistive technology (AT)
- Correct ARIA roles

### VIII.2 Semantic HTML — The Foundation

Rule: if a native HTML element exists for the purpose — use it, not a `div`.

```
Interactivity: <button>, <a>, <input>, <select>, <textarea>
Structure:     <header>, <main>, <nav>, <aside>, <footer>, <section>, <article>
Typography:    <h1>–<h6>, <p>, <ul>, <ol>, <li>, <blockquote>
Data:          <table>, <caption>, <thead>, <tbody>, <th scope>
Media:         <figure>, <figcaption>, <picture>
```

Native elements give for free: keyboard interaction, focus management, ARIA roles, browser defaults.
A `<div>` + JS handler requires all of this to be added manually.

### VIII.3 ARIA — Supplement, Not Replacement

ARIA extends semantics where native HTML is insufficient. The first rule of ARIA:
> If you can use a native HTML element with the required semantics — use it.

```
Roles:        role="dialog", role="list", role="alert", role="tabpanel"
States:       aria-expanded, aria-checked, aria-pressed, aria-selected
Properties:   aria-label, aria-labelledby, aria-describedby, aria-controls
Live regions: aria-live="polite", aria-live="assertive"
```

**aria-label vs aria-labelledby:**
- `aria-labelledby` references existing visible text — preferred.
- `aria-label` for elements without a visible label (icon-only button, search without a visible heading).

### VIII.4 Focus Management

```
Focus indicator:  always visible and high-contrast (:focus-visible)
Focus order:      matches logical DOM order (tabindex="0" only when necessary)
Focus trap:       modals and dialogs — focus does not escape while open
Focus return:     on modal close — focus returns to the trigger element
Skip links:       <a href="#main">Skip to content</a> — the first element on the page
```

`tabindex > 0` is almost always a mistake. Reconsider the DOM structure instead.

---

## IX. CSS Architecture

CSS is not a stylesheet. It is a language for describing a design system.

### IX.1 The Cascade and Specificity

Specificity, from low to high:
```
Tag selectors:        0-0-1   (h1, p, div)
Classes, attributes:  0-1-0   (.card, [type="text"])
IDs:                  1-0-0   (#header)
Inline styles:        1-0-0-0
!important:           outside the system
```

**The minimum specificity principle:**
Write styles with the lowest necessary specificity.
- Do not use ID selectors for styling.
- Do not use `!important` except in utility classes (the final layer).
- Do not nest selectors deeper than 2–3 levels.

### IX.2 The Token System

Three-level architecture (see section IV.4):

```
Global tokens (primitives):
  All possible values in the design system.
  Never used directly in components.

Semantic tokens (decisions):
  Values are bound to their context of use.
  This is what a theme changes.

Component tokens:
  A specific component references semantic tokens.
  Overridden only for local variants.
```

**Rule:** a token always references a token from the level above — never a primitive directly.
```css
/* Bad: */
.button-primary { background: #3B82F6; }

/* Good: */
.button-primary { background: var(--button-primary-bg); }
--button-primary-bg: var(--color-primary);
--color-primary: var(--color-blue-500);
--color-blue-500: #3B82F6;
```

### IX.3 Scoping Strategies

**BEM (Block Element Modifier):**
```css
.card { }                   /* Block */
.card__title { }            /* Element */
.card--featured { }         /* Modifier */
.card__title--truncated { } /* Element + Modifier */
```

**Utility-first (Tailwind approach):**
Atomic classes applied directly in HTML. No custom CSS unless necessary.
Strength: no specificity conflicts, easy to read.
Weakness: HTML becomes verbose, patterns are harder to extract.

**CSS Modules / Scoped styles:**
Each component receives unique hashed class suffixes. No collisions.
Strength: complete isolation.
Weakness: harder to override from a theme.

**Component-scoped (explicit prefix approach):**
All child classes carry the component prefix.
```css
.reviews-container { }                         /* Root — CSS scope anchor */
.reviews-container .reviews-card { }           /* Children — always through the root */
```

### IX.4 Cascade Layers

`@layer` gives explicit control over the order in which rule groups apply,
eliminating specificity wars between resets, design systems, and utilities:

```css
@layer reset, base, tokens, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer tokens {
  :root { --color-primary: #3B82F6; }
}

@layer components {
  .btn { background: var(--color-primary); }
}

@layer utilities {
  .sr-only { position: absolute; width: 1px; clip: rect(0,0,0,0); }
}
```

Rules in a later-declared layer always win over rules in earlier layers,
regardless of specificity. `!important` reverses layer order.

### IX.5 CSS Principles

**DRY through custom properties, not through duplication:**
A repeated value → token. A repeated pattern → class.

**Work with the browser, not against it:**
Flexbox and Grid solve 95% of layout problems.
`position: absolute` — only when the meaning is genuinely absolute.
Float in 2025 — only for text wrapping.

**Logical properties instead of physical:**
```css
/* Physical — breaks in RTL layouts: */
padding-left: 16px; margin-right: 8px;

/* Logical — works in any writing direction: */
padding-inline-start: 16px; margin-inline-end: 8px;
```

---

## X. Component Engineering

### X.1 Separation of Concerns

```
HTML  — structure and semantics
CSS   — appearance and animation
JS    — behavior and state
```

JS must not write inline styles (except CSS custom properties).
CSS must not contain logic (except structural selectors: `:has()`, `:is()`, `:where()`).
HTML must not contain presentation attributes (`style="..."`, deprecated `align`, `bgcolor`).

### X.2 HTML Hooks

Separate by attribute type:

```
class="..."         — style hooks (CSS targets)
id="..."            — ARIA anchors (for=, aria-labelledby=), URL anchors; one instance per page
data-ref="..."      — JS references to DOM nodes (cached at initialization)
data-action="..."   — JS event triggers (delegated listener on the root)
data-state="..."    — state visible to both JS and CSS
data-*-custom="..."  — data attributes with a component prefix
```

Prohibited: `js-*` classes as event hooks — an outdated pattern.
Prohibited: IDs as CSS selectors — breaks specificity.
Prohibited: mixing roles (id used for CSS and ARIA and JS simultaneously) — causes collisions.

### X.3 Event Delegation

```js
// Bad — a listener on every element:
document.querySelectorAll('.btn').forEach(btn =>
  btn.addEventListener('click', handler)
);

// Good — one listener on the root:
root.addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  switch (btn.dataset.action) { ... }
});
```

Benefits: works with dynamically added elements, single registration point,
easily cleaned up via AbortController.

### X.4 AbortController for Cleanup

```js
_bindEvents() {
  const sig = { signal: this._abort.signal };
  this._root.addEventListener('click', this._onClick.bind(this), sig);
  document.addEventListener('keydown', this._onKey.bind(this), sig);
}

destroy() {
  this._abort.abort(); // one line cleans up all listeners
}
```

### X.5 Security

**XSS (Cross-Site Scripting):**
```js
// Dangerous — interpolation directly into innerHTML:
el.innerHTML = `<p>${userInput}</p>`;

// Safe — escape before insertion:
_esc(s) { return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
el.innerHTML = `<p>${this._esc(userInput)}</p>`;

// Or use textContent for plain text:
el.textContent = userInput;
```

**URL validation:**
```js
_isSafeUrl(url) {
  return typeof url === 'string' && /^https?:\/\//i.test(url);
}
```

**Input validation:**
Any data from external sources (API, localStorage, URL parameters) must be validated
before use. Object keys must be checked against an allowlist (whitelist).

### X.6 Render Performance

**Layout thrashing:**
```js
// Bad — interleaving reads and writes forces reflow:
el.style.height = el.offsetHeight + 'px';
el2.style.height = el2.offsetHeight + 'px';

// Good — batch all reads first, then all writes:
const h1 = el.offsetHeight;
const h2 = el2.offsetHeight;
el.style.height = h1 + 'px';
el2.style.height = h2 + 'px';
```

**Batch DOM updates:**
```js
// Bad — multiple insertions into the live DOM:
items.forEach(item => list.appendChild(createEl(item)));

// Good — one DocumentFragment:
const frag = document.createDocumentFragment();
items.forEach(item => frag.appendChild(createEl(item)));
list.replaceChildren(frag);
```

**CSS transitions over JS animation:**
The browser optimizes `transform` and `opacity` through the compositor — no reflow or repaint.
Safe to animate: `transform`, `opacity`.
Do not animate: `width`, `height`, `top`, `left`, `margin` — they trigger layout.

---

## XI. Information Architecture

Information architecture answers one question: "how does a user find what they need?"

### XI.1 Content Hierarchy

Every content system has a structure. That structure must be explicit and consistent:

```
Page level:     the top-level concept this URL represents.
Section level:  a coherent sub-topic within the page.
Entity level:   a single item — product, article, record.
```

**Rules:**
- A page answers exactly one question at its top level.
- A section contains only content that belongs to its heading.
- Entities share a consistent structure: same fields in the same order.
- Depth beyond 3 levels signals an architecture problem, not a navigation problem.

**Card sorting** is the empirical method: give users category labels and ask them to group content.
The result reveals the user's mental model, not the organization's internal taxonomy.

### XI.2 Navigation Systems

Navigation is the product of the architecture, not a design element.
Fix the architecture first; navigation then becomes obvious.

**Global navigation:** present on every page. Contains the top 5–7 sections of the site.
**Local navigation:** within a section. Tabs, sidebar links, in-page jumps.
**Contextual navigation:** related content links. "See also", "Next step", "Breadcrumb".
**Utility navigation:** account, search, language, settings.

**Breadcrumbs:**
```
Home > Products > Cameras > Mirrorless
```
- Each level is a link, except the current page.
- Represent the IA hierarchy, not the browser history.
- Required when depth > 2 levels.

**Tabs:**
- Use for peer-level content that the user switches between.
- Do not use for sequential steps (use a stepper instead).
- Maximum 7 tabs; beyond that, use a dropdown or sidebar navigation.

### XI.3 Search

Search is an escape hatch for when navigation fails. It is not a replacement for navigation.

**Search placement:** globally accessible, typically in the header. Keyboard shortcut: `⌘K` / `Ctrl+K`.

**Query handling:**
- Zero results: show suggestions, related terms, browse links. Never an empty page.
- Typo tolerance: fuzzy matching for queries with ≥ 3 characters.
- Autocomplete: show suggestions after 2+ characters; debounce input (300ms).
- Results: show the matching term in context (bold the matched substring).

**Scoped search:** filter by content type before or after the query — do not force the user to choose scope first.

### XI.4 Taxonomy and Classification

Taxonomy determines how content is categorized. Classification is the assignment of items to categories.

**Types of classification:**
- **Hierarchical:** one parent per item (file system, product category tree).
- **Faceted:** multiple independent dimensions simultaneously (size + color + brand in e-commerce).
- **Tag-based:** flat, user-defined labels. Flexible but inconsistent.

**Faceted classification rules:**
- Each facet should reduce the result set meaningfully.
- Show item counts per facet value — zero-result paths are invisible walls.
- Allow multiple values within a facet (OR logic), single value across facets (AND logic).
- "Clear all filters" must always be reachable without reloading.

### XI.5 Naming and Labeling

Labels are the user's map. Incorrect labels cause confusion regardless of structure quality.

**Rules:**
- Use the user's vocabulary, not the organization's internal terminology.
- Labels must be unique — two different sections cannot share the same name.
- Action labels must be specific verbs: "Save draft" not "OK", "Delete account" not "Confirm".
- Consistency: the same thing must always be called the same thing across the interface.

**Test:** card sorting and tree testing reveal whether labels match user mental models.
**Never name by feature:** "Analytics" says nothing — "View reports" describes the action.

---

## XII. Responsive and Adaptive Design

A responsive interface works correctly at any size. An adaptive interface works optimally at defined sizes.
Both are required; they solve different problems.

### XII.1 Mobile-First as a Design Constraint

Mobile-first is not a CSS rule — it is a design methodology.
Start with the smallest screen and the least available space. Every element must justify its presence.
Expansion to larger screens adds, never removes.

**Why mobile-first works:**
1. Forces prioritization — there is no room for everything.
2. Progressive enhancement — more capable screens get more features.
3. Performance — CSS for mobile loads first; desktop enhancements load conditionally.

```css
/* Mobile-first in practice: */
.nav { display: none; }                  /* hidden on mobile */
@media (min-width: 768px) {
  .nav { display: flex; }               /* visible on tablet+ */
}
```

### XII.2 Breakpoints

Breakpoints must be based on content, not on device dimensions.
A breakpoint is the point at which the current layout can no longer accommodate the content.

**Common reference breakpoints (not rules — observe your content):**
```
xs:   < 480px   — single-column, no secondary content
sm:  480–767px  — single-column with some two-column patterns
md:  768–1023px — two-column layouts, secondary nav visible
lg: 1024–1279px — multi-column, sidebars, expanded navigation
xl: 1280px+     — maximum content width, large-screen optimizations
```

**Rule:** define breakpoints in a single source of truth — CSS custom properties or a shared token file.
Never hardcode a pixel value in more than one place.

### XII.3 Container Queries

Container queries adapt a component to its container's size, not the viewport's size.
This enables true component reuse across different layout contexts.

```css
/* Define a containment context: */
.card-grid {
  container-type: inline-size;
  container-name: grid;
}

/* Component adapts to its container, not the viewport: */
.card { display: block; }

@container grid (min-width: 400px) {
  .card { display: flex; }
}
```

**When to use container queries vs media queries:**
- Media query: the layout of the page changes (columns, navigation mode).
- Container query: a component's internal layout changes based on available space.

### XII.4 Fluid Typography and Spacing

Fixed breakpoints produce jumps. Fluid scaling produces smooth transitions.

```css
/* Fluid font size: scales linearly between 16px (320px viewport) and 20px (1280px viewport) */
:root {
  font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
}

/* Fluid spacing: */
.section {
  padding-block: clamp(2rem, 5vw, 5rem);
}
```

`clamp(min, preferred, max)` is the correct tool. It requires no media queries and
scales proportionally within defined bounds.

### XII.5 Touch Interface Design

Touch targets follow physical laws: a finger cannot be as precise as a cursor.

**Size requirements:**
```
Minimum tap target:    44 × 44 CSS px (WCAG 2.5.5 AAA)
Recommended:           48 × 48 CSS px (Material Design)
Minimum spacing between adjacent targets: 8px
```

**Touch-specific interaction patterns:**
- Swipe: directional, horizontal for carousels/tabs; vertical for menus.
- Long press: reveals secondary actions — always paired with a visible alternative.
- Pinch/zoom: never disable on content pages (`user-scalable=no` is an accessibility violation).
- Pull-to-refresh: a native-feeling pattern; do not implement custom unless necessary.

**Hover states on touch:**
Touch devices do not have persistent hover. Any information only exposed on hover is invisible on mobile.
→ All hover-only content (tooltips, reveal buttons) must have a tap-accessible alternative.

---

## XIII. Usability and UX Heuristics

Heuristics are not rules — they are lenses for evaluating interfaces.
An interface is usable when it matches how users think, not how the system works.

### XIII.1 Nielsen's Ten Heuristics

**1. Visibility of system status**
The system always keeps users informed about what is going on, through appropriate feedback within a reasonable time.
→ Every async operation shows a loading indicator. Every completed action is confirmed.

**2. Match between system and real world**
The system speaks the users' language — words, phrases, and concepts familiar to the user, rather than system-oriented terms.
→ "Save" not "Persist to storage." "Delete" not "Remove entity."

**3. User control and freedom**
Users often choose system functions by mistake. They need an "emergency exit."
→ Undo for every destructive action. Cancel for every modal and multi-step flow.

**4. Consistency and standards**
Users should not have to wonder whether different words, situations, or actions mean the same thing.
→ One label per concept. One pattern per interaction type. Follow platform conventions.

**5. Error prevention**
Even better than good error messages is a careful design that prevents problems from occurring.
→ Disable unavailable actions visually. Confirm irreversible actions. Validate inline.

**6. Recognition over recall**
Minimize the user's memory load. Objects, actions, and options should be visible.
→ Show recently used items. Keep context visible while completing a task. Use icons with labels.

**7. Flexibility and efficiency of use**
Accelerators — unseen by the novice user — allow experts to work faster.
→ Keyboard shortcuts for frequent actions. Bulk operations for power users. Saved searches and filters.

**8. Aesthetic and minimalist design**
Every extra unit of information in a dialogue competes with relevant information and diminishes its relative visibility.
→ Remove every element that does not contribute to the primary task on this screen.

**9. Help users recognize, diagnose, and recover from errors**
Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution.
→ "Payment declined: your card's billing zip code doesn't match. Update your card." not "Error 422."

**10. Help and documentation**
Even though it is better if the system can be used without documentation, it may be necessary to provide help.
→ Help is available in context — not only in a manual. It is searchable and focused on tasks.

### XIII.2 Consistency

Consistency is predictability applied to design.

**Types of consistency:**
- **Visual consistency:** the same components look the same everywhere.
- **Functional consistency:** the same components behave the same everywhere.
- **External consistency:** familiar patterns from the platform ecosystem are respected.
- **Internal consistency:** within the product, identical concepts are always expressed identically.

**The consistency test:**
A new team member arrives. They learn one part of the interface.
Do they correctly predict how another part works without being told?
If not — consistency is absent.

**Dangerous exceptions:**
Every exception to a pattern requires the user to learn a new rule.
One exception is a special case. Three exceptions destroy the pattern.
Audit before adding exceptions.

### XIII.3 Error Prevention

Prevention is superior to recovery. Design before the error occurs.

**Strategies:**

| Strategy | Example |
|---|---|
| Eliminate the wrong path | Disable "Submit" until required fields are filled |
| Show constraints early | "Password must be 8+ characters" before typing begins |
| Default to safe | Delete confirmation off by default; opt-in to "skip confirmation" |
| Confirmation for destructive actions | "Delete 47 files?" with specific count |
| Format enforcement | Date picker instead of free text for dates |
| Undo instead of confirm | "Message sent. Undo" — lower friction, same safety |

**The poka-yoke principle (mistake-proofing):**
Make correct behavior the path of least resistance.
Make incorrect behavior require extra effort.

### XIII.4 Mental Models

A mental model is what the user believes about how the system works.
An interface succeeds when its model matches the user's model.

**Types of mismatch:**
- The user expects deletion to be reversible; it is permanent.
- The user expects "Archive" and "Delete" to differ; they do the same thing.
- The user expects their work to be autosaved; it is not.

**Closing the gap:**
1. Learn the user's existing mental model through user research — do not assume.
2. Meet the model where possible (use familiar metaphors: shopping cart, inbox, folders).
3. Where the model must differ, teach explicitly — tooltips, empty states, onboarding.

**Affordances:**
Visual properties that suggest how an element is used.
- Raised, bordered box → button (pressable).
- Underlined blue text → link (navigable).
- Grabber handle → draggable.

Violating affordances creates invisible interfaces — elements that exist but are not discovered.

---

## XIV. Design Systems

A design system is a product that serves product teams.
It is not a library of components — it is a shared language for decisions.

### XIV.1 What a Design System Contains

```
Foundations:  tokens (color, type, space), principles, brand guidelines
Components:   documented, versioned, accessible UI components
Patterns:     compositions of components solving recurring UX problems
Content:      voice, tone, writing style guidelines
Process:      contribution model, review process, change management
```

A component library without documentation is not a design system — it is a collection.

### XIV.2 Token Architecture at Scale

Design tokens are the connective tissue between design tools and code.
The three-level model (primitive → semantic → component) enables:

- **Theming:** swap semantic layer → entire product rebrands.
- **Dark mode:** semantic layer maps to different primitives under `[data-theme="dark"]`.
- **Density:** a "compact" token set reduces spacing values throughout.

**Token naming convention:**
```
Format:  [category]-[concept]-[variant]-[state]
Example: color-action-primary-hover
         space-component-card-padding-x
         typography-body-size
```

Avoid abbreviations. Tokens are documentation — legibility beats brevity.

### XIV.3 Component Documentation Standards

A component without documentation is incomplete. Each component entry must include:

```
Purpose:     what problem this component solves, and when to use it.
Anatomy:     labeled diagram of all parts.
Variants:    visual examples of every variant and modifier.
States:      visual examples of idle, hover, focus, disabled, loading, error.
Usage:       dos and don'ts with concrete examples.
Accessibility: keyboard behavior, ARIA attributes, screen reader output.
Code:        copy-paste ready implementation with props documented.
Changelog:   version history of breaking and non-breaking changes.
```

**The "when not to use" section is as important as "when to use."**
Without it, components are misapplied and the system loses coherence.

### XIV.4 Governance

A design system without a governance model drifts into inconsistency.

**Contribution models:**
```
Centralized:   one team owns everything. High consistency, low velocity.
Federated:     each product team contributes; one team reviews. Balanced.
Open:          anyone contributes with lightweight review. High velocity, lower consistency.
```

**Decision record:**
Every significant change to the system should be documented with:
- What changed.
- Why it changed.
- What alternatives were considered.
- Migration path for existing consumers.

### XIV.5 Versioning and Migration

**Semantic versioning for design systems:**
```
MAJOR (2.0.0) — breaking change: component API changed, token renamed.
MINOR (1.1.0) — new component or variant; backward compatible.
PATCH (1.0.1) — bug fix, visual correction; backward compatible.
```

**Breaking change policy:**
- Announce at least one minor version in advance.
- Provide a codemod or migration guide.
- Deprecate before removing — at least one major version between deprecation and removal.

**Deprecation pattern:**
```
Phase 1 (current minor):    Mark as deprecated in documentation + console warning.
Phase 2 (next minor):       Add visual deprecation indicator in Storybook.
Phase 3 (next major):       Remove. Migration guide is required.
```

---

## XV. Specialized Interface Patterns

### XV.1 Forms

Complex forms are multi-step experiences, not single pages.

**Single-step forms (≤ 7 fields):**
- All fields visible at once.
- Submit at the bottom.
- Inline validation on blur.

**Multi-step forms (wizards):**
```
Stepper:      shows total steps and current position.
Progress:     step N of M visible at all times.
Navigation:   back is always possible; forward requires validation.
State:        completed steps are preserved when navigating back.
Final step:   shows a summary before irreversible submission.
```

**Field ordering principle:**
Easy → hard. Personal info before payment. Required before optional.
The hardest field placed last causes the highest abandonment rate.

**Logical field grouping:**
```html
<fieldset>
  <legend>Shipping address</legend>
  <!-- address fields -->
</fieldset>
<fieldset>
  <legend>Payment details</legend>
  <!-- payment fields -->
</fieldset>
```

### XV.2 Data Tables

A data table is an interface for exploring, comparing, and acting on structured data.

**Required capabilities for any data table:**

| Capability | When Required |
|---|---|
| Column sorting | When order matters |
| Column filtering | When dataset > 20 rows |
| Pagination or infinite scroll | When dataset > 50 rows |
| Row selection (checkbox) | When bulk actions exist |
| Column resizing | When content width varies |
| Sticky header | When table height > viewport |
| Empty state | Always |

**Sorting:**
- One column sorted at a time by default; multi-sort only if genuinely needed.
- Clicking a sorted column reverses order; clicking again removes sort.
- Sort direction indicator on the active column only.

**Density:**
Tables for data monitoring use compact density (32px row height).
Tables for reading use regular density (48px row height).
Never mix densities in the same table.

**Accessibility for tables:**
```html
<table>
  <caption>Monthly sales report, Q3 2025</caption>
  <thead>
    <tr>
      <th scope="col" aria-sort="ascending">Month</th>
      <th scope="col">Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">July</th>
      <td>$42,000</td>
    </tr>
  </tbody>
</table>
```

### XV.3 Dashboards

A dashboard is a display of the information required to achieve one or more goals,
consolidated on a single screen so the information can be monitored at a glance.

**Dashboard design principles:**

**1. Define the primary question.**
Every dashboard answers one primary question. Secondary questions are secondary.
Example: "Is this service healthy right now?" not "Everything we can measure about this service."

**2. Information hierarchy on a dashboard:**
```
Level 1 (glance): KPI cards — number + trend + context. Seen in 2 seconds.
Level 2 (scan):   Charts — patterns over time. Seen in 10 seconds.
Level 3 (read):   Tables and detail — precise values on demand.
```

**3. Chart selection:**

| Goal | Chart Type |
|---|---|
| Change over time | Line chart |
| Part-to-whole | Pie / donut (≤ 5 parts), stacked bar |
| Comparison across categories | Bar chart (horizontal for long labels) |
| Correlation between two variables | Scatter plot |
| Distribution | Histogram |
| Geospatial data | Map |

**Rule:** a pie chart with more than 5 segments is unreadable. Use a bar chart.

**4. Color on dashboards:**
- Use one color for all bars in a single chart, unless color encodes a different variable.
- Status colors (green/red) must be consistent with the global semantic palette.
- Do not use rainbow palettes — they imply a gradient of value where none exists.

**5. Empty and loading states:**
A dashboard without data must explain why, with a path to resolution.
A loading dashboard shows skeleton cards — not a spinner in the center of the page.

### XV.4 E-Commerce Interfaces

E-commerce interfaces mediate a commercial transaction. Every friction point has a measurable cost.

**Product catalog:**
```
Filters:     persistent sidebar on desktop; bottom sheet on mobile.
Grid:        2 columns on mobile, 3–4 on desktop. Card aspect ratio consistent.
Card:        image, name, price, primary differentiator (rating, badge). One CTA.
Sorting:     relevance (default), price asc/desc, newest, top rated.
```

**Product detail page (PDP):**
```
Above the fold:  image gallery, name, price, key variant selectors, primary CTA.
Below the fold:  description, specifications, reviews, related products.
```

**Rule:** the primary CTA ("Add to cart", "Buy now") must be visible without scrolling
on desktop. On mobile — sticky at the bottom of the viewport.

**Cart:**
- Always accessible without leaving the current page (slide-out drawer preferred).
- Shows item count in the navigation at all times.
- Line item includes: image, name, variant, quantity control, price, remove action.
- Order summary is sticky on desktop during checkout.

**Checkout funnel:**
```
Step 1: Contact info / Sign in
Step 2: Shipping address + method
Step 3: Payment
Step 4: Review + Place order
Step 5: Confirmation
```

**Checkout friction rules:**
- Guest checkout must always be available.
- Never require account creation before purchase.
- Autofill must work: `autocomplete` attributes are mandatory on every field.
- Payment errors must be specific: "Card declined: insufficient funds" not "Payment failed."
- The confirmation page must show: order number, items, total, estimated delivery, next steps.

---

## XVI. Verification

A set of questions for auditing any interface.

### XVI.1 Perceptual Audit

```
□ 3-second rule: what is remembered first after 3 seconds of viewing?
  → It must be the main content / primary action.

□ Hierarchy: does each section have one dominant element?
  → Are there no two equally "heavy" elements side by side?

□ Grouping: remove borders and color — does structure survive through spacing alone?
  → Does proximity create groups without decoration?

□ Scannability: is critical information in the first words of each line?
  → Is the F-pattern respected for text-heavy content?

□ Unnecessary containers: is every card/box/border justified?
  → No borders added purely for aesthetics without a grouping function?
```

### XVI.2 Typography Audit

```
□ Scale: are there ≤ 4 size levels in the component?
□ Rhythm: are vertical spacings multiples of the base unit?
□ Measure: is text block width ≤ 75 characters?
□ Size-free hierarchy: remove size differences — does hierarchy survive through weight/color?
□ Contrast: do all texts pass WCAG AA (minimum 4.5:1)?
□ Semantic roles: is each text element using the correct role (heading not styled as label)?
```

### XVI.3 Color Audit

```
□ Contrast: do all text and UI elements pass WCAG checks?
□ Independence: does meaning survive without color?
□ Semantics: is color used consistently (green always = success)?
□ Tokens: are all colors expressed through variables, zero hardcoded values?
□ Palette: no more than 3–4 colors in a component?
□ Theme: does the component render correctly in light and dark themes?
```

### XVI.4 Spatial Audit

```
□ Base unit: are all margins and paddings multiples of the base unit?
□ No magic numbers: no values like 13px, 37px, 5px?
□ Mobile: are touch targets ≥ 44px × 44px?
□ Density: is it consistent throughout the component?
□ Optical alignment: are rounded/icon elements visually centered, not only mathematically?
```

### XVI.5 Component Audit

```
□ States: are idle, hover, focus, disabled, loading, error, and empty all implemented?
□ Isolation: does the component set no external margins?
□ Prefix: do all data attributes and CSS variables carry a namespace?
□ Scope: are all CSS rules anchored to the root element of the component?
□ No global ID hooks in JS?
□ No inline styles (except CSS custom properties)?
□ Variants: are all documented variants visually distinguishable?
□ API: are props explicit, typed, and documented?
```

### XVI.6 Accessibility Audit

```
□ Semantics: are all interactive elements native button/a/input?
□ ARIA: are all necessary aria-label/labelledby/describedby attributes present?
□ Contrast: does everything pass WCAG AA?
□ Keyboard: is all functionality reachable via Tab/Enter/Escape/Arrow keys?
□ Focus: is the :focus-visible style visible and high-contrast?
□ Live regions: is dynamic content announced to screen readers?
□ Focus order: is it logical and does it match the visual order?
□ Target sizes: are touch targets ≥ 44px?
```

### XVI.7 CSS Architecture Audit

```
□ Specificity: no ID selectors in CSS?
□ !important: only in utility classes, as the final layer?
□ Tokens: all values expressed through CSS custom properties?
□ Themability: changing variables changes the entire appearance without editing rules?
□ Scope: every child selector is anchored to the root class?
□ Global utilities: not embedded inside component CSS?
□ Cascade layers: declared and ordered correctly?
□ Logical properties: no hard-coded left/right in directional contexts?
```

### XVI.8 Engineering Audit

```
□ Separation: CSS-only animations for transform/opacity?
□ Delegation: one listener on the root, not one per element?
□ XSS: all user content escaped before innerHTML?
□ URL validation: all external URLs verified before use in src/href?
□ Cleanup: all listeners removed on component destruction?
□ DOM batching: multiple updates via DocumentFragment?
□ No layout thrashing: reads and writes are not interleaved?
```

### XVI.9 Performance Audit

Core Web Vitals are the browser's measurement of perceived performance:

| Metric | Measures | Target |
|---|---|---|
| LCP (Largest Contentful Paint) | Loading performance | ≤ 2.5s |
| INP (Interaction to Next Paint) | Responsiveness | ≤ 200ms |
| CLS (Cumulative Layout Shift) | Visual stability | ≤ 0.1 |

**Common CLS causes and fixes:**
```
Image without dimensions:  always set width + height on <img> or use aspect-ratio.
Web font swap:             use font-display: optional or swap + preload the font.
Dynamic content injection: reserve space for async content with skeleton screens.
```

**Common LCP causes and fixes:**
```
Render-blocking resources:  defer or async non-critical JS; preload critical CSS.
Unoptimized images:         use WebP/AVIF; set correct sizes attribute; use srcset.
Slow server response:       TTFB > 600ms requires server-side optimization, not frontend.
```

**INP audit:**
```
□ Long tasks (> 50ms) broken up with scheduler.yield() or setTimeout chunking?
□ Input handlers free of synchronous DOM measurements?
□ Third-party scripts loaded asynchronously?
```

### XVI.10 Design Review Checklist

Before shipping any interface:

```
INFORMATION ARCHITECTURE
  □ The page answers exactly one primary question
  □ Navigation labels match user vocabulary
  □ All paths lead somewhere — no dead ends

INTERACTION
  □ Every action has feedback within 100ms
  □ Every error state is designed, not just the happy path
  □ Undo or confirmation exists for every destructive action

RESPONSIVE
  □ Tested at 320px, 768px, 1280px, 1440px
  □ Touch targets ≥ 44px on all interactive elements
  □ No content clipped or overflowing at any tested width

DESIGN SYSTEM
  □ Only system components are used — no one-offs without documented reason
  □ All tokens from the correct semantic level
  □ Changelog entry written if component is modified
```

---

## Appendix: One-Page Checklist

```
PERCEPTION
  □ 3-second rule: the most important thing is first
  □ One dominant element per section
  □ Grouping through space, not only through borders

HIERARCHY
  □ One primary action per screen
  □ Progressive disclosure for complex interfaces
  □ Informational = Visual = Functional hierarchy

TYPOGRAPHY
  □ ≤ 4 size levels in a component
  □ Vertical rhythm on the base unit
  □ Measure ≤ 75 characters
  □ Semantic roles — not chosen by size

COLOR
  □ All text: WCAG AA (4.5:1)
  □ UI elements: WCAG AA (3:1)
  □ Meaning survives without color
  □ All colors through tokens
  □ Light and dark themes verified

SPACE
  □ All spacings are multiples of the base unit
  □ Touch targets ≥ 44px
  □ Optical alignment verified for icons and rounded elements

COMPONENT
  □ All states implemented
  □ No external margins
  □ Namespace prefix on everything
  □ API documented

INFORMATION ARCHITECTURE
  □ Page answers one question
  □ Labels match user vocabulary
  □ Navigation depth ≤ 3 levels

INTERACTION
  □ Every action has immediate feedback
  □ Animation is motivated by function
  □ prefers-reduced-motion respected
  □ Error messages: specific, located, actionable
  □ Undo or confirmation for destructive actions

ACCESSIBILITY
  □ Native HTML for all interactive elements
  □ All fields have labels
  □ Full keyboard navigation
  □ :focus-visible style is present

CSS
  □ No IDs in CSS
  □ No !important (except utils)
  □ All styles scoped to the root
  □ Tokens at three levels
  □ Cascade layers declared
  □ Logical properties in directional contexts

ENGINEERING
  □ All user input escaped
  □ One delegated listener
  □ Cleanup on component destruction

PERFORMANCE
  □ LCP ≤ 2.5s
  □ INP ≤ 200ms
  □ CLS ≤ 0.1
  □ Images have width + height set

DESIGN SYSTEMS
  □ No undocumented one-off components
  □ Changelog entry for every modification
  □ Deprecation policy followed
```

---

*This document describes principles — they do not become obsolete when frameworks change.*
*Bootstrap, Tailwind, React, Vue are tools for implementing the principles,*
*not the principles themselves.*
