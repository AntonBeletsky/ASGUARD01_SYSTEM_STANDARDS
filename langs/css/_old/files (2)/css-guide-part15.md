# CSS GUIDE — PART 15
## Chapters 203–218

---

## 203. EVENT PAGE LAYOUT

```css
/* ─── Event hero ─── */
.event-hero {
  position: relative;
  min-height: 60dvh;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
}

.event-hero__bg {
  position: absolute;
  inset: 0;
  background-image: var(--event-image);
  background-size: cover;
  background-position: center;
  filter: brightness(0.5);
  scale: 1.02;
  transition: scale 8s ease-out;
}

.event-hero:hover .event-hero__bg { scale: 1; }

.event-hero__content {
  position: relative;
  z-index: 1;
  padding: var(--space-10) var(--space-8);
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--space-8);
  flex-wrap: wrap;
}

/* Event meta */
.event-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-block-end: var(--space-3);
}

.event-tag {
  padding: 0.25em 0.75em;
  background: rgba(255 255 255 / 0.15);
  color: white;
  border: 1px solid rgba(255 255 255 / 0.3);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  backdrop-filter: blur(4px);
}

.event-title {
  font-size: clamp(1.75rem, 4vw, 3.5rem);
  font-weight: var(--font-weight-black);
  color: white;
  line-height: 1.1;
  letter-spacing: -0.02em;
  text-wrap: balance;
  margin-block-end: var(--space-4);
}

.event-subtitle {
  color: rgba(255 255 255 / 0.8);
  font-size: var(--font-size-base);
  margin-block-end: var(--space-5);
}

/* Date/location chips */
.event-when-where {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}

.event-chip {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.4em 0.875em;
  background: rgba(255 255 255 / 0.12);
  color: white;
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  backdrop-filter: blur(4px);
}

/* Register panel */
.event-register {
  background: white;
  border-radius: var(--radius-2xl);
  padding: var(--space-6);
  min-width: 280px;
  box-shadow: var(--shadow-2xl);
  flex-shrink: 0;
}

.event-price {
  font-size: var(--step-3);
  font-weight: var(--font-weight-black);
  color: var(--color-text);
  margin-block-end: var(--space-1);
  font-variant-numeric: tabular-nums;
}
.event-price-note { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-block-end: var(--space-4); }

/* Seats left */
.event-seats {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--color-danger-500);
  font-weight: var(--font-weight-semibold);
  margin-block-end: var(--space-4);
}

.event-seats__bar {
  flex: 1;
  height: 4px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.event-seats__fill {
  height: 100%;
  background: var(--color-danger-500);
  width: var(--pct, 80%);
  border-radius: inherit;
}

/* Speakers grid */
.speakers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 180px), 1fr));
  gap: var(--space-5);
  padding: var(--space-8) 0;
}

.speaker-card {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.speaker-card img {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--color-border);
  transition: scale var(--duration-fast) var(--ease-bounce), border-color var(--duration-fast);
}
.speaker-card:hover img { scale: 1.05; border-color: var(--color-accent); }

.speaker-name  { font-weight: var(--font-weight-bold); font-size: var(--font-size-sm); }
.speaker-role  { font-size: var(--font-size-xs); color: var(--color-text-muted); }

/* Schedule timeline */
.schedule {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.schedule-item {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: var(--space-4);
  padding-block: var(--space-4);
  border-bottom: 1px solid var(--color-border);
  align-items: start;
}
.schedule-item:last-child { border: none; }

.schedule-time {
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
  padding-block-start: var(--space-1);
}

.schedule-talk-title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); margin-block-end: var(--space-1); }
.schedule-talk-speaker { font-size: var(--font-size-xs); color: var(--color-text-muted); }

/* Break / keynote variants */
.schedule-item--break  { background: var(--color-bg-subtle); opacity: 0.7; }
.schedule-item--keynote .schedule-talk-title { color: var(--color-accent); font-size: var(--font-size-base); }
```

---

## 204. JOB LISTING

