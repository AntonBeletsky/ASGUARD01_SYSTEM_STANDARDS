# LLM Operational Platform
## Task Execution Methodology — Full Reference (Architecture and Implementation, Unified)

---

## What this document is

**LLM Operational Platform** — or simply **Operational Platform** — is
the name of this project: a six-phase task-execution methodology and,
inline, phase by phase, exactly which command, field, and file of a real
working implementation (`llm-assembler`, a skill for line-precise batch
editing of text and code) satisfies each requirement. Reading only this
document is enough to use the system.

Two leaner companion documents exist and are not needed to use this one:
`llm-operational-platform-task-execution-methodology.md` states the architecture with zero
implementation detail, for reuse in a domain that isn't line-oriented text
at all; `llm-assembler/SKILL.md` plus its `references/` are the
implementation's own operating instructions, for someone who wants to use
the tool without reading about the methodology it happens to implement.
This document is the merge of both, kept in sync with the same tested
code — where it states a behavior, that behavior has an automated test
backing it, not just a description of intent.

---

## Core Philosophy

Any non-trivial task decomposes into three stages that must never be merged:

```
ANALYSIS → PLAN → EXECUTION
```

Merging these stages is the primary source of error: acting before the
full scope of work is understood leads to omissions, cascading failures,
and rework. This is the one rule everything else in this document exists
to protect.

These three stages expand into six operational phases:

| Stage | Phase(s) |
|---|---|
| Preparation | Phase 0 — Context Loading |
| Analysis | Phase 1 — Analysis |
| Plan | Phase 2 — Task Map · Phase 3 — Execution Plan |
| Execution | Phase 4 — Execution |
| Verification | Phase 5 — Validation |

### Interruption is not a special case

Any phase can be interrupted before it completes — mid-load, partway
through a taxonomy sweep, mid-batch. A methodology that only accounts for
a clean, uninterrupted run is describing the easy case and leaving the
common one undefined. Two properties make interruption survivable:

- **Every phase's output is a durable artifact, not a mental state.**
  Progress is exactly what's recorded so far — nothing that matters lives
  only in the reasoning that produced it.
- **Resuming means reading that artifact, not restarting the phase.**

**Concrete, in llm-assembler:** `checkpoint.json` is overwritten — never
appended — on every phase transition and every applied edit, and is the
one file a fresh session reads before anything else:

```
python3 scripts/cli.py resume
```

This reads the checkpoint, reports the real status of whatever batch was
active, and — if the last thing that happened was an unresolvable
discrepancy (see Phase 4) — pulls the actual diagnostic out of the
validation log instead of making you go find it. `wal.jsonl`, an
append-only log of what started and what finished applying, is what makes
resuming *safe*, not just possible: see "Three outcomes, not two" under
Phase 4 for exactly how a resumed session tells "this was already done"
apart from "this was never started."

---

## Phase 0 — Context Loading

**Purpose:** establish complete, confirmed situational awareness before
any analytical or productive work begins.

**Required tasks:**
- Load the governing reference against which correctness will be judged.
- Load all materials that are the subject of the work.
- Establish constraints: what must not be touched, what is critical, what
  takes priority.
- Explicitly confirm that loading is complete before proceeding.

**Governing rule:** no transformation or corrective work happens in this
phase — only intake and confirmation.

**Rationale:** context that is incomplete or misunderstood invalidates
every downstream conclusion. Errors introduced here propagate through
every later phase.

**On constraints specifically:** establishing a constraint in this phase
is not the same as enforcing it later. A constraint that is only ever
written down and never mechanically checked against the plan before
execution is a note, not a guardrail. Phase 3 is where that check
belongs.

### Concrete: llm-assembler

| Requirement | Command |
|---|---|
| Load the governing reference | No dedicated command — ordinary reading of the spec, ticket, or standard, with whatever tool already has it. Nothing about this step is text-domain-specific enough to mechanize. |
| Load subject material | `python3 scripts/cli.py register <path>`, once per file the task will touch. Idempotent — safe to call again if you're not sure it's already registered. |
| Establish constraints | `python3 scripts/cli.py add-constraint <batch_id> --file PATH --start ID --end ID --reason TEXT` |
| Confirm loading is complete | `python3 scripts/cli.py show-file <path>` — prints every live line with its current id and position; read it back before trusting it. |

`register` assigns a permanent `line_id` to every line in the file *at
its position when registered* — this is the single mechanism the rest of
the system is built on. A line's position drifts every time something
above it is inserted or deleted; addressing edits by id instead of by
number is what makes every later phase's location references survive
that drift instead of silently going stale. See Phase 2's "Location
reference" row for why this matters enough to be the foundation rather
than a detail.

`add-constraint` needs an open batch, so in practice it's called right
after Phase 3's "Open a batch," not literally before Phase 1 begins — the
ordering that matters is *before any descriptor could violate it*, not
*before anything else happens*. It's optional: most batches don't need a
protected zone declared at all. When declared, it's re-resolved against
the live registry every time it's checked, never against a cached
position — a protected range addressed by stale coordinates would be
exactly the bug this whole system exists to avoid.

---

## Phase 1 — Analysis

**Purpose:** systematically examine all loaded material against the
reference, identifying every deviation — without acting on any of them
yet.

### 1.1 Category Taxonomy
Establish an exhaustive, named classification of possible deviation types
**before** examining individual material. A category that is never
defined can never be searched for; an analysis without a taxonomy is
structurally incomplete.

### 1.2 Systematic Cross-Examination
Examine each unit of material against each defined category, in a fixed,
sequential order — unit × category — without skipping ahead. Use
structured, layered questioning to surface deviations methodically rather
than opportunistically.

### 1.3 Dependency Analysis ("Domino")
For every identified deviation, determine everything else that would
break or become inconsistent if only that single point were corrected in
isolation. This cascade analysis must be exhaustive — an incomplete
cascade produces a broken or inconsistent result once execution begins.

**Three distinct activities, only one of which resists automation.**
Tracing a cascade decomposes into: *searching* the material for places
that might be affected (a matter of coverage), *judging* which candidates
are genuine cascades versus coincidental (a matter of understanding what
the material means, not just what it contains), and *ordering* the
resulting dependencies once known (a matter of respecting them
correctly). Searching and ordering are mechanical and verifiable; judging
is not, and no correctness in the other two compensates for a candidate
wrongly accepted or wrongly dismissed.

