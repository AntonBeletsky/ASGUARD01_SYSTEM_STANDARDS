# PART X — CSS: ADVANCED INTERFACES & COMPLETE REFERENCE

---

## 152. IDE / CODE EDITOR MULTI-PANEL LAYOUT

```css
/* ─── IDE shell ─── */
.ide {
  display: grid;
  grid-template-areas:
    "titlebar  titlebar  titlebar"
    "activity  sidebar   main"
    "activity  sidebar   statusbar";
  grid-template-columns: 48px 240px 1fr;
  grid-template-rows: 35px 1fr 22px;
  height: 100dvh;
  background: #1e1e1e;
  color: #d4d4d4;
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  overflow: hidden;
}

/* Title bar */
.ide-titlebar {
  grid-area: titlebar;
  background: #3c3c3c;
  display: flex;
  align-items: center;
  padding-inline: var(--space-4);
  gap: var(--space-2);
  border-bottom: 1px solid #252525;
  user-select: none;
}

.ide-titlebar__dots {
  display: flex;
  gap: 6px;
  margin-inline-end: var(--space-4);
}

.ide-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}
.ide-dot--red    { background: #ff5f57; }
.ide-dot--yellow { background: #febc2e; }
.ide-dot--green  { background: #28c840; }

.ide-titlebar__title {
  color: rgba(255 255 255 / 0.6);
  font-size: var(--font-size-xs);
  flex: 1;
  text-align: center;
}

/* Activity bar (leftmost icons) */
.ide-activity {
  grid-area: activity;
  background: #333333;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-block: var(--space-2);
  gap: var(--space-1);
  border-right: 1px solid #252525;
}

.ide-activity-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  color: rgba(255 255 255 / 0.5);
  font-size: 1.125rem;
  position: relative;
  transition: color var(--duration-fast);
}

.ide-activity-btn:hover { color: rgba(255 255 255 / 0.85); }
.ide-activity-btn.active { color: white; }

/* Active indicator */
.ide-activity-btn.active::before {
  content: '';
  position: absolute;
  left: -4px;
  top: 50%;
  translate: 0 -50%;
  height: 60%;
  width: 2px;
  background: #0078d4;
  border-radius: 0 2px 2px 0;
}

/* Badge on activity icon */
.ide-activity-btn .badge {
  position: absolute;
  top: 2px;
  right: 2px;
  min-width: 14px;
  height: 14px;
  background: #0078d4;
  border-radius: 7px;
  font-size: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-family: var(--font-sans);
  padding-inline: 2px;
}

.ide-activity-spacer { flex: 1; }

/* Sidebar */
.ide-sidebar {
  grid-area: sidebar;
  background: #252526;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #1e1e1e;
}

.ide-sidebar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-2) var(--space-3);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255 255 255 / 0.5);
  border-bottom: 1px solid #3c3c3c;
  user-select: none;
}

.ide-sidebar__actions {
  display: flex;
  gap: var(--space-1);
}

.ide-sidebar-action {
  width: 1.25rem;
  height: 1.25rem;
  border: none;
  background: none;
  color: rgba(255 255 255 / 0.5);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
  font-size: 0.75rem;
  transition: color var(--duration-fast), background var(--duration-fast);
}
.ide-sidebar-action:hover {
  color: white;
  background: rgba(255 255 255 / 0.1);
}

.ide-sidebar__content {
  flex: 1;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255 255 255 / 0.2) transparent;
}

/* File tree in sidebar */
.ide-file-row {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: 0.125rem 0;
  padding-inline-start: calc(var(--depth, 0) * 1rem + 0.5rem);
  cursor: pointer;
  border-radius: 2px;
  color: rgba(255 255 255 / 0.75);
  font-size: var(--font-size-xs);
  transition: background var(--duration-fast), color var(--duration-fast);
  white-space: nowrap;
}
.ide-file-row:hover { background: rgba(255 255 255 / 0.06); }
.ide-file-row.active { background: rgba(255 255 255 / 0.1); color: white; }
.ide-file-row.open   { color: white; }

/* Main editor area */
.ide-main {
  grid-area: main;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Tab bar */
.ide-tabs {
  display: flex;
  background: #2d2d2d;
  border-bottom: 1px solid #1e1e1e;
  overflow-x: auto;
  scrollbar-width: none;
  flex-shrink: 0;
}
.ide-tabs::-webkit-scrollbar { display: none; }

.ide-tab {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.4rem 0.875rem;
  cursor: pointer;
  white-space: nowrap;
  border-right: 1px solid #1e1e1e;
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.5);
  background: #2d2d2d;
  transition: background var(--duration-fast), color var(--duration-fast);
  border-bottom: 2px solid transparent;
  user-select: none;
}

.ide-tab:hover { background: #3c3c3c; color: rgba(255 255 255 / 0.8); }
.ide-tab.active {
  background: #1e1e1e;
  color: white;
  border-bottom-color: #0078d4;
}

.ide-tab__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255 255 255 / 0.4);
  flex-shrink: 0;
}

.ide-tab__close {
  width: 1rem;
  height: 1rem;
  border-radius: 2px;
  border: none;
  background: none;
  color: inherit;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  font-size: 0.6875rem;
  transition: opacity var(--duration-fast), background var(--duration-fast);
}
.ide-tab:hover .ide-tab__close { opacity: 1; }
.ide-tab__close:hover { background: rgba(255 255 255 / 0.15); opacity: 1; }

/* Editor area */
.ide-editor {
  flex: 1;
  display: flex;
  overflow: hidden;
  position: relative;
}

.ide-gutter {
  width: 48px;
  background: #1e1e1e;
  padding-block-start: var(--space-2);
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.25);
  text-align: right;
  padding-inline-end: var(--space-2);
  user-select: none;
  flex-shrink: 0;
  line-height: 1.6;
}

.ide-code-area {
  flex: 1;
  overflow: auto;
  padding: var(--space-2) var(--space-4);
  line-height: 1.6;
}

/* Status bar */
.ide-statusbar {
  grid-area: statusbar;
  background: #0078d4;
  display: flex;
  align-items: center;
  padding-inline: var(--space-3);
  gap: var(--space-4);
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.9);
  user-select: none;
}

.ide-statusbar__item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  cursor: pointer;
  padding: 0 var(--space-1);
  transition: background var(--duration-fast);
  border-radius: 2px;
}
.ide-statusbar__item:hover { background: rgba(255 255 255 / 0.15); }

.ide-statusbar__spacer { flex: 1; }

/* Split editor panel */
.ide-editor-group {
  display: flex;
  flex: 1;
  overflow: hidden;
}
.ide-editor-group > * {
  flex: 1;
  border-left: 1px solid #3c3c3c;
  overflow: hidden;
}
.ide-editor-group > *:first-child { border-left: none; }
```

