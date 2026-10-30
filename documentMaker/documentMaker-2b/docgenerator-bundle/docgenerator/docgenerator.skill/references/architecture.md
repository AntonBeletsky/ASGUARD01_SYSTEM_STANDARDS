# Architecture reference

Deep-dive on how `scripts/doc_generator.py` works internally. Read this
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
sys.path.insert(0, "<this skill's scripts/ directory>")
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
