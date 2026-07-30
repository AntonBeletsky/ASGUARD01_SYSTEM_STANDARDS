# AI Task Execution Methodology — Build Protocol
## A Compositional Model of Build Dependencies: Six Dimensions, Two Qualifiers, One Standing Rule

*Version 1b. Following `1a` in sequence, per `version-control-1b.md`'s own convention — prefix `ai-task-execution-methodology-build-`, version token `1b`.*

---

## What Changed from v1a

v1a organized dependencies into eleven named types (A1–E2), grouped under five headings. Auditing that list against a domain it wasn't built from — a quick pass against database-migration files — surfaced a structural problem: **enforcement** (whether some mechanism actually checks a dependency, or it's convention-only) was only modeled as a special case of naming (Types B1 vs. B2), when it plainly applies just as much to ordering, boundaries, and containment. A list that has to grow every time a new domain reveals a new combination isn't a taxonomy — it's a work-in-progress inventory with a closed-looking table drawn around it.

v1b replaces the eleven-item list with **six dimensions and two cross-cutting qualifiers**. Instead of "which of eleven boxes does this fit," the question becomes "which dimension(s) does this touch, and how is each qualified" — a compositional question with a small, fixed vocabulary, rather than a matching question against a list that can never prove itself complete.

Two quick re-checks, done before committing to this structure:
- **Database migrations** — `up()`/`down()` pairing maps cleanly to Lifecycle (Completeness); migration-number uniqueness to Cardinality; table/column references to Name; migration order to Position (Sequence); version numbers to Generation. A plausible fit for five of six, without forcing anything.
- **Infrastructure-as-code (Terraform-style)** — module nesting and apply-order to Position; resource references to Name (compiler-checked); variable precedence (`tfvars` → CLI flags → environment) to Value (Explicit-Layered); provider/state versions to Generation; and, notably, **module output boundaries are actually enforced** by the tool itself — a live example of Boundary being `CHECKED` rather than convention-only, which neither original case study demonstrated.

Both are quick conceptual checks, not full worked case studies — they're evidence the compositional model transfers further than the enumerative one did, not proof it's complete. Nothing claims completeness here; see the *Catalog of Observed Patterns* below for why that claim is deliberately never made.

---

## Relationship to Other Documents in This System

`ai-task-execution-methodology.md` covers tasks where the file set is fixed and the work brings *content* into compliance with a spec. This document covers the other half: tasks where **the file set itself changes shape** — merged, split, or regrouped under a different boundary than the one it currently has.

Both documents share the same skeleton — Context Loading → Analysis → Map → Plan → Execution → Validation — and the same rule: **analysis, planning, and execution are separate stages, never interleaved.**

Three illustrative sources ground this document, none of them the point:
- **Case Study A** — an HTML/CSS/JS page assembled from independently-built tab fragments.
- **Case Study B** — a widget/orchestrator component system, from `containerization-11.md` and `containerization-orchestration-2.md`.
- **Case Study C** — a filename version-token parsing problem, from `version-control-1b.md`.

The **Dependency Model** and the **General Domino Algorithm** are the subject. The case studies, and the *Catalog of Observed Patterns*, are evidence the model works and aids to recognition — not the boundary of where it applies. See *Applying This to an Unfamiliar Domain* for how to use this on something none of the three resembles.

**Composability with the base methodology:** run the two in sequence, never simultaneously. Don't rename something *while* moving it unless the rename is strictly required to resolve a collision the move itself creates.

---

## Philosophy

```
ANALYSIS → MAP → EXECUTION → VALIDATION
```

Mixing stages causes most errors. A build task fails in a specific way when they're mixed: content gets pasted before every destination is confirmed, dependencies get assumed intact before they're checked, and by the time something breaks, several units are already half-rewritten with no clean way to tell which copy is authoritative.

**A unit's full content is not needed to plan where it goes. It's only needed to actually move it.** Loading, analysis, and mapping can and should be done from *structure* — line counts, boundaries, identifiers — not from holding a whole file's body in context. A fragment's full content only needs to enter context at the moment it's being extracted and placed, ideally as a mechanical range-copy rather than something read, held in mind, and retyped.

The other half of getting this right is knowing **what to check**, not just how to copy. That's what the model below is for — but a model only earns the word "conceptual" if it's built from a small number of orthogonal questions rather than a long list of things someone happened to notice. That distinction is the entire difference between v1a and v1b.

---

## The Dependency Model

### 1. Directions

```
MERGE        many units  →  one unit        (assemble many into one)
SPLIT        one unit    →  many units      (disassemble by some criterion)
REORGANIZE   many units  →  many units       (re-grouped differently than before)
EXTRACT      part of N units → one new shared unit, N units updated to reference it
```

### 2. Unit Roles

A **unit** is whatever the smallest thing is that can be moved, renamed, merged, or deleted on its own in the domain at hand.

| Role | Definition |
|---|---|
| **SHELL / CONTAINER** | Outer skeleton, the slots units drop into |
| **FRAGMENT / MODULE** | Bounded, self-contained content to move/merge/split |
| **SHARED RESOURCE** | Consumed by more than one fragment, or by the shell |
| **SCOPED RESOURCE** | Belongs to exactly one fragment |
| **ORCHESTRATOR** | Runtime glue wiring the shell to fragments |
| **ANCHOR** | Not a unit — a *location* where a fragment is meant to land |

### 3. Six Dimensions

A **build dependency** is any relationship between two units such that moving, renaming, duplicating, or removing one requires checking or updating the other to preserve correctness. Every dependency touches one or more of six dimensions — what can possibly be at stake — each optionally qualified by *how strictly* it's held (see §4).

#### POSITION — does correctness depend on where a unit sits, structurally?

Two modes:
- **NESTING** — must be inside/outside a given boundary
- **SEQUENCE** — must come before/after another unit, independent of any explicit reference

*Detect:* find the unit's current structural position — containment depth, or relative order in a list/build-stage/cascade. *Domino:* moving the unit changes its position; anything relying on the *old* position (nesting-based inheritance, order-based override) now gets a different answer, often silently. *Validate:* re-derive the position-dependent effect after the move and confirm it matches intent.

