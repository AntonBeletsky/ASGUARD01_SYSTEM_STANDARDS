# CSS GUIDE — PART 12
## Chapters 169–184

---

## 169. RADAR / SPIDER CHART

```css
/* ─── CSS-only radar chart using clip-path + conic-gradient ─── */
.radar-chart {
  position: relative;
  width: 280px;
  height: 280px;
  display: grid;
  place-items: center;
}

/* Background polygon levels */
.radar-grid {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
}

.radar-level {
  position: absolute;
  width: calc(var(--level, 1) * 20%);
  height: calc(var(--level, 1) * 20%);
  border: 1px solid var(--color-border);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  /* 6-sided: adjust for different axis counts */
}

/* Axis lines */
.radar-axis {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 50%;
  height: 1px;
  background: var(--color-border);
  transform-origin: left center;
  transform: rotate(var(--angle, 0deg));
}

/* Data polygon */
.radar-data {
  position: absolute;
  inset: 0;
  clip-path: polygon(
    /* JS calculates each point: (50% + r*sin(angle), 50% - r*cos(angle)) */
    var(--p1, 50% 10%),
    var(--p2, 90% 33%),
    var(--p3, 76% 80%),
    var(--p4, 24% 80%),
    var(--p5, 10% 33%),
    var(--p6, 50% 10%)
  );
  background: color-mix(in srgb, var(--color-accent) 25%, transparent);
  border: 2px solid var(--color-accent);
}

/* Labels */
.radar-label {
  position: absolute;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  white-space: nowrap;
  transform: translate(-50%, -50%);
  left: var(--lx, 50%);
  top:  var(--ly, 5%);
}

/* Value dots */
.radar-dot {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  border: 2px solid white;
  box-shadow: var(--shadow-sm);
  translate: -50% -50%;
  left: var(--dx, 50%);
  top:  var(--dy, 50%);
  cursor: pointer;
  transition: scale var(--duration-fast) var(--ease-bounce);
}
.radar-dot:hover { scale: 1.5; }

/* Tooltip on dot */
.radar-dot::after {
  content: attr(data-value);
  position: absolute;
  bottom: 120%;
  left: 50%;
  translate: -50% 0;
  background: var(--color-neutral-900);
  color: white;
  font-size: var(--font-size-xs);
  padding: 0.2em 0.5em;
  border-radius: var(--radius-md);
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--duration-fast);
}
.radar-dot:hover::after { opacity: 1; }

/* Multiple datasets */
.radar-data--secondary {
  clip-path: polygon(var(--q1), var(--q2), var(--q3), var(--q4), var(--q5), var(--q6));
  background: color-mix(in srgb, var(--color-success-500) 20%, transparent);
  border-color: var(--color-success-500);
}

/* Legend */
.radar-legend {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
  margin-block-start: var(--space-4);
  font-size: var(--font-size-xs);
}

.radar-legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.radar-legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--legend-color, var(--color-accent));
}
```

---

## 170. AREA & LINE CHART (CSS)

```css
/* ─── SVG-based line/area chart with CSS styling ─── */
.line-chart-container {
  position: relative;
  width: 100%;
  padding-block-end: var(--space-6);
}

/* Chart SVG styling */
.chart-svg {
  overflow: visible;
  width: 100%;
  height: auto;
}

/* Grid lines */
.chart-grid-line {
  stroke: var(--color-border);
  stroke-width: 1;
  stroke-dasharray: 4 4;
}

/* X/Y axis */
.chart-axis {
  stroke: var(--color-border-strong);
  stroke-width: 1.5;
  fill: none;
}

/* Area fill */
.chart-area {
  fill: color-mix(in srgb, var(--color-accent) 15%, transparent);
  transition: fill var(--duration-normal);
}

/* Line */
.chart-line {
  fill: none;
  stroke: var(--color-accent);
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
  /* Animate draw-on */
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: draw-line 1.5s var(--ease-out) forwards;
}

@keyframes draw-line {
  to { stroke-dashoffset: 0; }
}

/* Data points */
.chart-dot {
  fill: white;
  stroke: var(--color-accent);
  stroke-width: 2;
  cursor: pointer;
  transition: r var(--duration-fast) var(--ease-bounce);
}
.chart-dot:hover { r: 6; }

/* Labels */
.chart-label {
  font-size: 11px;
  fill: var(--color-text-muted);
  font-family: var(--font-sans);
}

.chart-value-label {
  font-size: 11px;
  fill: var(--color-text);
  font-weight: 600;
  font-family: var(--font-sans);
}

/* Tooltip crosshair */
.chart-crosshair {
  stroke: var(--color-text-muted);
  stroke-width: 1;
  stroke-dasharray: 4 2;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--duration-fast);
}

.chart-svg:hover .chart-crosshair { opacity: 1; }

/* Tooltip */
.chart-tooltip {
  position: absolute;
  background: var(--color-neutral-900);
  color: white;
  border-radius: var(--radius-lg);
  padding: var(--space-3);
  font-size: var(--font-size-xs);
  pointer-events: none;
  translate: -50% calc(-100% - 10px);
  opacity: 0;
  transition: opacity var(--duration-fast);
  min-width: 100px;
  box-shadow: var(--shadow-xl);
  z-index: 10;
}

.chart-tooltip.visible { opacity: 1; }

.chart-tooltip__date {
  color: rgba(255 255 255 / 0.6);
  margin-block-end: var(--space-1);
}

.chart-tooltip__value {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
}

/* Multi-series colors */
.chart-line--2 { stroke: var(--color-success-500); }
.chart-area--2 { fill: color-mix(in srgb, var(--color-success-500) 12%, transparent); }
.chart-line--3 { stroke: var(--color-warning-500); }
.chart-area--3 { fill: color-mix(in srgb, var(--color-warning-500) 12%, transparent); }

/* Stacked area */
.chart-area-stacked { fill-opacity: 0.6; }
```

