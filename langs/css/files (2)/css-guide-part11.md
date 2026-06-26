# PART XI — CSS: FINAL PATTERNS & QUICK REFERENCE

---

## 163. MULTI-THUMB RANGE SLIDER

```css
/* ─── Dual handle range (price range, date range) ─── */
/* Uses two overlapping inputs */
.range-slider {
  position: relative;
  height: 4px;
  width: 100%;
  margin-block: 1.5rem;
}

.range-slider__track {
  position: absolute;
  inset: 0;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
}

.range-slider__fill {
  position: absolute;
  inset-block: 0;
  left:  var(--left, 20%);
  right: var(--right, 20%);
  background: var(--color-accent);
  border-radius: var(--radius-full);
}

.range-slider input[type="range"] {
  position: absolute;
  inset: 0;
  appearance: none;
  -webkit-appearance: none;
  background: transparent;
  pointer-events: none;
  margin: 0;
  width: 100%;
}

.range-slider input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: white;
  border: 2px solid var(--color-accent);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  pointer-events: auto;
  transition: scale var(--duration-fast) var(--ease-bounce);
}

.range-slider input[type="range"]::-webkit-slider-thumb:hover { scale: 1.2; }
.range-slider input[type="range"]::-webkit-slider-thumb:active { scale: 1.1; cursor: grabbing; }

.range-slider input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: white;
  border: 2px solid var(--color-accent);
  box-shadow: var(--shadow-md);
  cursor: pointer;
}

/* Value labels */
.range-slider__labels {
  display: flex;
  justify-content: space-between;
  margin-block-start: 1.75rem;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.range-label {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 0.25rem 0.5rem;
  font-variant-numeric: tabular-nums;
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
}
```

---

## 164. COPY-TO-CLIPBOARD FEEDBACK

```css
/* ─── Copy button states ─── */
.copy-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.375rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  cursor: pointer;
  font: inherit;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  transition:
    background      var(--duration-fast),
    border-color    var(--duration-fast),
    color           var(--duration-fast);
  position: relative;
  overflow: hidden;
}

.copy-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }

/* Copied state */
.copy-btn.copied {
  background: var(--color-success-100);
  border-color: var(--color-success-300);
  color: var(--color-success-700);
  animation: copy-success 0.3s var(--ease-bounce);
}

@keyframes copy-success {
  0%   { scale: 0.95; }
  60%  { scale: 1.05; }
  100% { scale: 1; }
}

/* Icon swap via CSS */
.copy-btn .icon-copy    { display: block; }
.copy-btn .icon-check   { display: none; }
.copy-btn.copied .icon-copy  { display: none; }
.copy-btn.copied .icon-check { display: block; color: var(--color-success-600); }

/* Ripple effect on copy */
.copy-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-success-200);
  border-radius: inherit;
  scale: 0;
  opacity: 0;
}
.copy-btn.copied::after {
  animation: copy-ripple 0.4s ease-out;
}
@keyframes copy-ripple {
  from { scale: 0; opacity: 0.6; }
  to   { scale: 2; opacity: 0; }
}

/* Tooltip "Copied!" */
.copy-btn.copied::before {
  content: 'Copied!';
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  translate: -50% 0;
  background: var(--color-neutral-900);
  color: white;
  font-size: var(--font-size-xs);
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-md);
  white-space: nowrap;
  animation: tooltip-pop 0.2s var(--ease-bounce);
  pointer-events: none;
}

@keyframes tooltip-pop {
  from { opacity: 0; translate: -50% 4px; }
  to   { opacity: 1; translate: -50% 0; }
}
```

---

## 165. NETWORK STATUS INDICATOR

```css
/* ─── Online / Offline banner ─── */
.network-banner {
  position: fixed;
  top: 0;
  inset-inline: 0;
  z-index: var(--z-toast);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  translate: 0 -100%;
  transition: translate 0.3s var(--ease-bounce);
}

.network-banner.visible { translate: 0 0; }

.network-banner--offline {
  background: var(--color-danger-500);
  color: white;
}

.network-banner--online {
  background: var(--color-success-500);
  color: white;
  /* Auto-hide after 2s via animation */
  animation: banner-show-hide 2s ease-out 0.3s forwards;
}

@keyframes banner-show-hide {
  0%, 70% { translate: 0 0; }
  100%    { translate: 0 -100%; }
}

.network-banner__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.8;
}

.network-banner--offline .network-banner__dot {
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 100% { opacity: 0.8; }
  50%       { opacity: 0.2; }
}

/* ─── Status bar connection indicator ─── */
.connection-status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.connection-status::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--status-color, var(--color-neutral-400));
}

.connection-status.online  { --status-color: var(--color-success-500); }
.connection-status.offline { --status-color: var(--color-danger-500); }
.connection-status.slow    { --status-color: var(--color-warning-500); }

.connection-status.online::before {
  animation: status-pulse 2s ease-in-out infinite;
  box-shadow: 0 0 0 0 var(--color-success-300);
}

@keyframes status-pulse {
  0%   { box-shadow: 0 0 0 0 var(--color-success-300); }
  70%  { box-shadow: 0 0 0 5px transparent; }
  100% { box-shadow: 0 0 0 0 transparent; }
}
```

