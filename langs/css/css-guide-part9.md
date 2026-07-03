\# PART IX — CSS: SPECIALIZED INTERFACES \& LAYOUTS



\---



\## 142. SPLIT PANE / RESIZABLE PANELS



```css

/\* ─── Split view container ─── \*/

.split-pane {

&#x20; display: flex;

&#x20; height: 100%;

&#x20; overflow: hidden;

&#x20; position: relative;

&#x20; user-select: none; /\* prevent text selection during drag \*/

}



.split-pane--vertical {

&#x20; flex-direction: column;

}



/\* Individual panes \*/

.pane {

&#x20; overflow: auto;

&#x20; flex-shrink: 0;

&#x20; min-width: 0;

&#x20; min-height: 0;

&#x20; position: relative;

}



.pane--primary {

&#x20; width: var(--pane-size, 50%);

&#x20; flex: none;

}



.pane--secondary {

&#x20; flex: 1;

}



.split-pane--vertical .pane--primary {

&#x20; width: 100%;

&#x20; height: var(--pane-size, 50%);

}



/\* Resize handle \*/

.split-handle {

&#x20; position: relative;

&#x20; flex-shrink: 0;

&#x20; z-index: 1;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; background: var(--color-border);

&#x20; transition: background var(--duration-fast);

}



.split-pane:not(.split-pane--vertical) .split-handle {

&#x20; width: 4px;

&#x20; cursor: col-resize;

}



.split-pane--vertical .split-handle {

&#x20; height: 4px;

&#x20; width: 100%;

&#x20; cursor: row-resize;

}



.split-handle:hover,

.split-handle.dragging {

&#x20; background: var(--color-accent);

}



/\* Handle grip dots \*/

.split-handle\_\_grip {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: 3px;

&#x20; pointer-events: none;

}



.split-pane:not(.split-pane--vertical) .split-handle\_\_grip {

&#x20; flex-direction: row;

}



.split-handle\_\_dot {

&#x20; width: 3px;

&#x20; height: 3px;

&#x20; border-radius: 50%;

&#x20; background: currentColor;

&#x20; opacity: 0.5;

}



.split-handle:hover .split-handle\_\_dot { opacity: 1; }



/\* Dragging state \*/

.split-pane.is-dragging {

&#x20; cursor: col-resize;

}

.split-pane--vertical.is-dragging {

&#x20; cursor: row-resize;

}

.split-pane.is-dragging \* {

&#x20; pointer-events: none;

}



/\* Min/max constraints \*/

.pane { min-width: 120px; min-height: 60px; }



/\* Collapse button \*/

.pane\_\_collapse-btn {

&#x20; position: absolute;

&#x20; top: 50%;

&#x20; translate: 0 -50%;

&#x20; right: -12px;

&#x20; width: 20px;

&#x20; height: 32px;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: 0 var(--radius-md) var(--radius-md) 0;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; z-index: 2;

&#x20; font-size: 0.5rem;

&#x20; color: var(--color-text-muted);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.pane\_\_collapse-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }



/\* Collapsed state \*/

.pane.collapsed {

&#x20; width: 0 !important;

&#x20; overflow: hidden;

}

```



\---



\## 143. GANTT / PROJECT TIMELINE



```css

/\* ─── Gantt chart ─── \*/

.gantt {

&#x20; display: grid;

&#x20; grid-template-columns: 240px 1fr;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; font-size: var(--font-size-sm);

}



/\* Left panel — task names \*/

.gantt\_\_tasks {

&#x20; border-right: 2px solid var(--color-border);

&#x20; background: var(--color-surface);

&#x20; position: sticky;

&#x20; left: 0;

&#x20; z-index: 2;

}



.gantt\_\_task-header {

&#x20; height: 48px;

&#x20; padding: var(--space-3);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; background: var(--color-bg-subtle);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-xs);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wide);

}



.gantt\_\_task-row {

&#x20; height: 44px;

&#x20; padding: 0 var(--space-3);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast);

}

.gantt\_\_task-row:hover { background: var(--color-bg-subtle); }

.gantt\_\_task-row.selected { background: color-mix(in srgb, var(--color-accent) 8%, transparent); }



.gantt\_\_task-indent {

&#x20; width: calc(var(--depth, 0) \* 1.5rem);

&#x20; flex-shrink: 0;

}



.gantt\_\_task-toggle {

&#x20; width: 1rem;

&#x20; height: 1rem;

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; font-size: 0.5rem;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; flex-shrink: 0;

&#x20; transition: rotate var(--duration-fast);

}

.gantt\_\_task-row.expanded .gantt\_\_task-toggle { rotate: 90deg; }

.gantt\_\_task-row.leaf .gantt\_\_task-toggle { visibility: hidden; }



.gantt\_\_task-name {

&#x20; flex: 1;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

&#x20; font-weight: var(--font-weight-medium);

}



.gantt\_\_task-assignee {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

&#x20; flex-shrink: 0;

}



/\* Right panel — timeline \*/

.gantt\_\_timeline {

&#x20; overflow-x: auto;

&#x20; background: var(--color-surface);

&#x20; position: relative;

}



/\* Month headers \*/

.gantt\_\_months {

&#x20; display: flex;

&#x20; height: 24px;

&#x20; position: sticky;

&#x20; top: 0;

&#x20; z-index: 1;

&#x20; background: var(--color-bg-subtle);

&#x20; border-bottom: 1px solid var(--color-border);

}



.gantt\_\_month {

&#x20; height: 100%;

&#x20; border-right: 1px solid var(--color-border);

&#x20; padding: 0 var(--space-2);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wide);

&#x20; flex-shrink: 0;

}



/\* Day headers \*/

.gantt\_\_days {

&#x20; display: flex;

&#x20; height: 24px;

&#x20; position: sticky;

&#x20; top: 24px;

&#x20; z-index: 1;

&#x20; background: var(--color-bg-subtle);

&#x20; border-bottom: 1px solid var(--color-border);

}



.gantt\_\_day {

&#x20; height: 100%;

&#x20; width: var(--day-width, 32px);

&#x20; flex-shrink: 0;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 0.625rem;

&#x20; color: var(--color-text-subtle);

&#x20; border-right: 1px solid var(--color-border-subtle);

}



.gantt\_\_day.today {

&#x20; color: var(--color-accent);

&#x20; font-weight: var(--font-weight-bold);

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, transparent);

}



.gantt\_\_day.weekend { background: var(--color-bg-subtle); }



/\* Chart rows \*/

.gantt\_\_rows { position: relative; }



.gantt\_\_row {

&#x20; height: 44px;

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; position: relative;

&#x20; display: flex;

&#x20; align-items: center;

}



/\* Weekend columns \*/

.gantt\_\_row::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: repeating-linear-gradient(

&#x20;   to right,

&#x20;   transparent 0,

&#x20;   transparent calc(5 \* var(--day-width, 32px)),

&#x20;   var(--color-bg-subtle) calc(5 \* var(--day-width, 32px)),

&#x20;   var(--color-bg-subtle) calc(7 \* var(--day-width, 32px))

&#x20; );

&#x20; pointer-events: none;

}



/\* Today indicator \*/

.gantt\_\_today-line {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; left: var(--today-offset, 0);

&#x20; width: 2px;

&#x20; background: var(--color-accent);

&#x20; opacity: 0.7;

&#x20; pointer-events: none;

&#x20; z-index: 1;

}



/\* Task bars \*/

.gantt\_\_bar {

&#x20; position: absolute;

&#x20; height: 24px;

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--bar-color, var(--color-brand-500));

&#x20; left: var(--bar-start, 0);

&#x20; width: var(--bar-width, 100px);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; padding-inline: var(--space-2);

&#x20; overflow: hidden;

&#x20; cursor: grab;

&#x20; transition: filter var(--duration-fast), box-shadow var(--duration-fast);

&#x20; z-index: 1;

}



.gantt\_\_bar:hover {

&#x20; filter: brightness(1.1);

&#x20; box-shadow: var(--shadow-md);

}



.gantt\_\_bar.dragging { cursor: grabbing; opacity: 0.8; z-index: 5; }



/\* Progress fill \*/

.gantt\_\_bar-fill {

&#x20; position: absolute;

&#x20; inset-block: 0;

&#x20; inset-inline-start: 0;

&#x20; width: var(--progress, 0%);

&#x20; background: rgb(0 0 0 / 0.15);

&#x20; border-radius: inherit;

}



.gantt\_\_bar-label {

&#x20; position: relative;

&#x20; font-size: var(--font-size-xs);

&#x20; color: white;

&#x20; white-space: nowrap;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; z-index: 1;

}



/\* Milestone diamond \*/

.gantt\_\_milestone {

&#x20; position: absolute;

&#x20; width: 16px;

&#x20; height: 16px;

&#x20; background: var(--color-warning-500);

&#x20; rotate: 45deg;

&#x20; border: 2px solid white;

&#x20; left: var(--milestone-pos, 0);

&#x20; translate: -50% 0;

&#x20; cursor: pointer;

&#x20; z-index: 2;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}

.gantt\_\_milestone:hover { scale: 1.3; }



/\* Dependency arrow \*/

.gantt\_\_dependency {

&#x20; position: absolute;

&#x20; pointer-events: none;

&#x20; stroke: var(--color-neutral-400);

&#x20; stroke-width: 1.5;

&#x20; fill: none;

&#x20; stroke-dasharray: 4 2;

}



/\* Group/parent task bar \*/

.gantt\_\_bar--group {

&#x20; background: var(--color-neutral-700);

&#x20; height: 16px;

&#x20; border-radius: 2px;

}

.gantt\_\_bar--group::before,

.gantt\_\_bar--group::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 100%;

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; background: inherit;

}

.gantt\_\_bar--group::before { left: 0; clip-path: polygon(0 0, 100% 0, 0 100%); }

.gantt\_\_bar--group::after  { right: 0; clip-path: polygon(0 0, 100% 0, 100% 100%); }

```



