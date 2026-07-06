# AI Task Execution Methodology — Catalog Driver
## Extending Task Execution to Path-Addressed, Directory-Scoped Work

---

## Purpose and Relationship to the Base Methodology

**Prerequisite:** this document assumes the base methodology (`ai-task-execution-methodology.md`) — its Philosophy and Phases 0–5 — is already known. It is not repeated here.

The base methodology assumes the working set is **known and flat**: a short, named list of files, small enough to load into context at once, addressed internally by line numbers alone. That assumption holds for widget-level refactors, single-module audits, and anything where a human has already told the AI exactly which files matter.

It stops holding the moment a task is phrased as *"go through the `src/` catalog,"* *"audit this repository,"* or *"find every place this pattern occurs in the project."* Here the working set is not given — it must be **discovered**; it can be **arbitrarily large and deep**; and a bare line number, or a bare filename, stops meaning anything the instant more than one file in the tree could contain it.

This document is a **driver**: it does not replace the base methodology's philosophy, phases, or artifacts — it plugs into them, changing how each phase behaves when the input is a **catalog** (a directory tree) instead of an enumerated file list. Everywhere this document is silent, the base methodology applies unchanged.

Everything below is language- and stack-agnostic. The catalog might be a JavaScript monorepo, a Python package, a documentation site, or a mixed-language repository — the mechanics of discovery, addressing, and validation are the same regardless of what's inside the files.

---

## Terminology

| Term | Meaning in this document |
|---|---|
| **Catalog** | A root directory and everything nested beneath it — subdirectories and files, to arbitrary depth. What other conventions call a "directory tree" or "folder tree." |
| **Catalog root** | The single declared top-level directory that every path in the task is made relative to. A task may declare more than one root (e.g. a monorepo with independent packages), but each root is explicit, never assumed. |
| **Path** | The address of a file or directory relative to a catalog root, using forward slashes — e.g. `src/components/widget/index.js`. |
| **Manifest** | The structured inventory produced by scanning a catalog: a tree view and a flat list of every in-scope path, with metadata, built *before* any file content is read. |

---

## The Core Shift: What Changes When the Scope Is a Catalog

| Dimension | Base methodology (flat file set) | Catalog-driven reality |
|---|---|---|
| Scope discovery | Files are named upfront by the user | Files are found by scanning; scope isn't known until the scan completes |
| File identity | "the file" — obvious, singular | Many files can share a name; identity requires a full path |
| Location addressing | line numbers inside an implicit current file | path + line numbers; the path is mandatory, never implicit |
| Size | A handful of files, all fit in context | Trees can hold thousands of files; not all of it can be loaded at once |
| Structure | Flat list | A hierarchical tree of arbitrary nesting depth |
| Grouping unit (Phase 3) | one file = one group | file, directory, module, or package — granularity has to be chosen |
| Cross-file references | within a small, known set — easy to eyeball | may span distant branches of the tree; needs an explicit path anchor |
| Validation | pattern search across a known handful of files | pattern search across the *entire* catalog, including untouched files |
| Change types | RENAME/DELETE/REPLACE/ADD/MOVE act on content | a file itself can be relocated to a new path — a distinct operation |
| Noise sources | none — files are pre-selected as relevant | build artifacts, dependencies, binaries, generated code, VCS metadata |

---

## Philosophy Extension — Path Is the Unit of Identity

The base methodology's philosophy is a strict pipeline: `ANALYSIS → PLAN → EXECUTION`. Catalog-driven work adds one rule underneath all three stages, as inviolable as the pipeline itself:

```
NO LOCATION WITHOUT A PATH
```

A line number, a code fragment, or a dependency reference means nothing on its own once more than one file in scope could contain it. Every artifact this driver produces — manifest, map, plan, report — names the path before it names anything found inside that path.

This rule is stated first because the rest of this document exists to make it practical to follow: how paths are discovered (Phase 0), how they're recorded (Phase 2), how they're grouped (Phase 3), acted on in order (Phase 4), and verified (Phase 5).

---

## Workflow Structure — Catalog Extensions

