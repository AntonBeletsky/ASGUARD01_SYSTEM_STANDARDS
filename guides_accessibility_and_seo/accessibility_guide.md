# Complete Web Accessibility Guide for Frontend Developers

> **WCAG 2.2** · **ARIA 1.2** · **HTML · CSS · JavaScript**

---

## Table of Contents

1. [What is Accessibility and Why It Matters](#1-what-is-accessibility-and-why-it-matters)
2. [WCAG Standards and Conformance Levels](#2-wcag-standards-and-conformance-levels)
3. [Semantic HTML — The Foundation](#3-semantic-html--the-foundation)
4. [ARIA — Complete Reference](#4-aria--complete-reference)
5. [Keyboard Navigation](#5-keyboard-navigation)
6. [Focus Management with JavaScript](#6-focus-management-with-javascript)
7. [Accessible Forms](#7-accessible-forms)
8. [Images and Media Content](#8-images-and-media-content)
9. [Color, Contrast and Visual Design (CSS)](#9-color-contrast-and-visual-design-css)
10. [Motion and Animations](#10-motion-and-animations)
11. [Accessible UI Components](#11-accessible-ui-components)
12. [Live Regions and Notifications](#12-live-regions-and-notifications)
13. [Mobile Accessibility](#13-mobile-accessibility)
14. [Accessibility Testing](#14-accessibility-testing)
15. [Developer Checklist](#15-developer-checklist)
16. [Tools and Resources](#16-tools-and-resources)

---

## 1. What is Accessibility and Why It Matters

**Web accessibility (a11y)** is the practice of building websites and applications so that all people can use them, including those with physical, visual, auditory, cognitive, or motor disabilities.

### Who Uses Assistive Technologies

| Category | Tools |
|---|---|
| Blind and low-vision | Screen readers (NVDA, JAWS, VoiceOver, TalkBack) |
| Motor disabilities | Keyboard, switch devices, eye-tracking |
| Deaf and hard of hearing | Captions, transcripts |
| Cognitive differences | Plain language, predictable UI |
| Elderly users | Text zoom, high contrast |
| Situational limitations | Broken arm, bright sunlight on screen |

### Why It Matters

- **~15% of the world's population** lives with some form of disability (WHO)
- Many countries legally require WCAG compliance (ADA, EAA, Section 508)
- Accessible code = clean, semantic, SEO-friendly code
- Improves the experience for everyone (elevator pitch: captions were invented for deaf people, but everyone uses them)

---

## 2. WCAG Standards and Conformance Levels

**WCAG (Web Content Accessibility Guidelines)** is an international standard from the W3C.

### 4 Core Principles (POUR)

| Principle | Meaning |
|---|---|
| **P**erceivable | Content must be presentable in ways users can perceive |
| **O**perable | UI components must be operable by any input method |
| **U**nderstandable | Content and UI must be understandable |
| **R**obust | Content must work reliably with assistive technologies |

### Conformance Levels

- **A** — minimum, mandatory baseline
- **AA** — standard for most websites (legally required in most countries)
- **AAA** — enhanced, for specialized resources

> 🎯 **Target for most projects: WCAG 2.2 AA**

---

## 3. Semantic HTML — The Foundation

### The Golden Rule

```html
<!-- ❌ Bad — semantics lost, must duplicate everything via ARIA -->
<div class="button" onclick="submit()">Submit</div>

<!-- ✅ Good — native behavior, keyboard, role — all for free -->
<button type="submit">Submit</button>
```

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Unique and Descriptive Page Title</title>
</head>
<body>

  <!-- Skip link for keyboard users -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <header>
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content">
    <h1>Page Heading</h1>
    <!-- Main content -->
  </main>

  <aside aria-label="Related resources">
    <!-- Sidebar -->
  </aside>

  <footer>
    <!-- Footer -->
  </footer>

</body>
</html>
```

### Heading Hierarchy

```html
<!-- ❌ Bad — skipping levels, headings used for styling only -->
<h1>Company Site</h1>
<h3>Services</h3>  <!-- h2 is missing! -->
<h5>Development</h5>

<!-- ✅ Good — sequential hierarchy -->
<h1>Company Site</h1>
  <h2>Services</h2>
    <h3>Development</h3>
    <h3>Design</h3>
  <h2>Contact</h2>
```

### Semantic Tags and Their Meaning

```html
<!-- Text-level -->
<p>Paragraph</p>
<strong>Important (semantic)</strong>     <!-- not just bold -->
<em>Emphasis (semantic)</em>              <!-- not just italic -->
<b>Visually bold</b>                      <!-- no semantic meaning -->
<i>Visually italic</i>                    <!-- no semantic meaning -->
<mark>Highlighted/found text</mark>
<abbr title="HyperText Markup Language">HTML</abbr>
<time datetime="2024-01-15">January 15</time>
<code>console.log()</code>
<kbd>Ctrl+C</kbd>                         <!-- keyboard key -->
<blockquote cite="https://source.com">Quote</blockquote>
<cite>Citation source</cite>

<!-- Structural -->
<article>   <!-- self-contained content (post, card) -->
<section>   <!-- thematic section -->
<aside>     <!-- sidebar / supplemental content -->
<figure>    <!-- illustration, diagram, code -->
  <figcaption>Caption for the figure</figcaption>
</figure>

<!-- Lists -->
<ul>  <!-- unordered -->
<ol>  <!-- ordered -->
<dl>  <!-- description list -->
  <dt>Term</dt>
  <dd>Definition</dd>
</dl>
```

### Links vs Buttons

```html
<!-- Link — for navigation, changes URL -->
<a href="/page">Go to page</a>
<a href="https://external.com" target="_blank" rel="noopener noreferrer">
  External site
  <span class="visually-hidden">(opens in a new tab)</span>
</a>

<!-- Button — for actions, does not change URL -->
<button type="button" onclick="openModal()">Open modal</button>
<button type="submit">Submit form</button>
<button type="reset">Reset form</button>
```

---

## 4. ARIA — Complete Reference

> **First rule of ARIA**: Do not use ARIA if a native HTML element exists.

### Roles (role)

#### Landmark Roles
```html
<div role="banner">        <!-- = top-level <header> -->
<div role="navigation">    <!-- = <nav> -->
<div role="main">          <!-- = <main> -->
<div role="complementary"> <!-- = <aside> -->
<div role="contentinfo">   <!-- = top-level <footer> -->
<div role="search">        <!-- search form -->
<div role="region" aria-labelledby="section-title"> <!-- = named <section> -->
```

#### Widget Roles
```html
<div role="button">        <!-- interactive button -->
<div role="link">          <!-- link -->
<div role="checkbox">      <!-- checkbox -->
<div role="radio">         <!-- radio button -->
<div role="textbox">       <!-- text input -->
<div role="combobox">      <!-- dropdown with text input -->
<div role="listbox">       <!-- selection list -->
<div role="option">        <!-- listbox/combobox item -->
<div role="slider">        <!-- range slider -->
<div role="spinbutton">    <!-- numeric input with arrows -->
<div role="switch">        <!-- on/off toggle -->
<div role="tab">           <!-- tab -->
<div role="tablist">       <!-- tab container -->
<div role="tabpanel">      <!-- tab content panel -->
<div role="menu">          <!-- context menu -->
<div role="menuitem">      <!-- menu item -->
<div role="menuitemcheckbox"> <!-- menu item with checkbox -->
<div role="menuitemradio">    <!-- menu item with radio -->
<div role="tree">          <!-- tree widget -->
<div role="treeitem">      <!-- tree item -->
<div role="grid">          <!-- interactive grid -->
<div role="gridcell">      <!-- grid cell -->
<div role="tooltip">       <!-- tooltip -->
<div role="dialog">        <!-- dialog window -->
<div role="alertdialog">   <!-- alert dialog -->
```

#### Live Content Roles
```html
<div role="alert">         <!-- urgent message (implicit aria-live="assertive") -->
<div role="status">        <!-- status message (implicit aria-live="polite") -->
<div role="log">           <!-- message log -->
<div role="marquee">       <!-- scrolling content -->
<div role="timer">         <!-- timer -->
<div role="progressbar">   <!-- progress bar -->
```

---

### Properties

#### Naming Elements
```html
<!-- aria-label — direct label -->
<button aria-label="Close dialog">✕</button>
<input type="search" aria-label="Search the site">
<nav aria-label="Breadcrumbs">...</nav>

<!-- aria-labelledby — reference to an element's id -->
<h2 id="products-title">Our Products</h2>
<section aria-labelledby="products-title">...</section>

<!-- Labelling with multiple elements -->
<span id="first">First</span>
<span id="last">Last</span>
<input aria-labelledby="first last">

<!-- aria-describedby — additional description -->
<label for="password">Password</label>
<input id="password" type="password" aria-describedby="password-hint password-strength">
<p id="password-hint">At least 8 characters, letters and numbers</p>
<p id="password-strength">Strength: medium</p>

<!-- aria-details — link to detailed description -->
<img src="chart.png" alt="Sales chart" aria-details="chart-description">
<div id="chart-description">
  <h3>Sales Chart Data</h3>
  <table>...</table>
</div>
```

#### Relationships Between Elements
```html
<!-- aria-controls — element controls another -->
<button aria-controls="sidebar" aria-expanded="false">Open sidebar</button>
<aside id="sidebar">...</aside>

<!-- aria-owns — element "owns" another (for non-standard DOM structures) -->
<ul role="tree" aria-owns="subtree">...</ul>

<!-- aria-flowto — next element in reading order -->
<div id="step1" aria-flowto="step2">Step 1</div>
<div id="step2">Step 2</div>

<!-- aria-activedescendant — active child element -->
<ul role="listbox" aria-activedescendant="opt2" tabindex="0">
  <li role="option" id="opt1">Option 1</li>
  <li role="option" id="opt2" aria-selected="true">Option 2</li>
</ul>
```

#### Additional Information
```html
<!-- aria-haspopup — has a popup element -->
<button aria-haspopup="menu">Menu</button>
<button aria-haspopup="dialog">Open settings</button>
<button aria-haspopup="listbox">Select city</button>
<!-- values: menu | listbox | tree | grid | dialog | true -->

<!-- aria-keyshortcuts — keyboard shortcuts -->
<button aria-keyshortcuts="Alt+S">Save</button>

<!-- aria-roledescription — override role description -->
<div role="region" aria-roledescription="slide" aria-label="Slide 1 of 5">...</div>

<!-- aria-placeholder — input placeholder -->
<div role="textbox" aria-placeholder="Enter a message">...</div>

<!-- aria-valuemin, aria-valuemax, aria-valuenow, aria-valuetext -->
<div role="slider"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuenow="42"
  aria-valuetext="42 percent">
</div>

<!-- aria-posinset, aria-setsize — position in set -->
<li role="option" aria-setsize="10" aria-posinset="3">Item 3 of 10</li>

<!-- aria-level — heading or tree level -->
<div role="heading" aria-level="2">Second-level heading</div>

<!-- aria-colcount, aria-rowcount, aria-colindex, aria-rowindex — tables -->
<table aria-rowcount="100">
  <tr aria-rowindex="1">
    <td aria-colindex="1">Cell</td>
  </tr>
</table>

<!-- aria-colspan, aria-rowspan — for ARIA grids -->
<div role="gridcell" aria-colspan="2">Merged cell</div>
```

---

### States

```html
<!-- Visibility and state -->
<div aria-hidden="true">           <!-- hidden from AT -->
<button aria-disabled="true">      <!-- disabled -->
<details>
  <summary aria-expanded="false">  <!-- collapsed/expanded -->

<!-- Selection and check -->
<option aria-selected="true">      <!-- selected in list -->
<input type="checkbox" aria-checked="true">   <!-- checked -->
<input type="checkbox" aria-checked="mixed">  <!-- indeterminate -->
<div role="radio" aria-checked="false">       <!-- radio unchecked -->
<button role="switch" aria-checked="true">    <!-- switch on -->

<!-- Editing -->
<input aria-readonly="true">       <!-- read-only -->
<input aria-required="true">       <!-- required field -->
<input aria-invalid="true">        <!-- invalid value -->
<input aria-invalid="grammar">     <!-- grammar error -->
<input aria-invalid="spelling">    <!-- spelling error -->

<!-- Sortable table states -->
<th aria-sort="ascending">         <!-- sorted ascending -->
<th aria-sort="descending">        <!-- sorted descending -->
<th aria-sort="none">              <!-- not sorted -->

<!-- Current item -->
<a aria-current="page">Current page</a>
<li aria-current="step">Current step</li>
<tr aria-current="row">Current row</tr>
<!-- values: page | step | location | date | time | true -->

<!-- Pressed state (for toggle buttons) -->
<button aria-pressed="true">Bold</button>
<button aria-pressed="false">Italic</button>

<!-- Drag and drop -->
<div aria-grabbed="true">          <!-- being dragged -->
<div aria-dropeffect="move">       <!-- accepts drop -->

<!-- Busy -->
<div aria-busy="true">Loading...</div>
```

---

### aria-live — Live Regions

```html
<!-- polite — screen reader announces after finishing current phrase -->
<div aria-live="polite">
  42 results found
</div>

<!-- assertive — interrupts screen reader immediately (critical messages only) -->
<div aria-live="assertive" role="alert">
  Critical error! Your session has expired.
</div>

<!-- off — changes are not announced -->
<div aria-live="off">...</div>

<!-- aria-atomic — announce whole region or just changes -->
<div aria-live="polite" aria-atomic="true">
  Cart: 3 items totalling $49.99
</div>

<!-- aria-relevant — which changes to announce -->
<!-- additions | removals | text | all -->
<div aria-live="polite" aria-relevant="additions text">
  <!-- announce only additions and text changes -->
</div>
```

---

## 5. Keyboard Navigation

### Key Bindings

| Key | Action |
|---|---|
| `Tab` | Move to next focusable element |
| `Shift+Tab` | Move to previous focusable element |
| `Enter` | Activate link or button |
| `Space` | Activate button or checkbox |
| `Arrow keys` | Navigate within component (tabs, menu, listbox) |
| `Esc` | Close dialog/menu, cancel action |
| `Home/End` | First/last item in a group |

### tabindex

```html
<!-- tabindex="0" — add to tab order (only for natively non-focusable elements) -->
<div role="button" tabindex="0">Custom button</div>

<!-- tabindex="-1" — remove from tab order, but keep focus() accessible via JS -->
<div id="modal-content" tabindex="-1">Modal content</div>

<!-- tabindex="1+" — DO NOT USE! Breaks natural tab order -->
<!-- ❌ -->
<button tabindex="2">Button 2</button>
<button tabindex="1">Button 1</button>
```

### Skip Links

```html
<!-- HTML -->
<a href="#main-content" class="skip-link">Skip to main content</a>
<a href="#nav" class="skip-link">Skip to navigation</a>
```

```css
/* CSS */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px 16px;
  text-decoration: none;
  z-index: 9999;
  transition: top 0.2s;
}

.skip-link:focus {
  top: 0;
}
```

### Focus Order

```html
<!-- Tab order must match visual order -->
<!-- Don't change order via CSS only (flex-direction: row-reverse etc.) -->

<!-- ❌ Bad — visual and DOM order differ -->
<style>
  .container { display: flex; flex-direction: row-reverse; }
</style>
<div class="container">
  <button>Button 3</button>  <!-- visually right, first in DOM -->
  <button>Button 2</button>
  <button>Button 1</button>  <!-- visually left, last in DOM -->
</div>

<!-- ✅ Good — DOM order matches visual order -->
<div class="container">
  <button>Button 1</button>
  <button>Button 2</button>
  <button>Button 3</button>
</div>
```

---

## 6. Focus Management with JavaScript

### Basic Operations

```javascript
// Set focus on an element
element.focus();

// Remove focus
element.blur();

// Get current focused element
const focused = document.activeElement;

// Check if element is focusable
function isFocusable(el) {
  return el.tabIndex >= 0 && !el.disabled && el.offsetWidth > 0;
}
```

### Focus Trap — for Modal Windows

```javascript
function createFocusTrap(container) {
  const focusableSelectors = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
    'details > summary',
  ].join(', ');

  function getFocusableElements() {
    return [...container.querySelectorAll(focusableSelectors)];
  }

  function handleKeydown(e) {
    if (e.key !== 'Tab') return;

    const focusable = getFocusableElements();
    const firstEl = focusable[0];
    const lastEl = focusable[focusable.length - 1];

    if (e.shiftKey) {
      // Shift+Tab — going backwards
      if (document.activeElement === firstEl) {
        e.preventDefault();
        lastEl.focus();
      }
    } else {
      // Tab — going forwards
      if (document.activeElement === lastEl) {
        e.preventDefault();
        firstEl.focus();
      }
    }
  }

  container.addEventListener('keydown', handleKeydown);

  return {
    activate() {
      const focusable = getFocusableElements();
      if (focusable.length) focusable[0].focus();
    },
    deactivate() {
      container.removeEventListener('keydown', handleKeydown);
    }
  };
}

// Usage
const modal = document.getElementById('modal');
const trap = createFocusTrap(modal);

function openModal() {
  modal.removeAttribute('hidden');
  modal.setAttribute('aria-hidden', 'false');
  trap.activate();
  // Save element that was focused before opening
  previousFocus = document.activeElement;
}

function closeModal() {
  modal.setAttribute('hidden', '');
  modal.setAttribute('aria-hidden', 'true');
  trap.deactivate();
  // Return focus
  previousFocus?.focus();
}
```

### Focus Management on Route Change (SPA)

```javascript
// On page change in an SPA — move focus to heading or main
function handleRouteChange() {
  const main = document.getElementById('main-content');
  const heading = document.querySelector('h1');

  const target = heading || main;
  if (target) {
    if (!target.hasAttribute('tabindex')) {
      target.setAttribute('tabindex', '-1');
    }
    target.focus();
    window.scrollTo(0, 0);
  }
}
```

### Keyboard Events

```javascript
// Full keyboard support for a custom component
element.addEventListener('keydown', (e) => {
  switch (e.key) {
    case 'Enter':
    case ' ':         // Space for buttons
      e.preventDefault();
      element.click();
      break;
    case 'Escape':
      closeMenu();
      break;
    case 'ArrowDown':
      e.preventDefault();
      focusNextItem();
      break;
    case 'ArrowUp':
      e.preventDefault();
      focusPrevItem();
      break;
    case 'Home':
      e.preventDefault();
      focusFirstItem();
      break;
    case 'End':
      e.preventDefault();
      focusLastItem();
      break;
  }
});
```

### Roving tabindex — Navigation Within a Component

```javascript
// Pattern: only one element in a group has tabindex="0", others have "-1"
// Arrow keys move within, Tab exits the component

class RovingTabindex {
  constructor(container, itemSelector) {
    this.container = container;
    this.itemSelector = itemSelector;
    this.items = [...container.querySelectorAll(itemSelector)];
    this.currentIndex = 0;

    this.init();
  }

  init() {
    this.items.forEach((item, i) => {
      item.setAttribute('tabindex', i === 0 ? '0' : '-1');
    });

    this.container.addEventListener('keydown', this.handleKeydown.bind(this));
  }

  setFocus(index) {
    this.items[this.currentIndex].setAttribute('tabindex', '-1');
    this.currentIndex = (index + this.items.length) % this.items.length;
    this.items[this.currentIndex].setAttribute('tabindex', '0');
    this.items[this.currentIndex].focus();
  }

  handleKeydown(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      this.setFocus(this.currentIndex + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      this.setFocus(this.currentIndex - 1);
    } else if (e.key === 'Home') {
      e.preventDefault();
      this.setFocus(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      this.setFocus(this.items.length - 1);
    }
  }
}

// Usage
const tablist = document.querySelector('[role="tablist"]');
new RovingTabindex(tablist, '[role="tab"]');
```

---

## 7. Accessible Forms

### Correct Markup

```html
<form novalidate>  <!-- disable native browser validation, implement your own -->

  <!-- Every field must have a label -->
  <div class="field">
    <label for="name">
      Name
      <span aria-hidden="true">*</span>  <!-- asterisk is decorative -->
    </label>
    <input
      id="name"
      type="text"
      name="name"
      autocomplete="given-name"
      aria-required="true"
      aria-describedby="name-error"
    >
    <span id="name-error" role="alert" aria-live="polite" class="error" hidden>
      Please enter your name
    </span>
  </div>

  <!-- Field groups — fieldset + legend -->
  <fieldset>
    <legend>Payment method</legend>

    <label>
      <input type="radio" name="payment" value="card">
      Credit card
    </label>
    <label>
      <input type="radio" name="payment" value="cash">
      Cash
    </label>
  </fieldset>

  <!-- Checkboxes -->
  <fieldset>
    <legend>Notifications</legend>
    <label>
      <input type="checkbox" name="email-notify">
      By email
    </label>
    <label>
      <input type="checkbox" name="sms-notify">
      By SMS
    </label>
  </fieldset>

  <!-- Select -->
  <div class="field">
    <label for="country">Country</label>
    <select id="country" name="country" autocomplete="country">
      <option value="">-- Select a country --</option>
      <option value="us">United States</option>
      <option value="gb">United Kingdom</option>
    </select>
  </div>

  <!-- Textarea -->
  <div class="field">
    <label for="message">
      Message
      <span class="hint">(optional)</span>
    </label>
    <textarea
      id="message"
      name="message"
      rows="5"
      aria-describedby="message-hint"
    ></textarea>
    <p id="message-hint" class="hint">Maximum 500 characters</p>
  </div>

  <!-- Button with a clear action -->
  <button type="submit">Submit request</button>

</form>
```

### Validation and Errors

```javascript
function validateField(input) {
  const errorEl = document.getElementById(input.getAttribute('aria-describedby').split(' ')[0]);

  if (!input.value.trim() && input.required) {
    // Show error
    input.setAttribute('aria-invalid', 'true');
    errorEl.textContent = 'This field is required';
    errorEl.removeAttribute('hidden');
    return false;
  }

  // Clear error
  input.setAttribute('aria-invalid', 'false');
  errorEl.setAttribute('hidden', '');
  return true;
}

// Error summary on submit
function showSummaryError(errors) {
  const summary = document.getElementById('error-summary');
  const list = summary.querySelector('ul');

  list.innerHTML = errors.map(err =>
    `<li><a href="#${err.fieldId}">${err.message}</a></li>`
  ).join('');

  summary.removeAttribute('hidden');
  summary.focus();  // move focus to summary
}
```

```html
<!-- Error summary — placed at top of form -->
<div
  id="error-summary"
  role="alert"
  tabindex="-1"
  hidden
>
  <h2>Please fix the following errors:</h2>
  <ul>
    <!-- Errors with links to fields -->
  </ul>
</div>
```

### autocomplete — Helping Users Fill Forms

```html
<input autocomplete="name">             <!-- full name -->
<input autocomplete="given-name">       <!-- first name -->
<input autocomplete="family-name">      <!-- last name -->
<input autocomplete="email">            <!-- email -->
<input autocomplete="tel">              <!-- phone -->
<input autocomplete="username">         <!-- username -->
<input autocomplete="current-password"> <!-- current password -->
<input autocomplete="new-password">     <!-- new password -->
<input autocomplete="street-address">   <!-- street address -->
<input autocomplete="postal-code">      <!-- postal code -->
<input autocomplete="country">          <!-- country -->
<input autocomplete="cc-number">        <!-- card number -->
<input autocomplete="cc-exp">           <!-- card expiry -->
```

### Visually Hidden but Accessible Labels

```css
/* Visually hidden — hidden visually, but read by screen readers */
.visually-hidden,
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

/* Focusable version — for skip links */
.visually-hidden:focus,
.sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

---

## 8. Images and Media Content

### alt Text

```html
<!-- Informative image — describe the content -->
<img src="team.jpg" alt="A team of 5 people posing outside the Acme office">

<!-- Functional image — describe the action/purpose -->
<button>
  <img src="search-icon.svg" alt="">  <!-- alt="" when text is present nearby -->
  Search
</button>

<a href="/">
  <img src="logo.svg" alt="Acme — go to homepage">
</a>

<!-- Decorative image — empty alt -->
<img src="decorative-wave.svg" alt="" role="presentation">

<!-- Complex image — charts, diagrams -->
<figure>
  <img
    src="sales-chart.png"
    alt="Sales chart for 2024"
    aria-describedby="chart-data"
  >
  <figcaption id="chart-data">
    Sales Q1: $120k. Q2: $145k. Q3: $98k. Q4: $210k.
    Year-over-year growth: 15% compared to 2023.
  </figcaption>
</figure>

<!-- SVG — use title and desc -->
<svg role="img" aria-labelledby="svg-title svg-desc">
  <title id="svg-title">Company logo</title>
  <desc id="svg-desc">Blue circle with a white letter A in the center</desc>
  <!-- ... -->
</svg>

<!-- CSS background image with meaningful content -->
<div class="hero-banner" role="img" aria-label="Mountain peak at sunrise">
</div>
```

### Video and Audio

```html
<!-- Video with captions and transcript -->
<video controls>
  <source src="video.mp4" type="video/mp4">

  <!-- Captions -->
  <track kind="subtitles" src="subs-en.vtt" srclang="en" label="English" default>
  <track kind="subtitles" src="subs-es.vtt" srclang="es" label="Español">

  <!-- Audio description for low-vision users -->
  <track kind="descriptions" src="desc-en.vtt" srclang="en" label="Description">

  <!-- Fallback for browsers without video support -->
  <p>Your browser does not support video.
     <a href="video.mp4">Download the video</a>
  </p>
</video>

<!-- Link to transcript -->
<p>
  <a href="transcript.html">Read video transcript</a>
</p>

<!-- Audio -->
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg">
</audio>
<a href="transcript.html">Podcast transcript</a>
```

---

## 9. Color, Contrast and Visual Design (CSS)

### Text Contrast (WCAG AA)

| Text Type | Minimum Contrast (AA) | Enhanced (AAA) |
|---|---|---|
| Normal text | 4.5:1 | 7:1 |
| Large text (18pt / 14pt bold) | 3:1 | 4.5:1 |
| UI components, charts | 3:1 | — |
| Decorative elements | No requirement | — |

```css
/* Always check contrast with tools! */

/* ❌ Bad — gray text on white, contrast ~2:1 */
.hint { color: #aaa; }

/* ✅ Good — dark gray on white, contrast ~7:1 */
.hint { color: #595959; }
```

### Don't Use Color as the Only Indicator

```html
<!-- ❌ Bad — only color distinguishes error from success -->
<input class="error">    <!-- red border -->
<input class="success">  <!-- green border -->

<!-- ✅ Good — color + icon + text -->
<div class="field-error">
  <span aria-hidden="true">⚠</span>
  <input aria-invalid="true" aria-describedby="err">
  <span id="err">Invalid email format</span>
</div>
```

```css
/* Links must differ from body text in more than just color */

/* ❌ Bad — color only */
a { color: blue; }

/* ✅ Good — color + underline */
a {
  color: #0066cc;
  text-decoration: underline;
}

/* Or with sufficient contrast — remove underline but add another visual cue */
a {
  color: #0066cc;
  text-decoration: none;
  border-bottom: 2px solid currentColor;
}
a:hover, a:focus {
  text-decoration: underline;
}
```

### Visible Focus

```css
/* ❌ NEVER remove outline without a replacement! */
*:focus { outline: none; }  /* THIS IS FORBIDDEN */

/* ✅ Remove only if replaced */
:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* Nice style only for keyboard users */
:focus:not(:focus-visible) {
  outline: none;  /* remove on mouse click */
}

:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
  border-radius: 2px;
}
```

### Text Size and Responsiveness

```css
/* Use relative units */
html { font-size: 100%; }   /* not px! */
body { font-size: 1rem; }

/* Text must scale to 200% without loss of content */
@media (max-width: 600px) {
  body { font-size: clamp(1rem, 2.5vw, 1.25rem); }
}

/* Line height — minimum 1.5 for body text */
p {
  line-height: 1.5;
  margin-bottom: 1.5em;
  max-width: 75ch;
}

/* Letter spacing */
p { letter-spacing: 0.12em; }   /* no more than this */
/* Word spacing */
p { word-spacing: 0.16em; }     /* no more than this */
```

### Windows High Contrast Mode

```css
/* Support for Windows High Contrast Mode */
@media (forced-colors: active) {
  /* Forced system colors, override your own */
  .custom-button {
    border: 2px solid ButtonText;
    color: ButtonText;
    background: ButtonFace;
  }

  /* Don't hide outline */
  *:focus {
    outline: 2px solid Highlight !important;
  }
}

/* Legacy IE syntax */
@media (-ms-high-contrast: active) {
  .icon { border: 1px solid windowText; }
}
```

### User Color Preferences

```css
/* Dark system theme */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #121212;
    --text: #e0e0e0;
    --accent: #90caf9;
  }
}

/* Light theme */
@media (prefers-color-scheme: light) {
  :root {
    --bg: #ffffff;
    --text: #212121;
    --accent: #1565c0;
  }
}
```

---

## 10. Motion and Animations

### prefers-reduced-motion

```css
/* Base animations */
.button {
  transition: transform 0.2s ease, background-color 0.2s ease;
}

/* Disable / simplify based on system setting */
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

/* More nuanced approach — only remove decorative animations */
@media (prefers-reduced-motion: reduce) {
  .hero-animation { animation: none; }
  .parallax { transform: none !important; }
  .scroll-fade { opacity: 1 !important; }

  /* Keep functional animations (focus, state changes) */
  :focus-visible { outline: 3px solid #005fcc; }
}
```

```javascript
// Check in JavaScript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  // Run animation
  animateElement(el);
} else {
  // Show immediately
  el.style.opacity = '1';
}
```

### Dangerous Animations (Seizure Risk)

```
❌ PROHIBITED:
- Flashing more than 3 times per second
- Large flashing areas (>25% of the screen)
- Red flashes
```

---

## 11. Accessible UI Components

### Modal Dialog

```html
<button id="open-modal">Open dialog</button>

<div
  id="modal"
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
  hidden
>
  <h2 id="modal-title">Confirm deletion</h2>
  <p id="modal-desc">This action cannot be undone. Are you sure?</p>

  <div class="modal-actions">
    <button id="confirm-delete" autofocus>Delete</button>
    <button id="close-modal">Cancel</button>
  </div>
</div>

<div id="modal-backdrop" hidden></div>
```

```javascript
const modal = document.getElementById('modal');
const openBtn = document.getElementById('open-modal');
const closeBtn = document.getElementById('close-modal');
let lastFocused;

function openModal() {
  lastFocused = document.activeElement;
  modal.removeAttribute('hidden');
  document.getElementById('modal-backdrop').removeAttribute('hidden');
  document.body.setAttribute('aria-hidden', 'true');  // hide main content
  modal.removeAttribute('aria-hidden');

  // Focus the first interactive element or autofocus
  modal.querySelector('[autofocus]')?.focus() ||
  modal.querySelector('button, input, [tabindex="0"]')?.focus();
}

function closeModal() {
  modal.setAttribute('hidden', '');
  document.getElementById('modal-backdrop').setAttribute('hidden', '');
  document.body.removeAttribute('aria-hidden');
  lastFocused?.focus();  // return focus
}

// Close on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !modal.hidden) closeModal();
});

// Close on backdrop click
document.getElementById('modal-backdrop').addEventListener('click', closeModal);
```

### Tabs

```html
<div class="tabs">
  <div role="tablist" aria-label="Product information">
    <button
      role="tab"
      id="tab-desc"
      aria-controls="panel-desc"
      aria-selected="true"
      tabindex="0"
    >Description</button>

    <button
      role="tab"
      id="tab-specs"
      aria-controls="panel-specs"
      aria-selected="false"
      tabindex="-1"
    >Specifications</button>

    <button
      role="tab"
      id="tab-reviews"
      aria-controls="panel-reviews"
      aria-selected="false"
      tabindex="-1"
    >Reviews</button>
  </div>

  <div role="tabpanel" id="panel-desc" aria-labelledby="tab-desc">
    <h3>Product Description</h3>
    <p>...</p>
  </div>

  <div role="tabpanel" id="panel-specs" aria-labelledby="tab-specs" hidden>
    <h3>Technical Specifications</h3>
    <p>...</p>
  </div>

  <div role="tabpanel" id="panel-reviews" aria-labelledby="tab-reviews" hidden>
    <h3>Customer Reviews</h3>
    <p>...</p>
  </div>
</div>
```

```javascript
const tablist = document.querySelector('[role="tablist"]');
const tabs = [...tablist.querySelectorAll('[role="tab"]')];

tablist.addEventListener('keydown', (e) => {
  const currentIndex = tabs.indexOf(document.activeElement);
  let newIndex;

  if (e.key === 'ArrowRight') {
    newIndex = (currentIndex + 1) % tabs.length;
  } else if (e.key === 'ArrowLeft') {
    newIndex = (currentIndex - 1 + tabs.length) % tabs.length;
  } else if (e.key === 'Home') {
    newIndex = 0;
  } else if (e.key === 'End') {
    newIndex = tabs.length - 1;
  } else return;

  e.preventDefault();
  activateTab(tabs[newIndex]);
});

function activateTab(tab) {
  // Reset all
  tabs.forEach(t => {
    t.setAttribute('aria-selected', 'false');
    t.setAttribute('tabindex', '-1');
    document.getElementById(t.getAttribute('aria-controls')).hidden = true;
  });

  // Activate selected
  tab.setAttribute('aria-selected', 'true');
  tab.setAttribute('tabindex', '0');
  tab.focus();
  document.getElementById(tab.getAttribute('aria-controls')).hidden = false;
}
```

### Accordion

```html
<div class="accordion">
  <h3>
    <button
      type="button"
      aria-expanded="false"
      aria-controls="section1-content"
      id="section1-header"
    >
      How do I place an order?
      <span aria-hidden="true" class="icon">▼</span>
    </button>
  </h3>
  <div
    id="section1-content"
    role="region"
    aria-labelledby="section1-header"
    hidden
  >
    <p>To place an order...</p>
  </div>

  <h3>
    <button
      type="button"
      aria-expanded="false"
      aria-controls="section2-content"
      id="section2-header"
    >
      Payment methods
    </button>
  </h3>
  <div
    id="section2-content"
    role="region"
    aria-labelledby="section2-header"
    hidden
  >
    <p>We accept...</p>
  </div>
</div>
```

### Dropdown Menu (Disclosure)

```html
<div class="dropdown">
  <button
    type="button"
    aria-haspopup="menu"
    aria-expanded="false"
    aria-controls="user-menu"
    id="user-menu-btn"
  >
    Profile
  </button>

  <ul
    role="menu"
    id="user-menu"
    aria-labelledby="user-menu-btn"
    hidden
  >
    <li role="none">
      <a role="menuitem" href="/settings">Settings</a>
    </li>
    <li role="none">
      <a role="menuitem" href="/orders">Orders</a>
    </li>
    <li role="none">
      <button role="menuitem" type="button">Sign out</button>
    </li>
  </ul>
</div>
```

### Toast Notifications

```html
<!-- Toast container -->
<div
  id="toast-container"
  aria-live="polite"
  aria-atomic="false"
  class="toast-container"
>
</div>
```

```javascript
function showToast(message, type = 'info', duration = 5000) {
  const container = document.getElementById('toast-container');

  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.setAttribute('role', type === 'error' ? 'alert' : 'status');
  toast.innerHTML = `
    <span class="toast__message">${message}</span>
    <button class="toast__close" aria-label="Close notification">✕</button>
  `;

  toast.querySelector('.toast__close').addEventListener('click', () => {
    removeToast(toast);
  });

  container.appendChild(toast);

  if (duration > 0) {
    setTimeout(() => removeToast(toast), duration);
  }

  return toast;
}

function removeToast(toast) {
  toast.setAttribute('aria-hidden', 'true');
  toast.addEventListener('transitionend', () => toast.remove());
}
```

### Carousel / Slider

```html
<section aria-roledescription="carousel" aria-label="Featured products">

  <!-- Controls -->
  <div class="carousel-controls">
    <button
      type="button"
      aria-label="Previous slide"
      id="prev-btn"
    >‹</button>

    <!-- Indicators -->
    <div role="group" aria-label="Slides">
      <button aria-label="Slide 1" aria-current="true" aria-pressed="true">•</button>
      <button aria-label="Slide 2" aria-pressed="false">•</button>
      <button aria-label="Slide 3" aria-pressed="false">•</button>
    </div>

    <button
      type="button"
      aria-label="Next slide"
      id="next-btn"
    >›</button>

    <!-- Autoplay pause -->
    <button
      type="button"
      id="autoplay-btn"
      aria-label="Stop autoplay"
      aria-pressed="true"
    >⏸</button>
  </div>

  <!-- Slides -->
  <div class="carousel-slides">
    <div
      role="group"
      aria-roledescription="slide"
      aria-label="1 of 3: Samsung Smartphone"
      aria-hidden="false"
    >
      <img src="phone.jpg" alt="Samsung Galaxy S24 smartphone">
      <h3>Samsung Galaxy S24</h3>
      <p>From $799</p>
    </div>

    <div
      role="group"
      aria-roledescription="slide"
      aria-label="2 of 3: Apple Laptop"
      aria-hidden="true"
    >
      <!-- ... -->
    </div>
  </div>

</section>
```

### Data Tables

```html
<!-- Simple table -->
<table>
  <caption>Q4 2024 Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Quantity</th>
      <th scope="col">Revenue ($)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Smartphone</td>
      <td>150</td>
      <td>112,500</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td>Total</td>
      <td>450</td>
      <td>287,500</td>
    </tr>
  </tfoot>
</table>

<!-- Complex table with grouping -->
<table>
  <caption>Class Schedule</caption>
  <thead>
    <tr>
      <th scope="col" id="time-col">Time</th>
      <th scope="col" id="mon-col">Mon</th>
      <th scope="col" id="tue-col">Tue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row" id="row-9">9:00 AM</th>
      <td headers="mon-col row-9">Math</td>
      <td headers="tue-col row-9">Physics</td>
    </tr>
  </tbody>
</table>

<!-- Sortable table -->
<table>
  <thead>
    <tr>
      <th scope="col">
        <button aria-sort="none" type="button">
          Name <span aria-hidden="true">↕</span>
        </button>
      </th>
      <th scope="col">
        <button aria-sort="ascending" type="button">
          Date <span aria-hidden="true">↑</span>
        </button>
      </th>
    </tr>
  </thead>
</table>
```

---

## 12. Live Regions and Notifications

### Usage Patterns

```javascript
// Universal function for screen reader announcements
function announce(message, priority = 'polite') {
  const announcer = document.getElementById(`aria-announcer-${priority}`);

  // Clear then reset — ensures the announcement fires
  announcer.textContent = '';

  requestAnimationFrame(() => {
    announcer.textContent = message;
  });
}

// Place in HTML (visually hidden)
// <div id="aria-announcer-polite" aria-live="polite" class="visually-hidden"></div>
// <div id="aria-announcer-assertive" aria-live="assertive" class="visually-hidden"></div>

// Usage
announce('Item added to cart');
announce('Critical error: could not save', 'assertive');
announce(`Found ${count} results`);
announce('Load complete, showing 20 of 100 items');
```

### Loading Progress

```html
<!-- Page loading indicator -->
<div
  id="loading"
  role="status"
  aria-live="polite"
  aria-label="Loading"
  hidden
>
  <span aria-hidden="true" class="spinner"></span>
  <span class="visually-hidden">Loading, please wait</span>
</div>

<!-- Progress bar -->
<div role="progressbar"
  aria-valuenow="45"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Uploading file"
  aria-valuetext="45 percent complete"
>
  <div class="progress-bar__fill" style="width: 45%"></div>
</div>

<!-- Indeterminate progress -->
<div role="progressbar"
  aria-label="Processing request"
  aria-valuetext="In progress"
>
  <!-- Animated indicator -->
</div>
```

---

## 13. Mobile Accessibility

### Touch Targets

```css
/* Minimum touch target size: 44×44px (Apple HIG) / 48×48px (Material) */
button,
a,
input[type="checkbox"],
input[type="radio"] {
  min-height: 44px;
  min-width: 44px;
}

/* Expand click area without changing visual size */
.small-button {
  position: relative;
  padding: 4px;
}

.small-button::after {
  content: '';
  position: absolute;
  inset: -10px;  /* expand clickable area */
}
```

### Zoom / Scaling

```html
<!-- NEVER disable scaling! -->
<!-- ❌ Bad -->
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no, maximum-scale=1">

<!-- ✅ Good -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Gestures

```javascript
// For complex gestures, always provide an alternative
// For example, swipe can be replaced with buttons

// Pointer events support all input devices
element.addEventListener('pointerdown', handleStart);
element.addEventListener('pointermove', handleMove);
element.addEventListener('pointerup', handleEnd);
```

```css
/* Use touch-action CSS to avoid conflicts */
.swipeable {
  touch-action: pan-y;  /* allow vertical scroll, don't block horizontal swipe */
}
```

---

## 14. Accessibility Testing

### Automated Testing

```bash
# axe-core — most popular
npm install axe-core

# Playwright + axe
npm install @axe-core/playwright

# Jest + axe
npm install jest-axe
```

```javascript
// axe-core in browser
import axe from 'axe-core';

axe.run(document, {
  runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
}).then(results => {
  if (results.violations.length) {
    console.error('Accessibility violations:', results.violations);
    results.violations.forEach(v => {
      console.error(`[${v.impact}] ${v.description}`);
      v.nodes.forEach(n => console.error('  Element:', n.html));
    });
  }
});

// Playwright test
import { checkA11y, injectAxe } from 'axe-playwright';

test('homepage is accessible', async ({ page }) => {
  await page.goto('/');
  await injectAxe(page);
  await checkA11y(page, null, {
    axeOptions: {
      runOnly: ['wcag2a', 'wcag2aa']
    }
  });
});

// Jest test
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('button is accessible', async () => {
  const { container } = render(<MyButton label="Save" />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing

#### Keyboard Test (no mouse!)
```
1. Open the page
2. Press Tab — is focus visible?
3. Tab through all interactive elements
4. Can you activate each element with Enter/Space?
5. Do modal dialogs work (Escape closes them)?
6. Does focus return after closing?
7. Does the skip link work?
```

#### Screen Reader Test

| OS | Screen Reader | Browser |
|---|---|---|
| Windows | NVDA (free) | Firefox, Chrome |
| Windows | JAWS | IE, Chrome |
| macOS | VoiceOver (built-in, Cmd+F5) | Safari |
| iOS | VoiceOver (built-in) | Safari |
| Android | TalkBack (built-in) | Chrome |
| Linux | Orca | Firefox |

```
Basic VoiceOver test (macOS):
1. Cmd+F5 — enable
2. Tab — move between elements
3. VO+Arrows — navigate content
4. VO+U — rotor (quick navigation)
5. Cmd+F5 — disable
```

### DevTools

```javascript
// Chrome DevTools → Accessibility tree (Cmd+Shift+P → "Accessibility")
// Firefox → Developer Tools → Accessibility tab
// Lighthouse → Accessibility audit

// Check focus order
document.addEventListener('focusin', (e) => {
  console.log('Focused:', e.target.tagName, e.target.id, e.target.className);
});

// List all interactive elements
const interactive = document.querySelectorAll(
  'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
);
console.table([...interactive].map(el => ({
  tag: el.tagName,
  text: el.textContent?.trim() || el.value || el.alt,
  tabindex: el.tabIndex,
})));
```

---

## 15. Developer Checklist

### HTML
- [ ] `lang` attribute set on `<html>`
- [ ] Unique and descriptive `<title>` on every page
- [ ] Correct heading hierarchy (h1 → h2 → h3)
- [ ] Semantic tags used (nav, main, header, footer, article)
- [ ] All images have `alt` (empty for decorative)
- [ ] Every form field has an associated `<label>`
- [ ] Field groups wrapped in `<fieldset>` with `<legend>`
- [ ] Links used for navigation, buttons used for actions
- [ ] External links warn users about opening in a new tab
- [ ] Data tables have `<caption>` and `scope` on headers

### ARIA
- [ ] ARIA only used where no native HTML exists
- [ ] All custom interactive elements have a role
- [ ] All elements without visible text have `aria-label` or `aria-labelledby`
- [ ] Dynamic content uses `aria-live`
- [ ] Modals use `role="dialog"` and `aria-modal`
- [ ] `aria-expanded` is up to date on trigger buttons
- [ ] `aria-invalid` and `aria-required` on form fields

### Keyboard
- [ ] All functionality is accessible via keyboard
- [ ] Visible focus on all interactive elements
- [ ] Focus order is logical (matches visual order)
- [ ] No focus traps (except inside modals)
- [ ] Modals have focus trap and close on Escape
- [ ] Skip link present at the start of the page
- [ ] `tabindex` only 0 or -1, never positive

### CSS
- [ ] Text contrast minimum 4.5:1 (AA)
- [ ] UI component contrast minimum 3:1
- [ ] Color is not the only indicator of information
- [ ] `outline` visible on focus (no `outline: none`)
- [ ] Animations disabled with `prefers-reduced-motion`
- [ ] No `user-scalable=no` in viewport
- [ ] Text scales to 200% without content loss
- [ ] Touch targets minimum 44×44px

### JavaScript
- [ ] Dynamic changes announced to screen readers
- [ ] Focus returns after closing dialogs
- [ ] On route change (SPA) focus moves to new content
- [ ] Event handlers on both `click` and `keydown`/`keypress`

### Testing
- [ ] axe-core test passes (0 critical violations)
- [ ] Tested with keyboard only (no mouse)
- [ ] Tested with VoiceOver or NVDA
- [ ] Lighthouse Accessibility score ≥ 90

---

## 16. Tools and Resources

### Browser Extensions
- **axe DevTools** — automated accessibility checking
- **WAVE** — visual accessibility checking
- **Accessibility Insights** — full audit (Microsoft)
- **Colour Contrast Analyser** — contrast checking

### Developer Tools
- **Storybook + @storybook/addon-a11y** — component-level checking
- **eslint-plugin-jsx-a11y** — static JSX analysis
- **axe-core, jest-axe, @axe-core/playwright** — automated tests
- **Lighthouse** (built into Chrome DevTools)
- **Pa11y** — CLI tool for automation

### Online Tools
- **WebAIM Contrast Checker** — contrast.webaim.org
- **Colour Contrast Checker** — colourcontrast.cc
- **Accessible Color Palette Builder** — venngage.com/tools/accessible-color-palette-generator
- **WAVE** — wave.webaim.org
- **AChecker** — achecker.achecks.ca

### Standards and Documentation
- **WCAG 2.2** — w3.org/TR/WCAG22
- **ARIA 1.2** — w3.org/TR/wai-aria-1.2
- **ARIA Authoring Practices** — w3.org/WAI/ARIA/apg
- **WebAIM** — webaim.org
- **MDN Accessibility** — developer.mozilla.org/en-US/docs/Web/Accessibility
- **The A11y Project** — a11yproject.com

### Patterns and Components
- **ARIA APG Patterns** — w3.org/WAI/ARIA/apg/patterns (canonical reference)
- **Inclusive Components** — inclusive-components.design
- **Headless UI** — headlessui.com
- **Radix UI** — radix-ui.com
- **React Aria** — react-spectrum.adobe.com/react-aria

---

## Quick Reference: Most Common Mistakes

| Mistake | Fix |
|---|---|
| `<div onclick>` instead of `<button>` | Use `<button>` |
| Image without `alt` | Add `alt` or `alt=""` |
| `outline: none` with no replacement | Style `:focus-visible` |
| Form field without `<label>` | Add `<label for>` or `aria-label` |
| Contrast below 4.5:1 | Adjust text or background color |
| Focus doesn't return after closing dialog | Save `lastFocused` and restore it |
| `tabindex="3"` or higher | Only `0` or `-1` |
| Animation without `prefers-reduced-motion` | Add media query |
| Color as the only indicator | Add icon, text, or shape |
| `user-scalable=no` in viewport | Remove that restriction |
| Empty link `<a href="#">` | Use `<button>` or add `aria-label` |
| No skip link | Add one at the start of the page |
| `aria-label` duplicates visible text | Remove the redundant `aria-label` |

---

*This guide is based on WCAG 2.2, WAI-ARIA 1.2, and the ARIA Authoring Practices Guide.*
*Last updated: 2024*
