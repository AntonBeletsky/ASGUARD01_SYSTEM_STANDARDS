# AI Task Execution Methodology — Build Protocol
## A Domain-Independent Taxonomy and Execution Framework for Build Dependencies

*Version 1a. This file's own name follows `version-control-1b.md`'s convention — prefix `ai-task-execution-methodology-build-`, version token `1a` — its first lettered release.*

---

## Relationship to Other Documents in This System

`ai-task-execution-methodology.md` covers tasks where the file set is fixed and the work brings *content* into compliance with a spec — renaming, fixing violations, migrating APIs. This document covers the other half: tasks where **the file set itself changes shape** — merged, split, or regrouped under a different boundary than the one it currently has.

| | Base methodology | This methodology |
|---|---|---|
| What changes | Content inside a fixed set of files | The boundaries between units — count, location, composition |
| Unit of work | A *violation* (content that doesn't match a spec) | A *fragment* and a *dependency* (a relationship between two units that a move can break) |
| Typical verbs | rename, replace, delete | extract, insert, merge, split, dedupe, relink |
| "Domino" concept | Other occurrences of the same identifier, inside the same files | Every dependency type, checked against every unit, until no new one surfaces |
| Proof of correctness | grep for the old pattern returns zero | every dependency in the taxonomy resolves correctly; every moved byte is accounted for |

Both documents share the same skeleton — Context Loading → Analysis → Map → Plan → Execution → Validation — and the same rule: **analysis, planning, and execution are separate stages, never interleaved.**

**This document is written to be domain-independent.** Two illustrative domains ground it below:

- **Case Study A** — an HTML/CSS/JS page assembled from independently-built tab fragments (the same worked example used throughout the Workflow Structure section).
- **Case Study B** — a widget/orchestrator component system, drawn from `containerization-11.md` (the single-widget standard) and `containerization-orchestration-2.md` (how multiple widgets coexist on one page).

Neither domain is the subject. The **Dependency Taxonomy** and the **General Domino Algorithm** are the subject; the case studies are proof they work, not the boundary of where they apply. See *Applying This Taxonomy to an Unfamiliar Domain* for how to use this framework on something neither example resembles.

**Composability with the base methodology:** run the two in sequence, never simultaneously. Assemble first, then — if needed — run the base methodology's compliance pass over the result, or the reverse. Don't rename something *while* moving it unless the rename is strictly required to resolve a collision the move itself creates (`RENAME_FOR_COLLISION`, under Operation Types).

---

## Philosophy

The base methodology's rule holds without modification:

```
ANALYSIS → MAP → EXECUTION → VALIDATION
```

Mixing stages still causes most errors, but a build task fails in a specific way when they're mixed: content gets pasted before every destination for it is confirmed, dependencies get assumed intact before they're checked, and by the time something breaks, several units are already half-rewritten with no clean way to tell which copy is authoritative.

One more principle sits on top, because it's the actual reason this document exists:

**A unit's full content is not needed to plan where it goes. It's only needed to actually move it.**

Everything in Phase 0–2 — loading, analysis, mapping — can and should be done from *structure*: line counts, tag/marker boundaries, identifiers, import statements. None of that requires holding a 2,000-line file's full body in context. A fragment's full content only needs to enter context at the moment it's being extracted and placed — and even then, ideally as a mechanical range-copy rather than something read, held in mind, and retyped.

Token cost and correctness point the same direction here: reading less and copying exact ranges is both *cheaper* and *more accurate* than reading everything and reproducing it from memory.

The other half of getting this right is knowing **what to check**, not just how to copy. That is what the taxonomy below is for: a fixed, domain-independent list of the ways two pieces of a build can depend on each other, so that "did I check everything" has a checkable answer instead of being a matter of how careful you felt.

---

## Dependency Taxonomy

### 1. Directions

```
MERGE        many units  →  one unit        (assemble many into one)
SPLIT        one unit    →  many units      (disassemble by some criterion)
REORGANIZE   many units  →  many units       (re-grouped differently than before)
EXTRACT      part of N units → one new shared unit, N units updated to reference it
```

Every build task is one of these four, or a sequence of them run as separate passes.

### 2. Unit Roles

A **unit** is whatever the smallest thing is that can be moved, renamed, merged, or deleted on its own in the domain at hand — a file, a block within a file, a config section, a resource definition. Before analysis starts, every unit in scope gets exactly one role:

| Role | Definition | Case Study A | Case Study B |
|---|---|---|---|
| **SHELL / CONTAINER** | Outer skeleton, the slots units drop into | Page shell with nav + tab-panes | A page orchestrator (`.checkout-page`) |
| **FRAGMENT / MODULE** | Bounded, self-contained content to move/merge/split | A tab's standalone HTML preview | A widget (`.cart-container`) |
| **SHARED RESOURCE** | Consumed by more than one fragment, or by the shell | A page-wide CSS/JS file | A page-level CSS token, e.g. `--checkout-gap` |
| **SCOPED RESOURCE** | Belongs to exactly one fragment | A CSS file scoped to one component | A widget's own `static DEFAULTS` |
| **ORCHESTRATOR** | Runtime glue wiring the shell to fragments | JS reading `data-target`/`data-action` | `CheckoutPageController` |
| **ANCHOR** | Not a unit — a *location* where a fragment is meant to land | A TODO comment; a `<script src>` that doesn't resolve yet | An empty slot in a page layout grid |

A unit can hold more than one role if it's small — tagging exists so you know, before reading a byte of content, what kind of thing you're looking for.

### 3. Dependency Types

A **build dependency** is any relationship between two units such that moving, renaming, duplicating, or removing one requires checking or updating the other to preserve correctness. Eleven types cover the space, in five groups.

#### Quick reference

| # | Type | One-line definition | What silent failure looks like |
|---|---|---|---|
| A1 | Containment | B must physically live inside A | Cascade/scoping breaks after a move |
| A2 | Order / Sequence | A before B, with no explicit link | Behavior changes though every reference still resolves |
| B1 | Nominal Reference (checkable) | A names B; some artifact can confirm the match | Dangling reference — at least partly detectable |
| B2 | Nominal Contract (unenforced) | A names B; nothing checks the match | Total silence — no error, no warning, nothing |
| B3 | Cardinality / Uniqueness | B must be unique within its scope | Collision only after a merge changes the scope |
| C1 | Inheritance / Cascade | B receives a value from A implicitly | Silent fallback-value swap |
| C2 | Layered Override | Effective value = ordered merge of sources | Value silently changes to a different layer's |
| D1 | Shared-Instance / Identity | Must be the *same* object, not a lookalike | Coordination (usually teardown) silently stops working |
| D2 | Lifecycle-Cascade Completeness | Every created child must be torn down | Orphaned child — leaks silently |
| E1 | Encapsulation Boundary | Reference must respect a layering rule | Legal/illegal flips when nesting depth changes |
| E2 | Version / Generation | Content is tagged with a generation marker | Marker leaks into content, or a stale generation gets merged in |

A single change is often more than one type at once — check a unit against **all eleven**, not just the one that's obvious at a glance.

#### Group A — Structural

**A1. Containment**
- *Definition:* B must physically reside inside A's boundary to function or scope correctly.
- *Detect:* confirm B's current location is inside A's boundary (see *Precise Pattern Matching*).
- *Domino:* moving B outside A — or A away from B — breaks whatever A provides purely by nesting: inherited tokens, ancestor-scoped selectors, directory-relative resolution.
- *Validate:* after any move, re-confirm containment holds (or no longer holds, if that was the intent).
- *Example:* a modal must stay inside its widget's container (`containerization-11.md` §2.3) — moving it out breaks token inheritance and CSS scoping. A tab's markup must land inside the matching `tab-pane` div.

**A2. Order / Sequence**
- *Definition:* A must be processed, loaded, built, or run before B, for reasons independent of any explicit reference.
- *Detect:* look for procedural rules stated separately from the reference graph — cascade order, build stages, teardown order.
- *Domino:* relocating a block can silently change relative order even though every reference still resolves — nothing breaks structurally, effective behavior changes.
- *Validate:* after any reorder, explicitly re-check relative order against every order-sensitive rule, not just existence.
- *Example:* "destroy child widgets first — they remove their own listeners — remove the orchestrator's own listeners last" (`containerization-orchestration-2.md` §3). CSS cascade order, where a later duplicate rule silently wins.

#### Group B — Referential

**B1. Nominal Reference (structurally checkable)**
- *Definition:* A names B by an identifier, and some structural artifact — a DOM API, a schema, a compiler — can at least partly confirm whether the name resolves.
- *Detect:* grep the identifier across the *whole* unit set, not just visually nearby files.
- *Domino:* renaming, duplicating, or removing B breaks every A that names it.
- *Validate:* grep-count; the expected count is domain-specific (usually exactly one, unless the domain explicitly permits many-to-one).
- *Example:* `data-target="tab-x"` ↔ `id="tab-x"`. `new OrdersController('.orders-container')` ↔ the `.orders-container` class existing in HTML — the entire premise of Law Zero (`containerization-11.md`) is that this pairing resolves through data attributes and classes and nothing else.

**B2. Nominal Contract (convention-only, unenforced)**
- *Definition:* the same shape as B1 — a shared name — but nothing checks it. No schema, no DOM API, no compiler. A mismatch produces total silence, not an error.
- *Detect:* there is no artifact to grep for "does this resolve." Find *both* sides — every emit-like call and every listen-like call — and confirm the literal strings match, character for character.
- *Domino:* this is the single most dangerous category for a build task, because a merge/split/refactor that touches either side leaves no trace of having broken anything.
- *Validate:* an explicit two-column diff — every emitted name against every listened-for name. Treat a mismatch as CRITICAL even though nothing throws.
- *Example:* `document.dispatchEvent(new CustomEvent('cart:item-added', ...))` in one widget's file; `document.addEventListener('cart:item-added', ...)` in the orchestrator's (`containerization-orchestration-2.md` §7). Nothing links these two strings except convention.

**B3. Cardinality / Uniqueness**
- *Definition:* the flip side of B1/B2 — an identifier must occur exactly once (or at most once) within its effective scope.
- *Detect:* grep-count the identifier within whatever scope currently applies.
- *Domino:* cardinality constraints are frequently scope-*relative* — fine while two units are separate, become violations only once a MERGE places them in the same scope.
- *Validate:* after any MERGE/REORGANIZE, recompute every identifier's count in the *new* combined scope, not the old separate ones.
- *Example:* two independently-built widgets each using a generic `id="modal-title"` — legal in isolation, a collision the moment both share one page. This is exactly why `containerization-11.md` §7.3 mandates every `id` carry the widget's full-word prefix. Also: several `<link>`/`<script>` tags all claiming to be "the" copy of the same library, at different versions — must collapse to one.

#### Group C — Value Resolution

**C1. Inheritance / Cascade**
- *Definition:* B receives a value from A implicitly, via a scoping/cascade mechanism, without an explicit reference — the connection is positional, not nominal.
- *Detect:* look for fallback syntax (`var(--x, default)`) or documentation stating "children inherit automatically."
- *Domino:* moving B outside A's scope silently swaps which source wins — the inherited value vs. the hardcoded fallback — invisible precisely *because* the fallback exists and prevents an outright break.
- *Validate:* for every fallback-style default found, confirm whether the pre-move resolved value actually came from the parent or the fallback, and re-confirm post-move.
- *Example:* `.cart-container { --cart-radius: var(--checkout-radius, .5rem); }` (`containerization-orchestration-2.md` §2). Extracting the cart widget onto a page with no `.checkout-page` ancestor silently swaps the radius from the page's token to the hardcoded `.5rem`.

**C2. Layered Override / Precedence**
- *Definition:* the effective value of a setting is the result of merging multiple explicit sources in a fixed precedence order.
- *Detect:* look for a documented resolution chain ("rightmost wins") and enumerate every source currently contributing a value.
- *Domino:* relocating, stripping, or duplicating any one layer during a build operation can silently change the effective value to a *different* layer's, with no error.
- *Validate:* resolve the chain explicitly before and after the operation; confirm the effective value is unchanged unless the change was intentional.
- *Example:* the three-layer config system — `static DEFAULTS → opts → _readDataAttrs()`, rightmost wins (`containerization-11.md` §4.2). If a merge drops a fragment's `data-orders-delay="500"` attribute while lifting its markup, the effective delay silently reverts to whatever `opts`/`DEFAULTS` provides.

#### Group D — Runtime Lifecycle

**D1. Shared-Instance / Identity**
- *Definition:* multiple pieces of code must hold a reference to the *literally same* runtime object — not an equivalent one — for coordinated behavior to work.
- *Detect:* trace every creation site vs. every consumption site; confirm they all point at one creation, not several.
- *Domino:* splitting a class across files, or refactoring a constructor, can accidentally cause a second instance to be created where the original should have been reused — the code still runs, coordination silently breaks.
- *Validate:* confirm, by identity (a single documented creation site), that every consumer holds the *same* instance.
- *Example:* `this._ac = new AbortController()`, created once; every `addEventListener` in the class must pass `{ signal: this._ac.signal }` (`containerization-11.md` §4.8). One `destroy()` call must remove every listener — a helper method that creates its own local `AbortController` breaks this silently (an anti-pattern the spec calls out explicitly).

**D2. Lifecycle-Cascade Completeness**
- *Definition:* a parent's init/teardown procedure must reach *every* child it created — an exhaustive cascade, not a partial one.
- *Detect:* for every construct-time registration, confirm a matching teardown call exists in the parent's own teardown method.
- *Domino:* adding a new child during a build/merge task without wiring its teardown into the existing cascade leaves it permanently un-torn-down — invisible, because nothing references it *incorrectly*, it's simply never referenced at teardown time.
- *Validate:* build the construct-time list and the teardown-time list independently, then diff them.
- *Example:* `CheckoutPageController.destroy()` explicitly calls `this._cart?.destroy(); this._summary?.destroy(); this._promo?.destroy();` (`containerization-orchestration-2.md` §3). Adding a fourth widget without adding its `destroy()` call here is exactly this failure.

#### Group E — Boundary & Meta

**E1. Encapsulation Boundary / API Surface**
- *Definition:* not "does a reference resolve" but "is this reference *allowed* to exist," given the architecture's layering rules.
- *Detect:* identify each unit's declared public surface (vs. private/internal state) and its declared nesting depth.
- *Domino:* changing nesting depth — flattening two orchestration levels, or adding an intermediate layer — can turn a previously-legal call illegal, or vice versa, with the call site's own code completely unchanged.
- *Validate:* after any REORGANIZE that changes nesting, re-audit every cross-unit call against the *new* depth.
- *Example:* "a parent orchestrator calls public methods on its direct child orchestrator... it never bypasses it to call methods on the child orchestrator's internal widgets" — `this._ordersPanel.applySize(size)` legal, `this._ordersPanel._filters.setSize(size)` illegal (`containerization-orchestration-2.md` §6, §9.4).

**E2. Version / Generation**
- *Definition:* content carries an explicit version/generation marker, and correctness depends on knowing which generation is being combined, and what marker the output should carry.
- *Detect:* parse the marker per the project's own rule (see *Precise Pattern Matching* §2); confirm the rule for where the marker may legally appear.
- *Domino:* a build operation that copies a fragment's content verbatim risks also copying its version marker into the destination's *body* — a violation if the project forbids that; separately, merging fragments of meaningfully different generations may reintroduce stale content.
- *Validate:* confirm the output's marker follows the project's increment rule, and confirm no source's version token leaked into any destination's body text.
- *Example:* `version-control-1b.md` Rule 2 — "the version suffix lives only in the filename — never inside the file content." Copying a fragment's body into a merged file must not carry a stray version string into that file's prose.

---

## Domino Analysis: A General Algorithm

The base methodology's domino analysis asks: *what else breaks if I fix only this one thing?* For build tasks, the same question has to be asked once **per applicable dependency type** — a single change can be a Containment issue, a Nominal Contract mismatch, and a Cardinality collision simultaneously, and missing any one of the three is a real defect, not a rounding error.

```
INPUT: a proposed operation (move / rename / merge / split / delete) on some unit U

1. FRONTIER = { U };  CHECKED = { }
2. while FRONTIER is not empty:
     take one unit X from FRONTIER
     if X in CHECKED: continue
     add X to CHECKED
     for each dependency type T in the taxonomy (A1..E2):
         ask T's domino question about X
         for each unit Y the question surfaces as newly affected:
             if Y not in CHECKED: add Y to FRONTIER
3. output: CHECKED — every unit touched, directly or transitively
4. the operation is safe to execute only once CHECKED reaches a fixed point —
   one full pass over FRONTIER adds nothing new
```

This is a closure computation — structurally the transitive closure of a graph, where the "graph" is implicit and discovered incrementally: the taxonomy supplies the edge-detection rule, not an explicit adjacency list.

**Abbreviated trace** (renaming `.cart-container` → `.basket-container`):

```
U = the CSS class .cart-container

Iteration 1 (X = the class definition):
  B1 — new CartController('.cart-container') in INIT also names this class.
       → add: the INIT call site.
  E1 — CheckoutPageController holds this._cart = new CartController(...); the
       constructor call is a consumer already captured by B1. No new unit.
  C1 — --cart-radius is declared *under* .cart-container, not a reference to
       the class name itself. No new unit.

Iteration 2 (X = the INIT call site):
  no dependency type surfaces anything new.

CHECKED = { class definition, INIT call site } → fixed point. Safe to execute.
```

---

## Applying This Taxonomy to an Unfamiliar Domain

The taxonomy was derived from two domains — page assembly from HTML/CSS/JS fragments, and a widget/orchestrator component system. Neither domain is the point: the same eleven questions apply to a domain neither you nor this document has seen — a Terraform module layout, an entity-component game engine, a monorepo's package boundaries, a migration chain.

Before analyzing a new domain, answer these in order:

```
1. What is a "unit" here?
   (a file, a function, a resource block, a table — the smallest independently
   movable thing)

2. What is a "container / scope" here?
   (what nests inside what; what's globally visible vs. locally bounded)

3. What naming surfaces exist — and for each, is there a structural artifact that
   would flag a mismatch (Type B1), or is it convention-only (Type B2)?

4. Is there anything that must be unique per scope, which a merge could collide (B3)?

5. Is there implicit value inheritance across containment (C1), or an explicit
   multi-source override chain (C2)?

6. Is there a create/destroy, open/close, start/stop pairing — and if so, must
   two things share the literal same handle (D1), and must every created thing
   be torn down (D2)?

7. Is there a public-vs-internal boundary, or a fixed permitted nesting depth (E1)?

8. Is content tagged with a version/generation marker, and does the domain have
   its own rule for where that marker may legally live (E2)?
```

Answering these does not require a single example from this document — it requires reading the *new* domain's own rules (or reverse-engineering them from its files, the way Phase 1 below does) and mapping each finding onto the taxonomy. Once every "yes" is logged against its type, the General Domino Algorithm runs identically regardless of which domain produced the answers.

---

## Workflow Structure

### Phase 0 — Context Loading

Nothing gets transformed at this stage, only read and confirmed. "Context" means:

- **Direction** — MERGE / SPLIT / REORGANIZE / EXTRACT, and the destination unit(s)
- **Criterion** — the rule deciding where a boundary falls
- **Materials** — every unit in scope, with its declared role
- **Constraints** — anything that must not move, must stay byte-identical, or is off-limits
- **Scope boundary** — which discovered dependencies are this pass's job to resolve, and which belong to a different, not-yet-started task

```
User: here are 5 files, merge the 4 tab fragments into the shell
AI:   [reads file names + sizes, does not open content yet]
      → "5 files loaded. Direction: MERGE (4 fragments → 1 shell). Roles:
         shell = customer-account-1e-clean.html, fragments = account-{messages,
         mywallet,orders,wishlist}, shared = page.css/page.js. Confirming
         criterion before analysis."
```

**Do not assume a fragment's destination from its filename.** Confirm the mapping explicitly (see 1.1).

### Phase 1 — Analysis

#### 1.1 Classify Every Unit's Role

One pass, no content-reading required (see *Unit Roles*, above, for the vocabulary):

```
UNIT                              ROLE          STANDALONE?  SIZE    NOTES
customer-account-1e-clean.html    SHELL         yes          653 ln  14 nav links, 14 tab-panes
account-messages-1b.html          FRAGMENT      yes        1,770 ln  own <head>, own inline <script>
customer-account-page.css         SHARED        n/a              —  consumed by shell + all fragments
customer-account-page.js          ORCHESTRATOR  n/a              —  reads data-target/data-action
```

A FRAGMENT that is itself a standalone document is the most common source of wasted tokens: its actual payload is often 20–40% of its line count. The rest exists only so it could be previewed in isolation.

**Do not assume a fragment's filename matches its destination anchor.** `account-messages-1b.html` doesn't map to `id="tab-messages"` — it maps to `id="tab-correspondence"`. Confirm the real mapping before it's baked into the plan.

#### 1.2 Build the Structural Inventory — Scan, Don't Slurp

For each unit, get a skeleton without reading the body:

```bash
wc -l file.html
grep -n -E '<!DOCTYPE|<head|<body|</body|</html' file.html      # full document, or bare fragment?
grep -n -oE 'id="[a-zA-Z0-9_-]+"' file.html                       # candidate B1/B3 identifiers
grep -n -oE 'class="[^"]+"' file.html | tr ' ' '\n' | sort -u     # candidate B1/B3 identifiers
grep -n -E '<link|<script src|@import|href=|src='  file.html     # candidate B1 imports
```

Record exact line numbers for every boundary that might become a cut point. Don't read what's between them yet — that content only matters once this block is the one being moved.

**When a full read is actually justified** (the exception, not the default): the unit is small enough that scanning costs more round-trips than reading it outright (roughly, under ~150 lines / ~8KB); or no marker/tag-matching can find the boundary; or embedded logic could interact with the move in a non-obvious way and that risk needs judgment, not just relocation.

#### 1.3 Domino Analysis — Applying the Taxonomy

Run the *General Domino Algorithm* (above) starting from every candidate identifier found in 1.2. Check each against **all eleven types**, not just the one that seems obvious:

```
Export: id="tab-correspondence"                              [B1]
  ├── shell:163  data-target="tab-correspondence"
  ├── shell:328  href="#tab-correspondence"
  └── shell:514  aria-labelledby="account-nav-tab-correspondence"   [B1, paired]

Import: <script src="customer-account-messages.js">           [B1 — DANGLING]
  └── no file by that name in scope; account-messages-1b.html's own inline
      <script> (lines 615–1762) is the payload waiting to fill it

Cardinality check                                              [B3]
  └── 0 cross-fragment id collisions found (verified); 5 competing Bootstrap
      references (2 versions, 2 path conventions) must collapse to 1

(no B2 Nominal Contract present in this fragment — see Case Study B for that;
 no C1/C2/D1/D2/E1 present in this domain at all — see Case Study B)
```

**Scope note:** the shell declares the same dangling-script pattern for three other fragments and one unit (`customer-account-profile-details.js`) with no matching fragment among the files provided. That one is a Phase 0 scope question — confirm whether it belongs to this pass before treating it as this pass's problem.

**Rule:** the graph must be exhaustive before Phase 2 starts. An incomplete pass is this document's version of an incomplete domino — it just shows up as a broken tab, or a script that 404s, instead of a broken CSS rule.

### Phase 2 — The Build Map

A JSON artifact, not prose, so it can be checked mechanically. A Build Map has two co-equal parts: what physically moves (`operations`), and what must stay wired up (`reference_registry`, tagged by taxonomy type).

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
    "dependency_types_in_play": ["A1", "B1", "B3"],
    "criterion": "one standalone preview file per tab-pane, matched to existing anchors",
    "total_operations": 13
  },
  "operations": [
    {
      "id": "build-000",
      "type": "DEDUPE",
      "dependency_type": "B3",
      "source": { "file": "account-messages-1b.html", "lines": { "start": 8, "end": 8 },
                  "context": "<link href=\"...bootstrap@5.3.3/dist/css/bootstrap.min.css\">" },
      "destination": { "file": "customer-account-1e-clean.html",
                        "anchor": "do not carry over — shell already loads 5.3.8 at lines 32/592",
                        "lines": null },
      "depends_on": [],
      "collision_risk": "version mismatch (5.3.3 vs 5.3.8), both css and js bundle",
      "status": "pending"
    },
    {
      "id": "build-001",
      "type": "EXTRACT_INSERT",
      "dependency_type": "A1",
      "source": { "file": "account-messages-1b.html", "lines": { "start": 289, "end": 576 },
                  "context": "<section class=\"messages-container ...\" data-ref=\"messages-root\">" },
      "destination": { "file": "customer-account-1e-clean.html",
                        "anchor": "replace TODO comment at line 523, inside id=\"tab-correspondence\"",
                        "lines": { "start": 523, "end": 523 } },
      "depends_on": ["build-000"],
      "collision_risk": "none found in 1.3 — fragment declares only 2 ids, neither reused elsewhere",
      "status": "pending"
    }
  ],
  "reference_registry": [
    {
      "dependency_type": "B1",
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
      "dependency_type": "B1",
      "name": "customer-account-messages.js",
      "defined_in": [],
      "consumed_in": [{ "file": "customer-account-1e-clean.html", "line": 603, "via": "<script src>" }],
      "resolved": false,
      "note": "dangling until a later operation creates the file — the shell already expects it"
    },
    {
      "dependency_type": "B3",
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
      "note": "five references to the 'same' library, two versions and two path conventions — must collapse to one, by an explicit decision, not a silent drop"
    }
  ]
}
```

#### Required Fields

| Field | Purpose |
|---|---|
| `dependency_type` | One of the eleven taxonomy codes — determines which detect/domino/validate rule applies |
| `type` (operation) | EXTRACT / INSERT / MERGE / SPLIT / DEDUPE / RELINK / RENAME_FOR_COLLISION / REORDER |
| `source.lines` | Exact range — the only part of the source that should ever be read in full |
| `destination.anchor` | The literal marker or exact insertion point — never "somewhere in there" |
| `depends_on` | Other operation ids that must complete first |
| `collision_risk` | Explicit, always filled in — "none found" is a valid value; it's proof 1.3 was actually done |
| `status` | `pending` / `in-progress` / `done` / `verified` — "moved" and "confirmed correctly moved" are different claims |
| `defined_in` / `consumed_in` (registry) | Lists — a dependency can have multiple consumers, as `tab-correspondence` does above |
| `resolved` (registry) | Boolean — must be `true` for everything before the map counts as complete |

#### Operation Types

```
EXTRACT               — pull a bounded block out of a source, read-only on the source
INSERT                 — place an already-extracted block at a destination anchor
EXTRACT_INSERT          — the common case: one source range, one destination anchor
MERGE                  — combine two or more blocks into one
SPLIT                  — the inverse: one source range becomes N destination units
DEDUPE                  — remove a redundant copy of a shared resource once reconciled
RELINK                  — update a path/href/src/import to point at the new location
RENAME_FOR_COLLISION     — rename an identifier and propagate it to every consumer, in
                           one operation — never split across two rows
