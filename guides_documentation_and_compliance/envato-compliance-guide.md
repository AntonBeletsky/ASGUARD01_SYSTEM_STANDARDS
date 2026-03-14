# Envato Marketplace — Template Compliance Guide
> Complete Reference for Marketplace-Ready Template Development  
> Covers: Branding & IP · Personal Data · Code Quality · Assets · Legal · Pre-Launch Checklist

---

## Introduction

This guide provides a complete, actionable reference for developers building templates and themes intended for sale on Envato marketplaces (ThemeForest, CodeCanyon, VideoHive, etc.). The fundamental principle is **universal neutrality**: every buyer must receive a clean, blank-slate product that requires no scrubbing of someone else's personal or proprietary data.

Failure to comply with these rules leads to soft rejections, hard rejections, or removal of already-published items. This document covers every category of prohibited content with clear explanations of what is wrong, why it is wrong, and what the correct approach is.

> **How to use this guide:** Each section describes a category of compliance risk. Use the ✗ / ✓ examples throughout as a quick reference. The Pre-Launch Checklist at the end summarises every action item in one place.

---

## 1. Brands, Trademarks & Logos

Buyers purchasing a template do not hold a licence to display third-party trademarks. Embedding recognisable brand assets into demo content exposes both you and the buyer to intellectual-property claims and guarantees a rejection from Envato's review team.

### 1.1 Logos and Wordmarks

- ✗ **WRONG** — Apple, Nike, Google, Amazon, Adidas, Coca-Cola, or any other recognisable brand wordmark or logo — even rendered as a small decoration or used as a placeholder.
- ✓ **CORRECT** — Create abstract geometric shapes as placeholder logos, or use text strings such as `BRAND`, `LOGO`, or `YOUR LOGO HERE` styled to look like a real logo.

### 1.2 Social Media Brand Assets

Platform icons (Facebook, Instagram, X/Twitter, TikTok, LinkedIn, YouTube) are technically trademarked. You may include recognisable social icons from an icon set, but all links must point to a hash anchor:

```html
<!-- ✗ WRONG -->
<a href="https://www.facebook.com/ActualCompanyPage">...</a>

<!-- ✓ CORRECT -->
<a href="#">...</a>
```

Never pre-fill social profile URLs with your own accounts or any real company's accounts.

### 1.3 Product & Service Names in Copy

- ✗ **WRONG** — "Buy now on Amazon", "Powered by Shopify", "As seen on CNN", "Trusted by Microsoft" used as demo testimonial copy.
- ✓ **CORRECT** — "Buy now", "Powered by our platform", "As featured in leading publications".

### 1.4 App Store Badges

The Apple App Store badge and Google Play badge are licensed assets. Do not include them as static images. If your template needs app-store buttons, use custom-designed buttons or clearly labelled placeholder rectangles.

> **Key rule:** Ask yourself: *"Could a trademark owner send a cease-and-desist over this content?"* If yes — replace it with a placeholder.

---

## 2. Personal & Contact Information

Demo content must never contain real identifying information about any individual or organisation. This applies to both the developer and any fictional "sample" business shown in the template.

### 2.1 Phone Numbers

- ✗ **WRONG** — Any real phone number, including your own number used as a placeholder.
- ✓ **CORRECT** — Use the NANP reserved number range for US-style demos: `+1 (555) 000-0000` through `+1 (555) 999-9999`. For international formats use: `+44 0000 000000`, `+49 0000 0000000`.

### 2.2 Physical Addresses

- ✗ **WRONG** — Your home address, your studio address, a real business address, or even a well-known address (e.g. 10 Downing Street, 1600 Pennsylvania Ave).
- ✓ **CORRECT** — Use a clearly fictional address: `123 Demo Street, Sample City, ST 00000, United States`. Never use a real postcode/zip that places the address on a real map.

### 2.3 Email Addresses

- ✗ **WRONG** — `your.name@gmail.com`, `yourcompany@outlook.com`, any real deliverable email address.
- ✓ **CORRECT** — `support@example.com`, `hello@yourdomain.com`, `info@company.com`. The domain `example.com` is IANA-reserved and safe to use.

