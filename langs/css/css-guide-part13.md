\# CSS GUIDE — PART 13

\## Chapters 182–196



\---



\## 182. SUBSCRIPTION \& BILLING UI



```css

/\* ─── Current plan card ─── \*/

.plan-card-current {

&#x20; background: linear-gradient(

&#x20;   135deg,

&#x20;   color-mix(in srgb, var(--color-accent) 8%, var(--color-surface)),

&#x20;   var(--color-surface)

&#x20; );

&#x20; border: 2px solid var(--color-accent);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-6);

&#x20; position: relative;

&#x20; overflow: hidden;

}



.plan-card-current::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-block-start: 0;

&#x20; inset-inline-end: 0;

&#x20; width: 120px;

&#x20; height: 120px;

&#x20; background: radial-gradient(circle, color-mix(in srgb, var(--color-accent) 15%, transparent), transparent 70%);

&#x20; pointer-events: none;

}



.plan-name { font-size: var(--step-1); font-weight: var(--font-weight-black); }

.plan-price {

&#x20; font-size: var(--step-3);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-variant-numeric: tabular-nums;

&#x20; line-height: 1;

&#x20; margin-block: var(--space-3);

}

.plan-price span { font-size: var(--font-size-base); font-weight: var(--font-weight-normal); color: var(--color-text-muted); }

.plan-renews { font-size: var(--font-size-xs); color: var(--color-text-muted); }



/\* Usage meter \*/

.usage-meter {

&#x20; margin-block-start: var(--space-5);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-3);

}



.usage-row {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-1);

}



.usage-header {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

}



.usage-bar {

&#x20; height: 6px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

}



.usage-fill {

&#x20; height: 100%;

&#x20; border-radius: inherit;

&#x20; width: var(--usage, 0%);

&#x20; background: var(--color-accent);

&#x20; transition: width 0.6s var(--ease-out);

}



.usage-fill.warning { background: var(--color-warning-500); }

.usage-fill.critical { background: var(--color-danger-500); }



/\* Invoice table \*/

.invoice-list {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: 0;

}



.invoice-row {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr auto auto auto;

&#x20; gap: var(--space-4);

&#x20; align-items: center;

&#x20; padding: var(--space-3) 0;

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; font-size: var(--font-size-sm);

}

.invoice-row:last-child { border: none; }



.invoice-date { color: var(--color-text-muted); font-variant-numeric: tabular-nums; }

.invoice-amount { font-weight: var(--font-weight-semibold); font-variant-numeric: tabular-nums; }



.invoice-status {

&#x20; padding: 0.15em 0.5em;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

}

.invoice-status--paid    { background: var(--color-success-100); color: var(--color-success-700); }

.invoice-status--pending { background: var(--color-warning-100); color: var(--color-warning-700); }

.invoice-status--failed  { background: var(--color-danger-100);  color: var(--color-danger-700); }



.invoice-download {

&#x20; color: var(--color-accent);

&#x20; font-size: var(--font-size-xs);

&#x20; text-decoration: none;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25em;

}

.invoice-download:hover { text-decoration: underline; }



/\* Cancel confirmation \*/

.cancel-confirm {

&#x20; background: var(--color-danger-100);

&#x20; border: 1px solid var(--color-danger-200);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-6);

}



.cancel-confirm\_\_title {

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-danger-700);

&#x20; margin-block-end: var(--space-2);

}



.cancel-confirm\_\_desc {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-danger-600);

&#x20; margin-block-end: var(--space-5);

&#x20; line-height: 1.6;

}



/\* Downgrade prompt \*/

.downgrade-features {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

&#x20; margin-block: var(--space-4);

}



.downgrade-feature {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-danger-600);

}

.downgrade-feature::before { content: '✕'; font-weight: bold; color: var(--color-danger-500); }

```



\---



\## 183. FLASH SALE \& PROMO UI



