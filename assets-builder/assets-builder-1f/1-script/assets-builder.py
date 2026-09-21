#!/usr/bin/env python3
"""
assets-builder.py

Merges a front-end project's CSS/JS into two documented distributable files.
Implemented per TZ-assets-builder-script.md and PLAN-assets-builder-script.md.

File sections correspond to the plan's task categories (script-001..016):
  DISCOVERY, CLI, HTML_PARSE, NESTED_DEPS, DEP_GRAPH, CLASSIFICATION,
  DOMINO, CONFLICT_CSS, CONFLICT_JS, MERGE_CSS, MERGE_JS, REPORT,
  USAGE_MAP, CACHE.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
from collections import deque
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import tinycss2
except ImportError:
    tinycss2 = None

CACHE_VERSION = 1

# Always excluded from DISCOVERY, regardless of the user's --exclude:
# without this, a repeat build run would pick up dist/style.css and
# dist/scripts.js from the PREVIOUS run as ordinary sources (self-contamination).
DEFAULT_EXCLUDE = ["dist/**", ".git/**", "node_modules/**"]


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class FileRecord:
    abs_path: str
    rel_path: str
    size: int
    mtime: str
    hash: str
    file_type: str  # 'html' | 'css' | 'js'


@dataclass
class HtmlInclude:
    kind: str  # 'css-link' | 'css-inline' | 'js-src' | 'js-inline'
    href: str | None
    line: int
    is_external: bool
    attrs: dict
    resolved_rel: str | None = None
    inline_content: str | None = None


@dataclass
class CssImport:
    target_href: str
    media: str
    line: int
    resolved_rel: str | None = None


@dataclass
class JsModuleDep:
    kind: str
    target: str
    line: int


@dataclass
class Classification:
    label: str  # 'shared' | 'page-specific' | 'orphan' | 'vendor'
    used_by_pages: list


@dataclass
class CssRule:
    selector: str
    declarations: dict
    line: int


@dataclass
class JsSymbol:
    name: str
    line: int
    body_hash: str


@dataclass
class Conflict:
    conflict_type: str  # 'css-selector' | 'js-symbol'
    name: str
    files: list
    severity: str  # 'low' | 'medium' | 'high'
    detail: str


# ============================================================
# DISCOVERY (script-001)
# ============================================================

def compute_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def is_excluded(rel_path: str, patterns: list) -> bool:
    return any(fnmatch.fnmatch(rel_path, pat) for pat in patterns if pat)


def discover_files(project_root: Path, exclude_patterns: list) -> dict:
    files = {}
    for ext, ftype in [("*.html", "html"), ("*.css", "css"), ("*.js", "js")]:
        for path in sorted(project_root.rglob(ext)):
            if not path.is_file():
                continue
            rel = path.relative_to(project_root).as_posix()
            if is_excluded(rel, exclude_patterns):
                continue
            try:
                stat = path.stat()
                files[rel] = FileRecord(
                    abs_path=str(path),
                    rel_path=rel,
                    size=stat.st_size,
                    mtime=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    hash=compute_hash(path),
                    file_type=ftype,
                )
            except (OSError, UnicodeDecodeError) as e:
                print(f"[warn] skipped unreadable file {rel}: {e}", file=sys.stderr)
    return files


def read_text_safe(path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def count_lines(path) -> int:
    try:
        return read_text_safe(path).count("\n") + 1
    except Exception:
        return 0


# ============================================================
# HTML_PARSE (script-003)
# ============================================================

def is_external_url(url: str) -> bool:
    if not url:
        return False
    return url.startswith("http://") or url.startswith("https://") or url.startswith("//")


def resolve_href(html_abs_path: Path, href: str, project_root: Path) -> str | None:
    if not href or is_external_url(href):
        return None
    href_clean = href.split("#")[0].split("?")[0]
    if not href_clean:
        return None
    try:
        if href_clean.startswith("/"):
            target = (project_root / href_clean.lstrip("/")).resolve()
        else:
            target = (html_abs_path.parent / href_clean).resolve()
        rel = target.relative_to(project_root.resolve())
        return rel.as_posix()
    except (ValueError, OSError):
        return None


def parse_html_file(rel_path: str, rec: FileRecord, project_root: Path) -> list:
    if BeautifulSoup is None:
        raise RuntimeError("beautifulsoup4 is not installed: pip install beautifulsoup4 --break-system-packages")
    text = read_text_safe(rec.abs_path)
    soup = BeautifulSoup(text, "html.parser")
    includes = []
    html_abs_path = Path(rec.abs_path)
    for tag in soup.find_all(["link", "style", "script"]):
        if tag.name == "link":
            rel_attr = tag.get("rel") or []
            if isinstance(rel_attr, str):
                rel_attr = [rel_attr]
            if "stylesheet" not in [r.lower() for r in rel_attr]:
                continue
            href = tag.get("href", "")
            includes.append(HtmlInclude(
                kind="css-link", href=href, line=tag.sourceline or 0,
                is_external=is_external_url(href), attrs=dict(tag.attrs),
                resolved_rel=resolve_href(html_abs_path, href, project_root),
            ))
        elif tag.name == "style":
            includes.append(HtmlInclude(
                kind="css-inline", href=None, line=tag.sourceline or 0,
                is_external=False, attrs=dict(tag.attrs),
                inline_content=tag.string or "",
            ))
        elif tag.name == "script":
            src = tag.get("src")
            if src:
                includes.append(HtmlInclude(
                    kind="js-src", href=src, line=tag.sourceline or 0,
                    is_external=is_external_url(src), attrs=dict(tag.attrs),
                    resolved_rel=resolve_href(html_abs_path, src, project_root),
                ))
            else:
                includes.append(HtmlInclude(
                    kind="js-inline", href=None, line=tag.sourceline or 0,
                    is_external=False, attrs=dict(tag.attrs),
                    inline_content=tag.string or "",
                ))
    return includes


# ============================================================
# NESTED_DEPS (script-004)
# ============================================================

CSS_IMPORT_RE = re.compile(
    r'@import\s+(?:url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)|[\'"]([^\'"]+)[\'"])\s*([^;]*);',
    re.IGNORECASE,
)


def parse_css_imports(rel_path: str, rec: FileRecord, project_root: Path) -> list:
    text = read_text_safe(rec.abs_path)
    imports = []
    html_abs_path = Path(rec.abs_path)
    for i, line in enumerate(text.split("\n"), start=1):
        m = CSS_IMPORT_RE.search(line)
        if m:
            href = m.group(1) or m.group(2)
            media = (m.group(3) or "").strip()
            imports.append(CssImport(
                target_href=href, media=media, line=i,
                resolved_rel=resolve_href(html_abs_path, href, project_root),
            ))
    return imports


JS_IMPORT_RE = re.compile(r'^\s*import\s+.+?\sfrom\s+[\'"]([^\'"]+)[\'"]')
JS_EXPORT_FROM_RE = re.compile(r'^\s*export\s+.+?\sfrom\s+[\'"]([^\'"]+)[\'"]')
JS_REQUIRE_RE = re.compile(r'require\(\s*[\'"]([^\'"]+)[\'"]\s*\)')


def parse_js_module_deps(rec: FileRecord) -> list:
    text = read_text_safe(rec.abs_path)
    deps = []
    for lineno, line in enumerate(text.split("\n"), start=1):
        for pat, kind in [(JS_IMPORT_RE, "import"), (JS_EXPORT_FROM_RE, "export-from"), (JS_REQUIRE_RE, "require")]:
            m = pat.search(line)
            if m:
                deps.append(JsModuleDep(kind=kind, target=m.group(1), line=lineno))
    return deps


# ============================================================
# DEP_GRAPH (script-005)
# ============================================================

class DependencyGraph:
    def __init__(self):
        self.edges = {}          # node -> set(depends_on)
        self.reverse_edges = {}  # node -> set(depended_on_by)

    def add_edge(self, src: str, dst: str):
        self.edges.setdefault(src, set()).add(dst)
        self.reverse_edges.setdefault(dst, set()).add(src)
        self.edges.setdefault(dst, set())
        self.reverse_edges.setdefault(src, set())

    def ensure_node(self, node: str):
        self.edges.setdefault(node, set())
        self.reverse_edges.setdefault(node, set())

    def forward_closure(self, start: str, max_depth: int = 50) -> set:
        visited = set()
        stack = [(start, 0)]
        while stack:
            node, depth = stack.pop()
            if node in visited or depth > max_depth:
                continue
            visited.add(node)
            for nxt in self.edges.get(node, ()):
                if nxt not in visited:
                    stack.append((nxt, depth + 1))
        visited.discard(start)
        return visited

    def backward_closure(self, start: str, max_depth: int = 50) -> set:
        visited = set()
        stack = [(start, 0)]
        while stack:
            node, depth = stack.pop()
            if node in visited or depth > max_depth:
                continue
            visited.add(node)
            for prev in self.reverse_edges.get(node, ()):
                if prev not in visited:
                    stack.append((prev, depth + 1))
        visited.discard(start)
        return visited

    def detect_cyclic_nodes(self, max_depth: int = 50) -> list:
        cyclic = []
        for node in self.edges:
            if node in self.forward_closure(node, max_depth=max_depth):
                cyclic.append(node)
        return sorted(cyclic)


def build_dependency_graph(files: dict, html_includes: dict, css_imports: dict, project_root: Path) -> DependencyGraph:
    graph = DependencyGraph()
    for rel in files:
        graph.ensure_node(rel)
    for html_rel, includes in html_includes.items():
        for inc in includes:
            if inc.kind in ("css-link", "js-src") and not inc.is_external and inc.resolved_rel:
                if inc.resolved_rel in files:
                    graph.add_edge(html_rel, inc.resolved_rel)
    for css_rel, imports in css_imports.items():
        for imp in imports:
            if imp.resolved_rel and imp.resolved_rel in files:
                graph.add_edge(css_rel, imp.resolved_rel)
    return graph


# ============================================================
# CLASSIFICATION (script-006)
# ============================================================

def is_vendor_heuristic(rel_path: str) -> bool:
    lower = rel_path.lower()
    if re.search(r"\.min\.(css|js)$", lower):
        return True
    for marker in ("vendor/", "lib/", "libs/", "plugins/", "node_modules/"):
        if marker in lower:
            return True
    return False


def classify_files(files: dict, html_files: list, graph: DependencyGraph, vendor_patterns: list) -> dict:
    result = {}
    page_closures = {h: graph.forward_closure(h) for h in html_files}
    for rel, rec in files.items():
        if rec.file_type == "html":
            continue
        is_vendor = is_excluded(rel, vendor_patterns) or is_vendor_heuristic(rel)
        pages = sorted(h for h in html_files if rel in page_closures[h])
        if is_vendor:
            label = "vendor"
        elif len(pages) == 0:
            label = "orphan"
        elif len(pages) == 1:
            label = "page-specific"
        else:
            label = "shared"
        result[rel] = Classification(label=label, used_by_pages=pages)
    return result


# ============================================================
# DOMINO (script-007)
# ============================================================

def domino_impact(graph: DependencyGraph, target: str, html_files: list) -> list:
    affected = graph.backward_closure(target)
    return sorted(p for p in affected if p in html_files)


# ============================================================
# CONFLICT_CSS (script-008)
# ============================================================

def split_selector_list(selector: str) -> list:
    return [s.strip() for s in selector.split(",") if s.strip()]


def extract_css_rules(rec: FileRecord) -> list:
    if tinycss2 is None:
        raise RuntimeError("tinycss2 is not installed: pip install tinycss2 --break-system-packages")
    text = read_text_safe(rec.abs_path)
    rules = []
    try:
        stylesheet = tinycss2.parse_stylesheet(text, skip_comments=True, skip_whitespace=True)
    except Exception as e:
        print(f"[warn] failed to parse CSS {rec.rel_path}: {e}", file=sys.stderr)
        return rules
    for node in stylesheet:
        if getattr(node, "type", None) != "qualified-rule":
            continue
        raw_selector = re.sub(r"\s+", " ", tinycss2.serialize(node.prelude).strip())
        declarations = {}
        try:
            for decl in tinycss2.parse_declaration_list(node.content, skip_comments=True, skip_whitespace=True):
                if getattr(decl, "type", None) == "declaration":
                    declarations[decl.lower_name] = tinycss2.serialize(decl.value).strip()
        except Exception:
            pass
        line = getattr(node, "source_line", 0) or 0
        for single in split_selector_list(raw_selector):
            rules.append(CssRule(selector=single, declarations=dict(declarations), line=line))
    return rules


def detect_css_conflicts(css_rules_by_file: dict) -> list:
    by_selector = {}
    for file, rules in css_rules_by_file.items():
        for rule in rules:
            by_selector.setdefault(rule.selector, []).append((file, rule))
    conflicts = []
    for selector, occurrences in sorted(by_selector.items()):
        files_involved = sorted(set(f for f, _ in occurrences))
        if len(files_involved) < 2:
            continue
        all_decls = [r.declarations for _, r in occurrences]
        if all(d == all_decls[0] for d in all_decls):
            severity, detail = "low", "identical declarations in every occurrence (exact duplicate)"
        else:
            seen_props, overlapping_props = set(), set()
            for d in all_decls:
                overlapping_props |= (seen_props & set(d.keys()))
                seen_props |= set(d.keys())
            if not overlapping_props:
                severity, detail = "medium", "different properties — the cascade will combine them without loss"
            else:
                real_conflict = any(
                    len(set(d.get(p) for d in all_decls if p in d)) > 1
                    for p in overlapping_props
                )
                if real_conflict:
                    severity = "high"
                    detail = f"overlapping properties with different values: {sorted(overlapping_props)}"
                else:
                    severity, detail = "low", "overlapping properties, but the values match"
        conflicts.append(Conflict("css-selector", selector, files_involved, severity, detail))
    return conflicts


# ============================================================
# CONFLICT_JS (script-009)
# ============================================================

JS_TOP_LEVEL_FUNC_RE = re.compile(r"^function\s+([A-Za-z_$][\w$]*)\s*\(")
JS_TOP_LEVEL_VAR_RE = re.compile(r"^(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=")
JS_WINDOW_ASSIGN_RE = re.compile(r"^window\.([A-Za-z_$][\w$]*)\s*=")


def extract_js_top_level_symbols(rec: FileRecord, window: int = 12) -> list:
    text = read_text_safe(rec.abs_path)
    lines = text.split("\n")
    symbols = []
    for idx, line in enumerate(lines):
        for pat in (JS_TOP_LEVEL_FUNC_RE, JS_TOP_LEVEL_VAR_RE, JS_WINDOW_ASSIGN_RE):
            m = pat.match(line)
            if m:
                name = m.group(1)
                snippet = "\n".join(lines[idx: idx + window])
                body_hash = hashlib.md5(snippet.encode("utf-8", "replace")).hexdigest()[:8]
                symbols.append(JsSymbol(name=name, line=idx + 1, body_hash=body_hash))
    return symbols


def detect_js_conflicts(js_symbols_by_file: dict) -> list:
    by_name = {}
    for file, symbols in js_symbols_by_file.items():
        for sym in symbols:
            by_name.setdefault(sym.name, []).append((file, sym))
    conflicts = []
    for name, occurrences in sorted(by_name.items()):
        files_involved = sorted(set(f for f, _ in occurrences))
        if len(files_involved) < 2:
            continue
        hashes = set(s.body_hash for _, s in occurrences)
        if len(hashes) == 1:
            severity, detail = "low", "identical body (by first-lines fingerprint) — exact duplicate"
        else:
            severity = "high"
            detail = "same name, different body — the last definition silently wins when concatenated"
        conflicts.append(Conflict("js-symbol", name, files_involved, severity, detail))
    return conflicts


# ============================================================
# Shared plumbing: topological order for the build (used by MERGE_CSS/MERGE_JS)
# ============================================================

def compute_first_seen_order(html_files: list, includes_by_page: dict) -> dict:
    """"First seen" index for a deterministic tie-break during topological sort."""
    order = {}
    counter = 0
    for page in html_files:
        for inc in includes_by_page.get(page, []):
            if inc.resolved_rel and inc.resolved_rel not in order:
                order[inc.resolved_rel] = counter
                counter += 1
    return order


def topological_order(files: list, graph: DependencyGraph, first_seen: dict) -> list:
    """Files that others depend on (via @import/import) come first.
    Ties broken by first-appearance order in HTML, otherwise alphabetically."""
    file_set = set(files)
    precede = {f: set() for f in files}  # a -> {b, ...}: a must come before b
    for f in files:
        for dep in graph.edges.get(f, ()):
            if dep in file_set:
                precede.setdefault(dep, set()).add(f)
    in_degree = {f: 0 for f in files}
    for a, targets in precede.items():
        for b in targets:
            if b in in_degree:
                in_degree[b] += 1

    def sort_key(f):
        return (first_seen.get(f, 10**9), f)

    ready = sorted([f for f in files if in_degree[f] == 0], key=sort_key)
    queue = deque(ready)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        nxts = sorted(precede.get(node, ()), key=sort_key)
        for nxt in nxts:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)
        queue = deque(sorted(queue, key=sort_key))
    remaining = [f for f in files if f not in order]
    if remaining:
        order.extend(sorted(remaining, key=sort_key))  # a cycle — don't abort the build, just append as-is
    return order


# ============================================================
# MERGE_CSS / MERGE_JS (script-010, script-011)
# ============================================================

HEADER_LABELS = {
    "en": dict(file="FILE", scope="SCOPE", used="USED ON", size="SIZE",
               depends="DEPENDS ON", conflicts="CONFLICTS", orphanwarn="ORPHAN — not linked from any scanned HTML page"),
    "ru": dict(file="ФАЙЛ", scope="ОБЛАСТЬ", used="ИСПОЛЬЗУЕТСЯ НА", size="РАЗМЕР",
               depends="ЗАВИСИТ ОТ", conflicts="КОНФЛИКТЫ", orphanwarn="ORPHAN — не подключён ни на одной просканированной странице"),
}


def make_section_header(rel: str, rec: FileRecord, classification: Classification,
                          deps: list, conflicts_for_file: list, comment_lang: str,
                          unused_note: str | None) -> str:
    L = HEADER_LABELS[comment_lang]
    lines = ["/* ============================================================"]
    lines.append(f"   {L['file']}: {rel}")
    lines.append(f"   {L['scope']}: {classification.label}")
    if classification.label == "orphan":
        lines.append(f"   ⚠ {L['orphanwarn']}")
    if classification.used_by_pages:
        lines.append(f"   {L['used']}: {', '.join(classification.used_by_pages)}")
    lines.append(f"   {L['size']}: {rec.size} bytes | {count_lines(rec.abs_path)} lines")
    if deps:
        lines.append(f"   {L['depends']}: {', '.join(deps)}")
    if conflicts_for_file:
        cstr = "; ".join(f"{c.name} (severity: {c.severity})" for c in conflicts_for_file)
        lines.append(f"   {L['conflicts']}: {cstr}")
    if unused_note:
        lines.append(f"   {unused_note}")
    lines.append("   ============================================================ */")
    return "\n".join(lines)


def group_and_order(kind: str, files: dict, classification: dict, graph: DependencyGraph,
                      html_files: list, first_seen: dict) -> list:
    subset = [f for f, r in files.items() if r.file_type == kind]
    vendor = [f for f in subset if classification[f].label == "vendor"]
    shared = [f for f in subset if classification[f].label == "shared"]
    page_specific = [f for f in subset if classification[f].label == "page-specific"]
    orphan = [f for f in subset if classification[f].label == "orphan"]

    ordered = topological_order(vendor, graph, first_seen)
    ordered += topological_order(shared, graph, first_seen)
    for page in html_files:
        page_files = [f for f in page_specific if page in classification[f].used_by_pages]
        ordered += topological_order(page_files, graph, first_seen)
    ordered += topological_order(orphan, graph, first_seen)
    return ordered


def build_conflicts_by_file(conflicts: list) -> dict:
    out = {}
    for c in conflicts:
        for f in c.files:
            out.setdefault(f, []).append(c)
    return out


def build_merged_css(files, classification, graph, css_conflicts, html_files, first_seen,
                       css_imports, comment_lang, usage_map, strip_unused) -> tuple:
    ordered = group_and_order("css", files, classification, graph, html_files, first_seen)
    conflicts_by_file = build_conflicts_by_file(css_conflicts)

    media_qualifier = {}
    for imports in css_imports.values():
        for imp in imports:
            if imp.resolved_rel and imp.media:
                media_qualifier[imp.resolved_rel] = imp.media

    unused_by_file = {}
    if usage_map:
        for sel, info in usage_map.get("cssSelectors", {}).items():
            if info["status"] in ("unused", "dynamic-suspect"):
                for d in info["definedIn"]:
                    unused_by_file.setdefault(d["file"], []).append((sel, info["status"]))

    toc = ["/* ============================================================",
           "   TABLE OF CONTENTS" if comment_lang == "en" else "   ОГЛАВЛЕНИЕ",
           "   ============================================================"]
    for f in ordered:
        c = classification[f]
        used = f" | used on: {', '.join(c.used_by_pages)}" if c.used_by_pages else ""
        toc.append(f"   - {f}  [{c.label}]{used}")
    toc.append("   ============================================================ */")

    parts = ["\n".join(toc)]
    for f in ordered:
        rec = files[f]
        deps = sorted(d for d in graph.edges.get(f, ()) if d in files and files[d].file_type == "css")
        unused_note = None
        if f in unused_by_file:
            items = unused_by_file[f]
            unused_str = ", ".join(f"{s} ({st})" for s, st in items)
            tag = "⚠ POSSIBLY UNUSED (per analysis)" if comment_lang == "en" else "⚠ ВОЗМОЖНО НЕ ИСПОЛЬЗУЕТСЯ (по данным анализа)"
            unused_note = f"{tag}: {unused_str}"
        header = make_section_header(f, rec, classification[f], deps, conflicts_by_file.get(f, []), comment_lang, unused_note)
        content = read_text_safe(rec.abs_path).rstrip()

        if strip_unused and f in unused_by_file:
            content = strip_unused_css_rules(content, [s for s, st in unused_by_file[f] if st == "unused"])

        if f in media_qualifier:
            content = f"@media {media_qualifier[f]} {{\n{content}\n}}"
        parts.append(header + "\n" + content + "\n")
    return "\n".join(parts), ordered


def strip_unused_css_rules(content: str, unused_selectors: list) -> str:
    """Removes only rules with status=unused (never dynamic-suspect). Simple line-based
    selector { ... } heuristic."""
    if not unused_selectors:
        return content
    for sel in unused_selectors:
        pattern = re.compile(
            re.escape(sel) + r"\s*\{[^}]*\}\s*", re.MULTILINE
        )
        content = pattern.sub(f"/* removed by --strip-unused: {sel} */\n", content, count=1)
    return content


def detect_js_order_conflicts(html_files: list, js_order_by_page: dict) -> list:
    conflicts = []
    seen = set()
    for a_idx, page_a in enumerate(html_files):
        order_a = js_order_by_page.get(page_a, [])
        for i in range(len(order_a)):
            for j in range(i + 1, len(order_a)):
                x, y = order_a[i], order_a[j]
                for page_b in html_files[a_idx + 1:]:
                    order_b = js_order_by_page.get(page_b, [])
                    if x in order_b and y in order_b:
                        if order_b.index(y) < order_b.index(x):
                            key = (tuple(sorted([x, y])), page_a, page_b)
                            if key not in seen:
                                seen.add(key)
                                conflicts.append({
                                    "files": [x, y], "page_a": page_a, "order_a": [x, y],
                                    "page_b": page_b, "order_b": [y, x],
                                })
    return conflicts


def build_merged_js(files, classification, graph, js_conflicts, html_files, first_seen,
                      comment_lang, usage_map, strip_unused, js_order_by_page, on_order_conflict) -> tuple:
    ordered = group_and_order("js", files, classification, graph, html_files, first_seen)
    conflicts_by_file = build_conflicts_by_file(js_conflicts)
    order_conflicts = detect_js_order_conflicts(html_files, js_order_by_page)

    unused_by_file = {}
    if usage_map:
        for name, info in usage_map.get("jsSymbols", {}).items():
            if info["status"] == "unused":
                for d in info["definedIn"]:
                    unused_by_file.setdefault(d["file"], []).append(name)

    toc = ["/* ============================================================",
           "   TABLE OF CONTENTS" if comment_lang == "en" else "   ОГЛАВЛЕНИЕ",
           "   ============================================================"]
    for f in ordered:
        c = classification[f]
        used = f" | used on: {', '.join(c.used_by_pages)}" if c.used_by_pages else ""
        toc.append(f"   - {f}  [{c.label}]{used}")
    if order_conflicts:
        toc.append("   !! ORDER CONFLICTS DETECTED — see the banner below and build-report !!")
    toc.append("   ============================================================ */")

    parts = ["\n".join(toc)]

    if order_conflicts:
        banner = ["/* ############################################################",
                   "   WARNING: a contradictory JS include order was detected",
                   "   across pages — auto-sorting cannot satisfy both."]
        for oc in order_conflicts:
            banner.append(f"   - {oc['files'][0]} vs {oc['files'][1]}:")
            banner.append(f"       {oc['page_a']}: {' -> '.join(oc['order_a'])}")
            banner.append(f"       {oc['page_b']}: {' -> '.join(oc['order_b'])}")
        banner.append("   The order below is best-effort (topological + first-seen).")
        banner.append("   ############################################################ */")
        parts.append("\n".join(banner))
        if on_order_conflict == "fail":
            raise BuildAbortedError("order-conflict with --on-order-conflict=fail")

    for f in ordered:
        rec = files[f]
        deps = sorted(d for d in graph.edges.get(f, ()) if d in files and files[d].file_type == "js")
        unused_note = None
        if f in unused_by_file:
            names = ", ".join(unused_by_file[f])
            tag = "⚠ POSSIBLY UNUSED (per analysis)" if comment_lang == "en" else "⚠ ВОЗМОЖНО НЕ ИСПОЛЬЗУЕТСЯ (по данным анализа)"
            unused_note = f"{tag}: {names}"
        header = make_section_header(f, rec, classification[f], deps, conflicts_by_file.get(f, []), comment_lang, unused_note)
        content = read_text_safe(rec.abs_path).rstrip()
        parts.append(header.replace("/* ", "/* ").replace(" */", " */") + "\n" + content + "\n")
    return "\n".join(parts), ordered, order_conflicts


class BuildAbortedError(Exception):
    pass


class StartguiExit(Exception):
    """Raised to cleanly exit startgui (Ctrl+C, EOF, explicit item 0)."""
    pass


# ============================================================
# USAGE_MAP — extended mode (script-013)
# ============================================================

def collect_html_class_id_usage(files: dict, html_files: list) -> dict:
    """token ('.class' | '#id') -> [{file, line, context}]"""
    usage = {}
    for h in html_files:
        rec = files[h]
        text = read_text_safe(rec.abs_path)
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.find_all(True):
            for c in (tag.get("class") or []):
                usage.setdefault("." + c, []).append({"file": h, "line": tag.sourceline or 0, "context": "html-class"})
            id_ = tag.get("id")
            if id_:
                usage.setdefault("#" + id_, []).append({"file": h, "line": tag.sourceline or 0, "context": "html-id"})
    return usage


def build_usage_map(files: dict, css_rules_by_file: dict, js_symbols_by_file: dict, html_files: list) -> dict:
    html_usage = collect_html_class_id_usage(files, html_files)

    js_texts = {f: read_text_safe(r.abs_path) for f, r in files.items() if r.file_type == "js"}

    css_selectors_out = {}
    seen_simple = set()
    for file, rules in css_rules_by_file.items():
        for r in rules:
            if not re.match(r"^[.#][\w-]+$", r.selector):
                continue  # only track usage for simple single class/id selectors
            seen_simple.add(r.selector)
    for sel in sorted(seen_simple):
        defined_in = [{"file": f, "line": r.line} for f, rules in css_rules_by_file.items()
                      for r in rules if r.selector == sel]
        used_in = html_usage.get(sel, [])
        bare = sel[1:]
        dynamic_hits = []
        if not used_in:
            pat = re.compile(r"[\"'`][^\"'`]*\b" + re.escape(bare) + r"\b[^\"'`]*[\"'`]")
            for jf, text in js_texts.items():
                if pat.search(text):
                    dynamic_hits.append(jf)
        status = "used" if used_in else ("dynamic-suspect" if dynamic_hits else "unused")
        css_selectors_out[sel] = {"definedIn": defined_in, "usedIn": used_in,
                                    "dynamicSuspectIn": dynamic_hits, "status": status}

    js_symbols_out = {}
    for file, symbols in js_symbols_by_file.items():
        for sym in symbols:
            used_in = []
            for jf, text in js_texts.items():
                for lineno, line in enumerate(text.split("\n"), start=1):
                    if jf == file and lineno == sym.line:
                        continue
                    if re.search(r"\b" + re.escape(sym.name) + r"\b", line):
                        used_in.append({"file": jf, "line": lineno, "context": "reference"})
            status = "used" if used_in else "unused"
            key = sym.name if sym.name not in js_symbols_out else f"{sym.name}@{file}"
            js_symbols_out[key] = {"definedIn": [{"file": file, "line": sym.line}],
                                     "usedIn": used_in, "status": status}
    return {"cssSelectors": css_selectors_out, "jsSymbols": js_symbols_out}


# ============================================================
# CACHE (script-014)
# ============================================================

def load_cache(cache_path: Path):
    if not cache_path.exists():
        return None
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        if data.get("cacheVersion") != CACHE_VERSION:
            print("[info] cache version is stale — rebuilding from scratch", file=sys.stderr)
            return None
        return data
    except Exception as e:
        print(f"[warn] cache is corrupted, ignoring it: {e}", file=sys.stderr)
        return None


def files_changed_since_cache(files: dict, cache) -> set:
    if not cache:
        return set(files.keys())
    old_files = cache.get("files", {})
    changed = set()
    for rel, rec in files.items():
        old = old_files.get(rel)
        if not old or old.get("hash") != rec.hash:
            changed.add(rel)
    for rel in old_files:
        if rel not in files:
            changed.add(rel)  # a deleted file counts as a "change" too, invalidates dependent entries
    return changed


def get_css_rules_cached(rel, rec, cache, changed_files) -> list:
    if cache and rel not in changed_files:
        cached = cache.get("parsedCss", {}).get(rel)
        if cached is not None:
            return [CssRule(**r) for r in cached]
    return extract_css_rules(rec)


def get_js_symbols_cached(rel, rec, cache, changed_files) -> list:
    if cache and rel not in changed_files:
        cached = cache.get("parsedJs", {}).get(rel)
        if cached is not None:
            return [JsSymbol(**s) for s in cached]
    return extract_js_top_level_symbols(rec)


def save_cache(cache_path: Path, project_root: Path, files: dict,
                css_rules_by_file: dict, js_symbols_by_file: dict,
                usage_map: dict, conflicts: list):
    data = {
        "cacheVersion": CACHE_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "projectRoot": str(project_root),
        "files": {rel: {"hash": r.hash, "size": r.size, "mtime": r.mtime, "type": r.file_type}
                  for rel, r in files.items()},
        "parsedCss": {rel: [asdict(r) for r in rules] for rel, rules in css_rules_by_file.items()},
        "parsedJs": {rel: [asdict(s) for s in syms] for rel, syms in js_symbols_by_file.items()},
        "cssSelectors": usage_map.get("cssSelectors", {}) if usage_map else {},
        "jsSymbols": usage_map.get("jsSymbols", {}) if usage_map else {},
        "conflicts": [asdict(c) for c in conflicts],
    }
    cache_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ============================================================
# REPORT (script-012)
# ============================================================

def generate_report(files, html_files, classification, graph, css_conflicts, js_conflicts,
                      usage_map, order_conflicts, html_includes, mode, changed_files, cache_hit) -> dict:
    by_label = {"shared": [], "page-specific": [], "orphan": [], "vendor": []}
    for rel, c in classification.items():
        by_label[c.label].append(rel)

    external_assets = []
    for page, incs in html_includes.items():
        for inc in incs:
            if inc.is_external:
                external_assets.append({"page": page, "kind": inc.kind, "href": inc.href, "line": inc.line})

    pages_using = {rel: domino_impact(graph, rel, html_files)
                   for rel in classification if classification[rel].label == "shared"}
    domino_top = sorted(((rel, len(pages)) for rel, pages in pages_using.items()), key=lambda x: -x[1])[:5]

    report = {
        "meta": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "mode": mode,
            "totalFiles": len(files),
            "htmlPages": len(html_files),
            "cssFiles": sum(1 for r in files.values() if r.file_type == "css"),
            "jsFiles": sum(1 for r in files.values() if r.file_type == "js"),
        },
        "classification": {k: sorted(v) for k, v in by_label.items()},
        "conflicts": {
            "css": [asdict(c) for c in css_conflicts],
            "js": [asdict(c) for c in js_conflicts],
            "jsOrder": order_conflicts,
        },
        "externalAssets": external_assets,
        "dominoTop": [{"file": f, "affectedPages": n} for f, n in domino_top],
        "cache": {"reused": len(files) - len(changed_files) if cache_hit else 0,
                   "rescanned": len(changed_files) if cache_hit else len(files)},
    }
    if usage_map:
        unused_css = [k for k, v in usage_map["cssSelectors"].items() if v["status"] == "unused"]
        suspect_css = [k for k, v in usage_map["cssSelectors"].items() if v["status"] == "dynamic-suspect"]
        unused_js = [k for k, v in usage_map["jsSymbols"].items() if v["status"] == "unused"]
        report["usage"] = {"unusedCss": sorted(unused_css), "dynamicSuspectCss": sorted(suspect_css),
                             "unusedJs": sorted(unused_js)}
    return report


def render_report_markdown(report: dict) -> str:
    m = report["meta"]
    lines = [f"# assets-builder build report ({m['generatedAt']})", ""]
    lines.append(f"Mode: **{m['mode']}** · Files: {m['totalFiles']} "
                  f"(HTML: {m['htmlPages']}, CSS: {m['cssFiles']}, JS: {m['jsFiles']})")
    lines.append("")
    lines.append("## Classification")
    for label in ("shared", "page-specific", "orphan", "vendor"):
        items = report["classification"][label]
        lines.append(f"- **{label}** ({len(items)}): " + (", ".join(items) if items else "—"))
    lines.append("")
    lines.append("## CSS conflicts")
    if report["conflicts"]["css"]:
        for c in report["conflicts"]["css"]:
            lines.append(f"- `{c['name']}` [{c['severity']}] in {', '.join(c['files'])} — {c['detail']}")
    else:
        lines.append("None found.")
    lines.append("")
    lines.append("## JS conflicts")
    if report["conflicts"]["js"]:
        for c in report["conflicts"]["js"]:
            lines.append(f"- `{c['name']}` [{c['severity']}] in {', '.join(c['files'])} — {c['detail']}")
    else:
        lines.append("None found.")
    lines.append("")
    if report["conflicts"]["jsOrder"]:
        lines.append("## ⚠ JS include-order conflicts")
        for oc in report["conflicts"]["jsOrder"]:
            lines.append(f"- {oc['files'][0]} vs {oc['files'][1]}: "
                          f"{oc['page_a']} requires {oc['order_a']}, {oc['page_b']} requires {oc['order_b']}")
        lines.append("")
    lines.append("## External resources (not merged — keep in HTML manually)")
    if report["externalAssets"]:
        for e in report["externalAssets"]:
            lines.append(f"- {e['page']}: `{e['href']}` ({e['kind']})")
    else:
        lines.append("None found.")
    lines.append("")
    if report["dominoTop"]:
        lines.append("## Domino: most influential shared files")
        for d in report["dominoTop"]:
            lines.append(f"- `{d['file']}` — affects {d['affectedPages']} page(s).")
        lines.append("")
    if "usage" in report:
        u = report["usage"]
        lines.append("## Extended mode: usage")
        lines.append(f"- Unused CSS classes/IDs ({len(u['unusedCss'])}): " + (", ".join(u["unusedCss"]) or "—"))
        lines.append(f"- Possibly dynamic CSS ({len(u['dynamicSuspectCss'])}): " + (", ".join(u["dynamicSuspectCss"]) or "—"))
        lines.append(f"- Unused JS functions/variables ({len(u['unusedJs'])}): " + (", ".join(u["unusedJs"]) or "—"))
        lines.append("")
    lines.append("## Cache")
    lines.append(f"- Reused from cache: {report['cache']['reused']}, rescanned: {report['cache']['rescanned']}")
    return "\n".join(lines)


# ============================================================
# Shared analysis pipeline (used by both scan and build)
# ============================================================

def run_analysis(project_root: Path, exclude_patterns: list, vendor_patterns: list,
                   mode: str, cache_path: Path | None, use_cache: bool):
    full_exclude = list(dict.fromkeys(DEFAULT_EXCLUDE + list(exclude_patterns)))
    files = discover_files(project_root, full_exclude)
    html_files = sorted(rel for rel, r in files.items() if r.file_type == "html")
    css_files = sorted(rel for rel, r in files.items() if r.file_type == "css")
    js_files = sorted(rel for rel, r in files.items() if r.file_type == "js")

    html_includes = {h: parse_html_file(h, files[h], project_root) for h in html_files}
    css_imports = {c: parse_css_imports(c, files[c], project_root) for c in css_files}
    js_module_deps = {j: parse_js_module_deps(files[j]) for j in js_files}
    module_dep_files = sorted({j for j, deps in js_module_deps.items() if deps})

    graph = build_dependency_graph(files, html_includes, css_imports, project_root)
    cyclic = graph.detect_cyclic_nodes()

    classification = classify_files(files, html_files, graph, vendor_patterns)

    cache = load_cache(cache_path) if (use_cache and cache_path) else None
    changed_files = files_changed_since_cache(files, cache) if use_cache else set(files.keys())

    css_rules_by_file = {c: get_css_rules_cached(c, files[c], cache, changed_files) for c in css_files}
    js_symbols_by_file = {j: get_js_symbols_cached(j, files[j], cache, changed_files) for j in js_files}

    css_conflicts = detect_css_conflicts(css_rules_by_file)
    js_conflicts = detect_js_conflicts(js_symbols_by_file)

    usage_map = None
    if mode == "extended":
        usage_map = build_usage_map(files, css_rules_by_file, js_symbols_by_file, html_files)

    js_order_by_page = {}
    for page in html_files:
        js_order_by_page[page] = [inc.resolved_rel for inc in html_includes[page]
                                    if inc.kind == "js-src" and not inc.is_external and inc.resolved_rel]

    return dict(
        files=files, html_files=html_files, css_files=css_files, js_files=js_files,
        html_includes=html_includes, css_imports=css_imports, js_module_deps=js_module_deps,
        module_dep_files=module_dep_files, graph=graph, cyclic=cyclic, classification=classification,
        cache=cache, changed_files=changed_files, css_rules_by_file=css_rules_by_file,
        js_symbols_by_file=js_symbols_by_file, css_conflicts=css_conflicts, js_conflicts=js_conflicts,
        usage_map=usage_map, js_order_by_page=js_order_by_page,
    )


# ============================================================
# CLI (script-002 skeleton + script-015 full wiring)
# ============================================================

def add_common_args(p):
    p.add_argument("--project", required=True, help="project root")
    p.add_argument("--exclude", default="", help="comma-separated exclude patterns")
    p.add_argument("--vendor", default="", help="comma-separated explicit vendor patterns")
    p.add_argument("--cache", default=".assets-builder-cache.json")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--mode", choices=["basic", "extended"], default="basic")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--verbose", action="store_true")


# ============================================================
# PROMPT_HELPERS (ui-001) — a text menu, NOT a graphical interface.
# Stdlib input()/print() only: no new dependencies, and more importantly,
# input()-based code is testable by piping into stdin (see TZ §3),
# unlike curses.
# ============================================================

def _read_line(prompt: str) -> str:
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print()
        raise StartguiExit("interrupted by user (Ctrl+C)")
    except EOFError:
        print()
        raise StartguiExit("end of input (EOF)")


def menu_prompt(title, options, default=None) -> str:
    """Stacked (one-per-line) choice. options: list of (key, label).
    Used for the main menu and the help topic list — where there are
    many options or the labels are long."""
    valid_keys = {k for k, _ in options}
    while True:
        if title:
            print(title)
        for k, label in options:
            print(f"  {k}) {label}")
        suffix = f" [{default}]" if default is not None else ""
        raw = _read_line(f"Choose an option{suffix}: ").strip()
        if not raw and default is not None:
            return default
        if raw in valid_keys:
            return raw
        print(f"[!] Invalid choice: {raw!r}. Valid options: {', '.join(sorted(valid_keys))}")


def choice_prompt(label: str, options, default: str) -> str:
    """Compact single-line choice like 'Mode:  1) basic  2) extended   [1]: '.
    Used inside sub-flows for short enum-style questions."""
    valid_keys = {k for k, _ in options}
    opts_str = "  ".join(f"{k}) {lbl}" for k, lbl in options)
    while True:
        raw = _read_line(f"{label}:  {opts_str}   [{default}]: ").strip()
        if not raw:
            return default
        if raw in valid_keys:
            return raw
        print(f"[!] Invalid choice: {raw!r}. Valid options: {', '.join(sorted(valid_keys))}")


def text_prompt(label: str, default=None, validator=None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = _read_line(f"{label}{suffix}: ").strip()
        value = raw if raw else (default or "")
        if not value:
            print("[!] Value cannot be empty.")
            continue
        if validator:
            ok, err = validator(value)
            if not ok:
                print(f"[!] {err}")
                continue
        return value


def confirm_prompt(label: str, default: bool = True) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        raw = _read_line(f"{label} {hint}: ").strip().lower()
        if not raw:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("[!] Please answer y/n (or press Enter for the default).")


def _pause():
    _read_line("\nPress Enter to return to the menu...")


def _ask_project_path(current) -> str:
    def validate_dir(value):
        p = Path(value).expanduser()
        if not p.exists():
            return False, f"path does not exist: {value}"
        if not p.is_dir():
            return False, f"not a directory: {value}"
        return True, None
    raw = text_prompt("Project path", default=current, validator=validate_dir)
    return str(Path(raw).expanduser().resolve())


# ============================================================
# STARTGUI — main loop (ui-002) and sub-flows (ui-004..007).
# Each sub-flow only gathers parameters and calls the already
# existing cmd_scan/cmd_build/cmd_impact/cmd_clean_cache — without
# a single change inside them (see TZ §6, technical constraints).
# ============================================================

MAIN_MENU_OPTIONS = [
    ("1", "Scan project (scan)          — analysis without writing files"),
    ("2", "Build project (build)        — write style.css/scripts.js"),
    ("3", "File impact (impact)         — what a file change would affect"),
    ("4", "Clear cache (clean-cache)"),
    ("5", "Help"),
    ("6", "Change project path"),
    ("0", "Exit"),
]


def cmd_startgui(args) -> int:
    project = getattr(args, "project", None)
    if project:
        project = str(Path(project).expanduser().resolve())
    try:
        while True:
            print()
            print("=" * 64)
            print("  assets-builder — interactive mode")
            print("=" * 64)
            print(f"  Current project: {project if project else 'not set'}")
            print()
            choice = menu_prompt(None, MAIN_MENU_OPTIONS, default=None)
            print("=" * 64)

            if choice == "0":
                print("Goodbye.")
                return 0
            if choice == "5":
                _startgui_help_flow()
                continue
            if choice == "6":
                project = _ask_project_path(project)
                continue
            if choice in ("1", "2", "3", "4") and not project:
                print("[!] You need to set a project path first.")
                project = _ask_project_path(project)

            if choice == "1":
                _startgui_scan_flow(project)
            elif choice == "2":
                _startgui_build_flow(project)
            elif choice == "3":
                _startgui_impact_flow(project)
            elif choice == "4":
                _startgui_cleancache_flow(project)
    except StartguiExit as e:
        print(f"\nExiting: {e}")
        return 0


def _startgui_scan_flow(project: str):
    print("\n--- Scan project ---")
    mode_key = choice_prompt("Mode", [("1", "basic (faster)"), ("2", "extended (+ usage check)")], default="1")
    mode = "basic" if mode_key == "1" else "extended"
    save_key = choice_prompt("Save the report to a file?", [("1", "No, screen only"), ("2", "Yes (I'll give a path)")], default="1")
    report_path = report_json_path = None
    if save_key == "2":
        report_path = text_prompt("Path to the markdown report", default="scan-report.md")
        report_json_path = text_prompt("Path to the JSON report", default="scan-report.json")

    ns = argparse.Namespace(
        project=project, exclude="", vendor="", cache=".assets-builder-cache.json",
        no_cache=False, mode=mode, quiet=False, verbose=False,
        report=report_path, report_json=report_json_path,
    )
    try:
        code = cmd_scan(ns)
        print(f"\n(scan finished, exit code: {code})")
    except StartguiExit:
        raise
    except Exception as e:
        print(f"[error] {e}")
    _pause()


def _startgui_build_flow(project: str):
    print("\n--- Build project ---")
    mode_key = choice_prompt("Mode", [("1", "basic"), ("2", "extended")], default="1")
    mode = "basic" if mode_key == "1" else "extended"
    out_css = text_prompt("Path for style.css", default="dist/style.css")
    out_js = text_prompt("Path for scripts.js", default="dist/scripts.js")
    lang_key = choice_prompt("Comment language", [("1", "en"), ("2", "ru")], default="1")
    comment_lang = "en" if lang_key == "1" else "ru"
    conflict_key = choice_prompt("On a critical conflict",
                                   [("1", "build with a note (warn)"), ("2", "abort (fail)")], default="1")
    on_conflict = "warn" if conflict_key == "1" else "fail"
    order_key = choice_prompt("On a JS order conflict", [("1", "warn"), ("2", "fail")], default="1")
    on_order_conflict = "warn" if order_key == "1" else "fail"
    strip_unused = False
    if mode == "extended":
        strip_key = choice_prompt("Remove unused code? (--strip-unused)",
                                    [("1", "No"), ("2", "Yes")], default="1")
        strip_unused = (strip_key == "2")

    ns = argparse.Namespace(
        project=project, exclude="", vendor="", cache=".assets-builder-cache.json",
        no_cache=False, mode=mode, quiet=False, verbose=False,
        out_css=out_css, out_js=out_js,
        report="dist/build-report.md", report_json="dist/build-report.json",
        on_conflict=on_conflict, on_order_conflict=on_order_conflict,
        strip_unused=strip_unused, comment_lang=comment_lang,
    )
    try:
        code = cmd_build(ns)
        print(f"\n(build finished, exit code: {code})")
    except StartguiExit:
        raise
    except Exception as e:
        print(f"[error] {e}")
    _pause()


def _startgui_impact_flow(project: str):
    print("\n--- File impact (impact) ---")

    def validate_nonempty(v):
        return (True, None) if v.strip() else (False, "path cannot be empty")

    file_rel = text_prompt("File path relative to the project root", default=None, validator=validate_nonempty)
    ns = argparse.Namespace(project=project, exclude="", vendor="", file=file_rel)
    try:
        code = cmd_impact(ns)
        print(f"\n(impact finished, exit code: {code})")
    except StartguiExit:
        raise
    except Exception as e:
        print(f"[error] {e}")
    _pause()


def _startgui_cleancache_flow(project: str):
    print("\n--- Clear cache ---")
    if confirm_prompt("Delete .assets-builder-cache.json?", default=True):
        ns = argparse.Namespace(project=project, cache=".assets-builder-cache.json")
        try:
            code = cmd_clean_cache(ns)
            print(f"\n(clean-cache finished, exit code: {code})")
        except StartguiExit:
            raise
        except Exception as e:
            print(f"[error] {e}")
    else:
        print("Cancelled.")
    _pause()


# ============================================================
# HELP (ui-008..010) — implemented LAST per the task's explicit
# requirement: its content must accurately describe startgui, which
# by this point is already fully specified above.
# ============================================================

HELP_TOPICS = {
    "overview": """assets-builder — merges and documents a front-end project's CSS/JS.

