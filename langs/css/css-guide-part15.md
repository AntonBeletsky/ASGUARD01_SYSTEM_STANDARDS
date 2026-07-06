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

## 211. POPOVER API + CSS

```css
/* ─── Base popover reset ───
   [popover] and <dialog> render in the browser's top layer — z-index
   tokens like --z-modal / --z-popover do not apply to them and are not needed here. */
[popover] {
  margin: auto;
  padding: 0;
  border: none;
  inset: 0;
  max-width: min(90vw, 360px);
  background: var(--color-surface);
  color: var(--color-text);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-2xl);
  opacity: 0;
  scale: 0.95;
  transition:
    opacity  var(--duration-normal) var(--ease-out),
    scale    var(--duration-normal) var(--ease-out),
    display  var(--duration-normal) allow-discrete,
    overlay  var(--duration-normal) allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  scale: 1;
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
    scale: 0.95;
  }
}

/* Backdrop dims the page behind an open [popover="auto"] */
[popover]::backdrop {
  background: rgb(0 0 0 / 0);
  transition: background var(--duration-normal) allow-discrete;
}
[popover]:popover-open::backdrop {
  background: rgb(0 0 0 / 0.35);
}

/* ─── Popover menu, anchored to its trigger button ─── */
.popover-menu-trigger {
  anchor-name: --menu-trigger;
}

.popover-menu {
  padding: var(--space-2);
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 200px;
  max-width: 260px;
  position-anchor: --menu-trigger;
  position-area: bottom span-right;
  position-try-fallbacks: flip-block, flip-inline;
  margin-block-start: var(--space-2);
}

.popover-menu-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-lg);
  font: inherit;
  font-size: var(--font-size-sm);
  color: var(--color-text);
  background: none;
  border: none;
  text-align: start;
  cursor: pointer;
  transition: background var(--duration-fast);
}
.popover-menu-item:hover,
.popover-menu-item:focus-visible { background: var(--color-bg-subtle); }
.popover-menu-item--danger { color: var(--color-danger-500); }

.popover-menu-divider {
  height: 1px;
  background: var(--color-border);
  margin-block: var(--space-1);
}

/* ─── Lightweight anchored tooltip (auto popover) ─── */
.popover-tooltip-trigger { anchor-name: --tooltip-trigger; }

[popover="auto"].popover-tooltip {
  max-width: 220px;
  padding: var(--space-2) var(--space-3);
  background: var(--color-neutral-900);
  color: white;
  font-size: var(--font-size-xs);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  position-anchor: --tooltip-trigger;
  position-area: top;
  margin-block-end: var(--space-2);
}

/* ─── Popover used as a combobox listbox, matching trigger width ─── */
.popover-listbox {
  position-anchor: --combo-trigger;
  position-area: bottom span-right;
  width: anchor-size(width);
  max-height: 260px;
  overflow-y: auto;
  padding: var(--space-1);
}

.popover-listbox [role="option"] {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  cursor: pointer;
}
.popover-listbox [role="option"]:hover,
.popover-listbox [role="option"][aria-selected="true"] {
  background: color-mix(in srgb, var(--color-accent) 10%, transparent);
}

/* ─── Fallback for browsers without Popover API support ─── */
@supports not selector(:popover-open) {
  [popover] { display: none; }
  [popover].is-open-fallback {
    display: block;
    position: fixed;
    inset: 0;
    margin: auto;
  }
}
```

---

## 212. NATIVE `<DIALOG>` — DEEP DIVE

