\# PART VIII — CSS: FINAL FRONTIER PATTERNS



\---



\## 130. FULL CALENDAR / MONTH VIEW



```css

/\* ─── Calendar month view ─── \*/

.calendar {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; user-select: none;

}



/\* Header \*/

.calendar\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-4) var(--space-5);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; background: var(--color-bg-subtle);

}



.calendar\_\_month-year {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-base);

}



.calendar\_\_nav {

&#x20; display: flex;

&#x20; gap: var(--space-1);

}



.cal-nav-btn {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border: none;

&#x20; background: none;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.cal-nav-btn:hover { background: var(--color-bg-muted); color: var(--color-text); }



/\* View switcher \*/

.calendar\_\_views {

&#x20; display: flex;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; overflow: hidden;

}

.cal-view-btn {

&#x20; padding: 0.25rem 0.75rem;

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

&#x20; color: var(--color-text-muted);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.cal-view-btn.active {

&#x20; background: var(--color-accent);

&#x20; color: white;

}



/\* Weekday header row \*/

.calendar\_\_weekdays {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(7, 1fr);

&#x20; border-bottom: 1px solid var(--color-border);

}



.calendar\_\_weekday {

&#x20; padding: var(--space-2);

&#x20; text-align: center;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wide);

&#x20; color: var(--color-text-muted);

}



/\* Days grid \*/

.calendar\_\_grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(7, 1fr);

&#x20; grid-auto-rows: minmax(80px, auto);

}



.calendar\_\_cell {

&#x20; border-right: 1px solid var(--color-border);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; padding: var(--space-2);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: 2px;

&#x20; min-height: 80px;

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast);

&#x20; position: relative;

&#x20; overflow: hidden;

}



.calendar\_\_cell:nth-child(7n) { border-right: none; }

.calendar\_\_cell:hover { background: var(--color-bg-subtle); }

.calendar\_\_cell:focus-visible { outline: 2px solid var(--color-accent); outline-offset: -2px; }



/\* Day number \*/

.cal-day-num {

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; border-radius: 50%;

&#x20; align-self: flex-start;

&#x20; font-variant-numeric: tabular-nums;

&#x20; flex-shrink: 0;

}



/\* Today \*/

.calendar\_\_cell--today .cal-day-num {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; font-weight: var(--font-weight-bold);

}



/\* Selected \*/

.calendar\_\_cell--selected {

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, transparent);

}

.calendar\_\_cell--selected .cal-day-num {

&#x20; background: var(--color-accent);

&#x20; color: white;

}



/\* Outside month \*/

.calendar\_\_cell--outside {

&#x20; background: var(--color-bg-subtle);

&#x20; opacity: 0.5;

}



/\* Weekend \*/

.calendar\_\_cell--weekend .cal-day-num { color: var(--color-text-muted); }



/\* Events \*/

.cal-event {

&#x20; border-radius: 3px;

&#x20; padding: 1px 6px;

&#x20; font-size: 0.6875rem;

&#x20; font-weight: var(--font-weight-medium);

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

&#x20; cursor: pointer;

&#x20; transition: filter var(--duration-fast);

}

.cal-event:hover { filter: brightness(0.9); }



.cal-event--blue    { background: var(--color-brand-100); color: var(--color-brand-800); }

.cal-event--green   { background: var(--color-success-100); color: var(--color-success-800); }

.cal-event--red     { background: var(--color-danger-100); color: var(--color-danger-800); }

.cal-event--yellow  { background: var(--color-warning-100); color: var(--color-warning-800); }

.cal-event--purple  { background: oklch(0.93 0.05 300); color: oklch(0.35 0.15 300); }



/\* All-day / multi-day events \*/

.cal-event--multi {

&#x20; border-radius: 0;

&#x20; margin-inline: -var(--space-2);

&#x20; padding-inline: var(--space-2);

}

.cal-event--start { border-radius: 3px 0 0 3px; }

.cal-event--end   { border-radius: 0 3px 3px 0; }



/\* More events indicator \*/

.cal-more {

&#x20; font-size: 0.6875rem;

&#x20; color: var(--color-text-muted);

&#x20; cursor: pointer;

&#x20; padding: 1px 4px;

&#x20; border-radius: 3px;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.cal-more:hover { background: var(--color-bg-muted); color: var(--color-text); }



/\* Week view \*/

.calendar--week .calendar\_\_grid {

&#x20; grid-template-columns: 50px repeat(7, 1fr);

&#x20; grid-auto-rows: 48px;

}



.calendar\_\_time-col { font-size: 0.6875rem; color: var(--color-text-subtle); padding-inline-end: var(--space-2); text-align: right; padding-block-start: var(--space-1); }

```



\---



\## 131. SPREADSHEET-LIKE UI



```css

/\* ─── Data grid / spreadsheet ─── \*/

.spreadsheet {

&#x20; display: grid;

&#x20; overflow: auto;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-sm);

&#x20; position: relative;

}



.spreadsheet-table {

&#x20; border-collapse: collapse;

&#x20; width: max-content;

&#x20; min-width: 100%;

}



/\* Corner cell \*/

.spreadsheet-corner {

&#x20; position: sticky;

&#x20; top: 0;

&#x20; left: 0;

&#x20; z-index: 4;

&#x20; width: 40px;

&#x20; background: var(--color-bg-muted);

&#x20; border-right: 2px solid var(--color-border);

&#x20; border-bottom: 2px solid var(--color-border);

}



/\* Column headers \*/

.spreadsheet-table thead th {

&#x20; position: sticky;

&#x20; top: 0;

&#x20; z-index: 3;

&#x20; background: var(--color-bg-subtle);

&#x20; border: 1px solid var(--color-border);

&#x20; padding: 0.375rem 0.5rem;

&#x20; text-align: center;

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; min-width: 100px;

&#x20; white-space: nowrap;

&#x20; cursor: pointer;

&#x20; user-select: none;

&#x20; transition: background var(--duration-fast);

}



.spreadsheet-table thead th:hover { background: var(--color-bg-muted); }

.spreadsheet-table thead th.selected { background: color-mix(in srgb, var(--color-accent) 20%, var(--color-bg-subtle)); }



/\* Row headers \*/

.spreadsheet-table tbody td:first-child {

&#x20; position: sticky;

&#x20; left: 0;

&#x20; z-index: 2;

&#x20; background: var(--color-bg-subtle);

&#x20; border-right: 2px solid var(--color-border);

&#x20; padding: 0.25rem 0.5rem;

&#x20; text-align: center;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; min-width: 40px;

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast);

}



.spreadsheet-table tbody td:first-child:hover { background: var(--color-bg-muted); }



/\* Data cells \*/

.spreadsheet-cell {

&#x20; border: 1px solid var(--color-border);

&#x20; padding: 0.25rem 0.5rem;

&#x20; height: 28px;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

&#x20; cursor: cell;

&#x20; position: relative;

&#x20; transition: background var(--duration-fast);

&#x20; max-width: 200px;

}



.spreadsheet-cell:hover { background: color-mix(in srgb, var(--color-accent) 4%, var(--color-surface)); }



/\* Selected cell \*/

.spreadsheet-cell.selected {

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, var(--color-surface));

&#x20; outline: 2px solid var(--color-accent);

&#x20; outline-offset: -2px;

&#x20; z-index: 1;

}



/\* Editing cell \*/

.spreadsheet-cell.editing {

&#x20; padding: 0;

&#x20; overflow: visible;

&#x20; z-index: 5;

}



.cell-input {

&#x20; position: absolute;

&#x20; inset: -1px;

&#x20; border: 2px solid var(--color-accent);

&#x20; border-radius: 2px;

&#x20; padding: 0.25rem 0.5rem;

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; background: var(--color-surface);

&#x20; outline: none;

&#x20; z-index: 10;

&#x20; min-width: 100px;

&#x20; box-shadow: var(--shadow-lg);

}



/\* Range selection \*/

.spreadsheet-cell.in-range {

&#x20; background: color-mix(in srgb, var(--color-accent) 12%, var(--color-surface));

}



/\* Cell types \*/

.cell-number { text-align: end; font-variant-numeric: tabular-nums; }

.cell-formula { color: var(--color-brand-700); }

.cell-error   { color: var(--color-danger-500); font-weight: var(--font-weight-semibold); }

.cell-boolean { text-align: center; font-weight: var(--font-weight-semibold); }



/\* Freeze indicator \*/

.spreadsheet-table thead th.frozen::after,

.spreadsheet-table tbody td.frozen::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; right: -2px;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; width: 2px;

&#x20; background: var(--color-accent);

&#x20; opacity: 0.5;

}



/\* Column resize handle \*/

.col-resize {

&#x20; position: absolute;

&#x20; right: 0;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; width: 4px;

&#x20; cursor: col-resize;

&#x20; z-index: 1;

}

.col-resize:hover { background: var(--color-accent); opacity: 0.7; }



/\* Formula bar \*/

.formula-bar {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.25rem var(--space-3);

&#x20; background: var(--color-surface);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-sm);

}



.formula-bar\_\_cell-ref {

&#x20; min-width: 60px;

&#x20; padding: 0.25rem 0.5rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-sm);

&#x20; font: inherit;

&#x20; text-align: center;

&#x20; outline: none;

}



.formula-bar\_\_input {

&#x20; flex: 1;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-sm);

&#x20; padding: 0.25rem 0.5rem;

&#x20; font: inherit;

&#x20; outline: none;

&#x20; transition: border-color var(--duration-fast);

}

.formula-bar\_\_input:focus { border-color: var(--color-accent); }



.formula-bar\_\_fx {

&#x20; color: var(--color-brand-700);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-style: italic;

}

```



