# CSS GUIDE — PART 17
## Chapters 229–238

---

## 229. FINTECH / TRADING DASHBOARD

```css
/* ─── Ticker tape: continuous scrolling row of live prices ─── */
.ticker-tape {
  overflow: hidden;
  background: var(--color-neutral-900);
  padding-block: var(--space-2);
  white-space: nowrap;
}

.ticker-tape__track {
  display: inline-flex;
  gap: var(--space-8);
  animation: ticker-scroll 30s linear infinite;
}
.ticker-tape:hover .ticker-tape__track { animation-play-state: paused; }

@keyframes ticker-scroll {
  to { translate: -50% 0; } /* track content is duplicated once, so this loops seamlessly */
}

.ticker-item { display: inline-flex; align-items: center; gap: var(--space-2); font-family: var(--font-mono); font-size: var(--font-size-sm); color: white; }
.ticker-symbol { font-weight: var(--font-weight-bold); color: var(--color-text-subtle); }
.ticker-price  { font-variant-numeric: tabular-nums; }
.ticker-change { font-size: var(--font-size-xs); font-variant-numeric: tabular-nums; }
.ticker-change--up   { color: var(--color-success-500); }
.ticker-change--down { color: var(--color-danger-500); }
.ticker-change--up::before   { content: '▲ '; }
.ticker-change--down::before { content: '▼ '; }

/* ─── Order book: two mirrored columns, bid (buy) and ask (sell) ─── */
.order-book { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); font-family: var(--font-mono); font-size: var(--font-size-xs); }

.order-book-col-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding-block-end: var(--space-1);
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-semibold);
}

.order-row { display: grid; grid-template-columns: 1fr 1fr; position: relative; padding-block: 2px; }

/* Depth bar behind the row shows relative order size */
.order-row::before {
  content: '';
  position: absolute;
  inset-block: 0;
  width: var(--depth, 40%);
  z-index: -1;
}
.order-row--bid { text-align: end; }
.order-row--bid::before { inset-inline-end: 0; background: color-mix(in srgb, var(--color-success-500) 12%, transparent); }
.order-row--ask::before { inset-inline-start: 0; background: color-mix(in srgb, var(--color-danger-500) 12%, transparent); }
.order-price--bid { color: var(--color-success-600); }
.order-price--ask { color: var(--color-danger-600); }

/* ─── Watchlist row with sparkline ─── */
.watchlist-row {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}
.watchlist-row:hover { background: var(--color-bg-subtle); }
.watchlist-sparkline { width: 60px; height: 24px; }
.watchlist-sparkline--up   path { stroke: var(--color-success-500); }
.watchlist-sparkline--down path { stroke: var(--color-danger-500); }

/* ─── Candlestick building blocks ─── */
.candlestick { position: relative; width: 8px; }
.candlestick__wick { position: absolute; inset-inline-start: 50%; translate: -50% 0; width: 1px; background: var(--color-text-muted); }
.candlestick__body { position: absolute; inset-inline: 0; border-radius: 1px; }
.candlestick--bull .candlestick__body { background: var(--color-success-500); }
.candlestick--bear .candlestick__body { background: var(--color-danger-500); }

/* ─── Price flash: brief highlight when a value updates ─── */
.price-flash-up   { animation: flash-green 0.6s ease-out; }
.price-flash-down { animation: flash-red 0.6s ease-out; }
@keyframes flash-green { from { background: color-mix(in srgb, var(--color-success-500) 25%, transparent); } }
@keyframes flash-red   { from { background: color-mix(in srgb, var(--color-danger-500) 25%, transparent); } }
```

---

## 230. CRYPTO WALLET / PORTFOLIO UI

