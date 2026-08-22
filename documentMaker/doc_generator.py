#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_generator.py
=================

Генератор технической документации для фронтенд-проектов (HTML/CSS/JS).

Обходит указанный каталог проекта, строит дерево файлов, разбирает каждый
HTML/CSS/JS файл с учётом особенностей соответствующего языка, находит
связи между файлами (структурные и "смысловые" — через id/class/селекторы)
и собирает всё это в один самодостаточный HTML-файл документации
(вся CSS и JS документации встроены внутрь, внешние сети не требуются).

Используется только стандартная библиотека Python — устанавливать
дополнительные пакеты не нужно.

Запуск:
    python3 doc_generator.py /path/to/project -o docs.html

См. README.md рядом с этим файлом для полного описания опций.
"""

from __future__ import annotations

import argparse
import html as html_stdlib
import json
import os
import re
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Optional, Iterable
from urllib.parse import urlsplit

# --------------------------------------------------------------------------
# Константы конфигурации
# --------------------------------------------------------------------------

VERSION = "1.0.0"

#: Каталоги, которые никогда не анализируются (типичный технический мусор)
DEFAULT_IGNORE_DIRS = {
    "node_modules", ".git", ".svn", ".hg", "dist", "build", "out",
    ".next", ".nuxt", ".cache", "coverage", "__pycache__", ".idea",
    ".vscode", "vendor", ".parcel-cache", ".turbo", ".vercel",
}

#: Расширения файлов, которые разбираются как "исходники" трёх языков
HTML_EXTS = {".html", ".htm"}
CSS_EXTS = {".css"}
JS_EXTS = {".js", ".mjs", ".cjs", ".jsx"}

#: Расширения, которые попадают в карту каталогов, но не разбираются глубоко
KNOWN_OTHER_EXTS = {
    ".json", ".md", ".txt", ".svg", ".png", ".jpg", ".jpeg", ".gif",
    ".webp", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".map", ".yml",
    ".yaml", ".xml", ".scss", ".sass", ".less", ".ts", ".tsx", ".vue",
}

#: Порог "минифицированности" файла: если средняя длина строки больше
#: этого значения, файл считается минифицированным и не разбирается
#: детально (иначе документация утонет в нечитаемых портянках).
MINIFIED_AVG_LINE_LEN = 300
MINIFIED_MAX_FILE_FOR_FULL_DUMP = 20000  # символов, после которых код обрезаем в выводе

JS_KEYWORDS = {
    "break", "case", "catch", "class", "const", "continue", "debugger",
    "default", "delete", "do", "else", "export", "extends", "finally",
    "for", "function", "if", "import", "in", "instanceof", "let", "new",
    "return", "super", "switch", "this", "throw", "try", "typeof", "var",
    "void", "while", "with", "yield", "async", "await", "of", "static",
    "get", "set", "null", "true", "false", "undefined", "from", "as",
}

# Ключевые слова, которые синтаксически похожи на "имя_функции(...) {"
# но методами/функциями не являются — чтобы не принять их за объявления.
JS_CONTROL_KEYWORDS = {
    "if", "for", "while", "switch", "catch", "function", "return",
    "with", "do",
}


# --------------------------------------------------------------------------
# Общие утилиты
# --------------------------------------------------------------------------

def read_text_safe(path: Path) -> str:
    """Читает текстовый файл, устойчиво к проблемам с кодировкой."""
    for enc in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return path.read_bytes().decode("utf-8", errors="replace")


def human_size(num: int) -> str:
    """Форматирует размер в байтах в человекочитаемый вид (КБ, МБ...)."""
    size = float(num)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if size < 1024 or unit == "ГБ":
            return f"{size:.0f} {unit}" if unit == "Б" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} ГБ"


def slugify(rel_path: str) -> str:
    """Превращает относительный путь файла в безопасный id для HTML-якоря."""
    return "f-" + re.sub(r"[^a-zA-Z0-9_-]+", "-", rel_path).strip("-").lower()


def esc(text: Optional[str]) -> str:
    """HTML-экранирование с защитой от None."""
    if text is None:
        return ""
    return html_stdlib.escape(str(text), quote=True)


def is_probably_minified(text: str) -> bool:
    """Эвристика: файл в одну "простыню" строк — скорее всего минифицирован."""
    lines = text.splitlines() or [""]
    longest = max((len(ln) for ln in lines), default=0)
    avg = sum(len(ln) for ln in lines) / max(len(lines), 1)
    return longest > 2000 or (avg > MINIFIED_AVG_LINE_LEN and len(lines) < 10)


def count_loc(text: str) -> int:
    """Количество непустых строк (используется как приближение LOC)."""
    return sum(1 for ln in text.splitlines() if ln.strip())


def resolve_relative(base_file_rel: str, ref: str) -> Optional[str]:
    """
    Пытается разрешить относительную ссылку (href/src/@import/import) из
    HTML/CSS/JS файла в путь проекта, относительный к его корню.
    Возвращает None, если ссылка внешняя (http(s)://, protocol-relative,
    data:, bare-specifier без ./ или ../ для JS и т.п.) — такие ссылки
    считаются "внешними зависимостями", а не внутренними файлами проекта.
    """
    if not ref:
        return None
    ref = ref.strip().strip("'\"")
    if ref.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
        return None
    parsed = urlsplit(ref)
    if parsed.scheme or ref.startswith("//"):
        return None  # внешний ресурс (http(s)://, //cdn...)
    ref_path = parsed.path
    if not ref_path:
        return None
    base_dir = PurePosixPath(base_file_rel).parent
    combined = (base_dir / ref_path)
    # нормализуем ".." и "."
    parts: list[str] = []
    for part in combined.parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part == ".":
            continue
        else:
            parts.append(part)
    return str(PurePosixPath(*parts)) if parts else None


# --------------------------------------------------------------------------
# Модели данных
# --------------------------------------------------------------------------

@dataclass
class TreeNode:
    """Узел дерева каталогов (карта проекта)."""
    name: str
    rel_path: str
    is_dir: bool
    children: list["TreeNode"] = field(default_factory=list)
    kind: str = ""       # 'html' | 'css' | 'js' | 'other' | '' (для директорий)
    size: int = 0


@dataclass
class HtmlInfo:
    rel_path: str
    title: str = ""
    lang: str = ""
    meta_description: str = ""
    doctype_ok: bool = False
    headings: list[tuple] = field(default_factory=list)      # (level:int, text:str)
    stylesheets: list[str] = field(default_factory=list)      # raw href
    scripts: list[dict] = field(default_factory=list)         # {src, defer, async, module, inline}
    inline_styles: list[str] = field(default_factory=list)
    inline_scripts: list[str] = field(default_factory=list)
    forms: list[dict] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    ids: set = field(default_factory=set)
    classes: set = field(default_factory=set)
    landmarks: set = field(default_factory=set)
    comments: list[str] = field(default_factory=list)
    hrefs_internal: list[str] = field(default_factory=list)
    hrefs_external: list[str] = field(default_factory=list)
    word_count: int = 0
    loc: int = 0
    size: int = 0
    is_minified: bool = False
    raw: str = ""


@dataclass
class CssRuleInfo:
    selectors: list[str]
    declarations: list[tuple]   # (prop, value)
    comment: Optional[str]
    line: int


@dataclass
class CssAtRuleInfo:
    kind: str          # media / import / keyframes / font-face / supports / charset / other
    prelude: str
    comment: Optional[str]
    line: int
    nested_rules: list[CssRuleInfo] = field(default_factory=list)


@dataclass
class CssInfo:
    rel_path: str
    rules: list[CssRuleInfo] = field(default_factory=list)
    at_rules: list[CssAtRuleInfo] = field(default_factory=list)
    custom_props_defined: dict = field(default_factory=dict)
    custom_props_used: set = field(default_factory=set)
    colors: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    breakpoints: set = field(default_factory=set)
    unmatched_selectors: list = field(default_factory=list)
    loc: int = 0
    size: int = 0
    is_minified: bool = False
    raw: str = ""


@dataclass
class JsFunctionInfo:
    name: str
    params: list[str]
    kind: str            # function | arrow | method | constructor
    is_exported: bool
    doc: Optional[dict]   # {description, params:{}, returns:str, examples:[]}
    line: int


@dataclass
class JsClassInfo:
    name: str
    extends: Optional[str]
    methods: list[JsFunctionInfo]
    doc: Optional[dict]
    line: int


@dataclass
class JsInfo:
    rel_path: str
    imports: list[dict] = field(default_factory=list)     # {source, names, default_name, namespace}
    requires: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    functions: list[JsFunctionInfo] = field(default_factory=list)
    classes: list[JsClassInfo] = field(default_factory=list)
    dom_queries: list[dict] = field(default_factory=list)  # {method, selector, line}
    event_listeners: list[dict] = field(default_factory=list)
    network_calls: list[dict] = field(default_factory=list)
    todos: list[dict] = field(default_factory=list)
    top_comment: Optional[str] = None
    loc: int = 0
    size: int = 0
    is_minified: bool = False
    raw: str = ""


@dataclass
class Edge:
    src: str
    dst: str
    kind: str            # link|script|css-import|js-import|js-require|dom|style|external|unresolved
    label: str = ""


@dataclass
class ProjectData:
    root_name: str
    generated_at: str
    tree: TreeNode
    html_files: dict            # rel_path -> HtmlInfo
    css_files: dict             # rel_path -> CssInfo
    js_files: dict               # rel_path -> JsInfo
    other_files: list            # rel_path list
    edges: list
    stats: dict


# --------------------------------------------------------------------------
# Сканер проекта: строит дерево каталогов и список файлов
# --------------------------------------------------------------------------

def classify_ext(ext: str) -> str:
    ext = ext.lower()
    if ext in HTML_EXTS:
        return "html"
    if ext in CSS_EXTS:
        return "css"
    if ext in JS_EXTS:
        return "js"
    return "other"


def scan_project(root: Path, ignore_dirs: set, extra_ignore_globs: list) -> tuple:
    """
    Обходит каталог проекта.
    Возвращает (tree: TreeNode, html_paths, css_paths, js_paths, other_paths)
    Пути — относительные (posix-style) к root.
    """
    html_paths, css_paths, js_paths, other_paths = [], [], [], []

    def should_ignore_dir(dirname: str) -> bool:
        if dirname in ignore_dirs:
            return True
        if dirname.startswith(".") and dirname not in (".",):
            return True
        return False

    def build(dir_path: Path, rel: str) -> TreeNode:
        node = TreeNode(name=dir_path.name or root.name, rel_path=rel, is_dir=True)
        try:
            entries = sorted(
                dir_path.iterdir(),
                key=lambda p: (p.is_file(), p.name.lower()),
            )
        except PermissionError:
            return node
        for entry in entries:
            entry_rel = f"{rel}/{entry.name}" if rel else entry.name
            if entry.is_dir():
                if should_ignore_dir(entry.name):
                    continue
                child = build(entry, entry_rel)
                if child.children:  # пропускаем полностью пустые директории
                    node.children.append(child)
            else:
                if any(entry.match(g) for g in extra_ignore_globs):
                    continue
                kind = classify_ext(entry.suffix)
                try:
                    size = entry.stat().st_size
                except OSError:
                    size = 0
                child = TreeNode(
                    name=entry.name, rel_path=entry_rel, is_dir=False,
                    kind=kind, size=size,
                )
                node.children.append(child)
                if kind == "html":
                    html_paths.append(entry_rel)
                elif kind == "css":
                    css_paths.append(entry_rel)
                elif kind == "js":
                    js_paths.append(entry_rel)
                else:
                    other_paths.append(entry_rel)
        return node

    tree = build(root, "")
    return tree, html_paths, css_paths, js_paths, other_paths


# --------------------------------------------------------------------------
# Разбор HTML: используем html.parser.HTMLParser из стандартной библиотеки
# --------------------------------------------------------------------------

from html.parser import HTMLParser  # noqa: E402  (после константных блоков — ок)

_LANDMARK_TAGS = {"header", "nav", "main", "footer", "article", "aside", "section"}
_CAPTURE_TEXT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "title"}


class _HTMLAnalyzer(HTMLParser):
    """Однопроходный разбор HTML в структуру HtmlInfo.

    Namespaced with a leading underscore because it is an internal detail of
    analyze_html() and not part of the public API of this module.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.lang = ""
        self.meta_description = ""
        self.doctype_ok = False
        self.headings: list[tuple] = []
        self.stylesheets: list[str] = []
        self.scripts: list[dict] = []
        self.inline_styles: list[str] = []
        self.inline_scripts: list[str] = []
        self.forms: list[dict] = []
        self.images: list[dict] = []
        self.ids: set = set()
        self.classes: set = set()
        self.landmarks: set = set()
        self.comments: list[str] = []
        self.hrefs: list[str] = []
        self.word_count = 0

        self._capture_stack: list = []     # [[tag, [text_parts]], ...]
        self._tag_stack: list = []
        self._in_script = False
        self._in_style = False
        self._raw_buffer: list = []
        self._current_form: Optional[dict] = None

    # -- обработчики HTMLParser --------------------------------------

    def handle_decl(self, decl):
        if decl.strip().lower().startswith("doctype html"):
            self.doctype_ok = True

    def handle_starttag(self, tag, attrs):
        self._handle_open(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag, attrs):
        self._handle_open(tag, attrs, self_closing=True)

    def _handle_open(self, tag, attrs, self_closing):
        a = {k: (v if v is not None else "") for k, v in attrs}
        self._tag_stack.append(tag)

        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]

        if tag in _CAPTURE_TEXT_TAGS:
            self._capture_stack.append([tag, []])

        if tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.meta_description = a.get("content", "")

        if tag == "link":
            rel = a.get("rel", "").lower()
            if "stylesheet" in rel and a.get("href"):
                self.stylesheets.append(a["href"])

        if tag == "script":
            if a.get("src"):
                self.scripts.append({
                    "src": a["src"],
                    "defer": "defer" in a,
                    "async": "async" in a,
                    "module": a.get("type", "") == "module",
                    "inline": False,
                })
                self._in_script = False
            else:
                self._in_script = True
                self._raw_buffer = []

        if tag == "style":
            self._in_style = True
            self._raw_buffer = []

        if tag == "form":
            self._current_form = {
                "action": a.get("action", ""),
                "method": a.get("method", "get"),
                "fields": [],
            }

        if tag in ("input", "select", "textarea") and self._current_form is not None:
            field_name = a.get("name") or a.get("id") or a.get("type", "field")
            self._current_form["fields"].append(field_name)

        if tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt", "")})

        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])

        if tag in _LANDMARK_TAGS:
            self.landmarks.add(tag)

        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("class"):
            for c in a["class"].split():
                self.classes.add(c)

        if self_closing:
            self._handle_close(tag)

    def handle_endtag(self, tag):
        self._handle_close(tag)

    def _handle_close(self, tag):
        if self._tag_stack and tag in self._tag_stack:
            # снимаем стек до найденного тега (терпимо к незакрытым тегам вроде <br>)
            while self._tag_stack and self._tag_stack[-1] != tag:
                self._tag_stack.pop()
            if self._tag_stack:
                self._tag_stack.pop()

        if self._capture_stack and self._capture_stack[-1][0] == tag:
            _, parts = self._capture_stack.pop()
            text = "".join(parts).strip()
            text = re.sub(r"\s+", " ", text)
            if tag == "title":
                self.title = text
            else:
                self.headings.append((int(tag[1]), text))

        if tag == "script" and self._in_script:
            code = "".join(self._raw_buffer)
            if code.strip():
                self.inline_scripts.append(code)
            self._in_script = False

        if tag == "style" and self._in_style:
            css_text = "".join(self._raw_buffer)
            if css_text.strip():
                self.inline_styles.append(css_text)
            self._in_style = False

        if tag == "form" and self._current_form is not None:
            self.forms.append(self._current_form)
            self._current_form = None

    def handle_data(self, data):
        if self._in_script or self._in_style:
            self._raw_buffer.append(data)
            return
        if self._capture_stack:
            self._capture_stack[-1][1].append(data)
        text = data.strip()
        if text:
            self.word_count += len(text.split())

    def handle_comment(self, data):
        text = data.strip()
        if text:
            self.comments.append(text)


