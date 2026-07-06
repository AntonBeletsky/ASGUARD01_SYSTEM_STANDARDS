# PART VIII — CSS: FINAL FRONTIER PATTERNS

---

## 130. FULL CALENDAR / MONTH VIEW

```css
/* ─── Calendar month view ─── */
.calendar {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  user-select: none;
}

/* Header */
.calendar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
}

.calendar__month-year {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-base);
}

.calendar__nav {
  display: flex;
  gap: var(--space-1);
}

.cal-nav-btn {
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.cal-nav-btn:hover { background: var(--color-bg-muted); color: var(--color-text); }

/* View switcher */
.calendar__views {
  display: flex;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}
.cal-view-btn {
  padding: 0.25rem 0.75rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.cal-view-btn.active {
  background: var(--color-accent);
  color: white;
}

/* Weekday header row */
.calendar__weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  border-bottom: 1px solid var(--color-border);
}

.calendar__weekday {
  padding: var(--space-2);
  text-align: center;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  color: var(--color-text-muted);
}

/* Days grid */
.calendar__grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-auto-rows: minmax(80px, auto);
}

.calendar__cell {
  border-right: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-2);
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-height: 80px;
  cursor: pointer;
  transition: background var(--duration-fast);
  position: relative;
  overflow: hidden;
}

.calendar__cell:nth-child(7n) { border-right: none; }
.calendar__cell:hover { background: var(--color-bg-subtle); }
.calendar__cell:focus-visible { outline: 2px solid var(--color-accent); outline-offset: -2px; }

/* Day number */
.cal-day-num {
  width: 1.75rem;
  height: 1.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  border-radius: 50%;
  align-self: flex-start;
  font-variant-numeric: tabular-nums;
  flex-shrink: 0;
}

/* Today */
.calendar__cell--today .cal-day-num {
  background: var(--color-accent);
  color: white;
  font-weight: var(--font-weight-bold);
}

/* Selected */
.calendar__cell--selected {
  background: color-mix(in srgb, var(--color-accent) 8%, transparent);
}
.calendar__cell--selected .cal-day-num {
  background: var(--color-accent);
  color: white;
}

/* Outside month */
.calendar__cell--outside {
  background: var(--color-bg-subtle);
  opacity: 0.5;
}

/* Weekend */
.calendar__cell--weekend .cal-day-num { color: var(--color-text-muted); }

/* Events */
.cal-event {
  border-radius: 3px;
  padding: 1px 6px;
  font-size: 0.6875rem;
  font-weight: var(--font-weight-medium);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
  transition: filter var(--duration-fast);
}
.cal-event:hover { filter: brightness(0.9); }

.cal-event--blue    { background: var(--color-brand-100); color: var(--color-brand-800); }
.cal-event--green   { background: var(--color-success-100); color: var(--color-success-800); }
.cal-event--red     { background: var(--color-danger-100); color: var(--color-danger-800); }
.cal-event--yellow  { background: var(--color-warning-100); color: var(--color-warning-800); }
.cal-event--purple  { background: oklch(0.93 0.05 300); color: oklch(0.35 0.15 300); }

/* All-day / multi-day events */
.cal-event--multi {
  border-radius: 0;
  margin-inline: -var(--space-2);
  padding-inline: var(--space-2);
}
.cal-event--start { border-radius: 3px 0 0 3px; }
.cal-event--end   { border-radius: 0 3px 3px 0; }

/* More events indicator */
.cal-more {
  font-size: 0.6875rem;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 1px 4px;
  border-radius: 3px;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.cal-more:hover { background: var(--color-bg-muted); color: var(--color-text); }

/* Week view */
.calendar--week .calendar__grid {
  grid-template-columns: 50px repeat(7, 1fr);
  grid-auto-rows: 48px;
}

.calendar__time-col { font-size: 0.6875rem; color: var(--color-text-subtle); padding-inline-end: var(--space-2); text-align: right; padding-block-start: var(--space-1); }
```

---

## 131. SPREADSHEET-LIKE UI

```css
/* ─── Data grid / spreadsheet ─── */
.spreadsheet {
  display: grid;
  overflow: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
  position: relative;
}

.spreadsheet-table {
  border-collapse: collapse;
  width: max-content;
  min-width: 100%;
}

/* Corner cell */
.spreadsheet-corner {
  position: sticky;
  top: 0;
  left: 0;
  z-index: 4;
  width: 40px;
  background: var(--color-bg-muted);
  border-right: 2px solid var(--color-border);
  border-bottom: 2px solid var(--color-border);
}

/* Column headers */
.spreadsheet-table thead th {
  position: sticky;
  top: 0;
  z-index: 3;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  padding: 0.375rem 0.5rem;
  text-align: center;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  min-width: 100px;
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
  transition: background var(--duration-fast);
}

.spreadsheet-table thead th:hover { background: var(--color-bg-muted); }
.spreadsheet-table thead th.selected { background: color-mix(in srgb, var(--color-accent) 20%, var(--color-bg-subtle)); }

/* Row headers */
.spreadsheet-table tbody td:first-child {
  position: sticky;
  left: 0;
  z-index: 2;
  background: var(--color-bg-subtle);
  border-right: 2px solid var(--color-border);
  padding: 0.25rem 0.5rem;
  text-align: center;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  min-width: 40px;
  cursor: pointer;
  transition: background var(--duration-fast);
}

.spreadsheet-table tbody td:first-child:hover { background: var(--color-bg-muted); }

/* Data cells */
.spreadsheet-cell {
  border: 1px solid var(--color-border);
  padding: 0.25rem 0.5rem;
  height: 28px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: cell;
  position: relative;
  transition: background var(--duration-fast);
  max-width: 200px;
}

.spreadsheet-cell:hover { background: color-mix(in srgb, var(--color-accent) 4%, var(--color-surface)); }

/* Selected cell */
.spreadsheet-cell.selected {
  background: color-mix(in srgb, var(--color-accent) 8%, var(--color-surface));
  outline: 2px solid var(--color-accent);
  outline-offset: -2px;
  z-index: 1;
}

/* Editing cell */
.spreadsheet-cell.editing {
  padding: 0;
  overflow: visible;
  z-index: 5;
}

.cell-input {
  position: absolute;
  inset: -1px;
  border: 2px solid var(--color-accent);
  border-radius: 2px;
  padding: 0.25rem 0.5rem;
  font: inherit;
  font-size: var(--font-size-sm);
  background: var(--color-surface);
  outline: none;
  z-index: 10;
  min-width: 100px;
  box-shadow: var(--shadow-lg);
}

/* Range selection */
.spreadsheet-cell.in-range {
  background: color-mix(in srgb, var(--color-accent) 12%, var(--color-surface));
}

/* Cell types */
.cell-number { text-align: end; font-variant-numeric: tabular-nums; }
.cell-formula { color: var(--color-brand-700); }
.cell-error   { color: var(--color-danger-500); font-weight: var(--font-weight-semibold); }
.cell-boolean { text-align: center; font-weight: var(--font-weight-semibold); }

/* Freeze indicator */
.spreadsheet-table thead th.frozen::after,
.spreadsheet-table tbody td.frozen::after {
  content: '';
  position: absolute;
  right: -2px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--color-accent);
  opacity: 0.5;
}

/* Column resize handle */
.col-resize {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  cursor: col-resize;
  z-index: 1;
}
.col-resize:hover { background: var(--color-accent); opacity: 0.7; }

/* Formula bar */
.formula-bar {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.25rem var(--space-3);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

.formula-bar__cell-ref {
  min-width: 60px;
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font: inherit;
  text-align: center;
  outline: none;
}

.formula-bar__input {
  flex: 1;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 0.25rem 0.5rem;
  font: inherit;
  outline: none;
  transition: border-color var(--duration-fast);
}
.formula-bar__input:focus { border-color: var(--color-accent); }

.formula-bar__fx {
  color: var(--color-brand-700);
  font-weight: var(--font-weight-bold);
  font-style: italic;
}
```

