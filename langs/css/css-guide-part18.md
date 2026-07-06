# CSS GUIDE — PART 18
## Chapters 239–248

---

## 239. FOCUS MANAGEMENT COOKBOOK

```css
/* ─── :focus-visible vs :focus ───
   :focus fires for ANY focus (including some mouse clicks); :focus-visible
   fires only when the browser's heuristic decides a visible ring is
   warranted (keyboard nav, programmatic focus, etc). */

/* Baseline: never show a ring for pointer-only interaction */
button:focus:not(:focus-visible) {
  outline: none;
}
button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* ─── :focus-within for composite fields ───
   Style a whole group (label + input + icon) when any descendant has focus */
.field-group {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-2) var(--space-3);
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
}
.field-group:focus-within {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 20%, transparent);
}
.field-group input { border: none; outline: none; background: none; flex: 1; font: inherit; }

/* ─── Visual focus-trap indication (e.g. inside an open dialog) ───
   This only signals the trap visually — actually trapping Tab order
   is a JS concern, not something CSS can enforce on its own. */
.focus-trap-active {
  outline: 2px dashed var(--color-accent);
  outline-offset: 4px;
}

/* ─── Skip link: hidden until focused, then jumps to the top ─── */
.skip-link {
  position: absolute;
  top: -3rem;
  left: var(--space-4);
  padding: var(--space-2) var(--space-4);
  background: var(--color-neutral-900);
  color: white;
  border-radius: var(--radius-md);
  z-index: var(--z-top);
  transition: top var(--duration-fast);
}
.skip-link:focus-visible { top: var(--space-4); }

/* ─── Roving tabindex highlight (toolbar/menu pattern) ───
   Only one item in the group is a Tab stop at a time (tabindex managed
   in JS); CSS highlights whichever one currently holds that role. */
.toolbar-item[tabindex="0"] { background: var(--color-bg-subtle); }
.toolbar-item:focus-visible { outline: 2px solid var(--color-accent); outline-offset: -2px; }

/* ─── Focus ring that follows a custom shape (e.g. a pill button) ─── */
.pill-button { border-radius: var(--radius-full); outline-offset: 3px; }
.pill-button:focus-visible { outline: 2px solid var(--color-accent); }

/* ─── High-visibility focus mode toggle (an in-app preference, distinct from any prefers-* media feature) ─── */
[data-focus-mode="high-visibility"] :focus-visible {
  outline: 3px solid var(--color-accent);
  outline-offset: 3px;
  box-shadow: 0 0 0 6px color-mix(in srgb, var(--color-accent) 25%, transparent);
}
```

---

## 240. FORM VALIDATION STATES COOKBOOK

```css
/* ─── :user-valid / :user-invalid vs :valid / :invalid ───
   :valid/:invalid match immediately, even before the person has
   interacted with the field — flagging an empty required field the
   instant the page loads. :user-valid/:user-invalid only match AFTER
   the person has interacted with and left the field. */

input, textarea, select {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-2) var(--space-3);
}

/* Avoid this — flags empty required fields before any interaction:
   input:invalid { border-color: var(--color-danger-500); } */

/* Prefer this — only flags fields the person actually touched and left invalid */
input:user-invalid,
textarea:user-invalid { border-color: var(--color-danger-500); }
input:user-valid,
textarea:user-valid { border-color: var(--color-success-500); }

.field-hint { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-block-start: var(--space-1); }
input:user-invalid ~ .field-hint { color: var(--color-danger-500); }

/* ─── Form-level error summary via :has() ───
   Shows a summary banner only once the form contains at least one
   field the person has interacted with and left invalid. */
.form-error-summary { display: none; }
form:has(:user-invalid) .form-error-summary {
  display: block;
  padding: var(--space-4);
  background: var(--color-danger-100);
  color: var(--color-danger-900);
  border-radius: var(--radius-lg);
  margin-block-end: var(--space-4);
}

/* Required-field marker, driven purely by the `required` attribute */
label:has(+ :required)::after,
label:has(+ * :required)::after {
  content: ' *';
  color: var(--color-danger-500);
}

/* Success checkmark, shown once a field is confirmed valid */
.field-success-icon { display: none; }
.field-group:has(:user-valid) .field-success-icon {
  display: inline-flex;
  color: var(--color-success-500);
}

/* Dim submit until the whole form is currently valid */
button[type="submit"] { opacity: 1; transition: opacity var(--duration-fast); }
form:has(:invalid) button[type="submit"] { opacity: 0.5; }

/* Custom validity message box, positioned near the field (layout only —
   the message content itself still comes from the browser or from JS) */
.validity-tooltip {
  position: absolute;
  margin-block-start: var(--space-1);
  padding: var(--space-2) var(--space-3);
  background: var(--color-danger-500);
  color: white;
  font-size: var(--font-size-xs);
  border-radius: var(--radius-md);
}
```

