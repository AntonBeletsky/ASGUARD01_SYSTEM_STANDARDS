# CSS GUIDE — PART 16
## Chapters 219–228

---

## 219. CSS TRIGONOMETRIC FUNCTIONS

```css
/* ─── Analog clock hands, positioned with rotate() driven by trig-based angles ─── */
.clock {
  --clock-size: 200px;
  width: var(--clock-size);
  height: var(--clock-size);
  border-radius: 50%;
  background: var(--color-surface);
  border: 4px solid var(--color-border-strong);
  position: relative;
}

.clock-hand {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: 0 0;
  background: var(--color-text);
  border-radius: var(--radius-full);
}
.clock-hand--hour   { width: calc(var(--clock-size) * 0.28); height: 4px; rotate: calc(var(--angle-hour, 0deg) - 90deg); }
.clock-hand--minute { width: calc(var(--clock-size) * 0.38); height: 3px; rotate: calc(var(--angle-minute, 0deg) - 90deg); }
.clock-hand--second {
  width: calc(var(--clock-size) * 0.42);
  height: 1px;
  background: var(--color-danger-500);
  rotate: calc(var(--angle-second, 0deg) - 90deg);
}

/* ─── Radial menu: items placed directly on a circle using sin()/cos() ─── */
.radial-menu {
  --radius: 100px;
  --count: 6;
  position: relative;
  width: calc(var(--radius) * 2 + 48px);
  height: calc(var(--radius) * 2 + 48px);
}

.radial-menu-item {
  --i: 0; /* set per item: 0, 1, 2 … count-1, e.g. inline style="--i: 2" */
  --angle: calc((360deg / var(--count)) * var(--i));
  position: absolute;
  top: 50%;
  left: 50%;
  width: 48px;
  height: 48px;
  margin: -24px;
  translate:
    calc(cos(var(--angle) - 90deg) * var(--radius))
    calc(sin(var(--angle) - 90deg) * var(--radius));
  border-radius: 50%;
  background: var(--color-surface);
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: scale var(--duration-fast) var(--ease-bounce);
}
.radial-menu-item:hover { scale: 1.15; }

/* ─── Satellite positioned directly via trig functions (not a rotate() trick) ─── */
.orbit { position: relative; width: 240px; height: 240px; }
.orbit-track { position: absolute; inset: 0; border: 1px dashed var(--color-border); border-radius: 50%; }

.orbit-body {
  --angle: 0deg; /* animate this custom property 0deg → 360deg to move the body */
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--color-accent);
  top:  calc(50% + sin(var(--angle)) * 110px - 8px);
  left: calc(50% + cos(var(--angle)) * 110px - 8px);
}

/* ─── Per-letter wave using sin() and an --index set on each <span> ─── */
.wave-text span {
  display: inline-block;
  --index: 0; /* set per letter, e.g. via nth-child in JS or inline style */
  translate: 0 calc(sin(var(--index) * 40deg) * 10px);
}
```

---

## 220. CALC-SIZE() & INTERPOLATE-SIZE

```css
/* ─── Enable animating to/from intrinsic keywords like `auto` ─── */
:root {
  interpolate-size: allow-keywords;
}

/* ─── Accordion panel that animates height: auto smoothly, no JS measuring ─── */
.accordion-panel {
  height: 0;
  overflow: hidden;
  transition: height var(--duration-normal) var(--ease-out);
}
.accordion-panel[data-open="true"] {
  height: auto; /* interpolate-size makes this directly animatable */
}

/* ─── calc-size() adds extra room on top of the intrinsic size ─── */
.expandable-card {
  block-size: calc-size(auto, size);
  overflow: hidden;
  transition: block-size var(--duration-slow) var(--ease-out);
}
.expandable-card.collapsed { block-size: 4.5rem; }
.expandable-card.peek      { block-size: calc-size(auto, size + var(--space-4)); }

/* ─── Auto-growing sidebar that keeps a minimum width while animating ─── */
.sidebar-flex {
  inline-size: calc-size(auto, max(size, 240px));
  overflow: hidden;
  transition: inline-size var(--duration-normal) var(--ease-out);
}

/* ─── Dropdown list without a hardcoded max-height ─── */
.dropdown-list {
  height: 0;
  overflow: hidden;
  transition: height var(--duration-normal) var(--ease-out);
}
.dropdown[open] .dropdown-list { height: auto; }

/* ─── Notification banner that grows to fit newly-appended content ─── */
.banner-growing {
  block-size: calc-size(auto, size);
  transition: block-size var(--duration-normal) var(--ease-out);
  overflow: hidden;
}

/* ─── Fallback for browsers without calc-size()/interpolate-size support ───
   the old approach measured content height in JS and set an explicit
   pixel value before transitioning — CSS alone can't replicate that,
   so this only documents the intended baseline. */
@supports not (interpolate-size: allow-keywords) {
  .accordion-panel[data-open="true"] { height: var(--accordion-measured-height, auto); }
}
```

