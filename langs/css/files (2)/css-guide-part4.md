# PART IV — ADVANCED CSS: COMPLETE CONTINUATION

---

## 74. CSS FOR PWA & MOBILE-SPECIFIC PATTERNS

### 74.1 Safe Area Insets (Notch / Dynamic Island)

```css
/* ─── iOS safe area support ─── */
:root {
  --sat: env(safe-area-inset-top);
  --sar: env(safe-area-inset-right);
  --sab: env(safe-area-inset-bottom);
  --sal: env(safe-area-inset-left);
}

/* Full-bleed header that respects notch */
.app-header {
  padding-top: max(var(--space-4), env(safe-area-inset-top));
  padding-left:  max(var(--space-4), env(safe-area-inset-left));
  padding-right: max(var(--space-4), env(safe-area-inset-right));
}

/* Bottom navigation bar */
.bottom-nav {
  position: fixed;
  bottom: 0;
  inset-inline: 0;
  padding-bottom: max(var(--space-3), env(safe-area-inset-bottom));
  padding-inline: max(var(--space-4), env(safe-area-inset-left));
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  z-index: var(--z-fixed);
}

/* Full viewport — safe */
.full-page {
  min-height: 100dvh;
  padding: env(safe-area-inset-top, 0)
           env(safe-area-inset-right, 0)
           env(safe-area-inset-bottom, 0)
           env(safe-area-inset-left, 0);
}

/* Scrollable content above bottom nav */
.page-content {
  padding-bottom: calc(var(--bottom-nav-height, 4rem) + env(safe-area-inset-bottom, 0px));
}
```

### 74.2 Touch & Mobile Optimizations

```css
/* ─── Prevent rubber-band scroll on iOS ─── */
html, body {
  overscroll-behavior: none;      /* prevent pull-to-refresh */
}

/* Allow only inner scroll containers to scroll */
.scroll-container {
  overflow-y: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}

/* ─── Prevent double-tap zoom ─── */
button, a, [role="button"] {
  touch-action: manipulation;     /* removes 300ms tap delay */
}

/* ─── Tap highlight removal ─── */
* {
  -webkit-tap-highlight-color: transparent;
}

/* Custom tap highlight for interactive elements */
.interactive {
  -webkit-tap-highlight-color: color-mix(in srgb, var(--color-accent) 15%, transparent);
}

/* ─── Prevent text selection on UI elements ─── */
.ui-element {
  user-select: none;
  -webkit-user-select: none;
}

/* ─── Better input on mobile ─── */
input[type="text"],
input[type="email"],
input[type="search"],
textarea {
  font-size: max(16px, 1rem);     /* prevents iOS zoom on focus */
}

/* ─── Mobile-only styles ─── */
@media (hover: none) and (pointer: coarse) {
  /* Touch device */
  .hover-only { display: none; }
  .btn { min-height: 44px; min-width: 44px; }
  
  /* Larger tap targets */
  .nav-link {
    padding-block: 0.875rem;
  }
}

/* ─── Pull to refresh indicator ─── */
.pull-indicator {
  position: fixed;
  top: 0;
  left: 50%;
  translate: -50% calc(-100% + var(--pull, 0px));
  background: var(--color-surface);
  border-radius: 0 0 var(--radius-full) var(--radius-full);
  padding: 0.5rem 1rem;
  box-shadow: var(--shadow-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  transition: translate 0.2s;
}

/* ─── App icon mask (PWA) ─── */
/* In HTML: <link rel="mask-icon" href="icon.svg" color="#3b82f6"> */
/* In manifest.json: "display": "standalone" */

/* PWA display mode detection */
@media (display-mode: standalone) {
  .install-banner { display: none; }
  .app-header     { padding-top: env(safe-area-inset-top); }
}

@media (display-mode: fullscreen) {
  .exit-fullscreen-btn { display: flex; }
}
```

### 74.3 Mobile Navigation Patterns

```css
/* ─── Bottom Tab Bar (iOS/Android style) ─── */
.tab-bar {
  position: fixed;
  bottom: 0;
  inset-inline: 0;
  height: calc(3.5rem + env(safe-area-inset-bottom, 0px));
  padding-bottom: env(safe-area-inset-bottom, 0px);
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  display: flex;
  align-items: stretch;
  z-index: var(--z-fixed);
}

.tab-bar__item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.5rem;
  text-decoration: none;
  color: var(--color-text-muted);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  transition: color var(--duration-fast);
  position: relative;
}

.tab-bar__item[aria-current="page"] {
  color: var(--color-accent);
}

.tab-bar__icon {
  width: 1.5rem;
  height: 1.5rem;
  transition: transform var(--duration-fast) var(--ease-bounce);
}

.tab-bar__item[aria-current="page"] .tab-bar__icon {
  transform: scale(1.15) translateY(-1px);
}

/* Active indicator pill */
.tab-bar__item[aria-current="page"]::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  translate: -50%;
  width: 2rem;
  height: 3px;
  background: var(--color-accent);
  border-radius: 0 0 var(--radius-full) var(--radius-full);
}

/* ─── Hamburger → X animation ─── */
.hamburger {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 24px;
  padding: 0;
  background: none;
  border: none;
  cursor: pointer;
}

.hamburger span {
  display: block;
  height: 2px;
  background: currentColor;
  border-radius: 2px;
  transform-origin: center;
  transition:
    transform   var(--duration-normal) var(--ease-out),
    opacity     var(--duration-normal),
    translate   var(--duration-normal) var(--ease-out);
}

.hamburger[aria-expanded="true"] span:nth-child(1) {
  translate: 0 7px;
  transform: rotate(45deg);
}
.hamburger[aria-expanded="true"] span:nth-child(2) {
  opacity: 0;
  transform: scaleX(0);
}
.hamburger[aria-expanded="true"] span:nth-child(3) {
  translate: 0 -7px;
  transform: rotate(-45deg);
}
```

---

## 75. CSS MICRO-INTERACTIONS

### 75.1 Button States & Feedback

```css
/* ─── Complete interactive button system ─── */
.btn-interactive {
  position: relative;
  overflow: hidden;
  transform: translateZ(0);   /* GPU layer */

  /* State variables */
  --state-bg-modifier: 0;
}

/* Ripple effect */
.btn-interactive::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at var(--x, 50%) var(--y, 50%),
    rgb(255 255 255 / 0.3) 0%,
    transparent 70%
  );
  opacity: 0;
  transition: opacity 0.3s;
}

.btn-interactive:active::after {
  opacity: 1;
  transition: opacity 0s;
}

/* Press feedback */
.btn-interactive:active {
  scale: 0.97;
  transition: scale 0.1s var(--ease-out);
}

/* Success state */
.btn-interactive[data-state="success"] {
  --btn-bg: var(--color-success-500);
  animation: success-bounce 0.4s var(--ease-bounce);
}

@keyframes success-bounce {
  0%   { scale: 0.95; }
  60%  { scale: 1.05; }
  100% { scale: 1; }
}

/* Loading → Success transition */
.btn-interactive[data-state="loading"] {
  pointer-events: none;
  cursor: wait;
}

.btn-interactive[data-state="loading"] .btn-text {
  opacity: 0;
  transform: translateY(-100%);
}

.btn-interactive[data-state="loading"] .btn-spinner {
  opacity: 1;
  transform: translateY(0);
}

/* ─── Checkbox with animation ─── */
.animated-checkbox {
  --cb-size: 1.25rem;
  position: relative;
  width: var(--cb-size);
  height: var(--cb-size);
}

.animated-checkbox input {
  position: absolute;
  opacity: 0;
  inset: 0;
  margin: 0;
  cursor: pointer;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.animated-checkbox__box {
  width: 100%;
  height: 100%;
  border: 2px solid var(--color-border-strong);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  transition:
    border-color var(--duration-fast),
    background   var(--duration-fast),
    scale        var(--duration-fast) var(--ease-bounce);
}

.animated-checkbox input:checked + .animated-checkbox__box {
  border-color: var(--color-accent);
  background: var(--color-accent);
  scale: 1;
  animation: checkbox-pop 0.25s var(--ease-bounce);
}

@keyframes checkbox-pop {
  0%   { scale: 0.8; }
  60%  { scale: 1.15; }
  100% { scale: 1; }
}

/* Checkmark SVG path animation */
.animated-checkbox__check {
  stroke-dasharray: 20;
  stroke-dashoffset: 20;
  transition: stroke-dashoffset 0.2s ease-out 0.05s;
}

.animated-checkbox input:checked ~ .animated-checkbox__box .animated-checkbox__check {
  stroke-dashoffset: 0;
}

/* ─── Like/Heart button ─── */
.heart-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  position: relative;
}

.heart-btn svg {
  transition:
    fill      var(--duration-fast),
    scale     var(--duration-fast) var(--ease-bounce),
    filter    var(--duration-fast);
}

.heart-btn[aria-pressed="true"] svg {
  fill: var(--color-danger-500);
  scale: 1;
  animation: heart-burst 0.4s var(--ease-bounce);
}

@keyframes heart-burst {
  0%   { scale: 0.8; }
  50%  { scale: 1.3; filter: drop-shadow(0 0 8px var(--color-danger-500)); }
  100% { scale: 1; filter: none; }
}

/* Particle burst on like (via pseudo-elements) */
.heart-btn[aria-pressed="true"]::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: var(--color-danger-500);
  animation: burst-ring 0.4s ease-out forwards;
}

@keyframes burst-ring {
  0%   { scale: 0; opacity: 0.8; }
  100% { scale: 2.5; opacity: 0; }
}
```

### 75.2 Input Micro-interactions