Each section below is a delta against the matching phase in the base methodology. Where a mechanic isn't mentioned, it carries over unchanged.

### Phase 0 Extension — Catalog Discovery

In the base methodology, Phase 0 assumes the file list is already known — its only job is to load and confirm named materials. When the scope is a catalog, Phase 0 gains a discovery step that must complete *before* that rule applies. Nothing gets done here either — only walking the tree and confirming what was found.

#### 0.1 Declare the Catalog Root(s)

```
Bad:  "look through the code and fix the naming"
Good: "catalog root: /src — analyze everything under it"
```

Every path in every later artifact — map, plan, report — is written relative to this root. If a task spans more than one root (e.g. `/frontend` and `/backend`), each root gets its own manifest and its own root-relative paths; they are never silently merged into one ambiguous set.

#### 0.2 Define Scan Parameters

```
include:            ["**/*.js", "**/*.ts", "**/*.html", "**/*.css"]
exclude:             ["node_modules/**", ".git/**", "dist/**", "build/**", "vendor/**", "**/*.min.*"]
depth_limit:         none
size_threshold_kb:   500     # files above this are flagged, not auto-loaded in full
follow_symlinks:     false
include_hidden:      false
```

Why the exclude list matters: without it, the first scan of a real project pulls in tens of thousands of lines of dependency code, compiled output, and lockfiles — pure noise that can exhaust the context budget before Phase 1 even starts.

#### 0.3 Walk the Tree, Build the Manifest

Traversal must be deterministic — depth-first, alphabetical within each directory — so two scans of an unchanged catalog produce an identical manifest. That's what makes the manifest trustworthy as a reference point for every later phase.

The manifest has two views: a nested tree (the overall shape, at a glance) and a flat list (what every later phase actually iterates over).

```json
{
  "meta": {
    "catalog_root": "/src",
    "scanned_at": "2026-07-06T00:00:00Z",
    "scan_params": {
      "include": ["**/*.js", "**/*.html", "**/*.css"],
      "exclude": ["node_modules/**", ".git/**", "dist/**"]
    },
    "totals": { "directories": 38, "files": 214, "lines": 42318 }
  },
  "tree": {
    "components": { "widget": ["index.js", "styles.css", "widget.html"] },
    "utils": ["date.js", "format.js"]
  },
  "files": [
    { "path": "components/widget/index.js", "size_bytes": 4210, "lines": 187, "ext": "js" },
    { "path": "components/widget/widget.html", "size_bytes": 3050, "lines": 96, "ext": "html" },
    { "path": "utils/date.js", "size_bytes": 1104, "lines": 42, "ext": "js" }
  ]
}
```

#### 0.4 Confirm the Manifest — Nothing Else Happens Yet

Same rule as the base Phase 0, applied to the manifest instead of a named file list:

```
User: scan /src, do nothing else
AI:   [walks the tree] → "Catalog scanned: 214 files across 38 directories,
       42,318 lines. 6 files exceeded the size threshold and were
       flagged, not loaded. Manifest ready ✓"
```

Why it matters, one level up from the base doc's reasoning: if the manifest is wrong — a folder silently excluded, a symlink loop inflating the count, an exclude pattern too aggressive — every phase built on top of it inherits the error, and it surfaces as "missing files" much later, when it's expensive to trace back.

---

### Phase 1 Extension — Analysis at Catalog Scale

The base doc's Phase 1.2 — "sequential pass: file × category, no skipping ahead" — assumes opening every file is free. At catalog scale it isn't: most paths in a large tree are irrelevant to any given violation category, and opening all of them exhausts the context budget before the pass that matters even starts.

1. Tier 1 (the manifest, already built in Phase 0) is the full candidate list for this pass.
2. Use cheap signals — extension, directory, filename pattern, a fast pre-search across the flat file list — to shortlist candidates for a closer look.
3. Run the file × category matrix only across the shortlist, batched by directory or module:

```
Bad:  attempt file × category across all 214 files in a single pass
Good: components/  → file × category pass → confirm
      utils/       → file × category pass → confirm
      features/    → file × category pass → confirm
      ...
```