*Example (NESTING):* a modal must stay inside its widget's container (`containerization-11.md` §2.3) — moving it out breaks token inheritance and CSS scoping. *Example (SEQUENCE):* "destroy child widgets first — remove the orchestrator's own listeners last" (`containerization-orchestration-2.md` §3); CSS cascade order, where a later duplicate rule silently wins.

#### NAME — does one unit refer to another by a shared identifier?

*Detect:* grep the identifier across the *whole* unit set, not just visually nearby files. *Domino:* renaming, duplicating, or removing the named unit breaks every consumer of that name. *Validate:* type-appropriate to the Enforcement qualifier (below) — grep-count if `CHECKED`, an explicit two-column diff of every "emits" against every "listens for" if `CONVENTION_ONLY`.

*Example:* `data-target="tab-x"` ↔ `id="tab-x"`. `document.dispatchEvent(new CustomEvent('cart:item-added', ...))` ↔ `document.addEventListener('cart:item-added', ...)` — the entire premise of `containerization-11.md`'s Law Zero is that this kind of pairing resolves through data attributes and classes, and nothing else.

#### VALUE — where does a unit's effective value actually come from?

Two modes:
- **IMPLICIT-CASCADE** — value flows via containment/scope, typically with a fallback
- **EXPLICIT-LAYERED** — value is the merge of named sources in a stated precedence order

*Detect:* fallback syntax (`var(--x, default)`) or cascade-aware constructs (IMPLICIT); a documented resolution chain, e.g. "rightmost wins" (EXPLICIT) — enumerate every source currently contributing. *Domino:* moving a unit across a cascade boundary silently swaps which source wins (IMPLICIT); stripping or duplicating one layer during a build op silently changes the resolved value (EXPLICIT) — in both cases with no error. *Validate:* resolve the chain explicitly before and after the operation; confirm the effective value is unchanged unless the change was intentional.

*Example (IMPLICIT):* `.cart-container { --cart-radius: var(--checkout-radius, .5rem); }` — extracted onto a page with no `.checkout-page` ancestor, it silently falls back to `.5rem`. *Example (EXPLICIT):* the three-layer config system, `DEFAULTS → opts → data-attributes`, rightmost wins (`containerization-11.md` §4.2) — dropping a fragment's `data-orders-delay="500"` while lifting its markup silently reverts the effective delay to whatever the next layer provides.

#### LIFECYCLE — is there a create/destroy pairing, and what must it preserve?

Two modes:
- **IDENTITY** — two things must share the *literal same* handle/instance, not a lookalike
- **COMPLETENESS** — every created thing must be matched by a teardown; the cascade must be exhaustive

*Detect:* trace creation sites vs. consumption sites (IDENTITY); trace construct-time registrations vs. teardown-time calls (COMPLETENESS). *Domino:* a split that accidentally creates a second instance where the original should have been reused breaks IDENTITY; a new child added without wiring its teardown breaks COMPLETENESS — invisible, since nothing references it *incorrectly*, it's simply never referenced at teardown time. *Validate:* identity check (same object, one documented creation site) or a list-diff (construct-time list vs. teardown-time list).

*Example (IDENTITY):* `this._ac = new AbortController()`, created once; every listener must pass `{ signal: this._ac.signal }` — one `destroy()` call must remove every listener; a helper that creates its own `AbortController` breaks this silently. *Example (COMPLETENESS):* `CheckoutPageController.destroy()` explicitly calls `this._cart?.destroy(); this._summary?.destroy(); this._promo?.destroy();` — a fourth widget added later without a matching line is an orphaned child.

#### BOUNDARY — is a reference *allowed* to exist, given the architecture's layering?

Not "does it resolve" but "is it permitted," tied to structural depth.

*Detect:* identify each unit's declared public surface vs. internal state, and its declared nesting depth. *Domino:* changing nesting depth — flattening two levels, adding an intermediate one — can flip a call from legal to illegal, or the reverse, with the call site's own code completely unchanged. *Validate:* after any REORGANIZE that changes nesting, re-audit every cross-unit call against the *new* depth, not the old one.

*Example:* "a parent orchestrator calls public methods on its direct child orchestrator... it never bypasses it to call methods on the child's internal widgets" — `this._ordersPanel.applySize(size)` legal, `this._ordersPanel._filters.setSize(size)` illegal (`containerization-orchestration-2.md` §6, §9.4). Contrast: a Terraform module's outputs are the *only* way to expose a value — reaching into a submodule's internal resource from outside is a real error the tool itself throws, not just a discipline problem.

#### GENERATION — is content tagged with a version/generation marker?

*Detect:* parse the marker per the project's own rule (see *Precise Pattern Matching* §2); confirm the rule for where it may legally appear. *Domino:* copying a fragment's content verbatim risks also copying its marker into a place the project forbids; merging fragments of meaningfully different generations may reintroduce stale content. *Validate:* confirm the output's marker follows the project's increment rule; confirm no source's marker leaked into a destination's body.

*Example:* `version-control-1b.md` Rule 2 — "the version suffix lives only in the filename — never inside the file content." Copying a fragment's body into a merged file must not carry a stray version string into that file's prose.

### 4. Two Cross-Cutting Qualifiers

These are not a seventh and eighth dimension — they *modify* a finding in any of the six above. This is the direct fix for what v1a got wrong: enforcement was baked into one dimension (naming) instead of being asked of all six.

#### Enforcement

- **CHECKED** — some structural artifact (compiler, schema, DOM API, runtime, resolver) will at least partly flag a violation
- **CONVENTION_ONLY** — nothing checks it; a mismatch produces silence, not an error

Applies to every dimension, not just Name:

```
POSITION  — a bundler's module resolver throws on a broken relative path (CHECKED);
            "tests live next to their module" is enforced by nobody (CONVENTION_ONLY)
NAME      — an id/data-target pair the DOM can be queried against (CHECKED, weakly —
            HTML tolerates duplicate ids, a validator catches it, the browser doesn't);
            a custom-event name (CONVENTION_ONLY, no artifact at all)
BOUNDARY  — a Terraform module output (CHECKED, the tool errors); an underscore-
            prefixed "private" method in vanilla JS (CONVENTION_ONLY)
```

**Caveat: enforcement is a spectrum, not strictly binary.** CSS cascade order is a good case of *both at once* — the browser deterministically *applies* the rule (the mechanism is enforced), but nothing stops a developer from silently invalidating their own assumption about what that order currently produces by reordering the stylesheet (relying on it correctly is convention-only). When a finding straddles this line, say so explicitly rather than forcing one label.

