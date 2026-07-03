\# PART VI — CSS: DEEP CUTS \& SPECIALTY PATTERNS



\---



\## 101. HOVER EFFECTS LIBRARY



\### 101.1 Image Hover Effects



```css

/\* ─── 1. Zoom + overlay ─── \*/

.hover-zoom { position: relative; overflow: hidden; }

.hover-zoom img { transition: scale 0.5s var(--ease-out); display: block; width: 100%; }

.hover-zoom:hover img { scale: 1.08; }

.hover-zoom .overlay {

&#x20; position: absolute; inset: 0;

&#x20; background: linear-gradient(to top, rgb(0 0 0 / 0.7) 0%, transparent 60%);

&#x20; opacity: 0; transition: opacity 0.4s;

&#x20; display: flex; align-items: flex-end; padding: var(--space-4);

&#x20; color: white;

}

.hover-zoom:hover .overlay { opacity: 1; }



/\* ─── 2. Slide reveal ─── \*/

.hover-slide { position: relative; overflow: hidden; }

.hover-slide img { display: block; width: 100%; }

.hover-slide .caption {

&#x20; position: absolute; inset: 0;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; display: flex; flex-direction: column;

&#x20; align-items: center; justify-content: center;

&#x20; translate: 0 100%;

&#x20; transition: translate 0.4s var(--ease-out);

}

.hover-slide:hover .caption { translate: 0 0; }



/\* ─── 3. Grayscale → color ─── \*/

.hover-color img {

&#x20; filter: grayscale(100%) contrast(1.1);

&#x20; transition: filter 0.5s var(--ease-out);

}

.hover-color:hover img { filter: grayscale(0%); }



/\* ─── 4. Blur reveal ─── \*/

.hover-blur img {

&#x20; filter: blur(4px) brightness(0.7);

&#x20; scale: 1.05;

&#x20; transition: filter 0.4s, scale 0.4s;

}

.hover-blur:hover img { filter: blur(0) brightness(1); scale: 1; }



/\* ─── 5. Flip card ─── \*/

.hover-flip { perspective: 800px; }

.hover-flip\_\_inner {

&#x20; transform-style: preserve-3d;

&#x20; transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);

&#x20; position: relative;

}

.hover-flip:hover .hover-flip\_\_inner { transform: rotateY(180deg); }

.hover-flip\_\_front, .hover-flip\_\_back {

&#x20; backface-visibility: hidden;

}

.hover-flip\_\_back {

&#x20; position: absolute; inset: 0;

&#x20; transform: rotateY(180deg);

}



/\* ─── 6. Pan effect (image larger than container) ─── \*/

.hover-pan {

&#x20; overflow: hidden;

&#x20; cursor: crosshair;

}

.hover-pan img {

&#x20; width: 110%;

&#x20; max-width: none;

&#x20; translate: -5% 0;

&#x20; transition: translate 0.3s var(--ease-out);

}

/\* JS: on mousemove → update translate based on cursor position \*/

.hover-pan:hover img {

&#x20; translate: calc(var(--px, 0) \* -10%) calc(var(--py, 0) \* -10%);

}

```



\### 101.2 Button Hover Effects



```css

/\* ─── 1. Fill from left ─── \*/

.btn-fill-left {

&#x20; position: relative; overflow: hidden;

&#x20; background: transparent;

&#x20; border: 2px solid var(--color-accent);

&#x20; color: var(--color-accent);

&#x20; z-index: 0;

}

.btn-fill-left::before {

&#x20; content: '';

&#x20; position: absolute; inset: 0;

&#x20; background: var(--color-accent);

&#x20; transform: scaleX(0);

&#x20; transform-origin: left;

&#x20; transition: transform 0.3s var(--ease-out);

&#x20; z-index: -1;

}

.btn-fill-left:hover::before { transform: scaleX(1); }

.btn-fill-left:hover { color: white; }



/\* ─── 2. Sheen / shimmer ─── \*/

.btn-sheen {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; overflow: hidden;

&#x20; position: relative;

}

.btn-sheen::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 0; left: -100%;

&#x20; width: 60%;

&#x20; height: 100%;

&#x20; background: linear-gradient(

&#x20;   to right,

&#x20;   transparent 0%,

&#x20;   rgba(255 255 255 / 0.3) 50%,

&#x20;   transparent 100%

&#x20; );

&#x20; skewX(-20deg);

&#x20; transition: left 0.6s var(--ease-out);

}

.btn-sheen:hover::after { left: 140%; }



/\* ─── 3. Neon pulse ─── \*/

.btn-neon {

&#x20; background: transparent;

&#x20; border: 2px solid var(--color-accent);

&#x20; color: var(--color-accent);

&#x20; transition: box-shadow 0.3s, background 0.3s, color 0.3s;

}

.btn-neon:hover {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; box-shadow:

&#x20;   0 0 6px var(--color-accent),

&#x20;   0 0 20px var(--color-accent),

&#x20;   0 0 40px var(--color-accent);

}



/\* ─── 4. 3D push ─── \*/

.btn-3d {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; box-shadow:

&#x20;   0 6px 0 var(--color-accent-hover),

&#x20;   0 8px 6px rgba(0 0 0 / 0.3);

&#x20; transition:

&#x20;   box-shadow 0.1s,

&#x20;   translate 0.1s;

}

.btn-3d:hover { translate: 0 2px; box-shadow: 0 4px 0 var(--color-accent-hover), 0 5px 4px rgba(0 0 0 / 0.2); }

.btn-3d:active { translate: 0 6px; box-shadow: 0 0 0 var(--color-accent-hover); }



/\* ─── 5. Magnetic (via CSS vars from JS) ─── \*/

.btn-magnetic {

&#x20; transition: translate 0.15s var(--ease-out);

&#x20; translate: calc(var(--mx, 0) \* 0.4) calc(var(--my, 0) \* 0.4);

}



/\* ─── 6. Typewriter CTA ─── \*/

.btn-typewriter {

&#x20; overflow: hidden;

&#x20; white-space: nowrap;

}

.btn-typewriter .label {

&#x20; display: inline-block;

&#x20; max-width: 0;

&#x20; overflow: hidden;

&#x20; transition: max-width 0.4s var(--ease-out);

&#x20; vertical-align: bottom;

}

.btn-typewriter:hover .label { max-width: 10em; }

```



\### 101.3 Text Hover Effects



```css

/\* ─── 1. Underline draw ─── \*/

.text-underline-draw {

&#x20; position: relative;

&#x20; text-decoration: none;

&#x20; display: inline-block;

}

.text-underline-draw::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-inline: 0;

&#x20; bottom: -2px;

&#x20; height: 2px;

&#x20; background: currentColor;

&#x20; scale: 0 1;

&#x20; transform-origin: right;

&#x20; transition: scale 0.3s var(--ease-out), transform-origin 0s 0.3s;

}

.text-underline-draw:hover::after {

&#x20; scale: 1 1;

&#x20; transform-origin: left;

&#x20; transition: scale 0.3s var(--ease-out);

}



/\* ─── 2. Character split color ─── \*/

.text-split-color {

&#x20; background: linear-gradient(

&#x20;   to right,

&#x20;   var(--color-accent) 50%,

&#x20;   var(--color-text) 50%

&#x20; );

&#x20; background-size: 200% 100%;

&#x20; background-position: 100%;

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

&#x20; transition: background-position 0.5s var(--ease-out);

}

.text-split-color:hover { background-position: 0%; }



/\* ─── 3. Glitch text ─── \*/

.text-glitch {

&#x20; position: relative;

&#x20; color: var(--color-text);

}

.text-glitch::before,

.text-glitch::after {

&#x20; content: attr(data-text);

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; opacity: 0;

}

.text-glitch:hover::before {

&#x20; opacity: 0.8;

&#x20; color: oklch(0.7 0.3 250);

&#x20; clip-path: polygon(0 0, 100% 0, 100% 40%, 0 40%);

&#x20; animation: glitch-before 0.4s steps(2) infinite;

}

.text-glitch:hover::after {

&#x20; opacity: 0.8;

&#x20; color: oklch(0.7 0.3 10);

&#x20; clip-path: polygon(0 60%, 100% 60%, 100% 100%, 0 100%);

&#x20; animation: glitch-after 0.4s steps(2) infinite;

}

@keyframes glitch-before { 0%,100% { translate: -2px 0; } 50% { translate: 2px 0; } }

@keyframes glitch-after  { 0%,100% { translate: 2px 0; } 50% { translate: -2px 0; } }



/\* ─── 4. Letter spacing expand ─── \*/

.text-spacing {

&#x20; letter-spacing: normal;

&#x20; transition: letter-spacing 0.3s var(--ease-out);

}

.text-spacing:hover { letter-spacing: 0.15em; }



/\* ─── 5. Weight pulse (variable font) ─── \*/

.text-weight {

&#x20; font-variation-settings: 'wght' 400;

&#x20; transition: font-variation-settings 0.3s;

}

.text-weight:hover { font-variation-settings: 'wght' 800; }

```



\---



\## 102. BORDER ANIMATIONS



