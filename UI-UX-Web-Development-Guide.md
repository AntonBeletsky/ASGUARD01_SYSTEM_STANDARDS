# Complete UI/UX Guide for Modern Web Development

## Table of Contents

1. [Introduction](#introduction)
2. [Fundamental Principles](#fundamental-principles)
3. [Responsive Design](#responsive-design)
4. [Layout & Grid Systems](#layout--grid-systems)
5. [Typography](#typography)
6. [Color Theory & Accessibility](#color-theory--accessibility)
7. [Navigation & Information Architecture](#navigation--information-architecture)
8. [Forms & User Input](#forms--user-input)
9. [Buttons & Interactive Elements](#buttons--interactive-elements)
10. [Images & Media](#images--media)
11. [Performance & Loading States](#performance--loading-states)
12. [Accessibility (WCAG)](#accessibility-wcag)
13. [Mobile-First Design](#mobile-first-design)
14. [Touch & Gesture Interactions](#touch--gesture-interactions)
15. [Micro-interactions & Animations](#micro-interactions--animations)
16. [Design Systems & Component Libraries](#design-systems--component-libraries)
17. [Testing & User Research](#testing--user-research)
18. [SEO Considerations](#seo-considerations)
19. [Common Patterns & Best Practices](#common-patterns--best-practices)
20. [Tools & Resources](#tools--resources)

---

## Introduction

This guide provides comprehensive standards for creating modern, accessible, and user-friendly web applications that work seamlessly across all devices—desktop, tablet, and mobile.

### Key Objectives
- **Usability**: Easy to learn and efficient to use
- **Accessibility**: Inclusive for all users, including those with disabilities
- **Performance**: Fast loading and smooth interactions
- **Responsiveness**: Adapts to any screen size
- **Consistency**: Predictable and coherent experience

---

## Fundamental Principles

### 1. User-Centered Design
- Always design with real user needs in mind
- Conduct user research and testing
- Create user personas and journey maps
- Prioritize content based on user goals

### 2. Consistency
- Maintain visual consistency (colors, typography, spacing)
- Use consistent interaction patterns
- Follow platform conventions (iOS, Android, Web)
- Create and follow a design system

### 3. Feedback & Communication
- Provide immediate feedback for user actions
- Show system status clearly
- Use appropriate error messages
- Confirm destructive actions

### 4. Simplicity
- Remove unnecessary elements
- Focus on core functionality
- Use progressive disclosure
- Avoid cognitive overload

### 5. Hierarchy & Emphasis
- Establish clear visual hierarchy
- Guide user attention strategically
- Use size, color, and spacing to create emphasis
- Prioritize primary actions

---

## Responsive Design

### Breakpoint Standards

```css
/* Mobile First Approach */
/* Extra Small Devices (Phones, 0-576px) */
@media (min-width: 576px) { /* Small devices (Landscape phones, 576px+) */ }
@media (min-width: 768px) { /* Medium devices (Tablets, 768px+) */ }
@media (min-width: 992px) { /* Large devices (Desktops, 992px+) */ }
@media (min-width: 1200px) { /* Extra large devices (Large desktops, 1200px+) */ }
@media (min-width: 1400px) { /* XXL devices (Larger desktops, 1400px+) */ }
```

### Viewport Meta Tag
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

### Responsive Images
```html
<!-- Responsive Image with srcset -->
<img 
  src="image-800.jpg" 
  srcset="image-400.jpg 400w, 
          image-800.jpg 800w, 
          image-1200.jpg 1200w"
  sizes="(max-width: 600px) 100vw, 
         (max-width: 1200px) 50vw, 
         800px"
  alt="Descriptive text"
  loading="lazy"
>

<!-- Picture element for art direction -->
<picture>
  <source media="(min-width: 768px)" srcset="desktop-image.jpg">
  <source media="(min-width: 576px)" srcset="tablet-image.jpg">
  <img src="mobile-image.jpg" alt="Descriptive text">
</picture>
```

### Fluid Typography
```css
/* Using clamp() for responsive font sizes */
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}

p {
  font-size: clamp(1rem, 2vw, 1.125rem);
}

/* Alternative: calc() method */
body {
  font-size: calc(16px + 0.5vw);
}
```

### Container Queries (Modern Approach)
```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}
```

---

## Layout & Grid Systems

### CSS Grid Layout
```css
/* Basic Grid */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

/* Named Grid Areas */
.layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-columns: 250px 1fr 1fr;
  gap: 1rem;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

### Flexbox Patterns
```css
/* Centering */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Equal Height Columns */
.flex-container {
  display: flex;
  gap: 1rem;
}

.flex-item {
  flex: 1;
}

/* Responsive Flex */
.responsive-flex {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.responsive-flex > * {
  flex: 1 1 300px; /* grow, shrink, basis */
}
```

### Spacing System
```css
/* 8pt Grid System */
:root {
  --space-xs: 0.25rem;  /* 4px */
  --space-sm: 0.5rem;   /* 8px */
  --space-md: 1rem;     /* 16px */
  --space-lg: 1.5rem;   /* 24px */
  --space-xl: 2rem;     /* 32px */
  --space-2xl: 3rem;    /* 48px */
  --space-3xl: 4rem;    /* 64px */
}
```

### Safe Areas (Mobile Notch Support)
```css
.header {
  padding-top: env(safe-area-inset-top);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

.footer {
  padding-bottom: env(safe-area-inset-bottom);
}
```

---

## Typography

### Font Stack
```css
:root {
  /* System Font Stack */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
               "Helvetica Neue", Arial, sans-serif;
  
  /* Monospace Stack */
  --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", 
               Consolas, monospace;
  
  /* Serif Stack */
  --font-serif: "Iowan Old Style", "Apple Garamond", Baskerville, 
                "Times New Roman", serif;
}

body {
  font-family: var(--font-sans);
}
```

### Type Scale
```css
:root {
  /* Modular Scale (1.25 ratio) */
  --text-xs: 0.64rem;    /* 10.24px */
  --text-sm: 0.8rem;     /* 12.8px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.25rem;    /* 20px */
  --text-xl: 1.563rem;   /* 25px */
  --text-2xl: 1.953rem;  /* 31.25px */
  --text-3xl: 2.441rem;  /* 39px */
  --text-4xl: 3.052rem;  /* 48.83px */
}
```

### Line Height & Letter Spacing
```css
h1, h2, h3, h4, h5, h6 {
  line-height: 1.2;
  letter-spacing: -0.02em; /* Tighter for headings */
}

p {
  line-height: 1.6;
  letter-spacing: 0;
}

.small-text {
  line-height: 1.5;
  letter-spacing: 0.01em;
}
```

### Responsive Typography
```css
html {
  font-size: 16px;
}

@media (min-width: 768px) {
  html {
    font-size: 18px;
  }
}

@media (min-width: 1200px) {
  html {
    font-size: 20px;
  }
}

/* Or use fluid typography */
html {
  font-size: clamp(16px, 1vw + 14px, 20px);
}
```

### Text Readability
```css
.readable-text {
  max-width: 65ch; /* Optimal line length */
  text-align: left;
  hyphens: auto;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* Prevent orphans */
p {
  text-wrap: pretty; /* Modern browsers */
}
```

---

## Color Theory & Accessibility

### Color System
```css
:root {
  /* Primary Colors */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-200: #bfdbfe;
  --color-primary-300: #93c5fd;
  --color-primary-400: #60a5fa;
  --color-primary-500: #3b82f6; /* Base */
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;
  --color-primary-800: #1e40af;
  --color-primary-900: #1e3a8a;
  
  /* Semantic Colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
  
  /* Neutral Colors */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
}
```

### Dark Mode Support
```css
:root {
  --bg-primary: #ffffff;
  --text-primary: #111827;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #111827;
    --text-primary: #f9fafb;
  }
}

/* Manual toggle support */
[data-theme="dark"] {
  --bg-primary: #111827;
  --text-primary: #f9fafb;
}
```

### Contrast Ratios (WCAG Standards)
```
Normal Text:
- AA: 4.5:1 minimum
- AAA: 7:1 minimum

Large Text (18pt+ or 14pt+ bold):
- AA: 3:1 minimum
- AAA: 4.5:1 minimum

UI Components & Graphics:
- AA: 3:1 minimum
```

### Color Usage Best Practices
- Never rely on color alone to convey information
- Use icons, labels, or patterns alongside color
- Test with color blindness simulators
- Ensure sufficient contrast for text and interactive elements
- Provide alternative text for images

---

## Navigation & Information Architecture

### Primary Navigation Patterns

#### Desktop Navigation
```html
<nav class="primary-nav" aria-label="Primary navigation">
  <div class="nav-container">
    <a href="/" class="logo">Brand</a>
    <ul class="nav-menu">
      <li><a href="/products">Products</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
    <button class="menu-toggle" aria-label="Toggle menu" aria-expanded="false">
      <span class="hamburger"></span>
    </button>
  </div>
</nav>
```

```css
.primary-nav {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-menu {
  display: flex;
  gap: 2rem;
  list-style: none;
}

.menu-toggle {
  display: none;
}

@media (max-width: 768px) {
  .nav-menu {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    background: white;
    flex-direction: column;
    padding: 2rem;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .nav-menu.active {
    transform: translateX(0);
  }
  
  .menu-toggle {
    display: block;
  }
}
```

### Breadcrumbs
```html
<nav aria-label="Breadcrumb">
  <ol class="breadcrumb">
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Product Name</li>
  </ol>
</nav>
```

```css
.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  list-style: none;
  padding: 1rem 0;
}

.breadcrumb li:not(:last-child)::after {
  content: "/";
  margin-left: 0.5rem;
  color: #6b7280;
}

.breadcrumb a {
  color: #3b82f6;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.breadcrumb [aria-current="page"] {
  color: #6b7280;
  font-weight: 500;
}
```

### Mobile Navigation Best Practices
- Use hamburger menu for compact navigation
- Keep navigation items visible and accessible
- Implement smooth transitions
- Close menu when clicking outside
- Support swipe gestures
- Use bottom navigation for primary actions on mobile

### Tab Navigation
```html
<div class="tabs" role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
    Tab 1
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">
    Tab 2
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Content 1
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Content 2
</div>
```

---

## Forms & User Input

### Form Structure
```html
<form class="form" novalidate>
  <div class="form-group">
    <label for="email" class="form-label">
      Email Address
      <span class="required" aria-label="required">*</span>
    </label>
    <input 
      type="email" 
      id="email" 
      name="email"
      class="form-input"
      aria-required="true"
      aria-describedby="email-hint email-error"
      autocomplete="email"
    >
    <div id="email-hint" class="form-hint">
      We'll never share your email
    </div>
    <div id="email-error" class="form-error" role="alert" hidden>
      Please enter a valid email address
    </div>
  </div>
  
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Form Styling
```css
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.required {
  color: #ef4444;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid #d1d5db;
  border-radius: 0.375rem;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:invalid:not(:placeholder-shown) {
  border-color: #ef4444;
}

.form-input:valid:not(:placeholder-shown) {
  border-color: #10b981;
}

.form-hint {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.form-error {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #ef4444;
}
```

### Input Types & Validation
```html
<!-- Email -->
<input type="email" required pattern="[^@\s]+@[^@\s]+\.[^@\s]+">

<!-- Phone -->
<input type="tel" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" 
       placeholder="123-456-7890">

<!-- Number -->
<input type="number" min="0" max="100" step="1">

<!-- Date -->
<input type="date" min="2024-01-01" max="2024-12-31">

<!-- URL -->
<input type="url" pattern="https?://.+">

<!-- Password with requirements -->
<input type="password" 
       minlength="8" 
       pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
       title="Must contain at least one number, one uppercase and lowercase letter, and at least 8 characters">
```

### Autocomplete Attributes
```html
<input type="text" autocomplete="given-name">
<input type="text" autocomplete="family-name">
<input type="email" autocomplete="email">
<input type="tel" autocomplete="tel">
<input type="text" autocomplete="street-address">
<input type="text" autocomplete="postal-code">
<input type="text" autocomplete="country">
<input type="text" autocomplete="cc-number">
<input type="text" autocomplete="cc-exp">
```

### Form Validation Best Practices
- Validate on blur, not on every keystroke
- Show success states, not just errors
- Use inline validation for immediate feedback
- Display helpful error messages
- Don't disable submit button (show errors instead)
- Group related errors at the top
- Use aria-invalid and aria-describedby
- Support keyboard navigation

### Checkbox & Radio Groups
```html
<fieldset class="form-group">
  <legend>Choose your preferences</legend>
  
  <div class="checkbox-group">
    <input type="checkbox" id="option1" name="options" value="1">
    <label for="option1">Option 1</label>
  </div>
  
  <div class="checkbox-group">
    <input type="checkbox" id="option2" name="options" value="2">
    <label for="option2">Option 2</label>
  </div>
</fieldset>

<fieldset class="form-group">
  <legend>Choose one option</legend>
  
  <div class="radio-group">
    <input type="radio" id="choice1" name="choice" value="1">
    <label for="choice1">Choice 1</label>
  </div>
  
  <div class="radio-group">
    <input type="radio" id="choice2" name="choice" value="2">
    <label for="choice2">Choice 2</label>
  </div>
</fieldset>
```

---

## Buttons & Interactive Elements

### Button Styles
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  white-space: nowrap;
}

.btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* Primary Button */
.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-primary:active {
  background: #1d4ed8;
  transform: scale(0.98);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.btn-secondary:hover {
  background: #eff6ff;
}

/* Ghost Button */
.btn-ghost {
  background: transparent;
  color: #374151;
}

.btn-ghost:hover {
  background: #f3f4f6;
}

/* Danger Button */
.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
}

/* Button Sizes */
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1.125rem;
}

/* Icon Buttons */
.btn-icon {
  padding: 0.75rem;
  width: 2.75rem;
  height: 2.75rem;
}
```

### Touch Targets (Mobile)
```css
/* Minimum 44x44px touch target */
.touch-target {
  min-height: 44px;
  min-width: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Add invisible padding for small elements */
.small-icon {
  padding: 12px; /* Extends touch area */
  margin: -12px; /* Compensates for layout */
}
```

### Link Styles
```css
a {
  color: #3b82f6;
  text-decoration: underline;
  text-decoration-skip-ink: auto;
  transition: color 0.2s ease;
}

a:hover {
  color: #2563eb;
}

a:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
  border-radius: 2px;
}

a:visited {
  color: #7c3aed;
}

/* Remove underline for navigation links */
.nav-link {
  text-decoration: none;
}

.nav-link:hover {
  text-decoration: underline;
}
```

### Loading States
```html
<button class="btn btn-primary" disabled>
  <span class="spinner"></span>
  <span>Loading...</span>
</button>
```

```css
.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

---

## Images & Media

### Responsive Images
```html
<!-- Modern responsive image -->
<img 
  src="image.jpg"
  srcset="image-400.jpg 400w,
          image-800.jpg 800w,
          image-1200.jpg 1200w"
  sizes="(max-width: 400px) 100vw,
         (max-width: 800px) 50vw,
         800px"
  alt="Descriptive alternative text"
  width="800"
  height="600"
  loading="lazy"
  decoding="async"
>
```

### Image Optimization
```css
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Aspect ratio boxes */
.img-container {
  position: relative;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.img-container img {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
```

### WebP with Fallback
```html
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="Description">
</picture>
```

### Video Best Practices
```html
<video 
  controls
  preload="metadata"
  poster="thumbnail.jpg"
  width="1280"
  height="720"
>
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  <track 
    kind="subtitles" 
    src="subtitles-en.vtt" 
    srclang="en" 
    label="English"
  >
  Your browser doesn't support HTML5 video.
</video>
```

```css
video {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Maintain aspect ratio */
.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  height: 0;
  overflow: hidden;
}

.video-container iframe,
.video-container video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

### SVG Icons
```html
<!-- Inline SVG -->
<svg class="icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
</svg>

<!-- SVG as img -->
<img src="icon.svg" alt="Icon description" class="icon">

<!-- SVG sprite -->
<svg class="icon">
  <use href="icons.svg#icon-name"></use>
</svg>
```

```css
.icon {
  width: 1.5rem;
  height: 1.5rem;
  fill: currentColor;
  display: inline-block;
  vertical-align: middle;
}
```

---

## Performance & Loading States

### Critical CSS
```html
<!-- Inline critical CSS -->
<style>
  /* Critical above-the-fold styles */
  body { margin: 0; font-family: system-ui; }
  .header { background: #fff; padding: 1rem; }
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="styles.css"></noscript>
```

### Lazy Loading
```html
<!-- Images -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- Iframes -->
<iframe src="embed.html" loading="lazy"></iframe>
```

```javascript
// JavaScript lazy loading with Intersection Observer
const images = document.querySelectorAll('img[data-src]');

const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      observer.unobserve(img);
    }
  });
});

images.forEach(img => imageObserver.observe(img));
```

### Loading Skeletons
```html
<div class="skeleton-card">
  <div class="skeleton skeleton-image"></div>
  <div class="skeleton skeleton-title"></div>
  <div class="skeleton skeleton-text"></div>
  <div class="skeleton skeleton-text"></div>
</div>
```

```css
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-image {
  width: 100%;
  height: 200px;
  margin-bottom: 1rem;
}

.skeleton-title {
  width: 70%;
  height: 1.5rem;
  margin-bottom: 0.5rem;
}

.skeleton-text {
  width: 100%;
  height: 1rem;
  margin-bottom: 0.5rem;
}
```

### Progress Indicators
```html
<!-- Determinate progress bar -->
<div class="progress" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 75%"></div>
</div>

<!-- Indeterminate spinner -->
<div class="spinner" role="status" aria-label="Loading">
  <span class="sr-only">Loading...</span>
</div>
```

### Resource Hints
```html
<!-- DNS Prefetch -->
<link rel="dns-prefetch" href="https://fonts.googleapis.com">

<!-- Preconnect -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Prefetch -->
<link rel="prefetch" href="/next-page.html">

<!-- Preload -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="hero.jpg" as="image">
```

---

## Accessibility (WCAG)

### Semantic HTML
```html
<!-- Use semantic elements -->
<header>
  <nav aria-label="Primary navigation">
    <!-- navigation content -->
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <!-- content -->
  </article>
  
  <aside aria-label="Related content">
    <!-- sidebar content -->
  </aside>
</main>

<footer>
  <!-- footer content -->
</footer>
```

### ARIA Landmarks & Labels
```html
<!-- Landmarks -->
<nav aria-label="Main navigation"></nav>
<nav aria-label="Secondary navigation"></nav>
<main></main>
<aside aria-label="Sidebar"></aside>
<footer></footer>

<!-- Labels -->
<button aria-label="Close dialog">×</button>
<input type="search" aria-label="Search products">

<!-- Descriptions -->
<button aria-describedby="delete-warning">Delete</button>
<p id="delete-warning">This action cannot be undone</p>

<!-- Live regions -->
<div aria-live="polite" aria-atomic="true">
  <!-- Dynamic content updates -->
</div>
```

### Keyboard Navigation
```css
/* Focus indicators */
:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Remove default outline only if providing custom focus style */
:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}
```

```javascript
// Trap focus in modal
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'a[href], button:not([disabled]), textarea, input, select'
  );
  
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];
  
  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      } else if (!e.shiftKey && document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }
  });
  
  firstFocusable.focus();
}
```

### Screen Reader Support
```html
<!-- Hide decorative content -->
<img src="decorative.jpg" alt="" role="presentation">

<!-- Visually hidden but available to screen readers -->
<span class="sr-only">Additional context</span>

<!-- Skip links -->
<a href="#main-content" class="skip-link">Skip to main content</a>
```

```css
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

.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: white;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### WCAG 2.1 Level AA Checklist

**Perceivable:**
- [ ] Text alternatives for images
- [ ] Captions for videos
- [ ] Sufficient color contrast (4.5:1 for text, 3:1 for UI)
- [ ] Resizable text up to 200%
- [ ] No information conveyed by color alone

**Operable:**
- [ ] Keyboard accessible
- [ ] No keyboard traps
- [ ] Skip navigation links
- [ ] Page titles descriptive
- [ ] Focus order logical
- [ ] Link purpose clear
- [ ] Multiple ways to navigate
- [ ] Focus visible

**Understandable:**
- [ ] Language of page identified
- [ ] Consistent navigation
- [ ] Consistent identification
- [ ] Error identification
- [ ] Labels and instructions
- [ ] Error suggestions

**Robust:**
- [ ] Valid HTML
- [ ] Name, role, value for UI components
- [ ] Status messages announced

---

## Mobile-First Design

### Mobile-First CSS Approach
```css
/* Base styles (mobile) */
.container {
  width: 100%;
  padding: 1rem;
}

.grid {
  display: grid;
  gap: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
  
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Mobile Navigation Patterns

#### Bottom Navigation (Mobile App Pattern)
```html
<nav class="bottom-nav" role="navigation">
  <a href="/" class="nav-item active">
    <svg class="icon"><!-- Home icon --></svg>
    <span>Home</span>
  </a>
  <a href="/search" class="nav-item">
    <svg class="icon"><!-- Search icon --></svg>
    <span>Search</span>
  </a>
  <a href="/profile" class="nav-item">
    <svg class="icon"><!-- Profile icon --></svg>
    <span>Profile</span>
  </a>
</nav>
```

```css
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  background: white;
  border-top: 1px solid #e5e7eb;
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 1000;
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.75rem;
}

.nav-item.active {
  color: #3b82f6;
}

.nav-item .icon {
  width: 1.5rem;
  height: 1.5rem;
  margin-bottom: 0.25rem;
}

@media (min-width: 768px) {
  .bottom-nav {
    display: none; /* Hide on desktop */
  }
}
```

### Mobile Input Optimization
```html
<!-- Numeric keyboard -->
<input type="tel" inputmode="numeric" pattern="[0-9]*">

<!-- Email keyboard -->
<input type="email" inputmode="email">

<!-- URL keyboard -->
<input type="url" inputmode="url">

<!-- Decimal keyboard -->
<input type="number" inputmode="decimal">

<!-- Search keyboard -->
<input type="search" inputmode="search">

<!-- Prevent zoom on input focus (use with caution) -->
<input type="text" style="font-size: 16px;">
```

### Mobile Viewport Units
```css
/* Use dvh (dynamic viewport height) for mobile browsers */
.hero {
  height: 100dvh; /* Accounts for address bar */
  min-height: -webkit-fill-available; /* Safari fallback */
}

/* Fallback for older browsers */
@supports not (height: 100dvh) {
  .hero {
    height: 100vh;
  }
}
```

---

## Touch & Gesture Interactions

### Touch Target Sizing
```css
/* Minimum recommended touch target: 44x44px (Apple) or 48x48dp (Android) */
.touch-button {
  min-height: 48px;
  min-width: 48px;
  padding: 12px 16px;
}

/* Ensure adequate spacing between targets */
.touch-menu {
  display: flex;
  gap: 8px; /* Minimum 8px between targets */
}
```

### Touch Feedback
```css
.touchable {
  position: relative;
  overflow: hidden;
  -webkit-tap-highlight-color: transparent;
}

/* Ripple effect */
.touchable::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.touchable:active::after {
  width: 300px;
  height: 300px;
}

/* Active state */
.button:active {
  transform: scale(0.98);
  opacity: 0.8;
}
```

### Swipe Gestures (JavaScript)
```javascript
class SwipeDetector {
  constructor(element, options = {}) {
    this.element = element;
    this.threshold = options.threshold || 50;
    this.startX = 0;
    this.startY = 0;
    
    this.element.addEventListener('touchstart', this.handleTouchStart.bind(this));
    this.element.addEventListener('touchmove', this.handleTouchMove.bind(this));
    this.element.addEventListener('touchend', this.handleTouchEnd.bind(this));
  }
  
  handleTouchStart(e) {
    this.startX = e.touches[0].clientX;
    this.startY = e.touches[0].clientY;
  }
  
  handleTouchMove(e) {
    if (!this.startX || !this.startY) return;
    
    const deltaX = e.touches[0].clientX - this.startX;
    const deltaY = e.touches[0].clientY - this.startY;
    
    // Prevent scrolling if swiping horizontally
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      e.preventDefault();
    }
  }
  
  handleTouchEnd(e) {
    const endX = e.changedTouches[0].clientX;
    const endY = e.changedTouches[0].clientY;
    
    const deltaX = endX - this.startX;
    const deltaY = endY - this.startY;
    
    if (Math.abs(deltaX) > this.threshold) {
      if (deltaX > 0) {
        this.onSwipeRight();
      } else {
        this.onSwipeLeft();
      }
    }
    
    if (Math.abs(deltaY) > this.threshold) {
      if (deltaY > 0) {
        this.onSwipeDown();
      } else {
        this.onSwipeUp();
      }
    }
    
    this.startX = 0;
    this.startY = 0;
  }
  
  onSwipeLeft() { console.log('Swiped left'); }
  onSwipeRight() { console.log('Swiped right'); }
  onSwipeUp() { console.log('Swiped up'); }
  onSwipeDown() { console.log('Swiped down'); }
}

// Usage
const swipe = new SwipeDetector(document.querySelector('.swipeable'));
swipe.onSwipeLeft = () => {
  // Handle swipe left
};
```

### Pull to Refresh
```javascript
class PullToRefresh {
  constructor(element, onRefresh) {
    this.element = element;
    this.onRefresh = onRefresh;
    this.startY = 0;
    this.currentY = 0;
    this.threshold = 80;
    
    this.element.addEventListener('touchstart', this.handleTouchStart.bind(this));
    this.element.addEventListener('touchmove', this.handleTouchMove.bind(this));
    this.element.addEventListener('touchend', this.handleTouchEnd.bind(this));
  }
  
  handleTouchStart(e) {
    if (this.element.scrollTop === 0) {
      this.startY = e.touches[0].clientY;
    }
  }
  
  handleTouchMove(e) {
    if (this.startY === 0) return;
    
    this.currentY = e.touches[0].clientY;
    const pullDistance = this.currentY - this.startY;
    
    if (pullDistance > 0) {
      e.preventDefault();
      // Update UI to show pull indicator
      this.updatePullIndicator(pullDistance);
    }
  }
  
  handleTouchEnd(e) {
    const pullDistance = this.currentY - this.startY;
    
    if (pullDistance > this.threshold) {
      this.onRefresh();
    }
    
    this.startY = 0;
    this.currentY = 0;
    this.resetPullIndicator();
  }
  
  updatePullIndicator(distance) {
    // Implementation for visual feedback
  }
  
  resetPullIndicator() {
    // Reset visual feedback
  }
}
```

### Prevent Scroll Chaining
```css
/* Prevent overscroll from propagating to parent */
.scrollable-content {
  overscroll-behavior: contain;
}

/* Prevent pull-to-refresh and overscroll glow */
body {
  overscroll-behavior-y: none;
}
```

---

## Micro-interactions & Animations

### Animation Principles
```css
:root {
  /* Timing functions */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  
  /* Durations */
  --duration-instant: 100ms;
  --duration-fast: 200ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
}
```

### Hover Effects
```css
.card {
  transition: transform var(--duration-fast) var(--ease-out),
              box-shadow var(--duration-fast) var(--ease-out);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

/* Lift and scale */
.image-card {
  transition: transform var(--duration-normal) var(--ease-out);
}

.image-card:hover {
  transform: scale(1.05);
}

/* Underline animation */
.animated-link {
  position: relative;
  text-decoration: none;
}

.animated-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform var(--duration-normal) var(--ease-out);
}

.animated-link:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}
```

### Loading Animations
```css
/* Skeleton shimmer */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}

/* Pulse animation */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.loading-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Spinner */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

### Page Transitions
```css
/* Fade in */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.page-enter {
  animation: fadeIn var(--duration-normal) var(--ease-out);
}

/* Slide up */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-up {
  animation: slideUp var(--duration-normal) var(--ease-out);
}

/* Stagger children */
.stagger-container > * {
  opacity: 0;
  animation: slideUp var(--duration-normal) var(--ease-out) forwards;
}

.stagger-container > *:nth-child(1) { animation-delay: 0ms; }
.stagger-container > *:nth-child(2) { animation-delay: 100ms; }
.stagger-container > *:nth-child(3) { animation-delay: 200ms; }
.stagger-container > *:nth-child(4) { animation-delay: 300ms; }
```

### Scroll Animations
```javascript
// Intersection Observer for scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});
```

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.animate-on-scroll.animate-in {
  opacity: 1;
  transform: translateY(0);
}
```

### Reduced Motion Support
```css
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

## Design Systems & Component Libraries

### CSS Custom Properties (Design Tokens)
```css
:root {
  /* Colors */
  --color-primary: #3b82f6;
  --color-secondary: #8b5cf6;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  /* Spacing Scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  
  /* Typography */
  --font-sans: system-ui, sans-serif;
  --font-mono: monospace;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
  
  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  
  /* Z-index Scale */
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
}
```

### Component Architecture
```
components/
├── atoms/              # Basic building blocks
│   ├── Button/
│   ├── Input/
│   ├── Icon/
│   └── Badge/
├── molecules/          # Simple combinations
│   ├── FormField/
│   ├── SearchBar/
│   └── Card/
├── organisms/          # Complex components
│   ├── Header/
│   ├── Footer/
│   ├── Sidebar/
│   └── ProductCard/
└── templates/          # Page layouts
    ├── HomePage/
    ├── ProductPage/
    └── Dashboard/
```

### Utility Classes (Tailwind-inspired)
```css
/* Display */
.flex { display: flex; }
.grid { display: grid; }
.hidden { display: none; }
.block { display: block; }

/* Flexbox */
.flex-row { flex-direction: row; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.gap-4 { gap: var(--space-4); }

/* Spacing */
.m-0 { margin: 0; }
.m-4 { margin: var(--space-4); }
.mt-4 { margin-top: var(--space-4); }
.mb-4 { margin-bottom: var(--space-4); }
.p-4 { padding: var(--space-4); }
.px-4 { padding-left: var(--space-4); padding-right: var(--space-4); }
.py-4 { padding-top: var(--space-4); padding-bottom: var(--space-4); }

/* Typography */
.text-sm { font-size: var(--text-sm); }
.text-base { font-size: var(--text-base); }
.text-lg { font-size: var(--text-lg); }
.font-bold { font-weight: 700; }
.text-center { text-align: center; }

/* Colors */
.text-primary { color: var(--color-primary); }
.bg-primary { background-color: var(--color-primary); }
.border-primary { border-color: var(--color-primary); }

/* Width */
.w-full { width: 100%; }
.w-1\/2 { width: 50%; }
.w-1\/3 { width: 33.333%; }
.w-screen { width: 100vw; }
.max-w-screen-lg { max-width: 1024px; }

/* Rounded */
.rounded { border-radius: var(--radius-md); }
.rounded-lg { border-radius: var(--radius-lg); }
.rounded-full { border-radius: var(--radius-full); }

/* Shadow */
.shadow { box-shadow: var(--shadow-md); }
.shadow-lg { box-shadow: var(--shadow-lg); }
```

### Component Documentation Template
```markdown
# Button Component

## Description
Primary interactive element for user actions.

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' \| 'ghost' | 'primary' | Button style variant |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Button size |
| disabled | boolean | false | Disabled state |
| loading | boolean | false | Loading state |

## Usage
```html
<button class="btn btn-primary btn-md">
  Click me
</button>
```

## Accessibility
- Keyboard accessible (Enter/Space)
- Screen reader compatible
- ARIA attributes included
- Focus visible indicator

## Examples
[Visual examples with code]
```

---

## Testing & User Research

### Usability Testing Checklist
- [ ] Can users complete core tasks?
- [ ] Is navigation intuitive?
- [ ] Are error messages helpful?
- [ ] Is the interface responsive on all devices?
- [ ] Are loading states clear?
- [ ] Can users recover from errors?
- [ ] Is the flow logical?
- [ ] Are CTAs (Call-to-Actions) clear?

### A/B Testing Framework
```javascript
// Simple A/B test implementation
class ABTest {
  constructor(testName, variants) {
    this.testName = testName;
    this.variants = variants;
    this.variant = this.getVariant();
  }
  
  getVariant() {
    // Check if user already has a variant assigned
    const stored = localStorage.getItem(`ab_${this.testName}`);
    if (stored && this.variants.includes(stored)) {
      return stored;
    }
    
    // Assign random variant
    const variant = this.variants[Math.floor(Math.random() * this.variants.length)];
    localStorage.setItem(`ab_${this.testName}`, variant);
    return variant;
  }
  
  trackConversion(event) {
    // Send analytics event
    analytics.track('AB Test Conversion', {
      test: this.testName,
      variant: this.variant,
      event: event
    });
  }
}

// Usage
const buttonTest = new ABTest('checkout_button', ['green', 'blue']);
document.querySelector('.checkout-btn').classList.add(buttonTest.variant);
```

### Analytics Implementation
```javascript
// Track user interactions
function trackEvent(category, action, label) {
  // Google Analytics
  gtag('event', action, {
    'event_category': category,
    'event_label': label
  });
  
  // Custom analytics
  analytics.track(action, {
    category: category,
    label: label,
    timestamp: new Date().toISOString()
  });
}

// Track page views
function trackPageView(path) {
  gtag('config', 'GA_MEASUREMENT_ID', {
    'page_path': path
  });
}

// Track errors
window.addEventListener('error', (event) => {
  trackEvent('Error', 'JavaScript Error', event.message);
});

// Track performance
window.addEventListener('load', () => {
  const perfData = performance.timing;
  const loadTime = perfData.loadEventEnd - perfData.navigationStart;
  trackEvent('Performance', 'Page Load Time', loadTime);
});
```

### Heatmap & Session Recording
```javascript
// Implement click tracking
document.addEventListener('click', (e) => {
  const target = e.target;
  const rect = target.getBoundingClientRect();
  
  trackClick({
    x: e.clientX,
    y: e.clientY,
    element: target.tagName,
    class: target.className,
    id: target.id,
    text: target.textContent.substring(0, 50),
    timestamp: Date.now()
  });
});

function trackClick(data) {
  // Send to analytics service
  fetch('/api/analytics/click', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
}
```

---

## SEO Considerations

### HTML Meta Tags
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- Primary Meta Tags -->
  <title>Page Title - 50-60 characters</title>
  <meta name="title" content="Page Title">
  <meta name="description" content="Page description - 150-160 characters">
  <meta name="keywords" content="keyword1, keyword2, keyword3">
  <meta name="author" content="Author Name">
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://example.com/">
  <meta property="og:title" content="Page Title">
  <meta property="og:description" content="Page description">
  <meta property="og:image" content="https://example.com/image.jpg">
  
  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:url" content="https://example.com/">
  <meta property="twitter:title" content="Page Title">
  <meta property="twitter:description" content="Page description">
  <meta property="twitter:image" content="https://example.com/image.jpg">
  
  <!-- Canonical URL -->
  <link rel="canonical" href="https://example.com/page">
  
  <!-- Favicon -->
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  
  <!-- Robots -->
  <meta name="robots" content="index, follow">
</head>
```

### Structured Data (Schema.org)
```html
<!-- Article Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Headline",
  "image": "https://example.com/image.jpg",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.jpg"
    }
  },
  "datePublished": "2024-01-01",
  "dateModified": "2024-01-15"
}
</script>

<!-- Product Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": "https://example.com/product.jpg",
  "description": "Product description",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
</script>

<!-- Breadcrumb Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "Home",
    "item": "https://example.com"
  },{
    "@type": "ListItem",
    "position": 2,
    "name": "Products",
    "item": "https://example.com/products"
  },{
    "@type": "ListItem",
    "position": 3,
    "name": "Product Name",
    "item": "https://example.com/products/product-name"
  }]
}
</script>
```

### Semantic HTML for SEO
```html
<article>
  <header>
    <h1>Main Article Title</h1>
    <p class="meta">
      <time datetime="2024-01-01">January 1, 2024</time>
      by <span rel="author">Author Name</span>
    </p>
  </header>
  
  <section>
    <h2>Section Heading</h2>
    <p>Content...</p>
  </section>
  
  <footer>
    <p>Article footer information</p>
  </footer>