---

## 241. PREFERS-REDUCED-MOTION COOKBOOK

```css
/* ─── Global safe default: cut (most) animation/transition duration to
   near-zero rather than removing it outright — this keeps end-state
   logic like `transitionend` listeners working with no visible motion. ─── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* ─── Parallax hero: drop the transform-based effect for a static position ─── */
.parallax-hero { background-attachment: fixed; }
@media (prefers-reduced-motion: reduce) {
  .parallax-hero { background-attachment: scroll; }
}

/* ─── Auto-playing carousel: pause instead of removing entirely ─── */
@media (prefers-reduced-motion: reduce) {
  .carousel-autoplay { animation-play-state: paused; }
}

/* ─── Attention-seeking motion (bounce/shake/pulse) swapped for a
   static, still-noticeable style change ─── */
.notification-badge { animation: badge-bounce 1s ease-in-out infinite; }
@media (prefers-reduced-motion: reduce) {
  .notification-badge {
    animation: none;
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-danger-500) 40%, transparent);
  }
}

/* ─── Loading spinner: keep it (functional motion conveying real
   state) but slow it down, rather than removing it — removing all
   motion here would hide whether the app is still working ─── */
@media (prefers-reduced-motion: reduce) {
  .spinner { animation-duration: 1.5s; }
}

/* ─── Opt-in "safe" entrance: fade only, no motion/scale ─── */
.fade-in-safe { animation: fade-in var(--duration-slow) var(--ease-out); }
@keyframes fade-in { from { opacity: 0; } }

.slide-in-unsafe { animation: slide-in var(--duration-slow) var(--ease-out); }
@media (prefers-reduced-motion: reduce) {
  .slide-in-unsafe { animation: none; opacity: 1; translate: 0; }
}

/* ─── Per-component opt-out for an in-app "reduce motion" toggle,
   independent of the OS-level media feature ─── */
[data-motion="reduced"] * {
  animation-duration: 0.01ms !important;
  transition-duration: 0.01ms !important;
}
```

---

## 242. PREFERS-CONTRAST & FORCED-COLORS COOKBOOK

