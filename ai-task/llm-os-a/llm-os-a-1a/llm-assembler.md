---
name: llm-assembler
description: Reliable, auditable batch editing of source code and text files, line by line. Use this skill whenever a task involves several line-precise edits to code -- renaming an identifier everywhere it appears, restructuring or reordering blocks, multi-file refactors, inserting/deleting/moving/replacing many lines -- especially when the edits must stay consistent with each other, must survive a dropped or compacted conversation, or need to be provably complete rather than self-reported. Provides stable line IDs immune to line-number drift, idempotent atomic edit descriptors, a three-phase validator (plan-time, per-operation, post-condition) that independently checks the batch before and after applying it, a write-ahead log and checkpoint for safe resumption, and a CLI that keeps position tracking, hashing, and file writes in deterministic code instead of model arithmetic. Skip this for a single one-line fix -- reach for it once edits multiply or need to be trusted.
---

# llm-assembler

Batch, line-precise editing of code and text files, done through a small
deterministic engine instead of rewriting file content directly yourself.
You decide *what* changes; the engine handles *positions, hashing, and
file writes* -- the parts of this kind of task that are tedious, exact,
and easy to get quietly wrong across many edits in a row. Python 3
standard library only, no dependencies to install.

## When to reach for this

Use it when an edit involves several line-precise changes that need to
stay consistent with each other -- renaming something everywhere it
appears, restructuring a block, a refactor touching many lines or several
files -- especially if the work might get interrupted partway through, or
you need to be able to show it was actually complete rather than just
asserting so.

Don't reach for it for a single, obvious one-line fix. Editing the file
directly is faster, and the overhead of registering it, opening a batch,
and validating a plan buys you nothing when there's nothing to get
inconsistent.

## Why not just edit the file directly

Line numbers drift the moment you make more than one edit: insert two
lines near the top of a file and every line number below it is now wrong,
including the ones in whatever plan you made before starting. If a later
edit in the same pass still refers to the old numbers, it silently lands
on the wrong line. This skill sidesteps that by never addressing a line
by its number -- every line gets a permanent `line_id` the moment its file
is registered, and every descriptor targets an id, not a number. Resolving
an id to "where is it *right now*" is one small, mechanical lookup --
exactly the kind of bookkeeping that's safe to hand to code and risky to
do by counting across a long batch yourself.

## Core concepts

| Term | What it is |
|---|---|
| registry | `line_id -> current position`, one entry per registered file. The address book everything else is built on. |
| descriptor | One atomic edit: an op, a target (by id), and the content it expects to find there. The unit `apply-next` applies. |
| batch | A set of descriptors meant to be checked and applied together. |
| invariant | A completeness criterion for a batch -- "N occurrences of X should remain" -- declared separately from the descriptors it checks. |
| WAL | Append-only log of what started and what finished applying. What makes resuming after an interruption safe. |
| checkpoint | Where things stood as of the last phase transition. The first thing to read in a fresh session. |

Full field-by-field detail: `references/file-formats.md`.
Full command reference: `references/cli-reference.md`.

## Workflow

All commands: `python3 scripts/cli.py <command> ...`, run from inside the
project you're editing.

### 0. If `.llm-assembler/` already exists, resume first

```
python3 scripts/cli.py resume
```

Before writing or applying anything, check whether there's already work
in progress -- from this conversation compacting, or a previous session.
`resume` reads the checkpoint and reports the real state of the active
batch plus a concrete next command. If the last thing that happened was
an abort, it surfaces why. Don't assume a fresh start; ask.

### 1. Register the file(s) you're about to touch

```
python3 scripts/cli.py register path/to/file.py
```

Safe to call even if you're not sure it's already registered -- it's a
no-op on a file that already is. Do this for every file a batch will
reference before writing descriptors against it, since a descriptor needs
real ids to target.

### 2. Open a batch

```
python3 scripts/cli.py new-batch
```

One batch per logically-related set of edits -- a rename, a refactor, a
restructuring. Unrelated edits to unrelated parts of a codebase don't need
to share a batch; a batch's job is to let you check that *these specific*
edits are mutually consistent, not to be a container for everything you
do in a session.

### 3. Decide what to change, and write it as descriptors

```
python3 scripts/cli.py show-file path/to/file.py
python3 scripts/cli.py add-descriptor <batch_id> --op replace_range --file path/to/file.py \
    --start <id> --end <id> --payload-text '...'
```

This is the one step in the whole workflow that's actually yours to
reason about -- everything before and after it is mechanical. Use
`show-file` to get real, current ids rather than guessing at line numbers.
The five ops are `insert_after`, `delete_range`, `replace_range`,
`move_range`, `copy_range` -- see `references/cli-reference.md` for the
exact arguments each one takes. If two descriptors in the batch would
touch the same lines, decide which must go first and say so with
`--depends-on`; the planner will catch it if you don't, and refuse to
guess on your behalf.

