\# CSS GUIDE — PART 14

\## Chapters 193–207



\---



\## 193. CONTEXT-AWARE THEMING



```css

/\* ─── Theme propagation via CSS custom properties ─── \*/



/\* Base theme contract — every theme MUST define these \*/

\[data-theme] {

&#x20; /\* Surfaces \*/

&#x20; --bg:        unset;

&#x20; --surface:   unset;

&#x20; --elevated:  unset;

&#x20; /\* Text \*/

&#x20; --fg:        unset;

&#x20; --fg-muted:  unset;

&#x20; /\* Brand \*/

&#x20; --accent:    unset;

&#x20; --accent-fg: unset;

&#x20; /\* Feedback \*/

&#x20; --ok:        unset;

&#x20; --warn:      unset;

&#x20; --err:       unset;

}



/\* Light theme \*/

\[data-theme="light"] {

&#x20; color-scheme: light;

&#x20; --bg:        oklch(1 0 0);

&#x20; --surface:   oklch(1 0 0);

&#x20; --elevated:  oklch(0.98 0 0);

&#x20; --fg:        oklch(0.15 0 0);

&#x20; --fg-muted:  oklch(0.45 0 0);

&#x20; --accent:    oklch(0.60 0.20 250);

&#x20; --accent-fg: oklch(1 0 0);

&#x20; --ok:        oklch(0.55 0.18 145);

&#x20; --warn:      oklch(0.65 0.20 65);

&#x20; --err:       oklch(0.55 0.22 25);

}



/\* Dark theme \*/

\[data-theme="dark"] {

&#x20; color-scheme: dark;

&#x20; --bg:        oklch(0.10 0 0);

&#x20; --surface:   oklch(0.14 0 0);

&#x20; --elevated:  oklch(0.18 0 0);

&#x20; --fg:        oklch(0.95 0 0);

&#x20; --fg-muted:  oklch(0.60 0 0);

&#x20; --accent:    oklch(0.70 0.20 250);

&#x20; --accent-fg: oklch(0.10 0 0);

&#x20; --ok:        oklch(0.70 0.18 145);

&#x20; --warn:      oklch(0.80 0.20 65);

&#x20; --err:       oklch(0.70 0.22 25);

}



/\* Solarized theme \*/

\[data-theme="solarized"] {

&#x20; color-scheme: light;

&#x20; --bg:        oklch(0.97 0.02 90);

&#x20; --surface:   oklch(0.95 0.02 90);

&#x20; --elevated:  oklch(0.93 0.02 90);

&#x20; --fg:        oklch(0.40 0.05 220);

&#x20; --fg-muted:  oklch(0.55 0.05 220);

&#x20; --accent:    oklch(0.55 0.18 220);

&#x20; --accent-fg: oklch(1 0 0);

&#x20; --ok:        oklch(0.55 0.15 145);

&#x20; --warn:      oklch(0.65 0.18 65);

&#x20; --err:       oklch(0.55 0.20 25);

}



/\* Auto theme (follows OS) \*/

@media (prefers-color-scheme: dark) {

&#x20; \[data-theme="auto"] {

&#x20;   color-scheme: dark;

&#x20;   --bg:        oklch(0.10 0 0);

&#x20;   --surface:   oklch(0.14 0 0);

&#x20;   --elevated:  oklch(0.18 0 0);

&#x20;   --fg:        oklch(0.95 0 0);

&#x20;   --fg-muted:  oklch(0.60 0 0);

&#x20;   --accent:    oklch(0.70 0.20 250);

&#x20;   --accent-fg: oklch(0.10 0 0);

&#x20;   --ok:        oklch(0.70 0.18 145);

&#x20;   --warn:      oklch(0.80 0.20 65);

&#x20;   --err:       oklch(0.70 0.22 25);

&#x20; }

}



/\* Component using only theme tokens \*/

.themed-card {

&#x20; background: var(--surface);

&#x20; color: var(--fg);

&#x20; border: 1px solid color-mix(in oklch, var(--fg) 12%, transparent);

}



.themed-card p { color: var(--fg-muted); }

.themed-btn-primary { background: var(--accent); color: var(--accent-fg); }

.themed-badge-ok   { background: color-mix(in oklch, var(--ok) 15%, transparent); color: var(--ok); }

.themed-badge-err  { background: color-mix(in oklch, var(--err) 15%, transparent); color: var(--err); }



/\* ─── Local context override ─── \*/

/\* A dark card inside a light page \*/

.invert-theme {

&#x20; --bg:       oklch(0.10 0 0);

&#x20; --surface:  oklch(0.14 0 0);

&#x20; --fg:       oklch(0.95 0 0);

&#x20; --fg-muted: oklch(0.60 0 0);

&#x20; background: var(--bg);

&#x20; color: var(--fg);

&#x20; color-scheme: dark;

}



/\* Brand section override \*/

.brand-section {

&#x20; --bg:        var(--accent);

&#x20; --surface:   color-mix(in oklch, var(--accent) 85%, black);

&#x20; --fg:        var(--accent-fg);

&#x20; --fg-muted:  color-mix(in oklch, var(--accent-fg) 70%, transparent);

&#x20; background: var(--bg);

&#x20; color: var(--fg);

}

```



\---



\## 194. ANIMATED NUMBER COUNTERS