```css

/\* ─── Flash sale banner ─── \*/

.flash-banner {

&#x20; background: linear-gradient(135deg, #ff4d00, #ff0080);

&#x20; color: white;

&#x20; padding: var(--space-3) var(--space-6);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-4);

&#x20; flex-wrap: wrap;

&#x20; position: relative;

&#x20; overflow: hidden;

}



/\* Animated background stripes \*/

.flash-banner::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: repeating-linear-gradient(

&#x20;   45deg,

&#x20;   transparent 0,

&#x20;   transparent 20px,

&#x20;   rgba(255 255 255 / 0.05) 20px,

&#x20;   rgba(255 255 255 / 0.05) 40px

&#x20; );

&#x20; animation: stripe-scroll 3s linear infinite;

}



@keyframes stripe-scroll {

&#x20; from { background-position: 0 0; }

&#x20; to   { background-position: 56px 0; }

}



.flash-banner > \* { position: relative; z-index: 1; }



.flash-label {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-size: var(--font-size-base);

&#x20; letter-spacing: 0.05em;

&#x20; text-transform: uppercase;

}



.flash-label\_\_bolt { animation: bolt-pulse 0.5s ease-in-out infinite alternate; }

@keyframes bolt-pulse { from { scale: 1; } to { scale: 1.3; } }



.flash-text { font-size: var(--font-size-sm); }



.flash-countdown-inline {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; font-family: var(--font-mono);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-size: var(--font-size-lg);

&#x20; font-variant-numeric: tabular-nums;

&#x20; background: rgba(0 0 0 / 0.2);

&#x20; padding: 0.2em 0.6em;

&#x20; border-radius: var(--radius-md);

}



/\* Discount badge \*/

.discount-badge {

&#x20; position: absolute;

&#x20; top: -8px;

&#x20; right: -8px;

&#x20; width: 52px;

&#x20; height: 52px;

&#x20; background: var(--color-warning-400);

&#x20; border-radius: 50%;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: var(--font-weight-black);

&#x20; color: var(--color-warning-900);

&#x20; animation: badge-spin 4s linear infinite;

&#x20; box-shadow: var(--shadow-md);

&#x20; z-index: 1;

}



@keyframes badge-spin {

&#x20; 0%, 90%, 100% { rotate: 0deg; }

&#x20; 45%           { rotate: -15deg; }

&#x20; 50%           { rotate: 15deg; }

}



.discount-badge\_\_percent { font-size: 1rem; line-height: 1; }

.discount-badge\_\_off     { font-size: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }



/\* Product with sale price \*/

.sale-price-group {

&#x20; display: flex;

&#x20; align-items: baseline;

&#x20; gap: var(--space-2);

}



.sale-price-original {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: line-through;

&#x20; font-variant-numeric: tabular-nums;

}



.sale-price-new {

&#x20; font-size: var(--font-size-xl);

&#x20; font-weight: var(--font-weight-black);

&#x20; color: var(--color-danger-500);

&#x20; font-variant-numeric: tabular-nums;

}



.sale-save-label {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-success-600);

&#x20; background: var(--color-success-100);

&#x20; padding: 0.15em 0.5em;

&#x20; border-radius: var(--radius-full);

}



/\* Coupon code input \*/

.coupon-input-group {

&#x20; display: flex;

&#x20; gap: var(--space-2);

}



.coupon-input {

&#x20; flex: 1;

&#x20; padding: 0.625rem 0.875rem;

&#x20; border: 2px dashed var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; font-family: var(--font-mono);

&#x20; letter-spacing: 0.08em;

&#x20; text-transform: uppercase;

&#x20; background: var(--color-bg-subtle);

&#x20; outline: none;

&#x20; transition: border-color var(--duration-fast), background var(--duration-fast);

}

.coupon-input:focus {

&#x20; border-color: var(--color-accent);

&#x20; background: var(--color-surface);

&#x20; border-style: solid;

}

.coupon-input.applied {

&#x20; border-color: var(--color-success-400);

&#x20; border-style: solid;

&#x20; background: var(--color-success-100);

&#x20; color: var(--color-success-700);

}

.coupon-input.error {

&#x20; border-color: var(--color-danger-400);

&#x20; border-style: solid;

&#x20; animation: coupon-shake 0.3s ease-out;

}



@keyframes coupon-shake {

&#x20; 0%, 100% { translate: 0; }

&#x20; 25%       { translate: -6px; }

&#x20; 75%       { translate: 6px; }

}

```



\---



\## 184. KIOSK UI PATTERNS



```css

/\* ─── Kiosk full-screen layout ─── \*/

.kiosk {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; background: var(--kiosk-bg, #0a0a1a);

&#x20; color: var(--kiosk-text, white);

&#x20; font-family: var(--font-sans);

&#x20; overflow: hidden;

&#x20; cursor: none; /\* hide system cursor \*/

&#x20; display: flex;

&#x20; flex-direction: column;

}



/\* Kiosk header \*/

.kiosk-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-6) var(--space-8);

&#x20; background: rgba(255 255 255 / 0.05);

&#x20; border-bottom: 1px solid rgba(255 255 255 / 0.1);

}



.kiosk-clock {

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--step-2);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-variant-numeric: tabular-nums;

&#x20; color: rgba(255 255 255 / 0.8);

}



/\* Kiosk main area \*/

.kiosk-main {

&#x20; flex: 1;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; padding: var(--space-12);

&#x20; gap: var(--space-8);

}



/\* Big tap targets (min 80px for touchscreen) \*/

.kiosk-btn {

&#x20; min-height: 80px;

&#x20; min-width: 180px;

&#x20; padding: var(--space-5) var(--space-8);

&#x20; border-radius: var(--radius-2xl);

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; font: inherit;

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-bold);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-3);

&#x20; transition:

&#x20;   scale      0.12s var(--ease-bounce),

&#x20;   box-shadow 0.12s;

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.05em;

}



.kiosk-btn:active { scale: 0.96; }

.kiosk-btn--primary {

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; box-shadow: 0 0 40px color-mix(in srgb, var(--color-accent) 40%, transparent);

}

.kiosk-btn--secondary {

&#x20; background: rgba(255 255 255 / 0.1);

&#x20; color: white;

&#x20; border: 2px solid rgba(255 255 255 / 0.2);

}

.kiosk-btn--large {

&#x20; min-height: 120px;

&#x20; font-size: var(--step-2);

&#x20; padding: var(--space-6) var(--space-10);

}



/\* Touch ripple \*/

.kiosk-btn {

&#x20; position: relative;

&#x20; overflow: hidden;

}

.kiosk-btn::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; width: 200px;

&#x20; height: 200px;

&#x20; background: rgba(255 255 255 / 0.2);

&#x20; border-radius: 50%;

&#x20; translate: -50% -50%;

&#x20; left: var(--rx, 50%);

&#x20; top:  var(--ry, 50%);

&#x20; scale: 0;

&#x20; opacity: 0;

}

.kiosk-btn:active::after {

&#x20; animation: kiosk-ripple 0.5s ease-out;

}

@keyframes kiosk-ripple {

&#x20; from { scale: 0; opacity: 1; }

&#x20; to   { scale: 3; opacity: 0; }

}



/\* Idle screen \*/

.kiosk-idle {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: var(--kiosk-bg);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-8);

&#x20; z-index: 50;

&#x20; animation: idle-appear 0.5s var(--ease-out);

}



@keyframes idle-appear { from { opacity: 0; } }



.kiosk-idle\_\_tap {

&#x20; font-size: var(--step-3);

&#x20; font-weight: var(--font-weight-black);

&#x20; text-align: center;

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.1em;

&#x20; animation: tap-pulse 2s ease-in-out infinite;

}



@keyframes tap-pulse {

&#x20; 0%, 100% { opacity: 1; scale: 1; }

&#x20; 50%       { opacity: 0.6; scale: 0.98; }

}



/\* Kiosk numpad \*/

.kiosk-numpad {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(3, 1fr);

&#x20; gap: var(--space-3);

&#x20; max-width: 320px;

}



.kiosk-key {

&#x20; aspect-ratio: 1.2;

&#x20; border-radius: var(--radius-xl);

&#x20; border: 2px solid rgba(255 255 255 / 0.15);

&#x20; background: rgba(255 255 255 / 0.08);

&#x20; color: white;

&#x20; font-size: var(--step-2);

&#x20; font-weight: var(--font-weight-bold);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; transition: background 0.1s, scale 0.1s var(--ease-bounce);

&#x20; font-variant-numeric: tabular-nums;

}

.kiosk-key:active { background: rgba(255 255 255 / 0.25); scale: 0.94; }



.kiosk-key--del { background: rgba(255 100 100 / 0.15); border-color: rgba(255 100 100 / 0.3); }

.kiosk-key--ok  { background: var(--color-accent); border-color: transparent; }

.kiosk-key--zero { grid-column: span 2; aspect-ratio: auto; padding: var(--space-4); }

```