```css
/* ─── Job board list ─── */
.job-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.job-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  display: grid;
  grid-template-columns: 3.5rem 1fr auto;
  gap: var(--space-4);
  align-items: center;
  text-decoration: none;
  color: inherit;
  transition:
    box-shadow  var(--duration-fast),
    translate   var(--duration-fast),
    border-color var(--duration-fast);
}

.job-card:hover {
  box-shadow: var(--shadow-md);
  translate: 0 -2px;
  border-color: var(--color-border-strong);
}

.job-card.featured {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 3%, var(--color-surface));
}

/* Company logo */
.job-logo {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: var(--radius-lg);
  object-fit: contain;
  background: var(--color-bg-subtle);
  padding: 4px;
  border: 1px solid var(--color-border);
  flex-shrink: 0;
}

/* Job info */
.job-info { min-width: 0; }

.job-title {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-base);
  color: var(--color-text);
  margin-block-end: var(--space-1);
}

.job-company { font-size: var(--font-size-sm); color: var(--color-text-muted); margin-block-end: var(--space-2); }

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
}

.job-tag {
  padding: 0.15em 0.5em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.job-tag--type     { background: var(--color-brand-100);   color: var(--color-brand-700); }
.job-tag--remote   { background: var(--color-success-100); color: var(--color-success-700); }
.job-tag--hybrid   { background: var(--color-warning-100); color: var(--color-warning-700); }
.job-tag--onsite   { background: var(--color-bg-muted);    color: var(--color-text-muted); }
.job-tag--salary   { background: oklch(0.93 0.05 290);     color: oklch(0.35 0.15 290); }
.job-tag--featured { background: var(--color-accent);      color: white; }

/* Salary + date */
.job-aside {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--space-2);
  flex-shrink: 0;
}

.job-salary {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-sm);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.job-posted {
  font-size: var(--font-size-xs);
  color: var(--color-text-subtle);
  white-space: nowrap;
}

/* Save button */
.job-save {
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--color-text-muted);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
}
.job-save:hover { color: var(--color-accent); scale: 1.15; }
.job-save.saved { color: var(--color-accent); }

/* ─── Job detail page ─── */
.job-detail-header {
  display: flex;
  gap: var(--space-5);
  align-items: flex-start;
  padding-block-end: var(--space-6);
  border-bottom: 1px solid var(--color-border);
  margin-block-end: var(--space-6);
  flex-wrap: wrap;
}

.job-detail-logo {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-xl);
  object-fit: contain;
  border: 1px solid var(--color-border);
  padding: 6px;
  flex-shrink: 0;
}

.job-detail-info { flex: 1; min-width: 0; }

.job-detail-title {
  font-size: var(--step-2);
  font-weight: var(--font-weight-black);
  margin-block-end: var(--space-2);
}

.job-detail-company {
  font-size: var(--font-size-lg);
  color: var(--color-accent);
  font-weight: var(--font-weight-semibold);
  margin-block-end: var(--space-3);
}

.job-detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.job-meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

/* Apply panel */
.job-apply-panel {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  position: sticky;
  top: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.job-deadline {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  text-align: center;
}
```

---

## 205. REAL ESTATE CARD

```css
/* ─── Property card ─── */
.property-card {
  background: var(--color-surface);
  border-radius: var(--radius-2xl);
  overflow: hidden;
  border: 1px solid var(--color-border);
  transition:
    box-shadow  var(--duration-normal),
    translate   var(--duration-normal);
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
}

.property-card:hover {
  box-shadow: var(--shadow-xl);
  translate: 0 -3px;
}

/* Images carousel */
.property-images {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
}

.property-images img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: scale var(--duration-slow) var(--ease-out);
}
.property-card:hover .property-images img { scale: 1.05; }

/* Image count */
.property-img-count {
  position: absolute;
  bottom: var(--space-3);
  right: var(--space-3);
  background: rgba(0 0 0 / 0.6);
  color: white;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: 0.2em 0.6em;
  border-radius: var(--radius-md);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  gap: 0.25em;
}

/* Save button */
.property-save {
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
  color: var(--color-text-muted);
  transition: scale var(--duration-fast) var(--ease-bounce), color var(--duration-fast);
}
.property-save:hover { scale: 1.1; color: var(--color-danger-500); }
.property-save.saved { color: var(--color-danger-500); }

/* Status badge */
.property-status {
  position: absolute;
  top: var(--space-3);
  left: var(--space-3);
  padding: 0.2em 0.6em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.property-status--new    { background: var(--color-success-500); color: white; }
.property-status--sale   { background: var(--color-accent); color: white; }
.property-status--rent   { background: oklch(0.5 0.2 300); color: white; }
.property-status--sold   { background: var(--color-neutral-600); color: white; }
.property-status--pending{ background: var(--color-warning-500); color: white; }

/* Card body */
.property-body { padding: var(--space-4); flex: 1; display: flex; flex-direction: column; gap: var(--space-3); }

.property-price {
  font-size: var(--step-1);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
}
.property-price-note { font-size: var(--font-size-xs); color: var(--color-text-muted); font-weight: normal; }

.property-address { font-size: var(--font-size-sm); color: var(--color-text-muted); }

/* Stats row */
.property-stats {
  display: flex;
  gap: var(--space-4);
  font-size: var(--font-size-sm);
  padding-block-start: var(--space-3);
  border-top: 1px solid var(--color-border);
  color: var(--color-text-muted);
}

.property-stat {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-weight: var(--font-weight-medium);
}

.property-stat strong { color: var(--color-text); }

/* Agent info */
.property-agent {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding-block-start: var(--space-3);
  border-top: 1px solid var(--color-border);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.property-agent img {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  object-fit: cover;
}

.property-agent-name { font-weight: var(--font-weight-medium); color: var(--color-text); }

/* Map view toggle */
.property-view-toggle {
  display: flex;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.view-btn {
  flex: 1;
  padding: 0.5rem;
  border: none;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.view-btn.active { background: var(--color-accent); color: white; }
.view-btn:not(:last-child) { border-right: 1px solid var(--color-border); }
```

