# AI Task Execution Methodology — Build Protocol
## A Compositional Model of Build Dependencies — Six Dimensions, Two Qualifiers, and a Durable Cache Between Plan and Commit

*Version 1f. Following `1e` in sequence, per `version-control-1b.md`'s own convention — prefix `ai-task-execution-methodology-build-`, version token `1f`.*

---

## What Changed from v1a

v1a organized dependencies into eleven named types (A1–E2), grouped under five headings. Auditing that list against a domain it wasn't built from — a quick pass against database-migration files — surfaced a structural problem: **enforcement** (whether some mechanism actually checks a dependency, or it's convention-only) was only modeled as a special case of naming (Types B1 vs. B2), when it plainly applies just as much to ordering, boundaries, and containment. A list that has to grow every time a new domain reveals a new combination isn't a taxonomy — it's a work-in-progress inventory with a closed-looking table drawn around it.

v1b replaces the eleven-item list with **six dimensions and two cross-cutting qualifiers**. Instead of "which of eleven boxes does this fit," the question becomes "which dimension(s) does this touch, and how is each qualified" — a compositional question with a small, fixed vocabulary, rather than a matching question against a list that can never prove itself complete.

Two quick re-checks, done before committing to this structure:
- **Database migrations** — `up()`/`down()` pairing maps cleanly to Lifecycle (Completeness); migration-number uniqueness to Cardinality; table/column references to Name; migration order to Position (Sequence); version numbers to Generation. A plausible fit for five of six, without forcing anything.
- **Infrastructure-as-code (Terraform-style)** — module nesting and apply-order to Position; resource references to Name (compiler-checked); variable precedence (`tfvars` → CLI flags → environment) to Value (Explicit-Layered); provider/state versions to Generation; and, notably, **module output boundaries are actually enforced** by the tool itself — a live example of Boundary being `CHECKED` rather than convention-only, which neither original case study demonstrated.

Both are quick conceptual checks, not full worked case studies — they're evidence the compositional model transfers further than the enumerative one did, not proof it's complete. Nothing claims completeness here; see the *Catalog of Observed Patterns* below for why that claim is deliberately never made.

## What Changed from v1b

v1b fixed *what* gets checked — six dimensions instead of eleven ad hoc types. It didn't address *when* the checking turns into something physically verifiable. The Build Map (Phase 2) and Assembly Plan (Phase 3) were both external artifacts — JSON and a checklist that live in the conversation, not on the units themselves. Nothing stopped the gap between "I planned this" and "I'm now re-deriving it from a re-scan, or from memory" from opening up silently the moment execution started.

v1c added a Marking Pass: a cheap, reversible edit that plants a comment marker at every source boundary and every destination anchor *before* any real content moves, verified by a single grep. This directly answered a concrete question: does the plan fix entry points and insertion sections *before* the token-costly work starts, physically, not just on paper? Before v1c: no.

## What Changed from v1c

Two fixes, both raised as direct questions rather than found unprompted.

**Repositioning.** v1c placed the Marking Pass at 3.5 — after Assembly Plan, before Execution. Tracing what marking actually depends on: it needs Phase 1.3's domino findings, specifically the `ALSO:` notes reporting that a fragment's markup pulls its script and style along with it — findings Phase 2 has already formalized into the map. It does **not** need Assembly Plan, which only groups and orders operations Phase 2 already fully knows; a marker is found by content-search, not by its position in an execution queue, so waiting for an execution-order plan before marking was a dependency that was never real. v1d moves the Marking Pass to **Phase 2.5** — immediately after the Build Map, before Assembly Plan. A side effect: Assembly Plan now groups and orders operations whose entry/exit points are already physically marked and grep-verified, instead of grouping raw, unconfirmed coordinates.

**Generalizing the marker for multi-source merges.** v1c's `BUILD:INSERT op=build-001` names exactly one contributing operation. A MERGE combining two sources into one destination had no clean way to say so. The destination marker now takes a list — `sources=[build-001]` for the ordinary single-source case (kept as a one-element list so there is exactly one marker shape to learn, not two), `sources=[build-001, build-004]` when more than one operation lands at the same anchor, in insertion order. Verification generalizes the same way: every op id inside every `sources=[...]` list must have exactly one matching EXTRACT pair, and must appear in exactly one `sources=[...]` list — not zero, not two.

## What Changed from v1d

Every version through v1d was refined by reasoning about the model in the abstract — audited, stress-tested against domains that only existed as thought experiments, never actually run against a real task end-to-end. v1e is the first version informed by an actual Phase 0–5 run: the real `customer-account-1e-clean.html` merge (Case Study A's own source files), executed in full, not just planned.

That run surfaced one genuine gap Phase 1.2's structural inventory didn't guard against: **a unit's "obvious" container is not guaranteed to be its whole payload.** `account-messages-1b.html`'s delete-confirmation modal sits as a *sibling* of `.messages-container`, not inside it — the fragment's own author left the reason in a comment: `MODAL (outside section, inside container)`, since Bootstrap modals render in a `<body>`-level stacking context. The extraction range recorded in the Build Map (`289–576`, matching `.messages-container`'s own boundary exactly) was correct for what it claimed to cover, and still missed the modal, because nothing in Phase 1.2 asked "is there a sibling that belongs with this payload but isn't nested inside it." The gap wasn't caught until Phase 5's own id-accounting turned up one id fewer than expected — the validation layer working exactly as designed, just later in the pipeline than it needed to. Phase 1.2 now asks the question directly (below), so this class of gap is caught during analysis, not during a post-hoc count.

A second, smaller finding from the same run: an ANCHOR is not always something that already exists to be *filled* (a TODO comment, a dangling `<script src>`) — sometimes it has to be *created* (the shell had no `<link>` tag at all for the four new tab stylesheets, unlike the JS files, which already had dangling references waiting). Phase 2's Build Map now says so explicitly.

## What Changed from v1e

v1e was validated end to end on one real merge. This version is informed by a second one, run without this document's own discipline applied — which is exactly what makes it useful: it shows what a Build Protocol run looks like when Phase 2.5 is skipped, and precisely which class of defect that produces.

**The run.** `customer-account-1f.html` — a 14-tab account shell, 2,714 lines, assembled from independently-authored tab fragments, alongside 11 already-extracted per-tab CSS files and 11 already-extracted per-tab JS files (ranging 1.1–15.2 KB and 5.3–62.9 KB respectively). Larger in scope than Case Study A by more than a factor of three.

