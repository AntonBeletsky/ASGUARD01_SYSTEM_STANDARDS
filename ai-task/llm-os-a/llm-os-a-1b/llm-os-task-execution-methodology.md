# LLM-OS Task Execution Methodology — Abstract
## Architectural Logic and Phase Structure (Implementation-Agnostic)

---

## Purpose of This Document

This document isolates the **architecture** of the methodology — the phases, their purpose, the outputs each phase must produce, and the rules governing how phases relate to one another. It deliberately excludes technical implementation (data formats, search or matching techniques, syntax, tooling, domain-specific examples), so the same architecture can be reapplied to any domain by attaching a separate, domain-specific implementation layer to each phase.

This revision folds in four architectural lessons learned from building one such implementation layer (for line-precise text editing). None of the four are domain-specific — they're gaps the first version of this document left open regardless of domain — so they're stated here as general requirements, not as anything specific to text or code. Where an implementation layer exists, its own document maps each phase onto concrete mechanics; this document stays free of that mapping on purpose.

---

## Core Philosophy

Any non-trivial task decomposes into three stages that must never be merged:

```
ANALYSIS → PLAN → EXECUTION
```

Merging these stages is the primary source of error: acting before the full scope of work is understood leads to omissions, cascading failures, and rework.

These three stages expand into six operational phases:

| Stage | Phase(s) |
|---|---|
| Preparation | Phase 0 — Context Loading |
| Analysis | Phase 1 — Analysis |
| Plan | Phase 2 — Task Map · Phase 3 — Execution Plan |
| Execution | Phase 4 — Execution |
| Verification | Phase 5 — Validation |

### Interruption is not a special case

Any phase can be interrupted before it completes — Phase 0 mid-load, Phase 1 partway through the unit × category sweep, Phase 4 mid-batch. A methodology that only accounts for a clean, uninterrupted run through all six phases is describing the easy case and leaving the common one undefined.

Two properties make interruption survivable rather than catastrophic:

- **Every phase's output is a durable artifact, not a mental state.** A phase isn't "in progress" in some ambient sense — its progress is exactly what's recorded in its output so far (partial taxonomy, partial task map, partially-applied plan). Nothing that matters lives only in the reasoning that produced it.
- **Resuming means reading that artifact, not restarting the phase.** The correct response to an interruption is to determine, from the artifact itself, exactly how far the phase got and continue from there — never to re-run a phase from its beginning "to be safe," and never to guess how far it got from memory of having done it.

A methodology satisfies this property when every phase's required output (taxonomy, task map, plan, applied-state) is specified precisely enough that "how far did this get" is a fact you can read, not a judgment you have to reconstruct.

---

## Phase 0 — Context Loading

**Purpose:** establish complete, confirmed situational awareness before any analytical or productive work begins.

**Required tasks:**
- Load the governing reference against which correctness will be judged.
- Load all materials that are the subject of the work.
- Establish constraints: what must not be touched, what is critical, what takes priority.
- Explicitly confirm that loading is complete before proceeding.

**Governing rule:** no transformation or corrective work happens in this phase — only intake and confirmation.

**Rationale:** context that is incomplete or misunderstood invalidates every downstream conclusion. Errors introduced here propagate through every later phase.

**On constraints specifically:** establishing a constraint in this phase is not the same as enforcing it later. A constraint that is only ever written down and never mechanically checked against the plan before execution is a note, not a guardrail. Phase 3 is where that check belongs — see below.

---

## Phase 1 — Analysis

**Purpose:** systematically examine all loaded material against the reference, identifying every deviation — without acting on any of them yet.

### 1.1 Category Taxonomy
Establish an exhaustive, named classification of possible deviation types **before** examining individual material.
**Rationale:** a category that is never defined can never be searched for; an analysis without a taxonomy is structurally incomplete.

### 1.2 Systematic Cross-Examination
Examine each unit of material against each defined category, in a fixed, sequential order — unit × category — without skipping ahead.
Use structured, layered questioning to surface deviations methodically rather than opportunistically.

### 1.3 Dependency Analysis ("Domino")
For every identified deviation, determine everything else that would break or become inconsistent if only that single point were corrected in isolation.
**Rule:** this cascade analysis must be exhaustive. An incomplete cascade produces a broken or inconsistent result once execution begins.