\---



\## 144. ONBOARDING TOUR / PRODUCT WALKTHROUGH



```css

/\* ─── Tour spotlight ─── \*/

.tour-overlay {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; z-index: var(--z-modal);

&#x20; pointer-events: none;

}



/\* Spotlight effect using box-shadow \*/

.tour-spotlight {

&#x20; position: fixed;

&#x20; z-index: calc(var(--z-modal) + 1);

&#x20; border-radius: var(--spotlight-radius, var(--radius-lg));

&#x20; box-shadow: 0 0 0 9999px rgb(0 0 0 / 0.6);

&#x20; pointer-events: none;

&#x20; transition:

&#x20;   top    0.4s var(--ease-out),

&#x20;   left   0.4s var(--ease-out),

&#x20;   width  0.4s var(--ease-out),

&#x20;   height 0.4s var(--ease-out);

}



/\* Pulsing border on spotlight \*/

.tour-spotlight::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: -3px;

&#x20; border-radius: calc(var(--spotlight-radius, var(--radius-lg)) + 3px);

&#x20; border: 2px solid var(--color-accent);

&#x20; animation: spotlight-pulse 2s ease-in-out infinite;

}



@keyframes spotlight-pulse {

&#x20; 0%, 100% { opacity: 1; inset: -3px; }

&#x20; 50%       { opacity: 0.5; inset: -6px; }

}



/\* ─── Tour tooltip ─── \*/

.tour-tooltip {

&#x20; position: fixed;

&#x20; z-index: calc(var(--z-modal) + 2);

&#x20; background: var(--color-surface);

&#x20; border-radius: var(--radius-xl);

&#x20; box-shadow: var(--shadow-2xl);

&#x20; padding: var(--space-5);

&#x20; width: 280px;

&#x20; transition:

&#x20;   top  0.4s var(--ease-out),

&#x20;   left 0.4s var(--ease-out);

&#x20; animation: tooltip-appear 0.3s var(--ease-bounce);

}



@keyframes tooltip-appear {

&#x20; from { opacity: 0; scale: 0.92; }

}



/\* Arrow pointer \*/

.tour-tooltip::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; width: 12px;

&#x20; height: 12px;

&#x20; background: var(--color-surface);

&#x20; rotate: 45deg;

}



.tour-tooltip\[data-placement="top"]::before    { bottom: -6px; left: 50%; translate: -50% 0; box-shadow: 2px 2px 4px rgb(0 0 0 / 0.1); }

.tour-tooltip\[data-placement="bottom"]::before { top: -6px; left: 50%; translate: -50% 0; }

.tour-tooltip\[data-placement="left"]::before   { right: -6px; top: 50%; translate: 0 -50%; }

.tour-tooltip\[data-placement="right"]::before  { left: -6px; top: 50%; translate: 0 -50%; }



/\* Tooltip content \*/

.tour-tooltip\_\_step {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; margin-block-end: var(--space-2);

}



.tour-tooltip\_\_title {

&#x20; font-size: var(--font-size-base);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: var(--space-2);

}



.tour-tooltip\_\_desc {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

&#x20; margin-block-end: var(--space-4);

}



.tour-tooltip\_\_media {

&#x20; width: 100%;

&#x20; border-radius: var(--radius-lg);

&#x20; margin-block-end: var(--space-4);

&#x20; overflow: hidden;

}



.tour-tooltip\_\_media img,

.tour-tooltip\_\_media video {

&#x20; width: 100%;

&#x20; height: auto;

&#x20; display: block;

}



/\* Progress dots \*/

.tour-dots {

&#x20; display: flex;

&#x20; justify-content: center;

&#x20; gap: var(--space-1);

&#x20; margin-block-end: var(--space-4);

}



.tour-dot {

&#x20; width: 6px;

&#x20; height: 6px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-border-strong);

&#x20; transition: background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce), width var(--duration-fast);

}



.tour-dot.active {

&#x20; background: var(--color-accent);

&#x20; width: 18px;

&#x20; border-radius: var(--radius-full);

}



/\* Actions \*/

.tour-tooltip\_\_actions {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



.tour-skip {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; background: none;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; margin-inline-end: auto;

&#x20; padding: 0;

&#x20; text-decoration: underline;

&#x20; text-underline-offset: 2px;

}

.tour-skip:hover { color: var(--color-text); }



/\* ─── Onboarding checklist ─── \*/

.onboarding-checklist {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-5);

&#x20; max-width: 360px;

}



.checklist-header {

&#x20; margin-block-end: var(--space-4);

}



.checklist-title {

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-base);

&#x20; margin-block-end: var(--space-1);

}



.checklist-subtitle {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

}



.checklist-progress {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; margin-block: var(--space-3);

}



.checklist-bar {

&#x20; flex: 1;

&#x20; height: 6px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

}



.checklist-bar\_\_fill {

&#x20; height: 100%;

&#x20; background: var(--color-accent);

&#x20; border-radius: inherit;

&#x20; width: var(--progress, 0%);

&#x20; transition: width 0.5s var(--ease-out);

}



.checklist-count {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

&#x20; white-space: nowrap;

&#x20; font-variant-numeric: tabular-nums;

}



.checklist-items {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

}



.checklist-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-3);

&#x20; border-radius: var(--radius-lg);

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast);

&#x20; border: 1px solid transparent;

}

.checklist-item:hover { background: var(--color-bg-subtle); }

.checklist-item.active { border-color: var(--color-accent); background: color-mix(in srgb, var(--color-accent) 5%, transparent); }



.checklist-item\_\_icon {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: var(--radius-lg);

&#x20; background: var(--color-bg-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 1rem;

&#x20; flex-shrink: 0;

&#x20; transition: background var(--duration-fast);

}



.checklist-item.done .checklist-item\_\_icon {

&#x20; background: var(--color-success-100);

&#x20; color: var(--color-success-600);

}



.checklist-item\_\_text {

&#x20; flex: 1;

&#x20; min-width: 0;

}



.checklist-item\_\_title {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

}



.checklist-item.done .checklist-item\_\_title {

&#x20; text-decoration: line-through;

&#x20; color: var(--color-text-muted);

}



.checklist-item\_\_desc {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



/\* Completion celebration \*/

.checklist-complete {

&#x20; text-align: center;

&#x20; padding: var(--space-6);

}



.checklist-complete\_\_emoji {

&#x20; font-size: 3rem;

&#x20; animation: bounce 0.6s var(--ease-bounce);

}



@keyframes bounce {

&#x20; 0%   { translate: 0 0; }

&#x20; 40%  { translate: 0 -20px; }

&#x20; 70%  { translate: 0 -10px; }

&#x20; 100% { translate: 0 0; }

}

```