Problem: stylesheet and script files are scattered across nested folders,
some shared, some specific to a single page. To sell a template you need
one style.css and one scripts.js — while preserving where each block came
from and not losing track of conflicts between files.

Commands: scan, build, impact, clean-cache, startgui, help.
scan/build/impact/clean-cache — regular CLI (flags). startgui — the same
thing through a text menu where you type a number, no need to remember flags.

More detail: help <topic>, topics: scan, build, impact, clean-cache, startgui,
exit-codes, defaults.""",

    "scan": """scan — analyzes the project WITHOUT writing style.css/scripts.js (safe dry-run).

  assets-builder.py scan --project <path> [--mode basic|extended]
                          [--report PATH] [--report-json PATH]
                          [--exclude a,b] [--vendor a,b]
                          [--cache PATH] [--no-cache]

Exit code: 0 — no high-severity conflicts found; 1 — at least one CSS or
JS conflict with severity=high was found (this is a signal, not an error).""",

    "build": """build — full build: style.css + scripts.js + reports (+ cache, unless --no-cache).

  assets-builder.py build --project <path>
                           [--out-css dist/style.css] [--out-js dist/scripts.js]
                           [--mode basic|extended] [--comment-lang en|ru]
                           [--on-conflict warn|fail] [--on-order-conflict warn|fail]
                           [--strip-unused] [--report PATH] [--report-json PATH]

