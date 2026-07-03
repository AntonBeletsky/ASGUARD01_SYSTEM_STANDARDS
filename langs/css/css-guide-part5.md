\# PART V — CSS COMPLETE: REMAINING PATTERNS \& DEEP CUTS



\---



\## 91. CSS BACKGROUND PATTERNS LIBRARY



\### 91.1 Pure CSS Geometric Patterns



```css

/\* ─── 1. Checkerboard ─── \*/

.pattern-checkerboard {

&#x20; background-color: #e8e8e8;

&#x20; background-image:

&#x20;   conic-gradient(#ccc 90deg, transparent 90deg);

&#x20; background-size: 24px 24px;

}



/\* ─── 2. Polka dots ─── \*/

.pattern-dots {

&#x20; background-color: #f8f8f8;

&#x20; background-image:

&#x20;   radial-gradient(circle, #d0d0d0 1.5px, transparent 1.5px);

&#x20; background-size: 20px 20px;

}



/\* ─── 3. Grid lines ─── \*/

.pattern-grid {

&#x20; background-color: #fff;

&#x20; background-image:

&#x20;   linear-gradient(var(--color-border) 1px, transparent 1px),

&#x20;   linear-gradient(to right, var(--color-border) 1px, transparent 1px);

&#x20; background-size: 24px 24px;

}



/\* ─── 4. Diagonal stripes ─── \*/

.pattern-stripes {

&#x20; background-image: repeating-linear-gradient(

&#x20;   45deg,

&#x20;   transparent,

&#x20;   transparent 8px,

&#x20;   rgba(0 0 0 / 0.05) 8px,

&#x20;   rgba(0 0 0 / 0.05) 16px

&#x20; );

}



/\* ─── 5. Diagonal grid ─── \*/

.pattern-diagonal-grid {

&#x20; background-image:

&#x20;   repeating-linear-gradient(45deg, #e0e0e0 0, #e0e0e0 1px, transparent 0, transparent 50%),

&#x20;   repeating-linear-gradient(-45deg, #e0e0e0 0, #e0e0e0 1px, transparent 0, transparent 50%);

&#x20; background-size: 16px 16px;

&#x20; background-color: #fff;

}



/\* ─── 6. Honeycomb (hexagonal) ─── \*/

.pattern-hex {

&#x20; background-color: #f5f5f5;

&#x20; background-image:

&#x20;   radial-gradient(circle farthest-side at 0% 50%, #fbfbfb 23.5%, rgba(240,166,17,0) 0) 21px 30px,

&#x20;   radial-gradient(circle farthest-side at 0% 50%, #d9d9d9 24%, rgba(240,166,17,0) 0) 19px 30px,

&#x20;   linear-gradient(#fbfbfb 14%, rgba(240,166,17,0) 0, rgba(240,166,17,0) 85%, #fbfbfb 0) 0 0,

&#x20;   linear-gradient(150deg, #fbfbfb 24%, #d9d9d9 0, #d9d9d9 26%, rgba(240,166,17,0) 0, rgba(240,166,17,0) 74%, #d9d9d9 0, #d9d9d9 76%, #fbfbfb 0) 0 0,

&#x20;   linear-gradient(30deg, #fbfbfb 24%, #d9d9d9 0, #d9d9d9 26%, rgba(240,166,17,0) 0, rgba(240,166,17,0) 74%, #d9d9d9 0, #d9d9d9 76%, #fbfbfb 0) 0 0;

&#x20; background-size: 40px 60px;

}



/\* ─── 7. Triangles ─── \*/

.pattern-triangles {

&#x20; background-color: #f0f0f0;

&#x20; background-image:

&#x20;   linear-gradient(60deg, #e0e0e0 25%, transparent 25%),

&#x20;   linear-gradient(-60deg, #e0e0e0 25%, transparent 25%),

&#x20;   linear-gradient(60deg, transparent 75%, #e0e0e0 75%),

&#x20;   linear-gradient(-60deg, transparent 75%, #e0e0e0 75%);

&#x20; background-size: 20px 35px;

&#x20; background-position: 0 0, 0 0, 10px 18px, 10px 18px;

}



/\* ─── 8. Carbon fiber ─── \*/

.pattern-carbon {

&#x20; background-color: #1a1a1a;

&#x20; background-image:

&#x20;   linear-gradient(27deg, #151515 5px, transparent 5px) 0 5px,

&#x20;   linear-gradient(207deg, #151515 5px, transparent 5px) 10px 0px,

&#x20;   linear-gradient(27deg, #222 5px, transparent 5px) 0px 10px,

&#x20;   linear-gradient(207deg, #222 5px, transparent 5px) 10px 5px,

&#x20;   linear-gradient(90deg, #1b1b1b 10px, transparent 10px),

&#x20;   linear-gradient(#1d1d1d 25%, #1a1a1a 25%, #1a1a1a 50%, transparent 50%,

&#x20;     transparent 75%, #242424 75%, #242424);

&#x20; background-size: 20px 20px;

}



/\* ─── 9. Blueprint ─── \*/

.pattern-blueprint {

&#x20; background-color: #1a2d5a;

&#x20; background-image:

&#x20;   linear-gradient(rgba(255 255 255 / 0.07) 1px, transparent 1px),

&#x20;   linear-gradient(90deg, rgba(255 255 255 / 0.07) 1px, transparent 1px),

&#x20;   linear-gradient(rgba(255 255 255 / 0.04) 1px, transparent 1px),

&#x20;   linear-gradient(90deg, rgba(255 255 255 / 0.04) 1px, transparent 1px);

&#x20; background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;

&#x20; background-position: -2px -2px, -2px -2px, -1px -1px, -1px -1px;

}



/\* ─── 10. Noise texture (CSS only) ─── \*/

.pattern-noise {

&#x20; position: relative;

}

.pattern-noise::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; opacity: 0.05;

&#x20; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");

&#x20; background-repeat: repeat;

&#x20; background-size: 256px 256px;

&#x20; pointer-events: none;

}



/\* ─── 11. Animated gradient mesh ─── \*/

.pattern-animated-mesh {

&#x20; background-color: #0f0f1a;

}

.pattern-animated-mesh::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: -100%;

&#x20; background:

&#x20;   radial-gradient(ellipse at 20% 50%, oklch(0.5 0.25 280 / 0.4) 0%, transparent 60%),

&#x20;   radial-gradient(ellipse at 80% 20%, oklch(0.5 0.2 200 / 0.3) 0%, transparent 55%),

&#x20;   radial-gradient(ellipse at 60% 80%, oklch(0.5 0.22 320 / 0.35) 0%, transparent 50%);

&#x20; filter: blur(40px);

&#x20; animation: mesh-float 12s ease-in-out infinite alternate;

}



@keyframes mesh-float {

&#x20; 0%   { transform: translate(0%, 0%) scale(1); }

&#x20; 33%  { transform: translate(3%, -4%) scale(1.05); }

&#x20; 66%  { transform: translate(-2%, 5%) scale(0.97); }

&#x20; 100% { transform: translate(4%, -2%) scale(1.03); }

}

```



\### 91.2 SVG-based CSS Patterns



```css

/\* ─── Circuit board pattern ─── \*/

.pattern-circuit {

&#x20; background-color: #0d1b2a;

&#x20; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Cg fill='none' stroke='%231a3a5c' stroke-width='1'%3E%3Cpath d='M10 10 L10 50 L50 50'/%3E%3Cpath d='M50 10 L50 30 L90 30 L90 90'/%3E%3Cpath d='M30 60 L30 90 L70 90'/%3E%3C/g%3E%3Ccircle cx='10' cy='10' r='3' fill='%231a3a5c'/%3E%3Ccircle cx='50' cy='50' r='3' fill='%231a3a5c'/%3E%3Ccircle cx='90' cy='30' r='3' fill='%231a3a5c'/%3E%3C/svg%3E");

}



/\* ─── Topographic map ─── \*/

.pattern-topo {

&#x20; background-color: #f0f4e8;

&#x20; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cpath d='M20 100 Q60 20 100 100 Q140 180 180 100' fill='none' stroke='%23b8cc8a' stroke-width='1.5' opacity='0.6'/%3E%3Cpath d='M0 120 Q40 40 80 120 Q120 200 160 120 Q180 80 200 120' fill='none' stroke='%23b8cc8a' stroke-width='1.5' opacity='0.4'/%3E%3C/svg%3E");

}

```



\---



\## 92. CSS 3D EFFECTS — ADVANCED



\### 92.1 3D Card Scenes