```css

/\* ─── 1. Rotating gradient border ─── \*/

@property --border-angle {

&#x20; syntax: '<angle>';

&#x20; initial-value: 0deg;

&#x20; inherits: false;

}



.border-spinning {

&#x20; position: relative;

&#x20; border-radius: var(--radius-xl);

&#x20; padding: 2px;

&#x20; background: conic-gradient(

&#x20;   from var(--border-angle),

&#x20;   var(--color-brand-500) 0%,

&#x20;   var(--color-brand-300) 25%,

&#x20;   var(--color-brand-500) 50%,

&#x20;   var(--color-brand-700) 75%,

&#x20;   var(--color-brand-500) 100%

&#x20; );

&#x20; animation: border-spin 3s linear infinite;

}



@keyframes border-spin {

&#x20; to { --border-angle: 360deg; }

}



.border-spinning\_\_inner {

&#x20; background: var(--color-surface);

&#x20; border-radius: calc(var(--radius-xl) - 2px);

&#x20; padding: var(--space-4);

}



/\* ─── 2. Draw border on hover ─── \*/

.border-draw {

&#x20; position: relative;

}



.border-draw::before,

.border-draw::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; border-radius: inherit;

}



.border-draw::before {

&#x20; border-top: 2px solid var(--color-accent);

&#x20; border-right: 2px solid var(--color-accent);

&#x20; scale: 0 1;

&#x20; transform-origin: top right;

&#x20; transition: scale 0.3s var(--ease-out);

}



.border-draw::after {

&#x20; border-bottom: 2px solid var(--color-accent);

&#x20; border-left: 2px solid var(--color-accent);

&#x20; scale: 0 1;

&#x20; transform-origin: bottom left;

&#x20; transition: scale 0.3s var(--ease-out) 0.15s;

}



.border-draw:hover::before { scale: 1 1; }

.border-draw:hover::after  { scale: 1 1; }



/\* ─── 3. Corner brackets ─── \*/

.border-corners {

&#x20; position: relative;

&#x20; padding: var(--space-4);

}



.border-corners::before,

.border-corners::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; width: 20px;

&#x20; height: 20px;

&#x20; transition: width 0.3s, height 0.3s;

}



.border-corners::before {

&#x20; inset-block-start: 0;

&#x20; inset-inline-start: 0;

&#x20; border-top: 2px solid var(--color-accent);

&#x20; border-left: 2px solid var(--color-accent);

}



.border-corners::after {

&#x20; inset-block-end: 0;

&#x20; inset-inline-end: 0;

&#x20; border-bottom: 2px solid var(--color-accent);

&#x20; border-right: 2px solid var(--color-accent);

}



.border-corners:hover::before,

.border-corners:hover::after { width: 100%; height: 100%; }



/\* ─── 4. Marching ants ─── \*/

@keyframes march {

&#x20; to { stroke-dashoffset: -20; }

}



.border-marching {

&#x20; outline: none;

&#x20; position: relative;

}



.border-marching::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: -2px;

&#x20; border-radius: inherit;

&#x20; background: repeating-linear-gradient(

&#x20;   90deg,

&#x20;   var(--color-accent) 0 8px,

&#x20;   transparent 8px 16px

&#x20; ) top / 100% 2px no-repeat,

&#x20; repeating-linear-gradient(

&#x20;   180deg,

&#x20;   var(--color-accent) 0 8px,

&#x20;   transparent 8px 16px

&#x20; ) right / 2px 100% no-repeat,

&#x20; repeating-linear-gradient(

&#x20;   270deg,

&#x20;   var(--color-accent) 0 8px,

&#x20;   transparent 8px 16px

&#x20; ) bottom / 100% 2px no-repeat,

&#x20; repeating-linear-gradient(

&#x20;   0deg,

&#x20;   var(--color-accent) 0 8px,

&#x20;   transparent 8px 16px

&#x20; ) left / 2px 100% no-repeat;

&#x20; animation: march-h 0.5s linear infinite, march-v 0.5s linear infinite;

}



@keyframes march-h { to { background-position: calc(100% + 16px) top, right, calc(-100% - 16px) bottom, left; } }



/\* ─── 5. Pulsing outline ─── \*/

@keyframes outline-pulse {

&#x20; 0%   { outline-offset: 0; outline-color: var(--color-accent); }

&#x20; 50%  { outline-offset: 6px; outline-color: color-mix(in srgb, var(--color-accent) 30%, transparent); }

&#x20; 100% { outline-offset: 0; outline-color: var(--color-accent); }

}



.border-pulse:hover {

&#x20; animation: outline-pulse 1.5s ease-in-out infinite;

&#x20; outline: 2px solid var(--color-accent);

}



/\* ─── 6. Gradient border via mask ─── \*/

.border-gradient {

&#x20; position: relative;

&#x20; border-radius: var(--radius-xl);

&#x20; background: var(--color-surface);

}



.border-gradient::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: -1px;

&#x20; border-radius: inherit;

&#x20; background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-700));

&#x20; z-index: -1;

}

```



\---



\## 103. IMAGE COMPARISON SLIDER



```css

/\* ─── Before/After comparison (CSS-only via input\[range]) ─── \*/

.comparison {

&#x20; position: relative;

&#x20; overflow: hidden;

&#x20; --split: 50%;

}



.comparison\_\_before,

.comparison\_\_after {

&#x20; position: absolute;

&#x20; inset: 0;

}



.comparison\_\_before img,

.comparison\_\_after img {

&#x20; position: absolute;

&#x20; top: 0; left: 0;

&#x20; width: 100%; height: 100%;

&#x20; object-fit: cover;

}



.comparison\_\_after {

&#x20; clip-path: inset(0 0 0 var(--split));

}



/\* Divider line \*/

.comparison\_\_divider {

&#x20; position: absolute;

&#x20; top: 0; bottom: 0;

&#x20; left: var(--split);

&#x20; width: 2px;

&#x20; background: white;

&#x20; box-shadow: 0 0 8px rgba(0 0 0 / 0.5);

&#x20; z-index: 2;

}



/\* Handle \*/

.comparison\_\_handle {

&#x20; position: absolute;

&#x20; top: 50%;

&#x20; left: var(--split);

&#x20; translate: -50% -50%;

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; background: white;

&#x20; border-radius: 50%;

&#x20; box-shadow: 0 2px 12px rgba(0 0 0 / 0.3);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; z-index: 3;

&#x20; cursor: ew-resize;

}



.comparison\_\_handle::before,

.comparison\_\_handle::after {

&#x20; content: '';

&#x20; border: 6px solid transparent;

}



.comparison\_\_handle::before {

&#x20; border-right-color: var(--color-text);

&#x20; margin-right: 2px;

}



.comparison\_\_handle::after {

&#x20; border-left-color: var(--color-text);

&#x20; margin-left: 2px;

}



/\* Range input overlay \*/

.comparison\_\_range {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; opacity: 0;

&#x20; cursor: ew-resize;

&#x20; width: 100%;

&#x20; z-index: 4;

}



/\* JS: input.addEventListener('input', e => el.style.setProperty('--split', e.target.value + '%')) \*/

```



\---



\## 104. KANBAN BOARD



```css

/\* ─── Kanban layout ─── \*/

.kanban {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; overflow-x: auto;

&#x20; padding-block: var(--space-2);

&#x20; align-items: flex-start;

&#x20; min-height: calc(100dvh - var(--header-height, 60px));

&#x20; scrollbar-width: thin;

}



/\* Column \*/

.kanban-col {

&#x20; flex: 0 0 280px;

&#x20; background: var(--color-bg-subtle);

&#x20; border-radius: var(--radius-xl);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; max-height: calc(100dvh - var(--header-height, 60px) - var(--space-8));

}



.kanban-col\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; position: sticky;

&#x20; top: 0;

&#x20; background: inherit;

&#x20; border-radius: var(--radius-xl) var(--radius-xl) 0 0;

&#x20; z-index: 1;

}



.kanban-col\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; flex: 1;

}



.kanban-col\_\_count {

&#x20; background: var(--color-bg-muted);

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; padding: 0.15em 0.5em;

&#x20; border-radius: var(--radius-full);

&#x20; font-variant-numeric: tabular-nums;

}



/\* Column color accents \*/

.kanban-col--todo   .kanban-col\_\_header { border-top: 3px solid var(--color-neutral-400); }

.kanban-col--doing  .kanban-col\_\_header { border-top: 3px solid var(--color-brand-500); }

.kanban-col--review .kanban-col\_\_header { border-top: 3px solid var(--color-warning-500); }

.kanban-col--done   .kanban-col\_\_header { border-top: 3px solid var(--color-success-500); }



/\* Cards list \*/

.kanban-col\_\_cards {

&#x20; flex: 1;

&#x20; overflow-y: auto;

&#x20; padding: var(--space-3) var(--space-3) var(--space-3);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

&#x20; scrollbar-width: thin;

}



/\* Kanban card \*/

.kanban-card {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; padding: var(--space-3);

&#x20; cursor: grab;

&#x20; user-select: none;

&#x20; transition:

&#x20;   box-shadow var(--duration-fast),

&#x20;   scale      var(--duration-fast) var(--ease-bounce);

}



.kanban-card:hover {

&#x20; box-shadow: var(--shadow-md);

}



.kanban-card.dragging {

&#x20; opacity: 0.5;

&#x20; scale: 1.02;

&#x20; cursor: grabbing;

&#x20; box-shadow: var(--shadow-xl);

}



/\* Drop zone \*/

.kanban-col\_\_cards.drag-over {

&#x20; background: color-mix(in srgb, var(--color-accent) 5%, transparent);

&#x20; outline: 2px dashed var(--color-accent);

&#x20; outline-offset: -4px;

&#x20; border-radius: 0 0 var(--radius-xl) var(--radius-xl);

}



.kanban-card\_\_title {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; margin-block-end: var(--space-2);

}



.kanban-card\_\_tags {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-1);

&#x20; margin-block-end: var(--space-3);

}



.kanban-tag {

&#x20; padding: 0.125em 0.5em;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

}



.kanban-card\_\_footer {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; gap: var(--space-2);

}



.kanban-card\_\_due {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25em;

}



.kanban-card\_\_due--overdue { color: var(--color-danger-500); }

.kanban-card\_\_due--soon    { color: var(--color-warning-500); }



.kanban-card\_\_avatars {

&#x20; display: flex;

}



.kanban-card\_\_avatars .avatar {

&#x20; --size: 1.5rem;

&#x20; border: 2px solid var(--color-surface);

&#x20; margin-inline-start: -0.5rem;

}

.kanban-card\_\_avatars .avatar:first-child { margin-inline-start: 0; }



/\* Add column / Add card buttons \*/

.kanban-add-card {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: var(--space-2) var(--space-3);

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; border: none;

&#x20; background: none;

&#x20; width: 100%;

&#x20; cursor: pointer;

&#x20; border-radius: var(--radius-md);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.kanban-add-card:hover { background: var(--color-bg-muted); color: var(--color-text); }

```



