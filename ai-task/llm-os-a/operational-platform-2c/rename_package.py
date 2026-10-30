#!/usr/bin/env python3
"""rename_package.py -- give the delivered package one name, in its file names and in its text.
Written for this guide; not part of the original archive.

The package as delivered used several names for one thing: the tool `llm-assembler` (the skill, its folder, the state
directory `.llm-assembler/`), the project "LLM Operational Platform", and file names that carry them. This program turns the
delivered archive into a copy in which all of them are the single name **Operational Platform**; the delivered archive is
only read.

Usage
  python3 -I rename_package.py build ORIGINAL.zip DIST_DIR EXTRACT_ROOT REPORT.md
        writes DIST_DIR/operational-platform-a-2a.zip (which holds operational-platform.skill), unpacks the archive into
        EXTRACT_ROOT/operational-platform-extracted/ (five files, the .skill among them) and the .skill into
        EXTRACT_ROOT/operational-platform-skill-extracted/ (neither folder may exist), and writes REPORT.md: what was
        renamed, the proof that the code did not change, and the lines of a program that differ (all of them strings).
  python3 -I rename_package.py map FILE_IN FILE_OUT
        applies the same rules to one file (the guide's own scripts and transcripts are renamed with this).
  python3 -I rename_package.py carry-over ORIGINAL.zip RENAMED_CLI WORKDIR REPORT.md
        what happens to a project that already holds the state of the delivered tool (WORKDIR must not exist). The delivered
        tool is unpacked from ORIGINAL.zip into WORKDIR and run on a small project; the renamed tool, RENAMED_CLI (its cli.py),
        is run on copies of that project, before and after the state directory is renamed, and imports a batch that the
        delivered tool exported. Writes REPORT.md.

The rules
  * File names:  llm-assembler -> operational-platform;  llm-operational-platform-task-execution-methodology ->
                 operational-platform-task-execution-methodology;  llm-os -> operational-platform.
  * Text:  `.llm-assembler` (the state directory) -> `.operational-platform`;  `llm-assembler` -> `operational-platform` in
           code, in code spans and in link targets, and -> "Operational Platform" in running text;  "LLM Operational
           Platform" -> "Operational Platform".  A few paragraphs that explained the difference between the old names are
           replaced as a whole (PATCHES): after the rename there is nothing left to distinguish.
  * Words such as "assembly" and "assembled" are not names and are not touched.

The proof that the code did not change: each Python module of the original and of the copy is parsed, every string constant
(docstrings included) is blanked, and the two syntax trees must be equal; the strings that differ are listed.
"""
import ast
import difflib
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

NEW_ZIP = "operational-platform-a-2a.zip"
OLD_RESIDUE = re.compile(r"(?i)llm[-_ ]?assembler|llm[-_ ]os\b|llm[ -]operational")

# ---- file names ---------------------------------------------------------------------------------------------------
NAME_RULES = [
    ("llm-operational-platform-task-execution-methodology", "operational-platform-task-execution-methodology"),
    ("llm-assembler", "operational-platform"),
    ("llm-os", "operational-platform"),
]


def rename_name(name):
    for old, new in NAME_RULES:
        name = name.replace(old, new)
    return name


# ---- paragraphs that are replaced as a whole -----------------------------------------------------------------------
INTRO_OLD = """**LLM Operational Platform** — or simply **Operational Platform** — is
the name of this project: a six-phase task-execution methodology and a
tested implementation of it (`llm-assembler`, a skill for line-precise
batch editing of text and code)."""
INTRO_NEW = """**Operational Platform** is the name of this project: a six-phase
task-execution methodology and a tested implementation of it
(`operational-platform`, a skill for line-precise batch editing of text
and code)."""

NAME_NOTE_OLD = """`llm-assembler` is a specific tool's name, not the project's — it keeps
its own identity (the skill's `name:` field, its filenames) unchanged, the
same way a specific application keeps its own name on a platform. **LLM
Operational Platform** is the project both files above answer to: the
merged document in Set A opens with it, the standalone methodology
document in Set B opens with it, and `llm-assembler.md`'s own opening
line points back to both as the methodology it implements."""
NAME_NOTE_NEW = """**Operational Platform** is the one name of everything in this delivery:
the project, the methodology and the tool. The merged document in Set A
opens with it, the standalone methodology document in Set B opens with
it, and `operational-platform.md`'s own opening line points back to both
as the methodology it implements. In file names and in the skill's
`name:` field the name is written `operational-platform`, and the tool
keeps its state in a `.operational-platform/` directory."""

