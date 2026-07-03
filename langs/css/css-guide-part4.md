\# PART IV — ADVANCED CSS: COMPLETE CONTINUATION



\---



\## 74. CSS FOR PWA \& MOBILE-SPECIFIC PATTERNS



\### 74.1 Safe Area Insets (Notch / Dynamic Island)



```css

/\* ─── iOS safe area support ─── \*/

:root {

&#x20; --sat: env(safe-area-inset-top);

&#x20; --sar: env(safe-area-inset-right);

&#x20; --sab: env(safe-area-inset-bottom);

&#x20; --sal: env(safe-area-inset-left);

}



/\* Full-bleed header that respects notch \*/

.app-header {

&#x20; padding-top: max(var(--space-4), env(safe-area-inset-top));

&#x20; padding-left:  max(var(--space-4), env(safe-area-inset-left));

&#x20; padding-right: max(var(--space-4), env(safe-area-inset-right));

}



/\* Bottom navigation bar \*/

.bottom-nav {

&#x20; position: fixed;

&#x20; bottom: 0;

&#x20; inset-inline: 0;

&#x20; padding-bottom: max(var(--space-3), env(safe-area-inset-bottom));

&#x20; padding-inline: max(var(--space-4), env(safe-area-inset-left));

&#x20; background: var(--color-surface);

&#x20; border-top: 1px solid var(--color-border);

&#x20; z-index: var(--z-fixed);

}



/\* Full viewport — safe \*/

.full-page {

&#x20; min-height: 100dvh;

&#x20; padding: env(safe-area-inset-top, 0)

&#x20;          env(safe-area-inset-right, 0)

&#x20;          env(safe-area-inset-bottom, 0)

&#x20;          env(safe-area-inset-left, 0);

}



/\* Scrollable content above bottom nav \*/

.page-content {

&#x20; padding-bottom: calc(var(--bottom-nav-height, 4rem) + env(safe-area-inset-bottom, 0px));

}

```



\### 74.2 Touch \& Mobile Optimizations



```css

/\* ─── Prevent rubber-band scroll on iOS ─── \*/

html, body {

&#x20; overscroll-behavior: none;      /\* prevent pull-to-refresh \*/

}



/\* Allow only inner scroll containers to scroll \*/

.scroll-container {

&#x20; overflow-y: auto;

&#x20; overscroll-behavior: contain;

&#x20; -webkit-overflow-scrolling: touch;

}



/\* ─── Prevent double-tap zoom ─── \*/

button, a, \[role="button"] {

&#x20; touch-action: manipulation;     /\* removes 300ms tap delay \*/

}



/\* ─── Tap highlight removal ─── \*/

\* {

&#x20; -webkit-tap-highlight-color: transparent;

}



/\* Custom tap highlight for interactive elements \*/

.interactive {

&#x20; -webkit-tap-highlight-color: color-mix(in srgb, var(--color-accent) 15%, transparent);

}



/\* ─── Prevent text selection on UI elements ─── \*/

.ui-element {

&#x20; user-select: none;

&#x20; -webkit-user-select: none;

}



/\* ─── Better input on mobile ─── \*/

input\[type="text"],

input\[type="email"],

input\[type="search"],

textarea {

&#x20; font-size: max(16px, 1rem);     /\* prevents iOS zoom on focus \*/

}



/\* ─── Mobile-only styles ─── \*/

@media (hover: none) and (pointer: coarse) {

&#x20; /\* Touch device \*/

&#x20; .hover-only { display: none; }

&#x20; .btn { min-height: 44px; min-width: 44px; }

&#x20; 

&#x20; /\* Larger tap targets \*/

&#x20; .nav-link {

&#x20;   padding-block: 0.875rem;

&#x20; }

}



/\* ─── Pull to refresh indicator ─── \*/

.pull-indicator {

&#x20; position: fixed;

&#x20; top: 0;

&#x20; left: 50%;

&#x20; translate: -50% calc(-100% + var(--pull, 0px));

&#x20; background: var(--color-surface);

&#x20; border-radius: 0 0 var(--radius-full) var(--radius-full);

&#x20; padding: 0.5rem 1rem;

&#x20; box-shadow: var(--shadow-md);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; transition: translate 0.2s;

}



/\* ─── App icon mask (PWA) ─── \*/

/\* In HTML: <link rel="mask-icon" href="icon.svg" color="#3b82f6"> \*/

/\* In manifest.json: "display": "standalone" \*/



/\* PWA display mode detection \*/

@media (display-mode: standalone) {

&#x20; .install-banner { display: none; }

&#x20; .app-header     { padding-top: env(safe-area-inset-top); }

}



@media (display-mode: fullscreen) {

&#x20; .exit-fullscreen-btn { display: flex; }

}

```



\### 74.3 Mobile Navigation Patterns



```css

/\* ─── Bottom Tab Bar (iOS/Android style) ─── \*/

.tab-bar {

&#x20; position: fixed;

&#x20; bottom: 0;

&#x20; inset-inline: 0;

&#x20; height: calc(3.5rem + env(safe-area-inset-bottom, 0px));

&#x20; padding-bottom: env(safe-area-inset-bottom, 0px);

&#x20; background: var(--color-surface);

&#x20; border-top: 1px solid var(--color-border);

&#x20; display: flex;

&#x20; align-items: stretch;

&#x20; z-index: var(--z-fixed);

}



.tab-bar\_\_item {

&#x20; flex: 1;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: 0.25rem;

&#x20; padding: 0.5rem;

&#x20; text-decoration: none;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

&#x20; transition: color var(--duration-fast);

&#x20; position: relative;

}



.tab-bar\_\_item\[aria-current="page"] {

&#x20; color: var(--color-accent);

}



.tab-bar\_\_icon {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; transition: transform var(--duration-fast) var(--ease-bounce);

}



.tab-bar\_\_item\[aria-current="page"] .tab-bar\_\_icon {

&#x20; transform: scale(1.15) translateY(-1px);

}



/\* Active indicator pill \*/

.tab-bar\_\_item\[aria-current="page"]::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 0;

&#x20; left: 50%;

&#x20; translate: -50%;

&#x20; width: 2rem;

&#x20; height: 3px;

&#x20; background: var(--color-accent);

&#x20; border-radius: 0 0 var(--radius-full) var(--radius-full);

}



/\* ─── Hamburger → X animation ─── \*/

.hamburger {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: 5px;

&#x20; width: 24px;

&#x20; padding: 0;

&#x20; background: none;

&#x20; border: none;

&#x20; cursor: pointer;

}



.hamburger span {

&#x20; display: block;

&#x20; height: 2px;

&#x20; background: currentColor;

&#x20; border-radius: 2px;

&#x20; transform-origin: center;

&#x20; transition:

&#x20;   transform   var(--duration-normal) var(--ease-out),

&#x20;   opacity     var(--duration-normal),

&#x20;   translate   var(--duration-normal) var(--ease-out);

}



.hamburger\[aria-expanded="true"] span:nth-child(1) {

&#x20; translate: 0 7px;

&#x20; transform: rotate(45deg);

}

.hamburger\[aria-expanded="true"] span:nth-child(2) {

&#x20; opacity: 0;

&#x20; transform: scaleX(0);

}

.hamburger\[aria-expanded="true"] span:nth-child(3) {

&#x20; translate: 0 -7px;

&#x20; transform: rotate(-45deg);

}

```



\---



\## 75. CSS MICRO-INTERACTIONS



\### 75.1 Button States \& Feedback



```css

/\* ─── Complete interactive button system ─── \*/

.btn-interactive {

&#x20; position: relative;

&#x20; overflow: hidden;

&#x20; transform: translateZ(0);   /\* GPU layer \*/



&#x20; /\* State variables \*/

&#x20; --state-bg-modifier: 0;

}



/\* Ripple effect \*/

.btn-interactive::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: radial-gradient(

&#x20;   circle at var(--x, 50%) var(--y, 50%),

&#x20;   rgb(255 255 255 / 0.3) 0%,

&#x20;   transparent 70%

&#x20; );

&#x20; opacity: 0;

&#x20; transition: opacity 0.3s;

}



.btn-interactive:active::after {

&#x20; opacity: 1;

&#x20; transition: opacity 0s;

}



/\* Press feedback \*/

.btn-interactive:active {

&#x20; scale: 0.97;

&#x20; transition: scale 0.1s var(--ease-out);

}



/\* Success state \*/

.btn-interactive\[data-state="success"] {

&#x20; --btn-bg: var(--color-success-500);

&#x20; animation: success-bounce 0.4s var(--ease-bounce);

}



@keyframes success-bounce {

&#x20; 0%   { scale: 0.95; }

&#x20; 60%  { scale: 1.05; }

&#x20; 100% { scale: 1; }

}



/\* Loading → Success transition \*/

.btn-interactive\[data-state="loading"] {

&#x20; pointer-events: none;

&#x20; cursor: wait;

}



.btn-interactive\[data-state="loading"] .btn-text {

&#x20; opacity: 0;

&#x20; transform: translateY(-100%);

}



.btn-interactive\[data-state="loading"] .btn-spinner {

&#x20; opacity: 1;

&#x20; transform: translateY(0);

}



/\* ─── Checkbox with animation ─── \*/

.animated-checkbox {

&#x20; --cb-size: 1.25rem;

&#x20; position: relative;

&#x20; width: var(--cb-size);

&#x20; height: var(--cb-size);

}



.animated-checkbox input {

&#x20; position: absolute;

&#x20; opacity: 0;

&#x20; inset: 0;

&#x20; margin: 0;

&#x20; cursor: pointer;

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; z-index: 1;

}



.animated-checkbox\_\_box {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; border: 2px solid var(--color-border-strong);

&#x20; border-radius: var(--radius-sm);

&#x20; background: var(--color-surface);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   background   var(--duration-fast),

&#x20;   scale        var(--duration-fast) var(--ease-bounce);

}



.animated-checkbox input:checked + .animated-checkbox\_\_box {

&#x20; border-color: var(--color-accent);

&#x20; background: var(--color-accent);

&#x20; scale: 1;

&#x20; animation: checkbox-pop 0.25s var(--ease-bounce);

}



@keyframes checkbox-pop {

&#x20; 0%   { scale: 0.8; }

&#x20; 60%  { scale: 1.15; }

&#x20; 100% { scale: 1; }

}



/\* Checkmark SVG path animation \*/

.animated-checkbox\_\_check {

&#x20; stroke-dasharray: 20;

&#x20; stroke-dashoffset: 20;

&#x20; transition: stroke-dashoffset 0.2s ease-out 0.05s;

}



.animated-checkbox input:checked \~ .animated-checkbox\_\_box .animated-checkbox\_\_check {

&#x20; stroke-dashoffset: 0;

}



/\* ─── Like/Heart button ─── \*/

.heart-btn {

&#x20; background: none;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; padding: 0.5rem;

&#x20; position: relative;

}



.heart-btn svg {

&#x20; transition:

&#x20;   fill      var(--duration-fast),

&#x20;   scale     var(--duration-fast) var(--ease-bounce),

&#x20;   filter    var(--duration-fast);

}



.heart-btn\[aria-pressed="true"] svg {

&#x20; fill: var(--color-danger-500);

&#x20; scale: 1;

&#x20; animation: heart-burst 0.4s var(--ease-bounce);

}



@keyframes heart-burst {

&#x20; 0%   { scale: 0.8; }

&#x20; 50%  { scale: 1.3; filter: drop-shadow(0 0 8px var(--color-danger-500)); }

&#x20; 100% { scale: 1; filter: none; }

}



/\* Particle burst on like (via pseudo-elements) \*/

.heart-btn\[aria-pressed="true"]::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; border-radius: 50%;

&#x20; background: var(--color-danger-500);

&#x20; animation: burst-ring 0.4s ease-out forwards;

}



@keyframes burst-ring {

&#x20; 0%   { scale: 0; opacity: 0.8; }

&#x20; 100% { scale: 2.5; opacity: 0; }

}

```



\### 75.2 Input Micro-interactions



