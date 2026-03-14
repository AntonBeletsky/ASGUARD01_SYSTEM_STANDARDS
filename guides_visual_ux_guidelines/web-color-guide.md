# The Complete Guide to Web Color Theory & Palette Selection

> A comprehensive reference for designers and developers building cohesive, accessible, and psychologically effective web experiences.

---

## Table of Contents

1. [Foundations of Color Theory](#1-foundations-of-color-theory)
2. [Color Models & Formats for the Web](#2-color-models--formats-for-the-web)
3. [Building Color Palettes](#3-building-color-palettes)
4. [The 60-30-10 Rule](#4-the-60-30-10-rule)
5. [Color Harmony Schemes](#5-color-harmony-schemes)
6. [Contrast & Accessibility (WCAG)](#6-contrast--accessibility-wcag)
7. [Color Psychology & Semantics](#7-color-psychology--semantics)
8. [Typography & Color Pairing](#8-typography--color-pairing)
9. [Light & Dark Themes](#9-light--dark-themes)
10. [Color Tokens & Design Systems](#10-color-tokens--design-systems)
11. [Industry-Specific Palettes](#11-industry-specific-palettes)
12. [Common Mistakes to Avoid](#12-common-mistakes-to-avoid)
13. [Testing & Validation](#13-testing--validation)
14. [Tools & Resources](#14-tools--resources)
15. [Quick Reference Cheat Sheet](#15-quick-reference-cheat-sheet)

---

## 1. Foundations of Color Theory

### 1.1 The Color Wheel

The color wheel is the foundational tool for understanding color relationships. It is organized as follows:

**Primary Colors** (cannot be mixed from others):
- Red, Yellow, Blue *(traditional)*
- Red, Green, Blue *(light/digital — RGB)*

**Secondary Colors** (mixed from two primaries):
- Orange (Red + Yellow)
- Green (Yellow + Blue)
- Violet (Blue + Red)

**Tertiary Colors** (mixed from primary + adjacent secondary):
- Red-Orange, Yellow-Orange, Yellow-Green, Blue-Green, Blue-Violet, Red-Violet

### 1.2 Color Properties

Every color has three core dimensions:

| Property | Description | Example |
|---|---|---|
| **Hue** | The pure color identity (the "what color is it") | Red, Blue, Green |
| **Saturation** | Intensity/purity of the color (vivid vs. muted) | Crimson vs. Dusty Rose |
| **Lightness / Value** | How light or dark the color is | Navy vs. Sky Blue |

Understanding these dimensions allows you to:
- Create tints (adding white to a hue)
- Create shades (adding black to a hue)
- Create tones (adding gray to a hue)

### 1.3 Warm vs. Cool Colors

**Warm Colors** (Reds, Oranges, Yellows):
- Create energy, urgency, warmth
- Appear to advance visually (jump forward on screen)
- Great for CTAs, alerts, food brands

**Cool Colors** (Blues, Greens, Purples):
- Create calm, trust, professionalism
- Appear to recede visually (push back on screen)
- Great for backgrounds, corporate, tech, finance

**Neutral Colors** (Blacks, Whites, Grays, Browns):
- Balance and ground the composition
- Should form the majority of most web palettes
- Carry their own temperature (warm gray vs. cool gray)

---

## 2. Color Models & Formats for the Web

### 2.1 HEX

The most common format for web colors. A 6-digit hexadecimal code representing Red, Green, Blue values (00–FF each).

```css
/* Syntax: #RRGGBB */
color: #1A73E8;   /* Google Blue */
color: #FF5733;   /* Orange-Red */
color: #2D2D2D;   /* Near-Black */
```

**Shorthand** (when each pair is identical):
```css
color: #FFF;  /* = #FFFFFF (white) */
color: #000;  /* = #000000 (black) */
color: #F90;  /* = #FF9900 */
```

### 2.2 RGB & RGBA

```css
/* rgb(red, green, blue)    — values 0–255 */
color: rgb(26, 115, 232);

/* rgba(red, green, blue, alpha)  — alpha 0.0–1.0 */
background-color: rgba(26, 115, 232, 0.15);  /* 15% opacity */
```

### 2.3 HSL & HSLA

HSL stands for Hue, Saturation, Lightness — the most **human-friendly** format for designers.

```css
/* hsl(hue°, saturation%, lightness%) */
color: hsl(217, 80%, 51%);           /* Vibrant blue */
color: hsl(217, 80%, 90%);           /* Light tint of the same blue */
color: hsl(217, 20%, 51%);           /* Muted/desaturated version */

/* hsla adds alpha channel */
background: hsla(217, 80%, 51%, 0.2);
```

**Why HSL is superior for theming:**
- Changing only lightness creates a perfect tint/shade scale
- Changing only saturation mutes or intensifies a color
- Easy to reason about: "I want a darker version of this" → decrease lightness

### 2.4 CSS Color Variables (Custom Properties)

Modern best practice for maintaining a consistent color system:

```css
:root {
  --color-primary:       hsl(217, 80%, 51%);
  --color-primary-light: hsl(217, 80%, 90%);
  --color-primary-dark:  hsl(217, 80%, 35%);

  --color-secondary:     hsl(25, 95%, 55%);

  --color-neutral-100:   hsl(220, 15%, 98%);
  --color-neutral-200:   hsl(220, 10%, 90%);
  --color-neutral-600:   hsl(220, 10%, 40%);
  --color-neutral-900:   hsl(220, 15%, 10%);

  --color-success:       hsl(142, 70%, 45%);
  --color-warning:       hsl(45,  95%, 50%);
  --color-error:         hsl(0,   80%, 55%);
}
```

---

## 3. Building Color Palettes

### 3.1 Anatomy of a Complete Web Palette

A well-constructed web palette typically includes:

```
Primary Color     → Brand identity, CTAs, key UI elements
Secondary Color   → Supporting accents, hover states
Neutral Scale     → Backgrounds, text, borders (7–10 steps)
Semantic Colors   → Success, Warning, Error, Info
Surface Colors    → Cards, modals, overlays
```

### 3.2 Creating a Scale (Tint & Shade System)

For each key color, define a full 9-step scale (100–900) using HSL:

```css
/* Example: Blue Scale */
--blue-100: hsl(217, 90%, 95%);  /* Lightest — backgrounds, hover fills */
--blue-200: hsl(217, 85%, 87%);
--blue-300: hsl(217, 80%, 75%);
--blue-400: hsl(217, 78%, 63%);
--blue-500: hsl(217, 75%, 51%);  /* Base brand color */
--blue-600: hsl(217, 73%, 43%);
--blue-700: hsl(217, 72%, 35%);
--blue-800: hsl(217, 70%, 26%);
--blue-900: hsl(217, 68%, 18%);  /* Darkest — dark mode backgrounds */
```

**Tips for creating scales:**
- Reduce saturation slightly as you go darker (prevents muddy or unnatural deep tones)
- Increase saturation slightly in the mid-range (300–600) for vibrant, usable colors
- Steps 400–600 are your "interaction zone" (default, hover, active states)

### 3.3 Neutral (Gray) Scale

Neutrals carry the most weight on any website. Use **chromatic neutrals** — grays with a slight tint of your brand color — rather than pure grays.

```css
/* Warm neutral scale (slight warm tint — good for consumer brands) */
--neutral-50:  hsl(30, 20%, 98%);
--neutral-100: hsl(30, 15%, 95%);
--neutral-200: hsl(30, 10%, 88%);
--neutral-300: hsl(30,  8%, 76%);
--neutral-400: hsl(30,  6%, 60%);
--neutral-500: hsl(30,  5%, 46%);
--neutral-600: hsl(30,  5%, 34%);
--neutral-700: hsl(30,  4%, 24%);
--neutral-800: hsl(30,  4%, 16%);
--neutral-900: hsl(30,  4%, 10%);

/* Cool neutral scale (slight cool tint — good for tech/SaaS) */
--neutral-50:  hsl(220, 20%, 98%);
/* ... same pattern with higher hue value */
```

---

## 4. The 60-30-10 Rule

This is the single most reliable rule for visual balance in web design. Borrowed from interior design, it ensures no palette element overwhelms the others.

```
60% — Dominant Color (usually background / large surfaces)
30% — Secondary Color (sidebars, sections, secondary UI elements)
10% — Accent Color (CTAs, links, highlights, icons)
```

### 4.1 Practical Application

**Example: SaaS Dashboard**

| Area | Color Role | % |
|---|---|---|
| Page background, cards | Light neutral (`--neutral-50`) | ~60% |
| Sidebar, headers, section dividers | Mid neutral or brand light (`--neutral-100`) | ~30% |
| Buttons, active nav, badges, icons | Primary brand color (`--blue-500`) | ~10% |

### 4.2 Common Violations

- ❌ Using your brand color on 50% of the page — looks loud and exhausting
- ❌ Three competing accent colors of equal visual weight
- ❌ Applying a bright color to body text areas

### 4.3 Adapting the Rule

For dark themes: neutrals still dominate at 60%, but they are dark neutrals (800–900 scale). The rule is about **proportion**, not specific colors.

---

## 5. Color Harmony Schemes

### 5.1 Monochromatic

Uses a single hue with varying saturation and lightness.

```
Hue: Blue (220°)
Colors used: Blue-100, Blue-300, Blue-500, Blue-700, Blue-900
```

✅ **Pros:** Safe, elegant, professional, easy to maintain  
⚠️ **Cons:** Can feel monotonous without careful contrast variation  
🎯 **Best for:** Minimal portfolios, enterprise dashboards, landing pages

### 5.2 Analogous

Uses 2–3 adjacent hues on the color wheel (within ~30–60° of each other).

```
Example: Blue (220°) + Blue-Teal (195°) + Teal (170°)
```

✅ **Pros:** Natural, harmonious, feels cohesive  
⚠️ **Cons:** Low contrast between colors if not managed carefully  
🎯 **Best for:** Nature brands, wellness, lifestyle, editorial sites

### 5.3 Complementary

Uses two hues opposite each other on the color wheel (~180° apart).

```
Example: Blue (220°) + Orange (40°)
```

✅ **Pros:** High contrast, dynamic, eye-catching  
⚠️ **Cons:** Can feel harsh if both colors are heavily saturated  
🎯 **Best for:** E-commerce CTAs, sports brands, entertainment

**Rule:** Use one color as dominant (60%), the other purely as accent (10%).

### 5.4 Split-Complementary

Uses a base hue plus two colors adjacent to its complement (±30° from complement).

```
Example: Blue (220°) + Yellow-Orange (50°) + Red-Orange (20°)
```

✅ **Pros:** High contrast like complementary, but more flexible and less tension  
⚠️ **Cons:** Slightly more complex to balance  
🎯 **Best for:** Creative agencies, portfolio sites, marketing pages

### 5.5 Triadic

Uses three hues equally spaced on the color wheel (120° apart).

```
Example: Red (0°) + Blue (220°) + Yellow (60°)
         Or: Blue (220°) + Yellow-Green (100°) + Red-Orange (340°)
```

✅ **Pros:** Vibrant, playful, visually rich  
⚠️ **Cons:** Hard to balance — requires one dominant + one secondary + one accent  
🎯 **Best for:** Children's brands, games, creative platforms

### 5.6 Tetradic / Square

Uses four hues (either two pairs of complements, or equally spaced at 90°).

✅ **Pros:** Maximum variety  
⚠️ **Cons:** Very difficult to balance — typically use only one as dominant  
🎯 **Best for:** Rarely used in web UI; better for illustration/branding assets

---

## 6. Contrast & Accessibility (WCAG)

Accessibility is not optional. The Web Content Accessibility Guidelines (WCAG) define minimum contrast ratios to ensure readability for users with low vision or color blindness.

### 6.1 Contrast Ratio Requirements

| Standard | Contrast Ratio | Use Case |
|---|---|---|
| **WCAG AA** (minimum) | **4.5:1** | Normal text (< 18pt / < 14pt bold) |
| **WCAG AA Large Text** | **3:1** | Large text (≥ 18pt / ≥ 14pt bold) |
| **WCAG AAA** (enhanced) | **7:1** | Normal text (highest accessibility) |
| **WCAG AAA Large Text** | **4.5:1** | Large text |
| **UI Components** | **3:1** | Buttons, form inputs, icons |

> **Contrast ratio of 1:1** = no contrast (invisible). **21:1** = pure black on white (maximum).

### 6.2 How to Calculate Contrast

Contrast ratio = (L1 + 0.05) / (L2 + 0.05)

Where L1 is the relative luminance of the lighter color and L2 is the relative luminance of the darker color.

**Practical tip:** Always use a tool (see §14). Never guess.

### 6.3 Accessible Color Combinations (Examples)

| Background | Text Color | Ratio | WCAG |
|---|---|---|---|
| `#FFFFFF` white | `#595959` gray | 7.0:1 | AAA |
| `#FFFFFF` white | `#767676` gray | 4.6:1 | AA |
| `#1A73E8` blue | `#FFFFFF` white | 4.6:1 | AA |
| `#FF0000` red | `#FFFFFF` white | 4.0:1 | FAIL |
| `#F5F5F5` light gray | `#333333` dark | 10.4:1 | AAA |

### 6.4 Color Blindness Considerations

Approximately 8% of men and 0.5% of women have some form of color vision deficiency.

**Types:**
- **Deuteranopia / Deuteranomaly** — difficulty distinguishing Red/Green (most common)
- **Protanopia / Protanomaly** — reduced red sensitivity
- **Tritanopia** — difficulty with Blue/Yellow (rare)
- **Achromatopsia** — complete color blindness (very rare)

**Rules for color-blind-safe design:**
1. Never rely on color alone to convey meaning — add icons, labels, or patterns
2. Avoid Red/Green combinations without supporting cues
3. Test your palette with a color blindness simulator (see §14)
4. Sufficient lightness contrast helps all users including color-blind ones

```html
<!-- ❌ Bad: relies only on color for meaning -->
<span class="red-text">Error occurred</span>

<!-- ✅ Good: color + icon + label -->
<span class="error">
  <svg><!-- error icon --></svg>
  Error: File not found
</span>
```

### 6.5 The "Pure White" Problem

Using `#FFFFFF` pure white for large backgrounds often creates excessive contrast and visual fatigue. Use near-whites instead:

```css
/* Better background colors than pure white */
--bg-white: hsl(220, 20%, 98%);  /* Very slightly blue-gray */
--bg-warm:  hsl(30,  30%, 98%);  /* Very slightly warm */

/* Better text colors than pure black */
--text-dark: hsl(220, 15%, 12%);  /* Near-black with slight blue tint */
```

---

## 7. Color Psychology & Semantics

### 7.1 Color Meanings in Western Digital Contexts

| Color | Primary Associations | Best Used For | Avoid For |
|---|---|---|---|
| 🔵 **Blue** | Trust, stability, calm, intelligence | Finance, tech, healthcare, CTAs | Food (suppresses appetite), energy brands |
| 🔴 **Red** | Urgency, passion, error, danger | Alerts, sales, CTAs, food | Trust signals, calming interfaces |
| 🟢 **Green** | Success, growth, safety, nature | Success states, eco brands, finance | Error states, warnings |
| 🟡 **Yellow** | Warning, optimism, energy, caution | Warnings, highlights, children | Body text (low contrast), luxury |
| 🟠 **Orange** | Warmth, creativity, enthusiasm, affordable | E-commerce CTAs, food, consumer | Enterprise/corporate, luxury, finance |
| 🟣 **Purple** | Luxury, creativity, wisdom, mystery | Premium products, beauty, tech | Danger signals, food |
| ⚫ **Black** | Elegance, authority, sophistication | Luxury, fashion, editorial | Children's products, medical |
| ⚪ **White** | Purity, cleanliness, simplicity | Space/breathing room, healthcare, minimal | Accessible text on light backgrounds |
| 🩶 **Gray** | Neutrality, balance, secondary info | Disabled states, placeholders, secondary text | Primary CTAs, success signals |
| 🤎 **Brown/Beige** | Warmth, earth, reliability, organic | Food, lifestyle, artisan brands | Tech, finance, alerts |

### 7.2 Semantic Color Roles in UI Systems

These color meanings are so ingrained in user expectations that breaking them causes confusion:

```css
/* Universal UI semantic colors */
--color-success: /* Green family */   hsl(142, 70%, 45%);
--color-warning: /* Yellow/Amber */   hsl(45,  95%, 50%);
--color-error:   /* Red family */     hsl(0,   80%, 55%);
--color-info:    /* Blue family */    hsl(205, 85%, 50%);

/* Usage */
.alert-success { background: hsl(142, 70%, 95%); border-color: hsl(142, 70%, 45%); color: hsl(142, 70%, 25%); }
.alert-error   { background: hsl(0,   80%, 97%); border-color: hsl(0,   80%, 55%); color: hsl(0,   80%, 35%); }
```

**Critical rule:** Never use red for a success state or green for an error state, even if your brand uses these colors for other purposes. Semantic overrides brand in functional UI elements.

### 7.3 Cultural Context

Color meanings vary significantly across cultures. If you're building for international audiences:

| Color | Western | East Asian | Middle Eastern | Latin American |
|---|---|---|---|---|
| **White** | Purity, wedding | Mourning, death | Purity | Purity |
| **Red** | Danger, love | Luck, celebration | Caution | Passion |
| **Green** | Nature, go | Expensive, prestigious | Islam, sacred | Nature |
| **Black** | Death, luxury | Neutral | Mourning | Mourning |

---

## 8. Typography & Color Pairing

### 8.1 Text Color Hierarchy

Establishing a clear text color hierarchy improves readability and reduces visual noise:

```css
/* Text color hierarchy (light theme) */
--text-primary:   hsl(220, 15%, 12%);   /* Headlines, body text — high contrast */
--text-secondary: hsl(220, 10%, 38%);   /* Labels, captions, secondary info */
--text-tertiary:  hsl(220, 8%, 55%);    /* Placeholders, disabled, hints */
--text-inverse:   hsl(220, 20%, 98%);   /* Text on dark backgrounds */
--text-link:      hsl(217, 80%, 50%);   /* Interactive links */
--text-link-hover:hsl(217, 80%, 38%);   /* Link hover state */
```

### 8.2 Background & Text Combinations

| Background Type | Text Choice | Why |
|---|---|---|
| Light neutral bg | Dark near-black text | Maximum readability, long reading |
| Dark bg (800+) | Light neutral text | High contrast, avoid pure white |
| Vibrant brand bg (CTA) | White or very light | Contrast + emphasis |
| Light brand tint bg | Dark version of same hue | Cohesive, contained |
| Image background | White with text-shadow or overlay | Guarantees legibility |

### 8.3 Ensuring Legibility Over Images

```css
/* Method 1: Semi-transparent overlay */
.hero {
  background-image: url('hero.jpg');
  position: relative;
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);  /* 50% black overlay */
}

/* Method 2: Gradient overlay */
.hero::before {
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 0.75) 0%,
    rgba(0, 0, 0, 0) 60%
  );
}

/* Method 3: Text shadow (light text on unpredictable images) */
.hero-text {
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
}
```

---

## 9. Light & Dark Themes

### 9.1 Principles of Dark Mode Design

Dark mode is not a simple color inversion. It requires thoughtful redesign:

**Rule 1: Use dark gray, not black**
```css
/* ❌ Avoid pure black backgrounds */
--bg-base: #000000;

/* ✅ Use dark grays with slight hue */
--bg-base:    hsl(220, 13%, 9%);   /* Base surface */
--bg-raised:  hsl(220, 13%, 13%);  /* Cards, modals */
--bg-overlay: hsl(220, 13%, 17%);  /* Dropdowns, tooltips */
```

**Rule 2: Desaturate colors for dark mode**

Saturated colors on dark backgrounds appear too vibrant and can cause eye strain (halation effect):

```css
/* Light mode primary */
--color-primary: hsl(217, 80%, 51%);

/* Dark mode primary — less saturated, slightly lighter */
--color-primary: hsl(217, 65%, 65%);
```

**Rule 3: Reverse elevation using lightness, not shadows**

In light mode, shadows create depth. In dark mode, lighter surfaces appear "higher":

```css
/* Light theme: elevation via shadow */
.card { background: #FFF; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }

/* Dark theme: elevation via surface lightness */
.card-level-1 { background: hsl(220, 13%, 11%); }
.card-level-2 { background: hsl(220, 13%, 14%); }  /* Higher = lighter */
.card-level-3 { background: hsl(220, 13%, 18%); }
```

### 9.2 CSS Implementation

```css
/* Token-based theming approach */
:root {
  --surface-bg:      hsl(220, 20%, 98%);
  --surface-card:    hsl(220, 20%, 100%);
  --text-primary:    hsl(220, 15%, 12%);
  --text-secondary:  hsl(220, 10%, 38%);
  --border-color:    hsl(220, 15%, 88%);
}

[data-theme="dark"] {
  --surface-bg:      hsl(220, 13%, 9%);
  --surface-card:    hsl(220, 13%, 13%);
  --text-primary:    hsl(220, 15%, 92%);
  --text-secondary:  hsl(220, 10%, 65%);
  --border-color:    hsl(220, 13%, 22%);
}

/* OS-level preference (no JS required) */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --surface-bg: hsl(220, 13%, 9%);
    /* ... */
  }
}
```

### 9.3 Dark Mode Checklist

- [ ] Backgrounds use dark gray, not pure black
- [ ] Text uses near-white, not pure white
- [ ] Accent colors are desaturated 10–20%
- [ ] All color combinations re-checked for WCAG contrast
- [ ] Images with white backgrounds handled (transparent PNG or special handling)
- [ ] Illustrations/icons tested in dark context
- [ ] Form inputs, borders and dividers re-checked
- [ ] Focus ring colors verified for visibility

---

## 10. Color Tokens & Design Systems

### 10.1 Three-Tier Token Architecture

A scalable design token system uses three tiers:

**Tier 1 — Primitive Tokens** (raw values, no semantic meaning):
```css
--blue-500: hsl(217, 80%, 51%);
--red-500:  hsl(0, 80%, 55%);
--gray-100: hsl(220, 15%, 95%);
```

**Tier 2 — Semantic Tokens** (purpose-defined, reference primitives):
```css
--color-action-primary:   var(--blue-500);
--color-action-danger:    var(--red-500);
--color-background-page:  var(--gray-100);
```

**Tier 3 — Component Tokens** (component-specific, reference semantic):
```css
--button-primary-bg:      var(--color-action-primary);
--button-danger-bg:       var(--color-action-danger);
--page-bg:                var(--color-background-page);
```

### 10.2 Naming Conventions

Use a consistent naming pattern:
```
--{category}-{property}-{variant}-{state}

Examples:
--color-text-primary
--color-text-secondary-disabled
--color-background-surface-hover
--color-border-input-error-focused
```

### 10.3 Tailwind CSS Color Scale Reference

If using Tailwind CSS, the built-in scales follow this lightness structure:

| Step | Approximate Lightness | Typical Use |
|---|---|---|
| 50 | 97–98% | Very light backgrounds |
| 100 | 94–95% | Hover backgrounds |
| 200 | 88–90% | Disabled backgrounds |
| 300 | 76–80% | Border colors |
| 400 | 62–65% | Placeholder text |
| 500 | 50–55% | **Base color** (most uses) |
| 600 | 42–45% | Hover states |
| 700 | 34–37% | Active states |
| 800 | 25–28% | Dark text on light bg |
| 900 | 16–20% | Very dark backgrounds |

---

## 11. Industry-Specific Palettes

### 11.1 Finance & Banking
```css
/* Trust, stability, authority */
--primary:    hsl(214, 72%, 35%);   /* Deep blue */
--secondary:  hsl(214, 30%, 92%);   /* Light blue */
--accent:     hsl(142, 60%, 38%);   /* Success green */
--neutral:    hsl(214, 8%, 45%);    /* Slate gray */
```

### 11.2 Healthcare
```css
/* Clean, calm, trustworthy, clinical */
--primary:    hsl(200, 65%, 45%);   /* Medical teal/blue */
--secondary:  hsl(200, 40%, 92%);   /* Light teal bg */
--accent:     hsl(142, 55%, 42%);   /* Healthy green */
--neutral:    hsl(200, 8%, 50%);    /* Cool gray */
```

### 11.3 E-commerce / Retail
```css
/* Energetic, trustworthy, value-oriented */
--primary:    hsl(217, 78%, 50%);   /* Action blue */
--secondary:  hsl(25, 100%, 55%);   /* Warm orange (CTAs) */
--accent:     hsl(142, 65%, 40%);   /* "In stock" green */
--sale:       hsl(0, 80%, 52%);     /* Sale red */
```

### 11.4 SaaS / Technology
```css
/* Modern, professional, focused */
--primary:    hsl(250, 80%, 60%);   /* Indigo/purple */
--secondary:  hsl(250, 60%, 96%);   /* Light purple bg */
--accent:     hsl(180, 70%, 42%);   /* Teal complement */
--neutral:    hsl(220, 12%, 20%);   /* Dark slate */
```

### 11.5 Food & Restaurant
```css
/* Appetite-stimulating, warm, inviting */
--primary:    hsl(14, 90%, 50%);    /* Warm red-orange */
--secondary:  hsl(40, 95%, 55%);    /* Golden yellow */
--accent:     hsl(120, 40%, 30%);   /* Natural green */
--neutral:    hsl(25, 15%, 25%);    /* Warm near-black */
```

### 11.6 Wellness & Mindfulness
```css
/* Calm, natural, gentle */
--primary:    hsl(165, 40%, 50%);   /* Sage green */
--secondary:  hsl(30, 35%, 88%);    /* Warm beige */
--accent:     hsl(260, 35%, 65%);   /* Soft lavender */
--neutral:    hsl(30, 10%, 30%);    /* Warm dark gray */
```

---

## 12. Common Mistakes to Avoid

### 12.1 Too Many Colors
❌ Using 6+ distinct brand colors across a single page  
✅ Limit to 1–2 brand colors + neutrals + semantic colors

### 12.2 Low Contrast Text
❌ Light gray text on white background (`#BBBBBB` on `#FFFFFF` = 2.3:1 — fails WCAG)  
✅ Always verify with a contrast checker before shipping

### 12.3 Pure Black on Pure White
❌ `#000000` text on `#FFFFFF` background — too harsh, causes visual vibration  
✅ Use `#1A1A2E` or similar near-black on `#FAFAFA` or similar near-white

### 12.4 Relying Solely on Color to Communicate
❌ "Red fields have errors" (invisible to colorblind users)  
✅ Red color + error icon + error message text

### 12.5 Ignoring Hover/Focus/Active States
❌ No visual feedback on interactive elements  
✅ Define at minimum: default, hover (darken 10–15%), active (darken 20–25%), focus (visible outline), disabled (reduced opacity + muted color)

```css
.btn-primary {
  background: var(--color-primary);           /* Default */
}
.btn-primary:hover {
  background: var(--color-primary-hover);     /* 10% darker */
}
.btn-primary:active {
  background: var(--color-primary-active);    /* 20% darker */
}
.btn-primary:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;                        /* Always visible focus */
}
.btn-primary:disabled {
  background: var(--color-neutral-300);
  color: var(--color-neutral-500);
  cursor: not-allowed;
}
```

### 12.6 Forgetting Focus Indicators
❌ `outline: none` or `outline: 0` with no replacement  
✅ Always maintain a visible focus indicator for keyboard users

### 12.7 Inconsistent Border & Divider Colors
❌ Using random grays for different borders throughout the UI  
✅ Define 2–3 border color tokens and use them consistently

### 12.8 Over-using Gradients
❌ Gradient on every surface, card, and button  
✅ Reserve gradients for specific branded moments (hero sections, primary CTAs)

---

## 13. Testing & Validation

### 13.1 Contrast Testing Process

1. Export your final color pairs (text + background for every combination used)
2. Test every pair at [contrast-ratio.com](https://contrast-ratio.com) or using browser DevTools
3. Fix any pair that fails WCAG AA (4.5:1 for normal text, 3:1 for large text)
4. Document passing ratios in your design system for future reference

### 13.2 Color Blindness Testing

**Simulation methods:**
- Chrome DevTools → Rendering → Emulate vision deficiencies
- Firefox Accessibility Panel → Simulate
- Figma plugin: Able or Color Blind
- Online: [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/)

**Test for at minimum:**
- Deuteranopia (red-green, most common)
- Protanopia (red-green variant)
- Grayscale (no color — tests if meaning is conveyed without color)

### 13.3 Device & Display Testing

Colors appear differently across devices and color profiles:
- **Windows (sRGB):** Colors appear less saturated
- **macOS (P3 Display):** Wider gamut, richer colors
- **Mobile OLED screens:** Deeper blacks, punchier colors
- **Projectors:** Washed out, lower contrast

**Tip:** Test on at minimum two devices (one Windows/Android, one Mac/iOS). Design at sRGB to ensure broad compatibility.

### 13.4 Automated Tools

```bash
# Using axe-core (npm) for accessibility testing including color contrast
npm install axe-core

# Lighthouse (built into Chrome DevTools)
# Accessibility audit → reports contrast failures

# Pa11y (command line)
npm install -g pa11y
pa11y https://yoursite.com
```

---

## 14. Tools & Resources

### 14.1 Palette Generation

| Tool | URL | Best For |
|---|---|---|
| **Coolors** | coolors.co | Quick random palette generation |
| **Adobe Color** | color.adobe.com | Harmony rules, extract from image |
| **Paletton** | paletton.com | Color wheel with harmony rules |
| **Huemint** | huemint.com | AI-generated brand palettes |
| **Realtime Colors** | realtimecolors.com | Preview on real UI instantly |
| **Palette UI** | palette.ui.tools | Tailwind-compatible scales |

### 14.2 Contrast & Accessibility

| Tool | URL | Purpose |
|---|---|---|
| **Contrast Ratio** | contrast-ratio.com | Quick manual contrast check |
| **APCA Contrast** | apcacontrast.com | New perceptual contrast model |
| **Who Can Use** | whocanuse.com | Shows who can see your combo |
| **Color Review** | color.review | Pass/fail for all WCAG levels |

### 14.3 Color Blindness

| Tool | URL | Purpose |
|---|---|---|
| **Coblis** | color-blindness.com/coblis | Upload image & simulate |
| **Pilestone Simulator** | pilestone.com | Online simulator |
| Chrome DevTools | Built-in | Rendering → Vision deficiencies |

### 14.4 Color Inspiration

| Tool | URL | Purpose |
|---|---|---|
| **Dribbble** | dribbble.com | Real-world design color usage |
| **Muzli Colors** | colors.muz.li | Trending palettes from design world |
| **Color Hunt** | colorhunt.co | Community-curated palettes |
| **Khroma** | khroma.co | AI palette from your favorites |

### 14.5 CSS Color Functions (Modern CSS)

```css
/* CSS color-mix() — mix two colors */
.element {
  background: color-mix(in srgb, #1A73E8 20%, white);
}

/* CSS relative color syntax — modify a color */
:root { --brand: hsl(217, 80%, 51%); }
.hover {
  background: hsl(from var(--brand) h s calc(l - 10%));
}

/* oklch — perceptually uniform color space */
--color-primary: oklch(55% 0.2 250);
```

---

## 15. Quick Reference Cheat Sheet

### Contrast Ratios
```
Normal text:    ≥ 4.5:1 (WCAG AA) | ≥ 7:1 (WCAG AAA)
Large text:     ≥ 3.0:1 (WCAG AA) | ≥ 4.5:1 (WCAG AAA)
UI Components:  ≥ 3.0:1
```

### Palette Distribution
```
60% Dominant (backgrounds, large surfaces)
30% Secondary (sections, supporting elements)
10% Accent (CTAs, interactive, highlights)
```

### Semantic Colors
```
Success  → Green  (hue ~140°)
Warning  → Yellow (hue ~45°)
Error    → Red    (hue ~0°)
Info     → Blue   (hue ~205°)
```

### HSL Quick Adjustments
```
Tint  → increase lightness (+ 10–30%)
Shade → decrease lightness (- 10–30%)
Mute  → decrease saturation (- 20–50%)
Vibrant → increase saturation (+ 10–30%)
```

### Dark Mode Essentials
```
Background: dark gray, NOT black (#0a0a0a is too dark)
Text: near-white, NOT white (hsl(220, 15%, 92%))
Accents: desaturate 10–20% vs. light mode version
Elevation: lighter surface = higher elevation
```

### Rule of Thumb for Color Count
```
Backgrounds:  2–3 neutral tones
Brand colors: 1 primary + optional 1 secondary
Semantic:     4 fixed (success/warning/error/info)
Text:         3 levels (primary/secondary/tertiary)
Total unique values in use: 12–18 is healthy
```

---

*Last updated: February 2026 | Based on WCAG 2.2 guidelines*
