# docgenerator.skill

This is **Project 2** of the `docgenerator` bundle — a [Claude Agent
Skill](https://www.anthropic.com/) version of the documentation generator.
See the [top-level README](../README.md) for how it relates to
`doc-generator-cli/`, the plain standalone script.

**If you're a person browsing this folder:** the file that actually
matters is [`SKILL.md`](./SKILL.md) — that's the whole skill definition
(when an LLM agent should use it, how, and what to watch out for). This
README is just a signpost for humans; agents read `SKILL.md` directly, not
this file.

## What's here

```
docgenerator.skill/
├── SKILL.md              the skill itself: frontmatter + instructions
├── scripts/
│   └── doc_generator.py  a synced copy of the generator (self-contained on purpose)
├── references/           loaded by the agent only when actually needed
│   ├── architecture.md       how the parsing/analysis pipeline works
│   ├── output-guide.md       what each part of the generated doc means
│   ├── limitations.md        known blind spots, and how to talk about them
│   └── customization.md      how to retheme/extend the generator
└── evals/
    └── evals.json         draft test prompts (functional quality checks)
```

## Installing / using this skill

Drop this folder wherever your Claude setup looks for skills (for example,
a `skills/` directory that Claude Code, the API, or another agent harness
is configured to load from), or package it into a distributable archive
with Anthropic's `skill-creator` packaging script if your workflow expects
one. Once loaded, an agent decides to use it automatically based on the
`description` field in `SKILL.md`'s frontmatter — there's no separate
"activation" step.

## Keeping this in sync with the CLI project

`scripts/doc_generator.py` here is a **copy**, not a symlink or reference —
skills need to be self-contained so this folder can be extracted and
installed on its own, without the sibling `doc-generator-cli/` folder
needing to exist. The canonical, actively-maintained copy is
`../doc-generator-cli/doc_generator.py`; if you patch the generator, copy
the change into both places, or diff them before assuming they still
match. The `VERSION` constant near the top of the script is the quickest
way to eyeball whether the two have drifted.

## Validation status

Run against the actual `skill-creator` tooling, not just eyeballed:

- **`scripts/quick_validate.py`: passes** (`Skill is valid!`). This caught
  two real issues on the first pass — the `description` had literal `<`/`>`
  characters (not allowed in frontmatter) and was 1176 characters against a
  1024 limit — both fixed in `SKILL.md` directly.
- **`scripts/package_skill.py`: succeeds**, producing a real
  `docgenerator.skill.skill` archive (validates before packaging, so this
  confirms the validation result rather than duplicating it). `evals/` is
  excluded from the package by that script's own design — it's a
  development artifact, not something the running skill needs.
- **`evals/evals.json`: traced manually, not run automatically.** The real
  eval loop (`run_eval.py`/`run_loop.py`) needs a `claude` CLI with API
  access, which this environment doesn't have. `evals/manual-trace-results.md`
  walks through each of the 5 prompts against the actual instructions in
  `SKILL.md` and its references, and is explicit about the difference
  between that and a real execution transcript — including one specific,
  plausible gap it found (in eval 4) that a real run would need to confirm
  before it's worth acting on.
- **Description-optimization loop (`improve_description.py`): not run**,
  same infrastructure constraint. The manual trace's "What a real run
  would still add" section lists a few near-miss queries reasoned about
  informally instead.

In short: everything that's checkable without spinning up a second Claude
agent has been checked and fixed. What's left needs that infrastructure,
not more effort in this format.
