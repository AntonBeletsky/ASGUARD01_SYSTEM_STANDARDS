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

## Footer

A one-line disclaimer that generation is static analysis with no code
execution, and that some conclusions rely on heuristics/comments and may
be inaccurate — worth echoing to a user in your own words rather than
letting them assume the tool ran or tested the code.