def analyze_html(rel_path: str, raw: str) -> HtmlInfo:
    parser = _HTMLAnalyzer()
    try:
        parser.feed(raw)
        parser.close()
    except Exception:
        # HTMLParser редко падает, но лучше не терять весь прогон из-за одного файла
        pass

    internal, external = [], []
    for href in parser.hrefs:
        target = resolve_relative(rel_path, href)
        if target:
            internal.append(target)
        elif not href.startswith("#"):
            external.append(href)

    info = HtmlInfo(
        rel_path=rel_path,
        title=parser.title,
        lang=parser.lang,
        meta_description=parser.meta_description,
        doctype_ok=parser.doctype_ok,
        headings=parser.headings,
        stylesheets=parser.stylesheets,
        scripts=parser.scripts,
        inline_styles=parser.inline_styles,
        inline_scripts=parser.inline_scripts,
        forms=parser.forms,
        images=parser.images,
        ids=parser.ids,
        classes=parser.classes,
        landmarks=parser.landmarks,
        comments=parser.comments,
        hrefs_internal=internal,
        hrefs_external=external,
        word_count=parser.word_count,
        loc=count_loc(raw),
        size=len(raw.encode("utf-8", errors="ignore")),
        is_minified=is_probably_minified(raw),
        raw=raw,
    )
    return info


# --------------------------------------------------------------------------
# Разбор CSS: собственный лёгкий токенизатор (без внешних зависимостей)
#
# CSS не входит в стандартную библиотеку Python, поэтому парсер написан
# вручную: однопроходный сканер с подсчётом вложенности фигурных скобок
# (нужен для @media/@supports/@keyframes, где скобки вложены), который
# попутно распознаёт комментарии и связывает комментарий, стоящий сразу
# перед правилом, с этим правилом — по мотивам синтаксиса KSS
# (Knyle Style Sheets), где ведущий комментарий = документация компонента.
# --------------------------------------------------------------------------

_COLOR_RE = re.compile(
    r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)"
)
_VAR_USAGE_RE = re.compile(r"var\(\s*(--[a-zA-Z0-9_-]+)")
_BREAKPOINT_RE = re.compile(
    r"(min-width|max-width|min-height|max-height)\s*:\s*([\d.]+[a-z%]*)"
)


def _split_top_level(text: str, sep: str) -> list:
    """Разбивает строку по разделителю, не учитывая тот, что внутри ()/[]/строк."""
    parts, buf, depth = [], [], 0
    in_str = None
    i = 0
    while i < len(text):
        ch = text[i]
        if in_str:
            buf.append(ch)
            if ch == "\\" and i + 1 < len(text):
                buf.append(text[i + 1])
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in "'\"":
            in_str = ch
            buf.append(ch)
        elif ch in "([":
            depth += 1
            buf.append(ch)
        elif ch in ")]":
            depth -= 1
            buf.append(ch)
        elif ch == sep and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
        i += 1
    parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def _parse_css_blocks(text: str) -> list:
    """
    Однопроходный сканер CSS-текста (или тела @media).
    Возвращает список блоков: {'type': 'rule'|'at-simple'|'at-block',
                                'prelude': str, 'body': str|None,
                                'comment': str|None, 'line': int}
    """
    n = len(text)
    i = 0
    blocks = []
    last_comment = None

    while i < n:
        ch = text[i]

        if ch in " \t\r\n":
            i += 1
            continue

        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            end = n if end == -1 else end
            last_comment = text[i + 2:end].strip()
            i = (end + 2) if end < n else n
            continue

        line_no = text.count("\n", 0, i) + 1

        if ch == "@":
            j = i
            depth_brk = 0
            while j < n and text[j] not in "{;":
                if text[j] == "/" and j + 1 < n and text[j + 1] == "*":
                    break
                j += 1
            prelude = text[i:j].strip()
            if j < n and text[j] == ";":
                blocks.append({"type": "at-simple", "prelude": prelude,
                                "body": None, "comment": last_comment, "line": line_no})
                i = j + 1
            elif j < n and text[j] == "{":
                depth = 1
                k = j + 1
                while k < n and depth > 0:
                    if text[k] == "{":
                        depth += 1
                    elif text[k] == "}":
                        depth -= 1
                    k += 1
                body = text[j + 1:k - 1]
                blocks.append({"type": "at-block", "prelude": prelude,
                                "body": body, "comment": last_comment, "line": line_no})
                i = k
            else:
                i = n
            last_comment = None
            continue

        # обычное правило: селектор(ы) { объявления }
        j = i
        while j < n and text[j] not in "{}":
            if text[j] == "/" and j + 1 < n and text[j + 1] == "*":
                # комментарий внутри списка селекторов — пропускаем его как текст
                end2 = text.find("*/", j + 2)
                j = (end2 + 2) if end2 != -1 else n
                continue
            j += 1
        if j >= n or text[j] != "{":
            i = n
            continue
        selector_text = text[i:j].strip()
        depth = 1
        k = j + 1
        while k < n and depth > 0:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        body = text[j + 1:k - 1]
        if selector_text:
            blocks.append({"type": "rule", "prelude": selector_text,
                            "body": body, "comment": last_comment, "line": line_no})
        i = k
        last_comment = None

    return blocks


def _parse_declarations(body: str) -> list:
    decls = []
    for chunk in _split_top_level(body, ";"):
        if ":" not in chunk:
            continue
        prop, _, value = chunk.partition(":")
        decls.append((prop.strip(), value.strip()))
    return decls


def analyze_css(rel_path: str, raw: str) -> CssInfo:
    info = CssInfo(
        rel_path=rel_path,
        loc=count_loc(raw),
        size=len(raw.encode("utf-8", errors="ignore")),
        is_minified=is_probably_minified(raw),
        raw=raw,
    )

    blocks = _parse_css_blocks(raw)
    for b in blocks:
        if b["type"] == "rule":
            selectors = _split_top_level(b["prelude"], ",")
            decls = _parse_declarations(b["body"])
            for prop, value in decls:
                if prop.startswith("--"):
                    info.custom_props_defined[prop] = value
                for m in _VAR_USAGE_RE.finditer(value):
                    info.custom_props_used.add(m.group(1))
                for m in _COLOR_RE.finditer(value):
                    info.colors.append(m.group(0))
            info.rules.append(CssRuleInfo(
                selectors=selectors, declarations=decls,
                comment=b["comment"], line=b["line"],
            ))
        elif b["type"] == "at-simple":
            prelude = b["prelude"]
            kind = "import" if prelude.startswith("@import") else \
                   "charset" if prelude.startswith("@charset") else "other"
            if kind == "import":
                m = re.search(r"""@import\s+(?:url\(\s*)?["']?([^"')]+)["']?\)?""", prelude)
                if m:
                    target = resolve_relative(rel_path, m.group(1))
                    if target:
                        info.imports.append(target)
            info.at_rules.append(CssAtRuleInfo(
                kind=kind, prelude=prelude, comment=b["comment"], line=b["line"],
            ))
        elif b["type"] == "at-block":
            prelude = b["prelude"]
            if prelude.startswith("@media"):
                kind = "media"
                for m in _BREAKPOINT_RE.finditer(prelude):
                    info.breakpoints.add(f"{m.group(1)}: {m.group(2)}")
            elif prelude.startswith("@keyframes") or prelude.startswith("@-webkit-keyframes"):
                kind = "keyframes"
            elif prelude.startswith("@font-face"):
                kind = "font-face"
            elif prelude.startswith("@supports"):
                kind = "supports"
            else:
                kind = "other"

            nested = []
            if kind in ("media", "supports"):
                for nb in _parse_css_blocks(b["body"]):
                    if nb["type"] != "rule":
                        continue
                    selectors = _split_top_level(nb["prelude"], ",")
                    decls = _parse_declarations(nb["body"])
                    for prop, value in decls:
                        for m in _VAR_USAGE_RE.finditer(value):
                            info.custom_props_used.add(m.group(1))
                        for m in _COLOR_RE.finditer(value):
                            info.colors.append(m.group(0))
                    nested.append(CssRuleInfo(
                        selectors=selectors, declarations=decls,
                        comment=nb["comment"], line=nb["line"],
                    ))
            else:
                decls = _parse_declarations(b["body"] or "")
                for prop, value in decls:
                    for m in _COLOR_RE.finditer(value):
                        info.colors.append(m.group(0))

            info.at_rules.append(CssAtRuleInfo(
                kind=kind, prelude=prelude, comment=b["comment"], line=b["line"],
                nested_rules=nested,
            ))

    return info


# --------------------------------------------------------------------------
# Разбор JavaScript: эвристический (regex + маскирование строк/комментариев),
# без полноценного AST-парсера.
#
# Полный синтаксический разбор JS в чистом Python (без Node.js/Acorn/Esprima)
# — отдельная большая задача. Для целей документации важнее не 100% точный
# AST, а надёжное извлечение "витрины" файла: что импортируется/экспортируется,
# какие функции/классы объявлены, к каким элементам DOM обращается код и какие
# у функций JSDoc-комментарии. Поэтому используется маскирование строк и
# комментариев (чтобы регулярные выражения не путали текст внутри строк с
# кодом), а затем набор целевых регулярных выражений по замаскированному
# тексту, с извлечением реального фрагмента из оригинального текста.
# Ограничения этого подхода описаны в README.md.
# --------------------------------------------------------------------------

def _mask_js(text: str) -> str:
    """
    Возвращает строку той же длины, что и text, в которой:
      - содержимое комментариев (// и /* */) заменено пробелами;
      - содержимое template-литералов (`...`) заменено пробелами — в них
        часто лежит HTML-разметка с интерполяцией, которая иначе даёт
        ложные срабатывания при поиске структуры кода (например, похожие
        на теги или объявления функций фрагменты внутри строки-шаблона).
      - обычные '...' и "..." строки НЕ маскируются: именно в них лежат
        пути импортов, CSS-селекторы и имена событий, которые как раз
        нужно прочитать при разборе.
    Переносы строк всегда сохраняются, чтобы не сбить нумерацию строк.

    Ограничение: различить регулярно-выражённый литерал /.../ и оператор
    деления без полноценного токенайзера невозможно; здесь используется
    упрощённое правило (см. README.md, раздел "Известные ограничения").
    """
    out = list(text)
    n = len(text)
    i = 0

    def blank(a, b):
        for idx in range(a, b):
            if out[idx] != "\n":
                out[idx] = " "

    while i < n:
        ch = text[i]
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            j = n if j == -1 else j + 2
            blank(i, j)
            i = j
            continue
        if ch == "`":
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == "`":
                    j += 1
                    break
                j += 1
            blank(i, j)
            i = j
            continue
        if ch in "'\"":
            # строки НЕ маскируем, только перепрыгиваем их целиком, чтобы
            # спецсимволы/скобки внутри не сбили дальнейшее сканирование
            quote = ch
            j = i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == quote:
                    j += 1
                    break
                j += 1
            i = j
            continue
        i += 1
    return "".join(out)