**For material carrying its own embedded logic, judging requires reading
that logic, not only searching text.** A dependency can exist with no
shared wording anywhere — one part's logic silently assumes another part
still exists in a specific place, and nothing about that assumption is a
recurring string. Mechanical search produces no candidate for this kind
of cascade regardless of how exhaustive it is; judging it means reading
the dependent logic itself for what it hard-codes or assumes.

**This is its own pass, sequenced strictly after 1.2 closes, never
interleaved with it** — the ANALYSIS→PLAN→EXECUTION rule from Core
Philosophy, applied one level down. **It is durable and resumable**: each
deviation from 1.2 becomes an item with its own traced-or-not status, a
unit of progress deserving the same treatment applying one planned
change gets in Phase 4. **Nothing proceeds past it with an untraced
item** — the same "catch it before anything is touched" reasoning as
Phase 3's Plan Validation, one phase earlier.

### Concrete: llm-assembler

```
python3 scripts/cli.py sync-domino-queue <batch_id>
python3 scripts/cli.py domino-next <batch_id>
python3 scripts/cli.py domino-resolve <batch_id> <finding_id>
python3 scripts/cli.py domino-status <batch_id>
```

| Requirement | Command |
|---|---|
| 1.1 Taxonomy, defined before examining material | `add-category <batch_id> --code CODE --description TEXT`, called before any descriptor references the code. Enforced immediately, not deferred to a later check. |
| 1.2 Unit × category cross-examination | Not a command. `show-file` supplies the material; the taxonomy from 1.1 supplies the categories. The judgment of "does this line violate that category" is the reasoning step this system exists to support, not replace. |
| 1.3 Search | `domino-next`, mechanical: scans *every* registered file (`registry.scan_pattern` — the same primitive Phase 5's invariant check runs, just proactively instead of after the fact) for a finding's `domino_hint` or current content, filtered against everything already covered by a descriptor already in the batch. |
| 1.3 Judgment | Not a command. Deciding whether a candidate `domino-next` returns is a real cascade stays exactly as unmechanized as dependency discovery always was — the search narrows what needs a look, it doesn't replace looking. For material with its own embedded logic, this includes reading that logic directly for structural assumptions a text search can't surface (see Limitations). |
| 1.3 Ordering | `--depends-on <descriptor_id>` on `add-descriptor`, honored as a hard constraint by Phase 3's planner, which refuses to guess if ordering is ambiguous or cyclic. |
| 1.3 Durability / resumability | Every finding is a `pending`→`traced` entry in its own queue file; `domino-resolve` is WAL-backed and idempotent the same way applying a planned change is (Phase 4) — a session that drops mid-trace resumes rather than repeating findings already resolved. |
| 1.3 Gate | `validate-plan` (Phase 3) refuses outright, before any other check, if any finding is still `pending`. |

Taxonomy is optional and worth skipping for a small, single-purpose
batch — a plain rename doesn't need a category system. Reach for it when
the task itself has the shape of "find and classify issues" rather than
"make this one specific change."

Every direct finding from 1.2 gets queued for 1.3 by `sync-domino-queue`
(idempotent — safe to call again as more findings are added). Domino
tracing doesn't recurse: a descriptor produced *by* tracing (tagged
`--provenance domino --domino-of <finding's descriptor_id>`) is never
itself queued for its own trace — cascades of cascades are a deliberate
scope boundary, not an oversight; see Limitations. `domino-resolve` never
takes a self-reported count of cascades found — it recounts descriptors
that actually reference the finding, the same "recompute from what's
actually on disk" discipline Phase 4's fault recovery already applies to
"is this done yet."

---

## Phase 2 — Task Map

**Purpose:** convert the analysis into a structured, verifiable
artifact — not a narrative list — that captures every issue and its
relationships.

### Conceptually Required Attributes

Each recorded issue must carry:

| Attribute | Function | Concrete: descriptor field |
|---|---|---|
| Unique identifier | Enables reference from elsewhere, especially from dependencies | `descriptor_id` |
| Category | Ties the issue to the taxonomy defined in Phase 1.1 | `category`, checked against `taxonomy.json` |
| Severity | Determines execution priority | `severity` |
| Change type | Distinguishes the nature of the required transformation | `op` |
| Location reference | Precise and unambiguous enough to find and re-verify without re-deriving it | `start`/`end` (or `after`) — a `line_id`, never a raw line number |
| Current state / expected state | Recorded as two distinct values, never blended into one description | `expect_hash` (current) / `payload_ref` (expected) |
| Dependencies | Expressed as verifiable references to other issue identifiers, not free text | `depends_on`, a list of other `descriptor_id`s |
| Status | Tracks progress through the workflow | `status`: `pending` → `applied`, set only by the apply step, never by hand |
| *(not named explicitly by the abstract methodology)* | Where a finding came from — ordinary cross-examination or a domino trace — so Phase 5's final report can honestly break the two down | `provenance` (`direct`/`domino`) + `domino_of` |

A complete descriptor, in the concrete format:

```json
{
  "descriptor_id": "d0001",
  "op": "replace_range",
  "file_id": "f_98a15f28da",
  "start": "f_98a15f28da_l00001",
  "end": "f_98a15f28da_l00001",
  "after": null,
  "dest": null,
  "payload_ref": "1565ad0cf2da7c35",
  "expect_hash": "5ffdad1847bc",
  "depends_on": [],
  "category": "NAMING",
  "severity": "major",
  "provenance": "direct",
  "domino_hint": null,
  "domino_of": null,
  "context": null,
  "rule_ref": null,
  "status": "pending"
}
```

`expect_hash` and `payload_ref` deserve a specific note: they aren't
prose descriptions of current/expected state, they're a hash and a
content-addressed reference to a blob. This is what turns "current state
/ expected state, recorded as two distinct values" from something a
human reads into something a machine can check without a human in the
loop — see Phase 4's "reality is checked before it is changed." What a
hash doesn't do is give a reviewer anything to look at without
dereferencing it — that's what the optional `context` field is for: up
to 120 characters, human-readable, purely advisory, never itself
checked. `rule_ref` is similarly advisory — a free-text pointer at the
specific clause of governing material a finding answers to, unvalidated
because Phase 0 loads that material by reading, not by parsing it.

### Severity

