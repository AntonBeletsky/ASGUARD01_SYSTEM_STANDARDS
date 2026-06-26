# CSS GUIDE — PART 13
## Chapters 182–196

---

## 182. SUBSCRIPTION & BILLING UI

```css
/* ─── Current plan card ─── */
.plan-card-current {
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--color-accent) 8%, var(--color-surface)),
    var(--color-surface)
  );
  border: 2px solid var(--color-accent);
  border-radius: var(--radius-2xl);
  padding: var(--space-6);
  position: relative;
  overflow: hidden;
}

.plan-card-current::before {
  content: '';
  position: absolute;
  inset-block-start: 0;
  inset-inline-end: 0;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, color-mix(in srgb, var(--color-accent) 15%, transparent), transparent 70%);
  pointer-events: none;
}

.plan-name { font-size: var(--step-1); font-weight: var(--font-weight-black); }
.plan-price {
  font-size: var(--step-3);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
  line-height: 1;
  margin-block: var(--space-3);
}
.plan-price span { font-size: var(--font-size-base); font-weight: var(--font-weight-normal); color: var(--color-text-muted); }
.plan-renews { font-size: var(--font-size-xs); color: var(--color-text-muted); }

/* Usage meter */
.usage-meter {
  margin-block-start: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.usage-row {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.usage-header {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.usage-bar {
  height: 6px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.usage-fill {
  height: 100%;
  border-radius: inherit;
  width: var(--usage, 0%);
  background: var(--color-accent);
  transition: width 0.6s var(--ease-out);
}

.usage-fill.warning { background: var(--color-warning-500); }
.usage-fill.critical { background: var(--color-danger-500); }

/* Invoice table */
.invoice-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.invoice-row {
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: var(--space-4);
  align-items: center;
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border);
  font-size: var(--font-size-sm);
}
.invoice-row:last-child { border: none; }

.invoice-date { color: var(--color-text-muted); font-variant-numeric: tabular-nums; }
.invoice-amount { font-weight: var(--font-weight-semibold); font-variant-numeric: tabular-nums; }

.invoice-status {
  padding: 0.15em 0.5em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
}
.invoice-status--paid    { background: var(--color-success-100); color: var(--color-success-700); }
.invoice-status--pending { background: var(--color-warning-100); color: var(--color-warning-700); }
.invoice-status--failed  { background: var(--color-danger-100);  color: var(--color-danger-700); }

.invoice-download {
  color: var(--color-accent);
  font-size: var(--font-size-xs);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.25em;
}
.invoice-download:hover { text-decoration: underline; }

/* Cancel confirmation */
.cancel-confirm {
  background: var(--color-danger-100);
  border: 1px solid var(--color-danger-200);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.cancel-confirm__title {
  font-weight: var(--font-weight-bold);
  color: var(--color-danger-700);
  margin-block-end: var(--space-2);
}

.cancel-confirm__desc {
  font-size: var(--font-size-sm);
  color: var(--color-danger-600);
  margin-block-end: var(--space-5);
  line-height: 1.6;
}

/* Downgrade prompt */
.downgrade-features {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-block: var(--space-4);
}

.downgrade-feature {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--color-danger-600);
}
.downgrade-feature::before { content: '✕'; font-weight: bold; color: var(--color-danger-500); }
```

---

## 183. FLASH SALE & PROMO UI