```css

/\* ─── CSS counter animation (scroll-driven) ─── \*/

@property --n {

&#x20; syntax: '<integer>';

&#x20; initial-value: 0;

&#x20; inherits: false;

}



.count-up {

&#x20; counter-reset: n var(--n);

&#x20; animation: count-to linear both;

&#x20; animation-timeline: view();

&#x20; animation-range: entry 0% entry 60%;

}



.count-up::after {

&#x20; content: counter(n);

}



@keyframes count-to {

&#x20; from { --n: 0; }

&#x20; to   { --n: var(--count-target, 100); }

}



/\* With suffix (k, m, %, +) \*/

.count-up\[data-suffix]::after {

&#x20; content: counter(n) attr(data-suffix);

}



/\* Animated counter via transition \*/

@property --counter-value {

&#x20; syntax: '<number>';

&#x20; initial-value: 0;

&#x20; inherits: false;

}



.counter-animated {

&#x20; --counter-value: 0;

&#x20; transition: --counter-value 1.5s var(--ease-out);

}



/\* JS: el.style.setProperty('--counter-value', target) \*/

/\* then read value in JS to display: Math.round(el.style.getPropertyValue('--counter-value')) \*/



/\* ─── Odometer / slot machine counter ─── \*/

.odometer {

&#x20; display: inline-flex;

&#x20; overflow: hidden;

&#x20; font-family: var(--font-mono);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-variant-numeric: tabular-nums;

}



.odometer-digit {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; overflow: hidden;

&#x20; height: 1em;

&#x20; position: relative;

}



.odometer-reel {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; translate: 0 calc(var(--current, 0) \* -1em);

&#x20; transition: translate 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);

}



.odometer-reel span {

&#x20; height: 1em;

&#x20; display: block;

&#x20; line-height: 1;

}



/\* ─── Flip counter ─── \*/

.flip-counter {

&#x20; display: inline-flex;

&#x20; gap: 4px;

}



.flip-digit {

&#x20; position: relative;

&#x20; width: 1.5em;

&#x20; height: 2em;

&#x20; perspective: 200px;

}



.flip-digit\_\_front,

.flip-digit\_\_back {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: var(--color-neutral-800);

&#x20; color: white;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; border-radius: var(--radius-sm);

&#x20; font-weight: bold;

&#x20; backface-visibility: hidden;

&#x20; font-variant-numeric: tabular-nums;

}



.flip-digit\_\_back {

&#x20; transform: rotateX(180deg);

}



.flip-digit.flipping .flip-digit\_\_front {

&#x20; animation: flip-front 0.3s ease-in forwards;

}

.flip-digit.flipping .flip-digit\_\_back {

&#x20; animation: flip-back 0.3s ease-out forwards 0.3s;

}



@keyframes flip-front {

&#x20; to { transform: rotateX(-90deg); }

}

@keyframes flip-back {

&#x20; from { transform: rotateX(90deg); }

&#x20; to   { transform: rotateX(0deg); }

}



/\* Top/bottom fold effect \*/

.flip-digit::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-inline: 0;

&#x20; inset-block-start: 50%;

&#x20; height: 1px;

&#x20; background: rgba(0 0 0 / 0.3);

&#x20; z-index: 2;

}

```



\---



\## 195. MAP / GEO UI



```css

/\* ─── Map container shell ─── \*/

.map-shell {

&#x20; position: relative;

&#x20; width: 100%;

&#x20; aspect-ratio: 16 / 9;

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; background: #e8e0d8;

}



.map-shell iframe,

.map-shell .map-tile {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; border: none;

}



/\* Map overlay controls \*/

.map-controls {

&#x20; position: absolute;

&#x20; top: var(--space-3);

&#x20; right: var(--space-3);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-1);

&#x20; z-index: 10;

}



.map-control-btn {

&#x20; width: 2.25rem;

&#x20; height: 2.25rem;

&#x20; background: white;

&#x20; border: none;

&#x20; border-radius: var(--radius-md);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; box-shadow: var(--shadow-md);

&#x20; color: var(--color-text);

&#x20; font-size: 1.25rem;

&#x20; font-weight: bold;

&#x20; transition: background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

}

.map-control-btn:hover { background: var(--color-bg-subtle); scale: 1.05; }



/\* Zoom control group \*/

.map-zoom {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; border-radius: var(--radius-md);

&#x20; overflow: hidden;

&#x20; box-shadow: var(--shadow-md);

}

.map-zoom .map-control-btn { border-radius: 0; box-shadow: none; }

.map-zoom .map-control-btn:not(:last-child) { border-bottom: 1px solid var(--color-border); }



/\* Custom marker \*/

.map-marker {

&#x20; position: absolute;

&#x20; translate: -50% -100%;

&#x20; left: var(--mx, 50%);

&#x20; top:  var(--my, 50%);

&#x20; z-index: 5;

&#x20; cursor: pointer;

}



.map-marker\_\_pin {

&#x20; width: 32px;

&#x20; height: 40px;

&#x20; background: var(--marker-color, var(--color-accent));

&#x20; border-radius: 50% 50% 50% 0;

&#x20; rotate: -45deg;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; box-shadow: var(--shadow-lg);

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}

.map-marker:hover .map-marker\_\_pin { scale: 1.2; }



.map-marker\_\_icon {

&#x20; rotate: 45deg;

&#x20; font-size: 1rem;

&#x20; color: white;

}



/\* Pulse ring on marker \*/

.map-marker\_\_pulse {

&#x20; position: absolute;

&#x20; bottom: 0;

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; width: 32px;

&#x20; height: 32px;

&#x20; border-radius: 50%;

&#x20; background: var(--marker-color, var(--color-accent));

&#x20; opacity: 0;

&#x20; animation: marker-pulse 2s ease-in-out infinite;

}



@keyframes marker-pulse {

&#x20; 0%   { scale: 0.5; opacity: 0.5; }

&#x20; 100% { scale: 2; opacity: 0; }

}



/\* Marker cluster \*/

.map-cluster {

&#x20; width: 40px;

&#x20; height: 40px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-sm);

&#x20; box-shadow: var(--shadow-md);

&#x20; border: 3px solid white;

&#x20; cursor: pointer;

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}

.map-cluster:hover { scale: 1.1; }



/\* Marker tooltip \*/

.map-tooltip {

&#x20; position: absolute;

&#x20; bottom: calc(100% + 8px);

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; background: white;

&#x20; border-radius: var(--radius-lg);

&#x20; padding: var(--space-3) var(--space-4);

&#x20; box-shadow: var(--shadow-xl);

&#x20; min-width: 160px;

&#x20; pointer-events: none;

&#x20; opacity: 0;

&#x20; scale: 0.9;

&#x20; transition: opacity var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

&#x20; z-index: 20;

}

.map-marker:hover .map-tooltip {

&#x20; opacity: 1;

&#x20; scale: 1;

&#x20; pointer-events: auto;

}



.map-tooltip::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; top: 100%;

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; border: 6px solid transparent;

&#x20; border-top-color: white;

&#x20; filter: drop-shadow(0 2px 2px rgba(0 0 0 / 0.1));

}



/\* Search box overlay \*/

.map-search {

&#x20; position: absolute;

&#x20; top: var(--space-3);

&#x20; left: var(--space-3);

&#x20; right: 4rem;

&#x20; z-index: 10;

}



.map-search\_\_input {

&#x20; width: 100%;

&#x20; padding: 0.625rem 1rem;

&#x20; border: none;

&#x20; border-radius: var(--radius-full);

&#x20; background: white;

&#x20; box-shadow: var(--shadow-md);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; outline: none;

}



/\* Info panel sidebar \*/

.map-sidebar {

&#x20; position: absolute;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; left: 0;

&#x20; width: 320px;

&#x20; background: white;

&#x20; z-index: 10;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; box-shadow: var(--shadow-xl);

&#x20; translate: calc(-100% - 1px);

&#x20; transition: translate var(--duration-slow) var(--ease-out);

}



.map-sidebar.open { translate: 0; }

```



