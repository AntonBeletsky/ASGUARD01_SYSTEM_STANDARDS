# Customization reference

Read this only when a user explicitly asks for a modified version of the
tool or its output theme — not needed for a normal documentation request.
Every pointer below names the exact constant/function to edit in
`scripts/doc_generator.py`.

## Changing the visual theme

All colors, fonts, and spacing live in one place: the `:root` block at the
top of the `DOC_CSS` string constant. It's a deliberate "atlas/blueprint"
theme (ink-navy chrome, cool paper background, copper/verdigris/gold as
the HTML/CSS/JS legend colors) chosen to avoid generic template clichés —
see the design rationale in the chat history this bundle came from if the
user asks why it looks the way it does. To retheme:

1. Edit the CSS custom properties in `DOC_CSS` (`--ink`, `--paper`,
   `--accent`, `--map-html`/`--map-css`/`--map-js`, `--font-display`,
   `--font-body`, `--font-mono`). Everything downstream references these
   variables, so changing them here recolors the whole document
   consistently — don't hunt for hardcoded hex values elsewhere in the
   template functions.
2. `_GRAPH_COL_TITLE`, `_GRAPH_NODE_W/H`, and the inline `<style>` block
   inside `render_dependency_graph_svg()` control the dependency-graph SVG
   specifically; it reads the *same* CSS variables (inline SVG in an HTML
   document can use `var(--x)`), so a theme edit in step 1 usually
   propagates there too without extra work.
3. **Keep it offline-safe.** The whole point of a single self-contained
   HTML file is that it needs no network access to read. Don't add a
   Google Fonts `<link>` or a CDN script tag without discussing that
   trade-off with the user first — system font stacks were chosen
   deliberately (see `DOC_CSS`'s `--font-*` fallback chains) so the
   document looks intentional even fully offline.

## Adding ignore patterns

`DEFAULT_IGNORE_DIRS` (near the top of the script) is the always-excluded
directory set. For a one-off run, prefer the CLI's `--ignore <glob>` flag
(repeatable) over editing the script. Only edit `DEFAULT_IGNORE_DIRS`
itself if the user wants a persistent change to what counts as "noise" for
every future run.

## Extending the language coverage

- **New file extensions for an existing language** — add to `HTML_EXTS`,
  `CSS_EXTS`, or `JS_EXTS` (e.g. adding `.cjs` variants). Cheap, safe.
- **A genuinely new language/format (TypeScript, Vue SFCs, JSX-aware
  parsing)** — this is the most valuable real extension point, and also
  the most involved. Don't try to shoehorn it into the existing regex-based
  `analyze_js()`. Options, roughly in order of effort vs. payoff:
  1. Add a new `analyze_ts()`/`analyze_vue()` following the same pattern
     (`rel_path` + raw text in, a populated `*Info` dataclass out), reusing
     `_mask_js()`-style string/comment handling where it still applies.
  2. For real JS/TS accuracy, shell out to Node.js if it's available in
     the environment (`shutil.which("node")`) and use a small embedded
     Acorn/Espree or the TypeScript compiler API script to get a real AST,
     falling back to the existing regex parser when Node isn't present.
     This was deliberately *not* done for v1 to keep the tool
     dependency-free and instantly runnable anywhere — treat it as an
     opt-in upgrade path, not a replacement, unless the user's environment
     guarantees Node.js.
  3. For Vue SFCs specifically, the `<template>`/`<script>`/`<style>`
     blocks can mostly be split with the existing `HTMLParser`-based
     approach (treat the file as HTML, extract each top-level block, then
     run `analyze_html`/`analyze_js`/`analyze_css` on the relevant pieces)
     before any component-semantics (props/emits) work is attempted.

## Adding a new diagnostic ("Cartographer's note")

Diagnostics are computed in `analyze_project_stats()` and rendered in
`build_overview_section()`'s `notes` list. Follow the existing pattern:
compute a list of flagged items in `analyze_project_stats()`, add it to
the returned `stats` dict under a new key, then add one more `notes.append((title, description, items, more))` tuple in `build_overview_section()`.
The note-rendering HTML/CSS (`.note-block`) is generic and needs no
changes for a new diagnostic type.

## Adding a new per-file Structure field

Each file type's Structure tab is built by one function:
`_struct_panel_html()`, `_struct_panel_css()`, or `_struct_panel_js()`.
They all follow the same shape — check whether the relevant data is
present on the `*Info` object, and if so append a `<div class="struct-sub-h">`
heading plus a table or chip list. Extract the new fact inside the
corresponding `analyze_*()` function first (so it's on the `*Info`
dataclass), then add the display block here. Don't compute new facts
inside the rendering functions — keep analysis and rendering separated, as
they are everywhere else in the script.