```css
/* ─── Dialog reset ─── */
dialog {
  margin: auto;
  padding: 0;
  border: none;
  border-radius: var(--radius-2xl);
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: var(--shadow-2xl);
  max-width: min(90vw, 480px);
  width: 100%;
  opacity: 0;
  translate: 0 24px;
  transition:
    opacity   var(--duration-normal) var(--ease-out),
    translate var(--duration-normal) var(--ease-out),
    overlay   var(--duration-normal) allow-discrete,
    display   var(--duration-normal) allow-discrete;
}

dialog[open] {
  opacity: 1;
  translate: 0 0;
}

@starting-style {
  dialog[open] {
    opacity: 0;
    translate: 0 24px;
  }
}

/* ::backdrop is only rendered for dialogs opened via showModal() */
dialog::backdrop {
  background: rgb(15 15 20 / 0);
  backdrop-filter: blur(0px);
  transition:
    background      var(--duration-normal) allow-discrete,
    backdrop-filter var(--duration-normal) allow-discrete;
}
dialog[open]::backdrop {
  background: rgb(15 15 20 / 0.5);
  backdrop-filter: blur(2px);
}
@starting-style {
  dialog[open]::backdrop {
    background: rgb(15 15 20 / 0);
    backdrop-filter: blur(0px);
  }
}

/* ─── Anatomy ─── */
.dialog-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-6) var(--space-6) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}

.dialog-title { font-size: var(--font-size-lg); font-weight: var(--font-weight-bold); }
.dialog-description { font-size: var(--font-size-sm); color: var(--color-text-muted); margin-block-start: var(--space-1); }

.dialog-close {
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-lg);
  border: none;
  background: none;
  color: var(--color-text-muted);
  cursor: pointer;
  flex-shrink: 0;
  transition: background var(--duration-fast);
}
.dialog-close:hover { background: var(--color-bg-subtle); }

.dialog-body { padding: var(--space-6); overflow-y: auto; }

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-6) var(--space-6);
}

/* ─── Non-modal dialog (.show(), no ::backdrop rendered by the browser) ─── */
dialog.dialog--nonmodal[open] {
  position: fixed;
  inset-block-start: var(--space-6);
  inset-inline-end: var(--space-6);
  margin: 0;
  box-shadow: var(--shadow-xl);
}

/* ─── Full-screen sheet variant (mobile) ─── */
dialog.dialog--sheet {
  max-width: none;
  width: 100%;
  margin-block-end: 0;
  margin-inline: 0;
  border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
  translate: 0 100%;
}
dialog.dialog--sheet[open] { translate: 0 0; }
@starting-style {
  dialog.dialog--sheet[open] { translate: 0 100%; }
}

/* ─── Alert / destructive-confirm variant ─── */
.dialog--alert .dialog-header { border-bottom: none; padding-block-end: 0; }
.dialog--alert .dialog-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: var(--color-danger-100);
  color: var(--color-danger-500);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-block-end: var(--space-4);
  font-size: 1.25rem;
}
```

---

## 213. TOAST / SNACKBAR — NOTIFICATION QUEUE

```css
/* ─── Toast viewport: fixed stack container ─── */
.toast-viewport {
  position: fixed;
  inset-block-end: var(--space-6);
  inset-inline-end: var(--space-6);
  z-index: var(--z-toast);
  display: flex;
  flex-direction: column-reverse;
  gap: var(--space-3);
  width: min(360px, calc(100vw - var(--space-8)));
  pointer-events: none;
}

/* ─── Toast card ─── */
.toast {
  pointer-events: auto;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: var(--space-3);
  align-items: start;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
  animation: toast-in var(--duration-slow) var(--ease-bounce);
}

.toast.is-leaving {
  animation: toast-out var(--duration-normal) var(--ease-in) forwards;
}

@keyframes toast-in {
  from { opacity: 0; translate: 0 12px; scale: 0.95; }
}
@keyframes toast-out {
  to { opacity: 0; translate: 110% 0; }
}

/* Icon by variant */
.toast-icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
  font-size: 0.8rem;
}
.toast--success .toast-icon { background: var(--color-success-500); }
.toast--danger  .toast-icon { background: var(--color-danger-500); }
.toast--warning .toast-icon { background: var(--color-warning-500); }
.toast--info    .toast-icon { background: var(--color-brand-500); }

.toast-content { min-width: 0; }
.toast-title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.toast-message { font-size: var(--font-size-sm); color: var(--color-text-muted); margin-block-start: 0.125rem; }

.toast-action {
  display: inline-block;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-accent);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-block-start: var(--space-2);
}

.toast-close {
  width: 1.25rem;
  height: 1.25rem;
  border: none;
  background: none;
  color: var(--color-text-subtle);
  cursor: pointer;
  flex-shrink: 0;
}

/* Auto-dismiss progress bar along the bottom edge */
.toast-timer {
  position: absolute;
  inset-block-end: 0;
  inset-inline-start: 0;
  height: 3px;
  background: var(--color-accent);
  width: 100%;
  transform-origin: left;
  animation: toast-countdown var(--toast-duration, 5s) linear forwards;
}
@keyframes toast-countdown {
  to { scale: 0 1; }
}
.toast:hover .toast-timer,
.toast:focus-within .toast-timer { animation-play-state: paused; }

/* Depth preview when 3+ toasts queue up behind the front card */
.toast-viewport[data-stacked="true"] .toast:not(:first-child) {
  scale: calc(1 - var(--stack-index, 1) * 0.05);
  translate: 0 calc(var(--stack-index, 1) * -8px);
  opacity: calc(1 - var(--stack-index, 1) * 0.3);
}
```