\---



\## 105. TERMINAL / CONSOLE UI



```css

/\* ─── Terminal window ─── \*/

.terminal {

&#x20; background: #1a1a1a;

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.875rem;

&#x20; box-shadow: var(--shadow-2xl);

&#x20; color: #d4d4d4;

}



.terminal\_\_titlebar {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.625rem 1rem;

&#x20; background: #2d2d2d;

&#x20; border-bottom: 1px solid #3a3a3a;

}



.terminal\_\_dot { width: 12px; height: 12px; border-radius: 50%; }

.terminal\_\_dot--red    { background: #ff5f57; }

.terminal\_\_dot--yellow { background: #febc2e; }

.terminal\_\_dot--green  { background: #28c840; }



.terminal\_\_title {

&#x20; flex: 1;

&#x20; text-align: center;

&#x20; font-size: 0.75rem;

&#x20; color: #888;

}



.terminal\_\_body {

&#x20; padding: 1rem 1.25rem;

&#x20; min-height: 200px;

&#x20; max-height: 400px;

&#x20; overflow-y: auto;

&#x20; line-height: 1.6;

&#x20; scrollbar-width: thin;

&#x20; scrollbar-color: #444 transparent;

}



/\* Lines \*/

.terminal\_\_line {

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; gap: 0.5em;

&#x20; margin-block-end: 0.125em;

&#x20; white-space: pre-wrap;

&#x20; word-break: break-all;

}



.terminal\_\_prompt {

&#x20; color: #4ec9b0;

&#x20; user-select: none;

&#x20; flex-shrink: 0;

}



.terminal\_\_prompt::before { content: '$ '; }



.terminal\_\_cmd  { color: #d4d4d4; }

.terminal\_\_out  { color: #888; padding-inline-start: 1.5em; }

.terminal\_\_err  { color: #f48771; padding-inline-start: 1.5em; }

.terminal\_\_ok   { color: #4ec9b0; padding-inline-start: 1.5em; }

.terminal\_\_info { color: #9cdcfe; padding-inline-start: 1.5em; }



/\* Blinking cursor \*/

.terminal\_\_cursor {

&#x20; display: inline-block;

&#x20; width: 0.55em;

&#x20; height: 1.1em;

&#x20; background: #d4d4d4;

&#x20; vertical-align: text-bottom;

&#x20; animation: cursor-blink 1s step-end infinite;

}



@keyframes cursor-blink {

&#x20; 0%, 100% { opacity: 1; }

&#x20; 50%       { opacity: 0; }

}



/\* Syntax highlighting \*/

.term-string  { color: #ce9178; }

.term-number  { color: #b5cea8; }

.term-bool    { color: #569cd6; }

.term-null    { color: #569cd6; }

.term-key     { color: #9cdcfe; }

.term-comment { color: #6a9955; }



/\* ─── Command output animations ─── \*/

.terminal\_\_line {

&#x20; animation: line-appear 0.15s ease-out backwards;

}



@keyframes line-appear {

&#x20; from { opacity: 0; translate: 0 4px; }

}



/\* Stagger each new line \*/

.terminal\_\_line:nth-child(n) {

&#x20; animation-delay: calc(var(--line-index, 0) \* 0.05s);

}



/\* ─── Progress bar in terminal ─── \*/

.term-progress {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.75em;

&#x20; color: #4ec9b0;

&#x20; font-size: 0.875em;

}



.term-progress\_\_bar {

&#x20; flex: 1;

&#x20; height: 4px;

&#x20; background: #333;

&#x20; border-radius: 2px;

&#x20; overflow: hidden;

}



.term-progress\_\_fill {

&#x20; height: 100%;

&#x20; background: #4ec9b0;

&#x20; width: var(--progress, 0%);

&#x20; transition: width 0.3s;

}



/\* ─── JSON viewer ─── \*/

.json-viewer {

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.875rem;

&#x20; line-height: 1.7;

&#x20; color: #d4d4d4;

}



.json-key    { color: #9cdcfe; }

.json-str    { color: #ce9178; }

.json-num    { color: #b5cea8; }

.json-bool   { color: #569cd6; }

.json-null   { color: #569cd6; }

.json-punc   { color: #d4d4d4; }



/\* Collapsible JSON tree \*/

.json-toggle {

&#x20; cursor: pointer;

&#x20; user-select: none;

&#x20; background: none;

&#x20; border: none;

&#x20; color: inherit;

&#x20; padding: 0;

&#x20; font: inherit;

}

.json-toggle::before { content: '▾ '; font-size: 0.7em; }

.json-toggle.collapsed::before { content: '▸ '; }

.json-nested { padding-inline-start: 1.5em; }

.json-nested.collapsed { display: none; }

```



\---



\## 106. MEDIA PLAYER UI



\### 106.1 Audio Player



```css

/\* ─── Custom audio player ─── \*/

.audio-player {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-3);

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-5);

&#x20; max-width: 380px;

}



.audio-player\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-4);

}



.audio-player\_\_art {

&#x20; width: 3.5rem;

&#x20; height: 3.5rem;

&#x20; border-radius: var(--radius-lg);

&#x20; object-fit: cover;

&#x20; flex-shrink: 0;

&#x20; box-shadow: var(--shadow-md);

}



.audio-player\_\_info { min-width: 0; flex: 1; }



.audio-player\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



.audio-player\_\_artist {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



/\* Waveform (decorative) \*/

.audio-waveform {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: 2px;

&#x20; height: 40px;

&#x20; overflow: hidden;

}



.waveform-bar {

&#x20; width: 3px;

&#x20; background: var(--color-accent);

&#x20; border-radius: 2px;

&#x20; height: calc(var(--h, 0.5) \* 100%);

&#x20; opacity: 0.7;

&#x20; transition: height 0.1s;

}



/\* Playing animation \*/

.audio-player.playing .waveform-bar {

&#x20; animation: wave-bounce var(--d, 0.8s) ease-in-out infinite alternate;

&#x20; animation-delay: var(--delay, 0s);

&#x20; opacity: 1;

}



@keyframes wave-bounce {

&#x20; from { height: 20%; }

&#x20; to   { height: calc(var(--h, 0.5) \* 100%); }

}



/\* Progress \*/

.audio-progress {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-variant-numeric: tabular-nums;

}



.audio-progress\_\_bar {

&#x20; flex: 1;

&#x20; height: 4px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; cursor: pointer;

&#x20; position: relative;

}



.audio-progress\_\_fill {

&#x20; height: 100%;

&#x20; background: var(--color-accent);

&#x20; border-radius: inherit;

&#x20; width: var(--progress, 0%);

&#x20; position: relative;

}



.audio-progress\_\_fill::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; right: -5px;

&#x20; top: 50%;

&#x20; translate: 0 -50%;

&#x20; width: 12px;

&#x20; height: 12px;

&#x20; background: var(--color-accent);

&#x20; border-radius: 50%;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

&#x20; box-shadow: var(--shadow-sm);

}



.audio-progress\_\_bar:hover .audio-progress\_\_fill::after { opacity: 1; }



/\* Controls \*/

.audio-controls {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-3);

}



.audio-btn {

&#x20; background: none;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; border-radius: 50%;

&#x20; transition: color var(--duration-fast), background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

&#x20; width: 2rem;

&#x20; height: 2rem;

}



.audio-btn:hover { color: var(--color-text); background: var(--color-bg-subtle); }



.audio-btn--play {

&#x20; width: 3rem;

&#x20; height: 3rem;

&#x20; background: var(--color-accent);

&#x20; color: white;

}



.audio-btn--play:hover {

&#x20; background: var(--color-accent-hover);

&#x20; color: white;

&#x20; scale: 1.05;

}



/\* Volume \*/

.audio-volume {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



.volume-slider {

&#x20; width: 60px;

&#x20; height: 4px;

&#x20; appearance: none;

&#x20; background: linear-gradient(

&#x20;   to right,

&#x20;   var(--color-accent) var(--volume, 80%),

&#x20;   var(--color-bg-muted) var(--volume, 80%)

&#x20; );

&#x20; border-radius: var(--radius-full);

&#x20; outline: none;

&#x20; cursor: pointer;

}



.volume-slider::-webkit-slider-thumb {

&#x20; appearance: none;

&#x20; width: 12px;

&#x20; height: 12px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; cursor: pointer;

}

```



\### 106.2 Video Player



