# CSS GUIDE — PART 14
## Chapters 193–207

---

## 193. CONTEXT-AWARE THEMING

```css
/* ─── Theme propagation via CSS custom properties ─── */

/* Base theme contract — every theme MUST define these */
[data-theme] {
  /* Surfaces */
  --bg:        unset;
  --surface:   unset;
  --elevated:  unset;
  /* Text */
  --fg:        unset;
  --fg-muted:  unset;
  /* Brand */
  --accent:    unset;
  --accent-fg: unset;
  /* Feedback */
  --ok:        unset;
  --warn:      unset;
  --err:       unset;
}

/* Light theme */
[data-theme="light"] {
  color-scheme: light;
  --bg:        oklch(1 0 0);
  --surface:   oklch(1 0 0);
  --elevated:  oklch(0.98 0 0);
  --fg:        oklch(0.15 0 0);
  --fg-muted:  oklch(0.45 0 0);
  --accent:    oklch(0.60 0.20 250);
  --accent-fg: oklch(1 0 0);
  --ok:        oklch(0.55 0.18 145);
  --warn:      oklch(0.65 0.20 65);
  --err:       oklch(0.55 0.22 25);
}

/* Dark theme */
[data-theme="dark"] {
  color-scheme: dark;
  --bg:        oklch(0.10 0 0);
  --surface:   oklch(0.14 0 0);
  --elevated:  oklch(0.18 0 0);
  --fg:        oklch(0.95 0 0);
  --fg-muted:  oklch(0.60 0 0);
  --accent:    oklch(0.70 0.20 250);
  --accent-fg: oklch(0.10 0 0);
  --ok:        oklch(0.70 0.18 145);
  --warn:      oklch(0.80 0.20 65);
  --err:       oklch(0.70 0.22 25);
}

/* Solarized theme */
[data-theme="solarized"] {
  color-scheme: light;
  --bg:        oklch(0.97 0.02 90);
  --surface:   oklch(0.95 0.02 90);
  --elevated:  oklch(0.93 0.02 90);
  --fg:        oklch(0.40 0.05 220);
  --fg-muted:  oklch(0.55 0.05 220);
  --accent:    oklch(0.55 0.18 220);
  --accent-fg: oklch(1 0 0);
  --ok:        oklch(0.55 0.15 145);
  --warn:      oklch(0.65 0.18 65);
  --err:       oklch(0.55 0.20 25);
}

/* Auto theme (follows OS) */
@media (prefers-color-scheme: dark) {
  [data-theme="auto"] {
    color-scheme: dark;
    --bg:        oklch(0.10 0 0);
    --surface:   oklch(0.14 0 0);
    --elevated:  oklch(0.18 0 0);
    --fg:        oklch(0.95 0 0);
    --fg-muted:  oklch(0.60 0 0);
    --accent:    oklch(0.70 0.20 250);
    --accent-fg: oklch(0.10 0 0);
    --ok:        oklch(0.70 0.18 145);
    --warn:      oklch(0.80 0.20 65);
    --err:       oklch(0.70 0.22 25);
  }
}

/* Component using only theme tokens */
.themed-card {
  background: var(--surface);
  color: var(--fg);
  border: 1px solid color-mix(in oklch, var(--fg) 12%, transparent);
}

.themed-card p { color: var(--fg-muted); }
.themed-btn-primary { background: var(--accent); color: var(--accent-fg); }
.themed-badge-ok   { background: color-mix(in oklch, var(--ok) 15%, transparent); color: var(--ok); }
.themed-badge-err  { background: color-mix(in oklch, var(--err) 15%, transparent); color: var(--err); }

/* ─── Local context override ─── */
/* A dark card inside a light page */
.invert-theme {
  --bg:       oklch(0.10 0 0);
  --surface:  oklch(0.14 0 0);
  --fg:       oklch(0.95 0 0);
  --fg-muted: oklch(0.60 0 0);
  background: var(--bg);
  color: var(--fg);
  color-scheme: dark;
}

/* Brand section override */
.brand-section {
  --bg:        var(--accent);
  --surface:   color-mix(in oklch, var(--accent) 85%, black);
  --fg:        var(--accent-fg);
  --fg-muted:  color-mix(in oklch, var(--accent-fg) 70%, transparent);
  background: var(--bg);
  color: var(--fg);
}
```