```css
/* ─── Floating label ─── */
.float-label {
  position: relative;
}

.float-label__input {
  width: 100%;
  padding: 1.25rem 0.75rem 0.375rem;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  font: inherit;
  background: var(--color-surface);
  outline: none;
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
}

.float-label__label {
  position: absolute;
  inset-inline-start: 0.75rem;
  inset-block-start: 0.875rem;
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
  pointer-events: none;
  transition:
    font-size var(--duration-fast) var(--ease-out),
    translate var(--duration-fast) var(--ease-out),
    color     var(--duration-fast);
  transform-origin: left top;
}

/* Float the label when focused or has value */
.float-label__input:focus + .float-label__label,
.float-label__input:not(:placeholder-shown) + .float-label__label {
  font-size: var(--font-size-xs);
  translate: 0 -0.625rem;
  color: var(--color-accent);
}

.float-label__input:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);
}

/* ─── Password strength indicator ─── */
.password-strength {
  display: flex;
  gap: 3px;
  margin-top: 0.5rem;
}

.strength-bar {
  flex: 1;
  height: 4px;
  border-radius: var(--radius-full);
  background: var(--color-bg-muted);
  transition: background var(--duration-slow) var(--ease-out);
  position: relative;
  overflow: hidden;
}

.strength-bar::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: var(--bar-color, transparent);
  transform: scaleX(var(--bar-fill, 0));
  transform-origin: left;
  transition: transform var(--duration-slow) var(--ease-out);
}

/* JS sets data-strength="0|1|2|3|4" on parent */
.password-strength[data-strength="1"] .strength-bar:nth-child(1) {
  --bar-fill: 1; --bar-color: var(--color-danger-500);
}
.password-strength[data-strength="2"] .strength-bar:nth-child(-n+2) {
  --bar-fill: 1; --bar-color: var(--color-warning-500);
}
.password-strength[data-strength="3"] .strength-bar:nth-child(-n+3) {
  --bar-fill: 1; --bar-color: oklch(0.7 0.2 90);
}
.password-strength[data-strength="4"] .strength-bar {
  --bar-fill: 1; --bar-color: var(--color-success-500);
}

/* ─── Search with results preview ─── */
.search-box {
  position: relative;
  container-type: inline-size;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font: inherit;
  background: var(--color-surface);
  transition:
    border-color var(--duration-fast),
    box-shadow   var(--duration-fast),
    border-radius var(--duration-fast) var(--ease-out);
}

/* When results are shown, flatten bottom radius */
.search-box:has(.search-results:not(:empty)) .search-input {
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
  border-bottom-color: transparent;
  box-shadow: var(--shadow-xl);
}

.search-results {
  position: absolute;
  top: 100%;
  inset-inline: 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-top: none;
  border-radius: 0 0 var(--radius-xl) var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  max-height: 320px;
  overflow-y: auto;
}
```

### 75.3 Navigation Micro-interactions

```css
/* ─── Animated underline nav ─── */
.nav-animated {
  display: flex;
  gap: 0;
  position: relative;
}

/* Sliding indicator */
.nav-animated__indicator {
  position: absolute;
  bottom: 0;
  height: 2px;
  background: var(--color-accent);
  border-radius: 2px;
  transition:
    left  var(--duration-slow) var(--ease-out),
    width var(--duration-slow) var(--ease-out);
  /* JS sets left and width based on active item */
}

.nav-animated__link {
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: var(--color-text-muted);
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
  white-space: nowrap;
  transition: color var(--duration-fast);
}

.nav-animated__link:hover,
.nav-animated__link[aria-current="page"] {
  color: var(--color-text);
}

/* ─── Magnetic button effect (via CSS only) ─── */
/* JS manages --mx and --my (mouse offset) */
.magnetic {
  transform: translate(
    calc(var(--mx, 0px) * 0.3),
    calc(var(--my, 0px) * 0.3)
  );
  transition: transform 0.2s var(--ease-out);
}

.magnetic:not(:hover) {
  transform: translate(0, 0);
  transition: transform 0.5s var(--ease-bounce);
}

/* ─── Cursor follower ─── */
.cursor {
  width: 12px;
  height: 12px;
  background: var(--color-accent);
  border-radius: 50%;
  position: fixed;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: var(--z-top);
  translate: calc(var(--cx, 0px) - 50%) calc(var(--cy, 0px) - 50%);
  transition: translate 0.08s linear, scale 0.2s var(--ease-out);
  mix-blend-mode: difference;
}

.cursor-ring {
  width: 40px;
  height: 40px;
  border: 1.5px solid var(--color-accent);
  border-radius: 50%;
  position: fixed;
  pointer-events: none;
  z-index: var(--z-top);
  translate: calc(var(--cx, 0px) - 50%) calc(var(--cy, 0px) - 50%);
  transition: translate 0.25s var(--ease-out), scale 0.25s var(--ease-out), opacity 0.25s;
  mix-blend-mode: difference;
}

/* Scale on hover interactives */
:is(a, button, [role="button"]):hover ~ .cursor { scale: 3; }
:is(a, button, [role="button"]):hover ~ .cursor-ring { opacity: 0; }
```

---

## 76. ADVANCED COMPONENT PATTERNS

### 76.1 Drawer / Sidebar

```css
/* ─── Slide-in Drawer ─── */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 0);
  backdrop-filter: blur(0px);
  z-index: var(--z-overlay);
  pointer-events: none;
  transition:
    background    var(--duration-slow),
    backdrop-filter var(--duration-slow),
    display       var(--duration-slow) allow-discrete,
    overlay       var(--duration-slow) allow-discrete;
}

.drawer-overlay[data-open="true"] {
  background: rgb(0 0 0 / 0.5);
  backdrop-filter: blur(4px);
  pointer-events: auto;
}

@starting-style {
  .drawer-overlay[data-open="true"] {
    background: rgb(0 0 0 / 0);
    backdrop-filter: blur(0px);
  }
}

.drawer {
  position: fixed;
  inset-block: 0;
  inset-inline-start: 0;
  width: min(360px, 85vw);
  background: var(--color-surface);
  box-shadow: var(--shadow-2xl);
  z-index: var(--z-modal);
  display: flex;
  flex-direction: column;
  overflow: hidden;

  translate: -100% 0;
  transition:
    translate var(--duration-slow) var(--ease-out),
    display   var(--duration-slow) allow-discrete,
    overlay   var(--duration-slow) allow-discrete;
}

.drawer[data-open="true"] {
  translate: 0 0;
}

@starting-style {
  .drawer[data-open="true"] {
    translate: -100% 0;
  }
}

/* Right drawer */
.drawer--right {
  inset-inline-start: auto;
  inset-inline-end: 0;
  translate: 100% 0;
}
.drawer--right[data-open="true"] {
  translate: 0 0;
}

/* Bottom sheet */
.drawer--bottom {
  inset-inline: 0;
  inset-block-start: auto;
  width: 100%;
  max-height: 90dvh;
  border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
  translate: 0 100%;
}
.drawer--bottom[data-open="true"] {
  translate: 0 0;
}

/* Drag handle for bottom sheet */
.drawer--bottom::before {
  content: '';
  display: block;
  width: 2.5rem;
  height: 4px;
  background: var(--color-border-strong);
  border-radius: var(--radius-full);
  margin: 0.75rem auto;
  flex-shrink: 0;
}

/* Drawer sections */
.drawer__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.drawer__body {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
  overscroll-behavior: contain;
}

.drawer__footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--color-border);
  flex-shrink: 0;
  display: flex;
  gap: var(--space-3);
  justify-content: flex-end;
}
```

### 76.2 Combobox / Autocomplete

```css
/* ─── Combobox (accessible autocomplete) ─── */
.combobox {
  position: relative;
}

.combobox__input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  transition:
    border-color var(--duration-fast),
    box-shadow   var(--duration-fast),
    border-radius var(--duration-fast);
}

.combobox:has(.combobox__listbox:not([hidden])) .combobox__input-wrapper {
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);
}

.combobox__input {
  flex: 1;
  border: none;
  background: none;
  font: inherit;
  color: var(--color-text);
  outline: none;
  min-width: 0;
}

.combobox__toggle {
  padding: 0;
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: transform var(--duration-fast);
}

.combobox:has(.combobox__listbox:not([hidden])) .combobox__toggle {
  transform: rotate(180deg);
}

/* Listbox */
.combobox__listbox {
  position: absolute;
  top: 100%;
  inset-inline: 0;
  max-height: 256px;
  overflow-y: auto;
  background: var(--color-surface);
  border: 1px solid var(--color-accent);
  border-top: none;
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  box-shadow: var(--shadow-xl);
  z-index: var(--z-dropdown);
  overscroll-behavior: contain;
  scrollbar-width: thin;
}

.combobox__option {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.625rem 0.75rem;
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: background var(--duration-fast);
}

.combobox__option:hover,
.combobox__option[aria-selected="true"] {
  background: var(--color-bg-subtle);
}

.combobox__option[data-active="true"] {
  background: color-mix(in srgb, var(--color-accent) 10%, transparent);
  color: var(--color-accent);
}

/* Highlight matching text */
.combobox__option mark {
  background: color-mix(in srgb, var(--color-warning-500) 30%, transparent);
  color: inherit;
  border-radius: 2px;
}

/* Group headers */
.combobox__group-label {
  padding: 0.375rem 0.75rem;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  position: sticky;
  top: 0;
  background: var(--color-surface);
  z-index: 1;
}

/* No results */
.combobox__empty {
  padding: var(--space-4);
  text-align: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
}
```

### 76.3 Date Picker

