ai-task-execution-methodology.md:
---------------------------------
# AI Task Execution Methodology
## A Systematic Approach to Executing Complex Tasks with LLMs

---

## Philosophy

Any non-trivial task consists of three separate stages that must never be mixed:

```
ANALYSIS → PLAN → EXECUTION
```

Mixing stages is the primary cause of errors. LLMs tend to immediately "do" things rather than first understanding the full scope of the work. This leads to omissions, domino errors, and rework.

---

## Workflow Structure

### Phase 0 — Context Loading

Before any work begins, all context is loaded and explicitly confirmed:

- **Specification / guide** — the rules the result must conform to
- **Materials** — files, code, data to be processed
- **Constraints** — what must not be touched, what is critical, priorities

**Rule:** nothing gets done at this stage. Only reading and confirming that loading is complete.

```
User: load the guide, do nothing
AI: [reads] → "Guide loaded ✓"

User: load the files, these are the working materials
AI: [reads all files] → table of files with line counts and purpose
```

**Why it matters:** if context is loaded incompletely or misunderstood — all subsequent analysis will be wrong.

---

### Phase 1 — Analysis

Systematic examination of all materials **against** the specification.

#### 1.1 Define Violation Categories

First, build a taxonomy — an exhaustive list of problem types. Without it, the analysis will be incomplete.

```
Example for code refactoring:
- CSS_PREFIX — abbreviations in class names
- KEYFRAME_PREFIX — abbreviations in @keyframes
- DATA_CUSTOM — custom attributes without a prefix
- DATA_ACTION_VALUE — incorrect value format
- ID_PREFIX — id without widget prefix
- ID_DEAD — dead ids (present in HTML, unused anywhere)
- ID_JS_HOOK — id used as a JS hook (violates Law Zero)
- JS_VAR — abbreviations in variable names
```

#### 1.2 Analyze Each File Against Each Category

Sequential pass: file × category. No skipping ahead.

**Technique:** ask layered questions during analysis:
1. What is violated in CSS?
2. What is violated in HTML?
3. What is violated in JS?
4. Which ids are live, which are dead?
5. Where are the domino dependencies?

#### 1.3 Domino Analysis

For each violation: what else will break if only this one location is fixed?

```
Violation: CSS token --msg-bubble-radius → --messages-bubble-radius

Domino:
├── CSS lines 165,166: var(--msg-bubble-radius) in child rules
├── JS line 978: getPropertyValue('--msg-bubble-radius')
└── (no HTML — token is not used in attributes)
```

**Rule:** the domino must be exhaustive. An incomplete domino = broken code after the fix.

---

### Phase 2 — Task Map

The analysis is turned into a structured artifact. This is not just a list — it is a machine-readable map with dependencies.

#### Map Structure

```json
{
  "meta": {
    "total_issues": 84,
    "guide_version": "containerization-6"
  },
  "files": [
    {
      "file": "widget.html",
      "issues": [
        {
          "id": "widget-001",
          "category": "CSS_PREFIX",
          "severity": "HIGH",
          "change_type": "RENAME",
          "location": {
            "lines": { "start": 69, "end": 82 },
            "context": "--msg-bubble-radius: 0.75rem;",
            "scope": "CSS:tokens"
          },
          "current": "--msg-bubble-radius",
          "expected": "--messages-bubble-radius",
          "description": "Abbreviation 'msg' instead of 'messages'. §7.1",
          "rule_ref": "§7.1",
          "dependencies": [
            {
              "issue_id": "widget-002",
              "file": "widget.html",
              "description": "CSS line 165: var(--msg-bubble-radius) — token consumer"
            }
          ],
          "status": "pending"
        }
      ]
    }
  ]
}
```

#### Required Fields

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier for domino references |
| `severity` | CRITICAL / HIGH / MEDIUM / LOW — determines execution order |
| `location.lines` | Exact line numbers — without these, finding and verifying is impossible |
| `location.context` | Verbatim code fragment — for identification without opening the file |
| `current` / `expected` | What exists now → what it should be |
| `dependencies` | Domino with references to issue_id, not just plain text |
| `status` | `pending` / `in-progress` / `done` — progress tracking |

#### Severity

```
CRITICAL — code is broken or violates an architectural invariant
           Example: JS looks up DOM via id instead of data-attributes

HIGH     — naming violates the standard, scalability is at risk
           Example: abbreviations in CSS classes, tokens, ids

MEDIUM   — noise, does not affect functionality but pollutes the code
           Example: dead ids that are not used anywhere

LOW      — stylistic deviation
```

#### Change Types

```
RENAME   — rename while preserving function
DELETE   — remove entirely
REPLACE  — substitute one construct for another
ADD      — add something missing
MOVE     — relocate to a different place
```

---

### Phase 3 — Execution Plan

The task map is turned into an interactive tracker with grouping.

#### Plan Structure

```
File A (group)
  ├── CSS prefix (subgroup)
  │   ├── [ ] issue-001 — --msg-* → --messages-* (domino: 3)
  │   └── [ ] issue-002 — .msg-* → .messages-* (domino: 11)
  ├── @keyframes (subgroup)
  │   └── [ ] issue-003 — msg-bubble-in → messages-bubble-in
  └── id prefix (subgroup)
      └── [ ] issue-004 — id="msg-seller-name" → messages-seller-name

File B (group)
  └── ...
```

**Grouping rules:**
- One file = one group
- One violation type = one subgroup
- One specific issue = one item with a status
- Domino is executed together with the parent issue — not separately

#### Execution Priority

```
1. CRITICAL (Law Zero — architectural violations)
2. HIGH (naming — many dominos, high collision risk)
3. MEDIUM (dead code — safe, but needs cleanup)
4. LOW (stylistics)
```

Within a severity level — order by number of dominos (more dependencies = executed sooner).

---

### Phase 4 — Execution

#### Principles

**1. One file at a time**

Do not switch between files mid-way. A file is opened, all its issues are resolved, the file is validated, then move on to the next.

**2. Domino is executed immediately**

If issue-001 has 3 domino dependencies — all 4 changes are made in a single pass. Not "parent first, domino later."

**3. Multiple passes per file**

Complex files are processed in layers:
```
Pass 1: CSS (tokens + classes + keyframes)
Pass 2: HTML attributes
Pass 3: JS strings and expressions
Pass 4: ids (remove dead ones, rename live ones)
```

Why not all at once: regular expressions and string replacements can conflict. Layered processing isolates the risk.

**4. Order of replacements within a pass**

Always from longest to shortest:
```python
# ❌ Wrong
replacements = ['.msg-msg', '.msg-msg--sent', '.msg-msg--recv']
# When replacing .msg-msg → .messages-bubble
# the pattern will no longer match .msg-msg--sent

# ✅ Correct
replacements = [
    ('.msg-msg--sent', '.messages-bubble--sent'),  # more specific — first
    ('.msg-msg--recv', '.messages-bubble--received'),
    ('.msg-msg', '.messages-bubble'),               # general — last
]
```

**5. Validate after each file**

Do not defer to the end. An error in file A must not affect confidence in file B.

---

### Phase 5 — Validation

#### Validation Levels

**1. Automated — pattern search**

```python
# Search for remaining abbreviations
import re
remaining = [line for line in src.split('\n') 
             if re.search(r'\bmsg-', line) 
             and not line.strip().startswith(('#', '//', '<!--', '*'))]
```

Exclude comments — they do not affect code behavior but pollute results.

**2. Semantic — checking for legitimate exceptions**

Not all pattern matches are violations. For each "remaining" occurrence, understand the context:

```
document.querySelector('.widget-container')  ← LEGAL (bootstrap by container class)
document.querySelector('#some-id')           ← VIOLATION (Law Zero)

id="aria-title-for-modal"                    ← LEGAL (ARIA reference)
id="my-btn"  + JS: document.getElementById  ← VIOLATION (JS hook)
```

**3. Final Report**

```
FILE                    STATUS    CRITICAL  HIGH  MEDIUM
messages.html           ✅ CLEAN     0        0      0
my-reviews.html         ✅ CLEAN     0        0      0
mywallet.html           ✅ CLEAN     0        0      0  (Law Zero: 2 legal)
...
```

---

## Requirements Specification for Creating a Task Map

When specifying the task of creating a violation map, the following must be defined:

### Required Spec Elements

```markdown
1. Files in scope — list of all files to be analyzed

2. Specification — the document/guide to analyze against

3. Violation categories — exhaustive list with codes
   (without this, the analysis will be incomplete)

4. Severity scale — what counts as CRITICAL, HIGH, MEDIUM, LOW

5. Change types — RENAME, DELETE, REPLACE, ADD, MOVE

6. JSON schema — exact structure of the output artifact with field types

7. Rules for issue ids — issue_id format, numbering rules

8. Rules for dependencies — how to reference, what must be included

9. Requirements for the context field — maximum length, what to include

10. What is NOT in the map — clear scope boundaries
```

### Spec Improvements Over a Naive Approach

| Naive Spec Problem | Solution |
|--------------------|----------|
| No JSON schema | Specify each field's type, provide an example |
| No unique IDs | Format: `{widget}-{N:03d}`, numbered by severity |
| No current/expected separation | Two fields, not a single "description" |
| Domino is just text | Domino contains `issue_id` — a verifiable reference |
| No map validation | All `issue_id` in dependencies must exist in the map |
| No context field | Exact code fragment ≤120 characters |
| No severity | Cannot determine execution order |
| No change_type | RENAME and DELETE are different operations |

---

## Templates for Common Task Types

### Refactoring Against a Guide

```
Phase 0: load guide + all files
Phase 1: analyze file × violation category
Phase 2: JSON map with dominos
Phase 3: interactive plan (group=file, subgroup=violation type)
Phase 4: execution CRITICAL → HIGH → MEDIUM, file by file
Phase 5: automated pattern validation + manual exception review
```

### Codebase Audit

```
Phase 0: load quality standard + files
Phase 1: analyze by dimension (security, performance, accessibility, naming)
Phase 2: map with severity and effort estimates
Phase 3: plan grouped by dimension, not by file
Phase 4: quick wins first (HIGH severity + LOW effort)
Phase 5: regression tests
```

### API Migration

```
Phase 0: documentation for old and new API + file list
Phase 1: find all usages of deprecated methods
Phase 2: replacement map with breaking changes marked as CRITICAL
Phase 3: plan by files, breaking changes isolated into a separate batch
Phase 4: execution, tests after each file
Phase 5: grep for old patterns + smoke test
```

### Large-Scale Rename (brand/namespace)

```
Phase 0: list of old names + new names + files
Phase 1: find ALL occurrences including comments, documentation, tests
Phase 2: map split by file type and context
Phase 3: plan: types/interfaces first, then implementation, then tests, then documentation
Phase 4: replacements from longest to shortest, validate after each file
Phase 5: final grep, build, tests
```

---

## AI Checklist Upon Receiving a Task

```
□ Have I loaded and read the ENTIRE specification (not just the beginning)?
□ Have I loaded ALL files mentioned in the task?
□ Have I compiled an exhaustive taxonomy of violation types?
□ For each violation, have I found ALL domino dependencies?
□ Does the map contain exact line numbers (not "around" or "in method X")?
□ Do all issue_ids in dependencies actually exist in the map?
□ Is the execution order determined by severity?
□ Does each file have a plan of sequential passes?
□ Is validation planned after each file, not just at the end?
□ Do I know what constitutes a LEGAL exception for each pattern?
```

---

## Anti-Patterns

### ❌ Analyzing and Fixing Simultaneously

```
Bad:  "Found a violation — fixed it immediately — found the next one..."
Good: Full analysis → full map → execute the map
```

Reason: when analyzing and fixing simultaneously, the overall picture is lost. It is unknown how many more violations remain ahead, making it impossible to prioritize correctly.

### ❌ Descriptive Dominos Instead of Reference-Based

```
Bad:  "dependencies": [{"description": "update JS"}]
Good: "dependencies": [{"issue_id": "messages-012", "description": "..."}]
```

Reason: a descriptive domino cannot be verified. A reference-based domino can be validated automatically.

### ❌ Replacements in the Wrong Order

```
Bad:  .msg-msg → then .msg-msg--sent (will no longer be found)
Good: .msg-msg--sent first, then .msg-msg
```

### ❌ Validation Only at the End

```
Bad:  process 8 files → verify everything at once
Good: file → validate → next file
```

Reason: an error in file 2 may not surface until file 7. Isolated validation localizes the problem.

### ❌ Ignoring Comments During Validation

```
Bad:  grep finds 3 occurrences — panic
Good: verify that all 3 are in comments — ok
```

### ❌ Map Without Line Numbers

```
Bad:  "location": {"scope": "JS:_bubble"}
Good: "location": {"lines": {"start": 712, "end": 725}, "context": "bbl.className = ['msg-msg..."}
```

Reason: without line numbers, the location cannot be found automatically, nor can it be verified after the fix.

---

## Working with Large Files

When working with files > 500 lines:

**Read the entire file before starting.** Do not start from the first line and work downward — first get the full picture.

**Work in pattern batches**, not one at a time:
```python
# All tokens in one dictionary
token_map = {
    '--msg-bubble-radius': '--messages-bubble-radius',
    '--msg-bubble-sent-bg': '--messages-bubble-sent-bg',
    # ...14 tokens at once
}
for old, new in token_map.items():
    src = src.replace(old, new)
```

**Split into logical passes** (CSS → HTML → JS), not arbitrary chunks.

**Confirm the result of each pass** before proceeding to the next:
```
After pass 1 (CSS): grep shows 0 remaining tokens
After pass 2 (HTML): grep shows 0 remaining classes in attributes
...
```

---

## Execution Quality Metrics

### After Completing the Work, Ask Yourself:

```
1. Does the number of issues in the map equal the number of closed issues?
2. Does grep for all violation patterns return 0 (excluding comments)?
3. Do all ids in HTML have the correct widget prefix?
4. Are all data-action values in kebab-case verb-noun format?
5. Are there no document.querySelector('#...') or getElementById calls used for logic?
6. Do all addEventListener calls have a signal (AbortController) or { once: true }?
7. Has the code semantics not changed — only naming?
```

### Numerical Indicators

Record before and after:
- Number of files
- Total line count
- Number of issues by severity
- Number of files with zero violations

This allows for an objective assessment of the scope and completeness of the work.

---

*This methodology was developed based on the refactoring of 9 widgets (9,007 lines, 84 violations) against the containerization-6 standard.*


ai-task-execution-methodology-driver.md:
---------------------------------
# AI Task Execution Methodology Driver
## Multi-Plan Orchestration, Dependency Management & Atomic Context Integrity

> **Role:** This document is the orchestration layer over `ai-task-execution-methodology.md`.  
> It does not replace the base methodology — it manages multiple simultaneous instances of it.  
> The base methodology handles *one plan*. The Driver handles *N plans, M guides, K sessions*.

---

## Philosophy

The base methodology defines the single-plan invariant:

```
ANALYSIS → PLAN → EXECUTION
```

Real environments require managing multiple concurrent plans, dynamically loaded guides, and
LLM context boundaries. The Driver extends the invariant to:

```
REGISTRY_INIT
    ↓
GRAPH_BUILD       ← guides loaded, versions resolved, invariants extracted
    ↓
CONFLICT_SCAN     ← all conflicts detected before any execution begins
    ↓
SCHEDULE          ← topological sort, priority, conflict groups
    ↓
┌── [PLAN₁: ANALYSIS → PLAN → EXECUTE] ── ATOMIC_CHECK ── CHECKPOINT ──┐
├── [PLAN₂: ANALYSIS → PLAN → EXECUTE] ── ATOMIC_CHECK ── CHECKPOINT ──┤ → COHERENCE_GATE
└── [PLAN_N: ANALYSIS → PLAN → EXECUTE] ── ATOMIC_CHECK ── CHECKPOINT ─┘
    ↓
GLOBAL_VALIDATION
```

**Three new invariants — non-negotiable:**

**Invariant I — Registry First.**
Nothing executes without being registered. Unregistered guides and plans are invisible to the
system, causing silent conflicts and lost context.

**Invariant II — Atomic With Self-Check.**
Every atomic operation validates its own post-conditions before the system proceeds.
The system does not trust that an operation succeeded — it verifies.

**Invariant III — Coherence Gate.**
Before any new plan starts executing, the system checks that the global state is consistent.
A plan must not begin against a broken world.

---

## System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                      GLOBAL REGISTRY (GR)                            │
│                  ← single source of truth →                          │
│                                                                       │
│  ┌──────────────────┐  ┌─────────────────┐  ┌──────────────────┐   │
│  │   GUIDE_REG      │  │   PLAN_REG      │  │   TASK_REG       │   │
│  │  (symbol table)  │  │ (process table) │  │ (thread table)   │   │
│  └────────┬─────────┘  └────────┬────────┘  └────────┬─────────┘   │
│           │                     │                     │              │
│  ┌────────┴─────────────────────┴─────────────────────┴──────────┐  │
│  │                        LOCK_TABLE                              │  │
│  │         (resource locks · guide locks · plan locks)            │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
         │                    │                      │
         ▼                    ▼                      ▼
  ┌─────────────┐   ┌──────────────────┐   ┌──────────────────┐
  │ TASK EXEC   │   │   DEPENDENCY     │   │   CHECKPOINT     │
  │ GRAPH (TEG) │   │   RESOLVER       │   │   STORE          │
  └──────┬──────┘   └────────┬─────────┘   └────────┬─────────┘
         │                    │                      │
         └────────────────────┴──────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │    COHERENCE GATE    │
                   │  (global invariant   │
                   │    checker)          │
                   └──────────────────────┘
```

**Architectural analogs:**

| Driver Component | OS Analog | Compiler Analog |
|-----------------|-----------|-----------------|
| `GUIDE_REG` | Shared library table | Symbol table |
| `PLAN_REG` | Process table (PCB) | Compilation unit list |
| `TASK_REG` | Thread table | AST node registry |
| `LOCK_TABLE` | Mutex / rwlock table | — |
| `TEG` | Process DAG | AST with dependencies |
| `CHECKPOINT_STORE` | Journaling (ext4/zfs) | Incremental compilation cache |
| `COHERENCE_GATE` | Type checker | Invariant enforcer |
| `ATOMIC_CHECK` | Transaction commit | Assertion pass |

---

## Core Data Structures

### 3.1 Global Registry Initialization

```json
{
  "version": "driver-1.0",
  "session_id": "sess-YYYYMMDD-NNN",
  "created_at": "ISO8601",
  "guide_registry": {},
  "plan_registry": {},
  "task_registry": {},
  "lock_table": {},
  "checkpoint_store": {},
  "invariant_registry": {},
  "conflict_matrix": {},
  "context_budget": {
    "total_tokens": 200000,
    "allocated": 0,
    "critical_reserve": 20000,
    "compression_threshold": 0.70
  }
}
```

**Rule:** GR is initialized first in every session. All subsequent operations reference it.
The `session_id` ties together all plans and guides. Guides from a previous session are
not automatically valid in a new session — they must be re-registered.

---

### 3.2 Guide Descriptor (GD) — Compiler Symbol Analog

Each guide is registered with a full descriptor:

```json
{
  "guide_id": "arch-containerization-6",
  "name": "Containerization Standard v6",
  "type": "ARCHITECTURAL",
  "scope": "GLOBAL",
  "version": { "major": 6, "minor": 0, "patch": 0 },
  "path": "skills/containerization-6.md",
  "loaded_at": "ISO8601",
  "status": "ACTIVE",
  "supersedes": ["arch-containerization-5"],
  "conflicts_with": [],
  "applies_to_patterns": ["**/*.html", "**/*.css", "**/*.js"],
  "invariants": [
    {
      "id": "INV-LAW0",
      "description": "No JS DOM lookup by id",
      "severity": "CRITICAL",
      "check": { "type": "PATTERN_ABSENT", "pattern": "getElementById|querySelector\\('#", "exclude_comments": true }
    },
    {
      "id": "INV-CSS-TOKENS",
      "description": "All custom properties must use full widget name, no abbreviations",
      "severity": "HIGH",
      "check": { "type": "PATTERN_ABSENT", "pattern": "--[a-z]{1,4}-[a-z]", "exclude_comments": true }
    }
  ],
  "priority": 1,
  "used_by_plans": []
}
```

**Guide Types — strict hierarchy:**

| Type | Scope | Authority | Override allowed? | Example |
|------|-------|-----------|------------------|---------|
| `ARCHITECTURAL` | GLOBAL | Supreme | Never | Containerization standard, Law Zero |
| `SPECIALIZED` | PLAN | Domain | By higher ARCH only | CSS naming guide, API migration spec |
| `OPERATIONAL` | TASK | Execution | By SPEC and ARCH | Large file handling, replacement order |

**ARCHITECTURAL > SPECIALIZED > OPERATIONAL** — when guides conflict, higher type wins.

---

### 3.3 Plan Control Descriptor (PCD) — OS Process Block Analog

```json
{
  "plan_id": "PLAN-001",
  "name": "UI Refactoring — Messages Widget",
  "status": "RUNNING",
  "phase": "EXECUTION",
  "priority": 1,
  "conflict_group": "ui-widgets",
  "created_at": "ISO8601",
  "started_at": "ISO8601",
  "guides": {
    "architectural": ["arch-containerization-6"],
    "specialized": ["spec-css-naming"],
    "operational": ["ops-large-file"]
  },
  "scope": {
    "files": ["src/widgets/messages.html", "src/widgets/messages.css"],
    "excluded": [],
    "read_only": ["src/shared/tokens.css"]
  },
  "dependencies": {
    "requires_after": [],
    "blocks": ["PLAN-002"]
  },
  "resources": {
    "locks_held": ["src/widgets/messages.html"],
    "locks_waiting": []
  },
  "progress": {
    "total_tasks": 84,
    "done": 42,
    "failed": 0,
    "skipped": 0
  },
  "last_checkpoint": {
    "checkpoint_id": "CKP-001-042",
    "task_id": "T-001-042",
    "timestamp": "ISO8601"
  },
  "context_snapshot_id": "CTX-001-042",
  "rollback_target": "CKP-001-000"
}
```

**Plan Lifecycle — OS process states:**

```
        NEW
         │
         ▼
     ANALYZING ──────── Phase 1: full analysis in progress
         │
         ▼
     PLANNED ─────────── Phase 2-3: task map + execution plan ready
         │
         ▼
      READY ────────────  awaiting resources or dependency completion
         │
   ┌─────▼──────┐
   │  RUNNING   │ ←── scheduler activates
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │  BLOCKED   │ ←── waiting for lock or dependency plan
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │VALIDATING  │ ←── Phase 5: final validation pass
   └─────┬──────┘
         │
      ┌──┴──┐
      │     │
     DONE  FAILED ──→ ROLLING_BACK ──→ READY (retry)
                                    ──→ ABORTED (unrecoverable)
```

---

### 3.4 Task Execution Node (TEN) — AST Node Analog

```json
{
  "task_id": "T-001-042",
  "plan_id": "PLAN-001",
  "type": "ATOMIC",
  "parent_id": "T-001-040",
  "children": [],
  "status": "DONE",
  "phase": "EXECUTION",
  "order_index": 42,
  "guide_refs": ["arch-containerization-6.INV-CSS-TOKENS"],
  "resource_lock": "src/widgets/messages.html",
  "operation": {
    "type": "RENAME",
    "target": "--msg-bubble-radius",
    "replacement": "--messages-bubble-radius",
    "location": { "file": "messages.html", "lines": { "start": 69, "end": 82 } },
    "context": "--msg-bubble-radius: 0.75rem;"
  },
  "pre_conditions": [
    "T-001-041.status == DONE",
    "LOCK_TABLE['messages.html'].holder == 'PLAN-001'"
  ],
  "post_conditions": [
    { "type": "PATTERN_COUNT", "pattern": "--msg-bubble-radius", "file": "messages.html", "expected": 0 },
    { "type": "PATTERN_COUNT", "pattern": "--messages-bubble-radius", "file": "messages.html", "expected_min": 1 },
    { "type": "INVARIANT_CHECK", "invariant_id": "INV-CSS-TOKENS" }
  ],
  "atomic_check": {
    "status": "PASSED",
    "pre_check": "PASSED",
    "post_check": "PASSED",
    "invariant_check": "PASSED",
    "timestamp": "ISO8601"
  },
  "checkpoint_after": true,
  "rollback_snapshot": "SNAP-001-041"
}
```

**Task Node Types:**

| Type | Description | Self-validates? | Modifies? |
|------|-------------|----------------|-----------|
| `ATOMIC` | Smallest executable unit. Has pre/post conditions. | Yes | Yes |
| `COMPOSITE` | Container for ordered ATOMICs. Validates after all children DONE. | Yes (aggregate) | Via children |
| `CHECKPOINT` | State snapshot. No operation — recording only. | Hash match | No |
| `VALIDATION` | Read-only verification pass. Never modifies anything. | Yes | No |
| `GATE` | Coherence check. Must PASS for execution to proceed. | Yes | No |

---

## Task Execution Graph (TEG)

The TEG is the executable form of the task map (Phase 2 of base methodology),
extended with dependency edges, gates, and checkpoints.

### Graph Structure

```
TEG Root
│
├── GATE: pre-execution coherence check
│         (all invariants satisfied? all guides loaded? all locks available?)
│
├── COMPOSITE: File — messages.html  [PLAN-001]
│   │
│   ├── CHECKPOINT: pre-file snapshot
│   │
│   ├── COMPOSITE: Pass 1 — CSS Tokens
│   │   ├── ATOMIC: T-001-001 (--msg-bubble-radius → --messages-bubble-radius)
│   │   │   └── VALIDATION: grep count == 0
│   │   ├── ATOMIC: T-001-002 (--msg-sent-bg → --messages-sent-bg)
│   │   │   └── VALIDATION: grep count == 0
│   │   └── VALIDATION: all Pass-1 patterns → 0
│   │
│   ├── COMPOSITE: Pass 2 — CSS Classes
│   │   ├── ATOMIC: T-001-010 (.msg-bubble → .messages-bubble)
│   │   └── VALIDATION: all Pass-2 patterns → 0
│   │
│   └── CHECKPOINT: post-file snapshot ← only after all passes clean
│
├── COMPOSITE: File — messages.css  [PLAN-001]
│   └── ... (same structure)
│
└── GATE: post-execution coherence check ← system-level final gate
```

### Graph Edge Types

| Edge | Meaning | Breaks cycle? |
|------|---------|--------------|
| `REQUIRES` | B cannot start until A is DONE | Yes (hard dependency) |
| `BLOCKS` | A must not run while B is RUNNING | Yes (lock contention) |
| `DOMINOES_INTO` | Fix A requires fix B in same pass | No (same transaction) |
| `INVALIDATES` | A completion makes B unnecessary | — |
| `GATE_BEFORE` | GATE node must PASS before this node starts | Yes |

---

## Guide Management

### 5.1 Loading Protocol

Guides load in type order: **ARCHITECTURAL → SPECIALIZED → OPERATIONAL**

```
1. Receive guide (path or inline content)
2. Parse: guide_id, type, version, invariants, conflicts_with, supersedes
3. Check against all ACTIVE guides for conflicts
4. If conflict → CONFLICT_RESOLUTION (see §7)
5. If supersedes another → mark old guide SUPERSEDED in GUIDE_REG
6. Register in GUIDE_REG with status ACTIVE
7. Notify all plans whose scope overlaps with guide's applies_to_patterns
8. Affected plans: re-run invariant pre-scan on their task maps
9. Confirm output
```

**Confirmation output format:**

```
GUIDE LOADED ✓
  id:          arch-containerization-6
  type:        ARCHITECTURAL (scope: GLOBAL)
  version:     6.0.0
  invariants:  7 extracted and registered
  supersedes:  arch-containerization-5 → marked SUPERSEDED
  affects:     PLAN-001 (2 files), PLAN-002 (3 files)
  conflicts:   none detected
  action:      invariant pre-scan triggered for PLAN-001, PLAN-002
```

### 5.2 Invariant Registry

Invariants extracted from ARCHITECTURAL guides are stored separately.
They persist even if the guide is reloaded or updated.

```json
{
  "invariant_id": "INV-LAW0",
  "source_guide": "arch-containerization-6",
  "description": "No JS DOM lookup by id — only data-attributes",
  "severity": "CRITICAL",
  "scope": "GLOBAL",
  "check": {
    "type": "PATTERN_ABSENT",
    "pattern": "getElementById|querySelector\\('#",
    "exclude_comments": true
  },
  "status": "ACTIVE",
  "cannot_be_overridden_by": ["SPECIALIZED", "OPERATIONAL"]
}
```

**Rule:** ARCHITECTURAL invariants cannot be overridden by any plan, any SPECIALIZED guide,
or any LLM reasoning. If an operation would violate a CRITICAL invariant — the operation
is blocked, not the invariant.

### 5.3 Guide Version Resolution

```
Situation: arch-containerization-5 (ACTIVE) + arch-containerization-6 arrives

Conflict detected: same base, higher version
    ↓
Resolution algorithm:
    if new.version > existing.version AND same guide family:
        existing.status → SUPERSEDED
        new.status → ACTIVE
        notify all plans using existing
        plans must re-validate task maps against new invariants
    
    if same version → DUPLICATE_ERROR (do not reload silently)
    if lower version → REJECT (older version cannot supersede newer)
```

---

## Multi-Plan Scheduling

### 6.1 Scheduling Algorithm

```
1. Build plan dependency graph (DAG) from all PCD.dependencies fields
2. Topological sort → execution order tiers
3. Within same tier, sort by priority (1 = highest)
4. Group by conflict_group — same group → sequential execution
5. Cross-group plans at same tier → can run in parallel IF no resource conflicts
6. Resource check: if file locked → plan → BLOCKED, add to lock wait queue
7. Activate next READY plan: status → RUNNING
```

**Topological Sort Example:**

```
Plans registered:
  PLAN-000: deps=[]            → tier 0
  PLAN-001: deps=[PLAN-000]    → tier 1
  PLAN-002: deps=[PLAN-000]    → tier 1
  PLAN-003: deps=[PLAN-001, PLAN-002] → tier 2

conflict_groups:
  "ui-widgets": [PLAN-001, PLAN-002] → sequential within group

Execution schedule:
  Tier 0: [PLAN-000]
  Tier 1: [PLAN-001 → PLAN-002]   (sequential: same conflict_group)
  Tier 2: [PLAN-003]               (starts after both tier-1 plans DONE)
```

### 6.2 Conflict Groups

Plans in the same `conflict_group` cannot execute concurrently —
they operate in overlapping domains and would produce conflicting state.

```json
{
  "conflict_groups": {
    "ui-widgets": {
      "members": ["PLAN-001", "PLAN-002"],
      "policy": "SEQUENTIAL",
      "order_within_group": ["PLAN-001", "PLAN-002"]
    },
    "api-migration": {
      "members": ["PLAN-003"],
      "policy": "ISOLATED"
    }
  }
}
```

**Policy types:**

| Policy | Meaning |
|--------|---------|
| `SEQUENTIAL` | Members run one after another in declared order |
| `ISOLATED` | Group has no interaction with others (can run in parallel with other groups) |
| `GATED` | Next member starts only after previous passes its validation gate |

### 6.3 Resource Locking

**Lock types (OS mutex/rwlock analog):**

| Lock Type | Concurrent Holders | Use Case |
|-----------|--------------------|----------|
| `EXCLUSIVE` | 1 plan only | File being modified |
| `SHARED` | N plans simultaneously | Guide being read |
| `GUIDE_WRITE` | 1 (during guide update) | Guide registration or supersession |

**Lock acquisition flow:**
```
Plan requests lock on file X:
    1. Check LOCK_TABLE[X]
    2. If EXCLUSIVE lock held by another plan:
           plan.status → BLOCKED
           add to LOCK_TABLE[X].wait_queue
    3. If no lock:
           acquire EXCLUSIVE
           LOCK_TABLE[X] = { type: EXCLUSIVE, holder: PLAN-ID, acquired_at: NOW }
    4. On file completion:
           release lock
           notify wait_queue.head → next plan acquires
```

**Deadlock prevention:**
- All required locks must be declared in PCD.scope.files before plan starts
- Locks acquired in deterministic order (alphabetical by file path)
- Lock timeout: plan holding lock without progress for N tasks → ALERT → human review

---

## Atomic Execution Protocol (AEP)

Every atomic operation follows this protocol without exception.
This is the core correctness mechanism of the Driver.

### 7.1 Full Protocol

```
┌──────────────────────────────────────────────────────────────────┐
│                    ATOMIC EXECUTION PROTOCOL                      │
│                                                                   │
│  ① PRE_CHECK                                                     │
│    ├── all pre_conditions satisfied?                              │
│    ├── resource lock held by this plan?                           │
│    ├── no CRITICAL invariant would be violated by this op?        │
│    └── PASS → proceed | FAIL → HALT, log reason, block task       │
│                          │                                        │
│                          ▼                                        │
│  ② EXECUTE                                                       │
│    ├── snapshot current state (rollback_snapshot)                 │
│    ├── perform the atomic operation                               │
│    ├── record before/after in journal                             │
│    └── do NOT proceed to next task yet                            │
│                          │                                        │
│                          ▼                                        │
│  ③ SELF_CHECK                                                    │
│    ├── all post_conditions satisfied?                             │
│    ├── all invariant_checks pass?                                 │
│    ├── no regressions in adjacent already-completed operations?   │
│    └── PASS → commit | FAIL → rollback                           │
│                          │                                        │
│                          ▼                                        │
│  ④ CHECKPOINT_COMMIT (if checkpoint_after == true)               │
│    ├── save context snapshot (CTX)                                │
│    ├── task.status → DONE                                         │
│    ├── plan.progress.done++                                       │
│    └── release lock if this was last task for this file           │
│                          │                                        │
│                          ▼                                        │
│  ⑤ SYSTEM_COHERENCE (at GATE nodes or every N atomic ops)        │
│    ├── all active plans' invariants still satisfied?              │
│    ├── no cross-plan conflicting changes detected?                │
│    ├── context budget not in critical zone?                       │
│    └── PASS → continue | FAIL → system halt                       │
└──────────────────────────────────────────────────────────────────┘
```

### 7.2 Post-Condition Types

```json
[
  { "type": "PATTERN_COUNT",
    "pattern": "--msg-bubble-radius",
    "file": "messages.html",
    "expected": 0,
    "comment": "old token must be gone" },

  { "type": "PATTERN_COUNT",
    "pattern": "--messages-bubble-radius",
    "file": "messages.html",
    "expected_min": 1,
    "comment": "new token must exist" },

  { "type": "INVARIANT_CHECK",
    "invariant_id": "INV-CSS-TOKENS",
    "comment": "global CSS token invariant still satisfied" },

  { "type": "CROSS_FILE_CONSISTENCY",
    "source_file": "messages.html",
    "target_file": "messages.css",
    "pattern": "--messages-bubble-radius",
    "comment": "token used consistently across both files" },

  { "type": "FILE_UNCHANGED",
    "file": "src/shared/tokens.css",
    "comment": "read-only file must not be touched" }
]
```

| Post-Condition Type | Description |
|--------------------|-------------|
| `PATTERN_COUNT` | grep count equals expected value |
| `PATTERN_ABSENT` | pattern not found anywhere in file |
| `PATTERN_PRESENT` | pattern found at least N times |
| `INVARIANT_CHECK` | named invariant passes its check |
| `CROSS_FILE_CONSISTENCY` | same pattern consistent across two files |
| `FILE_UNCHANGED` | file hash matches pre-execution snapshot |
| `LINE_EXISTS` | specific line content at specific location |

### 7.3 Rollback Protocol

```
TASK FAILED (T-001-042, post-condition PATTERN_COUNT: expected 0, got 3)
    │
    ▼
[1] Journal: TASK_FAILED with actual state and failure detail
    │
    ▼
[2] Load rollback_snapshot (file state before this task)
    │
    ▼
[3] Restore file to snapshot state
    │
    ▼
[4] Verify restoration: file_hash == snapshot.hash
    │
    ▼
[5] task.status → FAILED → ROLLING_BACK → PENDING
    │
    ▼
[6] Output alert:
    "ROLLBACK: T-001-042 | Reason: PATTERN_COUNT (--msg-bubble-radius) expected 0, got 3
     File: messages.html | Snapshot: SNAP-001-041 | Retry: 1/2"
    │
    ▼
[7] Analyze failure:
    ├── RETRYABLE (transient, e.g. wrong replacement order) → retry with correction
    └── STRUCTURAL (wrong approach, invariant mismatch) → HALT plan, require review