---

## 221. CSS CUSTOM HIGHLIGHT API

```css
/* ─── CSS Custom Highlight API ───
   JS registers ranges into named highlights, e.g.:
   CSS.highlights.set('search-results', new Highlight(range1, range2));
   CSS then styles them below — no wrapping <mark> elements needed in the DOM. */

::highlight(search-results) {
  background-color: var(--color-warning-100);
  color: var(--color-warning-900);
}

/* The currently-focused match gets its own distinct highlight */
::highlight(search-current) {
  background-color: var(--color-warning-500);
  color: white;
}

/* Inline comment/annotation highlighting, e.g. in a collaborative editor */
::highlight(comment-thread) {
  background-color: color-mix(in srgb, var(--color-accent) 15%, transparent);
  text-decoration: underline dotted var(--color-accent);
}

/* @mention / keyword highlighting in a feed or editor */
::highlight(mention) {
  background-color: color-mix(in srgb, var(--color-brand-500) 15%, transparent);
  color: var(--color-brand-700);
  font-weight: var(--font-weight-semibold);
}

/* Diff-style highlights */
::highlight(diff-added)   { background-color: var(--color-success-100); }
::highlight(diff-removed) { background-color: var(--color-danger-100); text-decoration: line-through; }

/* Spelling/grammar-style squiggle without touching DOM structure */
::highlight(spelling-issue) {
  text-decoration: underline wavy var(--color-danger-500);
}

/* ─── Fallback: wrap matches in <mark> for browsers without the Highlight API ─── */
@supports not selector(::highlight(a)) {
  mark.search-match          { background-color: var(--color-warning-100); color: var(--color-warning-900); }
  mark.search-match--current { background-color: var(--color-warning-500); color: white; }
}
```

---

## 222. CONTAINER STYLE QUERIES

```css
/* ─── Container style queries react to a CUSTOM PROPERTY value on an
   ancestor container, not its size — distinct from the size-based
   @container queries covered in chapter 17. ─── */

.card-container {
  container-type: normal; /* style queries don't require size/inline-size containment */
  container-name: card-zone;
  /* --zone-mode / --zone-accent / --zone-scheme are set on this element,
     typically inline (style="--zone-mode: compact") or toggled by a small script */
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

/* React when an ancestor container sets --zone-mode: compact */
@container card-zone style(--zone-mode: compact) {
  .card { padding: var(--space-3); font-size: var(--font-size-sm); }
}

/* React when an ancestor sets --zone-accent to a specific value */
@container card-zone style(--zone-accent: danger) {
  .card       { border-color: var(--color-danger-500); }
  .card-title { color: var(--color-danger-500); }
}

/* Boolean-style toggle: style() treats a non-empty custom property as truthy */
@container card-zone style(--zone-featured) {
  .card { box-shadow: var(--shadow-lg); border-color: var(--color-accent); }
}

/* A dark "zone" that re-themes children without a `.dark` class on each of them */
@container card-zone style(--zone-scheme: dark) {
  .card {
    background: var(--color-neutral-900);
    color: white;
    border-color: var(--color-neutral-700);
  }
}

/* Combine a style query with a size query using `and` */
@container card-zone (min-width: 400px) and style(--zone-mode: compact) {
  .card { display: flex; align-items: center; gap: var(--space-4); }
}
```