REORDER                  — reposition a block within the same unit
```

#### Risk Levels

```
CRITICAL — breaks a dependency outright: dangling B1, colliding B3, a broken D1/D2
           chain, or silent content loss
HIGH     — structurally wrong even though the dependency technically resolves:
           bad nesting (A1), wrong order (A2), an E1 boundary violated
MEDIUM   — redundant, not broken: a B3 duplicate not yet reconciled, a C1/C2 value
           drift not yet confirmed
LOW      — cosmetic: whitespace, comment style, formatting
```

### Phase 3 — Assembly Plan

The map becomes a grouped, ordered tracker, regrouped around **destinations**.

```
Destination: customer-account-1e-clean.html (group)
  ├── Collisions & renames [B3] — resolved first
  │   └── (none required — 1.3 found no cross-fragment id collisions)
  ├── Shared resource reconciliation [B3] — done once, before insertion
  │   └── [ ] build-000 — bootstrap: five references collapse to one
  ├── Fragment insertion [A1] — one item per tab, in nav order
  │   ├── [ ] build-001 — messages  → #tab-correspondence  (depends_on: build-000)
  │   ├── [ ] build-003 — mywallet  → #tab-wallet           (depends_on: build-000)
  │   ├── [ ] build-005 — orders    → #tab-orders            (depends_on: build-000)
  │   └── [ ] build-007 — wishlist  → #tab-wishlist          (depends_on: build-000)
  ├── Script extraction [B1, resolving dangling script-src] — one per fragment
  │   └── [ ] build-002/004/006/008 — new customer-account-{name}.js per fragment
  └── Scoped CSS extraction — one per fragment with embedded <style>
      └── [ ] build-009..012 — customer-account-tab-*.css, per the tab-overview.css precedent
