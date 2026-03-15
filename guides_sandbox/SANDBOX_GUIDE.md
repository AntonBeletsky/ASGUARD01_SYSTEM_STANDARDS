# 🧩 Sandbox Guide — Section Marker Methodology

This file is an instruction for Claude on how to assemble and disassemble an HTML/CSS/JS sandbox using comment markers.

---

## What are Sandbox Sections

HTML, CSS, and JS files in the project are marked with special comment markers.
Claude finds these markers and either assembles everything into one file, or splits it back into the original files.

### HTML markers (in `.html` files)
```html
<!-- sandbox-section-html-start: section_name -->
  ... html code ...
<!-- sandbox-section-html-end: section_name -->
```

### CSS markers (in `.css` files)
```css
/* sandbox-section-css-start: section_name */
  ... css code ...
/* sandbox-section-css-end: section_name */
```

### JS markers (in `.js` files)
```js
/* sandbox-section-js-start: section_name */
  ... js code ...
/* sandbox-section-js-end: section_name */
```

> **Rule:** Section name in the marker is arbitrary, but must be identical in start and end.
> Example names: `header`, `modal`, `form-validation`, `main-layout`

---

## Command: "assemble sandbox"

**What Claude does:**
1. Finds all `.html`, `.css`, `.js` files in the project
2. Extracts content between `sandbox-section-*-start` and `sandbox-section-*-end` markers
3. Records the source of each section (which file it came from)
4. Assembles a single `sandbox.html` file using the structure below

**Output file structure `sandbox.html`:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sandbox</title>

  <!-- Bootstrap 5 CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

  <style>
    /* === [SOURCE: styles/main.css -> section_name] === */
    /* sandbox-section-css-start: section_name */
    ... css code ...
    /* sandbox-section-css-end: section_name */

    /* === [SOURCE: styles/modal.css -> modal-styles] === */
    /* sandbox-section-css-start: modal-styles */
    ... css code ...
    /* sandbox-section-css-end: modal-styles */
  </style>
</head>
<body>

  <!-- === [SOURCE: index.html -> header] === -->
  <!-- sandbox-section-html-start: header -->
  ... html code ...
  <!-- sandbox-section-html-end: header -->

  <!-- === [SOURCE: components/modal.html -> modal] === -->
  <!-- sandbox-section-html-start: modal -->
  ... html code ...
  <!-- sandbox-section-html-end: modal -->

  <!-- Bootstrap 5 JS Bundle (with Popper) -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmTA82D7P3AeA3bvvIB6JQKn4X6f" crossorigin="anonymous"></script>

  <script>
    /* === [SOURCE: scripts/app.js -> init] === */
    /* sandbox-section-js-start: init */
    ... js code ...
    /* sandbox-section-js-end: init */
  </script>
</body>
</html>
```

> **SOURCE comment** — kept inside the file so Claude knows where to return code when disassembling.

---

## Command: "disassemble sandbox into files"

**What Claude does:**
1. Opens the edited `sandbox.html`
2. Finds `[SOURCE: file -> section]` comments
3. Extracts content between `sandbox-section-*-start/end` markers
4. Writes updated content **back into the corresponding original files**, replacing content between those same markers
5. Markers in original files remain intact — only the content between them is updated

**Important:** Claude does not touch anything outside the markers in the original files.

---

## Quick Chat Commands

| Command | What it does |
|---|---|
| `assemble sandbox` | Builds `sandbox.html` from all marked sections in the project |
| `disassemble sandbox into files` | Splits edited `sandbox.html` back into the original files |

---

## Project markup example

**`index.html`**
```html
<main>
  <!-- sandbox-section-html-start: hero -->
  <section class="hero">
    <h1>Heading</h1>
  </section>
  <!-- sandbox-section-html-end: hero -->
</main>
```

**`styles/main.css`**
```css
/* sandbox-section-css-start: hero */
.hero {
  background: #000;
  color: #fff;
}
/* sandbox-section-css-end: hero */
```

**`scripts/app.js`**
```js
/* sandbox-section-js-start: hero */
document.querySelector('.hero').addEventListener('click', () => {
  console.log('clicked');
});
/* sandbox-section-js-end: hero */
```

---

## Bootstrap CDN (Bootstrap 5.3 current links)

```html
<!-- CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

<!-- JS Bundle (includes Popper) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmTA82D7P3AeA3bvvIB6JQKn4X6f" crossorigin="anonymous"></script>
```

---

## Assembly rules for Claude

1. **Keep markers** — `sandbox-section-*-start/end` markers stay in `sandbox.html`, do not remove them
2. **Add SOURCE** — before each block write `<!-- === [SOURCE: path/to/file -> section_name] === -->`
3. **Order in `<style>`** — Bootstrap first, then all CSS sections
4. **Order in `<script>`** — Bootstrap JS first, then all JS sections
5. **Copy verbatim** — HTML, CSS, JS is copied exactly as-is, no modifications
6. **On disassembly** — replace only the content between markers, leave the rest of each file untouched

---

## Disassembly rules for Claude

1. Read `[SOURCE: file -> section]` to know where to write
2. Find in the original file the markers `sandbox-section-*-start: section` and `sandbox-section-*-end: section`
3. Replace the content between them with the updated content from `sandbox.html`
4. If the file does not exist — create it and notify the user
5. If the section is not found in the original — append the section at the end of the file and notify the user

---

*Open this file in Antigravity and send it to the chat as context before running assemble/disassemble commands.*
