#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_generator.py
=================

Documentation generator for frontend projects (HTML/CSS/JS).

Walks a project directory, builds a file/directory tree, parses every
HTML/CSS/JS file with awareness of that language's own syntax, finds the
relationships between files (structural links as well as "meaning-level"
links through shared id/class/selectors), and packages all of it into a
single self-contained HTML documentation file (its CSS and JS are inlined,
no network access is required to read it).

Uses the Python standard library only — nothing else needs to be installed.

Usage:
    python3 doc_generator.py /path/to/project -o docs.html

See README.md next to this file for the full option list.
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
# Configuration constants
# --------------------------------------------------------------------------

VERSION = "1.0.0"

#: Directories that are never analyzed (typical build/tooling noise)
DEFAULT_IGNORE_DIRS = {
    "node_modules", ".git", ".svn", ".hg", "dist", "build", "out",
    ".next", ".nuxt", ".cache", "coverage", "__pycache__", ".idea",
    ".vscode", "vendor", ".parcel-cache", ".turbo", ".vercel",
}

#: Extensions parsed as "source" for the three languages
HTML_EXTS = {".html", ".htm"}
CSS_EXTS = {".css"}
JS_EXTS = {".js", ".mjs", ".cjs", ".jsx"}

#: Extensions that show up in the directory map but aren't parsed in depth
KNOWN_OTHER_EXTS = {
    ".json", ".md", ".txt", ".svg", ".png", ".jpg", ".jpeg", ".gif",
    ".webp", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".map", ".yml",
    ".yaml", ".xml", ".scss", ".sass", ".less", ".ts", ".tsx", ".vue",
}

#: "Looks minified" threshold: if the average line length exceeds this,
#: the file is treated as minified and not parsed in detail (otherwise the
#: documentation would drown in an unreadable wall of text).
MINIFIED_AVG_LINE_LEN = 300
MINIFIED_MAX_FILE_FOR_FULL_DUMP = 20000  # chars, beyond which shown code is truncated

JS_KEYWORDS = {
    "break", "case", "catch", "class", "const", "continue", "debugger",
    "default", "delete", "do", "else", "export", "extends", "finally",
    "for", "function", "if", "import", "in", "instanceof", "let", "new",
    "return", "super", "switch", "this", "throw", "try", "typeof", "var",
    "void", "while", "with", "yield", "async", "await", "of", "static",
    "get", "set", "null", "true", "false", "undefined", "from", "as",
}

# Keywords that syntactically look like "name(...) {" but are not actually
# function/method declarations — so they don't get mistaken for one.
JS_CONTROL_KEYWORDS = {
    "if", "for", "while", "switch", "catch", "function", "return",
    "with", "do",
}


# --------------------------------------------------------------------------
# General utilities
# --------------------------------------------------------------------------

def read_text_safe(path: Path) -> str:
    """Reads a text file, tolerant of encoding issues."""
    for enc in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return path.read_bytes().decode("utf-8", errors="replace")


def human_size(num: int) -> str:
    """Formats a byte count as a human-readable size (KB, MB...)."""
    size = float(num)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def slugify(rel_path: str) -> str:
    """Turns a file's relative path into a safe id for an HTML anchor."""
    return "f-" + re.sub(r"[^a-zA-Z0-9_-]+", "-", rel_path).strip("-").lower()


def esc(text: Optional[str]) -> str:
    """HTML-escaping that tolerates None."""
    if text is None:
        return ""
    return html_stdlib.escape(str(text), quote=True)


def is_probably_minified(text: str) -> bool:
    """Heuristic: a file collapsed into one giant line is probably minified."""
    lines = text.splitlines() or [""]
    longest = max((len(ln) for ln in lines), default=0)
    avg = sum(len(ln) for ln in lines) / max(len(lines), 1)
    return longest > 2000 or (avg > MINIFIED_AVG_LINE_LEN and len(lines) < 10)


def count_loc(text: str) -> int:
    """Number of non-blank lines (used as an approximation of LOC)."""
    return sum(1 for ln in text.splitlines() if ln.strip())


def resolve_relative(base_file_rel: str, ref: str) -> Optional[str]:
    """
    Attempts to resolve a relative reference (href/src/@import/import) from
    an HTML/CSS/JS file into a project-root-relative path.
    Returns None if the reference is external (http(s)://, protocol-relative,
    data:, a bare specifier without ./ or ../ for JS, etc.) — such references
    are treated as "external dependencies" rather than project files.
    """
    if not ref:
        return None
    ref = ref.strip().strip("'\"")
    if ref.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
        return None
    parsed = urlsplit(ref)
    if parsed.scheme or ref.startswith("//"):
        return None  # external resource (http(s)://, //cdn...)
    ref_path = parsed.path
    if not ref_path:
        return None
    base_dir = PurePosixPath(base_file_rel).parent
    combined = (base_dir / ref_path)
    # normalize ".." and "."
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
# Data models
# --------------------------------------------------------------------------

@dataclass
class TreeNode:
    """A node in the directory tree (the project map)."""
    name: str
    rel_path: str
    is_dir: bool
    children: list["TreeNode"] = field(default_factory=list)
    kind: str = ""       # 'html' | 'css' | 'js' | 'other' | '' (for directories)
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
    attr_pairs: set = field(default_factory=set)  # {(attr_name, attr_value), ...} -- docgen-002
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
    class_writes: list[dict] = field(default_factory=list)  # {class_name, line} -- docgen-004
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
# Project scanner: builds the directory tree and file lists
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


# docgen-006: a second, orthogonal axis to classify_ext -- "can this tool
# parse it deeply" (unchanged, still just html/css/js) vs. "is this worth a
# person's attention in the file tree". A .php file with real logic and a
# favicon.svg both land in classify_ext's "other" bucket, but they should
# not look identical in the sidebar. Used for tree/sidebar display only --
# it does not change which files get deep analysis.
SOURCE_OTHER_EXTS = {".php", ".jsx", ".tsx", ".vue", ".ts", ".scss", ".sass", ".less"}
CONFIG_EXTS = {".json", ".yaml", ".yml", ".toml", ".xml"}
CONFIG_NAMES = {".env", ".gitignore", ".editorconfig", ".npmrc", ".browserslistrc"}
DOCS_EXTS = {".md", ".txt", ".rst"}
#: below this many asset-tier files at one directory level, list them
#: individually rather than collapsing into one "Assets (N)" group -- not
#: worth the extra click for just one or two icons.
ASSET_GROUP_THRESHOLD = 4


def classify_importance(name: str, ext: str) -> str:
    """Returns 'source-other' | 'config' | 'docs' | 'asset' for any file
    classify_ext already called 'other'. Never called for html/css/js."""
    ext = ext.lower()
    if ext in SOURCE_OTHER_EXTS:
        return "source-other"
    if ext in CONFIG_EXTS or name.lower() in CONFIG_NAMES:
        return "config"
    if ext in DOCS_EXTS:
        return "docs"
    return "asset"


