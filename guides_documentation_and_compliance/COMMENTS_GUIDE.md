# 📝 GUIDE TO WRITING QUALITY COMMENTS

## Philosophy of Code Commenting

> **Golden Mean Rule**: Code should be self-documenting, comments explain "WHY", not "WHAT"

---

# 🌐 PART 1: HTML COMMENTS

## 📋 HTML COMMENTING PRINCIPLES

### 1. **Structural Separation** (Main Pattern)

```html
<!-- ========================================================================== -->
<!-- SECTION NAME - Brief Description                                           -->
<!-- Extended explanation if needed, architectural notes                        -->
<!-- ========================================================================== -->

<!-- Subsection or Component -->
<div class="component">
    <!-- Content here -->
</div>
```

**Use for:**
- Main page sections (header, main, footer)
- Large components (navigation, sidebar, modals)
- Logical content blocks

---

### 2. **Comment Hierarchy**

#### Level 1: Main Sections (80 characters)
```html
<!-- ========================================================================== -->
<!-- HEADER - Main Navigation & Branding                                        -->
<!-- Fixed top navigation with search, user actions, and theme switcher         -->
<!-- ========================================================================== -->
<header class="main-header">
    ...
</header>
```

#### Level 2: Subsections (60 characters)
```html
<!-- ====================================================== -->
<!-- USER NAVIGATION - Account Actions                     -->
<!-- ====================================================== -->
<nav class="user-nav">
    ...
</nav>
```

#### Level 3: Components (no lines)
```html
<!-- Search Form with Category Filter -->
<form class="search-form">
    ...
</form>
```

#### Level 4: Inline Explanations
```html
<!-- Dropdown menu shown on category button click -->
<div class="dropdown-menu" id="categoryMenu">
    ...
</div>
```

---

### 3. **When NOT to Comment HTML**

❌ **BAD** - Obvious comments:
```html
<!-- Navigation -->
<nav>...</nav>

<!-- Button -->
<button>Click me</button>

<!-- Div -->
<div class="container">...</div>
```

✅ **GOOD** - Meaningful comments:
```html
<!-- Navigation: Hidden on mobile (<992px), uses offcanvas instead -->
<nav class="d-none d-lg-block">...</nav>

<!-- Submit button: Disabled until form validation passes -->
<button type="submit" disabled>Submit</button>

<!-- Container: Max-width changes based on viewport (see responsive.css) -->
<div class="container">...</div>
```

---

### 4. **Special Comment Types**

#### TODO comments
```html
<!-- TODO: Replace placeholder image with actual product photo -->
<img src="placeholder.jpg" alt="Product">

<!-- TODO: Add lazy loading for better performance -->
<img src="large-image.jpg" alt="Hero">

<!-- TODO: Implement accessibility landmarks (ARIA) -->
<div class="modal">...</div>
```

#### FIXME comments
```html
<!-- FIXME: Button overlaps on screens <375px -->
<button class="cta-button">Sign Up</button>

<!-- FIXME: Missing alt text for accessibility -->
<img src="icon.svg">
```

#### HACK/WORKAROUND comments
```html
<!-- HACK: Extra wrapper needed for Safari flexbox bug -->
<div class="safari-flex-fix">
    <div class="actual-content">...</div>
</div>

<!-- WORKAROUND: Inline style required due to Bootstrap specificity -->
<div class="card" style="margin-bottom: 2rem;">...</div>
```

#### NOTE/WARNING comments
```html
<!-- NOTE: This structure is required by Bootstrap 5 Offcanvas -->
<div class="offcanvas offcanvas-start">...</div>

<!-- WARNING: Do not remove data-bs-dismiss, it's needed for modal closing -->
<button data-bs-dismiss="modal">Close</button>
```

---

### 5. **Closing Tag Comments**

For large code blocks (>50 lines), add a comment to the closing tag:

```html
<!-- ========================================================================== -->
<!-- SIDEBAR NAVIGATION                                                         -->
<!-- ========================================================================== -->
<div class="sidebar-nav offcanvas offcanvas-start" id="sidebarNav">
    
    <!-- Sidebar Header -->
    <div class="offcanvas-header">
        <h5>Categories</h5>
        <button type="button" class="btn-close"></button>
    </div>
    
    <!-- Sidebar Body -->
    <div class="offcanvas-body">
        <!-- Navigation Links -->
        <nav>
            <a href="#">Electronics</a>
            <a href="#">Fashion</a>
            <a href="#">Home & Living</a>
        </nav>
        
        <!-- Search Form -->
        <form class="sidebar-search">
            <input type="search" placeholder="Search...">
            <button type="submit">Search</button>
        </form>
    </div>
    
    <!-- Sidebar Footer -->
    <div class="offcanvas-footer">
        <p>&copy; 2024 Company</p>
    </div>
    
</div><!-- /.sidebar-nav (end SIDEBAR NAVIGATION) -->
```

---

### 6. **Conditional Comments** (for older browsers)

```html
<!--[if lt IE 9]>
    <script src="html5shiv.js"></script>
    <script src="respond.min.js"></script>
<![endif]-->

<!--[if IE]>
    <link rel="stylesheet" href="ie-fixes.css">
<![endif]-->
```

---

### 7. **Temporarily Disabling Code**

```html
<!-- DISABLED: Feature not ready for production
<div class="new-feature">
    <h2>Coming Soon!</h2>
</div>
-->

<!-- DEPRECATED: Old navigation, remove after testing new version
<nav class="old-nav">...</nav>
-->
```

---

### 8. **Documenting data-attributes**

```html
<!-- 
    data-bs-toggle: Bootstrap collapse trigger
    data-bs-target: ID of element to collapse
    aria-expanded: Accessibility state indicator
-->
<button 
    data-bs-toggle="collapse" 
    data-bs-target="#collapseOne"
    aria-expanded="false">
    Toggle
</button>
```

---

### 9. **Design System Comments**

```html
<!-- 
    DESIGN SYSTEM: Primary Button
    - Color: var(--primary-color) #0d6efd
    - Padding: 12px 24px
    - Border-radius: 8px
    - Hover: Darken 10%
    - Active: Scale 0.98
-->
<button class="btn btn-primary">
    Click Me
</button>
```

---

### 10. **Responsive Comments**

```html
<!-- Desktop: 3 columns | Tablet: 2 columns | Mobile: 1 column -->
<div class="row">
    <div class="col-lg-4 col-md-6 col-12">...</div>
    <div class="col-lg-4 col-md-6 col-12">...</div>
    <div class="col-lg-4 col-md-6 col-12">...</div>
</div>

<!-- Hidden on mobile (<992px), shown on desktop -->
<div class="d-none d-lg-block">
    Desktop Navigation
</div>

<!-- Visible only on mobile -->
<div class="d-lg-none">
    Mobile Navigation
</div>
```

---

### 11. **SEO Comments**