### 2.4 Real Names in Team / About Sections

- ✗ **WRONG** — Photos of your friends, colleagues, or family members with their actual names and job titles.
- ✓ **CORRECT** — Use widely available CC0 stock portraits (e.g. from Unsplash, Pexels) combined with generic names: "John Smith – CEO", "Sarah Johnson – Lead Designer".

### 2.5 Testimonials and Reviews

- ✗ **WRONG** — A review attributed to a real person you know, or a screenshot of a real review from your own portfolio.
- ✓ **CORRECT** — Invent personas with fictional names, generic avatars, and plausible but fictional quotes. Do not use photos of identifiable people without an explicit model release.

### 2.6 National ID, VAT, Company Registration Numbers

- ✗ **WRONG** — Any number that could be validated against a national registry.
- ✓ **CORRECT** — Use `VAT: XX0000000`, `Reg. No.: 0000000`.

---

## 3. Hardcoded Links & Paths

Every URL in demo content must either be a safe placeholder or resolve to a clearly neutral, universal destination. Never embed links that expose personal accounts, affiliate tracking, or local machine paths.

### 3.1 Internal Navigation Links

```html
<!-- ✗ WRONG -->
<a href="http://myportfolio.com/projects">Portfolio</a>

<!-- ✓ CORRECT -->
<a href="#">Portfolio</a>
<a href="index.html">Portfolio</a>
```

### 3.2 Developer's Own Website

Do not include links to your personal site, portfolio, or studio inside the template's demo content (pages, footer credits). You are allowed a single line in the **documentation PDF** that credits you as the author — not inside the template HTML/CSS itself.

### 3.3 Affiliate & Tracking Links

- ✗ **WRONG** — Any URL that contains tracking parameters, referral codes, or affiliate IDs.
- ✓ **CORRECT** — Strip all UTM parameters and tracking codes from URLs included in demo content.

### 3.4 Local / Absolute Filesystem Paths

```html
<!-- ✗ WRONG -->
<img src="C:\Users\Anton\Projects\MyTheme\images\bg.jpg">

<!-- ✓ CORRECT -->
<img src="assets/images/bg.jpg">
```

All asset references must be relative paths from the project root.

### 3.5 CDN URLs Pinned to Private Accounts

- ✗ **WRONG** — Linking to assets stored in your private AWS S3 bucket, Cloudinary account, or similar personal CDN.
- ✓ **CORRECT** — Bundle all assets locally, or use well-known public CDNs (`cdnjs.cloudflare.com`, `jsdelivr.net`, `fonts.googleapis.com`) with stable, version-pinned URLs.

---

## 4. API Keys, Credentials & Secrets

Shipping a working API key in a public product is a serious security and business mistake. Keys become publicly accessible the moment the file is downloaded and can be abused at your expense.

### 4.1 Map API Keys

```javascript
// ✗ WRONG
apiKey: 'AIzaSyAbc123RealKeyHere'

// ✓ CORRECT
apiKey: 'YOUR_GOOGLE_MAPS_API_KEY'
```

Google Maps, Mapbox, HERE Maps, and all other map providers require API keys. Leave a clearly labelled placeholder and document how the buyer obtains and inserts their own key.

### 4.2 Email / SMTP Credentials

- ✗ **WRONG** — SMTP host, username, and password for your own Gmail, SendGrid, Mailchimp, or similar account.
- ✓ **CORRECT** — Leave commented-out placeholders in config files:
  ```
  SMTP_HOST=your-smtp-host.com
  SMTP_USER=your@email.com
  SMTP_PASS=your-password
  ```

### 4.3 Payment Provider Keys

- ✗ **WRONG** — Stripe publishable key, PayPal client ID, Square application ID.
- ✓ **CORRECT** — `pk_test_YOUR_STRIPE_PUBLISHABLE_KEY` or equivalent labelled placeholder.

### 4.4 OAuth Tokens & Client Secrets

