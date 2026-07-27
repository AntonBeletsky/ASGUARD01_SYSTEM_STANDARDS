# AI Task Execution Methodology — Build Protocol
## A Companion Methodology for Merging, Splitting, and Reorganizing Files Across Boundaries

---

## Relationship to the Base Methodology

`ai-task-execution-methodology.md` covers tasks where the **file set is fixed** and the work is bringing *content* into compliance with a spec — renaming, fixing violations, migrating APIs. The number of files never changes; only what's written inside them does.

This document covers the other half of the problem: tasks where **the file set itself changes shape** — files get merged, split apart, or regrouped under a different boundary than the one they currently have.

| | Base methodology | This methodology |
|---|---|---|
| What changes | Content inside a fixed set of files | The boundaries between files — count, location, composition |
| Unit of work | A *violation* (text that doesn't match a spec) | A *fragment* (a bounded block of content) and a *reference* (a pointer from one location to another) |
| Typical verbs | rename, replace, delete | extract, insert, merge, split, dedupe, relink |
| "Domino" concept | Other occurrences of the same identifier, inside the same files | Every place, across *all* files, that points at a piece about to move |
| Proof of correctness | grep for the old pattern returns zero | every reference resolves to exactly one target; every moved byte is accounted for |

Both documents share the same skeleton — Context Loading → Analysis → Map → Plan → Execution → Validation — and the same non-negotiable rule: **analysis, planning, and execution are separate stages that are never interleaved.** What follows adapts that skeleton to structural work; where a phase carries over unchanged in spirit, this says so rather than re-explaining it.

**Composability:** run the two in sequence, never simultaneously. Assemble first, then — if needed — run the base methodology's naming/compliance pass over the result. Or the reverse: clean up naming first, then split the file. Don't rename something *while* moving it unless the rename is strictly required to resolve a collision the move itself creates (see `RENAME_FOR_COLLISION` under Operation Types).

---

## Philosophy

The base methodology's rule holds without modification:

```
ANALYSIS → MAP → EXECUTION → VALIDATION
```

Mixing stages still causes most errors, but a build task fails in a specific way when they're mixed: content gets pasted before every destination for it is confirmed, references get hard-coded before collisions are known, and by the time something breaks, three files are already half-rewritten with no clean way to tell which copy is authoritative.

One more principle sits on top, because it's the actual reason this document exists:

**A file's full content is not needed to plan where it goes. It's only needed to actually move it.**

Everything in Phase 0–2 — loading, analysis, mapping — can and should be done from *structure*: line counts, tag/marker boundaries, ids, classes, `href`/`src` targets, import statements. None of that requires holding a 2,000-line file's full body in context. A fragment's full content only needs to enter context at the moment it's being extracted and placed — and even then, ideally as a mechanical range-copy rather than something read, held in mind, and retyped.

Token cost and correctness point the same direction here: reading less and copying exact ranges is both *cheaper* and *more accurate* than reading everything and reproducing it from memory. A model that "remembers" a 40-line fragment and retypes it can silently drop an attribute or renumber a class; a model that cuts an exact, verified line range and pastes it verbatim cannot.

---

## Task Taxonomy

### Directions

```
MERGE        many files  →  one file       (assemble many into one)
SPLIT        one file    →  many files     (disassemble by some criterion)
REORGANIZE   many files  →  many files      (re-grouped differently than before)
EXTRACT      part of N files → one new shared file, N files updated to reference it
```

Every build task is one of these four, or a sequence of them run as separate passes.

### File Roles

Before analysis starts, every file in scope gets exactly one role. The role determines how it's read and what "correct" means for it.

| Role | Definition | Example |
|---|---|---|
| **SHELL / CONTAINER** | Defines the outer skeleton and the slots fragments drop into | A page shell with a nav sidebar and tab-panes, some already populated, some placeholders |
| **FRAGMENT / MODULE** | A bounded, self-contained unit of content to be moved, merged, or split out | A single tab's markup, previously built and previewed as its own standalone file |
| **SHARED RESOURCE** | Consumed by more than one fragment, or by the shell itself | A page-wide CSS file, a shared JS controller |
| **SCOPED RESOURCE** | Belongs to exactly one fragment | A CSS file scoped to a single component's class |
| **ORCHESTRATOR** | Runtime glue wiring the shell to fragments | JS that reads `data-target`/`data-action` and activates the right pane |
| **ANCHOR** | Not a file — a *location inside* a SHELL where a fragment is meant to land | A placeholder comment, an empty container, a stub already carrying the right `id`, or even a `<script src="...">` pointing at a file that doesn't exist yet |

A file can hold more than one role if it's small — the point of tagging is knowing, before reading a single byte of content, *what kind of thing you're looking for* in that file.

---

## Workflow Structure

### Phase 0 — Context Loading

Same rule as the base methodology: **nothing gets transformed at this stage**, only read and confirmed. For a build task, "context" specifically means:

- **Direction** — MERGE / SPLIT / REORGANIZE / EXTRACT, and the destination file(s)
- **Criterion** — the rule deciding where a boundary falls (e.g. "one file per tab-pane", "one file per top-level `<section>`", "anything referenced from ≥2 fragments becomes shared")
- **Materials** — every file in scope, with its declared role
- **Constraints** — anything that must not move, must stay byte-identical, or is off-limits
- **Scope boundary** — which discovered references are this pass's job to resolve, and which belong to a different, not-yet-started task (see the `profile-details` note under 1.3)

```
User: here are 5 files, merge the 4 tab fragments into the shell
AI:   [reads file names + sizes, does not open content yet]
      → "5 files loaded. Direction: MERGE (4 fragments → 1 shell).
         Roles: shell = customer-account-1e-clean.html,
         fragments = account-{messages,mywallet,orders,wishlist},
         shared = page.css/page.js. Confirming criterion before analysis."
```

**Do not assume a fragment's destination from its filename.** Confirm the mapping explicitly — see the naming-mismatch note under 1.1.

**Why it matters:** guessing the direction or criterion wrong here means the map built in Phase 1–2 targets the wrong shape, and that only surfaces once execution has already started moving content.

### Phase 1 — Analysis

#### 1.1 Classify Every File's Role

One pass, no content-reading required — a file name, a `wc -l`/`wc -c`, and (for markup) a check for `<!DOCTYPE`/`<head`/`<body` tells you whether a file is a full standalone document or a bare fragment:

```
FILE                             ROLE          STANDALONE?  LINES   NOTES
customer-account-1e-clean.html   SHELL         yes            653  14 nav links, 14 tab-panes (some placeholder)
account-messages-1b.html         FRAGMENT      yes          1,770  own <head>, own inline <script>
customer-account-page.css        SHARED        n/a              —  consumed by shell + all fragments
customer-account-tab-overview.css SCOPED       n/a              —  consumed only by the inline overview tab
customer-account-page.js         ORCHESTRATOR  n/a              —  reads data-target/data-action, hash-routes
```

A FRAGMENT that is itself a standalone document is the most common source of wasted tokens: its actual payload is often 20–40% of its line count. The rest — `<!DOCTYPE>`, a duplicated CDN `<head>`, closing boilerplate — exists only so the fragment could be previewed in isolation, and none of it survives the merge as-is. Flagging this up front means 1.2 goes looking for the *payload boundary*, not the whole file.

**Do not assume the fragment's filename matches its destination anchor.** In this document's reference case, `account-messages-1b.html` doesn't map to `id="tab-messages"` — it maps to `id="tab-correspondence"`. Confirm the real mapping (grep the shell for the fragment's likely keywords, or look for an explicit anchor comment) before it's baked into the plan.