4. Record both counts in `meta`: `manifest_totals.files` (everything discovered) and `analyzed_files` (everything actually opened in full) — see the tiered loading model under *Working with Large Catalogs*, below.

This mirrors the base doc's "Working with Large Files" guidance one level up: the unit too large for one pass is no longer a single file, it's the whole catalog, and the logical passes are directories or modules instead of CSS/HTML/JS layers.

---

### Phase 2 Extension — Task Map Schema

In the base methodology, `location.lines` is enough because the file is never in question — it was named back in Phase 0. In catalog-driven work, the file is exactly what's in question, so path is promoted from optional context to a mandatory field, and it always comes before the line number:

```
Base doc addressing:       lines 165–166
Catalog-driven addressing: components/widget/index.js : lines 165–166
```

#### Path Normalization Rules

- Always relative to the declared catalog root — never an absolute filesystem path, which breaks the moment the catalog is checked out somewhere else.
- Forward slashes only, regardless of the host OS.
- No leading `./`, no trailing slash.
- Case preserved exactly as it appears on disk. On case-insensitive-but-preserving filesystems (default macOS, Windows), `Widget.html` and `widget.html` can point to the *same* file even though they look like two different paths — flag this rather than silently treating them as distinct.

#### The Basename Collision Problem

The base methodology's domino references already carry a `file` field for cross-file dependencies:

```json
"dependencies": [
  { "issue_id": "widget-002", "file": "widget.html", "description": "..." }
]
```

That works when there are five files, each with a unique name. It silently breaks in a catalog, where `index.js`, `styles.css`, and `README.md` routinely exist dozens of times across different directories. A dependency that says `"file": "index.js"` in a 200-file catalog isn't a reference — it's a guess.

```
Bad:  "dependencies": [{"issue_id": "app-045", "file": "index.js"}]
      → which of the 14 index.js files in the catalog is this?

Good: "dependencies": [{"issue_id": "app-045",
                         "path": "features/checkout/index.js"}]
```

**Rule: every `file` field in the base schema becomes a `path` field, and it is always a full, root-relative path — never a bare filename.**

#### Extended Map Structure

```json
{
  "meta": {
    "total_issues": 112,
    "guide_version": "containerization-6",
    "catalog_root": "/src",
    "manifest_totals": { "directories": 38, "files": 214 },
    "analyzed_files": 187
  },
  "paths": [
    {
      "path": "features/checkout/summary.js",
      "issues": [
        {
          "id": "checkout-014",
          "category": "CSS_PREFIX",
          "severity": "HIGH",
          "change_type": "RENAME",
          "location": {
            "lines": { "start": 42, "end": 42 },
            "context": "className: 'msg-total-row'"
          },
          "current": "msg-total-row",
          "expected": "messages-total-row",
          "dependencies": [
            {
              "issue_id": "checkout-015",
              "path": "shared/styles/checkout.css",
              "description": "line 118: .msg-total-row rule, token consumer in a different directory"
            }
          ],
          "status": "pending"
        }
      ]
    },
    {
      "path": "features/checkout/legacy-summary.js",
      "issues": [
        {
          "id": "checkout-020",
          "category": "FILE_LOCATION",
          "severity": "MEDIUM",
          "change_type": "RELOCATE",
          "location": { "path": "features/checkout/legacy-summary.js" },
          "expected_path": "features/checkout/archive/legacy-summary.js",
          "dependencies": [
            {
              "issue_id": "checkout-021",
              "path": "features/checkout/index.js",
              "description": "line 3: import path must be updated after relocation"
            }
          ],
          "status": "pending"
        }
      ]
    }
  ]
}
```

#### Schema Changes at a Glance