#### Cardinality

- **EXACTLY_ONE** — must exist, and be unique, within its scope
- **AT_MOST_ONE** — may or may not exist, but if it does, must be unique
- **MANY_OK** — no uniqueness constraint at all

**Standing Rule — recompute relative to the scope *after* the operation, not before.** Cardinality and Boundary findings are frequently scope-relative: fine while two units are separate, real only once a MERGE places them in the same scope, or once a REORGANIZE changes nesting depth. A finding that was safe pre-operation must be re-derived against the *new* scope — never assumed to still hold from the old one.

### 5. Composing a Descriptor

A dependency's full description is `{dimension, mode (if applicable), enforcement, cardinality (if applicable)}` — not a single code. This is what a v1a-style label like "B3" was quietly collapsing:

```
Finding: five references to "the same" shared library, at two different versions
  dimension:   NAME        — they're all claiming to be "the" bootstrap include
  + dimension: GENERATION  — but at two different generations (5.3.3 vs 5.3.8)
  enforcement: CONVENTION_ONLY — nothing flags the mismatch
  cardinality: EXACTLY_ONE (after merge) — must collapse to one surviving reference

This is genuinely two-dimensional. Forcing it into one v1a-style box (it was
labeled "B3 — Cardinality") hid the fact that the resolution requires answering
two different questions: which reference wins BY NAME, and which GENERATION
gets kept. A single label can't carry that; a composed descriptor can.
```

A second worked composition, showing the enforcement spectrum explicitly rather than picking one value:

```
Finding: CSS rules for the same selector defined in two merged stylesheets
  dimension:   POSITION, mode SEQUENCE — later rule in cascade order wins
  enforcement: CHECKED (the cascade mechanism itself is deterministic)
               AND CONVENTION_ONLY (nothing enforces that today's file
               concatenation order matches the author's original assumption)
  cardinality: n/a — this dimension isn't about uniqueness, it's about order
```

---

## Domino Analysis: A General Algorithm

The question is asked once **per dimension**, not once per list-item — a single change can touch Position, Name, and Cardinality simultaneously, and missing any one is a real defect.

```
INPUT: a proposed operation (move / rename / merge / split / delete) on some unit U

1. FRONTIER = { U };  CHECKED = { }
2. while FRONTIER is not empty:
     take one unit X from FRONTIER
     if X in CHECKED: continue
     add X to CHECKED
     for each dimension D in {POSITION, NAME, VALUE, LIFECYCLE, BOUNDARY, GENERATION}:
         ask D's domino question about X
         tag every answer with its Enforcement and (if applicable) Cardinality
         for each unit Y the question surfaces as newly affected:
             if Y not in CHECKED: add Y to FRONTIER
3. output: CHECKED — every unit touched, directly or transitively
4. safe to execute only once CHECKED reaches a fixed point — one full pass adds nothing new
```

This is a closure computation — the transitive closure of a graph whose edges are discovered incrementally, using the six dimensions as the edge-detection rule rather than an explicit adjacency list.

**Abbreviated trace** (renaming `.cart-container` → `.basket-container`):

```
U = the CSS class .cart-container

Iteration 1 (X = the class definition):
  NAME     — new CartController('.cart-container') in INIT also names this class
             [enforcement: CONVENTION_ONLY — a typo here fails silently].
             → add: the INIT call site.
  BOUNDARY — CheckoutPageController holds this._cart = new CartController(...); the
             constructor call is a consumer already captured under NAME. No new unit.
  VALUE    — --cart-radius is declared *under* .cart-container, not a reference to
             the class name itself. No new unit.

Iteration 2 (X = the INIT call site):
  no dimension surfaces anything new.

CHECKED = { class definition, INIT call site } → fixed point. Safe to execute.
```

---

## Applying This to an Unfamiliar Domain

The model was built from three sources — none of them the point. The same questions apply to a domain none of them resembles — a game's entity-component system, a monorepo's package boundaries, a legal document assembled from clause templates.

```
1. What is a "unit" here?
2. What is a "container / scope" here?
3. POSITION  — does correctness depend on nesting, or on relative order?
4. NAME      — do units refer to each other by shared identifiers? For each: is
               there a structural artifact that would flag a mismatch, or is it
               convention-only?
5. VALUE     — is there implicit value inheritance across containment, or an
               explicit multi-source override chain?
6. LIFECYCLE — is there a create/destroy pairing? Must anything share the
               literal same instance? Must every created thing be torn down?
7. BOUNDARY  — is there a public-vs-internal distinction tied to structural depth?
8. GENERATION — is content tagged with a version/generation marker, and where
               may that marker legally live?
9. For everything found in 3–8: what CARDINALITY applies — exactly-one,
   at-most-one, or many-ok?
```

Answering these requires reading the *new* domain's own rules (or reverse-engineering them from its files, per Phase 1 below), not a single example from this document. Once every finding is logged against its dimension and qualifiers, the General Domino Algorithm runs identically regardless of which domain produced the answers.

---

## Workflow Structure

### Phase 0 — Context Loading

Nothing gets transformed at this stage, only read and confirmed:

- **Direction** — MERGE / SPLIT / REORGANIZE / EXTRACT, and the destination unit(s)
- **Criterion** — the rule deciding where a boundary falls
- **Materials** — every unit in scope, with its declared role
- **Constraints** — anything that must not move, must stay byte-identical, or is off-limits
- **Scope boundary** — which discovered dependencies are this pass's job to resolve, and which belong to a different, not-yet-started task

```
User: here are 5 files, merge the 4 tab fragments into the shell
AI:   [reads file names + sizes, does not open content yet]
      → "5 files loaded. Direction: MERGE (4 fragments → 1 shell). Roles: shell =
         customer-account-1e-clean.html, fragments = account-{messages,mywallet,
         orders,wishlist}, shared = page.css/page.js. Confirming criterion
         before analysis."
```

**Do not assume a fragment's destination from its filename.** Confirm the mapping explicitly (see 1.1).

### Phase 1 — Analysis

#### 1.1 Classify Every Unit's Role