```css

/\* ─── 3D Product showcase ─── \*/

.scene-3d {

&#x20; perspective: 1200px;

&#x20; perspective-origin: 50% 50%;

}



.card-3d-showcase {

&#x20; transform-style: preserve-3d;

&#x20; transform: rotateX(var(--rx, 0deg)) rotateY(var(--ry, 0deg));

&#x20; transition: transform 0.1s ease-out;

&#x20; width: 300px;

&#x20; height: 400px;

&#x20; position: relative;

}



/\* JS updates --rx and --ry on mousemove \*/



/\* Faces \*/

.face {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; backface-visibility: hidden;

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

}



.face-front  { transform: translateZ(20px); }

.face-back   { transform: rotateY(180deg) translateZ(20px); }

.face-top    {

&#x20; height: 20px;

&#x20; top: -20px;

&#x20; left: 0;

&#x20; right: 0;

&#x20; transform: rotateX(90deg);

&#x20; transform-origin: bottom;

}

.face-bottom {

&#x20; height: 20px;

&#x20; bottom: -20px;

&#x20; left: 0;

&#x20; right: 0;

&#x20; transform: rotateX(-90deg);

&#x20; transform-origin: top;

}

.face-left {

&#x20; width: 20px;

&#x20; left: -20px;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; transform: rotateY(-90deg);

&#x20; transform-origin: right;

}

.face-right {

&#x20; width: 20px;

&#x20; right: -20px;

&#x20; top: 0;

&#x20; bottom: 0;

&#x20; transform: rotateY(90deg);

&#x20; transform-origin: left;

}



/\* ─── Layered 3D card (depth illusion) ─── \*/

.depth-card {

&#x20; position: relative;

&#x20; transform-style: preserve-3d;

&#x20; transition: transform 0.4s var(--ease-out);

}



.depth-card:hover {

&#x20; transform: translateY(-4px);

}



/\* Each layer offset in Z \*/

.depth-card\_\_layer {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; border-radius: inherit;

}



.depth-card\_\_layer--3 { transform: translateZ(-3px); background: oklch(0.6 0.15 250 / 0.6); }

.depth-card\_\_layer--2 { transform: translateZ(-6px); background: oklch(0.5 0.15 250 / 0.4); }

.depth-card\_\_layer--1 { transform: translateZ(-9px); background: oklch(0.4 0.15 250 / 0.2); }



/\* ─── CSS Cube ─── \*/

.cube-container {

&#x20; perspective: 600px;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

}



.cube {

&#x20; --size: 100px;

&#x20; width: var(--size);

&#x20; height: var(--size);

&#x20; transform-style: preserve-3d;

&#x20; animation: cube-rotate 8s linear infinite;

}



@keyframes cube-rotate {

&#x20; from { transform: rotateX(-20deg) rotateY(0deg); }

&#x20; to   { transform: rotateX(-20deg) rotateY(360deg); }

}



.cube\_\_face {

&#x20; position: absolute;

&#x20; width: var(--size);

&#x20; height: var(--size);

&#x20; border: 2px solid oklch(0.7 0.2 250 / 0.6);

&#x20; background: oklch(0.5 0.2 250 / 0.15);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: 2rem;

&#x20; backface-visibility: visible;

}



.cube\_\_face--front  { transform: translateZ(calc(var(--size) / 2)); }

.cube\_\_face--back   { transform: rotateY(180deg) translateZ(calc(var(--size) / 2)); }

.cube\_\_face--right  { transform: rotateY(90deg) translateZ(calc(var(--size) / 2)); }

.cube\_\_face--left   { transform: rotateY(-90deg) translateZ(calc(var(--size) / 2)); }

.cube\_\_face--top    { transform: rotateX(90deg) translateZ(calc(var(--size) / 2)); }

.cube\_\_face--bottom { transform: rotateX(-90deg) translateZ(calc(var(--size) / 2)); }

```



\### 92.2 3D Typography



```css

/\* ─── 3D extruded text ─── \*/

.text-3d-extrude {

&#x20; font-size: clamp(3rem, 8vw, 8rem);

&#x20; font-weight: var(--font-weight-black);

&#x20; color: var(--color-accent);

&#x20; text-shadow:

&#x20;   1px  1px 0 oklch(from var(--color-accent) calc(l - 0.1) c h),

&#x20;   2px  2px 0 oklch(from var(--color-accent) calc(l - 0.15) c h),

&#x20;   3px  3px 0 oklch(from var(--color-accent) calc(l - 0.2) c h),

&#x20;   4px  4px 0 oklch(from var(--color-accent) calc(l - 0.25) c h),

&#x20;   5px  5px 0 oklch(from var(--color-accent) calc(l - 0.3) c h),

&#x20;   6px  6px 0 oklch(from var(--color-accent) calc(l - 0.35) c h),

&#x20;   7px  7px 8px rgb(0 0 0 / 0.4);

}



/\* ─── Letterpress / inset text ─── \*/

.text-letterpress {

&#x20; color: transparent;

&#x20; background: linear-gradient(to bottom, #555, #333);

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; text-shadow:

&#x20;   0 1px 1px rgba(255 255 255 / 0.2),

&#x20;   0 -1px 1px rgba(0 0 0 / 0.5);

}



/\* ─── Retro chrome text ─── \*/

.text-chrome {

&#x20; background: linear-gradient(

&#x20;   180deg,

&#x20;   #fff  0%,

&#x20;   #bbb 25%,

&#x20;   #fff 45%,

&#x20;   #888 65%,

&#x20;   #ddd 80%,

&#x20;   #fff 100%

&#x20; );

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

&#x20; filter: drop-shadow(1px 2px 4px rgb(0 0 0 / 0.5));

}



/\* ─── Animated holographic text ─── \*/

@keyframes holo-shift {

&#x20; 0%   { background-position: 0% 50%; }

&#x20; 50%  { background-position: 100% 50%; }

&#x20; 100% { background-position: 0% 50%; }

}



.text-holographic {

&#x20; background: linear-gradient(

&#x20;   135deg,

&#x20;   oklch(0.8 0.3 0),

&#x20;   oklch(0.8 0.3 60),

&#x20;   oklch(0.8 0.3 120),

&#x20;   oklch(0.8 0.3 180),

&#x20;   oklch(0.8 0.3 240),

&#x20;   oklch(0.8 0.3 300),

&#x20;   oklch(0.8 0.3 360)

&#x20; );

&#x20; background-size: 300% 300%;

&#x20; -webkit-background-clip: text;

&#x20; background-clip: text;

&#x20; color: transparent;

&#x20; animation: holo-shift 4s ease infinite;

}

```



\---



\## 93. ECOMMERCE UI PATTERNS



\### 93.1 Product Card



```css

/\* ─── Product card ─── \*/

.product-card {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

&#x20; transition:

&#x20;   box-shadow var(--duration-normal) var(--ease-out),

&#x20;   translate  var(--duration-normal) var(--ease-out);

&#x20; position: relative;

}



.product-card:hover {

&#x20; box-shadow: var(--shadow-xl);

&#x20; translate: 0 -3px;

}



/\* Image area \*/

.product-card\_\_media {

&#x20; position: relative;

&#x20; aspect-ratio: 1;

&#x20; background: var(--color-bg-subtle);

&#x20; overflow: hidden;

}



.product-card\_\_img {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; transition: scale var(--duration-slow) var(--ease-out);

}



.product-card:hover .product-card\_\_img { scale: 1.05; }



/\* Quick actions overlay \*/

.product-card\_\_actions {

&#x20; position: absolute;

&#x20; inset-block-end: 0;

&#x20; inset-inline: 0;

&#x20; padding: var(--space-3);

&#x20; background: linear-gradient(to top, rgb(0 0 0 / 0.5), transparent);

&#x20; display: flex;

&#x20; gap: var(--space-2);

&#x20; justify-content: center;

&#x20; translate: 0 100%;

&#x20; opacity: 0;

&#x20; transition:

&#x20;   translate var(--duration-normal) var(--ease-out),

&#x20;   opacity   var(--duration-normal);

}



.product-card:hover .product-card\_\_actions {

&#x20; translate: 0 0;

&#x20; opacity: 1;

}



/\* Badges \*/

.product-card\_\_badge {

&#x20; position: absolute;

&#x20; inset-block-start: var(--space-3);

&#x20; inset-inline-start: var(--space-3);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-1);

&#x20; z-index: 1;

}



.product-badge {

&#x20; display: inline-flex;

&#x20; padding: 0.2em 0.6em;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; border-radius: var(--radius-sm);

&#x20; line-height: 1.5;

}



.product-badge--new    { background: var(--color-accent); color: white; }

.product-badge--sale   { background: var(--color-danger-500); color: white; }

.product-badge--hot    { background: var(--color-warning-500); color: #111; }

.product-badge--sold   { background: var(--color-neutral-700); color: white; }



/\* Wishlist button \*/

.product-card\_\_wishlist {

&#x20; position: absolute;

&#x20; inset-block-start: var(--space-3);

&#x20; inset-inline-end: var(--space-3);

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: 50%;

&#x20; background: var(--color-surface);

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; box-shadow: var(--shadow-sm);

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

&#x20; z-index: 1;

}



.product-card\_\_wishlist:hover { scale: 1.1; }

.product-card\_\_wishlist\[aria-pressed="true"] { color: var(--color-danger-500); }



/\* Info area \*/

.product-card\_\_body {

&#x20; padding: var(--space-4);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

&#x20; flex: 1;

}



.product-card\_\_category {

&#x20; font-size: var(--font-size-xs);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; font-weight: var(--font-weight-medium);

}



.product-card\_\_name {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.4;

&#x20; overflow: hidden;

&#x20; display: -webkit-box;

&#x20; -webkit-line-clamp: 2;

&#x20; -webkit-box-orient: vertical;

}



/\* Rating \*/

.product-card\_\_rating {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

}



/\* Price \*/

.product-card\_\_price {

&#x20; display: flex;

&#x20; align-items: baseline;

&#x20; gap: var(--space-2);

&#x20; flex-wrap: wrap;

&#x20; margin-block-start: auto;

}



.price-current {

&#x20; font-size: var(--font-size-lg);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-variant-numeric: tabular-nums;

}



.price-original {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: line-through;

&#x20; font-variant-numeric: tabular-nums;

}



.price-discount {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; color: var(--color-danger-500);

&#x20; background: var(--color-danger-100);

&#x20; padding: 0.125em 0.4em;

&#x20; border-radius: var(--radius-sm);

}



/\* ─── Product grid ─── \*/

.product-grid {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr));

&#x20; gap: var(--space-4);

}

```



