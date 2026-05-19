# Web Accessibility Compliance Guide
## For Developers — EU · Germany · USA
### Standards: WCAG 2.2 AA · EN 301 549 v3.2.1 · Section 508 · ADA Title II

> **Purpose:** This guide enables an AI agent or developer to audit and remediate an HTML/CSS/JS website template to full compliance with EU, German, and US accessibility law. Every section maps legal requirement → technical standard → concrete code pattern. Work through the checklist top-to-bottom and the result will satisfy EN 301 549 v3.2.1 (WCAG 2.1 AA embedded), WCAG 2.2 AA best-practice, and the US ADA Title II / Section 508 obligations in force as of 2025-2026.

---

## Table of Contents

1. [Legal Framework Matrix](#1-legal-framework-matrix)
2. [Standards Architecture](#2-standards-architecture)
3. [The POUR Principles Expanded](#3-the-pour-principles-expanded)
4. [WCAG 2.1 AA — All 50 Success Criteria](#4-wcag-21-aa--all-50-success-criteria)
5. [WCAG 2.2 New Success Criteria (9 Added)](#5-wcag-22-new-success-criteria-9-added)
6. [EN 301 549 Extra Requirements Beyond WCAG](#6-en-301-549-extra-requirements-beyond-wcag)
7. [German-Specific Requirements (BITV 2.0 / BFSG)](#7-german-specific-requirements-bitv-20--bfsg)
8. [HTML Structural Checklist](#8-html-structural-checklist)
9. [CSS Accessibility Checklist](#9-css-accessibility-checklist)
10. [JavaScript / ARIA / Interactive Widgets Checklist](#10-javascript--aria--interactive-widgets-checklist)
11. [Forms Checklist](#11-forms-checklist)
12. [Images and Media Checklist](#12-images-and-media-checklist)
13. [Navigation and Focus Management](#13-navigation-and-focus-management)
14. [Color and Contrast Reference Tables](#14-color-and-contrast-reference-tables)
15. [Keyboard Interaction Patterns](#15-keyboard-interaction-patterns)
16. [Screen Reader Compatibility](#16-screen-reader-compatibility)
17. [Mandatory Legal Documents on the Site](#17-mandatory-legal-documents-on-the-site)
18. [Testing Protocol](#18-testing-protocol)
19. [AI Audit Checklist — Machine-Readable](#19-ai-audit-checklist--machine-readable)
20. [Reference Links](#20-reference-links)

---

## 1. Legal Framework Matrix

| Law / Regulation | Jurisdiction | Applies To | Technical Standard | Enforcement Started | Penalties |
|---|---|---|---|---|---|
| **ADA Title II** (DOJ Final Rule, Apr 2024) | USA | State & local governments | WCAG 2.1 Level AA | June 2024 (compliance: Apr 2027 / Apr 2028) | DOJ enforcement, private lawsuits, damages |
| **ADA Title III** | USA | Private businesses open to the public (courts increasingly apply to websites) | WCAG 2.1 AA (de facto, ~4,605 federal suits in 2024) | Ongoing | Private lawsuits, attorneys' fees |
| **Section 508** (Rehabilitation Act) | USA | Federal agencies & their contractors | WCAG 2.0 Level AA (update to 2.2 expected ~2026) | 1998 (ICT refresh 2018) | Agency audits, procurement bar |
| **EU Web Accessibility Directive (WAD)** (2016/2102) | EU | Public sector websites & apps | EN 301 549 v3.2.1 → WCAG 2.1 AA | Sep 2019 (websites) / Jun 2021 (apps) | Member state audits |
| **European Accessibility Act (EAA)** (2019/882) | EU | Private sector: e-commerce, banking, transport, telecoms, ebooks, media | EN 301 549 v3.2.1 → WCAG 2.1 AA | **28 June 2025** | Up to €100,000 or 4% annual revenue |
| **BGG** (Behindertengleichstellungsgesetz) | Germany | Federal public authorities | EN 301 549 / BITV 2.0 | 2002 | Monitoring, dispute resolution |
| **BITV 2.0** | Germany | Federal public sector websites & apps | EN 301 549 v3.2.1 → WCAG 2.1 AA + 38 extra criteria | 2019 | Monitoring + BGG disputes |
| **BFSG** (Barrierefreiheitsstärkungsgesetz) | Germany | Private sector (B2C) e-commerce, banking, transport | EN 301 549 → WCAG 2.1 AA | **28 June 2025** | Market surveillance, fines, injunctions |

### Who is EXEMPT?

**Germany (BFSG):** Micro-enterprises: fewer than 10 employees AND annual turnover ≤ €2 million.  
**EU EAA:** Same micro-enterprise exemption. Services contracted before 28 June 2025 have grace until 27 June 2030.  
**USA Section 508:** Private companies unless they are federal contractors or receive federal funding.  
**USA ADA Title III:** Applies to all businesses open to the public, but no private right of action for damages in some circuits without prior notice.

### Practical Rule for Developers

> **Build to WCAG 2.2 Level AA.** This exceeds all current legal minimums and protects against upcoming standard updates (EN 301 549 v4.1.1 expected 2026 will embed WCAG 2.2). If serving German public sector, also satisfy BITV 2.0 extras (Sign Language video, Easy Language, accessibility statement).

---

## 2. Standards Architecture

```
WCAG 2.1 AA (W3C)
    │  legally embedded in
    ▼
EN 301 549 v3.2.1 (ETSI/CEN/CENELEC)
    │  Chapter 9 = web, Chapter 10 = documents, Chapter 11 = non-web SW
    │  implemented by
    ├── EU WAD (public sector)
    ├── EU EAA → national laws → BFSG (Germany private), etc.
    └── BITV 2.0 (Germany public) + 38 extra criteria

WCAG 2.2 AA (W3C, Oct 2023)
    │  superset of WCAG 2.1 — adds 9 new SC, removes 1 (4.1.1)
    │  expected in EN 301 549 v4.1.1 (2026)
    └── Best practice NOW; courts increasingly cite it

Section 508 (US)
    └── References WCAG 2.0 AA; harmonized with EN 301 549 structure
```

---

## 3. The POUR Principles Expanded

All WCAG success criteria fall under four principles:

| Principle | Meaning | Failure Example |
|---|---|---|
| **Perceivable** | Info and UI must be presentable to users in ways they can perceive | Image without `alt`, video without captions |
| **Operable** | UI components and navigation must be operable | Button only clickable with mouse, no keyboard access |
| **Understandable** | Info and operation must be understandable | Form error only shown in red with no text |
| **Robust** | Content must be robust enough to be interpreted by assistive technologies | Missing ARIA roles, invalid HTML that breaks screen readers |

---

## 4. WCAG 2.1 AA — All 50 Success Criteria

Levels: **A** = minimum, **AA** = required by law, **AAA** = voluntary best practice.  
This section covers all A + AA criteria that EN 301 549 mandates for websites (Table A.1, Annex A).

### 4.1 Perceivable

#### 1.1 Text Alternatives

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **1.1.1** Non-text Content | A | All non-text content has a text alternative | `alt="description"` on `<img>`; `aria-label` on icon buttons; `role="presentation"` + empty `alt=""` on decorative images |

#### 1.2 Time-based Media

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **1.2.1** Audio-only / Video-only (pre-recorded) | A | Provide transcript (audio-only) or audio description (video-only) | Link to text transcript below media |
| **1.2.2** Captions (pre-recorded) | A | Captions for all pre-recorded audio in video | Closed captions file (.vtt) in `<track kind="captions">` |
| **1.2.3** Audio Description or Transcript (pre-recorded) | A | Audio description OR text alternative for pre-recorded video | `<track kind="descriptions">` or extended transcript |
| **1.2.4** Captions (live) | AA | Live captions for live audio content in video | Live caption service or auto-captions with human monitoring |
| **1.2.5** Audio Description (pre-recorded) | AA | Audio description for all pre-recorded video | Second audio track describing visual content |

#### 1.3 Adaptable

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **1.3.1** Info and Relationships | A | Structure/relationships conveyed through presentation can be programmatically determined | Use semantic HTML: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `<h1>`–`<h6>`, `<table>` with `<th scope>`, `<ul>`/`<ol>` for lists |
| **1.3.2** Meaningful Sequence | A | Reading order makes sense when linearized | DOM order matches visual reading order; avoid CSS-only reordering that breaks tab flow |
| **1.3.3** Sensory Characteristics | A | Instructions do not rely solely on shape, color, size, location, etc. | "Click the green button" → "Click the Submit button" |
| **1.3.4** Orientation | AA | Content not restricted to single orientation | No CSS `orientation: landscape` lock; avoid `screen.orientation.lock()` |
| **1.3.5** Identify Input Purpose | AA | Input purpose of form fields can be programmatically determined | Use HTML autocomplete attributes: `autocomplete="name"`, `"email"`, `"street-address"`, etc. |

#### 1.4 Distinguishable

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **1.4.1** Use of Color | A | Color not the only visual means of conveying information | Add icon, pattern, or text label alongside color |
| **1.4.2** Audio Control | A | Mechanism to pause/stop/control volume of auto-playing audio | Provide visible play/pause control; do not auto-play audio > 3 seconds by default |
| **1.4.3** Contrast (Minimum) | AA | Normal text: 4.5:1; large text (≥ 18pt or ≥ 14pt bold): 3:1 | Use contrast checker tools; see Section 14 for reference values |
| **1.4.4** Resize Text | AA | Text can be resized to 200% without loss of content/functionality | Use relative units (`rem`, `em`, `%`); test with browser zoom at 200% |
| **1.4.5** Images of Text | AA | No images of text (except logos) | Use real text with CSS styling; SVG text is acceptable |
| **1.4.10** Reflow | AA | Content reflows to single column at 320px wide (400% zoom) without horizontal scrolling | Responsive design; CSS flexbox/grid; no fixed widths for text containers; test at 1280px wide at 400% zoom |
| **1.4.11** Non-text Contrast | AA | UI components and graphical objects: 3:1 contrast against adjacent colors | Input borders, focus indicators, chart elements, custom checkboxes must meet 3:1 |
| **1.4.12** Text Spacing | AA | No loss of content when: line-height ≥ 1.5×, letter-spacing ≥ 0.12em, word-spacing ≥ 0.16em, paragraph spacing ≥ 2×font-size | Do not use `overflow: hidden` on text containers with fixed heights; use `min-height` |
| **1.4.13** Content on Hover or Focus | AA | Tooltip/popover content: dismissible, hoverable, persistent | Tooltip must stay visible when user moves mouse to it; Escape dismisses it |

### 4.2 Operable

#### 2.1 Keyboard Accessible

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **2.1.1** Keyboard | A | All functionality available via keyboard | Every interactive element reachable with Tab; activated with Enter/Space; no keyboard traps outside modals |
| **2.1.2** No Keyboard Trap | A | Keyboard focus not trapped in a component | Modal focus trapping is correct (trap INSIDE modal); provide Escape to close |
| **2.1.4** Character Key Shortcuts | A | Single-character keyboard shortcuts can be turned off, remapped, or only active on focus | If implementing keyboard shortcuts, provide settings to disable them |

#### 2.2 Enough Time

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **2.2.1** Timing Adjustable | A | Session timeouts: warn 20 seconds before, allow extend/turn-off | Show timeout warning dialog with `role="alertdialog"` |
| **2.2.2** Pause, Stop, Hide | A | Moving, blinking, scrolling content: mechanism to pause/stop/hide | Carousels, marquees, animated elements need a pause button |

#### 2.3 Seizures and Physical Reactions

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **2.3.1** Three Flashes or Below Threshold | A | No content flashes more than 3 times per second | Avoid rapid animations; test with PEAT tool if uncertain |

#### 2.4 Navigable

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **2.4.1** Bypass Blocks | A | Mechanism to skip repeated content | Skip link as first focusable element: `<a href="#main" class="skip-link">Skip to main content</a>` |
| **2.4.2** Page Titled | A | Web pages have descriptive titles | `<title>Page Name — Site Name</title>` (unique per page) |
| **2.4.3** Focus Order | A | Focus order preserves meaning and operability | Logical DOM order; avoid `tabindex` values > 0 |
| **2.4.4** Link Purpose (in Context) | A | Each link's purpose can be determined from link text or context | "Read more" → "Read more about [Article Title]"; use `aria-label` to supplement |
| **2.4.5** Multiple Ways | AA | More than one way to locate a page (except if step in process) | Provide search + site map OR search + navigation menu |
| **2.4.6** Headings and Labels | AA | Headings and labels are descriptive | No "Untitled" headings; no generic "Name" label on multiple fields |
| **2.4.7** Focus Visible | AA | Keyboard focus indicator is visible | Never `outline: none` without a custom visible replacement; see Section 9 for CSS patterns |

#### 2.5 Input Modalities

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **2.5.1** Pointer Gestures | A | Multipoint/path-based gestures have single-pointer alternative | Slider draggable also has +/- buttons |
| **2.5.2** Pointer Cancellation | A | Single-pointer: avoid activating on down-event, allow abort/undo | Use `click`/`mouseup` events, not `mousedown`/`touchstart` for activation |
| **2.5.3** Label in Name | A | Accessible name includes visible label text | `aria-label` must contain the visible label text verbatim or start with it |
| **2.5.4** Motion Actuation | A | Functionality via device motion has alternative; can be disabled | Shake-to-refresh: provide button alternative; respect `prefers-reduced-motion` |

### 4.3 Understandable

#### 3.1 Readable

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **3.1.1** Language of Page | A | Default human language of page is programmatically determinable | `<html lang="en">` (ISO 639-1 code) |
| **3.1.2** Language of Parts | AA | Language of passages in a different language is identified | `<span lang="de">Auf Wiedersehen</span>` |

#### 3.2 Predictable

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **3.2.1** On Focus | A | No context change on receiving focus | No redirect or form submit triggered solely by receiving focus |
| **3.2.2** On Input | A | No unexpected context change on input (unless user warned) | Auto-submitting form on radio change: warn user in advance |
| **3.2.3** Consistent Navigation | AA | Navigation repeated across pages is consistent | Site navigation appears in same relative order on every page |
| **3.2.4** Consistent Identification | AA | Components with same function are identified consistently | Search field always labeled "Search"; Back button always says "Back" |

#### 3.3 Input Assistance

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **3.3.1** Error Identification | A | Input errors described in text | `role="alert"` or `aria-describedby` linking to error message; error described specifically |
| **3.3.2** Labels or Instructions | A | Labels or instructions provided for user input | Every `<input>` has associated `<label>`; required fields marked with text (not only asterisk) |
| **3.3.3** Error Suggestion | AA | If error detected and suggestions known, suggest correction | "Invalid email" → "Please enter a valid email in the format name@example.com" |
| **3.3.4** Error Prevention (Legal, Financial, Data) | AA | For legal/financial submissions: reversible, checkable, or confirmable | Add confirmation step/summary before final form submission |

### 4.4 Robust

#### 4.1 Compatible

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **4.1.1** Parsing | A | (Largely obsolete in WCAG 2.2, but still in 2.1 and EN 301 549) — Valid HTML, no duplicate IDs | Run HTML validator; ensure unique IDs; properly nested elements |
| **4.1.2** Name, Role, Value | A | All UI components: name and role determinable, states/values settable | Custom controls use appropriate ARIA roles + states; native HTML preferred |
| **4.1.3** Status Messages | AA | Status messages programmatically determinable without focus | `role="status"` for non-urgent updates; `role="alert"` for errors |

---

## 5. WCAG 2.2 New Success Criteria (9 Added)

WCAG 2.2 was published October 2023. It adds 9 new success criteria and removes 4.1.1 (Parsing). While EN 301 549 v3.2.1 currently embeds WCAG 2.1, EN 301 549 v4.1.1 (expected 2026) will embed WCAG 2.2. Implement now for future-proofing and best practice.

| SC | Level | Requirement | Implementation |
|---|---|---|---|
| **2.4.11** Focus Appearance (Minimum) | AA | Focus indicator: at least 2 CSS pixels perimeter, contrast ≥ 3:1 between focused and unfocused states | `outline: 3px solid #0052cc; outline-offset: 2px;` — see CSS section |
| **2.4.12** Focus Appearance (Enhanced) | AAA | Focus indicator: full component perimeter, minimum area, contrast ≥ 4.5:1 | Voluntary; follow same pattern with stronger contrast |
| **2.4.13** Focus Appearance *(in 2.2, replaces 2.4.11/12 naming)* | AA | See 2.4.11 above | — |
| **2.5.7** Dragging Movements | AA | Any functionality using dragging has single-pointer alternative | Drag-to-reorder list items also has up/down buttons |
| **2.5.8** Target Size (Minimum) | AA | Touch targets at least 24×24 CSS pixels (with exceptions) | Recommended: 44×44px; minimum: 24×24px or sufficient spacing |
| **3.2.6** Consistent Help | A | Help mechanisms (contact info, live chat) appear in same relative order across pages | Keep help links/icons in consistent position in every page template |
| **3.3.7** Redundant Entry | A | Information previously entered not required to be entered again (same session, same process) | Auto-fill billing = shipping address; do not clear forms on error |
| **3.3.8** Accessible Authentication (Minimum) | AA | Cognitive function test (like CAPTCHA) is not sole authentication method OR alternative provided | Provide email link, passkey, or copy-paste-friendly CAPTCHA; do not require memorization or transcription without alternative |
| **3.3.9** Accessible Authentication (Enhanced) | AAA | No cognitive function test at any authentication step | Voluntary |

> **Note on 4.1.1 removal:** WCAG 2.2 removes SC 4.1.1 (Parsing) because modern browser parsing makes it largely obsolete. EN 301 549 v3.2.1 still includes it. Validate HTML anyway — it's good practice.

---

## 6. EN 301 549 Extra Requirements Beyond WCAG

EN 301 549 v3.2.1 Table A.1 lists additional clauses for websites beyond WCAG 2.1. These are mandatory under WAD/EAA/BFSG.

### 6.1 Chapter 5 — Generic Requirements

| Clause | Requirement | Implementation |
|---|---|---|
| **5.2** Activation of accessibility features | Accessibility features must be activatable without requiring accessibility | Do not gate "high contrast mode" behind a control that only works with mouse |
| **5.3** Biometrics | Where biometrics used, alternative method must exist | Face ID / fingerprint login must offer PIN/password alternative |
| **5.4** Preservation of accessibility information | Accessibility info must survive conversion between formats | PDF exports must retain heading structure, alt text, table headers |
| **5.5** Operable parts | Physical parts of ICT operable with one hand without fine motor | Not typically web, but relevant to hardware-controlled web kiosks |
| **5.6** Locking or toggle controls | Status of locking keys (Caps Lock, Num Lock) programmatically determinable | Inform user via visual or auditory indicator |

### 6.2 Chapter 6 — Two-Way Voice Communication (if applicable)

| Clause | Requirement |
|---|---|
| **6.1** Audio bandwidth | Frequency response 100 Hz – 8500 Hz (if telephony web app) |
| **6.2** Real-time text (RTT) | Web telephony must support real-time text alongside voice |
| **6.5** Video communication | If video call: min 20fps, 320×240 resolution for sign language |

### 6.3 Chapter 7 — ICT with Video Capabilities

| Clause | Requirement | Implementation |
|---|---|---|
| **7.1.1** Captioning playback | Video player must be able to display captions | Use `<video>` with `<track kind="captions">`; custom player must expose caption controls |
| **7.1.2** Captioning synchronization | Captions within ±100ms of audio | Validate .vtt file timing |
| **7.1.3** Preservation of captioning | Captions preserved through processing pipeline | Do not strip `<track>` on video re-encode |
| **7.2.1** Audio description playback | Player supports audio description track | Second audio track or extended description file |
| **7.3** User controls for captions/AD | Caption and audio description controls at same interaction level as other player controls | Do not hide behind settings menu |

### 6.4 Chapter 9 — Web (WCAG Reference)

EN 301 549 Chapter 9 directly references WCAG 2.1 A and AA. All criteria from Section 4 of this guide apply here.

### 6.5 Chapter 11 — Non-Web Software (if building PWA / Electron)

| Clause | Notes |
|---|---|
| **11.x** | Mirrors WCAG adapted for software contexts. Platform accessibility APIs must be used. |

### 6.6 Chapter 12 — Documentation and Support Services

| Clause | Requirement |
|---|---|
| **12.1.1** Accessibility and compatibility features documented | Publish accessibility statement describing features and known issues |
| **12.1.2** Accessible documentation | Product documentation itself must be accessible (PDF must be tagged, etc.) |
| **12.2.2** Support services | If technical support is offered, it must be accessible (not only phone-only for deaf users) |

---

## 7. German-Specific Requirements (BITV 2.0 / BFSG)

### 7.1 BITV 2.0 Additional Requirements (Public Sector Only)

These 38 additional criteria apply to German federal public sector sites but not private sector (BFSG).

| Requirement | Detail |
|---|---|
| **German Sign Language (DGS) video** | Homepage must include key information in Deutsche Gebärdensprache video (DGS) |
| **Easy Language (Leichte Sprache)** | Homepage must provide key information in Leichte Sprache (simplified German, max CEFR A2 level) |
| **BITV Self-Test** | Self-evaluation mandatory; available at https://studio.bitvtest.de |
| **Accessibility Statement (Erklärung zur Barrierefreiheit)** | More detailed than EAA/WAD version; see Section 17 |

### 7.2 BFSG Requirements (Private Sector — E-Commerce, Banking, etc.)

| Requirement | Detail |
|---|---|
| **Scope** | Applies to e-commerce websites/apps offering consumer contracts; also applies to banking, transport services |
| **Technical standard** | EN 301 549 → WCAG 2.1 Level A + AA mandatory; AAA voluntary |
| **Accessibility information** | Per §14 BFSG + Annex 3: must publish accessibility info in GTC (AGB) or a clearly visible location; this info itself must be accessible |
| **Feedback mechanism** | Users must be able to report accessibility barriers and receive response |
| **Exceptions** | Pre-existing content (before 28 June 2025) if classified as archive; third-party content not controlled by operator; online maps; |
| **Enforcement** | Market surveillance authorities (Marktüberwachungsbehörden) can investigate, order remediation, impose fines |

### 7.3 Accessibility Statement Requirements (all German entities under WAD/BFSG)

Under WAD/EAA, an Accessibility Statement must include:
- Compliance status: fully, partially, or not compliant
- Non-accessible content with reasons (disproportionate burden, not in scope, technical limitation)
- Accessible alternatives where non-accessible content exists
- Contact for feedback and reporting barriers (Rückmeldung/Feedback)
- Link to enforcement procedure (in Germany: Schlichtungsstelle or Ombudsstelle)
- Date of last review

---

## 8. HTML Structural Checklist

### 8.1 Document Structure

```html
<!DOCTYPE html>
<html lang="en"><!-- REQUIRED: ISO 639-1 language code; use lang="de" for German -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Do NOT use user-scalable=no — this violates 1.4.4 -->
  <title>Unique Page Title — Site Name</title><!-- SC 2.4.2: unique, descriptive -->
  <meta name="description" content="Page description for search engines">
</head>
<body>

  <!-- SC 2.4.1: Skip link — FIRST focusable element -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <header role="banner"><!-- landmark for screen readers -->
    <nav aria-label="Primary navigation"><!-- SC 2.4.1, 3.2.3 -->
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <!-- aria-current="page" on active link -->
        <li><a href="/contact" aria-current="page">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content"><!-- landmark; receives skip link focus -->
    
    <h1>Main Page Heading</h1><!-- One <h1> per page; do not skip heading levels -->
    
    <section aria-labelledby="section1-heading">
      <h2 id="section1-heading">Section Title</h2>
      <!-- h3, h4, h5, h6 as needed — never skip levels -->
    </section>

  </main>

  <aside aria-label="Related links"><!-- complementary landmark -->
  </aside>

  <footer role="contentinfo">
    <!-- Footer content -->
    <nav aria-label="Footer navigation"><!-- separate nav landmark -->
    </nav>
  </footer>

</body>
</html>
```

### 8.2 Landmark Roles Checklist

| Landmark | HTML Element | ARIA Role | Notes |
|---|---|---|---|
| Header | `<header>` | `banner` | One per page at top level |
| Navigation | `<nav>` | `navigation` | Multiple allowed; use `aria-label` to distinguish |
| Main content | `<main>` | `main` | One per page |
| Complementary | `<aside>` | `complementary` | Sidebars, callouts |
| Footer | `<footer>` | `contentinfo` | One per page at top level |
| Search | `<form role="search">` | `search` | Site search form |
| Form | `<section>` | `form` | Only when no other landmark fits |

### 8.3 Heading Hierarchy Rules

```html
<!-- CORRECT: sequential, no skipping -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
    <h3>Another Subsection</h3>
  <h2>Another Section</h2>

<!-- WRONG: skipping from h1 to h3 -->
<h1>Page Title</h1>
  <h3>Section</h3><!-- violates 1.3.1 -->
```

### 8.4 Tables

```html
<!-- Data table — REQUIRED markup -->
<table>
  <caption>Monthly Sales Figures</caption><!-- describes table purpose -->
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Revenue</th>
      <th scope="col">Units</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th><!-- row header -->
      <td>€12,000</td>
      <td>240</td>
    </tr>
  </tbody>
</table>

<!-- Layout tables: add role="presentation" and no <th> elements -->
<table role="presentation">...</table>
```

### 8.5 Lists

```html
<!-- Use semantic list elements — SC 1.3.1 -->
<ul><!-- unordered list -->
  <li>Item</li>
</ul>

<ol><!-- ordered/sequential list -->
  <li>Step 1</li>
</ol>

<dl><!-- definition/description list -->
  <dt>Term</dt>
  <dd>Definition</dd>
</dl>
```

---

## 9. CSS Accessibility Checklist

### 9.1 Focus Indicators — CRITICAL

```css
/* NEVER do this: */
* { outline: none; } /* VIOLATION of SC 2.4.7 and WCAG 2.2 SC 2.4.11 */
:focus { outline: none; } /* VIOLATION */

/* WCAG 2.2 SC 2.4.11 compliant focus style */
/* Minimum: 2px perimeter, 3:1 contrast between focused and unfocused */
:focus-visible {
  outline: 3px solid #0052cc;    /* high contrast blue */
  outline-offset: 2px;           /* keeps outline outside element */
  border-radius: 2px;            /* optional, matches element shape */
}

/* Dark background variation */
.dark-bg :focus-visible {
  outline: 3px solid #ffffff;
  outline-offset: 2px;
}

/* High contrast mode support */
@media (forced-colors: active) {
  :focus-visible {
    outline: 3px solid ButtonText;
  }
}
```

### 9.2 Color Contrast — Reference

```css
/* Approved high-contrast text color pairs (4.5:1 minimum) */

/* Black text on white: 21:1 ✓ */
body { color: #000000; background: #ffffff; }

/* Dark gray on white: 12.6:1 ✓ */
.body-text { color: #1a1a1a; background: #ffffff; }

/* WCAG AA body text — minimum approved dark blue on white: 7.7:1 ✓ */
.link { color: #0052cc; }

/* Large text (≥18pt/24px normal, ≥14pt/18.67px bold): 3:1 minimum */
h1, h2 { color: #595959; } /* 7.0:1 on white ✓ */

/* DANGER ZONES — requires testing: */
/* Light gray on white (#767676 on #fff = exactly 4.5:1 — borderline) */
/* Orange on white (#ff6600 on #fff = 3.0:1 — fails for body text, passes for large) */
```

### 9.3 Typography and Reflow

```css
/* SC 1.4.4 Resize Text — use relative units */
html { font-size: 100%; } /* = 16px in most browsers */
body { font-size: 1rem; }
h1 { font-size: 2rem; }

/* SC 1.4.10 Reflow — no fixed widths that cause horizontal scroll */
.container {
  max-width: 1200px;
  width: 100%;          /* not: width: 1200px */
  padding: 0 1rem;
}

/* SC 1.4.12 Text Spacing — content must survive these overrides */
/* Test by injecting this bookmarklet or CSS: */
/* p { line-height: 1.5 !important; letter-spacing: 0.12em !important;
       word-spacing: 0.16em !important; margin-bottom: 2em !important; } */

/* Correct approach — never hard-code container heights for text: */
.card { min-height: 100px; } /* not: height: 100px; overflow: hidden; */
```

### 9.4 Motion and Animation

```css
/* SC 2.3.1 and WCAG 2.2 — always honor reduced motion preference */
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

/* Provide motion only if user has not requested reduced motion */
@media (prefers-reduced-motion: no-preference) {
  .animated-element {
    transition: transform 0.3s ease;
  }
}
```

### 9.5 Hiding Content Correctly

```css
/* Visually hidden but accessible to screen readers (for skip links, SR-only text) */
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

/* Show on focus (for skip links) */
.skip-link:focus {
  position: static;
  width: auto;
  height: auto;
  overflow: visible;
  clip: auto;
  white-space: normal;
  /* and add visible styles: */
  background: #000;
  color: #fff;
  padding: 0.5rem 1rem;
  display: block;
}

/* Hidden from everyone including screen readers */
.hidden { display: none; }          /* removes from AT */
.invisible { visibility: hidden; }   /* removes from AT */

/* WRONG — hides visually but may still be read by SR: */
.bad-hide { opacity: 0; }           /* still in tab order! */
.bad-hide { position: absolute; left: -9999px; } /* still in tab order! */
```

### 9.6 High Contrast Mode

```css
/* Support Windows High Contrast Mode / Forced Colors */
@media (forced-colors: active) {
  /* Borders become visible */
  button { border: 2px solid ButtonText; }
  
  /* Custom decorative icons: hide and use text alternative */
  .icon-only::before {
    forced-color-adjust: none; /* preserve custom colors */
  }
  
  /* Ensure focus indicator survives */
  :focus-visible {
    outline: 3px solid Highlight;
  }
}
```

### 9.7 Target Size (WCAG 2.2 SC 2.5.8)

```css
/* Minimum 24×24 CSS pixels for interactive targets */
button,
a,
[role="button"],
input[type="checkbox"],
input[type="radio"] {
  min-width: 24px;
  min-height: 24px;
}

/* Recommended for touch: 44×44px */
.touch-target {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* If element is smaller, use transparent padding to increase hit area */
.small-icon-button {
  padding: 10px; /* expands click area */
}
```

---

## 10. JavaScript / ARIA / Interactive Widgets Checklist

### 10.1 ARIA Usage Rules

1. **First rule of ARIA:** Do not use ARIA if a native HTML element exists.
2. **Second rule:** Do not change native semantics unless absolutely necessary.
3. **Do not** add `role="button"` to `<div>` when you can use `<button>`.
4. All ARIA roles require corresponding keyboard behavior (see Section 15).

### 10.2 Common ARIA Patterns

```javascript
// ============================================================
// MODAL / DIALOG — SC 2.1.2 (No Keyboard Trap), 4.1.2
// ============================================================

class AccessibleModal {
  constructor(triggerEl, modalEl) {
    this.trigger = triggerEl;
    this.modal = modalEl;
    this.focusableSelectors = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
  }

  open() {
    this.modal.removeAttribute('hidden');
    this.modal.setAttribute('aria-modal', 'true');
    this.modal.setAttribute('role', 'dialog');
    // aria-labelledby must point to modal heading
    
    // Trap focus inside modal
    this._trapFocus();
    
    // Move focus to first focusable element or modal itself
    const firstFocusable = this.modal.querySelector(this.focusableSelectors);
    (firstFocusable || this.modal).focus();
    
    // Prevent background scroll
    document.body.setAttribute('aria-hidden', 'false'); // modal not hidden
    document.querySelector('#main-content').setAttribute('aria-hidden', 'true');
  }

  close() {
    this.modal.setAttribute('hidden', '');
    document.querySelector('#main-content').removeAttribute('aria-hidden');
    this.trigger.focus(); // Return focus to trigger
    this._removeFocusTrap();
  }

  _trapFocus() {
    this.modal.addEventListener('keydown', this._handleKeydown.bind(this));
  }

  _handleKeydown(e) {
    if (e.key === 'Escape') { this.close(); return; }
    if (e.key !== 'Tab') return;
    
    const focusable = Array.from(this.modal.querySelectorAll(this.focusableSelectors));
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === first) { e.preventDefault(); last.focus(); }
    } else {
      if (document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  }
}
```

```javascript
// ============================================================
// ACCORDION — SC 2.1.1, 4.1.2
// ============================================================

// HTML structure:
// <div class="accordion">
//   <h3>
//     <button aria-expanded="false" aria-controls="panel1" id="btn1">Title</button>
//   </h3>
//   <div id="panel1" role="region" aria-labelledby="btn1" hidden>Content</div>
// </div>

function toggleAccordion(btn) {
  const expanded = btn.getAttribute('aria-expanded') === 'true';
  const panel = document.getElementById(btn.getAttribute('aria-controls'));
  
  btn.setAttribute('aria-expanded', String(!expanded));
  if (expanded) {
    panel.setAttribute('hidden', '');
  } else {
    panel.removeAttribute('hidden');
  }
}
```

```javascript
// ============================================================
// TABS — SC 2.1.1, 4.1.2; follows ARIA Authoring Practices
// ============================================================

// HTML:
// <div role="tablist" aria-label="Product Information">
//   <button role="tab" aria-selected="true" aria-controls="panel1" id="tab1" tabindex="0">Overview</button>
//   <button role="tab" aria-selected="false" aria-controls="panel2" id="tab2" tabindex="-1">Specs</button>
// </div>
// <div role="tabpanel" id="panel1" aria-labelledby="tab1" tabindex="0">...</div>
// <div role="tabpanel" id="panel2" aria-labelledby="tab2" tabindex="0" hidden>...</div>

// Arrow key navigation within tablist
tablist.addEventListener('keydown', (e) => {
  const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
  const idx = tabs.indexOf(document.activeElement);
  
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
    tabs[(idx + 1) % tabs.length].focus();
    e.preventDefault();
  }
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    tabs[(idx - 1 + tabs.length) % tabs.length].focus();
    e.preventDefault();
  }
  if (e.key === 'Home') { tabs[0].focus(); e.preventDefault(); }
  if (e.key === 'End') { tabs[tabs.length - 1].focus(); e.preventDefault(); }
});
```

```javascript
// ============================================================
// LIVE REGIONS — SC 4.1.3 Status Messages
// ============================================================

// For non-critical updates (shopping cart count, save status):
// <div aria-live="polite" aria-atomic="true" id="status-message"></div>

// For errors/urgent:
// <div role="alert" aria-live="assertive" id="error-message"></div>

function announceToScreenReader(message, isAlert = false) {
  const region = document.createElement('div');
  region.setAttribute('aria-live', isAlert ? 'assertive' : 'polite');
  region.setAttribute('aria-atomic', 'true');
  region.className = 'visually-hidden';
  document.body.appendChild(region);
  
  // Delay allows AT to detect the region before content is added
  setTimeout(() => { region.textContent = message; }, 100);
  setTimeout(() => { region.remove(); }, 3000);
}

// Usage:
announceToScreenReader('Item added to cart'); // polite
announceToScreenReader('Session expiring in 2 minutes', true); // alert
```

### 10.3 Custom Checkbox / Radio

```html
<!-- PREFERRED: use native elements -->
<label>
  <input type="checkbox" name="agree" required>
  I agree to the terms
</label>

<!-- If custom styled checkbox is required: -->
<label class="custom-checkbox">
  <input type="checkbox" class="visually-hidden" name="agree">
  <span class="checkbox-visual" aria-hidden="true"></span>
  I agree to the terms
</label>
```

```css
/* Custom checkbox visual — must show state visually */
.custom-checkbox input:focus-visible + .checkbox-visual {
  outline: 3px solid #0052cc;
  outline-offset: 2px;
}
.custom-checkbox input:checked + .checkbox-visual {
  background-color: #0052cc;
  /* Add check mark via content or SVG */
}
```

### 10.4 Tooltip (SC 1.4.13)

```javascript
// Tooltip must be:
// 1. Triggered by both hover AND focus
// 2. Dismissible with Escape
// 3. Hoverable (user can move mouse to tooltip)
// 4. Persistent (stays open until dismissed)

// HTML:
// <button aria-describedby="tip1">?</button>
// <div role="tooltip" id="tip1" hidden>Help text here</div>

function initTooltip(trigger, tooltip) {
  let hideTimeout;
  
  const show = () => {
    clearTimeout(hideTimeout);
    tooltip.removeAttribute('hidden');
  };
  
  const hide = (delay = 300) => {
    hideTimeout = setTimeout(() => tooltip.setAttribute('hidden', ''), delay);
  };
  
  trigger.addEventListener('mouseenter', show);
  trigger.addEventListener('mouseleave', () => hide());
  trigger.addEventListener('focus', show);
  trigger.addEventListener('blur', () => hide());
  trigger.addEventListener('keydown', (e) => { if (e.key === 'Escape') hide(0); });
  
  tooltip.addEventListener('mouseenter', () => clearTimeout(hideTimeout));
  tooltip.addEventListener('mouseleave', () => hide());
}
```

### 10.5 Dynamic Content Updates

```javascript
// When content updates dynamically (SPA navigation, filtered results):

// 1. Update page title
document.title = `${newPageName} — ${siteName}`;

// 2. Announce page change to SR users
announceToScreenReader(`Navigated to ${newPageName}`);

// 3. Move focus appropriately
document.getElementById('main-content').focus(); // or first heading
// Note: main must have tabindex="-1" for programmatic focus:
// <main id="main-content" tabindex="-1">

// 4. Update document language if content language changes
document.documentElement.setAttribute('lang', newLang);
```

---

## 11. Forms Checklist

### 11.1 Labels

```html
<!-- REQUIRED: Every input must have a label -->

<!-- Method 1: Explicit label (preferred) -->
<label for="email">Email address <span aria-hidden="true">*</span></label>
<input type="email" id="email" name="email" required
       autocomplete="email"
       aria-required="true"
       aria-describedby="email-hint email-error">
<div id="email-hint">We'll never share your email.</div>
<div id="email-error" role="alert" aria-live="polite"></div>

<!-- Method 2: Wrapped label -->
<label>
  Email address
  <input type="email" name="email" autocomplete="email">
</label>

<!-- Method 3: aria-label (when no visible label is possible) -->
<input type="search" aria-label="Search products" placeholder="Search...">
<!-- Note: placeholder alone is NOT a label — insufficient for SC 1.3.1 -->

<!-- WRONG — these are NOT labels: -->
<!-- <input placeholder="Email"> — placeholder disappears on input -->
<!-- <input title="Email"> — unreliable across AT -->
```

### 11.2 Required Fields

```html
<!-- Mark required fields: SC 3.3.2 -->
<!-- Text explanation, not only asterisk -->
<p>Fields marked with <span aria-hidden="true">*</span> 
   <span class="visually-hidden">asterisk</span> are required.</p>

<label for="name">
  Full name <span aria-hidden="true">*</span>
</label>
<input type="text" id="name" required aria-required="true"
       autocomplete="name">
```

### 11.3 Error Messages

```html
<!-- SC 3.3.1 Error Identification — describe error specifically in text -->
<!-- SC 3.3.3 Error Suggestion — tell user how to fix it -->

<label for="phone">Phone number</label>
<input type="tel" id="phone" 
       aria-describedby="phone-error"
       aria-invalid="true"><!-- add/remove dynamically on error -->
<div id="phone-error" role="alert">
  <!-- Specific error + suggestion -->
  Phone number is invalid. Please enter a 10-digit number, e.g. 030 12345678.
</div>
```

```javascript
// Inline validation pattern
function validateField(input) {
  const error = document.getElementById(input.id + '-error');
  
  if (!input.validity.valid) {
    input.setAttribute('aria-invalid', 'true');
    error.textContent = getErrorMessage(input);
    // role="alert" on error div triggers announcement
  } else {
    input.removeAttribute('aria-invalid');
    error.textContent = '';
  }
}

// Validate on blur (not on every keystroke — too disruptive)
input.addEventListener('blur', () => validateField(input));
// Also validate on submit attempt
```

### 11.4 Autocomplete Attributes (SC 1.3.5)

```html
<!-- Required for personal data input fields -->
<input autocomplete="name">           <!-- Full name -->
<input autocomplete="given-name">     <!-- First name -->
<input autocomplete="family-name">    <!-- Last name -->
<input autocomplete="email">          <!-- Email -->
<input autocomplete="tel">            <!-- Telephone -->
<input autocomplete="street-address"> <!-- Street -->
<input autocomplete="postal-code">    <!-- Post/ZIP code -->
<input autocomplete="country">        <!-- Country -->
<input autocomplete="cc-name">        <!-- Credit card name -->
<input autocomplete="cc-number">      <!-- Credit card number -->
<input autocomplete="new-password">   <!-- New password -->
<input autocomplete="current-password"><!-- Current password -->
<input autocomplete="one-time-code">  <!-- OTP -->
```

### 11.5 Authentication (WCAG 2.2 SC 3.3.8)

```html
<!-- COMPLIANT: passkey / magic link / SMS OTP -->
<!-- Users may copy-paste OTP — do not block paste events -->
<input type="text" autocomplete="one-time-code" inputmode="numeric">

<!-- If CAPTCHA must be used: provide at least 2 alternatives -->
<!-- Option 1: Audio CAPTCHA -->
<!-- Option 2: Email verification link -->
<!-- Option 3: Math puzzle (still a cognitive test but widely accepted) -->

<!-- WCAG 2.2 SC 3.3.8: No pure "remember and type" tests without alternative -->
<!-- Passkeys (WebAuthn) are the gold standard: -->
<!-- https://www.w3.org/TR/webauthn-2/ -->
```

---

## 12. Images and Media Checklist

### 12.1 Images

```html
<!-- Informative image — describe what it conveys, not what it looks like -->
<img src="chart.png" alt="Bar chart showing revenue increased 40% in Q3 2024">

<!-- Decorative image — empty alt, no title -->
<img src="divider.png" alt="" role="presentation">

<!-- Functional image (button/link) — describe the action -->
<button><img src="search.svg" alt="Search"></button>
<a href="/home"><img src="logo.png" alt="Acme Corp — Home"></a>

<!-- Complex image (chart, diagram) — alt + long description -->
<figure>
  <img src="org-chart.png" 
       alt="Organization chart — see full description below"
       aria-describedby="orgchart-desc">
  <figcaption id="orgchart-desc">
    CEO Jane Smith leads three departments: Engineering (30 staff),
    Marketing (15 staff), and Sales (20 staff)...
  </figcaption>
</figure>

<!-- SVG inline — title + desc for accessibility -->
<svg role="img" aria-labelledby="svg-title svg-desc">
  <title id="svg-title">Monthly visitors</title>
  <desc id="svg-desc">Line chart showing growth from 1,000 to 5,000 visitors 
    over 6 months from January to June 2024.</desc>
  <!-- SVG paths -->
</svg>

<!-- SVG decorative -->
<svg aria-hidden="true" focusable="false">...</svg>
<!-- Note: focusable="false" is required in some IE/Edge versions -->
```

### 12.2 Video and Audio

```html
<!-- Pre-recorded video with audio — SC 1.2.2 (captions) + 1.2.5 (audio description) -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default>
  <track kind="descriptions" src="audiodesc-en.vtt" srclang="en" label="Audio Description">
  <track kind="subtitles" src="subtitles-de.vtt" srclang="de" label="Deutsch">
  Your browser does not support the video element.
</video>

<!-- Provide transcript link near video — SC 1.2.1, 1.2.3 -->
<p><a href="transcript-video1.html">Read text transcript of this video</a></p>

<!-- Audio-only content — SC 1.2.1: provide transcript -->
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg">
</audio>
<p><a href="podcast-transcript.html">Read transcript</a></p>
```

### 12.3 VTT Caption File Format

```
WEBVTT

00:00:00.000 --> 00:00:03.500
Welcome to our product overview.

00:00:03.600 --> 00:00:07.200
Today we'll show you three key features.

NOTE: Caption best practices:
- Max 42 characters per line
- Max 2 lines per caption
- Synchronize within ±100ms (EN 301 549 clause 7.1.2)
- Include speaker identification: [SPEAKER NAME]:
- Include non-speech audio: [upbeat music]
```

---

## 13. Navigation and Focus Management

### 13.1 Skip Links

```html
<!-- Must be first focusable element in DOM -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- For complex pages, provide multiple skip links -->
<a href="#main-content" class="skip-link">Skip to main content</a>
<a href="#site-search" class="skip-link">Skip to search</a>
<a href="#primary-nav" class="skip-link">Skip to navigation</a>
```

```css
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  background: #000;
  color: #fff;
  padding: 1rem;
  z-index: 9999;
  font-size: 1rem;
  text-decoration: none;
}
.skip-link:focus {
  top: 0;
}
```

### 13.2 Breadcrumbs

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Widget X</li><!-- current page: no link -->
  </ol>
</nav>
```

### 13.3 Pagination

```html
<nav aria-label="Page navigation">
  <ul>
    <li><a href="?page=1" aria-label="Previous page">‹ Previous</a></li>
    <li><a href="?page=1" aria-label="Page 1">1</a></li>
    <li><a href="?page=2" aria-label="Page 2, current page" aria-current="page">2</a></li>
    <li><a href="?page=3" aria-label="Page 3">3</a></li>
    <li><a href="?page=3" aria-label="Next page">Next ›</a></li>
  </ul>
</nav>
```

### 13.4 Dropdown / Mega Menu

```html
<nav aria-label="Primary">
  <ul role="menubar">
    <li role="none">
      <button role="menuitem" aria-haspopup="true" aria-expanded="false" id="nav-products">
        Products
      </button>
      <ul role="menu" aria-labelledby="nav-products" hidden>
        <li role="none"><a role="menuitem" href="/products/a">Product A</a></li>
        <li role="none"><a role="menuitem" href="/products/b">Product B</a></li>
      </ul>
    </li>
  </ul>
</nav>
```

```javascript
// Keyboard: Arrow keys navigate within menu; Escape closes; Enter/Space opens
// See ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/patterns/menubar/
```

### 13.5 Consistent Navigation (SC 3.2.3)

- Navigation order must be identical across all pages.
- If navigation items are reordered, mark as intentional (e.g. user-configurable dashboard is an exception).
- Active/current page must be marked with `aria-current="page"`.

---

## 14. Color and Contrast Reference Tables

### 14.1 Contrast Ratios Required

| Content Type | Minimum Ratio | Standard |
|---|---|---|
| Normal text (< 18pt / 14pt bold) | **4.5:1** | SC 1.4.3 |
| Large text (≥ 18pt / ≥ 14pt bold) | **3:1** | SC 1.4.3 |
| UI components (input borders, chart lines) | **3:1** | SC 1.4.11 |
| Focus indicators | **3:1** (WCAG 2.2 SC 2.4.11) | SC 2.4.11 |
| Decorative / inactive / logo | Exempt | — |

### 14.2 Approved Safe Color Pairs

| Background | Text/Element | Ratio | Use |
|---|---|---|---|
| `#ffffff` | `#000000` | 21:1 | Body text on white |
| `#ffffff` | `#1a1a1a` | 16.1:1 | Body text |
| `#ffffff` | `#333333` | 12.6:1 | Body text |
| `#ffffff` | `#595959` | 7.0:1 | Body text — large headings |
| `#ffffff` | `#767676` | 4.5:1 | Minimum — normal text |
| `#ffffff` | `#0052cc` | 7.7:1 | Links |
| `#ffffff` | `#d93025` | 4.6:1 | Error red |
| `#0052cc` | `#ffffff` | 7.7:1 | Primary button |
| `#000000` | `#ffffff` | 21:1 | Dark mode |

### 14.3 Contrast Testing Tools

- **Browser DevTools:** Chrome/Firefox Accessibility Inspector shows contrast ratio
- **axe DevTools:** browser extension
- **WebAIM Contrast Checker:** https://webaim.org/resources/contrastchecker/
- **Colour Contrast Analyser:** desktop app by TPGi
- **Lighthouse:** built into Chrome DevTools (audit tab)

---

## 15. Keyboard Interaction Patterns

Every interactive widget must support keyboard interaction. Reference: ARIA Authoring Practices Guide (APG).

### 15.1 Required Key Bindings by Widget Type

| Widget | Open/Activate | Navigate | Close/Cancel | Select |
|---|---|---|---|---|
| Button | Enter, Space | — | — | Enter, Space |
| Link | Enter | — | — | — |
| Checkbox | Space (toggle) | Tab | — | Space |
| Radio group | Arrow keys | Arrow keys | — | Arrow keys |
| Select (native) | — | Arrow keys | Escape | Enter |
| Modal/Dialog | — | Tab / Shift+Tab | Escape | — |
| Dropdown menu | Enter / Space / Down | Arrow keys | Escape | Enter |
| Tabs | — | Left/Right arrows | — | — (auto-activate or Enter) |
| Accordion | Enter / Space | Tab | — | — |
| Combobox | Alt+Down | Arrow keys | Escape | Enter |
| Slider | — | Left/Right/Up/Down arrows | — | — |
| Date picker | — | Arrow keys | Escape | Enter |
| Tree view | — | Arrow keys | — | Enter / Space |
| Tooltip | Shown on focus | — | Escape | — |

### 15.2 Tab Order Rules

1. Follow visual left-to-right, top-to-bottom reading order.
2. Avoid positive `tabindex` values (tabindex="1", "2", etc.) — they hijack natural order.
3. Use `tabindex="0"` to make non-interactive elements focusable when needed.
4. Use `tabindex="-1"` for programmatic focus only (modal target, SR announcements).
5. Items with `display:none` or `visibility:hidden` or `hidden` attribute are removed from tab order automatically.
6. Inside a widget (menu, tablist), use arrow keys for internal navigation, Tab to move out.

---

## 16. Screen Reader Compatibility

### 16.1 Screen Reader / Browser Pairings (Test Matrix)

| Screen Reader | Browser | OS | Priority |
|---|---|---|---|
| NVDA + Firefox | Firefox latest | Windows | High (free, widely used) |
| NVDA + Chrome | Chrome latest | Windows | High |
| JAWS + Chrome | Chrome latest | Windows | High (corporate) |
| VoiceOver + Safari | Safari latest | macOS / iOS | High (Apple users) |
| VoiceOver + Chrome | Chrome latest | macOS | Medium |
| TalkBack + Chrome | Chrome latest | Android | High (mobile) |
| Narrator + Edge | Edge latest | Windows | Medium |

### 16.2 Common Screen Reader Gotchas

```html
<!-- Icon-only buttons: MUST have accessible name -->
<button aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false"><!-- icon --></svg>
</button>

<!-- Images inside links: do not double-announce -->
<a href="/home">
  <img src="logo.png" alt="Acme Corp">
  <!-- Do NOT also add text "Home" — alt already describes the link -->
</a>

<!-- When link AND button text is identical, disambiguate -->
<a href="/products/a" aria-label="View details for Product A">View details</a>
<a href="/products/b" aria-label="View details for Product B">View details</a>

<!-- Tables: do NOT use tables for layout -->
<!-- Screen readers announce "table, 3 columns, 10 rows" for data tables -->

<!-- Placeholder: not an alternative to a label -->
<input id="name" type="text" placeholder="Enter your full name">
<!-- Screen reader announces placeholder as hint, but label is required -->
<label for="name">Full name</label>

<!-- Dynamic regions: use aria-live regions, not just visual updates -->
<!-- Screen readers only announce changes in monitored live regions -->
```

### 16.3 ARIA Landmark Announcement by SR

| HTML | ARIA Role | NVDA | JAWS | VoiceOver |
|---|---|---|---|---|
| `<header>` | `banner` | "banner landmark" | "banner" | "banner" |
| `<nav>` | `navigation` | "navigation landmark" | "navigation region" | "navigation" |
| `<main>` | `main` | "main landmark" | "main region" | "main" |
| `<footer>` | `contentinfo` | "content info landmark" | "content info" | "content information" |
| `<aside>` | `complementary` | "complementary landmark" | "complementary region" | "complementary" |

---

## 17. Mandatory Legal Documents on the Site

### 17.1 Accessibility Statement (Required by WAD / BFSG / EAA)

**Must be linked from every page** (footer is standard). Must itself be accessible (WCAG 2.1 AA).

**Template structure:**

```html
<!-- accessibility-statement.html -->

<h1>Accessibility Statement</h1>
<p>Last updated: [DATE]</p>

<h2>Compliance Status</h2>
<p>
  [Organization Name] is [fully / partially / not] conformant with 
  EN 301 549 v3.2.1 incorporating WCAG 2.1 Level AA.
  [If partially: "Partially conformant" means some content does not 
  fully conform to the standard, as noted below.]
</p>

<h2>Non-accessible Content</h2>
<p>The following content is not fully accessible:</p>
<ul>
  <li>
    [Description of non-accessible content]
    — <strong>Reason:</strong> [Disproportionate burden / Not in scope / 
    Technical limitation]
    — <strong>Alternative:</strong> [How users can access the content another way]
  </li>
</ul>

<h2>Feedback and Contact</h2>
<p>
  If you experience accessibility barriers on our website, 
  please contact us:
</p>
<address>
  <a href="mailto:accessibility@example.com">accessibility@example.com</a><br>
  Tel: <a href="tel:+4930123456">+49 30 123456</a>
</address>
<p>We aim to respond within [5 business days].</p>

<h2>Enforcement Procedure</h2>
<!-- Germany WAD (public sector): -->
<p>
  If your report is not satisfactorily addressed, you may contact 
  the <a href="https://www.schlichtungsstelle-bgg.de/">Federal Commissioner 
  for the Interests of Persons with Disabilities Ombudsman 
  (Schlichtungsstelle nach dem BGG)</a>.
</p>
<!-- EU/EAA (private sector): link to national market surveillance authority -->
<!-- Germany BFSG: Marktüberwachungsbehörden -->

<h2>Technical Specification</h2>
<p>
  This website relies on the following technologies for conformance:
  HTML, CSS, JavaScript, WAI-ARIA.
</p>

<h2>Assessment Approach</h2>
<p>
  [Organization Name] assessed the accessibility of this website by
  [self-evaluation / commissioned third-party audit / both].
  Testing was conducted using: [list tools and screen readers].
</p>
```

### 17.2 BFSG Accessibility Information (German Private Sector §14)

In addition to the accessibility statement, German BFSG-covered entities must publish accessibility information in their General Terms & Conditions (AGB) or a clearly visible location. This information must describe:

- How accessibility requirements are met
- Which features are accessible
- Contact for accessibility queries
- Reference to applicable standard (EN 301 549)

### 17.3 Feedback Mechanism

```html
<!-- Required: Users must be able to report barriers -->
<section aria-labelledby="feedback-heading">
  <h2 id="feedback-heading">Report an Accessibility Issue</h2>
  <form action="/accessibility-feedback" method="post">
    <div>
      <label for="issue-page">Page URL where you encountered the issue</label>
      <input type="url" id="issue-page" name="page" autocomplete="url">
    </div>
    <div>
      <label for="issue-description">Description of the accessibility barrier</label>
      <textarea id="issue-description" name="description" rows="5" required></textarea>
    </div>
    <div>
      <label for="contact-email">Your email (optional, for follow-up)</label>
      <input type="email" id="contact-email" name="email" autocomplete="email">
    </div>
    <button type="submit">Submit feedback</button>
  </form>
</section>
```

---

## 18. Testing Protocol

### 18.1 Automated Testing (catches ~30-40% of issues)

```bash
# Axe-core CLI
npm install -g @axe-core/cli
axe https://yoursite.com --reporter html --outputDir ./reports

# Pa11y (WCAG 2.1 AA by default)
npm install -g pa11y
pa11y https://yoursite.com --standard WCAG2AA --reporter html > report.html

# Lighthouse CI
npm install -g @lhci/cli
lhci autorun --collect.url=https://yoursite.com

# WAVE API
# https://wave.webaim.org/api/
```

**Run automated checks on:**
- Homepage
- Representative interior page
- Contact/form page
- Login/registration
- Checkout process (if applicable)
- All unique page templates

### 18.2 Manual Testing Checklist

**Keyboard-only navigation (no mouse):**
- [ ] Tab through entire page — every interactive element reachable
- [ ] Focus indicator always visible and clearly perceivable
- [ ] No keyboard traps (except properly implemented modals)
- [ ] All functionality operable: forms submittable, menus openable, modals closeable with Escape
- [ ] Skip link works (visible on focus, jumps to main content)
- [ ] Logical tab order matches visual reading order

**Screen reader testing (NVDA/JAWS/VoiceOver):**
- [ ] Page title announced on load
- [ ] All landmark regions announced
- [ ] Headings navigable with H key (NVDA/JAWS)
- [ ] All images have meaningful alt text
- [ ] Form fields have labels and error messages announced
- [ ] Dynamic content changes announced via live regions
- [ ] Custom widgets (tabs, accordions, modals) announce role, state, and name

**Visual and zoom:**
- [ ] 200% zoom: all content readable, no overflow, no loss of functionality
- [ ] 400% zoom (1280px viewport): content reflows to single column without horizontal scroll
- [ ] Text spacing bookmarklet applied: no content hidden or overlapping
- [ ] Color contrast checked with tool for all text/UI components
- [ ] Color not the only means of conveying information

**Motion and sensory:**
- [ ] `prefers-reduced-motion`: all animations suppressed
- [ ] No content flashes more than 3 times/second
- [ ] Auto-playing audio: mechanism to pause/stop visible within 3 seconds

### 18.3 Testing Tools by Category

| Category | Tool | URL / Notes |
|---|---|---|
| Automated WCAG | axe DevTools (browser extension) | Free + paid |
| Automated WCAG | WAVE | wave.webaim.org |
| Automated WCAG | Lighthouse | Chrome DevTools |
| Contrast | WebAIM Contrast Checker | webaim.org/resources/contrastchecker |
| Contrast | Colour Contrast Analyser | TPGi desktop app |
| Color blindness | Sim Daltonism | macOS app |
| Color blindness | Chrome DevTools (Rendering tab) | Built in |
| Keyboard | Manual tab navigation | No tools needed |
| Screen reader | NVDA | nvaccess.org (free, Windows) |
| Screen reader | VoiceOver | Built into macOS/iOS |
| Screen reader | JAWS | Freedom Scientific (commercial) |
| Mobile | TalkBack | Built into Android |
| Flicker | PEAT | Photosensitive Epilepsy Analysis Tool |
| Text spacing | Text Spacing Bookmarklet | https://www.html5accessibility.com/tests/tsbookmarklet.html |
| German | BITV-Test | bitvtest.de |
| Full audit | Deque WorldSpace | Commercial |

### 18.4 Testing Frequency

| Activity | Frequency |
|---|---|
| Automated CI scan | Every deployment |
| Manual keyboard test | Every sprint (new features) |
| Screen reader test | Monthly |
| Full audit | Annually or after major redesign |
| Accessibility statement update | After each audit |

---

## 19. AI Audit Checklist — Machine-Readable

This section provides a structured checklist suitable for AI-driven code review. For each item, the AI should:
1. Identify presence/absence in the HTML/CSS/JS
2. Assess compliance (PASS / FAIL / MANUAL CHECK NEEDED)
3. Generate specific remediation code

### CATEGORY A: Document Structure

```
[ ] A1  <html> has valid lang attribute (ISO 639-1)
[ ] A2  <head> contains <meta charset="UTF-8">
[ ] A3  <head> contains <meta name="viewport"> WITHOUT user-scalable=no
[ ] A4  <title> is present, unique, and descriptive (format: "Page — Site")
[ ] A5  <main id="..."> landmark present, one per page
[ ] A6  <header> landmark present with role="banner" implied
[ ] A7  <nav> landmarks present with aria-label to distinguish multiple navs
[ ] A8  <footer> landmark present
[ ] A9  <h1> present, exactly one per page
[ ] A10 Heading levels not skipped (h1→h2→h3, never h1→h3)
[ ] A11 Skip link is first focusable element, href points to #main-content
[ ] A12 Data tables use <th> with scope="col"/"row" and <caption>
[ ] A13 No layout tables (use CSS Grid/Flexbox instead)
[ ] A14 Lists use <ul>, <ol>, or <dl> — not <p> or <br>-separated items
```

### CATEGORY B: Images and Media

```
[ ] B1  All <img> have alt attribute
[ ] B2  Informative images: alt describes the information conveyed (not appearance)
[ ] B3  Decorative images: alt="" and role="presentation"
[ ] B4  Functional images (in links/buttons): alt describes the destination/action
[ ] B5  Complex images: alt + aria-describedby pointing to extended description
[ ] B6  Inline SVG: role="img" + <title> + <desc> or aria-label
[ ] B7  Decorative SVG: aria-hidden="true" focusable="false"
[ ] B8  <video> elements have <track kind="captions"> (pre-recorded)
[ ] B9  <video> elements have <track kind="descriptions"> or transcript link
[ ] B10 <audio> elements have transcript link
[ ] B11 Autoplay audio/video: mechanism to pause within 3 seconds
[ ] B12 No images of text (exception: logos)
```

### CATEGORY C: Color and Contrast

```
[ ] C1  Normal text contrast ≥ 4.5:1 (check all text/background combinations)
[ ] C2  Large text (≥24px or ≥18.67px bold) contrast ≥ 3:1
[ ] C3  UI components (input borders, button outlines) contrast ≥ 3:1
[ ] C4  Focus indicators contrast ≥ 3:1 against adjacent colors (WCAG 2.2)
[ ] C5  Color is not sole means of conveying information (errors, status, links)
[ ] C6  Link text distinguishable from body text without color alone (underline or other)
```

### CATEGORY D: Keyboard and Focus

```
[ ] D1  All interactive elements reachable via Tab key
[ ] D2  CSS: no "outline: none" or "outline: 0" without visible custom focus style
[ ] D3  Focus indicators visible with ≥3px perimeter and ≥3:1 contrast (SC 2.4.11)
[ ] D4  No positive tabindex values (tabindex="1" or higher)
[ ] D5  Tab order matches visual reading order
[ ] D6  Keyboard traps: none outside modals; modals trap correctly
[ ] D7  Modal: Escape key closes; focus returns to trigger
[ ] D8  Dropdown menus: Arrow keys navigate; Escape closes
[ ] D9  Tabs widget: Arrow keys navigate tabs; Tab moves to panel content
[ ] D10 All functionality achievable via keyboard only (no mouse-only interactions)
[ ] D11 Touch targets: ≥24×24px minimum (≥44×44px recommended) — SC 2.5.8
```

### CATEGORY E: Forms

```
[ ] E1  Every <input>, <select>, <textarea> has associated <label> (via for/id or wrapped)
[ ] E2  No label replaced by placeholder only
[ ] E3  Required fields: aria-required="true" and textual indicator (not only color/asterisk)
[ ] E4  Error messages: role="alert" or aria-live="polite"; describe error and suggest fix
[ ] E5  Error messages linked to field via aria-describedby
[ ] E6  Validation: aria-invalid="true" set on invalid fields
[ ] E7  Autocomplete attributes on personal data fields (SC 1.3.5)
[ ] E8  Authentication: no cognitive test as sole method (SC 3.3.8)
[ ] E9  Form submission: confirmation step for legal/financial transactions (SC 3.3.4)
[ ] E10 Previously entered data not re-required in same session (SC 3.3.7)
```

### CATEGORY F: ARIA and Semantics

```
[ ] F1  No ARIA used where native HTML element exists
[ ] F2  All ARIA roles have correct keyboard interaction implemented
[ ] F3  aria-label / aria-labelledby present on: dialogs, forms, nav landmarks, iframes
[ ] F4  aria-expanded on toggles (accordions, dropdowns, menus)
[ ] F5  aria-haspopup on elements that open menus/dialogs
[ ] F6  aria-controls links toggle to controlled element ID
[ ] F7  aria-live regions used for dynamic content updates
[ ] F8  role="alert" used for error messages; role="status" for non-urgent updates
[ ] F9  aria-current="page" on active navigation link
[ ] F10 iframe elements have title attribute
[ ] F11 Unique IDs throughout the document (no duplicate id attributes)
[ ] F12 Icon-only buttons: aria-label describing the action
[ ] F13 "Read more" links: aria-label includes context (SC 2.4.4)
```

### CATEGORY G: Content and Language

```
[ ] G1  <html lang="en"> (or correct language code) set
[ ] G2  Content in different language: lang attribute on that element
[ ] G3  Instructions do not rely solely on color/shape/location (SC 1.3.3)
[ ] G4  Orientation not locked to portrait or landscape (SC 1.3.4)
[ ] G5  No session timeout without 20-second warning and ability to extend (SC 2.2.1)
[ ] G6  Carousels/sliders: pause/stop control visible (SC 2.2.2)
[ ] G7  No content flashing >3 times/second (SC 2.3.1)
[ ] G8  Multiple ways to find pages: search + nav OR sitemap (SC 2.4.5)
[ ] G9  Consistent navigation order across all pages (SC 3.2.3)
[ ] G10 Consistent component identification across pages (SC 3.2.4)
[ ] G11 Help mechanism (contact info) in consistent position (SC 3.2.6 / WCAG 2.2)
```

### CATEGORY H: CSS and Responsive

```
[ ] H1  Font sizes in rem/em (not px only)
[ ] H2  200% zoom: no content loss, no horizontal scroll in text areas
[ ] H3  400% zoom / 320px wide: single-column reflow, no horizontal scroll (SC 1.4.10)
[ ] H4  Text containers: min-height not height; overflow not hidden on text (SC 1.4.12)
[ ] H5  prefers-reduced-motion: all transitions/animations suppressed (SC 2.3.3)
[ ] H6  prefers-color-scheme: dark mode meets same contrast ratios
[ ] H7  forced-colors / High Contrast Mode: borders visible, focus indicators work
[ ] H8  Tooltip content: stays visible when hovering over tooltip (SC 1.4.13)
[ ] H9  No content conveyed only by CSS (::before/::after used for decorative only)
```

### CATEGORY I: Legal Compliance

```
[ ] I1  Accessibility Statement published and linked from every page footer
[ ] I2  Accessibility Statement: compliance status declared
[ ] I3  Accessibility Statement: non-accessible content listed with reasons
[ ] I4  Accessibility Statement: contact email/phone for reporting barriers
[ ] I5  Accessibility Statement: link to enforcement/ombudsman body
[ ] I6  Accessibility Statement: date of last review
[ ] I7  Feedback mechanism (form or email) for reporting barriers
[ ] I8  Germany (BFSG): accessibility info in AGB/GTC or clearly visible location
[ ] I9  Germany (BITV, public): DGS video on homepage
[ ] I10 Germany (BITV, public): Leichte Sprache on homepage
```

### CATEGORY J: EN 301 549 Extras

```
[ ] J1  Biometric features (face ID, fingerprint): alternative non-biometric method exists
[ ] J2  Video player: captions can be enabled and are synchronized within ±100ms
[ ] J3  Video player: audio description track or extended description available
[ ] J4  Video player: caption/AD controls at same level as play/pause
[ ] J5  Downloadable documents (PDF, DOCX): accessible versions provided
[ ] J6  PDF documents: tagged, reading order correct, headings marked
[ ] J7  Support services: accessible via multiple channels (not phone-only)
[ ] J8  Accessibility features documented in product documentation
```

---

## 20. Reference Links

### Official Standards and Laws

| Resource | URL |
|---|---|
| WCAG 2.1 (W3C) | https://www.w3.org/TR/WCAG21/ |
| WCAG 2.2 (W3C) | https://www.w3.org/TR/WCAG22/ |
| ARIA Authoring Practices Guide | https://www.w3.org/WAI/ARIA/apg/ |
| EN 301 549 v3.2.1 (ETSI) | https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf |
| EU WAD (Directive 2016/2102) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016L2102 |
| EU EAA (Directive 2019/882) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019L0882 |
| European Commission Accessibility | https://digital-strategy.ec.europa.eu/en/policies/web-accessibility |
| EC: Latest Changes in EN 301 549 | https://digital-strategy.ec.europa.eu/en/policies/latest-changes-accessibility-standard |
| Germany BFSG (Federal Law) | https://www.gesetze-im-internet.de/bfsg/ |
| Germany BITV 2.0 | https://www.gesetze-im-internet.de/bitv_2_0/ |
| Germany BGG | https://www.gesetze-im-internet.de/bgg/ |
| ADA.gov — Title II Web Rule | https://www.ada.gov/resources/2024-03-08-web-rule/ |
| DOJ Final Rule (Federal Register) | https://www.federalregister.gov/documents/2024/04/24/2024-07758/ |
| Section 508 (Access Board) | https://www.access-board.gov/ict/ |

### Developer Tools and Testing

| Resource | URL |
|---|---|
| WebAIM | https://webaim.org |
| axe-core | https://github.com/dequelabs/axe-core |
| WAVE | https://wave.webaim.org |
| Pa11y | https://pa11y.org |
| Lighthouse | https://developer.chrome.com/docs/lighthouse |
| BITV-Test | https://www.bitvtest.de |
| NVDA Screen Reader | https://www.nvaccess.org |
| TPGi Colour Contrast Analyser | https://www.tpgi.com/color-contrast-checker/ |
| Text Spacing Bookmarklet | https://www.html5accessibility.com/tests/tsbookmarklet.html |
| MDN ARIA Reference | https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA |

### Accessibility Statement Generators

| Resource | URL |
|---|---|
| EU WAD Statement Generator | https://www.w3.org/WAI/planning/statements/generator/ |
| German Statement Template (BIK) | https://www.bitvtest.de/erklarung |

---

*Guide version: 2025-05-18. Based on EN 301 549 v3.2.1 (current legal standard), WCAG 2.2 AA (best practice), ADA Title II DOJ Final Rule (April 2024), Germany BFSG (effective 28 June 2025), Germany BITV 2.0. EN 301 549 v4.1.1 (expected 2026) will embed WCAG 2.2 AA — implementing WCAG 2.2 now ensures forward compatibility.*