_IMPORT_STATIC_RE = re.compile(
    r"import\s+(?P<clause>[^;\n]*?)\s+from\s+['\"](?P<src>[^'\"]+)['\"]"
)
_IMPORT_BARE_RE = re.compile(r"import\s+['\"](?P<src>[^'\"]+)['\"]")
_IMPORT_DYNAMIC_RE = re.compile(r"import\(\s*['\"](?P<src>[^'\"]+)['\"]\s*\)")
_REQUIRE_RE = re.compile(r"require\(\s*['\"](?P<src>[^'\"]+)['\"]\s*\)")

_EXPORT_DEFAULT_RE = re.compile(r"export\s+default\b")
_EXPORT_NAMED_DECL_RE = re.compile(
    r"export\s+(?:const|let|var|function\*?|class)\s+(?P<name>[A-Za-z_$][\w$]*)"
)
_EXPORT_LIST_RE = re.compile(r"export\s*\{([^}]+)\}")

_FUNCTION_DECL_RE = re.compile(
    r"(?<![\w$.])function\s*\*?\s*(?P<name>[A-Za-z_$][\w$]*)\s*\((?P<params>[^)]*)\)"
)
_ARROW_CONST_RE = re.compile(
    r"(?<![\w$.])(?:export\s+)?(?:const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*=\s*"
    r"(?:async\s*)?\((?P<params>[^)]*)\)\s*=>"
)
_ARROW_CONST_1ARG_RE = re.compile(
    r"(?<![\w$.])(?:export\s+)?(?:const|let|var)\s+(?P<name>[A-Za-z_$][\w$]*)\s*=\s*"
    r"(?:async\s*)?(?P<params>[A-Za-z_$][\w$]*)\s*=>"
)
_CLASS_RE = re.compile(
    r"(?<![\w$.])class\s+(?P<name>[A-Za-z_$][\w$]*)(?:\s+extends\s+(?P<extends>[A-Za-z_$][\w$.]*))?\s*\{"
)
_METHOD_RE = re.compile(
    r"(?<![\w$.])(?:static\s+)?(?:async\s+)?(?:\*\s*)?(?:get\s+|set\s+)?"
    r"(?P<name>[A-Za-z_$][\w$]*)\s*\((?P<params>[^)]*)\)\s*\{"
)

_DOM_QUERY_RE = re.compile(
    r"(?:document|[\w$]+)\.(?P<method>querySelector(?:All)?|getElementById|"
    r"getElementsByClassName|getElementsByTagName|closest)\(\s*(?P<q>['\"`])(?P<sel>.*?)(?P=q)\s*\)"
)
_EVENT_LISTENER_RE = re.compile(
    r"(?P<target>[\w$.]+)\.addEventListener\(\s*(?P<q>['\"`])(?P<evt>\w+)(?P=q)"
)
_FETCH_RE = re.compile(r"(?<![\w$.])fetch\s*\(")
_XHR_RE = re.compile(r"new\s+XMLHttpRequest\s*\(")
_AXIOS_RE = re.compile(r"(?<![\w$.])axios\.(get|post|put|delete|patch)\s*\(")

_JSDOC_RE = re.compile(r"/\*\*(?P<body>.*?)\*/\s*\n?", re.DOTALL)
_JSDOC_PARAM_RE = re.compile(
    r"@param\s+(?:\{[^}]*\}\s*)?(?P<name>[\w.$\[\]]+)\s*-?\s*(?P<desc>.*)"
)
_JSDOC_RETURNS_RE = re.compile(r"@returns?\s+(?:\{[^}]*\}\s*)?(?P<desc>.*)")
_JSDOC_EXAMPLE_RE = re.compile(r"@example\s*\n?(?P<code>(?:.*\n?)*)")
_TODO_RE = re.compile(r"(TODO|FIXME|HACK|XXX)\s*:?\s*(.*)")