</article>
```

### Performance & Core Web Vitals
```html
<!-- Preload critical resources -->
<link rel="preload" href="critical.css" as="style">
<link rel="preload" href="hero-image.jpg" as="image">

<!-- Defer non-critical CSS -->
<link rel="stylesheet" href="non-critical.css" media="print" onload="this.media='all'">

<!-- Async scripts -->
<script src="analytics.js" async></script>

<!-- Lazy load images -->
<img src="image.jpg" loading="lazy" alt="Description">
```

---

## Common Patterns & Best Practices

### Modal/Dialog
```html
<div class="modal" role="dialog" aria-labelledby="modal-title" aria-modal="true">
  <div class="modal-overlay" aria-hidden="true"></div>
  <div class="modal-content">
    <header class="modal-header">
      <h2 id="modal-title">Modal Title</h2>
      <button class="modal-close" aria-label="Close dialog">×</button>
    </header>
    <div class="modal-body">
      <p>Modal content...</p>
    </div>
    <footer class="modal-footer">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-primary">Confirm</button>
    </footer>
  </div>
</div>
```

```css
.modal {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal);
  display: none;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal.active {
  display: flex;
}

.modal-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
}

.modal-content {
  position: relative;
  background: white;
  border-radius: var(--radius-lg);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
}
```

### Toast Notifications
```html
<div class="toast toast-success" role="alert">
  <div class="toast-icon">✓</div>
  <div class="toast-content">
    <strong>Success!</strong>
    <p>Operation completed successfully</p>
  </div>
  <button class="toast-close" aria-label="Close">×</button>