```css
/* ─── Balance hero card ─── */
.wallet-balance {
  background: linear-gradient(135deg, var(--color-neutral-900), oklch(0.25 0.08 280));
  color: white;
  border-radius: var(--radius-2xl);
  padding: var(--space-8) var(--space-6);
  text-align: center;
}
.wallet-balance__label { font-size: var(--font-size-sm); opacity: 0.7; }
.wallet-balance__value {
  font-size: clamp(2rem, 6vw, 3rem);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
  margin-block: var(--space-2);
}
.wallet-balance__change {
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
  font-size: var(--font-size-sm);
  padding: 0.25em 0.75em;
  border-radius: var(--radius-full);
  background: rgba(255 255 255 / 0.1);
}
.wallet-balance__change--up   { color: var(--color-success-300); }
.wallet-balance__change--down { color: var(--color-danger-300); }

/* ─── Quick actions: send / receive / swap / buy ─── */
.wallet-actions { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-3); margin-block-start: var(--space-6); }
.wallet-action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3);
  border-radius: var(--radius-xl);
  background: rgba(255 255 255 / 0.08);
  color: white;
  border: none;
  cursor: pointer;
  transition: background var(--duration-fast);
}
.wallet-action-btn:hover { background: rgba(255 255 255 / 0.16); }
.wallet-action-btn__icon { width: 2.25rem; height: 2.25rem; border-radius: 50%; background: rgba(255 255 255 / 0.12); display: flex; align-items: center; justify-content: center; }

/* ─── Asset list row ─── */
.asset-row {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-xl);
  transition: background var(--duration-fast);
}
.asset-row:hover { background: var(--color-bg-subtle); }
.asset-icon { width: 2.5rem; height: 2.5rem; border-radius: 50%; }
.asset-name { font-weight: var(--font-weight-semibold); }
.asset-ticker { font-size: var(--font-size-xs); color: var(--color-text-muted); text-transform: uppercase; }
.asset-holdings { text-align: end; }
.asset-value { font-weight: var(--font-weight-bold); font-variant-numeric: tabular-nums; }
.asset-amount { font-size: var(--font-size-xs); color: var(--color-text-muted); font-variant-numeric: tabular-nums; }

/* ─── Allocation donut legend ─── */
.allocation-legend { display: flex; flex-direction: column; gap: var(--space-2); }
.allocation-legend-item { display: flex; align-items: center; gap: var(--space-2); font-size: var(--font-size-sm); }
.allocation-swatch { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }
.allocation-pct { margin-inline-start: auto; font-weight: var(--font-weight-semibold); font-variant-numeric: tabular-nums; }

/* ─── Send/Receive modal shell ─── */
.wallet-modal-tabs { display: flex; border-radius: var(--radius-lg); background: var(--color-bg-subtle); padding: 2px; }
.wallet-modal-tab { flex: 1; padding: var(--space-2); border: none; background: none; border-radius: var(--radius-md); font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); cursor: pointer; }
.wallet-modal-tab.active { background: var(--color-surface); box-shadow: var(--shadow-sm); }

.wallet-address-field {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  padding: var(--space-3);
  background: var(--color-bg-subtle);
  border-radius: var(--radius-lg);
}
.wallet-address-field span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.wallet-fee-row { display: flex; justify-content: space-between; font-size: var(--font-size-sm); color: var(--color-text-muted); padding-block: var(--space-2); }
```

---

## 231. EDUCATION / LMS COURSE PLAYER