```
UNIT                              ROLE          STANDALONE?  SIZE    NOTES
customer-account-1e-clean.html    SHELL         yes          653 ln  14 nav links, 14 tab-panes
account-messages-1b.html          FRAGMENT      yes        1,770 ln  own <head>, own inline <script>
customer-account-page.css         SHARED        n/a              —  consumed by shell + all fragments
customer-account-page.js          ORCHESTRATOR  n/a              —  reads data-target/data-action
```

A FRAGMENT that is itself a standalone document is the most common source of wasted tokens: its actual payload is often 20–40% of its line count.

**Do not assume a fragment's filename matches its destination anchor.** `account-messages-1b.html` maps to `id="tab-correspondence"`, not `id="tab-messages"`.

#### 1.2 Build the Structural Inventory — Scan, Don't Slurp

```bash
wc -l file.html
grep -n -E '<!DOCTYPE|<head|<body|</body|</html' file.html      # full document, or bare fragment?
grep -n -oE 'id="[a-zA-Z0-9_-]+"' file.html                       # candidate NAME identifiers
grep -n -oE 'class="[^"]+"' file.html | tr ' ' '\n' | sort -u     # candidate NAME identifiers
grep -n -E '<link|<script src|@import|href=|src='  file.html     # candidate NAME imports
```

Record exact line numbers for every boundary that might become a cut point. Don't read what's between them yet.

**Full read is justified only when:** the unit is small enough that scanning costs more round-trips than reading it outright (roughly under ~150 lines / ~8KB); or no marker/tag-matching can find the boundary; or embedded logic could interact with the move in a non-obvious way and that risk needs judgment.

#### 1.3 Domino Analysis — Applying the Model

Run the *General Domino Algorithm* starting from every candidate identifier found in 1.2, checked against all six dimensions:

```
Unit: id="tab-correspondence"
  NAME [enforcement: CHECKED-ish, cardinality: EXACTLY_ONE]
    ├── shell:163  data-target="tab-correspondence"
    ├── shell:328  href="#tab-correspondence"
    └── shell:514  aria-labelledby="account-nav-tab-correspondence"  (paired reference)

Unit: <script src="customer-account-messages.js">   (shell, line 603)
  NAME [enforcement: CHECKED — a broken script src is a real, if silent, 404]
    └── no file by that name in scope; account-messages-1b.html's own inline
        <script> (lines 615–1762) is the payload waiting to fill it — DANGLING

Cardinality check across the merged scope
  NAME + GENERATION, cardinality: EXACTLY_ONE (post-merge)
    └── 0 cross-fragment id collisions found (verified); 5 competing Bootstrap
        references (2 versions, 2 path conventions) must collapse to 1

(no BOUNDARY, VALUE, or LIFECYCLE findings in this fragment — see Case Study B)
```

**Scope note:** the shell declares the same dangling-script pattern for three other fragments and one unit (`customer-account-profile-details.js`) with no matching fragment among the files provided — a Phase 0 scope question, not necessarily this pass's problem.

**Rule:** the pass must be exhaustive across all six dimensions before Phase 2 starts.

### Phase 2 — The Build Map

A JSON artifact, not prose. Two co-equal parts: what physically moves (`operations`), and what must stay wired up (`reference_registry`, tagged with a full descriptor — not a single code).

```json
{
  "meta": {
    "direction": "MERGE_MANY_TO_ONE",
    "destination_units": ["customer-account-1e-clean.html"],
    "source_fragment_units": [
      "account-messages-1b.html", "account-mywallet-1b.html",
      "account-orders-1d.html", "account-wishlist-1b.html"
    ],
    "shared_resource_units": ["customer-account-page.css", "customer-account-page.js"],
    "dimensions_in_play": ["POSITION", "NAME", "GENERATION"],
    "criterion": "one standalone preview file per tab-pane, matched to existing anchors",
    "total_operations": 13
  },
  "operations": [
    {
      "id": "build-000",
      "type": "DEDUPE",
      "descriptor": { "dimension": ["NAME", "GENERATION"], "enforcement": "CONVENTION_ONLY", "cardinality": "EXACTLY_ONE" },
      "source": { "file": "account-messages-1b.html", "lines": { "start": 8, "end": 8 },
                  "context": "<link href=\"...bootstrap@5.3.3/dist/css/bootstrap.min.css\">" },
      "destination": { "file": "customer-account-1e-clean.html",
                        "anchor": "do not carry over — shell already loads 5.3.8 at lines 32/592",
                        "lines": null },
      "depends_on": [],
      "note": "two-dimensional: same resource by NAME, different GENERATION (5.3.3 vs 5.3.8) — resolving requires deciding both which reference wins and which version is kept",
      "status": "pending"
    },
    {
      "id": "build-001",
      "type": "EXTRACT_INSERT",
      "descriptor": { "dimension": ["POSITION"], "mode": "NESTING", "enforcement": "CHECKED", "cardinality": null },
      "source": { "file": "account-messages-1b.html", "lines": { "start": 289, "end": 576 },
                  "context": "<section class=\"messages-container ...\" data-ref=\"messages-root\">" },
      "destination": { "file": "customer-account-1e-clean.html",
                        "anchor": "replace TODO comment at line 523, inside id=\"tab-correspondence\"",
                        "lines": { "start": 523, "end": 523 } },
      "depends_on": ["build-000"],
      "note": "no NAME collision found in 1.3 — fragment declares only 2 ids, neither reused elsewhere",
      "status": "pending"
    }
  ],
  "reference_registry": [
    {
      "descriptor": { "dimension": ["NAME"], "enforcement": "CHECKED", "cardinality": "EXACTLY_ONE" },
      "name": "tab-correspondence",
      "defined_in": [{ "file": "customer-account-1e-clean.html", "line": 513 }],
      "consumed_in": [
        { "file": "customer-account-1e-clean.html", "line": 163, "via": "data-target" },
        { "file": "customer-account-1e-clean.html", "line": 328, "via": "href=\"#tab-correspondence\"" },
        { "file": "customer-account-1e-clean.html", "line": 514, "via": "aria-labelledby (paired)" }
      ],
      "resolved": true
    },
    {
      "descriptor": { "dimension": ["NAME"], "enforcement": "CHECKED", "cardinality": "EXACTLY_ONE" },
      "name": "customer-account-messages.js",
      "defined_in": [],
      "consumed_in": [{ "file": "customer-account-1e-clean.html", "line": 603, "via": "<script src>" }],
      "resolved": false,
      "note": "dangling until a later operation creates the file — the shell already expects it"
    },
    {
      "descriptor": { "dimension": ["NAME", "GENERATION"], "enforcement": "CONVENTION_ONLY", "cardinality": "EXACTLY_ONE" },
      "name": "bootstrap (css+js)",
      "defined_in": [
        { "file": "customer-account-1e-clean.html", "line": 30,  "version": "unversioned, local file://" },
        { "file": "customer-account-1e-clean.html", "line": 32,  "version": "5.3.8 (CDN css)" },
        { "file": "customer-account-1e-clean.html", "line": 592, "version": "5.3.8 (CDN js)" },
        { "file": "account-messages-1b.html", "line": 8,    "version": "5.3.3 (CDN css)" },
        { "file": "account-messages-1b.html", "line": 1765, "version": "5.3.3 (CDN js)" }
      ],
      "consumed_in": [],
      "resolved": false,
      "note": "five references, two versions and two path conventions — must collapse to one, by explicit decision"
    }
  ]
}
```