\---



\## 185. SCROLLYTELLING



```css

/\* ─── Scrollytelling layout ─── \*/

.scrolly {

&#x20; position: relative;

}



/\* Sticky graphic panel \*/

.scrolly-graphic {

&#x20; position: sticky;

&#x20; top: 0;

&#x20; height: 100dvh;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; pointer-events: none;

&#x20; z-index: 0;

}



/\* Story steps \*/

.scrolly-steps {

&#x20; position: relative;

&#x20; z-index: 1;

&#x20; padding-block-end: 100dvh;

}



.scrolly-step {

&#x20; max-width: 400px;

&#x20; padding: var(--space-8) var(--space-6);

&#x20; margin-inline-start: var(--space-8);

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; box-shadow: var(--shadow-lg);

&#x20; opacity: 0.3;

&#x20; transition: opacity 0.3s var(--ease-out);

&#x20; margin-block-end: 40dvh;

}



.scrolly-step.active { opacity: 1; }

.scrolly-step.active + .scrolly-step { opacity: 0.3; }



/\* Step content \*/

.scrolly-step\_\_num {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-black);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-accent);

&#x20; margin-block-end: var(--space-3);

}



.scrolly-step\_\_title {

&#x20; font-size: var(--step-1);

&#x20; font-weight: var(--font-weight-bold);

&#x20; margin-block-end: var(--space-3);

&#x20; text-wrap: balance;

}



.scrolly-step\_\_text {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.7;

}



/\* Graphic elements \*/

.scrolly-vis {

&#x20; width: min(500px, 55vw);

&#x20; aspect-ratio: 1;

&#x20; position: relative;

}



/\* Transition between vis states \*/

.vis-element {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; opacity: 0;

&#x20; transition: opacity 0.5s var(--ease-out), scale 0.5s var(--ease-out), translate 0.5s var(--ease-out);

&#x20; scale: 0.95;

}



.vis-element.active {

&#x20; opacity: 1;

&#x20; scale: 1;

&#x20; translate: 0 0;

}



/\* ─── Parallax sections ─── \*/

.parallax-section {

&#x20; position: relative;

&#x20; overflow: hidden;

&#x20; height: 80dvh;

}



.parallax-bg {

&#x20; position: absolute;

&#x20; inset: -20%;

&#x20; background-size: cover;

&#x20; background-position: center;

&#x20; will-change: transform;

&#x20; /\* JS: el.style.transform = `translateY(${scrollY \* 0.3}px)` \*/

}



.parallax-content {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; z-index: 1;

&#x20; /\* Content moves slower or not at all \*/

}



/\* Native scroll-driven parallax \*/

.parallax-native {

&#x20; animation: parallax-y linear both;

&#x20; animation-timeline: scroll(root block);

}



@keyframes parallax-y {

&#x20; from { translate: 0 calc(var(--parallax-start, -10%)); }

&#x20; to   { translate: 0 calc(var(--parallax-end, 10%)); }

}

```



\---



\## 186. RICH DROPDOWN MENUS



