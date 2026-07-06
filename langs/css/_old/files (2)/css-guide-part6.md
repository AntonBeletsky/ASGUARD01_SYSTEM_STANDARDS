# PART VI — CSS: DEEP CUTS & SPECIALTY PATTERNS

---

## 101. HOVER EFFECTS LIBRARY

### 101.1 Image Hover Effects

```css
/* ─── 1. Zoom + overlay ─── */
.hover-zoom { position: relative; overflow: hidden; }
.hover-zoom img { transition: scale 0.5s var(--ease-out); display: block; width: 100%; }
.hover-zoom:hover img { scale: 1.08; }
.hover-zoom .overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgb(0 0 0 / 0.7) 0%, transparent 60%);
  opacity: 0; transition: opacity 0.4s;
  display: flex; align-items: flex-end; padding: var(--space-4);
  color: white;
}
.hover-zoom:hover .overlay { opacity: 1; }

/* ─── 2. Slide reveal ─── */
.hover-slide { position: relative; overflow: hidden; }
.hover-slide img { display: block; width: 100%; }
.hover-slide .caption {
  position: absolute; inset: 0;
  background: var(--color-accent);
  color: white;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  translate: 0 100%;
  transition: translate 0.4s var(--ease-out);
}
.hover-slide:hover .caption { translate: 0 0; }

/* ─── 3. Grayscale → color ─── */
.hover-color img {
  filter: grayscale(100%) contrast(1.1);
  transition: filter 0.5s var(--ease-out);
}
.hover-color:hover img { filter: grayscale(0%); }

/* ─── 4. Blur reveal ─── */
.hover-blur img {
  filter: blur(4px) brightness(0.7);
  scale: 1.05;
  transition: filter 0.4s, scale 0.4s;
}
.hover-blur:hover img { filter: blur(0) brightness(1); scale: 1; }

/* ─── 5. Flip card ─── */
.hover-flip { perspective: 800px; }
.hover-flip__inner {
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
  position: relative;
}
.hover-flip:hover .hover-flip__inner { transform: rotateY(180deg); }
.hover-flip__front, .hover-flip__back {
  backface-visibility: hidden;
}
.hover-flip__back {
  position: absolute; inset: 0;
  transform: rotateY(180deg);
}

/* ─── 6. Pan effect (image larger than container) ─── */
.hover-pan {
  overflow: hidden;
  cursor: crosshair;
}
.hover-pan img {
  width: 110%;
  max-width: none;
  translate: -5% 0;
  transition: translate 0.3s var(--ease-out);
}
/* JS: on mousemove → update translate based on cursor position */
.hover-pan:hover img {
  translate: calc(var(--px, 0) * -10%) calc(var(--py, 0) * -10%);
}
```

### 101.2 Button Hover Effects

```css
/* ─── 1. Fill from left ─── */
.btn-fill-left {
  position: relative; overflow: hidden;
  background: transparent;
  border: 2px solid var(--color-accent);
  color: var(--color-accent);
  z-index: 0;
}
.btn-fill-left::before {
  content: '';
  position: absolute; inset: 0;
  background: var(--color-accent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s var(--ease-out);
  z-index: -1;
}
.btn-fill-left:hover::before { transform: scaleX(1); }
.btn-fill-left:hover { color: white; }

/* ─── 2. Sheen / shimmer ─── */
.btn-sheen {
  background: var(--color-accent);
  color: white;
  overflow: hidden;
  position: relative;
}
.btn-sheen::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%;
  height: 100%;
  background: linear-gradient(
    to right,
    transparent 0%,
    rgba(255 255 255 / 0.3) 50%,
    transparent 100%
  );
  skewX(-20deg);
  transition: left 0.6s var(--ease-out);
}
.btn-sheen:hover::after { left: 140%; }

/* ─── 3. Neon pulse ─── */
.btn-neon {
  background: transparent;
  border: 2px solid var(--color-accent);
  color: var(--color-accent);
  transition: box-shadow 0.3s, background 0.3s, color 0.3s;
}
.btn-neon:hover {
  background: var(--color-accent);
  color: white;
  box-shadow:
    0 0 6px var(--color-accent),
    0 0 20px var(--color-accent),
    0 0 40px var(--color-accent);
}

/* ─── 4. 3D push ─── */
.btn-3d {
  background: var(--color-accent);
  color: white;
  box-shadow:
    0 6px 0 var(--color-accent-hover),
    0 8px 6px rgba(0 0 0 / 0.3);
  transition:
    box-shadow 0.1s,
    translate 0.1s;
}
.btn-3d:hover { translate: 0 2px; box-shadow: 0 4px 0 var(--color-accent-hover), 0 5px 4px rgba(0 0 0 / 0.2); }
.btn-3d:active { translate: 0 6px; box-shadow: 0 0 0 var(--color-accent-hover); }

/* ─── 5. Magnetic (via CSS vars from JS) ─── */
.btn-magnetic {
  transition: translate 0.15s var(--ease-out);
  translate: calc(var(--mx, 0) * 0.4) calc(var(--my, 0) * 0.4);
}

/* ─── 6. Typewriter CTA ─── */
.btn-typewriter {
  overflow: hidden;
  white-space: nowrap;
}
.btn-typewriter .label {
  display: inline-block;
  max-width: 0;
  overflow: hidden;
  transition: max-width 0.4s var(--ease-out);
  vertical-align: bottom;
}
.btn-typewriter:hover .label { max-width: 10em; }
```

### 101.3 Text Hover Effects

```css
/* ─── 1. Underline draw ─── */
.text-underline-draw {
  position: relative;
  text-decoration: none;
  display: inline-block;
}
.text-underline-draw::after {
  content: '';
  position: absolute;
  inset-inline: 0;
  bottom: -2px;
  height: 2px;
  background: currentColor;
  scale: 0 1;
  transform-origin: right;
  transition: scale 0.3s var(--ease-out), transform-origin 0s 0.3s;
}
.text-underline-draw:hover::after {
  scale: 1 1;
  transform-origin: left;
  transition: scale 0.3s var(--ease-out);
}

/* ─── 2. Character split color ─── */
.text-split-color {
  background: linear-gradient(
    to right,
    var(--color-accent) 50%,
    var(--color-text) 50%
  );
  background-size: 200% 100%;
  background-position: 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  transition: background-position 0.5s var(--ease-out);
}
.text-split-color:hover { background-position: 0%; }

/* ─── 3. Glitch text ─── */
.text-glitch {
  position: relative;
  color: var(--color-text);
}
.text-glitch::before,
.text-glitch::after {
  content: attr(data-text);
  position: absolute;
  inset: 0;
  opacity: 0;
}
.text-glitch:hover::before {
  opacity: 0.8;
  color: oklch(0.7 0.3 250);
  clip-path: polygon(0 0, 100% 0, 100% 40%, 0 40%);
  animation: glitch-before 0.4s steps(2) infinite;
}
.text-glitch:hover::after {
  opacity: 0.8;
  color: oklch(0.7 0.3 10);
  clip-path: polygon(0 60%, 100% 60%, 100% 100%, 0 100%);
  animation: glitch-after 0.4s steps(2) infinite;
}
@keyframes glitch-before { 0%,100% { translate: -2px 0; } 50% { translate: 2px 0; } }
@keyframes glitch-after  { 0%,100% { translate: 2px 0; } 50% { translate: -2px 0; } }

/* ─── 4. Letter spacing expand ─── */
.text-spacing {
  letter-spacing: normal;
  transition: letter-spacing 0.3s var(--ease-out);
}
.text-spacing:hover { letter-spacing: 0.15em; }

/* ─── 5. Weight pulse (variable font) ─── */
.text-weight {
  font-variation-settings: 'wght' 400;
  transition: font-variation-settings 0.3s;
}
.text-weight:hover { font-variation-settings: 'wght' 800; }
```

---

## 102. BORDER ANIMATIONS