def _parse_jsdoc(comment_body: str) -> dict:
    """Разбирает тело JSDoc-комментария (между /** и */) на структуру."""
    lines = [re.sub(r"^\s*\*\s?", "", ln) for ln in comment_body.splitlines()]
    description_lines = []
    params = {}
    returns = None
    examples = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("@param"):
            m = _JSDOC_PARAM_RE.match(stripped)
            if m:
                params[m.group("name")] = m.group("desc").strip()
        elif stripped.startswith("@return"):
            m = _JSDOC_RETURNS_RE.match(stripped)
            if m:
                returns = m.group("desc").strip()
        elif stripped.startswith("@example"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("@"):
                code_lines.append(lines[i])
                i += 1
            examples.append("\n".join(code_lines).strip())
            continue
        elif stripped.startswith("@"):
            pass  # другие теги (@deprecated, @throws...) — не критичны для обзора
        elif stripped:
            description_lines.append(stripped)
        i += 1
    return {
        "description": " ".join(description_lines).strip(),
        "params": params,
        "returns": returns,
        "examples": examples,
    }


def _collect_jsdoc_map(raw: str) -> dict:
    """Строит отображение 'позиция окончания комментария' -> распарсенный JSDoc,
    чтобы затем находить ближайший предшествующий JSDoc для функции/класса."""
    result = []
    for m in _JSDOC_RE.finditer(raw):
        result.append((m.end(), _parse_jsdoc(m.group("body"))))
    return result


def _nearest_jsdoc(jsdoc_list: list, decl_start: int, raw: str) -> Optional[dict]:
    """Возвращает JSDoc, если между его концом и началом объявления нет
    ничего, кроме пробелов и модификаторов export/default/async — то есть
    комментарий действительно документирует именно это объявление."""
    best = None
    for end_pos, parsed in jsdoc_list:
        if end_pos > decl_start:
            continue
        gap_tokens = raw[end_pos:decl_start].split()
        if all(tok in ("export", "default", "async") for tok in gap_tokens):
            best = parsed
    return best


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _extract_class_body(masked: str, raw: str, start_brace: int) -> tuple:
    """По позиции открывающей { возвращает (тело_класса, индекс_после_закрывающей)."""
    depth = 1
    k = start_brace + 1
    n = len(masked)
    while k < n and depth > 0:
        if masked[k] == "{":
            depth += 1
        elif masked[k] == "}":
            depth -= 1
        k += 1
    return raw[start_brace + 1:k - 1], masked[start_brace + 1:k - 1], k


def analyze_js(rel_path: str, raw: str) -> JsInfo:
    info = JsInfo(
        rel_path=rel_path,
        loc=count_loc(raw),
        size=len(raw.encode("utf-8", errors="ignore")),
        is_minified=is_probably_minified(raw),
        raw=raw,
    )

    if info.is_minified:
        # Минифицированный файл: разбор ничего не даст, кроме "мусора".
        # Возвращаем только базовую статистику.
        return info

    masked = _mask_js(raw)
    jsdoc_list = _collect_jsdoc_map(raw)

    exported_names = set()
    if _EXPORT_DEFAULT_RE.search(masked):
        exported_names.add("default")
    for m in _EXPORT_NAMED_DECL_RE.finditer(masked):
        exported_names.add(m.group("name"))
        info.exports.append(m.group("name"))
    for m in _EXPORT_LIST_RE.finditer(masked):
        for part in m.group(1).split(","):
            name = part.strip().split(" as ")[0].strip()
            if name:
                exported_names.add(name)
                info.exports.append(name)

    for m in _IMPORT_STATIC_RE.finditer(masked):
        clause = m.group("clause")
        names = []
        default_name = None
        namespace = None
        ns_match = re.match(r"\*\s+as\s+([\w$]+)", clause)
        if ns_match:
            namespace = ns_match.group(1)
        else:
            brace_match = re.search(r"\{([^}]*)\}", clause)
            before_brace = clause.split("{")[0].strip().rstrip(",").strip()
            if before_brace:
                default_name = before_brace
            if brace_match:
                names = [p.strip().split(" as ")[0].strip()
                         for p in brace_match.group(1).split(",") if p.strip()]
        info.imports.append({
            "source": m.group("src"), "names": names,
            "default_name": default_name, "namespace": namespace,
        })
    for m in _IMPORT_BARE_RE.finditer(masked):
        info.imports.append({"source": m.group("src"), "names": [],
                              "default_name": None, "namespace": None})
    for m in _IMPORT_DYNAMIC_RE.finditer(masked):
        info.imports.append({"source": m.group("src"), "names": [],
                              "default_name": None, "namespace": None, "dynamic": True})
    for m in _REQUIRE_RE.finditer(masked):
        info.requires.append(m.group("src"))

    # top-level функции
    seen_spans = []
    for m in _FUNCTION_DECL_RE.finditer(masked):
        name = m.group("name")
        params = [p.strip() for p in m.group("params").split(",") if p.strip()]
        doc = _nearest_jsdoc(jsdoc_list, m.start(), raw)
        info.functions.append(JsFunctionInfo(
            name=name, params=params, kind="function",
            is_exported=name in exported_names, doc=doc, line=_line_of(raw, m.start()),
        ))
        seen_spans.append((m.start(), m.end()))

    for pattern in (_ARROW_CONST_RE, _ARROW_CONST_1ARG_RE):
        for m in pattern.finditer(masked):
            if any(a <= m.start() < b for a, b in seen_spans):
                continue
            name = m.group("name")
            params_raw = m.group("params")
            params = [p.strip() for p in params_raw.split(",") if p.strip()]
            doc = _nearest_jsdoc(jsdoc_list, m.start(), raw)
            info.functions.append(JsFunctionInfo(
                name=name, params=params, kind="arrow",
                is_exported=name in exported_names, doc=doc, line=_line_of(raw, m.start()),
            ))
            seen_spans.append((m.start(), m.end()))

    # классы
    for m in _CLASS_RE.finditer(masked):
        name = m.group("name")
        extends = m.group("extends")
        brace_pos = masked.find("{", m.end() - 1)
        if brace_pos == -1:
            continue
        body_raw, body_masked, _end = _extract_class_body(masked, raw, brace_pos)
        methods = []
        for mm in _METHOD_RE.finditer(body_masked):
            mname = mm.group("name")
            if mname in JS_CONTROL_KEYWORDS:
                continue
            mparams = [p.strip() for p in mm.group("params").split(",") if p.strip()]
            abs_pos = brace_pos + 1 + mm.start()
            mdoc = _nearest_jsdoc(jsdoc_list, abs_pos, raw)
            kind = "constructor" if mname == "constructor" else "method"
            methods.append(JsFunctionInfo(
                name=mname, params=mparams, kind=kind,
                is_exported=False, doc=mdoc, line=_line_of(raw, abs_pos),
            ))
        cdoc = _nearest_jsdoc(jsdoc_list, m.start(), raw)
        info.classes.append(JsClassInfo(
            name=name, extends=extends, methods=methods, doc=cdoc,
            line=_line_of(raw, m.start()),
        ))

    for m in _DOM_QUERY_RE.finditer(masked):
        info.dom_queries.append({
            "method": m.group("method"), "selector": m.group("sel"),
            "line": _line_of(raw, m.start()),
        })

    for m in _EVENT_LISTENER_RE.finditer(masked):
        info.event_listeners.append({
            "target": m.group("target"), "event": m.group("evt"),
            "line": _line_of(raw, m.start()),
        })

    for regex, kind in ((_FETCH_RE, "fetch"), (_XHR_RE, "xhr"), (_AXIOS_RE, "axios")):
        for m in regex.finditer(masked):
            info.network_calls.append({"kind": kind, "line": _line_of(raw, m.start())})

    for m in re.finditer(r"//[^\n]*|/\*.*?\*/", raw, re.DOTALL):
        tm = _TODO_RE.search(m.group(0))
        if tm:
            info.todos.append({
                "marker": tm.group(1), "text": tm.group(2).strip(),
                "line": _line_of(raw, m.start()),
            })

    # первый комментарий файла (если стоит в самом начале) — часто содержит
    # общее назначение модуля
    head = raw.lstrip()
    if head.startswith("/**") or head.startswith("/*"):
        end = head.find("*/")
        if end != -1:
            info.top_comment = re.sub(r"^\s*\*\s?", "", head[2:end], flags=re.MULTILINE).strip()
    elif head.startswith("//"):
        first_lines = []
        for ln in head.splitlines():
            if ln.strip().startswith("//"):
                first_lines.append(ln.strip()[2:].strip())
            else:
                break
        if first_lines:
            info.top_comment = " ".join(first_lines)

    return info


# --------------------------------------------------------------------------
# Построение связей между файлами ("карта зависимостей")
#
# Два уровня связей:
#   1. Структурные — то, что явно прописано в коде: <link>, <script src>,
#      @import, import/require.
#   2. Смысловые (DOM) — то, что связывает файлы через использование:
#      JS обращается к элементу по #id/.class, CSS-селектор нацелен на
#      #id/.class. Эти связи не видны по одним только "ссылкам" в файлах,
#      но именно они показывают, как HTML/CSS/JS реально работают вместе.
# --------------------------------------------------------------------------

_SIMPLE_TOKEN_RE = re.compile(r"[.#]([A-Za-z_-][\w-]*)")


def _selector_tokens(selector: str) -> list:
    """Извлекает простые #id и .class токены из CSS/JS-селектора."""
    return _SIMPLE_TOKEN_RE.findall(selector)


def build_edges(html_files: dict, css_files: dict, js_files: dict) -> tuple:
    """Возвращает (edges, used_tokens): used_tokens — множество всех
    #id/.class токенов, которые хоть раз были найдены и в HTML, и в
    CSS-селекторе или JS DOM-запросе (используется для поиска "мёртвых"
    хуков независимо от дедупликации рёбер в графе для отображения)."""
    edges: list = []
    used_tokens: set = set()

    all_html_paths = set(html_files)
    all_css_paths = set(css_files)
    all_js_paths = set(js_files)

    # реестр: где определены id/class (для смысловых связей)
    id_registry: dict = {}
    class_registry: dict = {}
    for path, hinfo in html_files.items():
        for i in hinfo.ids:
            id_registry.setdefault(i, []).append(path)
        for c in hinfo.classes:
            class_registry.setdefault(c, []).append(path)

    # 1. HTML -> CSS (<link rel=stylesheet>), HTML -> JS (<script src>),
    #    HTML -> HTML (<a href> на другую страницу проекта)
    for path, hinfo in html_files.items():
        for href in hinfo.hrefs_internal:
            if href in all_html_paths and href != path:
                edges.append(Edge(path, href, "page-link"))
        for href in hinfo.stylesheets:
            target = resolve_relative(path, href)
            if target and target in all_css_paths:
                edges.append(Edge(path, target, "link"))
            elif target:
                edges.append(Edge(path, target, "unresolved", label=href))
            else:
                edges.append(Edge(path, href, "external", label="CSS"))
        for script in hinfo.scripts:
            target = resolve_relative(path, script["src"])
            if target and target in all_js_paths:
                edges.append(Edge(path, target, "script"))
            elif target:
                edges.append(Edge(path, target, "unresolved", label=script["src"]))
            else:
                edges.append(Edge(path, script["src"], "external", label="JS"))

    # 2. CSS -> CSS (@import)
    for path, cinfo in css_files.items():
        for target in cinfo.imports:
            if target in all_css_paths:
                edges.append(Edge(path, target, "css-import"))

    # 3. JS -> JS (import/require), JS -> внешние библиотеки
    for path, jinfo in js_files.items():
        for imp in jinfo.imports:
            target = resolve_relative(path, imp["source"])
            if target is None:
                edges.append(Edge(path, imp["source"], "external", label="import"))
                continue
            resolved = None
            for candidate in (target, f"{target}.js", f"{target}.mjs", f"{target}/index.js"):
                if candidate in all_js_paths:
                    resolved = candidate
                    break
            edges.append(Edge(path, resolved or target,
                               "js-import" if resolved else "unresolved"))
        for src in jinfo.requires:
            target = resolve_relative(path, src)
            if target is None:
                edges.append(Edge(path, src, "external", label="require"))
                continue
            resolved = None
            for candidate in (target, f"{target}.js", f"{target}/index.js"):
                if candidate in all_js_paths:
                    resolved = candidate
                    break
            edges.append(Edge(path, resolved or target,
                               "js-require" if resolved else "unresolved"))

    # 4. JS -> HTML (обращение к DOM по #id/.class)
    for path, jinfo in js_files.items():
        for q in jinfo.dom_queries:
            method, sel = q["method"], q["selector"]
            targets = set()
            if method == "getElementById":
                targets.update(id_registry.get(sel, []))
                if sel in id_registry:
                    used_tokens.add(sel)
            else:
                for tok in _selector_tokens(sel) or ([sel] if method in
                        ("getElementsByClassName",) else []):
                    targets.update(id_registry.get(tok, []))
                    targets.update(class_registry.get(tok, []))
                    if tok in id_registry or tok in class_registry:
                        used_tokens.add(tok)
            if targets:
                for t in targets:
                    edges.append(Edge(path, t, "dom", label=sel))
            else:
                edges.append(Edge(path, "?", "dom-unresolved", label=sel))

    # 5. CSS -> HTML (селектор нацелен на #id/.class, объявленный в HTML)
    for path, cinfo in css_files.items():
        all_rules = list(cinfo.rules)
        for at in cinfo.at_rules:
            all_rules.extend(at.nested_rules)
        seen_targets = set()
        unmatched = []
        for rule in all_rules:
            for sel in rule.selectors:
                for tok in _selector_tokens(sel):
                    hit = False
                    for t in id_registry.get(tok, []) + class_registry.get(tok, []):
                        if (path, t) not in seen_targets:
                            edges.append(Edge(path, t, "style", label="." + tok))
                            seen_targets.add((path, t))
                        hit = True
                    if hit:
                        used_tokens.add(tok)
                    else:
                        unmatched.append(tok)
        cinfo.unmatched_selectors = sorted(set(unmatched))

    return edges, used_tokens


# --------------------------------------------------------------------------
# Агрегированная статистика по проекту (для секции "Обзор")
# --------------------------------------------------------------------------

def _normalize_color(c: str) -> str:
    return re.sub(r"\s+", " ", c.strip()).lower()


def analyze_project_stats(html_files: dict, css_files: dict, js_files: dict,
                           other_files: list, edges: list, used_tokens: set) -> dict:
    stats: dict = {}

    n_html, n_css, n_js = len(html_files), len(css_files), len(js_files)
    total_loc = (sum(f.loc for f in html_files.values())
                 + sum(f.loc for f in css_files.values())
                 + sum(f.loc for f in js_files.values()))
    total_size = (sum(f.size for f in html_files.values())
                  + sum(f.size for f in css_files.values())
                  + sum(f.size for f in js_files.values()))

    stats["counts"] = {"html": n_html, "css": n_css, "js": n_js,
                        "other": len(other_files),
                        "total": n_html + n_css + n_js + len(other_files)}
    stats["total_loc"] = total_loc
    stats["total_size"] = total_size

    all_files = (
        [(p, f.size, f.loc, "html") for p, f in html_files.items()]
        + [(p, f.size, f.loc, "css") for p, f in css_files.items()]
        + [(p, f.size, f.loc, "js") for p, f in js_files.items()]
    )
    stats["largest_files"] = sorted(all_files, key=lambda t: -t[1])[:5]

    # цветовая палитра проекта (по частоте использования)
    color_counter: dict = {}
    for cinfo in css_files.values():
        for c in cinfo.colors:
            key = _normalize_color(c)
            color_counter[key] = color_counter.get(key, 0) + 1
    stats["palette"] = sorted(color_counter.items(), key=lambda t: -t[1])[:24]

    # брейкпоинты адаптива
    breakpoints = set()
    for cinfo in css_files.values():
        breakpoints |= cinfo.breakpoints
    stats["breakpoints"] = sorted(breakpoints)

    # внешние библиотеки (по script src и import/require без резолва в проект)
    external_libs = set()
    for hinfo in html_files.values():
        for s in hinfo.scripts:
            src = s["src"]
            if resolve_relative(hinfo.rel_path, src) is None:
                name = src.split("/")[-1].split("?")[0]
                external_libs.add(name)
    for jinfo in js_files.values():
        for imp in jinfo.imports:
            if resolve_relative(jinfo.rel_path, imp["source"]) is None:
                external_libs.add(imp["source"])
        for req in jinfo.requires:
            if resolve_relative(jinfo.rel_path, req) is None:
                external_libs.add(req)
    stats["external_libs"] = sorted(external_libs)

    # TODO/FIXME по всему проекту
    todos = []
    for jinfo in js_files.values():
        for t in jinfo.todos:
            todos.append({**t, "file": jinfo.rel_path})
    stats["todos"] = todos

    # неиспользуемые id/class (объявлены в HTML, но ни разу не встречены
    # ни в одном CSS-селекторе, ни в одном DOM-запросе из JS)
    all_ids, all_classes = set(), set()
    for hinfo in html_files.values():
        all_ids |= hinfo.ids
        all_classes |= hinfo.classes
    stats["unused_ids"] = sorted(all_ids - used_tokens)
    stats["unused_classes"] = sorted(all_classes - used_tokens)

    # orphan CSS-селекторы (собраны на уровне build_edges, просто сводим)
    orphan_selectors = []
    for path, cinfo in css_files.items():
        for sel in cinfo.unmatched_selectors:
            orphan_selectors.append({"file": path, "token": sel})
    stats["orphan_css_selectors"] = orphan_selectors

    # неразрешённые ссылки (битые пути)
    stats["unresolved_links"] = [
        {"src": e.src, "dst": e.dst, "label": e.label}
        for e in edges if e.kind == "unresolved"
    ]

    # доступность: картинки без alt, формы без label - лёгкая эвристика
    images_no_alt = []
    for hinfo in html_files.values():
        for img in hinfo.images:
            if not img.get("alt"):
                images_no_alt.append({"file": hinfo.rel_path, "src": img.get("src", "")})
    stats["images_no_alt"] = images_no_alt

    return stats


# --------------------------------------------------------------------------
# Подсветка синтаксиса (выполняется на стороне Python при генерации,
# результат — уже готовый HTML с <span class="tok-...">, без JS-зависимостей
# при чтении документации и без внешних CDN типа highlight.js/Prism).
# --------------------------------------------------------------------------

def _tokenize_generic(text: str, patterns: list) -> str:
    """
    patterns: список (regex, css_class) в порядке приоритета.
    Собирает один общий regex с именованными группами и последовательно
    оборачивает совпадения в <span class="tok-...">, экранируя остальной
    текст через html.escape.
    """
    combined = re.compile(
        "|".join(f"(?P<g{i}>{p.pattern})" for i, (p, _) in enumerate(patterns)),
        re.DOTALL,
    )
    classes = [cls for _, cls in patterns]
    out = []
    pos = 0
    for m in combined.finditer(text):
        if m.start() > pos:
            out.append(esc(text[pos:m.start()]))
        idx = int(m.lastgroup[1:])
        out.append(f'<span class="tok-{classes[idx]}">{esc(m.group())}</span>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def highlight_html(src: str) -> str:
    patterns = [
        (re.compile(r"<!--.*?-->", re.DOTALL), "com"),
        (re.compile(r"<!DOCTYPE[^>]*>", re.IGNORECASE), "doctype"),
        (re.compile(r'"[^"]*"|\'[^\']*\''), "str"),
        (re.compile(r"</?[a-zA-Z][\w:-]*"), "tag"),
        (re.compile(r"[a-zA-Z-:]+(?==)"), "attr"),
        (re.compile(r"/?>"), "tag"),
    ]
    return _tokenize_generic(src, patterns)


def highlight_css(src: str) -> str:
    patterns = [
        (re.compile(r"/\*.*?\*/", re.DOTALL), "com"),
        (re.compile(r'"[^"]*"|\'[^\']*\''), "str"),
        (re.compile(r"@[\w-]+"), "kw"),
        (re.compile(r"--[\w-]+"), "var"),
        (re.compile(r"#[0-9a-fA-F]{3,8}\b"), "num"),
        (re.compile(r"[.#][\w-]+"), "sel"),
        (re.compile(r"\b\d+(\.\d+)?(px|em|rem|%|vh|vw|s|ms|deg)?\b"), "num"),
        (re.compile(r"[\w-]+(?=\s*:)"), "prop"),
    ]
    return _tokenize_generic(src, patterns)


def highlight_js(src: str) -> str:
    kw_pattern = r"\b(?:" + "|".join(sorted(JS_KEYWORDS, key=len, reverse=True)) + r")\b"
    patterns = [
        (re.compile(r"/\*\*?.*?\*/", re.DOTALL), "com"),
        (re.compile(r"//[^\n]*"), "com"),
        (re.compile(r"`(?:\\.|[^`\\])*`"), "str"),
        (re.compile(r'"(?:\\.|[^"\\])*"'), "str"),
        (re.compile(r"'(?:\\.|[^'\\])*'"), "str"),
        (re.compile(kw_pattern), "kw"),
        (re.compile(r"\b\d+(\.\d+)?\b"), "num"),
        (re.compile(r"[\w$]+(?=\()"), "fn"),
    ]
    return _tokenize_generic(src, patterns)


def highlight_by_kind(src: str, kind: str) -> str:
    if kind == "html":
        return highlight_html(src)
    if kind == "css":
        return highlight_css(src)
    if kind == "js":
        return highlight_js(src)
    return esc(src)


# --------------------------------------------------------------------------
# SVG-карта зависимостей ("атлас" проекта): HTML/CSS/JS файлы как узлы в
# трёх колонках, связи между ними — как маршруты между "станциями".
# Рисуется на стороне Python, без JS-библиотек для графов.
# --------------------------------------------------------------------------

_GRAPH_NODE_W = 240
_GRAPH_NODE_H = 40
_GRAPH_ROW_GAP = 14
_GRAPH_TOP = 64
_GRAPH_COL_X = {"html": 30, "css": 380, "js": 730}
_GRAPH_COL_TITLE = {"html": "HTML", "css": "CSS", "js": "JS"}


def _truncate_label(name: str, max_chars: int = 26) -> str:
    if len(name) <= max_chars:
        return name
    keep = max_chars - 1
    return "…" + name[-keep:]


def render_dependency_graph_svg(html_files: dict, css_files: dict, js_files: dict,
                                 edges: list) -> str:
    by_kind = {"html": sorted(html_files), "css": sorted(css_files), "js": sorted(js_files)}
    positions: dict = {}
    for kind, paths in by_kind.items():
        x = _GRAPH_COL_X[kind]
        for i, path in enumerate(paths):
            y = _GRAPH_TOP + i * (_GRAPH_NODE_H + _GRAPH_ROW_GAP)
            positions[path] = (x, y, kind)

    max_rows = max((len(v) for v in by_kind.values()), default=0)
    height = _GRAPH_TOP + max(max_rows, 1) * (_GRAPH_NODE_H + _GRAPH_ROW_GAP) + 30
    width = _GRAPH_COL_X["js"] + _GRAPH_NODE_W + 40

    def anchor(path):
        x, y, _ = positions[path]
        return x, y

    def edge_path_d(x1, y1, x2, y2):
        if x2 >= x1:
            sx, sy = x1 + _GRAPH_NODE_W, y1 + _GRAPH_NODE_H / 2
            tx, ty = x2, y2 + _GRAPH_NODE_H / 2
        else:
            sx, sy = x1, y1 + _GRAPH_NODE_H / 2
            tx, ty = x2 + _GRAPH_NODE_W, y2 + _GRAPH_NODE_H / 2
        dx = (tx - sx) * 0.5
        return f"M {sx:.1f},{sy:.1f} C {sx + dx:.1f},{sy:.1f} {tx - dx:.1f},{ty:.1f} {tx:.1f},{ty:.1f}"

    structural_kinds = {"link", "script", "css-import", "js-import", "js-require", "page-link"}
    semantic_kinds = {"dom", "style"}

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" class="dep-graph" role="img" '
        f'aria-label="Карта зависимостей проекта">'
    )
    parts.append("""
    <style>
      .dep-graph text { font-family: var(--font-body); }
      .dep-node rect { stroke-width: 1.4; }
      .dep-node.k-html rect { fill: var(--map-html-bg); stroke: var(--map-html); }
      .dep-node.k-css rect  { fill: var(--map-css-bg);  stroke: var(--map-css); }
      .dep-node.k-js rect   { fill: var(--map-js-bg);   stroke: var(--map-js); }
      .dep-node .dot { }
      .dep-node.k-html .dot { fill: var(--map-html); }
      .dep-node.k-css .dot  { fill: var(--map-css); }
      .dep-node.k-js .dot   { fill: var(--map-js); }
      .dep-node text.fname { font-size: 12px; fill: var(--ink-soft); }
      .edge-structural { stroke: var(--ink-soft); opacity: .38; fill: none; stroke-width: 1.4; }
      .edge-semantic { stroke: var(--map-accent-warm); opacity: .65; fill: none;
                        stroke-width: 1.3; stroke-dasharray: 3 3; }
      .col-title { font-family: var(--font-display); font-size: 13px;
                    letter-spacing: .08em; fill: var(--ink-soft); }
    </style>
    """)

    for kind, x in _GRAPH_COL_X.items():
        parts.append(
            f'<text class="col-title" x="{x}" y="28">{esc(_GRAPH_COL_TITLE[kind].upper())} '
            f'· {len(by_kind[kind])}</text>'
        )

    for e in edges:
        if e.src not in positions or e.dst not in positions:
            continue
        if e.src == e.dst:
            continue
        x1, y1 = anchor(e.src)
        x2, y2 = anchor(e.dst)
        d = edge_path_d(x1, y1, x2, y2)
        css_cls = "edge-semantic" if e.kind in semantic_kinds else "edge-structural"
        if e.kind not in structural_kinds and e.kind not in semantic_kinds:
            continue
        title = esc(f"{e.src} → {e.dst}" + (f" ({e.label})" if e.label else ""))
        parts.append(f'<path class="{css_cls}" d="{d}"><title>{title}</title></path>')

    for path, (x, y, kind) in positions.items():
        label = _truncate_label(path)
        parts.append(
            f'<g class="dep-node k-{kind}" transform="translate({x},{y})">'
            f'<rect width="{_GRAPH_NODE_W}" height="{_GRAPH_NODE_H}" rx="8"></rect>'
            f'<circle class="dot" cx="14" cy="{_GRAPH_NODE_H/2:.0f}" r="4"></circle>'
            f'<text class="fname" x="26" y="{_GRAPH_NODE_H/2 + 4:.0f}">{esc(label)}</text>'
            f'<title>{esc(path)}</title>'
            f'</g>'
        )

    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------
# Встроенные CSS и JS итогового документа ("Атлас проекта").
# Визуальный язык: карта/чертёж кодовой базы — тёмно-чернильный верх,
# холодная "бумага для чертежей" в качестве читаемой зоны, бронзовый и
# бирюзовый (окислившаяся медь/латунь) как два акцентных цвета вместо
# типовой пары "кремовый + терракотовый" или "чёрный + неон".
# Полностью офлайн: без CDN-шрифтов и внешних JS-библиотек — только
# системные шрифтовые стеки и встроенный код.
# --------------------------------------------------------------------------

DOC_CSS = """
:root {
  --ink: #16273f;
  --ink-soft: #3c4f66;
  --paper: #e9edf0;
  --paper-deep: #dbe2e7;
  --paper-line: #c7d1d8;
  --accent: #2f6f62;
  --accent-warm: #b5762f;
  --map-accent-warm: #b5762f;
  --map-html: #b5652d;
  --map-html-bg: #f1e2d4;
  --map-css: #2f6f62;
  --map-css-bg: #dde8e5;
  --map-js: #a9781f;
  --map-js-bg: #f1e7d1;
  --danger: #9c3b3b;
  --font-display: "Iowan Old Style", "Palatino Linotype", Palatino, "URW Palladio L", Georgia, serif;
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-mono: "SF Mono", SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
  --sidebar-w: 308px;
  --topbar-h: 64px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--font-body);
  color: var(--ink);
  background: var(--paper);
  font-size: 15px;
  line-height: 1.55;
}

::selection { background: var(--map-js-bg); color: var(--ink); }

a { color: var(--accent); }
a:hover { color: var(--accent-warm); }

:focus-visible {
  outline: 2px solid var(--accent-warm);
  outline-offset: 2px;
}

/* ---------- Топ-бар ---------- */
.topbar {
  position: sticky; top: 0; z-index: 40;
  height: var(--topbar-h);
  background: var(--ink);
  color: #eef2f4;
  display: flex; align-items: center; gap: 16px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255,255,255,.08);
}
.topbar .brand {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--font-display);
  font-size: 19px;
  white-space: nowrap;
}
.topbar .brand .compass { flex: none; }
.topbar .meta {
  font-size: 12.5px; color: #b9c6d1; white-space: nowrap;
}
.topbar .spacer { flex: 1; }
.topbar .stat-chip {
  font-size: 12px; color: #cfd9e0; border: 1px solid rgba(255,255,255,.18);
  border-radius: 999px; padding: 3px 10px; white-space: nowrap;
}
#doc-search {
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.2);
  color: #fff; border-radius: 8px; padding: 7px 12px;
  font-family: var(--font-body); font-size: 13px; width: 200px;
}
#doc-search::placeholder { color: #93a4b2; }
#doc-search:focus { background: rgba(255,255,255,.14); }

/* ---------- Раскладка ---------- */
.layout { display: flex; align-items: flex-start; }

.sidebar {
  width: var(--sidebar-w); flex: none;
  position: sticky; top: var(--topbar-h);
  height: calc(100vh - var(--topbar-h));
  overflow-y: auto;
  background: var(--paper-deep);
  border-right: 1px solid var(--paper-line);
  padding: 18px 14px 40px;
}
.sidebar .quicknav { list-style: none; margin: 0 0 16px; padding: 0; }
.sidebar .quicknav a {
  display: block; padding: 6px 8px; border-radius: 6px;
  text-decoration: none; color: var(--ink-soft); font-size: 13.5px;
}
.sidebar .quicknav a:hover { background: rgba(0,0,0,.05); color: var(--ink); }

.tree-eyebrow {
  font-size: 11px; letter-spacing: .09em; color: var(--ink-soft);
  text-transform: uppercase; margin: 4px 0 8px 8px; opacity: .75;
}

.tree, .tree ul { list-style: none; margin: 0; padding-left: 16px; }
.tree { padding-left: 0; }
.tree li { position: relative; }
.tree details > summary {
  cursor: pointer; list-style: none; padding: 4px 8px; border-radius: 6px;
  font-size: 13.5px; color: var(--ink); display: flex; align-items: center; gap: 6px;
}
.tree details > summary::-webkit-details-marker { display: none; }
.tree details > summary:hover { background: rgba(0,0,0,.05); }
.tree details > summary::before {
  content: "▸"; display: inline-block; font-size: 10px; color: var(--ink-soft);
  transition: transform .12s ease;
}
.tree details[open] > summary::before { transform: rotate(90deg); }
.tree .file-link {
  display: flex; align-items: center; gap: 7px;
  padding: 4px 8px 4px 22px; border-radius: 6px;
  text-decoration: none; color: var(--ink-soft); font-size: 13.2px;
}
.tree .file-link:hover { background: rgba(0,0,0,.06); color: var(--ink); }
.tree .file-link.active { background: var(--map-js-bg); color: var(--ink); font-weight: 600; }
.tree .dot { width: 7px; height: 7px; border-radius: 50%; flex: none; }
.tree .dot.k-html { background: var(--map-html); }
.tree .dot.k-css  { background: var(--map-css); }
.tree .dot.k-js   { background: var(--map-js); }
.tree .dot.k-other{ background: var(--ink-soft); opacity: .5; }
.tree[data-filtering="true"] li[data-match="false"] { display: none; }

/* ---------- Основной контент ---------- */
.content { flex: 1; min-width: 0; padding: 32px 40px 120px; max-width: 980px; }

h1.doc-title, h2.section-h, h3.file-h {
  font-family: var(--font-display); font-weight: 600; color: var(--ink);
}
h2.section-h {
  font-size: 26px; margin: 64px 0 18px; padding-top: 18px;
  border-top: 1px solid var(--paper-line);
}
.content > h2.section-h:first-child,
.content > section:first-child h2.section-h { margin-top: 0; padding-top: 0; border-top: none; }
.eyebrow {
  font-size: 11.5px; letter-spacing: .1em; text-transform: uppercase;
  color: var(--ink-soft); opacity: .8; margin: 0 0 4px;
}

.lede { font-size: 16px; color: var(--ink-soft); max-width: 62ch; }

.card-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px; margin: 18px 0 28px;
}
.stat-card {
  background: #fff; border: 1px solid var(--paper-line); border-radius: 10px;
  padding: 14px 16px;
}
.stat-card .n { font-family: var(--font-display); font-size: 26px; color: var(--ink); }
.stat-card .l { font-size: 12px; color: var(--ink-soft); }

.legend-row { display: flex; flex-wrap: wrap; gap: 10px; margin: 10px 0 26px; }
.legend-chip {
  display: inline-flex; align-items: center; gap: 7px;
  font-size: 12.5px; padding: 5px 11px; border-radius: 999px;
  border: 1px solid var(--paper-line); background: #fff;
}
.legend-chip .dot { width: 8px; height: 8px; border-radius: 50%; }

.swatch-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 26px; }
.swatch {
  width: 40px; height: 40px; border-radius: 8px; border: 1px solid rgba(0,0,0,.12);
}

.note-block {
  border: 1px solid var(--paper-line); border-left: 4px solid var(--accent-warm);
  background: #fff; border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 14px 0;
}
.note-block h4 {
  margin: 0 0 8px; font-size: 13px; letter-spacing: .04em;
  font-family: var(--font-display); color: var(--ink);
}
.note-block ul { margin: 0; padding-left: 20px; font-size: 13.5px; color: var(--ink-soft); }
.note-block.empty { border-left-color: var(--accent); color: var(--ink-soft); }
.note-block code { font-family: var(--font-mono); font-size: 12.5px; }

.dep-graph-wrap {
  background: #fff; border: 1px solid var(--paper-line); border-radius: 12px;
  padding: 12px; overflow-x: auto; margin: 12px 0 20px;
}
.dep-graph { display: block; min-width: 720px; }
.graph-legend { display: flex; gap: 18px; flex-wrap: wrap; font-size: 12px; color: var(--ink-soft); margin-bottom: 18px; }
.graph-legend .ln { display: inline-flex; align-items: center; gap: 6px; }
.graph-legend .ln svg { flex: none; }

/* ---------- Карточка файла ---------- */
.file-card {
  background: #fff; border: 1px solid var(--paper-line); border-radius: 14px;
  padding: 22px 24px 26px; margin: 0 0 26px; scroll-margin-top: calc(var(--topbar-h) + 12px);
}
.file-card .file-path {
  font-family: var(--font-mono); font-size: 13px; color: var(--ink-soft);
}
.file-card h3.file-h { font-size: 19px; margin: 2px 0 4px; word-break: break-word; }
.file-badges { display: flex; gap: 8px; flex-wrap: wrap; margin: 10px 0 14px; }
.badge {
  font-size: 11px; padding: 3px 9px; border-radius: 999px; font-family: var(--font-mono);
  border: 1px solid var(--paper-line); color: var(--ink-soft);
}
.badge.k-html { border-color: var(--map-html); color: var(--map-html); }
.badge.k-css  { border-color: var(--map-css);  color: var(--map-css); }
.badge.k-js   { border-color: var(--map-js);   color: var(--map-js); }
.badge.warn   { border-color: var(--danger); color: var(--danger); }

.rel-row { display: flex; flex-wrap: wrap; gap: 18px; margin: 4px 0 18px; font-size: 12.8px; }
.rel-row .rel-group strong { display: block; font-size: 10.5px; letter-spacing: .07em;
  text-transform: uppercase; color: var(--ink-soft); opacity: .75; margin-bottom: 5px; font-weight: 600; }
.chip-link {
  display: inline-block; margin: 0 6px 6px 0; padding: 3px 10px; border-radius: 999px;
  background: var(--paper); text-decoration: none; color: var(--ink); font-size: 12px;
  border: 1px solid var(--paper-line);
}
.chip-link:hover { background: var(--map-js-bg); }
.chip-plain {
  display: inline-block; margin: 0 6px 6px 0; padding: 3px 10px; border-radius: 999px;
  background: var(--paper); color: var(--ink-soft); font-size: 12px; border: 1px dashed var(--paper-line);
}

.tabs { margin-top: 6px; }
.tabs input[type="radio"] { position: absolute; opacity: 0; pointer-events: none; }
.tab-labels { display: flex; gap: 4px; border-bottom: 1px solid var(--paper-line); margin-bottom: 14px; }
.tab-labels label {
  cursor: pointer; font-size: 12.5px; padding: 7px 14px; color: var(--ink-soft);
  border-bottom: 2px solid transparent; margin-bottom: -1px;
}
.tab-panel { display: none; }
.tabs input.r-0:checked ~ .tab-panels .tab-panel:nth-child(1) { display: block; }
.tabs input.r-1:checked ~ .tab-panels .tab-panel:nth-child(2) { display: block; }
.tabs input.r-2:checked ~ .tab-panels .tab-panel:nth-child(3) { display: block; }
.tabs input.r-0:checked ~ .tab-labels label.l-0,
.tabs input.r-1:checked ~ .tab-labels label.l-1,
.tabs input.r-2:checked ~ .tab-labels label.l-2 { color: var(--ink); border-bottom-color: var(--accent-warm); font-weight: 600; }

.code-wrap { position: relative; }
.copy-btn {
  position: absolute; top: 8px; right: 8px; z-index: 2;
  font-size: 11px; padding: 4px 10px; border-radius: 6px; cursor: pointer;
  background: var(--ink); color: #eef2f4; border: none; opacity: .75;
  font-family: var(--font-body);
}
.copy-btn:hover { opacity: 1; }
pre.code {
  margin: 0; padding: 16px 18px; border-radius: 10px; overflow-x: auto;
  background: #101d30; color: #d8e2ea; font-family: var(--font-mono);
  font-size: 12.6px; line-height: 1.55; max-height: 520px; overflow-y: auto;
}
pre.code code { white-space: pre; }
.tok-tag { color: #7fb0d8; } .tok-attr { color: #e0b168; } .tok-str { color: #9fca8f; }
.tok-com { color: #6c7f95; font-style: italic; } .tok-doctype { color: #6c7f95; }
.tok-kw { color: #d391c6; } .tok-num { color: #e0a75e; } .tok-fn { color: #7fb0d8; }
.tok-sel { color: #7fb0d8; } .tok-prop { color: #9fca8f; } .tok-var { color: #e0b168; }

.struct-table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 4px 0 18px; }
.struct-table th {
  text-align: left; font-size: 10.5px; letter-spacing: .06em; text-transform: uppercase;
  color: var(--ink-soft); opacity: .75; padding: 6px 10px; border-bottom: 1px solid var(--paper-line);
}
.struct-table td { padding: 7px 10px; border-bottom: 1px solid var(--paper); vertical-align: top; }
.struct-table code { font-family: var(--font-mono); font-size: 12px; background: var(--paper);
  padding: 1px 5px; border-radius: 4px; }
.struct-sub-h { font-size: 12px; letter-spacing: .05em; text-transform: uppercase;
  color: var(--ink-soft); opacity: .8; margin: 20px 0 6px; }
.kss-comment { font-size: 12.5px; color: var(--ink-soft); margin: 2px 0 4px; }
.muted { color: var(--ink-soft); opacity: .8; font-size: 13px; }
.doc-desc { font-size: 13px; color: var(--ink-soft); margin: 2px 0 6px; }
.func-sig { font-family: var(--font-mono); font-size: 12.8px; color: var(--ink); }
.func-block { padding: 10px 0; border-top: 1px solid var(--paper); }
.func-block:first-child { border-top: none; }
.param-list { margin: 4px 0 0; padding-left: 18px; font-size: 12.5px; color: var(--ink-soft); }

footer.doc-footer {
  padding: 30px 40px 60px; color: var(--ink-soft); font-size: 12.5px;
}

@media (max-width: 880px) {
  .sidebar { position: fixed; left: -100%; transition: left .18s ease; z-index: 50;
    box-shadow: 8px 0 24px rgba(0,0,0,.2); }
  .sidebar.open { left: 0; }
  .content { padding: 24px 18px 100px; }
  #doc-search { width: 130px; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .tree details > summary::before, .sidebar { transition: none; }
}

@media print {
  .sidebar, .topbar, .copy-btn { display: none; }
  .content { max-width: none; padding: 0; }
  pre.code { max-height: none; }
}
"""


DOC_JS = """
(function () {
  "use strict";

  // ---- Поиск/фильтр по дереву файлов и разделам ----
  var searchInput = document.getElementById("doc-search");
  var tree = document.querySelector(".tree");
  if (searchInput && tree) {
    searchInput.addEventListener("input", function () {
      var q = searchInput.value.trim().toLowerCase();
      var items = tree.querySelectorAll("li[data-name]");
      if (!q) {
        tree.setAttribute("data-filtering", "false");
        items.forEach(function (li) { li.removeAttribute("data-match"); });
        return;
      }
      tree.setAttribute("data-filtering", "true");
      items.forEach(function (li) {
        var name = li.getAttribute("data-name") || "";
        var match = name.indexOf(q) !== -1;
        li.setAttribute("data-match", match ? "true" : "false");
        if (match) {
          var p = li.parentElement;
          while (p) {
            var details = p.closest ? p.closest("details") : null;
            if (!details) break;
            details.open = true;
            p = details.parentElement;
          }
        }
      });
    });
  }

  // ---- Подсветка активного файла в сайдбаре при прокрутке (scrollspy) ----
  var fileLinks = Array.prototype.slice.call(document.querySelectorAll(".tree .file-link"));
  var sections = fileLinks
    .map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); })
    .filter(Boolean);

  if (sections.length && "IntersectionObserver" in window) {
    var byId = {};
    fileLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = byId[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          fileLinks.forEach(function (a) { a.classList.remove("active"); });
          link.classList.add("active");
          var details = link.closest("details");
          while (details) {
            details.open = true;
            details = details.parentElement ? details.parentElement.closest("details") : null;
          }
        }
      });
    }, { rootMargin: "-15% 0px -70% 0px", threshold: 0 });

    sections.forEach(function (s) { observer.observe(s); });
  }

  // ---- Копирование кода ----
  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var pre = btn.parentElement.querySelector("pre.code");
      if (!pre) return;
      var text = pre.textContent;
      var done = function () {
        var old = btn.textContent;
        btn.textContent = "Скопировано";
        setTimeout(function () { btn.textContent = old; }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(done);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    });
  });

  // ---- Мобильное меню ----
  var toggle = document.getElementById("sidebar-toggle");
  var sidebar = document.querySelector(".sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", function () { sidebar.classList.toggle("open"); });
    sidebar.querySelectorAll(".file-link").forEach(function (a) {
      a.addEventListener("click", function () { sidebar.classList.remove("open"); });
    });
  }
})();
"""


# --------------------------------------------------------------------------
# Сборка HTML-фрагментов документа
# --------------------------------------------------------------------------

COMPASS_SVG = (
    '<svg class="compass" width="26" height="26" viewBox="0 0 26 26" '
    'aria-hidden="true"><circle cx="13" cy="13" r="11.5" fill="none" '
    'stroke="#8a9bab" stroke-width="1" opacity=".55"/>'
    '<path d="M13,2 L15.8,10.2 L24,13 L15.8,15.8 L13,24 L10.2,15.8 L2,13 L10.2,10.2 Z" '
    'fill="#b5762f"/><circle cx="13" cy="13" r="1.6" fill="#eef2f4"/></svg>'
)


def _tree_node_html(node: TreeNode, depth: int = 0) -> str:
    if node.is_dir:
        children_html = "".join(_tree_node_html(c, depth + 1) for c in node.children)
        open_attr = " open" if depth < 1 else ""
        return (
            f'<li data-name="{esc(node.name.lower())}">'
            f'<details{open_attr}><summary>{esc(node.name)}/</summary>'
            f'<ul>{children_html}</ul></details></li>'
        )
    slug = slugify(node.rel_path)
    if node.kind in ("html", "css", "js"):
        return (
            f'<li data-name="{esc(node.rel_path.lower())}">'
            f'<a class="file-link" href="#{slug}">'
            f'<span class="dot k-{node.kind}"></span>{esc(node.name)}</a></li>'
        )
    return (
        f'<li data-name="{esc(node.rel_path.lower())}">'
        f'<span class="file-link" style="cursor:default;opacity:.55">'
        f'<span class="dot k-other"></span>{esc(node.name)}</span></li>'
    )


def build_sidebar_tree(tree: TreeNode) -> str:
    inner = "".join(_tree_node_html(c, 0) for c in tree.children)
    return f'<ul class="tree" id="file-tree">{inner}</ul>'


_STRUCTURAL_EDGE_KINDS = {"link", "script", "css-import", "js-import", "js-require",
                           "external", "page-link"}
_SEMANTIC_EDGE_KINDS = {"dom", "style"}


def _relations_for(path: str, edges: list, all_paths: set):
    """Возвращает (structural_out, structural_in, semantic_out, semantic_in).
    Структурные связи (link/script/import/require/переходы между страницами)
    показываются как "Зависит от / Используется в". Смысловые DOM-связи
    (JS обращается к элементу, CSS нацелен на класс) показываются отдельно —
    это не "зависимость" в смысле загрузки файла, а то, какие HTML-элементы
    файл фактически затрагивает."""
    structural_out, structural_in = [], []
    semantic_out, semantic_in = [], []
    seen = set()
    for e in edges:
        if e.src == path and e.dst not in (path, "?"):
            key = ("out", e.dst, e.kind)
            if key in seen:
                continue
            seen.add(key)
            if e.kind in _STRUCTURAL_EDGE_KINDS:
                if e.kind == "external":
                    structural_out.append((e.dst, None, e.kind))
                elif e.dst in all_paths:
                    structural_out.append((e.dst, slugify(e.dst), e.kind))
            elif e.kind in _SEMANTIC_EDGE_KINDS and e.dst in all_paths:
                semantic_out.append((e.dst, slugify(e.dst), e.kind))
        if e.dst == path and e.src != path:
            key = ("in", e.src, e.kind)
            if key in seen:
                continue
            seen.add(key)
            if e.kind in _STRUCTURAL_EDGE_KINDS:
                structural_in.append((e.src, slugify(e.src), e.kind))
            elif e.kind in _SEMANTIC_EDGE_KINDS:
                semantic_in.append((e.src, slugify(e.src), e.kind))
    # убираем повторы файлов при сохранении порядка появления
    def dedup(items):
        out, seen_names = [], set()
        for it in items:
            if it[0] in seen_names:
                continue
            seen_names.add(it[0])
            out.append(it)
        return out
    return (dedup(structural_out), dedup(structural_in),
            dedup(semantic_out), dedup(semantic_in))


def _rel_row_html(structural_out: list, structural_in: list,
                   semantic_out: list = (), semantic_in: list = (),
                   semantic_out_label: str = "Затрагивает элементы в",
                   semantic_in_label: str = "Стилизуется / скриптуется в") -> str:
    def chips(items):
        out = []
        for name, href, kind in items:
            if href:
                out.append(f'<a class="chip-link" href="#{href}">{esc(name)}</a>')
            else:
                out.append(f'<span class="chip-plain">{esc(name)}</span>')
        return "".join(out) if out else '<span class="muted">—</span>'

    html = (
        '<div class="rel-row">'
        f'<div class="rel-group"><strong>Зависит от</strong>{chips(structural_out)}</div>'
        f'<div class="rel-group"><strong>Используется в</strong>{chips(structural_in)}</div>'
        "</div>"
    )
    if semantic_out or semantic_in:
        html += '<div class="rel-row">'
        if semantic_out:
            html += f'<div class="rel-group"><strong>{esc(semantic_out_label)}</strong>{chips(semantic_out)}</div>'
        if semantic_in:
            html += f'<div class="rel-group"><strong>{esc(semantic_in_label)}</strong>{chips(semantic_in)}</div>'
        html += "</div>"
    return html


def _badges_html(kind: str, info) -> str:
    badges = [f'<span class="badge k-{kind}">{kind.upper()}</span>']
    badges.append(f'<span class="badge">{human_size(info.size)}</span>')
    badges.append(f'<span class="badge">{info.loc} строк</span>')
    if info.is_minified:
        badges.append('<span class="badge warn">минифицирован</span>')
    return '<div class="file-badges">' + "".join(badges) + "</div>"


def _tabs_open(slug: str, labels: list) -> str:
    radios = "".join(
        f'<input class="r-{i}" type="radio" name="tabs-{slug}" id="tab-{i}-{slug}"'
        f'{" checked" if i == 0 else ""}>'
        for i in range(len(labels))
    )
    label_tags = "".join(
        f'<label class="l-{i}" for="tab-{i}-{slug}">{esc(lbl)}</label>'
        for i, lbl in enumerate(labels)
    )
    return f'<div class="tabs">{radios}<div class="tab-labels">{label_tags}</div><div class="tab-panels">'


_TABS_CLOSE = "</div></div>"


def _code_panel(slug: str, raw: str, kind: str) -> str:
    if len(raw) > MINIFIED_MAX_FILE_FOR_FULL_DUMP:
        shown = raw[:MINIFIED_MAX_FILE_FOR_FULL_DUMP]
        note = (f'<p class="muted">Файл большой ({human_size(len(raw))}) — показаны первые '
                f'{MINIFIED_MAX_FILE_FOR_FULL_DUMP} симв.</p>')
    else:
        shown, note = raw, ""
    highlighted = highlight_by_kind(shown, kind)
    return (
        '<div class="tab-panel">' + note +
        '<div class="code-wrap"><button class="copy-btn" type="button">Копировать</button>'
        f'<pre class="code"><code>{highlighted}</code></pre></div></div>'
    )


def _struct_panel_html(info: HtmlInfo) -> str:
    parts = ['<div class="tab-panel">']

    meta_rows = [
        ("Заголовок (&lt;title&gt;)", info.title or "—"),
        ("lang", info.lang or "—"),
        ("meta description", info.meta_description or "—"),
        ("DOCTYPE", "есть" if info.doctype_ok else "отсутствует"),
        ("Слов в тексте", str(info.word_count)),
    ]
    parts.append('<table class="struct-table"><tbody>')
    for label, val in meta_rows:
        parts.append(f"<tr><th>{label}</th><td>{esc(val)}</td></tr>")
    parts.append("</tbody></table>")

    if info.landmarks:
        chips = "".join(f'<span class="chip-plain">&lt;{esc(t)}&gt;</span>'
                         for t in sorted(info.landmarks))
        parts.append(f'<div class="struct-sub-h">Семантические landmark-теги</div><div>{chips}</div>')

    if info.headings:
        parts.append('<div class="struct-sub-h">Структура заголовков</div>')
        parts.append('<table class="struct-table"><thead><tr><th>Уровень</th><th>Текст</th></tr></thead><tbody>')
        for level, text in info.headings[:40]:
            indent = "&nbsp;" * ((level - 1) * 3)
            parts.append(f"<tr><td><code>h{level}</code></td><td>{indent}{esc(text)}</td></tr>")
        parts.append("</tbody></table>")

    if info.forms:
        parts.append('<div class="struct-sub-h">Формы</div>')
        parts.append('<table class="struct-table"><thead><tr><th>action</th><th>method</th><th>поля</th></tr></thead><tbody>')
        for f in info.forms:
            fields = ", ".join(f["fields"]) or "—"
            parts.append(f"<tr><td><code>{esc(f['action'] or '(текущая страница)')}</code></td>"
                         f"<td><code>{esc(f['method'])}</code></td><td>{esc(fields)}</td></tr>")
        parts.append("</tbody></table>")

    if info.images:
        no_alt = sum(1 for i in info.images if not i.get("alt"))
        parts.append(f'<div class="struct-sub-h">Изображения ({len(info.images)}'
                      + (f", из них без alt: {no_alt}" if no_alt else "") + ")</div>")
        parts.append('<table class="struct-table"><thead><tr><th>src</th><th>alt</th></tr></thead><tbody>')
        for img in info.images[:30]:
            alt = img.get("alt") or ""
            alt_html = esc(alt) if alt else '<span class="badge warn">нет alt</span>'
            parts.append(f"<tr><td><code>{esc(img.get('src',''))}</code></td><td>{alt_html}</td></tr>")
        parts.append("</tbody></table>")

    if info.ids or info.classes:
        parts.append('<div class="struct-sub-h">id / class на странице</div>')
        id_chips = "".join(f'<span class="chip-plain">#{esc(i)}</span>' for i in sorted(info.ids)[:40])
        class_chips = "".join(f'<span class="chip-plain">.{esc(c)}</span>' for c in sorted(info.classes)[:60])
        parts.append(f"<div>{id_chips}</div><div style='margin-top:6px'>{class_chips}</div>")

    if info.comments:
        parts.append('<div class="struct-sub-h">Комментарии в разметке</div><ul class="param-list">')
        for c in info.comments[:20]:
            c_short = c if len(c) < 160 else c[:160] + "…"
            parts.append(f"<li>{esc(c_short)}</li>")
        parts.append("</ul>")

    if info.hrefs_external:
        chips = "".join(f'<span class="chip-plain">{esc(h)}</span>' for h in info.hrefs_external[:20])
        parts.append(f'<div class="struct-sub-h">Внешние ссылки</div><div>{chips}</div>')

    parts.append("</div>")
    return "".join(parts)


def build_file_card_html(path: str, info: HtmlInfo, edges: list, all_paths: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(info.title or path)}</h3>'
        + _badges_html("html", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Ссылается на страницы",
                        semantic_in_label="Стилизуется / скриптуется из")
    )
    tabs = _tabs_open(slug, ["Код", "Структура"])
    body = _code_panel(slug, info.raw, "html") + _struct_panel_html(info)
    return header + tabs + body + _TABS_CLOSE + "</article>"


