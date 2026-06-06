# Methodology: JSON Architecture to English Markdown Guide

## Principles

The JSON file is the source of truth for structure only. It defines the guide title, volumes, chapters, sections, IDs, and ordering. It does not contain finished educational content.

The Markdown guide must be produced through small, resumable units. Each section is written as an independent Markdown fragment, reviewed on its own, then merged into the final document by script.

All working files, generated fragments, manifests, and final outputs must stay inside `_codex`.

## Scope

Input:

```text
../Ultimate_Software_Engineering_Knowledge_Architecture_FINAL.json
```

Ignored:

```text
../.old
```

Generated workspace:

```text
_codex/
  manifest.json
  parts/
  output/
```

## Decomposition Model

Use the JSON hierarchy as the task hierarchy:

```text
Guide > Volume > Chapter > Section
```

Task granularity:

```text
one JSON section = one Markdown fragment = one resumable writing task
```

This keeps work small enough for controlled drafting, review, validation, and retry.

## Fragment Naming

Each section fragment should be stored under its volume folder:

```text
_codex/parts/volume-01-clean-code/1.1.1-naming-variables-and-constants.md
```

Naming rules:

- preserve the section ID at the start of the filename;
- use a lowercase slug generated from the section title;
- keep volume folders zero-padded for stable ordering;
- never rename files manually after `manifest.json` is created.

## Progress Model

Progress is stored in:

```text
_codex/manifest.json
```

Recommended status lifecycle:

```text
pending -> drafting -> draft -> reviewed -> validated -> merged
```

Status meanings:

- `pending`: fragment exists or is planned, but content is not written.
- `drafting`: work is actively in progress.
- `draft`: initial content is complete, but not reviewed.
- `reviewed`: content passed human or AI review.
- `validated`: content passed script checks.
- `merged`: content was included in the final output.

The manifest should also track:

- source JSON path;
- guide title;
- volume, chapter, and section metadata;
- fragment path;
- content hash;
- validation errors;
- timestamps.

## Content Quality Standard

Each section must be practical, precise, and useful for a senior software engineer.

Every completed fragment should include:

- purpose and scope;
- core concepts;
- practical guidance;
- trade-offs;
- examples;
- common mistakes;
- review checklist.

Avoid:

- generic filler;
- repeated boilerplate;
- shallow definitions only;
- motivational text;
- unsupported claims;
- references to nonexistent sections;
- changing JSON-provided IDs or titles.

## Validation Rules

A fragment is valid only when:

- the front matter contains the expected section ID, volume, chapter, section title, and status;
- the first content heading matches the section ID and title;
- required content blocks are present;
- there are no `TODO`, `TBD`, or `[MISSING CONTENT]` placeholders;
- the body has enough substance for the section;
- Markdown heading levels are consistent;
- the file path matches the manifest entry.

## Merge Rules

The merge script must assemble content in JSON order, not filesystem order.

Final structure:

```markdown
# Ultimate Software Engineering Knowledge Architecture

## Volume 1: Clean Code

### 1.1 Naming Conventions

#### 1.1.1 Naming Variables and Constants
...
```

Default merge should be strict:

- merge only `validated` fragments;
- fail if any required fragment is missing or invalid;
- write output only to `_codex/output/`.

Preview merge may allow incomplete content only when explicitly requested. Missing sections must be marked visibly.

## Recommended Batch Size

Use batches that are small enough to review carefully:

- 1 volume for small volumes;
- 1 chapter for dense technical areas;
- 5 to 10 sections for deep content generation;
- 1 section at a time for complex or high-risk topics.

After each batch:

```text
validate -> review -> mark reviewed -> validate -> merge preview
```

## Completion Definition

The work is complete only when:

- all 481 section fragments exist;
- every fragment is reviewed and validated;
- final merge succeeds without incomplete placeholders;
- final Markdown is written under `_codex/output/`;
- `manifest.json` reflects the final merged state.

