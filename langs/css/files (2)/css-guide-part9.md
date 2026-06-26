# PART IX — CSS: SPECIALIZED INTERFACES & LAYOUTS

---

## 142. SPLIT PANE / RESIZABLE PANELS

```css
/* ─── Split view container ─── */
.split-pane {
  display: flex;
  height: 100%;
  overflow: hidden;
  position: relative;
  user-select: none; /* prevent text selection during drag */
}

.split-pane--vertical {
  flex-direction: column;
}

/* Individual panes */
.pane {
  overflow: auto;
  flex-shrink: 0;
  min-width: 0;
  min-height: 0;
  position: relative;
}

.pane--primary {
  width: var(--pane-size, 50%);
  flex: none;
}

.pane--secondary {
  flex: 1;
}

.split-pane--vertical .pane--primary {
  width: 100%;
  height: var(--pane-size, 50%);
}

/* Resize handle */
.split-handle {
  position: relative;
  flex-shrink: 0;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-border);
  transition: background var(--duration-fast);
}

.split-pane:not(.split-pane--vertical) .split-handle {
  width: 4px;
  cursor: col-resize;
}

.split-pane--vertical .split-handle {
  height: 4px;
  width: 100%;
  cursor: row-resize;
}

.split-handle:hover,
.split-handle.dragging {
  background: var(--color-accent);
}

/* Handle grip dots */
.split-handle__grip {
  display: flex;
  flex-direction: column;
  gap: 3px;
  pointer-events: none;
}

.split-pane:not(.split-pane--vertical) .split-handle__grip {
  flex-direction: row;
}

.split-handle__dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.5;
}

.split-handle:hover .split-handle__dot { opacity: 1; }

/* Dragging state */
.split-pane.is-dragging {
  cursor: col-resize;
}
.split-pane--vertical.is-dragging {
  cursor: row-resize;
}
.split-pane.is-dragging * {
  pointer-events: none;
}

/* Min/max constraints */
.pane { min-width: 120px; min-height: 60px; }

/* Collapse button */
.pane__collapse-btn {
  position: absolute;
  top: 50%;
  translate: 0 -50%;
  right: -12px;
  width: 20px;
  height: 32px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  font-size: 0.5rem;
  color: var(--color-text-muted);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.pane__collapse-btn:hover { background: var(--color-bg-subtle); color: var(--color-text); }

/* Collapsed state */
.pane.collapsed {
  width: 0 !important;
  overflow: hidden;
}
```

---

## 143. GANTT / PROJECT TIMELINE