```css

/\* ─── Floating label ─── \*/

.float-label {

&#x20; position: relative;

}



.float-label\_\_input {

&#x20; width: 100%;

&#x20; padding: 1.25rem 0.75rem 0.375rem;

&#x20; border: 1px solid var(--color-border-strong);

&#x20; border-radius: var(--radius-md);

&#x20; font: inherit;

&#x20; background: var(--color-surface);

&#x20; outline: none;

&#x20; transition: border-color var(--duration-fast), box-shadow var(--duration-fast);

}



.float-label\_\_label {

&#x20; position: absolute;

&#x20; inset-inline-start: 0.75rem;

&#x20; inset-block-start: 0.875rem;

&#x20; font-size: var(--font-size-base);

&#x20; color: var(--color-text-muted);

&#x20; pointer-events: none;

&#x20; transition:

&#x20;   font-size var(--duration-fast) var(--ease-out),

&#x20;   translate var(--duration-fast) var(--ease-out),

&#x20;   color     var(--duration-fast);

&#x20; transform-origin: left top;

}



/\* Float the label when focused or has value \*/

.float-label\_\_input:focus + .float-label\_\_label,

.float-label\_\_input:not(:placeholder-shown) + .float-label\_\_label {

&#x20; font-size: var(--font-size-xs);

&#x20; translate: 0 -0.625rem;

&#x20; color: var(--color-accent);

}



.float-label\_\_input:focus {

&#x20; border-color: var(--color-accent);

&#x20; box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);

}



/\* ─── Password strength indicator ─── \*/

.password-strength {

&#x20; display: flex;

&#x20; gap: 3px;

&#x20; margin-top: 0.5rem;

}



.strength-bar {

&#x20; flex: 1;

&#x20; height: 4px;

&#x20; border-radius: var(--radius-full);

&#x20; background: var(--color-bg-muted);

&#x20; transition: background var(--duration-slow) var(--ease-out);

&#x20; position: relative;

&#x20; overflow: hidden;

}



.strength-bar::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; border-radius: inherit;

&#x20; background: var(--bar-color, transparent);

&#x20; transform: scaleX(var(--bar-fill, 0));

&#x20; transform-origin: left;

&#x20; transition: transform var(--duration-slow) var(--ease-out);

}



/\* JS sets data-strength="0|1|2|3|4" on parent \*/

.password-strength\[data-strength="1"] .strength-bar:nth-child(1) {

&#x20; --bar-fill: 1; --bar-color: var(--color-danger-500);

}

.password-strength\[data-strength="2"] .strength-bar:nth-child(-n+2) {

&#x20; --bar-fill: 1; --bar-color: var(--color-warning-500);

}

.password-strength\[data-strength="3"] .strength-bar:nth-child(-n+3) {

&#x20; --bar-fill: 1; --bar-color: oklch(0.7 0.2 90);

}

.password-strength\[data-strength="4"] .strength-bar {

&#x20; --bar-fill: 1; --bar-color: var(--color-success-500);

}



/\* ─── Search with results preview ─── \*/

.search-box {

&#x20; position: relative;

&#x20; container-type: inline-size;

}



.search-input {

&#x20; width: 100%;

&#x20; padding: 0.75rem 1rem 0.75rem 2.75rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-full);

&#x20; font: inherit;

&#x20; background: var(--color-surface);

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   box-shadow   var(--duration-fast),

&#x20;   border-radius var(--duration-fast) var(--ease-out);

}



/\* When results are shown, flatten bottom radius \*/

.search-box:has(.search-results:not(:empty)) .search-input {

&#x20; border-radius: var(--radius-xl) var(--radius-xl) 0 0;

&#x20; border-bottom-color: transparent;

&#x20; box-shadow: var(--shadow-xl);

}



.search-results {

&#x20; position: absolute;

&#x20; top: 100%;

&#x20; inset-inline: 0;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-top: none;

&#x20; border-radius: 0 0 var(--radius-xl) var(--radius-xl);

&#x20; box-shadow: var(--shadow-xl);

&#x20; overflow: hidden;

&#x20; max-height: 320px;

&#x20; overflow-y: auto;

}

```



\### 75.3 Navigation Micro-interactions



```css

/\* ─── Animated underline nav ─── \*/

.nav-animated {

&#x20; display: flex;

&#x20; gap: 0;

&#x20; position: relative;

}



/\* Sliding indicator \*/

.nav-animated\_\_indicator {

&#x20; position: absolute;

&#x20; bottom: 0;

&#x20; height: 2px;

&#x20; background: var(--color-accent);

&#x20; border-radius: 2px;

&#x20; transition:

&#x20;   left  var(--duration-slow) var(--ease-out),

&#x20;   width var(--duration-slow) var(--ease-out);

&#x20; /\* JS sets left and width based on active item \*/

}



.nav-animated\_\_link {

&#x20; padding: 0.75rem 1rem;

&#x20; text-decoration: none;

&#x20; color: var(--color-text-muted);

&#x20; font-weight: var(--font-weight-medium);

&#x20; font-size: var(--font-size-sm);

&#x20; white-space: nowrap;

&#x20; transition: color var(--duration-fast);

}



.nav-animated\_\_link:hover,

.nav-animated\_\_link\[aria-current="page"] {

&#x20; color: var(--color-text);

}



/\* ─── Magnetic button effect (via CSS only) ─── \*/

/\* JS manages --mx and --my (mouse offset) \*/

.magnetic {

&#x20; transform: translate(

&#x20;   calc(var(--mx, 0px) \* 0.3),

&#x20;   calc(var(--my, 0px) \* 0.3)

&#x20; );

&#x20; transition: transform 0.2s var(--ease-out);

}



.magnetic:not(:hover) {

&#x20; transform: translate(0, 0);

&#x20; transition: transform 0.5s var(--ease-bounce);

}



/\* ─── Cursor follower ─── \*/

.cursor {

&#x20; width: 12px;

&#x20; height: 12px;

&#x20; background: var(--color-accent);

&#x20; border-radius: 50%;

&#x20; position: fixed;

&#x20; top: 0;

&#x20; left: 0;

&#x20; pointer-events: none;

&#x20; z-index: var(--z-top);

&#x20; translate: calc(var(--cx, 0px) - 50%) calc(var(--cy, 0px) - 50%);

&#x20; transition: translate 0.08s linear, scale 0.2s var(--ease-out);

&#x20; mix-blend-mode: difference;

}



.cursor-ring {

&#x20; width: 40px;

&#x20; height: 40px;

&#x20; border: 1.5px solid var(--color-accent);

&#x20; border-radius: 50%;

&#x20; position: fixed;

&#x20; pointer-events: none;

&#x20; z-index: var(--z-top);

&#x20; translate: calc(var(--cx, 0px) - 50%) calc(var(--cy, 0px) - 50%);

&#x20; transition: translate 0.25s var(--ease-out), scale 0.25s var(--ease-out), opacity 0.25s;

&#x20; mix-blend-mode: difference;

}



/\* Scale on hover interactives \*/

:is(a, button, \[role="button"]):hover \~ .cursor { scale: 3; }

:is(a, button, \[role="button"]):hover \~ .cursor-ring { opacity: 0; }

```



\---



\## 76. ADVANCED COMPONENT PATTERNS



\### 76.1 Drawer / Sidebar



```css

/\* ─── Slide-in Drawer ─── \*/

.drawer-overlay {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; background: rgb(0 0 0 / 0);

&#x20; backdrop-filter: blur(0px);

&#x20; z-index: var(--z-overlay);

&#x20; pointer-events: none;

&#x20; transition:

&#x20;   background    var(--duration-slow),

&#x20;   backdrop-filter var(--duration-slow),

&#x20;   display       var(--duration-slow) allow-discrete,

&#x20;   overlay       var(--duration-slow) allow-discrete;

}



.drawer-overlay\[data-open="true"] {

&#x20; background: rgb(0 0 0 / 0.5);

&#x20; backdrop-filter: blur(4px);

&#x20; pointer-events: auto;

}



@starting-style {

&#x20; .drawer-overlay\[data-open="true"] {

&#x20;   background: rgb(0 0 0 / 0);

&#x20;   backdrop-filter: blur(0px);

&#x20; }

}



.drawer {

&#x20; position: fixed;

&#x20; inset-block: 0;

&#x20; inset-inline-start: 0;

&#x20; width: min(360px, 85vw);

&#x20; background: var(--color-surface);

&#x20; box-shadow: var(--shadow-2xl);

&#x20; z-index: var(--z-modal);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; overflow: hidden;



&#x20; translate: -100% 0;

&#x20; transition:

&#x20;   translate var(--duration-slow) var(--ease-out),

&#x20;   display   var(--duration-slow) allow-discrete,

&#x20;   overlay   var(--duration-slow) allow-discrete;

}



.drawer\[data-open="true"] {

&#x20; translate: 0 0;

}



@starting-style {

&#x20; .drawer\[data-open="true"] {

&#x20;   translate: -100% 0;

&#x20; }

}



/\* Right drawer \*/

.drawer--right {

&#x20; inset-inline-start: auto;

&#x20; inset-inline-end: 0;

&#x20; translate: 100% 0;

}

.drawer--right\[data-open="true"] {

&#x20; translate: 0 0;

}



/\* Bottom sheet \*/

.drawer--bottom {

&#x20; inset-inline: 0;

&#x20; inset-block-start: auto;

&#x20; width: 100%;

&#x20; max-height: 90dvh;

&#x20; border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;

&#x20; translate: 0 100%;

}

.drawer--bottom\[data-open="true"] {

&#x20; translate: 0 0;

}



/\* Drag handle for bottom sheet \*/

.drawer--bottom::before {

&#x20; content: '';

&#x20; display: block;

&#x20; width: 2.5rem;

&#x20; height: 4px;

&#x20; background: var(--color-border-strong);

&#x20; border-radius: var(--radius-full);

&#x20; margin: 0.75rem auto;

&#x20; flex-shrink: 0;

}



/\* Drawer sections \*/

.drawer\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-5) var(--space-6);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; flex-shrink: 0;

}



.drawer\_\_body {

&#x20; flex: 1;

&#x20; overflow-y: auto;

&#x20; padding: var(--space-6);

&#x20; overscroll-behavior: contain;

}



.drawer\_\_footer {

&#x20; padding: var(--space-4) var(--space-6);

&#x20; border-top: 1px solid var(--color-border);

&#x20; flex-shrink: 0;

&#x20; display: flex;

&#x20; gap: var(--space-3);

&#x20; justify-content: flex-end;

}

```



\### 76.2 Combobox / Autocomplete



```css

/\* ─── Combobox (accessible autocomplete) ─── \*/

.combobox {

&#x20; position: relative;

}



.combobox\_\_input-wrapper {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.5rem;

&#x20; padding: 0.5rem 0.75rem;

&#x20; border: 1px solid var(--color-border-strong);

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-surface);

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   box-shadow   var(--duration-fast),

&#x20;   border-radius var(--duration-fast);

}



.combobox:has(.combobox\_\_listbox:not(\[hidden])) .combobox\_\_input-wrapper {

&#x20; border-radius: var(--radius-md) var(--radius-md) 0 0;

&#x20; border-color: var(--color-accent);

&#x20; box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);

}



.combobox\_\_input {

&#x20; flex: 1;

&#x20; border: none;

&#x20; background: none;

&#x20; font: inherit;

&#x20; color: var(--color-text);

&#x20; outline: none;

&#x20; min-width: 0;

}



.combobox\_\_toggle {

&#x20; padding: 0;

&#x20; background: none;

&#x20; border: none;

&#x20; color: var(--color-text-muted);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; transition: transform var(--duration-fast);

}



.combobox:has(.combobox\_\_listbox:not(\[hidden])) .combobox\_\_toggle {

&#x20; transform: rotate(180deg);

}



/\* Listbox \*/

.combobox\_\_listbox {

&#x20; position: absolute;

&#x20; top: 100%;

&#x20; inset-inline: 0;

&#x20; max-height: 256px;

&#x20; overflow-y: auto;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-accent);

&#x20; border-top: none;

&#x20; border-radius: 0 0 var(--radius-md) var(--radius-md);

&#x20; box-shadow: var(--shadow-xl);

&#x20; z-index: var(--z-dropdown);

&#x20; overscroll-behavior: contain;

&#x20; scrollbar-width: thin;

}



.combobox\_\_option {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: 0.625rem 0.75rem;

&#x20; cursor: pointer;

&#x20; font-size: var(--font-size-sm);

&#x20; transition: background var(--duration-fast);

}



.combobox\_\_option:hover,

.combobox\_\_option\[aria-selected="true"] {

&#x20; background: var(--color-bg-subtle);

}



.combobox\_\_option\[data-active="true"] {

&#x20; background: color-mix(in srgb, var(--color-accent) 10%, transparent);

&#x20; color: var(--color-accent);

}



/\* Highlight matching text \*/

.combobox\_\_option mark {

&#x20; background: color-mix(in srgb, var(--color-warning-500) 30%, transparent);

&#x20; color: inherit;

&#x20; border-radius: 2px;

}



/\* Group headers \*/

.combobox\_\_group-label {

&#x20; padding: 0.375rem 0.75rem;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; position: sticky;

&#x20; top: 0;

&#x20; background: var(--color-surface);

&#x20; z-index: 1;

}



/\* No results \*/

.combobox\_\_empty {

&#x20; padding: var(--space-4);

&#x20; text-align: center;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

}

```