| Field | Base methodology | Catalog extension |
|---|---|---|
| Top-level grouping key | `files`, grouped by `file` | `paths`, grouped by `path` |
| `file` | bare filename, assumed unique | replaced everywhere by `path`, always root-relative |
| `dependencies[].file` | bare filename | `dependencies[].path` — full root-relative path, mandatory |
| `meta` | guide version, issue count | adds `catalog_root`, `manifest_totals`, `analyzed_files` |
| `change_type` | RENAME / DELETE / REPLACE / ADD / MOVE | adds **RELOCATE** — moving a whole file to a new path |
| `location` | always `lines` + `context` | for RELOCATE, may hold only `path`; destination goes in `expected_path` |

#### RELOCATE: A New Change Type

The base doc's `MOVE` already means "relocate to a different place" — but in every base-doc example that's a rule, a block, a fragment moving *within files that are already known*. Relocating an entire file changes its **path** — the address every other file in the catalog may depend on through imports, links, or references. Conflating the two hides the fact that a RELOCATE issue almost always spawns a catalog-wide reference search (Phase 4 extension, below), while a content-level MOVE usually doesn't.

---

### Phase 3 Extension — Hierarchical Grouping

#### Grouping Granularity Rule

The base doc's rule — "one file = one group, one violation type = one subgroup" — assumes exactly two levels of grouping. A catalog usually needs more, and the right number depends on size.

```
Small catalog  (under ~15 files, fits in one working set):
  group by file, as in the base methodology — no change needed.

Medium catalog (dozens of files, a handful of directories):
  Directory (group) → File (subgroup) → Violation type → Issue

Large catalog / monorepo (hundreds of files, multiple packages):
  Package or top-level module (group) → Directory (subgroup)
    → File (sub-subgroup) → Violation type → Issue
```

Example at medium granularity:

```
features/checkout (directory)
  ├── summary.js (file)
  │   ├── CSS prefix (violation type)
  │   │   └── [ ] checkout-014 — msg-total-row → messages-total-row (domino: 1)
  │   └── dead ids (violation type)
  │       └── [ ] checkout-016 — id="msg-tip" unused
  └── legacy-summary.js (file)
      └── file location (violation type)
          └── [ ] checkout-020 — RELOCATE → archive/ (domino: 1)

shared/styles (directory)
  └── checkout.css (file)
      └── CSS prefix (violation type)
          └── [ ] checkout-015 — domino of checkout-014
```

#### Choosing Execution Boundaries Along Dependency Seams

A grouping boundary drawn at a fixed tree depth (e.g. "always group at depth 2") will regularly cut through a cluster of files that depend on each other, forcing constant cross-group domino jumps. Where the Phase 1.3 domino analysis is available, prefer boundaries that roughly align with it: files that mostly reference each other stay in one group; files with few or no cross-references to the rest of the catalog can be their own group even deep in the tree.

---

### Phase 4 Extension — Execution Order Across a Catalog

#### Principles

**1. Traversal is dependency-aware when possible, deterministic otherwise**

The base doc's "one file at a time" becomes "one path at a time" — but the *order* of paths now needs a rule, because a catalog rarely has one obvious reading order the way three named widget files do.

```
Dependency-aware order (preferred, when the domino graph from Phase 1.3
is known): process paths with no unresolved incoming dependencies first
— foundation/leaf modules — then move up toward paths that depend on them.

Deterministic structural order (fallback, when dependencies aren't
mapped or cross-file coupling is minimal): depth-first, alphabetical
within each directory — the same order the manifest itself was built
in, so the plan and the manifest never disagree about what comes next.
```

Severity is still the outer sort key either way, exactly as in the base methodology (CRITICAL → HIGH → MEDIUM → LOW) — the traversal strategy decides order *within* a severity band, across paths, the same role "more dominoes first" plays within a single file in the base doc.

**2. Cross-directory domino is resolved immediately, with the path stated explicitly**

The base doc's "domino is executed immediately, not parent-first-domino-later" is unchanged in spirit, but crossing directories raises the cost of losing track of where you are.

```
Now switching to shared/styles/checkout.css to complete the domino
from features/checkout/summary.js (checkout-014 → checkout-015).
```

Resolve the domino, then return to the original path. The excursion is not a new anchor, and it doesn't license picking up unrelated issues encountered along the way just because they happen to be on screen.

**3. RELOCATE always triggers a full-catalog reference search**