**What it got right.** Every `data-target` ↔ `id` pair across all 14 tabs resolved correctly. Every one of the 22 CSS/JS asset references resolved correctly. A full tag-balance pass across the whole file — the same depth-counter check specified under *Precise Pattern Matching* — found the real markup completely sound; the one apparent discrepancy (a `<span>` count off by one) traced to the string `<span` appearing inside an HTML comment documenting a legacy class-naming convention, not to a broken tag. In short: every check this document already specifies, this run passed.

**What it got wrong.** Two of the fourteen tab-panes — `tab-subscriptions` and `tab-item` — contained nothing past their header chrome except:
```html
<!-- TODO: insert tab content here — account-subscriptions -->
```
Not truncated mid-tag. Not corrupted. Not a shortened paraphrase of longer content. Simply never filled — an operation that was presumably planned and never executed, with nothing anywhere in the process that counted how many tab-panes were supposed to receive content and compared that number against how many actually did. No `BUILD:` marker of any kind appears anywhere in the file, meaning this run didn't use Phase 2.5 either — there was no physical record of intent for anything downstream to check against.

**Why "the file looks fine" didn't catch it.** A 2,714-line file with 12 fully-realized tabs habituates a reader — human or model — to the shape "header, then substantial content." Two tab-panes that repeat the header exactly and then stop are, visually and structurally, the same *kind* of thing as the other twelve, just shorter — nothing about them fails to parse, fails a lint rule, or breaks a link. Completeness and structural validity are different questions, and this document's existing validation levels (Phase 5) only ever asked the second one.

**Where the state that would have caught this actually lived.** Not in any file — in the model's own attention, over the course of one long task with fourteen separate content-insertion points to get through. That is exactly the kind of state a reliable system never trusts: it exists only while the process is running, degrades under load, and vanishes completely the moment the process is interrupted or its context is compacted. Nothing about *this specific run* is unusual; asking a model to hold the true/false state of fourteen independent "is this one actually done" facts purely in its own running attention, across a long single pass, is asking it to be the durable record — a job durable records exist specifically because attention, biological or artificial, is bad at.

**The fix.** Two changes, both additions rather than revisions to the existing model:

1. **A durable, external cache, populated and validated *before* anything commits.** Phase 2.5 (Marking) already fixes *where* content goes. This version adds Phase 2.6 (Cache Population) and Phase 2.7 (a validation gate) to fix *what* — every operation's exact payload, extracted once, hash-stamped, and checked against a hard completeness count before Phase 4 is allowed to touch a single destination file. See *The Cache-and-Commit Protocol*, below.
2. **An explicit reliability model borrowed from systems that already solved this class of problem.** Write-ahead logging, two-phase commit, and checksum-verified hand-offs are not new ideas — they exist because "did the write actually happen, and can I prove it without re-trusting the process that did it" is a solved problem in databases and distributed systems. See *Reliability Model: Guarantees Borrowed from Systems Engineering*, below.

Neither change touches the Dependency Model itself — the six dimensions, the two qualifiers, and the General Domino Algorithm are unchanged, because nothing about this incident was a dependency-classification failure. Every dependency this run had was correctly identified and correctly wired. The failure was one level below that: two units of content that were supposed to exist in the final file simply didn't, and nothing asked.

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

Knowing what to check and knowing where to cut both still have to survive the trip from "I've figured it out" to "I've done it" — and that trip has its own internal order: a step only earns its place in the sequence if something *earlier* actually produces what it needs. That's the test the Marking Pass failed at 3.5 and passes at 2.5.

**A fourth failure mode sits alongside the ones above, and it survives even when analysis, mapping, and marking are all done correctly.** Knowing where a unit's content should go, and having a physically marked boundary for it, does not yet guarantee the content actually crosses that boundary. By default, a "copy" step in a conversation with a model is the model *producing output* at the moment of transfer — and producing long verbatim spans as output, especially many of them across one long task, is exactly the operation a model is least reliable at: it can truncate, it can quietly stop partway through one item in a list and move on to the next, and nothing about the surrounding text will look wrong when it does. *What Changed from v1e*, above, is a real instance of this — not corrupted content, but content that was supposed to exist and simply never got written, with nothing in the process that noticed the gap. *The Cache-and-Commit Protocol*, below, treats "did this transfer actually happen, provably" as its own question, separate from "do I know where it goes."

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

