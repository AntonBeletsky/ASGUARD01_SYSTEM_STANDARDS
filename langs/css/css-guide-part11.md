\# PART XI — CSS: FINAL PATTERNS \& QUICK REFERENCE



\---



\## 163. MULTI-THUMB RANGE SLIDER



```css

/\* ─── Dual handle range (price range, date range) ─── \*/

/\* Uses two overlapping inputs \*/

.range-slider {

&#x20; position: relative;

&#x20; height: 4px;

&#x20; width: 100%;

&#x20; margin-block: 1.5rem;

}



.range-slider\_\_track {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

}



.range-slider\_\_fill {

&#x20; position: absolute;

&#x20; inset-block: 0;

&#x20; left:  var(--left, 20%);

&#x20; right: var(--right, 20%);

&#x20; background: var(--color-accent);

&#x20; border-radius: var(--radius-full);

}



.range-slider input\[type="range"] {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; appearance: none;

&#x20; -webkit-appearance: none;

&#x20; background: transparent;

&#x20; pointer-events: none;

&#x20; margin: 0;

&#x20; width: 100%;

}



.range-slider input\[type="range"]::-webkit-slider-thumb {

&#x20; appearance: none;

&#x20; -webkit-appearance: none;

&#x20; width: 18px;

&#x20; height: 18px;

&#x20; border-radius: 50%;

&#x20; background: white;

&#x20; border: 2px solid var(--color-accent);

&#x20; box-shadow: var(--shadow-md);

&#x20; cursor: pointer;

&#x20; pointer-events: auto;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}



.range-slider input\[type="range"]::-webkit-slider-thumb:hover { scale: 1.2; }

.range-slider input\[type="range"]::-webkit-slider-thumb:active { scale: 1.1; cursor: grabbing; }



.range-slider input\[type="range"]::-moz-range-thumb {

&#x20; width: 18px;

&#x20; height: 18px;

&#x20; border-radius: 50%;

&#x20; background: white;

&#x20; border: 2px solid var(--color-accent);

&#x20; box-shadow: var(--shadow-md);

&#x20; cursor: pointer;

}



/\* Value labels \*/

.range-slider\_\_labels {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; margin-block-start: 1.75rem;

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

}



.range-label {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; padding: 0.25rem 0.5rem;

&#x20; font-variant-numeric: tabular-nums;

&#x20; font-weight: var(--font-weight-medium);

&#x20; color: var(--color-text);

}

```



\---



\## 164. COPY-TO-CLIPBOARD FEEDBACK



```css

/\* ─── Copy button states ─── \*/

.copy-btn {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.375rem 0.75rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-surface);

&#x20; cursor: pointer;

&#x20; font: inherit;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; transition:

&#x20;   background      var(--duration-fast),

&#x20;   border-color    var(--duration-fast),

&#x20;   color           var(--duration-fast);

&#x20; position: relative;

&#x20; overflow: hidden;

}



.copy-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }



/\* Copied state \*/

.copy-btn.copied {

&#x20; background: var(--color-success-100);

&#x20; border-color: var(--color-success-300);

&#x20; color: var(--color-success-700);

&#x20; animation: copy-success 0.3s var(--ease-bounce);

}



@keyframes copy-success {

&#x20; 0%   { scale: 0.95; }

&#x20; 60%  { scale: 1.05; }

&#x20; 100% { scale: 1; }

}



/\* Icon swap via CSS \*/

.copy-btn .icon-copy    { display: block; }

.copy-btn .icon-check   { display: none; }

.copy-btn.copied .icon-copy  { display: none; }

.copy-btn.copied .icon-check { display: block; color: var(--color-success-600); }



/\* Ripple effect on copy \*/

.copy-btn::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: var(--color-success-200);

&#x20; border-radius: inherit;

&#x20; scale: 0;

&#x20; opacity: 0;

}

.copy-btn.copied::after {

&#x20; animation: copy-ripple 0.4s ease-out;

}

@keyframes copy-ripple {

&#x20; from { scale: 0; opacity: 0.6; }

&#x20; to   { scale: 2; opacity: 0; }

}



/\* Tooltip "Copied!" \*/

.copy-btn.copied::before {

&#x20; content: 'Copied!';

&#x20; position: absolute;

&#x20; bottom: calc(100% + 6px);

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; padding: 0.2rem 0.5rem;

&#x20; border-radius: var(--radius-md);

&#x20; white-space: nowrap;

&#x20; animation: tooltip-pop 0.2s var(--ease-bounce);

&#x20; pointer-events: none;

}



@keyframes tooltip-pop {

&#x20; from { opacity: 0; translate: -50% 4px; }

&#x20; to   { opacity: 1; translate: -50% 0; }

}

```