\### 76.3 Date Picker



```css

/\* ─── Calendar / Date Picker ─── \*/

.datepicker {

&#x20; position: relative;

&#x20; display: inline-block;

}



.datepicker\_\_trigger {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.5rem;

&#x20; padding: 0.5rem 0.75rem;

&#x20; border: 1px solid var(--color-border-strong);

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-surface);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; cursor: pointer;

&#x20; transition: border-color var(--duration-fast);

}

.datepicker\_\_trigger:hover { border-color: var(--color-neutral-400); }

.datepicker\_\_trigger:focus-visible {

&#x20; outline: 2px solid var(--color-accent);

&#x20; outline-offset: 2px;

}



.datepicker\_\_popup {

&#x20; position: absolute;

&#x20; top: calc(100% + 8px);

&#x20; inset-inline-start: 0;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; box-shadow: var(--shadow-xl);

&#x20; padding: var(--space-4);

&#x20; z-index: var(--z-dropdown);

&#x20; width: 280px;

&#x20; 

&#x20; /\* Open animation \*/

&#x20; animation: popup-appear var(--duration-normal) var(--ease-out);

}



@keyframes popup-appear {

&#x20; from { opacity: 0; translate: 0 -8px; scale: 0.97; }

&#x20; to   { opacity: 1; translate: 0 0; scale: 1; }

}



/\* Calendar header \*/

.cal-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; margin-bottom: var(--space-3);

}



.cal-header\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; cursor: pointer;

&#x20; padding: 0.25rem 0.5rem;

&#x20; border-radius: var(--radius-md);

&#x20; transition: background var(--duration-fast);

}

.cal-header\_\_title:hover { background: var(--color-bg-subtle); }



.cal-nav {

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; border-radius: var(--radius-md);

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-text-muted);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.cal-nav:hover {

&#x20; background: var(--color-bg-subtle);

&#x20; color: var(--color-text);

}



/\* Day grid \*/

.cal-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(7, 1fr);

&#x20; gap: 2px;

}



.cal-weekday {

&#x20; text-align: center;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

&#x20; padding: 0.25rem 0;

}



.cal-day {

&#x20; aspect-ratio: 1;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: var(--font-size-sm);

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; border: none;

&#x20; background: none;

&#x20; color: var(--color-text);

&#x20; transition:

&#x20;   background var(--duration-fast),

&#x20;   color      var(--duration-fast),

&#x20;   scale      var(--duration-fast) var(--ease-bounce);

&#x20; font-variant-numeric: tabular-nums;

}



.cal-day:hover {

&#x20; background: var(--color-bg-subtle);

&#x20; scale: 1.1;

}

.cal-day:focus-visible {

&#x20; outline: 2px solid var(--color-accent);

&#x20; outline-offset: 2px;

}

.cal-day--outside { color: var(--color-text-subtle); }

.cal-day--today {

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-accent);

}

.cal-day--selected {

&#x20; background: var(--color-accent);

&#x20; color: white;

}

.cal-day--selected:hover { background: var(--color-accent-hover); }

.cal-day--disabled {

&#x20; opacity: 0.3;

&#x20; cursor: not-allowed;

&#x20; pointer-events: none;

}



/\* Range selection \*/

.cal-day--in-range {

&#x20; background: color-mix(in srgb, var(--color-accent) 15%, transparent);

&#x20; border-radius: 0;

}

.cal-day--range-start { border-radius: var(--radius-md) 0 0 var(--radius-md); }

.cal-day--range-end   { border-radius: 0 var(--radius-md) var(--radius-md) 0; }

```



\### 76.4 Context Menu / Right-click Menu



```css

/\* ─── Context Menu ─── \*/

.context-menu {

&#x20; position: fixed;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; box-shadow: var(--shadow-xl);

&#x20; padding: var(--space-1);

&#x20; z-index: var(--z-popover);

&#x20; min-width: 180px;

&#x20; max-width: 240px;



&#x20; /\* Position set by JS \*/

&#x20; top: var(--y, 0);

&#x20; left: var(--x, 0);



&#x20; animation: context-appear 0.12s var(--ease-out);

&#x20; transform-origin: var(--origin-x, left) var(--origin-y, top);

}



@keyframes context-appear {

&#x20; from { opacity: 0; scale: 0.92; }

&#x20; to   { opacity: 1; scale: 1; }

}



.context-menu\_\_item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: 0.5rem 0.75rem;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text);

&#x20; border: none;

&#x20; background: none;

&#x20; width: 100%;

&#x20; text-align: start;

&#x20; transition: background var(--duration-fast);

}



.context-menu\_\_item:hover {

&#x20; background: var(--color-bg-subtle);

}



.context-menu\_\_item--danger {

&#x20; color: var(--color-danger-500);

}

.context-menu\_\_item--danger:hover {

&#x20; background: var(--color-danger-100);

}



.context-menu\_\_item--disabled {

&#x20; opacity: 0.4;

&#x20; cursor: not-allowed;

&#x20; pointer-events: none;

}



.context-menu\_\_shortcut {

&#x20; margin-inline-start: auto;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-variant-numeric: tabular-nums;

}



.context-menu\_\_separator {

&#x20; height: 1px;

&#x20; background: var(--color-border);

&#x20; margin: var(--space-1) 0;

}



.context-menu\_\_label {

&#x20; padding: 0.25rem 0.75rem;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

}



/\* Nested submenu \*/

.context-menu\_\_item--submenu::after {

&#x20; content: '›';

&#x20; margin-inline-start: auto;

&#x20; opacity: 0.5;

}



.context-menu\_\_submenu {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; left: 100%;

&#x20; margin-left: 4px;

&#x20; /\* Same styles as .context-menu \*/

}

.context-menu\_\_item--submenu:hover .context-menu\_\_submenu {

&#x20; display: block;

}

```



\### 76.5 Multi-select / Tag Input



```css

/\* ─── Tag Input ─── \*/

.tag-input {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-2);

&#x20; padding: 0.375rem 0.75rem;

&#x20; border: 1px solid var(--color-border-strong);

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-surface);

&#x20; min-height: 2.5rem;

&#x20; cursor: text;

&#x20; align-items: center;

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   box-shadow   var(--duration-fast);

}



.tag-input:focus-within {

&#x20; border-color: var(--color-accent);

&#x20; box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);

}



/\* Individual tags \*/

.tag-input\_\_tag {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: 0.25rem;

&#x20; padding: 0.125rem 0.5rem;

&#x20; background: var(--color-brand-100);

&#x20; color: var(--color-brand-700);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; max-width: 180px;

&#x20; animation: tag-appear 0.2s var(--ease-bounce);

}



@keyframes tag-appear {

&#x20; from { scale: 0.7; opacity: 0; }

&#x20; to   { scale: 1; opacity: 1; }

}



.tag-input\_\_tag span {

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



.tag-input\_\_remove {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; width: 1rem;

&#x20; height: 1rem;

&#x20; border-radius: 50%;

&#x20; border: none;

&#x20; background: none;

&#x20; color: inherit;

&#x20; cursor: pointer;

&#x20; opacity: 0.6;

&#x20; flex-shrink: 0;

&#x20; padding: 0;

&#x20; transition: opacity var(--duration-fast), background var(--duration-fast);

}

.tag-input\_\_remove:hover {

&#x20; opacity: 1;

&#x20; background: color-mix(in srgb, currentColor 15%, transparent);

}



/\* Dismissing tag \*/

.tag-input\_\_tag.removing {

&#x20; animation: tag-remove 0.15s var(--ease-in) forwards;

}



@keyframes tag-remove {

&#x20; to { scale: 0; opacity: 0; width: 0; padding: 0; margin: 0; }

}



/\* Input \*/

.tag-input\_\_input {

&#x20; border: none;

&#x20; background: none;

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text);

&#x20; outline: none;

&#x20; flex: 1;

&#x20; min-width: 80px;

}

```



\---



\## 77. CSS FOR PROSE CONTENT



\### 77.1 Typography for Long-form Reading