---

## 132. RICH TEXT EDITOR STYLING

```css
/* ─── Editor toolbar ─── */
.editor-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-bottom: none;
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
}

.toolbar-btn {
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.toolbar-btn:hover { background: var(--color-bg-muted); color: var(--color-text); }
.toolbar-btn.active {
  background: color-mix(in srgb, var(--color-accent) 15%, transparent);
  color: var(--color-accent);
}
.toolbar-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.toolbar-divider {
  width: 1px;
  height: 1.25rem;
  background: var(--color-border);
  margin-inline: var(--space-1);
}

/* Font family select */
.toolbar-select {
  height: 2rem;
  padding: 0 var(--space-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  font: inherit;
  font-size: var(--font-size-xs);
  cursor: pointer;
  outline: none;
}

/* ─── Editor content area ─── */
.editor-content {
  min-height: 400px;
  padding: var(--space-6) var(--space-8);
  border: 1px solid var(--color-border);
  border-radius: 0 0 var(--radius-xl) var(--radius-xl);
  background: var(--color-surface);
  outline: none;
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--color-text);
  caret-color: var(--color-accent);
}

.editor-content:focus { border-color: var(--color-accent); }

/* Content styling */
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
  color: var(--color-accent);
  text-decoration: underline;
  text-underline-offset: 2px;
}

.editor-content ul, .editor-content ol { padding-inline-start: 1.5em; margin-block-end: 0.75em; }
.editor-content li + li { margin-block-start: 0.25em; }
.editor-content ul { list-style: disc; }
.editor-content ol { list-style: decimal; }

/* Task list */
.editor-content ul[data-type="taskList"] { list-style: none; padding: 0; }
.editor-content .task-item { display: flex; gap: var(--space-2); align-items: flex-start; }
.editor-content .task-item input[type="checkbox"] { margin-block-start: 0.25em; }

.editor-content blockquote {
  border-inline-start: 3px solid var(--color-accent);
  padding-inline-start: var(--space-4);
  color: var(--color-text-muted);
  font-style: italic;
  margin-inline: 0;
  margin-block: 1em;
}

.editor-content pre {
  background: var(--color-neutral-900);
  color: var(--color-neutral-100);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 0.875em;
  margin-block: 1em;
}

.editor-content code { font-family: var(--font-mono); font-size: 0.875em; background: var(--color-bg-muted); padding: 0.125em 0.375em; border-radius: var(--radius-sm); }
.editor-content pre code { background: none; padding: 0; font-size: inherit; }

.editor-content hr { border: none; border-top: 1px solid var(--color-border); margin-block: 2em; }

.editor-content img { max-width: 100%; border-radius: var(--radius-lg); margin-block: 1em; }

.editor-content table { width: 100%; border-collapse: collapse; margin-block: 1em; }
.editor-content th, .editor-content td { border: 1px solid var(--color-border); padding: var(--space-2) var(--space-3); }
.editor-content th { background: var(--color-bg-subtle); font-weight: var(--font-weight-semibold); }

/* Selection */
.editor-content ::selection { background: color-mix(in srgb, var(--color-accent) 25%, transparent); }

/* Placeholder */
.editor-content:empty::before {
  content: attr(data-placeholder);
  color: var(--color-text-subtle);
  pointer-events: none;
}

/* Collaboration cursor */
.collab-cursor {
  border-left: 2px solid var(--cursor-color, var(--color-accent));
  position: relative;
}
.collab-cursor::before {
  content: attr(data-user);
  position: absolute;
  top: -1.5rem;
  left: -2px;
  background: var(--cursor-color, var(--color-accent));
  color: white;
  font-size: var(--font-size-xs);
  padding: 0.1em 0.4em;
  border-radius: var(--radius-sm);
  white-space: nowrap;
  pointer-events: none;
}

/* Floating formatting toolbar */
.editor-bubble-menu {
  display: flex;
  gap: 2px;
  padding: var(--space-1) var(--space-2);
  background: var(--color-neutral-900);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  animation: bubble-appear 0.15s var(--ease-out);
}

@keyframes bubble-appear {
  from { opacity: 0; scale: 0.92; translate: 0 4px; }
}

.bubble-btn {
  width: 1.75rem;
  height: 1.75rem;
  border: none;
  background: none;
  color: var(--color-neutral-300);
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xs);
  font-weight: bold;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.bubble-btn:hover { background: var(--color-neutral-700); color: white; }
.bubble-btn.active { color: var(--color-brand-300); }
```