```css
/* ─── 1. Rotating gradient border ─── */
@property --border-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.border-spinning {
  position: relative;
  border-radius: var(--radius-xl);
  padding: 2px;
  background: conic-gradient(
    from var(--border-angle),
    var(--color-brand-500) 0%,
    var(--color-brand-300) 25%,
    var(--color-brand-500) 50%,
    var(--color-brand-700) 75%,
    var(--color-brand-500) 100%
  );
  animation: border-spin 3s linear infinite;
}

@keyframes border-spin {
  to { --border-angle: 360deg; }
}

.border-spinning__inner {
  background: var(--color-surface);
  border-radius: calc(var(--radius-xl) - 2px);
  padding: var(--space-4);
}

/* ─── 2. Draw border on hover ─── */
.border-draw {
  position: relative;
}

.border-draw::before,
.border-draw::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
}

.border-draw::before {
  border-top: 2px solid var(--color-accent);
  border-right: 2px solid var(--color-accent);
  scale: 0 1;
  transform-origin: top right;
  transition: scale 0.3s var(--ease-out);
}

.border-draw::after {
  border-bottom: 2px solid var(--color-accent);
  border-left: 2px solid var(--color-accent);
  scale: 0 1;
  transform-origin: bottom left;
  transition: scale 0.3s var(--ease-out) 0.15s;
}

.border-draw:hover::before { scale: 1 1; }
.border-draw:hover::after  { scale: 1 1; }

/* ─── 3. Corner brackets ─── */
.border-corners {
  position: relative;
  padding: var(--space-4);
}

.border-corners::before,
.border-corners::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  transition: width 0.3s, height 0.3s;
}

.border-corners::before {
  inset-block-start: 0;
  inset-inline-start: 0;
  border-top: 2px solid var(--color-accent);
  border-left: 2px solid var(--color-accent);
}

.border-corners::after {
  inset-block-end: 0;
  inset-inline-end: 0;
  border-bottom: 2px solid var(--color-accent);
  border-right: 2px solid var(--color-accent);
}

.border-corners:hover::before,
.border-corners:hover::after { width: 100%; height: 100%; }

/* ─── 4. Marching ants ─── */
@keyframes march {
  to { stroke-dashoffset: -20; }
}

.border-marching {
  outline: none;
  position: relative;
}

.border-marching::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  background: repeating-linear-gradient(
    90deg,
    var(--color-accent) 0 8px,
    transparent 8px 16px
  ) top / 100% 2px no-repeat,
  repeating-linear-gradient(
    180deg,
    var(--color-accent) 0 8px,
    transparent 8px 16px
  ) right / 2px 100% no-repeat,
  repeating-linear-gradient(
    270deg,
    var(--color-accent) 0 8px,
    transparent 8px 16px
  ) bottom / 100% 2px no-repeat,
  repeating-linear-gradient(
    0deg,
    var(--color-accent) 0 8px,
    transparent 8px 16px
  ) left / 2px 100% no-repeat;
  animation: march-h 0.5s linear infinite, march-v 0.5s linear infinite;
}

@keyframes march-h { to { background-position: calc(100% + 16px) top, right, calc(-100% - 16px) bottom, left; } }

/* ─── 5. Pulsing outline ─── */
@keyframes outline-pulse {
  0%   { outline-offset: 0; outline-color: var(--color-accent); }
  50%  { outline-offset: 6px; outline-color: color-mix(in srgb, var(--color-accent) 30%, transparent); }
  100% { outline-offset: 0; outline-color: var(--color-accent); }
}

.border-pulse:hover {
  animation: outline-pulse 1.5s ease-in-out infinite;
  outline: 2px solid var(--color-accent);
}

/* ─── 6. Gradient border via mask ─── */
.border-gradient {
  position: relative;
  border-radius: var(--radius-xl);
  background: var(--color-surface);
}

.border-gradient::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  background: linear-gradient(135deg, var(--color-brand-400), var(--color-brand-700));
  z-index: -1;
}
```

---

## 103. IMAGE COMPARISON SLIDER

```css
/* ─── Before/After comparison (CSS-only via input[range]) ─── */
.comparison {
  position: relative;
  overflow: hidden;
  --split: 50%;
}

.comparison__before,
.comparison__after {
  position: absolute;
  inset: 0;
}

.comparison__before img,
.comparison__after img {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}

.comparison__after {
  clip-path: inset(0 0 0 var(--split));
}

/* Divider line */
.comparison__divider {
  position: absolute;
  top: 0; bottom: 0;
  left: var(--split);
  width: 2px;
  background: white;
  box-shadow: 0 0 8px rgba(0 0 0 / 0.5);
  z-index: 2;
}

/* Handle */
.comparison__handle {
  position: absolute;
  top: 50%;
  left: var(--split);
  translate: -50% -50%;
  width: 2.5rem;
  height: 2.5rem;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 12px rgba(0 0 0 / 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
  cursor: ew-resize;
}

.comparison__handle::before,
.comparison__handle::after {
  content: '';
  border: 6px solid transparent;
}

.comparison__handle::before {
  border-right-color: var(--color-text);
  margin-right: 2px;
}

.comparison__handle::after {
  border-left-color: var(--color-text);
  margin-left: 2px;
}

/* Range input overlay */
.comparison__range {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: ew-resize;
  width: 100%;
  z-index: 4;
}

/* JS: input.addEventListener('input', e => el.style.setProperty('--split', e.target.value + '%')) */
```

---

## 104. KANBAN BOARD

```css
/* ─── Kanban layout ─── */
.kanban {
  display: flex;
  gap: var(--space-4);
  overflow-x: auto;
  padding-block: var(--space-2);
  align-items: flex-start;
  min-height: calc(100dvh - var(--header-height, 60px));
  scrollbar-width: thin;
}

/* Column */
.kanban-col {
  flex: 0 0 280px;
  background: var(--color-bg-subtle);
  border-radius: var(--radius-xl);
  display: flex;
  flex-direction: column;
  max-height: calc(100dvh - var(--header-height, 60px) - var(--space-8));
}

.kanban-col__header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  background: inherit;
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
  z-index: 1;
}

.kanban-col__title {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  flex: 1;
}

.kanban-col__count {
  background: var(--color-bg-muted);
  color: var(--color-text-muted);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  padding: 0.15em 0.5em;
  border-radius: var(--radius-full);
  font-variant-numeric: tabular-nums;
}

/* Column color accents */
.kanban-col--todo   .kanban-col__header { border-top: 3px solid var(--color-neutral-400); }
.kanban-col--doing  .kanban-col__header { border-top: 3px solid var(--color-brand-500); }
.kanban-col--review .kanban-col__header { border-top: 3px solid var(--color-warning-500); }
.kanban-col--done   .kanban-col__header { border-top: 3px solid var(--color-success-500); }

/* Cards list */
.kanban-col__cards {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-3) var(--space-3) var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  scrollbar-width: thin;
}

/* Kanban card */
.kanban-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-3);
  cursor: grab;
  user-select: none;
  transition:
    box-shadow var(--duration-fast),
    scale      var(--duration-fast) var(--ease-bounce);
}

.kanban-card:hover {
  box-shadow: var(--shadow-md);
}

.kanban-card.dragging {
  opacity: 0.5;
  scale: 1.02;
  cursor: grabbing;
  box-shadow: var(--shadow-xl);
}

/* Drop zone */
.kanban-col__cards.drag-over {
  background: color-mix(in srgb, var(--color-accent) 5%, transparent);
  outline: 2px dashed var(--color-accent);
  outline-offset: -4px;
  border-radius: 0 0 var(--radius-xl) var(--radius-xl);
}

.kanban-card__title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  margin-block-end: var(--space-2);
}

.kanban-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-1);
  margin-block-end: var(--space-3);
}

.kanban-tag {
  padding: 0.125em 0.5em;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.kanban-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
}

.kanban-card__due {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: 0.25em;
}

.kanban-card__due--overdue { color: var(--color-danger-500); }
.kanban-card__due--soon    { color: var(--color-warning-500); }

.kanban-card__avatars {
  display: flex;
}

.kanban-card__avatars .avatar {
  --size: 1.5rem;
  border: 2px solid var(--color-surface);
  margin-inline-start: -0.5rem;
}
.kanban-card__avatars .avatar:first-child { margin-inline-start: 0; }

/* Add column / Add card buttons */
.kanban-add-card {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  border: none;
  background: none;
  width: 100%;
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.kanban-add-card:hover { background: var(--color-bg-muted); color: var(--color-text); }
```