</div>
```

```css
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: white;
  padding: 1rem;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  max-width: 400px;
  animation: slideIn 0.3s ease;
  z-index: var(--z-tooltip);
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast-success {
  border-left: 4px solid var(--color-success);
}

.toast-error {
  border-left: 4px solid var(--color-error);
}

.toast-warning {
  border-left: 4px solid var(--color-warning);
}
```

### Dropdown Menu
```html
<div class="dropdown">
  <button class="dropdown-toggle" aria-haspopup="true" aria-expanded="false">
    Menu
  </button>
  <ul class="dropdown-menu" role="menu">
    <li role="menuitem"><a href="#">Option 1</a></li>
    <li role="menuitem"><a href="#">Option 2</a></li>
    <li role="separator"></li>
    <li role="menuitem"><a href="#">Option 3</a></li>
  </ul>
</div>
```

```css
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 200px;
  background: white;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  list-style: none;
  padding: 0.5rem 0;
  margin-top: 0.5rem;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
  z-index: var(--z-dropdown);
}

.dropdown.active .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu li[role="menuitem"] a {
  display: block;
  padding: 0.5rem 1rem;
  color: #374151;
  text-decoration: none;
}

.dropdown-menu li[role="menuitem"]:hover {
  background: #f3f4f6;
}

