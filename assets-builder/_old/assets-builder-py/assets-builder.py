#!/usr/bin/env python3
"""
assets-builder.py

Сборка CSS/JS front-end проекта в два документированных дистрибутивных файла.
Реализация по TZ-assets-builder-script.md и PLAN-assets-builder-script.md.

Секции файла соответствуют категориям плана (script-001..016):
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

# Всегда исключаются из DISCOVERY, независимо от --exclude пользователя:
# без этого повторный запуск build подхватывает dist/style.css и dist/scripts.js
# из ПРЕДЫДУЩЕГО запуска как обычные исходники (self-contamination).
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
                print(f"[warn] пропущен нечитаемый файл {rel}: {e}", file=sys.stderr)
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
        raise RuntimeError("beautifulsoup4 не установлен: pip install beautifulsoup4 --break-system-packages")
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
        raise RuntimeError("tinycss2 не установлен: pip install tinycss2 --break-system-packages")
    text = read_text_safe(rec.abs_path)
    rules = []
    try:
        stylesheet = tinycss2.parse_stylesheet(text, skip_comments=True, skip_whitespace=True)
    except Exception as e:
        print(f"[warn] не удалось разобрать CSS {rec.rel_path}: {e}", file=sys.stderr)
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
            severity, detail = "low", "идентичные объявления во всех вхождениях (чистый дубль)"
        else:
            seen_props, overlapping_props = set(), set()
            for d in all_decls:
                overlapping_props |= (seen_props & set(d.keys()))
                seen_props |= set(d.keys())
            if not overlapping_props:
                severity, detail = "medium", "разные свойства — каскад скомбинирует без потерь"
            else:
                real_conflict = any(
                    len(set(d.get(p) for d in all_decls if p in d)) > 1
                    for p in overlapping_props
                )
                if real_conflict:
                    severity = "high"
                    detail = f"совпадающие свойства с разными значениями: {sorted(overlapping_props)}"
                else:
                    severity, detail = "low", "пересекающиеся свойства, но значения совпадают"
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
            severity, detail = "low", "идентичное тело (по фингерпринту первых строк) — чистый дубль"
        else:
            severity = "high"
            detail = "разное тело у одинакового имени — при конкатенации последнее определение молча победит"
        conflicts.append(Conflict("js-symbol", name, files_involved, severity, detail))
    return conflicts


# ============================================================
# Общая обвязка: топологический порядок для сборки (нужен MERGE_CSS/MERGE_JS)
# ============================================================

def compute_first_seen_order(html_files: list, includes_by_page: dict) -> dict:
    """Индекс "впервые встречен" для детерминированного tie-break при топосортировке."""
    order = {}
    counter = 0
    for page in html_files:
        for inc in includes_by_page.get(page, []):
            if inc.resolved_rel and inc.resolved_rel not in order:
                order[inc.resolved_rel] = counter
                counter += 1
    return order


def topological_order(files: list, graph: DependencyGraph, first_seen: dict) -> list:
    """Файлы, от которых зависят другие (через @import/import), идут раньше.
    При равенстве уровня — порядок первого появления в HTML, иначе алфавит."""
    file_set = set(files)
    precede = {f: set() for f in files}  # a -> {b, ...}: a должен стоять раньше b
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
        order.extend(sorted(remaining, key=sort_key))  # цикл — не роняем сборку, просто добавляем как есть
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
            tag = "⚠ UNUSED (по данным анализа)" if comment_lang == "en" else "⚠ ВОЗМОЖНО НЕ ИСПОЛЬЗУЕТСЯ (по данным анализа)"
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
    """Удаляет только правила с status=unused (никогда dynamic-suspect). Простая построчная эвристика по selector { ... }."""
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
        toc.append("   !! ORDER CONFLICTS DETECTED — см. ниже банер и build-report !!")
    toc.append("   ============================================================ */")

    parts = ["\n".join(toc)]

    if order_conflicts:
        banner = ["/* ############################################################",
                   "   ВНИМАНИЕ: обнаружен противоречивый порядок подключения JS",
                   "   между страницами — авто-сортировка не может угодить обеим."]
        for oc in order_conflicts:
            banner.append(f"   - {oc['files'][0]} vs {oc['files'][1]}:")
            banner.append(f"       {oc['page_a']}: {' -> '.join(oc['order_a'])}")
            banner.append(f"       {oc['page_b']}: {' -> '.join(oc['order_b'])}")
        banner.append("   Итоговый порядок ниже — best-effort (topological + first-seen).")
        banner.append("   ############################################################ */")
        parts.append("\n".join(banner))
        if on_order_conflict == "fail":
            raise BuildAbortedError("order-conflict с --on-order-conflict=fail")

    for f in ordered:
        rec = files[f]
        deps = sorted(d for d in graph.edges.get(f, ()) if d in files and files[d].file_type == "js")
        unused_note = None
        if f in unused_by_file:
            names = ", ".join(unused_by_file[f])
            tag = "⚠ UNUSED (по данным анализа)" if comment_lang == "en" else "⚠ ВОЗМОЖНО НЕ ИСПОЛЬЗУЕТСЯ (по данным анализа)"
            unused_note = f"{tag}: {names}"
        header = make_section_header(f, rec, classification[f], deps, conflicts_by_file.get(f, []), comment_lang, unused_note)
        content = read_text_safe(rec.abs_path).rstrip()
        parts.append(header.replace("/* ", "/* ").replace(" */", " */") + "\n" + content + "\n")
    return "\n".join(parts), ordered, order_conflicts


class BuildAbortedError(Exception):
    pass


# ============================================================
# USAGE_MAP — расширенный режим (script-013)
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
                continue  # трекаем usage только для простых одиночных class/id селекторов
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
            print("[info] версия кеша устарела — пересобираю с нуля", file=sys.stderr)
            return None
        return data
    except Exception as e:
        print(f"[warn] кеш повреждён, игнорирую: {e}", file=sys.stderr)
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
            changed.add(rel)  # файл удалён — тоже "изменение", инвалидирует зависимые записи
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
    lines = [f"# Отчёт сборки assets-builder ({m['generatedAt']})", ""]
    lines.append(f"Режим: **{m['mode']}** · Файлов: {m['totalFiles']} "
                  f"(HTML: {m['htmlPages']}, CSS: {m['cssFiles']}, JS: {m['jsFiles']})")
    lines.append("")
    lines.append("## Классификация")
    for label in ("shared", "page-specific", "orphan", "vendor"):
        items = report["classification"][label]
        lines.append(f"- **{label}** ({len(items)}): " + (", ".join(items) if items else "—"))
    lines.append("")
    lines.append("## Конфликты CSS")
    if report["conflicts"]["css"]:
        for c in report["conflicts"]["css"]:
            lines.append(f"- `{c['name']}` [{c['severity']}] в {', '.join(c['files'])} — {c['detail']}")
    else:
        lines.append("Не найдено.")
    lines.append("")
    lines.append("## Конфликты JS")
    if report["conflicts"]["js"]:
        for c in report["conflicts"]["js"]:
            lines.append(f"- `{c['name']}` [{c['severity']}] в {', '.join(c['files'])} — {c['detail']}")
    else:
        lines.append("Не найдено.")
    lines.append("")
    if report["conflicts"]["jsOrder"]:
        lines.append("## ⚠ Конфликты порядка подключения JS")
        for oc in report["conflicts"]["jsOrder"]:
            lines.append(f"- {oc['files'][0]} vs {oc['files'][1]}: "
                          f"{oc['page_a']} требует {oc['order_a']}, {oc['page_b']} требует {oc['order_b']}")
        lines.append("")
    lines.append("## Внешние ресурсы (не включены в сборку — оставить в HTML вручную)")
    if report["externalAssets"]:
        for e in report["externalAssets"]:
            lines.append(f"- {e['page']}: `{e['href']}` ({e['kind']})")
    else:
        lines.append("Не найдено.")
    lines.append("")
    if report["dominoTop"]:
        lines.append("## Домино: наиболее влиятельные общие файлы")
        for d in report["dominoTop"]:
            lines.append(f"- `{d['file']}` — затрагивает {d['affectedPages']} стр.")
        lines.append("")
    if "usage" in report:
        u = report["usage"]
        lines.append("## Расширенный режим: использование")
        lines.append(f"- Неиспользуемые CSS-классы/ID ({len(u['unusedCss'])}): " + (", ".join(u["unusedCss"]) or "—"))
        lines.append(f"- Возможно динамические CSS ({len(u['dynamicSuspectCss'])}): " + (", ".join(u["dynamicSuspectCss"]) or "—"))
        lines.append(f"- Неиспользуемые JS-функции/переменные ({len(u['unusedJs'])}): " + (", ".join(u["unusedJs"]) or "—"))
        lines.append("")
    lines.append("## Кеш")
    lines.append(f"- Переиспользовано из кеша: {report['cache']['reused']}, пересканировано: {report['cache']['rescanned']}")
    return "\n".join(lines)


# ============================================================
# Общий пайплайн анализа (используется и scan, и build)
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
# CLI (script-002 каркас + script-015 полное связывание)
# ============================================================

def add_common_args(p):
    p.add_argument("--project", required=True, help="корень проекта")
    p.add_argument("--exclude", default="", help="паттерны исключения через запятую")
    p.add_argument("--vendor", default="", help="явные vendor-паттерны через запятую")
    p.add_argument("--cache", default=".assets-builder-cache.json")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--mode", choices=["basic", "extended"], default="basic")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--verbose", action="store_true")


def build_arg_parser():
    parser = argparse.ArgumentParser(prog="assets-builder.py",
                                       description="Сборка и документирование CSS/JS front-end проекта")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="анализ + отчёт, без записи CSS/JS (безопасный dry-run)")
    add_common_args(p_scan)
    p_scan.add_argument("--report", default=None)
    p_scan.add_argument("--report-json", default=None)

    p_build = sub.add_parser("build", help="полный пайплайн с записью выходных файлов")
    add_common_args(p_build)
    p_build.add_argument("--out-css", default="dist/style.css")
    p_build.add_argument("--out-js", default="dist/scripts.js")
    p_build.add_argument("--report", default="dist/build-report.md")
    p_build.add_argument("--report-json", default="dist/build-report.json")
    p_build.add_argument("--on-conflict", choices=["warn", "fail"], default="warn")
    p_build.add_argument("--on-order-conflict", choices=["warn", "fail"], default="warn")
    p_build.add_argument("--strip-unused", action="store_true")
    p_build.add_argument("--comment-lang", choices=["ru", "en"], default="en")

    p_impact = sub.add_parser("impact", help="какие страницы затронет изменение файла (домино-анализ)")
    add_common_args(p_impact)
    p_impact.add_argument("file", help="относительный путь файла от корня проекта")

    p_clean = sub.add_parser("clean-cache", help="удалить файл кеша")
    p_clean.add_argument("--project", required=True)
    p_clean.add_argument("--cache", default=".assets-builder-cache.json")

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
        print(f"Найдено файлов: {len(result['files'])} "
              f"(HTML {len(result['html_files'])}, CSS {len(result['css_files'])}, JS {len(result['js_files'])})")
        for label in ("shared", "page-specific", "orphan", "vendor"):
            print(f"  {label}: {len(report['classification'][label])}")
        print(f"Конфликты CSS: {len(result['css_conflicts'])} (high: {len(high_css)})")
        print(f"Конфликты JS: {len(result['js_conflicts'])} (high: {len(high_js)})")
        if result["cyclic"]:
            print(f"[warn] обнаружены циклы в графе зависимостей: {result['cyclic']}")
        if result["module_dep_files"]:
            print(f"[info] файлы с ESM/CJS синтаксисом (требуют ручной проверки): {result['module_dep_files']}")

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(render_report_markdown(report), encoding="utf-8")
    if args.report_json:
        Path(args.report_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report_json).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    return 1 if (high_css or high_js) else 0


def extra_output_excludes(project_root: Path, *rel_or_abs_paths) -> list:
    """Если выходной файл лежит внутри project_root, но вне DEFAULT_EXCLUDE (напр. не в dist/),
    исключаем его точный относительный путь явно — чтобы discovery не подхватил свой же вывод."""
    extra = []
    for p in rel_or_abs_paths:
        pth = Path(p)
        abs_pth = pth if pth.is_absolute() else (project_root / pth)
        try:
            rel = abs_pth.resolve().relative_to(project_root.resolve())
            extra.append(rel.as_posix())
        except ValueError:
            pass  # вне project_root — и так не будет найден discovery
    return extra


def cmd_build(args) -> int:
    project_root = Path(args.project).resolve()
    cache_path = project_root / args.cache
    extra_excl = extra_output_excludes(project_root, args.out_css, args.out_js)
    result = run_analysis(project_root, split_csv(args.exclude) + extra_excl, split_csv(args.vendor),
                            args.mode, cache_path, not args.no_cache)

    high_conflicts = [c for c in result["css_conflicts"] + result["js_conflicts"] if c.severity == "high"]
    if high_conflicts and args.on_conflict == "fail":
        print(f"[error] {len(high_conflicts)} high-severity конфликт(ов), --on-conflict=fail — сборка прервана",
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
        print(f"Отчёт: {report_md_path}")
        if order_conflicts:
            print(f"[warn] order-conflict(ов): {len(order_conflicts)} — см. отчёт")

    return 0


def cmd_impact(args) -> int:
    project_root = Path(args.project).resolve()
    result = run_analysis(project_root, split_csv(args.exclude), split_csv(args.vendor),
                            "basic", None, False)
    target = args.file
    if target not in result["files"]:
        print(f"[error] файл не найден в проекте: {target}", file=sys.stderr)
        return 2
    affected = domino_impact(result["graph"], target, result["html_files"])
    print(f"Изменение {target} затронет {len(affected)} страниц(ы):")
    for p in affected:
        print(f"  - {p}")
    return 0


def cmd_clean_cache(args) -> int:
    project_root = Path(args.project).resolve()
    cache_path = project_root / args.cache
    if cache_path.exists():
        cache_path.unlink()
        print(f"Удалён: {cache_path}")
    else:
        print("Кеш не найден — нечего удалять")
    return 0


def main(argv=None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    handlers = {"scan": cmd_scan, "build": cmd_build, "impact": cmd_impact, "clean-cache": cmd_clean_cache}
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