---

## 133. COLOR PICKER UI

```css
/* ─── Full color picker ─── */
.color-picker {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
  width: 240px;
  box-shadow: var(--shadow-xl);
}

/* Saturation/lightness canvas */
.picker-canvas {
  width: 100%;
  aspect-ratio: 1.5;
  border-radius: var(--radius-lg);
  position: relative;
  overflow: hidden;
  cursor: crosshair;
  margin-block-end: var(--space-3);
  /* Background set by JS: hsl(var(--h), 100%, 50%) */
}

/* White gradient overlay */
.picker-canvas::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, white, transparent);
}

/* Black gradient overlay */
.picker-canvas::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent, black);
}

/* Crosshair handle */
.picker-handle {
  position: absolute;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 1px rgba(0 0 0 / 0.3), var(--shadow-sm);
  translate: -50% -50%;
  pointer-events: none;
  z-index: 2;
  left: var(--x, 50%);
  top: var(--y, 50%);
}

/* Hue slider */
.picker-hue {
  width: 100%;
  height: 12px;
  border-radius: var(--radius-full);
  background: linear-gradient(to right,
    hsl(0 100% 50%), hsl(30 100% 50%), hsl(60 100% 50%),
    hsl(90 100% 50%), hsl(120 100% 50%), hsl(150 100% 50%),
    hsl(180 100% 50%), hsl(210 100% 50%), hsl(240 100% 50%),
    hsl(270 100% 50%), hsl(300 100% 50%), hsl(330 100% 50%), hsl(360 100% 50%)
  );
  position: relative;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  border: none;
  outline: none;
  margin-block-end: var(--space-2);
}

.picker-hue::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid white;
  box-shadow: 0 0 0 1px rgba(0 0 0 / 0.2), var(--shadow-sm);
  cursor: pointer;
}

/* Alpha slider */
.picker-alpha {
  width: 100%;
  height: 12px;
  border-radius: var(--radius-full);
  position: relative;
  margin-block-end: var(--space-3);
  background:
    linear-gradient(to right, transparent, var(--current-color, #000)),
    repeating-conic-gradient(#ccc 0% 25%, #fff 0% 50%) 0 0 / 12px 12px;
  border-radius: var(--radius-full);
  cursor: pointer;
}

/* Color swatches */
.picker-swatches {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: var(--space-1);
  margin-block-end: var(--space-3);
}

.swatch {
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  cursor: pointer;
  border: 2px solid transparent;
  transition: scale var(--duration-fast) var(--ease-bounce), border-color var(--duration-fast);
}
.swatch:hover { scale: 1.15; }
.swatch.selected { border-color: var(--color-text); }

/* Hex input */
.picker-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: var(--space-1);
}

.picker-input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.picker-value-input {
  width: 100%;
  padding: 0.25rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font: inherit;
  font-size: var(--font-size-xs);
  font-family: var(--font-mono);
  text-align: center;
  outline: none;
  transition: border-color var(--duration-fast);
}
.picker-value-input:focus { border-color: var(--color-accent); }

.picker-label {
  font-size: 0.625rem;
  color: var(--color-text-subtle);
  text-transform: uppercase;
}

/* Preview swatch */
.picker-preview {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-block-end: var(--space-3);
}

.picker-preview-swatch {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  background: var(--current-color, #000);
  flex-shrink: 0;
}

/* Format toggle */
.picker-format {
  display: flex;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  width: fit-content;
  margin-block-end: var(--space-3);
}
.format-btn {
  padding: 0.2rem 0.5rem;
  font-size: var(--font-size-xs);
  border: none;
  background: none;
  cursor: pointer;
  color: var(--color-text-muted);
  transition: background var(--duration-fast);
}
.format-btn.active { background: var(--color-accent); color: white; }
```

---

## 134. DASHBOARD WIDGET TYPES

```css
/* ─── KPI / Metric card ─── */
.kpi-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  position: relative;
  overflow: hidden;
}

/* Accent stripe */
.kpi-card::before {
  content: '';
  position: absolute;
  inset-block: 0;
  inset-inline-start: 0;
  width: 4px;
  background: var(--kpi-color, var(--color-accent));
}

.kpi-card__label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  margin-block-end: var(--space-2);
}

.kpi-card__value {
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  font-weight: var(--font-weight-black);
  line-height: 1;
  font-variant-numeric: tabular-nums;
  margin-block-end: var(--space-3);
}

.kpi-card__trend {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
}

.trend-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
  padding: 0.2em 0.5em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
}
.trend-badge--up   { background: var(--color-success-100); color: var(--color-success-700); }
.trend-badge--down { background: var(--color-danger-100);  color: var(--color-danger-700); }
.trend-badge--flat { background: var(--color-bg-muted);    color: var(--color-text-muted); }

/* Mini sparkline in card */
.kpi-sparkline {
  position: absolute;
  inset-block-end: 0;
  inset-inline-end: 0;
  width: 80px;
  height: 40px;
  opacity: 0.15;
}

/* ─── Gauge widget ─── */
.gauge-widget {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  text-align: center;
}

.gauge-svg {
  width: 160px;
  height: 90px;
  overflow: visible;
}

/* SVG arc: cx=80, cy=80, r=60, startAngle=-180, endAngle=0 */
.gauge-bg {
  fill: none;
  stroke: var(--color-bg-muted);
  stroke-width: 12;
  stroke-dasharray: 188 1000; /* semicircle */
  stroke-dashoffset: -94;
  stroke-linecap: round;
}

.gauge-fill {
  fill: none;
  stroke: var(--gauge-color, var(--color-accent));
  stroke-width: 12;
  stroke-dasharray: calc(var(--gauge-pct, 0) * 1.88) 1000;
  stroke-dashoffset: -94;
  stroke-linecap: round;
  transition: stroke-dasharray 1s var(--ease-out);
}

.gauge-value {
  font-size: var(--step-2);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
}

/* ─── Activity heatmap widget ─── */
.activity-widget {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

.activity-grid {
  display: grid;
  grid-template-columns: repeat(52, 1fr);
  gap: 2px;
  margin-block: var(--space-3);
}

.activity-cell {
  aspect-ratio: 1;
  border-radius: 2px;
  background: oklch(
    from var(--color-accent)
    l
    calc(c * var(--intensity, 0))
    h
    / calc(0.1 + var(--intensity, 0) * 0.9)
  );
  cursor: pointer;
  position: relative;
}

.activity-cell:hover::after {
  content: attr(data-count) ' contributions\A' attr(data-date);
  position: absolute;
  bottom: 120%;
  left: 50%;
  translate: -50% 0;
  background: var(--color-neutral-900);
  color: white;
  font-size: 0.6875rem;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-md);
  white-space: pre;
  pointer-events: none;
  z-index: 10;
  text-align: center;
  min-width: 120px;
}

/* ─── Real-time ticker ─── */
.ticker-widget {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.ticker-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}

.ticker-live {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-danger-500);
}

.ticker-live::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-danger-500);
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; scale: 1; }
  50%       { opacity: 0.6; scale: 1.3; }
}

.ticker-row {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: var(--space-3);
  align-items: center;
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  transition: background var(--duration-fast);
  font-size: var(--font-size-sm);
}
.ticker-row:last-child { border: none; }
.ticker-row:hover { background: var(--color-bg-subtle); }

.ticker-symbol { font-weight: var(--font-weight-bold); font-family: var(--font-mono); }
.ticker-name   { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.ticker-price {
  font-weight: var(--font-weight-semibold);
  font-variant-numeric: tabular-nums;
  font-family: var(--font-mono);
}

.ticker-change {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
  padding: 0.2em 0.5em;
  border-radius: var(--radius-sm);
}

.ticker-row.up   .ticker-change { background: var(--color-success-100); color: var(--color-success-700); }
.ticker-row.down .ticker-change { background: var(--color-danger-100);  color: var(--color-danger-700); }

/* Flash on value change */
@keyframes flash-up   { from { background: var(--color-success-100); } }
@keyframes flash-down { from { background: var(--color-danger-100); } }

.ticker-row.flashing-up   { animation: flash-up 0.5s ease-out; }
.ticker-row.flashing-down { animation: flash-down 0.5s ease-out; }
```

