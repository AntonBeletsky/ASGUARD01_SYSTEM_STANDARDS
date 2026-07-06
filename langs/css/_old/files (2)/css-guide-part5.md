# PART V — CSS COMPLETE: REMAINING PATTERNS & DEEP CUTS

---

## 91. CSS BACKGROUND PATTERNS LIBRARY

### 91.1 Pure CSS Geometric Patterns

```css
/* ─── 1. Checkerboard ─── */
.pattern-checkerboard {
  background-color: #e8e8e8;
  background-image:
    conic-gradient(#ccc 90deg, transparent 90deg);
  background-size: 24px 24px;
}

/* ─── 2. Polka dots ─── */
.pattern-dots {
  background-color: #f8f8f8;
  background-image:
    radial-gradient(circle, #d0d0d0 1.5px, transparent 1.5px);
  background-size: 20px 20px;
}

/* ─── 3. Grid lines ─── */
.pattern-grid {
  background-color: #fff;
  background-image:
    linear-gradient(var(--color-border) 1px, transparent 1px),
    linear-gradient(to right, var(--color-border) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* ─── 4. Diagonal stripes ─── */
.pattern-stripes {
  background-image: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 8px,
    rgba(0 0 0 / 0.05) 8px,
    rgba(0 0 0 / 0.05) 16px
  );
}

/* ─── 5. Diagonal grid ─── */
.pattern-diagonal-grid {
  background-image:
    repeating-linear-gradient(45deg, #e0e0e0 0, #e0e0e0 1px, transparent 0, transparent 50%),
    repeating-linear-gradient(-45deg, #e0e0e0 0, #e0e0e0 1px, transparent 0, transparent 50%);
  background-size: 16px 16px;
  background-color: #fff;
}

/* ─── 6. Honeycomb (hexagonal) ─── */
.pattern-hex {
  background-color: #f5f5f5;
  background-image:
    radial-gradient(circle farthest-side at 0% 50%, #fbfbfb 23.5%, rgba(240,166,17,0) 0) 21px 30px,
    radial-gradient(circle farthest-side at 0% 50%, #d9d9d9 24%, rgba(240,166,17,0) 0) 19px 30px,
    linear-gradient(#fbfbfb 14%, rgba(240,166,17,0) 0, rgba(240,166,17,0) 85%, #fbfbfb 0) 0 0,
    linear-gradient(150deg, #fbfbfb 24%, #d9d9d9 0, #d9d9d9 26%, rgba(240,166,17,0) 0, rgba(240,166,17,0) 74%, #d9d9d9 0, #d9d9d9 76%, #fbfbfb 0) 0 0,
    linear-gradient(30deg, #fbfbfb 24%, #d9d9d9 0, #d9d9d9 26%, rgba(240,166,17,0) 0, rgba(240,166,17,0) 74%, #d9d9d9 0, #d9d9d9 76%, #fbfbfb 0) 0 0;
  background-size: 40px 60px;
}

/* ─── 7. Triangles ─── */
.pattern-triangles {
  background-color: #f0f0f0;
  background-image:
    linear-gradient(60deg, #e0e0e0 25%, transparent 25%),
    linear-gradient(-60deg, #e0e0e0 25%, transparent 25%),
    linear-gradient(60deg, transparent 75%, #e0e0e0 75%),
    linear-gradient(-60deg, transparent 75%, #e0e0e0 75%);
  background-size: 20px 35px;
  background-position: 0 0, 0 0, 10px 18px, 10px 18px;
}

/* ─── 8. Carbon fiber ─── */
.pattern-carbon {
  background-color: #1a1a1a;
  background-image:
    linear-gradient(27deg, #151515 5px, transparent 5px) 0 5px,
    linear-gradient(207deg, #151515 5px, transparent 5px) 10px 0px,
    linear-gradient(27deg, #222 5px, transparent 5px) 0px 10px,
    linear-gradient(207deg, #222 5px, transparent 5px) 10px 5px,
    linear-gradient(90deg, #1b1b1b 10px, transparent 10px),
    linear-gradient(#1d1d1d 25%, #1a1a1a 25%, #1a1a1a 50%, transparent 50%,
      transparent 75%, #242424 75%, #242424);
  background-size: 20px 20px;
}

/* ─── 9. Blueprint ─── */
.pattern-blueprint {
  background-color: #1a2d5a;
  background-image:
    linear-gradient(rgba(255 255 255 / 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255 255 255 / 0.07) 1px, transparent 1px),
    linear-gradient(rgba(255 255 255 / 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255 255 255 / 0.04) 1px, transparent 1px);
  background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
  background-position: -2px -2px, -2px -2px, -1px -1px, -1px -1px;
}

/* ─── 10. Noise texture (CSS only) ─── */
.pattern-noise {
  position: relative;
}
.pattern-noise::before {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.05;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 256px 256px;
  pointer-events: none;
}

/* ─── 11. Animated gradient mesh ─── */
.pattern-animated-mesh {
  background-color: #0f0f1a;
}
.pattern-animated-mesh::before {
  content: '';
  position: absolute;
  inset: -100%;
  background:
    radial-gradient(ellipse at 20% 50%, oklch(0.5 0.25 280 / 0.4) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, oklch(0.5 0.2 200 / 0.3) 0%, transparent 55%),
    radial-gradient(ellipse at 60% 80%, oklch(0.5 0.22 320 / 0.35) 0%, transparent 50%);
  filter: blur(40px);
  animation: mesh-float 12s ease-in-out infinite alternate;
}

@keyframes mesh-float {
  0%   { transform: translate(0%, 0%) scale(1); }
  33%  { transform: translate(3%, -4%) scale(1.05); }
  66%  { transform: translate(-2%, 5%) scale(0.97); }
  100% { transform: translate(4%, -2%) scale(1.03); }
}
```

### 91.2 SVG-based CSS Patterns

```css
/* ─── Circuit board pattern ─── */
.pattern-circuit {
  background-color: #0d1b2a;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Cg fill='none' stroke='%231a3a5c' stroke-width='1'%3E%3Cpath d='M10 10 L10 50 L50 50'/%3E%3Cpath d='M50 10 L50 30 L90 30 L90 90'/%3E%3Cpath d='M30 60 L30 90 L70 90'/%3E%3C/g%3E%3Ccircle cx='10' cy='10' r='3' fill='%231a3a5c'/%3E%3Ccircle cx='50' cy='50' r='3' fill='%231a3a5c'/%3E%3Ccircle cx='90' cy='30' r='3' fill='%231a3a5c'/%3E%3C/svg%3E");
}

/* ─── Topographic map ─── */
.pattern-topo {
  background-color: #f0f4e8;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cpath d='M20 100 Q60 20 100 100 Q140 180 180 100' fill='none' stroke='%23b8cc8a' stroke-width='1.5' opacity='0.6'/%3E%3Cpath d='M0 120 Q40 40 80 120 Q120 200 160 120 Q180 80 200 120' fill='none' stroke='%23b8cc8a' stroke-width='1.5' opacity='0.4'/%3E%3C/svg%3E");
}
```

---