def _color_swatch(color: str) -> str:
    safe = esc(color)
    try:
        style = f"background:{safe}"
    except Exception:
        style = ""
    return f'<span class="swatch" data-label="{safe}" style="{style}" title="{safe}"></span>'


def _struct_panel_css(info: CssInfo) -> str:
    parts = ['<div class="tab-panel">']

    nested_count = sum(len(a.nested_rules) for a in info.at_rules)
    top_rows = [
        ("Правил всего (включая вложенные в @media)", str(len(info.rules) + nested_count)),
        ("At-правил (@media/@keyframes/…)", str(len(info.at_rules))),
        ("Импортов (@import)", str(len(info.imports)) if info.imports else "0"),
    ]
    parts.append('<table class="struct-table"><tbody>')
    for label, val in top_rows:
        parts.append(f"<tr><th>{label}</th><td>{esc(val)}</td></tr>")
    parts.append("</tbody></table>")

    if info.custom_props_defined:
        parts.append('<div class="struct-sub-h">CSS custom properties, определённые здесь</div>')
        parts.append('<table class="struct-table"><thead><tr><th>Свойство</th><th>Значение</th></tr></thead><tbody>')
        for name, value in info.custom_props_defined.items():
            swatch = _color_swatch(value) if _COLOR_RE.match(value.strip()) else ""
            parts.append(f"<tr><td><code>{esc(name)}</code></td><td>{swatch} <code>{esc(value)}</code></td></tr>")
        parts.append("</tbody></table>")

    if info.breakpoints:
        chips = "".join(f'<span class="chip-plain">{esc(b)}</span>' for b in sorted(info.breakpoints))
        parts.append(f'<div class="struct-sub-h">Медиа-брейкпоинты</div><div>{chips}</div>')

    at_by_kind: dict = {}
    for a in info.at_rules:
        if a.kind in ("media", "import"):
            continue
        at_by_kind.setdefault(a.kind, []).append(a.prelude)
    for kind, items in at_by_kind.items():
        chips = "".join(f'<span class="chip-plain">{esc(p)}</span>' for p in items[:20])
        parts.append(f'<div class="struct-sub-h">@{esc(kind)}</div><div>{chips}</div>')

    all_rules_with_ctx = [(r, None) for r in info.rules]
    for a in info.at_rules:
        for r in a.nested_rules:
            all_rules_with_ctx.append((r, a.prelude))

    if all_rules_with_ctx:
        cap = 80
        parts.append(f'<div class="struct-sub-h">Правила '
                      f'({len(all_rules_with_ctx)}{" — показаны первые " + str(cap) if len(all_rules_with_ctx) > cap else ""})</div>')
        for rule, ctx in all_rules_with_ctx[:cap]:
            sel_html = ", ".join(f"<code>{esc(s)}</code>" for s in rule.selectors)
            ctx_html = f' <span class="muted">внутри {esc(ctx)}</span>' if ctx else ""
            comment_html = f'<div class="kss-comment">{esc(rule.comment)}</div>' if rule.comment else ""
            decls_preview = "; ".join(f"{p}: {v}" for p, v in rule.declarations[:5])
            more = "; …" if len(rule.declarations) > 5 else ""
            parts.append(
                '<div class="func-block">'
                f'<div class="func-sig">{sel_html}{ctx_html}</div>'
                f"{comment_html}"
                f'<div class="doc-desc"><code>{esc(decls_preview)}{esc(more)}</code></div>'
                "</div>"
            )

    if info.unmatched_selectors:
        chips = "".join(f'<span class="chip-plain">.{esc(s)}</span>' for s in info.unmatched_selectors[:30])
        parts.append(
            '<div class="note-block"><h4>Заметка картографа</h4>'
            "<p class='muted' style='margin:0 0 8px'>Эти классы/id используются в селекторах файла, "
            "но не найдены ни в одном HTML-файле проекта. Возможно, элементы добавляются "
            f"динамически через JS, либо это остатки неиспользуемого кода.</p><div>{chips}</div></div>"
        )

    parts.append("</div>")
    return "".join(parts)