```css

/\* ─── Mega select dropdown ─── \*/

.rich-select {

&#x20; position: relative;

}



.rich-select\_\_trigger {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: 0.625rem 0.875rem;

&#x20; border: 1px solid var(--color-border-strong);

&#x20; border-radius: var(--radius-lg);

&#x20; background: var(--color-surface);

&#x20; cursor: pointer;

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; min-width: 220px;

&#x20; text-align: start;

&#x20; transition: border-color var(--duration-fast), box-shadow var(--duration-fast);

}



.rich-select\_\_trigger:focus-visible {

&#x20; outline: none;

&#x20; border-color: var(--color-accent);

&#x20; box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 15%, transparent);

}



.rich-select\_\_value { flex: 1; }

.rich-select\_\_placeholder { color: var(--color-text-subtle); }



.rich-select\_\_icon {

&#x20; color: var(--color-text-muted);

&#x20; transition: rotate var(--duration-fast) var(--ease-out);

&#x20; flex-shrink: 0;

}



.rich-select\[data-open="true"] .rich-select\_\_icon { rotate: 180deg; }



/\* Dropdown panel \*/

.rich-select\_\_panel {

&#x20; position: absolute;

&#x20; top: calc(100% + 4px);

&#x20; left: 0;

&#x20; min-width: 100%;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; box-shadow: var(--shadow-xl);

&#x20; z-index: var(--z-dropdown);

&#x20; overflow: hidden;

&#x20; animation: dropdown-in 0.15s var(--ease-out);

&#x20; max-height: 320px;

&#x20; display: flex;

&#x20; flex-direction: column;

}



@keyframes dropdown-in {

&#x20; from { opacity: 0; translate: 0 -6px; scale: 0.98; }

}



/\* Search inside dropdown \*/

.rich-select\_\_search {

&#x20; padding: var(--space-2) var(--space-3);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; flex-shrink: 0;

}



.rich-select\_\_search input {

&#x20; width: 100%;

&#x20; padding: 0.375rem 0.625rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; background: var(--color-bg-subtle);

&#x20; outline: none;

}



/\* Options list \*/

.rich-select\_\_list {

&#x20; overflow-y: auto;

&#x20; scrollbar-width: thin;

&#x20; flex: 1;

&#x20; padding: var(--space-1);

}



/\* Group heading \*/

.rich-select\_\_group-title {

&#x20; padding: var(--space-1) var(--space-3);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; position: sticky;

&#x20; top: 0;

&#x20; background: var(--color-surface);

}



/\* Option \*/

.rich-select\_\_option {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: 0.5rem var(--space-3);

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; font-size: var(--font-size-sm);

&#x20; transition: background var(--duration-fast);

}

.rich-select\_\_option:hover,

.rich-select\_\_option\[aria-selected="true"] { background: var(--color-bg-subtle); }

.rich-select\_\_option\[aria-selected="true"] { color: var(--color-accent); font-weight: var(--font-weight-medium); }



.rich-select\_\_option-icon {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: var(--radius-sm);

&#x20; object-fit: cover;

&#x20; flex-shrink: 0;

}



.rich-select\_\_option-label { flex: 1; }

.rich-select\_\_option-desc  { font-size: var(--font-size-xs); color: var(--color-text-muted); }



/\* Check mark for selected \*/

.rich-select\_\_option-check {

&#x20; width: 1rem;

&#x20; height: 1rem;

&#x20; flex-shrink: 0;

&#x20; opacity: 0;

&#x20; color: var(--color-accent);

}

.rich-select\_\_option\[aria-selected="true"] .rich-select\_\_option-check { opacity: 1; }



/\* Multi-select chips preview \*/

.rich-select\_\_multi-preview {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: 4px;

&#x20; flex: 1;

}



.rich-select\_\_chip {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: 4px;

&#x20; padding: 0.1em 0.5em;

&#x20; background: var(--color-brand-100);

&#x20; color: var(--color-brand-700);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

}



.rich-select\_\_chip-remove {

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; color: inherit;

&#x20; opacity: 0.6;

&#x20; padding: 0;

&#x20; line-height: 1;

&#x20; display: flex;

}

.rich-select\_\_chip-remove:hover { opacity: 1; }



/\* Footer with actions \*/

.rich-select\_\_footer {

&#x20; padding: var(--space-2) var(--space-3);

&#x20; border-top: 1px solid var(--color-border);

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; font-size: var(--font-size-xs);

&#x20; flex-shrink: 0;

}

```



\---



\## 187. MULTI-STEP CHECKOUT



```css

/\* ─── Checkout layout ─── \*/

.checkout-layout {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 380px;

&#x20; gap: var(--space-8);

&#x20; max-width: 1000px;

&#x20; margin-inline: auto;

&#x20; padding: var(--space-8) var(--space-4);

&#x20; align-items: start;

}



@media (max-width: 768px) {

&#x20; .checkout-layout { grid-template-columns: 1fr; }

&#x20; .checkout-summary { order: -1; }

}



/\* Progress steps \*/

.checkout-steps {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; margin-block-end: var(--space-8);

&#x20; overflow: hidden;

}



.checkout-step {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; flex: 1;

&#x20; min-width: 0;

}



.checkout-step\_\_bubble {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: 50%;

&#x20; border: 2px solid var(--color-border);

&#x20; background: var(--color-surface);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; flex-shrink: 0;

&#x20; transition:

&#x20;   background   var(--duration-normal),

&#x20;   border-color var(--duration-normal),

&#x20;   color        var(--duration-normal);

&#x20; color: var(--color-text-muted);

&#x20; position: relative;

&#x20; z-index: 1;

}



.checkout-step.completed .checkout-step\_\_bubble {

&#x20; background: var(--color-success-500);

&#x20; border-color: var(--color-success-500);

&#x20; color: white;

}



.checkout-step.active .checkout-step\_\_bubble {

&#x20; border-color: var(--color-accent);

&#x20; color: var(--color-accent);

&#x20; box-shadow: 0 0 0 4px color-mix(in srgb, var(--color-accent) 15%, transparent);

}



.checkout-step\_\_label {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

&#x20; color: var(--color-text-muted);

&#x20; padding-inline-start: var(--space-2);

&#x20; white-space: nowrap;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

}



.checkout-step.active .checkout-step\_\_label { color: var(--color-accent); }

.checkout-step.completed .checkout-step\_\_label { color: var(--color-text); }



/\* Connector line \*/

.checkout-step\_\_line {

&#x20; flex: 1;

&#x20; height: 2px;

&#x20; background: var(--color-border);

&#x20; margin-inline: var(--space-2);

&#x20; transition: background var(--duration-normal);

}



.checkout-step.completed + .checkout-step .checkout-step\_\_line { background: var(--color-success-400); }



/\* Form sections \*/

.checkout-form-section {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; margin-block-end: var(--space-4);

}



.checkout-section-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-4) var(--space-5);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; background: var(--color-bg-subtle);

}



.checkout-section-num {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; flex-shrink: 0;

}



.checkout-section-title { font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm); }

.checkout-section-edit  { margin-inline-start: auto; font-size: var(--font-size-xs); color: var(--color-accent); cursor: pointer; }



.checkout-section-body { padding: var(--space-5); }



/\* Address form grid \*/

.address-grid {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 1fr;

&#x20; gap: var(--space-4);

}

.address-grid .full { grid-column: 1 / -1; }



/\* Summary panel \*/

.checkout-summary {

&#x20; background: var(--color-bg-subtle);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-5);

&#x20; position: sticky;

&#x20; top: var(--space-4);

}



.summary-item {

&#x20; display: flex;

&#x20; gap: var(--space-3);

&#x20; padding-block: var(--space-3);

&#x20; border-bottom: 1px solid var(--color-border);

}

.summary-item:last-of-type { border: none; }



.summary-item-thumb {

&#x20; width: 3.5rem;

&#x20; height: 3.5rem;

&#x20; object-fit: cover;

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-bg-muted);

&#x20; flex-shrink: 0;

&#x20; position: relative;

}



.summary-item-qty {

&#x20; position: absolute;

&#x20; top: -6px;

&#x20; right: -6px;

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; background: var(--color-text);

&#x20; color: var(--color-bg);

&#x20; border-radius: 50%;

&#x20; font-size: 0.625rem;

&#x20; font-weight: bold;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

}



.summary-item-info { flex: 1; min-width: 0; }

.summary-item-name { font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); }

.summary-item-variant { font-size: var(--font-size-xs); color: var(--color-text-muted); }

.summary-item-price { font-weight: var(--font-weight-semibold); font-variant-numeric: tabular-nums; white-space: nowrap; }



.summary-totals { margin-block-start: var(--space-4); }



.summary-line {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; font-size: var(--font-size-sm);

&#x20; padding-block: var(--space-1);

}

.summary-line--total {

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-base);

&#x20; padding-block-start: var(--space-3);

&#x20; margin-block-start: var(--space-2);

&#x20; border-top: 2px solid var(--color-border);

}

```