```html
<!-- SEO: H1 should be unique per page and contain primary keyword -->
<h1>Best Laptops 2024 - Gaming & Business</h1>

<!-- SEO: Meta description optimized for 155 characters -->
<meta name="description" content="...">

<!-- SEO: Structured data for rich snippets -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name"
}
</script>
```

---

### 12. **Accessibility (A11y) Comments**

```html
<!-- A11Y: Skip link for keyboard navigation -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- A11Y: ARIA landmark for screen readers -->
<nav role="navigation" aria-label="Main navigation">...</nav>

<!-- A11Y: Image decorative, empty alt is intentional -->
<img src="decorative-line.svg" alt="" role="presentation">

<!-- A11Y: Focus trap for modal accessibility -->
<div class="modal" role="dialog" aria-modal="true">...</div>
```

---

### 13. **Performance Comments**

```html
<!-- PERFORMANCE: Preload critical font -->
<link rel="preload" href="font.woff2" as="font" crossorigin>

<!-- PERFORMANCE: Lazy load images below the fold -->
<img src="placeholder.jpg" data-src="actual.jpg" loading="lazy" alt="Product">

<!-- PERFORMANCE: Async script to prevent render blocking -->
<script src="analytics.js" async></script>

<!-- PERFORMANCE: Defer non-critical JavaScript -->
<script src="chat-widget.js" defer></script>
```

---

### 14. **Integration комментарии**

```html
<!-- INTEGRATION: Google Tag Manager container -->
<noscript>
    <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXX"></iframe>
</noscript>

<!-- INTEGRATION: Facebook Pixel tracking code -->
<script>
    !function(f,b,e,v,n,t,s)
    {/* Facebook Pixel Code */}
</script>

<!-- INTEGRATION: Stripe payment form -->
<form id="payment-form" data-stripe-key="pk_test_xxxxx">
    <!-- Stripe.js will inject card element here -->
    <div id="card-element"></div>
</form>
```

---

### 15. **Team collaboration комментарии**

```html
<!-- @author: John Doe -->
<!-- @created: 2024-01-15 -->
<!-- @modified: 2024-02-14 by Jane Smith -->
<!-- @ticket: JIRA-1234 -->
<section class="feature-section">
    ...
</section>

<!-- REVIEW: Please check mobile layout - @jane -->
<div class="complex-grid">...</div>

<!-- QUESTION: Should this be a <section> or <article>? - @john -->
<div class="content-block">...</div>
```

---

## 🎯 HTML КОММЕНТАРИИ: BEST PRACTICES

### ✅ DO:

1. **Комментировать структуру** - основные секции и их назначение
2. **Объяснять неочевидное** - специфичное поведение, workarounds
3. **Документировать зависимости** - Bootstrap классы, JS инициализация
4. **Отмечать состояния** - hidden/visible, active/inactive
5. **Использовать иерархию** - разные уровни комментариев
6. **Указывать авторство** - для важных компонентов
7. **Добавлять TODO/FIXME** - для будущих улучшений

### ❌ DON'T:

1. **Не комментировать очевидное** - "Button", "Div", "Image"
2. **Не дублировать код** - комментарий не должен повторять HTML
3. **Не оставлять устаревшие комментарии** - удалять при изменениях
4. **Не использовать слишком много** - только там где нужно
5. **Не писать романы** - краткость и ясность
6. **Не забывать обновлять** - комментарии должны быть актуальными

---

## 📏 ШАБЛОНЫ ДЛЯ КОПИРОВАНИЯ

### Основная секция:
```html
<!-- ========================================================================== -->
<!-- SECTION_NAME - Brief Description                                           -->
<!-- Additional context, dependencies, or architectural notes                   -->
<!-- ========================================================================== -->
```

### Подсекция:
```html
<!-- ====================================================== -->
<!-- SUBSECTION_NAME - Brief Description                   -->
<!-- ====================================================== -->
```

### Компонент:
```html
<!-- Component Name: Purpose and behavior -->
<div class="component">...</div>
```

### Закрывающий тег:
```html
</div><!-- /.class-name (end SECTION_NAME) -->
```

---

# 🎨 PART 2: CSS COMMENTS

## 📋 CSS COMMENTING PRINCIPLES

### 1. **Структура файла CSS**

```css
/* ========================================================================== */
/* TABLE OF CONTENTS                                                          */
/* ========================================================================== */
/*
    1. CSS Variables / Custom Properties
    2. Reset & Base Styles
    3. Typography
    4. Layout & Grid
    5. Components
        5.1 Buttons
        5.2 Forms
        5.3 Cards
        5.4 Modals
    6. Utilities
    7. Responsive / Media Queries
    8. Print Styles
*/


/* ========================================================================== */
/* 1. CSS VARIABLES / CUSTOM PROPERTIES                                       */
/* Design tokens for consistent theming across the application               */
/* ========================================================================== */

:root {
    /* Colors */
    --primary-color: #0d6efd;      /* Primary brand color */
    --secondary-color: #6c757d;    /* Secondary actions */
    --success-color: #198754;      /* Success states */
    --danger-color: #dc3545;       /* Error states */
    
    /* Spacing */
    --spacing-xs: 0.25rem;         /* 4px */
    --spacing-sm: 0.5rem;          /* 8px */
    --spacing-md: 1rem;            /* 16px */
    --spacing-lg: 1.5rem;          /* 24px */
    --spacing-xl: 2rem;            /* 32px */
    
    /* Typography */
    --font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-size-base: 1rem;        /* 16px */
    --line-height-base: 1.5;       /* 24px */
    
    /* Transitions */
    --transition-speed: 0.3s;
    --transition-easing: cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

### 2. **Комментирование секций**

```css
/* ========================================================================== */
/* BUTTONS - Interactive Elements                                             */
/* Button styles following Material Design principles with focus states       */
/* ========================================================================== */

/* --- Base Button --- */
.btn {
    /* Layout */
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    
    /* Spacing */
    padding: 0.75rem 1.5rem;
    
    /* Typography */
    font-weight: 600;
    font-size: 1rem;
    text-decoration: none;
    
    /* Visual */
    border: 2px solid transparent;
    border-radius: 0.5rem;
    background-color: var(--primary-color);
    color: white;
    
    /* Interaction */
    cursor: pointer;
    transition: all var(--transition-speed) var(--transition-easing);
    
    /* Accessibility */
    user-select: none;
}