```css
/* ─── Calendar / Date Picker ─── */
.datepicker {
  position: relative;
  display: inline-block;
}

.datepicker__trigger {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  font: inherit;
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: border-color var(--duration-fast);
}
.datepicker__trigger:hover { border-color: var(--color-neutral-400); }
.datepicker__trigger:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.datepicker__popup {
  position: absolute;
  top: calc(100% + 8px);
  inset-inline-start: 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  padding: var(--space-4);
  z-index: var(--z-dropdown);
  width: 280px;
  
  /* Open animation */
  animation: popup-appear var(--duration-normal) var(--ease-out);
}

@keyframes popup-appear {
  from { opacity: 0; translate: 0 -8px; scale: 0.97; }
  to   { opacity: 1; translate: 0 0; scale: 1; }
}

/* Calendar header */
.cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.cal-header__title {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-md);
  transition: background var(--duration-fast);
}
.cal-header__title:hover { background: var(--color-bg-subtle); }

.cal-nav {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: var(--radius-md);
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.cal-nav:hover {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

/* Day grid */
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}

.cal-weekday {
  text-align: center;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  padding: 0.25rem 0;
}

.cal-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-sm);
  border-radius: var(--radius-md);
  cursor: pointer;
  border: none;
  background: none;
  color: var(--color-text);
  transition:
    background var(--duration-fast),
    color      var(--duration-fast),
    scale      var(--duration-fast) var(--ease-bounce);
  font-variant-numeric: tabular-nums;
}

.cal-day:hover {
  background: var(--color-bg-subtle);
  scale: 1.1;
}
.cal-day:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
.cal-day--outside { color: var(--color-text-subtle); }
.cal-day--today {
  font-weight: var(--font-weight-bold);
  color: var(--color-accent);
}
.cal-day--selected {
  background: var(--color-accent);
  color: white;
}
.cal-day--selected:hover { background: var(--color-accent-hover); }
.cal-day--disabled {
  opacity: 0.3;
  cursor: not-allowed;
  pointer-events: none;
}

/* Range selection */
.cal-day--in-range {
  background: color-mix(in srgb, var(--color-accent) 15%, transparent);
  border-radius: 0;
}
.cal-day--range-start { border-radius: var(--radius-md) 0 0 var(--radius-md); }
.cal-day--range-end   { border-radius: 0 var(--radius-md) var(--radius-md) 0; }
```

### 76.4 Context Menu / Right-click Menu

```css
/* ─── Context Menu ─── */
.context-menu {
  position: fixed;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: var(--space-1);
  z-index: var(--z-popover);
  min-width: 180px;
  max-width: 240px;

  /* Position set by JS */
  top: var(--y, 0);
  left: var(--x, 0);

  animation: context-appear 0.12s var(--ease-out);
  transform-origin: var(--origin-x, left) var(--origin-y, top);
}

@keyframes context-appear {
  from { opacity: 0; scale: 0.92; }
  to   { opacity: 1; scale: 1; }
}

.context-menu__item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  color: var(--color-text);
  border: none;
  background: none;
  width: 100%;
  text-align: start;
  transition: background var(--duration-fast);
}

.context-menu__item:hover {
  background: var(--color-bg-subtle);
}

.context-menu__item--danger {
  color: var(--color-danger-500);
}
.context-menu__item--danger:hover {
  background: var(--color-danger-100);
}

.context-menu__item--disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

.context-menu__shortcut {
  margin-inline-start: auto;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.context-menu__separator {
  height: 1px;
  background: var(--color-border);
  margin: var(--space-1) 0;
}

.context-menu__label {
  padding: 0.25rem 0.75rem;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
}

/* Nested submenu */
.context-menu__item--submenu::after {
  content: '›';
  margin-inline-start: auto;
  opacity: 0.5;
}

.context-menu__submenu {
  position: absolute;
  top: 0;
  left: 100%;
  margin-left: 4px;
  /* Same styles as .context-menu */
}
.context-menu__item--submenu:hover .context-menu__submenu {
  display: block;
}
```

### 76.5 Multi-select / Tag Input

```css
/* ─── Tag Input ─── */
.tag-input {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  padding: 0.375rem 0.75rem;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  min-height: 2.5rem;
  cursor: text;
  align-items: center;
  transition:
    border-color var(--duration-fast),
    box-shadow   var(--duration-fast);
}

.tag-input:focus-within {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);
}

/* Individual tags */
.tag-input__tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.125rem 0.5rem;
  background: var(--color-brand-100);
  color: var(--color-brand-700);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  max-width: 180px;
  animation: tag-appear 0.2s var(--ease-bounce);
}

@keyframes tag-appear {
  from { scale: 0.7; opacity: 0; }
  to   { scale: 1; opacity: 1; }
}

.tag-input__tag span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tag-input__remove {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  border: none;
  background: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.6;
  flex-shrink: 0;
  padding: 0;
  transition: opacity var(--duration-fast), background var(--duration-fast);
}
.tag-input__remove:hover {
  opacity: 1;
  background: color-mix(in srgb, currentColor 15%, transparent);
}

/* Dismissing tag */
.tag-input__tag.removing {
  animation: tag-remove 0.15s var(--ease-in) forwards;
}

@keyframes tag-remove {
  to { scale: 0; opacity: 0; width: 0; padding: 0; margin: 0; }
}

/* Input */
.tag-input__input {
  border: none;
  background: none;
  font: inherit;
  font-size: var(--font-size-sm);
  color: var(--color-text);
  outline: none;
  flex: 1;
  min-width: 80px;
}
```

---

## 77. CSS FOR PROSE CONTENT

### 77.1 Typography for Long-form Reading

```css
/* ─── The Prose Component ─── */
.prose {
  /* Measure (line length) */
  max-width: 65ch;
  
  /* Base typography */
  font-size: clamp(1rem, 1.5vw + 0.5rem, 1.125rem);
  line-height: var(--line-height-relaxed);
  color: var(--color-text);
  
  /* Hanging punctuation */
  hanging-punctuation: first last;
}

/* ─── Vertical rhythm ─── */
.prose > * {
  margin-block: 0;
}

.prose > * + * {
  margin-block-start: 1em;
}

/* Tighter after headings */
.prose h2 + *,
.prose h3 + *,
.prose h4 + * {
  margin-block-start: 0.5em;
}

/* ─── Headings ─── */
.prose h1, .prose h2, .prose h3,
.prose h4, .prose h5, .prose h6 {
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  text-wrap: balance;
  margin-block-start: 2em;
}

.prose h1 { font-size: var(--step-4); }
.prose h2 { font-size: var(--step-3); }
.prose h3 { font-size: var(--step-2); }
.prose h4 { font-size: var(--step-1); }
.prose h5, .prose h6 { font-size: var(--step-0); }

/* Anchors on headings */
.prose :is(h2, h3, h4) .heading-anchor {
  opacity: 0;
  margin-inline-start: 0.5em;
  color: var(--color-text-muted);
  text-decoration: none;
  font-weight: normal;
  transition: opacity var(--duration-fast);
}
.prose :is(h2, h3, h4):hover .heading-anchor {
  opacity: 1;
}

/* ─── Paragraphs ─── */
.prose p {
  overflow-wrap: break-word;
  text-wrap: pretty;
}

/* ─── Links ─── */
.prose a {
  color: var(--color-accent);
  text-decoration-line: underline;
  text-decoration-color: color-mix(in srgb, var(--color-accent) 40%, transparent);
  text-underline-offset: 0.2em;
  text-decoration-thickness: 1px;
  transition:
    text-decoration-color var(--duration-fast),
    text-decoration-thickness var(--duration-fast);
}

.prose a:hover {
  text-decoration-color: var(--color-accent);
  text-decoration-thickness: 2px;
}

/* ─── Lists ─── */
.prose ul, .prose ol {
  padding-inline-start: 1.5em;
}

.prose ul { list-style-type: disc; }
.prose ol { list-style-type: decimal; }

.prose li + li { margin-block-start: 0.5em; }
.prose li > ul, .prose li > ol { margin-block-start: 0.5em; }

/* Custom bullet */
.prose ul li::marker {
  color: var(--color-accent);
  font-size: 0.8em;
}

/* ─── Blockquote ─── */
.prose blockquote {
  border-inline-start: 3px solid var(--color-accent);
  padding-inline-start: 1.5em;
  padding-block: 0.25em;
  color: var(--color-text-muted);
  font-style: italic;
  font-size: 1.05em;
  quotes: '\201C' '\201D';
}

.prose blockquote::before {
  content: open-quote;
  font-size: 3em;
  line-height: 0;
  vertical-align: -0.5em;
  color: var(--color-accent);
  margin-inline-end: 0.1em;
}

/* ─── Code blocks ─── */
.prose pre {
  background: var(--color-neutral-900);
  color: var(--color-neutral-100);
  padding: 1.25em 1.5em;
  border-radius: var(--radius-lg);
  overflow-x: auto;
  font-size: 0.875em;
  line-height: 1.7;
  tab-size: 2;
  hyphens: none;
  margin-block: 1.5em;
  position: relative;
}

/* Line numbers */
.prose pre[data-line-numbers] {
  counter-reset: line;
  padding-inline-start: 3.5em;
}
.prose pre[data-line-numbers] .line::before {
  counter-increment: line;
  content: counter(line);
  position: absolute;
  left: 1em;
  color: var(--color-neutral-600);
  user-select: none;
  text-align: right;
  width: 1.5em;
}

/* Copy button for code */
.prose pre .copy-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  opacity: 0;
  transition: opacity var(--duration-fast);
}
.prose pre:hover .copy-btn { opacity: 1; }

/* Inline code */
.prose code:not(pre code) {
  background: var(--color-bg-muted);
  padding: 0.125em 0.375em;
  border-radius: var(--radius-sm);
  font-size: 0.875em;
  font-family: var(--font-mono);
  color: var(--color-text);
  word-break: break-all;
}

/* ─── Tables ─── */
.prose table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875em;
  margin-block: 1.5em;
  overflow-x: auto;
  display: block;
}

.prose th, .prose td {
  padding: 0.5em 0.75em;
  text-align: start;
  border: 1px solid var(--color-border);
}

.prose th {
  background: var(--color-bg-subtle);
  font-weight: var(--font-weight-semibold);
}

.prose tbody tr:nth-child(even) {
  background: var(--color-bg-subtle);
}

/* ─── HR ─── */
.prose hr {
  border: none;
  height: 1px;
  background: var(--color-border);
  margin-block: 2em;
}

/* Fancy HR */
.prose hr.fancy {
  display: flex;
  align-items: center;
  gap: 1em;
  border: none;
  height: auto;
}
.prose hr.fancy::before,
.prose hr.fancy::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-border);
}
.prose hr.fancy::before { content: '❧'; flex: none; }

/* ─── Images in prose ─── */
.prose img {
  border-radius: var(--radius-lg);
  margin-block: 1.5em;
}

.prose figure {
  margin-inline: 0;
  margin-block: 2em;
}

.prose figcaption {
  text-align: center;
  font-size: 0.875em;
  color: var(--color-text-muted);
  font-style: italic;
  margin-block-start: 0.5em;
}

/* ─── Callout / Note boxes ─── */
.prose .callout {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-lg);
  border-inline-start: 4px solid var(--callout-color, var(--color-brand-500));
  background: color-mix(in srgb, var(--callout-color, var(--color-brand-500)) 8%, var(--color-surface));
}

.prose .callout--info    { --callout-color: var(--color-brand-500); }
.prose .callout--warning { --callout-color: var(--color-warning-500); }
.prose .callout--danger  { --callout-color: var(--color-danger-500); }
.prose .callout--success { --callout-color: var(--color-success-500); }

/* ─── Footnotes ─── */
.prose .footnotes {
  margin-block-start: 3em;
  padding-block-start: 2em;
  border-block-start: 1px solid var(--color-border);
  font-size: 0.875em;
  color: var(--color-text-muted);
}

.prose .footnote-ref {
  font-size: 0.75em;
  vertical-align: super;
  font-variant-numeric: tabular-nums;
  line-height: 0;
}
```

