# Version Control Naming System

## Overview

This document describes the file versioning convention used across this project.

## Naming Format

```
<prefix>-<number><letter>.md
```

- **prefix** — any descriptive name (e.g. `version-control`, `report`, `notes`)
- **number** — integer starting from `1`, increments after all letters are exhausted
- **letter** — single character from `a` to `h`, resets to `a` after each number increment

## Sequence

The version suffix follows this order:

```
1a → 1b → 1c → 1d → 1e → 1f → 1g → 1h →
2a → 2b → 2c → 2d → 2e → 2f → 2g → 2h →
3a → ...
```

Each number has exactly **8 slots** (a through h).

## Rules

1. Every time a file is updated and re-issued, it receives the **next version suffix**.
2. The version suffix lives **only in the filename** — never inside the file content.
3. The letter cycles `a → b → c → d → e → f → g → h`, then the number increments and the letter resets to `a`.
4. There is no version `0` — counting starts at `1a`.

## Examples

| Filename | Meaning |
|---|---|
| `report-1a.md` | First ever issue |
| `report-1h.md` | Eighth revision in the first number group |
| `report-2a.md` | Ninth revision overall, number group resets |
| `notes-3d.md` | 20th revision of the `notes` file |

## Why No Version Inside the File?

Embedding a version string inside the file body causes unnecessary diffs on every release and makes automated diffing noisier. The filename alone carries all version information.