```css
/* ─── Flash sale banner ─── */
.flash-banner {
  background: linear-gradient(135deg, #ff4d00, #ff0080);
  color: white;
  padding: var(--space-3) var(--space-6);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  flex-wrap: wrap;
  position: relative;
  overflow: hidden;
}

/* Animated background stripes */
.flash-banner::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    45deg,
    transparent 0,
    transparent 20px,
    rgba(255 255 255 / 0.05) 20px,
    rgba(255 255 255 / 0.05) 40px
  );
  animation: stripe-scroll 3s linear infinite;
}

@keyframes stripe-scroll {
  from { background-position: 0 0; }
  to   { background-position: 56px 0; }
}

.flash-banner > * { position: relative; z-index: 1; }

.flash-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-weight: var(--font-weight-black);
  font-size: var(--font-size-base);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.flash-label__bolt { animation: bolt-pulse 0.5s ease-in-out infinite alternate; }
@keyframes bolt-pulse { from { scale: 1; } to { scale: 1.3; } }

.flash-text { font-size: var(--font-size-sm); }

.flash-countdown-inline {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-family: var(--font-mono);
  font-weight: var(--font-weight-black);
  font-size: var(--font-size-lg);
  font-variant-numeric: tabular-nums;
  background: rgba(0 0 0 / 0.2);
  padding: 0.2em 0.6em;
  border-radius: var(--radius-md);
}

/* Discount badge */
.discount-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 52px;
  height: 52px;
  background: var(--color-warning-400);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-black);
  color: var(--color-warning-900);
  animation: badge-spin 4s linear infinite;
  box-shadow: var(--shadow-md);
  z-index: 1;
}

@keyframes badge-spin {
  0%, 90%, 100% { rotate: 0deg; }
  45%           { rotate: -15deg; }
  50%           { rotate: 15deg; }
}

.discount-badge__percent { font-size: 1rem; line-height: 1; }
.discount-badge__off     { font-size: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }

/* Product with sale price */
.sale-price-group {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
}

.sale-price-original {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  text-decoration: line-through;
  font-variant-numeric: tabular-nums;
}

.sale-price-new {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-black);
  color: var(--color-danger-500);
  font-variant-numeric: tabular-nums;
}

.sale-save-label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  color: var(--color-success-600);
  background: var(--color-success-100);
  padding: 0.15em 0.5em;
  border-radius: var(--radius-full);
}

/* Coupon code input */
.coupon-input-group {
  display: flex;
  gap: var(--space-2);
}

.coupon-input {
  flex: 1;
  padding: 0.625rem 0.875rem;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  font: inherit;
  font-size: var(--font-size-sm);
  font-family: var(--font-mono);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: var(--color-bg-subtle);
  outline: none;
  transition: border-color var(--duration-fast), background var(--duration-fast);
}
.coupon-input:focus {
  border-color: var(--color-accent);
  background: var(--color-surface);
  border-style: solid;
}
.coupon-input.applied {
  border-color: var(--color-success-400);
  border-style: solid;
  background: var(--color-success-100);
  color: var(--color-success-700);
}
.coupon-input.error {
  border-color: var(--color-danger-400);
  border-style: solid;
  animation: coupon-shake 0.3s ease-out;
}

@keyframes coupon-shake {
  0%, 100% { translate: 0; }
  25%       { translate: -6px; }
  75%       { translate: 6px; }
}
```

---

## 184. KIOSK UI PATTERNS

```css
/* ─── Kiosk full-screen layout ─── */
.kiosk {
  position: fixed;
  inset: 0;
  background: var(--kiosk-bg, #0a0a1a);
  color: var(--kiosk-text, white);
  font-family: var(--font-sans);
  overflow: hidden;
  cursor: none; /* hide system cursor */
  display: flex;
  flex-direction: column;
}

/* Kiosk header */
.kiosk-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-6) var(--space-8);
  background: rgba(255 255 255 / 0.05);
  border-bottom: 1px solid rgba(255 255 255 / 0.1);
}

.kiosk-clock {
  font-family: var(--font-mono);
  font-size: var(--step-2);
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
  color: rgba(255 255 255 / 0.8);
}

/* Kiosk main area */
.kiosk-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  gap: var(--space-8);
}

/* Big tap targets (min 80px for touchscreen) */
.kiosk-btn {
  min-height: 80px;
  min-width: 180px;
  padding: var(--space-5) var(--space-8);
  border-radius: var(--radius-2xl);
  border: none;
  cursor: pointer;
  font: inherit;
  font-size: var(--step-1);
  font-weight: var(--font-weight-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  transition:
    scale      0.12s var(--ease-bounce),
    box-shadow 0.12s;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.kiosk-btn:active { scale: 0.96; }
.kiosk-btn--primary {
  background: var(--color-accent);
  color: white;
  box-shadow: 0 0 40px color-mix(in srgb, var(--color-accent) 40%, transparent);
}
.kiosk-btn--secondary {
  background: rgba(255 255 255 / 0.1);
  color: white;
  border: 2px solid rgba(255 255 255 / 0.2);
}
.kiosk-btn--large {
  min-height: 120px;
  font-size: var(--step-2);
  padding: var(--space-6) var(--space-10);
}

/* Touch ripple */
.kiosk-btn {
  position: relative;
  overflow: hidden;
}
.kiosk-btn::after {
  content: '';
  position: absolute;
  width: 200px;
  height: 200px;
  background: rgba(255 255 255 / 0.2);
  border-radius: 50%;
  translate: -50% -50%;
  left: var(--rx, 50%);
  top:  var(--ry, 50%);
  scale: 0;
  opacity: 0;
}
.kiosk-btn:active::after {
  animation: kiosk-ripple 0.5s ease-out;
}
@keyframes kiosk-ripple {
  from { scale: 0; opacity: 1; }
  to   { scale: 3; opacity: 0; }
}

/* Idle screen */
.kiosk-idle {
  position: absolute;
  inset: 0;
  background: var(--kiosk-bg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-8);
  z-index: 50;
  animation: idle-appear 0.5s var(--ease-out);
}

@keyframes idle-appear { from { opacity: 0; } }

.kiosk-idle__tap {
  font-size: var(--step-3);
  font-weight: var(--font-weight-black);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  animation: tap-pulse 2s ease-in-out infinite;
}

@keyframes tap-pulse {
  0%, 100% { opacity: 1; scale: 1; }
  50%       { opacity: 0.6; scale: 0.98; }
}

/* Kiosk numpad */
.kiosk-numpad {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-3);
  max-width: 320px;
}

.kiosk-key {
  aspect-ratio: 1.2;
  border-radius: var(--radius-xl);
  border: 2px solid rgba(255 255 255 / 0.15);
  background: rgba(255 255 255 / 0.08);
  color: white;
  font-size: var(--step-2);
  font-weight: var(--font-weight-bold);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.1s, scale 0.1s var(--ease-bounce);
  font-variant-numeric: tabular-nums;
}
.kiosk-key:active { background: rgba(255 255 255 / 0.25); scale: 0.94; }

.kiosk-key--del { background: rgba(255 100 100 / 0.15); border-color: rgba(255 100 100 / 0.3); }
.kiosk-key--ok  { background: var(--color-accent); border-color: transparent; }
.kiosk-key--zero { grid-column: span 2; aspect-ratio: auto; padding: var(--space-4); }
```