---

## 166. INFINITE CANVAS PATTERNS

```css
/* ─── Figma/Miro-style infinite canvas ─── */
.infinite-canvas {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  cursor: var(--canvas-cursor, default);
  background: var(--canvas-bg, #f0f0f0);
  touch-action: none;
  user-select: none;
}

/* Dot grid background */
.infinite-canvas::before {
  content: '';
  position: absolute;
  inset: -200%;
  background-image: radial-gradient(
    circle,
    var(--grid-dot-color, #ccc) 1px,
    transparent 1px
  );
  background-size: var(--grid-size, 20px) var(--grid-size, 20px);
  pointer-events: none;
  transform:
    translate(var(--pan-x, 0px), var(--pan-y, 0px))
    scale(var(--zoom, 1));
  transform-origin: center;
  /* JS updates --pan-x, --pan-y, --zoom */
}

/* Canvas viewport */
.canvas-viewport {
  position: absolute;
  top: 0;
  left: 0;
  transform:
    translate(var(--pan-x, 0px), var(--pan-y, 0px))
    scale(var(--zoom, 1));
  transform-origin: top left;
  will-change: transform;
}

/* Canvas states */
.infinite-canvas[data-tool="pan"]    { cursor: grab; }
.infinite-canvas[data-tool="pan"].panning { cursor: grabbing; }
.infinite-canvas[data-tool="select"] { cursor: default; }
.infinite-canvas[data-tool="draw"]   { cursor: crosshair; }
.infinite-canvas[data-tool="text"]   { cursor: text; }

/* Zoom controls HUD */
.canvas-hud {
  position: absolute;
  bottom: var(--space-5);
  left: 50%;
  translate: -50% 0;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-2) var(--space-3);
  box-shadow: var(--shadow-lg);
  z-index: 10;
}

.canvas-zoom-btn {
  width: 1.75rem;
  height: 1.75rem;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--color-text-muted);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: bold;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.canvas-zoom-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }

.canvas-zoom-level {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  min-width: 3.5em;
  text-align: center;
  color: var(--color-text);
  cursor: pointer;
  font-variant-numeric: tabular-nums;
}

/* Mini-map */
.canvas-minimap {
  position: absolute;
  bottom: var(--space-5);
  right: var(--space-5);
  width: 160px;
  height: 100px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  z-index: 10;
}

/* Viewport indicator on minimap */
.canvas-minimap__viewport {
  position: absolute;
  border: 1.5px solid var(--color-accent);
  border-radius: 2px;
  background: color-mix(in srgb, var(--color-accent) 15%, transparent);
  pointer-events: none;
  /* Position/size set by JS */
  left:   var(--vp-left, 0);
  top:    var(--vp-top, 0);
  width:  var(--vp-w, 30%);
  height: var(--vp-h, 30%);
}
```

---

## 167. CSS COLOUR BLINDNESS SIMULATION