---

## 153. DRAWING / WHITEBOARD UI

```css
/* ─── Canvas whiteboard ─── */
.whiteboard {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--board-bg, #fafafa);
  cursor: crosshair;
  user-select: none;
  touch-action: none;
}

/* Infinite canvas grid */
.whiteboard__grid {
  position: absolute;
  inset: -200%;
  background-image:
    linear-gradient(var(--grid-color, #e5e7eb) 1px, transparent 1px),
    linear-gradient(to right, var(--grid-color, #e5e7eb) 1px, transparent 1px);
  background-size: var(--grid-size, 20px) var(--grid-size, 20px);
  pointer-events: none;
  transform: translate(var(--pan-x, 0px), var(--pan-y, 0px)) scale(var(--zoom, 1));
  transform-origin: center;
}

/* Canvas layer */
.whiteboard__canvas {
  position: absolute;
  inset: 0;
  transform:
    translate(var(--pan-x, 0px), var(--pan-y, 0px))
    scale(var(--zoom, 1));
  transform-origin: top left;
}

/* ─── Toolbar ─── */
.whiteboard-toolbar {
  position: absolute;
  top: var(--space-4);
  left: 50%;
  translate: -50% 0;
  z-index: 10;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-2) var(--space-3);
  display: flex;
  align-items: center;
  gap: var(--space-1);
  box-shadow: var(--shadow-lg);
}

.whiteboard-tool {
  width: 2.25rem;
  height: 2.25rem;
  border: none;
  background: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  font-size: 1.1rem;
  transition:
    background var(--duration-fast),
    color      var(--duration-fast),
    scale      var(--duration-fast) var(--ease-bounce);
  position: relative;
}
.whiteboard-tool:hover { background: var(--color-bg-subtle); color: var(--color-text); }
.whiteboard-tool.active {
  background: var(--color-accent);
  color: white;
  scale: 1.05;
}

/* Tool tooltip */
.whiteboard-tool::after {
  content: attr(data-tool);
  position: absolute;
  top: calc(100% + 6px);
  left: 50%;
  translate: -50% 0;
  background: var(--color-neutral-900);
  color: white;
  font-size: var(--font-size-xs);
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-md);
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--duration-fast);
}
.whiteboard-tool:hover::after { opacity: 1; }

.whiteboard-toolbar__divider {
  width: 1px;
  height: 1.5rem;
  background: var(--color-border);
  margin-inline: var(--space-1);
}

/* Color picker strip */
.whiteboard-colors {
  display: flex;
  gap: 4px;
}

.color-swatch-small {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: scale var(--duration-fast) var(--ease-bounce), border-color var(--duration-fast);
}
.color-swatch-small:hover { scale: 1.2; }
.color-swatch-small.selected { border-color: var(--color-text); scale: 1.1; }

/* Stroke width selector */
.stroke-widths {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.stroke-btn {
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-md);
  transition: background var(--duration-fast);
}
.stroke-btn:hover { background: var(--color-bg-subtle); }
.stroke-btn.active { background: var(--color-bg-muted); }

.stroke-preview {
  background: currentColor;
  border-radius: var(--radius-full);
  width: 1.5rem;
}
.stroke-preview--sm { height: 2px; }
.stroke-preview--md { height: 4px; }
.stroke-preview--lg { height: 6px; }

/* ─── Side panel (layers, objects) ─── */
.whiteboard-panel {
  position: absolute;
  right: var(--space-4);
  top: var(--space-4);
  bottom: var(--space-4);
  width: 220px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  z-index: 10;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Object on canvas */
.canvas-object {
  position: absolute;
  cursor: move;
  user-select: none;
  transition: outline var(--duration-fast);
}

.canvas-object.selected {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* Resize handles */
.canvas-object.selected::after {
  content: '';
  position: absolute;
  inset: -5px;
  pointer-events: none;
}

.resize-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: white;
  border: 1.5px solid var(--color-accent);
  border-radius: 2px;
  cursor: nw-resize;
}

.resize-handle[data-pos="tl"] { top: -4px; left: -4px; cursor: nw-resize; }
.resize-handle[data-pos="tr"] { top: -4px; right: -4px; cursor: ne-resize; }
.resize-handle[data-pos="bl"] { bottom: -4px; left: -4px; cursor: sw-resize; }
.resize-handle[data-pos="br"] { bottom: -4px; right: -4px; cursor: se-resize; }
.resize-handle[data-pos="tc"] { top: -4px; left: 50%; translate: -50% 0; cursor: n-resize; }
.resize-handle[data-pos="bc"] { bottom: -4px; left: 50%; translate: -50% 0; cursor: s-resize; }
.resize-handle[data-pos="lc"] { left: -4px; top: 50%; translate: 0 -50%; cursor: w-resize; }
.resize-handle[data-pos="rc"] { right: -4px; top: 50%; translate: 0 -50%; cursor: e-resize; }

/* Zoom controls */
.whiteboard-zoom {
  position: absolute;
  bottom: var(--space-4);
  left: var(--space-4);
  display: flex;
  align-items: center;
  gap: var(--space-1);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-1) var(--space-2);
  box-shadow: var(--shadow-md);
}

.zoom-level {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  min-width: 3.5em;
  text-align: center;
  cursor: pointer;
  font-variant-numeric: tabular-nums;
}
```

---

## 154. PRESENTATION SLIDES