```

**Ordering rules:** collisions/renames first (everything downstream assumes names are unique) → shared-resource reconciliation next, once → fragment insertion in nav order, not numbering order → RELINK in the same step as the move it follows, never deferred.

### Phase 4 — Execution

**Standing rule:** for SPLIT/REORGANIZE, keep the original intact (copy, don't move-and-delete) until Phase 5 confirms the new units reconstruct it. A build task is far less reversible mid-flight than a rename.

**1. One destination at a time.** Complete, validate, then move on.

**2. Extract by range, never by memory:**

```python
# ❌ Wrong — read the fragment, then write "what it said" from memory
# ✅ Correct — cut the exact range, paste it verbatim
lines = open("account-messages-1b.html").readlines()
block = "".join(lines[288:576])          # 0-indexed slice for lines 289–576
insert_at(destination, anchor_line=523, content=block)
```

**3. Verify tag/brace balance before cutting** (see *Precise Pattern Matching*) — not after something renders broken.

**4. Resolve a B3 collision (or B1 rename) and all its consumers in one operation.** A rename that only touches the definition produces a dangling reference — worse than not renaming, because it now fails silently.

**5. Reconcile B3/shared resources as one unified pass**, not once per consumer.

**6. Preserve D1/D2 — identity and cascade completeness — when splitting a class or module across files.** A helper extracted into its own file must still share the original's `AbortController` (D1), and any new child added during the build must be added to the existing teardown cascade (D2), not left implicit.

**7. Validate immediately after each destination — not at the end.**

### Phase 5 — Validation

**Level 1 — Structural / Content-Preserving.** Prove, don't eyeball, that a moved block survived unchanged:

```bash
sed -n '289,576p' account-messages-1b.html | sha256sum
sed -n '523,810p' customer-account-1e-clean.html | sha256sum   # recompute after insertion — lines shift
```

For a pure `EXTRACT_INSERT`, these must match.

**Level 2 — Referential Integrity**, automated per type:

```bash
# B1 — every data-target resolves to exactly one matching id
for target in $(grep -oE 'data-target="[a-z-]+"' shell.html | sort -u); do
  id_attr=$(echo "$target" | sed 's/data-target=/id=/')
  count=$(grep -c "$id_attr" shell.html)
  [ "$count" -eq 1 ] || echo "MISMATCH: $target — found $count times"