**A container's boundary is not automatically its payload's boundary.** After finding a unit's main container, explicitly check for siblings that are architecturally part of the same logical piece but deliberately placed outside it — a modal rendered as a sibling of its trigger's container, for stacking-context reasons, is the common case (see *What Changed from v1d*). The fragment's own comments (`MODAL (outside section...)`) are usually the fastest way to find this, faster than inferring it later from an id-count that doesn't add up.

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
grep -n -iE 'modal|MODAL \(outside' file.html                     # siblings outside the main container — see below
```

Record exact line numbers for every boundary that might become a cut point. Don't read what's between them yet. **Finding the main container is not the same as finding the whole payload** — run the `modal` check above regardless of whether the container's own range looks complete; a sibling placed outside it for a real architectural reason (stacking context, `<body>`-level rendering) won't show up any other way until a later id/hash count comes up short.

**Full read is justified only when:** the unit is small enough that scanning costs more round-trips than reading it outright (roughly under ~150 lines / ~8KB); or no marker/tag-matching can find the boundary; or embedded logic could interact with the move in a non-obvious way and that risk needs judgment.

#### 1.3 Domino Analysis — Applying the Model

Run the *General Domino Algorithm* starting from every candidate identifier found in 1.2, checked against all six dimensions. **This is the step the Marking Pass (2.5) depends on** — the "also carries its script/style" findings below are exactly what an `ALSO:` marker note reports, so this analysis has to be complete before anything gets marked.

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

A JSON artifact, not prose. Two co-equal parts: what physically moves (`operations`), and what must stay wired up (`reference_registry`, tagged with a full descriptor — not a single code). This map is still external to the units themselves — **Phase 2.5, immediately next, is what plants its coordinates onto the units and makes them grep-verifiable, before Assembly Plan groups them for execution.**

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
| `source.lines` | Exact range — what Phase 2.5 turns into a physical `BUILD:EXTRACT` marker pair |
| `destination.anchor` | The literal marker or exact insertion point — what Phase 2.5 turns into a `BUILD:INSERT` marker |
| `depends_on` | Other operation ids that must complete first |
| `status` | `pending` / `in-progress` / `done` / `verified` — "moved" and "confirmed correctly moved" are different claims |

#### Operation Types

```
EXTRACT | INSERT | EXTRACT_INSERT | MERGE | SPLIT | DEDUPE | RELINK |
RENAME_FOR_COLLISION | REORDER
```

For `MERGE`, more than one operation can land at the same destination anchor — see Phase 2.5's `sources=[...]` marker for how that's expressed physically.

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

### Phase 2.5 — Marking Pass

The Build Map (Phase 2) is still external to the actual units — JSON that lives in the conversation, not on disk. This phase turns it into something physically checkable: a lightweight, reversible edit that plants a marker at every source boundary and every destination anchor, *before* a single byte of real content moves, and *before* the Assembly Plan groups anything for execution.

**Why here, and not after Assembly Plan.** Assembly Plan (Phase 3) groups and orders operations Phase 2 already fully knows — it discovers nothing new, so it is not a prerequisite for marking. What genuinely *is* a prerequisite is Phase 1.3's domino analysis: the `ALSO:` note on a destination marker is reporting exactly what 1.3 found (that this fragment's markup also carries a script and a style block along with it). Marking before 1.3 finishes would mean marking with incomplete information — the very thing the note exists to capture wouldn't exist yet. Marking after Assembly Plan, as v1c did, added a wait that was never load-bearing. Phase 2.5 sits at the earliest point that is actually load-bearing: right after the map that formalizes 1.3's findings, right before the plan that only reorders them.

**Why this earns its own phase, not just a principle inside Execution:**
- It's the first point units get touched at all — a distinct transition, not a variation on the read-only phases before it or the content-heavy phase after it.
- It has its own, much cheaper validation — does every marker pair up? — answerable with one grep, versus Phase 5's full content/dependency validation.
- Skipping straight from an abstract map to copying content is exactly how a boundary gets re-derived from memory mid-execution instead of staying fixed in place — the failure the *Philosophy* section warns about, made concrete.
- The map lives in conversation context, which can be compacted or lost across a long task. Markers live on the units themselves, and survive it. A line number can also silently drift the moment anything above it in the file changes; a marker found by content-search cannot.

**Marker format.** Adapt the comment syntax to the unit's format — HTML/XML `<!-- -->`, CSS `/* */`, JS `//` or `/* */`, Python/YAML/shell `#`. For formats with no comment syntax at all (strict JSON, CSV, binary), this phase cannot touch the unit directly — the Build Map has to carry the full weight instead; say so explicitly rather than silently skipping the phase.

At every DESTINATION anchor, the marker takes a `sources` **list**, in insertion order — a one-element list for the ordinary case, so there is exactly one marker shape to learn, not two:

```html
<!-- in customer-account-1e-clean.html, replacing the TODO at line 523 -->
<!-- BUILD:INSERT sources=[build-001]
     ALSO: op=build-002 (script) -> new file customer-account-messages.js
     ALSO: op=build-009 (style)  -> new file customer-account-tab-messages.css
-->
```

At every SOURCE boundary, each contributing operation keeps its own individually-tagged pair:

```html
<!-- in account-messages-1b.html, at lines 289 / 576 -->
<!-- BUILD:EXTRACT START op=build-001 -->
<section class="messages-container ...">
  ...
</section>
<!-- BUILD:EXTRACT END op=build-001 -->
```

**Handling a MERGE — more than one source at one destination.** Nothing changes on the source side; each contributor still gets its own EXTRACT pair. The destination's `sources` list simply grows, and its order fixes insertion order:

```html
<!-- BUILD:INSERT sources=[build-001, build-004] -->
<!-- illustrative — Case Study A has no multi-source merges; this shape is
     what it would look like if two fragments' content combined at one anchor -->
```

Where one unit feeds more than one operation — the common case; see the "fragment decomposes into markup+style+script" note under Phase 2 — say so explicitly at the boundary rather than leaving it implicit:
```html
<!-- BUILD:NOTE this file also contains build-002 (script, lines 616-1761)
     and build-009 (embedded <style>) — separate operations, see their own markers -->
```

**Verification, before Assembly Plan starts:**
```bash
grep -rn "BUILD:EXTRACT START\|BUILD:EXTRACT END\|BUILD:INSERT" .
```
Flatten every `sources=[...]` list across all INSERT markers into one set of required op ids. For every id in that set: exactly one EXTRACT START, exactly one matching EXTRACT END, and it appears in exactly one `sources=[...]` list — not zero, not two. Anything less is a Phase 2.5 defect — cheaper to fix now, before Assembly Plan groups it and Execution moves it, than after.

**What this buys everything downstream.** Every source boundary and destination anchor is now a fixed, grep-verifiable coordinate — not a re-derived line number, not something held only in conversation memory. In this version, markers feed exactly one further step: Phase 2.6 (Cache Population) is the *only* phase that reads them to touch a source file at all. Every phase after that — Assembly Plan, Execution, Validation — works only against the cache Phase 2.6 produces, never against the original source again. This is a stronger guarantee than v1e's own: there, Execution still read the marker directly at copy time, which meant a long task with many markers still asked the model to reproduce marked content as output once, at the moment it mattered most. Here, that reproduction happens exactly once, earlier, into a durable record — and Execution never touches source content again at all.

**Cleanup.** Markers are scaffolding for exactly one phase — Cache Population. Once Phase 2.7 confirms every marked range has a corresponding validated cache entry, the markers may be stripped from the source files immediately; nothing downstream reads them again. State whether the project wants them stripped or kept as an audit trail, as before — but note that if kept, the marker trail is now a secondary record. The cache file is the primary one, and it's the one with hashes.

---

## The Cache-and-Commit Protocol

Phase 2.5 answers **where**. This section answers **what** — and, critically, makes "what" a durable fact that can be checked, rather than something that exists only for as long as the model is holding it in mind.

### Why a cache, and why it has to be a real file

A dependency can be fully and correctly identified — right dimension, right mode, right enforcement, right cardinality — and the operation can still fail, for a reason none of the Six Dimensions describe: the content that was supposed to move from source to destination never actually arrived, or arrived changed. That is not a dependency defect. It is a transfer defect, and it needs its own mechanism, not a seventh dimension bolted onto the existing six.