---

## 185. SCROLLYTELLING

```css
/* ─── Scrollytelling layout ─── */
.scrolly {
  position: relative;
}

/* Sticky graphic panel */
.scrolly-graphic {
  position: sticky;
  top: 0;
  height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 0;
}

/* Story steps */
.scrolly-steps {
  position: relative;
  z-index: 1;
  padding-block-end: 100dvh;
}

.scrolly-step {
  max-width: 400px;
  padding: var(--space-8) var(--space-6);
  margin-inline-start: var(--space-8);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-lg);
  opacity: 0.3;
  transition: opacity 0.3s var(--ease-out);
  margin-block-end: 40dvh;
}

.scrolly-step.active { opacity: 1; }
.scrolly-step.active + .scrolly-step { opacity: 0.3; }

/* Step content */
.scrolly-step__num {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-black);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-accent);
  margin-block-end: var(--space-3);
}

.scrolly-step__title {
  font-size: var(--step-1);
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-3);
  text-wrap: balance;
}

.scrolly-step__text {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  line-height: 1.7;
}

/* Graphic elements */
.scrolly-vis {
  width: min(500px, 55vw);
  aspect-ratio: 1;
  position: relative;
}

/* Transition between vis states */
.vis-element {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.5s var(--ease-out), scale 0.5s var(--ease-out), translate 0.5s var(--ease-out);
  scale: 0.95;
}

.vis-element.active {
  opacity: 1;
  scale: 1;
  translate: 0 0;
}

/* ─── Parallax sections ─── */
.parallax-section {
  position: relative;
  overflow: hidden;
  height: 80dvh;
}

.parallax-bg {
  position: absolute;
  inset: -20%;
  background-size: cover;
  background-position: center;
  will-change: transform;
  /* JS: el.style.transform = `translateY(${scrollY * 0.3}px)` */
}

.parallax-content {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  /* Content moves slower or not at all */
}

/* Native scroll-driven parallax */
.parallax-native {
  animation: parallax-y linear both;
  animation-timeline: scroll(root block);
}

@keyframes parallax-y {
  from { translate: 0 calc(var(--parallax-start, -10%)); }
  to   { translate: 0 calc(var(--parallax-end, 10%)); }
}
```

---

## 186. RICH DROPDOWN MENUS