- ✗ **WRONG** — GitHub personal access tokens, OAuth client secrets, JWT signing keys, Firebase config objects with real project credentials.
- ✓ **CORRECT** — Replace every secret value with descriptive variable names in a `.env.example` file. Never commit a `.env` file.

### 4.5 Analytics Tracking IDs

```javascript
// ✗ WRONG
gtag('config', 'G-REAL1234567')

// ✓ CORRECT
gtag('config', 'YOUR_GA4_MEASUREMENT_ID')
```

This applies to Google Analytics, Facebook Pixel, Hotjar, Mixpanel, and all other analytics integrations.

---

## 5. Licensed & Restricted Content

The assets inside your deliverable archive must be either created by you, licensed for resale/redistribution, or clearly excluded from the package with documentation explaining where the buyer can obtain them.

### 5.1 Stock Photography

- ✗ **WRONG** — High-resolution stock images from Shutterstock, Getty Images, Adobe Stock, or any paid library included in the main download package.
- ✓ **CORRECT** — Replace all photography with solid-colour or gradient placeholder blocks labelled with their dimensions (e.g. `1200 × 800`). Use only CC0 images (Unsplash, Pexels) or images you have a redistribution-compatible licence for. Document image sources in your credits file.

### 5.2 Icon Libraries

Most icon libraries (Font Awesome Pro, Streamline, Iconfinder premium packs) have licences that prohibit redistribution inside a commercial theme. Safe options include:

| Library | Licence |
|---|---|
| Font Awesome Free | MIT / CC-BY |
| Feather Icons | MIT |
| Heroicons | MIT |
| Lucide | ISC |
| Material Icons | Apache 2.0 |

### 5.3 Fonts

- ✗ **WRONG** — Paid fonts such as Proxima Nova, Gotham, or any font purchased from MyFonts, Fonts.com, etc., unless you hold a web-embedding licence that explicitly permits redistribution.
- ✓ **CORRECT** — Use only Google Fonts or other OFL (Open Font Licence) typefaces. Document the font names and their source URLs in your README.

### 5.4 Third-Party Plugins & Scripts

- ✗ **WRONG** — Premium jQuery plugins, paid WordPress plugins, commercial Figma component libraries bundled without an extended/OEM licence.
- ✓ **CORRECT** — Use free/open-source plugins only, OR hold an Extended Licence permitting resale. Clearly state all dependencies in your documentation so buyers can obtain them independently if needed.

### 5.5 Music and Sound

- ✗ **WRONG** — Background tracks, UI sounds, or jingles from commercial libraries or from popular artists used without a sync licence.
- ✓ **CORRECT** — Use only royalty-free, redistribution-friendly audio. Freesound.org (CC0), ccMixter, and Bensound (with proper attribution) are acceptable sources.

---

## 6. Maps and Geographic Content

If your template includes an embedded map, the default centre point and any visible markers matter. Centering a map on your home address or office leaks location data and looks unprofessional to buyers in different countries.

### 6.1 Map Centre Point

- ✗ **WRONG** — Coordinates that resolve to your house, studio, or the office of a real business.
- ✓ **CORRECT** — Use a well-known neutral landmark as the default: central New York `(40.7128, -74.0060)`, central London `(51.5074, -0.1278)`, or simply the centre of an ocean.

### 6.2 Map Markers

- ✗ **WRONG** — A pin placed on a real business with a real name shown in the popup.
- ✓ **CORRECT** — Label markers generically: "Our Office", "Main Location", or use a pin with no popup text.

### 6.3 Geographic Specificity in Copy

- ✗ **WRONG** — "Serving customers across Kharkiv Oblast" or "Available in Kyiv, Lviv, and Odesa" used as hardcoded demo copy.
- ✓ **CORRECT** — "Serving customers nationwide", "Available in all major cities".

---

## 7. Code Quality & Hidden Debris

Envato reviewers inspect source code. Sloppy, cluttered, or system-generated junk files are grounds for rejection and undermine buyer trust.

### 7.1 System Files — Must Always Be Excluded

