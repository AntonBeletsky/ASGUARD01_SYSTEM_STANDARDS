# README

This delivery contains **two independent, complete packagings of the same
underlying work**: a six-phase task-execution methodology and a tested
implementation of it (`llm-assembler`, a skill for line-precise batch
editing of text and code). They are not sequential — Set B doesn't
supersede Set A, Set A isn't a summary of Set B. They're the same
content, organized two different ways for two different uses. Pick
whichever fits; nothing here requires using both.

## Files at a glance

| File | Set | Lines | What it is |
|---|---|---|---|
| `llm-os-task-execution-methodology-full-in-one-file-md.md` | **A** | ~900 | Methodology + implementation, merged into one document |
| `llm-os-task-execution-methodology.md` | **B** | ~320 | Methodology alone, implementation-agnostic |
| `llm-assembler.md` | **B** | ~315 | The tool's operating instructions, readable copy |
| `llm-assembler.skill` | **B** | — | The tool itself, packaged and installable |

## Set A — one merged, self-contained document

**`llm-os-task-execution-methodology-full-in-one-file-md.md`**

The methodology and the implementation woven together, phase by phase, in
a single file. Every abstract requirement (Phase 0's context loading,
Phase 1's taxonomy, Phase 3's execution ordering, and so on) is
immediately followed by the concrete command, field, or JSON file of
`llm-assembler` that satisfies it, plus a full CLI reference, full file
format reference, checklist, and anti-patterns section — all in the same
file. Reading only this document is enough; nothing else in this package
is required to understand or use it.

Reach for this when you want everything in one place and don't mind a
long document, or when you're handing this to someone else and want to
avoid explaining "read these three files, in this order."

## Set B — the same content, kept in separate, reusable layers

**`llm-os-task-execution-methodology.md`**
The methodology alone — six phases, their required outputs, the rules
governing them — with zero mention of text editing, code, JSON, or any
other implementation detail. Written so it can be handed to a different,
domain-specific implementation for something that isn't line-oriented
text at all (a different kind of audit, a different kind of transform)
without needing to be edited first.

**`llm-assembler.md`**
The operating instructions for the actual tool — what to run, in what
order, and why. A human-readable copy of the file that lives inside the
packaged skill below (`SKILL.md`). Read this if you want to understand or
use the tool without installing it.

**`llm-assembler.skill`**
The same tool, packaged and ready to install: `SKILL.md` plus the working
Python engine (`scripts/`, five modules, standard library only) plus
detailed references (`references/`, including `methodology-mapping.md` —
the same phase-by-phase mapping that Set A weaves inline, kept here
instead as its own file for exactly the domain-separation reason above).
This is the file that actually *does* anything; `llm-assembler.md` is a
readable copy of one part of it.

Reach for this set when you want to reuse the methodology document
somewhere the tool doesn't apply, when you want to actually install and
run the tool, or when you'd rather read one short, focused document at a
time than one long one.

## Which one is "the real one"

Both — they describe the same tested code. Nothing in Set A states a
behavior that Set B's implementation doesn't actually have, and vice
versa; Set A was written from the finished, tested state of Set B, not
the other way around. The difference between them is packaging, not
content: one file versus three, merged versus layered. Pick based on how
you intend to use it, not on which one seems more authoritative.
