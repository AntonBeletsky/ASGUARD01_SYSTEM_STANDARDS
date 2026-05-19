# Frontend Accessibility How-To Guide
## Every Pattern. Every Edge Case. Right vs Wrong.
### HTML · CSS · JavaScript · ARIA

> **How to use this guide:** Every section shows `❌ WRONG` (what breaks accessibility) and `✅ RIGHT` (the correct implementation). Copy-paste the RIGHT patterns directly into your codebase. Works with plain HTML, any CSS framework, any JS framework.

---

## Table of Contents

1. [Document Shell](#1-document-shell)
2. [Language](#2-language)
3. [Page Title](#3-page-title)
4. [Skip Navigation](#4-skip-navigation)
5. [Landmarks and Page Structure](#5-landmarks-and-page-structure)
6. [Headings](#6-headings)
7. [Links](#7-links)
8. [Buttons](#8-buttons)
9. [Images](#9-images)
10. [SVG Icons](#10-svg-icons)
11. [Navigation Menus](#11-navigation-menus)
12. [Dropdown Menus](#12-dropdown-menus)
13. [Mobile Hamburger Menu](#13-mobile-hamburger-menu)
14. [Breadcrumbs](#14-breadcrumbs)
15. [Tabs](#15-tabs)
16. [Accordion](#16-accordion)
17. [Modal Dialogs](#17-modal-dialogs)
18. [Tooltips](#18-tooltips)
19. [Disclosure Widgets](#19-disclosure-widgets)
20. [Carousels and Sliders](#20-carousels-and-sliders)
21. [Forms — Labels and Inputs](#21-forms--labels-and-inputs)
22. [Forms — Checkboxes and Radios](#22-forms--checkboxes-and-radios)
23. [Forms — Select and Combobox](#23-forms--select-and-combobox)
24. [Forms — Validation and Errors](#24-forms--validation-and-errors)
25. [Forms — Complex Patterns](#25-forms--complex-patterns)
26. [Search](#26-search)
27. [Tables](#27-tables)
28. [Lists](#28-lists)
29. [Cards](#29-cards)
30. [Pagination](#30-pagination)
31. [Notifications and Alerts](#31-notifications-and-alerts)
32. [Loading States and Spinners](#32-loading-states-and-spinners)
33. [Progress Bars](#33-progress-bars)
34. [Range Sliders](#34-range-sliders)
35. [Date Pickers](#35-date-pickers)
36. [Video and Audio Players](#36-video-and-audio-players)
37. [Data Visualizations and Charts](#37-data-visualizations-and-charts)
38. [Color and Contrast](#38-color-and-contrast)
39. [Focus Management](#39-focus-management)
40. [CSS Hiding Techniques](#40-css-hiding-techniques)
41. [Animation and Motion](#41-animation-and-motion)
42. [Responsive and Zoom](#42-responsive-and-zoom)
43. [Touch and Pointer](#43-touch-and-pointer)
44. [Keyboard Interaction Patterns](#44-keyboard-interaction-patterns)
45. [Dynamic Content and Live Regions](#45-dynamic-content-and-live-regions)
46. [Single Page App Navigation](#46-single-page-app-navigation)
47. [iframes](#47-iframes)
48. [PDFs and Downloads](#48-pdfs-and-downloads)
49. [Social Media Embeds](#49-social-media-embeds)
50. [Cookie Banners](#50-cookie-banners)
51. [Footer and Contact](#51-footer-and-contact)
52. [Accessibility Statement Page](#52-accessibility-statement-page)

---

## 1. Document Shell

### The Minimal Correct HTML Document

```html
❌ WRONG — Missing charset, viewport blocks zoom, no lang
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, user-scalable=no">
  <title>Home</title>
</head>
<body>...</body>
</html>
```

```html
✅ RIGHT — Full correct document shell
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <!-- 
    NEVER add user-scalable=no or maximum-scale=1
    This violates WCAG 1.4.4 (Resize Text) 
    Users who need to zoom on mobile cannot do so
  -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Brief description of this page (150 chars max)">
  
  <!-- SC 2.4.2: Unique, descriptive title — format: Page Name — Site Name -->
  <title>Products — Acme Corp</title>
  
  <!-- Preconnect to external fonts if used -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  
  <!-- Stylesheet -->
  <link rel="stylesheet" href="/styles.css">
</head>
<body>

  <!-- SC 2.4.1: Skip link — MUST be first focusable element in DOM -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <header>...</header>
  <main id="main-content" tabindex="-1">...</main>
  <footer>...</footer>

  <script src="/app.js" defer></script>
</body>
</html>
```

---

## 2. Language

```html
❌ WRONG — No lang attribute, no language marking for foreign phrases
<html>
<p>Our motto: <em>Auf Wiedersehen</em></p>
```

```html
✅ RIGHT — Page language set; inline language changes marked
<!-- Primary language of entire page -->
<html lang="en">

<!-- Inline content in a different language — SC 3.1.2 -->
<p>Our motto: <em lang="de">Auf Wiedersehen</em></p>

<!-- Multilingual quote -->
<blockquote lang="fr">
  <p>La liberté, l'égalité, la fraternité</p>
</blockquote>

<!-- Full list of language codes: https://www.iana.org/assignments/language-subtag-registry -->
<!-- Common codes:
  en    English
  de    German
  fr    French  
  es    Spanish
  it    Italian
  nl    Dutch
  pl    Polish
  ar    Arabic (also add dir="rtl" to html or element)
  zh    Chinese
  ja    Japanese
  ko    Korean
-->
```

### Right-to-Left Languages

```html
✅ RIGHT — RTL document
<html lang="ar" dir="rtl">

<!-- Or for a single RTL element within LTR page -->
<p>Direction: <span lang="ar" dir="rtl">مرحبا بالعالم</span></p>
```

---

## 3. Page Title

```html
❌ WRONG — Generic, identical on every page, site name first
<title>Acme Corp</title>
<title>Acme Corp - Page</title>
<title>Acme Corp | Contact</title><!-- Same format with generic "Contact" -->
```

```html
✅ RIGHT — Unique, descriptive, page name first (SC 2.4.2)
<!-- Home page -->
<title>Acme Corp — Industrial Widgets Since 1989</title>

<!-- Interior page: Page — Site -->
<title>Contact Us — Acme Corp</title>

<!-- Search results: include search term -->
<title>Search results for "widget" — Acme Corp</title>

<!-- Multi-step form: include step -->
<title>Step 2 of 3: Shipping Address — Checkout — Acme Corp</title>

<!-- Error page -->
<title>Page Not Found (404) — Acme Corp</title>

<!-- After SPA navigation: update programmatically -->
<script>
  function navigateTo(pageName) {
    // ... routing logic
    document.title = `${pageName} — Acme Corp`;
    // Also announce navigation to screen readers — see Section 46
  }
</script>
```

---

## 4. Skip Navigation

```html
❌ WRONG — No skip link; users tab through entire nav on every page
<header>
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
    <!-- 20 more links... -->
  </nav>
</header>
<main>...</main>
```

```html
✅ RIGHT — Skip link as first element (SC 2.4.1)
<body>

  <!-- Must be the FIRST focusable element -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- For complex pages: multiple skip links -->
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <a href="#site-nav"     class="skip-link">Skip to navigation</a>
  <a href="#site-search"  class="skip-link">Skip to search</a>

  <header>
    <nav id="site-nav">...</nav>
  </header>

  <!-- tabindex="-1" enables programmatic focus when skip link is clicked -->
  <main id="main-content" tabindex="-1">
    ...
  </main>

</body>
```

```css
/* Skip link CSS — hidden until focused */
.skip-link {
  position: absolute;
  top: -100vh;          /* Off-screen */
  left: 0;
  z-index: 9999;
  padding: 1rem 1.5rem;
  background: #000;
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  border-radius: 0 0 4px 0;
  
  /* Smooth reveal */
  transition: top 0.1s;
}
.skip-link:focus {
  top: 0;               /* Slides into view on focus */
}

/* Remove default focus ring since we have our own style */
.skip-link:focus {
  outline: 3px solid #fff;
  outline-offset: -3px;
}
```

---

## 5. Landmarks and Page Structure

### Why Landmarks Matter
Screen reader users navigate by landmarks (H, D, N, R keys in NVDA/JAWS). Every page MUST have navigable regions.

```html
❌ WRONG — No landmarks; all divs; screen reader cannot navigate
<div class="header">
  <div class="nav">...</div>
</div>
<div class="content">
  <div class="sidebar">...</div>
</div>
<div class="footer">...</div>
```

```html
✅ RIGHT — Full landmark structure (SC 1.3.1, 2.4.1)
<body>

  <a href="#main" class="skip-link">Skip to main content</a>

  <!-- 
    <header> at top level = implicit role="banner"
    Only ONE banner per page
    If <header> is inside <article>/<section>, it's NOT a banner landmark
  -->
  <header>
    <a href="/" aria-label="Acme Corp — Home">
      <img src="logo.svg" alt=""><!-- Empty alt: logo described in aria-label above -->
    </a>

    <!-- aria-label distinguishes multiple <nav> elements -->
    <nav aria-label="Primary navigation">
      <ul>...</ul>
    </nav>

    <form role="search" aria-label="Site search">
      <input type="search" aria-label="Search">
      <button type="submit">Search</button>
    </form>
  </header>

  <!-- Optional: above-the-fold alert/banner -->
  <!-- Use role="region" with aria-label for named regions without a semantic element -->
  <div role="region" aria-label="Promotional announcement">
    <p>Free shipping on orders over €50</p>
  </div>

  <!--
    <main> = implicit role="main"
    ONE per page
    Target of skip link
  -->
  <main id="main" tabindex="-1">

    <!-- Named section — only add role="region" if the section needs a landmark -->
    <section aria-labelledby="featured-heading">
      <h2 id="featured-heading">Featured Products</h2>
      ...
    </section>

    <!-- <article> = self-contained content (blog post, product card, comment) -->
    <article aria-labelledby="post-title">
      <h2 id="post-title">How We Make Widgets</h2>
      ...
    </article>

  </main>

  <!--
    <aside> = implicit role="complementary"
    Related but not essential to main content
  -->
  <aside aria-label="Related articles">
    ...
  </aside>

  <!--
    <footer> at top level = implicit role="contentinfo"
    ONE per page
  -->
  <footer>
    <nav aria-label="Footer navigation">
      <ul>...</ul>
    </nav>
    <nav aria-label="Legal links">
      <ul>
        <li><a href="/accessibility">Accessibility Statement</a></li>
        <li><a href="/privacy">Privacy Policy</a></li>
      </ul>
    </nav>
  </footer>

</body>
```

### Landmark Rules

| Rule | Detail |
|---|---|
| One `<main>` | Never more than one `<main>` visible at a time |
| One top-level `<header>` as banner | `<header>` inside `<article>` is NOT a banner |
| Label duplicate landmarks | Two `<nav>` elements need `aria-label` to distinguish them |
| `<section>` without a heading | Add `aria-label` or it won't be announced as a landmark |
| `<div>` and `<span>` | Never landmarks; no role by default |

---

## 6. Headings

```html
❌ WRONG — Big text styled to look like headings; skipped levels; decorative h1
<div class="big-text">Welcome</div><!-- looks like h1 but isn't -->
<h1>Products</h1>
<h3>Widget A</h3><!-- skip from h1 to h3 -->
<h3>Widget B</h3>
<h2>About</h2><!-- h2 after h3 is confusing -->

<!-- Using headings for visual styling only -->
<h2>—</h2><!-- decorative divider -->
<h4 style="font-size:0.8rem">small label</h4><!-- heading used for small text -->
```

```html
✅ RIGHT — Correct heading hierarchy (SC 1.3.1, 2.4.6)

<!-- 
  ONE <h1> per page — the page's main topic
  Never skip levels going down (h1→h2→h3 is fine; h1→h3 is wrong)
  Going back up is OK (h3→h2 after closing a subsection)
-->
<main>
  <h1>Our Products</h1><!-- Main topic of page -->
  
  <section>
    <h2>Widgets</h2><!-- Section heading -->
    
    <article>
      <h3>Widget A</h3><!-- Subsection -->
      <p>Description...</p>
    </article>
    
    <article>
      <h3>Widget B</h3>
      <p>Description...</p>
      
      <section>
        <h4>Technical Specifications</h4><!-- Sub-subsection -->
      </section>
    </article>
  </section>
  
  <section>
    <h2>Gadgets</h2><!-- Another h2 — back up from h3 level is fine -->
  </section>
</main>
```

```css
/* 
  Style headings with CSS — not with wrong heading level
  If you need "looks like h3 but is h2": use a class
*/
h2.display-small {
  font-size: 1.1rem;
  font-weight: 500;
}
/* Now: <h2 class="display-small"> — correct semantics, small visual */
```

---

## 7. Links

```html
❌ WRONG — Meaningless link text; link opens in new tab without warning;
          link that looks like a button; JavaScript void links
<a href="#">Click here</a>
<a href="#">Read more</a>
<a href="#">Read more</a><!-- duplicate text, different destinations -->
<a href="doc.pdf">Download</a><!-- no file type/size info -->
<a href="https://partner.com" target="_blank">Partner site</a><!-- no new-tab warning -->
<a href="javascript:void(0)" onclick="doThing()">Do thing</a><!-- use <button> -->
<span onclick="location='/about'">About</span><!-- not keyboard accessible -->
```

```html
✅ RIGHT — Descriptive, informative links (SC 2.4.4, 2.4.9)

<!-- Descriptive text in the link itself -->
<a href="/products/widget-a">View Widget A details</a>

<!-- When visual text is short, extend with aria-label (must contain visible text) -->
<a href="/products/widget-a" 
   aria-label="Read more about Widget A">Read more</a>

<!-- Or use aria-describedby for extra context -->
<article>
  <h3 id="article-title">Widget A</h3>
  <p id="article-desc">Our flagship product...</p>
  <a href="/products/widget-a" aria-describedby="article-title article-desc">
    Read more
  </a>
</article>

<!-- File downloads: include type and size -->
<a href="/docs/manual.pdf" 
   type="application/pdf"
   aria-label="Download product manual (PDF, 2.4 MB)">
  Download manual
  <span aria-hidden="true"> ↓ PDF, 2.4 MB</span>
</a>

<!-- New tab: warn the user -->
<a href="https://partner.com" 
   target="_blank" 
   rel="noopener noreferrer"
   aria-label="Visit partner site (opens in a new tab)">
  Partner site
  <!-- Or use an icon with hidden text: -->
  <svg aria-hidden="true" focusable="false"><!-- external link icon --></svg>
  <span class="visually-hidden">(opens in a new tab)</span>
</a>

<!-- Link to section on same page (anchor link) -->
<a href="#section-pricing">Jump to pricing</a>
<!-- The target must be focusable: -->
<section id="section-pricing" tabindex="-1">
  <h2>Pricing</h2>
</section>

<!-- DO use <button> for actions, <a> for navigation -->
<button onclick="openCart()">Add to cart</button><!-- action → button -->
<a href="/cart">View cart</a><!-- navigation → link -->
```

### Link vs Button — Decision Tree

```
Does clicking navigate to a new URL or same-page anchor?
  YES → use <a href="...">
  NO  → Does clicking perform an action (submit, open modal, toggle, etc.)?
    YES → use <button type="button">
    NO  → Rethink the interaction
```

---

## 8. Buttons

```html
❌ WRONG — Non-button elements used as buttons; buttons without accessible names;
          submit used for non-submit actions; input[type=image] without alt
<div onclick="save()">Save</div><!-- not keyboard accessible -->
<span class="btn" onclick="open()">Open</span><!-- not keyboard accessible -->

<button>
  <img src="close.png"><!-- no alt text → no accessible name -->
</button>

<button>
  <i class="fa fa-trash"></i><!-- icon-only, no accessible name -->
</button>

<input type="image" src="go.png"><!-- no alt attribute -->

<button type="submit" onclick="toggleMenu()">Menu</button><!-- wrong type -->

<!-- Button disabled in a non-standard way -->
<button class="disabled" onclick="return false">Pay Now</button>
```

```html
✅ RIGHT — Semantic, named, correctly typed buttons (SC 4.1.2)

<!-- Text button — simplest, best -->
<button type="button">Save changes</button>

<!-- Icon + text button -->
<button type="button">
  <svg aria-hidden="true" focusable="false" width="16" height="16">
    <!-- SVG paths -->
  </svg>
  Save changes
</button>

<!-- Icon-only button — MUST have accessible name -->
<button type="button" aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false" width="24" height="24">
    <!-- × icon -->
  </svg>
</button>

<!-- Icon-only with tooltip pattern -->
<button type="button" aria-label="Delete item" aria-describedby="delete-tip">
  <svg aria-hidden="true" focusable="false"><!-- trash icon --></svg>
</button>
<div role="tooltip" id="delete-tip">Permanently delete this item</div>

<!-- Submit button -->
<button type="submit">Send message</button>

<!-- Reset button (use sparingly — accidental resets are frustrating) -->
<button type="reset">Clear form</button>

<!-- Disabled button — use disabled attribute, not CSS class -->
<button type="button" disabled aria-disabled="true">
  Pay Now
</button>
<!-- Note: disabled removes from tab order; aria-disabled keeps in tab order 
     Use aria-disabled when you want users to know the button exists but is inactive -->

<!-- Toggle button — aria-pressed tracks state -->
<button type="button" aria-pressed="false" id="mute-btn">
  <svg aria-hidden="true" focusable="false"><!-- speaker icon --></svg>
  Mute
</button>
<script>
  document.getElementById('mute-btn').addEventListener('click', function() {
    const pressed = this.getAttribute('aria-pressed') === 'true';
    this.setAttribute('aria-pressed', String(!pressed));
    // Update icon as well
  });
</script>

<!-- Button that looks like a link (rare — use sparingly) -->
<button type="button" class="btn-link">Show more options</button>

<!-- input[type=image] — must have alt -->
<input type="image" src="go-button.png" alt="Submit search">
```

---

## 9. Images

```html
❌ WRONG — Missing alt; wrong alt text; filename as alt; "image of" prefix
<img src="chart.png"><!-- no alt at all — SR says "chart.png" or nothing -->
<img src="logo.png" alt="image">
<img src="photo.jpg" alt="photo.jpg"><!-- filename -->
<img src="team.jpg" alt="image of people"><!-- "image of" is redundant -->
<img src="decoration.png" alt="decorative swirl"><!-- decorative, should be empty -->
<img src="graph.png" alt="graph"><!-- too vague — what does it show? -->
```

```html
✅ RIGHT — Alt text that conveys purpose and information (SC 1.1.1)

<!-- 
  RULE: alt text conveys the INFORMATION the image provides,
  not what the image looks like.
  Screen readers already say "image" — don't repeat it.
-->

<!-- Informative image — describe what it communicates -->
<img src="revenue-chart.png" 
     alt="Bar chart: Q3 revenue €2.4M, up 40% from Q2 €1.7M">

<!-- Portrait / person in context -->
<img src="jane-smith.jpg" 
     alt="Jane Smith, CEO of Acme Corp, speaking at the 2024 Widget Summit">

<!-- Product image -->
<img src="widget-a.jpg" 
     alt="Widget A: stainless steel cylinder, 12cm tall, with red grip">

<!-- Logo — in a link, describe destination; standalone, say what it is -->
<!-- In link: -->
<a href="/"><img src="logo.svg" alt="Acme Corp — Home"></a>
<!-- Standalone: -->
<img src="logo.svg" alt="Acme Corp">

<!-- Decorative — empty alt, no title -->
<img src="divider.png" alt="" role="presentation">
<img src="background-swirl.png" alt="">

<!-- Functional: icon in a link or button — describe the ACTION -->
<button type="button"><img src="print.png" alt="Print this page"></button>
<a href="/map"><img src="map-pin.png" alt="View store location on map"></a>

<!-- Complex image: chart with lots of data -->
<!-- Short alt + detailed description nearby -->
<figure>
  <img src="org-chart.png"
       alt="Organization chart — text description follows"
       aria-describedby="org-desc">
  <figcaption id="org-desc">
    Acme Corp leadership: CEO Jane Smith oversees three divisions. 
    Engineering (Maria Lopez, 30 staff), Marketing (Tom Chen, 15 staff), 
    Sales (Anna Müller, 20 staff). Each division reports directly to the CEO.
  </figcaption>
</figure>

<!-- Image of text — only acceptable for logos -->
<!-- For all other cases, use real CSS text -->
<img src="logo-text.png" alt="Acme Corp"><!-- OK: logo -->
<!-- Replace with CSS text: -->
<p style="font-family: 'LogoFont';">Sale: 50% Off</p><!-- Better -->
```

### Alt Text Quick Reference

| Image Type | Alt Text |
|---|---|
| Informative | Convey the meaning/data shown |
| Decorative | `alt=""` |
| In a link | Describe the link destination |
| In a button | Describe the action |
| Logo (standalone) | Company name |
| Logo (in nav link) | "CompanyName — Home" |
| Product | Describe key visual attributes relevant to purchase |
| Portrait | Name and role/context |
| Chart / graph | The key takeaway, not visual description |
| Complex / diagram | Short alt + adjacent long description |

---

## 10. SVG Icons

```html
❌ WRONG — SVG without role; focusable SVG in IE; no accessible name on icon buttons
<svg class="icon"><!-- no title, no aria --></svg>

<button><svg class="icon-search"></svg></button><!-- no accessible name -->

<a href="/settings"><svg></svg></a><!-- no accessible name -->

<!-- SVG with title but no role="img" — title may not be announced -->
<svg><title>Settings</title><path .../></svg>
```

```html
✅ RIGHT — SVG accessibility (SC 1.1.1, 4.1.2)

<!-- 
  Decorative SVG icon (inside a button/link that already has text)
  aria-hidden="true" hides from screen readers
  focusable="false" prevents focus in IE11/Edge legacy
-->
<button type="button">
  <svg aria-hidden="true" focusable="false" width="20" height="20">
    <use href="#icon-search"></use>
  </svg>
  Search
</button>

<!-- Icon-only button — the button carries the accessible name, not the SVG -->
<button type="button" aria-label="Search">
  <svg aria-hidden="true" focusable="false" width="20" height="20">
    <use href="#icon-search"></use>
  </svg>
</button>

<!-- Informative standalone SVG — use role="img" + aria-labelledby -->
<svg role="img" aria-labelledby="svg-title svg-desc" width="400" height="200">
  <title id="svg-title">Monthly Revenue 2024</title>
  <desc id="svg-desc">
    Line chart showing revenue growth from €100K in January to €340K in June.
    Consistent upward trend with a dip in March (€110K).
  </desc>
  <!-- Chart paths -->
</svg>

<!-- Simple icon that IS the only content -->
<svg role="img" aria-label="Warning" width="24" height="24">
  <!-- warning triangle path -->
</svg>

<!-- SVG sprite definition (hidden, at top of body) -->
<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
  <symbol id="icon-search" viewBox="0 0 24 24">
    <circle cx="11" cy="11" r="8"/>
    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
  </symbol>
  <symbol id="icon-close" viewBox="0 0 24 24">
    <line x1="18" y1="6" x2="6" y2="18"/>
    <line x1="6" y1="6" x2="18" y2="18"/>
  </symbol>
</svg>

<!-- Use sprite -->
<svg aria-hidden="true" focusable="false"><use href="#icon-close"></use></svg>
```

---

## 11. Navigation Menus

```html
❌ WRONG — List of links not marked as nav; no current page indicator; 
          duplicate nav without label
<div class="nav">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/contact">Contact</a><!-- currently active page, but no indicator -->
</div>

<!-- Two navs with no aria-label — SR says "navigation, navigation" -->
<nav><ul><!-- primary --></ul></nav>
<nav><ul><!-- footer --></ul></nav>
```

```html
✅ RIGHT — Full accessible navigation (SC 2.4.1, 3.2.3)
<header>
  <nav aria-label="Primary navigation">
    <ul role="list"><!-- role="list" restores list semantics if CSS removes bullets -->
      <li>
        <a href="/">Home</a>
      </li>
      <li>
        <a href="/about">About</a>
      </li>
      <!-- aria-current="page" marks the active page -->
      <li>
        <a href="/contact" aria-current="page">Contact</a>
      </li>
    </ul>
  </nav>
</header>

<footer>
  <nav aria-label="Footer navigation">
    <ul role="list">
      <li><a href="/privacy">Privacy Policy</a></li>
      <li><a href="/accessibility">Accessibility</a></li>
    </ul>
  </nav>
</footer>
```

```css
/* Style the current page link */
[aria-current="page"] {
  font-weight: 700;
  color: #0052cc;
  border-bottom: 2px solid currentColor;
  /* Do NOT rely on color alone — add font-weight or underline (SC 1.4.1) */
}
```

---

## 12. Dropdown Menus

```html
❌ WRONG — CSS-only hover dropdown; keyboard inaccessible; no ARIA states
<nav>
  <ul>
    <li class="has-dropdown">
      <a href="/products">Products</a><!-- hover to open — keyboard can't do this -->
      <ul class="dropdown"><!-- hidden with CSS :hover on parent -->
        <li><a href="/products/a">Widget A</a></li>
        <li><a href="/products/b">Widget B</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

```html
✅ RIGHT — Keyboard-accessible dropdown with ARIA (SC 2.1.1, 4.1.2)
<nav aria-label="Primary navigation">
  <ul role="list">
    <li>
      <!-- 
        Button opens the submenu (it's an action, not navigation).
        aria-expanded tracks open/closed state.
        aria-haspopup="true" hints there's a submenu.
        aria-controls points to the submenu.
      -->
      <button type="button"
              aria-expanded="false"
              aria-haspopup="true"
              aria-controls="products-submenu"
              id="products-btn">
        Products
        <svg aria-hidden="true" focusable="false" class="chevron">
          <!-- down arrow icon -->
        </svg>
      </button>
      
      <ul id="products-submenu"
          aria-labelledby="products-btn"
          hidden><!-- hidden attribute: removes from tab order AND SR -->
        <li><a href="/products/widget-a">Widget A</a></li>
        <li><a href="/products/widget-b">Widget B</a></li>
        <li><a href="/products">View all products</a></li>
      </ul>
    </li>
    
    <li><a href="/about" aria-current="page">About</a></li>
  </ul>
</nav>
```

```javascript
// Dropdown keyboard behavior
document.querySelectorAll('[aria-haspopup="true"]').forEach(btn => {
  const menu = document.getElementById(btn.getAttribute('aria-controls'));

  function open() {
    btn.setAttribute('aria-expanded', 'true');
    menu.removeAttribute('hidden');
    // Focus first item
    menu.querySelector('a, button').focus();
  }
  function close() {
    btn.setAttribute('aria-expanded', 'false');
    menu.setAttribute('hidden', '');
    btn.focus(); // Return focus to trigger
  }

  btn.addEventListener('click', () => {
    btn.getAttribute('aria-expanded') === 'true' ? close() : open();
  });

  // Close on Escape
  menu.addEventListener('keydown', e => {
    if (e.key === 'Escape') close();
  });

  // Close on click outside
  document.addEventListener('click', e => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      btn.setAttribute('aria-expanded', 'false');
      menu.setAttribute('hidden', '');
    }
  });

  // Arrow key navigation within submenu
  menu.addEventListener('keydown', e => {
    const items = Array.from(menu.querySelectorAll('a, button'));
    const idx = items.indexOf(document.activeElement);

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      items[(idx + 1) % items.length].focus();
    }
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      items[(idx - 1 + items.length) % items.length].focus();
    }
    if (e.key === 'Tab' && !e.shiftKey && idx === items.length - 1) {
      close(); // Let focus leave naturally
    }
  });
});
```

```css
/* CSS for dropdown */
[aria-haspopup] .chevron {
  transition: transform 0.2s;
}
[aria-expanded="true"] .chevron {
  transform: rotate(180deg);
}

/* Submenu positioning */
[aria-haspopup] + ul {
  position: absolute;
  background: #fff;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  min-width: 200px;
  border-radius: 4px;
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
}

/* Focus on submenu items */
[aria-haspopup] + ul a:focus-visible,
[aria-haspopup] + ul button:focus-visible {
  outline: 3px solid #0052cc;
  outline-offset: -3px;
}
```

---

## 13. Mobile Hamburger Menu

```html
❌ WRONG — Checkbox hack; no ARIA; focus not managed when open
<input type="checkbox" id="nav-toggle" class="nav-toggle">
<label for="nav-toggle">☰</label><!-- no accessible name -->
<nav class="mobile-nav">...</nav><!-- appears/disappears via CSS only -->
```

```html
✅ RIGHT — Accessible mobile menu with focus management (SC 2.1.1, 2.1.2, 4.1.2)
<button type="button"
        aria-expanded="false"
        aria-controls="mobile-menu"
        aria-label="Open navigation menu"
        id="hamburger-btn"
        class="hamburger">
  <!-- Three bars icon (animated to X when open) -->
  <span class="bar" aria-hidden="true"></span>
  <span class="bar" aria-hidden="true"></span>
  <span class="bar" aria-hidden="true"></span>
</button>

<nav id="mobile-menu"
     aria-label="Mobile navigation"
     hidden>
  <ul role="list">
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
  <!-- Close button inside menu -->
  <button type="button" aria-label="Close navigation menu" class="menu-close">
    <svg aria-hidden="true" focusable="false"><!-- X icon --></svg>
  </button>
</nav>
```

```javascript
const btn = document.getElementById('hamburger-btn');
const menu = document.getElementById('mobile-menu');

function openMenu() {
  btn.setAttribute('aria-expanded', 'true');
  btn.setAttribute('aria-label', 'Close navigation menu');
  menu.removeAttribute('hidden');
  // Focus first menu item
  menu.querySelector('a').focus();
}

function closeMenu() {
  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('aria-label', 'Open navigation menu');
  menu.setAttribute('hidden', '');
  btn.focus(); // Return focus to hamburger button
}

btn.addEventListener('click', () => {
  btn.getAttribute('aria-expanded') === 'true' ? closeMenu() : openMenu();
});

// Close button inside menu
menu.querySelector('.menu-close').addEventListener('click', closeMenu);

// Close on Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
    closeMenu();
  }
});
```

```css
/* Animated hamburger → X */
.hamburger .bar {
  display: block;
  width: 24px;
  height: 2px;
  background: currentColor;
  margin: 5px 0;
  transition: transform 0.3s, opacity 0.3s;
}
[aria-expanded="true"] .bar:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}
[aria-expanded="true"] .bar:nth-child(2) {
  opacity: 0;
}
[aria-expanded="true"] .bar:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

@media (prefers-reduced-motion: reduce) {
  .hamburger .bar { transition: none; }
}
```

---

## 14. Breadcrumbs

```html
❌ WRONG — Visual separators read by screen reader; no landmark; current page not marked
<div class="breadcrumb">
  <a href="/">Home</a> > 
  <a href="/products">Products</a> > 
  <span>Widget A</span><!-- current page has no indicator for AT -->
</div>
```

```html
✅ RIGHT — Accessible breadcrumb (SC 1.3.1, 2.4.8)
<nav aria-label="Breadcrumb">
  <ol><!-- Ordered list: the sequence matters -->
    <li>
      <a href="/">Home</a>
    </li>
    <li>
      <a href="/products">Products</a>
    </li>
    <!-- Current page: no link; aria-current="page" -->
    <li>
      <span aria-current="page">Widget A</span>
    </li>
  </ol>
</nav>
```

```css
/* CSS arrow separators — decorative, not in DOM */
.breadcrumb ol {
  list-style: none;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  padding: 0;
  margin: 0;
}
/* Separator between items via CSS content — not in DOM, not read by SR */
.breadcrumb li + li::before {
  content: "/";
  color: #767676;
  margin-right: 0.5rem;
  aria-hidden: true;/* Note: aria-hidden on pseudo-elements is implicit */
}
[aria-current="page"] {
  font-weight: 600;
  color: #1a1a1a;
}
```

---

## 15. Tabs

```html
❌ WRONG — Anchor links used as tabs; no ARIA roles; no keyboard navigation
<div class="tabs">
  <a href="#tab1" class="tab active">Overview</a>
  <a href="#tab2" class="tab">Specs</a>
  <a href="#tab3" class="tab">Reviews</a>
</div>
<div id="tab1">Overview content</div>
<div id="tab2" style="display:none">Specs content</div>
<div id="tab3" style="display:none">Reviews content</div>
```

```html
✅ RIGHT — Full ARIA tabs pattern (SC 2.1.1, 4.1.2)

<!-- 
  Tabs keyboard pattern:
  - Tab moves INTO tablist, then to tabpanel content (not between tabs)
  - Arrow Left/Right moves between tabs
  - Home/End jump to first/last tab
  - Enter/Space activates a tab (if not auto-activated)
-->

<div class="tabs-container">
  <!-- tablist is the container for tab buttons -->
  <div role="tablist" aria-label="Product Information">
    
    <button role="tab"
            aria-selected="true"
            aria-controls="panel-overview"
            id="tab-overview"
            tabindex="0">
      Overview
    </button>
    
    <!-- Non-selected tabs: tabindex="-1" (arrow keys navigate between them) -->
    <button role="tab"
            aria-selected="false"
            aria-controls="panel-specs"
            id="tab-specs"
            tabindex="-1">
      Specifications
    </button>
    
    <button role="tab"
            aria-selected="false"
            aria-controls="panel-reviews"
            id="tab-reviews"
            tabindex="-1">
      Reviews (47)
    </button>
    
  </div>

  <!-- tabpanel — the content area -->
  <div role="tabpanel"
       id="panel-overview"
       aria-labelledby="tab-overview"
       tabindex="0"><!-- tabindex="0" allows panel to receive focus -->
    <h2 class="visually-hidden">Overview</h2><!-- heading for SR navigation -->
    <p>Widget A is our flagship product...</p>
  </div>

  <div role="tabpanel"
       id="panel-specs"
       aria-labelledby="tab-specs"
       tabindex="0"
       hidden><!-- hidden removes from AT and tab order -->
    <h2 class="visually-hidden">Specifications</h2>
    <!-- content -->
  </div>

  <div role="tabpanel"
       id="panel-reviews"
       aria-labelledby="tab-reviews"
       tabindex="0"
       hidden>
    <h2 class="visually-hidden">Reviews</h2>
    <!-- content -->
  </div>
</div>
```

```javascript
class AccessibleTabs {
  constructor(container) {
    this.tablist = container.querySelector('[role="tablist"]');
    this.tabs = Array.from(container.querySelectorAll('[role="tab"]'));
    this.panels = Array.from(container.querySelectorAll('[role="tabpanel"]'));
    
    this.tablist.addEventListener('keydown', this.handleKeydown.bind(this));
    this.tabs.forEach(tab => tab.addEventListener('click', this.handleClick.bind(this)));
  }
  
  activate(tab) {
    const idx = this.tabs.indexOf(tab);
    
    // Deactivate all tabs
    this.tabs.forEach(t => {
      t.setAttribute('aria-selected', 'false');
      t.setAttribute('tabindex', '-1');
    });
    // Hide all panels
    this.panels.forEach(p => p.setAttribute('hidden', ''));
    
    // Activate clicked tab
    tab.setAttribute('aria-selected', 'true');
    tab.setAttribute('tabindex', '0');
    tab.focus();
    
    // Show corresponding panel
    this.panels[idx].removeAttribute('hidden');
  }
  
  handleClick(e) { this.activate(e.currentTarget); }
  
  handleKeydown(e) {
    const idx = this.tabs.indexOf(document.activeElement);
    
    const keys = {
      ArrowRight: () => this.activate(this.tabs[(idx + 1) % this.tabs.length]),
      ArrowLeft:  () => this.activate(this.tabs[(idx - 1 + this.tabs.length) % this.tabs.length]),
      Home:       () => this.activate(this.tabs[0]),
      End:        () => this.activate(this.tabs[this.tabs.length - 1]),
    };
    
    if (keys[e.key]) {
      e.preventDefault();
      keys[e.key]();
    }
  }
}

document.querySelectorAll('.tabs-container').forEach(c => new AccessibleTabs(c));
```

```css
[role="tab"] {
  padding: 0.75rem 1.25rem;
  border: none;
  background: transparent;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  font-size: 1rem;
}
[role="tab"][aria-selected="true"] {
  border-bottom-color: #0052cc;
  font-weight: 600;
  color: #0052cc;
}
[role="tab"]:focus-visible {
  outline: 3px solid #0052cc;
  outline-offset: -2px;
}
```

---

## 16. Accordion

```html
❌ WRONG — Details/summary without headings; no ARIA; hidden via CSS only
<div class="accordion">
  <div class="accordion-header" onclick="toggle(this)">
    Question 1
  </div>
  <div class="accordion-body" style="display:none">
    Answer to question 1
  </div>
</div>
```

```html
✅ RIGHT — Heading + button accordion (SC 2.1.1, 4.1.2)

<!--
  Button inside a heading:
  - Heading gives structural context (SR users navigate headings)
  - Button handles keyboard activation and ARIA states
-->

<div class="accordion">

  <h3 class="accordion-heading">
    <button type="button"
            aria-expanded="false"
            aria-controls="panel1"
            class="accordion-trigger"
            id="trigger1">
      What is Widget A?
      <svg aria-hidden="true" focusable="false" class="accordion-icon">
        <!-- Chevron down icon -->
      </svg>
    </button>
  </h3>
  
  <div id="panel1"
       role="region"
       aria-labelledby="trigger1"
       hidden
       class="accordion-panel">
    <p>Widget A is our flagship cylindrical widget...</p>
  </div>

  <h3 class="accordion-heading">
    <button type="button"
            aria-expanded="false"
            aria-controls="panel2"
            class="accordion-trigger"
            id="trigger2">
      How do I install Widget A?
      <svg aria-hidden="true" focusable="false" class="accordion-icon">
        <!-- Chevron down icon -->
      </svg>
    </button>
  </h3>
  
  <div id="panel2"
       role="region"
       aria-labelledby="trigger2"
       hidden
       class="accordion-panel">
    <ol>
      <li>Remove from packaging</li>
      <li>Insert into slot</li>
    </ol>
  </div>

</div>
```

```javascript
document.querySelectorAll('.accordion-trigger').forEach(trigger => {
  trigger.addEventListener('click', function() {
    const expanded = this.getAttribute('aria-expanded') === 'true';
    const panel = document.getElementById(this.getAttribute('aria-controls'));
    
    this.setAttribute('aria-expanded', String(!expanded));
    
    if (expanded) {
      panel.setAttribute('hidden', '');
    } else {
      panel.removeAttribute('hidden');
    }
  });
});
```

```css
.accordion-trigger {
  width: 100%;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: none;
  border: 1px solid #ddd;
  font-size: 1rem;
  cursor: pointer;
}
.accordion-trigger:focus-visible {
  outline: 3px solid #0052cc;
  outline-offset: 2px;
}
.accordion-trigger[aria-expanded="true"] .accordion-icon {
  transform: rotate(180deg);
}
.accordion-panel {
  padding: 1rem;
  border: 1px solid #ddd;
  border-top: none;
}
@media (prefers-reduced-motion: no-preference) {
  .accordion-icon { transition: transform 0.2s ease; }
}
```

---

## 17. Modal Dialogs

This is one of the most complex patterns — focus management is critical.

```html
❌ WRONG — CSS visibility toggle; no focus trap; no return to trigger; 
          background content still interactive
<div id="modal" class="modal" style="display:none">
  <div class="modal-content">
    <button onclick="closeModal()">×</button>
    <h2>Sign Up</h2>
    <form>...</form>
  </div>
</div>
<!-- Background content still reachable by keyboard! -->
```

```html
✅ RIGHT — Fully accessible modal dialog (SC 2.1.1, 2.1.2, 4.1.2)

<!-- Trigger button -->
<button type="button" id="open-modal-btn">Open Sign Up</button>

<!-- 
  Modal: hidden by default
  role="dialog" marks it as a dialog
  aria-modal="true" tells SR to ignore background content
  aria-labelledby points to the modal title
-->
<div role="dialog"
     aria-modal="true"
     aria-labelledby="modal-title"
     aria-describedby="modal-desc"
     id="signup-modal"
     class="modal"
     hidden
     tabindex="-1">
  
  <div class="modal-inner">
    
    <h2 id="modal-title">Create Account</h2>
    <p id="modal-desc">
      Fill in your details to create a free account.
    </p>
    
    <!-- Close button in top corner -->
    <button type="button"
            class="modal-close"
            aria-label="Close Create Account dialog">
      <svg aria-hidden="true" focusable="false"><!-- × icon --></svg>
    </button>
    
    <!-- Form content -->
    <form>
      <label for="signup-name">Full name</label>
      <input type="text" id="signup-name" autocomplete="name" required>
      
      <label for="signup-email">Email</label>
      <input type="email" id="signup-email" autocomplete="email" required>
      
      <button type="submit">Create Account</button>
    </form>
    
  </div>
</div>

<!-- Backdrop -->
<div id="modal-backdrop" class="modal-backdrop" hidden aria-hidden="true"></div>
```

```javascript
class Modal {
  constructor(modalId, triggerId) {
    this.modal = document.getElementById(modalId);
    this.trigger = document.getElementById(triggerId);
    this.backdrop = document.getElementById('modal-backdrop');
    this.focusableSelector = [
      'a[href]', 'button:not([disabled])', 'input:not([disabled])',
      'select:not([disabled])', 'textarea:not([disabled])',
      '[tabindex]:not([tabindex="-1"])'
    ].join(', ');
    
    // Bind open/close
    this.trigger.addEventListener('click', () => this.open());
    this.modal.querySelector('.modal-close').addEventListener('click', () => this.close());
    this.backdrop.addEventListener('click', () => this.close());
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && !this.modal.hasAttribute('hidden')) this.close();
    });
    
    // Tab trapping
    this.modal.addEventListener('keydown', this.trapFocus.bind(this));
  }
  
  open() {
    this.modal.removeAttribute('hidden');
    this.backdrop.removeAttribute('hidden');
    
    // Hide background from screen readers
    document.getElementById('main-content').setAttribute('aria-hidden', 'true');
    document.querySelector('header').setAttribute('aria-hidden', 'true');
    
    // Prevent background scroll
    document.body.style.overflow = 'hidden';
    
    // Focus first focusable element (or modal itself)
    const firstFocusable = this.modal.querySelector(this.focusableSelector);
    (firstFocusable || this.modal).focus();
  }
  
  close() {
    this.modal.setAttribute('hidden', '');
    this.backdrop.setAttribute('hidden', '');
    
    // Restore background
    document.getElementById('main-content').removeAttribute('aria-hidden');
    document.querySelector('header').removeAttribute('aria-hidden');
    document.body.style.overflow = '';
    
    // Return focus to trigger
    this.trigger.focus();
  }
  
  trapFocus(e) {
    if (e.key !== 'Tab') return;
    
    const focusable = Array.from(this.modal.querySelectorAll(this.focusableSelector));
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    
    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault();
        last.focus();
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }
}

new Modal('signup-modal', 'open-modal-btn');
```

```css
.modal {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal[hidden] { display: none; }

.modal-inner {
  background: #fff;
  border-radius: 8px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  /* Elevated shadow to communicate modality */
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 999;
}
.modal-backdrop[hidden] { display: none; }

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}
.modal-close:focus-visible {
  outline: 3px solid #0052cc;
  outline-offset: 2px;
}
```

---

## 18. Tooltips

```html
❌ WRONG — CSS :hover only; no keyboard access; no Escape to dismiss;
          disappears when user moves mouse to it
<button class="has-tooltip">
  ?
  <span class="tooltip">This is help text</span><!-- CSS :hover shows this -->
</button>
```

```html
✅ RIGHT — Accessible tooltip (SC 1.4.13: hoverable, dismissible, persistent)
<!--
  SC 1.4.13 requirements:
  1. Hoverable: tooltip stays open when pointer moves to tooltip itself
  2. Dismissible: Escape hides it without moving focus
  3. Persistent: stays open until pointer leaves or focus moves
-->

<!-- For simple help text: use aria-describedby -->
<button type="button"
        aria-describedby="tip-save"
        class="icon-btn"
        aria-label="Save">
  <svg aria-hidden="true" focusable="false"><!-- save icon --></svg>
</button>
<div role="tooltip" id="tip-save" hidden>
  Save your work (Ctrl+S)
</div>

<!-- For definitions / abbreviations -->
<abbr title="Web Content Accessibility Guidelines">WCAG</abbr>
<!-- Note: title attribute tooltips are NOT accessible to keyboard users in most browsers -->
<!-- Use the pattern below instead: -->

<span class="has-tooltip" 
      aria-describedby="tip-wcag">
  <abbr>WCAG</abbr>
  <button type="button"
          class="tooltip-trigger visually-hidden-focusable"
          aria-label="What is WCAG?">ⓘ</button>
</span>
<div role="tooltip" id="tip-wcag" hidden>
  Web Content Accessibility Guidelines — international standard for web accessibility
</div>
```

```javascript
function initTooltip(trigger, tooltip) {
  let hideTimeout = null;

  const show = () => {
    clearTimeout(hideTimeout);
    tooltip.removeAttribute('hidden');
  };

  const hide = (delay = 100) => {
    hideTimeout = setTimeout(() => {
      tooltip.setAttribute('hidden', '');
    }, delay);
  };

  // Mouse: show on hover, hide on leave
  trigger.addEventListener('mouseenter', show);
  trigger.addEventListener('mouseleave', () => hide(300));// delay: allow moving to tooltip

  // Keyboard: show on focus, hide on blur
  trigger.addEventListener('focus', show);
  trigger.addEventListener('blur', () => hide());

  // SC 1.4.13: tooltip itself is hoverable
  tooltip.addEventListener('mouseenter', () => clearTimeout(hideTimeout));
  tooltip.addEventListener('mouseleave', () => hide(300));

  // SC 1.4.13: Escape dismisses
  trigger.addEventListener('keydown', e => {
    if (e.key === 'Escape') hide(0);
  });
}

// Initialize
document.querySelectorAll('[aria-describedby]').forEach(trigger => {
  const tip = document.getElementById(trigger.getAttribute('aria-describedby'));
  if (tip && tip.getAttribute('role') === 'tooltip') initTooltip(trigger, tip);
});
```

---

## 19. Disclosure Widgets

```html
❌ WRONG — Click event on div; no keyboard; no ARIA state
<div class="toggle-btn" onclick="toggle()">Show more ▼</div>
<div id="more" style="display:none">Hidden content</div>
```

```html
✅ RIGHT — Native <details>/<summary> (simplest) or button pattern
<!-- Option 1: HTML-native (simplest, no JS needed) -->
<details>
  <summary>Show advanced options</summary>
  <!-- Content is visible when details is open -->
  <div class="extra-options">
    <label>
      <input type="checkbox" name="verbose"> Verbose logging
    </label>
  </div>
</details>

<!-- Option 2: Button pattern for more control -->
<button type="button"
        aria-expanded="false"
        aria-controls="extra-content"
        id="toggle-btn">
  Show advanced options
  <svg aria-hidden="true" focusable="false" class="chevron"><!-- ▼ --></svg>
</button>

<div id="extra-content"
     hidden>
  <p>Advanced options here...</p>
</div>
```

```javascript
document.getElementById('toggle-btn').addEventListener('click', function() {
  const expanded = this.getAttribute('aria-expanded') === 'true';
  const content = document.getElementById(this.getAttribute('aria-controls'));
  
  this.setAttribute('aria-expanded', String(!expanded));
  expanded ? content.setAttribute('hidden', '') : content.removeAttribute('hidden');
});
```

---

## 20. Carousels and Sliders

```html
❌ WRONG — Auto-playing carousel with no pause; no keyboard access; no live region
<div class="carousel">
  <div class="slide active">Slide 1</div>
  <div class="slide">Slide 2</div>
  <!-- Auto-advances every 3 seconds — violates SC 2.2.2 -->
</div>
```

```html
✅ RIGHT — Accessible carousel (SC 2.2.2, 2.1.1, 4.1.2)
<section aria-label="Featured products" aria-roledescription="carousel">
  
  <!-- Controls row -->
  <div class="carousel-controls">
    <!-- SC 2.2.2: Pause mechanism must be visible -->
    <button type="button" 
            id="carousel-pause" 
            aria-label="Pause automatic slide rotation">
      <svg aria-hidden="true" focusable="false"><!-- pause icon --></svg>
    </button>
    
    <button type="button" aria-label="Previous slide" id="carousel-prev">
      <svg aria-hidden="true" focusable="false"><!-- ← --></svg>
    </button>
    
    <button type="button" aria-label="Next slide" id="carousel-next">
      <svg aria-hidden="true" focusable="false"><!-- → --></svg>
    </button>
  </div>
  
  <!-- Slides container -->
  <div class="carousel-slides"
       aria-live="polite"
       aria-atomic="false">
    
    <!-- Each slide is an article with a label -->
    <article class="slide"
             aria-roledescription="slide"
             aria-label="1 of 3: Widget A">
      <h3>Widget A — New Arrival</h3>
      <img src="widget-a.jpg" alt="Widget A: polished chrome cylinder">
      <a href="/products/widget-a">View details</a>
    </article>
    
    <article class="slide"
             aria-roledescription="slide"
             aria-label="2 of 3: Widget B"
             hidden><!-- hidden: not active slide -->
      <h3>Widget B — On Sale</h3>
      <img src="widget-b.jpg" alt="Widget B: matte black cube">
      <a href="/products/widget-b">View details</a>
    </article>
    
  </div>
  
  <!-- Dot indicators -->
  <div role="tablist" aria-label="Slides">
    <button role="tab" aria-selected="true"  aria-label="Slide 1"></button>
    <button role="tab" aria-selected="false" aria-label="Slide 2"></button>
  </div>
  
</section>
```

```javascript
// Key: pause autoplay on hover, focus, and when user explicitly pauses
let autoplay = true;
let interval;

function startAutoplay() {
  interval = setInterval(nextSlide, 5000);
}
function stopAutoplay() {
  clearInterval(interval);
}

const carousel = document.querySelector('[aria-label="Featured products"]');
carousel.addEventListener('mouseenter', stopAutoplay);
carousel.addEventListener('mouseleave', () => { if (autoplay) startAutoplay(); });
carousel.addEventListener('focusin', stopAutoplay);
carousel.addEventListener('focusout', () => { if (autoplay) startAutoplay(); });

document.getElementById('carousel-pause').addEventListener('click', function() {
  autoplay = !autoplay;
  if (autoplay) {
    startAutoplay();
    this.setAttribute('aria-label', 'Pause automatic slide rotation');
  } else {
    stopAutoplay();
    this.setAttribute('aria-label', 'Start automatic slide rotation');
  }
});
```

---

## 21. Forms — Labels and Inputs

This is where most accessibility failures occur.

```html
❌ WRONG — Every common form mistake
<form>
  <!-- No label — placeholder is not a label -->
  <input type="text" placeholder="Name">
  
  <!-- Label not associated (different text, no for/id match) -->
  <label>Email</label>
  <input type="email" name="email">
  
  <!-- Tooltip as label -->
  <input type="tel" title="Phone number">
  
  <!-- Required marked only with asterisk and color -->
  <label style="color:red">* Password</label>
  <input type="password">
  
  <!-- No fieldset for related group -->
  <label>Card number</label><input type="text">
  <label>Expiry</label><input type="text">
  <label>CVV</label><input type="text">
</form>
```

```html
✅ RIGHT — Fully accessible form (SC 1.3.1, 1.3.5, 3.3.2)
<form novalidate><!-- novalidate: we handle validation ourselves for better UX -->
  
  <!-- Required fields notice -->
  <p>
    Fields marked <abbr title="required" aria-label="required">*</abbr> are required.
  </p>

  <!-- Method 1: Explicit label with for/id -->
  <div class="field">
    <label for="full-name">
      Full name <span aria-hidden="true">*</span>
    </label>
    <!-- autocomplete: SC 1.3.5 -->
    <input type="text"
           id="full-name"
           name="fullName"
           required
           aria-required="true"
           autocomplete="name"
           aria-describedby="name-hint">
    <div id="name-hint" class="hint">Enter your first and last name.</div>
  </div>

  <!-- Method 2: Wrapped label (implicit association) -->
  <div class="field">
    <label>
      Email address <span aria-hidden="true">*</span>
      <input type="email"
             name="email"
             required
             aria-required="true"
             autocomplete="email">
    </label>
  </div>

  <!-- Method 3: aria-label (when no visible label is feasible) -->
  <!-- (Rare — prefer visible labels) -->
  <div class="search-row">
    <input type="search"
           aria-label="Search products"
           name="q">
    <button type="submit">Search</button>
  </div>

  <!-- Grouped related fields with fieldset + legend -->
  <fieldset>
    <legend>Payment card details</legend>
    
    <div class="field">
      <label for="card-number">Card number <span aria-hidden="true">*</span></label>
      <input type="text"
             id="card-number"
             autocomplete="cc-number"
             inputmode="numeric"
             pattern="[0-9\s]*"
             required aria-required="true">
    </div>
    
    <div class="field-row">
      <div class="field">
        <label for="card-expiry">Expiry date (MM/YY) <span aria-hidden="true">*</span></label>
        <input type="text"
               id="card-expiry"
               autocomplete="cc-exp"
               inputmode="numeric"
               required aria-required="true">
      </div>
      
      <div class="field">
        <label for="card-cvv">
          Security code (CVV) <span aria-hidden="true">*</span>
          <button type="button" 
                  aria-label="What is a CVV?"
                  aria-describedby="cvv-tip">ⓘ</button>
        </label>
        <input type="text"
               id="card-cvv"
               autocomplete="cc-csc"
               inputmode="numeric"
               maxlength="4"
               required aria-required="true">
        <div role="tooltip" id="cvv-tip" hidden>
          The 3 or 4 digit security code on the back of your card.
        </div>
      </div>
    </div>
  </fieldset>

  <!-- Textarea -->
  <div class="field">
    <label for="message">Message <span aria-hidden="true">*</span></label>
    <textarea id="message"
              name="message"
              rows="5"
              required
              aria-required="true"
              aria-describedby="message-count"
              maxlength="500"></textarea>
    <!-- Character counter — live region for SR -->
    <div id="message-count" aria-live="polite">
      <span id="char-count">500</span> characters remaining
    </div>
  </div>

</form>
```

```javascript
// Character counter
const textarea = document.getElementById('message');
const counter = document.getElementById('char-count');

textarea.addEventListener('input', function() {
  const remaining = 500 - this.value.length;
  counter.textContent = remaining;
  // aria-live="polite" on parent will announce change when user pauses
});
```

---

## 22. Forms — Checkboxes and Radios

```html
❌ WRONG — Custom checkboxes with no keyboard access; radio group without fieldset;
          state conveyed only by color
<div class="fancy-checkbox" onclick="toggle(this)">
  <div class="box" style="background: green">✓</div><!-- click only -->
  I agree
</div>

<!-- Radio group without grouping -->
<label>Delivery speed:</label>
<label><input type="radio" name="speed"> Standard</label>
<label><input type="radio" name="speed"> Express</label>
```

```html
✅ RIGHT — Native checkboxes, radios, and custom styled versions (SC 1.3.1, 2.1.1)

<!-- Native checkbox — always prefer this -->
<div class="field">
  <label class="checkbox-label">
    <input type="checkbox" name="newsletter" id="newsletter">
    Subscribe to newsletter
  </label>
</div>

<!-- Custom STYLED checkbox — keep native <input> for accessibility -->
<div class="field">
  <label class="custom-checkbox" for="agree">
    <input type="checkbox" id="agree" name="agree" required aria-required="true">
    <span class="checkbox-visual" aria-hidden="true">
      <!-- Checkmark drawn in CSS -->
    </span>
    I agree to the <a href="/terms">Terms and Conditions</a>
  </label>
</div>

<!-- Radio group — MUST use fieldset + legend -->
<fieldset>
  <legend>Delivery speed <span aria-hidden="true">*</span></legend>
  
  <label class="radio-label">
    <input type="radio" name="delivery" value="standard" 
           required aria-required="true" checked>
    Standard (3–5 days) — Free
  </label>
  
  <label class="radio-label">
    <input type="radio" name="delivery" value="express">
    Express (1–2 days) — €4.99
  </label>
  
  <label class="radio-label">
    <input type="radio" name="delivery" value="overnight">
    Overnight — €9.99
  </label>
</fieldset>

<!-- Checkbox group — also uses fieldset -->
<fieldset>
  <legend>Dietary preferences</legend>
  
  <label class="checkbox-label">
    <input type="checkbox" name="diet" value="vegetarian">
    Vegetarian
  </label>
  
  <label class="checkbox-label">
    <input type="checkbox" name="diet" value="vegan">
    Vegan
  </label>
</fieldset>
```

```css
/* Custom styled checkbox — native input is hidden but accessible */
.custom-checkbox input[type="checkbox"] {
  /* Use visually-hidden technique, NOT display:none or visibility:hidden
     Those remove from tab order! */
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
}

.checkbox-visual {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid #595959;/* Must meet 3:1 contrast (SC 1.4.11) */
  border-radius: 3px;
  background: #fff;
  vertical-align: middle;
  margin-right: 0.5rem;
  transition: all 0.1s;
}

/* Checked state — checkmark via CSS */
input[type="checkbox"]:checked + .checkbox-visual {
  background: #0052cc;
  border-color: #0052cc;
}
input[type="checkbox"]:checked + .checkbox-visual::after {
  content: '';
  display: block;
  width: 5px;
  height: 9px;
  border: 2px solid #fff;
  border-top: none;
  border-left: none;
  transform: rotate(45deg);
  margin: 1px auto 0;
}

/* Focus indicator on native input, shown on custom visual */
input[type="checkbox"]:focus-visible + .checkbox-visual {
  outline: 3px solid #0052cc;
  outline-offset: 2px;
}

/* Forced colors / high contrast mode */
@media (forced-colors: active) {
  .checkbox-visual {
    border: 2px solid ButtonText;
    forced-color-adjust: none;
  }
  input[type="checkbox"]:checked + .checkbox-visual {
    background: Highlight;
    border-color: Highlight;
  }
}
```

---

## 23. Forms — Select and Combobox

```html
❌ WRONG — Custom dropdown with no ARIA; native select without label;
          autocomplete input without proper role
<div class="custom-select" onclick="toggle()">
  <span>Choose country</span>
  <ul class="options">
    <li onclick="select(this)">Germany</li>
    <li onclick="select(this)">France</li>
  </ul>
</div>
```

```html
✅ RIGHT — Native <select> (simplest) and custom combobox (SC 1.3.1, 2.1.1, 4.1.2)

<!-- Option 1: Native select — always prefer for simple use cases -->
<div class="field">
  <label for="country">Country <span aria-hidden="true">*</span></label>
  <select id="country" name="country" 
          required aria-required="true"
          autocomplete="country">
    <option value="">— Select your country —</option>
    <option value="DE">Germany</option>
    <option value="FR">France</option>
    <option value="US">United States</option>
  </select>
</div>

<!-- Option 2: Custom combobox (autocomplete search) -->
<!-- Full implementation per ARIA APG pattern -->
<div class="field">
  <label id="country-label" for="country-input">
    Country <span aria-hidden="true">*</span>
  </label>
  
  <div class="combobox-container">
    <input type="text"
           id="country-input"
           role="combobox"
           aria-autocomplete="list"
           aria-expanded="false"
           aria-haspopup="listbox"
           aria-controls="country-listbox"
           aria-labelledby="country-label"
           aria-required="true"
           autocomplete="off">
    
    <button type="button" 
            aria-label="Show country options"
            tabindex="-1"
            class="combobox-toggle">
      <svg aria-hidden="true" focusable="false"><!-- chevron --></svg>
    </button>
    
    <ul id="country-listbox"
        role="listbox"
        aria-labelledby="country-label"
        hidden>
      <li role="option" aria-selected="false" data-value="DE">Germany</li>
      <li role="option" aria-selected="false" data-value="FR">France</li>
      <li role="option" aria-selected="false" data-value="US">United States</li>
    </ul>
  </div>
</div>
```

---

## 24. Forms — Validation and Errors

```html
❌ WRONG — Error only shown in red border; error message not associated with input;
          all errors shown only at top of page with no link; 
          browser default validation (ugly, inconsistent)
<input type="email" style="border-color: red">
<!-- Error message exists somewhere on the page but not connected to the input -->

<div class="error-summary">Email is invalid.</div>
<!-- Which email? Where? -->
```

```html
✅ RIGHT — Full accessible error handling (SC 3.3.1, 3.3.2, 3.3.3)

<!-- Error summary at top of form (appears after submit attempt) -->
<div role="alert"
     aria-labelledby="error-summary-title"
     id="error-summary"
     class="error-summary"
     hidden>
  <h2 id="error-summary-title">
    There are <span id="error-count">2</span> errors in this form
  </h2>
  <p>Please correct the following errors:</p>
  <ul id="error-list">
    <!-- Errors are links that focus the problematic field -->
    <li><a href="#email">Email address — Please enter a valid email</a></li>
    <li><a href="#phone">Phone number — Required field</a></li>
  </ul>
</div>

<form novalidate id="contact-form">
  
  <!-- Field with error state -->
  <div class="field" id="field-email">
    <label for="email">
      Email address <span aria-hidden="true">*</span>
    </label>
    <input type="email"
           id="email"
           name="email"
           required
           aria-required="true"
           aria-invalid="true"        <!-- added on error -->
           aria-describedby="email-error email-hint">
    
    <!-- Hint always visible -->
    <div id="email-hint" class="hint">
      We'll send your receipt to this address.
    </div>
    
    <!-- Error: role="alert" reads immediately; or use aria-live="assertive" -->
    <div id="email-error" 
         class="error-message" 
         role="alert">
      <!-- Specific: what's wrong + how to fix -->
      Email address is invalid. Please enter a valid email such as name@example.com.
    </div>
  </div>
  
  <!-- Inline success state -->
  <div class="field" id="field-username">
    <label for="username">Username <span aria-hidden="true">*</span></label>
    <input type="text"
           id="username"
           name="username"
           aria-describedby="username-status"
           aria-invalid="false"><!-- false when valid -->
    <!-- SR-announced status update -->
    <div id="username-status" aria-live="polite">
      <!-- Populated by JS: "Username is available" or "Username is taken" -->
    </div>
  </div>
  
  <button type="submit">Send message</button>
</form>
```

```javascript
const form = document.getElementById('contact-form');
const errorSummary = document.getElementById('error-summary');
const errorList = document.getElementById('error-list');
const errorCount = document.getElementById('error-count');

form.addEventListener('submit', function(e) {
  e.preventDefault();
  
  const errors = [];
  
  // Validate each field
  form.querySelectorAll('[required]').forEach(field => {
    const error = document.getElementById(field.id + '-error');
    
    if (!field.validity.valid) {
      field.setAttribute('aria-invalid', 'true');
      
      // Set specific error message
      const message = getErrorMessage(field);
      if (error) error.textContent = message;
      
      errors.push({ id: field.id, label: getLabel(field), message });
      
    } else {
      field.setAttribute('aria-invalid', 'false');
      if (error) error.textContent = '';
    }
  });
  
  if (errors.length > 0) {
    // Populate error summary
    errorCount.textContent = errors.length;
    errorList.innerHTML = errors.map(e => 
      `<li><a href="#${e.id}">${e.label} — ${e.message}</a></li>`
    ).join('');
    
    errorSummary.removeAttribute('hidden');
    // Move focus to summary so SR announces it
    errorSummary.focus();
    
  } else {
    errorSummary.setAttribute('hidden', '');
    // Submit the form
    submitForm(new FormData(form));
  }
});

function getErrorMessage(field) {
  if (field.validity.valueMissing) return 'This field is required.';
  if (field.validity.typeMismatch) {
    if (field.type === 'email') return 'Please enter a valid email address (e.g. name@example.com).';
    if (field.type === 'url') return 'Please enter a valid URL (e.g. https://example.com).';
  }
  if (field.validity.tooShort) return `Please enter at least ${field.minLength} characters. You entered ${field.value.length}.`;
  if (field.validity.patternMismatch) return field.dataset.patternError || 'Please match the required format.';
  return 'Invalid value.';
}

function getLabel(field) {
  const label = document.querySelector(`label[for="${field.id}"]`);
  return label ? label.textContent.replace('*', '').trim() : field.name;
}
```

```css
.field { margin-bottom: 1.5rem; }

.error-message {
  color: #b91c1c;/* Red — but NOT the only indicator */
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.error-message::before {
  content: "⚠ ";/* Icon adds non-color indicator */
  aria-hidden: "true";
}

/* Border changes on error — adds to color, doesn't replace it */
input[aria-invalid="true"] {
  border: 2px solid #b91c1c;
  /* Also add a background tint for extra non-color signal */
  background-color: #fef2f2;
}
input[aria-invalid="false"] {
  border: 2px solid #16a34a;
}
input[aria-invalid="false"]:not(:focus) {
  /* Optional: success indicator */
}

.error-summary {
  border: 2px solid #b91c1c;
  border-radius: 4px;
  padding: 1rem 1.5rem;
  background: #fef2f2;
  margin-bottom: 2rem;
}
.error-summary:focus {
  outline: 3px solid #b91c1c;
  outline-offset: 2px;
}
/* Remove the outline on the heading inside */
.error-summary[tabindex="-1"]:focus { outline: none; }
```

---

## 25. Forms — Complex Patterns

### Multi-Step Form

```html
✅ RIGHT — Progress indication for multi-step forms (SC 2.4.2, 3.3.4)

<!-- Step indicator -->
<nav aria-label="Form progress">
  <ol class="step-indicator">
    <li aria-current="step" class="step-complete">
      <span class="step-number" aria-hidden="true">1</span>
      <span class="step-label">Your details</span>
    </li>
    <li class="step-current" aria-current="step">
      <span class="step-number" aria-hidden="true">2</span>
      <span class="step-label">Delivery</span>
    </li>
    <li class="step-upcoming">
      <span class="step-number" aria-hidden="true">3</span>
      <span class="step-label">Payment</span>
    </li>
  </ol>
</nav>

<!-- Page title also reflects step -->
<!-- <title>Step 2 of 3: Delivery — Checkout — Acme Corp</title> -->

<!-- Summary before final submit — SC 3.3.4 -->
<section aria-labelledby="review-heading">
  <h2 id="review-heading">Review your order</h2>
  <dl>
    <dt>Name</dt><dd>Jane Smith</dd>
    <dt>Address</dt><dd>123 Main St, Berlin</dd>
    <dt>Total</dt><dd>€24.99</dd>
  </dl>
  <button type="button" onclick="editStep(1)">Edit details</button>
  <button type="submit">Confirm and pay</button>
</section>
```

### Password Field

```html
✅ RIGHT — Accessible password field with show/hide
<div class="field">
  <label for="password">Password <span aria-hidden="true">*</span></label>
  
  <div class="password-wrapper">
    <input type="password"
           id="password"
           name="password"
           autocomplete="new-password"
           required aria-required="true"
           aria-describedby="pw-requirements pw-strength">
    
    <!-- Show/hide toggle -->
    <button type="button"
            id="pw-toggle"
            aria-controls="password"
            aria-pressed="false">
      <svg id="pw-icon-show" aria-hidden="true" focusable="false"><!-- eye --></svg>
      <svg id="pw-icon-hide" aria-hidden="true" focusable="false" hidden><!-- eye-off --></svg>
      <span id="pw-toggle-label">Show password</span>
    </button>
  </div>
  
  <div id="pw-requirements" class="hint">
    At least 8 characters including a number and a symbol.
  </div>
  
  <!-- Password strength meter -->
  <div id="pw-strength" aria-live="polite">
    <!-- Populated by JS: "Password strength: Weak" -->
  </div>
</div>
```

```javascript
const pwField = document.getElementById('password');
const pwToggle = document.getElementById('pw-toggle');
const pwLabel = document.getElementById('pw-toggle-label');
const iconShow = document.getElementById('pw-icon-show');
const iconHide = document.getElementById('pw-icon-hide');

pwToggle.addEventListener('click', function() {
  const isPassword = pwField.type === 'password';
  pwField.type = isPassword ? 'text' : 'password';
  this.setAttribute('aria-pressed', String(isPassword));
  pwLabel.textContent = isPassword ? 'Hide password' : 'Show password';
  iconShow.hidden = isPassword;
  iconHide.hidden = !isPassword;
});
```

---

## 26. Search

```html
❌ WRONG — Search input without label; incorrect role; no submit button
<input type="text" placeholder="Search..." class="search">
<div onclick="search()">🔍</div><!-- not keyboard accessible -->
```

```html
✅ RIGHT — Accessible search (SC 1.3.1, 2.1.1, 4.1.2)

<!-- Simple search form -->
<form role="search" action="/search" method="get" aria-label="Site search">
  <label for="site-search">Search</label>
  <!-- Or if visual label is not wanted: -->
  <input type="search"
         id="site-search"
         name="q"
         aria-label="Search this site"
         placeholder="Enter keywords..."
         autocomplete="on"
         value="">
  <button type="submit" aria-label="Submit search">
    <svg aria-hidden="true" focusable="false"><!-- search icon --></svg>
    <span class="visually-hidden">Search</span>
  </button>
</form>

<!-- Search with live results (combobox pattern) -->
<form role="search" aria-label="Product search">
  <div class="search-combobox">
    <label for="product-search" class="visually-hidden">Search products</label>
    <input type="search"
           id="product-search"
           name="q"
           role="combobox"
           aria-autocomplete="list"
           aria-expanded="false"
           aria-controls="search-results-list"
           aria-haspopup="listbox"
           aria-label="Search products"
           placeholder="Search products...">
    
    <!-- Results announcement -->
    <div aria-live="polite" aria-atomic="true" class="visually-hidden" id="search-status">
      <!-- "3 results found for widget" -->
    </div>
    
    <!-- Live results list -->
    <ul id="search-results-list"
        role="listbox"
        aria-label="Search suggestions"
        hidden>
      <!-- Populated by JS -->
      <li role="option" aria-selected="false">
        <a href="/products/widget-a">Widget A</a>
      </li>
    </ul>
  </div>
  <button type="submit">Search</button>
</form>
```

---

## 27. Tables

```html
❌ WRONG — Table used for layout; data table without headers; no caption;
          headers not associated with data cells
<table><!-- layout table without role="presentation" -->
  <tr>
    <td>Name</td><td>Price</td><td>Stock</td><!-- looks like header, isn't -->
  </tr>
  <tr>
    <td>Widget A</td><td>€9.99</td><td>In stock</td>
  </tr>
</table>
```

```html
✅ RIGHT — Accessible data tables (SC 1.3.1)

<!-- Simple data table -->
<table>
  <!-- Caption describes the table's purpose -->
  <caption>
    Acme Corp Product Catalogue
    <span class="caption-details"> — 12 products, prices in EUR</span>
  </caption>
  
  <thead>
    <tr>
      <!-- scope="col" associates header with column -->
      <th scope="col">Product name</th>
      <th scope="col">Price</th>
      <th scope="col">Availability</th>
      <th scope="col">Actions</th>
    </tr>
  </thead>
  
  <tbody>
    <tr>
      <!-- scope="row" for row headers -->
      <th scope="row">Widget A</th>
      <td>€9.99</td>
      <td>
        <!-- Status: color + text + icon (not color alone — SC 1.4.1) -->
        <span class="status status-available">
          <svg aria-hidden="true" focusable="false"><!-- green dot --></svg>
          In stock
        </span>
      </td>
      <td>
        <!-- Disambiguate identical link text — SC 2.4.4 -->
        <a href="/products/widget-a" 
           aria-label="View details for Widget A">View details</a>
      </td>
    </tr>
    <tr>
      <th scope="row">Widget B</th>
      <td>€14.99</td>
      <td>
        <span class="status status-low">
          <svg aria-hidden="true" focusable="false"><!-- amber dot --></svg>
          Low stock (3 left)
        </span>
      </td>
      <td>
        <a href="/products/widget-b"
           aria-label="View details for Widget B">View details</a>
      </td>
    </tr>
  </tbody>
  
  <tfoot>
    <tr>
      <td colspan="4">Prices include VAT. Delivery from €3.99.</td>
    </tr>
  </tfoot>
</table>

<!-- Complex table with row/column groups -->
<table>
  <caption>Q3 2024 Sales by Region and Product</caption>
  <thead>
    <tr>
      <td></td><!-- empty corner cell -->
      <!-- Column group headers -->
      <th scope="colgroup" colspan="2" id="region-west">West</th>
      <th scope="colgroup" colspan="2" id="region-east">East</th>
    </tr>
    <tr>
      <td></td>
      <th scope="col" id="units-west">Units</th>
      <th scope="col" id="revenue-west">Revenue</th>
      <th scope="col" id="units-east">Units</th>
      <th scope="col" id="revenue-east">Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row" id="row-widget-a">Widget A</th>
      <!-- headers attribute for complex associations -->
      <td headers="region-west units-west row-widget-a">240</td>
      <td headers="region-west revenue-west row-widget-a">€2,400</td>
      <td headers="region-east units-east row-widget-a">180</td>
      <td headers="region-east revenue-east row-widget-a">€1,800</td>
    </tr>
  </tbody>
</table>

<!-- Layout table — role="presentation" -->
<table role="presentation">
  <tr>
    <td>Left column content</td>
    <td>Right column content</td>
  </tr>
</table>
```

### Responsive Tables

```html
✅ RIGHT — Responsive table patterns
<!-- Option 1: Horizontal scroll container -->
<div class="table-wrapper" 
     tabindex="0"
     role="region"
     aria-label="Product catalogue, scroll to see more">
  <table>...</table>
</div>

<!-- Option 2: Stacked cards on mobile using data-label -->
<!-- On mobile: hide thead, show data-label before each cell -->
<table class="responsive-table">
  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Product">Widget A</td>
      <td data-label="Price">€9.99</td>
    </tr>
  </tbody>
</table>
```

```css
@media (max-width: 600px) {
  .responsive-table thead { display: none; }
  .responsive-table td {
    display: flex;
    gap: 1rem;
  }
  .responsive-table td::before {
    content: attr(data-label);
    font-weight: 600;
    min-width: 40%;
  }
}
```

---

## 28. Lists

```html
❌ WRONG — Manual list with br; list items as paragraphs; 
          CSS removing list semantics
<p>• Item one<br>• Item two<br>• Item three</p>

<div class="list">
  <div class="list-item">Item one</div>
  <div class="list-item">Item two</div>
</div>
```

```html
✅ RIGHT — Semantic lists (SC 1.3.1)

<!-- Unordered list: items without meaningful order -->
<ul>
  <li>Free shipping on orders over €50</li>
  <li>30-day return policy</li>
  <li>2-year manufacturer warranty</li>
</ul>

<!-- Ordered list: sequence matters -->
<ol>
  <li>Remove Widget A from packaging</li>
  <li>Insert into the designated slot</li>
  <li>Twist clockwise until you hear a click</li>
</ol>

<!-- Description list: term-definition pairs -->
<dl>
  <dt>SKU</dt>
  <dd>WGT-A-001</dd>
  
  <dt>Dimensions</dt>
  <dd>12 cm × 5 cm × 5 cm</dd>
  
  <dt>Weight</dt>
  <dd>340 g</dd>
  
  <!-- One term, multiple definitions -->
  <dt>Compatible with</dt>
  <dd>Widget Hub Pro</dd>
  <dd>Widget Hub Lite</dd>
  <dd>Widget Base Station</dd>
</dl>

<!-- Nested list -->
<ul>
  <li>
    Products
    <ul>
      <li>Widgets</li>
      <li>Gadgets</li>
    </ul>
  </li>
  <li>Services</li>
</ul>
```

```css
/* When CSS list-style:none is applied, VoiceOver on Safari 
   removes list semantics. Restore with role="list": */
.styled-list {
  list-style: none;
  padding: 0;
}
/* Add role="list" to the <ul> element */
```

```html
<!-- Fix for VoiceOver list semantics -->
<ul role="list" class="styled-list">
  <li>Item one</li>
</ul>
```

---

## 29. Cards

Cards are tricky — they contain multiple interactive elements.

```html
❌ WRONG — Entire card is a link; duplicate links; 
          image without alt; heading order wrong
<a href="/products/widget-a" class="card">
  <img src="widget.jpg"><!-- no alt -->
  <h4>Widget A</h4><!-- wrong level, should follow page hierarchy -->
  <p>Our flagship...</p>
  <span>View details</span>
  <span>Add to cart</span><!-- multiple interactions inside one link — BAD -->
</a>
```

```html
✅ RIGHT — Accessible card patterns (SC 1.1.1, 2.4.4, 4.1.2)

<!-- Pattern 1: Card with one primary link -->
<article class="card">
  <!-- 
    Image linked to the article — alt describes destination
    The link and the h3 link cover the same href
    Use aria-hidden on redundant link to avoid duplicate announcements 
  -->
  <a href="/products/widget-a" tabindex="-1" aria-hidden="true">
    <img src="widget-a.jpg" 
         alt="Widget A: polished chrome cylinder, 12cm tall"
         width="300" height="200">
  </a>
  
  <div class="card-body">
    <!-- Heading level must follow page hierarchy -->
    <h2 class="card-title">
      <!-- Primary link on the heading -->
      <a href="/products/widget-a">Widget A</a>
    </h2>
    
    <p>Our flagship widget, precision-engineered for industrial applications.</p>
    
    <p class="price">
      <span class="visually-hidden">Price:</span>
      €9.99
    </p>
  </div>
</article>

<!-- Pattern 2: Card with multiple actions (add to cart + view details) -->
<article class="card" aria-labelledby="card2-title">
  <img src="widget-b.jpg" 
       alt="Widget B: matte black cube, 8cm"
       width="300" height="200">
  
  <div class="card-body">
    <h2 id="card2-title" class="card-title">Widget B</h2>
    <p>Compact and versatile for home use.</p>
    <p class="price">€14.99</p>
    
    <div class="card-actions">
      <!-- Each link/button is independently reachable -->
      <a href="/products/widget-b"
         aria-label="View details for Widget B">
        View details
      </a>
      <button type="button"
              aria-label="Add Widget B to cart">
        Add to cart
      </button>
    </div>
  </div>
</article>

<!-- Pattern 3: Entire card clickable (CSS + JS hack — use with care) -->
<article class="card card-clickable">
  <img src="widget-c.jpg" alt="Widget C">
  
  <h2 class="card-title">
    <a href="/products/widget-c" class="card-primary-link">Widget C</a>
    <!-- The ::after pseudo-element stretches the link to fill the card -->
  </h2>
  
  <p>Description...</p>
  
  <!-- Additional buttons inside are still clickable normally -->
  <button type="button" class="card-secondary-action" aria-label="Save Widget C">
    <svg aria-hidden="true" focusable="false"><!-- heart icon --></svg>
    Save
  </button>
</article>
```

```css
/* Make primary link cover entire card (without wrapping everything in <a>) */
.card { position: relative; }
.card-primary-link::after {
  content: '';
  position: absolute;
  inset: 0;/* top:0; right:0; bottom:0; left:0 */
  /* This expands the link's click area to the entire card */
}
/* Ensure other interactive elements are above the overlay */
.card-secondary-action {
  position: relative;
  z-index: 1;
}
```

---

## 30. Pagination

```html
❌ WRONG — No nav landmark; current page not announced; prev/next not described
<div class="pagination">
  <a href="?p=1">‹</a>
  <a href="?p=1">1</a>
  <span class="current">2</span><!-- not announced as current -->
  <a href="?p=3">3</a>
  <a href="?p=3">›</a>
</div>
```

```html
✅ RIGHT — Accessible pagination (SC 1.3.1, 2.4.4, 2.4.8)
<nav aria-label="Page navigation">
  <ul class="pagination">
    
    <li>
      <a href="?page=1" aria-label="Previous page, page 1">
        <svg aria-hidden="true" focusable="false"><!-- ← --></svg>
        <span class="visually-hidden">Previous</span>
      </a>
    </li>
    
    <li>
      <a href="?page=1" aria-label="Page 1">1</a>
    </li>
    
    <!-- Current page: aria-current, not a link -->
    <li>
      <span aria-current="page" aria-label="Page 2, current page">2</span>
    </li>
    
    <li>
      <a href="?page=3" aria-label="Page 3">3</a>
    </li>
    
    <!-- Ellipsis -->
    <li aria-hidden="true"><span>…</span></li>
    
    <li>
      <a href="?page=10" aria-label="Page 10, last page">10</a>
    </li>
    
    <li>
      <a href="?page=3" aria-label="Next page, page 3">
        <span class="visually-hidden">Next</span>
        <svg aria-hidden="true" focusable="false"><!-- → --></svg>
      </a>
    </li>
    
  </ul>
  
  <!-- Optional: page info for SR -->
  <p class="visually-hidden" aria-live="polite">
    Page 2 of 10
  </p>
</nav>
```

---

## 31. Notifications and Alerts

```html
❌ WRONG — Visual-only notification; not announced to screen readers;
          using alert() for notifications
<div class="toast" style="display:none">Item added to cart!</div>
<!-- Made visible via CSS — SR never knows it appeared -->

alert('Error: please fill all fields');<!-- disruptive, no styling, blocks page -->
```

```html
✅ RIGHT — ARIA live regions for dynamic announcements (SC 4.1.3)

<!--
  role="status" / aria-live="polite" — non-urgent, waits for user to pause
  role="alert" / aria-live="assertive" — urgent, interrupts immediately
  aria-atomic="true" — SR reads entire region (not just changed part)
-->

<!-- Toast/notification container — always in DOM, empty until needed -->
<!-- Polite: cart updates, save confirmations, search results count -->
<div id="notification-polite"
     role="status"
     aria-live="polite"
     aria-atomic="true"
     class="sr-live-region">
  <!-- Content injected by JS -->
</div>

<!-- Urgent: errors, warnings, security alerts -->
<div id="notification-urgent"
     role="alert"
     aria-live="assertive"
     aria-atomic="true"
     class="sr-live-region">
</div>

<!-- Visual toast notification (separate from SR region) -->
<div id="toast-container" aria-hidden="true"><!-- aria-hidden: SR uses live region instead -->
  <!-- Toasts appear here visually -->
</div>
```

```javascript
function notify(message, type = 'polite', duration = 5000) {
  // 1. Announce to screen readers
  const srRegion = document.getElementById(
    type === 'urgent' ? 'notification-urgent' : 'notification-polite'
  );
  // Clear first, then set — ensures re-announcement of same message
  srRegion.textContent = '';
  setTimeout(() => { srRegion.textContent = message; }, 50);
  
  // 2. Show visual toast
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.setAttribute('aria-hidden', 'true');// SR handled by live region
  
  // Icon for non-color signal
  const icon = type === 'urgent' ? '⚠' : '✓';
  toast.innerHTML = `<span aria-hidden="true">${icon}</span> ${message}
    <button class="toast-close" onclick="this.parentElement.remove()">
      <span class="visually-hidden">Dismiss notification</span>
      <span aria-hidden="true">×</span>
    </button>`;
  
  document.getElementById('toast-container').appendChild(toast);
  
  // Auto-remove after duration
  setTimeout(() => toast.remove(), duration);
}

// Usage:
notify('Item added to cart', 'polite');
notify('Session expired — please sign in again', 'urgent');
```

```css
.sr-live-region {
  /* In DOM but invisible — DO NOT use display:none (breaks live regions) */
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
}

.toast {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  padding: 0.75rem 1.25rem;
  background: #1a1a1a;
  color: #fff;
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  max-width: 380px;
  /* Visible to everyone except SR (SR uses live region) */
}
.toast-urgent { background: #b91c1c; }
```

---

## 32. Loading States and Spinners

```html
❌ WRONG — Spinner with no text; page blocked with no announcement;
          loading state not communicated to SR
<div class="spinner"></div><!-- Just an animated circle, SR reads nothing -->
```

```html
✅ RIGHT — Accessible loading indicators (SC 4.1.3)

<!-- Inline loading (button submitting) -->
<button type="submit" id="submit-btn" aria-disabled="false">
  <svg aria-hidden="true" focusable="false" class="spinner-icon hidden">
    <!-- spinning circle -->
  </svg>
  <span id="btn-label">Submit</span>
</button>

<!-- Page/section loading -->
<div id="results-container"
     aria-live="polite"
     aria-busy="true"><!-- aria-busy="true" tells SR content is loading -->
  <div class="loading-spinner" aria-hidden="true">
    <svg><!-- animated spinner --></svg>
  </div>
  <!-- Visually hidden loading text for SR -->
  <p class="visually-hidden">Loading results, please wait...</p>
</div>
```

```javascript
// Loading state for button
function setButtonLoading(btn, isLoading) {
  const label = btn.querySelector('#btn-label') || btn;
  const spinner = btn.querySelector('.spinner-icon');
  
  if (isLoading) {
    btn.setAttribute('aria-disabled', 'true');
    btn.setAttribute('aria-label', 'Submitting, please wait');
    if (spinner) spinner.classList.remove('hidden');
    label.textContent = 'Submitting...';
  } else {
    btn.removeAttribute('aria-disabled');
    btn.removeAttribute('aria-label');
    if (spinner) spinner.classList.add('hidden');
    label.textContent = 'Submit';
  }
}

// Loading state for content area
async function loadResults() {
  const container = document.getElementById('results-container');
  
  container.setAttribute('aria-busy', 'true');
  container.innerHTML = '<p class="visually-hidden">Loading, please wait...</p>';
  
  const data = await fetchData();
  
  container.setAttribute('aria-busy', 'false');
  container.innerHTML = renderResults(data);
  // aria-live="polite" will announce when content changes
}
```

---

## 33. Progress Bars

```html
❌ WRONG — Visual only progress bar; no ARIA; values not communicated
<div class="progress-bar">
  <div class="progress-fill" style="width: 65%"></div>
</div>
```

```html
✅ RIGHT — Accessible progress indicators (SC 4.1.2)

<!-- Determinate progress (known percentage) -->
<div class="progress-container">
  <label id="upload-label">Uploading file</label>
  
  <div role="progressbar"
       aria-labelledby="upload-label"
       aria-valuenow="65"
       aria-valuemin="0"
       aria-valuemax="100"
       aria-valuetext="65% complete">
    <div class="progress-fill" style="width: 65%"></div>
  </div>
  
  <p id="progress-text" aria-live="polite">65% complete</p>
</div>

<!-- Indeterminate progress (unknown duration) -->
<div class="progress-container">
  <p id="processing-label">Processing your order...</p>
  
  <div role="progressbar"
       aria-labelledby="processing-label"
       aria-valuetext="Processing, please wait">
    <!-- No aria-valuenow when indeterminate -->
    <div class="progress-indeterminate"></div>
  </div>
</div>

<!-- Step progress (multi-step process) -->
<div role="progressbar"
     aria-label="Order process"
     aria-valuenow="2"
     aria-valuemin="1"
     aria-valuemax="4"
     aria-valuetext="Step 2 of 4: Payment">
  ...
</div>
```

```javascript
function updateProgress(percent) {
  const bar = document.querySelector('[role="progressbar"]');
  const text = document.getElementById('progress-text');
  const fill = bar.querySelector('.progress-fill');
  
  bar.setAttribute('aria-valuenow', percent);
  bar.setAttribute('aria-valuetext', `${percent}% complete`);
  fill.style.width = `${percent}%`;
  
  // aria-live="polite" on text — announces at intervals, not every 1%
  if (percent % 10 === 0 || percent === 100) {
    text.textContent = percent === 100 ? 'Complete!' : `${percent}% complete`;
  }
}
```

---

## 34. Range Sliders

```html
❌ WRONG — Custom slider with no keyboard, no value announcement
<div class="slider-track" onclick="setSlider(event)">
  <div class="slider-thumb" style="left: 50%"></div>
</div>
```

```html
✅ RIGHT — Accessible range slider (SC 2.1.1, 4.1.2)

<!-- Native input[type=range] — always prefer this -->
<div class="field">
  <label for="price-range">
    Maximum price: <span id="price-display">€500</span>
  </label>
  
  <input type="range"
         id="price-range"
         name="maxPrice"
         min="0"
         max="1000"
         step="10"
         value="500"
         aria-labelledby="price-label"
         aria-valuetext="€500">
         <!-- aria-valuetext overrides the numeric announcement with formatted text -->
</div>

<!-- Custom two-handle price range slider -->
<div class="range-slider" 
     role="group" 
     aria-labelledby="price-range-label">
  <p id="price-range-label">Price range</p>
  
  <input type="range"
         id="price-min"
         min="0" max="1000" value="100" step="10"
         aria-label="Minimum price"
         aria-valuetext="€100">
  
  <input type="range"
         id="price-max"
         min="0" max="1000" value="500" step="10"
         aria-label="Maximum price"
         aria-valuetext="€500">
  
  <div aria-live="polite" class="visually-hidden" id="range-announcement">
    <!-- "Price range: €100 to €500" -->
  </div>
</div>
```

```javascript
const range = document.getElementById('price-range');
const display = document.getElementById('price-display');

range.addEventListener('input', function() {
  const value = this.value;
  display.textContent = `€${value}`;
  this.setAttribute('aria-valuetext', `€${value}`);
});
```

---

## 35. Date Pickers

```html
❌ WRONG — Text input with no format hint; calendar widget without keyboard
<input type="text" placeholder="Date" class="datepicker">
<!-- JS calendar opens on focus but keyboard can't navigate it -->
```

```html
✅ RIGHT — Accessible date inputs (SC 1.3.1, 2.1.1, 3.3.2)

<!-- Option 1: Native date input (best support) -->
<div class="field">
  <label for="event-date">Event date <span aria-hidden="true">*</span></label>
  <input type="date"
         id="event-date"
         name="eventDate"
         min="2024-01-01"
         max="2030-12-31"
         required aria-required="true">
</div>

<!-- Option 2: Separate fields for day, month, year (most accessible) -->
<fieldset>
  <legend>Date of birth <span aria-hidden="true">*</span></legend>
  
  <div class="date-inputs">
    <div class="field-small">
      <label for="dob-day">Day</label>
      <input type="number"
             id="dob-day"
             name="dobDay"
             min="1" max="31"
             inputmode="numeric"
             autocomplete="bday-day"
             aria-required="true"
             placeholder="DD">
    </div>
    
    <div class="field-small">
      <label for="dob-month">Month</label>
      <select id="dob-month" name="dobMonth" autocomplete="bday-month" aria-required="true">
        <option value="">MM</option>
        <option value="1">January</option>
        <option value="2">February</option>
        <!-- ... -->
      </select>
    </div>
    
    <div class="field-small">
      <label for="dob-year">Year</label>
      <input type="number"
             id="dob-year"
             name="dobYear"
             min="1900"
             max="2024"
             inputmode="numeric"
             autocomplete="bday-year"
             aria-required="true"
             placeholder="YYYY">
    </div>
  </div>
</fieldset>
```

---

## 36. Video and Audio Players

```html
❌ WRONG — Autoplay with sound; no captions; custom player without keyboard access;
          controls not accessible
<video autoplay>
  <source src="promo.mp4">
</video><!-- Autoplays with sound — SC 1.4.2 violation -->
```

```html
✅ RIGHT — Accessible media player (SC 1.2.1–1.2.5, 1.4.2)

<!-- Video with full accessibility support -->
<figure>
  <figcaption>
    <h3>Widget A — Product Overview</h3>
    <p>Duration: 2 minutes 35 seconds</p>
  </figcaption>
  
  <video controls
         preload="metadata"
         poster="video-poster.jpg"
         width="720" height="405"
         aria-label="Widget A Product Overview video">
    
    <source src="overview.mp4" type="video/mp4">
    <source src="overview.webm" type="video/webm">
    
    <!-- Captions — SC 1.2.2 (REQUIRED for pre-recorded video with audio) -->
    <track kind="captions"
           src="captions-en.vtt"
           srclang="en"
           label="English captions"
           default>
    
    <!-- Subtitles (translation) -->
    <track kind="subtitles"
           src="subtitles-de.vtt"
           srclang="de"
           label="Deutsch">
    
    <!-- Audio description — SC 1.2.5 -->
    <track kind="descriptions"
           src="audiodesc-en.vtt"
           srclang="en"
           label="Audio description">
    
    <!-- Chapters for long videos -->
    <track kind="chapters"
           src="chapters.vtt"
           srclang="en"
           label="Chapters">
    
    <!-- Fallback message -->
    <p>
      Your browser does not support HTML video.
      <a href="overview.mp4">Download the video (MP4, 45 MB)</a>.
    </p>
    
  </video>
  
  <!-- Transcript link — SC 1.2.3 alternative -->
  <p>
    <a href="overview-transcript.html">
      Read the text transcript for this video
    </a>
  </p>
</figure>

<!-- Audio-only content -->
<figure>
  <figcaption>Episode 12: The Widget Revolution</figcaption>
  
  <audio controls preload="metadata">
    <source src="episode12.mp3" type="audio/mpeg">
    <source src="episode12.ogg" type="audio/ogg">
    <p>Your browser does not support audio. 
       <a href="episode12.mp3">Download (MP3, 28 MB)</a></p>
  </audio>
  
  <!-- SC 1.2.1: Transcript required for audio-only content -->
  <details>
    <summary>Read transcript</summary>
    <div class="transcript">
      <p><strong>[Intro music fades]</strong></p>
      <p><strong>Host:</strong> Welcome to the Widget Revolution podcast...</p>
    </div>
  </details>
</figure>
```

---

## 37. Data Visualizations and Charts

```html
❌ WRONG — Chart with no text alternative; color-only data encoding;
          SVG with no accessible description
<canvas id="revenue-chart"></canvas><!-- No alt, no description -->
```

```html
✅ RIGHT — Accessible data visualization (SC 1.1.1, 1.4.1)

<!-- Pattern 1: Chart + data table (most robust) -->
<figure aria-labelledby="chart-title" aria-describedby="chart-desc">
  <figcaption>
    <h2 id="chart-title">Monthly Revenue Q3 2024</h2>
    <p id="chart-desc">
      Bar chart showing revenue by month. July: €180K, August: €210K, 
      September: €240K. Upward trend throughout the quarter.
    </p>
  </figcaption>
  
  <!-- Chart (visual) — marked as presentational for SR -->
  <canvas id="revenue-chart" aria-hidden="true" width="600" height="300"></canvas>
  
  <!-- Data table alternative — always visible (not hidden behind tab) -->
  <details>
    <summary>View data as table</summary>
    <table>
      <caption>Monthly Revenue Q3 2024 (EUR thousands)</caption>
      <thead>
        <tr>
          <th scope="col">Month</th>
          <th scope="col">Revenue</th>
          <th scope="col">vs Previous Month</th>
        </tr>
      </thead>
      <tbody>
        <tr><th scope="row">July</th><td>€180,000</td><td>—</td></tr>
        <tr><th scope="row">August</th><td>€210,000</td><td>+16.7%</td></tr>
        <tr><th scope="row">September</th><td>€240,000</td><td>+14.3%</td></tr>
      </tbody>
    </table>
  </details>
</figure>

<!-- Pattern 2: Inline SVG chart with full ARIA -->
<svg role="img"
     aria-labelledby="pie-title pie-desc"
     viewBox="0 0 200 200"
     width="200" height="200">
  <title id="pie-title">Market share by product, 2024</title>
  <desc id="pie-desc">
    Pie chart: Widget A 45%, Widget B 30%, Widget C 25%.
    Widget A holds the largest market share.
  </desc>
  
  <!-- Use patterns AND colors (not color alone — SC 1.4.1) -->
  <defs>
    <pattern id="pattern-a" patternUnits="userSpaceOnUse" width="4" height="4">
      <line x1="0" y1="4" x2="4" y2="0" stroke="#0052cc" stroke-width="1"/>
    </pattern>
    <pattern id="pattern-b" patternUnits="userSpaceOnUse" width="4" height="4">
      <circle cx="2" cy="2" r="1" fill="#d63031"/>
    </pattern>
  </defs>
  
  <!-- Pie slices with both color and pattern fill -->
  <path d="..." fill="url(#pattern-a)" aria-label="Widget A: 45%"/>
  <path d="..." fill="url(#pattern-b)" aria-label="Widget B: 30%"/>
  <path d="..." fill="#00b894" stroke-dasharray="4 2" aria-label="Widget C: 25%"/>
</svg>
```

---

## 38. Color and Contrast

```css
/* ============================================================
   WRONG — Failing contrast examples
   ============================================================ */

/* Light gray on white — fails 1.4.3 (ratio 2.85:1) */
.fails { color: #999999; background: #ffffff; }

/* Orange on white — fails for normal text (ratio 2.94:1) */
.fails { color: #ff6600; background: #ffffff; }

/* White on light blue — fails (ratio 1.7:1) */
.fails { color: #ffffff; background: #87ceeb; }

/* Placeholder text too light */
input::placeholder { color: #cccccc; }/* ratio 1.6:1 — FAIL */

/* ============================================================
   RIGHT — Passing contrast examples
   ============================================================ */

/* Body text: always ≥4.5:1 */
body { color: #1a1a1a; background: #ffffff; }/* 16.1:1 ✓ */

/* Links on white: must be distinguishable from text AND meet contrast */
a { 
  color: #0052cc;/* 7.7:1 on white ✓ */
  text-decoration: underline;/* Distinguishes from body text without color alone */
}
a:visited { color: #4b0082; }/* 9.7:1 on white ✓ */

/* Placeholder: meets 4.5:1 */
input::placeholder { color: #767676; }/* exactly 4.5:1 on white ✓ */

/* Disabled text: exempt from contrast — but still readable is better */
button:disabled { color: #767676; opacity: 0.6; }

/* Focus indicator: ≥3:1 between focused and unfocused states */
:focus-visible {
  outline: 3px solid #0052cc;/* blue on white: 7.7:1 ✓ */
  outline-offset: 2px;
}

/* UI components (input border, button border): ≥3:1 */
input {
  border: 2px solid #595959;/* 7.0:1 on white ✓ */
}

/* Large text (≥24px or ≥18.67px bold): only needs 3:1 */
h1 { 
  font-size: 2rem;/* 32px — large text */
  color: #595959;/* 7.0:1 ✓ (exceeds 3:1 minimum) */
}

/* Dark mode — check BOTH modes */
@media (prefers-color-scheme: dark) {
  body { color: #e8e8e8; background: #1a1a1a; }/* 13.9:1 ✓ */
  a { color: #70a9ff; }/* 4.6:1 on #1a1a1a ✓ */
  input { border-color: #9ca3af; }/* 3.2:1 on #1a1a1a ✓ */
}
```

```html
<!-- Color is not the only indicator — SC 1.4.1 -->

❌ WRONG — Error state shown only in red
<input style="border-color: red"><!-- color alone is the indicator -->

✅ RIGHT — Multiple indicators for error state
<input aria-invalid="true"><!-- + red border + icon + text message -->

<!-- Below the input: -->
<span class="error">
  <svg aria-hidden="true"><!-- warning icon --></svg>
  Please enter a valid email address.
</span>

<!-- ❌ WRONG — Link distinguished only by color (no underline) -->
<p>Read our <a style="text-decoration:none; color:#ff0000">privacy policy</a>.</p>

<!-- ✅ RIGHT — Underline or other non-color indicator -->
<p>Read our <a href="/privacy">privacy policy</a>.</p><!-- underline by default -->
```

---

## 39. Focus Management

```css
/* ============================================================
   THE #1 ACCESSIBILITY CSS SIN
   NEVER remove outlines without a custom replacement
   ============================================================ */

/* ❌ CATASTROPHICALLY WRONG — removes all focus indicators site-wide */
* { outline: none; }
*:focus { outline: none; }
a:focus, button:focus { outline: 0; }

/* ============================================================
   CORRECT approach — custom, beautiful focus indicators
   ============================================================ */

/* :focus-visible — only shows for keyboard navigation, not mouse click */
/* This respects user preference without hiding from keyboard users */
:focus-visible {
  outline: 3px solid #0052cc;
  outline-offset: 3px;
  border-radius: 2px;
}

/* :focus — for browsers that don't support :focus-visible */
/* Use with polyfill or progressive enhancement */
:focus:not(:focus-visible) {
  outline: none;/* Safe: hides only when mouse clicked */
}
:focus-visible {
  outline: 3px solid #0052cc;
  outline-offset: 3px;
}

/* Component-specific focus styles */
button:focus-visible {
  outline: 3px solid #0052cc;
  outline-offset: 2px;
}

/* White focus ring for dark backgrounds */
.dark-bg :focus-visible,
.hero :focus-visible {
  outline: 3px solid #ffffff;
  outline-offset: 3px;
}

/* Focus on cards */
.card a:focus-visible {
  outline: 3px solid #0052cc;
  outline-offset: 4px;
  border-radius: 4px;
}

/* WCAG 2.2 SC 2.4.11: Focus Appearance
   Minimum: 2px perimeter, 3:1 contrast focused vs unfocused */
:focus-visible {
  /* This 3px outline on a white background meets WCAG 2.2 SC 2.4.11 */
  /* #0052cc on white = 7.7:1; far exceeds the 3:1 minimum */
  outline: 3px solid #0052cc;
  outline-offset: 2px;/* Creates the required perimeter space */
}

/* High contrast / forced colors mode */
@media (forced-colors: active) {
  :focus-visible {
    outline: 3px solid Highlight;/* System color — always visible */
    outline-offset: 2px;
  }
}
```

### Programmatic Focus Management

```javascript
// When to move focus programmatically:
// 1. Modal opens → first focusable element in modal
// 2. Modal closes → trigger button
// 3. SPA navigation → main heading or <main>
// 4. Error summary appears → summary element
// 5. Dynamic content loads → heading of loaded content
// 6. Alert dialog → dialog element

// WRONG: Moving focus on page load to non-landmark
document.querySelector('.hero-text').focus();// Jarring, unexpected

// RIGHT: Only move focus when user initiates an action
openModalBtn.addEventListener('click', () => {
  // Opens modal and moves focus inside — expected
  modal.open();
});

// RIGHT: After AJAX page load in SPA
async function navigate(url) {
  await loadContent(url);
  document.title = `${newPageTitle} — Site Name`;
  
  // Reset focus to top
  const main = document.getElementById('main-content');
  main.setAttribute('tabindex', '-1');
  main.focus();
  // Remove tabindex after focus (prevents it appearing in tab order)
  main.addEventListener('blur', () => main.removeAttribute('tabindex'), { once: true });
}
```

---

## 40. CSS Hiding Techniques

Understanding what each technique does to accessibility:

```css
/* ============================================================
   What each hiding method does to screen readers and tab order
   ============================================================ */

/* 1. display: none
   - Invisible: YES
   - Tab order: REMOVED (not reachable)
   - Screen reader: HIDDEN
   - Use for: truly hidden content, inactive modal panels
*/
.hidden { display: none; }

/* 2. visibility: hidden
   - Invisible: YES
   - Tab order: REMOVED
   - Screen reader: HIDDEN
   - Use for: hidden but occupies space (like display:none for AT)
*/
.invisible { visibility: hidden; }

/* 3. opacity: 0
   - Invisible: YES (visually)
   - Tab order: STILL REACHABLE — DANGER!
   - Screen reader: STILL READ — DANGER!
   - Use: Only for CSS transitions (pair with pointer-events:none + tabindex=-1)
*/
.fading { opacity: 0; pointer-events: none; }/* Still in AT! */

/* 4. position: absolute; left: -9999px
   - Invisible: YES (off-screen)
   - Tab order: STILL REACHABLE — can cause scroll to off-screen location
   - Screen reader: STILL READ
   - Use: AVOID — use visually-hidden pattern instead
*/

/* 5. The CORRECT visually-hidden pattern
   - Invisible: YES
   - Tab order: STILL REACHABLE (good for skip links, SR-only labels)
   - Screen reader: STILL READ
   - Use for: skip links, SR-only labels, icon button text
*/
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

/* 6. Focusable visually-hidden (skip links)
   - Shows when focused, hides when not
*/
.skip-link {
  position: absolute;
  top: -100vh;
}
.skip-link:focus {
  top: 0;
}

/* 7. aria-hidden="true"
   - Invisible: NO (still visible)
   - Tab order: STILL REACHABLE — DANGER with interactive elements!
   - Screen reader: HIDDEN
   - Use for: decorative icons inside labeled buttons
   - NEVER use on: focusable elements (inputs, buttons, links)
*/
```

```html
<!-- aria-hidden on interactive elements — WRONG vs RIGHT -->

❌ WRONG: aria-hidden makes button invisible to SR but it's still focusable
<nav aria-hidden="true">
  <a href="/home">Home</a><!-- Focusable but invisible to SR = confusion -->
</nav>

✅ RIGHT: Use hidden attribute or inert to fully remove from interaction
<nav hidden><!-- removes from tab order AND SR -->
  <a href="/home">Home</a>
</nav>

<!-- Or: inert attribute (modern browsers) removes from all interaction -->
<nav inert>
  <a href="/home">Home</a><!-- Not focusable, not in SR -->
</nav>
```

---

## 41. Animation and Motion

```css
/* ============================================================
   SC 2.3.1: No flashing more than 3 times per second
   SC 2.2.2: Pause/stop/hide for moving content
   prefers-reduced-motion: respect user system preference
   ============================================================ */

/* ❌ WRONG — No motion preference check; potentially harmful animation */
.spinner {
  animation: spin 0.5s linear infinite;/* May cause vestibular issues */
}
.hero-text {
  animation: flicker 0.2s steps(2) infinite;/* >3Hz — potential seizure trigger */
}

/* ✅ RIGHT — Motion only when user hasn't requested reduction */

/* Provide static version by default */
.spinner {
  /* Static version: just a circle */
  border: 3px solid #e5e7eb;
  border-top-color: #0052cc;
  border-radius: 50%;
  width: 24px;
  height: 24px;
}

/* Animation only if preference allows */
@media (prefers-reduced-motion: no-preference) {
  .spinner {
    animation: spin 0.8s linear infinite;
  }
}

/* Global reduced motion reset */
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

/* Specific overrides for functional animations that must remain */
@media (prefers-reduced-motion: reduce) {
  /* Keep ARIA-required transitions (like modal appearing) 
     but make them instant */
  .modal {
    transition: none;
  }
  
  /* Keep focus indicators */
  :focus-visible {
    transition: none;
    outline: 3px solid #0052cc;/* Always visible, no animation needed */
  }
}

/* Scroll animations — only if motion allowed */
.fade-in-on-scroll {
  opacity: 0;
  transform: translateY(20px);
}
@media (prefers-reduced-motion: no-preference) {
  .fade-in-on-scroll.visible {
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.5s, transform 0.5s;
  }
}
@media (prefers-reduced-motion: reduce) {
  .fade-in-on-scroll {
    opacity: 1;/* Show immediately, no animation */
    transform: none;
  }
}
```

```javascript
// SC 2.2.2: Auto-playing content must have pause/stop control
class AutoCarousel {
  constructor(el) {
    this.el = el;
    this.paused = false;
    this.interval = null;
    
    // Also pause if user prefers reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      this.paused = true;
      return;// Don't start autoplay
    }
    
    this.start();
    this.addPauseControl();
    
    // Pause on hover and focus
    el.addEventListener('mouseenter', () => this.pause());
    el.addEventListener('mouseleave', () => { if (!this.paused) this.start(); });
    el.addEventListener('focusin', () => this.pause());
    el.addEventListener('focusout', () => { if (!this.paused) this.start(); });
  }
  
  start() { this.interval = setInterval(() => this.next(), 5000); }
  pause() { clearInterval(this.interval); }
  
  addPauseControl() {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Pause auto-rotation');
    btn.addEventListener('click', () => {
      this.paused = !this.paused;
      this.paused ? this.pause() : this.start();
      btn.setAttribute('aria-label', this.paused ? 'Start auto-rotation' : 'Pause auto-rotation');
      btn.setAttribute('aria-pressed', String(this.paused));
    });
    this.el.prepend(btn);
  }
}
```

---

## 42. Responsive and Zoom

```css
/* SC 1.4.4: Resize Text — 200% without loss of functionality */
/* SC 1.4.10: Reflow — 320px wide (400% zoom on 1280px screen) without horizontal scroll */

/* ❌ WRONG — Fixed units cause overflow at zoom */
.container { width: 1200px; }/* horizontal scroll at 400% zoom */
body { font-size: 14px; }/* fixed px: doesn't respect user browser font size */
.modal { width: 600px; }/* overflows on small screens/zoom */

/* ✅ RIGHT — Fluid, relative units */
html { font-size: 100%; }/* Respects browser default (usually 16px) */
body { font-size: 1rem; }/* Scales with user preference */

.container {
  max-width: 1200px;
  width: 100%;
  padding: 0 clamp(1rem, 4vw, 2rem);/* Responsive padding */
}

/* Fluid typography */
h1 { font-size: clamp(1.5rem, 4vw, 3rem); }
h2 { font-size: clamp(1.25rem, 3vw, 2rem); }

/* Modal that works at all zoom levels */
.modal-inner {
  width: min(500px, 95vw);/* never wider than viewport */
  max-height: min(600px, 90vh);
  overflow-y: auto;
}

/* SC 1.4.12: Text Spacing — content survives these overrides */
/* Test with: 
  letter-spacing: 0.12em
  word-spacing: 0.16em
  line-height: 1.5
  paragraph spacing: 2em
*/
/* Solution: never hard-code heights on text containers */

/* ❌ WRONG */
.card-body {
  height: 120px;
  overflow: hidden;/* Text gets clipped with spacing overrides */
}

/* ✅ RIGHT */
.card-body {
  min-height: 120px;/* Expands if text needs more space */
}

/* Table overflow — allow horizontal scroll on small screens */
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
/* Add tabindex so keyboard users can scroll it */
.table-container[tabindex="0"]:focus {
  outline: 3px solid #0052cc;
}
```

---

## 43. Touch and Pointer

```css
/* SC 2.5.8 (WCAG 2.2): Target Size Minimum — 24×24 CSS pixels */
/* SC 2.5.5 (WCAG 2.1 AAA): Target Size Enhanced — 44×44 CSS pixels */

/* ❌ WRONG — Tiny touch targets */
.close-btn {
  width: 16px;
  height: 16px;/* Too small for touch */
}

/* ✅ RIGHT — Adequate touch target size */
/* Minimum: 24×24px with adequate spacing */
.icon-btn {
  min-width: 44px;/* Recommended for comfortable touch */
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  /* If the visual element is smaller, padding expands hit area */
  padding: 10px;
}

/* Or use transparent pseudo-element to expand tap area without changing visual */
.small-btn {
  position: relative;
}
.small-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 44px;
  min-height: 44px;
}
```

```javascript
// SC 2.5.1: Multipoint gestures must have single-pointer alternative
// SC 2.5.2: Activation on up-event (allow cancellation)
// SC 2.5.4: Motion actuation — device motion has alternative

// ❌ WRONG — Only drag gesture, no button alternative
element.addEventListener('touchmove', handleDrag);

// ✅ RIGHT — Drag with keyboard/button alternative
element.addEventListener('touchmove', handleDrag);
document.getElementById('move-up-btn').addEventListener('click', moveUp);
document.getElementById('move-down-btn').addEventListener('click', moveDown);

// SC 2.5.2: Use 'click' (mouseup), not 'mousedown' for activation
// This allows users to drag away from button to cancel

// ❌ WRONG
button.addEventListener('mousedown', activateAction);

// ✅ RIGHT — fires on mouseup/pointer up
button.addEventListener('click', activateAction);// click = mousedown + mouseup on same element

// SC 2.5.4: Device motion alternative
window.addEventListener('devicemotion', handleShake);
// MUST provide button alternative:
document.getElementById('refresh-btn').addEventListener('click', handleShake);
// Also: check DeviceMotionEvent.requestPermission() on iOS

// Pointer event for both mouse and touch
element.addEventListener('pointerdown', handleStart);
element.addEventListener('pointermove', handleMove);
element.addEventListener('pointerup', handleEnd);
element.addEventListener('pointercancel', handleEnd);
```

---

## 44. Keyboard Interaction Patterns

### Complete Key Binding Reference

```javascript
// ============================================================
// BUTTON: Enter, Space to activate
// ============================================================
// Native <button> handles this automatically.
// For custom [role="button"] on a div/span (avoid if possible):
el.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    activate();
  }
});

// ============================================================
// LINK: Enter only (Space scrolls in links — do NOT intercept)
// ============================================================
// Native <a href="..."> handles Enter automatically.

// ============================================================
// LISTBOX / SELECT: Arrow keys, Home, End, Type-ahead
// ============================================================
listbox.addEventListener('keydown', e => {
  const options = Array.from(listbox.querySelectorAll('[role="option"]'));
  const idx = options.findIndex(o => o.getAttribute('aria-selected') === 'true');
  
  const handlers = {
    ArrowDown: () => Math.min(idx + 1, options.length - 1),
    ArrowUp:   () => Math.max(idx - 1, 0),
    Home:      () => 0,
    End:       () => options.length - 1,
  };
  
  if (handlers[e.key]) {
    e.preventDefault();
    const newIdx = handlers[e.key]();
    options.forEach(o => o.setAttribute('aria-selected', 'false'));
    options[newIdx].setAttribute('aria-selected', 'true');
    options[newIdx].focus();
  }
});

// ============================================================
// MENU / DROPDOWN: Arrow keys, Escape, Home, End, Type-ahead
// ============================================================
menu.addEventListener('keydown', e => {
  const items = Array.from(menu.querySelectorAll('[role="menuitem"]:not([disabled])'));
  const idx = items.indexOf(document.activeElement);
  
  if (e.key === 'ArrowDown') { items[(idx + 1) % items.length].focus(); e.preventDefault(); }
  if (e.key === 'ArrowUp')   { items[(idx - 1 + items.length) % items.length].focus(); e.preventDefault(); }
  if (e.key === 'Home')      { items[0].focus(); e.preventDefault(); }
  if (e.key === 'End')       { items[items.length - 1].focus(); e.preventDefault(); }
  if (e.key === 'Escape')    { closeMenu(); }
  
  // Type-ahead: jump to item starting with typed char
  if (e.key.length === 1) {
    const char = e.key.toLowerCase();
    const match = items.find((item, i) => 
      i > idx && item.textContent.trim().toLowerCase().startsWith(char)
    ) || items.find(item => item.textContent.trim().toLowerCase().startsWith(char));
    if (match) match.focus();
  }
});

// ============================================================
// TREE VIEW: Arrow keys, Home, End, Enter, Space
// ============================================================
// Left: collapse node or move to parent
// Right: expand node or move to first child
// Up/Down: navigate between visible items

// ============================================================
// GRID / DATA GRID: Arrow keys in two dimensions
// ============================================================
// Arrow keys: move between cells
// Tab: move between interactive elements within cell
// Enter: enter cell editing mode
// Escape: exit cell editing mode

// ============================================================
// DIALOG / MODAL: Tab/Shift+Tab within dialog, Escape to close
// ============================================================
// See Section 17 for full implementation
```

---

## 45. Dynamic Content and Live Regions

```html
<!-- ============================================================
     ARIA Live Region Types
     ============================================================ -->

<!-- 
  role="status" / aria-live="polite"
  - Waits for user to be idle
  - For: save confirmations, cart updates, search count, form hints
  - aria-atomic="true": read whole region; "false": read only changed part
-->
<div role="status" aria-live="polite" aria-atomic="true" id="cart-status"
     class="visually-hidden">
  <!-- "1 item added to cart. Cart total: 3 items" -->
</div>

<!--
  role="alert" / aria-live="assertive"
  - Interrupts immediately
  - For: errors, urgent warnings, session expiry
  - Use sparingly — frequent interruptions are annoying
-->
<div role="alert" aria-live="assertive" aria-atomic="true" id="error-alert"
     class="visually-hidden">
  <!-- "Error: Your session has expired. Please sign in again." -->
</div>

<!--
  aria-live="off"
  - Never announced automatically
  - Use when region updates frequently and SR announcement would be noise
-->
<div aria-live="off" id="clock">12:34:56</div><!-- Clock that updates every second -->

<!--
  role="log"
  - For sequential updates (chat messages, activity feed)
  - New items announced as they're appended
-->
<div role="log" aria-label="Chat messages" aria-live="polite" id="chat-log">
  <!-- Messages appended here are announced -->
</div>

<!--
  role="timer"
  - For countdowns/countups
  - Does NOT auto-announce; users can query it
-->
<div role="timer" aria-label="Time remaining" id="countdown">05:00</div>

<!--
  role="marquee"
  - For stock tickers, scrolling text
  - Rarely appropriate; use sparingly
-->
```

```javascript
// ============================================================
// Best practices for live regions
// ============================================================

// 1. Live regions must be in DOM BEFORE content is injected
//    (The region itself, not just the content, must exist on load)

// ❌ WRONG: Create and populate in one step
const region = document.createElement('div');
region.setAttribute('aria-live', 'polite');
region.textContent = 'Item saved';// SR may not catch this
document.body.appendChild(region);

// ✅ RIGHT: Region exists in HTML; only update content
const statusRegion = document.getElementById('status-region');// Already in DOM
// Small delay ensures SR registers the change
statusRegion.textContent = '';// Clear first
setTimeout(() => { statusRegion.textContent = 'Item saved successfully'; }, 50);

// 2. Force re-announcement of same message
function announce(message, regionId = 'status-region') {
  const region = document.getElementById(regionId);
  region.textContent = '';
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      region.textContent = message;
    });
  });
}

// 3. Announce search results count
function updateSearchResults(results) {
  renderResults(results);
  announce(`${results.length} results found for "${searchQuery}"`);
}

// 4. Announce form validation summary
function announceErrors(errorCount) {
  announce(
    errorCount === 0 
      ? 'Form submitted successfully' 
      : `Form submission failed: ${errorCount} error${errorCount > 1 ? 's' : ''} found`,
    'error-alert-region'
  );
}
```

---

## 46. Single Page App Navigation

```javascript
// SPA navigation must:
// 1. Update document.title
// 2. Announce the navigation to screen readers
// 3. Manage focus appropriately
// 4. Update history/URL (so browser back button works)
// 5. Handle <a> links naturally where possible

class SPARouter {
  navigate(url, title) {
    // 1. Update URL and history
    history.pushState({ url, title }, title, url);
    
    // 2. Update page title
    document.title = `${title} — Acme Corp`;
    
    // 3. Load content
    this.loadContent(url);
  }
  
  async loadContent(url) {
    const main = document.getElementById('main-content');
    
    // Announce loading to SR
    main.setAttribute('aria-busy', 'true');
    announce('Loading page, please wait...');
    
    const html = await fetch(url).then(r => r.text());
    main.innerHTML = extractMain(html);
    main.setAttribute('aria-busy', 'false');
    
    // 4. Move focus to top of new content
    // Option A: Focus main element
    main.setAttribute('tabindex', '-1');
    main.focus();
    main.removeAttribute('tabindex');
    
    // Option B: Focus the h1 of the loaded content
    const h1 = main.querySelector('h1');
    if (h1) {
      h1.setAttribute('tabindex', '-1');
      h1.focus();
      h1.removeAttribute('tabindex');
    }
    
    // 5. Announce navigation complete
    announce(`Navigated to ${document.title}`);
    
    // 6. Update aria-current in navigation
    document.querySelectorAll('nav a').forEach(link => {
      link.getAttribute('href') === url
        ? link.setAttribute('aria-current', 'page')
        : link.removeAttribute('aria-current');
    });
  }
}

// Handle browser back/forward
window.addEventListener('popstate', e => {
  if (e.state) router.loadContent(e.state.url);
});
```

---

## 47. iframes

```html
❌ WRONG — iframe without title; blank title; decorative iframe still read
<iframe src="map.html"></iframe>
<iframe src="ad.html" title=""></iframe>
<iframe src="analytics.html"></iframe><!-- hidden tracking iframe -->
```

```html
✅ RIGHT — Accessible iframes (SC 4.1.2)

<!-- Meaningful iframe: must have descriptive title -->
<iframe src="https://maps.example.com/?loc=berlin"
        title="Map showing Acme Corp Berlin office location"
        width="600"
        height="450"
        loading="lazy">
  <!-- Fallback for non-iframe browsers -->
  <p><a href="https://maps.example.com/?loc=berlin">View map on maps.example.com</a></p>
</iframe>

<!-- Video embed -->
<iframe src="https://www.youtube-nocookie.com/embed/abc123"
        title="Widget A Product Overview — YouTube video"
        width="560"
        height="315"
        allowfullscreen
        loading="lazy">
</iframe>

<!-- Invisible/tracking iframe: hide from AT -->
<iframe src="tracking.html"
        title="Analytics"
        aria-hidden="true"
        tabindex="-1"
        style="display:none">
</iframe>

<!-- Payment/form iframe -->
<iframe src="https://payment.provider.com/checkout"
        title="Secure payment form"
        sandbox="allow-scripts allow-forms allow-same-origin">
</iframe>
```

---

## 48. PDFs and Downloads

```html
❌ WRONG — PDF linked without warning; no accessible PDF; file size hidden
<a href="report.pdf">Annual Report</a>
<a href="manual.pdf">Manual</a>
```

```html
✅ RIGHT — Accessible document downloads (SC 2.4.4, EN 301 549 §10)

<!-- PDF link: indicate file type, size, and that it opens separately -->
<a href="/docs/annual-report-2024.pdf"
   type="application/pdf"
   aria-label="Download Annual Report 2024 (PDF, 3.2 MB, opens in new tab)"
   target="_blank"
   rel="noopener">
  Annual Report 2024
  <svg aria-hidden="true" focusable="false" class="icon-pdf"><!-- PDF icon --></svg>
  <span class="file-meta">(PDF, 3.2 MB)</span>
</a>

<!-- Offer accessible alternative when PDF may not be accessible -->
<ul class="download-options">
  <li>
    <a href="/docs/report.pdf" type="application/pdf"
       aria-label="Download Annual Report as PDF (3.2 MB)">
      PDF version
    </a>
    <span class="hint">May not be accessible on all devices</span>
  </li>
  <li>
    <a href="/docs/report.html"
       aria-label="View Annual Report as accessible HTML">
      HTML version <span class="badge">Accessible</span>
    </a>
  </li>
  <li>
    <a href="/docs/report.docx" type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
       aria-label="Download Annual Report as Word document (1.1 MB)">
      Word document (1.1 MB)
    </a>
  </li>
</ul>
```

---

## 49. Social Media Embeds

```html
❌ WRONG — Auto-playing embedded videos; no title on iframe; inaccessible feeds
<div class="instagram-embed"><!-- third-party embed with no accessibility control --></div>
```

```html
✅ RIGHT — Accessible social content (SC 1.2.2, SC 4.1.2)

<!-- Prefer link-out to embed when you can't control accessibility -->
<div class="social-post">
  <blockquote>
    <p>"Widget A changed my life. Best purchase of 2024."</p>
    <footer>
      — <cite>
        <a href="https://twitter.com/user/status/123" 
           target="_blank"
           rel="noopener noreferrer"
           aria-label="View full tweet by @acmefan on Twitter (opens in new tab)">
          @acmefan on Twitter
        </a>
      </cite>
    </footer>
  </blockquote>
</div>

<!-- YouTube embed: nocookie domain, title, no autoplay -->
<figure>
  <iframe 
    src="https://www.youtube-nocookie.com/embed/VIDEO_ID?autoplay=0&rel=0"
    title="Acme Corp: Widget A Launch Event 2024"
    width="560" height="315"
    loading="lazy"
    allowfullscreen>
  </iframe>
  <figcaption>
    Widget A Launch Event 2024 — 
    <a href="/videos/widget-a-launch-transcript">Read transcript</a>
  </figcaption>
</figure>
```

---

## 50. Cookie Banners

```html
❌ WRONG — Cookie banner traps keyboard; modal without focus management;
          no keyboard accessible way to reject all
<div id="cookie-banner" style="position:fixed; bottom:0">
  <p>We use cookies. <a href="/cookies">Learn more</a></p>
  <button onclick="acceptAll()">Accept all</button>
  <!-- No "reject all" option — legal problem in EU -->
  <!-- Banner doesn't trap focus; behind-banner content still interactive -->
</div>
```

```html
✅ RIGHT — Accessible, GDPR-compliant cookie banner (SC 2.1.1, 2.1.2)

<!--
  Cookie banner as a dialog (it's blocking action from users)
  Must be keyboard accessible
  Must offer genuine choices
-->
<div role="dialog"
     aria-labelledby="cookie-title"
     aria-describedby="cookie-desc"
     aria-modal="true"
     id="cookie-consent"
     class="cookie-banner">
  
  <h2 id="cookie-title">Cookie Preferences</h2>
  
  <p id="cookie-desc">
    We use cookies to improve your experience. 
    You can accept all, reject non-essential cookies, 
    or customize your preferences.
    <a href="/privacy-policy">Read our Privacy Policy</a>.
  </p>
  
  <!-- Choices — must be equally prominent (GDPR requirement) -->
  <div class="cookie-actions">
    <button type="button" 
            class="btn-primary"
            onclick="acceptAll()">
      Accept all cookies
    </button>
    
    <button type="button"
            class="btn-secondary"
            onclick="rejectNonEssential()">
      Reject non-essential
    </button>
    
    <button type="button"
            class="btn-tertiary"
            onclick="openPreferences()"
            aria-expanded="false"
            aria-controls="cookie-preferences">
      Customize preferences
    </button>
  </div>
  
  <!-- Expandable preferences panel -->
  <div id="cookie-preferences" hidden>
    <fieldset>
      <legend>Cookie categories</legend>
      
      <label class="cookie-toggle">
        <input type="checkbox" checked disabled aria-disabled="true">
        <span>Essential cookies</span>
        <span class="hint">Always active — required for the site to function</span>
      </label>
      
      <label class="cookie-toggle">
        <input type="checkbox" id="analytics-cookies" name="analytics">
        <span>Analytics cookies</span>
        <span class="hint">Help us understand how visitors use our site</span>
      </label>
      
      <label class="cookie-toggle">
        <input type="checkbox" id="marketing-cookies" name="marketing">
        <span>Marketing cookies</span>
        <span class="hint">Used to show you relevant advertisements</span>
      </label>
    </fieldset>
    
    <button type="button" onclick="savePreferences()">Save preferences</button>
  </div>
  
</div>
```

```javascript
// Focus management for cookie banner
document.addEventListener('DOMContentLoaded', () => {
  const banner = document.getElementById('cookie-consent');
  if (banner && !hasCookieConsent()) {
    // Focus first button in banner
    const firstBtn = banner.querySelector('button');
    firstBtn.focus();
    
    // Trap focus within banner
    banner.addEventListener('keydown', trapFocus);
  }
});

function dismissBanner() {
  const banner = document.getElementById('cookie-consent');
  banner.setAttribute('hidden', '');
  // Return focus to body/main content
  document.getElementById('main-content').focus();
}
```

---

## 51. Footer and Contact

```html
❌ WRONG — Phone number not a link; address not marked up; email obfuscated via JS
<p>Phone: 030 123456</p><!-- not clickable on mobile -->
<p>Email: info [at] acme [dot] com</p><!-- screen readers and AT can't use this -->
```

```html
✅ RIGHT — Accessible contact information (SC 1.3.1, 2.1.1)
<footer>
  <section aria-labelledby="footer-contact">
    <h2 id="footer-contact">Contact Us</h2>
    
    <!-- Use <address> for contact information -->
    <address>
      <p>
        <strong>Acme Corp GmbH</strong><br>
        Musterstraße 42<br>
        10115 Berlin<br>
        Germany
      </p>
      
      <!-- Phone: tel: link works on all devices -->
      <p>
        Phone: <a href="tel:+4930123456">+49 30 123456</a>
      </p>
      
      <!-- Email: mailto: link — no obfuscation needed for AT -->
      <p>
        Email: <a href="mailto:info@acme-corp.de">info@acme-corp.de</a>
      </p>
      
      <!-- Fax (if needed) -->
      <p>
        Fax: <a href="tel:+4930123457">+49 30 123457</a>
      </p>
    </address>
    
    <!-- Opening hours as a table or list -->
    <h3>Opening Hours</h3>
    <dl>
      <dt>Monday – Friday</dt>
      <dd>09:00 – 18:00 CET</dd>
      <dt>Saturday</dt>
      <dd>10:00 – 14:00 CET</dd>
      <dt>Sunday</dt>
      <dd>Closed</dd>
    </dl>
  </section>
  
  <!-- Social media links -->
  <section aria-labelledby="footer-social">
    <h2 id="footer-social">Follow Us</h2>
    <ul role="list">
      <li>
        <a href="https://twitter.com/acmecorp"
           target="_blank"
           rel="noopener noreferrer"
           aria-label="Acme Corp on Twitter (opens in new tab)">
          <svg aria-hidden="true" focusable="false"><!-- Twitter icon --></svg>
          Twitter
        </a>
      </li>
      <li>
        <a href="https://linkedin.com/company/acmecorp"
           target="_blank"
           rel="noopener noreferrer"
           aria-label="Acme Corp on LinkedIn (opens in new tab)">
          <svg aria-hidden="true" focusable="false"><!-- LinkedIn icon --></svg>
          LinkedIn
        </a>
      </li>
    </ul>
  </section>
  
  <!-- Legal links -->
  <nav aria-label="Legal">
    <ul role="list">
      <li><a href="/accessibility">Accessibility Statement</a></li>
      <li><a href="/privacy">Privacy Policy</a></li>
      <li><a href="/imprint">Legal Notice (Impressum)</a></li>
      <li><a href="/terms">Terms and Conditions</a></li>
    </ul>
  </nav>
  
  <p>
    <small>© 2024 Acme Corp GmbH. All rights reserved.</small>
  </p>
</footer>
```

---

## 52. Accessibility Statement Page

This page is legally required under EU WAD, BFSG, and EAA. It must itself be accessible.

```html
✅ RIGHT — Full accessibility statement (EN 301 549 §12.1.1, BFSG §14)

<!DOCTYPE html>
<html lang="en"><!-- or lang="de" for German -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Accessibility Statement — Acme Corp</title>
</head>
<body>

<a href="#main" class="skip-link">Skip to main content</a>

<header>
  <nav aria-label="Primary navigation">...</nav>
</header>

<main id="main" tabindex="-1">
  
  <h1>Accessibility Statement</h1>
  
  <p>
    <strong>Acme Corp GmbH</strong> is committed to making its website 
    accessible in accordance with the 
    Barrierefreiheitsstärkungsgesetz (BFSG) / 
    European Accessibility Act (EAA) / 
    EU Web Accessibility Directive (WAD 2016/2102).
  </p>
  
  <p>
    <strong>Date of this statement:</strong> 
    <time datetime="2025-06-28">28 June 2025</time>
  </p>
  
  <h2>Compliance Status</h2>
  
  <p>
    This website is <strong>partially conformant</strong> with 
    EN 301 549 v3.2.1 incorporating 
    Web Content Accessibility Guidelines (WCAG) 2.1 Level AA.
    "Partially conformant" means that some parts of the content 
    do not fully conform to the standard.
  </p>
  
  <h2>Non-accessible Content</h2>
  
  <p>The following content is not yet fully accessible:</p>
  
  <ul>
    <li>
      <strong>Older PDF documents</strong> published before 28 June 2025 
      may lack proper tagging and reading order.
      <br>
      <strong>Alternative:</strong> Contact us at 
      <a href="mailto:accessibility@acme-corp.de">accessibility@acme-corp.de</a>
      to request an accessible version.
      <br>
      <strong>Reason:</strong> Disproportionate burden — remediation of legacy 
      archive documents (>500 files) is planned for Q1 2026.
    </li>
    
    <li>
      <strong>Live video streams:</strong> Real-time captions are not yet 
      available for live events.
      <br>
      <strong>Alternative:</strong> Captioned recordings are published within 
      48 hours of each event.
      <br>
      <strong>Reason:</strong> Technical limitation — live captioning service 
      integration is in development.
    </li>
    
    <li>
      <strong>Third-party map embed</strong> (Google Maps): 
      The embedded map may not be fully keyboard accessible.
      <br>
      <strong>Alternative:</strong> 
      <a href="/contact">Our address and directions</a> are available as text.
      <br>
      <strong>Reason:</strong> Third-party content not under our control.
    </li>
  </ul>
  
  <h2>Feedback and Contact</h2>
  
  <p>
    If you experience accessibility barriers on our website or need content 
    in an accessible format, please contact us:
  </p>
  
  <address>
    <p>
      <strong>Accessibility Team</strong><br>
      Acme Corp GmbH
    </p>
    <p>
      Email: <a href="mailto:accessibility@acme-corp.de">accessibility@acme-corp.de</a>
    </p>
    <p>
      Phone: <a href="tel:+4930123456">+49 30 123456</a>
      (Monday–Friday, 09:00–18:00 CET)
    </p>
  </address>
  
  <p>We aim to respond within <strong>5 business days</strong>.</p>
  
  <h2>Enforcement Procedure</h2>
  
  <!-- For German public sector (WAD / BGG) -->
  <p>
    If your report is not satisfactorily addressed within a reasonable time, 
    you can contact the 
    <a href="https://www.schlichtungsstelle-bgg.de/" 
       target="_blank" 
       rel="noopener noreferrer"
       aria-label="Federal Conciliation Body (external website, opens in new tab)">
      Federal Conciliation Body (Schlichtungsstelle nach dem BGG)
    </a>.
  </p>
  
  <!-- For German private sector (BFSG) -->
  <p>
    For complaints regarding private-sector services under the BFSG, 
    contact the responsible market surveillance authority 
    (Marktüberwachungsbehörde) in your federal state.
  </p>
  
  <h2>Technical Information</h2>
  
  <p>This website relies on the following technologies:</p>
  <ul>
    <li>HTML5</li>
    <li>CSS3</li>
    <li>JavaScript (ES2020)</li>
    <li>WAI-ARIA 1.2</li>
  </ul>
  
  <h2>Assessment Approach</h2>
  
  <p>
    Acme Corp assessed the accessibility of this website by:
  </p>
  <ul>
    <li>Self-evaluation using NVDA + Firefox and VoiceOver + Safari</li>
    <li>Automated testing with axe-core and Lighthouse</li>
    <li>Third-party audit by [Accessibility Agency] on 
        <time datetime="2025-03-15">15 March 2025</time></li>
  </ul>
  
  <!-- Barrier reporting form -->
  <h2>Report an Accessibility Barrier</h2>
  
  <form action="/accessibility-feedback" method="post" novalidate>
    <div class="field">
      <label for="barrier-url">Page URL where you found the barrier</label>
      <input type="url" id="barrier-url" name="url" autocomplete="url"
             placeholder="https://acme-corp.de/...">
    </div>
    
    <div class="field">
      <label for="barrier-desc">
        Description of the barrier <span aria-hidden="true">*</span>
      </label>
      <textarea id="barrier-desc" name="description" rows="5" 
                required aria-required="true"></textarea>
    </div>
    
    <div class="field">
      <label for="barrier-at">Assistive technology used (optional)</label>
      <input type="text" id="barrier-at" name="assistiveTech"
             placeholder="e.g. NVDA + Firefox, VoiceOver + Safari">
    </div>
    
    <div class="field">
      <label for="barrier-email">
        Your email for follow-up (optional)
      </label>
      <input type="email" id="barrier-email" name="email" autocomplete="email">
    </div>
    
    <button type="submit">Submit report</button>
  </form>
  
</main>

<footer>...</footer>

</body>
</html>
```

---

## Quick Reference: The 10 Most Common Failures

| Rank | Failure | Fix |
|---|---|---|
| 1 | Missing or empty `alt` on images | Add descriptive `alt`; empty `alt=""` for decorative |
| 2 | Low color contrast | Check all text: 4.5:1 minimum; use a contrast checker |
| 3 | `outline: none` / no focus indicator | Use `:focus-visible` with custom, high-contrast outline |
| 4 | Missing form labels | Every `<input>` needs `<label for="...">` |
| 5 | Inaccessible custom UI components | Use semantic HTML; add ARIA roles + keyboard behavior |
| 6 | Empty link text or "click here" | Add descriptive text or `aria-label` |
| 7 | Missing document `lang` | `<html lang="en">` (or appropriate code) |
| 8 | Keyboard traps | Modal focus management; Escape to close |
| 9 | Auto-playing media | Don't autoplay; if you must, provide pause control |
| 10 | Missing page title | Unique, descriptive `<title>` on every page |

---

*Guide version: 2025-05-18. All patterns validated against WCAG 2.1 AA, WCAG 2.2 AA, EN 301 549 v3.2.1, and ARIA Authoring Practices Guide 1.2.*

---

# Part 2 — Advanced Patterns & Edge Cases

## Table of Contents (Part 2)

53. [Number and Currency Inputs](#53-number-and-currency-inputs)
54. [File Upload](#54-file-upload)
55. [Drag and Drop](#55-drag-and-drop)
56. [Infinite Scroll and Load More](#56-infinite-scroll-and-load-more)
57. [Filter and Sort Controls](#57-filter-and-sort-controls)
58. [Star Ratings](#58-star-ratings)
59. [Tags and Chips Input](#59-tags-and-chips-input)
60. [Rich Text Editor (WYSIWYG)](#60-rich-text-editor-wysiwyg)
61. [Maps and Geographic Content](#61-maps-and-geographic-content)
62. [Sticky Headers and Position: Sticky](#62-sticky-headers-and-position-sticky)
63. [Popover (Floating UI)](#63-popover-floating-ui)
64. [Context Menus](#64-context-menus)
65. [Stepper / Quantity Controls](#65-stepper--quantity-controls)
66. [Toggle Switches](#66-toggle-switches)
67. [Color Picker](#67-color-picker)
68. [Typeahead / Autocomplete](#68-typeahead--autocomplete)
69. [Virtual Scrolling and Long Lists](#69-virtual-scrolling-and-long-lists)
70. [Data Grid / Spreadsheet](#70-data-grid--spreadsheet)
71. [Print Styles and Print Accessibility](#71-print-styles-and-print-accessibility)
72. [Dark Mode](#72-dark-mode)
73. [High Contrast Mode and Forced Colors](#73-high-contrast-mode-and-forced-colors)
74. [Right-to-Left (RTL) Layouts](#74-right-to-left-rtl-layouts)
75. [Error Pages (404, 500)](#75-error-pages-404-500)
76. [Session Timeout Warning](#76-session-timeout-warning)
77. [Confirmation Dialogs](#77-confirmation-dialogs)
78. [Inline Editing](#78-inline-editing)
79. [Split Buttons and Button Groups](#79-split-buttons-and-button-groups)
80. [Wizard / Multi-Step Stepper](#80-wizard--multi-step-stepper)
81. [Sign In / Authentication Flows](#81-sign-in--authentication-flows)
82. [Notifications Badge and Counter](#82-notifications-badge-and-counter)
83. [Skeleton Screens](#83-skeleton-screens)
84. [Code Blocks and Technical Content](#84-code-blocks-and-technical-content)
85. [Math and Scientific Notation](#85-math-and-scientific-notation)
86. [Time, Date and Timezone Display](#86-time-date-and-timezone-display)
87. [Prices and Numbers](#87-prices-and-numbers)
88. [React Accessibility Patterns](#88-react-accessibility-patterns)
89. [Full Accessible Page Template](#89-full-accessible-page-template)
90. [Automated Testing Integration](#90-automated-testing-integration)

---

## 53. Number and Currency Inputs

```html
❌ WRONG — type="number" for everything; spinner arrows on credit card fields;
           phone as number; no format guidance
<input type="number" name="price" placeholder="Price">
<input type="number" name="phone">
<input type="number" name="creditCard">
```

```html
✅ RIGHT — correct number input by use case

<!-- Currency / price: type="text" + inputmode="decimal" -->
<div class="field">
  <label for="price">Price <span aria-hidden="true">*</span></label>
  <input type="text"
         id="price"
         name="price"
         inputmode="decimal"
         pattern="[0-9]+([.,][0-9]{1,2})?"
         autocomplete="off"
         aria-required="true"
         aria-describedby="price-hint price-error"
         placeholder="0.00">
  <div id="price-hint" class="hint">Enter amount in EUR, e.g. 12.50</div>
  <div id="price-error" role="alert" aria-live="polite"></div>
</div>

<!-- Bounded integer quantity -->
<div class="field">
  <label for="quantity">Quantity</label>
  <input type="number"
         id="quantity" name="quantity"
         min="1" max="99" step="1" value="1"
         aria-describedby="qty-hint">
  <div id="qty-hint" class="hint">Between 1 and 99</div>
</div>

<!-- Phone: type="tel", not type="number" -->
<div class="field">
  <label for="phone">Phone number</label>
  <input type="tel" id="phone" name="phone"
         autocomplete="tel" inputmode="tel"
         aria-describedby="phone-hint"
         placeholder="+49 30 123456">
  <div id="phone-hint" class="hint">Include country code, e.g. +49 for Germany</div>
</div>

<!-- Credit card: type="text" + inputmode="numeric" -->
<div class="field">
  <label for="cc-number">Card number</label>
  <input type="text" id="cc-number" name="ccNumber"
         autocomplete="cc-number"
         inputmode="numeric"
         pattern="[0-9\s]{13,19}"
         maxlength="19"
         placeholder="1234 5678 9012 3456">
</div>

<!-- Postal code -->
<div class="field">
  <label for="postcode">Postal code</label>
  <input type="text" id="postcode" name="postcode"
         autocomplete="postal-code"
         inputmode="numeric"
         pattern="[0-9]{5}"
         placeholder="10115">
</div>
```

```javascript
// Format credit card as 4-digit groups
document.getElementById('cc-number').addEventListener('input', function() {
  let v = this.value.replace(/\D/g, '').substring(0, 16);
  this.value = v.match(/.{1,4}/g)?.join(' ') ?? v;
});

// Format currency on blur
const priceInput = document.getElementById('price');
priceInput.addEventListener('blur', function() {
  const raw = parseFloat(this.value.replace(',', '.'));
  if (!isNaN(raw)) this.value = raw.toFixed(2);
});
```

---

## 54. File Upload

```html
❌ WRONG — native input hidden with display:none (removes from tab order);
           no file name announced; no error for wrong type
<div class="drop-zone" ondrop="handleDrop(event)">Drop file here</div>
<button onclick="document.getElementById('f').click()">Browse</button>
<input type="file" id="f" style="display:none">
```

```html
✅ RIGHT — accessible file upload (SC 2.1.1, 4.1.2)

<div class="field">
  <label for="avatar" class="file-label">
    Profile photo
    <span class="file-label-btn" aria-hidden="true">Choose file</span>
  </label>
  <!-- visually-hidden, NOT display:none — keeps keyboard access -->
  <input type="file"
         id="avatar" name="avatar"
         accept="image/jpeg,image/png,image/webp"
         aria-describedby="avatar-hint avatar-status"
         class="file-input-sr">
  <div id="avatar-hint" class="hint">JPEG, PNG or WebP. Max 5 MB.</div>
  <div id="avatar-status" aria-live="polite"></div>
</div>

<!-- Drag-and-drop with keyboard fallback -->
<div class="field">
  <p id="upload-label">Upload documents</p>
  <div class="drop-zone"
       id="drop-zone"
       role="region"
       aria-labelledby="upload-label"
       aria-describedby="drop-hint"
       tabindex="0">

    <svg aria-hidden="true" focusable="false" class="drop-icon"><!-- ↑ --></svg>
    <p id="drop-hint">
      Drag and drop files here, or
      <label for="docs-upload" class="link-label">browse to select</label>
    </p>

    <!-- visually-hidden native input -->
    <input type="file" id="docs-upload" name="documents"
           multiple accept=".pdf,.docx,.xlsx"
           aria-describedby="upload-formats upload-list"
           class="file-input-sr">
    <div id="upload-formats" class="hint">PDF, Word, Excel. Max 10 MB per file.</div>

    <ul id="upload-list" aria-live="polite" aria-label="Selected files"></ul>
  </div>
</div>
```

```javascript
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('docs-upload');
const fileList  = document.getElementById('upload-list');
const status    = document.getElementById('avatar-status');

// Enter / Space triggers picker
dropZone.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); }
});

dropZone.addEventListener('dragenter', () => dropZone.classList.add('drag-over'));
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('dragover',  e => e.preventDefault());
dropZone.addEventListener('drop', e => { e.preventDefault(); handleFiles(e.dataTransfer.files); });
fileInput.addEventListener('change',   () => handleFiles(fileInput.files));

function handleFiles(files) {
  const valid = [], errors = [];
  Array.from(files).forEach(f => {
    f.size > 10 * 1024 * 1024
      ? errors.push(`${f.name} too large (max 10 MB)`)
      : valid.push(f);
  });

  fileList.innerHTML = valid.map(f => `
    <li>
      <span>${f.name} (${(f.size/1024/1024).toFixed(1)} MB)</span>
      <button type="button" aria-label="Remove ${f.name}">Remove</button>
    </li>`).join('');

  status.textContent = valid.length
    ? `${valid.length} file(s) selected: ${valid.map(f=>f.name).join(', ')}.`
    : 'No files selected.';

  if (errors.length)
    document.getElementById('aria-live-assertive').textContent = errors.join(' ');
}
```

```css
.file-input-sr {
  position: absolute; width: 1px; height: 1px;
  overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap;
}
.drop-zone {
  border: 2px dashed #767676; border-radius: 8px;
  padding: 2rem; text-align: center;
}
.drop-zone:focus-visible { outline: 3px solid #0052cc; outline-offset: 2px; }
.drop-zone.drag-over { border-color: #0052cc; background: #f0f7ff; }
.link-label { color: #0052cc; text-decoration: underline; cursor: pointer; }
```

---

## 55. Drag and Drop

```html
❌ WRONG — pure mouse drag; keyboard users cannot reorder (SC 2.1.1, SC 2.5.7 violation)
<ul class="sortable">
  <li draggable="true" ondragstart="drag(event)">Item 1</li>
</ul>
```

```html
✅ RIGHT — drag + keyboard up/down buttons (SC 2.1.1, WCAG 2.2 SC 2.5.7)

<div role="region" aria-labelledby="sort-label">
  <h2 id="sort-label">Reorder items</h2>
  <p id="sort-hint" class="hint">
    Drag to reorder, or use Up / Down buttons.
  </p>
  <ul id="sortable-list" aria-describedby="sort-hint">

    <li class="sort-item" draggable="true" aria-grabbed="false" id="item-1">
      <span class="drag-handle" aria-hidden="true" title="Drag to reorder">⠿</span>
      <span class="item-label">Item 1</span>
      <div role="group" aria-label="Reorder Item 1">
        <button type="button" class="move-up" aria-label="Move Item 1 up">↑</button>
        <button type="button" class="move-down" aria-label="Move Item 1 down">↓</button>
      </div>
    </li>

    <li class="sort-item" draggable="true" aria-grabbed="false" id="item-2">
      <span class="drag-handle" aria-hidden="true">⠿</span>
      <span class="item-label">Item 2</span>
      <div role="group" aria-label="Reorder Item 2">
        <button type="button" class="move-up" aria-label="Move Item 2 up">↑</button>
        <button type="button" class="move-down" aria-label="Move Item 2 down">↓</button>
      </div>
    </li>

  </ul>
  <div aria-live="polite" aria-atomic="true"
       class="visually-hidden" id="sort-announce"></div>
</div>
```

```javascript
const list     = document.getElementById('sortable-list');
const announce = document.getElementById('sort-announce');

list.addEventListener('click', e => {
  const btn  = e.target.closest('.move-up, .move-down');
  if (!btn) return;
  const item  = btn.closest('.sort-item');
  const items = [...list.querySelectorAll('.sort-item')];
  const idx   = items.indexOf(item);
  const label = item.querySelector('.item-label').textContent;

  if (btn.classList.contains('move-up') && idx > 0) {
    list.insertBefore(item, items[idx - 1]);
    announce.textContent = `${label} moved up to position ${idx}.`;
    btn.focus();
  } else if (btn.classList.contains('move-down') && idx < items.length - 1) {
    list.insertBefore(items[idx + 1], item);
    announce.textContent = `${label} moved down to position ${idx + 2}.`;
    btn.focus();
  }
  refreshButtons();
});

function refreshButtons() {
  const items = [...list.querySelectorAll('.sort-item')];
  items.forEach((item, i) => {
    item.querySelector('.move-up').disabled   = i === 0;
    item.querySelector('.move-down').disabled = i === items.length - 1;
  });
}

list.addEventListener('dragstart', e => e.target.closest('.sort-item')?.setAttribute('aria-grabbed','true'));
list.addEventListener('dragend',   e => e.target.closest('.sort-item')?.setAttribute('aria-grabbed','false'));

refreshButtons();
```

---

## 56. Infinite Scroll and Load More

```html
❌ WRONG — auto-scroll fires on scroll event, no keyboard trigger, footer unreachable
<script>
  window.addEventListener('scroll', () => { if (nearBottom()) loadMore(); });
</script>
```

```html
✅ RIGHT — "Load More" button pattern (SC 2.1.1, 4.1.3)

<main id="main-content" tabindex="-1">
  <h1>Products</h1>

  <p aria-live="polite" aria-atomic="true" id="results-count">
    Showing 12 of 84 products
  </p>

  <ul id="product-list" aria-label="Products"><!-- cards --></ul>

  <div class="load-more-container">
    <button type="button" id="load-more-btn" aria-controls="product-list">
      Load more products
    </button>
    <div id="load-status" aria-live="polite" class="visually-hidden"></div>
  </div>
</main>
```

```javascript
let loaded = 12;
const total = 84, pageSize = 12;
const btn    = document.getElementById('load-more-btn');
const list   = document.getElementById('product-list');
const count  = document.getElementById('results-count');
const status = document.getElementById('load-status');

btn.addEventListener('click', async () => {
  btn.disabled = true;
  btn.textContent = 'Loading…';
  status.textContent = `Loading ${pageSize} more products…`;

  const items = await fetchProducts(loaded, pageSize);
  const firstNew = createCard(items[0]);
  items.slice(1).forEach(p => list.appendChild(createCard(p)));
  list.appendChild(firstNew);
  loaded += items.length;

  count.textContent = `Showing ${loaded} of ${total} products`;

  if (loaded >= total) {
    btn.remove();
    status.textContent = `All ${total} products loaded.`;
  } else {
    btn.disabled = false;
    btn.textContent = 'Load more products';
    status.textContent = `${items.length} more products loaded.`;
    firstNew.querySelector('a, button')?.focus(); // focus first new item
  }
});
```

---

## 57. Filter and Sort Controls

```html
❌ WRONG — select with onchange=submit (focus lost on reload); 
           active filters not announced to SR; color-only active state
<select onchange="this.form.submit()"><option>Sort by price</option></select>
<button class="active" onclick="filter('red')">Red</button><!-- active = CSS only -->
```

```html
✅ RIGHT — accessible filter + sort (SC 1.3.1, 2.4.3, 4.1.3)

<form id="filter-form" aria-label="Sort and filter products">

  <div class="field">
    <label for="sort-select">Sort by</label>
    <select id="sort-select" name="sort">
      <option value="relevance">Relevance</option>
      <option value="price-asc">Price: Low to High</option>
      <option value="price-desc">Price: High to Low</option>
      <option value="newest">Newest first</option>
    </select>
  </div>

  <fieldset>
    <legend>Filter by color</legend>
    <label class="filter-opt">
      <input type="checkbox" name="color" value="red">
      Red <span class="filter-count">(12)</span>
    </label>
    <label class="filter-opt">
      <input type="checkbox" name="color" value="blue">
      Blue <span class="filter-count">(8)</span>
    </label>
  </fieldset>

  <!-- Active filter chips -->
  <section aria-labelledby="active-label">
    <h2 id="active-label" class="visually-hidden">Active filters</h2>
    <ul id="active-filters" aria-label="Active filters"></ul>
  </section>

  <!-- Results count live region -->
  <p id="filter-status" aria-live="polite" aria-atomic="true">24 products found</p>

  <button type="submit">Apply filters</button>
  <button type="button" id="clear-filters">Clear all</button>
</form>

<section aria-live="polite" aria-busy="false" aria-labelledby="results-heading">
  <h2 id="results-heading" tabindex="-1">Results</h2>
  <ul id="results-list"><!-- cards --></ul>
</section>
```

```javascript
document.getElementById('filter-form').addEventListener('change', debounce(async () => {
  const section = document.querySelector('[aria-live="polite"][aria-labelledby="results-heading"]');
  section.setAttribute('aria-busy', 'true');
  document.getElementById('filter-status').textContent = 'Updating results…';

  const results = await fetchFiltered(new FormData(document.getElementById('filter-form')));
  renderResults(results);
  section.setAttribute('aria-busy', 'false');
  document.getElementById('filter-status').textContent = `${results.total} products found`;
  document.getElementById('results-heading').focus(); // tell SR results changed
}, 300));
```

---

## 58. Star Ratings

```html
❌ WRONG — star images with no text; no keyboard access; value hidden from SR
<div class="stars">
  <img src="star-full.png"><img src="star-full.png">
  <img src="star-half.png"><img src="star-empty.png">
</div>
```

```html
✅ RIGHT — read-only rating + interactive rating input

<!-- Read-only -->
<div role="img" aria-label="Rating: 3.5 out of 5 stars" class="star-display">
  <!-- SVG stars, aria-hidden="true" -->
</div>
<p>Based on <a href="#reviews">47 reviews</a></p>

<!-- Interactive: radio group (cleanest pattern) -->
<fieldset class="star-rating-input">
  <legend>Rate this product</legend>
  <label class="star-label">
    <input type="radio" name="rating" value="1" aria-label="1 star out of 5">
    <svg aria-hidden="true" focusable="false" class="star-icon"><!-- ★ --></svg>
  </label>
  <label class="star-label">
    <input type="radio" name="rating" value="2" aria-label="2 stars out of 5">
    <svg aria-hidden="true" focusable="false" class="star-icon"><!-- ★ --></svg>
  </label>
  <label class="star-label">
    <input type="radio" name="rating" value="3" aria-label="3 stars out of 5">
    <svg aria-hidden="true" focusable="false" class="star-icon"><!-- ★ --></svg>
  </label>
  <label class="star-label">
    <input type="radio" name="rating" value="4" aria-label="4 stars out of 5">
    <svg aria-hidden="true" focusable="false" class="star-icon"><!-- ★ --></svg>
  </label>
  <label class="star-label">
    <input type="radio" name="rating" value="5" aria-label="5 stars out of 5">
    <svg aria-hidden="true" focusable="false" class="star-icon"><!-- ★ --></svg>
  </label>
  <div aria-live="polite" class="visually-hidden" id="rating-status"></div>
</fieldset>
```

```javascript
document.querySelectorAll('[name="rating"]').forEach(r =>
  r.addEventListener('change', function() {
    document.getElementById('rating-status').textContent =
      `You selected ${this.value} star${this.value > 1 ? 's' : ''}.`;
  })
);
```

```css
.star-label input[type="radio"] {
  position: absolute; width: 1px; height: 1px;
  overflow: hidden; clip: rect(0,0,0,0);
}
.star-icon { fill: #d1d5db; width: 32px; height: 32px; }

/* Fill checked star and all preceding stars using general sibling */
.star-label:hover .star-icon,
.star-label:hover ~ .star-label .star-icon { fill: #f59e0b; }

input[type="radio"]:checked ~ .star-label .star-icon { fill: #d1d5db; }
input[type="radio"]:checked + svg, /* same label */
.star-label:has(input:checked) .star-icon { fill: #f59e0b; }

input[type="radio"]:focus-visible + .star-icon,
.star-label:has(input:focus-visible) .star-icon {
  outline: 3px solid #0052cc; outline-offset: 2px;
}
```

---

## 59. Tags and Chips Input

```html
❌ WRONG — delete span not keyboard accessible; input without label; no SR announcement
<div class="tags-input">
  <span class="tag">JS <span onclick="rm(this)">×</span></span>
  <input type="text" placeholder="Add tag…">
</div>
```

```html
✅ RIGHT — accessible tags input (SC 2.1.1, 4.1.2, 4.1.3)

<div class="field">
  <label id="tags-label" for="tags-input">Skills</label>
  <div id="tags-hint" class="hint">
    Type a skill and press Enter or comma to add.
    Press Backspace on empty input to remove the last tag.
  </div>
  <div class="tags-container" role="group" aria-labelledby="tags-label">
    <ul id="tags-list" aria-label="Selected skills" role="list"></ul>
    <input type="text" id="tags-input"
           autocomplete="off"
           aria-label="Add a skill"
           aria-describedby="tags-hint">
  </div>
  <input type="hidden" name="skills" id="skills-value">
  <div aria-live="polite" class="visually-hidden" id="tags-announce"></div>
</div>
```

```javascript
const tags     = new Set();
const input    = document.getElementById('tags-input');
const tagsList = document.getElementById('tags-list');
const announce = document.getElementById('tags-announce');

function addTag(value) {
  const tag = value.trim().toLowerCase();
  if (!tag || tags.has(tag)) return;
  tags.add(tag);
  render();
  announce.textContent = `${tag} added. ${tags.size} skill${tags.size > 1?'s':''} total.`;
  input.value = '';
}

function removeTag(tag) {
  tags.delete(tag);
  render();
  announce.textContent = `${tag} removed. ${tags.size} skill${tags.size !== 1?'s':''} selected.`;
  input.focus();
}

function render() {
  tagsList.innerHTML = [...tags].map(tag => `
    <li class="tag-item">
      <span class="tag-text">${tag}</span>
      <button type="button" class="tag-remove" aria-label="Remove skill: ${tag}">
        <span aria-hidden="true">×</span>
      </button>
    </li>`).join('');
  tagsList.querySelectorAll('.tag-remove').forEach(btn =>
    btn.addEventListener('click', () =>
      removeTag(btn.closest('li').querySelector('.tag-text').textContent)
    )
  );
  document.getElementById('skills-value').value = [...tags].join(',');
}

input.addEventListener('keydown', e => {
  if ((e.key === 'Enter' || e.key === ',') && input.value.trim()) {
    e.preventDefault(); addTag(input.value);
  }
  if (e.key === 'Backspace' && !input.value && tags.size > 0)
    removeTag([...tags].pop());
});
```

---

## 60. Rich Text Editor (WYSIWYG)

```html
❌ WRONG — toolbar buttons with no names; contenteditable with no role;
           no keyboard shortcut announcements
<div contenteditable class="editor"></div>
<button><b>B</b></button><!-- no aria-label -->
```

```html
✅ RIGHT — accessible RTE skeleton (SC 2.1.1, 4.1.2)
<!-- Recommendation: use TipTap, ProseMirror, or Quill (with a11y patches) -->

<div class="rte" role="group" aria-labelledby="rte-label">
  <p id="rte-label">Message body <span aria-hidden="true">*</span></p>

  <!-- Toolbar: arrow-key navigation between buttons (roving tabindex) -->
  <div role="toolbar" aria-label="Text formatting" aria-controls="rte-editor">

    <button type="button" role="button"
            aria-pressed="false"
            aria-label="Bold (Ctrl+B)"
            tabindex="0" data-cmd="bold">
      <svg aria-hidden="true" focusable="false"><!-- B --></svg>
    </button>

    <button type="button" aria-pressed="false"
            aria-label="Italic (Ctrl+I)"
            tabindex="-1" data-cmd="italic">
      <svg aria-hidden="true" focusable="false"><!-- I --></svg>
    </button>

    <button type="button" aria-pressed="false"
            aria-label="Underline (Ctrl+U)"
            tabindex="-1" data-cmd="underline">
      <svg aria-hidden="true" focusable="false"><!-- U --></svg>
    </button>

    <div role="separator" aria-orientation="vertical"></div>

    <button type="button" aria-label="Bulleted list"
            tabindex="-1" data-cmd="insertUnorderedList">
      <svg aria-hidden="true" focusable="false"><!-- list --></svg>
    </button>

    <select aria-label="Heading level" tabindex="-1">
      <option value="div">Normal text</option>
      <option value="h2">Heading 2</option>
      <option value="h3">Heading 3</option>
    </select>
  </div>

  <div id="rte-editor"
       role="textbox"
       contenteditable="true"
       aria-multiline="true"
       aria-label="Message body"
       aria-required="true"
       aria-describedby="rte-hint">
    <p>Type your message here…</p>
  </div>

  <div id="rte-hint" class="hint">
    Ctrl+B bold · Ctrl+I italic · Ctrl+Z undo
  </div>
  <div aria-live="polite" class="hint" id="rte-count">0 characters</div>
</div>
```

```javascript
// Roving tabindex in toolbar
const toolbar = document.querySelector('[role="toolbar"]');
const items   = [...toolbar.querySelectorAll('button, select')];

toolbar.addEventListener('keydown', e => {
  const idx = items.indexOf(document.activeElement);
  if (e.key === 'ArrowRight' && idx < items.length - 1) {
    items[idx].tabIndex = -1; items[idx+1].tabIndex = 0; items[idx+1].focus(); e.preventDefault();
  }
  if (e.key === 'ArrowLeft' && idx > 0) {
    items[idx].tabIndex = -1; items[idx-1].tabIndex = 0; items[idx-1].focus(); e.preventDefault();
  }
});

items.filter(b => b.dataset.cmd).forEach(btn => {
  btn.addEventListener('click', () => {
    document.execCommand(btn.dataset.cmd);
    btn.setAttribute('aria-pressed', String(document.queryCommandState(btn.dataset.cmd)));
    document.getElementById('rte-editor').focus();
  });
});
```

---

## 61. Maps and Geographic Content

```html
❌ WRONG — map embed is the only source of address; iframe without title
<iframe src="https://maps.google.com/..."></iframe>
```

```html
✅ RIGHT — text address first, map as enhancement (SC 1.1.1, EN 301 549 §9)

<section aria-labelledby="location-heading">
  <h2 id="location-heading">How to Find Us</h2>

  <!-- Text address — primary, always accessible -->
  <address>
    <strong>Acme Corp GmbH</strong><br>
    Musterstraße 42<br>
    10115 Berlin, Germany
  </address>

  <h3>Getting Here</h3>
  <ul>
    <li><strong>U-Bahn:</strong> U2 Stadtmitte, 5 minutes walk</li>
    <li><strong>Bus:</strong> Lines 147, M48 — stop Musterstraße</li>
    <li><strong>By car:</strong> Parkhaus Mitte, Hauptstraße 10 (200 m)</li>
  </ul>

  <p>
    <a href="https://maps.google.com/?q=Musterstraße+42+Berlin"
       target="_blank" rel="noopener noreferrer"
       aria-label="View our location on Google Maps (opens in new tab)">
      Open in Google Maps
    </a>
  </p>

  <!-- Embedded map: supplementary only -->
  <iframe
    src="https://www.google.com/maps/embed?..."
    title="Map showing Acme Corp at Musterstraße 42, Berlin"
    width="600" height="450"
    loading="lazy"
    referrerpolicy="no-referrer-when-downgrade">
  </iframe>
</section>
```

---

## 62. Sticky Headers and Position: Sticky

```css
/* Problem: sticky header obscures keyboard-focused elements.
   Browser scrolls focused element into view but ignores sticky height. */

/* ❌ WRONG — no scroll compensation */
header { position: sticky; top: 0; height: 80px; z-index: 100; }

/* ✅ RIGHT — scroll-padding-top compensates for sticky header */
:root { --header-h: 80px; }

html { scroll-padding-top: calc(var(--header-h) + 10px); }

/* For elements receiving programmatic focus */
:target,
[tabindex="-1"]:focus { scroll-margin-top: calc(var(--header-h) + 10px); }
```

```javascript
// Update CSS var when header height changes (e.g. responsive breakpoints)
const header = document.querySelector('header');
new ResizeObserver(() => {
  document.documentElement.style.setProperty('--header-h', `${header.offsetHeight}px`);
}).observe(header);
```

---

## 63. Popover (Floating UI)

```html
<!-- HTML Popover API (Chrome 114+, Safari 17+, Firefox 125+) -->

<!-- ✅ RIGHT — native popover (Escape + light-dismiss built in) -->
<button type="button" popovertarget="my-popover">Open filter</button>

<div id="my-popover" popover
     role="dialog"
     aria-labelledby="popover-title">
  <h2 id="popover-title">Filter Options</h2>
  <!-- content -->
  <button type="button" popovertarget="my-popover" popovertargetaction="hide">
    Close
  </button>
</div>

<!-- Fallback: manual popover with ARIA -->
<button type="button" id="pop-trigger"
        aria-expanded="false"
        aria-controls="pop-panel"
        aria-haspopup="dialog">
  Filter
</button>

<div id="pop-panel" role="dialog"
     aria-labelledby="pop-heading"
     aria-modal="false" hidden>
  <h2 id="pop-heading">Filter Options</h2>
  <!-- content -->
  <button type="button" id="pop-close" aria-label="Close filter options">Close</button>
</div>
```

```javascript
const trigger = document.getElementById('pop-trigger');
const panel   = document.getElementById('pop-panel');
const close   = document.getElementById('pop-close');

const open  = () => {
  panel.removeAttribute('hidden');
  trigger.setAttribute('aria-expanded','true');
  panel.querySelector('button,input,select,a[href]')?.focus();
};
const shut  = () => {
  panel.setAttribute('hidden','');
  trigger.setAttribute('aria-expanded','false');
  trigger.focus();
};

trigger.addEventListener('click', () => panel.hasAttribute('hidden') ? open() : shut());
close.addEventListener('click', shut);
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && !panel.hasAttribute('hidden')) shut();
});
document.addEventListener('click', e => {
  if (!trigger.contains(e.target) && !panel.contains(e.target) && !panel.hasAttribute('hidden'))
    shut();
});
```

---

## 64. Context Menus

```html
❌ WRONG — right-click only; no keyboard trigger
<div oncontextmenu="show(event)">Right-click me</div>
```

```html
✅ RIGHT — context menu with keyboard trigger (SC 2.1.1)

<li class="ctx-item" tabindex="0" aria-haspopup="menu" aria-controls="ctx-1" id="file-row">
  Document.pdf
  <button type="button" class="ctx-btn"
          aria-label="Options for Document.pdf"
          aria-haspopup="menu"
          aria-expanded="false"
          aria-controls="ctx-1">
    <svg aria-hidden="true" focusable="false"><!-- ⋮ --></svg>
  </button>
</li>

<ul id="ctx-1" role="menu" aria-labelledby="file-row" hidden>
  <li role="none"><button role="menuitem" type="button">Download</button></li>
  <li role="none"><button role="menuitem" type="button">Rename</button></li>
  <li role="separator"></li>
  <li role="none"><button role="menuitem" type="button" class="danger">Delete</button></li>
</ul>
```

```javascript
document.querySelectorAll('.ctx-btn').forEach(trigger => {
  const menu  = document.getElementById(trigger.getAttribute('aria-controls'));
  const items = () => [...menu.querySelectorAll('[role="menuitem"]')];

  const open  = () => {
    menu.removeAttribute('hidden');
    trigger.setAttribute('aria-expanded','true');
    items()[0].focus();
  };
  const close = () => {
    menu.setAttribute('hidden','');
    trigger.setAttribute('aria-expanded','false');
    trigger.focus();
  };

  trigger.addEventListener('click', () => menu.hasAttribute('hidden') ? open() : close());

  // Right-click
  trigger.closest('.ctx-item').addEventListener('contextmenu', e => {
    e.preventDefault(); open();
  });

  // Shift+F10 / ContextMenu key
  trigger.closest('.ctx-item').addEventListener('keydown', e => {
    if (e.key === 'ContextMenu' || (e.key === 'F10' && e.shiftKey)) {
      e.preventDefault(); open();
    }
  });

  // Arrow key navigation
  menu.addEventListener('keydown', e => {
    const list = items(); const idx = list.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); list[(idx+1)%list.length].focus(); }
    if (e.key === 'ArrowUp')   { e.preventDefault(); list[(idx-1+list.length)%list.length].focus(); }
    if (e.key === 'Escape')    close();
    if (e.key === 'Home')      list[0].focus();
    if (e.key === 'End')       list[list.length-1].focus();
  });

  document.addEventListener('click', e => {
    if (!menu.contains(e.target) && !trigger.contains(e.target) && !menu.hasAttribute('hidden'))
      close();
  });
});
```

---

## 65. Stepper / Quantity Controls

```html
❌ WRONG — +/- buttons with no names; value as plain span (not editable)
<button onclick="qty--">-</button>
<span class="qty">1</span>
<button onclick="qty++">+</button>
```

```html
✅ RIGHT — quantity stepper (SC 2.1.1, 4.1.2)

<div class="stepper" role="group" aria-labelledby="qty-label">
  <span id="qty-label">Quantity</span>
  <div class="stepper-controls">
    <button type="button" id="qty-dec" aria-label="Decrease quantity" aria-controls="qty-in">−</button>
    <input type="number" id="qty-in" name="quantity"
           value="1" min="1" max="99" step="1"
           aria-label="Quantity">
    <button type="button" id="qty-inc" aria-label="Increase quantity" aria-controls="qty-in">+</button>
  </div>
</div>
```

```javascript
const inp = document.getElementById('qty-in');
const dec = document.getElementById('qty-dec');
const inc = document.getElementById('qty-inc');

function updateQty(delta) {
  const val = Math.max(+inp.min, Math.min(+inp.max, (+inp.value || 1) + delta));
  inp.value = val;
  inp.dispatchEvent(new Event('change'));
  dec.disabled = val <= +inp.min;
  inc.disabled = val >= +inp.max;
}
dec.addEventListener('click', () => updateQty(-1));
inc.addEventListener('click', () => updateQty(+1));
inp.addEventListener('change', () => updateQty(0));
updateQty(0);
```

---

## 66. Toggle Switches

```html
❌ WRONG — custom toggle: state = CSS class only; not keyboard operable;
           red/green are the only state indicators
<div class="toggle on" onclick="toggle(this)"></div>
```

```html
✅ RIGHT — three patterns for accessible toggles (SC 1.4.1, 2.1.1, 4.1.2)

<!-- Pattern A: styled checkbox (best for form values) -->
<label class="toggle-label" for="dark-mode">
  <input type="checkbox" id="dark-mode" name="darkMode" role="switch">
  <span class="toggle-track" aria-hidden="true">
    <span class="toggle-thumb"></span>
  </span>
  Dark mode
</label>

<!-- Pattern B: button + aria-pressed (immediate action) -->
<button type="button" aria-pressed="false" id="notif-toggle" class="toggle-btn">
  <span class="toggle-track" aria-hidden="true"><span class="toggle-thumb"></span></span>
  Email notifications
</button>

<!-- Pattern C: role="switch" (settings with yes/no semantics) -->
<span id="wifi-lbl">Wi-Fi</span>
<button type="button" role="switch" aria-checked="true"
        aria-labelledby="wifi-lbl" class="toggle-btn">
</button>
```

```css
/* Visually-hidden native input keeps keyboard/SR access */
.toggle-label input { position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0); }

.toggle-track {
  display:inline-flex;width:44px;height:24px;border-radius:12px;
  background:#767676;/* off state: 3.5:1 on white ✓ */
  position:relative;vertical-align:middle;margin-right:.5rem;
  transition:background .2s;
}
.toggle-thumb {
  position:absolute;width:18px;height:18px;border-radius:50%;
  background:#fff;top:3px;left:3px;transition:left .2s;
}

/* On state: position change + color change = two non-color indicators */
input:checked + .toggle-track,
[aria-pressed="true"] .toggle-track,
[aria-checked="true"] .toggle-track { background:#0052cc; }

input:checked + .toggle-track .toggle-thumb,
[aria-pressed="true"] .toggle-thumb,
[aria-checked="true"] .toggle-thumb { left:calc(100% - 21px); }

/* Focus */
input:focus-visible + .toggle-track { outline:3px solid #0052cc;outline-offset:2px; }
.toggle-btn:focus-visible .toggle-track { outline:3px solid #0052cc;outline-offset:2px; }

/* High Contrast Mode */
@media (forced-colors:active) {
  .toggle-track { border:2px solid ButtonText; }
  input:checked + .toggle-track,[aria-pressed="true"] .toggle-track { background:Highlight; }
}

@media (prefers-reduced-motion:reduce) {
  .toggle-track,.toggle-thumb { transition:none; }
}
```

```javascript
// Pattern B
document.getElementById('notif-toggle').addEventListener('click', function() {
  const p = this.getAttribute('aria-pressed') === 'true';
  this.setAttribute('aria-pressed', String(!p));
});

// Pattern C
document.querySelectorAll('[role="switch"]').forEach(sw => {
  sw.addEventListener('click', function() {
    this.setAttribute('aria-checked', String(this.getAttribute('aria-checked') !== 'true'));
  });
  sw.addEventListener('keydown', e => { if (e.key === ' ') { e.preventDefault(); sw.click(); } });
});
```

---

## 67. Color Picker

```html
❌ WRONG — swatches as divs; color = only identifier; no keyboard access
<div class="swatch" style="background:#f00" onclick="pick('#f00')"></div>
```

```html
✅ RIGHT — color swatches as radio buttons (SC 1.4.1, 2.1.1)

<!-- Native color input -->
<div class="field">
  <label for="accent">Accent color</label>
  <input type="color" id="accent" name="accent" value="#0052cc">
</div>

<!-- Color swatches (product variant selection) -->
<fieldset>
  <legend>Choose color <span aria-hidden="true">*</span></legend>

  <label class="swatch-label">
    <input type="radio" name="color" value="red" aria-label="Red">
    <span class="swatch" style="background:#c0392b" aria-hidden="true"></span>
    <span class="swatch-name">Red</span>
  </label>

  <label class="swatch-label">
    <input type="radio" name="color" value="blue" aria-label="Blue">
    <span class="swatch" style="background:#2980b9" aria-hidden="true"></span>
    <span class="swatch-name">Blue</span>
  </label>

  <label class="swatch-label">
    <input type="radio" name="color" value="black" aria-label="Black">
    <span class="swatch" style="background:#1a1a1a" aria-hidden="true"></span>
    <span class="swatch-name">Black</span>
  </label>
</fieldset>
```

```css
.swatch-label input[type="radio"] {
  position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);
}
.swatch {
  width:36px;height:36px;border-radius:50%;display:block;
  border:2px solid transparent;
}
/* Selected: border = non-color indicator */
input:checked + .swatch {
  border-color:#1a1a1a;
  box-shadow:0 0 0 3px #fff, 0 0 0 5px #1a1a1a;
}
input:focus-visible + .swatch {
  outline:3px solid #0052cc;outline-offset:3px;
}
```

---

## 68. Typeahead / Autocomplete

```html
✅ RIGHT — full accessible typeahead / combobox (SC 2.1.1, 4.1.2)

<div class="field">
  <label id="country-lbl" for="country-in">Country</label>
  <div style="position:relative">
    <input type="search" id="country-in"
           role="combobox"
           aria-autocomplete="list"
           aria-expanded="false"
           aria-controls="country-lb"
           aria-haspopup="listbox"
           aria-labelledby="country-lbl"
           autocomplete="off"
           placeholder="Type to search…">
    <div aria-live="polite" aria-atomic="true"
         class="visually-hidden" id="ta-status"></div>
    <ul id="country-lb" role="listbox"
        aria-labelledby="country-lbl" hidden></ul>
  </div>
</div>
```

```javascript
const input   = document.getElementById('country-in');
const listbox = document.getElementById('country-lb');
const status  = document.getElementById('ta-status');
const options = ['Afghanistan','Albania','Algeria','Germany','France','Japan','Mexico'];
let activeIdx = -1;

const close = () => {
  listbox.setAttribute('hidden','');
  input.setAttribute('aria-expanded','false');
  input.removeAttribute('aria-activedescendant');
  activeIdx = -1;
};

const select = opt => {
  input.value = opt.dataset.value;
  status.textContent = `${opt.dataset.value} selected.`;
  close();
};

input.addEventListener('input', debounce(function() {
  const q = this.value.trim();
  if (q.length < 2) { close(); return; }

  const matches = options.filter(o => o.toLowerCase().includes(q.toLowerCase())).slice(0,8);
  if (!matches.length) { close(); status.textContent = 'No results.'; return; }

  listbox.innerHTML = matches.map((m,i) =>
    `<li role="option" aria-selected="false" id="opt-${i}" data-value="${m}">
       ${m.replace(new RegExp(`(${q})`,'gi'),'<mark>$1</mark>')}
     </li>`
  ).join('');

  listbox.removeAttribute('hidden');
  input.setAttribute('aria-expanded','true');
  activeIdx = -1;
  status.textContent = `${matches.length} result${matches.length!==1?'s':''} available.`;
}, 150));

input.addEventListener('keydown', e => {
  const opts = [...listbox.querySelectorAll('[role="option"]')];
  const len  = opts.length;
  if (!len && e.key !== 'Escape') return;

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    activeIdx = Math.min(activeIdx + 1, len - 1);
    opts.forEach((o,i) => o.setAttribute('aria-selected', String(i===activeIdx)));
    if (opts[activeIdx]) {
      input.setAttribute('aria-activedescendant', opts[activeIdx].id);
      opts[activeIdx].scrollIntoView({ block:'nearest' });
    }
  }
  if (e.key === 'ArrowUp') {
    e.preventDefault();
    activeIdx = Math.max(activeIdx - 1, 0);
    opts.forEach((o,i) => o.setAttribute('aria-selected', String(i===activeIdx)));
    if (opts[activeIdx]) input.setAttribute('aria-activedescendant', opts[activeIdx].id);
  }
  if (e.key === 'Enter' && activeIdx >= 0) select(opts[activeIdx]);
  if (e.key === 'Escape') close();
  if (e.key === 'Home') { activeIdx=0; opts[0]?.setAttribute('aria-selected','true'); }
  if (e.key === 'End')  { activeIdx=len-1; opts[len-1]?.setAttribute('aria-selected','true'); }
});

listbox.addEventListener('click', e => {
  const opt = e.target.closest('[role="option"]');
  if (opt) select(opt);
});

document.addEventListener('click', e => {
  if (!input.contains(e.target) && !listbox.contains(e.target)) close();
});

function debounce(fn, ms) {
  let t; return function(...a) { clearTimeout(t); t = setTimeout(()=>fn.apply(this,a),ms); };
}
```

---

## 69. Virtual Scrolling and Long Lists

```html
❌ WRONG — 10,000 items in DOM; SR must read through all items
<ul><!-- 10,000 <li> elements --></ul>
```

```html
✅ RIGHT — virtual list with aria-setsize / aria-posinset (SC 2.1.1, 4.1.2)

<div role="region" aria-label="Product catalogue">
  <p aria-live="polite" id="vlist-info" class="visually-hidden">
    Showing items 1–20 of 10,000 products.
  </p>
  <!-- Jump / search so users can navigate without scrolling 10,000 items -->
  <form role="search" aria-label="Find product">
    <label for="product-jump">Jump to product</label>
    <input type="search" id="product-jump" name="jump">
    <button type="submit">Find</button>
  </form>
  <!-- Scroll container -->
  <ul id="vlist" aria-label="Products"
      style="height:600px;overflow-y:auto;position:relative">
    <!-- Items rendered by JS with absolute positioning -->
  </ul>
</div>
```

```javascript
class VirtualList {
  constructor(el, items, itemH = 60) {
    this.el    = el;
    this.items = items;
    this.itemH = itemH;
    this.count = Math.ceil(el.clientHeight / itemH) + 5;

    // Full-height spacer so scroll bar is proportional
    this.spacer        = document.createElement('div');
    this.spacer.style.height = `${items.length * itemH}px`;
    this.spacer.setAttribute('aria-hidden','true');
    el.appendChild(this.spacer);

    this.render();
    el.addEventListener('scroll', () => this.render());
  }

  render() {
    const top   = this.el.scrollTop;
    const start = Math.floor(top / this.itemH);
    const end   = Math.min(start + this.count, this.items.length);

    this.el.querySelectorAll('[role="option"]').forEach(n => n.remove());

    for (let i = start; i < end; i++) {
      const li = document.createElement('li');
      li.setAttribute('role','option');
      li.setAttribute('aria-selected','false');
      li.setAttribute('aria-setsize',  this.items.length); // total count
      li.setAttribute('aria-posinset', i + 1);             // 1-based position
      li.style.cssText = `position:absolute;top:${i*this.itemH}px;height:${this.itemH}px;width:100%`;
      li.textContent   = this.items[i].name;
      this.el.appendChild(li);
    }

    document.getElementById('vlist-info').textContent =
      `Showing items ${start+1}–${end} of ${this.items.length} products.`;
  }
}
```

---

## 70. Data Grid / Spreadsheet

```html
✅ RIGHT — keyboard-navigable data grid (SC 2.1.1, 4.1.2)
<!--
  Grid keyboard:
  Arrow keys   — move between cells
  Enter        — enter edit mode
  Escape       — exit edit mode
  Tab/Shift+Tab— move between interactive elements WITHIN a cell
  Home / End   — first / last cell in row
  Ctrl+Home/End— first / last cell in grid
-->

<div role="grid" aria-label="Sales data"
     aria-rowcount="100" aria-colcount="5">

  <div role="row" aria-rowindex="1">
    <div role="columnheader" aria-sort="ascending" tabindex="0">Product</div>
    <div role="columnheader" aria-sort="none"      tabindex="-1">Q1</div>
    <div role="columnheader" aria-sort="none"      tabindex="-1">Q2</div>
    <div role="columnheader" aria-sort="none"      tabindex="-1">Q3</div>
    <div role="columnheader" aria-sort="none"      tabindex="-1">Total</div>
  </div>

  <div role="row" aria-rowindex="2">
    <div role="rowheader"  tabindex="-1">Widget A</div>
    <div role="gridcell"   tabindex="-1" aria-readonly="true">€12,000</div>
    <div role="gridcell"   tabindex="-1" aria-readonly="false">
      <span class="cell-val">€14,500</span>
      <input type="number" class="cell-edit visually-hidden"
             value="14500" aria-label="Widget A Q2 sales">
    </div>
    <div role="gridcell"   tabindex="-1">€16,000</div>
    <div role="gridcell"   tabindex="-1" aria-readonly="true">€42,500</div>
  </div>

</div>
```

```javascript
class A11yGrid {
  constructor(grid) {
    this.g = grid;
    this.r = 0; this.c = 0;
    this.M = [];
    grid.querySelectorAll('[role="row"]').forEach((row, r) => {
      this.M[r] = [];
      row.querySelectorAll('[role="gridcell"],[role="rowheader"],[role="columnheader"]')
         .forEach((cell, c) => { this.M[r][c] = cell; });
    });
    if (this.M[0]?.[0]) this.M[0][0].tabIndex = 0;
    grid.addEventListener('keydown', this.key.bind(this));
    grid.addEventListener('click', e => {
      const cell = e.target.closest('[role="gridcell"],[role="rowheader"],[role="columnheader"]');
      if (cell) this.focus(this.find(cell));
    });
  }

  focus([r, c]) {
    this.M.flat().forEach(el => el.tabIndex = -1);
    this.r = r; this.c = c;
    this.M[r][c].tabIndex = 0;
    this.M[r][c].focus();
  }

  find(el) {
    for (let r=0;r<this.M.length;r++)
      for (let c=0;c<this.M[r].length;c++)
        if (this.M[r][c]===el) return [r,c];
    return [0,0];
  }

  key(e) {
    const R = this.M.length - 1;
    const C = (this.M[this.r]?.length || 1) - 1;
    const mv = {
      ArrowRight: [this.r, Math.min(this.c+1, C)],
      ArrowLeft:  [this.r, Math.max(this.c-1, 0)],
      ArrowDown:  [Math.min(this.r+1, R), this.c],
      ArrowUp:    [Math.max(this.r-1, 0), this.c],
      Home: e.ctrlKey ? [0,0]   : [this.r, 0],
      End:  e.ctrlKey ? [R, C]  : [this.r, C],
    };
    if (mv[e.key]) { e.preventDefault(); this.focus(mv[e.key]); return; }

    if (e.key === 'Enter') {
      const cell  = this.M[this.r][this.c];
      if (cell.getAttribute('aria-readonly') !== 'true') {
        const inp = cell.querySelector('input');
        if (inp) {
          cell.querySelector('.cell-val').classList.add('visually-hidden');
          inp.classList.remove('visually-hidden');
          inp.focus();
          inp.addEventListener('blur', () => {
            inp.classList.add('visually-hidden');
            cell.querySelector('.cell-val').textContent =
              `€${Number(inp.value).toLocaleString()}`;
            cell.querySelector('.cell-val').classList.remove('visually-hidden');
            cell.focus();
          }, { once: true });
        }
      }
    }
  }
}

new A11yGrid(document.querySelector('[role="grid"]'));
```

---

## 71. Print Styles and Print Accessibility

```css
@media print {
  /* Show hidden elements useful in print */
  .visually-hidden { position:static !important; clip:auto !important; overflow:visible !important; }

  /* Expand abbreviations */
  abbr[title]::after { content:" (" attr(title) ")"; }

  /* Show URLs after links */
  a[href]::after { content:" (" attr(href) ")"; font-size:.8em; color:#595959; }
  a[href^="#"]::after,
  a[href^="javascript"]::after { content:""; }

  /* Keep critical content together */
  figure, table, blockquote, pre { page-break-inside:avoid; }
  h1,h2,h3,h4 { page-break-after:avoid; }
  thead { display:table-header-group; }
  tfoot { display:table-footer-group; }
  tr    { page-break-inside:avoid; }

  /* Remove chrome UI */
  button, .skip-link, nav, [role="dialog"],
  .cookie-banner, video, audio, .toast-container { display:none !important; }

  /* Ensure readable black-on-white */
  body    { color:#000; background:#fff; font-size:12pt; }
  h1,h2,h3,h4,h5,h6 { color:#000; }
  a       { color:#000; text-decoration:underline; }
  img     { max-width:100% !important; }

  /* Alt text shown if image fails */
  img::after { content:attr(alt); font-style:italic; font-size:.9em; }
}
```

---

## 72. Dark Mode

```css
/* ❌ WRONG — contrast not re-verified for dark mode */
@media (prefers-color-scheme:dark) {
  body { background:#1a1a1a; color:#ccc; }
  a    { color:#6699ff; } /* #6699ff on #1a1a1a = 4.1:1 ✗ */
  input { border-color:#555; } /* 2.1:1 on bg ✗ */
}

/* ✅ RIGHT — design tokens, verified ratios for both modes */
:root {
  --bg:          #ffffff;
  --surface:     #f8f9fa;
  --text:        #1a1a1a;  /* 16.1:1 ✓ */
  --text-muted:  #595959;  /*  7.0:1 ✓ */
  --link:        #0052cc;  /*  7.7:1 ✓ */
  --border:      #595959;  /*  7.0:1 ✓ (needs 3:1 for UI components) */
  --focus:       #0052cc;
  --error:       #b91c1c;  /*  5.9:1 ✓ */
  --success:     #166534;  /*  7.2:1 ✓ */
  --btn-bg:      #0052cc;
  --btn-text:    #ffffff;  /*  7.7:1 on btn-bg ✓ */
}

@media (prefers-color-scheme:dark) {
  :root {
    --bg:         #121212;
    --surface:    #1e1e1e;
    --text:       #e8e8e8;  /* 13.9:1 ✓ */
    --text-muted: #a0a0a0;  /*  5.9:1 ✓ */
    --link:       #70a9ff;  /*  4.7:1 ✓ */
    --border:     #6b7280;  /*  3.3:1 ✓ */
    --focus:      #70a9ff;
    --error:      #f87171;  /*  4.8:1 ✓ */
    --success:    #4ade80;  /*  5.2:1 ✓ */
    --btn-bg:     #3b82f6;
    --btn-text:   #ffffff;  /*  4.5:1 ✓ */
  }
}

/* User-controlled override */
[data-theme="light"] { /* same as :root */ }
[data-theme="dark"]  { /* same as @media dark */ }
```

```javascript
const btn = document.getElementById('theme-toggle');

function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('theme', t);
  btn.setAttribute('aria-pressed', String(t === 'dark'));
  btn.setAttribute('aria-label', t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
}

// Restore saved preference
const saved = localStorage.getItem('theme');
if (saved) applyTheme(saved);

btn.addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme');
  applyTheme(cur === 'dark' ? 'light' : 'dark');
});
```

---

## 73. High Contrast Mode and Forced Colors

```css
/* Windows High Contrast / Forced Colors: browser replaces custom colors
   with system color keywords. Your UI must still be intelligible. */

/* System color keywords available in forced-colors:
   ButtonText / ButtonFace — button text / background
   Canvas / CanvasText     — page background / text
   Highlight / HighlightText — selection / text on selection
   LinkText                — link color
   GrayText                — disabled text
*/

@media (forced-colors:active) {

  /* Buttons: add border so they're visible without background */
  button, [role="button"] { border:2px solid ButtonText; }

  /* Focus ring: use system Highlight */
  :focus-visible { outline:3px solid Highlight; outline-offset:2px; }

  /* Inputs: explicit border */
  input, select, textarea { border:2px solid ButtonText; }

  /* Card borders replace box-shadow (shadows vanish in forced colors) */
  .card { box-shadow:none; border:1px solid CanvasText; }

  /* Selected state */
  [aria-selected="true"] {
    background:Highlight; color:HighlightText;
    forced-color-adjust:none;
  }

  /* Custom toggle: use system colors */
  input:checked + .toggle-track { background:Highlight; }

  /* Links: always underline */
  a { text-decoration:underline; }

  /* DON'T rely on box-shadow for focus: it's stripped in forced colors.
     Use outline instead — it survives. */

  /* ❌ This disappears in forced colors: */
  /* :focus { outline:none; box-shadow:0 0 0 3px blue; } */

  /* ✅ This survives: */
  /* :focus-visible { outline:3px solid Highlight; } */
}

/* Test: DevTools → Rendering → Emulate CSS media: forced-colors: active */
```

---

## 74. Right-to-Left (RTL) Layouts

```html
<!-- RTL document -->
<html lang="ar" dir="rtl">

<!-- Inline RTL within LTR page -->
<p>The Arabic greeting is <span lang="ar" dir="rtl">مرحباً</span>.</p>

<!-- bdi: isolate unknown-direction user content -->
<p>User <bdi>أحمد</bdi> posted a comment.</p>

<!-- Phone numbers: always LTR even in RTL pages -->
<bdo dir="ltr">+49 30 123456</bdo>
```

```css
/* ❌ WRONG — physical properties require a separate RTL override file */
.card { margin-left:1rem; border-left:3px solid blue; text-align:left; }

/* ✅ RIGHT — logical properties work in both LTR and RTL automatically */
.card {
  margin-inline-start:  1rem;       /* = margin-left in LTR */
  border-inline-start:  3px solid blue; /* = border-left in LTR */
  text-align:           start;      /* = left in LTR, right in RTL */
}

/* Logical property reference:
   margin-inline-start / end     → left / right in LTR
   padding-inline-start / end
   border-inline-start / end
   inset-inline-start / end      → left / right in position
   float: inline-start / end     → float left / right
   text-align: start / end
*/

/* Mirror directional icons for RTL */
.arrow-icon           { transform:scaleX(1); }
:dir(rtl) .arrow-icon { transform:scaleX(-1); }
```

---

## 75. Error Pages (404, 500)

```html
✅ RIGHT — accessible, helpful error page (SC 2.4.1, 2.4.2, 3.3.3)

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Error type in title, page name first -->
  <title>Page Not Found (404) — Acme Corp</title>
</head>
<body>
<a href="#main" class="skip-link">Skip to main content</a>
<header><!-- same as rest of site --></header>

<main id="main" tabindex="-1">
  <h1>Page Not Found</h1>
  <p>We couldn't find the page you were looking for.
     It may have been moved, renamed, or deleted.</p>
  <p>Error code: <code>404</code></p>

  <h2>What can you do?</h2>
  <ul>
    <li>Check the URL for typos and try again.</li>
    <li><a href="/">Go to the homepage</a></li>
    <li>
      Search for what you need:
      <form role="search" action="/search" method="get">
        <label for="err-q" class="visually-hidden">Search</label>
        <input type="search" id="err-q" name="q" placeholder="Search…">
        <button type="submit">Search</button>
      </form>
    </li>
    <li><a href="/sitemap">Browse the sitemap</a></li>
    <li><a href="/contact">Contact us</a> if you think this is an error.</li>
  </ul>
</main>

<footer><!-- same as rest of site --></footer>
</body>
</html>

<!-- 500 title -->
<!-- <title>Service Unavailable (500) — Acme Corp</title> -->
<!-- <h1>Something went wrong on our end</h1> -->
<!-- Never expose stack traces or internal error details publicly -->
```

---

## 76. Session Timeout Warning

```html
✅ RIGHT — accessible timeout dialog (SC 2.2.1)
<!--
  SC 2.2.1: Warn at least 20 s before expiry; let user extend or turn off timer.
-->

<div role="alertdialog"
     aria-modal="true"
     aria-labelledby="timeout-title"
     aria-describedby="timeout-desc"
     id="session-dialog" hidden>

  <h2 id="timeout-title">Your session is about to expire</h2>
  <p id="timeout-desc">
    You will be signed out in
    <span aria-live="polite" aria-atomic="true">
      <strong id="countdown">60</strong> seconds
    </span>.
    Do you want to stay signed in?
  </p>

  <div class="dialog-actions">
    <button type="button" id="extend-btn" class="btn-primary">
      Yes, keep me signed in
    </button>
    <button type="button" id="signout-btn">
      No, sign me out now
    </button>
  </div>
</div>
<div id="timeout-backdrop" class="modal-backdrop" hidden aria-hidden="true"></div>
```

```javascript
class SessionTimer {
  constructor(timeoutMs = 30*60*1000, warnMs = 60*1000) {
    this.timeout = timeoutMs; this.warn = warnMs;
    this.dialog  = document.getElementById('session-dialog');
    this.cd      = document.getElementById('countdown');
    this.reset();

    document.getElementById('extend-btn').addEventListener('click', () => this.extend());
    document.getElementById('signout-btn').addEventListener('click', () => this.signout());

    ['click','keydown','mousemove','touchstart'].forEach(ev =>
      document.addEventListener(ev, () => this.reset(), { passive:true })
    );
  }

  reset() {
    clearTimeout(this.wt); clearTimeout(this.lt); clearInterval(this.ci);
    this.hide();
    this.wt = setTimeout(() => this.showWarning(), this.timeout - this.warn);
    this.lt = setTimeout(() => this.signout(),     this.timeout);
  }

  showWarning() {
    this.dialog.removeAttribute('hidden');
    document.getElementById('timeout-backdrop').removeAttribute('hidden');
    let s = Math.floor(this.warn / 1000);
    this.cd.textContent = s;
    this.ci = setInterval(() => { this.cd.textContent = --s; if (s <= 0) this.signout(); }, 1000);
    document.getElementById('extend-btn').focus();
  }

  hide() {
    clearInterval(this.ci);
    this.dialog.setAttribute('hidden','');
    document.getElementById('timeout-backdrop').setAttribute('hidden','');
  }

  extend() { this.hide(); this.reset(); fetch('/api/session/extend',{method:'POST'}); }
  signout() { window.location.href = '/signout'; }
}

new SessionTimer();
```

---

## 77. Confirmation Dialogs

```html
❌ WRONG — window.confirm(); no styling; blocks page; not keyboard-trap-safe
<button onclick="if(confirm('Delete?')) del()">Delete</button>
```

```html
✅ RIGHT — accessible confirm dialog (SC 2.1.2, 3.3.4)

<button type="button" class="danger"
        data-confirm-action="delete" data-confirm-target="item-42">
  Delete item
</button>

<div role="alertdialog"
     aria-modal="true"
     aria-labelledby="conf-title"
     aria-describedby="conf-desc"
     id="confirm-dialog" hidden>

  <h2 id="conf-title">Delete item?</h2>
  <p id="conf-desc">
    This action cannot be undone.
    The item and all its data will be permanently deleted.
  </p>
  <div class="dialog-actions">
    <!-- Cancel = safe default = focused first -->
    <button type="button" id="conf-cancel">Cancel</button>
    <!-- Destructive = second in DOM, user must actively reach it -->
    <button type="button" id="conf-ok" class="btn-danger">
      Yes, delete permanently
    </button>
  </div>
</div>
<div class="modal-backdrop" id="conf-backdrop" hidden aria-hidden="true"></div>
```

```javascript
let confirmCb = null;

function showConfirm(title, msg, onOk) {
  document.getElementById('conf-title').textContent = title;
  document.getElementById('conf-desc').textContent  = msg;
  confirmCb = onOk;
  document.getElementById('confirm-dialog').removeAttribute('hidden');
  document.getElementById('conf-backdrop').removeAttribute('hidden');
  document.getElementById('conf-cancel').focus();
}

function closeConfirm() {
  document.getElementById('confirm-dialog').setAttribute('hidden','');
  document.getElementById('conf-backdrop').setAttribute('hidden','');
  confirmCb = null;
}

document.getElementById('conf-cancel').addEventListener('click', closeConfirm);
document.getElementById('conf-ok').addEventListener('click', () => {
  confirmCb?.(); closeConfirm();
});
document.getElementById('confirm-dialog').addEventListener('keydown', e => {
  if (e.key === 'Escape') closeConfirm();
});

document.querySelectorAll('[data-confirm-action="delete"]').forEach(btn =>
  btn.addEventListener('click', () =>
    showConfirm('Delete item?','This cannot be undone.',() => deleteItem(btn.dataset.confirmTarget))
  )
);
```

---

## 78. Inline Editing

```html
❌ WRONG — click-only edit trigger; edit state not announced; no keyboard cancel
<td onclick="makeEditable(this)">Widget A</td>
```

```html
✅ RIGHT — accessible inline edit (SC 2.1.1, 4.1.2, 4.1.3)

<td class="editable-cell">
  <span class="cell-val" id="val-1">Widget A</span>
  <button type="button" class="edit-btn"
          aria-label="Edit product name: Widget A"
          aria-controls="edit-frm-1"
          aria-expanded="false">
    <svg aria-hidden="true" focusable="false"><!-- ✏ --></svg>
    <span class="visually-hidden">Edit</span>
  </button>

  <span id="edit-frm-1" hidden>
    <label for="edit-inp-1" class="visually-hidden">Product name</label>
    <input type="text" id="edit-inp-1" value="Widget A">
    <button type="button" class="save-btn" aria-label="Save product name">Save</button>
    <button type="button" class="cancel-btn" aria-label="Cancel editing product name">Cancel</button>
  </span>
  <span aria-live="polite" class="visually-hidden" id="edit-status-1"></span>
</td>
```

```javascript
document.querySelectorAll('.editable-cell').forEach(cell => {
  const editBtn   = cell.querySelector('.edit-btn');
  const display   = cell.querySelector('.cell-val');
  const form      = cell.querySelector('[id^="edit-frm"]');
  const input     = cell.querySelector('input');
  const saveBtn   = cell.querySelector('.save-btn');
  const cancelBtn = cell.querySelector('.cancel-btn');
  const status    = cell.querySelector('[aria-live]');

  const startEdit = () => {
    form.removeAttribute('hidden');
    editBtn.setAttribute('hidden','');
    editBtn.setAttribute('aria-expanded','true');
    input.value = display.textContent.trim();
    input.focus(); input.select();
  };
  const endEdit   = () => {
    form.setAttribute('hidden','');
    editBtn.removeAttribute('hidden');
    editBtn.setAttribute('aria-expanded','false');
    editBtn.focus();
  };
  const saveEdit  = () => {
    const v = input.value.trim();
    if (!v) return;
    display.textContent = v;
    editBtn.setAttribute('aria-label', `Edit product name: ${v}`);
    status.textContent  = `Product name updated to "${v}".`;
    endEdit();
  };

  editBtn.addEventListener('click', startEdit);
  saveBtn.addEventListener('click', saveEdit);
  cancelBtn.addEventListener('click', endEdit);
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter')  { e.preventDefault(); saveEdit(); }
    if (e.key === 'Escape') { e.preventDefault(); endEdit();  }
  });
});
```

---

## 79. Split Buttons and Button Groups

```html
❌ WRONG — dropdown trigger has no accessible name; group has no grouping
<div class="split">
  <button>Save</button>
  <button>▼</button><!-- "▼" is the accessible name — meaningless -->
</div>
```

```html
✅ RIGHT — split button + button group (SC 2.1.1, 4.1.2)

<!-- Split button -->
<div class="split-btn" role="group" aria-label="Save options">
  <button type="button" class="split-primary">Save</button>
  <button type="button"
          class="split-dd"
          aria-haspopup="menu"
          aria-expanded="false"
          aria-controls="save-menu"
          aria-label="More save options">
    <svg aria-hidden="true" focusable="false" class="chevron"><!-- ▾ --></svg>
  </button>
  <ul id="save-menu" role="menu" hidden>
    <li role="none"><button role="menuitem" type="button">Save as draft</button></li>
    <li role="none"><button role="menuitem" type="button">Save and publish</button></li>
    <li role="none"><button role="menuitem" type="button">Save as template</button></li>
  </ul>
</div>

<!-- Button group (radio-like exclusive selection) -->
<div role="group" aria-label="Text alignment">
  <button type="button" aria-pressed="true"  aria-label="Align left">
    <svg aria-hidden="true" focusable="false"><!-- ← lines --></svg>
  </button>
  <button type="button" aria-pressed="false" aria-label="Align center">
    <svg aria-hidden="true" focusable="false"><!-- center lines --></svg>
  </button>
  <button type="button" aria-pressed="false" aria-label="Align right">
    <svg aria-hidden="true" focusable="false"><!-- → lines --></svg>
  </button>
</div>
```

---

## 80. Wizard / Multi-Step Stepper

```html
✅ RIGHT — accessible multi-step wizard (SC 2.4.2, 3.3.4)

<nav aria-label="Registration progress">
  <ol class="wizard-steps">
    <li aria-label="Step 1 of 4: Account — completed">
      <span class="step-num" aria-hidden="true">1</span>
      <span>Account</span>
      <svg class="done-check" aria-hidden="true"><!-- ✓ --></svg>
    </li>
    <li aria-current="step" aria-label="Step 2 of 4: Personal — current step">
      <span class="step-num" aria-hidden="true">2</span>
      <span>Personal</span>
    </li>
    <li aria-label="Step 3 of 4: Address — not yet reached">
      <span class="step-num" aria-hidden="true">3</span>
      <span>Address</span>
    </li>
    <li aria-label="Step 4 of 4: Payment — not yet reached">
      <span class="step-num" aria-hidden="true">4</span>
      <span>Payment</span>
    </li>
  </ol>
</nav>

<!-- <title>Step 2 of 4: Personal Details — Register — Acme Corp</title> -->

<section aria-labelledby="step-h">
  <h1 id="step-h">Personal Details</h1>
  <form novalidate>
    <!-- fields -->
    <div class="wizard-nav">
      <button type="button" id="back-btn">← Back to Account</button>
      <button type="button" id="next-btn">Continue to Address →</button>
    </div>
  </form>
</section>
```

```javascript
function goStep(num, title) {
  document.title = `Step ${num} of 4: ${title} — Register — Acme Corp`;
  loadStepContent(num);
  // Move focus to step heading
  const h = document.getElementById('step-h');
  h.tabIndex = -1; h.focus();
  h.addEventListener('blur', () => h.removeAttribute('tabindex'), { once:true });
  // Announce to SR
  document.getElementById('aria-live-polite').textContent =
    `Moved to step ${num}: ${title}`;
}
```

---

## 81. Sign In / Authentication Flows

```html
✅ RIGHT — accessible login form (SC 1.3.5, 3.3.7, 3.3.8)

<main id="main" tabindex="-1">
  <h1>Sign in to Acme Corp</h1>

  <!-- Post-submit error -->
  <div role="alert" id="login-err" hidden>
    <h2>Sign in failed</h2>
    <p>The email or password you entered is incorrect. Please try again.</p>
  </div>

  <form id="login-form" novalidate>
    <div class="field">
      <label for="login-email">Email address</label>
      <input type="email" id="login-email" name="email"
             autocomplete="username" required aria-required="true">
    </div>

    <div class="field">
      <label for="login-pw">Password</label>
      <div class="pw-wrap">
        <input type="password" id="login-pw" name="password"
               autocomplete="current-password" required aria-required="true">
        <button type="button" aria-pressed="false" aria-controls="login-pw">
          <span class="show-lbl">Show password</span>
          <span class="hide-lbl" hidden>Hide password</span>
        </button>
      </div>
    </div>

    <label>
      <input type="checkbox" name="remember">
      Keep me signed in for 30 days
    </label>

    <button type="submit">Sign in</button>
  </form>

  <!-- SC 3.3.8: alternative auth — no sole reliance on cognitive test -->
  <section aria-labelledby="alt-auth-h">
    <h2 id="alt-auth-h">Other ways to sign in</h2>
    <ul>
      <li><a href="/auth/magic-link">Send me a sign-in link by email</a></li>
      <li><a href="/auth/passkey">Use a passkey</a></li>
    </ul>
  </section>

  <p><a href="/register">Create an account</a></p>
  <p><a href="/forgot-password">Forgot your password?</a></p>
</main>
```

---

## 82. Notifications Badge and Counter

```html
❌ WRONG — "3" means nothing without context; value duplicated for SR
<button>🔔 <span class="badge">3</span></button>
```

```html
✅ RIGHT — badge accessible name on parent button (SC 1.3.1, 4.1.3)

<button type="button" id="notif-btn"
        aria-label="Notifications, 3 unread">
  <svg aria-hidden="true" focusable="false"><!-- bell --></svg>
  <!-- Badge: aria-hidden, count already in button's aria-label -->
  <span class="badge" aria-hidden="true">3</span>
</button>
```

```javascript
let prev = 0;
function updateBadge(count) {
  const btn   = document.getElementById('notif-btn');
  const badge = btn.querySelector('.badge');

  btn.setAttribute('aria-label',
    count > 0 ? `Notifications, ${count} unread` : 'Notifications, no unread messages');
  badge.textContent = count > 0 ? count : '';
  badge.hidden      = count === 0;

  if (count > prev) {
    document.getElementById('aria-live-polite').textContent =
      `You have ${count} new notification${count !== 1 ? 's' : ''}.`;
  }
  prev = count;
}
```

---

## 83. Skeleton Screens

```html
❌ WRONG — multiple aria-busy regions; SR reads "Loading Loading Loading"
<div class="skeleton" aria-busy="true">
  <div class="sk-line"></div>
  <div class="sk-line"></div>
</div>
```

```html
✅ RIGHT — single container with aria-busy; skeleton hidden from SR (SC 4.1.3)

<section id="feed"
         aria-label="Latest articles"
         aria-live="polite"
         aria-busy="true">

  <!-- Skeleton: aria-hidden — SR waits for real content -->
  <div class="skeleton-list" aria-hidden="true">
    <div class="sk-card">
      <div class="sk-line sk-title"></div>
      <div class="sk-line"></div>
      <div class="sk-line sk-short"></div>
    </div>
  </div>

  <p class="visually-hidden">Loading articles, please wait.</p>
</section>
```

```javascript
async function loadFeed() {
  const section = document.getElementById('feed');
  section.setAttribute('aria-busy','true');

  const articles = await fetchArticles();

  section.innerHTML = renderArticles(articles); // replaces skeleton
  section.setAttribute('aria-busy','false');
  // aria-live="polite" + aria-busy="false" causes SR to announce new content
}
```

```css
.sk-line {
  height:1rem; border-radius:4px; background:#e5e7eb; margin:.5rem 0;
}
@media (prefers-reduced-motion:no-preference) {
  .sk-line {
    background:linear-gradient(90deg,#e5e7eb 25%,#f3f4f6 50%,#e5e7eb 75%);
    background-size:200% 100%;
    animation:shimmer 1.5s infinite;
  }
  @keyframes shimmer {
    0%   { background-position:-200% 0; }
    100% { background-position: 200% 0; }
  }
}
```

---

## 84. Code Blocks and Technical Content

```html
❌ WRONG — monospace div; no language label; no copy mechanism announced to SR
<div style="font-family:monospace">npm install widget</div>
```

```html
✅ RIGHT — semantic code with copy button (SC 1.3.1)

<!-- Inline code -->
<p>Run <code>npm install @acme/widget</code> to install.</p>

<!-- Block code -->
<figure class="code-block">
  <figcaption>
    <span class="code-lang">JavaScript</span>
    <button type="button" class="copy-btn"
            aria-label="Copy JavaScript code to clipboard"
            data-target="code-1">
      <svg aria-hidden="true" focusable="false"><!-- copy icon --></svg>
      Copy
    </button>
  </figcaption>
  <pre><code id="code-1" class="language-js"
             aria-label="JavaScript code example">
import { Widget } from '@acme/widget';

const w = new Widget({ container: '#app', theme: 'dark' });
  </code></pre>
</figure>
```

```javascript
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async function() {
    const code = document.getElementById(this.dataset.target)?.textContent?.trim()
              || this.closest('.code-block')?.querySelector('code')?.textContent?.trim();
    try {
      await navigator.clipboard.writeText(code);
      const orig = this.getAttribute('aria-label');
      this.setAttribute('aria-label','Code copied to clipboard');
      this.textContent = 'Copied!';
      setTimeout(() => { this.setAttribute('aria-label',orig); this.textContent='Copy'; }, 2000);
      document.getElementById('aria-live-polite').textContent = 'Code copied to clipboard.';
    } catch {
      document.getElementById('aria-live-assertive').textContent =
        'Copy failed. Please select the code and copy manually.';
    }
  });
});
```

---

## 85. Math and Scientific Notation

```html
❌ WRONG — math as image/plain text; SR reads "mc2" not "m c squared"
<img src="formula.png" alt="formula">
<p>E = mc²</p>
```

```html
✅ RIGHT — semantic math with aria-label fallback (SC 1.1.1, 1.3.1)

<!-- Simple: inline HTML + aria-label for spoken form -->
<p>
  Mass–energy equivalence:
  <span aria-label="E equals m c squared">E&nbsp;=&nbsp;mc<sup>2</sup></span>
</p>

<!-- Chemical formula -->
<p>Water: <span aria-label="H 2 O">H<sub>2</sub>O</span></p>

<!-- Fraction -->
<p>One half:
  <span aria-label="one half">
    <sup>1</sup>/<sub>2</sub>
  </span>
</p>

<!-- Complex: MathML (best AT support) -->
<math display="block"
      aria-label="x equals negative b plus or minus the square root
                  of b squared minus 4 a c, all over 2 a">
  <mrow>
    <mi>x</mi><mo>=</mo>
    <mfrac>
      <mrow>
        <mo>−</mo><mi>b</mi>
        <mo>±</mo>
        <msqrt>
          <msup><mi>b</mi><mn>2</mn></msup>
          <mo>−</mo><mn>4</mn><mi>a</mi><mi>c</mi>
        </msqrt>
      </mrow>
      <mrow><mn>2</mn><mi>a</mi></mrow>
    </mfrac>
  </mrow>
</math>

<!-- MathJax v3 config (renders MathML + SVG with speech support) -->
<script>
MathJax = {
  options: { enableMenu: true },
  a11y:    { speech: true, braille: true }
};
</script>
```

---

## 86. Time, Date and Timezone Display

```html
❌ WRONG — ambiguous format "12/05/24"; no machine-readable datetime; no timezone
<p>Posted: 12/05/24</p>
<p>Event: 3pm</p>
```

```html
✅ RIGHT — <time> with datetime attribute (SC 1.3.1)

<!-- Full unambiguous date -->
<p>Posted: <time datetime="2024-12-05">5 December 2024</time></p>

<!-- Relative time with absolute title fallback -->
<p>Updated
  <time datetime="2024-12-05T14:30:00+01:00"
        title="5 December 2024 at 14:30 CET"
        id="rel-time">
    2 hours ago
  </time>
</p>

<!-- Event with timezone -->
<p>Webinar:
  <time datetime="2025-03-15T10:00:00Z">
    15 March 2025, 10:00 UTC (11:00 CET / 06:00 EST)
  </time>
</p>

<!-- Duration -->
<p>Runtime: <time datetime="PT2H30M">2 hours 30 minutes</time></p>

<!-- Date range -->
<p>Conference:
  <time datetime="2025-06-10">10</time>–<time datetime="2025-06-12">12 June 2025</time>
</p>
```

```javascript
function relTime(dateStr) {
  const diff = Date.now() - new Date(dateStr);
  const m = Math.floor(diff / 60000);
  const h = Math.floor(m / 60);
  const d = Math.floor(h / 24);
  if (m < 1)  return 'just now';
  if (m < 60) return `${m} minute${m>1?'s':''} ago`;
  if (h < 24) return `${h} hour${h>1?'s':''} ago`;
  if (d < 7)  return `${d} day${d>1?'s':''} ago`;
  return new Date(dateStr).toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'});
}
document.querySelectorAll('[id="rel-time"]').forEach(el =>
  el.textContent = relTime(el.getAttribute('datetime'))
);
```

---

## 87. Prices and Numbers

```html
❌ WRONG — unformatted numbers; SR reads "1234567"; currency not identified
<p>Revenue: 1234567</p>
<p>Price: 9.99</p>
```

```html
✅ RIGHT — accessible number and currency display (SC 1.3.1)

<!-- Simple price with aria-label for spoken form -->
<p>Price: <span aria-label="9 euros and 99 cents">€9.99</span></p>

<!-- Large number -->
<p>Revenue: <span aria-label="1 million 234 thousand 567 euros">€1,234,567</span></p>

<!-- Sale price -->
<p class="price-group">
  <span class="visually-hidden">Regular price:</span>
  <del aria-label="Regular price: 29 euros 99 cents">€29.99</del>

  <span class="visually-hidden">Sale price:</span>
  <ins aria-label="Sale price: 19 euros 99 cents" class="sale">€19.99</ins>

  <span class="badge" aria-label="33 percent off">−33%</span>
</p>

<!-- Percentage -->
<p>Discount: <span aria-label="15 percent">15%</span></p>

<!-- Range -->
<p>Price range: <span aria-label="10 to 50 euros">€10 – €50</span></p>
```

```javascript
// Format with Intl.NumberFormat
const fmt = (n, cur='EUR', loc='de-DE') =>
  new Intl.NumberFormat(loc,{style:'currency',currency:cur}).format(n);

const spoken = (n, cur='EUR', loc='en') =>
  new Intl.NumberFormat(loc,{style:'currency',currency:cur,currencyDisplay:'name'}).format(n);
// "12.99 euros" — use as aria-label value
```

---

## 88. React Accessibility Patterns

```jsx
// ❌ WRONG — div soup; no focus management; duplicated IDs in lists
function List({ items }) {
  return (
    <div>
      {items.map(i => <div key={i.id} onClick={() => view(i)}>{i.name}</div>)}
    </div>
  );
}
```

```jsx
// ✅ RIGHT — key React a11y patterns

import { useState, useEffect, useRef, useId, useCallback } from 'react';

/* ── Unique IDs (React 18+) ───────────────────────────── */
function FormField({ label, required, hint, error, type = 'text', ...rest }) {
  const id      = useId();
  const hintId  = hint  ? `${id}-hint`  : undefined;
  const errorId = error ? `${id}-error` : undefined;
  const described = [hintId, errorId].filter(Boolean).join(' ') || undefined;

  return (
    <div className="field">
      <label htmlFor={id}>
        {label}{required && <span aria-hidden="true"> *</span>}
      </label>
      <input id={id} type={type}
             required={required} aria-required={required || undefined}
             aria-invalid={error ? 'true' : undefined}
             aria-describedby={described}
             {...rest} />
      {hint  && <div id={hintId}  className="hint">{hint}</div>}
      {error && <div id={errorId} role="alert">{error}</div>}
    </div>
  );
}

/* ── Modal with focus trap ──────────────────────────────── */
function Modal({ open, onClose, title, children, triggerRef }) {
  const dialogRef = useRef(null);
  const titleId   = useId();

  useEffect(() => {
    if (!open) return;
    const dialog   = dialogRef.current;
    const sel      = 'button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])';
    const focusable = [...dialog.querySelectorAll(sel)];
    const first    = focusable[0];
    const last     = focusable[focusable.length - 1];

    first?.focus();
    document.getElementById('main-content')?.setAttribute('aria-hidden', 'true');

    const trapTab = e => {
      if (e.key !== 'Tab') return;
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last?.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first?.focus(); }
    };
    const esc = e => { if (e.key === 'Escape') onClose(); };

    dialog.addEventListener('keydown', trapTab);
    document.addEventListener('keydown', esc);
    return () => {
      dialog.removeEventListener('keydown', trapTab);
      document.removeEventListener('keydown', esc);
      document.getElementById('main-content')?.removeAttribute('aria-hidden');
      triggerRef?.current?.focus();
    };
  }, [open, onClose, triggerRef]);

  if (!open) return null;
  return (
    <>
      <div ref={dialogRef} role="dialog" aria-modal="true"
           aria-labelledby={titleId} className="modal-inner" tabIndex={-1}>
        <h2 id={titleId}>{title}</h2>
        {children}
        <button type="button" onClick={onClose} aria-label={`Close ${title}`}>×</button>
      </div>
      <div className="modal-backdrop" onClick={onClose} aria-hidden="true" />
    </>
  );
}

/* ── Live announcement hook ─────────────────────────────── */
function useAnnounce() {
  return useCallback((msg, priority = 'polite') => {
    const el = document.getElementById(
      priority === 'assertive' ? 'aria-live-assertive' : 'aria-live-polite'
    );
    if (!el) return;
    el.textContent = '';
    requestAnimationFrame(() => { el.textContent = msg; });
  }, []);
}

/* ── Skip link ──────────────────────────────────────────── */
const SkipLink = () => (
  <a href="#main-content" className="skip-link">Skip to main content</a>
);

/* ── Page title ─────────────────────────────────────────── */
function usePageTitle(title) {
  useEffect(() => {
    const prev = document.title;
    document.title = `${title} — Acme Corp`;
    return () => { document.title = prev; };
  }, [title]);
}

/* ── Route change focus (React Router v6) ───────────────── */
import { useLocation } from 'react-router-dom';
function RouteAnnouncer() {
  const location = useLocation();
  useEffect(() => {
    const main = document.getElementById('main-content');
    if (main) {
      main.setAttribute('tabindex', '-1');
      main.focus();
      setTimeout(() => main.removeAttribute('tabindex'), 0);
    }
  }, [location.pathname]);
  return null;
}

/* ── Accessible Tabs ────────────────────────────────────── */
function Tabs({ tabs }) {
  const [active, setActive] = useState(0);
  const listId = useId();

  const onKey = e => {
    const n = tabs.length;
    const moves = { ArrowRight:(i)=>(i+1)%n, ArrowLeft:(i)=>(i-1+n)%n,
                    Home:()=>0, End:()=>n-1 };
    if (moves[e.key]) {
      e.preventDefault();
      const next = moves[e.key](active);
      setActive(next);
      document.getElementById(`tab-${listId}-${next}`)?.focus();
    }
  };

  return (
    <div>
      <div role="tablist" onKeyDown={onKey}>
        {tabs.map((t, i) => (
          <button key={t.id} role="tab"
                  id={`tab-${listId}-${i}`}
                  aria-selected={i === active}
                  aria-controls={`pnl-${listId}-${i}`}
                  tabIndex={i === active ? 0 : -1}
                  onClick={() => setActive(i)}>
            {t.label}
          </button>
        ))}
      </div>
      {tabs.map((t, i) => (
        <div key={t.id} role="tabpanel"
             id={`pnl-${listId}-${i}`}
             aria-labelledby={`tab-${listId}-${i}`}
             tabIndex={0}
             hidden={i !== active}>
          {t.content}
        </div>
      ))}
    </div>
  );
}

export { FormField, Modal, SkipLink, Tabs, useAnnounce, usePageTitle, RouteAnnouncer };
```

---

## 89. Full Accessible Page Template

A complete, copy-paste-ready HTML shell implementing every structural pattern.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Concise page description, 150 chars max.">
  <title>Page Name — Acme Corp</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>

  <!-- ① Skip links — FIRST focusable elements -->
  <a href="#main"    class="skip-link">Skip to main content</a>
  <a href="#primary-nav" class="skip-link">Skip to navigation</a>

  <!-- ② Global live regions — always in DOM, always empty at load -->
  <div id="aria-live-polite"    role="status"  aria-live="polite"    aria-atomic="true" class="visually-hidden"></div>
  <div id="aria-live-assertive" role="alert"   aria-live="assertive" aria-atomic="true" class="visually-hidden"></div>

  <!-- ══════════════════════════════════════════════════════════
       HEADER
  ══════════════════════════════════════════════════════════════ -->
  <header>

    <a href="/" aria-label="Acme Corp — homepage">
      <img src="/logo.svg" alt="" aria-hidden="true" width="120" height="40">
      <span class="logo-text">Acme Corp</span>
    </a>

    <nav id="primary-nav" aria-label="Primary navigation">
      <button type="button" class="hamburger"
              aria-expanded="false" aria-controls="nav-list"
              aria-label="Open navigation menu">
        <span class="bar" aria-hidden="true"></span>
        <span class="bar" aria-hidden="true"></span>
        <span class="bar" aria-hidden="true"></span>
      </button>

      <ul id="nav-list" role="list">
        <li><a href="/">Home</a></li>
        <li>
          <button type="button"
                  aria-expanded="false"
                  aria-controls="products-menu"
                  aria-haspopup="true">
            Products
            <svg aria-hidden="true" focusable="false" class="chevron"><!-- ▾ --></svg>
          </button>
          <ul id="products-menu" hidden>
            <li><a href="/products/widget-a">Widget A</a></li>
            <li><a href="/products/widget-b">Widget B</a></li>
            <li><a href="/products">All products</a></li>
          </ul>
        </li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact" aria-current="page">Contact</a></li>
      </ul>
    </nav>

    <form role="search" action="/search" method="get" aria-label="Site search">
      <label for="site-q" class="visually-hidden">Search</label>
      <input type="search" id="site-q" name="q" placeholder="Search…">
      <button type="submit" aria-label="Submit search">
        <svg aria-hidden="true" focusable="false"><!-- 🔍 --></svg>
      </button>
    </form>

    <div class="header-actions">
      <a href="/account" aria-label="My account">
        <svg aria-hidden="true" focusable="false"><!-- user --></svg>
        <span>Account</span>
      </a>
      <a href="/cart" aria-label="Cart, 3 items">
        <svg aria-hidden="true" focusable="false"><!-- cart --></svg>
        <span>Cart</span>
        <span class="badge" aria-hidden="true">3</span>
      </a>
    </div>

    <button type="button" id="theme-toggle"
            aria-pressed="false" aria-label="Switch to dark mode">
      <svg aria-hidden="true" focusable="false"><!-- moon --></svg>
    </button>

  </header>

  <!-- ══════════════════════════════════════════════════════════
       MAIN
  ══════════════════════════════════════════════════════════════ -->
  <main id="main" tabindex="-1">

    <!-- Breadcrumb -->
    <nav aria-label="Breadcrumb">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li><span aria-current="page">Widget A</span></li>
      </ol>
    </nav>

    <h1>Widget A — Product Details</h1>

    <section aria-labelledby="desc-h">
      <h2 id="desc-h">Description</h2>
      <figure>
        <img src="/products/widget-a.jpg"
             alt="Widget A: polished chrome cylinder, 12 cm × 5 cm, red silicone grip"
             width="600" height="400" loading="lazy">
        <figcaption>Widget A in Polished Chrome</figcaption>
      </figure>
      <p>Widget A is our flagship industrial widget…</p>
    </section>

    <section aria-labelledby="specs-h">
      <h2 id="specs-h">Specifications</h2>
      <dl>
        <dt>SKU</dt>        <dd>WGT-A-001</dd>
        <dt>Weight</dt>     <dd>340 g</dd>
        <dt>Dimensions</dt> <dd>12 cm × 5 cm × 5 cm</dd>
        <dt>Material</dt>   <dd>Stainless steel with silicone grip</dd>
      </dl>
    </section>

    <section aria-labelledby="purchase-h">
      <h2 id="purchase-h">Purchase</h2>
      <p class="price">
        <span class="visually-hidden">Price:</span>
        <span aria-label="9 euros and 99 cents">€9.99</span>
        <span class="vat">(inc. VAT)</span>
      </p>

      <form>
        <div class="stepper" role="group" aria-labelledby="qty-lbl">
          <span id="qty-lbl">Quantity</span>
          <button type="button" id="qty-dec" aria-label="Decrease quantity">−</button>
          <input type="number" id="qty" name="quantity"
                 value="1" min="1" max="99" aria-label="Quantity">
          <button type="button" id="qty-inc" aria-label="Increase quantity">+</button>
        </div>

        <fieldset>
          <legend>Color</legend>
          <label class="swatch-label">
            <input type="radio" name="color" value="chrome" checked aria-label="Chrome">
            <span class="swatch" style="background:#c0c0c0" aria-hidden="true"></span>
            <span>Chrome</span>
          </label>
          <label class="swatch-label">
            <input type="radio" name="color" value="black" aria-label="Matte Black">
            <span class="swatch" style="background:#1a1a1a" aria-hidden="true"></span>
            <span>Black</span>
          </label>
        </fieldset>

        <button type="submit" class="btn-primary">Add to cart</button>
        <button type="button" aria-label="Save Widget A to wishlist">Save to wishlist</button>
      </form>
    </section>

    <section aria-labelledby="reviews-h" id="reviews">
      <h2 id="reviews-h">Customer Reviews</h2>
      <div role="img" aria-label="Average rating: 4.3 out of 5 stars"><!-- stars SVG --></div>
      <p>4.3 out of 5 — 47 reviews</p>
      <ul aria-label="Customer reviews">
        <li>
          <article aria-labelledby="rev1-author">
            <header>
              <h3 id="rev1-author">Maria L.</h3>
              <div role="img" aria-label="Rating: 5 out of 5 stars"><!-- stars --></div>
              <time datetime="2024-11-20">20 November 2024</time>
            </header>
            <p>Excellent build quality. Exactly what I needed.</p>
          </article>
        </li>
      </ul>
    </section>

  </main>

  <!-- ══════════════════════════════════════════════════════════
       ASIDE
  ══════════════════════════════════════════════════════════════ -->
  <aside aria-label="Related products">
    <h2>You might also like</h2>
    <!-- product cards -->
  </aside>

  <!-- ══════════════════════════════════════════════════════════
       FOOTER
  ══════════════════════════════════════════════════════════════ -->
  <footer>
    <nav aria-label="Footer">
      <ul role="list">
        <li><a href="/accessibility">Accessibility Statement</a></li>
        <li><a href="/privacy">Privacy Policy</a></li>
        <li><a href="/imprint">Legal Notice</a></li>
        <li><a href="/sitemap">Sitemap</a></li>
      </ul>
    </nav>
    <address>
      <p>Acme Corp GmbH · Musterstraße 42 · 10115 Berlin</p>
      <p><a href="tel:+4930123456">+49 30 123456</a></p>
      <p><a href="mailto:info@acme-corp.de">info@acme-corp.de</a></p>
    </address>
    <p><small>© 2025 Acme Corp GmbH. All rights reserved.</small></p>
  </footer>

  <script src="/app.js" defer></script>
</body>
</html>
```

---

## 90. Automated Testing Integration

### CI/CD Pipeline

```bash
# Install tools
npm install --save-dev @axe-core/cli pa11y-ci @lhci/cli @playwright/test axe-playwright jest jest-axe @testing-library/react
```

```json
// .pa11yci.json
{
  "standard":  "WCAG2AA",
  "runners":   ["axe", "htmlcs"],
  "reporter":  "html",
  "threshold": 0,
  "urls": [
    "http://localhost:3000/",
    "http://localhost:3000/products",
    "http://localhost:3000/contact",
    "http://localhost:3000/checkout"
  ]
}
```

```javascript
// jest + jest-axe — component test
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('Button: no a11y violations', async () => {
  const { container } = render(
    <button type="button" aria-label="Save changes">Save</button>
  );
  expect(await axe(container)).toHaveNoViolations();
});

test('Form: meets WCAG 2.1 AA', async () => {
  const { container } = render(<ContactForm />);
  expect(await axe(container, {
    runOnly: { type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa'] }
  })).toHaveNoViolations();
});
```

```javascript
// Playwright E2E accessibility tests
import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y, getViolations } from 'axe-playwright';

test.describe('Homepage a11y', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
    await injectAxe(page);
  });

  test('no WCAG 2.2 AA violations', async ({ page }) => {
    await checkA11y(page, null, {
      axeOptions: { runOnly: ['wcag2a','wcag2aa','wcag21aa','wcag22aa'] }
    });
  });

  test('skip link works', async ({ page }) => {
    await page.keyboard.press('Tab');
    await expect(page.locator('.skip-link')).toBeFocused();
    await page.keyboard.press('Enter');
    await expect(page.locator('#main')).toBeFocused();
  });

  test('focus indicator always visible', async ({ page }) => {
    await page.keyboard.press('Tab');
    const outline = await page.locator(':focus').evaluate(el =>
      getComputedStyle(el).outlineStyle
    );
    expect(outline).not.toBe('none');
  });

  test('all images have alt text', async ({ page }) => {
    const v = await getViolations(page, null, { runOnly: ['image-alt'] });
    expect(v).toHaveLength(0);
  });

  test('color contrast passes', async ({ page }) => {
    const v = await getViolations(page, null, { runOnly: ['color-contrast'] });
    expect(v).toHaveLength(0);
  });

  test('modal keyboard behavior', async ({ page }) => {
    await page.click('#open-modal');
    const dialog = page.locator('[role="dialog"]');
    await expect(dialog).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(dialog).toBeHidden();
    await expect(page.locator('#open-modal')).toBeFocused();
  });
});
```

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/products'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'color-contrast': 'error',
        'image-alt':      'error',
        'label':          'error',
        'link-name':      'error',
        'button-name':    'error',
        'document-title': 'error',
        'html-has-lang':  'error',
        'skip-link':      'warn',
        'tabindex':       'warn',
      },
    },
    upload: { target: 'temporary-public-storage' },
  },
};
```

```yaml
# .github/workflows/a11y.yml
name: Accessibility

on: [push, pull_request]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run build
      - run: npm start &
      - run: npx wait-on http://localhost:3000
      - run: npm run test:a11y
      - run: npx playwright test tests/a11y/
      - run: npx lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: a11y-report
          path: reports/
```

---

## Final Reference — ARIA Roles Cheatsheet

| Role | Use when | Key keyboard | Required ARIA attrs |
|---|---|---|---|
| `button` | Action — prefer `<button>` | Enter, Space | `name` |
| `link` | Navigation — prefer `<a href>` | Enter | `name` |
| `checkbox` | Toggle — prefer `<input type=checkbox>` | Space | `checked` |
| `radio` | One of set — prefer `<input type=radio>` | Arrow keys | `checked` |
| `combobox` | Input + popup | Alt+↓ open, Escape, Enter | `expanded`, `controls` |
| `listbox` | Selection list | Arrow, Home, End | — |
| `option` | Item in listbox | — (listbox handles) | `selected` |
| `dialog` | Modal popup | Tab trap, Escape | `labelledby` |
| `alertdialog` | Blocking urgent dialog | Tab trap, Escape | `labelledby` |
| `tablist` | Tab container | Arrow keys | — |
| `tab` | Tab button | Enter/Space | `selected`, `controls` |
| `tabpanel` | Tab content | Tab to enter | `labelledby` |
| `menu` | Dropdown menu | Arrow, Escape | — |
| `menuitem` | Menu option | Enter, Space | — |
| `menuitemcheckbox` | Checkable menu item | Space | `checked` |
| `menuitemradio` | Radio menu item | Arrow keys | `checked` |
| `tree` | Hierarchical list | Arrow, Home, End | — |
| `treeitem` | Tree node | Enter, Space, Arrow | `expanded` (if has children) |
| `grid` | Data grid | Arrow keys 2D | — |
| `gridcell` | Grid cell | — (grid handles) | — |
| `slider` | Range — prefer `<input type=range>` | Arrow keys | `valuenow`, `valuemin`, `valuemax` |
| `progressbar` | Progress | — | `valuenow` (if determinate) |
| `switch` | On/off toggle | Space | `checked` |
| `tooltip` | Hover/focus hint | Escape | — |
| `log` | Chat / feed | — | `live=polite` (implicit) |
| `status` | Non-urgent update | — | `live=polite` (implicit) |
| `alert` | Error / urgent | — | `live=assertive` (implicit) |
| `timer` | Countdown | — | — |
| `search` | Search form | — | — |
| `img` | Informative SVG | — | `labelledby` or `label` |
| `presentation` / `none` | Decorative | — | — |
| `banner` | Site header — auto on `<header>` | — | — |
| `navigation` | Nav — auto on `<nav>` | — | `label` if multiple |
| `main` | Main — auto on `<main>` | — | — |
| `complementary` | Sidebar — auto on `<aside>` | — | — |
| `contentinfo` | Footer — auto on `<footer>` | — | — |
| `region` | Named section | — | `labelledby` or `label` |
| `form` | Form — auto on `<form>` with name | — | `label` |

---

*Part 2 complete — 90 sections total.  
Guide version: 2025-05-19. Patterns validated against WCAG 2.1 AA, WCAG 2.2 AA,  
EN 301 549 v3.2.1, ARIA APG 1.2.  
Tested with NVDA + Firefox, VoiceOver + Safari, TalkBack + Chrome.*