def build_file_card_css(path: str, info: CssInfo, edges: list, all_paths: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(path.split("/")[-1])}</h3>'
        + _badges_html("css", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Применяется на страницах",
                        semantic_in_label="")
    )
    tabs = _tabs_open(slug, ["Код", "Структура"])
    body = _code_panel(slug, info.raw, "css") + _struct_panel_css(info)
    return header + tabs + body + _TABS_CLOSE + "</article>"


def _doc_block_html(doc: Optional[dict]) -> str:
    if not doc:
        return ""
    out = []
    if doc.get("description"):
        out.append(f'<div class="doc-desc">{esc(doc["description"])}</div>')
    if doc.get("params"):
        out.append('<ul class="param-list">')
        for name, desc in doc["params"].items():
            out.append(f"<li><code>{esc(name)}</code> — {esc(desc)}</li>")
        out.append("</ul>")
    if doc.get("returns"):
        out.append(f'<div class="doc-desc"><em>Возвращает:</em> {esc(doc["returns"])}</div>')
    for ex in doc.get("examples", []):
        out.append(f'<pre class="code" style="margin-top:6px"><code>{esc(ex)}</code></pre>')
    return "".join(out)


def _func_block_html(fn: JsFunctionInfo) -> str:
    params = ", ".join(fn.params)
    exported = ' <span class="badge">export</span>' if fn.is_exported else ""
    kind_label = {"function": "function", "arrow": "const (arrow)",
                  "method": "method", "constructor": "constructor"}.get(fn.kind, fn.kind)
    return (
        '<div class="func-block">'
        f'<div class="func-sig">{esc(kind_label)} <strong>{esc(fn.name)}</strong>({esc(params)})'
        f' <span class="muted">· строка {fn.line}</span>{exported}</div>'
        + _doc_block_html(fn.doc) +
        "</div>"
    )