---

## 171. MIND MAP

```css
/* ─── Mind map layout ─── */
.mindmap {
  position: relative;
  width: 100%;
  height: 600px;
  overflow: auto;
  background: var(--color-bg-subtle);
  cursor: grab;
}
.mindmap.panning { cursor: grabbing; }

.mindmap-viewport {
  position: absolute;
  top: 0;
  left: 0;
  transform: translate(var(--pan-x, 0px), var(--pan-y, 0px)) scale(var(--zoom, 1));
  transform-origin: top left;
  will-change: transform;
}

/* Central node */
.mindmap-root {
  position: absolute;
  background: var(--color-accent);
  color: white;
  border-radius: var(--radius-2xl);
  padding: var(--space-3) var(--space-6);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-lg);
  box-shadow: var(--shadow-lg);
  white-space: nowrap;
  cursor: pointer;
  z-index: 2;
  transition: scale var(--duration-fast) var(--ease-bounce), box-shadow var(--duration-fast);
  left: var(--x, 0);
  top:  var(--y, 0);
  translate: -50% -50%;
}
.mindmap-root:hover { scale: 1.05; box-shadow: var(--shadow-xl); }

/* Branch node */
.mindmap-node {
  position: absolute;
  background: var(--color-surface);
  border: 2px solid var(--node-color, var(--color-border));
  border-radius: var(--radius-xl);
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  z-index: 2;
  white-space: nowrap;
  transition:
    scale      var(--duration-fast) var(--ease-bounce),
    box-shadow var(--duration-fast),
    background var(--duration-fast);
  left: var(--x, 0);
  top:  var(--y, 0);
  translate: -50% -50%;
}
.mindmap-node:hover {
  background: var(--color-bg-subtle);
  scale: 1.05;
  box-shadow: var(--shadow-md);
}

.mindmap-node.selected {
  background: color-mix(in srgb, var(--node-color, var(--color-accent)) 10%, var(--color-surface));
  border-color: var(--node-color, var(--color-accent));
}

/* Level colors */
.mindmap-node[data-level="1"] { --node-color: var(--color-brand-500); }
.mindmap-node[data-level="2"] { --node-color: var(--color-success-500); }
.mindmap-node[data-level="3"] { --node-color: var(--color-warning-500); }
.mindmap-node[data-level="4"] { --node-color: var(--color-danger-400); }

/* Connection SVG */
.mindmap-connections {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.mindmap-edge {
  fill: none;
  stroke: var(--edge-color, var(--color-border));
  stroke-width: 2;
  stroke-linecap: round;
  opacity: 0.7;
}

.mindmap-edge--level-1 { --edge-color: var(--color-brand-300); stroke-width: 2.5; }
.mindmap-edge--level-2 { --edge-color: var(--color-success-300); }
.mindmap-edge--level-3 { --edge-color: var(--color-warning-300); }

/* Collapse button */
.mindmap-collapse {
  position: absolute;
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  background: var(--color-surface);
  border: 1.5px solid var(--color-border);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem;
  color: var(--color-text-muted);
  z-index: 3;
  transition: background var(--duration-fast);
  left: var(--cx, 0);
  top:  var(--cy, 0);
  translate: -50% -50%;
}
.mindmap-collapse:hover { background: var(--color-bg-muted); }

/* Add node button */
.mindmap-add {
  position: absolute;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--color-accent);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
  z-index: 3;
}
.mindmap-node:hover ~ .mindmap-add,
.mindmap-add:hover { opacity: 1; scale: 1.1; }
```

---

## 172. COUNTDOWN TIMER