\### 93.2 Shopping Cart \& Checkout



```css

/\* ─── Cart item ─── \*/

.cart-item {

&#x20; display: grid;

&#x20; grid-template-columns: 80px 1fr auto;

&#x20; gap: var(--space-4);

&#x20; align-items: start;

&#x20; padding: var(--space-4) 0;

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; animation: cart-item-in 0.3s var(--ease-out);

}



@keyframes cart-item-in {

&#x20; from { opacity: 0; translate: 0 -8px; }

}



.cart-item.removing {

&#x20; animation: cart-item-out 0.25s var(--ease-in) forwards;

}



@keyframes cart-item-out {

&#x20; to { opacity: 0; height: 0; padding: 0; overflow: hidden; }

}



.cart-item\_\_image {

&#x20; width: 80px;

&#x20; height: 80px;

&#x20; object-fit: cover;

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-bg-subtle);

}



.cart-item\_\_name {

&#x20; font-weight: var(--font-weight-medium);

&#x20; font-size: var(--font-size-sm);

}



.cart-item\_\_meta {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

&#x20; margin-top: var(--space-1);

}



/\* Quantity stepper \*/

.quantity-stepper {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; overflow: hidden;

}



.quantity-stepper\_\_btn {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; font-size: 1.125rem;

&#x20; color: var(--color-text);

&#x20; transition: background var(--duration-fast);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

}



.quantity-stepper\_\_btn:hover { background: var(--color-bg-subtle); }

.quantity-stepper\_\_btn:disabled { opacity: 0.4; cursor: not-allowed; }



.quantity-stepper\_\_value {

&#x20; min-width: 2.5rem;

&#x20; text-align: center;

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; font-variant-numeric: tabular-nums;

&#x20; border: none;

&#x20; outline: none;

&#x20; background: none;

}



/\* ─── Order summary ─── \*/

.order-summary {

&#x20; background: var(--color-bg-subtle);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-6);

&#x20; border: 1px solid var(--color-border);

}



.order-line {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; align-items: baseline;

&#x20; padding-block: var(--space-2);

&#x20; font-size: var(--font-size-sm);

}



.order-line + .order-line { border-top: 1px solid var(--color-border); }



.order-line--total {

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-size: var(--font-size-base);

&#x20; padding-block-start: var(--space-4);

&#x20; border-top: 2px solid var(--color-border);

&#x20; margin-block-start: var(--space-2);

}



.order-line\_\_value { font-variant-numeric: tabular-nums; }



/\* ─── Checkout steps ─── \*/

.checkout-progress {

&#x20; display: flex;

&#x20; align-items: center;

}



.checkout-step {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; flex: 1;

&#x20; position: relative;

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

}



.checkout-step:not(:last-child)::after {

&#x20; content: '';

&#x20; flex: 1;

&#x20; height: 2px;

&#x20; background: var(--color-border);

&#x20; margin-inline-start: var(--space-2);

}



.checkout-step.completed::after { background: var(--color-accent); }



.checkout-step\_\_num {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: 50%;

&#x20; border: 2px solid var(--color-border);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

&#x20; flex-shrink: 0;

&#x20; background: var(--color-surface);

&#x20; transition:

&#x20;   background var(--duration-fast),

&#x20;   border-color var(--duration-fast),

&#x20;   color var(--duration-fast);

}



.checkout-step.active .checkout-step\_\_num {

&#x20; border-color: var(--color-accent);

&#x20; color: var(--color-accent);

}



.checkout-step.completed .checkout-step\_\_num {

&#x20; background: var(--color-accent);

&#x20; border-color: var(--color-accent);

&#x20; color: white;

}



/\* ─── Payment card input ─── \*/

.payment-card {

&#x20; background: linear-gradient(135deg, #1a1a2e, #16213e);

&#x20; border-radius: var(--radius-2xl);

&#x20; padding: var(--space-6);

&#x20; color: white;

&#x20; font-family: var(--font-mono);

&#x20; position: relative;

&#x20; overflow: hidden;

&#x20; aspect-ratio: 1.586;

&#x20; max-width: 380px;

}



.payment-card::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: linear-gradient(135deg, transparent 40%, rgba(255 255 255 / 0.05) 100%);

}



.payment-card\_\_chip {

&#x20; width: 2.5rem;

&#x20; height: 2rem;

&#x20; background: linear-gradient(135deg, #d4af37, #b8942a);

&#x20; border-radius: 6px;

&#x20; margin-block-end: var(--space-6);

}



.payment-card\_\_number {

&#x20; font-size: clamp(1rem, 3vw, 1.25rem);

&#x20; letter-spacing: 0.15em;

&#x20; margin-block-end: var(--space-4);

}



.payment-card\_\_meta {

&#x20; display: flex;

&#x20; justify-content: space-between;

&#x20; font-size: var(--font-size-xs);

&#x20; opacity: 0.7;

&#x20; margin-block-end: var(--space-2);

}



.payment-card\_\_name {

&#x20; font-size: var(--font-size-sm);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.1em;

}



.payment-card\_\_logo {

&#x20; position: absolute;

&#x20; inset-block-end: var(--space-5);

&#x20; inset-inline-end: var(--space-5);

&#x20; width: 3rem;

&#x20; opacity: 0.8;

}

```



\### 93.3 Star Rating



```css

/\* ─── CSS-only interactive star rating ─── \*/

.star-rating {

&#x20; display: flex;

&#x20; flex-direction: row-reverse;  /\* reverse for :checked \~ sibling trick \*/

&#x20; gap: 0.125rem;

&#x20; width: fit-content;

}



.star-rating input {

&#x20; position: absolute;

&#x20; opacity: 0;

&#x20; width: 0;

&#x20; height: 0;

}



.star-rating label {

&#x20; font-size: 1.5rem;

&#x20; color: var(--color-border-strong);

&#x20; cursor: pointer;

&#x20; transition: color var(--duration-fast), scale var(--duration-fast) var(--ease-bounce);

&#x20; line-height: 1;

}



/\* Highlight on hover — all stars before (visually after in RTL flex) \*/

.star-rating label:hover,

.star-rating label:hover \~ label {

&#x20; color: var(--color-warning-500);

&#x20; scale: 1.1;

}



/\* Highlight checked and before \*/

.star-rating input:checked \~ label {

&#x20; color: var(--color-warning-500);

}



/\* ─── Read-only star display ─── \*/

.stars-display {

&#x20; display: inline-flex;

&#x20; gap: 1px;

&#x20; color: var(--color-border);

&#x20; font-size: 1rem;

&#x20; position: relative;

}



/\* Filled stars via clip \*/

.stars-display::before {

&#x20; content: '★★★★★';

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; color: var(--color-warning-500);

&#x20; overflow: hidden;

&#x20; width: calc(var(--rating, 0) / 5 \* 100%);

&#x20; white-space: nowrap;

}



.stars-display::after {

&#x20; content: '★★★★★';

}



/\* ─── Rating with count ─── \*/

.rating-summary {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

}



.rating-average {

&#x20; font-size: var(--font-size-2xl);

&#x20; font-weight: var(--font-weight-black);

&#x20; font-variant-numeric: tabular-nums;

&#x20; line-height: 1;

}



.rating-count {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

}



/\* Rating bars breakdown \*/

.rating-bars {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-1);

&#x20; flex: 1;

}



.rating-bar-row {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



.rating-bar {

&#x20; flex: 1;

&#x20; height: 6px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

}



.rating-bar\_\_fill {

&#x20; height: 100%;

&#x20; background: var(--color-warning-500);

&#x20; border-radius: inherit;

&#x20; width: var(--pct, 0%);

&#x20; transition: width 0.6s var(--ease-out);

}

```



\### 93.4 Pagination



