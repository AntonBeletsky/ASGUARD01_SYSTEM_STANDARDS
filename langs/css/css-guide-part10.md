\# PART X — CSS: ADVANCED INTERFACES \& COMPLETE REFERENCE



\---



\## 152. IDE / CODE EDITOR MULTI-PANEL LAYOUT



```css

/\* ─── IDE shell ─── \*/

.ide {

&#x20; display: grid;

&#x20; grid-template-areas:

&#x20;   "titlebar  titlebar  titlebar"

&#x20;   "activity  sidebar   main"

&#x20;   "activity  sidebar   statusbar";

&#x20; grid-template-columns: 48px 240px 1fr;

&#x20; grid-template-rows: 35px 1fr 22px;

&#x20; height: 100dvh;

&#x20; background: #1e1e1e;

&#x20; color: #d4d4d4;

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.8125rem;

&#x20; overflow: hidden;

}



/\* Title bar \*/

.ide-titlebar {

&#x20; grid-area: titlebar;

&#x20; background: #3c3c3c;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; padding-inline: var(--space-4);

&#x20; gap: var(--space-2);

&#x20; border-bottom: 1px solid #252525;

&#x20; user-select: none;

}



.ide-titlebar\_\_dots {

&#x20; display: flex;

&#x20; gap: 6px;

&#x20; margin-inline-end: var(--space-4);

}



.ide-dot {

&#x20; width: 12px;

&#x20; height: 12px;

&#x20; border-radius: 50%;

}

.ide-dot--red    { background: #ff5f57; }

.ide-dot--yellow { background: #febc2e; }

.ide-dot--green  { background: #28c840; }



.ide-titlebar\_\_title {

&#x20; color: rgba(255 255 255 / 0.6);

&#x20; font-size: var(--font-size-xs);

&#x20; flex: 1;

&#x20; text-align: center;

}



/\* Activity bar (leftmost icons) \*/

.ide-activity {

&#x20; grid-area: activity;

&#x20; background: #333333;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; padding-block: var(--space-2);

&#x20; gap: var(--space-1);

&#x20; border-right: 1px solid #252525;

}



.ide-activity-btn {

&#x20; width: 36px;

&#x20; height: 36px;

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; border-radius: var(--radius-md);

&#x20; color: rgba(255 255 255 / 0.5);

&#x20; font-size: 1.125rem;

&#x20; position: relative;

&#x20; transition: color var(--duration-fast);

}



.ide-activity-btn:hover { color: rgba(255 255 255 / 0.85); }

.ide-activity-btn.active { color: white; }



/\* Active indicator \*/

.ide-activity-btn.active::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; left: -4px;

&#x20; top: 50%;

&#x20; translate: 0 -50%;

&#x20; height: 60%;

&#x20; width: 2px;

&#x20; background: #0078d4;

&#x20; border-radius: 0 2px 2px 0;

}



/\* Badge on activity icon \*/

.ide-activity-btn .badge {

&#x20; position: absolute;

&#x20; top: 2px;

&#x20; right: 2px;

&#x20; min-width: 14px;

&#x20; height: 14px;

&#x20; background: #0078d4;

&#x20; border-radius: 7px;

&#x20; font-size: 9px;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: white;

&#x20; font-family: var(--font-sans);

&#x20; padding-inline: 2px;

}



.ide-activity-spacer { flex: 1; }



/\* Sidebar \*/

.ide-sidebar {

&#x20; grid-area: sidebar;

&#x20; background: #252526;

&#x20; overflow: hidden;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; border-right: 1px solid #1e1e1e;

}



.ide-sidebar\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-2) var(--space-3);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.08em;

&#x20; color: rgba(255 255 255 / 0.5);

&#x20; border-bottom: 1px solid #3c3c3c;

&#x20; user-select: none;

}



.ide-sidebar\_\_actions {

&#x20; display: flex;

&#x20; gap: var(--space-1);

}



.ide-sidebar-action {

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border: none;

&#x20; background: none;

&#x20; color: rgba(255 255 255 / 0.5);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; border-radius: 2px;

&#x20; font-size: 0.75rem;

&#x20; transition: color var(--duration-fast), background var(--duration-fast);

}

.ide-sidebar-action:hover {

&#x20; color: white;

&#x20; background: rgba(255 255 255 / 0.1);

}



.ide-sidebar\_\_content {

&#x20; flex: 1;

&#x20; overflow-y: auto;

&#x20; scrollbar-width: thin;

&#x20; scrollbar-color: rgba(255 255 255 / 0.2) transparent;

}



/\* File tree in sidebar \*/

.ide-file-row {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; padding: 0.125rem 0;

&#x20; padding-inline-start: calc(var(--depth, 0) \* 1rem + 0.5rem);

&#x20; cursor: pointer;

&#x20; border-radius: 2px;

&#x20; color: rgba(255 255 255 / 0.75);

&#x20; font-size: var(--font-size-xs);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

&#x20; white-space: nowrap;

}

.ide-file-row:hover { background: rgba(255 255 255 / 0.06); }

.ide-file-row.active { background: rgba(255 255 255 / 0.1); color: white; }

.ide-file-row.open   { color: white; }



/\* Main editor area \*/

.ide-main {

&#x20; grid-area: main;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; overflow: hidden;

}



/\* Tab bar \*/

.ide-tabs {

&#x20; display: flex;

&#x20; background: #2d2d2d;

&#x20; border-bottom: 1px solid #1e1e1e;

&#x20; overflow-x: auto;

&#x20; scrollbar-width: none;

&#x20; flex-shrink: 0;

}

.ide-tabs::-webkit-scrollbar { display: none; }



.ide-tab {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.4rem 0.875rem;

&#x20; cursor: pointer;

&#x20; white-space: nowrap;

&#x20; border-right: 1px solid #1e1e1e;

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.5);

&#x20; background: #2d2d2d;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

&#x20; border-bottom: 2px solid transparent;

&#x20; user-select: none;

}



.ide-tab:hover { background: #3c3c3c; color: rgba(255 255 255 / 0.8); }

.ide-tab.active {

&#x20; background: #1e1e1e;

&#x20; color: white;

&#x20; border-bottom-color: #0078d4;

}



.ide-tab\_\_dot {

&#x20; width: 6px;

&#x20; height: 6px;

&#x20; border-radius: 50%;

&#x20; background: rgba(255 255 255 / 0.4);

&#x20; flex-shrink: 0;

}



.ide-tab\_\_close {

&#x20; width: 1rem;

&#x20; height: 1rem;

&#x20; border-radius: 2px;

&#x20; border: none;

&#x20; background: none;

&#x20; color: inherit;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; opacity: 0;

&#x20; font-size: 0.6875rem;

&#x20; transition: opacity var(--duration-fast), background var(--duration-fast);

}

.ide-tab:hover .ide-tab\_\_close { opacity: 1; }

.ide-tab\_\_close:hover { background: rgba(255 255 255 / 0.15); opacity: 1; }



/\* Editor area \*/

.ide-editor {

&#x20; flex: 1;

&#x20; display: flex;

&#x20; overflow: hidden;

&#x20; position: relative;

}



.ide-gutter {

&#x20; width: 48px;

&#x20; background: #1e1e1e;

&#x20; padding-block-start: var(--space-2);

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.25);

&#x20; text-align: right;

&#x20; padding-inline-end: var(--space-2);

&#x20; user-select: none;

&#x20; flex-shrink: 0;

&#x20; line-height: 1.6;

}



.ide-code-area {

&#x20; flex: 1;

&#x20; overflow: auto;

&#x20; padding: var(--space-2) var(--space-4);

&#x20; line-height: 1.6;

}



/\* Status bar \*/

.ide-statusbar {

&#x20; grid-area: statusbar;

&#x20; background: #0078d4;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; padding-inline: var(--space-3);

&#x20; gap: var(--space-4);

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.9);

&#x20; user-select: none;

}



.ide-statusbar\_\_item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25rem;

&#x20; cursor: pointer;

&#x20; padding: 0 var(--space-1);

&#x20; transition: background var(--duration-fast);

&#x20; border-radius: 2px;

}

.ide-statusbar\_\_item:hover { background: rgba(255 255 255 / 0.15); }



.ide-statusbar\_\_spacer { flex: 1; }



/\* Split editor panel \*/

.ide-editor-group {

&#x20; display: flex;

&#x20; flex: 1;

&#x20; overflow: hidden;

}

.ide-editor-group > \* {

&#x20; flex: 1;

&#x20; border-left: 1px solid #3c3c3c;

&#x20; overflow: hidden;

}

.ide-editor-group > \*:first-child { border-left: none; }

```



