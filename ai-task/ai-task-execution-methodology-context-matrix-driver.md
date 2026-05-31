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