```css
/* ─── Gantt chart ─── */
.gantt {
  display: grid;
  grid-template-columns: 240px 1fr;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  font-size: var(--font-size-sm);
}

/* Left panel — task names */
.gantt__tasks {
  border-right: 2px solid var(--color-border);
  background: var(--color-surface);
  position: sticky;
  left: 0;
  z-index: 2;
}

.gantt__task-header {
  height: 48px;
  padding: var(--space-3);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
  display: flex;
  align-items: center;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}

.gantt__task-row {
  height: 44px;
  padding: 0 var(--space-3);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  transition: background var(--duration-fast);
}
.gantt__task-row:hover { background: var(--color-bg-subtle); }
.gantt__task-row.selected { background: color-mix(in srgb, var(--color-accent) 8%, transparent); }

.gantt__task-indent {
  width: calc(var(--depth, 0) * 1.5rem);
  flex-shrink: 0;
}

.gantt__task-toggle {
  width: 1rem;
  height: 1rem;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--color-text-muted);
  font-size: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: rotate var(--duration-fast);
}
.gantt__task-row.expanded .gantt__task-toggle { rotate: 90deg; }
.gantt__task-row.leaf .gantt__task-toggle { visibility: hidden; }

.gantt__task-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: var(--font-weight-medium);
}

.gantt__task-assignee {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

/* Right panel — timeline */
.gantt__timeline {
  overflow-x: auto;
  background: var(--color-surface);
  position: relative;
}

/* Month headers */
.gantt__months {
  display: flex;
  height: 24px;
  position: sticky;
  top: 0;
  z-index: 1;
  background: var(--color-bg-subtle);
  border-bottom: 1px solid var(--color-border);
}

.gantt__month {
  height: 100%;
  border-right: 1px solid var(--color-border);
  padding: 0 var(--space-2);
  display: flex;
  align-items: center;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  flex-shrink: 0;
}

/* Day headers */
.gantt__days {
  display: flex;
  height: 24px;
  position: sticky;
  top: 24px;
  z-index: 1;
  background: var(--color-bg-subtle);
  border-bottom: 1px solid var(--color-border);
}

.gantt__day {
  height: 100%;
  width: var(--day-width, 32px);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem;
  color: var(--color-text-subtle);
  border-right: 1px solid var(--color-border-subtle);
}

.gantt__day.today {
  color: var(--color-accent);
  font-weight: var(--font-weight-bold);
  background: color-mix(in srgb, var(--color-accent) 8%, transparent);
}

.gantt__day.weekend { background: var(--color-bg-subtle); }

/* Chart rows */
.gantt__rows { position: relative; }

.gantt__row {
  height: 44px;
  border-bottom: 1px solid var(--color-border);
  position: relative;
  display: flex;
  align-items: center;
}

/* Weekend columns */
.gantt__row::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    to right,
    transparent 0,
    transparent calc(5 * var(--day-width, 32px)),
    var(--color-bg-subtle) calc(5 * var(--day-width, 32px)),
    var(--color-bg-subtle) calc(7 * var(--day-width, 32px))
  );
  pointer-events: none;
}

/* Today indicator */
.gantt__today-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left: var(--today-offset, 0);
  width: 2px;
  background: var(--color-accent);
  opacity: 0.7;
  pointer-events: none;
  z-index: 1;
}

/* Task bars */
.gantt__bar {
  position: absolute;
  height: 24px;
  border-radius: var(--radius-md);
  background: var(--bar-color, var(--color-brand-500));
  left: var(--bar-start, 0);
  width: var(--bar-width, 100px);
  display: flex;
  align-items: center;
  padding-inline: var(--space-2);
  overflow: hidden;
  cursor: grab;
  transition: filter var(--duration-fast), box-shadow var(--duration-fast);
  z-index: 1;
}

.gantt__bar:hover {
  filter: brightness(1.1);
  box-shadow: var(--shadow-md);
}

.gantt__bar.dragging { cursor: grabbing; opacity: 0.8; z-index: 5; }

/* Progress fill */
.gantt__bar-fill {
  position: absolute;
  inset-block: 0;
  inset-inline-start: 0;
  width: var(--progress, 0%);
  background: rgb(0 0 0 / 0.15);
  border-radius: inherit;
}

.gantt__bar-label {
  position: relative;
  font-size: var(--font-size-xs);
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  z-index: 1;
}

/* Milestone diamond */
.gantt__milestone {
  position: absolute;
  width: 16px;
  height: 16px;
  background: var(--color-warning-500);
  rotate: 45deg;
  border: 2px solid white;
  left: var(--milestone-pos, 0);
  translate: -50% 0;
  cursor: pointer;
  z-index: 2;
  transition: scale var(--duration-fast) var(--ease-bounce);
}
.gantt__milestone:hover { scale: 1.3; }

/* Dependency arrow */
.gantt__dependency {
  position: absolute;
  pointer-events: none;
  stroke: var(--color-neutral-400);
  stroke-width: 1.5;
  fill: none;
  stroke-dasharray: 4 2;
}

/* Group/parent task bar */
.gantt__bar--group {
  background: var(--color-neutral-700);
  height: 16px;
  border-radius: 2px;
}
.gantt__bar--group::before,
.gantt__bar--group::after {
  content: '';
  position: absolute;
  top: 100%;
  width: 8px;
  height: 8px;
  background: inherit;
}
.gantt__bar--group::before { left: 0; clip-path: polygon(0 0, 100% 0, 0 100%); }
.gantt__bar--group::after  { right: 0; clip-path: polygon(0 0, 100% 0, 100% 100%); }
```

---

## 144. ONBOARDING TOUR / PRODUCT WALKTHROUGH