def _struct_panel_js(info: JsInfo) -> str:
    parts = ['<div class="tab-panel">']

    if info.top_comment:
        parts.append(f'<div class="doc-desc">{esc(info.top_comment)}</div>')

    if info.imports or info.requires:
        parts.append('<div class="struct-sub-h">Импорты</div>')
        parts.append('<table class="struct-table"><thead><tr><th>Откуда</th><th>Что</th></tr></thead><tbody>')
        for imp in info.imports:
            names = imp.get("names") or []
            label = imp.get("namespace") and f"* as {imp['namespace']}" or \
                (", ".join(filter(None, [imp.get("default_name")] + names)) or "(побочный эффект)")
            dyn = " <span class='badge'>dynamic</span>" if imp.get("dynamic") else ""
            parts.append(f"<tr><td><code>{esc(imp['source'])}</code></td><td>{esc(label)}{dyn}</td></tr>")
        for req in info.requires:
            parts.append(f"<tr><td><code>{esc(req)}</code></td><td>require()</td></tr>")
        parts.append("</tbody></table>")

    if info.exports:
        chips = "".join(f'<span class="chip-plain">{esc(e)}</span>' for e in info.exports)
        parts.append(f'<div class="struct-sub-h">Экспорты</div><div>{chips}</div>')

    if info.functions:
        parts.append(f'<div class="struct-sub-h">Функции ({len(info.functions)})</div>')
        for fn in info.functions:
            parts.append(_func_block_html(fn))

    if info.classes:
        parts.append(f'<div class="struct-sub-h">Классы ({len(info.classes)})</div>')
        for cls in info.classes:
            extends = f" extends {esc(cls.extends)}" if cls.extends else ""
            parts.append(
                '<div class="func-block">'
                f'<div class="func-sig">class <strong>{esc(cls.name)}</strong>{extends} '
                f'<span class="muted">· строка {cls.line}</span></div>'
                + _doc_block_html(cls.doc)
            )
            for m in cls.methods:
                parts.append(
                    '<div style="margin-left:16px;border-top:1px dashed var(--paper-line);padding-top:8px">'
                    + _func_block_html(m) + "</div>"
                )
            parts.append("</div>")

    if info.dom_queries:
        parts.append('<div class="struct-sub-h">Обращения к DOM</div>')
        parts.append('<table class="struct-table"><thead><tr><th>Метод</th><th>Селектор</th><th>Строка</th></tr></thead><tbody>')
        for q in info.dom_queries:
            parts.append(f"<tr><td><code>{esc(q['method'])}</code></td>"
                         f"<td><code>{esc(q['selector'])}</code></td><td>{q['line']}</td></tr>")
        parts.append("</tbody></table>")

    if info.event_listeners:
        parts.append('<div class="struct-sub-h">Обработчики событий</div>')
        parts.append('<table class="struct-table"><thead><tr><th>Цель</th><th>Событие</th><th>Строка</th></tr></thead><tbody>')
        for ev in info.event_listeners:
            parts.append(f"<tr><td><code>{esc(ev['target'])}</code></td>"
                         f"<td><code>{esc(ev['event'])}</code></td><td>{ev['line']}</td></tr>")
        parts.append("</tbody></table>")

    if info.network_calls:
        chips = "".join(f'<span class="chip-plain">{esc(c["kind"])} · строка {c["line"]}</span>'
                         for c in info.network_calls)
        parts.append(f'<div class="struct-sub-h">Сетевые вызовы</div><div>{chips}</div>')

    if info.todos:
        parts.append('<div class="note-block"><h4>TODO / FIXME</h4><ul>')
        for t in info.todos:
            parts.append(f"<li><code>{esc(t['marker'])}</code> (строка {t['line']}): {esc(t['text'])}</li>")
        parts.append("</ul></div>")

    if not any([info.imports, info.requires, info.exports, info.functions,
                info.classes, info.dom_queries, info.event_listeners]):
        parts.append('<p class="muted">Явной структуры (функций, классов, импортов) не обнаружено.</p>')

    parts.append("</div>")
    return "".join(parts)