A tiered scale that separates:
- Violations of fundamental / architectural invariants (highest priority) — `critical`
- Violations of standards carrying broad structural or scaling risk — `major`
- Deviations that are "noise" — they don't affect function but degrade quality — `minor`
- Purely cosmetic deviation (lowest priority) — `cosmetic`

Severity is what makes execution order determinable — see Phase 3.

### Change Type

A fixed, closed vocabulary describing the nature of each transformation.
Concretely, five operations, deliberately narrow and non-overlapping so
each is easy to verify in isolation:

| Operation | Effect |
|---|---|
| `insert_after` | inserts new content after an anchor line (or at the very top, via the anchor `START`) |
| `delete_range` | removes a contiguous range |
| `replace_range` | removes a range and inserts new content in its place |
| `move_range` | relocates a range, preserving its identity (its ids travel with it) |
| `copy_range` | duplicates a range's content elsewhere, as new ids |

Anything more complex than one of these five is a sequence of them,
composed — there is no sixth primitive, on purpose. A narrow, orthogonal
set of operations is what makes every one of them cheap to check
mechanically; a "smart" operation that tries to do several things at once
is harder to verify and harder to reason about when something goes wrong
partway through it.

### The map is a snapshot, not a promise

A task map records the state of the material as understood when Phase 1
examined it. Nothing about recording an issue guarantees the material is
still in that state by the time Phase 4 acts on it. The map is not
re-validated by the mere fact of having been written down — what that
requires is stated in Phase 4.

**Concrete:** `expect_hash` is exactly this snapshot, made checkable. It
is computed once, from the live file, at the moment a descriptor is
added — never edited by hand afterward. If what it should match changes,
the correct response is a fresh descriptor, not a patched hash.

---

## Phase 3 — Execution Plan

**Purpose:** convert the task map into an actionable, trackable,
hierarchically organized plan.

### Structure
- Top-level grouping: one natural unit of work per group.
- Subgrouping: one category/type of issue per subgroup.
- Leaf items: individual issues, each carrying a trackable status.
- Dependency items execute together with their parent issue — never as
  independent, separately scheduled items.

### Execution Priority
1. Primary ordering: by severity, most fundamental first.
2. Secondary ordering within a severity tier: by number of dependencies —
   items with more cascading effects are executed sooner, since they
   affect more of the system.

### Plan Validation

Before any item in the plan is acted on, the plan as a whole must be
checked — not each item as it comes up, but the complete plan, once:

- every dependency reference resolves to an issue that actually exists;
- no dependency ordering is contradictory (a cycle);
- no planned change targets a Phase-0 constraint.

This belongs here, before Phase 4, because it is the last point at which
finding a problem costs nothing — nothing has been changed yet. The same
check performed mid-execution finds the same problem after some of the
plan has already been acted on, which is strictly more expensive to
recover from.

### Concrete: llm-assembler

```
python3 scripts/cli.py validate-plan <batch_id>
```

One command performs the entire Plan Validation requirement above:
schema-checks every descriptor, resolves every target against the live
registry, checks every target against every declared constraint, and
builds a conflict graph over all descriptors targeting the same file —
two descriptors whose resolved ranges intersect are a conflict unless one
explicitly `depends_on` the other, in which case that becomes an ordering
edge instead. The graph is topologically sorted into a safe `apply_order`
(Kahn's algorithm); a cycle or an unresolved conflict fails the whole
call with a precise diagnostic — which descriptors, which lines — rather
than picking an arbitrary order and hoping.

**Execution Priority is the tie-break inside that sort, not a separate
step.** Every hard `depends_on` edge and every conflict-forced ordering
is respected regardless of severity — severity only decides between
descriptors that are already free to run in either order at a given
point in the sort:

- If no descriptor in the batch sets `severity`, ties break by original
  insertion order.
- If any descriptor sets `severity`, ties break by severity first
  (`critical` → `major` → `minor` → `cosmetic`, unset counts as lowest),
  then by how many *other* descriptors list this one in their own
  `depends_on` — more first, since it's unblocking more of the batch —
  then by insertion order as a final tiebreak.

There is no "apply anyway" path past a failed `validate-plan`: `apply-next`
will not act on a batch that hasn't produced a valid `apply_order`.

---

## Phase 4 — Execution

**Purpose:** apply planned changes in a controlled, risk-minimizing
sequence.

**Governing principles:**

1. **Reality is checked before it is changed.** Immediately before acting
   on a planned item, confirm the material still matches what Phase 1
   recorded for it — not what the plan assumes, what is actually there
   right now. Skipping this and trusting the plan directly is how a
   correct analysis produces an incorrect result when acted on late
   enough for something to have changed underneath it.
2. **Single-unit focus.** Work is completed fully on one unit before
   moving to the next. Units are never interleaved mid-way.
3. **Immediate dependency resolution.** When an issue carries dependency
   items, all of them are resolved in the same pass as the parent
   issue — never deferred to "later."
4. **Layered passes.** Complex units are processed through multiple
   sequential passes, each addressing one logical dimension rather than
   attempting all dimensions simultaneously.
5. **Specific-before-general ordering.** Where multiple changes could
   overlap, the most specific change is applied before the most general
   one, so a general change cannot silently absorb or invalidate a more
   specific case that hasn't been applied yet.
6. **Incremental validation.** Each unit is validated immediately after
   its changes are applied — before moving to the next unit.

### Three outcomes, not two

The result of attempting to act on a planned item is not simply success
or failure:

- **Confirmed.** Reality matched the plan; the change was applied.
- **Already satisfied.** Reality no longer matches the plan's *starting*
  state, but matches what the plan's *ending* state would have been — the
  change is already present. Not a failure; the plan's record needs
  updating, nothing needs redoing.
- **Unresolvable.** Reality matches neither the starting nor the ending
  state. Something changed that the plan did not anticipate. This is the
  only one of the three that should stop forward progress — cleanly,
  leaving the material exactly as found.

### Concrete: llm-assembler

```
python3 scripts/cli.py apply-next <batch_id>
```

Applies exactly one descriptor — the next one in `apply_order` not yet
`applied` — and stops, which is what makes single-unit focus (principle
2) and immediate dependency resolution (principle 3) automatic rather
than something to remember: a `depends_on` descriptor is already in the
same `apply_order`, resolved in the same pass as whatever it depends on,
with no separate "later" queue to defer to.

**Principle 1, "reality checked before changed," and the three outcomes
above map onto `apply-next`'s result field exactly:**

| Abstract outcome | `apply-next` result | What actually happens |
|---|---|---|
| Confirmed | `applied` | Live content matched `expect_hash`; the edit was written, the registry updated, `wal.jsonl` records `op_applied`, `status` becomes `applied`. |
| Confirmed (idempotent replay) | `skipped` | `status` was already `applied` — a safe no-op, not a re-edit. |
| Already satisfied | `recovered` | Live content matched neither the pre-state nor was `status` set, but the WAL already shows `op_applied` for this descriptor (a prior run got the write done but was interrupted before recording it) — or, for ops that add positively-checkable content, the live content at the target already equals what the descriptor would have produced. Either way: bookkeeping is reconciled, the file is not touched again. |
| Unresolvable | `abort` (exit code 1) | Live content matches neither the expected pre-state nor a plausible post-state. The file is left exactly as found. The correct response is re-planning, not retrying the same call. |

This is also the concrete mechanism behind "interruption is not a special
case" from Core Philosophy: `wal.jsonl` writes `op_start` before a
mutation and `op_applied` immediately after, and `apply-next` checks for
that `op_applied` record *before* doing anything else. A session that
dies between the file write and the bookkeeping that follows it produces
exactly the `recovered` case on the next attempt — not a duplicated edit,
not a stuck batch.

**Specific-before-general (principle 5) is deliberately not mechanized.**
There is no notion in the engine of one descriptor being more "specific"
than another — range size isn't a reliable proxy (a one-line change can
be the general case; a ten-line change can be the specific exception).
Where this ordering matters, express it as an explicit `--depends-on`;
the conflict graph only forces an ordering when ranges actually overlap,
so a non-overlapping specific/general pair still needs the ordering
stated by hand if it matters semantically. This is a considered scope
boundary, not an oversight — a shallow heuristic here would produce
silent wrong answers that are worse than requiring an explicit
dependency.