done

# B1 — every local script src actually resolves to a real file
grep -oE 'script src="[^"]+\.js"' shell.html | sed -E 's/script src="([^"]+)"/\1/' | while read -r path; do
  [ -f "$path" ] || echo "DANGLING: $path"
done
```

**B2 needs a different technique** — there is no artifact to grep-count. List every emitted string and every listened-for string as two separate sets and diff them directly; a clean grep result proves nothing here.

**Level 3 — Syntax & Semantic Validity.** Tag balance across the *whole* destination, not just the inserted region. No shared resource loaded twice — confirm versions genuinely match before treating two references as one duplicate. Semantic exception review: a repeated utility class is legal; a repeated `id` is not, once merged.

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

`grep -n '</div>'` after a `<div>` you care about returns every closing div in the file, in document order — not necessarily the matching one. A depth counter, not a single-pattern search, gets this right:

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

Run against `account-messages-1b.html`, this finds the `<section class="messages-container">` opened at line 289 closing at line 576 — confirmed independently by the fragment's own closing comment, `<!-- /messages-container -->`, immediately after. The same technique generalizes to JS/JSON objects (`{ }`, watch for braces inside string literals) and to code (`( )`). Beyond a single well-known bracket type, use an actual parser instead of extending the regex further.

### 2. Version / Generation Tokens in Filenames

`version-control-1b.md` defines the version token as "the first occurrence of the pattern `<number><letter a–h>`." The prefix may itself contain digits, which breaks a naive "grab the first digit run" approach:

```
Asguard01MediaGallery-NG-20g_-_themes.html
         ^^                ^^
     part of the prefix     the actual token: 20g
