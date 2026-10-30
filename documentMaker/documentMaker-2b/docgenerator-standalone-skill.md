# docgenerator -- standalone skill (single file)

One self-contained Markdown file: paste it into any LLM chat, upload it as
a file, or drop it into a project's context -- no folder structure, no
separate script file to keep track of, no Agent-Skills-aware harness
required. Everything the formal `docgenerator.skill/` package spreads
across `SKILL.md` + `scripts/` + `references/` is here in one document, in
reading order.

This is a repackaging, not a rewrite -- the instructions and the script
below are the exact same content as the multi-file skill, just flattened.
If you *do* have access to the proper multi-file version (or an agent
harness that supports Anthropic Agent Skills), prefer that instead: it
keeps this same content out of context until it's actually needed, instead
of loading all of it (including the ~150KB script) up front the way a
single pasted file has to.

## How to use this file

**If the LLM reading this has code execution** (a sandbox, a bash tool,
a coding agent): find the fenced code block in the final section of this
file, "The script" -- it starts with `#!/usr/bin/env python3` and ends
with `raise SystemExit(main())`. Save exactly that block's contents to a
local file named `doc_generator.py`, then follow the instructions in
"Running it" below. This is the intended way to use this file -- the
analysis is static, deterministic Python, not something an LLM should try
to replicate by reading source files and reasoning about them by hand.

**If there's no code execution available**: the sections below still let
an LLM (or a person) explain what the tool does, how it's built, and what
it can't do -- but no real HTML documentation can be produced without
actually running the script. Say so rather than improvising a fake or
partial analysis.

---

# Frontend Project Documentation Generator

## Overview

This skill turns a folder of HTML/CSS/JS into either a browsable HTML
reference document or a spoken walkthrough — backed by the same static
analysis either way. It embeds a working, tested Python script (in full, at the end of
this file) that does the actual parsing and
cross-referencing. **Use the script, don't reimplement its logic.** It has
already been through several rounds of debugging on real edge cases (KSS-style
CSS comments, JSDoc extraction, DOM cross-referencing, minified-file
detection); redoing that analysis by hand in a single turn will be slower
and less reliable than running one command.

The script is pure Python standard library — no `pip install` needed,
works in any sandbox that has Python 3.9+.

## When to use this skill

Two distinct situations both belong to this skill:

**Mode A — the user wants a deliverable file.** Phrases like "document this
project", "generate docs for this site", "I need a reference for this
codebase I can send someone" → run the script, produce
`documentation.html`, present it as a file.