\---



\## 132. RICH TEXT EDITOR STYLING



```css

/\* ─── Editor toolbar ─── \*/

.editor-toolbar {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; padding: var(--space-2) var(--space-3);

&#x20; background: var(--color-bg-subtle);

&#x20; border: 1px solid var(--color-border);

&#x20; border-bottom: none;

&#x20; border-radius: var(--radius-xl) var(--radius-xl) 0 0;

}



.toolbar-btn {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border: none;

&#x20; background: none;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-bold);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.toolbar-btn:hover { background: var(--color-bg-muted); color: var(--color-text); }

.toolbar-btn.active {

&#x20; background: color-mix(in srgb, var(--color-accent) 15%, transparent);

&#x20; color: var(--color-accent);

}

.toolbar-btn:disabled { opacity: 0.3; cursor: not-allowed; }



.toolbar-divider {

&#x20; width: 1px;

&#x20; height: 1.25rem;

&#x20; background: var(--color-border);

&#x20; margin-inline: var(--space-1);

}



/\* Font family select \*/

.toolbar-select {

&#x20; height: 2rem;

&#x20; padding: 0 var(--space-2);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-surface);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-xs);

&#x20; cursor: pointer;

&#x20; outline: none;

}



/\* ─── Editor content area ─── \*/

.editor-content {

&#x20; min-height: 400px;

&#x20; padding: var(--space-6) var(--space-8);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: 0 0 var(--radius-xl) var(--radius-xl);

&#x20; background: var(--color-surface);

&#x20; outline: none;

&#x20; font-family: var(--font-sans);

&#x20; font-size: 1rem;

&#x20; line-height: 1.7;

&#x20; color: var(--color-text);

&#x20; caret-color: var(--color-accent);

}



.editor-content:focus { border-color: var(--color-accent); }



/\* Content styling \*/

.editor-content h1 { font-size: var(--step-3); font-weight: 800; line-height: 1.2; margin-block: 1.5em 0.5em; }

.editor-content h2 { font-size: var(--step-2); font-weight: 700; margin-block: 1.25em 0.5em; }

.editor-content h3 { font-size: var(--step-1); font-weight: 600; margin-block: 1em 0.5em; }

.editor-content p  { margin-block-end: 0.75em; }



.editor-content strong { font-weight: var(--font-weight-bold); }

.editor-content em     { font-style: italic; }

.editor-content u      { text-decoration: underline; }

.editor-content s      { text-decoration: line-through; }

.editor-content mark   { background: var(--color-warning-200); padding: 0 2px; border-radius: 2px; }

.editor-content sub    { vertical-align: sub; font-size: 0.75em; }

.editor-content sup    { vertical-align: super; font-size: 0.75em; }



.editor-content a {

&#x20; color: var(--color-accent);

&#x20; text-decoration: underline;

&#x20; text-underline-offset: 2px;

}



.editor-content ul, .editor-content ol { padding-inline-start: 1.5em; margin-block-end: 0.75em; }

.editor-content li + li { margin-block-start: 0.25em; }

.editor-content ul { list-style: disc; }

.editor-content ol { list-style: decimal; }



/\* Task list \*/

.editor-content ul\[data-type="taskList"] { list-style: none; padding: 0; }

.editor-content .task-item { display: flex; gap: var(--space-2); align-items: flex-start; }

.editor-content .task-item input\[type="checkbox"] { margin-block-start: 0.25em; }



.editor-content blockquote {

&#x20; border-inline-start: 3px solid var(--color-accent);

&#x20; padding-inline-start: var(--space-4);

&#x20; color: var(--color-text-muted);

&#x20; font-style: italic;

&#x20; margin-inline: 0;

&#x20; margin-block: 1em;

}



.editor-content pre {

&#x20; background: var(--color-neutral-900);

&#x20; color: var(--color-neutral-100);

&#x20; padding: var(--space-4);

&#x20; border-radius: var(--radius-lg);

&#x20; overflow-x: auto;

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.875em;

&#x20; margin-block: 1em;

}



.editor-content code { font-family: var(--font-mono); font-size: 0.875em; background: var(--color-bg-muted); padding: 0.125em 0.375em; border-radius: var(--radius-sm); }

.editor-content pre code { background: none; padding: 0; font-size: inherit; }



.editor-content hr { border: none; border-top: 1px solid var(--color-border); margin-block: 2em; }



.editor-content img { max-width: 100%; border-radius: var(--radius-lg); margin-block: 1em; }



.editor-content table { width: 100%; border-collapse: collapse; margin-block: 1em; }

.editor-content th, .editor-content td { border: 1px solid var(--color-border); padding: var(--space-2) var(--space-3); }

.editor-content th { background: var(--color-bg-subtle); font-weight: var(--font-weight-semibold); }



/\* Selection \*/

.editor-content ::selection { background: color-mix(in srgb, var(--color-accent) 25%, transparent); }



/\* Placeholder \*/

.editor-content:empty::before {

&#x20; content: attr(data-placeholder);

&#x20; color: var(--color-text-subtle);

&#x20; pointer-events: none;

}



/\* Collaboration cursor \*/

.collab-cursor {

&#x20; border-left: 2px solid var(--cursor-color, var(--color-accent));

&#x20; position: relative;

}

.collab-cursor::before {

&#x20; content: attr(data-user);

&#x20; position: absolute;

&#x20; top: -1.5rem;

&#x20; left: -2px;

&#x20; background: var(--cursor-color, var(--color-accent));

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; padding: 0.1em 0.4em;

&#x20; border-radius: var(--radius-sm);

&#x20; white-space: nowrap;

&#x20; pointer-events: none;

}



/\* Floating formatting toolbar \*/

.editor-bubble-menu {

&#x20; display: flex;

&#x20; gap: 2px;

&#x20; padding: var(--space-1) var(--space-2);

&#x20; background: var(--color-neutral-900);

&#x20; border-radius: var(--radius-lg);

&#x20; box-shadow: var(--shadow-xl);

&#x20; animation: bubble-appear 0.15s var(--ease-out);

}



@keyframes bubble-appear {

&#x20; from { opacity: 0; scale: 0.92; translate: 0 4px; }

}



.bubble-btn {

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; border: none;

&#x20; background: none;

&#x20; color: var(--color-neutral-300);

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: bold;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.bubble-btn:hover { background: var(--color-neutral-700); color: white; }

.bubble-btn.active { color: var(--color-brand-300); }

```



