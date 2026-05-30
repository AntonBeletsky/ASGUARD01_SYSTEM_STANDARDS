# AI Task Execution Methodology
## A Systematic Approach to Executing Complex Tasks with LLMs

---

## Philosophy

Any non-trivial task consists of three separate stages that must never be mixed:

```
ANALYSIS → PLAN → EXECUTION
```

Mixing stages is the primary cause of errors. LLMs tend to immediately "do" things rather than first understanding the full scope of the work. This leads to omissions, domino errors, and rework.

---

## Workflow Structure

### Phase 0 — Context Loading

Before any work begins, all context is loaded and explicitly confirmed:

- **Specification / guide** — the rules the result must conform to
- **Materials** — files, code, data to be processed
- **Constraints** — what must not be touched, what is critical, priorities

**Rule:** nothing gets done at this stage. Only reading and confirming that loading is complete.

```
User: load the guide, do nothing
AI: [reads] → "Guide loaded ✓"

User: load the files, these are the working materials
AI: [reads all files] → table of files with line counts and purpose
```

**Why it matters:** if context is loaded incompletely or misunderstood — all subsequent analysis will be wrong.

---

### Phase 1 — Analysis

Systematic examination of all materials **against** the specification.

#### 1.1 Define Violation Categories

First, build a taxonomy — an exhaustive list of problem types. Without it, the analysis will be incomplete.

```
Example for code refactoring:
- CSS_PREFIX — abbreviations in class names
- KEYFRAME_PREFIX — abbreviations in @keyframes
- DATA_CUSTOM — custom attributes without a prefix
- DATA_ACTION_VALUE — incorrect value format
- ID_PREFIX — id without widget prefix
- ID_DEAD — dead ids (present in HTML, unused anywhere)
- ID_JS_HOOK — id used as a JS hook (violates Law Zero)
- JS_VAR — abbreviations in variable names
```

#### 1.2 Analyze Each File Against Each Category

Sequential pass: file × category. No skipping ahead.

**Technique:** ask layered questions during analysis:
1. What is violated in CSS?
2. What is violated in HTML?
3. What is violated in JS?
4. Which ids are live, which are dead?
5. Where are the domino dependencies?

#### 1.3 Domino Analysis

For each violation: what else will break if only this one location is fixed?

```
Violation: CSS token --msg-bubble-radius → --messages-bubble-radius

Domino:
├── CSS lines 165,166: var(--msg-bubble-radius) in child rules
├── JS line 978: getPropertyValue('--msg-bubble-radius')
└── (no HTML — token is not used in attributes)
```

**Rule:** the domino must be exhaustive. An incomplete domino = broken code after the fix.

---

### Phase 2 — Task Map

The analysis is turned into a structured artifact. This is not just a list — it is a machine-readable map with dependencies.

#### Map Structure

```json
{
  "meta": {
    "total_issues": 84,
    "guide_version": "containerization-6"
  },
  "files": [
    {
      "file": "widget.html",
      "issues": [
        {
          "id": "widget-001",
          "category": "CSS_PREFIX",
          "severity": "HIGH",
          "change_type": "RENAME",
          "location": {
            "lines": { "start": 69, "end": 82 },
            "context": "--msg-bubble-radius: 0.75rem;",
            "scope": "CSS:tokens"
          },
          "current": "--msg-bubble-radius",
          "expected": "--messages-bubble-radius",
          "description": "Abbreviation 'msg' instead of 'messages'. §7.1",
          "rule_ref": "§7.1",
          "dependencies": [
            {
              "issue_id": "widget-002",
              "file": "widget.html",
              "description": "CSS line 165: var(--msg-bubble-radius) — token consumer"
            }
          ],
          "status": "pending"
        }
      ]
    }
  ]
}
```

#### Required Fields

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier for domino references |
| `severity` | CRITICAL / HIGH / MEDIUM / LOW — determines execution order |
| `location.lines` | Exact line numbers — without these, finding and verifying is impossible |
| `location.context` | Verbatim code fragment — for identification without opening the file |
| `current` / `expected` | What exists now → what it should be |
| `dependencies` | Domino with references to issue_id, not just plain text |
| `status` | `pending` / `in-progress` / `done` — progress tracking |

#### Severity

```
CRITICAL — code is broken or violates an architectural invariant
           Example: JS looks up DOM via id instead of data-attributes

HIGH     — naming violates the standard, scalability is at risk
           Example: abbreviations in CSS classes, tokens, ids

MEDIUM   — noise, does not affect functionality but pollutes the code
           Example: dead ids that are not used anywhere

LOW      — stylistic deviation
```

#### Change Types

```
RENAME   — rename while preserving function
DELETE   — remove entirely
REPLACE  — substitute one construct for another
ADD      — add something missing
MOVE     — relocate to a different place
```

---

### Phase 3 — Execution Plan

The task map is turned into an interactive tracker with grouping.

#### Plan Structure

