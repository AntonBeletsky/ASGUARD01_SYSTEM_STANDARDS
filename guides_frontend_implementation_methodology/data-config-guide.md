# Data Attributes as Component Configuration — Complete Guide

A practical reference for using `data-*` attributes as the configuration layer
for JavaScript components — the pattern used in this codebase's `ProductsCarousel`.

---

## Table of Contents

1. [Why Data Attributes for Config](#1-why-data-attributes-for-config)
2. [Naming Conventions](#2-naming-conventions)
3. [Reading Data Attributes in JS](#3-reading-data-attributes-in-js)
4. [Type Coercion Patterns](#4-type-coercion-patterns)
5. [Default Values](#5-default-values)
6. [Boolean Attributes](#6-boolean-attributes)
7. [Enum / Allowed Values](#7-enum--allowed-values)
8. [Nested / Scoped Attributes](#8-nested--scoped-attributes)
9. [Config Object Pattern](#9-config-object-pattern)
10. [Merging Data-config with JS Options](#10-merging-data-config-with-js-options)
11. [Updating Config at Runtime](#11-updating-config-at-runtime)
12. [Observing Config Changes (MutationObserver)](#12-observing-config-changes-mutationobserver)
13. [Validation & Error Handling](#13-validation--error-handling)
14. [Multi-instance Components](#14-multi-instance-components)
15. [Targeting Child Elements by Data Attribute](#15-targeting-child-elements-by-data-attribute)
16. [Data Attributes vs Alternatives](#16-data-attributes-vs-alternatives)
17. [Security Considerations](#17-security-considerations)
18. [Real-world Component Template](#18-real-world-component-template)
19. [Quick Reference](#19-quick-reference)

---

## 1. Why Data Attributes for Config

Data attributes let HTML drive component behavior without touching JavaScript.
A developer drops a snippet, tweaks attributes, done — no JS file to edit.

```html
<!-- Zero JS needed to configure this component -->
<div class="carousel"
     data-carousel-scroll-mode="page"
     data-carousel-loop="true"
     data-carousel-dots="false"
     data-carousel-arrows-opacity="0.5">
</div>
```

**Advantages over alternatives:**

| Concern | Data attributes | JS options object | CSS classes |
|---|---|---|---|
| Configured in HTML | ✅ | ❌ requires JS | ⚠️ flags only |
| Human-readable | ✅ | ✅ | ⚠️ |
| Typed values | ⚠️ always strings | ✅ native types | ❌ |
| Discoverable in DevTools | ✅ Elements panel | ⚠️ console only | ✅ |
| CMS / template friendly | ✅ | ❌ | ⚠️ |
| Multiple instances, different config | ✅ per-element | ✅ per-call | ✅ |
| Runtime changes | ✅ setAttribute | ✅ direct | ✅ |

---

## 2. Naming Conventions

### Structure

```
data-{component}-{option}
data-{component}-{group}-{option}
```

Always prefix with the component name — prevents collisions with other
components or third-party libraries on the same page.

```html
<!-- ✅ Good — namespaced -->
<div data-carousel-loop="true"
     data-carousel-scroll-mode="page">

<!-- ❌ Bad — generic, will collide -->
<div data-loop="true"
     data-mode="page">
```

### Casing rules

HTML attribute names are **case-insensitive** and conventionally **lowercase-kebab**.
`dataset` in JS converts kebab to **camelCase** automatically:

| HTML attribute | JS `dataset` key |
|---|---|
| `data-scroll-mode` | `dataset.scrollMode` |
| `data-arrows-opacity` | `dataset.arrowsOpacity` |
| `data-carousel-scroll-mode` | `dataset.carouselScrollMode` |
| `data-show-dots` | `dataset.showDots` |

Never use uppercase in attribute names — `data-scrollMode` becomes
`dataset.scrollmode` (all lowercased by the parser), not `dataset.scrollMode`.

```html
<!-- ❌ Wrong — uppercase in HTML attribute -->
<div data-scrollMode="page">
<!-- dataset.scrollmode — not what you expect -->

<!-- ✅ Correct — kebab in HTML, camelCase auto-mapped in JS -->
<div data-scroll-mode="page">
<!-- dataset.scrollMode ✓ -->
```

---

## 3. Reading Data Attributes in JS

### Via `dataset` (preferred)

```js
const el = document.querySelector('.carousel');

el.dataset.carouselLoop        // "true"   (always a string)
el.dataset.carouselScrollMode  // "page"
el.dataset.carouselDotsCount   // "5"
el.dataset.missing             // undefined (not null)
```

### Via `getAttribute` (explicit, handles edge cases)

```js
el.getAttribute('data-carousel-loop')  // "true" | null (not undefined)
```

Use `getAttribute` when:
- You need to distinguish "attribute absent" (`null`) from "attribute present but empty" (`""`)
- Working with SVG elements (dataset not always reliable)
- Reading attributes dynamically with a variable name

```js
const attrName = `data-carousel-${optionKey}`;
el.getAttribute(attrName); // dynamic — dataset won't work here
```

### Writing back

```js
el.dataset.carouselLoop = 'false';            // sets data-carousel-loop="false"
el.setAttribute('data-carousel-loop', 'false'); // equivalent
el.removeAttribute('data-carousel-loop');       // removes it entirely
delete el.dataset.carouselLoop;                 // same as removeAttribute
```

---

## 4. Type Coercion Patterns

All `dataset` values are strings. Convert them explicitly — never rely on implicit
JS coercion (it produces unexpected results for booleans).

### String (no conversion needed)

```js
// data-carousel-scroll-mode="page"
this.scrollMode = ds.carouselScrollMode ?? 'page';
// Result: "page" — already a string
```

### Number

```js
// data-carousel-threshold="5"
this.threshold = Number(ds.carouselThreshold ?? 5);
// or
this.threshold = parseFloat(ds.carouselThreshold ?? '5');

// Guard against NaN
this.threshold = Number(ds.carouselThreshold) || 5;
```

### Boolean — the critical one

```js
// ❌ WRONG — any non-empty string is truthy, including "false"
this.loop = Boolean(ds.carouselLoop);     // "false" → true ← BUG

// ✅ CORRECT — compare the string explicitly
this.loop  = ds.carouselLoop === 'true';  // opt-in: absent = false
this.smooth = ds.carouselSmooth !== 'false'; // opt-out: absent = true
```

Choose **opt-in** (`=== 'true'`) when the default is `false`.
Choose **opt-out** (`!== 'false'`) when the default is `true`.

### Array

```js
// data-carousel-breakpoints="320,768,1024"
this.breakpoints = (ds.carouselBreakpoints ?? '')
  .split(',')
  .map(Number)
  .filter(Boolean);
// Result: [320, 768, 1024]
```

### JSON (for complex config)

```html
<div data-carousel-config='{"speed":300,"easing":"ease-in-out"}'></div>
```

```js
// Parse safely — attribute might be malformed
try {
  this.advancedConfig = JSON.parse(ds.carouselConfig ?? 'null') ?? {};
} catch {
  console.warn('Invalid JSON in data-carousel-config');
  this.advancedConfig = {};
}
```

JSON in attributes works but is fragile — avoid for frequently changed settings.
Use it only for structured data that doesn't fit flat key-value attributes.

---

## 5. Default Values

### Nullish coalescing (`??`) — use for strings and numbers

```js
// ?? only falls back when the left side is null or undefined
// An empty string "" is preserved (intentional empty value)

this.scrollMode = ds.carouselScrollMode ?? 'page';
this.threshold  = Number(ds.carouselThreshold ?? 5);
```

### OR operator (`||`) — use carefully for numbers

```js
// || falls back on any falsy value — including 0
this.speed = Number(ds.carouselSpeed) || 300; // 0 would be replaced with 300 — BUG?
this.speed = ds.carouselSpeed !== undefined ? Number(ds.carouselSpeed) : 300; // safe
```

### Centralized defaults object

```js
const DEFAULTS = {
  scrollMode    : 'page',
  smooth        : true,
  threshold     : 5,
  loop          : false,
  showDots      : true,
  arrowsOpacity : 1,
};

function readConfig(el) {
  const ds = el.dataset;
  return {
    scrollMode    : ds.carouselScrollMode    ?? DEFAULTS.scrollMode,
    smooth        : ds.carouselSmooth        !== 'false' ? DEFAULTS.smooth : false,
    threshold     : Number(ds.carouselThreshold   ?? DEFAULTS.threshold),
    loop          : ds.carouselLoop          === 'true'  || DEFAULTS.loop,
    showDots      : ds.carouselDots          !== 'false' ? DEFAULTS.showDots : false,
    arrowsOpacity : parseFloat(ds.carouselArrowsOpacity ?? DEFAULTS.arrowsOpacity),
  };
}
```

---

## 6. Boolean Attributes

Two styles — pick one and be consistent across your component:

### Style A — explicit string value (recommended)

```html
<div data-carousel-loop="true">
<div data-carousel-loop="false">
```

```js
this.loop = ds.carouselLoop === 'true'; // absent or "false" → false
```

Pros: explicit, survives templating systems that always output a value.

### Style B — presence/absence (HTML-native style, like `disabled`)

```html
<div data-carousel-loop>        <!-- present = true -->
<div>                           <!-- absent  = false -->
```

```js
this.loop = el.hasAttribute('data-carousel-loop');
```

Pros: shorter HTML, idiomatic for binary flags.
Cons: can't set to `false` via attribute — must `removeAttribute`.

---

## 7. Enum / Allowed Values

Validate that the value is one of the expected options, fall back to default if not:

```js
const SCROLL_MODES = ['page', 'single'];

const raw = ds.carouselScrollMode ?? 'page';
this.scrollMode = SCROLL_MODES.includes(raw) ? raw : 'page';

// With a warning so developers notice mistakes fast
if (!SCROLL_MODES.includes(raw)) {
  console.warn(
    `[Carousel] Invalid data-carousel-scroll-mode="${raw}".`,
    `Allowed: ${SCROLL_MODES.join(', ')}. Using default: "page".`
  );
}
```

---

## 8. Nested / Scoped Attributes

For components with sub-components or grouped settings, add an extra segment:

```html
<div class="carousel"
     data-carousel-arrow-opacity="0.5"
     data-carousel-arrow-size="45"
     data-carousel-dot-color="#0d6efd"
     data-carousel-dot-size="10"
     data-carousel-dot-active-color="#fff">
```

```js
this.arrow = {
  opacity : parseFloat(ds.carouselArrowOpacity ?? 1),
  size    : Number(ds.carouselArrowSize ?? 45),
};

this.dot = {
  color       : ds.carouselDotColor       ?? 'var(--bs-gray-400)',
  size        : Number(ds.carouselDotSize ?? 10),
  activeColor : ds.carouselDotActiveColor ?? 'var(--bs-info)',
};
```

Grouping into nested objects also makes config easier to pass to sub-methods:

```js
this.#applyArrowStyles(this.arrow);
this.#applyDotStyles(this.dot);
```

---

## 9. Config Object Pattern

Parse all config in one place at construction time.
Never read `dataset` again after initialization — store everything in `this`.

```js
class ProductsCarousel {
  constructor(containerSelector) {
    this.container = document.querySelector(containerSelector);
    if (!this.container) return;

    // ── All config parsed here, once ─────────────────────────────────────
    this.config = this.#parseConfig(this.container.dataset);

    this.#init();
  }

  #parseConfig(ds) {
    return {
      scrollMode    : this.#enum(ds.carouselScrollMode,    ['page','single'], 'page'),
      smooth        : ds.carouselSmooth        !== 'false',
      threshold     : Number(ds.carouselThreshold          ?? 5),
      loop          : ds.carouselLoop          === 'true',
      showDots      : ds.carouselDots          !== 'false',
      arrowsOpacity : parseFloat(ds.carouselArrowsOpacity  ?? 1),
    };
  }

  #enum(value, allowed, fallback) {
    return allowed.includes(value) ? value : fallback;
  }
}
```

Benefits:
- Config is validated in one place
- Rest of the class reads `this.config.loop` — clean and readable
- Easy to log or serialize the entire config for debugging

---

## 10. Merging Data-config with JS Options

Sometimes a component is used both via HTML markup and via JS API.
Support both by merging JS options over data-attribute defaults:

```js
class ProductsCarousel {
  constructor(containerSelector, jsOptions = {}) {
    this.container = document.querySelector(containerSelector);

    const fromHTML = this.#parseConfig(this.container.dataset);

    // JS options win over HTML attributes
    this.config = { ...fromHTML, ...jsOptions };
  }
}

// HTML-only usage
new ProductsCarousel('.carousel');

// JS overrides specific options (ignores data-carousel-loop="true" in HTML)
new ProductsCarousel('.carousel', { loop: false, arrowsOpacity: 0.8 });
```

---

## 11. Updating Config at Runtime

To support live reconfiguration (e.g., a settings panel changing behavior):

```js
class ProductsCarousel {

  updateConfig(patch) {
    this.config = { ...this.config, ...patch };
    this.#applyConfig(); // re-apply changed settings
  }

  #applyConfig() {
    // Dots visibility
    if (this.pagination) {
      this.pagination.style.display = this.config.showDots ? '' : 'none';
    }
    // Arrow opacity
    [this.prevBtn, this.nextBtn].forEach(btn => {
      if (btn) btn.style.setProperty('--carousel-arrow-opacity', this.config.arrowsOpacity);
    });
  }
}

// Usage
const carousel = new ProductsCarousel('.carousel');
carousel.updateConfig({ showDots: false, arrowsOpacity: 1 });
```

---

## 12. Observing Config Changes (MutationObserver)

React to attribute changes automatically — useful when config is driven
by a CMS, A/B test framework, or external code:

```js
class ProductsCarousel {

  #observeAttributes() {
    const mo = new MutationObserver(mutations => {
      let changed = false;
      mutations.forEach(m => {
        if (m.attributeName?.startsWith('data-carousel-')) changed = true;
      });
      if (changed) {
        this.config = this.#parseConfig(this.container.dataset); // re-parse
        this.#applyConfig();
      }
    });

    mo.observe(this.container, { attributes: true });
    this._mo = mo; // store for later cleanup
  }

  destroy() {
    this._mo?.disconnect();
  }
}
```

```js
// External code changes an attribute → component auto-updates
document.querySelector('.carousel')
  .setAttribute('data-carousel-dots', 'false');
```

---

## 13. Validation & Error Handling

Fail loudly in development, gracefully in production:

```js
#parseConfig(ds) {
  const errors = [];

  const arrowsOpacity = parseFloat(ds.carouselArrowsOpacity ?? 1);
  if (arrowsOpacity < 0 || arrowsOpacity > 1) {
    errors.push(`data-carousel-arrows-opacity="${ds.carouselArrowsOpacity}" must be 0–1`);
  }

  const scrollMode = ds.carouselScrollMode ?? 'page';
  if (!['page', 'single'].includes(scrollMode)) {
    errors.push(`data-carousel-scroll-mode="${scrollMode}" is not valid. Use: page | single`);
  }

  if (errors.length) {
    console.group('[ProductsCarousel] Config errors:');
    errors.forEach(e => console.warn('⚠', e));
    console.groupEnd();
  }

  return {
    scrollMode    : ['page','single'].includes(scrollMode) ? scrollMode : 'page',
    arrowsOpacity : Math.min(1, Math.max(0, isNaN(arrowsOpacity) ? 1 : arrowsOpacity)),
    // ... rest of config
  };
}
```

---

## 14. Multi-instance Components

Each element gets its own component instance with its own config:

```html
<!-- Instance A — looping, no dots -->
<div class="carousel" id="featured"
     data-carousel-loop="true"
     data-carousel-dots="false">
</div>

<!-- Instance B — static, with dots, single-step -->
<div class="carousel" id="related"
     data-carousel-loop="false"
     data-carousel-scroll-mode="single">
</div>
```

```js
// Initialize all carousels on the page — each reads its own data attributes
window.addEventListener('load', () => {
  document.querySelectorAll('.carousel-track-container').forEach(el => {
    new ProductsCarousel(el); // pass element directly instead of selector
  });
});
```

For this to work, the constructor must accept either a selector string or
an element reference:

```js
constructor(target) {
  this.container = typeof target === 'string'
    ? document.querySelector(target)
    : target; // already an element
}
```

---

## 15. Targeting Child Elements by Data Attribute

Internal elements of a component should also be identified by data attributes —
not by class names. Class names are for styling; data attributes are for JS hooks.

```html
<div class="carousel-track-container" data-carousel>
  <button data-carousel-prev>‹</button>
  <div data-carousel-track>
    <div data-carousel-item>...</div>
    <div data-carousel-item>...</div>
  </div>
  <button data-carousel-next>›</button>
  <div data-carousel-pagination></div>
</div>
```

```js
// ✅ Query by data attribute — not fragile to class renames
this.track      = this.container.querySelector('[data-carousel-track]');
this.prevBtn    = this.container.querySelector('[data-carousel-prev]');
this.nextBtn    = this.container.querySelector('[data-carousel-next]');
this.pagination = this.container.querySelector('[data-carousel-pagination]');

// Filter clones from originals using an extra attribute
this.items = this.track.querySelectorAll(
  '[data-carousel-item]:not([data-carousel-clone])'
);
```

**Rule:** If JS touches it, put a `data-` on it. Keep class names CSS-only.

---

## 16. Data Attributes vs Alternatives

When data attributes are not the right tool:

### Use CSS custom properties instead — for visual/style values

```html
<!-- ❌ Style-only config in data attribute -->
<div data-carousel-dot-color="#0d6efd">

<!-- ✅ CSS variable — where style belongs -->
<div style="--carousel-dot-color: #0d6efd;">
```

```css
.pagination-dot.active {
  background-color: var(--carousel-dot-color, var(--bs-info));
}
```

### Use JS options object instead — for callbacks and non-serializable values

```js
// ❌ Can't put a function in a data attribute
// data-carousel-on-change="???"

// ✅ Pass callbacks via JS options
new ProductsCarousel('.carousel', {
  onChange: (index) => console.log('Slide changed to', index),
  renderDot: (index) => `<span class="my-dot">${index}</span>`,
});
```

### Use `<script type="application/json">` — for large structured config

```html
<div class="carousel" data-carousel-config-id="featured-config">
</div>

<script type="application/json" id="featured-config">
{
  "items": [...],
  "breakpoints": { "768": { "scrollMode": "single" } }
}
</script>
```

```js
const configId  = this.container.dataset.carouselConfigId;
const configEl  = document.getElementById(configId);
this.bigConfig  = configEl ? JSON.parse(configEl.textContent) : {};
```

---

## 17. Security Considerations

Data attributes are part of the DOM — anyone can read or write them.

**Never use data attributes for:**
- API keys or tokens
- Sensitive user data
- Server-side secrets

**XSS via innerHTML with data-attribute values:**

```js
// ❌ DANGEROUS — data attribute injected into HTML
el.innerHTML = `<div class="${this.container.dataset.theme}">`;
// Attacker sets data-theme='"><script>evil()</script>'

// ✅ SAFE — use textContent or setAttribute
const wrapper = document.createElement('div');
wrapper.setAttribute('class', this.container.dataset.theme ?? '');
el.appendChild(wrapper);
```

Always treat data attribute values as untrusted strings when inserting into HTML.

---

## 18. Real-world Component Template

A complete, production-ready starting point using all the patterns above:

```js
class MyComponent {
  // ── Static API ─────────────────────────────────────────────────────────
  static DEFAULTS = {
    mode    : 'page',          // enum: 'page' | 'single'
    smooth  : true,            // boolean opt-out
    count   : 3,               // number
    loop    : false,           // boolean opt-in
    showNav : true,            // boolean opt-out
    opacity : 1,               // float 0–1
  };

  static MODES = ['page', 'single'];

  // ── Init ───────────────────────────────────────────────────────────────
  constructor(target, jsOptions = {}) {
    this.container = typeof target === 'string'
      ? document.querySelector(target)
      : target;

    if (!this.container) {
      console.warn(`[MyComponent] Element not found:`, target);
      return;
    }

    this.config = {
      ...this.#parseDataConfig(this.container.dataset),
      ...jsOptions, // JS options override HTML config
    };

    this.#findElements();
    this.#validate();
    this.#init();
  }

  // ── Private ────────────────────────────────────────────────────────────
  #parseDataConfig(ds) {
    const D = MyComponent.DEFAULTS;
    return {
      mode    : MyComponent.MODES.includes(ds.myMode)
                ? ds.myMode
                : D.mode,
      smooth  : ds.mySmooth  !== 'false',
      count   : Number(ds.myCount   ?? D.count),
      loop    : ds.myLoop    === 'true',
      showNav : ds.myShowNav !== 'false',
      opacity : parseFloat(ds.myOpacity ?? D.opacity),
    };
  }

  #findElements() {
    this.track   = this.container.querySelector('[data-my-track]');
    this.prevBtn = this.container.querySelector('[data-my-prev]');
    this.nextBtn = this.container.querySelector('[data-my-next]');
    this.items   = [...this.container.querySelectorAll('[data-my-item]')];
  }

  #validate() {
    if (!this.track) console.warn('[MyComponent] Missing [data-my-track]');
    const op = this.config.opacity;
    if (isNaN(op) || op < 0 || op > 1) {
      console.warn(`[MyComponent] data-my-opacity="${op}" out of range 0–1, using 1`);
      this.config.opacity = 1;
    }
  }

  #init() {
    // Use this.config.* from here on
  }

  // ── Public API ─────────────────────────────────────────────────────────
  updateConfig(patch) {
    this.config = { ...this.config, ...patch };
    this.#applyConfig();
  }

  destroy() {
    this._mo?.disconnect();
    // remove event listeners...
  }
}

// ── Auto-init all instances on the page ──────────────────────────────────
window.addEventListener('load', () => {
  document.querySelectorAll('[data-my-component]').forEach(el => {
    el._myComponent = new MyComponent(el);
  });
});
```

---

## 19. Quick Reference

### Naming

```
data-{component}-{option}          data-carousel-loop
data-{component}-{group}-{option}  data-carousel-arrow-opacity
```

### Type conversions

```js
// String   (default)
ds.myOption ?? 'default'

// Number
Number(ds.myCount ?? 5)
parseFloat(ds.myOpacity ?? 1)

// Boolean opt-in  (absent = false)
ds.myLoop === 'true'

// Boolean opt-out (absent = true)
ds.mySmooth !== 'false'

// Enum
['a','b','c'].includes(ds.myMode) ? ds.myMode : 'a'

// Array
(ds.myList ?? '').split(',').map(Number).filter(Boolean)

// JSON
JSON.parse(ds.myConfig ?? 'null') ?? {}
```

### Reading / Writing

```js
el.dataset.myOption                     // read (camelCase)
el.getAttribute('data-my-option')       // read (kebab)
el.dataset.myOption = 'value'           // write
el.setAttribute('data-my-option', 'v')  // write (explicit)
el.removeAttribute('data-my-option')    // delete
el.hasAttribute('data-my-option')       // presence check
```

### Child element selectors

```js
el.querySelector('[data-carousel-track]')
el.querySelectorAll('[data-carousel-item]:not([data-carousel-clone])')
```

### Common mistakes

| Mistake | Fix |
|---|---|
| `Boolean(ds.myFlag)` — `"false"` → `true` | `ds.myFlag === 'true'` |
| `data-myOption` uppercase in HTML | `data-my-option` kebab only |
| Reading `dataset` inside animation loop | Cache in constructor |
| Using class names as JS selectors | Use `data-*` for JS hooks |
| Putting callbacks in data attributes | Pass via JS options object |
| Injecting `dataset` values into innerHTML | Use `textContent` / `setAttribute` |