## 92. CSS 3D EFFECTS — ADVANCED

### 92.1 3D Card Scenes

```css
/* ─── 3D Product showcase ─── */
.scene-3d {
  perspective: 1200px;
  perspective-origin: 50% 50%;
}

.card-3d-showcase {
  transform-style: preserve-3d;
  transform: rotateX(var(--rx, 0deg)) rotateY(var(--ry, 0deg));
  transition: transform 0.1s ease-out;
  width: 300px;
  height: 400px;
  position: relative;
}

/* JS updates --rx and --ry on mousemove */

/* Faces */
.face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.face-front  { transform: translateZ(20px); }
.face-back   { transform: rotateY(180deg) translateZ(20px); }
.face-top    {
  height: 20px;
  top: -20px;
  left: 0;
  right: 0;
  transform: rotateX(90deg);
  transform-origin: bottom;
}
.face-bottom {
  height: 20px;
  bottom: -20px;
  left: 0;
  right: 0;
  transform: rotateX(-90deg);
  transform-origin: top;
}
.face-left {
  width: 20px;
  left: -20px;
  top: 0;
  bottom: 0;
  transform: rotateY(-90deg);
  transform-origin: right;
}
.face-right {
  width: 20px;
  right: -20px;
  top: 0;
  bottom: 0;
  transform: rotateY(90deg);
  transform-origin: left;
}

/* ─── Layered 3D card (depth illusion) ─── */
.depth-card {
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.4s var(--ease-out);
}

.depth-card:hover {
  transform: translateY(-4px);
}

/* Each layer offset in Z */
.depth-card__layer {
  position: absolute;
  inset: 0;
  border-radius: inherit;
}

.depth-card__layer--3 { transform: translateZ(-3px); background: oklch(0.6 0.15 250 / 0.6); }
.depth-card__layer--2 { transform: translateZ(-6px); background: oklch(0.5 0.15 250 / 0.4); }
.depth-card__layer--1 { transform: translateZ(-9px); background: oklch(0.4 0.15 250 / 0.2); }

/* ─── CSS Cube ─── */
.cube-container {
  perspective: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cube {
  --size: 100px;
  width: var(--size);
  height: var(--size);
  transform-style: preserve-3d;
  animation: cube-rotate 8s linear infinite;
}

@keyframes cube-rotate {
  from { transform: rotateX(-20deg) rotateY(0deg); }
  to   { transform: rotateX(-20deg) rotateY(360deg); }
}

.cube__face {
  position: absolute;
  width: var(--size);
  height: var(--size);
  border: 2px solid oklch(0.7 0.2 250 / 0.6);
  background: oklch(0.5 0.2 250 / 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  backface-visibility: visible;
}

.cube__face--front  { transform: translateZ(calc(var(--size) / 2)); }
.cube__face--back   { transform: rotateY(180deg) translateZ(calc(var(--size) / 2)); }
.cube__face--right  { transform: rotateY(90deg) translateZ(calc(var(--size) / 2)); }
.cube__face--left   { transform: rotateY(-90deg) translateZ(calc(var(--size) / 2)); }
.cube__face--top    { transform: rotateX(90deg) translateZ(calc(var(--size) / 2)); }
.cube__face--bottom { transform: rotateX(-90deg) translateZ(calc(var(--size) / 2)); }
```

### 92.2 3D Typography

```css
/* ─── 3D extruded text ─── */
.text-3d-extrude {
  font-size: clamp(3rem, 8vw, 8rem);
  font-weight: var(--font-weight-black);
  color: var(--color-accent);
  text-shadow:
    1px  1px 0 oklch(from var(--color-accent) calc(l - 0.1) c h),
    2px  2px 0 oklch(from var(--color-accent) calc(l - 0.15) c h),
    3px  3px 0 oklch(from var(--color-accent) calc(l - 0.2) c h),
    4px  4px 0 oklch(from var(--color-accent) calc(l - 0.25) c h),
    5px  5px 0 oklch(from var(--color-accent) calc(l - 0.3) c h),
    6px  6px 0 oklch(from var(--color-accent) calc(l - 0.35) c h),
    7px  7px 8px rgb(0 0 0 / 0.4);
}

/* ─── Letterpress / inset text ─── */
.text-letterpress {
  color: transparent;
  background: linear-gradient(to bottom, #555, #333);
  -webkit-background-clip: text;
  background-clip: text;
  text-shadow:
    0 1px 1px rgba(255 255 255 / 0.2),
    0 -1px 1px rgba(0 0 0 / 0.5);
}

/* ─── Retro chrome text ─── */
.text-chrome {
  background: linear-gradient(
    180deg,
    #fff  0%,
    #bbb 25%,
    #fff 45%,
    #888 65%,
    #ddd 80%,
    #fff 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  filter: drop-shadow(1px 2px 4px rgb(0 0 0 / 0.5));
}

/* ─── Animated holographic text ─── */
@keyframes holo-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.text-holographic {
  background: linear-gradient(
    135deg,
    oklch(0.8 0.3 0),
    oklch(0.8 0.3 60),
    oklch(0.8 0.3 120),
    oklch(0.8 0.3 180),
    oklch(0.8 0.3 240),
    oklch(0.8 0.3 300),
    oklch(0.8 0.3 360)
  );
  background-size: 300% 300%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: holo-shift 4s ease infinite;
}
```

---

## 93. ECOMMERCE UI PATTERNS

### 93.1 Product Card

```css
/* ─── Product card ─── */
.product-card {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition:
    box-shadow var(--duration-normal) var(--ease-out),
    translate  var(--duration-normal) var(--ease-out);
  position: relative;
}

.product-card:hover {
  box-shadow: var(--shadow-xl);
  translate: 0 -3px;
}

/* Image area */
.product-card__media {
  position: relative;
  aspect-ratio: 1;
  background: var(--color-bg-subtle);
  overflow: hidden;
}

.product-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: scale var(--duration-slow) var(--ease-out);
}

.product-card:hover .product-card__img { scale: 1.05; }

/* Quick actions overlay */
.product-card__actions {
  position: absolute;
  inset-block-end: 0;
  inset-inline: 0;
  padding: var(--space-3);
  background: linear-gradient(to top, rgb(0 0 0 / 0.5), transparent);
  display: flex;
  gap: var(--space-2);
  justify-content: center;
  translate: 0 100%;
  opacity: 0;
  transition:
    translate var(--duration-normal) var(--ease-out),
    opacity   var(--duration-normal);
}

.product-card:hover .product-card__actions {
  translate: 0 0;
  opacity: 1;
}

/* Badges */
.product-card__badge {
  position: absolute;
  inset-block-start: var(--space-3);
  inset-inline-start: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  z-index: 1;
}

.product-badge {
  display: inline-flex;
  padding: 0.2em 0.6em;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  border-radius: var(--radius-sm);
  line-height: 1.5;
}

.product-badge--new    { background: var(--color-accent); color: white; }
.product-badge--sale   { background: var(--color-danger-500); color: white; }
.product-badge--hot    { background: var(--color-warning-500); color: #111; }
.product-badge--sold   { background: var(--color-neutral-700); color: white; }

/* Wishlist button */
.product-card__wishlist {
  position: absolute;
  inset-block-start: var(--space-3);
  inset-inline-end: var(--space-3);
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--color-surface);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
  transition: scale var(--duration-fast) var(--ease-bounce);
  z-index: 1;
}

.product-card__wishlist:hover { scale: 1.1; }
.product-card__wishlist[aria-pressed="true"] { color: var(--color-danger-500); }

/* Info area */
.product-card__body {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  flex: 1;
}

.product-card__category {
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  font-weight: var(--font-weight-medium);
}

.product-card__name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Rating */
.product-card__rating {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* Price */
.product-card__price {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
  flex-wrap: wrap;
  margin-block-start: auto;
}

.price-current {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
}

.price-original {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  text-decoration: line-through;
  font-variant-numeric: tabular-nums;
}

.price-discount {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  color: var(--color-danger-500);
  background: var(--color-danger-100);
  padding: 0.125em 0.4em;
  border-radius: var(--radius-sm);
}

/* ─── Product grid ─── */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr));
  gap: var(--space-4);
}
```