**Discovery is not the same activity as ordering, and only one of them can be delegated.** Once a dependency has been found, respecting it — never scheduling the dependent item before the thing it depends on, refusing to proceed if dependencies form a cycle — is a mechanical, verifiable operation: given a complete list of dependency edges, there is a correct order (or a correct refusal), and checking either is not a matter of judgment. *Finding* the dependency in the first place is not mechanical in the same way — it requires understanding what the material means, not just what it says, and no amount of correctness in the ordering step compensates for a dependency that Phase 1.3 never found. Treat these as two different reliability problems: exhaustiveness of discovery is a property of how thoroughly Phase 1.3 was carried out; correctness of ordering is a property that can be checked independently of how the dependencies were found at all.

---

## Phase 2 — Task Map

**Purpose:** convert the analysis into a structured, verifiable artifact — not a narrative list — that captures every issue and its relationships.

### Conceptually Required Attributes
Each recorded issue must carry:

| Attribute | Function |
|---|---|
| Unique identifier | Enables reference from elsewhere, especially from dependencies |
| Category | Ties the issue to the taxonomy defined in Phase 1.1 |
| Severity | Determines execution priority |
| Change type | Distinguishes the nature of the required transformation |
| Location reference | Precise and unambiguous enough to find and re-verify without re-deriving it |
| Current state / expected state | Recorded as two distinct values, never blended into one description |
| Dependencies | Expressed as verifiable references to other issue identifiers, not free text |
| Status | Tracks progress through the workflow |

### Severity
A tiered scale that separates:
- Violations of fundamental / architectural invariants (highest priority)
- Violations of standards carrying broad structural or scaling risk
- Deviations that are "noise" — they don't affect function but degrade quality
- Purely cosmetic deviation (lowest priority)

**Function:** severity is what makes execution order determinable.

### Change Type
A fixed, closed vocabulary describing the nature of each transformation — categories such as *creation*, *removal*, *substitution*, *addition*, *relocation*. Distinguishing these matters because different change types carry different risk and dependency profiles.

### The map is a snapshot, not a promise

A task map records the state of the material as understood when Phase 1 examined it. Nothing about recording an issue in the map guarantees the material is still in that state by the time Phase 4 gets to it — time passes, and in any process involving more than one actor or more than one pass, the underlying material can change between when an issue was found and when it's acted on. The map is not re-validated by the mere fact of having been written down. What that requires is stated explicitly in Phase 4.

---

## Phase 3 — Execution Plan

**Purpose:** convert the task map into an actionable, trackable, hierarchically organized plan.

### Structure
- Top-level grouping: one natural unit of work per group.
- Subgrouping: one category/type of issue per subgroup.
- Leaf items: individual issues, each carrying a trackable status.
- Dependency items execute together with their parent issue — never as independent, separately scheduled items.

### Execution Priority
1. Primary ordering: by severity, most fundamental first.
2. Secondary ordering within a severity tier: by number of dependencies — items with more cascading effects are executed sooner, since they affect more of the system.

### Plan Validation

Before any item in the plan is acted on, the plan as a whole must be checked — not each item as it comes up, but the complete plan, once:

- every dependency reference resolves to an issue that actually exists in the map;
- no dependency ordering is contradictory (a cycle where two or more items require each other first);
- no planned change targets a constraint established in Phase 0 as off-limits.

This check belongs here, before Phase 4, for a specific reason: it is the last point at which finding a problem costs nothing, because nothing has been changed yet. The same check performed mid-execution instead finds the same problem after some of the plan has already been acted on, which is strictly more expensive to recover from.

---

## Phase 4 — Execution

**Purpose:** apply planned changes in a controlled, risk-minimizing sequence.

**Governing principles:**

1. **Reality is checked before it is changed.** Immediately before acting on a planned item, confirm the material still matches what Phase 1 recorded for it — not what the plan assumes, what is actually there right now. The task map is a snapshot (see Phase 2); this is the point where that snapshot either gets confirmed or is caught being stale. Skipping this and trusting the plan directly is how a correct analysis produces an incorrect result when acted on late enough for something to have changed underneath it.
2. **Single-unit focus.** Work is completed fully on one unit before moving to the next. Units are never interleaved mid-way.
3. **Immediate dependency resolution.** When an issue carries dependency items, all of them are resolved in the same pass as the parent issue — never deferred to "later."
4. **Layered passes.** Complex units are processed through multiple sequential passes, each addressing one logical dimension of the unit rather than attempting all dimensions simultaneously. Simultaneous multi-dimensional changes risk internal conflict; isolating passes by dimension contains that risk.
5. **Specific-before-general ordering.** Where multiple changes could overlap, the most specific change is applied before the most general one, so a general change cannot silently absorb or invalidate a more specific case that hasn't been applied yet.
6. **Incremental validation.** Each unit is validated immediately after its changes are applied — before moving to the next unit. Validation is never deferred to the end of all execution.