```

---

## Checkpoint & Context Snapshot System

### 8.1 Checkpoint Types

| Type | Trigger | Frequency |
|------|---------|-----------|
| `AUTO_ATOMIC` | After each ATOMIC task (when `checkpoint_after: true`) | Per task |
| `FILE_BOUNDARY` | Before and after each file | Automatic |
| `PHASE_BOUNDARY` | At each phase change (ANALYSIS→PLAN, PLAN→EXECUTE, etc.) | Automatic |
| `GATE` | At each GATE node | Automatic |
| `BUDGET_PRESSURE` | When context budget crosses compression threshold | Automatic |
| `MANUAL` | User or guide directive | On demand |

### 8.2 Context Snapshot Structure

The snapshot is the "context switch register save" for the LLM —
everything needed to resume execution from this exact point:

```json
{
  "snapshot_id": "CTX-001-042",
  "plan_id": "PLAN-001",
  "task_id": "T-001-042",
  "timestamp": "ISO8601",

  "active_guides": [
    { "id": "arch-containerization-6", "version": "6.0.0", "status": "ACTIVE" },
    { "id": "spec-css-naming",         "version": "2.1.0", "status": "ACTIVE" }
  ],

  "plan_state": {
    "status": "RUNNING",
    "phase": "EXECUTION",
    "current_file": "messages.html",
    "current_pass": "PASS_1_CSS_TOKENS",
    "progress": { "done": 42, "total": 84, "failed": 0 }
  },

  "last_3_operations": [
    { "task_id": "T-001-040", "type": "RENAME", "target": "--msg-sent-bg",      "result": "DONE" },
    { "task_id": "T-001-041", "type": "RENAME", "target": "--msg-recv-bg",      "result": "DONE" },
    { "task_id": "T-001-042", "type": "RENAME", "target": "--msg-bubble-radius","result": "DONE" }
  ],

  "next_3_operations": [
    { "task_id": "T-001-043", "type": "RENAME",     "target": "--msg-avatar-size" },
    { "task_id": "T-001-044", "type": "VALIDATION", "scope": "PASS_1_complete"   },
    { "task_id": "T-001-045", "type": "CHECKPOINT", "phase": "PASS_2_START"      }
  ],

  "open_issues": {
    "remaining_in_current_file": 42,
    "remaining_in_plan": 42,
    "blocked_tasks": [],
    "unresolved_dominos": []
  },

  "active_locks": {
    "messages.html": { "type": "EXCLUSIVE", "holder": "PLAN-001" }
  },

  "global_invariant_status": {
    "INV-LAW0":       "SATISFIED",
    "INV-CSS-TOKENS": "IN_PROGRESS"
  },

  "context_budget": {
    "used": 45000,
    "remaining": 135000,
    "critical_reserve": 20000,
    "compression_triggered": false
  }
}
```

### 8.3 Context Budget Management

```
Context Budget = Total Window − Critical Reserve

Critical Reserve must cover:
  - Complete current atomic task
  - Write checkpoint snapshot
  - Produce coherence report
  - Issue resume prompt if needed

Thresholds:
  > 70% remaining  → normal operation
  30–70% remaining → COMPRESS: evict completed-phase details, keep task map
  < 30% remaining  → OFFLOAD: summarize all done phases into compact form
  < CRITICAL_RESERVE → HALT immediately → CHECKPOINT → emit resume prompt
```

**Resume prompt format (emitted on budget critical):**

```
CONTEXT BUDGET CRITICAL — CHECKPOINT SAVED

Snapshot: CTX-001-042
Plan: PLAN-001 | Phase: EXECUTION | Progress: 42/84
Current file: messages.html | Pass: PASS_1_CSS_TOKENS
Active guides: arch-containerization-6, spec-css-naming
Next task: T-001-043 (RENAME --msg-avatar-size → --messages-avatar-size, line 91)

To resume: load CTX-001-042, verify file state, continue from T-001-043.
```

### 8.4 Context Rehydration

When resuming after context loss (session boundary or overflow):

```
CONTEXT REHYDRATION PROTOCOL

1. Load checkpoint: CTX-001-042
2. Restore active guides:
   → arch-containerization-6 (ACTIVE) ✓
   → spec-css-naming (ACTIVE) ✓
3. Restore plan state:
   → PLAN-001, RUNNING, phase EXECUTION, task T-001-042 DONE
4. Restore file state:
   → messages.html: passes 1-2 complete, pass 3 starting
5. Restore lock table:
   → messages.html: EXCLUSIVE → PLAN-001
6. Verify: current file hash == checkpoint.file_hash
   → PASS ✓
7. Confirm:
   "Context rehydrated ✓ | Plan: PLAN-001 | Resuming: T-001-043 | Remaining: 42/84"
```

---

## Conflict Detection Matrix

### 9.1 Conflict Types

| Conflict | Detection Point | Resolution |
|----------|----------------|------------|
| `RESOURCE` | Lock acquisition | Serialize: lower-priority plan waits |
| `GUIDE_VERSION` | Guide loading | Supersede: higher version activates |
| `GUIDE_SEMANTIC` | Invariant extraction | Hierarchy: ARCH wins over SPEC |
| `SCOPE_OVERLAP` | Plan registration | Merge or serialize via conflict_group |
| `INVARIANT_VIOLATION` | Invariant pre-scan | Block operation, not the invariant |
| `TOKEN_AMBIGUITY` | Cross-plan analysis | Both plans must use same ARCH target |
| `TEMPORAL` | Dependency graph | Topological sort enforces order |

### 9.2 Conflict Matrix Template

Generated before first plan starts:

```
Conflict Matrix (generated: 2024-01-15T10:00:00Z)

          │ PLAN-001 │ PLAN-002 │ PLAN-003 │
──────────┼──────────┼──────────┼──────────┤
PLAN-001  │    —     │  SCOPE   │  none    │
PLAN-002  │  SCOPE   │    —     │ RESOURCE │
PLAN-003  │  none    │ RESOURCE │    —     │

SCOPE conflict (001 ↔ 002):
  shared file: messages.html
  resolution:  PLAN-001 processes first (higher priority)
               PLAN-002 → BLOCKED until PLAN-001 releases lock

RESOURCE conflict (002 ↔ 003):
  shared file: messages.css
  resolution:  serialize via topological order (002 before 003)

Status: all conflicts resolvable. No UNRESOLVABLE conflicts detected.
```

### 9.3 Cross-Plan Token Ambiguity Detection

```
Scenario:
  PLAN-001: renames  --msg-*  →  --messages-*   (in messages.html)
  PLAN-002: renames  --msg-*  →  --message-*    (in wallet.html)   ← DIFFERENT TARGET!

Detection: scan all plans for same source pattern, compare replacement targets
Conflict: TOKEN_AMBIGUITY on --msg-*
  PLAN-001 target: --messages-* (per arch-containerization-6 §7.1)
  PLAN-002 target: --message-*  (no guide reference)

Resolution:
  Check ARCH invariant INV-CSS-TOKENS → specifies --messages- (plural)
  PLAN-002 task map is WRONG → correct before execution
  PLAN-002.status remains PLANNED until corrected
```

---

## Validation Hierarchy

Four levels. A failure at any level blocks progression to the next.

```
Level 4 — SYSTEM   (global, cross-plan, all invariants)
    ↑
Level 3 — PLAN     (all files in plan, all phases complete)
    ↑
Level 2 — FILE     (all passes for one file, all dominos resolved)
    ↑
Level 1 — ATOMIC   (single operation post-conditions)
```

### Level 1 — Atomic Validation

Runs immediately after each ATOMIC task via AEP step ③.
Defined in task `post_conditions`. See §7.2.

### Level 2 — File Validation

Runs after all tasks for a file are DONE:

```
□ grep all violation patterns for this file → 0 results (excluding comments)
□ all task_ids scoped to this file → status DONE
□ file hash ≠ pre-execution hash (changes were actually made)
□ all domino dependencies for this file → resolved
□ no cross-file references left dangling (token defined here, consumers updated)
```

### Level 3 — Plan Validation

Runs after all files in plan are DONE:

```
□ progress.done == progress.total_tasks
□ progress.failed == 0
□ all ARCH invariants satisfied across all modified files
□ all cross-file dominos resolved (no open references)
□ lock table: all locks acquired by this plan released
□ all dependent plans notified (BLOCKED → READY)
```

### Level 4 — System Validation

Runs after all plans complete:

```
□ all PLAN_REG entries → status DONE
□ LOCK_TABLE fully empty (no orphaned locks)
□ GUIDE_REG: no ZOMBIE, CONFLICTING, or SUPERSEDED-but-still-used entries
□ all ARCH invariants → SATISFIED globally across all modified files
□ cross-plan consistency: no two plans wrote conflicting values for same pattern
□ checkpoint_store: no unverified or corrupted snapshots
□ context budget: no unrecovered overflows in any plan
```

**System validation report format:**

```
SYSTEM VALIDATION REPORT
════════════════════════════════════════════════════
Session:             sess-20240115-001
Timestamp:           2024-01-15T15:00:00Z

Plans completed:           3 / 3   ✅
Total tasks completed:   247 / 247  ✅
Failed tasks:              0        ✅
Invariants satisfied:      7 / 7   ✅
Orphaned locks:            0        ✅
Cross-plan conflicts:      0        ✅
Corrupt checkpoints:       0        ✅

FILES MODIFIED:
  messages.html    ✅   42 tasks | 0 violations remaining
  messages.css     ✅   18 tasks | 0 violations remaining
  wallet.html      ✅   31 tasks | 0 violations remaining
  wallet.css       ✅   22 tasks | 0 violations remaining
  checkout.html    ✅   58 tasks | 0 violations remaining
  checkout.js      ✅   76 tasks | 0 violations remaining

INVARIANT STATUS:
  INV-LAW0         ✅  SATISFIED  (0 getElementById in JS)
  INV-CSS-TOKENS   ✅  SATISFIED  (0 abbreviated custom properties)
  [...]

STATUS: ALL CLEAN ✅
════════════════════════════════════════════════════
```

---

## Full Multi-Plan Execution Workflow

### Phase 0D — Driver Initialization (before any base-methodology phase)

```
0D.1  Initialize GR with session_id
      → "Registry initialized ✓ | session: sess-20240115-001"

0D.2  Load ARCHITECTURAL guides
      → Parse, extract invariants, register in GUIDE_REG
      → "arch-containerization-6 loaded ✓ | 7 invariants"

0D.3  Load SPECIALIZED guides
      → Check against ARCH invariants for conflicts
      → "spec-css-naming loaded ✓ | no conflicts"

0D.4  Load OPERATIONAL guides
      → "ops-large-file loaded ✓"

0D.5  Register all plans
      → Parse PCD: scope, deps, conflict_group, guides
      → "PLAN-001 registered | scope: 2 files | conflict_group: ui-widgets"
      → "PLAN-002 registered | scope: 3 files | deps: [PLAN-001]"

0D.6  Build conflict matrix
      → "1 SCOPE conflict (001↔002), resolved by serialization | 0 guide conflicts"

0D.7  Topological sort → execution schedule
      → "Schedule: [PLAN-001] → [PLAN-002] → [PLAN-003]"

0D.8  Invariant pre-scan: all plans vs all ARCH invariants
      → "PLAN-001: 0 invariant violations in task map ✅"
      → "PLAN-002: 0 invariant violations in task map ✅"

0D.9  GATE: pre-execution coherence check
      → all guides loaded and conflict-free?       ✅
      → all plans registered with full PCDs?       ✅
      → all conflicts resolved or serialized?       ✅
      → all invariant pre-scans passed?             ✅
      → "GATE PASSED ✓ | System ready | Beginning PLAN-001"
```

### Phases 1D–5D — Per-Plan Execution (base methodology + Driver enrichment)

For each plan in scheduled order:

```
[Phase 1 — Analysis]
  Base: systematic file × category analysis
  Driver enrichment:
    + each finding becomes a TEN with guide_ref
    + dominos registered as DOMINOES_INTO edges in TEG
    + invariant_refs extracted per violation

[Phase 2 — Task Map]
  Base: JSON map with issue_ids and dependencies
  Driver enrichment:
    + add pre_conditions and post_conditions per task
    + insert CHECKPOINT nodes at file boundaries
    + insert GATE nodes at phase transitions
    + verify all dependency issue_ids exist in TASK_REG

[Phase 3 — Execution Plan]
  Base: interactive tracker with grouping
  Driver enrichment:
    + topological sort within plan
    + identify critical path (longest dependency chain)
    + mark checkpoint_after on all HIGH/CRITICAL tasks
    + reserve context budget for plan

[Phase 4 — Execution]
  Base: one file at a time, dominos together, layered passes
  Driver enrichment:
    + every ATOMIC task → full AEP (§7.1)
    + every COMPOSITE task → validate after all children DONE
    + at CHECKPOINT nodes → save CTX snapshot, verify hash
    + at GATE nodes → run system coherence check
    + on context budget < 30% → compress and offload

[Phase 5 — Validation]
  Base: automated pattern check + semantic review + final report
  Driver enrichment:
    + Level 1-4 validation hierarchy
    + cross-plan consistency check
    + invariant registry final pass
    + lock release verification
```

### Phase 6D — Post-Plan Coherence (after each plan completes)

```
6D.1  Release all locks held by this plan
6D.2  PLAN_REG: status → DONE | timestamp recorded
6D.3  Cross-plan coherence:
      - Files modified: still valid for subsequent plans?
      - Any downstream plans need re-analysis due to these changes?
6D.4  Unblock dependent plans: BLOCKED → READY
6D.5  GATE: global coherence check
      → "PLAN-001 complete | 84/84 DONE | all invariants satisfied"
      → "PLAN-002 unblocked → READY | locks available ✅"
```

---

## Anti-Patterns (Driver-Level)

### ❌ Unregistered Guides Applied Silently

```
Bad:  LLM receives a new spec inline and starts applying it
Good: Receive spec → register in GUIDE_REG → extract invariants
      → conflict scan → notify plans → then apply
```

Reason: unregistered guides have no invariants in the system.
Violations become invisible — the coherence gate cannot catch them.

---

### ❌ Plan Without Conflict Group

```
Bad:  PLAN-001 has no conflict_group field
Good: Every plan has a conflict_group, even if solo:
        "conflict_group": "solo-plan-001"
```

Reason: without groups, the scheduler cannot detect scope conflicts
between the current plan and any future plan added mid-session.

---

### ❌ Atomic Without Post-Conditions

```
Bad:  { "status": "done" }
Good: { "post_conditions": [ { "type": "PATTERN_COUNT", "expected": 0 } ] }
```

Reason: "I did it" is an assertion, not a verification.
`grep returns 0` is a verification. Only verifications count.

---

### ❌ Cross-Plan Token Ambiguity

```
Bad:  PLAN-001: --msg-* → --messages-*
      PLAN-002: --msg-* → --message-*    ← different target!
Good: Check ARCH invariant for canonical target before writing task maps.
      Both plans must resolve to the same target from the same invariant.
```

Reason: two plans, same source, different targets = codebase splits after execution.

---

### ❌ Context Overflow Without Checkpoint

```
Bad:  Process 10 files, context fills, LLM loses state of files 3-7 silently
Good: Checkpoint at every file boundary.
      Monitor context budget. At < 30% → compress immediately.
```

Reason: a silent context loss is worse than a declared one — the LLM will
hallucinate continuation from partial state without knowing anything is wrong.

---

### ❌ Checkpoint Without Hash Verification

```
Bad:  Save snapshot → assume correct → continue
Good: Save snapshot → verify file_hash matches → then continue
```

Reason: a corrupt checkpoint gives false confidence. When rollback is needed,
the system restores to a broken state and cannot detect it.

---

### ❌ Lock Acquisition Outside PCD Declaration

```
Bad:  Plan starts modifying file X that was not in its declared scope
Good: All files must be in PCD.scope before plan.status → RUNNING.
      Undeclared lock acquisition → HALT immediately.
```

---

### ❌ Invariant Pre-Scan Skipped

```
Bad:  Build 84-task plan → execute → discover 12 invariant violations at the end
Good: Build task map → run invariant pre-scan → mark violating tasks as BLOCKED
      → fix task map → then execute
```

Reason: discovering invariant violations during execution means partial work
is done and partial rollback is required. Pre-scanning prevents execution entirely.

---

### ❌ New Guide Loaded Without Notifying Existing Plans

```
Bad:  Load arch-v6 (supersedes arch-v5) → continue executing PLAN-002 against v5
Good: Load arch-v6 → mark v5 SUPERSEDED → notify PLAN-002 → PLAN-002 re-runs
      invariant pre-scan → PLAN-002.status → ANALYZING (re-validate task map)
```

---

## Templates

### Template 1 — Plan Registration

```markdown
## Plan Registration: PLAN-[NNN]

**ID:**             PLAN-[NNN]
**Name:**           [descriptive name]
**Priority:**       [1–10, 1=highest]
**Conflict Group:** [group name]

**Guides:**
  - ARCHITECTURAL: [guide_ids]
  - SPECIALIZED:   [guide_ids]
  - OPERATIONAL:   [guide_ids]

**Scope:**
  - Files (modify):    [exhaustive list — all must be declared]
  - Files (read-only): [list]
  - Excluded:          [list]

**Dependencies:**
  - requires_after: [PLAN-IDs or empty]
  - blocks:         [PLAN-IDs or empty]

**Estimated Tasks:** [N]
**Checkpoint Freq:** every [N] atomic tasks

Pre-registration checks:
  □ all required guides in GUIDE_REG?
  □ scope files not exclusively locked by another plan?
  □ conflict_group assigned?
  □ invariant pre-scan ready to run?
```

### Template 2 — Guide Registration

```markdown
## Guide Registration: [guide_id]

**ID:**       [type]-[name]-[version]
**Type:**     ARCHITECTURAL | SPECIALIZED | OPERATIONAL
**Scope:**    GLOBAL | PLAN | TASK
**Version:**  [major.minor.patch]
**Path:**     [path to .md file]

**Supersedes:** [guide_ids or "none"]
**Conflicts With:** [guide_ids or "none"]
**Applies To:** [file patterns]

**Invariants (ARCHITECTURAL only):**
| ID | Description | Severity | Check Type | Pattern |
|----|-------------|----------|------------|---------|
| INV-XX | ... | CRITICAL | PATTERN_ABSENT | regex |

Post-load actions:
  □ conflict scan with all ACTIVE guides
  □ superseded guides marked SUPERSEDED
  □ affected plans notified
  □ invariant pre-scan re-run on affected plans
  □ confirmation output emitted
```

### Template 3 — Atomic Task with Self-Check

```markdown
## Task T-[PLAN_ID]-[NNN]

**Type:** ATOMIC
**Plan:** PLAN-[NNN]
**Guide Ref:** [guide_id].[invariant_id]
**order_index:** [N]

**Operation:**
  type:        RENAME | DELETE | REPLACE | ADD | MOVE
  target:      [exact string or pattern]
  replacement: [exact string or N/A]
  file:        [filename]
  lines:       [start–end]
  context:     "[verbatim code fragment ≤120 chars]"

**Pre-Conditions:**
  □ T-[NNN-1].status == DONE
  □ LOCK_TABLE['[file]'].holder == 'PLAN-[NNN]'
  □ grep "[target]" == [expected_count]

**Execute:**
[the operation description]

**Self-Check (Post-Conditions):**
  □ grep "[target]" in [file] == 0
  □ grep "[replacement]" in [file] >= 1
  □ INV-[XX]: SATISFIED
  □ [any cross-file checks]

**checkpoint_after:** true | false
**rollback_snapshot:** SNAP-[PLAN]-[NNN-1]

**Result:** DONE | FAILED | ROLLED_BACK
```

### Template 4 — System Status Report

```markdown
## System Status Report — [timestamp]

**Session:** sess-[ID]
**Context Budget:** [used] / [total] ([%] remaining | compressions: [N])

### Guides
| ID | Type | Version | Status | Invariants | Plans Using |
|----|------|---------|--------|------------|-------------|
| arch-v6 | ARCH | 6.0.0 | ACTIVE | 7 | PLAN-001, PLAN-002 |

### Plans
| Plan | Name | Status | Phase | Progress | Locks Held |
|------|------|--------|-------|----------|------------|
| PLAN-001 | Messages | RUNNING | EXECUTION | 42/84 | messages.html |
| PLAN-002 | Wallet | BLOCKED | READY | 0/31 | waiting: messages.html |

### Invariants
| ID | Description | Status |
|----|-------------|--------|
| INV-LAW0 | No getElementById | ✅ SATISFIED |
| INV-CSS-TOKENS | No abbreviated tokens | ⚠️ IN_PROGRESS |

### Conflicts
[none | list active unresolved conflicts]

### Upcoming Checkpoints
[T-001-044: VALIDATION pass-1 | T-001-045: FILE_BOUNDARY messages.html]

### Alerts
[none | list active alerts]
```

---

## Master Checklist

### Session Start

```
□ Global Registry initialized with unique session_id?
□ ARCHITECTURAL guides loaded before SPECIALIZED?
□ All invariants extracted and registered separately?
□ All plans registered with full PCDs (scope, deps, conflict_group)?
□ Conflict matrix built across all registered plans?
□ Topological sort completed — execution schedule determined?
□ Invariant pre-scan run on every plan's task map?
□ Context budget set with critical reserve?
□ Coherence GATE passed before any plan starts executing?
```

### New Guide Mid-Session

```
□ Guide type identified (ARCH / SPEC / OPS)?
□ Guide conflicts with all ACTIVE guides checked?
□ Superseded guides marked SUPERSEDED in GUIDE_REG?
□ All affected plans notified?
□ Invariant pre-scan re-run on affected plans?
□ Affected plans re-validated (task maps still correct against new invariants)?
□ Guide status → ACTIVE in GUIDE_REG?
```

### New Plan Mid-Session

```
□ PCD fully specified (scope, deps, conflict_group, guides)?
□ All required guides in GUIDE_REG?
□ Invariant pre-scan run before status → READY?
□ Conflict matrix updated to include new plan?
□ Resource locks declared in PCD?
□ Topological position determined?
□ Coherence GATE passed before this plan's execution?
```

### Each Atomic Task

```
□ Pre-conditions checked and all PASS?
□ Resource lock confirmed for this plan?
□ No CRITICAL invariant violated by this operation?
□ Operation executed?
□ Self-check (post-conditions) run immediately — not deferred?
□ All post-conditions PASS?
□ Checkpoint saved if checkpoint_after == true?
□ Plan progress counter incremented?
```

### Each File Completion

```
□ grep all violation patterns → 0 (excluding comments)?
□ All task_ids scoped to this file → DONE?
□ All domino dependencies resolved?
□ No dangling cross-file references?
□ File lock released in LOCK_TABLE?
□ FILE_BOUNDARY checkpoint saved and hash verified?
```

### Each Plan Completion

```
□ progress.done == progress.total_tasks?
□ progress.failed == 0?
□ All ARCH invariants satisfied across all modified files?
□ All locks released by this plan?
□ Dependent plans unblocked (BLOCKED → READY)?
□ Cross-plan coherence check passed?
□ PLAN_REG: status → DONE?
```

### Session End (all plans complete)

```
□ All PLAN_REG entries → DONE?
□ LOCK_TABLE fully empty?
□ GUIDE_REG: no ZOMBIE or still-active SUPERSEDED entries?
□ All ARCH invariants → SATISFIED globally?
□ Cross-plan consistency verified (no conflicting writes)?
□ No corrupted checkpoints in CHECKPOINT_STORE?
□ Final system validation report generated and clean?
```

---

## Metrics

### Per-Plan Metrics

```
Plan ID:             PLAN-001
Tasks:               84 total | 84 done | 0 failed | 0 skipped
Files:               2 modified | 2 clean | 0 failed
Checkpoints:         18 saved | 18 verified | 0 corrupted
Context Budget:      peak 32% | compressions: 0 | overflows: 0
Rollbacks:           0
Atomic throughput:   14 tasks/file (avg)
Invariant coverage:  7/7 tested and satisfied
Cross-file dominos:  6 resolved | 0 open
```

### Session Metrics

```
Session:             sess-20240115-001
Duration:            04:30:00
Plans:               3 completed | 0 failed | 0 aborted
Guides Loaded:       5 (ARCH: 1, SPEC: 2, OPS: 2)
Total Tasks:         247 done | 0 failed
Conflicts detected:  1 SCOPE (serialized) | 0 unresolved
Rollbacks:           0
Context Budget:      peak usage: 67% | compressions: 2 | overflows: 0
Checkpoints:         41 saved | 41 verified | 0 corrupted
```

---

## Relationship to Base Methodology

```
base methodology          driver layer
─────────────────         ──────────────────────────────────
Phase 0 (context load) →  Phase 0D (GR init + guide/plan registration)
Phase 1 (analysis)     →  Phase 1 + TEG node creation per finding
Phase 2 (task map)     →  Phase 2 + pre/post conditions + GATE/CHECKPOINT nodes
Phase 3 (plan)         →  Phase 3 + topological sort + critical path
Phase 4 (execution)    →  Phase 4 + AEP per atomic + context budget tracking
Phase 5 (validation)   →  Phase 5 + validation hierarchy levels 1–4
[new]                  →  Phase 6D: post-plan coherence + dependent plan unblocking
[new]                  →  Global: GUIDE_REG, LOCK_TABLE, CONFLICT_MATRIX, CHECKPOINT_STORE
```

The Driver adds zero ambiguity to the base methodology.
It adds structure, recoverability, and multi-plan safety.
Every concept in the Driver maps to a concept the base methodology already treats
as important — the Driver just formalizes it for the multi-plan, multi-guide case.

---

*Designed by analogy with: OS process schedulers (PCB, process states, mutex tables),
compiler infrastructure (symbol tables, AST nodes, dependency graphs, type checkers),
and database transaction journals (ACID atomicity, rollback logs, checkpoint protocols).
Applied to the problem of managing N concurrent AI-driven development plans
against an evolving set of architectural and specialized guides.*


ai-task-execution-methodology-context-matrix.md:
---------------------------------
# AI Task Execution Methodology — Context Matrix
## Three-Dimensional Atomic Dependency Structure for LLM-Driven Development

> **Role:** Structural complement to `ai-task-execution-methodology-driver.md`.  
> The Driver manages *process lifecycle*. The Context Matrix manages *spatial organization of work*.  
> The Driver answers "when does what run?" — the Matrix answers "where does everything live and how does it connect?"

---

## Philosophy: Geometry of Dependency

The base methodology organizes work as a flat list (file × category).
The Driver organizes it as a graph (Task Execution Graph, TEG).
The Context Matrix organizes it as a **three-dimensional space** where:

- Every task has a **precise geometric address** — not just an id, but a position in 3D
- Every dependency is a **vector** — a directed connection between two addresses
- Every conflict is a **geometric intersection** — two chains occupying the same cell
- The execution order is **derived from geometry** — not assigned, but read off the structure

The key insight:

> **A dependency graph is not drawn separately from the task list. It IS the task list — arranged in 3D space. The spatial position of a node encodes everything about its nature, authority, and relationships.**

The matrix makes three categories of dependency structurally distinct:
```
Vertical   (Z-axis) = "WHY does this task exist?"     ← justification chain
Horizontal (X-Y plane) = "WHAT ELSE at this level?"   ← domino chain
Diagonal   (cross-Z, cross-Y) = "WHAT BREAKS elsewhere?" ← coupling chain
```

A flat list cannot distinguish these. The 3D matrix makes them visible as different geometric paths.

---

## The Three Axes

### Z-Axis: Architectural Depth (Layer)
**Bottom = most fundamental. Top = most local.**

```
Z=0  INVARIANT   — the architectural laws themselves (INV-LAW0, INV-CSS-TOKENS...)
                   these are never "done" — they are always active constraints

Z=1  SYSTEM      — guide specifications that express invariants as rules
                   (arch-containerization-6 §7.1: "use full widget name in tokens")

Z=2  PLAN        — the plan's scope: which files, which guide set, what boundaries
                   one plan = one volume of the matrix

Z=3  FILE        — all changes scoped to one file
                   one file = one horizontal slice within a plan's volume

Z=4  PASS        — one category of changes within one file (CSS pass, HTML pass, JS pass)
                   one pass = one region within a file slice

Z=5  ATOMIC      — one specific, indivisible operation
                   one replacement, one deletion, one addition at exact line numbers
```

**Reading the Z-axis:**
- Lower Z = higher authority, wider scope, longer lifetime
- Higher Z = lower authority, narrower scope, shorter lifetime
- A node at Z=5 is "justified" only if there is a vertical chain reaching Z=0
- A task with no invariant at its root has no architectural basis

**Execution direction:**
- **Planning** flows bottom → top (invariants define plan scope define file tasks define atomics)
- **Validation** flows top → bottom (atomic checks verify file integrity verifies plan integrity verifies invariant)

---

### X-Axis: Change Class
**What type of transformation is happening?**

```
X=0  STRUCTURAL   — rename, reorganize, relocate (semantics preserved)
                    the thing keeps doing exactly what it did, under a new name/shape
                    example: --msg-bubble-radius → --messages-bubble-radius

X=1  BEHAVIORAL   — change logic, replace implementation (semantics change)
                    the thing does something different after this operation
                    example: document.getElementById → data-attribute lookup

X=2  ADDITIVE     — introduce something new
                    example: add AbortController signal to addEventListener

X=3  REDUCTIVE    — remove something (after all references resolved)
                    example: delete dead id="msg-old-avatar"

X=4  RELATIONAL   — change how elements relate: move, rewire, reorder
                    example: move component initialization from inline to module
```

**Execution order within a layer (Z=const):**
```
X=0 first  (structural: renames cannot break anything that was working)
X=1 after  (behavioral: depends on correct structural foundation)
X=2 after  (additive: new elements reference existing — need correct names)
X=3 last   (reductive: delete only after all references updated)
X=4 after X=0,1,2 (relational: rewiring assumes correct names and logic)
```

**The Class/Function distinction** (from "смена класса или изменения функции"):
- X=0 STRUCTURAL = *смена класса* — changing what a thing IS CALLED or HOW IT IS SHAPED
- X=1 BEHAVIORAL = *изменение функции* — changing what a thing DOES

These two dimensions of change have fundamentally different risk profiles:
- Structural changes are mechanical — they can be automated and verified by pattern matching
- Behavioral changes are semantic — they require understanding intent, not just pattern

The matrix enforces: **never mix structural and behavioral changes in the same pass.**

---

### Y-Axis: Domain
**What entity type is being changed?**

```
Y=0  TOKEN       — CSS custom properties (--widget-property-name)
Y=1  CLASS       — CSS class selectors (.widget-element-modifier)
Y=2  KEYFRAME    — CSS @keyframes animation names
Y=3  ATTRIBUTE   — HTML data-* attributes and values
Y=4  ID          — HTML id attributes
Y=5  VARIABLE    — JS variables, constants, parameters
Y=6  FUNCTION    — JS functions, methods, arrow functions
Y=7  EVENT       — JS event handler registrations
Y=8  IMPORT      — module import/export paths and names
```

**Domain ordering within X=0 STRUCTURAL:**
```
Y=0 TOKEN first    (CSS tokens are consumed by classes — rename source before consumer)
Y=1 CLASS after    (classes use tokens — rename after tokens are correct)
Y=2 KEYFRAME after (keyframes are referenced by classes — rename after classes)
Y=3 ATTRIBUTE      (HTML attributes are independent of CSS chain)
Y=4 ID last        (ids referenced by JS — update JS references first, then ids)
Y=5 → Y=6 → Y=7   (JS: variables before functions that use them, events last)
```

---

## Matrix Coordinate System

Every node in the matrix has a **precise address**: `M[Z, X, Y]`

```
M[5, 0, 0]  =  ATOMIC · STRUCTURAL · TOKEN
                ↑          ↑           ↑
              Layer    Change Class   Domain

M[0, 0, 0]  =  INVARIANT · STRUCTURAL · TOKEN
               → the law that governs token naming (INV-CSS-TOKENS)

M[3, 0, 1]  =  FILE · STRUCTURAL · CLASS
               → all CSS class renames in one specific file

M[5, 1, 6]  =  ATOMIC · BEHAVIORAL · FUNCTION
               → one specific JS function logic change
```

**Address Properties:**
- Addresses are not unique without context — `M[5,0,0]` exists in every file, every plan
- Full address includes: `plan_id` + `file` + `M[Z, X, Y]` + `sequence_index`
- Short notation `M[5,0,0]` is sufficient when file context is established

---

## 3D Matrix Visualization

### View 1 — Top-Down (X-Y Plane, single layer slice)
*Looking straight down the Z-axis. What's happening at Z=5 ATOMIC in messages.html:*

```
                    Y → Domain
          TOK   CLS   KFR   ATR   ID    VAR   FUNC  EVT
        ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  X=0   │●──●  │  ●   │  ●   │  ●   │      │  ●   │      │      │
  STRUCT│(14)  │(22)  │(3)   │(8)   │      │(4)   │      │      │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  X=1   │      │      │      │      │  ●   │      │  ●   │      │
  BEHAV │      │      │      │      │(1)   │      │(2)   │      │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  X=2   │      │      │      │      │      │      │      │  ●   │
  ADD   │      │      │      │      │      │      │      │(1)   │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  X=3   │      │  ●   │      │      │  ●   │      │      │      │
  REDUCT│      │(2)   │      │      │(3)   │      │      │      │
        └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
        Numbers = node count in this cell. ● = cell occupied.
        arrows show dominant chain direction within STRUCTURAL row
```

### View 2 — Side View (Z-Y Plane, X=STRUCTURAL slice)
*Looking along the X-axis. Depth of architectural stack per domain:*

```
Z ↑
  │
5 │ATOM   ●     ●     ●     ●           ●
  │       │     │     │     │           │
4 │PASS   ●─────●─────●     ●           ●
  │       │                 │           │
3 │FILE   ●─────────────────●           ●
  │       │                             │
2 │PLAN   ●─────────────────────────────●
  │       │                             │
1 │SYS    ●─────────────────────────────●
  │       │                             │
0 │INV    ●─────────────────────────────●
  │
  └────────────────────────────────────── Y →
         TOK   CLS   KFR   ATR   ID   VAR FUNC EVT

  Vertical columns = justification chains (each ● must connect downward to Z=0)
  Horizontal rows  = layer-level aggregation nodes
```

### View 3 — Front View (Z-X Plane, Y=TOKEN slice)
*Looking along the Y-axis. What types of changes exist per architectural layer for TOKEN domain:*

```
Z ↑
  │
5 │ATOM   ●                        (14 rename ops for specific tokens)
  │       │
4 │PASS   ●                        (1 pass-level token task per file)
  │       │
3 │FILE   ●                        (1 file-level token scope node)
  │       │
2 │PLAN   ●                        (plan-level: all token changes in scope)
  │       │
1 │SYS    ●                        (guide §7.1: token naming rule)
  │       │