---

## 78. CSS IMAGE GALLERIES

### 78.1 Masonry Gallery

```css
/* ─── CSS Column Masonry (simple) ─── */
.gallery-masonry {
  column-count: 3;
  column-gap: var(--space-4);
  column-fill: balance;
}

.gallery-masonry .item {
  break-inside: avoid;
  margin-bottom: var(--space-4);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

/* Responsive masonry */
.gallery-masonry {
  column-count: 1;
}
@media (min-width: 480px) { .gallery-masonry { column-count: 2; } }
@media (min-width: 768px) { .gallery-masonry { column-count: 3; } }
@media (min-width: 1200px) { .gallery-masonry { column-count: 4; } }

/* Or: Native CSS masonry (behind flag) */
.gallery-native-masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-template-rows: masonry;
  gap: var(--space-4);
}

/* ─── Grid-based mosaic ─── */
.gallery-mosaic {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-auto-rows: 60px;
  gap: var(--space-3);
}

.gallery-mosaic .item {
  border-radius: var(--radius-lg);
  overflow: hidden;
  position: relative;
}

.gallery-mosaic .item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--duration-slow) var(--ease-out);
}

.gallery-mosaic .item:hover img {
  transform: scale(1.05);
}

/* Predefined mosaic patterns */
.gallery-mosaic .item:nth-child(1)  { grid-column: span 6; grid-row: span 5; }
.gallery-mosaic .item:nth-child(2)  { grid-column: span 3; grid-row: span 3; }
.gallery-mosaic .item:nth-child(3)  { grid-column: span 3; grid-row: span 3; }
.gallery-mosaic .item:nth-child(4)  { grid-column: span 3; grid-row: span 2; }
.gallery-mosaic .item:nth-child(5)  { grid-column: span 3; grid-row: span 2; }
.gallery-mosaic .item:nth-child(6)  { grid-column: span 4; grid-row: span 3; }
.gallery-mosaic .item:nth-child(7)  { grid-column: span 4; grid-row: span 3; }
.gallery-mosaic .item:nth-child(8)  { grid-column: span 4; grid-row: span 3; }
```

### 78.2 Lightbox / Image Viewer

```css
/* ─── CSS-only lightbox (via :target) ─── */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 0);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  z-index: var(--z-modal);
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-slow), background var(--duration-slow);
}

.lightbox:target {
  opacity: 1;
  background: rgb(0 0 0 / 0.9);
  pointer-events: auto;
  backdrop-filter: blur(8px);
}

.lightbox__inner {
  position: relative;
  max-width: min(90vw, 1200px);
  max-height: 90dvh;
  transform: scale(0.9);
  transition: transform var(--duration-slow) var(--ease-bounce);
}

.lightbox:target .lightbox__inner {
  transform: scale(1);
}

.lightbox__close {
  position: absolute;
  top: -3rem;
  right: 0;
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  opacity: 0.7;
  transition: opacity var(--duration-fast);
}
.lightbox__close:hover { opacity: 1; }

.lightbox__img {
  display: block;
  max-width: 100%;
  max-height: 80dvh;
  border-radius: var(--radius-lg);
  object-fit: contain;
  box-shadow: var(--shadow-2xl);
}

.lightbox__caption {
  color: rgb(255 255 255 / 0.7);
  text-align: center;
  padding: var(--space-3);
  font-size: var(--font-size-sm);
}

/* ─── Image hover zoom ─── */
.gallery-zoom-item {
  overflow: hidden;
  border-radius: var(--radius-lg);
  position: relative;
}

.gallery-zoom-item img {
  transition:
    transform var(--duration-slow) var(--ease-out),
    filter    var(--duration-slow) var(--ease-out);
  display: block;
  width: 100%;
}

.gallery-zoom-item:hover img {
  transform: scale(1.08);
  filter: brightness(0.85);
}

/* Reveal overlay on hover */
.gallery-zoom-item .overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity var(--duration-normal);
  background: linear-gradient(
    to top,
    rgb(0 0 0 / 0.7) 0%,
    transparent 50%
  );
}

.gallery-zoom-item:hover .overlay {
  opacity: 1;
}
```

---

## 79. CSS FOR CODE BLOCKS

### 79.1 Syntax Highlighting Themes

```css
/* ─── Dark code theme (Monokai-inspired) ─── */
.code-block {
  --code-bg:        #272822;
  --code-text:      #f8f8f2;
  --code-comment:   #75715e;
  --code-keyword:   #f92672;
  --code-string:    #e6db74;
  --code-number:    #ae81ff;
  --code-function:  #a6e22e;
  --code-operator:  #f92672;
  --code-class:     #66d9ef;
  --code-property:  #66d9ef;
  --code-variable:  #fd971f;
  --code-tag:       #f92672;
  --code-attr:      #a6e22e;

  background: var(--code-bg);
  color: var(--code-text);
  font-family: var(--font-mono);
  font-size: 0.875em;
  line-height: 1.7;
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  overflow-x: auto;
  tab-size: 2;
  white-space: pre;
  -webkit-overflow-scrolling: touch;
}

.code-block .token.comment    { color: var(--code-comment); font-style: italic; }
.code-block .token.keyword    { color: var(--code-keyword); }
.code-block .token.string     { color: var(--code-string); }
.code-block .token.number     { color: var(--code-number); }
.code-block .token.function   { color: var(--code-function); }
.code-block .token.operator   { color: var(--code-operator); }
.code-block .token.class-name { color: var(--code-class); }
.code-block .token.property   { color: var(--code-property); }
.code-block .token.variable   { color: var(--code-variable); }
.code-block .token.tag        { color: var(--code-tag); }
.code-block .token.attr-name  { color: var(--code-attr); }

/* ─── Light code theme ─── */
.code-block--light {
  --code-bg:       #f8f8f8;
  --code-text:     #383a42;
  --code-comment:  #a0a1a7;
  --code-keyword:  #a626a4;
  --code-string:   #50a14f;
  --code-number:   #986801;
  --code-function: #4078f2;
  --code-class:    #c18401;
}

/* ─── Code window chrome ─── */
.code-window {
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-xl);
}

.code-window__titlebar {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.75rem 1rem;
  background: #3c3c3c;
}

.code-window__dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
.code-window__dot:nth-child(1) { background: #ff5f56; }
.code-window__dot:nth-child(2) { background: #ffbd2e; }
.code-window__dot:nth-child(3) { background: #27c93f; }

.code-window__filename {
  margin-inline-start: auto;
  margin-inline-end: auto;
  font-size: var(--font-size-xs);
  color: rgb(255 255 255 / 0.6);
  font-family: var(--font-mono);
}

/* ─── Diff code blocks ─── */
.code-diff .line-added {
  background: color-mix(in srgb, var(--color-success-500) 15%, transparent);
  display: block;
  margin-inline: -1.5rem;
  padding-inline: 1.5rem;
}
.code-diff .line-added::before {
  content: '+';
  color: var(--color-success-500);
  margin-inline-end: 0.5em;
}

.code-diff .line-removed {
  background: color-mix(in srgb, var(--color-danger-500) 15%, transparent);
  display: block;
  margin-inline: -1.5rem;
  padding-inline: 1.5rem;
  text-decoration: line-through;
  opacity: 0.7;
}
.code-diff .line-removed::before {
  content: '-';
  color: var(--color-danger-500);
  margin-inline-end: 0.5em;
}
```

---

## 80. CSS SPRING PHYSICS ANIMATIONS

### 80.1 Spring-like Motion via CSS

