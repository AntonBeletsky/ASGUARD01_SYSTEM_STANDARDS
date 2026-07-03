\# CSS GUIDE — PART 12

\## Chapters 169–184



\---



\## 169. RADAR / SPIDER CHART



```css

/\* ─── CSS-only radar chart using clip-path + conic-gradient ─── \*/

.radar-chart {

&#x20; position: relative;

&#x20; width: 280px;

&#x20; height: 280px;

&#x20; display: grid;

&#x20; place-items: center;

}



/\* Background polygon levels \*/

.radar-grid {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; display: grid;

&#x20; place-items: center;

}



.radar-level {

&#x20; position: absolute;

&#x20; width: calc(var(--level, 1) \* 20%);

&#x20; height: calc(var(--level, 1) \* 20%);

&#x20; border: 1px solid var(--color-border);

&#x20; clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);

&#x20; /\* 6-sided: adjust for different axis counts \*/

}



/\* Axis lines \*/

.radar-axis {

&#x20; position: absolute;

&#x20; top: 50%;

&#x20; left: 50%;

&#x20; width: 50%;

&#x20; height: 1px;

&#x20; background: var(--color-border);

&#x20; transform-origin: left center;

&#x20; transform: rotate(var(--angle, 0deg));

}



/\* Data polygon \*/

.radar-data {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; clip-path: polygon(

&#x20;   /\* JS calculates each point: (50% + r\*sin(angle), 50% - r\*cos(angle)) \*/

&#x20;   var(--p1, 50% 10%),

&#x20;   var(--p2, 90% 33%),

&#x20;   var(--p3, 76% 80%),

&#x20;   var(--p4, 24% 80%),

&#x20;   var(--p5, 10% 33%),

&#x20;   var(--p6, 50% 10%)

&#x20; );

&#x20; background: color-mix(in srgb, var(--color-accent) 25%, transparent);

&#x20; border: 2px solid var(--color-accent);

}



/\* Labels \*/

.radar-label {

&#x20; position: absolute;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

&#x20; white-space: nowrap;

&#x20; transform: translate(-50%, -50%);

&#x20; left: var(--lx, 50%);

&#x20; top:  var(--ly, 5%);

}



/\* Value dots \*/

.radar-dot {

&#x20; position: absolute;

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; border: 2px solid white;

&#x20; box-shadow: var(--shadow-sm);

&#x20; translate: -50% -50%;

&#x20; left: var(--dx, 50%);

&#x20; top:  var(--dy, 50%);

&#x20; cursor: pointer;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}

.radar-dot:hover { scale: 1.5; }



/\* Tooltip on dot \*/

.radar-dot::after {

&#x20; content: attr(data-value);

&#x20; position: absolute;

&#x20; bottom: 120%;

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; padding: 0.2em 0.5em;

&#x20; border-radius: var(--radius-md);

&#x20; white-space: nowrap;

&#x20; opacity: 0;

&#x20; pointer-events: none;

&#x20; transition: opacity var(--duration-fast);

}

.radar-dot:hover::after { opacity: 1; }



/\* Multiple datasets \*/

.radar-data--secondary {

&#x20; clip-path: polygon(var(--q1), var(--q2), var(--q3), var(--q4), var(--q5), var(--q6));

&#x20; background: color-mix(in srgb, var(--color-success-500) 20%, transparent);

&#x20; border-color: var(--color-success-500);

}



/\* Legend \*/

.radar-legend {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; justify-content: center;

&#x20; margin-block-start: var(--space-4);

&#x20; font-size: var(--font-size-xs);

}



.radar-legend-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

}



.radar-legend-dot {

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; border-radius: 50%;

&#x20; background: var(--legend-color, var(--color-accent));

}

```



\---



\## 170. AREA \& LINE CHART (CSS)



```css

/\* ─── SVG-based line/area chart with CSS styling ─── \*/

.line-chart-container {

&#x20; position: relative;

&#x20; width: 100%;

&#x20; padding-block-end: var(--space-6);

}



/\* Chart SVG styling \*/

.chart-svg {

&#x20; overflow: visible;

&#x20; width: 100%;

&#x20; height: auto;

}



/\* Grid lines \*/

.chart-grid-line {

&#x20; stroke: var(--color-border);

&#x20; stroke-width: 1;

&#x20; stroke-dasharray: 4 4;

}



/\* X/Y axis \*/

.chart-axis {

&#x20; stroke: var(--color-border-strong);

&#x20; stroke-width: 1.5;

&#x20; fill: none;

}



/\* Area fill \*/

.chart-area {

&#x20; fill: color-mix(in srgb, var(--color-accent) 15%, transparent);

&#x20; transition: fill var(--duration-normal);

}



/\* Line \*/

.chart-line {

&#x20; fill: none;

&#x20; stroke: var(--color-accent);

&#x20; stroke-width: 2.5;

&#x20; stroke-linecap: round;

&#x20; stroke-linejoin: round;

&#x20; /\* Animate draw-on \*/

&#x20; stroke-dasharray: 1000;

&#x20; stroke-dashoffset: 1000;

&#x20; animation: draw-line 1.5s var(--ease-out) forwards;

}



@keyframes draw-line {

&#x20; to { stroke-dashoffset: 0; }

}



/\* Data points \*/

.chart-dot {

&#x20; fill: white;

&#x20; stroke: var(--color-accent);

&#x20; stroke-width: 2;

&#x20; cursor: pointer;

&#x20; transition: r var(--duration-fast) var(--ease-bounce);

}

.chart-dot:hover { r: 6; }



/\* Labels \*/

.chart-label {

&#x20; font-size: 11px;

&#x20; fill: var(--color-text-muted);

&#x20; font-family: var(--font-sans);

}



.chart-value-label {

&#x20; font-size: 11px;

&#x20; fill: var(--color-text);

&#x20; font-weight: 600;

&#x20; font-family: var(--font-sans);

}



/\* Tooltip crosshair \*/

.chart-crosshair {

&#x20; stroke: var(--color-text-muted);

&#x20; stroke-width: 1;

&#x20; stroke-dasharray: 4 2;

&#x20; opacity: 0;

&#x20; pointer-events: none;

&#x20; transition: opacity var(--duration-fast);

}



.chart-svg:hover .chart-crosshair { opacity: 1; }



/\* Tooltip \*/

.chart-tooltip {

&#x20; position: absolute;

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; border-radius: var(--radius-lg);

&#x20; padding: var(--space-3);

&#x20; font-size: var(--font-size-xs);

&#x20; pointer-events: none;

&#x20; translate: -50% calc(-100% - 10px);

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

&#x20; min-width: 100px;

&#x20; box-shadow: var(--shadow-xl);

&#x20; z-index: 10;

}



.chart-tooltip.visible { opacity: 1; }



.chart-tooltip\_\_date {

&#x20; color: rgba(255 255 255 / 0.6);

&#x20; margin-block-end: var(--space-1);

}



.chart-tooltip\_\_value {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-variant-numeric: tabular-nums;

}



/\* Multi-series colors \*/

.chart-line--2 { stroke: var(--color-success-500); }

.chart-area--2 { fill: color-mix(in srgb, var(--color-success-500) 12%, transparent); }

.chart-line--3 { stroke: var(--color-warning-500); }

.chart-area--3 { fill: color-mix(in srgb, var(--color-warning-500) 12%, transparent); }



/\* Stacked area \*/

.chart-area-stacked { fill-opacity: 0.6; }

```