---

## 214. PASSWORD & OTP INPUT UI

```css
/* ─── Password field with show/hide toggle ─── */
.password-field {
  position: relative;
  display: flex;
  align-items: center;
}

.password-field input {
  width: 100%;
  padding: 0.625rem var(--space-10) 0.625rem var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  font: inherit;
  background: var(--color-surface);
  transition: border-color var(--duration-fast);
}
.password-field input:focus-visible {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 20%, transparent);
}

.password-toggle {
  position: absolute;
  inset-inline-end: var(--space-2);
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: var(--radius-md);
}
.password-toggle:hover { color: var(--color-text); background: var(--color-bg-subtle); }

/* ─── Strength meter ─── */
.password-strength {
  display: flex;
  gap: var(--space-1);
  margin-block-start: var(--space-2);
}

.password-strength__segment {
  height: 4px;
  flex: 1;
  border-radius: var(--radius-full);
  background: var(--color-bg-muted);
  transition: background var(--duration-normal);
}

.password-strength[data-level="1"] .password-strength__segment:nth-child(-n+1) { background: var(--color-danger-500); }
.password-strength[data-level="2"] .password-strength__segment:nth-child(-n+2) { background: var(--color-warning-500); }
.password-strength[data-level="3"] .password-strength__segment:nth-child(-n+3) { background: var(--color-brand-500); }
.password-strength[data-level="4"] .password-strength__segment:nth-child(-n+4) { background: var(--color-success-500); }

.password-strength__label { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-block-start: var(--space-1); }

/* ─── Requirement checklist ─── */
.password-requirements {
  list-style: none;
  padding: 0;
  margin-block-start: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}
.password-requirements li {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}
.password-requirements li.met { color: var(--color-success-600); }
.password-requirements li.met::before { content: '✓'; font-weight: var(--font-weight-bold); }
.password-requirements li:not(.met)::before { content: '○'; }

/* ─── OTP / verification-code input ─── */
.otp-input {
  display: flex;
  gap: var(--space-2);
}

.otp-input__cell {
  width: 3rem;
  height: 3.5rem;
  text-align: center;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  font-family: var(--font-mono);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
}
.otp-input__cell:focus-visible {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 20%, transparent);
}
.otp-input__cell:not(:placeholder-shown) { border-color: var(--color-border-strong); }

.otp-input__cell.error { border-color: var(--color-danger-500); animation: otp-shake 0.3s; }
@keyframes otp-shake {
  25% { translate: -4px 0; }
  75% { translate: 4px 0; }
}
.otp-input__cell.success { border-color: var(--color-success-500); }

/* Visual separator between digit groups, e.g. a 3-3 layout */
.otp-input__sep { align-self: center; color: var(--color-text-subtle); font-weight: var(--font-weight-bold); }

.otp-resend { font-size: var(--font-size-sm); color: var(--color-text-muted); margin-block-start: var(--space-3); }
.otp-resend button {
  background: none;
  border: none;
  color: var(--color-accent);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  padding: 0;
}
.otp-resend button:disabled { color: var(--color-text-subtle); cursor: not-allowed; }
```