```css

/\* ─── Pagination ─── \*/

.pagination {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-1);

&#x20; flex-wrap: wrap;

}



.page-btn {

&#x20; min-width: 2.25rem;

&#x20; height: 2.25rem;

&#x20; padding-inline: 0.5rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-surface);

&#x20; color: var(--color-text);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; font-variant-numeric: tabular-nums;

&#x20; cursor: pointer;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; gap: var(--space-1);

&#x20; transition:

&#x20;   background      var(--duration-fast),

&#x20;   border-color    var(--duration-fast),

&#x20;   color           var(--duration-fast);

}



.page-btn:hover {

&#x20; background: var(--color-bg-subtle);

&#x20; border-color: var(--color-neutral-400);

}



.page-btn\[aria-current="page"],

.page-btn.active {

&#x20; background: var(--color-accent);

&#x20; border-color: var(--color-accent);

&#x20; color: white;

&#x20; font-weight: var(--font-weight-semibold);

}



.page-btn:disabled {

&#x20; opacity: 0.4;

&#x20; cursor: not-allowed;

&#x20; pointer-events: none;

}



.page-ellipsis {

&#x20; min-width: 2.25rem;

&#x20; height: 2.25rem;

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; letter-spacing: 0.1em;

}



/\* Compact pagination \*/

.pagination-compact {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; font-size: var(--font-size-sm);

}



.pagination-compact\_\_info {

&#x20; color: var(--color-text-muted);

&#x20; white-space: nowrap;

}



/\* ─── Infinite scroll trigger ─── \*/

.load-more-trigger {

&#x20; display: flex;

&#x20; justify-content: center;

&#x20; padding: var(--space-8);

&#x20; visibility: hidden;  /\* JS observes and shows \*/

}



.load-more-trigger\[data-visible] {

&#x20; visibility: visible;

}

```



\---



\## 94. SOCIAL \& CHAT UI PATTERNS



\### 94.1 Chat Interface



```css

/\* ─── Chat layout ─── \*/

.chat-layout {

&#x20; display: grid;

&#x20; grid-template-rows: auto 1fr auto;

&#x20; height: 100dvh;

&#x20; max-height: 700px;

&#x20; background: var(--color-bg-subtle);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-2xl);

&#x20; overflow: hidden;

}



/\* Chat header \*/

.chat-header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-4) var(--space-5);

&#x20; background: var(--color-surface);

&#x20; border-bottom: 1px solid var(--color-border);

}



.chat-header\_\_avatar {

&#x20; position: relative;

&#x20; flex-shrink: 0;

}



.chat-header\_\_avatar img {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

}



/\* Online dot \*/

.chat-header\_\_avatar::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; bottom: 1px;

&#x20; right: 1px;

&#x20; width: 10px;

&#x20; height: 10px;

&#x20; background: var(--color-success-500);

&#x20; border-radius: 50%;

&#x20; border: 2px solid var(--color-surface);

}



/\* Messages area \*/

.chat-messages {

&#x20; overflow-y: auto;

&#x20; padding: var(--space-4) var(--space-5);

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-3);

&#x20; overscroll-behavior: contain;

&#x20; scroll-behavior: smooth;

&#x20; scrollbar-width: thin;

}



/\* Message bubble \*/

.message {

&#x20; display: flex;

&#x20; align-items: flex-end;

&#x20; gap: var(--space-2);

&#x20; max-width: 75%;

&#x20; animation: message-appear 0.2s var(--ease-out);

}



@keyframes message-appear {

&#x20; from { opacity: 0; translate: 0 8px; }

}



.message--outgoing {

&#x20; align-self: flex-end;

&#x20; flex-direction: row-reverse;

}



.message\_\_avatar {

&#x20; width: 1.75rem;

&#x20; height: 1.75rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

&#x20; flex-shrink: 0;

&#x20; align-self: flex-end;

}



.message\_\_bubble {

&#x20; padding: 0.625rem 0.875rem;

&#x20; border-radius: var(--radius-xl);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.5;

&#x20; position: relative;

&#x20; max-width: 100%;

&#x20; word-break: break-word;

}



/\* Incoming \*/

.message--incoming .message\_\_bubble {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-start-start-radius: var(--radius-sm);

&#x20; color: var(--color-text);

}



/\* Outgoing \*/

.message--outgoing .message\_\_bubble {

&#x20; background: var(--color-accent);

&#x20; border-start-end-radius: var(--radius-sm);

&#x20; color: white;

}



/\* Message status \*/

.message\_\_meta {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-subtle);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25rem;

&#x20; padding-block-end: 0.125rem;

}



.message--outgoing .message\_\_meta {

&#x20; justify-content: flex-end;

}



/\* Date separator \*/

.chat-date {

&#x20; text-align: center;

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-subtle);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; margin-block: var(--space-2);

}



.chat-date::before,

.chat-date::after {

&#x20; content: '';

&#x20; flex: 1;

&#x20; height: 1px;

&#x20; background: var(--color-border);

}



/\* Typing indicator in chat \*/

.typing-bubble {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.25rem;

&#x20; padding: 0.625rem 0.875rem;

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; border-start-start-radius: var(--radius-sm);

&#x20; width: fit-content;

&#x20; animation: message-appear 0.2s var(--ease-out);

}



.typing-bubble span {

&#x20; width: 6px;

&#x20; height: 6px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-text-muted);

&#x20; animation: typing 1.4s ease-in-out infinite;

}

.typing-bubble span:nth-child(2) { animation-delay: 0.2s; }

.typing-bubble span:nth-child(3) { animation-delay: 0.4s; }



@keyframes typing {

&#x20; 0%, 60%, 100% { translate: 0; opacity: 0.4; }

&#x20; 30%           { translate: 0 -4px; opacity: 1; }

}



/\* Chat input \*/

.chat-input-area {

&#x20; padding: var(--space-4) var(--space-5);

&#x20; background: var(--color-surface);

&#x20; border-top: 1px solid var(--color-border);

&#x20; display: flex;

&#x20; gap: var(--space-3);

&#x20; align-items: flex-end;

}



.chat-input {

&#x20; flex: 1;

&#x20; padding: 0.625rem 0.875rem;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; background: var(--color-bg-subtle);

&#x20; font: inherit;

&#x20; font-size: var(--font-size-sm);

&#x20; outline: none;

&#x20; resize: none;

&#x20; max-height: 120px;

&#x20; overflow-y: auto;

&#x20; line-height: 1.5;

&#x20; transition: border-color var(--duration-fast);

}



.chat-input:focus {

&#x20; border-color: var(--color-accent);

&#x20; background: var(--color-surface);

}

```



\### 94.2 Social Feed



```css

/\* ─── Social post card ─── \*/

.post {

&#x20; background: var(--color-surface);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

}



.post\_\_header {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-4);

}



.post\_\_avatar {

&#x20; width: 2.5rem;

&#x20; height: 2.5rem;

&#x20; border-radius: 50%;

&#x20; object-fit: cover;

&#x20; flex-shrink: 0;

}



.post\_\_author {

&#x20; flex: 1;

&#x20; min-width: 0;

}



.post\_\_name {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-sm);

}



.post\_\_meta {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



.post\_\_menu {

&#x20; margin-inline-start: auto;

&#x20; color: var(--color-text-muted);

&#x20; background: none;

&#x20; border: none;

&#x20; cursor: pointer;

&#x20; padding: var(--space-1);

&#x20; border-radius: var(--radius-md);

}



.post\_\_content {

&#x20; padding: 0 var(--space-4) var(--space-4);

&#x20; font-size: var(--font-size-sm);

&#x20; line-height: 1.6;

}



.post\_\_content a {

&#x20; color: var(--color-accent);

}



/\* Hashtags \*/

.post\_\_content .hashtag {

&#x20; color: var(--color-accent);

&#x20; cursor: pointer;

}



/\* Media grid \*/

.post\_\_media {

&#x20; display: grid;

&#x20; gap: 2px;

}



.post\_\_media--1 { grid-template-columns: 1fr; }

.post\_\_media--2 { grid-template-columns: 1fr 1fr; }

.post\_\_media--3 {

&#x20; grid-template-columns: 2fr 1fr;

&#x20; grid-template-rows: 1fr 1fr;

}

.post\_\_media--3 .media-item:first-child { grid-row: span 2; }

.post\_\_media--4 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }



.media-item {

&#x20; aspect-ratio: 1;

&#x20; overflow: hidden;

&#x20; cursor: pointer;

&#x20; position: relative;

}



/\* More overlay for 4+ images \*/

.media-item--more::after {

&#x20; content: '+' attr(data-count);

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; background: rgb(0 0 0 / 0.5);

&#x20; color: white;

&#x20; font-size: var(--font-size-2xl);

&#x20; font-weight: var(--font-weight-bold);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

}



.media-item img,

.media-item video {

&#x20; width: 100%;

&#x20; height: 100%;

&#x20; object-fit: cover;

&#x20; transition: scale var(--duration-slow) var(--ease-out);

}



.media-item:hover img { scale: 1.03; }



/\* Post actions \*/

.post\_\_actions {

&#x20; display: flex;

&#x20; padding: var(--space-2) var(--space-4);

&#x20; gap: var(--space-1);

&#x20; border-top: 1px solid var(--color-border);

}



.post-action {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: 0.375rem;

&#x20; padding: var(--space-2) var(--space-3);

&#x20; border: none;

&#x20; background: none;

&#x20; cursor: pointer;

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-sm);

&#x20; font: inherit;

&#x20; border-radius: var(--radius-md);

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

&#x20; flex: 1;

&#x20; justify-content: center;

}



.post-action:hover {

&#x20; background: var(--color-bg-subtle);

&#x20; color: var(--color-text);

}



.post-action--liked {

&#x20; color: var(--color-danger-500);

&#x20; animation: like-action 0.3s var(--ease-bounce);

}



@keyframes like-action {

&#x20; 0%   { scale: 0.8; }

&#x20; 60%  { scale: 1.2; }

&#x20; 100% { scale: 1; }

}



/\* Comment count animation \*/

.post-action\_\_count {

&#x20; font-variant-numeric: tabular-nums;

&#x20; font-weight: var(--font-weight-medium);

}

```



