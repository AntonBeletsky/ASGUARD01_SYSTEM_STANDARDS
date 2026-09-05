# Documentation Requirements for Website Templates (Envato / ThemeForest and TemplateMonster)

Compiled from the official author guidelines for both platforms, current as of September 2026. Applies to HTML/CSS/JS templates, React/Vue/Angular templates, WordPress and other CMS themes — the requirements for the documentation itself are nearly identical across types; differences are noted separately.

## 1. Why This Matters

- Without documentation, an item won't pass moderation on either platform — it's one of the first things reviewed.
- TemplateMonster explicitly lists missing or weak documentation as one of the most common reasons items get sent back for improvement.
- Good documentation reduces support tickets and directly affects sales — both platforms call it a significant factor in conversion.

## 2. General Requirements (same for both platforms)

Required sections:
- **Installation** — step by step, from unzipping the archive to first launch (including demo content import, if applicable).
- **Setup/customization** — how to change colors, fonts, sections; separately, contact form configuration, if present.
- **File structure** — what's in which folder, with screenshots.
- **Environment requirements** — CMS/PHP/Node/browser versions, if critical to the template's operation.
- **Third-party asset credits** — all fonts, icons, images, plugins and libraries not authored by you, with license type and a link to the source.
- **What's not included in the archive** — stock photos used for preview only, paid fonts/plugins, activation keys: if something isn't included in the purchase, state this explicitly.
- **FAQ**.
- **Changelog** — version history with dates.
- **Support contact info** and what it covers.

General presentation rules:
- Language — English, an official requirement on both platforms.
- Write as if the reader has no coding experience — spell things out, add screenshots.
- Video/screencast — supplements the text only, never replaces it.
- Update the documentation with every release, and note the last-updated date.
- The underlying technology (plain HTML/CSS, React/Vue/Angular, WordPress, Shopify, etc.) doesn't change the list of sections — only the details within them.

## 3. The Key Difference Between Platforms — File Format

| Criterion | Envato / ThemeForest | TemplateMonster |
|---|---|---|
| Format | PDF **or** HTML | **HTML only** (PDF/TXT/XML discouraged) |
| Language | English | English |
| Video instead of text | Not allowed, supplement only | Not allowed, supplement only |
| One doc for multiple items | Not explicitly forbidden | Explicitly forbidden — each item needs its own |
| Changelog | Best practice | Required field in the upload form, fixed format |
| Folder in archive | Usually `documentation/` | `/Documentation` — fixed name |

**Takeaway**: if you're selling the same item on both platforms, build the documentation in HTML from the start. Converting HTML → PDF for Envato later is easier than the other way around.

## 4. Envato (ThemeForest / Envato Market) — Details

### 4.1 Format and content
PDF or HTML, in English. Must include:
- concise installation, customization, and usage instructions;
- additional general information;
- credits and links for all third-party resources.

Envato publishes a downloadable documentation template in its author help center — you can use it as a starting point.

### 4.2 Asset licensing
- Even an asset used only in the preview and not included in the purchase still requires a commercial license.
- If an asset is bundled into the file itself, you need a **redistribution** license (the right to resell), not just a usage license.
- If something isn't included in the package, this must be stated explicitly in both the item description and the documentation.

### 4.3 Licensing folder (not for all types)
A separate `/Licensing` folder with two .txt files is required inside the archive for:
- Joomla, Drupal, OpenCart, osCommerce — GPL license;
- Magento, PrestaShop — OSL v3 license.

For **WordPress**, no folder is needed — the license is attached automatically on upload.

### 4.4 Notes by template type
- **Email templates** — documentation should account for email-client markup constraints (tables, inline CSS).
- **Figma / Adobe XD / Sketch** — the organization of the file itself matters too (Pages/Frames, grid), but written documentation is still required separately.
- **WordPress** — documentation should cover demo content import and any bundled third-party plugins/libraries.

### 4.5 What to say about support (Item Support)
If you offer paid support, Envato's policy requires a minimum of **6 months** from the purchase date, extendable to 12. Support covers: answering technical questions about features, help with the item's bundled third-party assets, and bug fixes. It does not cover: turnkey installation, customization for a specific buyer, or hosting/third-party software help. Spelling this out in the documentation reduces disputed support requests.