Exit code: 0 — success; 2 — --on-conflict fail and a high-severity conflict
was found (files were not written); 3 — --on-order-conflict fail and a
JS order conflict was found.

--strip-unused only works in --mode extended and never removes code with
status=dynamic-suspect — only status=unused.""",

    "impact": """impact — which HTML pages a single file's change would affect (domino analysis).

  assets-builder.py impact --project <path> <file>

<file> — path relative to --project, exactly as it appears in reports
(e.g. assets/css/base.css). Exit code 2 if the file isn't found.""",

    "clean-cache": """clean-cache — deletes the cache file (.assets-builder-cache.json by default).

  assets-builder.py clean-cache --project <path> [--cache PATH]

Always exits with code 0, even if there was no cache.""",

    "startgui": """startgui — an interactive TEXT menu (not a graphical interface: no windows,
no mouse, just typing a number and pressing Enter).

  assets-builder.py startgui [--project <path>]

Asks the same questions that scan/build/impact/clean-cache have flags for,
and calls exactly the same code — the result is identical to a direct call
with the same parameters. The project path doesn't have to be given at
startup — it's asked for the first time it's needed and remembered for
the rest of the session.""",

    "exit-codes": """Exit codes:
  0 — success / (scan) no high-severity conflicts / (clean-cache) always
  1 — (scan) a high-severity conflict was found (CSS or JS) — not an error, a signal
  2 — (build) --on-conflict fail and a high-severity conflict was found — files not written
  3 — (build) --on-order-conflict fail and a JS order conflict was found
  2 — (impact) the given file was not found in the project""",

    "defaults": """Important defaults:

DEFAULT_EXCLUDE — always excluded from analysis, regardless of --exclude:
  dist/**, .git/**, node_modules/**
  (without this, a repeat build would pick up its own previous output
  as source files)

The cache (.assets-builder-cache.json) is reused by file content hash, not
by modification time: files that haven't changed aren't re-parsed.

--strip-unused only removes status=unused; status=dynamic-suspect (looks
like it's added via JS classList.add and similar) is never removed — that
is a guarantee at the code level, not just in the documentation.

--comment-lang defaults to en, not ru — templates are usually sold
internationally.

There is no --js-parser flag in the CLI: only the heuristic (regex-based)
JS parser is implemented, there is no "ast" mode.""",
}