\---



\## 153. DRAWING / WHITEBOARD UI



```css

/\* ─── Canvas whiteboard ─── \*/

.whiteboard {

&#x20; position: relative;

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; overflow: hidden;

&#x20; background: var(--board-bg, #fafafa);

&#x20; cursor: crosshair;

&#x20; user-select: none;

&#x20; touch-action: none;

}



/\* Infinite canvas grid \*/

.whiteboard\_\_grid {

&#x20; position: absolute;

&#x20; inset: -200%;

&#x20; background-image:

&#x20;   linear-gradient(var(--grid-color, #e5e7eb) 1px, transparent 1px),

&#x20;   linear-gradient(to right, var(--grid-color, #e5e7eb) 1px, transparent 1px);

&#x20; background-size: var(--grid-size, 20px) var(--grid-size, 20px);

&#x20; pointer-events: none;

&#x20; transform: translate(var(--pan-x, 0px), var(--pan-y, 0px)) scale(var(--zoom, 1));

&#x20; transform-origin: center;

}



/\* Canvas layer \*/

.whiteboard\_\_canvas {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; transform:

&#x20;   translate(var(--pan-x, 0px), var(--pan-y, 0px))

&#x20;   scale(var(--zoom, 1));

&#x20; transform-origin: top left;

}



/\* ─── Toolbar ─── \*/

.whiteboard-toolbar {

&#x20; position: absolute;

&#x20; top: var(--space-4);

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; z-index: 10;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-2) var(--space-3);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; box-shadow: var(--shadow-lg);

}



.whiteboard-tool {

&#x20; width: 2.25rem;

&#x20; height: 2.25rem;

&#x20; border: none;

&#x20; background: none;

&#x20; border-radius: var(--radius-lg);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-text-muted);

&#x20; font-size: 1.1rem;

&#x20; transition:

&#x20;   background var(--duration-fast),

&#x20;   color      var(--duration-fast),

&#x20;   scale      var(--duration-fast) var(--ease-bounce);

&#x20; position: relative;

}

.whiteboard-tool:hover { background: var(--color-bg-subtle); color: var(--color-text); }

.whiteboard-tool.active {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; scale: 1.05;

}



/\* Tool tooltip \*/

.whiteboard-tool::after {

&#x20; content: attr(data-tool);

&#x20; position: absolute;

&#x20; top: calc(100% + 6px);

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; padding: 0.2rem 0.5rem;

&#x20; border-radius: var(--radius-md);

&#x20; white-space: nowrap;

&#x20; opacity: 0;

&#x20; pointer-events: none;

&#x20; transition: opacity var(--duration-fast);

}

.whiteboard-tool:hover::after { opacity: 1; }



.whiteboard-toolbar\_\_divider {

&#x20; width: 1px;

&#x20; height: 1.5rem;

&#x20; background: var(--color-border);

&#x20; margin-inline: var(--space-1);

}



/\* Color picker strip \*/

.whiteboard-colors {

&#x20; display: flex;

&#x20; gap: 4px;

}



.color-swatch-small {

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border-radius: 50%;

&#x20; cursor: pointer;

&#x20; border: 2px solid transparent;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce), border-color var(--duration-fast);

}

.color-swatch-small:hover { scale: 1.2; }

.color-swatch-small.selected { border-color: var(--color-text); scale: 1.1; }



/\* Stroke width selector \*/

.stroke-widths {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

}



.stroke-btn {

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: var(--radius-md);

&#x20; transition: background var(--duration-fast);

}

.stroke-btn:hover { background: var(--color-bg-subtle); }

.stroke-btn.active { background: var(--color-bg-muted); }



.stroke-preview {

&#x20; background: currentColor;

&#x20; border-radius: var(--radius-full);

&#x20; width: 1.5rem;

}

.stroke-preview--sm { height: 2px; }

.stroke-preview--md { height: 4px; }

.stroke-preview--lg { height: 6px; }



/\* ─── Side panel (layers, objects) ─── \*/

.whiteboard-panel {

&#x20; position: absolute;

&#x20; right: var(--space-4);

&#x20; top: var(--space-4);

&#x20; bottom: var(--space-4);

&#x20; width: 220px;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; box-shadow: var(--shadow-lg);

&#x20; z-index: 10;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; overflow: hidden;

}



/\* Object on canvas \*/

.canvas-object {

&#x20; position: absolute;

&#x20; cursor: move;

&#x20; user-select: none;

&#x20; transition: outline var(--duration-fast);

}



.canvas-object.selected {

&#x20; outline: 2px solid var(--color-accent);

&#x20; outline-offset: 2px;

}



/\* Resize handles \*/

.canvas-object.selected::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: -5px;

&#x20; pointer-events: none;

}



.resize-handle {

&#x20; position: absolute;

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; background: white;

&#x20; border: 1.5px solid var(--color-accent);

&#x20; border-radius: 2px;

&#x20; cursor: nw-resize;

}



.resize-handle\[data-pos="tl"] { top: -4px; left: -4px; cursor: nw-resize; }

.resize-handle\[data-pos="tr"] { top: -4px; right: -4px; cursor: ne-resize; }

.resize-handle\[data-pos="bl"] { bottom: -4px; left: -4px; cursor: sw-resize; }

.resize-handle\[data-pos="br"] { bottom: -4px; right: -4px; cursor: se-resize; }

.resize-handle\[data-pos="tc"] { top: -4px; left: 50%; translate: -50% 0; cursor: n-resize; }

.resize-handle\[data-pos="bc"] { bottom: -4px; left: 50%; translate: -50% 0; cursor: s-resize; }

.resize-handle\[data-pos="lc"] { left: -4px; top: 50%; translate: 0 -50%; cursor: w-resize; }

.resize-handle\[data-pos="rc"] { right: -4px; top: 50%; translate: 0 -50%; cursor: e-resize; }



/\* Zoom controls \*/

.whiteboard-zoom {

&#x20; position: absolute;

&#x20; bottom: var(--space-4);

&#x20; left: var(--space-4);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-1) var(--space-2);

&#x20; box-shadow: var(--shadow-md);

}



.zoom-level {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-text-muted);

&#x20; min-width: 3.5em;

&#x20; text-align: center;

&#x20; cursor: pointer;

&#x20; font-variant-numeric: tabular-nums;

}

```