```css
/* ─── Spring easing approximations ─── */
:root {
  /* Gentle spring */
  --spring-gentle: linear(
    0, 0.014 2.7%, 0.106 6.2%, 0.378 13.2%, 0.827 21.3%, 1.005 25.2%,
    1.094 28.7%, 1.129 30.7%, 1.151 32.7%, 1.152 34.2%, 1.135 36.5%,
    1.073 41.5%, 1.017 47.5%, 1
  );

  /* Bouncy spring */
  --spring-bouncy: linear(
    0, 0.009 1.9%, 0.069 4.3%, 0.274 8.8%, 0.95 15.8%, 1.14 19.5%,
    1.196 22.1%, 1.208 24.4%, 1.196 26.8%, 1.126 31.2%,
    1.034 37.1%, 1.005 39.8%, 0.994 42.7%, 1
  );

  /* Stiff spring */
  --spring-stiff: linear(
    0, 0.052 3.7%, 0.231 7.6%, 0.738 15.5%, 1.018 19.6%, 1.071 22.6%,
    1.07 25.2%, 1.042 28.1%, 1.007 32.6%, 0.997 36.9%, 1
  );

  /* Wobbly spring */
  --spring-wobbly: linear(
    0, 0.004 1.1%, 0.033 2.9%, 0.123 6.1%, 0.471 12.5%, 0.704 16.4%,
    0.805 18.9%, 0.906 22.7%, 0.965 26.8%, 0.992 30.7%,
    1.001 34.5%, 1.004 38%, 1.001 41.6%, 0.999 46.1%, 1
  );
}

/* ─── Usage examples ─── */
.spring-appear {
  scale: 0;
  opacity: 0;
  transition:
    scale   0.5s var(--spring-bouncy),
    opacity 0.3s ease-out;
}

.spring-appear.visible {
  scale: 1;
  opacity: 1;
}

.spring-hover {
  transition: transform 0.4s var(--spring-gentle);
}
.spring-hover:hover {
  transform: translateY(-4px) scale(1.02);
}

.spring-press {
  transition: scale 0.15s var(--spring-stiff);
}
.spring-press:active {
  scale: 0.95;
}

/* ─── Staggered spring entrance ─── */
.spring-list .item {
  opacity: 0;
  translate: 0 20px;
  animation: spring-in var(--spring-bouncy) 0.5s forwards;
  animation-delay: calc(var(--i, 0) * 80ms);
}

@keyframes spring-in {
  to { opacity: 1; translate: 0 0; }
}

/* ─── WAAPI (Web Animations API) with springs ─── */
/*
element.animate([
  { transform: 'scale(0)', opacity: 0 },
  { transform: 'scale(1)', opacity: 1 }
], {
  duration: 500,
  easing: 'linear(0, 0.009 1.9%, 0.069 4.3%, ... 1)',
  fill: 'both'
});
*/
```

---

## 81. CSS FOR EMPTY STATES & ERROR STATES

### 81.1 Empty State Patterns

```css
/* ─── Empty state component ─── */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-16) var(--space-8);
  gap: var(--space-4);
}

.empty-state__illustration {
  width: min(200px, 60%);
  height: auto;
  opacity: 0.6;
  filter: grayscale(30%);
}

/* CSS-only illustration placeholder */
.empty-state__icon {
  width: 80px;
  height: 80px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: var(--color-text-muted);
  margin-inline: auto;
}

.empty-state__title {
  font-size: var(--step-1);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
}

.empty-state__description {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  max-width: 40ch;
  text-wrap: balance;
}

/* ─── Auto-show empty state when container is empty ─── */
.auto-empty {
  position: relative;
}

.auto-empty > .empty-state {
  display: none;
}

/* Show when no real children */
.auto-empty:not(:has(> :not(.empty-state))) > .empty-state {
  display: flex;
}

/* ─── Empty list with dash pattern ─── */
.empty-list-placeholder {
  padding: var(--space-8);
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition:
    border-color var(--duration-fast),
    background   var(--duration-fast);
}

.empty-list-placeholder:hover {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 5%, transparent);
  color: var(--color-accent);
}

/* ─── Drag and drop target ─── */
.drop-zone {
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-12);
  text-align: center;
  transition:
    border-color var(--duration-fast),
    background   var(--duration-fast),
    scale        var(--duration-fast) var(--ease-bounce);
}

.drop-zone[data-dragging="true"],
.drop-zone:focus-within {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 8%, transparent);
  scale: 1.01;
}
```

### 81.2 Error & Validation States

```css
/* ─── Form error patterns ─── */
.field--error .input {
  border-color: var(--color-danger-500);
  background: var(--color-danger-100);
}

.field--error .input:focus {
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-danger-500) 20%, transparent);
}

.field--error .label {
  color: var(--color-danger-700);
}

/* Shake animation for invalid submit */
.field--error.shake {
  animation: field-shake 0.4s var(--ease-out);
}

@keyframes field-shake {
  0%, 100% { translate: 0; }
  20%       { translate: -6px; }
  40%       { translate: 6px; }
  60%       { translate: -4px; }
  80%       { translate: 4px; }
}

/* ─── Error message ─── */
.error-message {
  display: flex;
  align-items: flex-start;
  gap: 0.375rem;
  font-size: var(--font-size-xs);
  color: var(--color-danger-600);
  margin-block-start: var(--space-1);
  animation: error-appear 0.2s var(--ease-out);
}

@keyframes error-appear {
  from { opacity: 0; translate: 0 -4px; }
  to   { opacity: 1; translate: 0 0; }
}

/* ─── 404 / Error page ─── */
.error-page {
  min-height: 100dvh;
  display: grid;
  place-items: center;
  padding: var(--space-8);
  text-align: center;
}

.error-page__code {
  font-size: clamp(4rem, 15vw, 12rem);
  font-weight: var(--font-weight-black);
  line-height: 1;
  background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-700));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  user-select: none;
  letter-spacing: -0.05em;
}

/* Glitch effect for error code */
.error-page__code--glitch {
  position: relative;
}

.error-page__code--glitch::before,
.error-page__code--glitch::after {
  content: attr(data-text);
  position: absolute;
  inset: 0;
  background: inherit;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.error-page__code--glitch::before {
  animation: glitch-1 0.3s infinite;
  clip-path: polygon(0 0, 100% 0, 100% 35%, 0 35%);
}

.error-page__code--glitch::after {
  animation: glitch-2 0.3s infinite;
  clip-path: polygon(0 65%, 100% 65%, 100% 100%, 0 100%);
}

@keyframes glitch-1 {
  0%, 100% { translate: 0; }
  20%  { translate: -3px 0; filter: hue-rotate(90deg); }
  40%  { translate: 3px 0; }
  60%  { translate: -1px 0; filter: hue-rotate(-90deg); }
  80%  { translate: 1px 0; }
}

@keyframes glitch-2 {
  0%, 100% { translate: 0; }
  30%  { translate: 3px 0; filter: hue-rotate(90deg); }
  50%  { translate: -3px 0; }
  70%  { translate: 2px 0; filter: hue-rotate(-90deg); }
  90%  { translate: -1px 0; }
}
```

---

## 82. CSS SELECTOR PERFORMANCE

### 82.1 Selector Efficiency

```css
/**
 * CSS selectors are matched RIGHT to LEFT.
 * Browser first finds all elements matching the rightmost part,
 * then walks up the DOM checking parents.
 *
 * Performance order (fastest → slowest):
 *
 * 1. ID:           #id               (1 element, instant)
 * 2. Class:        .class            (indexed by browser)
 * 3. Type:         div               (indexed by browser)
 * 4. Adjacent:     .a + .b
 * 5. Child:        .a > .b
 * 6. Descendant:   .a .b             (can be slow for large DOMs)
 * 7. Universal:    *                 (matches everything)
 * 8. Attribute:    [attr="value"]    (not indexed)
 * 9. Pseudo:       :nth-child()      (recalculated on DOM changes)
 * 10. :has()       :has(.child)      (expensive — triggers parent check)
 */

/* ─── Anti-patterns ─── */

/* ❌ Over-qualified — redundant type */
div.container { }        /* .container is enough */
ul.list li.item { }     /* .item is enough */

/* ❌ Overly deep descendant */
.header .nav .nav-list .nav-item .nav-link { }
/* ✅ Just: */
.nav-link { }

/* ❌ Inefficient universal with descendant */
.container * { box-sizing: border-box; }
/* ✅ One rule at root */
*, *::before, *::after { box-sizing: border-box; }

/* ❌ Expensive :nth-child in large lists */
.list-item:nth-child(odd) { }   /* recalculated on every DOM change */
/* ✅ Add class in JS for large dynamic lists */
.list-item.odd { }

/* ─── :has() performance notes ─── */
/* :has() triggers a "subject" invalidation —
   browser must check parents when DOM changes.
   Use sparingly on frequently-updating content. */

/* ✅ OK: on static content */
.card:has(img) { padding: 0; }

/* ⚠️ Expensive: on frequently updating elements */
body:has(.input:focus) { }  /* triggers full-page recalc on every focus */
/* ✅ Better: scope to nearest container */
.form:has(.input:focus) { }
```

---

## 83. BROWSER-SPECIFIC CSS

### 83.1 Browser Detection via CSS

```css
/* ─── Feature detection (preferred) ─── */
@supports (display: grid) { }
@supports (backdrop-filter: blur(1px)) { }
@supports (-webkit-backdrop-filter: blur(1px)) {
  /* Safari specific */
  .glass { -webkit-backdrop-filter: blur(10px); }
}

/* ─── Browser-specific hacks (last resort) ─── */

/* Safari only */
@supports (-webkit-appearance: none) and (not (overflow: -webkit-marquee)) and (not (-ms-ime-align: auto)) {
  .safari-fix { -webkit-transform: translateZ(0); }
}

/* Chrome / Edge (not Firefox, not Safari) */
@supports (-webkit-appearance: none) and (not (gap: 0)) {
  .chrome-fix { }
}

/* Firefox only */
@-moz-document url-prefix() {
  .firefox-fix { scrollbar-width: thin; }
}

/* ─── Vendor prefixes still needed ─── */

/* WebKit scrollbar (Chrome, Edge, Safari) */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: var(--color-border-strong);
  border-radius: 4px;
}

/* Backdrop filter */
.frosted {
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
}

/* Font smoothing */
body {
  -webkit-font-smoothing: antialiased;    /* macOS/iOS WebKit */
  -moz-osx-font-smoothing: grayscale;    /* macOS Firefox */
}

/* Text stroke */
.outlined {
  -webkit-text-stroke: 1px currentColor;
  text-stroke: 1px currentColor;
}

/* ─── iOS-specific ─── */
/* Prevent zoom on input focus (iOS Safari zooms when font-size < 16px) */
input, select, textarea {
  font-size: max(16px, 1rem);
}

/* Fix for iOS momentum scroll in overflow containers */
.scroll-ios {
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
}

/* Disable iOS callout menu on long-press */
.no-callout {
  -webkit-touch-callout: none;
}

/* ─── Windows High Contrast Mode ─── */
@media (forced-colors: active) {
  .btn {
    border: 2px solid ButtonText;
    background: ButtonFace;
    color: ButtonText;
  }
  
  .btn:hover {
    border-color: Highlight;
    color: Highlight;
  }
  
  .card {
    border: 1px solid CanvasText;
  }
  
  /* Preserve custom colors for decorative elements */
  .icon-decorative {
    forced-color-adjust: none;
  }
}

/* ─── Print-specific browser resets ─── */
@media print {
  /* Chrome adds URLs to links */
  a::after { content: none !important; }
  
  /* Firefox adds "Printed by..." */
  /* Can't be controlled via CSS */
}
```