---

## 194. ANIMATED NUMBER COUNTERS

```css
/* ─── CSS counter animation (scroll-driven) ─── */
@property --n {
  syntax: '<integer>';
  initial-value: 0;
  inherits: false;
}

.count-up {
  counter-reset: n var(--n);
  animation: count-to linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 60%;
}

.count-up::after {
  content: counter(n);
}

@keyframes count-to {
  from { --n: 0; }
  to   { --n: var(--count-target, 100); }
}

/* With suffix (k, m, %, +) */
.count-up[data-suffix]::after {
  content: counter(n) attr(data-suffix);
}

/* Animated counter via transition */
@property --counter-value {
  syntax: '<number>';
  initial-value: 0;
  inherits: false;
}

.counter-animated {
  --counter-value: 0;
  transition: --counter-value 1.5s var(--ease-out);
}

/* JS: el.style.setProperty('--counter-value', target) */
/* then read value in JS to display: Math.round(el.style.getPropertyValue('--counter-value')) */

/* ─── Odometer / slot machine counter ─── */
.odometer {
  display: inline-flex;
  overflow: hidden;
  font-family: var(--font-mono);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
}

.odometer-digit {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 1em;
  position: relative;
}

.odometer-reel {
  display: flex;
  flex-direction: column;
  translate: 0 calc(var(--current, 0) * -1em);
  transition: translate 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.odometer-reel span {
  height: 1em;
  display: block;
  line-height: 1;
}

/* ─── Flip counter ─── */
.flip-counter {
  display: inline-flex;
  gap: 4px;
}

.flip-digit {
  position: relative;
  width: 1.5em;
  height: 2em;
  perspective: 200px;
}

.flip-digit__front,
.flip-digit__back {
  position: absolute;
  inset: 0;
  background: var(--color-neutral-800);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  font-weight: bold;
  backface-visibility: hidden;
  font-variant-numeric: tabular-nums;
}

.flip-digit__back {
  transform: rotateX(180deg);
}

.flip-digit.flipping .flip-digit__front {
  animation: flip-front 0.3s ease-in forwards;
}
.flip-digit.flipping .flip-digit__back {
  animation: flip-back 0.3s ease-out forwards 0.3s;
}

@keyframes flip-front {
  to { transform: rotateX(-90deg); }
}
@keyframes flip-back {
  from { transform: rotateX(90deg); }
  to   { transform: rotateX(0deg); }
}

/* Top/bottom fold effect */
.flip-digit::after {
  content: '';
  position: absolute;
  inset-inline: 0;
  inset-block-start: 50%;
  height: 1px;
  background: rgba(0 0 0 / 0.3);
  z-index: 2;
}
```

---

## 195. MAP / GEO UI