\---



\## 196. TIMELINE / ACTIVITY FEED



```css

/\* ─── Activity feed ─── \*/

.activity-feed {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: 0;

&#x20; position: relative;

}



/\* Connecting line \*/

.activity-feed::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-inline-start: 1.25rem;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; width: 2px;

&#x20; background: linear-gradient(

&#x20;   to bottom,

&#x20;   transparent,

&#x20;   var(--color-border) 5%,

&#x20;   var(--color-border) 95%,

&#x20;   transparent

&#x20; );

}



/\* Feed item \*/

.feed-item {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; padding-block: var(--space-4);

&#x20; padding-inline-start: var(--space-2);

&#x20; position: relative;

&#x20; animation: feed-item-in 0.3s var(--ease-out) backwards;

&#x20; animation-delay: calc(var(--i, 0) \* 60ms);

}



@keyframes feed-item-in {

&#x20; from { opacity: 0; translate: -12px 0; }

}



/\* Icon bubble \*/

.feed-icon {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: 50%;

&#x20; background: var(--feed-icon-bg, var(--color-bg-muted));

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 1rem;

&#x20; flex-shrink: 0;

&#x20; border: 2px solid var(--color-surface);

&#x20; box-shadow: 0 0 0 3px var(--color-surface);

&#x20; position: relative;

&#x20; z-index: 1;

}



/\* Action type colors \*/

.feed-item--created  { --feed-icon-bg: var(--color-success-100); }

.feed-item--updated  { --feed-icon-bg: var(--color-brand-100); }

.feed-item--deleted  { --feed-icon-bg: var(--color-danger-100); }

.feed-item--comment  { --feed-icon-bg: var(--color-warning-100); }

.feed-item--assigned { --feed-icon-bg: oklch(0.93 0.05 300); }



/\* Content \*/

.feed-content { flex: 1; min-width: 0; }



.feed-header {

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; gap: var(--space-2);

&#x20; margin-block-end: var(--space-1);

&#x20; flex-wrap: wrap;

}



.feed-actor {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text);

}



.feed-action {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

}



.feed-subject {

&#x20; font-weight: var(--font-weight-medium);

&#x20; color: var(--color-text);

&#x20; font-size: var(--font-size-sm);

}



.feed-time {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-subtle);

&#x20; margin-inline-start: auto;

&#x20; white-space: nowrap;

&#x20; padding-block-start: 2px;

}



/\* Feed body (comment, diff, etc.) \*/

.feed-body {

&#x20; background: var(--color-bg-subtle);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; padding: var(--space-3);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

&#x20; margin-block-start: var(--space-2);

}



/\* Inline diff in feed \*/

.feed-diff {

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-xs);

&#x20; line-height: 1.6;

}



.feed-diff .del {

&#x20; background: var(--color-danger-100);

&#x20; color: var(--color-danger-700);

&#x20; text-decoration: line-through;

&#x20; padding: 0 2px;

&#x20; border-radius: 2px;

}



.feed-diff .ins {

&#x20; background: var(--color-success-100);

&#x20; color: var(--color-success-700);

&#x20; padding: 0 2px;

&#x20; border-radius: 2px;

}



/\* Reactions \*/

.feed-reactions {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-1);

&#x20; margin-block-start: var(--space-2);

}



.feed-reaction {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: 0.25em;

&#x20; padding: 0.2em 0.5em;

&#x20; background: var(--color-bg-subtle);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   background    var(--duration-fast),

&#x20;   border-color  var(--duration-fast),

&#x20;   scale         var(--duration-fast) var(--ease-bounce);

}

.feed-reaction:hover { background: var(--color-bg-muted); }

.feed-reaction.mine  {

&#x20; background: var(--color-brand-100);

&#x20; border-color: var(--color-brand-300);

&#x20; color: var(--color-brand-700);

}

.feed-reaction:active { scale: 0.94; }



.feed-reaction\_\_count {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-variant-numeric: tabular-nums;

}



/\* Load more \*/

.feed-load-more {

&#x20; display: flex;

&#x20; justify-content: center;

&#x20; padding-block: var(--space-4);

&#x20; position: relative;

&#x20; z-index: 1;

}

```