```css
/* ─── Course layout: video + sidebar of lessons ─── */
.course-player { display: grid; grid-template-columns: 1fr 320px; gap: var(--space-6); }

.course-video { aspect-ratio: 16 / 9; background: var(--color-neutral-900); border-radius: var(--radius-xl); position: relative; overflow: hidden; }

/* Chapter markers on the video progress bar */
.course-video-progress { position: relative; height: 4px; background: rgba(255 255 255 / 0.2); }
.course-video-progress__fill { height: 100%; background: var(--color-accent); }
.course-chapter-marker { position: absolute; top: 0; bottom: 0; width: 2px; background: rgba(255 255 255 / 0.6); }

/* ─── Lesson sidebar ─── */
.lesson-sidebar { border: 1px solid var(--color-border); border-radius: var(--radius-xl); overflow: hidden; max-height: 560px; overflow-y: auto; }

.lesson-module-header {
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-subtle);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  color: var(--color-text-muted);
  position: sticky;
  top: 0;
}

.lesson-row {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
}
.lesson-row:hover { background: var(--color-bg-subtle); }
.lesson-row.active { background: color-mix(in srgb, var(--color-accent) 8%, transparent); border-inline-start: 3px solid var(--color-accent); }

.lesson-status { width: 1.25rem; height: 1.25rem; border-radius: 50%; border: 2px solid var(--color-border-strong); flex-shrink: 0; position: relative; }
.lesson-status.completed { background: var(--color-success-500); border-color: var(--color-success-500); }
.lesson-status.completed::after { content: '✓'; position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.65rem; }
.lesson-status.playing { border-color: var(--color-accent); }
.lesson-status.playing::after { content: ''; position: absolute; inset: 3px; border-radius: 50%; background: var(--color-accent); }

.lesson-title { font-size: var(--font-size-sm); }
.lesson-duration { font-size: var(--font-size-xs); color: var(--color-text-muted); font-variant-numeric: tabular-nums; }

/* ─── Overall course progress ─── */
.course-progress-header { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-4); }
.course-progress-bar { flex: 1; height: 6px; background: var(--color-bg-muted); border-radius: var(--radius-full); overflow: hidden; }
.course-progress-bar__fill { height: 100%; background: var(--color-accent); border-radius: inherit; }
.course-progress-pct { font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold); color: var(--color-text-muted); }

/* ─── Timestamped notes panel ─── */
.lesson-note { display: flex; gap: var(--space-3); padding: var(--space-3) 0; border-bottom: 1px solid var(--color-border); }
.lesson-note-time { font-family: var(--font-mono); font-size: var(--font-size-xs); color: var(--color-accent); cursor: pointer; flex-shrink: 0; }

/* ─── Playback speed control ─── */
.playback-speed { display: flex; gap: 2px; background: rgba(255 255 255 / 0.1); border-radius: var(--radius-md); padding: 2px; }
.playback-speed button { padding: 0.25rem 0.5rem; border: none; background: none; color: rgba(255 255 255 / 0.7); font-size: var(--font-size-xs); border-radius: var(--radius-sm); cursor: pointer; }
.playback-speed button.active { background: rgba(255 255 255 / 0.2); color: white; }
```

---

## 232. HEALTHCARE CLINICIAN DASHBOARD

```css
/* ─── Patient vitals card grid ─── */
.vitals-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: var(--space-4); }

.vital-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: var(--space-4); position: relative; }
.vital-card[data-status="critical"] { border-color: var(--color-danger-500); background: color-mix(in srgb, var(--color-danger-500) 4%, var(--color-surface)); }
.vital-card[data-status="warning"]  { border-color: var(--color-warning-500); }

.vital-label { font-size: var(--font-size-xs); color: var(--color-text-muted); text-transform: uppercase; letter-spacing: var(--letter-spacing-wide); }
.vital-value { font-size: var(--font-size-2xl); font-weight: var(--font-weight-black); font-variant-numeric: tabular-nums; margin-block: var(--space-1); }
.vital-unit  { font-size: var(--font-size-sm); font-weight: var(--font-weight-normal); color: var(--color-text-muted); }
.vital-trend { font-size: var(--font-size-xs); display: flex; align-items: center; gap: 0.25em; }
.vital-trend--up     { color: var(--color-danger-500); }
.vital-trend--down   { color: var(--color-success-500); }
.vital-trend--stable { color: var(--color-text-muted); }

/* Small live-reading pulse dot for continuously-monitored vitals */
.vital-live-dot { position: absolute; top: var(--space-3); right: var(--space-3); width: 8px; height: 8px; border-radius: 50%; background: var(--color-success-500); animation: vital-pulse 2s ease-in-out infinite; }
@keyframes vital-pulse { 50% { scale: 1.4; opacity: 0.5; } }

/* ─── Medication schedule timeline ─── */
.med-timeline { display: flex; flex-direction: column; gap: 0; }
.med-row { display: grid; grid-template-columns: 80px 1fr auto; gap: var(--space-3); align-items: center; padding-block: var(--space-3); border-bottom: 1px solid var(--color-border); }
.med-time { font-family: var(--font-mono); font-size: var(--font-size-sm); color: var(--color-text-muted); }
.med-name { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.med-dose { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.med-status { padding: 0.2em 0.6em; border-radius: var(--radius-full); font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold); }
.med-status--given   { background: var(--color-success-100); color: var(--color-success-900); }
.med-status--due     { background: var(--color-warning-100); color: var(--color-warning-900); }
.med-status--overdue { background: var(--color-danger-100);  color: var(--color-danger-900); animation: med-overdue-blink 1.5s ease-in-out infinite; }
@keyframes med-overdue-blink { 50% { opacity: 0.5; } }

/* ─── Patient banner strip ─── */
.patient-banner { display: flex; align-items: center; gap: var(--space-4); padding: var(--space-4) var(--space-5); background: var(--color-bg-subtle); border-radius: var(--radius-xl); }
.patient-avatar { width: 3rem; height: 3rem; border-radius: 50%; }
.patient-name { font-weight: var(--font-weight-bold); }
.patient-meta { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.patient-alert-badge { display: flex; align-items: center; gap: var(--space-1); padding: 0.2em 0.6em; border-radius: var(--radius-md); background: var(--color-danger-100); color: var(--color-danger-700); font-size: var(--font-size-xs); font-weight: var(--font-weight-bold); }

/* Distinct from ch.206 (general consumer health UI) — this is a
   data-dense clinician-facing panel */
.clinician-panel { display: grid; grid-template-columns: 260px 1fr; gap: var(--space-6); }
```