/* Hover state with scale animation */
.btn:hover {
    background-color: var(--primary-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Active state with press effect */
.btn:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Focus state for keyboard navigation */
.btn:focus-visible {
    outline: 3px solid var(--primary-color);
    outline-offset: 2px;
}

/* Disabled state */
.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
}
```

---

### 3. **Группировка свойств с комментариями**

```css
.card {
    /* === Positioning === */
    position: relative;
    z-index: 1;
    
    /* === Box Model === */
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 400px;
    padding: 1.5rem;
    margin: 0 auto;
    
    /* === Visual === */
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    
    /* === Typography === */
    color: var(--text-color);
    font-size: 1rem;
    line-height: 1.6;
    
    /* === Transitions === */
    transition: 
        transform var(--transition-speed),
        box-shadow var(--transition-speed);
    
    /* === Other === */
    overflow: hidden;
}
```

**Порядок свойств (стандарт):**
1. Positioning (position, top, right, z-index)
2. Box Model (display, width, height, padding, margin, border)
3. Visual (background, color, opacity, box-shadow)
4. Typography (font-*, text-*, line-height, letter-spacing)
5. Transitions/Animations
6. Other (cursor, pointer-events, overflow)

---

### 4. **Комментирование сложной логики**

#### Magic Numbers (объяснять!)
```css
.sidebar {
    /* 
        80px = header height (64px) + margin (16px)
        Prevents content from hiding behind fixed header
    */
    margin-top: 80px;
    
    /* 
        280px = optimal width for navigation items (56px icon + 200px text + padding)
        Based on average menu item length in 15 languages
    */
    width: 280px;
}
```

#### Browser-specific hacks
```css
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    
    /* 
        HACK: Safari grid bug fix
        Safari calculates minmax() incorrectly with percentage widths
        Adding explicit min-width prevents layout collapse
    */
    grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
}
```

#### Z-index system
```css
/* 
    Z-INDEX SCALE
    Maintaining consistent layering across the application
    
    Base layer: 0
    Content: 1-9
    Overlays: 10-19
    Dropdowns: 20-29
    Sticky elements: 30-39
    Fixed headers: 40-49
    Modals: 50-59
    Toasts: 60-69
    Debug/Dev tools: 70-79
    Critical overlays: 80+
*/

.dropdown-menu {
    z-index: 20; /* Dropdowns layer */
}

.modal {
    z-index: 50; /* Modal layer */
}

.toast {
    z-index: 60; /* Toast notification layer */
}
```

---

### 5. **BEM комментарии**

```css
/* ========================================================================== */
/* CARD COMPONENT - BEM Methodology                                           */
/* Block-Element-Modifier naming convention                                   */
/* ========================================================================== */

/* Block: .card */
.card {
    /* Base card styles */
}

/* Element: .card__header */
.card__header {
    /* Card header with title and actions */
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
}

/* Element: .card__title */
.card__title {
    /* Card title text */
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0;
}

/* Element: .card__body */
.card__body {
    /* Main card content area */
    padding: 1.5rem;
}

/* Element: .card__footer */
.card__footer {
    /* Card footer with actions */
    padding: 1rem;
    border-top: 1px solid var(--border-color);
}

/* Modifier: .card--featured */
.card--featured {
    /* Highlighted card variant with accent color */
    border-left: 4px solid var(--accent-color);
    background: linear-gradient(135deg, rgba(13, 110, 253, 0.05), transparent);
}

/* Modifier: .card--compact */
.card--compact {
    /* Reduced padding for compact layout */
}

.card--compact .card__body {
    padding: 1rem;
}

/* State: .card.is-loading */
.card.is-loading {
    /* Loading state with animated skeleton */
    pointer-events: none;
    opacity: 0.6;
}
```

---

### 6. **Responsive комментарии**

```css
/* ========================================================================== */
/* RESPONSIVE DESIGN                                                          */
/* Mobile-first approach with progressive enhancement                         */
/* ========================================================================== */

/* 
    BREAKPOINT SYSTEM
    - xs: 0-575px (Mobile portrait)
    - sm: 576-767px (Mobile landscape)
    - md: 768-991px (Tablet)
    - lg: 992-1199px (Desktop)
    - xl: 1200-1399px (Large desktop)
    - xxl: 1400px+ (Extra large desktop)
*/

/* --- Mobile First (Default) --- */
.container {
    /* Base: Mobile portrait (320px-575px) */
    width: 100%;
    padding: 0 1rem;
}

/* --- Small devices (≥576px) --- */
@media (min-width: 576px) {
    .container {
        max-width: 540px;
    }
}