\---



\## 154. PRESENTATION SLIDES



```css

/\* ─── Slide deck layout ─── \*/

.presentation {

&#x20; width: 100%;

&#x20; aspect-ratio: 16 / 9;

&#x20; position: relative;

&#x20; overflow: hidden;

&#x20; font-family: var(--font-sans);

}



/\* Slide \*/

.slide {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; padding: 8% 10%;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; background: var(--slide-bg, white);

&#x20; color: var(--slide-color, var(--color-text));

&#x20; opacity: 0;

&#x20; transition:

&#x20;   opacity   0.4s var(--ease-out),

&#x20;   translate 0.4s var(--ease-out);

&#x20; pointer-events: none;

}



.slide.active   { opacity: 1; pointer-events: auto; translate: 0; }

.slide.prev     { translate: -100% 0; }

.slide.next     { translate: 100% 0; }



/\* Slide types \*/

.slide--title {

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; text-align: center;

}



.slide--title-content { justify-content: flex-start; }

.slide--two-col .slide-content { display: grid; grid-template-columns: 1fr 1fr; gap: 8%; }

.slide--blank { padding: 0; }



/\* Typography scales relative to slide width \*/

.slide-title {

&#x20; font-size: clamp(1.5rem, 5cqw, 3.5rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; line-height: 1.1;

&#x20; letter-spacing: -0.02em;

&#x20; margin-block-end: 0.4em;

&#x20; text-wrap: balance;

}



.slide-subtitle {

&#x20; font-size: clamp(0.875rem, 2.5cqw, 1.5rem);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.4;

}



.slide-heading {

&#x20; font-size: clamp(1.25rem, 3.5cqw, 2.25rem);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: 0.6em;

&#x20; text-wrap: balance;

}



.slide-body {

&#x20; font-size: clamp(0.75rem, 2cqw, 1.125rem);

&#x20; line-height: 1.6;

&#x20; flex: 1;

}



/\* Bullet list \*/

.slide-list {

&#x20; list-style: none;

&#x20; padding: 0;

&#x20; margin: 0;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: 0.6em;

}



.slide-list li {

&#x20; display: flex;

&#x20; gap: 0.5em;

&#x20; align-items: flex-start;

}



.slide-list li::before {

&#x20; content: '▸';

&#x20; color: var(--slide-accent, var(--color-accent));

&#x20; flex-shrink: 0;

&#x20; margin-top: 0.1em;

}



/\* Code block in slide \*/

.slide-code {

&#x20; background: rgba(0 0 0 / 0.08);

&#x20; border-radius: 0.5em;

&#x20; padding: 0.75em 1em;

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.75em;

&#x20; line-height: 1.6;

&#x20; overflow: auto;

&#x20; border: 1px solid rgba(0 0 0 / 0.1);

}



/\* Image in slide \*/

.slide-image {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; border-radius: 0.5em;

}



/\* Slide number \*/

.slide-number {

&#x20; position: absolute;

&#x20; bottom: 4%;

&#x20; right: 6%;

&#x20; font-size: clamp(0.5rem, 1.2cqw, 0.75rem);

&#x20; color: rgba(0 0 0 / 0.25);

&#x20; font-variant-numeric: tabular-nums;

}



/\* ─── Presentation themes ─── \*/

.presentation--dark {

&#x20; --slide-bg: #0f172a;

&#x20; --slide-color: #f1f5f9;

&#x20; --slide-accent: #60a5fa;

}



.presentation--gradient {

&#x20; --slide-bg: linear-gradient(135deg, #667eea, #764ba2);

&#x20; --slide-color: white;

}



.presentation--minimal {

&#x20; --slide-bg: white;

&#x20; --slide-color: #1a1a1a;

&#x20; --slide-accent: #111;

}



/\* ─── Slide transitions ─── \*/

.slide--fade.prev   { opacity: 0; translate: 0; }

.slide--fade.next   { opacity: 0; translate: 0; }



.slide--zoom.active { animation: slide-zoom-in 0.4s var(--ease-out); }

@keyframes slide-zoom-in { from { scale: 0.9; opacity: 0; } }



.slide--flip {

&#x20; transform-style: preserve-3d;

&#x20; backface-visibility: hidden;

}

.slide--flip.prev { animation: slide-flip-out 0.4s ease-in forwards; }

.slide--flip.next { animation: slide-flip-in 0.4s ease-out; }



@keyframes slide-flip-out { to   { transform: rotateY(-90deg); opacity: 0; } }

@keyframes slide-flip-in  { from { transform: rotateY(90deg);  opacity: 0; } }



/\* ─── Slide thumbnails navigation ─── \*/

.slide-thumbs {

&#x20; display: flex;

&#x20; gap: var(--space-2);

&#x20; overflow-x: auto;

&#x20; padding: var(--space-2);

&#x20; background: var(--color-bg-subtle);

&#x20; scrollbar-width: thin;

}



.slide-thumb {

&#x20; flex: 0 0 160px;

&#x20; aspect-ratio: 16 / 9;

&#x20; border-radius: var(--radius-md);

&#x20; overflow: hidden;

&#x20; cursor: pointer;

&#x20; border: 2px solid transparent;

&#x20; transition: border-color var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

&#x20; position: relative;

}

.slide-thumb:hover { scale: 1.02; }

.slide-thumb.active { border-color: var(--color-accent); }



.slide-thumb\_\_num {

&#x20; position: absolute;

&#x20; bottom: 4px;

&#x20; right: 6px;

&#x20; font-size: 10px;

&#x20; color: rgba(0 0 0 / 0.4);

&#x20; font-weight: bold;

}



/\* Presenter view \*/

.presenter-view {

&#x20; display: grid;

&#x20; grid-template-columns: 2fr 1fr;

&#x20; gap: var(--space-4);

&#x20; height: 100dvh;

&#x20; padding: var(--space-4);

&#x20; background: #1a1a1a;

}



.presenter-current { border-radius: var(--radius-xl); overflow: hidden; }

.presenter-notes {

&#x20; background: #2a2a2a;

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-5);

&#x20; color: white;

&#x20; overflow-y: auto;

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.7;

}

.presenter-timer {

&#x20; font-size: clamp(2rem, 4vw, 3rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-family: var(--font-mono);

&#x20; font-variant-numeric: tabular-nums;

&#x20; color: white;

&#x20; text-align: center;

&#x20; padding: var(--space-4);

}

```



\---



\## 155. VIDEO EDITOR TIMELINE