### 93.2 Shopping Cart & Checkout

```css
/* ─── Cart item ─── */
.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto;
  gap: var(--space-4);
  align-items: start;
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--color-border);
  animation: cart-item-in 0.3s var(--ease-out);
}

@keyframes cart-item-in {
  from { opacity: 0; translate: 0 -8px; }
}

.cart-item.removing {
  animation: cart-item-out 0.25s var(--ease-in) forwards;
}

@keyframes cart-item-out {
  to { opacity: 0; height: 0; padding: 0; overflow: hidden; }
}

.cart-item__image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: var(--radius-md);
  background: var(--color-bg-subtle);
}

.cart-item__name {
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-sm);
}

.cart-item__meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  margin-top: var(--space-1);
}

/* Quantity stepper */
.quantity-stepper {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.quantity-stepper__btn {
  width: 2rem;
  height: 2rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1.125rem;
  color: var(--color-text);
  transition: background var(--duration-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.quantity-stepper__btn:hover { background: var(--color-bg-subtle); }
.quantity-stepper__btn:disabled { opacity: 0.4; cursor: not-allowed; }

.quantity-stepper__value {
  min-width: 2.5rem;
  text-align: center;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  font-variant-numeric: tabular-nums;
  border: none;
  outline: none;
  background: none;
}

/* ─── Order summary ─── */
.order-summary {
  background: var(--color-bg-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  border: 1px solid var(--color-border);
}

.order-line {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding-block: var(--space-2);
  font-size: var(--font-size-sm);
}

.order-line + .order-line { border-top: 1px solid var(--color-border); }

.order-line--total {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-base);
  padding-block-start: var(--space-4);
  border-top: 2px solid var(--color-border);
  margin-block-start: var(--space-2);
}

.order-line__value { font-variant-numeric: tabular-nums; }

/* ─── Checkout steps ─── */
.checkout-progress {
  display: flex;
  align-items: center;
}

.checkout-step {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex: 1;
  position: relative;
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

.checkout-step:not(:last-child)::after {
  content: '';
  flex: 1;
  height: 2px;
  background: var(--color-border);
  margin-inline-start: var(--space-2);
}

.checkout-step.completed::after { background: var(--color-accent); }

.checkout-step__num {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 2px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
  background: var(--color-surface);
  transition:
    background var(--duration-fast),
    border-color var(--duration-fast),
    color var(--duration-fast);
}

.checkout-step.active .checkout-step__num {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.checkout-step.completed .checkout-step__num {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: white;
}

/* ─── Payment card input ─── */
.payment-card {
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  border-radius: var(--radius-2xl);
  padding: var(--space-6);
  color: white;
  font-family: var(--font-mono);
  position: relative;
  overflow: hidden;
  aspect-ratio: 1.586;
  max-width: 380px;
}

.payment-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 40%, rgba(255 255 255 / 0.05) 100%);
}

.payment-card__chip {
  width: 2.5rem;
  height: 2rem;
  background: linear-gradient(135deg, #d4af37, #b8942a);
  border-radius: 6px;
  margin-block-end: var(--space-6);
}

.payment-card__number {
  font-size: clamp(1rem, 3vw, 1.25rem);
  letter-spacing: 0.15em;
  margin-block-end: var(--space-4);
}

.payment-card__meta {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  opacity: 0.7;
  margin-block-end: var(--space-2);
}

.payment-card__name {
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.payment-card__logo {
  position: absolute;
  inset-block-end: var(--space-5);
  inset-inline-end: var(--space-5);
  width: 3rem;
  opacity: 0.8;
}
```

### 93.3 Star Rating

```css
/* ─── CSS-only interactive star rating ─── */
.star-rating {
  display: flex;
  flex-direction: row-reverse;  /* reverse for :checked ~ sibling trick */
  gap: 0.125rem;
  width: fit-content;
}

.star-rating input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.star-rating label {
  font-size: 1.5rem;
  color: var(--color-border-strong);
  cursor: pointer;
  transition: color var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);
  line-height: 1;
}

/* Highlight on hover — all stars before (visually after in RTL flex) */
.star-rating label:hover,
.star-rating label:hover ~ label {
  color: var(--color-warning-500);
  scale: 1.1;
}

/* Highlight checked and before */
.star-rating input:checked ~ label {
  color: var(--color-warning-500);
}

/* ─── Read-only star display ─── */
.stars-display {
  display: inline-flex;
  gap: 1px;
  color: var(--color-border);
  font-size: 1rem;
  position: relative;
}

/* Filled stars via clip */
.stars-display::before {
  content: '★★★★★';
  position: absolute;
  inset: 0;
  color: var(--color-warning-500);
  overflow: hidden;
  width: calc(var(--rating, 0) / 5 * 100%);
  white-space: nowrap;
}

.stars-display::after {
  content: '★★★★★';
}

/* ─── Rating with count ─── */
.rating-summary {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.rating-average {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-black);
  font-variant-numeric: tabular-nums;
  line-height: 1;
}

.rating-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

/* Rating bars breakdown */
.rating-bars {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  flex: 1;
}

.rating-bar-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.rating-bar {
  flex: 1;
  height: 6px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.rating-bar__fill {
  height: 100%;
  background: var(--color-warning-500);
  border-radius: inherit;
  width: var(--pct, 0%);
  transition: width 0.6s var(--ease-out);
}
```

### 93.4 Pagination