```css
/* ─── Slide deck layout ─── */
.presentation {
  width: 100%;
  aspect-ratio: 16 / 9;
  position: relative;
  overflow: hidden;
  font-family: var(--font-sans);
}

/* Slide */
.slide {
  position: absolute;
  inset: 0;
  padding: 8% 10%;
  display: flex;
  flex-direction: column;
  background: var(--slide-bg, white);
  color: var(--slide-color, var(--color-text));
  opacity: 0;
  transition:
    opacity   0.4s var(--ease-out),
    translate 0.4s var(--ease-out);
  pointer-events: none;
}

.slide.active   { opacity: 1; pointer-events: auto; translate: 0; }
.slide.prev     { translate: -100% 0; }
.slide.next     { translate: 100% 0; }

/* Slide types */
.slide--title {
  align-items: center;
  justify-content: center;
  text-align: center;
}

.slide--title-content { justify-content: flex-start; }
.slide--two-col .slide-content { display: grid; grid-template-columns: 1fr 1fr; gap: 8%; }
.slide--blank { padding: 0; }

/* Typography scales relative to slide width */
.slide-title {
  font-size: clamp(1.5rem, 5cqw, 3.5rem);
  font-weight: var(--font-weight-black);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-block-end: 0.4em;
  text-wrap: balance;
}

.slide-subtitle {
  font-size: clamp(0.875rem, 2.5cqw, 1.5rem);
  color: var(--color-text-muted);
  line-height: 1.4;
}

.slide-heading {
  font-size: clamp(1.25rem, 3.5cqw, 2.25rem);
  font-weight: var(--font-weight-bold);
  margin-block-end: 0.6em;
  text-wrap: balance;
}

.slide-body {
  font-size: clamp(0.75rem, 2cqw, 1.125rem);
  line-height: 1.6;
  flex: 1;
}

/* Bullet list */
.slide-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6em;
}

.slide-list li {
  display: flex;
  gap: 0.5em;
  align-items: flex-start;
}

.slide-list li::before {
  content: '▸';
  color: var(--slide-accent, var(--color-accent));
  flex-shrink: 0;
  margin-top: 0.1em;
}

/* Code block in slide */
.slide-code {
  background: rgba(0 0 0 / 0.08);
  border-radius: 0.5em;
  padding: 0.75em 1em;
  font-family: var(--font-mono);
  font-size: 0.75em;
  line-height: 1.6;
  overflow: auto;
  border: 1px solid rgba(0 0 0 / 0.1);
}

/* Image in slide */
.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.5em;
}

/* Slide number */
.slide-number {
  position: absolute;
  bottom: 4%;
  right: 6%;
  font-size: clamp(0.5rem, 1.2cqw, 0.75rem);
  color: rgba(0 0 0 / 0.25);
  font-variant-numeric: tabular-nums;
}

/* ─── Presentation themes ─── */
.presentation--dark {
  --slide-bg: #0f172a;
  --slide-color: #f1f5f9;
  --slide-accent: #60a5fa;
}

.presentation--gradient {
  --slide-bg: linear-gradient(135deg, #667eea, #764ba2);
  --slide-color: white;
}

.presentation--minimal {
  --slide-bg: white;
  --slide-color: #1a1a1a;
  --slide-accent: #111;
}

/* ─── Slide transitions ─── */
.slide--fade.prev   { opacity: 0; translate: 0; }
.slide--fade.next   { opacity: 0; translate: 0; }

.slide--zoom.active { animation: slide-zoom-in 0.4s var(--ease-out); }
@keyframes slide-zoom-in { from { scale: 0.9; opacity: 0; } }

.slide--flip {
  transform-style: preserve-3d;
  backface-visibility: hidden;
}
.slide--flip.prev { animation: slide-flip-out 0.4s ease-in forwards; }
.slide--flip.next { animation: slide-flip-in 0.4s ease-out; }

@keyframes slide-flip-out { to   { transform: rotateY(-90deg); opacity: 0; } }
@keyframes slide-flip-in  { from { transform: rotateY(90deg);  opacity: 0; } }

/* ─── Slide thumbnails navigation ─── */
.slide-thumbs {
  display: flex;
  gap: var(--space-2);
  overflow-x: auto;
  padding: var(--space-2);
  background: var(--color-bg-subtle);
  scrollbar-width: thin;
}

.slide-thumb {
  flex: 0 0 160px;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
  position: relative;
}
.slide-thumb:hover { scale: 1.02; }
.slide-thumb.active { border-color: var(--color-accent); }

.slide-thumb__num {
  position: absolute;
  bottom: 4px;
  right: 6px;
  font-size: 10px;
  color: rgba(0 0 0 / 0.4);
  font-weight: bold;
}

/* Presenter view */
.presenter-view {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-4);
  height: 100dvh;
  padding: var(--space-4);
  background: #1a1a1a;
}

.presenter-current { border-radius: var(--radius-xl); overflow: hidden; }
.presenter-notes {
  background: #2a2a2a;
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  color: white;
  overflow-y: auto;
  font-size: var(--font-size-sm);
  line-height: 1.7;
}
.presenter-timer {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: var(--font-weight-black);
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  color: white;
  text-align: center;
  padding: var(--space-4);
}
```

---

## 155. VIDEO EDITOR TIMELINE