SKILL_HEAD_OLD = """# llm-assembler

*Part of the **LLM Operational Platform** (Operational Platform for
short) -- the tool that implements its task-execution methodology.
`references/methodology-mapping.md` maps the methodology's phases onto
the commands below; the full methodology on its own, with no mention of
this tool, lives in `llm-operational-platform-task-execution-methodology.md`.*"""
SKILL_HEAD_NEW = """# Operational Platform

*The tool of the **Operational Platform** project -- it implements the
project's task-execution methodology. `references/methodology-mapping.md`
maps the methodology's phases onto the commands below; the full
methodology on its own, with no mention of this tool, lives in
`operational-platform-task-execution-methodology.md`.*"""

FULL_INTRO_OLD = """**LLM Operational Platform** — or simply **Operational Platform** — is
the name of this project: a six-phase task-execution methodology and,
inline, phase by phase, exactly which command, field, and file of a real
working implementation (`llm-assembler`, a skill for line-precise batch
editing of text and code) satisfies each requirement. Reading only this
document is enough to use the system."""
FULL_INTRO_NEW = """**Operational Platform** is the name of this project: a six-phase
task-execution methodology and, inline, phase by phase, exactly which
command, field, and file of a real working implementation
(`operational-platform`, a skill for line-precise batch editing of text
and code) satisfies each requirement. Reading only this document is
enough to use the system."""

ABSTRACT_INTRO_OLD = """**LLM Operational Platform** — or simply **Operational Platform** — is
the name of the project this document belongs to: a six-phase
task-execution methodology, and, separately, a tested implementation of
it (`llm-assembler`, a skill for line-precise batch editing of text and
code). This document covers the methodology alone."""
ABSTRACT_INTRO_NEW = """**Operational Platform** is the name of the project this document
belongs to: a six-phase task-execution methodology, and, separately, a
tested implementation of it (`operational-platform`, a skill for
line-precise batch editing of text and code). This document covers the
methodology alone."""

FRONT_OLD, FRONT_NEW = "name: llm-assembler\n", "name: operational-platform\n"

# member name (as delivered) -> list of (old, new); a patch that does not match is an error
PATCHES = {
    "README.md": [(INTRO_OLD, INTRO_NEW), (NAME_NOTE_OLD, NAME_NOTE_NEW)],
    "llm-assembler.md": [(FRONT_OLD, FRONT_NEW), (SKILL_HEAD_OLD, SKILL_HEAD_NEW)],
    "llm-assembler/SKILL.md": [(FRONT_OLD, FRONT_NEW), (SKILL_HEAD_OLD, SKILL_HEAD_NEW)],
    "llm-operational-platform-task-execution-methodology-full-in-one-file-md.md": [(FULL_INTRO_OLD, FULL_INTRO_NEW)],
    "llm-operational-platform-task-execution-methodology.md": [(ABSTRACT_INTRO_OLD, ABSTRACT_INTRO_NEW)],
    "llm-assembler/scripts/storage.py": [("for llm-assembler lives here", "for Operational Platform lives here")],
}

# ---- text -----------------------------------------------------------------------------------------------------------
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
SPAN = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
LINK_TARGET = re.compile(r"\]\([^)\s]*\)")
GENERIC = [
    ("llm-operational-platform-task-execution-methodology", "operational-platform-task-execution-methodology"),
    ("llm-assembler-skill-extracted", "operational-platform-skill-extracted"),
    ("llm-os-extracted", "operational-platform-extracted"),
    ("llm-os-a-2a", "operational-platform-a-2a"),
    ("how-work-llm-assembler", "how-work-operational-platform"),
    (".llm-assembler", ".operational-platform"),
]


def identifier_form(text, counts):
    for old, new in GENERIC + [("llm-assembler", "operational-platform"), ("LLM Operational Platform", "Operational Platform")]:
        n = text.count(old)
        if n:
            counts[old] = counts.get(old, 0) + n
            text = text.replace(old, new)
    return text


def prose_form(text, counts):
    for old, new in GENERIC + [("LLM Operational Platform", "Operational Platform"), ("llm-assembler", "Operational Platform")]:
        n = text.count(old)
        if n:
            counts[old] = counts.get(old, 0) + n
            text = text.replace(old, new)
    return text


def rename_markdown(text, counts):
    out, fence = [], None                                   # fence = (character, length) while inside a fenced block
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence is None and m:
            fence = (m.group(1)[0], len(m.group(1)))
            out.append(identifier_form(line, counts))
        elif fence is not None:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and line.strip() == m.group(1):
                fence = None
            out.append(identifier_form(line, counts))
        else:
            pieces, pos = [], 0
            protected = [m.span() for m in SPAN.finditer(line)] + [m.span() for m in LINK_TARGET.finditer(line)]
            for a, b in sorted(protected):
                if a < pos:
                    continue
                pieces.append(prose_form(line[pos:a], counts))
                pieces.append(identifier_form(line[a:b], counts))
                pos = b
            pieces.append(prose_form(line[pos:], counts))
            out.append("".join(pieces))
    return "\n".join(out)