### Three outcomes, not two

The result of attempting to act on a planned item is not simply success or failure. Collapsing it to a binary loses a distinction that matters for how to respond:

- **Confirmed.** Reality matched the plan; the change was applied.
- **Already satisfied.** Reality no longer matches the plan's *starting* state, but it matches what the plan's *ending* state would have been — the change, or its effect, is already present. This is not a failure and does not need redoing; it needs the plan's own record updated to reflect that this item is done, so nothing downstream mistakes it for outstanding work.
- **Unresolvable.** Reality matches neither the plan's starting state nor its ending state. Something changed that the plan did not anticipate. This is the only one of the three that should stop forward progress on the item — and it should stop cleanly, leaving the material exactly as found, rather than guessing.

Treating "already satisfied" the same as "confirmed" risks reapplying a change that shouldn't be reapplied. Treating it the same as "unresolvable" halts progress that didn't need to halt. Both misclassifications are avoidable once the distinction is made explicit.

---

## Phase 5 — Validation

**Purpose:** confirm that execution achieved the intended state and introduced no new problems.

**Validation levels:**

1. **Automated check.** A systematic, repeatable check for the absence of originally identified deviation patterns.
2. **Semantic / contextual review.** Not every surviving match is a genuine violation. Each one must be evaluated in its context to distinguish a legitimate exception from a real, unresolved issue. This step cannot be delegated to the automated check above — it produces the candidates for review, not the judgment itself. What the automated check owes this step is enough context per candidate (not just a count) that the judgment can actually be made without re-deriving where each candidate even is.
3. **Final report.** A structured summary of status per unit, distinguishing fully clean units from units with remaining issues, broken down by severity.

---

## Requirements for Specifying a Task Map

Before a task map can be produced, the request that defines it must explicitly specify:

1. **Scope** — the exhaustive set of units to be analyzed.
2. **Reference** — the specification/standard being analyzed against.
3. **Category taxonomy** — an exhaustive, coded list of deviation types.
4. **Severity scale** — explicit criteria for what qualifies at each tier.
5. **Change-type vocabulary** — the closed set of transformation types.
6. **Output structure** — the exact structure and field types of the resulting artifact.
7. **Identifier rules** — how unique issue identifiers are formed.
8. **Dependency reference rules** — how cascade relationships are expressed and what they must contain.
9. **Location / context requirements** — the precision required to make an item findable and independently verifiable.
10. **Explicit exclusions and protected material** — what is deliberately out of scope for the map, and what is in scope but must not itself be modified (the Phase 0 constraints, restated here so the map's own specification doesn't silently drop them).

### Conceptual Improvements Over a Naive Specification

| Gap in a naive specification | What closes it |
|---|---|
| No defined output structure | An explicit structure with typed fields and a worked example |
| No unique identifiers | A defined identifier format and numbering rule |
| No current/expected separation | Two distinct fields instead of one blended description |
| Dependencies expressed only as text | Reference-based dependencies pointing to verifiable identifiers |
| No structural validation of the map itself | A requirement that every referenced dependency identifier actually exists in the map |
| No bound on location precision | An explicit requirement for exact, boundable location context |
| No severity | No way to determine execution order |
| No change type | No way to distinguish operations with different risk profiles |
| No re-verification before acting | Execution checks the material against the map's recorded state before changing anything, rather than trusting the map to still be accurate |
| No account of interruption | Every phase's output is a durable, resumable artifact rather than a mental state |

---

## How the Methodology Adapts to Task Shape

The phase architecture is constant, but its emphasis shifts with the nature of the task:

**Conformance transformation** — bringing material into alignment with a reference standard.
Analyze unit × category; group the execution plan by unit.

**Diagnostic audit** — assessing quality or risk across multiple dimensions.
Analyze by dimension rather than by unit; group the plan by dimension; prioritize by the combination of impact and effort, tackling high-impact / low-effort items first.

**System transition** — moving material from one system, interface, or approach to another.
Find all usages/references first; isolate high-risk (breaking) changes into their own execution batch; validate after every unit rather than at the end.

**Global identifier or terminology change** — renaming or redefining something referenced throughout a body of material.
Search exhaustively across all contexts, including secondary and reference material, not just primary content; order execution from structural/definitional layers toward dependent/surface layers; close with a final exhaustive check.