\---



\## 188. RESPONSIVE TABLES — ADVANCED



```css

/\* ─── Responsive table strategies ─── \*/



/\* Strategy 1: Horizontal scroll with freeze \*/

.table-freeze-wrap {

&#x20; overflow-x: auto;

&#x20; border-radius: var(--radius-xl);

&#x20; border: 1px solid var(--color-border);

&#x20; position: relative;

}



.table-freeze {

&#x20; width: max-content;

&#x20; min-width: 100%;

&#x20; border-collapse: collapse;

}



.table-freeze thead th,

.table-freeze tbody td {

&#x20; padding: var(--space-3) var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; white-space: nowrap;

&#x20; font-size: var(--font-size-sm);

&#x20; text-align: start;

}



.table-freeze thead th {

&#x20; background: var(--color-bg-subtle);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-xs);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wide);

&#x20; color: var(--color-text-muted);

&#x20; position: sticky;

&#x20; top: 0;

&#x20; z-index: 2;

}



/\* Frozen first column \*/

.table-freeze .col-freeze {

&#x20; position: sticky;

&#x20; left: 0;

&#x20; z-index: 1;

&#x20; background: var(--color-surface);

&#x20; box-shadow: 1px 0 0 var(--color-border);

}



.table-freeze thead .col-freeze {

&#x20; z-index: 3;

&#x20; background: var(--color-bg-subtle);

}



/\* Strategy 2: Card layout on mobile \*/

@media (max-width: 640px) {

&#x20; .table-cards { display: block; }

&#x20; .table-cards thead { display: none; }

&#x20; .table-cards tbody { display: block; }

&#x20; .table-cards tr {

&#x20;   display: grid;

&#x20;   grid-template-columns: 1fr 1fr;

&#x20;   gap: var(--space-2) var(--space-4);

&#x20;   background: var(--color-surface);

&#x20;   border: 1px solid var(--color-border);

&#x20;   border-radius: var(--radius-xl);

&#x20;   padding: var(--space-4);

&#x20;   margin-block-end: var(--space-3);

&#x20; }

&#x20; .table-cards td {

&#x20;   display: flex;

&#x20;   flex-direction: column;

&#x20;   gap: 2px;

&#x20;   font-size: var(--font-size-sm);

&#x20;   border: none;

&#x20;   padding: 0;

&#x20; }

&#x20; .table-cards td::before {

&#x20;   content: attr(data-label);

&#x20;   font-size: var(--font-size-xs);

&#x20;   font-weight: var(--font-weight-semibold);

&#x20;   text-transform: uppercase;

&#x20;   letter-spacing: var(--letter-spacing-wide);

&#x20;   color: var(--color-text-muted);

&#x20; }

&#x20; /\* Full-width cells \*/

&#x20; .table-cards td.full { grid-column: 1 / -1; }

}



/\* Strategy 3: Priority columns \*/

/\* JS hides low-priority columns based on viewport \*/

.table-col--p1 { /\* always shown \*/ }

.table-col--p2 { /\* hidden below 480px \*/ }

.table-col--p3 { /\* hidden below 640px \*/ }

.table-col--p4 { /\* hidden below 768px \*/ }



@media (max-width: 480px) { .table-col--p2 { display: none; } }

@media (max-width: 640px) { .table-col--p3 { display: none; } }

@media (max-width: 768px) { .table-col--p4 { display: none; } }



/\* Virtual row hover indicator \*/

.vrow-highlight {

&#x20; position: absolute;

&#x20; left: 0;

&#x20; right: 0;

&#x20; background: var(--color-bg-subtle);

&#x20; pointer-events: none;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

&#x20; height: var(--row-height, 48px);

&#x20; top: var(--row-top, 0);

}

.table-freeze-wrap:hover .vrow-highlight { opacity: 1; }



/\* Expandable row \*/

.expandable-row td { padding: 0; }

.expandable-row-content {

&#x20; overflow: hidden;

&#x20; max-height: 0;

&#x20; transition: max-height 0.3s var(--ease-out);

&#x20; padding-inline: var(--space-4);

}

.expandable-row.open .expandable-row-content {

&#x20; max-height: 500px;

&#x20; padding-block: var(--space-4);

}



.expand-toggle {

&#x20; background: none;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; padding: var(--space-1);

&#x20; border-radius: var(--radius-sm);

&#x20; transition: rotate var(--duration-fast), color var(--duration-fast);

}

.expandable-row.open .expand-toggle { rotate: 90deg; color: var(--color-accent); }

```



