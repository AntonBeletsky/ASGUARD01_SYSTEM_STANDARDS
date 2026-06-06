# Execution Plan

This plan describes how to create the Markdown guide later. It is intentionally not executed yet.

## Phase 1: Prepare Workspace

1. Keep all generated work inside `_codex`.
2. Confirm the source JSON exists in the repository root.
3. Run `inspect` to confirm guide statistics and hierarchy.
4. Run `init` only when ready to create fragment files.

Expected result:

```text
_codex/manifest.json
_codex/parts/
```

## Phase 2: Generate Empty Fragments

1. Use the Python script to create one Markdown fragment per section.
2. Preserve JSON ordering in the manifest.
3. Use stable filenames based on section IDs and titles.
4. Do not manually create files outside `_codex`.

Expected result:

```text
481 section fragment files
```

## Phase 3: Fill Content in Batches

1. Use `next` to choose the next pending section.
2. Mark the section as `drafting`.
3. Fill the Markdown fragment using `CONTENT_INSTRUCTIONS.md`.
4. Mark it as `draft`.
5. Repeat for a small batch.

Recommended batch sizes:

- 5 sections for deep technical content;
- 1 chapter for straightforward content;
- 1 volume only after the process is proven stable.

## Phase 4: Review and Validate

1. Review each draft against the quality checklist.
2. Mark acceptable fragments as `reviewed`.
3. Run `validate`.
4. Fix reported issues.
5. Promote passing fragments to `validated`.

Expected result:

```text
No placeholders, wrong headings, missing blocks, or thin content.
```

## Phase 5: Merge

1. Run a preview merge if incomplete sections remain.
2. Run strict merge only after all fragments are validated.
3. Write the final guide to `_codex/output/`.
4. Keep merge order controlled by JSON, not by filesystem sorting.

Expected result:

```text
_codex/output/Ultimate_Software_Engineering_Knowledge_Architecture_FINAL.md
```

## Phase 6: Final Review

1. Check the final table of contents.
2. Check volume and chapter transitions.
3. Search for repeated boilerplate.
4. Search for placeholders.
5. Confirm the final file is complete and readable as one guide.

