# SEO HTML Guide
## A Complete Reference for AI-Assisted Page Refactoring

> **One rule**: every HTML decision either helps, hurts, or is neutral to search engine understanding.
> Know which category you're in before touching anything.
> This guide covers what to do, what not to do, and what is acceptable but optional.

---

## Table of Contents

1. [Decision Tree](#1-decision-tree)
2. [Document Structure](#2-document-structure)
3. [Title Tag](#3-title-tag)
4. [Meta Description](#4-meta-description)
5. [Heading Hierarchy](#5-heading-hierarchy)
6. [Semantic HTML Elements](#6-semantic-html-elements)
7. [Images](#7-images)
8. [Links](#8-links)
9. [Structured Data — Schema.org](#9-structured-data--schemaorg)
10. [Open Graph & Social Meta](#10-open-graph--social-meta)
11. [Canonical & Indexing Control](#11-canonical--indexing-control)
12. [Performance Signals](#12-performance-signals)
13. [Accessibility as SEO](#13-accessibility-as-seo)
14. [Mobile & Viewport](#14-mobile--viewport)
15. [URL Structure](#15-url-structure)
16. [What Stays As-Is](#16-what-stays-as-is)
17. [Anti-Patterns — Never Do These](#17-anti-patterns--never-do-these)
18. [Replacement Table](#18-replacement-table)
19. [Final Checklist](#19-final-checklist)

---

## 1. Decision Tree

Run every HTML element and attribute through this filter before touching anything.

```
There is an HTML element or attribute
              │
              ▼
Does it communicate meaning, structure, or content to search engines?
    YES ──► Evaluate correctness — fix if wrong, keep if right
              │
             NO
              ▼
Is it a visual/presentational concern only?
    YES ──► Leave it alone — SEO is not affected
              │
             NO
              ▼
Is it missing but required for crawlability or indexing?
    YES ──► ADD it
              │
             NO
              ▼
Is it present but actively harmful (duplicate, misleading, blocked)?
    YES ──► KILL or FIX it
              │
             NO
              ▼
    LEAVE AS-IS
```

**Five outcomes:** FIX / ADD / KILL / LEAVE / SLIM (keep the signal, remove the noise).

---

## 2. Document Structure

### Required skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title — Site Name</title>
    <meta name="description" content="150–160 character description.">
    <link rel="canonical" href="https://example.com/page/">
</head>
<body>
    <header>...</header>
    <main>...</main>
    <footer>...</footer>
</body>
</html>
```

### Rules

| Element | Rule |
|---|---|
| `<!DOCTYPE html>` | Must be the very first line. No exceptions. |
| `<html lang="en">` | `lang` attribute is required. Use the correct BCP 47 language code. |
| `<meta charset="utf-8">` | Must be within the first 1024 bytes of the document. |
| `<head>` | Title and canonical must appear here — not in `<body>`. |
| `<main>` | One per page. Wraps the primary content Google indexes. |

### ❌ Wrong

```html
<!DOCTYPE html>
<html>  <!-- no lang -->
<head>
    <title>Page</title>
    <!-- no charset, no viewport, no canonical -->
</head>
<body>
    <div id="main">...</div>  <!-- div instead of <main> -->
</body>
```

### ✅ Correct

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Running Shoes for Men — ShoeStore</title>
    <meta name="description" content="Shop men's running shoes. Free shipping on orders over $50.">
    <link rel="canonical" href="https://shoestore.com/mens-running-shoes/">
</head>
<body>
    <header>...</header>
    <main>...</main>
    <footer>...</footer>
</body>
```

---

## 3. Title Tag

The single most important on-page SEO element. Google uses it as the primary signal for page topic.

### Rules

- **Length:** 50–60 characters. Google truncates at ~600px display width (roughly 60 chars).
- **Format:** `Primary Keyword — Secondary Keyword | Brand` or `Topic: Subtopic — Brand`
- **One per page.** Multiple `<title>` tags: the last one wins — this is a bug.
- **Unique per page.** Duplicate titles across pages = duplicate content signal.
- **No keyword stuffing.** `Shoes Shoes Buy Shoes Cheap Shoes` is penalised.
- **Front-load the keyword.** The first words carry the most weight.

### ❌ Wrong

```html
<!-- Too long — gets truncated, loses brand -->
<title>Buy The Best Running Shoes For Men Online With Free Shipping And Great Deals At ShoeStore</title>

<!-- Too generic — tells Google nothing specific -->
<title>Home</title>
<title>Products</title>
<title>Page 1</title>

<!-- Keyword stuffed -->
<title>Running Shoes Running Shoes Buy Running Shoes Men Running Shoes</title>

<!-- Missing brand -->
<title>Running Shoes</title>

<!-- Duplicate across pages -->
<title>ShoeStore — Products</title>  <!-- on every product page -->
```

### ✅ Correct

```html
<!-- Product page -->
<title>Nike Air Zoom Pegasus 40 — Men's Running — ShoeStore</title>

<!-- Category page -->
<title>Men's Running Shoes — Free Shipping — ShoeStore</title>

<!-- Homepage -->
<title>ShoeStore — Running & Training Shoes for Men and Women</title>

<!-- Blog post -->
<title>How to Choose Running Shoes: 7 Expert Tips — ShoeStore Blog</title>
```

### Acceptable (not ideal, but not harmful)

```html
<!-- Slightly over 60 chars — Google may rewrite but won't penalise -->
<title>Men's Trail Running Shoes — Waterproof & Lightweight — ShoeStore</title>

<!-- Brand first (common for well-known brands) -->
<title>ShoeStore | Men's Running Shoes</title>
```

---

## 4. Meta Description

Not a direct ranking factor, but controls the snippet in search results — directly affects click-through rate (CTR), which is an indirect ranking signal.

### Rules

- **Length:** 150–160 characters. Google truncates longer descriptions.
- **One per page.** Duplicate: the last one wins.
- **Unique per page.** Identical descriptions across pages = wasted opportunity.
- **Contains a CTA.** "Shop now", "Learn more", "Get free shipping".
- **Includes the primary keyword** — Google bolds matched terms in the snippet.
- **Describes what the page delivers** — not just what the site is.

### ❌ Wrong

```html
<!-- Too short — wastes snippet space -->
<meta name="description" content="Buy shoes online.">

<!-- Too long — gets truncated mid-sentence -->
<meta name="description" content="We sell the best running shoes for men and women with a huge selection of brands including Nike, Adidas, New Balance, Brooks, ASICS, Saucony and many more at great prices with free shipping on all orders.">

<!-- Generic — identical on every page -->
<meta name="description" content="ShoeStore — Your online shoe destination.">

<!-- Missing — Google generates one from page content (often bad) -->
<!-- <meta name="description" ...> -->
```

### ✅ Correct

```html
<!-- Product page -->
<meta name="description" content="Nike Air Zoom Pegasus 40 for men. Responsive cushioning, breathable mesh upper. Free shipping & 30-day returns. Shop now at ShoeStore.">

<!-- Category page -->
<meta name="description" content="Shop 200+ men's running shoes from Nike, Adidas, Brooks & more. Free shipping on orders over $50. Filter by distance, terrain, and width.">

<!-- Blog post -->
<meta name="description" content="Choosing the wrong running shoe causes injury. Our expert guide covers arch support, drop, cushioning, and fit — with recommendations for every runner type.">
```

---

## 5. Heading Hierarchy

Headings are the outline of the page. Google uses them to understand topic structure and extract featured snippets.

### Rules

- **One `<h1>` per page.** It defines the page topic. Multiple `<h1>` tags dilute the signal.
- **`<h1>` must match (or closely relate to) the `<title>`.** Different topics = confusing signal.
- **Hierarchy is sequential.** `<h1>` → `<h2>` → `<h3>`. Never skip levels (e.g. `<h1>` → `<h3>`).
- **Headings describe sections, not style.** Never use `<h2>` just to make text bigger.
- **Keywords in headings carry weight.** Include natural variations of the target keyword.
- **Every page needs at least one heading.** A page with no headings has no structure signal.

### ❌ Wrong

```html
<!-- Two h1 tags -->
<h1>Men's Running Shoes</h1>
...
<h1>Featured Products</h1>

<!-- Skipped level -->
<h1>Men's Running Shoes</h1>
<h3>Nike Collection</h3>  <!-- h2 was skipped -->

<!-- Heading used for visual styling only -->
<h2 style="font-size: 12px; color: gray;">Filter by size</h2>

<!-- No heading on the page at all -->
<div class="big-text">Men's Running Shoes</div>

<!-- h1 disconnected from title -->
<title>Nike Running Shoes — ShoeStore</title>
...
<h1>Welcome to our store</h1>
```

### ✅ Correct

```html
<h1>Men's Running Shoes</h1>          <!-- page topic — matches title -->

<h2>Road Running</h2>                 <!-- major section -->
    <h3>Neutral Shoes</h3>            <!-- subsection -->
    <h3>Stability Shoes</h3>

<h2>Trail Running</h2>
    <h3>Waterproof Options</h3>
    <h3>Minimalist Trail Shoes</h3>

<h2>How to Choose Running Shoes</h2>  <!-- informational section -->
    <h3>Understanding Pronation</h3>
    <h3>Matching Shoes to Terrain</h3>
```

### Acceptable

```html
<!-- h1 slightly broader than title — OK if semantically related -->
<title>Nike Pegasus 40 Review — ShoeStore</title>
<h1>Nike Air Zoom Pegasus 40: Full Review</h1>

<!-- Decorative elements styled to look like headings — OK if using CSS, not heading tags -->
<p class="section-label">Filter by brand</p>  <!-- not a heading, just styled text -->
```

---

## 6. Semantic HTML Elements

Semantic elements tell crawlers what kind of content is in each section, without relying on class names or IDs which Google ignores for structure.

### Core semantic elements

| Element | Use when | Never use for |
|---|---|---|
| `<header>` | Site header or section header | Decorative top banners |
| `<nav>` | Navigation menus | Any list of links |
| `<main>` | Primary page content | Sidebars, repeated elements |
| `<article>` | Self-contained content (post, card, product) | Layout containers |
| `<section>` | Thematic grouping with a heading | Generic layout divisions |
| `<aside>` | Tangentially related content (sidebar, related posts) | Main content |
| `<footer>` | Site footer or section footer | Any bottom element |
| `<figure>` + `<figcaption>` | Images with captions | Images without captions |
| `<time datetime="...">` | Dates and times | Decorative timeline visuals |
| `<address>` | Contact information for the nearest `<article>` or `<body>` | Postal addresses in content |
| `<mark>` | Highlighted/relevant text | General emphasis |
| `<abbr title="...">` | Abbreviations with expansions | Tooltips |

### ❌ Wrong

```html
<!-- Div soup — Google sees flat content with no structure -->
<div class="header">
    <div class="nav">...</div>
</div>
<div class="content">
    <div class="article">
        <div class="title">...</div>
    </div>
</div>
<div class="footer">...</div>

<!-- section without a heading -->
<section>
    <p>Some content without a heading</p>
</section>

<!-- article for a layout box -->
<article class="sidebar-widget">Latest tweets</article>

<!-- nav wrapping every list -->
<nav>
    <ul>
        <li>Item 1</li>  <!-- this is not navigation -->
    </ul>
</nav>
```

### ✅ Correct

```html
<header>
    <nav aria-label="Main navigation">
        <ul>...</ul>
    </nav>
</header>

<main>
    <article itemscope itemtype="https://schema.org/Product">
        <h1 itemprop="name">Nike Pegasus 40</h1>
        <section>
            <h2>Product Details</h2>
            <p itemprop="description">...</p>
        </section>
        <section>
            <h2>Customer Reviews</h2>
            ...
        </section>
    </article>

    <aside>
        <h2>Related Products</h2>
        ...
    </aside>
</main>

<footer>
    <address>
        123 Main St, New York, NY 10001
    </address>
</footer>
```

---

## 7. Images

Images are crawled, indexed, and returned in Google Image Search. Every image is an SEO opportunity — or a missed one.

### Rules

#### `alt` attribute

- **Required on every `<img>`.** Missing `alt` = accessibility violation + missed keyword opportunity.
- **Describes the image content** — not the page topic, not keyword spam.
- **Decorative images:** `alt=""` (empty string). This tells screen readers and crawlers to skip it.
- **Max ~125 characters.** Longer text gets cut off by assistive technologies.
- **No "image of..." or "photo of..." prefix** — Google already knows it's an image.

#### File names

- **Descriptive, hyphenated.** `nike-pegasus-40-mens-running-shoe.jpg` not `IMG_4829.jpg`.
- **Lowercase.** Servers are case-sensitive; URLs with `Image.jpg` and `image.jpg` can be two different files.
- **No spaces.** Spaces become `%20` in URLs — ugly and fragile.

#### `loading` attribute

- **`loading="lazy"`** on all images below the fold. Improves Core Web Vitals (LCP, FID).
- **`loading="eager"` or omit** on the first visible image (hero, product image above fold).
- **`fetchpriority="high"`** on the single most important image (LCP element).

#### Dimensions

- **Always specify `width` and `height`.** Prevents Cumulative Layout Shift (CLS) — a Core Web Vitals metric that directly affects ranking.

#### Format

- **WebP or AVIF** preferred. Smaller file size = faster load = better Core Web Vitals.
- **JPEG** for photos when WebP/AVIF unavailable.
- **PNG** for images requiring transparency.
- **SVG** for icons and logos — infinitely scalable, no quality loss.

### ❌ Wrong

```html
<!-- Missing alt entirely -->
<img src="shoe.jpg">

<!-- Keyword stuffed alt -->
<img src="shoe.jpg" alt="running shoes buy cheap running shoes men running shoes nike">

<!-- "image of" prefix -->
<img src="shoe.jpg" alt="Image of a running shoe">

<!-- Non-descriptive file name -->
<img src="IMG_4829.jpg" alt="Running shoe">

<!-- Missing dimensions — causes layout shift -->
<img src="shoe.jpg" alt="Nike Pegasus 40">

<!-- lazy loading on the hero image -->
<img src="hero.jpg" alt="Men's running shoes" loading="lazy">

<!-- eager loading on everything -->
<img src="product-4.jpg" alt="..." loading="eager">
<img src="product-5.jpg" alt="..." loading="eager">
```

### ✅ Correct

```html
<!-- Hero / LCP image -->
<img
    src="nike-pegasus-40-mens-blue.webp"
    alt="Nike Air Zoom Pegasus 40 in blue, men's size"
    width="800"
    height="800"
    fetchpriority="high"
    loading="eager">

<!-- Below-fold product images -->
<img
    src="nike-react-infinity-mens-white.webp"
    alt="Nike React Infinity Run Flyknit 3 in white"
    width="400"
    height="400"
    loading="lazy">

<!-- Decorative image — skip in accessibility tree -->
<img src="divider-wave.svg" alt="" width="1440" height="60" loading="lazy">

<!-- Icon inside a button — alt describes the action, not the icon -->
<button>
    <img src="cart-icon.svg" alt="Add to cart" width="24" height="24">
</button>
```

### Acceptable

```html
<!-- JPEG when WebP not available — not ideal, not harmful -->
<img src="product.jpg" alt="Nike Pegasus 40" width="400" height="400" loading="lazy">

<!-- Omitting fetchpriority on LCP image — Google can usually identify it -->
<img src="hero.webp" alt="Men's running shoes sale" width="1200" height="600" loading="eager">
```

---

## 8. Links

Links are how PageRank flows between pages. Every link is a vote of relevance.

### Rules

#### `href`

- **Never use `href="#"` for real links.** It creates a non-functional link that goes nowhere.
- **Absolute URLs for external links.** Relative URLs for internal links.
- **No JavaScript-only navigation** (`onclick`, `href="javascript:void(0)"`). Crawlers cannot follow them.

#### Anchor text

- **Descriptive, keyword-relevant.** "men's running shoes" not "click here" or "read more".
- **Unique per destination.** Same destination = same or similar anchor text.
- **Avoid generic anchors:** "here", "click here", "more", "read more", "link", "this page".

#### `rel` attribute

- **`rel="nofollow"`** — tells Google not to pass PageRank. Use on paid links, UGC, untrusted links.
- **`rel="sponsored"`** — for paid/affiliate links. Required by Google guidelines.
- **`rel="ugc"`** — for user-generated content (comments, forum posts).
- **`rel="noopener noreferrer"`** — security attribute for `target="_blank"` links. Not an SEO signal.
- **Never use `rel="nofollow"` on internal links** — it wastes crawl budget and blocks PageRank flow.

#### `target`

- **`target="_blank"`** on external links is acceptable but not required for SEO.
- Always pair with `rel="noopener noreferrer"` for security.

#### Link depth

- **Important pages must be reachable in ≤3 clicks from the homepage.** Deeper = harder to crawl.

### ❌ Wrong

```html
<!-- Non-functional anchor — crawlers stop here -->
<a href="#">View product</a>
<a href="javascript:void(0)">View product</a>

<!-- Generic anchor text — no keyword signal -->
<a href="/mens-running-shoes">Click here</a>
<a href="/blog/how-to-choose">Read more</a>

<!-- nofollow on internal link — wastes PageRank -->
<a href="/category/running" rel="nofollow">Running Shoes</a>

<!-- Missing rel on paid link — Google guideline violation -->
<a href="https://affiliate.example.com/product">Buy on Amazon</a>

<!-- Keyword stuffed anchor -->
<a href="/shoes">cheap shoes buy shoes online shoes discount</a>
```

### ✅ Correct

```html
<!-- Internal link — descriptive anchor, no rel needed -->
<a href="/mens-running-shoes/">Men's Running Shoes</a>

<!-- External link — noopener for security -->
<a href="https://nike.com" target="_blank" rel="noopener noreferrer">Nike Official</a>

<!-- Affiliate/paid link — sponsored required -->
<a href="https://amazon.com/product/..." rel="sponsored noopener" target="_blank">
    Buy on Amazon
</a>

<!-- UGC link in comments -->
<a href="https://usersite.com" rel="ugc nofollow">User's website</a>

<!-- Image link — alt text serves as anchor text -->
<a href="/nike-pegasus-40/">
    <img src="pegasus-40.webp" alt="Nike Air Zoom Pegasus 40" width="400" height="400" loading="lazy">
</a>
```

### Acceptable

```html
<!-- "Learn more" anchor — not ideal but not penalised if used sparingly -->
<a href="/return-policy/">Learn more about returns</a>

<!-- target="_blank" on internal links — unusual but not an SEO issue -->
<a href="/size-guide/" target="_blank" rel="noopener">Size guide (opens in new tab)</a>
```

---

## 9. Structured Data — Schema.org

Structured data is machine-readable markup that tells Google exactly what type of content exists on the page. It enables rich results (star ratings, prices, breadcrumbs, FAQs) in search — directly increasing CTR.

### Two formats: Microdata vs JSON-LD

**JSON-LD** (Google's preferred format) — placed in `<script>` in `<head>` or `<body>`.
**Microdata** — embedded directly in HTML via `itemscope`/`itemprop` attributes.

Both are valid. JSON-LD is easier to maintain. Microdata is tightly coupled to HTML structure but has less maintenance overhead when content is already in the DOM.

### Key schema types

#### Product

```html
<!-- JSON-LD (recommended) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Nike Air Zoom Pegasus 40",
  "description": "Responsive cushioning for everyday running.",
  "image": "https://example.com/images/pegasus-40.webp",
  "brand": {
    "@type": "Brand",
    "name": "Nike"
  },
  "offers": {
    "@type": "Offer",
    "price": "130.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://shoestore.com/nike-pegasus-40/"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "128",
    "bestRating": "5"
  }
}
</script>

<!-- Microdata (alternative — same data in HTML attributes) -->
<article itemscope itemtype="https://schema.org/Product">
    <h1 itemprop="name">Nike Air Zoom Pegasus 40</h1>
    <img itemprop="image" src="pegasus-40.webp" alt="Nike Pegasus 40" width="800" height="800">
    <p itemprop="description">Responsive cushioning for everyday running.</p>

    <div itemprop="offers" itemscope itemtype="https://schema.org/Offer">
        <link itemprop="availability" href="https://schema.org/InStock">
        <span itemprop="price" content="130.00">$130</span>
        <span itemprop="priceCurrency" content="USD">USD</span>
    </div>

    <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating"
         aria-label="Rating: 4.5 out of 5">
        <meta itemprop="ratingValue" content="4.5">
        <meta itemprop="bestRating" content="5">
        <meta itemprop="reviewCount" content="128">
    </div>
</article>
```

#### BreadcrumbList

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://shoestore.com/" },
    { "@type": "ListItem", "position": 2, "name": "Running", "item": "https://shoestore.com/running/" },
    { "@type": "ListItem", "position": 3, "name": "Men's", "item": "https://shoestore.com/running/mens/" },
    { "@type": "ListItem", "position": 4, "name": "Nike Pegasus 40" }
  ]
}
</script>

<!-- HTML breadcrumb — must match the JSON-LD data -->
<nav aria-label="Breadcrumb">
    <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/running/">Running</a></li>
        <li><a href="/running/mens/">Men's</a></li>
        <li aria-current="page">Nike Pegasus 40</li>
    </ol>
</nav>
```

#### FAQPage

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the drop height of the Nike Pegasus 40?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The Nike Pegasus 40 has a 10mm heel-to-toe drop."
      }
    },
    {
      "@type": "Question",
      "name": "Is the Pegasus 40 good for wide feet?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, the Pegasus 40 is available in wide (2E) sizing for men."
      }
    }
  ]
}
</script>
```

#### Article / BlogPosting

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "How to Choose Running Shoes: 7 Expert Tips",
  "datePublished": "2024-03-15",
  "dateModified": "2024-11-20",
  "author": {
    "@type": "Person",
    "name": "Jane Smith"
  },
  "publisher": {
    "@type": "Organization",
    "name": "ShoeStore",
    "logo": {
      "@type": "ImageObject",
      "url": "https://shoestore.com/logo.png"
    }
  },
  "image": "https://shoestore.com/blog/how-to-choose-running-shoes.webp",
  "description": "Expert guide to choosing the right running shoe for your gait, terrain, and distance."
}
</script>
```

#### Organization / WebSite (homepage only)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "ShoeStore",
  "url": "https://shoestore.com/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://shoestore.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
</script>
```

### Rules

- **Structured data must match visible page content.** Do not mark up content that does not appear on the page — Google treats this as spam.
- **Do not mark up entire pages as a single Product if there are multiple products** — use `ItemList`.
- **Validate with Google's Rich Results Test** before deploying.
- **Do not use deprecated types.** `DataFeedItem` and `Product` rich results have specific requirements — check Google Search Central docs.

### ❌ Wrong

```html
<!-- Rating markup with no visible rating on the page -->
<meta itemprop="ratingValue" content="5">  <!-- but no stars shown to users -->

<!-- Fake reviews — never do this -->
<meta itemprop="reviewCount" content="1500">  <!-- but only 3 real reviews exist -->

<!-- Wrong type for the content -->
<!-- Page shows multiple products but marked as single Product -->
<div itemscope itemtype="https://schema.org/Product">
    <!-- contains a grid of 20 different products -->
</div>

<!-- JSON-LD data that doesn't match the HTML -->
<!-- JSON-LD says price is $99, HTML shows $149 -->
```

---

## 10. Open Graph & Social Meta

Open Graph controls how pages appear when shared on Facebook, LinkedIn, Twitter/X, Slack, iMessage, etc. Not a direct ranking factor, but affects CTR from social traffic.

### Required tags

```html
<head>
    <!-- Open Graph -->
    <meta property="og:title" content="Nike Pegasus 40 — Men's Running Shoes — ShoeStore">
    <meta property="og:description" content="Responsive cushioning for everyday running. Free shipping. Shop now.">
    <meta property="og:image" content="https://shoestore.com/og/pegasus-40.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:url" content="https://shoestore.com/nike-pegasus-40/">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="ShoeStore">

    <!-- Twitter/X Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Nike Pegasus 40 — Men's Running Shoes">
    <meta name="twitter:description" content="Responsive cushioning for everyday running. Free shipping.">
    <meta name="twitter:image" content="https://shoestore.com/og/pegasus-40.jpg">
    <meta name="twitter:site" content="@ShoeStore">
</head>
```

### OG image rules

- **Dimensions:** 1200×630px minimum. This is the standard social share card size.
- **Aspect ratio:** 1.91:1 (landscape). Square images are clipped on most platforms.
- **File size:** Under 1MB. Under 300KB is ideal.
- **Format:** JPEG or PNG. WebP has inconsistent support on older scrapers.
- **No text near edges** — platforms crop differently. Keep critical text in the center 80%.
- **Must be an absolute URL** — relative URLs break social scrapers.

### `og:type` values

| Page type | `og:type` value |
|---|---|
| Homepage / generic | `website` |
| Product page | `product` |
| Blog post / article | `article` |
| Video page | `video.movie` or `video.episode` |
| Profile / person | `profile` |

### ❌ Wrong

```html
<!-- Relative image URL — breaks every social scraper -->
<meta property="og:image" content="/images/product.jpg">

<!-- No dimensions — causes "invalid image" warnings -->
<meta property="og:image" content="https://example.com/og.jpg">

<!-- og:title same as page title but truncated — wasted chars -->
<meta property="og:title" content="Nike Air Zoom Pegasus 40 Men's Running Shoes ShoeStore Free Shipping Returns">

<!-- Missing og:url — canonical URL not communicated to social -->
<!-- Missing og:type — defaults to "website" even on product pages -->
```

### ✅ Correct

```html
<meta property="og:title" content="Nike Pegasus 40 — Free Shipping — ShoeStore">
<meta property="og:description" content="The everyday trainer with responsive cushioning. Shop men's and women's versions. Free shipping on all orders.">
<meta property="og:image" content="https://shoestore.com/og/pegasus-40-1200x630.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Nike Air Zoom Pegasus 40 running shoe in blue">
<meta property="og:url" content="https://shoestore.com/nike-pegasus-40/">
<meta property="og:type" content="product">
<meta property="og:site_name" content="ShoeStore">
```

---

## 11. Canonical & Indexing Control

Canonical tags and indexing directives tell Google which pages to index and which to treat as the "master" version.

### Canonical tag

```html
<!-- Every indexable page must have a canonical pointing to itself -->
<link rel="canonical" href="https://shoestore.com/nike-pegasus-40/">
```

**When canonical matters most:**

- Pages accessible via multiple URLs (`?sort=price`, `?ref=email`)
- HTTP and HTTPS versions of the same page
- WWW and non-WWW versions
- Paginated content (`/page/2/`, `/page/3/`)
- Product variants (`/shoes/red/`, `/shoes/blue/` — if content is nearly identical)

### ❌ Wrong

```html
<!-- Relative canonical — fragile, use absolute -->
<link rel="canonical" href="/nike-pegasus-40/">

<!-- Canonical pointing to a different page without reason -->
<!-- Page is /mens-shoes/nike-pegasus-40/ but canonical says /womens-shoes/nike-pegasus-40/ -->

<!-- Missing canonical on paginated pages — Google may choose wrong page -->
<!-- /category/running/page/2/ — no canonical -->

<!-- Self-referencing canonical on a page with noindex — contradicts itself -->
<link rel="canonical" href="https://shoestore.com/page/">
<meta name="robots" content="noindex">
```

### Robots meta tag

```html
<!-- Index this page and follow all links (default — no need to add explicitly) -->
<meta name="robots" content="index, follow">

<!-- Do not index, but follow links (e.g. thank-you pages, admin pages) -->
<meta name="robots" content="noindex, follow">

<!-- Index but do not follow links (rare — use carefully) -->
<meta name="robots" content="index, nofollow">

<!-- Do not index, do not follow (staging, private pages) -->
<meta name="robots" content="noindex, nofollow">

<!-- Prevent Google from showing a cached version -->
<meta name="robots" content="index, follow, noarchive">

<!-- Prevent snippet in search results -->
<meta name="robots" content="index, follow, nosnippet">
```

### hreflang (multilingual sites)

```html
<!-- In <head> of each language version -->
<link rel="alternate" hreflang="en" href="https://shoestore.com/en/shoes/">
<link rel="alternate" hreflang="de" href="https://shoestore.com/de/schuhe/">
<link rel="alternate" hreflang="fr" href="https://shoestore.com/fr/chaussures/">
<link rel="alternate" hreflang="x-default" href="https://shoestore.com/shoes/">
```

**Rules:**
- `hreflang` is bidirectional. If page A links to page B, page B must link back to page A.
- `x-default` is the fallback for users in regions not explicitly listed.
- Use language + region codes: `en-US`, `en-GB`, `pt-BR`, `pt-PT`.

### Pagination

```html
<!-- Paginated series — use canonical on each page pointing to itself, not page 1 -->
<!-- /category/running/        → canonical: /category/running/ -->
<!-- /category/running/page/2/ → canonical: /category/running/page/2/ -->

<!-- Google dropped rel="prev"/"next" support in 2019 — do not use -->
<!-- ❌ Outdated: -->
<link rel="prev" href="/category/running/">
<link rel="next" href="/category/running/page/3/">
```

---

## 12. Performance Signals

Core Web Vitals are direct Google ranking factors. They are measured by Chrome user data in the field.

### The three metrics

| Metric | What it measures | Good threshold |
|---|---|---|
| **LCP** (Largest Contentful Paint) | Load time of the largest visible element | < 2.5s |
| **INP** (Interaction to Next Paint) | Responsiveness to user interaction | < 200ms |
| **CLS** (Cumulative Layout Shift) | Visual stability — unexpected layout shifts | < 0.1 |

### HTML-level optimizations

#### LCP

```html
<!-- Preload the LCP image — tells browser to fetch it immediately -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">

<!-- fetchpriority="high" on the LCP image element itself -->
<img src="hero.webp" alt="Men's running shoes" width="1200" height="600"
     loading="eager" fetchpriority="high">

<!-- Preconnect to third-party font servers -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

#### CLS

```html
<!-- Always specify width and height — browser reserves space before image loads -->
<img src="product.webp" alt="Product" width="400" height="400" loading="lazy">

<!-- For responsive images — use aspect-ratio in CSS -->
<style>
img { aspect-ratio: attr(width) / attr(height); }
</style>

<!-- Font loading — prevent FOUT/FOIT causing CLS -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
```

#### Resource hints

```html
<head>
    <!-- Preconnect: establish connection early for critical third parties -->
    <link rel="preconnect" href="https://fonts.googleapis.com">

    <!-- DNS-prefetch: lighter version for non-critical third parties -->
    <link rel="dns-prefetch" href="https://analytics.google.com">

    <!-- Preload: fetch critical resources immediately -->
    <link rel="preload" as="style" href="critical.css">
    <link rel="preload" as="image" href="hero.webp" fetchpriority="high">
    <link rel="preload" as="font" href="nunito-sans.woff2" type="font/woff2" crossorigin>

    <!-- Prefetch: fetch resources likely needed on the next page -->
    <link rel="prefetch" href="/product-detail.js">
</head>
```

### ❌ Wrong

```html
<!-- No dimensions — causes CLS -->
<img src="product.jpg" alt="Product">

<!-- lazy loading on hero image — delays LCP -->
<img src="hero.jpg" alt="Hero" loading="lazy">

<!-- Blocking render: CSS loaded without preload -->
<link rel="stylesheet" href="large-unused-styles.css">

<!-- Render-blocking script in <head> without defer/async -->
<script src="analytics.js"></script>

<!-- Too many preloads — defeats the purpose -->
<link rel="preload" as="image" href="product-1.jpg">
<link rel="preload" as="image" href="product-2.jpg">
<link rel="preload" as="image" href="product-3.jpg">
<!-- only the LCP image should be preloaded -->
```

### ✅ Correct

```html
<head>
    <!-- 1. Preconnect to font CDN -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <!-- 2. Preload the LCP image -->
    <link rel="preload" as="image" href="hero.webp" fetchpriority="high">

    <!-- 3. Non-critical CSS: load async -->
    <link rel="stylesheet" href="non-critical.css" media="print" onload="this.media='all'">
</head>

<body>
    <!-- LCP image: no lazy loading, high priority -->
    <img src="hero.webp" alt="Men's running shoes" width="1920" height="800"
         loading="eager" fetchpriority="high">

    <!-- Below-fold images: lazy loading, explicit dimensions -->
    <img src="product-2.webp" alt="Nike React Infinity" width="400" height="400" loading="lazy">

    <!-- Scripts: defer to not block rendering -->
    <script src="app.js" defer></script>
    <script src="analytics.js" async></script>
</body>
```

---

## 13. Accessibility as SEO

Google's crawlers increasingly simulate user experience. Poor accessibility = poor user experience = lower rankings. Many accessibility attributes are direct SEO signals.

### ARIA and semantic overlap

```html
<!-- aria-label on nav — helps Google understand navigation context -->
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Category navigation">...</nav>
<nav aria-label="Breadcrumb">...</nav>

<!-- aria-label on rating — communicates numeric score to crawlers -->
<div aria-label="Rating: 4.5 out of 5">
    <!-- star icons -->
</div>

<!-- aria-hidden on decorative icons — keeps them out of the semantic tree -->
<i class="fas fa-star" aria-hidden="true"></i>

<!-- aria-labelledby on buttons in repetitive layouts -->
<button type="button" aria-labelledby="product-title-3">Add to cart</button>
<h2 id="product-title-3">Nike Pegasus 40</h2>

<!-- aria-current on breadcrumb current page -->
<li><a href="/running/" aria-current="page">Running Shoes</a></li>
```

### Skip navigation

```html
<!-- Allows keyboard users (and crawlers) to skip repetitive nav -->
<a href="#main-content" class="visually-hidden focusable">Skip to main content</a>

<nav>...</nav>

<main id="main-content">...</main>
```

### Form labels

```html
<!-- ❌ Wrong — no association between label and input -->
<div>
    <span>Email</span>
    <input type="email" name="email">
</div>

<!-- ✅ Correct — explicit association -->
<div>
    <label for="email">Email address</label>
    <input type="email" id="email" name="email" autocomplete="email">
</div>
```

### Language of parts

```html
<!-- Mark language changes within a page -->
<p>The French word for shoe is <span lang="fr">chaussure</span>.</p>
```

---

## 14. Mobile & Viewport

Google uses mobile-first indexing. The mobile version of a page is what gets indexed and ranked.

### Viewport

```html
<!-- Required — without this, Google treats the page as not mobile-friendly -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- ❌ Never restrict zoom — accessibility violation AND ranking signal -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```

### Touch targets

- Buttons and links must be at least **48×48px** tap target size.
- Less than 48px = Google flags as "tap targets too close together" in Search Console.

### Font sizes

- Body text must be at least **16px** (1rem).
- Smaller text triggers a "text too small to read" mobile usability issue in Search Console.

### ❌ Wrong

```html
<!-- No viewport meta — page renders at desktop width on mobile -->
<!-- (missing <meta name="viewport">) -->

<!-- Zoom disabled — accessibility and ranking violation -->
<meta name="viewport" content="width=device-width, user-scalable=no">

<!-- Tiny tap targets -->
<a href="/product/" style="font-size: 10px; padding: 2px 4px;">View</a>
```

---

## 15. URL Structure

URLs are a weak but real ranking signal. More importantly, clean URLs get more clicks.

### Rules

- **Lowercase.** `/Running-Shoes/` and `/running-shoes/` are two different URLs.
- **Hyphens, not underscores.** Google treats hyphens as word separators. Underscores are not separators — `running_shoes` is read as one word `runningshoes`.
- **Short and descriptive.** `/mens-running-shoes/` not `/category/p=true&id=847&sort=asc`.
- **No special characters.** Only letters, numbers, hyphens, and forward slashes.
- **Trailing slash consistency.** Pick one (`/page/` or `/page`) and stick to it. Redirect the other to the canonical version.
- **Keyword in URL.** `/nike-pegasus-40/` is better than `/product/SKU-1234/`.
- **Depth.** Keep important pages within 3 directory levels of the root.

### ❌ Wrong

```
/Running_Shoes/Nike/           ← uppercase + underscores
/p?id=1234&cat=2&sort=price    ← no keywords, query-string only
/category/subcategory/sub-subcategory/brand/product-line/product-name/  ← too deep
/mens%20running%20shoes/       ← encoded spaces
/MENS-RUNNING-SHOES/           ← uppercase
```

### ✅ Correct

```
/mens-running-shoes/
/mens-running-shoes/nike/
/mens-running-shoes/nike/pegasus-40/
/blog/how-to-choose-running-shoes/
```

---

## 16. What Stays As-Is

Some HTML patterns look SEO-relevant but are either neutral or intentionally structured a certain way. Do not touch these.

### `inert` attribute on image links

```html
<!-- Image link uses inert — the text link below handles navigation -->
<!-- Do NOT remove inert — it prevents duplicate links for crawlers -->
<a href="#" inert>
    <img src="product.webp" alt="Product Name" ...>
</a>
<a href="/product/">Product Name</a>  <!-- this is the real link -->
```

### `tabindex="-1"` on icon buttons

```html
<!-- aria-hidden + tabindex="-1" on icon buttons that are decorative duplicates -->
<!-- Removing tabindex="-1" creates keyboard navigation noise, not SEO benefit -->
<div aria-hidden="true">
    <a href="#" tabindex="-1"><i class="fas fa-heart"></i></a>
</div>
```

### `aria-hidden="true"` on badge/icon containers

```html
<!-- Decorative badge container — correct to have aria-hidden -->
<!-- Removing it causes screen readers to announce "-20%" out of context -->
<div class="product-card-badges-top" aria-hidden="true">
    <span class="badge">-20%</span>
</div>
```

### `<meta itemprop="...">` inside structured data

```html
<!-- These invisible meta tags carry structured data values -->
<!-- They are correct — do not remove just because they have no visible output -->
<div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
    <meta itemprop="ratingValue" content="4.5">  <!-- correct: hidden but semantic -->
    <meta itemprop="bestRating" content="5">
    <meta itemprop="reviewCount" content="128">
</div>
```

### `<link itemprop="availability">` inside offers

```html
<!-- This is correct structured data syntax — not a CSS link -->
<link itemprop="availability" href="https://schema.org/InStock">
```

---

## 17. Anti-Patterns — Never Do These

```html
<!-- ❌ Duplicate title tags -->
<title>Page Title</title>
<title>Another Title</title>
<!-- The last one wins — always a bug -->

<!-- ❌ Hidden content intended to deceive Google (cloaking) -->
<p style="display:none">keyword keyword keyword</p>
<p style="color:white; background:white">hidden keywords</p>
<!-- Google penalises this as spam -->

<!-- ❌ Keyword stuffing in meta keywords (ignored since 2009) -->
<meta name="keywords" content="shoes running shoes buy shoes cheap shoes">
<!-- Completely ignored by Google — wastes HTML space -->

<!-- ❌ Multiple h1 tags on non-homepage -->
<h1>Main Topic</h1>
...
<h1>Another Topic</h1>

<!-- ❌ Using headings for styling, not structure -->
<h4 class="sidebar-label">Filter by size</h4>
<!-- Use <p class="sidebar-label"> or <span> instead -->

<!-- ❌ noindex on pages that should be indexed -->
<meta name="robots" content="noindex">
<!-- On a product page — kills it from search entirely -->

<!-- ❌ nofollow on internal links -->
<a href="/category/" rel="nofollow">Category</a>
<!-- Leaks PageRank, wastes crawl budget -->

<!-- ❌ JavaScript-only content with no fallback -->
<div id="product-grid"></div>
<script>renderProducts()</script>
<!-- If JS fails or is slow, Google sees an empty div -->

<!-- ❌ Lazy loading on the LCP image -->
<img src="hero.jpg" alt="Hero" loading="lazy">
<!-- Delays LCP, harms Core Web Vitals -->

<!-- ❌ Missing width/height on images -->
<img src="product.jpg" alt="Product">
<!-- Causes CLS — layout shifts penalise ranking -->

<!-- ❌ Canonical pointing to a redirected URL -->
<link rel="canonical" href="https://example.com/old-url/">
<!-- Old URL redirects to /new-url/ — canonical should point to /new-url/ -->

<!-- ❌ Mixed content: HTTP resource on HTTPS page -->
<img src="http://example.com/image.jpg" alt="Product">
<!-- Browser blocks it, Google sees broken content -->

<!-- ❌ Fake structured data — rating markup with no visible rating -->
<script type="application/ld+json">
{ "aggregateRating": { "ratingValue": "5", "reviewCount": "5000" } }
</script>
<!-- No ratings visible on page — Google penalises as structured data spam -->
```

---

## 18. Replacement Table

### Meta tags

| Wrong | Correct | Notes |
|---|---|---|
| `<meta name="keywords" content="...">` | Remove entirely | Ignored by Google since 2009 |
| No `<title>` | Add `<title>Primary Keyword — Brand</title>` | Most important on-page element |
| `<title>` over 60 chars | Trim to 50–60 chars | Truncation loses brand |
| No `<meta name="description">` | Add with 150–160 chars | Controls search snippet |
| No `<link rel="canonical">` | Add self-referencing canonical | Prevents duplicate content issues |
| `<link rel="canonical" href="/relative/">` | `<link rel="canonical" href="https://example.com/full-url/">` | Must be absolute |
| `<meta name="viewport" content="..., user-scalable=no">` | Remove `user-scalable=no` | Accessibility + ranking violation |

### Headings

| Wrong | Correct |
|---|---|
| Multiple `<h1>` | Single `<h1>` per page |
| `<h1>` and `<title>` on different topics | Align them |
| `<h3>` after `<h1>` (skipped level) | `<h1>` → `<h2>` → `<h3>` |
| `<h2>` used to style sidebar labels | `<p>` or `<span>` with CSS class |

### Images

| Wrong | Correct |
|---|---|
| `alt="image of shoe"` | `alt="Nike Pegasus 40 in blue"` |
| `alt="shoe shoe running shoe buy shoe"` | `alt="Nike Pegasus 40 men's running shoe"` |
| No `alt` attribute | `alt="..."` or `alt=""` for decorative |
| No `width`/`height` | Always specify both |
| `loading="lazy"` on hero | `loading="eager"` + `fetchpriority="high"` |
| `IMG_4829.jpg` | `nike-pegasus-40-mens-blue.jpg` |
| PNG for photos | WebP with JPEG fallback |

### Links

| Wrong | Correct |
|---|---|
| `<a href="#">Click here</a>` | `<a href="/shoes/">Men's Running Shoes</a>` |
| `<a href="javascript:void(0)">` | Real `href` or `<button>` |
| `rel="nofollow"` on internal links | Remove `rel` from internal links |
| Affiliate link without `rel="sponsored"` | Add `rel="sponsored noopener"` |
| `target="_blank"` without `rel="noopener"` | Add `rel="noopener noreferrer"` |

### Semantic structure

| Wrong | Correct |
|---|---|
| `<div class="header">` | `<header>` |
| `<div class="nav">` | `<nav aria-label="Main navigation">` |
| `<div id="main">` | `<main>` |
| `<div class="footer">` | `<footer>` |
| `<div class="article">` | `<article>` |
| No semantic structure at all | `<header>`, `<main>`, `<footer>` minimum |

---

## 19. Final Checklist

Run this before and after every SEO refactoring session.

### Document

- [ ] `<!DOCTYPE html>` is the very first line
- [ ] `<html lang="...">` has the correct BCP 47 language code
- [ ] `<meta charset="utf-8">` is within the first 1024 bytes
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">` present — no `user-scalable=no`
- [ ] `<title>` exists, is unique, 50–60 chars, keyword-first
- [ ] `<meta name="description">` exists, is unique, 150–160 chars, has CTA
- [ ] `<link rel="canonical" href="https://...">` exists with absolute URL
- [ ] No `<meta name="keywords">` (useless noise)
- [ ] `<main>` wraps primary content — one per page

### Headings

- [ ] Exactly one `<h1>` per page
- [ ] `<h1>` topic aligns with `<title>`
- [ ] Heading hierarchy is sequential — no skipped levels
- [ ] No headings used purely for visual styling

### Semantic HTML

- [ ] `<header>`, `<nav>`, `<main>`, `<footer>` are used correctly
- [ ] `<article>` wraps self-contained content
- [ ] `<section>` has a heading
- [ ] `<nav>` has `aria-label` when multiple navs exist on a page

### Images

- [ ] Every `<img>` has an `alt` attribute (descriptive or empty for decorative)
- [ ] No keyword-stuffed `alt` text
- [ ] File names are descriptive and hyphenated
- [ ] Every `<img>` has `width` and `height` attributes
- [ ] Hero / LCP image has `loading="eager"` and `fetchpriority="high"`
- [ ] All below-fold images have `loading="lazy"`
- [ ] Images are in WebP or AVIF format where possible

### Links

- [ ] No `href="#"` on real navigation links
- [ ] No `href="javascript:..."` links
- [ ] Anchor text is descriptive — no "click here", "read more", "here"
- [ ] Internal links have no `rel="nofollow"`
- [ ] Paid/affiliate links have `rel="sponsored"`
- [ ] External links have `rel="noopener noreferrer"` if `target="_blank"`

### Structured Data

- [ ] Product pages have Product schema with price, availability, and aggregateRating
- [ ] Structured data values match visible page content
- [ ] Validated with Google Rich Results Test
- [ ] BreadcrumbList schema matches the visible HTML breadcrumb
- [ ] FAQ schema only used when actual Q&A content is on the page
- [ ] `datePublished` and `dateModified` present on articles

### Open Graph

- [ ] `og:title`, `og:description`, `og:image`, `og:url`, `og:type` are all present
- [ ] `og:image` is an absolute URL, 1200×630px minimum
- [ ] `twitter:card` is `summary_large_image`
- [ ] Twitter meta tags match OG tags

### Performance

- [ ] LCP image is preloaded: `<link rel="preload" as="image" href="..." fetchpriority="high">`
- [ ] Font CDN uses `<link rel="preconnect">`
- [ ] No render-blocking scripts in `<head>` without `defer` or `async`
- [ ] Scripts use `defer` (for DOM-dependent) or `async` (for independent)

### Indexing

- [ ] No `<meta name="robots" content="noindex">` on pages that should rank
- [ ] No `rel="noindex"` on important pages
- [ ] Canonical URLs use HTTPS, not HTTP
- [ ] Canonical does not point to a redirected URL

### Mobile

- [ ] Viewport meta is present without `user-scalable=no`
- [ ] Touch targets are ≥48×48px
- [ ] Body font size is ≥16px

---

## Score

After refactoring, a clean page should pass every checklist item. Priority order if time is limited:

1. **CRITICAL:** `<title>`, `<meta description>`, `<link rel="canonical">`, single `<h1>`, image `alt` text, no `noindex` on ranked pages
2. **HIGH:** Structured data, semantic elements (`<main>`, `<article>`), image dimensions, `loading` attributes
3. **MEDIUM:** Open Graph, resource hints, anchor text quality, heading hierarchy
4. **LOW:** `hreflang`, `og:image` dimensions, `rel="sponsored"` on affiliate links

---

*Guide written based on Google Search Central documentation, Core Web Vitals spec, Schema.org vocabulary, and HTML Living Standard.*
*Applicable to any HTML page targeting Google Search.*
*Version: 1.0*