\---



\## 145. MUSIC PLAYER



```css

/\* ─── Full music player ─── \*/

.music-player {

&#x20; background: var(--player-bg, #1a1a2e);

&#x20; color: white;

&#x20; border-radius: var(--radius-2xl);

&#x20; overflow: hidden;

&#x20; max-width: 360px;

&#x20; box-shadow: var(--shadow-2xl);

}



/\* Album art \*/

.player-art {

&#x20; position: relative;

&#x20; aspect-ratio: 1;

&#x20; overflow: hidden;

}



.player-art img {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; transition: scale var(--duration-slow) var(--ease-out);

}



.music-player.playing .player-art img {

&#x20; animation: album-spin 20s linear infinite;

}



/\* Spinning album (alternative) \*/

@keyframes album-spin {

&#x20; to { rotate: 360deg; }

}



/\* Playing indicator overlay \*/

.player-art\_\_eq {

&#x20; position: absolute;

&#x20; bottom: var(--space-4);

&#x20; right: var(--space-4);

&#x20; display: flex;

&#x20; align-items: flex-end;

&#x20; gap: 2px;

&#x20; height: 24px;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

}



.music-player.playing .player-art\_\_eq { opacity: 1; }



.player-art\_\_bar {

&#x20; width: 3px;

&#x20; border-radius: 2px;

&#x20; background: white;

&#x20; animation: eq-bar 0.8s ease-in-out infinite alternate;

}

.player-art\_\_bar:nth-child(1) { height: 40%; animation-delay: 0s; }

.player-art\_\_bar:nth-child(2) { height: 70%; animation-delay: 0.15s; }

.player-art\_\_bar:nth-child(3) { height: 90%; animation-delay: 0.3s; }

.player-art\_\_bar:nth-child(4) { height: 55%; animation-delay: 0.1s; }

.player-art\_\_bar:nth-child(5) { height: 80%; animation-delay: 0.25s; }



@keyframes eq-bar {

&#x20; from { height: 20%; }

&#x20; to   { /\* uses var \*/ }

}



/\* Favorite button on art \*/

.player-art\_\_like {

&#x20; position: absolute;

&#x20; top: var(--space-3);

&#x20; right: var(--space-3);

&#x20; width: 2.25rem;

&#x20; height: 2.25rem;

&#x20; border-radius: 50%;

&#x20; background: rgb(0 0 0 / 0.3);

&#x20; backdrop-filter: blur(8px);

&#x20; border: 1px solid rgba(255 255 255 / 0.15);

&#x20; color: white;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; cursor: pointer;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}

.player-art\_\_like:hover { scale: 1.1; }

.player-art\_\_like.liked { color: var(--color-danger-400); }



/\* Player controls \*/

.player-controls {

&#x20; padding: var(--space-5);

}



.player-info {

&#x20; margin-block-end: var(--space-4);

}



.player-title {

&#x20; font-size: var(--font-size-lg);

&#x20; font-weight: var(--font-weight-bold);

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



.player-artist {

&#x20; font-size: var(--font-size-sm);

&#x20; color: rgba(255 255 255 / 0.6);

&#x20; margin-block-start: var(--space-1);

}



/\* Seek bar \*/

.player-seek {

&#x20; margin-block-end: var(--space-4);

}



.player-track {

&#x20; width: 100%;

&#x20; height: 4px;

&#x20; appearance: none;

&#x20; background: rgba(255 255 255 / 0.2);

&#x20; border-radius: var(--radius-full);

&#x20; outline: none;

&#x20; cursor: pointer;

&#x20; position: relative;

&#x20; margin-block-end: var(--space-2);

}



.player-track::-webkit-slider-thumb {

&#x20; appearance: none;

&#x20; width: 14px;

&#x20; height: 14px;

&#x20; border-radius: 50%;

&#x20; background: white;

&#x20; cursor: pointer;

&#x20; box-shadow: 0 0 4px rgba(0 0 0 / 0.4);

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}

.player-track:hover::-webkit-slider-thumb { scale: 1.3; }



/\* Progress fill for range \*/

.player-track {

&#x20; background: linear-gradient(

&#x20;   to right,

&#x20;   white var(--seek-progress, 0%),

&#x20;   rgba(255 255 255 / 0.2) var(--seek-progress, 0%)

&#x20; );

}



.player-times {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.5);

&#x20; font-variant-numeric: tabular-nums;

&#x20; font-family: var(--font-mono);

}



/\* Main controls row \*/

.player-main-controls {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; margin-block-end: var(--space-3);

}



.player-btn {

&#x20; background: none;

&#x20; border: none;

&#x20; color: rgba(255 255 255 / 0.7);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; border-radius: 50%;

&#x20; transition: color var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

}

.player-btn:hover { color: white; scale: 1.1; }

.player-btn.active { color: var(--color-accent); }



.player-btn--play {

&#x20; width: 3.5rem;

&#x20; height: 3.5rem;

&#x20; background: white;

&#x20; color: var(--player-bg, #1a1a2e);

&#x20; border-radius: 50%;

&#x20; font-size: 1.25rem;

&#x20; box-shadow: 0 4px 16px rgba(0 0 0 / 0.3);

&#x20; transition: scale var(--duration-fast) var(--ease-bounce), box-shadow var(--duration-fast);

}

.player-btn--play:hover { scale: 1.07; box-shadow: 0 6px 20px rgba(0 0 0 / 0.4); }

.player-btn--play:active { scale: 0.95; }



/\* Volume row \*/

.player-volume {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



.volume-track {

&#x20; flex: 1;

&#x20; height: 3px;

&#x20; appearance: none;

&#x20; background: linear-gradient(

&#x20;   to right,

&#x20;   rgba(255 255 255 / 0.7) var(--volume, 70%),

&#x20;   rgba(255 255 255 / 0.15) var(--volume, 70%)

&#x20; );

&#x20; border-radius: var(--radius-full);

&#x20; outline: none;

&#x20; cursor: pointer;

}

.volume-track::-webkit-slider-thumb {

&#x20; appearance: none;

&#x20; width: 10px;

&#x20; height: 10px;

&#x20; border-radius: 50%;

&#x20; background: white;

&#x20; cursor: pointer;

}



/\* Mini player variant \*/

.music-player--mini {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; border-radius: var(--radius-2xl);

&#x20; max-width: none;

&#x20; width: 100%;

}



.music-player--mini .player-art {

&#x20; width: 3rem;

&#x20; height: 3rem;

&#x20; border-radius: var(--radius-lg);

&#x20; aspect-ratio: auto;

&#x20; flex-shrink: 0;

}

.music-player--mini .player-info { flex: 1; margin: 0; }

.music-player--mini .player-title { font-size: var(--font-size-sm); }

.music-player--mini .player-artist { font-size: var(--font-size-xs); }

```