---

## 135. STATUS INDICATORS

```css
/* ─── Status dot ─── */
.status-dot {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  font-size: var(--font-size-sm);
}

.status-dot::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  background: var(--status-color, var(--color-neutral-400));
}

.status-dot.online   { --status-color: var(--color-success-500); }
.status-dot.offline  { --status-color: var(--color-neutral-400); }
.status-dot.busy     { --status-color: var(--color-danger-500); }
.status-dot.away     { --status-color: var(--color-warning-500); }
.status-dot.pending  { --status-color: var(--color-brand-500); }

/* Animated online dot */
.status-dot.online::before {
  animation: status-pulse 2s ease-in-out infinite;
  box-shadow: 0 0 0 0 var(--color-success-300);
}

@keyframes status-pulse {
  0%   { box-shadow: 0 0 0 0 color-mix(in srgb, var(--color-success-500) 50%, transparent); }
  70%  { box-shadow: 0 0 0 6px transparent; }
  100% { box-shadow: 0 0 0 0 transparent; }
}

/* ─── Status badge (system) ─── */
.sys-status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.sys-status--operational { background: var(--color-success-100); color: var(--color-success-800); }
.sys-status--degraded    { background: var(--color-warning-100); color: var(--color-warning-800); }
.sys-status--outage      { background: var(--color-danger-100);  color: var(--color-danger-800); }
.sys-status--maintenance { background: var(--color-brand-100);   color: var(--color-brand-800); }

/* ─── Status page component ─── */
.status-component {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border);
}
.status-component:last-child { border: none; }

.status-component__name { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
.status-component__uptime { font-size: var(--font-size-xs); color: var(--color-text-muted); }

/* 90-day bar */
.uptime-bar {
  display: flex;
  gap: 1px;
  height: 28px;
  align-items: flex-end;
}

.uptime-day {
  flex: 1;
  border-radius: 2px;
  cursor: pointer;
  transition: opacity var(--duration-fast);
  min-width: 2px;
}
.uptime-day:hover { opacity: 0.7; }

.uptime-day--up      { background: var(--color-success-500); height: 100%; }
.uptime-day--partial { background: var(--color-warning-500); height: 60%; }
.uptime-day--down    { background: var(--color-danger-500);  height: 100%; }
.uptime-day--no-data { background: var(--color-bg-muted);    height: 40%; }

/* ─── Connection quality indicator ─── */
.signal-bars {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 1rem;
}

.signal-bar {
  width: 3px;
  border-radius: 1px;
  background: var(--color-bg-muted);
  transition: background var(--duration-fast);
}

.signal-bar:nth-child(1) { height: 30%; }
.signal-bar:nth-child(2) { height: 55%; }
.signal-bar:nth-child(3) { height: 80%; }
.signal-bar:nth-child(4) { height: 100%; }

/* Active bars */
.signal-bars[data-strength="1"] .signal-bar:nth-child(-n+1) { background: var(--color-danger-500); }
.signal-bars[data-strength="2"] .signal-bar:nth-child(-n+2) { background: var(--color-warning-500); }
.signal-bars[data-strength="3"] .signal-bar:nth-child(-n+3) { background: var(--color-success-500); }
.signal-bars[data-strength="4"] .signal-bar:nth-child(-n+4) { background: var(--color-success-500); }
```

---

## 136. COMPLETE DARK MODE TOKEN SYSTEM