---

## 206. MEDICAL / HEALTH UI

```css
/* ─── Health dashboard ─── */
.health-metric {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  position: relative;
  overflow: hidden;
}

/* Colored accent stripe */
.health-metric::before {
  content: '';
  position: absolute;
  inset-block: 0;
  inset-inline-start: 0;
  width: 4px;
  background: var(--metric-color, var(--color-accent));
  border-radius: 4px 0 0 4px;
}

.health-metric__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
}

.health-metric__icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-xl);
  background: color-mix(in srgb, var(--metric-color, var(--color-accent)) 12%, transparent);
  color: var(--metric-color, var(--color-accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.health-metric__label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
}

.health-metric__value {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: var(--font-weight-black);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.health-metric__unit {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-normal);
  color: var(--color-text-muted);
}

/* Normal range indicator */
.health-range {
  position: relative;
  height: 6px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  margin-block-start: var(--space-2);
}

.health-range__normal {
  position: absolute;
  inset-block: 0;
  left: var(--range-start, 20%);
  width: calc(var(--range-end, 80%) - var(--range-start, 20%));
  background: var(--color-success-300);
  border-radius: inherit;
}

.health-range__cursor {
  position: absolute;
  top: 50%;
  left: var(--cursor-pos, 50%);
  translate: -50% -50%;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--metric-color, var(--color-accent));
  border: 2px solid white;
  box-shadow: var(--shadow-sm);
  z-index: 1;
}

/* Status */
.health-status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: 0.2em 0.6em;
  border-radius: var(--radius-full);
}

.health-status--normal { background: var(--color-success-100); color: var(--color-success-700); }
.health-status--low    { background: var(--color-brand-100);   color: var(--color-brand-700); }
.health-status--high   { background: var(--color-danger-100);  color: var(--color-danger-700); }
.health-status--watch  { background: var(--color-warning-100); color: var(--color-warning-700); }

/* Medication schedule */
.med-schedule {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.med-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: background var(--duration-fast);
}

.med-item.taken {
  background: var(--color-success-100);
  border-color: var(--color-success-300);
  opacity: 0.7;
}

.med-icon {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: var(--radius-lg);
  background: var(--color-brand-100);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.med-name  { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.med-dose  { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.med-time  { margin-inline-start: auto; font-size: var(--font-size-xs); font-variant-numeric: tabular-nums; color: var(--color-text-muted); white-space: nowrap; }

/* Appointment card */
.appointment {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  align-items: center;
}

.appointment-date {
  width: 3.5rem;
  text-align: center;
  flex-shrink: 0;
}

.appointment-day   { font-size: var(--step-1); font-weight: var(--font-weight-black); line-height: 1; }
.appointment-month { font-size: var(--font-size-xs); text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-text-muted); }

.appointment-divider {
  width: 1px;
  height: 3rem;
  background: var(--color-border);
  flex-shrink: 0;
}

.appointment-info  { flex: 1; min-width: 0; }
.appointment-title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.appointment-meta  { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-block-start: var(--space-1); }

/* Vitals chart placeholder */
.vitals-chart { position: relative; width: 100%; height: 120px; }
.vitals-chart svg { width: 100%; height: 100%; }

.vitals-line {
  fill: none;
  stroke: var(--metric-color, var(--color-accent));
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.vitals-area {
  fill: color-mix(in srgb, var(--metric-color, var(--color-accent)) 10%, transparent);
}
```