```css
/* ─── Mega select dropdown ─── */
.rich-select {
  position: relative;
}

.rich-select__trigger {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.625rem 0.875rem;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  cursor: pointer;
  font: inherit;
  font-size: var(--font-size-sm);
  min-width: 220px;
  text-align: start;
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
}

.rich-select__trigger:focus-visible {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);
}

.rich-select__value { flex: 1; }
.rich-select__placeholder { color: var(--color-text-subtle); }

.rich-select__icon {
  color: var(--color-text-muted);
  transition: rotate var(--duration-fast) var(--ease-out);
  flex-shrink: 0;
}

.rich-select[data-open="true"] .rich-select__icon { rotate: 180deg; }

/* Dropdown panel */
.rich-select__panel {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  min-width: 100%;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  z-index: var(--z-dropdown);
  overflow: hidden;
  animation: dropdown-in 0.15s var(--ease-out);
  max-height: 320px;
  display: flex;
  flex-direction: column;
}

@keyframes dropdown-in {
  from { opacity: 0; translate: 0 -6px; scale: 0.98; }
}

/* Search inside dropdown */
.rich-select__search {
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.rich-select__search input {
  width: 100%;
  padding: 0.375rem 0.625rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font: inherit;
  font-size: var(--font-size-sm);
  background: var(--color-bg-subtle);
  outline: none;
}

/* Options list */
.rich-select__list {
  overflow-y: auto;
  scrollbar-width: thin;
  flex: 1;
  padding: var(--space-1);
}

/* Group heading */
.rich-select__group-title {
  padding: var(--space-1) var(--space-3);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  position: sticky;
  top: 0;
  background: var(--color-surface);
}

/* Option */
.rich-select__option {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.5rem var(--space-3);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: background var(--duration-fast);
}
.rich-select__option:hover,
.rich-select__option[aria-selected="true"] { background: var(--color-bg-subtle); }
.rich-select__option[aria-selected="true"] { color: var(--color-accent); font-weight: var(--font-weight-medium); }

.rich-select__option-icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: var(--radius-sm);
  object-fit: cover;
  flex-shrink: 0;
}

.rich-select__option-label { flex: 1; }
.rich-select__option-desc  { font-size: var(--font-size-xs); color: var(--color-text-muted); }

/* Check mark for selected */
.rich-select__option-check {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
  opacity: 0;
  color: var(--color-accent);
}
.rich-select__option[aria-selected="true"] .rich-select__option-check { opacity: 1; }

/* Multi-select chips preview */
.rich-select__multi-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  flex: 1;
}

.rich-select__chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 0.1em 0.5em;
  background: var(--color-brand-100);
  color: var(--color-brand-700);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.rich-select__chip-remove {
  border: none;
  background: none;
  cursor: pointer;
  color: inherit;
  opacity: 0.6;
  padding: 0;
  line-height: 1;
  display: flex;
}
.rich-select__chip-remove:hover { opacity: 1; }

/* Footer with actions */
.rich-select__footer {
  padding: var(--space-2) var(--space-3);
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  flex-shrink: 0;
}
```

---

## 187. MULTI-STEP CHECKOUT

```css
/* ─── Checkout layout ─── */
.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: var(--space-8);
  max-width: 1000px;
  margin-inline: auto;
  padding: var(--space-8) var(--space-4);
  align-items: start;
}

@media (max-width: 768px) {
  .checkout-layout { grid-template-columns: 1fr; }
  .checkout-summary { order: -1; }
}

/* Progress steps */
.checkout-steps {
  display: flex;
  align-items: center;
  margin-block-end: var(--space-8);
  overflow: hidden;
}

.checkout-step {
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 0;
}

.checkout-step__bubble {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 2px solid var(--color-border);
  background: var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
  transition:
    background   var(--duration-normal),
    border-color var(--duration-normal),
    color        var(--duration-normal);
  color: var(--color-text-muted);
  position: relative;
  z-index: 1;
}

.checkout-step.completed .checkout-step__bubble {
  background: var(--color-success-500);
  border-color: var(--color-success-500);
  color: white;
}

.checkout-step.active .checkout-step__bubble {
  border-color: var(--color-accent);
  color: var(--color-accent);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--color-accent) 15%, transparent);
}

.checkout-step__label {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-muted);
  padding-inline-start: var(--space-2);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.checkout-step.active .checkout-step__label { color: var(--color-accent); }
.checkout-step.completed .checkout-step__label { color: var(--color-text); }

/* Connector line */
.checkout-step__line {
  flex: 1;
  height: 2px;
  background: var(--color-border);
  margin-inline: var(--space-2);
  transition: background var(--duration-normal);
}

.checkout-step.completed + .checkout-step .checkout-step__line { background: var(--color-success-400); }

/* Form sections */
.checkout-form-section {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  margin-block-end: var(--space-4);
}

.checkout-section-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
}

.checkout-section-num {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--color-accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
}

.checkout-section-title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }
.checkout-section-edit  { margin-inline-start: auto; font-size: var(--font-size-xs); color: var(--color-accent); cursor: pointer; }

.checkout-section-body { padding: var(--space-5); }

/* Address form grid */
.address-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}
.address-grid .full { grid-column: 1 / -1; }

/* Summary panel */
.checkout-summary {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  position: sticky;
  top: var(--space-4);
}

.summary-item {
  display: flex;
  gap: var(--space-3);
  padding-block: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}
.summary-item:last-of-type { border: none; }

.summary-item-thumb {
  width: 3.5rem;
  height: 3.5rem;
  object-fit: cover;
  border-radius: var(--radius-md);
  background: var(--color-bg-muted);
  flex-shrink: 0;
  position: relative;
}

.summary-item-qty {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 1.25rem;
  height: 1.25rem;
  background: var(--color-text);
  color: var(--color-bg);
  border-radius: 50%;
  font-size: 0.625rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.summary-item-info { flex: 1; min-width: 0; }
.summary-item-name { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }
.summary-item-variant { font-size: var(--font-size-xs); color: var(--color-text-muted); }
.summary-item-price { font-weight: var(--font-weight-semibold); font-variant-numeric: tabular-nums; white-space: nowrap; }

.summary-totals { margin-block-start: var(--space-4); }

.summary-line {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-sm);
  padding-block: var(--space-1);
}
.summary-line--total {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-base);
  padding-block-start: var(--space-3);
  margin-block-start: var(--space-2);
  border-top: 2px solid var(--color-border);
}
```