```css
/* ─── Countdown timer card ─── */
.countdown {
  display: flex;
  gap: var(--space-4);
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

.countdown-unit {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
}

.countdown-value {
  position: relative;
  width: 80px;
  height: 80px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.25rem;
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
  font-family: var(--font-mono);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

/* Flip animation on change */
.countdown-value.flipping {
  animation: flip-digit 0.4s ease-in-out;
}

@keyframes flip-digit {
  0%   { transform: rotateX(0deg); }
  50%  { transform: rotateX(90deg); }
  100% { transform: rotateX(0deg); }
}

/* Separator */
.countdown-sep {
  font-size: 2rem;
  font-weight: var(--font-weight-black);
  color: var(--color-text-muted);
  padding-block-end: var(--space-5);
  line-height: 1;
}

.countdown-label {
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
}

/* Urgent state */
.countdown.urgent .countdown-value {
  border-color: var(--color-danger-300);
  color: var(--color-danger-600);
  animation: urgent-pulse 1s ease-in-out infinite;
}

@keyframes urgent-pulse {
  0%, 100% { box-shadow: var(--shadow-md); }
  50%       { box-shadow: 0 0 0 4px color-mix(in srgb, var(--color-danger-500) 20%, transparent); }
}

/* Dark variant */
.countdown--dark .countdown-value {
  background: var(--color-neutral-900);
  color: white;
  border-color: var(--color-neutral-700);
}

/* Circular variant */
.countdown--circle .countdown-value {
  border-radius: 50%;
  width: 90px;
  height: 90px;
  position: relative;
}

.countdown--circle .countdown-value svg {
  position: absolute;
  inset: -4px;
  width: calc(100% + 8px);
  height: calc(100% + 8px);
  rotate: -90deg;
}

.countdown-ring {
  fill: none;
  stroke: var(--color-bg-muted);
  stroke-width: 4;
}

.countdown-ring-fill {
  fill: none;
  stroke: var(--color-accent);
  stroke-width: 4;
  stroke-linecap: round;
  stroke-dasharray: 251; /* 2π×40 */
  stroke-dashoffset: calc(251 - 251 * var(--progress, 0));
  transition: stroke-dashoffset 0.9s linear;
}

/* Inline mini countdown */
.countdown-inline {
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
  font-variant-numeric: tabular-nums;
  font-family: var(--font-mono);
  font-weight: var(--font-weight-bold);
  color: var(--color-danger-500);
  background: var(--color-danger-100);
  padding: 0.2em 0.6em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
}

/* Progress bar countdown */
.countdown-bar {
  width: 100%;
  height: 6px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.countdown-bar__fill {
  height: 100%;
  background: var(--color-accent);
  width: var(--progress, 100%);
  border-radius: inherit;
  transition: width 1s linear, background 0.3s;
}

.countdown-bar__fill[style*="--progress: 2"] { background: var(--color-danger-500); }
.countdown-bar__fill[style*="--progress: 1"] { background: var(--color-danger-500); }
```

---

## 173. EMOJI PICKER

```css
/* ─── Emoji picker panel ─── */
.emoji-picker {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  width: 320px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 400px;
  animation: picker-appear 0.15s var(--ease-out);
}

@keyframes picker-appear {
  from { opacity: 0; scale: 0.95; translate: 0 6px; }
}

/* Search */
.emoji-search {
  padding: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.emoji-search__input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font: inherit;
  font-size: var(--font-size-sm);
  background: var(--color-bg-subtle);
  outline: none;
  transition: border-color var(--duration-fast);
}
.emoji-search__input:focus { border-color: var(--color-accent); }

/* Category tabs */
.emoji-tabs {
  display: flex;
  overflow-x: auto;
  scrollbar-width: none;
  padding-inline: var(--space-2);
  gap: 2px;
  border-bottom: 1px solid var(--color-border);
  padding-block: var(--space-1);
}
.emoji-tabs::-webkit-scrollbar { display: none; }

.emoji-tab {
  flex-shrink: 0;
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--duration-fast);
  position: relative;
}
.emoji-tab:hover { background: var(--color-bg-subtle); }
.emoji-tab.active { background: var(--color-bg-muted); }
.emoji-tab.active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 50%;
  translate: -50% 0;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--color-accent);
}

/* Emoji grid */
.emoji-body {
  overflow-y: auto;
  flex: 1;
  padding: var(--space-2) var(--space-3);
  scrollbar-width: thin;
}

.emoji-section-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  margin-block: var(--space-2);
  padding-inline: var(--space-1);
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 2px;
}

.emoji-btn {
  width: 2.25rem;
  height: 2.25rem;
  border: none;
  background: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition:
    background var(--duration-fast),
    scale      var(--duration-fast) var(--ease-bounce);
  position: relative;
}
.emoji-btn:hover { background: var(--color-bg-subtle); scale: 1.3; }
.emoji-btn:active { scale: 1.1; }

/* Skin tone modifier */
.emoji-btn.has-variants::after {
  content: '';
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--color-text-muted);
  opacity: 0.5;
}

/* Footer: recent + skin tone */
.emoji-footer {
  padding: var(--space-2) var(--space-3);
  border-top: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.skin-tones {
  display: flex;
  gap: 4px;
}

.skin-tone-btn {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: scale var(--duration-fast) var(--ease-bounce), border-color var(--duration-fast);
}
.skin-tone-btn:hover { scale: 1.2; }
.skin-tone-btn.selected { border-color: var(--color-text); }

.skin-tone-btn[data-tone="1"] { background: #ffd83d; }
.skin-tone-btn[data-tone="2"] { background: #ffcd96; }
.skin-tone-btn[data-tone="3"] { background: #e0a86c; }
.skin-tone-btn[data-tone="4"] { background: #b97836; }
.skin-tone-btn[data-tone="5"] { background: #8a5018; }
.skin-tone-btn[data-tone="6"] { background: #4a2c0e; }
```

---

## 174. FILE UPLOAD QUEUE