```css
/* ─── Pagination ─── */
.pagination {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  flex-wrap: wrap;
}

.page-btn {
  min-width: 2.25rem;
  height: 2.25rem;
  padding-inline: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font: inherit;
  font-size: var(--font-size-sm);
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-1);
  transition:
    background      var(--duration-fast),
    border-color    var(--duration-fast),
    color           var(--duration-fast);
}

.page-btn:hover {
  background: var(--color-bg-subtle);
  border-color: var(--color-neutral-400);
}

.page-btn[aria-current="page"],
.page-btn.active {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: white;
  font-weight: var(--font-weight-semibold);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

.page-ellipsis {
  min-width: 2.25rem;
  height: 2.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  letter-spacing: 0.1em;
}

/* Compact pagination */
.pagination-compact {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--font-size-sm);
}

.pagination-compact__info {
  color: var(--color-text-muted);
  white-space: nowrap;
}

/* ─── Infinite scroll trigger ─── */
.load-more-trigger {
  display: flex;
  justify-content: center;
  padding: var(--space-8);
  visibility: hidden;  /* JS observes and shows */
}

.load-more-trigger[data-visible] {
  visibility: visible;
}
```

---

## 94. SOCIAL & CHAT UI PATTERNS

### 94.1 Chat Interface

```css
/* ─── Chat layout ─── */
.chat-layout {
  display: grid;
  grid-template-rows: auto 1fr auto;
  height: 100dvh;
  max-height: 700px;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  overflow: hidden;
}

/* Chat header */
.chat-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

.chat-header__avatar {
  position: relative;
  flex-shrink: 0;
}

.chat-header__avatar img {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
}

/* Online dot */
.chat-header__avatar::after {
  content: '';
  position: absolute;
  bottom: 1px;
  right: 1px;
  width: 10px;
  height: 10px;
  background: var(--color-success-500);
  border-radius: 50%;
  border: 2px solid var(--color-surface);
}

/* Messages area */
.chat-messages {
  overflow-y: auto;
  padding: var(--space-4) var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  overscroll-behavior: contain;
  scroll-behavior: smooth;
  scrollbar-width: thin;
}

/* Message bubble */
.message {
  display: flex;
  align-items: flex-end;
  gap: var(--space-2);
  max-width: 75%;
  animation: message-appear 0.2s var(--ease-out);
}

@keyframes message-appear {
  from { opacity: 0; translate: 0 8px; }
}

.message--outgoing {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message__avatar {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  align-self: flex-end;
}

.message__bubble {
  padding: 0.625rem 0.875rem;
  border-radius: var(--radius-xl);
  font-size: var(--font-size-sm);
  line-height: 1.5;
  position: relative;
  max-width: 100%;
  word-break: break-word;
}

/* Incoming */
.message--incoming .message__bubble {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-start-start-radius: var(--radius-sm);
  color: var(--color-text);
}

/* Outgoing */
.message--outgoing .message__bubble {
  background: var(--color-accent);
  border-start-end-radius: var(--radius-sm);
  color: white;
}

/* Message status */
.message__meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-subtle);
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding-block-end: 0.125rem;
}

.message--outgoing .message__meta {
  justify-content: flex-end;
}

/* Date separator */
.chat-date {
  text-align: center;
  font-size: var(--font-size-xs);
  color: var(--color-text-subtle);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-block: var(--space-2);
}

.chat-date::before,
.chat-date::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

/* Typing indicator in chat */
.typing-bubble {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.625rem 0.875rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  border-start-start-radius: var(--radius-sm);
  width: fit-content;
  animation: message-appear 0.2s var(--ease-out);
}

.typing-bubble span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-text-muted);
  animation: typing 1.4s ease-in-out infinite;
}
.typing-bubble span:nth-child(2) { animation-delay: 0.2s; }
.typing-bubble span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 60%, 100% { translate: 0; opacity: 0.4; }
  30%           { translate: 0 -4px; opacity: 1; }
}

/* Chat input */
.chat-input-area {
  padding: var(--space-4) var(--space-5);
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  display: flex;
  gap: var(--space-3);
  align-items: flex-end;
}

.chat-input {
  flex: 1;
  padding: 0.625rem 0.875rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  background: var(--color-bg-subtle);
  font: inherit;
  font-size: var(--font-size-sm);
  outline: none;
  resize: none;
  max-height: 120px;
  overflow-y: auto;
  line-height: 1.5;
  transition: border-color var(--duration-fast);
}

.chat-input:focus {
  border-color: var(--color-accent);
  background: var(--color-surface);
}
```

### 94.2 Social Feed

```css
/* ─── Social post card ─── */
.post {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.post__header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
}

.post__avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.post__author {
  flex: 1;
  min-width: 0;
}

.post__name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
}

.post__meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.post__menu {
  margin-inline-start: auto;
  color: var(--color-text-muted);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-md);
}

.post__content {
  padding: 0 var(--space-4) var(--space-4);
  font-size: var(--font-size-sm);
  line-height: 1.6;
}

.post__content a {
  color: var(--color-accent);
}

/* Hashtags */
.post__content .hashtag {
  color: var(--color-accent);
  cursor: pointer;
}

/* Media grid */
.post__media {
  display: grid;
  gap: 2px;
}

.post__media--1 { grid-template-columns: 1fr; }
.post__media--2 { grid-template-columns: 1fr 1fr; }
.post__media--3 {
  grid-template-columns: 2fr 1fr;
  grid-template-rows: 1fr 1fr;
}
.post__media--3 .media-item:first-child { grid-row: span 2; }
.post__media--4 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }

.media-item {
  aspect-ratio: 1;
  overflow: hidden;
  cursor: pointer;
  position: relative;
}

/* More overlay for 4+ images */
.media-item--more::after {
  content: '+' attr(data-count);
  position: absolute;
  inset: 0;
  background: rgb(0 0 0 / 0.5);
  color: white;
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  display: flex;
  align-items: center;
  justify-content: center;
}

.media-item img,
.media-item video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: scale var(--duration-slow) var(--ease-out);
}

.media-item:hover img { scale: 1.03; }

/* Post actions */
.post__actions {
  display: flex;
  padding: var(--space-2) var(--space-4);
  gap: var(--space-1);
  border-top: 1px solid var(--color-border);
}

.post-action {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: var(--space-2) var(--space-3);
  border: none;
  background: none;
  cursor: pointer;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
  font: inherit;
  border-radius: var(--radius-md);
  transition: background var(--duration-fast), color var(--duration-fast);
  flex: 1;
  justify-content: center;
}

.post-action:hover {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

.post-action--liked {
  color: var(--color-danger-500);
  animation: like-action 0.3s var(--ease-bounce);
}

@keyframes like-action {
  0%   { scale: 0.8; }
  60%  { scale: 1.2; }
  100% { scale: 1; }
}

/* Comment count animation */
.post-action__count {
  font-variant-numeric: tabular-nums;
  font-weight: var(--font-weight-medium);
}
```

---

## 95. CSS ANIMATION: PARTICLE & SPECIAL EFFECTS

### 95.1 CSS Confetti