```
File A (group)
  ├── CSS prefix (subgroup)
  │   ├── [ ] issue-001 — --msg-* → --messages-* (domino: 3)
  │   └── [ ] issue-002 — .msg-* → .messages-* (domino: 11)
  ├── @keyframes (subgroup)
  │   └── [ ] issue-003 — msg-bubble-in → messages-bubble-in
  └── id prefix (subgroup)
      └── [ ] issue-004 — id="msg-seller-name" → messages-seller-name

File B (group)
  └── ...
```

**Grouping rules:**
- One file = one group
- One violation type = one subgroup
- One specific issue = one item with a status
- Domino is executed together with the parent issue — not separately

#### Execution Priority

```
1. CRITICAL (Law Zero — architectural violations)
2. HIGH (naming — many dominos, high collision risk)
3. MEDIUM (dead code — safe, but needs cleanup)
4. LOW (stylistics)
```

Within a severity level — order by number of dominos (more dependencies = executed sooner).

---

### Phase 4 — Execution

#### Principles

**1. One file at a time**

Do not switch between files mid-way. A file is opened, all its issues are resolved, the file is validated, then move on to the next.

**2. Domino is executed immediately**

If issue-001 has 3 domino dependencies — all 4 changes are made in a single pass. Not "parent first, domino later."

**3. Multiple passes per file**

Complex files are processed in layers:
```
Pass 1: CSS (tokens + classes + keyframes)
Pass 2: HTML attributes
Pass 3: JS strings and expressions
Pass 4: ids (remove dead ones, rename live ones)
```

Why not all at once: regular expressions and string replacements can conflict. Layered processing isolates the risk.

**4. Order of replacements within a pass**

Always from longest to shortest:
```python
# ❌ Wrong
replacements = ['.msg-msg', '.msg-msg--sent', '.msg-msg--recv']
# When replacing .msg-msg → .messages-bubble
# the pattern will no longer match .msg-msg--sent

# ✅ Correct
replacements = [
    ('.msg-msg--sent', '.messages-bubble--sent'),  # more specific — first
    ('.msg-msg--recv', '.messages-bubble--received'),
    ('.msg-msg', '.messages-bubble'),               # general — last
]
```

**5. Validate after each file**

Do not defer to the end. An error in file A must not affect confidence in file B.

---

### Phase 5 — Validation

#### Validation Levels

**1. Automated — pattern search**

```python
# Search for remaining abbreviations
import re
remaining = [line for line in src.split('\n') 
             if re.search(r'\bmsg-', line) 
             and not line.strip().startswith(('#', '//', '<!--', '*'))]
```

Exclude comments — they do not affect code behavior but pollute results.

**2. Semantic — checking for legitimate exceptions**

Not all pattern matches are violations. For each "remaining" occurrence, understand the context:

```
document.querySelector('.widget-container')  ← LEGAL (bootstrap by container class)
document.querySelector('#some-id')           ← VIOLATION (Law Zero)

id="aria-title-for-modal"                    ← LEGAL (ARIA reference)
id="my-btn"  + JS: document.getElementById  ← VIOLATION (JS hook)
```

**3. Final Report**

```
FILE                    STATUS    CRITICAL  HIGH  MEDIUM
messages.html           ✅ CLEAN     0        0      0
my-reviews.html         ✅ CLEAN     0        0      0
mywallet.html           ✅ CLEAN     0        0      0  (Law Zero: 2 legal)
...
```

---

## Requirements Specification for Creating a Task Map

When specifying the task of creating a violation map, the following must be defined:

### Required Spec Elements

```markdown
1. Files in scope — list of all files to be analyzed

2. Specification — the document/guide to analyze against

3. Violation categories — exhaustive list with codes
   (without this, the analysis will be incomplete)

4. Severity scale — what counts as CRITICAL, HIGH, MEDIUM, LOW

5. Change types — RENAME, DELETE, REPLACE, ADD, MOVE

6. JSON schema — exact structure of the output artifact with field types

7. Rules for issue ids — issue_id format, numbering rules

8. Rules for dependencies — how to reference, what must be included

9. Requirements for the context field — maximum length, what to include

10. What is NOT in the map — clear scope boundaries
```

### Spec Improvements Over a Naive Approach

| Naive Spec Problem | Solution |
|--------------------|----------|
| No JSON schema | Specify each field's type, provide an example |
| No unique IDs | Format: `{widget}-{N:03d}`, numbered by severity |
| No current/expected separation | Two fields, not a single "description" |
| Domino is just text | Domino contains `issue_id` — a verifiable reference |
| No map validation | All `issue_id` in dependencies must exist in the map |
| No context field | Exact code fragment ≤120 characters |
| No severity | Cannot determine execution order |
| No change_type | RENAME and DELETE are different operations |

---

## Templates for Common Task Types

### Refactoring Against a Guide