```

A correct extractor constrains the *letter*, not just the digits:

```python
import re

VERSION_TOKEN = re.compile(r'(\d+)([a-h])(?![a-zA-Z])')

def parse_version(filename):
    m = VERSION_TOKEN.search(filename)     # .search(), not .match() — token can be anywhere
    if not m:
        return None
    return {"prefix": filename[:m.start()], "number": int(m.group(1)),
             "letter": m.group(2), "rest": filename[m.end():]}
```

`01` in the prefix never matches: the character right after it is `M`, which isn't in `[a-h]`, so the pattern fails there and the search continues to `20g`. The trailing `(?![a-zA-Z])` is a hardening guard, not something the spec states explicitly — it protects against a messier case the given examples don't contain, where a version-shaped digit+letter is immediately followed by another letter and is therefore probably the start of a word, not a deliberate suffix (`5act...` should not parse as version `5a` plus leftover `ct...`). Verified against every example in `version-control-1b.md`, plus this document's own filename, `ai-task-execution-methodology-build-1a.md` → prefix `ai-task-execution-methodology-build-`, version `1a`.

**Rule of thumb, both cases:** if a boundary can be found with an explicit marker — a closing comment, a TODO anchor — use the marker. It's faster, and it doubles as a sanity check on the pattern-matcher's result.

---

## Requirements Specification for Creating a Build Map

```markdown
1. Units in scope — every unit, each with a declared role (§ Unit Roles)
2. Direction — MERGE / SPLIT / REORGANIZE / EXTRACT, and the destination unit(s)
3. Criterion — the exact rule deciding a boundary
4. Which dependency types (A1–E2) are actually in play for this task — not all
   eleven apply to every domain; declare which do, and why the rest don't