\---



\## 197. AUDIT LOG TABLE



```css

/\* ─── Audit log ─── \*/

.audit-log {

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

}



.audit-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-4);

&#x20; padding: var(--space-4) var(--space-5);

&#x20; background: var(--color-bg-subtle);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; flex-wrap: wrap;

}



.audit-filters {

&#x20; display: flex;

&#x20; gap: var(--space-2);

&#x20; flex-wrap: wrap;

}



.audit-filter-chip {

&#x20; padding: 0.25rem 0.75rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-medium);

&#x20; cursor: pointer;

&#x20; background: var(--color-surface);

&#x20; color: var(--color-text-muted);

&#x20; transition: all var(--duration-fast);

}

.audit-filter-chip.active {

&#x20; background: var(--color-accent);

&#x20; border-color: var(--color-accent);

&#x20; color: white;

}



.audit-search { margin-inline-start: auto; }



/\* Log row \*/

.audit-row {

&#x20; display: grid;

&#x20; grid-template-columns: 160px 120px 1fr auto auto;

&#x20; gap: var(--space-4);

&#x20; align-items: center;

&#x20; padding: var(--space-3) var(--space-5);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; font-size: var(--font-size-sm);

&#x20; transition: background var(--duration-fast);

}

.audit-row:last-child { border: none; }

.audit-row:hover { background: var(--color-bg-subtle); }



.audit-ts {

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; font-variant-numeric: tabular-nums;

&#x20; white-space: nowrap;

}



.audit-actor {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; min-width: 0;

}



.audit-actor img {

&#x20; width: 1.25rem;

&#x20; height: 1.25rem;

&#x20; border-radius: 50%;

&#x20; flex-shrink: 0;

&#x20; object-fit: cover;

}



.audit-actor-name {

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

&#x20; font-weight: var(--font-weight-medium);

}



/\* Action badge \*/

.audit-action {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; padding: 0.15em 0.5em;

&#x20; border-radius: var(--radius-sm);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-family: var(--font-mono);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.03em;

}



.audit-action--create { background: var(--color-success-100); color: var(--color-success-800); }

.audit-action--update { background: var(--color-brand-100);   color: var(--color-brand-800); }

.audit-action--delete { background: var(--color-danger-100);  color: var(--color-danger-800); }

.audit-action--login  { background: var(--color-bg-muted);    color: var(--color-text-muted); }

.audit-action--export { background: var(--color-warning-100); color: var(--color-warning-800); }



.audit-resource {

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

&#x20; color: var(--color-text);

}



.audit-resource strong { font-weight: var(--font-weight-medium); }



.audit-ip {

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; white-space: nowrap;

}



/\* Expandable details \*/

.audit-row-detail {

&#x20; grid-column: 1 / -1;

&#x20; background: var(--color-bg-subtle);

&#x20; border-top: 1px solid var(--color-border);

&#x20; padding: var(--space-4) var(--space-5);

&#x20; font-family: var(--font-mono);

&#x20; font-size: var(--font-size-xs);

&#x20; line-height: 1.7;

&#x20; color: var(--color-text-muted);

&#x20; max-height: 0;

&#x20; overflow: hidden;

&#x20; transition: max-height 0.3s var(--ease-out), padding 0.3s;

&#x20; padding-block: 0;

}



.audit-row.expanded .audit-row-detail {

&#x20; max-height: 400px;

&#x20; padding-block: var(--space-4);

}



/\* Severity indicator \*/

.audit-severity {

&#x20; width: 6px;

&#x20; height: 6px;

&#x20; border-radius: 50%;

&#x20; flex-shrink: 0;

}

.audit-severity--info    { background: var(--color-brand-400); }

.audit-severity--warning { background: var(--color-warning-500); }

.audit-severity--critical{ background: var(--color-danger-500); animation: pulse 1s ease-in-out infinite; }

```



\---



\## 198. IMAGE ANNOTATION UI