---

## 215. STICKY / FROZEN TABLE HEADERS & COLUMNS

```css
/* ─── Scroll container ─── */
.data-table-scroll {
  overflow: auto;
  max-height: 480px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
}

.data-table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  font-size: var(--font-size-sm);
}

/* ─── Sticky header row ─── */
.data-table thead th {
  position: sticky;
  top: 0;
  z-index: var(--z-raised);
  background: var(--color-bg-subtle);
  text-align: start;
  padding: var(--space-3) var(--space-4);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
}

/* Shadow appears once body content has scrolled beneath the sticky header */
.data-table-scroll[data-scrolled="true"] thead th {
  box-shadow: 0 1px 0 var(--color-border-strong), 0 4px 6px -4px rgb(0 0 0 / 0.15);
}

.data-table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
}
.data-table tr:last-child td { border-bottom: none; }

/* ─── Frozen first column ───
   background must be set explicitly (not left transparent), otherwise
   scrolling body content shows through underneath the frozen cell. */
.data-table .col-frozen {
  position: sticky;
  inset-inline-start: 0;
  z-index: var(--z-base);
  background: inherit;
}
.data-table thead .col-frozen { z-index: calc(var(--z-raised) + 1); background: var(--color-bg-subtle); }

.data-table-scroll[data-scrolled-x="true"] .col-frozen {
  box-shadow: 4px 0 6px -4px rgb(0 0 0 / 0.15);
}

/* ─── Frozen last column (e.g. row actions) ─── */
.data-table .col-frozen-end {
  position: sticky;
  inset-inline-end: 0;
  background: inherit;
  text-align: end;
}
.data-table-scroll[data-scrolled-x-end="true"] .col-frozen-end {
  box-shadow: -4px 0 6px -4px rgb(0 0 0 / 0.15);
}

/* ─── Sticky footer (totals row) ─── */
.data-table tfoot td {
  position: sticky;
  bottom: 0;
  background: var(--color-bg-subtle);
  font-weight: var(--font-weight-semibold);
  border-top: 2px solid var(--color-border-strong);
  border-bottom: none;
}

/* Hover state must repaint frozen cells too, or they'll look "stuck" mid-highlight */
.data-table tbody tr:hover td,
.data-table tbody tr:hover .col-frozen,
.data-table tbody tr:hover .col-frozen-end { background: var(--color-bg-subtle); }

/* Zebra striping stays compatible with frozen columns via `background: inherit` above */
.data-table--striped tbody tr:nth-child(even) td { background: var(--color-bg-subtle); }
```

---

## 216. ACTIVITY / PROGRESS RING