\---



\## 171. MIND MAP



```css

/\* ─── Mind map layout ─── \*/

.mindmap {

&#x20; position: relative;

&#x20; width: 100%;

&#x20; height: 600px;

&#x20; overflow: auto;

&#x20; background: var(--color-bg-subtle);

&#x20; cursor: grab;

}

.mindmap.panning { cursor: grabbing; }



.mindmap-viewport {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; left: 0;

&#x20; transform: translate(var(--pan-x, 0px), var(--pan-y, 0px)) scale(var(--zoom, 1));

&#x20; transform-origin: top left;

&#x20; will-change: transform;

}



/\* Central node \*/

.mindmap-root {

&#x20; position: absolute;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-3) var(--space-6);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-lg);

&#x20; box-shadow: var(--shadow-lg);

&#x20; white-space: nowrap;

&#x20; cursor: pointer;

&#x20; z-index: 2;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce), box-shadow var(--duration-fast);

&#x20; left: var(--x, 0);

&#x20; top:  var(--y, 0);

&#x20; translate: -50% -50%;

}

.mindmap-root:hover { scale: 1.05; box-shadow: var(--shadow-xl); }



/\* Branch node \*/

.mindmap-node {

&#x20; position: absolute;

&#x20; background: var(--color-surface);

&#x20; border: 2px solid var(--node-color, var(--color-border));

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-2) var(--space-4);

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; box-shadow: var(--shadow-sm);

&#x20; cursor: pointer;

&#x20; z-index: 2;

&#x20; white-space: nowrap;

&#x20; transition:

&#x20;   scale      var(--duration-fast) var(--ease-bounce),

&#x20;   box-shadow var(--duration-fast),

&#x20;   background var(--duration-fast);

&#x20; left: var(--x, 0);

&#x20; top:  var(--y, 0);

&#x20; translate: -50% -50%;

}

.mindmap-node:hover {

&#x20; background: var(--color-bg-subtle);

&#x20; scale: 1.05;

&#x20; box-shadow: var(--shadow-md);

}



.mindmap-node.selected {

&#x20; background: color-mix(in srgb, var(--node-color, var(--color-accent)) 10%, var(--color-surface));

&#x20; border-color: var(--node-color, var(--color-accent));

}



/\* Level colors \*/

.mindmap-node\[data-level="1"] { --node-color: var(--color-brand-500); }

.mindmap-node\[data-level="2"] { --node-color: var(--color-success-500); }

.mindmap-node\[data-level="3"] { --node-color: var(--color-warning-500); }

.mindmap-node\[data-level="4"] { --node-color: var(--color-danger-400); }



/\* Connection SVG \*/

.mindmap-connections {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; pointer-events: none;

&#x20; z-index: 1;

}



.mindmap-edge {

&#x20; fill: none;

&#x20; stroke: var(--edge-color, var(--color-border));

&#x20; stroke-width: 2;

&#x20; stroke-linecap: round;

&#x20; opacity: 0.7;

}



.mindmap-edge--level-1 { --edge-color: var(--color-brand-300); stroke-width: 2.5; }

.mindmap-edge--level-2 { --edge-color: var(--color-success-300); }

.mindmap-edge--level-3 { --edge-color: var(--color-warning-300); }



/\* Collapse button \*/

.mindmap-collapse {

&#x20; position: absolute;

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-surface);

&#x20; border: 1.5px solid var(--color-border);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 0.625rem;

&#x20; color: var(--color-text-muted);

&#x20; z-index: 3;

&#x20; transition: background var(--duration-fast);

&#x20; left: var(--cx, 0);

&#x20; top:  var(--cy, 0);

&#x20; translate: -50% -50%;

}

.mindmap-collapse:hover { background: var(--color-bg-muted); }



/\* Add node button \*/

.mindmap-add {

&#x20; position: absolute;

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; font-size: 1rem;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

&#x20; z-index: 3;

}

.mindmap-node:hover \~ .mindmap-add,

.mindmap-add:hover { opacity: 1; scale: 1.1; }

```



\---



\## 172. COUNTDOWN TIMER