def scan_project(root: Path, ignore_dirs: set, extra_ignore_globs: list) -> tuple:
    """
    Walks the project directory.
    Returns (tree: TreeNode, html_paths, css_paths, js_paths, other_paths).
    Paths are relative (posix-style) to root.
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
                if child.children:  # skip directories that end up fully empty
                    node.children.append(child)
            else:
                if any(entry.match(g) for g in extra_ignore_globs):
                    continue
                routing_kind = classify_ext(entry.suffix)
                # docgen-006: TreeNode.kind drives sidebar display and is
                # allowed to be more specific than the html/css/js/other
                # routing_kind above, which still controls what gets deeply
                # analyzed and must NOT change here.
                display_kind = (routing_kind if routing_kind != "other"
                                 else classify_importance(entry.name, entry.suffix))
                try:
                    size = entry.stat().st_size
                except OSError:
                    size = 0
                child = TreeNode(
                    name=entry.name, rel_path=entry_rel, is_dir=False,
                    kind=display_kind, size=size,
                )
                node.children.append(child)
                if routing_kind == "html":
                    html_paths.append(entry_rel)
                elif routing_kind == "css":
                    css_paths.append(entry_rel)
                elif routing_kind == "js":
                    js_paths.append(entry_rel)
                else:
                    other_paths.append(entry_rel)
        return node

    tree = build(root, "")
    return tree, html_paths, css_paths, js_paths, other_paths


# --------------------------------------------------------------------------
# HTML parsing: built on html.parser.HTMLParser from the standard library
# --------------------------------------------------------------------------

from html.parser import HTMLParser  # noqa: E402  (fine after the constant blocks)

_LANDMARK_TAGS = {"header", "nav", "main", "footer", "article", "aside", "section"}
_CAPTURE_TEXT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "title"}


class _HTMLAnalyzer(HTMLParser):
    """Single-pass parse of HTML into an HtmlInfo structure.

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
        self.attr_pairs: set = set()  # docgen-002
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

    # -- HTMLParser callbacks --------------------------------------

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
        # docgen-002: every attribute, generically -- this is what lets a JS
        # or CSS attribute selector like [data-ref="x"] get cross-referenced
        # the same way #id/.class already were. Not filtered by attr name:
        # a selector could target any of them (aria-*, type, data-*, ...).
        for attr_name, attr_value in a.items():
            if attr_value:
                self.attr_pairs.add((attr_name, attr_value))

        if self_closing:
            self._handle_close(tag)

    def handle_endtag(self, tag):
        self._handle_close(tag)

    def _handle_close(self, tag):
        if self._tag_stack and tag in self._tag_stack:
            # unwind the stack down to the matching tag (tolerant of unclosed tags like <br>)
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
        # HTMLParser rarely throws, but one bad file shouldn't kill the whole run
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
        attr_pairs=parser.attr_pairs,
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
# CSS parsing: a small hand-written tokenizer (no external dependencies)
#
# CSS isn't in the Python standard library, so this parser is hand-rolled:
# a single-pass scanner that tracks brace nesting depth (needed for
# @media/@supports/@keyframes, where braces nest), which also recognizes
# comments and attaches a comment sitting right before a rule to that rule
# — modeled on KSS (Knyle Style Sheets) syntax, where a leading comment is
# the component's documentation.
# --------------------------------------------------------------------------

_COLOR_RE = re.compile(
    r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)"
)
_VAR_USAGE_RE = re.compile(r"var\(\s*(--[a-zA-Z0-9_-]+)")
_BREAKPOINT_RE = re.compile(
    r"(min-width|max-width|min-height|max-height)\s*:\s*([\d.]+[a-z%]*)"
)