```css

/\* ─── Image annotator ─── \*/

.annotator {

&#x20; position: relative;

&#x20; display: inline-block;

&#x20; cursor: crosshair;

&#x20; user-select: none;

}



.annotator img {

&#x20; display: block;

&#x20; max-width: 100%;

}



/\* Annotation layer \*/

.annotation-layer {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; pointer-events: none;

}



/\* Annotation region \*/

.annotation {

&#x20; position: absolute;

&#x20; border: 2px solid var(--annotation-color, var(--color-accent));

&#x20; border-radius: var(--radius-sm);

&#x20; background: color-mix(in srgb, var(--annotation-color, var(--color-accent)) 10%, transparent);

&#x20; cursor: pointer;

&#x20; pointer-events: auto;

&#x20; transition:

&#x20;   background  var(--duration-fast),

&#x20;   border-color var(--duration-fast),

&#x20;   scale       var(--duration-fast) var(--ease-bounce);

&#x20; left:   var(--ax, 0);

&#x20; top:    var(--ay, 0);

&#x20; width:  var(--aw, 100px);

&#x20; height: var(--ah, 100px);

}



.annotation:hover {

&#x20; background: color-mix(in srgb, var(--annotation-color, var(--color-accent)) 20%, transparent);

&#x20; z-index: 2;

}



.annotation.selected {

&#x20; border-color: var(--annotation-color, var(--color-accent));

&#x20; background: color-mix(in srgb, var(--annotation-color, var(--color-accent)) 15%, transparent);

&#x20; z-index: 3;

&#x20; outline: 3px solid color-mix(in srgb, var(--annotation-color, var(--color-accent)) 30%, transparent);

}



/\* Annotation number badge \*/

.annotation::before {

&#x20; content: var(--num, '1');

&#x20; position: absolute;

&#x20; top: -10px;

&#x20; left: -10px;

&#x20; width: 20px;

&#x20; height: 20px;

&#x20; background: var(--annotation-color, var(--color-accent));

&#x20; color: white;

&#x20; border-radius: 50%;

&#x20; font-size: 0.625rem;

&#x20; font-weight: bold;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; border: 2px solid white;

&#x20; box-shadow: var(--shadow-sm);

&#x20; font-family: var(--font-sans);

&#x20; pointer-events: none;

}



/\* Resize handles \*/

.annotation-handle {

&#x20; position: absolute;

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; background: white;

&#x20; border: 2px solid var(--annotation-color, var(--color-accent));

&#x20; border-radius: 2px;

}

.annotation-handle\[data-pos="tl"] { top: -4px; left: -4px; cursor: nw-resize; }

.annotation-handle\[data-pos="tr"] { top: -4px; right: -4px; cursor: ne-resize; }

.annotation-handle\[data-pos="bl"] { bottom: -4px; left: -4px; cursor: sw-resize; }

.annotation-handle\[data-pos="br"] { bottom: -4px; right: -4px; cursor: se-resize; }



/\* Annotation popup \*/

.annotation-popup {

&#x20; position: absolute;

&#x20; top: calc(100% + 8px);

&#x20; left: 0;

&#x20; min-width: 200px;

&#x20; background: white;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; box-shadow: var(--shadow-xl);

&#x20; padding: var(--space-3);

&#x20; z-index: 20;

&#x20; animation: annotation-pop 0.2s var(--ease-bounce);

&#x20; pointer-events: auto;

}



@keyframes annotation-pop { from { opacity: 0; scale: 0.9; translate: 0 6px; } }



.annotation-popup textarea {

&#x20; width: 100%;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; padding: var(--space-2);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-xs);

&#x20; resize: vertical;

&#x20; min-height: 60px;

&#x20; outline: none;

&#x20; transition: border-color var(--duration-fast);

}

.annotation-popup textarea:focus { border-color: var(--color-accent); }



/\* Annotations panel \*/

.annotations-panel {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

&#x20; max-height: 400px;

&#x20; overflow-y: auto;

}



.annotation-item {

&#x20; display: flex;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-3);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; cursor: pointer;

&#x20; transition: background var(--duration-fast), border-color var(--duration-fast);

}

.annotation-item:hover { background: var(--color-bg-subtle); }

.annotation-item.active { border-color: var(--color-accent); background: color-mix(in srgb, var(--color-accent) 5%, transparent); }



.annotation-item\_\_num {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; background: var(--annotation-color, var(--color-accent));

&#x20; color: white;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: bold;

&#x20; flex-shrink: 0;

}



.annotation-item\_\_text {

&#x20; flex: 1;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.5;

&#x20; overflow: hidden;

&#x20; display: -webkit-box;

&#x20; -webkit-line-clamp: 2;

&#x20; -webkit-box-orient: vertical;

}

```



\---



\## 199. DYNAMIC ISLAND



```css

/\* ─── Dynamic Island (iOS 14 Pro+) style notification ─── \*/

.dynamic-island {

&#x20; position: fixed;

&#x20; top: var(--space-3);

&#x20; left: 50%;

&#x20; translate: -50% 0;

&#x20; z-index: var(--z-top);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

}



/\* The pill \*/

.island-pill {

&#x20; background: #000;

&#x20; border-radius: 9999px;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-3);

&#x20; overflow: hidden;

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   width    0.4s cubic-bezier(0.34, 1.56, 0.64, 1),

&#x20;   height   0.4s cubic-bezier(0.34, 1.56, 0.64, 1),

&#x20;   border-radius 0.4s;



&#x20; /\* Default — compact \*/

&#x20; width: 120px;

&#x20; height: 34px;

&#x20; padding-inline: var(--space-3);

}



/\* States \*/

.island-pill\[data-state="compact"] {

&#x20; width: 120px;

&#x20; height: 34px;

}



.island-pill\[data-state="expanded"] {

&#x20; width: 340px;

&#x20; height: 80px;

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-3) var(--space-4);

}



.island-pill\[data-state="minimal"] {

&#x20; width: 34px;

&#x20; height: 34px;

}



/\* Content layers \*/

.island-content {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; width: 100%;

&#x20; opacity: 0;

&#x20; transition: opacity 0.2s;

}



.island-pill\[data-state="expanded"] .island-content { opacity: 1; }



/\* Compact icons \*/

.island-icons {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; width: 100%;

}



.island-pill\[data-state="expanded"] .island-icons { display: none; }

.island-pill\[data-state="minimal"] .island-icons { display: none; }



.island-icon-left,

.island-icon-right {

&#x20; width: 20px;

&#x20; height: 20px;

&#x20; border-radius: 50%;

&#x20; overflow: hidden;

&#x20; flex-shrink: 0;

}



/\* Progress bar in island \*/

.island-progress {

&#x20; flex: 1;

&#x20; height: 3px;

&#x20; background: rgba(255 255 255 / 0.2);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

}



.island-progress\_\_fill {

&#x20; height: 100%;

&#x20; background: var(--color-success-400);

&#x20; width: var(--progress, 0%);

&#x20; transition: width 0.5s linear;

&#x20; border-radius: inherit;

}



/\* Album art in island \*/

.island-art {

&#x20; width: 40px;

&#x20; height: 40px;

&#x20; border-radius: var(--radius-md);

&#x20; object-fit: cover;

&#x20; flex-shrink: 0;

}



/\* Text in island \*/

.island-text { flex: 1; min-width: 0; }

.island-title {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; color: white;

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}

.island-subtitle {

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.6);

}



/\* Wave animation (music) \*/

.island-wave {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 2px;

&#x20; height: 20px;

}

.island-wave span {

&#x20; width: 2px;

&#x20; background: var(--color-success-400);

&#x20; border-radius: 1px;

&#x20; animation: island-wave-bar 0.8s ease-in-out infinite alternate;

}

.island-wave span:nth-child(1) { height: 40%; animation-delay: 0s; }

.island-wave span:nth-child(2) { height: 70%; animation-delay: 0.1s; }

.island-wave span:nth-child(3) { height: 100%; animation-delay: 0.2s; }

.island-wave span:nth-child(4) { height: 60%; animation-delay: 0.15s; }



@keyframes island-wave-bar {

&#x20; from { height: 20%; }

&#x20; to   { height: 100%; }

}

```