---

## 105. TERMINAL / CONSOLE UI

```css
/* ─── Terminal window ─── */
.terminal {
  background: #1a1a1a;
  border-radius: var(--radius-xl);
  overflow: hidden;
  font-family: var(--font-mono);
  font-size: 0.875rem;
  box-shadow: var(--shadow-2xl);
  color: #d4d4d4;
}

.terminal__titlebar {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.625rem 1rem;
  background: #2d2d2d;
  border-bottom: 1px solid #3a3a3a;
}

.terminal__dot { width: 12px; height: 12px; border-radius: 50%; }
.terminal__dot--red    { background: #ff5f57; }
.terminal__dot--yellow { background: #febc2e; }
.terminal__dot--green  { background: #28c840; }

.terminal__title {
  flex: 1;
  text-align: center;
  font-size: 0.75rem;
  color: #888;
}

.terminal__body {
  padding: 1rem 1.25rem;
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
  line-height: 1.6;
  scrollbar-width: thin;
  scrollbar-color: #444 transparent;
}

/* Lines */
.terminal__line {
  display: flex;
  align-items: flex-start;
  gap: 0.5em;
  margin-block-end: 0.125em;
  white-space: pre-wrap;
  word-break: break-all;
}

.terminal__prompt {
  color: #4ec9b0;
  user-select: none;
  flex-shrink: 0;
}

.terminal__prompt::before { content: '$ '; }

.terminal__cmd  { color: #d4d4d4; }
.terminal__out  { color: #888; padding-inline-start: 1.5em; }
.terminal__err  { color: #f48771; padding-inline-start: 1.5em; }
.terminal__ok   { color: #4ec9b0; padding-inline-start: 1.5em; }
.terminal__info { color: #9cdcfe; padding-inline-start: 1.5em; }

/* Blinking cursor */
.terminal__cursor {
  display: inline-block;
  width: 0.55em;
  height: 1.1em;
  background: #d4d4d4;
  vertical-align: text-bottom;
  animation: cursor-blink 1s step-end infinite;
}

@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* Syntax highlighting */
.term-string  { color: #ce9178; }
.term-number  { color: #b5cea8; }
.term-bool    { color: #569cd6; }
.term-null    { color: #569cd6; }
.term-key     { color: #9cdcfe; }
.term-comment { color: #6a9955; }

/* ─── Command output animations ─── */
.terminal__line {
  animation: line-appear 0.15s ease-out backwards;
}

@keyframes line-appear {
  from { opacity: 0; translate: 0 4px; }
}

/* Stagger each new line */
.terminal__line:nth-child(n) {
  animation-delay: calc(var(--line-index, 0) * 0.05s);
}

/* ─── Progress bar in terminal ─── */
.term-progress {
  display: flex;
  align-items: center;
  gap: 0.75em;
  color: #4ec9b0;
  font-size: 0.875em;
}

.term-progress__bar {
  flex: 1;
  height: 4px;
  background: #333;
  border-radius: 2px;
  overflow: hidden;
}

.term-progress__fill {
  height: 100%;
  background: #4ec9b0;
  width: var(--progress, 0%);
  transition: width 0.3s;
}

/* ─── JSON viewer ─── */
.json-viewer {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  line-height: 1.7;
  color: #d4d4d4;
}

.json-key    { color: #9cdcfe; }
.json-str    { color: #ce9178; }
.json-num    { color: #b5cea8; }
.json-bool   { color: #569cd6; }
.json-null   { color: #569cd6; }
.json-punc   { color: #d4d4d4; }

/* Collapsible JSON tree */
.json-toggle {
  cursor: pointer;
  user-select: none;
  background: none;
  border: none;
  color: inherit;
  padding: 0;
  font: inherit;
}
.json-toggle::before { content: '▾ '; font-size: 0.7em; }
.json-toggle.collapsed::before { content: '▸ '; }
.json-nested { padding-inline-start: 1.5em; }
.json-nested.collapsed { display: none; }
```

---

## 106. MEDIA PLAYER UI

### 106.1 Audio Player

```css
/* ─── Custom audio player ─── */
.audio-player {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-5);
  max-width: 380px;
}

.audio-player__header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.audio-player__art {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: var(--radius-lg);
  object-fit: cover;
  flex-shrink: 0;
  box-shadow: var(--shadow-md);
}

.audio-player__info { min-width: 0; flex: 1; }

.audio-player__title {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.audio-player__artist {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

/* Waveform (decorative) */
.audio-waveform {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  height: 40px;
  overflow: hidden;
}

.waveform-bar {
  width: 3px;
  background: var(--color-accent);
  border-radius: 2px;
  height: calc(var(--h, 0.5) * 100%);
  opacity: 0.7;
  transition: height 0.1s;
}

/* Playing animation */
.audio-player.playing .waveform-bar {
  animation: wave-bounce var(--d, 0.8s) ease-in-out infinite alternate;
  animation-delay: var(--delay, 0s);
  opacity: 1;
}

@keyframes wave-bounce {
  from { height: 20%; }
  to   { height: calc(var(--h, 0.5) * 100%); }
}

/* Progress */
.audio-progress {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.audio-progress__bar {
  flex: 1;
  height: 4px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  cursor: pointer;
  position: relative;
}

.audio-progress__fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: inherit;
  width: var(--progress, 0%);
  position: relative;
}

.audio-progress__fill::after {
  content: '';
  position: absolute;
  right: -5px;
  top: 50%;
  translate: 0 -50%;
  width: 12px;
  height: 12px;
  background: var(--color-accent);
  border-radius: 50%;
  opacity: 0;
  transition: opacity var(--duration-fast);
  box-shadow: var(--shadow-sm);
}

.audio-progress__bar:hover .audio-progress__fill::after { opacity: 1; }

/* Controls */
.audio-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
}

.audio-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: color var(--duration-fast), background var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
  width: 2rem;
  height: 2rem;
}

.audio-btn:hover { color: var(--color-text); background: var(--color-bg-subtle); }

.audio-btn--play {
  width: 3rem;
  height: 3rem;
  background: var(--color-accent);
  color: white;
}

.audio-btn--play:hover {
  background: var(--color-accent-hover);
  color: white;
  scale: 1.05;
}

/* Volume */
.audio-volume {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.volume-slider {
  width: 60px;
  height: 4px;
  appearance: none;
  background: linear-gradient(
    to right,
    var(--color-accent) var(--volume, 80%),
    var(--color-bg-muted) var(--volume, 80%)
  );
  border-radius: var(--radius-full);
  outline: none;
  cursor: pointer;
}

.volume-slider::-webkit-slider-thumb {
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-accent);
  cursor: pointer;
}
```

### 106.2 Video Player