```css

/\* ─── Video editor layout ─── \*/

.video-editor {

&#x20; display: grid;

&#x20; grid-template-rows: auto 1fr auto;

&#x20; height: 100dvh;

&#x20; background: #1a1a1a;

&#x20; color: #d0d0d0;

&#x20; font-family: var(--font-sans);

&#x20; font-size: var(--font-size-sm);

}



/\* Preview area \*/

.video-preview {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 300px;

&#x20; gap: var(--space-2);

&#x20; padding: var(--space-3);

&#x20; background: #111;

&#x20; border-bottom: 1px solid #333;

}



.video-canvas {

&#x20; aspect-ratio: 16 / 9;

&#x20; background: #000;

&#x20; border-radius: var(--radius-lg);

&#x20; overflow: hidden;

&#x20; position: relative;

}



.video-canvas video { width: 100%; height: 100%; object-fit: contain; }



/\* Playback controls \*/

.playback-controls {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; background: #1a1a1a;

&#x20; border-bottom: 1px solid #333;

}



.playback-btn {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border: none;

&#x20; background: none;

&#x20; color: rgba(255 255 255 / 0.75);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; border-radius: var(--radius-md);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.playback-btn:hover { background: rgba(255 255 255 / 0.1); color: white; }

.playback-btn--play { width: 2.5rem; height: 2.5rem; font-size: 1.25rem; }



.playback-time {

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-sm);

&#x20; font-variant-numeric: tabular-nums;

&#x20; color: rgba(255 255 255 / 0.7);

&#x20; white-space: nowrap;

}



/\* ─── Timeline ─── \*/

.timeline {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; overflow: hidden;

&#x20; background: #1e1e1e;

}



.timeline\_\_ruler {

&#x20; height: 24px;

&#x20; background: #252525;

&#x20; border-bottom: 1px solid #333;

&#x20; position: relative;

&#x20; overflow: hidden;

&#x20; flex-shrink: 0;

}



/\* Time markers \*/

.timeline\_\_tick {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; width: 1px;

&#x20; background: rgba(255 255 255 / 0.1);

}

.timeline\_\_tick::after {

&#x20; content: attr(data-time);

&#x20; position: absolute;

&#x20; top: 4px;

&#x20; left: 4px;

&#x20; font-size: 9px;

&#x20; color: rgba(255 255 255 / 0.4);

&#x20; white-space: nowrap;

}



/\* Playhead \*/

.timeline\_\_playhead {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; left: var(--playhead, 0%);

&#x20; width: 1px;

&#x20; background: #ff4757;

&#x20; z-index: 10;

&#x20; pointer-events: none;

}

.timeline\_\_playhead::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 0;

&#x20; left: -5px;

&#x20; width: 11px;

&#x20; height: 12px;

&#x20; background: #ff4757;

&#x20; clip-path: polygon(0 0, 100% 0, 50% 100%);

}



/\* Track list \*/

.timeline\_\_tracks {

&#x20; flex: 1;

&#x20; overflow: auto;

}



.timeline\_\_track {

&#x20; display: flex;

&#x20; height: 48px;

&#x20; border-bottom: 1px solid #2a2a2a;

&#x20; position: relative;

}



.timeline\_\_track-header {

&#x20; width: 160px;

&#x20; flex-shrink: 0;

&#x20; background: #252525;

&#x20; border-right: 1px solid #333;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding-inline: var(--space-3);

&#x20; position: sticky;

&#x20; left: 0;

&#x20; z-index: 1;

}



.track-label {

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.7);

&#x20; flex: 1;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



.track-mute, .track-solo {

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border: none;

&#x20; background: rgba(255 255 255 / 0.1);

&#x20; border-radius: 3px;

&#x20; color: rgba(255 255 255 / 0.5);

&#x20; cursor: pointer;

&#x20; font-size: 0.625rem;

&#x20; font-weight: bold;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.track-mute.active  { background: #ff4757; color: white; }

.track-solo.active  { background: #ffd700; color: #111; }



/\* Track content area \*/

.timeline\_\_track-content {

&#x20; flex: 1;

&#x20; position: relative;

&#x20; overflow: hidden;

}



/\* Clip \*/

.timeline-clip {

&#x20; position: absolute;

&#x20; top: 4px;

&#x20; bottom: 4px;

&#x20; background: var(--clip-color, #0078d4);

&#x20; border-radius: 4px;

&#x20; left: var(--clip-start, 0%);

&#x20; width: var(--clip-width, 20%);

&#x20; overflow: hidden;

&#x20; cursor: grab;

&#x20; transition: filter var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

&#x20; border: 1px solid rgba(255 255 255 / 0.2);

}

.timeline-clip:hover { filter: brightness(1.15); }

.timeline-clip.selected { outline: 2px solid white; outline-offset: 1px; }

.timeline-clip:active { cursor: grabbing; }



/\* Waveform in audio clip \*/

.timeline-clip\_\_waveform {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; opacity: 0.4;

&#x20; background-image: var(--waveform);

&#x20; background-size: 100% 100%;

}



.timeline-clip\_\_label {

&#x20; position: relative;

&#x20; padding: 2px 6px;

&#x20; font-size: 9px;

&#x20; color: white;

&#x20; white-space: nowrap;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; z-index: 1;

}



/\* Resize handles on clip \*/

.timeline-clip\_\_resize-left,

.timeline-clip\_\_resize-right {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; width: 8px;

&#x20; cursor: ew-resize;

&#x20; background: rgba(255 255 255 / 0.2);

&#x20; z-index: 2;

&#x20; border-radius: 2px;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

}

.timeline-clip\_\_resize-left  { left: 0; }

.timeline-clip\_\_resize-right { right: 0; }

.timeline-clip:hover .timeline-clip\_\_resize-left,

.timeline-clip:hover .timeline-clip\_\_resize-right { opacity: 1; }



/\* Video track (different color) \*/

.timeline\_\_track--video .timeline-clip { --clip-color: #764ba2; }

.timeline\_\_track--audio .timeline-clip { --clip-color: #0078d4; }

.timeline\_\_track--text  .timeline-clip { --clip-color: #2d8b47; }

.timeline\_\_track--effect .timeline-clip { --clip-color: #c47900; }

```



\---



\## 156. IMAGE ZOOM / MAGNIFIER



```css

/\* ─── Image zoom on hover ─── \*/

.zoom-container {

&#x20; position: relative;

&#x20; overflow: hidden;

&#x20; cursor: zoom-in;

}



/\* CSS-only zoom (transform scale) \*/

.zoom-container img {

&#x20; transition: transform 0.4s var(--ease-out), transform-origin 0s;

&#x20; transform-origin: var(--ox, 50%) var(--oy, 50%);

&#x20; display: block;

&#x20; width: 100%;

}



.zoom-container:hover img {

&#x20; transform: scale(2);

}



/\* ─── Magnifier lens ─── \*/

/\* JS sets --mx --my (mouse position %) \*/

.magnifier {

&#x20; position: relative;

&#x20; display: inline-block;

&#x20; cursor: crosshair;

}



.magnifier img { display: block; width: 100%; }



.magnifier-lens {

&#x20; position: absolute;

&#x20; width: 120px;

&#x20; height: 120px;

&#x20; border-radius: 50%;

&#x20; border: 2px solid white;

&#x20; box-shadow:

&#x20;   0 0 0 1px rgba(0 0 0 / 0.3),

&#x20;   var(--shadow-xl);

&#x20; pointer-events: none;

&#x20; overflow: hidden;

&#x20; left: calc(var(--mx, 50%) - 60px);

&#x20; top:  calc(var(--my, 50%) - 60px);

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

&#x20; z-index: 2;

}



.magnifier:hover .magnifier-lens { opacity: 1; }



/\* Background image = same as parent, scaled up \*/

.magnifier-lens\_\_inner {

&#x20; position: absolute;

&#x20; width: 300%;

&#x20; height: 300%;

&#x20; left: calc(-150% + 50% - (var(--mx, 50%) - 50%) \* 3);

&#x20; top:  calc(-150% + 50% - (var(--my, 50%) - 50%) \* 3);

&#x20; background-image: var(--zoom-image);

&#x20; background-size: 100% 100%;

&#x20; background-repeat: no-repeat;

}



/\* ─── Picture-in-picture zoom preview ─── \*/

.zoom-with-preview {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 220px;

&#x20; gap: var(--space-4);

&#x20; align-items: start;

}



.zoom-main {

&#x20; position: relative;

&#x20; cursor: crosshair;

&#x20; overflow: hidden;

}



.zoom-preview-box {

&#x20; position: absolute;

&#x20; border: 2px solid var(--color-accent);

&#x20; pointer-events: none;

&#x20; left: var(--preview-x, 0);

&#x20; top:  var(--preview-y, 0);

&#x20; width: var(--preview-w, 30%);

&#x20; height: var(--preview-h, 30%);

&#x20; background: rgba(59 130 246 / 0.1);

}



.zoom-preview-panel {

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; overflow: hidden;

&#x20; aspect-ratio: 1;

&#x20; background: var(--color-bg-muted);

}



.zoom-preview-panel img {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: none;

&#x20; object-position: var(--preview-pos, 0 0);

}

```