def build_file_card_js(path: str, info: JsInfo, edges: list, all_paths: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(path.split("/")[-1])}</h3>'
        + _badges_html("js", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Управляет элементами на",
                        semantic_in_label="")
    )
    tabs = _tabs_open(slug, ["Код", "Структура"])
    body = _code_panel(slug, info.raw, "js") + _struct_panel_js(info)
    return header + tabs + body + _TABS_CLOSE + "</article>"


def build_overview_section(pdata: "ProjectData") -> str:
    s = pdata.stats
    counts = s["counts"]
    parts = ['<section id="overview">']
    parts.append('<h2 class="section-h">Обзор проекта</h2>')
    parts.append(
        '<p class="lede">Автоматически собранная карта проекта: '
        f'{counts["html"]} HTML, {counts["css"]} CSS и {counts["js"]} JS файлов, '
        f'{human_size(s["total_size"])} исходного кода, {s["total_loc"]} непустых строк.</p>'
    )

    parts.append('<div class="card-grid">')
    for label, val in [
        ("HTML-файлов", counts["html"]), ("CSS-файлов", counts["css"]),
        ("JS-файлов", counts["js"]), ("Прочих файлов", counts["other"]),
        ("Строк кода", s["total_loc"]), ("Общий размер", human_size(s["total_size"])),
    ]:
        parts.append(f'<div class="stat-card"><div class="n">{val}</div><div class="l">{label}</div></div>')
    parts.append("</div>")

    parts.append(
        '<div class="legend-row">'
        '<span class="legend-chip"><span class="dot" style="background:var(--map-html)"></span>HTML</span>'
        '<span class="legend-chip"><span class="dot" style="background:var(--map-css)"></span>CSS</span>'
        '<span class="legend-chip"><span class="dot" style="background:var(--map-js)"></span>JS</span>'
        "</div>"
    )

    if s["largest_files"]:
        parts.append('<div class="struct-sub-h">Крупнейшие файлы</div>')
        parts.append('<table class="struct-table"><thead><tr><th>Файл</th><th>Размер</th><th>Строк</th></tr></thead><tbody>')
        for path, size, loc, kind in s["largest_files"]:
            parts.append(f'<tr><td><a href="#{slugify(path)}"><code>{esc(path)}</code></a></td>'
                         f"<td>{human_size(size)}</td><td>{loc}</td></tr>")
        parts.append("</tbody></table>")

    if s["palette"]:
        parts.append('<div class="struct-sub-h">Цветовая палитра (по частоте использования в CSS)</div>')
        parts.append('<div class="swatch-row">')
        for color, _count in s["palette"]:
            parts.append(_color_swatch(color))
        parts.append("</div>")

    if s["breakpoints"]:
        chips = "".join(f'<span class="chip-plain">{esc(b)}</span>' for b in s["breakpoints"])
        parts.append(f'<div class="struct-sub-h">Адаптивные брейкпоинты</div><div>{chips}</div>')

    if s["external_libs"]:
        chips = "".join(f'<span class="chip-plain">{esc(lib)}</span>' for lib in s["external_libs"])
        parts.append(f'<div class="struct-sub-h">Внешние библиотеки / CDN</div><div>{chips}</div>')

    notes = []
    if s["unused_ids"] or s["unused_classes"]:
        items = [f"#{i}" for i in s["unused_ids"][:15]] + [f".{c}" for c in s["unused_classes"][:25]]
        more = len(s["unused_ids"]) + len(s["unused_classes"]) - len(items)
        notes.append(("Неиспользуемые id / class",
                      "Заданы в HTML, но ни разу не встречены в CSS-селекторах или JS-запросах к DOM. "
                      "Возможно, задел на будущее или остаток рефакторинга.",
                      items, more))
    if s["orphan_css_selectors"]:
        items = [f'{o["file"]}: .{o["token"]}' for o in s["orphan_css_selectors"][:20]]
        more = len(s["orphan_css_selectors"]) - len(items)
        notes.append(("CSS-правила без соответствия в HTML",
                      "Селекторы нацелены на классы/id, которых нет ни на одной странице проекта.",
                      items, more))
    if s["unresolved_links"]:
        items = [f'{u["src"]} → {u["dst"]}' for u in s["unresolved_links"][:20]]
        more = len(s["unresolved_links"]) - len(items)
        notes.append(("Неразрешённые ссылки",
                      "Путь в href/src не удалось сопоставить ни с одним файлом проекта — возможно, опечатка.",
                      items, more))
    if s["images_no_alt"]:
        items = [f'{i["file"]}: {i["src"]}' for i in s["images_no_alt"][:20]]
        more = len(s["images_no_alt"]) - len(items)
        notes.append(("Изображения без alt",
                      "Влияет на доступность (screen readers) и SEO.",
                      items, more))
    if s["todos"]:
        items = [f'{t["file"]}:{t["line"]} — {t["text"]}' for t in s["todos"][:20]]
        more = len(s["todos"]) - len(items)
        notes.append(("TODO / FIXME по проекту", "", items, more))

    if notes:
        parts.append('<div class="struct-sub-h">Заметки картографа</div>')
        for title, desc, items, more in notes:
            parts.append('<div class="note-block"><h4>' + esc(title) + "</h4>")
            if desc:
                parts.append(f"<p class='muted' style='margin:0 0 8px'>{esc(desc)}</p>")
            parts.append("<ul>" + "".join(f"<li><code>{esc(i)}</code></li>" for i in items) + "</ul>")
            if more > 0:
                parts.append(f'<p class="muted" style="margin:6px 0 0">…и ещё {more}.</p>')
            parts.append("</div>")
    else:
        parts.append(
            '<div class="note-block empty"><h4>Заметки картографа</h4>'
            "<p class='muted' style='margin:0'>Явных нестыковок между HTML, CSS и JS не найдено.</p></div>"
        )

    parts.append("</section>")
    return "".join(parts)


_GRAPH_LEGEND_SVG = (
    '<span class="ln"><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" '
    'stroke="var(--ink-soft)" stroke-width="1.6" opacity=".5"/></svg>структурная связь '
    "(link/script/import)</span>"
    '<span class="ln"><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" '
    'stroke="var(--map-accent-warm)" stroke-width="1.4" stroke-dasharray="3 3"/></svg>'
    "смысловая связь (DOM id/class)</span>"
)


def build_dependency_section(pdata: "ProjectData") -> str:
    svg = render_dependency_graph_svg(pdata.html_files, pdata.css_files, pdata.js_files, pdata.edges)
    return (
        '<section id="dependency-map">'
        '<h2 class="section-h">Карта зависимостей</h2>'
        '<p class="lede">Сплошные линии — прямые ссылки (&lt;link&gt;, &lt;script&gt;, import/require). '
        "Пунктирные — смысловые связи через DOM: какой JS/CSS обращается к каким элементам HTML.</p>"
        f'<div class="graph-legend">{_GRAPH_LEGEND_SVG}</div>'
        f'<div class="dep-graph-wrap">{svg}</div>'
        "</section>"
    )


# --------------------------------------------------------------------------
# Финальная сборка одного HTML-файла документации (шаблон с плейсхолдерами)
# --------------------------------------------------------------------------

DOCUMENT_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>__STYLES__</style>
</head>
<body>
<header class="topbar">
  <button id="sidebar-toggle" aria-label="Меню" style="background:none;border:none;color:#fff;font-size:18px;display:none">☰</button>
  <div class="brand">__COMPASS__<span>__PROJECT_NAME__</span></div>
  <span class="meta">сгенерировано __GENERATED_AT__</span>
  <div class="spacer"></div>
  __STAT_CHIPS__
  <input id="doc-search" type="search" placeholder="Поиск по файлам…" aria-label="Поиск по файлам">
</header>
<div class="layout">
  <nav class="sidebar" aria-label="Навигация по проекту">
    <ul class="quicknav">
      <li><a href="#overview">Обзор проекта</a></li>
      <li><a href="#dependency-map">Карта зависимостей</a></li>
    </ul>
    <div class="tree-eyebrow">Файлы проекта</div>
    __SIDEBAR_TREE__
  </nav>
  <main class="content">
    __OVERVIEW__
    __DEPENDENCY_MAP__
    <h2 class="section-h">Файлы</h2>
    __FILE_SECTIONS__
  </main>
</div>
<footer class="doc-footer">
  Документация сгенерирована автоматически скриптом doc_generator.py v__VERSION__ — статический анализ,
  без выполнения кода проекта. Часть выводов (назначение функций, категории) основана на эвристиках
  и комментариях в исходном коде и может быть неточной.
</footer>
<script>__SCRIPTS__</script>
</body>
</html>
"""


def render_document(pdata: "ProjectData", project_title: str) -> str:
    counts = pdata.stats["counts"]
    stat_chips = "".join(
        f'<span class="stat-chip">{v} {label}</span>'
        for label, v in [("HTML", counts["html"]), ("CSS", counts["css"]), ("JS", counts["js"])]
    )

    all_paths = set(pdata.html_files) | set(pdata.css_files) | set(pdata.js_files)

    file_sections = []
    for path in sorted(pdata.html_files):
        file_sections.append(build_file_card_html(path, pdata.html_files[path], pdata.edges, all_paths))
    for path in sorted(pdata.css_files):
        file_sections.append(build_file_card_css(path, pdata.css_files[path], pdata.edges, all_paths))
    for path in sorted(pdata.js_files):
        file_sections.append(build_file_card_js(path, pdata.js_files[path], pdata.edges, all_paths))

    html = DOCUMENT_TEMPLATE
    html = html.replace("__TITLE__", esc(project_title))
    html = html.replace("__STYLES__", DOC_CSS)
    html = html.replace("__COMPASS__", COMPASS_SVG)
    html = html.replace("__PROJECT_NAME__", esc(project_title))
    html = html.replace("__GENERATED_AT__", esc(pdata.generated_at))
    html = html.replace("__STAT_CHIPS__", stat_chips)
    html = html.replace("__SIDEBAR_TREE__", build_sidebar_tree(pdata.tree))
    html = html.replace("__OVERVIEW__", build_overview_section(pdata))
    html = html.replace("__DEPENDENCY_MAP__", build_dependency_section(pdata))
    html = html.replace("__FILE_SECTIONS__", "".join(file_sections))
    html = html.replace("__VERSION__", VERSION)
    html = html.replace("__SCRIPTS__", DOC_JS)
    return html


# --------------------------------------------------------------------------
# Оркестрация: сборка ProjectData целиком
# --------------------------------------------------------------------------

def build_project_data(root: Path, ignore_dirs: set, extra_ignore_globs: list) -> "ProjectData":
    tree, html_paths, css_paths, js_paths, other_paths = scan_project(root, ignore_dirs, extra_ignore_globs)

    html_files = {p: analyze_html(p, read_text_safe(root / p)) for p in html_paths}
    css_files = {p: analyze_css(p, read_text_safe(root / p)) for p in css_paths}
    js_files = {p: analyze_js(p, read_text_safe(root / p)) for p in js_paths}

    edges, used_tokens = build_edges(html_files, css_files, js_files)
    stats = analyze_project_stats(html_files, css_files, js_files, other_paths, edges, used_tokens)

    return ProjectData(
        root_name=root.name,
        generated_at=datetime.now().strftime("%d.%m.%Y %H:%M"),
        tree=tree,
        html_files=html_files,
        css_files=css_files,
        js_files=js_files,
        other_files=other_paths,
        edges=edges,
        stats=stats,
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="doc_generator.py",
        description="Генерирует единый HTML-файл документации для фронтенд-проекта (HTML/CSS/JS).",
    )
    parser.add_argument("project_dir", help="Путь к корню фронтенд-проекта")
    parser.add_argument("-o", "--output", default="documentation.html",
                         help="Путь к результирующему HTML-файлу (по умолчанию: documentation.html)")
    parser.add_argument("--title", default=None,
                         help="Название проекта в документации (по умолчанию — имя папки)")
    parser.add_argument("--ignore", action="append", default=[],
                         help="Дополнительный glob-паттерн для исключения файлов (можно указывать несколько раз)")
    parser.add_argument("--no-default-ignore", action="store_true",
                         help="Не исключать стандартные технические папки (node_modules, .git и т.п.)")
    args = parser.parse_args(argv)

    root = Path(args.project_dir).resolve()
    if not root.is_dir():
        print(f"Ошибка: {root} — не найдена директория", file=sys.stderr)
        return 1

    ignore_dirs = set() if args.no_default_ignore else set(DEFAULT_IGNORE_DIRS)
    project_title = args.title or root.name

    print(f"Сканирую {root} …")
    pdata = build_project_data(root, ignore_dirs, args.ignore)
    counts = pdata.stats["counts"]
    print(f"Найдено: {counts['html']} HTML, {counts['css']} CSS, {counts['js']} JS, "
          f"{counts['other']} прочих файлов.")

    print("Строю документацию …")
    html = render_document(pdata, project_title)

    out_path = Path(args.output).resolve()
    out_path.write_text(html, encoding="utf-8")
    print(f"Готово: {out_path} ({human_size(len(html.encode('utf-8')))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
