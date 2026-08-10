---
name: llm-assembler
description: Reliable, auditable batch editing of source code and text files, line by line. Use whenever a task involves several line-precise edits -- renaming an identifier everywhere it appears, restructuring blocks, multi-file refactors, inserting/deleting/moving/replacing many lines, or a structured audit/conformance sweep prioritized by category and severity -- especially when edits must stay consistent with each other, survive a dropped or compacted conversation, or need to be provably complete rather than self-reported. Provides stable line IDs immune to line-number drift, idempotent atomic descriptors, protected-zone constraints, a three-phase validator (plan-time, per-op, post-condition) checking the batch before and after applying it, a write-ahead log and checkpoint for safe resumption, and a CLI keeping position tracking, hashing, and file writes in deterministic code instead of model arithmetic. Skip for a single one-line fix -- reach for it once edits multiply, need prioritizing, or need to be trusted.
---

# llm-assembler

*Part of the **LLM Operational Platform** (Operational Platform for
short) -- the tool that implements its task-execution methodology.
`references/methodology-mapping.md` maps the methodology's phases onto
the commands below; the full methodology on its own, with no mention of
this tool, lives in `llm-operational-platform-task-execution-methodology.md`.*

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
| descriptor | One atomic edit: an op, a target (by id), and the content it expects to find there. The unit `apply-next` applies. Optionally tagged with `category` and `severity`, and with `provenance` (`direct` or `domino`) once the domino coprocessor is in use. |
| batch | A set of descriptors meant to be checked and applied together. |
| taxonomy | A batch's declared, closed set of category codes — defined before descriptors reference one, the same "define it before you search for it" discipline as the invariants below. |
| constraint | A protected range a batch must not touch, checked at plan-time. |
| finding | A `direct`-provenance descriptor queued for domino tracing — not a new kind of object, the same descriptor, viewed as "still owes a cascade check." |
| domino coprocessor | Traces each finding for cascading, related locations elsewhere in the material, mechanically surfacing candidates and gating the plan until every finding is traced. |
| invariant | A completeness criterion for a batch -- "N occurrences of X should remain" -- declared separately from the descriptors it checks. |
| WAL | Append-only log of what started and what finished applying. What makes resuming after an interruption safe. |
| checkpoint | Where things stood as of the last phase transition. The first thing to read in a fresh session. |

Full field-by-field detail: `references/file-formats.md`.
Full command reference: `references/cli-reference.md`.
Mapping onto the abstract six-phase methodology this skill implements:
`references/methodology-mapping.md`.

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

If part of a file must not be touched by this batch — vendored code, a
section someone else owns, anything out of scope on purpose — declare it
now, before analysis starts, the same Phase-0 spirit as loading the
material itself:

```
python3 scripts/cli.py add-constraint <batch_id> --file path/to/file.py \
    --start <id> --end <id> --reason '...'
```

This needs an open batch, so in practice it comes right after step 2
below, not literally before it — the ordering that matters is "before any
descriptor could violate it," not "before `new-batch`." Most batches
don't need this at all; reach for it when there's a specific region you
already know must stay untouched.

### 2. Open a batch

```
python3 scripts/cli.py new-batch
```

One batch per logically-related set of edits -- a rename, a refactor, a
restructuring. Unrelated edits to unrelated parts of a codebase don't need
to share a batch; a batch's job is to let you check that *these specific*
edits are mutually consistent, not to be a container for everything you
do in a session.

### 3. If this is an audit-shaped task, declare a taxonomy first

```
python3 scripts/cli.py add-category <batch_id> --code NAMING --description '...'
```

Optional, and worth skipping for a small, single-purpose batch -- a plain
rename doesn't need a category system. Declare one when the task itself
has the shape of "find and classify issues" rather than "make this one
specific change": a conformance sweep, a diagnostic audit, anything where
knowing *what kind* of issue each fix addresses matters as much as the
fix itself. Declare every code before writing any descriptor that uses
it -- `add-descriptor --category` checks against whatever's been declared
so far and refuses one that isn't, by design: a category invented on the
fly, after the fact, isn't a taxonomy, it's a label.

### 4. Analyze systematically, then record each finding as a descriptor