---

## 207. DASHBOARD DARK THEME

```css
/* ─── Complete dark dashboard ─── */
.dark-dash {
  --dd-bg:         #0d1117;
  --dd-surface:    #161b22;
  --dd-surface-2:  #21262d;
  --dd-border:     #30363d;
  --dd-text:       #e6edf3;
  --dd-muted:      #8b949e;
  --dd-accent:     #58a6ff;
  --dd-success:    #3fb950;
  --dd-warning:    #d29922;
  --dd-danger:     #f85149;

  background: var(--dd-bg);
  color: var(--dd-text);
  font-family: var(--font-sans);
  min-height: 100dvh;
}

/* Dark surface */
.dd-card {
  background: var(--dd-surface);
  border: 1px solid var(--dd-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
}

.dd-card--raised {
  background: var(--dd-surface-2);
}

/* Dark stat card */
.dd-stat {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-5);
  background: var(--dd-surface);
  border: 1px solid var(--dd-border);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}

/* Glow accent on top */
.dd-stat::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(
    to right,
    transparent,
    var(--dd-stat-color, var(--dd-accent)),
    transparent
  );
}

.dd-stat__label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--dd-muted);
}

.dd-stat__value {
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
  color: var(--dd-text);
  line-height: 1;
}

.dd-stat__change {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
}

.dd-stat__change--up   { color: var(--dd-success); }
.dd-stat__change--down { color: var(--dd-danger); }

/* Dark table */
.dd-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-sm);
}

.dd-table th {
  padding: var(--space-2) var(--space-3);
  text-align: start;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  color: var(--dd-muted);
  border-bottom: 1px solid var(--dd-border);
}

.dd-table td {
  padding: var(--space-3);
  border-bottom: 1px solid color-mix(in srgb, var(--dd-border) 50%, transparent);
  color: var(--dd-text);
  vertical-align: middle;
}

.dd-table tbody tr:hover td { background: color-mix(in srgb, var(--dd-accent) 4%, transparent); }

/* Dark badge */
.dd-badge {
  display: inline-flex;
  padding: 0.15em 0.5em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  border: 1px solid;
}

.dd-badge--success { background: rgba(63 185 80 / 0.1); border-color: rgba(63 185 80 / 0.3); color: var(--dd-success); }
.dd-badge--danger  { background: rgba(248 81 73 / 0.1); border-color: rgba(248 81 73 / 0.3); color: var(--dd-danger); }
.dd-badge--warning { background: rgba(210 153 34 / 0.1);border-color: rgba(210 153 34 / 0.3);color: var(--dd-warning); }
.dd-badge--info    { background: rgba(88 166 255 / 0.1);border-color: rgba(88 166 255 / 0.3);color: var(--dd-accent); }

/* Dark button */
.dd-btn {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--dd-border);
  background: var(--dd-surface-2);
  color: var(--dd-text);
  font: inherit;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: background var(--duration-fast), border-color var(--duration-fast);
}
.dd-btn:hover { background: var(--dd-surface); border-color: var(--dd-accent); }
.dd-btn--primary { background: var(--dd-accent); color: var(--dd-bg); border-color: var(--dd-accent); }
.dd-btn--primary:hover { filter: brightness(1.1); }

/* Dark input */
.dd-input {
  background: var(--dd-bg);
  border: 1px solid var(--dd-border);
  border-radius: var(--radius-md);
  color: var(--dd-text);
  padding: 0.5rem 0.75rem;
  font: inherit;
  font-size: var(--font-size-sm);
  outline: none;
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
}
.dd-input:focus {
  border-color: var(--dd-accent);
  box-shadow: 0 0 0 3px rgba(88 166 255 / 0.15);
}
.dd-input::placeholder { color: var(--dd-muted); }
```

---

## 208. HOTKEY / KEYBOARD SHORTCUT HINTS