```css
/* ─── Two-layer semantic token system ─── */

/* ── Layer 1: Raw palette (never changes) ── */
:root {
  /* Grays */
  --gray-0:   #ffffff;
  --gray-50:  #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  --gray-950: #030712;

  /* Brand */
  --blue-100: #dbeafe; --blue-500: #3b82f6; --blue-600: #2563eb; --blue-900: #1e3a8a;
  --green-100: #dcfce7; --green-500: #22c55e; --green-600: #16a34a; --green-900: #14532d;
  --red-100: #fee2e2; --red-500: #ef4444; --red-600: #dc2626; --red-900: #7f1d1d;
  --yellow-100: #fef9c3; --yellow-500: #eab308; --yellow-900: #713f12;
  --purple-100: #f3e8ff; --purple-500: #a855f7; --purple-900: #3b0764;
}

/* ── Layer 2: Semantic tokens (changes per theme) ── */

/* Light theme */
:root,
[data-theme="light"] {
  color-scheme: light;

  /* Backgrounds */
  --bg-base:        var(--gray-0);
  --bg-subtle:      var(--gray-50);
  --bg-muted:       var(--gray-100);
  --bg-moderate:    var(--gray-200);

  /* Surfaces */
  --surface-base:   var(--gray-0);
  --surface-raised: var(--gray-0);
  --surface-overlay:var(--gray-0);
  --surface-sunken: var(--gray-50);

  /* Borders */
  --border-subtle:  var(--gray-100);
  --border-default: var(--gray-200);
  --border-strong:  var(--gray-300);
  --border-bolder:  var(--gray-400);

  /* Text */
  --text-primary:   var(--gray-900);
  --text-secondary: var(--gray-600);
  --text-tertiary:  var(--gray-500);
  --text-disabled:  var(--gray-400);
  --text-inverse:   var(--gray-0);
  --text-on-accent: var(--gray-0);
  --text-link:      var(--blue-600);
  --text-link-hover:var(--blue-500);

  /* Interactive */
  --interactive:        var(--blue-500);
  --interactive-hover:  var(--blue-600);
  --interactive-active: var(--blue-900);
  --interactive-subtle: var(--blue-100);
  --interactive-focus:  var(--blue-500);

  /* Feedback */
  --success-bg:     var(--green-100);
  --success-border: #86efac;
  --success-text:   var(--green-900);
  --success-icon:   var(--green-500);

  --warning-bg:     var(--yellow-100);
  --warning-border: #fde047;
  --warning-text:   var(--yellow-900);
  --warning-icon:   var(--yellow-500);

  --danger-bg:      var(--red-100);
  --danger-border:  #fca5a5;
  --danger-text:    var(--red-900);
  --danger-icon:    var(--red-500);

  --info-bg:        var(--blue-100);
  --info-border:    #93c5fd;
  --info-text:      var(--blue-900);
  --info-icon:      var(--blue-500);

  /* Shadows */
  --shadow-color:    0deg 0% 0%;
  --shadow-strength: 0.08;
  --shadow-xs: 0 1px 2px hsl(var(--shadow-color) / var(--shadow-strength));
  --shadow-sm: 0 1px 3px hsl(var(--shadow-color) / var(--shadow-strength)),
               0 1px 2px hsl(var(--shadow-color) / calc(var(--shadow-strength) * 0.6));
  --shadow-md: 0 4px 6px hsl(var(--shadow-color) / calc(var(--shadow-strength) * 0.8)),
               0 2px 4px hsl(var(--shadow-color) / calc(var(--shadow-strength) * 0.5));
  --shadow-lg: 0 10px 15px hsl(var(--shadow-color) / calc(var(--shadow-strength) * 0.8)),
               0 4px 6px hsl(var(--shadow-color) / calc(var(--shadow-strength) * 0.5));
  --shadow-xl: 0 20px 25px hsl(var(--shadow-color) / calc(var(--shadow-strength) * 0.9)),
               0 8px 10px hsl(var(--shadow-color) / calc(var(--shadow-strength) * 0.5));
}

/* Dark theme */
[data-theme="dark"],
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;

    --bg-base:        var(--gray-950);
    --bg-subtle:      var(--gray-900);
    --bg-muted:       var(--gray-800);
    --bg-moderate:    var(--gray-700);

    --surface-base:   var(--gray-900);
    --surface-raised: var(--gray-800);
    --surface-overlay:var(--gray-800);
    --surface-sunken: var(--gray-950);

    --border-subtle:  var(--gray-800);
    --border-default: var(--gray-700);
    --border-strong:  var(--gray-600);
    --border-bolder:  var(--gray-500);

    --text-primary:   var(--gray-50);
    --text-secondary: var(--gray-400);
    --text-tertiary:  var(--gray-500);
    --text-disabled:  var(--gray-600);
    --text-inverse:   var(--gray-950);
    --text-link:      #60a5fa;
    --text-link-hover:#93c5fd;

    --interactive:        #60a5fa;
    --interactive-hover:  #93c5fd;
    --interactive-active: #dbeafe;
    --interactive-subtle: rgba(59, 130, 246, 0.15);

    --success-bg:     rgba(34, 197, 94, 0.1);
    --success-border: rgba(34, 197, 94, 0.3);
    --success-text:   #86efac;

    --warning-bg:     rgba(234, 179, 8, 0.1);
    --warning-border: rgba(234, 179, 8, 0.3);
    --warning-text:   #fde047;

    --danger-bg:      rgba(239, 68, 68, 0.1);
    --danger-border:  rgba(239, 68, 68, 0.3);
    --danger-text:    #fca5a5;

    --info-bg:        rgba(59, 130, 246, 0.1);
    --info-border:    rgba(59, 130, 246, 0.3);
    --info-text:      #93c5fd;

    --shadow-color:    0deg 0% 0%;
    --shadow-strength: 0.4;
  }
}

/* ── Apply tokens universally ── */
body {
  background: var(--bg-base);
  color: var(--text-primary);
}

/* Token usage examples */
.card {
  background:   var(--surface-base);
  border:       1px solid var(--border-default);
  box-shadow:   var(--shadow-sm);
  color:        var(--text-primary);
}

.card__description { color: var(--text-secondary); }
.card__meta        { color: var(--text-tertiary); }

.alert--success {
  background: var(--success-bg);
  border:     1px solid var(--success-border);
  color:      var(--success-text);
}
.alert--warning { background: var(--warning-bg); border: 1px solid var(--warning-border); color: var(--warning-text); }
.alert--danger  { background: var(--danger-bg);  border: 1px solid var(--danger-border);  color: var(--danger-text); }
.alert--info    { background: var(--info-bg);    border: 1px solid var(--info-border);    color: var(--info-text); }
```

---

## 137. DIFF VIEWER