/* --- Medium devices (≥768px) --- */
@media (min-width: 768px) {
    .container {
        max-width: 720px;
    }
    
    /* Switch to 2-column grid on tablets */
    .grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* --- Large devices (≥992px) --- */
@media (min-width: 992px) {
    .container {
        max-width: 960px;
    }
    
    /* Desktop navigation becomes horizontal */
    .nav {
        flex-direction: row;
    }
    
    /* 3-column grid on desktop */
    .grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* --- Extra large devices (≥1200px) --- */
@media (min-width: 1200px) {
    .container {
        max-width: 1140px;
    }
    
    /* 4-column grid on large screens */
    .grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

/* --- Print styles --- */
@media print {
    /* Hide navigation and interactive elements when printing */
    .no-print,
    .navbar,
    .sidebar,
    button {
        display: none !important;
    }
    
    /* Expand content to full width */
    .container {
        max-width: 100%;
    }
}
```

---

### 7. **Animation комментарии**

```css
/* ========================================================================== */
/* ANIMATIONS & TRANSITIONS                                                   */
/* Smooth micro-interactions following Material Design motion principles      */
/* ========================================================================== */

/* 
    EASING FUNCTIONS
    - ease-in: Start slow, speed up (entrance)
    - ease-out: Start fast, slow down (exit)
    - ease-in-out: Smooth acceleration and deceleration (transition)
*/

/* Fade in animation */
@keyframes fadeIn {
    /* Start: invisible and slightly below */
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    
    /* End: fully visible at natural position */
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Apply fade-in to elements as they enter viewport */
.fade-in {
    animation: fadeIn 0.6s ease-out forwards;
}

/* Pulse animation for loading indicators */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    
    50% {
        opacity: 0.7;
        transform: scale(0.95);
    }
}

.loading-pulse {
    /* Infinite pulse with 2-second cycle */
    animation: pulse 2s ease-in-out infinite;
}

/* 
    PERFORMANCE NOTE:
    Only animate transform and opacity for better performance
    These properties can be GPU-accelerated
    Avoid animating width, height, top, left (causes reflow)
*/

.smooth-move {
    /* Use transform instead of position changes */
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    will-change: transform; /* Hint browser for optimization */
}
```

---

### 8. **Utility Classes комментарии**

```css
/* ========================================================================== */
/* UTILITY CLASSES                                                            */
/* Single-purpose classes for rapid prototyping and consistency              */
/* ========================================================================== */

/* --- Spacing Utilities --- */

/* Margin Top */
.mt-0 { margin-top: 0 !important; }
.mt-1 { margin-top: var(--spacing-xs) !important; }  /* 4px */
.mt-2 { margin-top: var(--spacing-sm) !important; }  /* 8px */
.mt-3 { margin-top: var(--spacing-md) !important; }  /* 16px */
.mt-4 { margin-top: var(--spacing-lg) !important; }  /* 24px */
.mt-5 { margin-top: var(--spacing-xl) !important; }  /* 32px */

/* Padding */
.p-0 { padding: 0 !important; }
.p-1 { padding: var(--spacing-xs) !important; }
.p-2 { padding: var(--spacing-sm) !important; }
.p-3 { padding: var(--spacing-md) !important; }
.p-4 { padding: var(--spacing-lg) !important; }
.p-5 { padding: var(--spacing-xl) !important; }

/* --- Display Utilities --- */

/* Display types with browser prefixes for older browsers */
.d-none { display: none !important; }
.d-block { display: block !important; }
.d-inline { display: inline !important; }
.d-inline-block { display: inline-block !important; }
.d-flex { display: flex !important; }
.d-inline-flex { display: inline-flex !important; }
.d-grid { display: grid !important; }

/* --- Text Utilities --- */

/* Text alignment */
.text-left { text-align: left !important; }
.text-center { text-align: center !important; }
.text-right { text-align: right !important; }

/* Text transformation */
.text-lowercase { text-transform: lowercase !important; }
.text-uppercase { text-transform: uppercase !important; }
.text-capitalize { text-transform: capitalize !important; }

/* Font weight */
.fw-light { font-weight: 300 !important; }
.fw-normal { font-weight: 400 !important; }
.fw-medium { font-weight: 500 !important; }
.fw-semibold { font-weight: 600 !important; }
.fw-bold { font-weight: 700 !important; }

/* --- Visibility Utilities --- */

/* 
    Screen reader only content
    Visually hidden but accessible to assistive technologies
*/
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Visually hidden until focused (skip links) */
.sr-only-focusable:focus {
    position: static;
    width: auto;
    height: auto;
    margin: 0;
    overflow: visible;
    clip: auto;
    white-space: normal;
}
```

---

### 9. **Browser Compatibility комментарии**

```css
/* ========================================================================== */
/* BROWSER COMPATIBILITY                                                      */
/* Vendor prefixes and fallbacks for cross-browser support                   */
/* ========================================================================== */

.gradient-bg {
    /* Fallback for browsers that don't support gradients */
    background-color: #0d6efd;
    
    /* Modern gradient (all current browsers) */
    background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
}

.sticky-header {
    /* Fallback for old browsers */
    position: fixed;
    
    /* Sticky positioning (IE11+, all modern browsers) */
    position: sticky;
    top: 0;
}

.grid-layout {
    /* Fallback for browsers without grid support */
    display: flex;
    flex-wrap: wrap;
    
    /* Modern grid layout */
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

/* 
    CSS Grid feature query
    Enhanced layout for browsers that support grid
*/
@supports (display: grid) {
    .grid-layout {
        display: grid;
    }
}

/* 
    Backdrop filter feature query
    Glassmorphism effect for supporting browsers
*/
@supports (backdrop-filter: blur(10px)) or (-webkit-backdrop-filter: blur(10px)) {
    .glass-panel {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px); /* Safari */
    }
}
```

---

### 10. **Dark Mode комментарии**

```css
/* ========================================================================== */
/* DARK MODE THEME                                                            */
/* Color scheme following system preferences or manual toggle                */
/* ========================================================================== */

/* Light mode (default) */
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --border-color: #dee2e6;
}

/* 
    Dark mode via data attribute
    Toggled by JavaScript: document.documentElement.setAttribute('data-theme', 'dark')
*/
[data-theme="dark"] {
    --bg-primary: #212529;
    --bg-secondary: #343a40;
    --text-primary: #f8f9fa;
    --text-secondary: #adb5bd;
    --border-color: #495057;
}

/* 
    Automatic dark mode based on system preference
    Respects user's OS-level dark mode setting
*/
@media (prefers-color-scheme: dark) {
    :root:not([data-theme]) {
        --bg-primary: #212529;
        --bg-secondary: #343a40;
        --text-primary: #f8f9fa;
        --text-secondary: #adb5bd;
        --border-color: #495057;
    }
}

/* Apply theme colors to elements */
body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    
    /* Smooth transition when switching themes */
    transition: background-color 0.3s ease, color 0.3s ease;
}

.card {
    background-color: var(--bg-secondary);
    border-color: var(--border-color);
}
```

---

### 11. **Performance комментарии**

```css
/* ========================================================================== */
/* PERFORMANCE OPTIMIZATIONS                                                  */
/* Critical CSS loaded inline, non-critical deferred                         */
/* ========================================================================== */

/* 
    CRITICAL CSS (above-the-fold)
    Inline this in <head> for faster initial render
    Includes: reset, typography, header, hero section
*/

/* 
    GPU Acceleration Hints
    Use will-change sparingly, only for active animations
*/
.animating-element {
    will-change: transform, opacity;
}

.animating-element:not(.is-animating) {
    /* Remove hint when not animating to free GPU memory */
    will-change: auto;
}

/* 
    Contain layout for better rendering performance
    Tells browser that element's children won't affect outside layout
*/
.isolated-component {
    contain: layout style paint;
}

/* 
    Content-visibility for virtual scrolling
    Dramatically improves performance for long lists
*/
.virtual-list-item {
    content-visibility: auto;
    contain-intrinsic-size: 0 200px; /* Estimated height */
}

/* 
    Font loading optimization
    Prevent FOIT (Flash of Invisible Text)
*/
@font-face {
    font-family: 'CustomFont';
    src: url('font.woff2') format('woff2');
    font-display: swap; /* Show fallback immediately, swap when loaded */
}
```

---

### 12. **TODO/FIXME комментарии в CSS**

```css
/* TODO: Replace hex colors with CSS custom properties for themability */
.old-component {
    color: #333333;
    background: #ffffff;
}

/* FIXME: Z-index too high, conflicts with modal (z-index: 1050) */
.dropdown {
    z-index: 9999;
}

/* HACK: Negative margin to overcome Bootstrap's default spacing */
.custom-section {
    margin-top: -2rem;
}

/* NOTE: This specificity is required to override Bootstrap defaults */
.navbar.navbar-dark .navbar-nav .nav-link {
    color: white;
}

/* DEPRECATED: Remove after migrating to Flexbox layout */
.float-left {
    float: left;
}

/* REVIEW: Is 500px the right breakpoint? Need designer input */
@media (max-width: 500px) {
    .responsive-element {
        display: none;
    }
}
```

---

## 🎯 CSS КОММЕНТАРИИ: BEST PRACTICES

### ✅ DO:

1. **Использовать Table of Contents** для больших файлов
2. **Группировать свойства** по категориям (positioning, box model, visual...)
3. **Объяснять magic numbers** - почему именно это значение
4. **Документировать hacks** - почему нужен workaround
5. **Комментировать z-index** - система слоев
6. **Указывать browser compatibility** - префиксы, fallbacks
7. **Описывать responsive behavior** - breakpoints и изменения
8. **Добавлять performance notes** - will-change, contain

### ❌ DON'T:

1. **Не комментировать очевидные свойства** - `color: red; /* Red color */`
2. **Не оставлять старый закомментированный код** - использовать Git
3. **Не писать слишком длинные комментарии** - краткость важна
4. **Не забывать обновлять** - комментарии должны быть актуальными
5. **Не перегружать утилиты комментариями** - они самодокументируемые

---

# 💻 PART 3: JAVASCRIPT COMMENTS

## 📋 JAVASCRIPT COMMENTING PRINCIPLES

### 1. **JSDoc - стандарт документирования**

```javascript
/**
 * Calculates the total price with tax
 * 
 * @param {number} price - Base price of the item
 * @param {number} taxRate - Tax rate as decimal (e.g., 0.15 for 15%)
 * @param {Object} options - Optional configuration
 * @param {boolean} options.roundUp - Whether to round up to nearest cent
 * @param {string} options.currency - Currency code (default: 'USD')
 * @returns {number} Total price including tax
 * @throws {TypeError} If price or taxRate is not a number
 * @example
 * // Calculate $100 with 15% tax
 * const total = calculateTotal(100, 0.15);
 * console.log(total); // 115
 * 
 * @example
 * // With options
 * const total = calculateTotal(100, 0.15, { 
 *     roundUp: true, 
 *     currency: 'EUR' 
 * });
 */
function calculateTotal(price, taxRate, options = {}) {
    if (typeof price !== 'number' || typeof taxRate !== 'number') {
        throw new TypeError('Price and taxRate must be numbers');
    }
    
    const total = price * (1 + taxRate);
    
    return options.roundUp ? Math.ceil(total * 100) / 100 : total;
}
```

---

### 2. **Документирование классов**

```javascript
/**
 * SearchManager - Unified search functionality
 * 
 * Handles search operations from multiple sources (navbar, sidebar)
 * with analytics tracking and configurable behavior.
 * 
 * @class
 * @example
 * const searchManager = new SearchManager({
 *     searchEndpoint: '/api/search',
 *     enableAnalytics: true
 * });
 * 
 * searchManager.search('laptop', 'navbar', 'Electronics');
 */
class SearchManager {
    /**
     * Search source constants
     * @type {Object}
     * @property {string} NAVBAR - Search from navbar
     * @property {string} SIDEBAR - Search from sidebar
     */
    static SOURCE = {
        NAVBAR: 'navbar',
        SIDEBAR: 'sidebar'
    };
    
    /**
     * Private configuration object
     * @type {Object}
     * @private
     */
    #config;
    
    /**
     * Cached navbar form element
     * @type {HTMLFormElement|null}
     * @private
     */
    #navbarForm;
    
    /**
     * Create a SearchManager instance
     * 
     * @param {Object} config - Configuration object
     * @param {string} config.navbarFormId - ID of navbar search form
     * @param {string} config.navbarInputId - ID of navbar search input
     * @param {string} config.searchEndpoint - Search API endpoint
     * @param {number} [config.minQueryLength=1] - Minimum query length
     * @param {boolean} [config.enableAnalytics=true] - Enable analytics tracking
     * @param {boolean} [config.enableDebugLog=false] - Enable debug logging
     * 
     * @throws {Error} If required form elements are not found
     */
    constructor(config = {}) {
        // Merge with defaults
        this.#config = {
            navbarFormId: 'navbarSearchForm',
            navbarInputId: 'navbarSearchInput',
            searchEndpoint: '/search',
            minQueryLength: 1,
            enableAnalytics: true,
            enableDebugLog: false,
            ...config
        };
        
        // Cache DOM elements
        this.#cacheElements();
        
        // Initialize event handlers
        this.#initEventHandlers();
        
        if (this.#config.enableDebugLog) {
            console.log('[SearchManager] Initialized', this.#config);
        }
    }
    
    /**
     * Cache DOM elements for performance
     * 
     * Finds and stores references to form and input elements
     * to avoid repeated DOM queries.
     * 
     * @private
     * @throws {Error} If required elements are not found
     */
    #cacheElements() {
        this.#navbarForm = document.getElementById(this.#config.navbarFormId);
        
        if (!this.#navbarForm) {
            throw new Error(`Navbar form not found: ${this.#config.navbarFormId}`);
        }
        
        // ... cache other elements
    }
    
    /**
     * Initialize event handlers
     * 
     * Sets up form submission handlers for navbar and sidebar search forms.
     * Prevents default form submission and calls search handler instead.
     * 
     * @private
     */
    #initEventHandlers() {
        // ... implementation
    }
    
    /**
     * Execute search with given parameters
     * 
     * This is the main public method for triggering searches programmatically.
     * Validates input, tracks analytics, and redirects to search results.
     * 
     * @param {string} query - Search query string
     * @param {string} [source=SearchManager.SOURCE.NAVBAR] - Search source
     * @param {string} [category=null] - Optional category filter
     * 
     * @returns {void}
     * 
     * @example
     * // Basic search
     * searchManager.search('laptop');
     * 
     * @example
     * // Search with category
     * searchManager.search('laptop', SearchManager.SOURCE.NAVBAR, 'Electronics');
     * 
     * @public
     */
    search(query, source = SearchManager.SOURCE.NAVBAR, category = null) {
        this.#handleSearch(query, source, category);
    }
    
    /**
     * Handle search logic
     * 
     * Internal method that performs validation, builds URL,
     * tracks analytics, and executes the search.
     * 
     * @param {string} query - Search query
     * @param {string} source - Search source
     * @param {string|null} category - Category filter
     * @private
     */
    #handleSearch(query, source, category) {
        // Validate query length
        if (!query || query.length < this.#config.minQueryLength) {
            if (this.#config.enableDebugLog) {
                console.warn('[SearchManager] Query too short:', query);
            }
            return;
        }
        
        // Track analytics if enabled
        if (this.#config.enableAnalytics) {
            this.#trackSearch(query, source, category);
        }
        
        // Build and execute search
        const url = this.#buildSearchUrl(query, source, category);
        this.#executeSearch(url);
    }
    
    /**
     * Build search URL with query parameters
     * 
     * @param {string} query - Search query
     * @param {string} source - Search source
     * @param {string|null} category - Category filter
     * @returns {string} Complete search URL with query parameters
     * @private
     */
    #buildSearchUrl(query, source, category) {
        const params = new URLSearchParams();
        params.set('q', query);
        params.set('source', source);
        
        if (category && category !== 'All') {
            params.set('category', category.toLowerCase());
        }
        
        return `${this.#config.searchEndpoint}?${params.toString()}`;
    }
    
    /**
     * Execute search by redirecting to URL
     * 
     * @param {string} url - Search results URL
     * @private
     */
    #executeSearch(url) {
        if (this.#config.enableDebugLog) {
            console.log('[SearchManager] Navigating to:', url);
        }
        
        window.location.href = url;
    }
    
    /**
     * Track search in analytics
     * 
     * Sends search event to Google Analytics and data layer
     * for tracking user search behavior.
     * 
     * @param {string} query - Search query
     * @param {string} source - Search source
     * @param {string|null} category - Category filter
     * @private
     */
    #trackSearch(query, source, category) {
        // Google Analytics 4
        if (typeof gtag !== 'undefined') {
            gtag('event', 'search', {
                search_term: query,
                search_source: source,
                search_category: category || 'all'
            });
        }
        
        // Data Layer for GTM
        if (typeof dataLayer !== 'undefined') {
            dataLayer.push({
                event: 'site_search',
                searchQuery: query,
                searchSource: source,
                searchCategory: category
            });
        }
    }
    
    /**
     * Update configuration
     * 
     * Allows changing configuration after initialization.
     * Useful for A/B testing or dynamic configuration.
     * 
     * @param {Object} newConfig - Configuration updates
     * @returns {void}
     * @public
     * 
     * @example
     * searchManager.updateConfig({
     *     enableDebugLog: true,
     *     minQueryLength: 3
     * });
     */
    updateConfig(newConfig) {
        Object.assign(this.#config, newConfig);
        
        if (this.#config.enableDebugLog) {
            console.log('[SearchManager] Config updated:', this.#config);
        }
    }
    
    /**
     * Get current configuration (read-only copy)
     * 
     * @returns {Object} Copy of current configuration
     * @public
     */
    getConfig() {
        return { ...this.#config };
    }
}
```

---

### 3. **Комментарии для сложной логики**

```javascript
/**
 * Calculate optimal grid column count based on container width
 * 
 * This algorithm balances between:
 * 1. Minimum column width (300px for readability)
 * 2. Maximum columns (6 for visual hierarchy)
 * 3. Responsive behavior (fewer columns on mobile)
 * 
 * @param {number} containerWidth - Container width in pixels
 * @returns {number} Optimal number of columns
 */
function calculateColumns(containerWidth) {
    const MIN_COLUMN_WIDTH = 300;
    const MAX_COLUMNS = 6;
    
    // Calculate how many 300px columns fit
    const possibleColumns = Math.floor(containerWidth / MIN_COLUMN_WIDTH);
    
    // Clamp between 1 and MAX_COLUMNS
    // Math.max ensures at least 1 column
    // Math.min prevents exceeding maximum
    const columns = Math.max(1, Math.min(possibleColumns, MAX_COLUMNS));
    
    return columns;
}

/**
 * Debounce function calls
 * 
 * Limits how often a function can be called by waiting for a quiet period.
 * Useful for expensive operations triggered by rapid events (resize, scroll, input).
 * 
 * Technical details:
 * - Uses closure to maintain timer reference
 * - clearTimeout cancels pending calls
 * - setTimeout schedules the actual call
 * 
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 * 
 * @example
 * const debouncedResize = debounce(() => {
 *     console.log('Window resized!');
 * }, 250);
 * 
 * window.addEventListener('resize', debouncedResize);
 */
function debounce(func, wait) {
    let timeout;
    
    return function executedFunction(...args) {
        // Store context for proper 'this' binding
        const context = this;
        
        // Cancel previous scheduled call
        clearTimeout(timeout);
        
        // Schedule new call after wait period
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}
```

---

### 4. **Inline комментарии для трicky кода**

```javascript
function processUserData(data) {
    // EDGE CASE: API sometimes returns null instead of empty array
    // This normalizes the data structure for consistent handling
    const items = data.items || [];
    
    // Filter out soft-deleted items (deleted_at !== null)
    // Backend returns them for audit purposes, but we hide from UI
    const activeItems = items.filter(item => !item.deleted_at);
    
    // PERFORMANCE: Map is faster than multiple array iterations
    // We need both ID lookup and sorted list, so create both in one pass
    const itemMap = new Map();
    const sortedItems = activeItems
        .map(item => {
            // Store in map for O(1) lookup later
            itemMap.set(item.id, item);
            
            // Return item for sorting
            return item;
        })
        .sort((a, b) => {
            // Sort by priority (descending), then by name (ascending)
            if (a.priority !== b.priority) {
                return b.priority - a.priority; // Higher priority first
            }
            return a.name.localeCompare(b.name); // Alphabetical
        });
    
    return {
        items: sortedItems,
        itemMap: itemMap,
        count: sortedItems.length
    };
}
```

---

### 5. **TODO комментарии**

```javascript
// TODO: Add error handling for network failures
// TODO: Implement retry logic with exponential backoff
// TODO: Cache results in localStorage for offline support
async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
}

// TODO(@john): Review this algorithm with team
// Current complexity is O(n²), can we optimize to O(n log n)?
function findDuplicates(array) {
    // ... implementation
}

// TODO(priority: high): Fix memory leak in event listeners
// TODO(deadline: 2024-03-15): Migrate to new API endpoint
// TODO(ticket: JIRA-1234): Implement proper input sanitization
class FormValidator {
    // ... implementation
}
```

---

### 6. **FIXME комментарии**

```javascript
// FIXME: Race condition when multiple clicks happen rapidly
// Need to disable button during API call
async function handleSubmit() {
    const result = await api.submit(formData);
    showSuccessMessage(result);
}

// FIXME: Memory leak - event listener not removed on unmount
// Add cleanup in destructor or use WeakMap
class Component {
    constructor() {
        document.addEventListener('click', this.handleClick);
    }
}

// FIXME: XSS vulnerability - user input not sanitized
// Use DOMPurify before inserting HTML
function displayUserComment(comment) {
    element.innerHTML = comment; // DANGEROUS!
}

// FIXME: This breaks in IE11 due to arrow functions in constructor
// Rewrite using traditional function syntax or add polyfill
class ModernComponent {
    constructor() {
        this.handler = () => {
            // ...
        };
    }
}
```

---

### 7. **HACK/WORKAROUND комментарии**

```javascript
// HACK: Force reflow to trigger CSS transition
// Without this, transition doesn't play due to browser optimization
element.classList.add('transitioning');
void element.offsetWidth; // Force reflow
element.classList.add('active');

// WORKAROUND: Safari doesn't support :has() selector
// Manually toggle class on parent when checkbox is checked
checkbox.addEventListener('change', (e) => {
    const parent = e.target.closest('.item');
    parent.classList.toggle('has-checked-child', e.target.checked);
});

// HACK: Third-party library overwrites our global variable
// Save reference before library loads, restore after
const ourGlobal = window.conflictingName;
loadThirdPartyLibrary();
window.ourGlobal = ourGlobal;
window.theirGlobal = window.conflictingName;
window.conflictingName = ourGlobal;

// WORKAROUND: iOS Safari doesn't fire click events on non-interactive elements
// Add cursor: pointer to make elements "clickable" in iOS
element.style.cursor = 'pointer';
element.addEventListener('click', handler);
```

---

### 8. **NOTE/WARNING комментарии**

```javascript
// NOTE: This function must be called before DOM is ready
// It modifies the document structure during parsing
initializeEarlyFeatures();

// WARNING: Changing this value affects ALL user sessions
// Update requires database migration and can't be rolled back
const SESSION_TIMEOUT = 3600000; // 1 hour

// NOTE: API rate limit is 100 requests per minute
// Implement exponential backoff if you need more frequent calls
async function fetchData() {
    // ...
}

// WARNING: Do not remove this setTimeout
// It's a workaround for a React 18 hydration bug
// See: https://github.com/facebook/react/issues/24430
setTimeout(() => {
    initializeComponent();
}, 0);

// NOTE: This regex is intentionally permissive
// We validate properly on the server, this is just UI feedback
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// WARNING: This function has side effects
// It modifies the global state and triggers re-renders
// Consider using a pure function instead
function updateAppState(newData) {
    // ...
}
```

---

### 9. **Алгоритмы и сложность**

```javascript
/**
 * Binary search in sorted array
 * 
 * Time Complexity: O(log n)
 * Space Complexity: O(1)
 * 
 * @param {Array<number>} arr - Sorted array of numbers
 * @param {number} target - Value to find
 * @returns {number} Index of target, or -1 if not found
 */
function binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    
    // Continue while search space is valid
    while (left <= right) {
        // Calculate middle point
        // Using (left + right) / 2 can cause integer overflow
        // This formula prevents that issue
        const mid = left + Math.floor((right - left) / 2);
        
        if (arr[mid] === target) {
            return mid; // Found target
        } else if (arr[mid] < target) {
            left = mid + 1; // Target is in right half
        } else {
            right = mid - 1; // Target is in left half
        }
    }
    
    return -1; // Target not found
}

/**
 * Memoized Fibonacci calculation
 * 
 * Without memoization: O(2^n) time, O(n) space
 * With memoization: O(n) time, O(n) space
 * 
 * The cache prevents recalculating the same values multiple times,
 * trading space for dramatic time savings.
 */
const fibonacci = (() => {
    const cache = new Map();
    
    return function fib(n) {
        // Base cases
        if (n <= 1) return n;
        
        // Check cache first
        if (cache.has(n)) {
            return cache.get(n);
        }
        
        // Calculate and cache result
        const result = fib(n - 1) + fib(n - 2);
        cache.set(n, result);
        
        return result;
    };
})();
```

---

### 10. **Секции кода**

```javascript
/* ========================================================================== */
/* EVENT HANDLERS                                                             */
/* User interaction handlers with debouncing and throttling                   */
/* ========================================================================== */

/**
 * Handle search input changes (debounced)
 */
const handleSearchInput = debounce((e) => {
    const query = e.target.value;
    performSearch(query);
}, 300);

/**
 * Handle window resize (throttled)
 */
const handleResize = throttle(() => {
    updateLayout();
}, 100);


/* ========================================================================== */
/* API CALLS                                                                  */
/* Backend communication with error handling and retries                      */
/* ========================================================================== */

/**
 * Fetch user data from API
 */
async function fetchUser(userId) {
    // ... implementation
}

/**
 * Update user profile
 */
async function updateUser(userId, data) {
    // ... implementation
}


/* ========================================================================== */
/* UTILITY FUNCTIONS                                                          */
/* Helper functions used throughout the application                           */
/* ========================================================================== */

/**
 * Format currency with locale support
 */
function formatCurrency(amount, currency = 'USD') {
    // ... implementation
}

/**
 * Sanitize HTML to prevent XSS
 */
function sanitizeHTML(dirty) {
    // ... implementation
}
```

---

### 11. **Deprecated/Legacy комментарии**

```javascript
/**
 * @deprecated Since version 2.0. Use newMethod() instead.
 * This will be removed in version 3.0
 * 
 * Old method that doesn't handle edge cases properly.
 * Kept for backward compatibility.
 * 
 * @see {@link newMethod}
 */
function oldMethod() {
    console.warn('oldMethod is deprecated, use newMethod instead');
    // ... legacy implementation
}

/**
 * Modern implementation with proper error handling
 * 
 * @since 2.0
 */
function newMethod() {
    // ... new implementation
}

// LEGACY: Support for IE11
// Can be removed once we drop IE11 support (planned Q2 2024)
if (!Array.prototype.includes) {
    Array.prototype.includes = function(searchElement) {
        return this.indexOf(searchElement) !== -1;
    };
}
```

---

### 12. **Security комментарии**

```javascript
/**
 * Validate user input before processing
 * 
 * SECURITY: Never trust user input
 * - Sanitize HTML to prevent XSS
 * - Validate against whitelist, not blacklist
 * - Escape special characters
 * 
 * @param {string} userInput - Raw user input
 * @returns {string} Sanitized safe input
 */
function sanitizeInput(userInput) {
    // Remove all HTML tags
    const withoutTags = userInput.replace(/<[^>]*>/g, '');
    
    // Escape special characters
    const escaped = withoutTags
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    
    return escaped;
}

// SECURITY: API token must never be exposed in client code
// Load from environment variable or secure config
const API_TOKEN = process.env.API_TOKEN;

// SECURITY: Use HTTPS in production
// HTTP is acceptable only in local development
const API_URL = process.env.NODE_ENV === 'production'
    ? 'https://api.example.com'
    : 'http://localhost:3000';

// SECURITY: Rate limiting to prevent abuse
// Allow max 5 requests per second per user
const rateLimiter = new RateLimiter({
    maxRequests: 5,
    windowMs: 1000
});
```

---

### 13. **Performance Comments**

```javascript
/**
 * Lazy load images as they enter viewport
 * 
 * PERFORMANCE: Reduces initial page load time
 * - Only loads images when needed
 * - Uses IntersectionObserver (efficient)
 * - Falls back to eager loading if not supported
 */
function lazyLoadImages() {
    // Check if IntersectionObserver is supported
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Swap data-src to src (triggers load)
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    
                    // Stop observing this image
                    imageObserver.unobserve(img);
                }
            });
        });
        
        // Observe all lazy images
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback: Load all images immediately
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// PERFORMANCE: Virtualize long lists
// Only render visible items + buffer
// Dramatically reduces DOM nodes for 1000+ items
class VirtualList {
    constructor(items, itemHeight, containerHeight) {
        this.items = items;
        this.itemHeight = itemHeight;
        this.containerHeight = containerHeight;
        
        // Calculate visible range
        this.visibleCount = Math.ceil(containerHeight / itemHeight);
        this.bufferSize = 5; // Extra items above/below for smooth scrolling
        
        this.render();
    }
    