**This is not a seventh dimension.** The Six Dimensions ask whether *other* units are affected by an operation on U. The question here is different: did the operation *on* U itself execute the way the Build Map said it would? Conflating the two would repeat exactly the mistake *What Changed from v1a* diagnoses — forcing an orthogonal concern into a taxonomy it doesn't belong in. The *Catalog of Observed Patterns* is unchanged by this version for the same reason: it catalogs dependencies, not transfer failures.

The cache is a plain JSON file, external to the conversation, addressed by the same operation ids the Build Map already assigned. Three properties make it do its job:

- **Durable.** It's a file on disk, not a fact held in the model's running attention. Conversation context can be compacted, summarized, or simply run long enough that early details degrade — none of that touches a file.
- **Hash-stamped at every hand-off.** Every entry records a checksum of its own content the moment it's extracted, and that checksum gets recomputed and re-compared at every later point the entry is used.
- **Populated and validated by script, never by hand.** The model orchestrates *which* range goes into *which* entry — it does not type out the entry's content field itself. Hand-authoring JSON containing HTML/CSS/JS means manually escaping quotes, newlines, and backslashes, which reintroduces the exact transcription risk the cache exists to remove. A model that can mis-transcribe content into a destination file can just as easily mis-transcribe it into a JSON string. `json.dump()` (or equivalent) does the escaping; the model never does.

### Cache schema

```json
{
  "meta": {
    "cache_id": "customer-account-1f-merge",
    "build_map_ref": "build-map.json",
    "total_planned_ops": 14,
    "pipeline_status": "populating"
  },
  "entries": [
    {
      "op_id": "build-007",
      "source": {
        "file": "account-subscriptions-1c.html",
        "lines": { "start": 412, "end": 588 },
        "marker": "op=build-007"
      },
      "destination": {
        "file": "customer-account-1f.html",
        "anchor_marker": "BUILD:INSERT sources=[build-007]"
      },
      "content": "<section class=\"subscriptions-container\">...</section>",
      "content_length_bytes": 8421,
      "sha256_at_extraction": "3f9a1c…",
      "status": "pending",
      "sha256_post_commit": null
    }
  ]
}
```

`status` moves through exactly four values, in exactly this order, for every entry: `pending → extracted → validated → committed`. An entry that fails a check at `validated` or `committed` moves to `failed` and goes back to `pending` for that op id only — it does not block or invalidate any other entry.

### Phase 2.6 — Cache Population

Runs immediately after Phase 2.5's marker verification passes. For every operation in the Build Map:

```python
import hashlib

def populate_entry(op, source_text):
    start_tag = f'<!-- BUILD:EXTRACT START op={op["id"]} -->'
    end_tag   = f'<!-- BUILD:EXTRACT END op={op["id"]} -->'
    start = source_text.index(start_tag) + len(start_tag)
    end   = source_text.index(end_tag)
    content = source_text[start:end]
    return {
        "op_id": op["id"],
        "source": op["source"],
        "destination": op["destination"],
        "content": content,
        "content_length_bytes": len(content.encode("utf-8")),
        "sha256_at_extraction": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "status": "extracted",
    }
```

One rule governs this phase: **the range comes from the marker, and the entry's content field comes from the script's read of that range — never from the model recalling what the range probably contained.**

### Phase 2.7 — Cache Validation Gate

Blocks Phase 3 and Phase 4 outright until every check below passes for every entry. This is the phase that would have caught *What Changed from v1e*'s actual incident.

```python
def validate_cache(build_map, cache):
    planned = {op["id"] for op in build_map["operations"]}
    cached  = {e["op_id"] for e in cache["entries"]}

    missing = planned - cached
    extra   = cached - planned
    assert not missing, f"BLOCKING: {len(missing)} planned op(s) never entered the cache: {missing}"
    assert not extra,   f"BLOCKING: cache has op(s) the Build Map never planned: {extra}"

    for e in cache["entries"]:
        fresh = read_source_range(e["source"])                     # re-read from disk, not from the entry
        fresh_hash = hashlib.sha256(fresh.encode("utf-8")).hexdigest()
        assert fresh_hash == e["sha256_at_extraction"], f"{e['op_id']}: source drifted or extraction was wrong"
        assert tag_balance_ok(e["content"]), f"{e['op_id']}: content is not internally well-formed on its own"
        e["status"] = "validated"

    return True   # the only value that unblocks Phase 3/4
```

The `missing` check is a direct, mechanical answer to the question this document had no formal check for before this version: *does every planned operation have content behind it, yes or no.* For the `customer-account-1f.html` run, this check — had it existed — would have returned the two dropped tabs' op ids before Phase 4 ever ran, rather than a person discovering two blank tabs after the fact.

### Requirements Specification for the Content Cache

A cache is well-formed only if:

1. Every op id in the Build Map has **exactly one** entry — checked by set difference, not by eye.
2. Every entry's `sha256_at_extraction` was computed by re-hashing the actual extracted bytes, not copied from elsewhere or left as a placeholder.
3. Every entry's `content` was written by a script reading a marked range, never typed by the model into the JSON literal.
4. Every entry passes an internal well-formedness check (tag balance, at minimum) **before** it is eligible for commit — catching a truncated extraction at the earliest possible point, not after it's already in the destination.
5. `status` transitions are one-directional (`pending → extracted → validated → committed`, or `→ failed` back to `pending`) — nothing skips a state, and nothing is committed without having first been validated.
6. The cache file itself is queried, not fully loaded, once it grows large — see *Working with Many Units*, below.

### Downstream: how Phase 4 consumes a validated entry

Covered in full under *Workflow Structure → Phase 4 — Execution (Commit)*, below. In outline: read the validated entry, re-hash it immediately before splicing (catching anything that changed between validation and commit), splice, then hash the result and compare against `sha256_at_extraction` one more time. Three hash checks across the pipeline — at extraction, at validation, and at commit — not one.

---

## Reliability Model: Guarantees Borrowed from Systems Engineering

None of the ideas below are new. They're the standard toolkit for "how does a system guarantee a change either fully happened or didn't happen at all, in a way that survives an interruption" — the same problem a database or a distributed system solves for writes, applied here to content moving from one file to another during a build task.

**Write-ahead logging (WAL).** A database never writes a change directly to its data pages. It first writes the *intent* to a log, confirms the log entry is durably recorded, and only then applies the change — so that if the process crashes between the two steps, replaying the log recovers exactly what should have happened, no more and no less. The cache plays the log's role here: nothing is written to a destination file until its cache entry exists, is hash-verified, and is marked `validated`. If the conversation's context is compacted or the task is interrupted mid-run, the cache file on disk is the record of what's actually been confirmed — not anyone's memory of how far the task had gotten.