\---



\## 146. BLOG / ARTICLE LAYOUTS



```css

/\* ─── Blog list page ─── \*/

.blog-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr));

&#x20; gap: var(--space-8);

}



/\* Featured first post \*/

.blog-grid .post-card:first-child {

&#x20; grid-column: 1 / -1;

}



.blog-grid .post-card:first-child .post-card\_\_image {

&#x20; aspect-ratio: 2 / 1;

}



/\* ─── Post card ─── \*/

.post-card {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; transition:

&#x20;   box-shadow var(--duration-normal),

&#x20;   translate  var(--duration-normal);

&#x20; text-decoration: none;

&#x20; color: inherit;

}



.post-card:hover {

&#x20; box-shadow: var(--shadow-lg);

&#x20; translate: 0 -2px;

}



.post-card\_\_image {

&#x20; aspect-ratio: 16 / 9;

&#x20; overflow: hidden;

}



.post-card\_\_image img {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; transition: scale var(--duration-slow) var(--ease-out);

}



.post-card:hover .post-card\_\_image img { scale: 1.04; }



.post-card\_\_body {

&#x20; padding: var(--space-5);

&#x20; flex: 1;

&#x20; display: flex;

&#x20; flex-direction: column;

}



.post-card\_\_tags {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-1);

&#x20; margin-block-end: var(--space-3);

}



.post-tag {

&#x20; padding: 0.2em 0.6em;

&#x20; background: var(--tag-bg, var(--color-brand-100));

&#x20; color: var(--tag-color, var(--color-brand-700));

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-decoration: none;

&#x20; transition: filter var(--duration-fast);

}

.post-tag:hover { filter: brightness(0.9); }



.post-card\_\_title {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-bold);

&#x20; line-height: 1.35;

&#x20; margin-block-end: var(--space-3);

&#x20; text-wrap: balance;

&#x20; flex: 1;

}



.post-card\_\_excerpt {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

&#x20; overflow: hidden;

&#x20; display: -webkit-box;

&#x20; -webkit-line-clamp: 2;

&#x20; -webkit-box-orient: vertical;

&#x20; margin-block-end: var(--space-4);

}



.post-card\_\_meta {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-start: auto;

&#x20; padding-block-start: var(--space-4);

&#x20; border-top: 1px solid var(--color-border);

}



.post-card\_\_author {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



.post-card\_\_author img {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

}



.post-card\_\_read-time {

&#x20; margin-inline-start: auto;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25em;

}



/\* ─── Article page ─── \*/

.article-layout {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr min(65ch, 100%) 1fr;

&#x20; row-gap: 0;

}



.article-layout > \* {

&#x20; grid-column: 2;

}



/\* Full-width elements \*/

.article-layout .full-width {

&#x20; grid-column: 1 / -1;

&#x20; width: 100%;

}



/\* Wide elements (breakout) \*/

.article-layout .breakout {

&#x20; grid-column: 1 / -1;

&#x20; max-width: min(100%, 900px);

&#x20; margin-inline: auto;

&#x20; padding-inline: var(--space-4);

}



/\* Article header \*/

.article-header {

&#x20; padding-block: var(--space-8);

}



.article-header\_\_tags {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-2);

&#x20; margin-block-end: var(--space-4);

}



.article-header\_\_title {

&#x20; font-size: clamp(2rem, 5vw, 3.5rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; line-height: 1.1;

&#x20; letter-spacing: -0.03em;

&#x20; text-wrap: balance;

&#x20; margin-block-end: var(--space-5);

}



.article-header\_\_subtitle {

&#x20; font-size: clamp(1rem, 2vw, 1.25rem);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

&#x20; max-width: 55ch;

&#x20; margin-block-end: var(--space-6);

&#x20; text-wrap: pretty;

}



.article-header\_\_meta {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-4);

&#x20; padding-block: var(--space-4);

&#x20; border-block: 1px solid var(--color-border);

&#x20; flex-wrap: wrap;

}



.article-author {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

}



.article-author\_\_avatar {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

}



.article-author\_\_name {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

}



.article-author\_\_bio {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



.article-meta-item {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.375rem;

}



/\* Hero image \*/

.article-hero {

&#x20; width: 100%;

&#x20; aspect-ratio: 2 / 1;

&#x20; object-fit: cover;

&#x20; margin-block: var(--space-8);

}



.article-hero-caption {

&#x20; text-align: center;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-style: italic;

&#x20; margin-block-start: -var(--space-6);

&#x20; margin-block-end: var(--space-8);

}



/\* Reading progress bar \*/

.reading-progress {

&#x20; position: fixed;

&#x20; top: 0;

&#x20; left: 0;

&#x20; height: 3px;

&#x20; background: var(--color-accent);

&#x20; width: var(--read-progress, 0%);

&#x20; z-index: var(--z-top);

&#x20; transition: width 0.05s linear;

&#x20; box-shadow: 0 0 8px var(--color-accent);

}



/\* Share bar \*/

.share-bar {

&#x20; position: sticky;

&#x20; top: 50%;

&#x20; translate: 0 -50%;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

&#x20; padding: var(--space-3);

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; box-shadow: var(--shadow-md);

&#x20; width: fit-content;

&#x20; grid-column: 1;

&#x20; margin-inline-start: auto;

&#x20; margin-inline-end: var(--space-4);

}



.share-btn {

&#x20; width: 2.25rem;

&#x20; height: 2.25rem;

&#x20; border-radius: var(--radius-lg);

&#x20; border: 1px solid var(--color-border);

&#x20; background: var(--color-surface);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; font-size: 0.875rem;

&#x20; transition:

&#x20;   background var(--duration-fast),

&#x20;   border-color var(--duration-fast),

&#x20;   color var(--duration-fast),

&#x20;   scale var(--duration-fast) var(--ease-bounce);

}

.share-btn:hover { scale: 1.1; background: var(--color-bg-subtle); color: var(--color-text); }

.share-btn.liked { color: var(--color-danger-500); border-color: var(--color-danger-200); background: var(--color-danger-100); }



/\* Related posts \*/

.related-posts {

&#x20; margin-block-start: var(--space-16);

&#x20; padding-block-start: var(--space-8);

&#x20; border-top: 1px solid var(--color-border);

}



.related-posts\_\_title {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: var(--space-6);

}



.related-posts\_\_grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));

&#x20; gap: var(--space-6);

}

```