\---



\## 165. NETWORK STATUS INDICATOR



```css

/\* ─── Online / Offline banner ─── \*/

.network-banner {

&#x20; position: fixed;

&#x20; top: 0;

&#x20; inset-inline: 0;

&#x20; z-index: var(--z-toast);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-2) var(--space-4);

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; translate: 0 -100%;

&#x20; transition: translate 0.3s var(--ease-bounce);

}



.network-banner.visible { translate: 0 0; }



.network-banner--offline {

&#x20; background: var(--color-danger-500);

&#x20; color: white;

}



.network-banner--online {

&#x20; background: var(--color-success-500);

&#x20; color: white;

&#x20; /\* Auto-hide after 2s via animation \*/

&#x20; animation: banner-show-hide 2s ease-out 0.3s forwards;

}



@keyframes banner-show-hide {

&#x20; 0%, 70% { translate: 0 0; }

&#x20; 100%    { translate: 0 -100%; }

}



.network-banner\_\_dot {

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; border-radius: 50%;

&#x20; background: currentColor;

&#x20; opacity: 0.8;

}



.network-banner--offline .network-banner\_\_dot {

&#x20; animation: blink 1s step-end infinite;

}



@keyframes blink {

&#x20; 0%, 100% { opacity: 0.8; }

&#x20; 50%       { opacity: 0.2; }

}



/\* ─── Status bar connection indicator ─── \*/

.connection-status {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



.connection-status::before {

&#x20; content: '';

&#x20; width: 6px;

&#x20; height: 6px;

&#x20; border-radius: 50%;

&#x20; background: var(--status-color, var(--color-neutral-400));

}



.connection-status.online  { --status-color: var(--color-success-500); }

.connection-status.offline { --status-color: var(--color-danger-500); }

.connection-status.slow    { --status-color: var(--color-warning-500); }



.connection-status.online::before {

&#x20; animation: status-pulse 2s ease-in-out infinite;

&#x20; box-shadow: 0 0 0 0 var(--color-success-300);

}



@keyframes status-pulse {

&#x20; 0%   { box-shadow: 0 0 0 0 var(--color-success-300); }

&#x20; 70%  { box-shadow: 0 0 0 5px transparent; }

&#x20; 100% { box-shadow: 0 0 0 0 transparent; }

}

```



\---



\## 166. INFINITE CANVAS PATTERNS



```css

/\* ─── Figma/Miro-style infinite canvas ─── \*/

.infinite-canvas {

&#x20; position: relative;

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; overflow: hidden;

&#x20; cursor: var(--canvas-cursor, default);

&#x20; background: var(--canvas-bg, #f0f0f0);

&#x20; touch-action: none;

&#x20; user-select: none;

}



/\* Dot grid background \*/

.infinite-canvas::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: -200%;

&#x20; background-image: radial-gradient(

&#x20;   circle,

&#x20;   var(--grid-dot-color, #ccc) 1px,

&#x20;   transparent 1px

&#x20; );

&#x20; background-size: var(--grid-size, 20px) var(--grid-size, 20px);

&#x20; pointer-events: none;

&#x20; transform:

&#x20;   translate(var(--pan-x, 0px), var(--pan-y, 0px))

&#x20;   scale(var(--zoom, 1));

&#x20; transform-origin: center;

&#x20; /\* JS updates --pan-x, --pan-y, --zoom \*/

}



/\* Canvas viewport \*/

.canvas-viewport {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; left: 0;

&#x20; transform:

&#x20;   translate(var(--pan-x, 0px), var(--pan-y, 0px))

&#x20;   scale(var(--zoom, 1));

&#x20; transform-origin: top left;

&#x20; will-change: transform;

}



/\* Canvas states \*/

.infinite-canvas\[data-tool="pan"]    { cursor: grab; }

.infinite-canvas\[data-tool="pan"].panning { cursor: grabbing; }

.infinite-canvas\[data-tool="select"] { cursor: default; }

.infinite-canvas\[data-tool="draw"]   { cursor: crosshair; }

.infinite-canvas\[data-tool="text"]   { cursor: text; }



/\* Zoom controls HUD \*/

.canvas-hud {

&#x20; position: absolute;

&#x20; bottom: var(--space-5);

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-2) var(--space-3);

&#x20; box-shadow: var(--shadow-lg);

&#x20; z-index: 10;

}



.canvas-zoom-btn {

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; border-radius: var(--radius-md);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 1.1rem;

&#x20; font-weight: bold;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.canvas-zoom-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }



.canvas-zoom-level {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; min-width: 3.5em;

&#x20; text-align: center;

&#x20; color: var(--color-text);

&#x20; cursor: pointer;

&#x20; font-variant-numeric: tabular-nums;

}



/\* Mini-map \*/

.canvas-minimap {

&#x20; position: absolute;

&#x20; bottom: var(--space-5);

&#x20; right: var(--space-5);

&#x20; width: 160px;

&#x20; height: 100px;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; overflow: hidden;

&#x20; box-shadow: var(--shadow-md);

&#x20; z-index: 10;

}



/\* Viewport indicator on minimap \*/

.canvas-minimap\_\_viewport {

&#x20; position: absolute;

&#x20; border: 1.5px solid var(--color-accent);

&#x20; border-radius: 2px;

&#x20; background: color-mix(in srgb, var(--color-accent) 15%, transparent);

&#x20; pointer-events: none;

&#x20; /\* Position/size set by JS \*/

&#x20; left:   var(--vp-left, 0);

&#x20; top:    var(--vp-top, 0);

&#x20; width:  var(--vp-w, 30%);

&#x20; height: var(--vp-h, 30%);

}

```