\---



\## 157. BREADCRUMB ADVANCED PATTERNS



```css

/\* ─── Standard breadcrumb ─── \*/

.breadcrumbs {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; flex-wrap: wrap;

&#x20; gap: 0.25rem;

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; padding: var(--space-2) 0;

}



.breadcrumb-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25rem;

}



/\* Separator \*/

.breadcrumb-item + .breadcrumb-item::before {

&#x20; content: '/';

&#x20; color: var(--color-border-strong);

&#x20; margin-inline-end: 0.25rem;

}



/\* Chevron separator \*/

.breadcrumbs--chevron .breadcrumb-item + .breadcrumb-item::before {

&#x20; content: '';

&#x20; width: 6px;

&#x20; height: 6px;

&#x20; border-right: 1.5px solid var(--color-border-strong);

&#x20; border-top: 1.5px solid var(--color-border-strong);

&#x20; rotate: 45deg;

&#x20; margin-inline-end: 0.25rem;

}



/\* Dot separator \*/

.breadcrumbs--dot .breadcrumb-item + .breadcrumb-item::before {

&#x20; content: '•';

&#x20; font-size: 0.5em;

&#x20; vertical-align: middle;

&#x20; color: var(--color-border-strong);

}



.breadcrumb-link {

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: none;

&#x20; transition: color var(--duration-fast);

&#x20; padding: 0.125rem 0.25rem;

&#x20; border-radius: var(--radius-sm);

}

.breadcrumb-link:hover {

&#x20; color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, transparent);

&#x20; text-decoration: none;

}



.breadcrumb-item:last-child {

&#x20; color: var(--color-text);

&#x20; font-weight: var(--font-weight-medium);

&#x20; pointer-events: none;

}



/\* Collapsible breadcrumbs (for deep navigation) \*/

.breadcrumbs--collapsible .breadcrumb-item.collapsed { display: none; }

.breadcrumbs--collapsible .breadcrumb-item.collapsed.show { display: flex; }



.breadcrumb-ellipsis {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; padding: 0.125rem 0.375rem;

&#x20; border-radius: var(--radius-sm);

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; background: var(--color-bg-subtle);

&#x20; transition: background var(--duration-fast);

&#x20; font-size: 0.8em;

&#x20; font-weight: var(--font-weight-bold);

&#x20; letter-spacing: 0.05em;

}

.breadcrumb-ellipsis:hover { background: var(--color-bg-muted); }



/\* ─── Breadcrumb with icons ─── \*/

.breadcrumbs--icons .breadcrumb-link {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.375rem;

}



.breadcrumb-icon {

&#x20; width: 1rem;

&#x20; height: 1rem;

&#x20; flex-shrink: 0;

&#x20; opacity: 0.7;

}



/\* ─── Floating breadcrumb pill ─── \*/

.breadcrumbs--pill {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-full);

&#x20; padding: var(--space-2) var(--space-3);

&#x20; display: inline-flex;

&#x20; box-shadow: var(--shadow-sm);

}



/\* ─── Breadcrumb with dropdown on click ─── \*/

.breadcrumb-dropdown {

&#x20; position: relative;

}



.breadcrumb-dropdown-menu {

&#x20; position: absolute;

&#x20; top: calc(100% + 4px);

&#x20; left: 0;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; box-shadow: var(--shadow-xl);

&#x20; padding: var(--space-1);

&#x20; z-index: var(--z-dropdown);

&#x20; min-width: 160px;

&#x20; display: none;

}



.breadcrumb-dropdown:focus-within .breadcrumb-dropdown-menu { display: block; }



.breadcrumb-dropdown-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: var(--space-2) var(--space-3);

&#x20; border-radius: var(--radius-md);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text);

&#x20; text-decoration: none;

&#x20; transition: background var(--duration-fast);

}

.breadcrumb-dropdown-item:hover { background: var(--color-bg-subtle); }

```



\---



\## 158. PRINT CSS DEEP DIVE