```css

/\* ─── Custom video player ─── \*/

.video-player {

&#x20; position: relative;

&#x20; background: #000;

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; aspect-ratio: 16 / 9;

&#x20; cursor: pointer;

}



.video-player video {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; display: block;

}



/\* Controls overlay \*/

.video-controls {

&#x20; position: absolute;

&#x20; inset-inline: 0;

&#x20; bottom: 0;

&#x20; padding: var(--space-4);

&#x20; background: linear-gradient(to top, rgba(0 0 0 / 0.8), transparent);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);



&#x20; opacity: 0;

&#x20; translate: 0 4px;

&#x20; transition:

&#x20;   opacity var(--duration-normal),

&#x20;   translate var(--duration-normal);

}



.video-player:hover .video-controls,

.video-player:focus-within .video-controls,

.video-player.paused .video-controls {

&#x20; opacity: 1;

&#x20; translate: 0 0;

}



/\* Seekbar \*/

.video-seekbar {

&#x20; width: 100%;

&#x20; height: 4px;

&#x20; background: rgba(255 255 255 / 0.3);

&#x20; border-radius: var(--radius-full);

&#x20; cursor: pointer;

&#x20; position: relative;

&#x20; transition: height var(--duration-fast);

}



.video-seekbar:hover { height: 6px; }



/\* Buffered progress \*/

.video-seekbar\_\_buffered {

&#x20; position: absolute;

&#x20; inset-block: 0;

&#x20; inset-inline-start: 0;

&#x20; width: var(--buffered, 0%);

&#x20; background: rgba(255 255 255 / 0.4);

&#x20; border-radius: inherit;

}



.video-seekbar\_\_fill {

&#x20; position: absolute;

&#x20; inset-block: 0;

&#x20; inset-inline-start: 0;

&#x20; width: var(--progress, 0%);

&#x20; background: var(--color-accent);

&#x20; border-radius: inherit;

}



.video-seekbar\_\_thumb {

&#x20; position: absolute;

&#x20; top: 50%;

&#x20; left: var(--progress, 0%);

&#x20; translate: -50% -50%;

&#x20; width: 12px;

&#x20; height: 12px;

&#x20; background: white;

&#x20; border-radius: 50%;

&#x20; pointer-events: none;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

&#x20; box-shadow: var(--shadow-sm);

}



.video-seekbar:hover .video-seekbar\_\_thumb { opacity: 1; }



/\* Controls row \*/

.video-controls\_\_row {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

}



.video-btn {

&#x20; background: none;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; color: white;

&#x20; opacity: 0.85;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; padding: var(--space-1);

&#x20; border-radius: var(--radius-md);

&#x20; transition: opacity var(--duration-fast);

}



.video-btn:hover { opacity: 1; }



.video-time {

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.85);

&#x20; font-variant-numeric: tabular-nums;

&#x20; font-family: var(--font-mono);

&#x20; white-space: nowrap;

&#x20; margin-inline-end: auto;

}



/\* Big play button in center \*/

.video-play-btn {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; pointer-events: none;

}



.video-play-btn\_\_icon {

&#x20; width: 4rem;

&#x20; height: 4rem;

&#x20; background: rgba(255 255 255 / 0.15);

&#x20; backdrop-filter: blur(8px);

&#x20; border-radius: 50%;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: white;

&#x20; font-size: 1.5rem;

&#x20; transition: opacity var(--duration-slow), scale var(--duration-slow);

&#x20; scale: 1;

&#x20; opacity: 1;

}



.video-player.playing .video-play-btn\_\_icon {

&#x20; opacity: 0;

&#x20; scale: 1.5;

}

```



\---



\## 107. NOTIFICATION CENTER



```css

/\* ─── Notification bell with count ─── \*/

.notif-bell {

&#x20; position: relative;

&#x20; display: inline-flex;

}



.notif-bell\_\_count {

&#x20; position: absolute;

&#x20; top: -4px;

&#x20; right: -4px;

&#x20; min-width: 1.125rem;

&#x20; height: 1.125rem;

&#x20; background: var(--color-danger-500);

&#x20; color: white;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: 0.625rem;

&#x20; font-weight: var(--font-weight-bold);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; padding-inline: 0.25rem;

&#x20; border: 2px solid var(--color-bg);

&#x20; animation: badge-in 0.3s var(--ease-bounce);

}



@keyframes badge-in {

&#x20; from { scale: 0; }

}



/\* ─── Notification panel ─── \*/

.notif-panel {

&#x20; width: 360px;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; box-shadow: var(--shadow-xl);

&#x20; overflow: hidden;

&#x20; max-height: 80dvh;

&#x20; display: flex;

&#x20; flex-direction: column;

}



.notif-panel\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; padding: var(--space-4) var(--space-5);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; gap: var(--space-3);

}



.notif-panel\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; flex: 1;

}



.notif-panel\_\_mark-all {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-accent);

&#x20; background: none;

&#x20; border: none;

&#x20; cursor: pointer;

}



.notif-list {

&#x20; overflow-y: auto;

&#x20; flex: 1;

&#x20; scrollbar-width: thin;

}



/\* Individual notification \*/

.notif-item {

&#x20; display: flex;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-4) var(--space-5);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast);

&#x20; position: relative;

&#x20; text-decoration: none;

&#x20; color: inherit;

}



.notif-item:hover { background: var(--color-bg-subtle); }



/\* Unread indicator \*/

.notif-item--unread { background: color-mix(in srgb, var(--color-accent) 4%, var(--color-surface)); }

.notif-item--unread::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-block: 0;

&#x20; inset-inline-start: 0;

&#x20; width: 3px;

&#x20; background: var(--color-accent);

}



.notif-item\_\_icon {

&#x20; width: 2.25rem;

&#x20; height: 2.25rem;

&#x20; border-radius: 50%;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 1rem;

&#x20; flex-shrink: 0;

&#x20; background: var(--color-bg-muted);

}



.notif-item\_\_icon--success { background: var(--color-success-100); }

.notif-item\_\_icon--warning { background: var(--color-warning-100); }

.notif-item\_\_icon--error   { background: var(--color-danger-100); }

.notif-item\_\_icon--info    { background: var(--color-brand-100); }



.notif-item\_\_body { flex: 1; min-width: 0; }



.notif-item\_\_text {

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.4;

&#x20; overflow: hidden;

&#x20; display: -webkit-box;

&#x20; -webkit-line-clamp: 2;

&#x20; -webkit-box-orient: vertical;

}



.notif-item\_\_text strong { font-weight: var(--font-weight-semibold); }



.notif-item\_\_time {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-start: var(--space-1);

}



/\* Dismiss button \*/

.notif-item\_\_dismiss {

&#x20; position: absolute;

&#x20; top: var(--space-3);

&#x20; right: var(--space-3);

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border-radius: 50%;

&#x20; border: none;

&#x20; background: var(--color-bg-muted);

&#x20; color: var(--color-text-muted);

&#x20; font-size: 0.625rem;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

}



.notif-item:hover .notif-item\_\_dismiss { opacity: 1; }



/\* Notification group by date \*/

.notif-group-label {

&#x20; padding: var(--space-2) var(--space-5);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; background: var(--color-bg-subtle);

&#x20; position: sticky;

&#x20; top: 0;

&#x20; z-index: 1;

}



/\* Empty state \*/

.notif-empty {

&#x20; padding: var(--space-12);

&#x20; text-align: center;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

}



/\* Inline toast within panel \*/

.notif-panel\_\_footer {

&#x20; padding: var(--space-3) var(--space-5);

&#x20; border-top: 1px solid var(--color-border);

&#x20; text-align: center;

}



.notif-panel\_\_footer a {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-accent);

&#x20; text-decoration: none;

}

```



\---



\## 108. DOCUMENT LAYOUTS: INVOICE \& CV



\### 108.1 Invoice / Receipt



```css

/\* ─── Invoice layout ─── \*/

.invoice {

&#x20; max-width: 720px;

&#x20; margin-inline: auto;

&#x20; padding: var(--space-12);

&#x20; background: var(--color-surface);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text);



&#x20; @media print {

&#x20;   padding: 0;

&#x20;   max-width: none;

&#x20; }

}



.invoice\_\_header {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; align-items: flex-start;

&#x20; margin-block-end: var(--space-10);

}



.invoice\_\_logo {

&#x20; font-size: var(--step-3);

&#x20; font-weight: var(--font-weight-black);

&#x20; color: var(--color-text);

&#x20; letter-spacing: -0.03em;

}



.invoice\_\_badge {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; padding: 0.25em 0.75em;

&#x20; border-radius: var(--radius-sm);

&#x20; background: var(--color-brand-100);

&#x20; color: var(--color-brand-700);

}



.invoice\_\_badge--paid { background: var(--color-success-100); color: var(--color-success-700); }

.invoice\_\_badge--due  { background: var(--color-warning-100); color: var(--color-warning-700); }

.invoice\_\_badge--overdue { background: var(--color-danger-100); color: var(--color-danger-700); }



/\* Metadata grid \*/

.invoice\_\_meta {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 1fr;

&#x20; gap: var(--space-8);

&#x20; margin-block-end: var(--space-8);

}



.invoice\_\_address { }



.invoice\_\_label {

&#x20; font-size: var(--font-size-xs);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; margin-block-end: var(--space-1);

}



.invoice\_\_details {

&#x20; display: grid;

&#x20; grid-template-columns: auto auto;

&#x20; gap: var(--space-1) var(--space-6);

&#x20; margin-block-end: var(--space-8);

}



.invoice\_\_detail-label {

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-xs);

}



/\* Line items table \*/

.invoice\_\_table {

&#x20; width: 100%;

&#x20; border-collapse: collapse;

&#x20; margin-block-end: var(--space-6);

}



.invoice\_\_table th {

&#x20; text-align: start;

&#x20; padding-block: var(--space-2);

&#x20; padding-inline: var(--space-3);

&#x20; border-bottom: 2px solid var(--color-border);

&#x20; font-size: var(--font-size-xs);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; font-weight: var(--font-weight-semibold);

}



.invoice\_\_table th:last-child,

.invoice\_\_table td:last-child {

&#x20; text-align: end;

}



.invoice\_\_table td {

&#x20; padding: var(--space-3);

&#x20; border-bottom: 1px solid var(--color-border);

}



.invoice\_\_table tbody tr:last-child td { border: none; }



/\* Totals \*/

.invoice\_\_totals {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr auto;

&#x20; gap: var(--space-1) var(--space-8);

&#x20; max-width: 280px;

&#x20; margin-inline-start: auto;

&#x20; margin-block-end: var(--space-8);

}



.invoice\_\_totals-label { color: var(--color-text-muted); font-size: var(--font-size-sm); }

.invoice\_\_totals-value { text-align: end; font-variant-numeric: tabular-nums; }



.invoice\_\_total-row { font-weight: var(--font-weight-bold); font-size: var(--font-size-base); border-top: 2px solid var(--color-border); padding-block-start: var(--space-2); }



/\* Notes \*/

.invoice\_\_notes {

&#x20; padding: var(--space-4);

&#x20; background: var(--color-bg-subtle);

&#x20; border-radius: var(--radius-lg);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; border: 1px solid var(--color-border);

}

```



