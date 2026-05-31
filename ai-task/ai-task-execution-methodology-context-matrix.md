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
