# Operative Skill Synthesis Protocol (OSSP)
> A context-efficiency framework for LLM skill orchestration

---

## Problem Statement

An LLM operating with a static set of loaded `.md` skills faces a fundamental
**context pollution problem**:

```
Total skill content loaded  ≠  Total skill content needed
```

Each skill file may contain sections irrelevant to the current task. These sections
consume context window tokens with **0% utility** — they crowd out working memory,
degrade reasoning quality, and waste compute on every forward pass.

**Core inefficiency pattern:**
```
[skill-A.md]  80% irrelevant  │  20% needed
[skill-B.md]  60% irrelevant  │  40% needed
[skill-C.md]  95% irrelevant  │   5% needed
─────────────────────────────────────────────
Context load: 100%   │   Useful signal: ~22%
Context waste: ~78%  ← THE PROBLEM
```

**Solution:** Before execution, synthesize a single `one-temp-skill.md` containing
only the sections relevant to the task, then discard all source skills.

---

## Protocol Overview

```
PHASE 0 → PHASE 1 → PHASE 2 → PHASE 3 → PHASE 4
 Intake    Audit    Extract   Synthesize  Execute
```

---

## PHASE 0 — Task Intake & Decomposition

**Trigger:** A task arrives. Source files may or may not be present.

**Actions:**

1. **Parse the task** — identify the primary goal, deliverable type, constraints.
2. **Detect task dimensions** — list the distinct operations the task requires.
   Each dimension is a potential hook into a skill.

```
Example task: "Convert this data CSV into a styled Excel report with charts"

Dimensions detected:
  → file reading (CSV input)
  → xlsx manipulation (output format)
  → data visualization (charts)
  → formatting/styling
```

3. **Do NOT load any skill in full yet.** Proceed to Phase 1.

---

## PHASE 1 — Skill Audit (Lightweight Scan)

**Goal:** Determine which skills are relevant and at what depth, without loading
full skill content into active context.

**Rule:** Read only the **frontmatter + section headers** of each available skill.

### Skill Header Schema (expected format):
```yaml
---
name: skill-name
description: One-line summary of what this skill covers
---

## Section A
## Section B
## Section C
```

### Relevance Scoring:

For each skill, assign a **Relevance Score (RS)** per task dimension:

| Score | Meaning                                          |
|-------|--------------------------------------------------|
| `0`   | Skill has no bearing on this task                |
| `1`   | Skill has marginal/reference value               |
| `2`   | Skill has significant overlap with task needs    |
| `3`   | Skill is critical — task cannot proceed without it |

**Decision rule:**
- `RS = 0` → **Skip entirely.** Do not read this skill.
- `RS = 1` → **Skim only.** Extract no more than 1–2 key facts.
- `RS = 2` → **Selective read.** Extract relevant sections only.
- `RS = 3` → **Deep read.** Extract all sections that apply to the task.

---

## PHASE 2 — Section Extraction

**Goal:** From each skill with `RS ≥ 1`, extract only the sections that map to
detected task dimensions. Discard the rest.

### Extraction Rules:

1. **Match sections to dimensions** — A section is extracted only if it directly
   serves at least one task dimension identified in Phase 0.

2. **No copy-paste of full sections** if partial content suffices — trim to the
   minimum actionable instruction set.

3. **Preserve structural intent** — if a section contains a critical sequence
   (e.g., install → configure → run), preserve the full sequence even if only
   one step was the original match. Broken sequences create execution errors.

4. **Annotate source** — tag each extracted block with its origin for traceability:
   ```
   <!-- source: skill-name.md § Section Title -->
   ```

---

## PHASE 3 — Synthesis into `one-temp-skill.md`

**Goal:** Merge extracted blocks into a single, self-contained skill document
optimized for the current task.

### one-temp-skill.md Structure:

```markdown
# one-temp-skill — [Task Label]
> Auto-synthesized | Sources: [list of contributing skills]

---

## [P0] Critical Path
<!-- Sections without which the task CANNOT be completed -->
...

## [P1] Required Context
<!-- Sections needed for correct/complete output -->
...

## [P2] Reference
<!-- Lookup tables, flags, options — consult if needed -->
...

## [P3] Conditionals
<!-- Sections that apply only if a specific condition is true -->
<!-- Condition: [state the condition explicitly] -->
...
```

### Priority Assignment:

| Priority | Label            | When to assign                                                      |
|----------|------------------|---------------------------------------------------------------------|
| `P0`     | CRITICAL PATH    | Must be followed first; blocks all other work if missing            |
| `P1`     | REQUIRED         | Needed for correctness; skipping causes output defects              |
| `P2`     | REFERENCE        | Lookup-style info; consult on demand, not read linearly             |
| `P3`     | CONDITIONAL      | Applies only under a stated condition; skip if condition is false   |

**Priority ordering rule:** Always resolve P0 → P1 before P2 → P3.

### Synthesis Quality Checks:

Before finalizing `one-temp-skill.md`, verify:

- [ ] No contradictions between merged sections from different source skills
- [ ] All task dimensions from Phase 0 are covered by at least one section
- [ ] No duplicate instructions (deduplicate, keep the more specific version)
- [ ] No orphaned steps (every step has a clear predecessor and successor)
- [ ] Total token count is materially lower than sum of all source skills

---

## PHASE 4 — Context Flush & Execution

**Actions:**

1. **Mentally unload all source skills.** They are no longer in active working
   context. Only `one-temp-skill.md` remains as the operative guide.

2. **Execute the task** using `one-temp-skill.md` as the sole reference.
   Follow section order: P0 → P1, then consult P2/P3 as needed.

3. **If a gap is discovered mid-execution:**
   - Do not re-load the full source skill.
   - Formulate a targeted query: *"What does [skill-name] say about [X]?"*
   - Extract only the missing piece and append it to `one-temp-skill.md`
     under the appropriate priority level.

4. **On task completion:** `one-temp-skill.md` is discarded. It is a
   single-use, task-scoped artifact.

---

## Compact Execution Checklist

```
□ PHASE 0  Parse task → list task dimensions
□ PHASE 1  Scan skill headers → assign RS per skill
           Skip RS=0 skills entirely
□ PHASE 2  Extract matching sections from RS≥1 skills
           Trim to minimum actionable content
           Annotate source on each block
□ PHASE 3  Merge → assign P0/P1/P2/P3 priorities
           Run synthesis quality checks
□ PHASE 4  Flush source skills from context
           Execute: P0 → P1 → P2/P3 on demand
           Append gaps as targeted micro-extracts
           Discard one-temp-skill.md on completion
```

---

## Anti-Patterns to Avoid

| Anti-pattern                          | Why it fails                                              |
|---------------------------------------|-----------------------------------------------------------|
| Loading all skills before analyzing   | Pollutes context before relevance is known                |
| Keeping source skills after synthesis | Redundant tokens; creates attention dilution              |
| Extracting "just in case" sections    | Defeats the purpose; reverts to 0% efficiency problem     |
| Assigning everything P0              | Destroys priority signal; execution becomes unordered     |
| Re-synthesizing on every minor task   | Overhead exceeds gain for simple, single-skill tasks      |
| Ignoring source annotations           | Makes mid-execution gap-filling slow and imprecise        |

---

## When NOT to Use This Protocol

This protocol has overhead. Skip synthesis and load skill directly when:

- Only **one skill** is relevant (no merge needed)
- The task is **trivially simple** (< 3 execution steps)
- The skill is **already minimal** (< 50 lines total)
- The task is **exploratory** with no defined deliverable yet

---

## Protocol Metadata

```yaml
protocol:     Operative Skill Synthesis Protocol
version:      1.0
language:     en
scope:        LLM context optimization
applies-to:   Any LLM using .md skill files
trigger:      Multi-skill tasks with partial relevance overlap
output:       one-temp-skill.md (single-use, task-scoped)
lifecycle:    Synthesize → Execute → Discard
```