\---



\## 95. CSS ANIMATION: PARTICLE \& SPECIAL EFFECTS



\### 95.1 CSS Confetti



```css

/\* ─── CSS Confetti (via many pseudo-elements + JS class for each piece) ─── \*/

.confetti-piece {

&#x20; position: fixed;

&#x20; width: 10px;

&#x20; height: 10px;

&#x20; top: -10px;

&#x20; left: var(--x, 50%);

&#x20; background: var(--color, oklch(0.7 0.3 var(--hue, 0)));

&#x20; border-radius: var(--shape, 2px);

&#x20; animation:

&#x20;   confetti-fall    var(--duration, 3s) var(--ease, ease-in) var(--delay, 0s) forwards,

&#x20;   confetti-wobble  var(--wobble, 0.5s) ease-in-out infinite alternate;

&#x20; opacity: 0;

}



@keyframes confetti-fall {

&#x20; 0%   { translate: 0 0; opacity: 1; rotate: 0deg; }

&#x20; 100% { translate: var(--drift, 50px) 110dvh; opacity: 0; rotate: var(--spin, 360deg); }

}



@keyframes confetti-wobble {

&#x20; from { translate: -5px 0; }

&#x20; to   { translate: 5px 0; }

}



/\* ─── CSS Sparkle effect ─── \*/

.sparkle {

&#x20; position: relative;

&#x20; display: inline-block;

}



.sparkle::before,

.sparkle::after {

&#x20; content: '✦';

&#x20; position: absolute;

&#x20; font-size: 0.5em;

&#x20; animation: sparkle-blink 1.5s ease-in-out infinite;

&#x20; color: var(--color-warning-400);

}



.sparkle::before {

&#x20; top: -0.5em;

&#x20; right: -0.5em;

&#x20; animation-delay: 0s;

}

.sparkle::after {

&#x20; bottom: -0.25em;

&#x20; left: -0.25em;

&#x20; animation-delay: 0.75s;

&#x20; font-size: 0.35em;

}



@keyframes sparkle-blink {

&#x20; 0%, 100% { opacity: 0; scale: 0.5; }

&#x20; 50%       { opacity: 1; scale: 1; }

}



/\* ─── Firework burst ─── \*/

@keyframes firework-burst {

&#x20; 0%   { width: 0; height: 0; opacity: 1; }

&#x20; 100% { width: 200px; height: 200px; opacity: 0; margin: -100px; }

}



.firework {

&#x20; position: fixed;

&#x20; left: var(--x);

&#x20; top: var(--y);

&#x20; width: 4px;

&#x20; height: 4px;

&#x20; background: transparent;

&#x20; border-radius: 50%;

&#x20; box-shadow:

&#x20;   0 0 0 2px var(--c1, oklch(0.8 0.3 0)),

&#x20;   0 0 0 4px var(--c2, oklch(0.8 0.3 120)),

&#x20;   0 0 0 6px var(--c3, oklch(0.8 0.3 240));

&#x20; animation: firework-burst 0.6s ease-out forwards;

}



/\* ─── Glow pulse ─── \*/

@keyframes glow-pulse {

&#x20; 0%, 100% {

&#x20;   box-shadow:

&#x20;     0 0 5px var(--glow-color),

&#x20;     0 0 10px var(--glow-color),

&#x20;     0 0 20px var(--glow-color);

&#x20; }

&#x20; 50% {

&#x20;   box-shadow:

&#x20;     0 0 10px var(--glow-color),

&#x20;     0 0 25px var(--glow-color),

&#x20;     0 0 50px var(--glow-color);

&#x20; }

}



.glow-element {

&#x20; --glow-color: var(--color-accent);

&#x20; animation: glow-pulse 2s ease-in-out infinite;

}



/\* ─── Matrix rain (CSS only, limited) ─── \*/

.matrix-column {

&#x20; position: absolute;

&#x20; top: -100%;

&#x20; font-family: monospace;

&#x20; color: #0f0;

&#x20; text-shadow: 0 0 8px #0f0;

&#x20; font-size: 14px;

&#x20; line-height: 1.4;

&#x20; animation: matrix-fall var(--duration, 3s) linear var(--delay, 0s) infinite;

&#x20; white-space: nowrap;

}



@keyframes matrix-fall {

&#x20; from { translate: 0 0; opacity: 0.8; }

&#x20; to   { translate: 0 200vh; opacity: 0; }

}

```



\### 95.2 CSS Art Techniques



```css

/\* ─── CSS-only illustrations (no images) ─── \*/



/\* Sun \*/

.css-sun {

&#x20; --size: 80px;

&#x20; width: var(--size);

&#x20; height: var(--size);

&#x20; background: radial-gradient(circle, #FFD700 40%, #FF8C00 100%);

&#x20; border-radius: 50%;

&#x20; box-shadow:

&#x20;   0 0 0 8px #FF8C00,

&#x20;   0 0 0 12px rgba(255 200 0 / 0.3),

&#x20;   /\* Rays \*/

&#x20;   0 -55px 0 -5px #FF8C00,

&#x20;   55px 0 0 -5px #FF8C00,

&#x20;   0 55px 0 -5px #FF8C00,

&#x20;   -55px 0 0 -5px #FF8C00,

&#x20;   40px -40px 0 -5px #FF8C00,

&#x20;   40px 40px 0 -5px #FF8C00,

&#x20;   -40px 40px 0 -5px #FF8C00,

&#x20;   -40px -40px 0 -5px #FF8C00;

&#x20; animation: sun-rotate 10s linear infinite;

}



@keyframes sun-rotate {

&#x20; to { rotate: 360deg; }

}



/\* Moon \*/

.css-moon {

&#x20; width: 80px;

&#x20; height: 80px;

&#x20; background: #f5e642;

&#x20; border-radius: 50%;

&#x20; box-shadow: inset -20px -5px 0 0 #d4b800;

}



/\* Cloud \*/

.css-cloud {

&#x20; width: 120px;

&#x20; height: 50px;

&#x20; background: white;

&#x20; border-radius: 25px;

&#x20; position: relative;

&#x20; box-shadow: 0 4px 12px rgba(0 0 0 / 0.1);

}



.css-cloud::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; width: 60px;

&#x20; height: 60px;

&#x20; background: white;

&#x20; border-radius: 50%;

&#x20; top: -30px;

&#x20; left: 20px;

}



.css-cloud::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; width: 40px;

&#x20; height: 40px;

&#x20; background: white;

&#x20; border-radius: 50%;

&#x20; top: -20px;

&#x20; left: 55px;

}



/\* Heart \*/

.css-heart {

&#x20; --size: 60px;

&#x20; position: relative;

&#x20; width: var(--size);

&#x20; height: var(--size);

&#x20; background: #ff4d6d;

&#x20; transform: rotate(-45deg);

}

.css-heart::before,

.css-heart::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; width: var(--size);

&#x20; height: var(--size);

&#x20; background: inherit;

&#x20; border-radius: 50%;

}

.css-heart::before { top: calc(var(--size) \* -0.5); left: 0; }

.css-heart::after  { top: 0; left: calc(var(--size) \* 0.5); }



/\* Loader as art: orbiting dots \*/

.orbit {

&#x20; --size: 60px;

&#x20; width: var(--size);

&#x20; height: var(--size);

&#x20; position: relative;

&#x20; animation: orbit-spin 2s linear infinite;

}



.orbit::before,

.orbit::after {

&#x20; content: '';

&#x20; position: absolute;

&#x20; width: 12px;

&#x20; height: 12px;

&#x20; border-radius: 50%;

&#x20; background: var(--color-accent);

}

.orbit::before { top: 0; left: 50%; translate: -50%; }

.orbit::after  { bottom: 0; left: 50%; translate: -50%; opacity: 0.5; }



@keyframes orbit-spin { to { rotate: 360deg; } }

```



\---



\## 96. DOCUMENTATION SITE PATTERNS



\### 96.1 Table of Contents / Sidebar Nav