```css
/* ─── Code diff / Git diff viewer ─── */
.diff-viewer {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  line-height: 1.6;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  background: var(--color-neutral-950, #0d1117);
  color: var(--color-neutral-200);
}

.diff-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  background: rgba(255 255 255 / 0.04);
  border-bottom: 1px solid rgba(255 255 255 / 0.1);
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.5);
}

.diff-filename {
  color: rgba(255 255 255 / 0.8);
  font-weight: var(--font-weight-semibold);
}

.diff-stats {
  display: flex;
  gap: var(--space-3);
}

.diff-stat--add { color: #3fb950; }
.diff-stat--del { color: #f85149; }

/* Diff body */
.diff-body { overflow-x: auto; }

.diff-table {
  width: 100%;
  border-collapse: collapse;
  min-width: max-content;
}

.diff-table td { padding: 0; white-space: pre; }

/* Line numbers */
.diff-gutter-old,
.diff-gutter-new {
  min-width: 40px;
  padding: 0 var(--space-2);
  text-align: right;
  color: rgba(255 255 255 / 0.3);
  user-select: none;
  border-right: 1px solid rgba(255 255 255 / 0.08);
  vertical-align: top;
}

/* Code content */
.diff-code {
  padding: 0 var(--space-3);
  width: 100%;
  white-space: pre-wrap;
  word-break: break-all;
}

/* Line types */
.diff-line--add {
  background: rgba(63, 185, 80, 0.1);
}
.diff-line--add .diff-gutter-new { color: rgba(63, 185, 80, 0.6); }
.diff-line--add .diff-code::before {
  content: '+';
  color: #3fb950;
  margin-inline-end: 0.5em;
}

.diff-line--del {
  background: rgba(248, 81, 73, 0.1);
}
.diff-line--del .diff-gutter-old { color: rgba(248, 81, 73, 0.6); }
.diff-line--del .diff-code::before {
  content: '-';
  color: #f85149;
  margin-inline-end: 0.5em;
}

.diff-line--context .diff-code::before {
  content: ' ';
  margin-inline-end: 0.5em;
}

/* Hunk header */
.diff-hunk {
  background: rgba(58, 130, 246, 0.05);
  border-block: 1px solid rgba(58, 130, 246, 0.15);
  color: rgba(58, 130, 246, 0.8);
  font-style: italic;
  padding: 0.25rem var(--space-4);
  font-size: var(--font-size-xs);
}

/* Char-level highlighting */
.diff-char-add { background: rgba(63, 185, 80, 0.4); border-radius: 2px; }
.diff-char-del { background: rgba(248, 81, 73, 0.4); border-radius: 2px; }

/* Unified vs split toggle */
.diff-viewer--split .diff-table {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

/* Collapse unchanged */
.diff-collapse-btn {
  width: 100%;
  padding: var(--space-1) var(--space-4);
  background: rgba(255 255 255 / 0.03);
  border: none;
  border-block: 1px solid rgba(255 255 255 / 0.08);
  color: rgba(255 255 255 / 0.4);
  font-size: var(--font-size-xs);
  font-family: var(--font-mono);
  cursor: pointer;
  text-align: start;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.diff-collapse-btn:hover { background: rgba(255 255 255 / 0.06); color: rgba(255 255 255 / 0.7); }
```

---

## 138. SEARCH RESULTS PAGE

```css
/* ─── Search results layout ─── */
.search-page {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: var(--space-8);
  max-width: 1100px;
  margin-inline: auto;
  padding: var(--space-6) var(--space-4);
}

@media (max-width: 768px) {
  .search-page { grid-template-columns: 1fr; }
  .search-filters { display: none; }
}

/* Filter sidebar */
.search-filters { }

.filter-group {
  margin-block-end: var(--space-6);
  padding-block-end: var(--space-6);
  border-bottom: 1px solid var(--color-border);
}
.filter-group:last-child { border: none; }

.filter-title {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  margin-block-end: var(--space-3);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.filter-option {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  cursor: pointer;
  padding: 0.25rem 0;
  border-radius: var(--radius-md);
  transition: color var(--duration-fast);
}
.filter-option:hover { color: var(--color-accent); }

.filter-count {
  margin-inline-start: auto;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

/* Active filter tags */
.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-block-end: var(--space-4);
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.25rem 0.75rem;
  background: var(--color-brand-100);
  color: var(--color-brand-700);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.filter-tag__remove {
  border: none;
  background: none;
  color: inherit;
  cursor: pointer;
  padding: 0;
  display: flex;
  opacity: 0.6;
  transition: opacity var(--duration-fast);
}
.filter-tag__remove:hover { opacity: 1; }

/* Search results */
.search-results { }

.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-block-end: var(--space-4);
  gap: var(--space-4);
  flex-wrap: wrap;
}

.results-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}
.results-count strong { color: var(--color-text); font-weight: var(--font-weight-semibold); }

.results-sort {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
}

/* Result item */
.search-result {
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--color-border);
  animation: result-in 0.2s var(--ease-out) backwards;
  animation-delay: calc(var(--i, 0) * 40ms);
}

@keyframes result-in {
  from { opacity: 0; translate: 0 8px; }
}

.search-result:last-child { border: none; }

.result-url {
  font-size: var(--font-size-xs);
  color: var(--color-success-600);
  margin-block-end: var(--space-1);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.result-favicon {
  width: 14px;
  height: 14px;
  border-radius: 2px;
  object-fit: contain;
}

.result-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-accent);
  text-decoration: none;
  line-height: 1.4;
  margin-block-end: var(--space-2);
  display: block;
}
.result-title:hover { text-decoration: underline; }

/* Highlight search terms */
.result-title mark,
.result-snippet mark {
  background: none;
  color: inherit;
  font-weight: var(--font-weight-bold);
  text-decoration: underline;
  text-decoration-color: var(--color-warning-400);
  text-underline-offset: 2px;
}

.result-snippet {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.6;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  margin-block-end: var(--space-2);
}

.result-meta {
  display: flex;
  gap: var(--space-4);
  font-size: var(--font-size-xs);
  color: var(--color-text-subtle);
}

/* Sitelinks */
.result-sitelinks {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2);
  margin-block-start: var(--space-3);
}

.sitelink {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: background var(--duration-fast);
}
.sitelink:hover { background: var(--color-bg-subtle); }

.sitelink__title  { font-size: var(--font-size-sm); color: var(--color-accent); font-weight: var(--font-weight-medium); }
.sitelink__desc   { font-size: var(--font-size-xs); color: var(--color-text-muted); }

/* Knowledge panel */
.knowledge-panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  margin-block-end: var(--space-6);
}

.knowledge-panel__image {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
  border-radius: var(--radius-lg);
  margin-block-end: var(--space-4);
}

.knowledge-panel__title {
  font-size: var(--step-1);
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-1);
}

.knowledge-panel__subtitle {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  margin-block-end: var(--space-3);
}

.knowledge-panel__desc {
  font-size: var(--font-size-sm);
  line-height: 1.6;
  margin-block-end: var(--space-4);
}

.knowledge-panel__attrs {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: var(--space-1) var(--space-4);
  font-size: var(--font-size-sm);
}

.knowledge-attr-key { color: var(--color-text-muted); }
.knowledge-attr-val a { color: var(--color-accent); text-decoration: none; }
.knowledge-attr-val a:hover { text-decoration: underline; }

/* Pagination */
.results-pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-1);
  padding-block: var(--space-8);
}
```