```css
/* ─── Keyboard shortcut hints system ─── */

/* KBD element styling */
kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.15em 0.45em;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-bottom-width: 2px;
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.8em;
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  box-shadow: 0 1px 0 var(--color-border);
  white-space: nowrap;
  user-select: none;
  line-height: 1.4;
}

/* Dark kbd */
.dark-theme kbd {
  background: #2d2d2d;
  border-color: #555;
  color: #ccc;
  box-shadow: 0 1px 0 #555;
}

/* Key combination */
.shortcut {
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
}

.shortcut .plus {
  color: var(--color-text-subtle);
  font-size: 0.75em;
}

/* Shortcut hint in UI element */
[data-shortcut]::after {
  content: attr(data-shortcut);
  display: inline-flex;
  align-items: center;
  margin-inline-start: auto;
  font-family: var(--font-mono);
  font-size: 0.75em;
  color: var(--color-text-subtle);
  background: var(--color-bg-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 0.1em 0.4em;
}

/* Shortcut tooltip on hover */
.shortcut-tooltip {
  position: relative;
}

.shortcut-tooltip::after {
  content: attr(data-key);
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  translate: -50% 0;
  background: var(--color-neutral-900);
  color: white;
  font-size: var(--font-size-xs);
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-md);
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-fast);
  z-index: var(--z-tooltip);
}

.shortcut-tooltip:hover::after { opacity: 1; }

/* ─── Hotkey legend panel ─── */
.hotkey-legend {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  max-width: 560px;
}

.hotkey-legend__title {
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-4);
  font-size: var(--font-size-base);
}

.hotkey-section { margin-block-end: var(--space-5); }

.hotkey-section__title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  margin-block-end: var(--space-3);
  padding-block-end: var(--space-2);
  border-bottom: 1px solid var(--color-border);
}

.hotkey-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-block: var(--space-2);
  font-size: var(--font-size-sm);
}

.hotkey-desc { color: var(--color-text-muted); }

.hotkey-keys {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

/* Key pressed state animation */
.key-hint {
  transition: all 0.1s;
}

.key-hint.pressed {
  background: var(--color-accent);
  border-color: var(--color-accent-hover);
  color: white;
  scale: 0.92;
  box-shadow: none;
}
```

---

## 209. CSS DATA ATTRIBUTES PATTERNS

