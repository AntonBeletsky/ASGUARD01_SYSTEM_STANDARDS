# docgenerator

**Turn a folder of HTML/CSS/JS into a single, browsable, offline HTML
reference — automatically.** Point it at a frontend project and get back
one self-contained file with a searchable directory map, a dependency
graph that shows how the files actually connect (not just which files
reference which, but which JS/CSS reaches into which HTML elements), and
a syntax-highlighted, structurally-parsed breakdown of every file.

This repository is **two independently-usable projects sharing one
engine**: a plain command-line script for people, and a Claude Agent Skill
wrapping that same script for LLM agents. Both are complete, working code.

```
docgenerator/
├── README.md                  ← this file
├── doc-generator-cli/          Project 1 — run it yourself, by hand
└── docgenerator.skill/         Project 2 — an LLM agent runs it for you
```

## Contents

- [Which project do you want?](#which-project-do-you-want)
- [Quick start](#quick-start)
- [What it produces](#what-it-produces)
- [Design research: how existing documentation systems informed this](#design-research-how-existing-documentation-systems-informed-this)
- [Why it looks the way it does](#why-it-looks-the-way-it-does)
- [Architecture](#architecture)
- [Known limitations](#known-limitations)
- [Project status](#project-status)
- [Full file listing](#full-file-listing)
- [Roadmap: what's worth building next](#roadmap-whats-worth-building-next)

## Which project do you want?

| | `doc-generator-cli/` | `docgenerator.skill/` |
|---|---|---|
| **What it is** | A plain Python script | A Claude Agent Skill |
| **Who runs it** | You, from a terminal | An LLM agent, autonomously, as part of helping with a broader task |
| **How you use it** | `python3 doc_generator.py ...` | Ask an agent to document/explain a frontend project in plain language |
| **Requires** | Python 3.9+, nothing else | An agent harness that loads Agent Skills |
| **Can it just answer questions instead of making a file?** | No — it only ever writes a file | Yes — the skill can use the same analysis conversationally, with no file produced, when that's what's actually useful |
| **Start here** | [`doc-generator-cli/README.md`](doc-generator-cli/README.md) | [`docgenerator.skill/SKILL.md`](docgenerator.skill/SKILL.md) |

Both run the *exact same* `doc_generator.py` — same file, same logic, same
output. `docgenerator.skill/scripts/doc_generator.py` is a synced copy,
kept manually in sync with the canonical copy in `doc-generator-cli/` (see
"Keeping this in sync" in `docgenerator.skill/README.md`).

## Quick start

**As a script**, from anywhere with Python 3.9+:

```bash
cd doc-generator-cli
python3 doc_generator.py /path/to/your/project -o documentation.html --title "My Project"
```

Or try it on the bundled demo first, with no setup:

```bash
python3 doc_generator.py examples/sample-project -o /tmp/demo.html
open /tmp/demo.html
```

**As a skill**, install `docgenerator.skill/` (or the packaged
`docgenerator.skill.skill` archive, if one was built — see "Project
status") wherever your Claude setup loads Agent Skills from, then just ask
in plain language: *"document this project,"* *"explain how this codebase
is structured,"* *"what does this frontend app do,"* or *"help this
contractor get oriented in our repo."* The skill decides on its own when
to use the tool — there's no separate activation step.

## What it produces

- **A directory map** — the full project tree, collapsible, in a sidebar.
- **A project overview** — file counts by type, total lines of code and
  size, the project's actual color palette (collected from every color
  value used in the CSS, ranked by frequency — not a curated brand
  palette, a *usage* palette), responsive breakpoints in use, and any
  external libraries/CDNs detected.
- **A dependency graph** — an SVG with HTML/CSS/JS files as nodes in three
  columns. Solid lines are structural references (stylesheet/script tags,
  `@import`, `import`/`require`, page-to-page links). Dashed lines are
  something most tools don't compute at all: *semantic* links, found by
  cross-checking every literal `#id`/`.class` a JS file queries or a CSS
  rule targets against a project-wide registry of what's actually declared
  in the HTML. A CSS rule targeting `.hero-title` and an HTML element with
  `class="hero-title"` get linked even though neither file mentions the
  other's name or path.
- **A card per file**, with "Code" (syntax-highlighted, done in Python at
  generation time — no client-side highlighting library needed) and
  "Structure" tabs:
  - **HTML** — title/lang/description, the full h1–h6 heading outline,
    semantic landmark tags, forms and their fields, images (flagged if
    missing `alt`), every `id`/`class` on the page, markup comments.
  - **CSS** — custom properties with a color-swatch preview, media
    breakpoints, `@font-face`/`@keyframes`/`@supports`, and a living list
    of every rule showing its selector, its author's leading comment if it
    had one, and its declarations — a direct implementation of the
    [KSS](https://github.com/kss-node/kss-node) convention where a comment
    above a selector *is* that component's documentation.
  - **JS** — imports/exports (ES modules and CommonJS), every function and
    class with its parsed JSDoc (description, `@param`, `@returns`,
    `@example`), DOM access, event listeners, network calls, TODO/FIXME.
- **"Cartographer's notes"** — automatically-flagged issues: `id`/`class`
  declared in HTML but never matched by any CSS selector or JS query;
  CSS selectors with no matching HTML anywhere in the project; broken
  internal links; images without `alt`. Flagged as things *worth
  checking*, not certainties — see "Known limitations."

Everything ships in **one `.html` file**. No build step, no server, no
internet connection needed to read it — open it straight from disk, even
years later, even on a machine that no longer has the original project
installed.

## Design research: how existing documentation systems informed this

Before writing any code, this project's documentation *template* (as
distinct from the analysis engine) was designed by looking at how existing
systems structure technical documentation — deliberately spanning both
"produced by a company for a language/platform" and "produced by
individuals for code they wrote":

- **MDN Web Docs** doesn't use one template for everything — it has a
  catalog of page types, each with its own structure. A CSS reference page
  opens by naming the module and its purpose, gives an overview of
  capabilities, then a live example demonstrating it. An HTML element page
  gives a summary paragraph, worked examples, and an interactive "Try it"
  block. Every reference page carries a standardized browser-compatibility
  table and a "See also" cross-link section. Navigation across the whole
  site is generated from one shared data structure, not hand-written per
  page.
- **Microsoft Learn / MSDN** formalizes this further with explicit content
  *types* — conceptual, how-to, tutorial, reference, quickstart — each
  with its own expected shape. Notably, Microsoft's own style guidance
  warns that when reference docs are auto-generated from source comments,
  someone still has to review comment quality, because developers
  routinely omit what a reader actually needs — the exact caveat this
  project's own `references/limitations.md` makes about its own output.
- **Template marketplaces (ThemeForest/Envato and similar)** treat
  documentation as a purchase requirement, not an afterthought: every item
  needs install/customization/usage instructions, and — closest to this
  project's own approach — a documented breakdown of the file/folder
  structure, ideally with screenshots. That's directly where the "explain
  the directory tree, not just the code" requirement in this project came
  from.
- **JSDoc, Storybook, and KSS** are the closest relatives to what this
  tool actually does: all three generate documentation *from* the same
  source that ships, instead of maintaining it by hand somewhere else.
  JSDoc turns `@param`/`@returns`/`@example` comments into a browsable
  reference. Storybook's Autodocs statically analyzes a component's source
  to build a live preview plus a props table with no manual documentation
  step. KSS reads a leading CSS comment as a component's own description,
  organized into a numbered "living style guide" that's part of the actual
  running application rather than a separate document that drifts out of
  sync.

**The pattern that recurs across every one of these, at the level of a
single documented unit, is the same triad**: a live/rendered example, the
underlying code or syntax, and a plain-language explanation — wrapped in
predictable navigation and a consistent section taxonomy so a reader never
has to re-learn the page's shape. That triad is exactly what a file card
in this generator's output does: a "Code" tab (the syntax), a "Structure"
tab (the parsed, explained facts), and — unlike any single one of the
systems above — a computed "Depends on / Used in" relationship section,
because for a whole *project* (rather than one language or one component
library) the connections between files are as much a part of understanding
it as any individual file's content.

## Why it looks the way it does

The visual design is a deliberate "atlas/blueprint" theme — a deep-ink
header, cool "drafting paper" as the reading surface, and copper/verdigris/
gold as the three legend colors for HTML/CSS/JS, used consistently in the
file tree, the badges, and the dependency-graph nodes. This wasn't an
arbitrary skin: the generator's job is literally to produce a *map* of a
codebase, so the visual language leans into cartography rather than
imitating a generic SaaS-docs template. The dependency graph is drawn like
a transit map — files as stations, links as routes.

Two more decisions worth calling out because they're easy to miss just
from using the output:

- **Progressive enhancement, almost everywhere.** The folder tree
  collapses via native `<details>/<summary>` — no JavaScript. Tab
  switching between "Code" and "Structure" uses a `radio` + `:checked ~`
  CSS trick — no JavaScript. Smooth scrolling is `scroll-behavior: smooth`
  — no JavaScript. The only real client-side JS handles things that
  genuinely need a running page: live search-as-you-type, scrollspy
  (`IntersectionObserver`), and the copy-code button. If a browser's JS
  fails or is disabled, the document is still fully readable.
- **Offline-first as a hard constraint, not a nice-to-have.** No CDN
  fonts, no CDN highlighting library. Syntax highlighting is computed once
  in Python at generation time and baked into the HTML as `<span>` tags.
  Fonts are system stacks chosen for character, not generic sans-serif
  defaults, but never loaded over a network. The whole point of "one
  self-contained file" is that it should still open five years from now
  on a machine with no internet access — every dependency choice was
  filtered through that constraint.

## Architecture

```
scan_project()            → directory tree + html/css/js path lists
  → analyze_html/css/js()  → one typed *Info object per file
    → build_edges()        → structural + semantic links between files
      → analyze_project_stats() → aggregated project-wide statistics
        → render_document()      → one HTML string
```

Every file is parsed **exactly once** into a dataclass (`HtmlInfo`,
`CssInfo`, or `JsInfo`); that object is the single source of truth for the
code display, the dependency graph, and the statistics alike — there's no
second pass over file contents anywhere in the pipeline.

- **HTML** is parsed with Python's standard-library `html.parser` — no
  external HTML library needed.
- **CSS** has no standard-library parser in Python, so this project
  includes a hand-written single-pass, brace-balancing tokenizer that also
  implements the KSS "leading comment documents this rule" convention
  directly.
- **JS** is parsed heuristically — masking out comments and template
  literals, then running targeted regexes over what's left — deliberately
  *not* a full AST parser. That's a considered trade-off, not an
  oversight: it keeps the tool dependency-free and instantly runnable
  anywhere with just Python, at the cost of missing some edge cases a real
  parser (Acorn/Babel/the TypeScript compiler) would catch. See
  `docgenerator.skill/references/architecture.md` for the full reasoning
  and `references/customization.md` for how to swap in a real parser.
- The output document itself is a Python string template with
  `__PLACEHOLDER__` tokens filled by plain `.replace()` calls —
  deliberately not Jinja2 or f-strings, since both would collide with the
  literal `{`/`}` characters in the embedded CSS/JS.

Full internals, function-by-function, are in
`docgenerator.skill/references/architecture.md` — written for an LLM
agent to consult, but equally useful for a human maintaining the script.

## Known limitations

This is **static, heuristic analysis** — not a compiler, not a browser,
and it never executes the project's own code.

- JS parsing is regex-based; it can miss unusual syntax and can't resolve
  a selector passed as a variable (`querySelector(x)`) — only literal
  strings are seen.
- Minified files are detected heuristically and skipped from detailed
  analysis on purpose, rather than dumping unreadable output.
- The CSS parser handles the common cases correctly but isn't a full
  implementation of the CSS grammar (e.g. exotic selector nesting).
- "Unused id/class" and "orphaned selector" notes are the most likely
  false positives, because they require proving an *absence* across a
  static scan — a class added dynamically by JS, a CMS, or a framework
  directive is invisible to this tool by construction.
- React/Vue/Svelte components, TypeScript, Tailwind-style utility CSS, and
  CSS-in-JS are all explicitly out of scope for v1 — see
  `docgenerator.skill/references/limitations.md` for exactly what breaks
  and why, and what a partial result still looks like for each.

## Project status

Both projects are complete, working code — not placeholders.

- **`doc-generator-cli/`** has been run end-to-end and its output visually
  verified across several iterations, including a full English
  localization pass (script, generated UI strings, CLI help text, and the
  bundled demo project are all English).
- **`docgenerator.skill/`** passes the real `skill-creator` validator
  (`quick_validate.py` → `Skill is valid!`) and has been packaged into an
  actual distributable `docgenerator.skill.skill` archive via
  `package_skill.py` — the validation pass caught and fixed two genuine
  spec violations along the way (angle brackets in the frontmatter
  description; the description exceeding the 1024-character limit).
  Its `evals/evals.json` test prompts have been traced manually against
  the shipped instructions rather than run through the automated,
  subagent-based eval loop — that loop needs a `claude` CLI with live API
  access, which wasn't available in the environment this was built in. The
  manual trace (`docgenerator.skill/evals/manual-trace-results.md`) is
  explicit about that gap, including one specific, unconfirmed weak point
  it found rather than smoothing it over.

## Full file listing

```
docgenerator/
├── README.md                              this file
│
├── doc-generator-cli/                     Project 1 — standalone script
│   ├── README.md                          usage, CLI flags, architecture, limitations
│   ├── doc_generator.py                   the generator (stdlib only)
│   └── examples/
│       ├── example-documentation.html     pre-generated output, ready to open
│       └── sample-project/                the "Skylark" demo frontend project
│           ├── index.html
│           ├── about.html
│           ├── css/
│           │   ├── style.css
│           │   └── vars.css
│           └── js/
│               ├── app.js
│               └── utils.js
│
└── docgenerator.skill/                    Project 2 — Claude Agent Skill
    ├── README.md                          human-facing pointer + validation/packaging status
    ├── SKILL.md                           the skill: frontmatter + agent instructions
    ├── scripts/
    │   └── doc_generator.py               synced copy — the skill is self-contained
    ├── references/                        loaded by the agent only when actually needed
    │   ├── architecture.md                pipeline, data model, cross-referencing, in depth
    │   ├── output-guide.md                what every section/badge/tab in the output means
    │   ├── limitations.md                 known blind spots, and how to talk about them honestly
    │   └── customization.md               how to retheme, extend parsers, add diagnostics
    └── evals/
        ├── evals.json                     5 draft functional test prompts
        └── manual-trace-results.md        instruction-trace results (not an automated run)
```

(A packaged `docgenerator.skill.skill` archive — everything above except
`evals/`, per that folder's own packaging exclusion rules — is also
provided alongside this bundle when one has been built.)

## Roadmap: what's worth building next

Roughly in order of value versus effort:

1. **A real JS parser.** Swapping the regex-based `analyze_js()` for an
   actual AST — via a Node.js subprocess running Acorn/Espree, or the
   TypeScript compiler API — would remove nearly every parsing limitation
   in one move, and open the door to real TypeScript and JSX support.
   Biggest single improvement available.
2. **Framework-component awareness.** Vue single-file components split
   cleanly into existing HTML/JS/CSS analysis with a bit of preprocessing;
   real React/JSX prop/hook analysis needs the AST work above first.
3. **Real accessibility and coverage auditing.** Today's checks (missing
   `alt`, orphaned selectors) are heuristics. A headless-browser pass
   (Playwright/Chromium) would enable genuine contrast checking, ARIA
   auditing, and real "unused CSS" detection via the browser's own
   Coverage API instead of static guessing.
4. **Modern CSS paradigms.** Utility-first CSS (Tailwind), CSS Modules,
   and CSS-in-JS all break the "one meaningful rule, one selector" model
   the current CSS parser assumes, and would each need their own analysis
   approach.
5. **Documentation infrastructure.** Versioning/diffing between
   generation runs, git-blame-based authorship per file, CI/CD
   auto-publishing, and full-text search over parsed functions/comments
   (today's search is filename-only).
6. **Design-token export.** The color-palette and custom-property
   extraction already collected is most of the way to a real [W3C Design
   Tokens](https://design-tokens.github.io/community-group/format/)
   export — currently just displayed, not exported in a reusable format.
7. **Optional LLM-assisted summaries.** Static analysis explains
   *structure* reliably; it can't always explain *intent* when the source
   has no comments. An opt-in step that asks an LLM (with the user's own
   API key) for a one-paragraph natural-language file summary would close
   that gap — the one place in this whole design where breaking the
   offline-only constraint would be a deliberate, clearly-flagged trade-off,
   not a default.