```css

/\* ─── Docs layout ─── \*/

.docs-layout {

&#x20; display: grid;

&#x20; grid-template-columns: 260px 1fr 220px;

&#x20; gap: 0;

&#x20; min-height: 100dvh;

}



@media (max-width: 1024px) {

&#x20; .docs-layout {

&#x20;   grid-template-columns: 240px 1fr;

&#x20; }

&#x20; .docs-toc { display: none; }

}



@media (max-width: 768px) {

&#x20; .docs-layout {

&#x20;   grid-template-columns: 1fr;

&#x20; }

&#x20; .docs-sidebar { display: none; }

}



/\* Left sidebar \*/

.docs-sidebar {

&#x20; border-right: 1px solid var(--color-border);

&#x20; padding: var(--space-6) var(--space-4);

&#x20; position: sticky;

&#x20; top: var(--header-height, 60px);

&#x20; height: calc(100dvh - var(--header-height, 60px));

&#x20; overflow-y: auto;

&#x20; scrollbar-width: thin;

}



.docs-sidebar-section {

&#x20; margin-block-end: var(--space-6);

}



.docs-sidebar-title {

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; margin-block-end: var(--space-2);

&#x20; padding-inline: var(--space-3);

}



.docs-nav-link {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: 0.375rem var(--space-3);

&#x20; border-radius: var(--radius-md);

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: none;

&#x20; transition: background var(--duration-fast), color var(--duration-fast);

&#x20; position: relative;

}



.docs-nav-link:hover {

&#x20; background: var(--color-bg-subtle);

&#x20; color: var(--color-text);

}



.docs-nav-link\[aria-current="page"] {

&#x20; color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 8%, transparent);

&#x20; font-weight: var(--font-weight-medium);

}



/\* Active left border \*/

.docs-nav-link\[aria-current="page"]::before {

&#x20; content: '';

&#x20; position: absolute;

&#x20; inset-inline-start: 0;

&#x20; inset-block: 4px;

&#x20; width: 2px;

&#x20; background: var(--color-accent);

&#x20; border-radius: var(--radius-full);

}



/\* Nested nav items \*/

.docs-nav-sub {

&#x20; padding-inline-start: var(--space-5);

&#x20; display: none;

}



.docs-nav-link\[aria-expanded="true"] \~ .docs-nav-sub {

&#x20; display: block;

}



/\* Right TOC \*/

.docs-toc {

&#x20; padding: var(--space-6) var(--space-4);

&#x20; position: sticky;

&#x20; top: var(--header-height, 60px);

&#x20; height: calc(100dvh - var(--header-height, 60px));

&#x20; overflow-y: auto;

&#x20; border-left: 1px solid var(--color-border);

&#x20; font-size: var(--font-size-xs);

}



.docs-toc-title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wider);

&#x20; color: var(--color-text-muted);

&#x20; font-size: var(--font-size-xs);

&#x20; margin-block-end: var(--space-3);

}



.docs-toc-link {

&#x20; display: block;

&#x20; padding: 0.25rem 0;

&#x20; color: var(--color-text-muted);

&#x20; text-decoration: none;

&#x20; border-inline-start: 2px solid transparent;

&#x20; padding-inline-start: var(--space-3);

&#x20; transition: color var(--duration-fast), border-color var(--duration-fast);

&#x20; line-height: 1.4;

}



.docs-toc-link:hover { color: var(--color-text); }

.docs-toc-link.active {

&#x20; color: var(--color-accent);

&#x20; border-color: var(--color-accent);

}



.docs-toc-link\[data-level="3"] { padding-inline-start: var(--space-6); }

.docs-toc-link\[data-level="4"] { padding-inline-start: var(--space-9); }

```



\### 96.2 Code Documentation Styles



```css

/\* ─── API parameter table ─── \*/

.param-table {

&#x20; width: 100%;

&#x20; border-collapse: collapse;

&#x20; font-size: var(--font-size-sm);

&#x20; margin-block: var(--space-6);

&#x20; overflow-x: auto;

&#x20; display: block;

}



.param-table th {

&#x20; text-align: start;

&#x20; padding: var(--space-3) var(--space-4);

&#x20; background: var(--color-bg-subtle);

&#x20; font-weight: var(--font-weight-semibold);

&#x20; font-size: var(--font-size-xs);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: var(--letter-spacing-wide);

&#x20; color: var(--color-text-muted);

&#x20; border-bottom: 1px solid var(--color-border);

}



.param-table td {

&#x20; padding: var(--space-3) var(--space-4);

&#x20; border-bottom: 1px solid var(--color-border);

&#x20; vertical-align: top;

}



/\* Type tag \*/

.param-type {

&#x20; display: inline-flex;

&#x20; padding: 0.1em 0.5em;

&#x20; background: var(--color-brand-100);

&#x20; color: var(--color-brand-700);

&#x20; border-radius: var(--radius-sm);

&#x20; font-family: var(--font-mono);

&#x20; font-size: 0.85em;

&#x20; white-space: nowrap;

}



.param-type--string  { background: var(--color-success-100); color: var(--color-success-900); }

.param-type--number  { background: var(--color-warning-100); color: var(--color-warning-900); }

.param-type--boolean { background: var(--color-danger-100);  color: var(--color-danger-900); }

.param-type--object  { background: var(--color-brand-100);   color: var(--color-brand-900); }

.param-type--array   { background: var(--color-neutral-100); color: var(--color-neutral-800); }



/\* Required badge \*/

.param-required {

&#x20; display: inline-flex;

&#x20; padding: 0.1em 0.4em;

&#x20; background: var(--color-danger-100);

&#x20; color: var(--color-danger-700);

&#x20; border-radius: var(--radius-sm);

&#x20; font-size: 0.75em;

&#x20; font-weight: var(--font-weight-bold);

&#x20; text-transform: uppercase;

&#x20; letter-spacing: 0.05em;

&#x20; margin-inline-start: 0.375em;

}



/\* ─── Version badge ─── \*/

.version-badge {

&#x20; display: inline-flex;

&#x20; align-items: center;

&#x20; gap: 0.375rem;

&#x20; padding: 0.2em 0.6em;

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-full);

&#x20; font-size: var(--font-size-xs);

&#x20; font-family: var(--font-mono);

&#x20; color: var(--color-text-muted);

&#x20; background: var(--color-surface);

}



.version-badge--new     { border-color: var(--color-success-300); color: var(--color-success-700); background: var(--color-success-100); }

.version-badge--deprecated { border-color: var(--color-warning-300); color: var(--color-warning-700); background: var(--color-warning-100); }

.version-badge--removed { border-color: var(--color-danger-300); color: var(--color-danger-700); background: var(--color-danger-100); }



/\* ─── Live demo box ─── \*/

.demo-box {

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-xl);

&#x20; overflow: hidden;

}



.demo-box\_\_preview {

&#x20; padding: var(--space-8);

&#x20; background: var(--color-bg-subtle);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; min-height: 160px;

}



.demo-box\_\_code {

&#x20; border-top: 1px solid var(--color-border);

&#x20; background: var(--code-bg, #1e1e1e);

&#x20; position: relative;

}



.demo-box\_\_toolbar {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-2);

&#x20; padding: var(--space-2) var(--space-4);

&#x20; background: rgba(255 255 255 / 0.05);

&#x20; border-bottom: 1px solid rgba(255 255 255 / 0.1);

}



.demo-box\_\_lang {

&#x20; font-size: var(--font-size-xs);

&#x20; color: rgba(255 255 255 / 0.5);

&#x20; font-family: var(--font-mono);

&#x20; margin-inline-end: auto;

}

```



\---



\## 97. ADVANCED FORM PATTERNS



\### 97.1 Multi-step Form / Wizard