\### 108.2 Resume / CV Layout



```css

/\* ─── CV / Resume ─── \*/

.cv {

&#x20; max-width: 800px;

&#x20; margin-inline: auto;

&#x20; display: grid;

&#x20; grid-template-columns: 240px 1fr;

&#x20; min-height: 100%;

&#x20; font-size: 0.875rem;



&#x20; @media print {

&#x20;   max-width: none;

&#x20;   font-size: 10pt;

&#x20; }

}



/\* Left column \*/

.cv\_\_sidebar {

&#x20; background: var(--color-neutral-900);

&#x20; color: var(--color-neutral-100);

&#x20; padding: var(--space-8) var(--space-6);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-6);

}



.cv\_\_photo {

&#x20; width: 120px;

&#x20; height: 120px;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

&#x20; border: 3px solid var(--color-neutral-700);

&#x20; margin-inline: auto;

&#x20; display: block;

}



.cv\_\_name {

&#x20; text-align: center;

&#x20; font-size: 1.25rem;

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: 0.25rem;

}



.cv\_\_title {

&#x20; text-align: center;

&#x20; font-size: 0.75rem;

&#x20; color: var(--color-neutral-400);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.1em;

}



.cv\_\_section-title {

&#x20; font-size: 0.625rem;

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.15em;

&#x20; color: var(--color-neutral-400);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: var(--space-3);

&#x20; padding-block-end: var(--space-1);

&#x20; border-bottom: 1px solid var(--color-neutral-700);

}



.cv\_\_contact-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: 0.8125rem;

&#x20; color: var(--color-neutral-300);

&#x20; margin-block-end: var(--space-2);

&#x20; text-decoration: none;

}



.cv\_\_contact-item:hover { color: white; }



/\* Skills \*/

.cv\_\_skill {

&#x20; margin-block-end: var(--space-2);

}



.cv\_\_skill-name {

&#x20; font-size: 0.8125rem;

&#x20; margin-block-end: 0.25rem;

&#x20; color: var(--color-neutral-200);

}



.cv\_\_skill-bar {

&#x20; height: 4px;

&#x20; background: var(--color-neutral-700);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

}



.cv\_\_skill-fill {

&#x20; height: 100%;

&#x20; background: var(--color-accent);

&#x20; border-radius: inherit;

&#x20; width: var(--level, 0%);

}



/\* Right column \*/

.cv\_\_main {

&#x20; padding: var(--space-8) var(--space-7);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-7);

}



.cv\_\_main-section-title {

&#x20; font-size: var(--font-size-lg);

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-neutral-900);

&#x20; padding-block-end: var(--space-2);

&#x20; border-bottom: 2px solid var(--color-accent);

&#x20; margin-block-end: var(--space-4);

}



/\* Experience item \*/

.cv\_\_exp-item {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr auto;

&#x20; gap: var(--space-1);

&#x20; margin-block-end: var(--space-5);

}



.cv\_\_exp-title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: 0.9375rem;

}



.cv\_\_exp-company {

&#x20; color: var(--color-accent);

&#x20; font-size: 0.875rem;

}



.cv\_\_exp-date {

&#x20; font-size: 0.75rem;

&#x20; color: var(--color-text-muted);

&#x20; text-align: end;

&#x20; grid-column: 2;

&#x20; grid-row: 1;

&#x20; white-space: nowrap;

}



.cv\_\_exp-desc {

&#x20; grid-column: 1 / -1;

&#x20; font-size: 0.8125rem;

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

&#x20; margin-block-start: var(--space-1);

}



.cv\_\_exp-bullets {

&#x20; grid-column: 1 / -1;

&#x20; padding-inline-start: 1em;

&#x20; margin-block-start: var(--space-2);

}



.cv\_\_exp-bullets li {

&#x20; font-size: 0.8125rem;

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-1);

&#x20; line-height: 1.5;

}

```



\---



\## 109. CSS COUNTERS — ADVANCED PATTERNS



```css

/\* ─── Legal document numbering (1.1.1 style) ─── \*/

.legal-doc {

&#x20; counter-reset: chapter;

}

.legal-doc h1 {

&#x20; counter-increment: chapter;

&#x20; counter-reset: section;

}

.legal-doc h1::before {

&#x20; content: counter(chapter) '. ';

}

.legal-doc h2 {

&#x20; counter-increment: section;

&#x20; counter-reset: subsection;

}

.legal-doc h2::before {

&#x20; content: counter(chapter) '.' counter(section) '. ';

}

.legal-doc h3 {

&#x20; counter-increment: subsection;

}

.legal-doc h3::before {

&#x20; content: counter(chapter) '.' counter(section) '.' counter(subsection) '. ';

}



/\* ─── Step counter with circle indicators ─── \*/

.steps-counter {

&#x20; counter-reset: step;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-6);

}



.step-item {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; counter-increment: step;

}



.step-item::before {

&#x20; content: counter(step);

&#x20; flex-shrink: 0;

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-sm);

&#x20; margin-block-start: 0.125rem;

}



/\* ─── Progress with counters ─── \*/

.reading-progress {

&#x20; counter-reset: words characters;

}

.reading-progress p {

&#x20; counter-increment: words 50;    /\* approximation \*/

}

/\* Not truly countable from CSS alone, but useful for footnotes etc \*/



/\* ─── Footnote system ─── \*/

:root { counter-reset: footnote; }



.footnote {

&#x20; counter-increment: footnote;

}



.footnote::after {

&#x20; content: '\[' counter(footnote) ']';

&#x20; vertical-align: super;

&#x20; font-size: 0.7em;

&#x20; color: var(--color-accent);

&#x20; text-decoration: none;

&#x20; margin-inline-start: 0.1em;

}



.footnotes-list { counter-reset: footnote-ref; }

.footnotes-list li {

&#x20; counter-increment: footnote-ref;

&#x20; list-style: none;

}

.footnotes-list li::before {

&#x20; content: '\[' counter(footnote-ref) '] ';

&#x20; color: var(--color-accent);

&#x20; font-weight: var(--font-weight-bold);

}



/\* ─── Figure / Table numbering ─── \*/

.document {

&#x20; counter-reset: figure table;

}



.figure {

&#x20; counter-increment: figure;

}

.figure figcaption::before {

&#x20; content: 'Figure ' counter(figure) ': ';

&#x20; font-weight: var(--font-weight-semibold);

}



.data-table {

&#x20; counter-increment: table;

}

.data-table caption::before {

&#x20; content: 'Table ' counter(table) ': ';

&#x20; font-weight: var(--font-weight-semibold);

}

```



\---



\## 110. CSS GRID: MAGAZINE LAYOUTS



```css

/\* ─── Classic magazine grid ─── \*/

.magazine {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(12, 1fr);

&#x20; grid-auto-rows: auto;

&#x20; gap: var(--space-4);

&#x20; max-width: 1200px;

&#x20; margin-inline: auto;

}



/\* Featured story (top-left, large) \*/

.story--hero {

&#x20; grid-column: 1 / 8;

&#x20; grid-row: 1 / 3;

}



/\* Secondary stories \*/

.story--secondary {

&#x20; grid-column: 8 / 13;

&#x20; grid-row: 1;

}



.story--secondary:nth-of-type(2) {

&#x20; grid-column: 8 / 13;

&#x20; grid-row: 2;

}



/\* Full-width divider story \*/

.story--full {

&#x20; grid-column: 1 / -1;

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 1fr;

&#x20; gap: var(--space-4);

}



/\* 3-column row \*/

.story--third {

&#x20; grid-column: span 4;

}



/\* Responsive \*/

@media (max-width: 768px) {

&#x20; .magazine {

&#x20;   grid-template-columns: 1fr;

&#x20; }

&#x20; .story--hero,

&#x20; .story--secondary,

&#x20; .story--third,

&#x20; .story--full {

&#x20;   grid-column: 1;

&#x20;   grid-row: auto;

&#x20; }

&#x20; .story--full { grid-template-columns: 1fr; }

}



/\* ─── Story card base ─── \*/

.story {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; background: var(--color-surface);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; border: 1px solid var(--color-border);

}



.story\_\_image {

&#x20; width: 100%;

&#x20; aspect-ratio: 16 / 9;

&#x20; object-fit: cover;

}



.story--hero .story\_\_image { aspect-ratio: 16 / 10; }



.story\_\_body { padding: var(--space-4); flex: 1; display: flex; flex-direction: column; gap: var(--space-2); }



.story\_\_category {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-accent);

}



.story\_\_title {

&#x20; font-weight: var(--font-weight-bold);

&#x20; line-height: var(--line-height-snug);

&#x20; text-wrap: balance;

}



.story--hero .story\_\_title {

&#x20; font-size: clamp(1.25rem, 2.5vw, 2rem);

}



.story\_\_excerpt {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; overflow: hidden;

&#x20; display: -webkit-box;

&#x20; -webkit-line-clamp: 3;

&#x20; -webkit-box-orient: vertical;

}



.story\_\_meta {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; margin-block-start: auto;

&#x20; padding-block-start: var(--space-3);

&#x20; border-top: 1px solid var(--color-border);

}



.story\_\_author {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



.story\_\_author img {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

}



.story\_\_date {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-subtle);

&#x20; margin-inline-start: auto;

}



/\* ─── Newsletter layout ─── \*/

.newsletter {

&#x20; max-width: 600px;

&#x20; margin-inline: auto;

&#x20; font-family: Georgia, serif;

&#x20; color: #333;

&#x20; background: #fff;

}



.newsletter\_\_header {

&#x20; background: #1a1a2e;

&#x20; padding: var(--space-8);

&#x20; text-align: center;

&#x20; color: white;

}



.newsletter\_\_logo {

&#x20; font-size: 2rem;

&#x20; font-weight: bold;

&#x20; letter-spacing: -0.03em;

}



.newsletter\_\_tagline {

&#x20; font-size: 0.875rem;

&#x20; opacity: 0.7;

&#x20; font-style: italic;

}



.newsletter\_\_date {

&#x20; font-size: 0.75rem;

&#x20; opacity: 0.5;

&#x20; margin-block-start: var(--space-2);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.1em;

}



.newsletter\_\_body { padding: var(--space-6); }



.newsletter\_\_intro {

&#x20; font-size: 1rem;

&#x20; line-height: 1.7;

&#x20; border-inline-start: 3px solid var(--color-accent);

&#x20; padding-inline-start: var(--space-4);

&#x20; color: #555;

&#x20; margin-block-end: var(--space-6);

}



.newsletter\_\_story {

&#x20; margin-block-end: var(--space-6);

&#x20; padding-block-end: var(--space-6);

&#x20; border-bottom: 1px solid #eee;

}



.newsletter\_\_story:last-child { border: none; }



.newsletter\_\_story-title {

&#x20; font-size: 1.25rem;

&#x20; font-weight: bold;

&#x20; margin-block-end: var(--space-2);

&#x20; line-height: 1.3;

}



.newsletter\_\_story-title a { color: inherit; text-decoration: none; }

.newsletter\_\_story-title a:hover { color: var(--color-accent); }



.newsletter\_\_story-text {

&#x20; font-size: 0.9375rem;

&#x20; line-height: 1.65;

&#x20; color: #444;

}



.newsletter\_\_cta {

&#x20; display: inline-block;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; padding: 0.625rem 1.5rem;

&#x20; border-radius: 4px;

&#x20; text-decoration: none;

&#x20; font-size: 0.875rem;

&#x20; font-weight: bold;

&#x20; margin-block-start: var(--space-3);

}



.newsletter\_\_footer {

&#x20; background: #f5f5f5;

&#x20; padding: var(--space-6);

&#x20; text-align: center;

&#x20; font-size: 0.75rem;

&#x20; color: #999;

&#x20; border-top: 1px solid #ddd;

}

```