**Two-phase commit (2PC).** A transaction that touches multiple participants asks each one to *prepare* — confirm it can complete its part — before any of them *commit*. If even one participant can't prepare, the whole transaction aborts before anything is applied, rather than leaving some participants committed and others not. Phase 2.6–2.7 is the prepare phase: every operation is extracted and validated *before* Phase 4 commits any of them. An operation that fails validation blocks commit for that operation specifically — it does not get silently skipped while the rest proceed, and it does not get force-committed to "finish on schedule."

**Content-addressing and checksums.** Verifying a value once, at the moment it's created, proves nothing about whether it's still that value later. This pipeline hashes at three distinct hand-offs — extraction (2.6), validation (2.7), and immediately pre-splice (Phase 4) — and re-verifies at each one against the original, rather than trusting a single early check to hold for the rest of the pipeline's duration.

**Atomicity at the smallest safe unit.** The atomic unit here is one operation, not one task. A 14-operation merge in which 12 operations are extracted, validated, and committed correctly and 2 fail validation is not an 86%-successful merge — it's 12 completed atomic units and 2 correctly-identified incomplete ones, each independently visible in the cache's `status` field. Keeping the unit small is what makes a partial failure *legible* instead of just partial.

**Durability over volatile context — the central substitution this version makes.** Conversation context, across one long task, behaves like a process's volatile memory: it holds everything that's happening, right up until it's compacted, summarized, or the task ends — at which point anything that existed only there is gone. A cache file on disk behaves like durable storage: it survives exactly the events volatile memory doesn't. The rule this version adds is the same rule every reliable system already enforces about its own state: **if it isn't durably recorded and hash-verified, it hasn't happened yet, no matter how confident the process currently running feels about it.**

**Idempotency and resumability.** Because every entry carries a `status`, a run that's interrupted after committing 9 of 14 operations can resume by processing only the 5 entries not yet `committed` — re-running populate or validate against an already-`validated` entry is a safe no-op, not a re-extraction that risks producing a slightly different result the second time. This is what makes the pipeline safe to pick back up after exactly the kind of interruption that produced *What Changed from v1e*'s incident in the first place.

**Isolation.** One destination file's commit does not begin until the previous one's Phase 5 validation has passed — unchanged from v1e's "one file at a time," but now with an explicit reason: interleaving two destinations' commits is how a failure in one becomes indistinguishable from a failure in the other, when the report is written after the fact.

**Standing rule.** Nothing in this pipeline is treated as real until it is on disk and hash-verified at least twice. A value that exists only in conversation context, or that has been hashed once but not re-checked at its next hand-off, is still in flight — not yet a fact the pipeline is entitled to rely on.

---

### Phase 3 — Assembly Plan

By this point, every operation's entry and exit points are physically marked (Phase 2.5), and every operation's content is already extracted, hash-verified, and validated in the cache (Phases 2.6–2.7) — strictly more has been confirmed before this phase than in v1e, where Assembly Plan only had markers to rely on. This phase remains purely about execution **order**; it discovers nothing new.

Group by destination. Within a destination, order by: name-collision resolution and renames first, then shared-resource reconciliation once for the whole destination, then insertions in the order they'll read naturally, not the order their op ids happen to sort in.

```
Destination: customer-account-1e-clean.html (Case Study A's scenario)
  1. RENAME_FOR_COLLISION — build-004, build-009 (duplicate #summary-panel id)
  2. DEDUPE — jquery.slim.min.js (3 fragments load it; keep the shell's copy)
  3. INSERT — build-001 (Profile), build-002 (Orders), build-003 (Wishlist) ...
```

Nothing here changes what Phase 2.5 already marked or what Phase 2.6–2.7 already cached and validated — only the sequence Phase 4 commits it in.

### Phase 4 — Execution (Commit)

**Standing rule, unchanged from v1e:** for SPLIT/REORGANIZE, keep the original intact until Phase 5 confirms the new units reconstruct it.

**1. One destination at a time.** Unchanged.

**2. Read only from the validated cache — never from the source, never from memory.** By this phase, the source files are no longer part of the critical path. Every byte reaching a destination came from a cache entry already marked `validated` in Phase 2.7:

```python
def commit_op(destination_text, entry):
    anchor_tag = f'<!-- BUILD:INSERT sources=[{entry["op_id"]}'
    assert anchor_tag in destination_text, f"{entry['op_id']}: anchor not found"
    fresh_hash = hashlib.sha256(entry["content"].encode("utf-8")).hexdigest()
    assert fresh_hash == entry["sha256_at_extraction"], f"{entry['op_id']}: content changed since validation — do not splice"
    destination_text = destination_text.replace(anchor_tag, entry["content"], 1)
    entry["status"] = "committed"
    entry["sha256_post_commit"] = fresh_hash
    return destination_text
```
For a destination anchor fed by more than one op (`sources=[id1, id2, ...]`), commit each listed entry in list order and concatenate — Phase 2.5/2.6 already fixed that order.

**3. A cache entry that fails re-verification at commit time is a Phase 2.7 defect, not a Phase 4 workaround.** If the hash computed just before splicing doesn't match `sha256_at_extraction`, stop, do not splice, and send that one operation back to Phase 2.6 for re-extraction. Do not proceed with a value that may have drifted.

**4. Commit is scripted, not narrated.** The model's role is to invoke the commit step and read its result — not to describe, summarize, or reproduce the content being inserted anywhere in its own response. A commit that requires the model to retype the HTML/CSS/JS being moved, anywhere, is the exact anti-pattern this version exists to remove.

**5. Resolve a NAME collision and all its consumers in one operation.** Unchanged from v1e.

**6. Reconcile shared resources as one unified pass.** Unchanged from v1e.

**7. Preserve LIFECYCLE — both modes.** Unchanged from v1e.

**8. Re-audit BOUNDARY after any change in nesting depth.** Unchanged from v1e.

**9. Validate immediately after each destination — not at the end.** Unchanged from v1e.

### Phase 5 — Validation

**Level 0 — Completeness. New in this version, and it runs first.**
```bash
jq '.operations | length' build-map.json
jq '[.entries[] | select(.status=="committed")] | length' cache.json
```
If these counts differ, stop — do not proceed to Levels 1–3 — and identify by op id which planned operation never reached `committed`. This is the check that would have caught *What Changed from v1e*'s incident directly: 14 planned, 12 committed, and no prior version of this document ever compared those two numbers.