---

## 233. FLIGHT BOOKING — SEAT MAP

```css
/* ─── Aircraft seat map ─── */
.seat-map { display: inline-flex; flex-direction: column; gap: var(--space-2); padding: var(--space-6); background: var(--color-bg-subtle); border-radius: var(--radius-2xl); }

.seat-row { display: grid; grid-template-columns: 1.5rem repeat(3, 2rem) 1rem repeat(3, 2rem); gap: 6px; align-items: center; }
.seat-row-number { font-size: var(--font-size-xs); color: var(--color-text-muted); text-align: center; }

.seat {
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-sm) var(--radius-sm) var(--radius-md) var(--radius-md);
  border: none;
  cursor: pointer;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: white;
  transition: scale var(--duration-fast) var(--ease-bounce);
}
.seat:hover:not(:disabled) { scale: 1.1; }
.seat--available     { background: var(--color-bg-muted); color: var(--color-text-muted); }
.seat--selected       { background: var(--color-accent); }
.seat--occupied       { background: var(--color-neutral-300); cursor: not-allowed; }
.seat--extra-legroom  { background: var(--color-success-300); }
.seat--business       { background: oklch(0.85 0.1 80); color: oklch(0.35 0.15 80); }
.seat:disabled        { cursor: not-allowed; opacity: 0.6; }

.seat-aisle { width: 1rem; }

.seat-row--exit::before {
  content: 'EXIT';
  writing-mode: vertical-rl;
  font-size: var(--font-size-xs);
  color: var(--color-danger-500);
  font-weight: var(--font-weight-bold);
}

/* ─── Legend ─── */
.seat-legend { display: flex; flex-wrap: wrap; gap: var(--space-4); padding-block-start: var(--space-4); border-top: 1px solid var(--color-border); }
.seat-legend-item { display: flex; align-items: center; gap: var(--space-2); font-size: var(--font-size-xs); }
.seat-legend-swatch { width: 1rem; height: 1rem; border-radius: var(--radius-sm); }

/* ─── Selected-seat summary bar ─── */
.seat-summary {
  position: sticky;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  box-shadow: 0 -4px 12px rgb(0 0 0 / 0.06);
}
.seat-summary-price { font-size: var(--font-size-lg); font-weight: var(--font-weight-bold); }

.cabin-divider {
  text-align: center;
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  padding-block: var(--space-2);
  border-block: 1px dashed var(--color-border);
}
```

---

## 234. HOTEL BOOKING — ROOM SELECTOR