```css
/* ─── Video editor layout ─── */
.video-editor {
  display: grid;
  grid-template-rows: auto 1fr auto;
  height: 100dvh;
  background: #1a1a1a;
  color: #d0d0d0;
  font-family: var(--font-sans);
  font-size: var(--font-size-sm);
}

/* Preview area */
.video-preview {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--space-2);
  padding: var(--space-3);
  background: #111;
  border-bottom: 1px solid #333;
}

.video-canvas {
  aspect-ratio: 16 / 9;
  background: #000;
  border-radius: var(--radius-lg);
  overflow: hidden;
  position: relative;
}

.video-canvas video { width: 100%; height: 100%; object-fit: contain; }

/* Playback controls */
.playback-controls {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: #1a1a1a;
  border-bottom: 1px solid #333;
}

.playback-btn {
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  color: rgba(255 255 255 / 0.75);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.playback-btn:hover { background: rgba(255 255 255 / 0.1); color: white; }
.playback-btn--play { width: 2.5rem; height: 2.5rem; font-size: 1.25rem; }

.playback-time {
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
  font-variant-numeric: tabular-nums;
  color: rgba(255 255 255 / 0.7);
  white-space: nowrap;
}

/* ─── Timeline ─── */
.timeline {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #1e1e1e;
}

.timeline__ruler {
  height: 24px;
  background: #252525;
  border-bottom: 1px solid #333;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

/* Time markers */
.timeline__tick {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
  background: rgba(255 255 255 / 0.1);
}
.timeline__tick::after {
  content: attr(data-time);
  position: absolute;
  top: 4px;
  left: 4px;
  font-size: 9px;
  color: rgba(255 255 255 / 0.4);
  white-space: nowrap;
}

/* Playhead */
.timeline__playhead {
  position: absolute;
  top: 0;
  bottom: 0;
  left: var(--playhead, 0%);
  width: 1px;
  background: #ff4757;
  z-index: 10;
  pointer-events: none;
}
.timeline__playhead::before {
  content: '';
  position: absolute;
  top: 0;
  left: -5px;
  width: 11px;
  height: 12px;
  background: #ff4757;
  clip-path: polygon(0 0, 100% 0, 50% 100%);
}

/* Track list */
.timeline__tracks {
  flex: 1;
  overflow: auto;
}

.timeline__track {
  display: flex;
  height: 48px;
  border-bottom: 1px solid #2a2a2a;
  position: relative;
}

.timeline__track-header {
  width: 160px;
  flex-shrink: 0;
  background: #252525;
  border-right: 1px solid #333;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding-inline: var(--space-3);
  position: sticky;
  left: 0;
  z-index: 1;
}

.track-label {
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.7);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.track-mute, .track-solo {
  width: 1.25rem;
  height: 1.25rem;
  border: none;
  background: rgba(255 255 255 / 0.1);
  border-radius: 3px;
  color: rgba(255 255 255 / 0.5);
  cursor: pointer;
  font-size: 0.625rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.track-mute.active  { background: #ff4757; color: white; }
.track-solo.active  { background: #ffd700; color: #111; }

/* Track content area */
.timeline__track-content {
  flex: 1;
  position: relative;
  overflow: hidden;
}

/* Clip */
.timeline-clip {
  position: absolute;
  top: 4px;
  bottom: 4px;
  background: var(--clip-color, #0078d4);
  border-radius: 4px;
  left: var(--clip-start, 0%);
  width: var(--clip-width, 20%);
  overflow: hidden;
  cursor: grab;
  transition: filter var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
  border: 1px solid rgba(255 255 255 / 0.2);
}
.timeline-clip:hover { filter: brightness(1.15); }
.timeline-clip.selected { outline: 2px solid white; outline-offset: 1px; }
.timeline-clip:active { cursor: grabbing; }

/* Waveform in audio clip */
.timeline-clip__waveform {
  position: absolute;
  inset: 0;
  opacity: 0.4;
  background-image: var(--waveform);
  background-size: 100% 100%;
}

.timeline-clip__label {
  position: relative;
  padding: 2px 6px;
  font-size: 9px;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  z-index: 1;
}

/* Resize handles on clip */
.timeline-clip__resize-left,
.timeline-clip__resize-right {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 8px;
  cursor: ew-resize;
  background: rgba(255 255 255 / 0.2);
  z-index: 2;
  border-radius: 2px;
  opacity: 0;
  transition: opacity var(--duration-fast);
}
.timeline-clip__resize-left  { left: 0; }
.timeline-clip__resize-right { right: 0; }
.timeline-clip:hover .timeline-clip__resize-left,
.timeline-clip:hover .timeline-clip__resize-right { opacity: 1; }

/* Video track (different color) */
.timeline__track--video .timeline-clip { --clip-color: #764ba2; }
.timeline__track--audio .timeline-clip { --clip-color: #0078d4; }
.timeline__track--text  .timeline-clip { --clip-color: #2d8b47; }
.timeline__track--effect .timeline-clip { --clip-color: #c47900; }
```

---

## 156. IMAGE ZOOM / MAGNIFIER

```css
/* ─── Image zoom on hover ─── */
.zoom-container {
  position: relative;
  overflow: hidden;
  cursor: zoom-in;
}

/* CSS-only zoom (transform scale) */
.zoom-container img {
  transition: transform 0.4s var(--ease-out), transform-origin 0s;
  transform-origin: var(--ox, 50%) var(--oy, 50%);
  display: block;
  width: 100%;
}

.zoom-container:hover img {
  transform: scale(2);
}

/* ─── Magnifier lens ─── */
/* JS sets --mx --my (mouse position %) */
.magnifier {
  position: relative;
  display: inline-block;
  cursor: crosshair;
}

.magnifier img { display: block; width: 100%; }

.magnifier-lens {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow:
    0 0 0 1px rgba(0 0 0 / 0.3),
    var(--shadow-xl);
  pointer-events: none;
  overflow: hidden;
  left: calc(var(--mx, 50%) - 60px);
  top:  calc(var(--my, 50%) - 60px);
  opacity: 0;
  transition: opacity var(--duration-fast);
  z-index: 2;
}

.magnifier:hover .magnifier-lens { opacity: 1; }

/* Background image = same as parent, scaled up */
.magnifier-lens__inner {
  position: absolute;
  width: 300%;
  height: 300%;
  left: calc(-150% + 50% - (var(--mx, 50%) - 50%) * 3);
  top:  calc(-150% + 50% - (var(--my, 50%) - 50%) * 3);
  background-image: var(--zoom-image);
  background-size: 100% 100%;
  background-repeat: no-repeat;
}

/* ─── Picture-in-picture zoom preview ─── */
.zoom-with-preview {
  display: grid;
  grid-template-columns: 1fr 220px;
  gap: var(--space-4);
  align-items: start;
}

.zoom-main {
  position: relative;
  cursor: crosshair;
  overflow: hidden;
}

.zoom-preview-box {
  position: absolute;
  border: 2px solid var(--color-accent);
  pointer-events: none;
  left: var(--preview-x, 0);
  top:  var(--preview-y, 0);
  width: var(--preview-w, 30%);
  height: var(--preview-h, 30%);
  background: rgba(59 130 246 / 0.1);
}

.zoom-preview-panel {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  aspect-ratio: 1;
  background: var(--color-bg-muted);
}

.zoom-preview-panel img {
  width: 100%;
  height: 100%;
  object-fit: none;
  object-position: var(--preview-pos, 0 0);
}
```

---

## 157. BREADCRUMB ADVANCED PATTERNS