```css
/* ─── Upload queue list ─── */
.upload-queue {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.upload-item {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-3) var(--space-4);
  display: grid;
  grid-template-columns: 2.5rem 1fr auto;
  gap: var(--space-3);
  align-items: center;
  animation: upload-item-in 0.2s var(--ease-out);
}

@keyframes upload-item-in {
  from { opacity: 0; translate: 0 -8px; }
}

.upload-item.removing {
  animation: upload-item-out 0.2s var(--ease-in) forwards;
}

@keyframes upload-item-out {
  to { opacity: 0; translate: 0 -4px; height: 0; margin: 0; padding: 0; overflow: hidden; }
}

/* File icon */
.upload-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.upload-icon--image  { background: var(--color-brand-100); }
.upload-icon--pdf    { background: var(--color-danger-100); }
.upload-icon--doc    { background: var(--color-brand-100); }
.upload-icon--sheet  { background: var(--color-success-100); }
.upload-icon--zip    { background: var(--color-warning-100); }
.upload-icon--video  { background: oklch(0.93 0.05 290); }
.upload-icon--audio  { background: oklch(0.93 0.05 320); }
.upload-icon--other  { background: var(--color-bg-muted); }

/* Upload info */
.upload-info { min-width: 0; }

.upload-name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-block-end: var(--space-1);
}

.upload-meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.upload-size { font-variant-numeric: tabular-nums; }

/* Progress bar */
.upload-progress {
  height: 4px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
  margin-block-start: var(--space-2);
}

.upload-progress__fill {
  height: 100%;
  border-radius: inherit;
  background: var(--color-accent);
  width: var(--progress, 0%);
  transition: width 0.3s var(--ease-out);
}

.upload-progress__fill--error { background: var(--color-danger-500); }
.upload-progress__fill--done  { background: var(--color-success-500); }

/* Status */
.upload-status {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  gap: 0.25em;
}

.upload-status--uploading { color: var(--color-accent); }
.upload-status--done      { color: var(--color-success-600); }
.upload-status--error     { color: var(--color-danger-500); }
.upload-status--paused    { color: var(--color-warning-600); }

/* Action buttons */
.upload-actions {
  display: flex;
  gap: var(--space-1);
  flex-shrink: 0;
}

.upload-action-btn {
  width: 1.75rem;
  height: 1.75rem;
  border: none;
  background: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.upload-action-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }
.upload-action-btn.danger:hover { background: var(--color-danger-100); color: var(--color-danger-600); }

/* Queue summary */
.upload-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3);
  background: var(--color-bg-subtle);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
}

.upload-summary__total { color: var(--color-text-muted); }
.upload-summary__speed { font-variant-numeric: tabular-nums; font-weight: var(--font-weight-medium); }
```

---

## 175. VIDEO CALL UI

```css
/* ─── Video call layout ─── */
.video-call {
  position: fixed;
  inset: 0;
  background: #0f0f0f;
  display: grid;
  grid-template-rows: 1fr auto;
  overflow: hidden;
}

/* Main video grid */
.call-grid {
  position: relative;
  flex: 1;
  display: grid;
  gap: 4px;
  padding: 4px;
  overflow: hidden;
}

/* 1 participant */
.call-grid[data-participants="1"] { grid-template-columns: 1fr; }
/* 2 participants */
.call-grid[data-participants="2"] { grid-template-columns: 1fr 1fr; }
/* 3-4 participants */
.call-grid[data-participants="3"],
.call-grid[data-participants="4"] {
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}
/* 5-6 */
.call-grid[data-participants="5"],
.call-grid[data-participants="6"] {
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 1fr 1fr;
}

/* Participant tile */
.call-tile {
  position: relative;
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

.call-tile video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Video off state */
.call-tile--no-video {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2a2a3e, #1a1a2e);
}

.call-tile__avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255 255 255 / 0.2);
}

/* Name label */
.call-tile__name {
  position: absolute;
  bottom: var(--space-2);
  left: var(--space-2);
  background: rgba(0 0 0 / 0.6);
  color: white;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  padding: 0.2em 0.6em;
  border-radius: var(--radius-md);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  gap: 0.375rem;
  max-width: calc(100% - var(--space-4));
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Muted mic indicator */
.call-tile__muted {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
  width: 1.75rem;
  height: 1.75rem;
  background: var(--color-danger-500);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: white;
}

/* Speaking indicator */
.call-tile.speaking {
  outline: 3px solid var(--color-success-400);
  outline-offset: -3px;
}

/* Active speaker large view */
.call-tile.pinned {
  grid-column: 1 / -1;
  grid-row: 1 / -1;
}

/* Hand raised */
.call-tile__hand {
  position: absolute;
  top: var(--space-2);
  left: var(--space-2);
  font-size: 1.25rem;
  animation: hand-wave 1s ease-in-out infinite;
}
@keyframes hand-wave {
  0%, 100% { rotate: 0deg; }
  25%       { rotate: 20deg; }
  75%       { rotate: -10deg; }
}

/* Self tile (always bottom-right) */
.call-tile--self {
  position: absolute;
  bottom: var(--space-4);
  right: var(--space-4);
  width: 160px;
  height: 90px;
  border-radius: var(--radius-lg);
  border: 2px solid rgba(255 255 255 / 0.2);
  overflow: hidden;
  z-index: 5;
  cursor: move;
  box-shadow: var(--shadow-xl);
}

/* Bottom controls bar */
.call-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-6);
  background: rgba(0 0 0 / 0.8);
  backdrop-filter: blur(20px);
}

.call-btn {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  color: white;
  background: rgba(255 255 255 / 0.15);
  transition:
    background  var(--duration-fast),
    scale       var(--duration-fast) var(--ease-bounce);
}
.call-btn:hover { background: rgba(255 255 255 / 0.25); scale: 1.05; }

.call-btn--active { background: rgba(255 255 255 / 0.9); color: #0f0f0f; }
.call-btn--danger { background: var(--color-danger-500); }
.call-btn--danger:hover { background: var(--color-danger-600); }
.call-btn--end { width: 3.5rem; height: 3.5rem; font-size: 1.25rem; }

/* Participants panel */
.call-participants-panel {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 280px;
  background: rgba(15 15 15 / 0.95);
  backdrop-filter: blur(20px);
  border-left: 1px solid rgba(255 255 255 / 0.1);
  display: flex;
  flex-direction: column;
  z-index: 10;
  animation: panel-slide 0.3s var(--ease-out);
}

@keyframes panel-slide {
  from { translate: 100% 0; }
}

.call-participant-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid rgba(255 255 255 / 0.05);
  color: white;
}

.call-participant-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.call-participant-name {
  flex: 1;
  font-size: var(--font-size-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.call-participant-status {
  display: flex;
  gap: var(--space-1);
  font-size: 0.75rem;
  opacity: 0.6;
}
```