```css
/* ─── Data attribute driven styling ─── */

/* ── State management ── */
[data-state="loading"]  { cursor: wait; opacity: 0.7; pointer-events: none; }
[data-state="disabled"] { opacity: 0.4; cursor: not-allowed; pointer-events: none; }
[data-state="error"]    { border-color: var(--color-danger-500) !important; }
[data-state="success"]  { border-color: var(--color-success-500) !important; }

/* ── Size variants ── */
[data-size="xs"] { --component-size: 1.5rem; font-size: var(--font-size-xs); }
[data-size="sm"] { --component-size: 2rem;   font-size: var(--font-size-sm); }
[data-size="md"] { --component-size: 2.5rem; font-size: var(--font-size-base); }
[data-size="lg"] { --component-size: 3rem;   font-size: var(--font-size-lg); }
[data-size="xl"] { --component-size: 3.5rem; font-size: var(--font-size-xl); }

/* ── Color variants ── */
[data-color="primary"]  { --variant-color: var(--color-accent); }
[data-color="success"]  { --variant-color: var(--color-success-500); }
[data-color="warning"]  { --variant-color: var(--color-warning-500); }
[data-color="danger"]   { --variant-color: var(--color-danger-500); }
[data-color="neutral"]  { --variant-color: var(--color-neutral-500); }

/* ── Layout variants ── */
[data-layout="grid"]   { display: grid; }
[data-layout="flex"]   { display: flex; }
[data-layout="stack"]  { display: flex; flex-direction: column; }
[data-layout="cluster"]{ display: flex; flex-wrap: wrap; }

/* ── Alignment ── */
[data-align="start"]   { align-items: flex-start; }
[data-align="center"]  { align-items: center; }
[data-align="end"]     { align-items: flex-end; }
[data-justify="start"]  { justify-content: flex-start; }
[data-justify="center"] { justify-content: center; }
[data-justify="between"]{ justify-content: space-between; }
[data-justify="end"]    { justify-content: flex-end; }

/* ── Spacing via data attributes ── */
[data-gap="1"]  { gap: var(--space-1); }
[data-gap="2"]  { gap: var(--space-2); }
[data-gap="4"]  { gap: var(--space-4); }
[data-gap="6"]  { gap: var(--space-6); }
[data-gap="8"]  { gap: var(--space-8); }

[data-p="2"]  { padding: var(--space-2); }
[data-p="4"]  { padding: var(--space-4); }
[data-p="6"]  { padding: var(--space-6); }
[data-p="8"]  { padding: var(--space-8); }

/* ── Position ── */
[data-position="top"]    { top: 0; }
[data-position="bottom"] { bottom: 0; }
[data-position="left"]   { left: 0; }
[data-position="right"]  { right: 0; }

/* ── Animation trigger ── */
[data-animate="fade-in"] { animation: fadeIn var(--duration-normal) var(--ease-out); }
[data-animate="slide-up"]{ animation: slideUp var(--duration-normal) var(--ease-out); }
[data-animate="bounce"]  { animation: bounce 0.5s var(--ease-bounce); }
[data-animate="shake"]   { animation: shake 0.4s var(--ease-out); }

/* ── Theme data attributes ── */
[data-theme="dark"]  { color-scheme: dark; }
[data-theme="light"] { color-scheme: light; }

/* ── Interactive data states ── */
[data-expanded="true"]  .expand-icon { rotate: 180deg; }
[data-selected="true"]  { background: color-mix(in srgb, var(--color-accent) 10%, transparent); }
[data-current="page"]   { font-weight: var(--font-weight-semibold); color: var(--color-accent); }
[data-pressed="true"]   { scale: 0.97; }

/* ── Grid cols via data ── */
[data-cols="1"]  { grid-template-columns: repeat(1, 1fr); }
[data-cols="2"]  { grid-template-columns: repeat(2, 1fr); }
[data-cols="3"]  { grid-template-columns: repeat(3, 1fr); }
[data-cols="4"]  { grid-template-columns: repeat(4, 1fr); }
[data-cols="auto"]{ grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr)); }

/* ── Border radius ── */
[data-radius="none"] { border-radius: 0; }
[data-radius="sm"]   { border-radius: var(--radius-sm); }
[data-radius="md"]   { border-radius: var(--radius-md); }
[data-radius="lg"]   { border-radius: var(--radius-lg); }
[data-radius="xl"]   { border-radius: var(--radius-xl); }
[data-radius="full"] { border-radius: var(--radius-full); }

/* ── Shadow ── */
[data-shadow="none"]{ box-shadow: none; }
[data-shadow="sm"]  { box-shadow: var(--shadow-sm); }
[data-shadow="md"]  { box-shadow: var(--shadow-md); }
[data-shadow="lg"]  { box-shadow: var(--shadow-lg); }
[data-shadow="xl"]  { box-shadow: var(--shadow-xl); }

/* ── Visibility ── */
[data-visible="false"]  { opacity: 0; pointer-events: none; }
[data-visible="true"]   { opacity: 1; pointer-events: auto; }
[data-hidden="true"]    { display: none !important; }
[data-sticky="true"]    { position: sticky; }
[data-fixed="true"]     { position: fixed; }
```

---

## 210. GLASSMORPHISM ADVANCED