\---



\## 111. CSS FOR SPECIFIC INTERACTIONS



\### 111.1 Drag and Drop Visual Feedback



```css

/\* ─── Draggable item ─── \*/

.draggable {

&#x20; cursor: grab;

&#x20; user-select: none;

&#x20; transition:

&#x20;   box-shadow var(--duration-fast),

&#x20;   scale      var(--duration-fast) var(--ease-bounce),

&#x20;   opacity    var(--duration-fast);

}



.draggable:active { cursor: grabbing; }



.draggable\[draggable="true"]:active,

.draggable.is-dragging {

&#x20; opacity: 0.5;

&#x20; scale: 1.02;

&#x20; box-shadow: var(--shadow-xl);

&#x20; cursor: grabbing;

&#x20; z-index: var(--z-raised);

&#x20; position: relative;

}



/\* Drop target \*/

.drop-target {

&#x20; transition:

&#x20;   background var(--duration-fast),

&#x20;   border-color var(--duration-fast);

&#x20; border: 2px solid transparent;

&#x20; border-radius: var(--radius-lg);

}



.drop-target.drag-over {

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, var(--color-surface));

&#x20; border-color: var(--color-accent);

}



.drop-target.drag-over--reject {

&#x20; background: color-mix(in srgb, var(--color-danger-500) 8%, var(--color-surface));

&#x20; border-color: var(--color-danger-500);

}



/\* Ghost placeholder (where item will be dropped) \*/

.drag-ghost {

&#x20; border: 2px dashed var(--color-accent);

&#x20; border-radius: var(--radius-lg);

&#x20; opacity: 0.5;

&#x20; background: color-mix(in srgb, var(--color-accent) 10%, transparent);

&#x20; height: var(--ghost-height, 60px);

&#x20; transition: height var(--duration-fast) var(--ease-out);

}



/\* Drag handle icon \*/

.drag-handle {

&#x20; cursor: grab;

&#x20; color: var(--color-text-muted);

&#x20; padding: var(--space-1);

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

}



.draggable:hover .drag-handle { opacity: 1; }

.draggable:active .drag-handle { cursor: grabbing; opacity: 1; }

```



\### 111.2 Swipe-able Cards (Mobile)



```css

/\* ─── Swipe card deck ─── \*/

.swipe-deck {

&#x20; position: relative;

&#x20; width: 300px;

&#x20; height: 400px;

}



.swipe-card {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; border-radius: var(--radius-2xl);

&#x20; background: var(--color-surface);

&#x20; box-shadow: var(--shadow-xl);

&#x20; cursor: grab;

&#x20; user-select: none;

&#x20; transform-origin: bottom center;

&#x20; transition: transform var(--duration-normal) var(--ease-out);

}



/\* Stack of cards \*/

.swipe-card:nth-child(1) { z-index: 3; }

.swipe-card:nth-child(2) { z-index: 2; scale: 0.95; translate: 0 16px; }

.swipe-card:nth-child(3) { z-index: 1; scale: 0.9;  translate: 0 32px; }



/\* JS sets --tx and --rotate on the top card \*/

.swipe-card.is-top {

&#x20; translate: var(--tx, 0) var(--ty, 0);

&#x20; rotate: var(--rotate, 0deg);

&#x20; transition: none;  /\* real-time drag \*/

}



.swipe-card.swiped-right {

&#x20; translate: 200% var(--ty, 0);

&#x20; rotate: 30deg;

&#x20; opacity: 0;

&#x20; transition:

&#x20;   translate 0.5s var(--ease-out),

&#x20;   rotate    0.5s var(--ease-out),

&#x20;   opacity   0.3s;

}



.swipe-card.swiped-left {

&#x20; translate: -200% var(--ty, 0);

&#x20; rotate: -30deg;

&#x20; opacity: 0;

&#x20; transition:

&#x20;   translate 0.5s var(--ease-out),

&#x20;   rotate    0.5s var(--ease-out),

&#x20;   opacity   0.3s;

}



/\* Like / Dislike indicators \*/

.swipe-like,

.swipe-nope {

&#x20; position: absolute;

&#x20; top: var(--space-6);

&#x20; padding: 0.5rem 1rem;

&#x20; border: 3px solid;

&#x20; border-radius: var(--radius-md);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-size: 1.5rem;

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.1em;

&#x20; opacity: 0;

&#x20; rotate: -20deg;

&#x20; pointer-events: none;

&#x20; transition: opacity var(--duration-fast);

}



.swipe-like {

&#x20; inset-inline-start: var(--space-6);

&#x20; color: var(--color-success-500);

&#x20; border-color: var(--color-success-500);

&#x20; rotate: -20deg;

}



.swipe-nope {

&#x20; inset-inline-end: var(--space-6);

&#x20; color: var(--color-danger-500);

&#x20; border-color: var(--color-danger-500);

&#x20; rotate: 20deg;

}



/\* JS sets --tx > 50 → show like; --tx < -50 → show nope \*/

.swipe-card.showing-like .swipe-like { opacity: calc((var(--tx, 0) - 50) / 100); }

.swipe-card.showing-nope .swipe-nope { opacity: calc((var(--tx, 0) \* -1 - 50) / 100); }

```



\### 111.3 Scroll-linked Effects



```css

/\* ─── Hero parallax header ─── \*/

.parallax-hero {

&#x20; position: relative;

&#x20; height: 80dvh;

&#x20; overflow: hidden;

}



.parallax-hero\_\_bg {

&#x20; position: absolute;

&#x20; inset: -30%;

&#x20; width: 160%;

&#x20; height: 160%;

&#x20; object-fit: cover;



&#x20; /\* Scroll-driven parallax \*/

&#x20; animation: parallax-scroll linear both;

&#x20; animation-timeline: scroll(root);

&#x20; animation-range: 0% 100vh;

}



@keyframes parallax-scroll {

&#x20; from { translate: 0 0; }

&#x20; to   { translate: 0 30%; }

}



.parallax-hero\_\_content {

&#x20; position: relative;

&#x20; z-index: 1;

&#x20; /\* Opposite direction — content scrolls slower \*/

&#x20; animation: parallax-content linear both;

&#x20; animation-timeline: scroll(root);

&#x20; animation-range: 0% 100vh;

}



@keyframes parallax-content {

&#x20; from { translate: 0 0; opacity: 1; }

&#x20; to   { translate: 0 -20%; opacity: 0; }

}



/\* ─── Sticky section with progress ─── \*/

.sticky-section {

&#x20; height: 300vh;  /\* tall container for scroll room \*/

&#x20; position: relative;

}



.sticky-section\_\_inner {

&#x20; position: sticky;

&#x20; top: 0;

&#x20; height: 100dvh;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; overflow: hidden;

}



/\* Track progress within sticky section \*/

.sticky-section {

&#x20; view-timeline: --section block;

}



.sticky-progress-bar {

&#x20; position: fixed;

&#x20; top: 0; left: 0;

&#x20; height: 3px;

&#x20; background: var(--color-accent);

&#x20; width: 0%;

&#x20; animation: track linear both;

&#x20; animation-timeline: --section;

&#x20; animation-range: contain;

}



@keyframes track {

&#x20; from { width: 0%; }

&#x20; to   { width: 100%; }

}



/\* ─── Reveal stagger on scroll ─── \*/

.scroll-reveal-list .item {

&#x20; opacity: 0;

&#x20; translate: 0 30px;

}



.scroll-reveal-list .item {

&#x20; animation: reveal-item linear both;

&#x20; animation-timeline: view();

&#x20; animation-range: entry 0% entry 40%;

&#x20; animation-delay: calc(var(--i, 0) \* 100ms);

}



@keyframes reveal-item {

&#x20; to { opacity: 1; translate: 0 0; }

}

```



\---



\## 112. ADVANCED CSS COLOR SYSTEM



\### 112.1 Dynamic Palette Generation