```css
/* ─── Custom video player ─── */
.video-player {
  position: relative;
  background: #000;
  border-radius: var(--radius-xl);
  overflow: hidden;
  aspect-ratio: 16 / 9;
  cursor: pointer;
}

.video-player video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Controls overlay */
.video-controls {
  position: absolute;
  inset-inline: 0;
  bottom: 0;
  padding: var(--space-4);
  background: linear-gradient(to top, rgba(0 0 0 / 0.8), transparent);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);

  opacity: 0;
  translate: 0 4px;
  transition:
    opacity var(--duration-normal),
    translate var(--duration-normal);
}

.video-player:hover .video-controls,
.video-player:focus-within .video-controls,
.video-player.paused .video-controls {
  opacity: 1;
  translate: 0 0;
}

/* Seekbar */
.video-seekbar {
  width: 100%;
  height: 4px;
  background: rgba(255 255 255 / 0.3);
  border-radius: var(--radius-full);
  cursor: pointer;
  position: relative;
  transition: height var(--duration-fast);
}

.video-seekbar:hover { height: 6px; }

/* Buffered progress */
.video-seekbar__buffered {
  position: absolute;
  inset-block: 0;
  inset-inline-start: 0;
  width: var(--buffered, 0%);
  background: rgba(255 255 255 / 0.4);
  border-radius: inherit;
}

.video-seekbar__fill {
  position: absolute;
  inset-block: 0;
  inset-inline-start: 0;
  width: var(--progress, 0%);
  background: var(--color-accent);
  border-radius: inherit;
}

.video-seekbar__thumb {
  position: absolute;
  top: 50%;
  left: var(--progress, 0%);
  translate: -50% -50%;
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--duration-fast);
  box-shadow: var(--shadow-sm);
}

.video-seekbar:hover .video-seekbar__thumb { opacity: 1; }

/* Controls row */
.video-controls__row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.video-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  opacity: 0.85;
  display: flex;
  align-items: center;
  padding: var(--space-1);
  border-radius: var(--radius-md);
  transition: opacity var(--duration-fast);
}

.video-btn:hover { opacity: 1; }

.video-time {
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.85);
  font-variant-numeric: tabular-nums;
  font-family: var(--font-mono);
  white-space: nowrap;
  margin-inline-end: auto;
}

/* Big play button in center */
.video-play-btn {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.video-play-btn__icon {
  width: 4rem;
  height: 4rem;
  background: rgba(255 255 255 / 0.15);
  backdrop-filter: blur(8px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  transition: opacity var(--duration-slow), scale var(--duration-slow);
  scale: 1;
  opacity: 1;
}

.video-player.playing .video-play-btn__icon {
  opacity: 0;
  scale: 1.5;
}
```

---

## 107. NOTIFICATION CENTER

```css
/* ─── Notification bell with count ─── */
.notif-bell {
  position: relative;
  display: inline-flex;
}

.notif-bell__count {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 1.125rem;
  height: 1.125rem;
  background: var(--color-danger-500);
  color: white;
  border-radius: var(--radius-full);
  font-size: 0.625rem;
  font-weight: var(--font-weight-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  padding-inline: 0.25rem;
  border: 2px solid var(--color-bg);
  animation: badge-in 0.3s var(--ease-bounce);
}

@keyframes badge-in {
  from { scale: 0; }
}

/* ─── Notification panel ─── */
.notif-panel {
  width: 360px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  max-height: 80dvh;
  display: flex;
  flex-direction: column;
}

.notif-panel__header {
  display: flex;
  align-items: center;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  gap: var(--space-3);
}

.notif-panel__title {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  flex: 1;
}

.notif-panel__mark-all {
  font-size: var(--font-size-xs);
  color: var(--color-accent);
  background: none;
  border: none;
  cursor: pointer;
}

.notif-list {
  overflow-y: auto;
  flex: 1;
  scrollbar-width: thin;
}

/* Individual notification */
.notif-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background var(--duration-fast);
  position: relative;
  text-decoration: none;
  color: inherit;
}

.notif-item:hover { background: var(--color-bg-subtle); }

/* Unread indicator */
.notif-item--unread { background: color-mix(in srgb, var(--color-accent) 4%, var(--color-surface)); }
.notif-item--unread::before {
  content: '';
  position: absolute;
  inset-block: 0;
  inset-inline-start: 0;
  width: 3px;
  background: var(--color-accent);
}

.notif-item__icon {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
  background: var(--color-bg-muted);
}

.notif-item__icon--success { background: var(--color-success-100); }
.notif-item__icon--warning { background: var(--color-warning-100); }
.notif-item__icon--error   { background: var(--color-danger-100); }
.notif-item__icon--info    { background: var(--color-brand-100); }

.notif-item__body { flex: 1; min-width: 0; }

.notif-item__text {
  font-size: var(--font-size-sm);
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.notif-item__text strong { font-weight: var(--font-weight-semibold); }

.notif-item__time {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-block-start: var(--space-1);
}

/* Dismiss button */
.notif-item__dismiss {
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  border: none;
  background: var(--color-bg-muted);
  color: var(--color-text-muted);
  font-size: 0.625rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--duration-fast);
}

.notif-item:hover .notif-item__dismiss { opacity: 1; }

/* Notification group by date */
.notif-group-label {
  padding: var(--space-2) var(--space-5);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  background: var(--color-bg-subtle);
  position: sticky;
  top: 0;
  z-index: 1;
}

/* Empty state */
.notif-empty {
  padding: var(--space-12);
  text-align: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
}

/* Inline toast within panel */
.notif-panel__footer {
  padding: var(--space-3) var(--space-5);
  border-top: 1px solid var(--color-border);
  text-align: center;
}

.notif-panel__footer a {
  font-size: var(--font-size-sm);
  color: var(--color-accent);
  text-decoration: none;
}
```

---

## 108. DOCUMENT LAYOUTS: INVOICE & CV

### 108.1 Invoice / Receipt

```css
/* ─── Invoice layout ─── */
.invoice {
  max-width: 720px;
  margin-inline: auto;
  padding: var(--space-12);
  background: var(--color-surface);
  font-size: var(--font-size-sm);
  color: var(--color-text);

  @media print {
    padding: 0;
    max-width: none;
  }
}

.invoice__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-block-end: var(--space-10);
}

.invoice__logo {
  font-size: var(--step-3);
  font-weight: var(--font-weight-black);
  color: var(--color-text);
  letter-spacing: -0.03em;
}

.invoice__badge {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  padding: 0.25em 0.75em;
  border-radius: var(--radius-sm);
  background: var(--color-brand-100);
  color: var(--color-brand-700);
}

.invoice__badge--paid { background: var(--color-success-100); color: var(--color-success-700); }
.invoice__badge--due  { background: var(--color-warning-100); color: var(--color-warning-700); }
.invoice__badge--overdue { background: var(--color-danger-100); color: var(--color-danger-700); }

/* Metadata grid */
.invoice__meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  margin-block-end: var(--space-8);
}

.invoice__address { }

.invoice__label {
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-semibold);
  margin-block-end: var(--space-1);
}

.invoice__details {
  display: grid;
  grid-template-columns: auto auto;
  gap: var(--space-1) var(--space-6);
  margin-block-end: var(--space-8);
}

.invoice__detail-label {
  color: var(--color-text-muted);
  font-size: var(--font-size-xs);
}

/* Line items table */
.invoice__table {
  width: 100%;
  border-collapse: collapse;
  margin-block-end: var(--space-6);
}

.invoice__table th {
  text-align: start;
  padding-block: var(--space-2);
  padding-inline: var(--space-3);
  border-bottom: 2px solid var(--color-border);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-semibold);
}

.invoice__table th:last-child,
.invoice__table td:last-child {
  text-align: end;
}

.invoice__table td {
  padding: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.invoice__table tbody tr:last-child td { border: none; }

/* Totals */
.invoice__totals {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--space-1) var(--space-8);
  max-width: 280px;
  margin-inline-start: auto;
  margin-block-end: var(--space-8);
}

.invoice__totals-label { color: var(--color-text-muted); font-size: var(--font-size-sm); }
.invoice__totals-value { text-align: end; font-variant-numeric: tabular-nums; }

.invoice__total-row { font-weight: var(--font-weight-bold); font-size: var(--font-size-base); border-top: 2px solid var(--color-border); padding-block-start: var(--space-2); }

/* Notes */
.invoice__notes {
  padding: var(--space-4);
  background: var(--color-bg-subtle);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  border: 1px solid var(--color-border);
}
```

### 108.2 Resume / CV Layout

