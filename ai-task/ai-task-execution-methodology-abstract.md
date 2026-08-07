# AI Task Execution Methodology — Abstract
## Architectural Logic and Phase Structure (Implementation-Agnostic)

---

## Purpose of This Document

This document isolates the **architecture** of the methodology — the phases, their purpose, the outputs each phase must produce, and the rules governing how phases relate to one another. It deliberately excludes technical implementation (data formats, search or matching techniques, syntax, tooling, domain-specific examples), so the same architecture can be reapplied to any domain by attaching a separate, domain-specific implementation layer to each phase.

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

---

## Phase 4 — Execution

**Purpose:** apply planned changes in a controlled, risk-minimizing sequence.

**Governing principles:**

1. **Single-unit focus.** Work is completed fully on one unit before moving to the next. Units are never interleaved mid-way.
2. **Immediate dependency resolution.** When an issue carries dependency items, all of them are resolved in the same pass as the parent issue — never deferred to "later."
3. **Layered passes.** Complex units are processed through multiple sequential passes, each addressing one logical dimension of the unit rather than attempting all dimensions simultaneously. Simultaneous multi-dimensional changes risk internal conflict; isolating passes by dimension contains that risk.
4. **Specific-before-general ordering.** Where multiple changes could overlap, the most specific change is applied before the most general one, so a general change cannot silently absorb or invalidate a more specific case that hasn't been applied yet.
5. **Incremental validation.** Each unit is validated immediately after its changes are applied — before moving to the next unit. Validation is never deferred to the end of all execution.

---

## Phase 5 — Validation

**Purpose:** confirm that execution achieved the intended state and introduced no new problems.

**Validation levels:**

1. **Automated check.** A systematic, repeatable check for the absence of originally identified deviation patterns.
2. **Semantic / contextual review.** Not every surviving match is a genuine violation. Each one must be evaluated in its context to distinguish a legitimate exception from a real, unresolved issue.
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
10. **Explicit exclusions** — what is deliberately out of scope for the map.

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

*This document defines architecture only. Search techniques, data formats, output schemas, matching/replacement logic, and other domain-specific mechanics belong in a separate implementation layer attached to each phase.*