```css
/* ─── Single ring via conic-gradient (CSS-only, no SVG) ─── */
.progress-ring {
  --ring-size: 120px;
  --ring-thickness: 10px;
  --ring-value: 65; /* 0–100 */
  --ring-color: var(--color-accent);
  width: var(--ring-size);
  height: var(--ring-size);
  border-radius: 50%;
  background: conic-gradient(var(--ring-color) calc(var(--ring-value) * 1%), var(--color-bg-muted) 0);
  display: grid;
  place-items: center;
  transition: background 0.6s var(--ease-out);
}

/* Punch a hole in the middle to turn the filled disc into a ring */
.progress-ring::before {
  content: '';
  grid-area: 1 / 1;
  width: calc(100% - var(--ring-thickness) * 2);
  height: calc(100% - var(--ring-thickness) * 2);
  border-radius: 50%;
  background: var(--color-surface);
}

.progress-ring__label {
  grid-area: 1 / 1;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
}

.progress-ring--sm { --ring-size: 32px; --ring-thickness: 4px; }
.progress-ring--sm .progress-ring__label { font-size: var(--font-size-xs); }

.progress-ring[data-complete="true"] { --ring-color: var(--color-success-500); }

/* ─── SVG variant — smoother animation via stroke-dashoffset ─── */
.progress-ring-svg { width: 120px; height: 120px; rotate: -90deg; }
.progress-ring-svg circle { fill: none; stroke-width: 10; }
.progress-ring-svg .track { stroke: var(--color-bg-muted); }
.progress-ring-svg .fill {
  stroke: var(--color-accent);
  stroke-linecap: round;
  stroke-dasharray: var(--ring-circumference, 314);
  stroke-dashoffset: calc(var(--ring-circumference, 314) * (1 - var(--ring-value, 0.65)));
  transition: stroke-dashoffset 0.8s var(--ease-out);
}

/* ─── Multi-ring activity dashboard (concentric rings, Apple-Watch style) ─── */
.activity-rings { position: relative; width: 160px; height: 160px; }
.activity-rings svg { width: 100%; height: 100%; rotate: -90deg; }
.activity-rings circle { fill: none; stroke-linecap: round; transition: stroke-dashoffset 0.8s var(--ease-out); }
.activity-rings .ring-track { stroke: color-mix(in srgb, currentColor 15%, transparent); }
.activity-rings .ring-move     { stroke: var(--color-danger-500); }
.activity-rings .ring-exercise { stroke: var(--color-success-500); }
.activity-rings .ring-stand    { stroke: var(--color-brand-500); }

.activity-legend { display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--font-size-sm); }
.activity-legend-item { display: flex; align-items: center; gap: var(--space-2); }
.activity-legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
```

---

## 217. BOARDING PASS / TICKET UI

```css
/* ─── Ticket shell with a true perforated-hole edge (mask-based, works on any background) ─── */
.ticket {
  --notch-size: 12px;
  --notch-position: 72%;
  display: grid;
  grid-template-columns: 1fr auto;
  background: var(--color-surface);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-lg);
  max-width: 480px;
  position: relative;
  mask-image:
    radial-gradient(circle var(--notch-size) at var(--notch-position) 0%,   transparent 99%, black 100%),
    radial-gradient(circle var(--notch-size) at var(--notch-position) 100%, transparent 99%, black 100%);
  mask-composite: intersect;
  -webkit-mask-composite: source-in; /* approximate legacy WebKit fallback */
}

/* Dashed tear line lines up with the mask notches via the same custom property */
.ticket-divider {
  position: absolute;
  inset-block: 0;
  inset-inline-start: var(--notch-position);
  border-inline-start: 2px dashed var(--color-border-strong);
  pointer-events: none;
}

/* ─── Main stub ─── */
.ticket-main {
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.ticket-route { display: flex; align-items: center; gap: var(--space-3); }
.ticket-airport { font-size: var(--font-size-2xl); font-weight: var(--font-weight-black); }
.ticket-city { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.ticket-plane-icon { color: var(--color-text-subtle); flex-shrink: 0; }

/* Dotted flight-path line between the two airport codes */
.ticket-path {
  flex: 1;
  height: 1px;
  background-image: linear-gradient(to right, var(--color-border-strong) 50%, transparent 0);
  background-size: 8px 1px;
  background-repeat: repeat-x;
}

.ticket-meta {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  padding-block-start: var(--space-4);
  border-top: 1px dashed var(--color-border);
}
.ticket-meta-label { font-size: var(--font-size-xs); text-transform: uppercase; letter-spacing: var(--letter-spacing-wider); color: var(--color-text-muted); }
.ticket-meta-value { font-size: var(--font-size-base); font-weight: var(--font-weight-bold); font-variant-numeric: tabular-nums; }

/* ─── Tear-off stub: boarding info + barcode, rotated to fit a narrow column ─── */
.ticket-stub {
  padding: var(--space-6) var(--space-4);
  background: var(--color-bg-subtle);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  writing-mode: vertical-rl;
  text-orientation: mixed;
}
.ticket-stub-gate { font-weight: var(--font-weight-bold); font-size: var(--font-size-sm); }
.ticket-stub-seat { font-family: var(--font-mono); font-weight: var(--font-weight-bold); }

/* Barcode placeholder (repeating bars), reset to horizontal inside the vertical stub */
.ticket-barcode {
  writing-mode: horizontal-tb;
  width: 100%;
  height: 48px;
  background-image: repeating-linear-gradient(90deg, var(--color-neutral-900) 0 2px, transparent 2px 5px);
}

/* ─── Fare class badge ─── */
.ticket-class {
  align-self: flex-start;
  padding: 0.2em 0.6em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
}
.ticket-class--economy  { background: var(--color-bg-muted);  color: var(--color-text-muted); }
.ticket-class--business { background: oklch(0.85 0.1 80);     color: oklch(0.4 0.15 80); }
.ticket-class--first    { background: var(--color-neutral-900); color: white; }
```