```css
/* ─── Map container shell ─── */
.map-shell {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-xl);
  overflow: hidden;
  background: #e8e0d8;
}

.map-shell iframe,
.map-shell .map-tile {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: none;
}

/* Map overlay controls */
.map-controls {
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  z-index: 10;
}

.map-control-btn {
  width: 2.25rem;
  height: 2.25rem;
  background: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
  color: var(--color-text);
  font-size: 1.25rem;
  font-weight: bold;
  transition: background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
}
.map-control-btn:hover { background: var(--color-bg-subtle); scale: 1.05; }

/* Zoom control group */
.map-zoom {
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}
.map-zoom .map-control-btn { border-radius: 0; box-shadow: none; }
.map-zoom .map-control-btn:not(:last-child) { border-bottom: 1px solid var(--color-border); }

/* Custom marker */
.map-marker {
  position: absolute;
  translate: -50% -100%;
  left: var(--mx, 50%);
  top:  var(--my, 50%);
  z-index: 5;
  cursor: pointer;
}

.map-marker__pin {
  width: 32px;
  height: 40px;
  background: var(--marker-color, var(--color-accent));
  border-radius: 50% 50% 50% 0;
  rotate: -45deg;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
  transition: scale var(--duration-fast) var(--ease-bounce);
}
.map-marker:hover .map-marker__pin { scale: 1.2; }

.map-marker__icon {
  rotate: 45deg;
  font-size: 1rem;
  color: white;
}

/* Pulse ring on marker */
.map-marker__pulse {
  position: absolute;
  bottom: 0;
  left: 50%;
  translate: -50% 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--marker-color, var(--color-accent));
  opacity: 0;
  animation: marker-pulse 2s ease-in-out infinite;
}

@keyframes marker-pulse {
  0%   { scale: 0.5; opacity: 0.5; }
  100% { scale: 2; opacity: 0; }
}

/* Marker cluster */
.map-cluster {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-sm);
  box-shadow: var(--shadow-md);
  border: 3px solid white;
  cursor: pointer;
  transition: scale var(--duration-fast) var(--ease-bounce);
}
.map-cluster:hover { scale: 1.1; }

/* Marker tooltip */
.map-tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  translate: -50% 0;
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-3) var(--space-4);
  box-shadow: var(--shadow-xl);
  min-width: 160px;
  pointer-events: none;
  opacity: 0;
  scale: 0.9;
  transition: opacity var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
  z-index: 20;
}
.map-marker:hover .map-tooltip {
  opacity: 1;
  scale: 1;
  pointer-events: auto;
}

.map-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  translate: -50% 0;
  border: 6px solid transparent;
  border-top-color: white;
  filter: drop-shadow(0 2px 2px rgba(0 0 0 / 0.1));
}

/* Search box overlay */
.map-search {
  position: absolute;
  top: var(--space-3);
  left: var(--space-3);
  right: 4rem;
  z-index: 10;
}

.map-search__input {
  width: 100%;
  padding: 0.625rem 1rem;
  border: none;
  border-radius: var(--radius-full);
  background: white;
  box-shadow: var(--shadow-md);
  font: inherit;
  font-size: var(--font-size-sm);
  outline: none;
}

/* Info panel sidebar */
.map-sidebar {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 320px;
  background: white;
  z-index: 10;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
  translate: calc(-100% - 1px);
  transition: translate var(--duration-slow) var(--ease-out);
}

.map-sidebar.open { translate: 0; }
```

---

## 196. TIMELINE / ACTIVITY FEED

```css
/* ─── Activity feed ─── */
.activity-feed {
  display: flex;
  flex-direction: column;
  gap: 0;
  position: relative;
}

/* Connecting line */
.activity-feed::before {
  content: '';
  position: absolute;
  inset-inline-start: 1.25rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(
    to bottom,
    transparent,
    var(--color-border) 5%,
    var(--color-border) 95%,
    transparent
  );
}

/* Feed item */
.feed-item {
  display: flex;
  gap: var(--space-4);
  padding-block: var(--space-4);
  padding-inline-start: var(--space-2);
  position: relative;
  animation: feed-item-in 0.3s var(--ease-out) backwards;
  animation-delay: calc(var(--i, 0) * 60ms);
}

@keyframes feed-item-in {
  from { opacity: 0; translate: -12px 0; }
}

/* Icon bubble */
.feed-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: var(--feed-icon-bg, var(--color-bg-muted));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
  border: 2px solid var(--color-surface);
  box-shadow: 0 0 0 3px var(--color-surface);
  position: relative;
  z-index: 1;
}

/* Action type colors */
.feed-item--created  { --feed-icon-bg: var(--color-success-100); }
.feed-item--updated  { --feed-icon-bg: var(--color-brand-100); }
.feed-item--deleted  { --feed-icon-bg: var(--color-danger-100); }
.feed-item--comment  { --feed-icon-bg: var(--color-warning-100); }
.feed-item--assigned { --feed-icon-bg: oklch(0.93 0.05 300); }

/* Content */
.feed-content { flex: 1; min-width: 0; }

.feed-header {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  margin-block-end: var(--space-1);
  flex-wrap: wrap;
}

.feed-actor {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  color: var(--color-text);
}

.feed-action {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.feed-subject {
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
  font-size: var(--font-size-sm);
}

.feed-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-subtle);
  margin-inline-start: auto;
  white-space: nowrap;
  padding-block-start: 2px;
}

/* Feed body (comment, diff, etc.) */
.feed-body {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-3);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-block-start: var(--space-2);
}

/* Inline diff in feed */
.feed-diff {
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  line-height: 1.6;
}

.feed-diff .del {
  background: var(--color-danger-100);
  color: var(--color-danger-700);
  text-decoration: line-through;
  padding: 0 2px;
  border-radius: 2px;
}

.feed-diff .ins {
  background: var(--color-success-100);
  color: var(--color-success-700);
  padding: 0 2px;
  border-radius: 2px;
}

/* Reactions */
.feed-reactions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-block-start: var(--space-2);
}

.feed-reaction {
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
  padding: 0.2em 0.5em;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  cursor: pointer;
  transition:
    background    var(--duration-fast),
    border-color  var(--duration-fast),
    scale         var(--duration-fast) var(--ease-bounce);
}
.feed-reaction:hover { background: var(--color-bg-muted); }
.feed-reaction.mine  {
  background: var(--color-brand-100);
  border-color: var(--color-brand-300);
  color: var(--color-brand-700);
}
.feed-reaction:active { scale: 0.94; }

.feed-reaction__count {
  font-weight: var(--font-weight-semibold);
  font-variant-numeric: tabular-nums;
}

/* Load more */
.feed-load-more {
  display: flex;
  justify-content: center;
  padding-block: var(--space-4);
  position: relative;
  z-index: 1;
}
```