---

## 188. RESPONSIVE TABLES — ADVANCED

```css
/* ─── Responsive table strategies ─── */

/* Strategy 1: Horizontal scroll with freeze */
.table-freeze-wrap {
  overflow-x: auto;
  border-radius: var(--radius-xl);
  border: 1px solid var(--color-border);
  position: relative;
}

.table-freeze {
  width: max-content;
  min-width: 100%;
  border-collapse: collapse;
}

.table-freeze thead th,
.table-freeze tbody td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
  font-size: var(--font-size-sm);
  text-align: start;
}

.table-freeze thead th {
  background: var(--color-bg-subtle);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  color: var(--color-text-muted);
  position: sticky;
  top: 0;
  z-index: 2;
}

/* Frozen first column */
.table-freeze .col-freeze {
  position: sticky;
  left: 0;
  z-index: 1;
  background: var(--color-surface);
  box-shadow: 1px 0 0 var(--color-border);
}

.table-freeze thead .col-freeze {
  z-index: 3;
  background: var(--color-bg-subtle);
}

/* Strategy 2: Card layout on mobile */
@media (max-width: 640px) {
  .table-cards { display: block; }
  .table-cards thead { display: none; }
  .table-cards tbody { display: block; }
  .table-cards tr {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-2) var(--space-4);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-xl);
    padding: var(--space-4);
    margin-block-end: var(--space-3);
  }
  .table-cards td {
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-size: var(--font-size-sm);
    border: none;
    padding: 0;
  }
  .table-cards td::before {
    content: attr(data-label);
    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-semibold);
    text-transform: uppercase;
    letter-spacing: var(--letter-spacing-wide);
    color: var(--color-text-muted);
  }
  /* Full-width cells */
  .table-cards td.full { grid-column: 1 / -1; }
}

/* Strategy 3: Priority columns */
/* JS hides low-priority columns based on viewport */
.table-col--p1 { /* always shown */ }
.table-col--p2 { /* hidden below 480px */ }
.table-col--p3 { /* hidden below 640px */ }
.table-col--p4 { /* hidden below 768px */ }

@media (max-width: 480px) { .table-col--p2 { display: none; } }
@media (max-width: 640px) { .table-col--p3 { display: none; } }
@media (max-width: 768px) { .table-col--p4 { display: none; } }

/* Virtual row hover indicator */
.vrow-highlight {
  position: absolute;
  left: 0;
  right: 0;
  background: var(--color-bg-subtle);
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-fast);
  height: var(--row-height, 48px);
  top: var(--row-top, 0);
}
.table-freeze-wrap:hover .vrow-highlight { opacity: 1; }

/* Expandable row */
.expandable-row td { padding: 0; }
.expandable-row-content {
  overflow: hidden;
  max-height: 0;
  transition: max-height 0.3s var(--ease-out);
  padding-inline: var(--space-4);
}
.expandable-row.open .expandable-row-content {
  max-height: 500px;
  padding-block: var(--space-4);
}

.expand-toggle {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-muted);
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  transition: rotate var(--duration-fast), color var(--duration-fast);
}
.expandable-row.open .expand-toggle { rotate: 90deg; color: var(--color-accent); }
```