```css
/* ─── Standard breadcrumb ─── */
.breadcrumbs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.25rem;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  padding: var(--space-2) 0;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* Separator */
.breadcrumb-item + .breadcrumb-item::before {
  content: '/';
  color: var(--color-border-strong);
  margin-inline-end: 0.25rem;
}

/* Chevron separator */
.breadcrumbs--chevron .breadcrumb-item + .breadcrumb-item::before {
  content: '';
  width: 6px;
  height: 6px;
  border-right: 1.5px solid var(--color-border-strong);
  border-top: 1.5px solid var(--color-border-strong);
  rotate: 45deg;
  margin-inline-end: 0.25rem;
}

/* Dot separator */
.breadcrumbs--dot .breadcrumb-item + .breadcrumb-item::before {
  content: '•';
  font-size: 0.5em;
  vertical-align: middle;
  color: var(--color-border-strong);
}

.breadcrumb-link {
  color: var(--color-text-muted);
  text-decoration: none;
  transition: color var(--duration-fast);
  padding: 0.125rem 0.25rem;
  border-radius: var(--radius-sm);
}
.breadcrumb-link:hover {
  color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 8%, transparent);
  text-decoration: none;
}

.breadcrumb-item:last-child {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
  pointer-events: none;
}

/* Collapsible breadcrumbs (for deep navigation) */
.breadcrumbs--collapsible .breadcrumb-item.collapsed { display: none; }
.breadcrumbs--collapsible .breadcrumb-item.collapsed.show { display: flex; }

.breadcrumb-ellipsis {
  display: flex;
  align-items: center;
  padding: 0.125rem 0.375rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--color-text-muted);
  background: var(--color-bg-subtle);
  transition: background var(--duration-fast);
  font-size: 0.8em;
  font-weight: var(--font-weight-bold);
  letter-spacing: 0.05em;
}
.breadcrumb-ellipsis:hover { background: var(--color-bg-muted); }

/* ─── Breadcrumb with icons ─── */
.breadcrumbs--icons .breadcrumb-link {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.breadcrumb-icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
  opacity: 0.7;
}

/* ─── Floating breadcrumb pill ─── */
.breadcrumbs--pill {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  padding: var(--space-2) var(--space-3);
  display: inline-flex;
  box-shadow: var(--shadow-sm);
}

/* ─── Breadcrumb with dropdown on click ─── */
.breadcrumb-dropdown {
  position: relative;
}

.breadcrumb-dropdown-menu {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: var(--space-1);
  z-index: var(--z-dropdown);
  min-width: 160px;
  display: none;
}

.breadcrumb-dropdown:focus-within .breadcrumb-dropdown-menu { display: block; }

.breadcrumb-dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--color-text);
  text-decoration: none;
  transition: background var(--duration-fast);
}
.breadcrumb-dropdown-item:hover { background: var(--color-bg-subtle); }
```

---

## 158. PRINT CSS DEEP DIVE

```css
/* ─── Complete print stylesheet ─── */
@media print {

  /* ─── Page setup ─── */
  @page {
    size: A4 portrait;
    margin: 2cm 2.5cm;

    /* Headers and footers */
    @top-left {
      content: 'Company Name';
      font-size: 9pt;
      color: #666;
    }
    @top-right {
      content: string(chapter-title);
      font-size: 9pt;
      color: #666;
    }
    @bottom-center {
      content: counter(page) ' / ' counter(pages);
      font-size: 9pt;
      color: #666;
    }
    @bottom-left {
      content: 'Printed: ' date(now, '%Y-%m-%d');
      font-size: 8pt;
      color: #999;
    }
  }

  @page :first {
    @top-left { content: ''; }
    @top-right { content: ''; }
    margin-top: 3cm;
  }

  @page :left {
    margin-left: 3cm;
    margin-right: 2cm;
  }

  @page :right {
    margin-left: 2cm;
    margin-right: 3cm;
  }

  /* ─── Reset for print ─── */
  *,
  *::before,
  *::after {
    background: transparent !important;
    color: #000 !important;
    box-shadow: none !important;
    text-shadow: none !important;
  }

  body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #000;
    background: white;
  }

  /* ─── Hide non-print elements ─── */
  nav,
  header:not(.print-header),
  footer:not(.print-footer),
  aside,
  .sidebar,
  .no-print,
  .btn,
  button:not(.print-btn),
  .modal,
  .toast,
  .tooltip,
  .cookie-banner,
  .back-top-btn,
  .share-bar,
  .toc,
  .ads,
  video,
  audio,
  iframe:not(.print-iframe),
  [aria-hidden="true"] {
    display: none !important;
  }

  /* ─── Show print-only elements ─── */
  .print-only { display: block !important; }
  .print-inline { display: inline !important; }

  /* ─── Typography ─── */
  h1 { font-size: 22pt; page-break-before: always; }
  h1:first-child { page-break-before: auto; }
  h2 { font-size: 16pt; }
  h3 { font-size: 13pt; }
  h4 { font-size: 11pt; }

  h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid;
    orphans: 3;
    widows: 3;
  }

  p, li {
    orphans: 3;
    widows: 3;
    font-size: 11pt;
  }

  /* String set for running headers */
  h2 { string-set: chapter-title content(); }

  /* ─── Links ─── */
  a[href]::after {
    content: ' (' attr(href) ')';
    font-size: 9pt;
    color: #555;
    word-break: break-all;
  }

  /* Don't show URLs for internal/JS links */
  a[href^="#"]::after,
  a[href^="javascript:"]::after,
  a[href^="tel:"]::after,
  a[href^="mailto:"]::after,
  a.no-print-url::after {
    content: '';
  }

  /* ─── Images ─── */
  img {
    max-width: 100% !important;
    page-break-inside: avoid;
  }

  figure { page-break-inside: avoid; }

  figcaption {
    font-size: 9pt;
    font-style: italic;
    color: #555;
    text-align: center;
  }

  /* ─── Tables ─── */
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #ccc; padding: 6pt 8pt; font-size: 10pt; }
  th { background: #f5f5f5 !important; font-weight: bold; }

  thead { display: table-header-group; } /* Repeat on every page */
  tfoot { display: table-footer-group; }
  tr    { page-break-inside: avoid; }

  /* ─── Code blocks ─── */
  pre, code {
    font-family: 'Courier New', monospace;
    font-size: 9pt;
    background: #f8f8f8 !important;
    border: 1px solid #ddd;
    color: #000 !important;
  }

  pre {
    white-space: pre-wrap;
    word-break: break-all;
    page-break-inside: avoid;
    padding: 8pt;
    border-radius: 3pt;
  }

  /* ─── Page breaks ─── */
  .page-break-before  { page-break-before: always; break-before: page; }
  .page-break-after   { page-break-after: always;  break-after: page; }
  .no-page-break      { page-break-inside: avoid;  break-inside: avoid; }
  .page-break-column  { break-before: column; }

  blockquote { page-break-inside: avoid; }
  section    { page-break-inside: avoid; }

  /* ─── Grid/Flex reset ─── */
  .grid, .flex { display: block !important; }
  .col, [class*="col-"] { width: 100% !important; float: none !important; }

  /* ─── Sidebar layout → single column ─── */
  .with-sidebar { display: block !important; }
  .sidebar { display: none !important; }

  /* ─── QR code for URL ─── */
  .print-qr {
    display: block !important;
    width: 80pt;
    height: 80pt;
  }

  /* ─── Color coding for print (patterns instead) ─── */
  .status-success { border: 2px solid #000; }
  .status-warning { border: 2px dashed #000; }
  .status-error   { border: 2px dotted #000; }

  /* ─── CSS Counters for print ─── */
  body { counter-reset: print-section; }
  h2 {
    counter-increment: print-section;
    counter-reset: print-subsection;
  }
  h2::before { content: counter(print-section) '. '; }

  h3 { counter-increment: print-subsection; }
  h3::before { content: counter(print-section) '.' counter(print-subsection) '. '; }
}
```