---

## 197. AUDIT LOG TABLE

```css
/* ─── Audit log ─── */
.audit-log {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.audit-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  background: var(--color-bg-subtle);
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.audit-filters {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.audit-filter-chip {
  padding: 0.25rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  background: var(--color-surface);
  color: var(--color-text-muted);
  transition: all var(--duration-fast);
}
.audit-filter-chip.active {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: white;
}

.audit-search { margin-inline-start: auto; }

/* Log row */
.audit-row {
  display: grid;
  grid-template-columns: 160px 120px 1fr auto auto;
  gap: var(--space-4);
  align-items: center;
  padding: var(--space-3) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  font-size: var(--font-size-sm);
  transition: background var(--duration-fast);
}
.audit-row:last-child { border: none; }
.audit-row:hover { background: var(--color-bg-subtle); }

.audit-ts {
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.audit-actor {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  min-width: 0;
}

.audit-actor img {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  flex-shrink: 0;
  object-fit: cover;
}

.audit-actor-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: var(--font-weight-medium);
}

/* Action badge */
.audit-action {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 0.15em 0.5em;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  font-family: var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.audit-action--create { background: var(--color-success-100); color: var(--color-success-800); }
.audit-action--update { background: var(--color-brand-100);   color: var(--color-brand-800); }
.audit-action--delete { background: var(--color-danger-100);  color: var(--color-danger-800); }
.audit-action--login  { background: var(--color-bg-muted);    color: var(--color-text-muted); }
.audit-action--export { background: var(--color-warning-100); color: var(--color-warning-800); }

.audit-resource {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--color-text);
}

.audit-resource strong { font-weight: var(--font-weight-medium); }

.audit-ip {
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  white-space: nowrap;
}

/* Expandable details */
.audit-row-detail {
  grid-column: 1 / -1;
  background: var(--color-bg-subtle);
  border-top: 1px solid var(--color-border);
  padding: var(--space-4) var(--space-5);
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  line-height: 1.7;
  color: var(--color-text-muted);
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s var(--ease-out), padding 0.3s;
  padding-block: 0;
}

.audit-row.expanded .audit-row-detail {
  max-height: 400px;
  padding-block: var(--space-4);
}

/* Severity indicator */
.audit-severity {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
.audit-severity--info    { background: var(--color-brand-400); }
.audit-severity--warning { background: var(--color-warning-500); }
.audit-severity--critical{ background: var(--color-danger-500); animation: pulse 1s ease-in-out infinite; }
```

---

## 198. IMAGE ANNOTATION UI

