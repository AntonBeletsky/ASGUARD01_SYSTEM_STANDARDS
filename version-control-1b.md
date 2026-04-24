# Version Control Naming System

## Overview

This document describes the file versioning convention used across this project.

## Naming Format

```
<prefix><number><letter>.<ext>
```

- **prefix** — any arbitrary sequence of characters: letters (upper or lowercase), digits, dashes, underscores, dots, or any combination thereof
- **number** — integer starting from `1`, increments after all letters are exhausted
- **letter** — single character from `a` to `h`, resets to `a` after each number increment
- **ext** — any file extension (`.html`, `.md`, `.txt`, etc.)

The version token is the first occurrence of the pattern `<number><letter a–h>` inside the filename.

## Sequence

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
4. Counting starts at `1a` — there is no version `0`.
5. The prefix may contain any characters, including digits and dashes — the version token is always the `<number><letter>` pattern.

## Real-World Examples

| Filename | Prefix | Version |
|---|---|---|
| `compare-page-ng-1a.html` | `compare-page-ng-` | `1a` |
| `Asguard01MediaGallery-NG-20g_-_themes.html` | `Asguard01MediaGallery-NG-` | `20g` |
| `payment-complete-page-1d.html` | `payment-complete-page-` | `1d` |
| `report-3h.md` | `report-` | `3h` |

## Why No Version Inside the File?

Embedding a version string inside the file body causes unnecessary diffs on every release and makes automated diffing noisier. The filename alone carries all version information.
