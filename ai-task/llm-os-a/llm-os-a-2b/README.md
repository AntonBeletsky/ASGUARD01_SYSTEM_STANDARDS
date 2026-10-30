# README

**Operational Platform** is
the name of this project: a six-phase task-execution methodology and a
tested implementation of it (`operational-platform`, a skill for line-precise
batch editing of text and code).

This delivery contains **two independent, complete packagings of the same
underlying work**. They are not sequential — Set B doesn't supersede Set
A, Set A isn't a summary of Set B. They're the same content, organized
two different ways for two different uses. Pick whichever fits; nothing
here requires using both.

## Files at a glance

| File | Set | Lines | What it is |
|---|---|---|---|
| `operational-platform-task-execution-methodology-full-in-one-file-md.md` | **A** | ~1210 | Methodology + implementation, merged into one document |
| `operational-platform-task-execution-methodology.md` | **B** | ~395 | Methodology alone, implementation-agnostic |
| `operational-platform.md` | **B** | ~520 | The tool's operating instructions, readable copy |
| `operational-platform.skill` | **B** | — | The tool itself, packaged and installable |

## Set A — one merged, self-contained document

**`operational-platform-task-execution-methodology-full-in-one-file-md.md`**

The methodology and the implementation woven together, phase by phase, in
a single file. Every abstract requirement (Phase 0's context loading,
Phase 1.3's cascade tracing, Phase 3's execution ordering, and so on) is
immediately followed by the concrete command, field, or JSON file of
`operational-platform` that satisfies it, plus a full CLI reference, full file
format reference, checklist, and anti-patterns section — all in the same
file. Reading only this document is enough; nothing else in this package
is required to understand or use it.

Reach for this when you want everything in one place and don't mind a
long document, or when you're handing this to someone else and want to
avoid explaining "read these three files, in this order."

## Set B — the same content, kept in separate, reusable layers

**`operational-platform-task-execution-methodology.md`**
The methodology alone — six phases, their required outputs, the rules
governing them — with zero mention of text editing, code, JSON, or any
other implementation detail. Written so it can be handed to a different,
domain-specific implementation for something that isn't line-oriented
text at all (a different kind of audit, a different kind of transform)
without needing to be edited first.

**`operational-platform.md`**
The operating instructions for the actual tool — what to run, in what
order, and why. A human-readable copy of the file that lives inside the
packaged skill below (`SKILL.md`). Read this if you want to understand or
use the tool without installing it.

**`operational-platform.skill`**
The same tool, packaged and ready to install: `SKILL.md` plus the working
Python engine (`scripts/`, seven modules, standard library only) plus
detailed references (`references/`, including `methodology-mapping.md` —
the same phase-by-phase mapping that Set A weaves inline, kept here
instead as its own file for exactly the domain-separation reason above).
This is the file that actually *does* anything; `operational-platform.md` is a
readable copy of one part of it.

Reach for this set when you want to reuse the methodology document
somewhere the tool doesn't apply, when you want to actually install and
run the tool, or when you'd rather read one short, focused document at a
time than one long one.

## Where the name shows up

**Operational Platform** is the project name, and `operational-platform` is
the installable skill: its `name:` field, the `.skill` file, and the
`.operational-platform/` state directory it creates inside a project being
edited. The merged document in Set A and the standalone methodology
document in Set B both open with the project name, and
`operational-platform.md`'s own opening line points back to the
methodology it implements.

Earlier versions used two different names -- `llm-assembler` for the tool
and "LLM Operational Platform" for the project. Both are now simply
Operational Platform. A project that already has an older `.llm-assembler/`
state directory is still found and used as it is, rather than silently
starting over beside it; new state goes to `.operational-platform/`.

## Which one is "the real one"

Both — they describe the same tested code. Nothing in Set A states a
behavior that Set B's implementation doesn't actually have, and vice
versa; Set A was written from the finished, tested state of Set B, not
the other way around. The difference between them is packaging, not
content: one file versus three, merged versus layered. Pick based on how
you intend to use it, not on which one seems more authoritative.