5. Operation vocabulary — EXTRACT / INSERT / MERGE / SPLIT / DEDUPE / RELINK /
   RENAME_FOR_COLLISION / REORDER
6. Risk scale — what counts as CRITICAL / HIGH / MEDIUM / LOW for this task
7. JSON schema — exact structure for `operations` and `reference_registry`
8. Rules for operation ids — format, numbering
9. Context-field requirements — verbatim snippet length cap (≤120 chars)
10. What is explicitly NOT in scope — e.g. "rename nothing except to resolve a
    collision the merge itself creates"; which discovered dangling references
    belong to a different task
```

| Naive Spec Problem | Solution |
|---|---|
| "Just combine these files" | Explicit direction + destination unit name(s) |
| No stated criterion | A criterion precise enough that a second person draws the same boundaries |
| "Check the dependencies" | Named types (A1–E2), each with its own detect/validate method |
| Collisions found during execution | Found in 1.3, resolved in the map — before a single byte moves |
| "Looks right" as the validation bar | Type-appropriate check: grep-count for B1, explicit diff for B2, identity check for D1 |
| A dangling reference assumed to be a bug | Checked against scope first — it may be a different task's placeholder |

---

## Templates for Common Task Types

### Merge Fragments into a Shell (Many → One)
```
Phase 0: confirm shell + fragment list + shared/scoped resources + destination
Phase 1: role-classify; scan each fragment for its payload boundary; run the
         Domino Algorithm across shell + fragments + resources for every
         applicable dependency type