HELP_TOPIC_ORDER = ["overview", "scan", "build", "impact", "clean-cache", "startgui", "exit-codes", "defaults"]


def render_help(topic) -> str:
    if not topic:
        return HELP_TOPICS["overview"] + "\n\nAvailable topics: " + ", ".join(HELP_TOPIC_ORDER)
    key = str(topic).strip().lower()
    if key not in HELP_TOPICS:
        return f"[!] Unknown topic: {topic!r}. Available topics: {', '.join(HELP_TOPIC_ORDER)}"
    return HELP_TOPICS[key]


def cmd_help(args) -> int:
    print(render_help(getattr(args, "topic", None)))
    return 0


def _startgui_help_flow():
    while True:
        print("\n--- Help ---")
        options = [(str(i + 1), t) for i, t in enumerate(HELP_TOPIC_ORDER)]
        options.append(("0", "Back to main menu"))
        choice = menu_prompt(None, options, default=None)
        if choice == "0":
            return
        topic = HELP_TOPIC_ORDER[int(choice) - 1]
        print()
        print(render_help(topic))
        _pause()


def build_arg_parser():
    parser = argparse.ArgumentParser(prog="assets-builder.py",
                                       description="Merge and document a front-end project's CSS/JS")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="analysis + report, without writing CSS/JS (safe dry-run)")
    add_common_args(p_scan)
    p_scan.add_argument("--report", default=None)
    p_scan.add_argument("--report-json", default=None)

    p_build = sub.add_parser("build", help="full pipeline, writes the output files")
    add_common_args(p_build)
    p_build.add_argument("--out-css", default="dist/style.css")
    p_build.add_argument("--out-js", default="dist/scripts.js")
    p_build.add_argument("--report", default="dist/build-report.md")
    p_build.add_argument("--report-json", default="dist/build-report.json")
    p_build.add_argument("--on-conflict", choices=["warn", "fail"], default="warn")
    p_build.add_argument("--on-order-conflict", choices=["warn", "fail"], default="warn")
    p_build.add_argument("--strip-unused", action="store_true")
    p_build.add_argument("--comment-lang", choices=["ru", "en"], default="en")

    p_impact = sub.add_parser("impact", help="which pages a file's change would affect (domino analysis)")
    add_common_args(p_impact)
    p_impact.add_argument("file", help="file path relative to the project root")

    p_clean = sub.add_parser("clean-cache", help="delete the cache file")
    p_clean.add_argument("--project", required=True)
    p_clean.add_argument("--cache", default=".assets-builder-cache.json")

    p_startgui = sub.add_parser("startgui", help="interactive text menu (not a graphical interface)")
    p_startgui.add_argument("--project", default=None,
                              help="project path (optional — can be given later, inside the menu)")

    p_help = sub.add_parser("help", help="detailed help by topic (complements -h/--help)")
    p_help.add_argument("topic", nargs="?", default=None,
                          help="overview|scan|build|impact|clean-cache|startgui|exit-codes|defaults")

    return parser