```css

/\* ─── Complete print stylesheet ─── \*/

@media print {



&#x20; /\* ─── Page setup ─── \*/

&#x20; @page {

&#x20;   size: A4 portrait;

&#x20;   margin: 2cm 2.5cm;



&#x20;   /\* Headers and footers \*/

&#x20;   @top-left {

&#x20;     content: 'Company Name';

&#x20;     font-size: 9pt;

&#x20;     color: #666;

&#x20;   }

&#x20;   @top-right {

&#x20;     content: string(chapter-title);

&#x20;     font-size: 9pt;

&#x20;     color: #666;

&#x20;   }

&#x20;   @bottom-center {

&#x20;     content: counter(page) ' / ' counter(pages);

&#x20;     font-size: 9pt;

&#x20;     color: #666;

&#x20;   }

&#x20;   @bottom-left {

&#x20;     content: 'Printed: ' date(now, '%Y-%m-%d');

&#x20;     font-size: 8pt;

&#x20;     color: #999;

&#x20;   }

&#x20; }



&#x20; @page :first {

&#x20;   @top-left { content: ''; }

&#x20;   @top-right { content: ''; }

&#x20;   margin-top: 3cm;

&#x20; }



&#x20; @page :left {

&#x20;   margin-left: 3cm;

&#x20;   margin-right: 2cm;

&#x20; }



&#x20; @page :right {

&#x20;   margin-left: 2cm;

&#x20;   margin-right: 3cm;

&#x20; }



&#x20; /\* ─── Reset for print ─── \*/

&#x20; \*,

&#x20; \*::before,

&#x20; \*::after {

&#x20;   background: transparent !important;

&#x20;   color: #000 !important;

&#x20;   box-shadow: none !important;

&#x20;   text-shadow: none !important;

&#x20; }



&#x20; body {

&#x20;   font-family: Georgia, 'Times New Roman', serif;

&#x20;   font-size: 11pt;

&#x20;   line-height: 1.5;

&#x20;   color: #000;

&#x20;   background: white;

&#x20; }



&#x20; /\* ─── Hide non-print elements ─── \*/

&#x20; nav,

&#x20; header:not(.print-header),

&#x20; footer:not(.print-footer),

&#x20; aside,

&#x20; .sidebar,

&#x20; .no-print,

&#x20; .btn,

&#x20; button:not(.print-btn),

&#x20; .modal,

&#x20; .toast,

&#x20; .tooltip,

&#x20; .cookie-banner,

&#x20; .back-top-btn,

&#x20; .share-bar,

&#x20; .toc,

&#x20; .ads,

&#x20; video,

&#x20; audio,

&#x20; iframe:not(.print-iframe),

&#x20; \[aria-hidden="true"] {

&#x20;   display: none !important;

&#x20; }



&#x20; /\* ─── Show print-only elements ─── \*/

&#x20; .print-only { display: block !important; }

&#x20; .print-inline { display: inline !important; }



&#x20; /\* ─── Typography ─── \*/

&#x20; h1 { font-size: 22pt; page-break-before: always; }

&#x20; h1:first-child { page-break-before: auto; }

&#x20; h2 { font-size: 16pt; }

&#x20; h3 { font-size: 13pt; }

&#x20; h4 { font-size: 11pt; }



&#x20; h1, h2, h3, h4, h5, h6 {

&#x20;   page-break-after: avoid;

&#x20;   orphans: 3;

&#x20;   widows: 3;

&#x20; }



&#x20; p, li {

&#x20;   orphans: 3;

&#x20;   widows: 3;

&#x20;   font-size: 11pt;

&#x20; }



&#x20; /\* String set for running headers \*/

&#x20; h2 { string-set: chapter-title content(); }



&#x20; /\* ─── Links ─── \*/

&#x20; a\[href]::after {

&#x20;   content: ' (' attr(href) ')';

&#x20;   font-size: 9pt;

&#x20;   color: #555;

&#x20;   word-break: break-all;

&#x20; }



&#x20; /\* Don't show URLs for internal/JS links \*/

&#x20; a\[href^="#"]::after,

&#x20; a\[href^="javascript:"]::after,

&#x20; a\[href^="tel:"]::after,

&#x20; a\[href^="mailto:"]::after,

&#x20; a.no-print-url::after {

&#x20;   content: '';

&#x20; }



&#x20; /\* ─── Images ─── \*/

&#x20; img {

&#x20;   max-width: 100% !important;

&#x20;   page-break-inside: avoid;

&#x20; }



&#x20; figure { page-break-inside: avoid; }



&#x20; figcaption {

&#x20;   font-size: 9pt;

&#x20;   font-style: italic;

&#x20;   color: #555;

&#x20;   text-align: center;

&#x20; }



&#x20; /\* ─── Tables ─── \*/

&#x20; table { border-collapse: collapse; width: 100%; }

&#x20; th, td { border: 1px solid #ccc; padding: 6pt 8pt; font-size: 10pt; }

&#x20; th { background: #f5f5f5 !important; font-weight: bold; }



&#x20; thead { display: table-header-group; } /\* Repeat on every page \*/

&#x20; tfoot { display: table-footer-group; }

&#x20; tr    { page-break-inside: avoid; }



&#x20; /\* ─── Code blocks ─── \*/

&#x20; pre, code {

&#x20;   font-family: 'Courier New', monospace;

&#x20;   font-size: 9pt;

&#x20;   background: #f8f8f8 !important;

&#x20;   border: 1px solid #ddd;

&#x20;   color: #000 !important;

&#x20; }



&#x20; pre {

&#x20;   white-space: pre-wrap;

&#x20;   word-break: break-all;

&#x20;   page-break-inside: avoid;

&#x20;   padding: 8pt;

&#x20;   border-radius: 3pt;

&#x20; }



&#x20; /\* ─── Page breaks ─── \*/

&#x20; .page-break-before  { page-break-before: always; break-before: page; }

&#x20; .page-break-after   { page-break-after: always;  break-after: page; }

&#x20; .no-page-break      { page-break-inside: avoid;  break-inside: avoid; }

&#x20; .page-break-column  { break-before: column; }



&#x20; blockquote { page-break-inside: avoid; }

&#x20; section    { page-break-inside: avoid; }



&#x20; /\* ─── Grid/Flex reset ─── \*/

&#x20; .grid, .flex { display: block !important; }

&#x20; .col, \[class\*="col-"] { width: 100% !important; float: none !important; }



&#x20; /\* ─── Sidebar layout → single column ─── \*/

&#x20; .with-sidebar { display: block !important; }

&#x20; .sidebar { display: none !important; }



&#x20; /\* ─── QR code for URL ─── \*/

&#x20; .print-qr {

&#x20;   display: block !important;

&#x20;   width: 80pt;

&#x20;   height: 80pt;

&#x20; }



&#x20; /\* ─── Color coding for print (patterns instead) ─── \*/

&#x20; .status-success { border: 2px solid #000; }

&#x20; .status-warning { border: 2px dashed #000; }

&#x20; .status-error   { border: 2px dotted #000; }



&#x20; /\* ─── CSS Counters for print ─── \*/

&#x20; body { counter-reset: print-section; }

&#x20; h2 {

&#x20;   counter-increment: print-section;

&#x20;   counter-reset: print-subsection;

&#x20; }

&#x20; h2::before { content: counter(print-section) '. '; }



&#x20; h3 { counter-increment: print-subsection; }

&#x20; h3::before { content: counter(print-section) '.' counter(print-subsection) '. '; }

}

```



\---



\## 159. FONT LOADING STRATEGIES