```css
/* ─── CV / Resume ─── */
.cv {
  max-width: 800px;
  margin-inline: auto;
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100%;
  font-size: 0.875rem;

  @media print {
    max-width: none;
    font-size: 10pt;
  }
}

/* Left column */
.cv__sidebar {
  background: var(--color-neutral-900);
  color: var(--color-neutral-100);
  padding: var(--space-8) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.cv__photo {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--color-neutral-700);
  margin-inline: auto;
  display: block;
}

.cv__name {
  text-align: center;
  font-size: 1.25rem;
  font-weight: var(--font-weight-bold);
  margin-block-end: 0.25rem;
}

.cv__title {
  text-align: center;
  font-size: 0.75rem;
  color: var(--color-neutral-400);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.cv__section-title {
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--color-neutral-400);
  font-weight: var(--font-weight-bold);
  margin-block-end: var(--space-3);
  padding-block-end: var(--space-1);
  border-bottom: 1px solid var(--color-neutral-700);
}

.cv__contact-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.8125rem;
  color: var(--color-neutral-300);
  margin-block-end: var(--space-2);
  text-decoration: none;
}

.cv__contact-item:hover { color: white; }

/* Skills */
.cv__skill {
  margin-block-end: var(--space-2);
}

.cv__skill-name {
  font-size: 0.8125rem;
  margin-block-end: 0.25rem;
  color: var(--color-neutral-200);
}

.cv__skill-bar {
  height: 4px;
  background: var(--color-neutral-700);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.cv__skill-fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: inherit;
  width: var(--level, 0%);
}

/* Right column */
.cv__main {
  padding: var(--space-8) var(--space-7);
  display: flex;
  flex-direction: column;
  gap: var(--space-7);
}

.cv__main-section-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--color-neutral-900);
  padding-block-end: var(--space-2);
  border-bottom: 2px solid var(--color-accent);
  margin-block-end: var(--space-4);
}

/* Experience item */
.cv__exp-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--space-1);
  margin-block-end: var(--space-5);
}

.cv__exp-title {
  font-weight: var(--font-weight-semibold);
  font-size: 0.9375rem;
}

.cv__exp-company {
  color: var(--color-accent);
  font-size: 0.875rem;
}

.cv__exp-date {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-align: end;
  grid-column: 2;
  grid-row: 1;
  white-space: nowrap;
}

.cv__exp-desc {
  grid-column: 1 / -1;
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-block-start: var(--space-1);
}

.cv__exp-bullets {
  grid-column: 1 / -1;
  padding-inline-start: 1em;
  margin-block-start: var(--space-2);
}

.cv__exp-bullets li {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  margin-block-end: var(--space-1);
  line-height: 1.5;
}
```

---

## 109. CSS COUNTERS — ADVANCED PATTERNS

```css
/* ─── Legal document numbering (1.1.1 style) ─── */
.legal-doc {
  counter-reset: chapter;
}
.legal-doc h1 {
  counter-increment: chapter;
  counter-reset: section;
}
.legal-doc h1::before {
  content: counter(chapter) '. ';
}
.legal-doc h2 {
  counter-increment: section;
  counter-reset: subsection;
}
.legal-doc h2::before {
  content: counter(chapter) '.' counter(section) '. ';
}
.legal-doc h3 {
  counter-increment: subsection;
}
.legal-doc h3::before {
  content: counter(chapter) '.' counter(section) '.' counter(subsection) '. ';
}

/* ─── Step counter with circle indicators ─── */
.steps-counter {
  counter-reset: step;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.step-item {
  display: flex;
  gap: var(--space-4);
  counter-increment: step;
}

.step-item::before {
  content: counter(step);
  flex-shrink: 0;
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
  margin-block-start: 0.125rem;
}

/* ─── Progress with counters ─── */
.reading-progress {
  counter-reset: words characters;
}
.reading-progress p {
  counter-increment: words 50;    /* approximation */
}
/* Not truly countable from CSS alone, but useful for footnotes etc */

/* ─── Footnote system ─── */
:root { counter-reset: footnote; }

.footnote {
  counter-increment: footnote;
}

.footnote::after {
  content: '[' counter(footnote) ']';
  vertical-align: super;
  font-size: 0.7em;
  color: var(--color-accent);
  text-decoration: none;
  margin-inline-start: 0.1em;
}

.footnotes-list { counter-reset: footnote-ref; }
.footnotes-list li {
  counter-increment: footnote-ref;
  list-style: none;
}
.footnotes-list li::before {
  content: '[' counter(footnote-ref) '] ';
  color: var(--color-accent);
  font-weight: var(--font-weight-bold);
}

/* ─── Figure / Table numbering ─── */
.document {
  counter-reset: figure table;
}

.figure {
  counter-increment: figure;
}
.figure figcaption::before {
  content: 'Figure ' counter(figure) ': ';
  font-weight: var(--font-weight-semibold);
}

.data-table {
  counter-increment: table;
}
.data-table caption::before {
  content: 'Table ' counter(table) ': ';
  font-weight: var(--font-weight-semibold);
}
```

---

## 110. CSS GRID: MAGAZINE LAYOUTS

```css
/* ─── Classic magazine grid ─── */
.magazine {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-auto-rows: auto;
  gap: var(--space-4);
  max-width: 1200px;
  margin-inline: auto;
}

/* Featured story (top-left, large) */
.story--hero {
  grid-column: 1 / 8;
  grid-row: 1 / 3;
}

/* Secondary stories */
.story--secondary {
  grid-column: 8 / 13;
  grid-row: 1;
}

.story--secondary:nth-of-type(2) {
  grid-column: 8 / 13;
  grid-row: 2;
}

/* Full-width divider story */
.story--full {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

/* 3-column row */
.story--third {
  grid-column: span 4;
}

/* Responsive */
@media (max-width: 768px) {
  .magazine {
    grid-template-columns: 1fr;
  }
  .story--hero,
  .story--secondary,
  .story--third,
  .story--full {
    grid-column: 1;
    grid-row: auto;
  }
  .story--full { grid-template-columns: 1fr; }
}

/* ─── Story card base ─── */
.story {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.story__image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

.story--hero .story__image { aspect-ratio: 16 / 10; }

.story__body { padding: var(--space-4); flex: 1; display: flex; flex-direction: column; gap: var(--space-2); }

.story__category {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-accent);
}

.story__title {
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-snug);
  text-wrap: balance;
}

.story--hero .story__title {
  font-size: clamp(1.25rem, 2.5vw, 2rem);
}

.story__excerpt {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.story__meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-block-start: auto;
  padding-block-start: var(--space-3);
  border-top: 1px solid var(--color-border);
}

.story__author {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.story__author img {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  object-fit: cover;
}

.story__date {
  font-size: var(--font-size-xs);
  color: var(--color-text-subtle);
  margin-inline-start: auto;
}

/* ─── Newsletter layout ─── */
.newsletter {
  max-width: 600px;
  margin-inline: auto;
  font-family: Georgia, serif;
  color: #333;
  background: #fff;
}

.newsletter__header {
  background: #1a1a2e;
  padding: var(--space-8);
  text-align: center;
  color: white;
}

.newsletter__logo {
  font-size: 2rem;
  font-weight: bold;
  letter-spacing: -0.03em;
}

.newsletter__tagline {
  font-size: 0.875rem;
  opacity: 0.7;
  font-style: italic;
}

.newsletter__date {
  font-size: 0.75rem;
  opacity: 0.5;
  margin-block-start: var(--space-2);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.newsletter__body { padding: var(--space-6); }

.newsletter__intro {
  font-size: 1rem;
  line-height: 1.7;
  border-inline-start: 3px solid var(--color-accent);
  padding-inline-start: var(--space-4);
  color: #555;
  margin-block-end: var(--space-6);
}

.newsletter__story {
  margin-block-end: var(--space-6);
  padding-block-end: var(--space-6);
  border-bottom: 1px solid #eee;
}

.newsletter__story:last-child { border: none; }

.newsletter__story-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-block-end: var(--space-2);
  line-height: 1.3;
}

.newsletter__story-title a { color: inherit; text-decoration: none; }
.newsletter__story-title a:hover { color: var(--color-accent); }

.newsletter__story-text {
  font-size: 0.9375rem;
  line-height: 1.65;
  color: #444;
}

.newsletter__cta {
  display: inline-block;
  background: var(--color-accent);
  color: white;
  padding: 0.625rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: bold;
  margin-block-start: var(--space-3);
}

.newsletter__footer {
  background: #f5f5f5;
  padding: var(--space-6);
  text-align: center;
  font-size: 0.75rem;
  color: #999;
  border-top: 1px solid #ddd;
}
```