def split_csv(s: str) -> list:
    return [x.strip() for x in s.split(",") if x.strip()]


def cmd_scan(args) -> int:
    project_root = Path(args.project).resolve()
    result = run_analysis(project_root, split_csv(args.exclude), split_csv(args.vendor),
                            args.mode, project_root / args.cache, not args.no_cache)
    high_css = [c for c in result["css_conflicts"] if c.severity == "high"]
    high_js = [c for c in result["js_conflicts"] if c.severity == "high"]

    report = generate_report(result["files"], result["html_files"], result["classification"],
                               result["graph"], result["css_conflicts"], result["js_conflicts"],
                               result["usage_map"], [], result["html_includes"], args.mode,
                               result["changed_files"], bool(result["cache"]))

    if not args.quiet:
        print(f"Files found: {len(result['files'])} "
              f"(HTML {len(result['html_files'])}, CSS {len(result['css_files'])}, JS {len(result['js_files'])})")
        for label in ("shared", "page-specific", "orphan", "vendor"):
            print(f"  {label}: {len(report['classification'][label])}")
        print(f"CSS conflicts: {len(result['css_conflicts'])} (high: {len(high_css)})")
        print(f"JS conflicts: {len(result['js_conflicts'])} (high: {len(high_js)})")
        if result["cyclic"]:
            print(f"[warn] cycles detected in the dependency graph: {result['cyclic']}")
        if result["module_dep_files"]:
            print(f"[info] files with ESM/CJS syntax (need manual review): {result['module_dep_files']}")

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(render_report_markdown(report), encoding="utf-8")
    if args.report_json:
        Path(args.report_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report_json).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    return 1 if (high_css or high_js) else 0


