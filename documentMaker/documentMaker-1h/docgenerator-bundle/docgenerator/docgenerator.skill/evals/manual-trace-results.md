# Manual instruction trace (not an automated eval run)

**What this is, and isn't.** The real eval loop (`scripts/run_eval.py` /
`run_loop.py`) spawns a fresh subagent — one that has loaded *only* this
skill, none of this conversation's context — actually executes each prompt
in `evals.json`, and grades the resulting transcript with a separate
grader subagent (`agents/grader.md`). That requires a `claude` CLI with API
access; neither was available in the sandbox this skill was built in
(checked directly: no `claude` binary on PATH, no `ANTHROPIC_API_KEY` set).

What follows instead is a manual trace: for each eval prompt, tracing
which instruction in `SKILL.md` (and its referenced files) would fire, and
whether following it actually produces the `expected_output`. This is
weaker evidence than a real transcript — it checks that the instructions
*say* the right thing, not that an agent *actually does* the right thing
when it matters (skips a step, misreads a file path, etc.). Treat every
verdict below as provisional until it's been through the real loop.

## Eval 1 — "document this old landing page, something I can open in a browser"

Squarely **Mode A** per `SKILL.md`: an explicit file request. "Running it"
gives the exact command; "After running it (Mode A)" explicitly says to
present the file and give a short orientation, "not a re-description of
every section." Matches `expected_output` directly.

**Verdict: PASS** (high confidence — this is the most-covered path in the
whole skill).

## Eval 2 — "handing this repo to a contractor" (no word "documentation")

The `description` field lists "onboard me to this repo" as a literal
trigger example, and this prompt is a close paraphrase of it.

**Verdict: PASS**, with one caveat worth flagging: neither `SKILL.md` nor
the description over-specifies *how* to recognize novel phrasings of Mode
A — it relies on the agent generalizing from the listed examples rather
than pattern-matching a fixed list. That's the right design (skill-creator
explicitly warns against overly narrow, example-listing instructions), but
it also means this eval is really testing the agent's general judgment as
much as the skill's instructions — worth keeping in the eval set anyway,
since a real run would surface whether that judgment call actually goes
the right way in practice.

## Eval 3 — "does script.js touch about.html or only index.html?"

**Mode B**, and the best-covered case in the skill: "Using it as an
analysis tool (Mode B)" instructs importing the script's functions for
ground truth rather than reading source by eye, and
`references/architecture.md`'s "Function reference for direct import"
section uses almost this exact question as its worked example.

**Verdict: PASS** (high confidence).

## Eval 4 — React/TSX + Vite project

`SKILL.md` explicitly says to check `references/limitations.md` "before
promising results" for framework-heavy projects; `limitations.md` has a
dedicated section naming this exact stack and instructing the agent to
say so *upfront*, plus a closing section clarifying it's fine to still run
the tool for the parts it can see (plain CSS, vanilla JS, the file tree)
while being clear the component-level story is missing.

**Verdict: PASS**, with a real gap worth noting: `SKILL.md`'s own phrasing
("see the caveats... before promising results") could be followed by an
agent that reads it as a reason to *skip running the tool entirely* rather
than "run it, but caveat honestly" — the resolving instruction lives one
hop away in `limitations.md`, not in `SKILL.md` itself. This is a plausible
failure mode a real eval run could catch that this trace can only guess
at. Worth considering pulling that one clarifying sentence up into
`SKILL.md` directly if a real run shows agents under-running the tool here.

## Eval 5 — files actually under `./project/vendor/webapp`

`SKILL.md`'s "Before running it" section covers this almost word-for-word,
down to naming `vendor` specifically as a default-ignored directory to
check for — not a coincidence: this instruction was written after hitting
exactly this failure mode while testing the underlying script (a test file
placed under a `vendor/` folder was silently skipped by
`DEFAULT_IGNORE_DIRS`).

**Verdict: PASS** (highest confidence of the five — grounded in an actual
prior failure, not a hypothetical).

## Summary

5/5 pass on instruction-trace grounds; 2 of the 5 (evals 2 and 4) surfaced
a genuine, specific weakness worth watching in a real run rather than a
clean pass — both noted above rather than smoothed over. No changes made
to `SKILL.md` based on this trace alone; the eval-4 gap is flagged as a
candidate fix to make *if* a real run confirms it, not applied speculatively.

## What a real run would still add

- Whether the agent actually resolves `scripts/doc_generator.py` correctly
  relative to wherever this skill ends up mounted (untestable without a
  real harness to mount it in)
- Whether prompt 2's reliance on generalization actually holds up
  in practice, per the caveat above
- A real quantitative check on `description` trigger precision/recall
  (`improve_description.py`'s job) against near-miss queries — e.g.
  "fix this bug in script.js", "convert this HTML page to a PDF", "write
  API docs for our Django backend" — that this trace can reason about
  informally (none of the three read as likely false-triggers against the
  current description) but can't actually measure