    // ... implementation
}
```

---

### 14. **Browser Compatibility Comments**

```javascript
/**
 * Feature detection for modern JavaScript features
 * 
 * COMPATIBILITY: Check before using to prevent errors
 * - Optional chaining: Chrome 80+, Firefox 74+, Safari 13.1+
 * - Nullish coalescing: Chrome 80+, Firefox 72+, Safari 13.1+
 * - BigInt: Chrome 67+, Firefox 68+, Safari 14+
 */

// Safe optional chaining with fallback
const userName = user?.profile?.name ?? 'Guest';

// Polyfill for older browsers
if (!('replaceAll' in String.prototype)) {
    String.prototype.replaceAll = function(search, replace) {
        return this.split(search).join(replace);
    };
}

// Use feature detection, not browser detection
const supportsWebP = () => {
    const canvas = document.createElement('canvas');
    
    if (canvas.getContext && canvas.getContext('2d')) {
        // WebP check
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }
    
    return false;
};

// COMPATIBILITY: Safari requires webkit prefix
const requestAnimationFrame = 
    window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    function(callback) { setTimeout(callback, 16); }; // Fallback: ~60fps
```

---

### 15. **Config/Constants Comments**

```javascript
/* ========================================================================== */
/* CONFIGURATION                                                              */
/* Application-wide settings and constants                                    */
/* ========================================================================== */