*(On Envato Elements — the subscription model — the formal Item Support policy doesn't apply.)*

## 5. TemplateMonster — Details

Documentation is on the list of the most common reasons TemplateMonster sends an item back for revision, so there's little room for "good enough" here.

### 5.1 Format
**HTML only** — PDF/TXT/XML are explicitly discouraged in the author guide. A text version with screenshots is required; video is a supplement only. Each item needs its own unique documentation — reusing one file across different templates isn't allowed.

### 5.2 Required sections (must-haves)
1. **Installation Instructions** — step by step, ideally with video too.
2. **Server Requirements** — hosting/server/software version requirements.
3. **Plugin Information** — which plugins are used and how to connect them.
4. **Modification Guidelines** — how to customize, with screenshots, including contact form setup.
5. **Regular Updates** — documentation updated alongside the product, with a current date.
6. **Complete information** — explicitly state if paid plugins/fonts/activation keys are needed.

### 5.3 What documentation should not contain
- links to personal websites, social media, or other marketplaces;
- one piece of documentation "for all products";
- reliance on video/online format alone, without a text version.

### 5.4 Where documentation sits in the archive

| Product type | Archive structure |
|---|---|
| CMS themes (WordPress, etc.) | `/Documentation` (HTML) + `/PSD` (optional) + `/Demo Content` + `/themename.zip` |
| HTML templates | `/Documentation` (HTML) + `/PSD` (optional) + `/themename.zip` |
| Graphics | `/Documentation` (PDF/HTML) + `/Source Files` |

A `readme.txt` at the archive root is optional, but it's a convenient place for brief credits and licensing details.

### 5.5 Changelog — a separate required field
This is a field in the product upload form, not a file inside the archive — but it's still documentation, and shouldn't be skipped.
- Date format: `MM DD, YYYY`.
- Entry categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`, `Updated`.
- Roughly 30 characters minimum per entry, or the form won't save.
- Published under the Description block once moderation approves the change.

Example entry:
```
June 15, 2026:
- Fixed: mobile menu overlapping the hero section on small screens.
- Added: new "Pricing" page template with three plan layouts.
```

### 5.6 Other review criteria that overlap with documentation
- Cross-browser compatibility must be stated in both the description and the documentation.
- Any third-party plugins/modules must be described in the documentation, with the author guaranteeing compatibility.
- The author is responsible for copyright issues if third-party software is used without a proper license.

## 6. Pre-Upload Checklist

- [ ] Documentation in English
- [ ] HTML format (works for both platforms; PDF is an extra option for Envato only)
- [ ] Separate `Documentation` folder in the archive
- [ ] Step-by-step installation + screenshots
- [ ] Customization/setup section
- [ ] Clearly states what's not included
- [ ] Credits and licenses for all third-party resources, with source links
- [ ] Server/CMS/version requirements
- [ ] FAQ
- [ ] Changelog with dates (+ separate field on TemplateMonster upload)
- [ ] Support contact info and what it covers/doesn't cover
- [ ] For Joomla/Drupal/OpenCart/osCommerce/Magento/PrestaShop — `Licensing` folder
- [ ] One product = one unique set of documentation
- [ ] Last-updated date noted
- [ ] No links to personal sites/social media/other marketplaces (critical for TemplateMonster)

## 7. Suggested index.html Documentation Structure

Works as a base for both platforms:
1. Title, template version, last-updated date
2. Table of contents
3. About the template / Getting Started
4. Requirements (server, software versions, browsers)
5. Installation
6. Setup and customization
7. File structure overview
8. Third-party assets & credits
9. FAQ
10. Changelog
11. Support — what's covered, how to reach out

## 8. Sources

- Envato Author Support — [Themes Item Preparation & Technical Requirements](https://help.author.envato.com/hc/en-us/articles/360000470826-Themes-Item-Preparation-Technical-Requirements)
- Envato Market — [Item Support Policy](https://themeforest.net/page/item_support_policy)
- Envato Author Support — [Item Support - Best Practices](https://help.author.envato.com/hc/en-us/articles/360000471703-Item-Support-Best-Practices)
- TemplateMonster — [The Most Common Reasons For Product Improvement Requests](https://helpdesk.templatemonster.com/the-most-common-reasons-for-product-improvement-requests/)
- TemplateMonster — [Item Archive Requirements](https://helpdesk.templatemonster.com/item-archive-requirements/)
- TemplateMonster — [How to Write an Effective Changelog for Your Products](https://helpdesk.templatemonster.com/how-to-write-changelog/)

Both platforms update their requirements periodically — if anything here doesn't match what you see in the actual upload interface, check these pages directly.