```css
/* ─── Image annotator ─── */
.annotator {
  position: relative;
  display: inline-block;
  cursor: crosshair;
  user-select: none;
}

.annotator img {
  display: block;
  max-width: 100%;
}

/* Annotation layer */
.annotation-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

/* Annotation region */
.annotation {
  position: absolute;
  border: 2px solid var(--annotation-color, var(--color-accent));
  border-radius: var(--radius-sm);
  background: color-mix(in srgb, var(--annotation-color, var(--color-accent)) 10%, transparent);
  cursor: pointer;
  pointer-events: auto;
  transition:
    background  var(--duration-fast),
    border-color var(--duration-fast),
    scale       var(--duration-fast) var(--ease-bounce);
  left:   var(--ax, 0);
  top:    var(--ay, 0);
  width:  var(--aw, 100px);
  height: var(--ah, 100px);
}

.annotation:hover {
  background: color-mix(in srgb, var(--annotation-color, var(--color-accent)) 20%, transparent);
  z-index: 2;
}

.annotation.selected {
  border-color: var(--annotation-color, var(--color-accent));
  background: color-mix(in srgb, var(--annotation-color, var(--color-accent)) 15%, transparent);
  z-index: 3;
  outline: 3px solid color-mix(in srgb, var(--annotation-color, var(--color-accent)) 30%, transparent);
}

/* Annotation number badge */
.annotation::before {
  content: var(--num, '1');
  position: absolute;
  top: -10px;
  left: -10px;
  width: 20px;
  height: 20px;
  background: var(--annotation-color, var(--color-accent));
  color: white;
  border-radius: 50%;
  font-size: 0.625rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
  box-shadow: var(--shadow-sm);
  font-family: var(--font-sans);
  pointer-events: none;
}

/* Resize handles */
.annotation-handle {
  position: absolute;
  width: 8px;
  height: 8px;
  background: white;
  border: 2px solid var(--annotation-color, var(--color-accent));
  border-radius: 2px;
}
.annotation-handle[data-pos="tl"] { top: -4px; left: -4px; cursor: nw-resize; }
.annotation-handle[data-pos="tr"] { top: -4px; right: -4px; cursor: ne-resize; }
.annotation-handle[data-pos="bl"] { bottom: -4px; left: -4px; cursor: sw-resize; }
.annotation-handle[data-pos="br"] { bottom: -4px; right: -4px; cursor: se-resize; }

/* Annotation popup */
.annotation-popup {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  min-width: 200px;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: var(--space-3);
  z-index: 20;
  animation: annotation-pop 0.2s var(--ease-bounce);
  pointer-events: auto;
}

@keyframes annotation-pop { from { opacity: 0; scale: 0.9; translate: 0 6px; } }

.annotation-popup textarea {
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-2);
  font: inherit;
  font-size: var(--font-size-xs);
  resize: vertical;
  min-height: 60px;
  outline: none;
  transition: border-color var(--duration-fast);
}
.annotation-popup textarea:focus { border-color: var(--color-accent); }

/* Annotations panel */
.annotations-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-height: 400px;
  overflow-y: auto;
}

.annotation-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: background var(--duration-fast), border-color var(--duration-fast);
}
.annotation-item:hover { background: var(--color-bg-subtle); }
.annotation-item.active { border-color: var(--color-accent); background: color-mix(in srgb, var(--color-accent) 5%, transparent); }

.annotation-item__num {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--annotation-color, var(--color-accent));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xs);
  font-weight: bold;
  flex-shrink: 0;
}

.annotation-item__text {
  flex: 1;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  line-height: 1.5;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
```

---

## 199. DYNAMIC ISLAND