**Layered passes (principle 4)** are multiple batches, run in sequence,
each scoped to one dimension — see "How the Methodology Adapts to Task
Shape" below, "Diagnostic audit."

**Incremental validation (principle 6)** is Phase 5, called once per
batch, not once at the end of a multi-batch task — see next.

`apply-all` loops `apply-next` to completion or the first `abort`, for a
batch trusted enough not to need per-step reaction; prefer looping
`apply-next` yourself when you want the chance to respond to each result.

---

## Phase 5 — Validation

**Purpose:** confirm that execution achieved the intended state and
introduced no new problems.

**Validation levels:**

1. **Automated check.** A systematic, repeatable check for the absence of
   originally identified deviation patterns.
2. **Semantic / contextual review.** Not every surviving match is a
   genuine violation. Each one must be evaluated in its context to
   distinguish a legitimate exception from a real, unresolved issue. This
   cannot be delegated to the automated check — it produces the
   candidates for review, not the judgment itself.
3. **Final report.** A structured summary of status per unit,
   distinguishing fully clean units from units with remaining issues,
   broken down by severity. For every declared taxonomy category, the
   report records a finding or an explicit "checked, none found" — never
   silence, which is indistinguishable from never having checked. Where
   the report cites a phase of this methodology as the basis for a
   decision, it separates what that citation supplied (a process step, a
   required check) from what came from applying it to the material at
   hand (a fact about that material) — a citation that blends the two
   reads as if the methodology itself contained domain knowledge it
   doesn't.

### Concrete: llm-assembler

```
python3 scripts/cli.py validate-post <batch_id>
```

Only meaningful once every descriptor in the batch shows `applied`.
Performs two checks, both re-derived fresh from the file on disk, never
from anything the batch claims about itself:

- **Syntax validity** of every touched file — for `.py` files, an actual
  `compile()` call; other extensions report "skipped, no checker
  registered" rather than being silently assumed fine (see
  `SYNTAX_CHECKERS` in `scripts/validator.py` to add one for another
  language).
- **Every declared invariant** — `add-invariant <batch_id> --file PATH
  --pattern REGEX --expected-count N [--checked-against PATH]`, a
  completeness criterion declared *separately* from the descriptors, at
  planning time, ideally derived by actually searching the file rather
  than by trusting a count of however many descriptors happened to get
  written. `--checked-against` names the file that search actually used;
  `validate-plan` collects any invariant missing one, in a batch that
  also carries payload-bearing descriptors, into a non-blocking
  `warnings` list — visible instead of indistinguishable from a real
  check. This is what catches the single most common real failure mode: a
  rename that's internally consistent — every descriptor valid, no
  conflicts — and still misses an occurrence nobody's plan happened to
  include.

**Level 2, semantic/contextual review, is where the automated check
deliberately stops rather than trying to finish the job:** each failing
invariant's result includes up to 20 concrete `matches` — line number and
text, not just a count — specifically so the judgment of "is this
particular surviving match a real problem or a legitimate exception" has
something to work with, without the tool making that judgment itself:

```json
{
  "description": "no remaining references to the old parameter name",
  "pattern": "old_name", "expected": 0, "actual": 1, "result": "fail",
  "matches": [{"line": 2, "text": "print(old_name)"}],
  "matches_truncated": false
}
```

**Level 3, the final report**, is `status <batch_id>` (counts by
descriptor status) plus the last `validate-post` result. For a task
spanning several batches — see "Diagnostic audit" below — that's several
calls aggregated by hand; there is no cross-batch rollup command.

A failed post-condition does not automatically undo what was applied
(see Limitations). The intended recovery is a small follow-up batch that
closes the specific gap `validate-post` reported, planned and validated
the same way as any other — not an automatic rollback, which would need
either a stored pre-batch snapshot or a correct inverse for every
operation, and isn't built until there's a concrete reason to need it.

---

## Requirements for Specifying a Task Map

Before a task map can be produced, the request that defines it must
explicitly specify:

| # | Requirement | Concrete: how it's satisfied |
|---|---|---|
| 1 | **Scope** — the exhaustive set of units to be analyzed, and, for any unit whose transformation targets specific regions within it rather than the unit as a whole, the exhaustive partition of that unit's relevant region | Every file `register`ed before the batch is planned; for region-scoped work, a range map covering the region completely, built before descriptors exist (see "Content assembly / transplant" below) |
| 2 | **Reference** — the specification being analyzed against | Read directly, no dedicated mechanism (see Phase 0) |
| 3 | **Category taxonomy** — exhaustive, coded deviation types | `taxonomy.json`, via `add-category` |
| 4 | **Severity scale** — explicit criteria per tier | The closed vocabulary `critical`/`major`/`minor`/`cosmetic` |
| 5 | **Change-type vocabulary** — closed set of transformation types | The five ops: `insert_after`/`delete_range`/`replace_range`/`move_range`/`copy_range` |
| 6 | **Output structure** — exact structure and field types | The descriptor schema in Phase 2 above, and `references/file-formats.md` in full |
| 7 | **Identifier rules** — how unique ids are formed | `descriptor_id`: `d0001`, `d0002`, ... sequential per batch; `line_id`: `<file_id>_l<seq>`, permanent once assigned |
| 8 | **Dependency reference rules** — how cascades are expressed | `depends_on`: a list of `descriptor_id`s, checked to exist and checked for cycles at `validate-plan` |
| 9 | **Location / context requirements** — precision needed to find and re-verify | `line_id`, resolved through the registry to a live position — never a raw line number; optionally paired with `--context` (≤120 chars, human-readable, advisory) so a reviewer can see what's there without dereferencing `expect_hash` |
| 10 | **Explicit exclusions and protected material** | `constraints.json`, via `add-constraint`; anything simply never `register`ed is out of scope by omission |
| 11 | **Reference-clause traceability** (conformance tasks) — optionally, which specific clause of the governing standard a finding answers to, distinct from its taxonomy category | `--rule-ref`, free-text and unvalidated — Phase 0 doesn't parse or index governing material, so this can't be checked the way `depends_on` is checked |

### Conceptual Improvements Over a Naive Specification

| Gap in a naive specification | What closes it |
|---|---|
| No defined output structure | The descriptor schema, typed fields, worked examples throughout this document |
| No unique identifiers | `descriptor_id` / `line_id`, assigned by the tool, never by hand |
| No current/expected separation | `expect_hash` and `payload_ref` as two distinct fields, verifying that content hasn't drifted — plus optional `--context`, a short human-readable echo for review, since a hash alone tells code what to check but tells a person nothing to look at |
| Dependencies expressed only as text | `depends_on` referencing real `descriptor_id`s, checked to exist |
| No structural validation of the map itself | `validate-plan`'s schema check, before anything else runs |
| No bound on location precision | `line_id`, immune to the position drift a raw line number suffers |
| No severity | No way to determine execution order — closed by the `severity` field and its tie-break role in `apply_order` |
| No change type | No way to distinguish operations with different risk profiles — closed by the five-op vocabulary |
| No re-verification before acting | `expect_hash`, checked live at `apply-next`, not trusted from the plan |
| No account of interruption | `checkpoint.json` + `wal.jsonl`; `resume` |

---

## How the Methodology Adapts to Task Shape

**Conformance transformation** — bringing material into alignment with a
reference standard.
Analyze unit × category; group the execution plan by unit.
*Concrete:* one taxonomy category per deviation type from the reference;
batch by unit (file, or natural subdivision); `add-invariant` per
category, confirming the pattern defining that deviation is gone.

**Diagnostic audit** — assessing quality or risk across multiple
dimensions.
Analyze by dimension rather than by unit; group the plan by dimension;
prioritize by the combination of impact and effort, tackling high-impact
/ low-effort items first.
*Concrete:* lean on `severity` more than `category` for ordering, since
the question is "what's worth doing first," not "what kind of thing is
this"; batch by dimension rather than by file — this is Phase 4's
"layered passes" principle at the multi-batch scale.

**System transition** — moving material from one system, interface, or
approach to another.
Find all usages/references first; isolate high-risk (breaking) changes
into their own execution batch; validate after every unit rather than at
the end.
*Concrete:* `register` everything that references what's moving before
writing any descriptor; `add-constraint` anything not yet ready to
change; `sync-domino-queue` after cross-examination closes so the
coprocessor surfaces references that weren't independently flagged as
their own violation — most transitions live or die on whether every
reference to what's moving got found; isolate breaking changes into
their own batch; `validate-post` after every batch, not only at the end
of the whole transition.

**Global identifier or terminology change** — renaming or redefining
something referenced throughout a body of material.
Search exhaustively across all contexts, including secondary and
reference material, not just primary content; order execution from
structural/definitional layers toward dependent/surface layers; close
with a final exhaustive check.
*Concrete:* domino tracing *is* the discipline here, not an optional
extra — give the rename's descriptor a `domino_hint` of the exact old
name so the mechanical search has a precise string to work from, and let
the queue surface every other file that uses it. One `add-invariant
--pattern <old-name> --expected-count 0` per touched file is the
completeness check that catches whatever domino tracing still missed —
between the two, the risk this mitigates (a rename that's internally
consistent but not exhaustive, the worked example throughout this
document) is caught twice, not once.