.dropdown-menu li[role="separator"] {
  height: 1px;
  background: #e5e7eb;
  margin: 0.5rem 0;
}
```

### Accordion
```html
<div class="accordion">
  <div class="accordion-item">
    <button class="accordion-header" aria-expanded="false" aria-controls="panel-1">
      <span>Accordion Item 1</span>
      <svg class="accordion-icon" aria-hidden="true"><!-- chevron --></svg>
    </button>
    <div id="panel-1" class="accordion-panel" hidden>
      <p>Panel content...</p>
    </div>
  </div>
</div>
```

```css
.accordion-item {
  border: 1px solid #e5e7eb;
  border-radius: var(--radius-md);
  margin-bottom: 0.5rem;
}

.accordion-header {
  width: 100%;
  padding: 1rem;
  background: transparent;
  border: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: 500;
}

.accordion-header:hover {
  background: #f9fafb;
}

.accordion-icon {
  transition: transform 0.3s ease;
}

.accordion-header[aria-expanded="true"] .accordion-icon {
  transform: rotate(180deg);
}

.accordion-panel {
  padding: 0 1rem 1rem;
}
```

### Infinite Scroll
```javascript
class InfiniteScroll {
  constructor(options) {
    this.container = options.container;
    this.loadMore = options.loadMore;
    this.threshold = options.threshold || 100;
    this.loading = false;
    this.page = 1;
    
    this.init();
  }
  