**Level 1 — Structural / Content-Preserving.** Now a second, independent confirmation rather than the first: Phase 4 already re-hashed each entry immediately pre- and post-splice, so a Level-1 pass here checks the destination file *as it currently sits on disk*, catching anything that altered it after a correct commit — not just re-confirming what commit already confirmed.

**Level 2 — Dependency Resolution, by Enforcement type.** Unchanged from v1e: grep-count for `CHECKED`, explicit diff for `CONVENTION_ONLY`.

**Level 3 — Syntax & Semantic Validity.** Unchanged from v1e: tag balance across the whole destination, no shared resource loaded twice, repeated-id vs. repeated-class judged by Cardinality. Applied to `customer-account-1f.html` during this version's own incident review, this check found the file's real markup fully tag-balanced end to end — the sole apparent mismatch traced to the word `<span` inside a comment, not a broken tag. That's a working instance of the base methodology's *Semantic — checking for legitimate exceptions*: a pattern match inside a comment isn't a violation. It's also the reason Level 0 has to be a separate, mandatory check rather than something inferred from Level 3 passing — a file can be perfectly tag-balanced and still be missing content entirely.

**Marker Cleanup Check.** Unchanged from v1e.

**Final Report:**
```
OP-ID      SOURCE → DESTINATION                     CACHED  VALIDATED  COMMITTED  HASH OK
build-001  ...messages → #tab-correspondence          YES      YES        YES       YES
build-013  ...subscriptions → #tab-subscriptions      NO — never entered the cache (1 of 14 planned ops)
build-014  ...item → #tab-item                        NO — never entered the cache (1 of 14 planned ops)
```
A row with no cache entry is a blocking row in this report — never a quiet omission.

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

Run against `account-messages-1b.html`, this finds the `<section class="messages-container">` opened at line 289 closing at line 576 — confirmed independently by the fragment's own closing comment, `<!-- /messages-container -->`. This is exactly the boundary Phase 2.5 plants its `BUILD:EXTRACT` markers around. The same technique generalizes to JS/JSON objects (`{ }`) and code (`( )`). Beyond a single well-known bracket type, use an actual parser.

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

`01` in the prefix never matches — the character right after it is `M`, not in `[a-h]`. The trailing `(?![a-zA-Z])` is a hardening guard, not something the spec states explicitly. Verified against every example in `version-control-1b.md`, plus this document's own filename → prefix `ai-task-execution-methodology-build-`, version `1d`.

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
11. Marker convention for this task's file types — the comment syntax to use
    in Phase 2.5, and confirmation that syntax is legal in every format involved
```

| Naive Spec Problem | Solution |
|---|---|
| "Just combine these files" | Explicit direction + destination unit name(s) |
| "Check the dependencies" | A composed descriptor per finding, not a single vague label |
| Collisions found during execution | Found in 1.3, resolved in the map — before a single byte moves |
| "Looks right" as the validation bar | Enforcement-appropriate check: grep-count for CHECKED, explicit diff for CONVENTION_ONLY |
| A dangling reference assumed to be a bug | Checked against scope first — it may be a different task's placeholder |
| One label forced onto a two-dimensional finding | `dimension` is a list — bootstrap is NAME *and* GENERATION at once |
| Plan exists only in conversation, not on the units | Phase 2.5 plants it as grep-verifiable markers before Assembly Plan even groups it |
| A marker format that only names one contributing operation | `sources=[...]` is always a list — one element for the ordinary case, more for a MERGE |

---

## Templates for Common Task Types

### Merge Fragments into a Shell (Many → One)
```
Phase 0:    confirm shell + fragment list + shared/scoped resources + destination
Phase 1:    role-classify; scan each fragment for its payload boundary (check for
            siblings like modals rendered outside the obvious container); run the
            Domino Algorithm across all six dimensions for shell + fragments + resources
Phase 2:    Build Map — EXTRACT_INSERT per fragment payload, DEDUPE per NAME/
            GENERATION conflict, RENAME_FOR_COLLISION per Cardinality violation
Phase 2.5:  plant BUILD:EXTRACT/INSERT markers at every boundary and anchor found
            in 1.3/Phase 2; verify pairing with one grep
Phase 2.6:  populate the cache — script-extract every marked range into a hash-
            stamped entry; the model never hand-types a cache entry's content
Phase 2.7:  validation gate — planned-op count == cache-entry count, every hash
            re-verified against a fresh source read, every entry tag-balanced
            standalone; proceed only once this holds for every single operation
Phase 3:    plan by destination — collisions/renames → shared-resource
            reconciliation → insertion in reading order
Phase 4:    commit from the validated cache only, one destination at a time;
            re-hash immediately before and after each splice
Phase 5:    completeness count first, then hash-match, dependency resolution
            by enforcement type, tag-balance
```

### Split a Monolith by Criterion (One → Many)
```
Phase 0:    confirm source + split criterion + destination unit list
Phase 1:    classify the criterion's dimension (usually POSITION or a NAME
            grouping); scan for cross-references between the pieces that will result
Phase 2:    Build Map — SPLIT + RELINK for every reference that will cross a new
            boundary once the pieces are separated
Phase 2.5:  mark each resulting piece's boundary in the source, and each RELINK's
            new target anchor in whichever destination will hold it
Phase 2.6:  populate the cache — one entry per resulting piece, hash-stamped
Phase 2.7:  validation gate — piece count == cache-entry count; every piece
            internally tag-balanced; every RELINK's new target confirmed to exist
Phase 3:    order destination files by dependency (a piece another piece
            imports from is written first)
Phase 4:    commit each piece to its own destination from the cache; update
            RELINKs last, once every piece exists
Phase 5:    completeness count, then confirm the split set still reconstructs
            the original when concatenated in source order (before markers
            are stripped) — the SPLIT-specific analog of a hash check
```

### Extract a Shared Resource and Relink Consumers
```
Phase 0:    confirm the N consumers, the common content, and the new shared
            unit's destination
Phase 1:    verify the content really is identical across all N (not just
            similar) — a near-miss here becomes a false DEDUPE later;
            find every consumer's reference to the now-duplicated content
Phase 2:    Build Map — one EXTRACT (content → new shared unit), N RELINK
            operations (each consumer → reference the new unit instead)