---

## 176. REAL-TIME COLLABORATION CURSORS

```css
/* ─── Multi-user cursor indicators ─── */
.collab-cursor {
  position: fixed;
  pointer-events: none;
  z-index: var(--z-top);
  translate: var(--cx, 0px) var(--cy, 0px);
  transition: translate 0.08s linear;
  will-change: translate;
}

/* Cursor SVG arrow */
.collab-cursor__arrow {
  width: 20px;
  height: 20px;
  filter: drop-shadow(0 1px 2px rgb(0 0 0 / 0.3));
  fill: var(--user-color, #3b82f6);
  stroke: white;
  stroke-width: 1.5;
}

/* Name label */
.collab-cursor__label {
  position: absolute;
  top: 18px;
  left: 12px;
  background: var(--user-color, #3b82f6);
  color: white;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: 0.2em 0.5em;
  border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md);
  white-space: nowrap;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Away/idle cursor */
.collab-cursor.idle .collab-cursor__arrow {
  opacity: 0.5;
}

.collab-cursor.idle .collab-cursor__label::after {
  content: ' (idle)';
  opacity: 0.7;
}

/* Click ripple */
.collab-cursor.clicking::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  border: 2px solid var(--user-color, #3b82f6);
  border-radius: 50%;
  animation: cursor-click 0.4s ease-out forwards;
}

@keyframes cursor-click {
  from { scale: 1; opacity: 0.8; }
  to   { scale: 3; opacity: 0; }
}

/* ─── User presence avatars (top bar) ─── */
.presence-bar {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.presence-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 2px solid var(--user-color, var(--color-accent));
  cursor: pointer;
  position: relative;
  transition: scale var(--duration-fast) var(--ease-bounce), z-index 0s;
}
.presence-avatar:hover { scale: 1.2; z-index: 1; }

/* Active/viewing indicator */
.presence-avatar.active::before {
  content: '';
  position: absolute;
  inset: -3px;
  border: 2px solid var(--user-color, var(--color-accent));
  border-radius: 50%;
  animation: presence-pulse 2s ease-in-out infinite;
}

@keyframes presence-pulse {
  0%, 100% { opacity: 0.8; scale: 1; }
  50%       { opacity: 0; scale: 1.5; }
}

/* Selection highlight overlay */
.collab-selection {
  position: absolute;
  background: color-mix(in srgb, var(--user-color, #3b82f6) 20%, transparent);
  border: 1px solid color-mix(in srgb, var(--user-color, #3b82f6) 50%, transparent);
  border-radius: 2px;
  pointer-events: none;
}

/* Typing indicator in shared doc */
.collab-typing {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 6px;
  background: var(--user-color, #3b82f6);
  border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md);
  position: absolute;
}

.collab-typing span {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: white;
  animation: typing-dot 1.2s ease-in-out infinite;
}
.collab-typing span:nth-child(2) { animation-delay: 0.15s; }
.collab-typing span:nth-child(3) { animation-delay: 0.3s; }

@keyframes typing-dot {
  0%, 60%, 100% { opacity: 0.3; scale: 0.8; }
  30%           { opacity: 1; scale: 1; }
}
```

---

## 177. CHANGELOG / RELEASE NOTES