def _split_top_level(text: str, sep: str) -> list:
    """Splits a string on a separator, ignoring one that's inside ()/[]/strings."""
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
    Single-pass scan of a CSS text (or an @media body).
    Returns a list of blocks: {'type': 'rule'|'at-simple'|'at-block',
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

        # a normal rule: selector(s) { declarations }
        j = i
        while j < n and text[j] not in "{}":
            if text[j] == "/" and j + 1 < n and text[j + 1] == "*":
                # a comment inside the selector list — skip it as plain text
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
# JavaScript parsing: heuristic (regex + string/comment masking), not a
# full AST parser.
#
# Fully parsing JS syntax in pure Python (without Node.js/Acorn/Esprima) is
# a project of its own. For documentation purposes, a 100%-accurate AST
# matters less than reliably extracting a file's "storefront": what it
# imports/exports, which functions/classes it declares, which DOM elements
# it touches, and what JSDoc says about its functions. So this masks out
# comments (so regexes don't mistake commented-out code for real code) and
# then runs a set of targeted regexes over the masked text, pulling the
# actual snippet from the original text. The limitations of this approach
# are documented in README.md.
# --------------------------------------------------------------------------

def _mask_js(text: str) -> str:
    """
    Returns a string of the same length as text, in which:
      - comment bodies (// and /* */) are replaced with spaces;
      - template-literal (`...`) bodies are replaced with spaces — these
        often hold interpolated HTML markup, which otherwise produces false
        positives when scanning for code structure (e.g. tag-like or
        function-declaration-like fragments inside the string);
      - regular '...' and "..." strings are NOT masked: they're exactly
        where import paths, CSS selectors, and event names live, and that's
        the content the parser actually needs to read.
    Newlines are always preserved so line numbers stay accurate.

    Limitation: telling a regex literal /.../ apart from a division operator
    is not possible without a full tokenizer; a simplified rule is used here
    (see README.md, "Known limitations").
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
            # strings are NOT masked, just skipped over whole, so that
            # special characters/brackets inside them don't confuse later scanning
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
# docgen-004: classList.add/remove/toggle(...) and className = "..." are
# *writes* of a class onto an element, not queries -- but they're just as
# valid evidence that a class is "used" as a querySelector read is. Without
# this, any project that builds its DOM by creating elements and assigning
# classes to them (instead of querying for pre-existing ones) reads as if
# none of its classes were ever touched by JS at all.
_CLASSLIST_WRITE_RE = re.compile(
    r"\.classList\.(?:add|remove|toggle)\(\s*(?P<args>[^)]*)\)"
)
_CLASSLIST_ARG_RE = re.compile(r"""['"`]([^'"`]+)['"`]""")
_CLASSNAME_ASSIGN_RE = re.compile(
    r"\.className\s*=\s*(?P<q>['\"`])(?P<val>[^'\"`]*)(?P=q)"
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
    """Parses the body of a JSDoc comment (between /** and */) into a structure."""
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
            pass  # other tags (@deprecated, @throws...) aren't critical for an overview
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
    """Builds a mapping of 'comment end position' -> parsed JSDoc, so the
    nearest preceding JSDoc for a function/class can be found afterwards."""
    result = []
    for m in _JSDOC_RE.finditer(raw):
        result.append((m.end(), _parse_jsdoc(m.group("body"))))
    return result


def _nearest_jsdoc(jsdoc_list: list, decl_start: int, raw: str) -> Optional[dict]:
    """Returns a JSDoc block if nothing but whitespace and export/default/async
    modifiers sit between its end and the start of the declaration — i.e. the
    comment really documents this particular declaration."""
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
    """Given the position of an opening {, returns (class_body, index_after_closing_brace)."""
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
        # A minified file wouldn't yield anything but noise from parsing.
        # Return basic stats only.
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

    # top-level functions
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

    # classes
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

    # docgen-004: classList writes and className assignments -- a class an
    # element receives via JS is "used" whether or not that element (or any
    # element bearing that class) exists anywhere in the static HTML; unlike
    # dom_queries above, these are NOT cross-checked against the HTML id/class
    # registry in build_edges() -- see the comment there for why.
    for m in _CLASSLIST_WRITE_RE.finditer(masked):
        line = _line_of(raw, m.start())
        for am in _CLASSLIST_ARG_RE.finditer(m.group("args")):
            info.class_writes.append({"class_name": am.group(1), "line": line})
    for m in _CLASSNAME_ASSIGN_RE.finditer(masked):
        line = _line_of(raw, m.start())
        for token in m.group("val").split():
            info.class_writes.append({"class_name": token, "line": line})

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

    # the file's very first comment (if it sits right at the top) often
    # carries the module's overall purpose
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
# Building the relationships between files (the "dependency map")
#
# Two layers of relationships:
#   1. Structural — what's explicitly written in the code: <link>,
#      <script src>, @import, import/require.
#   2. Semantic (DOM) — what connects files through usage: JS reaching into
#      an element by #id/.class, a CSS selector targeting #id/.class. These
#      links aren't visible from "references" inside a single file alone,
#      but they're exactly what shows how HTML/CSS/JS actually work together.
# --------------------------------------------------------------------------

_SIMPLE_TOKEN_RE = re.compile(r"[.#]([A-Za-z_-][\w-]*)")
# docgen-002: [attr="value"] / [attr~="value"] / [attr^="value"] etc. Only
# the exact-match core is cross-referenced (~=, ^=, $=, *=, |= all narrow or
# widen an exact match in ways a simple registry lookup can't reproduce
# faithfully) -- captured here so callers can still see the attribute name
# and value even if the operator itself is ignored for matching purposes.
_ATTR_SELECTOR_RE = re.compile(
    r"\[\s*([a-zA-Z_:][\w:-]*)\s*[~^$*|]?=\s*[\"']([^\"']*)[\"']\s*\]"
)


def _selector_tokens(selector: str) -> list:
    """Extracts plain #id and .class tokens from a CSS/JS selector."""
    return _SIMPLE_TOKEN_RE.findall(selector)


def _selector_attr_pairs(selector: str) -> list:
    """Extracts (attr_name, attr_value) pairs from [attr=value]-style parts
    of a CSS/JS selector. docgen-002."""
    return _ATTR_SELECTOR_RE.findall(selector)


_STRUCTURAL_EDGE_KINDS = {"link", "script", "css-import", "js-import", "js-require",
                           "external", "page-link"}
_SEMANTIC_EDGE_KINDS = {"dom", "style"}


def build_edges(html_files: dict, css_files: dict, js_files: dict) -> tuple:
    """Returns (edges, used_tokens): used_tokens is the set of every
    #id/.class token that was found both in HTML and in a CSS selector or a
    JS DOM query (used to find "dead" hooks independent of edge de-duplication
    used for the on-screen graph)."""
    edges: list = []
    used_tokens: set = set()

    all_html_paths = set(html_files)
    all_css_paths = set(css_files)
    all_js_paths = set(js_files)

    # registry: where each id/class is defined (for semantic links)
    id_registry: dict = {}
    class_registry: dict = {}
    attr_registry: dict = {}  # (attr_name, attr_value) -> [html paths] -- docgen-002
    for path, hinfo in html_files.items():
        for i in hinfo.ids:
            id_registry.setdefault(i, []).append(path)
        for c in hinfo.classes:
            class_registry.setdefault(c, []).append(path)
        for pair in hinfo.attr_pairs:
            attr_registry.setdefault(pair, []).append(path)

    # 1. HTML -> CSS (<link rel=stylesheet>), HTML -> JS (<script src>),
    #    HTML -> HTML (<a href> to another project page)
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

    # 3. JS -> JS (import/require), JS -> external libraries
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

    # 4. JS -> HTML (reaching into the DOM by #id/.class/[attr=value])
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
                # docgen-002: [data-ref="x"]-style hooks, invisible to
                # _selector_tokens above since it only looks for . and #.
                for pair in _selector_attr_pairs(sel):
                    targets.update(attr_registry.get(pair, []))
                    if pair in attr_registry:
                        used_tokens.add(f"[{pair[0]}={pair[1]}]")
            if targets:
                for t in targets:
                    edges.append(Edge(path, t, "dom", label=sel))
            else:
                edges.append(Edge(path, "?", "dom-unresolved", label=sel))

        # docgen-004: a classList.add/className write is proof the class is
        # used by JS regardless of whether the target element exists in the
        # static HTML -- it may be created by this same script. Unlike the
        # read-side loop above, this does NOT require a registry match before
        # counting as "used": requiring one would defeat the purpose, since
        # dynamically-created elements are by definition absent from the
        # static registry.
        for cw in jinfo.class_writes:
            used_tokens.add(cw["class_name"])

    # 5. CSS -> HTML (a selector targets an #id/.class declared in HTML)
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
                    # docgen-001/004: a static-HTML miss is no longer enough
                    # to call a selector orphaned on its own -- used_tokens
                    # (already populated above from JS reads AND writes,
                    # including classes assigned to dynamically-created
                    # elements that never appear in the static registry) can
                    # still vouch for it. Only flag what NEITHER source
                    # accounts for. (used_tokens is a set built earlier in
                    # this same function -- see sections 4 and the
                    # class_writes loop directly above section 5.)
                    elif tok not in used_tokens:
                        unmatched.append(tok)
                # docgen-002: [data-ref="x"]-style selectors -- same
                # treatment as the .class/#id loop just above, using the
                # same `used_tokens` cross-check (and the same
                # "[attr=value]" label format section 4 writes to it with).
                for pair in _selector_attr_pairs(sel):
                    label = f"[{pair[0]}={pair[1]}]"
                    hit = False
                    for t in attr_registry.get(pair, []):
                        if (path, t) not in seen_targets:
                            edges.append(Edge(path, t, "style", label=label))
                            seen_targets.add((path, t))
                        hit = True
                    if hit:
                        used_tokens.add(label)
                    elif label not in used_tokens:
                        unmatched.append(label)
        cinfo.unmatched_selectors = sorted(set(unmatched))

    return edges, used_tokens


# --------------------------------------------------------------------------
# Aggregated project statistics (for the "Overview" section)
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

    # the project's color palette (by usage frequency)
    color_counter: dict = {}
    for cinfo in css_files.values():
        for c in cinfo.colors:
            key = _normalize_color(c)
            color_counter[key] = color_counter.get(key, 0) + 1
    stats["palette"] = sorted(color_counter.items(), key=lambda t: -t[1])[:24]

    # responsive breakpoints
    breakpoints = set()
    for cinfo in css_files.values():
        breakpoints |= cinfo.breakpoints
    stats["breakpoints"] = sorted(breakpoints)

    # external libraries (from script src and import/require that don't
    # resolve inside the project)
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

    # project-wide TODO/FIXME
    todos = []
    for jinfo in js_files.values():
        for t in jinfo.todos:
            todos.append({**t, "file": jinfo.rel_path})
    stats["todos"] = todos

    # unused id/class (declared in HTML but never matched by any CSS
    # selector or any JS DOM query)
    all_ids, all_classes = set(), set()
    for hinfo in html_files.values():
        all_ids |= hinfo.ids
        all_classes |= hinfo.classes
    stats["unused_ids"] = sorted(all_ids - used_tokens)
    stats["unused_classes"] = sorted(all_classes - used_tokens)

    # orphan CSS selectors (collected at the build_edges stage, just rolled up here)
    orphan_selectors = []
    for path, cinfo in css_files.items():
        for sel in cinfo.unmatched_selectors:
            orphan_selectors.append({"file": path, "token": sel})
    stats["orphan_css_selectors"] = orphan_selectors

    # docgen-003: dom_queries the cross-referencer couldn't match to anything
    # (kind="dom-unresolved") used to vanish with no trace once the SVG
    # renderer's kind filter dropped them -- surface a count instead.
    stats["dom_queries_total"] = sum(len(jinfo.dom_queries) for jinfo in js_files.values())
    stats["dom_unresolved"] = [
        {"file": e.src, "selector": e.label} for e in edges if e.kind == "dom-unresolved"
    ]

    # unresolved links (broken paths)
    stats["unresolved_links"] = [
        {"src": e.src, "dst": e.dst, "label": e.label}
        for e in edges if e.kind == "unresolved"
    ]

    # accessibility: images without alt, forms without labels — a light heuristic
    images_no_alt = []
    for hinfo in html_files.values():
        for img in hinfo.images:
            if not img.get("alt"):
                images_no_alt.append({"file": hinfo.rel_path, "src": img.get("src", "")})
    stats["images_no_alt"] = images_no_alt

    return stats


# --------------------------------------------------------------------------
# Syntax highlighting (runs in Python at generation time; the result is
# already-final HTML with <span class="tok-...">, so reading the docs later
# needs no JS and no CDN such as highlight.js/Prism).
# --------------------------------------------------------------------------

def _tokenize_generic(text: str, patterns: list) -> str:
    """
    patterns: a list of (regex, css_class) in priority order.
    Builds one combined regex with named groups and wraps matches in
    <span class="tok-...">, escaping everything else through html.escape.
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
# SVG dependency map ("atlas" of the project): HTML/CSS/JS files as nodes
# in three columns, links between them drawn as routes between "stations".
# Rendered in Python, no JS graphing library involved.
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
        f'aria-label="Project dependency map">'
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
# The final document's embedded CSS and JS (the "Project Atlas").
# Visual language: a map/blueprint of the codebase — a deep ink header,
# cool "drafting paper" as the reading surface, bronze and verdigris
# (oxidized copper/brass) as the two accents instead of the usual
# "cream + terracotta" or "black + neon" pairing.
# Fully offline: no CDN fonts, no external JS libraries — system font
# stacks and inlined code only.
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

/* ---------- Top bar ---------- */
.topbar {
  position: sticky; top: 0; z-index: 40;
  height: var(--topbar-h);
  background: var(--ink);
  color: #eef2f4;
  display: flex; align-items: center; gap: 16px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255,255,255,.08);
}
/* docgen-r1: hidden by default (desktop has a static sidebar, no toggle
   needed); shown only inside the mobile media query below. Base rule lives
   in the stylesheet -- not an inline style -- specifically so that media
   query can override it without needing !important. */
.hamburger-btn {
  display: none; background: none; border: none; color: #fff;
  font-size: 18px; cursor: pointer; padding: 4px 6px; flex: none;
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

/* ---------- Layout ---------- */
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
.sidebar-backdrop { display: none; }  /* shown only in the mobile media query */
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
.tree-eyebrow-row {
  display: flex; align-items: center; justify-content: space-between; gap: 8px;
}
.tree-eyebrow-row .tree-eyebrow { margin: 4px 0 8px; }
.tree-toggle-all {
  font-size: 11px; color: var(--accent); background: none; border: none;
  cursor: pointer; padding: 2px 6px; margin: 0 0 6px; white-space: nowrap;
}
.tree-toggle-all:hover { text-decoration: underline; }

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
.tree .dot.k-source { background: var(--accent); opacity: .8; }  /* docgen-006: php/jsx/vue/ts/scss etc. */
.tree .dot.k-other{ background: var(--ink-soft); opacity: .5; }
.tree[data-filtering="true"] li[data-match="false"] { display: none; }

/* ---------- Main content ---------- */
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

/* ---------- File card ---------- */
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

/* docgen-r3: pre.code and .dep-graph-wrap already scroll internally on
   overflow (see MINIFIED_MAX_FILE_FOR_FULL_DUMP-truncated code, and the
   dependency graph); struct-table had no equivalent, so a long selector
   or file path forced the whole page to scroll horizontally instead of
   just the one table. */
.table-wrap { overflow-x: auto; margin: 4px 0 18px; }
.table-wrap .struct-table { margin: 0; }
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
  .hamburger-btn { display: block; }  /* docgen-r1 */
  .sidebar { position: fixed; left: -100%; transition: left .18s ease; z-index: 50;
    box-shadow: 8px 0 24px rgba(0,0,0,.2); }
  .sidebar.open { left: 0; }
  .content { padding: 24px 18px 100px; }
  #doc-search { width: 130px; }
  /* docgen-r2: brand+timestamp+3 stat chips+search never fit a phone-width
     row together -- drop the two lowest-value items (the timestamp is
     secondary metadata; the counts are already in the Overview stat
     cards) and let the project name truncate instead of overflowing. */
  .topbar .meta, .topbar .stat-chip { display: none; }
  .topbar .brand { flex: 1 1 auto; min-width: 0; }
  .topbar .brand span {
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0;
  }
  .sidebar.open ~ .sidebar-backdrop {
    display: block; position: fixed; inset: 0; background: rgba(10,16,26,.45); z-index: 45;
  }
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

  // ---- Collapse all / expand all (docgen-r4) ----
  var toggleAllBtn = document.getElementById("tree-toggle-all");
  if (toggleAllBtn) {
    toggleAllBtn.addEventListener("click", function () {
      var allDetails = document.querySelectorAll(".tree details");
      var anyOpen = Array.prototype.some.call(allDetails, function (d) { return d.open; });
      allDetails.forEach(function (d) { d.open = !anyOpen; });
      toggleAllBtn.textContent = anyOpen ? "Expand all" : "Collapse all";
    });
  }

  // ---- Search/filter over the file tree and sections ----
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

  // ---- Highlight the active file in the sidebar while scrolling (scrollspy) ----
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

  // ---- Copy code ----
  document.querySelectorAll(".copy-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var pre = btn.parentElement.querySelector("pre.code");
      if (!pre) return;
      var text = pre.textContent;
      var done = function () {
        var old = btn.textContent;
        btn.textContent = "Copied";
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

  // ---- Mobile menu ----
  var toggle = document.getElementById("sidebar-toggle");
  var sidebar = document.querySelector(".sidebar");
  var backdrop = document.getElementById("sidebar-backdrop");
  if (toggle && sidebar) {
    toggle.addEventListener("click", function () { sidebar.classList.toggle("open"); });
    sidebar.querySelectorAll(".file-link").forEach(function (a) {
      a.addEventListener("click", function () { sidebar.classList.remove("open"); });
    });
    if (backdrop) {
      backdrop.addEventListener("click", function () { sidebar.classList.remove("open"); });
    }
  }
})();
"""


# --------------------------------------------------------------------------
# Assembling the document's HTML fragments
# --------------------------------------------------------------------------

COMPASS_SVG = (
    '<svg class="compass" width="26" height="26" viewBox="0 0 26 26" '
    'aria-hidden="true"><circle cx="13" cy="13" r="11.5" fill="none" '
    'stroke="#8a9bab" stroke-width="1" opacity=".55"/>'
    '<path d="M13,2 L15.8,10.2 L24,13 L15.8,15.8 L13,24 L10.2,15.8 L2,13 L10.2,10.2 Z" '
    'fill="#b5762f"/><circle cx="13" cy="13" r="1.6" fill="#eef2f4"/></svg>'
)


_IMPORTANCE_DOT_CLASS = {
    "source-other": "k-source", "config": "k-config",
    "docs": "k-config", "asset": "k-other",
}
_IMPORTANCE_DIMMED = {"asset"}  # docgen-006: only true assets get muted


def _leaf_node_html(node: TreeNode, linkable: set) -> str:
    slug = slugify(node.rel_path)
    # plan.json: a file routed for deep analysis can still have deep_analyze
    # set to 0, in which case there's no card for the sidebar to link to --
    # falls back to the same non-clickable treatment as a config/docs file.
    if node.kind in ("html", "css", "js") and node.rel_path in linkable:
        return (
            f'<li data-name="{esc(node.rel_path.lower())}">'
            f'<a class="file-link" href="#{slug}">'
            f'<span class="dot k-{node.kind}"></span>{esc(node.name)}</a></li>'
        )
    if node.kind in ("html", "css", "js"):
        dot_cls, style = f"k-{node.kind}", "cursor:default"
    else:
        dot_cls = _IMPORTANCE_DOT_CLASS.get(node.kind, "k-other")
        style = "cursor:default;opacity:.55" if node.kind in _IMPORTANCE_DIMMED else "cursor:default"
    return (
        f'<li data-name="{esc(node.rel_path.lower())}">'
        f'<span class="file-link" style="{style}">'
        f'<span class="dot {dot_cls}"></span>{esc(node.name)}</span></li>'
    )


def _render_children_html(children: list, depth: int, linkable: set) -> str:
    """docgen-006: renders a directory's children, grouping asset-tier
    files (icons, fonts, etc.) into one collapsed 'Assets (N)' entry once
    there are enough of them to bury the files that actually matter --
    everything else (dirs, core source, source-other, config, docs) is
    listed exactly as before."""
    prominent, assets = [], []
    for c in children:
        (assets if (not c.is_dir and c.kind == "asset") else prominent).append(c)

    parts = [_tree_node_html(c, depth, linkable) for c in prominent]
    if len(assets) >= ASSET_GROUP_THRESHOLD:
        inner = "".join(_leaf_node_html(a, linkable) for a in assets)
        names = " ".join(a.name.lower() for a in assets)
        parts.append(
            f'<li data-name="{esc(names)}">'
            f'<details><summary>Assets ({len(assets)})</summary>'
            f'<ul>{inner}</ul></details></li>'
        )
    else:
        parts.extend(_leaf_node_html(a, linkable) for a in assets)
    return "".join(parts)


def _tree_node_html(node: TreeNode, depth: int, linkable: set) -> str:
    if node.is_dir:
        children_html = _render_children_html(node.children, depth + 1, linkable)
        open_attr = " open" if depth < 1 else ""
        return (
            f'<li data-name="{esc(node.name.lower())}">'
            f'<details{open_attr}><summary>{esc(node.name)}/</summary>'
            f'<ul>{children_html}</ul></details></li>'
        )
    return _leaf_node_html(node, linkable)


def build_sidebar_tree(tree: TreeNode, linkable: set) -> str:
    inner = _render_children_html(tree.children, 0, linkable)
    return f'<ul class="tree" id="file-tree">{inner}</ul>'


def _relations_for(path: str, edges: list, all_paths: set, linkable: set):
    """Returns (structural_out, structural_in, semantic_out, semantic_in).
    Structural links (link/script/import/require/page navigation) are shown
    as "Depends on / Used in". Semantic DOM links (JS reaches into an
    element, CSS targets a class) are shown separately — that's not a
    "dependency" in the load-order sense, it's which HTML elements the file
    actually touches. `linkable` (plan.json's deep_analyze=1 files) controls
    whether a chip gets an href -- a file the plan excluded from analysis
    still shows up as a relationship, just not as a dead link to a card
    that was never generated."""
    def slug_if_linkable(p):
        return slugify(p) if p in linkable else None

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
                    structural_out.append((e.dst, slug_if_linkable(e.dst), e.kind))
            elif e.kind in _SEMANTIC_EDGE_KINDS and e.dst in all_paths:
                semantic_out.append((e.dst, slug_if_linkable(e.dst), e.kind))
        if e.dst == path and e.src != path:
            key = ("in", e.src, e.kind)
            if key in seen:
                continue
            seen.add(key)
            if e.kind in _STRUCTURAL_EDGE_KINDS:
                structural_in.append((e.src, slug_if_linkable(e.src), e.kind))
            elif e.kind in _SEMANTIC_EDGE_KINDS:
                semantic_in.append((e.src, slug_if_linkable(e.src), e.kind))
    # de-duplicate by file while preserving order of first appearance
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
                   semantic_out_label: str = "Touches elements in",
                   semantic_in_label: str = "Styled / scripted from") -> str:
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
        f'<div class="rel-group"><strong>Depends on</strong>{chips(structural_out)}</div>'
        f'<div class="rel-group"><strong>Used in</strong>{chips(structural_in)}</div>'
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
    badges.append(f'<span class="badge">{info.loc} lines</span>')
    if info.is_minified:
        badges.append('<span class="badge warn">minified</span>')
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
        note = (f'<p class="muted">This file is large ({human_size(len(raw))}) — showing the first '
                f'{MINIFIED_MAX_FILE_FOR_FULL_DUMP} characters.</p>')
    else:
        shown, note = raw, ""
    highlighted = highlight_by_kind(shown, kind)
    return (
        '<div class="tab-panel">' + note +
        '<div class="code-wrap"><button class="copy-btn" type="button">Copy</button>'
        f'<pre class="code"><code>{highlighted}</code></pre></div></div>'
    )


def _struct_panel_html(info: HtmlInfo) -> str:
    parts = ['<div class="tab-panel">']

    meta_rows = [
        ("Title (&lt;title&gt;)", info.title or "—"),
        ("lang", info.lang or "—"),
        ("meta description", info.meta_description or "—"),
        ("DOCTYPE", "present" if info.doctype_ok else "missing"),
        ("Word count", str(info.word_count)),
    ]
    parts.append('<div class="table-wrap">')  # docgen-r3
    parts.append('<table class="struct-table"><tbody>')
    for label, val in meta_rows:
        parts.append(f"<tr><th>{label}</th><td>{esc(val)}</td></tr>")
    parts.append("</tbody></table>")
    parts.append("</div>")  # docgen-r3

    if info.landmarks:
        chips = "".join(f'<span class="chip-plain">&lt;{esc(t)}&gt;</span>'
                         for t in sorted(info.landmarks))
        parts.append(f'<div class="struct-sub-h">Semantic landmark tags</div><div>{chips}</div>')

    if info.headings:
        parts.append('<div class="struct-sub-h">Heading structure</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>Level</th><th>Text</th></tr></thead><tbody>')
        for level, text in info.headings[:40]:
            indent = "&nbsp;" * ((level - 1) * 3)
            parts.append(f"<tr><td><code>h{level}</code></td><td>{indent}{esc(text)}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.forms:
        parts.append('<div class="struct-sub-h">Forms</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>action</th><th>method</th><th>fields</th></tr></thead><tbody>')
        for f in info.forms:
            fields = ", ".join(f["fields"]) or "—"
            parts.append(f"<tr><td><code>{esc(f['action'] or '(current page)')}</code></td>"
                         f"<td><code>{esc(f['method'])}</code></td><td>{esc(fields)}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.images:
        no_alt = sum(1 for i in info.images if not i.get("alt"))
        parts.append(f'<div class="struct-sub-h">Images ({len(info.images)}'
                      + (f", missing alt: {no_alt}" if no_alt else "") + ")</div>")
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>src</th><th>alt</th></tr></thead><tbody>')
        for img in info.images[:30]:
            alt = img.get("alt") or ""
            alt_html = esc(alt) if alt else '<span class="badge warn">no alt</span>'
            parts.append(f"<tr><td><code>{esc(img.get('src',''))}</code></td><td>{alt_html}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.ids or info.classes:
        parts.append('<div class="struct-sub-h">id / class on this page</div>')
        id_chips = "".join(f'<span class="chip-plain">#{esc(i)}</span>' for i in sorted(info.ids)[:40])
        class_chips = "".join(f'<span class="chip-plain">.{esc(c)}</span>' for c in sorted(info.classes)[:60])
        parts.append(f"<div>{id_chips}</div><div style='margin-top:6px'>{class_chips}</div>")

    if info.comments:
        parts.append('<div class="struct-sub-h">Comments in the markup</div><ul class="param-list">')
        for c in info.comments[:20]:
            c_short = c if len(c) < 160 else c[:160] + "…"
            parts.append(f"<li>{esc(c_short)}</li>")
        parts.append("</ul>")

    if info.hrefs_external:
        chips = "".join(f'<span class="chip-plain">{esc(h)}</span>' for h in info.hrefs_external[:20])
        parts.append(f'<div class="struct-sub-h">External links</div><div>{chips}</div>')

    parts.append("</div>")
    return "".join(parts)


def build_file_card_html(path: str, info: HtmlInfo, edges: list, all_paths: set, linkable: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths, linkable)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(info.title or path)}</h3>'
        + _badges_html("html", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Links to pages",
                        semantic_in_label="Styled / scripted from")
    )
    tabs = _tabs_open(slug, ["Code", "Structure"])
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
        ("Rules total (including those nested in @media)", str(len(info.rules) + nested_count)),
        ("At-rules (@media/@keyframes/…)", str(len(info.at_rules))),
        ("Imports (@import)", str(len(info.imports)) if info.imports else "0"),
    ]
    parts.append('<div class="table-wrap">')  # docgen-r3
    parts.append('<table class="struct-table"><tbody>')
    for label, val in top_rows:
        parts.append(f"<tr><th>{label}</th><td>{esc(val)}</td></tr>")
    parts.append("</tbody></table>")
    parts.append("</div>")  # docgen-r3

    if info.custom_props_defined:
        parts.append('<div class="struct-sub-h">CSS custom properties defined here</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>Property</th><th>Value</th></tr></thead><tbody>')
        for name, value in info.custom_props_defined.items():
            swatch = _color_swatch(value) if _COLOR_RE.match(value.strip()) else ""
            parts.append(f"<tr><td><code>{esc(name)}</code></td><td>{swatch} <code>{esc(value)}</code></td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.breakpoints:
        chips = "".join(f'<span class="chip-plain">{esc(b)}</span>' for b in sorted(info.breakpoints))
        parts.append(f'<div class="struct-sub-h">Media breakpoints</div><div>{chips}</div>')

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
        parts.append(f'<div class="struct-sub-h">Rules '
                      f'({len(all_rules_with_ctx)}{" — showing the first " + str(cap) if len(all_rules_with_ctx) > cap else ""})</div>')
        for rule, ctx in all_rules_with_ctx[:cap]:
            sel_html = ", ".join(f"<code>{esc(s)}</code>" for s in rule.selectors)
            ctx_html = f' <span class="muted">inside {esc(ctx)}</span>' if ctx else ""
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
        chips = "".join(
            f'<span class="chip-plain">{esc(s if s.startswith("[") else "." + s)}</span>'
            for s in info.unmatched_selectors[:30]
        )
        parts.append(
            '<div class="note-block"><h4>Cartographer\'s note</h4>'
            "<p class='muted' style='margin:0 0 8px'>These classes/ids are used in this file's selectors, "
            "but weren't found in any HTML file in the project. The elements might be added dynamically "
            f"via JS, or this could be leftover unused code.</p><div>{chips}</div></div>"
        )

    parts.append("</div>")
    return "".join(parts)


def build_file_card_css(path: str, info: CssInfo, edges: list, all_paths: set, linkable: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths, linkable)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(path.split("/")[-1])}</h3>'
        + _badges_html("css", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Applied on pages",
                        semantic_in_label="")
    )
    tabs = _tabs_open(slug, ["Code", "Structure"])
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
        out.append(f'<div class="doc-desc"><em>Returns:</em> {esc(doc["returns"])}</div>')
    for ex in doc.get("examples", []):
        out.append(f'<pre class="code" style="margin-top:6px"><code>{esc(ex)}</code></pre>')
    return "".join(out)