\---



\## 189. MICRO-TYPOGRAPHY



```css

/\* ─── Advanced micro-typography utilities ─── \*/



/\* Hanging punctuation \*/

.hang-quotes {

&#x20; hanging-punctuation: first last allow-end;

}



.hang-indent {

&#x20; text-indent: -0.5em;

&#x20; padding-inline-start: 0.5em;

}



/\* Proper quotation marks \*/

:lang(en) q { quotes: '\\201C' '\\201D' '\\2018' '\\2019'; }

:lang(de) q { quotes: '\\201E' '\\201C' '\\201A' '\\2018'; }

:lang(ru) q { quotes: '\\00AB' '\\00BB' '\\2039' '\\203A'; }

:lang(fr) q { quotes: '\\00AB\\202F' '\\202F\\00BB' '\\2039\\202F' '\\202F\\203A'; }



/\* Smart dashes \*/

abbr\[title] {

&#x20; text-decoration: underline dotted;

&#x20; cursor: help;

}



/\* Ordinals: 1st, 2nd \*/

.ordinal {

&#x20; font-feature-settings: 'ordn' 1;

&#x20; font-variant-numeric: ordinal;

}



/\* Fractions: ½ \*/

.fraction {

&#x20; font-feature-settings: 'frac' 1;

&#x20; font-variant-numeric: diagonal-fractions;

}



/\* Tabular numbers (tables, prices) \*/

.tabular {

&#x20; font-feature-settings: 'tnum' 1;

&#x20; font-variant-numeric: tabular-nums;

}



/\* Old-style numbers (prose) \*/

.oldstyle {

&#x20; font-feature-settings: 'onum' 1;

&#x20; font-variant-numeric: oldstyle-nums;

}



/\* Small caps \*/

.small-caps {

&#x20; font-variant-caps: small-caps;

&#x20; font-feature-settings: 'smcp' 1;

}



.all-small-caps {

&#x20; font-variant-caps: all-small-caps;

&#x20; font-feature-settings: 'c2sc' 1, 'smcp' 1;

}



/\* Kerning \*/

.kern-on  { font-kerning: normal; font-feature-settings: 'kern' 1; }

.kern-off { font-kerning: none; }



/\* Text optical alignment \*/

.optical-align { text-autospace: normal; }



/\* Superscript / subscript \*/

.superscript {

&#x20; font-size: 0.7em;

&#x20; vertical-align: super;

&#x20; font-feature-settings: 'sups' 1;

&#x20; font-variant-position: super;

}



.subscript {

&#x20; font-size: 0.7em;

&#x20; vertical-align: sub;

&#x20; font-feature-settings: 'subs' 1;

&#x20; font-variant-position: sub;

}



/\* Measure (optimal line length) \*/

.measure      { max-width: 65ch; }  /\* optimal prose \*/

.measure-wide { max-width: 85ch; }  /\* wide columns \*/

.measure-narrow { max-width: 45ch; } /\* narrow columns \*/



/\* Widow/orphan control \*/

.no-orphans {

&#x20; text-wrap: pretty;    /\* CSS \*/

&#x20; widows: 3;

&#x20; orphans: 3;

}



/\* Ellipsis on single line \*/

.ellipsis {

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

&#x20; min-width: 0;

}



/\* Multi-line clamp \*/

.clamp-2-lines {

&#x20; display: -webkit-box;

&#x20; -webkit-line-clamp: 2;

&#x20; -webkit-box-orient: vertical;

&#x20; overflow: hidden;

}



/\* Hyphenation zones \*/

.hyphen-auto { hyphens: auto; hyphenate-limit-chars: 6 3 2; }

.hyphen-manual { hyphens: manual; } /\* only at \&shy; \*/

.hyphen-none   { hyphens: none; overflow-wrap: break-word; }



/\* Word break strategies \*/

.break-normal  { word-break: normal; overflow-wrap: normal; }

.break-words   { overflow-wrap: break-word; word-break: break-word; }

.break-all     { word-break: break-all; }

.break-anywhere{ overflow-wrap: anywhere; }



/\* Typography scale debugging \*/

.debug-typography \* {

&#x20; background: linear-gradient(

&#x20;   to bottom,

&#x20;   oklch(0.7 0.15 240 / 0.08) 0,

&#x20;   oklch(0.7 0.15 240 / 0.08) 1px,

&#x20;   transparent 1px

&#x20; ) !important;

&#x20; background-size: 1px 1.5rem !important;

}

```



\---



\## 190. FLOATING UI PATTERNS