```css
/* ─── Changelog page ─── */
.changelog {
  max-width: 720px;
  margin-inline: auto;
  padding: var(--space-8) var(--space-4);
}

/* Version entry */
.changelog-entry {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: var(--space-8);
  padding-block: var(--space-8);
  border-bottom: 1px solid var(--color-border);
  position: relative;
}

.changelog-entry:last-child { border: none; }

@media (max-width: 600px) {
  .changelog-entry { grid-template-columns: 1fr; gap: var(--space-4); }
  .changelog-sidebar { flex-direction: row; align-items: center; }
}

/* Timeline line */
.changelog-entry::before {
  content: '';
  position: absolute;
  left: 179px;
  top: 0;
  bottom: 0;
  width: 1px;
  background: var(--color-border);
}

@media (max-width: 600px) {
  .changelog-entry::before { display: none; }
}

/* Sidebar: date + version */
.changelog-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding-block-start: var(--space-2);
  position: relative;
}

/* Timeline dot */
.changelog-sidebar::after {
  content: '';
  position: absolute;
  right: calc(-var(--space-8) / 2 - 4.5px);
  top: var(--space-3);
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--color-accent);
  border: 2px solid var(--color-surface);
  box-shadow: 0 0 0 2px var(--color-accent);
}

@media (max-width: 600px) {
  .changelog-sidebar::after { display: none; }
}

.changelog-version {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-black);
  font-family: var(--font-mono);
  color: var(--color-text);
}

.changelog-date {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-medium);
}

.changelog-badge {
  display: inline-flex;
  padding: 0.2em 0.6em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  width: fit-content;
}

.changelog-badge--major   { background: var(--color-danger-100); color: var(--color-danger-700); }
.changelog-badge--minor   { background: var(--color-brand-100); color: var(--color-brand-700); }
.changelog-badge--patch   { background: var(--color-bg-muted); color: var(--color-text-muted); }
.changelog-badge--beta    { background: var(--color-warning-100); color: var(--color-warning-700); }
.changelog-badge--latest  { background: var(--color-success-100); color: var(--color-success-700); }

/* Content */
.changelog-content { }

.changelog-content h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-4);
  color: var(--color-text);
}

/* Change categories */
.changelog-category {
  margin-block-end: var(--space-4);
}

.changelog-category-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  margin-block-end: var(--space-2);
}

/* Category type indicators */
.changelog-category--added .changelog-category-title     { color: var(--color-success-600); }
.changelog-category--changed .changelog-category-title   { color: var(--color-brand-600); }
.changelog-category--fixed .changelog-category-title     { color: var(--color-warning-600); }
.changelog-category--removed .changelog-category-title   { color: var(--color-danger-600); }
.changelog-category--deprecated .changelog-category-title { color: var(--color-neutral-500); }
.changelog-category--security .changelog-category-title  { color: var(--color-danger-700); }

.changelog-category-icon {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem;
}

.changelog-category--added .changelog-category-icon     { background: var(--color-success-100); }
.changelog-category--changed .changelog-category-icon   { background: var(--color-brand-100); }
.changelog-category--fixed .changelog-category-icon     { background: var(--color-warning-100); }
.changelog-category--removed .changelog-category-icon   { background: var(--color-danger-100); }

/* Change items */
.changelog-items {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.changelog-item {
  font-size: var(--font-size-sm);
  color: var(--color-text);
  padding-inline-start: 1em;
  position: relative;
  line-height: 1.5;
}

.changelog-item::before {
  content: '–';
  position: absolute;
  left: 0;
  color: var(--color-text-muted);
}

.changelog-item code {
  font-family: var(--font-mono);
  font-size: 0.85em;
  background: var(--color-bg-muted);
  padding: 0.1em 0.3em;
  border-radius: var(--radius-sm);
}

/* PR/Issue links */
.changelog-item a {
  color: var(--color-accent);
  text-decoration: none;
  font-size: 0.85em;
  font-family: var(--font-mono);
}
.changelog-item a:hover { text-decoration: underline; }
```

---

## 178. ROADMAP UI

```css
/* ─── Product roadmap ─── */
.roadmap {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
  gap: var(--space-4);
}

/* Column */
.roadmap-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.roadmap-col__header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding-block-end: var(--space-3);
  border-bottom: 2px solid var(--col-color, var(--color-border));
}

.roadmap-col__title {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-sm);
  flex: 1;
}

.roadmap-col__count {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  background: var(--color-bg-muted);
  padding: 0.15em 0.5em;
  border-radius: var(--radius-full);
  font-variant-numeric: tabular-nums;
  font-weight: var(--font-weight-semibold);
}

/* Column phases */
.roadmap-col--planned  { --col-color: var(--color-neutral-400); }
.roadmap-col--progress { --col-color: var(--color-brand-500); }
.roadmap-col--review   { --col-color: var(--color-warning-500); }
.roadmap-col--done     { --col-color: var(--color-success-500); }

/* Roadmap card */
.roadmap-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
  cursor: pointer;
  transition:
    box-shadow  var(--duration-fast),
    translate   var(--duration-fast);
  border-top: 3px solid var(--card-color, var(--color-border));
}

.roadmap-card:hover {
  box-shadow: var(--shadow-md);
  translate: 0 -1px;
}

.roadmap-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-block-end: var(--space-2);
}

.roadmap-tag {
  padding: 0.1em 0.5em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
}

.roadmap-card__title {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  line-height: 1.4;
  margin-block-end: var(--space-2);
}

.roadmap-card__desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  line-height: 1.5;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.roadmap-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-block-start: var(--space-3);
  padding-block-start: var(--space-3);
  border-top: 1px solid var(--color-border);
}

.roadmap-card__votes {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0.2em 0.5em;
  border-radius: var(--radius-md);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.roadmap-card__votes:hover { background: var(--color-brand-100); color: var(--color-brand-600); }
.roadmap-card__votes.voted { color: var(--color-accent); font-weight: var(--font-weight-semibold); }

.roadmap-card__quarter {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-medium);
}

/* Quarter header (timeline view) */
.roadmap-quarter {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  padding: var(--space-2) 0;
  border-bottom: 1px solid var(--color-border);
  margin-block-end: var(--space-3);
}
```