---

## 189. MICRO-TYPOGRAPHY

```css
/* ─── Advanced micro-typography utilities ─── */

/* Hanging punctuation */
.hang-quotes {
  hanging-punctuation: first last allow-end;
}

.hang-indent {
  text-indent: -0.5em;
  padding-inline-start: 0.5em;
}

/* Proper quotation marks */
:lang(en) q { quotes: '\201C' '\201D' '\2018' '\2019'; }
:lang(de) q { quotes: '\201E' '\201C' '\201A' '\2018'; }
:lang(ru) q { quotes: '\00AB' '\00BB' '\2039' '\203A'; }
:lang(fr) q { quotes: '\00AB\202F' '\202F\00BB' '\2039\202F' '\202F\203A'; }

/* Smart dashes */
abbr[title] {
  text-decoration: underline dotted;
  cursor: help;
}

/* Ordinals: 1st, 2nd */
.ordinal {
  font-feature-settings: 'ordn' 1;
  font-variant-numeric: ordinal;
}

/* Fractions: ½ */
.fraction {
  font-feature-settings: 'frac' 1;
  font-variant-numeric: diagonal-fractions;
}

/* Tabular numbers (tables, prices) */
.tabular {
  font-feature-settings: 'tnum' 1;
  font-variant-numeric: tabular-nums;
}

/* Old-style numbers (prose) */
.oldstyle {
  font-feature-settings: 'onum' 1;
  font-variant-numeric: oldstyle-nums;
}

/* Small caps */
.small-caps {
  font-variant-caps: small-caps;
  font-feature-settings: 'smcp' 1;
}

.all-small-caps {
  font-variant-caps: all-small-caps;
  font-feature-settings: 'c2sc' 1, 'smcp' 1;
}

/* Kerning */
.kern-on  { font-kerning: normal; font-feature-settings: 'kern' 1; }
.kern-off { font-kerning: none; }

/* Text optical alignment */
.optical-align { text-autospace: normal; }

/* Superscript / subscript */
.superscript {
  font-size: 0.7em;
  vertical-align: super;
  font-feature-settings: 'sups' 1;
  font-variant-position: super;
}

.subscript {
  font-size: 0.7em;
  vertical-align: sub;
  font-feature-settings: 'subs' 1;
  font-variant-position: sub;
}

/* Measure (optimal line length) */
.measure      { max-width: 65ch; }  /* optimal prose */
.measure-wide { max-width: 85ch; }  /* wide columns */
.measure-narrow { max-width: 45ch; } /* narrow columns */

/* Widow/orphan control */
.no-orphans {
  text-wrap: pretty;    /* CSS */
  widows: 3;
  orphans: 3;
}

/* Ellipsis on single line */
.ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
}

/* Multi-line clamp */
.clamp-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Hyphenation zones */
.hyphen-auto { hyphens: auto; hyphenate-limit-chars: 6 3 2; }
.hyphen-manual { hyphens: manual; } /* only at &shy; */
.hyphen-none   { hyphens: none; overflow-wrap: break-word; }

/* Word break strategies */
.break-normal  { word-break: normal; overflow-wrap: normal; }
.break-words   { overflow-wrap: break-word; word-break: break-word; }
.break-all     { word-break: break-all; }
.break-anywhere{ overflow-wrap: anywhere; }

/* Typography scale debugging */
.debug-typography * {
  background: linear-gradient(
    to bottom,
    oklch(0.7 0.15 240 / 0.08) 0,
    oklch(0.7 0.15 240 / 0.08) 1px,
    transparent 1px
  ) !important;
  background-size: 1px 1.5rem !important;
}
```

---

## 190. FLOATING UI PATTERNS