\---



\## 167. CSS COLOUR BLINDNESS SIMULATION



```css

/\* ─── Colour blindness filters (for testing/accessibility) ─── \*/



/\* Apply to root for simulation \*/

.cb-protanopia {   /\* Red-blind \*/

&#x20; filter: url('#protanopia');

}

.cb-deuteranopia { /\* Green-blind (most common) \*/

&#x20; filter: url('#deuteranopia');

}

.cb-tritanopia {   /\* Blue-blind \*/

&#x20; filter: url('#tritanopia');

}

.cb-achromatopsia { /\* No colour \*/

&#x20; filter: grayscale(100%);

}



/\* SVG filter matrix definitions (in HTML) \*/

/\*

<svg style="position:absolute;width:0;height:0">

&#x20; <defs>

&#x20;   <filter id="protanopia">

&#x20;     <feColorMatrix type="matrix" values="

&#x20;       0.56667 0.43333 0     0 0

&#x20;       0.55833 0.44167 0     0 0

&#x20;       0       0.24167 0.75833 0 0

&#x20;       0       0       0     1 0"/>

&#x20;   </filter>

&#x20;   <filter id="deuteranopia">

&#x20;     <feColorMatrix type="matrix" values="

&#x20;       0.625   0.375   0      0 0

&#x20;       0.70    0.30    0      0 0

&#x20;       0       0.30    0.70   0 0

&#x20;       0       0       0      1 0"/>

&#x20;   </filter>

&#x20;   <filter id="tritanopia">

&#x20;     <feColorMatrix type="matrix" values="

&#x20;       0.95    0.05    0      0 0

&#x20;       0       0.43333 0.56667 0 0

&#x20;       0       0.475   0.525  0 0

&#x20;       0       0       0      1 0"/>

&#x20;   </filter>

&#x20; </defs>

</svg>

\*/



/\* ─── High contrast mode CSS (manual) ─── \*/

\[data-contrast="high"] {

&#x20; --color-text:         #000000;

&#x20; --color-bg:           #ffffff;

&#x20; --color-border:       #000000;

&#x20; --color-accent:       #0000ee;

&#x20; --color-text-muted:   #333333;

&#x20; --color-success-500:  #006400;

&#x20; --color-danger-500:   #cc0000;

&#x20; --color-warning-500:  #886600;

}



\[data-contrast="high"] .btn {

&#x20; border: 2px solid currentColor;

&#x20; text-decoration: underline;

}



\[data-contrast="high"] a {

&#x20; color: #0000ee;

&#x20; text-decoration: underline;

}



\[data-contrast="high"] a:visited { color: #551a8b; }

\[data-contrast="high"] :focus-visible {

&#x20; outline: 3px solid #000;

&#x20; outline-offset: 3px;

}

```



\---



\## 168. THE MASTER CSS QUICK REFERENCE CARD



```css

/\*

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

║  .a \~ .b        → all following siblings                            ║

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

║  \*               0-0-0   (zero)                                     ║

║  p, div          0-0-1   (element)                                  ║

║  .class, \[attr]  0-1-0   (class)                                    ║

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

\*/

```



\---



\## FINAL SUMMARY



```

╔══════════════════════════════════════════════════════════════════════╗

║         THE MONUMENTAL CSS GUIDE — PARTS I–XI — COMPLETE            ║

╠══════════════════════════════════════════════════════════════════════╣

║                                                                      ║

║  168 CHAPTERS                                                        ║

║  1,000+ CODE EXAMPLES                                               ║

║  \~38,000 LINES OF CONTENT                                           ║

║  \~700KB COMBINED                                                    ║

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