---

## Checklist Upon Receiving a Task

- [ ] Has the entire reference specification been loaded and read — not only its beginning?
- [ ] Have all materials referenced by the task been loaded?
- [ ] Has an exhaustive taxonomy of deviation types been compiled?
- [ ] For every identified issue, have all dependency effects been traced?
- [ ] Does the map contain precise, unambiguous location references rather than approximate ones?
- [ ] Do all dependency references in the map correspond to entries that actually exist?
- [ ] Is execution order determined by severity?
- [ ] Does each unit have a defined plan of sequential passes?
- [ ] Is validation planned incrementally, after each unit, rather than only at the end?
- [ ] Is it clear, for every category, what constitutes a legitimate exception versus a genuine violation?
- [ ] If this task is interrupted partway through any phase, can it resume from what's recorded rather than restarting that phase?
- [ ] Before a planned change is applied, is the material re-checked against what the plan expected, rather than assumed unchanged since Phase 1?
- [ ] Does execution distinguish "already done" from "not yet done" from "cannot proceed," rather than treating anything unexpected as the same kind of failure?

---

## Anti-Patterns

**Simultaneous analysis and correction**
Identifying and immediately fixing issues one at a time, without ever holding the complete picture, destroys the ability to prioritize or judge completeness.
→ Correct approach: complete analysis, then a complete map, then execution against that map.

**Descriptive rather than referential dependencies**
Recording cascade relationships as free-text description cannot be verified.
→ Correct approach: dependencies reference other issues' unique identifiers, enabling automated verification.

**Incorrect operation ordering**
Applying a general change before a more specific, overlapping change makes the specific case unreachable.
→ Correct approach: apply the most specific changes first, the most general last.

**End-only validation**
Deferring all verification until every unit is processed allows an error introduced early to surface only much later, once it is harder to trace back.
→ Correct approach: validate immediately after each unit.

**Ignoring legitimate context during validation**
Treating every surviving match as a violation, without contextual review, produces false alarms.
→ Correct approach: verify whether a remaining match is a legitimate exception before treating it as unresolved.

**Location-less mapping**
Recording an issue's location only in general or approximate terms makes it impossible to reliably find, re-verify, or confirm as resolved.
→ Correct approach: record precise, specific location references.

**Trusting the map without re-checking reality**
Acting on a planned item purely because it's in the map, without confirming the material still looks the way Phase 1 recorded it, lets a correct analysis produce an incorrect result whenever something changed in between.
→ Correct approach: re-verify the material immediately before acting on it, every time, not just the first time.

**Binary success/failure on execution**
Treating "the material already reflects this change" the same as "this change could not be applied" either causes rework that wasn't needed or halts progress that didn't need to halt.
→ Correct approach: distinguish confirmed, already-satisfied, and unresolvable outcomes, and respond to each differently.

**No resumption path**
Restarting a phase from the beginning after an interruption — or worse, guessing how far it got from memory rather than from its recorded output — wastes completed work and risks silently redoing something already done correctly.
→ Correct approach: make every phase's output durable enough that resuming is a matter of reading it, not reconstructing it.

---

## Working with Large Bodies of Material

- Read the entire unit before beginning transformation; do not proceed sequentially from the start without first understanding the whole.
- Apply matching changes in batches, grouped by pattern or category, rather than one at a time.
- Split work into logical passes aligned with the natural dimensions of the material, not arbitrary chunks.
- Confirm the result of each pass before proceeding to the next.

---

## Quality Assessment

**Completion questions:**
1. Does the number of issues recorded in the map equal the number marked resolved?
2. Does a systematic recheck for all originally identified deviation patterns return none remaining, excluding legitimate exceptions?
3. Do all elements conform to the structural rules defined by the reference specification?
4. Have all violations of fundamental / architectural invariants been eliminated?
5. Has the underlying meaning or behavior of the material remained unchanged wherever only structural or naming changes were intended?

**Numerical indicators to record before and after:**
- Total number of units
- Total volume of material
- Number of issues by severity
- Number of units with zero remaining issues

**Function:** these indicators turn "the work is done" into an objective, quantifiable claim rather than a subjective impression.

---

*This document defines architecture only. Search techniques, data formats, output schemas, matching/replacement logic, resumption mechanics, and other domain-specific mechanics belong in a separate implementation layer attached to each phase. Where such a layer exists, its own document should map back onto the phases named here — this document should not need to change to accommodate what that mapping says.*
