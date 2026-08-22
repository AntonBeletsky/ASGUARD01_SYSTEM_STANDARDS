# EntityMap JSON Language — project

A specification, a real model written in it, and the tooling used to inspect that model — five files, meant to sit together in one folder.

| # | File | Format | Purpose |
|---|---|---|---|
| 1 | `EntityMapJSONLanguage.md` | Markdown | The language specification (v1.0) |
| 2 | `university_course_map.json` | JSON | Example model in that language — a university course domain: departments, teachers, students, courses, lessons, attendance, assignments, grades |
| 3 | `university_erd.html` | HTML | Interactive ER diagram of file 2 — zoom, fullscreen, dark/light theme, an accessible text-table alternative |
| 4 | `EMJLDesign.html` | HTML | Analysis: cross-checks files 1 and 2 against each other and against file 3, with 4 concrete findings |
| 5 | `readme.md` | Markdown | This file |

## Reading order

1 → 2 → 3 → 4

## Requirements

All 5 files must stay in the same folder — `EMJLDesign.html` links to the other four with plain relative paths (`<a href="university_erd.html">` etc.), and those links only resolve if the files are co-located. Files 3 and 4 also load Bootstrap and (file 3 only) Mermaid from `cdn.jsdelivr.net` at runtime, so an internet connection is needed to see them fully styled/rendered — opening them offline still shows the content, just unstyled.

## What was found

Four findings came out of cross-checking files 1 and 2 (full detail in `EMJLDesign.html`):

1. `university_course_map.json` isn't strict JSON — 29 lines of `//` comments make it fail a standard parser until they're stripped.
2. One relation's comment says a teacher can exist without a department; the field it describes (`nullable: false`) says otherwise.
3. The diagram in `university_erd.html` draws "head of department" as mandatory; the JSON declares it optional (`nullable: true`, `one_to_zero_one`) — a direct contradiction, not just a simplification.
4. The `DayOfWeek` enum is defined but never referenced anywhere in the model, and is missing Sunday.