```css
/* ─── Colour blindness filters (for testing/accessibility) ─── */

/* Apply to root for simulation */
.cb-protanopia {   /* Red-blind */
  filter: url('#protanopia');
}
.cb-deuteranopia { /* Green-blind (most common) */
  filter: url('#deuteranopia');
}
.cb-tritanopia {   /* Blue-blind */
  filter: url('#tritanopia');
}
.cb-achromatopsia { /* No colour */
  filter: grayscale(100%);
}

/* SVG filter matrix definitions (in HTML) */
/*
<svg style="position:absolute;width:0;height:0">
  <defs>
    <filter id="protanopia">
      <feColorMatrix type="matrix" values="
        0.56667 0.43333 0     0 0
        0.55833 0.44167 0     0 0
        0       0.24167 0.75833 0 0
        0       0       0     1 0"/>
    </filter>
    <filter id="deuteranopia">
      <feColorMatrix type="matrix" values="
        0.625   0.375   0      0 0
        0.70    0.30    0      0 0
        0       0.30    0.70   0 0
        0       0       0      1 0"/>
    </filter>
    <filter id="tritanopia">
      <feColorMatrix type="matrix" values="
        0.95    0.05    0      0 0
        0       0.43333 0.56667 0 0
        0       0.475   0.525  0 0
        0       0       0      1 0"/>
    </filter>
  </defs>
</svg>
*/

/* ─── High contrast mode CSS (manual) ─── */
[data-contrast="high"] {
  --color-text:         #000000;
  --color-bg:           #ffffff;
  --color-border:       #000000;
  --color-accent:       #0000ee;
  --color-text-muted:   #333333;
  --color-success-500:  #006400;
  --color-danger-500:   #cc0000;
  --color-warning-500:  #886600;
}

[data-contrast="high"] .btn {
  border: 2px solid currentColor;
  text-decoration: underline;
}

[data-contrast="high"] a {
  color: #0000ee;
  text-decoration: underline;
}

[data-contrast="high"] a:visited { color: #551a8b; }
[data-contrast="high"] :focus-visible {
  outline: 3px solid #000;
  outline-offset: 3px;
}
```

---

## 168. THE MASTER CSS QUICK REFERENCE CARD

```css
/*
╔═════════════════════════════════════════════════════════════════════╗
║                   CSS QUICK REFERENCE — 2025                         ║
╠═════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  CENTERING CHEAT SHEET                                              ║
║  ──────────────────────────────────────────────────────────────     ║
║  display:flex; align-items:center; justify-content:center          ║
║  display:grid; place-items:center                                   ║
║  position:absolute; inset:0; margin:auto; w:fit; h:fit             ║
║                                                                     ║
║  FLEXBOX AXES                                                       ║
║  ──────────────────────────────────────────────────────────────     ║
║  justify-content → main axis (row: horizontal, col: vertical)      ║
║  align-items     → cross axis (row: vertical, col: horizontal)     ║
║  align-content   → multiple rows on cross axis                     ║
║  align-self      → individual item on cross axis                   ║
║  justify-self    → (grid only) individual item on main axis        ║
║                                                                     ║
║  GRID SIZING                                                        ║
║  ──────────────────────────────────────────────────────────────     ║
║  fr              fills remaining space                              ║
║  auto            fit to content                                     ║
║  min-content     smallest possible                                  ║
║  max-content     as wide as content needs                           ║
║  minmax(a,b)     min a, max b                                       ║
║  fit-content(x)  max-content but no wider than x                   ║
║  repeat(n, size) repeat n times                                     ║
║  repeat(auto-fit, minmax(200px,1fr))  ← responsive magic           ║
║                                                                     ║
║  SELECTORS CHEAT SHEET                                              ║
║  ──────────────────────────────────────────────────────────────     ║
║  .a .b          → descendant                                        ║
║  .a > .b        → direct child                                      ║
║  .a + .b        → adjacent sibling                                  ║
║  .a ~ .b        → all following siblings                            ║
║  :has(.b)       → parent with child .b                             ║
║  :is(a,b,c)     → any of list (keeps specificity)                  ║
║  :where(a,b,c)  → any of list (zero specificity)                   ║
║  :not(.a)       → not matching                                      ║
║                                                                     ║
║  UNITS CHEAT SHEET                                                  ║
║  ──────────────────────────────────────────────────────────────     ║
║  px             absolute pixels                                     ║
║  rem            relative to root font-size (16px default)          ║
║  em             relative to current font-size                       ║
║  %              relative to parent (or itself for padding-top %)   ║
║  vw/vh          viewport width/height                               ║
║  dvh            dynamic viewport height (mobile URL bar aware)     ║
║  svh/lvh        small/large viewport height                        ║
║  ch             width of "0" character                              ║
║  cqw/cqi        container query width/inline-size                  ║
║                                                                     ║
║  SPECIFICITY CALCULATOR                                             ║
║  ──────────────────────────────────────────────────────────────     ║
║  *               0-0-0   (zero)                                     ║
║  p, div          0-0-1   (element)                                  ║
║  .class, [attr]  0-1-0   (class)                                    ║
║  :hover, :is(X)  inherits arg specificity                          ║
║  :where(X)       0-0-0   (always zero!)                             ║
║  #id             1-0-0   (ID)                                       ║
║  style=""        1-0-0-0 (inline)                                   ║
║  !important      overrides all                                      ║
║                                                                     ║
║  RESPONSIVE BREAKPOINTS                                             ║
║  ──────────────────────────────────────────────────────────────     ║
║  @media (min-width: 640px)  sm  → small tablets                    ║
║  @media (min-width: 768px)  md  → tablets                          ║
║  @media (min-width: 1024px) lg  → small laptops                    ║
║  @media (min-width: 1280px) xl  → desktops                         ║
║  @media (min-width: 1536px) 2xl → large screens                    ║
║                                                                     ║
║  PHYSICAL → LOGICAL                                                 ║
║  ──────────────────────────────────────────────────────────────     ║
║  margin-left   → margin-inline-start                                ║
║  margin-right  → margin-inline-end                                  ║
║  margin-top    → margin-block-start                                 ║
║  margin-bottom → margin-block-end                                   ║
║  width         → inline-size                                        ║
║  height        → block-size                                         ║
║                                                                     ║
║  ANIMATION QUICK GUIDE                                              ║
║  ──────────────────────────────────────────────────────────────     ║
║  GPU-safe:       transform, opacity                                 ║
║  Avoid animating: width, height, margin, padding, top, left        ║
║  Respect user:   @media (prefers-reduced-motion: reduce)           ║
║  Spring easing:  linear(0, ...) via CSS linear()                   ║
║  Scroll-driven:  animation-timeline: scroll() or view()            ║
║                                                                     ║
║  MODERN FEATURES (2025 browser support)                             ║
║  ──────────────────────────────────────────────────────────────     ║
║  ✅ :has()                 Chrome 105+ Safari 15.4+ FF 121+        ║
║  ✅ CSS Nesting            Chrome 120+ Safari 17.2+ FF 117+        ║
║  ✅ @layer                 Chrome 99+ Safari 15.4+ FF 97+          ║
║  ✅ Container Queries      Chrome 105+ Safari 16+ FF 110+          ║
║  ✅ color-mix()            Chrome 111+ Safari 16.2+ FF 113+        ║
║  ✅ oklch()                Chrome 111+ Safari 15.4+ FF 113+        ║
║  ✅ Relative color         Chrome 119+ Safari 16.4+ FF 128+        ║
║  ✅ Scroll-Driven Anims    Chrome 115+  (no FF, no Safari)         ║
║  ✅ Anchor Positioning     Chrome 125+  (no FF, no Safari)         ║
║  ✅ @starting-style        Chrome 117+ Safari 17.5+                ║
║  ✅ interpolate-size       Chrome 129+  (experimental)             ║
║  ✅ View Transitions       Chrome 111+ Safari 18+                  ║
║  ✅ @scope                 Chrome 118+ Safari 17.4+                ║
║  ✅ Subgrid                Chrome 117+ Safari 16+ FF 71+           ║
║                                                                     ║
╚═════════════════════════════════════════════════════════════════════╝
*/
```