```css

/\* ─── Step form ─── \*/

.wizard {

&#x20; display: grid;

&#x20; gap: var(--space-8);

}



.wizard\_\_step {

&#x20; display: none;

&#x20; animation: step-enter 0.3s var(--ease-out);

}



.wizard\_\_step.active { display: block; }

.wizard\_\_step.exiting {

&#x20; display: block;

&#x20; animation: step-exit 0.2s var(--ease-in) forwards;

}



@keyframes step-enter {

&#x20; from { opacity: 0; translate: 30px 0; }

}

@keyframes step-exit {

&#x20; to { opacity: 0; translate: -30px 0; }

}



/\* ─── Form field group patterns ─── \*/

.field-row {

&#x20; display: grid;

&#x20; grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr));

&#x20; gap: var(--space-4);

}



/\* ─── OTP / PIN input ─── \*/

.otp-input {

&#x20; display: flex;

&#x20; gap: var(--space-3);

&#x20; justify-content: center;

}



.otp-digit {

&#x20; width: 3rem;

&#x20; height: 3.5rem;

&#x20; text-align: center;

&#x20; font-size: var(--font-size-xl);

&#x20; font-weight: var(--font-weight-bold);

&#x20; font-variant-numeric: tabular-nums;

&#x20; border: 2px solid var(--color-border-strong);

&#x20; border-radius: var(--radius-lg);

&#x20; background: var(--color-surface);

&#x20; outline: none;

&#x20; caret-color: var(--color-accent);

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   box-shadow   var(--duration-fast);

}



.otp-digit:focus {

&#x20; border-color: var(--color-accent);

&#x20; box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-accent) 20%, transparent);

}



.otp-digit.filled {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 5%, var(--color-surface));

}



/\* ─── Credit card form ─── \*/

.cc-form {

&#x20; display: grid;

&#x20; gap: var(--space-4);

}



.cc-number-input {

&#x20; letter-spacing: 0.15em;

&#x20; font-family: var(--font-mono);

}



.cc-form-row {

&#x20; display: grid;

&#x20; grid-template-columns: 2fr 1fr;

&#x20; gap: var(--space-4);

}



/\* ─── File upload zone ─── \*/

.file-upload {

&#x20; border: 2px dashed var(--color-border-strong);

&#x20; border-radius: var(--radius-xl);

&#x20; padding: var(--space-10);

&#x20; text-align: center;

&#x20; cursor: pointer;

&#x20; transition:

&#x20;   border-color var(--duration-fast),

&#x20;   background   var(--duration-fast),

&#x20;   scale        var(--duration-fast) var(--ease-bounce);

&#x20; position: relative;

}



.file-upload input\[type="file"] {

&#x20; position: absolute;

&#x20; inset: 0;

&#x20; opacity: 0;

&#x20; cursor: pointer;

&#x20; width: 100%;

&#x20; height: 100%;

}



.file-upload:hover,

.file-upload:focus-within {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 5%, transparent);

}



.file-upload.dragging {

&#x20; border-color: var(--color-accent);

&#x20; background: color-mix(in srgb, var(--color-accent) 10%, transparent);

&#x20; scale: 1.01;

}



.file-upload\_\_icon {

&#x20; font-size: 3rem;

&#x20; margin-block-end: var(--space-3);

&#x20; color: var(--color-text-muted);

&#x20; transition: scale var(--duration-fast) var(--ease-bounce);

}



.file-upload.dragging .file-upload\_\_icon { scale: 1.2; }



.file-upload\_\_title {

&#x20; font-weight: var(--font-weight-semibold);

&#x20; margin-block-end: var(--space-1);

}



.file-upload\_\_subtitle {

&#x20; font-size: var(--font-size-sm);

&#x20; color: var(--color-text-muted);

}



/\* Uploaded files list \*/

.file-list {

&#x20; display: flex;

&#x20; flex-direction: column;

&#x20; gap: var(--space-2);

&#x20; margin-block-start: var(--space-4);

}



.file-item {

&#x20; display: flex;

&#x20; align-items: center;

&#x20; gap: var(--space-3);

&#x20; padding: var(--space-3);

&#x20; background: var(--color-bg-subtle);

&#x20; border: 1px solid var(--color-border);

&#x20; border-radius: var(--radius-lg);

&#x20; animation: file-appear 0.2s var(--ease-out);

}



@keyframes file-appear {

&#x20; from { opacity: 0; translate: 0 -6px; }

}



.file-item\_\_icon {

&#x20; width: 2rem;

&#x20; height: 2rem;

&#x20; border-radius: var(--radius-md);

&#x20; background: var(--color-brand-100);

&#x20; display: flex;

&#x20; align-items: center;

&#x20; justify-content: center;

&#x20; color: var(--color-accent);

&#x20; flex-shrink: 0;

&#x20; font-size: var(--font-size-xs);

&#x20; font-weight: var(--font-weight-bold);

}



.file-item\_\_info { flex: 1; min-width: 0; }



.file-item\_\_name {

&#x20; font-size: var(--font-size-sm);

&#x20; font-weight: var(--font-weight-medium);

&#x20; overflow: hidden;

&#x20; text-overflow: ellipsis;

&#x20; white-space: nowrap;

}



.file-item\_\_size {

&#x20; font-size: var(--font-size-xs);

&#x20; color: var(--color-text-muted);

}



/\* Upload progress \*/

.file-item\_\_progress {

&#x20; height: 3px;

&#x20; background: var(--color-bg-muted);

&#x20; border-radius: var(--radius-full);

&#x20; overflow: hidden;

&#x20; margin-block-start: var(--space-1);

}



.file-item\_\_progress-bar {

&#x20; height: 100%;

&#x20; background: var(--color-accent);

&#x20; border-radius: inherit;

&#x20; width: var(--progress, 0%);

&#x20; transition: width 0.2s var(--ease-out);

}

```



\---



\## 98. CSS CUSTOM SCROLLBAR LIBRARY



```css

/\* ─── Scrollbar token system ─── \*/

:root {

&#x20; --scrollbar-width: 6px;

&#x20; --scrollbar-track: transparent;

&#x20; --scrollbar-thumb: var(--color-border-strong);

&#x20; --scrollbar-thumb-hover: var(--color-text-muted);

&#x20; --scrollbar-radius: var(--radius-full);

}



/\* ─── Firefox (standard) ─── \*/

.custom-scroll {

&#x20; scrollbar-width: thin;

&#x20; scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);

}



/\* ─── WebKit ─── \*/

.custom-scroll::-webkit-scrollbar {

&#x20; width: var(--scrollbar-width);

&#x20; height: var(--scrollbar-width);

}



.custom-scroll::-webkit-scrollbar-track {

&#x20; background: var(--scrollbar-track);

&#x20; border-radius: var(--scrollbar-radius);

}



.custom-scroll::-webkit-scrollbar-thumb {

&#x20; background: var(--scrollbar-thumb);

&#x20; border-radius: var(--scrollbar-radius);

&#x20; transition: background var(--duration-fast);

}



.custom-scroll::-webkit-scrollbar-thumb:hover {

&#x20; background: var(--scrollbar-thumb-hover);

}



.custom-scroll::-webkit-scrollbar-corner {

&#x20; background: transparent;

}



/\* ─── Preset variants ─── \*/

.scroll-thin {

&#x20; --scrollbar-width: 4px;

}



.scroll-hidden {

&#x20; scrollbar-width: none;

}

.scroll-hidden::-webkit-scrollbar { display: none; }



.scroll-brand {

&#x20; --scrollbar-thumb: var(--color-accent);

&#x20; --scrollbar-thumb-hover: var(--color-accent-hover);

&#x20; --scrollbar-track: color-mix(in srgb, var(--color-accent) 10%, transparent);

}



.scroll-dark {

&#x20; --scrollbar-thumb: #555;

&#x20; --scrollbar-thumb-hover: #777;

&#x20; --scrollbar-track: #2a2a2a;

}



.scroll-light {

&#x20; --scrollbar-thumb: #ddd;

&#x20; --scrollbar-thumb-hover: #bbb;

&#x20; --scrollbar-track: #f5f5f5;

}



/\* Overlay scrollbar (doesn't take space) \*/

.scroll-overlay {

&#x20; overflow: overlay;  /\* Chrome only, fallback to auto \*/

&#x20; overflow: auto;

}



/\* ─── macOS-style auto-hiding scrollbar ─── \*/

.scroll-macos {

&#x20; scrollbar-width: thin;

&#x20; scrollbar-color: transparent transparent;

&#x20; transition: scrollbar-color var(--duration-slow);

}



.scroll-macos:hover {

&#x20; scrollbar-color: var(--scrollbar-thumb) transparent;

}



.scroll-macos::-webkit-scrollbar { width: 8px; }

.scroll-macos::-webkit-scrollbar-thumb {

&#x20; background: transparent;

&#x20; border-radius: 4px;

&#x20; border: 2px solid transparent;

&#x20; background-clip: content-box;

&#x20; transition: background var(--duration-slow);

}

.scroll-macos:hover::-webkit-scrollbar-thumb {

&#x20; background-color: rgba(0 0 0 / 0.25);

}

```



\---



\## 99. CSS SPECIFICITY — BATTLE-TESTED SOLUTIONS



\### 99.1 Specificity Conflict Resolution Patterns



```css

/\* ─── Pattern 1: The @layer override ─── \*/

@layer base, components, overrides;



@layer base {

&#x20; .text { color: var(--color-text); }

}



@layer components {

&#x20; .card .text { color: var(--color-text-muted); }  /\* 0-2-0 \*/

}



@layer overrides {

&#x20; /\* This wins even with lower specificity because overrides > components \*/

&#x20; .text-accent { color: var(--color-accent); }  /\* 0-1-0 \*/

}



/\* ─── Pattern 2: :where() to drop specificity ─── \*/

/\* Problem: library component has too-high specificity \*/

:is(.nav, .sidebar, .footer) .link {  /\* 0-2-0 — hard to override \*/

&#x20; color: var(--color-accent);

}



/\* ✅ Rewrite with :where() \*/

:where(.nav, .sidebar, .footer) .link {  /\* 0-1-0 — easy to override \*/

&#x20; color: var(--color-accent);

}



/\* ─── Pattern 3: Isolation with data attributes ─── \*/

/\* Use data attributes instead of class nesting to avoid specificity stacking \*/

.card { }                      /\* 0-1-0 \*/

.card\[data-variant="featured"] { }  /\* 0-1-1 — still manageable \*/



/\* vs \*/

.card.card--featured { }       /\* 0-2-0 — requires another class to beat \*/



/\* ─── Pattern 4: The !important escape hatch (scoped) ─── \*/

/\* Never globally, but acceptable in these cases: \*/



/\* 1. Utility classes \*/

@layer utilities {

&#x20; .hidden { display: none !important; }

&#x20; .sr-only { position: absolute !important; }

&#x20; .text-center { text-align: center !important; }

}



/\* 2. Forced states \*/

\[aria-hidden="true"] { display: none !important; }



/\* 3. Animation endpoints \*/

.animate-to-end { /\* JS toggles this \*/

&#x20; transform: translateX(100%) !important;

}



/\* ─── Pattern 5: Double-class trick (without @layer) ─── \*/

/\* Increase specificity without IDs \*/

.btn.btn { color: blue; }       /\* 0-2-0 \*/

.btn.btn.btn { color: green; }  /\* 0-3-0 — use sparingly \*/



/\* ─── Pattern 6: Specificity graph checking ─── \*/

/\*

A healthy specificity graph should be flat or slowly increasing.

Use this mental model:

&#x20; All selectors in 0-0-x zone: element tags

&#x20; All selectors in 0-1-x zone: classes (preferred)

&#x20; Avoid 1-x-x zone: IDs

&#x20; Avoid 0-0-0 with !important: only utilities



Red flags:

&#x20; Many 1-x-x selectors (too many IDs)

&#x20; Zigzag specificity (increasing then decreasing)

&#x20; Heavy !important usage (> 5% of rules)

\*/

```