```css

/\* ─── Countdown timer card ─── \*/

.countdown {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; flex-wrap: wrap;

}



.countdown-unit {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

}



.countdown-value {

&#x20; position: relative;

&#x20; width: 80px;

&#x20; height: 80px;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 2.25rem;

&#x20; font-weight: var(--font-weight-black);

&#x20; font-variant-numeric: tabular-nums;

&#x20; font-family: var(--font-mono);

&#x20; box-shadow: var(--shadow-md);

&#x20; overflow: hidden;

}



/\* Flip animation on change \*/

.countdown-value.flipping {

&#x20; animation: flip-digit 0.4s ease-in-out;

}



@keyframes flip-digit {

&#x20; 0%   { transform: rotateX(0deg); }

&#x20; 50%  { transform: rotateX(90deg); }

&#x20; 100% { transform: rotateX(0deg); }

}



/\* Separator \*/

.countdown-sep {

&#x20; font-size: 2rem;

&#x20; font-weight: var(--font-weight-black);

&#x20; color: var(--color-text-muted);

&#x20; padding-block-end: var(--space-5);

&#x20; line-height: 1;

}



.countdown-label {

&#x20; font-size: var(--font-size-xs);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

}



/\* Urgent state \*/

.countdown.urgent .countdown-value {

&#x20; border-color: var(--color-danger-300);

&#x20; color: var(--color-danger-600);

&#x20; animation: urgent-pulse 1s ease-in-out infinite;

}



@keyframes urgent-pulse {

&#x20; 0%, 100% { box-shadow: var(--shadow-md); }

&#x20; 50%       { box-shadow: 0 0 0 4px color-mix(in srgb, var(--color-danger-500) 20%, transparent); }

}



/\* Dark variant \*/

.countdown--dark .countdown-value {

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; border-color: var(--color-neutral-700);

}



/\* Circular variant \*/

.countdown--circle .countdown-value {

&#x20; border-radius: 50%;

&#x20; width: 90px;

&#x20; height: 90px;

&#x20; position: relative;

}



.countdown--circle .countdown-value svg {

&#x20; position: absolute;

&#x20; inset: -4px;

&#x20; width: calc(100% + 8px);

&#x20; height: calc(100% + 8px);

&#x20; rotate: -90deg;

}



.countdown-ring {

&#x20; fill: none;

&#x20; stroke: var(--color-bg-muted);

&#x20; stroke-width: 4;

}



.countdown-ring-fill {

&#x20; fill: none;

&#x20; stroke: var(--color-accent);

&#x20; stroke-width: 4;

&#x20; stroke-linecap: round;

&#x20; stroke-dasharray: 251; /\* 2π×40 \*/

&#x20; stroke-dashoffset: calc(251 - 251 \* var(--progress, 0));

&#x20; transition: stroke-dashoffset 0.9s linear;

}



/\* Inline mini countdown \*/

.countdown-inline {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: 0.25em;

&#x20; font-variant-numeric: tabular-nums;

&#x20; font-family: var(--font-mono);

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-danger-500);

&#x20; background: var(--color-danger-100);

&#x20; padding: 0.2em 0.6em;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-sm);

}



/\* Progress bar countdown \*/

.countdown-bar {

&#x20; width: 100%;

&#x20; height: 6px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

}



.countdown-bar\_\_fill {

&#x20; height: 100%;

&#x20; background: var(--color-accent);

&#x20; width: var(--progress, 100%);

&#x20; border-radius: inherit;

&#x20; transition: width 1s linear, background 0.3s;

}



.countdown-bar\_\_fill\[style\*="--progress: 2"] { background: var(--color-danger-500); }

.countdown-bar\_\_fill\[style\*="--progress: 1"] { background: var(--color-danger-500); }

```



\---



\## 173. EMOJI PICKER



```css

/\* ─── Emoji picker panel ─── \*/

.emoji-picker {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; box-shadow: var(--shadow-xl);

&#x20; width: 320px;

&#x20; overflow: hidden;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; max-height: 400px;

&#x20; animation: picker-appear 0.15s var(--ease-out);

}



@keyframes picker-appear {

&#x20; from { opacity: 0; scale: 0.95; translate: 0 6px; }

}



/\* Search \*/

.emoji-search {

&#x20; padding: var(--space-3);

&#x20; border-bottom: 1px solid var(--color-border);

}



.emoji-search\_\_input {

&#x20; width: 100%;

&#x20; padding: 0.5rem 0.75rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-full);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; background: var(--color-bg-subtle);

&#x20; outline: none;

&#x20; transition: border-color var(--duration-fast);

}

.emoji-search\_\_input:focus { border-color: var(--color-accent); }



/\* Category tabs \*/

.emoji-tabs {

&#x20; display: flex;

&#x20; overflow-x: auto;

&#x20; scrollbar-width: none;

&#x20; padding-inline: var(--space-2);

&#x20; gap: 2px;

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; padding-block: var(--space-1);

}

.emoji-tabs::-webkit-scrollbar { display: none; }



.emoji-tab {

&#x20; flex-shrink: 0;

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border: none;

&#x20; background: none;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; font-size: 1rem;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; transition: background var(--duration-fast);

&#x20; position: relative;

}

.emoji-tab:hover { background: var(--color-bg-subtle); }

.emoji-tab.active { background: var(--color-bg-muted); }

.emoji-tab.active::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; bottom: -5px;

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; width: 3px;

&#x20; height: 3px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

}



/\* Emoji grid \*/

.emoji-body {

&#x20; overflow-y: auto;

&#x20; flex: 1;

&#x20; padding: var(--space-2) var(--space-3);

&#x20; scrollbar-width: thin;

}



.emoji-section-title {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; margin-block: var(--space-2);

&#x20; padding-inline: var(--space-1);

}



.emoji-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(8, 1fr);

&#x20; gap: 2px;

}



.emoji-btn {

&#x20; width: 2.25rem;

&#x20; height: 2.25rem;

&#x20; border: none;

&#x20; background: none;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; font-size: 1.25rem;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; transition:

&#x20;   background var(--duration-fast),

&#x20;   scale      var(--duration-fast) var(--ease-bounce);

&#x20; position: relative;

}

.emoji-btn:hover { background: var(--color-bg-subtle); scale: 1.3; }

.emoji-btn:active { scale: 1.1; }



/\* Skin tone modifier \*/

.emoji-btn.has-variants::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; bottom: 2px;

&#x20; right: 2px;

&#x20; width: 4px;

&#x20; height: 4px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-text-muted);

&#x20; opacity: 0.5;

}



/\* Footer: recent + skin tone \*/

.emoji-footer {

&#x20; padding: var(--space-2) var(--space-3);

&#x20; border-top: 1px solid var(--color-border);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

}



.skin-tones {

&#x20; display: flex;

&#x20; gap: 4px;

}



.skin-tone-btn {

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border-radius: 50%;

&#x20; border: 2px solid transparent;

&#x20; cursor: pointer;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce), border-color var(--duration-fast);

}

.skin-tone-btn:hover { scale: 1.2; }

.skin-tone-btn.selected { border-color: var(--color-text); }



.skin-tone-btn\[data-tone="1"] { background: #ffd83d; }

.skin-tone-btn\[data-tone="2"] { background: #ffcd96; }

.skin-tone-btn\[data-tone="3"] { background: #e0a86c; }

.skin-tone-btn\[data-tone="4"] { background: #b97836; }

.skin-tone-btn\[data-tone="5"] { background: #8a5018; }

.skin-tone-btn\[data-tone="6"] { background: #4a2c0e; }

```



\---



\## 174. FILE UPLOAD QUEUE