0 │INV    ●                        (INV-CSS-TOKENS: the invariant)
  │
  └────────────────────────────────── X →
         STRUCT BEHAV  ADD  REDUCT RELAT

  For TOKEN domain: only X=0 (STRUCTURAL) is populated.
  Tokens don't have behavioral changes — they are named values.
  If X=1 appears in TOKEN domain → SUSPECT (tokens shouldn't change behavior)
```

### View 4 — Isometric (3D impression)
*The overall structure of a plan's matrix volume:*

```
                      ↑ Z (Architectural depth)
                   /    \
                 Z=5      ← Atomic operations (many nodes)
               /    \
            Z=4        ← Pass tasks
          /    \
        Z=3      ← File tasks
      /    \
    Z=2      ← Plan scope
  /    \
Z=1      ← System guide
  \    /
    Z=0   ← Invariants (foundation)
      \
       Y → (Domain: TOKEN, CLASS, KEYFRAME, ATTR, ID, VAR, FUNC, EVT)
       \
        X → (Change Class: STRUCT, BEHAV, ADD, REDUCT, RELAT)


          ┌──────────────────────────────────┐
         /│   Z=5 ATOMIC                    /│
        / │  ┌────────────────────────────┐/ │
       /  │  │ ● ─ ● ─ ● │ ● │   │ ● │  │  │
      /   │  │     ●     │   │ ● │   │  │  │
     /    │  └────────────────────────────┘  │
    /     │  Z=3 FILE                        │
   /      │  ┌────────────────────────────┐  │
  /       │  │ ●─────────── ●            │  │
 /        │  └────────────────────────────┘  │
└─────────┘  Z=0 INVARIANT                   │
│            ┌────────────────────────────┐  │
│            │ ●─────────────────────── ●│  │
│            └────────────────────────────┘  │
└────────────────────────────────────────────┘
```

---

## Node Structure

Each occupied cell contains a **Matrix Node** — the atomic unit of the matrix:

```json
{
  "address": { "Z": 5, "X": 0, "Y": 0 },
  "address_label": "ATOMIC · STRUCTURAL · TOKEN",

  "node_id": "MN-P001-F01-5-0-0-014",
  "plan_id": "PLAN-001",
  "file": "messages.html",
  "sequence": 14,

  "content": {
    "type": "RENAME",
    "target":      "--msg-bubble-radius",
    "replacement": "--messages-bubble-radius",
    "location": { "lines": { "start": 69, "end": 69 } },
    "context": "--msg-bubble-radius: 0.75rem;"
  },

  "chains": {
    "vertical": {
      "parent":      "MN-P001-F01-4-0-0-001",
      "grandparent": "MN-P001-F01-3-0-0-001",
      "root_inv":    "MN-GLOBAL-0-0-0-INV-CSS-TOKENS"
    },
    "horizontal": {
      "prev": "MN-P001-F01-5-0-0-013",
      "next": "MN-P001-F01-5-0-0-015"
    },
    "diagonal": [
      {
        "target_node": "MN-P001-F01-5-0-1-022",
        "target_label": "ATOMIC·STRUCTURAL·CLASS",
        "edge_type": "DOMINOES_INTO",
        "note": "class .msg-bubble uses this token value"
      }
    ]
  },

  "pre_conditions": [
    "MN-P001-F01-5-0-0-013.status == DONE",
    "LOCK_TABLE['messages.html'].holder == 'PLAN-001'"
  ],
  "post_conditions": [
    { "type": "PATTERN_COUNT", "pattern": "--msg-bubble-radius",   "file": "messages.html", "expected": 0 },
    { "type": "PATTERN_COUNT", "pattern": "--messages-bubble-radius", "file": "messages.html", "expected_min": 1 },
    { "type": "INVARIANT_CHECK", "invariant_id": "INV-CSS-TOKENS" }
  ],

  "status": "DONE",
  "atomic_check": { "pre": "PASSED", "post": "PASSED", "invariant": "PASSED" }
}
```

**Node fields by address component:**

| Z-Level | Required Fields |
|---------|----------------|
| Z=0 INVARIANT | `check` (pattern), `severity`, `scope`, `cannot_override_by` |
| Z=1 SYSTEM | `guide_ref` (§section), `applies_to_patterns` |
| Z=2 PLAN | `plan_id`, `scope` (file list), `conflict_group` |
| Z=3 FILE | `file`, all child node counts, pass list |
| Z=4 PASS | `pass_name`, `pass_order`, domain handled |
| Z=5 ATOMIC | `content`, `pre_conditions`, `post_conditions`, `location` |

---

## Chain Types

### Type 1 — Vertical Chain (Justification)
*Answers: "Why does this task exist?"*

Every Z=5 node must have an unbroken vertical chain reaching Z=0.
The chain is the proof that a task is architecturally grounded.

```
Vertical chain for MN-...-5-0-0-014:

Z=0  ● INV-CSS-TOKENS
     │  "no abbreviated custom properties"
     │
Z=1  ● arch-containerization-6 §7.1
     │  "all --custom-properties must use full widget name"
     │
Z=2  ● PLAN-001: scope includes messages.html tokens
     │
Z=3  ● messages.html: token pass required
     │
Z=4  ● Pass-1 CSS Tokens: 20 nodes in this pass
     │
Z=5  ● --msg-bubble-radius → --messages-bubble-radius (line 69)
```

**Rule:** if you cannot draw a vertical chain to Z=0 for a task, that task has no invariant basis.
Either find the invariant it serves, or do not do the task.

---

### Type 2 — Horizontal Chain (Domino)
*Answers: "What else at this level must change together?"*

Horizontal chains live in a single Z-layer. They represent the domino effect from the original methodology, now visible as a path in the X-Y plane.

```
Horizontal chain at Z=5 (ATOMIC), single file, following X=0 STRUCTURAL:

M[5,0,0] ──→ M[5,0,1] ──→ M[5,0,2] ──→ M[5,0,3] ──→ M[5,3,4]
 TOKEN          CLASS        KEYFRAME      ATTRIBUTE     ID-delete
 (rename        (rename      (rename       (rename       (remove
  --msg-*)       .msg-*)      msg-bubble)   data-msg)     dead ids)

Y increases left→right: source domain before consumer domain
X increases: STRUCTURAL before REDUCTIVE
```

**Rule:** a horizontal chain must be executed as one atomic batch within a pass.
You cannot execute M[5,0,0] and M[5,0,1] in different passes — they are chained.

**Horizontal chain discovery:**
```
For each domain Y in X-layer:
  Find all consumers of Y's output at the same Z-level
  Connect: Y-producer → Y-consumer as horizontal edge
  Order: by consumer dependency (which Y-domain reads which)
```

---

### Type 3 — Diagonal Chain (Coupling)
*Answers: "What breaks in a different domain AND a different layer?"*

Diagonal chains cross both Z and Y axes. These are the hardest dependencies to discover
from a flat task list. In the matrix, they are visible as diagonal vectors in 3D space.

```
Diagonal chain example:

M[5, 0, 0]   ATOMIC · STRUCTURAL · TOKEN (CSS file defines --messages-bubble-radius)
    │↘
    │  M[5, 0, 1]   ATOMIC · STRUCTURAL · CLASS (CSS consumer: .messages-bubble)
    │       ↘
    │         M[5, 0, 3]   ATOMIC · STRUCTURAL · ATTRIBUTE (HTML: data-variant attr)
    │               ↘
    │                 M[5, 1, 6]   ATOMIC · BEHAVIORAL · FUNCTION
    │                              (JS: reads data-variant and applies token value)

This chain crosses Y=0→1→3→6 AND stays at Z=5 (all atomic)
But if JS was at a different abstraction layer:

M[4, 0, 0]  (PASS-level: the whole CSS token pass)
    │↘
    │  M[5, 1, 6]  (ATOMIC-level: one specific JS function)

This crosses BOTH Z (4→5) AND X (0→1) AND Y (0→6) — a full diagonal
```

**Diagonal chain detection protocol:**
```
For each M[Z, X, Y] node:
  1. Find all nodes that CONSUME this node's output
  2. If consumer is at same [Z, X, Y+n] → horizontal edge
  3. If consumer is at [Z, X+n, Y] → X-diagonal (class change triggers behavioral change)
  4. If consumer is at [Z+n, X, Y] → Z-diagonal (file-level node triggers atomic node)
  5. If consumer crosses both → full diagonal
  Register all as `diagonal` chain edges in the node
```

---

## Population Protocol

From Phase 1 analysis → placing every finding into the matrix.

### Step 1 — Determine Address

For each violation found during analysis:

```
DETERMINE Z:
  Is this a rule/law?              → Z=0 (reference only, don't create — load from guide)
  Is this a guide specification?   → Z=1 (reference only, already in GUIDE_REG)
  Does this span multiple files?   → Z=2 (PLAN scope — usually auto-created)
  Is this file-scoped?             → Z=3 (FILE scope — one per file)
  Is this one pass in one file?    → Z=4 (PASS scope — one per pass per file)
  Is this one specific change?     → Z=5 (ATOMIC — create a new node)
  
  Default for found violations: Z=5

DETERMINE X:
  Name changes, no logic changes?  → X=0 (STRUCTURAL)
  Logic/behavior changes?          → X=1 (BEHAVIORAL)
  Adding new elements?             → X=2 (ADDITIVE)
  Removing elements?               → X=3 (REDUCTIVE)
  Moving/rewiring?                 → X=4 (RELATIONAL)

DETERMINE Y:
  CSS --custom-property?           → Y=0 (TOKEN)
  CSS .class-selector?             → Y=1 (CLASS)
  CSS @keyframes?                  → Y=2 (KEYFRAME)
  HTML data-* attribute?           → Y=3 (ATTRIBUTE)
  HTML id="" attribute?            → Y=4 (ID)
  JS variable/const?               → Y=5 (VARIABLE)
  JS function/method?              → Y=6 (FUNCTION)
  JS addEventListener?             → Y=7 (EVENT)
  Module import/export?            → Y=8 (IMPORT)
```

### Step 2 — Find Vertical Parent

```
For new node at M[Z, X, Y]:
  Scan for existing node at M[Z-1, X, Y]:
    - If found → set vertical.parent
    - If not found → create parent node at Z-1 (aggregate node)
  Repeat until Z=0 is reached (must exist — it's the invariant)
  
  If no Z=0 node can be found for [X, Y]:
    → FLAG: no invariant basis for this domain/class combination
    → Do not proceed until guide provides Z=0 anchor
```

### Step 3 — Find Horizontal Neighbors

```
For new node at M[Z, X, Y]:
  Scan nodes at M[Z, X, Y-1]: if found → set as horizontal.prev
  Scan nodes at M[Z, X, Y+1]: if found → set as horizontal.next
  Also scan: M[Z, X+1, Y] for cross-class chains (structural → behavioral)
  
  Order within horizontal chain:
    Sort by: Y ascending within same X
    Then by: X ascending (X=0 before X=1)
    Then by: replacement string length descending (longest first — prevents substring collision)
```

### Step 4 — Find Diagonal Dependencies

```
For new node at M[Z, X, Y]:
  Ask: "what CONSUMES the output of this operation?"
  For each consumer:
    Determine its address M[Z', X', Y']
    If Z' ≠ Z OR X' ≠ X OR Y' ≠ Y:
      → diagonal edge: source.diagonal.push({ target: M[Z',X',Y'], edge_type: DOMINOES_INTO })
      → target.pre_conditions.push(source.status == DONE)
  
  Common diagonal patterns:
    M[5,0,0] TOKEN rename → M[5,0,1] CLASS that uses this token   (Y-diagonal)
    M[5,0,1] CLASS rename → M[5,0,3] HTML attribute that uses class (Y-diagonal)
    M[5,0,3] ATTR rename  → M[5,1,6] JS function that reads attr   (X+Y diagonal)
    M[3,0,0] FILE-level   → M[5,0,0] ATOMIC nodes within           (Z-diagonal, parent)
```

### Step 5 — Validate Matrix Integrity

After all violations are placed:

```
Integrity checks:
  □ Every Z=5 node has a vertical chain reaching Z=0?
  □ No two nodes at the same address have contradictory content?
  □ All diagonal edges are registered in both source and target nodes?
  □ Horizontal chain ordering is consistent (no cycles at same Z-level)?
  □ All REDUCTIVE nodes (X=3) have empty diagonal.consumers lists?
       (cannot delete something still referenced)
  □ All BEHAVIORAL nodes (X=1) have their STRUCTURAL prerequisites at X=0 complete?
```

---

## Conflict Detection in Matrix Space

A conflict is a **geometric collision** — two chains occupying the same address
with incompatible content, or two chains that intersect at a shared node
with incompatible ordering.

### Conflict Type 1 — Cell Collision (same address, different content)

```
M[5, 0, 0] (messages.html):
  PLAN-001 places: --msg-bubble-radius → --messages-bubble-radius
  PLAN-002 places: --msg-bubble-radius → --message-bubble-radius   ← COLLISION

Geometry: two nodes fighting for the same cell M[5,0,0] in the same file.
Detection: when populating, check if cell already occupied → if content differs → CONFLICT
Resolution: check Z=0 invariant. Which replacement does INV-CSS-TOKENS mandate?
            Both plans must resolve to the same value. Incorrect plan → rework task map.
```

### Conflict Type 2 — Chain Crossing (shared intermediate node, incompatible ordering)

```
Chain A: M[5,0,0] → M[5,0,1] → M[5,0,3]
Chain B:              M[5,0,1] → M[5,1,5]

Both chains pass through M[5,0,1]. Chain B assumes [5,0,1] is done (STRUCTURAL·CLASS).
Chain A also needs [5,0,1] done before [5,0,3].

If these chains belong to different plans:
  → RESOURCE CONFLICT: M[5,0,1] is a shared node
  → Resolution: execute chain A and chain B sequentially, not in parallel
  
If same plan, different passes:
  → TEMPORAL CONFLICT: ordering must be explicit
  → Resolution: merge into single pass, A first, B after
```

### Conflict Type 3 — Vertical Contradiction (two Z=0 invariants contradict at same [X,Y])

```
INV-CSS-TOKENS: no abbreviated custom properties (Z=0, X=0, Y=0)
INV-COMPAT-LEGACY: preserve --msg- prefix for backward compatibility (Z=0, X=0, Y=0)

Both are at M[0, 0, 0] → INVARIANT CONFLICT
Cannot have two Z=0 nodes with contradictory rules at same [X, Y]

Resolution (in priority order):
  1. ARCHITECTURAL guide wins over SPECIALIZED guide (guide type hierarchy)
  2. Higher version wins (guide supersession)
  3. If same type and version → human resolution required, BLOCK all plans
  
This conflict must be resolved before any Z=5 nodes are created at [X=0, Y=0]
```

### Conflict Matrix as Geometric Intersection Map

```
Cross-plan conflict map (address space, Z=5 layer, X=0, messages.html):

          Y=0 TOK   Y=1 CLS   Y=2 KFR   Y=3 ATR   Y=4 ID
PLAN-001  ████████   ████████   ████       ████████   ████
PLAN-002             ████████              ████████   ████

Overlap at Y=1 CLASS and Y=3 ATTR and Y=4 ID:
  → PLAN-001 and PLAN-002 share cells [5,0,1], [5,0,3], [5,3,4] in messages.html
  → These cells are SCOPE conflicts → serialize (PLAN-001 first, then PLAN-002)
```

---

## Execution Order from Matrix Geometry

The matrix makes execution order unambiguous — it is **read off the structure**, not assigned.

### Global Order (across Z-layers)

```
1. Z=0 always active (invariants — never executed, always enforced)
2. Z=1 load (guides — Phase 0D of Driver)
3. Z=2 plan (populate plan scope nodes — Phase 2-3 of base methodology)
4. Z=3 analyze file by file (Phase 1 of base methodology)
5. Z=4 define passes per file (Phase 3 plan)
6. Z=5 execute atomics (Phase 4 execution)
7. Z=3 → Z=0 validate upward (Phase 5 validation)
```

### Within Z=5 ATOMIC Layer

```
For each file (determined by plan dependency order):
  For each X in [0, 1, 2, 3, 4] (ascending — STRUCTURAL before BEHAVIORAL before REDUCTIVE):
    For each Y in domain-dependency order [0→1→2, 3, 4, 5→6→7→8]:
      Execute horizontal chain at M[5, X, Y]:
        Sort chain members by replacement string length (LONGEST FIRST)
        Execute each member via AEP (Atomic Execution Protocol)
        After each member: self-check (post_conditions)
        After chain complete: check diagonal consumers' pre_conditions
      Move to next Y
    Move to next X
  Move to next file
```

### Critical Path via Matrix

The critical path is the longest chain from any Z=5 node back to Z=0, plus its horizontal chain length:

```
Critical path = max(vertical_depth + horizontal_length + diagonal_length)

Example:
  M[5,0,0] vertical: 5 hops to Z=0
  M[5,0,0] horizontal: 8 nodes in chain
  M[5,0,0] diagonal: leads to M[5,1,6] which has 3 more nodes
  
  Total path: 5 + 8 + 3 = 16
  
  If another chain has length 22 → that chain is the critical path
  Start with critical path nodes when scheduling execution
```

---

## Atomic Self-Check via Matrix Context

When the AEP runs for a Z=5 node, the self-check has full matrix context:

```
ATOMIC SELF-CHECK for M[5, 0, 0] (--msg-bubble-radius → --messages-bubble-radius):

① Vertical check (upward):
  ├── M[4,0,0] parent pass: still internally consistent? ✅
  ├── M[3,0,0] file scope: progress counter incremented? ✅
  └── M[0,0,0] INV-CSS-TOKENS: still satisfied after this op? ✅

② Horizontal check (sideways):
  ├── M[5,0,0] self post_conditions: PATTERN_COUNT == 0? ✅
  └── M[5,0,1] next node: pre_conditions now satisfied? ✅

③ Diagonal check (across domains):
  └── M[5,0,1] CLASS consumer: aware this token was renamed? 
      (diagonal edge: must be in same pass — pre_condition registered) ✅

④ Cell-level check:
  └── No other plan claims this cell with different content? ✅

⑤ Layer coherence (at GATE intervals):
  └── All Z=5 nodes completed so far: none contradict each other? ✅

RESULT: PASSED — commit checkpoint, update M[5,0,0].status → DONE
```

This is richer than a flat post-condition check: it validates in five geometric directions simultaneously.

---

## Layer Snapshot (Matrix Checkpoint)

A checkpoint in matrix terms is a **layer snapshot** — a serialized state of all nodes at one Z-level:

```json
{
  "snapshot_id": "MSNAP-P001-F01-Z5-014",
  "plan_id": "PLAN-001",
  "file": "messages.html",
  "layer": 5,
  "timestamp": "ISO8601",

  "layer_state": {
    "total_nodes": 74,
    "done": 38,
    "in_progress": 1,
    "pending": 35,
    "failed": 0
  },

  "cell_states": {
    "5-0-0": { "done": 14, "total": 20 },
    "5-0-1": { "done": 22, "total": 22 },
    "5-0-2": { "done": 2,  "total": 3  },
    "5-0-3": { "done": 0,  "total": 8  },
    "5-3-4": { "done": 0,  "total": 3  }
  },

  "active_chains": {
    "horizontal": "M[5,0,0] → 014/020 position",
    "next_diagonal": "M[5,0,1] chain starts when M[5,0,0] chain completes"
  },

  "last_completed_node": "MN-P001-F01-5-0-0-014",
  "next_node": "MN-P001-F01-5-0-0-015",
  "file_hash": "sha256:abc123..."
}
```

**Layer snapshot triggers:**
- After completing every cell (`M[Z, X, Y]` fully done)
- At X-boundary (moving from X=0 to X=1)
- At file boundary (moving to next file)
- On context budget pressure

---

## Matrix Status Report

The matrix enables precise, geometric progress reporting:

```
CONTEXT MATRIX STATUS
══════════════════════════════════════════════════════════════════
Plan:    PLAN-001
File:    messages.html
Layer:   Z=5 (ATOMIC)
═══════════╤══════════════════════════════════════════════════════
           │             Y → Domain
     X     │ TOK    CLS    KFR    ATR    ID     VAR    FUNC   EVT
═══════════╪════════════════════════════════════════════════════════
 STRUCT 0  │14/20  22/22   2/3   0/8    —      4/4     —      —
 BEHAV  1  │  —      —     —      —    0/1     —      0/2     —
 ADD    2  │  —      —     —      —     —       —      —      0/1
 REDUCT 3  │  —     0/2    —      —    0/3     —       —      —
═══════════╧════════════════════════════════════════════════════════

Progress bars:
  M[5,0,0] TOKEN:     ██████████████░░░░░░   14/20   70%
  M[5,0,1] CLASS:     ████████████████████   22/22  100% ✅
  M[5,0,2] KEYFRAME:  █████████████░░░░░░░    2/3    67%
  M[5,0,3] ATTR:      ░░░░░░░░░░░░░░░░░░░░    0/8    0%  BLOCKED (waiting M[5,0,0])
  M[5,3,4] ID-DELETE: ░░░░░░░░░░░░░░░░░░░░    0/3    0%  BLOCKED (waiting M[5,0,1])
  M[5,1,4] ID-BEHAV:  ░░░░░░░░░░░░░░░░░░░░    0/1    0%  BLOCKED (waiting M[5,0,4])

Critical path: M[5,0,0]─→M[5,0,1]─→M[5,0,3]─→M[5,1,6]   length=4
Bottleneck: M[5,0,0] TOKEN chain (6 remaining)
Next checkpoint: after M[5,0,0] chain completes

Vertical integrity:
  All Z=5 nodes → Z=0: ✅ (all have invariant anchors)
Diagonal coverage:
  All consumer nodes have registered pre_conditions: ✅
Cross-cell conflicts: 0 ✅
══════════════════════════════════════════════════════════════════
```

---

## Integration with the Driver

The Context Matrix replaces and enriches the Driver's Task Execution Graph (TEG):

```
Driver concept          Matrix equivalent
──────────────────────  ─────────────────────────────────────────────
TEN (Task Node)     →   Matrix Node M[Z, X, Y]
TEG dependency edge →   Chain vector (vertical / horizontal / diagonal)
GATE node           →   Z-layer boundary check (all nodes at Z-level checked)
CHECKPOINT node     →   Layer snapshot (full Z-level serialized)
conflict_matrix     →   Geometric intersection scan (cell collisions + chain crossings)
TEG topological sort→   Matrix traversal order (Z ascending, X ascending, Y by domain order)
Validation Level 1  →   Z=5 post_conditions (atomic)
Validation Level 2  →   Z=3 aggregate check (file)
Validation Level 3  →   Z=2 aggregate check (plan)
Validation Level 4  →   Z=0 invariant check (system)
```

**Context Budget ↔ Matrix layers:**

```
The LLM's context window corresponds to how many Z-layers it can hold:

Full context (100%): all Z-layers active simultaneously
                     Z=0 invariants + Z=1 guides + Z=2-5 working set

Compressed (70%):    Z=0, Z=1 always retained (small, fundamental)
                     Z=2, Z=3 compressed to summaries
                     Z=4, Z=5 active (currently executing)

Minimal (30%):       Z=0 invariants only (compressed invariant list)
                     Z=5 current cell only (one M[Z,X,Y] node at a time)
                     Context rehydration required for any other layer
```

---

## Anti-Patterns

### ❌ Ungrounded Node (no vertical chain to Z=0)

```
Bad:  M[5, 0, 1] created (rename CSS class) with no Z=0 anchor
Good: Trace upward before creating:
      M[5,0,1] ← M[4,0,1] ← M[3,0,1] ← M[2,0,1] ← M[1,0,1] ← M[0,0,1: INV-CSS-CLASSES]
      If M[0,0,1] does not exist → the rename has no invariant basis → do not create
```

---

### ❌ Executing X=3 (REDUCTIVE) Before X=0 (STRUCTURAL) Completes

```
Bad:  Delete dead id at M[5,3,4] while M[5,0,1] class chain is still in progress
      (the class chain might reference this id as an ARIA attribute)
Good: X ascending order within each Z-layer. X=3 nodes' pre_conditions must
      include all M[5,0,*], M[5,1,*], M[5,2,*] at same file → DONE
```

---

### ❌ Diagonal Dependency Not Registered (Silent Coupling)

```
Bad:  Rename token at M[5,0,0], JS function at M[5,1,6] reads it via getPropertyValue()
      M[5,0,0] has no diagonal edge to M[5,1,6]
      Execution completes M[5,0,0], then executes M[5,1,6] in a different pass
      — too late, M[5,1,6] was never flagged for update
Good: During population (Step 4), scan all JS files for getPropertyValue(--msg-bubble-radius)
      Register diagonal: M[5,0,0] → M[5,1,6] (DOMINOES_INTO)
      M[5,1,6] gets added to the current plan's scope
```

---

### ❌ Cell Collision Discovered During Execution

```
Bad:  PLAN-001 and PLAN-002 both write to M[5,0,0] with different replacements
      Discovered when PLAN-002 tries to execute an already-done cell with wrong content
Good: Conflict scan before any execution begins (Driver Phase 0D.6)
      Matrix population checks cell occupancy before placing any node
      → Collision detected at population time, resolved before execution
```

---

### ❌ Horizontal Chain Without Length-Ordering

```
Bad:  Process .msg-msg before .msg-msg--sent
      .msg-msg replacement will corrupt .msg-msg--sent occurrences
Good: Within any horizontal chain at same [Z, X, Y]:
      Sort by replacement string length DESCENDING before executing
      .msg-msg--sent (longer) → .msg-msg--recv (longer) → .msg-msg (shorter)
      This rule lives in the matrix structure: the horizontal chain has explicit ordering
```

---

### ❌ Layer Skip (Z+1 nodes executed before Z-1 nodes are mapped)

```
Bad:  Start executing Z=5 atomics for a file before Z=4 pass structure is mapped
      → some atomics will be missed (they weren't known yet)
Good: Each Z-layer must be fully populated before the Z+1 layer executes.
      Population is bottom-up (Z=2→3→4→5).
      Execution is at Z=5, but population (mapping) of all Z-levels is prerequisite.
```

---

### ❌ Behavioral Change (X=1) Mixed Into Structural Pass (X=0)

```
Bad:  Pass-1 CSS: rename tokens AND change an animation timing function
      (timing function is behavioral — it changes what the animation does)
Good: Pass-1 CSS: only X=0 STRUCTURAL changes (renames)
      Behavioral changes scheduled for their own pass, after all structural renames confirmed
      The matrix enforces this: X=0 and X=1 cells are in different regions of the X-Y plane
```

---

## Templates

### Template 1 — Matrix Node (Atomic)

```markdown
## Matrix Node MN-[PLAN]-[FILE]-[Z]-[X]-[Y]-[NNN]

**Address:**   M[[Z], [X], [Y]]
**Label:**     [LAYER] · [CHANGE_CLASS] · [DOMAIN]
**Plan:**      PLAN-[NNN]
**File:**      [filename]

**Content:**
  operation:   RENAME | DELETE | REPLACE | ADD | MOVE
  target:      "[exact string]"
  replacement: "[exact string or N/A]"
  lines:       [start]–[end]
  context:     "[verbatim code fragment ≤120 chars]"

**Chains:**
  vertical.parent:  MN-...-[Z-1]-[X]-[Y]-[NNN]
  vertical.root:    MN-GLOBAL-0-[X]-[Y]-[INV-ID]
  horizontal.prev:  MN-...-[Z]-[X]-[Y-1]-[NNN] or null
  horizontal.next:  MN-...-[Z]-[X]-[Y+1]-[NNN] or null
  diagonal:
    - target: MN-...-[Z']-[X']-[Y']-[NNN] | edge: DOMINOES_INTO

**Pre-Conditions:**
  □ [prev_node].status == DONE
  □ LOCK_TABLE['[file]'].holder == '[plan_id]'
  □ grep "[target]" in [file] == [N]

**Post-Conditions:**
  □ grep "[target]" in [file] == 0
  □ grep "[replacement]" in [file] >= 1
  □ INV-[ID]: SATISFIED

**Status:** PENDING | IN_PROGRESS | DONE | FAILED | ROLLED_BACK
```

### Template 2 — Layer Status Snapshot

```markdown
## Layer Snapshot MSNAP-[PLAN]-[FILE]-Z[N]-[SEQ]

**Plan:** PLAN-[NNN]    **File:** [filename]    **Layer:** Z=[N]
**Timestamp:** [ISO8601]

**Cell Progress:**
| Cell M[Z,X,Y] | Label | Done | Total | Status |
|---------------|-------|------|-------|--------|
| [5,0,0] | ATOMIC·STRUCT·TOKEN | N | N | IN_PROGRESS |
| [5,0,1] | ATOMIC·STRUCT·CLASS | N | N | DONE ✅ |

**Active Chain:** M[[Z],[X],[Y]] → position [N]/[total]
**Blocked Cells:** [list M[Z,X,Y] and why]
**Critical Path:** M[...] → M[...] → M[...] (length=[N])
**File Hash:** sha256:[hash]
**Context Budget:** [used]/[total] ([%])
```

### Template 3 — Conflict Report

```markdown
## Conflict Report

**Type:** CELL_COLLISION | CHAIN_CROSSING | VERTICAL_CONTRADICTION
**Detected at:** Phase [0D population | 1 analysis | 4 execution]

**Address:** M[[Z], [X], [Y]] in [file]

**Parties:**
  Node A: [plan_id] → [content.replacement]
  Node B: [plan_id] → [content.replacement]

**Geometry:**
  [describe which chains intersect and how]

**Invariant Reference:**
  M[0, [X], [Y]]: [invariant description]

**Resolution:**
  □ Canonical value from Z=0 invariant: [value]
  □ Non-conforming party: [plan_id]
  □ Action: rework [plan_id] task map at M[[Z],[X],[Y]]
  □ Block [plan_id] execution until corrected
```

---

## Master Checklist (Matrix-Specific)

### Population Phase

```
□ Every violation assigned an M[Z, X, Y] address?
□ Every Z=5 node has a vertical chain to Z=0?
□ All diagonal dependencies discovered and registered?
□ Horizontal chains sorted by domain dependency order?
□ Horizontal chains sorted by replacement string length (descending)?
□ No cell collision between plans at any shared file?
□ X=3 REDUCTIVE nodes have empty diagonal.consumers lists?
□ All X=1 BEHAVIORAL nodes have X=0 STRUCTURAL prerequisites registered?
□ Matrix integrity checks all passed?
```

### Execution Phase

```
□ Executing in Z-ascending order (planning at Z=3,4, executing at Z=5)?
□ Within Z=5: executing in X-ascending order (STRUCTURAL before BEHAVIORAL)?
□ Within each X: executing in domain-dependency Y order?
□ Within each chain: longest replacement string first?
□ After each cell M[Z,X,Y] completes: diagonal consumers' pre_conditions checked?
□ Layer snapshot saved at each cell and X-boundary completion?
□ Vertical check (upward to Z=0) performed at each GATE?
```

### Validation Phase

```
□ Z=5 post_conditions: all nodes DONE? (Validation Level 1)
□ Z=3 file aggregate: grep all patterns → 0 per file? (Validation Level 2)
□ Z=2 plan aggregate: all file-level nodes DONE? (Validation Level 3)
□ Z=0 invariants: all satisfied globally? (Validation Level 4)
□ No cell collisions remain unresolved?
□ All diagonal chains fully executed (no open consumers)?
□ All layer snapshots verified (hash matches)?
```

---

## Metrics

### Matrix Density Metrics

```
Populated cells:     47 / 360 possible (13% density — sparse is normal)
Deepest chain:       vertical depth 5 + horizontal 14 + diagonal 3 = 22 hops
Critical path:       22 hops (M[0,0,0] → ... → M[5,0,0] chain → M[5,1,6])
Conflict density:    1 cell collision / 47 cells = 2% (resolved before execution)
Diagonal ratio:      8 diagonal edges / 47 nodes = 17% (cross-domain coupling)
```

### Execution Quality Indicators

```
Self-check pass rate:    100% (no node proceeded without post_condition pass)
Rollback count:          0
Layer skip violations:   0 (Z-order respected throughout)
X-order violations:      0 (STRUCTURAL before BEHAVIORAL throughout)
Ungrounded nodes:        0 (all Z=5 nodes have Z=0 anchor)
Unregistered diagonals:  0 (diagonal scan at population found all consumers)
```

---

## Relationship Map

```
ai-task-execution-methodology.md
    └── defines:  ANALYSIS → PLAN → EXECUTION (single plan, flat structure)
    
ai-task-execution-methodology-driver.md
    └── extends:  N plans, M guides, process lifecycle, atomic execution protocol
    └── manages:  GUIDE_REG, PLAN_REG, TASK_REG, LOCK_TABLE, CHECKPOINT_STORE
    
ai-task-execution-methodology-context-matrix.md  ← THIS DOCUMENT
    └── organizes: all tasks in 3D space M[Z, X, Y]
    └── replaces:  TEG (flat graph) with geometric address space
    └── enables:   geometric conflict detection, spatial execution order, layer snapshots
    └── maps to:   Driver's validation hierarchy (Z=5→Z=0 = Level 1→4)
    └── informs:   context budget management (Z-layers ↔ context window regions)
```

---

## Multi-Plan Matrix Volumes

When N plans operate in the same session, each plan occupies its own **matrix volume** —
a bounded sub-space of the global matrix. Volumes can be disjoint (no shared files),
adjacent (shared files, no conflicting cells), or overlapping (shared cells — a conflict state).

### Volume Geometry

```
Global Matrix Address Space
═══════════════════════════════════════════════════════════════════════
    Z ↑
      │
    5 │  [PLAN-001 volume]          [PLAN-002 volume]
    4 │   ┌──────────────┐           ┌──────────────┐
    3 │   │  msgs.html   │           │  wallet.html │
    2 │   │  msgs.css    │           │  wallet.css  │
    1 │   └──────────────┘           └──────────────┘
      │        ↕ shared Z=0,Z=1 layer (invariants + guides — global, one instance)
    0 │  ●───────────────────────────────────────────●  INV-CSS-TOKENS (scope: GLOBAL)
      │
      └────────────────────────────────────────────── Y,X plane
```

**Volume properties:**

```json
{
  "volume_id": "VOL-P001",
  "plan_id": "PLAN-001",
  "file_set": ["messages.html", "messages.css"],
  "z_range": [2, 5],
  "shared_layers": [0, 1],
  "address_prefix": "MN-P001-",
  "boundary_cells": {
    "messages.html.Z3": "MN-P001-messages.html-3-0-0-root",
    "messages.css.Z3":  "MN-P001-messages.css-3-0-0-root"
  },
  "overlap_with": {
    "VOL-P002": {
      "type": "DISJOINT",
      "shared_files": [],
      "shared_cells": []
    }
  }
}
```

---

### Volume Overlap Classification

```
DISJOINT:
  file_set(P001) ∩ file_set(P002) = ∅
  → completely independent volumes
  → can run in parallel without any coordination

ADJACENT:
  file_set(P001) ∩ file_set(P002) ≠ ∅
  occupied_cells(P001) ∩ occupied_cells(P002) = ∅
  → same files touched, but no cell collision
  → still must serialize (lock contention) — the file is shared
  → execution: sequential via LOCK_TABLE

OVERLAPPING (CONFLICT STATE):
  occupied_cells(P001) ∩ occupied_cells(P002) ≠ ∅
  → two plans write the same M[Z,X,Y] with different content
  → MUST be resolved before any execution begins
  → resolution: canonical value from Z=0 invariant, or plan rework

NESTED (rare, valid):
  file_set(P002) ⊂ file_set(P001)
  → P002 is a sub-operation of P001's domain
  → P001 waits for P002 at GATE before processing P002's files
```

---

### Shared Layer Protocol (Z=0 and Z=1)

Z=0 (invariants) and Z=1 (guide specs) are **global** — they belong to no single volume
but are readable by all. Write access to shared layers follows strict rules:

```
Z=0 INVARIANT layer:
  Write: only via guide loading (Driver Phase 0D.2)
  Read:  any plan, any time
  Mutate: NEVER during execution — only between plans (at Driver Phase 6D)
  Conflict: two Z=0 nodes at same [X,Y] with contradictory rules → SYSTEM HALT

Z=1 SYSTEM layer:
  Write: only during guide registration (Driver Phase 0D)
  Read:  any plan, any time
  Update: when guide is superseded → Z=1 node updated, all volumes notified
  Cascade: if Z=1 changes → all Z=2+ nodes in affected volumes re-validate
           (vertical chains now point to new Z=1 content)
```

**Z=1 update cascade protocol:**

```
arch-containerization-5 superseded by arch-containerization-6
    │
    ▼
Z=1 node M[1,0,0] updated: content → arch-containerization-6 §7.1
    │
    ▼
All volumes with vertical chains through M[1,0,0]:
    → VOL-P001: cascade to Z=2,3,4,5 nodes at [0,0] and [0,1]
    → VOL-P002: cascade to Z=2,3,4,5 nodes at [0,0]
    │
    ▼
For each affected Z=5 node:
    → re-derive post_condition patterns from new guide §
    → if new post_condition contradicts existing content → ROLLBACK + REWORK
    → if new post_condition consistent with existing content → PASS (no action)
    │
    ▼
Cascade report:
  "Z=1 updated: arch-v6 | cascaded to 74 Z=5 nodes in VOL-P001, 31 in VOL-P002
   Post-condition rederivation: 105 nodes | rework required: 0 | PASS: 105"
```

---

## Cross-File Chain Stitching

A diagonal chain is **cross-file** when the source node and target node live in different files.
This is the hardest coupling to detect and the most common source of post-execution regressions.

### Cross-File Chain Types

```
Type A — Definition → Usage:
  messages.css  M[5,0,0] defines --messages-bubble-radius
  messages.html M[5,0,1] uses   var(--messages-bubble-radius) in style attr
  → M[messages.css, 5,0,0] ──DOMINOES_INTO──▶ M[messages.html, 5,0,1]

Type B — Component → Consumer:
  tokens.css      M[5,0,0] defines --messages-bubble-radius (shared token file)
  messages.html   M[5,0,3] reads  it via getPropertyValue('--messages-bubble-radius')
  wallet.html     M[5,0,3] reads  it via same JS utility
  → One Z=5 source → N targets in N different files

Type C — Event → Handler:
  messages.html  M[5,0,3] defines  data-action="msg-submit"
  messages.js    M[5,1,7] listens  data-action === 'msg-submit'  ← behavioral coupling
  → DOM attr rename (structural) requires JS event handler update (behavioral)
  → Crosses X-axis: X=0 → X=1 (structural → behavioral)
  → Crosses file boundary: .html → .js

Type D — Module → Importer:
  messages.js    M[5,2,8] exports  class MessagesWidget (was MsgWidget)
  app.js         M[5,0,8] imports  { MessagesWidget } (was { MsgWidget })
  router.js      M[5,0,8] imports  MessagesWidget
  → One rename fans out to all importers across N files
```

### Cross-File Chain Registration

```json
{
  "chain_id": "XFC-P001-001",
  "type": "CROSS_FILE",
  "subtype": "DEFINITION_USAGE",
  "source": {
    "node_id": "MN-P001-messages.css-5-0-0-001",
    "file": "messages.css",
    "address": "M[5,0,0]",
    "content": "--messages-bubble-radius defined"
  },
  "targets": [
    {
      "node_id": "MN-P001-messages.html-5-0-1-014",
      "file": "messages.html",
      "address": "M[5,0,1]",
      "content": "var(--messages-bubble-radius) in inline style",
      "edge_type": "DOMINOES_INTO",
      "pre_condition": "MN-P001-messages.css-5-0-0-001.status == DONE"
    }
  ],
  "execution_constraint": "source file must complete before target file starts",
  "lock_order": ["messages.css", "messages.html"]
}
```

### Cross-File Scan Protocol

Run during Phase 1 (analysis), after all files are inventoried but before task maps are built:

```
CROSS-FILE SCAN PROTOCOL

For each pattern P found in file A:
  1. Classify P: is it a definition or a usage?
     definition: CSS custom property, CSS class, @keyframes name,
                 exported function, exported class, id attribute
     usage:      var(--P), .class-P, animation-name: P, import { P },
                 getElementById/querySelector matching P, data-* === P

  2. If P is a definition:
     Search all OTHER files in scope for usages of P
     For each usage found in file B:
       Register cross-file chain: A.M[5,0,Y] → B.M[5,?,Y']
       Determine edge type (structural or behavioral coupling)
       Add B's Z=5 node to the plan's scope if not already present

  3. If P is a usage:
     Search all OTHER files for P's definition
     If definition not in scope:
       → FLAG: definition file missing from plan scope
       → Option A: add definition file to plan scope
       → Option B: treat as read-only reference (do not rename P at usage site)
       → Must resolve before execution

  4. Special case — re-export:
     If file B imports P from file A AND re-exports P to file C:
       Register chain: A → B → C (transitive)
       C's node pre_condition: B's node DONE (not just A's)

OUTPUT: cross_file_chains[] registered in TEG and Volume descriptors
```

### Cross-File Execution Order

Cross-file chains impose a **partial order on files** within a plan.
This order is derived geometrically, not assigned manually:

```
Build file dependency graph from cross-file chains:
  messages.css → messages.html (Type A: css defines, html uses)
  tokens.css   → messages.css  (Type A: tokens defined in shared file)
  tokens.css   → wallet.css
  messages.html→ messages.js   (Type C: html attr → js event handler)

Topological sort:
  Tier 0: tokens.css
  Tier 1: messages.css, wallet.css  (both depend on tokens.css)
  Tier 2: messages.html              (depends on messages.css)
  Tier 3: messages.js                (depends on messages.html)

File execution order: [tokens.css] → [messages.css, wallet.css] → [messages.html] → [messages.js]
(parallel within tier IF no lock conflict)
```

---

## Dynamic Guide Loading (Mid-Execution Reshape)

When a guide arrives after execution has started, the matrix must be reshaped.
This is the most disruptive operation — handled with a full cascade protocol.

### Reshape Triggers

```
Trigger 1: new ARCHITECTURAL guide arrives (supersedes existing)
           → Z=0 and/or Z=1 nodes change → cascade to ALL Z=2+ volumes

Trigger 2: new SPECIALIZED guide arrives (new domain or rule set)
           → Z=1 node added → new vertical chains required in affected files
           → some Z=5 nodes may gain new post_conditions

Trigger 3: existing guide version updated (patch)
           → Z=1 node content updated → re-derive post_conditions for affected Z=5 nodes

Trigger 4: guide removed (deprecated)
           → Z=1 node marked INACTIVE → vertical chains now have broken links
           → affected Z=5 nodes must find new Z=0 anchor or be flagged UNGROUNDED
```

### Full Reshape Protocol

```
NEW GUIDE ARRIVED: spec-widget-naming-2.1 (SPECIALIZED, X=0, Y=0,1)
Currently: PLAN-001 at 42/84 (Z=5 pass halfway through messages.html)

STEP 1 — HALT current atomic execution
  Complete current ATOMIC task (cannot interrupt mid-operation)
  Write checkpoint: MSNAP-P001-F01-Z5-042-RESHAPE-PRE
  Status: "Reshape triggered — checkpoint saved before guide integration"

STEP 2 — Register guide in GUIDE_REG
  Parse invariants from spec-widget-naming-2.1
  New invariant found: INV-WIDGET-NAME (widget name must match file basename)
  Insert M[0, 0, 0-INV-WIDGET-NAME] into shared Z=0 layer
  Insert M[1, 0, 0-spec-2.1] into shared Z=1 layer

STEP 3 — Cascade to affected volumes
  INV-WIDGET-NAME applies to: messages.html, messages.css (file basename = "messages")
  VOL-P001 affected: yes
  VOL-P002 affected: yes (wallet.html — basename "wallet")

STEP 4 — Vertical chain audit per affected volume
  For each Z=5 node in VOL-P001 at [0,0] and [0,1]:
    Check: does its target string conform to INV-WIDGET-NAME?
    Conforming: M[5,0,0] --messages-bubble-radius ✅ (already correct)
    Conforming: M[5,0,1] .messages-bubble         ✅ (already correct)
    NON-CONFORMING FOUND: M[5,0,1-pending] .msg-thread → should be .messages-thread
      (was planned as .msg-thread, new invariant requires .messages-thread)

STEP 5 — Rework non-conforming nodes (ONLY pending ones)
  Already DONE nodes: cannot rollback unless FAILED or explicitly ordered
    → check if DONE node's content now violates new invariant
    → if YES: flag for REMEDIATION pass (separate atomic task added)
    → if NO:  DONE node is grandfathered (content already correct)

  PENDING nodes: rewrite target from .msg-thread → .messages-thread
    → update post_conditions
    → update diagonal edges (any node consuming .msg-thread now consumes .messages-thread)

STEP 6 — New task generation
  If new invariant requires NEW work not in current plan:
    → generate new Z=5 nodes for newly-required changes
    → insert into horizontal chains at correct Y-position
    → update plan progress counter: 84 → 87 (3 new tasks)

STEP 7 — Re-run invariant pre-scan on all PENDING nodes
  "Pre-scan: 42 PENDING nodes in VOL-P001 | 0 new violations | 0 ungrounded nodes"

STEP 8 — RESUME
  Load checkpoint MSNAP-P001-F01-Z5-042-RESHAPE-PRE
  Verify current state consistent with checkpoint
  Continue from node 043
  "Reshape complete ✓ | 1 node reworked | 3 nodes added | resume: T-001-043"
```

---

## LLM Navigation Protocol

The LLM does not "see" the entire matrix — it maintains an **active viewport**
over the matrix space. The navigation protocol defines what the LLM holds in active
context vs what it references from checkpoints.

### Viewport Model

```
Context Window = Viewport over Matrix Space

At any moment, the LLM's context contains:

  ┌─────────────────────────────────────────────────────────────────┐
  │  PERSISTENT ZONE (always retained)                              │
  │  Z=0: condensed invariant table (all INV-IDs + one-line rules)  │
  │  Z=1: active guide references (id + version + §-ref per node)   │
  │  Context budget: [used/total/%]                                  │
  │  Session id: [id]   Plan: [id]   File: [name]                   │
  └────────────────────────────────────────────────────────────────-┘
  │  WORKING ZONE (current execution context)                        │
  │  Z=3: current file aggregate (all chain counts)                  │
  │  Z=4: current pass descriptor (name, order, cell list)           │
  │  Z=5: current cell M[Z,X,Y] — FULL NODE DETAIL                 │
  │  Z=5: next 3 nodes (lite: id + target + pre_conditions only)    │
  │  Z=5: prev 3 nodes (lite: id + status + post_check result only) │
  └────────────────────────────────────────────────────────────────-┘
  │  REFERENCE ZONE (compressed, available on demand)               │
  │  Z=5: completed nodes → compressed to count per cell            │
  │  Z=3: completed files → compressed to one-line status           │
  │  Cross-file chains: only active (consumer not yet started)       │
  └─────────────────────────────────────────────────────────────────┘
```

### Viewport Navigation Rules

**Rule 1 — Locality:**  
The LLM holds full detail only for the node it is currently executing
and its immediate neighbors in all three chain directions.
Everything else is referenced by id, not loaded in full.

**Rule 2 — Invariant Anchoring:**  
Z=0 content is always in the persistent zone, compressed to one line per invariant.
If a Z=0 invariant is needed for a self-check, the compressed form is sufficient —
full guide prose is never reloaded during execution.

**Rule 3 — Lookahead:**  
Before starting a new cell M[Z, X, Y], load the cell's node list (ids + targets only).
Full node detail loads one-at-a-time as execution proceeds through the chain.
This prevents front-loading all 84 nodes at session start.

**Rule 4 — Diagonal Pre-load:**  
When a node with diagonal edges completes, immediately pre-load the target node's
address and pre_condition list into the working zone.
The diagonal target does not need full detail yet — only its pre_condition check.

**Rule 5 — File Boundary Reset:**  
When transitioning to a new file (Z=3 boundary), evict the completed file's
Z=4 and Z=5 content from the working zone.
The new file's Z=3 aggregate and Z=4 pass structure loads fresh.
Cross-file chain references are retained.

### Viewport State Machine

```
IDLE
  │  (receive task: start plan)
  ▼
LOAD_INVARIANTS           Z=0 condensed table → persistent zone
  │
  ▼
LOAD_GUIDES               Z=1 guide refs → persistent zone
  │
  ▼
LOAD_FILE                 Z=3 file aggregate → working zone
  │
  ▼
LOAD_PASS                 Z=4 pass descriptor → working zone
  │
  ▼
LOAD_CELL         ──────  cell M[Z,X,Y] node list (lite) → working zone
  │
  ▼
EXECUTE_NODE              current node full detail → working zone front
  │
  ├─ self-check PASS ──→  ADVANCE_NODE (next in horizontal chain)
  │                         or ADVANCE_CELL (chain done, next Y)
  │                         or ADVANCE_PASS (all Y done at this X)
  │                         or ADVANCE_FILE (all passes done)
  │                         or ADVANCE_PLAN (all files done)
  │
  └─ self-check FAIL ──→  ROLLBACK → re-EXECUTE_NODE (retry)
                           or FLAG_STRUCTURAL_FAIL → IDLE (halt)
```

### Navigation Prompt Format

At each file and pass boundary, the LLM emits a **navigation statement** —
a compact declaration of where it is in the matrix and where it is going:

```
MATRIX NAVIGATION
  Position:    VOL-P001 | messages.html | Z=5 | M[5,0,0] | node 14/20
  Completed:   M[5,0,1] CLASS ✅ (22/22) | M[5,0,2] KEYFRAME ✅ (3/3)
  Blocked:     M[5,0,3] ATTR ░ (0/8) — waiting: M[5,0,0] completion
  Active chain: M[5,0,0] TOKEN → node 15/20
  Next target:  --msg-avatar-size → --messages-avatar-size (line 91)
  Diagonal:    upon M[5,0,0] completion → unlock M[5,0,3] ATTR chain (8 nodes)
  Budget:      47% remaining (105k/200k) | compress threshold: 70% ✓
```

---

## Matrix Compression Protocol

When context budget falls below thresholds, the matrix representation is compressed
in layers — the outermost (highest Z, most local) layers fold first.

### Compression Levels

```
Level 0 — NORMAL (budget > 70%)
  All zones active. Full node detail available.
  Completed nodes: lite form (id + status + post_check).
  
Level 1 — COMPRESS (budget 30–70%)
  Completed files → one-line status per file (no cell detail).
  Completed passes → count per cell only, no node list.
  Pending nodes → full detail retained.
  Z=0, Z=1 → unchanged (always retained).
  
Level 2 — OFFLOAD (budget 10–30%)
  Completed files → removed from working zone, referenced by checkpoint id only.
  Completed passes → removed, referenced by MSNAP id.
  Current cell only → full detail.
  Next 1 node → lite (id + target).
  Z=0 → ultra-compressed: "INV-CSS-TOKENS:noAbbrev | INV-LAW0:noGetById"
  Z=1 → guide ids only, no §-refs.
  
Level 3 — CRITICAL (budget < 10%)
  HALT execution.
  Write MSNAP at current cell boundary.
  Emit resume prompt (see §8.3 of Driver).
  Compress everything to: plan_id + last_node_id + next_node_id + file_hash.
  New session required.
```

### Compression Transform Examples

**Level 1 — Completed cell folding:**

```
Before compression (full Z=5 node list):
  M[5,0,0]: [node-001 DONE, node-002 DONE, ... node-014 DONE, node-015 PENDING ...]

After Level 1 compression:
  M[5,0,0]: done=14/20 | last=node-014 DONE | next=node-015 PENDING
```

**Level 1 — Completed file folding:**

```
Before:
  messages.html: Z=3 aggregate + Z=4 passes + Z=5 nodes (all DONE)

After:
  messages.html: ✅ DONE | tasks=84 | MSNAP=MSNAP-P001-F01-Z5-084
```

**Level 2 — Invariant ultra-compression:**

```
Before:
  M[0,0,0] INV-CSS-TOKENS: "all CSS custom properties must use full widget name,
    no abbreviations, format: --widgetname-property-name, check: PATTERN_ABSENT
    of abbreviated forms, scope: GLOBAL, severity: CRITICAL"

After:
  INV-CSS-TOKENS: noAbbrev (CRIT)
```

### Decompression (Rehydration from Checkpoint)

```
DECOMPRESSION PROTOCOL on session resume

1. Load MSNAP-P001-F01-Z5-042
2. Restore persistent zone:
   Z=0 → expand from ultra-compressed invariant table
   Z=1 → expand guide refs from guide_ids (GUIDE_REG lookup)
3. Restore working zone:
   Z=3 → file aggregate from MSNAP.layer_state
   Z=4 → current pass from MSNAP.active_chains.horizontal
   Z=5 → current cell — load nodes from cell_states at last completed + pending
4. Verify file hash: sha256(messages.html) == MSNAP.file_hash
   → MATCH: proceed ✅
   → MISMATCH: file modified externally → HALT, require human review ❌
5. Restore cross-file chains: load XFC-P001-* for active (not yet consumed) chains
6. Emit navigation statement (see above)
7. Resume at MSNAP.next_node
```

---

## Matrix Diff and Regression Detection

After each pass and file, the matrix computes a **structural diff** between
the expected end state (from task map) and the actual state (from execution).
Divergences are regressions — detected geometrically before validation.

### Expected vs Actual State

```
For each completed cell M[Z, X, Y]:
  Expected state (from task map at population time):
    all_patterns_removed: ["--msg-bubble-radius", "--msg-sent-bg", ...]
    all_patterns_added:   ["--messages-bubble-radius", "--messages-sent-bg", ...]
    node_count_done: 20

  Actual state (from execution results + file scan):
    grep("--msg-bubble-radius", messages.html) = 0   ✅
    grep("--messages-bubble-radius", messages.html) = 14  ✅
    node_count_done: 20                              ✅
    
  Diff: ∅ — no regression
```

**Regression signature types:**

```
REGRESSION TYPE 1 — Missing replacement (pattern still present):
  grep("--msg-bubble-radius") == 2  (expected 0)
  → 2 instances were not caught by horizontal chain
  → Cause: substring was not in context; line range was stale
  → Action: add 2 missing nodes to cell M[5,0,0], re-execute

REGRESSION TYPE 2 — Corrupted replacement (wrong string inserted):
  grep("--messages-bubble-radius") == 12  (expected 14)
  grep("--messagesbubble-radius")  == 2   (unexpected — mangled)
  → 2 instances were replaced incorrectly (missing hyphen)
  → Cause: replacement string was wrong in 2 nodes
  → Action: rollback those 2 nodes, fix replacement string, re-execute

REGRESSION TYPE 3 — Cross-cell contamination (wrong domain affected):
  grep("messages-bubble-radius") in CLASS selectors == 3  (unexpected)
  → STRUCTURAL·TOKEN rename contaminated STRUCTURAL·CLASS names
  → Cause: replacement pattern was too broad (not anchored to --)
  → Action: rollback contaminated nodes, refine pattern, re-execute

REGRESSION TYPE 4 — Diagonal breakage (consumer not updated):
  M[5,0,0] TOKEN: DONE ✅ (--messages-bubble-radius renamed correctly)
  M[5,0,3] ATTR:  DONE ✅
  M[5,1,6] FUNC:  PENDING — but JS still references old --msg-bubble-radius!
  → Diagonal chain was registered but pre_condition was not checked before M[5,1,6]
  → Cause: pre_condition check was skipped
  → Action: M[5,1,6].status → REWORK, re-execute after verifying pre_conditions
```

### Diff Protocol

Run at every cell completion, every pass completion, and every file completion:

```
MATRIX DIFF at cell M[5,0,0] completion (messages.html)

Expected removals:         20 patterns
Actual removals:
  grep each expected → results: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  All zeros ✅

Expected additions:        20 patterns
Actual additions:
  grep each expected → results: [3,2,1,4,2,1,2,1,3,4,2,1,1,2,3,2,1,1,2,1]
  All > 0 ✅

Contamination scan:
  Unexpected patterns at M[5,0,1] from M[5,0,0] operation: 0 ✅
  Unexpected patterns at M[5,0,3] from M[5,0,0] operation: 0 ✅

Diagonal pre-condition scan:
  M[5,0,3] ATTR chain: pre_condition "M[5,0,0].done==20" → SATISFIED ✅
  M[5,1,6] FUNC chain: pre_condition "M[5,0,0].done==20" → SATISFIED ✅

DIFF RESULT: ∅ — cell M[5,0,0] clean, proceed to M[5,0,2] KEYFRAME
```

---

## Compound and Recursive Chain Patterns

Real codebases contain chains that are more complex than simple linear sequences.
The matrix accommodates four advanced patterns.

### Pattern A — Fan-Out Chain

One definition node → N consumer nodes across multiple files and domains.

```
M[tokens.css, 5, 0, 0] --messages-bubble-radius DEFINED
    │
    ├──▶  M[messages.html, 5, 0, 0]  var(--messages-bubble-radius) in style attr
    ├──▶  M[messages.css,  5, 0, 1]  --messages-bubble-radius: 0.75rem (declaration)
    ├──▶  M[messages.js,   5, 1, 6]  getPropertyValue('--messages-bubble-radius')
    └──▶  M[tests/messages.test.js, 5, 0, 5]  expect(token).toBe('--messages-bubble-radius')

Fan-out node: one source, N targets
Execution constraint: ALL N targets share pre_condition on source
                      but targets are independent of each other
                      → can execute targets in parallel (if in different files, no lock conflict)
```

### Pattern B — Fan-In Chain

N prerequisite nodes must all be DONE before one target node can start.

```
M[5,0,0] TOKEN        DONE ──┐
M[5,0,1] CLASS        DONE ──┤──▶  M[5,1,6] FUNCTION (JS reads token + class)
M[5,0,3] ATTRIBUTE    DONE ──┘     pre_conditions: ALL THREE must be DONE

Fan-in node: register all N as pre_conditions
Execution constraint: target cannot start until ALL sources DONE
                      → this is the bottleneck in the critical path
```

### Pattern C — Transitive Chain

A → B → C where B is both a consumer of A and a producer for C.

```
tokens.css    M[5,0,0]: --msg-bubble-radius → --messages-bubble-radius (definition)
    │
    ▼
messages.css  M[5,0,0]: re-declares --messages-bubble-radius with new value (re-export)
    │
    ▼
messages.html M[5,0,3]: var(--messages-bubble-radius) (final consumer)

Transitive chain: A → B → C
Execution order:  tokens.css M[5,0,0] → messages.css M[5,0,0] → messages.html M[5,0,3]
Lock order:       alphabetical: messages.css, messages.html, tokens.css
                  Execute: tokens.css first (despite lock order — dependency wins over alpha)
Detection:        during cross-file scan, B appears as both consumer AND producer
                  register: XFC-A→B + XFC-B→C + XFC-A→C (transitive)
```

### Pattern D — Convergent-Divergent (Diamond)

A → {B, C} → D  where B and C are parallel, D waits for both.

```
   M[tokens.css, 5,0,0]   TOKEN rename
         │
    ┌────┴────┐
    │         │
    ▼         ▼
M[msgs.css  M[msgs.html    (parallel — different files, different locks)
  5,0,0]     5,0,0]
CLASS reuse TOKEN consumer
    │         │
    └────┬────┘
         │
         ▼
M[msgs.js, 5,1,6]   JS function — needs both CSS and HTML in correct state

Diamond shape: both middle nodes must complete before bottom node starts
Execution:  tokens.css → [messages.css ∥ messages.html] → messages.js
            (∥ = parallel execution where lock table permits)
Critical path: tokens.css → messages.css → messages.js
               OR
               tokens.css → messages.html → messages.js
               (whichever is longer = critical path)
```

---

## Behavioral Node Special Protocol (X=1)

BEHAVIORAL nodes (X=1) are fundamentally different from STRUCTURAL nodes (X=0).
STRUCTURAL changes are mechanical — the matrix verifies them by pattern count.
BEHAVIORAL changes are semantic — the matrix cannot verify them by pattern alone.

### X=1 Node Properties

```json
{
  "address": { "Z": 5, "X": 1, "Y": 6 },
  "content": {
    "type": "REPLACE",
    "target":      "document.getElementById('msg-container')",
    "replacement": "document.querySelector('[data-widget=\"messages\"]')",
    "rationale":   "INV-LAW0: no getElementById — replace with data-attribute lookup",
    "behavioral_impact": "selector changes from id-based to data-attribute-based",
    "semantic_equivalent": true
  },
  "verification": {
    "pattern_check": {
      "removed": "getElementById\\('msg-container'\\)",
      "added":   "querySelector\\('\\[data-widget=\"messages\"\\]'\\)"
    },
    "semantic_check": {
      "type": "FUNCTIONAL_EQUIVALENCE",
      "description": "both selectors must resolve to same DOM element at runtime",
      "pre_condition_required": "data-widget='messages' attribute exists on target element",
      "cross_file_dependency": "M[messages.html, 5,0,3] ATTR — data-widget added first"
    },
    "regression_risk": "HIGH"
  }
}
```

### X=1 Execution Constraints

**Constraint 1 — Structural prerequisites must be 100% complete:**
```
Before any X=1 node executes in a file:
  ALL M[Z, X=0, *] nodes in that file → status DONE
  Reason: behavioral changes reference names — names must be final before logic changes
```

**Constraint 2 — Cross-file structural prerequisites:**
```
X=1 node in messages.js referencing data-widget attribute:
  Must wait for M[messages.html, 5, 0, 3] STRUCTURAL·ATTRIBUTE → DONE
  (the attribute must exist in its final form before the JS reads it)
```

**Constraint 3 — Semantic verification supplement:**
```
PATTERN verification (what the matrix can check automatically):
  grep "getElementById('msg-container')" → 0    ✅ / ❌
  grep "querySelector('[data-widget='messages']')" → 1   ✅ / ❌

SEMANTIC verification (what the LLM must reason about):
  "Does the new selector select the same element the old one did?"
  "Does the element have the required data-attribute after M[5,0,3] completes?"
  "Are there any other calls in this file assuming id-based selection?"
  "Does any test mock getElementById that must also be updated?"
```

**X=1 Self-Check extension (AEP step ③ for behavioral nodes):**

```
③-SEMANTIC:
  After pattern check passes:
    □ New implementation is semantically equivalent to old?
    □ All cross-file pre_conditions satisfied (data-attributes exist)?
    □ No other X=1 behavioral change in same file conflicts with this one?
    □ No regression introduced in X=0 STRUCTURAL layer
       (behavioral change must not create new structural violations)
    □ Downstream X=2 ADDITIVE nodes (if any) still valid?
```

---

## Matrix Build Algorithm

Complete pseudocode for populating the matrix from Phase 1 analysis output.
This is the bridge from "list of findings" to "3D geometric structure."

```
ALGORITHM: BUILD_MATRIX_FROM_ANALYSIS

Input:  analysis_findings[]  (from Phase 1 of base methodology)
        guide_registry{}     (from Driver GUIDE_REG — Z=0 and Z=1 already populated)
        plan_id, file_set

Output: matrix{}             (populated with all nodes and chains)

─────────────────────────────────────────────────────────────────────

PHASE A: Z=2,3,4 scaffold (top-down skeleton)

  1. Create M[2, *, *] plan aggregate node (one per plan)
  2. For each file in file_set:
       Create M[3, *, *] file aggregate node
       Link: M[3] vertical.parent → M[2]
  3. For each file:
       Identify passes required (which [X, Y] cells are non-empty?)
       Create M[4, X, Y] pass nodes for each occupied cell
       Link: M[4] vertical.parent → M[3]
  4. Verify: every M[4] has vertical chain to M[0] via M[3] → M[2] → M[1] → M[0]

PHASE B: Z=5 node creation (bottom-up population from findings)

  For each finding F in analysis_findings[]:
    a. Determine address: M[5, X, Y] (use determination rules from §Population Protocol)
    b. Check cell occupancy:
         if cell occupied by different plan → CELL_COLLISION → log conflict
         if cell occupied by same plan → add node to existing cell (sequence++)
    c. Create TEN (Task Execution Node) with:
         content: F.target, F.replacement, F.file, F.location
         pre_conditions: [prev_node_in_chain.status == DONE, lock check]
         post_conditions: [pattern_count checks, invariant_checks]
    d. Link to vertical parent:
         vertical.parent = M[4, X, Y] in same file
    e. Register in TASK_REG (Driver)

PHASE C: Horizontal chain construction

  For each file F:
    For each Z=5 X-level (0, 1, 2, 3, 4):
      Collect all nodes at M[5, X, *] in file F
      Sort by:
        primary:   Y ascending (domain dependency order)
        secondary: replacement string length DESCENDING (substring safety)
      Link as doubly-linked chain:
        node[i].horizontal.next = node[i+1]
        node[i+1].horizontal.prev = node[i]
      First node: pre_condition ← previous X-level all DONE
                  (M[5, X-1, *] all DONE before M[5, X, *] start)

PHASE D: Diagonal chain discovery

  For each M[5, X, Y] node N:
    For each consumer pattern (token var(), class ref, attr ref, function call, import):
      Search all files in scope for occurrences of N.content.target being consumed
      For each match M in another domain Y' or file F':
        If M not yet in matrix → create new Z=5 node for M, add to plan scope
        Register diagonal edge: N.diagonal → M (edge_type: DOMINOES_INTO)
        Register reverse: M.pre_conditions → N.status == DONE
  
  Special diagonal scan:
    Cross-file (Type A,B,C,D from §Cross-File Chain Stitching)
    Fan-out detection: N has > 1 diagonal target
    Fan-in detection: M has > 1 diagonal source
    Diamond detection: Fan-out that converges into Fan-in downstream

PHASE E: Chain integrity validation

  □ Every Z=5 node has vertical chain to Z=0?
  □ Horizontal chains have no cycles? (topological check per file per X-level)
  □ Diagonal edges are bidirectional? (source registers, target pre_conditions registered)
  □ X=3 REDUCTIVE nodes have zero remaining consumers? (no diagonal targets pending)
  □ X=1 BEHAVIORAL nodes have all X=0 STRUCTURAL prerequisites at same file complete?
  □ Cross-file chains respect file dependency order?
  □ No CELL_COLLISION logged without resolution?

PHASE F: Critical path calculation

  For each Z=5 leaf node N (no horizontal.next, no diagonal targets pending):
    Walk backward: N → prev → ... → first node in chain
    Add: vertical depth (always 5 for Z=5)
    Add: diagonal path lengths
    Total = critical path length for this endpoint
  
  global_critical_path = max over all endpoints
  Mark critical path nodes: node.on_critical_path = true
  Schedule critical path nodes first within each execution tier

OUTPUT SUMMARY:
  "Matrix built: PLAN-001 | files=2 | cells=12 | nodes=84
   chains: vertical=84 | horizontal=5 chains (84 nodes) | diagonal=8 edges
   cross-file: 3 XFC chains (A→B→C file order: tokens.css→messages.css→messages.html)
   critical path: 14 hops | conflicts: 0
   integrity: all checks PASSED ✅"
```

---

## Worked Example — Two Plans, Three Files

A complete end-to-end illustration of the matrix with all mechanisms active.

### Setup

```
Session: sess-20240115-001
Guides:  arch-containerization-6 (Z=0: INV-CSS-TOKENS, INV-LAW0)
Plans:   PLAN-001: rename CSS tokens+classes in messages.html + messages.css
         PLAN-002: rename CSS tokens+classes in wallet.html (partially overlaps token names)
Files:   messages.html, messages.css, wallet.html
```

### Step 1 — Guide Loading (Z=0, Z=1)

```
Z=0 layer populated:
  M[0,0,0] INV-CSS-TOKENS  "no abbreviated --custom-properties"  scope:GLOBAL
  M[0,1,4] INV-LAW0        "no getElementById"                   scope:GLOBAL

Z=1 layer populated:
  M[1,0,0] arch-v6 §7.1    "use full widget name in token prefix"
  M[1,0,1] arch-v6 §5.3    "use BEM: .widgetname-element--modifier"
  M[1,1,4] arch-v6 §9.1    "replace id selectors with data-attributes"
```

### Step 2 — Plan Registration + Volume Creation

```
VOL-P001:
  Z=2: M[2,0,0] PLAN-001 aggregate
  Z=3: M[3,0,0] messages.html aggregate
       M[3,0,0] messages.css aggregate

VOL-P002:
  Z=2: M[2,0,0] PLAN-002 aggregate
  Z=3: M[3,0,0] wallet.html aggregate

Overlap check: VOL-P001 ∩ VOL-P002 = DISJOINT (no shared files)
Conflict matrix: PLAN-001 vs PLAN-002 → NO conflicts (different files)
Schedule: [PLAN-001] ∥ [PLAN-002]  ← can run in parallel
```

### Step 3 — Matrix Build (messages.html, PLAN-001 only)

```
Analysis findings for messages.html (partial):
  F001: --msg-bubble-radius (x14 occurrences) → TOKEN
  F002: --msg-sent-bg       (x8)              → TOKEN
  F003: .msg-bubble         (x22)             → CLASS
  F004: data-msg-variant    (x8)              → ATTRIBUTE
  F005: getElementById('msg-container') (x3)  → BEHAVIORAL, FUNCTION

ADDRESS ASSIGNMENT:
  F001 → M[5, 0, 0]  ATOMIC·STRUCTURAL·TOKEN     (14 nodes)
  F002 → M[5, 0, 0]  ATOMIC·STRUCTURAL·TOKEN     (8 more nodes, same cell)
  F003 → M[5, 0, 1]  ATOMIC·STRUCTURAL·CLASS     (22 nodes)
  F004 → M[5, 0, 3]  ATOMIC·STRUCTURAL·ATTRIBUTE (8 nodes)
  F005 → M[5, 1, 6]  ATOMIC·BEHAVIORAL·FUNCTION  (3 nodes)

HORIZONTAL CHAINS:
  X=0: M[5,0,0]→M[5,0,1]→M[5,0,3]  (TOKEN→CLASS→ATTR, in Y-order)
  X=1: M[5,1,6]                      (single, starts after X=0 complete)

DIAGONAL EDGES:
  M[5,0,0]→M[5,0,1]: class .msg-bubble uses token (but both in same file, same pass)
  M[5,0,3]→M[5,1,6]: data-msg-variant attr consumed by JS function
  M[5,0,0]→M[messages.css, 5,0,0]: token defined in .html used in .css  ← CROSS-FILE

CRITICAL PATH: M[5,0,0](22 nodes) → M[5,0,3](8 nodes) → M[5,1,6](3 nodes) = 33 nodes long
```

### Step 4 — Execution (PLAN-001, messages.html)

```
MATRIX NAVIGATION — Start
  Position: VOL-P001 | messages.html | Z=5 | M[5,0,0] | node 1/22
  Budget: 89% remaining

[Execute M[5,0,0] node 1/22]
  Operation: --msg-bubble-radius → --messages-bubble-radius (line 69)
  AEP: pre ✅ → execute → self-check:
    grep("--msg-bubble-radius")    == 13  (was 14, now 13) ✅
    grep("--messages-bubble-radius") == 1  (new) ✅
    INV-CSS-TOKENS: SATISFIED ✅
  Result: DONE | checkpoint: MSNAP-P001-F01-Z5-001

[... nodes 2–22 execute similarly ...]

[M[5,0,0] chain COMPLETE — 22/22 DONE]
  DIFF check:
    grep all removed patterns → all 0 ✅
    grep all added patterns   → all > 0 ✅
    contamination scan at M[5,0,1] → 0 unexpected changes ✅
  Diagonal: M[5,0,3] ATTR pre_condition satisfied → UNLOCKED ✅
  Layer snapshot: MSNAP-P001-F01-Z5-022

[Execute M[5,0,1] CLASS chain — 22 nodes]
  [... executes, completes ...]

[Execute M[5,0,3] ATTRIBUTE chain — 8 nodes]
  [... executes, completes ...]
  Diagonal: M[5,1,6] FUNCTION pre_conditions satisfied → UNLOCKED ✅

[Execute M[5,1,6] BEHAVIORAL chain — 3 nodes]
  Node 1: getElementById('msg-container') → querySelector('[data-widget="messages"]')
  AEP semantic check:
    pattern: "getElementById\\('msg-container'\\)" → 0 ✅
    pattern: "querySelector\\('\\[data-widget=\\\"messages\\\"\\]'\\)" → 1 ✅
    semantic: data-widget="messages" attr exists in M[5,0,3] completed work ✅
  Result: DONE ✅

[messages.html Z=5 COMPLETE — 55/55 DONE]
  File-level validation (Level 2):
    All patterns removed: 0 occurrences each ✅
    All ARCH invariants: SATISFIED ✅
    Lock released: messages.html
  Cross-file chain: XFC-P001-001 activated → messages.css may now lock and start
  Layer snapshot: MSNAP-P001-F01-Z5-055-FILE-COMPLETE
```

### Step 5 — Cross-Plan Status at Midpoint

```
SYSTEM STATUS — PLAN-001 at 55/84 | PLAN-002 at 31/48

VOL-P001 (messages.html ✅, messages.css IN_PROGRESS):
  M[5,0,0] messages.css TOKEN: 12/18 ░░░░░░░░░████████████  67%

VOL-P002 (wallet.html IN_PROGRESS):
  M[5,0,0] wallet.html TOKEN: 15/22 ░░░░░░░████████████████  68%

Shared Z=0 layer:
  INV-CSS-TOKENS: SATISFIED in both volumes ✅
  INV-LAW0:       SATISFIED in VOL-P001 | NOT_YET_CHECKED in VOL-P002 (no JS in wallet)

Cross-volume interactions: 0 (volumes are disjoint)
Lock table: messages.css (P001), wallet.html (P002) — no contention ✅

Critical path remaining:
  VOL-P001: messages.css 6 nodes remaining (critical) + file validation
  VOL-P002: wallet.html 7 nodes remaining (critical) + file validation
Projected: P001 finishes first, P002 follows within 10 nodes
```

### Step 6 — Final System Validation (all plans complete)

```
SYSTEM VALIDATION (Level 4)
══════════════════════════════════════════════════════════════════════

Matrix Population:
  Total cells populated:  18 (across 3 files, 2 plans)
  Total nodes created:    132 (84 P001 + 48 P002)
  Total chains:           vertical=132, horizontal=7, diagonal=11, cross-file=4

Execution Results:
  Nodes DONE:     132 / 132  ✅
  Nodes FAILED:       0       ✅
  Rollbacks:          0       ✅
  Diffs clean:       all     ✅

Invariant Status:
  INV-CSS-TOKENS:  grep all abbreviated patterns in all 3 files → 0   ✅
  INV-LAW0:        grep getElementById in all JS files → 0             ✅

Cross-Plan Consistency:
  Token --messages-bubble-radius: consistent in messages.html, messages.css ✅
  Token --wallet-card-radius: consistent in wallet.html ✅
  No cross-plan contamination ✅

Layer Snapshots:
  Total saved: 28 | Verified: 28 | Corrupted: 0 ✅

Context Budget:
  Peak usage: 61% | Compressions triggered: 0 | Overflows: 0 ✅

STATUS: ALL CLEAN ✅  Session complete.
══════════════════════════════════════════════════════════════════════
```

---

## Quick Reference Card

### Address Lookup

```
"I have a CSS token rename"     → M[5, 0, 0]  ATOMIC · STRUCTURAL · TOKEN
"I have a CSS class rename"     → M[5, 0, 1]  ATOMIC · STRUCTURAL · CLASS
"I have a keyframes rename"     → M[5, 0, 2]  ATOMIC · STRUCTURAL · KEYFRAME
"I have an HTML attr rename"    → M[5, 0, 3]  ATOMIC · STRUCTURAL · ATTRIBUTE
"I have an HTML id removal"     → M[5, 3, 4]  ATOMIC · REDUCTIVE · ID
"I have a JS var rename"        → M[5, 0, 5]  ATOMIC · STRUCTURAL · VARIABLE
"I have a JS logic change"      → M[5, 1, 6]  ATOMIC · BEHAVIORAL · FUNCTION
"I have a new event listener"   → M[5, 2, 7]  ATOMIC · ADDITIVE · EVENT
"I have a module import fix"    → M[5, 0, 8]  ATOMIC · STRUCTURAL · IMPORT
"All token work in one file"    → M[4, 0, 0]  PASS · STRUCTURAL · TOKEN
"All X=0 work in one file"      → M[3, 0, *]  FILE · STRUCTURAL · *
"All work in plan"              → M[2, *, *]  PLAN aggregate
"The guide rule"                → M[1, 0, 0]  SYSTEM · arch-v6
"The invariant"                 → M[0, 0, 0]  INVARIANT · INV-CSS-TOKENS
```

### Execution Order Cheat Sheet

```
Files:   by cross-file chain topological order (definition files before consumer files)
X-axis:  0 → 1 → 2 → 3 → 4  (STRUCTURAL before BEHAVIORAL before ADDITIVE before REDUCTIVE)
Y-axis:  0 → 1 → 2 (CSS chain), then 3, then 4, then 5 → 6 → 7 (JS chain), then 8
Within chain: longest replacement string first (substring collision prevention)
```

### Chain Cheat Sheet

```
Vertical  (Z-axis):   WHY does this task exist? (justification to invariant)
Horizontal (X-Y plane): WHAT ELSE changes in the same pass? (domino sequence)
Diagonal  (crossing):  WHAT ELSE breaks in another domain? (coupling)
Cross-file:            WHERE ELSE in another file? (fan-out / transitive)
```

### Self-Check Directions

```
At each atomic node — check in 5 directions simultaneously:
  ① Up    (vertical):   parent pass still coherent?
  ② Down  (to Z=0):    invariant still satisfied?
  ③ Left  (horizontal.prev): prev chain node still correct?
  ④ Right (horizontal.next): next chain node pre_conditions met?
  ⑤ Across (diagonal):  diagonal consumers' pre_conditions now satisfiable?
```

---

*Designed by analogy with:  
three-dimensional tensor indexing (M[Z,X,Y] address space),  
compiler abstract syntax trees (vertical chains = scope nesting, Z=0 = type system),  
database B-tree indexes (domain-ordered horizontal traversal),  
OS memory privilege rings (Z-layers = authority rings, Z=0 cannot be overridden),  
hardware combinational path analysis (diagonal chains = timing paths through logic),  
and ACID transaction journals (layer snapshots = commit logs, diff = integrity check).*


ai-task-execution-methodology-context-matrix-driver.md:
---------------------------------
# AI Task Execution Methodology — Context Matrix Driver
## Runtime Engine for Three-Dimensional Atomic Dependency Execution

> **Role:** This document is the operational layer over `ai-task-execution-methodology-context-matrix.md`.  
> The Matrix defines *structure*. The Matrix Driver defines *how to operate that structure*.  
> The Matrix is the data model. The Matrix Driver is the runtime engine.  
>
> Document stack (bottom → top authority):
> ```
> ai-task-execution-methodology.md               ← base execution protocol (single plan)
>     ↑ managed by
> ai-task-execution-methodology-driver.md        ← multi-plan orchestration, process lifecycle
>     ↑ spatial model provided by
> ai-task-execution-methodology-context-matrix.md ← 3D structure, addresses, chain types
>     ↑ operated by
> ai-task-execution-methodology-context-matrix-driver.md  ← THIS DOCUMENT: runtime engine
> ```

---

## Philosophy

The Context Matrix defines a three-dimensional address space `M[Z, X, Y]`
and the chain types that connect nodes within it.
It answers: *"where does everything live, and how is it connected?"*

The Matrix Driver answers the operational questions the Matrix cannot answer alone:

```
Matrix says:      "M[5,0,0] has post_conditions and a diagonal to M[5,0,3]"
Matrix Driver:    "execute M[5,0,0], verify post_conditions, unlock M[5,0,3], advance cursor"

Matrix says:      "Z=5 nodes execute in X-ascending, Y-domain order"
Matrix Driver:    "maintain cursor, load viewport, emit node to AEP, record result, check coherence"

Matrix says:      "new guide reshapes Z=1 and cascades to Z=5"
Matrix Driver:    "HALT at atomic boundary, snapshot, cascade, rework, resume — in 8 steps"

Matrix says:      "context budget has three zones"
Matrix Driver:    "monitor budget token by token, trigger compression level, emit resume prompt"
```

**Four new invariants — non-negotiable:**

**Invariant M-I — Cursor Integrity.**  
At every moment there is exactly one active cursor per volume.
The cursor always points to a valid node in the matrix.
A cursor at an invalid address is a system fault, not a task failure.

**Invariant M-II — Viewport Consistency.**  
What the LLM has in active context must exactly match the Matrix Runtime Object's
viewport state. Silent divergence between viewport and MRO is worse than total context loss.

**Invariant M-III — Chain Atomicity.**  
A chain (horizontal or diagonal) is the unit of commitment, not an individual node.
Nodes within a chain are executed one-at-a-time but committed as a group.
Partial chain commit is a rollback target, not a valid resting state.

**Invariant M-IV — Scaffold Before Nodes.**  
Z=3 and Z=4 scaffold nodes must be fully built before any Z=5 node is created.
A Z=5 node without a complete vertical chain to Z=0 must not enter the matrix.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      MATRIX RUNTIME OBJECT (MRO)                             │
│                  ← live operational state, one per volume →                  │
│                                                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐   │
│  │   CURSOR     │ │  VIEWPORT    │ │ CHAIN STATE  │ │ COHERENCE STATE  │   │
│  │  (position)  │ │  (context)   │ │  (in-flight) │ │ (global health)  │   │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └────────┬─────────┘   │
└─────────┼────────────────┼────────────────┼──────────────────┼──────────────┘
          │                │                │                  │
          ▼                ▼                ▼                  ▼
┌─────────────┐  ┌──────────────────┐  ┌─────────────┐  ┌────────────────────┐
│ TRAVERSAL   │  │ VIEWPORT MANAGER │  │   CHAIN     │  │ COHERENCE MONITOR  │
│   ENGINE    │  │                  │  │  EXECUTOR   │  │                    │
│ (move/halt) │  │ (load/compress/  │  │ (horiz/diag │  │ (invariant watch,  │
│             │  │  rehydrate)      │  │  /cross-file)│  │  gate checks)      │
└──────┬──────┘  └──────────────────┘  └─────────────┘  └────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────────────────────────┐
│  SUBSYSTEMS                                                                 │
│                                                                             │
│  POPULATION ENGINE    DIFF ENGINE    RESHAPE HANDLER    VOLUME COORDINATOR  │
│  CHECKPOINT MANAGER   STATUS EMITTER ERROR RECOVERY     INTEGRATION BRIDGE  │
└────────────────────────────────────────────────────────────────────────────┘
```

**Architectural analogs:**

| Matrix Driver Component | OS Analog | Hardware Analog |
|------------------------|-----------|-----------------|
| `MRO` | Process runtime state | CPU register file |
| `CURSOR` | Program Counter (PC) | Address bus pointer |
| `VIEWPORT MANAGER` | Virtual Memory Manager | Cache line controller |
| `TRAVERSAL ENGINE` | CPU fetch-decode-execute | Instruction pipeline |
| `CHAIN EXECUTOR` | Thread scheduler (coroutine) | Data dependency unit |
| `COHERENCE MONITOR` | Hardware watchdog / ECC | Bus coherence protocol |
| `POPULATION ENGINE` | Linker (symbol resolution) | Synthesis tool |
| `DIFF ENGINE` | Memory-mapped I/O checker | Logic analyzer |
| `RESHAPE HANDLER` | Hot-patch / live-kernel-patch | Reconfigurable FPGA |
| `CHECKPOINT MANAGER` | Journaling filesystem (ext4) | NVRAM state flush |
| `VOLUME COORDINATOR` | SMP inter-CPU coherence | Multi-core cache fabric |

---

## Matrix Runtime Object (MRO)

The MRO is the central live state structure — one instance per active volume (plan).
Everything the engine reads and writes goes through the MRO.

```json
{
  "mro_id":     "MRO-P001-sess-20240115-001",
  "volume_id":  "VOL-P001",
  "plan_id":    "PLAN-001",
  "session_id": "sess-20240115-001",
  "created_at": "ISO8601",

  "cursor": {
    "position":       { "Z": 5, "X": 0, "Y": 0 },
    "sequence":       14,
    "node_id":        "MN-P001-messages.html-5-0-0-014",
    "file":           "messages.html",
    "state":          "EXECUTING",
    "advance_pending": false
  },

  "viewport": {
    "persistent_zone": {
      "invariants":       "condensed",
      "guide_refs":       "active",
      "session_meta":     "full",
      "bytes_used":       4200
    },
    "working_zone": {
      "file_aggregate":   "MN-P001-messages.html-3-0-0-root",
      "pass_descriptor":  "MN-P001-messages.html-4-0-0-001",
      "current_node":     "full",
      "lookahead_nodes":  3,
      "lookbehind_nodes": 3,
      "bytes_used":       12800
    },
    "reference_zone": {
      "completed_cells":  "count-only",
      "completed_files":  "one-line",
      "active_xfc":       "lite",
      "bytes_used":       6000
    },
    "budget": {
      "total":            200000,
      "used":             23000,
      "remaining":        177000,
      "critical_reserve": 20000,
      "compression_level": 0,
      "last_compression": null
    }
  },

  "chain_state": {
    "horizontal": {
      "active_chain_id":    "HCHAIN-P001-messages.html-5-0-0",
      "position":           "14/22",
      "started_at":         "ISO8601",
      "pending_commit":     false
    },
    "diagonal": {
      "in_flight": [
        {
          "source":  "MN-P001-messages.html-5-0-0-022",
          "targets": ["MN-P001-messages.html-5-0-3-001"],
          "state":   "WAITING_SOURCE_COMPLETE"
        }
      ]
    },
    "cross_file": {
      "pending_unlock": [
        {
          "xfc_id":         "XFC-P001-001",
          "source_file":    "messages.css",
          "target_file":    "messages.html",
          "unlock_trigger": "messages.css M[5,0,0] chain complete"
        }
      ]
    }
  },

  "coherence_state": {
    "last_gate_check":    "ISO8601",
    "gate_result":        "PASSED",
    "invariant_snapshot": {
      "INV-CSS-TOKENS": "SATISFIED",
      "INV-LAW0":       "NOT_YET_REACHED"
    },
    "active_locks": {
      "messages.html": { "type": "EXCLUSIVE", "holder": "PLAN-001" }
    },
    "regression_flags":   []
  },

  "lifecycle": {
    "phase":          "EXECUTION",
    "sub_phase":      "HORIZONTAL_CHAIN",
    "population_complete": true,
    "integrity_check_passed": true,
    "last_checkpoint_id": "MSNAP-P001-F01-Z5-013",
    "rollback_target":    "MSNAP-P001-F01-Z5-013"
  }
}
```

### MRO Lifecycle

```
CREATED
   │  (Population Engine completes scaffold)
   ▼
POPULATING         ← Population Engine filling Z=5 nodes, building chains
   │  (all integrity checks pass)
   ▼
READY              ← cursor positioned at first Z=5 node, viewport loaded
   │  (Traversal Engine activated)
   ▼
EXECUTING          ← cursor at a Z=5 node, AEP in progress
   │
   ├──[self-check PASS]──▶ ADVANCING  ← cursor moving to next position
   │                            │
   │                            └──▶ EXECUTING (next node)
   │
   ├──[GATE node reached]──▶ GATE_CHECK  ← Coherence Monitor runs
   │                              │
   │                    [PASS]────┘──▶ EXECUTING
   │                    [FAIL]────────▶ HALTED
   │
   ├──[budget threshold]──▶ COMPRESSING  ← Viewport Manager compresses
   │                              │
   │                              └──▶ EXECUTING (resumed)
   │
   ├──[budget critical]──▶ CHECKPOINTING  ← full snapshot, resume prompt
   │                              │
   │                              └──▶ SUSPENDED (new session required)
   │
   ├──[self-check FAIL]──▶ ROLLING_BACK  ← Error Recovery activates
   │                              │
   │                    [retry]───└──▶ EXECUTING
   │                    [structural]───▶ HALTED
   │
   ├──[reshape trigger]──▶ RESHAPING  ← Reshape Handler activates
   │                              │
   │                              └──▶ EXECUTING (resumed)
   │
   └──[all Z=5 nodes DONE]──▶ VALIDATING  ← Diff Engine full pass
                                    │
                          [clean]───└──▶ DONE
                          [regression]──▶ REMEDIATING
```

---

## Population Engine

The Population Engine transforms raw analysis findings into a fully-formed matrix.
It runs once per volume before the Traversal Engine starts.

### Engine States

```
IDLE → SCAFFOLDING → POPULATING → CHAINING → DIAGNOSING → READY
         │               │            │           │
         ▼               ▼            ▼           ▼
      Z=2,3,4         Z=5 nodes   H-chains    Integrity
      nodes built     created     D-chains    verified
                                  XFC-chains
```

### Phase A — Scaffold (Z=2, Z=3, Z=4)

```
SCAFFOLD PROTOCOL

Input: plan_id, file_set, guide_registry (Z=0, Z=1 already populated by Driver)

1. Create M[2,*,*] plan aggregate node
   node_id: "MN-[PLAN]-plan-2-aggregate"
   content: { plan_id, file_count, guide_ids[], conflict_group }
   vertical.parent: M[1,*,*] guide nodes (via guide_refs)
   vertical.root:   M[0,*,*] invariant nodes
   Status: emit "Z=2 scaffold: PLAN-001 aggregate created"

2. For each file F in file_set (alphabetical order):
   Create M[3,*,*] file aggregate node
   node_id: "MN-[PLAN]-[file]-3-aggregate"
   content: { file, hash_at_start: sha256(F), pass_list: [], task_count: 0 }
   vertical.parent: M[2,*,*]
   Status: emit "Z=3 scaffold: [file] aggregate created"

3. For each file F:
   Scan for required [X, Y] cells:
     Run pre-population scan: which change classes and domains are present?
   For each occupied [X, Y]:
     Create M[4, X, Y] pass descriptor node
     node_id: "MN-[PLAN]-[file]-4-[X]-[Y]-pass"
     content: { pass_name, pass_order: X*10+Y, domain: Y, change_class: X,
                expected_node_count: 0 }
     vertical.parent: M[3,*,*] file aggregate
   Status: emit "Z=4 scaffold: [file] — [N] passes identified: M[4,0,0], M[4,0,1]..."

4. Vertical chain verify: every M[4] traces to M[0]?
   For each M[4]: walk vertical.parent chain → must reach M[0] in 4 hops
   If any chain broken → SCAFFOLD_FAIL → halt (do not proceed to Z=5 population)
   Status: "Scaffold complete ✓ | files=[N] | passes=[N] | all chains to Z=0 verified"
```

### Phase B — Node Creation (Z=5)

```
NODE CREATION PROTOCOL

Input: analysis_findings[] (stream, one finding per violation/change needed)

For each finding F:
  1. DETERMINE_ADDRESS(F):
     Z = 5 (always for individual findings)
     X = classify_change_class(F)    ← STRUCTURAL/BEHAVIORAL/ADDITIVE/REDUCTIVE/RELATIONAL
     Y = classify_domain(F)          ← TOKEN/CLASS/KEYFRAME/ATTR/ID/VAR/FUNC/EVENT/IMPORT

  2. CELL_CHECK:
     existing = matrix.get_cell(file=F.file, Z=5, X=X, Y=Y)
     if existing.plan_id != current_plan → COLLISION_FLAG → log, continue
     if not existing → initialize cell as empty list

  3. SEQUENCE_ASSIGN:
     seq = cell.node_count + 1
     node_id = "MN-[PLAN]-[file]-5-[X]-[Y]-[seq:03d]"

  4. CREATE_NODE:
     {
       address: M[5, X, Y],
       node_id, plan_id, file, sequence: seq,
       content: {
         type: F.operation_type,
         target: F.target_string,
         replacement: F.replacement_string,
         location: { lines: { start: F.line_start, end: F.line_end } },
         context: F.surrounding_code
       },
       vertical: { parent: M[4,X,Y] in same file, root: M[0,X,Y] },
       horizontal: { prev: null, next: null },  ← filled in Phase C
       diagonal: [],                             ← filled in Phase D
       pre_conditions: [],                       ← filled in Phase C/D
       post_conditions: derive_post_conditions(F, X, Y),
       status: "PENDING",
       checkpoint_after: (X >= 1 OR seq % 10 == 0)  ← behavioral + every 10 atomics
     }

  5. REGISTER:
     matrix.add_node(node)
     M[4,X,Y].expected_node_count++
     M[3].task_count++

  6. EMIT per 10 nodes:
     "[N] nodes created | M[5,0,0]:[N] M[5,0,1]:[N] M[5,1,6]:[N]..."

POST-CREATION:
  Status: "Node creation complete | total=[N] | cells=[N] | files=[N]"
```

### Phase C — Horizontal Chain Construction

```
HORIZONTAL CHAIN PROTOCOL

For each file F:
  For each X-level (0, 1, 2, 3, 4):
    nodes = matrix.get_all_nodes(file=F, Z=5, X=X)
    if nodes is empty: skip

    // SORT: by Y ascending, then by replacement string length DESCENDING
    sort_key(node) = (node.address.Y * 10000) + (1000 - len(node.content.replacement))
    sorted_nodes = sort(nodes, key=sort_key)

    // LINK as doubly-linked list
    for i in range(len(sorted_nodes)):
      node = sorted_nodes[i]
      if i > 0:
        prev = sorted_nodes[i-1]
        node.horizontal.prev = prev.node_id
        // pre_condition: previous node DONE
        node.pre_conditions.append({ "node": prev.node_id, "state": "DONE" })
      if i < len(sorted_nodes) - 1:
        node.horizontal.next = sorted_nodes[i+1].node_id

    // CROSS-X pre_condition: X=1 cannot start until all X=0 nodes in file DONE
    if X > 0:
      all_prev_x_nodes = matrix.get_all_nodes(file=F, Z=5, X=X-1)
      first_node_in_chain = sorted_nodes[0]
      for prev_x_node in all_prev_x_nodes:
        first_node_in_chain.pre_conditions.append(
          { "node": prev_x_node.node_id, "state": "DONE" }
        )

    // REGISTER chain metadata
    chain_id = "HCHAIN-[PLAN]-[file]-5-[X]-[Y_start]-[Y_end]"
    matrix.register_chain(chain_id, sorted_nodes)

    Status: "H-chain [chain_id]: [N] nodes | order: [Y_list] | longest→shortest per Y"

  // CROSS-FILE pre_condition: file B starts after all required file A chains DONE
  (handled in Phase D cross-file scan)
```

### Phase D — Diagonal Chain Discovery

```
DIAGONAL CHAIN DISCOVERY PROTOCOL

STEP 1 — Intra-file diagonals (same file, different [X] or [Y]):

  For each node N at M[5, X, Y] in file F:
    consumers = find_consumers_in_file(N.content.target, F, exclude_cell=[5,X,Y])
    for each consumer C (at different [X', Y']):
      edge = { source: N.node_id, target: C.node_id, edge_type: "DOMINOES_INTO" }
      N.diagonal.append(edge)
      C.pre_conditions.append({ "node": N.node_id, "state": "DONE", "chain": "all" })
      //  "all" = entire chain containing N must be DONE, not just N

STEP 2 — Cross-file diagonals (different files):

  For each node N at M[5, X, Y] in file F:
    For each other file F' in volume.file_set:
      consumers_in_F' = find_consumers_in_file(N.content.target, F')
      if consumers_in_F' is not empty:
        // Determine XFC type
        xfc_type = classify_xfc(N, consumers_in_F')
        xfc_id = "XFC-[PLAN]-[seq:03d]"
        xfc = {
          chain_id: xfc_id, type: xfc_type,
          source: { node_id: N.node_id, file: F },
          targets: [{ node_id: C.node_id, file: F' } for C in consumers_in_F'],
          lock_order: sorted([F, F']),  // alphabetical for deadlock prevention
          file_execution_constraint: "F must complete before F' starts"
        }
        matrix.register_xfc(xfc)
        for C in consumers_in_F':
          C.pre_conditions.append({ "xfc": xfc_id, "state": "SOURCE_FILE_DONE" })

STEP 3 — Fan-out detection:
  nodes_with_multiple_diagonal_targets = [N for N if len(N.diagonal) > 1]
  for N in fan_out_nodes:
    // targets are independent — can execute in parallel (if different files/lock)
    matrix.flag_fan_out(N.node_id, targets=[e.target for e in N.diagonal])

STEP 4 — Fan-in detection:
  nodes_with_multiple_diagonal_sources = {}
  for N in all_nodes:
    for edge in N.diagonal:
      target_id = edge.target
      nodes_with_multiple_diagonal_sources[target_id].append(N.node_id)
  for target_id, sources in nodes_with_multiple_diagonal_sources.items():
    if len(sources) > 1:
      target = matrix.get_node(target_id)
      // target cannot start until ALL sources DONE
      target.pre_conditions = [ensure_all_sources for each source]
      matrix.flag_fan_in(target_id, sources=sources)

STEP 5 — Diamond detection:
  for each fan-out node FO:
    for each fan-in node FI:
      if path_exists(FO, FI) through FO's targets:
        matrix.flag_diamond(fan_out=FO, fan_in=FI,
                            parallel_paths=paths_between(FO, FI))

Status: "Diagonal discovery complete | intra=[N] | cross-file=[N] | fan-out=[N] | fan-in=[N] | diamonds=[N]"
```

### Phase E — Integrity Verification

```
INTEGRITY_CHECK PROTOCOL

Run after all nodes, chains, and diagonals are built:

□ CHECK 1 — Every Z=5 node has vertical chain to Z=0:
  for each node N at Z=5:
    walk: N → N.vertical.parent → ... → Z=0
    verify: path length == 5, terminal node is M[0,*,*]
  FAIL: list nodes with broken vertical chains → halt

□ CHECK 2 — No horizontal chain cycles:
  for each chain HCHAIN:
    detect cycles via DFS
  FAIL: list cycle members → halt (chains must be DAGs)

□ CHECK 3 — All diagonal edges bidirectional:
  for each diagonal edge (source → target):
    verify target.pre_conditions contains source reference
  FAIL: register missing reverse registration, fix, continue

□ CHECK 4 — X=3 REDUCTIVE nodes have zero pending consumers:
  for each node N at X=3:
    check N.diagonal is empty OR all diagonal targets are X=3 nodes
  FAIL: list nodes with consumers → block reductive node, mark WAITING_CONSUMERS

□ CHECK 5 — X=1 BEHAVIORAL prerequisites:
  for each node N at X=1:
    check: all M[5, X=0, *] nodes in same file are pre-conditions or already DONE
  FAIL: add missing pre-conditions, re-sort chain

□ CHECK 6 — Cell collision registry:
  read COLLISION_FLAG entries from Phase B
  for each collision:
    check if resolution was registered (canonical value from Z=0)
    UNRESOLVED → halt Population Engine, require conflict resolution

□ CHECK 7 — Cross-file lock order consistency:
  for all XFC chains: verify lock_order is alphabetical (deadlock prevention)
  FAIL: reorder lock_order, update volume file dependency graph

RESULT:
  PASS → MRO.lifecycle.integrity_check_passed = true → proceed to READY
  FAIL → halt, emit detailed integrity report, require manual resolution
```

---

## Traversal Engine

The Traversal Engine is the main execution loop — the Program Counter of the Matrix Driver.
It selects the next node, loads it into the viewport, triggers AEP, and advances the cursor.

### Main Loop

```
TRAVERSAL_ENGINE_LOOP:

  while MRO.lifecycle.phase == "EXECUTION":

    // 1. SELECT NEXT NODE
    node = CURSOR.resolve()
    if node is null:
      TRAVERSAL_ENGINE_LOOP.exit("VOLUME_COMPLETE")

    // 2. BUDGET CHECK (before loading node)
    budget_check = VIEWPORT_MANAGER.check_budget()
    if budget_check == "CRITICAL":
      CHECKPOINT_MANAGER.emergency_snapshot(node_id=node.node_id)
      STATUS_EMITTER.emit_resume_prompt()
      MRO.lifecycle.phase = "SUSPENDED"
      break
    if budget_check in ["LEVEL_2", "LEVEL_3"]:
      VIEWPORT_MANAGER.compress(to_level=budget_check)

    // 3. LOAD NODE INTO VIEWPORT
    VIEWPORT_MANAGER.load_node(node, mode="FULL")
    VIEWPORT_MANAGER.load_lookahead(CURSOR.next_nodes(3), mode="LITE")
    VIEWPORT_MANAGER.load_lookbehind(CURSOR.prev_nodes(3), mode="LITE")

    // 4. PRE_CONDITION CHECK
    pre_result = check_pre_conditions(node)
    if pre_result == "FAIL":
      CURSOR.mark_blocked(node, reason=pre_result.reason)
      CURSOR.advance_to_unblocked()
      continue

    // 5. AEP — EXECUTE
    MRO.cursor.state = "EXECUTING"
    exec_result = AEP.execute(node)

    // 6. HANDLE RESULT
    if exec_result == "PASS":
      CHAIN_EXECUTOR.on_node_complete(node)
      DIFF_ENGINE.record_node_result(node, exec_result)
      COHERENCE_MONITOR.on_node_complete(node)
      if node.checkpoint_after:
        CHECKPOINT_MANAGER.save_node_checkpoint(node)
      CURSOR.advance()

    elif exec_result == "FAIL":
      ERROR_RECOVERY.handle_node_failure(node, exec_result)
      // Error Recovery either retries (CURSOR stays) or escalates (MRO.phase → HALTED)

    // 7. GATE CHECK (at GATE nodes, file boundaries, plan boundaries)
    if CURSOR.at_gate():
      gate_result = COHERENCE_MONITOR.run_gate_check()
      if gate_result == "FAIL":
        MRO.lifecycle.phase = "HALTED"
        STATUS_EMITTER.emit_halt_report(gate_result)
        break

    // 8. PHASE TRANSITION
    if CURSOR.at_file_boundary():
      TRAVERSAL_ENGINE.advance_file()
    elif CURSOR.at_pass_boundary():
      TRAVERSAL_ENGINE.advance_pass()
    elif CURSOR.at_plan_boundary():
      TRAVERSAL_ENGINE.advance_to_validation()
```

### Cursor

The cursor maintains the LLM's exact position in 3D matrix space.
It is the Program Counter of the execution.

```
CURSOR STATE:

{
  "position":        { "Z": 5, "X": 0, "Y": 0 },
  "sequence":        14,
  "node_id":         "MN-P001-messages.html-5-0-0-014",
  "file":            "messages.html",
  "state":           "EXECUTING",     // EXECUTING | BLOCKED | AT_GATE | AT_CHECKPOINT
  "chain_context": {
    "chain_id":      "HCHAIN-P001-messages.html-5-0-0",
    "position_in_chain": 14,
    "chain_length":  22,
    "chain_committed": false
  }
}

CURSOR MOVEMENT OPERATIONS:

  advance_node():
    sequence++
    if sequence > chain.length:
      advance_cell()
    else:
      node_id = chain[sequence]
      emit: "→ node [seq]/[total]"

  advance_cell():
    Y++ (or next occupied Y at same X)
    if no next Y at current X:
      advance_x()
    sequence = 1
    node_id = matrix.first_node_at(Z=5, X, Y, file)
    emit: "→ cell M[5,[X],[Y]] | [chain_id]"

  advance_x():
    X++ (to next occupied X)
    if no next X in file:
      advance_file()
    Y = first occupied Y at new X
    sequence = 1
    emit: "→ X=[X] ([CHANGE_CLASS_NAME]) | checking pre_conditions"

  advance_file():
    file = next_file_in_topological_order()
    if no next file:
      advance_to_validation()
    X = 0, Y = 0, sequence = 1
    VIEWPORT_MANAGER.evict_file(completed_file)
    VIEWPORT_MANAGER.load_file(new_file)
    LOCK_TABLE.release(completed_file)
    LOCK_TABLE.acquire(new_file)
    emit: "→ FILE: [new_file] | lock acquired | viewport refreshed"

  advance_to_validation():
    MRO.lifecycle.phase = "VALIDATING"
    DIFF_ENGINE.run_full_pass()
    emit: "→ VALIDATION phase | all Z=5 nodes processed"

  mark_blocked(node, reason):
    node.cursor_blocked_reason = reason
    find next unblocked node
    emit: "⊘ M[[Z],[X],[Y]] seq=[N] BLOCKED: [reason]"

  resolve():
    return matrix.get_node(file=cursor.file, Z=5, X=cursor.X, Y=cursor.Y, seq=cursor.sequence)
    if pre_conditions_unsatisfied: mark_blocked()
```

---

## Viewport Manager

The Viewport Manager is the Memory Management Unit of the Matrix Driver.
It maps the matrix content onto the LLM's context window.

### Zone Controller

```
VIEWPORT_MANAGER:

  PERSISTENT_ZONE:                          ← never evicted, always in context
    capacity: 6000 tokens (max)
    contents:
      - condensed invariant table (Z=0, all INV-IDs + one-line rules)
      - active guide refs (Z=1, id + version + §-ref, no prose)
      - session meta: session_id, plan_id, budget_summary
      - MRO cursor position (always current)

    update_triggers:
      - guide supersession (Z=1 update)
      - invariant violation detected (Z=0 entry marked "VIOLATED")
      - budget percentage crosses threshold

  WORKING_ZONE:                             ← current execution context
    capacity: 20000 tokens (max)
    contents:
      - file aggregate (Z=3): all chain counts, pass status
      - pass descriptor (Z=4): name, order, cell list with progress
      - current node (Z=5): FULL detail (content, chains, pre/post conditions)
      - lookahead (Z=5): next 3 nodes in LITE form (id, target, pre_conditions only)
      - lookbehind (Z=5): prev 3 nodes in LITE form (id, status, post_check result)
      - active XFC chains: source node + unlock condition

    eviction_policy:
      - file boundary: evict completed file's Z=3,Z=4 entirely
      - pass boundary: evict completed pass Z=4 → compress to one line in Z=3
      - cell boundary: evict completed cell → compress to count in Z=4

  REFERENCE_ZONE:                           ← compressed, on-demand accessible
    capacity: 10000 tokens (max)
    contents:
      - completed cells: count per M[Z,X,Y] only
      - completed files: "[file] ✅ DONE | tasks=[N] | MSNAP=[id]"
      - pending XFC chains: xfc_id + source_file + status only
      - cross-volume status: one line per other volume

    access_protocol:
      - LLM may reference any entry by id
      - full detail: load from CHECKPOINT_MANAGER (not from context)
      - never load full detail into reference zone (defeats compression)
```

### Compression Trigger Protocol

```
CHECK_BUDGET():
  pct_remaining = budget.remaining / budget.total

  if pct_remaining > 0.70: return "LEVEL_0"  // normal, no action
  if pct_remaining > 0.30: return "LEVEL_1"  // compress
  if pct_remaining > 0.10: return "LEVEL_2"  // offload
  return "CRITICAL"                           // halt immediately

COMPRESS(to_level):

  LEVEL_1:
    // Fold completed cells in working zone
    for each completed cell C in working_zone:
      replace full node list with: "M[[Z],[X],[Y]]: ✅ [N]/[N]"
    // Fold completed passes in file aggregate
    for each completed pass P in Z=3 aggregate:
      replace pass descriptor with: "M[4,[X],[Y]] ✅ [N] tasks"
    emit: "COMPRESS L1 | freed ≈[N] tokens | budget now [%]"

  LEVEL_2:
    // Full file offload for completed files
    for each completed file F:
      CHECKPOINT_MANAGER.verify(MSNAP for F)  // must verify before evicting
      replace F context with: "[F] ✅ MSNAP=[id]"
    // Ultra-compress invariants
    persistent_zone.invariants = ultra_compress(invariants)
      // "INV-CSS-TOKENS:noAbbrev | INV-LAW0:noGetById"
    // Reduce lookahead to 1
    load_lookahead(CURSOR.next_nodes(1), mode="LITE")
    emit: "COMPRESS L2 | freed ≈[N] tokens | budget now [%]"

  CRITICAL:
    // Never call compress — HALT is the only valid action
    raise BUDGET_CRITICAL_FAULT
```

### Rehydration Protocol

```
REHYDRATE(snapshot_id):
  snap = CHECKPOINT_MANAGER.load(snapshot_id)

  // 1. Restore persistent zone
  persistent_zone.invariants = expand(snap.invariant_table_compressed)
  persistent_zone.guide_refs = expand(snap.guide_refs_compressed)
  persistent_zone.session_meta = snap.session_meta
  persistent_zone.cursor = snap.cursor

  // 2. Restore working zone
  working_zone.file_aggregate = matrix.get_node(snap.cursor.file, Z=3)
  working_zone.pass_descriptor = matrix.get_node(snap.cursor.file, Z=4,
                                                  X=snap.cursor.X, Y=snap.cursor.Y)
  current_node = matrix.get_node(snap.last_completed_node)
  next_node = matrix.get_node(snap.next_node)
  working_zone.current_node = next_node (full)
  working_zone.lookahead = CURSOR.next_nodes(3) (lite)
  working_zone.lookbehind = [current_node] + CURSOR.prev_nodes(2) (lite)

  // 3. Restore reference zone
  reference_zone.completed_cells = snap.cell_states
  reference_zone.completed_files = snap.completed_files_summary
  reference_zone.active_xfc = [xfc for xfc if xfc.state != "CONSUMED"]

  // 4. Verify file integrity
  actual_hash = sha256(read_file(snap.cursor.file))
  if actual_hash != snap.file_hash:
    HALT("FILE_MODIFIED_EXTERNALLY: [file] | expected=[snap.hash] | actual=[actual]")

  // 5. Restore MRO state
  MRO.cursor = snap.cursor
  MRO.cursor.state = "READY_TO_RESUME"
  MRO.lifecycle.last_checkpoint_id = snapshot_id
  MRO.coherence_state.invariant_snapshot = snap.global_invariant_status

  // 6. Emit navigation statement
  STATUS_EMITTER.emit_navigation()
  emit: "Context rehydrated ✓ | MSNAP=[id] | file=[file] | cursor=M[[Z],[X],[Y]] seq=[N] | resume: [next_node]"
```

---

## Chain Executor

The Chain Executor manages the execution semantics specific to each chain type.
It wraps the base AEP with chain-level commit logic.

### Horizontal Chain Executor

```
HORIZONTAL_CHAIN_EXECUTOR:

  on_chain_start(chain_id):
    chain = matrix.get_chain(chain_id)
    // pre-commit snapshot (for rollback to chain start)
    snap = CHECKPOINT_MANAGER.snapshot_file(chain.file, tag="CHAIN_START")
    MRO.lifecycle.rollback_target = snap.snapshot_id
    MRO.chain_state.horizontal.active_chain_id = chain_id
    MRO.chain_state.horizontal.pending_commit = true
    emit: "⛓ Chain start: [chain_id] | [N] nodes | rollback anchor: [snap_id]"

  on_node_complete(node):
    chain = matrix.get_chain_containing(node)
    chain.completed_count++
    // update Z=4 pass progress
    pass_node = matrix.get_pass_node(node.file, node.address.X, node.address.Y)
    pass_node.completed++
    // check if chain complete
    if chain.completed_count == chain.total_count:
      on_chain_complete(chain)

  on_chain_complete(chain):
    // CHAIN-LEVEL DIFF CHECK (not just per-node)
    diff = DIFF_ENGINE.check_chain(chain)
    if diff.regressions:
      ERROR_RECOVERY.handle_chain_regression(chain, diff)
      return

    // COMMIT
    MRO.chain_state.horizontal.pending_commit = false
    // update Z=4 pass node: status → DONE
    pass_node.status = "DONE"
    // check diagonal unlocks
    CHAIN_EXECUTOR.check_diagonal_unlocks(chain)
    // checkpoint at cell boundary
    snap = CHECKPOINT_MANAGER.save_cell_checkpoint(chain)
    emit: "✅ Chain done: [chain_id] | [N]/[N] | MSNAP=[snap_id]"

  check_diagonal_unlocks(chain):
    // after this chain completes, which diagonal targets are now unblocked?
    source_nodes = chain.all_nodes
    for each node N in source_nodes:
      for each edge E in N.diagonal:
        target = matrix.get_node(E.target)
        if all_pre_conditions_satisfied(target):
          target.cursor_blocked = false
          MRO.coherence_state.regression_flags.remove_if_present(E)
          emit: "↗ Diagonal unlock: [E.target] at M[[Z'],[X'],[Y']] — [reason]"
```

### Diagonal Chain Executor

```
DIAGONAL_CHAIN_EXECUTOR:

  on_diagonal_registration(source_node, target_node, edge_type):
    // Register in MRO.chain_state.diagonal.in_flight
    entry = {
      source: source_node.node_id,
      target: target_node.node_id,
      edge_type: edge_type,
      state: "WAITING_SOURCE"
    }
    MRO.chain_state.diagonal.in_flight.append(entry)
    emit: "↗ Diagonal registered: [source] → [target] | state: WAITING_SOURCE"

  on_source_node_chain_complete(source_chain):
    // Find all in-flight diagonals sourced from this chain
    in_flight = MRO.chain_state.diagonal.in_flight
    to_unlock = [D for D in in_flight if D.source in source_chain.node_ids]
    for D in to_unlock:
      D.state = "SOURCE_COMPLETE"
      target = matrix.get_node(D.target)
      // recheck: are ALL pre_conditions for target now satisfied?
      if all_pre_conditions_satisfied(target):
        D.state = "UNLOCKED"
        target.cursor_blocked = false
        emit: "↗ Diagonal UNLOCKED: [D.target] | all pre_conditions satisfied"
      else:
        remaining = unsatisfied_pre_conditions(target)
        emit: "↗ Diagonal PARTIAL: [D.target] | remaining pre_conditions: [remaining]"

  on_diagonal_target_complete(target_node):
    D = find_diagonal(target=target_node)
    D.state = "CONSUMED"
    MRO.chain_state.diagonal.in_flight.remove(D)
    emit: "↗ Diagonal consumed: [D.source] → [D.target] | DONE"
```

### Cross-File Chain Executor

```
CROSS_FILE_CHAIN_EXECUTOR:

  on_source_file_complete(file):
    // Find all XFC chains with this file as source
    xcfs = matrix.get_xfc_chains_sourced_from(file)
    for XFC in xcfs:
      // Unlock target file for processing
      MRO.chain_state.cross_file.pending_unlock.remove(XFC)
      // Notify Volume Coordinator (may be different plan's volume)
      VOLUME_COORDINATOR.unlock_target_file(XFC.target_file, triggered_by=XFC.xfc_id)
      emit: "⇒ XFC [XFC.xfc_id]: [file] → [XFC.target_file] UNLOCKED"

  on_target_file_ready(file, xfc_id):
    // Target file's pre_conditions now satisfied
    // Acquire lock and add to Traversal Engine queue
    LOCK_TABLE.acquire(file)
    TRAVERSAL_ENGINE.enqueue_file(file)
    emit: "⇒ XFC [xfc_id]: [file] queued for execution | lock acquired"
```

---

## Coherence Monitor

The Coherence Monitor is the background invariant watchdog.
It runs at every GATE node, every file boundary, and on demand.

### Monitor Protocol

```
COHERENCE_MONITOR:

  LEVELS:
    CONTINUOUS:    after every atomic node — lightweight invariant check (pattern count)
    FILE_BOUNDARY: after each file — full invariant scan for that file
    GATE:          at explicit GATE nodes — full global invariant check
    PLAN_BOUNDARY: after all files in plan — cross-file consistency check

  run_continuous(node):
    // Only check invariants referenced by this specific node
    for each invariant_id in node.post_conditions where type == INVARIANT_CHECK:
      inv = INVARIANT_REGISTRY.get(invariant_id)
      result = inv.check(file=node.file, scope="NODE_VICINITY")
      if result == "VIOLATED":
        COHERENCE_MONITOR.flag_violation(inv, node)
        return "VIOLATED"
    return "SATISFIED"

  run_file_boundary(file):
    // Full invariant scan for all invariants whose scope includes this file
    relevant_invs = INVARIANT_REGISTRY.get_for_file(file)
    violations = []
    for inv in relevant_invs:
      result = inv.check(file=file, scope="FULL_FILE")
      if result == "VIOLATED":
        violations.append({ inv: inv, file: file, result: result })
    if violations:
      emit_violation_report(violations)
      return "VIOLATED"
    // Update MRO coherence_state
    MRO.coherence_state.invariant_snapshot[inv.id] = "SATISFIED"
    emit: "COHERENCE ✓ [file] | [N] invariants checked | all satisfied"
    return "SATISFIED"

  run_gate_check():
    // Full global check across all files processed so far
    results = {}
    for inv in INVARIANT_REGISTRY.all_active():
      results[inv.id] = inv.check(scope="ALL_PROCESSED_FILES")
    MRO.coherence_state.gate_result = "PASS" if all SATISFIED else "FAIL"
    MRO.coherence_state.last_gate_check = NOW()
    // Check cross-plan consistency (no conflicting writes)
    cross_plan = VOLUME_COORDINATOR.check_consistency()
    // Check no orphaned locks
    orphans = LOCK_TABLE.find_orphans()
    if orphans:
      results["LOCK_ORPHAN"] = "VIOLATED"
    emit_gate_report(results)
    return MRO.coherence_state.gate_result

  flag_violation(inv, node):
    MRO.coherence_state.invariant_snapshot[inv.id] = "VIOLATED"
    MRO.coherence_state.regression_flags.append({
      invariant: inv.id, node: node.node_id, severity: inv.severity
    })
    if inv.severity == "CRITICAL":
      TRAVERSAL_ENGINE.halt("CRITICAL_INVARIANT_VIOLATED")
    else:
      emit: "⚠ COHERENCE WARNING: [inv.id] | node=[node_id] | severity=[inv.severity]"
```

---

## Diff Engine

The Diff Engine computes the structural delta between expected and actual matrix state.
It runs continuously, not just at validation — regressions are caught as they occur.

### Engine Components

```
DIFF_ENGINE:

  EXPECTED_STATE_TRACKER:
    Populated during Phase B (node creation).
    For each cell M[Z,X,Y] in each file:
      expected_removals[cell] = [node.content.target for node in cell]
      expected_additions[cell] = [node.content.replacement for node in cell]
      expected_node_count[cell] = len(cell.nodes)

  ACTUAL_STATE_SCANNER:
    After each chain completion: grep-scan the file for expected patterns.
    Input: file, cell, expected_removals[], expected_additions[]
    Output: diff_result{
      missing_removals: [patterns still present],
      missing_additions: [patterns not yet present],
      contaminations:   [unexpected patterns in wrong cells],
      counts: { removed: N, added: N, contaminated: N }
    }

  REGRESSION_CLASSIFIER:
    Classifies diff_result into one of four regression types (see Matrix §Diff):
      TYPE_1: missing_removals is non-empty → MISSING_REPLACEMENT
      TYPE_2: missing_additions is non-empty OR count mismatch → CORRUPTED_REPLACEMENT
      TYPE_3: contaminations is non-empty → CROSS_CELL_CONTAMINATION
      TYPE_4: diagonal consumer has wrong pre_condition state → DIAGONAL_BREAKAGE

  RECOVERY_SUGGESTER:
    For each regression:
      TYPE_1: find missed instances, generate new atomic nodes, add to chain tail
      TYPE_2: generate rollback + corrected replacement node
      TYPE_3: generate rollback of contaminating operation + narrowed pattern
      TYPE_4: mark consumer node REWORK, regenerate pre_condition check
```

### Diff Run Protocol

```
DIFF_ENGINE.check_chain(chain):

  // 1. Scan all patterns from completed chain
  removals_found = { p: grep(p, chain.file, count=True) for p in expected_removals[chain.cell] }
  additions_found = { p: grep(p, chain.file, count=True) for p in expected_additions[chain.cell] }

  // 2. Classify
  missing_removals  = [p for p, count in removals_found  if count != 0]
  missing_additions = [p for p, count in additions_found if count == 0]
  contaminations    = check_contamination(chain)  // look for expected removals in OTHER cells

  // 3. Diagonal check
  diagonal_breaks = []
  for each node N in chain.nodes where N.diagonal is not empty:
    for edge E in N.diagonal:
      target = matrix.get_node(E.target)
      if not all_pre_conditions_from_this_chain_satisfied(target):
        diagonal_breaks.append((N, target))

  // 4. Build result
  result = DiffResult(
    chain_id=chain.chain_id,
    missing_removals=missing_removals,
    missing_additions=missing_additions,
    contaminations=contaminations,
    diagonal_breaks=diagonal_breaks,
    regression_types=REGRESSION_CLASSIFIER.classify(result)
  )

  // 5. Report
  if result.is_clean():
    emit: "DIFF ✓ chain=[chain_id] | removals=[N]/[N] | additions=[N]/[N] | clean"
  else:
    emit_regression_report(result)
    ERROR_RECOVERY.handle_chain_regression(chain, result)

  return result
```

---

## Reshape Handler

The Reshape Handler manages the most disruptive operation: a new guide arrives
while the Traversal Engine is executing. The handler must halt cleanly,
integrate the guide into the matrix structure, and resume without data loss.

### Reshape State Machine

```
IDLE
  │  (guide_loaded event from Driver GUIDE_REG)
  ▼
RESHAPE_TRIGGERED
  │  Step 1: signal Traversal Engine
  ▼
WAITING_ATOMIC_BOUNDARY    ← cannot interrupt mid-operation
  │  (current AEP completes — PASS or FAIL)
  ▼
HALTED_AT_BOUNDARY
  │  Step 2: emergency snapshot
  ▼
SNAPSHOTTED
  │  Step 3: update Z=0, Z=1 layers
  ▼
Z_LAYERS_UPDATED
  │  Step 4: cascade to affected volumes
  ▼
CASCADE_COMPLETE
  │  Step 5: rework non-conforming PENDING nodes
  ▼
NODES_REWORKED
  │  Step 6: generate new nodes (if guide adds requirements)
  ▼
NEW_NODES_INTEGRATED
  │  Step 7: re-run integrity check on affected chains
  ▼
INTEGRITY_VERIFIED
  │  Step 8: resume Traversal Engine
  ▼
IDLE
```

### Reshape Handler Protocol

```
RESHAPE_HANDLER.handle(new_guide):

  // STEP 1 — Signal
  TRAVERSAL_ENGINE.set_flag(HALT_AT_NEXT_ATOMIC_BOUNDARY)
  reshape_start_node = CURSOR.current_node_id
  emit: "RESHAPE: new guide [new_guide.id] | halting at next atomic boundary"

  // STEP 2 — Snapshot (after Traversal Engine confirms halt)
  snap = CHECKPOINT_MANAGER.save(tag="RESHAPE_PRE", note=new_guide.guide_id)
  MRO.lifecycle.rollback_target = snap.snapshot_id

  // STEP 3 — Z-layer update
  old_guide = GUIDE_REG.get_active_for_family(new_guide.guide_family)
  if old_guide:
    old_guide.status = "SUPERSEDED"
    // find Z=1 nodes pointing to old guide → update to new guide
    z1_nodes_to_update = matrix.find_z1_nodes(guide_id=old_guide.guide_id)
    for z1_node in z1_nodes_to_update:
      z1_node.guide_ref = new_guide.guide_id
      z1_node.version = new_guide.version
  // register new guide's invariants in Z=0
  for inv in new_guide.invariants:
    if not INVARIANT_REGISTRY.exists(inv.id):
      INVARIANT_REGISTRY.register(inv)
      matrix.create_z0_node(inv)
    else:
      INVARIANT_REGISTRY.update(inv)
      matrix.update_z0_node(inv)
  emit: "RESHAPE: Z=0,Z=1 updated | old guide superseded | [N] invariants registered/updated"

  // STEP 4 — Cascade to affected volumes
  affected_volumes = VOLUME_COORDINATOR.find_volumes_affected_by(new_guide)
  for vol in affected_volumes:
    // Re-derive post_conditions for all PENDING Z=5 nodes
    pending_nodes = matrix.get_all_nodes(volume=vol, Z=5, status="PENDING")
    for node in pending_nodes:
      new_post = derive_post_conditions(node.content, new_guide)
      if new_post != node.post_conditions:
        node.post_conditions = new_post
        node.reshape_flag = "POST_CONDITIONS_UPDATED"
    emit: "RESHAPE cascade: VOL-[vol.id] | [N] pending nodes re-derived"

  // STEP 5 — Rework non-conforming PENDING nodes
  non_conforming = []
  for vol in affected_volumes:
    pending_nodes = matrix.get_all_nodes(volume=vol, Z=5, status="PENDING")
    for node in pending_nodes:
      inv_check = INVARIANT_REGISTRY.check_node_conformance(node, new_guide)
      if not inv_check.conforms:
        non_conforming.append((node, inv_check.canonical_value))
  for (node, canonical) in non_conforming:
    node.content.replacement = canonical
    // update post_conditions for new replacement
    node.post_conditions = derive_post_conditions(node.content, new_guide)
    // update diagonal edges: any consumer expecting old value must be updated
    for edge in node.diagonal:
      target = matrix.get_node(edge.target)
      update_consumer_pre_conditions(target, old_value=node.content.replacement_old,
                                              new_value=canonical)
  emit: "RESHAPE rework: [N] nodes corrected | canonical value from [new_guide.invariant_id]"

  // STEP 6 — DONE nodes that now violate invariant
  done_nodes_violated = []
  for vol in affected_volumes:
    done_nodes = matrix.get_all_nodes(volume=vol, Z=5, status="DONE")
    for node in done_nodes:
      inv_check = INVARIANT_REGISTRY.check_result_conformance(node, new_guide)
      if not inv_check.conforms:
        done_nodes_violated.append(node)
  if done_nodes_violated:
    emit: "RESHAPE: [N] DONE nodes now violate new guide | generating remediation tasks"
    for node in done_nodes_violated:
      remediation_node = create_remediation_node(node, new_guide)
      matrix.insert_node(remediation_node, after=CURSOR.current_node)
    emit: "RESHAPE: [N] remediation nodes injected into chain"

  // STEP 7 — Integrity re-check on affected chains
  for vol in affected_volumes:
    POPULATION_ENGINE.run_integrity_check(volume=vol, scope="PENDING_ONLY")

  // STEP 8 — Resume
  TRAVERSAL_ENGINE.clear_flag(HALT_AT_NEXT_ATOMIC_BOUNDARY)
  CHECKPOINT_MANAGER.load(snap.snapshot_id)  // restore viewport to pre-reshape state
  MRO.lifecycle.phase = "EXECUTION"
  STATUS_EMITTER.emit_navigation()
  emit: "RESHAPE complete ✓ | guide=[new_guide.id] | reworked=[N] | remediation=[N] | resume: [cursor.node_id]"
```

---

## Checkpoint Manager

The Checkpoint Manager is the journaling filesystem of the Matrix Driver.
Every snapshot is verified before it is trusted for rollback.

### Snapshot Types

```
SNAPSHOT TYPES (triggers and contents):

  NODE_CHECKPOINT:
    trigger: node.checkpoint_after == true AND node.status → DONE
    contents: MRO.cursor, node result, file hash, chain progress
    size: minimal (cursor + hash + result)

  CELL_CHECKPOINT:
    trigger: horizontal chain completes (all nodes in M[Z,X,Y] DONE)
    contents: full cell state, diff result, invariant snapshot for this file
    size: medium

  FILE_CHECKPOINT (= MSNAP):
    trigger: file boundary (before and after)
    contents: full layer snapshot per §Matrix §Layer Snapshot structure
    size: full

  GATE_CHECKPOINT:
    trigger: GATE node — after coherence check PASS
    contents: coherence_state, invariant_snapshot for all processed files, lock table
    size: medium + invariants

  RESHAPE_CHECKPOINT:
    trigger: Reshape Handler step 2
    tag: "RESHAPE_PRE"
    contents: everything (full MRO + viewport state + all active chains)
    size: large

  EMERGENCY_CHECKPOINT:
    trigger: budget CRITICAL
    tag: "BUDGET_CRITICAL"
    contents: minimal (cursor position + next node + file hash + plan progress)
    size: minimal
    purpose: only to enable session resume
```

### Save Protocol

```
CHECKPOINT_MANAGER.save(snapshot_type, node_id=None, tag=None):

  snap_id = "MSNAP-[PLAN]-[file_abbrev]-Z[N]-[seq:03d]-[type_abbrev]"
  snap = {
    "snapshot_id":    snap_id,
    "type":           snapshot_type,
    "plan_id":        MRO.plan_id,
    "cursor":         copy(MRO.cursor),
    "file_hash":      sha256(read_file(MRO.cursor.file)),
    "timestamp":      NOW(),
    "tag":            tag,
    "layer_state":    serialize_layer_state(),
    "invariant_snapshot": copy(MRO.coherence_state.invariant_snapshot),
    "context_budget": copy(MRO.viewport.budget)
  }

  // TYPE-SPECIFIC ADDITIONS
  if snapshot_type in [FILE_CHECKPOINT, RESHAPE_CHECKPOINT]:
    snap["cell_states"] = { M[Z,X,Y]: { done, total } for each cell }
    snap["active_xfc"]  = [xfc for xfc in chain_state.cross_file.pending_unlock]
    snap["active_diagonal"] = [d for d in chain_state.diagonal.in_flight]

  // VERIFY BEFORE STORING
  verify_result = verify_snapshot(snap)
  if not verify_result.valid:
    HALT("SNAPSHOT_CORRUPT: [snap_id] | [verify_result.reason]")

  CHECKPOINT_STORE[snap_id] = snap
  MRO.lifecycle.last_checkpoint_id = snap_id
  return snap

VERIFY_SNAPSHOT(snap):
  // File hash must match actual file
  actual_hash = sha256(read_file(snap.cursor.file))
  if actual_hash != snap.file_hash:
    return VerifyResult(valid=False, reason="FILE_HASH_MISMATCH")
  // Cursor must point to valid node
  node = matrix.get_node(snap.cursor.node_id)
  if node is None:
    return VerifyResult(valid=False, reason="CURSOR_NODE_NOT_FOUND")
  // Layer state must be internally consistent
  for cell, state in snap.cell_states.items():
    if state.done > state.total:
      return VerifyResult(valid=False, reason=f"DONE_EXCEEDS_TOTAL at {cell}")
  return VerifyResult(valid=True)
```

### Rollback Protocol

```
CHECKPOINT_MANAGER.rollback(to_snapshot_id, reason):

  snap = CHECKPOINT_STORE[to_snapshot_id]

  // 1. Restore file to snapshot state
  restore_file(snap.cursor.file, from_hash=snap.file_hash)
  verify_restore: sha256(file) == snap.file_hash
  if not verified: HALT("RESTORE_FAILED: file hash mismatch after restore")

  // 2. Restore MRO cursor
  MRO.cursor = copy(snap.cursor)
  MRO.cursor.state = "PENDING"

  // 3. Reset node statuses in matrix (from snap.cursor back to now)
  rolled_back_nodes = matrix.get_nodes_after(snap.cursor, status_filter=["DONE","FAILED"])
  for node in rolled_back_nodes:
    node.status = "PENDING"
    node.atomic_check = {}

  // 4. Reset chain states
  MRO.chain_state.horizontal.pending_commit = false
  for d in MRO.chain_state.diagonal.in_flight:
    if d.state == "UNLOCKED":
      d.state = "WAITING_SOURCE"  // re-lock

  // 5. Restore viewport
  VIEWPORT_MANAGER.rehydrate(to_snapshot_id)

  // 6. Report
  emit: "ROLLBACK ✓ | to=[to_snapshot_id] | reason=[reason]
         | nodes_reset=[N] | file restored | cursor at M[[Z],[X],[Y]] seq=[N]"
```

---

## Volume Coordinator

The Volume Coordinator manages inter-volume interactions
when multiple plans operate simultaneously in the same session.

### Coordinator Protocol

```
VOLUME_COORDINATOR:

  REGISTRY: { vol_id → MRO }  // all active MROs in this session

  register_volume(mro):
    REGISTRY[mro.volume_id] = mro
    emit: "VOLUME registered: [mro.volume_id] | plan=[mro.plan_id]"

  check_consistency():
    // After each file completes in any volume:
    // Check that no two volumes wrote conflicting content to the same patterns

    all_completed_files = [file for vol in REGISTRY for file in vol.completed_files]
    conflicts = []
    for file in all_completed_files:
      // Which volumes touched this file?
      touching_volumes = [vol for vol in REGISTRY if file in vol.scope.files]
      if len(touching_volumes) > 1:
        // Scan for pattern conflicts
        for P in common_patterns_between(touching_volumes, file):
          values = [vol.get_replacement_for(P, file) for vol in touching_volumes]
          if len(set(values)) > 1:  // different values for same pattern
            conflicts.append({ pattern: P, file: file, values: values })
    if conflicts:
      emit_conflict_report(conflicts)
      return "CONFLICT_DETECTED"
    return "CONSISTENT"

  unlock_target_file(file, triggered_by):
    // Called by Cross-File Chain Executor
    target_vol = find_volume_owning(file)
    target_mro = REGISTRY[target_vol.volume_id]
    target_mro.chain_state.cross_file.pending_unlock = [
      xfc for xfc in target_mro.chain_state.cross_file.pending_unlock
      if xfc.xfc_id != triggered_by
    ]
    emit: "VOLUME: [target_vol.volume_id] file [file] unlocked by XFC [triggered_by]"

  find_volumes_affected_by(guide):
    // Used by Reshape Handler
    affected = []
    for vol_id, mro in REGISTRY.items():
      vol_files = mro.volume.file_set
      guide_patterns = guide.applies_to_patterns
      if any_file_matches_patterns(vol_files, guide_patterns):
        affected.append(mro)
    return affected

  parallel_execution_allowed(vol_A, vol_B):
    // Can two volumes execute simultaneously?
    if vol_A.volume.overlap_with[vol_B.volume_id].type == "OVERLAPPING":
      return False  // conflict state — never parallel
    if vol_A.volume.overlap_with[vol_B.volume_id].type == "ADJACENT":
      return False  // same files — lock contention
    return True     // DISJOINT — parallel OK
```

---

## Error Recovery

The Error Recovery subsystem handles failures at node, chain, and system levels.

### Failure Classification

```
FAILURE_CLASSIFICATION:

  NODE_FAILURE (AEP step ③ fails):
    RETRYABLE:
      - WRONG_ORDER: replacement order caused substring collision
        → fix: reorder chain (longest first) and retry
      - STALE_LOCATION: line numbers changed due to earlier operations
        → fix: re-scan file for target, update location, retry
      - PATTERN_MISMATCH: grep found different count than expected pre_condition
        → fix: re-scan, update pre_condition count, retry
      max retries: 2

    STRUCTURAL (requires rework, cannot retry as-is):
      - INVARIANT_VIOLATED: replacement itself violates Z=0 invariant
        → fix: rework replacement content, update matrix node, restart
      - CANONICAL_MISMATCH: replacement conflicts with Z=0 guide canonical value
        → fix: correct replacement to canonical, restart
      - DIAGONAL_CONTRADICTION: operation conflicts with a diagonal pre_condition
        → fix: re-order chain to satisfy diagonal dependency, restart

    UNRECOVERABLE (halt plan):
      - FILE_CORRUPT: file hash changed unexpectedly mid-execution
      - LOCK_STOLEN: another process modified a locked file
      - INVARIANT_UNREACHABLE: no valid replacement exists that satisfies all invariants

  CHAIN_FAILURE (diff engine detects regression after chain complete):
    REGRESSION_TYPE_1 (missing removal):
      → generate additional nodes for missed instances
      → append to chain tail (new nodes, same cell)
      → MRO: chain.status → REQUIRES_CONTINUATION
      → re-execute continuation

    REGRESSION_TYPE_2 (corrupted replacement):
      → rollback chain to CHAIN_START snapshot
      → analyze: which node caused corruption?
      → fix: node content (pattern, replacement, or line range)
      → re-execute chain from start

    REGRESSION_TYPE_3 (cross-cell contamination):
      → rollback contaminating node only
      → narrow its pattern (add anchors: ^ or -- or .)
      → re-execute narrowed node
      → verify: no longer contaminates adjacent cell

    REGRESSION_TYPE_4 (diagonal breakage):
      → mark broken diagonal target as REWORK
      → re-insert into chain at correct position (after source chain)
      → re-execute

  SYSTEM_FAILURE (Coherence Monitor gate check fails):
    → halt ALL volumes
    → emit full gate report
    → require human review before any resume
    → preserve all MRO states and snapshots
```

### Recovery Protocol

```
ERROR_RECOVERY.handle_node_failure(node, exec_result):

  failure_class = FAILURE_CLASSIFICATION.classify(exec_result)

  if failure_class == "RETRYABLE":
    node.retry_count++
    if node.retry_count > MAX_RETRIES:
      failure_class = "STRUCTURAL"
    else:
      fix = generate_fix(failure_class, exec_result)
      apply_fix(node, fix)
      CHECKPOINT_MANAGER.rollback(to=MRO.lifecycle.rollback_target)
      emit: "RETRY [node.node_id] | attempt [node.retry_count] | fix=[fix.type]"
      // Traversal Engine will re-execute this node
      return

  if failure_class == "STRUCTURAL":
    reworked_node = rework_node(node, exec_result)
    matrix.replace_node(node, reworked_node)
    CHECKPOINT_MANAGER.rollback(to=MRO.lifecycle.rollback_target)
    emit: "REWORK [node.node_id] | reworked content: [reworked_node.content.replacement]"
    return

  if failure_class == "UNRECOVERABLE":
    MRO.lifecycle.phase = "HALTED"
    emit: "HALT [node.node_id] | UNRECOVERABLE: [exec_result.reason]
           | snapshot=[MRO.lifecycle.last_checkpoint_id] | requires human review"
```

---

## Status Emitter

The Status Emitter produces all human-readable output from the Matrix Driver.
It is the single output channel — nothing else writes to the LLM output.

### Emission Types

```
STATUS_EMITTER.emit_navigation():
  Output format (emitted at every file/pass boundary and on resume):

  ┌─────────────────────────────────────────────────────────────────┐
  │ MATRIX NAVIGATION                                               │
  │   Volume:    VOL-P001 | PLAN-001                                │
  │   File:      messages.html                                      │
  │   Layer:     Z=5 (ATOMIC)                                       │
  │   Cell:      M[5,0,0] STRUCTURAL·TOKEN                          │
  │   Position:  node 14/22 in chain HCHAIN-...-5-0-0              │
  │   X-status:  X=0 in progress | X=1 BLOCKED (awaiting X=0)      │
  │   Done:      M[5,0,1]CLASS ✅ | M[5,0,2]KFR ✅                  │
  │   Blocked:   M[5,0,3]ATTR ░ (awaiting M[5,0,0] chain complete) │
  │   Diagonal:  upon M[5,0,0] completion → unlock M[5,0,3](8)     │
  │   Budget:    47% remaining | level: 0 (normal)                  │
  │   Next:      MN-...-5-0-0-015 | target: --msg-avatar-size       │
  └─────────────────────────────────────────────────────────────────┘

STATUS_EMITTER.emit_node_result(node, result):
  // Compact, inline, one line
  "  [result_icon] T[seq] M[[Z],[X],[Y]] | [target] → [replacement] | [check_summary]"
  //  ✅ T014 M[5,0,0] | --msg-bubble-radius → --messages-bubble-radius | grep:0 ✓ inv:✓
  //  ❌ T015 M[5,0,0] | --msg-avatar-size → ... | grep:2 ✗ (expected 0)

STATUS_EMITTER.emit_chain_complete(chain, diff):
  "  ✅ Chain M[5,[X],[Y]] [N]/[N] | diff:clean | MSNAP=[snap_id] | → [next_cell_label]"

STATUS_EMITTER.emit_file_complete(file, validation_result):
  "  ✅ FILE [file] | tasks=[N]/[N] | inv:[N]✓ | lock released | → [next_file]"
  OR
  "  ❌ FILE [file] | regression: [type] | rollback to [snap_id] | [detail]"

STATUS_EMITTER.emit_resume_prompt():
  Output format (on budget critical — new session entry point):

  ╔══════════════════════════════════════════════════════════════════╗
  ║ CONTEXT BUDGET CRITICAL — SESSION CHECKPOINT SAVED              ║
  ║                                                                  ║
  ║ Snapshot:    MSNAP-P001-F01-Z5-042-BUDGET                       ║
  ║ Volume:      VOL-P001 | PLAN-001                                 ║
  ║ File:        messages.html                                       ║
  ║ Cell:        M[5,0,0] STRUCTURAL·TOKEN                           ║
  ║ Position:    node 42/84 in plan | 22/22 in current chain        ║
  ║                                                                  ║
  ║ Active guides:  arch-containerization-6 (v6.0.0)                ║
  ║                 spec-css-naming (v2.1.0)                        ║
  ║                                                                  ║
  ║ Next operation: MN-P001-messages.html-5-0-0-023                 ║
  ║   type: RENAME | target: --msg-thread-bg | line: 118            ║
  ║                                                                  ║
  ║ Remaining: M[5,0,0] 0 nodes | M[5,0,3] 8 nodes | M[5,1,6] 3   ║
  ║                                                                  ║
  ║ To resume: load MSNAP above → verify file hash → continue       ║
  ╚══════════════════════════════════════════════════════════════════╝
```

---

## Integration Bridge

The Integration Bridge connects the Matrix Driver to the base Driver,
maintaining the contract between the two systems.

### Contract Points

```
BASE_DRIVER provides to MATRIX_DRIVER:

  GUIDE_REG → MATRIX_DRIVER.POPULATION_ENGINE uses it for:
    - Z=0 invariant source (guide.invariants → M[0,X,Y] nodes)
    - Z=1 system reference source (guide.specs → M[1,X,Y] nodes)
    - Reshape events (guide supersession → RESHAPE_HANDLER)

  PLAN_REG → MATRIX_DRIVER uses it for:
    - MRO creation (one MRO per plan)
    - Conflict group info → VOLUME_COORDINATOR
    - File scope → Population Engine Phase A scaffold

  LOCK_TABLE → MATRIX_DRIVER uses it for:
    - File lock acquisition (CURSOR.advance_file)
    - Cross-file chain unlock (XFC Executor)
    - Deadlock prevention (alphabetical lock order)

  TASK_REG ← MATRIX_DRIVER writes to it:
    - Each Z=5 matrix node → registered as TEN in TASK_REG
    - node.status updates propagate both ways

  CHECKPOINT_STORE → shared:
    - MATRIX_DRIVER snapshots stored in same CHECKPOINT_STORE
    - MSNAP ids are valid entries in CHECKPOINT_STORE

MATRIX_DRIVER provides to BASE_DRIVER:

  Validation Level 1 (atomic):
    DIFF_ENGINE.check_chain result → node.atomic_check field

  Validation Level 2 (file):
    COHERENCE_MONITOR.run_file_boundary → plan file completion status

  Validation Level 3 (plan):
    VOLUME completion → PCD.progress.done updated

  Validation Level 4 (system):
    VOLUME_COORDINATOR.check_consistency → GLOBAL_VALIDATION

  Gate results:
    COHERENCE_MONITOR.run_gate_check → GATE node PASS/FAIL → Traversal Engine

  Context snapshot:
    MRO viewport state → Driver CTX snapshot content
```

### Bridge Sync Protocol

```
INTEGRATION_BRIDGE.sync_on_node_complete(node, result):
  // After each ATOMIC node:
  TASK_REG[node.node_id].status = node.status
  TASK_REG[node.node_id].atomic_check = node.atomic_check
  PCD.progress.done += 1 if result == "PASS" else 0
  PCD.progress.failed += 1 if result == "FAIL" else 0
  PCD.last_checkpoint = CHECKPOINT_MANAGER.last_snap_id
  PCD.context_snapshot_id = MRO.lifecycle.last_checkpoint_id

INTEGRATION_BRIDGE.sync_on_file_complete(file, coherence_result):
  // After each file:
  PCD.scope.files.mark_complete(file)
  if coherence_result == "VIOLATED":
    PCD.status = "BLOCKED"
    BASE_DRIVER.gate_fail(reason="COHERENCE_VIOLATION", file=file)

INTEGRATION_BRIDGE.sync_on_volume_complete(mro):
  // After all files in plan:
  PCD.status = "VALIDATING"
  validation = DIFF_ENGINE.run_full_pass(scope="ALL_FILES")
  if validation.clean:
    PCD.status = "DONE"
    BASE_DRIVER.plan_complete(mro.plan_id)
    VOLUME_COORDINATOR.unlock_dependent_volumes(mro.plan_id)
  else:
    PCD.status = "FAILED"
    BASE_DRIVER.plan_failed(mro.plan_id, reason=validation.regressions)
```

---

## Full Lifecycle: Matrix Driver Boot to Completion

The complete operational sequence for one volume, from boot to done:

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  MATRIX DRIVER — FULL LIFECYCLE (VOL-P001)                               ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  BOOT                                                                     ║
║    ├─ POPULATION_ENGINE receives: plan_id, file_set, guide_registry      ║
║    ├─ Phase A: scaffold Z=2,3,4 → "scaffold complete: 2 files, 5 passes" ║
║    ├─ Phase B: nodes from analysis_findings → "84 nodes created"         ║
║    ├─ Phase C: horizontal chains → "5 chains | order verified"           ║
║    ├─ Phase D: diagonal discovery → "8 intra + 3 cross-file chains"      ║
║    └─ Phase E: integrity check → "all 7 checks PASSED ✓"                ║
║                                                                           ║
║  MRO CREATED                                                              ║
║    ├─ cursor: M[5,0,0] seq=1 | state: READY                              ║
║    ├─ viewport: persistent zone loaded (Z=0 condensed, Z=1 refs)         ║
║    ├─ chain_state: HCHAIN-5-0-0 pending_commit=false                     ║
║    └─ coherence_state: invariants PENDING (not yet checked)              ║
║                                                                           ║
║  TRAVERSAL ENGINE STARTS                                                  ║
║    ├─ STATUS_EMITTER.emit_navigation()                                    ║
║    ├─ LOCK_TABLE.acquire(messages.html)                                  ║
║    ├─ CHAIN_EXECUTOR.on_chain_start(HCHAIN-5-0-0)                        ║
║    │   └─ CHECKPOINT_MANAGER.save(CHAIN_START) → MSNAP-P001-F01-Z5-000  ║
║    │                                                                      ║
║    ├─ [nodes 1–22: M[5,0,0] TOKEN chain]                                 ║
║    │   ├─ per node: VIEWPORT_MANAGER.load → AEP → DIFF_ENGINE.record    ║
║    │   ├─ per node: COHERENCE_MONITOR.run_continuous                     ║
║    │   ├─ per node: CHAIN_EXECUTOR.on_node_complete                      ║
║    │   └─ CHAIN_EXECUTOR.on_chain_complete → diagonal unlock M[5,0,3]   ║
║    │                                                                      ║
║    ├─ [nodes 23–44: M[5,0,1] CLASS chain]                                ║
║    │   └─ (same per-node loop)                                           ║
║    │                                                                      ║
║    ├─ [GATE node: post-X=0 coherence check]                              ║
║    │   ├─ COHERENCE_MONITOR.run_gate_check() → PASS                     ║
║    │   └─ CHECKPOINT_MANAGER.save(GATE) → MSNAP-P001-F01-Z5-044-GATE   ║
║    │                                                                      ║
║    ├─ [nodes 45–52: M[5,0,3] ATTR chain] ← unlocked by diagonal        ║
║    │                                                                      ║
║    ├─ [nodes 53–55: M[5,1,6] BEHAVIORAL chain]                           ║
║    │   └─ semantic check: data-widget attr confirmed in M[5,0,3] ✓      ║
║    │                                                                      ║
║    ├─ [FILE BOUNDARY: messages.html complete]                             ║
║    │   ├─ DIFF_ENGINE.run_full_pass(file=messages.html)                  ║
║    │   ├─ COHERENCE_MONITOR.run_file_boundary(messages.html) → PASS     ║
║    │   ├─ CHECKPOINT_MANAGER.save(FILE) → MSNAP-P001-F01-Z5-055-FILE   ║
║    │   ├─ LOCK_TABLE.release(messages.html)                              ║
║    │   ├─ XFC_EXECUTOR.on_source_file_complete(messages.html)            ║
║    │   │   └─ → messages.css UNLOCKED                                   ║
║    │   ├─ VIEWPORT_MANAGER.evict_file(messages.html)                     ║
║    │   └─ STATUS_EMITTER.emit_file_complete(messages.html, PASS)        ║
║    │                                                                      ║
║    ├─ [messages.css: 29 nodes, same loop]                                ║
║    │                                                                      ║
║    └─ [ALL FILES COMPLETE → VALIDATING]                                  ║
║                                                                           ║
║  VALIDATION                                                               ║
║    ├─ DIFF_ENGINE.run_full_pass(scope=ALL_FILES) → clean                 ║
║    ├─ COHERENCE_MONITOR.run_gate_check(scope=PLAN) → PASS               ║
║    ├─ VOLUME_COORDINATOR.check_consistency() → CONSISTENT               ║
║    └─ INTEGRATION_BRIDGE.sync_on_volume_complete(MRO)                    ║
║        └─ BASE_DRIVER.plan_complete(PLAN-001) → PLAN-002 UNBLOCKED      ║
║                                                                           ║
║  MRO FINAL STATE                                                          ║
║    cursor: END_OF_VOLUME | state: DONE                                   ║
║    progress: 84/84 | failed: 0 | rollbacks: 0                           ║
║    snapshots: 23 saved | 23 verified | 0 corrupted                       ║
║    coherence: all invariants SATISFIED                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## Anti-Patterns (Matrix Driver Level)

### ❌ Traversal Engine Started Before Integrity Check

```
Bad:  Population Engine completes Phase B → Traversal Engine starts immediately
Good: Population Engine must complete Phases C, D, and E (integrity check)
      before Traversal Engine starts.
      A node without horizontal links or with broken vertical chains
      will fail in ways that are impossible to diagnose during execution.
```

### ❌ Viewport Loaded Without Budget Check

```
Bad:  Load full node into working zone → only then check budget
Good: Check budget BEFORE loading any node.
      Loading a large node on a 5% remaining budget will trigger critical halt
      mid-operation, which produces an incomplete viewport snapshot.
```

### ❌ Chain Committed Without Diff Check

```
Bad:  All nodes in chain → DONE → commit immediately
Good: All nodes in chain → DONE → DIFF_ENGINE.check_chain → only then commit.
      "DONE" means the operations ran. It does not mean the operations produced
      correct results. The diff check is what determines correctness.
```

### ❌ Rollback Without Snapshot Verification

```
Bad:  Failure detected → CHECKPOINT_MANAGER.rollback(last_snapshot)
Good: CHECKPOINT_MANAGER.load(snap) → VERIFY_SNAPSHOT → rollback only if verified.
      An unverified snapshot may itself be in a corrupted state.
      Rolling back to corruption compounds the failure.
```

### ❌ Reshape Without Atomic Boundary Wait

```
Bad:  New guide arrives → immediately update Z=0 → cascade to EXECUTING node
Good: Set HALT_AT_NEXT_ATOMIC_BOUNDARY flag.
      Wait for current AEP to complete.
      Only then begin reshape.
      A reshape mid-AEP leaves the node in an undefined state:
      pre_conditions were from old guide, post_conditions now from new guide.
```

### ❌ Cross-File Chain Without Lock Order Enforcement

```
Bad:  XFC source file: wallet.css | target file: messages.css
      Lock acquired: messages.css first (because it was ready)
Good: Always acquire locks in alphabetical order: messages.css, wallet.css
      (regardless of which file is source and which is target).
      Non-alphabetical lock acquisition can cause deadlock with another
      volume acquiring the same pair in opposite order.
```

### ❌ Coherence Monitor Run Only at Plan End

```
Bad:  Run coherence check only at Phase 5 (final validation)
Good: CONTINUOUS after each atomic node (lightweight)
      FILE_BOUNDARY after each file (full file scan)
      GATE at explicit gate nodes (global scan)
      Discovering an invariant violation at plan end means
      up to 80+ nodes of work may need to be rolled back.
      Continuous monitoring catches violations at 1-node scope.
```

### ❌ Volume Coordinator Bypassed for Same-Session Volumes

```
Bad:  PLAN-001 and PLAN-002 run in same session, each manages its own locks
      independently without Volume Coordinator
Good: All lock acquisitions, XFC unlocks, and parallel-execution decisions
      route through VOLUME_COORDINATOR.
      Two volumes independently deciding they can both lock the same file
      is a race condition that produces silent corruption.
```

---

## Operational Checklists

### Matrix Driver Boot Checklist

```
□ Base Driver's GUIDE_REG has Z=0 and Z=1 populated (guides loaded before Matrix Driver boot)?
□ Population Engine Phase A (scaffold) complete before Phase B starts?
□ Population Engine Phase E (integrity check) PASSED before MRO transitions to READY?
□ MRO cursor correctly positioned at first Z=5 node (not null)?
□ Viewport persistent zone loaded (Z=0 condensed, Z=1 refs, session meta)?
□ Context budget initialized with correct critical_reserve?
□ Volume registered with Volume Coordinator?
□ All cross-file chains registered in chain_state.cross_file.pending_unlock?
□ Traversal Engine HALT flag clear (not carrying over from previous volume)?
□ CHECKPOINT_MANAGER has CHAIN_START snapshot before first chain executes?
```

### Per-Node Execution Checklist

```
□ Budget checked before node loaded into viewport?
□ Node loaded: current=FULL, lookahead=LITE (3), lookbehind=LITE (3)?
□ Pre-conditions verified (not assumed): all → PASS before AEP runs?
□ AEP executed: pre_check → execute → self_check → checkpoint_commit?
□ DIFF_ENGINE.record_node_result called immediately after AEP?
□ COHERENCE_MONITOR.run_continuous called after DIFF record?
□ CHAIN_EXECUTOR.on_node_complete called (updates chain progress, Z=4 counter)?
□ Checkpoint saved if node.checkpoint_after == true?
□ Cursor advanced (not left at completed node)?
```

### Per-Chain Completion Checklist

```
□ DIFF_ENGINE.check_chain run before chain committed?
□ Diff result clean (no missing_removals, no missing_additions, no contaminations)?
□ All diagonal edges from this chain: in-flight updated to "SOURCE_COMPLETE"?
□ Diagonal targets re-checked: any newly unblocked → cursor_blocked = false?
□ CHAIN_EXECUTOR.on_chain_complete called (Z=4 pass node → DONE)?
□ Cell checkpoint saved (MSNAP with full cell_states)?
□ Z=4 pass node progress counter matches actual executed node count?
```

### Per-File Completion Checklist

```
□ All Z=5 nodes for this file: status DONE?
□ DIFF_ENGINE.run_full_pass(file) clean?
□ COHERENCE_MONITOR.run_file_boundary(file): all invariants SATISFIED?
□ File MSNAP saved and hash verified?
□ LOCK_TABLE.release(file) called?
□ XFC_EXECUTOR.on_source_file_complete(file) called (may unlock target files)?
□ VIEWPORT_MANAGER.evict_file(file) called (frees working zone)?
□ INTEGRATION_BRIDGE.sync_on_file_complete called?
□ STATUS_EMITTER.emit_file_complete called?
```

### Reshape Event Checklist

```
□ HALT_AT_NEXT_ATOMIC_BOUNDARY flag set before any cascade?
□ RESHAPE_PRE snapshot saved before any Z=0/Z=1 modifications?
□ Old guide marked SUPERSEDED in GUIDE_REG before new guide activated?
□ Z=1 nodes updated to point to new guide?
□ New Z=0 invariant nodes created (or existing updated)?
□ All PENDING nodes in affected volumes re-derived against new guide?
□ DONE nodes checked for violations — remediation tasks generated if needed?
□ Remediation tasks inserted into chain at correct positions?
□ Integrity check re-run on all affected chains (PENDING scope only)?
□ HALT flag cleared and Traversal Engine resumed from RESHAPE_PRE snapshot?
□ STATUS_EMITTER.emit_reshape_complete called?
```

---

## Metrics the Matrix Driver Maintains

### Per-MRO (Volume) Metrics

```json
{
  "mro_id": "MRO-P001-sess-20240115-001",
  "runtime_metrics": {
    "nodes_executed":         84,
    "nodes_passed":           84,
    "nodes_failed":            0,
    "nodes_retried":           0,
    "nodes_reworked":          0,
    "rollbacks":               0,
    "chain_regressions":       0,
    "reshapes":                0,
    "compressions":            0,
    "context_overflows":       0,
    "coherence_violations":    0,
    "snapshots_saved":        23,
    "snapshots_verified":     23,
    "snapshots_corrupted":     0
  },
  "quality_metrics": {
    "self_check_pass_rate":  "100%",
    "diff_clean_rate":       "100%",
    "gate_pass_rate":        "100%",
    "vertical_chain_coverage": "84/84 nodes grounded to Z=0",
    "diagonal_coverage":     "all 8 edges registered and consumed",
    "cross_file_coverage":   "all 3 XFC chains consumed cleanly"
  },
  "performance_metrics": {
    "peak_context_usage":    "61%",
    "compression_level_reached": 0,
    "avg_nodes_per_chain":   16.8,
    "critical_path_length":  33,
    "parallel_execution":    "N/A (single volume active)"
  }
}
```

---

## Relationship Summary

```
DOCUMENT STACK AND DIVISION OF RESPONSIBILITY:

ai-task-execution-methodology.md
    WHAT: base protocol — ANALYSIS → PLAN → EXECUTION (single plan)
    DOES: defines phases, file-by-file execution, domino rules
    DOES NOT: manage multiple plans, track context, handle guides dynamically

ai-task-execution-methodology-driver.md
    WHAT: multi-plan orchestrator
    DOES: GUIDE_REG, PLAN_REG, TASK_REG, LOCK_TABLE, CHECKPOINT_STORE,
          conflict matrix, topological scheduling, AEP, validation hierarchy 1–4
    DOES NOT: define spatial organization of tasks, manage viewport, traverse 3D space

ai-task-execution-methodology-context-matrix.md
    WHAT: 3D structural model
    DOES: defines M[Z,X,Y] address space, axis semantics, node structure,
          chain types (vertical/horizontal/diagonal/cross-file), conflict geometry,
          population protocol, integrity rules
    DOES NOT: execute anything, manage state, move a cursor, monitor budget

ai-task-execution-methodology-context-matrix-driver.md  ← THIS DOCUMENT
    WHAT: runtime engine for the 3D matrix
    DOES: MRO, CURSOR, VIEWPORT_MANAGER, TRAVERSAL_ENGINE, CHAIN_EXECUTOR,
          COHERENCE_MONITOR, DIFF_ENGINE, RESHAPE_HANDLER, CHECKPOINT_MANAGER,
          VOLUME_COORDINATOR, ERROR_RECOVERY, STATUS_EMITTER, INTEGRATION_BRIDGE
    DOES NOT: define what the structure is (that's the Matrix),
              define what the phases are (that's the base methodology),
              define what multi-plan scheduling is (that's the Driver)

EXECUTION FLOW ACROSS ALL FOUR DOCUMENTS:
  Base: ANALYSIS → PLAN → EXECUTION → VALIDATION
  Driver: wraps base in GUIDE_REG → CONFLICT_SCAN → SCHEDULE → [base × N] → GLOBAL_VALID
  Matrix: defines WHERE each task lives in M[Z,X,Y]
  Matrix Driver: operates the matrix — populates it, navigates it, monitors it, recovers it
```

---

*Designed by analogy with:  
CPU fetch-decode-execute pipeline (Traversal Engine = instruction pipeline),  
virtual memory manager (Viewport Manager = MMU with zone-based eviction),  
hardware watchdog timer (Coherence Monitor = invariant watchdog),  
filesystem journal with fsck (Diff Engine = structural integrity checker),  
FPGA partial reconfiguration (Reshape Handler = live circuit modification without full reload),  
SMP cache coherence protocol (Volume Coordinator = multi-core cache consistency),  
and NVRAM journaling (Checkpoint Manager = atomic write-ahead log with verification).*

---

## Formal State Machine

Complete specification of all MRO states, transitions, triggers, and outputs.
This is the authoritative reference — every subsystem behaviour maps to one of these transitions.

### State Definitions

```
S0   CREATED           MRO object allocated, no content yet
S1   SCAFFOLDING       Population Engine Phase A running (Z=2,3,4 scaffold)
S2   POPULATING        Population Engine Phase B running (Z=5 nodes)
S3   CHAINING          Population Engine Phases C+D running (chain links + diagonals)
S4   INTEGRITY_CHECK   Population Engine Phase E running
S5   READY             All integrity checks passed, cursor at first node
S6   EXECUTING         Traversal Engine running, cursor at a Z=5 node, AEP in flight
S7   ADVANCING         AEP completed, cursor moving to next position
S8   GATE_CHECK        Coherence Monitor running full gate scan
S9   COMPRESSING       Viewport Manager compressing (Level 1 or 2)
S10  CHECKPOINTING     Checkpoint Manager writing snapshot
S11  ROLLING_BACK      Error Recovery restoring file to snapshot
S12  BLOCKED           Cursor at a node whose pre_conditions are not yet met
S13  HALTED_RESHAPE    Traversal Engine paused at atomic boundary for reshape
S14  RESHAPING         Reshape Handler active (Steps 2–7)
S15  VALIDATING        Diff Engine running full-volume pass
S16  REMEDIATING       Regression found in validation — generating remediation nodes
S17  SUSPENDED         Budget CRITICAL — session ended, awaiting resume
S18  DONE              All nodes DONE, validation clean, volume complete
S19  FAILED            Unrecoverable error — volume cannot proceed
S20  HALTED            System-level halt — human review required
```

### Transition Table

```
FROM         EVENT                              TO           ACTION
────────────────────────────────────────────────────────────────────────────────────
S0           plan_registered + guide_reg_ready  S1           Population Engine.phase_A()
S1           scaffold_complete + all_Z4_to_Z0   S2           Population Engine.phase_B()
S1           scaffold_fail                       S20          emit_halt("SCAFFOLD_FAIL")
S2           all_findings_processed              S3           Population Engine.phase_C_D()
S3           chains_built + diagonals_registered S4           Population Engine.phase_E()
S4           integrity_check_PASSED              S5           cursor.set_first_node()
                                                              viewport.load_persistent_zone()
                                                              emit_navigation()
S4           integrity_check_FAILED             S20          emit_halt("INTEGRITY_FAIL")
S5           traversal_engine_start              S6           chain_executor.on_chain_start()
                                                              lock_table.acquire(file)
S6           budget_check = LEVEL_1 or LEVEL_2  S9           (before loading next node)
S6           budget_check = CRITICAL             S10 → S17   emergency_snapshot()
                                                              emit_resume_prompt()
S6           pre_conditions_fail                 S12          cursor.mark_blocked()
                                                              cursor.advance_to_unblocked()
S6           aep_execute_pass                    S7           diff_engine.record_node_result()
                                                              coherence_monitor.run_continuous()
S6           aep_execute_fail                    S11          error_recovery.handle()
S7           node.checkpoint_after = true        S10 → S6    checkpoint_manager.save_node()
S7           node.checkpoint_after = false       S6           cursor.advance()
S7           cursor.at_gate()                    S8           coherence_monitor.run_gate_check()
S7           cursor.at_file_boundary()           S10 → S6    checkpoint_manager.save_file()
                                                              diff_engine.run_full_pass(file)
                                                              coherence_monitor.run_file()
                                                              lock_table.release(file)
                                                              viewport_manager.evict_file()
                                                              xfc_executor.on_source_complete()
S7           cursor.at_end_of_volume()           S15          diff_engine.run_full_pass(ALL)
S8           gate_check_PASS                     S6           continue_traversal()
S8           gate_check_FAIL                     S20          emit_halt("GATE_FAIL")
S9           compression_done                    S6           continue_traversal()
S10          snapshot_saved + verified           S6           (if normal) continue
                                                  S17         (if emergency) suspend
S11          rollback_complete + RETRYABLE        S6           retry node (max 2)
S11          rollback_complete + STRUCTURAL       S6           rework node, re-insert
S11          UNRECOVERABLE                        S19          emit_fail_report()
S12          pre_conditions_now_met               S6           cursor.unblock()
S12          blocker_node_DONE                    S6           cursor.unblock()
S13          current_aep_complete                 S14          reshape_handler.step_2()
S14          reshape_complete                     S6           resume from RESHAPE_PRE snap
S14          reshape_integrity_fail               S20          emit_halt("RESHAPE_INTEGRITY")
S15          validation_clean                     S18          integration_bridge.sync_done()
                                                              volume_coordinator.unlock_deps()
S15          validation_regression                S16          diff_engine.classify_regression()
S16          remediation_nodes_injected           S6           cursor.set_to_first_remediation()
S16          remediation_impossible               S19          emit_fail_report()
S17          new_session_started + snap_loaded    S6           rehydrate(MSNAP)
                                                              emit_navigation()
S18          —                                    TERMINAL     —
S19          —                                    TERMINAL     human_review_required
S20          —                                    TERMINAL     human_review_required
```

### State Machine Diagram

```
                    ┌──────────────────┐
         S0 ───────▶│   SCAFFOLDING    │S1
                    └────────┬─────────┘
                  PASS       │      FAIL
                    ┌────────┘         └──────────▶ S20 HALTED
                    ▼
                    S2 POPULATING
                    │
                    ▼
                    S3 CHAINING
                    │
                    ▼
                  S4 INTEGRITY_CHECK
                    │ PASS             FAIL ──────▶ S20 HALTED
                    ▼
                  S5 READY
                    │
                    ▼
              ┌── S6 EXECUTING ◀─────────────────────────────────────┐
              │       │                                               │
    budget    │       │ aep_pass                                      │
    pressure  │       ▼                                               │
              │   S7 ADVANCING                                        │
              │       │                                               │
              │  ┌────┼──────────────────────────────────────┐        │
              │  │    │                 │           │         │        │
              │  ▼    ▼                 ▼           ▼         ▼        │
              │ S10  S8             checkpoint   S15      gate_pass   │
              │ CKP  GATE_CHECK     file_bound   VALID    ────────────┘
              │  │    │ PASS              │         │
              │  │    └────────────────▶ │     S16 REMED ──▶ S6
              │  │      FAIL             │         │
              │  │       ▼               │     regression   
              │  │     S20              S6    impossible ──▶ S19
              │  │                           S18 DONE (if clean)
              │  ▼
              │ aep_fail ──▶ S11 ROLLING_BACK
              │                 │ retry ──▶ S6
              │                 │ UNRECOV ─▶ S19 FAILED
              │
     budget   └──▶ S9 COMPRESSING ──▶ S6
     CRITICAL     S10 ──▶ S17 SUSPENDED ──▶ (new session) ──▶ S6
     
     reshape_trigger ──▶ S13 HALTED_RESHAPE ──▶ S14 RESHAPING ──▶ S6
     pre_cond_fail  ──▶ S12 BLOCKED ──▶ (blocker DONE) ──▶ S6
```

---

## Cursor Priority Queue

When multiple nodes are simultaneously unblocked (pre_conditions all satisfied),
the Traversal Engine does not pick arbitrarily.
A deterministic priority queue governs selection.

### Priority Function

```
CURSOR_PRIORITY(node) → integer score (lower = higher priority, execute first)

Score components:

  P1 = critical_path_weight(node)
       0 if node.on_critical_path else 5
       // Critical path nodes always first

  P2 = chain_type_weight(node)
       0 if chain contains FAN_IN target (blocking downstream fan-in)
       1 if chain contains DIAGONAL source (triggers unlock on completion)
       2 if chain is INDEPENDENT (no pending downstream dependents)
       3 if chain is REDUCTIVE (X=3 — execute last within X group)
       // Nodes whose completion unblocks others go first

  P3 = x_axis_weight(node)
       node.address.X * 10
       // STRUCTURAL (0) before BEHAVIORAL (10) before ADDITIVE (20)
       // before REDUCTIVE (30) before RELATIONAL (40)

  P4 = y_axis_weight(node)
       domain_order_table[node.address.Y]
       // TOKEN(0) < CLASS(1) < KEYFRAME(2) < ATTR(3) < ID(4)
       // < VAR(5) < FUNC(6) < EVENT(7) < IMPORT(8)

  P5 = file_dependency_order(node)
       topological_rank(node.file)
       // Files earlier in XFC topological order first

  P6 = replacement_length_tiebreak(node)
       -len(node.content.replacement)
       // Longer replacement first (substring collision prevention)
       // Negative because lower score = higher priority

  TOTAL_SCORE = P1 * 100000 + P2 * 10000 + P3 * 1000 + P4 * 100 + P5 * 10 + P6

SELECTION: cursor moves to node with lowest TOTAL_SCORE among all PENDING + unblocked nodes
```

### Priority Queue Example

```
Unblocked nodes after M[5,0,0] TOKEN chain completes:

  Node A: M[5,0,1] CLASS in messages.html (next in H-chain, critical path)
    P1=0 (critical) P2=1 (diagonal source) P3=0 (STRUCT) P4=10 (CLASS) P5=0 P6=-22
    Score: 0 + 10000 + 0 + 1000 + 0 - 22 = 10978

  Node B: M[5,0,0] TOKEN in messages.css (XFC unlocked by messages.html TOKEN complete)
    P1=0 (critical) P2=2 (independent) P3=0 (STRUCT) P4=0 (TOKEN) P5=1 P6=-18
    Score: 0 + 20000 + 0 + 0 + 10 - 18 = 19992

  Node C: M[5,0,3] ATTR in messages.html (diagonal-unlocked)
    P1=5 (not on main critical path) P2=1 (diagonal source → JS) P3=0 P4=30 (ATTR) P5=0 P6=-8
    Score: 500000 + 10000 + 0 + 3000 + 0 - 8 = 512992

Selection order: A (10978) → B (19992) → C (512992)
→ Continue CLASS chain in messages.html first
→ Then start TOKEN chain in messages.css
→ Then ATTR chain in messages.html
```

### Blocked Node Re-evaluation

```
UNBLOCK_SCAN():
  // Triggered by: chain_complete, diagonal_unlock, xfc_unlock
  // Check all BLOCKED nodes: are their pre_conditions now satisfied?

  for node in [N for N in TASK_REG if N.cursor_blocked == true]:
    unsatisfied = [P for P in node.pre_conditions if not P.check()]
    if len(unsatisfied) == 0:
      node.cursor_blocked = false
      priority_queue.insert(node, score=CURSOR_PRIORITY(node))
      emit: "↑ UNBLOCKED: [node.node_id] M[[Z],[X],[Y]] seq=[N] | score=[score]"

  // Re-sort priority queue
  priority_queue.sort()
```

---

## Incremental Population Mode

In real execution, analysis findings do not always arrive all at once.
A file may be large, the LLM may produce findings in batches,
or new guide requirements may create additional findings mid-population.

### Incremental Mode vs Batch Mode

```
BATCH MODE (default):
  All findings for all files arrive → Population Engine runs phases A–E → READY
  Prerequisite: complete analysis finished before any execution starts.
  Guarantees: full integrity check before first node executes.

INCREMENTAL MODE (triggered when):
  - File set is large (> threshold) and analysis proceeds file-by-file
  - New guide loaded mid-population adds new requirements
  - Execution of file N reveals new findings in file N+1 (cross-file discovery)
  - User adds a new file to the plan scope mid-session
```

### Incremental Population Protocol

```
INCREMENTAL_POPULATION_PROTOCOL:

STATE: MRO.lifecycle.population_mode = "INCREMENTAL"

  PHASE A (scaffold): runs ONCE at start for all known files
    // Scaffold can be built for all files even if findings are not yet available
    // File aggregate Z=3 nodes created with task_count = 0 (to be filled)

  PHASE B (nodes): runs PER_FILE as findings arrive
    for each file F as its findings become available:
      run phase_B(file=F, findings=F.findings)
      // Only Z=5 nodes for file F created now

  PHASE C (chains): runs PER_FILE immediately after phase B for that file
    run phase_C(file=F)
    // H-chains built for file F immediately

  PHASE D (diagonals): runs PER_FILE for file F, BUT
    // Cross-file diagonals to files not yet populated: DEFERRED
    // Register as PENDING_XFC: { source_node, target_file, target_pattern }
    PENDING_XFC_LIST.append(pending entries)

  PHASE D (cross-file resolution): runs when target file's phase B completes
    for each pending XFC where target_file == F:
      find target node in newly-populated F
      register XFC chain properly
      remove from PENDING_XFC_LIST
      emit: "XFC [xfc_id] resolved: [source] → [target] | was pending"

  PHASE E (integrity): runs PER_FILE after phases B+C+D for that file
    run integrity_check(file=F, scope="THIS_FILE_ONLY")
    if PASSED:
      file F nodes: status → PENDING (eligible for execution)
    if FAILED:
      file F nodes: status → INTEGRITY_BLOCKED
      emit_integrity_report(file=F)

  CONCURRENT EXECUTION:
    File A: population DONE + integrity PASSED → eligible for execution
    File B: population still running → not yet eligible
    Constraint: file B cannot start execution until:
      (a) its own population + integrity DONE
      (b) any XFC from file A to file B: file A execution DONE
    → File A can execute while file B is still being populated
    → But file B's execution start waits for (a) AND (b)
```

### New File Added Mid-Execution

```
SCENARIO: 5 files registered, PLAN-001 is at file 3, user adds file 6 to scope.

PROTOCOL:

  1. VALIDATION: can file 6 be added without conflicting with already-executed files?
     check: does file 6 have XFC sources in files 1–3 (already DONE)?
     if YES: those XFC sources are already committed.
             Any targets in file 6 must work with the DONE state of files 1–3.
             → Generate target nodes for file 6 based on DONE state of sources.
     if NO: file 6 is independent → add normally.

  2. SCAFFOLD: create M[3], M[4] nodes for file 6.

  3. ANALYSIS: run phase B for file 6.

  4. XFC RESOLUTION: resolve any cross-file chains involving file 6.

  5. TOPOLOGICAL INSERT: determine where file 6 fits in the execution order.
     if file 6 depends on file 5 (not yet executed): insert after file 5.
     if file 6 is independent: insert at end of queue.

  6. LOCK TABLE: add file 6 to MRO.volume.file_set, lock will be acquired when its turn comes.

  7. STATUS EMITTER:
     "FILE ADDED: file6.css | scope extended | topological position: after file5.css
      | population: PENDING | estimated tasks: [N]"
```

---

## Diagnostic Mode

When execution stalls, produces unexpected results, or an error occurs that the
Error Recovery cannot classify, the Diagnostic Mode provides structured introspection
of the MRO and matrix state without modifying anything.

### Diagnostic Queries

```
DIAGNOSTIC_MODE — READ ONLY, no state changes

QUERY_1: "where exactly is the cursor?"

  OUTPUT:
    Cursor position:  VOL-P001 | messages.html | M[5,0,0] | seq=14/22
    Cursor state:     EXECUTING
    Node id:          MN-P001-messages.html-5-0-0-014
    Chain:            HCHAIN-P001-messages.html-5-0-0 | 14/22
    Prev node:        MN-...-013 | status=DONE | post_check=PASSED
    Next node:        MN-...-015 | status=PENDING | pre_cond=SATISFIED
    Chain pending_commit: true (chain not yet committed to cell checkpoint)
    Rollback anchor:  MSNAP-P001-F01-Z5-000-CHAIN_START


QUERY_2: "what is currently blocked and why?"

  OUTPUT:
    BLOCKED nodes (3):
      MN-...-5-0-3-001  M[5,0,3] ATTR  | waiting: M[5,0,0] chain ALL DONE (14/22)
      MN-...-5-0-3-002  M[5,0,3] ATTR  | waiting: M[5,0,0] chain ALL DONE (14/22)
      MN-...-5-1-6-001  M[5,1,6] FUNC  | waiting: M[5,0,3] chain ALL DONE (0/8)
    
    Blocking chain: HCHAIN-...-5-0-0 at 14/22 (8 nodes remaining)
    Estimated unlock: 8 more executions of M[5,0,0]
    Critical path: M[5,0,0](8 remain) → M[5,0,3](8) → M[5,1,6](3) = 19 nodes to end


QUERY_3: "what does node MN-P001-messages.html-5-0-0-014 look like?"

  OUTPUT: full node JSON (from matrix, read-only)
    address: M[5,0,0] | label: ATOMIC·STRUCTURAL·TOKEN
    content: RENAME --msg-bubble-radius → --messages-bubble-radius (line 69)
    status: EXECUTING
    pre_conditions: [MN-...-013.status==DONE ✅] [lock: messages.html held ✅]
    post_conditions:
      PATTERN_COUNT --msg-bubble-radius messages.html expected:0
      PATTERN_COUNT --messages-bubble-radius messages.html expected_min:1
      INVARIANT_CHECK INV-CSS-TOKENS
    diagonal: [→ MN-...-5-0-3-001 DOMINOES_INTO]
    atomic_check: { pre: PASSED, post: PENDING, invariant: PENDING }
    checkpoint_after: false
    rollback_snapshot: MSNAP-P001-F01-Z5-013


QUERY_4: "what is the invariant status right now?"

  OUTPUT:
    INV-CSS-TOKENS:  IN_PROGRESS (M[5,0,0] executing — not yet fully satisfied)
    INV-LAW0:        NOT_YET_REACHED (JS files not yet started)
    
    Last full check: MSNAP-P001-F01-Z5-000-GATE (at start-of-execution gate)
    Last continuous check: after MN-...-013 (SATISFIED for checked scope)
    Next gate check: at M[5,0,0] chain completion (all X=0 done → GATE node)


QUERY_5: "show the diff state for the current file"

  OUTPUT:
    File: messages.html
    Cell M[5,0,0] STRUCTURAL·TOKEN — IN PROGRESS:
      Expected removals: 22 patterns
      Removed so far:    13 (confirmed by execution result records)
      Remaining:          9 (nodes 015–022 pending + node 014 in flight)
      grep scan now:     --msg-bubble-radius: 9 remaining ← matches expected
      Status: ON TRACK ✓
    
    Cell M[5,0,1] STRUCTURAL·CLASS — PENDING (blocked):
      Expected removals: 22 patterns
      grep now: .msg-bubble: 22 (none removed yet — correct, X=1 not started)
      Status: WAITING ✓
    
    Contamination scan:
      No unexpected changes to M[5,0,1] from M[5,0,0] work so far ✓


QUERY_6: "show the full volume topology"

  OUTPUT: file dependency graph + topological order
    tokens.css → messages.css (XFC-P001-001: token definition → usage)
                → messages.html (XFC-P001-002: same token)
    messages.html → messages.js (XFC-P001-003: data-attr → JS handler)
    
    Topological order:
      Tier 0: tokens.css
      Tier 1: messages.css, messages.html (parallel — no lock conflict)
      Tier 2: messages.js
    
    Current status:
      tokens.css    ✅ DONE
      messages.css  🔄 IN_PROGRESS  (lock held)
      messages.html ░  BLOCKED (waiting messages.css XFC-P001-001)
      messages.js   ░  BLOCKED (waiting messages.html XFC-P001-003)


QUERY_7: "what snapshots exist and are they valid?"

  OUTPUT:
    Snapshot registry for VOL-P001:
      MSNAP-P001-F01-Z5-000-CHAIN_START  ✓ verified  (file hash matches)
      MSNAP-P001-F01-Z5-010-NODE         ✓ verified
      MSNAP-P001-F01-Z5-013-NODE         ✓ verified  ← current rollback target
      [...]
    Total: 14 snapshots | 14 verified | 0 corrupted
    Oldest safe rollback: MSNAP-P001-F01-Z5-000-CHAIN_START
```

### Diagnostic Trigger Conditions

```
Diagnostic Mode is entered automatically when:

  1. Error Recovery STRUCTURAL failure → cannot determine rework strategy
     → QUERY_3 + QUERY_5 automatically emitted before human review
  
  2. Gate check FAIL → cannot determine which invariant is violated
     → QUERY_4 + QUERY_5 emitted before HALTED
  
  3. Budget CRITICAL but resume prompt must be complete
     → QUERY_2 + QUERY_6 emitted as part of resume prompt
  
  4. Cross-plan consistency check FAIL
     → QUERY_6 emitted for all volumes
  
  5. Human types diagnostic command (explicit request)
     → run requested query, do not modify any state
```

---

## Session Handoff Protocol

A session handoff occurs when the LLM context ends (budget exhaustion, user break,
session timeout) and a new session must resume exactly where the previous left off.

This is the most critical recovery operation. A failed handoff means lost work.
The Session Handoff Protocol is therefore the most rigorously verified sequence.

### Outgoing Session (before context ends)

```
OUTGOING_SESSION_PROTOCOL (triggered by budget CRITICAL or user signal):

STEP 1 — ATOMIC BOUNDARY HALT:
  Set: TRAVERSAL_ENGINE.halt_after_current_aep = true
  Wait: current AEP completes (PASS or FAIL)
  Do NOT begin the next node.

STEP 2 — EMERGENCY SNAPSHOT:
  snap = CHECKPOINT_MANAGER.save(type=EMERGENCY_CHECKPOINT)
  Verify: sha256(current_file) == snap.file_hash
  If verification fails: HALT — do not emit resume prompt with corrupt snapshot
  MRO.lifecycle.last_checkpoint_id = snap.snapshot_id

STEP 3 — REFERENCE PACKAGE:
  Build compact reference package containing:
    A. Snapshot ID and file hash (for verification on resume)
    B. Active guide IDs + versions (must be re-loaded in new session)
    C. Cursor position: volume, file, M[Z,X,Y], sequence
    D. Progress summary: done/total per file, per plan
    E. Pending XFC chains (source/target/state)
    F. In-flight diagonal chains (source/target/state)
    G. All BLOCKED nodes and their blocking conditions
    H. Context budget state at handoff
    I. Open issues: any REWORK nodes, any PENDING integrity issues

STEP 4 — EMIT RESUME PROMPT:
  (see STATUS_EMITTER.emit_resume_prompt() format in §Status Emitter)
  The resume prompt IS the reference package in human-readable form.
  It must be self-contained — the new session must be able to operate
  from the resume prompt alone, without access to the old session's context.

STEP 5 — FINAL EMIT:
  "SESSION HANDOFF COMPLETE | snap=[snap_id] | new session: load snap + verify + resume"
  MRO.lifecycle.phase = "SUSPENDED"
```

### Incoming Session (new session, resuming)

```
INCOMING_SESSION_PROTOCOL:

STEP 1 — IDENTIFY RESUME POINT:
  Parse resume prompt → extract:
    snap_id, guide_ids[], cursor_position, file, file_hash
    pending_xfc[], in_flight_diagonal[], blocked_nodes[]
  Emit: "INCOMING SESSION | resuming from [snap_id]"

STEP 2 — GUIDE VERIFICATION:
  For each guide_id in guide_ids[]:
    Is guide loaded in GUIDE_REG?
    Is version correct?
    If missing: load guide from path before proceeding
    If version mismatch: run reshape protocol for version difference
  Emit: "Guides verified: [N]/[N] ✓" or "Guide [id] missing → loading..."

STEP 3 — MATRIX REHYDRATION:
  Call VIEWPORT_MANAGER.rehydrate(snap_id)
  This restores:
    - persistent zone (Z=0, Z=1, session meta)
    - working zone (file aggregate, pass descriptor, current+next nodes)
    - reference zone (completed cells/files, pending XFCs)
  File hash verification is part of rehydrate() — if it fails, HALT.

STEP 4 — CHAIN STATE RESTORATION:
  Restore from reference package:
    horizontal chain state: which chain is active, position in chain
    diagonal chain state: restore in_flight_diagonal[] entries
    cross-file chain state: restore pending_xfc[] entries
  For each BLOCKED node: re-verify blocking conditions
    (if condition was satisfied in the old session but blocked status was saved:
     re-check → if now unblocked, mark cursor_blocked = false)

STEP 5 — INTEGRITY SPOT-CHECK:
  Run DIAGNOSTIC QUERY_4 (invariant status)
  Run DIAGNOSTIC QUERY_5 (diff state for current file)
  Run DIAGNOSTIC QUERY_2 (blocked nodes)
  Compare against reference package expectations.
  If any discrepancy → HALT, emit discrepancy report.
  If all consistent → proceed.

STEP 6 — CONFIRM AND EMIT:
  emit_navigation()
  "INCOMING SESSION READY ✓
   Snapshot:  [snap_id]
   File hash: VERIFIED ✓
   Guides:    [N]/[N] loaded ✓
   Chains:    [H: position] [D: [N] in-flight] [XFC: [N] pending]
   Blocked:   [N] nodes (conditions unchanged ✓)
   Cursor:    M[[Z],[X],[Y]] seq=[N] → [next_node_target]
   Resuming."

STEP 7 — RESUME TRAVERSAL ENGINE:
  MRO.lifecycle.phase = "EXECUTING"
  MRO.cursor.state = "READY_TO_RESUME"
  TRAVERSAL_ENGINE.start()
  // Traversal Engine picks up from cursor position
  // First action: check pre_conditions for next node (do not assume they're still met)
```

### Handoff Failure Modes

```
FAILURE: file hash mismatch on incoming session
  Cause: file was modified externally between sessions
  Action: HALT — cannot resume safely
  Recovery: human must determine what changed and whether to:
    (a) restore file to snapshot state (accept losing external changes)
    (b) re-analyze the file and rebuild matrix from current state

FAILURE: guide version mismatch (old session had v5, new session loads v6)
  Cause: guide was updated between sessions
  Action: treat as guide update event → run RESHAPE_HANDLER
  Note: this is a VALID state — reshaping at session start is safe

FAILURE: diagonal chain source status changed (was DONE, now PENDING — corruption)
  Cause: matrix state was corrupted between sessions (should not happen with verified snaps)
  Action: HALT — cannot trust matrix state
  Recovery: roll back to last verified GATE checkpoint and re-execute from there

FAILURE: missing guide cannot be loaded
  Cause: guide file not found at registered path
  Action: HALT — cannot execute without required ARCHITECTURAL guide
  Recovery: human must provide guide at expected path

FAILURE: resume prompt is incomplete (truncated)
  Cause: context budget ran out before resume prompt was fully emitted
  Action: load last verified GATE checkpoint (coarser granularity than EMERGENCY snap)
  Cost: re-execute from last GATE checkpoint (may duplicate some work — idempotent ops)
```

---

## Concurrent Volume Execution

When two or more volumes run simultaneously (DISJOINT volumes, parallelism permitted),
the Matrix Driver manages concurrency at the MRO level.

### Concurrency Model

```
LLM CONTEXT = one thread (no true parallelism)
"Concurrent" in Matrix Driver = time-sliced interleaving of volumes

Slice triggers:
  - Current volume reaches a GATE node (natural pause)
  - Current volume's next node is BLOCKED (waiting for XFC)
  - Budget pressure (compress current, switch to fresh volume context)
  - Explicit round-robin after N nodes (fairness)

NOT triggered:
  - Mid-chain interleaving (never switch volumes inside a horizontal chain)
  - Mid-AEP interleaving (never switch while an atomic operation is executing)
  - Mid-diagonal interleaving (never switch after unlocking diagonal but before target executes)
```

### Volume Scheduler

```
VOLUME_SCHEDULER:

  active_mros = [MRO-P001, MRO-P002]  // all non-SUSPENDED, non-DONE volumes
  current_mro = MRO-P001               // which volume the LLM is currently executing

  SLICE_POINT detection:
    volume_can_yield() = (
      cursor.at_gate()        OR   // natural pause
      cursor.next_is_blocked()  OR   // nothing to do here
      budget_pressure()           OR   // current volume compressing
      nodes_since_last_yield >= FAIRNESS_LIMIT (default: 20 nodes)
    )

  YIELD_AND_SWITCH():
    // 1. Snapshot current MRO state (lightweight — cursor + chain position)
    MRO_P001.lifecycle.yield_snapshot = compact_snapshot(cursor)
    // 2. Compress current volume's working zone
    VIEWPORT_MANAGER.compress(current_mro, to_level=1)
    // 3. Select next MRO
    next_mro = SELECT_NEXT_MRO(active_mros, exclude=current_mro)
    // 4. Load next MRO's viewport
    VIEWPORT_MANAGER.load_mro(next_mro)
    current_mro = next_mro
    STATUS_EMITTER.emit_volume_switch(from=MRO-P001, to=MRO-P002)

  SELECT_NEXT_MRO(mros, exclude):
    candidates = [mro for mro in mros if mro != exclude and mro.state in [READY, EXECUTING]]
    // Priority: volume with most-unblocked critical-path nodes first
    scored = [(mro, critical_path_score(mro)) for mro in candidates]
    return min(scored, key=lambda x: x[1]).mro

  critical_path_score(mro):
    // How far is this volume from its next GATE checkpoint?
    // Shorter distance = higher priority (want to reach gates faster = more coherence checks)
    return nodes_until_next_gate(mro)
```

### Volume Switch Output Format

```
─────────────────────────────────────────────────────────────
VOLUME YIELD: VOL-P001 → VOL-P002
  Reason:       FAIRNESS_LIMIT (20 nodes since last yield)
  VOL-P001:     messages.html M[5,0,1] seq=12/22 | yield_snap saved
  VOL-P002:     wallet.html M[5,0,0] seq=7/18    | resuming
─────────────────────────────────────────────────────────────
MATRIX NAVIGATION [VOL-P002]
  Volume:   VOL-P002 | PLAN-002
  File:     wallet.html
  Cell:     M[5,0,0] STRUCTURAL·TOKEN
  Position: node 8/18
  ...
─────────────────────────────────────────────────────────────
```

### Cross-Volume XFC Coordination

```
SCENARIO: VOL-P001 finishes messages.css
          XFC-CROSS-001: messages.css (P001) → wallet.css (P002)
          wallet.css is in VOL-P002's scope

PROTOCOL:
  1. VOL-P001 XFC_EXECUTOR.on_source_file_complete(messages.css)
  2. XFC_EXECUTOR notifies VOLUME_COORDINATOR:
     "XFC-CROSS-001: source complete | target: wallet.css in VOL-P002"
  3. VOLUME_COORDINATOR:
     find MRO-P002
     MRO-P002.chain_state.cross_file.pending_unlock.remove(XFC-CROSS-001)
     MRO-P002.cursor.unblock_file(wallet.css) if it was blocked on this XFC
  4. VOLUME_SCHEDULER re-evaluates VOL-P002's priority
     (wallet.css just became executable → higher priority for next slice)
  5. Emit:
     "⇒ CROSS-VOLUME XFC: VOL-P001 messages.css → VOL-P002 wallet.css UNLOCKED"
```

### Shared Z=0/Z=1 Write Coordination

```
Problem: both volumes read from Z=0,Z=1 constantly.
         If a reshape happens in one volume, Z=0 must be updated for both.

Protocol:
  GLOBAL_Z0_Z1_LOCK: acquired by Reshape Handler when updating shared layers
  While lock is held: all other volumes' Traversal Engines set READ_ONLY_MODE
  (they may read Z=0, Z=1 but must not act on their content until lock released)
  After lock released: all volumes receive Z_LAYER_UPDATE event
  Each volume's Reshape Handler runs cascade for its own pending/executing nodes
```

---

## Decision Trees

Compact operational decision trees for the most frequent driver decisions.

### Decision Tree 1: Should I Checkpoint Here?

```
Should I checkpoint at this moment?
        │
        ├─[YES] → node.checkpoint_after == true?
        ├─[YES] → cursor.at_file_boundary?
        ├─[YES] → cursor.at_gate?
        ├─[YES] → budget < 30%?
        ├─[YES] → reshape just completed?
        ├─[YES] → chain just completed (cell boundary)?
        └─[NO]  → none of the above
                  → do not checkpoint
                  → advance cursor normally

Checkpoint types map:
  node.checkpoint_after=true → NODE_CHECKPOINT (minimal)
  chain_complete            → CELL_CHECKPOINT (medium)
  file_boundary             → FILE_CHECKPOINT (full, = MSNAP)
  gate_check_pass           → GATE_CHECKPOINT (medium + invariants)
  budget < 30%              → EMERGENCY_CHECKPOINT (minimal) → SUSPEND
  reshape complete          → GATE_CHECKPOINT (full MRO state)
```

### Decision Tree 2: Is This Failure Retryable?

```
AEP self-check FAILED. What now?
        │
        ├─ Pattern still present after operation?
        │   ├─ YES: count > 0 but was 0 before → WRONG_ORDER?
        │   │         test: is the pattern a substring of another unfixed pattern?
        │   │         YES → RETRYABLE (fix: sort longest-first) → retry
        │   │         NO  → STRUCTURAL (wrong target pattern) → rework
        │   │
        │   └─ YES: count unchanged → operation may not have run
        │           check: stale line numbers? file shifted?
        │           YES → RETRYABLE (re-scan for target, update location) → retry
        │           NO  → STRUCTURAL (target not present as expected) → rework
        │
        ├─ Replacement present but wrong form?
        │   (e.g., "--messagesbubble-radius" instead of "--messages-bubble-radius")
        │   → STRUCTURAL (wrong replacement string) → rework, fix content.replacement
        │
        ├─ Invariant check VIOLATED?
        │   Replacement itself violates Z=0 invariant?
        │   YES → STRUCTURAL (replacement was wrong per guide)
        │         fix: derive correct replacement from INV canonical value → rework
        │   NO  → operation introduced a new violation in adjacent code
        │         → STRUCTURAL (scope of operation was too broad) → rework with narrower pattern
        │
        └─ Pre-condition FAIL on node execution?
            Pre-condition was satisfied at START but not now?
            YES → another volume modified the same file (LOCK_STOLEN?) → UNRECOVERABLE
            NO  → pre-condition was incorrectly evaluated → RETRYABLE (re-evaluate)
```

### Decision Tree 3: Which Compression Level?

```
Budget check triggered. What level?
        │
        ├─ remaining > 70%: LEVEL_0 — do nothing, continue
        │
        ├─ 30% < remaining ≤ 70%: LEVEL_1
        │   → fold completed cells in working zone
        │   → fold completed passes in file aggregate
        │   → continue execution
        │
        ├─ 10% < remaining ≤ 30%: LEVEL_2
        │   → LEVEL_1 actions PLUS:
        │   → full file offload for completed files (verify MSNAP first)
        │   → ultra-compress Z=0 invariants in persistent zone
        │   → reduce lookahead from 3 to 1
        │   → continue execution
        │
        └─ remaining ≤ 10% (or remaining ≤ critical_reserve):
            CRITICAL — do NOT start next node
            → EMERGENCY_CHECKPOINT immediately
            → emit_resume_prompt
            → MRO.phase → SUSPENDED
            → session ends
```

### Decision Tree 4: Is This a Diagonal or a Horizontal Edge?

```
Node N at M[5, X, Y] produces output consumed by node C. What edge type?
        │
        ├─ C is in the same file AND same [X, Y] cell:
        │   → HORIZONTAL (sequence neighbor in same chain)
        │   → no edge registration needed — handled by chain ordering
        │
        ├─ C is in the same file AND different Y (same or different X):
        │   → DIAGONAL (intra-file)
        │   → register: N.diagonal → C with DOMINOES_INTO
        │   → C.pre_conditions gets: N's chain ALL DONE
        │
        ├─ C is in a DIFFERENT file:
        │   → CROSS_FILE (XFC)
        │   → register XFC chain: xfc_id, source node, target node, lock_order
        │   → C.pre_conditions gets: source_file ALL DONE (file-level, not just chain)
        │
        └─ C is in a DIFFERENT volume (different plan):
            → CROSS_VOLUME_XFC
            → register with Volume Coordinator
            → lock_order: alphabetical across both volumes
            → C unblock: via VOLUME_COORDINATOR.unlock_target_file()
```

### Decision Tree 5: When to Run the Diff Engine?

```
When should DIFF_ENGINE run?
        │
        ├─ After each individual node? → NO
        │   (post_conditions in AEP step ③ already cover the node level)
        │   (DIFF_ENGINE is for aggregate validation, not per-node)
        │
        ├─ After each H-CHAIN completes? → YES (always)
        │   DIFF_ENGINE.check_chain(chain)
        │   Checks all expected removals + additions for the entire cell
        │
        ├─ After each FILE completes? → YES (always)
        │   DIFF_ENGINE.run_full_pass(file)
        │   Checks all cells for this file + contamination scan
        │
        ├─ After GATE node? → YES (if GATE is file-level or plan-level)
        │   DIFF_ENGINE.run_full_pass(scope=ALL_PROCESSED_FILES)
        │
        ├─ After RESHAPE? → YES (on affected files only)
        │   DIFF_ENGINE.run_full_pass(scope=RESHAPE_AFFECTED_FILES)
        │
        └─ After complete VOLUME? → YES
            DIFF_ENGINE.run_full_pass(scope=ALL_FILES) → final clean bill
```

---

## Master Quick Reference

### Subsystem Responsibilities

```
┌──────────────────────────┬──────────────────────────────────────────────────────┐
│ Subsystem                │ Responsibility                                        │
├──────────────────────────┼──────────────────────────────────────────────────────┤
│ Population Engine        │ Builds Z=2,3,4,5 nodes + chains + integrity check    │
│ Traversal Engine         │ Main loop: select → load → execute → advance          │
│ Viewport Manager         │ Maps matrix to LLM context: zones + compression       │
│ Chain Executor           │ Manages chain-level commit, diagonal unlocks, XFC     │
│ Coherence Monitor        │ Watches invariants: continuous + file + gate          │
│ Diff Engine              │ Computes expected vs actual state, classifies regression│
│ Reshape Handler          │ Integrates new guides mid-execution (8-step protocol) │
│ Checkpoint Manager       │ Saves + verifies snapshots, manages rollbacks         │
│ Volume Coordinator       │ Inter-volume locking, XFC across plans, consistency   │
│ Error Recovery           │ Classifies failures, retries/reworks/halts            │
│ Status Emitter           │ All human-visible output (navigation, results, alerts) │
│ Integration Bridge       │ Sync between Matrix Driver and base Driver            │
│ Cursor Priority Queue    │ Deterministic node selection when multiple unblocked  │
│ Volume Scheduler         │ Time-slices concurrent volumes (fairness + priority)  │
│ Diagnostic Mode          │ Read-only introspection without state changes         │
│ Session Handoff Protocol │ Clean session boundary — outgoing + incoming          │
└──────────────────────────┴──────────────────────────────────────────────────────┘
```

### Address → Subsystem → Output Format

```
Situation                          Primary Subsystem       Output Marker
──────────────────────────────────────────────────────────────────────────────
New volume starting                Population Engine       "scaffold complete:"
Integrity check result             Population Engine       "integrity: N/N ✓"
Session start / file boundary      Status Emitter          "MATRIX NAVIGATION"
Each atomic node result            Status Emitter          "✅/❌ T[seq] M[Z,X,Y]"
Chain completion                   Chain Executor          "✅ Chain M[5,X,Y]"
File completion                    Chain Executor          "✅ FILE [name]"
Diagonal unlock                    Chain Executor          "↗ Diagonal UNLOCKED:"
XFC unlock                         XFC Executor            "⇒ XFC [id]: UNLOCKED"
Coherence gate result              Coherence Monitor       "COHERENCE ✓/❌"
Diff result                        Diff Engine             "DIFF ✓/regression"
Rollback triggered                 Checkpoint Manager      "ROLLBACK ✓"
Reshape triggered                  Reshape Handler         "RESHAPE: halting..."
Reshape complete                   Reshape Handler         "RESHAPE complete ✓"
Budget level change                Viewport Manager        "COMPRESS L[N]"
Session handoff (outgoing)         Status Emitter          "SESSION HANDOFF COMPLETE"
Session resume (incoming)          Status Emitter          "INCOMING SESSION READY ✓"
Volume switch                      Volume Scheduler        "VOLUME YIELD: → "
Diagnostic query                   Diagnostic Mode         "QUERY_N OUTPUT:"
Halt (any cause)                   Status Emitter          "HALT [cause]"
```

### Key Thresholds and Limits

```
Context budget zones:
  > 70%  normal operation (Level 0)
  30–70% Level 1 compression (fold completed cells/passes)
  10–30% Level 2 compression (offload files, ultra-compress Z=0)
  < 10%  CRITICAL → emergency snapshot → suspend

Retry limits:
  RETRYABLE node failure: max 2 retries before escalating to STRUCTURAL

Chain ordering rules:
  X ascending within each file: 0 (STRUCT) → 1 (BEHAV) → 2 (ADD) → 3 (REDUCT) → 4 (RELAT)
  Y order within each X: TOKEN → CLASS → KEYFRAME → ATTR → ID → VAR → FUNC → EVENT → IMPORT
  Within each [X,Y] chain: longest replacement string first (descending by len)

Fairness slice limit:
  20 nodes per volume before yielding to next concurrent volume (if any)

Checkpoint triggers (mandatory, not optional):
  node.checkpoint_after = true | chain complete | file boundary | gate pass
  reshape pre | reshape post | budget < 30% | emergency

Lookahead / lookbehind:
  Normal:     3 nodes ahead, 3 nodes behind (LITE form)
  Level 2:    1 node ahead, 1 node behind
  Critical:   0 ahead (only current node in full, next node ID only)
```

---

## Worked Example — Full Matrix Driver Operation

Two volumes, one reshape, one session handoff, concurrent execution.
All major subsystems active.

### Setup

```
Session:   sess-20240115-001
Guides:    arch-containerization-5 (initial)
Plans:     PLAN-001: messages.html + messages.css (VOL-P001)
           PLAN-002: wallet.html (VOL-P002)
Event:     arch-containerization-6 arrives mid-execution (supersedes arch-v5)
Event:     budget pressure triggers session handoff mid-PLAN-002
```

### Boot Sequence

```
[Driver Phase 0D]
  GR initialized: sess-20240115-001
  arch-containerization-5 loaded → Z=0: INV-CSS-TOKENS, INV-LAW0
  PLAN-001 registered → VOL-P001 created
  PLAN-002 registered → VOL-P002 created
  Conflict matrix: VOL-P001 ∩ VOL-P002 = DISJOINT → parallel execution allowed

[Population Engine: VOL-P001]
  Phase A: scaffold messages.html (3 passes) + messages.css (2 passes)
  Phase B: 55 nodes from analysis_findings
  Phase C: 4 H-chains built
  Phase D: 8 intra-file diagonals + 2 cross-file XFC chains
  Phase E: integrity check → 7/7 PASSED ✓
  "VOL-P001 READY | 55 nodes | 4 chains | 10 edges"

[Population Engine: VOL-P002]
  Phase A: scaffold wallet.html (2 passes)
  Phase B: 29 nodes
  Phase C: 2 H-chains
  Phase D: 3 intra-file diagonals
  Phase E: integrity → PASSED ✓
  "VOL-P002 READY | 29 nodes | 2 chains | 3 edges"

[Coherence GATE 0: pre-execution]
  All guides loaded ✓ | All volumes integrity PASSED ✓ | Conflicts: 0 ✓
  "GATE 0 PASSED — begin execution"
```

### Concurrent Execution Phase (nodes 1–20)

```
[VOLUME_SCHEDULER: activate both volumes, start with VOL-P001 (critical path longer)]

[VOL-P001: messages.html M[5,0,0] TOKEN chain — nodes 1–10]
  ✅ T001 M[5,0,0] --msg-bubble-radius → --messages-bubble-radius | grep:13 → 0 ✓
  ✅ T002 M[5,0,0] --msg-sent-bg → --messages-sent-bg            | grep:8  → 0 ✓
  ...  (10 nodes, each self-checked via AEP step ③)
  "COMPRESS L1 | budget: 68% → 65% | folded: 0 completed cells"  ← no fold yet

[VOLUME YIELD after 20 nodes → switch to VOL-P002]
  "VOLUME YIELD: VOL-P001 → VOL-P002 | reason: FAIRNESS_LIMIT"
  VOL-P001 yield_snapshot saved | viewport compressed L1
  VOL-P002 viewport loaded

[VOL-P002: wallet.html M[5,0,0] TOKEN chain — nodes 1–10]
  ✅ T001 M[5,0,0] --wal-card-radius → --wallet-card-radius | grep:6 → 0 ✓
  ...

[VOLUME YIELD → back to VOL-P001]
```

### Reshape Event (mid-execution)

```
[arch-containerization-6 received while VOL-P001 at messages.css M[5,0,0] seq=7]

RESHAPE_HANDLER triggered:
  "RESHAPE: arch-v6 received | halting at next atomic boundary"
  TRAVERSAL_ENGINE.halt_after_current_aep = true

[seq=7 AEP completes: PASS]
  MRO.cursor.state = "HALTED_AT_BOUNDARY"

STEP 2: RESHAPE_PRE snapshot
  "RESHAPE_PRE saved: MSNAP-P001-F02-Z5-007-RESHAPE_PRE ✓"

STEP 3: Z-layer update
  arch-v5 → SUPERSEDED in GUIDE_REG
  Z=1 node M[1,0,0]: guide_ref → arch-v6
  New invariant from arch-v6: INV-WIDGET-COMPOUND (compound tokens need hyphens)
  "RESHAPE: Z=0 updated | 1 new invariant: INV-WIDGET-COMPOUND"

STEP 4: Cascade to both volumes
  VOL-P001 affected: messages.html (partially done), messages.css (in progress)
    PENDING nodes re-derived: 27 nodes updated post_conditions
  VOL-P002 affected: wallet.html (partially done)
    PENDING nodes re-derived: 14 nodes updated

STEP 5: Non-conforming PENDING nodes
  messages.css M[5,0,0] seq=8–12: target pattern correct (arch-v6 compatible) ✓
  messages.html M[5,0,3] seq=3: data-msg-compound → data-messages-compound ← rework needed
    (arch-v5 allowed data-msg-*, arch-v6 requires full widget name in data-*)
    node content updated: replacement → "data-messages-compound"
  "RESHAPE rework: 1 node | VOL-P001 messages.html M[5,0,3] seq=3"

STEP 6: DONE nodes violating new invariant
  messages.html M[5,0,0] DONE: all --messages-* ← compatible with arch-v6 ✓
  messages.html M[5,0,1] DONE: all .messages-* ← compatible ✓
  "0 DONE nodes violated by arch-v6 — no remediation needed"

STEP 7: Integrity re-check (PENDING scope)
  "Post-reshape integrity: VOL-P001 27 nodes re-checked | PASSED ✓"
  "Post-reshape integrity: VOL-P002 14 nodes re-checked | PASSED ✓"

STEP 8: Resume from RESHAPE_PRE
  VIEWPORT_MANAGER.rehydrate(MSNAP-P001-F02-Z5-007-RESHAPE_PRE)
  cursor: messages.css M[5,0,0] seq=8
  "RESHAPE complete ✓ | arch-v6 active | reworked=1 | remediation=0 | resume: seq=8"
```

### Session Handoff (VOL-P002 suspended)

```
[VOL-P002: wallet.html M[5,0,1] CLASS chain, seq=6 | budget drops to 9%]

CHECKPOINT_MANAGER: budget CRITICAL
  "COMPRESS L2 | budget: 11% → 9% — below critical threshold"
  TRAVERSAL_ENGINE.halt_after_current_aep = true
  [seq=6 AEP completes: PASS]
  EMERGENCY_CHECKPOINT:
    snap_id: MSNAP-P002-F01-Z5-021-BUDGET_CRITICAL
    file_hash: sha256(wallet.html) = abc123...
    cursor: wallet.html M[5,0,1] seq=7/22
  "Snapshot verified ✓"

STATUS_EMITTER.emit_resume_prompt():
  ╔═══════════════════════════════════════════════════════════════════╗
  ║ CONTEXT BUDGET CRITICAL — SESSION HANDOFF                        ║
  ║                                                                   ║
  ║ Snapshot:    MSNAP-P002-F01-Z5-021-BUDGET_CRITICAL               ║
  ║ File hash:   sha256:abc123...                                     ║
  ║ Volume:      VOL-P002 | PLAN-002                                  ║
  ║ File:        wallet.html                                          ║
  ║ Cell:        M[5,0,1] STRUCTURAL·CLASS                            ║
  ║ Position:    node 7/22 (seq 021 in plan, 6/22 DONE in chain)     ║
  ║                                                                   ║
  ║ Active guides: arch-containerization-6 (v6.0.0) ← NOTE: v6       ║
  ║                                                                   ║
  ║ Next op: MN-P002-wallet.html-5-0-1-007                            ║
  ║   RENAME .wal-card → .wallet-card (line 44)                       ║
  ║                                                                   ║
  ║ Completed: M[5,0,0] TOKEN ✅ 18/18                                ║
  ║ In chain:  M[5,0,1] CLASS ░  6/22                                ║
  ║ Pending:   M[5,0,3] ATTR  ░  0/4 (blocked: M[5,0,1] chain)      ║
  ║                                                                   ║
  ║ Blocked nodes: 4 (all waiting M[5,0,1] chain complete)           ║
  ║ In-flight diagonal: none                                          ║
  ║ Pending XFC: none (wallet.html is terminal in XFC graph)         ║
  ║                                                                   ║
  ║ VOL-P001 status: DONE (messages.html ✅ messages.css ✅)          ║
  ║                                                                   ║
  ║ To resume: load MSNAP above → verify sha256 → guides → continue  ║
  ╚═══════════════════════════════════════════════════════════════════╝
  "SESSION HANDOFF COMPLETE | VOL-P001 already DONE | VOL-P002 suspended"
```

### Incoming Session Resume

```
[New session started]

STEP 1: Parse resume prompt
  snap_id: MSNAP-P002-F01-Z5-021-BUDGET_CRITICAL
  cursor: wallet.html M[5,0,1] seq=7
  guide required: arch-containerization-6 v6.0.0
  VOL-P001: DONE (no action needed)

STEP 2: Guide verification
  arch-containerization-6 v6.0.0: loaded ✓ (same as outgoing session)

STEP 3: Rehydration
  VIEWPORT_MANAGER.rehydrate(MSNAP-P002-F01-Z5-021-BUDGET_CRITICAL)
  File hash check: sha256(wallet.html) = abc123... ← MATCH ✓

STEP 4: Chain state
  H-chain HCHAIN-P002-wallet.html-5-0-1: position=6/22, pending_commit=true
  Diagonal: none in-flight
  XFC: none pending

STEP 5: Spot-check
  QUERY_4: INV-CSS-TOKENS → SATISFIED (M[5,0,0] DONE) | INV-WIDGET-COMPOUND → IN_PROGRESS ✓
  QUERY_5: M[5,0,1] CLASS — 6/22 done, 16 remaining, no contamination ✓
  QUERY_2: 4 blocked nodes — all waiting M[5,0,1] chain ← correct

STEP 6: Confirm
  "INCOMING SESSION READY ✓
   Snapshot:  MSNAP-P002-F01-Z5-021-BUDGET_CRITICAL | VERIFIED ✓
   File hash: MATCH ✓
   Guides:    arch-v6 loaded ✓
   Chains:    H[5,0,1] at 6/22 | D[none] | XFC[none]
   Blocked:   4 nodes (M[5,0,3] — condition unchanged ✓)
   Cursor:    M[5,0,1] seq=7 → RENAME .wal-card → .wallet-card
   Resuming."

[TRAVERSAL ENGINE resumes]
  ✅ T022 M[5,0,1] .wal-card → .wallet-card (line 44)
  ... (16 more CLASS nodes)
  ✅ Chain M[5,0,1] 22/22 | diff:clean | → M[5,0,3] ATTR UNLOCKED
  ... (4 ATTR nodes)
  ✅ FILE wallet.html | tasks=29/29 | inv:2✓ | lock released
  DIFF_ENGINE.run_full_pass(ALL) → clean
  "VOL-P002 DONE ✅ | 29/29 | 0 failed | 2 sessions"

[GLOBAL VALIDATION]
  VOL-P001: DONE ✅ | VOL-P002: DONE ✅
  INV-CSS-TOKENS: SATISFIED globally ✓
  INV-WIDGET-COMPOUND: SATISFIED globally ✓
  INV-LAW0: SATISFIED globally ✓
  Cross-volume: no conflicts ✓

  ════════════════════════════════════════
  SYSTEM VALIDATION: ALL CLEAN ✅
  Plans: 2/2 | Tasks: 84/84 | Snapshots: 38/38 verified | Sessions: 2
  ════════════════════════════════════════
```

---

## Complete Anti-Pattern Catalogue

*(Supplements §Anti-Patterns with Matrix Driver–specific patterns)*

### ❌ Traversal Engine Started Before Population Phase E

Already listed. Severity: HIGH.

### ❌ Snapshot Taken Without File Hash Verification

Already listed. Severity: CRITICAL.

### ❌ Chain Committed Without Diff Check

Already listed. Severity: HIGH.

### ❌ Viewport Loaded Before Budget Check

Already listed. Severity: MEDIUM.

### ❌ Reshape Without Atomic Boundary Wait

Already listed. Severity: CRITICAL.

### ❌ Cross-Volume XFC Without Volume Coordinator

Already listed. Severity: HIGH.

### ❌ Cohernce Monitor Only at Plan End

Already listed. Severity: HIGH.

---

### ❌ Incremental Population Without Deferred XFC Registry

```
Bad:  File A populated, file B not yet populated.
      Diagonal from file A to file B: cannot be registered (file B has no nodes).
      Skip the diagonal, continue with file A.
Good: Register PENDING_XFC entry in the PENDING_XFC_LIST.
      When file B population completes: resolve all matching PENDING_XFC entries.
      File A may execute but file B remains BLOCKED until XFC resolved AND file A DONE.
```

### ❌ Priority Queue Not Used (First-Available Node)

```
Bad:  Multiple nodes unblocked simultaneously → execute whichever appears first.
Good: Always score all unblocked candidates with CURSOR_PRIORITY().
      Execute in priority order.
      Without this: X=3 REDUCTIVE may execute before X=0 STRUCTURAL
      (if X=3 happens to appear first in the node list), causing invalid deletions.
```

### ❌ Session Handoff Resume Without Spot-Checks (Steps 5)

```
Bad:  Load snapshot → file hash matches → immediately resume execution.
Good: Load → verify → QUERY_4 + QUERY_5 + QUERY_2 → confirm state matches expectations
      → then resume.
      The file hash verifies the file's binary content but not:
      - whether the matrix node statuses are correct
      - whether the chain's pending_commit state is correct
      - whether blocked nodes are still legitimately blocked
      Spot-checks catch state corruption that file hash cannot.
```

### ❌ Volume Scheduler Yielding Mid-Chain

```
Bad:  VOL-P001 executing HCHAIN-...-5-0-0, budget pressure, yield to VOL-P002.
      VOL-P001 chain interrupted mid-execution.
Good: Volume yield only at:
      - Chain completion (cell boundary)
      - Gate node (explicit pause point)
      - File boundary
      NEVER yield mid-chain. A chain is the minimum yield-safe unit.
      Mid-chain yield leaves pending_commit=true with no snapshot,
      meaning rollback target is chain start (all work since chain start lost).
```

### ❌ Diagnostic Mode Modifying State

```
Bad:  During diagnostic QUERY_3, notice a node's replacement looks wrong →
      "fix" the replacement while in diagnostic mode.
Good: Diagnostic Mode is READ ONLY.
      Any fix discovered during diagnostics must be implemented via:
      Error Recovery (if mid-execution) or Population Engine node update (if still PENDING)
      through proper channels with full snapshot + integrity verification.
```

### ❌ Cross-Volume Lock in Non-Alphabetical Order

```
Bad:  VOL-P001 locks wallet.css first, then tries messages.css.
      VOL-P002 locks messages.css first, then tries wallet.css.
      → Classic deadlock: each volume holds one lock the other needs.
Good: All volumes acquire locks alphabetically (by file path).
      Both volumes would try messages.css first → one waits → no deadlock.
      The lock_order field in XFC registrations encodes this. Follow it.
```

---

## Master Checklist (Complete)

### Matrix Driver Initialization

```
□ Base Driver's GUIDE_REG populated with ARCHITECTURAL guides first?
□ Z=0 invariant nodes derived from guides and placed in shared layer?
□ Z=1 system nodes created and linked to Z=0?
□ Population Engine Phase A scaffold BEFORE Phase B nodes?
□ Phase E integrity check PASSED (7 checks, all green)?
□ MRO created with correct initial cursor position?
□ Viewport persistent zone loaded (Z=0 condensed + Z=1 refs)?
□ Context budget initialized with critical_reserve (default: 20k tokens)?
□ Volume registered with Volume Coordinator?
□ Priority Queue initialized (empty, ready for unblocked nodes)?
□ CHAIN_START snapshot saved before first chain executes?
```

### Each Node Execution

```
□ Budget checked (BEFORE loading node into viewport)?
□ Node loaded: FULL current + LITE ×3 lookahead + LITE ×3 lookbehind?
□ All pre_conditions verified (not assumed): ALL → PASS?
□ Lock confirmed: this file, this plan?
□ AEP step ①: pre_check → PASS before executing?
□ AEP step ②: rollback snapshot recorded before modifying?
□ AEP step ③: self_check → ALL post_conditions PASS?
□ AEP step ③-SEMANTIC (X=1 only): semantic equivalence confirmed?
□ AEP step ④: checkpoint saved if checkpoint_after=true?
□ DIFF_ENGINE.record_node_result() called?
□ COHERENCE_MONITOR.run_continuous() called?
□ CHAIN_EXECUTOR.on_node_complete() called (updates Z=4 counter)?
□ Cursor advanced (not left at completed node)?
```

### Each Chain Completion

```
□ DIFF_ENGINE.check_chain() run before committing?
□ Diff: missing_removals = []? missing_additions = []? contaminations = []?
□ Diff: diagonal_breaks = []?
□ All diagonal edges from this chain: in-flight updated to SOURCE_COMPLETE?
□ UNBLOCK_SCAN() run: any newly unblocked nodes added to priority queue?
□ Priority queue re-sorted?
□ CELL_CHECKPOINT saved (MSNAP with cell_states)?
□ Z=4 pass node status → DONE?
□ STATUS_EMITTER.emit_chain_complete() called?
```

### Each File Completion

```
□ All Z=5 nodes for this file: status DONE?
□ DIFF_ENGINE.run_full_pass(file) → clean?
□ COHERENCE_MONITOR.run_file_boundary(file) → all invariants SATISFIED?
□ FILE_CHECKPOINT (MSNAP) saved AND verified (sha256 match)?
□ LOCK_TABLE.release(file) called?
□ XFC_EXECUTOR.on_source_file_complete(file) called?
□ VIEWPORT_MANAGER.evict_file(file) called?
□ INTEGRATION_BRIDGE.sync_on_file_complete() called?
□ STATUS_EMITTER.emit_file_complete() called?
□ Volume Scheduler: any concurrent volumes now eligible for XFC unlock?
```

### Reshape Event

```
□ HALT_AT_NEXT_ATOMIC_BOUNDARY set before any Z-layer changes?
□ Current AEP allowed to complete before reshape begins?
□ RESHAPE_PRE snapshot saved AND verified before Step 3?
□ Old guide marked SUPERSEDED before new guide referenced?
□ Z=1 nodes updated to new guide reference?
□ New Z=0 invariant nodes created/updated?
□ All affected volumes notified (not just current)?
□ PENDING nodes re-derived (new post_conditions from new guide)?
□ DONE nodes checked for violations → remediation nodes generated if needed?
□ Non-conforming PENDING node replacements corrected to canonical?
□ Diagonal edges updated if replacement value changed?
□ Integrity re-check on affected chains (PENDING scope)?
□ HALT flag cleared?
□ Resume from RESHAPE_PRE snapshot (not from memory)?
□ emit_navigation() called after reshape?
```

### Session Handoff (Outgoing)

```
□ HALT_AT_NEXT_ATOMIC_BOUNDARY set (do not interrupt mid-AEP)?
□ EMERGENCY_CHECKPOINT saved before emitting resume prompt?
□ File hash verified IN SNAPSHOT (not just assumed)?
□ Resume prompt contains: snap_id, file_hash, cursor position, guide IDs+versions?
□ Resume prompt contains: pending XFC chains, in-flight diagonals, blocked nodes?
□ Resume prompt contains: completed files summary (which volumes are DONE)?
□ MRO.phase → SUSPENDED?
```

### Session Handoff (Incoming)

```
□ Guide IDs+versions from resume prompt loaded and verified?
□ Version mismatch → reshape protocol before rehydration?
□ VIEWPORT_MANAGER.rehydrate() run (includes file hash check)?
□ File hash MATCH confirmed (not just assumed)?
□ Chain state restored (H-chain position, diagonal in-flight, XFC pending)?
□ QUERY_4 run: invariant status matches expectation?
□ QUERY_5 run: diff state matches expectation?
□ QUERY_2 run: blocked nodes still legitimately blocked?
□ Discrepancy found → HALT (not proceed-and-hope)?
□ INCOMING_SESSION_READY emitted?
□ TRAVERSAL_ENGINE started fresh?
□ First action: verify pre_conditions for next node (do not assume)?
```

### Concurrent Volume Execution

```
□ DISJOINT overlap verified before parallel execution enabled?
□ Volume Scheduler initialized with all active MROs?
□ Shared Z=0/Z=1 accessed read-only by Traversal Engine?
□ Reshape handler acquires GLOBAL_Z0_Z1_LOCK before modifying shared layers?
□ All other volumes in READ_ONLY_MODE during Z=0/Z=1 update?
□ Lock acquisition order: always alphabetical (deadlock prevention)?
□ Volume yield only at chain boundary, gate, or file boundary?
□ Cross-volume XFC: target volume notified via Volume Coordinator (not directly)?
□ Consistency check run after each volume completes?
```

---

*Designed by analogy with:  
CPU fetch-decode-execute pipeline (Traversal Engine = instruction pipeline),  
virtual memory manager with TLB (Viewport Manager = MMU + zone-based eviction),  
hardware watchdog timer + ECC memory (Coherence Monitor = combined integrity watchdog),  
filesystem journal with fsck (Diff Engine = structural integrity checker + repair),  
FPGA partial reconfiguration at runtime (Reshape Handler = live circuit modification),  
SMP MESI cache coherence protocol (Volume Coordinator = multi-core coherence fabric),  
NVRAM journaling with write-ahead log (Checkpoint Manager = atomic commit + verify),  
OS process scheduler with priority queue (Volume Scheduler + Cursor Priority Queue),  
CPU program counter + prefetch buffer (Cursor + Viewport lookahead/lookbehind),  
and POSIX signal handling (Diagnostic Mode = SIGSTOP + read-only inspection).*


temp-skill-ai-guide.md:
---------------------------------
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