```css
/* ─── Room card ─── */
.room-card { display: grid; grid-template-columns: 220px 1fr auto; gap: var(--space-5); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: var(--space-4); align-items: center; }

.room-gallery { position: relative; aspect-ratio: 4 / 3; border-radius: var(--radius-lg); overflow: hidden; }
.room-gallery img { width: 100%; height: 100%; object-fit: cover; }
.room-gallery-count { position: absolute; bottom: var(--space-2); right: var(--space-2); background: rgba(0 0 0 / 0.6); color: white; font-size: var(--font-size-xs); padding: 0.15em 0.5em; border-radius: var(--radius-md); }

.room-title { font-weight: var(--font-weight-bold); font-size: var(--font-size-base); }
.room-amenities { display: flex; flex-wrap: wrap; gap: var(--space-3); margin-block-start: var(--space-2); }
.room-amenity { display: flex; align-items: center; gap: 0.375rem; font-size: var(--font-size-xs); color: var(--color-text-muted); }
.room-occupancy { font-size: var(--font-size-xs); color: var(--color-text-muted); margin-block-start: var(--space-2); }

.room-price-col { text-align: end; }
.room-price { font-size: var(--font-size-xl); font-weight: var(--font-weight-black); }
.room-price-note { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.room-select-btn { margin-block-start: var(--space-3); }

.room-card.sold-out { opacity: 0.55; }
.room-card.sold-out .room-select-btn { pointer-events: none; }

/* ─── Availability calendar ─── */
.availability-calendar { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
.avail-day { aspect-ratio: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: var(--radius-md); font-size: var(--font-size-xs); cursor: pointer; }
.avail-day--available { background: var(--color-success-100); color: var(--color-success-900); }
.avail-day--limited   { background: var(--color-warning-100); color: var(--color-warning-900); }
.avail-day--booked    { background: var(--color-bg-muted); color: var(--color-text-subtle); cursor: not-allowed; }
.avail-day--selected  { background: var(--color-accent); color: white; }
.avail-day-price { font-size: 0.65rem; font-variant-numeric: tabular-nums; }

/* ─── Rate comparison option ─── */
.rate-option { border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: var(--space-3) var(--space-4); cursor: pointer; transition: border-color var(--duration-fast); }
.rate-option.selected { border-color: var(--color-accent); border-width: 2px; }
.rate-option-badge { display: inline-block; font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold); color: var(--color-success-600); margin-block-end: var(--space-1); }
```

---

## 235. WEATHER FORECAST WIDGET

```css
/* ─── Current conditions hero ─── */
.weather-now {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-6);
  border-radius: var(--radius-2xl);
  background: linear-gradient(160deg, oklch(0.6 0.15 230), oklch(0.75 0.12 210));
  color: white;
}
.weather-now-temp { font-size: clamp(3rem, 8vw, 5rem); font-weight: 200; line-height: 1; }
.weather-now-condition { font-size: var(--font-size-base); opacity: 0.9; }
.weather-now-meta { display: flex; gap: var(--space-4); font-size: var(--font-size-xs); opacity: 0.8; margin-block-start: var(--space-2); }
.weather-icon { width: 4rem; height: 4rem; }

/* ─── Hourly forecast, horizontal scroll ─── */
.hourly-forecast { display: flex; gap: var(--space-2); overflow-x: auto; padding-block: var(--space-3); scroll-snap-type: x proximity; }
.hourly-item { scroll-snap-align: start; flex: 0 0 64px; display: flex; flex-direction: column; align-items: center; gap: var(--space-2); padding: var(--space-3) var(--space-2); border-radius: var(--radius-xl); }
.hourly-item.now { background: var(--color-bg-subtle); }
.hourly-time { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.hourly-temp { font-weight: var(--font-weight-semibold); font-variant-numeric: tabular-nums; }

/* ─── 7-day forecast rows ─── */
.daily-forecast-row { display: grid; grid-template-columns: 80px auto 1fr auto auto; align-items: center; gap: var(--space-3); padding: var(--space-2) 0; }
.daily-day { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }

.daily-range-track { position: relative; height: 4px; background: var(--color-bg-muted); border-radius: var(--radius-full); }
.daily-range-fill {
  position: absolute;
  inset-block: 0;
  left: var(--range-start, 20%);
  width: var(--range-width, 50%);
  background: linear-gradient(to right, var(--color-brand-300), var(--color-warning-500));
  border-radius: inherit;
}
.daily-temp-lo { color: var(--color-text-muted); }
.daily-temp-hi { font-weight: var(--font-weight-semibold); }

/* ─── Precipitation / UV index bars ─── */
.index-bar-group { display: flex; flex-direction: column; gap: var(--space-1); }
.index-bar-label { display: flex; justify-content: space-between; font-size: var(--font-size-xs); color: var(--color-text-muted); }
.index-bar-track { height: 6px; background: var(--color-bg-muted); border-radius: var(--radius-full); overflow: hidden; }
.index-bar-fill { height: 100%; border-radius: inherit; }
.index-bar-fill--rain { background: var(--color-brand-500); }
.index-bar-fill--uv   { background: linear-gradient(to right, var(--color-success-500), var(--color-warning-500), var(--color-danger-500)); }
```