```css
/* ─── CSS Confetti (via many pseudo-elements + JS class for each piece) ─── */
.confetti-piece {
  position: fixed;
  width: 10px;
  height: 10px;
  top: -10px;
  left: var(--x, 50%);
  background: var(--color, oklch(0.7 0.3 var(--hue, 0)));
  border-radius: var(--shape, 2px);
  animation:
    confetti-fall    var(--duration, 3s) var(--ease, ease-in) var(--delay, 0s) forwards,
    confetti-wobble  var(--wobble, 0.5s) ease-in-out infinite alternate;
  opacity: 0;
}

@keyframes confetti-fall {
  0%   { translate: 0 0; opacity: 1; rotate: 0deg; }
  100% { translate: var(--drift, 50px) 110dvh; opacity: 0; rotate: var(--spin, 360deg); }
}

@keyframes confetti-wobble {
  from { translate: -5px 0; }
  to   { translate: 5px 0; }
}

/* ─── CSS Sparkle effect ─── */
.sparkle {
  position: relative;
  display: inline-block;
}

.sparkle::before,
.sparkle::after {
  content: '✦';
  position: absolute;
  font-size: 0.5em;
  animation: sparkle-blink 1.5s ease-in-out infinite;
  color: var(--color-warning-400);
}

.sparkle::before {
  top: -0.5em;
  right: -0.5em;
  animation-delay: 0s;
}
.sparkle::after {
  bottom: -0.25em;
  left: -0.25em;
  animation-delay: 0.75s;
  font-size: 0.35em;
}

@keyframes sparkle-blink {
  0%, 100% { opacity: 0; scale: 0.5; }
  50%       { opacity: 1; scale: 1; }
}

/* ─── Firework burst ─── */
@keyframes firework-burst {
  0%   { width: 0; height: 0; opacity: 1; }
  100% { width: 200px; height: 200px; opacity: 0; margin: -100px; }
}

.firework {
  position: fixed;
  left: var(--x);
  top: var(--y);
  width: 4px;
  height: 4px;
  background: transparent;
  border-radius: 50%;
  box-shadow:
    0 0 0 2px var(--c1, oklch(0.8 0.3 0)),
    0 0 0 4px var(--c2, oklch(0.8 0.3 120)),
    0 0 0 6px var(--c3, oklch(0.8 0.3 240));
  animation: firework-burst 0.6s ease-out forwards;
}

/* ─── Glow pulse ─── */
@keyframes glow-pulse {
  0%, 100% {
    box-shadow:
      0 0 5px var(--glow-color),
      0 0 10px var(--glow-color),
      0 0 20px var(--glow-color);
  }
  50% {
    box-shadow:
      0 0 10px var(--glow-color),
      0 0 25px var(--glow-color),
      0 0 50px var(--glow-color);
  }
}

.glow-element {
  --glow-color: var(--color-accent);
  animation: glow-pulse 2s ease-in-out infinite;
}

/* ─── Matrix rain (CSS only, limited) ─── */
.matrix-column {
  position: absolute;
  top: -100%;
  font-family: monospace;
  color: #0f0;
  text-shadow: 0 0 8px #0f0;
  font-size: 14px;
  line-height: 1.4;
  animation: matrix-fall var(--duration, 3s) linear var(--delay, 0s) infinite;
  white-space: nowrap;
}

@keyframes matrix-fall {
  from { translate: 0 0; opacity: 0.8; }
  to   { translate: 0 200vh; opacity: 0; }
}
```

### 95.2 CSS Art Techniques

```css
/* ─── CSS-only illustrations (no images) ─── */

/* Sun */
.css-sun {
  --size: 80px;
  width: var(--size);
  height: var(--size);
  background: radial-gradient(circle, #FFD700 40%, #FF8C00 100%);
  border-radius: 50%;
  box-shadow:
    0 0 0 8px #FF8C00,
    0 0 0 12px rgba(255 200 0 / 0.3),
    /* Rays */
    0 -55px 0 -5px #FF8C00,
    55px 0 0 -5px #FF8C00,
    0 55px 0 -5px #FF8C00,
    -55px 0 0 -5px #FF8C00,
    40px -40px 0 -5px #FF8C00,
    40px 40px 0 -5px #FF8C00,
    -40px 40px 0 -5px #FF8C00,
    -40px -40px 0 -5px #FF8C00;
  animation: sun-rotate 10s linear infinite;
}

@keyframes sun-rotate {
  to { rotate: 360deg; }
}

/* Moon */
.css-moon {
  width: 80px;
  height: 80px;
  background: #f5e642;
  border-radius: 50%;
  box-shadow: inset -20px -5px 0 0 #d4b800;
}

/* Cloud */
.css-cloud {
  width: 120px;
  height: 50px;
  background: white;
  border-radius: 25px;
  position: relative;
  box-shadow: 0 4px 12px rgba(0 0 0 / 0.1);
}

.css-cloud::before {
  content: '';
  position: absolute;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
  top: -30px;
  left: 20px;
}

.css-cloud::after {
  content: '';
  position: absolute;
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 50%;
  top: -20px;
  left: 55px;
}

/* Heart */
.css-heart {
  --size: 60px;
  position: relative;
  width: var(--size);
  height: var(--size);
  background: #ff4d6d;
  transform: rotate(-45deg);
}
.css-heart::before,
.css-heart::after {
  content: '';
  position: absolute;
  width: var(--size);
  height: var(--size);
  background: inherit;
  border-radius: 50%;
}
.css-heart::before { top: calc(var(--size) * -0.5); left: 0; }
.css-heart::after  { top: 0; left: calc(var(--size) * 0.5); }

/* Loader as art: orbiting dots */
.orbit {
  --size: 60px;
  width: var(--size);
  height: var(--size);
  position: relative;
  animation: orbit-spin 2s linear infinite;
}

.orbit::before,
.orbit::after {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-accent);
}
.orbit::before { top: 0; left: 50%; translate: -50%; }
.orbit::after  { bottom: 0; left: 50%; translate: -50%; opacity: 0.5; }

@keyframes orbit-spin { to { rotate: 360deg; } }
```

---

## 96. DOCUMENTATION SITE PATTERNS

### 96.1 Table of Contents / Sidebar Nav