```css
/* ─── Floating action button (FAB) ─── */
.fab {
  position: fixed;
  inset-block-end: var(--space-6);
  inset-inline-end: var(--space-6);
  z-index: var(--z-fixed);
  display: flex;
  flex-direction: column-reverse;
  align-items: flex-end;
  gap: var(--space-3);
}

.fab-main {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  background: var(--color-accent);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  box-shadow: var(--shadow-xl);
  transition:
    scale      var(--duration-fast) var(--ease-bounce),
    rotate     var(--duration-slow) var(--ease-out),
    box-shadow var(--duration-fast);
  position: relative;
  z-index: 1;
}

.fab-main:hover {
  scale: 1.08;
  box-shadow: 0 8px 30px color-mix(in srgb, var(--color-accent) 40%, transparent);
}

.fab[data-open="true"] .fab-main { rotate: 45deg; }

/* Speed dial items */
.fab-items {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--space-3);
  opacity: 0;
  translate: 0 10px;
  pointer-events: none;
  transition:
    opacity   var(--duration-normal) var(--ease-out),
    translate var(--duration-normal) var(--ease-out);
}

.fab[data-open="true"] .fab-items {
  opacity: 1;
  translate: 0 0;
  pointer-events: auto;
}

.fab-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  animation: fab-item-in 0.3s var(--ease-bounce) backwards;
}

.fab-item:nth-child(1) { animation-delay: 0.05s; }
.fab-item:nth-child(2) { animation-delay: 0.1s; }
.fab-item:nth-child(3) { animation-delay: 0.15s; }

@keyframes fab-item-in {
  from { opacity: 0; translate: 0 20px; }
}

.fab-item__label {
  background: var(--color-neutral-900);
  color: white;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: 0.3em 0.75em;
  border-radius: var(--radius-md);
  white-space: nowrap;
  box-shadow: var(--shadow-md);
}

.fab-item__btn {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 50%;
  background: var(--color-surface);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
  font-size: 1.125rem;
  color: var(--color-text);
  transition: scale var(--duration-fast) var(--ease-bounce), box-shadow var(--duration-fast);
}
.fab-item__btn:hover { scale: 1.1; box-shadow: var(--shadow-xl); }

/* ─── Floating toolbar (text selection) ─── */
.float-toolbar {
  position: fixed;
  background: var(--color-neutral-900);
  border-radius: var(--radius-xl);
  padding: var(--space-1) var(--space-2);
  display: flex;
  align-items: center;
  gap: 2px;
  box-shadow: var(--shadow-xl);
  z-index: var(--z-popover);
  animation: float-toolbar-in 0.15s var(--ease-out);
  top: var(--toolbar-y, 100px);
  left: var(--toolbar-x, 50%);
  translate: -50% calc(-100% - 8px);
}

@keyframes float-toolbar-in {
  from { opacity: 0; scale: 0.9; }
}

/* Arrow */
.float-toolbar::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  translate: -50% 0;
  border: 5px solid transparent;
  border-top-color: var(--color-neutral-900);
}

.float-toolbar-btn {
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  color: rgba(255 255 255 / 0.8);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--duration-fast), color var(--duration-fast);
}
.float-toolbar-btn:hover { background: rgba(255 255 255 / 0.15); color: white; }
.float-toolbar-btn.active { background: rgba(255 255 255 / 0.2); color: white; }

.float-toolbar-divider {
  width: 1px;
  height: 1.25rem;
  background: rgba(255 255 255 / 0.15);
  margin-inline: 2px;
}
```

---

## 191. SPOTLIGHT SEARCH

```css
/* ─── App-wide spotlight search (CMD+K) ─── */
.spotlight-overlay {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 0.5);
  backdrop-filter: blur(6px);
  z-index: var(--z-modal);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-block-start: 15dvh;
  padding-inline: var(--space-4);
}

.spotlight {
  width: 100%;
  max-width: 580px;
  background: var(--color-surface);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-2xl);
  overflow: hidden;
  animation: spotlight-in 0.2s var(--ease-bounce);
}

@keyframes spotlight-in {
  from { opacity: 0; scale: 0.95; translate: 0 -12px; }
}

.spotlight-input-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.spotlight-icon { color: var(--color-text-muted); font-size: 1.125rem; flex-shrink: 0; }

.spotlight-input {
  flex: 1;
  border: none;
  background: none;
  font: inherit;
  font-size: var(--font-size-lg);
  color: var(--color-text);
  outline: none;
}
.spotlight-input::placeholder { color: var(--color-text-subtle); }

.spotlight-kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.15em 0.4em;
  background: var(--color-bg-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  box-shadow: 0 1px 0 var(--color-border);
  flex-shrink: 0;
}

/* Results */
.spotlight-results {
  max-height: 400px;
  overflow-y: auto;
  scrollbar-width: thin;
}

.spotlight-section-title {
  padding: var(--space-2) var(--space-5);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  position: sticky;
  top: 0;
  background: var(--color-surface);
}

.spotlight-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0.625rem var(--space-5);
  cursor: pointer;
  transition: background var(--duration-fast);
  border-radius: 0;
}

.spotlight-item:hover,
.spotlight-item[aria-selected="true"] {
  background: var(--color-bg-subtle);
}

.spotlight-item[aria-selected="true"] .spotlight-item__right { opacity: 1; }

.spotlight-item__icon {
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 1rem;
  background: var(--color-bg-muted);
}

.spotlight-item__label {
  flex: 1;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.spotlight-item__label mark {
  background: var(--color-warning-200);
  color: inherit;
  font-weight: var(--font-weight-bold);
  border-radius: 2px;
}

.spotlight-item__sublabel {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.spotlight-item__right {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  opacity: 0;
  transition: opacity var(--duration-fast);
  flex-shrink: 0;
}

/* Footer hint */
.spotlight-footer {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-2) var(--space-5);
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
  font-size: var(--font-size-xs);
  color: var(--color-text-subtle);
}

/* Empty state */
.spotlight-empty {
  padding: var(--space-12);
  text-align: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
}

.spotlight-empty__icon { font-size: 2.5rem; margin-block-end: var(--space-3); }
```