---

## 139. ADVANCED TEXT EFFECTS

```css
/* ─── Animated gradient text ─── */
@keyframes gradient-flow {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.text-gradient-animated {
  background: linear-gradient(
    270deg,
    oklch(0.7 0.25 0),
    oklch(0.7 0.25 120),
    oklch(0.7 0.25 240),
    oklch(0.7 0.25 0)
  );
  background-size: 400% 400%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-flow 4s ease infinite;
}

/* ─── Text reveal (mask wipe) ─── */
.text-mask-reveal {
  background: linear-gradient(
    to right,
    var(--color-text) 50%,
    transparent 50%
  );
  background-size: 200% 100%;
  background-position: 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  transition: background-position 0.5s var(--ease-out);
}
.text-mask-reveal:hover { background-position: 0%; }

/* ─── Outline to fill text ─── */
.text-outline-fill {
  color: transparent;
  -webkit-text-stroke: 2px var(--color-accent);
  transition:
    color                var(--duration-slow) var(--ease-out),
    -webkit-text-stroke  var(--duration-slow);
}
.text-outline-fill:hover {
  color: var(--color-accent);
  -webkit-text-stroke: 0px transparent;
}

/* ─── Flickering neon ─── */
@keyframes neon-flicker {
  0%,19%,21%,23%,25%,54%,56%,100% {
    text-shadow:
      0 0 4px #fff,
      0 0 10px #fff,
      0 0 18px var(--color-accent),
      0 0 38px var(--color-accent),
      0 0 73px var(--color-accent);
    opacity: 1;
  }
  20%,24%,55% {
    text-shadow: none;
    opacity: 0.5;
  }
}

.text-neon {
  color: white;
  animation: neon-flicker 5s infinite;
}

/* ─── Blurry emergence ─── */
@keyframes blur-emerge {
  from { filter: blur(12px); opacity: 0; letter-spacing: 0.5em; }
  to   { filter: blur(0);    opacity: 1; letter-spacing: normal; }
}
.text-blur-in { animation: blur-emerge 1s var(--ease-out) forwards; }

/* ─── Wave text (letter by letter) ─── */
.text-wave span {
  display: inline-block;
  animation: wave-letter 1.5s ease-in-out infinite;
  animation-delay: calc(var(--i, 0) * 0.08s);
}

@keyframes wave-letter {
  0%, 60%, 100% { translate: 0 0; }
  30%           { translate: 0 -0.5em; }
}

/* ─── Scramble/glitch reveal ─── */
/* Achieved purely via JS + CSS class */
.text-scramble {
  display: inline-block;
  font-family: var(--font-mono);
}
.text-scramble.scrambling {
  animation: scramble-jitter 0.05s linear infinite;
}
@keyframes scramble-jitter {
  0%,100% { translate: 0 0; }
  25%     { translate: -1px 0; }
  75%     { translate: 1px 0; }
}

/* ─── Stamp effect ─── */
@keyframes stamp-in {
  0%   { scale: 4; opacity: 0; }
  60%  { scale: 0.9; opacity: 0.8; }
  80%  { scale: 1.05; }
  100% { scale: 1; opacity: 1; }
}
.text-stamp { animation: stamp-in 0.5s var(--ease-out) forwards; }

/* ─── Text shadow depth ─── */
.text-depth {
  --depth: 6;
  text-shadow:
    1px 1px 0 hsl(0 0% 60%),
    2px 2px 0 hsl(0 0% 55%),
    3px 3px 0 hsl(0 0% 50%),
    4px 4px 0 hsl(0 0% 45%),
    5px 5px 0 hsl(0 0% 40%),
    6px 6px 8px hsl(0 0% 0% / 0.3);
}

/* ─── Kinetic typography container ─── */
.kinetic-text {
  font-size: clamp(2rem, 8vw, 6rem);
  font-weight: var(--font-weight-black);
  line-height: 1;
  overflow: hidden;
}

.kinetic-line {
  display: block;
  overflow: hidden;
}

.kinetic-word {
  display: inline-block;
  translate: 0 110%;
  animation: kinetic-in 0.7s var(--ease-out) forwards;
  animation-delay: calc(var(--w, 0) * 0.1s);
}

@keyframes kinetic-in {
  to { translate: 0 0; }
}
```

---

## 140. MODAL STACK & OVERLAY SYSTEM