#### Required Fields

| Field | Purpose |
|---|---|
| `descriptor.dimension` | A list — one or more of POSITION/NAME/VALUE/LIFECYCLE/BOUNDARY/GENERATION; often more than one, as bootstrap shows |
| `descriptor.mode` | If the dimension has modes (POSITION, VALUE, LIFECYCLE) — which one |
| `descriptor.enforcement` | CHECKED / CONVENTION_ONLY — determines which validation technique applies |
| `descriptor.cardinality` | EXACTLY_ONE / AT_MOST_ONE / MANY_OK / `null` if not applicable |
| `source.lines` | Exact range — the only part of the source that should ever be read in full |
| `destination.anchor` | The literal marker or exact insertion point |
| `depends_on` | Other operation ids that must complete first |
| `status` | `pending` / `in-progress` / `done` / `verified` — "moved" and "confirmed correctly moved" are different claims |

#### Operation Types

```
EXTRACT | INSERT | EXTRACT_INSERT | MERGE | SPLIT | DEDUPE | RELINK |
RENAME_FOR_COLLISION | REORDER
```

#### Risk Levels

```
CRITICAL — a CHECKED-enforcement dependency is actually broken, or a CONVENTION_ONLY
           one is silently mismatched, or content is lost
HIGH     — structurally wrong even though the dependency technically resolves
           (bad POSITION, a BOUNDARY violated)
MEDIUM   — redundant, not broken (a Cardinality duplicate not yet reconciled, a
           VALUE drift not yet confirmed)
LOW      — cosmetic
```

### Phase 3 — Assembly Plan

```
Destination: customer-account-1e-clean.html (group)
  ├── Collisions & renames [NAME, cardinality EXACTLY_ONE] — resolved first
  │   └── (none required — 1.3 found no cross-fragment id collisions)
  ├── Shared resource reconciliation [NAME+GENERATION] — done once, before insertion
  │   └── [ ] build-000 — bootstrap: five references collapse to one
  ├── Fragment insertion [POSITION, mode NESTING] — one item per tab, in nav order
  │   ├── [ ] build-001 — messages  → #tab-correspondence  (depends_on: build-000)
  │   ├── [ ] build-003 — mywallet  → #tab-wallet           (depends_on: build-000)
  │   ├── [ ] build-005 — orders    → #tab-orders            (depends_on: build-000)
  │   └── [ ] build-007 — wishlist  → #tab-wishlist          (depends_on: build-000)
  ├── Script extraction [NAME, resolving dangling script-src] — one per fragment
  │   └── [ ] build-002/004/006/008 — new customer-account-{name}.js per fragment
  └── Scoped CSS extraction — one per fragment with embedded <style>
      └── [ ] build-009..012 — customer-account-tab-*.css, per the tab-overview.css precedent
```

**Ordering rules:** collisions/renames first → shared-resource reconciliation next, once → fragment insertion in nav order, not numbering order → RELINK in the same step as the move it follows.

### Phase 4 — Execution

**Standing rule (execution-time):** for SPLIT/REORGANIZE, keep the original intact until Phase 5 confirms the new units reconstruct it.

**1. One destination at a time.**

**2. Extract by range, never by memory:**
```python
lines = open("account-messages-1b.html").readlines()
block = "".join(lines[288:576])          # 0-indexed slice for lines 289–576
insert_at(destination, anchor_line=523, content=block)
```

**3. Verify tag/brace balance before cutting** (see *Precise Pattern Matching*).

**4. Resolve a NAME collision (Cardinality: EXACTLY_ONE violated) and all its consumers in one operation.** A rename that only touches the definition produces a dangling reference — worse than not renaming.

**5. Reconcile shared resources (NAME+GENERATION conflicts) as one unified pass**, not once per consumer.

**6. Preserve LIFECYCLE — both modes — when splitting a class or module across files.** A helper extracted into its own file must still share the original's identity-mode handle (e.g. `AbortController`); any new child added during the build must be added to the existing completeness-mode teardown cascade.

**7. Re-audit BOUNDARY after any change in nesting depth** — a call legal before a REORGANIZE may not be legal after, with no code at the call site having changed.

**8. Validate immediately after each destination — not at the end.**

### Phase 5 — Validation

**Level 1 — Structural / Content-Preserving.** Prove, don't eyeball:
```bash
sed -n '289,576p' account-messages-1b.html | sha256sum
sed -n '523,810p' customer-account-1e-clean.html | sha256sum   # recompute after insertion
```

**Level 2 — Dependency Resolution, by Enforcement type:**
```bash
# CHECKED-style NAME dependency — grep-count
for target in $(grep -oE 'data-target="[a-z-]+"' shell.html | sort -u); do
  id_attr=$(echo "$target" | sed 's/data-target=/id=/')
  count=$(grep -c "$id_attr" shell.html)
  [ "$count" -eq 1 ] || echo "MISMATCH: $target — found $count times"
done
```
**CONVENTION_ONLY dependencies need a different technique** — there is no artifact to grep-count. List every emitted string and every listened-for string as two separate sets and diff them; a clean grep result proves nothing here.

**Level 3 — Syntax & Semantic Validity.** Tag balance across the *whole* destination. No shared resource loaded twice — confirm generations genuinely match before treating two references as one duplicate. A repeated utility class is legal (Cardinality: MANY_OK); a repeated `id` is not (EXACTLY_ONE), once merged.