```css
/* ─── forced-colors: active fires in Windows High Contrast Mode (and
   similar OS-level modes), where the OS overrides most author colors
   with a small system palette. ─── */
@media (forced-colors: active) {
  .card { border: 1px solid CanvasText; } /* system color keyword, not a hex value */
  .btn-primary {
    forced-color-adjust: none; /* opt this element out of the OS override */
    background: ButtonFace;
    color: ButtonText;
    border: 1px solid ButtonText;
  }
}

/* Icons that rely on color alone (no shape difference) need a forced-colors fallback */
.status-dot--success { background: var(--color-success-500); }
.status-dot--danger  { background: var(--color-danger-500); }
@media (forced-colors: active) {
  .status-dot--success::after { content: '✓'; }
  .status-dot--danger::after  { content: '✕'; }
}

/* Preserve a custom focus ring instead of losing it to the forced palette */
.custom-focus:focus-visible { outline: 2px solid var(--color-accent); }
@media (forced-colors: active) {
  .custom-focus:focus-visible { outline: 2px solid Highlight; }
}

/* ─── prefers-contrast: more — an author-space preference, independent
   of forced-colors (no OS override involved) ─── */
@media (prefers-contrast: more) {
  :root {
    --color-border: var(--color-neutral-900);
    --color-text-muted: var(--color-neutral-800);
  }
  .card { border-width: 2px; }
  button { outline-offset: 3px; }
}

@media (prefers-contrast: less) {
  .card { box-shadow: none; border-color: var(--color-border); }
}

/* ─── Explicitly opt an element BACK IN to forced-colors overrides
   after a broader forced-color-adjust: none higher up the tree ─── */
.decorative-illustration {
  forced-color-adjust: auto;
}
```

---

## 243. ARIA + CSS ATTRIBUTE SELECTOR COOKBOOK

```css
/* ─── Style directly from ARIA state — a single source of truth,
   instead of toggling a parallel `.is-open`/`.active` class in JS ─── */

/* Disclosure/accordion trigger, driven by aria-expanded */
.disclosure-trigger[aria-expanded="true"] .disclosure-icon { rotate: 180deg; }
.disclosure-icon { transition: rotate var(--duration-fast); }

/* Tab list, driven by aria-selected */
[role="tab"][aria-selected="true"] {
  border-bottom: 2px solid var(--color-accent);
  color: var(--color-accent);
  font-weight: var(--font-weight-semibold);
}
[role="tab"][aria-selected="false"] { color: var(--color-text-muted); }

/* Current page/step, driven by aria-current (several possible values) */
[aria-current="page"] { font-weight: var(--font-weight-semibold); color: var(--color-accent); }
[aria-current="step"] { background: var(--color-accent); color: white; }

/* Busy/loading region */
[aria-busy="true"] { cursor: progress; opacity: 0.6; pointer-events: none; }

/* Invalid form field, mirrored from aria-invalid rather than a class */
[aria-invalid="true"] { border-color: var(--color-danger-500); }

/* Pressed toggle button */
[aria-pressed="true"] { background: var(--color-accent); color: white; }

/* Disabled state kept in sync with aria-disabled (for elements that
   stay focusable/announced while disabled, unlike native `disabled`) */
[aria-disabled="true"] { opacity: 0.5; cursor: not-allowed; }

/* Sort direction indicator on a table header, driven by aria-sort */
[aria-sort="ascending"]::after  { content: '↑'; margin-inline-start: var(--space-1); }
[aria-sort="descending"]::after { content: '↓'; margin-inline-start: var(--space-1); }

/* ─── Anti-pattern to avoid ───
   Don't drive the same visual state from BOTH a class and an aria-*
   attribute — the two can drift out of sync. Once the attribute
   already has to be correct for screen readers (as in every rule
   above), treat it as the single source of truth rather than adding a
   parallel .is-active class that must always match it. */

/* Complements chapter 209 (data-* attribute patterns): reach for data-*
   for purely visual/JS-hook state with no accessibility meaning, and
   aria-* for state that assistive tech also needs to know about. */
```

---

## 244. CSS :HAS() RECIPES COOKBOOK