```css

/\* ─── Upload queue list ─── \*/

.upload-queue {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

}



.upload-item {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; display: grid;

&#x20; grid-template-columns: 2.5rem 1fr auto;

&#x20; gap: var(--space-3);

&#x20; align-items: center;

&#x20; animation: upload-item-in 0.2s var(--ease-out);

}



@keyframes upload-item-in {

&#x20; from { opacity: 0; translate: 0 -8px; }

}



.upload-item.removing {

&#x20; animation: upload-item-out 0.2s var(--ease-in) forwards;

}



@keyframes upload-item-out {

&#x20; to { opacity: 0; translate: 0 -4px; height: 0; margin: 0; padding: 0; overflow: hidden; }

}



/\* File icon \*/

.upload-icon {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: var(--radius-md);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 1.25rem;

&#x20; flex-shrink: 0;

}



.upload-icon--image  { background: var(--color-brand-100); }

.upload-icon--pdf    { background: var(--color-danger-100); }

.upload-icon--doc    { background: var(--color-brand-100); }

.upload-icon--sheet  { background: var(--color-success-100); }

.upload-icon--zip    { background: var(--color-warning-100); }

.upload-icon--video  { background: oklch(0.93 0.05 290); }

.upload-icon--audio  { background: oklch(0.93 0.05 320); }

.upload-icon--other  { background: var(--color-bg-muted); }



/\* Upload info \*/

.upload-info { min-width: 0; }



.upload-name {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

&#x20; margin-block-end: var(--space-1);

}



.upload-meta {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



.upload-size { font-variant-numeric: tabular-nums; }



/\* Progress bar \*/

.upload-progress {

&#x20; height: 4px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

&#x20; margin-block-start: var(--space-2);

}



.upload-progress\_\_fill {

&#x20; height: 100%;

&#x20; border-radius: inherit;

&#x20; background: var(--color-accent);

&#x20; width: var(--progress, 0%);

&#x20; transition: width 0.3s var(--ease-out);

}



.upload-progress\_\_fill--error { background: var(--color-danger-500); }

.upload-progress\_\_fill--done  { background: var(--color-success-500); }



/\* Status \*/

.upload-status {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25em;

}



.upload-status--uploading { color: var(--color-accent); }

.upload-status--done      { color: var(--color-success-600); }

.upload-status--error     { color: var(--color-danger-500); }

.upload-status--paused    { color: var(--color-warning-600); }



/\* Action buttons \*/

.upload-actions {

&#x20; display: flex;

&#x20; gap: var(--space-1);

&#x20; flex-shrink: 0;

}



.upload-action-btn {

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; border: none;

&#x20; background: none;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 0.875rem;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.upload-action-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }

.upload-action-btn.danger:hover { background: var(--color-danger-100); color: var(--color-danger-600); }



/\* Queue summary \*/

.upload-summary {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-3);

&#x20; background: var(--color-bg-subtle);

&#x20; border-radius: var(--radius-lg);

&#x20; font-size: var(--font-size-sm);

}



.upload-summary\_\_total { color: var(--color-text-muted); }

.upload-summary\_\_speed { font-variant-numeric: tabular-nums; font-weight: var(--font-weight-medium); }

```



\---



\## 175. VIDEO CALL UI



```css

/\* ─── Video call layout ─── \*/

.video-call {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; background: #0f0f0f;

&#x20; display: grid;

&#x20; grid-template-rows: 1fr auto;

&#x20; overflow: hidden;

}



/\* Main video grid \*/

.call-grid {

&#x20; position: relative;

&#x20; flex: 1;

&#x20; display: grid;

&#x20; gap: 4px;

&#x20; padding: 4px;

&#x20; overflow: hidden;

}



/\* 1 participant \*/

.call-grid\[data-participants="1"] { grid-template-columns: 1fr; }

/\* 2 participants \*/

.call-grid\[data-participants="2"] { grid-template-columns: 1fr 1fr; }

/\* 3-4 participants \*/

.call-grid\[data-participants="3"],

.call-grid\[data-participants="4"] {

&#x20; grid-template-columns: 1fr 1fr;

&#x20; grid-template-rows: 1fr 1fr;

}

/\* 5-6 \*/

.call-grid\[data-participants="5"],

.call-grid\[data-participants="6"] {

&#x20; grid-template-columns: repeat(3, 1fr);

&#x20; grid-template-rows: 1fr 1fr;

}



/\* Participant tile \*/

.call-tile {

&#x20; position: relative;

&#x20; background: #1a1a1a;

&#x20; border-radius: 8px;

&#x20; overflow: hidden;

}



.call-tile video {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; display: block;

}



/\* Video off state \*/

.call-tile--no-video {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; background: linear-gradient(135deg, #2a2a3e, #1a1a2e);

}



.call-tile\_\_avatar {

&#x20; width: 80px;

&#x20; height: 80px;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

&#x20; border: 3px solid rgba(255 255 255 / 0.2);

}



/\* Name label \*/

.call-tile\_\_name {

&#x20; position: absolute;

&#x20; bottom: var(--space-2);

&#x20; left: var(--space-2);

&#x20; background: rgba(0 0 0 / 0.6);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

&#x20; padding: 0.2em 0.6em;

&#x20; border-radius: var(--radius-md);

&#x20; backdrop-filter: blur(4px);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.375rem;

&#x20; max-width: calc(100% - var(--space-4));

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



/\* Muted mic indicator \*/

.call-tile\_\_muted {

&#x20; position: absolute;

&#x20; top: var(--space-2);

&#x20; right: var(--space-2);

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; background: var(--color-danger-500);

&#x20; border-radius: 50%;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 0.75rem;

&#x20; color: white;

}



/\* Speaking indicator \*/

.call-tile.speaking {

&#x20; outline: 3px solid var(--color-success-400);

&#x20; outline-offset: -3px;

}



/\* Active speaker large view \*/

.call-tile.pinned {

&#x20; grid-column: 1 / -1;

&#x20; grid-row: 1 / -1;

}



/\* Hand raised \*/

.call-tile\_\_hand {

&#x20; position: absolute;

&#x20; top: var(--space-2);

&#x20; left: var(--space-2);

&#x20; font-size: 1.25rem;

&#x20; animation: hand-wave 1s ease-in-out infinite;

}

@keyframes hand-wave {

&#x20; 0%, 100% { rotate: 0deg; }

&#x20; 25%       { rotate: 20deg; }

&#x20; 75%       { rotate: -10deg; }

}



/\* Self tile (always bottom-right) \*/

.call-tile--self {

&#x20; position: absolute;

&#x20; bottom: var(--space-4);

&#x20; right: var(--space-4);

&#x20; width: 160px;

&#x20; height: 90px;

&#x20; border-radius: var(--radius-lg);

&#x20; border: 2px solid rgba(255 255 255 / 0.2);

&#x20; overflow: hidden;

&#x20; z-index: 5;

&#x20; cursor: move;

&#x20; box-shadow: var(--shadow-xl);

}



/\* Bottom controls bar \*/

.call-controls {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-4) var(--space-6);

&#x20; background: rgba(0 0 0 / 0.8);

&#x20; backdrop-filter: blur(20px);

}



.call-btn {

&#x20; width: 3rem;

&#x20; height: 3rem;

&#x20; border-radius: 50%;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 1.125rem;

&#x20; color: white;

&#x20; background: rgba(255 255 255 / 0.15);

&#x20; transition:

&#x20;   background  var(--duration-fast),

&#x20;   scale       var(--duration-fast) var(--ease-bounce);

}

.call-btn:hover { background: rgba(255 255 255 / 0.25); scale: 1.05; }



.call-btn--active { background: rgba(255 255 255 / 0.9); color: #0f0f0f; }

.call-btn--danger { background: var(--color-danger-500); }

.call-btn--danger:hover { background: var(--color-danger-600); }

.call-btn--end { width: 3.5rem; height: 3.5rem; font-size: 1.25rem; }



/\* Participants panel \*/

.call-participants-panel {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; right: 0;

&#x20; bottom: 0;

&#x20; width: 280px;

&#x20; background: rgba(15 15 15 / 0.95);

&#x20; backdrop-filter: blur(20px);

&#x20; border-left: 1px solid rgba(255 255 255 / 0.1);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; z-index: 10;

&#x20; animation: panel-slide 0.3s var(--ease-out);

}



@keyframes panel-slide {

&#x20; from { translate: 100% 0; }

}



.call-participant-row {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; border-bottom: 1px solid rgba(255 255 255 / 0.05);

&#x20; color: white;

}



.call-participant-avatar {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

&#x20; flex-shrink: 0;

}



.call-participant-name {

&#x20; flex: 1;

&#x20; font-size: var(--font-size-sm);

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



.call-participant-status {

&#x20; display: flex;

&#x20; gap: var(--space-1);

&#x20; font-size: 0.75rem;

&#x20; opacity: 0.6;

}

```