```css

/\* ─── Generate full palette from one brand color ─── \*/

@property --brand-h { syntax: '<number>'; initial-value: 250; inherits: true; }

@property --brand-c { syntax: '<number>'; initial-value: 0.2; inherits: true; }



:root {

&#x20; /\* Set base hue and chroma \*/

&#x20; --brand-h: 250;

&#x20; --brand-c: 0.2;



&#x20; /\* Auto-generate 10-step palette \*/

&#x20; --brand-50:  oklch(0.97 calc(var(--brand-c) \* 0.15) var(--brand-h));

&#x20; --brand-100: oklch(0.94 calc(var(--brand-c) \* 0.25) var(--brand-h));

&#x20; --brand-200: oklch(0.89 calc(var(--brand-c) \* 0.40) var(--brand-h));

&#x20; --brand-300: oklch(0.82 calc(var(--brand-c) \* 0.60) var(--brand-h));

&#x20; --brand-400: oklch(0.74 calc(var(--brand-c) \* 0.80) var(--brand-h));

&#x20; --brand-500: oklch(0.63 var(--brand-c) var(--brand-h));

&#x20; --brand-600: oklch(0.54 var(--brand-c) var(--brand-h));

&#x20; --brand-700: oklch(0.45 var(--brand-c) var(--brand-h));

&#x20; --brand-800: oklch(0.36 calc(var(--brand-c) \* 0.9) var(--brand-h));

&#x20; --brand-900: oklch(0.27 calc(var(--brand-c) \* 0.8) var(--brand-h));

&#x20; --brand-950: oklch(0.18 calc(var(--brand-c) \* 0.6) var(--brand-h));

}



/\* Change entire palette by changing 2 variables \*/

\[data-brand="emerald"] {

&#x20; --brand-h: 155;

&#x20; --brand-c: 0.18;

}



\[data-brand="rose"] {

&#x20; --brand-h: 10;

&#x20; --brand-c: 0.25;

}



\[data-brand="amber"] {

&#x20; --brand-h: 65;

&#x20; --brand-c: 0.22;

}



/\* ─── Automatic semantic tokens from palette ─── \*/

:root {

&#x20; --color-accent:          var(--brand-500);

&#x20; --color-accent-hover:    var(--brand-600);

&#x20; --color-accent-light:    var(--brand-100);

&#x20; --color-accent-dark:     var(--brand-800);

&#x20; --color-accent-subtle:   var(--brand-50);

&#x20; --color-accent-contrast: var(--brand-950);

}



/\* ─── APCA contrast checking via CSS (approximation) ─── \*/

/\*

&#x20; APCA Lc values for text:

&#x20; Lc >= 75: body text

&#x20; Lc >= 60: large text / UI

&#x20; Lc >= 45: placeholder, disabled



&#x20; Use oklch() lightness difference as approximation:

&#x20; High contrast: L(bg) - L(text) > 0.5

&#x20; Medium:        L(bg) - L(text) > 0.35

\*/



/\* ─── Adaptive color based on background ─── \*/

.adaptive-text {

&#x20; /\* Light-dark based on container \*/

&#x20; color: light-dark(

&#x20;   oklch(0.2 0 0),    /\* dark text on light bg \*/

&#x20;   oklch(0.95 0 0)    /\* light text on dark bg \*/

&#x20; );

}



/\* For dynamic backgrounds, use contrast-color (future spec) \*/

/\* color: contrast-color(var(--bg) vs oklch(0.2 0 0), oklch(0.95 0 0)); \*/

```



\---



\## 113. CSS TRANSITIONS — COMPLETE COOKBOOK



\### 113.1 Every Useful Transition Pattern



```css

/\* ─── Height: 0 → auto (the holy grail) ─── \*/

/\* Modern: with interpolate-size \*/

:root { interpolate-size: allow-keywords; }

.expandable {

&#x20; height: 0;

&#x20; overflow: hidden;

&#x20; transition: height 0.3s var(--ease-out);

}

.expandable.open { height: auto; }



/\* Legacy: max-height trick \*/

.expandable-legacy {

&#x20; max-height: 0;

&#x20; overflow: hidden;

&#x20; transition: max-height 0.4s var(--ease-out);

}

.expandable-legacy.open {

&#x20; max-height: 1000px;  /\* must exceed content height \*/

&#x20; transition-timing-function: var(--ease-in);  /\* prevents overshoot feel \*/

}



/\* ─── Smooth appear/disappear with display ─── \*/

.appear {

&#x20; opacity: 0;

&#x20; translate: 0 8px;

&#x20; display: none;

&#x20; transition:

&#x20;   opacity   0.2s var(--ease-out),

&#x20;   translate 0.2s var(--ease-out),

&#x20;   display   0.2s allow-discrete,

&#x20;   overlay   0.2s allow-discrete;

}



.appear.visible {

&#x20; opacity: 1;

&#x20; translate: 0 0;

&#x20; display: block;

}



@starting-style {

&#x20; .appear.visible {

&#x20;   opacity: 0;

&#x20;   translate: 0 8px;

&#x20; }

}



/\* ─── Smooth theme transition ─── \*/

/\* Only apply during theme toggle, not on load \*/

html.theme-transitioning \* {

&#x20; transition:

&#x20;   background-color 0.3s !important,

&#x20;   border-color     0.2s !important,

&#x20;   color            0.2s !important,

&#x20;   box-shadow       0.3s !important;

}

/\* JS: document.documentElement.classList.add('theme-transitioning')

&#x20;  → change theme → setTimeout remove class \*/



/\* ─── Transition only on user interaction (not on load) ─── \*/

.card {

&#x20; /\* No transition initially \*/

}



.user-has-interacted .card {

&#x20; transition: box-shadow var(--duration-normal) var(--ease-out);

}

/\* JS: document.addEventListener('pointerdown', () => body.classList.add('user-has-interacted')) \*/



/\* ─── Staggered list transitions ─── \*/

.list-item {

&#x20; transition:

&#x20;   opacity   0.3s var(--ease-out) calc(var(--index, 0) \* 50ms),

&#x20;   translate 0.3s var(--ease-out) calc(var(--index, 0) \* 50ms);

}



.list-item.entering  { opacity: 0; translate: 0 10px; }

.list-item.visible   { opacity: 1; translate: 0 0; }

.list-item.exiting   { opacity: 0; translate: 0 -10px; }

```



\---



\## 114. CSS ARCHITECTURE DECISION RECORDS (ADR)



```css

/\*

&#x20;\* ADR-001: Use CSS Custom Properties for ALL design tokens

&#x20;\* STATUS: Accepted

&#x20;\* CONTEXT: Need theming, easy override, component isolation

&#x20;\* DECISION: All values in :root as --token-name, never hardcode

&#x20;\* CONSEQUENCES: + theming, + isolation, - IE11 (dropped)

&#x20;\*

&#x20;\* ADR-002: Use @layer for specificity management

&#x20;\* STATUS: Accepted

&#x20;\* DECISION: @layer reset, base, layout, components, utilities, overrides

&#x20;\* CONSEQUENCES: + predictable specificity, + no !important wars

&#x20;\*

&#x20;\* ADR-003: Mobile-first breakpoints

&#x20;\* STATUS: Accepted

&#x20;\* DECISION: min-width queries, 0/640/768/1024/1280/1536 scale

&#x20;\* CONSEQUENCES: + smaller default CSS, + progressive enhancement

&#x20;\*

&#x20;\* ADR-004: Logical properties everywhere

&#x20;\* STATUS: Accepted (with exceptions for purely decorative)

&#x20;\* DECISION: margin-inline, padding-block, inset-inline-start etc

&#x20;\* CONSEQUENCES: + RTL support free, - slightly more verbose

&#x20;\*

&#x20;\* ADR-005: BEM naming within @scope or CSS modules

&#x20;\* STATUS: Accepted

&#x20;\* DECISION: .component\_\_element--modifier at component level

&#x20;\* CONSEQUENCES: + readable, + explicit, - verbose

&#x20;\*

&#x20;\* ADR-006: No ID selectors in authored CSS

&#x20;\* STATUS: Accepted

&#x20;\* DECISION: Use classes only. IDs for JS/anchor only.

&#x20;\* CONSEQUENCES: + reusable, + lower specificity

&#x20;\*

&#x20;\* ADR-007: clamp() for all fluid values

&#x20;\* STATUS: Accepted

&#x20;\* DECISION: clamp(min, preferred, max) for font-size/spacing

&#x20;\* CONSEQUENCES: + fewer breakpoints, + fluid UX

&#x20;\*

&#x20;\* ADR-008: oklch() for new color definitions

&#x20;\* STATUS: Accepted

&#x20;\* DECISION: New colors in oklch(), legacy in hex for compatibility

&#x20;\* CONSEQUENCES: + perceptual uniformity, + easy tinting

&#x20;\*

&#x20;\* ADR-009: CSS Nesting (native, not preprocessor)

&#x20;\* STATUS: Accepted (progressive enhancement)

&#x20;\* DECISION: Native @nesting, PostCSS as fallback if needed

&#x20;\* CONSEQUENCES: + co-located, - older browser support

&#x20;\*

&#x20;\* ADR-010: Container queries for component responsiveness

&#x20;\* STATUS: Accepted

&#x20;\* DECISION: component-level container-type, not just viewport

&#x20;\* CONSEQUENCES: + true component-driven design

&#x20;\*/

```



\---



\## 115. COMPLETE VISUAL DEBUGGING KIT