```css
/* ─── Tour spotlight ─── */
.tour-overlay {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal);
  pointer-events: none;
}

/* Spotlight effect using box-shadow */
.tour-spotlight {
  position: fixed;
  z-index: calc(var(--z-modal) + 1);
  border-radius: var(--spotlight-radius, var(--radius-lg));
  box-shadow: 0 0 0 9999px rgb(0 0 0 / 0.6);
  pointer-events: none;
  transition:
    top    0.4s var(--ease-out),
    left   0.4s var(--ease-out),
    width  0.4s var(--ease-out),
    height 0.4s var(--ease-out);
}

/* Pulsing border on spotlight */
.tour-spotlight::after {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: calc(var(--spotlight-radius, var(--radius-lg)) + 3px);
  border: 2px solid var(--color-accent);
  animation: spotlight-pulse 2s ease-in-out infinite;
}

@keyframes spotlight-pulse {
  0%, 100% { opacity: 1; inset: -3px; }
  50%       { opacity: 0.5; inset: -6px; }
}

/* ─── Tour tooltip ─── */
.tour-tooltip {
  position: fixed;
  z-index: calc(var(--z-modal) + 2);
  background: var(--color-surface);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-2xl);
  padding: var(--space-5);
  width: 280px;
  transition:
    top  0.4s var(--ease-out),
    left 0.4s var(--ease-out);
  animation: tooltip-appear 0.3s var(--ease-bounce);
}

@keyframes tooltip-appear {
  from { opacity: 0; scale: 0.92; }
}

/* Arrow pointer */
.tour-tooltip::before {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  background: var(--color-surface);
  rotate: 45deg;
}

.tour-tooltip[data-placement="top"]::before    { bottom: -6px; left: 50%; translate: -50% 0; box-shadow: 2px 2px 4px rgb(0 0 0 / 0.1); }
.tour-tooltip[data-placement="bottom"]::before { top: -6px; left: 50%; translate: -50% 0; }
.tour-tooltip[data-placement="left"]::before   { right: -6px; top: 50%; translate: 0 -50%; }
.tour-tooltip[data-placement="right"]::before  { left: -6px; top: 50%; translate: 0 -50%; }

/* Tooltip content */
.tour-tooltip__step {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  margin-block-end: var(--space-2);
}

.tour-tooltip__title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-2);
}

.tour-tooltip__desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-block-end: var(--space-4);
}

.tour-tooltip__media {
  width: 100%;
  border-radius: var(--radius-lg);
  margin-block-end: var(--space-4);
  overflow: hidden;
}

.tour-tooltip__media img,
.tour-tooltip__media video {
  width: 100%;
  height: auto;
  display: block;
}

/* Progress dots */
.tour-dots {
  display: flex;
  justify-content: center;
  gap: var(--space-1);
  margin-block-end: var(--space-4);
}

.tour-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-border-strong);
  transition: background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce), width var(--duration-fast);
}

.tour-dot.active {
  background: var(--color-accent);
  width: 18px;
  border-radius: var(--radius-full);
}

/* Actions */
.tour-tooltip__actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.tour-skip {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  background: none;
  border: none;
  cursor: pointer;
  margin-inline-end: auto;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 2px;
}
.tour-skip:hover { color: var(--color-text); }

/* ─── Onboarding checklist ─── */
.onboarding-checklist {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-5);
  max-width: 360px;
}

.checklist-header {
  margin-block-end: var(--space-4);
}

.checklist-title {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-base);
  margin-block-end: var(--space-1);
}

.checklist-subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.checklist-progress {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-block: var(--space-3);
}

.checklist-bar {
  flex: 1;
  height: 6px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.checklist-bar__fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: inherit;
  width: var(--progress, 0%);
  transition: width 0.5s var(--ease-out);
}

.checklist-count {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}

.checklist-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.checklist-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: background var(--duration-fast);
  border: 1px solid transparent;
}
.checklist-item:hover { background: var(--color-bg-subtle); }
.checklist-item.active { border-color: var(--color-accent); background: color-mix(in srgb, var(--color-accent) 5%, transparent); }

.checklist-item__icon {
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-lg);
  background: var(--color-bg-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
  transition: background var(--duration-fast);
}

.checklist-item.done .checklist-item__icon {
  background: var(--color-success-100);
  color: var(--color-success-600);
}

.checklist-item__text {
  flex: 1;
  min-width: 0;
}

.checklist-item__title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.checklist-item.done .checklist-item__title {
  text-decoration: line-through;
  color: var(--color-text-muted);
}

.checklist-item__desc {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

/* Completion celebration */
.checklist-complete {
  text-align: center;
  padding: var(--space-6);
}

.checklist-complete__emoji {
  font-size: 3rem;
  animation: bounce 0.6s var(--ease-bounce);
}

@keyframes bounce {
  0%   { translate: 0 0; }
  40%  { translate: 0 -20px; }
  70%  { translate: 0 -10px; }
  100% { translate: 0 0; }
}
```

---

## 145. MUSIC PLAYER