\---



\## 147. PORTFOLIO / SHOWCASE PATTERNS



```css

/\* ─── Portfolio grid ─── \*/

.portfolio-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));

&#x20; gap: var(--space-4);

}



/\* Asymmetric masonry variant \*/

.portfolio-masonry {

&#x20; columns: 3 280px;

&#x20; column-gap: var(--space-4);

}



.portfolio-masonry .portfolio-item {

&#x20; break-inside: avoid;

&#x20; margin-block-end: var(--space-4);

}



/\* Portfolio item \*/

.portfolio-item {

&#x20; position: relative;

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; cursor: pointer;

&#x20; background: var(--color-bg-muted);

}



.portfolio-item\_\_media {

&#x20; display: block;

&#x20; width: 100%;

&#x20; height: auto;

&#x20; transition: scale var(--duration-slow) var(--ease-out), filter var(--duration-slow);

}



.portfolio-item:hover .portfolio-item\_\_media {

&#x20; scale: 1.06;

&#x20; filter: brightness(0.7);

}



/\* Overlay info \*/

.portfolio-item\_\_info {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; justify-content: flex-end;

&#x20; padding: var(--space-4);

&#x20; background: linear-gradient(to top, rgb(0 0 0 / 0.8) 0%, transparent 60%);

&#x20; opacity: 0;

&#x20; translate: 0 8px;

&#x20; transition:

&#x20;   opacity   var(--duration-normal),

&#x20;   translate var(--duration-normal) var(--ease-out);

}



.portfolio-item:hover .portfolio-item\_\_info {

&#x20; opacity: 1;

&#x20; translate: 0 0;

}



.portfolio-item\_\_title {

&#x20; color: white;

&#x20; font-size: var(--font-size-base);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: var(--space-1);

}



.portfolio-item\_\_desc {

&#x20; color: rgba(255 255 255 / 0.7);

&#x20; font-size: var(--font-size-xs);

}



.portfolio-item\_\_tags {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-1);

&#x20; margin-block-start: var(--space-2);

}



.portfolio-item\_\_tag {

&#x20; padding: 0.15em 0.5em;

&#x20; background: rgba(255 255 255 / 0.15);

&#x20; color: white;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: 0.625rem;

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.05em;

&#x20; backdrop-filter: blur(4px);

}



/\* Category filter \*/

.portfolio-filters {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-2);

&#x20; margin-block-end: var(--space-6);

}



.portfolio-filter-btn {

&#x20; padding: 0.4rem 1rem;

&#x20; border-radius: var(--radius-full);

&#x20; border: 1px solid var(--color-border);

&#x20; background: var(--color-surface);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; transition:

&#x20;   background      var(--duration-fast),

&#x20;   border-color    var(--duration-fast),

&#x20;   color           var(--duration-fast),

&#x20;   scale           var(--duration-fast) var(--ease-bounce);

}

.portfolio-filter-btn:hover { border-color: var(--color-accent); color: var(--color-accent); }

.portfolio-filter-btn.active {

&#x20; background: var(--color-accent);

&#x20; border-color: var(--color-accent);

&#x20; color: white;

}



/\* Filter animation \*/

.portfolio-item {

&#x20; transition:

&#x20;   opacity   var(--duration-normal) var(--ease-out),

&#x20;   scale     var(--duration-normal) var(--ease-bounce),

&#x20;   translate var(--duration-normal) var(--ease-out);

}



.portfolio-item.hidden {

&#x20; opacity: 0;

&#x20; scale: 0.9;

&#x20; pointer-events: none;

&#x20; position: absolute;

}

```



\---



\## 148. RESTAURANT MENU