\---



\## 176. REAL-TIME COLLABORATION CURSORS



```css

/\* ─── Multi-user cursor indicators ─── \*/

.collab-cursor {

&#x20; position: fixed;

&#x20; pointer-events: none;

&#x20; z-index: var(--z-top);

&#x20; translate: var(--cx, 0px) var(--cy, 0px);

&#x20; transition: translate 0.08s linear;

&#x20; will-change: translate;

}



/\* Cursor SVG arrow \*/

.collab-cursor\_\_arrow {

&#x20; width: 20px;

&#x20; height: 20px;

&#x20; filter: drop-shadow(0 1px 2px rgb(0 0 0 / 0.3));

&#x20; fill: var(--user-color, #3b82f6);

&#x20; stroke: white;

&#x20; stroke-width: 1.5;

}



/\* Name label \*/

.collab-cursor\_\_label {

&#x20; position: absolute;

&#x20; top: 18px;

&#x20; left: 12px;

&#x20; background: var(--user-color, #3b82f6);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; padding: 0.2em 0.5em;

&#x20; border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md);

&#x20; white-space: nowrap;

&#x20; max-width: 120px;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

}



/\* Away/idle cursor \*/

.collab-cursor.idle .collab-cursor\_\_arrow {

&#x20; opacity: 0.5;

}



.collab-cursor.idle .collab-cursor\_\_label::after {

&#x20; content: ' (idle)';

&#x20; opacity: 0.7;

}



/\* Click ripple \*/

.collab-cursor.clicking::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 2px;

&#x20; left: 2px;

&#x20; width: 16px;

&#x20; height: 16px;

&#x20; border: 2px solid var(--user-color, #3b82f6);

&#x20; border-radius: 50%;

&#x20; animation: cursor-click 0.4s ease-out forwards;

}



@keyframes cursor-click {

&#x20; from { scale: 1; opacity: 0.8; }

&#x20; to   { scale: 3; opacity: 0; }

}



/\* ─── User presence avatars (top bar) ─── \*/

.presence-bar {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



.presence-avatar {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: 50%;

&#x20; border: 2px solid var(--user-color, var(--color-accent));

&#x20; cursor: pointer;

&#x20; position: relative;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce), z-index 0s;

}

.presence-avatar:hover { scale: 1.2; z-index: 1; }



/\* Active/viewing indicator \*/

.presence-avatar.active::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: -3px;

&#x20; border: 2px solid var(--user-color, var(--color-accent));

&#x20; border-radius: 50%;

&#x20; animation: presence-pulse 2s ease-in-out infinite;

}



@keyframes presence-pulse {

&#x20; 0%, 100% { opacity: 0.8; scale: 1; }

&#x20; 50%       { opacity: 0; scale: 1.5; }

}



/\* Selection highlight overlay \*/

.collab-selection {

&#x20; position: absolute;

&#x20; background: color-mix(in srgb, var(--user-color, #3b82f6) 20%, transparent);

&#x20; border: 1px solid color-mix(in srgb, var(--user-color, #3b82f6) 50%, transparent);

&#x20; border-radius: 2px;

&#x20; pointer-events: none;

}



/\* Typing indicator in shared doc \*/

.collab-typing {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: 3px;

&#x20; padding: 2px 6px;

&#x20; background: var(--user-color, #3b82f6);

&#x20; border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md);

&#x20; position: absolute;

}



.collab-typing span {

&#x20; width: 4px;

&#x20; height: 4px;

&#x20; border-radius: 50%;

&#x20; background: white;

&#x20; animation: typing-dot 1.2s ease-in-out infinite;

}

.collab-typing span:nth-child(2) { animation-delay: 0.15s; }

.collab-typing span:nth-child(3) { animation-delay: 0.3s; }



@keyframes typing-dot {

&#x20; 0%, 60%, 100% { opacity: 0.3; scale: 0.8; }

&#x20; 30%           { opacity: 1; scale: 1; }

}

```



\---



\## 177. CHANGELOG / RELEASE NOTES