```css
/* ─── Full music player ─── */
.music-player {
  background: var(--player-bg, #1a1a2e);
  color: white;
  border-radius: var(--radius-2xl);
  overflow: hidden;
  max-width: 360px;
  box-shadow: var(--shadow-2xl);
}

/* Album art */
.player-art {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.player-art img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: scale var(--duration-slow) var(--ease-out);
}

.music-player.playing .player-art img {
  animation: album-spin 20s linear infinite;
}

/* Spinning album (alternative) */
@keyframes album-spin {
  to { rotate: 360deg; }
}

/* Playing indicator overlay */
.player-art__eq {
  position: absolute;
  bottom: var(--space-4);
  right: var(--space-4);
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 24px;
  opacity: 0;
  transition: opacity var(--duration-fast);
}

.music-player.playing .player-art__eq { opacity: 1; }

.player-art__bar {
  width: 3px;
  border-radius: 2px;
  background: white;
  animation: eq-bar 0.8s ease-in-out infinite alternate;
}
.player-art__bar:nth-child(1) { height: 40%; animation-delay: 0s; }
.player-art__bar:nth-child(2) { height: 70%; animation-delay: 0.15s; }
.player-art__bar:nth-child(3) { height: 90%; animation-delay: 0.3s; }
.player-art__bar:nth-child(4) { height: 55%; animation-delay: 0.1s; }
.player-art__bar:nth-child(5) { height: 80%; animation-delay: 0.25s; }

@keyframes eq-bar {
  from { height: 20%; }
  to   { /* uses var */ }
}

/* Favorite button on art */
.player-art__like {
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background: rgb(0 0 0 / 0.3);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255 255 255 / 0.15);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: scale var(--duration-fast) var(--ease-bounce);
}
.player-art__like:hover { scale: 1.1; }
.player-art__like.liked { color: var(--color-danger-400); }

/* Player controls */
.player-controls {
  padding: var(--space-5);
}

.player-info {
  margin-block-end: var(--space-4);
}

.player-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.player-artist {
  font-size: var(--font-size-sm);
  color: rgba(255 255 255 / 0.6);
  margin-block-start: var(--space-1);
}

/* Seek bar */
.player-seek {
  margin-block-end: var(--space-4);
}

.player-track {
  width: 100%;
  height: 4px;
  appearance: none;
  background: rgba(255 255 255 / 0.2);
  border-radius: var(--radius-full);
  outline: none;
  cursor: pointer;
  position: relative;
  margin-block-end: var(--space-2);
}

.player-track::-webkit-slider-thumb {
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: white;
  cursor: pointer;
  box-shadow: 0 0 4px rgba(0 0 0 / 0.4);
  transition: scale var(--duration-fast) var(--ease-bounce);
}
.player-track:hover::-webkit-slider-thumb { scale: 1.3; }

/* Progress fill for range */
.player-track {
  background: linear-gradient(
    to right,
    white var(--seek-progress, 0%),
    rgba(255 255 255 / 0.2) var(--seek-progress, 0%)
  );
}

.player-times {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.5);
  font-variant-numeric: tabular-nums;
  font-family: var(--font-mono);
}

/* Main controls row */
.player-main-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-block-end: var(--space-3);
}

.player-btn {
  background: none;
  border: none;
  color: rgba(255 255 255 / 0.7);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: color var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
}
.player-btn:hover { color: white; scale: 1.1; }
.player-btn.active { color: var(--color-accent); }

.player-btn--play {
  width: 3.5rem;
  height: 3.5rem;
  background: white;
  color: var(--player-bg, #1a1a2e);
  border-radius: 50%;
  font-size: 1.25rem;
  box-shadow: 0 4px 16px rgba(0 0 0 / 0.3);
  transition: scale var(--duration-fast) var(--ease-bounce), box-shadow var(--duration-fast);
}
.player-btn--play:hover { scale: 1.07; box-shadow: 0 6px 20px rgba(0 0 0 / 0.4); }
.player-btn--play:active { scale: 0.95; }

/* Volume row */
.player-volume {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.volume-track {
  flex: 1;
  height: 3px;
  appearance: none;
  background: linear-gradient(
    to right,
    rgba(255 255 255 / 0.7) var(--volume, 70%),
    rgba(255 255 255 / 0.15) var(--volume, 70%)
  );
  border-radius: var(--radius-full);
  outline: none;
  cursor: pointer;
}
.volume-track::-webkit-slider-thumb {
  appearance: none;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: white;
  cursor: pointer;
}

/* Mini player variant */
.music-player--mini {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-2xl);
  max-width: none;
  width: 100%;
}

.music-player--mini .player-art {
  width: 3rem;
  height: 3rem;
  border-radius: var(--radius-lg);
  aspect-ratio: auto;
  flex-shrink: 0;
}
.music-player--mini .player-info { flex: 1; margin: 0; }
.music-player--mini .player-title { font-size: var(--font-size-sm); }
.music-player--mini .player-artist { font-size: var(--font-size-xs); }
```

---

## 146. BLOG / ARTICLE LAYOUTS

```css
/* ─── Blog list page ─── */
.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr));
  gap: var(--space-8);
}

/* Featured first post */
.blog-grid .post-card:first-child {
  grid-column: 1 / -1;
}

.blog-grid .post-card:first-child .post-card__image {
  aspect-ratio: 2 / 1;
}

/* ─── Post card ─── */
.post-card {
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-xl);
  overflow: hidden;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  transition:
    box-shadow var(--duration-normal),
    translate  var(--duration-normal);
  text-decoration: none;
  color: inherit;
}

.post-card:hover {
  box-shadow: var(--shadow-lg);
  translate: 0 -2px;
}

.post-card__image {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.post-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: scale var(--duration-slow) var(--ease-out);
}

.post-card:hover .post-card__image img { scale: 1.04; }

.post-card__body {
  padding: var(--space-5);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.post-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-block-end: var(--space-3);
}

.post-tag {
  padding: 0.2em 0.6em;
  background: var(--tag-bg, var(--color-brand-100));
  color: var(--tag-color, var(--color-brand-700));
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-decoration: none;
  transition: filter var(--duration-fast);
}
.post-tag:hover { filter: brightness(0.9); }

.post-card__title {
  font-size: var(--step-1);
  font-weight: var(--font-weight-bold);
  line-height: 1.35;
  margin-block-end: var(--space-3);
  text-wrap: balance;
  flex: 1;
}

.post-card__excerpt {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.6;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-block-end: var(--space-4);
}

.post-card__meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-block-start: auto;
  padding-block-start: var(--space-4);
  border-top: 1px solid var(--color-border);
}

.post-card__author {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.post-card__author img {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  object-fit: cover;
}

.post-card__read-time {
  margin-inline-start: auto;
  display: flex;
  align-items: center;
  gap: 0.25em;
}

/* ─── Article page ─── */
.article-layout {
  display: grid;
  grid-template-columns: 1fr min(65ch, 100%) 1fr;
  row-gap: 0;
}

.article-layout > * {
  grid-column: 2;
}

/* Full-width elements */
.article-layout .full-width {
  grid-column: 1 / -1;
  width: 100%;
}

/* Wide elements (breakout) */
.article-layout .breakout {
  grid-column: 1 / -1;
  max-width: min(100%, 900px);
  margin-inline: auto;
  padding-inline: var(--space-4);
}

/* Article header */
.article-header {
  padding-block: var(--space-8);
}

.article-header__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-block-end: var(--space-4);
}

.article-header__title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: var(--font-weight-black);
  line-height: 1.1;
  letter-spacing: -0.03em;
  text-wrap: balance;
  margin-block-end: var(--space-5);
}

.article-header__subtitle {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: var(--color-text-muted);
  line-height: 1.6;
  max-width: 55ch;
  margin-block-end: var(--space-6);
  text-wrap: pretty;
}

.article-header__meta {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding-block: var(--space-4);
  border-block: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.article-author {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.article-author__avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
}

.article-author__name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
}

.article-author__bio {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.article-meta-item {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

/* Hero image */
.article-hero {
  width: 100%;
  aspect-ratio: 2 / 1;
  object-fit: cover;
  margin-block: var(--space-8);
}

.article-hero-caption {
  text-align: center;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-style: italic;
  margin-block-start: -var(--space-6);
  margin-block-end: var(--space-8);
}

/* Reading progress bar */
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-accent);
  width: var(--read-progress, 0%);
  z-index: var(--z-top);
  transition: width 0.05s linear;
  box-shadow: 0 0 8px var(--color-accent);
}

/* Share bar */
.share-bar {
  position: sticky;
  top: 50%;
  translate: 0 -50%;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  width: fit-content;
  grid-column: 1;
  margin-inline-start: auto;
  margin-inline-end: var(--space-4);
}

.share-btn {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-muted);
  font-size: 0.875rem;
  transition:
    background var(--duration-fast),
    border-color var(--duration-fast),
    color var(--duration-fast),
    scale var(--duration-fast) var(--ease-bounce);
}
.share-btn:hover { scale: 1.1; background: var(--color-bg-subtle); color: var(--color-text); }
.share-btn.liked { color: var(--color-danger-500); border-color: var(--color-danger-200); background: var(--color-danger-100); }

/* Related posts */
.related-posts {
  margin-block-start: var(--space-16);
  padding-block-start: var(--space-8);
  border-top: 1px solid var(--color-border);
}

.related-posts__title {
  font-size: var(--step-1);
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-6);
}

.related-posts__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: var(--space-6);
}
```