```css

/\* ─── Strategy 1: font-display: swap (most common) ─── \*/

@font-face {

&#x20; font-family: 'PrimaryFont';

&#x20; src: url('font.woff2') format('woff2');

&#x20; font-weight: 400;

&#x20; font-style: normal;

&#x20; font-display: swap;

&#x20; /\* FOUT: Flash of Unstyled Text — system font → custom font \*/

}



/\* ─── Strategy 2: font-display: optional (no CLS) ─── \*/

@font-face {

&#x20; font-family: 'PerformanceFont';

&#x20; src: url('font.woff2') format('woff2');

&#x20; font-display: optional;

&#x20; /\* Only uses font if already cached (100ms budget) \*/

&#x20; /\* No layout shift, no FOUT — best CLS score \*/

}



/\* ─── Strategy 3: Size-adjust to eliminate FOUT ─── \*/

/\* Match fallback font metrics to custom font \*/

@font-face {

&#x20; font-family: 'FallbackArial';

&#x20; src: local('Arial');

&#x20; ascent-override: 90%;

&#x20; descent-override: 22%;

&#x20; line-gap-override: 0%;

&#x20; size-adjust: 107%;

}



@font-face {

&#x20; font-family: 'MyFont';

&#x20; src: url('myfont.woff2') format('woff2');

&#x20; font-display: swap;

}



body {

&#x20; font-family: 'MyFont', 'FallbackArial', Arial, sans-serif;

&#x20; /\* Fallback metrics match → no layout shift during swap \*/

}



/\* ─── Strategy 4: Preloading critical fonts ─── \*/

/\*

HTML in <head>:

<link rel="preload" href="font-regular.woff2" as="font" type="font/woff2" crossorigin>

<link rel="preload" href="font-bold.woff2" as="font" type="font/woff2" crossorigin>

\*/



/\* ─── Strategy 5: Subsetting via unicode-range ─── \*/

@font-face {

&#x20; font-family: 'MyFont';

&#x20; src: url('font-latin.woff2') format('woff2');

&#x20; unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA,

&#x20;                U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+2074, U+20AC,

&#x20;                U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;

&#x20; font-display: swap;

}



@font-face {

&#x20; font-family: 'MyFont';

&#x20; src: url('font-cyrillic.woff2') format('woff2');

&#x20; unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;

&#x20; font-display: swap;

}



/\* ─── Strategy 6: Variable font (single file for all weights) ─── \*/

@font-face {

&#x20; font-family: 'MyVariableFont';

&#x20; src: url('font-variable.woff2') format('woff2-variations');

&#x20; font-weight: 100 900;

&#x20; font-style: normal oblique 0deg 12deg;

&#x20; font-stretch: 75% 125%;

&#x20; font-display: swap;

}



/\* ─── Strategy 7: System font stack (no loading at all) ─── \*/

:root {

&#x20; /\* Modern OS system fonts — fast, no network \*/

&#x20; --font-system: system-ui, -apple-system, 'Segoe UI', Roboto,

&#x20;                'Helvetica Neue', Arial, 'Noto Sans', sans-serif,

&#x20;                'Apple Color Emoji', 'Segoe UI Emoji';



&#x20; --font-system-mono: ui-monospace, 'Cascadia Code', 'Source Code Pro',

&#x20;                     Menlo, Consolas, 'DejaVu Sans Mono', monospace;



&#x20; --font-system-serif: ui-serif, Georgia, Cambria, 'Times New Roman', Times, serif;

}



/\* ─── Font smoothing per OS ─── \*/

@media (-webkit-min-device-pixel-ratio: 1.5) {

&#x20; /\* Retina / HiDPI — antialiased looks better \*/

&#x20; body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

}



/\* ─── Font loaded state via JS ─── \*/

/\* document.fonts.ready.then(() => document.body.classList.add('fonts-loaded')) \*/



.fonts-loaded body {

&#x20; font-family: 'MyFont', var(--font-system);

}



/\* ─── Prevent invisible text during load ─── \*/

/\* font-display: block = FOIT (Flash of Invisible Text) = bad for UX \*/

/\* Only use for icon fonts where fallback makes no sense \*/

@font-face {

&#x20; font-family: 'IconFont';

&#x20; src: url('icons.woff2') format('woff2');

&#x20; font-display: block; /\* wait for icon font, don't show broken characters \*/

}



/\* ─── CSS Font Loading API detection ─── \*/

/\*

document.fonts.load('1em MyFont').then(() => {

&#x20; // Font loaded, apply font-specific styles

&#x20; document.documentElement.classList.add('font-loaded');

});

\*/

```



\---



\## 160. CSS PERFORMANCE COMPLETE CHECKLIST



```css

/\*

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

║  SPECIFICITY \& CASCADE                                               ║

║  ─────────────────────────────────────────────────────────────────  ║

║  □ No ID selectors in authored CSS                                   ║

║  □ Max specificity 0-2-0                                             ║

║  □ @layer used for organization                                      ║

║  □ !important only in utilities/reset                                ║

║  □ No universal selector (\*) in production with heavy properties     ║

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

\*/



/\* ─── Common performance anti-patterns and fixes ─── \*/



/\* ❌ Animating layout properties \*/

@keyframes bad-size {

&#x20; from { width: 0; height: 0; }

&#x20; to   { width: 100px; height: 100px; }

}



/\* ✅ Use transform instead \*/

@keyframes good-size {

&#x20; from { transform: scale(0); }

&#x20; to   { transform: scale(1); }

}



/\* ❌ Forcing layout recalculation \*/

.el { transition: margin 0.3s; }

.el:hover { margin: 10px; }  /\* reflow on every frame \*/



/\* ✅ GPU-composited property \*/

.el { transition: translate 0.3s; }

.el:hover { translate: 10px 0; }



/\* ❌ Expensive selector recalculation \*/

.list:has(li:nth-child(n):hover) \~ .other { color: red; }

/\* Triggers recalc on every mouse move over any li \*/



/\* ✅ Use JS to toggle class \*/

.list.has-hover \~ .other { color: red; }



/\* ❌ Painting entire page \*/

body { background-attachment: fixed; } /\* repaint on scroll \*/



/\* ✅ Use scroll-driven animation or pseudoelement \*/

.hero::before {

&#x20; content: '';

&#x20; position: fixed; inset: 0;

&#x20; background-image: url('bg.jpg');

&#x20; z-index: -1;

}



/\* ─── contain patterns for components ─── \*/

.feed-item {

&#x20; contain: layout paint;

&#x20; /\* Layout: children don't affect outside layout \*/

&#x20; /\* Paint: renders in own layer, clips \*/

}



.widget {

&#x20; contain: strict;

&#x20; /\* All constraints — for truly isolated components \*/

}



/\* ─── Lazy rendering patterns ─── \*/

.below-fold {

&#x20; content-visibility: auto;

&#x20; contain-intrinsic-block-size: 500px;

&#x20; /\* Browser skips rendering until near viewport \*/

&#x20; /\* 500px = placeholder height for accurate scroll \*/

}

```



\---



\## 161. ADVANCED OKLCH COLOR SYSTEM



```css

/\* ─── Complete oklch-based design system ─── \*/



/\* Generate a full scale from a single oklch definition \*/

:root {

&#x20; /\* Define brand via hue angle \*/

&#x20; --hue-brand:    250;   /\* blue-purple \*/

&#x20; --hue-success:  145;   /\* green \*/

&#x20; --hue-warning:  65;    /\* yellow-amber \*/

&#x20; --hue-danger:   25;    /\* red-orange \*/

&#x20; --hue-info:     220;   /\* blue \*/

&#x20; --chroma-mid:   0.20;



&#x20; /\* ── Brand scale ── \*/

&#x20; --brand-50:  oklch(0.975 calc(var(--chroma-mid)\*0.12) var(--hue-brand));

&#x20; --brand-100: oklch(0.940 calc(var(--chroma-mid)\*0.22) var(--hue-brand));

&#x20; --brand-200: oklch(0.890 calc(var(--chroma-mid)\*0.38) var(--hue-brand));

&#x20; --brand-300: oklch(0.820 calc(var(--chroma-mid)\*0.60) var(--hue-brand));

&#x20; --brand-400: oklch(0.730 calc(var(--chroma-mid)\*0.80) var(--hue-brand));

&#x20; --brand-500: oklch(0.630 var(--chroma-mid) var(--hue-brand));

&#x20; --brand-600: oklch(0.540 var(--chroma-mid) var(--hue-brand));

&#x20; --brand-700: oklch(0.450 var(--chroma-mid) var(--hue-brand));

&#x20; --brand-800: oklch(0.355 calc(var(--chroma-mid)\*0.9) var(--hue-brand));

&#x20; --brand-900: oklch(0.270 calc(var(--chroma-mid)\*0.8) var(--hue-brand));

&#x20; --brand-950: oklch(0.180 calc(var(--chroma-mid)\*0.6) var(--hue-brand));



&#x20; /\* ── Relative color for tints/shades ── \*/

&#x20; --brand-light:   oklch(from var(--brand-500) calc(l + 0.25) c h);

&#x20; --brand-lighter: oklch(from var(--brand-500) calc(l + 0.4) c h);

&#x20; --brand-dark:    oklch(from var(--brand-500) calc(l - 0.2) c h);

&#x20; --brand-darker:  oklch(from var(--brand-500) calc(l - 0.35) c h);

&#x20; --brand-alpha-10: oklch(from var(--brand-500) l c h / 0.1);

&#x20; --brand-alpha-20: oklch(from var(--brand-500) l c h / 0.2);



&#x20; /\* ── Analogous colors ── \*/

&#x20; --brand-warm: oklch(from var(--brand-500) l c calc(h - 30));

&#x20; --brand-cool: oklch(from var(--brand-500) l c calc(h + 30));



&#x20; /\* ── Complementary ── \*/

&#x20; --brand-complement: oklch(from var(--brand-500) l c calc(h + 180));



&#x20; /\* ── Accessible pair (auto-contrast) ── \*/

&#x20; /\* For text ON brand-500 background: \*/

&#x20; --brand-text-light: oklch(0.98 0.01 var(--hue-brand));  /\* near white \*/

&#x20; --brand-text-dark:  oklch(0.20 0.05 var(--hue-brand));  /\* near black \*/



&#x20; /\* ── Muted/desaturated version ── \*/

&#x20; --brand-muted: oklch(from var(--brand-500) l calc(c \* 0.35) h);



&#x20; /\* ── Vivid / boosted version ── \*/

&#x20; --brand-vivid: oklch(from var(--brand-500) l calc(c \* 1.5) h);

}



/\* ─── Adaptive contrast via CSS ─── \*/

/\* APCA-like — check L difference \*/

.on-brand-bg {

&#x20; /\* Automatically pick readable text based on background lightness \*/

&#x20; color: oklch(from var(--bg-color, var(--brand-500))

&#x20;   clamp(0, calc((0.6 - l) \* 9999), 1)   /\* 0 if bg is light, 1 if dark \*/

&#x20;   0

&#x20;   0                                      /\* pure white or black \*/

&#x20; );

}



/\* ─── Perceptual gradient ─── \*/

/\* Linear-gradient in oklch = perceptually uniform \*/

.oklch-gradient {

&#x20; background: linear-gradient(

&#x20;   to right,

&#x20;   oklch(0.6 0.2 260),

&#x20;   oklch(0.6 0.2 200)

&#x20; );

&#x20; /\* vs sRGB gradient which has dark muddy middle \*/

}



/\* ─── Color space comparison ─── \*/

.gradient-srgb    { background: linear-gradient(in srgb to right, red, blue); }

.gradient-oklch   { background: linear-gradient(in oklch to right, red, blue); }

.gradient-hsl     { background: linear-gradient(in hsl to right, red, blue); }

/\* oklch version looks most natural and vibrant in the middle \*/

```