```css

/\* ─── Changelog page ─── \*/

.changelog {

&#x20; max-width: 720px;

&#x20; margin-inline: auto;

&#x20; padding: var(--space-8) var(--space-4);

}



/\* Version entry \*/

.changelog-entry {

&#x20; display: grid;

&#x20; grid-template-columns: 180px 1fr;

&#x20; gap: var(--space-8);

&#x20; padding-block: var(--space-8);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; position: relative;

}



.changelog-entry:last-child { border: none; }



@media (max-width: 600px) {

&#x20; .changelog-entry { grid-template-columns: 1fr; gap: var(--space-4); }

&#x20; .changelog-sidebar { flex-direction: row; align-items: center; }

}



/\* Timeline line \*/

.changelog-entry::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; left: 179px;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; width: 1px;

&#x20; background: var(--color-border);

}



@media (max-width: 600px) {

&#x20; .changelog-entry::before { display: none; }

}



/\* Sidebar: date + version \*/

.changelog-sidebar {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

&#x20; padding-block-start: var(--space-2);

&#x20; position: relative;

}



/\* Timeline dot \*/

.changelog-sidebar::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; right: calc(-var(--space-8) / 2 - 4.5px);

&#x20; top: var(--space-3);

&#x20; width: 9px;

&#x20; height: 9px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; border: 2px solid var(--color-surface);

&#x20; box-shadow: 0 0 0 2px var(--color-accent);

}



@media (max-width: 600px) {

&#x20; .changelog-sidebar::after { display: none; }

}



.changelog-version {

&#x20; font-size: var(--font-size-xl);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-family: var(--font-mono);

&#x20; color: var(--color-text);

}



.changelog-date {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-weight: var(--font-weight-medium);

}



.changelog-badge {

&#x20; display: inline-flex;

&#x20; padding: 0.2em 0.6em;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; width: fit-content;

}



.changelog-badge--major   { background: var(--color-danger-100); color: var(--color-danger-700); }

.changelog-badge--minor   { background: var(--color-brand-100); color: var(--color-brand-700); }

.changelog-badge--patch   { background: var(--color-bg-muted); color: var(--color-text-muted); }

.changelog-badge--beta    { background: var(--color-warning-100); color: var(--color-warning-700); }

.changelog-badge--latest  { background: var(--color-success-100); color: var(--color-success-700); }



/\* Content \*/

.changelog-content { }



.changelog-content h3 {

&#x20; font-size: var(--font-size-lg);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: var(--space-4);

&#x20; color: var(--color-text);

}



/\* Change categories \*/

.changelog-category {

&#x20; margin-block-end: var(--space-4);

}



.changelog-category-title {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; margin-block-end: var(--space-2);

}



/\* Category type indicators \*/

.changelog-category--added .changelog-category-title     { color: var(--color-success-600); }

.changelog-category--changed .changelog-category-title   { color: var(--color-brand-600); }

.changelog-category--fixed .changelog-category-title     { color: var(--color-warning-600); }

.changelog-category--removed .changelog-category-title   { color: var(--color-danger-600); }

.changelog-category--deprecated .changelog-category-title { color: var(--color-neutral-500); }

.changelog-category--security .changelog-category-title  { color: var(--color-danger-700); }



.changelog-category-icon {

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border-radius: var(--radius-sm);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 0.625rem;

}



.changelog-category--added .changelog-category-icon     { background: var(--color-success-100); }

.changelog-category--changed .changelog-category-icon   { background: var(--color-brand-100); }

.changelog-category--fixed .changelog-category-icon     { background: var(--color-warning-100); }

.changelog-category--removed .changelog-category-icon   { background: var(--color-danger-100); }



/\* Change items \*/

.changelog-items {

&#x20; list-style: none;

&#x20; padding: 0;

&#x20; margin: 0;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-1);

}



.changelog-item {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text);

&#x20; padding-inline-start: 1em;

&#x20; position: relative;

&#x20; line-height: 1.5;

}



.changelog-item::before {

&#x20; content: '–';

&#x20; position: absolute;

&#x20; left: 0;

&#x20; color: var(--color-text-muted);

}



.changelog-item code {

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.85em;

&#x20; background: var(--color-bg-muted);

&#x20; padding: 0.1em 0.3em;

&#x20; border-radius: var(--radius-sm);

}



/\* PR/Issue links \*/

.changelog-item a {

&#x20; color: var(--color-accent);

&#x20; text-decoration: none;

&#x20; font-size: 0.85em;

&#x20; font-family: var(--font-mono);

}

.changelog-item a:hover { text-decoration: underline; }

```



\---



\## 178. ROADMAP UI



```css

/\* ─── Product roadmap ─── \*/

.roadmap {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));

&#x20; gap: var(--space-4);

}



/\* Column \*/

.roadmap-col {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-3);

}



.roadmap-col\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding-block-end: var(--space-3);

&#x20; border-bottom: 2px solid var(--col-color, var(--color-border));

}



.roadmap-col\_\_title {

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-sm);

&#x20; flex: 1;

}



.roadmap-col\_\_count {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; background: var(--color-bg-muted);

&#x20; padding: 0.15em 0.5em;

&#x20; border-radius: var(--radius-full);

&#x20; font-variant-numeric: tabular-nums;

&#x20; font-weight: var(--font-weight-semibold);

}



/\* Column phases \*/

.roadmap-col--planned  { --col-color: var(--color-neutral-400); }

.roadmap-col--progress { --col-color: var(--color-brand-500); }

.roadmap-col--review   { --col-color: var(--color-warning-500); }

.roadmap-col--done     { --col-color: var(--color-success-500); }



/\* Roadmap card \*/

.roadmap-card {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-4);

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   box-shadow  var(--duration-fast),

&#x20;   translate   var(--duration-fast);

&#x20; border-top: 3px solid var(--card-color, var(--color-border));

}



.roadmap-card:hover {

&#x20; box-shadow: var(--shadow-md);

&#x20; translate: 0 -1px;

}



.roadmap-card\_\_tags {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-1);

&#x20; margin-block-end: var(--space-2);

}



.roadmap-tag {

&#x20; padding: 0.1em 0.5em;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

}



.roadmap-card\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.4;

&#x20; margin-block-end: var(--space-2);

}



.roadmap-card\_\_desc {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.5;

&#x20; overflow: hidden;

&#x20; display: -webkit-box;

&#x20; -webkit-line-clamp: 2;

&#x20; -webkit-box-orient: vertical;

}



.roadmap-card\_\_footer {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; margin-block-start: var(--space-3);

&#x20; padding-block-start: var(--space-3);

&#x20; border-top: 1px solid var(--color-border);

}



.roadmap-card\_\_votes {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; cursor: pointer;

&#x20; padding: 0.2em 0.5em;

&#x20; border-radius: var(--radius-md);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.roadmap-card\_\_votes:hover { background: var(--color-brand-100); color: var(--color-brand-600); }

.roadmap-card\_\_votes.voted { color: var(--color-accent); font-weight: var(--font-weight-semibold); }



.roadmap-card\_\_quarter {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-weight: var(--font-weight-medium);

}



/\* Quarter header (timeline view) \*/

.roadmap-quarter {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; padding: var(--space-2) 0;

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; margin-block-end: var(--space-3);

}

```