```css

/\* ─── The Prose Component ─── \*/

.prose {

&#x20; /\* Measure (line length) \*/

&#x20; max-width: 65ch;

&#x20; 

&#x20; /\* Base typography \*/

&#x20; font-size: clamp(1rem, 1.5vw + 0.5rem, 1.125rem);

&#x20; line-height: var(--line-height-relaxed);

&#x20; color: var(--color-text);

&#x20; 

&#x20; /\* Hanging punctuation \*/

&#x20; hanging-punctuation: first last;

}



/\* ─── Vertical rhythm ─── \*/

.prose > \* {

&#x20; margin-block: 0;

}



.prose > \* + \* {

&#x20; margin-block-start: 1em;

}



/\* Tighter after headings \*/

.prose h2 + \*,

.prose h3 + \*,

.prose h4 + \* {

&#x20; margin-block-start: 0.5em;

}



/\* ─── Headings ─── \*/

.prose h1, .prose h2, .prose h3,

.prose h4, .prose h5, .prose h6 {

&#x20; font-weight: var(--font-weight-bold);

&#x20; line-height: var(--line-height-tight);

&#x20; text-wrap: balance;

&#x20; margin-block-start: 2em;

}



.prose h1 { font-size: var(--step-4); }

.prose h2 { font-size: var(--step-3); }

.prose h3 { font-size: var(--step-2); }

.prose h4 { font-size: var(--step-1); }

.prose h5, .prose h6 { font-size: var(--step-0); }



/\* Anchors on headings \*/

.prose :is(h2, h3, h4) .heading-anchor {

&#x20; opacity: 0;

&#x20; margin-inline-start: 0.5em;

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: none;

&#x20; font-weight: normal;

&#x20; transition: opacity var(--duration-fast);

}

.prose :is(h2, h3, h4):hover .heading-anchor {

&#x20; opacity: 1;

}



/\* ─── Paragraphs ─── \*/

.prose p {

&#x20; overflow-wrap: break-word;

&#x20; text-wrap: pretty;

}



/\* ─── Links ─── \*/

.prose a {

&#x20; color: var(--color-accent);

&#x20; text-decoration-line: underline;

&#x20; text-decoration-color: color-mix(in srgb, var(--color-accent) 40%, transparent);

&#x20; text-underline-offset: 0.2em;

&#x20; text-decoration-thickness: 1px;

&#x20; transition:

&#x20;   text-decoration-color var(--duration-fast),

&#x20;   text-decoration-thickness var(--duration-fast);

}



.prose a:hover {

&#x20; text-decoration-color: var(--color-accent);

&#x20; text-decoration-thickness: 2px;

}



/\* ─── Lists ─── \*/

.prose ul, .prose ol {

&#x20; padding-inline-start: 1.5em;

}



.prose ul { list-style-type: disc; }

.prose ol { list-style-type: decimal; }



.prose li + li { margin-block-start: 0.5em; }

.prose li > ul, .prose li > ol { margin-block-start: 0.5em; }



/\* Custom bullet \*/

.prose ul li::marker {

&#x20; color: var(--color-accent);

&#x20; font-size: 0.8em;

}



/\* ─── Blockquote ─── \*/

.prose blockquote {

&#x20; border-inline-start: 3px solid var(--color-accent);

&#x20; padding-inline-start: 1.5em;

&#x20; padding-block: 0.25em;

&#x20; color: var(--color-text-muted);

&#x20; font-style: italic;

&#x20; font-size: 1.05em;

&#x20; quotes: '\\201C' '\\201D';

}



.prose blockquote::before {

&#x20; content: open-quote;

&#x20; font-size: 3em;

&#x20; line-height: 0;

&#x20; vertical-align: -0.5em;

&#x20; color: var(--color-accent);

&#x20; margin-inline-end: 0.1em;

}



/\* ─── Code blocks ─── \*/

.prose pre {

&#x20; background: var(--color-neutral-900);

&#x20; color: var(--color-neutral-100);

&#x20; padding: 1.25em 1.5em;

&#x20; border-radius: var(--radius-lg);

&#x20; overflow-x: auto;

&#x20; font-size: 0.875em;

&#x20; line-height: 1.7;

&#x20; tab-size: 2;

&#x20; hyphens: none;

&#x20; margin-block: 1.5em;

&#x20; position: relative;

}



/\* Line numbers \*/

.prose pre\[data-line-numbers] {

&#x20; counter-reset: line;

&#x20; padding-inline-start: 3.5em;

}

.prose pre\[data-line-numbers] .line::before {

&#x20; counter-increment: line;

&#x20; content: counter(line);

&#x20; position: absolute;

&#x20; left: 1em;

&#x20; color: var(--color-neutral-600);

&#x20; user-select: none;

&#x20; text-align: right;

&#x20; width: 1.5em;

}



/\* Copy button for code \*/

.prose pre .copy-btn {

&#x20; position: absolute;

&#x20; top: 0.75rem;

&#x20; right: 0.75rem;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

}

.prose pre:hover .copy-btn { opacity: 1; }



/\* Inline code \*/

.prose code:not(pre code) {

&#x20; background: var(--color-bg-muted);

&#x20; padding: 0.125em 0.375em;

&#x20; border-radius: var(--radius-sm);

&#x20; font-size: 0.875em;

&#x20; font-family: var(--font-mono);

&#x20; color: var(--color-text);

&#x20; word-break: break-all;

}



/\* ─── Tables ─── \*/

.prose table {

&#x20; width: 100%;

&#x20; border-collapse: collapse;

&#x20; font-size: 0.875em;

&#x20; margin-block: 1.5em;

&#x20; overflow-x: auto;

&#x20; display: block;

}



.prose th, .prose td {

&#x20; padding: 0.5em 0.75em;

&#x20; text-align: start;

&#x20; border: 1px solid var(--color-border);

}



.prose th {

&#x20; background: var(--color-bg-subtle);

&#x20; font-weight: var(--font-weight-semibold);

}



.prose tbody tr:nth-child(even) {

&#x20; background: var(--color-bg-subtle);

}



/\* ─── HR ─── \*/

.prose hr {

&#x20; border: none;

&#x20; height: 1px;

&#x20; background: var(--color-border);

&#x20; margin-block: 2em;

}



/\* Fancy HR \*/

.prose hr.fancy {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 1em;

&#x20; border: none;

&#x20; height: auto;

}

.prose hr.fancy::before,

.prose hr.fancy::after {

&#x20; content: '';

&#x20; flex: 1;

&#x20; height: 1px;

&#x20; background: var(--color-border);

}

.prose hr.fancy::before { content: '❧'; flex: none; }



/\* ─── Images in prose ─── \*/

.prose img {

&#x20; border-radius: var(--radius-lg);

&#x20; margin-block: 1.5em;

}



.prose figure {

&#x20; margin-inline: 0;

&#x20; margin-block: 2em;

}



.prose figcaption {

&#x20; text-align: center;

&#x20; font-size: 0.875em;

&#x20; color: var(--color-text-muted);

&#x20; font-style: italic;

&#x20; margin-block-start: 0.5em;

}



/\* ─── Callout / Note boxes ─── \*/

.prose .callout {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; padding: var(--space-4) var(--space-5);

&#x20; border-radius: var(--radius-lg);

&#x20; border-inline-start: 4px solid var(--callout-color, var(--color-brand-500));

&#x20; background: color-mix(in srgb, var(--callout-color, var(--color-brand-500)) 8%, var(--color-surface));

}



.prose .callout--info    { --callout-color: var(--color-brand-500); }

.prose .callout--warning { --callout-color: var(--color-warning-500); }

.prose .callout--danger  { --callout-color: var(--color-danger-500); }

.prose .callout--success { --callout-color: var(--color-success-500); }



/\* ─── Footnotes ─── \*/

.prose .footnotes {

&#x20; margin-block-start: 3em;

&#x20; padding-block-start: 2em;

&#x20; border-block-start: 1px solid var(--color-border);

&#x20; font-size: 0.875em;

&#x20; color: var(--color-text-muted);

}



.prose .footnote-ref {

&#x20; font-size: 0.75em;

&#x20; vertical-align: super;

&#x20; font-variant-numeric: tabular-nums;

&#x20; line-height: 0;

}

```



\---



\## 78. CSS IMAGE GALLERIES



\### 78.1 Masonry Gallery



```css

/\* ─── CSS Column Masonry (simple) ─── \*/

.gallery-masonry {

&#x20; column-count: 3;

&#x20; column-gap: var(--space-4);

&#x20; column-fill: balance;

}



.gallery-masonry .item {

&#x20; break-inside: avoid;

&#x20; margin-bottom: var(--space-4);

&#x20; border-radius: var(--radius-lg);

&#x20; overflow: hidden;

}



/\* Responsive masonry \*/

.gallery-masonry {

&#x20; column-count: 1;

}

@media (min-width: 480px) { .gallery-masonry { column-count: 2; } }

@media (min-width: 768px) { .gallery-masonry { column-count: 3; } }

@media (min-width: 1200px) { .gallery-masonry { column-count: 4; } }



/\* Or: Native CSS masonry (behind flag) \*/

.gallery-native-masonry {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));

&#x20; grid-template-rows: masonry;

&#x20; gap: var(--space-4);

}



/\* ─── Grid-based mosaic ─── \*/

.gallery-mosaic {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(12, 1fr);

&#x20; grid-auto-rows: 60px;

&#x20; gap: var(--space-3);

}



.gallery-mosaic .item {

&#x20; border-radius: var(--radius-lg);

&#x20; overflow: hidden;

&#x20; position: relative;

}



.gallery-mosaic .item img {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; transition: transform var(--duration-slow) var(--ease-out);

}



.gallery-mosaic .item:hover img {

&#x20; transform: scale(1.05);

}



/\* Predefined mosaic patterns \*/

.gallery-mosaic .item:nth-child(1)  { grid-column: span 6; grid-row: span 5; }

.gallery-mosaic .item:nth-child(2)  { grid-column: span 3; grid-row: span 3; }

.gallery-mosaic .item:nth-child(3)  { grid-column: span 3; grid-row: span 3; }

.gallery-mosaic .item:nth-child(4)  { grid-column: span 3; grid-row: span 2; }

.gallery-mosaic .item:nth-child(5)  { grid-column: span 3; grid-row: span 2; }

.gallery-mosaic .item:nth-child(6)  { grid-column: span 4; grid-row: span 3; }

.gallery-mosaic .item:nth-child(7)  { grid-column: span 4; grid-row: span 3; }

.gallery-mosaic .item:nth-child(8)  { grid-column: span 4; grid-row: span 3; }

```



\### 78.2 Lightbox / Image Viewer



```css

/\* ─── CSS-only lightbox (via :target) ─── \*/

.lightbox {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; background: rgb(0 0 0 / 0);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; padding: var(--space-4);

&#x20; z-index: var(--z-modal);

&#x20; pointer-events: none;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-slow), background var(--duration-slow);

}



.lightbox:target {

&#x20; opacity: 1;

&#x20; background: rgb(0 0 0 / 0.9);

&#x20; pointer-events: auto;

&#x20; backdrop-filter: blur(8px);

}



.lightbox\_\_inner {

&#x20; position: relative;

&#x20; max-width: min(90vw, 1200px);

&#x20; max-height: 90dvh;

&#x20; transform: scale(0.9);

&#x20; transition: transform var(--duration-slow) var(--ease-bounce);

}



.lightbox:target .lightbox\_\_inner {

&#x20; transform: scale(1);

}



.lightbox\_\_close {

&#x20; position: absolute;

&#x20; top: -3rem;

&#x20; right: 0;

&#x20; color: white;

&#x20; text-decoration: none;

&#x20; font-size: 1.5rem;

&#x20; opacity: 0.7;

&#x20; transition: opacity var(--duration-fast);

}

.lightbox\_\_close:hover { opacity: 1; }



.lightbox\_\_img {

&#x20; display: block;

&#x20; max-width: 100%;

&#x20; max-height: 80dvh;

&#x20; border-radius: var(--radius-lg);

&#x20; object-fit: contain;

&#x20; box-shadow: var(--shadow-2xl);

}



.lightbox\_\_caption {

&#x20; color: rgb(255 255 255 / 0.7);

&#x20; text-align: center;

&#x20; padding: var(--space-3);

&#x20; font-size: var(--font-size-sm);

}



/\* ─── Image hover zoom ─── \*/

.gallery-zoom-item {

&#x20; overflow: hidden;

&#x20; border-radius: var(--radius-lg);

&#x20; position: relative;

}



.gallery-zoom-item img {

&#x20; transition:

&#x20;   transform var(--duration-slow) var(--ease-out),

&#x20;   filter    var(--duration-slow) var(--ease-out);

&#x20; display: block;

&#x20; width: 100%;

}



.gallery-zoom-item:hover img {

&#x20; transform: scale(1.08);

&#x20; filter: brightness(0.85);

}



/\* Reveal overlay on hover \*/

.gallery-zoom-item .overlay {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: white;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-normal);

&#x20; background: linear-gradient(

&#x20;   to top,

&#x20;   rgb(0 0 0 / 0.7) 0%,

&#x20;   transparent 50%

&#x20; );

}



.gallery-zoom-item:hover .overlay {

&#x20; opacity: 1;

}

```



\---



\## 79. CSS FOR CODE BLOCKS



\### 79.1 Syntax Highlighting Themes



```css

/\* ─── Dark code theme (Monokai-inspired) ─── \*/

.code-block {

&#x20; --code-bg:        #272822;

&#x20; --code-text:      #f8f8f2;

&#x20; --code-comment:   #75715e;

&#x20; --code-keyword:   #f92672;

&#x20; --code-string:    #e6db74;

&#x20; --code-number:    #ae81ff;

&#x20; --code-function:  #a6e22e;

&#x20; --code-operator:  #f92672;

&#x20; --code-class:     #66d9ef;

&#x20; --code-property:  #66d9ef;

&#x20; --code-variable:  #fd971f;

&#x20; --code-tag:       #f92672;

&#x20; --code-attr:      #a6e22e;



&#x20; background: var(--code-bg);

&#x20; color: var(--code-text);

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.875em;

&#x20; line-height: 1.7;

&#x20; padding: 1.5rem;

&#x20; border-radius: var(--radius-lg);

&#x20; overflow-x: auto;

&#x20; tab-size: 2;

&#x20; white-space: pre;

&#x20; -webkit-overflow-scrolling: touch;

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



/\* ─── Light code theme ─── \*/

.code-block--light {

&#x20; --code-bg:       #f8f8f8;

&#x20; --code-text:     #383a42;

&#x20; --code-comment:  #a0a1a7;

&#x20; --code-keyword:  #a626a4;

&#x20; --code-string:   #50a14f;

&#x20; --code-number:   #986801;

&#x20; --code-function: #4078f2;

&#x20; --code-class:    #c18401;

}



/\* ─── Code window chrome ─── \*/

.code-window {

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; box-shadow: var(--shadow-xl);

}



.code-window\_\_titlebar {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.75rem 1rem;

&#x20; background: #3c3c3c;

}



.code-window\_\_dot {

&#x20; width: 12px;

&#x20; height: 12px;

&#x20; border-radius: 50%;

}

.code-window\_\_dot:nth-child(1) { background: #ff5f56; }

.code-window\_\_dot:nth-child(2) { background: #ffbd2e; }

.code-window\_\_dot:nth-child(3) { background: #27c93f; }



.code-window\_\_filename {

&#x20; margin-inline-start: auto;

&#x20; margin-inline-end: auto;

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgb(255 255 255 / 0.6);

&#x20; font-family: var(--font-mono);

}



/\* ─── Diff code blocks ─── \*/

.code-diff .line-added {

&#x20; background: color-mix(in srgb, var(--color-success-500) 15%, transparent);

&#x20; display: block;

&#x20; margin-inline: -1.5rem;

&#x20; padding-inline: 1.5rem;

}

.code-diff .line-added::before {

&#x20; content: '+';

&#x20; color: var(--color-success-500);

&#x20; margin-inline-end: 0.5em;

}



.code-diff .line-removed {

&#x20; background: color-mix(in srgb, var(--color-danger-500) 15%, transparent);

&#x20; display: block;

&#x20; margin-inline: -1.5rem;

&#x20; padding-inline: 1.5rem;

&#x20; text-decoration: line-through;

&#x20; opacity: 0.7;

}

.code-diff .line-removed::before {

&#x20; content: '-';

&#x20; color: var(--color-danger-500);

&#x20; margin-inline-end: 0.5em;

}

```