```css
/* ─── Docs layout ─── */
.docs-layout {
  display: grid;
  grid-template-columns: 260px 1fr 220px;
  gap: 0;
  min-height: 100dvh;
}

@media (max-width: 1024px) {
  .docs-layout {
    grid-template-columns: 240px 1fr;
  }
  .docs-toc { display: none; }
}

@media (max-width: 768px) {
  .docs-layout {
    grid-template-columns: 1fr;
  }
  .docs-sidebar { display: none; }
}

/* Left sidebar */
.docs-sidebar {
  border-right: 1px solid var(--color-border);
  padding: var(--space-6) var(--space-4);
  position: sticky;
  top: var(--header-height, 60px);
  height: calc(100dvh - var(--header-height, 60px));
  overflow-y: auto;
  scrollbar-width: thin;
}

.docs-sidebar-section {
  margin-block-end: var(--space-6);
}

.docs-sidebar-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  margin-block-end: var(--space-2);
  padding-inline: var(--space-3);
}

.docs-nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 0.375rem var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  text-decoration: none;
  transition: background var(--duration-fast), color var(--duration-fast);
  position: relative;
}

.docs-nav-link:hover {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

.docs-nav-link[aria-current="page"] {
  color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 8%, transparent);
  font-weight: var(--font-weight-medium);
}

/* Active left border */
.docs-nav-link[aria-current="page"]::before {
  content: '';
  position: absolute;
  inset-inline-start: 0;
  inset-block: 4px;
  width: 2px;
  background: var(--color-accent);
  border-radius: var(--radius-full);
}

/* Nested nav items */
.docs-nav-sub {
  padding-inline-start: var(--space-5);
  display: none;
}

.docs-nav-link[aria-expanded="true"] ~ .docs-nav-sub {
  display: block;
}

/* Right TOC */
.docs-toc {
  padding: var(--space-6) var(--space-4);
  position: sticky;
  top: var(--header-height, 60px);
  height: calc(100dvh - var(--header-height, 60px));
  overflow-y: auto;
  border-left: 1px solid var(--color-border);
  font-size: var(--font-size-xs);
}

.docs-toc-title {
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
  color: var(--color-text-muted);
  font-size: var(--font-size-xs);
  margin-block-end: var(--space-3);
}

.docs-toc-link {
  display: block;
  padding: 0.25rem 0;
  color: var(--color-text-muted);
  text-decoration: none;
  border-inline-start: 2px solid transparent;
  padding-inline-start: var(--space-3);
  transition: color var(--duration-fast), border-color var(--duration-fast);
  line-height: 1.4;
}

.docs-toc-link:hover { color: var(--color-text); }
.docs-toc-link.active {
  color: var(--color-accent);
  border-color: var(--color-accent);
}

.docs-toc-link[data-level="3"] { padding-inline-start: var(--space-6); }
.docs-toc-link[data-level="4"] { padding-inline-start: var(--space-9); }
```

### 96.2 Code Documentation Styles

```css
/* ─── API parameter table ─── */
.param-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-sm);
  margin-block: var(--space-6);
  overflow-x: auto;
  display: block;
}

.param-table th {
  text-align: start;
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-subtle);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}

.param-table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
  vertical-align: top;
}

/* Type tag */
.param-type {
  display: inline-flex;
  padding: 0.1em 0.5em;
  background: var(--color-brand-100);
  color: var(--color-brand-700);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.85em;
  white-space: nowrap;
}

.param-type--string  { background: var(--color-success-100); color: var(--color-success-900); }
.param-type--number  { background: var(--color-warning-100); color: var(--color-warning-900); }
.param-type--boolean { background: var(--color-danger-100);  color: var(--color-danger-900); }
.param-type--object  { background: var(--color-brand-100);   color: var(--color-brand-900); }
.param-type--array   { background: var(--color-neutral-100); color: var(--color-neutral-800); }

/* Required badge */
.param-required {
  display: inline-flex;
  padding: 0.1em 0.4em;
  background: var(--color-danger-100);
  color: var(--color-danger-700);
  border-radius: var(--radius-sm);
  font-size: 0.75em;
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-inline-start: 0.375em;
}

/* ─── Version badge ─── */
.version-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.2em 0.6em;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-family: var(--font-mono);
  color: var(--color-text-muted);
  background: var(--color-surface);
}

.version-badge--new     { border-color: var(--color-success-300); color: var(--color-success-700); background: var(--color-success-100); }
.version-badge--deprecated { border-color: var(--color-warning-300); color: var(--color-warning-700); background: var(--color-warning-100); }
.version-badge--removed { border-color: var(--color-danger-300); color: var(--color-danger-700); background: var(--color-danger-100); }

/* ─── Live demo box ─── */
.demo-box {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.demo-box__preview {
  padding: var(--space-8);
  background: var(--color-bg-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 160px;
}

.demo-box__code {
  border-top: 1px solid var(--color-border);
  background: var(--code-bg, #1e1e1e);
  position: relative;
}

.demo-box__toolbar {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: rgba(255 255 255 / 0.05);
  border-bottom: 1px solid rgba(255 255 255 / 0.1);
}

.demo-box__lang {
  font-size: var(--font-size-xs);
  color: rgba(255 255 255 / 0.5);
  font-family: var(--font-mono);
  margin-inline-end: auto;
}
```

---

## 97. ADVANCED FORM PATTERNS

### 97.1 Multi-step Form / Wizard

```css
/* ─── Step form ─── */
.wizard {
  display: grid;
  gap: var(--space-8);
}

.wizard__step {
  display: none;
  animation: step-enter 0.3s var(--ease-out);
}

.wizard__step.active { display: block; }
.wizard__step.exiting {
  display: block;
  animation: step-exit 0.2s var(--ease-in) forwards;
}

@keyframes step-enter {
  from { opacity: 0; translate: 30px 0; }
}
@keyframes step-exit {
  to { opacity: 0; translate: -30px 0; }
}

/* ─── Form field group patterns ─── */
.field-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr));
  gap: var(--space-4);
}

/* ─── OTP / PIN input ─── */
.otp-input {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
}

.otp-digit {
  width: 3rem;
  height: 3.5rem;
  text-align: center;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  font-variant-numeric: tabular-nums;
  border: 2px solid var(--color-border-strong);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  outline: none;
  caret-color: var(--color-accent);
  transition:
    border-color var(--duration-fast),
    box-shadow   var(--duration-fast);
}

.otp-digit:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 20%, transparent);
}

.otp-digit.filled {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 5%, var(--color-surface));
}

/* ─── Credit card form ─── */
.cc-form {
  display: grid;
  gap: var(--space-4);
}

.cc-number-input {
  letter-spacing: 0.15em;
  font-family: var(--font-mono);
}

.cc-form-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-4);
}

/* ─── File upload zone ─── */
.file-upload {
  border: 2px dashed var(--color-border-strong);
  border-radius: var(--radius-xl);
  padding: var(--space-10);
  text-align: center;
  cursor: pointer;
  transition:
    border-color var(--duration-fast),
    background   var(--duration-fast),
    scale        var(--duration-fast) var(--ease-bounce);
  position: relative;
}

.file-upload input[type="file"] {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
  width: 100%;
  height: 100%;
}

.file-upload:hover,
.file-upload:focus-within {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 5%, transparent);
}

.file-upload.dragging {
  border-color: var(--color-accent);
  background: color-mix(in srgb, var(--color-accent) 10%, transparent);
  scale: 1.01;
}

.file-upload__icon {
  font-size: 3rem;
  margin-block-end: var(--space-3);
  color: var(--color-text-muted);
  transition: scale var(--duration-fast) var(--ease-bounce);
}

.file-upload.dragging .file-upload__icon { scale: 1.2; }

.file-upload__title {
  font-weight: var(--font-weight-semibold);
  margin-block-end: var(--space-1);
}

.file-upload__subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}

/* Uploaded files list */
.file-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-block-start: var(--space-4);
}

.file-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  animation: file-appear 0.2s var(--ease-out);
}

@keyframes file-appear {
  from { opacity: 0; translate: 0 -6px; }
}

.file-item__icon {
  width: 2rem;
  height: 2rem;
  border-radius: var(--radius-md);
  background: var(--color-brand-100);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  flex-shrink: 0;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
}

.file-item__info { flex: 1; min-width: 0; }

.file-item__name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-item__size {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

/* Upload progress */
.file-item__progress {
  height: 3px;
  background: var(--color-bg-muted);
  border-radius: var(--radius-full);
  overflow: hidden;
  margin-block-start: var(--space-1);
}

.file-item__progress-bar {
  height: 100%;
  background: var(--color-accent);
  border-radius: inherit;
  width: var(--progress, 0%);
  transition: width 0.2s var(--ease-out);
}
```