/**
 * API Configuration
 * 
 * @constant
 * @type {Object}
 */
const API_CONFIG = {
    /** Base URL for all API requests */
    BASE_URL: process.env.API_URL || 'https://api.example.com',
    
    /** API version (used in headers) */
    VERSION: 'v1',
    
    /** Request timeout in milliseconds */
    TIMEOUT: 30000, // 30 seconds
    
    /** Number of retry attempts for failed requests */
    MAX_RETRIES: 3,
    
    /** Delay between retries in milliseconds */
    RETRY_DELAY: 1000 // 1 second
};

/**
 * Application Constants
 * 
 * @constant
 */
const CONSTANTS = {
    /** Maximum file upload size in bytes (10MB) */
    MAX_FILE_SIZE: 10 * 1024 * 1024,
    
    /** Allowed file types for upload */
    ALLOWED_FILE_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'],
    
    /** Pagination default page size */
    PAGE_SIZE: 20,
    
    /** Local storage key prefix */
    STORAGE_PREFIX: 'app_',
    
    /** Session timeout in milliseconds (30 minutes) */
    SESSION_TIMEOUT: 30 * 60 * 1000
};

/**
 * Feature Flags
 * 
 * Control which features are enabled/disabled
 * Can be toggled remotely or per environment
 * 
 * @constant
 */