\---



\## 133. COLOR PICKER UI



```css

/\* ─── Full color picker ─── \*/

.color-picker {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-4);

&#x20; width: 240px;

&#x20; box-shadow: var(--shadow-xl);

}



/\* Saturation/lightness canvas \*/

.picker-canvas {

&#x20; width: 100%;

&#x20; aspect-ratio: 1.5;

&#x20; border-radius: var(--radius-lg);

&#x20; position: relative;

&#x20; overflow: hidden;

&#x20; cursor: crosshair;

&#x20; margin-block-end: var(--space-3);

&#x20; /\* Background set by JS: hsl(var(--h), 100%, 50%) \*/

}



/\* White gradient overlay \*/

.picker-canvas::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: linear-gradient(to right, white, transparent);

}



/\* Black gradient overlay \*/

.picker-canvas::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: linear-gradient(to bottom, transparent, black);

}



/\* Crosshair handle \*/

.picker-handle {

&#x20; position: absolute;

&#x20; width: 14px;

&#x20; height: 14px;

&#x20; border-radius: 50%;

&#x20; border: 2px solid white;

&#x20; box-shadow: 0 0 0 1px rgba(0 0 0 / 0.3), var(--shadow-sm);

&#x20; translate: -50% -50%;

&#x20; pointer-events: none;

&#x20; z-index: 2;

&#x20; left: var(--x, 50%);

&#x20; top: var(--y, 50%);

}



/\* Hue slider \*/

.picker-hue {

&#x20; width: 100%;

&#x20; height: 12px;

&#x20; border-radius: var(--radius-full);

&#x20; background: linear-gradient(to right,

&#x20;   hsl(0 100% 50%), hsl(30 100% 50%), hsl(60 100% 50%),

&#x20;   hsl(90 100% 50%), hsl(120 100% 50%), hsl(150 100% 50%),

&#x20;   hsl(180 100% 50%), hsl(210 100% 50%), hsl(240 100% 50%),

&#x20;   hsl(270 100% 50%), hsl(300 100% 50%), hsl(330 100% 50%), hsl(360 100% 50%)

&#x20; );

&#x20; position: relative;

&#x20; cursor: pointer;

&#x20; appearance: none;

&#x20; -webkit-appearance: none;

&#x20; border: none;

&#x20; outline: none;

&#x20; margin-block-end: var(--space-2);

}



.picker-hue::-webkit-slider-thumb {

&#x20; appearance: none;

&#x20; width: 16px;

&#x20; height: 16px;

&#x20; border-radius: 50%;

&#x20; background: white;

&#x20; border: 2px solid white;

&#x20; box-shadow: 0 0 0 1px rgba(0 0 0 / 0.2), var(--shadow-sm);

&#x20; cursor: pointer;

}



/\* Alpha slider \*/

.picker-alpha {

&#x20; width: 100%;

&#x20; height: 12px;

&#x20; border-radius: var(--radius-full);

&#x20; position: relative;

&#x20; margin-block-end: var(--space-3);

&#x20; background:

&#x20;   linear-gradient(to right, transparent, var(--current-color, #000)),

&#x20;   repeating-conic-gradient(#ccc 0% 25%, #fff 0% 50%) 0 0 / 12px 12px;

&#x20; border-radius: var(--radius-full);

&#x20; cursor: pointer;

}



/\* Color swatches \*/

.picker-swatches {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(8, 1fr);

&#x20; gap: var(--space-1);

&#x20; margin-block-end: var(--space-3);

}



.swatch {

&#x20; aspect-ratio: 1;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; border: 2px solid transparent;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce), border-color var(--duration-fast);

}

.swatch:hover { scale: 1.15; }

.swatch.selected { border-color: var(--color-text); }



/\* Hex input \*/

.picker-inputs {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 1fr 1fr 1fr;

&#x20; gap: var(--space-1);

}



.picker-input-group {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; gap: 2px;

}



.picker-value-input {

&#x20; width: 100%;

&#x20; padding: 0.25rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-sm);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-xs);

&#x20; font-family: var(--font-mono);

&#x20; text-align: center;

&#x20; outline: none;

&#x20; transition: border-color var(--duration-fast);

}

.picker-value-input:focus { border-color: var(--color-accent); }



.picker-label {

&#x20; font-size: 0.625rem;

&#x20; color: var(--color-text-subtle);

&#x20; text-transform: uppercase;

}



/\* Preview swatch \*/

.picker-preview {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; margin-block-end: var(--space-3);

}



.picker-preview-swatch {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: var(--radius-lg);

&#x20; border: 1px solid var(--color-border);

&#x20; background: var(--current-color, #000);

&#x20; flex-shrink: 0;

}



/\* Format toggle \*/

.picker-format {

&#x20; display: flex;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; overflow: hidden;

&#x20; width: fit-content;

&#x20; margin-block-end: var(--space-3);

}

.format-btn {

&#x20; padding: 0.2rem 0.5rem;

&#x20; font-size: var(--font-size-xs);

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; transition: background var(--duration-fast);

}

.format-btn.active { background: var(--color-accent); color: white; }

```



\---



\## 134. DASHBOARD WIDGET TYPES