```css

/\* ─── Restaurant menu layout ─── \*/

.menu-page {

&#x20; max-width: 900px;

&#x20; margin-inline: auto;

&#x20; padding: var(--space-8) var(--space-4);

}



/\* Menu header \*/

.menu-header {

&#x20; text-align: center;

&#x20; padding-block: var(--space-10);

&#x20; position: relative;

}



.menu-header\_\_logo {

&#x20; font-family: Georgia, serif;

&#x20; font-size: clamp(2.5rem, 6vw, 4rem);

&#x20; font-weight: 700;

&#x20; letter-spacing: -0.03em;

}



.menu-header\_\_tagline {

&#x20; font-style: italic;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-lg);

&#x20; margin-block-start: var(--space-2);

}



.menu-divider {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; margin-block: var(--space-6);

&#x20; color: var(--color-accent);

}

.menu-divider::before,

.menu-divider::after {

&#x20; content: '';

&#x20; flex: 1;

&#x20; height: 1px;

&#x20; background: currentColor;

&#x20; opacity: 0.3;

}

.menu-divider::before { content: '✦ ✦ ✦'; display: block; flex: none; }



/\* Menu sections \*/

.menu-section {

&#x20; margin-block-end: var(--space-10);

}



.menu-section\_\_title {

&#x20; font-family: Georgia, serif;

&#x20; font-size: var(--step-2);

&#x20; font-weight: 700;

&#x20; text-align: center;

&#x20; margin-block-end: var(--space-2);

&#x20; color: var(--color-text);

}



.menu-section\_\_subtitle {

&#x20; text-align: center;

&#x20; font-style: italic;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; margin-block-end: var(--space-6);

}



/\* Menu items \*/

.menu-item {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; padding-block: var(--space-4);

&#x20; border-bottom: 1px dotted var(--color-border);

&#x20; align-items: flex-start;

}

.menu-item:last-child { border: none; }



.menu-item\_\_image {

&#x20; width: 80px;

&#x20; height: 80px;

&#x20; border-radius: var(--radius-lg);

&#x20; object-fit: cover;

&#x20; flex-shrink: 0;

}



.menu-item\_\_info { flex: 1; }



.menu-item\_\_header {

&#x20; display: flex;

&#x20; align-items: baseline;

&#x20; gap: var(--space-2);

&#x20; margin-block-end: var(--space-1);

}



.menu-item\_\_name {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-base);

}



/\* Dotted leader \*/

.menu-item\_\_leader {

&#x20; flex: 1;

&#x20; border-bottom: 1px dotted var(--color-border);

&#x20; margin-block-end: 4px;

}



.menu-item\_\_price {

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-variant-numeric: tabular-nums;

&#x20; color: var(--color-text);

&#x20; white-space: nowrap;

}



.menu-item\_\_description {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.5;

}



.menu-item\_\_badges {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-1);

&#x20; margin-block-start: var(--space-2);

}



.menu-badge {

&#x20; padding: 0.15em 0.5em;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

}



.menu-badge--spicy    { background: #fef2f2; color: #dc2626; }

.menu-badge--vegan    { background: #f0fdf4; color: #16a34a; }

.menu-badge--gluten   { background: #fefce8; color: #ca8a04; }

.menu-badge--popular  { background: #fdf4ff; color: #9333ea; }

.menu-badge--new      { background: #eff6ff; color: #2563eb; }

.menu-badge--chef     { background: var(--color-warning-100); color: var(--color-warning-700); }



/\* Grid menu variant \*/

.menu-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));

&#x20; gap: var(--space-4);

}



.menu-card {

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   box-shadow var(--duration-normal),

&#x20;   translate  var(--duration-normal);

}

.menu-card:hover { box-shadow: var(--shadow-md); translate: 0 -2px; }



.menu-card\_\_image { width: 100%; aspect-ratio: 4/3; object-fit: cover; }

.menu-card\_\_body { padding: var(--space-3); }

.menu-card\_\_name { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }

.menu-card\_\_price {

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-accent);

&#x20; margin-block-start: var(--space-1);

}

```



\---



\## 149. MARKETING PAGE SECTIONS