---

## 98. CSS CUSTOM SCROLLBAR LIBRARY

```css
/* ─── Scrollbar token system ─── */
:root {
  --scrollbar-width: 6px;
  --scrollbar-track: transparent;
  --scrollbar-thumb: var(--color-border-strong);
  --scrollbar-thumb-hover: var(--color-text-muted);
  --scrollbar-radius: var(--radius-full);
}

/* ─── Firefox (standard) ─── */
.custom-scroll {
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
}

/* ─── WebKit ─── */
.custom-scroll::-webkit-scrollbar {
  width: var(--scrollbar-width);
  height: var(--scrollbar-width);
}

.custom-scroll::-webkit-scrollbar-track {
  background: var(--scrollbar-track);
  border-radius: var(--scrollbar-radius);
}

.custom-scroll::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb);
  border-radius: var(--scrollbar-radius);
  transition: background var(--duration-fast);
}

.custom-scroll::-webkit-scrollbar-thumb:hover {
  background: var(--scrollbar-thumb-hover);
}

.custom-scroll::-webkit-scrollbar-corner {
  background: transparent;
}

/* ─── Preset variants ─── */
.scroll-thin {
  --scrollbar-width: 4px;
}

.scroll-hidden {
  scrollbar-width: none;
}
.scroll-hidden::-webkit-scrollbar { display: none; }

.scroll-brand {
  --scrollbar-thumb: var(--color-accent);
  --scrollbar-thumb-hover: var(--color-accent-hover);
  --scrollbar-track: color-mix(in srgb, var(--color-accent) 10%, transparent);
}

.scroll-dark {
  --scrollbar-thumb: #555;
  --scrollbar-thumb-hover: #777;
  --scrollbar-track: #2a2a2a;
}

.scroll-light {
  --scrollbar-thumb: #ddd;
  --scrollbar-thumb-hover: #bbb;
  --scrollbar-track: #f5f5f5;
}

/* Overlay scrollbar (doesn't take space) */
.scroll-overlay {
  overflow: overlay;  /* Chrome only, fallback to auto */
  overflow: auto;
}

/* ─── macOS-style auto-hiding scrollbar ─── */
.scroll-macos {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
  transition: scrollbar-color var(--duration-slow);
}

.scroll-macos:hover {
  scrollbar-color: var(--scrollbar-thumb) transparent;
}

.scroll-macos::-webkit-scrollbar { width: 8px; }
.scroll-macos::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: 4px;
  border: 2px solid transparent;
  background-clip: content-box;
  transition: background var(--duration-slow);
}
.scroll-macos:hover::-webkit-scrollbar-thumb {
  background-color: rgba(0 0 0 / 0.25);
}
```

---

## 99. CSS SPECIFICITY — BATTLE-TESTED SOLUTIONS

### 99.1 Specificity Conflict Resolution Patterns

```css
/* ─── Pattern 1: The @layer override ─── */
@layer base, components, overrides;

@layer base {
  .text { color: var(--color-text); }
}

@layer components {
  .card .text { color: var(--color-text-muted); }  /* 0-2-0 */
}

@layer overrides {
  /* This wins even with lower specificity because overrides > components */
  .text-accent { color: var(--color-accent); }  /* 0-1-0 */
}

/* ─── Pattern 2: :where() to drop specificity ─── */
/* Problem: library component has too-high specificity */
:is(.nav, .sidebar, .footer) .link {  /* 0-2-0 — hard to override */
  color: var(--color-accent);
}

/* ✅ Rewrite with :where() */
:where(.nav, .sidebar, .footer) .link {  /* 0-1-0 — easy to override */
  color: var(--color-accent);
}

/* ─── Pattern 3: Isolation with data attributes ─── */
/* Use data attributes instead of class nesting to avoid specificity stacking */
.card { }                      /* 0-1-0 */
.card[data-variant="featured"] { }  /* 0-1-1 — still manageable */

/* vs */
.card.card--featured { }       /* 0-2-0 — requires another class to beat */

/* ─── Pattern 4: The !important escape hatch (scoped) ─── */
/* Never globally, but acceptable in these cases: */

/* 1. Utility classes */
@layer utilities {
  .hidden { display: none !important; }
  .sr-only { position: absolute !important; }
  .text-center { text-align: center !important; }
}

/* 2. Forced states */
[aria-hidden="true"] { display: none !important; }

/* 3. Animation endpoints */
.animate-to-end { /* JS toggles this */
  transform: translateX(100%) !important;
}

/* ─── Pattern 5: Double-class trick (without @layer) ─── */
/* Increase specificity without IDs */
.btn.btn { color: blue; }       /* 0-2-0 */
.btn.btn.btn { color: green; }  /* 0-3-0 — use sparingly */

/* ─── Pattern 6: Specificity graph checking ─── */
/*
A healthy specificity graph should be flat or slowly increasing.
Use this mental model:
  All selectors in 0-0-x zone: element tags
  All selectors in 0-1-x zone: classes (preferred)
  Avoid 1-x-x zone: IDs
  Avoid 0-0-0 with !important: only utilities

Red flags:
  Many 1-x-x selectors (too many IDs)
  Zigzag specificity (increasing then decreasing)
  Heavy !important usage (> 5% of rules)
*/
```

---

## 100. THE FINAL MASTER REFERENCE

### 100.1 CSS Properties Grouped by Impact

```css
/* ─── Properties that trigger LAYOUT (expensive) ─── */
/*
  width, height, min-*, max-*
  margin, padding
  border (width changes)
  position, top, right, bottom, left, inset
  display (change)
  overflow
  font-size, line-height
  float, clear
  grid-template-*, grid-column, grid-row
  flex-basis, flex-grow, flex-shrink
  content (pseudo-elements)
  table-layout
  column-*
*/

/* ─── Properties that trigger PAINT only ─── */
/*
  color, background-color
  border-color, border-style (not width)
  outline
  box-shadow, text-shadow
  border-radius
  visibility
  background-image (gradient changes)
  filter (some types)
  opacity (in some browsers — now composited!)
*/

/* ─── Properties that are COMPOSITED (cheapest) ─── */
/*
  transform: translate(), scale(), rotate()
  opacity (modern browsers)
  will-change (promotes to layer)
  filter: blur, brightness (on composited layers)
  backdrop-filter (composited)
  clip-path (on composited elements)
*/

/* ─── Properties NOT inherited ─── */
/*
  Most layout: display, position, width, height, margin, padding,
               border, overflow, z-index, float
  Visual: background, box-shadow, opacity, transform, filter
  UI: outline, cursor (yes! cursor is inherited — exception)
*/

/* ─── Properties that ARE inherited ─── */
/*
  Typography: font-*, line-height, letter-spacing, word-spacing,
              text-align, text-transform, text-indent,
              text-decoration (partial), white-space, hyphens
  Color: color, (not background-color!)
  Other: cursor, pointer-events, visibility, quotes,
         list-style-*, border-collapse, border-spacing,
         caption-side, empty-cells, direction, writing-mode,
         word-break, overflow-wrap
  Custom properties: depend on inherits: declaration in @property
*/
```