---

## 84. CSS LOGICAL PROPERTIES — COMPLETE REFERENCE TABLE

```css
/*
╔══════════════════════════════════════════════════════════════════════╗
║  PHYSICAL PROPERTY         → LOGICAL PROPERTY                        ║
╠══════════════════════════════════════════════════════════════════════╣
║  Width / Height                                                       ║
║  width                     → inline-size                             ║
║  height                    → block-size                              ║
║  min-width                 → min-inline-size                         ║
║  max-width                 → max-inline-size                         ║
║  min-height                → min-block-size                          ║
║  max-height                → max-block-size                          ║
╠══════════════════════════════════════════════════════════════════════╣
║  Margin                                                               ║
║  margin-top                → margin-block-start                      ║
║  margin-bottom             → margin-block-end                        ║
║  margin-left               → margin-inline-start                     ║
║  margin-right              → margin-inline-end                       ║
║  margin: T R B L           → margin-block: T B; margin-inline: L R  ║
╠══════════════════════════════════════════════════════════════════════╣
║  Padding                                                              ║
║  padding-top               → padding-block-start                     ║
║  padding-bottom            → padding-block-end                       ║
║  padding-left              → padding-inline-start                    ║
║  padding-right             → padding-inline-end                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Position                                                             ║
║  top                       → inset-block-start                       ║
║  bottom                    → inset-block-end                         ║
║  left                      → inset-inline-start                      ║
║  right                     → inset-inline-end                        ║
║  top + bottom              → inset-block                             ║
║  left + right              → inset-inline                            ║
║  top+right+bottom+left     → inset                                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  Border                                                               ║
║  border-top                → border-block-start                      ║
║  border-bottom             → border-block-end                        ║
║  border-left               → border-inline-start                     ║
║  border-right              → border-inline-end                       ║
║  border-top-width          → border-block-start-width                ║
║  border-top-style          → border-block-start-style                ║
║  border-top-color          → border-block-start-color                ║
╠══════════════════════════════════════════════════════════════════════╣
║  Border Radius                                                        ║
║  border-top-left-radius    → border-start-start-radius               ║
║  border-top-right-radius   → border-start-end-radius                 ║
║  border-bottom-left-radius → border-end-start-radius                 ║
║  border-bottom-right-radius→ border-end-end-radius                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  Text & Other                                                         ║
║  text-align: left          → text-align: start                       ║
║  text-align: right         → text-align: end                         ║
║  float: left               → float: inline-start                     ║
║  float: right              → float: inline-end                       ║
║  clear: left               → clear: inline-start                     ║
║  clear: right              → clear: inline-end                       ║
║  resize: horizontal        → resize: inline                          ║
║  resize: vertical          → resize: block                           ║
║  overscroll-behavior-x     → overscroll-behavior-inline              ║
║  overscroll-behavior-y     → overscroll-behavior-block               ║
╠══════════════════════════════════════════════════════════════════════╣
║  Writing Mode Mapping (horizontal-tb LTR = default)                   ║
║                                                                        ║
║  Direction    block-start  block-end  inline-start  inline-end        ║
║  ─────────────────────────────────────────────────────────────────── ║
║  horiz. LTR   top          bottom     left          right             ║
║  horiz. RTL   top          bottom     right         left              ║
║  vert.  LTR   left         right      top           bottom            ║
║  vert.  RTL   right        left       top           bottom            ║
╚══════════════════════════════════════════════════════════════════════╝
*/
```

---

## 85. CSS CUSTOM PROPERTIES — ADVANCED PATTERNS

### 85.1 Space-toggle Technique

```css
/*
 * The "Space Toggle" technique — CSS variables as boolean switches.
 * 0 = falsy (empty value = turns off property)
 * initial = truthy (valid value = turns on property)
 *
 * Author: Lea Verou / Ana Tudor
 */

.element {
  --is-dark: ;          /* initial (truthy) */
  --is-light: initial;  /* initial (truthy) */

  /* Space toggle usage */
  background:
    var(--is-dark, black)
    var(--is-light, white);
  /* Only ONE will be valid — the other's var() resolves to empty */
}

/* Flip the switch */
.dark-context {
  --is-dark: initial;
  --is-light: ;
}

/* ─── Practical example: component theming ─── */
.alert {
  --success: ;
  --warning: ;
  --error:   ;

  background: var(--success, var(--color-success-100))
              var(--warning, var(--color-warning-100))
              var(--error,   var(--color-danger-100));
  color:      var(--success, var(--color-success-900))
              var(--warning, var(--color-warning-900))
              var(--error,   var(--color-danger-900));
}

.alert--success { --success: initial; }
.alert--warning { --warning: initial; }
.alert--error   { --error:   initial; }
```

### 85.2 CSS Variable Tricks

```css
/* ─── Responsive props without media queries ─── */
:root {
  /* Clamp-based responsive spacing */
  --space-responsive: clamp(
    var(--space-4),
    5vw,
    var(--space-12)
  );
}

/* ─── Inherited token override pattern ─── */
/* Parent sets context */
.theme-compact {
  --card-padding: var(--space-4);
  --card-gap: var(--space-2);
  --font-scale: 0.9;
}

/* Child reads context */
.card {
  padding: var(--card-padding, var(--space-6));
  gap: var(--card-gap, var(--space-4));
  font-size: calc(var(--font-scale, 1) * 1rem);
}

/* ─── CSS-only dark mode toggle via variables ─── */
:root {
  --scheme: light;
  
  /* Light defaults */
  --bg: white;
  --text: #111;
}

/* Applied when JS sets data-theme */
[data-theme="dark"] {
  --scheme: dark;
  --bg: #111;
  --text: white;
}

/* Smooth transition between themes */
*, *::before, *::after {
  transition:
    background-color 0.3s,
    border-color 0.3s,
    color 0.3s;
}

/* Except interactive elements (feels laggy) */
button, input, a {
  transition: none;
}

/* ─── Math with custom properties ─── */
:root {
  --cols: 3;
  --gap: 1rem;
  --col-width: calc((100% - var(--gap) * (var(--cols) - 1)) / var(--cols));
}

/* ─── CSS custom property as type guard ─── */
@property --opacity {
  syntax: '<number>';
  initial-value: 1;
  inherits: false;
}

/* Now invalid values silently fall back to initial: */
.element {
  --opacity: "not a number";  /* Falls back to 1 */
  opacity: var(--opacity);    /* = 1, not broken */
}
```

---

## 86. REAL-WORLD PAGE PATTERNS

### 86.1 Dashboard Layout

```css
/* ─── App Shell ─── */
.app-shell {
  display: grid;
  grid-template-areas:
    "sidebar header"
    "sidebar main";
  grid-template-columns: var(--sidebar-width, 240px) 1fr;
  grid-template-rows: var(--header-height, 60px) 1fr;
  min-height: 100dvh;
}

.app-header  { grid-area: header; }
.app-sidebar { grid-area: sidebar; }
.app-main    { grid-area: main; overflow-y: auto; }

/* Collapsible sidebar */
.app-shell[data-sidebar="collapsed"] {
  --sidebar-width: 64px;
}

.app-sidebar {
  transition: width var(--duration-slow) var(--ease-out);
  width: var(--sidebar-width, 240px);
  overflow: hidden;
}

/* Sidebar nav item */
.sidebar-nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.625rem 0.75rem;
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  white-space: nowrap;
  overflow: hidden;
  transition: background var(--duration-fast), color var(--duration-fast);
}

.sidebar-nav-item:hover {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

.sidebar-nav-item[aria-current="page"] {
  background: color-mix(in srgb, var(--color-accent) 12%, transparent);
  color: var(--color-accent);
}

.sidebar-nav-item .icon {
  flex-shrink: 0;
  width: 1.25rem;
  height: 1.25rem;
}

/* Hide label when collapsed */
.app-shell[data-sidebar="collapsed"] .sidebar-nav-item .label {
  opacity: 0;
  width: 0;
  pointer-events: none;
}

/* ─── Dashboard grid ─── */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-6);
  padding: var(--space-6);
  align-items: start;
}

/* Widget sizes */
.widget { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: var(--space-5); }
.widget--full   { grid-column: 1 / -1; }
.widget--half   { grid-column: span 6; }
.widget--third  { grid-column: span 4; }
.widget--quarter { grid-column: span 3; }

@media (max-width: 768px) {
  .app-shell {
    grid-template-areas: "header" "main";
    grid-template-columns: 1fr;
    grid-template-rows: var(--header-height, 60px) 1fr;
  }
  .app-sidebar {
    position: fixed;
    inset-block: 0;
    inset-inline-start: 0;
    z-index: var(--z-fixed);
    translate: -100%;
    transition: translate var(--duration-slow) var(--ease-out);
  }
  .app-sidebar[data-open="true"] {
    translate: 0;
  }
  .widget--half,
  .widget--third,
  .widget--quarter { grid-column: 1 / -1; }
}
```

### 86.2 Landing Page Patterns