---

## 236. SPORTS LIVE SCOREBOARD

```css
/* ─── Live scoreboard ─── */
.scoreboard { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: var(--space-4); padding: var(--space-5); background: var(--color-neutral-900); color: white; border-radius: var(--radius-2xl); }

.scoreboard-team { display: flex; flex-direction: column; align-items: center; gap: var(--space-2); }
.scoreboard-team--away { flex-direction: row-reverse; }
.team-logo { width: 3rem; height: 3rem; }
.team-score { font-size: clamp(2rem, 5vw, 3rem); font-weight: var(--font-weight-black); font-variant-numeric: tabular-nums; }
.team-name { font-size: var(--font-size-sm); opacity: 0.8; }

.scoreboard-status { text-align: center; }
.scoreboard-clock { font-family: var(--font-mono); font-size: var(--font-size-lg); font-variant-numeric: tabular-nums; }
.scoreboard-period { font-size: var(--font-size-xs); opacity: 0.7; }

.live-badge { display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.2em 0.6em; border-radius: var(--radius-full); background: var(--color-danger-500); font-size: var(--font-size-xs); font-weight: var(--font-weight-bold); text-transform: uppercase; }
.live-badge::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: white; animation: live-pulse 1.2s ease-in-out infinite; }
@keyframes live-pulse { 50% { opacity: 0.3; } }

/* ─── Match event timeline ─── */
.match-timeline { position: relative; padding-block: var(--space-4); }
.match-timeline::before { content: ''; position: absolute; inset-inline: 0; top: 50%; height: 2px; background: var(--color-border); }
.match-event {
  position: absolute;
  top: 50%;
  translate: -50% -50%;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--color-surface);
  border: 2px solid var(--color-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
}
.match-event--goal { border-color: var(--color-success-500); }
.match-event--card-yellow { border-color: var(--color-warning-500); background: var(--color-warning-500); }
.match-event--card-red    { border-color: var(--color-danger-500); background: var(--color-danger-500); }

/* ─── Compact mini standings table ─── */
.mini-standings-row { display: grid; grid-template-columns: 1.5rem 1fr repeat(4, 2rem); gap: var(--space-2); align-items: center; padding: var(--space-2) var(--space-3); font-size: var(--font-size-xs); text-align: center; }
.mini-standings-row:nth-child(odd) { background: var(--color-bg-subtle); }
.mini-standings-rank { text-align: start; font-weight: var(--font-weight-semibold); }
.mini-standings-team { text-align: start; font-weight: var(--font-weight-medium); }
.mini-standings-row--qualifying { border-inline-start: 3px solid var(--color-success-500); }
.mini-standings-row--relegation { border-inline-start: 3px solid var(--color-danger-500); }
```

---

## 237. PODCAST / AUDIOBOOK PLAYER