---

## 179. QUIZ / EDUCATIONAL UI

```css
/* ─── Quiz question card ─── */
.quiz {
  max-width: 680px;
  margin-inline: auto;
  padding: var(--space-4);
}

.quiz-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin-block-end: var(--space-6);
}

.quiz-progress-bar {
  flex: 1;
  height: 8px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.quiz-progress-bar__fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: inherit;
  width: var(--quiz-progress, 0%);
  transition: width 0.4s var(--ease-out);
}

.quiz-question-num {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-medium);
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.quiz-timer {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-family: var(--font-mono);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-sm);
  font-variant-numeric: tabular-nums;
  color: var(--timer-color, var(--color-text-muted));
}

.quiz-timer.warning { --timer-color: var(--color-danger-500); animation: timer-pulse 1s ease-in-out infinite; }
@keyframes timer-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}

/* Question */
.quiz-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-8);
  margin-block-end: var(--space-4);
  animation: question-enter 0.3s var(--ease-out);
}

@keyframes question-enter {
  from { opacity: 0; translate: 20px 0; }
}

.quiz-category {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-accent);
  margin-block-end: var(--space-3);
}

.quiz-question {
  font-size: clamp(1rem, 2vw + 0.5rem, 1.25rem);
  font-weight: var(--font-weight-semibold);
  line-height: 1.5;
  margin-block-end: var(--space-6);
  text-wrap: pretty;
}

.quiz-image {
  width: 100%;
  border-radius: var(--radius-lg);
  margin-block-end: var(--space-4);
}

/* Answer options */
.quiz-options {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.quiz-option {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-4);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-xl);
  cursor: pointer;
  transition:
    border-color var(--duration-fast),
    background   var(--duration-fast),
    scale        var(--duration-fast) var(--ease-bounce);
  user-select: none;
}

.quiz-option:hover {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 5%, transparent);
}

.quiz-option.selected {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 8%, transparent);
  scale: 1.01;
}

/* Answer reveal states */
.quiz-option.correct {
  border-color: var(--color-success-500);
  background: var(--color-success-100);
  animation: correct-flash 0.4s var(--ease-out);
}

.quiz-option.wrong {
  border-color: var(--color-danger-500);
  background: var(--color-danger-100);
  animation: wrong-shake 0.4s var(--ease-out);
}

@keyframes correct-flash {
  0%   { scale: 0.98; }
  50%  { scale: 1.02; }
  100% { scale: 1; }
}

@keyframes wrong-shake {
  0%, 100% { translate: 0; }
  25%       { translate: -6px; }
  75%       { translate: 6px; }
}

/* Option letter badge */
.quiz-option__letter {
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-md);
  background: var(--color-bg-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-sm);
  flex-shrink: 0;
  transition: background var(--duration-fast), color var(--duration-fast);
}

.quiz-option.selected .quiz-option__letter  { background: var(--color-accent); color: white; }
.quiz-option.correct .quiz-option__letter   { background: var(--color-success-500); color: white; }
.quiz-option.wrong .quiz-option__letter     { background: var(--color-danger-500); color: white; }

.quiz-option__text {
  flex: 1;
  font-size: var(--font-size-sm);
  line-height: 1.5;
}

/* Explanation */
.quiz-explanation {
  margin-block-start: var(--space-4);
  padding: var(--space-4);
  background: var(--color-bg-subtle);
  border-radius: var(--radius-lg);
  border-inline-start: 3px solid var(--color-accent);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.6;
  animation: fade-in 0.3s var(--ease-out);
}

@keyframes fade-in { from { opacity: 0; translate: 0 8px; } }

.quiz-explanation__title {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin-block-end: var(--space-2);
}

/* Results screen */
.quiz-results {
  text-align: center;
  padding: var(--space-10);
}

.quiz-score {
  font-size: clamp(3rem, 10vw, 6rem);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
  line-height: 1;
  background: linear-gradient(135deg, var(--color-accent), var(--color-brand-300));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: score-in 0.8s var(--spring-bouncy) forwards;
}

@keyframes score-in {
  from { scale: 0; opacity: 0; }
}

.quiz-grade {
  font-size: var(--step-1);
  font-weight: var(--font-weight-bold);
  margin-block: var(--space-2);
}
```

---

## 180. DYSLEXIA-FRIENDLY TYPOGRAPHY