def _func_block_html(fn: JsFunctionInfo) -> str:
    params = ", ".join(fn.params)
    exported = ' <span class="badge">export</span>' if fn.is_exported else ""
    undoc = "" if fn.doc else ' <span class="badge warn">no JSDoc</span>'  # docgen-005
    kind_label = {"function": "function", "arrow": "const (arrow)",
                  "method": "method", "constructor": "constructor"}.get(fn.kind, fn.kind)
    return (
        '<div class="func-block">'
        f'<div class="func-sig">{esc(kind_label)} <strong>{esc(fn.name)}</strong>({esc(params)})'
        f' <span class="muted">· line {fn.line}</span>{exported}{undoc}</div>'
        + _doc_block_html(fn.doc) +
        "</div>"
    )


def _jsdoc_coverage_html(info: JsInfo) -> str:
    """docgen-005: a flat list of 200+ functions makes 'about half of these
    have no explanation at all' undiscoverable without counting by hand --
    surface it as one line before the list itself."""
    total = len(info.functions) + sum(len(c.methods) for c in info.classes)
    if total == 0:
        return ""
    documented = (sum(1 for fn in info.functions if fn.doc)
                  + sum(1 for c in info.classes for m in c.methods if m.doc))
    pct = round(100 * documented / total)
    return (f'<p class="muted" style="margin:2px 0 14px">JSDoc coverage: '
            f'<strong>{documented} / {total}</strong> functions and methods ({pct}%) '
            f'have a description. Entries without one are marked '
            f'<span class="badge warn">no JSDoc</span> below.</p>')