---

## 111. CSS FOR SPECIFIC INTERACTIONS

### 111.1 Drag and Drop Visual Feedback

```css
/* ─── Draggable item ─── */
.draggable {
  cursor: grab;
  user-select: none;
  transition:
    box-shadow var(--duration-fast),
    scale      var(--duration-fast) var(--ease-bounce),
    opacity    var(--duration-fast);
}

.draggable:active { cursor: grabbing; }

.draggable[draggable="true"]:active,
.draggable.is-dragging {
  opacity: 0.5;
  scale: 1.02;
  box-shadow: var(--shadow-xl);
  cursor: grabbing;
  z-index: var(--z-raised);
  position: relative;
}

/* Drop target */
.drop-target {
  transition:
    background var(--duration-fast),
    border-color var(--duration-fast);
  border: 2px solid transparent;
  border-radius: var(--radius-lg);
}

.drop-target.drag-over {
  background: color-mix(in srgb, var(--color-accent) 8%, var(--color-surface));
  border-color: var(--color-accent);
}

.drop-target.drag-over--reject {
  background: color-mix(in srgb, var(--color-danger-500) 8%, var(--color-surface));
  border-color: var(--color-danger-500);
}

/* Ghost placeholder (where item will be dropped) */
.drag-ghost {
  border: 2px dashed var(--color-accent);
  border-radius: var(--radius-lg);
  opacity: 0.5;
  background: color-mix(in srgb, var(--color-accent) 10%, transparent);
  height: var(--ghost-height, 60px);
  transition: height var(--duration-fast) var(--ease-out);
}

/* Drag handle icon */
.drag-handle {
  cursor: grab;
  color: var(--color-text-muted);
  padding: var(--space-1);
  opacity: 0;
  transition: opacity var(--duration-fast);
}

.draggable:hover .drag-handle { opacity: 1; }
.draggable:active .drag-handle { cursor: grabbing; opacity: 1; }
```

### 111.2 Swipe-able Cards (Mobile)

```css
/* ─── Swipe card deck ─── */
.swipe-deck {
  position: relative;
  width: 300px;
  height: 400px;
}

.swipe-card {
  position: absolute;
  inset: 0;
  border-radius: var(--radius-2xl);
  background: var(--color-surface);
  box-shadow: var(--shadow-xl);
  cursor: grab;
  user-select: none;
  transform-origin: bottom center;
  transition: transform var(--duration-normal) var(--ease-out);
}

/* Stack of cards */
.swipe-card:nth-child(1) { z-index: 3; }
.swipe-card:nth-child(2) { z-index: 2; scale: 0.95; translate: 0 16px; }
.swipe-card:nth-child(3) { z-index: 1; scale: 0.9;  translate: 0 32px; }

/* JS sets --tx and --rotate on the top card */
.swipe-card.is-top {
  translate: var(--tx, 0) var(--ty, 0);
  rotate: var(--rotate, 0deg);
  transition: none;  /* real-time drag */
}

.swipe-card.swiped-right {
  translate: 200% var(--ty, 0);
  rotate: 30deg;
  opacity: 0;
  transition:
    translate 0.5s var(--ease-out),
    rotate    0.5s var(--ease-out),
    opacity   0.3s;
}

.swipe-card.swiped-left {
  translate: -200% var(--ty, 0);
  rotate: -30deg;
  opacity: 0;
  transition:
    translate 0.5s var(--ease-out),
    rotate    0.5s var(--ease-out),
    opacity   0.3s;
}

/* Like / Dislike indicators */
.swipe-like,
.swipe-nope {
  position: absolute;
  top: var(--space-6);
  padding: 0.5rem 1rem;
  border: 3px solid;
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-black);
  font-size: 1.5rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0;
  rotate: -20deg;
  pointer-events: none;
  transition: opacity var(--duration-fast);
}

.swipe-like {
  inset-inline-start: var(--space-6);
  color: var(--color-success-500);
  border-color: var(--color-success-500);
  rotate: -20deg;
}

.swipe-nope {
  inset-inline-end: var(--space-6);
  color: var(--color-danger-500);
  border-color: var(--color-danger-500);
  rotate: 20deg;
}

/* JS sets --tx > 50 → show like; --tx < -50 → show nope */
.swipe-card.showing-like .swipe-like { opacity: calc((var(--tx, 0) - 50) / 100); }
.swipe-card.showing-nope .swipe-nope { opacity: calc((var(--tx, 0) * -1 - 50) / 100); }
```

### 111.3 Scroll-linked Effects

```css
/* ─── Hero parallax header ─── */
.parallax-hero {
  position: relative;
  height: 80dvh;
  overflow: hidden;
}

.parallax-hero__bg {
  position: absolute;
  inset: -30%;
  width: 160%;
  height: 160%;
  object-fit: cover;

  /* Scroll-driven parallax */
  animation: parallax-scroll linear both;
  animation-timeline: scroll(root);
  animation-range: 0% 100vh;
}

@keyframes parallax-scroll {
  from { translate: 0 0; }
  to   { translate: 0 30%; }
}

.parallax-hero__content {
  position: relative;
  z-index: 1;
  /* Opposite direction — content scrolls slower */
  animation: parallax-content linear both;
  animation-timeline: scroll(root);
  animation-range: 0% 100vh;
}

@keyframes parallax-content {
  from { translate: 0 0; opacity: 1; }
  to   { translate: 0 -20%; opacity: 0; }
}

/* ─── Sticky section with progress ─── */
.sticky-section {
  height: 300vh;  /* tall container for scroll room */
  position: relative;
}

.sticky-section__inner {
  position: sticky;
  top: 0;
  height: 100dvh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

/* Track progress within sticky section */
.sticky-section {
  view-timeline: --section block;
}

.sticky-progress-bar {
  position: fixed;
  top: 0; left: 0;
  height: 3px;
  background: var(--color-accent);
  width: 0%;
  animation: track linear both;
  animation-timeline: --section;
  animation-range: contain;
}

@keyframes track {
  from { width: 0%; }
  to   { width: 100%; }
}

/* ─── Reveal stagger on scroll ─── */
.scroll-reveal-list .item {
  opacity: 0;
  translate: 0 30px;
}

.scroll-reveal-list .item {
  animation: reveal-item linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 40%;
  animation-delay: calc(var(--i, 0) * 100ms);
}

@keyframes reveal-item {
  to { opacity: 1; translate: 0 0; }
}
```

---

## 112. ADVANCED CSS COLOR SYSTEM

### 112.1 Dynamic Palette Generation

