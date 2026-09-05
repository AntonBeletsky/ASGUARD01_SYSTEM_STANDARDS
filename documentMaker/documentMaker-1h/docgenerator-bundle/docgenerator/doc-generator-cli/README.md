# doc-generator-cli

The standalone command-line tool. Point it at a frontend project, get back
one self-contained HTML documentation file. This is **Project 1** of the
`docgenerator` bundle — see the [top-level README](../README.md) for how it
relates to `docgenerator.skill/`, the Claude Agent Skill version.

Run it yourself, by hand, whenever you want. No LLM involved — it's a plain
Python script.

## Quick start

```bash
python3 doc_generator.py /path/to/project -o documentation.html
```

Open `documentation.html` in a browser. That's it — pure standard library,
nothing to install.

Try it on the bundled demo first:

```bash
python3 doc_generator.py examples/sample-project -o /tmp/demo.html --title "Skylark demo"
open /tmp/demo.html   # or just double-click it
```

`examples/example-documentation.html` is that exact output, already
generated, if you want to look before you run anything.

## CLI options

| Flag | Default | Description |
|---|---|---|
| `project_dir` | — | path to the root of the frontend project (required) |
| `-o, --output` | `documentation.html` | path to the output file |
| `--title` | the project folder's name | documentation title |
| `--ignore` | — | extra glob pattern to exclude files (repeatable) |
| `--no-default-ignore` | off | don't exclude node_modules/.git/dist/vendor/etc. |
| `--plan-only` | off | write a generation-plan JSON and stop -- no HTML is written |
| `--plan-output` | `<output>.plan.json` | where `--plan-only` writes the plan |
| `--from-plan PLAN_JSON` | — | render respecting a (possibly hand-edited) plan from a previous `--plan-only` run |

## Optional: the generation plan

By default the tool goes straight from scan to finished HTML in one shot --
nothing below is required for normal use. But every diagnostic here is a
heuristic (see "Known limitations"), and on a large or unusually-structured
project the default output can include sections or warnings that aren't
useful for that specific codebase. The generation plan is an optional
middle step for exactly that case: a flat JSON of binary (1/0) switches,
generated from the real findings, that you can review and edit before any
HTML gets written.

```bash
python3 doc_generator.py ./my-project -o docs.html --plan-only
# writes docs.plan.json, prints real counts, renders nothing

# open docs.plan.json, flip whatever isn't useful for this project to 0 --
# e.g. turn off orphan-selector checking for a canvas-heavy app that
# renders most of its DOM at runtime, or exclude a vendored file from
# getting its own card

python3 doc_generator.py ./my-project -o docs.html --from-plan docs.plan.json
```

The plan has five parts: `sections` (overview / dependency_graph /
cartographer_notes / color_palette), `diagnostics` (each Cartographer's-notes
check individually), `files` (`deep_analyze` per HTML/CSS/JS file -- a file
set to 0 still appears in the tree and in other files' "Depends on" lists,
just without its own card or a live link), and `assets` (the grouping
threshold from the file-importance tiers). Every default is 1 ("show it") --
the plan never turns anything off on its own, it's a lever for a person or
an agent to pull, not a second layer of heuristics. A partial or even
malformed plan file degrades gracefully: anything missing or unreadable
falls back to 1, so hand-editing just the lines you care about is safe.

## What ends up in the documentation

- **Directory map** — the full project tree in the sidebar (collapsible
  folders built on plain `<details>/<summary>`, no JS involved).
- **Project overview** — file counts by type, lines of code, size, the
  project's color palette (collected from color values in the CSS),
  responsive breakpoints, detected external libraries/CDNs.
- **Dependency map** — an SVG graph: HTML/CSS/JS files as nodes in three
  columns, with solid lines for structural references and dashed lines for
  semantic (DOM) ones.