```css
/* ─── Advanced glass components ─── */

/* Base glass mixin variables */
:root {
  --glass-blur:   20px;
  --glass-sat:    180%;
  --glass-bright: 110%;
  --glass-bg:     rgba(255 255 255 / 0.1);
  --glass-border: rgba(255 255 255 / 0.2);
  --glass-shadow: 0 8px 32px rgba(0 0 0 / 0.2);
}

/* Light glass */
.glass-light {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-sat)) brightness(var(--glass-bright));
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-sat)) brightness(var(--glass-bright));
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow), inset 0 1px 0 rgba(255 255 255 / 0.3);
}

/* Dark glass */
.glass-dark {
  background: rgba(0 0 0 / 0.2);
  backdrop-filter: blur(16px) saturate(150%);
  -webkit-backdrop-filter: blur(16px) saturate(150%);
  border: 1px solid rgba(255 255 255 / 0.08);
  box-shadow: 0 8px 32px rgba(0 0 0 / 0.4), inset 0 1px 0 rgba(255 255 255 / 0.08);
}

/* Colored glass */
.glass-color {
  background: color-mix(in srgb, var(--glass-tint, var(--color-accent)) 15%, transparent);
  backdrop-filter: blur(12px) saturate(160%);
  -webkit-backdrop-filter: blur(12px) saturate(160%);
  border: 1px solid color-mix(in srgb, var(--glass-tint, var(--color-accent)) 30%, transparent);
  box-shadow: 0 8px 24px color-mix(in srgb, var(--glass-tint, var(--color-accent)) 20%, transparent);
}

/* Glass card */
.glass-card {
  border-radius: var(--radius-2xl);
  padding: var(--space-6);
  overflow: hidden;
  position: relative;
}

/* Inner light refraction effect */
.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    to right,
    transparent,
    rgba(255 255 255 / 0.4),
    transparent
  );
  pointer-events: none;
}

/* Corner highlight */
.glass-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 30%;
  height: 30%;
  background: radial-gradient(circle at top left, rgba(255 255 255 / 0.15), transparent 70%);
  pointer-events: none;
}

/* Glass input */
.glass-input {
  background: rgba(255 255 255 / 0.08);
  border: 1px solid rgba(255 255 255 / 0.15);
  border-radius: var(--radius-lg);
  color: white;
  padding: 0.625rem 1rem;
  font: inherit;
  font-size: var(--font-size-sm);
  outline: none;
  backdrop-filter: blur(4px);
  transition: border-color var(--duration-fast), background var(--duration-fast);
}
.glass-input::placeholder { color: rgba(255 255 255 / 0.4); }
.glass-input:focus {
  border-color: rgba(255 255 255 / 0.4);
  background: rgba(255 255 255 / 0.12);
}

/* Glass button */
.glass-btn {
  background: rgba(255 255 255 / 0.12);
  border: 1px solid rgba(255 255 255 / 0.2);
  border-radius: var(--radius-lg);
  color: white;
  padding: 0.5rem 1.25rem;
  font: inherit;
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  backdrop-filter: blur(4px);
  transition:
    background  var(--duration-fast),
    border-color var(--duration-fast),
    scale       var(--duration-fast) var(--ease-bounce);
}
.glass-btn:hover {
  background: rgba(255 255 255 / 0.2);
  border-color: rgba(255 255 255 / 0.35);
  scale: 1.02;
}

/* Frosted glass navigation */
.glass-nav {
  position: fixed;
  top: 0;
  inset-inline: 0;
  z-index: var(--z-sticky);
  padding: var(--space-3) var(--space-6);
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.glass-nav::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255 255 255 / 0.08);
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(255 255 255 / 0.12);
  pointer-events: none;
}

.glass-nav > * { position: relative; z-index: 1; }

/* Glass modal */
.glass-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0 0 0 / 0.3);
  backdrop-filter: blur(8px);
  z-index: var(--z-modal);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
}

.glass-modal {
  background: rgba(255 255 255 / 0.12);
  backdrop-filter: blur(40px) saturate(200%);
  border: 1px solid rgba(255 255 255 / 0.2);
  border-radius: var(--radius-3xl);
  box-shadow:
    0 20px 60px rgba(0 0 0 / 0.4),
    inset 0 1px 0 rgba(255 255 255 / 0.3);
  padding: var(--space-8);
  width: 100%;
  max-width: 480px;
  color: white;
  animation: glass-modal-in 0.3s var(--ease-bounce);
}

@keyframes glass-modal-in {
  from { opacity: 0; scale: 0.93; translate: 0 16px; }
}

/* Glass sidebar */
.glass-sidebar {
  position: fixed;
  inset-block: 0;
  inset-inline-start: 0;
  width: 260px;
  padding: var(--space-6) var(--space-4);
  background: rgba(255 255 255 / 0.06);
  backdrop-filter: blur(30px) saturate(180%);
  border-right: 1px solid rgba(255 255 255 / 0.1);
  z-index: var(--z-fixed);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

/* Glass nav link */
.glass-nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.625rem 0.875rem;
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: rgba(255 255 255 / 0.7);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.glass-nav-link:hover {
  background: rgba(255 255 255 / 0.1);
  color: white;
}
.glass-nav-link.active {
  background: rgba(255 255 255 / 0.15);
  color: white;
  font-weight: var(--font-weight-semibold);
}
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                     PART 15 — COMPLETE                               ║
║  Chapters 203–210 | 8 new chapters | Output: css-guide-part15.md    ║
╚══════════════════════════════════════════════════════════════════════╝
```