```css
/* ─── Generate full palette from one brand color ─── */
@property --brand-h { syntax: '<number>'; initial-value: 250; inherits: true; }
@property --brand-c { syntax: '<number>'; initial-value: 0.2; inherits: true; }

:root {
  /* Set base hue and chroma */
  --brand-h: 250;
  --brand-c: 0.2;

  /* Auto-generate 10-step palette */
  --brand-50:  oklch(0.97 calc(var(--brand-c) * 0.15) var(--brand-h));
  --brand-100: oklch(0.94 calc(var(--brand-c) * 0.25) var(--brand-h));
  --brand-200: oklch(0.89 calc(var(--brand-c) * 0.40) var(--brand-h));
  --brand-300: oklch(0.82 calc(var(--brand-c) * 0.60) var(--brand-h));
  --brand-400: oklch(0.74 calc(var(--brand-c) * 0.80) var(--brand-h));
  --brand-500: oklch(0.63 var(--brand-c) var(--brand-h));
  --brand-600: oklch(0.54 var(--brand-c) var(--brand-h));
  --brand-700: oklch(0.45 var(--brand-c) var(--brand-h));
  --brand-800: oklch(0.36 calc(var(--brand-c) * 0.9) var(--brand-h));
  --brand-900: oklch(0.27 calc(var(--brand-c) * 0.8) var(--brand-h));
  --brand-950: oklch(0.18 calc(var(--brand-c) * 0.6) var(--brand-h));
}

/* Change entire palette by changing 2 variables */
[data-brand="emerald"] {
  --brand-h: 155;
  --brand-c: 0.18;
}

[data-brand="rose"] {
  --brand-h: 10;
  --brand-c: 0.25;
}

[data-brand="amber"] {
  --brand-h: 65;
  --brand-c: 0.22;
}

/* ─── Automatic semantic tokens from palette ─── */
:root {
  --color-accent:          var(--brand-500);
  --color-accent-hover:    var(--brand-600);
  --color-accent-light:    var(--brand-100);
  --color-accent-dark:     var(--brand-800);
  --color-accent-subtle:   var(--brand-50);
  --color-accent-contrast: var(--brand-950);
}

/* ─── APCA contrast checking via CSS (approximation) ─── */
/*
  APCA Lc values for text:
  Lc >= 75: body text
  Lc >= 60: large text / UI
  Lc >= 45: placeholder, disabled

  Use oklch() lightness difference as approximation:
  High contrast: L(bg) - L(text) > 0.5
  Medium:        L(bg) - L(text) > 0.35
*/

/* ─── Adaptive color based on background ─── */
.adaptive-text {
  /* Light-dark based on container */
  color: light-dark(
    oklch(0.2 0 0),    /* dark text on light bg */
    oklch(0.95 0 0)    /* light text on dark bg */
  );
}

/* For dynamic backgrounds, use contrast-color (future spec) */
/* color: contrast-color(var(--bg) vs oklch(0.2 0 0), oklch(0.95 0 0)); */
```

---

## 113. CSS TRANSITIONS — COMPLETE COOKBOOK

### 113.1 Every Useful Transition Pattern

```css
/* ─── Height: 0 → auto (the holy grail) ─── */
/* Modern: with interpolate-size */
:root { interpolate-size: allow-keywords; }
.expandable {
  height: 0;
  overflow: hidden;
  transition: height 0.3s var(--ease-out);
}
.expandable.open { height: auto; }

/* Legacy: max-height trick */
.expandable-legacy {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s var(--ease-out);
}
.expandable-legacy.open {
  max-height: 1000px;  /* must exceed content height */
  transition-timing-function: var(--ease-in);  /* prevents overshoot feel */
}

/* ─── Smooth appear/disappear with display ─── */
.appear {
  opacity: 0;
  translate: 0 8px;
  display: none;
  transition:
    opacity   0.2s var(--ease-out),
    translate 0.2s var(--ease-out),
    display   0.2s allow-discrete,
    overlay   0.2s allow-discrete;
}

.appear.visible {
  opacity: 1;
  translate: 0 0;
  display: block;
}

@starting-style {
  .appear.visible {
    opacity: 0;
    translate: 0 8px;
  }
}

/* ─── Smooth theme transition ─── */
/* Only apply during theme toggle, not on load */
html.theme-transitioning * {
  transition:
    background-color 0.3s !important,
    border-color     0.2s !important,
    color            0.2s !important,
    box-shadow       0.3s !important;
}
/* JS: document.documentElement.classList.add('theme-transitioning')
   → change theme → setTimeout remove class */

/* ─── Transition only on user interaction (not on load) ─── */
.card {
  /* No transition initially */
}

.user-has-interacted .card {
  transition: box-shadow var(--duration-normal) var(--ease-out);
}
/* JS: document.addEventListener('pointerdown', () => body.classList.add('user-has-interacted')) */

/* ─── Staggered list transitions ─── */
.list-item {
  transition:
    opacity   0.3s var(--ease-out) calc(var(--index, 0) * 50ms),
    translate 0.3s var(--ease-out) calc(var(--index, 0) * 50ms);
}

.list-item.entering  { opacity: 0; translate: 0 10px; }
.list-item.visible   { opacity: 1; translate: 0 0; }
.list-item.exiting   { opacity: 0; translate: 0 -10px; }
```

---

## 114. CSS ARCHITECTURE DECISION RECORDS (ADR)

```css
/*
 * ADR-001: Use CSS Custom Properties for ALL design tokens
 * STATUS: Accepted
 * CONTEXT: Need theming, easy override, component isolation
 * DECISION: All values in :root as --token-name, never hardcode
 * CONSEQUENCES: + theming, + isolation, - IE11 (dropped)
 *
 * ADR-002: Use @layer for specificity management
 * STATUS: Accepted
 * DECISION: @layer reset, base, layout, components, utilities, overrides
 * CONSEQUENCES: + predictable specificity, + no !important wars
 *
 * ADR-003: Mobile-first breakpoints
 * STATUS: Accepted
 * DECISION: min-width queries, 0/640/768/1024/1280/1536 scale
 * CONSEQUENCES: + smaller default CSS, + progressive enhancement
 *
 * ADR-004: Logical properties everywhere
 * STATUS: Accepted (with exceptions for purely decorative)
 * DECISION: margin-inline, padding-block, inset-inline-start etc
 * CONSEQUENCES: + RTL support free, - slightly more verbose
 *
 * ADR-005: BEM naming within @scope or CSS modules
 * STATUS: Accepted
 * DECISION: .component__element--modifier at component level
 * CONSEQUENCES: + readable, + explicit, - verbose
 *
 * ADR-006: No ID selectors in authored CSS
 * STATUS: Accepted
 * DECISION: Use classes only. IDs for JS/anchor only.
 * CONSEQUENCES: + reusable, + lower specificity
 *
 * ADR-007: clamp() for all fluid values
 * STATUS: Accepted
 * DECISION: clamp(min, preferred, max) for font-size/spacing
 * CONSEQUENCES: + fewer breakpoints, + fluid UX
 *
 * ADR-008: oklch() for new color definitions
 * STATUS: Accepted
 * DECISION: New colors in oklch(), legacy in hex for compatibility
 * CONSEQUENCES: + perceptual uniformity, + easy tinting
 *
 * ADR-009: CSS Nesting (native, not preprocessor)
 * STATUS: Accepted (progressive enhancement)
 * DECISION: Native @nesting, PostCSS as fallback if needed
 * CONSEQUENCES: + co-located, - older browser support
 *
 * ADR-010: Container queries for component responsiveness
 * STATUS: Accepted
 * DECISION: component-level container-type, not just viewport
 * CONSEQUENCES: + true component-driven design
 */
```

---

## 115. COMPLETE VISUAL DEBUGGING KIT