**Content assembly / transplant** — building a new unit by combining
material drawn from two or more existing units, none of which is itself
the reference standard.
Partition every source region into a complete inventory before
extraction — not only the regions a conflict or open decision was raised
about; treat a region with no conflict as an inventory item requiring
the disposition "transfer as-is," not as an item with no disposition at
all.
*Concrete:* build the range map as its own pass (`sed -n`, `wc -l`,
whatever confirms a boundary against the live source) separate from the
pass that works out what needs a decision. Prefer an `add-invariant`
that cross-checks two independently sourced facts (a markup attribute's
count against a class definition's count) over one whose
`--expected-count` is grepped from the same payload file a descriptor
was just built from — the second kind confirms the plan agrees with
itself, not that it's complete.

---

## Full CLI Reference

Every command: `python3 scripts/cli.py <command> ...`, run from inside
the project being edited. Every command prints one JSON object; exit 0 on
success, 1 on a reported validation/apply failure, 2 on a usage error.
State lives in `.llm-assembler/` at the project root, the same convention
as `.git/`.

| Command | Purpose |
|---|---|
| `register <path> [--force]` | Phase 0: bring a file under management, assigning permanent ids. Idempotent. |
| `show-file <path>` | Read-only: every live line with its id and position. |
| `new-batch` | Open a batch — a set of descriptors checked and applied together. |
| `add-descriptor <batch_id> --op OP --file PATH [--start ID --end ID \| --after ID_or_START] [--dest ID] [--payload-file F \| --payload-text T] [--depends-on IDS] [--category CODE] [--severity LEVEL] [--provenance direct\|domino] [--domino-hint P] [--domino-of ID] [--context T] [--rule-ref T]` | Phase 1/2: record one issue as one atomic edit. |
| `add-invariant <batch_id> --file PATH --pattern REGEX --expected-count N [--description T] [--checked-against PATH]` | Declare a completeness criterion, independent of the descriptors it checks. |
| `add-category <batch_id> --code CODE [--description T]` | Phase 1.1: declare one taxonomy entry, before any descriptor uses it. |
| `add-constraint <batch_id> --file PATH --start ID --end ID [--reason T]` | Phase 0: declare a protected range. |
| `sync-domino-queue <batch_id>` | Phase 1.3: queue every direct-provenance finding not already queued. Idempotent. |
| `domino-next <batch_id>` | Phase 1.3: next untraced finding plus mechanically-computed candidates. Read-only. |
| `domino-resolve <batch_id> <finding_id>` | Phase 1.3: mark a finding traced; independently recounts linked cascades. |
| `domino-status <batch_id>` | Phase 1.3: pending/traced counts, whether the queue is `ready_for_plan`. |
| `validate-plan <batch_id>` | Phase 3: domino-completeness + schema + registry resolution + constraint check + conflict graph + safe ordering, all before anything is touched. |
| `check <batch_id> <descriptor_id>` | Read-only: would this descriptor currently apply cleanly? |
| `apply-next <batch_id>` | Phase 4: apply exactly one descriptor, returning `applied`/`skipped`/`recovered`/`abort`. |
| `apply-all <batch_id>` | Loop `apply-next` to completion or the first abort. |
| `validate-post <batch_id>` | Phase 5: syntax check + invariant re-check, both fresh from disk. |
| `status <batch_id>` | Batch status, descriptor counts by status and by provenance, current `apply_order`. |
| `checkpoint` | Print `checkpoint.json` as-is. |
| `resume` | The first command to run in a fresh session — real batch status plus a concrete next step, including the last abort's diagnostic if that's how things stopped. |

**Rules of the road**, unchanged by anything above: let the engine
compute hashes and touch files — never hand-edit a file the engine has an
open batch for, or write into `expect_hash` yourself, or the registry and
the file go out of sync and the next check either fails a fine edit or
passes one it shouldn't. Don't hand-edit anything under
`.llm-assembler/` — `wal.jsonl` is written only by the engine,
`validation_log.jsonl` only by the validator, specifically so neither can
forge the other's verdict (a guarantee that's only as real as the write
permissions actually enforced around it, worth noting plainly rather than
overselling). A validated plan is a snapshot, not a promise — between
validating and applying, nothing stops the world from changing; that's
what the per-operation check on every `apply-next` call is for. Small
batches are easier to recover from than large ones. A finding with zero
mechanical candidates isn't automatically a finding with zero cascades —
`domino-next`'s search only surfaces shared text; resolving a finding
records that it was looked at, not that nothing was there.

---

## Full File Format Reference

```
.llm-assembler/
    registry.json            line_id -> current position, one entry per file
    wal.jsonl                 append-only: what started, what finished
    validation_log.jsonl       append-only: validator verdicts, all phases
    checkpoint.json             overwritten each interrupt; resume starts here
    payloads/<hash>.blob         content-addressed text, git-object style
    batches/<batch_id>/
        descriptors.json           the batch's edit queue
        invariants.json              completeness criteria
        taxonomy.json                  declared category codes
        constraints.json                 protected ranges
        domino_queue.json                  cascade-tracing progress, Phase 1.3
```

**registry.json** — one entry per file, global to the project, not
per-batch (a per-batch registry would let two batches disagree about
where the same line currently is, reproducing the exact drift problem the
registry exists to solve). `lines` maps `line_id -> position`, 1-based;
`null` means deleted — the id survives as a tombstone so a stale
reference fails with a clear error instead of silently resolving to
whatever now occupies that old position.

```json
{"files": {"f_98a15f28da": {"path": "sample.py", "next_seq": 18,
  "lines": {"f_98a15f28da_l00001": 1, "f_98a15f28da_l00003": null}}}}
```

**batches/\<id\>/descriptors.json** — the full schema is in Phase 2
above. `status` on the batch: `planning` → `validated` (by
`validate-plan`) → `committed`/`failed` (by `validate-post`).
`apply_order` is written by `validate-plan`, never by hand.

**batches/\<id\>/invariants.json**:

```json
{"batch_id": "batch_0001", "invariants": [
  {"type": "occurrence_count", "file_id": "f_98a15f28da",
   "pattern": "person_name", "expected_count": 0,
   "description": "no remaining references to the old parameter name",
   "checked_against": "src/handlers.py"}
]}
```

Deliberately a separate file from `descriptors.json`, not a field inside
it: if the plan and its own completeness criterion were written by one
call into one file, a systematic gap in the plan would be equally likely
to be missing from the criterion, and the check would pass while being
substantively wrong. Being a separate file narrows that risk; it doesn't
close it, since nothing stops the file from being written by re-counting
the same descriptors anyway. `checked_against` names what the count was
actually verified against, and a batch that skips it while carrying real
payload content gets flagged, non-blocking, at `validate-plan` — see
Phase 5's "Concrete" section above. Same reasoning for `taxonomy.json`
and `constraints.json` below being their own files rather than fields.

**batches/\<id\>/taxonomy.json**:

```json
{"batch_id": "batch_0001", "categories": [
  {"code": "NAMING", "description": "identifier does not follow the naming convention"}
]}
```

**batches/\<id\>/constraints.json**:

```json
{"batch_id": "batch_0001", "protected_ranges": [
  {"file_id": "f_98a15f28da", "start": "f_98a15f28da_l00040",
   "end": "f_98a15f28da_l00062", "reason": "vendored code, do not modify"}
]}
```

**batches/\<id\>/domino_queue.json** — one entry per direct-provenance
descriptor, populated by `sync-domino-queue`:

```json
{"batch_id": "batch_0001", "entries": [
  {"finding_id": "dm0001", "descriptor_id": "d0001", "status": "pending", "linked_descriptors": 0}
]}
```

`linked_descriptors` is written only by `domino-resolve`, and only as a
count it derives itself by scanning for descriptors whose `domino_of`
names this entry — never a number taken on trust. `validate-plan` reads
this file before anything else it checks: any entry still `pending`
fails the call immediately. A batch that never calls `sync-domino-queue`
has no domino queue at all, and `validate-plan` behaves exactly as if
this file didn't exist.