#### 1.2 Build the Structural Inventory — Scan, Don't Slurp

For each file, get a skeleton without reading the body:

```bash
wc -l file.html
grep -n -E '<!DOCTYPE|<head|<body|</body|</html' file.html      # full document, or bare fragment?
grep -n -oE 'id="[a-zA-Z0-9_-]+"' file.html                       # exports: ids it defines
grep -n -oE 'class="[^"]+"' file.html | tr ' ' '\n' | sort -u     # exports: classes it defines
grep -n -E '<link|<script src|@import|href=|src='  file.html     # imports: what it expects elsewhere
```

Record exact line numbers for every boundary that might become a cut point. Don't read what's between them yet — that content only matters once this specific block is the one being moved.

**When a full read is actually justified** (the exception, not the default):
- the file is small enough that scanning costs more round-trips than reading it outright (roughly, under ~150 lines / ~8KB)
- no marker or tag-matching can find the boundary — logic and markup are interleaved in a way that requires understanding it to know where one "thing" ends and the next begins
- an embedded script's behavior could interact with the move in a non-obvious way (e.g. it touches `document`/`window` outside its own subtree), and that risk needs judgment, not just relocation

#### 1.3 Reference Graph Analysis — the Build-Task "Domino"

The base methodology's domino asks: *what else breaks if I fix only this one violation?* The build-task equivalent asks: *what else points at this block, and will it still find it once the block moves?*

For every export found in 1.2, grep for its name **across the entire file set**, not just the file that defines it:

```
Export: id="tab-correspondence"     (tab-pane, defined in shell, line 513)
  ├── shell:163   data-target="tab-correspondence"                (sidebar nav link)
  ├── shell:328   href="#tab-correspondence"                       (Overview shortcut card)
  └── shell:514   aria-labelledby="account-nav-tab-correspondence" (paired ARIA reference, see below)

Export: id="account-nav-tab-correspondence"   (nav link, defined in shell, line 162)
  └── shell:514   aria-labelledby → this id      (the tab-pane's half of the same ARIA pair)

Export: data-ref="messages-root"    (fragment-local markup, account-messages-1b.html:290)
  └── account-messages-1b.html:1759   new MessagesController('[data-ref="messages-root"]')
      — an internal consumer, in the SAME file's own inline <script>. Moving the
      markup without also moving this script breaks the pairing just as surely as
      an external reference would.

Import: <script src="customer-account-messages.js">   (shell, line 603)
  └── DANGLING — no file by that name among the files in scope. The payload
      waiting to fill it is account-messages-1b.html's own inline <script>
      (lines 615–1762). The shell pre-declares this filename the same way it
      pre-declares markup anchors with TODO comments — it's a reference, not
      just boilerplate.
```

Build the full edge list before moving anything. Flag three conditions explicitly:

```
DANGLING   — an import/reference with no matching export anywhere in scope
AMBIGUOUS  — the same id/name defined in 2+ places that will share a document/
             namespace once merged (not a problem while fragments are separate
             standalone pages — becomes one the moment they share a DOM)
ORPHANED   — an export nothing in scope consumes (not necessarily wrong, worth a note)
```

**Scope note:** the shell declares the same dangling-script pattern for `customer-account-mywallet.js` (line 604), `customer-account-orders.js` (605), `customer-account-profile-details.js` (607), and `customer-account-wishlist.js` (608) — five dangling references total, one per script tag except `customer-account-page.js` (606), which already exists. Four of the five have a matching fragment among the files provided; `profile-details` does not. That one is a Phase 0 scope question — confirm whether it belongs to this pass before treating it as this pass's problem.