\---



\## 179. QUIZ / EDUCATIONAL UI



```css

/\* ─── Quiz question card ─── \*/

.quiz {

&#x20; max-width: 680px;

&#x20; margin-inline: auto;

&#x20; padding: var(--space-4);

}



.quiz-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-4);

&#x20; margin-block-end: var(--space-6);

}



.quiz-progress-bar {

&#x20; flex: 1;

&#x20; height: 8px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

}



.quiz-progress-bar\_\_fill {

&#x20; height: 100%;

&#x20; background: var(--color-accent);

&#x20; border-radius: inherit;

&#x20; width: var(--quiz-progress, 0%);

&#x20; transition: width 0.4s var(--ease-out);

}



.quiz-question-num {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; font-weight: var(--font-weight-medium);

&#x20; white-space: nowrap;

&#x20; font-variant-numeric: tabular-nums;

}



.quiz-timer {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; font-family: var(--font-mono);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-sm);

&#x20; font-variant-numeric: tabular-nums;

&#x20; color: var(--timer-color, var(--color-text-muted));

}



.quiz-timer.warning { --timer-color: var(--color-danger-500); animation: timer-pulse 1s ease-in-out infinite; }

@keyframes timer-pulse {

&#x20; 0%, 100% { opacity: 1; }

&#x20; 50%       { opacity: 0.5; }

}



/\* Question \*/

.quiz-card {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-8);

&#x20; margin-block-end: var(--space-4);

&#x20; animation: question-enter 0.3s var(--ease-out);

}



@keyframes question-enter {

&#x20; from { opacity: 0; translate: 20px 0; }

}



.quiz-category {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-accent);

&#x20; margin-block-end: var(--space-3);

}



.quiz-question {

&#x20; font-size: clamp(1rem, 2vw + 0.5rem, 1.25rem);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; line-height: 1.5;

&#x20; margin-block-end: var(--space-6);

&#x20; text-wrap: pretty;

}



.quiz-image {

&#x20; width: 100%;

&#x20; border-radius: var(--radius-lg);

&#x20; margin-block-end: var(--space-4);

}



/\* Answer options \*/

.quiz-options {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-3);

}



.quiz-option {

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; gap: var(--space-4);

&#x20; padding: var(--space-4);

&#x20; border: 2px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   background   var(--duration-fast),

&#x20;   scale        var(--duration-fast) var(--ease-bounce);

&#x20; user-select: none;

}



.quiz-option:hover {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 5%, transparent);

}



.quiz-option.selected {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, transparent);

&#x20; scale: 1.01;

}



/\* Answer reveal states \*/

.quiz-option.correct {

&#x20; border-color: var(--color-success-500);

&#x20; background: var(--color-success-100);

&#x20; animation: correct-flash 0.4s var(--ease-out);

}



.quiz-option.wrong {

&#x20; border-color: var(--color-danger-500);

&#x20; background: var(--color-danger-100);

&#x20; animation: wrong-shake 0.4s var(--ease-out);

}



@keyframes correct-flash {

&#x20; 0%   { scale: 0.98; }

&#x20; 50%  { scale: 1.02; }

&#x20; 100% { scale: 1; }

}



@keyframes wrong-shake {

&#x20; 0%, 100% { translate: 0; }

&#x20; 25%       { translate: -6px; }

&#x20; 75%       { translate: 6px; }

}



/\* Option letter badge \*/

.quiz-option\_\_letter {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-bg-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-sm);

&#x20; flex-shrink: 0;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}



.quiz-option.selected .quiz-option\_\_letter  { background: var(--color-accent); color: white; }

.quiz-option.correct .quiz-option\_\_letter   { background: var(--color-success-500); color: white; }

.quiz-option.wrong .quiz-option\_\_letter     { background: var(--color-danger-500); color: white; }



.quiz-option\_\_text {

&#x20; flex: 1;

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.5;

}



/\* Explanation \*/

.quiz-explanation {

&#x20; margin-block-start: var(--space-4);

&#x20; padding: var(--space-4);

&#x20; background: var(--color-bg-subtle);

&#x20; border-radius: var(--radius-lg);

&#x20; border-inline-start: 3px solid var(--color-accent);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

&#x20; animation: fade-in 0.3s var(--ease-out);

}



@keyframes fade-in { from { opacity: 0; translate: 0 8px; } }



.quiz-explanation\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text);

&#x20; margin-block-end: var(--space-2);

}



/\* Results screen \*/

.quiz-results {

&#x20; text-align: center;

&#x20; padding: var(--space-10);

}



.quiz-score {

&#x20; font-size: clamp(3rem, 10vw, 6rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-variant-numeric: tabular-nums;

&#x20; line-height: 1;

&#x20; background: linear-gradient(135deg, var(--color-accent), var(--color-brand-300));

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

&#x20; animation: score-in 0.8s var(--spring-bouncy) forwards;

}



@keyframes score-in {

&#x20; from { scale: 0; opacity: 0; }

}



.quiz-grade {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block: var(--space-2);

}

```



\---



\## 180. DYSLEXIA-FRIENDLY TYPOGRAPHY