**Final Report:**
```
OPERATION      SOURCE → DESTINATION                    STATUS       REFS OK   HASH MATCH
build-000      bootstrap 5.3.3 → dropped (kept 5.3.8)   ✅ VERIFIED    n/a        n/a
build-001      messages → #tab-correspondence            ✅ VERIFIED   3/3        ✅
build-002..012 scripts + scoped CSS, same shape           ✅ VERIFIED    —          ✅
```

---

## Precise Pattern Matching (Beyond Naive Regex)

### 1. Nested Boundaries (Tags, Braces)

```python
import re

def find_block_end(text, start_pos, tag="div"):
    """Given the offset of an opening <tag ...>, return the offset just past
    its matching closing </tag>. Assumes well-formed, non-self-closing nesting."""
    pattern = re.compile(rf"</?{tag}\b[^>]*>")
    depth = 0
    for m in pattern.finditer(text, start_pos):
        depth += -1 if m.group().startswith("</") else 1
        if depth == 0:
            return m.end()
    return None  # unbalanced input — a Phase 1 finding, not a Phase 4 surprise
```

Run against `account-messages-1b.html`, this finds the `<section class="messages-container">` opened at line 289 closing at line 576 — confirmed independently by the fragment's own closing comment, `<!-- /messages-container -->`. The same technique generalizes to JS/JSON objects (`{ }`) and code (`( )`). Beyond a single well-known bracket type, use an actual parser.

### 2. Version / Generation Tokens in Filenames

`version-control-1b.md` defines the version token as "the first occurrence of the pattern `<number><letter a–h>`." The prefix may itself contain digits:

```
Asguard01MediaGallery-NG-20g_-_themes.html
         ^^                ^^
     part of the prefix     the actual token: 20g
```

```python
import re

VERSION_TOKEN = re.compile(r'(\d+)([a-h])(?![a-zA-Z])')

def parse_version(filename):
    m = VERSION_TOKEN.search(filename)
    if not m:
        return None
    return {"prefix": filename[:m.start()], "number": int(m.group(1)),
             "letter": m.group(2), "rest": filename[m.end():]}
```

`01` in the prefix never matches — the character right after it is `M`, not in `[a-h]`. The trailing `(?![a-zA-Z])` is a hardening guard, not something the spec states explicitly. Verified against every example in `version-control-1b.md`, plus this document's own filename → prefix `ai-task-execution-methodology-build-`, version `1b`.

**Rule of thumb, both cases:** if a boundary can be found with an explicit marker, use the marker — faster, and it doubles as a sanity check.

---

## Requirements Specification for Creating a Build Map

```markdown
1. Units in scope — every unit, each with a declared role
2. Direction — MERGE / SPLIT / REORGANIZE / EXTRACT, and the destination unit(s)
3. Criterion — the exact rule deciding a boundary
4. Which dimensions are actually in play for this task, and their qualifiers —
   not all six apply to every domain; declare which do, and why the rest don't
5. Operation vocabulary — EXTRACT / INSERT / MERGE / SPLIT / DEDUPE / RELINK /
   RENAME_FOR_COLLISION / REORDER
6. Risk scale — what counts as CRITICAL / HIGH / MEDIUM / LOW for this task
7. JSON schema — exact structure for `operations` and `reference_registry`,
   including the {dimension, mode, enforcement, cardinality} descriptor shape
8. Rules for operation ids — format, numbering
9. Context-field requirements — verbatim snippet length cap (≤120 chars)
10. What is explicitly NOT in scope — which discovered dangling references
    belong to a different task
```

| Naive Spec Problem | Solution |
|---|---|
| "Just combine these files" | Explicit direction + destination unit name(s) |
| "Check the dependencies" | A composed descriptor per finding, not a single vague label |
| Collisions found during execution | Found in 1.3, resolved in the map — before a single byte moves |
| "Looks right" as the validation bar | Enforcement-appropriate check: grep-count for CHECKED, explicit diff for CONVENTION_ONLY |
| A dangling reference assumed to be a bug | Checked against scope first — it may be a different task's placeholder |
| One label forced onto a two-dimensional finding | `dimension` is a list — bootstrap is NAME *and* GENERATION at once |

---

## Templates for Common Task Types

### Merge Fragments into a Shell (Many → One)
```
Phase 0: confirm shell + fragment list + shared/scoped resources + destination
Phase 1: role-classify; scan each fragment for its payload boundary; run the
         Domino Algorithm across all six dimensions for shell + fragments + resources
Phase 2: Build Map — EXTRACT_INSERT per fragment's payload, DEDUPE per NAME/
         GENERATION conflict, RENAME_FOR_COLLISION for any Cardinality violation
Phase 3: plan by destination — collisions/renames → shared-resource
         reconciliation → insertion in logical order
Phase 4: cut by exact range, resolve collisions atomically, validate per fragment
Phase 5: hash-match, resolve every dimension by its enforcement type, tag-balance
```

### Split a Monolith by Criteria (One → Many)
```
Phase 0: confirm the source + the split criterion + destination naming pattern
Phase 1: find every boundary matching the criterion (tag-balance/marker-
         confirmed, not guessed); identify which shared resources each new
         unit needs to carry to stay independently valid
Phase 2: Build Map — SPLIT (⇒ N EXTRACTs) per boundary, an ANCHOR operation for
         what's left behind at each cut point
Phase 3: plan by destination unit
Phase 4: cut by exact, verified range; leave an explicit marker at each cut point
Phase 5: round-trip check — do shell + new units reconstruct the original's
         observable behavior, modulo intended cleanup?
```
This is the direction for a file like Case Study A's monolith, `customer-account-1e.html` (2,744 lines, 210KB) — decomposable by the same tab-pane criterion used above for MERGE, run in reverse.

### Extract a Shared Resource and Relink Consumers
```
Phase 0: confirm which resource is suspected duplicated, and across which consumers
Phase 1: diff every occurrence before assuming they're identical — a byte-identical
         duplicate and a different-GENERATION one require different handling
Phase 2: Build Map — EXTRACT the canonical version into a new shared unit;
         DEDUPE per consumer; RELINK per consumer to the new unit
Phase 3: plan: canonical extraction first, then dedupe+relink each consumer
Phase 4: execute; surface any divergence from "canonical" as a decision, not a
         silent drop
Phase 5: every consumer still behaves as before; the shared unit loads exactly
         once per consumer
```