Phase 2.5:  mark the extraction boundary once; mark each of the N relink points
Phase 2.6:  populate the cache — one entry for the extracted content; the N
            relinks don't need cache entries (no content moves for them, only
            a reference changes) but do need their own Build Map ops tracked
            through the same status field for the Level 0 count
Phase 2.7:  validation gate — the shared unit's entry is hash-verified; all N
            relink targets confirmed to point at the new unit's actual path
Phase 3:    create the shared unit first, always — every relink depends on it
            existing before it can be pointed at
Phase 4:    commit the shared unit from cache; then update all N consumers
            in one pass so no consumer is left referencing the old, now-
            duplicated copy
Phase 5:    completeness count (1 extraction + N relinks, all committed);
            confirm no consumer still contains its own copy of the content
```

### Reorganize by a New Grouping (Many → Many)
```
Phase 0:    confirm the current units, the new grouping criterion, and the
            resulting destination set
Phase 1:    classify every unit's role under the *new* grouping (not the old
            one); domino-check every NAME and BOUNDARY relationship that the
            regrouping could change, since REORGANIZE touches the most units
            of any of the four directions
Phase 2:    Build Map — likely a mix of MOVE, SPLIT, MERGE, and RELINK
            operations, one per unit that changes destination or reference
Phase 2.5:  mark every unit's boundary in its current location and its anchor
            in its new one — this direction has the most markers of the four,
            so verify the grep-count twice
Phase 2.6:  populate the cache — one entry per unit that physically moves
Phase 2.7:  validation gate — same checks, applied to the largest operation
            count of the four directions; do not shortcut this because the
            task is large — large is exactly when Level 0 earns its keep
Phase 3:    order by new-destination dependency, same as Split
Phase 4:    commit destination by destination, exactly as above
Phase 5:    completeness count, then re-run Phase 1's role classification
            against the result — every unit should now classify under the
            new grouping the same way Phase 1 predicted it would
```

---

## AI Checklist Upon Receiving a Task

```
□ Confirmed the direction and exact destination unit(s) — not assumed from names?
□ Assigned every unit a role before reading a single line of content?
□ Scanned for structure before reading full content anywhere a scan would answer it?
□ Checked every candidate identifier against ALL SIX dimensions, not just the
  one that was obvious at a glance?