```css
/* ─── Dynamic Island (iOS 14 Pro+) style notification ─── */
.dynamic-island {
  position: fixed;
  top: var(--space-3);
  left: 50%;
  translate: -50% 0;
  z-index: var(--z-top);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* The pill */
.island-pill {
  background: #000;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  overflow: hidden;
  cursor: pointer;
  transition:
    width    0.4s cubic-bezier(0.34, 1.56, 0.64, 1),
    height   0.4s cubic-bezier(0.34, 1.56, 0.64, 1),
    border-radius 0.4s;

  /* Default — compact */
  width: 120px;
  height: 34px;
  padding-inline: var(--space-3);
}

/* States */
.island-pill[data-state="compact"] {
  width: 120px;
  height: 34px;
}

.island-pill[data-state="expanded"] {
  width: 340px;
  height: 80px;
  border-radius: var(--radius-2xl);
  padding: var(--space-3) var(--space-4);
}

.island-pill[data-state="minimal"] {
  width: 34px;
  height: 34px;
}

/* Content layers */
.island-content {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  opacity: 0;
  transition: opacity 0.2s;
}

.island-pill[data-state="expanded"] .island-content { opacity: 1; }

/* Compact icons */
.island-icons {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.island-pill[data-state="expanded"] .island-icons { display: none; }
.island-pill[data-state="minimal"] .island-icons { display: none; }

.island-icon-left,
.island-icon-right {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

/* Progress bar in island */
.island-progress {
  flex: 1;
  height: 3px;
  background: rgba(255 255 255 / 0.2);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.island-progress__fill {
  height: 100%;
  background: var(--color-success-400);
  width: var(--progress, 0%);
  transition: width 0.5s linear;
  border-radius: inherit;
}

/* Album art in island */
.island-art {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  object-fit: cover;
  flex-shrink: 0;
}

/* Text in island */
.island-text { flex: 1; min-width: 0; }
.island-title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: white;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.island-subtitle {
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.6);
}

/* Wave animation (music) */
.island-wave {
  display: flex;
  align-items: center;
  gap: 2px;
  height: 20px;
}
.island-wave span {
  width: 2px;
  background: var(--color-success-400);
  border-radius: 1px;
  animation: island-wave-bar 0.8s ease-in-out infinite alternate;
}
.island-wave span:nth-child(1) { height: 40%; animation-delay: 0s; }
.island-wave span:nth-child(2) { height: 70%; animation-delay: 0.1s; }
.island-wave span:nth-child(3) { height: 100%; animation-delay: 0.2s; }
.island-wave span:nth-child(4) { height: 60%; animation-delay: 0.15s; }

@keyframes island-wave-bar {
  from { height: 20%; }
  to   { height: 100%; }
}
```

---

## 200. SKELETON PATTERNS LIBRARY

```css
/* ─── Complete skeleton loading system ─── */
@keyframes sk-shimmer {
  from { background-position: -200% center; }
  to   { background-position: 200% center; }
}

/* Base skeleton mixin */
.sk {
  background: linear-gradient(
    90deg,
    var(--sk-base, var(--color-bg-muted)) 25%,
    var(--sk-shine, var(--color-bg-subtle)) 50%,
    var(--sk-base, var(--color-bg-muted)) 75%
  );
  background-size: 200% 100%;
  animation: sk-shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-md);
}

/* Prefers reduced motion: no animation */
@media (prefers-reduced-motion: reduce) {
  .sk { animation: none; }
}

/* Dark skeleton */
[data-theme="dark"] .sk {
  --sk-base:  oklch(0.20 0 0);
  --sk-shine: oklch(0.25 0 0);
}

/* ── Shape utilities ── */
.sk-circle { border-radius: 50%; aspect-ratio: 1; }
.sk-text   { height: 1em; border-radius: var(--radius-full); }
.sk-block  { border-radius: var(--radius-md); }
.sk-round  { border-radius: var(--radius-2xl); }

/* ── Preset skeleton components ── */

/* Avatar */
.sk-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
}

/* Text lines */
.sk-title   { height: 1.25em; width: 60%; border-radius: var(--radius-full); }
.sk-line    { height: 0.875em; width: 100%; border-radius: var(--radius-full); }
.sk-line-sm { height: 0.875em; width: 70%; border-radius: var(--radius-full); }
.sk-line-xs { height: 0.875em; width: 40%; border-radius: var(--radius-full); }

/* ── Preset skeleton layouts ── */

/* Card skeleton */
.sk-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  padding: var(--space-4);
}

.sk-card__image { width: 100%; aspect-ratio: 16/9; border-radius: var(--radius-lg); }
.sk-card__body  { padding-block-start: var(--space-4); display: flex; flex-direction: column; gap: var(--space-3); }

/* Profile skeleton */
.sk-profile {
  display: flex;
  gap: var(--space-4);
  align-items: flex-start;
  padding: var(--space-4);
}
.sk-profile__avatar { width: 3rem; height: 3rem; border-radius: 50%; flex-shrink: 0; }
.sk-profile__info   { flex: 1; display: flex; flex-direction: column; gap: var(--space-2); }

/* Table skeleton */
.sk-table-row {
  display: grid;
  grid-template-columns: 2rem 1fr 1fr 1fr auto;
  gap: var(--space-4);
  align-items: center;
  padding-block: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}
.sk-table-row > .sk { height: 0.75em; border-radius: var(--radius-full); }

/* List item skeleton */
.sk-list-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding-block: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

/* Dashboard widget skeleton */
.sk-widget {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}
.sk-widget__value { height: 2.5rem; width: 40%; border-radius: var(--radius-md); }
.sk-widget__chart { height: 80px; border-radius: var(--radius-lg); }

/* Article skeleton */
.sk-article { display: flex; flex-direction: column; gap: var(--space-4); }
.sk-article__hero    { width: 100%; aspect-ratio: 2/1; border-radius: var(--radius-xl); }
.sk-article__heading { height: 2em; width: 80%; border-radius: var(--radius-full); }

/* Chat skeleton */
.sk-chat { display: flex; flex-direction: column; gap: var(--space-4); padding: var(--space-4); }
.sk-chat-msg       { display: flex; gap: var(--space-3); align-items: flex-end; max-width: 70%; }
.sk-chat-msg--right { align-self: flex-end; flex-direction: row-reverse; }
.sk-chat-msg__bubble { flex: 1; height: 3rem; border-radius: var(--radius-2xl); }

/* Staggered shimmer delay */
.sk:nth-child(1) { animation-delay: 0s; }
.sk:nth-child(2) { animation-delay: 0.1s; }
.sk:nth-child(3) { animation-delay: 0.2s; }
.sk:nth-child(4) { animation-delay: 0.3s; }
.sk:nth-child(5) { animation-delay: 0.4s; }
```