Because any path in the catalog could hold a reference to the file being moved — an import, a relative link, a config entry, a documentation mention — moving a file is never executed standalone:

```
1. Move features/checkout/legacy-summary.js
     → features/checkout/archive/legacy-summary.js
2. grep the ENTIRE manifest (not just features/checkout/) for
   "legacy-summary" and for the old relative import forms
3. Fix every match found — this is the domino, and it's mandatory,
   even for matches in directories nobody expected
4. Only then mark the RELOCATE issue done
```

---

### Phase 5 Extension — Validation at Catalog Scale

#### Validation Additions

**1. Full-manifest validation, not touched-files validation**

The base doc's automated pattern search already generalizes to multiple files — grep doesn't care how many there are. The catalog-driven addition is *scope*: validation patterns run against every path in the manifest, not only the paths that appear in the task map. A violation sitting in a path nobody happened to analyze is otherwise invisible by construction, not because it doesn't exist.

**2. Coverage**

Compare paths discovered (manifest) vs. paths analyzed (opened in Phase 1) vs. paths with issues raised. A gap between discovered and analyzed with no documented reason means the audit is incomplete, not clean.

**3. Orphan paths**

Paths present on disk but outside the declared include/exclude scope. Each one gets a one-line disposition: correctly filtered noise, or a scope gap that should have been included.

**4. Path drift**

After any RELOCATE, re-scan (or targeted grep) the full catalog for the old path string; zero remaining matches is the only acceptable result, changelog and history files aside.

**5. Extended Final Report**

```
DIRECTORY              FILES  ANALYZED  STATUS      CRITICAL  HIGH  MEDIUM
features/checkout        6       6      ✅ CLEAN       0        0      0
shared/styles             4       4      ✅ CLEAN       0        0      0
utils/                    9       6      ⚠ PARTIAL      0        0      0  (3 files exceeded size threshold, unread)
...
TOTAL                   214     187                    0        0      2

Coverage: 187 / 214 analyzed (87%). Remaining gap: files flagged for
exceeding the size threshold, plus files the Phase 1 shortlist judged
irrelevant to every violation category — both itemized in meta. (Scan-
param exclusions like node_modules/ and build/ fall under the orphan-
path check above, not this coverage figure.)
```

---

## Requirements Specification — Catalog Extension

Extends the base doc's "Requirements Specification for Creating a Task Map." In addition to the base ten elements, a catalog-scoped task specification must define:

```markdown
11. Catalog root(s) — the top-level directory (or directories) all
    paths are made relative to

12. Scan parameters — include/exclude globs, depth limit, size
    threshold, symlink policy, hidden-file policy

13. Path format convention — separator, root-relativity,
    case-sensitivity notes for the target filesystem

14. Manifest requirements — tree view + flat list, and exactly which
    metadata fields each entry must carry

15. Grouping granularity rule — how directory/module/file grouping is
    chosen, and at what catalog size each tier applies

16. Cross-path dependency rule — every dependency entry carries
    `path`, never a bare filename

17. Relocation handling — RELOCATE always triggers a full-catalog
    reference search, never a partial one

18. Coverage and staleness policy — how `analyzed_files` is
    reconciled against `manifest_totals.files`, and when the catalog
    must be re-scanned during a long-running task
```

### Spec Improvements Over a Naive Catalog Approach

| Naive catalog spec problem | Consequence | Solution |
|---|---|---|
| No declared root | Paths are ambiguous, or break when the catalog is checked out elsewhere | Always declare and record `catalog_root` |
| No include/exclude patterns | Scan pulls in `node_modules`, build output, lockfiles, binaries | Explicit include/exclude globs with sensible defaults |
| Bare filename instead of path | Domino references silently resolve to the wrong file when basenames collide | Every reference is a full root-relative `path` |
| No manifest confirmation step | Analysis starts on an unconfirmed, possibly wrong file set | Manifest built and confirmed before Phase 1 begins |
| Single grouping tier assumed | A 300-file catalog gets planned like a 5-file widget; the plan collapses | Grouping granularity scales with catalog size |
| No relocation handling | Moving a file leaves stale imports scattered across the tree | RELOCATE mandates a full-catalog reference search |
| No coverage tracking | "Audited and clean" is indistinguishable from "never looked at" | `analyzed_files` vs. `manifest_totals.files` tracked explicitly |

