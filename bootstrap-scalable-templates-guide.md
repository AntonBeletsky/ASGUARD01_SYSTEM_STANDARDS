# Bootstrap Scalable & Adaptive Template Development Guide

> A complete, production-ready reference for building large-scale, fully responsive, and modern Bootstrap 5 templates from the ground up.

---

## Table of Contents

1. [Project Architecture & Folder Structure](#1-project-architecture--folder-structure)
2. [Bootstrap Setup: CDN vs Build Pipeline](#2-bootstrap-setup-cdn-vs-build-pipeline)
3. [CSS Custom Properties & SASS Theming](#3-css-custom-properties--sass-theming)
4. [Grid System Mastery](#4-grid-system-mastery)
5. [Breakpoint Strategy](#5-breakpoint-strategy)
6. [Typography Scale](#6-typography-scale)
7. [Component Architecture](#7-component-architecture)
8. [Navigation Patterns](#8-navigation-patterns)
9. [Layout Sections: Hero, Cards, Features, Footer](#9-layout-sections-hero-cards-features-footer)
10. [Dark Mode Implementation](#10-dark-mode-implementation)
11. [Accessibility (A11y)](#11-accessibility-a11y)
12. [Performance Optimization](#12-performance-optimization)
13. [JavaScript Interactivity](#13-javascript-interactivity)
14. [RTL & Internationalization](#14-rtl--internationalization)
15. [Testing & QA Checklist](#15-testing--qa-checklist)
16. [Deployment & CI/CD Tips](#16-deployment--cicd-tips)

---

## 1. Project Architecture & Folder Structure

A well-organized file structure is the backbone of any scalable template. Separate concerns early and enforce naming conventions.

```
project-root/
├── src/
│   ├── scss/
│   │   ├── _variables.scss        # Override Bootstrap variables
│   │   ├── _mixins.scss           # Custom mixins
│   │   ├── _typography.scss       # Font definitions & scale
│   │   ├── _components.scss       # Custom component styles
│   │   ├── _utilities.scss        # Utility class extensions
│   │   ├── _dark.scss             # Dark mode overrides
│   │   └── main.scss              # Entry point — imports everything
│   ├── js/
│   │   ├── modules/               # Feature-specific JS modules
│   │   │   ├── navbar.js
│   │   │   ├── darkMode.js
│   │   │   └── animations.js
│   │   └── main.js                # Entry point
│   ├── assets/
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   └── templates/
│       ├── partials/              # Reusable HTML snippets
│       │   ├── _head.html
│       │   ├── _navbar.html
│       │   └── _footer.html
│       ├── index.html
│       ├── about.html
│       └── contact.html
├── dist/                          # Compiled output
├── .browserslistrc
├── package.json
├── vite.config.js (or webpack.config.js)
└── README.md
```

### Naming Conventions

| Type | Convention | Example |
|---|---|---|
| SASS partials | Underscore prefix | `_variables.scss` |
| JS modules | camelCase | `darkMode.js` |
| HTML partials | Underscore prefix | `_navbar.html` |
| CSS classes | BEM + Bootstrap | `.card__header--highlighted` |
| CSS variables | `--bs-*` namespace | `--bs-primary-rgb` |

---

## 2. Bootstrap Setup: CDN vs Build Pipeline

### Option A — CDN (Rapid Prototyping)

Use when: quick demos, client previews, no custom theming needed.

```html
<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bootstrap Template</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- Custom CSS after Bootstrap -->
  <link rel="stylesheet" href="css/main.css">
</head>
<body>
  <!-- content -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
```

### Option B — Vite + SASS (Production, Recommended)

```bash
# Initialize project
npm create vite@latest my-template -- --template vanilla
cd my-template
npm install

# Install Bootstrap and dependencies
npm install bootstrap @popperjs/core
npm install --save-dev sass autoprefixer postcss
```

**`vite.config.js`**
```javascript
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        // Make Bootstrap variables available globally
        additionalData: `@import "./src/scss/_variables.scss";`
      }
    }
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        about: resolve(__dirname, 'about.html'),
      }
    }
  }
});
```

**`src/scss/main.scss`** — selective Bootstrap import
```scss
// 1. Override Bootstrap defaults BEFORE importing
@import "variables";

// 2. Import only the Bootstrap parts you need
@import "../node_modules/bootstrap/scss/functions";
@import "../node_modules/bootstrap/scss/variables";
@import "../node_modules/bootstrap/scss/variables-dark";
@import "../node_modules/bootstrap/scss/maps";
@import "../node_modules/bootstrap/scss/mixins";
@import "../node_modules/bootstrap/scss/root";

// Core
@import "../node_modules/bootstrap/scss/reboot";
@import "../node_modules/bootstrap/scss/type";
@import "../node_modules/bootstrap/scss/images";
@import "../node_modules/bootstrap/scss/containers";
@import "../node_modules/bootstrap/scss/grid";
@import "../node_modules/bootstrap/scss/tables";
@import "../node_modules/bootstrap/scss/forms";
@import "../node_modules/bootstrap/scss/buttons";
@import "../node_modules/bootstrap/scss/transitions";
@import "../node_modules/bootstrap/scss/dropdown";
@import "../node_modules/bootstrap/scss/nav";
@import "../node_modules/bootstrap/scss/navbar";
@import "../node_modules/bootstrap/scss/card";
@import "../node_modules/bootstrap/scss/modal";
@import "../node_modules/bootstrap/scss/utilities";
@import "../node_modules/bootstrap/scss/helpers";
@import "../node_modules/bootstrap/scss/utilities/api";

// 3. Your custom styles
@import "typography";
@import "components";
@import "utilities";
@import "dark";
```

> **Tip:** Importing only what you need can reduce Bootstrap's compiled CSS from ~220KB to under 50KB for typical templates.

---

## 3. CSS Custom Properties & SASS Theming

Bootstrap 5 uses both SASS variables and CSS custom properties. Master both layers.

### Override SASS Variables (compile-time)

```scss
// src/scss/_variables.scss

// === COLOR SYSTEM ===
$primary:   #0d6efd;     // Brand blue
$secondary: #6c757d;
$success:   #198754;
$danger:    #dc3545;
$warning:   #ffc107;
$info:      #0dcaf0;

// Custom brand colors (extend the palette)
$brand-accent: #ff6b35;
$brand-dark:   #1a1a2e;

// Add to the $theme-colors map
$theme-colors: (
  "primary":    $primary,
  "secondary":  $secondary,
  "success":    $success,
  "info":       $info,
  "warning":    $warning,
  "danger":     $danger,
  "light":      $light,
  "dark":       $dark,
  "accent":     $brand-accent,   // Custom addition
);

// === TYPOGRAPHY ===
$font-family-sans-serif: 'Inter', 'Segoe UI', system-ui, sans-serif;
$font-size-base:         1rem;       // 16px
$line-height-base:       1.6;
$headings-font-weight:   700;
$headings-line-height:   1.2;

// === SPACING ===
$spacer: 1rem;
$spacers: (
  0: 0,
  1: $spacer * 0.25,   // 4px
  2: $spacer * 0.5,    // 8px
  3: $spacer,          // 16px
  4: $spacer * 1.5,    // 24px
  5: $spacer * 3,      // 48px
  6: $spacer * 5,      // 80px  ← Custom section padding
  7: $spacer * 8,      // 128px ← Custom hero padding
);

// === BORDERS ===
$border-radius:    0.5rem;
$border-radius-lg: 1rem;
$border-radius-xl: 1.5rem;   // Custom
$border-radius-pill: 50rem;

// === SHADOWS ===
$box-shadow:    0 0.125rem 0.5rem rgba(0,0,0,0.08);
$box-shadow-lg: 0 1rem 3rem rgba(0,0,0,0.12);

// === GRID ===
$grid-gutter-width: 1.5rem;
$container-max-widths: (
  sm: 540px,
  md: 720px,
  lg: 960px,
  xl: 1140px,
  xxl: 1400px,
);

// === TRANSITIONS ===
$transition-base: all 0.25s ease-in-out;
$transition-fade: opacity 0.2s linear;
```

### CSS Custom Properties (runtime theming)

```css
:root {
  /* Extended brand tokens */
  --brand-primary-hue: 215;
  --brand-gradient: linear-gradient(135deg, #0d6efd 0%, #6610f2 100%);
  --section-padding: 5rem;
  --hero-min-height: 90vh;
  --card-hover-lift: translateY(-6px);
  --nav-height: 72px;
}

/* Runtime theme switching without recompile */
[data-theme="corporate"] {
  --bs-primary: #003087;
  --bs-primary-rgb: 0, 48, 135;
}

[data-theme="startup"] {
  --bs-primary: #ff6b35;
  --bs-primary-rgb: 255, 107, 53;
}
```

---

## 4. Grid System Mastery

### Responsive Column Patterns

```html
<!-- ✅ Pattern 1: Content + Sidebar -->
<div class="row g-4">
  <div class="col-12 col-lg-8">Main content</div>
  <div class="col-12 col-lg-4">Sidebar</div>
</div>

<!-- ✅ Pattern 2: Auto-responsive card grid -->
<div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 row-cols-xl-4 g-4">
  <div class="col"><div class="card h-100">...</div></div>
  <div class="col"><div class="card h-100">...</div></div>
  <div class="col"><div class="card h-100">...</div></div>
  <div class="col"><div class="card h-100">...</div></div>
</div>

<!-- ✅ Pattern 3: Masonry-style (CSS columns) -->
<div class="row" style="--bs-masonry-columns: 3;">
  <div class="col">...</div>
</div>

<!-- ✅ Pattern 4: Centered content with max-width -->
<div class="row justify-content-center">
  <div class="col-12 col-md-10 col-lg-8 col-xl-6">
    <p>Narrow reading column</p>
  </div>
</div>
```

### Custom Grid Extension (SASS)

```scss
// Add a 7-column grid for special layouts
.col-7-cols {
  @include make-col(1, 7);
}

// Fluid container with custom max-width
.container-narrow {
  @extend .container;
  max-width: 860px;
}

.container-wide {
  @extend .container-fluid;
  max-width: 1600px;
  padding-left: clamp(1rem, 4vw, 3rem);
  padding-right: clamp(1rem, 4vw, 3rem);
}
```

### CSS Grid Inside Bootstrap

Use native CSS Grid for complex internal layouts — Bootstrap grid handles page structure, CSS Grid handles component internals.

```html
<!-- Feature grid with CSS Grid precision -->
<section class="container">
  <div class="features-grid">
    <div class="feature-item feature-item--hero">Large hero feature</div>
    <div class="feature-item">Feature 2</div>
    <div class="feature-item">Feature 3</div>
    <div class="feature-item">Feature 4</div>
    <div class="feature-item feature-item--wide">Wide feature</div>
  </div>
</section>
```

```scss
.features-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto;

  @include media-breakpoint-down(md) {
    grid-template-columns: 1fr;
  }

  .feature-item--hero {
    grid-column: span 2;
    grid-row: span 2;
  }

  .feature-item--wide {
    grid-column: 1 / -1;
  }
}
```

---

## 5. Breakpoint Strategy

### Bootstrap 5 Default Breakpoints

| Breakpoint | Prefix | Min-Width | Device |
|---|---|---|---|
| Extra small | *(none)* | < 576px | Portrait phones |
| Small | `sm` | ≥ 576px | Landscape phones |
| Medium | `md` | ≥ 768px | Tablets |
| Large | `lg` | ≥ 992px | Desktops |
| Extra large | `xl` | ≥ 1200px | Large desktops |
| XXL | `xxl` | ≥ 1400px | Wide screens |

### Custom Breakpoints

```scss
// _variables.scss
$grid-breakpoints: (
  xs:  0,
  sm:  576px,
  md:  768px,
  lg:  992px,
  xl:  1200px,
  xxl: 1400px,
  xxxl: 1920px,   // 4K / ultra-wide screens
);
```

### Mobile-First SASS Mixin Usage

```scss
// Always write mobile styles FIRST, then use up-mixins

.hero-title {
  font-size: 2rem;           // mobile default

  @include media-breakpoint-up(md) {
    font-size: 3rem;
  }

  @include media-breakpoint-up(xl) {
    font-size: clamp(3rem, 5vw, 5rem);   // fluid on large screens
  }
}

// Range mixin — target only specific breakpoints
.sidebar {
  @include media-breakpoint-between(md, lg) {
    width: 220px;
  }
}

// Down mixin — override for small screens only
.navbar-brand {
  @include media-breakpoint-down(sm) {
    font-size: 1rem;
  }
}
```

### Fluid Typography with clamp()

```scss
// _typography.scss
:root {
  --fs-sm:    clamp(0.8rem,  1vw,   0.9rem);
  --fs-base:  clamp(1rem,    1.2vw, 1.125rem);
  --fs-lg:    clamp(1.125rem,1.5vw, 1.25rem);
  --fs-xl:    clamp(1.5rem,  3vw,   2rem);
  --fs-2xl:   clamp(2rem,    4vw,   3rem);
  --fs-3xl:   clamp(2.5rem,  6vw,   4.5rem);
  --fs-hero:  clamp(3rem,    8vw,   6rem);
}
```

---

## 6. Typography Scale

### Google Fonts Integration

```html
<!-- Optimized font loading -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@700;800&display=swap" rel="stylesheet">
```

### Typography Component Classes

```scss
// _typography.scss

// Display headings for heroes and landing pages
.display-hero {
  font-size: var(--fs-hero);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.05;
}

// Eyebrow / Overline text
.text-overline {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--bs-primary);
}

// Balanced text wrapping (modern CSS)
.text-balance {
  text-wrap: balance;
}

// Gradient text effect
.text-gradient {
  background: var(--brand-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

// Responsive body text
body {
  font-size: var(--fs-base);
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

---

## 7. Component Architecture

### Extending Bootstrap Components with BEM

```scss
// _components.scss — Example: Extended Card

.card-feature {
  @extend .card;
  border: none;
  border-radius: var(--bs-border-radius-xl);
  box-shadow: var(--bs-box-shadow);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;

  &:hover {
    transform: var(--card-hover-lift);
    box-shadow: 0 1.5rem 4rem rgba(0,0,0,0.15);
  }

  &__icon {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    background: rgba(var(--bs-primary-rgb), 0.1);
    color: var(--bs-primary);
    margin-bottom: 1.25rem;
  }

  &__body {
    @extend .card-body;
    padding: 2rem;
  }

  &__title {
    @extend .card-title;
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
  }

  &__text {
    @extend .card-text;
    color: var(--bs-secondary-color);
    line-height: 1.7;
  }
}
```

### Button System Extension

```scss
// Custom button variant using Bootstrap mixin
@each $name, $value in (
  "accent": $brand-accent,
  "surface": #f8f9fa
) {
  .btn-#{$name} {
    @include button-variant($value, $value);
  }
  .btn-outline-#{$name} {
    @include button-outline-variant($value);
  }
}

// CTA Button with glow effect
.btn-cta {
  @extend .btn, .btn-primary;
  padding: 0.875rem 2.25rem;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  border-radius: var(--bs-border-radius-pill);
  box-shadow: 0 0 0 0 rgba(var(--bs-primary-rgb), 0.4);
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 8px 24px rgba(var(--bs-primary-rgb), 0.4);
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
    box-shadow: none;
  }
}
```

---

## 8. Navigation Patterns

### Sticky Navbar with Scroll Effect

```html
<!-- _navbar.html -->
<nav id="mainNavbar" class="navbar navbar-expand-lg navbar-light bg-white fixed-top py-3">
  <div class="container">
    
    <!-- Brand -->
    <a class="navbar-brand fw-bold fs-4" href="/">
      <span class="text-primary">Brand</span>Name
    </a>

    <!-- Toggler -->
    <button class="navbar-toggler border-0 shadow-none" type="button"
            data-bs-toggle="collapse" data-bs-target="#navContent"
            aria-controls="navContent" aria-expanded="false"
            aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <!-- Links -->
    <div class="collapse navbar-collapse" id="navContent">
      <ul class="navbar-nav ms-auto align-items-lg-center gap-lg-1">
        <li class="nav-item"><a class="nav-link" href="#features">Features</a></li>
        <li class="nav-item"><a class="nav-link" href="#pricing">Pricing</a></li>
        <li class="nav-item">
          <!-- Dropdown -->
          <div class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown">Resources</a>
            <ul class="dropdown-menu dropdown-menu-end shadow border-0 rounded-3">
              <li><a class="dropdown-item py-2" href="/docs">Documentation</a></li>
              <li><a class="dropdown-item py-2" href="/blog">Blog</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item py-2" href="/changelog">Changelog</a></li>
            </ul>
          </div>
        </li>
        <li class="nav-item ms-lg-3 d-grid d-lg-block">
          <a href="/signup" class="btn btn-primary rounded-pill px-4">Get Started</a>
        </li>
      </ul>
    </div>

  </div>
</nav>
```

```scss
// Scrolled navbar state
#mainNavbar {
  transition: padding 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;

  &.scrolled {
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    box-shadow: 0 2px 20px rgba(0,0,0,0.08);
  }

  .nav-link {
    font-weight: 500;
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0.5rem;
      right: 0.5rem;
      height: 2px;
      background: var(--bs-primary);
      transform: scaleX(0);
      transition: transform 0.25s ease;
    }

    &:hover::after,
    &.active::after {
      transform: scaleX(1);
    }
  }
}
```

```javascript
// js/modules/navbar.js
const navbar = document.getElementById('mainNavbar');

const handleScroll = () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
};

window.addEventListener('scroll', handleScroll, { passive: true });
```

---

## 9. Layout Sections: Hero, Cards, Features, Footer

### Hero Section Patterns

```html
<!-- Pattern A: Split Hero (Text + Visual) -->
<section class="hero-split min-vh-100 d-flex align-items-center py-7">
  <div class="container">
    <div class="row align-items-center g-5">
      <div class="col-12 col-lg-6 order-2 order-lg-1">
        <span class="text-overline">Introducing v2.0</span>
        <h1 class="display-4 fw-bold mt-2 mb-4 text-balance">
          Build faster with<br>
          <span class="text-gradient">modern tools</span>
        </h1>
        <p class="lead text-secondary mb-5">
          A comprehensive platform designed to help teams ship better products
          in record time. Zero config, maximum output.
        </p>
        <div class="d-flex flex-wrap gap-3">
          <a href="/start" class="btn-cta btn">Start for Free</a>
          <a href="/demo" class="btn btn-outline-secondary rounded-pill px-4">
            Watch Demo ▸
          </a>
        </div>
        <p class="small text-muted mt-3">No credit card required · Free forever plan</p>
      </div>
      <div class="col-12 col-lg-6 order-1 order-lg-2">
        <div class="hero-visual ratio ratio-4x3">
          <img src="assets/images/hero-dashboard.webp"
               alt="Dashboard preview"
               class="img-fluid rounded-4 shadow-lg"
               loading="eager">
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Pattern B: Centered Hero with Background -->
<section class="hero-centered py-7 text-center position-relative overflow-hidden">
  <!-- Background decoration -->
  <div class="hero-bg-blob" aria-hidden="true"></div>
  
  <div class="container position-relative">
    <div class="row justify-content-center">
      <div class="col-12 col-md-10 col-lg-8">
        <span class="badge bg-primary-subtle text-primary rounded-pill px-3 py-2 mb-4">
          🚀 Just launched
        </span>
        <h1 class="display-hero fw-bold mb-4">
          The future of collaboration is here
        </h1>
        <p class="fs-lg text-secondary mb-5 text-balance">
          Designed from the ground up for distributed teams. Real-time, 
          async-friendly, and built to scale with your ambitions.
        </p>
        <div class="d-flex justify-content-center gap-3 flex-wrap">
          <a href="/signup" class="btn-cta btn btn-lg">Start Building Free</a>
          <a href="/pricing" class="btn btn-lg btn-outline-dark rounded-pill px-4">
            See Pricing
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
```

### Feature Sections

```html
<!-- Three-column feature grid with icons -->
<section class="py-6 bg-light" id="features">
  <div class="container">

    <div class="row justify-content-center mb-5">
      <div class="col-12 col-md-7 text-center">
        <span class="text-overline">Why choose us</span>
        <h2 class="display-5 fw-bold mt-2">Everything you need</h2>
        <p class="text-secondary">
          Purpose-built tools that scale from solo projects to enterprise teams.
        </p>
      </div>
    </div>

    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <!-- Feature Card -->
      <div class="col">
        <div class="card-feature">
          <div class="card-feature__body">
            <div class="card-feature__icon">⚡</div>
            <h3 class="card-feature__title">Lightning Fast</h3>
            <p class="card-feature__text">
              Optimized from core to edge — sub-second load times on every device.
            </p>
          </div>
        </div>
      </div>
      <!-- Repeat for each feature -->
    </div>

  </div>
</section>
```

### Statistics / Social Proof Bar

```html
<section class="py-5 border-top border-bottom">
  <div class="container">
    <div class="row row-cols-2 row-cols-md-4 g-4 text-center">
      <div class="col">
        <div class="stat-counter" data-target="50000">
          <span class="display-5 fw-bold text-primary" id="stat-users">0</span>
          <span class="display-5 fw-bold text-primary">+</span>
          <p class="text-muted mb-0 small fw-medium mt-1">Active Users</p>
        </div>
      </div>
      <div class="col">
        <span class="display-5 fw-bold">99.9%</span>
        <p class="text-muted mb-0 small fw-medium mt-1">Uptime SLA</p>
      </div>
      <div class="col">
        <span class="display-5 fw-bold">4.9 ★</span>
        <p class="text-muted mb-0 small fw-medium mt-1">Average Rating</p>
      </div>
      <div class="col">
        <span class="display-5 fw-bold">180+</span>
        <p class="text-muted mb-0 small fw-medium mt-1">Countries</p>
      </div>
    </div>
  </div>
</section>
```

### Responsive Footer

```html
<footer class="bg-dark text-white pt-6 pb-4">
  <div class="container">
    <div class="row g-5 mb-5">

      <!-- Brand column -->
      <div class="col-12 col-md-4">
        <a href="/" class="text-white text-decoration-none fw-bold fs-4 d-block mb-3">
          BrandName
        </a>
        <p class="text-white-50 mb-4">
          Building tools that help teams move fast and ship with confidence.
        </p>
        <!-- Social icons -->
        <div class="d-flex gap-2">
          <a href="#" class="btn btn-outline-secondary btn-sm rounded-circle" aria-label="Twitter">
            𝕏
          </a>
          <a href="#" class="btn btn-outline-secondary btn-sm rounded-circle" aria-label="GitHub">
            ⊙
          </a>
          <a href="#" class="btn btn-outline-secondary btn-sm rounded-circle" aria-label="LinkedIn">
            in
          </a>
        </div>
      </div>

      <!-- Link columns -->
      <div class="col-6 col-md-2">
        <h6 class="text-uppercase fw-bold mb-3 small letter-spacing">Product</h6>
        <ul class="list-unstyled">
          <li class="mb-2"><a href="#" class="text-white-50 text-decoration-none hover-white">Features</a></li>
          <li class="mb-2"><a href="#" class="text-white-50 text-decoration-none hover-white">Pricing</a></li>
          <li class="mb-2"><a href="#" class="text-white-50 text-decoration-none hover-white">Changelog</a></li>
          <li class="mb-2"><a href="#" class="text-white-50 text-decoration-none hover-white">Roadmap</a></li>
        </ul>
      </div>

      <div class="col-6 col-md-2">
        <h6 class="text-uppercase fw-bold mb-3 small">Company</h6>
        <ul class="list-unstyled">
          <li class="mb-2"><a href="#" class="text-white-50 text-decoration-none">About</a></li>
          <li class="mb-2"><a href="#" class="text-white-50 text-decoration-none">Blog</a></li>
          <li class="mb-2"><a href="#" class="text-white-50 text-decoration-none">Careers</a></li>
          <li class="mb-2"><a href="#" class="text-white-50 text-decoration-none">Contact</a></li>
        </ul>
      </div>

      <!-- Newsletter -->
      <div class="col-12 col-md-4">
        <h6 class="fw-bold mb-3">Stay in the loop</h6>
        <p class="text-white-50 small">Weekly updates. No spam. Unsubscribe anytime.</p>
        <div class="input-group mt-3">
          <input type="email" class="form-control bg-white-10 border-0 text-white"
                 placeholder="you@example.com" aria-label="Email">
          <button class="btn btn-primary" type="button">Subscribe</button>
        </div>
      </div>

    </div>

    <!-- Bottom bar -->
    <div class="border-top border-white-10 pt-4 d-flex flex-column flex-md-row justify-content-between gap-2">
      <p class="text-white-50 small mb-0">© 2025 BrandName, Inc. All rights reserved.</p>
      <div class="d-flex gap-3">
        <a href="#" class="text-white-50 text-decoration-none small">Privacy Policy</a>
        <a href="#" class="text-white-50 text-decoration-none small">Terms of Service</a>
        <a href="#" class="text-white-50 text-decoration-none small">Cookie Policy</a>
      </div>
    </div>

  </div>
</footer>
```

---

## 10. Dark Mode Implementation

Bootstrap 5.3+ includes native dark mode via `data-bs-theme`.

### HTML Setup

```html
<!-- Auto-detect system preference -->
<html lang="en" data-bs-theme="auto">

<!-- Or explicit -->
<html lang="en" data-bs-theme="light">
```

### JavaScript Toggle

```javascript
// js/modules/darkMode.js

const STORAGE_KEY = 'bs-theme';

const getPreferredTheme = () =>
  localStorage.getItem(STORAGE_KEY)
  || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

const setTheme = (theme) => {
  document.documentElement.setAttribute('data-bs-theme', theme);
  localStorage.setItem(STORAGE_KEY, theme);
  updateToggleIcons(theme);
};

const updateToggleIcons = (theme) => {
  document.querySelectorAll('[data-bs-theme-icon]').forEach(el => {
    el.textContent = theme === 'dark' ? '☀️' : '🌙';
    el.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
  });
};

// Initialize
setTheme(getPreferredTheme());

// Toggle button
document.querySelectorAll('[data-bs-toggle="theme"]').forEach(btn => {
  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-bs-theme');
    setTheme(current === 'dark' ? 'light' : 'dark');
  });
});

// Sync with OS changes
window.matchMedia('(prefers-color-scheme: dark)')
  .addEventListener('change', e => {
    if (!localStorage.getItem(STORAGE_KEY)) {
      setTheme(e.matches ? 'dark' : 'light');
    }
  });
```

### SASS Dark Mode Overrides

```scss
// _dark.scss
[data-bs-theme="dark"] {
  // Custom surface colors
  --bs-body-bg: #0f1117;
  --bs-body-color: #e8eaf0;
  --bs-secondary-color: #9ca3b0;
  
  // Card overrides
  --bs-card-bg: #1a1d2e;
  --bs-card-border-color: rgba(255,255,255,0.08);

  // Code blocks
  pre, code {
    background: #1e2030;
    border-color: rgba(255,255,255,0.1);
  }

  // Hero backgrounds
  .hero-split,
  .hero-centered {
    background: radial-gradient(ellipse at top, #1a1d2e 0%, #0f1117 70%);
  }

  // Navbar in dark
  #mainNavbar {
    --bs-navbar-bg: rgba(15,17,23,0.9);
    backdrop-filter: blur(12px);
  }
}
```

---

## 11. Accessibility (A11y)

### Essential Checklist

```html
<!-- 1. Semantic HTML structure -->
<header role="banner">
  <nav aria-label="Main navigation">...</nav>
</header>
<main id="main-content">...</main>
<footer role="contentinfo">...</footer>

<!-- 2. Skip navigation link (CRITICAL for keyboard users) -->
<a href="#main-content" class="visually-hidden-focusable">
  Skip to main content
</a>

<!-- 3. Icon-only buttons must have labels -->
<button aria-label="Close modal">✕</button>
<button aria-label="Toggle navigation">
  <span class="navbar-toggler-icon" aria-hidden="true"></span>
</button>

<!-- 4. Images: meaningful vs decorative -->
<img src="hero.jpg" alt="Team collaborating on a whiteboard">
<img src="divider.svg" alt="" role="presentation">

<!-- 5. Form labels always connected to inputs -->
<div class="mb-3">
  <label for="emailInput" class="form-label">Email address</label>
  <input type="email" class="form-control" id="emailInput"
         aria-describedby="emailHelp" required>
  <div id="emailHelp" class="form-text">We never share your email.</div>
</div>

<!-- 6. Descriptive link text -->
<!-- ❌ Bad: --> <a href="/article">Read more</a>
<!-- ✅ Good: --> <a href="/article">Read more about our pricing changes</a>

<!-- 7. Color contrast — Bootstrap components pass AA. For custom: -->
<!-- Use online tools: webaim.org/resources/contrastchecker -->
```

### Focus Management

```scss
// Ensure visible focus indicators
:focus-visible {
  outline: 3px solid var(--bs-primary);
  outline-offset: 3px;
  border-radius: 4px;
}

// Remove outline ONLY when using mouse (not keyboard)
:focus:not(:focus-visible) {
  outline: none;
}
```

### Reduced Motion

```scss
// Respect user's OS motion preferences
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 12. Performance Optimization

### HTML Head Optimization

```html
<head>
  <meta charset="utf-8">
  <!-- Prevent layout shift -->
  <meta name="viewport" content="width=device-width, initial-scale=1">
  
  <!-- Preconnect to external origins -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  
  <!-- Critical CSS inline (above-the-fold only) -->
  <style>
    /* Only styles needed for first paint */
    body { margin: 0; font-family: system-ui, sans-serif; }
    .navbar { height: 72px; background: #fff; }
  </style>
  
  <!-- Main CSS non-blocking load -->
  <link rel="preload" href="/css/main.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/css/main.css"></noscript>
  
  <!-- Meta for SEO and social -->
  <meta name="description" content="...">
  <meta property="og:title" content="...">
  <meta property="og:image" content="...">
</head>
```

### Image Best Practices

```html
<!-- Always specify dimensions to prevent CLS -->
<img src="hero.webp"
     alt="Product screenshot"
     width="1200"
     height="800"
     loading="lazy"
     decoding="async"
     class="img-fluid rounded-4">

<!-- Art direction with picture element -->
<picture>
  <source media="(max-width: 576px)" srcset="hero-mobile.webp" type="image/webp">
  <source media="(max-width: 992px)" srcset="hero-tablet.webp" type="image/webp">
  <source srcset="hero-desktop.webp" type="image/webp">
  <img src="hero-desktop.jpg" alt="Dashboard" class="img-fluid" loading="eager">
</picture>

<!-- Responsive images with srcset -->
<img src="card.jpg"
     srcset="card-400.webp 400w, card-800.webp 800w, card-1200.webp 1200w"
     sizes="(max-width: 576px) 100vw, (max-width: 992px) 50vw, 33vw"
     alt="Feature card">
```

### Bootstrap JS Tree Shaking

```javascript
// main.js — import ONLY what you use
import { Modal }    from 'bootstrap/js/dist/modal';
import { Dropdown } from 'bootstrap/js/dist/dropdown';
import { Collapse } from 'bootstrap/js/dist/collapse';
import { Tooltip }  from 'bootstrap/js/dist/tooltip';

// Initialize tooltips
document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
  new Tooltip(el);
});
```

### SCSS Bundle Size Reduction

```scss
// Disable unused Bootstrap utilities
$utilities: map-merge(
  $utilities,
  (
    "opacity": map-merge(
      map-get($utilities, "opacity"),
      ( "values": (0, 25, 50, 75, 100) )  // Keep only these
    ),
    "font-size": false,   // Disable entirely if not using fs-* classes
    "rounded": map-merge(
      map-get($utilities, "rounded"),
      ( "responsive": false )  // Disable responsive variants
    ),
  )
);
```

---

## 13. JavaScript Interactivity

### Scroll-Triggered Animations (Intersection Observer)

```javascript
// js/modules/animations.js

const observerOptions = {
  threshold: 0.15,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      // Unobserve after triggering (performance)
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('[data-animate]').forEach(el => observer.observe(el));
```

```scss
// Corresponding CSS
[data-animate] {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;

  // Stagger children
  @for $i from 1 through 8 {
    &:nth-child(#{$i}) {
      transition-delay: #{($i - 1) * 0.1}s;
    }
  }

  &.is-visible {
    opacity: 1;
    transform: translateY(0);
  }

  @media (prefers-reduced-motion: reduce) {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

```html
<!-- Usage -->
<div class="row g-4">
  <div class="col" data-animate>Card 1 — animates first</div>
  <div class="col" data-animate>Card 2 — animates second</div>
  <div class="col" data-animate>Card 3 — animates third</div>
</div>
```

### Counter Animation

```javascript
// js/modules/counter.js
const animateCounter = (el, target, duration = 2000) => {
  const start = performance.now();
  const step = (timestamp) => {
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
    el.textContent = Math.floor(eased * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
};

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      animateCounter(el, Number(el.dataset.target));
      counterObserver.unobserve(el);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-counter]').forEach(el => counterObserver.observe(el));
```

---

## 14. RTL & Internationalization

Bootstrap 5 has built-in RTL support — add `dir="rtl"` and use the RTL CSS build.

```html
<!-- RTL layout -->
<html lang="ar" dir="rtl">
<head>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css">
</head>
```

### RTL-safe SASS

```scss
// Use logical properties (work in both LTR and RTL)
.nav-link {
  // ❌ Avoid: margin-left, padding-left
  // ✅ Use:
  margin-inline-start: 1rem;
  padding-inline: 0.75rem;
  border-inline-start: 3px solid transparent;
}

// Bootstrap mixins for LTR/RTL
.card-header {
  @include border-top-radius($card-inner-border-radius);
}
```

### Language Switching

```javascript
// Dynamic lang + dir switching
const switchLanguage = (lang, dir = 'ltr') => {
  document.documentElement.setAttribute('lang', lang);
  document.documentElement.setAttribute('dir', dir);
  
  // Load appropriate Bootstrap CSS
  const bsLink = document.getElementById('bootstrap-css');
  bsLink.href = dir === 'rtl'
    ? '/css/bootstrap.rtl.min.css'
    : '/css/bootstrap.min.css';
};
```

---

## 15. Testing & QA Checklist

Use this checklist before every release.

### Responsive Testing

```
□ 320px  — smallest phone (iPhone SE)
□ 375px  — iPhone 14
□ 390px  — iPhone 14 Pro
□ 414px  — iPhone Plus
□ 768px  — iPad portrait
□ 1024px — iPad landscape / small laptop
□ 1280px — standard laptop
□ 1440px — large desktop
□ 1920px — full HD
□ 2560px — 4K display
```

### Performance Targets (Lighthouse)

```
□ Performance score    ≥ 90
□ Largest Contentful Paint (LCP) < 2.5s
□ First Input Delay (FID)        < 100ms
□ Cumulative Layout Shift (CLS)  < 0.1
□ Time to Interactive (TTI)      < 3.5s
□ Total Blocking Time (TBT)      < 200ms
```

### Accessibility

```
□ Run axe DevTools / Lighthouse A11y audit — score ≥ 95
□ Tab through entire page with keyboard only
□ Test with screen reader (NVDA, VoiceOver, TalkBack)
□ Verify all color contrast ratios ≥ 4.5:1 (AA)
□ All images have alt text (or empty alt for decorative)
□ All form inputs have associated labels
□ Focus indicators visible on all interactive elements
□ No keyboard traps
□ Skip navigation link present
```

### Cross-Browser Testing

```
□ Chrome (latest 2 versions)
□ Firefox (latest 2 versions)
□ Safari (latest 2 versions on macOS + iOS)
□ Edge (latest 2 versions)
□ Samsung Internet (mobile)
```

### HTML Validation

```bash
# Validate HTML
npx html-validate "dist/**/*.html"

# Check for broken links
npx broken-link-checker http://localhost:5173

# Lighthouse CI
npm install -g @lhci/cli
lhci autorun
```

---

## 16. Deployment & CI/CD Tips

### Build Script (`package.json`)

```json
{
  "scripts": {
    "dev":     "vite",
    "build":   "vite build",
    "preview": "vite preview",
    "lint:css": "stylelint 'src/**/*.scss'",
    "lint:html": "html-validate 'src/**/*.html'",
    "a11y":    "axe http://localhost:5173 --exit",
    "perf":    "lhci autorun",
    "validate": "npm run lint:css && npm run lint:html"
  }
}
```

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Build & Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run validate
      
      - name: Build
        run: npm run build
      
      - name: Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
      
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v2
        with:
          publish-dir: './dist'
          production-branch: main
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

### `.browserslistrc`

```
> 0.5%
last 2 versions
Firefox ESR
not dead
not IE 11
```

---

## Quick Reference Cards

### Bootstrap 5 Spacing Scale

| Class | Value |
|---|---|
| `*-0` | 0 |
| `*-1` | 0.25rem (4px) |
| `*-2` | 0.5rem (8px) |
| `*-3` | 1rem (16px) |
| `*-4` | 1.5rem (24px) |
| `*-5` | 3rem (48px) |
| `*-6` *(custom)* | 5rem (80px) |
| `*-7` *(custom)* | 8rem (128px) |

### Most-Used Utility Combinations

```html
<!-- Visually centered section -->
<section class="py-6 text-center">

<!-- Card with hover effect -->
<div class="card border-0 shadow-sm rounded-4 h-100">

<!-- Responsive text alignment -->
<p class="text-center text-md-start">

<!-- Full-bleed on mobile, contained on desktop -->
<div class="container-fluid container-md">

<!-- Sticky sidebar -->
<aside class="sticky-top" style="top: calc(var(--nav-height) + 1rem)">

<!-- Vertically centered flex row -->
<div class="d-flex align-items-center gap-3">
```

---

*Guide version: 2025 — Bootstrap 5.3.x compatible*
*License: MIT — Free to use, modify, and distribute*