  init() {
    this.observer = new IntersectionObserver(
      (entries) => this.handleIntersection(entries),
      { rootMargin: `${this.threshold}px` }
    );
    
    this.sentinel = document.createElement('div');
    this.sentinel.className = 'infinite-scroll-sentinel';
    this.container.appendChild(this.sentinel);
    this.observer.observe(this.sentinel);
  }
  
  async handleIntersection(entries) {
    const entry = entries[0];
    
    if (entry.isIntersecting && !this.loading) {
      this.loading = true;
      this.showLoading();
      
      try {
        const hasMore = await this.loadMore(this.page);
        this.page++;
        
        if (!hasMore) {
          this.destroy();
        }
      } catch (error) {
        console.error('Error loading more items:', error);
      } finally {
        this.loading = false;
        this.hideLoading();
      }
    }
  }
  
  showLoading() {
    // Show loading indicator
  }
  
  hideLoading() {
    // Hide loading indicator
  }
  
  destroy() {
    this.observer.disconnect();
    this.sentinel.remove();
  }
}

// Usage
const scroll = new InfiniteScroll({
  container: document.querySelector('.items-container'),
  loadMore: async (page) => {
    const response = await fetch(`/api/items?page=${page}`);
    const data = await response.json();
    
    // Append items to container
    data.items.forEach(item => {
      // Add item to DOM
    });
    
    return data.hasMore;
  }
});
```

---

## Tools & Resources

### Design Tools
- **Figma** - UI/UX design and prototyping
- **Adobe XD** - Design and prototyping
- **Sketch** - Mac-only design tool
- **Framer** - Interactive prototyping
- **InVision** - Design collaboration

### Development Tools
- **Chrome DevTools** - Browser debugging
- **Firefox Developer Tools** - Browser debugging
- **Lighthouse** - Performance auditing
- **WebPageTest** - Performance testing
- **Axe DevTools** - Accessibility testing

### Testing Tools
- **BrowserStack** - Cross-browser testing
- **LambdaTest** - Cross-browser testing
- **Percy** - Visual regression testing
- **Cypress** - E2E testing
- **Playwright** - Browser automation

### Color & Accessibility Tools
- **Coolors** - Color palette generator
- **ColorBox** - Accessible color systems
- **WebAIM Contrast Checker** - WCAG compliance
- **Colorblindly** - Color blindness simulator
- **Stark** - Accessibility toolkit

### Performance Tools
- **GTmetrix** - Performance analysis
- **PageSpeed Insights** - Google's performance tool
- **Cloudflare** - CDN and performance
- **ImageOptim** - Image compression
- **TinyPNG** - PNG/JPG compression

### Icon & Asset Libraries
- **Heroicons** - Free SVG icons
- **Font Awesome** - Icon library
- **Lucide** - Icon library
- **Unsplash** - Free stock photos
- **Pexels** - Free stock photos

### Learning Resources
- **MDN Web Docs** - Comprehensive web documentation
- **Web.dev** - Google's web development guides
- **CSS-Tricks** - CSS tutorials and articles
- **Smashing Magazine** - Web design articles
- **A List Apart** - Web design and development

### Frameworks & Libraries
- **React** - JavaScript UI library
- **Vue.js** - Progressive JavaScript framework
- **Svelte** - Compiler-based framework
- **Tailwind CSS** - Utility-first CSS
- **Bootstrap** - CSS framework

---

## Conclusion

This guide covers the essential standards for modern web development with focus on UI/UX best practices. Key takeaways:

1. **Start with mobile-first** approach
2. **Prioritize accessibility** from the beginning
3. **Optimize for performance** at every step
4. **Test on real devices** regularly
5. **Follow established patterns** but adapt to your users
6. **Iterate based on feedback** and analytics
7. **Stay updated** with web standards and best practices

Remember: Great UI/UX is invisible—users shouldn't notice the design, they should just accomplish their goals effortlessly.

---

## Version History

- **v1.0.0** (2024) - Initial comprehensive guide
- Regular updates to reflect current web standards and best practices

## Contributing

This is a living document. Contributions, corrections, and suggestions are welcome.

## License

This guide is provided as-is for educational purposes.