- **A card for every file**: path, size, LOC, what it depends on and where
  it's used (structural and semantic links shown separately), plus "Code"
  (syntax highlighting) and "Structure" tabs:
  - **HTML** — title/lang/description, the h1–h6 heading outline, landmark
    tags, forms and their fields, images (checked for `alt`), every
    `id`/`class` on the page, comments.
  - **CSS** — custom properties (variables) with a color swatch preview,
    media breakpoints, `@font-face`/`@keyframes`/`@supports`, and a living
    list of rules — "selector → the author's comment → declarations" (in
    the spirit of KSS / a living style guide).
  - **JS** — imports/exports (ES modules and CommonJS), functions and
    classes together with their JSDoc (description, `@param`, `@returns`,
    `@example`), DOM access (`querySelector`, `getElementById`, …), event
    listeners, network calls (`fetch`/XHR/axios), TODO/FIXME.
- **"Cartographer's notes"** — automatic warnings: id/class declared in
  HTML but never used anywhere; CSS selectors with no match in HTML; broken
  internal links; images without `alt`.

## Architecture

```
scan_project()  → directory tree + lists of html/css/js paths
analyze_html()  → HtmlInfo   (html.parser.HTMLParser, standard library)
analyze_css()   → CssInfo    (a hand-written single-pass tokenizer)
analyze_js()    → JsInfo     (comment/string masking + regex)
build_edges()   → list of Edge (structural and DOM links between files)
analyze_project_stats() → aggregated project statistics
render_document() → assembles one HTML file via DOCUMENT_TEMPLATE (placeholders __X__)
```

Every file is parsed exactly once into a `*Info` object; those objects are
the single source of truth for displaying code, building the link graph,
and computing statistics alike. The HTML document itself is a string
template with placeholders (`__TITLE__`, `__SIDEBAR_TREE__`,
`__FILE_SECTIONS__`, etc.) filled in once inside `render_document()` via
plain `.replace()` calls — deliberately not Jinja2 or f-strings (their
`{}` would collide with literal CSS/JS) — so the script stays a single
file with zero dependencies.

The same logic and the same file, byte-for-byte, is also what powers
`docgenerator.skill/` — see `../docgenerator.skill/references/architecture.md`
for a deeper walkthrough aimed at an LLM agent using it autonomously.

## Reading it on a phone

Below 880px the sidebar becomes a slide-out drawer: tap the ☰ button
(top-left) to open it, tap a file or anywhere on the dimmed backdrop to
close it. The topbar drops its lowest-value elements (timestamp, the
HTML/CSS/JS count chips — the same counts are in the Overview cards
either way) instead of clipping them, and any table wide enough to
otherwise force the whole page sideways (a long selector, a long path)
scrolls within itself instead. A "Collapse all / Expand all" link sits
above the file tree for projects with several top-level folders.

## Known limitations (worth understanding)

This is **static, heuristic analysis**, not a full compiler:

- **JS is parsed with regular expressions**, not a real AST (Acorn/Babel/the
  TypeScript compiler API aren't available here without Node.js). Regular
  `'...'`/`"..."` string literals are deliberately NOT masked (import paths
  and selectors live inside them), so code inside a string that happens to
  look like a function declaration could in theory produce a false
  positive. Telling a regex literal `/.../` apart from a division operator
  uses a simplified rule, not the full JS grammar. `querySelector(aVariable)`
  is not resolved — only literal strings are.
- **Minified files** (detected heuristically via very long lines) aren't
  parsed in detail — only their size/badge is shown, so the documentation
  doesn't drown in unreadable output.
- **The CSS parser** is a hand-written tokenizer based on brace-balancing,
  not the formal CSS grammar; native CSS nesting (`&`) and exotic selectors
  (e.g. commas inside `:is(a, b)`) are handled approximately.
- **DOM links** are only found where the selector is a literal string in
  JS/CSS; elements created entirely dynamically (e.g. via a templating
  engine working on strings) won't show up in the dependency map.
- The script **never executes the project's code** — a plus for safety (you
  can safely point it at an untrusted third-party project) and a minus for
  accuracy (nothing that only appears at runtime is visible).

If you need fully accurate information about JS structure, the next
logical step is wiring in a real parser — see
`../docgenerator.skill/references/customization.md` for where to start.