const FEATURES = {
    /** Enable new UI redesign */
    NEW_UI: true,
    
    /** Enable experimental search algorithm */
    EXPERIMENTAL_SEARCH: false,
    
    /** Enable analytics tracking */
    ANALYTICS: process.env.NODE_ENV === 'production',
    
    /** Enable debug mode */
    DEBUG: process.env.NODE_ENV === 'development'
};
```

---

## 🎯 JAVASCRIPT COMMENTS: BEST PRACTICES

### ✅ DO:

1. **Use JSDoc** for functions, classes, methods
2. **Explain "WHY"**, not "WHAT" - code should be self-documenting
3. **Document complex logic** - algorithms, edge cases
4. **Specify parameter types** - helps IDE and developers
5. **Add usage examples** (@example in JSDoc)
6. **Comment workarounds** - explain why hack is needed
7. **Mark TODO/FIXME** - with priority and responsible person
8. **Document side effects** - functions with side effects
9. **Specify complexity** - O(n), O(log n) for algorithms
10. **Warn about security** - XSS, injection, validation

### ❌ DON'T:

1. **Don't comment obvious code**
   ```javascript
   // BAD
   let i = 0; // Initialize counter
   i++; // Increment counter
   
   // GOOD
   let attemptCount = 0;
   attemptCount++; // Retry on failure
   ```

2. **Don't leave commented-out code** - use Git
   ```javascript
   // BAD
   // function oldImplementation() {
   //     return something;
   // }
   
   function newImplementation() {
       return somethingBetter;
   }
   ```

3. **Don't write novels** - comments should be concise
   ```javascript
   // BAD
   /**
    * This function takes a user object and processes it
    * by first checking if the user exists, then it validates
    * the user data, and after that it saves the user to the
    * database, and finally it returns the saved user object
    * back to the caller who can then use it for whatever
    * they need to do with it...
    */
   
   // GOOD
   /**
    * Validate and save user to database
    * @param {Object} user - User data to save
    * @returns {Object} Saved user object
    */
   ```

4. **Don't forget to update** - outdated comments are worse than none

5. **Don't duplicate code** in comments
   ```javascript
   // BAD
   function add(a, b) {
       return a + b; // Return sum of a and b
   }
   
   // GOOD
   function add(a, b) {
       return a + b; // Using + for numeric addition, not string concatenation
   }
   ```

---

## 📏 UNIVERSAL RULES

### 1. **Hierarchy of Importance**

```
1. Self-documenting code (best comment is no comment)
2. Meaningful names (variables, functions, classes)
3. Function/Method documentation (JSDoc, API description)
4. Inline comments (only for non-obvious logic)
5. TODO/FIXME (temporary notes)
```

### 2. **When to Comment**

✅ **COMMENT:**
- Complex algorithms
- Business logic and rules
- Workarounds and hacks
- Edge cases and special handling
- Public API and interfaces
- Security concerns
- Performance optimizations
- Browser compatibility issues

❌ **DON'T COMMENT:**
- Obvious code
- What code does (should be clear from code)
- Temporary TODOs (create a ticket)
- Commented-out code (delete it)

### 3. **Comment Language**

- **Use English** for open source and international teams
- **Use native language** for local projects (if team agrees)
- **Be consistent** - choose one language and stick to it

### 4. **Writing Style**

```javascript
// CORRECT: Sentences start with capital letter, end with period
// This function handles user authentication and returns a token.