---

## Templates for Catalog-Scoped Task Types

### Full-Repository Audit (Unfamiliar Codebase)

```
Phase 0: declare catalog root(s) + scan parameters, walk the tree, confirm manifest
Phase 1: manifest-guided targeted reads; analyze by dimension, batched by directory
Phase 2: map with path-anchored locations and directory rollups
Phase 3: plan grouped by module/package, then file, then violation type
Phase 4: dependency-aware traversal, module by module
Phase 5: full-manifest validation + coverage check + orphan check
```

### Monorepo-Wide Refactor

```
Phase 0: declare each package as a sub-catalog under the monorepo root, build manifests
Phase 1: analyze package by package; cross-package references noted as found
Phase 2: map split by package; cross-package dependencies marked CRITICAL
Phase 3: plan: foundation/shared packages first, dependents after (topological order)
Phase 4: execute foundation packages first, validate, only then move to dependents
Phase 5: catalog-wide grep + per-package build/test + cross-package smoke test
```

### Directory Restructuring / File Relocation

```
Phase 0: declare root + complete old-path → new-path mapping, confirm old paths exist
Phase 1: find every reference to each old path across the ENTIRE catalog
Phase 2: map keyed old path → new path (RELOCATE), domino = every referencing path
Phase 3: plan leaves-first (files nobody imports), then upward — no dangling state
Phase 4: move the file, then immediately fix every referencing path — never deferred
Phase 5: full-catalog grep for every old path string; zero matches required
```

### Cross-Catalog Duplicate / Dead-File Detection

```
Phase 0: declare root + scan parameters, build manifest with per-file signatures
Phase 1: cluster by signature similarity; build reference graph for inbound-zero files
Phase 2: map of duplicate clusters and orphan candidates (zero inbound references)
Phase 3: confirm true orphans — not entry points, not dynamically loaded — before DELETE
Phase 4: remove or merge, path by path, rechecking the reference graph after each
Phase 5: full build/test to confirm nothing dynamically depended on a removed path
```

---

## AI Checklist — Catalog Extension

In addition to the base checklist:

```
□ Have I declared an explicit catalog root that every path is relative to?
□ Have I defined include/exclude scan parameters before walking the tree?
□ Have I built and confirmed a manifest BEFORE reading any file content?
□ Does every location in the map carry a full path, never a bare filename?
□ Have I checked for basename collisions before trusting a filename in
  a dependency reference?
□ Have I chosen a grouping granularity that matches the catalog's
  actual size?
□ Is my execution order across paths dependency-aware, or at minimum
  deterministic?
□ For every RELOCATE, have I searched the ENTIRE catalog for
  references to the old path — not just the directories that seemed
  related?
□ Does final validation cover the full manifest, not only the paths I
  happened to touch?
□ Have I reconciled manifest count vs. analyzed count vs. issue-free
  count (coverage), and is the gap explained?
```

---

## Anti-Patterns — Catalog Extension

### ❌ Scanning Without a Declared Root

```
Bad:  paths recorded as absolute filesystem paths, or relative to
      whatever directory the AI happened to be "in"
Good: every path recorded relative to one explicitly declared
      catalog_root
```

Reason: absolute or context-dependent paths break the instant the catalog moves — a different checkout, a different machine, a different working directory.

### ❌ Bare Filenames in Dependencies

```
Bad:  "dependencies": [{"issue_id": "app-045", "file": "index.js"}]
Good: "dependencies": [{"issue_id": "app-045",
                         "path": "features/checkout/index.js"}]
```

Reason: basename collisions turn a "reference" into a guess the moment a catalog has more than a handful of files.

### ❌ Loading the Entire Catalog "Just in Case"

```
Bad:  open every file in the manifest before starting Phase 1
Good: manifest first, then targeted reads guided by cheap signals
```