```css
/* ─── Parent selector by descendant: style a card differently
   depending on whether it contains an image ─── */
.card:has(img) { grid-template-rows: auto 1fr; }
.card:not(:has(img)) { padding-block-start: var(--space-6); }

/* ─── Form-level error state via :has(:invalid) ─── */
form:has(:invalid) .submit-btn { opacity: 0.5; pointer-events: none; }

/* ─── Style a label based on its paired input's state ─── */
label:has(input:checked) {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 8%, transparent);
}
label:has(input:disabled) { opacity: 0.5; }

/* ─── Counting children: react to "how many", without a JS class toggle ─── */
.list:has(> :nth-child(1)):not(:has(> :nth-child(2))) {
  justify-content: center; /* exactly one item */
}
.list:has(> :nth-child(6)) {
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); /* six or more: denser layout */
}

/* ─── Empty-state detection without a server-rendered "no results" flag ─── */
.results-list:not(:has(.result-item)) { display: none; }
.empty-state { display: none; }
.results-list:not(:has(.result-item)) + .empty-state { display: block; }

/* ─── Sibling-aware styling: a heading immediately followed by a data
   table gets tighter spacing than one followed by prose ─── */
h2:has(+ table) { margin-block-end: var(--space-2); }

/* ─── Quantity query on a grid: switch layout only once there are
   enough items to justify it ─── */
.gallery:has(> :nth-child(4)) { grid-template-columns: repeat(2, 1fr); }

/* ─── Parent reacts to one specific hovered descendant, unlike
   :focus-within's "any descendant" behaviour ─── */
.card:has(.card-cta:hover) { box-shadow: var(--shadow-lg); }

/* ─── Style a container differently when it holds an error message ─── */
.toast:has(.toast--danger) { border-color: var(--color-danger-500); }
```

---

## 245. STACKING CONTEXT & Z-INDEX — COMPLETE GUIDE

```css
/* ─── Common ways an element creates a NEW stacking context — once
   created, z-index values inside it are only ever compared to each
   other, never directly to values outside it. ─── */

/* 1. Positioned + z-index other than auto */
.creates-context-1 { position: relative; z-index: 1; }

/* 2. Any opacity below 1 */
.creates-context-2 { opacity: 0.99; }

/* 3. transform / filter / backdrop-filter / perspective (any value other than none) */
.creates-context-3 { transform: translateZ(0); }

/* 4. will-change naming a property that would itself create a context */
.creates-context-4 { will-change: transform; }

/* 5. isolation: isolate — creates a context with no other side effects,
   the cleanest way to contain z-index on purpose */
.creates-context-5 { isolation: isolate; }

/* 6. mix-blend-mode other than normal */
.creates-context-6 { mix-blend-mode: multiply; }

/* 7. Flex/grid children with z-index other than auto */
.flex-parent { display: flex; }
.flex-parent > .creates-context-7 { z-index: 1; }

/* ─── Debugging "z-index doesn't work" ───
   The most common cause: an ancestor between the two competing
   elements creates its own stacking context (often by accident, via a
   transform or opacity added for an unrelated reason). No z-index
   value on the descendant can escape that ancestor's context. */
.debug-outline * { outline: 1px solid var(--color-danger-500); }

/* ─── A documented z-index scale, so values are picked from a shared
   list instead of ad hoc numbers that creep upward over time ─── */
:root {
  --z-base: 0;
  --z-raised: 10;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-overlay: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-toast: 700;
  --z-tooltip: 800;
  --z-top: 900;
}
/* Every layered component in this guide (modal stack ch.140, toast
   ch.213, popover ch.211…) draws its z-index from this one scale. */

/* ─── Reset a nested context back to the ambient stacking order, for a
   component that must not trap a child above its own siblings ─── */
.reset-context {
  isolation: auto;
  z-index: auto;
}
```

---

## 246. @STARTING-STYLE ENTRY/EXIT COOKBOOK