```css

/\* ─── Accessible reading mode for dyslexia ─── \*/

\[data-reading-mode="dyslexia"] {

&#x20; /\* Recommended fonts for dyslexia \*/

&#x20; font-family: 'OpenDyslexic', 'Lexie Readable', Verdana, Geneva, Tahoma, sans-serif;



&#x20; /\* Increased spacing \*/

&#x20; letter-spacing: 0.12em;

&#x20; word-spacing: 0.25em;

&#x20; line-height: 1.9;



&#x20; /\* Left-aligned (never justify) \*/

&#x20; text-align: left;



&#x20; /\* Prevent auto-hyphenation \*/

&#x20; hyphens: none;

&#x20; -webkit-hyphens: none;



&#x20; /\* No italics (harder to read) \*/

&#x20; font-style: normal;

}



/\* ─── Dyslexia-friendly reading panel ─── \*/

.reading-panel {

&#x20; background: var(--reading-bg, #f9f5e7);  /\* warm cream, not pure white \*/

&#x20; color: var(--reading-text, #333);        /\* not pure black \*/

&#x20; padding: var(--space-8) clamp(var(--space-6), 8vw, var(--space-16));

&#x20; border-radius: var(--radius-2xl);

}



/\* Wide line spacing \*/

.reading-panel p { line-height: 1.9; margin-block-end: 1.5em; }



/\* Paragraph alternating highlighting \*/

.reading-panel.bionic p:nth-child(even) {

&#x20; background: color-mix(in srgb, var(--reading-bg, #f9f5e7) 90%, #d4b483);

&#x20; padding: var(--space-1) var(--space-2);

&#x20; border-radius: var(--radius-sm);

}



/\* Bionic reading — bold first syllables (needs JS for text processing) \*/

.bionic-word b {

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-text);

}



.bionic-word {

&#x20; color: var(--color-text-muted);

}



/\* Reading ruler / focus line \*/

.reading-ruler {

&#x20; position: fixed;

&#x20; left: 0;

&#x20; right: 0;

&#x20; height: calc(1.9em \* 3);  /\* 3 lines \*/

&#x20; background: rgba(255 255 200 / 0.3);

&#x20; pointer-events: none;

&#x20; top: var(--ruler-y, 50%);

&#x20; translate: 0 -50%;

&#x20; z-index: var(--z-fixed);

&#x20; border-block: 1px solid rgba(200 180 0 / 0.2);

}



/\* ─── Reading preferences panel ─── \*/

.reading-prefs {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-5);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-4);

}



.reading-pref-row {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; gap: var(--space-4);

}



.reading-pref-label {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

}



/\* Font size slider \*/

.font-size-btns {

&#x20; display: flex;

&#x20; gap: var(--space-1);

}



.font-size-btn {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-surface);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: var(--font-weight-bold);

&#x20; transition: background var(--duration-fast);

}

.font-size-btn:hover { background: var(--color-bg-subtle); }

.font-size-btn.active { background: var(--color-accent); color: white; border-color: var(--color-accent); }



/\* Background color swatches \*/

.bg-swatches { display: flex; gap: var(--space-2); }



.bg-swatch {

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; border: 2px solid transparent;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}

.bg-swatch:hover { scale: 1.1; }

.bg-swatch.active { border-color: var(--color-text); }



.bg-swatch--white  { background: #ffffff; box-shadow: inset 0 0 0 1px #ddd; }

.bg-swatch--cream  { background: #f9f5e7; }

.bg-swatch--yellow { background: #fefce8; }

.bg-swatch--green  { background: #f0fdf4; }

.bg-swatch--blue   { background: #eff6ff; }

.bg-swatch--dark   { background: #1a1a1a; }

```



\---



\## 181. CUSTOM CURSORS



```css

/\* ─── Custom cursor system ─── \*/

/\* Apply via JS: document.documentElement.style.cursor = 'url(cursor.svg), auto' \*/



/\* CSS-based custom cursors using SVG data URLs \*/

:root {

&#x20; --cursor-default: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M5.5 3.21V20.8l4.19-4.19h9.06L5.5 3.21z' fill='white' stroke='black' stroke-width='1'/%3E%3C/svg%3E") 0 0, auto;



&#x20; --cursor-pointer: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M8 1v14l3-3h8L8 1z' fill='%233b82f6' stroke='white' stroke-width='1.5'/%3E%3C/svg%3E") 0 0, pointer;

}



/\* Large accessible cursor \*/

\[data-cursor="large"] \* { cursor: url("large-cursor.svg") 0 0, auto !important; }



/\* ─── CSS-only cursor following element ─── \*/

/\* JS: document.addEventListener('mousemove', e => {

&#x20;   document.documentElement.style.setProperty('--cx', e.clientX + 'px');

&#x20;   document.documentElement.style.setProperty('--cy', e.clientY + 'px');

}); \*/



.custom-cursor {

&#x20; position: fixed;

&#x20; top: 0;

&#x20; left: 0;

&#x20; pointer-events: none;

&#x20; z-index: 9999;

&#x20; translate: calc(var(--cx, 0px) - 50%) calc(var(--cy, 0px) - 50%);

&#x20; transition: translate 0.08s linear, scale 0.2s var(--ease-out), opacity 0.2s;

}



/\* Default dot cursor \*/

.custom-cursor\_\_dot {

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; background: var(--color-accent);

&#x20; border-radius: 50%;

&#x20; transition: scale 0.2s var(--ease-bounce), background 0.15s;

}



/\* Ring cursor \*/

.custom-cursor\_\_ring {

&#x20; position: fixed;

&#x20; top: 0;

&#x20; left: 0;

&#x20; width: 36px;

&#x20; height: 36px;

&#x20; border: 2px solid var(--color-accent);

&#x20; border-radius: 50%;

&#x20; pointer-events: none;

&#x20; z-index: 9998;

&#x20; translate: calc(var(--cx, 0px) - 50%) calc(var(--cy, 0px) - 50%);

&#x20; transition: translate 0.15s var(--ease-out), scale 0.3s var(--ease-bounce);

&#x20; mix-blend-mode: difference;

}



/\* Hover state — grow ring, shrink dot \*/

a:hover \~ .custom-cursor .custom-cursor\_\_dot,

button:hover \~ .custom-cursor .custom-cursor\_\_dot { scale: 3; background: transparent; border: 2px solid var(--color-accent); }



a:hover \~ .custom-cursor\_\_ring,

button:hover \~ .custom-cursor\_\_ring { scale: 0; }



/\* Text cursor \*/

.custom-cursor--text .custom-cursor\_\_dot {

&#x20; width: 2px;

&#x20; height: 1.2em;

&#x20; border-radius: 1px;

&#x20; animation: text-cursor-blink 1s step-end infinite;

}



@keyframes text-cursor-blink {

&#x20; 0%, 100% { opacity: 1; }

&#x20; 50%       { opacity: 0; }

}



/\* Grab cursor \*/

.custom-cursor--grab .custom-cursor\_\_dot {

&#x20; width: 24px;

&#x20; height: 24px;

&#x20; background: url("data:image/svg+xml,...") center / contain no-repeat;

&#x20; background-color: transparent;

}



/\* Cursor trail \*/

.cursor-trail {

&#x20; position: fixed;

&#x20; width: 6px;

&#x20; height: 6px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; pointer-events: none;

&#x20; z-index: 9997;

&#x20; opacity: 0;

&#x20; animation: trail-fade 0.5s ease-out forwards;

&#x20; translate: var(--tx, 0) var(--ty, 0);

}



@keyframes trail-fade {

&#x20; from { opacity: 0.6; scale: 1; }

&#x20; to   { opacity: 0; scale: 0.2; }

}

```



\---

<br>



```

╔══════════════════════════════════════════════════════════════════════╗

║                     PART 12 — COMPLETE                               ║

║  Chapters 169–181 | 13 new chapters | Output: css-guide-part12.md   ║

╚══════════════════════════════════════════════════════════════════════╝

```