---

## 159. FONT LOADING STRATEGIES

```css
/* ─── Strategy 1: font-display: swap (most common) ─── */
@font-face {
  font-family: 'PrimaryFont';
  src: url('font.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
  /* FOUT: Flash of Unstyled Text — system font → custom font */
}

/* ─── Strategy 2: font-display: optional (no CLS) ─── */
@font-face {
  font-family: 'PerformanceFont';
  src: url('font.woff2') format('woff2');
  font-display: optional;
  /* Only uses font if already cached (100ms budget) */
  /* No layout shift, no FOUT — best CLS score */
}

/* ─── Strategy 3: Size-adjust to eliminate FOUT ─── */
/* Match fallback font metrics to custom font */
@font-face {
  font-family: 'FallbackArial';
  src: local('Arial');
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
  size-adjust: 107%;
}

@font-face {
  font-family: 'MyFont';
  src: url('myfont.woff2') format('woff2');
  font-display: swap;
}

body {
  font-family: 'MyFont', 'FallbackArial', Arial, sans-serif;
  /* Fallback metrics match → no layout shift during swap */
}

/* ─── Strategy 4: Preloading critical fonts ─── */
/*
HTML in <head>:
<link rel="preload" href="font-regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="font-bold.woff2" as="font" type="font/woff2" crossorigin>
*/

/* ─── Strategy 5: Subsetting via unicode-range ─── */
@font-face {
  font-family: 'MyFont';
  src: url('font-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA,
                 U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+2074, U+20AC,
                 U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
  font-display: swap;
}

@font-face {
  font-family: 'MyFont';
  src: url('font-cyrillic.woff2') format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
  font-display: swap;
}

/* ─── Strategy 6: Variable font (single file for all weights) ─── */
@font-face {
  font-family: 'MyVariableFont';
  src: url('font-variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal oblique 0deg 12deg;
  font-stretch: 75% 125%;
  font-display: swap;
}

/* ─── Strategy 7: System font stack (no loading at all) ─── */
:root {
  /* Modern OS system fonts — fast, no network */
  --font-system: system-ui, -apple-system, 'Segoe UI', Roboto,
                 'Helvetica Neue', Arial, 'Noto Sans', sans-serif,
                 'Apple Color Emoji', 'Segoe UI Emoji';

  --font-system-mono: ui-monospace, 'Cascadia Code', 'Source Code Pro',
                      Menlo, Consolas, 'DejaVu Sans Mono', monospace;

  --font-system-serif: ui-serif, Georgia, Cambria, 'Times New Roman', Times, serif;
}

/* ─── Font smoothing per OS ─── */
@media (-webkit-min-device-pixel-ratio: 1.5) {
  /* Retina / HiDPI — antialiased looks better */
  body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
}

/* ─── Font loaded state via JS ─── */
/* document.fonts.ready.then(() => document.body.classList.add('fonts-loaded')) */

.fonts-loaded body {
  font-family: 'MyFont', var(--font-system);
}

/* ─── Prevent invisible text during load ─── */
/* font-display: block = FOIT (Flash of Invisible Text) = bad for UX */
/* Only use for icon fonts where fallback makes no sense */
@font-face {
  font-family: 'IconFont';
  src: url('icons.woff2') format('woff2');
  font-display: block; /* wait for icon font, don't show broken characters */
}

/* ─── CSS Font Loading API detection ─── */
/*
document.fonts.load('1em MyFont').then(() => {
  // Font loaded, apply font-specific styles
  document.documentElement.classList.add('font-loaded');
});
*/
```

---

## 160. CSS PERFORMANCE COMPLETE CHECKLIST