// INCORRECT: lowercase, no punctuation
// this function handles user authentication and returns a token

// CORRECT: Brief comments without period
// Handle authentication

// CORRECT: Multi-line with proper punctuation
/**
 * This is a longer explanation that spans multiple lines.
 * Each sentence is properly capitalized and punctuated.
 * The closing delimiter is on its own line.
 */
```

---

## 🎓 FINAL CHECKLIST FOR QUALITY CODE

### HTML
- [ ] Main sections documented
- [ ] Complex components have explanations
- [ ] Responsive behavior described
- [ ] Accessibility attributes commented
- [ ] Closing tags of large blocks marked
- [ ] TODO/FIXME added where necessary

### CSS
- [ ] Table of Contents for large files
- [ ] CSS variables documented
- [ ] Complex selectors explained
- [ ] Magic numbers commented
- [ ] Browser hacks have explanations
- [ ] Z-index system described
- [ ] Media queries contain breakpoint notes
- [ ] Animations have performance notes

### JavaScript
- [ ] JSDoc for all public functions/methods/classes
- [ ] Parameters and return types specified
- [ ] Complex algorithms explained
- [ ] Edge cases documented
- [ ] Security concerns noted
- [ ] Performance optimizations described
- [ ] Browser compatibility indicated
- [ ] TODO/FIXME with priorities

**Remember**: Good code explains itself, comments explain the context! 🚀