def _struct_panel_js(info: JsInfo) -> str:
    parts = ['<div class="tab-panel">']

    if info.top_comment:
        parts.append(f'<div class="doc-desc">{esc(info.top_comment)}</div>')

    if info.imports or info.requires:
        parts.append('<div class="struct-sub-h">Imports</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>From</th><th>What</th></tr></thead><tbody>')
        for imp in info.imports:
            names = imp.get("names") or []
            label = imp.get("namespace") and f"* as {imp['namespace']}" or \
                (", ".join(filter(None, [imp.get("default_name")] + names)) or "(side effect only)")
            dyn = " <span class='badge'>dynamic</span>" if imp.get("dynamic") else ""
            parts.append(f"<tr><td><code>{esc(imp['source'])}</code></td><td>{esc(label)}{dyn}</td></tr>")
        for req in info.requires:
            parts.append(f"<tr><td><code>{esc(req)}</code></td><td>require()</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.exports:
        chips = "".join(f'<span class="chip-plain">{esc(e)}</span>' for e in info.exports)
        parts.append(f'<div class="struct-sub-h">Exports</div><div>{chips}</div>')

    if info.functions or info.classes:
        parts.append(_jsdoc_coverage_html(info))

    if info.functions:
        parts.append(f'<div class="struct-sub-h">Functions ({len(info.functions)})</div>')
        for fn in info.functions:
            parts.append(_func_block_html(fn))

    if info.classes:
        parts.append(f'<div class="struct-sub-h">Classes ({len(info.classes)})</div>')
        for cls in info.classes:
            extends = f" extends {esc(cls.extends)}" if cls.extends else ""
            parts.append(
                '<div class="func-block">'
                f'<div class="func-sig">class <strong>{esc(cls.name)}</strong>{extends} '
                f'<span class="muted">· line {cls.line}</span></div>'
                + _doc_block_html(cls.doc)
            )
            for m in cls.methods:
                parts.append(
                    '<div style="margin-left:16px;border-top:1px dashed var(--paper-line);padding-top:8px">'
                    + _func_block_html(m) + "</div>"
                )
            parts.append("</div>")

    if info.dom_queries:
        parts.append('<div class="struct-sub-h">DOM access</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>Method</th><th>Selector</th><th>Line</th></tr></thead><tbody>')
        for q in info.dom_queries:
            parts.append(f"<tr><td><code>{esc(q['method'])}</code></td>"
                         f"<td><code>{esc(q['selector'])}</code></td><td>{q['line']}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.event_listeners:
        parts.append('<div class="struct-sub-h">Event listeners</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>Target</th><th>Event</th><th>Line</th></tr></thead><tbody>')
        for ev in info.event_listeners:
            parts.append(f"<tr><td><code>{esc(ev['target'])}</code></td>"
                         f"<td><code>{esc(ev['event'])}</code></td><td>{ev['line']}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if info.network_calls:
        chips = "".join(f'<span class="chip-plain">{esc(c["kind"])} · line {c["line"]}</span>'
                         for c in info.network_calls)
        parts.append(f'<div class="struct-sub-h">Network calls</div><div>{chips}</div>')

    if info.todos:
        parts.append('<div class="note-block"><h4>TODO / FIXME</h4><ul>')
        for t in info.todos:
            parts.append(f"<li><code>{esc(t['marker'])}</code> (line {t['line']}): {esc(t['text'])}</li>")
        parts.append("</ul></div>")

    if not any([info.imports, info.requires, info.exports, info.functions,
                info.classes, info.dom_queries, info.event_listeners]):
        parts.append('<p class="muted">No explicit structure (functions, classes, imports) was found.</p>')

    parts.append("</div>")
    return "".join(parts)


def build_file_card_js(path: str, info: JsInfo, edges: list, all_paths: set, linkable: set) -> str:
    slug = slugify(path)
    s_out, s_in, sem_out, sem_in = _relations_for(path, edges, all_paths, linkable)
    header = (
        f'<article class="file-card" id="{slug}">'
        f'<div class="file-path">{esc(path)}</div>'
        f'<h3 class="file-h">{esc(path.split("/")[-1])}</h3>'
        + _badges_html("js", info)
        + _rel_row_html(s_out, s_in, sem_out, sem_in,
                        semantic_out_label="Targets elements on",
                        semantic_in_label="")
    )
    tabs = _tabs_open(slug, ["Code", "Structure"])
    body = _code_panel(slug, info.raw, "js") + _struct_panel_js(info)
    return header + tabs + body + _TABS_CLOSE + "</article>"


# --------------------------------------------------------------------------
# Generation plan: an optional intermediate stage between analysis and
# rendering. build_project_data() already knows everything about the
# project; derive_generation_plan() repackages those facts into a flat,
# binary-flag JSON a human or an LLM agent can inspect and hand-edit before
# a single line of HTML is written. Every default is 1 ("show it") --
# this stage is a lever for a person to pull, not a second layer of
# heuristics deciding things on its own. Entirely optional: render_document()
# synthesizes an all-1 plan internally when none is given, so default runs
# are byte-identical to a version of this tool with no plan concept at all.
# --------------------------------------------------------------------------

_PLAN_SECTION_KEYS = ("overview", "dependency_graph", "cartographer_notes", "color_palette")
_PLAN_DIAGNOSTIC_KEYS = ("unused_id_class", "orphan_css_selectors", "unresolved_links",
                         "unresolved_dom_lookups", "images_without_alt", "todo_fixme")


def derive_generation_plan(pdata: "ProjectData", project_title: str) -> dict:
    """Builds an all-1 (show everything) plan reflecting what was actually
    found, so a reader deciding what to flip off can see real counts
    instead of guessing blind."""
    s = pdata.stats
    plan = {
        "meta": {
            "project": project_title,
            "html": s["counts"]["html"], "css": s["counts"]["css"],
            "js": s["counts"]["js"], "other": s["counts"]["other"],
            "_available_diagnostic_counts": {
                "unused_id_class": len(s["unused_ids"]) + len(s["unused_classes"]),
                "orphan_css_selectors": len(s["orphan_css_selectors"]),
                "unresolved_links": len(s["unresolved_links"]),
                "unresolved_dom_lookups": len(s["dom_unresolved"]),
                "images_without_alt": len(s["images_no_alt"]),
                "todo_fixme": len(s["todos"]),
            },
        },
        "sections": {k: 1 for k in _PLAN_SECTION_KEYS},
        "diagnostics": {k: 1 for k in _PLAN_DIAGNOSTIC_KEYS},
        "files": {
            path: {"deep_analyze": 1}
            for path in list(pdata.html_files) + list(pdata.css_files) + list(pdata.js_files)
        },
        "assets": {"group_when_over": ASSET_GROUP_THRESHOLD, "list_individually": 0},
    }
    return plan


def _normalize_plan(plan: dict, pdata: "ProjectData") -> dict:
    """Fills in anything missing from a hand-edited or partial plan with
    the permissive (1) default, so a plan.json with only the three lines
    someone actually cared about changing still works. Never raises on a
    malformed plan -- worst case, missing/invalid pieces fall back to 1."""
    plan = dict(plan) if isinstance(plan, dict) else {}
    sections = dict(plan.get("sections") or {})
    for k in _PLAN_SECTION_KEYS:
        sections[k] = 1 if sections.get(k, 1) else 0
    diagnostics = dict(plan.get("diagnostics") or {})
    for k in _PLAN_DIAGNOSTIC_KEYS:
        diagnostics[k] = 1 if diagnostics.get(k, 1) else 0
    files_in = plan.get("files") or {}
    all_paths = list(pdata.html_files) + list(pdata.css_files) + list(pdata.js_files)
    files = {}
    for path in all_paths:
        entry = files_in.get(path) or {}
        files[path] = {"deep_analyze": 1 if entry.get("deep_analyze", 1) else 0}
    assets_in = plan.get("assets") or {}
    try:
        group_when_over = int(assets_in.get("group_when_over", ASSET_GROUP_THRESHOLD))
    except (TypeError, ValueError):
        group_when_over = ASSET_GROUP_THRESHOLD
    return {
        "meta": plan.get("meta") or {},
        "sections": sections,
        "diagnostics": diagnostics,
        "files": files,
        "assets": {"group_when_over": group_when_over,
                    "list_individually": 1 if assets_in.get("list_individually") else 0},
    }


def save_plan(plan: dict, path: Path) -> None:
    path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_plan(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_overview_section(pdata: "ProjectData", plan: dict) -> str:
    if not plan["sections"]["overview"]:
        return ""
    diag = plan["diagnostics"]
    s = pdata.stats
    counts = s["counts"]
    parts = ['<section id="overview">']
    parts.append('<h2 class="section-h">Project overview</h2>')
    parts.append(
        '<p class="lede">An automatically assembled map of the project: '
        f'{counts["html"]} HTML, {counts["css"]} CSS, and {counts["js"]} JS files, '
        f'{human_size(s["total_size"])} of source code, {s["total_loc"]} non-blank lines.</p>'
    )

    parts.append('<div class="card-grid">')
    for label, val in [
        ("HTML files", counts["html"]), ("CSS files", counts["css"]),
        ("JS files", counts["js"]), ("Other files", counts["other"]),
        ("Lines of code", s["total_loc"]), ("Total size", human_size(s["total_size"])),
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
        parts.append('<div class="struct-sub-h">Largest files</div>')
        parts.append('<div class="table-wrap">')  # docgen-r3
        parts.append('<table class="struct-table"><thead><tr><th>File</th><th>Size</th><th>Lines</th></tr></thead><tbody>')
        for path, size, loc, kind in s["largest_files"]:
            parts.append(f'<tr><td><a href="#{slugify(path)}"><code>{esc(path)}</code></a></td>'
                         f"<td>{human_size(size)}</td><td>{loc}</td></tr>")
        parts.append("</tbody></table>")
        parts.append("</div>")  # docgen-r3

    if s["palette"] and plan["sections"]["color_palette"]:
        parts.append('<div class="struct-sub-h">Color palette (by usage frequency in CSS)</div>')
        parts.append('<div class="swatch-row">')
        for color, _count in s["palette"]:
            parts.append(_color_swatch(color))
        parts.append("</div>")

    if s["breakpoints"]:
        chips = "".join(f'<span class="chip-plain">{esc(b)}</span>' for b in s["breakpoints"])
        parts.append(f'<div class="struct-sub-h">Responsive breakpoints</div><div>{chips}</div>')

    if s["external_libs"]:
        chips = "".join(f'<span class="chip-plain">{esc(lib)}</span>' for lib in s["external_libs"])
        parts.append(f'<div class="struct-sub-h">External libraries / CDN</div><div>{chips}</div>')

    if not plan["sections"]["cartographer_notes"]:
        parts.append("</section>")
        return "".join(parts)

    notes = []
    if (s["unused_ids"] or s["unused_classes"]) and diag["unused_id_class"]:
        items = [f"#{i}" for i in s["unused_ids"][:15]] + [f".{c}" for c in s["unused_classes"][:25]]
        more = len(s["unused_ids"]) + len(s["unused_classes"]) - len(items)
        notes.append(("Unused id / class",
                      "Declared in HTML, but never matched by a CSS selector or a JS DOM query. "
                      "Might be reserved for future use, or leftover from a refactor.",
                      items, more))
    if s["orphan_css_selectors"] and diag["orphan_css_selectors"]:
        items = [f'{o["file"]}: {o["token"] if o["token"].startswith("[") else "." + o["token"]}'
                 for o in s["orphan_css_selectors"][:20]]
        more = len(s["orphan_css_selectors"]) - len(items)
        notes.append(("CSS rules with no match in HTML",
                      "These selectors target classes/ids not found in any page's static HTML, and not "
                      "assigned anywhere in JS via classList/className either -- likely dead, but a "
                      "class built from a runtime string (e.g. `'tone-' + variant`) can still slip past both checks.",
                      items, more))
    if s["unresolved_links"] and diag["unresolved_links"]:
        items = [f'{u["src"]} → {u["dst"]}' for u in s["unresolved_links"][:20]]
        more = len(s["unresolved_links"]) - len(items)
        notes.append(("Unresolved links",
                      "The path in href/src couldn't be matched to any project file — possibly a typo.",
                      items, more))
    if s["images_no_alt"] and diag["images_without_alt"]:
        items = [f'{i["file"]}: {i["src"]}' for i in s["images_no_alt"][:20]]
        more = len(s["images_no_alt"]) - len(items)
        notes.append(("Images without alt",
                      "Affects accessibility (screen readers) and SEO.",
                      items, more))
    if s["todos"] and diag["todo_fixme"]:
        items = [f'{t["file"]}:{t["line"]} — {t["text"]}' for t in s["todos"][:20]]
        more = len(s["todos"]) - len(items)
        notes.append(("Project-wide TODO / FIXME", "", items, more))
    if s["dom_unresolved"] and diag["unresolved_dom_lookups"]:
        items = [f'{d["file"]}: {d["selector"]}' for d in s["dom_unresolved"][:20]]
        more = len(s["dom_unresolved"]) - len(items)
        notes.append((
            "Unresolved DOM lookups",
            f'{s["dom_queries_total"]} DOM lookup(s) found in JS; {len(s["dom_unresolved"])} use a selector '
            "this scan couldn't match to a static element -- often an attribute selector like [data-x], "
            "or a selector built from a variable rather than a literal string. Not necessarily broken: "
            "these are real, just outside what this analysis can trace.",
            items, more,
        ))

    if notes:
        parts.append('<div class="struct-sub-h">Cartographer\'s notes</div>')
        for title, desc, items, more in notes:
            parts.append('<div class="note-block"><h4>' + esc(title) + "</h4>")
            if desc:
                parts.append(f"<p class='muted' style='margin:0 0 8px'>{esc(desc)}</p>")
            parts.append("<ul>" + "".join(f"<li><code>{esc(i)}</code></li>" for i in items) + "</ul>")
            if more > 0:
                parts.append(f'<p class="muted" style="margin:6px 0 0">…and {more} more.</p>')
            parts.append("</div>")
    else:
        parts.append(
            '<div class="note-block empty"><h4>Cartographer\'s notes</h4>'
            "<p class='muted' style='margin:0'>No obvious mismatches between HTML, CSS, and JS were found "
            "(or the checks that would have found them are turned off in the generation plan).</p></div>"
        )

    parts.append("</section>")
    return "".join(parts)


_GRAPH_LEGEND_SVG = (
    '<span class="ln"><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" '
    'stroke="var(--ink-soft)" stroke-width="1.6" opacity=".5"/></svg>structural link '
    "(link/script/import)</span>"
    '<span class="ln"><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" '
    'stroke="var(--map-accent-warm)" stroke-width="1.4" stroke-dasharray="3 3"/></svg>'
    "semantic link (DOM id/class)</span>"
)


def build_dependency_section(pdata: "ProjectData") -> str:
    if not pdata.html_files and not pdata.css_files and not pdata.js_files:
        return ""
    svg = render_dependency_graph_svg(pdata.html_files, pdata.css_files, pdata.js_files, pdata.edges)
    return (
        '<section id="dependency-map">'
        '<h2 class="section-h">Dependency map</h2>'
        '<p class="lede">Solid lines are direct references (&lt;link&gt;, &lt;script&gt;, import/require). '
        "Dashed lines are semantic DOM links: which JS/CSS reaches into which HTML elements.</p>"
        f'<div class="graph-legend">{_GRAPH_LEGEND_SVG}</div>'
        f'<div class="dep-graph-wrap">{svg}</div>'
        "</section>"
    )


# --------------------------------------------------------------------------
# Final assembly of the single documentation HTML file (a template with
# placeholders)
# --------------------------------------------------------------------------

DOCUMENT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>__STYLES__</style>
</head>
<body>
<header class="topbar">
  <button id="sidebar-toggle" class="hamburger-btn" aria-label="Menu">☰</button>
  <div class="brand">__COMPASS__<span>__PROJECT_NAME__</span></div>
  <span class="meta">generated __GENERATED_AT__</span>
  <div class="spacer"></div>
  __STAT_CHIPS__
  <input id="doc-search" type="search" placeholder="Search files…" aria-label="Search files">
</header>
<div class="layout">
  <nav class="sidebar" aria-label="Project navigation">
    <ul class="quicknav">
      <li><a href="#overview">Project overview</a></li>
      <li><a href="#dependency-map">Dependency map</a></li>
    </ul>
    <div class="tree-eyebrow-row">
      <div class="tree-eyebrow">Project files</div>
      <button type="button" id="tree-toggle-all" class="tree-toggle-all">Collapse all</button>
    </div>
    __SIDEBAR_TREE__
  </nav>
  <div class="sidebar-backdrop" id="sidebar-backdrop"></div>
  <main class="content">
    __OVERVIEW__
    __DEPENDENCY_MAP__
    <h2 class="section-h">Files</h2>
    __FILE_SECTIONS__
  </main>
</div>
<footer class="doc-footer">
  Documentation generated automatically by doc_generator.py v__VERSION__ — static analysis,
  the project's code is never executed. Some conclusions (what a function is for, categorization)
  rely on heuristics and on comments in the source, and may be inaccurate.
</footer>
<script>__SCRIPTS__</script>
</body>
</html>
"""


def render_document(pdata: "ProjectData", project_title: str, plan: dict = None) -> str:
    plan = _normalize_plan(plan or {}, pdata)

    counts = pdata.stats["counts"]
    stat_chips = "".join(
        f'<span class="stat-chip">{v} {label}</span>'
        for label, v in [("HTML", counts["html"]), ("CSS", counts["css"]), ("JS", counts["js"])]
    )

    all_paths = set(pdata.html_files) | set(pdata.css_files) | set(pdata.js_files)
    linkable = {p for p in all_paths if plan["files"].get(p, {}).get("deep_analyze", 1)}

    file_sections = []
    for path in sorted(pdata.html_files):
        if path in linkable:
            file_sections.append(build_file_card_html(path, pdata.html_files[path], pdata.edges, all_paths, linkable))
    for path in sorted(pdata.css_files):
        if path in linkable:
            file_sections.append(build_file_card_css(path, pdata.css_files[path], pdata.edges, all_paths, linkable))
    for path in sorted(pdata.js_files):
        if path in linkable:
            file_sections.append(build_file_card_js(path, pdata.js_files[path], pdata.edges, all_paths, linkable))

    dependency_map_html = build_dependency_section(pdata) if plan["sections"]["dependency_graph"] else ""

    html = DOCUMENT_TEMPLATE
    html = html.replace("__TITLE__", esc(project_title))
    html = html.replace("__STYLES__", DOC_CSS)
    html = html.replace("__COMPASS__", COMPASS_SVG)
    html = html.replace("__PROJECT_NAME__", esc(project_title))
    html = html.replace("__GENERATED_AT__", esc(pdata.generated_at))
    html = html.replace("__STAT_CHIPS__", stat_chips)
    html = html.replace("__SIDEBAR_TREE__", build_sidebar_tree(pdata.tree, linkable))
    html = html.replace("__OVERVIEW__", build_overview_section(pdata, plan))
    html = html.replace("__DEPENDENCY_MAP__", dependency_map_html)
    html = html.replace("__FILE_SECTIONS__", "".join(file_sections))
    html = html.replace("__VERSION__", VERSION)
    html = html.replace("__SCRIPTS__", DOC_JS)
    return html


# --------------------------------------------------------------------------
# Orchestration: assembling the full ProjectData
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
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
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
        description="Generates a single HTML documentation file for a frontend project (HTML/CSS/JS).",
    )
    parser.add_argument("project_dir", help="Path to the root of the frontend project")
    parser.add_argument("-o", "--output", default="documentation.html",
                         help="Path to the output HTML file (default: documentation.html)")
    parser.add_argument("--title", default=None,
                         help="Project name shown in the documentation (default: the folder name)")
    parser.add_argument("--ignore", action="append", default=[],
                         help="Extra glob pattern to exclude files (can be given multiple times)")
    parser.add_argument("--no-default-ignore", action="store_true",
                         help="Do not exclude the standard tooling folders (node_modules, .git, etc.)")
    parser.add_argument("--plan-only", action="store_true",
                         help="Scan and analyze, write a generation-plan JSON, then stop -- no HTML is "
                              "written. Review/edit the plan, then rerun with --from-plan.")
    parser.add_argument("--plan-output", default=None,
                         help="Path for --plan-only's JSON (default: <output> with .html replaced by .plan.json)")
    parser.add_argument("--from-plan", default=None, metavar="PLAN_JSON",
                         help="Render using a (possibly hand-edited) generation-plan JSON from a previous "
                              "--plan-only run, instead of the all-sections-on default.")
    args = parser.parse_args(argv)

    root = Path(args.project_dir).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        return 1

    ignore_dirs = set() if args.no_default_ignore else set(DEFAULT_IGNORE_DIRS)
    project_title = args.title or root.name

    print(f"Scanning {root} …")
    pdata = build_project_data(root, ignore_dirs, args.ignore)
    counts = pdata.stats["counts"]
    print(f"Found: {counts['html']} HTML, {counts['css']} CSS, {counts['js']} JS, "
          f"{counts['other']} other files.")

    if args.plan_only:
        plan = derive_generation_plan(pdata, project_title)
        plan_path = Path(args.plan_output) if args.plan_output else \
            Path(args.output).with_suffix("").with_suffix(".plan.json") if args.output.endswith(".html") \
            else Path(str(args.output) + ".plan.json")
        save_plan(plan, plan_path)
        print(f"Plan written: {plan_path.resolve()}")
        print("Nothing was rendered. Edit any 1/0 flag, then rerun with --from-plan "
              f"{plan_path.name} -o {args.output}.")
        return 0

    plan = None
    if args.from_plan:
        plan_path = Path(args.from_plan)
        if not plan_path.is_file():
            print(f"Error: plan file not found: {plan_path}", file=sys.stderr)
            return 1
        try:
            plan = load_plan(plan_path)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error: couldn't read plan file ({e}) -- rendering with all sections on instead.",
                  file=sys.stderr)
            plan = None

    print("Building documentation …")
    html = render_document(pdata, project_title, plan)

    out_path = Path(args.output).resolve()
    out_path.write_text(html, encoding="utf-8")
    print(f"Done: {out_path} ({human_size(len(html.encode('utf-8')))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