\---



\## 100. THE FINAL MASTER REFERENCE



\### 100.1 CSS Properties Grouped by Impact



```css

/\* ─── Properties that trigger LAYOUT (expensive) ─── \*/

/\*

&#x20; width, height, min-\*, max-\*

&#x20; margin, padding

&#x20; border (width changes)

&#x20; position, top, right, bottom, left, inset

&#x20; display (change)

&#x20; overflow

&#x20; font-size, line-height

&#x20; float, clear

&#x20; grid-template-\*, grid-column, grid-row

&#x20; flex-basis, flex-grow, flex-shrink

&#x20; content (pseudo-elements)

&#x20; table-layout

&#x20; column-\*

\*/



/\* ─── Properties that trigger PAINT only ─── \*/

/\*

&#x20; color, background-color

&#x20; border-color, border-style (not width)

&#x20; outline

&#x20; box-shadow, text-shadow

&#x20; border-radius

&#x20; visibility

&#x20; background-image (gradient changes)

&#x20; filter (some types)

&#x20; opacity (in some browsers — now composited!)

\*/



/\* ─── Properties that are COMPOSITED (cheapest) ─── \*/

/\*

&#x20; transform: translate(), scale(), rotate()

&#x20; opacity (modern browsers)

&#x20; will-change (promotes to layer)

&#x20; filter: blur, brightness (on composited layers)

&#x20; backdrop-filter (composited)

&#x20; clip-path (on composited elements)

\*/



/\* ─── Properties NOT inherited ─── \*/

/\*

&#x20; Most layout: display, position, width, height, margin, padding,

&#x20;              border, overflow, z-index, float

&#x20; Visual: background, box-shadow, opacity, transform, filter

&#x20; UI: outline, cursor (yes! cursor is inherited — exception)

\*/



/\* ─── Properties that ARE inherited ─── \*/

/\*

&#x20; Typography: font-\*, line-height, letter-spacing, word-spacing,

&#x20;             text-align, text-transform, text-indent,

&#x20;             text-decoration (partial), white-space, hyphens

&#x20; Color: color, (not background-color!)

&#x20; Other: cursor, pointer-events, visibility, quotes,

&#x20;        list-style-\*, border-collapse, border-spacing,

&#x20;        caption-side, empty-cells, direction, writing-mode,

&#x20;        word-break, overflow-wrap

&#x20; Custom properties: depend on inherits: declaration in @property

\*/

```



\### 100.2 Every CSS At-Rule



```css

/\* ─── COMPLETE @RULE REFERENCE ─── \*/



@charset "UTF-8";                         /\* Character encoding (must be first) \*/



@import url('style.css');                 /\* Import external stylesheet \*/

@import url('style.css') layer(base);    /\* Import into layer \*/

@import url('style.css') supports(display: grid);  /\* Conditional import \*/

@import url('style.css') (max-width: 768px);        /\* Media conditional \*/



@layer base, components;                 /\* Declare layer order \*/

@layer base { /\* rules \*/ }             /\* Define layer \*/



@media (min-width: 768px) { }           /\* Media query \*/

@media print { }



@supports (display: grid) { }           /\* Feature query \*/

@supports not (gap: 1rem) { }

@supports selector(:has()) { }          /\* Selector support query \*/



@keyframes name {                        /\* Animation keyframes \*/

&#x20; from { } to { }

&#x20; 0% { } 50% { } 100% { }

}



@font-face {                             /\* Custom font \*/

&#x20; font-family: 'Name';

&#x20; src: url('font.woff2') format('woff2');

&#x20; font-display: swap;

&#x20; unicode-range: U+0000-00FF;

}



@property --name {                       /\* Custom property type \*/

&#x20; syntax: '<color>';

&#x20; initial-value: red;

&#x20; inherits: false;

}



@counter-style thumbs {                  /\* Custom counter \*/

&#x20; system: cyclic;

&#x20; symbols: "\\1F44D";

&#x20; suffix: " ";

}



@page { margin: 2cm; }                  /\* Print page margins \*/

@page :first { }

@page :left { }

@page :right { }

@page :blank { }



@namespace url('http://www.w3.org/1999/xhtml');  /\* XML namespace \*/



@scope (.card) { }                       /\* Scope (new) \*/

@scope (.card) to (.body) { }



@container (min-width: 400px) { }       /\* Container query \*/

@container sidebar (min-width: 300px) { }



@color-profile --fogra39 {              /\* Color profile \*/

&#x20; src: url('FOGRA39.icc');

&#x20; rendering-intent: relative-colorimetric;

}



@position-try --tooltip-top { }         /\* Anchor positioning fallback \*/



/\* ─── DRAFT / PROPOSED (not yet stable) ─── \*/

/\* @custom-selector :--heading h1, h2, h3; \*/

/\* @mixin name { } \*/

/\* @apply mixin-name; \*/

/\* @when supports(display: grid) { } @else { } \*/

/\* @function --fluid($min, $max) { result: clamp($min, ...); } \*/

```



\### 100.3 Color Function Syntax Reference



```css

/\* All modern color functions and their syntax \*/



/\* ─── Legacy ─── \*/

color: rgb(255, 0, 0);

color: rgb(255 0 0);              /\* modern no-comma \*/

color: rgb(255 0 0 / 0.5);       /\* with alpha \*/

color: rgba(255, 0, 0, 0.5);     /\* legacy with alpha \*/



color: hsl(0, 100%, 50%);

color: hsl(0 100% 50%);

color: hsl(0 100% 50% / 0.5);



/\* ─── HWB ─── \*/

color: hwb(0 0% 0%);             /\* hue white black \*/

color: hwb(0 0% 0% / 0.5);



/\* ─── Lab / LCH ─── \*/

color: lab(50% 40 59.4);         /\* lightness a b \*/

color: lch(50% 70 40);           /\* lightness chroma hue \*/



/\* ─── OKLAB / OKLCH (recommended) ─── \*/

color: oklab(0.5 0.15 -0.1);    /\* lightness a b \*/

color: oklch(0.5 0.2 250);       /\* lightness chroma hue \*/

color: oklch(0.5 0.2 250 / 0.5);



/\* ─── display-p3 (wide gamut) ─── \*/

color: color(display-p3 0.5 0.3 0.8);

color: color(display-p3 0.5 0.3 0.8 / 0.5);



/\* ─── Other color() spaces ─── \*/

color: color(srgb 0.5 0.3 0.8);

color: color(srgb-linear 0.5 0.3 0.8);

color: color(a98-rgb 0.5 0.3 0.8);

color: color(prophoto-rgb 0.5 0.3 0.8);

color: color(rec2020 0.5 0.3 0.8);

color: color(xyz-d50 0.3 0.2 0.5);

color: color(xyz-d65 0.3 0.2 0.5);



/\* ─── Named system colors ─── \*/

color: Canvas;           /\* page background \*/

color: CanvasText;       /\* page text \*/

color: LinkText;         /\* link color \*/

color: VisitedText;      /\* visited link \*/

color: ActiveText;       /\* active link \*/

color: ButtonFace;       /\* button background \*/

color: ButtonText;       /\* button text \*/

color: ButtonBorder;     /\* button border \*/

color: Field;            /\* input background \*/

color: FieldText;        /\* input text \*/

color: Highlight;        /\* selected background \*/

color: HighlightText;    /\* selected text \*/

color: GrayText;         /\* disabled text \*/

color: AccentColor;      /\* OS accent \*/

color: AccentColorText;  /\* text on accent \*/

color: Mark;             /\* highlighted text bg \*/

color: MarkText;         /\* highlighted text \*/



/\* ─── Color functions ─── \*/

color: color-mix(in oklch, blue 30%, red);

color: color-mix(in srgb, var(--accent) 20%, transparent);



/\* Relative color syntax \*/

color: oklch(from var(--base) l c h);

color: oklch(from var(--base) calc(l + 0.2) c h);

color: oklch(from var(--base) l calc(c \* 0.5) h);

color: rgba(from var(--base) r g b / 0.5);



/\* light-dark() \*/

color: light-dark(#000, #fff);

background: light-dark(white, #111);

```



\---



```

╔══════════════════════════════════════════════════════════════════════╗

║            THE MONUMENTAL CSS GUIDE — COMPLETE                       ║

╠══════════════════════════════════════════════════════════════════════╣

║                                                                      ║

║  PARTS:      I · II · III · IV · V                                  ║

║  CHAPTERS:   100 chapters                                            ║

║  TOTAL SIZE: \~20,000+ lines                                          ║

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