**wal.jsonl** (append-only):

```json
{"ts": 1786003123.4, "event": "op_start", "batch_id": "batch_0001", "descriptor_id": "d0001", "op": "replace_range"}
{"ts": 1786003123.5, "event": "op_applied", "batch_id": "batch_0001", "descriptor_id": "d0001"}
{"ts": 1786003140.0, "event": "domino_start", "batch_id": "batch_0001", "finding_id": "dm0001"}
{"ts": 1786003141.2, "event": "domino_traced", "batch_id": "batch_0001", "finding_id": "dm0001", "linked_descriptors": 2}
```

**validation_log.jsonl** (append-only, written only by the validator —
see "Rules of the road" above for why this and the WAL stay separate
files with separate writers):

```json
{"ts": 1786003100.1, "phase": "plan", "batch_id": "batch_0001", "result": "pass", "apply_order": ["d0001"]}
{"ts": 1786003123.6, "phase": "post", "batch_id": "batch_0001", "result": "pass", "syntax": {}, "invariants": []}
```

**checkpoint.json** — overwritten in full on every phase transition and
every applied descriptor, never appended:

```json
{"updated_at": 1786003123.6, "active_batch": "batch_0001",
 "queue_position": 3, "total_descriptors": 4,
 "registry_snapshot_hash": "9f2a3c1e04bb", "last_interrupt_cause": "post_op"}
```

**payloads/\<hash\>.blob** — plain text, named by the sha256 of its own
content: the same text stored twice costs nothing extra, and two
descriptors with identical payload text share a blob automatically.

---

## Checklist Upon Receiving a Task

- [ ] Has the entire reference specification been loaded and read — not only its beginning?
- [ ] Have all materials referenced by the task been `register`ed?
- [ ] Has an exhaustive taxonomy of deviation types been compiled — `add-category`, before any descriptor needs one?
- [ ] For every identified issue, has its cascade been traced as its own resumable pass — `sync-domino-queue` / `domino-next` / `domino-resolve`, checked complete by `domino-status` — rather than a single attempt with no record of what's covered?
- [ ] Does the map contain precise, unambiguous location references — `line_id`, never a raw line number?
- [ ] Do all dependency references correspond to descriptors that actually exist — checked automatically by `validate-plan`?
- [ ] Is execution order determined by severity where the batch has more than a few, unequally urgent items?
- [ ] Does each unit have a defined plan of sequential passes — separate batches for separate dimensions?
- [ ] Is validation planned incrementally, `validate-post` after each batch, rather than only at the very end?
- [ ] Is it clear, for every category, what constitutes a legitimate exception versus a genuine violation — reviewed against the concrete `matches` `validate-post` returns, not just a pass/fail count?
- [ ] If this task is interrupted partway through, does `resume` pick it back up without repeating completed work?
- [ ] Before a planned change is applied, is the material re-checked against what the plan expected — automatic, via `expect_hash`, on every `apply-next`?
- [ ] Does execution distinguish `applied`/`recovered` from `abort`, rather than treating anything unexpected the same way?

---

## Anti-Patterns

**Simultaneous analysis and correction** — identifying and immediately
fixing issues one at a time, without ever holding the complete picture,
destroys the ability to prioritize or judge completeness.
→ *Prevented by:* there is no command that both analyzes and applies —
`add-descriptor` only records; `apply-next` only acts on an already-
`validate-plan`'d batch. The two are structurally different calls.

**Interleaved cross-examination and cascade-tracing** — tracing a
finding's cascade before cross-examination has finished looking at
everything else makes deduplication against not-yet-discovered findings
unreliable and progress through either pass unmeasurable.
→ *Prevented by:* `sync-domino-queue` only ever queues findings that
already exist as descriptors — there's no way to trace a cascade for
something that hasn't been recorded yet, which structurally forces 1.2's
output to exist first.

**Descriptive rather than referential dependencies** — recording cascade
relationships as free-text description cannot be verified.
→ *Prevented by:* `depends_on` holds `descriptor_id`s, and
`validate-plan` fails the batch outright if one doesn't resolve. Domino
links are the same shape — `domino_of` names a real `descriptor_id`,
checked at `add-descriptor` time, and the resulting cascade count is
recomputed from these references, never taken as a claim.

**Incorrect operation ordering** — applying a general change before a
more specific, overlapping one makes the specific case unreachable.
→ *Not fully prevented* — this one is explicitly not mechanized (see
Phase 4); the conflict graph enforces ordering where ranges overlap and
none is declared, but "specificity" itself isn't inferred. Discipline,
not the tool, is what closes this one.

**End-only validation** — deferring all verification until every unit is
processed lets an error introduced early surface only much later.
→ *Prevented by:* `validate-post` is meant to run per batch, not once
across an entire multi-batch task; nothing rewards batching everything
into one giant unit before checking anything.

**Ignoring legitimate context during validation** — treating every
surviving match as a violation, without contextual review, produces false
alarms.
→ *Supported, not automated:* `validate-post` returns concrete matches
with line and text, specifically so this review has something to work
with — the review itself stays a human/model judgment, on purpose.

**Location-less mapping** — recording an issue's location only
approximately makes it impossible to reliably find, re-verify, or confirm
resolved.
→ *Prevented by:* every location is a `line_id`, resolved through the
registry to a real, current position — there is no "approximately here"
representation available at all.

**Trusting the map without re-checking reality** — acting on a planned
item purely because it's in the map, without confirming the material
still matches, lets a correct analysis produce an incorrect result.
→ *Prevented by:* `expect_hash`, checked live before every `apply-next`,
not read from the plan and trusted.

**Binary success/failure on execution** — treating "already done" the
same as "cannot proceed" either causes needless rework or halts progress
that didn't need to halt.
→ *Prevented by:* the four-way `applied`/`skipped`/`recovered`/`abort`
result, not a boolean.

**No resumption path** — restarting from scratch after an interruption,
or guessing how far things got from memory rather than from a record.
→ *Prevented by:* `checkpoint.json` + `wal.jsonl` + `resume`.

**Conflict-filtered inventory** — building the transfer inventory from
the list of items that surfaced as needing a decision during analysis,
rather than from an exhaustive partition of the material itself; content
with no conflict generates no entry and is silently dropped precisely
because it was well-behaved.
→ *Prevented by:* partitioning a source region into a complete range map
before any descriptor exists — every line "transfer as-is," "transfer
with a decision," or "excluded, stated why" — with the open-decisions
list applied as a filter over that map afterward, never mistaken for the
map itself. See `SKILL.md`, step 4, and "Content assembly / transplant"
under "How the Methodology Adapts to Task Shape."

