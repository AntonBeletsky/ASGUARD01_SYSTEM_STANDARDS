# The Complete AI Guide to Semantic HTML5 Markup
## W3C-Compliant Standards Reference · A Monumental, Self-Contained Reference

> **Purpose**: This document is a definitive, exhaustive reference for producing correct, accessible, and semantically meaningful HTML5 markup in full conformance with W3C specifications. Every pattern, rule, and anti-pattern documented here is derived from the HTML Living Standard (WHATWG/W3C), WCAG 2.2, and WAI-ARIA 1.2.

---

## Table of Contents

1. [Foundational Principles](#1-foundational-principles)
2. [Document Skeleton](#2-document-skeleton)
3. [The `<head>` Element — Metadata](#3-the-head-element--metadata)
4. [Sectioning Elements](#4-sectioning-elements)
5. [Heading Hierarchy](#5-heading-hierarchy)
6. [Text-Level Semantics](#6-text-level-semantics)
7. [Grouping Content](#7-grouping-content)
8. [Lists](#8-lists)
9. [Links and Navigation](#9-links-and-navigation)
10. [Images and Figures](#10-images-and-figures)
11. [Tables](#11-tables)
12. [Forms](#12-forms)
13. [Interactive Elements](#13-interactive-elements)
14. [Embedded Content and Media](#14-embedded-content-and-media)
15. [Scripting Elements](#15-scripting-elements)
16. [Metadata and Microdata](#16-metadata-and-microdata)
17. [Accessibility — WAI-ARIA Integration](#17-accessibility--wai-aria-integration)
18. [Global Attributes](#18-global-attributes)
19. [Complete Page Patterns](#19-complete-page-patterns)
20. [Anti-Patterns and Common Mistakes](#20-anti-patterns-and-common-mistakes)
21. [Validation and Tooling](#21-validation-and-tooling)
22. [Quick-Reference Checklists](#22-quick-reference-checklists)

---

## 1. Foundational Principles

### 1.1 What Is Semantic HTML?

Semantic HTML means using elements that convey **meaning** — not just visual appearance. Every element chosen should answer the question: *What is this content, not how should it look?*

```
Presentational thinking: "I need bold text here."
Semantic thinking:        "Is this text important (strong), a keyword (b),
                           a title (h2), or a label (label)?"
```

### 1.2 The Four Pillars of W3C-Compliant HTML5

| Pillar | Description |
|--------|-------------|
| **Validity** | Document passes W3C Nu HTML Checker with zero errors |
| **Semantics** | Elements used match their defined purpose |
| **Accessibility** | Content is perceivable and operable by all users |
| **Interoperability** | Works correctly across all conforming user agents |

### 1.3 Content Model Categories

Every HTML5 element belongs to one or more content categories. Understanding these prevents nesting errors.

| Category | Description | Examples |
|----------|-------------|---------|
| **Metadata** | Affects document setup, not rendered | `<link>`, `<meta>`, `<title>`, `<style>` |
| **Flow** | Most body content | Nearly all body elements |
| **Sectioning** | Defines document outline sections | `<article>`, `<aside>`, `<nav>`, `<section>` |
| **Heading** | Section headings | `<h1>`–`<h6>`, `<hgroup>` |
| **Phrasing** | Inline content (text-level) | `<a>`, `<em>`, `<strong>`, `<span>`, `<time>` |
| **Embedded** | External resources embedded in document | `<img>`, `<video>`, `<iframe>`, `<canvas>` |
| **Interactive** | User-interaction content | `<a href>`, `<button>`, `<input>`, `<select>` |
| **Palpable** | Non-empty, visible content | Makes content non-empty |
| **Script-supporting** | Not rendered, supports scripts | `<script>`, `<template>` |

### 1.4 The Document Outline Algorithm

HTML5 uses a heading-based outline. Section elements (`<article>`, `<section>`, `<aside>`, `<nav>`) create new outline scopes. A **correct outline** is logical, hierarchical, and reflects the information architecture.

```
Document
├── header (site header)
├── main
│   ├── h1  "Page Title"
│   ├── section
│   │   ├── h2  "Section A"
│   │   └── section
│   │       └── h3  "Subsection A.1"
│   └── article
│       ├── h2  "Article Title"
│       └── section
│           └── h3  "Article Section"
├── aside
│   └── h2  "Related Content"
└── footer
```

---

## 2. Document Skeleton

### 2.1 Minimum Valid HTML5 Document

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
</head>
<body>
  <!-- Content -->
</body>
</html>
```

### 2.2 Rules for the DOCTYPE

```html
<!DOCTYPE html>
```

- Must be the **very first line** — no whitespace, no BOM before it (except UTF-8 BOM which browsers handle)
- Case-insensitive but lowercase is conventional
- Not an HTML tag — it is a "document type declaration"
- No legacy XHTML doctype should ever be used in new HTML5 documents

### 2.3 The `<html>` Element

```html
<html lang="en">
```

**Required attributes:**

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `lang` | Primary language of document content | `lang="en"`, `lang="uk"`, `lang="fr"` |

**Language subtags (BCP 47):**

```html
<html lang="en">          <!-- English -->
<html lang="en-US">       <!-- American English -->
<html lang="en-GB">       <!-- British English -->
<html lang="de">          <!-- German -->
<html lang="zh-Hans">     <!-- Chinese Simplified -->
<html lang="ar" dir="rtl"><!-- Arabic, right-to-left -->
```

**Rules:**
- Always specify `lang` — required for screen readers and search engines
- Use BCP 47 language tags (IANA Language Subtag Registry)
- Add `dir="rtl"` for right-to-left languages
- Do NOT use `xmlns` attribute (that is XHTML, not HTML5)

### 2.4 The `<body>` Element

The `<body>` element represents all rendered content. It takes no required attributes.

**Permitted content:** Flow content.

**Do NOT use deprecated body attributes:**

```html
<!-- WRONG — deprecated presentational attributes -->
<body bgcolor="#fff" text="#000" link="#00f" vlink="#800080">

<!-- CORRECT — use CSS -->
<body>
```

---

## 3. The `<head>` Element — Metadata

### 3.1 Required Head Elements

```html
<head>
  <!-- 1. Character encoding — MUST be within first 1024 bytes -->
  <meta charset="UTF-8">

  <!-- 2. Viewport for responsive design -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- 3. Document title — required by spec, critical for SEO and a11y -->
  <title>Descriptive Page Title — Site Name</title>
</head>
```

### 3.2 The `<meta charset>` Element

```html
<meta charset="UTF-8">
```

- Must appear **before** `<title>` and any element with text content
- Must appear within the first 1024 bytes of the file
- `UTF-8` is the only acceptable value for new documents
- No closing tag — it is a void element

### 3.3 The `<title>` Element

```html
<title>Article Title — Category — Site Name</title>
```

**Rules:**
- Exactly **one** `<title>` per document
- Must be non-empty
- Should uniquely describe the page (for tabs, bookmarks, search results)
- Recommended format: `[Page Topic] — [Site Name]`
- Maximum ~55–70 characters for full SEO display
- No HTML markup allowed inside `<title>` — text only

### 3.4 The `<meta name="viewport">` Element

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**Viewport directive reference:**

| Directive | Recommended Value | Notes |
|-----------|-------------------|-------|
| `width` | `device-width` | Never use a fixed pixel value |
| `initial-scale` | `1.0` | Ensures 1:1 mapping on load |
| `minimum-scale` | Omit or `1.0` | Never restrict below 1.0 — violates WCAG 1.4.4 |
| `maximum-scale` | Omit | Never set — prevents user zoom (WCAG violation) |
| `user-scalable` | Omit | `no` is a WCAG 1.4.4 violation |

### 3.5 SEO and Social Meta Tags

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Complete HTML5 Guide — DevDocs</title>

  <!-- SEO -->
  <meta name="description" content="A comprehensive guide to semantic HTML5 markup conforming to W3C standards.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://example.com/html5-guide">

  <!-- Open Graph (Facebook, LinkedIn, Discord) -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="Complete HTML5 Guide">
  <meta property="og:description" content="Comprehensive W3C-compliant semantic markup reference.">
  <meta property="og:image" content="https://example.com/images/og-html5.jpg">
  <meta property="og:url" content="https://example.com/html5-guide">
  <meta property="og:site_name" content="DevDocs">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@devdocs">
  <meta name="twitter:title" content="Complete HTML5 Guide">
  <meta name="twitter:description" content="Comprehensive W3C-compliant semantic markup reference.">
  <meta name="twitter:image" content="https://example.com/images/twitter-html5.jpg">
</head>
```

### 3.6 Link Relations (`<link>`)

```html
<!-- Favicon -->
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<!-- Stylesheets -->
<link rel="stylesheet" href="/css/main.css">

<!-- Preconnect to external origins (performance) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/images/hero.webp" as="image">

<!-- Alternate versions -->
<link rel="alternate" hreflang="fr" href="https://example.com/fr/html5-guide">
<link rel="alternate" hreflang="de" href="https://example.com/de/html5-guide">
<link rel="alternate" hreflang="x-default" href="https://example.com/html5-guide">

<!-- RSS / Atom feeds -->
<link rel="alternate" type="application/rss+xml" title="Blog RSS Feed" href="/feed.rss">

<!-- Web App Manifest -->
<link rel="manifest" href="/site.webmanifest">
```

**Common `rel` values:**

| Value | Purpose |
|-------|---------|
| `stylesheet` | CSS file |
| `icon` | Favicon |
| `canonical` | Preferred URL for this content |
| `alternate` | Alternative version (language, format) |
| `preload` | Preload critical resource |
| `preconnect` | Warm up connection to origin |
| `prefetch` | Prefetch likely-needed resource |
| `dns-prefetch` | Early DNS resolution |
| `manifest` | Web App Manifest |
| `author` | Page author |
| `license` | Content license |
| `next` / `prev` | Pagination |

### 3.7 Scripts in `<head>`

```html
<!-- Modern: defer keeps scripts non-blocking -->
<script src="/js/analytics.js" defer></script>

<!-- async for independent scripts (analytics, ads) -->
<script src="https://www.googletagmanager.com/gtm.js" async></script>

<!-- Critical inline scripts (rare — keep minimal) -->
<script>
  // Theme detection before first paint — acceptable inline use
  if (localStorage.getItem('theme') === 'dark') {
    document.documentElement.classList.add('dark');
  }
</script>

<!-- Module scripts -->
<script type="module" src="/js/app.js"></script>
```

**`defer` vs `async` vs neither:**

| Attribute | Parse block? | Execution order | Use case |
|-----------|-------------|-----------------|---------|
| Neither | Yes (blocks) | Sequential | Critical scripts that must run synchronously |
| `defer` | No | Sequential (DOM-ready) | Most scripts — maintains order |
| `async` | No | Unordered | Independent scripts (analytics, ads) |
| `type="module"` | No | Deferred by default | ES modules |

---

## 4. Sectioning Elements

Sectioning elements define the **document outline** and establish structural regions of the page. Each creates a new sectioning context.

### 4.1 Overview of Sectioning Elements

| Element | Purpose | Landmark Role |
|---------|---------|---------------|
| `<header>` | Introductory content for its parent or the page | `banner` (when top-level), `none` otherwise |
| `<footer>` | Closing content for its parent or the page | `contentinfo` (when top-level), `none` otherwise |
| `<main>` | Primary content of the document | `main` |
| `<nav>` | Navigation links | `navigation` |
| `<article>` | Independent, self-contained content | `article` |
| `<section>` | Thematic grouping with a heading | `region` (only if it has an accessible name) |
| `<aside>` | Tangentially related content | `complementary` |

### 4.2 `<header>`

Represents introductory content — typically a logo, site title, and primary navigation.

```html
<!-- Site-level header (landmark: banner) -->
<header>
  <a href="/" aria-label="Home">
    <img src="/logo.svg" alt="CompanyName" width="120" height="40">
  </a>
  <nav aria-label="Primary">
    <ul>
      <li><a href="/about">About</a></li>
      <li><a href="/services">Services</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
</header>

<!-- Article-level header (no landmark role) -->
<article>
  <header>
    <h2>Article Title</h2>
    <p>Published by <a href="/authors/jane">Jane Doe</a> on
      <time datetime="2025-06-01">June 1, 2025</time>
    </p>
  </header>
  <!-- article content -->
</article>
```

**Rules:**
- A `<header>` inside `<body>` (not nested in another sectioning element) becomes the `banner` landmark
- A `<header>` inside `<article>` or `<section>` is just a header for that section — no landmark role
- Must not contain another `<header>` or `<footer>`
- Does NOT require a heading, but often contains one

### 4.3 `<footer>`

Represents closing content — typically copyright, links, contact info.

```html
<!-- Site-level footer (landmark: contentinfo) -->
<footer>
  <nav aria-label="Footer">
    <ul>
      <li><a href="/privacy">Privacy Policy</a></li>
      <li><a href="/terms">Terms of Service</a></li>
    </ul>
  </nav>
  <p><small>&copy; 2025 Company Name. All rights reserved.</small></p>
</footer>

<!-- Article-level footer -->
<article>
  <!-- content -->
  <footer>
    <p>Tags: <a href="/tags/html">HTML</a>, <a href="/tags/css">CSS</a></p>
    <p>Last updated: <time datetime="2025-06-01">June 1, 2025</time></p>
  </footer>
</article>
```

**Rules:**
- Must not contain another `<header>` or `<footer>`
- Can appear multiple times on a page (one top-level, others inside sectioning elements)

### 4.4 `<main>`

Represents the **dominant content** of the document. Excludes repeated site-wide content (header, nav, footer, sidebars).

```html
<body>
  <header><!-- site header --></header>
  <nav aria-label="Primary"><!-- primary nav --></nav>

  <main>
    <h1>Welcome to Our Site</h1>
    <p>This is the main content area.</p>
    <!-- All primary content here -->
  </main>

  <aside><!-- sidebar --></aside>
  <footer><!-- site footer --></footer>
</body>
```

**Rules:**
- There must be **at most one visible `<main>`** per page
- Must not be a descendant of `<article>`, `<aside>`, `<footer>`, `<header>`, or `<nav>`
- Should contain the primary `<h1>` of the page
- Hidden `<main>` elements (via `hidden` attribute) may coexist for SPA use cases

### 4.5 `<nav>`

Represents a block of **navigation links** — major blocks of links intended for navigating the site or page.

```html
<!-- Primary site navigation -->
<nav aria-label="Primary">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
    <li><a href="/services">Services</a></li>
    <li><a href="/blog">Blog</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>

<!-- Breadcrumb navigation -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/blog">Blog</a></li>
    <li><span aria-current="page">HTML5 Guide</span></li>
  </ol>
</nav>

<!-- Table of contents -->
<nav aria-label="Table of contents">
  <ol>
    <li><a href="#intro">Introduction</a></li>
    <li><a href="#structure">Document Structure</a></li>
    <li><a href="#semantics">Semantic Elements</a></li>
  </ol>
</nav>

<!-- Pagination -->
<nav aria-label="Pagination">
  <a href="/page/1" aria-label="Previous page">←</a>
  <a href="/page/1">1</a>
  <span aria-current="page">2</span>
  <a href="/page/3">3</a>
  <a href="/page/3" aria-label="Next page">→</a>
</nav>
```

**Rules:**
- Label each `<nav>` with `aria-label` or `aria-labelledby` when multiple `<nav>` elements exist on a page
- Only wrap **major** navigation blocks — do not wrap every group of links
- Not all links need to be inside `<nav>` — footer links often do not warrant `<nav>`
- Use `<ol>` for ordered navigation (breadcrumbs, steps), `<ul>` for unordered

### 4.6 `<article>`

Represents **independently distributable or reusable** content. Should make sense if syndicated on its own.

```html
<!-- Blog post -->
<article>
  <header>
    <h2><a href="/posts/html5-guide">Complete HTML5 Guide</a></h2>
    <p>By <a href="/authors/jane" rel="author">Jane Doe</a> ·
       <time datetime="2025-06-01T09:00:00Z">June 1, 2025</time></p>
  </header>
  <p>This guide covers all aspects of semantic HTML5...</p>
  <footer>
    <ul aria-label="Article tags">
      <li><a href="/tags/html">HTML</a></li>
      <li><a href="/tags/semantics">Semantics</a></li>
    </ul>
  </footer>
</article>

<!-- Comment (nested article inside article) -->
<article>
  <h2>User Comments</h2>
  <article>
    <header>
      <h3>Comment by Alice</h3>
      <time datetime="2025-06-02T14:30:00Z">June 2, 2025 at 2:30 PM</time>
    </header>
    <p>Great article! Very comprehensive.</p>
  </article>
  <article>
    <header>
      <h3>Comment by Bob</h3>
      <time datetime="2025-06-02T16:00:00Z">June 2, 2025 at 4:00 PM</time>
    </header>
    <p>Bookmarked for future reference.</p>
  </article>
</article>

<!-- Product card -->
<article>
  <img src="/products/widget.jpg" alt="Blue Widget — ergonomic design">
  <h3>Blue Widget</h3>
  <p>$29.99</p>
  <p>Ergonomically designed for comfort.</p>
  <a href="/products/blue-widget">View Product</a>
</article>
```

**Use `<article>` for:**
- Blog posts, news articles
- Forum posts, comments
- Product cards
- User-generated content items
- Social media posts

**Do NOT use `<article>` for:**
- Generic content sections
- Page layout regions
- Repeated UI components without semantic independence

### 4.7 `<section>`

Represents a **thematic grouping** of content, typically with a heading. Think of it as a chapter or a named division.

```html
<!-- Correct: section with heading -->
<section>
  <h2>Our Services</h2>
  <p>We offer a wide range of services...</p>
  <ul>
    <li>Web Design</li>
    <li>Development</li>
    <li>SEO</li>
  </ul>
</section>

<!-- Page with multiple named sections -->
<main>
  <h1>About Our Company</h1>

  <section>
    <h2>Our History</h2>
    <p>Founded in 2010...</p>
  </section>

  <section>
    <h2>Our Mission</h2>
    <p>We believe in the open web...</p>
  </section>

  <section>
    <h2>Meet the Team</h2>
    <!-- team members -->
  </section>
</main>
```

**`<section>` vs `<div>` — the key distinction:**

| Use `<section>` | Use `<div>` |
|-----------------|-------------|
| Content has a heading and thematic identity | Content is grouped for layout/styling only |
| Content would appear in a document outline | No outline contribution needed |
| Can be given a label (via heading) | Generic container |

**Rules:**
- Almost always has a heading (`<h2>`–`<h6>`)
- If you can't give it a heading, it probably should be a `<div>`
- Gets `region` landmark role only when it has an accessible name (`aria-labelledby` or `aria-label`)

### 4.8 `<aside>`

Represents content **tangentially related** to the main content — could be removed without breaking the main content flow.

```html
<!-- Sidebar aside -->
<aside aria-label="Related articles">
  <h2>Related Articles</h2>
  <ul>
    <li><a href="/css-guide">CSS Flexbox Guide</a></li>
    <li><a href="/js-guide">JavaScript Guide</a></li>
  </ul>
</aside>

<!-- Pull quote inside article -->
<article>
  <h2>The Importance of Semantic HTML</h2>
  <p>Semantic HTML is the foundation of accessible web development...</p>

  <aside>
    <blockquote>
      <p>The web is for everyone. Semantic markup ensures that everyone
         can access and understand your content.</p>
    </blockquote>
  </aside>

  <p>When we use elements correctly, assistive technologies can...</p>
</article>

<!-- Advertising sidebar -->
<aside aria-label="Advertisement">
  <!-- ad content -->
</aside>
```

**Use `<aside>` for:**
- Sidebars with related links
- Pull quotes
- Advertising
- Author biographical note
- Glossary definitions

---

## 5. Heading Hierarchy

### 5.1 The Heading Elements

```html
<h1>Page Title — Primary Heading</h1>
<h2>Major Section</h2>
<h3>Subsection</h3>
<h4>Sub-subsection</h4>
<h5>Minor heading</h5>
<h6>Smallest heading</h6>
```

### 5.2 Rules for Headings

**Rule 1: One `<h1>` per page**
```html
<!-- CORRECT -->
<h1>Main Page Title</h1>

<!-- WRONG — multiple h1 on one page -->
<h1>Title One</h1>
<h1>Title Two</h1>
```

**Rule 2: Never skip heading levels downward**
```html
<!-- WRONG — skips from h2 to h4 -->
<h2>Section</h2>
<h4>Subsection</h4>

<!-- CORRECT — sequential levels -->
<h2>Section</h2>
<h3>Subsection</h3>
```

**Rule 3: You MAY skip upward**
```html
<!-- CORRECT — going back up is fine -->
<h2>Section A</h2>
<h3>Subsection A.1</h3>
<h2>Section B</h2>   <!-- jumping from h3 back to h2 is valid -->
```

**Rule 4: Headings are for structure, not styling**
```html
<!-- WRONG — using h3 for visual size, not structure -->
<h3>I just wanted smaller text</h3>

<!-- CORRECT — use CSS for visual size; heading for meaning -->
<p class="lead">I just wanted styled text</p>
```

### 5.3 `<hgroup>` Element

Groups a heading with related secondary content (tagline, subheading).

```html
<hgroup>
  <h1>Developer Blog</h1>
  <p>Thoughts on web development, accessibility, and open standards</p>
</hgroup>

<hgroup>
  <h2>The CSS Box Model</h2>
  <p>Understanding margin, border, padding, and content areas</p>
</hgroup>
```

**Rules:**
- Content must be `<h1>`–`<h6>` plus zero or more `<p>` elements
- Only the heading contributes to the document outline
- The `<p>` elements are the subtitle/tagline
- Previously deprecated, reinstated in HTML living standard

---

## 6. Text-Level Semantics

### 6.1 Emphasis and Importance

```html
<!-- <em> — Stress emphasis (changes meaning when spoken aloud) -->
<p>I <em>never</em> said she stole the money.</p>
<p>I never said <em>she</em> stole the money.</p>

<!-- <strong> — Strong importance, seriousness, urgency -->
<p><strong>Warning:</strong> This action cannot be undone.</p>
<p>Read the <strong>safety instructions</strong> before proceeding.</p>
```

**`<em>` vs `<strong>` vs `<b>` vs `<i>`:**

| Element | Semantic meaning | Screen reader behavior |
|---------|-----------------|----------------------|
| `<em>` | Stress emphasis | Changes inflection |
| `<strong>` | Strong importance / seriousness | May announce "important" |
| `<b>` | Stylistically bold without importance | No change (presentational) |
| `<i>` | Alternate voice/mood, technical term, idiomatic text | No change (presentational) |

### 6.2 Typographic Semantics

```html
<!-- <b> — Bring attention without importance (keywords, product names) -->
<p>The <b>submit</b> button sends the form data.</p>

<!-- <i> — Idiomatic, technical, foreign terms, internal monologue -->
<p>The Latin phrase <i lang="la">carpe diem</i> means "seize the day."</p>
<p>She thought: <i>What if this all goes wrong?</i></p>
<p>The <i class="taxonomy">Homo sapiens</i> is the only living member...</p>

<!-- <u> — Unarticulated annotation (spelling error, Chinese proper names) -->
<p>The word <u class="spelling-error">recieve</u> is misspelled.</p>

<!-- <s> — Strikethrough — content no longer accurate or relevant -->
<p>Price: <s>$99.99</s> $79.99</p>

<!-- <mark> — Highlighted / marked for reference in current context -->
<p>Search results for <mark>semantic HTML</mark>: 1,234 results found.</p>
<p>Remember to submit your report by <mark>Friday, June 6</mark>.</p>

<!-- <small> — Side comments, fine print, legal disclaimers -->
<p>Our service is free to start.</p>
<small>Terms and conditions apply. Subject to fair use policy.</small>
```

### 6.3 Code and Technical Text

```html
<!-- <code> — Inline code fragment -->
<p>Use the <code>Array.prototype.map()</code> method to transform arrays.</p>

<!-- <kbd> — Keyboard input -->
<p>Press <kbd>Ctrl</kbd>+<kbd>S</kbd> to save the document.</p>

<!-- <samp> — Sample output from a program -->
<p>The terminal displayed: <samp>Error: Connection refused (ECONNREFUSED)</samp></p>

<!-- <var> — Mathematical or programming variable -->
<p>The formula is <var>E</var> = <var>m</var><var>c</var><sup>2</sup>.</p>

<!-- <pre><code> — Block of code -->
<pre><code class="language-javascript">
function greet(name) {
  return `Hello, ${name}!`;
}
console.log(greet('World'));
</code></pre>
```

### 6.4 Quotations

```html
<!-- <blockquote> — Extended quotation from another source -->
<blockquote cite="https://www.w3.org/TR/html52/introduction.html">
  <p>The Web was invented as a communications tool intended to allow
     anyone, anywhere to share information.</p>
</blockquote>

<!-- With attribution using <figure> and <figcaption> -->
<figure>
  <blockquote>
    <p>The best way to predict the future is to invent it.</p>
  </blockquote>
  <figcaption>
    — <cite>Alan Kay</cite>, 1971 PARC meeting
  </figcaption>
</figure>

<!-- <q> — Inline quotation -->
<p>As Tim Berners-Lee said, <q cite="https://example.com">This is for everyone.</q></p>

<!-- <cite> — Reference to a creative work title -->
<p>I was reading <cite>The Pragmatic Programmer</cite> last night.</p>
<p>The concept was introduced in <cite>RFC 2616</cite>.</p>
```

**Rules for quotations:**
- `<blockquote>` is for block-level quotes; `<q>` for inline quotes
- `cite` attribute takes a **URL**, not a person's name
- `<cite>` element is for **work titles**, not people's names
- Attribution (person's name, date) goes in `<figcaption>`, not inside `<blockquote>`

### 6.5 Date and Time

```html
<!-- <time> — Machine-readable date/time -->

<!-- Date -->
<time datetime="2025-06-01">June 1, 2025</time>

<!-- Time -->
<time datetime="14:30">2:30 PM</time>

<!-- Date and time (UTC) -->
<time datetime="2025-06-01T14:30:00Z">June 1, 2025 at 2:30 PM UTC</time>

<!-- Date and time (with timezone offset) -->
<time datetime="2025-06-01T14:30:00+03:00">June 1, 2025 at 2:30 PM (Kyiv)</time>

<!-- Year and month -->
<time datetime="2025-06">June 2025</time>

<!-- Year only -->
<time datetime="2025">2025</time>

<!-- Duration (ISO 8601) -->
<time datetime="PT2H30M">2 hours 30 minutes</time>
<time datetime="P1DT6H">1 day 6 hours</time>

<!-- Week -->
<time datetime="2025-W23">Week 23, 2025</time>
```

**`datetime` format reference (ISO 8601):**

| Format | Example | Meaning |
|--------|---------|---------|
| `YYYY-MM-DD` | `2025-06-01` | Date |
| `HH:MM` | `14:30` | Time (local) |
| `HH:MM:SS` | `14:30:00` | Time with seconds |
| `YYYY-MM-DDTHH:MM:SSZ` | `2025-06-01T14:30:00Z` | UTC datetime |
| `YYYY-MM-DDTHH:MM:SS±HH:MM` | `2025-06-01T14:30:00+03:00` | With offset |
| `YYYY-MM` | `2025-06` | Year-month |
| `YYYY` | `2025` | Year only |
| `YYYY-Www` | `2025-W23` | Year-week |
| `PTnHnMnS` | `PT1H30M` | Duration |

### 6.6 Abbreviations and Definitions

```html
<!-- <abbr> — Abbreviation with expansion -->
<p><abbr title="HyperText Markup Language">HTML</abbr> is the language of the web.</p>
<p>The <abbr title="World Wide Web Consortium">W3C</abbr> publishes web standards.</p>

<!-- <dfn> — The defining instance of a term -->
<p>
  <dfn id="def-semantic">Semantic HTML</dfn> is the practice of using HTML elements
  according to their intended purpose, conveying meaning about the content they contain.
</p>
<!-- Later in the document, link back to the definition -->
<p>Using <a href="#def-semantic">semantic HTML</a> improves accessibility.</p>

<!-- Combined dfn + abbr -->
<p>
  <dfn><abbr title="Application Programming Interface">API</abbr></dfn>
  is a set of rules that allows programs to talk to each other.
</p>
```

### 6.7 Ruby Annotations (East Asian Typography)

```html
<!-- Ruby for Japanese kanji with furigana -->
<ruby>
  漢 <rt>かん</rt>
  字 <rt>じ</rt>
</ruby>

<!-- Ruby with fallback parentheses -->
<ruby>
  漢字
  <rp>(</rp>
  <rt>かんじ</rt>
  <rp>)</rp>
</ruby>
```

### 6.8 Other Inline Semantics

```html
<!-- <sup> and <sub> — Superscript and subscript -->
<p>Water is H<sub>2</sub>O.</p>
<p>Einstein's formula: E = mc<sup>2</sup></p>
<p>The 1<sup>st</sup> of June</p>

<!-- <br> — Line break (only for content where breaks are meaningful) -->
<address>
  Jane Doe<br>
  123 Main Street<br>
  Anytown, CA 90210
</address>

<p>Roses are red,<br>
Violets are blue,<br>
HTML is semantic,<br>
And so should you.</p>

<!-- <wbr> — Word break opportunity (suggest line break in long words/URLs) -->
<p>https://www.example.com/very<wbr>/long<wbr>/url<wbr>/path</p>

<!-- <bdi> — Bidirectional Isolation (for unknown text direction) -->
<p>Username: <bdi>مرحبا</bdi> has posted 42 comments.</p>

<!-- <bdo> — Bidirectional Override -->
<p><bdo dir="rtl">This text will appear reversed</bdo></p>

<!-- <span> — Generic inline container (no semantic meaning) -->
<p>The sky is <span class="color-sample" style="color: #87CEEB;">sky blue</span>.</p>

<!-- <data> — Machine-readable equivalent -->
<p>Product: <data value="978-0-553-21311-7">The Lord of the Rings</data></p>
```

---

## 7. Grouping Content

### 7.1 Paragraphs

```html
<!-- <p> — Paragraph (most common flow element) -->
<p>This is a paragraph. It represents a discrete block of text.</p>

<!-- WRONG — empty paragraph for spacing -->
<p></p>

<!-- CORRECT — use CSS margin/padding for spacing -->
<p>First paragraph.</p>
<!-- use CSS: p + p { margin-top: 1em; } -->
<p>Second paragraph.</p>
```

**Rules:**
- Never use `<p>` for layout spacing
- A `<p>` cannot contain block-level elements (`<div>`, `<ul>`, etc.)
- A `<p>` element is implicitly closed when a block element starts

### 7.2 `<div>` — Generic Block Container

```html
<!-- <div> has NO semantic meaning — use only when no semantic element fits -->

<!-- WRONG — using div when article is appropriate -->
<div class="blog-post">
  <div class="post-title">My Post</div>
  <div class="post-content">Content here.</div>
</div>

<!-- CORRECT -->
<article>
  <h2>My Post</h2>
  <p>Content here.</p>
</article>

<!-- CORRECT use of div — layout wrapper with no semantic meaning -->
<div class="container">
  <article>...</article>
  <aside>...</aside>
</div>
```

### 7.3 `<address>`

Represents **contact information** for the nearest `<article>` or the document's author/owner.

```html
<!-- Document author contact info (in <footer>) -->
<footer>
  <address>
    Written by <a href="/about/jane">Jane Doe</a>.<br>
    Contact: <a href="mailto:jane@example.com">jane@example.com</a><br>
    123 Web Street, Internet City
  </address>
</footer>

<!-- Article author -->
<article>
  <h2>Understanding Semantics</h2>
  <address>
    By <a href="/authors/jane" rel="author">Jane Doe</a>
  </address>
  <p>Content...</p>
</article>
```

**Rules:**
- `<address>` is for **contact information**, not any postal address
- For a generic postal address (shipping address, business location), use `<p>` or schema.org markup
- Must not contain headings, sectioning elements, or other `<address>` elements

### 7.4 `<hr>` — Thematic Break

```html
<!-- <hr> — Thematic break between paragraphs/content blocks -->

<section>
  <h2>Act I: The Beginning</h2>
  <p>The hero sets out on their journey...</p>
</section>

<hr>  <!-- Marks a thematic shift, scene change -->

<section>
  <h2>Act II: The Conflict</h2>
  <p>Obstacles arise...</p>
</section>
```

**Rules:**
- Use `<hr>` for **thematic breaks** in content, not for visual separators
- For visual separators, use CSS (borders, margins)
- `<hr>` is a void element — no closing tag, no content

### 7.5 `<figure>` and `<figcaption>`

```html
<!-- Image with caption -->
<figure>
  <img src="/images/semantic-diagram.png"
       alt="Diagram showing HTML5 semantic elements arranged by their position on a typical webpage">
  <figcaption>
    Fig. 1: Common arrangement of HTML5 semantic sectioning elements.
  </figcaption>
</figure>

<!-- Code block with caption -->
<figure>
  <pre><code class="language-html">
&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
  &lt;head&gt;...&lt;/head&gt;
  &lt;body&gt;...&lt;/body&gt;
&lt;/html&gt;
  </code></pre>
  <figcaption>Listing 1: Minimum valid HTML5 document</figcaption>
</figure>

<!-- Grouped images -->
<figure>
  <img src="/before.jpg" alt="Website before redesign — cluttered layout with poor contrast">
  <img src="/after.jpg" alt="Website after redesign — clean layout with clear hierarchy">
  <figcaption>Before and after the 2025 redesign.</figcaption>
</figure>

<!-- Blockquote with attribution in figcaption -->
<figure>
  <blockquote>
    <p>Programs must be written for people to read, and only incidentally
       for machines to execute.</p>
  </blockquote>
  <figcaption>
    — <cite>Harold Abelson</cite>,
    <cite>Structure and Interpretation of Computer Programs</cite>, 1996
  </figcaption>
</figure>
```

**Rules:**
- `<figure>` wraps self-contained content referenced from the main flow
- `<figcaption>` must be the **first or last** child of `<figure>`
- Only one `<figcaption>` per `<figure>`
- `<figcaption>` is optional — `<figure>` can exist without it
- Content inside `<figure>` should be referenceable (e.g., "See Figure 1")

### 7.6 `<details>` and `<summary>`

```html
<!-- Disclosure widget -->
<details>
  <summary>What is semantic HTML?</summary>
  <p>Semantic HTML means using elements that convey meaning about their content,
     not just visual appearance. It improves accessibility, SEO, and maintainability.</p>
</details>

<!-- Accordion-style FAQ -->
<details>
  <summary>How do I validate my HTML?</summary>
  <p>Use the <a href="https://validator.w3.org">W3C Nu HTML Checker</a>.</p>
</details>

<!-- Open by default -->
<details open>
  <summary>Browser support</summary>
  <p>All modern browsers support this element natively.</p>
</details>
```

**Rules:**
- `<summary>` must be the **first** child of `<details>`
- `<summary>` is the visible label/toggle
- Without `<summary>`, browsers supply a default label ("Details")
- `open` attribute makes it expanded by default

---

## 8. Lists

### 8.1 Unordered Lists

```html
<!-- <ul> — Unordered list: order does not matter -->
<ul>
  <li>Apples</li>
  <li>Oranges</li>
  <li>Bananas</li>
</ul>

<!-- Navigation using ul -->
<nav aria-label="Primary">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
    <li>
      <a href="/services">Services</a>
      <!-- Nested list for submenu -->
      <ul>
        <li><a href="/services/design">Design</a></li>
        <li><a href="/services/development">Development</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

### 8.2 Ordered Lists

```html
<!-- <ol> — Ordered list: sequence matters -->
<ol>
  <li>Preheat the oven to 180°C.</li>
  <li>Mix dry ingredients in a bowl.</li>
  <li>Combine wet and dry ingredients.</li>
  <li>Pour into baking tin and bake for 30 minutes.</li>
</ol>

<!-- Start attribute — begin at a specific number -->
<ol start="4">
  <li>Step four</li>
  <li>Step five</li>
</ol>

<!-- Reversed order -->
<ol reversed>
  <li>Third place: Team C</li>
  <li>Second place: Team B</li>
  <li>First place: Team A</li>
</ol>

<!-- Custom type attribute -->
<ol type="A">    <!-- A, B, C... -->
  <li>Section A</li>
  <li>Section B</li>
</ol>

<ol type="i">    <!-- i, ii, iii... (lowercase Roman) -->
  <li>Chapter one</li>
  <li>Chapter two</li>
</ol>
```

### 8.3 Description Lists

```html
<!-- <dl> — Description list: key-value pairs, glossaries, metadata -->
<dl>
  <dt>HTML</dt>
  <dd>HyperText Markup Language — the standard language for web pages.</dd>

  <dt>CSS</dt>
  <dd>Cascading Style Sheets — controls the visual presentation of HTML.</dd>

  <dt>JavaScript</dt>
  <dd>A programming language that enables interactive web pages.</dd>
</dl>

<!-- Multiple definitions for one term -->
<dl>
  <dt>Bass</dt>
  <dd>A type of fish found in fresh and salt water.</dd>
  <dd>A low-frequency range in music.</dd>
  <dd>A stringed musical instrument.</dd>
</dl>

<!-- Multiple terms for one definition -->
<dl>
  <dt>UK</dt>
  <dt>Great Britain</dt>
  <dd>A nation in northwestern Europe comprising England, Scotland, and Wales (and Northern Ireland for UK).</dd>
</dl>

<!-- Metadata pattern using dl -->
<article>
  <h2>Article Title</h2>
  <dl>
    <div>
      <dt>Author</dt>
      <dd><a href="/authors/jane">Jane Doe</a></dd>
    </div>
    <div>
      <dt>Published</dt>
      <dd><time datetime="2025-06-01">June 1, 2025</time></dd>
    </div>
    <div>
      <dt>Reading time</dt>
      <dd>8 minutes</dd>
    </div>
  </dl>
  <p>Article content...</p>
</article>
```

**Rules for lists:**
- `<li>` is only valid inside `<ul>` or `<ol>`
- `<dt>` and `<dd>` are only valid inside `<dl>`
- Only `<li>` and script/template elements allowed inside `<ul>`/`<ol>`
- Only `<dt>`, `<dd>`, `<div>`, and script/template elements allowed inside `<dl>`
- Do NOT use lists purely for visual indentation

---

## 9. Links and Navigation

### 9.1 The `<a>` Element

```html
<!-- Basic link -->
<a href="https://www.w3.org">Visit the W3C website</a>

<!-- Internal link -->
<a href="/about">About Us</a>

<!-- Anchor link (same page) -->
<a href="#section-2">Skip to Section 2</a>

<!-- Email link -->
<a href="mailto:contact@example.com">Email us</a>

<!-- Phone link -->
<a href="tel:+1-555-123-4567">+1 (555) 123-4567</a>

<!-- SMS link -->
<a href="sms:+1-555-123-4567">Send us a text</a>

<!-- Download link -->
<a href="/files/guide.pdf" download="html5-guide.pdf">Download PDF Guide</a>

<!-- New window/tab (use sparingly) -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  External Site (opens in new tab)
</a>
```

### 9.2 Link Attributes Reference

| Attribute | Value | Purpose |
|-----------|-------|---------|
| `href` | URL | Destination |
| `target` | `_blank`, `_self`, `_parent`, `_top` | Where to open |
| `rel` | See table below | Relationship to destination |
| `download` | Filename (optional) | Prompt download |
| `hreflang` | Language code | Language of destination |
| `type` | MIME type | Media type of destination |
| `referrerpolicy` | Policy string | Controls referrer header |

**`rel` values for `<a>`:**

| Value | Meaning |
|-------|---------|
| `noopener` | Prevent window.opener access (always use with `target="_blank"`) |
| `noreferrer` | Don't send referrer header (implies `noopener`) |
| `nofollow` | Signal to search engines not to follow |
| `external` | Document is not part of same site |
| `author` | Link to author info |
| `license` | Link to license |
| `next` / `prev` | Pagination relationship |
| `help` | Link to help document |
| `bookmark` | Permalink to nearest ancestor section |

### 9.3 Accessible Link Text

```html
<!-- WRONG — meaningless link text -->
<a href="/docs/html5-guide.pdf">Click here</a>
<a href="/learn">Read more</a>
<a href="https://w3.org">This website</a>

<!-- CORRECT — descriptive link text -->
<a href="/docs/html5-guide.pdf">Download the HTML5 Guide (PDF)</a>
<a href="/learn">Learn more about semantic HTML</a>
<a href="https://w3.org">W3C — World Wide Web Consortium</a>

<!-- When context is in surrounding text, aria-label adds clarity -->
<article>
  <h3>HTML5 Guide</h3>
  <p>A comprehensive guide to semantic markup...</p>
  <a href="/html5-guide" aria-label="Read more about HTML5 Guide">Read more</a>
</article>

<!-- Icon-only links MUST have accessible text -->
<a href="https://twitter.com/webdev" aria-label="Follow us on Twitter">
  <svg aria-hidden="true" focusable="false"><!-- twitter icon --></svg>
</a>

<!-- Image links: alt text serves as link text -->
<a href="/">
  <img src="/logo.svg" alt="CompanyName — Home">
</a>
```

### 9.4 Skip Navigation Links

```html
<!-- Must be the FIRST element in <body> -->
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <header><!-- site header --></header>
  <nav><!-- navigation --></nav>

  <main id="main-content">
    <!-- Primary content -->
  </main>
</body>

<!-- Commonly styled to be visually hidden until focused:
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
}
.skip-link:focus {
  top: 0;
}
-->
```

---

## 10. Images and Figures

### 10.1 The `<img>` Element

```html
<!-- Basic image — alt is REQUIRED -->
<img src="/images/hero.jpg" alt="Aerial view of downtown San Francisco at golden hour">

<!-- Decorative image — empty alt -->
<img src="/images/decorative-divider.png" alt="">

<!-- Responsive image — width/height prevent layout shift (CLS) -->
<img
  src="/images/photo.jpg"
  alt="Team photo from the 2025 annual conference"
  width="800"
  height="600"
  loading="lazy"
  decoding="async"
>
```

### 10.2 Crafting `alt` Text

**Rules for `alt` attribute:**

```html
<!-- Informative images: describe what the image conveys -->
<img src="chart.png" alt="Bar chart showing 40% growth in web accessibility adoption from 2020 to 2025">

<!-- Functional images (buttons, links): describe the action or destination -->
<a href="/"><img src="logo.png" alt="CompanyName — Return to homepage"></a>

<!-- Decorative images: empty alt (NOT missing alt) -->
<img src="flourish.svg" alt="">

<!-- Images of text: reproduce the text -->
<img src="sale-banner.png" alt="Summer Sale — 50% off all items this weekend only">

<!-- Complex images (diagrams, charts): provide extended description -->
<figure>
  <img
    src="complex-diagram.png"
    alt="Network topology diagram"
    aria-describedby="diagram-description"
  >
  <figcaption id="diagram-description">
    The diagram shows three server nodes connected in a triangle configuration.
    Server A (primary) connects to Server B (backup) and Server C (cache).
    Server B and Server C also connect to each other for redundancy.
  </figcaption>
</figure>

<!-- WRONG: never do these -->
<img src="photo.jpg">                          <!-- missing alt -->
<img src="photo.jpg" alt="photo">              <!-- meaningless alt -->
<img src="photo.jpg" alt="image of a cat">     <!-- redundant "image of" -->
<img src="logo.png" alt="logo">                <!-- meaningless -->
```

### 10.3 Responsive Images

```html
<!-- srcset for resolution switching (same image, different sizes) -->
<img
  src="/images/hero-800.jpg"
  srcset="/images/hero-400.jpg 400w,
          /images/hero-800.jpg 800w,
          /images/hero-1200.jpg 1200w,
          /images/hero-2400.jpg 2400w"
  sizes="(max-width: 600px) 100vw,
         (max-width: 1200px) 50vw,
         800px"
  alt="Mountain landscape at sunrise"
  width="800"
  height="533"
>

<!-- <picture> for art direction (different crops for different screens) -->
<picture>
  <!-- Mobile: portrait crop -->
  <source
    media="(max-width: 767px)"
    srcset="/images/hero-mobile.webp 400w, /images/hero-mobile@2x.webp 800w"
    type="image/webp"
  >
  <!-- Modern format first, fallback last -->
  <source
    media="(min-width: 768px)"
    srcset="/images/hero-desktop.webp 800w, /images/hero-desktop@2x.webp 1600w"
    type="image/webp"
  >
  <!-- JPEG fallback for browsers without WebP support -->
  <img
    src="/images/hero-desktop.jpg"
    alt="CEO Jane Doe speaking at the 2025 Web Summit"
    width="1200"
    height="630"
    loading="eager"
    fetchpriority="high"
  >
</picture>

<!-- SVG inline for icons/illustrations (optimal for scalability) -->
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
     viewBox="0 0 24 24" aria-hidden="true" focusable="false">
  <path d="M12 2L2 7l10 5 10-5-10-5z"/>
  <path d="M2 17l10 5 10-5"/>
  <path d="M2 12l10 5 10-5"/>
</svg>
```

**`loading` attribute values:**

| Value | Behavior |
|-------|---------|
| `lazy` | Deferred until near viewport (use for below-fold images) |
| `eager` | Load immediately (default, use for above-fold/hero images) |

**`decoding` attribute:**

| Value | Behavior |
|-------|---------|
| `async` | Decode off main thread (recommended for most images) |
| `sync` | Decode synchronously (use when image must appear instantly) |
| `auto` | Browser decides |

**`fetchpriority` attribute:**

| Value | Use case |
|-------|---------|
| `high` | LCP (Largest Contentful Paint) image — hero, above fold |
| `low` | Below-fold images, thumbnails |
| `auto` | Default |

---

## 11. Tables

### 11.1 Table Structure Elements

```html
<!-- Complete, accessible table -->
<table>
  <caption>
    Q2 2025 Sales Performance by Region
  </caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Sales (USD)</th>
      <th scope="col">Growth</th>
      <th scope="col">Target Met</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">North America</th>
      <td>$1,250,000</td>
      <td>+12%</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th scope="row">Europe</th>
      <td>$890,000</td>
      <td>+7%</td>
      <td>Yes</td>
    </tr>
    <tr>
      <th scope="row">Asia Pacific</th>
      <td>$620,000</td>
      <td>+24%</td>
      <td>No</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$2,760,000</td>
      <td>+14%</td>
      <td>—</td>
    </tr>
  </tfoot>
</table>
```

### 11.2 Table Elements Reference

| Element | Purpose |
|---------|---------|
| `<table>` | The table container |
| `<caption>` | Table title/description (first child of `<table>`) |
| `<colgroup>` | Groups one or more columns |
| `<col>` | Represents a column (void element, inside `<colgroup>`) |
| `<thead>` | Header row group |
| `<tbody>` | Body row group (can be multiple) |
| `<tfoot>` | Footer row group |
| `<tr>` | Table row |
| `<th>` | Header cell |
| `<td>` | Data cell |

### 11.3 Scope and Headers Attributes

```html
<!-- Simple table: scope attribute -->
<table>
  <caption>Student Grades</caption>
  <thead>
    <tr>
      <th scope="col">Student</th>
      <th scope="col">Math</th>
      <th scope="col">Science</th>
      <th scope="col">English</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Alice</th>
      <td>92</td>
      <td>88</td>
      <td>95</td>
    </tr>
    <tr>
      <th scope="row">Bob</th>
      <td>78</td>
      <td>82</td>
      <td>70</td>
    </tr>
  </tbody>
</table>

<!-- Complex table: headers + id attributes -->
<table>
  <caption>Conference Room Booking Schedule</caption>
  <thead>
    <tr>
      <th id="room-header">Room</th>
      <th id="mon" scope="col">Monday</th>
      <th id="tue" scope="col">Tuesday</th>
      <th id="wed" scope="col">Wednesday</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="room-a" scope="row">Room A</th>
      <td headers="mon room-a">Engineering</td>
      <td headers="tue room-a">Available</td>
      <td headers="wed room-a">Marketing</td>
    </tr>
    <tr>
      <th id="room-b" scope="row">Room B</th>
      <td headers="mon room-b">HR</td>
      <td headers="tue room-b">Engineering</td>
      <td headers="wed room-b">Available</td>
    </tr>
  </tbody>
</table>
```

**`scope` values:**

| Value | Meaning |
|-------|---------|
| `col` | Header applies to its column |
| `row` | Header applies to its row |
| `colgroup` | Header applies to a column group |
| `rowgroup` | Header applies to a row group |

### 11.4 Cell Spanning

```html
<table>
  <caption>Weekly Schedule</caption>
  <thead>
    <tr>
      <th scope="col">Time</th>
      <th scope="col">Monday</th>
      <th scope="col">Tuesday</th>
      <th scope="col">Wednesday</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">9:00 AM</th>
      <td colspan="2">Team Standup (Mon–Tue)</td>  <!-- spans 2 columns -->
      <td>Design Review</td>
    </tr>
    <tr>
      <th scope="row">10:00 AM</th>
      <td>Development</td>
      <td rowspan="2">All-day Workshop</td>  <!-- spans 2 rows -->
      <td>Development</td>
    </tr>
    <tr>
      <th scope="row">11:00 AM</th>
      <td>Code Review</td>
      <!-- Tue cell covered by rowspan above -->
      <td>Deployment</td>
    </tr>
  </tbody>
</table>
```

### 11.5 Column Styling with `<colgroup>`

```html
<table>
  <caption>Budget Overview</caption>
  <colgroup>
    <col>                           <!-- Category column -->
    <col class="budget-col">        <!-- Budget column -->
    <col class="actual-col">        <!-- Actual column -->
    <col span="2" class="diff-col"> <!-- Spans 2 columns -->
  </colgroup>
  <thead>
    <tr>
      <th scope="col">Category</th>
      <th scope="col">Budget</th>
      <th scope="col">Actual</th>
      <th scope="col">Difference</th>
      <th scope="col">Status</th>
    </tr>
  </thead>
  <!-- tbody... -->
</table>
```

**Critical table rules:**
- Tables are for **tabular data** — never for layout
- Always include `<caption>` for accessibility
- Always use `scope` on `<th>` elements
- Use `<thead>`, `<tbody>`, `<tfoot>` to group rows
- Do not use `<table>` for visual grid layouts — use CSS Grid or Flexbox

---

## 12. Forms

### 12.1 The `<form>` Element

```html
<form
  action="/api/submit"
  method="post"
  enctype="multipart/form-data"
  novalidate
  aria-labelledby="form-title"
>
  <h2 id="form-title">Contact Us</h2>
  <!-- form controls -->
</form>
```

**`<form>` attributes:**

| Attribute | Values | Description |
|-----------|--------|-------------|
| `action` | URL | Where to send form data |
| `method` | `get`, `post` | HTTP method |
| `enctype` | `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain` | Encoding (use `multipart/form-data` for file uploads) |
| `novalidate` | Boolean | Disables browser validation (handle in JS) |
| `autocomplete` | `on`, `off` | Enable/disable autocomplete |
| `target` | `_blank`, `_self`… | Where to display response |

### 12.2 Labels — The Most Important Rule

```html
<!-- Method 1: Explicit association (preferred) -->
<label for="email">Email address</label>
<input type="email" id="email" name="email">

<!-- Method 2: Implicit wrapping -->
<label>
  Email address
  <input type="email" name="email">
</label>

<!-- Method 3: aria-labelledby (when label element not possible) -->
<span id="search-label">Search the site</span>
<input type="search" aria-labelledby="search-label">

<!-- Method 4: aria-label (when no visible label possible) -->
<input type="search" aria-label="Search">

<!-- WRONG: placeholder is NOT a label -->
<input type="email" placeholder="Enter your email">   <!-- no label! -->
```

**Rules:**
- Every `<input>`, `<select>`, `<textarea>` must have an accessible name
- `<label>` is preferred over ARIA alternatives
- `placeholder` disappears on input — cannot substitute for a label
- `for` attribute must exactly match the `id` of the control

### 12.3 Input Types Reference

```html
<!-- Text inputs -->
<input type="text"     id="name"    name="name"    autocomplete="name">
<input type="email"    id="email"   name="email"   autocomplete="email">
<input type="password" id="pwd"     name="password" autocomplete="current-password">
<input type="tel"      id="phone"   name="phone"   autocomplete="tel">
<input type="url"      id="website" name="website" autocomplete="url">
<input type="search"   id="q"       name="q">
<input type="number"   id="qty"     name="qty"     min="1" max="99" step="1">
<input type="range"    id="vol"     name="volume"  min="0" max="100" value="50">

<!-- Date/Time inputs -->
<input type="date"           id="bday"  name="birthday"  autocomplete="bday">
<input type="time"           id="appt"  name="appointment-time">
<input type="datetime-local" id="event" name="event-datetime">
<input type="month"          id="mon"   name="month">
<input type="week"           id="wk"    name="week">

<!-- File and color -->
<input type="file"  id="avatar" name="avatar" accept="image/png, image/jpeg" multiple>
<input type="color" id="color"  name="theme-color" value="#0066cc">

<!-- Hidden -->
<input type="hidden" name="csrf_token" value="abc123xyz">

<!-- Buttons -->
<input type="submit" value="Submit Form">
<input type="reset"  value="Reset">
<input type="button" value="Click Me">
<input type="image"  src="/submit.png" alt="Submit" width="80" height="30">

<!-- Checkbox and Radio -->
<input type="checkbox" id="agree" name="agree" value="yes">
<input type="radio" id="choice-a" name="choice" value="a">
```

### 12.4 Complete Accessible Form

```html
<form action="/register" method="post" novalidate>
  <h2 id="register-heading">Create an Account</h2>

  <!-- Name group -->
  <div class="form-group">
    <label for="first-name">First name <span aria-hidden="true">*</span></label>
    <input
      type="text"
      id="first-name"
      name="first_name"
      autocomplete="given-name"
      required
      aria-required="true"
      aria-describedby="first-name-error"
    >
    <span id="first-name-error" role="alert" aria-live="polite"></span>
  </div>

  <div class="form-group">
    <label for="last-name">Last name <span aria-hidden="true">*</span></label>
    <input
      type="text"
      id="last-name"
      name="last_name"
      autocomplete="family-name"
      required
      aria-required="true"
    >
  </div>

  <!-- Email -->
  <div class="form-group">
    <label for="reg-email">Email address <span aria-hidden="true">*</span></label>
    <input
      type="email"
      id="reg-email"
      name="email"
      autocomplete="email"
      required
      aria-required="true"
      aria-describedby="email-hint"
      inputmode="email"
    >
    <p id="email-hint" class="hint">We'll send a confirmation to this address.</p>
  </div>

  <!-- Password -->
  <div class="form-group">
    <label for="reg-password">Password <span aria-hidden="true">*</span></label>
    <input
      type="password"
      id="reg-password"
      name="password"
      autocomplete="new-password"
      required
      aria-required="true"
      aria-describedby="password-rules"
      minlength="8"
    >
    <p id="password-rules" class="hint">
      At least 8 characters, including one number and one special character.
    </p>
  </div>

  <!-- Radio group -->
  <fieldset>
    <legend>Account type <span aria-hidden="true">*</span></legend>
    <div>
      <input type="radio" id="acct-personal" name="account_type" value="personal" required>
      <label for="acct-personal">Personal</label>
    </div>
    <div>
      <input type="radio" id="acct-business" name="account_type" value="business">
      <label for="acct-business">Business</label>
    </div>
  </fieldset>

  <!-- Checkboxes -->
  <fieldset>
    <legend>Email preferences</legend>
    <div>
      <input type="checkbox" id="pref-news" name="preferences" value="newsletter">
      <label for="pref-news">Monthly newsletter</label>
    </div>
    <div>
      <input type="checkbox" id="pref-updates" name="preferences" value="updates">
      <label for="pref-updates">Product updates</label>
    </div>
    <div>
      <input type="checkbox" id="pref-security" name="preferences" value="security" checked>
      <label for="pref-security">Security alerts</label>
    </div>
  </fieldset>

  <!-- Select -->
  <div class="form-group">
    <label for="country">Country</label>
    <select id="country" name="country" autocomplete="country">
      <option value="">— Select your country —</option>
      <optgroup label="North America">
        <option value="US">United States</option>
        <option value="CA">Canada</option>
        <option value="MX">Mexico</option>
      </optgroup>
      <optgroup label="Europe">
        <option value="GB">United Kingdom</option>
        <option value="DE">Germany</option>
        <option value="FR">France</option>
        <option value="UA">Ukraine</option>
      </optgroup>
    </select>
  </div>

  <!-- Textarea -->
  <div class="form-group">
    <label for="bio">Short bio</label>
    <textarea
      id="bio"
      name="bio"
      rows="4"
      maxlength="500"
      aria-describedby="bio-count"
    ></textarea>
    <span id="bio-count" aria-live="polite">0 / 500 characters</span>
  </div>

  <!-- File upload -->
  <div class="form-group">
    <label for="avatar-upload">Profile photo</label>
    <input
      type="file"
      id="avatar-upload"
      name="avatar"
      accept="image/jpeg,image/png,image/webp"
      aria-describedby="avatar-hint"
    >
    <p id="avatar-hint" class="hint">JPG, PNG or WebP. Max 2MB.</p>
  </div>

  <!-- Required fields notice -->
  <p><span aria-hidden="true">*</span> Required fields</p>

  <!-- Submit -->
  <button type="submit">Create Account</button>
</form>
```

### 12.5 `<fieldset>` and `<legend>`

```html
<!-- Always use fieldset + legend for radio/checkbox groups -->
<fieldset>
  <legend>Shipping method</legend>
  <label>
    <input type="radio" name="shipping" value="standard">
    Standard (5–7 days)
  </label>
  <label>
    <input type="radio" name="shipping" value="express">
    Express (2–3 days)
  </label>
  <label>
    <input type="radio" name="shipping" value="overnight">
    Overnight (next day)
  </label>
</fieldset>

<!-- Fieldset for logical form sections -->
<fieldset>
  <legend>Billing address</legend>
  <div>
    <label for="bill-street">Street address</label>
    <input type="text" id="bill-street" name="billing_street" autocomplete="billing street-address">
  </div>
  <div>
    <label for="bill-city">City</label>
    <input type="text" id="bill-city" name="billing_city" autocomplete="billing address-level2">
  </div>
  <div>
    <label for="bill-zip">ZIP / Postal code</label>
    <input type="text" id="bill-zip" name="billing_zip" autocomplete="billing postal-code">
  </div>
</fieldset>
```

### 12.6 Buttons

```html
<!-- <button type="submit"> — submits form (default type) -->
<button type="submit">Submit Application</button>

<!-- <button type="button"> — no default action, use for JS interactions -->
<button type="button" id="open-modal">Open Settings</button>
<button type="button" aria-expanded="false" aria-controls="menu">Menu</button>

<!-- <button type="reset"> — resets all form fields to defaults -->
<button type="reset">Reset Form</button>

<!-- Button with icon + text -->
<button type="submit">
  <svg aria-hidden="true" focusable="false" width="16" height="16">
    <!-- checkmark icon -->
  </svg>
  Save Changes
</button>

<!-- Icon-only button — MUST have accessible name -->
<button type="button" aria-label="Delete item">
  <svg aria-hidden="true" focusable="false"><!-- trash icon --></svg>
</button>

<!-- Disabled button -->
<button type="submit" disabled aria-disabled="true">Processing...</button>
```

**Rules:**
- Always specify `type` on `<button>` — default is `submit` which can cause accidental form submission
- Prefer `<button>` over `<input type="submit">` — `<button>` can contain HTML
- Never use `<div>` or `<span>` as buttons — they are not keyboard accessible by default
- Disabled buttons: add both `disabled` attribute and `aria-disabled="true"`

### 12.7 Autocomplete Attribute Values

```html
<!-- Personal info -->
<input autocomplete="name">
<input autocomplete="given-name">
<input autocomplete="family-name">
<input autocomplete="email">
<input autocomplete="tel">
<input autocomplete="bday">        <!-- Birthday -->
<input autocomplete="sex">

<!-- Address -->
<input autocomplete="street-address">
<input autocomplete="address-line1">
<input autocomplete="address-line2">
<input autocomplete="address-level2"> <!-- City -->
<input autocomplete="address-level1"> <!-- State/Province -->
<input autocomplete="postal-code">
<input autocomplete="country">

<!-- Credentials -->
<input autocomplete="username">
<input autocomplete="current-password">
<input autocomplete="new-password">
<input autocomplete="one-time-code">

<!-- Payment -->
<input autocomplete="cc-name">
<input autocomplete="cc-number">
<input autocomplete="cc-exp">
<input autocomplete="cc-csc">

<!-- Billing prefix -->
<input autocomplete="billing postal-code">
<input autocomplete="billing street-address">

<!-- Shipping prefix -->
<input autocomplete="shipping address-level2">
```

---

## 13. Interactive Elements

### 13.1 `<details>` and `<summary>` (Disclosure Widget)

*(Covered in Section 7.6)*

### 13.2 `<dialog>` Element

```html
<!-- Modal dialog -->
<dialog id="confirm-dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirm Deletion</h2>
  <p>Are you sure you want to delete this item? This action cannot be undone.</p>
  <form method="dialog">
    <button type="button" id="cancel-btn">Cancel</button>
    <button type="submit" value="confirm">Delete</button>
  </form>
</dialog>

<!-- Non-modal dialog -->
<dialog id="notification">
  <p>Your file has been saved successfully.</p>
  <button type="button" autofocus>Dismiss</button>
</dialog>

<!-- JavaScript to show -->
<script>
  // Show modal
  document.getElementById('confirm-dialog').showModal();

  // Show non-modal
  document.getElementById('notification').show();

  // Close
  document.getElementById('confirm-dialog').close();
</script>
```

**`<dialog>` rules:**
- `showModal()` creates a modal with focus trap and backdrop
- `show()` creates a non-modal dialog
- `method="dialog"` on an inner form closes the dialog on submit
- Always set `aria-modal="true"` for modals
- Always label with `aria-labelledby` pointing to a heading inside

### 13.3 Custom Interactive Patterns

When semantic elements cannot be used, apply ARIA roles:

```html
<!-- Tab interface -->
<div role="tablist" aria-label="Settings panels">
  <button role="tab" id="tab-general" aria-controls="panel-general" aria-selected="true">
    General
  </button>
  <button role="tab" id="tab-security" aria-controls="panel-security" aria-selected="false" tabindex="-1">
    Security
  </button>
  <button role="tab" id="tab-privacy" aria-controls="panel-privacy" aria-selected="false" tabindex="-1">
    Privacy
  </button>
</div>

<div role="tabpanel" id="panel-general" aria-labelledby="tab-general">
  <!-- General settings content -->
</div>
<div role="tabpanel" id="panel-security" aria-labelledby="tab-security" hidden>
  <!-- Security settings content -->
</div>
<div role="tabpanel" id="panel-privacy" aria-labelledby="tab-privacy" hidden>
  <!-- Privacy settings content -->
</div>

<!-- Accordion -->
<div>
  <h3>
    <button
      type="button"
      aria-expanded="true"
      aria-controls="section1-content"
      id="section1-header"
    >
      What is semantic HTML?
    </button>
  </h3>
  <div
    id="section1-content"
    role="region"
    aria-labelledby="section1-header"
  >
    <p>Semantic HTML uses elements that convey meaning...</p>
  </div>
</div>
```

---

## 14. Embedded Content and Media

### 14.1 `<video>`

```html
<!-- Basic accessible video -->
<video
  controls
  width="800"
  height="450"
  poster="/thumbnails/intro-video.jpg"
  preload="metadata"
>
  <!-- Multiple formats for browser compatibility -->
  <source src="/videos/intro.webm" type="video/webm">
  <source src="/videos/intro.mp4"  type="video/mp4">

  <!-- Subtitles / Closed captions -->
  <track
    kind="subtitles"
    src="/captions/intro.en.vtt"
    srclang="en"
    label="English"
    default
  >
  <track
    kind="subtitles"
    src="/captions/intro.fr.vtt"
    srclang="fr"
    label="Français"
  >
  <!-- Audio descriptions for blind users -->
  <track
    kind="descriptions"
    src="/descriptions/intro.en.vtt"
    srclang="en"
    label="English descriptions"
  >

  <!-- Fallback for no video support -->
  <p>
    Your browser does not support HTML5 video.
    <a href="/videos/intro.mp4">Download the video</a>.
  </p>
</video>
```

**`<track>` kind values:**

| Kind | Purpose |
|------|---------|
| `subtitles` | Transcription or translation of dialogue |
| `captions` | Subtitles + non-speech audio (sound effects, music) for deaf users |
| `descriptions` | Text description of video content for blind users |
| `chapters` | Chapter navigation |
| `metadata` | Programmatic use, not displayed |

**Video attributes:**

| Attribute | Purpose |
|-----------|---------|
| `controls` | Show browser controls (always include) |
| `autoplay` | Play on load (use with `muted` only) |
| `muted` | Muted by default (required with autoplay) |
| `loop` | Loop playback |
| `playsinline` | Play inline on iOS (not fullscreen) |
| `poster` | Thumbnail image before play |
| `preload` | `none`, `metadata`, `auto` |

### 14.2 `<audio>`

```html
<audio controls preload="metadata">
  <source src="/audio/podcast-ep42.opus" type="audio/ogg; codecs=opus">
  <source src="/audio/podcast-ep42.mp3"  type="audio/mpeg">
  <track kind="captions" src="/captions/ep42.vtt" srclang="en" label="English" default>
  <p>
    Your browser does not support HTML5 audio.
    <a href="/audio/podcast-ep42.mp3">Download the audio</a>.
  </p>
</audio>
```

### 14.3 `<iframe>`

```html
<!-- Map embed -->
<iframe
  src="https://maps.google.com/..."
  width="600"
  height="450"
  style="border:0"
  allowfullscreen
  loading="lazy"
  referrerpolicy="no-referrer-when-downgrade"
  title="Company office location on Google Maps"
></iframe>

<!-- YouTube embed -->
<iframe
  src="https://www.youtube.com/embed/VIDEO_ID"
  width="560"
  height="315"
  title="Introduction to Semantic HTML — Tutorial Video"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen
  loading="lazy"
></iframe>

<!-- Sandboxed iframe for untrusted content -->
<iframe
  src="/user-content/preview.html"
  sandbox="allow-scripts allow-same-origin"
  title="User content preview"
></iframe>
```

**Sandbox attribute values:**

| Value | Permission granted |
|-------|--------------------|
| `allow-forms` | Form submission |
| `allow-scripts` | Script execution |
| `allow-same-origin` | Same-origin access |
| `allow-top-navigation` | Navigate top-level browsing context |
| `allow-popups` | `window.open()` |
| `allow-downloads` | File downloads |
| (empty) | Maximum restriction |

**Rules:**
- Always specify `title` attribute — required for accessibility
- `loading="lazy"` for below-fold iframes
- Use `sandbox` for untrusted content
- Avoid `frameborder` attribute — use CSS `border: none` instead

### 14.4 `<canvas>`

```html
<!-- Canvas requires fallback content and accessible label -->
<canvas
  id="chart-canvas"
  width="600"
  height="400"
  role="img"
  aria-label="Bar chart showing monthly revenue growth from January to June 2025"
>
  <!-- Fallback for no canvas support -->
  <p>Monthly Revenue Chart: Jan $10k, Feb $12k, Mar $15k, Apr $14k, May $18k, Jun $22k</p>
</canvas>
```

### 14.5 `<svg>` Inline

```html
<!-- Informative SVG: requires title and/or description -->
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 100 100"
  role="img"
  aria-labelledby="svg-title svg-desc"
>
  <title id="svg-title">Revenue growth chart</title>
  <desc id="svg-desc">Line chart showing 120% revenue growth over Q1-Q2 2025</desc>
  <!-- SVG content -->
  <polyline points="10,90 30,70 50,50 70,30 90,10" fill="none" stroke="#0066cc"/>
</svg>

<!-- Decorative SVG: hidden from screen readers -->
<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
</svg>
```

---

## 15. Scripting Elements

### 15.1 `<script>`

```html
<!-- External script — defer recommended -->
<script src="/js/app.js" defer></script>

<!-- Module script -->
<script type="module" src="/js/app.mjs"></script>

<!-- Inline script (minimize use) -->
<script>
  // Acceptable: theme initialization before paint
  document.documentElement.dataset.theme = localStorage.getItem('theme') || 'light';
</script>

<!-- Script with integrity and crossorigin -->
<script
  src="https://cdn.example.com/library.min.js"
  integrity="sha384-AbCdEfGhIjKlMnOpQrStUvWxYzAbCd..."
  crossorigin="anonymous"
  defer
></script>

<!-- importmap for ES modules -->
<script type="importmap">
{
  "imports": {
    "react": "https://esm.sh/react@18",
    "react-dom": "https://esm.sh/react-dom@18"
  }
}
</script>
```

### 15.2 `<noscript>`

```html
<!-- In <head>: alternative CSS/meta when JS is disabled -->
<head>
  <noscript>
    <link rel="stylesheet" href="/css/no-js.css">
  </noscript>
</head>

<!-- In <body>: visible fallback message -->
<noscript>
  <p class="noscript-warning">
    This application requires JavaScript to function.
    Please enable JavaScript in your browser settings.
  </p>
</noscript>
```

### 15.3 `<template>` and `<slot>`

```html
<!-- Template: not rendered until cloned via JS -->
<template id="product-card-template">
  <article class="product-card">
    <img class="product-image" src="" alt="">
    <h3 class="product-name"></h3>
    <p class="product-price"></p>
    <button type="button" class="add-to-cart">Add to Cart</button>
  </article>
</template>

<!-- Web Component usage -->
<my-card>
  <span slot="title">Product Name</span>
  <span slot="price">$29.99</span>
</my-card>
```

---

## 16. Metadata and Microdata

### 16.1 JSON-LD (Recommended by Google)

```html
<!-- Article structured data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Complete HTML5 Semantic Markup Guide",
  "description": "A comprehensive W3C-compliant reference for HTML5 semantics.",
  "image": "https://example.com/images/html5-guide.jpg",
  "author": {
    "@type": "Person",
    "name": "Jane Doe",
    "url": "https://example.com/authors/jane"
  },
  "publisher": {
    "@type": "Organization",
    "name": "DevDocs",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2025-06-01T09:00:00+00:00",
  "dateModified": "2025-06-01T09:00:00+00:00",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/html5-guide"
  }
}
</script>

<!-- Organization structured data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer service"
  },
  "sameAs": [
    "https://twitter.com/example",
    "https://www.linkedin.com/company/example"
  ]
}
</script>

<!-- Breadcrumb structured data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog"},
    {"@type": "ListItem", "position": 3, "name": "HTML5 Guide"}
  ]
}
</script>

<!-- FAQ Page structured data -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is semantic HTML?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Semantic HTML uses elements that convey meaning about the content they contain."
      }
    },
    {
      "@type": "Question",
      "name": "Why is semantic HTML important?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "It improves accessibility, SEO, and code maintainability."
      }
    }
  ]
}
</script>
```

### 16.2 Microdata (HTML Attributes)

```html
<!-- Product with microdata -->
<article itemscope itemtype="https://schema.org/Product">
  <img itemprop="image" src="/products/widget.jpg" alt="Blue Widget">
  <h2 itemprop="name">Blue Widget</h2>
  <p itemprop="description">An ergonomically designed widget for maximum comfort.</p>

  <div itemprop="offers" itemscope itemtype="https://schema.org/Offer">
    <span itemprop="priceCurrency" content="USD">$</span>
    <span itemprop="price" content="29.99">29.99</span>
    <link itemprop="availability" href="https://schema.org/InStock">In stock
  </div>

  <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
    <span itemprop="ratingValue">4.5</span>/5
    based on <span itemprop="reviewCount">128</span> reviews
  </div>
</article>
```

---

## 17. Accessibility — WAI-ARIA Integration

### 17.1 ARIA Principles

**The Five Rules of ARIA:**

1. **Use native HTML first** — a `<button>` is always better than `<div role="button">`
2. **Don't change native semantics** — don't add `role="heading"` to a `<button>`
3. **All interactive ARIA controls must be keyboard operable**
4. **Don't use `role="presentation"` or `aria-hidden="true"` on visible, focusable elements**
5. **All interactive elements must have an accessible name**

### 17.2 ARIA Landmark Roles

```html
<!-- Explicit landmarks (usually implicit via semantic elements) -->
<header role="banner">      <!-- Site header -->
<nav role="navigation">     <!-- Navigation -->
<main role="main">          <!-- Main content -->
<aside role="complementary"><!-- Sidebar -->
<footer role="contentinfo"> <!-- Site footer -->
<form role="search">        <!-- Search form -->
<section role="region" aria-labelledby="section-heading"> <!-- Named section -->
```

**Landmark roles and their HTML equivalents:**

| ARIA Role | Semantic Element | Notes |
|-----------|-----------------|-------|
| `banner` | `<header>` (top-level) | Only one per page |
| `navigation` | `<nav>` | Label with `aria-label` if multiple |
| `main` | `<main>` | Only one per page |
| `complementary` | `<aside>` | Related supplementary content |
| `contentinfo` | `<footer>` (top-level) | Only one per page |
| `search` | `<search>` | HTML element for search |
| `region` | `<section>` (with name) | Requires accessible name |
| `form` | `<form>` (with name) | Requires accessible name |

### 17.3 ARIA States and Properties

```html
<!-- Expanded/collapsed state -->
<button aria-expanded="false" aria-controls="menu-content">Menu</button>
<ul id="menu-content" hidden>
  <li><a href="/">Home</a></li>
</ul>

<!-- Selected state (listbox, tree) -->
<li role="option" aria-selected="true">Option A</li>

<!-- Checked state (custom checkbox) -->
<div role="checkbox" aria-checked="true" tabindex="0">Custom checkbox</div>

<!-- Pressed state (toggle button) -->
<button aria-pressed="false" type="button">Bold</button>

<!-- Required field -->
<input type="email" required aria-required="true">

<!-- Invalid field -->
<input type="email" aria-invalid="true" aria-describedby="email-error">
<span id="email-error" role="alert">Please enter a valid email address.</span>

<!-- Disabled -->
<button disabled aria-disabled="true">Cannot proceed</button>

<!-- Current page/item -->
<a href="/" aria-current="page">Home</a>
<li aria-current="step">Step 2 of 4</li>

<!-- Live regions (announced by screen readers) -->
<div role="alert" aria-live="assertive">
  Error: Form submission failed. Please try again.
</div>
<div aria-live="polite" aria-atomic="true">
  3 results found for "HTML"
</div>
<div role="status" aria-live="polite">
  File saved successfully.
</div>

<!-- Busy state (loading) -->
<div aria-busy="true" aria-live="polite">
  Loading results...
</div>

<!-- Controls/owns relationships -->
<button aria-controls="panel-id">Toggle Panel</button>
<div id="panel-id">Panel content</div>

<!-- Labelledby and describedby -->
<h2 id="section-title">Contact Form</h2>
<form aria-labelledby="section-title">
  <input aria-describedby="field-hint">
  <p id="field-hint">Enter your name as it appears on your ID.</p>
</form>
```

### 17.4 ARIA Roles Reference

**Widget roles:**

| Role | Element equivalent | Interactive? |
|------|--------------------|-------------|
| `button` | `<button>` | Yes |
| `checkbox` | `<input type="checkbox">` | Yes |
| `radio` | `<input type="radio">` | Yes |
| `textbox` | `<input type="text">` / `<textarea>` | Yes |
| `combobox` | `<select>` (complex) | Yes |
| `listbox` | `<select>` | Yes |
| `option` | `<option>` | No |
| `slider` | `<input type="range">` | Yes |
| `spinbutton` | `<input type="number">` | Yes |
| `switch` | Toggle button | Yes |
| `tab` | Tab button | Yes |
| `tabpanel` | Tab panel | No |
| `tablist` | Tab group | No |
| `tooltip` | Tooltip | No |
| `progressbar` | `<progress>` | No |
| `menuitem` | Menu item | Yes |
| `menu` | Dropdown menu | No |
| `menubar` | Navigation menu bar | No |
| `tree` | Tree view | Yes |
| `treeitem` | Tree item | Yes |
| `dialog` | `<dialog>` | Yes |
| `alertdialog` | Critical dialog | Yes |

**Document structure roles:**

| Role | Purpose |
|------|---------|
| `article` | Self-contained content |
| `columnheader` | Table column header |
| `definition` | Definition of a term |
| `figure` | Figurative content |
| `group` | Logical grouping |
| `heading` | Section heading |
| `img` | Image with alt text |
| `list` | List of items |
| `listitem` | Item in a list |
| `math` | Mathematical expression |
| `none` / `presentation` | Remove from accessibility tree |
| `note` | Supplementary content |
| `row` | Row in a grid/table |
| `rowgroup` | Group of rows |
| `rowheader` | Row header |
| `table` | Tabular data |
| `term` | Term being defined |

### 17.5 Keyboard Navigation

All interactive elements must be keyboard accessible:

```html
<!-- Focusable elements (naturally) -->
<a href="...">...</a>
<button>...</button>
<input>
<select>
<textarea>
<details>

<!-- Make custom element focusable -->
<div tabindex="0" role="button" onclick="..." onkeydown="...">Custom button</div>

<!-- Remove from tab order but keep focusable via JS -->
<div tabindex="-1" id="modal-content">...</div>

<!-- Skip link (keyboard shortcut to main content) -->
<a href="#main" class="skip-to-main">Skip to main content</a>

<!-- Focus management in dialogs -->
<dialog id="modal" aria-modal="true">
  <!-- First focusable element gets focus when dialog opens -->
  <button autofocus type="button">Close</button>
</dialog>
```

**`tabindex` values:**

| Value | Behavior |
|-------|---------|
| (absent) | Natural tab order (only natively focusable elements) |
| `0` | Added to natural tab order |
| `-1` | Focusable via JavaScript only (not in tab sequence) |
| `1` or higher | Sets position in tab order (AVOID — causes confusion) |

### 17.6 Color and Contrast

While contrast is CSS territory, HTML provides semantic hooks:

```html
<!-- Use semantic elements that convey state, not color alone -->
<!-- WRONG: only color indicates error -->
<p style="color: red;">Invalid input</p>

<!-- CORRECT: semantic + visual -->
<p role="alert">
  <strong>Error:</strong> Please enter a valid email address.
</p>
```

---

## 18. Global Attributes

Global attributes can be applied to any HTML element.

### 18.1 Core Global Attributes

```html
<!-- id — Unique identifier within document -->
<section id="features">

<!-- class — CSS class names -->
<p class="lead highlight">

<!-- style — Inline CSS (use sparingly) -->
<p style="font-size: 1.2rem;">

<!-- title — Advisory information (tooltip) -->
<abbr title="HyperText Markup Language">HTML</abbr>

<!-- lang — Language override for specific element -->
<p lang="fr">Bonjour le monde.</p>

<!-- dir — Text direction -->
<p dir="rtl">مرحبا</p>
<p dir="auto">Content with unknown direction</p>

<!-- tabindex — Keyboard navigation order -->
<div tabindex="0" role="button">Focusable div</div>

<!-- hidden — Hides element from all users (not just visually) -->
<div hidden>Not visible, not accessible</div>

<!-- contenteditable — Makes element editable -->
<div contenteditable="true" role="textbox" aria-multiline="true" aria-label="Notes">
  Edit this content.
</div>

<!-- draggable — Drag-and-drop -->
<li draggable="true">Draggable item</li>

<!-- spellcheck -->
<textarea spellcheck="true"></textarea>

<!-- translate — Whether to translate content -->
<span translate="no">CompanyBrand™</span>
```

### 18.2 Data Attributes

```html
<!-- Custom data-* attributes for JavaScript hooks -->
<button
  type="button"
  data-action="delete"
  data-item-id="42"
  data-confirm="Are you sure?"
>
  Delete
</button>

<article
  data-category="technology"
  data-published="2025-06-01"
  data-author-id="7"
>
  Article content...
</article>
```

**Rules for data attributes:**
- Name must be at least one character after `data-`
- Name must not contain uppercase letters
- Name must not contain colons (`:`)
- Value is always a string (parse in JavaScript as needed)

### 18.3 ARIA Global Attributes

These can be used on any element:

```html
aria-label          <!-- Accessible name -->
aria-labelledby     <!-- Accessible name from another element -->
aria-describedby    <!-- Additional description -->
aria-details        <!-- Detailed description (complex) -->
aria-hidden         <!-- Hide from accessibility tree -->
aria-live           <!-- Live region announcements -->
aria-atomic         <!-- Announce whole region or just changed part -->
aria-relevant       <!-- What changes to announce (additions/removals/text/all) -->
aria-busy           <!-- Loading state -->
aria-controls       <!-- ID(s) of controlled element(s) -->
aria-owns           <!-- ID(s) of owned elements -->
aria-flowto         <!-- Reading order override -->
aria-current        <!-- Current item in set (page/step/date/time/location/true) -->
aria-keyshortcuts   <!-- Keyboard shortcut hint -->
aria-roledescription <!-- Override the role description -->
```

---

## 19. Complete Page Patterns

### 19.1 Standard Article Page

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Complete HTML5 Guide — DevDocs</title>
  <meta name="description" content="Comprehensive W3C-compliant semantic HTML5 reference.">
  <link rel="canonical" href="https://devdocs.example.com/html5-guide">
  <link rel="stylesheet" href="/css/main.css">
  <meta property="og:title" content="Complete HTML5 Guide">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://devdocs.example.com/images/html5-og.jpg">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "Complete HTML5 Guide",
    "author": {"@type": "Person", "name": "Jane Doe"}
  }
  </script>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <header>
    <a href="/" aria-label="DevDocs — Home">
      <img src="/logo.svg" alt="DevDocs" width="120" height="36">
    </a>
    <nav aria-label="Primary">
      <ul>
        <li><a href="/html">HTML</a></li>
        <li><a href="/css">CSS</a></li>
        <li><a href="/javascript">JavaScript</a></li>
      </ul>
    </nav>
    <div role="search">
      <label for="site-search" class="visually-hidden">Search DevDocs</label>
      <input type="search" id="site-search" name="q" placeholder="Search...">
      <button type="submit">Search</button>
    </div>
  </header>

  <nav aria-label="Breadcrumb">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/html">HTML</a></li>
      <li><span aria-current="page">HTML5 Guide</span></li>
    </ol>
  </nav>

  <div class="layout-container">
    <main id="main-content">
      <article>
        <header>
          <h1>Complete HTML5 Semantic Markup Guide</h1>
          <dl>
            <div>
              <dt>Author</dt>
              <dd>
                <a href="/authors/jane" rel="author">Jane Doe</a>
              </dd>
            </div>
            <div>
              <dt>Published</dt>
              <dd>
                <time datetime="2025-06-01T09:00:00Z">June 1, 2025</time>
              </dd>
            </div>
            <div>
              <dt>Reading time</dt>
              <dd>15 minutes</dd>
            </div>
          </dl>
        </header>

        <nav aria-label="Table of contents">
          <h2>Contents</h2>
          <ol>
            <li><a href="#introduction">Introduction</a></li>
            <li><a href="#document-structure">Document Structure</a></li>
            <li><a href="#sectioning">Sectioning Elements</a></li>
          </ol>
        </nav>

        <section id="introduction">
          <h2>Introduction</h2>
          <p>Semantic HTML is the practice of using HTML elements
             according to their intended purpose...</p>

          <figure>
            <img
              src="/images/semantic-diagram.png"
              alt="Diagram of a webpage with labeled semantic regions: header, nav, main, article, aside, footer"
              width="800"
              height="500"
              loading="lazy"
              decoding="async"
            >
            <figcaption>
              Fig. 1: Typical arrangement of HTML5 semantic elements.
            </figcaption>
          </figure>
        </section>

        <section id="document-structure">
          <h2>Document Structure</h2>
          <p>Every HTML5 document begins with a DOCTYPE declaration...</p>

          <figure>
            <pre><code class="language-html">
&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
  &lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Page Title&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;!-- Content --&gt;
  &lt;/body&gt;
&lt;/html&gt;
            </code></pre>
            <figcaption>Listing 1: Minimum valid HTML5 document</figcaption>
          </figure>

          <details>
            <summary>Why does the DOCTYPE matter?</summary>
            <p>The DOCTYPE tells the browser to use standards mode rendering,
               preventing quirks mode which may break layout.</p>
          </details>
        </section>

        <footer>
          <section aria-label="Article metadata">
            <dl>
              <div>
                <dt>Last updated</dt>
                <dd><time datetime="2025-06-01">June 1, 2025</time></dd>
              </div>
              <div>
                <dt>License</dt>
                <dd><a href="https://creativecommons.org/licenses/by/4.0/" rel="license">CC BY 4.0</a></dd>
              </div>
            </dl>
          </section>

          <section aria-label="Tags">
            <h2>Tags</h2>
            <ul>
              <li><a href="/tags/html">HTML</a></li>
              <li><a href="/tags/semantics">Semantics</a></li>
              <li><a href="/tags/accessibility">Accessibility</a></li>
            </ul>
          </section>
        </footer>
      </article>

      <section aria-labelledby="comments-heading">
        <h2 id="comments-heading">Comments (3)</h2>

        <article>
          <header>
            <h3>
              <a href="/users/alice">Alice</a>
            </h3>
            <time datetime="2025-06-02T11:00:00Z">June 2, 2025 at 11:00 AM</time>
          </header>
          <p>This is exactly the reference I needed. Bookmarked!</p>
        </article>

      </section>
    </main>

    <aside aria-label="Related resources">
      <h2>Related</h2>
      <ul>
        <li><a href="/css-guide">CSS Guide</a></li>
        <li><a href="/aria-guide">ARIA Guide</a></li>
      </ul>

      <section aria-labelledby="ad-label">
        <h3 id="ad-label" class="visually-hidden">Advertisement</h3>
        <div aria-label="Advertisement">
          <!-- ad content -->
        </div>
      </section>
    </aside>
  </div>

  <footer>
    <nav aria-label="Footer links">
      <ul>
        <li><a href="/about">About</a></li>
        <li><a href="/privacy">Privacy Policy</a></li>
        <li><a href="/terms">Terms of Service</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
    <p>
      <small>
        &copy; <time datetime="2025">2025</time> DevDocs.
        Content licensed under
        <a href="https://creativecommons.org/licenses/by/4.0/" rel="license">CC BY 4.0</a>.
      </small>
    </p>
  </footer>

  <script src="/js/app.js" defer></script>
</body>
</html>
```

### 19.2 E-Commerce Product Page Pattern

```html
<main>
  <nav aria-label="Breadcrumb">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/shop">Shop</a></li>
      <li><a href="/shop/gadgets">Gadgets</a></li>
      <li><span aria-current="page">Blue Widget Pro</span></li>
    </ol>
  </nav>

  <article itemscope itemtype="https://schema.org/Product">
    <section aria-label="Product images">
      <figure>
        <img
          src="/products/blue-widget-main.webp"
          alt="Blue Widget Pro — front view, matte blue finish"
          width="600"
          height="600"
          loading="eager"
          fetchpriority="high"
          itemprop="image"
        >
      </figure>
    </section>

    <div class="product-info">
      <h1 itemprop="name">Blue Widget Pro</h1>

      <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
        <span aria-label="4.5 out of 5 stars">★★★★½</span>
        (<span itemprop="reviewCount">248</span> reviews)
      </div>

      <div itemprop="offers" itemscope itemtype="https://schema.org/Offer">
        <p>
          <strong>
            <span itemprop="priceCurrency" content="USD">$</span><span itemprop="price" content="49.99">49.99</span>
          </strong>
        </p>
        <link itemprop="availability" href="https://schema.org/InStock">
        <p>In stock — ships within 2 business days</p>
      </div>

      <section aria-labelledby="options-heading">
        <h2 id="options-heading">Options</h2>
        <form action="/cart/add" method="post">
          <input type="hidden" name="product_id" value="widget-pro-blue">

          <fieldset>
            <legend>Color</legend>
            <label>
              <input type="radio" name="color" value="blue" checked>
              Blue
            </label>
            <label>
              <input type="radio" name="color" value="red">
              Red
            </label>
            <label>
              <input type="radio" name="color" value="green">
              Green
            </label>
          </fieldset>

          <div>
            <label for="quantity">Quantity</label>
            <input
              type="number"
              id="quantity"
              name="quantity"
              value="1"
              min="1"
              max="10"
            >
          </div>

          <button type="submit">Add to Cart</button>
        </form>
      </section>

      <section aria-labelledby="desc-heading">
        <h2 id="desc-heading">Description</h2>
        <p itemprop="description">
          The Blue Widget Pro features an ergonomic design optimized for...
        </p>
      </section>

      <section aria-labelledby="specs-heading">
        <h2 id="specs-heading">Specifications</h2>
        <dl>
          <dt>Dimensions</dt>
          <dd>10 × 5 × 3 cm</dd>
          <dt>Weight</dt>
          <dd>150 g</dd>
          <dt>Material</dt>
          <dd>Anodized aluminum</dd>
          <dt>Warranty</dt>
          <dd>2 years</dd>
        </dl>
      </section>
    </div>
  </article>
</main>
```

### 19.3 Navigation Patterns

```html
<!-- Mega menu pattern -->
<nav aria-label="Primary">
  <ul>
    <li>
      <button type="button" aria-expanded="false" aria-controls="products-menu">
        Products
      </button>
      <div id="products-menu" role="group" aria-label="Products submenu" hidden>
        <ul>
          <li><a href="/products/widgets">Widgets</a></li>
          <li><a href="/products/gadgets">Gadgets</a></li>
          <li><a href="/products/tools">Tools</a></li>
        </ul>
        <figure>
          <img src="/images/featured-product.jpg" alt="Featured: Pro Widget">
          <figcaption><a href="/products/pro-widget">Featured: Pro Widget</a></figcaption>
        </figure>
      </div>
    </li>
    <li><a href="/about">About</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>
```

---

## 20. Anti-Patterns and Common Mistakes

### 20.1 Structural Anti-Patterns

```html
<!-- ❌ WRONG: Using divs for everything -->
<div class="header">
  <div class="nav">
    <div class="nav-item">Home</div>
  </div>
</div>

<!-- ✅ CORRECT -->
<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<!-- ❌ WRONG: Using <section> as a generic wrapper -->
<section class="container">
  <section class="wrapper">
    <p>Text.</p>
  </section>
</section>

<!-- ✅ CORRECT: div for layout wrappers -->
<div class="container">
  <p>Text.</p>
</div>

<!-- ❌ WRONG: Using <article> for every card -->
<article class="stat-card">
  <div>42</div>
  <div>Users online</div>
</article>

<!-- ✅ CORRECT: <article> only for independently distributable content -->
<div class="stat-card">
  <strong class="stat-number">42</strong>
  <span class="stat-label">Users online</span>
</div>

<!-- ❌ WRONG: Missing <main> -->
<body>
  <header>...</header>
  <div id="content">...</div>
  <footer>...</footer>
</body>

<!-- ✅ CORRECT -->
<body>
  <header>...</header>
  <main>...</main>
  <footer>...</footer>
</body>

<!-- ❌ WRONG: Multiple <main> elements visible simultaneously -->
<main>First main</main>
<main>Second main</main>

<!-- ✅ CORRECT: Only one visible <main> -->
<main id="app-main">Content</main>
```

### 20.2 Heading Anti-Patterns

```html
<!-- ❌ WRONG: Multiple h1 elements -->
<h1>Page Title</h1>
<h1>Another Title</h1>

<!-- ❌ WRONG: Skipping heading levels -->
<h1>Title</h1>
<h4>Subsection</h4>

<!-- ❌ WRONG: Using headings for visual styling -->
<h4>I just want small bold text</h4>

<!-- ❌ WRONG: Empty headings -->
<h2></h2>
<h2><!-- icon here via CSS --></h2>

<!-- ✅ CORRECT: Logical hierarchy -->
<h1>Page Title</h1>
<h2>Section One</h2>
<h3>Subsection 1.1</h3>
<h2>Section Two</h2>
```

### 20.3 Link and Button Anti-Patterns

```html
<!-- ❌ WRONG: Div or span as button -->
<div class="btn" onclick="submit()">Submit</div>
<span class="link" onclick="navigate()">Click here</span>

<!-- ✅ CORRECT: Native elements -->
<button type="button" onclick="submit()">Submit</button>
<a href="/destination">Navigate</a>

<!-- ❌ WRONG: Links without href (as buttons) -->
<a onclick="doSomething()">Do Something</a>

<!-- ✅ CORRECT: Use button for actions, a[href] for navigation -->
<button type="button" onclick="doSomething()">Do Something</button>

<!-- ❌ WRONG: Meaningless link text -->
<a href="/products">Click here</a>
<a href="/report.pdf">Read more</a>
<a href="/">This website</a>

<!-- ✅ CORRECT: Descriptive link text -->
<a href="/products">Browse our product catalog</a>
<a href="/report.pdf">Download Annual Report 2025 (PDF, 2.4 MB)</a>
<a href="/">DevDocs Homepage</a>

<!-- ❌ WRONG: target="_blank" without rel="noopener" -->
<a href="https://example.com" target="_blank">External link</a>

<!-- ✅ CORRECT -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  External site (opens in new tab)
</a>
```

### 20.4 Image Anti-Patterns

```html
<!-- ❌ WRONG: Missing alt attribute -->
<img src="photo.jpg">

<!-- ❌ WRONG: Generic alt text -->
<img src="logo.png" alt="image">
<img src="chart.png" alt="chart">
<img src="photo.jpg" alt="photo of person">

<!-- ❌ WRONG: Redundant "image of" in alt -->
<img src="cat.jpg" alt="image of a cat sitting on a mat">

<!-- ✅ CORRECT: Descriptive alt text -->
<img src="logo.png" alt="DevDocs">
<img src="chart.png" alt="Bar chart: revenue grew from $100k in Q1 to $180k in Q4 2025">
<img src="cat.jpg" alt="Orange tabby cat sitting on a woven mat">

<!-- ❌ WRONG: Alt text for decorative images -->
<img src="divider.png" alt="decorative divider">
<img src="bg.png" alt="background">

<!-- ✅ CORRECT: Empty alt for decorative images -->
<img src="divider.png" alt="">
<img src="bg.png" alt="">

<!-- ❌ WRONG: No width/height on images (causes CLS) -->
<img src="photo.jpg" alt="Team photo">

<!-- ✅ CORRECT: Always specify dimensions -->
<img src="photo.jpg" alt="Team photo" width="800" height="533">
```

### 20.5 Form Anti-Patterns

```html
<!-- ❌ WRONG: Input without label -->
<input type="text" placeholder="Enter your name">

<!-- ❌ WRONG: Placeholder as label -->
<input type="email" placeholder="Email address">

<!-- ✅ CORRECT -->
<label for="name">Full name</label>
<input type="text" id="name" name="name" autocomplete="name">

<!-- ❌ WRONG: Label not associated with input -->
<label>Email</label>
<input type="email" name="email">

<!-- ✅ CORRECT: Explicit association via for/id -->
<label for="email">Email</label>
<input type="email" id="email" name="email">

<!-- ❌ WRONG: Div used as button in form -->
<div class="submit-btn" onclick="document.forms[0].submit()">Submit</div>

<!-- ✅ CORRECT -->
<button type="submit">Submit</button>

<!-- ❌ WRONG: Missing type on button inside form -->
<button>Click Me</button>   <!-- defaults to type="submit"! -->

<!-- ✅ CORRECT: Always specify type -->
<button type="button" onclick="openHelp()">Help</button>
<button type="submit">Submit</button>

<!-- ❌ WRONG: Radio/checkbox without fieldset+legend -->
<label><input type="radio" name="size" value="S"> Small</label>
<label><input type="radio" name="size" value="M"> Medium</label>
<label><input type="radio" name="size" value="L"> Large</label>

<!-- ✅ CORRECT -->
<fieldset>
  <legend>Size</legend>
  <label><input type="radio" name="size" value="S"> Small</label>
  <label><input type="radio" name="size" value="M"> Medium</label>
  <label><input type="radio" name="size" value="L"> Large</label>
</fieldset>
```

### 20.6 Table Anti-Patterns

```html
<!-- ❌ WRONG: Table for layout -->
<table>
  <tr>
    <td><nav><!-- navigation --></nav></td>
    <td><main><!-- content --></main></td>
  </tr>
</table>

<!-- ✅ CORRECT: CSS for layout -->
<div class="layout">
  <nav>...</nav>
  <main>...</main>
</div>

<!-- ❌ WRONG: Table without caption or scope -->
<table>
  <tr>
    <td>Name</td><td>Score</td>
  </tr>
  <tr>
    <td>Alice</td><td>95</td>
  </tr>
</table>

<!-- ✅ CORRECT: Proper table markup -->
<table>
  <caption>Quiz Results</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Alice</th>
      <td>95</td>
    </tr>
  </tbody>
</table>
```

### 20.7 Accessibility Anti-Patterns

```html
<!-- ❌ WRONG: ARIA roles on semantic elements that already have them -->
<button role="button">Submit</button>  <!-- redundant -->
<nav role="navigation">...</nav>       <!-- redundant -->

<!-- ❌ WRONG: aria-hidden on focusable element -->
<a href="/" aria-hidden="true">Home</a>   <!-- invisible to AT but keyboard-focusable -->

<!-- ✅ CORRECT: Remove from tab order if hiding from AT -->
<a href="/" aria-hidden="true" tabindex="-1">Home</a>
<!-- (but why would you hide a real link? reconsider the design) -->

<!-- ❌ WRONG: Only color conveys information -->
<p style="color: red">Error occurred</p>
<p style="color: green">Success!</p>

<!-- ✅ CORRECT: Semantic role + color -->
<p role="alert"><strong>Error:</strong> Something went wrong.</p>
<p role="status"><strong>Success:</strong> Your file was saved.</p>

<!-- ❌ WRONG: Icon with no accessible name -->
<button type="button">
  <svg><!-- search icon --></svg>
</button>

<!-- ✅ CORRECT -->
<button type="button" aria-label="Search">
  <svg aria-hidden="true" focusable="false"><!-- search icon --></svg>
</button>

<!-- ❌ WRONG: Positive tabindex -->
<input type="text" tabindex="3">
<button tabindex="1">First</button>

<!-- ✅ CORRECT: Use DOM order; tabindex="0" if needed -->
<button>First</button>
<input type="text">

<!-- ❌ WRONG: role="presentation" on interactive element -->
<table role="presentation">
  <tr><td><a href="...">...</a></td></tr>  <!-- links inside presentation table lose context -->
</table>
```

### 20.8 Meta and Head Anti-Patterns

```html
<!-- ❌ WRONG: Missing charset declaration -->
<head>
  <title>My Page</title>
</head>

<!-- ❌ WRONG: Charset not first in head -->
<head>
  <title>My Page</title>
  <meta charset="UTF-8">
</head>

<!-- ❌ WRONG: Setting maximum-scale or user-scalable=no -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

<!-- ✅ CORRECT -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- ❌ WRONG: Empty or generic title -->
<title>Page</title>
<title>Home</title>
<title>Untitled</title>

<!-- ✅ CORRECT: Descriptive, unique title -->
<title>Contact Sales Team — DevDocs</title>
```

---

## 21. Validation and Tooling

### 21.1 W3C Nu HTML Checker

**URL:** https://validator.w3.org/nu/

Use it:
- During development after major structural changes
- Before deployment
- In CI/CD pipelines via API

```bash
# CLI validation via curl
curl -H "Content-Type: text/html; charset=utf-8" \
     --data-binary @index.html \
     "https://validator.w3.org/nu/?out=json" | jq '.messages[]'
```

### 21.2 Accessibility Testing Tools

| Tool | Type | URL |
|------|------|-----|
| axe DevTools | Browser extension | deque.com/axe |
| WAVE | Browser extension / online | wave.webaim.org |
| Lighthouse | Chrome DevTools built-in | — |
| IBM Equal Access | Browser extension | ibm.com/able |
| NVDA | Screen reader (Windows) | nvaccess.org |
| VoiceOver | Screen reader (macOS/iOS) | Built-in |
| TalkBack | Screen reader (Android) | Built-in |
| Narrator | Screen reader (Windows) | Built-in |
| JAWS | Screen reader (Windows) | freedomscientific.com |

### 21.3 Browser DevTools Checks

**Accessibility tree inspection:**
- Chrome DevTools → Accessibility panel (Elements pane)
- Firefox DevTools → Accessibility panel
- Safari Web Inspector → Accessibility

**Landmark navigation:**
- Headings map extensions (HeadingsMap for Firefox/Chrome)
- Screen reader landmark navigation

**Color contrast:**
- Chrome DevTools → Rendering → Emulate vision deficiencies
- DevTools color picker shows contrast ratio

### 21.4 HTML Linting

```json
// .htmlhintrc — HTMLHint configuration
{
  "tagname-lowercase": true,
  "attr-lowercase": true,
  "attr-value-double-quotes": true,
  "doctype-first": true,
  "tag-pair": true,
  "spec-char-escape": true,
  "id-unique": true,
  "src-not-empty": true,
  "attr-no-duplication": true,
  "title-require": true,
  "alt-require": true,
  "doctype-html5": true,
  "head-script-disabled": true,
  "id-class-value": "dash",
  "style-disabled": false,
  "inline-script-disabled": false,
  "space-tab-mixed-disabled": "space"
}
```

### 21.5 Automated Testing Integration

```javascript
// Jest + axe-core
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('page has no accessibility violations', async () => {
  document.body.innerHTML = '<main><h1>Hello</h1><p>Content</p></main>';
  const results = await axe(document.body);
  expect(results).toHaveNoViolations();
});

// Playwright + axe
const { checkA11y } = require('axe-playwright');
await checkA11y(page, null, {
  detailedReport: true,
  detailedReportOptions: { html: true }
});
```

### 21.6 HTML Validation in CI/CD

```yaml
# GitHub Actions example
name: HTML Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate HTML
        uses: Cyb3r-Jak3/html5validator-action@v7.2.0
        with:
          target: public/
          css: true
```

---

## 22. Quick-Reference Checklists

### 22.1 Document Structure Checklist

- [ ] `<!DOCTYPE html>` is the first line
- [ ] `<html lang="xx">` has correct BCP 47 language code
- [ ] `<meta charset="UTF-8">` is first element in `<head>`
- [ ] `<meta name="viewport">` present without `user-scalable=no`
- [ ] `<title>` is present, non-empty, and descriptive
- [ ] Exactly one `<main>` element visible on the page
- [ ] Page has a `<header>` and `<footer>` at the top level
- [ ] All page sections use appropriate semantic elements

### 22.2 Headings Checklist

- [ ] Exactly one `<h1>` per page
- [ ] Heading levels are not skipped (no h1 → h3)
- [ ] Headings describe their section content
- [ ] Headings are used for structure, not visual styling
- [ ] Every `<section>` has an associated heading

### 22.3 Links and Navigation Checklist

- [ ] All `<a>` elements have descriptive text
- [ ] No link text is "click here", "read more", or "here"
- [ ] `target="_blank"` links have `rel="noopener noreferrer"`
- [ ] A skip link is the first focusable element in `<body>`
- [ ] All `<nav>` elements have `aria-label` when multiple exist
- [ ] Current page/step indicated with `aria-current`

### 22.4 Images Checklist

- [ ] All `<img>` elements have `alt` attribute (may be empty for decorative)
- [ ] Alt text describes the image's content/purpose, not "image of"
- [ ] Decorative images have `alt=""`
- [ ] All images have `width` and `height` attributes
- [ ] Large images use `loading="lazy"` (below-fold) or `fetchpriority="high"` (hero)
- [ ] Complex images have extended descriptions via `aria-describedby` or `<figcaption>`

### 22.5 Forms Checklist

- [ ] Every `<input>`, `<select>`, `<textarea>` has a `<label>` or `aria-label`
- [ ] Labels are explicitly associated via `for`/`id` or implicit wrapping
- [ ] Radio and checkbox groups use `<fieldset>` + `<legend>`
- [ ] Required fields have `required` attribute and `aria-required="true"`
- [ ] Error messages are associated with fields via `aria-describedby`
- [ ] Error messages use `role="alert"` or `aria-live="polite"`
- [ ] All `<button>` elements have explicit `type` attribute
- [ ] No native interactive elements use ARIA to override their semantics

### 22.6 Tables Checklist

- [ ] All tables have a `<caption>`
- [ ] All `<th>` elements have `scope` attribute
- [ ] Complex tables use `headers` attribute on `<td>`
- [ ] Tables use `<thead>`, `<tbody>`, `<tfoot>` as appropriate
- [ ] No table is used for layout purposes

### 22.7 Accessibility Checklist

- [ ] All interactive elements are keyboard operable
- [ ] Focus indicator is visible (never `outline: none` without alternative)
- [ ] Color alone is not used to convey information
- [ ] All videos have captions (`<track kind="captions">`)
- [ ] All audio content has a text transcript
- [ ] No positive `tabindex` values used
- [ ] ARIA roles not applied to elements that already have equivalent native semantics
- [ ] `aria-hidden="true"` not applied to focusable elements
- [ ] All icon-only buttons have `aria-label`
- [ ] Live regions (`aria-live`) used for dynamic content updates
- [ ] Page validated with automated tool (axe, WAVE, Lighthouse)
- [ ] Page tested with a screen reader

### 22.8 Performance and SEO Checklist

- [ ] `<title>` is unique and descriptive (55–70 chars)
- [ ] `<meta name="description">` is present and meaningful
- [ ] `<link rel="canonical">` points to preferred URL
- [ ] Structured data (JSON-LD) added for appropriate content types
- [ ] Images have correct `srcset` and `sizes` for responsive loading
- [ ] Scripts use `defer` or `async` appropriately
- [ ] No render-blocking resources in `<head>` beyond critical CSS
- [ ] `<link rel="preload">` for critical resources

---

## Appendix A: Element Content Model Quick Reference

| Element | Permitted content | Allowed parents |
|---------|------------------|-----------------|
| `html` | `head` then `body` | Document root |
| `head` | Metadata content | `html` |
| `body` | Flow content | `html` |
| `header` | Flow content (no header/footer) | Flow content parents |
| `footer` | Flow content (no header/footer) | Flow content parents |
| `main` | Flow content | `body`, `div`, `form`, etc. (not inside article/aside/footer/header/nav) |
| `nav` | Flow content | Flow content |
| `article` | Flow content | Flow content |
| `section` | Flow content | Flow content |
| `aside` | Flow content | Flow content |
| `h1`–`h6` | Phrasing content | Flow content |
| `p` | Phrasing content | Flow content |
| `ul` | `li` elements | Flow content |
| `ol` | `li` elements | Flow content |
| `li` | Flow content | `ul`, `ol` |
| `dl` | `dt`, `dd`, `div` | Flow content |
| `dt` | Flow content (no heading/sectioning/footer/header) | `dl` |
| `dd` | Flow content | `dl` |
| `div` | Flow content | Flow content |
| `span` | Phrasing content | Phrasing content |
| `a` | Transparent (no interactive content) | Phrasing content, flow content |
| `em` | Phrasing content | Phrasing content |
| `strong` | Phrasing content | Phrasing content |
| `img` | Empty (void) | Phrasing content |
| `figure` | flow content + optional `figcaption` | Flow content |
| `figcaption` | Flow content | `figure` (first or last child) |
| `table` | caption?, colgroup*, thead?, (tbody+\|tr+), tfoot? | Flow content |
| `tr` | `th`\|`td` elements | `thead`, `tbody`, `tfoot`, `table` |
| `th` | Flow content (no header/footer/sectioning/heading) | `tr` |
| `td` | Flow content | `tr` |
| `form` | Flow content (no nested forms) | Flow content |
| `fieldset` | Optional `legend` then flow content | Flow content |
| `label` | Phrasing content (no nested label) | Phrasing content |
| `input` | Empty (void) | Phrasing content |
| `button` | Phrasing content (no interactive content) | Phrasing content |
| `select` | `option`, `optgroup` | Phrasing content |
| `textarea` | Text | Phrasing content |
| `details` | `summary` then flow content | Flow content |
| `summary` | Phrasing content \| heading | `details` (first child) |
| `dialog` | Flow content | Flow content |
| `video` | source*, track*, flow content (no video/audio) | Flow content |
| `audio` | source*, track*, flow content (no video/audio) | Flow content |
| `source` | Empty (void) | `video`, `audio`, `picture` |
| `track` | Empty (void) | `video`, `audio` |
| `picture` | source*, `img` | Phrasing content |
| `iframe` | Text (fallback) | Phrasing/flow content |
| `canvas` | Transparent | Phrasing/flow content |
| `script` | Script | Metadata, phrasing, flow |
| `noscript` | When in head: link/style/meta; in body: transparent | Metadata, phrasing, flow |
| `template` | Any | Metadata, phrasing, flow, script-supporting |

---

## Appendix B: Void Elements (No Closing Tag)

```html
<area>
<base>
<br>
<col>
<embed>
<hr>
<img>
<input>
<link>
<meta>
<source>
<track>
<wbr>
```

**Rules:**
- Never use `/>` self-closing syntax in HTML5 (valid in SVG/MathML only)
- `<br />`, `<img />` are technically valid but unnecessary; prefer `<br>`, `<img>`
- Never write `</br>`, `</img>`, etc.

---

## Appendix C: Character Entity Reference

| Character | Entity | Numeric | Use case |
|-----------|--------|---------|---------|
| `&` | `&amp;` | `&#38;` | Ampersand in text |
| `<` | `&lt;` | `&#60;` | Less-than in text |
| `>` | `&gt;` | `&#62;` | Greater-than in text |
| `"` | `&quot;` | `&#34;` | Quote in attributes |
| `'` | `&apos;` | `&#39;` | Apostrophe in attributes |
| ` ` | `&nbsp;` | `&#160;` | Non-breaking space |
| `©` | `&copy;` | `&#169;` | Copyright |
| `®` | `&reg;` | `&#174;` | Registered trademark |
| `™` | `&trade;` | `&#8482;` | Trademark |
| `—` | `&mdash;` | `&#8212;` | Em dash |
| `–` | `&ndash;` | `&#8211;` | En dash |
| `…` | `&hellip;` | `&#8230;` | Ellipsis |
| `"` | `&ldquo;` | `&#8220;` | Left double quote |
| `"` | `&rdquo;` | `&#8221;` | Right double quote |
| `'` | `&lsquo;` | `&#8216;` | Left single quote |
| `'` | `&rsquo;` | `&#8217;` | Right single quote |
| `→` | `&rarr;` | `&#8594;` | Right arrow |
| `←` | `&larr;` | `&#8592;` | Left arrow |
| `↑` | `&uarr;` | `&#8593;` | Up arrow |
| `↓` | `&darr;` | `&#8595;` | Down arrow |
| `★` | `&star;` | `&#9733;` | Star (filled) |
| `☆` | — | `&#9734;` | Star (outline) |

---

## Appendix D: Deprecated Elements and Attributes

**Never use these in HTML5:**

| Deprecated Element | Use instead |
|--------------------|------------|
| `<font>` | CSS `font-*` properties |
| `<center>` | CSS `text-align: center` |
| `<big>` | CSS `font-size` |
| `<strike>`, `<s>` (old) | `<s>` (new semantic) or CSS |
| `<tt>` | `<code>` or `<kbd>` or `<samp>` |
| `<frame>`, `<frameset>`, `<noframes>` | No equivalent — redesign |
| `<applet>` | `<object>` or modern APIs |
| `<basefont>` | CSS |
| `<blink>` | CSS animation (use sparingly) |
| `<marquee>` | CSS animation |
| `<isindex>` | `<input type="search">` |
| `<listing>` | `<pre><code>` |
| `<plaintext>` | Encode content, use `<pre>` |
| `<xmp>` | `<pre><code>` |

**Deprecated attributes (do not use):**

| Element | Attribute | Use instead |
|---------|-----------|------------|
| `<body>` | `bgcolor`, `text`, `link`, `vlink`, `alink` | CSS |
| `<table>` | `border`, `cellpadding`, `cellspacing`, `bgcolor`, `width` | CSS |
| `<tr>`, `<td>`, `<th>` | `bgcolor`, `valign`, `align`, `nowrap` | CSS |
| `<img>` | `border`, `hspace`, `vspace`, `align` | CSS |
| `<a>` | `name` | `id` on any element |
| `<hr>` | `size`, `width`, `color`, `noshade` | CSS |
| `<ol>` | `type` | CSS `list-style-type` (or `type` for semantic meaning) |
| `<ul>` | `type` | CSS `list-style-type` |
| `<input>` | `size` (for most types) | CSS `width` |
| All elements | `style="..."` (overuse) | External CSS class |

---

*This document conforms to the HTML Living Standard (WHATWG), W3C HTML 5.3, WCAG 2.2, WAI-ARIA 1.2, and BCP 47. Last reviewed: June 2025.*

*Validate your HTML: https://validator.w3.org/nu/*
*WCAG Quick Reference: https://www.w3.org/WAI/WCAG22/quickref/*
*HTML Living Standard: https://html.spec.whatwg.org/*