def rename_text(name, text, counts=None):
    """name is the member's name as delivered (it selects the patches); returns the text of the renamed member."""
    counts = {} if counts is None else counts
    for old, new in PATCHES.get(name, []):
        if text.count(old) != 1:
            raise SystemExit(f"{name}: a patch does not match exactly once: {old[:60]!r}")
        text = text.replace(old, new)
        counts["(a paragraph)"] = counts.get("(a paragraph)", 0) + 1
    if name.endswith(".md"):
        return rename_markdown(text, counts)
    return identifier_form(text, counts)


# ---- the proof that no program changed ------------------------------------------------------------------------------
class Blank(ast.NodeTransformer):
    def visit_Constant(self, node):
        return ast.copy_location(ast.Constant(value=""), node) if isinstance(node.value, str) else node


def strings(tree):
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def same_tree(old_src, new_src):
    a, b = ast.parse(old_src), ast.parse(new_src)
    same = ast.dump(Blank().visit(ast.parse(old_src))) == ast.dump(Blank().visit(ast.parse(new_src)))
    differing = [(x, y) for x, y in zip(strings(a), strings(b)) if x != y] if same else []
    return same, differing


# ---- build ----------------------------------------------------------------------------------------------------------
def build(original, dist, extract_root, report):
    outer = zipfile.ZipFile(original)
    rows, counts_by_member, modules = [], {}, []
    new_outer = io.BytesIO()
    members_new = {}                                        # new path under extract_root -> bytes
    with zipfile.ZipFile(new_outer, "w", zipfile.ZIP_DEFLATED) as zo:
        for info in outer.infolist():
            data = outer.read(info)
            if info.filename.endswith(".skill"):
                start = len(rows)
                inner, inner_out = zipfile.ZipFile(io.BytesIO(data)), io.BytesIO()
                with zipfile.ZipFile(inner_out, "w", zipfile.ZIP_DEFLATED) as zi:
                    for member in inner.infolist():
                        old = inner.read(member)
                        c = {}
                        new = rename_text(member.filename, old.decode("utf-8"), c).encode("utf-8")
                        newname = rename_name(member.filename)
                        zinfo = zipfile.ZipInfo(newname, member.date_time)
                        zinfo.compress_type, zinfo.external_attr, zinfo.create_system = zipfile.ZIP_DEFLATED, member.external_attr, member.create_system
                        zi.writestr(zinfo, new)
                        members_new["operational-platform-skill-extracted/" + newname] = new
                        rows.append((info.filename + " : " + member.filename, rename_name(info.filename) + " : " + newname,
                                     len(old), len(new), sum(c.values())))
                        if member.filename.endswith(".py"):
                            modules.append((member.filename, old.decode("utf-8"), new.decode("utf-8")))
                new = inner_out.getvalue()
                members_new["operational-platform-extracted/" + rename_name(info.filename)] = new
                rows.insert(start, (info.filename, rename_name(info.filename), len(data), len(new), None))
            else:
                c = {}
                new = rename_text(info.filename, data.decode("utf-8"), c).encode("utf-8")
                members_new["operational-platform-extracted/" + rename_name(info.filename)] = new
                rows.append((info.filename, rename_name(info.filename), len(data), len(new), sum(c.values())))
            zinfo = zipfile.ZipInfo(rename_name(info.filename), info.date_time)
            zinfo.compress_type, zinfo.external_attr, zinfo.create_system = zipfile.ZIP_DEFLATED, info.external_attr, info.create_system
            zo.writestr(zinfo, new)
    Path(dist).mkdir(parents=True, exist_ok=True)
    out_zip = Path(dist) / NEW_ZIP
    out_zip.write_bytes(new_outer.getvalue())
    for rel, content in members_new.items():                # the unpacked copies, which the scenarios run
        target = Path(extract_root) / rel
        if target.exists():
            raise SystemExit(f"{target} exists")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    # the .skill is also written beside the archive, the way it is delivered inside it
    Path(dist, "operational-platform.skill").write_bytes(zipfile.ZipFile(out_zip).read("operational-platform.skill"))

    residue = [r[1] for r in rows if OLD_RESIDUE.search(r[1])]
    for rel, content in members_new.items():
        if rel.endswith(".skill"):                          # a zip: its members were scanned one by one
            continue
        if OLD_RESIDUE.search(content.decode("utf-8")):
            residue.append(rel)
    L = [f"The delivered archive ({Path(original).stat().st_size:,} bytes, SHA-256 `{hashlib.sha256(Path(original).read_bytes()).hexdigest()}`) "
         f"holds {len([r for r in rows if ' : ' not in r[0]])} files, one of which (the package) holds {len([r for r in rows if ' : ' in r[0]])} more. "
         f"The renamed archive `{NEW_ZIP}` is {out_zip.stat().st_size:,} bytes, SHA-256 `{hashlib.sha256(out_zip.read_bytes()).hexdigest()}`.", "",
         "| Delivered as | Renamed to | Bytes before | Bytes after | Names replaced in the text |", "|---|---|---:|---:|---:|"]
    for old, new, a, b, n in rows:
        L.append(f"| `{old}` | `{new}` | {a:,} | {b:,} | {'—' if n is None else n} |")
    L += ["", f"**The code did not change; strings did.** {len(modules)} Python modules were parsed before and after; the syntax tree of each, with every "
          "string constant (docstrings included) blanked, is the same:", "", "| Module | Syntax trees equal | Strings that differ | Lines that differ |", "|---|:--:|---:|---:|"]
    all_same, diffs = True, []
    for name, old, new in modules:
        same, differing = same_tree(old, new)
        all_same &= same
        d = list(difflib.unified_diff(old.splitlines(), new.splitlines(), fromfile=name, tofile=rename_name(name), lineterm="", n=0))
        nlines = sum(1 for x in d if x[:1] in "+-" and x[:3] not in ("+++", "---")) // 2
        L.append(f"| `{rename_name(name)}` | {'yes' if same else '**NO**'} | {len(differing)} | {nlines} |")
        if nlines:
            diffs.append((rename_name(name), d))
    for name, d in diffs:                                   # the lines themselves: `-` as delivered, `+` renamed
        L += ["", f"The lines of `{name}` that differ (`-` as delivered, `+` renamed):", "", "```diff", *d, "```"]
    L += ["", "**Residue.** " + ("None of the old names is left in a file name or in a text of the renamed archive." if not residue
                                else "Old names are left in: " + ", ".join(residue))]
    Path(report).write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{len(rows)} members renamed; trees equal: {all_same}; residue: {residue or 'none'}; {out_zip}")
    sys.exit(0 if all_same and not residue else 1)


