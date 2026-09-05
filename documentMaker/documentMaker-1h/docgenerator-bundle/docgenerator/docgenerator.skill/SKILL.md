---
name: docgenerator
description: Generates comprehensive, offline-readable documentation for frontend (HTML/CSS/JS) projects by scanning the directory tree, parsing every HTML/CSS/JS file, and mapping structural links (stylesheets, scripts, @import, import/require) and semantic DOM links (which JS/CSS touches which HTML elements) into one self-contained HTML file with a searchable file tree, dependency graph, and per-file code + structure breakdown. Use whenever the user wants to document, explain, map, summarize, or get an overview/reference for a website, web app, static site, or HTML/CSS/JS codebase — including "document this project", "explain how this codebase is structured", "generate a project overview", "map the dependencies here", "what does this frontend project do", or "onboard me to this repo" — even without the word "documentation", and even for a conversational walkthrough with no file wanted. Also useful to audit a frontend project for unused CSS, orphaned selectors, missing alt text, or broken links.
---

# Frontend Project Documentation Generator

## Overview

This skill turns a folder of HTML/CSS/JS into either a browsable HTML
reference document or a spoken walkthrough — backed by the same static
analysis either way. It bundles a working, tested Python script
(`scripts/doc_generator.py`) that does the actual parsing and
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
`references/limitations.md` before promising results.

## Running it

```bash
python3 scripts/doc_generator.py <project_dir> -o <output_path>.html --title "<Project Name>"
```

Resolve `scripts/doc_generator.py` relative to this SKILL.md's own
location (wherever this skill is mounted). Useful flags:

- `--title "..."` — set a human-readable title instead of the folder name
- `--ignore "<glob>"` — exclude extra files, repeatable
- `--no-default-ignore` — include node_modules/.git/dist/vendor/etc. (rarely wanted)

Full flag reference and internals: `references/architecture.md`.

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
files. See `references/output-guide.md` for what each section/field means
so you can translate it into plain language for the user.

## Setting expectations honestly

This is static heuristic analysis, not a compiler and not a live browser.
It will occasionally miss something or flag a false positive (e.g. a CSS
class that's actually added by JS at runtime and looks "unused" here). When
you relay findings — especially the "Cartographer's notes" warnings
(unused id/class, orphaned CSS selectors, broken links) — phrase them as
"the analysis flags X, worth double-checking" rather than as certain fact.
The full list of known blind spots is in `references/limitations.md`;
skim it before telling a user something is definitely dead code or
definitely broken.

## Mode C — plan first on a large or unusual project

For a large project, or one where you can already tell a specific
diagnostic is likely to be noisy for this codebase (heavily dynamic DOM,
a vendored/minified file that slipped past the minification heuristic,
a single-file-per-type project where the dependency graph will be
near-trivial), run `--plan-only` before the normal full run:

```bash
python3 scripts/doc_generator.py <project_dir> -o <output>.html --plan-only
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

## Reference files

Read these as needed — they're not preloaded, and most single requests
won't need all four:

- `references/architecture.md` — the parsing pipeline, data model, and
  cross-referencing logic in depth. Read this if the user asks how the
  tool works, wants a change to the analysis logic, or you need to import
  its functions directly for Mode B.
- `references/output-guide.md` — what every section, badge, and tab in the
  generated HTML actually means. Read this before summarizing output to a
  user, so your description is accurate rather than guessed from the UI.
- `references/limitations.md` — known blind spots and how to talk about
  them. Read this before asserting something is broken/unused/missing, and
  before taking on a project type (framework components, TypeScript, CSS-in-JS)
  this tool wasn't built for.
- `references/customization.md` — how to adjust the visual theme, add
  ignore patterns, or extend a parser. Read this only if the user
  explicitly asks for a modified version of the tool or generator theme.