**Unprompted substitution** — replacing material that won't resolve here
(a broken path, a missing dependency) with a working alternative nobody
asked for, so something renders or runs. The mirror image of
conflict-filtered inventory: that one drops what nobody asked dropped,
this one replaces what nobody asked replaced.
→ *Prevented by:* no mechanism forces the correct answer here, only
discipline — carry an unresolvable reference forward exactly as written
and say so, rather than silently swapping in something that works. See
"Rules of the road" in `SKILL.md`.

---

## Working with Large Bodies of Material

- Read the entire unit before beginning transformation — `show-file`
  before `add-descriptor`, not instead of it.
- Apply matching changes in batches, grouped by pattern or category,
  rather than one at a time — one `batch` per logically-related set of
  edits.
- Split work into logical passes aligned with the natural dimensions of
  the material, not arbitrary chunks — separate batches per dimension,
  not one batch chunked by line count.
- Confirm the result of each pass before proceeding to the next —
  `validate-post` before opening the next batch.

---

## Quality Assessment

**Completion questions:**
1. Does the number of issues recorded equal the number marked resolved? — `status <batch_id>`'s counts.
2. Does a systematic recheck return none remaining, excluding legitimate exceptions? — `validate-post`'s invariant results, reviewed against their `matches`.
3. Do all elements conform to the reference's structural rules? — the syntax check half of `validate-post`, where a checker is registered.
4. Have all violations of fundamental/architectural invariants been eliminated? — filter descriptor results by `severity: critical`.
5. Has underlying meaning or behavior remained unchanged where only structural or naming changes were intended? — not mechanically checkable in general; the closest available proxy is the syntax check plus manual review of a representative sample.

**Numerical indicators to record before and after:** total units, total
volume of material, issue count by severity, units with zero remaining
issues. No dedicated command aggregates these across a multi-batch task
today — see Limitations.

---

## Limitations

Stated plainly rather than discovered the hard way.

- **Single active batch at a time.** `checkpoint.json` tracks one active
  batch; two batches touching the same file concurrently isn't detected.
- **No automatic rollback on a failed post-condition.** Already-applied
  descriptors stay applied; recovery is a follow-up batch, not an undo.
- **`delete_range`/`move_range` have a narrower crash-recovery window**
  than the three ops that add positively-checkable content — see
  `references/limitations.md` for the exact boundary; it fails safe
  (`abort`) rather than silently guessing wrong.
- **No automatic detection that descriptor B targets content descriptor A
  is about to create** within the same batch — declare it with
  `--depends-on`.
- **`move_range`/`copy_range` don't cross files** — a cross-file move is
  two descriptors in two batches (or one batch, correctly ordered).
- **Syntax checking ships with Python only** — extend `SYNTAX_CHECKERS`
  for other languages.
- **One invariant type** — `occurrence_count`. Extend
  `validator.validate_post`'s invariant loop for a different kind of
  completeness check.
- **Domino tracing finds candidates, not verdicts, and only where there's
  shared text** (see Phase 1.3) — a cascade with no shared wording (a
  business rule reimplemented independently, a value that has to change
  in step but is spelled differently) won't surface on its own. The
  mechanical layer narrows what needs a look; it doesn't replace looking,
  and pretending it does would give false confidence the search was
  exhaustive when it wasn't. One recurring shape of this worth naming:
  material with its own embedded logic, where one part silently assumes
  another still exists in a specific place — this produces no text match
  at all, and is caught only by reading the dependent logic directly (see
  Phase 1.3's "Concrete" section above).
- **Domino tracing doesn't recurse** — a `--provenance domino` descriptor
  is never itself queued for its own trace. Cascades of cascades are a
  deliberate scope boundary for this version.
- **"Specific before general" is not mechanized** (see Phase 4) — and for
  line_id addressing, mostly doesn't need to be. The classic risk here is
  a naive streaming text replace: the general pattern replaced first, in
  one pass over mutable raw text, can make a more specific string that
  was a substring of it physically stop existing before a second pass
  ever reaches it. That risk depends on "find pattern X across the whole
  file, replace every occurrence" being one operation over text that's
  changing underneath it — which this system never does. Two descriptors
  whose ranges don't overlap can't touch each other's content regardless
  of order, so order is provably irrelevant, by construction. Two whose
  ranges do overlap are already a conflict the graph catches on its own,
  already requiring an explicit `--depends-on`, with no new mechanism
  needed. The one place a residual version of this risk survives:
  composing a single descriptor's own `payload_text` with a naive
  sequential substitution inside it, rather than assembling the correct
  final result directly — not an ordering question, and not something
  `--depends-on` could address; a general "compose the text correctly"
  concern true of writing any text.
- **Categories, constraints, and the domino queue are per-batch, not
  project-wide** — a declaration or a traced finding in one batch says
  nothing to a later one touching the same material.
- **No cross-batch rollup** for a task spanning several batches — Quality
  Assessment's numerical indicators are aggregated by hand today.
- **CRLF line endings come back as LF** — files are read with
  `splitlines()` and rejoined with `\n`.
- **`context` and `rule_ref` are advisory and unvalidated** — neither is
  ever checked against anything; `context` can drift from the real
  content the moment something else changes that line, and `rule_ref`
  can cite a clause that's wrong, renumbered, or doesn't exist, with
  nothing here able to tell. Both are notes left for a human, not a
  second gate alongside `expect_hash` and `depends_on`.

---

## Closing note on layering

Nothing in this document is here because "the methodology says so" in
some free-floating sense — every abstract requirement above is paired
with the concrete mechanism satisfying it, and every concrete mechanism
exists because of a specific, statable failure mode it closes (drift,
unreliable long-sequence bookkeeping, a plan trusting itself, a session
that doesn't survive interruption, the person checking the work sharing
blind spots with the person who did it). Where the abstract requirement
and the concrete answer are kept in two separate, leaner documents
instead of merged here, that's so each can be read and trusted on its
own — the methodology by someone applying it to a domain this
implementation never touches, the implementation by someone who never
needed the methodology stated separately at all. This document exists as
a third option for whoever wants both without switching files, kept
accurate to the same tested code both other documents describe.