```css

/\* ─── KPI / Metric card ─── \*/

.kpi-card {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-5);

&#x20; position: relative;

&#x20; overflow: hidden;

}



/\* Accent stripe \*/

.kpi-card::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-block: 0;

&#x20; inset-inline-start: 0;

&#x20; width: 4px;

&#x20; background: var(--kpi-color, var(--color-accent));

}



.kpi-card\_\_label {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-2);

}



.kpi-card\_\_value {

&#x20; font-size: clamp(1.5rem, 3vw, 2.5rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; line-height: 1;

&#x20; font-variant-numeric: tabular-nums;

&#x20; margin-block-end: var(--space-3);

}



.kpi-card\_\_trend {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-sm);

}



.trend-badge {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: 0.25em;

&#x20; padding: 0.2em 0.5em;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

}

.trend-badge--up   { background: var(--color-success-100); color: var(--color-success-700); }

.trend-badge--down { background: var(--color-danger-100);  color: var(--color-danger-700); }

.trend-badge--flat { background: var(--color-bg-muted);    color: var(--color-text-muted); }



/\* Mini sparkline in card \*/

.kpi-sparkline {

&#x20; position: absolute;

&#x20; inset-block-end: 0;

&#x20; inset-inline-end: 0;

&#x20; width: 80px;

&#x20; height: 40px;

&#x20; opacity: 0.15;

}



/\* ─── Gauge widget ─── \*/

.gauge-widget {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-5);

&#x20; text-align: center;

}



.gauge-svg {

&#x20; width: 160px;

&#x20; height: 90px;

&#x20; overflow: visible;

}



/\* SVG arc: cx=80, cy=80, r=60, startAngle=-180, endAngle=0 \*/

.gauge-bg {

&#x20; fill: none;

&#x20; stroke: var(--color-bg-muted);

&#x20; stroke-width: 12;

&#x20; stroke-dasharray: 188 1000; /\* semicircle \*/

&#x20; stroke-dashoffset: -94;

&#x20; stroke-linecap: round;

}



.gauge-fill {

&#x20; fill: none;

&#x20; stroke: var(--gauge-color, var(--color-accent));

&#x20; stroke-width: 12;

&#x20; stroke-dasharray: calc(var(--gauge-pct, 0) \* 1.88) 1000;

&#x20; stroke-dashoffset: -94;

&#x20; stroke-linecap: round;

&#x20; transition: stroke-dasharray 1s var(--ease-out);

}



.gauge-value {

&#x20; font-size: var(--step-2);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-variant-numeric: tabular-nums;

}



/\* ─── Activity heatmap widget ─── \*/

.activity-widget {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-5);

}



.activity-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(52, 1fr);

&#x20; gap: 2px;

&#x20; margin-block: var(--space-3);

}



.activity-cell {

&#x20; aspect-ratio: 1;

&#x20; border-radius: 2px;

&#x20; background: oklch(

&#x20;   from var(--color-accent)

&#x20;   l

&#x20;   calc(c \* var(--intensity, 0))

&#x20;   h

&#x20;   / calc(0.1 + var(--intensity, 0) \* 0.9)

&#x20; );

&#x20; cursor: pointer;

&#x20; position: relative;

}



.activity-cell:hover::after {

&#x20; content: attr(data-count) ' contributions\\A' attr(data-date);

&#x20; position: absolute;

&#x20; bottom: 120%;

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; font-size: 0.6875rem;

&#x20; padding: 0.25rem 0.5rem;

&#x20; border-radius: var(--radius-md);

&#x20; white-space: pre;

&#x20; pointer-events: none;

&#x20; z-index: 10;

&#x20; text-align: center;

&#x20; min-width: 120px;

}



/\* ─── Real-time ticker ─── \*/

.ticker-widget {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

}



.ticker-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-3) var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

}



.ticker-live {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-danger-500);

}



.ticker-live::before {

&#x20; content: '';

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-danger-500);

&#x20; animation: pulse 1.5s ease-in-out infinite;

}



@keyframes pulse {

&#x20; 0%, 100% { opacity: 1; scale: 1; }

&#x20; 50%       { opacity: 0.6; scale: 1.3; }

}



.ticker-row {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr auto auto;

&#x20; gap: var(--space-3);

&#x20; align-items: center;

&#x20; padding: var(--space-3) var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; transition: background var(--duration-fast);

&#x20; font-size: var(--font-size-sm);

}

.ticker-row:last-child { border: none; }

.ticker-row:hover { background: var(--color-bg-subtle); }



.ticker-symbol { font-weight: var(--font-weight-bold); font-family: var(--font-mono); }

.ticker-name   { font-size: var(--font-size-xs); color: var(--color-text-muted); }



.ticker-price {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-variant-numeric: tabular-nums;

&#x20; font-family: var(--font-mono);

}



.ticker-change {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-variant-numeric: tabular-nums;

&#x20; padding: 0.2em 0.5em;

&#x20; border-radius: var(--radius-sm);

}



.ticker-row.up   .ticker-change { background: var(--color-success-100); color: var(--color-success-700); }

.ticker-row.down .ticker-change { background: var(--color-danger-100);  color: var(--color-danger-700); }



/\* Flash on value change \*/

@keyframes flash-up   { from { background: var(--color-success-100); } }

@keyframes flash-down { from { background: var(--color-danger-100); } }



.ticker-row.flashing-up   { animation: flash-up 0.5s ease-out; }

.ticker-row.flashing-down { animation: flash-down 0.5s ease-out; }

```



\---



\## 135. STATUS INDICATORS



```css

/\* ─── Status dot ─── \*/

.status-dot {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: 0.5em;

&#x20; font-size: var(--font-size-sm);

}



.status-dot::before {

&#x20; content: '';

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; border-radius: 50%;

&#x20; flex-shrink: 0;

&#x20; background: var(--status-color, var(--color-neutral-400));

}



.status-dot.online   { --status-color: var(--color-success-500); }

.status-dot.offline  { --status-color: var(--color-neutral-400); }

.status-dot.busy     { --status-color: var(--color-danger-500); }

.status-dot.away     { --status-color: var(--color-warning-500); }

.status-dot.pending  { --status-color: var(--color-brand-500); }



/\* Animated online dot \*/

.status-dot.online::before {

&#x20; animation: status-pulse 2s ease-in-out infinite;

&#x20; box-shadow: 0 0 0 0 var(--color-success-300);

}



@keyframes status-pulse {

&#x20; 0%   { box-shadow: 0 0 0 0 color-mix(in srgb, var(--color-success-500) 50%, transparent); }

&#x20; 70%  { box-shadow: 0 0 0 6px transparent; }

&#x20; 100% { box-shadow: 0 0 0 0 transparent; }

}



/\* ─── Status badge (system) ─── \*/

.sys-status {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: var(--space-2) var(--space-4);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

}



.sys-status--operational { background: var(--color-success-100); color: var(--color-success-800); }

.sys-status--degraded    { background: var(--color-warning-100); color: var(--color-warning-800); }

.sys-status--outage      { background: var(--color-danger-100);  color: var(--color-danger-800); }

.sys-status--maintenance { background: var(--color-brand-100);   color: var(--color-brand-800); }



/\* ─── Status page component ─── \*/

.status-component {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-3) 0;

&#x20; border-bottom: 1px solid var(--color-border);

}

.status-component:last-child { border: none; }



.status-component\_\_name { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }

.status-component\_\_uptime { font-size: var(--font-size-xs); color: var(--color-text-muted); }



/\* 90-day bar \*/

.uptime-bar {

&#x20; display: flex;

&#x20; gap: 1px;

&#x20; height: 28px;

&#x20; align-items: flex-end;

}



.uptime-day {

&#x20; flex: 1;

&#x20; border-radius: 2px;

&#x20; cursor: pointer;

&#x20; transition: opacity var(--duration-fast);

&#x20; min-width: 2px;

}

.uptime-day:hover { opacity: 0.7; }



.uptime-day--up      { background: var(--color-success-500); height: 100%; }

.uptime-day--partial { background: var(--color-warning-500); height: 60%; }

.uptime-day--down    { background: var(--color-danger-500);  height: 100%; }

.uptime-day--no-data { background: var(--color-bg-muted);    height: 40%; }



/\* ─── Connection quality indicator ─── \*/

.signal-bars {

&#x20; display: flex;

&#x20; align-items: flex-end;

&#x20; gap: 2px;

&#x20; height: 1rem;

}



.signal-bar {

&#x20; width: 3px;

&#x20; border-radius: 1px;

&#x20; background: var(--color-bg-muted);

&#x20; transition: background var(--duration-fast);

}



.signal-bar:nth-child(1) { height: 30%; }

.signal-bar:nth-child(2) { height: 55%; }

.signal-bar:nth-child(3) { height: 80%; }

.signal-bar:nth-child(4) { height: 100%; }



/\* Active bars \*/

.signal-bars\[data-strength="1"] .signal-bar:nth-child(-n+1) { background: var(--color-danger-500); }

.signal-bars\[data-strength="2"] .signal-bar:nth-child(-n+2) { background: var(--color-warning-500); }

.signal-bars\[data-strength="3"] .signal-bar:nth-child(-n+3) { background: var(--color-success-500); }

.signal-bars\[data-strength="4"] .signal-bar:nth-child(-n+4) { background: var(--color-success-500); }

```



\---



\## 136. COMPLETE DARK MODE TOKEN SYSTEM