**Mode B — the user wants an explanation, not a file.** Phrases like
"what does this project do", "how is this frontend structured", "walk me
through this codebase", "what depends on what here" → you can still run the
script (it's fast and gives you ground-truth structure), then read the
resulting HTML or the underlying data yourself and answer conversationally,
instead of just handing over a file. See "Using it as an analysis tool"
below.

Don't wait for the word "documentation" — a request to understand,
summarize, or get oriented in an unfamiliar frontend project is this
skill's job even if the user describes it entirely differently.

This skill is specifically for **HTML/CSS/JS** projects (plain or close to
plain — vanilla sites, small-to-medium multi-page apps, WordPress/static-site
themes). For React/Vue/Svelte component trees, TypeScript-heavy codebases,
or backend/API documentation, see the caveats in
"Limitations reference" below before promising results.

## Running it

First, save the Python code block from "The script" section (the last
section of this file -- starts with `#!/usr/bin/env python3`, ends with
`raise SystemExit(main())`) to a local file named `doc_generator.py`.
Then:

```bash
python3 doc_generator.py <project_dir> -o <output_path>.html --title "<Project Name>"
```

Useful flags:

- `--title "..."` — set a human-readable title instead of the folder name
- `--ignore "<glob>"` — exclude extra files, repeatable
- `--no-default-ignore` — include node_modules/.git/dist/vendor/etc. (rarely wanted)

Full flag reference and internals: see "Architecture reference" below.

**Before running it**, confirm you have a real path to an existing
directory that actually contains `.html`/`.css`/`.js` files — if the user
uploaded a zip or a single file, unpack/locate the project root first. If
the scan reports 0 files found, don't just report the number — check
whether the project root was pointed at correctly, or whether everything
relevant is sitting inside a default-ignored folder (`node_modules`,
`dist`, `vendor`, …); rerun with `--no-default-ignore` if that's the case
and explain why.

**After running it** (Mode A), present the output file to the user the way
you would any generated file — don't just say it's done, make it openable.
Give a one- or two-sentence orientation ("the sidebar has the full file
tree, and there's a dependency map before the file-by-file breakdown"), not
a re-description of every section — the file speaks for itself.

## Using it as an analysis tool (Mode B)

The generated HTML is also a convenient source of ground truth for you to
read from when the user wants a conversational answer instead of a file:
run the script to a temp path, then open the HTML (or, for programmatic
answers, `import` the script's functions directly — `analyze_html`,
`analyze_css`, `analyze_js`, `build_edges` — from a short Python snippet)
to pull out exactly the facts you need: what a file depends on, which CSS
rule an element description question, whether a class is actually used
anywhere, etc. This is faster and more reliable than reading and
cross-referencing every source file by eye, especially past a handful of
files. See "Output guide" below for what each section/field means
so you can translate it into plain language for the user.

## Setting expectations honestly

This is static heuristic analysis, not a compiler and not a live browser.
It will occasionally miss something or flag a false positive (e.g. a CSS
class that's actually added by JS at runtime and looks "unused" here). When
you relay findings — especially the "Cartographer's notes" warnings
(unused id/class, orphaned CSS selectors, broken links) — phrase them as
"the analysis flags X, worth double-checking" rather than as certain fact.
The full list of known blind spots is in "Limitations reference" below;
skim it before telling a user something is definitely dead code or
definitely broken.

The same caution applies to the User Manual's badges: INFERRED means a fact
was *declared* by a convention file (package.json lists a `dev` script), not
that it was verified (the script works). And the Cartographer's notes are
labeled Warning or Note -- only call something a bug if it is labeled
Warning; a Note is worth knowing, not necessarily wrong.

## Mode C — plan first on a large or unusual project

For a large project, or one where you can already tell a specific
diagnostic is likely to be noisy for this codebase (heavily dynamic DOM,
a vendored/minified file that slipped past the minification heuristic,
a single-file-per-type project where the dependency graph will be
near-trivial), run `--plan-only` before the normal full run:

```bash
python3 doc_generator.py <project_dir> -o <output>.html --plan-only
```

This writes `<output>.plan.json` and renders nothing yet. It's a flat JSON
of 1/0 switches — `sections`, `diagnostics` (one flag per Cartographer's-notes
check), `files` (per-file `deep_analyze`) — pre-filled with the *real*
finding counts (`meta._available_diagnostic_counts`), so you can see, for
example, "orphan_css_selectors: 40 found" before deciding whether that
section is worth showing for this particular project. Edit whatever isn't
useful to `0`, then render for real with `--from-plan <output>.plan.json`.

This turns "blindly run the tool and hand over whatever it produces" into
"look at what the tool actually found, make a judgment call about what's
useful for this specific project, then produce a more focused result" —
use it when you have a real reason to expect noise, not as a default extra
step for every request; for a typical small-to-medium project the plain
run (Mode A) is simpler and just as good.

## Mode D — the User Manual, and what you must not make up

The generated file has two parts, switched from the top bar: a **Code
Manual** (tree, dependency map, a card per file) and a **User Manual** (nine
task-ordered sections for someone who will never open a source file). Every
User Manual section has a badge: AUTO and INFERRED are built from the project
(README, package.json, CSS variables, fonts); TEMPLATE means the tool has
nothing and says so; FROM docgen-manual.md means a person wrote it. A line
above the sections gives the tally ("7 of 9 built from your project, 1 written
by hand, 1 still template") -- quote it rather than calling the manual
"complete".

When the user wants a finished User Manual:

1. Generate normally and read the coverage line.
2. Run `python3 doc_generator.py <project_dir> --manual-scaffold` to create
   `docgen-manual.md` in the project root. It refuses if the file already
   exists -- never work around that, and never overwrite the file: it is the
   person's writing.
3. Fill in a section **only** with facts the user gave you or that you can
   point to in the project's own files. Do not invent FAQ questions, support
   terms, license statements, hosting instructions or feature claims to make
   the tally look better. If you don't have the facts, ask for them; if they
   aren't available, leave the hint in place -- a section that honestly
   renders as TEMPLATE is the correct outcome, not a failure.
4. Regenerate and report the new coverage line.

If a `docgen-manual.md` already exists, just regenerate: it is picked up
automatically. Don't edit the generated HTML to fill the manual in -- it is
rewritten on every run, so edits there are lost.

## What follows in this file

Everything below is inlined, not loaded on demand the way a real Skill's
`references/` folder would be (there's no separate-file mechanism in a
single pasted document) -- in order: **Architecture reference**, **Output
guide**, **Limitations reference**, **Customization reference**, then **The
script** itself, complete, in one fenced code block.

---

# Architecture reference

Deep-dive on how the script ("The script", last section of this file) works internally. Read this
when you need to explain the tool's logic, modify it, or import its
functions directly for a Mode B conversational answer.

## Contents

1. [Pipeline overview](#pipeline-overview)
2. [Data model](#data-model)
3. [HTML parsing](#html-parsing)
4. [CSS parsing](#css-parsing)
5. [JS parsing](#js-parsing)
6. [Cross-referencing (the dependency graph)](#cross-referencing-the-dependency-graph)
7. [Rendering](#rendering)
8. [The two manuals](#the-two-manuals)
9. [The generation plan](#the-generation-plan)
10. [Function reference for direct import](#function-reference-for-direct-import)

## Pipeline overview

Five sequential stages, each consuming the previous stage's output:

```
scan_project()            → directory tree + html/css/js path lists
  → analyze_html/css/js()  → one *Info object per file
    → build_edges()        → list[Edge] + used_tokens set
      → analyze_project_stats() → aggregated dict of project-wide stats
        → render_document()      → single HTML string
```

Every file is parsed **exactly once** into a typed object (`HtmlInfo`,
`CssInfo`, or `JsInfo`). That object is then the single source of truth for
three separate downstream consumers: the syntax-highlighted code display,
the dependency graph, and the aggregated statistics. There's no second pass
over file contents anywhere in the pipeline — if you're adding a new
analysis, extend the relevant `*Info` dataclass and populate it inside
`analyze_html`/`analyze_css`/`analyze_js`, don't add a parallel scan.

## Data model

All defined as `@dataclass` near the top of the script:

- **`TreeNode`** — one directory-tree node. `is_dir`, `children`, and for
  files, `kind` (`html`/`css`/`js`/`other`) and `size`.
- **`HtmlInfo`** — per HTML file: `title`, `lang`, `meta_description`,
  `headings` (list of `(level, text)`), `stylesheets`/`scripts` (raw
  href/src values), `inline_styles`/`inline_scripts`, `forms`, `images`,
  `ids`/`classes` (sets), `landmarks`, `comments`, `hrefs_internal`/`hrefs_external`,
  plus `raw` (the full source, used for the Code tab and highlighting).
- **`CssInfo`** — per CSS file: `rules` (list of `CssRuleInfo`: selectors +
  declarations + optional leading comment + line number), `at_rules` (list
  of `CssAtRuleInfo`, with `nested_rules` for `@media`/`@supports` bodies),
  `custom_props_defined`/`custom_props_used`, `colors`, `imports`,
  `breakpoints`, `unmatched_selectors` (populated later, by `build_edges`).
- **`JsInfo`** — per JS file: `imports`/`requires`/`exports`, `functions`
  (list of `JsFunctionInfo`: name, params, kind, `doc` parsed from JSDoc),
  `classes` (list of `JsClassInfo`, each with its own `methods`),
  `dom_queries`, `event_listeners`, `network_calls`, `todos`, `top_comment`.
- **`Edge`** — one link between two files: `src`, `dst`, `kind` (see
  below), optional `label`.
- **`ProjectData`** — the top-level container passed into `render_document()`:
  the tree, the three `*_files` dicts (rel_path → Info object), `other_files`,
  `edges`, and the `stats` dict from `analyze_project_stats`.

## HTML parsing

`analyze_html()` wraps a private `_HTMLAnalyzer(HTMLParser)` subclass built
on Python's standard-library `html.parser`. It tracks a tag stack, a
"currently capturing text for this heading/title" stack, and dedicated
buffers while inside `<script>`/`<style>` (whose contents `HTMLParser`
hands back as raw, unparsed text — exploited here to grab inline JS/CSS
verbatim). No external HTML parser (e.g. BeautifulSoup) is used or needed.

## CSS parsing

There's no CSS parser in the Python standard library, so `_parse_css_blocks()`
is a hand-rolled single-pass scanner that tracks brace-nesting depth
(necessary because `@media`/`@supports` bodies contain their own nested
rule blocks). It recognizes `/* ... */` comments during the same pass and,
whenever a comment sits immediately before a rule with nothing but
whitespace between them, attaches it to that rule as `CssRuleInfo.comment`
— this is a direct implementation of the
[KSS](https://github.com/kss-node/kss-node) convention where a leading
comment above a selector *is* that component's documentation. `@media`
bodies are recursively re-parsed with the same function, since a nested
rule block has the identical `selector { declarations }` shape as a
top-level one.

Selector splitting (`_split_top_level`) respects parentheses so commas
inside `:not(a, b)` or `url(a,b)` don't get treated as selector separators
— but this is a heuristic, not a full CSS grammar; see
`limitations.md`.

## JS parsing

`analyze_js()` does **not** build a real AST. It uses `_mask_js()` to
produce a same-length copy of the source where comment bodies and
backtick-template contents are blanked to spaces, then runs a battery of
targeted regexes (`_FUNCTION_DECL_RE`, `_CLASS_RE`, `_IMPORT_STATIC_RE`,
`_DOM_QUERY_RE`, etc.) against that masked text.

**Important, non-obvious design choice:** regular `'...'`/`"..."` string
literals are *not* masked, only skipped-over during the scan. That's
deliberate — import paths, `querySelector()` selector arguments, and
`addEventListener()` event names all live inside such strings, and the
whole point of parsing is to read them. Only comments and backtick
template literals (which tend to contain interpolated markup that would
otherwise cause false-positive structural matches) get blanked. If you're
extending the regex set, keep this masking behavior in mind: your regex
runs against masked text but should assume plain-quoted strings are intact.

JSDoc comments are collected separately (`_collect_jsdoc_map`, over the
*unmasked* raw source, since their content is exactly what's needed) and
attached to the nearest following declaration via `_nearest_jsdoc()`,
which tolerates `export`/`export default`/`async` sitting between the
comment and the declaration it documents.

## Cross-referencing (the dependency graph)

`build_edges()` produces two categories of `Edge`, distinguished by `kind`:

**Structural** (`link`, `script`, `css-import`, `js-import`, `js-require`,
`page-link`, `external`) — explicit references found directly in the
code: `<link href>`, `<script src>`, `@import`, `import`/`require`,
`<a href>` between project pages. Resolved via `resolve_relative()`, which
turns a relative reference into a project-root-relative path, or returns
`None` for anything external (bare specifiers, `http(s)://`, `data:`, etc.).

**Semantic** (`dom`, `style`) — not visible from following references
alone. Built by cross-checking every literal `#id`/`.class` token found in
a JS `dom_queries` entry or a CSS selector against a project-wide registry
of every `id`/`class` actually declared somewhere in the HTML. A CSS rule
targeting `.hero-title` and an HTML element with `class="hero-title"` are
linked even though neither file references the other by name or path.
This is what lets the tool say "this JS file manipulates elements on
index.html" even when index.html never appears in app.js's source text.

The same cross-check also powers the diagnostics in `analyze_project_stats()`:
any HTML `id`/`class` that's declared but never matched becomes an "unused
id/class" note; any CSS selector token that never matches any HTML file
becomes an "orphaned selector" note. These are heuristic, not certainties
— see `limitations.md`.

## Rendering

`render_document()` fills `DOCUMENT_TEMPLATE`, a triple-quoted string with
`__PLACEHOLDER__` tokens, via plain `.replace()` calls — not Jinja2, not
`.format()`/f-strings (both would collide with the literal `{`/`}` in the
embedded CSS/JS). Syntax highlighting (`highlight_html/css/js`) runs at
generation time in Python, producing `<span class="tok-...">`-wrapped HTML,
so the output file needs no client-side highlighting library. The only
client-side JavaScript (`DOC_JS`) handles things that genuinely require a
running browser: live search-as-you-type, scrollspy (`IntersectionObserver`),
and the copy-code button. Folder collapsing (`<details>/<summary>`), tab
switching (`radio` + `:checked ~`), and smooth scrolling (`scroll-behavior:
smooth`) are pure HTML/CSS with no JS dependency, so the document stays
readable even if a script fails or is blocked.

## The two manuals

The output is two parallel layouts in one file: `#code-manual` (everything
described above -- tree, dependency graph, file cards, Cartographer's
notes) and `#user-manual` (nine task-ordered sections for a reader who
will never open a source file). Both are always in the DOM unless the plan
turns one off. Two `<input type="radio" name="manual-switch">` elements
placed *before* the top bar choose between them through `:checked ~`
selectors, so switching needs no JavaScript and the offline-first
constraint is untouched. Those radios must stay earlier siblings of the
top bar and of both layouts, or the `~` selectors stop reaching them.
`<body data-manuals="both|code|user">` carries the plan's choice for the
single-manual cases, and the mobile drawer's `activeLayout()` reads the
checked radio (or `data-manuals`) to decide which of the two
`<nav class="sidebar">` elements the hamburger button opens.

**Where the User Manual's facts come from.** All of it is read once, in
`build_project_data()` -- the only place in the pipeline with filesystem
access -- and stored on `ProjectData`; rendering never reopens the project
directory.

| Field | Source | Parser |
|---|---|---|
| `package_info` | root `package.json` | `analyze_package_json()` -> `PackageInfo` (name, description, version, scripts, engines, dependencies, devDependencies, license). Malformed JSON gives `None`, never an exception. |
| `readme_raw`, `changelog_raw` | root `README` / `CHANGELOG` / `HISTORY` (`.md` or `.txt`) | `_find_root_file()`: project root only, case-insensitive |
| `manual_md` | root `docgen-manual.md` | `parse_manual_md()` |

Every read goes through `_read_optional()`: an unreadable file means "not
present" and never aborts the run.

**Sections and tiers.** `build_user_manual(pdata, plan)` returns
`(nav_html, content_html)`. Internally each section is
`(slug, title, tier, body_html)`, where `tier` is one of:

- `auto` -- derived from the scanned project (file tree, CSS custom
  properties, README shown as written);
- `inferred` -- derived from a convention (package.json's declared
  scripts/engines, "an index.html exists, so open it");
- `scaffold` -- no project data; a prompt, never invented text;
- `manual` -- hand-written, see below.

A section that mixes sources takes the *weakest* one: Requirements built
from both `engines` (package.json) and external libraries (the scan) is
`inferred`. `_confidence_badge_html(tier)` renders the badge; its labels
live in `_CONFIDENCE_TIER_LABEL`. A tier says where content came from, not
that it is correct: an `inferred` Getting started lists scripts that were
*declared*, not scripts anyone ran.

**`docgen-manual.md`.** The one place a person writes what no tool can
know. It lives in the project (next to README.md), not in the generated
HTML, because the HTML is rewritten on every run. `parse_manual_md()` splits
on `## ` headings (aliases in `_MANUAL_SECTION_ALIASES`; unknown headings
are returned in `"unknown"` and warned about on stderr), strips HTML
comments -- which is what makes the generated hints inert, so an untouched
section stays `scaffold` -- and keeps a section only if text remains. Fenced
code blocks are respected: a `## ` line inside one is code, and a comment
inside one is preserved. The overlay in `build_user_manual()` then applies:
a `scaffold` section is *replaced* by the hand-written text and becomes
`manual`; a section that already has project data keeps it and gets the
text *appended* in a `manual-note` block under its own badge, so a
person's notes are never mistaken for derived facts. `build_manual_scaffold()`
writes the starter file with hints tailored to what the scan found;
`--manual-scaffold` writes it with `open(path, "x")` (atomic no-clobber)
and refuses if the file exists -- a person's prose must never be
overwritten by a tool run.

**Coverage line.** Computed *after* the overlay (otherwise hand-written
sections would be miscounted as templates) from the tiers of the final
section list: `auto`+`inferred` count as "built from your project",
`manual` as hand-written, `scaffold` as templates. The segmented bar has
one `cov-seg confidence-<tier>` span per section.

**Markdown rendering.** `_simple_markdown_to_html()` handles headings,
paragraphs, `-`/`*` lists, fenced code blocks, and (via `_inline_md()`)
bold, inline code and links. Everything is `esc()`-escaped *first*;
`_inline_md()` then adds only its own tags, and a link only survives if its
target passes `_MD_LINK_OK_RE` (http(s), mailto, anchors, relative paths --
never `javascript:` or `data:`). Not supported: italics, tables, images.

**Code Manual changes that came with this.** Cartographer's notes are
labeled `Note` or `Warning` (`_WARNING_NOTE_TITLES`, currently only
"Unresolved links": a path that points nowhere is likely a real defect,
whereas "Unresolved DOM lookups" describes a limit of this analysis and is
deliberately a Note), warnings sorted first. Apart from those labels the
Code Manual's output is unchanged by the User Manual work -- verified by
diffing its HTML before and after.

## The generation plan

`derive_generation_plan(pdata, project_title)` turns an already-built
`ProjectData` into a flat dict of binary switches (`sections`,
`diagnostics`, per-file `files.*.deep_analyze`, `assets`) with every value
defaulted to 1 -- it repackages facts already computed elsewhere (stat
counts, diagnostic list lengths under `meta._available_diagnostic_counts`)
rather than analyzing anything new. `render_document(pdata, project_title,
plan=None)` accepts an optional plan; when omitted it synthesizes a
permissive all-1 one via `_normalize_plan({}, pdata)`, so a call with no
plan behaves identically to the version of this tool before the plan
concept existed -- this is what keeps `main()`'s default path (no
`--plan-only`/`--from-plan`) byte-for-byte unchanged.

`_normalize_plan(plan, pdata)` is the single place partial or hand-edited
plans get reconciled against the current project: any missing or invalid
key falls back to 1, and `files` is rebuilt to cover exactly the current
run's file list regardless of what the plan on disk mentions -- a plan
saved against an older version of the project degrades gracefully rather
than erroring.

Two things worth knowing if you're extending this:
- A file with `deep_analyze: 0` is excluded from `render_document()`'s
  file-card loop, but *not* from `all_paths` -- other files' "Depends
  on"/"Used in" chips still list it (via `_relations_for()`'s `linkable`
  parameter), just without an `href`, since there's no card to jump to.
  Same treatment in the sidebar tree (`_leaf_node_html()`'s `linkable`
  check) -- the file stays visible in the map, it just stops looking
  clickable.
- `sections.overview: 0` suppresses the entire `<section id="overview">`,
  including `diagnostics.*` and `sections.color_palette` -- those two are
  nested toggles *within* the overview section in the current HTML
  structure, not independent top-level sections, so they're only
  consulted when `overview` itself is 1.

- `manuals.user_manual` / `manuals.code_manual` decide which layout is
  *generated at all* (not just hidden): the disabled one's nav and content
  are left empty and `data-manuals` tells the CSS to drop the tab switcher.
  `_normalize_plan()` refuses to turn both off -- that is treated as a
  mistake and shows both rather than producing a blank document.

## Function reference for direct import

For Mode B (answering a question instead of generating a file), you can
`import` these directly rather than shelling out and re-reading HTML:

```python
import sys
sys.path.insert(0, "<directory containing doc_generator.py>")
from doc_generator import (
    build_project_data,   # one call: returns a fully populated ProjectData
    analyze_html, analyze_css, analyze_js,  # single-file analysis
    build_edges,          # (html_files, css_files, js_files) -> (edges, used_tokens)
    read_text_safe,       # encoding-tolerant file read
)

pdata = build_project_data(root=Path("/path/to/project"),
                            ignore_dirs=set(DEFAULT_IGNORE_DIRS),
                            extra_ignore_globs=[])
# pdata.html_files["index.html"].headings, pdata.edges, pdata.stats, etc.
```

This is faster than running the CLI and re-parsing the HTML output when
you just need a fact or two (e.g. "does `app.js` import `utils.js`?" is
`any(e.kind == "js-import" and e.dst == "utils.js" for e in pdata.edges if e.src == "app.js")`).

---

# Output guide

What each part of the generated `documentation.html` actually means — read
this before describing the output to a user, so the description matches
reality instead of a guess at what a UI element probably does.

## Page chrome

- **Top bar** — project title, generation timestamp, three count chips
  (HTML/CSS/JS), and a search box that live-filters the sidebar file tree
  by filename substring (not full-text search over code — see
  `limitations.md`).
- **Sidebar** — "Project overview" and "Dependency map" quick links, then
  the full directory tree. Folders are native `<details>` (top level open
  by default); files of a recognized type (HTML/CSS/JS) link to their card
  further down the page; other files (images, JSON, fonts, …) are listed
  but not clickable — they appear in the map but don't get their own
  analysis card.

## The two manuals

The top bar has two tabs. **Code Manual** is everything in the sections
below ("Project overview", "Dependency map", the per-file cards) and is for
someone who has to read or change the code. **User Manual** (next section)
is for someone who has to use or customize the project without reading a
source file. The "Search files" box only filters the Code Manual's tree, so
it is hidden while the User Manual is showing. If the plan turned one
manual off, there are no tabs and only the other one exists.

In the Cartographer's notes, each note is labeled **Warning** (likely a
real defect; currently only broken internal links) or **Note** (worth
knowing, not necessarily wrong -- unused classes, orphan selectors,
unresolved DOM lookups, images without alt, TODOs). Warnings are listed
first. Don't present a Note as a bug.

## "Project overview" section

- **Stat cards** — raw counts: files by type, total non-blank lines
  (`loc`), total size on disk.
- **Largest files** — top 5 by byte size, linking to their card.
- **Color palette** — every hex/`rgb()`/`hsla()` value found in any CSS
  file's declarations, deduplicated and shown as swatches, ordered by how
  often each color string appears. This is a **usage-frequency palette**,
  not a curated brand palette — a one-off `#ccc` used for a single border
  will appear alongside the primary brand color if it's syntactically
  present enough times. Useful for spotting the actual working palette of
  a project, not a substitute for a real design-token audit.
- **Responsive breakpoints** — every distinct `min-width`/`max-width`
  value found inside a `@media` prelude, project-wide.
- **External libraries / CDN** — script `src` values and `import`/`require`
  sources that didn't resolve to a file inside the project — i.e. anything
  loaded from a CDN or an npm package. This is a flat list of strings (URLs
  or bare specifiers), not a dependency-version report.
- **"Cartographer's notes"** — the diagnostics block. Each note names a
  *possible* issue, not a confirmed bug:
  - *Unused id/class* — declared in HTML, never matched by any CSS
    selector or JS DOM query found by this tool. Common false-positive
    cause: the class is added dynamically at runtime by JS in a way the
    static analysis can't see (a templated string, a third-party library,
    a framework directive).
  - *CSS rules with no match in HTML* — the mirror image: a selector
    targets a class/id that doesn't exist in any HTML file scanned. Same
    caveat — could be legitimately dynamic, could be dead code.
  - *Unresolved links* — an `href`/`src` that looks like a relative path
    but doesn't point at any file the scanner found. Often a real typo;
    also fires on paths outside the scanned root.
  - *Images without `alt`* — a straightforward accessibility check, no
    heuristic ambiguity here.
  - *TODO/FIXME* — every JS comment containing those markers, with file
    and line.
  - If none of these fired, the section says so explicitly rather than
    being empty/absent — don't tell a user "no notes section" when it's
    actually present and saying everything looked fine.

## "Dependency map" section

An SVG with three columns (HTML / CSS / JS), each project file as one
node. **Solid lines** are structural edges (`<link>`, `<script src>`,
`@import`, `import`/`require`, page-to-page `<a href>`). **Dashed lines**
are semantic DOM edges — a JS DOM query or a CSS selector matching an
element that lives in that HTML file. Hovering a node or edge in a real
browser shows a tooltip with the exact path/selector; a static screenshot
won't show that detail, so don't describe hover tooltips as visible by
default.

## Per-file cards

Every card, regardless of file type, has:

- **Path + badges** — file type, size, line count, and a "minified" badge
  if the heuristic in `limitations.md` triggered (in which case the
  Structure tab will be sparse or empty — that's expected, not a bug).
- **"Depends on" / "Used in"** — structural edges only, each a clickable
  chip jumping to the related file's card.
- **A second relationship row** (only shown when relevant) — semantic
  edges, labeled differently per file type: HTML shows "Styled / scripted
  from"; CSS shows "Applied on pages"; JS shows "Targets elements on".
- **"Code" tab** — the full source, syntax-highlighted. Files above ~20,000
  characters are truncated with a note, not silently cut.
- **"Structure" tab** — parsed facts, different per type:
  - *HTML*: title/lang/description/doctype, landmark tags present, the
    heading outline (indented by level), forms with their fields, images
    (flagging missing `alt`), every id/class on the page, markup comments.
  - *CSS*: rule and at-rule counts, custom properties (with a color swatch
    if the value looks like one), media breakpoints, then the rule list
    itself — each entry shows its selector(s), its leading comment if it
    had one, and a preview of its declarations (KSS-style).
  - *JS*: imports/exports table, then every function and class with its
    parsed JSDoc (description/params/returns/example) if present, DOM
    access table, event-listener table, network calls, TODOs.

## User Manual

Nine sections in reader order, each headed by a **badge** saying where its
content came from -- relay that, because it is the whole point:

| Badge | Means | Don't say |
|---|---|---|
| AUTO | derived from the project itself (file tree, CSS variables, the README shown as written) | -- |
| INFERRED | derived from a convention: `package.json` scripts/engines/dependencies, or "an index.html exists, so open it" | that the commands were *run* or *work* -- they were only declared |
| TEMPLATE (dashed outline) | no project data; a prompt for what belongs there | that it "has an FAQ/support section" -- it has a placeholder |
| FROM docgen-manual.md | written by a person; shown as-is, not checked | that the tool verified it |

The sections: **Overview** (the project's own README if there is one, else
the `package.json` description, else a stats line and a TEMPLATE),
**Requirements** (declared runtime versions, external libraries),
**Getting started** (`package.json` scripts, or "open index.html"),
**Project structure** (one row per top-level folder, linking to the Code
Manual), **Customization** (every CSS custom property with its value and a
color swatch), **Third-party credits** (declared dependencies, CDN
libraries, bundled font files, a count of bundled images -- licenses are
shown as "verify manually" because code doesn't contain them, except the
project's own `license` field), **FAQ**, **Changelog** (the project's own
CHANGELOG/HISTORY file if present), **Support**. FAQ and Support are always
TEMPLATE unless a person wrote them.

A **coverage line** with a one-segment-per-section bar sits above the
sections: "N of 9 are built from your project, M written by hand, K still
templates", plus the next step (`--manual-scaffold`, or "fill in the
remaining templates in docgen-manual.md"). Quote it instead of describing
the manual as "complete" -- a manual that is 5/9 real should be reported as
such. Sections where a person added notes to project data (e.g.
Customization) keep their original badge and show the notes beneath under
a separate FROM docgen-manual.md badge.

## Footer

A one-line disclaimer that generation is static analysis with no code
execution, and that some conclusions rely on heuristics/comments and may
be inaccurate — worth echoing to a user in your own words rather than
letting them assume the tool ran or tested the code.

---

# Limitations reference

Read this before asserting a finding is definitely true, and before taking
on a project this tool wasn't designed for. The short version: this is
static, regex/heuristic analysis of plain HTML/CSS/JS — confident about
structure, not infallible about meaning.

## What kind of projects this handles well

Vanilla or close-to-vanilla multi-page sites: static HTML pages, CSS
(including modern features — custom properties, `@media`, `@supports`,
nesting-lite), and JS written as ES modules or classic scripts, whether or
not a bundler produced them. Marketing sites, documentation sites,
small-to-medium web apps, WordPress/CMS themes exported as static assets,
course projects, legacy codebases someone needs to onboard onto.

## What it handles poorly — say so before promising results

- **React/Vue/Svelte/Angular component trees.** The script has no concept
  of JSX, `.vue` single-file components, or template directives. If a
  project is mostly `.jsx`/`.tsx`/`.vue` files, the HTML/CSS/JS analysis
  will be thin or misleading — most of the real structure lives in syntax
  this tool doesn't parse. Say this upfront rather than running it and
  presenting a sparse result as if it were complete. `.jsx` files *are*
  scanned as JS (regex-only, no JSX awareness), which will pick up some
  imports/functions but nothing about props, hooks, or component structure.
- **TypeScript.** `.ts`/`.tsx` aren't in the default `JS_EXTS` scan list at
  all — they show up in the directory tree as "other" files, not analyzed.
  Don't imply TS files were checked.
- **Utility-first CSS (Tailwind and similar).** The CSS parser assumes
  meaningful author-written rules with selectors that map to specific
  components. A Tailwind project's actual CSS file is often almost entirely
  generated utility classes; the "living style guide" rule listing will be
  either enormous or (if Tailwind is compiled separately and not in the
  scanned tree) show almost nothing meaningful. The dependency graph and
  KSS-style comments add little value here.
- **CSS-in-JS (styled-components, Emotion, etc.) and CSS Modules.** Styles
  defined inside `.js` template literals or with build-time class-name
  hashing aren't connected to anything by this tool's CSS parser — it only
  understands actual `.css` files with literal class names.
- **Bundled/minified output.** If the "project" you're pointed at is
  actually a `dist/`/`build/` folder, most files will hit the minified-file
  heuristic and get skipped from detailed analysis (by design — see
  below). Point the tool at *source*, not build output, whenever both
  exist.

## Specific heuristics and their failure modes

- **Minified-file detection** — triggers on very long average line length.
  A false positive (skipping a real, readable file) is possible if someone
  writes genuinely long single-purpose lines; a false negative (treating a
  lightly-minified file as normal) is possible for gently compressed code
  that still has some newlines. If Structure looks suspiciously empty for
  a file that should have content, check whether it got flagged minified.
- **JS parsing is regex-based, not an AST.** It can miss constructs it
  wasn't written to recognize (unusual export syntax, decorators,
  generators mixed with other patterns) and, rarely, misfire on code
  inside a string that happens to look like a declaration (regular quoted
  strings are intentionally left unmasked — see `architecture.md` — so
  their contents are visible to the same regexes that scan real code).
  `querySelector(someVariable)` — anything not a literal string argument —
  is invisible to the DOM cross-referencing; the tool only sees literal
  selectors.
- **Regex-literal vs. division ambiguity** (`/pattern/` vs `a / b`) has no
  clean solution without a full tokenizer; a simplified rule is used. Very
  rare in practice, but a possible source of a stray highlighting glitch.
- **CSS selector splitting** assumes commas inside `()`/`[]` aren't
  selector separators, which covers `:not(a, b)` and `url(...)` correctly
  but isn't the full CSS grammar — deeply unusual selectors may split
  wrong.
- **"Unused id/class" and "orphaned CSS selector" notes** are the most
  likely to produce false positives, because they require the *absence*
  of a match across the whole project, and dynamically-added
  classes/elements (from JS, from a CMS, from a component the crawler
  can't see into) are invisible to a static scan by definition. Phrase
  these as "worth checking", not "confirmed dead code," when relaying them.
- **No code execution, ever.** Nothing that only exists at runtime (DOM
  nodes JS creates, styles applied conditionally, content injected from an
  API) is visible. This is intentional (the tool needs to be safe to run
  against untrusted third-party projects) but means the analysis is a
  static lower bound on what the site actually does, not a complete
  runtime picture.

## User Manual specifics

- **A tier is provenance, not correctness.** INFERRED means "derived from
  a convention", not "verified": package.json can declare a `dev` script that
  has been broken for a year, and the Getting started table will list it.
- **Only the project root is read** for `package.json`, `README`,
  `CHANGELOG`/`HISTORY` and `docgen-manual.md`. A monorepo's package.json in a
  subfolder, or a README that lives in `docs/`, is not picked up.
- **Per-dependency licenses are not read.** Only the project's own
  `license` field is available from package.json; each dependency's license
  lives in its own package (inside `node_modules`, which is ignored). Fonts,
  icons and images are listed as "verify manually" because who made them
  and under what terms is not in the files. This matters: marketplace
  documentation standards require crediting every third-party asset, and
  the tool can only point at the gap, not fill it.
- **Nothing about deployment, hosting, accounts, pricing or support terms
  can be known** -- those sections are TEMPLATE by design, and the right
  response to a request to "fill them in" is to get the facts from the
  person, not to write plausible ones.
- **Markdown is minimal**: headings, paragraphs, lists, fenced code, bold,
  inline code, links. No italics, tables or images -- a README that leans on
  them still shows, just less prettily.
- **Overview with no README and no package.json description** is a stats
  line plus a TEMPLATE; the tool can describe structure, not purpose.
- **`docgen-manual.md`**: only `## ` headings are sections (a heading it
  doesn't recognize is ignored with a warning on stderr, not an error).
  Duplicate headings are concatenated.

## What to do when you hit one of these

Don't silently work around a limitation by inventing an answer from
general knowledge instead of the tool's actual output — say plainly what
the tool could and couldn't determine, and offer to look at the specific
file by hand (reading the source directly) if the user needs certainty on
a point the static analysis is weak on. For framework-heavy or TypeScript
projects, it's fine to still run the tool for the parts it *can* see
(plain CSS files, any vanilla JS, the overall file tree) while being clear
that the component-level story is missing.

---

# Customization reference

Read this only when a user explicitly asks for a modified version of the
tool or its output theme — not needed for a normal documentation request.
Every pointer below names the exact constant/function to edit in
"The script" section at the end of this file.

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

## Adding or changing a User Manual section

The nine sections are built inside `build_user_manual()`, one block each,
appending `(slug, title, tier, body_html)` to `sections`; the nav, the
content, the coverage line and the `docgen-manual.md` overlay are all
derived from that one list, so a new section needs no other wiring:

1. Add a block that appends a tuple. Use `um-<name>` for the slug (it is the
   HTML id) and pick the tier honestly: `auto` only for facts derived from
   the project, `inferred` for convention-derived, `scaffold` for "no data --
   here is what belongs here". Never put invented prose in an `auto`/`inferred`
   body.
2. Add it to `_MANUAL_SECTION_ORDER` (so `--manual-scaffold` writes a heading
   and hint for it) and, if it has natural alternate names, to
   `_MANUAL_SECTION_ALIASES`. Add a hint for it in `build_manual_scaffold()`.
3. The coverage line says "of 9" from `len(sections)`, so it updates itself.

To change what counts as a *Warning* in the Code Manual, edit
`_WARNING_NOTE_TITLES`: add a note's title only if it is likely a real
defect rather than a limit of the analysis.

---

# The script

Save exactly the contents of the fenced block below to a file named
`doc_generator.py`. Pure standard library, Python 3.9+, nothing to install.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_generator.py
=================

Documentation generator for frontend projects (HTML/CSS/JS).

Walks a project directory, builds a file/directory tree, parses every
HTML/CSS/JS file with awareness of that language's own syntax, finds the
relationships between files (structural links as well as "meaning-level"
links through shared id/class/selectors), and packages all of it into a
single self-contained HTML documentation file (its CSS and JS are inlined,
no network access is required to read it).

Uses the Python standard library only — nothing else needs to be installed.

Usage:
    python3 doc_generator.py /path/to/project -o docs.html

See README.md next to this file for the full option list.
"""

from __future__ import annotations

import argparse
import html as html_stdlib
import json
import os
import re
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Optional, Iterable
from urllib.parse import urlsplit

# --------------------------------------------------------------------------
# Configuration constants
# --------------------------------------------------------------------------

VERSION = "1.0.0"

#: Directories that are never analyzed (typical build/tooling noise)
DEFAULT_IGNORE_DIRS = {
    "node_modules", ".git", ".svn", ".hg", "dist", "build", "out",
    ".next", ".nuxt", ".cache", "coverage", "__pycache__", ".idea",
    ".vscode", "vendor", ".parcel-cache", ".turbo", ".vercel",
}

#: Extensions parsed as "source" for the three languages
HTML_EXTS = {".html", ".htm"}
CSS_EXTS = {".css"}
JS_EXTS = {".js", ".mjs", ".cjs", ".jsx"}

#: Extensions that show up in the directory map but aren't parsed in depth
KNOWN_OTHER_EXTS = {
    ".json", ".md", ".txt", ".svg", ".png", ".jpg", ".jpeg", ".gif",
    ".webp", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".map", ".yml",
    ".yaml", ".xml", ".scss", ".sass", ".less", ".ts", ".tsx", ".vue",
}

#: "Looks minified" threshold: if the average line length exceeds this,
#: the file is treated as minified and not parsed in detail (otherwise the
#: documentation would drown in an unreadable wall of text).
MINIFIED_AVG_LINE_LEN = 300
MINIFIED_MAX_FILE_FOR_FULL_DUMP = 20000  # chars, beyond which shown code is truncated

JS_KEYWORDS = {
    "break", "case", "catch", "class", "const", "continue", "debugger",
    "default", "delete", "do", "else", "export", "extends", "finally",
    "for", "function", "if", "import", "in", "instanceof", "let", "new",
    "return", "super", "switch", "this", "throw", "try", "typeof", "var",
    "void", "while", "with", "yield", "async", "await", "of", "static",
    "get", "set", "null", "true", "false", "undefined", "from", "as",
}

# Keywords that syntactically look like "name(...) {" but are not actually
# function/method declarations — so they don't get mistaken for one.
JS_CONTROL_KEYWORDS = {
    "if", "for", "while", "switch", "catch", "function", "return",
    "with", "do",
}


# --------------------------------------------------------------------------
# General utilities
# --------------------------------------------------------------------------

def read_text_safe(path: Path) -> str:
    """Reads a text file, tolerant of encoding issues."""
    for enc in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return path.read_bytes().decode("utf-8", errors="replace")


def human_size(num: int) -> str:
    """Formats a byte count as a human-readable size (KB, MB...)."""
    size = float(num)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def slugify(rel_path: str) -> str:
    """Turns a file's relative path into a safe id for an HTML anchor."""
    return "f-" + re.sub(r"[^a-zA-Z0-9_-]+", "-", rel_path).strip("-").lower()


def esc(text: Optional[str]) -> str:
    """HTML-escaping that tolerates None."""
    if text is None:
        return ""
    return html_stdlib.escape(str(text), quote=True)


def is_probably_minified(text: str) -> bool:
    """Heuristic: a file collapsed into one giant line is probably minified."""
    lines = text.splitlines() or [""]
    longest = max((len(ln) for ln in lines), default=0)
    avg = sum(len(ln) for ln in lines) / max(len(lines), 1)
    return longest > 2000 or (avg > MINIFIED_AVG_LINE_LEN and len(lines) < 10)


def count_loc(text: str) -> int:
    """Number of non-blank lines (used as an approximation of LOC)."""
    return sum(1 for ln in text.splitlines() if ln.strip())


def resolve_relative(base_file_rel: str, ref: str) -> Optional[str]:
    """
    Attempts to resolve a relative reference (href/src/@import/import) from
    an HTML/CSS/JS file into a project-root-relative path.
    Returns None if the reference is external (http(s)://, protocol-relative,
    data:, a bare specifier without ./ or ../ for JS, etc.) — such references
    are treated as "external dependencies" rather than project files.
    """
    if not ref:
        return None
    ref = ref.strip().strip("'\"")
    if ref.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
        return None
    parsed = urlsplit(ref)
    if parsed.scheme or ref.startswith("//"):
        return None  # external resource (http(s)://, //cdn...)
    ref_path = parsed.path
    if not ref_path:
        return None
    base_dir = PurePosixPath(base_file_rel).parent
    combined = (base_dir / ref_path)
    # normalize ".." and "."
    parts: list[str] = []
    for part in combined.parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part == ".":
            continue
        else:
            parts.append(part)
    return str(PurePosixPath(*parts)) if parts else None


# --------------------------------------------------------------------------
# Data models
# --------------------------------------------------------------------------

@dataclass
class TreeNode:
    """A node in the directory tree (the project map)."""
    name: str
    rel_path: str
    is_dir: bool
    children: list["TreeNode"] = field(default_factory=list)
    kind: str = ""       # 'html' | 'css' | 'js' | 'other' | '' (for directories)
    size: int = 0


@dataclass
class HtmlInfo:
    rel_path: str
    title: str = ""
    lang: str = ""
    meta_description: str = ""
    doctype_ok: bool = False
    headings: list[tuple] = field(default_factory=list)      # (level:int, text:str)
    stylesheets: list[str] = field(default_factory=list)      # raw href
    scripts: list[dict] = field(default_factory=list)         # {src, defer, async, module, inline}
    inline_styles: list[str] = field(default_factory=list)
    inline_scripts: list[str] = field(default_factory=list)
    forms: list[dict] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    ids: set = field(default_factory=set)
    classes: set = field(default_factory=set)
    attr_pairs: set = field(default_factory=set)  # {(attr_name, attr_value), ...} -- docgen-002
    landmarks: set = field(default_factory=set)
    comments: list[str] = field(default_factory=list)
    hrefs_internal: list[str] = field(default_factory=list)
    hrefs_external: list[str] = field(default_factory=list)
    word_count: int = 0
    loc: int = 0
    size: int = 0
    is_minified: bool = False
    raw: str = ""


@dataclass
class CssRuleInfo:
    selectors: list[str]
    declarations: list[tuple]   # (prop, value)
    comment: Optional[str]
    line: int


@dataclass
class CssAtRuleInfo:
    kind: str          # media / import / keyframes / font-face / supports / charset / other
    prelude: str
    comment: Optional[str]
    line: int
    nested_rules: list[CssRuleInfo] = field(default_factory=list)


@dataclass
class CssInfo:
    rel_path: str
    rules: list[CssRuleInfo] = field(default_factory=list)
    at_rules: list[CssAtRuleInfo] = field(default_factory=list)
    custom_props_defined: dict = field(default_factory=dict)
    custom_props_used: set = field(default_factory=set)
    colors: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    breakpoints: set = field(default_factory=set)
    unmatched_selectors: list = field(default_factory=list)
    loc: int = 0
    size: int = 0
    is_minified: bool = False
    raw: str = ""


@dataclass
class JsFunctionInfo:
    name: str
    params: list[str]
    kind: str            # function | arrow | method | constructor
    is_exported: bool
    doc: Optional[dict]   # {description, params:{}, returns:str, examples:[]}
    line: int


@dataclass
class JsClassInfo:
    name: str
    extends: Optional[str]
    methods: list[JsFunctionInfo]
    doc: Optional[dict]
    line: int


@dataclass
class JsInfo:
    rel_path: str
    imports: list[dict] = field(default_factory=list)     # {source, names, default_name, namespace}
    requires: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    functions: list[JsFunctionInfo] = field(default_factory=list)
    classes: list[JsClassInfo] = field(default_factory=list)
    dom_queries: list[dict] = field(default_factory=list)  # {method, selector, line}
    class_writes: list[dict] = field(default_factory=list)  # {class_name, line} -- docgen-004
    event_listeners: list[dict] = field(default_factory=list)
    network_calls: list[dict] = field(default_factory=list)
    todos: list[dict] = field(default_factory=list)
    top_comment: Optional[str] = None
    loc: int = 0
    size: int = 0
    is_minified: bool = False
    raw: str = ""


@dataclass
class Edge:
    src: str
    dst: str
    kind: str            # link|script|css-import|js-import|js-require|dom|style|external|unresolved
    label: str = ""


@dataclass
class ProjectData:
    root_name: str
    generated_at: str
    tree: TreeNode
    html_files: dict            # rel_path -> HtmlInfo
    css_files: dict             # rel_path -> CssInfo
    js_files: dict               # rel_path -> JsInfo
    other_files: list            # rel_path list
    edges: list
    stats: dict
    package_info: Optional["PackageInfo"] = None   # docgen-h2
    manual_md: Optional[dict] = None                # docgen-h5
    readme_raw: Optional[str] = None                # docgen-h4, root README.md if found
    readme_path: Optional[str] = None
    changelog_raw: Optional[str] = None              # docgen-h4, root CHANGELOG.md/HISTORY.md if found
    changelog_path: Optional[str] = None


# --------------------------------------------------------------------------
# Project scanner: builds the directory tree and file lists
# --------------------------------------------------------------------------

def classify_ext(ext: str) -> str:
    ext = ext.lower()
    if ext in HTML_EXTS:
        return "html"
    if ext in CSS_EXTS:
        return "css"
    if ext in JS_EXTS:
        return "js"
    return "other"


# docgen-006: a second, orthogonal axis to classify_ext -- "can this tool
# parse it deeply" (unchanged, still just html/css/js) vs. "is this worth a
# person's attention in the file tree". A .php file with real logic and a
# favicon.svg both land in classify_ext's "other" bucket, but they should
# not look identical in the sidebar. Used for tree/sidebar display only --
# it does not change which files get deep analysis.
SOURCE_OTHER_EXTS = {".php", ".jsx", ".tsx", ".vue", ".ts", ".scss", ".sass", ".less"}
CONFIG_EXTS = {".json", ".yaml", ".yml", ".toml", ".xml"}
CONFIG_NAMES = {".env", ".gitignore", ".editorconfig", ".npmrc", ".browserslistrc"}
DOCS_EXTS = {".md", ".txt", ".rst"}
#: below this many asset-tier files at one directory level, list them
#: individually rather than collapsing into one "Assets (N)" group -- not
#: worth the extra click for just one or two icons.
ASSET_GROUP_THRESHOLD = 4


def classify_importance(name: str, ext: str) -> str:
    """Returns 'source-other' | 'config' | 'docs' | 'asset' for any file
    classify_ext already called 'other'. Never called for html/css/js."""
    ext = ext.lower()
    if ext in SOURCE_OTHER_EXTS:
        return "source-other"
    if ext in CONFIG_EXTS or name.lower() in CONFIG_NAMES:
        return "config"
    if ext in DOCS_EXTS:
        return "docs"
    return "asset"


# --------------------------------------------------------------------------
# docgen-h2: package.json parsing. classify_importance() above already
# tiers package.json as "config" for sidebar display (docgen-006); this is
# the first thing that actually reads its content. Deliberately narrow --
# this is a convention-file reader, not a general JSON/npm-ecosystem
# analyzer, so it only pulls the handful of fields the User Manual
# (docgen-h4) needs and stays silent (returns None) on anything it can't
# confidently parse rather than guessing.
# --------------------------------------------------------------------------

@dataclass
class PackageInfo:
    name: str = ""
    description: str = ""
    version: str = ""
    scripts: dict = field(default_factory=dict)        # {"dev": "vite", ...}
    engines: dict = field(default_factory=dict)         # {"node": ">=18", ...}
    dependencies: dict = field(default_factory=dict)    # {"react": "^18.2.0", ...}
    dev_dependencies: dict = field(default_factory=dict)
    license: str = ""


def analyze_package_json(raw: str) -> Optional[PackageInfo]:
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(data, dict):
        return None

    def _str(key):
        v = data.get(key, "")
        return v if isinstance(v, str) else ""

    def _dict(key):
        v = data.get(key, {})
        return v if isinstance(v, dict) else {}

    return PackageInfo(
        name=_str("name"),
        description=_str("description"),
        version=_str("version"),
        scripts=_dict("scripts"),
        engines=_dict("engines"),
        dependencies=_dict("dependencies"),
        dev_dependencies=_dict("devDependencies"),
        license=_str("license"),
    )


# docgen-h4: convention-file lookup for the User Manual's Overview and
# Changelog sections -- "root" means directly in the project directory,
# not nested in a subfolder, matching where these files are conventionally
# expected to live (and where a README inside node_modules/some-dep would
# NOT match).
_README_NAMES = ("readme.md", "readme.txt", "readme")
_CHANGELOG_NAMES = ("changelog.md", "changelog.txt", "history.md", "history.txt")


def _read_optional(root: Path, rel: Optional[str]) -> Optional[str]:
    """Read a convention file if it exists; an unreadable one (permissions,
    a directory with that name) degrades to "not present" instead of
    aborting the whole documentation run."""
    if not rel:
        return None
    try:
        return read_text_safe(root / rel)
    except OSError:
        return None


def _find_root_file(other_files: list, candidate_names: tuple) -> Optional[str]:
    for path in other_files:
        if "/" not in path and path.lower() in candidate_names:
            return path
    return None


# Link targets allowed through _inline_md: http(s), mailto, anchors, and
# plain relative paths. Anything else (javascript:, data:, ...) stays as
# literal text instead of becoming a link.
_MD_LINK_OK_RE = re.compile(r"^(https?://|mailto:|#|\./|\.\./|[\w./-]+$)", re.IGNORECASE)


def _inline_md(escaped: str) -> str:
    """Bold, inline code and links. Runs on text that has ALREADY been
    esc()-escaped, so the only HTML this can emit is the handful of tags
    added right here -- source text can never inject markup."""
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)

    def _link(m):
        return f'<a href="{m.group(2)}">{m.group(1)}</a>' if _MD_LINK_OK_RE.match(m.group(2)) else m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _link, escaped)


def _simple_markdown_to_html(text: str) -> str:
    """Deliberately minimal: headings, paragraphs, -/* bullet lists, plus
    inline bold / code / links (see _inline_md). No italics, tables, images
    or code fences -- good enough to make a README or CHANGELOG readable
    inline without reimplementing a markdown engine; every token is
    esc()-escaped first, so this never introduces unescaped HTML even if
    the source file contains some."""
    lines = text.replace("\r\n", "\n").split("\n")
    out, para_buf, in_list = [], [], False
    fence_buf = None            # None = not inside a fenced code block

    def code_block(buf):
        return '<pre class="md-code"><code>' + esc("\n".join(buf)) + "</code></pre>"

    def flush_para():
        if para_buf:
            out.append("<p>" + _inline_md(" ".join(esc(l) for l in para_buf)) + "</p>")
            para_buf.clear()

    for line in lines:
        stripped = line.strip()
        if fence_buf is not None:                       # inside ``` ... ```
            if re.match(r"^(```|~~~)\s*$", stripped):
                out.append(code_block(fence_buf))
                fence_buf = None
            else:
                fence_buf.append(line)                  # keep indentation, no inline markup
            continue
        if re.match(r"^(```|~~~)", stripped):
            flush_para()
            if in_list:
                out.append("</ul>")
                in_list = False
            fence_buf = []
            continue
        if not stripped:
            flush_para()
            if in_list:
                out.append("</ul>")
                in_list = False
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if m:
            flush_para()
            if in_list:
                out.append("</ul>")
                in_list = False
            level = min(len(m.group(1)) + 2, 6)  # offset below the page's own h1/h2
            out.append(f"<h{level}>{_inline_md(esc(m.group(2)))}</h{level}>")
            continue
        m = re.match(r"^[-*]\s+(.*)", stripped)
        if m:
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline_md(esc(m.group(1)))}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        para_buf.append(stripped)
    flush_para()
    if in_list:
        out.append("</ul>")
    if fence_buf is not None:                           # unterminated fence: show it, don't swallow it
        out.append(code_block(fence_buf))
    return "\n".join(out)


def scan_project(root: Path, ignore_dirs: set, extra_ignore_globs: list) -> tuple:
    """
    Walks the project directory.
    Returns (tree: TreeNode, html_paths, css_paths, js_paths, other_paths).
    Paths are relative (posix-style) to root.
    """
    html_paths, css_paths, js_paths, other_paths = [], [], [], []

    def should_ignore_dir(dirname: str) -> bool:
        if dirname in ignore_dirs:
            return True
        if dirname.startswith(".") and dirname not in (".",):
            return True
        return False

    def build(dir_path: Path, rel: str) -> TreeNode:
        node = TreeNode(name=dir_path.name or root.name, rel_path=rel, is_dir=True)
        try:
            entries = sorted(
                dir_path.iterdir(),
                key=lambda p: (p.is_file(), p.name.lower()),
            )
        except PermissionError:
            return node
        for entry in entries:
            entry_rel = f"{rel}/{entry.name}" if rel else entry.name
            if entry.is_dir():
                if should_ignore_dir(entry.name):
                    continue
                child = build(entry, entry_rel)
                if child.children:  # skip directories that end up fully empty
                    node.children.append(child)
            else:
                if any(entry.match(g) for g in extra_ignore_globs):
                    continue
                routing_kind = classify_ext(entry.suffix)
                # docgen-006: TreeNode.kind drives sidebar display and is
                # allowed to be more specific than the html/css/js/other
                # routing_kind above, which still controls what gets deeply
                # analyzed and must NOT change here.
                display_kind = (routing_kind if routing_kind != "other"
                                 else classify_importance(entry.name, entry.suffix))
                try:
                    size = entry.stat().st_size
                except OSError:
                    size = 0
                child = TreeNode(
                    name=entry.name, rel_path=entry_rel, is_dir=False,
                    kind=display_kind, size=size,
                )
                node.children.append(child)
                if routing_kind == "html":
                    html_paths.append(entry_rel)
                elif routing_kind == "css":
                    css_paths.append(entry_rel)
                elif routing_kind == "js":
                    js_paths.append(entry_rel)
                else:
                    other_paths.append(entry_rel)
        return node

    tree = build(root, "")
    return tree, html_paths, css_paths, js_paths, other_paths


# --------------------------------------------------------------------------
# HTML parsing: built on html.parser.HTMLParser from the standard library
# --------------------------------------------------------------------------

from html.parser import HTMLParser  # noqa: E402  (fine after the constant blocks)

_LANDMARK_TAGS = {"header", "nav", "main", "footer", "article", "aside", "section"}
_CAPTURE_TEXT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "title"}


class _HTMLAnalyzer(HTMLParser):
    """Single-pass parse of HTML into an HtmlInfo structure.

    Namespaced with a leading underscore because it is an internal detail of
    analyze_html() and not part of the public API of this module.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.lang = ""
        self.meta_description = ""
        self.doctype_ok = False
        self.headings: list[tuple] = []
        self.stylesheets: list[str] = []
        self.scripts: list[dict] = []
        self.inline_styles: list[str] = []
        self.inline_scripts: list[str] = []
        self.forms: list[dict] = []
        self.images: list[dict] = []
        self.ids: set = set()
        self.classes: set = set()
        self.attr_pairs: set = set()  # docgen-002
        self.landmarks: set = set()
        self.comments: list[str] = []
        self.hrefs: list[str] = []
        self.word_count = 0

        self._capture_stack: list = []     # [[tag, [text_parts]], ...]
        self._tag_stack: list = []
        self._in_script = False
        self._in_style = False
        self._raw_buffer: list = []
        self._current_form: Optional[dict] = None

    # -- HTMLParser callbacks --------------------------------------

    def handle_decl(self, decl):
        if decl.strip().lower().startswith("doctype html"):
            self.doctype_ok = True

    def handle_starttag(self, tag, attrs):
        self._handle_open(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag, attrs):
        self._handle_open(tag, attrs, self_closing=True)

    def _handle_open(self, tag, attrs, self_closing):
        a = {k: (v if v is not None else "") for k, v in attrs}
        self._tag_stack.append(tag)

        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]

        if tag in _CAPTURE_TEXT_TAGS:
            self._capture_stack.append([tag, []])

        if tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.meta_description = a.get("content", "")

        if tag == "link":
            rel = a.get("rel", "").lower()
            if "stylesheet" in rel and a.get("href"):
                self.stylesheets.append(a["href"])

        if tag == "script":
            if a.get("src"):
                self.scripts.append({
                    "src": a["src"],
                    "defer": "defer" in a,
                    "async": "async" in a,
                    "module": a.get("type", "") == "module",
                    "inline": False,
                })
                self._in_script = False
            else:
                self._in_script = True
                self._raw_buffer = []

        if tag == "style":
            self._in_style = True
            self._raw_buffer = []

        if tag == "form":
            self._current_form = {
                "action": a.get("action", ""),
                "method": a.get("method", "get"),
                "fields": [],
            }

        if tag in ("input", "select", "textarea") and self._current_form is not None:
            field_name = a.get("name") or a.get("id") or a.get("type", "field")
            self._current_form["fields"].append(field_name)

        if tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt", "")})

        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])

        if tag in _LANDMARK_TAGS:
            self.landmarks.add(tag)

        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("class"):
            for c in a["class"].split():
                self.classes.add(c)
        # docgen-002: every attribute, generically -- this is what lets a JS
        # or CSS attribute selector like [data-ref="x"] get cross-referenced
        # the same way #id/.class already were. Not filtered by attr name:
        # a selector could target any of them (aria-*, type, data-*, ...).
        for attr_name, attr_value in a.items():
            if attr_value:
                self.attr_pairs.add((attr_name, attr_value))

        if self_closing:
            self._handle_close(tag)

    def handle_endtag(self, tag):
        self._handle_close(tag)

    def _handle_close(self, tag):
        if self._tag_stack and tag in self._tag_stack:
            # unwind the stack down to the matching tag (tolerant of unclosed tags like <br>)
            while self._tag_stack and self._tag_stack[-1] != tag:
                self._tag_stack.pop()
            if self._tag_stack:
                self._tag_stack.pop()

        if self._capture_stack and self._capture_stack[-1][0] == tag:
            _, parts = self._capture_stack.pop()
            text = "".join(parts).strip()
            text = re.sub(r"\s+", " ", text)
            if tag == "title":
                self.title = text
            else:
                self.headings.append((int(tag[1]), text))

        if tag == "script" and self._in_script:
            code = "".join(self._raw_buffer)
            if code.strip():
                self.inline_scripts.append(code)
            self._in_script = False

        if tag == "style" and self._in_style:
            css_text = "".join(self._raw_buffer)
            if css_text.strip():
                self.inline_styles.append(css_text)
            self._in_style = False

        if tag == "form" and self._current_form is not None:
            self.forms.append(self._current_form)
            self._current_form = None

    def handle_data(self, data):
        if self._in_script or self._in_style:
            self._raw_buffer.append(data)
            return
        if self._capture_stack:
            self._capture_stack[-1][1].append(data)
        text = data.strip()
        if text:
            self.word_count += len(text.split())

    def handle_comment(self, data):
        text = data.strip()
        if text:
            self.comments.append(text)


def analyze_html(rel_path: str, raw: str) -> HtmlInfo:
    parser = _HTMLAnalyzer()
    try:
        parser.feed(raw)
        parser.close()
    except Exception:
        # HTMLParser rarely throws, but one bad file shouldn't kill the whole run
        pass

    internal, external = [], []
    for href in parser.hrefs:
        target = resolve_relative(rel_path, href)
        if target:
            internal.append(target)
        elif not href.startswith("#"):
            external.append(href)

    info = HtmlInfo(
        rel_path=rel_path,
        title=parser.title,
        lang=parser.lang,
        meta_description=parser.meta_description,
        doctype_ok=parser.doctype_ok,
        headings=parser.headings,
        stylesheets=parser.stylesheets,
        scripts=parser.scripts,
        inline_styles=parser.inline_styles,
        inline_scripts=parser.inline_scripts,
        forms=parser.forms,
        images=parser.images,
        ids=parser.ids,
        classes=parser.classes,
        attr_pairs=parser.attr_pairs,
        landmarks=parser.landmarks,
        comments=parser.comments,
        hrefs_internal=internal,
        hrefs_external=external,
        word_count=parser.word_count,
        loc=count_loc(raw),
        size=len(raw.encode("utf-8", errors="ignore")),
        is_minified=is_probably_minified(raw),
        raw=raw,
    )
    return info


# --------------------------------------------------------------------------
# CSS parsing: a small hand-written tokenizer (no external dependencies)
#
# CSS isn't in the Python standard library, so this parser is hand-rolled:
# a single-pass scanner that tracks brace nesting depth (needed for
# @media/@supports/@keyframes, where braces nest), which also recognizes
# comments and attaches a comment sitting right before a rule to that rule
# — modeled on KSS (Knyle Style Sheets) syntax, where a leading comment is
# the component's documentation.
# --------------------------------------------------------------------------

_COLOR_RE = re.compile(
    r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)"
)
_VAR_USAGE_RE = re.compile(r"var\(\s*(--[a-zA-Z0-9_-]+)")
_BREAKPOINT_RE = re.compile(
    r"(min-width|max-width|min-height|max-height)\s*:\s*([\d.]+[a-z%]*)"
)


def _split_top_level(text: str, sep: str) -> list:
    """Splits a string on a separator, ignoring one that's inside ()/[]/strings."""
    parts, buf, depth = [], [], 0
    in_str = None
    i = 0
    while i < len(text):
        ch = text[i]
        if in_str:
            buf.append(ch)
            if ch == "\\" and i + 1 < len(text):
                buf.append(text[i + 1])
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in "'\"":
            in_str = ch
            buf.append(ch)
        elif ch in "([":
            depth += 1
            buf.append(ch)
        elif ch in ")]":
            depth -= 1
            buf.append(ch)
        elif ch == sep and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
        i += 1
    parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def _parse_css_blocks(text: str) -> list:
    """
    Single-pass scan of a CSS text (or an @media body).
    Returns a list of blocks: {'type': 'rule'|'at-simple'|'at-block',
                                'prelude': str, 'body': str|None,
                                'comment': str|None, 'line': int}
    """
    n = len(text)
    i = 0
    blocks = []
    last_comment = None

    while i < n:
        ch = text[i]

        if ch in " \t\r\n":
            i += 1
            continue

        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            end = n if end == -1 else end
            last_comment = text[i + 2:end].strip()
            i = (end + 2) if end < n else n
            continue

        line_no = text.count("\n", 0, i) + 1

        if ch == "@":
            j = i
            depth_brk = 0
            while j < n and text[j] not in "{;":
                if text[j] == "/" and j + 1 < n and text[j + 1] == "*":
                    break
                j += 1
            prelude = text[i:j].strip()
            if j < n and text[j] == ";":
                blocks.append({"type": "at-simple", "prelude": prelude,
                                "body": None, "comment": last_comment, "line": line_no})
                i = j + 1
            elif j < n and text[j] == "{":
                depth = 1
                k = j + 1
                while k < n and depth > 0:
                    if text[k] == "{":
                        depth += 1
                    elif text[k] == "}":
                        depth -= 1
                    k += 1
                body = text[j + 1:k - 1]
                blocks.append({"type": "at-block", "prelude": prelude,
                                "body": body, "comment": last_comment, "line": line_no})
                i = k
            else:
                i = n
            last_comment = None
            continue

        # a normal rule: selector(s) { declarations }
        j = i
        while j < n and text[j] not in "{}":
            if text[j] == "/" and j + 1 < n and text[j + 1] == "*":
                # a comment inside the selector list — skip it as plain text
                end2 = text.find("*/", j + 2)
                j = (end2 + 2) if end2 != -1 else n
                continue
            j += 1
        if j >= n or text[j] != "{":
            i = n
            continue
        selector_text = text[i:j].strip()
        depth = 1
        k = j + 1
        while k < n and depth > 0:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        body = text[j + 1:k - 1]
        if selector_text:
            blocks.append({"type": "rule", "prelude": selector_text,
                            "body": body, "comment": last_comment, "line": line_no})
        i = k
        last_comment = None

    return blocks


def _parse_declarations(body: str) -> list:
    decls = []
    for chunk in _split_top_level(body, ";"):
        if ":" not in chunk:
            continue
        prop, _, value = chunk.partition(":")
        decls.append((prop.strip(), value.strip()))
    return decls


def analyze_css(rel_path: str, raw: str) -> CssInfo:
    info = CssInfo(
        rel_path=rel_path,
        loc=count_loc(raw),
        size=len(raw.encode("utf-8", errors="ignore")),
        is_minified=is_probably_minified(raw),
        raw=raw,
    )

    blocks = _parse_css_blocks(raw)
    for b in blocks:
        if b["type"] == "rule":
            selectors = _split_top_level(b["prelude"], ",")
            decls = _parse_declarations(b["body"])
            for prop, value in decls:
                if prop.startswith("--"):
                    info.custom_props_defined[prop] = value
                for m in _VAR_USAGE_RE.finditer(value):
                    info.custom_props_used.add(m.group(1))
                for m in _COLOR_RE.finditer(value):
                    info.colors.append(m.group(0))
            info.rules.append(CssRuleInfo(
                selectors=selectors, declarations=decls,
                comment=b["comment"], line=b["line"],
            ))
        elif b["type"] == "at-simple":
            prelude = b["prelude"]
            kind = "import" if prelude.startswith("@import") else \
                   "charset" if prelude.startswith("@charset") else "other"
            if kind == "import":
                m = re.search(r"""@import\s+(?:url\(\s*)?["']?([^"')]+)["']?\)?""", prelude)
                if m:
                    target = resolve_relative(rel_path, m.group(1))
                    if target:
                        info.imports.append(target)
            info.at_rules.append(CssAtRuleInfo(
                kind=kind, prelude=prelude, comment=b["comment"], line=b["line"],
            ))
        elif b["type"] == "at-block":
            prelude = b["prelude"]
            if prelude.startswith("@media"):
                kind = "media"
                for m in _BREAKPOINT_RE.finditer(prelude):
                    info.breakpoints.add(f"{m.group(1)}: {m.group(2)}")
            elif prelude.startswith("@keyframes") or prelude.startswith("@-webkit-keyframes"):
                kind = "keyframes"
            elif prelude.startswith("@font-face"):
                kind = "font-face"
            elif prelude.startswith("@supports"):
                kind = "supports"
            else:
                kind = "other"

            nested = []
            if kind in ("media", "supports"):
                for nb in _parse_css_blocks(b["body"]):
                    if nb["type"] != "rule":
                        continue
                    selectors = _split_top_level(nb["prelude"], ",")
                    decls = _parse_declarations(nb["body"])
                    for prop, value in decls:
                        for m in _VAR_USAGE_RE.finditer(value):
                            info.custom_props_used.add(m.group(1))
                        for m in _COLOR_RE.finditer(value):
                            info.colors.append(m.group(0))
                    nested.append(CssRuleInfo(
                        selectors=selectors, declarations=decls,
                        comment=nb["comment"], line=nb["line"],
                    ))
            else:
                decls = _parse_declarations(b["body"] or "")
                for prop, value in decls:
                    for m in _COLOR_RE.finditer(value):
                        info.colors.append(m.group(0))

            info.at_rules.append(CssAtRuleInfo(
                kind=kind, prelude=prelude, comment=b["comment"], line=b["line"],
                nested_rules=nested,
            ))

    return info


# --------------------------------------------------------------------------
# JavaScript parsing: heuristic (regex + string/comment masking), not a
# full AST parser.
#
# Fully parsing JS syntax in pure Python (without Node.js/Acorn/Esprima) is
# a project of its own. For documentation purposes, a 100%-accurate AST
# matters less than reliably extracting a file's "storefront": what it
# imports/exports, which functions/classes it declares, which DOM elements
# it touches, and what JSDoc says about its functions. So this masks out
# comments (so regexes don't mistake commented-out code for real code) and
# then runs a set of targeted regexes over the masked text, pulling the
# actual snippet from the original text. The limitations of this approach
# are documented in README.md.
# --------------------------------------------------------------------------

def _mask_js(text: str) -> str:
    """
    Returns a string of the same length as text, in which:
      - comment bodies (// and /* */) are replaced with spaces;
      - template-literal (`...`) bodies are replaced with spaces — these
        often hold interpolated HTML markup, which otherwise produces false
        positives when scanning for code structure (e.g. tag-like or
        function-declaration-like fragments inside the string);
      - regular '...' and "..." strings are NOT masked: they're exactly
        where import paths, CSS selectors, and event names live, and that's
        the content the parser actually needs to read.
    Newlines are always preserved so line numbers stay accurate.

    Limitation: telling a regex literal /.../ apart from a division operator
    is not possible without a full tokenizer; a simplified rule is used here
    (see README.md, "Known limitations").
    """
    out = list(text)
    n = len(text)
    i = 0

    def blank(a, b):
        for idx in range(a, b):
            if out[idx] != "\n":
                out[idx] = " "

    while i < n:
        ch = text[i]
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            j = n if j == -1 else j + 2
            blank(i, j)
            i = j
            continue
        if ch == "`":
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == "`":
                    j += 1
                    break
                j += 1
            blank(i, j)
            i = j
            continue
        if ch in "'\"":
            # strings are NOT masked, just skipped over whole, so that
            # special characters/brackets inside them don't confuse later scanning
            quote = ch
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == quote:
                    j += 1
                    break
                j += 1
            i = j
            continue
        i += 1
    return "".join(out)


_IMPORT_STATIC_RE = re.compile(
    r"import\s+(?P<clause>[^;\n]*?)\s+from\s+['\"](?P<src>[^'\"]+)['\"]"
)
_IMPORT_BARE_RE = re.compile(r"import\s+['\"](?P<src>[^'\"]+)['\"]")
_IMPORT_DYNAMIC_RE = re.compile(r"import\(\s*['\"](?P<src>[^'\"]+)['\"]\s*\)")
_REQUIRE_RE = re.compile(r"require\(\s*['\"](?P<src>[^'\"]+)['\"]\s*\)")

_EXPORT_DEFAULT_RE = re.compile(r"export\s+default\b")
_EXPORT_NAMED_DECL_RE = re.compile(
    r"export\s+(?:const|let|var|function\*?|class)\s+(?P<name>[A-Za-z_$][\w$]*)"
)
_EXPORT_LIST_RE = re.compile(r"export\s*\{([^}]+)\}")

_FUNCTION_DECL_RE = re.compile(
    r"(?<![\w$.])function\s*\*?\s*(?P<name>[A-Za-z_$][\w$]*)\s*\((?P<params>[^)]*)\)"
)
_ARROW_CONST_RE = re.compile(
    r"(?<![\w$.])(?:export\s+)?(?:const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*=\s*"
    r"(?:async\s*)?\((?P<params>[^)]*)\)\s*=>"
)
_ARROW_CONST_1ARG_RE = re.compile(
    r"(?<![\w$.])(?:export\s+)?(?:const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*=\s*"
    r"(?:async\s*)?(?P<params>[A-Za-z_$][\w$]*)\s*=>"
)
_CLASS_RE = re.compile(
    r"(?<![\w$.])class\s+(?P<name>[A-Za-z_$][\w$]*)(?:\s+extends\s+(?P<extends>[A-Za-z_$][\w$.]*))?\s*\{"
)
_METHOD_RE = re.compile(
    r"(?<![\w$.])(?:static\s+)?(?:async\s+)?(?:\*\s*)?(?:get\s+|set\s+)?"
    r"(?P<name>[A-Za-z_$][\w$]*)\s*\((?P<params>[^)]*)\)\s*\{"
)

_DOM_QUERY_RE = re.compile(
    r"(?:document|[\w$]+)\.(?P<method>querySelector(?:All)?|getElementById|"
    r"getElementsByClassName|getElementsByTagName|closest)\(\s*(?P<q>['\"`])(?P<sel>.*?)(?P=q)\s*\)"
)
_EVENT_LISTENER_RE = re.compile(
    r"(?P<target>[\w$.]+)\.addEventListener\(\s*(?P<q>['\"`])(?P<evt>\w+)(?P=q)"
)
# docgen-004: classList.add/remove/toggle(...) and className = "..." are
# *writes* of a class onto an element, not queries -- but they're just as
# valid evidence that a class is "used" as a querySelector read is. Without
# this, any project that builds its DOM by creating elements and assigning
# classes to them (instead of querying for pre-existing ones) reads as if
# none of its classes were ever touched by JS at all.
_CLASSLIST_WRITE_RE = re.compile(
    r"\.classList\.(?:add|remove|toggle)\(\s*(?P<args>[^)]*)\)"
)
_CLASSLIST_ARG_RE = re.compile(r"""['"`]([^'"`]+)['"`]""")
_CLASSNAME_ASSIGN_RE = re.compile(
    r"\.className\s*=\s*(?P<q>['\"`])(?P<val>[^'\"`]*)(?P=q)"
)
_FETCH_RE = re.compile(r"(?<![\w$.])fetch\s*\(")
_XHR_RE = re.compile(r"new\s+XMLHttpRequest\s*\(")
_AXIOS_RE = re.compile(r"(?<![\w$.])axios\.(get|post|put|delete|patch)\s*\(")

_JSDOC_RE = re.compile(r"/\*\*(?P<body>.*?)\*/\s*\n?", re.DOTALL)
_JSDOC_PARAM_RE = re.compile(
    r"@param\s+(?:\{[^}]*\}\s*)?(?P<name>[\w.$\[\]]+)\s*-?\s*(?P<desc>.*)"
)
_JSDOC_RETURNS_RE = re.compile(r"@returns?\s+(?:\{[^}]*\}\s*)?(?P<desc>.*)")
_JSDOC_EXAMPLE_RE = re.compile(r"@example\s*\n?(?P<code>(?:.*\n?)*)")
_TODO_RE = re.compile(r"(TODO|FIXME|HACK|XXX)\s*:?\s*(.*)")


def _parse_jsdoc(comment_body: str) -> dict:
    """Parses the body of a JSDoc comment (between /** and */) into a structure."""
    lines = [re.sub(r"^\s*\*\s?", "", ln) for ln in comment_body.splitlines()]
    description_lines = []
    params = {}
    returns = None
    examples = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("@param"):
            m = _JSDOC_PARAM_RE.match(stripped)
            if m:
                params[m.group("name")] = m.group("desc").strip()
        elif stripped.startswith("@return"):
            m = _JSDOC_RETURNS_RE.match(stripped)
            if m:
                returns = m.group("desc").strip()
        elif stripped.startswith("@example"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("@"):
                code_lines.append(lines[i])
                i += 1
            examples.append("\n".join(code_lines).strip())
            continue
        elif stripped.startswith("@"):
            pass  # other tags (@deprecated, @throws...) aren't critical for an overview
        elif stripped:
            description_lines.append(stripped)
        i += 1
    return {
        "description": " ".join(description_lines).strip(),
        "params": params,
        "returns": returns,
        "examples": examples,
    }


def _collect_jsdoc_map(raw: str) -> dict:
    """Builds a mapping of 'comment end position' -> parsed JSDoc, so the
    nearest preceding JSDoc for a function/class can be found afterwards."""
    result = []
    for m in _JSDOC_RE.finditer(raw):
        result.append((m.end(), _parse_jsdoc(m.group("body"))))
    return result


def _nearest_jsdoc(jsdoc_list: list, decl_start: int, raw: str) -> Optional[dict]:
    """Returns a JSDoc block if nothing but whitespace and export/default/async
    modifiers sit between its end and the start of the declaration — i.e. the
    comment really documents this particular declaration."""
    best = None
    for end_pos, parsed in jsdoc_list:
        if end_pos > decl_start:
            continue
        gap_tokens = raw[end_pos:decl_start].split()
        if all(tok in ("export", "default", "async") for tok in gap_tokens):
            best = parsed
    return best


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _extract_class_body(masked: str, raw: str, start_brace: int) -> tuple:
    """Given the position of an opening {, returns (class_body, index_after_closing_brace)."""
    depth = 1
    k = start_brace + 1
    n = len(masked)
    while k < n and depth > 0:
        if masked[k] == "{":
            depth += 1
        elif masked[k] == "}":
            depth -= 1
        k += 1
    return raw[start_brace + 1:k - 1], masked[start_brace + 1:k - 1], k


def analyze_js(rel_path: str, raw: str) -> JsInfo:
    info = JsInfo(
        rel_path=rel_path,
        loc=count_loc(raw),
        size=len(raw.encode("utf-8", errors="ignore")),
        is_minified=is_probably_minified(raw),
        raw=raw,
    )

    if info.is_minified:
        # A minified file wouldn't yield anything but noise from parsing.
        # Return basic stats only.
        return info

    masked = _mask_js(raw)
    jsdoc_list = _collect_jsdoc_map(raw)

    exported_names = set()
    if _EXPORT_DEFAULT_RE.search(masked):
        exported_names.add("default")
    for m in _EXPORT_NAMED_DECL_RE.finditer(masked):
        exported_names.add(m.group("name"))
        info.exports.append(m.group("name"))
    for m in _EXPORT_LIST_RE.finditer(masked):
        for part in m.group(1).split(","):
            name = part.strip().split(" as ")[0].strip()
            if name:
                exported_names.add(name)
                info.exports.append(name)

    for m in _IMPORT_STATIC_RE.finditer(masked):
        clause = m.group("clause")
        names = []
        default_name = None
        namespace = None
        ns_match = re.match(r"\*\s+as\s+([\w$]+)", clause)
        if ns_match:
            namespace = ns_match.group(1)
        else:
            brace_match = re.search(r"\{([^}]*)\}", clause)
            before_brace = clause.split("{")[0].strip().rstrip(",").strip()
            if before_brace:
                default_name = before_brace
            if brace_match:
                names = [p.strip().split(" as ")[0].strip()
                         for p in brace_match.group(1).split(",") if p.strip()]
        info.imports.append({
            "source": m.group("src"), "names": names,
            "default_name": default_name, "namespace": namespace,
        })
    for m in _IMPORT_BARE_RE.finditer(masked):
        info.imports.append({"source": m.group("src"), "names": [],
                              "default_name": None, "namespace": None})
    for m in _IMPORT_DYNAMIC_RE.finditer(masked):
        info.imports.append({"source": m.group("src"), "names": [],
                              "default_name": None, "namespace": None, "dynamic": True})
    for m in _REQUIRE_RE.finditer(masked):
        info.requires.append(m.group("src"))

    # top-level functions
    seen_spans = []
    for m in _FUNCTION_DECL_RE.finditer(masked):
        name = m.group("name")
        params = [p.strip() for p in m.group("params").split(",") if p.strip()]
        doc = _nearest_jsdoc(jsdoc_list, m.start(), raw)
        info.functions.append(JsFunctionInfo(
            name=name, params=params, kind="function",
            is_exported=name in exported_names, doc=doc, line=_line_of(raw, m.start()),
        ))
        seen_spans.append((m.start(), m.end()))

    for pattern in (_ARROW_CONST_RE, _ARROW_CONST_1ARG_RE):
        for m in pattern.finditer(masked):
            if any(a <= m.start() < b for a, b in seen_spans):
                continue
            name = m.group("name")
            params_raw = m.group("params")
            params = [p.strip() for p in params_raw.split(",") if p.strip()]
            doc = _nearest_jsdoc(jsdoc_list, m.start(), raw)
            info.functions.append(JsFunctionInfo(
                name=name, params=params, kind="arrow",
                is_exported=name in exported_names, doc=doc, line=_line_of(raw, m.start()),
            ))
            seen_spans.append((m.start(), m.end()))

    # classes
    for m in _CLASS_RE.finditer(masked):
        name = m.group("name")
        extends = m.group("extends")
        brace_pos = masked.find("{", m.end() - 1)
        if brace_pos == -1:
            continue
        body_raw, body_masked, _end = _extract_class_body(masked, raw, brace_pos)
        methods = []
        for mm in _METHOD_RE.finditer(body_masked):
            mname = mm.group("name")
            if mname in JS_CONTROL_KEYWORDS:
                continue
            mparams = [p.strip() for p in mm.group("params").split(",") if p.strip()]
            abs_pos = brace_pos + 1 + mm.start()
            mdoc = _nearest_jsdoc(jsdoc_list, abs_pos, raw)
            kind = "constructor" if mname == "constructor" else "method"
            methods.append(JsFunctionInfo(
                name=mname, params=mparams, kind=kind,
                is_exported=False, doc=mdoc, line=_line_of(raw, abs_pos),
            ))
        cdoc = _nearest_jsdoc(jsdoc_list, m.start(), raw)
        info.classes.append(JsClassInfo(
            name=name, extends=extends, methods=methods, doc=cdoc,
            line=_line_of(raw, m.start()),
        ))

    for m in _DOM_QUERY_RE.finditer(masked):
        info.dom_queries.append({
            "method": m.group("method"), "selector": m.group("sel"),
            "line": _line_of(raw, m.start()),
        })

    # docgen-004: classList writes and className assignments -- a class an
    # element receives via JS is "used" whether or not that element (or any
    # element bearing that class) exists anywhere in the static HTML; unlike
    # dom_queries above, these are NOT cross-checked against the HTML id/class
    # registry in build_edges() -- see the comment there for why.
    for m in _CLASSLIST_WRITE_RE.finditer(masked):
        line = _line_of(raw, m.start())
        for am in _CLASSLIST_ARG_RE.finditer(m.group("args")):
            info.class_writes.append({"class_name": am.group(1), "line": line})
    for m in _CLASSNAME_ASSIGN_RE.finditer(masked):
        line = _line_of(raw, m.start())
        for token in m.group("val").split():
            info.class_writes.append({"class_name": token, "line": line})

    for m in _EVENT_LISTENER_RE.finditer(masked):
        info.event_listeners.append({
            "target": m.group("target"), "event": m.group("evt"),
            "line": _line_of(raw, m.start()),
        })

    for regex, kind in ((_FETCH_RE, "fetch"), (_XHR_RE, "xhr"), (_AXIOS_RE, "axios")):
        for m in regex.finditer(masked):
            info.network_calls.append({"kind": kind, "line": _line_of(raw, m.start())})

    for m in re.finditer(r"//[^\n]*|/\*.*?\*/", raw, re.DOTALL):
        tm = _TODO_RE.search(m.group(0))
        if tm:
            info.todos.append({
                "marker": tm.group(1), "text": tm.group(2).strip(),
                "line": _line_of(raw, m.start()),
            })

    # the file's very first comment (if it sits right at the top) often
    # carries the module's overall purpose
    head = raw.lstrip()
    if head.startswith("/**") or head.startswith("/*"):
        end = head.find("*/")
        if end != -1:
            info.top_comment = re.sub(r"^\s*\*\s?", "", head[2:end], flags=re.MULTILINE).strip()
    elif head.startswith("//"):
        first_lines = []
        for ln in head.splitlines():
            if ln.strip().startswith("//"):
                first_lines.append(ln.strip()[2:].strip())
            else:
                break
        if first_lines:
            info.top_comment = " ".join(first_lines)

    return info


# --------------------------------------------------------------------------
# Building the relationships between files (the "dependency map")
#
# Two layers of relationships:
#   1. Structural — what's explicitly written in the code: <link>,
#      <script src>, @import, import/require.
#   2. Semantic (DOM) — what connects files through usage: JS reaching into
#      an element by #id/.class, a CSS selector targeting #id/.class. These
#      links aren't visible from "references" inside a single file alone,
#      but they're exactly what shows how HTML/CSS/JS actually work together.
# --------------------------------------------------------------------------

_SIMPLE_TOKEN_RE = re.compile(r"[.#]([A-Za-z_-][\w-]*)")
# docgen-002: [attr="value"] / [attr~="value"] / [attr^="value"] etc. Only
# the exact-match core is cross-referenced (~=, ^=, $=, *=, |= all narrow or
# widen an exact match in ways a simple registry lookup can't reproduce
# faithfully) -- captured here so callers can still see the attribute name
# and value even if the operator itself is ignored for matching purposes.
_ATTR_SELECTOR_RE = re.compile(
    r"\[\s*([a-zA-Z_:][\w:-]*)\s*[~^$*|]?=\s*[\"']([^\"']*)[\"']\s*\]"
)


def _selector_tokens(selector: str) -> list:
    """Extracts plain #id and .class tokens from a CSS/JS selector."""
    return _SIMPLE_TOKEN_RE.findall(selector)


def _selector_attr_pairs(selector: str) -> list:
    """Extracts (attr_name, attr_value) pairs from [attr=value]-style parts
    of a CSS/JS selector. docgen-002."""
    return _ATTR_SELECTOR_RE.findall(selector)


_STRUCTURAL_EDGE_KINDS = {"link", "script", "css-import", "js-import", "js-require",
                           "external", "page-link"}
_SEMANTIC_EDGE_KINDS = {"dom", "style"}


def build_edges(html_files: dict, css_files: dict, js_files: dict) -> tuple:
    """Returns (edges, used_tokens): used_tokens is the set of every
    #id/.class token that was found both in HTML and in a CSS selector or a
    JS DOM query (used to find "dead" hooks independent of edge de-duplication
    used for the on-screen graph)."""
    edges: list = []
    used_tokens: set = set()

    all_html_paths = set(html_files)
    all_css_paths = set(css_files)
    all_js_paths = set(js_files)

    # registry: where each id/class is defined (for semantic links)
    id_registry: dict = {}
    class_registry: dict = {}
    attr_registry: dict = {}  # (attr_name, attr_value) -> [html paths] -- docgen-002
    for path, hinfo in html_files.items():
        for i in hinfo.ids:
            id_registry.setdefault(i, []).append(path)
        for c in hinfo.classes:
            class_registry.setdefault(c, []).append(path)
        for pair in hinfo.attr_pairs:
            attr_registry.setdefault(pair, []).append(path)

    # 1. HTML -> CSS (<link rel=stylesheet>), HTML -> JS (<script src>),
    #    HTML -> HTML (<a href> to another project page)
    for path, hinfo in html_files.items():
        for href in hinfo.hrefs_internal:
            if href in all_html_paths and href != path:
                edges.append(Edge(path, href, "page-link"))
        for href in hinfo.stylesheets:
            target = resolve_relative(path, href)
            if target and target in all_css_paths:
                edges.append(Edge(path, target, "link"))
            elif target:
                edges.append(Edge(path, target, "unresolved", label=href))
            else:
                edges.append(Edge(path, href, "external", label="CSS"))
        for script in hinfo.scripts:
            target = resolve_relative(path, script["src"])
            if target and target in all_js_paths:
                edges.append(Edge(path, target, "script"))
            elif target:
                edges.append(Edge(path, target, "unresolved", label=script["src"]))
            else:
                edges.append(Edge(path, script["src"], "external", label="JS"))

    # 2. CSS -> CSS (@import)
    for path, cinfo in css_files.items():
        for target in cinfo.imports:
            if target in all_css_paths:
                edges.append(Edge(path, target, "css-import"))

    # 3. JS -> JS (import/require), JS -> external libraries
    for path, jinfo in js_files.items():
        for imp in jinfo.imports:
            target = resolve_relative(path, imp["source"])
            if target is None:
                edges.append(Edge(path, imp["source"], "external", label="import"))
                continue
            resolved = None
            for candidate in (target, f"{target}.js", f"{target}.mjs", f"{target}/index.js"):
                if candidate in all_js_paths:
                    resolved = candidate
                    break
            edges.append(Edge(path, resolved or target,
                               "js-import" if resolved else "unresolved"))
        for src in jinfo.requires:
            target = resolve_relative(path, src)
            if target is None:
                edges.append(Edge(path, src, "external", label="require"))
                continue
            resolved = None
            for candidate in (target, f"{target}.js", f"{target}/index.js"):
                if candidate in all_js_paths:
                    resolved = candidate
                    break
            edges.append(Edge(path, resolved or target,
                               "js-require" if resolved else "unresolved"))

    # 4. JS -> HTML (reaching into the DOM by #id/.class/[attr=value])
    for path, jinfo in js_files.items():
        for q in jinfo.dom_queries:
            method, sel = q["method"], q["selector"]
            targets = set()
            if method == "getElementById":
                targets.update(id_registry.get(sel, []))
                if sel in id_registry:
                    used_tokens.add(sel)
            else:
                for tok in _selector_tokens(sel) or ([sel] if method in
                        ("getElementsByClassName",) else []):
                    targets.update(id_registry.get(tok, []))
                    targets.update(class_registry.get(tok, []))
                    if tok in id_registry or tok in class_registry:
                        used_tokens.add(tok)
                # docgen-002: [data-ref="x"]-style hooks, invisible to
                # _selector_tokens above since it only looks for . and #.
                for pair in _selector_attr_pairs(sel):
                    targets.update(attr_registry.get(pair, []))
                    if pair in attr_registry:
                        used_tokens.add(f"[{pair[0]}={pair[1]}]")
            if targets:
                for t in targets:
                    edges.append(Edge(path, t, "dom", label=sel))
            else:
                edges.append(Edge(path, "?", "dom-unresolved", label=sel))

        # docgen-004: a classList.add/className write is proof the class is
        # used by JS regardless of whether the target element exists in the
        # static HTML -- it may be created by this same script. Unlike the
        # read-side loop above, this does NOT require a registry match before
        # counting as "used": requiring one would defeat the purpose, since
        # dynamically-created elements are by definition absent from the
        # static registry.
        for cw in jinfo.class_writes:
            used_tokens.add(cw["class_name"])

    # 5. CSS -> HTML (a selector targets an #id/.class declared in HTML)
    for path, cinfo in css_files.items():
        all_rules = list(cinfo.rules)
        for at in cinfo.at_rules:
            all_rules.extend(at.nested_rules)
        seen_targets = set()
        unmatched = []
        for rule in all_rules:
            for sel in rule.selectors:
                for tok in _selector_tokens(sel):
                    hit = False
                    for t in id_registry.get(tok, []) + class_registry.get(tok, []):
                        if (path, t) not in seen_targets:
                            edges.append(Edge(path, t, "style", label="." + tok))
                            seen_targets.add((path, t))
                        hit = True
                    if hit:
                        used_tokens.add(tok)
                    # docgen-001/004: a static-HTML miss is no longer enough
                    # to call a selector orphaned on its own -- used_tokens
                    # (already populated above from JS reads AND writes,
                    # including classes assigned to dynamically-created
                    # elements that never appear in the static registry) can
                    # still vouch for it. Only flag what NEITHER source
                    # accounts for. (used_tokens is a set built earlier in
                    # this same function -- see sections 4 and the
                    # class_writes loop directly above section 5.)
                    elif tok not in used_tokens:
                        unmatched.append(tok)
                # docgen-002: [data-ref="x"]-style selectors -- same
                # treatment as the .class/#id loop just above, using the
                # same `used_tokens` cross-check (and the same
                # "[attr=value]" label format section 4 writes to it with).
                for pair in _selector_attr_pairs(sel):
                    label = f"[{pair[0]}={pair[1]}]"
                    hit = False
                    for t in attr_registry.get(pair, []):
                        if (path, t) not in seen_targets:
                            edges.append(Edge(path, t, "style", label=label))
                            seen_targets.add((path, t))
                        hit = True
                    if hit:
                        used_tokens.add(label)
                    elif label not in used_tokens:
                        unmatched.append(label)
        cinfo.unmatched_selectors = sorted(set(unmatched))

    return edges, used_tokens


# --------------------------------------------------------------------------
# Aggregated project statistics (for the "Overview" section)
# --------------------------------------------------------------------------

def _normalize_color(c: str) -> str:
    return re.sub(r"\s+", " ", c.strip()).lower()


def analyze_project_stats(html_files: dict, css_files: dict, js_files: dict,
                           other_files: list, edges: list, used_tokens: set) -> dict:
    stats: dict = {}

    n_html, n_css, n_js = len(html_files), len(css_files), len(js_files)
    total_loc = (sum(f.loc for f in html_files.values())
                 + sum(f.loc for f in css_files.values())
                 + sum(f.loc for f in js_files.values()))
    total_size = (sum(f.size for f in html_files.values())
                  + sum(f.size for f in css_files.values())
                  + sum(f.size for f in js_files.values()))

    stats["counts"] = {"html": n_html, "css": n_css, "js": n_js,
                        "other": len(other_files),
                        "total": n_html + n_css + n_js + len(other_files)}
    stats["total_loc"] = total_loc
    stats["total_size"] = total_size

    all_files = (
        [(p, f.size, f.loc, "html") for p, f in html_files.items()]
        + [(p, f.size, f.loc, "css") for p, f in css_files.items()]
        + [(p, f.size, f.loc, "js") for p, f in js_files.items()]
    )
    stats["largest_files"] = sorted(all_files, key=lambda t: -t[1])[:5]

    # the project's color palette (by usage frequency)
    color_counter: dict = {}
    for cinfo in css_files.values():
        for c in cinfo.colors:
            key = _normalize_color(c)
            color_counter[key] = color_counter.get(key, 0) + 1
    stats["palette"] = sorted(color_counter.items(), key=lambda t: -t[1])[:24]

    # responsive breakpoints
    breakpoints = set()
    for cinfo in css_files.values():
        breakpoints |= cinfo.breakpoints
    stats["breakpoints"] = sorted(breakpoints)

    # external libraries (from script src and import/require that don't
    # resolve inside the project)
    external_libs = set()
    for hinfo in html_files.values():
        for s in hinfo.scripts:
            src = s["src"]
            if resolve_relative(hinfo.rel_path, src) is None:
                name = src.split("/")[-1].split("?")[0]
                external_libs.add(name)
    for jinfo in js_files.values():
        for imp in jinfo.imports:
            if resolve_relative(jinfo.rel_path, imp["source"]) is None:
                external_libs.add(imp["source"])
        for req in jinfo.requires:
            if resolve_relative(jinfo.rel_path, req) is None:
                external_libs.add(req)
    stats["external_libs"] = sorted(external_libs)

    # project-wide TODO/FIXME
    todos = []
    for jinfo in js_files.values():
        for t in jinfo.todos:
            todos.append({**t, "file": jinfo.rel_path})
    stats["todos"] = todos

    # unused id/class (declared in HTML but never matched by any CSS
    # selector or any JS DOM query)
    all_ids, all_classes = set(), set()
    for hinfo in html_files.values():
        all_ids |= hinfo.ids
        all_classes |= hinfo.classes
    stats["unused_ids"] = sorted(all_ids - used_tokens)
    stats["unused_classes"] = sorted(all_classes - used_tokens)

    # orphan CSS selectors (collected at the build_edges stage, just rolled up here)
    orphan_selectors = []
    for path, cinfo in css_files.items():
        for sel in cinfo.unmatched_selectors:
            orphan_selectors.append({"file": path, "token": sel})
    stats["orphan_css_selectors"] = orphan_selectors

    # docgen-003: dom_queries the cross-referencer couldn't match to anything
    # (kind="dom-unresolved") used to vanish with no trace once the SVG
    # renderer's kind filter dropped them -- surface a count instead.
    stats["dom_queries_total"] = sum(len(jinfo.dom_queries) for jinfo in js_files.values())
    stats["dom_unresolved"] = [
        {"file": e.src, "selector": e.label} for e in edges if e.kind == "dom-unresolved"
    ]

    # unresolved links (broken paths)
    stats["unresolved_links"] = [
        {"src": e.src, "dst": e.dst, "label": e.label}
        for e in edges if e.kind == "unresolved"
    ]

    # accessibility: images without alt, forms without labels — a light heuristic
    images_no_alt = []
    for hinfo in html_files.values():
        for img in hinfo.images:
            if not img.get("alt"):
                images_no_alt.append({"file": hinfo.rel_path, "src": img.get("src", "")})
    stats["images_no_alt"] = images_no_alt

    return stats


# --------------------------------------------------------------------------
# Syntax highlighting (runs in Python at generation time; the result is
# already-final HTML with <span class="tok-...">, so reading the docs later
# needs no JS and no CDN such as highlight.js/Prism).
# --------------------------------------------------------------------------

def _tokenize_generic(text: str, patterns: list) -> str:
    """
    patterns: a list of (regex, css_class) in priority order.
    Builds one combined regex with named groups and wraps matches in
    <span class="tok-...">, escaping everything else through html.escape.
    """
    combined = re.compile(
        "|".join(f"(?P<g{i}>{p.pattern})" for i, (p, _) in enumerate(patterns)),
        re.DOTALL,
    )
    classes = [cls for _, cls in patterns]
    out = []
    pos = 0
    for m in combined.finditer(text):
        if m.start() > pos:
            out.append(esc(text[pos:m.start()]))
        idx = int(m.lastgroup[1:])
        out.append(f'<span class="tok-{classes[idx]}">{esc(m.group())}</span>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def highlight_html(src: str) -> str:
    patterns = [
        (re.compile(r"<!--.*?-->", re.DOTALL), "com"),
        (re.compile(r"<!DOCTYPE[^>]*>", re.IGNORECASE), "doctype"),
        (re.compile(r'"[^"]*"|\'[^\']*\''), "str"),
        (re.compile(r"</?[a-zA-Z][\w:-]*"), "tag"),
        (re.compile(r"[a-zA-Z-:]+(?==)"), "attr"),
        (re.compile(r"/?>"), "tag"),
    ]
    return _tokenize_generic(src, patterns)


def highlight_css(src: str) -> str:
    patterns = [
        (re.compile(r"/\*.*?\*/", re.DOTALL), "com"),
        (re.compile(r'"[^"]*"|\'[^\']*\''), "str"),
        (re.compile(r"@[\w-]+"), "kw"),
        (re.compile(r"--[\w-]+"), "var"),
        (re.compile(r"#[0-9a-fA-F]{3,8}\b"), "num"),
        (re.compile(r"[.#][\w-]+"), "sel"),
        (re.compile(r"\b\d+(\.\d+)?(px|em|rem|%|vh|vw|s|ms|deg)?\b"), "num"),
        (re.compile(r"[\w-]+(?=\s*:)"), "prop"),
    ]
    return _tokenize_generic(src, patterns)


def highlight_js(src: str) -> str:
    kw_pattern = r"\b(?:" + "|".join(sorted(JS_KEYWORDS, key=len, reverse=True)) + r")\b"
    patterns = [
        (re.compile(r"/\*\*?.*?\*/", re.DOTALL), "com"),
        (re.compile(r"//[^\n]*"), "com"),
        (re.compile(r"`(?:\\.|[^`\\])*`"), "str"),
        (re.compile(r'"(?:\\.|[^"\\])*"'), "str"),
        (re.compile(r"'(?:\\.|[^'\\])*'"), "str"),
        (re.compile(kw_pattern), "kw"),
        (re.compile(r"\b\d+(\.\d+)?\b"), "num"),
        (re.compile(r"[\w$]+(?=\()"), "fn"),
    ]
    return _tokenize_generic(src, patterns)


def highlight_by_kind(src: str, kind: str) -> str:
    if kind == "html":
        return highlight_html(src)
    if kind == "css":
        return highlight_css(src)
    if kind == "js":
        return highlight_js(src)
    return esc(src)


# --------------------------------------------------------------------------
# SVG dependency map ("atlas" of the project): HTML/CSS/JS files as nodes
# in three columns, links between them drawn as routes between "stations".
# Rendered in Python, no JS graphing library involved.
# --------------------------------------------------------------------------

_GRAPH_NODE_W = 240
_GRAPH_NODE_H = 40
_GRAPH_ROW_GAP = 14
_GRAPH_TOP = 64
_GRAPH_COL_X = {"html": 30, "css": 380, "js": 730}
_GRAPH_COL_TITLE = {"html": "HTML", "css": "CSS", "js": "JS"}


def _truncate_label(name: str, max_chars: int = 26) -> str:
    if len(name) <= max_chars:
        return name
    keep = max_chars - 1
    return "…" + name[-keep:]


def render_dependency_graph_svg(html_files: dict, css_files: dict, js_files: dict,
                                 edges: list) -> str:
    by_kind = {"html": sorted(html_files), "css": sorted(css_files), "js": sorted(js_files)}
    positions: dict = {}
    for kind, paths in by_kind.items():
        x = _GRAPH_COL_X[kind]
        for i, path in enumerate(paths):
            y = _GRAPH_TOP + i * (_GRAPH_NODE_H + _GRAPH_ROW_GAP)
            positions[path] = (x, y, kind)

    max_rows = max((len(v) for v in by_kind.values()), default=0)
    height = _GRAPH_TOP + max(max_rows, 1) * (_GRAPH_NODE_H + _GRAPH_ROW_GAP) + 30
    width = _GRAPH_COL_X["js"] + _GRAPH_NODE_W + 40

    def anchor(path):
        x, y, _ = positions[path]
        return x, y

    def edge_path_d(x1, y1, x2, y2):
        if x2 >= x1:
            sx, sy = x1 + _GRAPH_NODE_W, y1 + _GRAPH_NODE_H / 2
            tx, ty = x2, y2 + _GRAPH_NODE_H / 2
        else:
            sx, sy = x1, y1 + _GRAPH_NODE_H / 2
            tx, ty = x2 + _GRAPH_NODE_W, y2 + _GRAPH_NODE_H / 2
        dx = (tx - sx) * 0.5
        return f"M {sx:.1f},{sy:.1f} C {sx + dx:.1f},{sy:.1f} {tx - dx:.1f},{ty:.1f} {tx:.1f},{ty:.1f}"

    structural_kinds = {"link", "script", "css-import", "js-import", "js-require", "page-link"}
    semantic_kinds = {"dom", "style"}

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" class="dep-graph" role="img" '
        f'aria-label="Project dependency map">'
    )
    parts.append("""
    <style>
      .dep-graph text { font-family: var(--font-body); }
      .dep-node rect { stroke-width: 1.4; }
      .dep-node.k-html rect { fill: var(--map-html-bg); stroke: var(--map-html); }
      .dep-node.k-css rect  { fill: var(--map-css-bg);  stroke: var(--map-css); }
      .dep-node.k-js rect   { fill: var(--map-js-bg);   stroke: var(--map-js); }
      .dep-node .dot { }
      .dep-node.k-html .dot { fill: var(--map-html); }
      .dep-node.k-css .dot  { fill: var(--map-css); }
      .dep-node.k-js .dot   { fill: var(--map-js); }
      .dep-node text.fname { font-size: 12px; fill: var(--ink-soft); }
      .edge-structural { stroke: var(--ink-soft); opacity: .38; fill: none; stroke-width: 1.4; }
      .edge-semantic { stroke: var(--map-accent-warm); opacity: .65; fill: none;
                        stroke-width: 1.3; stroke-dasharray: 3 3; }
      .col-title { font-family: var(--font-display); font-size: 13px;
                    letter-spacing: .08em; fill: var(--ink-soft); }
    </style>
    """)

    for kind, x in _GRAPH_COL_X.items():
        parts.append(
            f'<text class="col-title" x="{x}" y="28">{esc(_GRAPH_COL_TITLE[kind].upper())} '
            f'· {len(by_kind[kind])}</text>'
        )

    for e in edges:
        if e.src not in positions or e.dst not in positions:
            continue
        if e.src == e.dst:
            continue
        x1, y1 = anchor(e.src)
        x2, y2 = anchor(e.dst)
        d = edge_path_d(x1, y1, x2, y2)
        css_cls = "edge-semantic" if e.kind in semantic_kinds else "edge-structural"
        if e.kind not in structural_kinds and e.kind not in semantic_kinds:
            continue
        title = esc(f"{e.src} → {e.dst}" + (f" ({e.label})" if e.label else ""))
        parts.append(f'<path class="{css_cls}" d="{d}"><title>{title}</title></path>')

    for path, (x, y, kind) in positions.items():
        label = _truncate_label(path)
        parts.append(
            f'<g class="dep-node k-{kind}" transform="translate({x},{y})">'
            f'<rect width="{_GRAPH_NODE_W}" height="{_GRAPH_NODE_H}" rx="8"></rect>'
            f'<circle class="dot" cx="14" cy="{_GRAPH_NODE_H/2:.0f}" r="4"></circle>'
            f'<text class="fname" x="26" y="{_GRAPH_NODE_H/2 + 4:.0f}">{esc(label)}</text>'
            f'<title>{esc(path)}</title>'
            f'</g>'
        )

    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------
# The final document's embedded CSS and JS (the "Project Atlas").
# Visual language: a map/blueprint of the codebase — a deep ink header,
# cool "drafting paper" as the reading surface, bronze and verdigris
# (oxidized copper/brass) as the two accents instead of the usual
# "cream + terracotta" or "black + neon" pairing.
# Fully offline: no CDN fonts, no external JS libraries — system font
# stacks and inlined code only.
# --------------------------------------------------------------------------

DOC_CSS = """
:root {
  --ink: #16273f;
  --ink-soft: #3c4f66;
  --paper: #e9edf0;
  --paper-deep: #dbe2e7;
  --paper-line: #c7d1d8;
  --accent: #2f6f62;
  --accent-warm: #b5762f;
  --map-accent-warm: #b5762f;
  --map-html: #b5652d;
  --map-html-bg: #f1e2d4;
  --map-css: #2f6f62;
  --map-css-bg: #dde8e5;
  --map-js: #a9781f;
  --map-js-bg: #f1e7d1;
  --danger: #9c3b3b;
  --font-display: "Iowan Old Style", "Palatino Linotype", Palatino, "URW Palladio L", Georgia, serif;
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-mono: "SF Mono", SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
  --sidebar-w: 308px;
  --topbar-h: 64px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--font-body);
  color: var(--ink);
  background: var(--paper);
  font-size: 15px;
  line-height: 1.55;
}

::selection { background: var(--map-js-bg); color: var(--ink); }

a { color: var(--accent); }
a:hover { color: var(--accent-warm); }

:focus-visible {
  outline: 2px solid var(--accent-warm);
  outline-offset: 2px;
}

/* ---------- Top bar ---------- */
.topbar {
  position: sticky; top: 0; z-index: 40;
  height: var(--topbar-h);
  background: var(--ink);
  color: #eef2f4;
  display: flex; align-items: center; gap: 16px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255,255,255,.08);
}
/* docgen-r1: hidden by default (desktop has a static sidebar, no toggle
   needed); shown only inside the mobile media query below. Base rule lives
   in the stylesheet -- not an inline style -- specifically so that media
   query can override it without needing !important. */
.hamburger-btn {
  display: none; background: none; border: none; color: #fff;
  font-size: 18px; cursor: pointer; padding: 4px 6px; flex: none;
}
.topbar .brand {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--font-display);
  font-size: 19px;
  white-space: nowrap;
}
.topbar .brand .compass { flex: none; }
.topbar .meta {
  font-size: 12.5px; color: #b9c6d1; white-space: nowrap;
}
/* docgen-h1: the two manuals are two parallel #code-manual/#user-manual
   layouts, always both present in the DOM; radio+:checked (same pattern
   already used for the Code/Structure tabs) shows one and hides the
   other, no JS needed. Radios must be earlier siblings of both layout
   divs in the HTML for the ~ selectors below to reach them. */
.manual-radio { position: absolute; opacity: 0; pointer-events: none; }
.manual-tabs { display: flex; gap: 2px; }
.manual-tab-label {
  cursor: pointer; font-size: 12.5px; padding: 6px 12px; border-radius: 999px;
  color: #b9c6d1; white-space: nowrap;
}
.manual-tab-label:hover { background: rgba(255,255,255,.08); }
#switch-code-manual:checked ~ .topbar label[for="switch-code-manual"],
#switch-user-manual:checked ~ .topbar label[for="switch-user-manual"] {
  background: rgba(255,255,255,.14); color: #fff; font-weight: 600;
}
#user-manual { display: none; }
#switch-user-manual:checked ~ #user-manual { display: flex; }
#switch-user-manual:checked ~ #code-manual { display: none; }
/* docgen-h8: plan.json can show just one manual -- no tab switcher then, and
   the remaining layout is visible without needing a radio to be checked. */
body[data-manuals="code"] .manual-tabs, body[data-manuals="code"] #user-manual { display: none; }
body[data-manuals="user"] .manual-tabs, body[data-manuals="user"] #code-manual { display: none; }
body[data-manuals="user"] #user-manual { display: flex; }
/* the file search only filters the Code Manual's tree: hide it where it can't do anything
   (visibility, not display, while both manuals exist, so the topbar doesn't jump on switch) */
#switch-user-manual:checked ~ .topbar #doc-search { visibility: hidden; }
body[data-manuals="user"] #doc-search { display: none; }
.topbar .spacer { flex: 1; }
.topbar .stat-chip {
  font-size: 12px; color: #cfd9e0; border: 1px solid rgba(255,255,255,.18);
  border-radius: 999px; padding: 3px 10px; white-space: nowrap;
}
#doc-search {
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.2);
  color: #fff; border-radius: 8px; padding: 7px 12px;
  font-family: var(--font-body); font-size: 13px; width: 200px;
}
#doc-search::placeholder { color: #93a4b2; }
#doc-search:focus { background: rgba(255,255,255,.14); }

/* ---------- Layout ---------- */
.layout { display: flex; align-items: flex-start; }

.sidebar {
  width: var(--sidebar-w); flex: none;
  position: sticky; top: var(--topbar-h);
  height: calc(100vh - var(--topbar-h));
  overflow-y: auto;
  background: var(--paper-deep);
  border-right: 1px solid var(--paper-line);
  padding: 18px 14px 40px;
}
.sidebar-backdrop { display: none; }  /* shown only in the mobile media query */
.sidebar .quicknav { list-style: none; margin: 0 0 16px; padding: 0; }
.sidebar .quicknav a {
  display: block; padding: 6px 8px; border-radius: 6px;
  text-decoration: none; color: var(--ink-soft); font-size: 13.5px;
}
.sidebar .quicknav a:hover { background: rgba(0,0,0,.05); color: var(--ink); }

.tree-eyebrow {
  font-size: 11px; letter-spacing: .09em; color: var(--ink-soft);
  text-transform: uppercase; margin: 4px 0 8px 8px; opacity: .75;
}
.tree-eyebrow-row {
  display: flex; align-items: center; justify-content: space-between; gap: 8px;
}
.tree-eyebrow-row .tree-eyebrow { margin: 4px 0 8px; }
.tree-toggle-all {
  font-size: 11px; color: var(--accent); background: none; border: none;
  cursor: pointer; padding: 2px 6px; margin: 0 0 6px; white-space: nowrap;
}
.tree-toggle-all:hover { text-decoration: underline; }

.tree, .tree ul { list-style: none; margin: 0; padding-left: 16px; }
.tree { padding-left: 0; }
.tree li { position: relative; }
.tree details > summary {
  cursor: pointer; list-style: none; padding: 4px 8px; border-radius: 6px;
  font-size: 13.5px; color: var(--ink); display: flex; align-items: center; gap: 6px;
}
.tree details > summary::-webkit-details-marker { display: none; }
.tree details > summary:hover { background: rgba(0,0,0,.05); }
.tree details > summary::before {
  content: "▸"; display: inline-block; font-size: 10px; color: var(--ink-soft);
  transition: transform .12s ease;
}
.tree details[open] > summary::before { transform: rotate(90deg); }
.tree .file-link {
  display: flex; align-items: center; gap: 7px;
  padding: 4px 8px 4px 22px; border-radius: 6px;
  text-decoration: none; color: var(--ink-soft); font-size: 13.2px;
}
.tree .file-link:hover { background: rgba(0,0,0,.06); color: var(--ink); }
.tree .file-link.active { background: var(--map-js-bg); color: var(--ink); font-weight: 600; }
.tree .dot { width: 7px; height: 7px; border-radius: 50%; flex: none; }
.tree .dot.k-html { background: var(--map-html); }
.tree .dot.k-css  { background: var(--map-css); }
.tree .dot.k-js   { background: var(--map-js); }
.tree .dot.k-source { background: var(--accent); opacity: .8; }  /* docgen-006: php/jsx/vue/ts/scss etc. */
.tree .dot.k-other{ background: var(--ink-soft); opacity: .5; }
.tree[data-filtering="true"] li[data-match="false"] { display: none; }

/* ---------- Main content ---------- */
.content { flex: 1; min-width: 0; padding: 32px 40px 120px; max-width: 980px; }

h1.doc-title, h2.section-h, h3.file-h {
  font-family: var(--font-display); font-weight: 600; color: var(--ink);
}
h2.section-h {
  font-size: 26px; margin: 64px 0 18px; padding-top: 18px;
  border-top: 1px solid var(--paper-line);
}
.content > h2.section-h:first-child,
.content > section:first-child h2.section-h { margin-top: 0; padding-top: 0; border-top: none; }
.eyebrow {
  font-size: 11.5px; letter-spacing: .1em; text-transform: uppercase;
  color: var(--ink-soft); opacity: .8; margin: 0 0 4px;
}

.lede { font-size: 16px; color: var(--ink-soft); max-width: 62ch; }

.card-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px; margin: 18px 0 28px;
}
.stat-card {
  background: #fff; border: 1px solid var(--paper-line); border-radius: 10px;
  padding: 14px 16px;
}
.stat-card .n { font-family: var(--font-display); font-size: 26px; color: var(--ink); }
.stat-card .l { font-size: 12px; color: var(--ink-soft); }

.legend-row { display: flex; flex-wrap: wrap; gap: 10px; margin: 10px 0 26px; }
.legend-chip {
  display: inline-flex; align-items: center; gap: 7px;
  font-size: 12.5px; padding: 5px 11px; border-radius: 999px;
  border: 1px solid var(--paper-line); background: #fff;
}
.legend-chip .dot { width: 8px; height: 8px; border-radius: 50%; }

.swatch-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 26px; }
.swatch {
  width: 40px; height: 40px; border-radius: 8px; border: 1px solid rgba(0,0,0,.12);
}

.note-block {
  border: 1px solid var(--paper-line); border-left: 4px solid var(--accent-warm);
  background: #fff; border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 14px 0;
}
.note-block h4 {
  margin: 0 0 8px; font-size: 13px; letter-spacing: .04em;
  font-family: var(--font-display); color: var(--ink);
}
.note-block ul { margin: 0; padding-left: 20px; font-size: 13.5px; color: var(--ink-soft); }
.note-block.empty { border-left-color: var(--accent); color: var(--ink-soft); }
/* docgen-h7: Note (default look) vs Warning */
.note-block .callout-kind {
  font-family: var(--font-mono); font-size: 10.5px; letter-spacing: .08em;
  text-transform: uppercase; color: var(--ink-soft); margin-right: 6px; font-weight: 600;
}
.note-block.warning { border-left-color: var(--danger); background: #fbf3f3; }
.note-block.warning .callout-kind { color: var(--danger); }
.note-block code { font-family: var(--font-mono); font-size: 12.5px; }

.dep-graph-wrap {
  background: #fff; border: 1px solid var(--paper-line); border-radius: 12px;
  padding: 12px; overflow-x: auto; margin: 12px 0 20px;
}
.dep-graph { display: block; min-width: 720px; }
.graph-legend { display: flex; gap: 18px; flex-wrap: wrap; font-size: 12px; color: var(--ink-soft); margin-bottom: 18px; }
.graph-legend .ln { display: inline-flex; align-items: center; gap: 6px; }
.graph-legend .ln svg { flex: none; }

/* ---------- File card ---------- */
.file-card {
  background: #fff; border: 1px solid var(--paper-line); border-radius: 14px;
  padding: 22px 24px 26px; margin: 0 0 26px; scroll-margin-top: calc(var(--topbar-h) + 12px);
}
.file-card .file-path {
  font-family: var(--font-mono); font-size: 13px; color: var(--ink-soft);
}
.file-card h3.file-h { font-size: 19px; margin: 2px 0 4px; word-break: break-word; }
.file-badges { display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0 14px; }
.badge {
  font-size: 11px; padding: 3px 9px; border-radius: 999px; font-family: var(--font-mono);
  border: 1px solid var(--paper-line); color: var(--ink-soft);
}
.badge.k-html { border-color: var(--map-html); color: var(--map-html); }
.badge.k-css  { border-color: var(--map-css);  color: var(--map-css); }
.badge.k-js   { border-color: var(--map-js);   color: var(--map-js); }
.badge.warn   { border-color: var(--danger); color: var(--danger); }
/* docgen-h3: User Manual confidence tiers -- deliberately distinct from
   the k-html/k-css/k-js badges above (those say "what kind of file";
   these say "how much of this can you trust"), so no color is reused. */
.badge.confidence-auto     { border-color: var(--accent); color: var(--accent); }
.badge.confidence-inferred { border-color: var(--accent-warm); color: var(--accent-warm); }
.badge.confidence-scaffold { border-color: var(--ink-soft); color: var(--ink-soft); border-style: dashed; }
.badge.confidence-manual   { border-color: #5b7fa6; color: #5b7fa6; }
.section-h .badge { margin-left: 10px; vertical-align: middle; font-weight: 400; }
/* docgen-h4: User Manual building blocks */
.readme-embed {
  background: #fff; border: 1px solid var(--paper-line); border-radius: 12px;
  padding: 6px 22px 14px; max-width: 80ch;
}
.readme-embed h3, .readme-embed h4, .readme-embed h5, .readme-embed h6 {
  font-family: var(--font-display); color: var(--ink);
}
.manual-note { margin-top: 20px; }
.readme-embed pre.md-code {
  background: #101d30; color: #d8e2ea; font-family: var(--font-mono); font-size: 12.6px;
  line-height: 1.55; padding: 12px 14px; border-radius: 8px; overflow-x: auto; margin: 10px 0;
}
/* docgen-h6: segmented bar, one segment per User Manual section, colored by tier */
.coverage { margin: 0 0 8px; }
.coverage-bar { display: flex; gap: 4px; margin-bottom: 10px; max-width: 480px; }
.cov-seg { flex: 1; height: 8px; border-radius: 4px; border: 1px dashed var(--ink-soft); background: transparent; }
.cov-seg.confidence-auto     { background: var(--accent);      border: 1px solid var(--accent); }
.cov-seg.confidence-inferred { background: var(--accent-warm); border: 1px solid var(--accent-warm); }
.cov-seg.confidence-manual   { background: #5b7fa6;            border: 1px solid #5b7fa6; }
/* the coverage block is now the first child, so the first section no longer
   matches :first-child -- give it the same "no top rule" treatment by hand */
.coverage + section h2.section-h { margin-top: 24px; padding-top: 0; border-top: none; }
.inline-switch { color: var(--accent); cursor: pointer; text-decoration: underline; }
.inline-switch:hover { color: var(--accent-warm); }
.um-swatch {
  display: inline-block; width: 16px; height: 16px; border-radius: 4px; margin-right: 8px;
  border: 1px solid rgba(0,0,0,.18); vertical-align: middle;
}

.rel-row { display: flex; flex-wrap: wrap; gap: 18px; margin: 4px 0 18px; font-size: 12.8px; }
.rel-row .rel-group strong { display: block; font-size: 10.5px; letter-spacing: .07em;
  text-transform: uppercase; color: var(--ink-soft); opacity: .75; margin-bottom: 5px; font-weight: 600; }
.chip-link {
  display: inline-block; margin: 0 6px 6px 0; padding: 3px 10px; border-radius: 999px;
  background: var(--paper); text-decoration: none; color: var(--ink); font-size: 12px;
  border: 1px solid var(--paper-line);
}
.chip-link:hover { background: var(--map-js-bg); }
.chip-plain {
  display: inline-block; margin: 0 6px 6px 0; padding: 3px 10px; border-radius: 999px;
  background: var(--paper); color: var(--ink-soft); font-size: 12px; border: 1px dashed var(--paper-line);
}

.tabs { margin-top: 6px; }
.tabs input[type="radio"] { position: absolute; opacity: 0; pointer-events: none; }
.tab-labels { display: flex; gap: 4px; border-bottom: 1px solid var(--paper-line); margin-bottom: 14px; }
.tab-labels label {
  cursor: pointer; font-size: 12.5px; padding: 7px 14px; color: var(--ink-soft);
  border-bottom: 2px solid transparent; margin-bottom: -1px;
}
.tab-panel { display: none; }
.tabs input.r-0:checked ~ .tab-panels .tab-panel:nth-child(1) { display: block; }
.tabs input.r-1:checked ~ .tab-panels .tab-panel:nth-child(2) { display: block; }
.tabs input.r-2:checked ~ .tab-panels .tab-panel:nth-child(3) { display: block; }
.tabs input.r-0:checked ~ .tab-labels label.l-0,
.tabs input.r-1:checked ~ .tab-labels label.l-1,
.tabs input.r-2:checked ~ .tab-labels label.l-2 { color: var(--ink); border-bottom-color: var(--accent-warm); font-weight: 600; }

.code-wrap { position: relative; }
.copy-btn {
  position: absolute; top: 8px; right: 8px; z-index: 2;
  font-size: 11px; padding: 4px 10px; border-radius: 6px; cursor: pointer;
  background: var(--ink); color: #eef2f4; border: none; opacity: .75;
  font-family: var(--font-body);
}
.copy-btn:hover { opacity: 1; }
pre.code {
  margin: 0; padding: 16px 18px; border-radius: 10px; overflow-x: auto;
  background: #101d30; color: #d8e2ea; font-family: var(--font-mono);
  font-size: 12.6px; line-height: 1.55; max-height: 520px; overflow-y: auto;
}
pre.code code { white-space: pre; }
.tok-tag { color: #7fb0d8; } .tok-attr { color: #e0b168; } .tok-str { color: #9fca8f; }
.tok-com { color: #6c7f95; font-style: italic; } .tok-doctype { color: #6c7f95; }
.tok-kw { color: #d391c6; } .tok-num { color: #e0a75e; } .tok-fn { color: #7fb0d8; }
.tok-sel { color: #7fb0d8; } .tok-prop { color: #9fca8f; } .tok-var { color: #e0b168; }

/* docgen-r3: pre.code and .dep-graph-wrap already scroll internally on
   overflow (see MINIFIED_MAX_FILE_FOR_FULL_DUMP-truncated code, and the
   dependency graph); struct-table had no equivalent, so a long selector
   or file path forced the whole page to scroll horizontally instead of
   just the one table. */
.table-wrap { overflow-x: auto; margin: 4px 0 18px; }
.table-wrap .struct-table { margin: 0; }
.struct-table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 4px 0 18px; }
.struct-table th {
  text-align: left; font-size: 10.5px; letter-spacing: .06em; text-transform: uppercase;
  color: var(--ink-soft); opacity: .75; padding: 6px 10px; border-bottom: 1px solid var(--paper-line);
}
.struct-table td { padding: 7px 10px; border-bottom: 1px solid var(--paper); vertical-align: top; }
.struct-table code { font-family: var(--font-mono); font-size: 12px; background: var(--paper);
  padding: 1px 5px; border-radius: 4px; }
.struct-sub-h { font-size: 12px; letter-spacing: .05em; text-transform: uppercase;
  color: var(--ink-soft); opacity: .8; margin: 20px 0 6px; }
.kss-comment { font-size: 12.5px; color: var(--ink-soft); margin: 2px 0 4px; }
.muted { color: var(--ink-soft); opacity: .8; font-size: 13px; }
.doc-desc { font-size: 13px; color: var(--ink-soft); margin: 2px 0 6px; }
.func-sig { font-family: var(--font-mono); font-size: 12.8px; color: var(--ink); }
.func-block { padding: 10px 0; border-top: 1px solid var(--paper); }
.func-block:first-child { border-top: none; }
.param-list { margin: 4px 0 0; padding-left: 18px; font-size: 12.5px; color: var(--ink-soft); }

footer.doc-footer {
  padding: 30px 40px 60px; color: var(--ink-soft); font-size: 12.5px;
}

@media (max-width: 880px) {
  .hamburger-btn { display: block; }  /* docgen-r1 */
  .sidebar { position: fixed; left: -100%; transition: left .18s ease; z-index: 50;
    box-shadow: 8px 0 24px rgba(0,0,0,.2); }
  .sidebar.open { left: 0; }
  .content { padding: 24px 18px 100px; }
  #doc-search { width: 130px; }
  /* docgen-r2: brand+timestamp+3 stat chips+search never fit a phone-width
     row together -- drop the two lowest-value items (the timestamp is
     secondary metadata; the counts are already in the Overview stat
     cards) and let the project name truncate instead of overflowing. */
  .topbar .meta, .topbar .stat-chip { display: none; }
  /* docgen-h1 fix: the manual-switch tabs reintroduced the same overflow
     docgen-r2 fixed -- same remedy, drop the label text, keep the icon. */
  .manual-tab-text { display: none; }
  .manual-tab-label { padding: 6px 8px; font-size: 15px; }
  .topbar .brand { flex: 1 1 auto; min-width: 0; }
  .topbar .brand span {
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0;
  }
  .sidebar.open ~ .sidebar-backdrop {
    display: block; position: fixed; inset: 0; background: rgba(10,16,26,.45); z-index: 45;
  }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .tree details > summary::before, .sidebar { transition: none; }
}

@media print {
  .sidebar, .topbar, .copy-btn { display: none; }
  .content { max-width: none; padding: 0; }
  pre.code { max-height: none; }
}
"""


DOC_JS = """
(function () {
  "use strict";

  // ---- Collapse all / expand all (docgen-r4) ----
  var toggleAllBtn = document.getElementById("tree-toggle-all");
  if (toggleAllBtn) {
    toggleAllBtn.addEventListener("click", function () {
      var allDetails = document.querySelectorAll(".tree details");
      var anyOpen = Array.prototype.some.call(allDetails, function (d) { return d.open; });
      allDetails.forEach(function (d) { d.open = !anyOpen; });
      toggleAllBtn.textContent = anyOpen ? "Expand all" : "Collapse all";
    });
  }

  // ---- Search/filter over the file tree and sections ----
  var searchInput = document.getElementById("doc-search");
  var tree = document.querySelector(".tree");
  if (searchInput && tree) {
    searchInput.addEventListener("input", function () {
      var q = searchInput.value.trim().toLowerCase();
      var items = tree.querySelectorAll("li[data-name]");
      if (!q) {
        tree.setAttribute("data-filtering", "false");
        items.forEach(function (li) { li.removeAttribute("data-match"); });
        return;
      }
      tree.setAttribute("data-filtering", "true");
      items.forEach(function (li) {
        var name = li.getAttribute("data-name") || "";
        var match = name.indexOf(q) !== -1;
        li.setAttribute("data-match", match ? "true" : "false");
        if (match) {
          var p = li.parentElement;
          while (p) {
            var details = p.closest ? p.closest("details") : null;
            if (!details) break;
            details.open = true;
            p = details.parentElement;
          }
        }
      });
    });
  }

  // ---- Highlight the active file in the sidebar while scrolling (scrollspy) ----
  var fileLinks = Array.prototype.slice.call(document.querySelectorAll(".tree .file-link"));
  var sections = fileLinks
    .map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); })
    .filter(Boolean);

  if (sections.length && "IntersectionObserver" in window) {
    var byId = {};
    fileLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = byId[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          fileLinks.forEach(function (a) { a.classList.remove("active"); });
          link.classList.add("active");
          var details = link.closest("details");
          while (details) {
            details.open = true;
            details = details.parentElement ? details.parentElement.closest("details") : null;
          }
        }
      });
    }, { rootMargin: "-15% 0px -70% 0px", threshold: 0 });

    sections.forEach(function (s) { observer.observe(s); });
  }

  // ---- Copy code ----
  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var pre = btn.parentElement.querySelector("pre.code");
      if (!pre) return;
      var text = pre.textContent;
      var done = function () {
        var old = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = old; }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(done);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    });
  });

  // ---- Mobile menu ----
  // docgen-h1: two manuals means two <nav class="sidebar">, one per
  // #code-manual/#user-manual layout -- only one is ever visible (CSS
  // hides the other via the manual-switch radios), so "the active one" is
  // whichever layout matches the checked radio, not just the first match.
  var toggle = document.getElementById("sidebar-toggle");
  var userManualRadio = document.getElementById("switch-user-manual");
  function activeLayout() {
    var userOnly = document.body.getAttribute("data-manuals") === "user";
    var id = ((userManualRadio && userManualRadio.checked) || userOnly) ? "user-manual" : "code-manual";
    return document.getElementById(id);
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var layout = activeLayout();
      var sidebar = layout ? layout.querySelector(".sidebar") : null;
      if (sidebar) sidebar.classList.toggle("open");
    });
    document.querySelectorAll(".sidebar .file-link, .sidebar .quicknav a").forEach(function (a) {
      a.addEventListener("click", function () {
        var sb = a.closest(".sidebar");
        if (sb) sb.classList.remove("open");
      });
    });
    document.querySelectorAll(".sidebar-backdrop").forEach(function (bd) {
      bd.addEventListener("click", function () {
        var sb = bd.parentElement ? bd.parentElement.querySelector(".sidebar") : null;
        if (sb) sb.classList.remove("open");
      });
    });
  }
})();
"""


# --------------------------------------------------------------------------
# Assembling the document's HTML fragments
# --------------------------------------------------------------------------

COMPASS_SVG = (
    '<svg class="compass" width="26" height="26" viewBox="0 0 26 26" '
    'aria-hidden="true"><circle cx="13" cy="13" r="11.5" fill="none" '
    'stroke="#8a9bab" stroke-width="1" opacity=".55"/>'
    '<path d="M13,2 L15.8,10.2 L24,13 L15.8,15.8 L13,24 L10.2,15.8 L2,13 L10.2,10.2 Z" '
    'fill="#b5762f"/><circle cx="13" cy="13" r="1.6" fill="#eef2f4"/></svg>'
)


_IMPORTANCE_DOT_CLASS = {
    "source-other": "k-source", "config": "k-config",
    "docs": "k-config", "asset": "k-other",
}
_IMPORTANCE_DIMMED = {"asset"}  # docgen-006: only true assets get muted


def _leaf_node_html(node: TreeNode, linkable: set) -> str:
    slug = slugify(node.rel_path)
    # plan.json: a file routed for deep analysis can still have deep_analyze
    # set to 0, in which case there's no card for the sidebar to link to --
    # falls back to the same non-clickable treatment as a config/docs file.
    if node.kind in ("html", "css", "js") and node.rel_path in linkable:
        return (
            f'<li data-name="{esc(node.rel_path.lower())}">'
            f'<a class="file-link" href="#{slug}">'
            f'<span class="dot k-{node.kind}"></span>{esc(node.name)}</a></li>'
        )
    if node.kind in ("html", "css", "js"):
        dot_cls, style = f"k-{node.kind}", "cursor:default"
    else:
        dot_cls = _IMPORTANCE_DOT_CLASS.get(node.kind, "k-other")
        style = "cursor:default;opacity:.55" if node.kind in _IMPORTANCE_DIMMED else "cursor:default"
    return (
        f'<li data-name="{esc(node.rel_path.lower())}">'
        f'<span class="file-link" style="{style}">'
        f'<span class="dot {dot_cls}"></span>{esc(node.name)}</span></li>'
    )


def _render_children_html(children: list, depth: int, linkable: set) -> str:
    """docgen-006: renders a directory's children, grouping asset-tier
    files (icons, fonts, etc.) into one collapsed 'Assets (N)' entry once
    there are enough of them to bury the files that actually matter --
    everything else (dirs, core source, source-other, config, docs) is
    listed exactly as before."""
    prominent, assets = [], []
    for c in children:
        (assets if (not c.is_dir and c.kind == "asset") else prominent).append(c)

    parts = [_tree_node_html(c, depth, linkable) for c in prominent]
    if len(assets) >= ASSET_GROUP_THRESHOLD:
        inner = "".join(_leaf_node_html(a, linkable) for a in assets)
        names = " ".join(a.name.lower() for a in assets)
        parts.append(
            f'<li data-name="{esc(names)}">'
            f'<details><summary>Assets ({len(assets)})</summary>'
            f'<ul>{inner}</ul></details></li>'
        )
    else:
        parts.extend(_leaf_node_html(a, linkable) for a in assets)
    return "".join(parts)


def _tree_node_html(node: TreeNode, depth: int, linkable: set) -> str:
    if node.is_dir:
        children_html = _render_children_html(node.children, depth + 1, linkable)
        open_attr = " open" if depth < 1 else ""
        return (
            f'<li data-name="{esc(node.name.lower())}">'
            f'<details{open_attr}><summary>{esc(node.name)}/</summary>'
            f'<ul>{children_html}</ul></details></li>'
        )
    return _leaf_node_html(node, linkable)


def build_sidebar_tree(tree: TreeNode, linkable: set) -> str:
    inner = _render_children_html(tree.children, 0, linkable)
    return f'<ul class="tree" id="file-tree">{inner}</ul>'


def _relations_for(path: str, edges: list, all_paths: set, linkable: set):
    """Returns (structural_out, structural_in, semantic_out, semantic_in).
    Structural links (link/script/import/require/page navigation) are shown
    as "Depends on / Used in". Semantic DOM links (JS reaches into an
    element, CSS targets a class) are shown separately — that's not a
    "dependency" in the load-order sense, it's which HTML elements the file
    actually touches. `linkable` (plan.json's deep_analyze=1 files) controls
    whether a chip gets an href -- a file the plan excluded from analysis
    still shows up as a relationship, just not as a dead link to a card
    that was never generated."""
    def slug_if_linkable(p):
        return slugify(p) if p in linkable else None

    structural_out, structural_in = [], []
    semantic_out, semantic_in = [], []
    seen = set()
    for e in edges:
        if e.src == path and e.dst not in (path, "?"):
            key = ("out", e.dst, e.kind)
            if key in seen:
                continue
            seen.add(key)
            if e.kind in _STRUCTURAL_EDGE_KINDS:
                if e.kind == "external":
                    structural_out.append((e.dst, None, e.kind))
                elif e.dst in all_paths:
                    structural_out.append((e.dst, slug_if_linkable(e.dst), e.kind))
            elif e.kind in _SEMANTIC_EDGE_KINDS and e.dst in all_paths:
                semantic_out.append((e.dst, slug_if_linkable(e.dst), e.kind))
        if e.dst == path and e.src != path:
            key = ("in", e.src, e.kind)
            if key in seen:
                continue
            seen.add(key)
            if e.kind in _STRUCTURAL_EDGE_KINDS:
                structural_in.append((e.src, slug_if_linkable(e.src), e.kind))
            elif e.kind in _SEMANTIC_EDGE_KINDS:
                semantic_in.append((e.src, slug_if_linkable(e.src), e.kind))
    # de-duplicate by file while preserving order of first appearance
    def dedup(items):
        out, seen_names = [], set()
        for it in items:
            if it[0] in seen_names:
                continue
            seen_names.add(it[0])
            out.append(it)
        return out
    return (dedup(structural_out), dedup(structural_in),
            dedup(semantic_out), dedup(semantic_in))


def _rel_row_html(structural_out: list, structural_in: list,
                   semantic_out: list = (), semantic_in: list = (),
                   semantic_out_label: str = "Touches elements in",
                   semantic_in_label: str = "Styled / scripted from") -> str:
    def chips(items):
        out = []
        for name, href, kind in items:
            if href:
                out.append(f'<a class="chip-link" href="#{href}">{esc(name)}</a>')
            else:
                out.append(f'<span class="chip-plain">{esc(name)}</span>')
        return "".join(out) if out else '<span class="muted">—</span>'

    html = (
        '<div class="rel-row">'
        f'<div class="rel-group"><strong>Depends on</strong>{chips(structural_out)}</div>'
        f'<div class="rel-group"><strong>Used in</strong>{chips(structural_in)}</div>'
        "</div>"
    )
    if semantic_out or semantic_in:
        html += '<div class="rel-row">'
        if semantic_out:
            html += f'<div class="rel-group"><strong>{esc(semantic_out_label)}</strong>{chips(semantic_out)}</div>'
        if semantic_in:
            html += f'<div class="rel-group"><strong>{esc(semantic_in_label)}</strong>{chips(semantic_in)}</div>'
        html += "</div>"
    return html


def _badges_html(kind: str, info) -> str:
    badges = [f'<span class="badge k-{kind}">{kind.upper()}</span>']
    badges.append(f'<span class="badge">{human_size(info.size)}</span>')
    badges.append(f'<span class="badge">{info.loc} lines</span>')
    if info.is_minified:
        badges.append('<span class="badge warn">minified</span>')
    return '<div class="file-badges">' + "".join(badges) + "</div>"


def _tabs_open(slug: str, labels: list) -> str:
    radios = "".join(
        f'<input class="r-{i}" type="radio" name="tabs-{slug}" id="tab-{i}-{slug}"'
        f'{" checked" if i == 0 else ""}>'
        for i in range(len(labels))
    )
    label_tags = "".join(
        f'<label class="l-{i}" for="tab-{i}-{slug}">{esc(lbl)}</label>'
        for i, lbl in enumerate(labels)
    )
    return f'<div class="tabs">{radios}<div class="tab-labels">{label_tags}</div><div class="tab-panels">'


_TABS_CLOSE = "</div></div>"


def _code_panel(slug: str, raw: str, kind: str) -> str:
    if len(raw) > MINIFIED_MAX_FILE_FOR_FULL_DUMP:
        shown = raw[:MINIFIED_MAX_FILE_FOR_FULL_DUMP]
        note = (f'<p class="muted">This file is large ({human_size(len(raw))}) — showing the first '
                f'{MINIFIED_MAX_FILE_FOR_FULL_DUMP} characters.</p>')
    else:
        shown, note = raw, ""
    highlighted = highlight_by_kind(shown, kind)
    return (
        '<div class="tab-panel">' + note +
        '<div class="code-wrap"><button class="copy-btn" type="button">Copy</button>'
        f'<pre class="code"><code>{highlighted}</code></pre></div></div>'
    )


def _struct_panel_html(info: HtmlInfo) -> str:
    parts = ['<div class="tab-panel">']

    meta_rows = [
        ("Title (&lt;title&gt;)", info.title or "—"),
        ("lang", info.lang or "—"),
        ("meta description", info.meta_description or "—"),
        ("DOCTYPE", "present" if info.doctype_ok else "missing"),
        ("Word count", str(info.word_count)),
    ]
    parts.append('<div class="table-wrap">')  # docgen-r3
    parts.append('<table class="struct-table"><tbody>')
    for label, val in meta_rows:
        parts.append(f"<tr><th>{label}</th><td>{esc(val)}</td></tr>")
    parts.append("</tbody></table>")
    parts.append("</div>")  # docgen-r3

    if info.landmarks:
        chips = "".join(f'<span class="chip-plain">&lt;{esc(t)}&gt;</span>'
                         for t in sorted(info.landmarks))
        parts.append(f'<div class="struct-sub-h">Semantic landmark tags</div><div>{chips}</div>')

    if info.headings:
        parts.append('<div class="struct-sub-h">Heading structure</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>Level</th><th>Text</th></tr></thead><tbody>')
        for level, text in info.headings[:40]:
            indent = "&nbsp;" * ((level - 1) * 3)
            parts.append(f"<tr><td><code>h{level}</code></td><td>{indent}{esc(text)}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.forms:
        parts.append('<div class="struct-sub-h">Forms</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>action</th><th>method</th><th>fields</th></tr></thead><tbody>')
        for f in info.forms:
            fields = ", ".join(f["fields"]) or "—"
            parts.append(f"<tr><td><code>{esc(f['action'] or '(current page)')}</code></td>"
                         f"<td><code>{esc(f['method'])}</code></td><td>{esc(fields)}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.images:
        no_alt = sum(1 for i in info.images if not i.get("alt"))
        parts.append(f'<div class="struct-sub-h">Images ({len(info.images)}'
                      + (f", missing alt: {no_alt}" if no_alt else "") + ")</div>")
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>src</th><th>alt</th></tr></thead><tbody>')
        for img in info.images[:30]:
            alt = img.get("alt") or ""
            alt_html = esc(alt) if alt else '<span class="badge warn">no alt</span>'
            parts.append(f"<tr><td><code>{esc(img.get('src',''))}</code></td><td>{alt_html}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.ids or info.classes:
        parts.append('<div class="struct-sub-h">id / class on this page</div>')
        id_chips = "".join(f'<span class="chip-plain">#{esc(i)}</span>' for i in sorted(info.ids)[:40])
        class_chips = "".join(f'<span class="chip-plain">.{esc(c)}</span>' for c in sorted(info.classes)[:60])
        parts.append(f"<div>{id_chips}</div><div style='margin-top:6px'>{class_chips}</div>")

    if info.comments:
        parts.append('<div class="struct-sub-h">Comments in the markup</div><ul class="param-list">')
        for c in info.comments[:20]:
            c_short = c if len(c) < 160 else c[:160] + "…"
            parts.append(f"<li>{esc(c_short)}</li>")
        parts.append("</ul>")

    if info.hrefs_external:
        chips = "".join(f'<span class="chip-plain">{esc(h)}</span>' for h in info.hrefs_external[:20])
        parts.append(f'<div class="struct-sub-h">External links</div><div>{chips}</div>')

    parts.append("</div>")
    return "".join(parts)


def build_file_card_html(path: str, info: HtmlInfo, edges: list, all_paths: set, linkable: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths, linkable)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(info.title or path)}</h3>'
        + _badges_html("html", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Links to pages",
                        semantic_in_label="Styled / scripted from")
    )
    tabs = _tabs_open(slug, ["Code", "Structure"])
    body = _code_panel(slug, info.raw, "html") + _struct_panel_html(info)
    return header + tabs + body + _TABS_CLOSE + "</article>"


def _color_swatch(color: str) -> str:
    safe = esc(color)
    try:
        style = f"background:{safe}"
    except Exception:
        style = ""
    return f'<span class="swatch" data-label="{safe}" style="{style}" title="{safe}"></span>'


def _struct_panel_css(info: CssInfo) -> str:
    parts = ['<div class="tab-panel">']

    nested_count = sum(len(a.nested_rules) for a in info.at_rules)
    top_rows = [
        ("Rules total (including those nested in @media)", str(len(info.rules) + nested_count)),
        ("At-rules (@media/@keyframes/…)", str(len(info.at_rules))),
        ("Imports (@import)", str(len(info.imports)) if info.imports else "0"),
    ]
    parts.append('<div class="table-wrap">')  # docgen-r3
    parts.append('<table class="struct-table"><tbody>')
    for label, val in top_rows:
        parts.append(f"<tr><th>{label}</th><td>{esc(val)}</td></tr>")
    parts.append("</tbody></table>")
    parts.append("</div>")  # docgen-r3

    if info.custom_props_defined:
        parts.append('<div class="struct-sub-h">CSS custom properties defined here</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>Property</th><th>Value</th></tr></thead><tbody>')
        for name, value in info.custom_props_defined.items():
            swatch = _color_swatch(value) if _COLOR_RE.match(value.strip()) else ""
            parts.append(f"<tr><td><code>{esc(name)}</code></td><td>{swatch} <code>{esc(value)}</code></td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.breakpoints:
        chips = "".join(f'<span class="chip-plain">{esc(b)}</span>' for b in sorted(info.breakpoints))
        parts.append(f'<div class="struct-sub-h">Media breakpoints</div><div>{chips}</div>')

    at_by_kind: dict = {}
    for a in info.at_rules:
        if a.kind in ("media", "import"):
            continue
        at_by_kind.setdefault(a.kind, []).append(a.prelude)
    for kind, items in at_by_kind.items():
        chips = "".join(f'<span class="chip-plain">{esc(p)}</span>' for p in items[:20])
        parts.append(f'<div class="struct-sub-h">@{esc(kind)}</div><div>{chips}</div>')

    all_rules_with_ctx = [(r, None) for r in info.rules]
    for a in info.at_rules:
        for r in a.nested_rules:
            all_rules_with_ctx.append((r, a.prelude))

    if all_rules_with_ctx:
        cap = 80
        parts.append(f'<div class="struct-sub-h">Rules '
                      f'({len(all_rules_with_ctx)}{" — showing the first " + str(cap) if len(all_rules_with_ctx) > cap else ""})</div>')
        for rule, ctx in all_rules_with_ctx[:cap]:
            sel_html = ", ".join(f"<code>{esc(s)}</code>" for s in rule.selectors)
            ctx_html = f' <span class="muted">inside {esc(ctx)}</span>' if ctx else ""
            comment_html = f'<div class="kss-comment">{esc(rule.comment)}</div>' if rule.comment else ""
            decls_preview = "; ".join(f"{p}: {v}" for p, v in rule.declarations[:5])
            more = "; …" if len(rule.declarations) > 5 else ""
            parts.append(
                '<div class="func-block">'
                f'<div class="func-sig">{sel_html}{ctx_html}</div>'
                f"{comment_html}"
                f'<div class="doc-desc"><code>{esc(decls_preview)}{esc(more)}</code></div>'
                "</div>"
            )

    if info.unmatched_selectors:
        chips = "".join(
            f'<span class="chip-plain">{esc(s if s.startswith("[") else "." + s)}</span>'
            for s in info.unmatched_selectors[:30]
        )
        parts.append(
            '<div class="note-block"><h4>Cartographer\'s note</h4>'
            "<p class='muted' style='margin:0 0 8px'>These classes/ids are used in this file's selectors, "
            "but weren't found in any HTML file in the project. The elements might be added dynamically "
            f"via JS, or this could be leftover unused code.</p><div>{chips}</div></div>"
        )

    parts.append("</div>")
    return "".join(parts)


def build_file_card_css(path: str, info: CssInfo, edges: list, all_paths: set, linkable: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths, linkable)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(path.split("/")[-1])}</h3>'
        + _badges_html("css", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Applied on pages",
                        semantic_in_label="")
    )
    tabs = _tabs_open(slug, ["Code", "Structure"])
    body = _code_panel(slug, info.raw, "css") + _struct_panel_css(info)
    return header + tabs + body + _TABS_CLOSE + "</article>"


def _doc_block_html(doc: Optional[dict]) -> str:
    if not doc:
        return ""
    out = []
    if doc.get("description"):
        out.append(f'<div class="doc-desc">{esc(doc["description"])}</div>')
    if doc.get("params"):
        out.append('<ul class="param-list">')
        for name, desc in doc["params"].items():
            out.append(f"<li><code>{esc(name)}</code> — {esc(desc)}</li>")
        out.append("</ul>")
    if doc.get("returns"):
        out.append(f'<div class="doc-desc"><em>Returns:</em> {esc(doc["returns"])}</div>')
    for ex in doc.get("examples", []):
        out.append(f'<pre class="code" style="margin-top:6px"><code>{esc(ex)}</code></pre>')
    return "".join(out)


def _func_block_html(fn: JsFunctionInfo) -> str:
    params = ", ".join(fn.params)
    exported = ' <span class="badge">export</span>' if fn.is_exported else ""
    undoc = "" if fn.doc else ' <span class="badge warn">no JSDoc</span>'  # docgen-005
    kind_label = {"function": "function", "arrow": "const (arrow)",
                  "method": "method", "constructor": "constructor"}.get(fn.kind, fn.kind)
    return (
        '<div class="func-block">'
        f'<div class="func-sig">{esc(kind_label)} <strong>{esc(fn.name)}</strong>({esc(params)})'
        f' <span class="muted">· line {fn.line}</span>{exported}{undoc}</div>'
        + _doc_block_html(fn.doc) +
        "</div>"
    )


def _jsdoc_coverage_html(info: JsInfo) -> str:
    """docgen-005: a flat list of 200+ functions makes 'about half of these
    have no explanation at all' undiscoverable without counting by hand --
    surface it as one line before the list itself."""
    total = len(info.functions) + sum(len(c.methods) for c in info.classes)
    if total == 0:
        return ""
    documented = (sum(1 for fn in info.functions if fn.doc)
                  + sum(1 for c in info.classes for m in c.methods if m.doc))
    pct = round(100 * documented / total)
    return (f'<p class="muted" style="margin:2px 0 14px">JSDoc coverage: '
            f'<strong>{documented} / {total}</strong> functions and methods ({pct}%) '
            f'have a description. Entries without one are marked '
            f'<span class="badge warn">no JSDoc</span> below.</p>')


def _struct_panel_js(info: JsInfo) -> str:
    parts = ['<div class="tab-panel">']

    if info.top_comment:
        parts.append(f'<div class="doc-desc">{esc(info.top_comment)}</div>')

    if info.imports or info.requires:
        parts.append('<div class="struct-sub-h">Imports</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>From</th><th>What</th></tr></thead><tbody>')
        for imp in info.imports:
            names = imp.get("names") or []
            label = imp.get("namespace") and f"* as {imp['namespace']}" or \
                (", ".join(filter(None, [imp.get("default_name")] + names)) or "(side effect only)")
            dyn = " <span class='badge'>dynamic</span>" if imp.get("dynamic") else ""
            parts.append(f"<tr><td><code>{esc(imp['source'])}</code></td><td>{esc(label)}{dyn}</td></tr>")
        for req in info.requires:
            parts.append(f"<tr><td><code>{esc(req)}</code></td><td>require()</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.exports:
        chips = "".join(f'<span class="chip-plain">{esc(e)}</span>' for e in info.exports)
        parts.append(f'<div class="struct-sub-h">Exports</div><div>{chips}</div>')

    if info.functions or info.classes:
        parts.append(_jsdoc_coverage_html(info))

    if info.functions:
        parts.append(f'<div class="struct-sub-h">Functions ({len(info.functions)})</div>')
        for fn in info.functions:
            parts.append(_func_block_html(fn))

    if info.classes:
        parts.append(f'<div class="struct-sub-h">Classes ({len(info.classes)})</div>')
        for cls in info.classes:
            extends = f" extends {esc(cls.extends)}" if cls.extends else ""
            parts.append(
                '<div class="func-block">'
                f'<div class="func-sig">class <strong>{esc(cls.name)}</strong>{extends} '
                f'<span class="muted">· line {cls.line}</span></div>'
                + _doc_block_html(cls.doc)
            )
            for m in cls.methods:
                parts.append(
                    '<div style="margin-left:16px;border-top:1px dashed var(--paper-line);padding-top:8px">'
                    + _func_block_html(m) + "</div>"
                )
            parts.append("</div>")

    if info.dom_queries:
        parts.append('<div class="struct-sub-h">DOM access</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>Method</th><th>Selector</th><th>Line</th></tr></thead><tbody>')
        for q in info.dom_queries:
            parts.append(f"<tr><td><code>{esc(q['method'])}</code></td>"
                         f"<td><code>{esc(q['selector'])}</code></td><td>{q['line']}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.event_listeners:
        parts.append('<div class="struct-sub-h">Event listeners</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>Target</th><th>Event</th><th>Line</th></tr></thead><tbody>')
        for ev in info.event_listeners:
            parts.append(f"<tr><td><code>{esc(ev['target'])}</code></td>"
                         f"<td><code>{esc(ev['event'])}</code></td><td>{ev['line']}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.network_calls:
        chips = "".join(f'<span class="chip-plain">{esc(c["kind"])} · line {c["line"]}</span>'
                         for c in info.network_calls)
        parts.append(f'<div class="struct-sub-h">Network calls</div><div>{chips}</div>')

    if info.todos:
        parts.append('<div class="note-block"><h4>TODO / FIXME</h4><ul>')
        for t in info.todos:
            parts.append(f"<li><code>{esc(t['marker'])}</code> (line {t['line']}): {esc(t['text'])}</li>")
        parts.append("</ul></div>")

    if not any([info.imports, info.requires, info.exports, info.functions,
                info.classes, info.dom_queries, info.event_listeners]):
        parts.append('<p class="muted">No explicit structure (functions, classes, imports) was found.</p>')

    parts.append("</div>")
    return "".join(parts)


def build_file_card_js(path: str, info: JsInfo, edges: list, all_paths: set, linkable: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths, linkable)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(path.split("/")[-1])}</h3>'
        + _badges_html("js", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Targets elements on",
                        semantic_in_label="")
    )
    tabs = _tabs_open(slug, ["Code", "Structure"])
    body = _code_panel(slug, info.raw, "js") + _struct_panel_js(info)
    return header + tabs + body + _TABS_CLOSE + "</article>"


# --------------------------------------------------------------------------
# Generation plan: an optional intermediate stage between analysis and
# rendering. build_project_data() already knows everything about the
# project; derive_generation_plan() repackages those facts into a flat,
# binary-flag JSON a human or an LLM agent can inspect and hand-edit before
# a single line of HTML is written. Every default is 1 ("show it") --
# this stage is a lever for a person to pull, not a second layer of
# heuristics deciding things on its own. Entirely optional: render_document()
# synthesizes an all-1 plan internally when none is given, so default runs
# are byte-identical to a version of this tool with no plan concept at all.
# --------------------------------------------------------------------------

_PLAN_SECTION_KEYS = ("overview", "dependency_graph", "cartographer_notes", "color_palette")
_PLAN_MANUAL_KEYS = ("user_manual", "code_manual")     # docgen-h8
_PLAN_DIAGNOSTIC_KEYS = ("unused_id_class", "orphan_css_selectors", "unresolved_links",
                         "unresolved_dom_lookups", "images_without_alt", "todo_fixme")


def derive_generation_plan(pdata: "ProjectData", project_title: str) -> dict:
    """Builds an all-1 (show everything) plan reflecting what was actually
    found, so a reader deciding what to flip off can see real counts
    instead of guessing blind."""
    s = pdata.stats
    plan = {
        "meta": {
            "project": project_title,
            "html": s["counts"]["html"], "css": s["counts"]["css"],
            "js": s["counts"]["js"], "other": s["counts"]["other"],
            "_available_diagnostic_counts": {
                "unused_id_class": len(s["unused_ids"]) + len(s["unused_classes"]),
                "orphan_css_selectors": len(s["orphan_css_selectors"]),
                "unresolved_links": len(s["unresolved_links"]),
                "unresolved_dom_lookups": len(s["dom_unresolved"]),
                "images_without_alt": len(s["images_no_alt"]),
                "todo_fixme": len(s["todos"]),
            },
        },
        "sections": {k: 1 for k in _PLAN_SECTION_KEYS},
        "manuals": {k: 1 for k in _PLAN_MANUAL_KEYS},
        "diagnostics": {k: 1 for k in _PLAN_DIAGNOSTIC_KEYS},
        "files": {
            path: {"deep_analyze": 1}
            for path in list(pdata.html_files) + list(pdata.css_files) + list(pdata.js_files)
        },
        "assets": {"group_when_over": ASSET_GROUP_THRESHOLD, "list_individually": 0},
    }
    return plan


def _normalize_plan(plan: dict, pdata: "ProjectData") -> dict:
    """Fills in anything missing from a hand-edited or partial plan with
    the permissive (1) default, so a plan.json with only the three lines
    someone actually cared about changing still works. Never raises on a
    malformed plan -- worst case, missing/invalid pieces fall back to 1."""
    plan = dict(plan) if isinstance(plan, dict) else {}
    sections = dict(plan.get("sections") or {})
    for k in _PLAN_SECTION_KEYS:
        sections[k] = 1 if sections.get(k, 1) else 0
    diagnostics = dict(plan.get("diagnostics") or {})
    for k in _PLAN_DIAGNOSTIC_KEYS:
        diagnostics[k] = 1 if diagnostics.get(k, 1) else 0
    # docgen-h8: which manual(s) render. At least one always does -- a plan
    # that turns both off (a mistake, not a request for an empty file) falls
    # back to showing both rather than producing a blank document.
    manuals = dict(plan.get("manuals") or {})
    for k in _PLAN_MANUAL_KEYS:
        manuals[k] = 1 if manuals.get(k, 1) else 0
    if not any(manuals.values()):
        manuals = {k: 1 for k in _PLAN_MANUAL_KEYS}
    files_in = plan.get("files") or {}
    all_paths = list(pdata.html_files) + list(pdata.css_files) + list(pdata.js_files)
    files = {}
    for path in all_paths:
        entry = files_in.get(path) or {}
        files[path] = {"deep_analyze": 1 if entry.get("deep_analyze", 1) else 0}
    assets_in = plan.get("assets") or {}
    try:
        group_when_over = int(assets_in.get("group_when_over", ASSET_GROUP_THRESHOLD))
    except (TypeError, ValueError):
        group_when_over = ASSET_GROUP_THRESHOLD
    return {
        "meta": plan.get("meta") or {},
        "sections": sections,
        "manuals": manuals,
        "diagnostics": diagnostics,
        "files": files,
        "assets": {"group_when_over": group_when_over,
                    "list_individually": 1 if assets_in.get("list_individually") else 0},
    }


def save_plan(plan: dict, path: Path) -> None:
    path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_plan(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


_WARNING_NOTE_TITLES = {"Unresolved links"}


def build_overview_section(pdata: "ProjectData", plan: dict) -> str:
    if not plan["sections"]["overview"]:
        return ""
    diag = plan["diagnostics"]
    s = pdata.stats
    counts = s["counts"]
    parts = ['<section id="overview">']
    parts.append('<h2 class="section-h">Project overview</h2>')
    parts.append(
        '<p class="lede">An automatically assembled map of the project: '
        f'{counts["html"]} HTML, {counts["css"]} CSS, and {counts["js"]} JS files, '
        f'{human_size(s["total_size"])} of source code, {s["total_loc"]} non-blank lines.</p>'
    )

    parts.append('<div class="card-grid">')
    for label, val in [
        ("HTML files", counts["html"]), ("CSS files", counts["css"]),
        ("JS files", counts["js"]), ("Other files", counts["other"]),
        ("Lines of code", s["total_loc"]), ("Total size", human_size(s["total_size"])),
    ]:
        parts.append(f'<div class="stat-card"><div class="n">{val}</div><div class="l">{label}</div></div>')
    parts.append("</div>")

    parts.append(
        '<div class="legend-row">'
        '<span class="legend-chip"><span class="dot" style="background:var(--map-html)"></span>HTML</span>'
        '<span class="legend-chip"><span class="dot" style="background:var(--map-css)"></span>CSS</span>'
        '<span class="legend-chip"><span class="dot" style="background:var(--map-js)"></span>JS</span>'
        "</div>"
    )

    if s["largest_files"]:
        parts.append('<div class="struct-sub-h">Largest files</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>File</th><th>Size</th><th>Lines</th></tr></thead><tbody>')
        for path, size, loc, kind in s["largest_files"]:
            parts.append(f'<tr><td><a href="#{slugify(path)}"><code>{esc(path)}</code></a></td>'
                         f"<td>{human_size(size)}</td><td>{loc}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if s["palette"] and plan["sections"]["color_palette"]:
        parts.append('<div class="struct-sub-h">Color palette (by usage frequency in CSS)</div>')
        parts.append('<div class="swatch-row">')
        for color, _count in s["palette"]:
            parts.append(_color_swatch(color))
        parts.append("</div>")

    if s["breakpoints"]:
        chips = "".join(f'<span class="chip-plain">{esc(b)}</span>' for b in s["breakpoints"])
        parts.append(f'<div class="struct-sub-h">Responsive breakpoints</div><div>{chips}</div>')

    if s["external_libs"]:
        chips = "".join(f'<span class="chip-plain">{esc(lib)}</span>' for lib in s["external_libs"])
        parts.append(f'<div class="struct-sub-h">External libraries / CDN</div><div>{chips}</div>')

    if not plan["sections"]["cartographer_notes"]:
        parts.append("</section>")
        return "".join(parts)

    notes = []
    if (s["unused_ids"] or s["unused_classes"]) and diag["unused_id_class"]:
        items = [f"#{i}" for i in s["unused_ids"][:15]] + [f".{c}" for c in s["unused_classes"][:25]]
        more = len(s["unused_ids"]) + len(s["unused_classes"]) - len(items)
        notes.append(("Unused id / class",
                      "Declared in HTML, but never matched by a CSS selector or a JS DOM query. "
                      "Might be reserved for future use, or leftover from a refactor.",
                      items, more))
    if s["orphan_css_selectors"] and diag["orphan_css_selectors"]:
        items = [f'{o["file"]}: {o["token"] if o["token"].startswith("[") else "." + o["token"]}'
                 for o in s["orphan_css_selectors"][:20]]
        more = len(s["orphan_css_selectors"]) - len(items)
        notes.append(("CSS rules with no match in HTML",
                      "These selectors target classes/ids not found in any page's static HTML, and not "
                      "assigned anywhere in JS via classList/className either -- likely dead, but a "
                      "class built from a runtime string (e.g. `'tone-' + variant`) can still slip past both checks.",
                      items, more))
    if s["unresolved_links"] and diag["unresolved_links"]:
        items = [f'{u["src"]} → {u["dst"]}' for u in s["unresolved_links"][:20]]
        more = len(s["unresolved_links"]) - len(items)
        notes.append(("Unresolved links",
                      "The path in href/src couldn't be matched to any project file — possibly a typo.",
                      items, more))
    if s["images_no_alt"] and diag["images_without_alt"]:
        items = [f'{i["file"]}: {i["src"]}' for i in s["images_no_alt"][:20]]
        more = len(s["images_no_alt"]) - len(items)
        notes.append(("Images without alt",
                      "Affects accessibility (screen readers) and SEO.",
                      items, more))
    if s["todos"] and diag["todo_fixme"]:
        items = [f'{t["file"]}:{t["line"]} — {t["text"]}' for t in s["todos"][:20]]
        more = len(s["todos"]) - len(items)
        notes.append(("Project-wide TODO / FIXME", "", items, more))
    if s["dom_unresolved"] and diag["unresolved_dom_lookups"]:
        items = [f'{d["file"]}: {d["selector"]}' for d in s["dom_unresolved"][:20]]
        more = len(s["dom_unresolved"]) - len(items)
        notes.append((
            "Unresolved DOM lookups",
            f'{s["dom_queries_total"]} DOM lookup(s) found in JS; {len(s["dom_unresolved"])} use a selector '
            "this scan couldn't match to a static element -- often an attribute selector like [data-x], "
            "or a selector built from a variable rather than a literal string. Not necessarily broken: "
            "these are real, just outside what this analysis can trace.",
            items, more,
        ))

    if notes:
        parts.append('<div class="struct-sub-h">Cartographer\'s notes</div>')
        # docgen-h7: two tiers, as in MSDN's Note/Warning convention -- a
        # Warning is something likely to be a real defect (a path that points
        # nowhere); a Note is worth knowing but not necessarily wrong. Only
        # "Unresolved links" qualifies: "Unresolved DOM lookups" describes a
        # limit of this analysis (its own text says so), so calling it a
        # Warning would contradict itself. Warnings are listed first.
        notes.sort(key=lambda n: n[0] not in _WARNING_NOTE_TITLES)      # stable sort
        for title, desc, items, more in notes:
            is_warning = title in _WARNING_NOTE_TITLES
            parts.append(f'<div class="note-block{" warning" if is_warning else ""}"><h4>'
                         f'<span class="callout-kind">{"Warning" if is_warning else "Note"}</span> '
                         + esc(title) + "</h4>")
            if desc:
                parts.append(f"<p class='muted' style='margin:0 0 8px'>{esc(desc)}</p>")
            parts.append("<ul>" + "".join(f"<li><code>{esc(i)}</code></li>" for i in items) + "</ul>")
            if more > 0:
                parts.append(f'<p class="muted" style="margin:6px 0 0">…and {more} more.</p>')
            parts.append("</div>")
    else:
        parts.append(
            '<div class="note-block empty"><h4>Cartographer\'s notes</h4>'
            "<p class='muted' style='margin:0'>No obvious mismatches between HTML, CSS, and JS were found "
            "(or the checks that would have found them are turned off in the generation plan).</p></div>"
        )

    parts.append("</section>")
    return "".join(parts)


_GRAPH_LEGEND_SVG = (
    '<span class="ln"><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" '
    'stroke="var(--ink-soft)" stroke-width="1.6" opacity=".5"/></svg>structural link '
    "(link/script/import)</span>"
    '<span class="ln"><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" '
    'stroke="var(--map-accent-warm)" stroke-width="1.4" stroke-dasharray="3 3"/></svg>'
    "semantic link (DOM id/class)</span>"
)


# --------------------------------------------------------------------------
# docgen-h5: docgen-manual.md -- the one place a person writes what the
# tool cannot know (intent, FAQ, support, how-to-customize prose). A file in
# the PROJECT, next to README.md and CHANGELOG.md, not something inside the
# generated HTML: the HTML is machine output and is rewritten on every run,
# so anything typed into it would be lost. This file is never overwritten
# by the tool (see --manual-scaffold, which refuses if it already exists).
# Sections are `## Heading` blocks matching a User Manual section; text
# under a heading is shown (as MANUAL), anything inside HTML comments --
# including the generated hints -- is ignored, so an untouched template can
# never be mistaken for a written answer.
# --------------------------------------------------------------------------

_MANUAL_FILE_NAMES = ("docgen-manual.md",)
_MANUAL_SECTION_ALIASES = {
    "overview": "um-overview",
    "requirements": "um-requirements",
    "getting started": "um-getting-started", "installation": "um-getting-started",
    "project structure": "um-structure", "structure": "um-structure",
    "customization": "um-customization", "customisation": "um-customization",
    "third party credits": "um-credits", "credits": "um-credits",
    "faq": "um-faq",
    "changelog": "um-changelog",
    "support": "um-support",
}
_MANUAL_SECTION_ORDER = (
    ("um-overview", "Overview"), ("um-requirements", "Requirements"),
    ("um-getting-started", "Getting started"), ("um-structure", "Project structure"),
    ("um-customization", "Customization"), ("um-credits", "Third-party credits"),
    ("um-faq", "FAQ"), ("um-changelog", "Changelog"), ("um-support", "Support"),
)


def _normalize_heading(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


_FENCE_RE = re.compile(r"(?ms)^[ \t]*(```|~~~)[^\n]*\n.*?^[ \t]*\1[ \t]*$")


def _strip_html_comments(body: str) -> str:
    """Remove HTML comments (hints included) -- but never from inside a
    fenced code block, where `<!-- ... -->` is an example someone wrote on
    purpose, not a note to the tool."""
    out, last = [], 0
    for m in _FENCE_RE.finditer(body):
        out.append(re.sub(r"<!--.*?(?:-->|\Z)", "", body[last:m.start()], flags=re.DOTALL))
        out.append(m.group(0))
        last = m.end()
    out.append(re.sub(r"<!--.*?(?:-->|\Z)", "", body[last:], flags=re.DOTALL))
    return "".join(out)


def parse_manual_md(raw: str, path: str) -> dict:
    """Returns {"path", "sections": {slug: text}, "unknown": [headings]}.
    A section appears in "sections" only if it has real text left after
    HTML comments (hints included) are removed. A `## ` line inside a fenced
    code block is code, not a section heading."""
    text = raw.replace("\r\n", "\n")
    fenced = [(m.start(), m.end()) for m in _FENCE_RE.finditer(text)]
    heads = [m for m in re.finditer(r"(?m)^##[ \t]+(.+?)[ \t]*$", text)
             if not any(a <= m.start() < b for a, b in fenced)]
    sections, unknown = {}, []
    for i, m in enumerate(heads):
        body_end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = _strip_html_comments(text[m.end():body_end]).strip()
        slug = _MANUAL_SECTION_ALIASES.get(_normalize_heading(m.group(1)))
        if slug is None:
            unknown.append(m.group(1).strip())
        elif body:
            sections[slug] = f"{sections[slug]}\n\n{body}" if slug in sections else body
    return {"path": path, "sections": sections, "unknown": unknown}


def build_manual_scaffold(pdata: "ProjectData") -> str:
    """Starter docgen-manual.md: one heading per section, each followed by
    a hint comment saying what the tool already knows and what only a
    person can write. Hints are comments, so leaving one untouched leaves
    the section marked TEMPLATE in the output."""
    pkg = pdata.package_info
    n_props = len({n for c in pdata.css_files.values() for n in c.custom_props_defined})
    n_scripts = len(pkg.scripts) if pkg else 0

    hints = {
        "um-overview": (
            f"{pdata.readme_path} was found at the project root, so this section is already filled from it. "
            "Write below only to ADD something the README does not say."
            if pdata.readme_path else
            "No README.md was found. In a few sentences: what is this project, who is it for, and what problem "
            "does it solve? The tool can see structure but not intent."),
        "um-requirements": (
            "Declared runtime versions and external libraries are filled in automatically. Add what code cannot "
            "show: required server or OS, supported browsers, accounts or API keys."),
        "um-getting-started": (
            (f"{n_scripts} package.json script(s) are listed automatically. " if n_scripts else
             "No package.json scripts were found. ")
            + "Write the real first-run steps: install, configure, run, and what success looks like."),
        "um-structure": (
            "The folder summary is automatic. Add one line per top-level folder saying what it is FOR."),
        "um-customization": (
            (f"{n_props} CSS custom propert{'y' if n_props == 1 else 'ies'} found and listed automatically. "
             if n_props else "No CSS custom properties were found. ")
            + "Explain HOW to use them: switch the color scheme, change fonts, add a page. The tool sees the "
              "properties, not your intent."),
        "um-credits": (
            "Packages, CDN libraries and bundled fonts are listed automatically, but their LICENSES cannot be "
            "read from code. For every font, icon, image and library you did not author: who made it, under which "
            "license, and a link to the source."),
        "um-faq": (
            "Real questions people ask about this project, each as a bold question followed by its answer. "
            "The tool has no way to know what they are."),
        "um-changelog": (
            f"{pdata.changelog_path} was found and is used automatically -- you can delete this heading."
            if pdata.changelog_path else
            "Newest first. A date, then short lines grouped as Added / Changed / Fixed / Removed / Security."),
        "um-support": (
            "How to reach you, what you will help with, what is out of scope, and how long support lasts."),
    }

    lines = [
        "# User Manual -- hand-written parts",
        "",
        "> This file is yours. `doc_generator.py` reads it on every run but never overwrites it.",
        "> Write text under a `##` heading and it appears in the generated User Manual, marked as",
        "> written by hand. Basic markdown works: paragraphs, `-` lists, **bold**, `code`, [links](url).",
        "> Text inside HTML comments is ignored, including the hints below; a section you leave empty",
        "> stays marked TEMPLATE in the output instead of pretending to be an answer.",
        "",
    ]
    for slug, title in _MANUAL_SECTION_ORDER:
        lines += [f"## {title}", f"<!-- docgen-hint: {hints[slug]} -->", ""]
    return "\n".join(lines)


# docgen-h3: shared confidence-tier badge for every User Manual section.
# Four tiers, in decreasing order of "this is a fact about your project":
#   AUTO     -- derived straight from the scanned codebase (file tree, CSS
#               custom properties, README.md content verbatim)
#   INFERRED -- derived from a convention (package.json's declared scripts/
#               engines, "an index.html exists, so open it"), not from the
#               code's own behavior
#   SCAFFOLD -- no project data at all; a template explaining what belongs
#               here, nothing more
#   MANUAL   -- real prose, but written by a person (docgen-manual.md),
#               not verified by the tool in any way
# Tagging every section is the same principle as Cartographer's notes
# saying "worth checking" instead of stating fact: a template must never
# read like a finding, and an inference must never read like a fact.
_CONFIDENCE_TIER_LABEL = {
    "auto": "AUTO — from your project",
    "inferred": "INFERRED — from project conventions",
    "scaffold": "TEMPLATE — needs your input",
    "manual": "FROM docgen-manual.md",
}

_FONT_EXTS = (".ttf", ".otf", ".woff", ".woff2", ".eot")
_IMAGE_EXTS = (".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico")
_UM_TO_CODE_LINK = '<label for="switch-code-manual" class="inline-switch">Code Manual</label>'


def _confidence_badge_html(tier: str) -> str:
    label = _CONFIDENCE_TIER_LABEL.get(tier, tier.upper())
    return f'<span class="badge confidence-{esc(tier)}">{esc(label)}</span>'


def _count_files_in(node: "TreeNode") -> int:
    if not node.is_dir:
        return 1
    return sum(_count_files_in(c) for c in node.children)


def _um_table(headers: list, rows: list) -> str:
    """Cells are already-escaped HTML (callers use esc() / <code>)."""
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return (f'<div class="table-wrap"><table class="struct-table"><thead><tr>{head}</tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


def build_user_manual(pdata: "ProjectData", plan: dict) -> tuple:
    """docgen-h4: the nine User Manual sections. Each is (slug, title, tier,
    body_html); the tier says how much of the body is a fact about the
    project versus a template (see _CONFIDENCE_TIER_LABEL). Where the tool
    cannot know something (FAQ, support, intent), the body says so plainly
    rather than inventing text."""
    pkg = pdata.package_info
    s = pdata.stats
    counts = s["counts"]
    sections = []

    # 1. Overview ------------------------------------------------------
    if pdata.readme_raw:
        sections.append(("um-overview", "Overview", "auto",
            f"<p class=\"muted\">From this project's own <code>{esc(pdata.readme_path)}</code>, shown as written.</p>"
            f'<div class="readme-embed">{_simple_markdown_to_html(pdata.readme_raw)}</div>'))
    elif pkg and pkg.description:
        sections.append(("um-overview", "Overview", "inferred",
            f"<p>{esc(pkg.description)}</p>"
            "<p class=\"muted\">Taken from the <code>description</code> field of <code>package.json</code>; "
            "no <code>README.md</code> was found at the project root.</p>"))
    else:
        sections.append(("um-overview", "Overview", "scaffold",
            f'<p>This project has {counts["html"]} HTML, {counts["css"]} CSS and {counts["js"]} JS files '
            f'({human_size(s["total_size"])}, {s["total_loc"]} non-blank lines).</p>'
            "<p class=\"muted\">No <code>README.md</code> was found at the project root and there is no "
            "<code>package.json</code> description, so nothing here says what this project is <em>for</em>. "
            "Static analysis can see structure, not intent &mdash; write a short paragraph on the project's "
            "purpose and audience here (see <code>docgen-manual.md</code>).</p>"))

    # 2. Requirements --------------------------------------------------
    req_parts, req_tier = [], "auto"
    if pkg and pkg.engines:
        req_tier = "inferred"
        req_parts.append(
            "<p>Runtime versions declared in <code>package.json</code>:</p>"
            + _um_table(["Runtime", "Version"],
                        [[f"<code>{esc(k)}</code>", f"<code>{esc(v)}</code>"] for k, v in pkg.engines.items()]))
    if s["external_libs"]:
        chips = "".join(f'<span class="chip-plain">{esc(lib)}</span>' for lib in s["external_libs"])
        req_parts.append(f"<p>External libraries loaded from a CDN or imported by bare name:</p><div>{chips}</div>")
    if not req_parts:
        req_parts.append(
            "<p>The scan found no declared runtime versions and no external libraries. That only means none are "
            "<em>visible to static analysis</em> &mdash; it does not prove none are needed (a build step, or a "
            "server the project assumes, would not show up here).</p>")
    sections.append(("um-requirements", "Requirements", req_tier, "".join(req_parts)))

    # 3. Getting started -----------------------------------------------
    if pkg and pkg.scripts:
        gs_tier = "inferred"
        gs_body = ("<p>Scripts declared in <code>package.json</code>. You typically run <code>npm install</code> "
                   "once, then one of these:</p>"
                   + _um_table(["Command", "Runs"],
                               [[f"<code>npm run {esc(n)}</code>", f"<code>{esc(c)}</code>"]
                                for n, c in pkg.scripts.items()]))
    else:
        entry = next((p for p in sorted(pdata.html_files) if p.lower() == "index.html"), None)
        if entry is None and pdata.html_files:
            entry = sorted(pdata.html_files)[0]
        if entry:
            gs_tier = "inferred"
            gs_body = ("<p>No <code>package.json</code> scripts were found, so there is no build or dev-server "
                       f"command to run. This looks like a static site: open <code>{esc(entry)}</code> "
                       "directly in a browser.</p>")
        else:
            gs_tier = "scaffold"
            gs_body = ("<p>No HTML entry point and no <code>package.json</code> scripts were found. Describe here "
                       "how someone is meant to run or open this project.</p>")
    sections.append(("um-getting-started", "Getting started", gs_tier, gs_body))

    # 4. Project structure ---------------------------------------------
    struct_rows, root_files = [], 0
    for node in pdata.tree.children:
        if node.is_dir:
            struct_rows.append([f"<code>{esc(node.name)}/</code>", f"{_count_files_in(node)} file(s)"])
        else:
            root_files += 1
    if root_files:
        struct_rows.insert(0, ["<em>(project root)</em>", f"{root_files} file(s)"])
    sections.append(("um-structure", "Project structure", "auto",
        (_um_table(["Location", "Contents"], struct_rows) if struct_rows else "<p>No files were found.</p>")
        + "<p class=\"muted\">The full file-by-file breakdown &mdash; code, structure, and what depends on "
          f"what &mdash; is in the {_UM_TO_CODE_LINK}.</p>"))

    # 5. Customization -------------------------------------------------
    props = {}
    for cpath, cinfo in sorted(pdata.css_files.items()):
        for name, value in cinfo.custom_props_defined.items():
            props.setdefault(name, (value, cpath))
    if props:
        rows = []
        for name, (value, cpath) in props.items():
            swatch = (f'<span class="um-swatch" style="background:{esc(value)}"></span>'
                      if _COLOR_RE.match(value.strip()) else "")
            rows.append([f"<code>{esc(name)}</code>", f"{swatch}<code>{esc(value)}</code>",
                         f"<code>{esc(cpath)}</code>"])
        cust_body = ("<p>CSS custom properties (variables) defined in this project &mdash; where a theme "
                     "change would start:</p>" + _um_table(["Property", "Value", "Defined in"], rows)
                     + f'<p class="muted">Which rules use each one is in the {_UM_TO_CODE_LINK}.</p>')
    else:
        cust_body = ("<p>No CSS custom properties were found, so there is no single place to change colors or "
                     "spacing from &mdash; they are set directly inside individual rules "
                     f"(see the {_UM_TO_CODE_LINK}).</p>")
    sections.append(("um-customization", "Customization", "auto", cust_body))

    # 6. Third-party credits -------------------------------------------
    credit_rows = []
    if pkg:
        for n, v in pkg.dependencies.items():
            credit_rows.append([f"<code>{esc(n)}</code>", f"<code>{esc(v)}</code>", "dependency",
                                "not read by this tool &mdash; see the package"])
        for n, v in pkg.dev_dependencies.items():
            credit_rows.append([f"<code>{esc(n)}</code>", f"<code>{esc(v)}</code>", "dev dependency",
                                "not read by this tool &mdash; see the package"])
    declared = set(pkg.dependencies) | set(pkg.dev_dependencies) if pkg else set()
    for lib in s["external_libs"]:
        if lib not in declared:
            credit_rows.append([f"<code>{esc(lib)}</code>", "&mdash;", "external (CDN / bare import)",
                                "unknown &mdash; verify manually"])
    for p in pdata.other_files:
        if Path(p).suffix.lower() in _FONT_EXTS:
            credit_rows.append([f"<code>{esc(p)}</code>", "&mdash;", "bundled font file",
                                "unknown &mdash; verify manually"])
    credit_parts = []
    if pkg and pkg.license:
        credit_parts.append(f"<p>This project's own license, as declared in <code>package.json</code>: "
                            f"<code>{esc(pkg.license)}</code>.</p>")
    elif pkg:
        credit_parts.append("<p>No <code>license</code> field is declared in <code>package.json</code>.</p>")
    if credit_rows:
        credit_parts.append(_um_table(["Name", "Version", "Kind", "License"], credit_rows))
    else:
        credit_parts.append("<p>No dependencies, external libraries or bundled fonts were detected.</p>")
    n_images = sum(1 for p in pdata.other_files if Path(p).suffix.lower() in _IMAGE_EXTS)
    if n_images:
        credit_parts.append(f"<p class=\"muted\">{n_images} image/icon file(s) are bundled. The tool cannot tell "
                            "who made them; any that are not yours need credit and a license check too.</p>")
    sections.append(("um-credits", "Third-party credits", "inferred" if pkg else "auto", "".join(credit_parts)))

    # 7. FAQ -----------------------------------------------------------
    sections.append(("um-faq", "FAQ", "scaffold",
        "<p>No FAQ can be generated &mdash; the questions people actually ask about a project are not "
        "recorded in its code.</p><p class=\"muted\">Add real question-and-answer pairs here "
        "(see <code>docgen-manual.md</code>).</p>"))

    # 8. Changelog -----------------------------------------------------
    if pdata.changelog_raw:
        sections.append(("um-changelog", "Changelog", "auto",
            f"<p class=\"muted\">From this project's own <code>{esc(pdata.changelog_path)}</code>, shown as written.</p>"
            f'<div class="readme-embed">{_simple_markdown_to_html(pdata.changelog_raw)}</div>'))
    else:
        sections.append(("um-changelog", "Changelog", "scaffold",
            "<p>No <code>CHANGELOG.md</code> or <code>HISTORY.md</code> was found at the project root, and version "
            "history cannot be reconstructed from a single snapshot of the code.</p>"
            "<p class=\"muted\">Keep one entry per release, newest first: a date, then short lines grouped as "
            "Added / Changed / Fixed / Removed / Security.</p>"))

    # 9. Support -------------------------------------------------------
    sections.append(("um-support", "Support", "scaffold",
        "<p>Contact details and what support covers are not something a codebase records.</p>"
        "<p class=\"muted\">State here how to reach you, what you will help with, and what is out of scope.</p>"))

    # docgen-h5: overlay hand-written text from docgen-manual.md. A TEMPLATE
    # section is REPLACED by it (and becomes MANUAL). A section that already
    # has real project data keeps that data and gets the hand-written text
    # appended beneath, under its own MANUAL badge -- so a person's notes
    # never hide, and never get confused with, what the tool derived.
    manual_sections = (pdata.manual_md or {}).get("sections", {})
    overlaid = []
    for slug, title, tier, body in sections:
        text = manual_sections.get(slug)
        if text:
            rendered = _simple_markdown_to_html(text)
            if tier == "scaffold":
                tier = "manual"
                body = ("<p class=\"muted\">Written in <code>docgen-manual.md</code>.</p>"
                        f'<div class="readme-embed">{rendered}</div>')
            else:
                body += ('<div class="manual-note"><p class="muted">'
                         f'{_confidence_badge_html("manual")} Notes added in <code>docgen-manual.md</code>:</p>'
                         f'<div class="readme-embed">{rendered}</div></div>')
        overlaid.append((slug, title, tier, body))
    sections = overlaid

    nav = ('<ul class="quicknav">'
           + "".join(f'<li><a href="#{slug}">{esc(title)}</a></li>' for slug, title, _t, _b in sections)
           + "</ul>")
    # docgen-h6: how much of this manual is real, said up front. Same idea as
    # docgen-005's JSDoc coverage line, one level up: a manual that is 5/9
    # real should say so before the reader has to find out section by
    # section. Counted AFTER the docgen-manual.md overlay, so hand-written
    # sections are not miscounted as templates.
    total = len(sections)
    n_project = sum(1 for _s, _t, tier, _b in sections if tier in ("auto", "inferred"))
    n_manual = sum(1 for _s, _t, tier, _b in sections if tier == "manual")
    n_template = total - n_project - n_manual
    if n_template == 0:
        next_step = "No template sections remain."
    elif pdata.manual_md is None:
        next_step = ("Run <code>python3 doc_generator.py &lt;project&gt; --manual-scaffold</code> to create "
                     "<code>docgen-manual.md</code>, then write the sections only you can.")
    else:
        next_step = f"Fill in the remaining templates in <code>{esc(pdata.manual_md['path'])}</code>."
    segs = "".join(f'<span class="cov-seg confidence-{tier}" title="{esc(title)}"></span>'
                   for _s, title, tier, _b in sections)
    coverage = (f'<div class="coverage"><div class="coverage-bar">{segs}</div>'
                f"<p><strong>{n_project} of {total}</strong> sections are built from your project, "
                f"<strong>{n_manual}</strong> written by hand, <strong>{n_template}</strong> still templates. "
                f"{next_step}</p></div>")
    content = coverage + "".join(
        f'<section id="{slug}"><h2 class="section-h">{esc(title)} {_confidence_badge_html(tier)}</h2>{body}</section>'
        for slug, title, tier, body in sections)
    return nav, content


def build_dependency_section(pdata: "ProjectData") -> str:
    if not pdata.html_files and not pdata.css_files and not pdata.js_files:
        return ""
    svg = render_dependency_graph_svg(pdata.html_files, pdata.css_files, pdata.js_files, pdata.edges)
    return (
        '<section id="dependency-map">'
        '<h2 class="section-h">Dependency map</h2>'
        '<p class="lede">Solid lines are direct references (&lt;link&gt;, &lt;script&gt;, import/require). '
        "Dashed lines are semantic DOM links: which JS/CSS reaches into which HTML elements.</p>"
        f'<div class="graph-legend">{_GRAPH_LEGEND_SVG}</div>'
        f'<div class="dep-graph-wrap">{svg}</div>'
        "</section>"
    )


# --------------------------------------------------------------------------
# Final assembly of the single documentation HTML file (a template with
# placeholders)
# --------------------------------------------------------------------------

DOCUMENT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>__STYLES__</style>
</head>
<body data-manuals="__MANUAL_MODE__">
<input type="radio" name="manual-switch" id="switch-code-manual" class="manual-radio" checked>
<input type="radio" name="manual-switch" id="switch-user-manual" class="manual-radio">
<header class="topbar">
  <button id="sidebar-toggle" class="hamburger-btn" aria-label="Menu">☰</button>
  <div class="brand">__COMPASS__<span>__PROJECT_NAME__</span></div>
  <span class="meta">generated __GENERATED_AT__</span>
  <div class="manual-tabs">
    <label for="switch-code-manual" class="manual-tab-label">🗺 <span class="manual-tab-text">Code Manual</span></label>
    <label for="switch-user-manual" class="manual-tab-label">📖 <span class="manual-tab-text">User Manual</span></label>
  </div>
  <div class="spacer"></div>
  __STAT_CHIPS__
  <input id="doc-search" type="search" placeholder="Search files…" aria-label="Search files">
</header>
<div class="layout" id="code-manual">
  <nav class="sidebar" aria-label="Project navigation">
    <ul class="quicknav">
      <li><a href="#overview">Project overview</a></li>
      <li><a href="#dependency-map">Dependency map</a></li>
    </ul>
    <div class="tree-eyebrow-row">
      <div class="tree-eyebrow">Project files</div>
      <button type="button" id="tree-toggle-all" class="tree-toggle-all">Collapse all</button>
    </div>
    __SIDEBAR_TREE__
  </nav>
  <div class="sidebar-backdrop" id="sidebar-backdrop"></div>
  <main class="content">
    __OVERVIEW__
    __DEPENDENCY_MAP__
    <h2 class="section-h">Files</h2>
    __FILE_SECTIONS__
  </main>
</div>
<div class="layout" id="user-manual">
  <nav class="sidebar" aria-label="User manual navigation">
    <div class="tree-eyebrow">On this page</div>
    __USER_MANUAL_NAV__
  </nav>
  <div class="sidebar-backdrop" id="user-manual-backdrop"></div>
  <main class="content">
    __USER_MANUAL_CONTENT__
  </main>
</div>
<footer class="doc-footer">
  Documentation generated automatically by doc_generator.py v__VERSION__ — static analysis,
  the project's code is never executed. Some conclusions (what a function is for, categorization)
  rely on heuristics and on comments in the source, and may be inaccurate.
</footer>
<script>__SCRIPTS__</script>
</body>
</html>
"""


def render_document(pdata: "ProjectData", project_title: str, plan: dict = None) -> str:
    plan = _normalize_plan(plan or {}, pdata)

    counts = pdata.stats["counts"]
    stat_chips = "".join(
        f'<span class="stat-chip">{v} {label}</span>'
        for label, v in [("HTML", counts["html"]), ("CSS", counts["css"]), ("JS", counts["js"])]
    )

    all_paths = set(pdata.html_files) | set(pdata.css_files) | set(pdata.js_files)
    linkable = {p for p in all_paths if plan["files"].get(p, {}).get("deep_analyze", 1)}

    file_sections = []
    for path in sorted(pdata.html_files):
        if path in linkable:
            file_sections.append(build_file_card_html(path, pdata.html_files[path], pdata.edges, all_paths, linkable))
    for path in sorted(pdata.css_files):
        if path in linkable:
            file_sections.append(build_file_card_css(path, pdata.css_files[path], pdata.edges, all_paths, linkable))
    for path in sorted(pdata.js_files):
        if path in linkable:
            file_sections.append(build_file_card_js(path, pdata.js_files[path], pdata.edges, all_paths, linkable))

    dependency_map_html = build_dependency_section(pdata) if plan["sections"]["dependency_graph"] else ""

    user_manual_nav, user_manual_content = build_user_manual(pdata, plan)
    show_code, show_user = plan["manuals"]["code_manual"], plan["manuals"]["user_manual"]
    manual_mode = "both" if (show_code and show_user) else ("code" if show_code else "user")
    if not show_user:
        user_manual_nav = user_manual_content = ""
    if not show_code:                       # nothing to render AND nothing left in the file
        file_sections, dependency_map_html = [], ""

    html = DOCUMENT_TEMPLATE
    html = html.replace("__TITLE__", esc(project_title))
    html = html.replace("__STYLES__", DOC_CSS)
    html = html.replace("__COMPASS__", COMPASS_SVG)
    html = html.replace("__PROJECT_NAME__", esc(project_title))
    html = html.replace("__GENERATED_AT__", esc(pdata.generated_at))
    html = html.replace("__STAT_CHIPS__", stat_chips)
    html = html.replace("__SIDEBAR_TREE__", build_sidebar_tree(pdata.tree, linkable) if show_code else "")
    html = html.replace("__OVERVIEW__", build_overview_section(pdata, plan) if show_code else "")
    html = html.replace("__DEPENDENCY_MAP__", dependency_map_html)
    html = html.replace("__FILE_SECTIONS__", "".join(file_sections))
    html = html.replace("__MANUAL_MODE__", manual_mode)
    html = html.replace("__USER_MANUAL_NAV__", user_manual_nav)
    html = html.replace("__USER_MANUAL_CONTENT__", user_manual_content)
    html = html.replace("__VERSION__", VERSION)
    html = html.replace("__SCRIPTS__", DOC_JS)
    return html


# --------------------------------------------------------------------------
# Orchestration: assembling the full ProjectData
# --------------------------------------------------------------------------

def build_project_data(root: Path, ignore_dirs: set, extra_ignore_globs: list) -> "ProjectData":
    tree, html_paths, css_paths, js_paths, other_paths = scan_project(root, ignore_dirs, extra_ignore_globs)

    html_files = {p: analyze_html(p, read_text_safe(root / p)) for p in html_paths}
    css_files = {p: analyze_css(p, read_text_safe(root / p)) for p in css_paths}
    js_files = {p: analyze_js(p, read_text_safe(root / p)) for p in js_paths}

    edges, used_tokens = build_edges(html_files, css_files, js_files)
    stats = analyze_project_stats(html_files, css_files, js_files, other_paths, edges, used_tokens)

    # docgen-h2: package.json is already scanned into other_paths (tiered
    # "config" by classify_importance) -- read it only if it sits at the
    # project root, matching where npm/node actually expect it, not any
    # nested package.json a dependency might carry.
    package_info = None
    if "package.json" in other_paths:
        try:
            package_info = analyze_package_json(read_text_safe(root / "package.json"))
        except OSError:
            package_info = None

    # docgen-h4: README.md/CHANGELOG.md, read once here (the only place
    # this call chain has filesystem access) so the User Manual's Overview
    # and Changelog sections can use the real text without re-opening the
    # project directory later at render time.
    readme_path = _find_root_file(other_paths, _README_NAMES)
    readme_raw = _read_optional(root, readme_path)
    changelog_path = _find_root_file(other_paths, _CHANGELOG_NAMES)
    changelog_raw = _read_optional(root, changelog_path)
    # docgen-h5: hand-written parts, if the project has a docgen-manual.md
    manual_path = _find_root_file(other_paths, _MANUAL_FILE_NAMES)
    manual_raw = _read_optional(root, manual_path)
    manual_md = parse_manual_md(manual_raw, manual_path) if manual_raw is not None else None

    return ProjectData(
        root_name=root.name,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        tree=tree,
        html_files=html_files,
        css_files=css_files,
        js_files=js_files,
        other_files=other_paths,
        edges=edges,
        stats=stats,
        package_info=package_info,
        readme_raw=readme_raw,
        readme_path=readme_path,
        changelog_raw=changelog_raw,
        changelog_path=changelog_path,
        manual_md=manual_md,
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="doc_generator.py",
        description="Generates a single HTML documentation file for a frontend project (HTML/CSS/JS).",
    )
    parser.add_argument("project_dir", help="Path to the root of the frontend project")
    parser.add_argument("-o", "--output", default="documentation.html",
                         help="Path to the output HTML file (default: documentation.html)")
    parser.add_argument("--title", default=None,
                         help="Project name shown in the documentation (default: the folder name)")
    parser.add_argument("--ignore", action="append", default=[],
                         help="Extra glob pattern to exclude files (can be given multiple times)")
    parser.add_argument("--no-default-ignore", action="store_true",
                         help="Do not exclude the standard tooling folders (node_modules, .git, etc.)")
    parser.add_argument("--plan-only", action="store_true",
                         help="Scan and analyze, write a generation-plan JSON, then stop -- no HTML is "
                              "written. Review/edit the plan, then rerun with --from-plan.")
    parser.add_argument("--manual-scaffold", action="store_true",
                         help="Write a starter docgen-manual.md into the project root (the file where you write "
                              "the User Manual parts the tool cannot know), then stop. Never overwrites an "
                              "existing file.")
    parser.add_argument("--plan-output", default=None,
                         help="Path for --plan-only's JSON (default: <output> with .html replaced by .plan.json)")
    parser.add_argument("--from-plan", default=None, metavar="PLAN_JSON",
                         help="Render using a (possibly hand-edited) generation-plan JSON from a previous "
                              "--plan-only run, instead of the all-sections-on default.")
    args = parser.parse_args(argv)

    root = Path(args.project_dir).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        return 1

    ignore_dirs = set() if args.no_default_ignore else set(DEFAULT_IGNORE_DIRS)
    project_title = args.title or root.name

    print(f"Scanning {root} …")
    pdata = build_project_data(root, ignore_dirs, args.ignore)
    counts = pdata.stats["counts"]
    print(f"Found: {counts['html']} HTML, {counts['css']} CSS, {counts['js']} JS, "
          f"{counts['other']} other files.")

    if pdata.manual_md and pdata.manual_md["unknown"]:
        print(f"Warning: {pdata.manual_md['path']} has heading(s) matching no User Manual section "
              f"(ignored): {', '.join(pdata.manual_md['unknown'])}", file=sys.stderr)

    if args.manual_scaffold:
        target = root / "docgen-manual.md"
        if pdata.manual_md is not None or target.exists():
            print(f"Error: {target.name} already exists -- not overwriting hand-written content.",
                  file=sys.stderr)
            return 1
        try:
            with open(target, "x", encoding="utf-8") as fh:      # "x": atomic no-clobber
                fh.write(build_manual_scaffold(pdata))
        except FileExistsError:
            print(f"Error: {target.name} already exists -- not overwriting hand-written content.",
                  file=sys.stderr)
            return 1
        print(f"Scaffold written: {target}")
        print("Fill in the sections only you can write, then rerun without --manual-scaffold.")
        return 0

    if args.plan_only:
        plan = derive_generation_plan(pdata, project_title)
        plan_path = Path(args.plan_output) if args.plan_output else \
            Path(args.output).with_suffix("").with_suffix(".plan.json") if args.output.endswith(".html") \
            else Path(str(args.output) + ".plan.json")
        save_plan(plan, plan_path)
        print(f"Plan written: {plan_path.resolve()}")
        print("Nothing was rendered. Edit any 1/0 flag, then rerun with --from-plan "
              f"{plan_path.name} -o {args.output}.")
        return 0

    plan = None
    if args.from_plan:
        plan_path = Path(args.from_plan)
        if not plan_path.is_file():
            print(f"Error: plan file not found: {plan_path}", file=sys.stderr)
            return 1
        try:
            plan = load_plan(plan_path)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error: couldn't read plan file ({e}) -- rendering with all sections on instead.",
                  file=sys.stderr)
            plan = None

    print("Building documentation …")
    html = render_document(pdata, project_title, plan)

    out_path = Path(args.output).resolve()
    out_path.write_text(html, encoding="utf-8")
    print(f"Done: {out_path} ({human_size(len(html.encode('utf-8')))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