```css
/* ─── Hero section ─── */
.hero {
  position: relative;
  min-height: 100dvh;
  display: grid;
  place-items: center;
  text-align: center;
  overflow: hidden;
  padding: var(--space-8);
}

.hero__background {
  position: absolute;
  inset: 0;
  z-index: 0;
  background: var(--color-bg);
}

/* Animated gradient background */
.hero__gradient {
  position: absolute;
  inset: -50%;
  background:
    radial-gradient(ellipse at 30% 40%, var(--color-brand-500) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 60%, var(--color-brand-300) 0%, transparent 50%);
  opacity: 0.15;
  animation: hero-drift 10s ease-in-out infinite alternate;
  filter: blur(60px);
}

@keyframes hero-drift {
  from { translate: -5% -5%; rotate: 0deg; }
  to   { translate: 5% 5%; rotate: 5deg; }
}

.hero__content {
  position: relative;
  z-index: 1;
  max-width: 60rem;
}

.hero__eyebrow {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.375rem 0.875rem;
  background: color-mix(in srgb, var(--color-accent) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--color-accent) 25%, transparent);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-accent);
  margin-block-end: var(--space-6);
  animation: eyebrow-in 0.5s var(--ease-out) 0.2s both;
}

@keyframes eyebrow-in {
  from { opacity: 0; translate: 0 -8px; }
}

.hero__title {
  font-size: clamp(2.5rem, 6vw + 1rem, 6rem);
  font-weight: var(--font-weight-black);
  line-height: 1.05;
  letter-spacing: -0.03em;
  text-wrap: balance;
  margin-block-end: var(--space-6);
  animation: title-in 0.6s var(--ease-out) 0.35s both;
}

@keyframes title-in {
  from { opacity: 0; translate: 0 20px; }
}

.hero__subtitle {
  font-size: clamp(1.125rem, 2vw + 0.5rem, 1.5rem);
  color: var(--color-text-muted);
  max-width: 50ch;
  margin-inline: auto;
  margin-block-end: var(--space-8);
  text-wrap: pretty;
  animation: subtitle-in 0.6s var(--ease-out) 0.5s both;
}

@keyframes subtitle-in {
  from { opacity: 0; translate: 0 15px; }
}

.hero__actions {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
  flex-wrap: wrap;
  animation: actions-in 0.6s var(--ease-out) 0.65s both;
}

@keyframes actions-in {
  from { opacity: 0; translate: 0 10px; }
}

/* ─── Feature grid section ─── */
.features {
  padding-block: clamp(4rem, 10vw, 10rem);
  padding-inline: clamp(1rem, 5vw, 4rem);
}

.features__header {
  text-align: center;
  max-width: 45ch;
  margin-inline: auto;
  margin-block-end: clamp(3rem, 6vw, 5rem);
}

.features__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: var(--space-6);
}

.feature-card {
  padding: var(--space-6);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  background: var(--color-surface);
  transition:
    box-shadow var(--duration-normal) var(--ease-out),
    translate  var(--duration-normal) var(--ease-out),
    border-color var(--duration-fast);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
    color-mix(in srgb, var(--color-accent) 8%, transparent),
    transparent 70%
  );
  opacity: 0;
  transition: opacity var(--duration-normal);
}

.feature-card:hover {
  box-shadow: var(--shadow-lg);
  translate: 0 -2px;
  border-color: var(--color-border-strong);
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-icon {
  width: 3rem;
  height: 3rem;
  border-radius: var(--radius-xl);
  background: color-mix(in srgb, var(--color-accent) 12%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  margin-block-end: var(--space-4);
  font-size: 1.5rem;
}
```

---

## 87. CSS THEMING — COMPLETE SYSTEM

### 87.1 Multi-theme Architecture

```css
/* ─── Theme definition pattern ─── */

/* Base — structural tokens (never theme-specific) */
:root {
  --font-sans: system-ui, sans-serif;
  --font-mono: 'Fira Code', monospace;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  
  /* Semantic (change per theme) */
  --bg-base:      white;
  --bg-subtle:    #f8f9fa;
  --bg-muted:     #e9ecef;
  --surface:      white;
  --border:       #dee2e6;
  --border-strong: #ced4da;
  --text:         #212529;
  --text-muted:   #6c757d;
  --text-subtle:  #adb5bd;
  --accent:       #3b82f6;
  --accent-hover: #2563eb;
  --accent-text:  white;
}

/* ─── Theme: Dark ─── */
[data-theme="dark"],
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg-base:      #0f172a;
    --bg-subtle:    #1e293b;
    --bg-muted:     #334155;
    --surface:      #1e293b;
    --border:       #334155;
    --border-strong: #475569;
    --text:         #f1f5f9;
    --text-muted:   #94a3b8;
    --text-subtle:  #64748b;
  }
}

/* ─── Theme: Sepia ─── */
[data-theme="sepia"] {
  --bg-base:    #f8f1e3;
  --bg-subtle:  #ede7d3;
  --surface:    #f8f1e3;
  --border:     #d4c9a8;
  --text:       #3d2b1f;
  --text-muted: #7a6551;
  --accent:     #8b5e3c;
}

/* ─── Theme: High Contrast ─── */
[data-theme="high-contrast"] {
  --bg-base:      black;
  --surface:      black;
  --border:       white;
  --text:         white;
  --text-muted:   #eeeeee;
  --accent:       yellow;
  --accent-text:  black;
}

/* ─── Theme: Colorful ─── */
[data-theme="purple"] {
  --accent:       #8b5cf6;
  --accent-hover: #7c3aed;
  --bg-subtle:    #faf5ff;
}
[data-theme="green"] {
  --accent:       #10b981;
  --accent-hover: #059669;
  --bg-subtle:    #f0fdf4;
}
[data-theme="rose"] {
  --accent:       #f43f5e;
  --accent-hover: #e11d48;
  --bg-subtle:    #fff1f2;
}

/* ─── Theme switcher component ─── */
.theme-switcher {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

.theme-dot {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition:
    scale var(--duration-fast) var(--ease-bounce),
    border-color var(--duration-fast);
}

.theme-dot:hover { scale: 1.15; }
.theme-dot[aria-pressed="true"] { border-color: var(--text); }

.theme-dot--light   { background: white; box-shadow: 0 0 0 1px #ddd; }
.theme-dot--dark    { background: #0f172a; }
.theme-dot--sepia   { background: #f8f1e3; box-shadow: 0 0 0 1px #d4c9a8; }
.theme-dot--purple  { background: #8b5cf6; }
.theme-dot--green   { background: #10b981; }
.theme-dot--rose    { background: #f43f5e; }
```

---

## 88. COMPLETE ANIMATION COOKBOOK

### 88.1 Page Transitions

```css
/* ─── Full page transition library ─── */

/* Base state for page entering */
.page-enter {
  animation: var(--page-enter, page-fade-in) var(--duration-slow) var(--ease-out) both;
}
.page-leave {
  animation: var(--page-leave, page-fade-out) var(--duration-slow) var(--ease-in) both;
}

/* Fade */
@keyframes page-fade-in   { from { opacity: 0; } }
@keyframes page-fade-out  { to   { opacity: 0; } }

/* Slide from right */
@keyframes page-slide-in-right  { from { translate: 100% 0; opacity: 0; } }
@keyframes page-slide-out-left  { to   { translate: -30% 0; opacity: 0; } }

/* Slide from left */
@keyframes page-slide-in-left   { from { translate: -100% 0; opacity: 0; } }
@keyframes page-slide-out-right { to   { translate: 30% 0; opacity: 0; } }

/* Scale */
@keyframes page-scale-in   { from { scale: 1.05; opacity: 0; } }
@keyframes page-scale-out  { to   { scale: 0.95; opacity: 0; } }

/* Flip */
@keyframes page-flip-in  { from { rotateY: -10deg; opacity: 0; } }
@keyframes page-flip-out { to   { rotateY: 10deg; opacity: 0; } }

/* Apply theme based on direction */
[data-direction="forward"] {
  --page-enter: page-slide-in-right;
  --page-leave: page-slide-out-left;
}
[data-direction="backward"] {
  --page-enter: page-slide-in-left;
  --page-leave: page-slide-out-right;
}
```

### 88.2 Loading Animations

```css
/* ─── Complete loading library ─── */

/* 1. Classic spinner */
@keyframes spin { to { rotate: 360deg; } }
.loader-spin {
  width: 24px; height: 24px;
  border: 2px solid var(--color-bg-muted);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

/* 2. Dots pulse */
.loader-dots {
  display: flex; gap: 4px; align-items: center;
}
.loader-dots span {
  width: 8px; height: 8px;
  background: var(--color-accent);
  border-radius: 50%;
  animation: dots-bounce 1.2s ease-in-out infinite;
}
.loader-dots span:nth-child(2) { animation-delay: 0.2s; }
.loader-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dots-bounce {
  0%, 80%, 100% { scale: 0.6; opacity: 0.4; }
  40%           { scale: 1;   opacity: 1; }
}

/* 3. Progress bar */
.loader-bar {
  width: 100%; height: 3px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}
.loader-bar::after {
  content: '';
  position: absolute;
  inset-block: 0;
  width: 40%;
  background: var(--color-accent);
  border-radius: inherit;
  animation: bar-slide 1.5s ease-in-out infinite;
}
@keyframes bar-slide {
  from { inset-inline-start: -40%; }
  to   { inset-inline-start: 100%; }
}

/* 4. Skeleton shimmer */
@keyframes shimmer {
  from { background-position: -200% 0; }
  to   { background-position: 200% 0; }
}
.loader-skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-subtle) 25%,
    var(--color-bg-muted) 50%,
    var(--color-bg-subtle) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-md);
}

/* 5. Circular indeterminate */
.loader-circle {
  width: 36px; height: 36px;
  animation: rotate 2s linear infinite;
}
.loader-circle circle {
  stroke: var(--color-accent);
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}
@keyframes rotate { to { rotate: 360deg; } }
@keyframes dash {
  0%   { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
  50%  { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
  100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
}

/* 6. Typing indicator */
.loader-typing {
  display: inline-flex;
  gap: 4px;
  align-items: center;
  padding: 0.625rem 0.875rem;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
}
.loader-typing span {
  width: 6px; height: 6px;
  background: var(--color-text-muted);
  border-radius: 50%;
  animation: typing-dot 1.4s ease-in-out infinite;
}
.loader-typing span:nth-child(2) { animation-delay: 0.2s; }
.loader-typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing-dot {
  0%, 60%, 100% { translate: 0; opacity: 0.4; }
  30%           { translate: 0 -4px; opacity: 1; }
}

/* 7. Page progress (top bar) */
.page-progress {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  background: var(--color-accent);
  z-index: var(--z-top);
  border-radius: 0 var(--radius-full) var(--radius-full) 0;
  width: var(--progress, 0%);
  transition: width 0.2s var(--ease-out);
  box-shadow: 0 0 8px var(--color-accent);
}
```