```css

/\* ─── Two-layer semantic token system ─── \*/



/\* ── Layer 1: Raw palette (never changes) ── \*/

:root {

&#x20; /\* Grays \*/

&#x20; --gray-0:   #ffffff;

&#x20; --gray-50:  #f9fafb;

&#x20; --gray-100: #f3f4f6;

&#x20; --gray-200: #e5e7eb;

&#x20; --gray-300: #d1d5db;

&#x20; --gray-400: #9ca3af;

&#x20; --gray-500: #6b7280;

&#x20; --gray-600: #4b5563;

&#x20; --gray-700: #374151;

&#x20; --gray-800: #1f2937;

&#x20; --gray-900: #111827;

&#x20; --gray-950: #030712;



&#x20; /\* Brand \*/

&#x20; --blue-100: #dbeafe; --blue-500: #3b82f6; --blue-600: #2563eb; --blue-900: #1e3a8a;

&#x20; --green-100: #dcfce7; --green-500: #22c55e; --green-600: #16a34a; --green-900: #14532d;

&#x20; --red-100: #fee2e2; --red-500: #ef4444; --red-600: #dc2626; --red-900: #7f1d1d;

&#x20; --yellow-100: #fef9c3; --yellow-500: #eab308; --yellow-900: #713f12;

&#x20; --purple-100: #f3e8ff; --purple-500: #a855f7; --purple-900: #3b0764;

}



/\* ── Layer 2: Semantic tokens (changes per theme) ── \*/



/\* Light theme \*/

:root,

\[data-theme="light"] {

&#x20; color-scheme: light;



&#x20; /\* Backgrounds \*/

&#x20; --bg-base:        var(--gray-0);

&#x20; --bg-subtle:      var(--gray-50);

&#x20; --bg-muted:       var(--gray-100);

&#x20; --bg-moderate:    var(--gray-200);



&#x20; /\* Surfaces \*/

&#x20; --surface-base:   var(--gray-0);

&#x20; --surface-raised: var(--gray-0);

&#x20; --surface-overlay:var(--gray-0);

&#x20; --surface-sunken: var(--gray-50);



&#x20; /\* Borders \*/

&#x20; --border-subtle:  var(--gray-100);

&#x20; --border-default: var(--gray-200);

&#x20; --border-strong:  var(--gray-300);

&#x20; --border-bolder:  var(--gray-400);



&#x20; /\* Text \*/

&#x20; --text-primary:   var(--gray-900);

&#x20; --text-secondary: var(--gray-600);

&#x20; --text-tertiary:  var(--gray-500);

&#x20; --text-disabled:  var(--gray-400);

&#x20; --text-inverse:   var(--gray-0);

&#x20; --text-on-accent: var(--gray-0);

&#x20; --text-link:      var(--blue-600);

&#x20; --text-link-hover:var(--blue-500);



&#x20; /\* Interactive \*/

&#x20; --interactive:        var(--blue-500);

&#x20; --interactive-hover:  var(--blue-600);

&#x20; --interactive-active: var(--blue-900);

&#x20; --interactive-subtle: var(--blue-100);

&#x20; --interactive-focus:  var(--blue-500);



&#x20; /\* Feedback \*/

&#x20; --success-bg:     var(--green-100);

&#x20; --success-border: #86efac;

&#x20; --success-text:   var(--green-900);

&#x20; --success-icon:   var(--green-500);



&#x20; --warning-bg:     var(--yellow-100);

&#x20; --warning-border: #fde047;

&#x20; --warning-text:   var(--yellow-900);

&#x20; --warning-icon:   var(--yellow-500);



&#x20; --danger-bg:      var(--red-100);

&#x20; --danger-border:  #fca5a5;

&#x20; --danger-text:    var(--red-900);

&#x20; --danger-icon:    var(--red-500);



&#x20; --info-bg:        var(--blue-100);

&#x20; --info-border:    #93c5fd;

&#x20; --info-text:      var(--blue-900);

&#x20; --info-icon:      var(--blue-500);



&#x20; /\* Shadows \*/

&#x20; --shadow-color:    0deg 0% 0%;

&#x20; --shadow-strength: 0.08;

&#x20; --shadow-xs: 0 1px 2px hsl(var(--shadow-color) / var(--shadow-strength));

&#x20; --shadow-sm: 0 1px 3px hsl(var(--shadow-color) / var(--shadow-strength)),

&#x20;              0 1px 2px hsl(var(--shadow-color) / calc(var(--shadow-strength) \* 0.6));

&#x20; --shadow-md: 0 4px 6px hsl(var(--shadow-color) / calc(var(--shadow-strength) \* 0.8)),

&#x20;              0 2px 4px hsl(var(--shadow-color) / calc(var(--shadow-strength) \* 0.5));

&#x20; --shadow-lg: 0 10px 15px hsl(var(--shadow-color) / calc(var(--shadow-strength) \* 0.8)),

&#x20;              0 4px 6px hsl(var(--shadow-color) / calc(var(--shadow-strength) \* 0.5));

&#x20; --shadow-xl: 0 20px 25px hsl(var(--shadow-color) / calc(var(--shadow-strength) \* 0.9)),

&#x20;              0 8px 10px hsl(var(--shadow-color) / calc(var(--shadow-strength) \* 0.5));

}



/\* Dark theme \*/

\[data-theme="dark"],

@media (prefers-color-scheme: dark) {

&#x20; :root:not(\[data-theme="light"]) {

&#x20;   color-scheme: dark;



&#x20;   --bg-base:        var(--gray-950);

&#x20;   --bg-subtle:      var(--gray-900);

&#x20;   --bg-muted:       var(--gray-800);

&#x20;   --bg-moderate:    var(--gray-700);



&#x20;   --surface-base:   var(--gray-900);

&#x20;   --surface-raised: var(--gray-800);

&#x20;   --surface-overlay:var(--gray-800);

&#x20;   --surface-sunken: var(--gray-950);



&#x20;   --border-subtle:  var(--gray-800);

&#x20;   --border-default: var(--gray-700);

&#x20;   --border-strong:  var(--gray-600);

&#x20;   --border-bolder:  var(--gray-500);



&#x20;   --text-primary:   var(--gray-50);

&#x20;   --text-secondary: var(--gray-400);

&#x20;   --text-tertiary:  var(--gray-500);

&#x20;   --text-disabled:  var(--gray-600);

&#x20;   --text-inverse:   var(--gray-950);

&#x20;   --text-link:      #60a5fa;

&#x20;   --text-link-hover:#93c5fd;



&#x20;   --interactive:        #60a5fa;

&#x20;   --interactive-hover:  #93c5fd;

&#x20;   --interactive-active: #dbeafe;

&#x20;   --interactive-subtle: rgba(59, 130, 246, 0.15);



&#x20;   --success-bg:     rgba(34, 197, 94, 0.1);

&#x20;   --success-border: rgba(34, 197, 94, 0.3);

&#x20;   --success-text:   #86efac;



&#x20;   --warning-bg:     rgba(234, 179, 8, 0.1);

&#x20;   --warning-border: rgba(234, 179, 8, 0.3);

&#x20;   --warning-text:   #fde047;



&#x20;   --danger-bg:      rgba(239, 68, 68, 0.1);

&#x20;   --danger-border:  rgba(239, 68, 68, 0.3);

&#x20;   --danger-text:    #fca5a5;



&#x20;   --info-bg:        rgba(59, 130, 246, 0.1);

&#x20;   --info-border:    rgba(59, 130, 246, 0.3);

&#x20;   --info-text:      #93c5fd;



&#x20;   --shadow-color:    0deg 0% 0%;

&#x20;   --shadow-strength: 0.4;

&#x20; }

}



/\* ── Apply tokens universally ── \*/

body {

&#x20; background: var(--bg-base);

&#x20; color: var(--text-primary);

}



/\* Token usage examples \*/

.card {

&#x20; background:   var(--surface-base);

&#x20; border:       1px solid var(--border-default);

&#x20; box-shadow:   var(--shadow-sm);

&#x20; color:        var(--text-primary);

}



.card\_\_description { color: var(--text-secondary); }

.card\_\_meta        { color: var(--text-tertiary); }



.alert--success {

&#x20; background: var(--success-bg);

&#x20; border:     1px solid var(--success-border);

&#x20; color:      var(--success-text);

}

.alert--warning { background: var(--warning-bg); border: 1px solid var(--warning-border); color: var(--warning-text); }

.alert--danger  { background: var(--danger-bg);  border: 1px solid var(--danger-border);  color: var(--danger-text); }

.alert--info    { background: var(--info-bg);    border: 1px solid var(--info-border);    color: var(--info-text); }

```



\---



\## 137. DIFF VIEWER