**Aside:** `account-orders-1d.html` declares 0 ids; `account-messages-1b.html` declares 2. Both already follow a no-id-hooks convention — everything interactive is targeted via `data-action`/`data-ref` instead, the same convention the base methodology's Law Zero asks for. That choice, made for JS-hook hygiene, pays a second dividend here: almost no collision surface once merged. `account-mywallet-1b.html` (29 ids) and `account-wishlist-1b.html` (18 ids) are exactly the files worth checking first — and worth checking against the shell's own ids too, not just against each other.

**Rule:** the graph must be exhaustive before Phase 2 starts. An incomplete graph is this document's version of an incomplete domino — the failure just shows up as a broken tab or a script that 404s, instead of a broken CSS rule.

### Phase 2 — The Build Map

The counterpart to the base methodology's Task Map — a JSON artifact, not prose, so it can be checked mechanically. A Build Map has **two** co-equal parts: what physically moves, and what must stay wired up.

A single fragment file usually decomposes into more than one operation — markup, scoped styles, and scoped script each have their own destination and are extracted as separate, layered passes, echoing the base methodology's own CSS → HTML → JS layering (Phase 4.3 there). The example below shows the shape for one fragment (`account-messages-1b.html` → 3 operations); the other three fragments follow the same pattern.

```json
{
  "meta": {
    "direction": "MERGE_MANY_TO_ONE",
    "destination_files": ["customer-account-1e-clean.html"],
    "source_fragment_files": [
      "account-messages-1b.html",
      "account-mywallet-1b.html",
      "account-orders-1d.html",
      "account-wishlist-1b.html"
    ],
    "shared_resource_files": ["customer-account-page.css", "customer-account-page.js"],
    "criterion": "one standalone preview file per tab-pane, matched to the shell's existing data-target values, TODO anchors, and dangling script-src references",
    "total_operations": 13
  },
  "operations": [
    {
      "id": "build-000",
      "type": "DEDUPE",
      "source": {
        "file": "account-messages-1b.html",
        "lines": { "start": 8, "end": 8 },
        "context": "<link href=\"...bootstrap@5.3.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\">"
      },
      "destination": {
        "file": "customer-account-1e-clean.html",
        "anchor": "do not carry this <link> (or the matching bootstrap@5.3.3 JS bundle) over — shell already loads 5.3.8 of both at lines 32 and 592",
        "lines": null
      },
      "references_touched": [
        { "ref_type": "shared-resource-version", "name": "bootstrap (css+js)", "expected_count": 1 }
      ],
      "depends_on": [],
      "collision_risk": "version mismatch (5.3.3 vs 5.3.8) in both the CSS link and the JS bundle — resolved by keeping the shell's version of each",
      "status": "pending"
    },
    {
      "id": "build-001",
      "type": "EXTRACT_INSERT",
      "source": {
        "file": "account-messages-1b.html",
        "lines": { "start": 289, "end": 576 },
        "context": "<section class=\"messages-container d-flex flex-column ...\" data-ref=\"messages-root\">"
      },
      "destination": {
        "file": "customer-account-1e-clean.html",
        "anchor": "replace <!-- TODO: insert tab content here — account-messages --> (line 523, inside id=\"tab-correspondence\")",
        "lines": { "start": 523, "end": 523 }
      },
      "references_touched": [
        { "ref_type": "data-target/id-pair", "name": "tab-correspondence", "expected_count": 1 },
        { "ref_type": "data-ref", "name": "messages-root", "expected_count": 1 }
      ],
      "depends_on": ["build-000"],
      "collision_risk": "none found in 1.3 — the fragment declares only 2 ids total, neither reused elsewhere",
      "status": "pending"
    },
    {
      "id": "build-002",
      "type": "EXTRACT",
      "source": {
        "file": "account-messages-1b.html",
        "lines": { "start": 616, "end": 1761 },
        "context": "class MessagesController { ... }  ...  new MessagesController('[data-ref=\"messages-root\"]');"
      },
      "destination": {
        "file": "customer-account-messages.js",
        "anchor": "new file — resolves the shell's existing but dangling <script src=\"...customer-account-messages.js\"> at line 603",
        "lines": { "start": 1, "end": 1146 }
      },
      "references_touched": [
        { "ref_type": "script-src", "name": "customer-account-messages.js", "expected_count": 1 },
        { "ref_type": "data-ref", "name": "messages-root", "expected_count": 1 }
      ],
      "depends_on": [],
      "collision_risk": "none — shell defines no existing MessagesController",
      "status": "pending"
    }
  ],
  "reference_registry": [
    {
      "ref_type": "data-target/id-pair",
      "name": "tab-correspondence",
      "defined_in": [{ "file": "customer-account-1e-clean.html", "line": 513 }],
      "consumed_in": [
        { "file": "customer-account-1e-clean.html", "line": 163, "via": "data-target" },
        { "file": "customer-account-1e-clean.html", "line": 328, "via": "href=\"#tab-correspondence\" on the Overview shortcut card" }
      ],
      "resolved": true
    },
    {
      "ref_type": "aria-pair",
      "name": "account-nav-tab-correspondence ⇄ tab-correspondence",
      "defined_in": [
        { "file": "customer-account-1e-clean.html", "line": 162, "attr": "id (on the nav link)" },
        { "file": "customer-account-1e-clean.html", "line": 513, "attr": "id (on the tab-pane)" }
      ],
      "consumed_in": [
        { "file": "customer-account-1e-clean.html", "line": 162, "attr": "aria-controls → tab-correspondence" },
        { "file": "customer-account-1e-clean.html", "line": 514, "attr": "aria-labelledby → account-nav-tab-correspondence" }
      ],
      "resolved": true
    },
    {
      "ref_type": "script-src",
      "name": "customer-account-messages.js",
      "defined_in": [],
      "consumed_in": [{ "file": "customer-account-1e-clean.html", "line": 603, "via": "<script src>" }],
      "resolved": false,
      "note": "dangling until build-002 creates the file — the shell already expects it"
    },
    {
      "ref_type": "shared-resource-version",
      "name": "bootstrap (css+js)",
      "defined_in": [
        { "file": "customer-account-1e-clean.html", "line": 30, "version": "unversioned (local file:// copy)" },
        { "file": "customer-account-1e-clean.html", "line": 32, "version": "5.3.8 (CDN css)" },
        { "file": "customer-account-1e-clean.html", "line": 592, "version": "5.3.8 (CDN js bundle)" },
        { "file": "account-messages-1b.html", "line": 8, "version": "5.3.3 (CDN css)" },
        { "file": "account-messages-1b.html", "line": 1765, "version": "5.3.3 (CDN js bundle)" }
      ],
      "consumed_in": [],
      "resolved": false,
      "note": "five references to the 'same' library, two version strings and two path conventions (absolute file:// vs relative ../../../assets/...), before a single fragment is merged in — DEDUPE requires an explicit decision, not a silent drop"
    }
  ]
}
```