---

## 147. PORTFOLIO / SHOWCASE PATTERNS

```css
/* ─── Portfolio grid ─── */
.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
  gap: var(--space-4);
}

/* Asymmetric masonry variant */
.portfolio-masonry {
  columns: 3 280px;
  column-gap: var(--space-4);
}

.portfolio-masonry .portfolio-item {
  break-inside: avoid;
  margin-block-end: var(--space-4);
}

/* Portfolio item */
.portfolio-item {
  position: relative;
  border-radius: var(--radius-xl);
  overflow: hidden;
  cursor: pointer;
  background: var(--color-bg-muted);
}

.portfolio-item__media {
  display: block;
  width: 100%;
  height: auto;
  transition: scale var(--duration-slow) var(--ease-out), filter var(--duration-slow);
}

.portfolio-item:hover .portfolio-item__media {
  scale: 1.06;
  filter: brightness(0.7);
}

/* Overlay info */
.portfolio-item__info {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: var(--space-4);
  background: linear-gradient(to top, rgb(0 0 0 / 0.8) 0%, transparent 60%);
  opacity: 0;
  translate: 0 8px;
  transition:
    opacity   var(--duration-normal),
    translate var(--duration-normal) var(--ease-out);
}

.portfolio-item:hover .portfolio-item__info {
  opacity: 1;
  translate: 0 0;
}

.portfolio-item__title {
  color: white;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-1);
}

.portfolio-item__desc {
  color: rgba(255 255 255 / 0.7);
  font-size: var(--font-size-xs);
}

.portfolio-item__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-block-start: var(--space-2);
}

.portfolio-item__tag {
  padding: 0.15em 0.5em;
  background: rgba(255 255 255 / 0.15);
  color: white;
  border-radius: var(--radius-full);
  font-size: 0.625rem;
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  backdrop-filter: blur(4px);
}

/* Category filter */
.portfolio-filters {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-block-end: var(--space-6);
}

.portfolio-filter-btn {
  padding: 0.4rem 1rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  font: inherit;
  font-size: var(--font-size-sm);
  cursor: pointer;
  color: var(--color-text-muted);
  transition:
    background      var(--duration-fast),
    border-color    var(--duration-fast),
    color           var(--duration-fast),
    scale           var(--duration-fast) var(--ease-bounce);
}
.portfolio-filter-btn:hover { border-color: var(--color-accent); color: var(--color-accent); }
.portfolio-filter-btn.active {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: white;
}

/* Filter animation */
.portfolio-item {
  transition:
    opacity   var(--duration-normal) var(--ease-out),
    scale     var(--duration-normal) var(--ease-bounce),
    translate var(--duration-normal) var(--ease-out);
}

.portfolio-item.hidden {
  opacity: 0;
  scale: 0.9;
  pointer-events: none;
  position: absolute;
}
```

---

## 148. RESTAURANT MENU