\---



\## 162. CSS VARIABLES — MEGA REFERENCE



```css

/\* ─── Every CSS variable pattern ─── \*/



/\* 1. Simple value \*/

:root { --color: red; }



/\* 2. With fallback \*/

.el { color: var(--color, blue); }



/\* 3. Fallback chain \*/

.el { font-size: var(--size-custom, var(--size-default, 1rem)); }



/\* 4. Computed from another variable \*/

:root {

&#x20; --base: 16;

&#x20; --lg: calc(var(--base) \* 1.25px);

}



/\* 5. Component namespace pattern \*/

.btn {

&#x20; --\_bg: var(--btn-bg, var(--color-accent));  /\* --\_ = private \*/

&#x20; background: var(--\_bg);

}



/\* 6. Boolean / toggle (space toggle) \*/

.el {

&#x20; --is-active: ;        /\* empty = false \*/

&#x20; color: var(--is-active, initial) red;  /\* red when true \*/

}

.el.active { --is-active: initial; }   /\* set to truthy \*/



/\* 7. Typed variable via @property \*/

@property --progress {

&#x20; syntax: '<number>';

&#x20; initial-value: 0;

&#x20; inherits: false;

}

.el {

&#x20; --progress: 0;

&#x20; animation: fill linear;

&#x20; animation-timeline: scroll();

}

@keyframes fill { to { --progress: 1; } }

width: calc(var(--progress) \* 100%);



/\* 8. Color channel decomposition \*/

:root {

&#x20; --accent-h: 250;

&#x20; --accent-c: 0.2;

&#x20; --accent-l: 0.6;

&#x20; --accent: oklch(var(--accent-l) var(--accent-c) var(--accent-h));

&#x20; --accent-hover: oklch(calc(var(--accent-l) - 0.1) var(--accent-c) var(--accent-h));

}



/\* 9. Contextual override via data-attributes \*/

\[data-size="sm"] { --size: 0.875rem; }

\[data-size="md"] { --size: 1rem; }

\[data-size="lg"] { --size: 1.25rem; }

.text { font-size: var(--size, 1rem); }



/\* 10. Responsive variable (breakpoint-based) \*/

:root { --columns: 1; }

@media (min-width: 640px)  { :root { --columns: 2; } }

@media (min-width: 1024px) { :root { --columns: 3; } }

.grid { grid-template-columns: repeat(var(--columns), 1fr); }



/\* 11. Theme variable override \*/

\[data-theme="dark"]  { --bg: #111; --text: #f0f0f0; }

\[data-theme="light"] { --bg: #fff; --text: #111; }



/\* 12. Animation state via variable \*/

.animated {

&#x20; --state: 0;

&#x20; translate: calc(var(--state) \* 100px) 0;

&#x20; transition: translate 0.3s;

}

.animated.active { --state: 1; }



/\* 13. Fluid clamp with variable inputs \*/

:root {

&#x20; --min: 1rem;

&#x20; --max: 2rem;

&#x20; --fluid: clamp(var(--min), 2vw + 0.5rem, var(--max));

}

h1 { font-size: var(--fluid); }



/\* 14. Z-index scale via variable \*/

:root {

&#x20; --z-base: 0;

&#x20; --z-dropdown: 10;

&#x20; --z-sticky: 20;

&#x20; --z-modal: 50;

}



/\* 15. Animation delay stagger \*/

.items > \* {

&#x20; animation-delay: calc(var(--i, 0) \* 50ms);

}

/\* Set --i via: style="--i: 0", "1", "2"... or JS \*/



/\* 16. Grid-responsive via variable \*/

.grid {

&#x20; --min-col: 250px;

&#x20; --cols: auto-fit;

&#x20; grid-template-columns: repeat(var(--cols), minmax(var(--min-col), 1fr));

}

.grid-fixed { --cols: 3; }



/\* 17. Semantic color aliasing \*/

:root {

&#x20; --color-primary-raw: #3b82f6;

&#x20; --color-primary: var(--color-primary-raw);  /\* alias for override \*/

}

/\* User can override --color-primary without touching raw \*/



/\* 18. Cascading component tokens \*/

.theme-orange { --accent: orange; }

.theme-orange .btn { /\* inherits --accent: orange \*/ }



/\* 19. Math utilities \*/

:root {

&#x20; --ratio: 1.618;

&#x20; --step-0: 1rem;

&#x20; --step-1: calc(var(--step-0) \* var(--ratio));

&#x20; --step-2: calc(var(--step-1) \* var(--ratio));

&#x20; --step--1: calc(var(--step-0) / var(--ratio));

}



/\* 20. Environment variable integration \*/

.safe {

&#x20; padding-top: max(var(--space-4), env(safe-area-inset-top));

}

```



\---



```

╔══════════════════════════════════════════════════════════════════════╗

║              CSS MASTER GUIDE — PARTS I–X                            ║

╠══════════════════════════════════════════════════════════════════════╣

║  162 chapters · 1,000+ code examples · \~35,000+ lines               ║

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