```css
/* ─── Add to <head> temporarily for debugging ─── */
/* <link rel="stylesheet" href="debug.css"> */

/* Highlight different element types */
.debug-layout article  { outline: 2px solid oklch(0.7 0.25 0); }
.debug-layout section  { outline: 2px solid oklch(0.7 0.25 120); }
.debug-layout aside    { outline: 2px solid oklch(0.7 0.25 240); }
.debug-layout div      { outline: 1px solid oklch(0.7 0.1 0 / 0.3); }
.debug-layout p        { outline: 1px solid oklch(0.7 0.1 120 / 0.3); }
.debug-layout span     { outline: 1px dashed oklch(0.7 0.1 240 / 0.5); }

/* Show all text as visual blocks */
.debug-text * {
  color: transparent !important;
  background: var(--color-bg-muted) !important;
  border-radius: 2px !important;
}

/* Show all images as colored boxes */
.debug-img img {
  filter: hue-rotate(90deg) !important;
  opacity: 0.5 !important;
}

/* Show overflow issues */
.debug-overflow * {
  overflow: visible !important;
  max-width: none !important;
}

/* Highlight elements with inline styles */
.debug-inline [style] {
  outline: 3px solid red !important;
}

/* Highlight bad practices */
.debug-bad *[width][height] {
  outline: 3px solid orange;  /* should use CSS for sizing */
}
.debug-bad img:not([alt]) {
  outline: 3px solid red;  /* missing alt */
  filter: brightness(0.3) sepia(1) hue-rotate(330deg);
}
.debug-bad a:not([href]) {
  outline: 3px solid red;
}
.debug-bad button:not([type]) {
  outline: 2px dashed orange;
}
.debug-bad input:not([id]):not([aria-label]):not([aria-labelledby]) {
  outline: 3px solid red;
}

/* Grid overlay */
.debug-grid::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 99999;
  background:
    repeating-linear-gradient(
      to right,
      oklch(0.6 0.25 250 / 0.07) 0,
      oklch(0.6 0.25 250 / 0.07) 1px,
      transparent 1px,
      transparent calc(100% / 12)
    );
}

/* Typography rhythm overlay */
.debug-rhythm::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 99998;
  background: repeating-linear-gradient(
    to bottom,
    oklch(0.7 0.15 40 / 0.1) 0,
    oklch(0.7 0.15 40 / 0.1) 1px,
    transparent 1px,
    transparent 1.5rem  /* matches line-height */
  );
}

/* Show z-index values */
.debug-zindex * {
  position: relative;
}
.debug-zindex *::before {
  content: attr(style);
  position: absolute;
  top: 0;
  left: 0;
  font-size: 10px;
  background: red;
  color: white;
  padding: 1px 3px;
  pointer-events: none;
  z-index: 9999;
  font-family: monospace;
}
```

---

## 116. CSS SNIPPETS — FINAL COLLECTION

### 116.1 The Useful 30

```css
/* 1. Perfect circle image */
.avatar { border-radius: 50%; aspect-ratio: 1; object-fit: cover; }

/* 2. Truncate text (1 line) */
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* 3. Clamp text (N lines) */
.clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

/* 4. Center absolutely anything */
.abs-center { position: absolute; inset: 0; margin: auto; width: fit-content; height: fit-content; }

/* 5. Full viewport section */
.full-page { min-height: 100dvh; }

/* 6. Sticky footer */
body { display: flex; flex-direction: column; min-height: 100dvh; }
main { flex: 1; }

/* 7. Responsive fluid container */
.container { max-inline-size: min(100% - 2rem, 72rem); margin-inline: auto; }

/* 8. Aspect ratio box */
.ratio-16-9 { aspect-ratio: 16 / 9; overflow: hidden; }

/* 9. Visually hidden (accessible) */
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }

/* 10. Smooth scroll */
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion) { html { scroll-behavior: auto; } }

/* 11. No FOUC for images */
img { display: block; max-width: 100%; height: auto; }

/* 12. Better box sizing */
*, *::before, *::after { box-sizing: border-box; }

/* 13. Remove default button */
button { appearance: none; border: none; background: none; cursor: pointer; font: inherit; }

/* 14. CSS reset for lists */
ul, ol { list-style: none; padding: 0; margin: 0; }

/* 15. Fluid typography */
.fluid-text { font-size: clamp(1rem, 2vw + 0.5rem, 1.5rem); }

/* 16. Glass morphism */
.glass { background: rgb(255 255 255 / 0.1); backdrop-filter: blur(10px); border: 1px solid rgb(255 255 255 / 0.2); }

/* 17. Gradient text */
.gradient-text { background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; background-clip: text; color: transparent; }

/* 18. Skeleton loading */
.skeleton { background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 4px; }
@keyframes shimmer { from { background-position: -200% 0; } to { background-position: 200% 0; } }

/* 19. Focus ring */
:focus-visible { outline: 2px solid var(--color-accent, currentColor); outline-offset: 2px; }

/* 20. Disabled state */
:disabled, [aria-disabled="true"] { opacity: 0.5; cursor: not-allowed; pointer-events: none; }

/* 21. Scrollbar gutter stability */
html { scrollbar-gutter: stable; }

/* 22. Prevent layout shift from scrollbar */
body { overflow-y: scroll; }

/* 23. Text balance on headings */
h1, h2, h3 { text-wrap: balance; }
p { text-wrap: pretty; }

/* 24. Print: show URLs */
@media print { a[href]::after { content: ' (' attr(href) ')'; } }

/* 25. High-DPI images */
@media (-webkit-min-device-pixel-ratio: 2) { .logo { background-image: url('logo@2x.png'); background-size: 100px 50px; } }

/* 26. iOS form zoom fix */
input, select, textarea { font-size: max(16px, 1em); }

/* 27. Custom checkbox reset to style */
input[type="checkbox"] { appearance: none; -webkit-appearance: none; }

/* 28. Better default transition */
.interactive { transition: background-color var(--t, 0.15s), color var(--t, 0.15s), border-color var(--t, 0.15s), opacity var(--t, 0.15s), transform var(--t, 0.15s); }

/* 29. Safe area padding */
.safe { padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left); }

/* 30. The universal overlay */
.overlay { position: absolute; inset: 0; background: var(--overlay-color, rgb(0 0 0 / 0.5)); }
```

### 116.2 One-liner CSS Tricks

```css
/* Make page unselectable (kiosk mode) */
body { user-select: none; }

/* Force GPU acceleration */
.promoted { will-change: transform; transform: translateZ(0); }

/* Prevent image dragging */
img { -webkit-user-drag: none; user-drag: none; }

/* Smooth font on dark backgrounds */
.dark-bg { -webkit-font-smoothing: antialiased; }

/* Remove tap highlight on mobile */
* { -webkit-tap-highlight-color: transparent; }

/* Clickable everywhere in a link */
.card-link::after { content: ''; position: absolute; inset: 0; }
.card-link { position: relative; }

/* Respect user's system color scheme */
html { color-scheme: light dark; }

/* Prevent orphaned words in headings */
h1, h2 { text-wrap: balance; }

/* Ratio-aware padding hack (legacy) */
.aspect-box::before { content: ''; display: block; padding-top: 56.25%; }

/* Disable all animations (debug) */
* { animation: none !important; transition: none !important; }

/* Make <details> not show triangle */
summary { list-style: none; }
summary::-webkit-details-marker { display: none; }

/* Force hardware rendering for videos */
video { transform: translateZ(0); }

/* Prevent white flash on image load */
img { background: var(--color-bg-subtle); }
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║            PARTS I–VI: COMPLETE CSS MASTER REFERENCE                 ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  116 chapters · 600+ code examples · ~22,000 lines                  ║
║                                                                      ║
║  NEW IN PART VI:                                                     ║
║  ✅ Hover effects library (image, button, text — 15 effects)         ║
║  ✅ Border animations (spinning, draw, corners, marching ants)       ║
║  ✅ Before/After comparison slider                                   ║
║  ✅ Kanban board (full drag-drop states)                             ║
║  ✅ Terminal / Console UI (syntax highlighting, progress)            ║
║  ✅ Audio player + Video player (custom controls)                    ║
║  ✅ Notification center (panel, items, bell, unread)                 ║
║  ✅ Invoice layout + Resume/CV layout                                ║
║  ✅ CSS Counters advanced (legal, footnotes, figures)                ║
║  ✅ Magazine & Newsletter layouts                                    ║
║  ✅ Drag-and-drop visual feedback                                    ║
║  ✅ Swipe card deck (Tinder-style)                                  ║
║  ✅ Scroll-linked parallax + sticky sections                         ║
║  ✅ Dynamic palette generation from one variable                     ║
║  ✅ Transition cookbook (height:auto, display, stagger)              ║
║  ✅ CSS Architecture Decision Records (ADR)                          ║
║  ✅ Visual debugging kit (30+ debug utilities)                       ║
║  ✅ Final snippets collection (60 one-liners and utilities)          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```