```css
/* ─── Restaurant menu layout ─── */
.menu-page {
  max-width: 900px;
  margin-inline: auto;
  padding: var(--space-8) var(--space-4);
}

/* Menu header */
.menu-header {
  text-align: center;
  padding-block: var(--space-10);
  position: relative;
}

.menu-header__logo {
  font-family: Georgia, serif;
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 700;
  letter-spacing: -0.03em;
}

.menu-header__tagline {
  font-style: italic;
  color: var(--color-text-muted);
  font-size: var(--font-size-lg);
  margin-block-start: var(--space-2);
}

.menu-divider {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-block: var(--space-6);
  color: var(--color-accent);
}
.menu-divider::before,
.menu-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: currentColor;
  opacity: 0.3;
}
.menu-divider::before { content: '✦ ✦ ✦'; display: block; flex: none; }

/* Menu sections */
.menu-section {
  margin-block-end: var(--space-10);
}

.menu-section__title {
  font-family: Georgia, serif;
  font-size: var(--step-2);
  font-weight: 700;
  text-align: center;
  margin-block-end: var(--space-2);
  color: var(--color-text);
}

.menu-section__subtitle {
  text-align: center;
  font-style: italic;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  margin-block-end: var(--space-6);
}

/* Menu items */
.menu-item {
  display: flex;
  gap: var(--space-4);
  padding-block: var(--space-4);
  border-bottom: 1px dotted var(--color-border);
  align-items: flex-start;
}
.menu-item:last-child { border: none; }

.menu-item__image {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-lg);
  object-fit: cover;
  flex-shrink: 0;
}

.menu-item__info { flex: 1; }

.menu-item__header {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
  margin-block-end: var(--space-1);
}

.menu-item__name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-base);
}

/* Dotted leader */
.menu-item__leader {
  flex: 1;
  border-bottom: 1px dotted var(--color-border);
  margin-block-end: 4px;
}

.menu-item__price {
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
  color: var(--color-text);
  white-space: nowrap;
}

.menu-item__description {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.5;
}

.menu-item__badges {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-block-start: var(--space-2);
}

.menu-badge {
  padding: 0.15em 0.5em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
}

.menu-badge--spicy    { background: #fef2f2; color: #dc2626; }
.menu-badge--vegan    { background: #f0fdf4; color: #16a34a; }
.menu-badge--gluten   { background: #fefce8; color: #ca8a04; }
.menu-badge--popular  { background: #fdf4ff; color: #9333ea; }
.menu-badge--new      { background: #eff6ff; color: #2563eb; }
.menu-badge--chef     { background: var(--color-warning-100); color: var(--color-warning-700); }

/* Grid menu variant */
.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-4);
}

.menu-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  cursor: pointer;
  transition:
    box-shadow var(--duration-normal),
    translate  var(--duration-normal);
}
.menu-card:hover { box-shadow: var(--shadow-md); translate: 0 -2px; }

.menu-card__image { width: 100%; aspect-ratio: 4/3; object-fit: cover; }
.menu-card__body { padding: var(--space-3); }
.menu-card__name { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.menu-card__price {
  font-weight: var(--font-weight-bold);
  color: var(--color-accent);
  margin-block-start: var(--space-1);
}
```

---

## 149. MARKETING PAGE SECTIONS