```
Phase 0: load guide + all files
Phase 1: analyze file × violation category
Phase 2: JSON map with dominos
Phase 3: interactive plan (group=file, subgroup=violation type)
Phase 4: execution CRITICAL → HIGH → MEDIUM, file by file
Phase 5: automated pattern validation + manual exception review
```

### Codebase Audit

```
Phase 0: load quality standard + files
Phase 1: analyze by dimension (security, performance, accessibility, naming)
Phase 2: map with severity and effort estimates
Phase 3: plan grouped by dimension, not by file
Phase 4: quick wins first (HIGH severity + LOW effort)
Phase 5: regression tests
```

### API Migration

```
Phase 0: documentation for old and new API + file list
Phase 1: find all usages of deprecated methods
Phase 2: replacement map with breaking changes marked as CRITICAL
Phase 3: plan by files, breaking changes isolated into a separate batch
Phase 4: execution, tests after each file
Phase 5: grep for old patterns + smoke test
```

### Large-Scale Rename (brand/namespace)

```
Phase 0: list of old names + new names + files
Phase 1: find ALL occurrences including comments, documentation, tests
Phase 2: map split by file type and context
Phase 3: plan: types/interfaces first, then implementation, then tests, then documentation
Phase 4: replacements from longest to shortest, validate after each file
Phase 5: final grep, build, tests
```

---

## AI Checklist Upon Receiving a Task

```
□ Have I loaded and read the ENTIRE specification (not just the beginning)?
□ Have I loaded ALL files mentioned in the task?
□ Have I compiled an exhaustive taxonomy of violation types?
□ For each violation, have I found ALL domino dependencies?
□ Does the map contain exact line numbers (not "around" or "in method X")?
□ Do all issue_ids in dependencies actually exist in the map?
□ Is the execution order determined by severity?
□ Does each file have a plan of sequential passes?
□ Is validation planned after each file, not just at the end?
□ Do I know what constitutes a LEGAL exception for each pattern?
```

---

## Anti-Patterns

### ❌ Analyzing and Fixing Simultaneously

```
Bad:  "Found a violation — fixed it immediately — found the next one..."
Good: Full analysis → full map → execute the map
```

Reason: when analyzing and fixing simultaneously, the overall picture is lost. It is unknown how many more violations remain ahead, making it impossible to prioritize correctly.

### ❌ Descriptive Dominos Instead of Reference-Based

```
Bad:  "dependencies": [{"description": "update JS"}]
Good: "dependencies": [{"issue_id": "messages-012", "description": "..."}]
```

Reason: a descriptive domino cannot be verified. A reference-based domino can be validated automatically.

### ❌ Replacements in the Wrong Order

```
Bad:  .msg-msg → then .msg-msg--sent (will no longer be found)
Good: .msg-msg--sent first, then .msg-msg
```

### ❌ Validation Only at the End

```
Bad:  process 8 files → verify everything at once
Good: file → validate → next file
```

Reason: an error in file 2 may not surface until file 7. Isolated validation localizes the problem.

### ❌ Ignoring Comments During Validation

```
Bad:  grep finds 3 occurrences — panic
Good: verify that all 3 are in comments — ok
```

### ❌ Map Without Line Numbers

```
Bad:  "location": {"scope": "JS:_bubble"}
Good: "location": {"lines": {"start": 712, "end": 725}, "context": "bbl.className = ['msg-msg..."}
```

Reason: without line numbers, the location cannot be found automatically, nor can it be verified after the fix.

---

## Working with Large Files

When working with files > 500 lines:

**Read the entire file before starting.** Do not start from the first line and work downward — first get the full picture.

**Work in pattern batches**, not one at a time:
```python
# All tokens in one dictionary
token_map = {
    '--msg-bubble-radius': '--messages-bubble-radius',
    '--msg-bubble-sent-bg': '--messages-bubble-sent-bg',
    # ...14 tokens at once
}
for old, new in token_map.items():
    src = src.replace(old, new)
```

**Split into logical passes** (CSS → HTML → JS), not arbitrary chunks.

**Confirm the result of each pass** before proceeding to the next:
```
After pass 1 (CSS): grep shows 0 remaining tokens
After pass 2 (HTML): grep shows 0 remaining classes in attributes
...
```

---

## Execution Quality Metrics

### After Completing the Work, Ask Yourself:

```
1. Does the number of issues in the map equal the number of closed issues?
2. Does grep for all violation patterns return 0 (excluding comments)?
3. Do all ids in HTML have the correct widget prefix?
4. Are all data-action values in kebab-case verb-noun format?
5. Are there no document.querySelector('#...') or getElementById calls used for logic?
6. Do all addEventListener calls have a signal (AbortController) or { once: true }?
7. Has the code semantics not changed — only naming?
```

### Numerical Indicators

Record before and after:
- Number of files
- Total line count
- Number of issues by severity
- Number of files with zero violations

This allows for an objective assessment of the scope and completeness of the work.

---

*This methodology was developed based on the refactoring of 9 widgets (9,007 lines, 84 violations) against the containerization-6 standard.*