```css
/* ─── The core pattern: an element needs (a) a starting state, (b) an
   ending state, (c) a transition between them, and (d) `display`/
   `overlay` included in that transition with `allow-discrete`, so the
   browser doesn't just snap `display: none` on and off instantly. ─── */

.entry-exit-base {
  opacity: 0;
  scale: 0.95;
  transition:
    opacity var(--duration-normal) var(--ease-out),
    scale   var(--duration-normal) var(--ease-out),
    display var(--duration-normal) allow-discrete,
    overlay var(--duration-normal) allow-discrete;
}
.entry-exit-base.is-open { opacity: 1; scale: 1; }
@starting-style {
  .entry-exit-base.is-open { opacity: 0; scale: 0.95; }
}

/* ─── Applied to a plain conditionally-rendered element (a display:
   none toggle), not just popover/dialog — the general-purpose form ─── */
.conditional-panel {
  display: none;
  opacity: 0;
  transition: opacity var(--duration-normal), display var(--duration-normal) allow-discrete;
}
.conditional-panel.is-visible { display: block; opacity: 1; }
@starting-style {
  .conditional-panel.is-visible { opacity: 0; }
}

/* ─── Slide-up entry, the same technique behind the toast in chapter 213 ─── */
.slide-up-entry {
  translate: 0 16px;
  opacity: 0;
  transition: translate var(--duration-normal) var(--ease-out), opacity var(--duration-normal) var(--ease-out);
}
.slide-up-entry.mounted { translate: 0 0; opacity: 1; }
@starting-style {
  .slide-up-entry.mounted { translate: 0 16px; opacity: 0; }
}

/* ─── Height entry/exit, combined with interpolate-size (chapter 220) ─── */
.grow-in {
  height: 0;
  overflow: hidden;
  transition: height var(--duration-normal) var(--ease-out);
}
.grow-in.expanded { height: auto; }
@starting-style {
  .grow-in.expanded { height: 0; }
}

/* ─── Common mistake: omitting `allow-discrete` on `display` means the
   browser still flips display instantly, so @starting-style never
   gets a chance to apply and the "entry" animation silently never runs ─── */
.broken-example {
  display: none;
  opacity: 0;
  transition: opacity var(--duration-normal); /* missing `display … allow-discrete` here */
}
```

---

## 247. LOADING & PROGRESS INDICATOR LIBRARY

```css
/* ─── Spinner: ring ─── */
.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid var(--color-bg-muted);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { rotate: 360deg; } }

/* ─── Spinner: dots ─── */
.spinner--dots { display: flex; gap: var(--space-1); }
.spinner--dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  animation: dot-bounce 1.4s ease-in-out infinite both;
}
.spinner--dots span:nth-child(2) { animation-delay: 0.16s; }
.spinner--dots span:nth-child(3) { animation-delay: 0.32s; }
@keyframes dot-bounce {
  0%, 80%, 100% { scale: 0.6; opacity: 0.5; }
  40% { scale: 1; opacity: 1; }
}

/* ─── Spinner: equalizer bars ─── */
.spinner--bars { display: flex; gap: 3px; align-items: flex-end; height: 1.5rem; }
.spinner--bars span { width: 4px; background: var(--color-accent); animation: bar-scale 1s ease-in-out infinite; }
.spinner--bars span:nth-child(2) { animation-delay: 0.1s; }
.spinner--bars span:nth-child(3) { animation-delay: 0.2s; }
.spinner--bars span:nth-child(4) { animation-delay: 0.3s; }
@keyframes bar-scale {
  0%, 100% { height: 30%; }
  50% { height: 100%; }
}

/* ─── Indeterminate progress bar (unknown duration/amount) ─── */
.progress-indeterminate {
  height: 4px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}
.progress-indeterminate::after {
  content: '';
  position: absolute;
  inset-block: 0;
  width: 40%;
  background: var(--color-accent);
  border-radius: inherit;
  animation: indeterminate-slide 1.4s ease-in-out infinite;
}
@keyframes indeterminate-slide {
  from { left: -40%; }
  to   { left: 100%; }
}

/* ─── Determinate progress bar (known percentage) ─── */
.progress-determinate { height: 6px; background: var(--color-bg-muted); border-radius: var(--radius-full); overflow: hidden; }
.progress-determinate__fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: inherit;
  transition: width var(--duration-normal) var(--ease-out);
}

/* ─── Choosing between this library and skeleton screens (ch. 200) ───
   Spinners/progress bars suit short, unpredictable waits with no
   layout to preview yet (e.g. submitting a form). Skeletons suit waits
   where the eventual layout is already known (e.g. a feed of cards
   about to load) — they set content-shape expectations a spinner can't. */

@media (prefers-reduced-motion: reduce) {
  .spinner, .spinner--dots span, .spinner--bars span, .progress-indeterminate::after {
    animation-duration: 2s; /* slower, not removed — this motion is functional, not decorative */
  }
}
```