### 100.2 Every CSS At-Rule

```css
/* ─── COMPLETE @RULE REFERENCE ─── */

@charset "UTF-8";                         /* Character encoding (must be first) */

@import url('style.css');                 /* Import external stylesheet */
@import url('style.css') layer(base);    /* Import into layer */
@import url('style.css') supports(display: grid);  /* Conditional import */
@import url('style.css') (max-width: 768px);        /* Media conditional */

@layer base, components;                 /* Declare layer order */
@layer base { /* rules */ }             /* Define layer */

@media (min-width: 768px) { }           /* Media query */
@media print { }

@supports (display: grid) { }           /* Feature query */
@supports not (gap: 1rem) { }
@supports selector(:has()) { }          /* Selector support query */

@keyframes name {                        /* Animation keyframes */
  from { } to { }
  0% { } 50% { } 100% { }
}

@font-face {                             /* Custom font */
  font-family: 'Name';
  src: url('font.woff2') format('woff2');
  font-display: swap;
  unicode-range: U+0000-00FF;
}

@property --name {                       /* Custom property type */
  syntax: '<color>';
  initial-value: red;
  inherits: false;
}

@counter-style thumbs {                  /* Custom counter */
  system: cyclic;
  symbols: "\1F44D";
  suffix: " ";
}

@page { margin: 2cm; }                  /* Print page margins */
@page :first { }
@page :left { }
@page :right { }
@page :blank { }

@namespace url('http://www.w3.org/1999/xhtml');  /* XML namespace */

@scope (.card) { }                       /* Scope (new) */
@scope (.card) to (.body) { }

@container (min-width: 400px) { }       /* Container query */
@container sidebar (min-width: 300px) { }

@color-profile --fogra39 {              /* Color profile */
  src: url('FOGRA39.icc');
  rendering-intent: relative-colorimetric;
}

@position-try --tooltip-top { }         /* Anchor positioning fallback */

/* ─── DRAFT / PROPOSED (not yet stable) ─── */
/* @custom-selector :--heading h1, h2, h3; */
/* @mixin name { } */
/* @apply mixin-name; */
/* @when supports(display: grid) { } @else { } */
/* @function --fluid($min, $max) { result: clamp($min, ...); } */
```

### 100.3 Color Function Syntax Reference

```css
/* All modern color functions and their syntax */

/* ─── Legacy ─── */
color: rgb(255, 0, 0);
color: rgb(255 0 0);              /* modern no-comma */
color: rgb(255 0 0 / 0.5);       /* with alpha */
color: rgba(255, 0, 0, 0.5);     /* legacy with alpha */

color: hsl(0, 100%, 50%);
color: hsl(0 100% 50%);
color: hsl(0 100% 50% / 0.5);

/* ─── HWB ─── */
color: hwb(0 0% 0%);             /* hue white black */
color: hwb(0 0% 0% / 0.5);

/* ─── Lab / LCH ─── */
color: lab(50% 40 59.4);         /* lightness a b */
color: lch(50% 70 40);           /* lightness chroma hue */

/* ─── OKLAB / OKLCH (recommended) ─── */
color: oklab(0.5 0.15 -0.1);    /* lightness a b */
color: oklch(0.5 0.2 250);       /* lightness chroma hue */
color: oklch(0.5 0.2 250 / 0.5);

/* ─── display-p3 (wide gamut) ─── */
color: color(display-p3 0.5 0.3 0.8);
color: color(display-p3 0.5 0.3 0.8 / 0.5);

/* ─── Other color() spaces ─── */
color: color(srgb 0.5 0.3 0.8);
color: color(srgb-linear 0.5 0.3 0.8);
color: color(a98-rgb 0.5 0.3 0.8);
color: color(prophoto-rgb 0.5 0.3 0.8);
color: color(rec2020 0.5 0.3 0.8);
color: color(xyz-d50 0.3 0.2 0.5);
color: color(xyz-d65 0.3 0.2 0.5);

/* ─── Named system colors ─── */
color: Canvas;           /* page background */
color: CanvasText;       /* page text */
color: LinkText;         /* link color */
color: VisitedText;      /* visited link */
color: ActiveText;       /* active link */
color: ButtonFace;       /* button background */
color: ButtonText;       /* button text */
color: ButtonBorder;     /* button border */
color: Field;            /* input background */
color: FieldText;        /* input text */
color: Highlight;        /* selected background */
color: HighlightText;    /* selected text */
color: GrayText;         /* disabled text */
color: AccentColor;      /* OS accent */
color: AccentColorText;  /* text on accent */
color: Mark;             /* highlighted text bg */
color: MarkText;         /* highlighted text */

/* ─── Color functions ─── */
color: color-mix(in oklch, blue 30%, red);
color: color-mix(in srgb, var(--accent) 20%, transparent);

/* Relative color syntax */
color: oklch(from var(--base) l c h);
color: oklch(from var(--base) calc(l + 0.2) c h);
color: oklch(from var(--base) l calc(c * 0.5) h);
color: rgba(from var(--base) r g b / 0.5);

/* light-dark() */
color: light-dark(#000, #fff);
background: light-dark(white, #111);
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║            THE MONUMENTAL CSS GUIDE — COMPLETE                       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  PARTS:      I · II · III · IV · V                                  ║
║  CHAPTERS:   100 chapters                                            ║
║  TOTAL SIZE: ~20,000+ lines                                          ║
║                                                                      ║
║  COVERAGE:                                                           ║
║  ✅ Architecture: ITCSS, SMACSS, BEM, CUBE, @layer, tokens          ║
║  ✅ Layout: Grid, Flexbox, Subgrid, Container Queries                ║
║  ✅ Typography: fluid, variable fonts, OpenType, prose               ║
║  ✅ Color: oklch, color-mix, relative syntax, dark mode              ║
║  ✅ Animation: keyframes, transitions, scroll-driven, spring         ║
║  ✅ Modern: :has(), nesting, anchor, view transitions, @scope        ║
║  ✅ Components: 30+ complete UI components with states               ║
║  ✅ Patterns: backgrounds, 3D, parallax, glass, aurora               ║
║  ✅ Contexts: email, PWA, print, RTL, shadow DOM, SVG                ║
║  ✅ Accessibility: WCAG 2.2, focus, motion, contrast, forced-colors  ║
║  ✅ Performance: GPU, contain, content-visibility, critical CSS       ║
║  ✅ E-commerce: product cards, cart, checkout, payment card           ║
║  ✅ Social: chat UI, feed, typing indicator, reactions                ║
║  ✅ Docs: sidebar nav, TOC, code blocks, API tables                  ║
║  ✅ Debugging: DevTools, audit checklist, gotchas (50+)              ║
║  ✅ Reference: all properties, at-rules, units, functions            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```