```css
/* ─── Layered modal system ─── */
:root {
  --modal-base-z: 50;
}

/* Overlay manager — each modal increments z-index */
.modal-stack {
  isolation: isolate;
}

/* Individual modal */
.modal {
  position: fixed;
  inset: 0;
  z-index: calc(var(--modal-base-z) + var(--stack-index, 0) * 10);
  display: grid;
  place-items: center;
  padding: var(--space-4);
  pointer-events: none;
}

.modal.open { pointer-events: auto; }

/* Backdrop per modal */
.modal__backdrop {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / calc(0.3 + var(--stack-index, 0) * 0.05));
  backdrop-filter: blur(calc(2px + var(--stack-index, 0) * 1px));
  animation: backdrop-in var(--duration-normal) var(--ease-out);
}

@keyframes backdrop-in  { from { opacity: 0; } }
@keyframes backdrop-out { to   { opacity: 0; } }

.modal.closing .modal__backdrop { animation: backdrop-out var(--duration-fast) var(--ease-in) forwards; }

/* Dialog box */
.modal__dialog {
  position: relative;
  background: var(--color-surface);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-2xl);
  width: 100%;
  max-width: var(--modal-width, 560px);
  max-height: calc(100dvh - var(--space-8));
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: modal-in var(--duration-normal) var(--spring-bouncy);
  z-index: 1;
}

@keyframes modal-in {
  from { opacity: 0; scale: 0.93; translate: 0 12px; }
}

.modal.closing .modal__dialog {
  animation: modal-out var(--duration-fast) var(--ease-in) forwards;
}

@keyframes modal-out {
  to { opacity: 0; scale: 0.96; translate: 0 8px; }
}

/* Stacked modal offset */
.modal[style*="--stack-index: 1"] .modal__dialog {
  scale: 0.98;
  translate: 0 -10px;
}
.modal[style*="--stack-index: 2"] .modal__dialog {
  scale: 0.96;
  translate: 0 -20px;
}

/* Mobile sheet variant */
@media (max-width: 640px) {
  .modal--sheet {
    align-items: flex-end;
    padding: 0;
  }
  .modal--sheet .modal__dialog {
    border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
    max-width: 100%;
    max-height: 90dvh;
    animation: sheet-in var(--duration-normal) var(--ease-out);
  }
  @keyframes sheet-in {
    from { translate: 0 100%; }
  }
}

/* Fullscreen modal */
.modal--fullscreen .modal__dialog {
  max-width: 100%;
  max-height: 100%;
  border-radius: 0;
  height: 100dvh;
  animation: none;
}

/* Focus trap visual */
.modal:not(.open) { display: none; }

/* Scrollable body */
.modal__body {
  flex: 1;
  overflow-y: auto;
  overscroll-behavior: contain;
}

/* Confirm dialog variant */
.modal--confirm .modal__dialog { max-width: 400px; }
.modal--confirm .modal__body {
  padding: var(--space-6);
  text-align: center;
}
.modal--confirm .confirm-icon {
  font-size: 3rem;
  margin-block-end: var(--space-4);
}
.modal--confirm .confirm-title {
  font-size: var(--step-1);
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-2);
}
.modal--confirm .confirm-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}
.modal--confirm .confirm-actions {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--color-border);
}
.modal--confirm .confirm-actions .btn { flex: 1; }
```

---

## 141. SCROLLING PATTERNS

```css
/* ─── Smooth momentum scroll ─── */
.smooth-scroll {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-y: contain;
  scroll-behavior: smooth;
}

/* ─── Virtual scroll container ─── */
.virtual-list {
  height: 400px;
  overflow-y: auto;
  position: relative;
  contain: strict;
}

.virtual-list__inner {
  position: relative;
  height: var(--total-height, 0);
}

.virtual-list__item {
  position: absolute;
  top: var(--item-top, 0);
  left: 0;
  right: 0;
  height: var(--item-height, 48px);
  contain: layout style;
}

/* ─── Horizontal scroll with snap ─── */
.h-scroll {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-padding-inline: var(--space-4);
  padding-inline: var(--space-4);
  gap: var(--space-4);
  scrollbar-width: none;
  padding-block: var(--space-2);
  -webkit-overflow-scrolling: touch;
}
.h-scroll::-webkit-scrollbar { display: none; }
.h-scroll > * { scroll-snap-align: start; flex-shrink: 0; }

/* ─── Infinite scroll loading indicator ─── */
.infinite-scroll-sentinel {
  height: 2px;
  visibility: hidden;
}

.infinite-scroll-loader {
  display: flex;
  justify-content: center;
  padding: var(--space-8);
  opacity: 0;
  transition: opacity var(--duration-normal);
}
.infinite-scroll-loader.visible { opacity: 1; }

/* ─── Scroll fade edges ─── */
.scroll-fade {
  position: relative;
  overflow: hidden;
}

.scroll-fade::before,
.scroll-fade::after {
  content: '';
  position: absolute;
  z-index: 1;
  pointer-events: none;
}

/* Horizontal fades */
.scroll-fade--x::before {
  inset-block: 0;
  inset-inline-start: 0;
  width: 2rem;
  background: linear-gradient(to right, var(--color-surface), transparent);
}
.scroll-fade--x::after {
  inset-block: 0;
  inset-inline-end: 0;
  width: 2rem;
  background: linear-gradient(to left, var(--color-surface), transparent);
}

/* Vertical fades */
.scroll-fade--y::before {
  inset-inline: 0;
  inset-block-start: 0;
  height: 2rem;
  background: linear-gradient(to bottom, var(--color-surface), transparent);
}
.scroll-fade--y::after {
  inset-inline: 0;
  inset-block-end: 0;
  height: 2rem;
  background: linear-gradient(to top, var(--color-surface), transparent);
}

/* ─── Scroll to top button ─── */
.scroll-top-btn {
  position: fixed;
  inset-block-end: var(--space-6);
  inset-inline-end: var(--space-6);
  width: 2.5rem;
  height: 2.5rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  box-shadow: var(--shadow-md);
  z-index: var(--z-fixed);
  opacity: 0;
  translate: 0 1rem;
  transition:
    opacity   var(--duration-normal),
    translate var(--duration-normal) var(--ease-bounce);
  pointer-events: none;
}

.scroll-top-btn.visible {
  opacity: 1;
  translate: 0 0;
  pointer-events: auto;
}

.scroll-top-btn:hover {
  background: var(--color-accent);
  color: white;
  border-color: var(--color-accent);
  scale: 1.1;
}
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║              CSS MASTER GUIDE — PARTS I–VIII                         ║
╠══════════════════════════════════════════════════════════════════════╣
║  141 chapters · 800+ code examples · ~28,000 lines                  ║
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
```