\---



\## 80. CSS SPRING PHYSICS ANIMATIONS



\### 80.1 Spring-like Motion via CSS



```css

/\* ─── Spring easing approximations ─── \*/

:root {

&#x20; /\* Gentle spring \*/

&#x20; --spring-gentle: linear(

&#x20;   0, 0.014 2.7%, 0.106 6.2%, 0.378 13.2%, 0.827 21.3%, 1.005 25.2%,

&#x20;   1.094 28.7%, 1.129 30.7%, 1.151 32.7%, 1.152 34.2%, 1.135 36.5%,

&#x20;   1.073 41.5%, 1.017 47.5%, 1

&#x20; );



&#x20; /\* Bouncy spring \*/

&#x20; --spring-bouncy: linear(

&#x20;   0, 0.009 1.9%, 0.069 4.3%, 0.274 8.8%, 0.95 15.8%, 1.14 19.5%,

&#x20;   1.196 22.1%, 1.208 24.4%, 1.196 26.8%, 1.126 31.2%,

&#x20;   1.034 37.1%, 1.005 39.8%, 0.994 42.7%, 1

&#x20; );



&#x20; /\* Stiff spring \*/

&#x20; --spring-stiff: linear(

&#x20;   0, 0.052 3.7%, 0.231 7.6%, 0.738 15.5%, 1.018 19.6%, 1.071 22.6%,

&#x20;   1.07 25.2%, 1.042 28.1%, 1.007 32.6%, 0.997 36.9%, 1

&#x20; );



&#x20; /\* Wobbly spring \*/

&#x20; --spring-wobbly: linear(

&#x20;   0, 0.004 1.1%, 0.033 2.9%, 0.123 6.1%, 0.471 12.5%, 0.704 16.4%,

&#x20;   0.805 18.9%, 0.906 22.7%, 0.965 26.8%, 0.992 30.7%,

&#x20;   1.001 34.5%, 1.004 38%, 1.001 41.6%, 0.999 46.1%, 1

&#x20; );

}



/\* ─── Usage examples ─── \*/

.spring-appear {

&#x20; scale: 0;

&#x20; opacity: 0;

&#x20; transition:

&#x20;   scale   0.5s var(--spring-bouncy),

&#x20;   opacity 0.3s ease-out;

}



.spring-appear.visible {

&#x20; scale: 1;

&#x20; opacity: 1;

}



.spring-hover {

&#x20; transition: transform 0.4s var(--spring-gentle);

}

.spring-hover:hover {

&#x20; transform: translateY(-4px) scale(1.02);

}



.spring-press {

&#x20; transition: scale 0.15s var(--spring-stiff);

}

.spring-press:active {

&#x20; scale: 0.95;

}



/\* ─── Staggered spring entrance ─── \*/

.spring-list .item {

&#x20; opacity: 0;

&#x20; translate: 0 20px;

&#x20; animation: spring-in var(--spring-bouncy) 0.5s forwards;

&#x20; animation-delay: calc(var(--i, 0) \* 80ms);

}



@keyframes spring-in {

&#x20; to { opacity: 1; translate: 0 0; }

}



/\* ─── WAAPI (Web Animations API) with springs ─── \*/

/\*

element.animate(\[

&#x20; { transform: 'scale(0)', opacity: 0 },

&#x20; { transform: 'scale(1)', opacity: 1 }

], {

&#x20; duration: 500,

&#x20; easing: 'linear(0, 0.009 1.9%, 0.069 4.3%, ... 1)',

&#x20; fill: 'both'

});

\*/

```



\---



\## 81. CSS FOR EMPTY STATES \& ERROR STATES



\### 81.1 Empty State Patterns



```css

/\* ─── Empty state component ─── \*/

.empty-state {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; text-align: center;

&#x20; padding: var(--space-16) var(--space-8);

&#x20; gap: var(--space-4);

}



.empty-state\_\_illustration {

&#x20; width: min(200px, 60%);

&#x20; height: auto;

&#x20; opacity: 0.6;

&#x20; filter: grayscale(30%);

}



/\* CSS-only illustration placeholder \*/

.empty-state\_\_icon {

&#x20; width: 80px;

&#x20; height: 80px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-2xl);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 2rem;

&#x20; color: var(--color-text-muted);

&#x20; margin-inline: auto;

}



.empty-state\_\_title {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text);

}



.empty-state\_\_description {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; max-width: 40ch;

&#x20; text-wrap: balance;

}



/\* ─── Auto-show empty state when container is empty ─── \*/

.auto-empty {

&#x20; position: relative;

}



.auto-empty > .empty-state {

&#x20; display: none;

}



/\* Show when no real children \*/

.auto-empty:not(:has(> :not(.empty-state))) > .empty-state {

&#x20; display: flex;

}



/\* ─── Empty list with dash pattern ─── \*/

.empty-list-placeholder {

&#x20; padding: var(--space-8);

&#x20; border: 2px dashed var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   background   var(--duration-fast);

}



.empty-list-placeholder:hover {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 5%, transparent);

&#x20; color: var(--color-accent);

}



/\* ─── Drag and drop target ─── \*/

.drop-zone {

&#x20; border: 2px dashed var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-12);

&#x20; text-align: center;

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   background   var(--duration-fast),

&#x20;   scale        var(--duration-fast) var(--ease-bounce);

}



.drop-zone\[data-dragging="true"],

.drop-zone:focus-within {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, transparent);

&#x20; scale: 1.01;

}

```



\### 81.2 Error \& Validation States



```css

/\* ─── Form error patterns ─── \*/

.field--error .input {

&#x20; border-color: var(--color-danger-500);

&#x20; background: var(--color-danger-100);

}



.field--error .input:focus {

&#x20; box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-danger-500) 20%, transparent);

}



.field--error .label {

&#x20; color: var(--color-danger-700);

}



/\* Shake animation for invalid submit \*/

.field--error.shake {

&#x20; animation: field-shake 0.4s var(--ease-out);

}



@keyframes field-shake {

&#x20; 0%, 100% { translate: 0; }

&#x20; 20%       { translate: -6px; }

&#x20; 40%       { translate: 6px; }

&#x20; 60%       { translate: -4px; }

&#x20; 80%       { translate: 4px; }

}



/\* ─── Error message ─── \*/

.error-message {

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; gap: 0.375rem;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-danger-600);

&#x20; margin-block-start: var(--space-1);

&#x20; animation: error-appear 0.2s var(--ease-out);

}



@keyframes error-appear {

&#x20; from { opacity: 0; translate: 0 -4px; }

&#x20; to   { opacity: 1; translate: 0 0; }

}



/\* ─── 404 / Error page ─── \*/

.error-page {

&#x20; min-height: 100dvh;

&#x20; display: grid;

&#x20; place-items: center;

&#x20; padding: var(--space-8);

&#x20; text-align: center;

}



.error-page\_\_code {

&#x20; font-size: clamp(4rem, 15vw, 12rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; line-height: 1;

&#x20; background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-700));

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

&#x20; user-select: none;

&#x20; letter-spacing: -0.05em;

}



/\* Glitch effect for error code \*/

.error-page\_\_code--glitch {

&#x20; position: relative;

}



.error-page\_\_code--glitch::before,

.error-page\_\_code--glitch::after {

&#x20; content: attr(data-text);

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: inherit;

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

}



.error-page\_\_code--glitch::before {

&#x20; animation: glitch-1 0.3s infinite;

&#x20; clip-path: polygon(0 0, 100% 0, 100% 35%, 0 35%);

}



.error-page\_\_code--glitch::after {

&#x20; animation: glitch-2 0.3s infinite;

&#x20; clip-path: polygon(0 65%, 100% 65%, 100% 100%, 0 100%);

}



@keyframes glitch-1 {

&#x20; 0%, 100% { translate: 0; }

&#x20; 20%  { translate: -3px 0; filter: hue-rotate(90deg); }

&#x20; 40%  { translate: 3px 0; }

&#x20; 60%  { translate: -1px 0; filter: hue-rotate(-90deg); }

&#x20; 80%  { translate: 1px 0; }

}



@keyframes glitch-2 {

&#x20; 0%, 100% { translate: 0; }

&#x20; 30%  { translate: 3px 0; filter: hue-rotate(90deg); }

&#x20; 50%  { translate: -3px 0; }

&#x20; 70%  { translate: 2px 0; filter: hue-rotate(-90deg); }

&#x20; 90%  { translate: -1px 0; }

}

```



\---



\## 82. CSS SELECTOR PERFORMANCE



\### 82.1 Selector Efficiency



```css

/\*\*

&#x20;\* CSS selectors are matched RIGHT to LEFT.

&#x20;\* Browser first finds all elements matching the rightmost part,

&#x20;\* then walks up the DOM checking parents.

&#x20;\*

&#x20;\* Performance order (fastest → slowest):

&#x20;\*

&#x20;\* 1. ID:           #id               (1 element, instant)

&#x20;\* 2. Class:        .class            (indexed by browser)

&#x20;\* 3. Type:         div               (indexed by browser)

&#x20;\* 4. Adjacent:     .a + .b

&#x20;\* 5. Child:        .a > .b

&#x20;\* 6. Descendant:   .a .b             (can be slow for large DOMs)

&#x20;\* 7. Universal:    \*                 (matches everything)

&#x20;\* 8. Attribute:    \[attr="value"]    (not indexed)

&#x20;\* 9. Pseudo:       :nth-child()      (recalculated on DOM changes)

&#x20;\* 10. :has()       :has(.child)      (expensive — triggers parent check)

&#x20;\*/



/\* ─── Anti-patterns ─── \*/



/\* ❌ Over-qualified — redundant type \*/

div.container { }        /\* .container is enough \*/

ul.list li.item { }     /\* .item is enough \*/



/\* ❌ Overly deep descendant \*/

.header .nav .nav-list .nav-item .nav-link { }

/\* ✅ Just: \*/

.nav-link { }



/\* ❌ Inefficient universal with descendant \*/

.container \* { box-sizing: border-box; }

/\* ✅ One rule at root \*/

\*, \*::before, \*::after { box-sizing: border-box; }



/\* ❌ Expensive :nth-child in large lists \*/

.list-item:nth-child(odd) { }   /\* recalculated on every DOM change \*/

/\* ✅ Add class in JS for large dynamic lists \*/

.list-item.odd { }



/\* ─── :has() performance notes ─── \*/

/\* :has() triggers a "subject" invalidation —

&#x20;  browser must check parents when DOM changes.

&#x20;  Use sparingly on frequently-updating content. \*/



/\* ✅ OK: on static content \*/

.card:has(img) { padding: 0; }



/\* ⚠️ Expensive: on frequently updating elements \*/

body:has(.input:focus) { }  /\* triggers full-page recalc on every focus \*/

/\* ✅ Better: scope to nearest container \*/

.form:has(.input:focus) { }

```



\---



\## 83. BROWSER-SPECIFIC CSS



