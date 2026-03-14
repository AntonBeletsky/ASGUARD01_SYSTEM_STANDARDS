# Kill Fucked Customization — Make Clean Bootstrap

> **One rule**: custom CSS is written only when Bootstrap physically cannot do it.
> Everything else — utility classes in HTML. The question before every rule: *"What exactly is unique here?"*
> If the answer is "nothing" — the rule dies.

---

## Table of Contents

1. [Decision Tree](#1-decision-tree)
2. [Phase 0 — Freeze Tokens](#2-phase-0--freeze-tokens)
3. [Phase 1 — Kill font-size-only Classes](#3-phase-1--kill-font-size-only-classes)
4. [Phase 2 — Merge Component Duplicates](#4-phase-2--merge-component-duplicates)
5. [Phase 3 — Replace Custom Tabs with nav-underline](#5-phase-3--replace-custom-tabs-with-nav-underline)
6. [Phase 4 — Kill Structural Page CSS](#6-phase-4--kill-structural-page-css)
7. [Phase 5 — Clean JS Templates](#7-phase-5--clean-js-templates)
8. [Phase 6 — Verify States and Dark Mode](#8-phase-6--verify-states-and-dark-mode)
9. [Replacement Table: Tokens](#9-replacement-table-tokens)
10. [Replacement Table: CSS Classes → BS Utilities](#10-replacement-table-css-classes--bs-utilities)
11. [Replacement Table: Components](#11-replacement-table-components)
12. [What Stays Custom — and Why](#12-what-stays-custom--and-why)
13. [Final Checklist](#13-final-checklist)

---

## 1. Decision Tree

Run **every** CSS rule through this filter before touching any code.

```
There is a custom CSS rule
          │
          ▼
Does a Bootstrap utility do the same thing?
    YES  ──►  KILL the rule, put utility in HTML
          │
         NO
          ▼
Is the class needed as a JS hook, but a Bootstrap utility covers the style?
    YES  ──►  REPLACE: remove CSS, add BS class to HTML/JS template
          │
         NO
          ▼
Does it duplicate another custom class?
    YES  ──►  MERGE into one class, delete the rest
          │
         NO
          ▼
Does the rule contain properties Bootstrap already provides?
    YES  ──►  SLIM: keep only unique properties,
              remove the rest and put utilities in HTML
          │
         NO
          ▼
    KEEP as-is
    (unique logic — no BS equivalent exists)
```

**Five outcomes:** KILL / REPLACE / MERGE / SLIM / KEEP.
There is no sixth. No "leave for now" and no "might be useful later".

---

## 2. Phase 0 — Freeze Tokens

**Do this first.** If you start with rules instead of tokens, deleting classes will leave dead `var(--custom-*)` references that do nothing but pollute the CSS.

### Algorithm

1. List all custom `--prefix-*` tokens from `:root` or the container.
2. Find the Bootstrap equivalent for each using the table below.
3. If an equivalent exists — the token is **deleted**, all `var(--prefix-*)` usages in rules are replaced with `var(--bs-*)`.
4. If no equivalent exists — the token **stays**, but moves to the widget container, not `:root`.

### Why tokens must not live on `:root`

A custom token on `:root` is a global variable. If two different widgets on the same page use the same token name with different values, they conflict. Bootstrap already occupies `:root` with its own namespace — we don't compete with it. Everything custom belongs on `.widget-container`:

```css
/* ❌ Wrong — global scope */
:root {
  --rv-brand: #1a56db;
  --rv-radius: 14px;
}

/* ✅ Correct — scoped to the container */
.rv-page {
  --rv-star: #f59e0b; /* stays: no BS equivalent */
}
```

### What not to touch

**Dynamic** tokens that JS sets via `element.style.setProperty()` — these are not design tokens, they are a data-passing mechanism from JS to CSS. Do not touch them.

```css
/* This is a JS→CSS data channel, not a design token — leave alone */
.rv-bar-fill { width: var(--rv-bar-pct, 0%); }
```

---

## 3. Phase 1 — Kill font-size-only Classes

The largest category of waste. The pattern looks like this:

```css
/* ❌ This is a "font-size-only" class — kill it */
.rv-card-meta  { font-size: 13px; }
.rv-card-title { font-size: 15px; }
.rv-form-label { font-size: 14px; }
```

### The rule

If the **only** property of a class is `font-size`, and that value matches a Bootstrap utility or the base font size — the class is unnecessary.

### font-size → BS utility mapping

| Value | Bootstrap utility | Note |
|---|---|---|
| `≈ 11–12px` | `small` | `0.875em` of parent |
| `13px` | `small` | close enough, accept |
| `14px` | *(nothing)* | BS default body size — no class needed |
| `15px` | *(nothing)* | remove class, leave unstyled |
| `1rem / 16px` | *(nothing)* | base size — class not needed |
| `1.25rem / 20px` | `fs-5` | |
| `1.5rem / 24px` | `fs-4` | |
| `2rem / 32px` | `fs-3` | |
| `2rem+` | `fs-2`, `fs-1` | |
| `< 12px` | `small` + custom | only if design truly requires it |

### How to replace

Delete the class from CSS. In HTML or in JS templates (innerHTML strings), replace the class with a BS utility:

```html
<!-- ❌ Before -->
<span class="rv-card-meta">Jan 15, 2025</span>
<h2 class="rv-card-title">Product Name</h2>

<!-- ✅ After -->
<span class="small text-secondary">Jan 15, 2025</span>
<h2 class="fw-semibold">Product Name</h2>
```

### Special case: `font-size` + something else

If a class does `font-size` AND something else — it does not die completely. Run it through the decision tree: if the remaining properties are also covered by BS — kill it. If not — slim it: remove `font-size`, keep the unique part:

```css
/* ❌ Before — font-size + one more property */
.rv-bar-label { font-size: 13px; width: 44px; }
.rv-bar-count { font-size: 13px; width: 24px; text-align: right; }

/* ✅ After — removed font-size (→ small in HTML), kept the unique part */
.rv-page .rv-bar-label { width: 44px; }
.rv-page .rv-bar-count { width: 24px; text-align: right; }
```

---

## 4. Phase 2 — Merge Component Duplicates

Bootstrap projects grow organically: first `.product-card`, then `.comment-card`, then `.stat-card` — and all of them have identical `border`, `border-radius`, `box-shadow`. That is copy-paste disguised as different class names.

### How to find duplicates

```bash
# Quick scan for identical property sets
grep -A5 "box-shadow:" styles.css | sort | uniq -d
```

Or visually: if two classes differ only in name and share the same `border`, `radius`, `shadow` — they are duplicates.

### Merge strategy

1. Pick **one** base class (usually the first or the most general).
2. In HTML/JS replace all other class names with the base one.
3. Properties unique to each variant — move them to modifiers:

```css
/* ❌ Before — three copies of the same block */
.rv-card {
  border-radius: 14px;
  border: 1px solid var(--bs-border-color-translucent);
  box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.05);
  transition: box-shadow .18s ease;
  overflow: hidden;
}
.rv-comment-card {
  border-radius: 14px;
  border: 1px solid var(--bs-border-color-translucent);
  box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.05);
  transition: box-shadow .18s ease;
}
.rv-stat-card {
  border-radius: 14px;
  border: 1px solid var(--bs-border-color-translucent);
  box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.05);
  padding: 1rem 1.2rem;
  background: var(--bs-body-bg);
}

/* ✅ After — one base class + Bootstrap utilities */
/* padding and bg go via p-3, bg-body directly in HTML */
.rv-page .rv-card {
  box-shadow: var(--bs-box-shadow-sm);
  transition: box-shadow .18s ease;
  overflow: hidden; /* only this cannot be done with a utility */
}
.rv-page .rv-card:hover {
  box-shadow: var(--bs-box-shadow);
}
```

```html
<!-- rv-stat-card gets p-3 bg-body directly in HTML — no extra CSS needed -->
<div class="rv-card card rounded-3 p-3 bg-body">...</div>
```

### After merging — slim down to unique

After duplicates are merged into one class, run that one class through the decision tree again. Often there is nothing left that BS cannot handle, except one or two properties.

---

## 5. Phase 3 — Replace Custom Tabs with nav-underline

Bootstrap 5.3 ships `.nav-underline` — underline tabs with transition. If the project has a custom tab style via `.nav-link` that draws `border-bottom: 2px solid` on the active state — that is `.nav-underline` written by hand.

### How to recognise it

```css
/* Tell-tale sign: border-bottom on nav-link + color change on .active */
.my-tabs .nav-link {
  border-bottom: 2px solid transparent;
  transition: color .18s ease, border-color .18s ease;
}
.my-tabs .nav-link.active {
  border-bottom-color: var(--bs-primary);
}
```

That is `.nav-underline`. The entire block goes in the trash.

### Replacement

```html
<!-- ❌ Before -->
<ul class="nav my-tabs">
  <li class="nav-item">
    <button class="nav-link active" ...>Tab 1</button>
  </li>
</ul>

<!-- ✅ After -->
<ul class="nav nav-underline">
  <li class="nav-item">
    <button class="nav-link active" ...>Tab 1</button>
  </li>
</ul>
```

The entire custom CSS block is deleted. Bootstrap handles color, `border-bottom`, transition, `:hover` and `.active` states on its own.

### If the active tab color differs from `--bs-primary`

Keep **one line** of override — that is all that remains from the entire custom tab block:

```css
/* The only thing that survives the entire custom tab block */
.rv-page .nav-underline .nav-link.active {
  color: var(--bs-primary); /* adjust only if brand color differs from BS primary */
  border-bottom-color: var(--bs-primary);
}
```

---

## 6. Phase 4 — Kill Structural Page CSS

### Global `body` override — always wrong

```css
/* ❌ This must not exist — breaks every other component on the page */
body {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
}
```

The component does not own `body`. If a font is needed, set it via the BS font variable on the widget container:

```css
/* ✅ Correct — scoped to the component only */
.rv-page {
  --bs-font-sans-serif: 'DM Sans', sans-serif;
  font-size: 0.9375rem; /* 15px as em */
}
```

In most cases even this is unnecessary — if the project's design system already sets the font globally.

### Custom centering container — replace with BS container

```css
/* ❌ Before — custom centering */
.rv-page { max-width: 860px; margin-inline: auto; }
```

Bootstrap has ready-made containers. Pick the closest one:

| BS class | Max-width | When to use |
|---|---|---|
| `container-sm` | 540px | narrow forms |
| `container-md` | 720px | medium widgets |
| `container-lg` | 960px | standard pages |
| `container-xl` | 1140px | wide dashboards |
| `container` | responsive | universal |

860px ≈ `container-lg` (960px). The 100px difference — accept it. Remove the custom `max-width`, add `container-lg` in HTML:

```html
<!-- ❌ Before -->
<div class="rv-page">

<!-- ✅ After -->
<div class="rv-page container-lg">
```

If `860px` is critical and `container-lg` does not work — override via a BS variable, not a custom class:

```css
/* Overriding a BS variable — not writing a custom class */
.rv-page { --bs-container-lg-max-width: 860px; }
```

---

## 7. Phase 5 — Clean JS Templates

When a component generates HTML via `innerHTML` in JS, classes live in strings like:

```js
return `<span class="rv-card-meta">${this._esc(p.date)}</span>`;
```

After deleting CSS rules, update these strings. The algorithm is the same: deleted class → BS utility in the template string.

### Safety rules

- Only **static** Bootstrap class strings go into JS templates. Dynamic values always via `_esc()` or `textContent` — never as part of a class attribute.
- Never: `` `class="${userInput}"` `` — that is XSS.
- Acceptable: `` `class="badge rounded-pill ${this._esc(badgeClass)}"` `` — only if `badgeClass` comes from a trusted config (`STATUS_MAP`), not from user input.

### Common template replacements

```js
// ❌ Before — custom classes
`<span class="rv-card-meta">${date}</span>`
`<p class="rv-card-text">${text}</p>`
`<h2 class="rv-card-title">${name}</h2>`
`<span class="rv-badge-status text-bg-success">Published</span>`
`<div class="rv-section-hdr">Label</div>`

// ✅ After — Bootstrap utilities
`<span class="small text-secondary">${date}</span>`
`<p class="mb-2">${text}</p>`
`<h2 class="fw-semibold">${name}</h2>`
`<span class="badge rounded-pill text-bg-success">Published</span>`
`<div class="small text-secondary text-uppercase fw-semibold">Label</div>`
```

### Outgoing-comment bg tint — move into JS template

If the component applies a background tint via a CSS selector `[data-comment-type="outgoing"]` with a custom token — remove the CSS, add the BS class directly in the JS template:

```js
// ❌ Before — CSS applies bg via data-attribute + custom color token
// CSS: .rv-comment-card[data-comment-type="outgoing"] { background: var(--rv-brand-soft); }
const cardClass = `rv-comment-card`;

// ✅ After — BS utility directly in the template, zero custom CSS
const tintClass = c.type === 'outgoing' ? 'bg-primary-subtle' : '';
const cardClass = `rv-card card rounded-3 ${tintClass}`;
```

---

## 8. Phase 6 — Verify States and Dark Mode

### Dark mode

Bootstrap 5.3 switches the theme via `data-bs-theme="dark"` on `<html>`. All `--bs-*` variables automatically change values. Custom `var(--rv-*)` tokens do not.

**Test:** add `data-bs-theme="dark"` to `<html>`, walk through the component visually. If anything breaks — a hardcoded color or a custom token without a dark-mode variant is lurking somewhere.

**Fix:** every remaining custom token must have a dark-mode override:

```css
.rv-page {
  --rv-star: #f59e0b; /* light theme — amber */
}

[data-bs-theme="dark"] .rv-page {
  --rv-star: #fbbf24; /* dark theme — slightly lighter */
}
```

For backgrounds and text — use only `--bs-*` semantic variables; they adapt automatically:

```css
/* ✅ Adapts to dark mode automatically */
background: var(--bs-body-bg);
color: var(--bs-body-color);
border-color: var(--bs-border-color);

/* ❌ Does not adapt */
background: #ffffff;
color: #212529;
```

### Verifying data-attribute state hooks

After refactoring, confirm JS still correctly sets `data-state` / `data-*` attributes that the remaining custom CSS depends on:

```js
// These mechanisms must work after the cleanup:
el.dataset.state = 'liked';          // → .rv-helpful-btn[data-state="liked"]
article.dataset.new = 'true';        // → .rv-card[data-new="true"] { animation }
picker.classList.add('is-invalid');  // → .rv-star-picker.is-invalid { animation }
```

### Verifying responsive

The only custom `@media` that typically survives is fixed pixel sizes for images and avatars on mobile. Bootstrap cannot change specific px sizes via utilities:

```css
/* Stays — no BS equivalent for exact thumb dimensions */
@media (max-width: 575.98px) {
  .rv-page .rv-product-thumb,
  .rv-page .rv-product-thumb-placeholder {
    width: 68px;
    height: 68px;
  }
}
```

---

## 9. Replacement Table: Tokens

| Custom token | Value | Bootstrap replacement |
|---|---|---|
| `--rv-brand` / `--custom-primary` | hex blue | `var(--bs-primary)` |
| `--rv-brand-soft` | light blue tint | `var(--bs-primary-subtle)` |
| `--rv-radius` | `8–14px` | `var(--bs-border-radius-lg)` (0.5rem) or `--bs-border-radius-xl` |
| `--rv-shadow` | light shadow | `var(--bs-box-shadow-sm)` |
| `--rv-shadow-hover` | hover shadow | `var(--bs-box-shadow)` |
| `--rv-transition` | `.18s ease` | kill, write inline where needed |
| `--rv-font` | font name | `--bs-font-sans-serif` on container |
| any `--*-success` | green | `var(--bs-success)` / `var(--bs-success-subtle)` |
| any `--*-danger` | red | `var(--bs-danger)` / `var(--bs-danger-subtle)` |
| any `--*-warning` | yellow | `var(--bs-warning)` / `var(--bs-warning-subtle)` |
| any `--*-info` | cyan | `var(--bs-info)` / `var(--bs-info-subtle)` |
| `--*-secondary-text` | gray text | `var(--bs-secondary-color)` |
| `--*-border` | border color | `var(--bs-border-color)` |
| `--*-bg` / `--*-surface` | background | `var(--bs-body-bg)` / `var(--bs-tertiary-bg)` |

---

## 10. Replacement Table: CSS Classes → BS Utilities

### Typography

| Custom class | What it does | BS utility |
|---|---|---|
| `.meta-label` / `.card-meta` | `font-size: 12–13px` | `small` |
| `.title` / `.heading` | `font-size: 20–22px` | `h5` / `fs-5` |
| `.subtitle` | `font-size: 13px` | `small text-secondary` |
| `.label-uppercase` | `text-transform: uppercase; letter-spacing` | `text-uppercase fw-semibold` |
| `.bold-text` | `font-weight: 700` | `fw-bold` |
| `.semibold-text` | `font-weight: 600` | `fw-semibold` |
| `.muted-text` | `color: gray` | `text-secondary` |
| `.hint-text` | `color: lighter gray` | `text-body-tertiary` |
| `.monospace` | `font-family: monospace` | `font-monospace` |
| `.truncate` | `overflow: hidden; text-overflow: ellipsis` | `text-truncate` (+ `mw-0` on flex parent) |
| `.break-word` | `word-break: break-word` | `text-break` |

### Spacing

| Custom style | BS utility |
|---|---|
| `padding: 16px` | `p-3` |
| `padding: 24px` | `p-4` |
| `padding: 48px 16px` | `py-5 px-3` |
| `margin-bottom: 8px` | `mb-2` |
| `margin-bottom: 16px` | `mb-3` |
| `margin-top: auto` | `mt-auto` |
| `gap: 8px` | `gap-2` |
| `gap: 16px` | `gap-3` |

### Display and alignment

| Custom style | BS utility |
|---|---|
| `display: none` | `d-none` |
| `display: flex; align-items: center` | `d-flex align-items-center` |
| `display: flex; justify-content: space-between` | `d-flex justify-content-between` |
| `flex-shrink: 0` | `flex-shrink-0` |
| `flex-grow: 1` | `flex-grow-1` |
| `min-width: 0` | `mw-0` (custom utility needed) |
| `text-align: center` | `text-center` |
| `opacity: 0.5` | `opacity-50` |
| `visibility: hidden` | `invisible` |
| `overflow: hidden` | `overflow-hidden` |
| `cursor: pointer` | use a `<button>` element |

### Colors and backgrounds

| Custom class | BS utility |
|---|---|
| `.bg-light-gray` / `.surface` | `bg-body-tertiary` |
| `.bg-white` | `bg-body` |
| `.bg-primary-tint` | `bg-primary-subtle` |
| `.bg-success-tint` | `bg-success-subtle` |
| `.text-gray` | `text-secondary` |
| `.text-blue` | `text-primary` |
| `.text-green` | `text-success` |
| `.text-red` | `text-danger` |

### Borders and shadows

| Custom style | BS utility |
|---|---|
| `border: 1px solid var(--bs-border-color)` | `border` |
| `border-top: 1px solid ...` | `border-top` |
| `border-radius: 8px` | `rounded-3` |
| `border-radius: 14px` | `rounded-4` |
| `border-radius: 50%` | `rounded-circle` |
| `border-radius: 999px` | `rounded-pill` |
| `box-shadow: small` | `shadow-sm` |
| `box-shadow: medium` | `shadow` |
| `box-shadow: large` | `shadow-lg` |
| `box-shadow: none` | `shadow-none` |

### Inline styles → BS utilities

| `style="..."` | BS utility |
|---|---|
| `style="font-size:.875rem"` | `small` or `fs-6` |
| `style="font-weight:600"` | `fw-semibold` |
| `style="font-weight:700"` | `fw-bold` |
| `style="color:#6c757d"` | `text-secondary` |
| `style="display:none"` | `d-none` |
| `style="text-align:center"` | `text-center` |
| `style="white-space:nowrap"` | `text-nowrap` |
| `style="word-break:break-word"` | `text-break` |
| `style="font-family:monospace"` | `font-monospace` |
| `style="opacity:.5"` | `opacity-50` |
| `style="cursor:pointer"` | use a `<button>` element |

---

## 11. Replacement Table: Components

### Buttons

```html
<!-- ❌ Custom button -->
<button class="custom-btn custom-btn-blue">Click</button>
<style>
.custom-btn { padding: 8px 16px; border-radius: 4px; border: none; cursor: pointer; }
.custom-btn-blue { background: #3498db; color: white; }
</style>

<!-- ✅ Bootstrap -->
<button class="btn btn-primary">Click</button>
```

### Badges / status labels

```html
<!-- ❌ Custom badge -->
<span class="status-badge status-published">Published</span>
<style>
.status-badge { padding: 3px 10px; border-radius: 999px; font-size: 11px; font-weight: 600; }
.status-published { background: #4bbf73; color: #fff; }
</style>

<!-- ✅ Bootstrap -->
<span class="badge rounded-pill text-bg-success">Published</span>
```

### Form inputs

```html
<!-- ❌ Custom input -->
<input class="custom-input" type="text">
<style>
.custom-input { border: 1px solid #ddd; border-radius: 4px; padding: 8px 12px;
                font-size: 14px; width: 100%; }
.custom-input:focus { border-color: #3498db; outline: none; }
</style>

<!-- ✅ Bootstrap -->
<input class="form-control" type="text">
```

### Underline tabs

```html
<!-- ❌ Custom underline tabs -->
<ul class="nav my-tabs">
  <li><button class="nav-link active">Tab</button></li>
</ul>

<!-- ✅ Bootstrap nav-underline (BS 5.3+) -->
<ul class="nav nav-underline">
  <li class="nav-item"><button class="nav-link active" ...>Tab</button></li>
</ul>
```

### Empty state

```html
<!-- ❌ Custom empty state -->
<div class="empty-state">
  <i class="bi bi-inbox"></i>
  <p class="empty-title">Nothing here</p>
  <p class="empty-sub">Items will appear here.</p>
</div>
<style>
.empty-state { text-align: center; padding: 3rem 1rem; }
.empty-state i { font-size: 44px; color: #aaa; display: block; margin-bottom: 1rem; }
.empty-title { font-weight: 600; margin-bottom: 4px; }
</style>

<!-- ✅ Bootstrap utilities only — zero custom CSS -->
<div class="text-center py-5 px-3">
  <i class="bi bi-inbox fs-1 text-secondary opacity-25 d-block mb-3"></i>
  <p class="fw-semibold mb-1">Nothing here</p>
  <p class="text-secondary small mb-0">Items will appear here.</p>
</div>
```

### Accordion with custom chevron

```html
<!-- ❌ Custom toggle with manually rotated arrow -->
<button class="my-toggle" aria-expanded="false">
  Title
  <span class="my-chevron">▾</span>
</button>
<style>
.my-chevron { transition: transform .2s; }
.my-toggle[aria-expanded="true"] .my-chevron { transform: rotate(180deg); }
</style>

<!-- ✅ Bootstrap accordion — chevron, transition, aria-expanded all automatic -->
<button class="accordion-button collapsed" type="button"
        data-bs-toggle="collapse" data-bs-target="#section-1">
  Title
</button>
```

### Search input group

```html
<!-- ❌ Custom search bar with a visible seam between icon and input -->
<div class="search-wrap">
  <span class="search-icon">🔍</span>
  <input class="search-input" type="text" placeholder="Search…">
</div>
<style>
.search-wrap { display: flex; border: 1px solid #ddd; border-radius: 20px; }
.search-icon { padding: 8px 12px; }
.search-input { border: none; outline: none; flex: 1; border-radius: 0 20px 20px 0; }
</style>

<!-- ✅ Bootstrap input-group -->
<div class="input-group">
  <span class="input-group-text bg-body-tertiary border-end-0 rounded-start-pill">
    <i class="bi bi-search text-secondary"></i>
  </span>
  <input type="search" class="form-control bg-body-tertiary border-start-0 rounded-end-pill"
         placeholder="Search…">
</div>
```

---

## 12. What Stays Custom — and Why

Not everything can be killed. This is the list of what **must** remain custom, with an explanation for each.

### Fixed image and avatar sizes

```css
/* KEEP — Bootstrap cannot set specific px dimensions via utilities */
.rv-page .rv-product-thumb {
  width: 92px;
  height: 92px;
  object-fit: contain;
  flex-shrink: 0;
  padding: 6px;
}
.rv-page .rv-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  flex-shrink: 0;
}
```

`w-25`, `w-50`, etc. are percentages, not pixels. For exact sizes, custom CSS is required.

### Rating progress bars with a CSS-variable width

```css
/* KEEP — width is driven by JS: el.style.setProperty('--rv-bar-pct', pct) */
.rv-page .rv-bar-track {
  height: 8px;
  border-radius: var(--bs-border-radius-pill);
  overflow: hidden;
}
.rv-page .rv-bar-fill {
  height: 100%;
  background: var(--rv-star);
  width: var(--rv-bar-pct, 0%);
  transition: width .5s ease;
}
```

Bootstrap's `progress` component does not support JS-driven width via CSS variables.

### Star picker (interactive, ARIA)

```css
/* KEEP — BS has no star-rating component */
.rv-star-picker span {
  font-size: 28px;
  cursor: pointer;
  color: var(--bs-border-color);
  transition: color .18s ease;
}
.rv-star-picker span.active  { color: var(--rv-star); }
.rv-star-picker span:focus-visible {
  outline: 2px solid var(--bs-primary);
  border-radius: 2px;
}
.rv-star-picker.is-invalid { animation: rv-shake 0.35s ease; }
```

### Hover shadow on cards

```css
/* KEEP — BS provides no hover-shadow utility */
.rv-page .rv-card:hover {
  box-shadow: var(--bs-box-shadow);
}
```

The base shadow goes via `shadow-sm` utility in HTML. The hover shadow stays as one custom line.

### Data-attribute state hooks

```css
/* KEEP — BS cannot change appearance via data-attributes */
.rv-page .rv-card[data-new="true"] {
  animation: rv-card-in 200ms ease both;
}
.rv-page .rv-helpful-btn[data-state="liked"] {
  opacity: 0.6;
  pointer-events: none;
}
```

### Keyframe animations

```css
/* KEEP — BS has no general keyframe animation system */
@keyframes rv-card-in {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes rv-shake {
  0%, 100% { transform: translateX(0); }
  20%      { transform: translateX(-6px); }
  60%      { transform: translateX(6px); }
}
```

Rules: animate only `transform` and `opacity` (compositor thread, no reflow). The `rv-` prefix on `@keyframes` names is mandatory — keyframe names are global.

---

## 13. Final Checklist

Run this before every commit.

### Tokens

- [ ] No `--custom-*` tokens on `:root` — all custom tokens are on `.widget-container`
- [ ] No tokens that duplicate Bootstrap (`--custom-primary` instead of `var(--bs-primary)`)
- [ ] Dynamic tokens (JS via `setProperty`) are untouched
- [ ] Remaining custom tokens have a `[data-bs-theme="dark"]` override

### CSS classes

- [ ] No classes whose only property is `font-size` — replaced with `small` / `fs-*`
- [ ] No duplicates — multiple classes with the same property sets
- [ ] No classes that only do what a BS utility already does
- [ ] Global `body { font-family; font-size }` override is gone
- [ ] Custom centering container replaced with a `container-*` class
- [ ] All `border-radius` via `var(--bs-border-radius-*)` or `rounded-*` utility
- [ ] All `box-shadow` via `var(--bs-box-shadow*)` or `shadow-*` utility

### HTML and JS templates

- [ ] No `style="..."` attributes (except dynamic values set from JS data)
- [ ] Badge/status classes replaced with `badge rounded-pill text-bg-*`
- [ ] Font-size classes in innerHTML templates replaced with `small`, `fs-*`
- [ ] Section header classes replaced with `small text-secondary text-uppercase fw-semibold`
- [ ] Empty state uses only BS utilities (`py-5 text-center fs-1 opacity-25`)
- [ ] `form-control-sm` used for small textareas instead of a custom `font-size`
- [ ] Custom `nav-link` styles with `border-bottom` replaced with `nav-underline`

### States and behaviour

- [ ] `data-state` / `data-*` attributes that the remaining CSS depends on are working
- [ ] `data-new` animation fires correctly on newly added cards
- [ ] `is-invalid` shake animation triggers correctly on the star picker
- [ ] Hover shadows work (custom `rv-card:hover` was not accidentally deleted)
- [ ] Like button in `liked` state styles via `[data-state="liked"]`

### Dark mode

- [ ] Add `data-bs-theme="dark"` to `<html>`, walk through the component visually
- [ ] No hardcoded hex colors in the remaining CSS
- [ ] No hardcoded `rgba(0,0,0,...)` — replaced with `rgba(var(--bs-dark-rgb), ...)`
- [ ] Remaining custom tokens (`--rv-star`) have a dark-mode value

### Responsive

- [ ] `@media` breakpoints use BS values: `575.98px`, `767.98px`, `991.98px`
- [ ] Thumbnail / avatar `@media` with specific px sizes are kept
- [ ] `prefers-reduced-motion` block for animations is kept

### Score

After cleanup the expected benchmark: **−60–70% declarations**. Less than that — something was not killed. More custom CSS than before — something was added that should not have been.

---

## Anti-patterns — never do these

```css
/* ❌ !important to fight Bootstrap */
.my-card { padding: 20px !important; }
/* Fix: use p-4 utility in HTML */

/* ❌ Duplicating a BS utility in a custom class */
.centered { text-align: center; }
.flex-center { display: flex; align-items: center; }
/* Fix: text-center, d-flex align-items-center */

/* ❌ Hardcoded hex instead of a BS variable */
.label { color: #6c757d; }
/* Fix: color: var(--bs-secondary-color); or text-secondary utility */

/* ❌ Global Bootstrap component override */
.card { border-radius: 12px; }
/* Fix: add rounded-4 in HTML on the specific cards that need it */

/* ❌ Custom breakpoint that does not match BS */
@media (max-width: 800px) { ... }
/* Fix: @media (max-width: 767.98px) — the BS md breakpoint */
```

---

*Guide written based on the audit of `my-reviews-5e.html` — applicable to any Bootstrap 5.3+ component.*
*Version: 1.0 — Bootstrap 5.3+*