---

## 218. NATIVE FORM CONTROL THEMING

```css
/* ─── Global native-control theming via accent-color ─── */
:root {
  accent-color: var(--color-accent);
  color-scheme: light dark;
}

.form-danger-zone  { accent-color: var(--color-danger-500); }
.form-success-zone { accent-color: var(--color-success-500); }

/* ─── Checkbox / radio: sizing + label pairing, no visual replacement needed ─── */
input[type="checkbox"],
input[type="radio"] {
  width: 1.125rem;
  height: 1.125rem;
  margin: 0;
  cursor: pointer;
}
.control--lg input[type="checkbox"],
.control--lg input[type="radio"] { width: 1.5rem; height: 1.5rem; }

.control {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  cursor: pointer;
}

/* ─── Range slider ─── */
input[type="range"] {
  accent-color: var(--color-accent);
  block-size: 1.25rem;
  inline-size: 100%;
}
/* Firefox exposes the track/thumb via standard pseudo-elements */
input[type="range"]::-moz-range-track { height: 4px; border-radius: var(--radius-full); background: var(--color-bg-muted); }
input[type="range"]::-moz-range-thumb { border: none; }
/* Chromium/WebKit require vendor-prefixed pseudo-elements for the same parts */
input[type="range"]::-webkit-slider-runnable-track { height: 4px; border-radius: var(--radius-full); background: var(--color-bg-muted); }
input[type="range"]::-webkit-slider-thumb { margin-block-start: -8px; /* centers the thumb on a 4px track */ }

/* ─── Progress element ─── */
progress {
  accent-color: var(--color-accent);
  inline-size: 100%;
  block-size: 8px;
  border-radius: var(--radius-full);
  overflow: hidden;
  border: none;
  background: var(--color-bg-muted); /* used by Firefox directly */
}
progress::-webkit-progress-bar   { background: var(--color-bg-muted); border-radius: inherit; }
progress::-webkit-progress-value { background: var(--color-accent);   border-radius: inherit; transition: width var(--duration-normal); }
progress::-moz-progress-bar      { background: var(--color-accent);   border-radius: inherit; }
/* Indeterminate progress (no [value]) keeps the browser's native animation — leave width/value alone */

/* ─── Dark theme: color-scheme flips native chrome automatically ─── */
[data-theme="dark"] {
  color-scheme: dark;
  accent-color: var(--color-accent);
}
/* color-scheme: dark also re-themes scrollbars and default focus rings —
   no extra rules are needed for that part. */

/* ─── Select: light-touch native styling, not a full custom replacement ─── */
select {
  accent-color: var(--color-accent);
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  font: inherit;
  color: var(--color-text);
}
select:focus-visible {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 20%, transparent);
}

/* ─── File input button ─── */
input[type="file"]::file-selector-button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-bg-subtle);
  font: inherit;
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  margin-inline-end: var(--space-3);
  transition: background var(--duration-fast);
}
input[type="file"]::file-selector-button:hover { background: var(--color-bg-muted); }
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                     PART 15 — COMPLETE                               ║
║  Chapters 203–218 | 16 new chapters | Output: css-guide-part15.md    ║
╚══════════════════════════════════════════════════════════════════════╝
```