```css
/* ─── Testimonials ─── */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
  gap: var(--space-6);
}

.testimonial-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  transition: box-shadow var(--duration-normal);
}
.testimonial-card:hover { box-shadow: var(--shadow-lg); }

.testimonial-stars {
  display: flex;
  gap: 2px;
  color: var(--color-warning-400);
  font-size: 0.875rem;
}

.testimonial-quote {
  font-size: var(--font-size-base);
  line-height: 1.7;
  color: var(--color-text);
  flex: 1;
  font-style: italic;
}

.testimonial-quote::before { content: '"'; font-size: 2em; line-height: 0; vertical-align: -0.4em; color: var(--color-accent); opacity: 0.4; margin-inline-end: 0.1em; }

.testimonial-author {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding-block-start: var(--space-4);
  border-top: 1px solid var(--color-border);
}

.testimonial-author img {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
}

.testimonial-author__name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
}

.testimonial-author__role {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

/* ─── Logo cloud / Social proof ─── */
.logo-cloud {
  text-align: center;
  padding-block: var(--space-10);
}

.logo-cloud__label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  margin-block-end: var(--space-6);
}

.logo-cloud__logos {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: var(--space-8);
  filter: grayscale(100%);
  opacity: 0.5;
}

.logo-cloud__logos img { height: 28px; width: auto; }

/* Marquee version */
.logo-cloud--marquee .logo-cloud__logos {
  flex-wrap: nowrap;
  overflow: hidden;
  -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
  mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
}

.logo-cloud--marquee .logo-cloud__inner {
  display: flex;
  gap: var(--space-8);
  animation: logo-scroll 20s linear infinite;
  flex-shrink: 0;
}

@keyframes logo-scroll {
  from { translate: 0; }
  to   { translate: -50%; }
}

/* ─── CTA section ─── */
.cta-section {
  background: var(--color-accent);
  color: white;
  padding: clamp(3rem, 8vw, 8rem) clamp(1rem, 5vw, 4rem);
  border-radius: var(--radius-3xl);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  inset: -50%;
  background:
    radial-gradient(circle at 30% 50%, rgba(255 255 255 / 0.1) 0%, transparent 50%),
    radial-gradient(circle at 70% 50%, rgba(255 255 255 / 0.08) 0%, transparent 50%);
}

.cta-section > * { position: relative; z-index: 1; }

.cta-section__title {
  font-size: clamp(1.75rem, 4vw, 3rem);
  font-weight: var(--font-weight-black);
  line-height: 1.15;
  text-wrap: balance;
  margin-block-end: var(--space-4);
}

.cta-section__desc {
  font-size: clamp(1rem, 2vw, 1.25rem);
  opacity: 0.85;
  max-width: 50ch;
  margin-inline: auto;
  margin-block-end: var(--space-8);
  text-wrap: pretty;
}

.cta-section__actions {
  display: flex;
  gap: var(--space-4);
  justify-content: center;
  flex-wrap: wrap;
}

.btn--light {
  background: white;
  color: var(--color-accent);
  font-weight: var(--font-weight-bold);
}
.btn--light:hover { background: rgba(255 255 255 / 0.9); }

.btn--outline-white {
  background: transparent;
  border: 2px solid rgba(255 255 255 / 0.5);
  color: white;
}
.btn--outline-white:hover { background: rgba(255 255 255 / 0.1); border-color: white; }

/* ─── Stats / Numbers section ─── */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr));
  gap: var(--space-8);
  text-align: center;
}

.stat-item { }

.stat-item__number {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: var(--font-weight-black);
  line-height: 1;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, var(--color-accent), color-mix(in oklch, var(--color-accent) 50%, var(--color-brand-300)));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.stat-item__label {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  margin-block-start: var(--space-2);
  font-weight: var(--font-weight-medium);
}

/* Number counter animation */
.stat-item__number {
  animation: count-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 50%;
}

@keyframes count-in {
  from { opacity: 0; translate: 0 20px; }
}

/* ─── FAQ accordion ─── */
.faq-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.faq-item {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: border-color var(--duration-fast);
}
.faq-item.open { border-color: var(--color-accent); }

.faq-question {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-5);
  cursor: pointer;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-base);
  list-style: none;
  user-select: none;
  transition: color var(--duration-fast);
}
.faq-item.open .faq-question { color: var(--color-accent); }

.faq-question::marker { display: none; }
.faq-question::-webkit-details-marker { display: none; }

.faq-icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--color-bg-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 1rem;
  transition:
    background  var(--duration-fast),
    rotate      var(--duration-fast) var(--ease-out);
}
.faq-item.open .faq-icon {
  background: var(--color-accent);
  color: white;
  rotate: 45deg;
}

.faq-answer {
  padding: 0 var(--space-5) var(--space-5);
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  line-height: 1.7;
}

/* ─── How it works / Steps ─── */
.how-it-works {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr));
  gap: var(--space-8);
  position: relative;
}

/* Connecting line between steps */
.how-it-works::before {
  content: '';
  position: absolute;
  top: 2rem;
  left: 2.5rem;
  right: 2.5rem;
  height: 2px;
  background: linear-gradient(to right, var(--color-accent), color-mix(in oklch, var(--color-accent) 50%, transparent));
  opacity: 0.3;
}

@media (max-width: 768px) {
  .how-it-works::before { display: none; }
}

.step-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  position: relative;
}

.step-card__num {
  width: 4rem;
  height: 4rem;
  border-radius: var(--radius-2xl);
  background: color-mix(in srgb, var(--color-accent) 12%, transparent);
  border: 2px solid color-mix(in srgb, var(--color-accent) 20%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--step-1);
  font-weight: var(--font-weight-black);
  color: var(--color-accent);
}

.step-card__title {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-lg);
}

.step-card__desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.6;
}
```

---

## 150. ADVANCED TOOLTIP POSITIONING