```css
/* ─── Accessible reading mode for dyslexia ─── */
[data-reading-mode="dyslexia"] {
  /* Recommended fonts for dyslexia */
  font-family: 'OpenDyslexic', 'Lexie Readable', Verdana, Geneva, Tahoma, sans-serif;

  /* Increased spacing */
  letter-spacing: 0.12em;
  word-spacing: 0.25em;
  line-height: 1.9;

  /* Left-aligned (never justify) */
  text-align: left;

  /* Prevent auto-hyphenation */
  hyphens: none;
  -webkit-hyphens: none;

  /* No italics (harder to read) */
  font-style: normal;
}

/* ─── Dyslexia-friendly reading panel ─── */
.reading-panel {
  background: var(--reading-bg, #f9f5e7);  /* warm cream, not pure white */
  color: var(--reading-text, #333);        /* not pure black */
  padding: var(--space-8) clamp(var(--space-6), 8vw, var(--space-16));
  border-radius: var(--radius-2xl);
}

/* Wide line spacing */
.reading-panel p { line-height: 1.9; margin-block-end: 1.5em; }

/* Paragraph alternating highlighting */
.reading-panel.bionic p:nth-child(even) {
  background: color-mix(in srgb, var(--reading-bg, #f9f5e7) 90%, #d4b483);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
}

/* Bionic reading — bold first syllables (needs JS for text processing) */
.bionic-word b {
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}

.bionic-word {
  color: var(--color-text-muted);
}

/* Reading ruler / focus line */
.reading-ruler {
  position: fixed;
  left: 0;
  right: 0;
  height: calc(1.9em * 3);  /* 3 lines */
  background: rgba(255 255 200 / 0.3);
  pointer-events: none;
  top: var(--ruler-y, 50%);
  translate: 0 -50%;
  z-index: var(--z-fixed);
  border-block: 1px solid rgba(200 180 0 / 0.2);
}

/* ─── Reading preferences panel ─── */
.reading-prefs {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.reading-pref-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}

.reading-pref-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

/* Font size slider */
.font-size-btns {
  display: flex;
  gap: var(--space-1);
}

.font-size-btn {
  width: 2rem;
  height: 2rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-bold);
  transition: background var(--duration-fast);
}
.font-size-btn:hover { background: var(--color-bg-subtle); }
.font-size-btn.active { background: var(--color-accent); color: white; border-color: var(--color-accent); }

/* Background color swatches */
.bg-swatches { display: flex; gap: var(--space-2); }

.bg-swatch {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  border: 2px solid transparent;
  transition: scale var(--duration-fast) var(--ease-bounce);
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

---

## 181. CUSTOM CURSORS

```css
/* ─── Custom cursor system ─── */
/* Apply via JS: document.documentElement.style.cursor = 'url(cursor.svg), auto' */

/* CSS-based custom cursors using SVG data URLs */
:root {
  --cursor-default: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M5.5 3.21V20.8l4.19-4.19h9.06L5.5 3.21z' fill='white' stroke='black' stroke-width='1'/%3E%3C/svg%3E") 0 0, auto;

  --cursor-pointer: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M8 1v14l3-3h8L8 1z' fill='%233b82f6' stroke='white' stroke-width='1.5'/%3E%3C/svg%3E") 0 0, pointer;
}

/* Large accessible cursor */
[data-cursor="large"] * { cursor: url("large-cursor.svg") 0 0, auto !important; }

/* ─── CSS-only cursor following element ─── */
/* JS: document.addEventListener('mousemove', e => {
    document.documentElement.style.setProperty('--cx', e.clientX + 'px');
    document.documentElement.style.setProperty('--cy', e.clientY + 'px');
}); */

.custom-cursor {
  position: fixed;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 9999;
  translate: calc(var(--cx, 0px) - 50%) calc(var(--cy, 0px) - 50%);
  transition: translate 0.08s linear, scale 0.2s var(--ease-out), opacity 0.2s;
}

/* Default dot cursor */
.custom-cursor__dot {
  width: 8px;
  height: 8px;
  background: var(--color-accent);
  border-radius: 50%;
  transition: scale 0.2s var(--ease-bounce), background 0.15s;
}

/* Ring cursor */
.custom-cursor__ring {
  position: fixed;
  top: 0;
  left: 0;
  width: 36px;
  height: 36px;
  border: 2px solid var(--color-accent);
  border-radius: 50%;
  pointer-events: none;
  z-index: 9998;
  translate: calc(var(--cx, 0px) - 50%) calc(var(--cy, 0px) - 50%);
  transition: translate 0.15s var(--ease-out), scale 0.3s var(--ease-bounce);
  mix-blend-mode: difference;
}

/* Hover state — grow ring, shrink dot */
a:hover ~ .custom-cursor .custom-cursor__dot,
button:hover ~ .custom-cursor .custom-cursor__dot { scale: 3; background: transparent; border: 2px solid var(--color-accent); }

a:hover ~ .custom-cursor__ring,
button:hover ~ .custom-cursor__ring { scale: 0; }

/* Text cursor */
.custom-cursor--text .custom-cursor__dot {
  width: 2px;
  height: 1.2em;
  border-radius: 1px;
  animation: text-cursor-blink 1s step-end infinite;
}

@keyframes text-cursor-blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* Grab cursor */
.custom-cursor--grab .custom-cursor__dot {
  width: 24px;
  height: 24px;
  background: url("data:image/svg+xml,...") center / contain no-repeat;
  background-color: transparent;
}

/* Cursor trail */
.cursor-trail {
  position: fixed;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-accent);
  pointer-events: none;
  z-index: 9997;
  opacity: 0;
  animation: trail-fade 0.5s ease-out forwards;
  translate: var(--tx, 0) var(--ty, 0);
}

@keyframes trail-fade {
  from { opacity: 0.6; scale: 1; }
  to   { opacity: 0; scale: 0.2; }
}
```

---
<br>

```
╔══════════════════════════════════════════════════════════════════════╗
║                     PART 12 — COMPLETE                               ║
║  Chapters 169–181 | 13 new chapters | Output: css-guide-part12.md   ║
╚══════════════════════════════════════════════════════════════════════╝
```