def extra_output_excludes(project_root: Path, *rel_or_abs_paths) -> list:
    """If an output file lives inside project_root but outside DEFAULT_EXCLUDE (e.g. not in
    dist/), exclude its exact relative path explicitly — so discovery doesn't pick up its own output."""
    extra = []
    for p in rel_or_abs_paths:
        pth = Path(p)
        abs_pth = pth if pth.is_absolute() else (project_root / pth)
        try:
            rel = abs_pth.resolve().relative_to(project_root.resolve())
            extra.append(rel.as_posix())
        except ValueError:
            pass  # outside project_root — discovery wouldn't find it anyway
    return extra


def cmd_build(args) -> int:
    project_root = Path(args.project).resolve()
    cache_path = project_root / args.cache
    extra_excl = extra_output_excludes(project_root, args.out_css, args.out_js)
    result = run_analysis(project_root, split_csv(args.exclude) + extra_excl, split_csv(args.vendor),
                            args.mode, cache_path, not args.no_cache)

    high_conflicts = [c for c in result["css_conflicts"] + result["js_conflicts"] if c.severity == "high"]
    if high_conflicts and args.on_conflict == "fail":
        print(f"[error] {len(high_conflicts)} high-severity conflict(s), --on-conflict=fail — build aborted",
              file=sys.stderr)
        return 2

    first_seen = compute_first_seen_order(result["html_files"], result["html_includes"])

    css_out, css_order = build_merged_css(
        result["files"], result["classification"], result["graph"], result["css_conflicts"],
        result["html_files"], first_seen, result["css_imports"], args.comment_lang,
        result["usage_map"], args.strip_unused,
    )
    try:
        js_out, js_order, order_conflicts = build_merged_js(
            result["files"], result["classification"], result["graph"], result["js_conflicts"],
            result["html_files"], first_seen, args.comment_lang, result["usage_map"],
            args.strip_unused, result["js_order_by_page"], args.on_order_conflict,
        )
    except BuildAbortedError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 3

    out_css_path = project_root / args.out_css if not Path(args.out_css).is_absolute() else Path(args.out_css)
    out_js_path = project_root / args.out_js if not Path(args.out_js).is_absolute() else Path(args.out_js)
    out_css_path.parent.mkdir(parents=True, exist_ok=True)
    out_js_path.parent.mkdir(parents=True, exist_ok=True)
    out_css_path.write_text(css_out, encoding="utf-8")
    out_js_path.write_text(js_out, encoding="utf-8")

    report = generate_report(result["files"], result["html_files"], result["classification"],
                               result["graph"], result["css_conflicts"], result["js_conflicts"],
                               result["usage_map"], order_conflicts, result["html_includes"], args.mode,
                               result["changed_files"], bool(result["cache"]))
    report["output"] = {
        "css": str(out_css_path), "js": str(out_js_path),
        "cssSizeBytes": len(css_out.encode("utf-8")), "jsSizeBytes": len(js_out.encode("utf-8")),
        "originalCssBytes": sum(result["files"][f].size for f in result["css_files"]),
        "originalJsBytes": sum(result["files"][f].size for f in result["js_files"]),
    }

    report_md_path = project_root / args.report if not Path(args.report).is_absolute() else Path(args.report)
    report_json_path = project_root / args.report_json if not Path(args.report_json).is_absolute() else Path(args.report_json)
    report_md_path.parent.mkdir(parents=True, exist_ok=True)
    report_json_path.parent.mkdir(parents=True, exist_ok=True)
    report_md_path.write_text(render_report_markdown(report), encoding="utf-8")
    report_json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if not args.no_cache:
        save_cache(cache_path, project_root, result["files"], result["css_rules_by_file"],
                    result["js_symbols_by_file"], result["usage_map"], result["css_conflicts"] + result["js_conflicts"])

    if not args.quiet:
        print(f"OK: {out_css_path} ({len(css_out)} chars), {out_js_path} ({len(js_out)} chars)")
        print(f"Report: {report_md_path}")
        if order_conflicts:
            print(f"[warn] order conflict(s): {len(order_conflicts)} — see the report")

    return 0


def cmd_impact(args) -> int:
    project_root = Path(args.project).resolve()
    result = run_analysis(project_root, split_csv(args.exclude), split_csv(args.vendor),
                            "basic", None, False)
    target = args.file
    if target not in result["files"]:
        print(f"[error] file not found in the project: {target}", file=sys.stderr)
        return 2
    affected = domino_impact(result["graph"], target, result["html_files"])
    print(f"Changing {target} would affect {len(affected)} page(s):")
    for p in affected:
        print(f"  - {p}")
    return 0


def cmd_clean_cache(args) -> int:
    project_root = Path(args.project).resolve()
    cache_path = project_root / args.cache
    if cache_path.exists():
        cache_path.unlink()
        print(f"Deleted: {cache_path}")
    else:
        print("No cache found — nothing to delete")
    return 0


def main(argv=None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    handlers = {"scan": cmd_scan, "build": cmd_build, "impact": cmd_impact, "clean-cache": cmd_clean_cache,
                "startgui": cmd_startgui, "help": cmd_help}
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