\### 83.1 Browser Detection via CSS



```css

/\* ─── Feature detection (preferred) ─── \*/

@supports (display: grid) { }

@supports (backdrop-filter: blur(1px)) { }

@supports (-webkit-backdrop-filter: blur(1px)) {

&#x20; /\* Safari specific \*/

&#x20; .glass { -webkit-backdrop-filter: blur(10px); }

}



/\* ─── Browser-specific hacks (last resort) ─── \*/



/\* Safari only \*/

@supports (-webkit-appearance: none) and (not (overflow: -webkit-marquee)) and (not (-ms-ime-align: auto)) {

&#x20; .safari-fix { -webkit-transform: translateZ(0); }

}



/\* Chrome / Edge (not Firefox, not Safari) \*/

@supports (-webkit-appearance: none) and (not (gap: 0)) {

&#x20; .chrome-fix { }

}



/\* Firefox only \*/

@-moz-document url-prefix() {

&#x20; .firefox-fix { scrollbar-width: thin; }

}



/\* ─── Vendor prefixes still needed ─── \*/



/\* WebKit scrollbar (Chrome, Edge, Safari) \*/

::-webkit-scrollbar { width: 8px; }

::-webkit-scrollbar-track { background: transparent; }

::-webkit-scrollbar-thumb {

&#x20; background: var(--color-border-strong);

&#x20; border-radius: 4px;

}



/\* Backdrop filter \*/

.frosted {

&#x20; -webkit-backdrop-filter: blur(12px);

&#x20; backdrop-filter: blur(12px);

}



/\* Font smoothing \*/

body {

&#x20; -webkit-font-smoothing: antialiased;    /\* macOS/iOS WebKit \*/

&#x20; -moz-osx-font-smoothing: grayscale;    /\* macOS Firefox \*/

}



/\* Text stroke \*/

.outlined {

&#x20; -webkit-text-stroke: 1px currentColor;

&#x20; text-stroke: 1px currentColor;

}



/\* ─── iOS-specific ─── \*/

/\* Prevent zoom on input focus (iOS Safari zooms when font-size < 16px) \*/

input, select, textarea {

&#x20; font-size: max(16px, 1rem);

}



/\* Fix for iOS momentum scroll in overflow containers \*/

.scroll-ios {

&#x20; overflow-y: scroll;

&#x20; -webkit-overflow-scrolling: touch;

}



/\* Disable iOS callout menu on long-press \*/

.no-callout {

&#x20; -webkit-touch-callout: none;

}



/\* ─── Windows High Contrast Mode ─── \*/

@media (forced-colors: active) {

&#x20; .btn {

&#x20;   border: 2px solid ButtonText;

&#x20;   background: ButtonFace;

&#x20;   color: ButtonText;

&#x20; }

&#x20; 

&#x20; .btn:hover {

&#x20;   border-color: Highlight;

&#x20;   color: Highlight;

&#x20; }

&#x20; 

&#x20; .card {

&#x20;   border: 1px solid CanvasText;

&#x20; }

&#x20; 

&#x20; /\* Preserve custom colors for decorative elements \*/

&#x20; .icon-decorative {

&#x20;   forced-color-adjust: none;

&#x20; }

}



/\* ─── Print-specific browser resets ─── \*/

@media print {

&#x20; /\* Chrome adds URLs to links \*/

&#x20; a::after { content: none !important; }

&#x20; 

&#x20; /\* Firefox adds "Printed by..." \*/

&#x20; /\* Can't be controlled via CSS \*/

}

```



\---



\## 84. CSS LOGICAL PROPERTIES — COMPLETE REFERENCE TABLE



```css

/\*

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

║  Text \& Other                                                         ║

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

\*/

```



\---



\## 85. CSS CUSTOM PROPERTIES — ADVANCED PATTERNS



\### 85.1 Space-toggle Technique



```css

/\*

&#x20;\* The "Space Toggle" technique — CSS variables as boolean switches.

&#x20;\* 0 = falsy (empty value = turns off property)

&#x20;\* initial = truthy (valid value = turns on property)

&#x20;\*

&#x20;\* Author: Lea Verou / Ana Tudor

&#x20;\*/



.element {

&#x20; --is-dark: ;          /\* initial (truthy) \*/

&#x20; --is-light: initial;  /\* initial (truthy) \*/



&#x20; /\* Space toggle usage \*/

&#x20; background:

&#x20;   var(--is-dark, black)

&#x20;   var(--is-light, white);

&#x20; /\* Only ONE will be valid — the other's var() resolves to empty \*/

}



/\* Flip the switch \*/

.dark-context {

&#x20; --is-dark: initial;

&#x20; --is-light: ;

}



/\* ─── Practical example: component theming ─── \*/

.alert {

&#x20; --success: ;

&#x20; --warning: ;

&#x20; --error:   ;



&#x20; background: var(--success, var(--color-success-100))

&#x20;             var(--warning, var(--color-warning-100))

&#x20;             var(--error,   var(--color-danger-100));

&#x20; color:      var(--success, var(--color-success-900))

&#x20;             var(--warning, var(--color-warning-900))

&#x20;             var(--error,   var(--color-danger-900));

}



.alert--success { --success: initial; }

.alert--warning { --warning: initial; }

.alert--error   { --error:   initial; }

```



\### 85.2 CSS Variable Tricks



```css

/\* ─── Responsive props without media queries ─── \*/

:root {

&#x20; /\* Clamp-based responsive spacing \*/

&#x20; --space-responsive: clamp(

&#x20;   var(--space-4),

&#x20;   5vw,

&#x20;   var(--space-12)

&#x20; );

}



/\* ─── Inherited token override pattern ─── \*/

/\* Parent sets context \*/

.theme-compact {

&#x20; --card-padding: var(--space-4);

&#x20; --card-gap: var(--space-2);

&#x20; --font-scale: 0.9;

}



/\* Child reads context \*/

.card {

&#x20; padding: var(--card-padding, var(--space-6));

&#x20; gap: var(--card-gap, var(--space-4));

&#x20; font-size: calc(var(--font-scale, 1) \* 1rem);

}



/\* ─── CSS-only dark mode toggle via variables ─── \*/

:root {

&#x20; --scheme: light;

&#x20; 

&#x20; /\* Light defaults \*/

&#x20; --bg: white;

&#x20; --text: #111;

}



/\* Applied when JS sets data-theme \*/

\[data-theme="dark"] {

&#x20; --scheme: dark;

&#x20; --bg: #111;

&#x20; --text: white;

}



/\* Smooth transition between themes \*/

\*, \*::before, \*::after {

&#x20; transition:

&#x20;   background-color 0.3s,

&#x20;   border-color 0.3s,

&#x20;   color 0.3s;

}



/\* Except interactive elements (feels laggy) \*/

button, input, a {

&#x20; transition: none;

}



/\* ─── Math with custom properties ─── \*/

:root {

&#x20; --cols: 3;

&#x20; --gap: 1rem;

&#x20; --col-width: calc((100% - var(--gap) \* (var(--cols) - 1)) / var(--cols));

}



/\* ─── CSS custom property as type guard ─── \*/

@property --opacity {

&#x20; syntax: '<number>';

&#x20; initial-value: 1;

&#x20; inherits: false;

}



/\* Now invalid values silently fall back to initial: \*/

.element {

&#x20; --opacity: "not a number";  /\* Falls back to 1 \*/

&#x20; opacity: var(--opacity);    /\* = 1, not broken \*/

}

```



\---



\## 86. REAL-WORLD PAGE PATTERNS



\### 86.1 Dashboard Layout



```css

/\* ─── App Shell ─── \*/

.app-shell {

&#x20; display: grid;

&#x20; grid-template-areas:

&#x20;   "sidebar header"

&#x20;   "sidebar main";

&#x20; grid-template-columns: var(--sidebar-width, 240px) 1fr;

&#x20; grid-template-rows: var(--header-height, 60px) 1fr;

&#x20; min-height: 100dvh;

}



.app-header  { grid-area: header; }

.app-sidebar { grid-area: sidebar; }

.app-main    { grid-area: main; overflow-y: auto; }



/\* Collapsible sidebar \*/

.app-shell\[data-sidebar="collapsed"] {

&#x20; --sidebar-width: 64px;

}



.app-sidebar {

&#x20; transition: width var(--duration-slow) var(--ease-out);

&#x20; width: var(--sidebar-width, 240px);

&#x20; overflow: hidden;

}



/\* Sidebar nav item \*/

.sidebar-nav-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: 0.625rem 0.75rem;

&#x20; border-radius: var(--radius-md);

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: none;

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; white-space: nowrap;

&#x20; overflow: hidden;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}



.sidebar-nav-item:hover {

&#x20; background: var(--color-bg-subtle);

&#x20; color: var(--color-text);

}



.sidebar-nav-item\[aria-current="page"] {

&#x20; background: color-mix(in srgb, var(--color-accent) 12%, transparent);

&#x20; color: var(--color-accent);

}



.sidebar-nav-item .icon {

&#x20; flex-shrink: 0;

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

}



/\* Hide label when collapsed \*/

.app-shell\[data-sidebar="collapsed"] .sidebar-nav-item .label {

&#x20; opacity: 0;

&#x20; width: 0;

&#x20; pointer-events: none;

}



/\* ─── Dashboard grid ─── \*/

.dashboard-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(12, 1fr);

&#x20; gap: var(--space-6);

&#x20; padding: var(--space-6);

&#x20; align-items: start;

}



/\* Widget sizes \*/

.widget { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: var(--space-5); }

.widget--full   { grid-column: 1 / -1; }

.widget--half   { grid-column: span 6; }

.widget--third  { grid-column: span 4; }

.widget--quarter { grid-column: span 3; }



@media (max-width: 768px) {

&#x20; .app-shell {

&#x20;   grid-template-areas: "header" "main";

&#x20;   grid-template-columns: 1fr;

&#x20;   grid-template-rows: var(--header-height, 60px) 1fr;

&#x20; }

&#x20; .app-sidebar {

&#x20;   position: fixed;

&#x20;   inset-block: 0;

&#x20;   inset-inline-start: 0;

&#x20;   z-index: var(--z-fixed);

&#x20;   translate: -100%;

&#x20;   transition: translate var(--duration-slow) var(--ease-out);

&#x20; }

&#x20; .app-sidebar\[data-open="true"] {

&#x20;   translate: 0;

&#x20; }

&#x20; .widget--half,

&#x20; .widget--third,

&#x20; .widget--quarter { grid-column: 1 / -1; }

}

```



\### 86.2 Landing Page Patterns



