#!/usr/bin/env python3
"""Regression tests for the operational-platform skill.

Usage:
    python3 operational-platform-tests.py [PATH]

PATH is either a packaged operational-platform.skill (default: the one
sitting next to this file) or an unpacked skill directory containing
scripts/cli.py. The tests drive the real CLI as a subprocess, in throwaway
projects under a temp directory, so what passes here is what ships.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "operational-platform.skill"
WORK = Path(tempfile.mkdtemp(prefix="opplat_tests_"))
if target.is_dir():
    SCRIPTS = target / "scripts"
else:
    zipfile.ZipFile(target).extractall(WORK / "pkg")
    SCRIPTS = WORK / "pkg" / "operational-platform" / "scripts"
CLI = SCRIPTS / "cli.py"
ROOT = WORK / "projects"
STATE = ".operational-platform"
PASS = 0
FAIL = 0


def run(*args, cwd, env=None):
    r = subprocess.run([sys.executable, str(CLI), *args], cwd=cwd, capture_output=True, text=True, env=env)
    try:
        out = json.loads(r.stdout)
    except json.JSONDecodeError:
        out = {"_raw": r.stdout, "_stderr": r.stderr}
    return r.returncode, out


def check(label, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok  {label}")
    else:
        FAIL += 1
        print(f" FAIL {label}")


def project(name, files):
    d = ROOT / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    for fname, content in files.items():
        (d / fname).write_text(content)
    return d


def fid_of(name):
    return "f_" + hashlib.sha256(name.encode()).hexdigest()[:10]


def lid(fname, n):
    return f"{fid_of(fname)}_l{n:05d}"


def setup(name, content, fname="f.py"):
    d = project(name, {fname: content})
    run("register", fname, cwd=d)
    return d, d / fname


def new_batch(d, *extra):
    rc, out = run("new-batch", *extra, cwd=d)
    return out["batch_id"]


def replace(d, batch, fname, n, text, *extra):
    return run("add-descriptor", batch, "--op", "replace_range", "--file", fname,
               "--start", lid(fname, n), "--end", lid(fname, n), "--payload-text", text, *extra, cwd=d)


# ============================================================ core mechanics
print("== CORE-1: position drift survives insert+delete+replace in one batch ==")
d, fp = setup("c1", "a\nb\n\n\nc\nd\n\n\ne\nf\n")
b = new_batch(d)
run("add-descriptor", b, "--op", "insert_after", "--file", "f.py", "--after", lid("f.py", 1),
    "--payload-text", "INSERTED", cwd=d)
run("add-descriptor", b, "--op", "delete_range", "--file", "f.py",
    "--start", lid("f.py", 7), "--end", lid("f.py", 8), cwd=d)
run("add-descriptor", b, "--op", "replace_range", "--file", "f.py",
    "--start", lid("f.py", 9), "--end", lid("f.py", 10), "--payload-text", "REPLACED", cwd=d)
run("validate-plan", b, cwd=d)
rc, out = run("apply-all", b, cwd=d)
check("drift-surviving batch applies clean", rc == 0)
check("REPLACED landed despite two prior shifts", "REPLACED" in fp.read_text().splitlines())

print("== CORE-2: move_range ==")
d, fp = setup("c2", "one\ntwo\nthree\nfour\nfive\n")
b = new_batch(d)
run("add-descriptor", b, "--op", "move_range", "--file", "f.py", "--start", lid("f.py", 4),
    "--end", lid("f.py", 4), "--dest", lid("f.py", 1), cwd=d)
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
check("move earlier is correct", fp.read_text().splitlines() == ["one", "four", "two", "three", "five"])

print("== CORE-3: fault recovery does not double-apply ==")
d, fp = setup("c3", "x\ny\nz\n")
b = new_batch(d)
replace(d, b, "f.py", 2, "Y2")
run("validate-plan", b, cwd=d); run("apply-next", b, cwd=d)
dp = d / STATE / "batches" / b / "descriptors.json"
dd = json.loads(dp.read_text()); dd["descriptors"][0]["status"] = "pending"; dp.write_text(json.dumps(dd))
before = fp.read_text()
rc, out = run("apply-next", b, cwd=d)
check("recovered without re-touching the file", out.get("result") == "recovered" and fp.read_text() == before)

print("== CORE-4: abort on unexplained drift leaves the file alone ==")
d, fp = setup("c4", "p\nq\nr\n")
b = new_batch(d)
replace(d, b, "f.py", 2, "Q2")
run("validate-plan", b, cwd=d)
fp.write_text("p\nHAND-EDITED\nr\n")
rc, out = run("apply-next", b, cwd=d)
check("aborts", rc == 1 and out.get("result") == "abort")
check("file untouched after abort", fp.read_text() == "p\nHAND-EDITED\nr\n")

print("== CORE-5: overlapping edits are rejected ==")
d, fp = setup("c5", "a\nb\nc\nd\n")
b = new_batch(d)
run("add-descriptor", b, "--op", "replace_range", "--file", "f.py", "--start", lid("f.py", 2),
    "--end", lid("f.py", 3), "--payload-text", "X", cwd=d)
run("add-descriptor", b, "--op", "delete_range", "--file", "f.py", "--start", lid("f.py", 3),
    "--end", lid("f.py", 4), cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("overlap rejected", rc == 1 and "conflicts" in out)

print("== CORE-6: syntax check catches a broken file ==")
d, fp = setup("c6", "def foo():\n    return 1\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "def foo(")
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
rc, out = run("validate-post", b, cwd=d)
check("syntax error caught", rc == 1 and out["result"] == "fail")

print("== CORE-7: incomplete rename fails an invariant, with match context ==")
d, fp = setup("c7", "old_name = 1\nprint(old_name)\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "new_name = 1")
run("add-invariant", b, "--file", "f.py", "--pattern", "old_name", "--expected-count", "0", cwd=d)
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
rc, out = run("validate-post", b, cwd=d)
check("incomplete rename caught with the surviving line", rc == 1 and out["invariants"][0]["matches"][0]["line"] == 2)

# ===================================================================== gates
print("== GATE-1: a declared category must be closed or used ==")
d, fp = setup("g1", "a\nb\n")
b = new_batch(d)
run("add-category", b, "--code", "UNUSED", cwd=d)
replace(d, b, "f.py", 1, "A2")
rc, out = run("validate-plan", b, cwd=d)
check("blocked: category has no descriptor and isn't closed", rc == 1 and "taxonomy_incomplete" in out)
run("close-category", b, "--code", "UNUSED", "--note", "nothing found", cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("unblocked after close-category", rc == 0 and out["result"] == "pass")

print("== GATE-2: required file must be registered ==")
d, fp = setup("g2", "a\n")
b = new_batch(d)
run("require-file", b, "spec.md", cwd=d)
replace(d, b, "f.py", 1, "b")
rc, out = run("validate-plan", b, cwd=d)
check("blocked: required file never registered", rc == 1 and "materials_missing" in out)
(d / "spec.md").write_text("spec\n"); run("register", "spec.md", cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("unblocked once registered", rc == 0)

print("== GATE-3: source ranges need a disposition ==")
d, fp = setup("g3", "one\ntwo\nthree\nfour\n")
b = new_batch(d)
run("add-source-range", b, "--file", "f.py", "--start", lid("f.py", 1), "--end", lid("f.py", 4), cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("blocked: range has no disposition", rc == 1 and "inventory_incomplete" in out)
rc, out = run("inventory-next", b, cwd=d)
check("inventory-next returns the range content", out["content"] == ["one", "two", "three", "four"])
run("inventory-resolve", b, out["range_id"], "--disposition", "transferred_verbatim", cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("unblocked once resolved", rc == 0)

print("== GATE-4: opt-in file x category matrix ==")
d, fp = setup("g4", "a\n")
(d / "g.py").write_text("c\n"); run("register", "g.py", cwd=d)
b = new_batch(d)
run("add-category", b, "--code", "SWEEP", cwd=d)
run("set-category-scope", b, "--code", "SWEEP", "--files", "f.py,g.py", cwd=d)
replace(d, b, "f.py", 1, "A2", "--category", "SWEEP")
rc, out = run("validate-plan", b, cwd=d)
check("blocked: g.py in scope but uncovered", rc == 1 and any("g.py" in x for x in out.get("unit_category_matrix_incomplete", [])))
run("close-category-file", b, "--code", "SWEEP", "--file", "g.py", "--note", "clean", cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("unblocked once g.py closed for SWEEP", rc == 0)

print("== GATE-5: a declared shape must actually be used ==")
d, fp = setup("g5", "a\n")
b = new_batch(d, "--shape", "rename")
replace(d, b, "f.py", 1, "b")
rc, out = run("validate-plan", b, cwd=d)
check("rename shape blocked: domino never engaged", rc == 1 and "shape_incomplete" in out)
run("sync-domino-queue", b, cwd=d)
rc, out = run("domino-next", b, cwd=d)
run("domino-resolve", b, out["finding_id"], cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("unblocked once the queue is engaged and resolved", rc == 0)

print("== GATE-6: overlapping batches are refused ==")
d, fp = setup("g6", "a\nb\nc\n")
b1 = new_batch(d); b2 = new_batch(d)
replace(d, b1, "f.py", 1, "A2"); replace(d, b2, "f.py", 1, "A3")
rc1, _ = run("validate-plan", b1, cwd=d)
rc2, out2 = run("validate-plan", b2, cwd=d)
check("first batch locks the range", rc1 == 0)
check("second batch on the same line is refused", rc2 == 1 and "cross_batch_conflicts" in out2)

# ============================================================== invariants
print("== INV-1: accepted exceptions leave the failing count but stay listed ==")
d, fp = setup("i1", "old_name = 1\nold_name = 2\n")
b = new_batch(d)
run("add-invariant", b, "--file", "f.py", "--pattern", "old_name", "--expected-count", "0", cwd=d)
run("accept-match", b, "--file", "f.py", "--pattern", "old_name", "--line", "2", "--note", "kept on purpose", cwd=d)
run("validate-plan", b, cwd=d)
rc, out = run("validate-post", b, cwd=d)
inv = out["invariants"][0]
check("still fails: line 1 not accepted", rc == 1)
check("count excludes the accepted line", inv["actual"] == 1)
check("accepted match is still listed with its note", any(m.get("accepted") for m in inv["matches"]))

print("== INV-2: --exclude-comments drops whole-line comments ==")
d, fp = setup("i2", "# old_name is dead code, see old_name\nold_name = 2\n")
b = new_batch(d)
run("add-invariant", b, "--file", "f.py", "--pattern", "old_name", "--expected-count", "0", "--exclude-comments", cwd=d)
run("validate-plan", b, cwd=d)
rc, out = run("validate-post", b, cwd=d)
check("only the code line is counted", out["invariants"][0]["actual"] == 1 and rc == 1)

print("== INV-3: balanced_pairs ==")
d, fp = setup("i3", "def f(a, b):\n    return (a + b)\n")
b = new_batch(d)
run("add-invariant", b, "--file", "f.py", "--pattern", "()", "--expected-count", "0", "--type", "balanced_pairs", cwd=d)
run("validate-plan", b, cwd=d)
rc, out = run("validate-post", b, cwd=d)
check("balanced parentheses pass", rc == 0 and out["invariants"][0]["result"] == "pass")

print("== INV-4: --checked-against needs evidence the file was inspected ==")
d, fp = setup("i4", "old = 1\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "new = 1")
run("add-invariant", b, "--file", "f.py", "--pattern", "old", "--expected-count", "0",
    "--severity", "critical", "--checked-against", "spec_never_seen.md", cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("warns: the named file was never inspected", rc == 0 and any("never" in w or "no record" in w for w in out.get("warnings", [])))

print("== INV-5: rule_ref spelled two ways is flagged ==")
d, fp = setup("i5", "a\nb\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "A2", "--rule-ref=\u00a77.1")
replace(d, b, "f.py", 2, "B2", "--rule-ref=7.1")
rc, out = run("validate-plan", b, cwd=d)
check("flags the same clause written differently", rc == 0 and any("written differently" in w for w in out.get("warnings", [])))

# ======================================================= project-level scope
print("== SCOPE-1: project-level categories need no batch id ==")
d, fp = setup("s1", "a\nb\n")
rc, out = run("add-category", "--code", "GLOBAL", "--project", cwd=d)
check("add-category --project works without a batch id", rc == 0 and out.get("code") == "GLOBAL")
b = new_batch(d)
rc, out = replace(d, b, "f.py", 1, "A2", "--category", "GLOBAL")
check("a fresh batch can use it without re-declaring", rc == 0 and out["category"] == "GLOBAL")
rc, out = run("add-category", "--code", "LOCAL", cwd=d)
check("without --project a batch id is still required", rc == 2)

# =============================================================== file fidelity
print("== FIDELITY-1: CRLF survives an edit ==")
d = ROOT / "f1"; d.mkdir(parents=True)
(d / "f.py").write_bytes(b"a = 1\r\nb = 2\r\n")
run("register", "f.py", cwd=d)
b = new_batch(d)
replace(d, b, "f.py", 1, "a = 100")
run("validate-plan", b, cwd=d); run("apply-next", b, cwd=d)
raw = (d / "f.py").read_bytes()
check("both lines still end in CRLF", raw.count(b"\r\n") == 2)

# ================================================================== tooling
print("== TOOL-1: find-pattern, explain, dry-run, report ==")
d, fp = setup("t1", "token_x = 1\nprint(token_x)\n")
rc, out = run("find-pattern", "--pattern", "token_x", cwd=d)
check("find-pattern finds both occurrences", len(out["matches"]) == 2)
b = new_batch(d)
replace(d, b, "f.py", 1, "token_y = 1")
rc, out = run("explain", b, "d0001", cwd=d)
check("explain shows before and after", out["before"] == "token_x = 1" and out["after"] == "token_y = 1")
rc, out = run("dry-run", b, "--file", "f.py", cwd=d)
check("dry-run previews without touching the file",
      out["_raw"].strip() == "token_y = 1\nprint(token_x)" and fp.read_text() == "token_x = 1\nprint(token_x)\n")
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
rc, out = run("report", "--batches", b, cwd=d)
check("report gives a line delta", out["lines_now"] == out["lines_before"])

print("== TOOL-2: domino signal ratio ==")
d, fp = setup("t2", "shared_tok = 1\nprint(shared_tok)\nlonely = 2\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "shared_tok2 = 1", "--domino-hint=shared_tok")
replace(d, b, "f.py", 3, "lonely2 = 2")
run("sync-domino-queue", b, cwd=d)
for _ in range(2):
    rc, out = run("domino-next", b, cwd=d)
    run("domino-resolve", b, out["finding_id"], cwd=d)
rc, out = run("domino-status", b, cwd=d)
check("separates findings with candidates from empty ones",
      out["traced_with_candidates"] == 1 and out["traced_empty"] == 1)

print("== TOOL-3: batch export and import ==")
d, fp = setup("t3", "a\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "A2")
run("export-batch", b, "--out", str(d / "exported.tar.gz"), cwd=d)
check("export produced an archive", (d / "exported.tar.gz").exists())
d2, _ = setup("t3_import", "a\n")
rc, out = run("import-batch", str(d / "exported.tar.gz"), cwd=d2)
check("import reports success", "imported_from" in out)
rc, out = run("status", b, cwd=d2)
check("imported batch is visible in the new project", rc == 0 and out["batch_id"] == b)

print("== TOOL-4: status --group-by ==")
d, fp = setup("t4", "a\nb\n")
b = new_batch(d)
run("add-category", b, "--code", "X", cwd=d)
replace(d, b, "f.py", 1, "A2", "--category", "X")
rc, out = run("status", b, "--group-by", "category", cwd=d)
check("breaks the count down by category", out["grouped"].get("X") == 1)

print("== TOOL-5: cross-file move ==")
d = project("t5", {"src.py": "keep1\nMOVE_ME\nkeep2\n", "dst.py": "dest1\ndest2\n"})
run("register", "src.py", cwd=d); run("register", "dst.py", cwd=d)
b = new_batch(d)
run("move-across-files", b, "--src-file", "src.py", "--start", lid("src.py", 2), "--end", lid("src.py", 2),
    "--dest-file", "dst.py", "--dest-after", lid("dst.py", 1), cwd=d)
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
check("content left the source", (d / "src.py").read_text() == "keep1\nkeep2\n")
check("content arrived at the destination", (d / "dst.py").read_text() == "dest1\nMOVE_ME\ndest2\n")

print("== TOOL-6: templating across files ==")
d = project("t6", {"t1.py": "tok_a = 1\nprint(tok_a)\n", "t2.py": "x = tok_a\n"})
run("register", "t1.py", cwd=d); run("register", "t2.py", cwd=d)
b = new_batch(d)
rc, out = run("add-descriptor-template", b, "--find", "tok_a", "--replace", "tok_b", cwd=d)
check("one descriptor per match (3 across 2 files)", out["count"] == 3)
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
check("every occurrence renamed",
      (d / "t1.py").read_text() == "tok_b = 1\nprint(tok_b)\n" and (d / "t2.py").read_text() == "x = tok_b\n")

print("== TOOL-7: templating keeps indentation and treats find as literal text ==")
d = project("t7", {"t.py": "def f():\n    if x:\n        v = a.b(1)\n    return aXb\n"})
run("register", "t.py", cwd=d)
b = new_batch(d)
rc, out = run("add-descriptor-template", b, "--find", "a.b", "--replace", "c.d", cwd=d)
check("only the literal 'a.b' matched, not 'aXb'", out["count"] == 1)
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
check("indentation preserved",
      (d / "t.py").read_text() == "def f():\n    if x:\n        v = c.d(1)\n    return aXb\n")
rc, out = run("validate-post", b, cwd=d)
check("file still parses", rc == 0)

# ====================================================================== undo
print("== UNDO-1: every op reverses exactly ==")
cases = [("insert_after", "a\nb\n"), ("delete_range", "a\nb\nc\n"), ("replace_range", "a\nb\n"),
         ("move_range", "a\nb\nc\n"), ("copy_range", "a\nb\n")]
for op, content in cases:
    d, fp = setup(f"u_{op}", content)
    b = new_batch(d)
    original = fp.read_text()
    L = lambda n: lid("f.py", n)
    if op == "insert_after":
        run("add-descriptor", b, "--op", op, "--file", "f.py", "--after", L(1), "--payload-text", "NEW", cwd=d)
    elif op == "delete_range":
        run("add-descriptor", b, "--op", op, "--file", "f.py", "--start", L(2), "--end", L(2), cwd=d)
    elif op == "replace_range":
        replace(d, b, "f.py", 1, "CHANGED")
    elif op == "move_range":
        run("add-descriptor", b, "--op", op, "--file", "f.py", "--start", L(3), "--end", L(3), "--dest", L(1), cwd=d)
    elif op == "copy_range":
        run("add-descriptor", b, "--op", op, "--file", "f.py", "--start", L(1), "--end", L(1), "--dest", L(2), cwd=d)
    run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
    changed = fp.read_text() != original
    run("undo-descriptor", b, "d0001", cwd=d)
    check(f"undo {op}: the change happened, and undo restored the file exactly",
          changed and fp.read_text() == original)

print("== UNDO-2: an undone descriptor stays undone through the pipeline ==")
d, fp = setup("u2", "alpha\nbeta\ngamma\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "ALPHA"); replace(d, b, "f.py", 2, "BETA")
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
run("undo-descriptor", b, "d0001", cwd=d)
check("undo restored line 1 and left line 2 alone", fp.read_text() == "alpha\nBETA\ngamma\n")
run("apply-all", b, cwd=d)
check("apply-all does not 'recover' it back to applied (file unchanged)", fp.read_text() == "alpha\nBETA\ngamma\n")
rc, out = run("status", b, cwd=d)
check("status still shows undone, not applied", out["counts"] == {"undone": 1, "applied": 1})
rc, out = run("apply-next", b, cwd=d)
check("apply-next reports nothing left to do", out.get("result") == "done")
rc, out = run("validate-plan", b, cwd=d)
check("validate-plan passes with an undone descriptor present", rc == 0)
rc, out = run("validate-post", b, cwd=d)
check("validate-post accepts the batch and lists what was undone", rc == 0 and out.get("undone_descriptors") == ["d0001"])
lock_file = d / STATE / "active_locks.json"
locks = json.loads(lock_file.read_text()) if lock_file.exists() else {"batches": {}}
check("the batch reached a terminal state and released its lock", b not in locks["batches"])
probe = subprocess.run([sys.executable, "-c",
    f"import sys; sys.path.insert(0, {str(SCRIPTS)!r}); import engine; "
    f"print(engine._wal_has_applied('{b}', 'd0001')); print(engine.apply_descriptor('{b}', 'd0001')['result'])"],
    cwd=d, capture_output=True, text=True)
check("WAL ordering: a later undo cancels the earlier op_applied", probe.stdout.split()[0] == "False")
check("apply_descriptor itself refuses an undone descriptor", probe.stdout.split()[1] == "skipped")

# =============================================================== batch ids
print("== IDS-1: an unknown batch id is an error and leaves nothing behind ==")
d, fp = setup("ids1", "a\n")
rc, out = run("status", "batch_9999", cwd=d)
check("status on a nonexistent batch is rejected", rc == 2 and "no such batch" in out.get("error", ""))
rc, out = run("validate-plan", "batch_9999", cwd=d)
check("validate-plan on a nonexistent batch is rejected", rc == 2)
check("no phantom directory was created", not (d / STATE / "batches" / "batch_9999").exists())
check("the next real batch is batch_0001, no gap", new_batch(d) == "batch_0001")

print("== IDS-2: an imported batch can't be overwritten by the next new-batch ==")
dA, _ = setup("ids2a", "a\nb\n")
for _ in range(3):
    new_batch(dA)
replace(dA, "batch_0003", "f.py", 1, "A2")
run("export-batch", "batch_0003", "--out", str(dA / "b3.tar.gz"), cwd=dA)
dB, _ = setup("ids2b", "a\nb\n")
new_batch(dB)
rc, out = run("import-batch", str(dA / "b3.tar.gz"), cwd=dB)
check("import brought batch_0003 into a project holding only batch_0001", "imported_from" in out)
check("new-batch numbers past the highest id, not the count", new_batch(dB) == "batch_0004")
rc, out = run("status", "batch_0003", cwd=dB)
check("the imported batch still has its descriptor", out["counts"].get("pending") == 1)

print("== SCOPE-2: a project-level category is vocabulary, not an obligation ==")
d, fp = setup("s2", "a\nb\n")
run("add-category", "--code", "SEC_AUDIT", "--project", cwd=d)
b = new_batch(d)
replace(d, b, "f.py", 1, "A2")
rc, out = run("validate-plan", b, cwd=d)
check("an unrelated batch is not blocked by an inherited category", rc == 0 and out["result"] == "pass")
b2 = new_batch(d)
replace(d, b2, "f.py", 2, "B2")
run("set-category-scope", b2, "--code", "SEC_AUDIT", "--files", "f.py", cwd=d)
rc, out = run("validate-plan", b2, cwd=d)
check("scoping it in a batch is the opt-in that creates the obligation",
      rc == 1 and ("taxonomy_incomplete" in out or "unit_category_matrix_incomplete" in out))

print("== TOOL-3b: a refused import leaves nothing behind and doesn't poison the next one ==")
dA, _ = setup("t3b_a", "a\n")
new_batch(dA)
run("export-batch", "batch_0001", "--out", str(dA / "b1.tar.gz"), cwd=dA)
dB, _ = setup("t3b_b", "a\n")
new_batch(dB)                                      # B already owns batch_0001
rc, out = run("import-batch", str(dA / "b1.tar.gz"), cwd=dB)
check("importing onto an existing id is refused", rc == 2 and "already exists" in out.get("error", ""))
check("no temp directory is left behind", not (dB / STATE / "_import_tmp").exists())
dC, _ = setup("t3b_c", "a\n")
for _ in range(2):
    new_batch(dC)
run("export-batch", "batch_0002", "--out", str(dC / "b2.tar.gz"), cwd=dC)
rc, out = run("import-batch", str(dC / "b2.tar.gz"), cwd=dB)
check("a later, valid import still works", rc == 0 and "imported_from" in out)

print("== TOOL-3c: an archive that tries to write outside the project is rejected ==")
import io, tarfile
evil = dB / "evil.tar.gz"
with tarfile.open(evil, "w:gz") as tf:
    info = tarfile.TarInfo("../escaped.txt"); data = b"nope"; info.size = len(data)
    tf.addfile(info, io.BytesIO(data))
rc, out = run("import-batch", str(evil), cwd=dB)
check("path traversal is refused", rc == 2)
check("nothing was written outside the state directory", not (dB.parent / "escaped.txt").exists()
      and not (dB / STATE / "escaped.txt").exists())

# ============================== claims made in the docs, checked one by one
print("== DOCS-1: .js is syntax-checked with node, and skipped (not failed) without it ==")
d = project("dj", {"a.js": "var a = 1;\n"}); run("register", "a.js", cwd=d)
b = new_batch(d)
replace(d, b, "a.js", 1, "var a = ;")
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
rc, out = run("validate-post", b, cwd=d)
if shutil.which("node"):
    check("a broken .js file fails validate-post", rc == 1)
    d = project("dj2", {"a.js": "var a = 1;\n"}); run("register", "a.js", cwd=d)
    b = new_batch(d)
    replace(d, b, "a.js", 1, "var a = ;")
    run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
    rc, out = run("validate-post", b, cwd=d, env=dict(os.environ, PATH="/nonexistent"))
    check("without node it reports 'skipped' and does not fail",
          rc == 0 and any("skipped" in str(v) for v in out["syntax"].values()))
else:
    print("  --  node not installed here; the .js checks were not exercised")

print("== DOCS-2: a file with mixed line endings is normalised on its first edit ==")
d = project("dm", {}); (d / "f.py").write_bytes(b"a\r\nb\nc\n"); run("register", "f.py", cwd=d)
reg = json.loads((d / STATE / "registry.json").read_text())
check("detected as CRLF because \\r\\n is present", list(reg["files"].values())[0]["line_ending"] == "crlf")
b = new_batch(d)
replace(d, b, "f.py", 2, "B")
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
check("every line, including untouched ones, now ends in CRLF", (d / "f.py").read_bytes() == b"a\r\nB\r\nc\r\n")

print("== DOCS-3: a template match on an already-targeted line surfaces at validate-plan ==")
d, fp = setup("d3", "tok = 1\nother = 2\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "something_else = 1")
run("add-descriptor-template", b, "--find", "tok", "--replace", "new_tok", cwd=d)
rc, out = run("validate-plan", b, cwd=d)
check("the overlap is reported as a conflict, not silently skipped", rc == 1 and "conflicts" in out)

print("== DOCS-4: status --group-by nests by several fields; find-pattern --file restricts ==")
d = project("d4", {"x.py": "tok\n", "y.py": "tok\n"})
run("register", "x.py", cwd=d); run("register", "y.py", cwd=d)
b = new_batch(d)
run("add-category", b, "--code", "C", cwd=d)
replace(d, b, "x.py", 1, "A", "--category", "C")
rc, out = run("status", b, "--group-by", "file_id,category", cwd=d)
check("two-level grouping", out["grouped"][fid_of("x.py")]["C"] == 1)
rc, out = run("find-pattern", "--pattern", "tok", cwd=d)
check("without --file both files match", len(out["matches"]) == 2)
rc, out = run("find-pattern", "--pattern", "tok", "--file", "x.py", cwd=d)
check("with --file only that file matches", [m["path"] for m in out["matches"]] == ["x.py"])

print("== DOCS-5: undo refuses when something else changed the line since ==")
d, fp = setup("d5", "alpha\nbeta\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "ALPHA")
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
fp.write_text("HAND-EDITED\nbeta\n")
rc, out = run("undo-descriptor", b, "d0001", cwd=d)
check("undo is refused", rc == 2 and "no longer matches" in out.get("error", ""))
check("and the file is left as it was", fp.read_text() == "HAND-EDITED\nbeta\n")

print("== DOCS-6: a descriptor from before undo support can't be undone ==")
d, fp = setup("d6", "alpha\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "ALPHA")
run("validate-plan", b, cwd=d); run("apply-all", b, cwd=d)
dp = d / STATE / "batches" / b / "descriptors.json"
dd = json.loads(dp.read_text())
dd["descriptors"][0]["created_ids"] = None; dd["descriptors"][0]["pre_payload_ref"] = None
dp.write_text(json.dumps(dd))
rc, out = run("undo-descriptor", b, "d0001", cwd=d)
check("refused, and says why", rc == 2 and "predates undo support" in out.get("error", ""))

print("== DOCS-7: inventory-resolve validates what it is given ==")
d, fp = setup("d7", "one\ntwo\n")
b = new_batch(d)
run("add-source-range", b, "--file", "f.py", "--start", lid("f.py", 1), "--end", lid("f.py", 2), cwd=d)
rc, out = run("inventory-resolve", b, "ri0001", "--disposition", "transferred_with_edit", cwd=d)
check("transferred_with_edit without descriptor ids is rejected", rc == 2)
rc, out = run("inventory-resolve", b, "ri0001", "--disposition", "transferred_with_edit",
              "--descriptor-ids", "d9999", cwd=d)
check("an unknown descriptor id is rejected", rc == 2 and "not found" in out.get("error", ""))

print("== DOCS-8: each shape names what it requires ==")
for shape, expect in [("assembly", 1), ("conformance", 1), ("transition", 2)]:
    d, fp = setup(f"d8_{shape}", "a\n")
    b = new_batch(d, "--shape", shape)
    replace(d, b, "f.py", 1, "b")
    rc, out = run("validate-plan", b, cwd=d)
    check(f"{shape}: blocked, with {expect} unmet requirement(s) listed",
          rc == 1 and len(out.get("shape_incomplete", [])) == expect)

print("== DOCS-9: dry-run is a preview that does not check hashes (as documented) ==")
d, fp = setup("d9", "alpha\nbeta\n")
b = new_batch(d)
replace(d, b, "f.py", 1, "ALPHA")
run("validate-plan", b, cwd=d)
fp.write_text("drifted\nbeta\n")
rc, out = run("dry-run", b, "--file", "f.py", cwd=d)
check("dry-run shows a clean result for a file that has since drifted", out["_raw"].strip() == "ALPHA\nbeta")
rc, out = run("apply-next", b, cwd=d)
check("while apply-next aborts on the same file", rc == 1 and out.get("result") == "abort")

print("== DOCS-10: release-lock clears an abandoned batch's lock ==")
d, fp = setup("d10", "a\nb\n")
b1 = new_batch(d); b2 = new_batch(d)
replace(d, b1, "f.py", 1, "A1"); replace(d, b2, "f.py", 1, "A2")
run("validate-plan", b1, cwd=d)
rc, out = run("validate-plan", b2, cwd=d)
check("the second batch is blocked by the first", rc == 1 and "cross_batch_conflicts" in out)
rc, out = run("release-lock", b1, cwd=d)
check("release-lock reports the lock was held, with a warning", out.get("released") is True and "warning" in out)
rc, out = run("validate-plan", b2, cwd=d)
check("the second batch now validates", rc == 0)
rc, out = run("release-lock", b1, cwd=d)
check("releasing again is harmless and says nothing was held", rc == 0 and out.get("released") is False)

# ==================================================================== legacy
print("== LEGACY-1: a project with the old state directory keeps its state ==")
d, fp = setup("l1", "a\nb\n")
(d / STATE).rename(d / ".llm-assembler")
b = new_batch(d)
check("the old directory is used, and no new one appears beside it",
      (d / ".llm-assembler" / "batches" / b).exists() and not (d / STATE).exists())

print()
print("=" * 60)
print(f"TOTAL: {PASS} passed, {FAIL} failed")
print("=" * 60)
shutil.rmtree(WORK, ignore_errors=True)
sys.exit(1 if FAIL else 0)