```css

/\* ─── Floating action button (FAB) ─── \*/

.fab {

&#x20; position: fixed;

&#x20; inset-block-end: var(--space-6);

&#x20; inset-inline-end: var(--space-6);

&#x20; z-index: var(--z-fixed);

&#x20; display: flex;

&#x20; flex-direction: column-reverse;

&#x20; align-items: flex-end;

&#x20; gap: var(--space-3);

}



.fab-main {

&#x20; width: 3.5rem;

&#x20; height: 3.5rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 1.5rem;

&#x20; box-shadow: var(--shadow-xl);

&#x20; transition:

&#x20;   scale      var(--duration-fast) var(--ease-bounce),

&#x20;   rotate     var(--duration-slow) var(--ease-out),

&#x20;   box-shadow var(--duration-fast);

&#x20; position: relative;

&#x20; z-index: 1;

}



.fab-main:hover {

&#x20; scale: 1.08;

&#x20; box-shadow: 0 8px 30px color-mix(in srgb, var(--color-accent) 40%, transparent);

}



.fab\[data-open="true"] .fab-main { rotate: 45deg; }



/\* Speed dial items \*/

.fab-items {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: flex-end;

&#x20; gap: var(--space-3);

&#x20; opacity: 0;

&#x20; translate: 0 10px;

&#x20; pointer-events: none;

&#x20; transition:

&#x20;   opacity   var(--duration-normal) var(--ease-out),

&#x20;   translate var(--duration-normal) var(--ease-out);

}



.fab\[data-open="true"] .fab-items {

&#x20; opacity: 1;

&#x20; translate: 0 0;

&#x20; pointer-events: auto;

}



.fab-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; animation: fab-item-in 0.3s var(--ease-bounce) backwards;

}



.fab-item:nth-child(1) { animation-delay: 0.05s; }

.fab-item:nth-child(2) { animation-delay: 0.1s; }

.fab-item:nth-child(3) { animation-delay: 0.15s; }



@keyframes fab-item-in {

&#x20; from { opacity: 0; translate: 0 20px; }

}



.fab-item\_\_label {

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; padding: 0.3em 0.75em;

&#x20; border-radius: var(--radius-md);

&#x20; white-space: nowrap;

&#x20; box-shadow: var(--shadow-md);

}



.fab-item\_\_btn {

&#x20; width: 2.75rem;

&#x20; height: 2.75rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-surface);

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; box-shadow: var(--shadow-lg);

&#x20; font-size: 1.125rem;

&#x20; color: var(--color-text);

&#x20; transition: scale var(--duration-fast) var(--ease-bounce), box-shadow var(--duration-fast);

}

.fab-item\_\_btn:hover { scale: 1.1; box-shadow: var(--shadow-xl); }



/\* ─── Floating toolbar (text selection) ─── \*/

.float-toolbar {

&#x20; position: fixed;

&#x20; background: var(--color-neutral-900);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-1) var(--space-2);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 2px;

&#x20; box-shadow: var(--shadow-xl);

&#x20; z-index: var(--z-popover);

&#x20; animation: float-toolbar-in 0.15s var(--ease-out);

&#x20; top: var(--toolbar-y, 100px);

&#x20; left: var(--toolbar-x, 50%);

&#x20; translate: -50% calc(-100% - 8px);

}



@keyframes float-toolbar-in {

&#x20; from { opacity: 0; scale: 0.9; }

}



/\* Arrow \*/

.float-toolbar::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 100%;

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; border: 5px solid transparent;

&#x20; border-top-color: var(--color-neutral-900);

}



.float-toolbar-btn {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border: none;

&#x20; background: none;

&#x20; color: rgba(255 255 255 / 0.8);

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: bold;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.float-toolbar-btn:hover { background: rgba(255 255 255 / 0.15); color: white; }

.float-toolbar-btn.active { background: rgba(255 255 255 / 0.2); color: white; }



.float-toolbar-divider {

&#x20; width: 1px;

&#x20; height: 1.25rem;

&#x20; background: rgba(255 255 255 / 0.15);

&#x20; margin-inline: 2px;

}

```



\---



\## 191. SPOTLIGHT SEARCH



```css

/\* ─── App-wide spotlight search (CMD+K) ─── \*/

.spotlight-overlay {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; background: rgb(0 0 0 / 0.5);

&#x20; backdrop-filter: blur(6px);

&#x20; z-index: var(--z-modal);

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; justify-content: center;

&#x20; padding-block-start: 15dvh;

&#x20; padding-inline: var(--space-4);

}



.spotlight {

&#x20; width: 100%;

&#x20; max-width: 580px;

&#x20; background: var(--color-surface);

&#x20; border-radius: var(--radius-2xl);

&#x20; box-shadow: var(--shadow-2xl);

&#x20; overflow: hidden;

&#x20; animation: spotlight-in 0.2s var(--ease-bounce);

}



@keyframes spotlight-in {

&#x20; from { opacity: 0; scale: 0.95; translate: 0 -12px; }

}



.spotlight-input-row {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-4) var(--space-5);

&#x20; border-bottom: 1px solid var(--color-border);

}



.spotlight-icon { color: var(--color-text-muted); font-size: 1.125rem; flex-shrink: 0; }



.spotlight-input {

&#x20; flex: 1;

&#x20; border: none;

&#x20; background: none;

&#x20; font: inherit;

&#x20; font-size: var(--font-size-lg);

&#x20; color: var(--color-text);

&#x20; outline: none;

}

.spotlight-input::placeholder { color: var(--color-text-subtle); }



.spotlight-kbd {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; padding: 0.15em 0.4em;

&#x20; background: var(--color-bg-muted);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-sm);

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; box-shadow: 0 1px 0 var(--color-border);

&#x20; flex-shrink: 0;

}



/\* Results \*/

.spotlight-results {

&#x20; max-height: 400px;

&#x20; overflow-y: auto;

&#x20; scrollbar-width: thin;

}



.spotlight-section-title {

&#x20; padding: var(--space-2) var(--space-5);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; position: sticky;

&#x20; top: 0;

&#x20; background: var(--color-surface);

}



.spotlight-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: 0.625rem var(--space-5);

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast);

&#x20; border-radius: 0;

}



.spotlight-item:hover,

.spotlight-item\[aria-selected="true"] {

&#x20; background: var(--color-bg-subtle);

}



.spotlight-item\[aria-selected="true"] .spotlight-item\_\_right { opacity: 1; }



.spotlight-item\_\_icon {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: var(--radius-md);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; flex-shrink: 0;

&#x20; font-size: 1rem;

&#x20; background: var(--color-bg-muted);

}



.spotlight-item\_\_label {

&#x20; flex: 1;

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



.spotlight-item\_\_label mark {

&#x20; background: var(--color-warning-200);

&#x20; color: inherit;

&#x20; font-weight: var(--font-weight-bold);

&#x20; border-radius: 2px;

}



.spotlight-item\_\_sublabel {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



.spotlight-item\_\_right {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast);

&#x20; flex-shrink: 0;

}



/\* Footer hint \*/

.spotlight-footer {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-4);

&#x20; padding: var(--space-2) var(--space-5);

&#x20; border-top: 1px solid var(--color-border);

&#x20; background: var(--color-bg-subtle);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-subtle);

}



/\* Empty state \*/

.spotlight-empty {

&#x20; padding: var(--space-12);

&#x20; text-align: center;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

}



.spotlight-empty\_\_icon { font-size: 2.5rem; margin-block-end: var(--space-3); }

```