```css

/\* ─── Hero section ─── \*/

.hero {

&#x20; position: relative;

&#x20; min-height: 100dvh;

&#x20; display: grid;

&#x20; place-items: center;

&#x20; text-align: center;

&#x20; overflow: hidden;

&#x20; padding: var(--space-8);

}



.hero\_\_background {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; z-index: 0;

&#x20; background: var(--color-bg);

}



/\* Animated gradient background \*/

.hero\_\_gradient {

&#x20; position: absolute;

&#x20; inset: -50%;

&#x20; background:

&#x20;   radial-gradient(ellipse at 30% 40%, var(--color-brand-500) 0%, transparent 50%),

&#x20;   radial-gradient(ellipse at 70% 60%, var(--color-brand-300) 0%, transparent 50%);

&#x20; opacity: 0.15;

&#x20; animation: hero-drift 10s ease-in-out infinite alternate;

&#x20; filter: blur(60px);

}



@keyframes hero-drift {

&#x20; from { translate: -5% -5%; rotate: 0deg; }

&#x20; to   { translate: 5% 5%; rotate: 5deg; }

}



.hero\_\_content {

&#x20; position: relative;

&#x20; z-index: 1;

&#x20; max-width: 60rem;

}



.hero\_\_eyebrow {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.375rem 0.875rem;

&#x20; background: color-mix(in srgb, var(--color-accent) 10%, transparent);

&#x20; border: 1px solid color-mix(in srgb, var(--color-accent) 25%, transparent);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; color: var(--color-accent);

&#x20; margin-block-end: var(--space-6);

&#x20; animation: eyebrow-in 0.5s var(--ease-out) 0.2s both;

}



@keyframes eyebrow-in {

&#x20; from { opacity: 0; translate: 0 -8px; }

}



.hero\_\_title {

&#x20; font-size: clamp(2.5rem, 6vw + 1rem, 6rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; line-height: 1.05;

&#x20; letter-spacing: -0.03em;

&#x20; text-wrap: balance;

&#x20; margin-block-end: var(--space-6);

&#x20; animation: title-in 0.6s var(--ease-out) 0.35s both;

}



@keyframes title-in {

&#x20; from { opacity: 0; translate: 0 20px; }

}



.hero\_\_subtitle {

&#x20; font-size: clamp(1.125rem, 2vw + 0.5rem, 1.5rem);

&#x20; color: var(--color-text-muted);

&#x20; max-width: 50ch;

&#x20; margin-inline: auto;

&#x20; margin-block-end: var(--space-8);

&#x20; text-wrap: pretty;

&#x20; animation: subtitle-in 0.6s var(--ease-out) 0.5s both;

}



@keyframes subtitle-in {

&#x20; from { opacity: 0; translate: 0 15px; }

}



.hero\_\_actions {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; justify-content: center;

&#x20; flex-wrap: wrap;

&#x20; animation: actions-in 0.6s var(--ease-out) 0.65s both;

}



@keyframes actions-in {

&#x20; from { opacity: 0; translate: 0 10px; }

}



/\* ─── Feature grid section ─── \*/

.features {

&#x20; padding-block: clamp(4rem, 10vw, 10rem);

&#x20; padding-inline: clamp(1rem, 5vw, 4rem);

}



.features\_\_header {

&#x20; text-align: center;

&#x20; max-width: 45ch;

&#x20; margin-inline: auto;

&#x20; margin-block-end: clamp(3rem, 6vw, 5rem);

}



.features\_\_grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));

&#x20; gap: var(--space-6);

}



.feature-card {

&#x20; padding: var(--space-6);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; background: var(--color-surface);

&#x20; transition:

&#x20;   box-shadow var(--duration-normal) var(--ease-out),

&#x20;   translate  var(--duration-normal) var(--ease-out),

&#x20;   border-color var(--duration-fast);

&#x20; position: relative;

&#x20; overflow: hidden;

}



.feature-card::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: radial-gradient(

&#x20;   circle at var(--mouse-x, 50%) var(--mouse-y, 50%),

&#x20;   color-mix(in srgb, var(--color-accent) 8%, transparent),

&#x20;   transparent 70%

&#x20; );

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-normal);

}



.feature-card:hover {

&#x20; box-shadow: var(--shadow-lg);

&#x20; translate: 0 -2px;

&#x20; border-color: var(--color-border-strong);

}



.feature-card:hover::before {

&#x20; opacity: 1;

}



.feature-icon {

&#x20; width: 3rem;

&#x20; height: 3rem;

&#x20; border-radius: var(--radius-xl);

&#x20; background: color-mix(in srgb, var(--color-accent) 12%, transparent);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-accent);

&#x20; margin-block-end: var(--space-4);

&#x20; font-size: 1.5rem;

}

```



\---



\## 87. CSS THEMING — COMPLETE SYSTEM



\### 87.1 Multi-theme Architecture



```css

/\* ─── Theme definition pattern ─── \*/



/\* Base — structural tokens (never theme-specific) \*/

:root {

&#x20; --font-sans: system-ui, sans-serif;

&#x20; --font-mono: 'Fira Code', monospace;

&#x20; --radius-md: 0.375rem;

&#x20; --radius-lg: 0.5rem;

&#x20; --radius-xl: 0.75rem;

&#x20; --radius-2xl: 1rem;

&#x20; --space-1: 0.25rem;

&#x20; --space-2: 0.5rem;

&#x20; --space-4: 1rem;

&#x20; --space-6: 1.5rem;

&#x20; --space-8: 2rem;

&#x20; 

&#x20; /\* Semantic (change per theme) \*/

&#x20; --bg-base:      white;

&#x20; --bg-subtle:    #f8f9fa;

&#x20; --bg-muted:     #e9ecef;

&#x20; --surface:      white;

&#x20; --border:       #dee2e6;

&#x20; --border-strong: #ced4da;

&#x20; --text:         #212529;

&#x20; --text-muted:   #6c757d;

&#x20; --text-subtle:  #adb5bd;

&#x20; --accent:       #3b82f6;

&#x20; --accent-hover: #2563eb;

&#x20; --accent-text:  white;

}



/\* ─── Theme: Dark ─── \*/

\[data-theme="dark"],

@media (prefers-color-scheme: dark) {

&#x20; :root:not(\[data-theme="light"]) {

&#x20;   --bg-base:      #0f172a;

&#x20;   --bg-subtle:    #1e293b;

&#x20;   --bg-muted:     #334155;

&#x20;   --surface:      #1e293b;

&#x20;   --border:       #334155;

&#x20;   --border-strong: #475569;

&#x20;   --text:         #f1f5f9;

&#x20;   --text-muted:   #94a3b8;

&#x20;   --text-subtle:  #64748b;

&#x20; }

}



/\* ─── Theme: Sepia ─── \*/

\[data-theme="sepia"] {

&#x20; --bg-base:    #f8f1e3;

&#x20; --bg-subtle:  #ede7d3;

&#x20; --surface:    #f8f1e3;

&#x20; --border:     #d4c9a8;

&#x20; --text:       #3d2b1f;

&#x20; --text-muted: #7a6551;

&#x20; --accent:     #8b5e3c;

}



/\* ─── Theme: High Contrast ─── \*/

\[data-theme="high-contrast"] {

&#x20; --bg-base:      black;

&#x20; --surface:      black;

&#x20; --border:       white;

&#x20; --text:         white;

&#x20; --text-muted:   #eeeeee;

&#x20; --accent:       yellow;

&#x20; --accent-text:  black;

}



/\* ─── Theme: Colorful ─── \*/

\[data-theme="purple"] {

&#x20; --accent:       #8b5cf6;

&#x20; --accent-hover: #7c3aed;

&#x20; --bg-subtle:    #faf5ff;

}

\[data-theme="green"] {

&#x20; --accent:       #10b981;

&#x20; --accent-hover: #059669;

&#x20; --bg-subtle:    #f0fdf4;

}

\[data-theme="rose"] {

&#x20; --accent:       #f43f5e;

&#x20; --accent-hover: #e11d48;

&#x20; --bg-subtle:    #fff1f2;

}



/\* ─── Theme switcher component ─── \*/

.theme-switcher {

&#x20; display: flex;

&#x20; gap: var(--space-2);

&#x20; align-items: center;

}



.theme-dot {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; border: 2px solid transparent;

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   scale var(--duration-fast) var(--ease-bounce),

&#x20;   border-color var(--duration-fast);

}



.theme-dot:hover { scale: 1.15; }

.theme-dot\[aria-pressed="true"] { border-color: var(--text); }



.theme-dot--light   { background: white; box-shadow: 0 0 0 1px #ddd; }

.theme-dot--dark    { background: #0f172a; }

.theme-dot--sepia   { background: #f8f1e3; box-shadow: 0 0 0 1px #d4c9a8; }

.theme-dot--purple  { background: #8b5cf6; }

.theme-dot--green   { background: #10b981; }

.theme-dot--rose    { background: #f43f5e; }

```



\---



\## 88. COMPLETE ANIMATION COOKBOOK



\### 88.1 Page Transitions



```css

/\* ─── Full page transition library ─── \*/



/\* Base state for page entering \*/

.page-enter {

&#x20; animation: var(--page-enter, page-fade-in) var(--duration-slow) var(--ease-out) both;

}

.page-leave {

&#x20; animation: var(--page-leave, page-fade-out) var(--duration-slow) var(--ease-in) both;

}



/\* Fade \*/

@keyframes page-fade-in   { from { opacity: 0; } }

@keyframes page-fade-out  { to   { opacity: 0; } }



/\* Slide from right \*/

@keyframes page-slide-in-right  { from { translate: 100% 0; opacity: 0; } }

@keyframes page-slide-out-left  { to   { translate: -30% 0; opacity: 0; } }



/\* Slide from left \*/

@keyframes page-slide-in-left   { from { translate: -100% 0; opacity: 0; } }

@keyframes page-slide-out-right { to   { translate: 30% 0; opacity: 0; } }



/\* Scale \*/

@keyframes page-scale-in   { from { scale: 1.05; opacity: 0; } }

@keyframes page-scale-out  { to   { scale: 0.95; opacity: 0; } }



/\* Flip \*/

@keyframes page-flip-in  { from { rotateY: -10deg; opacity: 0; } }

@keyframes page-flip-out { to   { rotateY: 10deg; opacity: 0; } }



/\* Apply theme based on direction \*/

\[data-direction="forward"] {

&#x20; --page-enter: page-slide-in-right;

&#x20; --page-leave: page-slide-out-left;

}

\[data-direction="backward"] {

&#x20; --page-enter: page-slide-in-left;

&#x20; --page-leave: page-slide-out-right;

}

```



\### 88.2 Loading Animations



```css

/\* ─── Complete loading library ─── \*/



/\* 1. Classic spinner \*/

@keyframes spin { to { rotate: 360deg; } }

.loader-spin {

&#x20; width: 24px; height: 24px;

&#x20; border: 2px solid var(--color-bg-muted);

&#x20; border-top-color: var(--color-accent);

&#x20; border-radius: 50%;

&#x20; animation: spin 0.7s linear infinite;

}



/\* 2. Dots pulse \*/

.loader-dots {

&#x20; display: flex; gap: 4px; align-items: center;

}

.loader-dots span {

&#x20; width: 8px; height: 8px;

&#x20; background: var(--color-accent);

&#x20; border-radius: 50%;

&#x20; animation: dots-bounce 1.2s ease-in-out infinite;

}

.loader-dots span:nth-child(2) { animation-delay: 0.2s; }

.loader-dots span:nth-child(3) { animation-delay: 0.4s; }



@keyframes dots-bounce {

&#x20; 0%, 80%, 100% { scale: 0.6; opacity: 0.4; }

&#x20; 40%           { scale: 1;   opacity: 1; }

}



/\* 3. Progress bar \*/

.loader-bar {

&#x20; width: 100%; height: 3px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

&#x20; position: relative;

}

.loader-bar::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-block: 0;

&#x20; width: 40%;

&#x20; background: var(--color-accent);

&#x20; border-radius: inherit;

&#x20; animation: bar-slide 1.5s ease-in-out infinite;

}

@keyframes bar-slide {

&#x20; from { inset-inline-start: -40%; }

&#x20; to   { inset-inline-start: 100%; }

}



/\* 4. Skeleton shimmer \*/

@keyframes shimmer {

&#x20; from { background-position: -200% 0; }

&#x20; to   { background-position: 200% 0; }

}

.loader-skeleton {

&#x20; background: linear-gradient(

&#x20;   90deg,

&#x20;   var(--color-bg-subtle) 25%,

&#x20;   var(--color-bg-muted) 50%,

&#x20;   var(--color-bg-subtle) 75%

&#x20; );

&#x20; background-size: 200% 100%;

&#x20; animation: shimmer 1.5s ease-in-out infinite;

&#x20; border-radius: var(--radius-md);

}



/\* 5. Circular indeterminate \*/

.loader-circle {

&#x20; width: 36px; height: 36px;

&#x20; animation: rotate 2s linear infinite;

}

.loader-circle circle {

&#x20; stroke: var(--color-accent);

&#x20; stroke-linecap: round;

&#x20; animation: dash 1.5s ease-in-out infinite;

}

@keyframes rotate { to { rotate: 360deg; } }

@keyframes dash {

&#x20; 0%   { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }

&#x20; 50%  { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }

&#x20; 100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }

}



/\* 6. Typing indicator \*/

.loader-typing {

&#x20; display: inline-flex;

&#x20; gap: 4px;

&#x20; align-items: center;

&#x20; padding: 0.625rem 0.875rem;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

}

.loader-typing span {

&#x20; width: 6px; height: 6px;

&#x20; background: var(--color-text-muted);

&#x20; border-radius: 50%;

&#x20; animation: typing-dot 1.4s ease-in-out infinite;

}

.loader-typing span:nth-child(2) { animation-delay: 0.2s; }

.loader-typing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing-dot {

&#x20; 0%, 60%, 100% { translate: 0; opacity: 0.4; }

&#x20; 30%           { translate: 0 -4px; opacity: 1; }

}



/\* 7. Page progress (top bar) \*/

.page-progress {

&#x20; position: fixed;

&#x20; top: 0; left: 0;

&#x20; height: 3px;

&#x20; background: var(--color-accent);

&#x20; z-index: var(--z-top);

&#x20; border-radius: 0 var(--radius-full) var(--radius-full) 0;

&#x20; width: var(--progress, 0%);

&#x20; transition: width 0.2s var(--ease-out);

&#x20; box-shadow: 0 0 8px var(--color-accent);

}

```