| File | Why it must be excluded |
|---|---|
| `.DS_Store` | macOS folder metadata — exposes your local folder structure |
| `Thumbs.db` | Windows Explorer thumbnail cache |
| `desktop.ini` | Windows folder configuration file |
| `.Spotlight-V100` | macOS Spotlight indexing data |
| `ehthumbs.db` | Windows Media Centre thumbnail cache |

### 7.2 Version Control Directories

```
✗ Include:  .git/   .svn/   .hg/
✓ Add these to .gitignore and exclude from your ZIP export
```

Shipping a `.git` folder exposes your entire commit history, which may contain earlier versions of code with real credentials or personal data.

### 7.3 Developer Comments and TODOs

```javascript
// ✗ WRONG
// TODO: fix this before launch, Anton
// HACK: temporary workaround, ask Sergiy about this
// my personal FTP is ftp://...

// ✓ CORRECT — remove all personal notes before packaging
// Keep only comments that explain non-obvious logic, written in English
```

### 7.4 Unused / Dead Code

Remove commented-out blocks of old code, unused CSS classes, orphaned JavaScript functions, and empty template files included by accident. Clean code is a positive review signal.

### 7.5 Console Logs and Debug Statements

```javascript
// ✗ WRONG
console.log('testing fix for Alex, remove later')

// ✓ CORRECT — all console.log() and debugger; statements removed or behind a debug flag
```

### 7.6 Build Artefacts

Do not include `node_modules/`, `vendor/` (PHP Composer), `__pycache__/`, `*.pyc`, `.cache/`, or `dist/` build output alongside editable source files without a clear README explaining the project structure. Either ship only the compiled output, or ship both with clear build instructions.

---

## 8. Copyright & Legal Text

The legal text visible in your demo must be clearly placeholder content and must not imply affiliation with or ownership by any specific real entity.

### 8.1 Footer Copyright Line

- ✗ **WRONG** — `© 2026 Anton Kovalenko Design Studio` — or any real name/business.
- ✓ **CORRECT** — `© 2026 YourBrandName. All rights reserved.`

### 8.2 Privacy Policy & Terms of Service

Do not include a real privacy policy or terms of service based on your own company. Include a visually styled placeholder page that signals to buyers where their own legal text should go:

> `[Your Privacy Policy text goes here. Replace this with your actual legal copy before going live.]`

### 8.3 Registered / Trademarked Symbols

Do not use ® or ™ symbols next to fictional brand names in demo content. This could imply you are making a claim of trademark ownership.

### 8.4 Licences of Included Components

Your documentation must list every third-party library, plugin, and asset included, along with its licence. Example:

| Component | Licence / Source |
|---|---|
| Bootstrap 5.3.2 | MIT — getbootstrap.com |
| Inter typeface | OFL 1.1 — fonts.google.com |
| Feather Icons 4.29 | MIT — feathericons.com |
| Unsplash demo photos | Unsplash Licence — unsplash.com |

---

## 9. Metadata & File Properties

Metadata embedded in files can inadvertently expose personal information that buyers and Envato reviewers may inspect.

### 9.1 Image EXIF Data

Photos taken with a camera or smartphone embed GPS coordinates, device model, and sometimes the photographer's name in EXIF metadata. Strip EXIF data from all images before packaging:

```bash
# ExifTool
exiftool -all= ./assets/images/

# ImageMagick
convert input.jpg -strip output.jpg
```

### 9.2 Document Metadata (PSD, AI, Sketch, Figma)

If you include source files, check that document metadata does not contain your real name, company, or email. In Photoshop: **File → File Info → clear Author, Copyright fields** before export.

### 9.3 HTML `<meta>` Tags

```html
<!-- ✗ WRONG -->
<meta name="author" content="Anton Kovalenko">
<meta name="generator" content="WebStorm 2024.3 by JetBrains">

<!-- ✓ CORRECT -->
<meta name="author" content="Your Name">
```

### 9.4 `package.json` / `composer.json`

```json
// ✗ WRONG
"author": "anton.k@mypersonalmail.com"

// ✓ CORRECT
"author": "Your Name <support@yourdomain.com>"
```

---

## 10. Dummy Content Standards

The text and placeholder content visible in the demo must be clean, professional, and contextually appropriate.