Reason: at catalog scale this isn't thoroughness, it's noise — it exhausts the context budget on irrelevant content before the analysis that matters even starts.

### ❌ Treating a Path as a Permanent Identity

```
Bad:  a domino reference recorded once and trusted for the rest of a
      long-running task, even after upstream files have been relocated
Good: paths re-verified against the current manifest before being
      acted on, once meaningful relocation work has happened since
      they were recorded
```

Reason: a path names where a file currently is, not what it permanently is — RELOCATE issues invalidate every stored reference to the old path.

### ❌ Flat Grouping on a Deep Tree

```
Bad:  "one file = one group" applied unchanged to a 300-file monorepo
Good: grouping granularity scales up — package → directory → file →
      violation type — as catalog size grows
```

Reason: a two-level grouping scheme designed for five files produces an unreadable, unmanageable plan at three hundred.

### ❌ Relocating a File Without a Full-Catalog Reference Search

```
Bad:  move the file, fix the imports in the two files that were
      open at the time
Good: move the file, then grep the ENTIRE manifest for the old path
      string before marking the issue done
```

Reason: a relative import three directories away, with no obvious connection to the file being moved, is exactly the reference a partial search misses — and it's a broken build.

### ❌ Ignoring the Manifest/Analyzed Gap

```
Bad:  report "audit complete" with no mention of how many discovered
      files were actually opened
Good: meta.manifest_totals.files vs. meta.analyzed_files stated
      explicitly, gap explained
```

Reason: an unexplained gap is indistinguishable from work that was simply never done.

### ❌ Following Symlinks Blindly

```
Bad:  recursive scan follows every symlink, eventually looping back
      on itself or double-counting a directory reachable two ways
Good: symlinks not followed by default; if followed, each real path
      is visited once, tracked explicitly
```

Reason: an unguarded symlink cycle turns a bounded scan into one that never terminates, or into a manifest with duplicated, misleading counts.

---

## Working with Large Catalogs

Extends the base doc's "Working with Large Files" one level up: the same discipline — see the whole shape before working — applies, but the object that needs to be seen whole is now the catalog, and "whole" can't mean "full content" once file count runs into the hundreds or thousands.

**Load in tiers, not all-or-nothing:**

```
Tier 1 — Manifest only (path, size, line count, extension)
         Every path in scope, always. This is what "seeing the whole
         catalog" means at this scale — not full content.

Tier 2 — Outline (first N lines, exported symbols, or a pre-search hit)
         Only paths a cheap signal flagged as possibly relevant.

Tier 3 — Full content
         Only paths confirmed relevant, opened completely, one
         directory or module batch at a time — never the whole
         catalog at once.
```

**Batch Tier 3 loads by directory or module**, exactly as in the Phase 1 extension, so a single working set never exceeds what the current pass can actually hold onto.

**Confirm each batch before moving to the next**, the same rule the base doc applies to file-internal passes (CSS → HTML → JS):

```
After components/: 41 files, Tier 3, 0 remaining pattern hits
After utils/:       12 files, Tier 3, 2 remaining — flagged, resolved
...
```

**Re-tier, don't re-scan, when returning to a phase.** If Phase 4 execution needs a file that was only Tier 1 or Tier 2 during Phase 1, promote it to Tier 3 on demand — there's no need to rebuild the manifest, only to load more of what it already pointed to.

---

## Execution Quality Metrics — Catalog Extension

In addition to the base doc's numerical indicators, record:

```
1. Paths discovered (manifest) vs. paths analyzed vs. paths modified
2. Coverage % = analyzed / discovered
3. Directories touched vs. total directories in the manifest
4. Orphan/excluded paths reviewed, and their disposition recorded
5. Stale path references found after any RELOCATE (target: 0)
6. Basename collisions detected, and how each was resolved
```

---

*This driver extends the base methodology to directory-scale, path-addressed work — full-repository audits, monorepo-wide refactors, and catalog-wide file relocations — where the working set must be discovered by scanning rather than declared upfront by name.*