---

## 89. ACCESSIBILITY DEEP DIVE

### 89.1 WCAG 2.1 / 2.2 CSS Requirements

```css
/* ─── 1.1.1 Non-text Content — provide alt text (HTML, not CSS) ─── */
/* Decorative images via CSS don't need alt */
.decorative { background-image: url('pattern.svg'); }

/* ─── 1.4.1 Use of Color — never use color alone ─── */
/* ❌ Only color to indicate required */
.required-field { border-color: red; }

/* ✅ Color + icon + text */
.required-field {
  border-color: var(--color-danger-500);
}
.required-field::after {
  content: ' *';
  color: var(--color-danger-500);
  font-weight: bold;
}

/* ─── 1.4.3 Contrast Minimum — 4.5:1 normal, 3:1 large ─── */
/* Large text = 18pt (24px) or 14pt (18.67px) bold */

/* ─── 1.4.4 Resize Text — don't prevent zoom ─── */
/* ✅ Use em/rem, not px for text */
/* ✅ Don't use maximum-scale=1 in viewport meta */

/* ─── 1.4.10 Reflow — must work at 320px width ─── */
.component {
  max-width: 100%;
  overflow-wrap: break-word;
  /* No fixed widths that cause horizontal scroll */
}

/* ─── 1.4.11 Non-text Contrast — UI components 3:1 ─── */
input, button {
  border: 1px solid var(--color-border-strong); /* must be 3:1 vs background */
}

/* ─── 1.4.12 Text Spacing ─── */
/* Users can set: line-height: 1.5×, letter-spacing: 0.12em,
   word-spacing: 0.16em, paragraph spacing: 2×. Must not break. */
.text {
  /* Don't use fixed height that clips at custom spacing */
  min-height: 1.5em;  /* not height! */
  overflow: visible;  /* not hidden */
}

/* ─── 2.1.1 Keyboard — all functionality via keyboard ─── */
/* All interactive elements must be natively focusable or have tabindex */
[tabindex="0"] { cursor: pointer; }  /* custom interactive */
[tabindex="-1"] { }  /* programmatically focusable, not in tab order */

/* ─── 2.4.7 Focus Visible ─── */
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
  border-radius: 2px;
}
/* Never: */
/* :focus { outline: none; }  ← WCAG violation */

/* ─── 2.5.3 Label in Name ─── */
/* Button with icon only must have accessible name */
.icon-btn {
  /* aria-label="Close" in HTML */
  /* Visual label must match accessible name */
}

/* ─── 2.5.8 Target Size (WCAG 2.2 AA) — minimum 24×24px ─── */
.interactive-target {
  min-width: 24px;
  min-height: 24px;
}
/* Enhanced: 44×44px (WCAG AAA / Apple HIG) */
.interactive-enhanced {
  min-width: 44px;
  min-height: 44px;
}

/* ─── 3.3.4 Error Suggestion ─── */
.field__error {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--color-danger-600);
  font-size: var(--font-size-sm);
  margin-top: var(--space-1);
  /* Must be programmatically associated via aria-describedby */
}
```

### 89.2 Focus Management Patterns

```css
/* ─── Focus trap indicator ─── */
.focus-trap-active {
  position: relative;
}

.focus-trap-active::after {
  content: '';
  position: fixed;
  inset: 0;
  outline: 3px solid var(--color-accent);
  outline-offset: -3px;
  pointer-events: none;
  z-index: var(--z-top);
}

/* ─── Focus ring styles by component ─── */

/* Links */
a:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
  border-radius: 2px;
}

/* Buttons */
.btn:focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--color-bg),
    0 0 0 4px var(--color-accent);
}

/* Inputs */
.input:focus-visible {
  border-color: var(--color-accent);
  box-shadow:
    0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);
  outline: none;
}

/* Cards (when clickable) */
.card-link:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 4px;
  border-radius: calc(var(--radius-xl) + 4px);
}

/* ─── Skip navigation ─── */
.skip-nav {
  position: absolute;
  top: -100%;
  left: 50%;
  translate: -50%;
  padding: 0.875rem 2rem;
  background: var(--color-accent);
  color: white;
  font-weight: var(--font-weight-bold);
  text-decoration: none;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  z-index: var(--z-top);
  transition: top var(--duration-fast);
  white-space: nowrap;
}

.skip-nav:focus {
  top: 0;
  outline: none;
  box-shadow: 0 4px 12px rgb(0 0 0 / 0.3);
}

/* ─── Reduced motion full implementation ─── */
@media (prefers-reduced-motion: reduce) {
  /* Remove ALL animations and transitions */
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    transition-delay: 0ms !important;
    scroll-behavior: auto !important;
  }

  /* Remove parallax */
  .parallax { transform: none !important; }

  /* Keep useful state changes (no duration = instant) */
  :focus-visible { outline-offset: 2px; }  /* instant is fine */
}

/* ─── Prefers contrast ─── */
@media (prefers-contrast: more) {
  :root {
    --color-border: var(--color-neutral-600);
    --color-text-muted: var(--color-neutral-600);
    --color-text-subtle: var(--color-neutral-500);
  }

  .btn {
    border-width: 2px;
    font-weight: var(--font-weight-bold);
  }

  input, select, textarea {
    border-width: 2px;
  }
}

@media (prefers-contrast: less) {
  :root {
    --shadow-md: 0 2px 4px rgb(0 0 0 / 0.06);
  }
}
```

---

## 90. FINAL QUICK REFERENCE

### 90.1 CSS Reset — The Essential 2025 Version

```css
/* ─── The Complete Modern Reset ─── */

/* Box sizing */
*, *::before, *::after {
  box-sizing: border-box;
}

/* Remove defaults */
* {
  margin: 0;
  padding: 0;
}

/* Document */
html {
  font-size: 100%;
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
  color-scheme: light dark;
  hanging-punctuation: first last;
  scroll-behavior: smooth;
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Body */
body {
  min-height: 100dvh;
  font-family: var(--font-sans, system-ui, sans-serif);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Media */
img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}
img, video { height: auto; }

/* Typography */
h1, h2, h3, h4, h5, h6 {
  font-size: inherit;
  font-weight: inherit;
  overflow-wrap: break-word;
  text-wrap: balance;
}

p, li, figcaption {
  overflow-wrap: break-word;
  text-wrap: pretty;
}

/* Forms */
input, button, textarea, select {
  font: inherit;
  color: inherit;
}
button { cursor: pointer; border: none; background: none; }
textarea { resize: vertical; }

/* Lists */
:where(ul, ol):not([class]) { padding-inline-start: 1.5em; }

/* Links */
a { color: inherit; text-decoration-skip-ink: auto; }

/* Tables */
table { border-collapse: collapse; }

/* Hidden */
[hidden] { display: none !important; }

/* Focus */
:focus { outline: none; }
:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}

/* Safe area */
body {
  padding-inline: env(safe-area-inset-left, 0) env(safe-area-inset-right, 0);
}
```

### 90.2 The 10 CSS Rules That Matter Most

```css
/*
 1. box-sizing: border-box on everything
 2. Use Custom Properties for all design tokens
 3. Prefer logical properties (margin-inline, padding-block)
 4. Use clamp() for fluid sizing
 5. CSS Grid for 2D, Flexbox for 1D
 6. :focus-visible for accessible focus rings
 7. Respect prefers-reduced-motion
 8. Use @layer to control specificity
 9. oklch() for perceptually uniform colors
 10. Never use !important except in utilities and reset
*/

/* The minimal setup that covers 90% of needs: */

*, *::before, *::after { box-sizing: border-box; }
html { font-size: 100%; color-scheme: light dark; }
body { min-height: 100dvh; font-family: system-ui, sans-serif; line-height: 1.5; -webkit-font-smoothing: antialiased; }
img, video { display: block; max-width: 100%; height: auto; }
input, button, textarea, select { font: inherit; }
:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }
```

---

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    COMPLETE CSS GUIDE — FINAL STATS                   ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  PARTS:       I (Russian) + II (Russian) + III (English) + IV (Eng)  ║
║  CHAPTERS:    90 chapters                                             ║
║  LINES:       ~16,000+ lines of Markdown                              ║
║  CODE:        500+ working CSS examples                               ║
║  COMPONENTS:  Button, Card, Modal, Drawer, Combobox, DatePicker,     ║
║               ContextMenu, TagInput, Carousel, MegaMenu, Timeline,  ║
║               Pricing, Toast, Tooltip, Accordion, Tabs, Stepper,    ║
║               Avatar, Badge, Chip, Table, Progress, Skeleton,        ║
║               Dashboard, Landing Page, Prose, Code Blocks, Gallery  ║
║  TOPICS:      Reset · Tokens · Cascade · @layer · Nesting ·          ║
║               Grid · Flexbox · Subgrid · Flexbox · Animations ·      ║
║               Scroll-Driven · View Transitions · Anchor Positioning  ║
║               Container Queries · Scope · @property · oklch() ·     ║
║               Logical Props · Writing Modes · Dark Mode · a11y ·     ║
║               Performance · Email · PWA · Shadow DOM · SVG ·         ║
║               Print · Houdini · Spring Physics · Micro-interactions  ║
║               Browser Hacks · ITCSS · SMACSS · BEM · CUBE CSS ·     ║
║               Empty States · Error States · i18n · RTL               ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

*End of Part IV. The complete 4-part CSS Reference Guide is now finished.*