```css
/* ─── Complete tooltip system via anchor positioning ─── */

/* The anchor target */
[data-tooltip-target] {
  anchor-name: --tooltip-anchor;
}

/* Base tooltip */
.tooltip-popup {
  position: fixed;
  position-anchor: --tooltip-anchor;

  /* Default: top center */
  bottom: calc(anchor(top) + 8px);
  left:  anchor(center);
  translate: -50% 0;

  padding: 0.4rem 0.75rem;
  background: var(--color-neutral-900);
  color: white;
  font-size: var(--font-size-xs);
  border-radius: var(--radius-md);
  white-space: nowrap;
  pointer-events: none;
  max-width: 240px;
  white-space: normal;
  line-height: 1.4;
  box-shadow: var(--shadow-lg);

  /* Auto-flip if out of viewport */
  position-try-fallbacks:
    --tooltip-bottom,
    --tooltip-right,
    --tooltip-left;
}

@position-try --tooltip-bottom {
  top:    calc(anchor(bottom) + 8px);
  bottom: auto;
  left:   anchor(center);
  translate: -50% 0;
}

@position-try --tooltip-right {
  left:    calc(anchor(right) + 8px);
  bottom:  auto;
  right:   auto;
  top:     anchor(center);
  translate: 0 -50%;
}

@position-try --tooltip-left {
  right:   calc(100% - anchor(left) + 8px);
  left:    auto;
  bottom:  auto;
  top:     anchor(center);
  translate: 0 -50%;
}

/* CSS-only fallback (no anchor positioning) */
@supports not (anchor-name: --a) {
  .tooltip-wrapper {
    position: relative;
    display: inline-block;
  }

  .tooltip-popup-fallback {
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    translate: -50% 0;
    z-index: var(--z-tooltip);
    width: max-content;
    max-width: 240px;

    opacity: 0;
    translate: -50% 4px;
    transition:
      opacity   var(--duration-fast),
      translate var(--duration-fast);
    pointer-events: none;
  }

  .tooltip-wrapper:hover .tooltip-popup-fallback,
  .tooltip-wrapper:focus-within .tooltip-popup-fallback {
    opacity: 1;
    translate: -50% 0;
  }
}

/* ─── Rich tooltip ─── */
.tooltip-rich {
  position: fixed;
  position-anchor: --rich-anchor;
  width: 280px;

  top:  calc(anchor(bottom) + 8px);
  left: anchor(center);
  translate: -50% 0;

  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  padding: var(--space-4);
  pointer-events: none;

  position-try-fallbacks: --rich-above;
}

@position-try --rich-above {
  top:    auto;
  bottom: calc(anchor(top) + 8px);
  left:   anchor(center);
  translate: -50% 0;
}

.tooltip-rich__title {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  margin-block-end: var(--space-1);
}

.tooltip-rich__body {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  line-height: 1.5;
}

.tooltip-rich__image {
  width: 100%;
  border-radius: var(--radius-md);
  margin-block-end: var(--space-3);
  object-fit: cover;
  height: 120px;
}
```

---

## 151. READING PROGRESS & TOC

```css
/* ─── Reading progress tracker ─── */
.reading-container {
  position: relative;
}

/* Progress line in margin */
.reading-progress-line {
  position: fixed;
  top: var(--header-height, 0);
  bottom: 0;
  left: 0;
  width: 3px;
  z-index: var(--z-fixed);
}

.reading-progress-line__track {
  width: 100%;
  height: 100%;
  background: var(--color-border);
}

.reading-progress-line__fill {
  width: 100%;
  height: var(--read-progress, 0%);
  background: linear-gradient(to bottom, var(--color-accent), color-mix(in oklch, var(--color-accent) 50%, var(--color-brand-300)));
  transition: height 0.1s linear;
}

/* ─── Table of contents (scroll spy) ─── */
.toc {
  position: sticky;
  top: calc(var(--header-height, 60px) + var(--space-6));
  max-height: calc(100dvh - var(--header-height, 60px) - var(--space-12));
  overflow-y: auto;
  scrollbar-width: thin;
  padding: var(--space-4);
  font-size: var(--font-size-sm);
}

.toc__title {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  margin-block-end: var(--space-3);
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toc-item { }

.toc-link {
  display: block;
  padding: 0.3rem 0.75rem;
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  text-decoration: none;
  line-height: 1.4;
  transition:
    color      var(--duration-fast),
    background var(--duration-fast),
    padding-inline-start var(--duration-fast);
  border-inline-start: 2px solid transparent;
}

.toc-link:hover {
  color: var(--color-text);
  background: var(--color-bg-subtle);
}

.toc-link.active {
  color: var(--color-accent);
  border-inline-start-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 6%, transparent);
  font-weight: var(--font-weight-medium);
}

/* Heading levels */
.toc-item[data-level="2"] .toc-link { }
.toc-item[data-level="3"] .toc-link { padding-inline-start: 1.5rem; font-size: var(--font-size-xs); }
.toc-item[data-level="4"] .toc-link { padding-inline-start: 2.5rem; font-size: var(--font-size-xs); }

/* ─── Back to top button with reading % ─── */
.back-top-progress {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  width: 2.75rem;
  height: 2.75rem;
  z-index: var(--z-fixed);

  opacity: 0;
  translate: 0 1rem;
  transition:
    opacity   var(--duration-normal),
    translate var(--duration-normal) var(--ease-bounce);
}

.back-top-progress.visible {
  opacity: 1;
  translate: 0 0;
}

.back-top-progress svg {
  width: 100%;
  height: 100%;
  rotate: -90deg;
}

.progress-ring {
  fill: none;
  stroke: var(--color-bg-muted);
  stroke-width: 3;
}

.progress-ring--fill {
  fill: none;
  stroke: var(--color-accent);
  stroke-width: 3;
  stroke-linecap: round;
  stroke-dasharray: 80;
  stroke-dashoffset: calc(80 - 80 * var(--read-progress, 0) / 100);
  transition: stroke-dashoffset 0.1s;
}

.back-top-btn {
  position: absolute;
  inset: 4px;
  border-radius: 50%;
  background: var(--color-surface);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  box-shadow: var(--shadow-sm);
  transition: color var(--duration-fast), background var(--duration-fast);
  font-size: 0.75rem;
}
.back-top-btn:hover { color: var(--color-accent); }
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║              CSS MASTER GUIDE — PARTS I–IX                           ║
╠══════════════════════════════════════════════════════════════════════╣
║  151 chapters · 900+ code examples · ~31,000 lines                  ║
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