```css

/\* ─── Code diff / Git diff viewer ─── \*/

.diff-viewer {

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.8125rem;

&#x20; line-height: 1.6;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; background: var(--color-neutral-950, #0d1117);

&#x20; color: var(--color-neutral-200);

}



.diff-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-3) var(--space-4);

&#x20; background: rgba(255 255 255 / 0.04);

&#x20; border-bottom: 1px solid rgba(255 255 255 / 0.1);

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.5);

}



.diff-filename {

&#x20; color: rgba(255 255 255 / 0.8);

&#x20; font-weight: var(--font-weight-semibold);

}



.diff-stats {

&#x20; display: flex;

&#x20; gap: var(--space-3);

}



.diff-stat--add { color: #3fb950; }

.diff-stat--del { color: #f85149; }



/\* Diff body \*/

.diff-body { overflow-x: auto; }



.diff-table {

&#x20; width: 100%;

&#x20; border-collapse: collapse;

&#x20; min-width: max-content;

}



.diff-table td { padding: 0; white-space: pre; }



/\* Line numbers \*/

.diff-gutter-old,

.diff-gutter-new {

&#x20; min-width: 40px;

&#x20; padding: 0 var(--space-2);

&#x20; text-align: right;

&#x20; color: rgba(255 255 255 / 0.3);

&#x20; user-select: none;

&#x20; border-right: 1px solid rgba(255 255 255 / 0.08);

&#x20; vertical-align: top;

}



/\* Code content \*/

.diff-code {

&#x20; padding: 0 var(--space-3);

&#x20; width: 100%;

&#x20; white-space: pre-wrap;

&#x20; word-break: break-all;

}



/\* Line types \*/

.diff-line--add {

&#x20; background: rgba(63, 185, 80, 0.1);

}

.diff-line--add .diff-gutter-new { color: rgba(63, 185, 80, 0.6); }

.diff-line--add .diff-code::before {

&#x20; content: '+';

&#x20; color: #3fb950;

&#x20; margin-inline-end: 0.5em;

}



.diff-line--del {

&#x20; background: rgba(248, 81, 73, 0.1);

}

.diff-line--del .diff-gutter-old { color: rgba(248, 81, 73, 0.6); }

.diff-line--del .diff-code::before {

&#x20; content: '-';

&#x20; color: #f85149;

&#x20; margin-inline-end: 0.5em;

}



.diff-line--context .diff-code::before {

&#x20; content: ' ';

&#x20; margin-inline-end: 0.5em;

}



/\* Hunk header \*/

.diff-hunk {

&#x20; background: rgba(58, 130, 246, 0.05);

&#x20; border-block: 1px solid rgba(58, 130, 246, 0.15);

&#x20; color: rgba(58, 130, 246, 0.8);

&#x20; font-style: italic;

&#x20; padding: 0.25rem var(--space-4);

&#x20; font-size: var(--font-size-xs);

}



/\* Char-level highlighting \*/

.diff-char-add { background: rgba(63, 185, 80, 0.4); border-radius: 2px; }

.diff-char-del { background: rgba(248, 81, 73, 0.4); border-radius: 2px; }



/\* Unified vs split toggle \*/

.diff-viewer--split .diff-table {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 1fr;

}



/\* Collapse unchanged \*/

.diff-collapse-btn {

&#x20; width: 100%;

&#x20; padding: var(--space-1) var(--space-4);

&#x20; background: rgba(255 255 255 / 0.03);

&#x20; border: none;

&#x20; border-block: 1px solid rgba(255 255 255 / 0.08);

&#x20; color: rgba(255 255 255 / 0.4);

&#x20; font-size: var(--font-size-xs);

&#x20; font-family: var(--font-mono);

&#x20; cursor: pointer;

&#x20; text-align: start;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.diff-collapse-btn:hover { background: rgba(255 255 255 / 0.06); color: rgba(255 255 255 / 0.7); }

```



\---



\## 138. SEARCH RESULTS PAGE



```css

/\* ─── Search results layout ─── \*/

.search-page {

&#x20; display: grid;

&#x20; grid-template-columns: 220px 1fr;

&#x20; gap: var(--space-8);

&#x20; max-width: 1100px;

&#x20; margin-inline: auto;

&#x20; padding: var(--space-6) var(--space-4);

}



@media (max-width: 768px) {

&#x20; .search-page { grid-template-columns: 1fr; }

&#x20; .search-filters { display: none; }

}



/\* Filter sidebar \*/

.search-filters { }



.filter-group {

&#x20; margin-block-end: var(--space-6);

&#x20; padding-block-end: var(--space-6);

&#x20; border-bottom: 1px solid var(--color-border);

}

.filter-group:last-child { border: none; }



.filter-title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; margin-block-end: var(--space-3);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; cursor: pointer;

}



.filter-options {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

}



.filter-option {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-sm);

&#x20; cursor: pointer;

&#x20; padding: 0.25rem 0;

&#x20; border-radius: var(--radius-md);

&#x20; transition: color var(--duration-fast);

}

.filter-option:hover { color: var(--color-accent); }



.filter-count {

&#x20; margin-inline-start: auto;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-variant-numeric: tabular-nums;

}



/\* Active filter tags \*/

.active-filters {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-2);

&#x20; margin-block-end: var(--space-4);

}



.filter-tag {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.25rem 0.75rem;

&#x20; background: var(--color-brand-100);

&#x20; color: var(--color-brand-700);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

}



.filter-tag\_\_remove {

&#x20; border: none;

&#x20; background: none;

&#x20; color: inherit;

&#x20; cursor: pointer;

&#x20; padding: 0;

&#x20; display: flex;

&#x20; opacity: 0.6;

&#x20; transition: opacity var(--duration-fast);

}

.filter-tag\_\_remove:hover { opacity: 1; }



/\* Search results \*/

.search-results { }



.results-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; margin-block-end: var(--space-4);

&#x20; gap: var(--space-4);

&#x20; flex-wrap: wrap;

}



.results-count {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

}

.results-count strong { color: var(--color-text); font-weight: var(--font-weight-semibold); }



.results-sort {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-sm);

}



/\* Result item \*/

.search-result {

&#x20; padding: var(--space-4) 0;

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; animation: result-in 0.2s var(--ease-out) backwards;

&#x20; animation-delay: calc(var(--i, 0) \* 40ms);

}



@keyframes result-in {

&#x20; from { opacity: 0; translate: 0 8px; }

}



.search-result:last-child { border: none; }



.result-url {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-success-600);

&#x20; margin-block-end: var(--space-1);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

}



.result-favicon {

&#x20; width: 14px;

&#x20; height: 14px;

&#x20; border-radius: 2px;

&#x20; object-fit: contain;

}



.result-title {

&#x20; font-size: var(--font-size-lg);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: var(--color-accent);

&#x20; text-decoration: none;

&#x20; line-height: 1.4;

&#x20; margin-block-end: var(--space-2);

&#x20; display: block;

}

.result-title:hover { text-decoration: underline; }



/\* Highlight search terms \*/

.result-title mark,

.result-snippet mark {

&#x20; background: none;

&#x20; color: inherit;

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-decoration: underline;

&#x20; text-decoration-color: var(--color-warning-400);

&#x20; text-underline-offset: 2px;

}



.result-snippet {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

&#x20; overflow: hidden;

&#x20; display: -webkit-box;

&#x20; -webkit-line-clamp: 2;

&#x20; -webkit-box-orient: vertical;

&#x20; margin-block-end: var(--space-2);

}



.result-meta {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-subtle);

}



/\* Sitelinks \*/

.result-sitelinks {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 1fr;

&#x20; gap: var(--space-2);

&#x20; margin-block-start: var(--space-3);

}



.sitelink {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: 2px;

&#x20; padding: var(--space-2);

&#x20; border-radius: var(--radius-md);

&#x20; text-decoration: none;

&#x20; transition: background var(--duration-fast);

}

.sitelink:hover { background: var(--color-bg-subtle); }



.sitelink\_\_title  { font-size: var(--font-size-sm); color: var(--color-accent); font-weight: var(--font-weight-medium); }

.sitelink\_\_desc   { font-size: var(--font-size-xs); color: var(--color-text-muted); }



/\* Knowledge panel \*/

.knowledge-panel {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-5);

&#x20; margin-block-end: var(--space-6);

}



.knowledge-panel\_\_image {

&#x20; width: 100%;

&#x20; aspect-ratio: 16/9;

&#x20; object-fit: cover;

&#x20; border-radius: var(--radius-lg);

&#x20; margin-block-end: var(--space-4);

}



.knowledge-panel\_\_title {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: var(--space-1);

}



.knowledge-panel\_\_subtitle {

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; margin-block-end: var(--space-3);

}



.knowledge-panel\_\_desc {

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.6;

&#x20; margin-block-end: var(--space-4);

}



.knowledge-panel\_\_attrs {

&#x20; display: grid;

&#x20; grid-template-columns: auto 1fr;

&#x20; gap: var(--space-1) var(--space-4);

&#x20; font-size: var(--font-size-sm);

}



.knowledge-attr-key { color: var(--color-text-muted); }

.knowledge-attr-val a { color: var(--color-accent); text-decoration: none; }

.knowledge-attr-val a:hover { text-decoration: underline; }



/\* Pagination \*/

.results-pagination {

&#x20; display: flex;

&#x20; justify-content: center;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; padding-block: var(--space-8);

}

```



