# The Complete Bootstrap 5.3 Customization Guide

> A comprehensive reference for developers who want to go beyond Bootstrap's defaults and build fully custom, branded UIs.

---

## Table of Contents

1. [How Bootstrap's Architecture Works](#1-how-bootstraps-architecture-works)
2. [Setup: Sass Compilation Pipeline](#2-setup-sass-compilation-pipeline)
3. [Overriding Default Variables](#3-overriding-default-variables)
4. [The Color System](#4-the-color-system)
5. [Dark Mode & Color Modes](#5-dark-mode--color-modes)
6. [Typography Customization](#6-typography-customization)
7. [Spacing & Sizing](#7-spacing--sizing)
8. [Breakpoints & Grid](#8-breakpoints--grid)
9. [Component Customization](#9-component-customization)
10. [CSS Custom Properties (Variables)](#10-css-custom-properties-variables)
11. [Utility API — Creating Your Own Utilities](#11-utility-api--creating-your-own-utilities)
12. [Selective Imports — Reducing Bundle Size](#12-selective-imports--reducing-bundle-size)
13. [Custom Themes from Scratch](#13-custom-themes-from-scratch)
14. [JavaScript Customization](#14-javascript-customization)
15. [RTL Support](#15-rtl-support)
16. [Build Tools & Optimization](#16-build-tools--optimization)
17. [Real-World Examples](#17-real-world-examples)
18. [Common Pitfalls & Troubleshooting](#18-common-pitfalls--troubleshooting)

---

## 1. How Bootstrap's Architecture Works

Understanding the internals makes customization predictable rather than trial-and-error.

### Sass Layer Order

Bootstrap is built in layers. When you compile it, the order matters:

```
1. functions      — pure Sass helpers (color-contrast, tint, shade…)
2. variables      — ALL default values (use !default so you can override)
3. mixins         — reusable patterns (breakpoints, grid, transitions…)
4. maps           — theme colors, spacers, font sizes as Sass maps
5. utilities      — utility class definitions
6. components     — buttons, cards, modals, navbars…
```

Every variable in Bootstrap is declared with `!default`, which means Sass only sets it **if no value has been assigned yet**. This is the hook for all customization: you declare your overrides **before** importing Bootstrap.

### Where Things Live (npm install)

```
node_modules/bootstrap/
  scss/
    _variables.scss       ← all ~600 variables live here
    _variables-dark.scss  ← dark mode overrides
    _maps.scss            ← Sass maps built from variables
    _mixins.scss
    _utilities.scss       ← Utility API definitions
    bootstrap.scss        ← main entry, imports everything
    bootstrap-grid.scss   ← grid only
    bootstrap-utilities.scss ← utilities only
    bootstrap-reboot.scss ← reboot/reset only
  dist/
    css/bootstrap.min.css
    js/bootstrap.bundle.min.js
```

---

## 2. Setup: Sass Compilation Pipeline

### Prerequisites

```bash
npm install bootstrap
npm install --save-dev sass  # or node-sass, dart-sass preferred
```

### Recommended File Structure

```
your-project/
  scss/
    custom.scss       ← YOUR entry point
    _variables.scss   ← your variable overrides
    _components.scss  ← your component overrides
    _utilities.scss   ← custom utilities
  css/
    main.css          ← compiled output
```

### custom.scss — The Correct Import Order

```scss
// 1. Your variable overrides (MUST come before Bootstrap functions/variables)
@import "variables";

// 2. Bootstrap functions (needed before variables)
@import "../node_modules/bootstrap/scss/functions";

// 3. Bootstrap default variables (your overrides above will win due to !default)
@import "../node_modules/bootstrap/scss/variables";
@import "../node_modules/bootstrap/scss/variables-dark";

// 4. Maps (built from variables — after variables)
@import "../node_modules/bootstrap/scss/maps";

// 5. Mixins
@import "../node_modules/bootstrap/scss/mixins";
@import "../node_modules/bootstrap/scss/utilities";

// 6. Layout & base
@import "../node_modules/bootstrap/scss/root";
@import "../node_modules/bootstrap/scss/reboot";
@import "../node_modules/bootstrap/scss/type";
@import "../node_modules/bootstrap/scss/images";
@import "../node_modules/bootstrap/scss/containers";
@import "../node_modules/bootstrap/scss/grid";
@import "../node_modules/bootstrap/scss/helpers";

// 7. Components (only import what you need)
@import "../node_modules/bootstrap/scss/transitions";
@import "../node_modules/bootstrap/scss/dropdown";
@import "../node_modules/bootstrap/scss/button-group";
@import "../node_modules/bootstrap/scss/nav";
@import "../node_modules/bootstrap/scss/navbar";
@import "../node_modules/bootstrap/scss/card";
@import "../node_modules/bootstrap/scss/accordion";
@import "../node_modules/bootstrap/scss/breadcrumb";
@import "../node_modules/bootstrap/scss/pagination";
@import "../node_modules/bootstrap/scss/badge";
@import "../node_modules/bootstrap/scss/alert";
@import "../node_modules/bootstrap/scss/progress";
@import "../node_modules/bootstrap/scss/list-group";
@import "../node_modules/bootstrap/scss/close";
@import "../node_modules/bootstrap/scss/toasts";
@import "../node_modules/bootstrap/scss/modal";
@import "../node_modules/bootstrap/scss/tooltip";
@import "../node_modules/bootstrap/scss/popover";
@import "../node_modules/bootstrap/scss/spinners";
@import "../node_modules/bootstrap/scss/offcanvas";
@import "../node_modules/bootstrap/scss/placeholders";

// 8. Utilities (last so they can override components)
@import "../node_modules/bootstrap/scss/utilities/api";

// 9. Your custom components & utility additions
@import "components";
@import "utilities";
```

### Compile Command

```bash
# One-time
npx sass scss/custom.scss css/main.css --style=compressed

# Watch mode
npx sass --watch scss/custom.scss:css/main.css

# With source maps for debugging
npx sass --watch --source-map scss/custom.scss:css/main.css
```

---

## 3. Overriding Default Variables

All overrides go in your `_variables.scss` BEFORE Bootstrap's variables are imported.

### The Golden Rule

```scss
// ✅ Correct — defined before Bootstrap variables are imported
$primary: #6f42c1;

// ❌ Wrong — defined after; Bootstrap's !default already set the value
@import "bootstrap/scss/variables";
$primary: #6f42c1; // too late, has no effect
```

### Key Variables Reference

```scss
// ─── Colors ───────────────────────────────────────────
$primary:       #0d6efd;
$secondary:     #6c757d;
$success:       #198754;
$info:          #0dcaf0;
$warning:       #ffc107;
$danger:        #dc3545;
$light:         #f8f9fa;
$dark:          #212529;

// ─── Body ──────────────────────────────────────────────
$body-bg:                 #fff;
$body-color:              #212529;
$body-emphasis-color:     $black;
$body-secondary-color:    rgba($body-color, .75);
$body-tertiary-color:     rgba($body-color, .5);
$body-tertiary-bg:        #f8f9fa;

// ─── Links ─────────────────────────────────────────────
$link-color:              $primary;
$link-decoration:         underline;
$link-hover-color:        shift-color($link-color, $link-shade-percentage);
$link-shade-percentage:   20%;

// ─── Typography ────────────────────────────────────────
$font-family-sans-serif:  system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
$font-family-monospace:   SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace;
$font-family-base:        $font-family-sans-serif;
$font-size-root:          null;      // affects rem base
$font-size-base:          1rem;      // 16px by default
$font-size-sm:            $font-size-base * .875;
$font-size-lg:            $font-size-base * 1.25;
$font-weight-lighter:     lighter;
$font-weight-light:       300;
$font-weight-normal:      400;
$font-weight-medium:      500;
$font-weight-semibold:    600;
$font-weight-bold:        700;
$font-weight-bolder:      bolder;
$font-weight-base:        $font-weight-normal;
$line-height-base:        1.5;
$line-height-sm:          1.25;
$line-height-lg:          2;

// ─── Headings ──────────────────────────────────────────
$h1-font-size:            $font-size-base * 2.5;
$h2-font-size:            $font-size-base * 2;
$h3-font-size:            $font-size-base * 1.75;
$h4-font-size:            $font-size-base * 1.5;
$h5-font-size:            $font-size-base * 1.25;
$h6-font-size:            $font-size-base;
$headings-font-family:    null;
$headings-font-weight:    500;
$headings-color:          inherit;

// ─── Spacing ───────────────────────────────────────────
$spacer:    1rem;
$spacers: (
  0: 0,
  1: $spacer * .25,
  2: $spacer * .5,
  3: $spacer,
  4: $spacer * 1.5,
  5: $spacer * 3,
);

// ─── Border ────────────────────────────────────────────
$border-width:            1px;
$border-widths: (
  1: 1px,
  2: 2px,
  3: 3px,
  4: 4px,
  5: 5px,
);
$border-style:            solid;
$border-color:            #dee2e6;
$border-radius:           .375rem;
$border-radius-sm:        .25rem;
$border-radius-lg:        .5rem;
$border-radius-xl:        1rem;
$border-radius-xxl:       2rem;
$border-radius-pill:      50rem;

// ─── Shadows ───────────────────────────────────────────
$box-shadow:              0 .5rem 1rem rgba($black, .15);
$box-shadow-sm:           0 .125rem .25rem rgba($black, .075);
$box-shadow-lg:           0 1rem 3rem rgba($black, .175);
$box-shadow-inset:        inset 0 1px 2px rgba($black, .075);

// ─── Z-index ───────────────────────────────────────────
$zindex-dropdown:         1000;
$zindex-sticky:           1020;
$zindex-fixed:            1030;
$zindex-offcanvas:        1045;
$zindex-modal-backdrop:   1050;
$zindex-modal:            1055;
$zindex-popover:          1070;
$zindex-tooltip:          1080;
$zindex-toast:            1090;

// ─── Transitions ───────────────────────────────────────
$transition-base:         all .2s ease-in-out;
$transition-fade:         opacity .15s linear;
$transition-collapse:     height .35s ease;
$transition-collapse-width: width .35s ease;

// ─── Buttons ───────────────────────────────────────────
$btn-padding-y:           .375rem;
$btn-padding-x:           .75rem;
$btn-font-size:           $font-size-base;
$btn-border-radius:       $border-radius;
$btn-border-width:        $border-width;
$btn-font-weight:         $font-weight-normal;
$btn-box-shadow:          inset 0 1px 0 rgba($white, .15), 0 1px 1px rgba($black, .075);
$btn-transition:          color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;

// ─── Cards ─────────────────────────────────────────────
$card-spacer-y:           1rem;
$card-spacer-x:           1rem;
$card-border-width:       $border-width;
$card-border-color:       rgba($black, .175);
$card-border-radius:      $border-radius;
$card-box-shadow:         null;
$card-bg:                 $white;

// ─── Navbar ────────────────────────────────────────────
$navbar-padding-y:        $spacer * .5;
$navbar-padding-x:        null;
$navbar-brand-font-size:  $font-size-lg;
$navbar-toggler-padding-y: .25rem;
$navbar-toggler-padding-x: .75rem;
$navbar-toggler-border-radius: $btn-border-radius;

// ─── Modals ────────────────────────────────────────────
$modal-inner-padding:     1rem;
$modal-header-padding:    1rem 1rem;
$modal-sm:                300px;
$modal-md:                500px;
$modal-lg:                800px;
$modal-xl:                1140px;
$modal-backdrop-bg:       $black;
$modal-backdrop-opacity:  .5;
```

---

## 4. The Color System

### Theme Colors Map

Bootstrap uses a Sass map called `$theme-colors` to generate color variants across components and utilities. You can override it completely or merge your own colors into it.

```scss
// Option A: Replace specific theme colors
$primary:   #7c3aed;   // violet
$success:   #059669;   // emerald

// Option B: Extend the theme colors map
$theme-colors: (
  "primary":    $primary,
  "secondary":  $secondary,
  "success":    $success,
  "info":       $info,
  "warning":    $warning,
  "danger":     $danger,
  "light":      $light,
  "dark":       $dark,
  // Add your brand colors:
  "brand":      #7c3aed,
  "accent":     #f59e0b,
  "muted":      #6b7280,
);
```

After adding "brand" to `$theme-colors`, Bootstrap will automatically generate:
- `.btn-brand`, `.btn-outline-brand`
- `.text-brand`, `.bg-brand`
- `.border-brand`
- `.alert-brand`
- `.badge bg-brand`

### Gray Scale

```scss
$white:    #fff;
$gray-100: #f8f9fa;
$gray-200: #e9ecef;
$gray-300: #dee2e6;
$gray-400: #ced4da;
$gray-500: #adb5bd;
$gray-600: #6c757d;
$gray-700: #495057;
$gray-800: #343a40;
$gray-900: #212529;
$black:    #000;

$grays: (
  "100": $gray-100,
  "200": $gray-200,
  // ... add custom steps
);
```

### Color Functions

Bootstrap ships with several Sass color helpers in `_functions.scss`:

```scss
// tint: mix color with white
tint-color($color, $weight)     // tint-color($primary, 80%) → very light primary

// shade: mix color with black
shade-color($color, $weight)    // shade-color($primary, 20%) → darker primary

// shift-color: positive = shade, negative = tint
shift-color($color, $weight)

// Best contrast (returns black or white for text on a background)
color-contrast($background)
```

**Practical example — generating a full color palette:**

```scss
$brand: #7c3aed;

$theme-colors: map-merge($theme-colors, ("brand": $brand));

// These utility classes are then auto-generated:
// .bg-brand         → background: #7c3aed
// .text-brand       → color: #7c3aed
// .btn-brand        → filled button
// .btn-outline-brand → outlined button
// .border-brand     → border color
```

### Subtle Colors (Bootstrap 5.3+)

Bootstrap 5.3 introduced subtle background and border colors for each theme color:

```scss
// Auto-generated maps in _maps.scss:
// $theme-colors-text    → text color variants
// $theme-colors-bg-subtle  → very light backgrounds
// $theme-colors-border-subtle → light borders

// They produce classes like:
// .text-primary-emphasis
// .bg-primary-subtle
// .border-primary-subtle
```

---

## 5. Dark Mode & Color Modes

Bootstrap 5.3 introduced a first-class color mode system using `data-bs-theme`.

### Enabling Dark Mode

The simplest way — add `data-bs-theme="dark"` to `<html>`:

```html
<html lang="en" data-bs-theme="dark">
```

Or apply it to any element to scope dark mode:

```html
<div data-bs-theme="dark">
  <!-- Everything inside is dark themed -->
</div>
```

### How It Works Internally

Bootstrap stores color-mode-sensitive values in CSS custom properties. The `:root[data-bs-theme="dark"]` selector overrides them:

```scss
// _variables-dark.scss (simplified)
:root,
[data-bs-theme="light"] {
  --bs-body-color: #{$body-color};
  --bs-body-bg: #{$body-bg};
  // ...
}

[data-bs-theme="dark"] {
  --bs-body-color: #{$body-color-dark};
  --bs-body-bg: #{$body-bg-dark};
  // ...
}
```

### Customizing Dark Mode Colors

```scss
// _variables.scss — dark mode specific overrides
$body-bg-dark:              #1a1a2e;
$body-color-dark:           #e2e8f0;
$body-secondary-bg-dark:    #16213e;
$body-tertiary-bg-dark:     #0f3460;

$border-color-dark:         #334155;
$border-color-translucent-dark: rgba(255, 255, 255, .15);

$headings-color-dark:       inherit;
$link-color-dark:           tint-color($primary, 40%);
$code-color-dark:           tint-color($code-color, 40%);
```

### Adding a Custom Color Mode

You can create your own mode (e.g., "high-contrast"):

```scss
[data-bs-theme="high-contrast"] {
  --bs-body-bg: #000;
  --bs-body-color: #fff;
  --bs-primary-rgb: 255, 255, 0;
  --bs-border-color: #fff;
  // override whatever you need
}
```

```html
<html data-bs-theme="high-contrast">
```

### Toggling Color Modes with JavaScript

```javascript
const toggle = document.getElementById('theme-toggle');
const html = document.documentElement;

toggle.addEventListener('click', () => {
  const current = html.getAttribute('data-bs-theme');
  html.setAttribute('data-bs-theme', current === 'dark' ? 'light' : 'dark');
  // Persist choice:
  localStorage.setItem('theme', html.getAttribute('data-bs-theme'));
});

// On load, restore saved preference
const saved = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
html.setAttribute('data-bs-theme', saved ?? (prefersDark ? 'dark' : 'light'));
```

---

## 6. Typography Customization

### Custom Font Family

```scss
// Google Fonts example
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

$font-family-sans-serif: 'Inter', system-ui, -apple-system, sans-serif;
$font-family-monospace:  'JetBrains Mono', 'Fira Code', monospace;
$font-family-base:       $font-family-sans-serif;

// Heading-specific font
$headings-font-family:   'Playfair Display', Georgia, serif;
$headings-font-weight:   700;
$headings-line-height:   1.2;
```

### Font Scale

```scss
// Change base size (all rem values scale proportionally)
$font-size-base: 1rem;     // 16px — default
$font-size-base: 1.0625rem; // 17px — slightly larger for readability

// Customize heading sizes
$h1-font-size: clamp(2rem, 5vw, 3.5rem);  // fluid typography
$h2-font-size: clamp(1.5rem, 4vw, 2.5rem);
$h3-font-size: $font-size-base * 1.75;
```

### Display Headings

```scss
$display-font-sizes: (
  1: 5rem,
  2: 4.5rem,
  3: 4rem,
  4: 3.5rem,
  5: 3rem,
  6: 2.5rem,
);
$display-font-weight: 300;
$display-line-height: $headings-line-height;
```

### Lead, Small, and Other Text

```scss
$lead-font-size:    $font-size-base * 1.25;
$lead-font-weight:  300;
$small-font-size:   .875em;
$sub-sup-font-size: .75em;
$text-muted:        var(--#{$prefix}secondary-color);
$initialism-font-size: $small-font-size;
```

---

## 7. Spacing & Sizing

### Extending the Spacer Scale

Bootstrap's default spacers go from 0–5. You can add more:

```scss
$spacer: 1rem;
$spacers: (
  0:  0,
  1:  $spacer * .25,   // 4px
  2:  $spacer * .5,    // 8px
  3:  $spacer,         // 16px
  4:  $spacer * 1.5,   // 24px
  5:  $spacer * 3,     // 48px
  // Custom additions:
  6:  $spacer * 4,     // 64px
  7:  $spacer * 5,     // 80px
  8:  $spacer * 6,     // 96px
  "px": 1px,
  "0-5": $spacer * .125,
);
```

This automatically generates `mt-6`, `pb-7`, `gap-8`, `px-0-5`, etc.

### Container Widths

```scss
$container-max-widths: (
  sm:  540px,
  md:  720px,
  lg:  960px,
  xl:  1140px,
  xxl: 1320px,
  // Add your own:
  xxxl: 1600px,
);
```

### Container Padding

```scss
$container-padding-x: 1.5rem; // default is 0.75rem per side (gutter/2)
```

---

## 8. Breakpoints & Grid

### Custom Breakpoints

```scss
$grid-breakpoints: (
  xs:  0,
  sm:  576px,
  md:  768px,
  lg:  992px,
  xl:  1200px,
  xxl: 1400px,
  // Add a custom breakpoint:
  xxxl: 1600px,
);
```

If you add a new breakpoint, also add a container width for it:

```scss
$container-max-widths: (
  sm:   540px,
  md:   720px,
  lg:   960px,
  xl:   1140px,
  xxl:  1320px,
  xxxl: 1500px,
);
```

Bootstrap's mixins will automatically generate responsive classes for your new breakpoint: `.col-xxxl-6`, `.d-xxxl-flex`, `.mt-xxxl-5`, etc.

### Grid Configuration

```scss
$grid-columns:      12;   // number of columns
$grid-gutter-width: 1.5rem; // space between columns
$grid-row-columns:  6;    // max for .row-cols-* classes
```

### Using Breakpoint Mixins

```scss
// In your custom SCSS, use Bootstrap's breakpoint mixins:

// Styles for sm and up
@include media-breakpoint-up(sm) {
  .my-component { font-size: 1.2rem; }
}

// Styles for md and down
@include media-breakpoint-down(md) {
  .my-component { padding: .5rem; }
}

// Styles only between breakpoints
@include media-breakpoint-between(md, xl) {
  .my-component { display: flex; }
}

// Styles for exactly one breakpoint
@include media-breakpoint-only(lg) {
  .my-component { background: red; }
}
```

---

## 9. Component Customization

### Buttons

```scss
// Global button defaults
$btn-padding-y:        .5rem;
$btn-padding-x:        1.25rem;
$btn-font-size:        $font-size-base;
$btn-font-weight:      600;
$btn-border-radius:    2rem;       // pill-style by default
$btn-transition:       all .2s ease-in-out;
$btn-focus-box-shadow: 0 0 0 .25rem rgba($primary, .25);

// Size variants
$btn-padding-y-sm:     .25rem;
$btn-padding-x-sm:     .75rem;
$btn-font-size-sm:     $font-size-sm;
$btn-padding-y-lg:     .75rem;
$btn-padding-x-lg:     1.5rem;
$btn-font-size-lg:     $font-size-lg;
```

**Adding a custom button variant using the mixin:**

```scss
// After Bootstrap is imported, create a new variant
.btn-gradient {
  @include button-variant(
    // background, border, color, hover-bg, hover-border, hover-color, ...
    linear-gradient(135deg, #6f42c1, #e83e8c),
    transparent,
    $white
  );
  border: none;
}
```

### Navbar

```scss
$navbar-padding-y:              $spacer * .5;
$navbar-brand-font-size:        1.5rem;
$navbar-brand-font-weight:      700;
$navbar-toggler-border-radius:  .25rem;

// Light navbar
$navbar-light-color:            rgba($black, .55);
$navbar-light-hover-color:      rgba($black, .7);
$navbar-light-active-color:     rgba($black, .9);
$navbar-light-toggler-border-color: rgba($black, .1);
$navbar-light-brand-color:      rgba($black, .9);

// Dark navbar
$navbar-dark-color:             rgba($white, .55);
$navbar-dark-hover-color:       rgba($white, .75);
$navbar-dark-active-color:      $white;
$navbar-dark-toggler-border-color: rgba($white, .1);
$navbar-dark-brand-color:       $white;
```

### Cards

```scss
$card-spacer-y:             1.25rem;
$card-spacer-x:             1.25rem;
$card-title-spacer-y:       .5rem;
$card-border-width:         $border-width;
$card-border-color:         rgba($black, .125);
$card-border-radius:        $border-radius-lg;
$card-box-shadow:           $box-shadow-sm;
$card-inner-border-radius:  subtract($card-border-radius, $card-border-width);
$card-cap-padding-y:        .75rem;
$card-cap-padding-x:        $card-spacer-x;
$card-cap-bg:               rgba($black, .03);
$card-height:               null;
$card-bg:                   var(--#{$prefix}body-bg);
$card-img-overlay-padding:  1rem;
$card-group-margin:         $grid-gutter-width * .5;
```

### Forms

```scss
$form-label-margin-bottom:         .5rem;
$form-label-font-size:             null;
$form-label-font-weight:           null;

$input-padding-y:                  $input-btn-padding-y;
$input-padding-x:                  $input-btn-padding-x;
$input-font-size:                  $input-btn-font-size;
$input-border-width:               $input-btn-border-width;
$input-border-color:               $gray-400;
$input-border-radius:              $border-radius;
$input-bg:                         $white;
$input-color:                      $gray-900;
$input-focus-border-color:         tint-color($primary, 50%);
$input-focus-box-shadow:           0 0 0 .25rem rgba($primary, .25);
$input-placeholder-color:          $gray-500;
$input-disabled-bg:                $gray-200;
$input-disabled-border-color:      null;

// Validation states
$form-feedback-valid-color:        $success;
$form-feedback-invalid-color:      $danger;
$form-feedback-icon-valid-color:   $form-feedback-valid-color;
$form-feedback-icon-invalid-color: $form-feedback-invalid-color;
```

### Modals

```scss
$modal-inner-padding:          1.5rem;
$modal-footer-margin-between:  .5rem;
$modal-dialog-margin:          .5rem;
$modal-dialog-margin-y-sm-up:  1.75rem;
$modal-title-line-height:      $line-height-base;
$modal-content-color:          null;
$modal-content-bg:             $white;
$modal-content-border-color:   rgba($black, .2);
$modal-content-border-width:   $border-width;
$modal-content-border-radius:  $border-radius-lg;
$modal-content-box-shadow-xs:  $box-shadow-sm;
$modal-content-box-shadow-sm-up: $box-shadow;
$modal-backdrop-bg:            $black;
$modal-backdrop-opacity:       .5;
$modal-header-border-color:    $border-color;
$modal-footer-border-color:    $modal-header-border-color;
$modal-header-border-width:    $modal-content-border-width;
$modal-footer-border-width:    $modal-header-border-width;
$modal-header-padding-y:       $modal-inner-padding;
$modal-header-padding-x:       $modal-inner-padding;
```

### Alerts

```scss
$alert-padding-y:               1rem;
$alert-padding-x:               1rem;
$alert-margin-bottom:           1rem;
$alert-border-radius:           $border-radius;
$alert-link-font-weight:        $font-weight-bold;
$alert-border-width:            $border-width;
$alert-dismissible-padding-r:   3rem;
$alert-bg-scale:                -80%;  // how light the subtle background is
$alert-border-scale:            -70%;
$alert-color-scale:             40%;
```

### Badges, Progress, Tooltips

```scss
// Badges
$badge-font-size:         .75em;
$badge-font-weight:       $font-weight-bold;
$badge-color:             $white;
$badge-padding-y:         .35em;
$badge-padding-x:         .65em;
$badge-border-radius:     $border-radius;

// Progress
$progress-height:                   1rem;
$progress-font-size:                $font-size-base * .75;
$progress-bg:                       $gray-200;
$progress-border-radius:            $border-radius;
$progress-box-shadow:               $box-shadow-inset;
$progress-bar-color:                $white;
$progress-bar-bg:                   $primary;
$progress-bar-animation-timing:     1s linear infinite;
$progress-bar-transition:           width .6s ease;

// Tooltips
$tooltip-font-size:       $font-size-sm;
$tooltip-max-width:       200px;
$tooltip-color:           var(--#{$prefix}body-bg);
$tooltip-bg:              var(--#{$prefix}emphasis-color);
$tooltip-border-radius:   $border-radius;
$tooltip-opacity:         .9;
$tooltip-padding-y:       .25rem;
$tooltip-padding-x:       .5rem;
```

---

## 10. CSS Custom Properties (Variables)

Bootstrap 5.3 extensively uses CSS custom properties for runtime theming. These can be overridden without recompiling Sass.

### Where Bootstrap Defines CSS Variables

```css
:root,
[data-bs-theme="light"] {
  /* Colors */
  --bs-blue: #0d6efd;
  --bs-primary: #0d6efd;
  --bs-primary-rgb: 13, 110, 253;

  /* Body */
  --bs-body-color: #212529;
  --bs-body-color-rgb: 33, 37, 41;
  --bs-body-bg: #fff;
  --bs-body-bg-rgb: 255, 255, 255;
  --bs-body-font-family: system-ui, ...;
  --bs-body-font-size: 1rem;
  --bs-body-font-weight: 400;
  --bs-body-line-height: 1.5;

  /* Borders */
  --bs-border-width: 1px;
  --bs-border-style: solid;
  --bs-border-color: #dee2e6;
  --bs-border-radius: 0.375rem;
  --bs-border-radius-sm: 0.25rem;
  --bs-border-radius-lg: 0.5rem;
  --bs-border-radius-xl: 1rem;
  --bs-border-radius-xxl: 2rem;
  --bs-border-radius-pill: 50rem;

  /* Shadows */
  --bs-box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  --bs-box-shadow-sm: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  --bs-box-shadow-lg: 0 1rem 3rem rgba(0, 0, 0, 0.175);

  /* Focus */
  --bs-focus-ring-width: 0.25rem;
  --bs-focus-ring-opacity: 0.25;
  --bs-focus-ring-color: rgba(13, 110, 253, 0.25);
}
```

### Overriding CSS Variables at Runtime

This is the key technique for JavaScript-driven theming — no Sass recompilation needed:

```javascript
// Globally change primary color
document.documentElement.style.setProperty('--bs-primary', '#7c3aed');
document.documentElement.style.setProperty('--bs-primary-rgb', '124, 58, 237');

// Change border radius globally
document.documentElement.style.setProperty('--bs-border-radius', '0');      // sharp
document.documentElement.style.setProperty('--bs-border-radius-sm', '0');
document.documentElement.style.setProperty('--bs-border-radius-lg', '0');
```

### Component-Level CSS Variable Override

Individual components expose their own CSS variables. Override them on the element:

```html
<!-- Override card variables just for this card -->
<div class="card" style="
  --bs-card-bg: #1e293b;
  --bs-card-border-color: #334155;
  --bs-card-color: #e2e8f0;
">
```

```scss
// Or in SCSS — scoped to a specific element
.my-special-card {
  --bs-card-bg: #f0fdf4;
  --bs-card-border-color: #bbf7d0;
  --bs-card-cap-bg: #dcfce7;
}
```

**Component CSS variable prefixes to know:**
- Buttons: `--bs-btn-*`
- Cards: `--bs-card-*`
- Navbars: `--bs-navbar-*`
- Modals: `--bs-modal-*`
- Dropdowns: `--bs-dropdown-*`
- Alerts: `--bs-alert-*`
- Tables: `--bs-table-*`
- Badges: `--bs-badge-*`
- Progress: `--bs-progress-*`

---

## 11. Utility API — Creating Your Own Utilities

Bootstrap's Utility API is one of its most powerful features. It lets you generate utility classes from a Sass map with full responsive and state variant support.

### How the Utility API Works

Each entry in `$utilities` describes a utility class:

```scss
$utilities: (
  "opacity": (
    property: opacity,
    values: (
      0:   0,
      25:  .25,
      50:  .5,
      75:  .75,
      100: 1,
    )
  ),
  // → generates .opacity-0, .opacity-25, .opacity-50, .opacity-75, .opacity-100
);
```

### Adding Custom Utilities

```scss
// In your custom utilities file, after importing Bootstrap utilities:
$utilities: map-merge(
  $utilities,
  (
    // Custom width utility
    "width": (
      property: width,
      class: w,
      values: (
        25:  25%,
        33:  33.333%,
        50:  50%,
        66:  66.666%,
        75:  75%,
        100: 100%,
        auto: auto,
      ),
      responsive: true,
    ),

    // Custom text shadow utility
    "text-shadow": (
      property: text-shadow,
      class: text-shadow,
      values: (
        "none": none,
        "sm":   0 1px 2px rgba(0,0,0,.2),
        "md":   0 2px 8px rgba(0,0,0,.3),
        "lg":   0 4px 16px rgba(0,0,0,.4),
      ),
    ),

    // Cursor utility with responsive + hover state
    "cursor": (
      property: cursor,
      class: cursor,
      values: auto default pointer wait text move not-allowed,
      responsive: true,
    ),

    // Aspect ratio (fill gaps in Bootstrap's defaults)
    "aspect-ratio": (
      property: aspect-ratio,
      class: ratio,
      values: (
        "1x1":   1 / 1,
        "4x3":   4 / 3,
        "16x9":  16 / 9,
        "21x9":  21 / 9,
        "2x1":   2 / 1,
      ),
    ),

    // Transition utility
    "transition": (
      property: transition,
      class: transition,
      values: (
        "none":  none,
        "all":   all .2s ease-in-out,
        "color": color .2s ease-in-out,
      ),
    ),
  )
);
```

### Utility API Options

```scss
"utility-name": (
  // Required
  property: css-property-name,     // e.g. margin, display, color
  values: (...),                    // map or list of values

  // Optional
  class: "custom-class-prefix",    // default: utility name
  css-var: true,                   // output as CSS var instead of property
  css-variable-name: "my-var",     // CSS var name
  local-vars: (...),               // local CSS vars to define per value
  state: hover focus,              // generate :hover, :focus variants
  responsive: true,                // generate sm:, md:, lg:, xl:, xxl: variants
  rfs: true,                       // enable responsive font-size
  print: true,                     // generate print- variants
  rtl: false,                      // exclude from RTL
),
```

### Modifying or Removing Existing Utilities

```scss
// Disable an existing utility
$utilities: map-merge(
  $utilities,
  ("float": map-merge(map-get($utilities, "float"), (print: true)))
);

// Remove a utility entirely
$utilities: map-remove($utilities, "float");

// Add more values to an existing utility
$utilities: map-merge(
  $utilities,
  (
    "opacity": map-merge(
      map-get($utilities, "opacity"),
      (
        values: map-merge(
          map-get(map-get($utilities, "opacity"), "values"),
          (10: .10, 20: .20, 30: .30, 40: .40, 60: .60, 70: .70, 80: .80, 90: .90)
        )
      )
    )
  )
);
```

### Enabling Responsive Variants

By default many Bootstrap utilities are not responsive. Enable them:

```scss
// Make opacity responsive
$utilities: map-merge(
  $utilities,
  (
    "opacity": map-merge(
      map-get($utilities, "opacity"),
      (responsive: true)
    )
  )
);
// Now you can use: .opacity-50.opacity-md-100
```

### State Variants

```scss
$utilities: map-merge(
  $utilities,
  (
    "background-color": map-merge(
      map-get($utilities, "background-color"),
      (state: hover focus)
    )
  )
);
// Generates: .bg-primary:hover, .bg-primary:focus
// Usage: <a class="bg-primary hover:bg-secondary"> (not quite — use class="bg-primary bg-hover-secondary")
```

---

## 12. Selective Imports — Reducing Bundle Size

Only importing what you use can dramatically reduce CSS output.

### Minimal Setup (Grid Only)

```scss
@import "functions";
@import "variables";
@import "variables-dark";
@import "maps";
@import "mixins";
@import "utilities";

// Layout only
@import "containers";
@import "grid";

// Utilities
@import "utilities/api";
```

### Common Lightweight Combinations

```scss
// Reboot + Grid + Utilities + Buttons + Cards (no modals, no dropdowns)
@import "functions";
@import "variables";
@import "variables-dark";
@import "maps";
@import "mixins";
@import "utilities";
@import "root";
@import "reboot";
@import "type";
@import "containers";
@import "grid";
@import "buttons";
@import "card";
@import "utilities/api";
```

### What Each Import Adds (approximate compressed sizes)

| Import | Size |
|--------|------|
| reboot | ~6 KB |
| grid + containers | ~7 KB |
| utilities/api | ~20–50 KB (depends on map) |
| buttons | ~4 KB |
| navbar | ~5 KB |
| modal | ~8 KB |
| forms | ~15 KB |
| Full bootstrap.scss | ~160 KB |

---

## 13. Custom Themes from Scratch

### Minimal Custom Theme Template

```scss
// ═══════════════════════════════════════════════
// Brand Configuration
// ═══════════════════════════════════════════════

// Typography
$font-family-sans-serif: 'Inter', system-ui, sans-serif;
$headings-font-family:   'Poppins', sans-serif;
$headings-font-weight:   700;
$font-size-base:         1rem;
$line-height-base:       1.6;

// Brand Colors
$brand-violet:   #6d28d9;
$brand-pink:     #db2777;
$brand-amber:    #d97706;

// Override theme colors
$primary:         $brand-violet;
$secondary:       #64748b;
$success:         #059669;
$warning:         $brand-amber;
$danger:          #dc2626;
$info:            #0284c7;
$light:           #f1f5f9;
$dark:            #0f172a;

// Extend theme
$theme-colors: (
  "primary":   $primary,
  "secondary": $secondary,
  "success":   $success,
  "info":      $info,
  "warning":   $warning,
  "danger":    $danger,
  "light":     $light,
  "dark":      $dark,
  "brand":     $brand-violet,
  "accent":    $brand-pink,
);

// Shape
$border-radius:      .75rem;
$border-radius-sm:   .5rem;
$border-radius-lg:   1rem;
$border-radius-xl:   1.5rem;
$border-radius-pill: 50rem;

// Elevation
$box-shadow:    0 4px 6px -1px rgba(0, 0, 0, .1), 0 2px 4px -2px rgba(0, 0, 0, .1);
$box-shadow-sm: 0 1px 3px rgba(0, 0, 0, .1), 0 1px 2px rgba(0, 0, 0, .06);
$box-shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, .1), 0 8px 10px -6px rgba(0, 0, 0, .1);

// Spacing
$spacer: 1rem;
$spacers: (
  0: 0, 1: .25rem, 2: .5rem, 3: 1rem,
  4: 1.5rem, 5: 3rem, 6: 4rem, 7: 6rem, 8: 8rem,
);

// Buttons
$btn-border-radius:  $border-radius;
$btn-font-weight:    600;
$btn-padding-x:      1.25rem;

// Cards
$card-border-radius: $border-radius-lg;
$card-box-shadow:    $box-shadow;
$card-border-color:  rgba(0, 0, 0, .06);

// Forms
$input-border-radius: $border-radius;
$input-border-color:  #cbd5e1;
$input-focus-border-color: $primary;
$input-focus-box-shadow: 0 0 0 .2rem rgba($primary, .2);

// ═══════════════════════════════════════════════
// Import Bootstrap
// ═══════════════════════════════════════════════
@import "../node_modules/bootstrap/scss/functions";
@import "../node_modules/bootstrap/scss/variables";
@import "../node_modules/bootstrap/scss/variables-dark";
@import "../node_modules/bootstrap/scss/maps";
@import "../node_modules/bootstrap/scss/mixins";
@import "../node_modules/bootstrap/scss/utilities";
@import "../node_modules/bootstrap/scss/bootstrap";

// ═══════════════════════════════════════════════
// Custom Components
// ═══════════════════════════════════════════════

// Gradient button
.btn-gradient-primary {
  background: linear-gradient(135deg, $brand-violet, $brand-pink);
  border: none;
  color: white;
  font-weight: 600;

  &:hover, &:focus {
    background: linear-gradient(135deg, darken($brand-violet, 8%), darken($brand-pink, 8%));
    color: white;
    box-shadow: 0 4px 12px rgba($brand-violet, .4);
  }
}

// Glassmorphism card
.card-glass {
  background: rgba(255, 255, 255, .7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, .8);
}
```

---

## 14. JavaScript Customization

### Plugin Default Options

Every Bootstrap plugin exposes its default configuration via `Constructor.Default`:

```javascript
// Change global Tooltip defaults
const tooltipDefaults = bootstrap.Tooltip.Default;
tooltipDefaults.placement = 'bottom';
tooltipDefaults.trigger = 'hover focus';
tooltipDefaults.delay = { show: 200, hide: 100 };
tooltipDefaults.animation = false;

// Change global Modal defaults
bootstrap.Modal.Default.backdrop = 'static'; // prevent close on backdrop click
bootstrap.Modal.Default.keyboard = false;

// Change Dropdown defaults
bootstrap.Dropdown.Default.offset = [0, 8];
bootstrap.Dropdown.Default.autoClose = 'outside';
```

### Events API

Every Bootstrap plugin fires events you can listen to:

```javascript
const modal = document.getElementById('myModal');

// Before the modal opens
modal.addEventListener('show.bs.modal', event => {
  const trigger = event.relatedTarget; // element that triggered the modal
  const data = trigger.getAttribute('data-title');
  modal.querySelector('.modal-title').textContent = data;
});

// After the modal finishes opening
modal.addEventListener('shown.bs.modal', () => {
  modal.querySelector('input').focus();
});

// Before the modal closes
modal.addEventListener('hide.bs.modal', event => {
  if (!isFormSaved) event.preventDefault(); // cancel close
});

// After the modal fully closes
modal.addEventListener('hidden.bs.modal', () => {
  console.log('Modal is gone');
});
```

### Programmatic Usage

```javascript
// Initialize manually
const el = document.getElementById('myDropdown');
const dropdown = new bootstrap.Dropdown(el, {
  offset: [0, 10],
  popperConfig: (defaultConfig) => ({
    ...defaultConfig,
    strategy: 'fixed',
  })
});

// Control programmatically
dropdown.show();
dropdown.hide();
dropdown.toggle();
dropdown.update();
dropdown.dispose(); // destroy instance

// Get existing instance
const instance = bootstrap.Dropdown.getInstance(el);
// or get or create:
const instance2 = bootstrap.Dropdown.getOrCreateInstance(el);

// Tooltip on dynamic elements
document.body.addEventListener('mouseenter', e => {
  if (e.target.matches('[data-bs-toggle="tooltip"]')) {
    bootstrap.Tooltip.getOrCreateInstance(e.target).show();
  }
}, true);
```

### Custom Popper Config

Dropdowns, tooltips, and popovers use Popper.js. You can customize the Popper config:

```javascript
new bootstrap.Dropdown(el, {
  popperConfig(defaultConfig) {
    return {
      ...defaultConfig,
      modifiers: [
        ...defaultConfig.modifiers,
        {
          name: 'offset',
          options: { offset: [0, 12] }
        },
        {
          name: 'preventOverflow',
          options: { padding: 8 }
        }
      ]
    };
  }
});
```

---

## 15. RTL Support

Bootstrap 5 includes RTL support via RTLCSS.

### Using the RTL CSS

```html
<!-- CDN -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.rtl.min.css">
```

Or set the `dir` attribute:

```html
<html lang="ar" dir="rtl">
```

### Building RTL with Sass

```bash
# Using rtlcss npm package
npm install --save-dev rtlcss

# In your build:
npx sass scss/custom.scss css/main.css
npx rtlcss css/main.css css/main.rtl.css
```

### RTL-aware Variables

```scss
// These Sass variables control RTL behavior
$enable-rtl: true;  // enables Bootstrap's RTL support in Sass output

// Logical properties are used internally, e.g.:
// margin-left → margin-inline-start
// padding-right → padding-inline-end
```

---

## 16. Build Tools & Optimization

### Vite Setup

```javascript
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "./src/scss/variables";`
      }
    }
  }
});
```

```scss
// src/scss/main.scss
@import "../../node_modules/bootstrap/scss/bootstrap";
```

### Webpack / sass-loader

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [{
      test: /\.scss$/,
      use: [
        'style-loader',
        'css-loader',
        {
          loader: 'sass-loader',
          options: {
            additionalData: `@import "src/scss/variables";`
          }
        }
      ]
    }]
  }
};
```

### PurgeCSS Integration (Remove Unused CSS)

```javascript
// postcss.config.js
const purgecss = require('@fullhuman/postcss-purgecss');

module.exports = {
  plugins: [
    purgecss({
      content: ['./src/**/*.html', './src/**/*.js'],
      safelist: {
        // Keep dynamic Bootstrap classes
        standard: [/^modal/, /^tooltip/, /^popover/, /^offcanvas/, /^show/, /^collapsing/],
        deep: [/data-bs/],
      }
    })
  ]
};
```

### Enable / Disable Bootstrap Features via Variables

```scss
// Global feature flags
$enable-caret:                true;   // dropdown caret arrows
$enable-rounded:              true;   // border-radius on components
$enable-shadows:              false;  // box-shadow on components
$enable-gradients:            false;  // gradient backgrounds
$enable-transitions:          true;   // CSS transitions
$enable-reduced-motion:       true;   // prefers-reduced-motion support
$enable-smooth-scroll:        true;   // scroll-behavior: smooth
$enable-grid-classes:         true;   // .container, .row, .col-*
$enable-container-classes:    true;   // .container-* classes
$enable-cssgrid:              false;  // CSS Grid utilities (experimental)
$enable-button-pointers:      true;   // cursor: pointer on buttons
$enable-rfs:                  true;   // Responsive Font Sizing
$enable-validation-icons:     true;   // input validation icons
$enable-negative-margins:     false;  // .mt-n1, .mb-n3, etc.
$enable-deprecation-messages: true;
$enable-important-utilities:  true;   // !important on utility classes
$enable-dark-mode:            true;   // dark mode support
$color-mode-type:             data;   // "data" (data-bs-theme) or "media" (prefers-color-scheme)
```

---

## 17. Real-World Examples

### Example 1: SaaS Dashboard Theme

```scss
// Dark sidebar + light content area theme
$font-family-sans-serif: 'Inter', system-ui, sans-serif;
$primary: #4f46e5;  // indigo
$dark:    #0f172a;

// Sidebar will use dark, content area light
.sidebar {
  background: $dark;
  color: rgba(white, .85);
  
  .nav-link {
    color: rgba(white, .6);
    border-radius: .5rem;
    
    &:hover {
      color: white;
      background: rgba(white, .05);
    }
    
    &.active {
      color: white;
      background: $primary;
    }
  }
}
```

### Example 2: E-Commerce Product Card

```scss
.product-card {
  --bs-card-border-color: transparent;
  --bs-card-border-radius: 1rem;
  --bs-card-box-shadow: 0 2px 8px rgba(0, 0, 0, .08);
  
  transition: transform .2s, box-shadow .2s;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, .12);
  }
  
  .product-badge {
    position: absolute;
    top: 1rem;
    left: 1rem;
    background: $danger;
    color: white;
    font-size: .7rem;
    font-weight: 700;
    padding: .2rem .5rem;
    border-radius: 50rem;
    text-transform: uppercase;
    letter-spacing: .05em;
  }
  
  .product-price {
    font-size: 1.25rem;
    font-weight: 700;
    color: $primary;
  }
  
  .original-price {
    text-decoration: line-through;
    color: $gray-500;
    font-size: .9rem;
  }
}
```

### Example 3: Dynamic Theme Switcher

```javascript
class ThemeManager {
  themes = {
    default: { primary: '#0d6efd', '--bs-border-radius': '.375rem' },
    violet:  { primary: '#6d28d9', '--bs-border-radius': '.75rem' },
    coral:   { primary: '#ef4444', '--bs-border-radius': '.25rem' },
    teal:    { primary: '#0d9488', '--bs-border-radius': '.5rem' },
  };
  
  apply(name) {
    const theme = this.themes[name];
    const root = document.documentElement;
    
    // Convert hex to RGB for --bs-primary-rgb
    const r = parseInt(theme.primary.slice(1, 3), 16);
    const g = parseInt(theme.primary.slice(3, 5), 16);
    const b = parseInt(theme.primary.slice(5, 7), 16);
    
    root.style.setProperty('--bs-primary', theme.primary);
    root.style.setProperty('--bs-primary-rgb', `${r}, ${g}, ${b}`);
    
    Object.entries(theme).forEach(([key, val]) => {
      if (key !== 'primary') root.style.setProperty(key, val);
    });
    
    localStorage.setItem('bs-theme-name', name);
  }
  
  init() {
    const saved = localStorage.getItem('bs-theme-name') ?? 'default';
    this.apply(saved);
  }
}

const themeManager = new ThemeManager();
themeManager.init();

document.querySelectorAll('[data-theme]').forEach(btn => {
  btn.addEventListener('click', () => themeManager.apply(btn.dataset.theme));
});
```

---

## 18. Common Pitfalls & Troubleshooting

**Variable overrides not working**
Your overrides must appear before Bootstrap imports `_variables.scss`. Remember the `!default` rule: Bootstrap only sets a variable if it's not already defined.

**Dark mode not applying**
Make sure `$enable-dark-mode: true` is set, and that you're using `data-bs-theme="dark"` on `<html>` or a parent element. Also check that `$color-mode-type` is set to `data` (default) rather than `media`.

**Custom theme color not generating utilities**
After adding to `$theme-colors`, you need to also update `$theme-colors-text`, `$theme-colors-bg-subtle`, and `$theme-colors-border-subtle` in `_maps.scss` if you want subtle variants. The simplest fix is to ensure you're importing `_maps.scss` after your variable overrides.

**CSS variable override not affecting a component**
Some components use hardcoded Sass values compiled to static CSS rather than CSS variables. Check if the property you want to override is a CSS variable in the compiled output (look for `var(--bs-...)`) — if it's a plain value, you need to override it via Sass variable, not a CSS property at runtime.

**Grid not responsive after adding custom breakpoint**
You must add the breakpoint to BOTH `$grid-breakpoints` AND `$container-max-widths`. They must stay in sync.

**PurgeCSS removing dynamic classes**
Bootstrap generates classes dynamically via JavaScript (e.g., `show`, `collapsing`, `tooltip-inner`). Add these to the PurgeCSS `safelist` to prevent them from being removed.

**`!important` utility not overriding component style**
Bootstrap utilities have `!important` only when `$enable-important-utilities: true` (it is by default). If a component style uses inline CSS or a higher-specificity selector, utilities still lose. Use CSS variables or scoped overrides instead.

**Sass `@use` vs `@import`**
Bootstrap 5.x officially uses the older `@import` syntax. If your build uses `@use`/`@forward`, you may need to configure a compatibility shim or stick with `@import` for the Bootstrap parts.

---

*This guide covers Bootstrap 5.3. For the very latest changes, always check [getbootstrap.com/docs](https://getbootstrap.com/docs/5.3/).*