---

## 223. FIELD-SIZING (AUTO-GROWING FORM FIELDS)

```css
/* ─── Auto-growing textarea, no JS required ─── */
textarea.autosize {
  field-sizing: content;
  min-height: 2.5lh;   /* at least 2 lines tall */
  max-height: 12lh;    /* stop growing and start scrolling past 12 lines */
  padding: var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  font: inherit;
  line-height: var(--line-height-normal);
  resize: none; /* a manual resize handle is redundant once the field auto-sizes */
}

/* ─── Auto-growing single-line input (e.g. an inline "rename" field) ─── */
input.autosize-inline {
  field-sizing: content;
  min-width: 4ch;
  max-width: 100%;
  padding: 0.25em 0.5em;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font: inherit;
  background: transparent;
}
input.autosize-inline:hover,
input.autosize-inline:focus-visible {
  border-color: var(--color-border);
  background: var(--color-bg-subtle);
}

/* ─── Search box that grows with the typed query, capped by its container ─── */
.search-box {
  field-sizing: content;
  min-width: 8ch;
  max-width: 100%;
  padding: 0.4em 0.8em;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
}

/* ─── Chat composer that grows with the message, up to a cap ─── */
.chat-composer textarea {
  field-sizing: content;
  max-height: 8lh;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-xl);
  border: 1px solid var(--color-border);
}

/* ─── Fallback for browsers without field-sizing support ───
   the classic approach mirrors the value into a hidden div and measures
   it in JS — CSS alone can't replicate that, so this only sets a
   reasonable baseline height until such a script runs. */
@supports not (field-sizing: content) {
  textarea.autosize { height: 4.5rem; }
}
```

---

## 224. LIGHT-DARK() FUNCTION DEEP DIVE

```css
/* ─── light-dark() collapses a light/dark pair into one declaration,
   switching automatically with color-scheme — no [data-theme] selector needed ─── */
:root {
  color-scheme: light dark;

  --surface:       light-dark(var(--color-neutral-0),   var(--color-neutral-900));
  --on-surface:    light-dark(var(--color-neutral-900), var(--color-neutral-100));
  --border-subtle: light-dark(var(--color-neutral-200), var(--color-neutral-700));
}

.card-ld {
  background: var(--surface);
  color: var(--on-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

/* Per-element opt-out: force one scheme regardless of page/user preference */
.always-light { color-scheme: light; }
.always-dark  { color-scheme: dark; }

/* Direct one-off use, without a named variable, for values used only once */
.callout {
  background: light-dark(var(--color-brand-100), var(--color-brand-900));
  border-inline-start: 3px solid var(--color-accent);
  padding: var(--space-4);
}

/* Shadows often need to soften, not just recolor, in dark mode */
.elevated {
  box-shadow: light-dark(var(--shadow-md), 0 4px 6px -1px rgb(0 0 0 / 0.4));
}

/* Icons/illustrations inverted in dark mode without shipping two assets */
.mono-icon {
  filter: light-dark(none, invert(1));
}

/* ─── When light-dark() is enough vs when the full token system (ch. 29 / 136) is needed ───
   light-dark() fits simple, independent light/dark pairs like the ones
   above. It does not scale to systems with more than two themes (e.g. a
   brand theme + high-contrast theme + dark) and can't express semantic
   renaming across breakpoints — for that, keep the [data-theme]
   custom-property system from chapter 29/136. */

/* Both systems can coexist: light-dark() for the default two-mode case,
   overridden by an explicit [data-theme="brand"] block for special cases */
[data-theme="brand"] {
  --surface: var(--color-brand-900);
  --on-surface: white;
}
```

---

## 225. NATIVE CUSTOMIZABLE SELECT