\---



\## 200. SKELETON PATTERNS LIBRARY



```css

/\* ─── Complete skeleton loading system ─── \*/

@keyframes sk-shimmer {

&#x20; from { background-position: -200% center; }

&#x20; to   { background-position: 200% center; }

}



/\* Base skeleton mixin \*/

.sk {

&#x20; background: linear-gradient(

&#x20;   90deg,

&#x20;   var(--sk-base, var(--color-bg-muted)) 25%,

&#x20;   var(--sk-shine, var(--color-bg-subtle)) 50%,

&#x20;   var(--sk-base, var(--color-bg-muted)) 75%

&#x20; );

&#x20; background-size: 200% 100%;

&#x20; animation: sk-shimmer 1.5s ease-in-out infinite;

&#x20; border-radius: var(--radius-md);

}



/\* Prefers reduced motion: no animation \*/

@media (prefers-reduced-motion: reduce) {

&#x20; .sk { animation: none; }

}



/\* Dark skeleton \*/

\[data-theme="dark"] .sk {

&#x20; --sk-base:  oklch(0.20 0 0);

&#x20; --sk-shine: oklch(0.25 0 0);

}



/\* ── Shape utilities ── \*/

.sk-circle { border-radius: 50%; aspect-ratio: 1; }

.sk-text   { height: 1em; border-radius: var(--radius-full); }

.sk-block  { border-radius: var(--radius-md); }

.sk-round  { border-radius: var(--radius-2xl); }



/\* ── Preset skeleton components ── \*/



/\* Avatar \*/

.sk-avatar {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: 50%;

}



/\* Text lines \*/

.sk-title   { height: 1.25em; width: 60%; border-radius: var(--radius-full); }

.sk-line    { height: 0.875em; width: 100%; border-radius: var(--radius-full); }

.sk-line-sm { height: 0.875em; width: 70%; border-radius: var(--radius-full); }

.sk-line-xs { height: 0.875em; width: 40%; border-radius: var(--radius-full); }



/\* ── Preset skeleton layouts ── \*/



/\* Card skeleton \*/

.sk-card {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; padding: var(--space-4);

}



.sk-card\_\_image { width: 100%; aspect-ratio: 16/9; border-radius: var(--radius-lg); }

.sk-card\_\_body  { padding-block-start: var(--space-4); display: flex; flex-direction: column; gap: var(--space-3); }



/\* Profile skeleton \*/

.sk-profile {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; align-items: flex-start;

&#x20; padding: var(--space-4);

}

.sk-profile\_\_avatar { width: 3rem; height: 3rem; border-radius: 50%; flex-shrink: 0; }

.sk-profile\_\_info   { flex: 1; display: flex; flex-direction: column; gap: var(--space-2); }



/\* Table skeleton \*/

.sk-table-row {

&#x20; display: grid;

&#x20; grid-template-columns: 2rem 1fr 1fr 1fr auto;

&#x20; gap: var(--space-4);

&#x20; align-items: center;

&#x20; padding-block: var(--space-3);

&#x20; border-bottom: 1px solid var(--color-border);

}

.sk-table-row > .sk { height: 0.75em; border-radius: var(--radius-full); }



/\* List item skeleton \*/

.sk-list-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding-block: var(--space-3);

&#x20; border-bottom: 1px solid var(--color-border);

}



/\* Dashboard widget skeleton \*/

.sk-widget {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-5);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-4);

}

.sk-widget\_\_value { height: 2.5rem; width: 40%; border-radius: var(--radius-md); }

.sk-widget\_\_chart { height: 80px; border-radius: var(--radius-lg); }



/\* Article skeleton \*/

.sk-article { display: flex; flex-direction: column; gap: var(--space-4); }

.sk-article\_\_hero    { width: 100%; aspect-ratio: 2/1; border-radius: var(--radius-xl); }

.sk-article\_\_heading { height: 2em; width: 80%; border-radius: var(--radius-full); }



/\* Chat skeleton \*/

.sk-chat { display: flex; flex-direction: column; gap: var(--space-4); padding: var(--space-4); }

.sk-chat-msg       { display: flex; gap: var(--space-3); align-items: flex-end; max-width: 70%; }

.sk-chat-msg--right { align-self: flex-end; flex-direction: row-reverse; }

.sk-chat-msg\_\_bubble { flex: 1; height: 3rem; border-radius: var(--radius-2xl); }



/\* Staggered shimmer delay \*/

.sk:nth-child(1) { animation-delay: 0s; }

.sk:nth-child(2) { animation-delay: 0.1s; }

.sk:nth-child(3) { animation-delay: 0.2s; }

.sk:nth-child(4) { animation-delay: 0.3s; }

.sk:nth-child(5) { animation-delay: 0.4s; }

```