```css
/*
╔══════════════════════════════════════════════════════════════════════╗
║                CSS PERFORMANCE AUDIT — 2025                          ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  LOADING (affects FCP, LCP)                                         ║
║  ─────────────────────────────────────────────────────────────────  ║
║  □ Critical CSS inlined in <head> (< 14KB gzipped)                  ║
║  □ Deferred non-critical CSS via rel="preload"                       ║
║  □ No CSS @import chains (use bundler or HTTP/2)                     ║
║  □ CSS minified and compressed (Brotli > gzip)                      ║
║  □ Unused CSS removed (< 10% waste)                                 ║
║  □ Font files preloaded (<link rel="preload" as="font">)            ║
║  □ font-display: swap (avoid FOIT)                                   ║
║  □ Variable fonts used (1 file vs 5+ files)                         ║
║  □ Only WOFF2 format (drop WOFF, EOT, TTF in 2025)                  ║
║  □ Font subsets with unicode-range                                   ║
║                                                                      ║
║  RENDERING (affects CLS, FID, INP)                                  ║
║  ─────────────────────────────────────────────────────────────────  ║
║  □ Images have explicit width/height (prevents CLS)                  ║
║  □ aspect-ratio on dynamic content                                   ║
║  □ Animations use ONLY transform and opacity                         ║
║  □ No layout-triggering animations (width, margin, padding)         ║
║  □ will-change sparingly (only animated elements)                    ║
║  □ contain: layout/paint on independent components                   ║
║  □ content-visibility: auto on below-fold sections                   ║
║  □ touch-action: manipulation on interactive elements                ║
║  □ No CSS custom properties in tight animation loops                 ║
║  □ prefers-reduced-motion respected                                   ║
║                                                                      ║
║  PAINT (affects LCP, visual stability)                              ║
║  ─────────────────────────────────────────────────────────────────  ║
║  □ No excessive box-shadow (composite, not paint)                    ║
║  □ backdrop-filter only where needed                                 ║
║  □ filter limited (promotes to own layer)                            ║
║  □ Avoid opacity: 0 on large painted areas                          ║
║  □ GPU layers not overused (< 20 promoted layers)                    ║
║                                                                      ║
║  SPECIFICITY & CASCADE                                               ║
║  ─────────────────────────────────────────────────────────────────  ║
║  □ No ID selectors in authored CSS                                   ║
║  □ Max specificity 0-2-0                                             ║
║  □ @layer used for organization                                      ║
║  □ !important only in utilities/reset                                ║
║  □ No universal selector (*) in production with heavy properties     ║
║                                                                      ║
║  QUALITY                                                             ║
║  ─────────────────────────────────────────────────────────────────  ║
║  □ box-sizing: border-box universal                                  ║
║  □ No floats for layout                                              ║
║  □ Logical properties for RTL support                               ║
║  □ fluid typography via clamp()                                      ║
║  □ CSS custom properties for all design tokens                       ║
║  □ :focus-visible for keyboard navigation                            ║
║  □ color-scheme: light dark set                                      ║
║  □ Graceful degradation via @supports                                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
*/

/* ─── Common performance anti-patterns and fixes ─── */

/* ❌ Animating layout properties */
@keyframes bad-size {
  from { width: 0; height: 0; }
  to   { width: 100px; height: 100px; }
}

/* ✅ Use transform instead */
@keyframes good-size {
  from { transform: scale(0); }
  to   { transform: scale(1); }
}

/* ❌ Forcing layout recalculation */
.el { transition: margin 0.3s; }
.el:hover { margin: 10px; }  /* reflow on every frame */

/* ✅ GPU-composited property */
.el { transition: translate 0.3s; }
.el:hover { translate: 10px 0; }

/* ❌ Expensive selector recalculation */
.list:has(li:nth-child(n):hover) ~ .other { color: red; }
/* Triggers recalc on every mouse move over any li */

/* ✅ Use JS to toggle class */
.list.has-hover ~ .other { color: red; }

/* ❌ Painting entire page */
body { background-attachment: fixed; } /* repaint on scroll */

/* ✅ Use scroll-driven animation or pseudoelement */
.hero::before {
  content: '';
  position: fixed; inset: 0;
  background-image: url('bg.jpg');
  z-index: -1;
}

/* ─── contain patterns for components ─── */
.feed-item {
  contain: layout paint;
  /* Layout: children don't affect outside layout */
  /* Paint: renders in own layer, clips */
}

.widget {
  contain: strict;
  /* All constraints — for truly isolated components */
}

/* ─── Lazy rendering patterns ─── */
.below-fold {
  content-visibility: auto;
  contain-intrinsic-block-size: 500px;
  /* Browser skips rendering until near viewport */
  /* 500px = placeholder height for accurate scroll */
}
```

---

## 161. ADVANCED OKLCH COLOR SYSTEM

```css
/* ─── Complete oklch-based design system ─── */

/* Generate a full scale from a single oklch definition */
:root {
  /* Define brand via hue angle */
  --hue-brand:    250;   /* blue-purple */
  --hue-success:  145;   /* green */
  --hue-warning:  65;    /* yellow-amber */
  --hue-danger:   25;    /* red-orange */
  --hue-info:     220;   /* blue */
  --chroma-mid:   0.20;

  /* ── Brand scale ── */
  --brand-50:  oklch(0.975 calc(var(--chroma-mid)*0.12) var(--hue-brand));
  --brand-100: oklch(0.940 calc(var(--chroma-mid)*0.22) var(--hue-brand));
  --brand-200: oklch(0.890 calc(var(--chroma-mid)*0.38) var(--hue-brand));
  --brand-300: oklch(0.820 calc(var(--chroma-mid)*0.60) var(--hue-brand));
  --brand-400: oklch(0.730 calc(var(--chroma-mid)*0.80) var(--hue-brand));
  --brand-500: oklch(0.630 var(--chroma-mid) var(--hue-brand));
  --brand-600: oklch(0.540 var(--chroma-mid) var(--hue-brand));
  --brand-700: oklch(0.450 var(--chroma-mid) var(--hue-brand));
  --brand-800: oklch(0.355 calc(var(--chroma-mid)*0.9) var(--hue-brand));
  --brand-900: oklch(0.270 calc(var(--chroma-mid)*0.8) var(--hue-brand));
  --brand-950: oklch(0.180 calc(var(--chroma-mid)*0.6) var(--hue-brand));

  /* ── Relative color for tints/shades ── */
  --brand-light:   oklch(from var(--brand-500) calc(l + 0.25) c h);
  --brand-lighter: oklch(from var(--brand-500) calc(l + 0.4) c h);
  --brand-dark:    oklch(from var(--brand-500) calc(l - 0.2) c h);
  --brand-darker:  oklch(from var(--brand-500) calc(l - 0.35) c h);
  --brand-alpha-10: oklch(from var(--brand-500) l c h / 0.1);
  --brand-alpha-20: oklch(from var(--brand-500) l c h / 0.2);

  /* ── Analogous colors ── */
  --brand-warm: oklch(from var(--brand-500) l c calc(h - 30));
  --brand-cool: oklch(from var(--brand-500) l c calc(h + 30));

  /* ── Complementary ── */
  --brand-complement: oklch(from var(--brand-500) l c calc(h + 180));

  /* ── Accessible pair (auto-contrast) ── */
  /* For text ON brand-500 background: */
  --brand-text-light: oklch(0.98 0.01 var(--hue-brand));  /* near white */
  --brand-text-dark:  oklch(0.20 0.05 var(--hue-brand));  /* near black */

  /* ── Muted/desaturated version ── */
  --brand-muted: oklch(from var(--brand-500) l calc(c * 0.35) h);

  /* ── Vivid / boosted version ── */
  --brand-vivid: oklch(from var(--brand-500) l calc(c * 1.5) h);
}

/* ─── Adaptive contrast via CSS ─── */
/* APCA-like — check L difference */
.on-brand-bg {
  /* Automatically pick readable text based on background lightness */
  color: oklch(from var(--bg-color, var(--brand-500))
    clamp(0, calc((0.6 - l) * 9999), 1)   /* 0 if bg is light, 1 if dark */
    0
    0                                      /* pure white or black */
  );
}

/* ─── Perceptual gradient ─── */
/* Linear-gradient in oklch = perceptually uniform */
.oklch-gradient {
  background: linear-gradient(
    to right,
    oklch(0.6 0.2 260),
    oklch(0.6 0.2 200)
  );
  /* vs sRGB gradient which has dark muddy middle */
}

/* ─── Color space comparison ─── */
.gradient-srgb    { background: linear-gradient(in srgb to right, red, blue); }
.gradient-oklch   { background: linear-gradient(in oklch to right, red, blue); }
.gradient-hsl     { background: linear-gradient(in hsl to right, red, blue); }
/* oklch version looks most natural and vibrant in the middle */
```