#### Required Fields

| Field | Purpose |
|---|---|
| `type` | One of the Operation Types below — determines what "correct" means for this row |
| `source.lines` | Exact range — the only part of the source file that should ever be read in full |
| `source.context` | A verbatim, ≤120-character snippet — lets the block be re-found without re-scanning |
| `destination.anchor` | The literal marker or exact insertion point — never "somewhere in the tab-pane" |
| `references_touched` | Every id/class/attribute this move could affect — what Phase 5 checks against |
| `depends_on` | Other operation `id`s that must complete first (a collision rename, a resource dedupe) |
| `collision_risk` | Explicit, always filled in — "none found" is a valid value; it's proof 1.3 was actually done |
| `status` | `pending` / `in-progress` / `done` / `verified` — the last state has no base-methodology equivalent, added because "moved" and "confirmed correctly moved" are different claims |

The `reference_registry` adds: `defined_in` / `consumed_in` (each a list — a reference can have multiple consumers, as `tab-correspondence` does above) and `resolved` (boolean — must be `true` for everything before the map counts as complete).

#### Operation Types

```
EXTRACT               — pull a bounded block out of a source, read-only on the source
INSERT                 — place an already-extracted block at a destination anchor
EXTRACT_INSERT          — the common case: one source range, one destination anchor, one step
MERGE                  — combine two or more blocks into one (e.g. two <style> blocks into one file)
SPLIT                  — the inverse: one source range becomes N destination files
DEDUPE                  — remove a redundant copy of a shared resource once reconciled
RELINK                  — update a path/href/src/import to point at the new location
RENAME_FOR_COLLISION     — rename an id/class/variable and propagate it to every consumer,
                           in the same operation — never split across two rows
REORDER                  — reposition a block within the same file (e.g. move a var above its first use)
```

#### Risk Levels

Repurposed from the base methodology's severity scale, re-grounded in what a build task can actually break:

```
CRITICAL — breaks referential integrity: a dangling reference, a duplicate id in
           one namespace, or silent content loss
HIGH     — structurally wrong even if references technically resolve: bad nesting,
           wrong insertion point, a fragment landing inside the wrong tab-pane
MEDIUM   — redundant, not broken: a shared resource loaded twice, a near-duplicate
           block that should be reconciled
LOW      — cosmetic: whitespace, comment style, incidental formatting differences
```

### Phase 3 — Assembly Plan

The map becomes a grouped, ordered tracker — same principle as the base methodology, regrouped around **destinations** rather than source files, because a MERGE task's unit of delivery is "this destination is fully assembled," not "this source is fully processed."

```
Destination: customer-account-1e-clean.html (group)
  ├── Collisions & renames (subgroup — resolved first; nothing downstream is
  │     trustworthy until these are settled)
  │   └── (none required — 1.3 found no cross-fragment id collisions)
  ├── Shared resource reconciliation (subgroup — done once, before insertion)
  │   └── [ ] build-000 — bootstrap css+js: five references collapse to the
  │           shell's existing 5.3.8, drop each fragment's own 5.3.3
  ├── Fragment markup insertion (subgroup — one item per tab, in nav order)
  │   ├── [ ] build-001 — account-messages markup → #tab-correspondence  (depends_on: build-000)
  │   ├── [ ] build-003 — account-mywallet  markup → #tab-wallet         (depends_on: build-000)
  │   ├── [ ] build-005 — account-orders    markup → #tab-orders         (depends_on: build-000)
  │   └── [ ] build-007 — account-wishlist  markup → #tab-wishlist       (depends_on: build-000)
  ├── Fragment script extraction (subgroup — resolves the shell's own dangling
  │   │     <script src> references at lines 603–605 and 608)
  │   ├── [ ] build-002 — account-messages script → customer-account-messages.js (new file)
  │   ├── [ ] build-004 — account-mywallet  script → customer-account-mywallet.js (new file)
  │   ├── [ ] build-006 — account-orders    script → customer-account-orders.js (new file)
  │   └── [ ] build-008 — account-wishlist  script → customer-account-wishlist.js (new file)
  └── Scoped CSS extraction (subgroup — one item per fragment with embedded <style>)
      └── [ ] build-009..012 — lift each fragment's <style> block into its own
              customer-account-tab-*.css, following the tab-overview.css precedent
```