```css
/* ─── Opt in to the new customizable <select> rendering ─── */
select, ::picker(select) {
  appearance: base-select;
}

select {
  padding: 0.5rem 2.25rem 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  font: inherit;
  color: var(--color-text);
}
select:focus-visible {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 20%, transparent);
}

/* The dropdown arrow is its own styleable part once appearance: base-select is set */
select::picker-icon {
  color: var(--color-text-muted);
  transition: rotate var(--duration-fast);
}
select:open::picker-icon { rotate: 180deg; }

/* The popup panel itself, rendered in the top layer via ::picker(select) */
::picker(select) {
  padding: var(--space-1);
  margin-block-start: var(--space-1);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  box-shadow: var(--shadow-lg);
}

/* Fully styleable <option> — including layout, not just color, unlike the old <select> */
option {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
}
option:hover,
option:focus-visible { background: var(--color-bg-subtle); }
option:checked {
  background: color-mix(in srgb, var(--color-accent) 10%, transparent);
  font-weight: var(--font-weight-semibold);
}

/* Checkmark on the selected option, via the new ::checkmark part */
option::checkmark {
  color: var(--color-accent);
  order: 1; /* move the checkmark to the end of the option row */
  margin-inline-start: auto;
}

/* <optgroup> labels */
optgroup {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  padding: var(--space-2) var(--space-3) var(--space-1);
}

/* Rich options: avatar + label + secondary text, all native, no custom div dropdown */
.select-option-rich { display: flex; align-items: center; gap: var(--space-3); }
.select-option-rich img { width: 1.5rem; height: 1.5rem; border-radius: 50%; }
.select-option-rich small { display: block; color: var(--color-text-muted); font-size: var(--font-size-xs); }

/* ─── Fallback for browsers without customizable <select> support ─── */
@supports not (appearance: base-select) {
  select { appearance: auto; } /* keep the plain native control, no custom popup styling */
}
```

---

## 226. READING-FLOW & READING-ORDER

```css
/* ─── reading-flow keeps DOM/accessibility-tree/Tab order in sync with
   VISUAL order, even when flex/grid reorders things on screen ─── */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  reading-flow: grid-rows; /* screen readers & Tab follow row-by-row visual order */
}

.flex-toolbar {
  display: flex;
  reading-flow: flex-visual; /* Tab/AX order follows left-to-right visual position,
                                 not source order, once items are reordered */
}

/* ─── reading-order fine-tunes one item's position in that flow without touching the DOM ─── */
.priority-action {
  order: -1;         /* visually first */
  reading-order: -1; /* also read/focused first, staying in sync with `order` */
}
.decorative-late-item {
  order: 5;
  reading-order: 5; /* keep it visually and semantically last together */
}

/* ─── Common pitfall this feature exists to fix: `order` alone only changes
   paint order, not focus/AX order — a mouse user and a keyboard/screen-reader
   user can end up navigating a component in two different sequences. ─── */
.mismatched-example {
  display: flex;
  /* `order` used on children here, reading-flow intentionally NOT set,
     to illustrate the exact mismatch bug */
}

/* ─── Practical case: image leads visually, but content should stay
   first in reading/tab order regardless of the current layout ─── */
.feature-card {
  display: grid;
  grid-template-areas: "media" "body";
  reading-flow: grid-order;
}
.feature-card__media { grid-area: media; }
.feature-card__body  { grid-area: body; }

@container (min-width: 500px) {
  .feature-card {
    grid-template-columns: 1fr 1fr;
    grid-template-areas: "body media";
  }
  /* reading-flow: grid-order keeps .feature-card__body announced/focused
     first even though it now sits visually on the right */
}
```

---

## 227. VARIABLE FONTS DEEP DIVE