Phase 2: Build Map — EXTRACT_INSERT per fragment's payload, DEDUPE per B3
         conflict, RENAME_FOR_COLLISION for any B1/B3 name shared across fragments
Phase 3: plan by destination — collisions/renames → shared-resource
         reconciliation → insertion in logical order
Phase 4: cut by exact range, resolve collisions atomically, validate per fragment
Phase 5: hash-match, reference-count by type, tag-balance the final unit
```

### Split a Monolith by Criteria (One → Many)
```
Phase 0: confirm the source + the split criterion + destination naming pattern
Phase 1: find every boundary matching the criterion (tag-balance/marker-
         confirmed, not guessed); identify which shared resources each new
         unit needs to carry to stay independently valid
Phase 2: Build Map — SPLIT (⇒ N EXTRACTs) per boundary, an ANCHOR operation for
         what's left behind at each cut point
Phase 3: plan by destination unit (one group per new unit produced)
Phase 4: cut by exact, verified range; leave an explicit marker at each cut
         point — never a silent gap
Phase 5: round-trip check — do the shell + new units together reconstruct the
         original's observable behavior, modulo intended cleanup?
```
This is the direction for a file like this document's Case Study A monolith, `customer-account-1e.html` (2,744 lines, 210KB) — decomposable by the same tab-pane criterion used above for MERGE, run in reverse.

### Extract a Shared Resource and Relink Consumers
```
Phase 0: confirm which resource is suspected duplicated, and across which consumers
Phase 1: diff every occurrence against the others before assuming they're
         identical (B3) — a byte-identical duplicate and a version-mismatched
         one require different handling
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
         the OLD structure, paying particular attention to E1 (does the new
         nesting depth change which calls are legal?)
Phase 2: Build Map — SPLIT of the old grouping followed by a MERGE into the
         new one, planned together so nothing is copy-pasted into two places
Phase 3: plan by new destination
Phase 4: execute as one coordinated pass — the exception to "one destination
         at a time," since source and destination can be mid-transition
         simultaneously here
Phase 5: hash-match, reference-count, round-trip — Merge's and Split's checks combined
```

---

## AI Checklist Upon Receiving a Task

```
□ Confirmed the direction and exact destination unit(s) — not assumed from names?
□ Assigned every unit a role before reading a single line of content?
□ Scanned for structure before reading full content anywhere a scan would answer it?
□ Checked every candidate identifier against ALL applicable dependency types
  (A1–E2), not just the one that was obvious at a glance?
□ For every Nominal Contract (B2) pair, explicitly diffed emitted vs.
  listened-for strings — not trusted the absence of an error?
□ Checked whether a dangling reference belongs to a DIFFERENT, not-yet-started
  task rather than assuming it's this pass's bug?
□ Confirmed collisions/B3 conflicts are resolved in the map BEFORE anything
  depending on them gets inserted?
□ Confirmed each fragment's destination explicitly, rather than assumed
  filename-to-anchor matching?
□ Preserved D1 (shared instance) and D2 (cascade completeness) when splitting
  any class or module across units?
□ Planned validation after each destination, not deferred to the end?
□ Can PROVE content wasn't silently altered in transit (hash/diff), rather
  than stating it "looks right"?
□ For a split: would re-analyzing the output reproduce the same boundaries
  started from?
```

---

## Anti-Patterns

### ❌ Reading Full Units When a Structural Scan Would Answer the Question
```
Bad:  cat the entire 1,770-line fragment to find one section
Good: grep -n 'class="messages-container' first, read only lines 289–576
```
Reason: the map only needs boundaries and identifiers until the moment of extraction.

### ❌ Retyping Content From Memory Instead of Extracting It
```
Bad:  read a fragment, hold it in mind, "reproduce" it in the destination
Good: cut the exact recorded range and paste it verbatim
```
Reason: memory-copies drift silently; range-copies are mechanically checkable.

### ❌ Merging Before Resolving Collisions
```
Bad:  paste all fragments in, then notice two both defined id="filter-btn"
Good: run the Domino Algorithm first; resolve every B3/B1 conflict in the map
```
Reason: a collision found after the merge means editing content that's already moved.

### ❌ Forgetting to Reconcile Shared/Global Resources
```
Bad:  the destination loads a library three times, once per fragment's own <head>
Good: shared resources reconciled as their own operation — including confirming
      "duplicates" are actually identical, not just similar-looking