```css

/\* ─── Add to <head> temporarily for debugging ─── \*/

/\* <link rel="stylesheet" href="debug.css"> \*/



/\* Highlight different element types \*/

.debug-layout article  { outline: 2px solid oklch(0.7 0.25 0); }

.debug-layout section  { outline: 2px solid oklch(0.7 0.25 120); }

.debug-layout aside    { outline: 2px solid oklch(0.7 0.25 240); }

.debug-layout div      { outline: 1px solid oklch(0.7 0.1 0 / 0.3); }

.debug-layout p        { outline: 1px solid oklch(0.7 0.1 120 / 0.3); }

.debug-layout span     { outline: 1px dashed oklch(0.7 0.1 240 / 0.5); }



/\* Show all text as visual blocks \*/

.debug-text \* {

&#x20; color: transparent !important;

&#x20; background: var(--color-bg-muted) !important;

&#x20; border-radius: 2px !important;

}



/\* Show all images as colored boxes \*/

.debug-img img {

&#x20; filter: hue-rotate(90deg) !important;

&#x20; opacity: 0.5 !important;

}



/\* Show overflow issues \*/

.debug-overflow \* {

&#x20; overflow: visible !important;

&#x20; max-width: none !important;

}



/\* Highlight elements with inline styles \*/

.debug-inline \[style] {

&#x20; outline: 3px solid red !important;

}



/\* Highlight bad practices \*/

.debug-bad \*\[width]\[height] {

&#x20; outline: 3px solid orange;  /\* should use CSS for sizing \*/

}

.debug-bad img:not(\[alt]) {

&#x20; outline: 3px solid red;  /\* missing alt \*/

&#x20; filter: brightness(0.3) sepia(1) hue-rotate(330deg);

}

.debug-bad a:not(\[href]) {

&#x20; outline: 3px solid red;

}

.debug-bad button:not(\[type]) {

&#x20; outline: 2px dashed orange;

}

.debug-bad input:not(\[id]):not(\[aria-label]):not(\[aria-labelledby]) {

&#x20; outline: 3px solid red;

}



/\* Grid overlay \*/

.debug-grid::before {

&#x20; content: '';

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; pointer-events: none;

&#x20; z-index: 99999;

&#x20; background:

&#x20;   repeating-linear-gradient(

&#x20;     to right,

&#x20;     oklch(0.6 0.25 250 / 0.07) 0,

&#x20;     oklch(0.6 0.25 250 / 0.07) 1px,

&#x20;     transparent 1px,

&#x20;     transparent calc(100% / 12)

&#x20;   );

}



/\* Typography rhythm overlay \*/

.debug-rhythm::after {

&#x20; content: '';

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; pointer-events: none;

&#x20; z-index: 99998;

&#x20; background: repeating-linear-gradient(

&#x20;   to bottom,

&#x20;   oklch(0.7 0.15 40 / 0.1) 0,

&#x20;   oklch(0.7 0.15 40 / 0.1) 1px,

&#x20;   transparent 1px,

&#x20;   transparent 1.5rem  /\* matches line-height \*/

&#x20; );

}



/\* Show z-index values \*/

.debug-zindex \* {

&#x20; position: relative;

}

.debug-zindex \*::before {

&#x20; content: attr(style);

&#x20; position: absolute;

&#x20; top: 0;

&#x20; left: 0;

&#x20; font-size: 10px;

&#x20; background: red;

&#x20; color: white;

&#x20; padding: 1px 3px;

&#x20; pointer-events: none;

&#x20; z-index: 9999;

&#x20; font-family: monospace;

}

```



\---



\## 116. CSS SNIPPETS — FINAL COLLECTION



\### 116.1 The Useful 30



```css

/\* 1. Perfect circle image \*/

.avatar { border-radius: 50%; aspect-ratio: 1; object-fit: cover; }



/\* 2. Truncate text (1 line) \*/

.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }



/\* 3. Clamp text (N lines) \*/

.clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }



/\* 4. Center absolutely anything \*/

.abs-center { position: absolute; inset: 0; margin: auto; width: fit-content; height: fit-content; }



/\* 5. Full viewport section \*/

.full-page { min-height: 100dvh; }



/\* 6. Sticky footer \*/

body { display: flex; flex-direction: column; min-height: 100dvh; }

main { flex: 1; }



/\* 7. Responsive fluid container \*/

.container { max-inline-size: min(100% - 2rem, 72rem); margin-inline: auto; }



/\* 8. Aspect ratio box \*/

.ratio-16-9 { aspect-ratio: 16 / 9; overflow: hidden; }



/\* 9. Visually hidden (accessible) \*/

.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }



/\* 10. Smooth scroll \*/

html { scroll-behavior: smooth; }

@media (prefers-reduced-motion) { html { scroll-behavior: auto; } }



/\* 11. No FOUC for images \*/

img { display: block; max-width: 100%; height: auto; }



/\* 12. Better box sizing \*/

\*, \*::before, \*::after { box-sizing: border-box; }



/\* 13. Remove default button \*/

button { appearance: none; border: none; background: none; cursor: pointer; font: inherit; }



/\* 14. CSS reset for lists \*/

ul, ol { list-style: none; padding: 0; margin: 0; }



/\* 15. Fluid typography \*/

.fluid-text { font-size: clamp(1rem, 2vw + 0.5rem, 1.5rem); }



/\* 16. Glass morphism \*/

.glass { background: rgb(255 255 255 / 0.1); backdrop-filter: blur(10px); border: 1px solid rgb(255 255 255 / 0.2); }



/\* 17. Gradient text \*/

.gradient-text { background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; background-clip: text; color: transparent; }



/\* 18. Skeleton loading \*/

.skeleton { background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 4px; }

@keyframes shimmer { from { background-position: -200% 0; } to { background-position: 200% 0; } }



/\* 19. Focus ring \*/

:focus-visible { outline: 2px solid var(--color-accent, currentColor); outline-offset: 2px; }



/\* 20. Disabled state \*/

:disabled, \[aria-disabled="true"] { opacity: 0.5; cursor: not-allowed; pointer-events: none; }



/\* 21. Scrollbar gutter stability \*/

html { scrollbar-gutter: stable; }



/\* 22. Prevent layout shift from scrollbar \*/

body { overflow-y: scroll; }



/\* 23. Text balance on headings \*/

h1, h2, h3 { text-wrap: balance; }

p { text-wrap: pretty; }



/\* 24. Print: show URLs \*/

@media print { a\[href]::after { content: ' (' attr(href) ')'; } }



/\* 25. High-DPI images \*/

@media (-webkit-min-device-pixel-ratio: 2) { .logo { background-image: url('logo@2x.png'); background-size: 100px 50px; } }



/\* 26. iOS form zoom fix \*/

input, select, textarea { font-size: max(16px, 1em); }



/\* 27. Custom checkbox reset to style \*/

input\[type="checkbox"] { appearance: none; -webkit-appearance: none; }



/\* 28. Better default transition \*/

.interactive { transition: background-color var(--t, 0.15s), color var(--t, 0.15s), border-color var(--t, 0.15s), opacity var(--t, 0.15s), transform var(--t, 0.15s); }



/\* 29. Safe area padding \*/

.safe { padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left); }



/\* 30. The universal overlay \*/

.overlay { position: absolute; inset: 0; background: var(--overlay-color, rgb(0 0 0 / 0.5)); }

```



\### 116.2 One-liner CSS Tricks



```css

/\* Make page unselectable (kiosk mode) \*/

body { user-select: none; }



/\* Force GPU acceleration \*/

.promoted { will-change: transform; transform: translateZ(0); }



/\* Prevent image dragging \*/

img { -webkit-user-drag: none; user-drag: none; }



/\* Smooth font on dark backgrounds \*/

.dark-bg { -webkit-font-smoothing: antialiased; }



/\* Remove tap highlight on mobile \*/

\* { -webkit-tap-highlight-color: transparent; }



/\* Clickable everywhere in a link \*/

.card-link::after { content: ''; position: absolute; inset: 0; }

.card-link { position: relative; }



/\* Respect user's system color scheme \*/

html { color-scheme: light dark; }



/\* Prevent orphaned words in headings \*/

h1, h2 { text-wrap: balance; }



/\* Ratio-aware padding hack (legacy) \*/

.aspect-box::before { content: ''; display: block; padding-top: 56.25%; }



/\* Disable all animations (debug) \*/

\* { animation: none !important; transition: none !important; }



/\* Make <details> not show triangle \*/

summary { list-style: none; }

summary::-webkit-details-marker { display: none; }



/\* Force hardware rendering for videos \*/

video { transform: translateZ(0); }



/\* Prevent white flash on image load \*/

img { background: var(--color-bg-subtle); }

```



\---



```

╔══════════════════════════════════════════════════════════════════════╗

║            PARTS I–VI: COMPLETE CSS MASTER REFERENCE                 ║

╠══════════════════════════════════════════════════════════════════════╣

║                                                                      ║

║  116 chapters · 600+ code examples · \~22,000 lines                  ║

║                                                                      ║

║  NEW IN PART VI:                                                     ║

║  ✅ Hover effects library (image, button, text — 15 effects)         ║

║  ✅ Border animations (spinning, draw, corners, marching ants)       ║

║  ✅ Before/After comparison slider                                   ║

║  ✅ Kanban board (full drag-drop states)                             ║

║  ✅ Terminal / Console UI (syntax highlighting, progress)            ║

║  ✅ Audio player + Video player (custom controls)                    ║

║  ✅ Notification center (panel, items, bell, unread)                 ║

║  ✅ Invoice layout + Resume/CV layout                                ║

║  ✅ CSS Counters advanced (legal, footnotes, figures)                ║

║  ✅ Magazine \& Newsletter layouts                                    ║

║  ✅ Drag-and-drop visual feedback                                    ║

║  ✅ Swipe card deck (Tinder-style)                                  ║

║  ✅ Scroll-linked parallax + sticky sections                         ║

║  ✅ Dynamic palette generation from one variable                     ║

║  ✅ Transition cookbook (height:auto, display, stagger)              ║

║  ✅ CSS Architecture Decision Records (ADR)                          ║

║  ✅ Visual debugging kit (30+ debug utilities)                       ║

║  ✅ Final snippets collection (60 one-liners and utilities)          ║

║                                                                      ║

╚══════════════════════════════════════════════════════════════════════╝

```