\---



\## 89. ACCESSIBILITY DEEP DIVE



\### 89.1 WCAG 2.1 / 2.2 CSS Requirements



```css

/\* ─── 1.1.1 Non-text Content — provide alt text (HTML, not CSS) ─── \*/

/\* Decorative images via CSS don't need alt \*/

.decorative { background-image: url('pattern.svg'); }



/\* ─── 1.4.1 Use of Color — never use color alone ─── \*/

/\* ❌ Only color to indicate required \*/

.required-field { border-color: red; }



/\* ✅ Color + icon + text \*/

.required-field {

&#x20; border-color: var(--color-danger-500);

}

.required-field::after {

&#x20; content: ' \*';

&#x20; color: var(--color-danger-500);

&#x20; font-weight: bold;

}



/\* ─── 1.4.3 Contrast Minimum — 4.5:1 normal, 3:1 large ─── \*/

/\* Large text = 18pt (24px) or 14pt (18.67px) bold \*/



/\* ─── 1.4.4 Resize Text — don't prevent zoom ─── \*/

/\* ✅ Use em/rem, not px for text \*/

/\* ✅ Don't use maximum-scale=1 in viewport meta \*/



/\* ─── 1.4.10 Reflow — must work at 320px width ─── \*/

.component {

&#x20; max-width: 100%;

&#x20; overflow-wrap: break-word;

&#x20; /\* No fixed widths that cause horizontal scroll \*/

}



/\* ─── 1.4.11 Non-text Contrast — UI components 3:1 ─── \*/

input, button {

&#x20; border: 1px solid var(--color-border-strong); /\* must be 3:1 vs background \*/

}



/\* ─── 1.4.12 Text Spacing ─── \*/

/\* Users can set: line-height: 1.5×, letter-spacing: 0.12em,

&#x20;  word-spacing: 0.16em, paragraph spacing: 2×. Must not break. \*/

.text {

&#x20; /\* Don't use fixed height that clips at custom spacing \*/

&#x20; min-height: 1.5em;  /\* not height! \*/

&#x20; overflow: visible;  /\* not hidden \*/

}



/\* ─── 2.1.1 Keyboard — all functionality via keyboard ─── \*/

/\* All interactive elements must be natively focusable or have tabindex \*/

\[tabindex="0"] { cursor: pointer; }  /\* custom interactive \*/

\[tabindex="-1"] { }  /\* programmatically focusable, not in tab order \*/



/\* ─── 2.4.7 Focus Visible ─── \*/

:focus-visible {

&#x20; outline: 2px solid var(--color-accent);

&#x20; outline-offset: 2px;

&#x20; border-radius: 2px;

}

/\* Never: \*/

/\* :focus { outline: none; }  ← WCAG violation \*/



/\* ─── 2.5.3 Label in Name ─── \*/

/\* Button with icon only must have accessible name \*/

.icon-btn {

&#x20; /\* aria-label="Close" in HTML \*/

&#x20; /\* Visual label must match accessible name \*/

}



/\* ─── 2.5.8 Target Size (WCAG 2.2 AA) — minimum 24×24px ─── \*/

.interactive-target {

&#x20; min-width: 24px;

&#x20; min-height: 24px;

}

/\* Enhanced: 44×44px (WCAG AAA / Apple HIG) \*/

.interactive-enhanced {

&#x20; min-width: 44px;

&#x20; min-height: 44px;

}



/\* ─── 3.3.4 Error Suggestion ─── \*/

.field\_\_error {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.375rem;

&#x20; color: var(--color-danger-600);

&#x20; font-size: var(--font-size-sm);

&#x20; margin-top: var(--space-1);

&#x20; /\* Must be programmatically associated via aria-describedby \*/

}

```



\### 89.2 Focus Management Patterns



```css

/\* ─── Focus trap indicator ─── \*/

.focus-trap-active {

&#x20; position: relative;

}



.focus-trap-active::after {

&#x20; content: '';

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; outline: 3px solid var(--color-accent);

&#x20; outline-offset: -3px;

&#x20; pointer-events: none;

&#x20; z-index: var(--z-top);

}



/\* ─── Focus ring styles by component ─── \*/



/\* Links \*/

a:focus-visible {

&#x20; outline: 2px solid var(--color-accent);

&#x20; outline-offset: 3px;

&#x20; border-radius: 2px;

}



/\* Buttons \*/

.btn:focus-visible {

&#x20; outline: none;

&#x20; box-shadow:

&#x20;   0 0 0 2px var(--color-bg),

&#x20;   0 0 0 4px var(--color-accent);

}



/\* Inputs \*/

.input:focus-visible {

&#x20; border-color: var(--color-accent);

&#x20; box-shadow:

&#x20;   0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);

&#x20; outline: none;

}



/\* Cards (when clickable) \*/

.card-link:focus-visible {

&#x20; outline: 2px solid var(--color-accent);

&#x20; outline-offset: 4px;

&#x20; border-radius: calc(var(--radius-xl) + 4px);

}



/\* ─── Skip navigation ─── \*/

.skip-nav {

&#x20; position: absolute;

&#x20; top: -100%;

&#x20; left: 50%;

&#x20; translate: -50%;

&#x20; padding: 0.875rem 2rem;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-decoration: none;

&#x20; border-radius: 0 0 var(--radius-lg) var(--radius-lg);

&#x20; z-index: var(--z-top);

&#x20; transition: top var(--duration-fast);

&#x20; white-space: nowrap;

}



.skip-nav:focus {

&#x20; top: 0;

&#x20; outline: none;

&#x20; box-shadow: 0 4px 12px rgb(0 0 0 / 0.3);

}



/\* ─── Reduced motion full implementation ─── \*/

@media (prefers-reduced-motion: reduce) {

&#x20; /\* Remove ALL animations and transitions \*/

&#x20; \*,

&#x20; \*::before,

&#x20; \*::after {

&#x20;   animation-duration: 0.01ms !important;

&#x20;   animation-iteration-count: 1 !important;

&#x20;   transition-duration: 0.01ms !important;

&#x20;   transition-delay: 0ms !important;

&#x20;   scroll-behavior: auto !important;

&#x20; }



&#x20; /\* Remove parallax \*/

&#x20; .parallax { transform: none !important; }



&#x20; /\* Keep useful state changes (no duration = instant) \*/

&#x20; :focus-visible { outline-offset: 2px; }  /\* instant is fine \*/

}



/\* ─── Prefers contrast ─── \*/

@media (prefers-contrast: more) {

&#x20; :root {

&#x20;   --color-border: var(--color-neutral-600);

&#x20;   --color-text-muted: var(--color-neutral-600);

&#x20;   --color-text-subtle: var(--color-neutral-500);

&#x20; }



&#x20; .btn {

&#x20;   border-width: 2px;

&#x20;   font-weight: var(--font-weight-bold);

&#x20; }



&#x20; input, select, textarea {

&#x20;   border-width: 2px;

&#x20; }

}



@media (prefers-contrast: less) {

&#x20; :root {

&#x20;   --shadow-md: 0 2px 4px rgb(0 0 0 / 0.06);

&#x20; }

}

```



\---



\## 90. FINAL QUICK REFERENCE



\### 90.1 CSS Reset — The Essential 2025 Version



```css

/\* ─── The Complete Modern Reset ─── \*/



/\* Box sizing \*/

\*, \*::before, \*::after {

&#x20; box-sizing: border-box;

}



/\* Remove defaults \*/

\* {

&#x20; margin: 0;

&#x20; padding: 0;

}



/\* Document \*/

html {

&#x20; font-size: 100%;

&#x20; -webkit-text-size-adjust: 100%;

&#x20; text-size-adjust: 100%;

&#x20; color-scheme: light dark;

&#x20; hanging-punctuation: first last;

&#x20; scroll-behavior: smooth;

}



@media (prefers-reduced-motion: reduce) {

&#x20; html { scroll-behavior: auto; }

&#x20; \*, \*::before, \*::after {

&#x20;   animation-duration: 0.01ms !important;

&#x20;   animation-iteration-count: 1 !important;

&#x20;   transition-duration: 0.01ms !important;

&#x20; }

}



/\* Body \*/

body {

&#x20; min-height: 100dvh;

&#x20; font-family: var(--font-sans, system-ui, sans-serif);

&#x20; line-height: 1.5;

&#x20; -webkit-font-smoothing: antialiased;

&#x20; -moz-osx-font-smoothing: grayscale;

}



/\* Media \*/

img, picture, video, canvas, svg {

&#x20; display: block;

&#x20; max-width: 100%;

}

img, video { height: auto; }



/\* Typography \*/

h1, h2, h3, h4, h5, h6 {

&#x20; font-size: inherit;

&#x20; font-weight: inherit;

&#x20; overflow-wrap: break-word;

&#x20; text-wrap: balance;

}



p, li, figcaption {

&#x20; overflow-wrap: break-word;

&#x20; text-wrap: pretty;

}



/\* Forms \*/

input, button, textarea, select {

&#x20; font: inherit;

&#x20; color: inherit;

}

button { cursor: pointer; border: none; background: none; }

textarea { resize: vertical; }



/\* Lists \*/

:where(ul, ol):not(\[class]) { padding-inline-start: 1.5em; }



/\* Links \*/

a { color: inherit; text-decoration-skip-ink: auto; }



/\* Tables \*/

table { border-collapse: collapse; }



/\* Hidden \*/

\[hidden] { display: none !important; }



/\* Focus \*/

:focus { outline: none; }

:focus-visible {

&#x20; outline: 2px solid currentColor;

&#x20; outline-offset: 2px;

}



/\* Safe area \*/

body {

&#x20; padding-inline: env(safe-area-inset-left, 0) env(safe-area-inset-right, 0);

}

```



\### 90.2 The 10 CSS Rules That Matter Most



```css

/\*

&#x20;1. box-sizing: border-box on everything

&#x20;2. Use Custom Properties for all design tokens

&#x20;3. Prefer logical properties (margin-inline, padding-block)

&#x20;4. Use clamp() for fluid sizing

&#x20;5. CSS Grid for 2D, Flexbox for 1D

&#x20;6. :focus-visible for accessible focus rings

&#x20;7. Respect prefers-reduced-motion

&#x20;8. Use @layer to control specificity

&#x20;9. oklch() for perceptually uniform colors

&#x20;10. Never use !important except in utilities and reset

\*/



/\* The minimal setup that covers 90% of needs: \*/



\*, \*::before, \*::after { box-sizing: border-box; }

html { font-size: 100%; color-scheme: light dark; }

body { min-height: 100dvh; font-family: system-ui, sans-serif; line-height: 1.5; -webkit-font-smoothing: antialiased; }

img, video { display: block; max-width: 100%; height: auto; }

input, button, textarea, select { font: inherit; }

:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }

@media (prefers-reduced-motion: reduce) { \*, \*::before, \*::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }

```



\---



```

╔═══════════════════════════════════════════════════════════════════════╗

║                    COMPLETE CSS GUIDE — FINAL STATS                   ║

╠═══════════════════════════════════════════════════════════════════════╣

║                                                                       ║

║  PARTS:       I (Russian) + II (Russian) + III (English) + IV (Eng)  ║

║  CHAPTERS:    90 chapters                                             ║

║  LINES:       \~16,000+ lines of Markdown                              ║

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



\*End of Part IV. The complete 4-part CSS Reference Guide is now finished.\*