```
Reason: two references to what looks like one resource can differ in version or path convention. Dropping one without checking is a silent downgrade or break.

### ❌ Treating a Convention-Only Contract as if It Were Enforced
```
Bad:  assume two matching-sounding event names are fine because nothing threw
Good: list every emitted name and every listened-for name side by side and diff them
```
Reason: a Type B2 dependency has no structural artifact to lean on. "It ran without errors" means nothing here.

### ❌ Bypassing an Encapsulation Boundary to Save a Step
```
Bad:  this._ordersPanel._filters.setSize(size) — reaching past the child orchestrator
Good: this._ordersPanel.applySize(size) — calling its public method
```
Reason: legal today doesn't mean legal after the next REORGANIZE. A bypass that "happens to work" at the current nesting depth breaks the moment that depth changes.

### ❌ Guessing Boundaries Instead of Matching Them
```
Bad:  "split roughly around line 800"
Good: split at the exact tag-balanced or marker-confirmed boundary
```
Reason: nested tags make an eyeballed boundary a coin flip past one level of nesting.

### ❌ Assuming a Fragment's Filename Matches Its Destination Anchor
```
Bad:  assume account-messages-1b.html must map to id="tab-messages"
Good: confirm the actual mapping — here it's id="tab-correspondence"
```
Reason: naming drifts between when a component was built and where it ends up living.

### ❌ Validating Only by Reading the Result
```
Bad:  skim the merged file — it "looks fine"
Good: grep-count B1/B3, diff B2 pairs, hash-compare moved blocks, tag-balance the whole file
```
Reason: a page can render correctly while still containing a duplicate id or a dangling pair that only breaks under one specific interaction.

---

## Case Studies

### Case Study A — HTML/CSS/JS Tab-Fragment Merge

One shell (653 lines, 14 tab-panes) absorbing four standalone tab-preview files (1,133–1,770 lines each) into its placeholder tab-panes. Full worked example threaded through *Workflow Structure*, above.

| Type | Where it showed up |
|---|---|
| A1 Containment | Tab-pane boundaries, TODO anchors |
| B1 Nominal Reference | `data-target`/`id`/`aria-*` pairs; the dangling `<script src="customer-account-messages.js">` |
| B3 Cardinality | 0 cross-fragment id collisions (verified); 5 competing Bootstrap references collapsing to 1 |
| E2 Version | The fragment files themselves carry `version-control-1b.md` suffixes (`-1b`, `-1d`) |
| C1 / C2 / D1 / D2 / E1 | Not present in this domain — see Case Study B |

### Case Study B — Widget/Orchestrator Assembly

Per `containerization-11.md` + `containerization-orchestration-2.md`: several independently-built widgets (cart, summary, promo) combined under a page orchestrator. Each widget is *designed* for this from the start (Law Zero, isolated CSS scoping, event-only communication), so the taxonomy surfaces risks Case Study A never touches:

- **B2 Nominal Contract** — `CartController` emits `dispatchEvent(new CustomEvent('cart:item-added', {...}))`; `CheckoutPageController` must listen for the identical string. Nothing links the two files except that literal string.
- **C1 Inheritance** — `.cart-container { --cart-radius: var(--checkout-radius, .5rem); }`. Assembled under `.checkout-page`, it inherits the page's radius; assembled standalone, it silently falls back to `.5rem`.
- **C2 Layered Override** — `DEFAULTS → opts → data-attributes`. Lifting a widget's markup without carrying its `data-orders-*` attributes silently changes the effective config.
- **D1 Shared-Instance** — every listener in a widget must share that instance's own `this._ac.signal`. Splitting the class across files must not let an extracted helper create its own `AbortController`.
- **D2 Lifecycle-Cascade Completeness** — `CheckoutPageController.destroy()` explicitly tears down `_cart`, `_summary`, `_promo`. A fourth widget added later without a matching line is an orphaned child.
- **E1 Encapsulation Boundary** — `this._ordersPanel.applySize(size)` legal; `this._ordersPanel._filters.setSize(size)` illegal. Changing nesting depth during a REORGANIZE flips which calls are allowed.

### Case Study C — Parsing a Version Token

`version-control-1b.md`'s own tricky case: `Asguard01MediaGallery-NG-20g_-_themes.html`. The prefix contains a digit run (`01`) that is *not* the version token — the actual version is `20g`. See *Precise Pattern Matching §2* for the extractor and why a naive "first digit run" reads this file wrong.

---

## Working with Many Units (Token Discipline)

**Default posture: scan first, always.**

```bash
wc -l *.html *.css *.js                                     # size, in one call
grep -c '<!DOCTYPE' *.html                                    # which are full documents
grep -n -oE 'id="[a-zA-Z0-9_-]+"' file.html | sort -u          # B1/B3 candidates
grep -n -E '<link|<script src|@import' file.html               # B1 imports
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

**Batch structural queries across the whole unit set, not one at a time:**

```bash
for f in *.html; do echo "=== $f ==="; grep -c 'id="' "$f"; done
```
is one round-trip; five separate single-file greps are five.

---

## Execution Quality Metrics

```
1. Planned operations = completed AND verified operations (not just completed)?
2. Every reference-registry entry resolves to the expected count — zero
   dangling, zero unintended duplicates?
3. Hash/diff confirms every EXTRACT_INSERT preserved content exactly, apart
   from explicitly-listed intentional changes?
4. Every shared resource loads exactly once, confirmed same version everywhere?
5. Every B3 collision resolved before merge, rename applied to 100% of consumers?
6. Destination passes a basic structural check — balanced tags, valid syntax?
7. For a split: reassembling the outputs reproduces the original's behavior,
   modulo intended cleanup?
8. Every dependency type declared "in play" in the map's meta has at least one
   corresponding entry in the reference registry — was the taxonomy actually
   applied, not just cited?
```

**Numerical indicators to record before/after:** unit counts (source/destination); total lines/bytes (should reconcile: after ≈ before + intentional additions − discarded boilerplate − deduped duplicates); reference-registry entries, resolved vs. dangling, by type; collisions found/resolved; shared-resource conflicts found (including version mismatches) and how each was decided.

---

*This methodology is a companion to `ai-task-execution-methodology.md`, scoped to tasks where units are restructured across boundaries rather than edited in place under a fixed spec. Version 1a generalizes the framework from a single worked example into a domain-independent taxonomy of eleven build-dependency types plus a general domino algorithm, grounded in two illustrative domains — an HTML/CSS/JS page assembly (Case Study A) and a widget/orchestrator component system per `containerization-11.md` and `containerization-orchestration-2.md` (Case Study B) — with a third short illustration (Case Study C) on parsing the version tokens defined in `version-control-1b.md`, the same convention this file's own name follows.*