---

## 248. MULTI-STEP WIZARD / STEPPER (GENERAL PATTERN)

```css
/* ─── Horizontal stepper ─── */
.stepper { display: flex; align-items: center; }
.stepper-step { display: flex; align-items: center; gap: var(--space-2); flex: 1; }

.stepper-step__circle {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 2px solid var(--color-border-strong);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  flex-shrink: 0;
  transition: background var(--duration-fast), border-color var(--duration-fast);
}
.stepper-step__label { font-size: var(--font-size-sm); color: var(--color-text-muted); white-space: nowrap; }

/* Connecting line between steps */
.stepper-step:not(:last-child)::after {
  content: '';
  flex: 1;
  height: 2px;
  background: var(--color-border);
  margin-inline: var(--space-2);
}

/* ─── States ─── */
.stepper-step--done .stepper-step__circle { background: var(--color-success-500); border-color: var(--color-success-500); color: white; }
.stepper-step--done .stepper-step__circle::before { content: '✓'; }
.stepper-step--done:not(:last-child)::after { background: var(--color-success-500); }
.stepper-step--done .stepper-step__label { color: var(--color-text); }

.stepper-step--active .stepper-step__circle {
  border-color: var(--color-accent);
  color: var(--color-accent);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--color-accent) 15%, transparent);
}
.stepper-step--active .stepper-step__label { color: var(--color-text); font-weight: var(--font-weight-semibold); }

.stepper-step--upcoming .stepper-step__circle { background: var(--color-bg-subtle); }

.stepper-step--error .stepper-step__circle { background: var(--color-danger-500); border-color: var(--color-danger-500); color: white; }
.stepper-step--error .stepper-step__label { color: var(--color-danger-500); }

/* ─── Vertical stepper variant ─── */
.stepper--vertical { flex-direction: column; align-items: stretch; }
.stepper--vertical .stepper-step {
  flex-direction: column;
  align-items: flex-start;
  flex: 0 0 auto;
  position: relative;
  padding-inline-start: var(--space-8);
  padding-block-end: var(--space-6);
}
.stepper--vertical .stepper-step__circle { position: absolute; inset-inline-start: 0; }
.stepper--vertical .stepper-step:not(:last-child)::after {
  content: '';
  position: absolute;
  inset-inline-start: 0.9375rem;
  top: 2rem;
  bottom: 0;
  width: 2px;
  height: auto;
  background: var(--color-border);
  margin: 0;
}
.stepper--vertical .stepper-step__content { margin-block-start: var(--space-1); font-size: var(--font-size-xs); color: var(--color-text-muted); }

/* ─── Compact mobile variant: dots only, current step's label shown separately ─── */
.stepper--compact .stepper-step__label { display: none; }
.stepper--compact .stepper-step__circle { width: 0.5rem; height: 0.5rem; border-width: 0; background: var(--color-border-strong); }
.stepper--compact .stepper-step--done .stepper-step__circle,
.stepper--compact .stepper-step--active .stepper-step__circle { background: var(--color-accent); }
.stepper--compact .stepper-step--active .stepper-step__circle { scale: 1.4; }

/* This is the general-purpose pattern, generalized from the specific
   checkout stepper (ch. 187) and onboarding tour (ch. 144) — reuse it
   there instead of styling a one-off stepper per feature. */
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                     PART 18 — COMPLETE                               ║
║  Chapters 239–248 | 10 new chapters | Output: css-guide-part18.md    ║
╚══════════════════════════════════════════════════════════════════════╝
```