```css
/* ─── Now-playing bar ─── */
.podcast-player { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: var(--space-4); padding: var(--space-3) var(--space-5); background: var(--color-surface); border-top: 1px solid var(--color-border); }

.podcast-cover { width: 3.5rem; height: 3.5rem; border-radius: var(--radius-lg); }
.podcast-title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.podcast-show  { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.podcast-controls { display: flex; align-items: center; gap: var(--space-4); justify-content: center; }
.podcast-play-btn { width: 2.75rem; height: 2.75rem; border-radius: 50%; background: var(--color-accent); color: white; border: none; display: flex; align-items: center; justify-content: center; cursor: pointer; }
.podcast-skip-btn { background: none; border: none; color: var(--color-text-muted); cursor: pointer; }

.podcast-progress { display: flex; align-items: center; gap: var(--space-2); font-size: var(--font-size-xs); font-variant-numeric: tabular-nums; color: var(--color-text-muted); }
.podcast-progress-track { flex: 1; height: 4px; background: var(--color-bg-muted); border-radius: var(--radius-full); position: relative; cursor: pointer; }
.podcast-progress-fill { position: absolute; inset-block: 0; left: 0; background: var(--color-accent); border-radius: inherit; }

/* ─── Playback speed selector ─── */
.speed-select { display: flex; align-items: center; gap: 0.25em; padding: 0.25em 0.6em; border-radius: var(--radius-full); background: var(--color-bg-subtle); font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold); cursor: pointer; }

/* ─── Sleep timer ─── */
.sleep-timer-display { display: flex; flex-direction: column; align-items: center; gap: var(--space-3); padding: var(--space-6); }
.sleep-timer-ring { width: 120px; height: 120px; }
.sleep-timer-remaining { font-family: var(--font-mono); font-size: var(--font-size-xl); font-variant-numeric: tabular-nums; }
.sleep-timer-presets { display: flex; gap: var(--space-2); flex-wrap: wrap; justify-content: center; }
.sleep-timer-preset { padding: 0.4em 0.9em; border-radius: var(--radius-full); border: 1px solid var(--color-border); background: none; font-size: var(--font-size-sm); cursor: pointer; }
.sleep-timer-preset.active { background: var(--color-accent); color: white; border-color: var(--color-accent); }

/* ─── Episode list row with chapters ─── */
.episode-row { display: grid; grid-template-columns: auto 1fr auto; gap: var(--space-3); align-items: center; padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--color-border); }
.episode-row.playing { background: color-mix(in srgb, var(--color-accent) 6%, transparent); }
.episode-duration { font-size: var(--font-size-xs); color: var(--color-text-muted); font-variant-numeric: tabular-nums; }
.episode-progress-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--color-text-subtle); }
.episode-progress-dot.finished { background: var(--color-success-500); }
```

---

## 238. FORUM / COMMUNITY THREAD UI

```css
/* ─── Thread post ─── */
.forum-post { display: grid; grid-template-columns: 48px 1fr; gap: var(--space-3); padding: var(--space-4) 0; border-bottom: 1px solid var(--color-border); }
.forum-avatar { width: 48px; height: 48px; border-radius: 50%; }

.forum-post-header { display: flex; align-items: baseline; gap: var(--space-2); flex-wrap: wrap; }
.forum-author { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.forum-timestamp { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.forum-author-badge { font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold); padding: 0.1em 0.5em; border-radius: var(--radius-sm); }
.forum-author-badge--op  { background: var(--color-accent); color: white; }
.forum-author-badge--mod { background: var(--color-success-100); color: var(--color-success-900); }

.forum-post-body { font-size: var(--font-size-sm); line-height: var(--line-height-relaxed); margin-block: var(--space-2); }

/* ─── Voting control ─── */
.forum-vote { display: flex; align-items: center; gap: var(--space-2); }
.vote-btn { width: 1.75rem; height: 1.75rem; border-radius: var(--radius-md); border: none; background: var(--color-bg-subtle); color: var(--color-text-muted); cursor: pointer; }
.vote-btn.active--up   { background: var(--color-success-500); color: white; }
.vote-btn.active--down { background: var(--color-danger-500); color: white; }
.vote-count { font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); min-width: 2ch; text-align: center; }

/* ─── Nested replies ─── */
.forum-replies { margin-inline-start: var(--space-6); padding-inline-start: var(--space-4); border-inline-start: 2px solid var(--color-border); display: flex; flex-direction: column; gap: var(--space-3); }
.forum-replies .forum-replies { margin-inline-start: var(--space-4); }
.forum-replies .forum-replies .forum-replies { margin-inline-start: var(--space-2); }

.forum-collapse-toggle { font-size: var(--font-size-xs); color: var(--color-accent); background: none; border: none; cursor: pointer; padding: var(--space-1) 0; }

/* ─── Thread meta bar ─── */
.forum-thread-meta { display: flex; gap: var(--space-4); font-size: var(--font-size-xs); color: var(--color-text-muted); padding-block: var(--space-3); border-bottom: 1px solid var(--color-border); }
.forum-thread-pinned { display: inline-flex; align-items: center; gap: 0.25em; color: var(--color-accent); font-weight: var(--font-weight-semibold); }
.forum-reputation { font-size: var(--font-size-xs); color: var(--color-text-subtle); }
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                     PART 17 — COMPLETE                               ║
║  Chapters 229–238 | 10 new chapters | Output: css-guide-part17.md    ║
╚══════════════════════════════════════════════════════════════════════╝
```