---

## 201. CSS-ONLY MODALS WITHOUT JS

```css
/* ─── CSS-only modal via :target ─── */

/* HTML pattern:
   <a href="#modal-1">Open</a>
   <div id="modal-1" class="css-modal"> ... </div>
*/

.css-modal {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-normal);
}

.css-modal:target {
  opacity: 1;
  pointer-events: auto;
}

/* Backdrop */
.css-modal__backdrop {
  position: absolute;
  inset: 0;
  background: rgb(0 0 0 / 0.5);
  backdrop-filter: blur(4px);
}

/* Close link as backdrop */
.css-modal__close-area {
  position: absolute;
  inset: 0;
  z-index: 0;
}

/* Dialog box */
.css-modal__dialog {
  position: relative;
  background: var(--color-surface);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-2xl);
  padding: var(--space-8);
  width: 100%;
  max-width: 480px;
  z-index: 1;
  transition: scale var(--duration-normal) var(--ease-bounce), translate var(--duration-normal);
  scale: 0.9;
  translate: 0 20px;
}

.css-modal:target .css-modal__dialog {
  scale: 1;
  translate: 0 0;
}

/* Close X link */
.css-modal__close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--color-bg-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: var(--color-text-muted);
  font-size: 1.125rem;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.css-modal__close:hover { background: var(--color-bg-muted); color: var(--color-text); }

/* ─── CSS-only tooltip via :focus-within + sibling ─── */
.tooltip-trigger {
  position: relative;
  display: inline-block;
}

.tooltip-trigger:focus,
.tooltip-trigger:hover {
  outline: none;
}

.tooltip-trigger:focus + .tooltip-content,
.tooltip-trigger:hover + .tooltip-content {
  opacity: 1;
  translate: -50% 0;
  pointer-events: auto;
}

.tooltip-content {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  translate: -50% 6px;
  background: var(--color-neutral-900);
  color: white;
  font-size: var(--font-size-xs);
  padding: 0.4em 0.75em;
  border-radius: var(--radius-md);
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-fast), translate var(--duration-fast);
  z-index: var(--z-tooltip);
}

/* ─── CSS-only accordion via :has() ─── */
.css-accordion {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.css-accordion-item {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.css-accordion-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  width: 0;
  height: 0;
}

.css-accordion-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  cursor: pointer;
  font-weight: var(--font-weight-medium);
  user-select: none;
  transition: background var(--duration-fast);
}
.css-accordion-label:hover { background: var(--color-bg-subtle); }

.css-accordion-label::after {
  content: '+';
  font-size: 1.25rem;
  font-weight: 300;
  color: var(--color-text-muted);
  transition: rotate var(--duration-fast) var(--ease-out);
}

.css-accordion-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s var(--ease-out);
}

/* Open state via :has() */
.css-accordion-item:has(.css-accordion-input:checked) .css-accordion-label::after {
  rotate: 45deg;
}

.css-accordion-item:has(.css-accordion-input:checked) .css-accordion-body {
  max-height: 500px;
}

.css-accordion-item:has(.css-accordion-input:checked) .css-accordion-label {
  background: var(--color-bg-subtle);
}

.css-accordion-body__inner {
  padding: var(--space-4) var(--space-5);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.6;
}
```