```
python3 scripts/cli.py show-file path/to/file.py
python3 scripts/cli.py add-descriptor <batch_id> --op replace_range --file path/to/file.py \
    --start <id> --end <id> --payload-text '...' [--category CODE] [--severity LEVEL]
```

These are two different activities worth keeping mentally separate even
though they happen back to back. First: read the material and decide
what's actually wrong -- against a reference standard, against a taxonomy
from step 3, against whatever the task defines as correct. Second: record
each finding precisely enough that it can be checked and applied without
you having to remember or re-derive it. The second half is mechanical;
the first half is the one piece of this whole workflow that's genuinely
yours to reason about.

Use `show-file` to get real, current ids rather than guessing at line
numbers. The five ops are `insert_after`, `delete_range`, `replace_range`,
`move_range`, `copy_range` -- see `references/cli-reference.md` for the
exact arguments each one takes. Tag `--severity` (`critical` / `major` /
`minor` / `cosmetic`) once a batch has more than a few descriptors that
aren't all equally urgent -- it changes execution order, not just
bookkeeping (see "Execution order" in `references/cli-reference.md`). If
two descriptors in the batch would touch the same lines, decide which
must go first and say so with `--depends-on`; the planner will catch it
if you don't, and refuse to guess on your behalf.

If, while analyzing one thing, you notice that fixing it would require
touching something else you haven't written a descriptor for yet, add
that second descriptor now rather than trusting yourself to remember it
once the batch has grown to thirty items. The next step exists
specifically to catch what you *don't* notice while analyzing.

### 5. Trace every direct finding for cascades before declaring the map done

```
python3 scripts/cli.py sync-domino-queue <batch_id>
python3 scripts/cli.py domino-next <batch_id>
# reason about the candidates it returns; for every real cascade:
python3 scripts/cli.py add-descriptor <batch_id> --op ... --provenance domino --domino-of <descriptor_id> ...
python3 scripts/cli.py domino-resolve <batch_id> <finding_id>
# repeat domino-next / domino-resolve until domino-status reports ready_for_plan
```

For every descriptor added in step 4, something else in the material may
depend on what it's changing -- another reference to the same identifier,
another consumer of the value, another place implementing the same rule.
Missing one of these doesn't fail loudly; it produces a batch that's
internally consistent and still wrong, because whatever it missed is
still there afterward, unchanged, now inconsistent with everything that
did change. This is exhaustive on purpose, not sampled and not skipped
for cheap-looking findings -- a missed cascade is exactly as broken
whether the finding that missed it looked trivial or not.

`sync-domino-queue` is idempotent -- it queues every finding added since
the last time you ran it and leaves everything else alone, so it's safe
to call again if step 4 continues after you've started tracing.
`domino-next` does the part that's worth not doing by hand: it searches
every registered file, not just the ones this batch already touches, for
other occurrences of what the finding is changing (its `domino_hint` if
you gave one when adding the descriptor, otherwise the literal current
content), and hands back only what isn't already covered by some
descriptor already in the batch. That search is mechanical and exhaustive
by construction; deciding which of its candidates are real cascades and
which are coincidental is not, and stays yours. Add a descriptor for each
real one, tagged `--provenance domino --domino-of <the finding's
descriptor_id>`, before calling `domino-resolve` -- resolving doesn't
take your word for how many you found, it independently counts
descriptors that actually reference the finding and records that number,
the same way nothing else in this system trusts a self-report over the
actual state on disk.

This step is a gate, not a suggestion: `validate-plan` in step 7 refuses
outright, before touching anything else, if any finding is still
untraced. A batch that never calls `sync-domino-queue` at all is
unaffected by any of this -- the gate only exists once you've opted in by
starting the queue.

Because each `domino-next` call is meant to be backed by a real look at
the material rather than a glance, treat interruption here the same way
you'd treat it mid-`apply-next`: `domino-resolve` is WAL-backed and
idempotent, and `checkpoint.json` tracks how many findings are still
pending, so a dropped session picks back up mid-trace rather than
repeating findings you already resolved. See `references/limitations.md`
for what the mechanical candidate search does and doesn't catch.

### 6. Declare what "complete" means -- before checking the plan

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

### 7. Validate the plan -- and don't proceed past a failure