**Ordering rules:**
1. Collisions and renames first — every later step assumes names are already unique.
2. Shared/global resource reconciliation next, and only once — inserting fragments before this is settled means re-touching every fragment again if a dedupe decision changes.
3. Fragment insertion in whatever order matches the shell's own nav order, not the order the fragments happen to be numbered. Nav order is what a reviewer checks against; matching it makes verification easier, not just tidier.
4. RELINK operations happen in the same step as the MOVE they follow — never deferred to "a cleanup pass at the end."

### Phase 4 — Execution

**Standing rule:** for SPLIT/REORGANIZE tasks, where a monolith gets carved up and possibly deleted, keep the original intact (copy, don't move-and-delete) until Phase 5 confirms the new files reconstruct it. A build task is far less reversible mid-flight than a rename — grep can always find a missed rename; nothing recovers a deleted source that turns out to still be needed.

#### Principles

**1. One destination file at a time**

Complete every operation targeting a destination, validate it, then move to the next. Don't leave one destination half-assembled to go start another.

**2. Extract by range, never by memory**

```python
# ❌ Wrong — read the fragment, then write "what it said" into the destination
fragment_text = read_lines("account-messages-1b.html", 289, 576)
# ...then compose a new version by hand based on what was read

# ✅ Correct — cut the exact range, paste it verbatim
lines = open("account-messages-1b.html").readlines()
block = "".join(lines[288:576])          # 0-indexed slice for lines 289–576
insert_at(destination, anchor_line=523, content=block)
```

The map's `source.lines` exists precisely so this step never needs a re-read to "remember" what was there — the range was already recorded in 1.2.

**3. Verify tag/brace balance before cutting**

A range guessed by eye is a common source of truncated or over-included blocks once tags nest more than one level. Confirm the range mechanically (see *Precise Boundary Matching*, below) before it's treated as final — not after something renders broken.

**4. Resolve a collision and all its consumers in one operation**

If `RENAME_FOR_COLLISION` applies to some `id`, the rename and every one of its consumers — the element's `id=`, every `data-target`/`aria-labelledby`/`for` pointing at it, every CSS selector, every `querySelector` in JS — change together. A rename that only touches the definition produces a dangling reference, which is worse than not renaming at all: it now fails silently instead of obviously.

**5. Reconcile shared resources as one unified pass**

Don't rediscover the Bootstrap version mismatch once per fragment as each is inserted — resolve it once, in Phase 2/3, and every fragment insertion after that simply doesn't re-add a `<link>` or `<script src>` that's already been decided.

**6. Validate immediately after each destination — not at the end**

Same reasoning as the base methodology: an error introduced while assembling destination 1 shouldn't be discovered while debugging destination 3.

### Phase 5 — Validation

#### Level 1 — Structural / Content-Preserving

The check the base methodology has no equivalent for: **prove**, don't eyeball, that a moved block survived the move unchanged.

```bash
# hash the source range exactly as extracted
sed -n '289,576p' account-messages-1b.html | sha256sum

# hash the same span in the destination, after insertion
sed -n '523,810p' customer-account-1e-clean.html | sha256sum   # line numbers shift once inserted — recompute
```

For a pure `EXTRACT_INSERT` with no intended edits, these must match. If they don't, something was altered in transit — whitespace, an attribute, a typo — and that's a Phase 4 defect, not a Phase 5 nitpick.

Reconcile line/byte counts at the file-set level too:

```
total lines before = shell(653) + Σ fragment payloads (excluding boilerplate)
total lines after  = new shell line count + new per-fragment .js/.css files
difference should equal: (boilerplate discarded) − (wrapper markup added, if any)
```

#### Level 2 — Referential Integrity

Automated, not visual:

```bash
# every data-target must resolve to exactly one matching id
for target in $(grep -oE 'data-target="[a-z-]+"' shell.html | sort -u); do
  id_attr=$(echo "$target" | sed 's/data-target=/id=/')
  count=$(grep -c "$id_attr" shell.html)
  [ "$count" -eq 1 ] || echo "MISMATCH: $target — found $count times"
done

# every <script src="local-file.js"> must point at a file that actually exists
grep -oE 'script src="[^"]+\.js"' shell.html | while read -r tag; do
  path=$(echo "$tag" | sed -E 's/script src="([^"]+)"/\1/')
  [ -f "$path" ] || echo "DANGLING: $path"
done
```

Extend the same idea to every entry in `reference_registry`: count occurrences of every id, confirm every `href`/`src` target file exists, confirm every CSS class the moved fragment relies on is actually defined somewhere in the merged stylesheet set.

#### Level 3 — Syntax & Semantic Validity

- Tag balance across the **whole** destination file, not just the inserted region — an off-by-one during insertion can unbalance something outside the block that was fine before.
- No shared/global resource loaded twice — grep the final `<head>` for duplicate `href`s, and only ignore version/path differences after confirming the versions genuinely match.
- **Semantic exception review**, same spirit as the base methodology:
  ```
  Two fragments both use class="d-flex justify-content-between"   ← LEGAL (utility class, meant to repeat)
  Two fragments both define id="filter-btn"                        ← VIOLATION once merged (ids must be unique per document)
  ```

#### Final Report

```
OPERATION      SOURCE → DESTINATION                          STATUS       REFS OK   HASH MATCH
build-000      bootstrap 5.3.3 → dropped (kept 5.3.8, css+js)  ✅ VERIFIED    n/a        n/a
build-001      messages markup → #tab-correspondence           ✅ VERIFIED   3/3        ✅
build-002      messages script → customer-account-messages.js  ✅ VERIFIED   2/2        ✅
build-003..008 mywallet/orders/wishlist, same shape             ✅ VERIFIED    —          ✅
build-009..012 scoped <style> → customer-account-tab-*.css      ✅ VERIFIED    —          ✅
```

---

## Precise Boundary Matching (Beyond Naive Regex)

Nested tags break naive boundary-finding. `grep -n '</div>'` after a `<div>` you care about returns every closing div in the file, in document order — not necessarily the one that matches. The same problem shows up in JSON/JS (`{ ... }`) and in code (`( ... )`). A range that's "roughly right" is exactly what Level 1 validation exists to catch — but it's cheaper to get it right the first time.

The fix is a small depth counter instead of a single-pattern search — cheap, deterministic, and correct for well-formed input:

```python
import re

def find_block_end(text, start_pos, tag="div"):
    """Given the character offset of an opening <tag ...>, return the
    offset just past its matching closing </tag>. Assumes well-formed,
    non-self-closing nesting of the same tag name."""
    pattern = re.compile(rf"</?{tag}\b[^>]*>")
    depth = 0
    for m in pattern.finditer(text, start_pos):
        depth += -1 if m.group().startswith("</") else 1
        if depth == 0:
            return m.end()
    return None  # unbalanced input — a Phase 1 finding, not a Phase 4 surprise
```

Run against `account-messages-1b.html`, this finds the `<section class="messages-container">` opened at line 289 closing at line 576 — confirmed independently by the fragment's own closing comment, `<!-- /messages-container -->`, immediately after. Two independent methods agreeing is itself a validation step, not just a convenience. (Its `<script>...</script>` block doesn't need the depth-counter at all — script tags don't nest, so a plain `grep -n '<script\|</script>'` is enough to confirm lines 615–1762 directly.)

The same technique generalizes directly:
- **HTML/XML** — match `</?tag\b`, as above
- **JS/JSON objects** — match `[{}]`, `{` as +1, `}` as −1 (watch for braces inside string literals — a real parser earns its keep once this matters)
- **Function/expression bounds in code** — match `[()]` the same way

Beyond a single well-known tag/bracket type, or wherever string literals could contain lookalike characters, reach for an actual parser (`html.parser`/`BeautifulSoup` for markup, the language's own AST module for code) instead of extending the regex further. The depth-counter is a good default, not a universal one.

**Rule of thumb:** if a boundary can be found with an explicit marker — a closing comment, or a TODO anchor like the ones already present in this document's reference shell — use the marker. It's faster, and it doubles as a sanity check on the depth-counter's result.

---

## Requirements Specification for Creating a Build Map

Mirrors the base methodology's equivalent section: what must be defined before asking an AI to produce a Build Map, or the map will be systematically incomplete.

### Required Spec Elements

```markdown
1. Files in scope — every file, each with a declared role
   (SHELL / FRAGMENT / SHARED / SCOPED / ORCHESTRATOR)

2. Direction — MERGE / SPLIT / REORGANIZE / EXTRACT, and the destination file(s)

3. Criterion — the exact rule deciding a boundary
   (e.g. "one file per <section>", "one file per tab-pane id",
   "anything consumed by ≥2 fragments becomes shared")

4. Operation vocabulary — EXTRACT / INSERT / MERGE / SPLIT / DEDUPE / RELINK /
   RENAME_FOR_COLLISION / REORDER

5. Risk scale — what counts as CRITICAL / HIGH / MEDIUM / LOW for this task

6. JSON schema — exact structure for both `operations` and `reference_registry`

7. Rules for operation ids — format, numbering

8. Reference-type taxonomy — which kinds of pointers count
   (id, class, href, src, import, css-variable, data-attribute pairing, aria-* pairing…)

9. Context-field requirements — verbatim snippet length cap (≤120 chars, same as base)

10. What is explicitly NOT in scope — e.g. "rename nothing except to resolve a
    collision the merge itself creates" (naming-convention cleanup is the base
    methodology's job, run as a separate pass if needed); and which discovered
    dangling references belong to a different task (see the profile-details note above)
```

### Spec Improvements Over a Naive Approach

| Naive Spec Problem | Solution |
|---|---|
| "Just combine these files" | Explicit direction + destination file name(s) |
| No stated criterion | A criterion precise enough that a second person draws the same boundaries |
| Boundaries described in prose ("the messages part") | Exact line ranges, confirmed via tag-balance, not eyeballed |
| No reference registry | Every id/class/href/src cross-checked, not just the ones that happen to get noticed |
| Collisions found during execution | Found in 1.3, resolved in the map — before a single byte moves |
| "Looks right" as the validation bar | grep-counted reference resolution + hash-matched content preservation |
| Fragment filename assumed to match its destination anchor | Confirmed explicitly — filenames and anchor ids don't have to agree, and often don't |
| A dangling reference assumed to be an error | Checked against scope first — it may be a different task's placeholder, not a bug in this one |

---

## Templates for Common Task Types

### Merge Fragments into a Shell (Many → One)

```
Phase 0: confirm shell + fragment list + shared/scoped resources + destination
Phase 1: role-classify every file; scan (not read) each fragment for its payload
         boundary; build the full reference graph across shell + fragments + resources
Phase 2: Build Map — one EXTRACT_INSERT per fragment's markup, one EXTRACT per
         fragment's scoped script/style, one DEDUPE per shared-resource conflict,
         RENAME_FOR_COLLISION for any name shared across fragments
Phase 3: plan grouped by destination: collisions/renames → shared-resource
         reconciliation → markup insertion → script extraction → style extraction
Phase 4: cut by exact range, paste verbatim, resolve collisions atomically,
         validate after each fragment lands
Phase 5: hash-match every moved block, grep-count every reference, tag-balance
         the final file
```

### Split a Monolith by Criteria (One → Many)

```
Phase 0: confirm the source monolith + the split criterion + destination naming pattern
Phase 1: find every boundary matching the criterion (tag-balance or marker-confirmed,
         not guessed); decide what stays in the remaining shell vs. becomes its own
         file; identify which shared resources each new file needs to carry to stay
         independently valid, if that's a requirement
Phase 2: Build Map — one SPLIT (⇒ N EXTRACTs) per boundary match; an ANCHOR/placeholder
         operation for what's left behind in the shell at each cut point
Phase 3: plan grouped by destination file (one group per new file produced)
Phase 4: cut by exact, verified range; leave an explicit marker at each cut point
         (never a silent gap); write only the minimum boilerplate each new file needs
Phase 5: round-trip check — do the shell + new files together reconstruct the
         original's observable content/behavior, modulo the intended cleanup?
```

This is the direction to reach for on a file like this document's 2,744-line, 210KB `customer-account-1e.html` — a bloated monolith that the same tab-pane-boundary criterion used above for MERGE would decompose, run in reverse.

### Extract a Shared Resource and Relink Consumers

```
Phase 0: confirm which resource is suspected duplicated/near-duplicated, and across
         which consumers
Phase 1: diff every occurrence against the others *before* assuming they're
         identical — a byte-for-byte duplicate and a "looks similar" duplicate
         (e.g. a version mismatch) require different handling
Phase 2: Build Map — one EXTRACT for the canonical version into a new shared file;
         one DEDUPE per consumer that had its own copy; one RELINK per consumer to
         point at the new file
Phase 3: plan: canonical extraction first, then dedupe+relink each consumer, one
         at a time
Phase 4: execute; if any occurrence diverged from the "canonical" one in a way that
         mattered, surface that divergence as a decision — don't silently drop it
Phase 5: every consumer still renders/behaves as before; the shared file loads
         exactly once per consumer that needs it
```

### Reorganize by New Grouping Criteria (Many → Many)

```
Phase 0: confirm the old grouping, the new grouping, and the mapping rule between them
Phase 1: role-classify under both groupings; build the reference graph against the
         OLD structure (what exists today)
Phase 2: Build Map — treat as a SPLIT of the old grouping followed by a MERGE into
         the new one, planned together so a block extracted once lands in exactly
         one new destination, never copy-pasted into two by mistake
Phase 3: plan grouped by new destination
Phase 4: execute as one coordinated pass — the exception to "one destination at a
         time," since here a block's source and destination can both be mid-
         transition simultaneously and the full map is what keeps that safe
Phase 5: hash-match, reference-count, and round-trip — Merge's and Split's checks,
         combined
```

---

## AI Checklist Upon Receiving a Task

```
□ Have I confirmed the direction (MERGE / SPLIT / REORGANIZE / EXTRACT) and the
  exact destination file(s) — not assumed them from the file names?
□ Has every file been assigned a role before I read a single line of its content?
□ Did I scan for structure (line counts, tag markers, grep) before reading full
  content anywhere a scan would answer the question?
□ Have I built the COMPLETE reference graph — every export matched to its
  consumers, every import matched to its export, across ALL files in scope?
□ Are there any dangling references (an import with no matching export)?
□ Have I checked whether a dangling reference belongs to a DIFFERENT, not-yet-
  started task rather than assuming it's this pass's bug to fix?
□ Are there any id/name collisions that only become real once files share a
  namespace — even if no single source file looks broken on its own?
□ Does the map contain exact line ranges and exact destination anchors — never
  "somewhere in file X" or "near the top"?
□ Have I confirmed each fragment's destination explicitly, rather than assuming
  its filename matches the target anchor?
□ Are collisions and shared-resource conflicts resolved in the map BEFORE any
  content depending on them gets inserted?
□ Is validation planned after each destination, not deferred to the end?
□ Can I PROVE content wasn't silently altered in transit (hash/diff), rather than
  just stating it "looks right"?
□ For a split: would re-analyzing my own output reproduce the same boundaries
  I started from?
```

---

## Anti-Patterns

### ❌ Reading Full Files When a Structural Scan Would Answer the Question

```
Bad:  cat the entire 1,770-line fragment to find one section
Good: grep -n 'class="messages-container' first, then read only lines 289–576
```

Reason: the map only needs boundaries and identifiers until the moment of actual extraction. Reading everything up front spends tokens on content that, for most of the file, is never looked at again.

### ❌ Retyping Content From Memory Instead of Extracting It

```
Bad:  read a fragment, hold it in mind, "reproduce" it in the destination
Good: cut the exact recorded line range and paste it verbatim
```

Reason: reproduction from memory isn't deterministic — an attribute, a modifier class, a data value can silently drift. A range-copy is either exactly right or mechanically checkable; a memory-copy usually *looks* fine either way, which is what makes it risky.

### ❌ Merging Before Resolving Collisions

```
Bad:  paste all fragments in, then notice two of them both defined id="filter-btn"
Good: build the full reference graph first; resolve every collision in the map;
      only then execute
```

Reason: a collision found after the merge means editing content that's already moved and possibly already referenced elsewhere — strictly more work than catching it in 1.3.

### ❌ Forgetting to Reconcile Shared/Global Resources

```
Bad:  the destination loads Bootstrap three times because each fragment was
      previously its own standalone page with its own <head>
Good: shared resources are identified in the inventory and reconciled — including
      checking that "duplicates" are actually identical, not just similar-looking —
      as their own operation
```

Reason: two links that look like the same library can point at two different versions — or, as with this shell's own `<link>` tags, at two different *path conventions* for what's presumably the same local asset folder (`file:///C:/GitHub/bsshtml/assets/...` at line 30 vs. relative `../../../assets/...` from line 595 on). Dropping a "duplicate" without checking is a silent downgrade, upgrade, or broken path — not a cleanup.

### ❌ Guessing Split/Merge Boundaries Instead of Matching Them

```
Bad:  "split roughly around line 800"
Good: split at the exact tag-balanced or marker-confirmed boundary
```

Reason: nested tags make an eyeballed boundary a coin flip past one level of nesting. The depth-counting approach costs one script; a mis-cut block costs a debugging session.

### ❌ Assuming a Fragment's Filename Matches Its Destination Anchor

```
Bad:  assume account-messages-1b.html must map to id="tab-messages"
Good: confirm the actual mapping — here it's id="tab-correspondence"
```

Reason: naming drifts between when a component was built and where it ends up living. An assumed mapping fails silently if the wrong anchor happens to also exist in the shell.

### ❌ Validating Only by Reading the Result

```
Bad:  skim the merged file — it "looks fine"
Good: grep-count every reference, hash-compare every moved block, tag-balance
      the whole file
```

Reason: a page can render correctly in isolation while still containing a duplicate id, a dangling `aria-labelledby`, or a subtly altered attribute that only breaks under one specific interaction. Visual inspection catches what looks wrong; it doesn't catch what's structurally wrong but currently silent.

---

## Working with Many Files (Token Discipline)

This section exists because build tasks tend to touch more files, and larger ones, than a single-spec refactor does.

**Default posture: scan first, always.**

```bash
wc -l *.html *.css *.js                                     # size, in one call
grep -c '<!DOCTYPE' *.html                                    # which are full documents
grep -n -oE 'id="[a-zA-Z0-9_-]+"' file.html | sort -u          # exports
grep -n -E '<link|<script src|@import' file.html               # imports
```

**Read the full content of a range only when it's about to be extracted or inserted** — not before, and not "just in case."

**Decision tree for when a full read is actually justified:**

```
Is the file under ~150 lines / ~8KB?
  → yes: a full read costs less than several rounds of scanning. Just read it.
  → no: continue

Can every boundary you need be found by a marker or a tag-balance check?
  → yes: scan for boundaries, read only the ranges you'll actually move
  → no: continue

Does understanding the move require understanding embedded logic — a <script>
whose behavior could reach outside its own subtree, or config referenced
conditionally?
  → yes: a full read of that specific piece is justified — scoped to it, not
    the whole file
  → no: you're probably about to over-read; scan again before giving up
```

**Batch structural queries across the whole file set, not one file at a time** — the same way the base methodology batches pattern replacements:

```bash
for f in *.html; do echo "=== $f ==="; grep -c 'id="' "$f"; done
```

is one round-trip; five separate single-file greps are five.

---

## Execution Quality Metrics

### After Completing the Work, Ask Yourself:

```
1. Does the number of planned operations equal the number completed AND verified
   (not just completed)?
2. Does every entry in the reference registry resolve to exactly the expected
   count in the final output — zero dangling, zero unintended duplicates?
3. Does a hash or diff check confirm every EXTRACT_INSERT preserved its content
   exactly, apart from changes explicitly listed as intentional?
4. Is every shared/global resource loaded exactly once in the final output — and
   confirmed to be the same version everywhere it was reconciled?
5. Were all naming collisions resolved before the merge, with the rename applied
   to 100% of that name's consumers?
6. Does the destination pass a basic structural check — balanced tags, valid
   JSON/CSS/JS syntax?
7. For a split: does reassembling the outputs reproduce the original's observable
   content/behavior, modulo the intentional cleanup?
```

### Numerical Indicators

Record before and after:
- Number of source files, number of destination files
- Total lines/bytes before vs. after (should reconcile: after ≈ before + intentional
  additions − discarded boilerplate − deduped duplicates)
- Number of entries in the reference registry, and how many resolved vs. dangling
- Number of collisions found, and number resolved
- Number of shared-resource conflicts found (including version mismatches), and
  how each was decided

---

*This methodology is a companion to `ai-task-execution-methodology.md`, scoped to tasks where files are restructured across boundaries — merged, split, or reorganized — rather than edited in place under a fixed spec. Its worked examples reference a representative case: a 14-tab account-page shell (with existing `data-target`/TODO-anchored markup placeholders and pre-declared but dangling per-tab `<script src>` references) plus four independently-built tab fragments — each its own full HTML document with embedded styles and scripts — to be combined into one page, alongside a shared page stylesheet, per-tab stylesheets, and a hash-routed JS controller, all of which have to stay wired up correctly once the pieces share one DOM.*