---

## FINAL SUMMARY

```
╔══════════════════════════════════════════════════════════════════════╗
║         THE MONUMENTAL CSS GUIDE — PARTS I–XI — COMPLETE            ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  168 CHAPTERS                                                        ║
║  1,000+ CODE EXAMPLES                                               ║
║  ~38,000 LINES OF CONTENT                                           ║
║  ~700KB COMBINED                                                    ║
║                                                                      ║
║  COVERAGE (exhaustive):                                              ║
║  ─────────────────────────────────────────────────────────────────  ║
║  Architecture    @layer, ITCSS, SMACSS, BEM, CUBE, tokens          ║
║  Layout          Grid, Flexbox, Subgrid, Container Queries          ║
║  Typography      fluid, variable fonts, OpenType, prose             ║
║  Color           oklch, color-mix, relative, dark mode              ║
║  Animation       keyframes, transitions, scroll-driven, spring      ║
║  Modern CSS      :has(), nesting, anchor, view transitions          ║
║  Components      30+ complete UI patterns with all states           ║
║  E-commerce      product, cart, checkout, payment card              ║
║  Social/Media    chat, feed, audio, video players                   ║
║  Dashboards      KPI, gauge, heatmap, ticker, analytics             ║
║  Documents       invoice, CV, blog, article, magazine               ║
║  Dev Tools       IDE, terminal, diff viewer, spreadsheet            ║
║  Creative        whiteboard, slides, video editor, canvas           ║
║  Marketing       hero, CTA, testimonials, FAQ, stats, logos         ║
║  Accessibility   WCAG 2.2, focus, motion, contrast, forced-colors  ║
║  Performance     GPU, contain, content-visibility, critical CSS     ║
║  Reference       all properties, at-rules, units, functions        ║
║  Debugging       DevTools, debug kit, gotchas (50+)                ║
╚══════════════════════════════════════════════════════════════════════╝
```