```css
/* ─── Registering a variable font ─── */
@font-face {
  font-family: 'InterVariable';
  src: url('/fonts/InterVariable.woff2') format('woff2-variations');
  font-weight: 100 900;     /* the whole weight axis range this file supports */
  font-stretch: 75% 125%;   /* width axis range */
  font-style: oblique 0deg 10deg;
  font-display: swap;
}

body {
  font-family: 'InterVariable', var(--font-sans);
  font-optical-sizing: auto; /* lets the font adjust rendering per size, if it has an opsz axis */
}

/* ─── Standard axes exposed through normal properties, no font-variation-settings needed ─── */
.text-thin        { font-weight: 350; }
.text-bold         { font-weight: 750; }
.text-condensed    { font-stretch: 85%; }
.text-wide         { font-stretch: 115%; }
.text-italic-lean  { font-style: oblique 6deg; }

/* ─── Custom/registered axes need font-variation-settings directly ─── */
.text-custom-axis {
  font-variation-settings: 'wght' 620, 'opsz' 28, 'GRAD' 15;
}

/* ─── Animating a variable axis directly on hover/focus ─── */
.variable-heading {
  font-weight: 400;
  transition: font-weight var(--duration-slow) var(--ease-out);
}
.variable-heading:hover { font-weight: 800; }

/* ─── @property lets a custom axis participate in transitions/keyframes
   as an isolated, composable value instead of a whole settings string ─── */
@property --heading-wght {
  syntax: '<number>';
  inherits: true;
  initial-value: 400;
}
.animated-variable-text {
  font-variation-settings: 'wght' var(--heading-wght);
  transition: --heading-wght var(--duration-slow) var(--ease-out);
}
.animated-variable-text:hover { --heading-wght: 800; }

/* ─── Optical sizing tied to viewport for display headings ─── */
.fluid-display-heading {
  font-size: clamp(2rem, 6vw, 5rem);
  font-optical-sizing: auto;
  font-variation-settings: 'opsz' clamp(14, 6cqw, 96);
}

@media (prefers-reduced-motion: reduce) {
  .variable-heading,
  .animated-variable-text { transition: none; }
}
```

---

## 228. CSS NATIVE SCROLL-DRIVEN CAROUSEL

```css
/* ─── Native CSS carousel: scroll-marker-group + scroll-button, no JS ───
   Builds on the manual scroll-snap technique from chapter 63.1, adding
   browser-native pagination dots and prev/next buttons on top of it. */

.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: var(--space-4);
  scroll-marker-group: after; /* renders the generated marker group after the scroller */
}

.carousel-item {
  scroll-snap-align: center;
  flex: 0 0 100%;
}

/* Each item contributes one marker to the group via its own ::scroll-marker */
.carousel-item::scroll-marker {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-bg-muted);
  transition: background var(--duration-fast), scale var(--duration-fast);
}

/* The marker for the currently-snapped item */
.carousel-item::scroll-marker:target-current {
  background: var(--color-accent);
  scale: 1.3;
}

/* Layout of the marker group itself (the row of dots) */
.carousel::scroll-marker-group {
  display: flex;
  justify-content: center;
  gap: var(--space-2);
  margin-block-start: var(--space-3);
}

/* ─── Native prev/next buttons, auto-disabled at the scroll limits ─── */
.carousel::scroll-button(inline-start),
.carousel::scroll-button(inline-end) {
  content: '‹';
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: var(--color-surface);
  box-shadow: var(--shadow-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.carousel::scroll-button(inline-end) { content: '›'; }

.carousel::scroll-button(*):disabled {
  opacity: 0.3;
  cursor: default;
}

/* ─── Comparison note ───
   Manual scroll-snap carousels (ch. 63.1) need JS to build pagination
   dots and prev/next buttons and to track the active slide. This
   combination moves all three responsibilities into CSS, at the cost
   of needing a very recent browser and a documented fallback below. */

/* ─── Fallback for browsers without this feature ─── */
@supports not (scroll-marker-group: after) {
  .carousel::scroll-marker-group,
  .carousel::scroll-button(*) { display: none; }
  /* fall back to the manual JS-driven dots/buttons pattern from chapter 63.1 */
}
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                     PART 16 — COMPLETE                               ║
║  Chapters 219–228 | 10 new chapters | Output: css-guide-part16.md    ║
╚══════════════════════════════════════════════════════════════════════╝
```