### 10.1 Lorem Ipsum

Standard Lorem Ipsum text is acceptable for body copy placeholders, but be aware that some reviewers flag excessive Lorem Ipsum in prominent locations (hero headings, navigation items). Use contextually appropriate sample text in key visible areas.

### 10.2 Numbers in Content

Prices, statistics, and measurements shown in demo content should look realistic but be obviously fictional:

- **Product prices:** $19, $49, $99 — avoid $0.00 or unrealistically large numbers
- **Statistics:** "Over 2,000 happy customers" — plausible but clearly placeholder
- **Dates:** Use relative dates or clearly near-future/past dates — avoid today's exact date hardcoded

### 10.3 Language

- ✗ **WRONG** — Demo content written entirely in Russian, Ukrainian, German, or any non-English language (unless the template is specifically sold as a localised product).
- ✓ **CORRECT** — All default demo content in English. If you include multilingual support, provide the English version as the primary demo.

### 10.4 Offensive or Sensitive Copy

Demo text must not reference politics, religion, controversial current events, or contain jokes that could be interpreted as discriminatory. Keep all copy neutral and universally business-appropriate.

---

## 11. Pre-Launch Compliance Checklist

Run through every item below before submitting your template.

### Branding & Trademarks
- [ ] No real brand logos or wordmarks in any image or HTML
- [ ] Social icons link to `#` only
- [ ] No app store badges (Apple/Google) as static images
- [ ] No real brand names used in marketing copy

### Personal & Contact Data
- [ ] All phone numbers use reserved/fictional ranges (555-xxxx)
- [ ] All addresses use fictional street names and zip codes
- [ ] All emails use `@example.com` or `@yourdomain.com`
- [ ] No real names or recognisable photos in team/testimonial sections
- [ ] No national ID, VAT, or company registration numbers

### Links & Paths
- [ ] All internal navigation links are relative or point to `#`
- [ ] No links to developer's personal site in demo content
- [ ] No affiliate or tracking parameters in any URL
- [ ] All asset paths are relative (no `C:\` or `/Users/` paths)
- [ ] No assets served from personal CDN or private cloud storage

### API Keys & Credentials
- [ ] No real Google Maps / Mapbox API keys in source code
- [ ] No SMTP passwords, OAuth tokens, or payment keys
- [ ] No analytics tracking IDs (replace with `YOUR_MEASUREMENT_ID`)
- [ ] `.env` file excluded; `.env.example` provided with placeholder values

### Assets & Licensing
- [ ] No premium stock photos in the download package
- [ ] All fonts are OFL or similarly redistribution-compatible
- [ ] All icon libraries are free/open-source
- [ ] All third-party plugins either free or covered by extended licence
- [ ] Credits/licences documented in README or separate `CREDITS.txt`

### Maps
- [ ] Map default centre is a neutral public landmark or ocean
- [ ] Map markers use generic labels only

### Code Quality
- [ ] `.DS_Store`, `Thumbs.db`, and other OS junk files removed
- [ ] `.git`, `.svn` directories excluded from ZIP
- [ ] No personal TODO / HACK comments with real names
- [ ] All `console.log()` and `debugger;` statements removed
- [ ] `node_modules`, `vendor`, `__pycache__` excluded or clearly documented

### Legal Text
- [ ] Footer copyright uses placeholder brand name (not real name)
- [ ] Privacy Policy / Terms of Service pages are clearly placeholder
- [ ] No ® or ™ next to fictional brand names
- [ ] Third-party component licences listed in documentation

### Metadata
- [ ] EXIF data stripped from all photos
- [ ] PSD/AI source file metadata cleared of personal information
- [ ] HTML `<meta name="author">` contains placeholder value
- [ ] `package.json` author field uses placeholder contact

### Content
- [ ] Default demo language is English
- [ ] No offensive, political, or religious content
- [ ] Prices and statistics look realistic but are obviously fictional

---

> **Final thought:** When in doubt, ask: *"Would a buyer in any country, in any industry, be embarrassed or harmed by this content?"* If yes — replace it. A clean, neutral template sells better and stays live longer.