\---



\## 201. CSS-ONLY MODALS WITHOUT JS



```css

/\* ─── CSS-only modal via :target ─── \*/



/\* HTML pattern:

&#x20;  <a href="#modal-1">Open</a>

&#x20;  <div id="modal-1" class="css-modal"> ... </div>

\*/



.css-modal {

&#x20; position: fixed;

&#x20; inset: 0;

&#x20; z-index: var(--z-modal);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; padding: var(--space-4);

&#x20; pointer-events: none;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-normal);

}



.css-modal:target {

&#x20; opacity: 1;

&#x20; pointer-events: auto;

}



/\* Backdrop \*/

.css-modal\_\_backdrop {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: rgb(0 0 0 / 0.5);

&#x20; backdrop-filter: blur(4px);

}



/\* Close link as backdrop \*/

.css-modal\_\_close-area {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; z-index: 0;

}



/\* Dialog box \*/

.css-modal\_\_dialog {

&#x20; position: relative;

&#x20; background: var(--color-surface);

&#x20; border-radius: var(--radius-2xl);

&#x20; box-shadow: var(--shadow-2xl);

&#x20; padding: var(--space-8);

&#x20; width: 100%;

&#x20; max-width: 480px;

&#x20; z-index: 1;

&#x20; transition: scale var(--duration-normal) var(--ease-bounce), translate var(--duration-normal);

&#x20; scale: 0.9;

&#x20; translate: 0 20px;

}



.css-modal:target .css-modal\_\_dialog {

&#x20; scale: 1;

&#x20; translate: 0 0;

}



/\* Close X link \*/

.css-modal\_\_close {

&#x20; position: absolute;

&#x20; top: var(--space-4);

&#x20; right: var(--space-4);

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-bg-muted);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; text-decoration: none;

&#x20; color: var(--color-text-muted);

&#x20; font-size: 1.125rem;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

}

.css-modal\_\_close:hover { background: var(--color-bg-muted); color: var(--color-text); }



/\* ─── CSS-only tooltip via :focus-within + sibling ─── \*/

.tooltip-trigger {

&#x20; position: relative;

&#x20; display: inline-block;

}



.tooltip-trigger:focus,

.tooltip-trigger:hover {

&#x20; outline: none;

}



.tooltip-trigger:focus + .tooltip-content,

.tooltip-trigger:hover + .tooltip-content {

&#x20; opacity: 1;

&#x20; translate: -50% 0;

&#x20; pointer-events: auto;

}



.tooltip-content {

&#x20; position: absolute;

&#x20; bottom: calc(100% + 8px);

&#x20; left: 50%;

&#x20; translate: -50% 6px;

&#x20; background: var(--color-neutral-900);

&#x20; color: white;

&#x20; font-size: var(--font-size-xs);

&#x20; padding: 0.4em 0.75em;

&#x20; border-radius: var(--radius-md);

&#x20; white-space: nowrap;

&#x20; pointer-events: none;

&#x20; opacity: 0;

&#x20; transition: opacity var(--duration-fast), translate var(--duration-fast);

&#x20; z-index: var(--z-tooltip);

}



/\* ─── CSS-only accordion via :has() ─── \*/

.css-accordion {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-1);

}



.css-accordion-item {

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; overflow: hidden;

}



.css-accordion-input {

&#x20; position: absolute;

&#x20; opacity: 0;

&#x20; pointer-events: none;

&#x20; width: 0;

&#x20; height: 0;

}



.css-accordion-label {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: space-between;

&#x20; padding: var(--space-4) var(--space-5);

&#x20; cursor: pointer;

&#x20; font-weight: var(--font-weight-medium);

&#x20; user-select: none;

&#x20; transition: background var(--duration-fast);

}

.css-accordion-label:hover { background: var(--color-bg-subtle); }



.css-accordion-label::after {

&#x20; content: '+';

&#x20; font-size: 1.25rem;

&#x20; font-weight: 300;

&#x20; color: var(--color-text-muted);

&#x20; transition: rotate var(--duration-fast) var(--ease-out);

}



.css-accordion-body {

&#x20; max-height: 0;

&#x20; overflow: hidden;

&#x20; transition: max-height 0.3s var(--ease-out);

}



/\* Open state via :has() \*/

.css-accordion-item:has(.css-accordion-input:checked) .css-accordion-label::after {

&#x20; rotate: 45deg;

}



.css-accordion-item:has(.css-accordion-input:checked) .css-accordion-body {

&#x20; max-height: 500px;

}



.css-accordion-item:has(.css-accordion-input:checked) .css-accordion-label {

&#x20; background: var(--color-bg-subtle);

}



.css-accordion-body\_\_inner {

&#x20; padding: var(--space-4) var(--space-5);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; line-height: 1.6;

}

```



\---



\## 202. RECIPE CARD