---

## 192. APP LAUNCHER / GRID MENU

```css
/* ─── App grid launcher ─── */
.app-launcher {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 0.7);
  backdrop-filter: blur(20px);
  z-index: var(--z-modal);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  gap: var(--space-8);
  animation: launcher-in 0.25s var(--ease-out);
}

@keyframes launcher-in { from { opacity: 0; } }

/* Search in launcher */
.launcher-search {
  width: 100%;
  max-width: 360px;
  padding: 0.875rem 1.25rem;
  background: rgba(255 255 255 / 0.15);
  border: 1px solid rgba(255 255 255 / 0.2);
  border-radius: var(--radius-2xl);
  font: inherit;
  font-size: var(--font-size-base);
  color: white;
  outline: none;
  backdrop-filter: blur(4px);
  transition: background var(--duration-fast), border-color var(--duration-fast);
}
.launcher-search::placeholder { color: rgba(255 255 255 / 0.5); }
.launcher-search:focus {
  background: rgba(255 255 255 / 0.2);
  border-color: rgba(255 255 255 / 0.4);
}

/* App grid */
.app-grid {
  display: grid;
  grid-template-columns: repeat(var(--cols, 6), 1fr);
  gap: var(--space-6) var(--space-4);
  max-width: 700px;
  width: 100%;
}

@media (max-width: 600px) { .app-grid { --cols: 4; } }
@media (max-width: 400px) { .app-grid { --cols: 3; } }

/* App icon */
.app-icon-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  background: none;
  border: none;
  padding: var(--space-2);
  border-radius: var(--radius-xl);
  color: white;
  transition:
    background  var(--duration-fast),
    scale       var(--duration-fast) var(--ease-bounce);
  animation: app-icon-in 0.3s var(--ease-bounce) backwards;
  animation-delay: calc(var(--i, 0) * 30ms);
}

@keyframes app-icon-in {
  from { opacity: 0; scale: 0.7; }
}

.app-icon-btn:hover {
  background: rgba(255 255 255 / 0.12);
  scale: 1.05;
}

.app-icon-btn:active { scale: 0.95; }

.app-icon {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: var(--radius-xl);
  background: var(--icon-bg, var(--color-accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  box-shadow: 0 4px 12px rgba(0 0 0 / 0.3);
  position: relative;
  overflow: hidden;
}

/* Notification badge on app icon */
.app-icon__badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 1.25rem;
  height: 1.25rem;
  background: var(--color-danger-500);
  border-radius: var(--radius-full);
  font-size: 0.625rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid transparent;
  padding-inline: 2px;
}

.app-icon-label {
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.9);
  text-shadow: 0 1px 3px rgba(0 0 0 / 0.5);
  max-width: 5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Dock bar */
.app-dock {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: rgba(255 255 255 / 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255 255 255 / 0.15);
  border-radius: var(--radius-2xl);
  padding: var(--space-3) var(--space-4);
  box-shadow: 0 8px 32px rgba(0 0 0 / 0.3);
}

.dock-divider {
  width: 1px;
  height: 2.5rem;
  background: rgba(255 255 255 / 0.15);
  margin-inline: var(--space-2);
}

/* Dock icon magnification on hover (macOS style) */
.app-dock:hover .app-icon-btn {
  transition: scale 0.15s var(--ease-out);
}

.app-icon-btn {
  --scale: 1;
  scale: var(--scale);
}

/* JS sets --scale based on distance from cursor */
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                     PART 13 — COMPLETE                               ║
║  Chapters 182–192 | 11 new chapters | Output: css-guide-part13.md   ║
╚══════════════════════════════════════════════════════════════════════╝
```