```css

/\* ─── Testimonials ─── \*/

.testimonials-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));

&#x20; gap: var(--space-6);

}



.testimonial-card {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-6);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-4);

&#x20; transition: box-shadow var(--duration-normal);

}

.testimonial-card:hover { box-shadow: var(--shadow-lg); }



.testimonial-stars {

&#x20; display: flex;

&#x20; gap: 2px;

&#x20; color: var(--color-warning-400);

&#x20; font-size: 0.875rem;

}



.testimonial-quote {

&#x20; font-size: var(--font-size-base);

&#x20; line-height: 1.7;

&#x20; color: var(--color-text);

&#x20; flex: 1;

&#x20; font-style: italic;

}



.testimonial-quote::before { content: '"'; font-size: 2em; line-height: 0; vertical-align: -0.4em; color: var(--color-accent); opacity: 0.4; margin-inline-end: 0.1em; }



.testimonial-author {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding-block-start: var(--space-4);

&#x20; border-top: 1px solid var(--color-border);

}



.testimonial-author img {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

}



.testimonial-author\_\_name {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

}



.testimonial-author\_\_role {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



/\* ─── Logo cloud / Social proof ─── \*/

.logo-cloud {

&#x20; text-align: center;

&#x20; padding-block: var(--space-10);

}



.logo-cloud\_\_label {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-6);

}



.logo-cloud\_\_logos {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-8);

&#x20; filter: grayscale(100%);

&#x20; opacity: 0.5;

}



.logo-cloud\_\_logos img { height: 28px; width: auto; }



/\* Marquee version \*/

.logo-cloud--marquee .logo-cloud\_\_logos {

&#x20; flex-wrap: nowrap;

&#x20; overflow: hidden;

&#x20; -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);

&#x20; mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);

}



.logo-cloud--marquee .logo-cloud\_\_inner {

&#x20; display: flex;

&#x20; gap: var(--space-8);

&#x20; animation: logo-scroll 20s linear infinite;

&#x20; flex-shrink: 0;

}



@keyframes logo-scroll {

&#x20; from { translate: 0; }

&#x20; to   { translate: -50%; }

}



/\* ─── CTA section ─── \*/

.cta-section {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; padding: clamp(3rem, 8vw, 8rem) clamp(1rem, 5vw, 4rem);

&#x20; border-radius: var(--radius-3xl);

&#x20; text-align: center;

&#x20; position: relative;

&#x20; overflow: hidden;

}



.cta-section::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: -50%;

&#x20; background:

&#x20;   radial-gradient(circle at 30% 50%, rgba(255 255 255 / 0.1) 0%, transparent 50%),

&#x20;   radial-gradient(circle at 70% 50%, rgba(255 255 255 / 0.08) 0%, transparent 50%);

}



.cta-section > \* { position: relative; z-index: 1; }



.cta-section\_\_title {

&#x20; font-size: clamp(1.75rem, 4vw, 3rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; line-height: 1.15;

&#x20; text-wrap: balance;

&#x20; margin-block-end: var(--space-4);

}



.cta-section\_\_desc {

&#x20; font-size: clamp(1rem, 2vw, 1.25rem);

&#x20; opacity: 0.85;

&#x20; max-width: 50ch;

&#x20; margin-inline: auto;

&#x20; margin-block-end: var(--space-8);

&#x20; text-wrap: pretty;

}



.cta-section\_\_actions {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; justify-content: center;

&#x20; flex-wrap: wrap;

}



.btn--light {

&#x20; background: white;

&#x20; color: var(--color-accent);

&#x20; font-weight: var(--font-weight-bold);

}

.btn--light:hover { background: rgba(255 255 255 / 0.9); }



.btn--outline-white {

&#x20; background: transparent;

&#x20; border: 2px solid rgba(255 255 255 / 0.5);

&#x20; color: white;

}

.btn--outline-white:hover { background: rgba(255 255 255 / 0.1); border-color: white; }



/\* ─── Stats / Numbers section ─── \*/

.stats-row {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr));

&#x20; gap: var(--space-8);

&#x20; text-align: center;

}



.stat-item { }



.stat-item\_\_number {

&#x20; font-size: clamp(2.5rem, 5vw, 4rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; line-height: 1;

&#x20; font-variant-numeric: tabular-nums;

&#x20; letter-spacing: -0.03em;

&#x20; background: linear-gradient(135deg, var(--color-accent), color-mix(in oklch, var(--color-accent) 50%, var(--color-brand-300)));

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

}



.stat-item\_\_label {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-start: var(--space-2);

&#x20; font-weight: var(--font-weight-medium);

}



/\* Number counter animation \*/

.stat-item\_\_number {

&#x20; animation: count-in linear both;

&#x20; animation-timeline: view();

&#x20; animation-range: entry 0% entry 50%;

}



@keyframes count-in {

&#x20; from { opacity: 0; translate: 0 20px; }

}



/\* ─── FAQ accordion ─── \*/

.faq-list {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

}



.faq-item {

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; transition: border-color var(--duration-fast);

}

.faq-item.open { border-color: var(--color-accent); }



.faq-question {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; gap: var(--space-4);

&#x20; padding: var(--space-5);

&#x20; cursor: pointer;

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-base);

&#x20; list-style: none;

&#x20; user-select: none;

&#x20; transition: color var(--duration-fast);

}

.faq-item.open .faq-question { color: var(--color-accent); }



.faq-question::marker { display: none; }

.faq-question::-webkit-details-marker { display: none; }



.faq-icon {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-bg-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; flex-shrink: 0;

&#x20; font-size: 1rem;

&#x20; transition:

&#x20;   background  var(--duration-fast),

&#x20;   rotate      var(--duration-fast) var(--ease-out);

}

.faq-item.open .faq-icon {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; rotate: 45deg;

}



.faq-answer {

&#x20; padding: 0 var(--space-5) var(--space-5);

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.7;

}



/\* ─── How it works / Steps ─── \*/

.how-it-works {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr));

&#x20; gap: var(--space-8);

&#x20; position: relative;

}



/\* Connecting line between steps \*/

.how-it-works::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 2rem;

&#x20; left: 2.5rem;

&#x20; right: 2.5rem;

&#x20; height: 2px;

&#x20; background: linear-gradient(to right, var(--color-accent), color-mix(in oklch, var(--color-accent) 50%, transparent));

&#x20; opacity: 0.3;

}



@media (max-width: 768px) {

&#x20; .how-it-works::before { display: none; }

}



.step-card {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-4);

&#x20; position: relative;

}



.step-card\_\_num {

&#x20; width: 4rem;

&#x20; height: 4rem;

&#x20; border-radius: var(--radius-2xl);

&#x20; background: color-mix(in srgb, var(--color-accent) 12%, transparent);

&#x20; border: 2px solid color-mix(in srgb, var(--color-accent) 20%, transparent);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-black);

&#x20; color: var(--color-accent);

}



.step-card\_\_title {

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-lg);

}



.step-card\_\_desc {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

}

```



\---



\## 150. ADVANCED TOOLTIP POSITIONING



```css

/\* ─── Complete tooltip system via anchor positioning ─── \*/



/\* The anchor target \*/

\[data-tooltip-target] {

&#x20; anchor-name: --tooltip-anchor;

}



/\* Base tooltip \*/

.tooltip-popup {

&#x20; position: fixed;

&#x20; position-anchor: --tooltip-anchor;



&#x20; /\* Default: top center \*/

&#x20; bottom: calc(anchor(top) + 8px);

&#x20; left:  anchor(center);

&#x20; translate: -50% 0;



&#x20; padding: 0.4rem 0.75rem;

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; border-radius: var(--radius-md);

&#x20; white-space: nowrap;

&#x20; pointer-events: none;

&#x20; max-width: 240px;

&#x20; white-space: normal;

&#x20; line-height: 1.4;

&#x20; box-shadow: var(--shadow-lg);



&#x20; /\* Auto-flip if out of viewport \*/

&#x20; position-try-fallbacks:

&#x20;   --tooltip-bottom,

&#x20;   --tooltip-right,

&#x20;   --tooltip-left;

}



@position-try --tooltip-bottom {

&#x20; top:    calc(anchor(bottom) + 8px);

&#x20; bottom: auto;

&#x20; left:   anchor(center);

&#x20; translate: -50% 0;

}



@position-try --tooltip-right {

&#x20; left:    calc(anchor(right) + 8px);

&#x20; bottom:  auto;

&#x20; right:   auto;

&#x20; top:     anchor(center);

&#x20; translate: 0 -50%;

}



@position-try --tooltip-left {

&#x20; right:   calc(100% - anchor(left) + 8px);

&#x20; left:    auto;

&#x20; bottom:  auto;

&#x20; top:     anchor(center);

&#x20; translate: 0 -50%;

}



/\* CSS-only fallback (no anchor positioning) \*/

@supports not (anchor-name: --a) {

&#x20; .tooltip-wrapper {

&#x20;   position: relative;

&#x20;   display: inline-block;

&#x20; }



&#x20; .tooltip-popup-fallback {

&#x20;   position: absolute;

&#x20;   bottom: calc(100% + 8px);

&#x20;   left: 50%;

&#x20;   translate: -50% 0;

&#x20;   z-index: var(--z-tooltip);

&#x20;   width: max-content;

&#x20;   max-width: 240px;



&#x20;   opacity: 0;

&#x20;   translate: -50% 4px;

&#x20;   transition:

&#x20;     opacity   var(--duration-fast),

&#x20;     translate var(--duration-fast);

&#x20;   pointer-events: none;

&#x20; }



&#x20; .tooltip-wrapper:hover .tooltip-popup-fallback,

&#x20; .tooltip-wrapper:focus-within .tooltip-popup-fallback {

&#x20;   opacity: 1;

&#x20;   translate: -50% 0;

&#x20; }

}



/\* ─── Rich tooltip ─── \*/

.tooltip-rich {

&#x20; position: fixed;

&#x20; position-anchor: --rich-anchor;

&#x20; width: 280px;



&#x20; top:  calc(anchor(bottom) + 8px);

&#x20; left: anchor(center);

&#x20; translate: -50% 0;



&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; box-shadow: var(--shadow-xl);

&#x20; padding: var(--space-4);

&#x20; pointer-events: none;



&#x20; position-try-fallbacks: --rich-above;

}



@position-try --rich-above {

&#x20; top:    auto;

&#x20; bottom: calc(anchor(top) + 8px);

&#x20; left:   anchor(center);

&#x20; translate: -50% 0;

}



.tooltip-rich\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; margin-block-end: var(--space-1);

}



.tooltip-rich\_\_body {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.5;

}



.tooltip-rich\_\_image {

&#x20; width: 100%;

&#x20; border-radius: var(--radius-md);

&#x20; margin-block-end: var(--space-3);

&#x20; object-fit: cover;

&#x20; height: 120px;

}

```