### 4. Declare what "complete" means -- before checking the plan

```
python3 scripts/cli.py add-invariant <batch_id> --file path/to/file.py \
    --pattern 'old_name' --expected-count 0 --description '...'
```

This step is the easiest to skip and the most worth not skipping. A batch
can be perfectly self-consistent -- every descriptor valid, nothing
conflicting -- and still miss something, because a plan has no way to
notice its own blind spot. The fix isn't a smarter plan; it's a criterion
that comes from somewhere other than the plan. Before writing this, go
check the actual file yourself -- search for the pattern you're touching
-- rather than trusting your own count of how many descriptors you just
wrote. If you determine "how many places need to change" the same way you
decided what those places were, a gap in one is a gap in both, and this
check will pass while still being wrong.

Not every batch needs one. A single, self-contained edit doesn't have a
"did I get all of them" question to ask. A rename, a find-and-replace
style change, or anything with a "make sure none of the old X remain"
character does.

### 5. Validate the plan -- and don't proceed past a failure

```
python3 scripts/cli.py validate-plan <batch_id>
```

Checks every descriptor's shape, resolves every target against the live
registry, and works out a dependency-safe order -- or reports exactly
which descriptors conflict or form a cycle. This is the cheapest point in
the whole process to catch a mistake, because nothing has been touched
yet. If it fails, fix the batch (add a `--depends-on`, drop a redundant
descriptor, re-check a target id) and validate again. There's no "apply
anyway" path -- `apply-next` won't do anything useful without a validated
plan.

### 6. Apply, one descriptor at a time, and read each result

```
python3 scripts/cli.py apply-next <batch_id>
```

Loop this until the batch is done. Each call returns one of `applied`,
`skipped`, `recovered`, or `abort`:

- `applied` / `skipped` / `recovered` -- keep going.
- `abort` -- stop. The file was left untouched. The detail tells you the
  live content matched neither what was expected before nor after the
  edit, which means something changed this file outside the batch.
  Re-plan (re-register if the file genuinely changed, open a fresh batch)
  rather than retrying the same call expecting a different result.

`apply-all` runs this loop for you and stops at the first abort, if you'd
rather not handle each result individually -- reasonable for a batch
you're confident in, less useful when you want the chance to react to
each step.

### 7. Check the post-condition

```
python3 scripts/cli.py validate-post <batch_id>
```

Only meaningful once every descriptor shows `applied`. Checks syntax
validity of every file the batch touched, and re-derives every invariant
from step 4 fresh from disk -- not from anything the batch claimed about
itself. A failure here does not undo what was applied; see
`references/limitations.md`. If an invariant failed because something was
genuinely missed, the fix is a small follow-up batch closing that specific
gap, planned and validated the same way as any other.

### 8. Report what actually happened

Summarize from the tool's output, not from memory of composing the batch
-- `status <batch_id>` and the `validate-post` result are the facts; what
you intended a few steps ago isn't.

## Rules of the road

**Let the engine compute hashes and touch files -- never do either
yourself mid-batch.** If you hand-edit a file the engine has an open batch
for, or write a value into `expect_hash` yourself, the registry and the
file go out of sync, and the next hash check either fails a perfectly
fine edit or -- worse -- happens to pass one it shouldn't. Checking "does
reality match what I expect" is only meaningful if the file's actual
history matches what the tool recorded.

**Don't hand-edit anything under `.llm-assembler/`.** Every file there is
written by exactly one part of the system for a reason -- `wal.jsonl` only
by the engine, `validation_log.jsonl` only by the validator, so neither
can forge the other's verdict. A hand edit breaks that guarantee silently.

**A validated plan is a snapshot, not a promise.** Between validating and
applying, nothing stops the world from changing (a hand-edit, another
process). That's what the per-operation hash check on every `apply-next`
call is for -- treat an `abort` as the check doing its job, not as a bug.

**Small batches are easier to recover from than large ones.** Nothing
technical stops fifty descriptors in one batch, but a batch that fails
post-condition partway through is easier to understand and fix at ten
descriptors than at fifty.

## If something goes wrong

`python3 scripts/cli.py resume` first, always. It reads `checkpoint.json`,
checks the real status of the active batch, and -- if the last thing that
happened was an abort -- pulls the actual diagnostic out of
`validation_log.jsonl` instead of making you go find it.

## Reference

- `references/cli-reference.md` -- every command, every argument, in full.
- `references/file-formats.md` -- the exact shape of every file under `.llm-assembler/`.
- `references/limitations.md` -- what this deliberately doesn't do yet, and why.