```css

/\* ─── Recipe card ─── \*/

.recipe-card {

&#x20; background: var(--color-surface);

&#x20; border-radius: var(--radius-2xl);

&#x20; overflow: hidden;

&#x20; border: 1px solid var(--color-border);

&#x20; max-width: 720px;

&#x20; margin-inline: auto;

}



.recipe-hero {

&#x20; position: relative;

&#x20; aspect-ratio: 16 / 9;

&#x20; overflow: hidden;

}



.recipe-hero img {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; transition: scale var(--duration-slow) var(--ease-out);

}

.recipe-card:hover .recipe-hero img { scale: 1.04; }



/\* Overlay info \*/

.recipe-hero\_\_overlay {

&#x20; position: absolute;

&#x20; inset-block-end: 0;

&#x20; inset-inline: 0;

&#x20; padding: var(--space-6);

&#x20; background: linear-gradient(to top, rgb(0 0 0 / 0.75), transparent);

}



.recipe-category {

&#x20; display: inline-flex;

&#x20; padding: 0.25em 0.75em;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; margin-block-end: var(--space-2);

}



.recipe-title {

&#x20; font-size: var(--step-2);

&#x20; font-weight: var(--font-weight-black);

&#x20; color: white;

&#x20; text-wrap: balance;

&#x20; line-height: 1.2;

}



/\* Meta row \*/

.recipe-meta {

&#x20; display: flex;

&#x20; flex-wrap: wrap;

&#x20; gap: var(--space-6);

&#x20; padding: var(--space-5) var(--space-6);

&#x20; border-bottom: 1px solid var(--color-border);

}



.recipe-stat {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; text-align: center;

}



.recipe-stat\_\_icon { font-size: 1.25rem; }



.recipe-stat\_\_value {

&#x20; font-size: var(--font-size-lg);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-variant-numeric: tabular-nums;

}



.recipe-stat\_\_label {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wide);

&#x20; font-weight: var(--font-weight-medium);

}



/\* Difficulty \*/

.recipe-difficulty {

&#x20; display: flex;

&#x20; gap: 3px;

}

.difficulty-dot {

&#x20; width: 8px;

&#x20; height: 8px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-bg-muted);

}

.difficulty-dot.filled { background: var(--color-warning-500); }



/\* Body: ingredients + instructions \*/

.recipe-body {

&#x20; display: grid;

&#x20; grid-template-columns: 1fr 2fr;

&#x20; gap: 0;

}



@media (max-width: 600px) {

&#x20; .recipe-body { grid-template-columns: 1fr; }

}



.recipe-ingredients {

&#x20; padding: var(--space-6);

&#x20; border-right: 1px solid var(--color-border);

&#x20; background: var(--color-bg-subtle);

}



.recipe-instructions {

&#x20; padding: var(--space-6);

}



.recipe-section-title {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-black);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-4);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



/\* Ingredients list \*/

.ingredient-list {

&#x20; list-style: none;

&#x20; padding: 0;

&#x20; margin: 0;

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

}



.ingredient-item {

&#x20; display: flex;

&#x20; align-items: flex-start;

&#x20; gap: var(--space-3);

&#x20; font-size: var(--font-size-sm);

&#x20; padding-block: var(--space-1);

&#x20; border-bottom: 1px dashed var(--color-border);

&#x20; cursor: pointer;

&#x20; transition: color var(--duration-fast);

}

.ingredient-item.checked { color: var(--color-text-muted); text-decoration: line-through; }



.ingredient-checkbox {

&#x20; width: 1rem;

&#x20; height: 1rem;

&#x20; border-radius: var(--radius-sm);

&#x20; border: 1.5px solid var(--color-border);

&#x20; background: var(--color-surface);

&#x20; flex-shrink: 0;

&#x20; margin-top: 2px;

&#x20; transition: background var(--duration-fast), border-color var(--duration-fast);

}

.ingredient-item.checked .ingredient-checkbox {

&#x20; background: var(--color-success-500);

&#x20; border-color: var(--color-success-500);

}



.ingredient-amount { font-weight: var(--font-weight-semibold); white-space: nowrap; }

.ingredient-name   { color: var(--color-text-muted); }



/\* Instructions steps \*/

.step-list { list-style: none; padding: 0; margin: 0; counter-reset: step; }



.step-item {

&#x20; display: flex;

&#x20; gap: var(--space-4);

&#x20; padding-block: var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; counter-increment: step;

}

.step-item:last-child { border: none; }



.step-num {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

&#x20; color: white;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-sm);

&#x20; flex-shrink: 0;

}

.step-num::before { content: counter(step); }



.step-text { font-size: var(--font-size-sm); line-height: 1.7; color: var(--color-text-muted); }

.step-text strong { color: var(--color-text); font-weight: var(--font-weight-semibold); }



/\* Serving adjuster \*/

.servings-adj {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-sm);

}



.servings-btn {

&#x20; width: 1.5rem;

&#x20; height: 1.5rem;

&#x20; border-radius: 50%;

&#x20; border: 1px solid var(--color-border);

&#x20; background: var(--color-surface);

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-weight: bold;

&#x20; transition: background var(--duration-fast);

}

.servings-btn:hover { background: var(--color-bg-subtle); }



.servings-value { font-weight: var(--font-weight-bold); font-variant-numeric: tabular-nums; }

```



\---



```

╔══════════════════════════════════════════════════════════════════════╗

║                     PART 14 — COMPLETE                               ║

║  Chapters 193–202 | 10 new chapters | Output: css-guide-part14.md   ║

╚══════════════════════════════════════════════════════════════════════╝

```

