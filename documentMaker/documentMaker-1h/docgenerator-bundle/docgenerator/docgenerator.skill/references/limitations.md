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

## What to do when you hit one of these

Don't silently work around a limitation by inventing an answer from
general knowledge instead of the tool's actual output — say plainly what
the tool could and couldn't determine, and offer to look at the specific
file by hand (reading the source directly) if the user needs certainty on
a point the static analysis is weak on. For framework-heavy or TypeScript
projects, it's fine to still run the tool for the parts it *can* see
(plain CSS files, any vanilla JS, the overall file tree) while being clear
that the component-level story is missing.
