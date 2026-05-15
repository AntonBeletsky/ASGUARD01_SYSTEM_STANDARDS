# Front-End Design Guide
## A Complete System of Design and Layout Principles

> This document is a system of principles, not a collection of solutions.
> Every principle is a verification question you can ask about any interface.
> Specific implementations change (frameworks, design tokens, component libraries) —
> principles do not.

---

## Document Structure

```
I.   Perception          — how the brain processes visual information
II.  Hierarchy           — order of importance and attention
III. Typography          — text as a system
IV.  Color               — a semantic layer, not decoration
V.   Space               — grid, rhythm, density
VI.  Component           — the unit of interface
VII. Interaction         — states, feedback, animation
VIII.Accessibility       — not an option, a requirement
IX.  CSS Architecture    — the structure of style code
X.   Component Engineering — isolation, state, security
XI.  Verification        — how to audit any UI
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

### VI.4 Responsive Design

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

### IX.4 CSS Principles

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

## XI. Verification

A set of questions for auditing any interface.

### XI.1 Perceptual Audit

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

### XI.2 Typography Audit

```
□ Scale: are there ≤ 4 size levels in the component?
□ Rhythm: are vertical spacings multiples of the base unit?
□ Measure: is text block width ≤ 75 characters?
□ Size-free hierarchy: remove size differences — does hierarchy survive through weight/color?
□ Contrast: do all texts pass WCAG AA (minimum 4.5:1)?
```

### XI.3 Color Audit

```
□ Contrast: do all text and UI elements pass WCAG checks?
□ Independence: does meaning survive without color?
□ Semantics: is color used consistently (green always = success)?
□ Tokens: are all colors expressed through variables, zero hardcoded values?
□ Palette: no more than 3–4 colors in a component?
```

### XI.4 Spatial Audit

```
□ Base unit: are all margins and paddings multiples of the base unit?
□ No magic numbers: no values like 13px, 37px, 5px?
□ Mobile: are touch targets ≥ 44px × 44px?
□ Density: is it consistent throughout the component?
```

### XI.5 Component Audit

```
□ States: are idle, hover, focus, disabled, loading, error, and empty all implemented?
□ Isolation: does the component set no external margins?
□ Prefix: do all data attributes and CSS variables carry a namespace?
□ Scope: are all CSS rules anchored to the root element of the component?
□ No global ID hooks in JS?
□ No inline styles (except CSS custom properties)?
```

### XI.6 Accessibility Audit

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

### XI.7 CSS Architecture Audit

```
□ Specificity: no ID selectors in CSS?
□ !important: only in utility classes, as the final layer?
□ Tokens: all values expressed through CSS custom properties?
□ Themability: changing variables changes the entire appearance without editing rules?
□ Scope: every child selector is anchored to the root class?
□ Global utilities: not embedded inside component CSS?
```

### XI.8 Engineering Audit

```
□ Separation: CSS-only animations for transform/opacity?
□ Delegation: one listener on the root, not one per element?
□ XSS: all user content escaped before innerHTML?
□ URL validation: all external URLs verified before use in src/href?
□ Cleanup: all listeners removed on component destruction?
□ DOM batching: multiple updates via DocumentFragment?
□ No layout thrashing: reads and writes are not interleaved?
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

COLOR
  □ All text: WCAG AA (4.5:1)
  □ UI elements: WCAG AA (3:1)
  □ Meaning survives without color
  □ All colors through tokens

SPACE
  □ All spacings are multiples of the base unit
  □ Touch targets ≥ 44px

COMPONENT
  □ All states implemented
  □ No external margins
  □ Namespace prefix on everything

INTERACTION
  □ Every action has immediate feedback
  □ Animation is motivated by function
  □ prefers-reduced-motion respected

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

ENGINEERING
  □ All user input escaped
  □ One delegated listener
  □ Cleanup on component destruction
```

---

*This document describes principles — they do not become obsolete when frameworks change.*
*Bootstrap, Tailwind, React, Vue are tools for implementing the principles,*
*not the principles themselves.*