□ Checked for siblings (modals, popovers, anything rendered outside its
  trigger's container on purpose) that belong with the payload but live
  outside its obvious NESTING boundary?
□ For every CONVENTION_ONLY finding, explicitly diffed both sides — not
  trusted the absence of an error?
□ Checked whether a dangling reference belongs to a DIFFERENT, not-yet-started
  task rather than assuming it's this pass's bug?
□ Planted BUILD:EXTRACT/INSERT markers right after the Build Map (2.5) — not
  after Assembly Plan — so every ALSO: note reflects the full domino analysis?
□ If markers can't physically exist in this file format, said so explicitly
  rather than silently skipping the Marking Pass?
□ Verified every op id in every sources=[...] list has exactly one matching
  EXTRACT START/END, and appears in exactly one sources=[...] list?
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
□ Cleaned up (or intentionally kept) every planted marker before delivery?
□ For a split: would re-analyzing the output reproduce the same boundaries started from?
□ Does every planned operation have exactly one entry in the cache — checked by set comparison, not by skimming the file?
□ Was every cache entry's hash re-verified against a fresh read of its source, not just trusted from extraction time?
□ Was every cache entry checked for internal well-formedness on its own, before it ever reached a destination?
□ Was the cache populated by a script — never hand-authored JSON containing the model's retyped version of the content?
□ Did commit re-hash each entry immediately before splicing, and refuse to splice on a mismatch?
□ Does the final report's planned-vs-committed count get compared programmatically, not eyeballed?
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
Not hypothetical: this is exactly what happened partway through this methodology's own first real run — a hand-typed `new_str` for `build-001` didn't match the file (the retyped version silently diverged from what was actually extracted), the edit tool rejected it on a failed match, and the fix was switching to a script that pulled the already-verified bytes directly. Caught immediately because the mismatch was total; a *partial* divergence — one dropped attribute, one renumbered class — would not have been.

### ❌ Jumping From Map Straight to Copying, Skipping the Marking Pass
```
Bad:  Build Map is done — start editing files directly, re-deriving each
      boundary from the map's line numbers (or memory) as you go
Good: plant BUILD:EXTRACT/INSERT markers first, grep-verify every one pairs
      up, THEN copy against the markers
```
Reason: a line number recorded in Phase 2 can drift the moment anything above it changes; a marker found by content-search can't. Skipping straight to copying also means the first sign of a mismatched plan shows up mid-edit, with content already half-moved, instead of in one cheap grep before anything moved at all.

### ❌ Waiting for the Assembly Plan Before Marking
```
Bad:  finish grouping and ordering operations (Phase 3) before planting any
      BUILD:EXTRACT/INSERT markers
Good: mark immediately after the Build Map (Phase 2.5) — Assembly Plan then
      groups and orders operations that are already physically marked
```
Reason: Assembly Plan only reorders what Phase 2 already fully knows — it discovers nothing new, so it isn't a real prerequisite for marking. What genuinely is a prerequisite is Phase 1.3's domino analysis, which is what the marker's `ALSO:` notes are actually reporting. Marking before 1.3 finishes would produce incomplete markers; waiting past Phase 2 to mark — as an earlier version of this methodology did — adds a dependency that was never real.

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

### ❌ Trusting a Cache Entry Without Re-Hashing It
```
Bad:  extract once, assume it's still correct by the time commit runs
Good: re-verify the hash at validation (2.7) AND again immediately before
      the splice (Phase 4) — two checks, at two different times, not one
```

### ❌ Hand-Authoring the JSON Cache
```
Bad:  the model writes out "content": "<section>...</section>" by typing
      the escaped JSON itself
Good: a script reads the marked byte range and calls a JSON serializer —
      escaping is never something the model does by hand
```
Reason: hand-authoring the cache reintroduces the exact transcription risk the cache exists to remove — a model that can mis-transcribe content into a destination file can just as easily mis-transcribe it into a JSON string.

### ❌ Committing Before the Validation Gate Passes
```
Bad:  cache 12 of 14 operations, notice time or context is short, commit
      what's cached and call the merge done
Good: Phase 2.7 blocks Phase 4 outright until planned-op count equals
      cache-entry count; an incomplete cache is a stop condition
```
Reason: this is, concretely, what produced *What Changed from v1e*'s incident — two operations were never in any cache, because there wasn't one, so nothing ever compared 14 planned against 12 landed.

### ❌ Treating a Fully Tag-Balanced File as Proof of Completeness
```
Bad:  the whole destination parses cleanly, every tag balances → assume
      nothing is missing
Good: a bare TODO comment or an empty dynamic-render container is also
      tag-balanced; completeness (Level 0) and structural validity
      (Level 3) are different questions, and only one answers the other
```
Reason: `customer-account-1f.html`'s two dangling tabs didn't break tag balance anywhere — an HTML comment is syntactically valid on its own. A file can be perfectly well-formed and still be missing two-fourteenths of its content.

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

**What the Marking Pass looks like for this case** (Phase 2.5, right after the Build Map, before Assembly Plan groups anything):
```html
<!-- in customer-account-1e-clean.html, replacing the TODO at line 523 -->
<!-- BUILD:INSERT sources=[build-001]
     ALSO: op=build-002 (script) -> new file customer-account-messages.js
     ALSO: op=build-009 (style)  -> new file customer-account-tab-messages.css
-->
```
```html
<!-- in account-messages-1b.html, at lines 289 / 576 -->
<!-- BUILD:EXTRACT START op=build-001 -->
<section class="messages-container ...">
...
</section>
<!-- BUILD:EXTRACT END op=build-001 -->
```
One command — `grep -rn "BUILD:" *.html` — confirms `build-001` has exactly one START, one END, and appears in exactly one `sources=[...]` list, before Assembly Plan groups it or Execution touches a single byte of the actual payload.

**Update — this case has since been run end-to-end, not just planned.** It turned out to need a two-element `sources` list after all: `account-messages-1b.html` has a delete-confirmation modal sitting *outside* `.messages-container` (lines 587–607, a sibling, not a child — see *What Changed from v1d*). The real destination marker is `sources=[build-001, build-015]`, `build-015` being the modal, inserted right after `build-001`'s content lands. Phase 1.2's `modal` grep (added in v1e) is what would catch this during analysis instead of during a post-hoc id count.

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

### Case Study D — Fourteen Tabs, Twelve Landed

`customer-account-1f.html`: a 14-tab shell, 2,714 lines / 166,082 bytes, alongside 11 already-extracted per-tab CSS files (1.1–15.2 KB each) and 11 already-extracted per-tab JS files (5.3–62.9 KB each) — over three times the scope of Case Study A. All 14 `data-target`/`id` pairs resolved correctly; all 22 CSS/JS references resolved correctly; a full tag-balance pass found the markup sound end to end.

Two tab-panes — `tab-subscriptions` and `tab-item` — contained nothing past their header chrome except one unfilled comment each:
```html
<!-- TODO: insert tab content here — account-subscriptions -->
```
No `BUILD:` marker of any kind appeared anywhere in the file — this run predates this version's discipline entirely. Nothing in the process ever compared "operations planned" against "operations landed," so nothing caught that two of fourteen never did.

| Check | Result |
|---|---|
| NAME (`data-target` ↔ `id`, 14 pairs) | all resolved |
| NAME (`<link>`/`<script src>`, 22 refs) | all resolved |
| Tag balance, whole file | sound (one apparent `span` mismatch traced to a comment, not a defect) |
| Completeness (14 planned vs. filled) | 12 of 14 — two bare TODOs |

Every check this case passed is a check v1e already specified. The one that would have caught the actual defect — completeness — didn't exist as a formal step anywhere before this version. Phase 2.7's gate and Phase 5's Level 0 exist specifically to close this gap.

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
grep -rn "BUILD:EXTRACT\|BUILD:INSERT" .            # after 2.5: confirm every op id pairs up
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

**The cache file is subject to the same discipline.** On a large task, the cache can grow to hold dozens of sizeable entries — do not load the whole cache into context to check one operation's status. Query it the same way structure gets scanned elsewhere in this document:
```bash
jq '.entries[] | select(.op_id=="build-007") | .status' cache.json
```

---

## Execution Quality Metrics

### After Completing the Work, Ask Yourself:
```
0.  Does planned-operation count equal committed-and-hash-verified count,
    exactly - checked programmatically, not eyeballed? (New in this version;
    this is the check "What Changed from v1e" shows was previously absent.)
1.  Does the number of operations in the Build Map equal the number
    resolved in the final report?
2.  Was every dependency finding resolved by its actual Enforcement type -
    grep-count for CHECKED, explicit diff for CONVENTION_ONLY - rather
    than assumed resolved because nothing errored?
3.  For every BOUNDARY finding, was legality re-checked after the
    operation, not just before?
4.  For every LIFECYCLE finding, do both modes (IDENTITY and
    COMPLETENESS) still hold after the operation?
5.  Were markers stripped or deliberately retained - a decision made, not
    an oversight?
6.  Would re-running Phase 1's role classification against the finished
    result reproduce the same roles Phase 1 assigned at the start?
```

### Numerical Indicators to Log Before/After
- Operations planned vs. operations committed vs. operations still `pending` or `failed` in the cache
- Cache entries: populated vs. validated vs. committed, and how many needed re-extraction after failing validation once
- Hash mismatches caught at each of the three checkpoints (extraction, 2.7, Phase 4) - ideally zero, but a non-zero count here is signal that the gate is doing its job, not just noise
- File count, line count, and byte count before and after, per destination
- Dependency findings by Enforcement type (CHECKED vs. CONVENTION_ONLY) and how each was actually verified

---

*This methodology is a companion to `ai-task-execution-methodology.md`. Version 1b replaced v1a's eleven-item enumerative taxonomy with a compositional model. Version 1c added a Marking Pass. Version 1d repositioned it to Phase 2.5 and generalized its marker to a `sources=[...]` list. Version 1e was the first revision informed by an actual Phase 0–5 run rather than reasoning about the model in the abstract. Version 1f is informed by a second real run — a 14-tab merge, `customer-account-1f.html`, in which every dependency check this document already specified passed cleanly, and the defect that shipped anyway (two of fourteen tab-panes left as bare TODO comments) was one this document had no formal check for: not "is this correct" but "did this happen at all." The Cache-and-Commit Protocol, and the Reliability Model that motivates it — write-ahead logging, two-phase commit, hash verification at every hand-off, durability over conversation context — exist to make that count a mandatory, mechanical gate rather than something a person has to remember to run. The three original illustrative sources remain as Case Studies A–C; Case Study D is the source of this version's own finding, in the same spirit.*