---

## 202. RECIPE CARD

```css
/* ─── Recipe card ─── */
.recipe-card {
  background: var(--color-surface);
  border-radius: var(--radius-2xl);
  overflow: hidden;
  border: 1px solid var(--color-border);
  max-width: 720px;
  margin-inline: auto;
}

.recipe-hero {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.recipe-hero img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: scale var(--duration-slow) var(--ease-out);
}
.recipe-card:hover .recipe-hero img { scale: 1.04; }

/* Overlay info */
.recipe-hero__overlay {
  position: absolute;
  inset-block-end: 0;
  inset-inline: 0;
  padding: var(--space-6);
  background: linear-gradient(to top, rgb(0 0 0 / 0.75), transparent);
}

.recipe-category {
  display: inline-flex;
  padding: 0.25em 0.75em;
  background: var(--color-accent);
  color: white;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  margin-block-end: var(--space-2);
}

.recipe-title {
  font-size: var(--step-2);
  font-weight: var(--font-weight-black);
  color: white;
  text-wrap: balance;
  line-height: 1.2;
}

/* Meta row */
.recipe-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-border);
}

.recipe-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  text-align: center;
}

.recipe-stat__icon { font-size: 1.25rem; }

.recipe-stat__value {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
}

.recipe-stat__label {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  font-weight: var(--font-weight-medium);
}

/* Difficulty */
.recipe-difficulty {
  display: flex;
  gap: 3px;
}
.difficulty-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-bg-muted);
}
.difficulty-dot.filled { background: var(--color-warning-500); }

/* Body: ingredients + instructions */
.recipe-body {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 0;
}

@media (max-width: 600px) {
  .recipe-body { grid-template-columns: 1fr; }
}

.recipe-ingredients {
  padding: var(--space-6);
  border-right: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
}

.recipe-instructions {
  padding: var(--space-6);
}

.recipe-section-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-black);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  margin-block-end: var(--space-4);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* Ingredients list */
.ingredient-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.ingredient-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  font-size: var(--font-size-sm);
  padding-block: var(--space-1);
  border-bottom: 1px dashed var(--color-border);
  cursor: pointer;
  transition: color var(--duration-fast);
}
.ingredient-item.checked { color: var(--color-text-muted); text-decoration: line-through; }

.ingredient-checkbox {
  width: 1rem;
  height: 1rem;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--color-border);
  background: var(--color-surface);
  flex-shrink: 0;
  margin-top: 2px;
  transition: background var(--duration-fast), border-color var(--duration-fast);
}
.ingredient-item.checked .ingredient-checkbox {
  background: var(--color-success-500);
  border-color: var(--color-success-500);
}

.ingredient-amount { font-weight: var(--font-weight-semibold); white-space: nowrap; }
.ingredient-name   { color: var(--color-text-muted); }

/* Instructions steps */
.step-list { list-style: none; padding: 0; margin: 0; counter-reset: step; }

.step-item {
  display: flex;
  gap: var(--space-4);
  padding-block: var(--space-4);
  border-bottom: 1px solid var(--color-border);
  counter-increment: step;
}
.step-item:last-child { border: none; }

.step-num {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--color-accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-sm);
  flex-shrink: 0;
}
.step-num::before { content: counter(step); }

.step-text { font-size: var(--font-size-sm); line-height: 1.7; color: var(--color-text-muted); }
.step-text strong { color: var(--color-text); font-weight: var(--font-weight-semibold); }

/* Serving adjuster */
.servings-adj {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
}

.servings-btn {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: background var(--duration-fast);
}
.servings-btn:hover { background: var(--color-bg-subtle); }

.servings-value { font-weight: var(--font-weight-bold); font-variant-numeric: tabular-nums; }
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                     PART 14 — COMPLETE                               ║
║  Chapters 193–202 | 10 new chapters | Output: css-guide-part14.md   ║
╚══════════════════════════════════════════════════════════════════════╝
```
