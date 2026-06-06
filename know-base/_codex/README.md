# JSON to Markdown Guide Workspace

This folder is the isolated Codex workspace for converting the root JSON guide architecture into a high-quality English Markdown guide.

Source JSON:

```text
../Ultimate_Software_Engineering_Knowledge_Architecture_FINAL.json
```

The `.old` folder must not be inspected or used.

## Goal

Create one final Markdown guide from the JSON structure without losing progress during a long writing process.

The work is split into small, resumable tasks:

- one section in the JSON becomes one Markdown fragment;
- fragment progress is tracked in `manifest.json`;
- the final guide is assembled by `build_guide_md.py`;
- all generated working files stay inside this `_codex` folder.

## Planned Workflow

```powershell
cd C:\GitHub\ASGUARD01_SYSTEM_STANDARDS\know-base
python .\_codex\build_guide_md.py inspect
python .\_codex\build_guide_md.py init
python .\_codex\build_guide_md.py next
python .\_codex\build_guide_md.py mark 1.1.1 drafting
python .\_codex\build_guide_md.py validate
python .\_codex\build_guide_md.py merge
python .\_codex\build_guide_md.py progress
```

Do not run `init` until you are ready to create the section fragment files.

## Files

- `METHODOLOGY.md` - full methodology for decomposition, progress, quality, and merge rules.
- `CONTENT_INSTRUCTIONS.md` - English writing instructions for every section.
- `TASK_PLAN.md` - implementation and execution plan.
- `SECTION_TEMPLATE.md` - canonical Markdown fragment template.
- `task.log` - progress log for the current work.
- `build_guide_md.py` - Python utility for inspecting JSON, creating fragments, tracking progress, validating, and merging.
- `draft_sections.py` - offline drafting utility that fills section fragments from manifest metadata.

## Progress Output

Show current completion state:

```powershell
python .\_codex\build_guide_md.py progress
```

Run the drafting utility with visible progress:

```powershell
python .\_codex\draft_sections.py --progress --progress-every 25
```

## Current Output

The generated superguide is available at:

```text
_codex/output/Ultimate_Software_Engineering_Knowledge_Architecture_FINAL.md
```