### Reorganize by New Grouping Criteria (Many → Many)
```
Phase 0: confirm old grouping, new grouping, and the mapping rule between them
Phase 1: role-classify under both groupings; run the Domino Algorithm against
         the OLD structure, paying particular attention to BOUNDARY (does the
         new nesting depth change which calls are legal?)
Phase 2: Build Map — SPLIT of the old grouping followed by a MERGE into the
         new one, planned together so nothing is copy-pasted into two places
Phase 3: plan by new destination
Phase 4: execute as one coordinated pass — the exception to "one destination
         at a time"
Phase 5: hash-match, dependency-resolve, round-trip — Merge's and Split's checks combined
```

---

## AI Checklist Upon Receiving a Task

```
□ Confirmed the direction and exact destination unit(s) — not assumed from names?
□ Assigned every unit a role before reading a single line of content?
□ Scanned for structure before reading full content anywhere a scan would answer it?
□ Checked every candidate identifier against ALL SIX dimensions, not just the
  one that was obvious at a glance?
□ For every CONVENTION_ONLY finding, explicitly diffed both sides — not
  trusted the absence of an error?
□ Checked whether a dangling reference belongs to a DIFFERENT, not-yet-started
  task rather than assuming it's this pass's bug?
□ Confirmed Cardinality conflicts are resolved in the map BEFORE anything
  depending on them gets inserted?
□ Confirmed each fragment's destination explicitly, rather than assumed
  filename-to-anchor matching?
□ Preserved both LIFECYCLE modes when splitting any class or module across units?
□ Re-audited BOUNDARY findings if this operation changes nesting depth?
□ Allowed a single finding to carry MORE THAN ONE dimension, rather than
  forcing it into whichever one came to mind first?
□ Planned validation after each destination, not deferred to the end?
□ Can PROVE content wasn't silently altered in transit (hash/diff)?
□ For a split: would re-analyzing the output reproduce the same boundaries started from?
```

---

## Anti-Patterns

### ❌ Reading Full Units When a Structural Scan Would Answer the Question
```
Bad:  cat the entire 1,770-line fragment to find one section
Good: grep -n 'class="messages-container' first, read only lines 289–576
```

### ❌ Retyping Content From Memory Instead of Extracting It
```
Bad:  read a fragment, hold it in mind, "reproduce" it in the destination
Good: cut the exact recorded range and paste it verbatim
```

### ❌ Merging Before Resolving Collisions
```
Bad:  paste all fragments in, then notice two both defined id="filter-btn"
Good: run the Domino Algorithm first; resolve every Cardinality conflict in the map
```

### ❌ Forgetting to Reconcile Shared/Global Resources
```
Bad:  the destination loads a library three times, once per fragment's own <head>
Good: shared resources reconciled as their own operation — confirming
      "duplicates" are actually identical GENERATION, not just similar-looking
```

### ❌ Assuming Enforcement Is a Naming-Only Concern
```
Bad:  treat POSITION, BOUNDARY, and LIFECYCLE findings as automatically safe
      because "nothing throws an error" for those the way it might for a
      broken import path
Good: ask Enforcement of every dimension explicitly — a BOUNDARY violation in
      vanilla JS is exactly as silent as a mismatched event name
```
Reason: this is the specific mistake v1a made — modeling enforcement as a property of one dimension instead of a question asked of all six. It's listed here because the failure is easy to reintroduce even after reading the fix.

### ❌ Treating a Convention-Only Contract as if It Were Enforced
```
Bad:  assume two matching-sounding event names are fine because nothing threw
Good: list every emitted name and every listened-for name side by side and diff them
```

### ❌ Bypassing a BOUNDARY to Save a Step
```
Bad:  this._ordersPanel._filters.setSize(size) — reaching past the child orchestrator
Good: this._ordersPanel.applySize(size) — calling its public method
```
Reason: legal today doesn't mean legal after the next REORGANIZE.

### ❌ Guessing Boundaries Instead of Matching Them
```
Bad:  "split roughly around line 800"
Good: split at the exact tag-balanced or marker-confirmed boundary
```

### ❌ Assuming a Fragment's Filename Matches Its Destination Anchor
```
Bad:  assume account-messages-1b.html must map to id="tab-messages"
Good: confirm the actual mapping — here it's id="tab-correspondence"
```

### ❌ Validating Only by Reading the Result
```
Bad:  skim the merged file — it "looks fine"
Good: grep-count CHECKED dependencies, diff CONVENTION_ONLY pairs, hash-compare
      moved blocks, tag-balance the whole file
```

---

## Case Studies

### Case Study A — HTML/CSS/JS Tab-Fragment Merge

One shell (653 lines, 14 tab-panes) absorbing four standalone tab-preview files (1,133–1,770 lines each). Full worked example threaded through *Workflow Structure*, above.

| Dimension(s) | Where it showed up |
|---|---|
| POSITION (Nesting) | Tab-pane boundaries, TODO anchors |
| NAME | `data-target`/`id`/`aria-*` pairs; the dangling `<script src="customer-account-messages.js">` |
| NAME + GENERATION | 5 competing Bootstrap references (2 versions, 2 path conventions) collapsing to 1 |
| GENERATION alone | The fragment files carry `version-control-1b.md` suffixes (`-1b`, `-1d`) |
| VALUE / LIFECYCLE / BOUNDARY | Not present in this domain — see Case Study B |

### Case Study B — Widget/Orchestrator Assembly

Per `containerization-11.md` + `containerization-orchestration-2.md`: independently-built widgets combined under a page orchestrator. Each widget is *designed* for this from the start, so the model surfaces risks Case Study A never touches:

- **NAME, enforcement CONVENTION_ONLY** — `CartController` emits `dispatchEvent(new CustomEvent('cart:item-added', {...}))`; `CheckoutPageController` must listen for the identical string.
- **VALUE, mode IMPLICIT-CASCADE** — `.cart-container { --cart-radius: var(--checkout-radius, .5rem); }`. Assembled under `.checkout-page`, inherits the page's radius; assembled standalone, silently falls back to `.5rem`.
- **VALUE, mode EXPLICIT-LAYERED** — `DEFAULTS → opts → data-attributes`. Lifting a widget's markup without its `data-orders-*` attributes silently changes the effective config.
- **LIFECYCLE, mode IDENTITY** — every listener in a widget must share `this._ac.signal`. Splitting the class across files must not let an extracted helper create its own `AbortController`.
- **LIFECYCLE, mode COMPLETENESS** — `CheckoutPageController.destroy()` explicitly tears down `_cart`, `_summary`, `_promo`. A fourth widget added later without a matching line is orphaned.
- **BOUNDARY, enforcement CONVENTION_ONLY** — `this._ordersPanel.applySize(size)` legal; `this._ordersPanel._filters.setSize(size)` illegal. Changing nesting depth during a REORGANIZE flips which calls are allowed.

### Case Study C — Parsing a Version Token

`version-control-1b.md`'s own tricky case: `Asguard01MediaGallery-NG-20g_-_themes.html`. The prefix contains a digit run (`01`) that is *not* the version token — the actual version is `20g`. See *Precise Pattern Matching §2* for the extractor.

---

## Catalog of Observed Patterns

**A specific task's dependencies may not resemble anything below — and that is not a gap in your analysis.** This catalog records patterns seen across the three sources above. It is not a checklist to satisfy, and it will never be complete; adding a hundred more rows would still leave it incomplete. It exists to sharpen recognition, not to define a boundary. If nothing here matches what's in front of you, the correct move is not to conclude "no dependencies exist" — it's to run the nine questions in *Applying This to an Unfamiliar Domain* directly against the real units of the task. A pattern absent from this table is exactly as valid a finding as one present in it.

| Pattern | Dimension(s) | Mode | Enforcement | Cardinality | Source |
|---|---|---|---|---|---|
| Custom event name, dispatch ↔ listen | NAME | — | CONVENTION_ONLY | EXACTLY_ONE (per consumer's expectation) | Case B |
| CSS custom property with fallback | VALUE | IMPLICIT-CASCADE | mixed — see §4 caveat | — | Case B |
| `up()`/`down()` migration pair | LIFECYCLE | COMPLETENESS | usually CHECKED by the runner | EXACTLY_ONE pairing | (quick check, §"What Changed") |
| Relative import path after a file move | POSITION + NAME | NESTING | CHECKED (resolver errors) | EXACTLY_ONE | generic |
| Public-method-only call to a child orchestrator | BOUNDARY | — | CONVENTION_ONLY in vanilla JS; CHECKED in e.g. Terraform modules | — | Case B |
| Shared `AbortController` across all listeners in a class | LIFECYCLE | IDENTITY | CONVENTION_ONLY | EXACTLY_ONE (shared instance) | Case B |
| Two "same" shared library references at different versions | NAME + GENERATION | — | CONVENTION_ONLY | EXACTLY_ONE (after merge) | Case A |
| CSS cascade order, later duplicate rule wins | POSITION | SEQUENCE | mixed — see §4 caveat | — | Case A |
| Three-layer config resolution, rightmost wins | VALUE | EXPLICIT-LAYERED | CHECKED (deterministic), but silently changes if a layer is dropped | — | Case B |
| Filename version token that must not leak into file content | GENERATION | — | CONVENTION_ONLY | — | Case C |
| Two independently-built pages sharing a generic `id` | NAME | — | weakly CHECKED — a validator catches it, the browser tolerates it | EXACTLY_ONE (after merge) | Case A |
| Directory-based module resolution after a move | POSITION | NESTING | CHECKED (bundler/resolver errors) | EXACTLY_ONE | generic |

---

## Working with Many Units (Token Discipline)

**Default posture: scan first, always.**
```bash
wc -l *.html *.css *.js
grep -c '<!DOCTYPE' *.html
grep -n -oE 'id="[a-zA-Z0-9_-]+"' file.html | sort -u
grep -n -E '<link|<script src|@import' file.html
```

**Decision tree for when a full read is justified:**
```
Is the unit under ~150 lines / ~8KB?  → yes: just read it.  → no: continue
Can every boundary be found by a marker or tag-balance check?
  → yes: scan for boundaries, read only the ranges you'll move.  → no: continue
Does understanding the move require understanding embedded logic that could
reach outside its own subtree?
  → yes: a full read of that specific piece is justified, scoped to it.
  → no: you're probably about to over-read; scan again before giving up.
```

**Batch structural queries across the whole unit set:**
```bash
for f in *.html; do echo "=== $f ==="; grep -c 'id="' "$f"; done
```

---

## Execution Quality Metrics

```
1. Planned operations = completed AND verified operations?
2. Every reference-registry entry resolves to the expected count — zero
   dangling, zero unintended duplicates?
3. Hash/diff confirms every EXTRACT_INSERT preserved content exactly?
4. Every shared resource loads exactly once, confirmed same generation everywhere?
5. Every Cardinality conflict resolved before merge, rename applied to 100%
   of consumers?
6. Destination passes a basic structural check — balanced tags, valid syntax?
7. For a split: reassembling the outputs reproduces the original's behavior?
8. Every dimension declared "in play" in the map's meta has at least one
   corresponding entry in the reference registry — was the model actually
   applied, not just cited?
9. Did any finding get forced into a single dimension when it genuinely
   spanned two (as bootstrap spans NAME and GENERATION)?
```

**Numerical indicators to record before/after:** unit counts; total lines/bytes (should reconcile); reference-registry entries, resolved vs. dangling, by dimension; Cardinality conflicts found/resolved; Enforcement mix (how many CHECKED vs. CONVENTION_ONLY findings, since the latter carry more risk per finding).

---

*This methodology is a companion to `ai-task-execution-methodology.md`. Version 1b replaces v1a's eleven-item enumerative taxonomy with a compositional model — six dimensions, two cross-cutting qualifiers, one standing rule — built after auditing v1a against a domain it wasn't derived from and finding that enforcement had been modeled as a property of naming alone rather than a question askable of every dimension. The three illustrative sources (an HTML/CSS/JS page assembly, a widget/orchestrator component system per `containerization-11.md` and `containerization-orchestration-2.md`, and a version-token parsing problem per `version-control-1b.md`) remain as Case Studies and feed the Catalog of Observed Patterns — which opens, deliberately, by stating that it is not exhaustive and is not meant to be.*
