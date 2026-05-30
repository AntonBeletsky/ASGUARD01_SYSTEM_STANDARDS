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