\---



\## 192. APP LAUNCHER / GRID MENU



```css

/\* ─── App grid launcher ─── \*/

.app-launcher {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; background: rgb(0 0 0 / 0.7);

&#x20; backdrop-filter: blur(20px);

&#x20; z-index: var(--z-modal);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; padding: var(--space-8);

&#x20; gap: var(--space-8);

&#x20; animation: launcher-in 0.25s var(--ease-out);

}



@keyframes launcher-in { from { opacity: 0; } }



/\* Search in launcher \*/

.launcher-search {

&#x20; width: 100%;

&#x20; max-width: 360px;

&#x20; padding: 0.875rem 1.25rem;

&#x20; background: rgba(255 255 255 / 0.15);

&#x20; border: 1px solid rgba(255 255 255 / 0.2);

&#x20; border-radius: var(--radius-2xl);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-base);

&#x20; color: white;

&#x20; outline: none;

&#x20; backdrop-filter: blur(4px);

&#x20; transition: background var(--duration-fast), border-color var(--duration-fast);

}

.launcher-search::placeholder { color: rgba(255 255 255 / 0.5); }

.launcher-search:focus {

&#x20; background: rgba(255 255 255 / 0.2);

&#x20; border-color: rgba(255 255 255 / 0.4);

}



/\* App grid \*/

.app-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(var(--cols, 6), 1fr);

&#x20; gap: var(--space-6) var(--space-4);

&#x20; max-width: 700px;

&#x20; width: 100%;

}



@media (max-width: 600px) { .app-grid { --cols: 4; } }

@media (max-width: 400px) { .app-grid { --cols: 3; } }



/\* App icon \*/

.app-icon-btn {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; cursor: pointer;

&#x20; background: none;

&#x20; border: none;

&#x20; padding: var(--space-2);

&#x20; border-radius: var(--radius-xl);

&#x20; color: white;

&#x20; transition:

&#x20;   background  var(--duration-fast),

&#x20;   scale       var(--duration-fast) var(--ease-bounce);

&#x20; animation: app-icon-in 0.3s var(--ease-bounce) backwards;

&#x20; animation-delay: calc(var(--i, 0) \* 30ms);

}



@keyframes app-icon-in {

&#x20; from { opacity: 0; scale: 0.7; }

}



.app-icon-btn:hover {

&#x20; background: rgba(255 255 255 / 0.12);

&#x20; scale: 1.05;

}



.app-icon-btn:active { scale: 0.95; }



.app-icon {

&#x20; width: 3.5rem;

&#x20; height: 3.5rem;

&#x20; border-radius: var(--radius-xl);

&#x20; background: var(--icon-bg, var(--color-accent));

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 1.75rem;

&#x20; box-shadow: 0 4px 12px rgba(0 0 0 / 0.3);

&#x20; position: relative;

&#x20; overflow: hidden;

}



/\* Notification badge on app icon \*/

.app-icon\_\_badge {

&#x20; position: absolute;

&#x20; top: -2px;

&#x20; right: -2px;

&#x20; min-width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; background: var(--color-danger-500);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: 0.625rem;

&#x20; font-weight: bold;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; border: 2px solid transparent;

&#x20; padding-inline: 2px;

}



.app-icon-label {

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.9);

&#x20; text-shadow: 0 1px 3px rgba(0 0 0 / 0.5);

&#x20; max-width: 5rem;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



/\* Dock bar \*/

.app-dock {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; background: rgba(255 255 255 / 0.1);

&#x20; backdrop-filter: blur(20px);

&#x20; border: 1px solid rgba(255 255 255 / 0.15);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; box-shadow: 0 8px 32px rgba(0 0 0 / 0.3);

}



.dock-divider {

&#x20; width: 1px;

&#x20; height: 2.5rem;

&#x20; background: rgba(255 255 255 / 0.15);

&#x20; margin-inline: var(--space-2);

}



/\* Dock icon magnification on hover (macOS style) \*/

.app-dock:hover .app-icon-btn {

&#x20; transition: scale 0.15s var(--ease-out);

}



.app-icon-btn {

&#x20; --scale: 1;

&#x20; scale: var(--scale);

}



/\* JS sets --scale based on distance from cursor \*/

```



\---



```

╔══════════════════════════════════════════════════════════════════════╗

║                     PART 13 — COMPLETE                               ║

║  Chapters 182–192 | 11 new chapters | Output: css-guide-part13.md   ║

╚══════════════════════════════════════════════════════════════════════╝

```