# ---- a project that already holds the state of the delivered tool ---------------------------------------------------------
def carry_over(original, renamed_cli, workdir, report):
    """The renamed tool looks for `.operational-platform/`, the delivered one for `.llm-assembler/`. Is the old directory
    recognized, is renaming it enough, and does a batch that the delivered tool exported still import?"""
    work = Path(workdir)
    if work.exists():
        raise SystemExit(f"{work} exists")
    work.mkdir(parents=True)
    outer = zipfile.ZipFile(original)
    skill = zipfile.ZipFile(io.BytesIO(outer.read(next(n for n in outer.namelist() if n.endswith(".skill")))))
    skill.extractall(work / "delivered-tool")               # a folder of its own; nothing in it is imported, the tool is only run (with -I, through its cli.py)
    old_cli = next((work / "delivered-tool").glob("*/scripts/cli.py"))

    def call(cli, cwd, *args):                              # (exit code, reply), with the paths of the tool, the project and the work folder masked
        r = subprocess.run([sys.executable, "-I", str(cli), *args], cwd=cwd, capture_output=True, text=True)
        return r.returncode, (r.stdout + r.stderr).replace(str(cli), "<cli.py>").replace(str(cwd), "<project>").replace(str(work), "<work>")

    def must(cli, cwd, *args):
        rc, out = call(cli, cwd, *args)
        if rc:
            raise SystemExit(f"{args[0]} failed: {out}")
        return out

    proj = work / "project"
    proj.mkdir()
    (proj / "list.txt").write_text("".join(f"item {i}\n" for i in range(1, 7)), encoding="utf-8")
    fid = json.loads(must(old_cli, proj, "register", "list.txt"))["file_id"]
    receiving_a, receiving_b = work / "receiving_delivered", work / "receiving_renamed"
    for d in (receiving_a, receiving_b):                    # two copies that hold the registered file and no batch yet
        shutil.copytree(proj, d)
    (receiving_b / ".llm-assembler").rename(receiving_b / ".operational-platform")

    must(old_cli, proj, "new-batch")
    must(old_cli, proj, "add-descriptor", "batch_0001", "--op", "replace_range", "--file", "list.txt",
         "--start", f"{fid}_l00002", "--end", f"{fid}_l00002", "--payload-text", "item 2, edited")
    must(old_cli, proj, "validate-plan", "batch_0001")
    exported = work / "batch_0001.tar.gz"
    must(old_cli, proj, "export-batch", "batch_0001", "--out", str(exported))
    must(old_cli, proj, "apply-all", "batch_0001")
    state = [p for p in (proj / ".llm-assembler").rglob("*") if p.is_file()]
    named = [p for p in state if OLD_RESIDUE.search(p.read_text(encoding="utf-8", errors="replace"))]

    delivered, moved, unmoved = (work / n for n in ("project_delivered", "project_moved", "project_unmoved"))
    for d in (delivered, moved, unmoved):
        shutil.copytree(proj, d)
    (moved / ".llm-assembler").rename(moved / ".operational-platform")

    def pairs(args_list, cli_a, dir_a, cli_b, dir_b):       # the same commands, one tool in each directory
        out = []
        for args in args_list:
            a, b = call(cli_a, dir_a, *args), call(cli_b, dir_b, *args)
            out.append((" ".join(args).replace(str(exported), "batch_0001.tar.gz"), a[0], b[0], a[1] == b[1]))
        return out

    moved_rows = pairs([("status", "batch_0001"), ("show-file", "list.txt"), ("validate-post", "batch_0001"), ("status", "batch_0001")],
                       old_cli, delivered, renamed_cli, moved)
    import_rows = pairs([("import-batch", str(exported)), ("status", "batch_0001"), ("validate-plan", "batch_0001"),
                         ("apply-all", "batch_0001"), ("validate-post", "batch_0001"), ("show-file", "list.txt")],
                        old_cli, receiving_a, renamed_cli, receiving_b)
    rc, out = call(renamed_cli, unmoved, "status", "batch_0001")
    reply = json.loads(out)
    new_dir = unmoved / ".operational-platform"
    made = sorted(str(q.relative_to(unmoved)) for q in new_dir.rglob("*")) if new_dir.exists() else []

    L = ["| Step | Result |", "|---|---|",
         f"| The delivered tool registers a file, opens a batch, adds one descriptor, plans, exports the batch and applies it | {len(state)} files of state under `.llm-assembler/` |",
         f"| Files of that state that contain the old name | **{len(named)}** of {len(state)} |",
         f"| The renamed tool is asked for the batch in a copy that still has `.llm-assembler/` | `status` `{reply.get('status')}`, `counts` `{json.dumps(reply.get('counts'))}` — "
         f"the answer for a batch that does not exist; and a new `.operational-platform/` appears, holding {', '.join('`' + m + '`' for m in made) or 'nothing'} |",
         "", "After `mv .llm-assembler .operational-platform` in another copy, the same four commands were run by the delivered tool on the copy that kept its "
         "directory and by the renamed tool on the copy whose directory was renamed (the path of the project is masked as `<project>`, that of the tool as `<cli.py>`):", "",
         "| Command | Exit codes | Same reply |", "|---|:--:|:--:|"]
    L += [f"| `{cmd}` | {ca} and {cb} | {'yes' if same else '**NO**'} |" for cmd, ca, cb, same in moved_rows]
    L += ["", "The batch that the delivered tool exported before it applied it (the archive holds the batch's files and the payloads, and no name of the tool) "
          "was then imported into two more copies of the project, which held the registered file and no batch — by the delivered tool in the copy that kept its "
          "directory, and by the renamed tool in the copy whose directory was renamed:", "",
          "| Command | Exit codes | Same reply |", "|---|:--:|:--:|"]
    L += [f"| `{cmd}` | {ca} and {cb} | {'yes' if same else '**NO**'} |" for cmd, ca, cb, same in import_rows]
    Path(report).write_text("\n".join(L) + "\n", encoding="utf-8")
    ok = not named and all(r[3] for r in moved_rows + import_rows)
    print(f"state files: {len(state)}; naming the old tool: {len(named)}; replies identical after the move: {all(r[3] for r in moved_rows)}; "
          f"after the import: {all(r[3] for r in import_rows)}; phantom: {made}")
    sys.exit(0 if ok else 1)


def main(argv):
    if len(argv) == 6 and argv[1] == "build":
        build(*argv[2:6])
    elif len(argv) == 4 and argv[1] == "map":
        src = Path(argv[2])
        Path(argv[3]).write_text(rename_text(src.name, src.read_text(encoding="utf-8")), encoding="utf-8")
    elif len(argv) == 6 and argv[1] == "carry-over":
        carry_over(*argv[2:6])
    else:
        sys.exit(__doc__)


main(sys.argv)