\---



\## 151. READING PROGRESS \& TOC



```css

/\* ─── Reading progress tracker ─── \*/

.reading-container {

&#x20; position: relative;

}



/\* Progress line in margin \*/

.reading-progress-line {

&#x20; position: fixed;

&#x20; top: var(--header-height, 0);

&#x20; bottom: 0;

&#x20; left: 0;

&#x20; width: 3px;

&#x20; z-index: var(--z-fixed);

}



.reading-progress-line\_\_track {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; background: var(--color-border);

}



.reading-progress-line\_\_fill {

&#x20; width: 100%;

&#x20; height: var(--read-progress, 0%);

&#x20; background: linear-gradient(to bottom, var(--color-accent), color-mix(in oklch, var(--color-accent) 50%, var(--color-brand-300)));

&#x20; transition: height 0.1s linear;

}



/\* ─── Table of contents (scroll spy) ─── \*/

.toc {

&#x20; position: sticky;

&#x20; top: calc(var(--header-height, 60px) + var(--space-6));

&#x20; max-height: calc(100dvh - var(--header-height, 60px) - var(--space-12));

&#x20; overflow-y: auto;

&#x20; scrollbar-width: thin;

&#x20; padding: var(--space-4);

&#x20; font-size: var(--font-size-sm);

}



.toc\_\_title {

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-xs);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-3);

}



.toc-list {

&#x20; list-style: none;

&#x20; padding: 0;

&#x20; margin: 0;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: 2px;

}



.toc-item { }



.toc-link {

&#x20; display: block;

&#x20; padding: 0.3rem 0.75rem;

&#x20; border-radius: var(--radius-md);

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: none;

&#x20; line-height: 1.4;

&#x20; transition:

&#x20;   color      var(--duration-fast),

&#x20;   background var(--duration-fast),

&#x20;   padding-inline-start var(--duration-fast);

&#x20; border-inline-start: 2px solid transparent;

}



.toc-link:hover {

&#x20; color: var(--color-text);

&#x20; background: var(--color-bg-subtle);

}



.toc-link.active {

&#x20; color: var(--color-accent);

&#x20; border-inline-start-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 6%, transparent);

&#x20; font-weight: var(--font-weight-medium);

}



/\* Heading levels \*/

.toc-item\[data-level="2"] .toc-link { }

.toc-item\[data-level="3"] .toc-link { padding-inline-start: 1.5rem; font-size: var(--font-size-xs); }

.toc-item\[data-level="4"] .toc-link { padding-inline-start: 2.5rem; font-size: var(--font-size-xs); }



/\* ─── Back to top button with reading % ─── \*/

.back-top-progress {

&#x20; position: fixed;

&#x20; bottom: var(--space-6);

&#x20; right: var(--space-6);

&#x20; width: 2.75rem;

&#x20; height: 2.75rem;

&#x20; z-index: var(--z-fixed);



&#x20; opacity: 0;

&#x20; translate: 0 1rem;

&#x20; transition:

&#x20;   opacity   var(--duration-normal),

&#x20;   translate var(--duration-normal) var(--ease-bounce);

}



.back-top-progress.visible {

&#x20; opacity: 1;

&#x20; translate: 0 0;

}



.back-top-progress svg {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; rotate: -90deg;

}



.progress-ring {

&#x20; fill: none;

&#x20; stroke: var(--color-bg-muted);

&#x20; stroke-width: 3;

}



.progress-ring--fill {

&#x20; fill: none;

&#x20; stroke: var(--color-accent);

&#x20; stroke-width: 3;

&#x20; stroke-linecap: round;

&#x20; stroke-dasharray: 80;

&#x20; stroke-dashoffset: calc(80 - 80 \* var(--read-progress, 0) / 100);

&#x20; transition: stroke-dashoffset 0.1s;

}



.back-top-btn {

&#x20; position: absolute;

&#x20; inset: 4px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-surface);

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-text-muted);

&#x20; box-shadow: var(--shadow-sm);

&#x20; transition: color var(--duration-fast), background var(--duration-fast);

&#x20; font-size: 0.75rem;

}

.back-top-btn:hover { color: var(--color-accent); }

```



\---



```

╔══════════════════════════════════════════════════════════════════════╗

║              CSS MASTER GUIDE — PARTS I–IX                           ║

╠══════════════════════════════════════════════════════════════════════╣

║  151 chapters · 900+ code examples · \~31,000 lines                  ║

║                                                                      ║

║  NEW IN PART IX:                                                     ║

║  ✅ Split pane / resizable panels (drag handle, collapse)            ║

║  ✅ Gantt chart (tasks, bars, milestones, dependencies)              ║

║  ✅ Onboarding tour (spotlight, tooltip, checklist)                  ║

║  ✅ Music player (full + mini, waveform, equalizer bars)             ║

║  ✅ Blog layouts (post card, article page, share bar, related)       ║

║  ✅ Portfolio grid (masonry, filter animation, category)             ║

║  ✅ Restaurant menu (list + grid, badges, dotted leaders)            ║

║  ✅ Marketing sections (testimonials, CTA, stats, FAQ, how-it-works) ║

║  ✅ Advanced tooltip positioning (anchor API + fallbacks)            ║

║  ✅ Reading progress (line, TOC scroll spy, back-to-top ring)        ║

╚══════════════════════════════════════════════════════════════════════╝

```