\---



\## 139. ADVANCED TEXT EFFECTS



```css

/\* ─── Animated gradient text ─── \*/

@keyframes gradient-flow {

&#x20; 0%   { background-position: 0% 50%; }

&#x20; 50%  { background-position: 100% 50%; }

&#x20; 100% { background-position: 0% 50%; }

}



.text-gradient-animated {

&#x20; background: linear-gradient(

&#x20;   270deg,

&#x20;   oklch(0.7 0.25 0),

&#x20;   oklch(0.7 0.25 120),

&#x20;   oklch(0.7 0.25 240),

&#x20;   oklch(0.7 0.25 0)

&#x20; );

&#x20; background-size: 400% 400%;

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

&#x20; animation: gradient-flow 4s ease infinite;

}



/\* ─── Text reveal (mask wipe) ─── \*/

.text-mask-reveal {

&#x20; background: linear-gradient(

&#x20;   to right,

&#x20;   var(--color-text) 50%,

&#x20;   transparent 50%

&#x20; );

&#x20; background-size: 200% 100%;

&#x20; background-position: 100%;

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

&#x20; transition: background-position 0.5s var(--ease-out);

}

.text-mask-reveal:hover { background-position: 0%; }



/\* ─── Outline to fill text ─── \*/

.text-outline-fill {

&#x20; color: transparent;

&#x20; -webkit-text-stroke: 2px var(--color-accent);

&#x20; transition:

&#x20;   color                var(--duration-slow) var(--ease-out),

&#x20;   -webkit-text-stroke  var(--duration-slow);

}

.text-outline-fill:hover {

&#x20; color: var(--color-accent);

&#x20; -webkit-text-stroke: 0px transparent;

}



/\* ─── Flickering neon ─── \*/

@keyframes neon-flicker {

&#x20; 0%,19%,21%,23%,25%,54%,56%,100% {

&#x20;   text-shadow:

&#x20;     0 0 4px #fff,

&#x20;     0 0 10px #fff,

&#x20;     0 0 18px var(--color-accent),

&#x20;     0 0 38px var(--color-accent),

&#x20;     0 0 73px var(--color-accent);

&#x20;   opacity: 1;

&#x20; }

&#x20; 20%,24%,55% {

&#x20;   text-shadow: none;

&#x20;   opacity: 0.5;

&#x20; }

}



.text-neon {

&#x20; color: white;

&#x20; animation: neon-flicker 5s infinite;

}



/\* ─── Blurry emergence ─── \*/

@keyframes blur-emerge {

&#x20; from { filter: blur(12px); opacity: 0; letter-spacing: 0.5em; }

&#x20; to   { filter: blur(0);    opacity: 1; letter-spacing: normal; }

}

.text-blur-in { animation: blur-emerge 1s var(--ease-out) forwards; }



/\* ─── Wave text (letter by letter) ─── \*/

.text-wave span {

&#x20; display: inline-block;

&#x20; animation: wave-letter 1.5s ease-in-out infinite;

&#x20; animation-delay: calc(var(--i, 0) \* 0.08s);

}



@keyframes wave-letter {

&#x20; 0%, 60%, 100% { translate: 0 0; }

&#x20; 30%           { translate: 0 -0.5em; }

}



/\* ─── Scramble/glitch reveal ─── \*/

/\* Achieved purely via JS + CSS class \*/

.text-scramble {

&#x20; display: inline-block;

&#x20; font-family: var(--font-mono);

}

.text-scramble.scrambling {

&#x20; animation: scramble-jitter 0.05s linear infinite;

}

@keyframes scramble-jitter {

&#x20; 0%,100% { translate: 0 0; }

&#x20; 25%     { translate: -1px 0; }

&#x20; 75%     { translate: 1px 0; }

}



/\* ─── Stamp effect ─── \*/

@keyframes stamp-in {

&#x20; 0%   { scale: 4; opacity: 0; }

&#x20; 60%  { scale: 0.9; opacity: 0.8; }

&#x20; 80%  { scale: 1.05; }

&#x20; 100% { scale: 1; opacity: 1; }

}

.text-stamp { animation: stamp-in 0.5s var(--ease-out) forwards; }



/\* ─── Text shadow depth ─── \*/

.text-depth {

&#x20; --depth: 6;

&#x20; text-shadow:

&#x20;   1px 1px 0 hsl(0 0% 60%),

&#x20;   2px 2px 0 hsl(0 0% 55%),

&#x20;   3px 3px 0 hsl(0 0% 50%),

&#x20;   4px 4px 0 hsl(0 0% 45%),

&#x20;   5px 5px 0 hsl(0 0% 40%),

&#x20;   6px 6px 8px hsl(0 0% 0% / 0.3);

}



/\* ─── Kinetic typography container ─── \*/

.kinetic-text {

&#x20; font-size: clamp(2rem, 8vw, 6rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; line-height: 1;

&#x20; overflow: hidden;

}



.kinetic-line {

&#x20; display: block;

&#x20; overflow: hidden;

}



.kinetic-word {

&#x20; display: inline-block;

&#x20; translate: 0 110%;

&#x20; animation: kinetic-in 0.7s var(--ease-out) forwards;

&#x20; animation-delay: calc(var(--w, 0) \* 0.1s);

}



@keyframes kinetic-in {

&#x20; to { translate: 0 0; }

}

```



\---



\## 140. MODAL STACK \& OVERLAY SYSTEM