```
python3 scripts/cli.py validate-plan <batch_id>
```

Checks that every domino finding is traced, checks every descriptor's
shape, resolves every target against the live registry, confirms nothing
touches a declared constraint, and works out a dependency-safe order --
or reports exactly which findings are still untraced, or which
descriptors conflict, form a cycle, or reach into protected territory.
This is the cheapest point in the whole process to catch a mistake,
because nothing has been touched yet. If it fails, fix the batch (finish
tracing, add a `--depends-on`, drop a redundant descriptor, re-check a
target id) and validate again. There's no "apply anyway" path --
`apply-next` won't do anything useful without a validated plan.

### 8. Apply, one descriptor at a time, and read each result

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

### 9. Check the post-condition

```
python3 scripts/cli.py validate-post <batch_id>
```

Only meaningful once every descriptor shows `applied`. Checks syntax
validity of every file the batch touched, and re-derives every invariant
from step 5 fresh from disk -- not from anything the batch claimed about
itself. For each invariant, the result includes concrete matches (line +
text), not just a pass/fail count, because a surviving match isn't
automatically a real problem -- some may be legitimate exceptions, and
telling the two apart is a judgment call this step deliberately leaves to
you rather than making silently. A failure here does not undo what was
applied; see `references/limitations.md`. If something was genuinely
missed, the fix is a small follow-up batch closing that specific gap,
planned and validated the same way as any other.

### 10. Report what actually happened

Summarize from the tool's output, not from memory of composing the batch
-- `status <batch_id>` and the `validate-post` result are the facts; what
you intended a few steps ago isn't.

## Adapting to task shape

The workflow above is the same nine steps regardless of what the task
is, but which steps carry the weight shifts with its shape:

- **Conformance transformation** (bring material into line with a
  standard) -- one taxonomy category per deviation type from the
  reference; batch by unit (file, or natural subdivision); an invariant
  per category confirming the pattern that defines it is gone.
- **Diagnostic audit** (assess quality or risk, not fix one known thing)
  -- lean on `severity` more than `category` for ordering, since the
  question is "what's worth doing first," not "what kind of thing is
  this"; batch by dimension rather than by file.
- **System transition** (move from one approach/interface to another) --
  register everything that references what's moving before writing any
  descriptor; `add-constraint` anything not ready to change yet; the
  domino coprocessor is doing real work here -- most transitions live or
  die on whether every reference to what's moving got found; isolate
  breaking changes into their own batch; `validate-post` after every
  batch, not only at the end of the whole transition.
- **Global rename / terminology change** -- domino tracing *is* the
  discipline here: give each rename's descriptor a `--domino-hint` of the
  exact old name so the mechanical search has something precise to look
  for, then let the queue surface every other file that uses it. One
  `add-invariant --pattern <old> --expected-count 0` per touched file is
  the completeness check that catches whatever domino tracing still
  missed; between the two, the risk this skill actually mitigates here --
  a rename that's internally consistent but not exhaustive -- gets caught
  twice, not once.

Full detail and the mapping back to the abstract methodology phases:
`references/methodology-mapping.md`.

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

**A finding with zero mechanical candidates isn't automatically a
finding with zero cascades.** `domino-next`'s candidate list is a search
result, not a verdict -- it only surfaces what shares text with the
finding's old content or its `domino_hint`. A purely conceptual
dependency with no shared wording won't show up on its own; if you have
reason to think one exists, look for it the same way you'd look for
anything else, and add the descriptor regardless of what the mechanical
list found. Resolving a finding records that it was traced, not that
nothing was there.

## If something goes wrong

`python3 scripts/cli.py resume` first, always. It reads `checkpoint.json`,
checks the real status of the active batch, and -- if the last thing that
happened was an abort -- pulls the actual diagnostic out of
`validation_log.jsonl` instead of making you go find it.

## Reference

- `references/cli-reference.md` -- every command, every argument, in full.
- `references/file-formats.md` -- the exact shape of every file under `.llm-assembler/`.
- `references/methodology-mapping.md` -- how these commands satisfy each phase of the abstract six-phase methodology this skill implements.
- `references/limitations.md` -- what this deliberately doesn't do yet, and why.