---

## 162. CSS VARIABLES — MEGA REFERENCE

```css
/* ─── Every CSS variable pattern ─── */

/* 1. Simple value */
:root { --color: red; }

/* 2. With fallback */
.el { color: var(--color, blue); }

/* 3. Fallback chain */
.el { font-size: var(--size-custom, var(--size-default, 1rem)); }

/* 4. Computed from another variable */
:root {
  --base: 16;
  --lg: calc(var(--base) * 1.25px);
}

/* 5. Component namespace pattern */
.btn {
  --_bg: var(--btn-bg, var(--color-accent));  /* --_ = private */
  background: var(--_bg);
}

/* 6. Boolean / toggle (space toggle) */
.el {
  --is-active: ;        /* empty = false */
  color: var(--is-active, initial) red;  /* red when true */
}
.el.active { --is-active: initial; }   /* set to truthy */

/* 7. Typed variable via @property */
@property --progress {
  syntax: '<number>';
  initial-value: 0;
  inherits: false;
}
.el {
  --progress: 0;
  animation: fill linear;
  animation-timeline: scroll();
}
@keyframes fill { to { --progress: 1; } }
width: calc(var(--progress) * 100%);

/* 8. Color channel decomposition */
:root {
  --accent-h: 250;
  --accent-c: 0.2;
  --accent-l: 0.6;
  --accent: oklch(var(--accent-l) var(--accent-c) var(--accent-h));
  --accent-hover: oklch(calc(var(--accent-l) - 0.1) var(--accent-c) var(--accent-h));
}

/* 9. Contextual override via data-attributes */
[data-size="sm"] { --size: 0.875rem; }
[data-size="md"] { --size: 1rem; }
[data-size="lg"] { --size: 1.25rem; }
.text { font-size: var(--size, 1rem); }

/* 10. Responsive variable (breakpoint-based) */
:root { --columns: 1; }
@media (min-width: 640px)  { :root { --columns: 2; } }
@media (min-width: 1024px) { :root { --columns: 3; } }
.grid { grid-template-columns: repeat(var(--columns), 1fr); }

/* 11. Theme variable override */
[data-theme="dark"]  { --bg: #111; --text: #f0f0f0; }
[data-theme="light"] { --bg: #fff; --text: #111; }

/* 12. Animation state via variable */
.animated {
  --state: 0;
  translate: calc(var(--state) * 100px) 0;
  transition: translate 0.3s;
}
.animated.active { --state: 1; }

/* 13. Fluid clamp with variable inputs */
:root {
  --min: 1rem;
  --max: 2rem;
  --fluid: clamp(var(--min), 2vw + 0.5rem, var(--max));
}
h1 { font-size: var(--fluid); }

/* 14. Z-index scale via variable */
:root {
  --z-base: 0;
  --z-dropdown: 10;
  --z-sticky: 20;
  --z-modal: 50;
}

/* 15. Animation delay stagger */
.items > * {
  animation-delay: calc(var(--i, 0) * 50ms);
}
/* Set --i via: style="--i: 0", "1", "2"... or JS */

/* 16. Grid-responsive via variable */
.grid {
  --min-col: 250px;
  --cols: auto-fit;
  grid-template-columns: repeat(var(--cols), minmax(var(--min-col), 1fr));
}
.grid-fixed { --cols: 3; }

/* 17. Semantic color aliasing */
:root {
  --color-primary-raw: #3b82f6;
  --color-primary: var(--color-primary-raw);  /* alias for override */
}
/* User can override --color-primary without touching raw */

/* 18. Cascading component tokens */
.theme-orange { --accent: orange; }
.theme-orange .btn { /* inherits --accent: orange */ }

/* 19. Math utilities */
:root {
  --ratio: 1.618;
  --step-0: 1rem;
  --step-1: calc(var(--step-0) * var(--ratio));
  --step-2: calc(var(--step-1) * var(--ratio));
  --step--1: calc(var(--step-0) / var(--ratio));
}

/* 20. Environment variable integration */
.safe {
  padding-top: max(var(--space-4), env(safe-area-inset-top));
}
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║              CSS MASTER GUIDE — PARTS I–X                            ║
╠══════════════════════════════════════════════════════════════════════╣
║  162 chapters · 1,000+ code examples · ~35,000+ lines               ║
║                                                                      ║
║  NEW IN PART X:                                                      ║
║  ✅ IDE / Code editor multi-panel layout (VS Code style)            ║
║  ✅ Drawing / Whiteboard UI (canvas, toolbar, objects, handles)     ║
║  ✅ Presentation slides (themes, transitions, presenter view)        ║
║  ✅ Video editor timeline (clips, handles, tracks, playhead)         ║
║  ✅ Image zoom / magnifier (hover zoom, lens, picture-in-picture)   ║
║  ✅ Breadcrumbs advanced (chevron, pills, dropdown, icons)          ║
║  ✅ Print CSS deep dive (page setup, headers/footers, counters)     ║
║  ✅ Font loading strategies (swap, optional, size-adjust, preload)  ║
║  ✅ CSS Performance complete checklist (loading, rendering, paint)  ║
║  ✅ OKLCH color system (perceptual scale, relative, gradients)      ║
║  ✅ CSS Variables mega reference (20 patterns)                      ║
╚══════════════════════════════════════════════════════════════════════╝
```