```css

/\* ─── Layered modal system ─── \*/

:root {

&#x20; --modal-base-z: 50;

}



/\* Overlay manager — each modal increments z-index \*/

.modal-stack {

&#x20; isolation: isolate;

}



/\* Individual modal \*/

.modal {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; z-index: calc(var(--modal-base-z) + var(--stack-index, 0) \* 10);

&#x20; display: grid;

&#x20; place-items: center;

&#x20; padding: var(--space-4);

&#x20; pointer-events: none;

}



.modal.open { pointer-events: auto; }



/\* Backdrop per modal \*/

.modal\_\_backdrop {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; background: rgb(0 0 0 / calc(0.3 + var(--stack-index, 0) \* 0.05));

&#x20; backdrop-filter: blur(calc(2px + var(--stack-index, 0) \* 1px));

&#x20; animation: backdrop-in var(--duration-normal) var(--ease-out);

}



@keyframes backdrop-in  { from { opacity: 0; } }

@keyframes backdrop-out { to   { opacity: 0; } }



.modal.closing .modal\_\_backdrop { animation: backdrop-out var(--duration-fast) var(--ease-in) forwards; }



/\* Dialog box \*/

.modal\_\_dialog {

&#x20; position: relative;

&#x20; background: var(--color-surface);

&#x20; border-radius: var(--radius-2xl);

&#x20; box-shadow: var(--shadow-2xl);

&#x20; width: 100%;

&#x20; max-width: var(--modal-width, 560px);

&#x20; max-height: calc(100dvh - var(--space-8));

&#x20; overflow: hidden;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; animation: modal-in var(--duration-normal) var(--spring-bouncy);

&#x20; z-index: 1;

}



@keyframes modal-in {

&#x20; from { opacity: 0; scale: 0.93; translate: 0 12px; }

}



.modal.closing .modal\_\_dialog {

&#x20; animation: modal-out var(--duration-fast) var(--ease-in) forwards;

}



@keyframes modal-out {

&#x20; to { opacity: 0; scale: 0.96; translate: 0 8px; }

}



/\* Stacked modal offset \*/

.modal\[style\*="--stack-index: 1"] .modal\_\_dialog {

&#x20; scale: 0.98;

&#x20; translate: 0 -10px;

}

.modal\[style\*="--stack-index: 2"] .modal\_\_dialog {

&#x20; scale: 0.96;

&#x20; translate: 0 -20px;

}



/\* Mobile sheet variant \*/

@media (max-width: 640px) {

&#x20; .modal--sheet {

&#x20;   align-items: flex-end;

&#x20;   padding: 0;

&#x20; }

&#x20; .modal--sheet .modal\_\_dialog {

&#x20;   border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;

&#x20;   max-width: 100%;

&#x20;   max-height: 90dvh;

&#x20;   animation: sheet-in var(--duration-normal) var(--ease-out);

&#x20; }

&#x20; @keyframes sheet-in {

&#x20;   from { translate: 0 100%; }

&#x20; }

}



/\* Fullscreen modal \*/

.modal--fullscreen .modal\_\_dialog {

&#x20; max-width: 100%;

&#x20; max-height: 100%;

&#x20; border-radius: 0;

&#x20; height: 100dvh;

&#x20; animation: none;

}



/\* Focus trap visual \*/

.modal:not(.open) { display: none; }



/\* Scrollable body \*/

.modal\_\_body {

&#x20; flex: 1;

&#x20; overflow-y: auto;

&#x20; overscroll-behavior: contain;

}



/\* Confirm dialog variant \*/

.modal--confirm .modal\_\_dialog { max-width: 400px; }

.modal--confirm .modal\_\_body {

&#x20; padding: var(--space-6);

&#x20; text-align: center;

}

.modal--confirm .confirm-icon {

&#x20; font-size: 3rem;

&#x20; margin-block-end: var(--space-4);

}

.modal--confirm .confirm-title {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: var(--space-2);

}

.modal--confirm .confirm-desc {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

}

.modal--confirm .confirm-actions {

&#x20; display: flex;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-4) var(--space-6);

&#x20; border-top: 1px solid var(--color-border);

}

.modal--confirm .confirm-actions .btn { flex: 1; }

```



\---



\## 141. SCROLLING PATTERNS



```css

/\* ─── Smooth momentum scroll ─── \*/

.smooth-scroll {

&#x20; overflow-y: auto;

&#x20; -webkit-overflow-scrolling: touch;

&#x20; overscroll-behavior-y: contain;

&#x20; scroll-behavior: smooth;

}



/\* ─── Virtual scroll container ─── \*/

.virtual-list {

&#x20; height: 400px;

&#x20; overflow-y: auto;

&#x20; position: relative;

&#x20; contain: strict;

}



.virtual-list\_\_inner {

&#x20; position: relative;

&#x20; height: var(--total-height, 0);

}



.virtual-list\_\_item {

&#x20; position: absolute;

&#x20; top: var(--item-top, 0);

&#x20; left: 0;

&#x20; right: 0;

&#x20; height: var(--item-height, 48px);

&#x20; contain: layout style;

}



/\* ─── Horizontal scroll with snap ─── \*/

.h-scroll {

&#x20; display: flex;

&#x20; overflow-x: auto;

&#x20; scroll-snap-type: x mandatory;

&#x20; scroll-padding-inline: var(--space-4);

&#x20; padding-inline: var(--space-4);

&#x20; gap: var(--space-4);

&#x20; scrollbar-width: none;

&#x20; padding-block: var(--space-2);

&#x20; -webkit-overflow-scrolling: touch;

}

.h-scroll::-webkit-scrollbar { display: none; }

.h-scroll > \* { scroll-snap-align: start; flex-shrink: 0; }



/\* ─── Infinite scroll loading indicator ─── \*/

.infinite-scroll-sentinel {

&#x20; height: 2px;

&#x20; visibility: hidden;

}



.infinite-scroll-loader {

&#x20; display: flex;

&#x20; justify-content: center;

&#x20; padding: var(--space-8);

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-normal);

}

.infinite-scroll-loader.visible { opacity: 1; }



/\* ─── Scroll fade edges ─── \*/

.scroll-fade {

&#x20; position: relative;

&#x20; overflow: hidden;

}



.scroll-fade::before,

.scroll-fade::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; z-index: 1;

&#x20; pointer-events: none;

}



/\* Horizontal fades \*/

.scroll-fade--x::before {

&#x20; inset-block: 0;

&#x20; inset-inline-start: 0;

&#x20; width: 2rem;

&#x20; background: linear-gradient(to right, var(--color-surface), transparent);

}

.scroll-fade--x::after {

&#x20; inset-block: 0;

&#x20; inset-inline-end: 0;

&#x20; width: 2rem;

&#x20; background: linear-gradient(to left, var(--color-surface), transparent);

}



/\* Vertical fades \*/

.scroll-fade--y::before {

&#x20; inset-inline: 0;

&#x20; inset-block-start: 0;

&#x20; height: 2rem;

&#x20; background: linear-gradient(to bottom, var(--color-surface), transparent);

}

.scroll-fade--y::after {

&#x20; inset-inline: 0;

&#x20; inset-block-end: 0;

&#x20; height: 2rem;

&#x20; background: linear-gradient(to top, var(--color-surface), transparent);

}



/\* ─── Scroll to top button ─── \*/

.scroll-top-btn {

&#x20; position: fixed;

&#x20; inset-block-end: var(--space-6);

&#x20; inset-inline-end: var(--space-6);

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: 50%;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-text-muted);

&#x20; box-shadow: var(--shadow-md);

&#x20; z-index: var(--z-fixed);

&#x20; opacity: 0;

&#x20; translate: 0 1rem;

&#x20; transition:

&#x20;   opacity   var(--duration-normal),

&#x20;   translate var(--duration-normal) var(--ease-bounce);

&#x20; pointer-events: none;

}



.scroll-top-btn.visible {

&#x20; opacity: 1;

&#x20; translate: 0 0;

&#x20; pointer-events: auto;

}



.scroll-top-btn:hover {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border-color: var(--color-accent);

&#x20; scale: 1.1;

}

```



\---



```

╔══════════════════════════════════════════════════════════════════════╗

║              CSS MASTER GUIDE — PARTS I–VIII                         ║

╠══════════════════════════════════════════════════════════════════════╣

║  141 chapters · 800+ code examples · \~28,000 lines                  ║

║                                                                      ║

║  NEW IN PART VIII:                                                   ║

║  ✅ Full calendar month view (events, week/month, hover)             ║

║  ✅ Spreadsheet UI (formula bar, resize, freeze, cell edit)          ║

║  ✅ Rich text editor (toolbar, content styles, bubble menu)          ║

║  ✅ Color picker (canvas, hue, alpha, swatches, hex input)           ║

║  ✅ Dashboard widgets (KPI, gauge, heatmap, ticker)                  ║

║  ✅ Status indicators (dot, system, uptime bar, signal bars)         ║

║  ✅ Complete dark mode token system (2-layer, all themes)            ║

║  ✅ Diff viewer (git diff, char-level, unified/split)                ║

║  ✅ Search results page (filters, knowledge panel, sitelinks)        ║

║  ✅ Advanced text effects (10 patterns: wave, stamp, kinetic etc.)   ║

║  ✅ Modal stack system (layered z-index, sheet, fullscreen)          ║

║  ✅ Scrolling patterns (virtual list, h-scroll, fade edges)          ║

╚══════════════════════════════════════════════════════════════════════╝

