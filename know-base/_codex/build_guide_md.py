#!/usr/bin/env python3
"""Manage section fragments and merge a JSON guide into Markdown.

All writes are constrained to the _codex workspace that contains this script.
The source JSON is read from the repository root by default.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
DEFAULT_SOURCE = ROOT_DIR / "Ultimate_Software_Engineering_Knowledge_Architecture_FINAL.json"
DEFAULT_MANIFEST = SCRIPT_DIR / "manifest.json"
DEFAULT_OUTPUT = SCRIPT_DIR / "output" / "Ultimate_Software_Engineering_Knowledge_Architecture_FINAL.md"

STATUSES = ("pending", "drafting", "draft", "reviewed", "validated", "merged")
STRICT_MERGE_STATUSES = {"validated", "merged"}
REVIEWED_MERGE_STATUSES = {"reviewed", "validated", "merged"}

REQUIRED_BLOCKS = (
    "##### Purpose",
    "##### Core Ideas",
    "##### Practical Guidance",
    "##### Trade-offs",
    "##### Examples",
    "##### Common Mistakes",
    "##### Review Checklist",
)

PLACEHOLDER_RE = re.compile(r"\bTODO\b|\bTBD\b|\[MISSING CONTENT\]", re.IGNORECASE)
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_'/.-]*")


@dataclass(frozen=True)
class SectionTask:
    volume_id: int
    volume_title: str
    chapter_id: str
    chapter_title: str
    section_id: str
    section_title: str

    @property
    def rel_path(self) -> Path:
        volume_slug = slugify(self.volume_title)
        section_slug = slugify(self.section_title)
        volume_folder = f"volume-{self.volume_id:02d}-{volume_slug}"
        filename = f"{self.section_id}-{section_slug}.md"
        return Path("parts") / volume_folder / filename


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-")
    return slug or "section"


def ensure_inside_workspace(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(SCRIPT_DIR)
    except ValueError as exc:
        raise ValueError(f"Refusing to write outside _codex: {resolved}") from exc
    return resolved


def workspace_path(value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = SCRIPT_DIR / path
    return ensure_inside_workspace(path)


def load_source(source: Path) -> dict[str, Any]:
    if not source.exists():
        raise FileNotFoundError(f"Source JSON not found: {source}")
    with source.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)
    if not isinstance(data, dict) or not isinstance(data.get("guide"), dict):
        raise ValueError("Expected top-level JSON object with a 'guide' object")
    return data


def iter_tasks(guide: dict[str, Any]) -> Iterable[SectionTask]:
    volumes = guide.get("volumes")
    if not isinstance(volumes, list):
        raise ValueError("Expected guide.volumes to be an array")

    for volume in volumes:
        chapters = volume.get("chapters")
        if not isinstance(chapters, list):
            raise ValueError(f"Expected chapters array in volume {volume.get('id')}")

        for chapter in chapters:
            sections = chapter.get("sections")
            if not isinstance(sections, list):
                raise ValueError(f"Expected sections array in chapter {chapter.get('id')}")

            for section in sections:
                yield SectionTask(
                    volume_id=int(volume["id"]),
                    volume_title=str(volume["title"]),
                    chapter_id=str(chapter["id"]),
                    chapter_title=str(chapter["title"]),
                    section_id=str(section["id"]),
                    section_title=str(section["title"]),
                )


def task_to_manifest_entry(task: SectionTask, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    existing = existing or {}
    now = utc_now()
    return {
        "id": task.section_id,
        "volume_id": task.volume_id,
        "volume_title": task.volume_title,
        "chapter_id": task.chapter_id,
        "chapter_title": task.chapter_title,
        "section_title": task.section_title,
        "status": existing.get("status", "pending"),
        "path": task.rel_path.as_posix(),
        "sha256": existing.get("sha256"),
        "created_at": existing.get("created_at", now),
        "updated_at": existing.get("updated_at", now),
        "validation": existing.get("validation", {}),
    }


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError("manifest.json not found. Run 'init' first.")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_manifest(manifest: dict[str, Any], path: Path = DEFAULT_MANIFEST) -> None:
    target = ensure_inside_workspace(path)
    temp_path = target.with_suffix(target.suffix + ".tmp")
    temp_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp_path.replace(target)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render_fragment(task: SectionTask, status: str = "pending") -> str:
    return f"""---
id: {task.section_id}
volume: {task.volume_title}
chapter: {task.chapter_title}
section: {task.section_title}
status: {status}
---

#### {task.section_id} {task.section_title}

##### Purpose

[MISSING CONTENT]

##### Core Ideas

[MISSING CONTENT]

##### Practical Guidance

[MISSING CONTENT]

##### Trade-offs

[MISSING CONTENT]

##### Examples

[MISSING CONTENT]

##### Common Mistakes

[MISSING CONTENT]

##### Review Checklist

- [ ] [MISSING CONTENT]
"""


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        return {}, text

    frontmatter: dict[str, str] = {}
    for line in lines[1:closing_index]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()

    body = "\n".join(lines[closing_index + 1 :]).lstrip()
    return frontmatter, body


def replace_frontmatter_status(text: str, status: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        return text

    changed = False
    for index in range(1, closing_index):
        if lines[index].startswith("status:"):
            lines[index] = f"status: {status}"
            changed = True
            break

    if not changed:
        lines.insert(closing_index, f"status: {status}")

    return "\n".join(lines) + "\n"


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def validate_fragment(entry: dict[str, Any], min_words: int) -> dict[str, Any]:
    errors: list[str] = []
    full_path = workspace_path(entry["path"])

    if not full_path.exists():
        return {
            "ok": False,
            "errors": [f"Missing fragment file: {entry['path']}"],
            "word_count": 0,
            "validated_at": utc_now(),
        }

    text = full_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)

    expected_frontmatter = {
        "id": entry["id"],
        "volume": entry["volume_title"],
        "chapter": entry["chapter_title"],
        "section": entry["section_title"],
    }

    for key, expected in expected_frontmatter.items():
        actual = frontmatter.get(key)
        if actual != str(expected):
            errors.append(f"Front matter '{key}' expected '{expected}', found '{actual}'")

    status = frontmatter.get("status", entry.get("status"))
    if status not in STATUSES:
        errors.append(f"Invalid status '{status}'")

    expected_heading = f"#### {entry['id']} {entry['section_title']}"
    if not body.startswith(expected_heading):
        errors.append(f"Body must start with '{expected_heading}'")

    for block in REQUIRED_BLOCKS:
        if block not in body:
            errors.append(f"Missing required block: {block}")

    if PLACEHOLDER_RE.search(body):
        errors.append("Contains TODO, TBD, or [MISSING CONTENT] placeholder")

    word_count = count_words(body)
    if word_count < min_words:
        errors.append(f"Word count {word_count} is below minimum {min_words}")

    return {
        "ok": not errors,
        "errors": errors,
        "word_count": word_count,
        "validated_at": utc_now(),
    }


def source_label(source: Path) -> str:
    resolved = source.resolve()
    try:
        return resolved.relative_to(ROOT_DIR).as_posix()
    except ValueError:
        return str(resolved)


def build_manifest(source: Path, guide: dict[str, Any], existing_manifest: dict[str, Any] | None) -> dict[str, Any]:
    existing_by_id: dict[str, dict[str, Any]] = {}
    if existing_manifest:
        existing_by_id = {str(task["id"]): task for task in existing_manifest.get("tasks", [])}

    tasks = [
        task_to_manifest_entry(task, existing_by_id.get(task.section_id))
        for task in iter_tasks(guide)
    ]

    stats = guide.get("stats", {})
    return {
        "source_json": source_label(source),
        "guide_title": guide.get("title", "Untitled Guide"),
        "structure": guide.get("structure", "Guide > Volume > Chapter > Section"),
        "stats": {
            "volumes": stats.get("volumes"),
            "chapters": stats.get("chapters"),
            "sections": stats.get("sections"),
            "manifest_tasks": len(tasks),
        },
        "created_at": (existing_manifest or {}).get("created_at", utc_now()),
        "updated_at": utc_now(),
        "tasks": tasks,
    }


def command_inspect(args: argparse.Namespace) -> int:
    data = load_source(Path(args.source))
    guide = data["guide"]
    tasks = list(iter_tasks(guide))
    volume_ids = {task.volume_id for task in tasks}
    chapter_ids = {task.chapter_id for task in tasks}

    print(f"Source: {Path(args.source)}")
    print(f"Title: {guide.get('title')}")
    print(f"Structure: {guide.get('structure')}")
    print(f"Volumes: {len(volume_ids)}")
    print(f"Chapters: {len(chapter_ids)}")
    print(f"Sections: {len(tasks)}")
    return 0


def command_init(args: argparse.Namespace) -> int:
    source = Path(args.source).resolve()
    data = load_source(source)
    guide = data["guide"]

    existing_manifest = None
    if DEFAULT_MANIFEST.exists():
        existing_manifest = load_manifest()

    manifest = build_manifest(source, guide, existing_manifest)

    created = 0
    skipped = 0
    for entry in manifest["tasks"]:
        full_path = workspace_path(entry["path"])
        if full_path.exists():
            skipped += 1
        else:
            if not args.dry_run:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                task = SectionTask(
                    volume_id=int(entry["volume_id"]),
                    volume_title=entry["volume_title"],
                    chapter_id=entry["chapter_id"],
                    chapter_title=entry["chapter_title"],
                    section_id=entry["id"],
                    section_title=entry["section_title"],
                )
                full_path.write_text(render_fragment(task), encoding="utf-8")
            created += 1

        entry["sha256"] = sha256_file(full_path)

    if not args.dry_run:
        (SCRIPT_DIR / "output").mkdir(exist_ok=True)
        save_manifest(manifest)

    mode = "dry run" if args.dry_run else "created"
    print(f"Init {mode}: {created} new fragments, {skipped} existing fragments")
    print(f"Manifest tasks: {len(manifest['tasks'])}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    counts = {status: 0 for status in STATUSES}
    unknown = 0

    for task in manifest.get("tasks", []):
        status = task.get("status")
        if status in counts:
            counts[status] += 1
        else:
            unknown += 1

    print(f"Guide: {manifest.get('guide_title')}")
    print(f"Tasks: {len(manifest.get('tasks', []))}")
    for status in STATUSES:
        print(f"{status}: {counts[status]}")
    if unknown:
        print(f"unknown: {unknown}")

    next_task = next((task for task in manifest.get("tasks", []) if task.get("status") != "merged"), None)
    if next_task:
        print(f"Next: {next_task['id']} {next_task['section_title']}")
        print(f"Path: {next_task['path']}")
    return 0


def command_progress(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    tasks = manifest.get("tasks", [])
    counts = {status: 0 for status in STATUSES}

    for task in tasks:
        status = task.get("status")
        if status in counts:
            counts[status] += 1

    total = len(tasks)
    completed = counts["merged"]
    validated_or_better = counts["validated"] + counts["merged"]
    reviewed_or_better = counts["reviewed"] + validated_or_better
    percent = (completed / total * 100) if total else 0

    print(f"Guide: {manifest.get('guide_title')}")
    print(f"Progress: {completed}/{total} merged ({percent:.1f}%)")
    print(f"Reviewed or better: {reviewed_or_better}/{total}")
    print(f"Validated or better: {validated_or_better}/{total}")
    for status in STATUSES:
        print(f"{status}: {counts[status]}")

    next_task = next((task for task in tasks if task.get("status") != "merged"), None)
    if next_task:
        print(f"Next task: {next_task['id']} {next_task['section_title']}")
        print(f"Next path: {next_task['path']}")
    else:
        print("Next task: none")

    output_path = DEFAULT_OUTPUT
    if output_path.exists():
        print(f"Output: {output_path}")
        print(f"Output bytes: {output_path.stat().st_size}")
    else:
        print("Output: not created")

    return 0


def command_next(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    wanted = set(args.status)
    task = next((item for item in manifest.get("tasks", []) if item.get("status") in wanted), None)

    if not task:
        print(f"No task found with status: {', '.join(args.status)}")
        return 0

    print(f"{task['id']} {task['section_title']}")
    print(f"Volume: {task['volume_id']} {task['volume_title']}")
    print(f"Chapter: {task['chapter_id']} {task['chapter_title']}")
    print(f"Path: {task['path']}")

    if args.mark_drafting:
        task["status"] = "drafting"
        task["updated_at"] = utc_now()
        full_path = workspace_path(task["path"])
        if full_path.exists():
            text = full_path.read_text(encoding="utf-8")
            full_path.write_text(replace_frontmatter_status(text, "drafting"), encoding="utf-8")
            task["sha256"] = sha256_file(full_path)
        manifest["updated_at"] = utc_now()
        save_manifest(manifest)
        print("Marked as drafting")

    return 0


def command_mark(args: argparse.Namespace) -> int:
    if args.status not in STATUSES:
        print(f"Invalid status: {args.status}", file=sys.stderr)
        return 2

    manifest = load_manifest()
    task = next((item for item in manifest.get("tasks", []) if item.get("id") == args.section_id), None)
    if not task:
        print(f"Section not found: {args.section_id}", file=sys.stderr)
        return 1

    task["status"] = args.status
    task["updated_at"] = utc_now()

    full_path = workspace_path(task["path"])
    if full_path.exists():
        text = full_path.read_text(encoding="utf-8")
        full_path.write_text(replace_frontmatter_status(text, args.status), encoding="utf-8")
        task["sha256"] = sha256_file(full_path)

    manifest["updated_at"] = utc_now()
    save_manifest(manifest)
    print(f"Marked {args.section_id} as {args.status}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    tasks = manifest.get("tasks", [])
    if args.status:
        tasks = [task for task in tasks if task.get("status") in set(args.status)]

    ok_count = 0
    fail_count = 0
    printed_errors = 0

    for task in tasks:
        result = validate_fragment(task, args.min_words)
        task["validation"] = result
        task["sha256"] = sha256_file(workspace_path(task["path"]))
        task["updated_at"] = utc_now()

        if result["ok"]:
            ok_count += 1
            if args.promote and task.get("status") == "reviewed":
                task["status"] = "validated"
        else:
            fail_count += 1
            if printed_errors < args.max_errors:
                print(f"[FAIL] {task['id']} {task['section_title']}")
                for error in result["errors"]:
                    print(f"  - {error}")
                printed_errors += 1

    manifest["updated_at"] = utc_now()
    save_manifest(manifest)

    print(f"Validated: {ok_count} ok, {fail_count} failed")
    if fail_count and printed_errors >= args.max_errors:
        print(f"Error output limited to {args.max_errors} failed fragments")
    return 1 if fail_count else 0


def body_without_frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    _, body = split_frontmatter(text)
    return body.strip()


def command_merge(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    tasks = manifest.get("tasks", [])

    if args.allow_incomplete:
        allowed_statuses = set(STATUSES)
    elif args.allow_reviewed:
        allowed_statuses = REVIEWED_MERGE_STATUSES
    else:
        allowed_statuses = STRICT_MERGE_STATUSES

    errors: list[str] = []
    for task in tasks:
        status = task.get("status")
        if status not in allowed_statuses:
            errors.append(f"{task['id']} has status '{status}'")
            continue

        full_path = workspace_path(task["path"])
        if not full_path.exists():
            errors.append(f"{task['id']} missing file {task['path']}")
            continue

        validation = task.get("validation", {})
        if not args.allow_incomplete and not validation.get("ok"):
            errors.append(f"{task['id']} has not passed validation")

    if errors and not args.allow_incomplete:
        print("Merge refused:")
        for error in errors[: args.max_errors]:
            print(f"  - {error}")
        if len(errors) > args.max_errors:
            print(f"  ... {len(errors) - args.max_errors} more")
        return 1

    lines: list[str] = []
    lines.append(f"# {manifest.get('guide_title', 'Untitled Guide')}")
    lines.append("")
    lines.append(f"Generated from `{manifest.get('source_json')}`.")
    lines.append("")

    current_volume: tuple[int, str] | None = None
    current_chapter: tuple[str, str] | None = None

    for task in tasks:
        volume = (int(task["volume_id"]), task["volume_title"])
        chapter = (task["chapter_id"], task["chapter_title"])

        if volume != current_volume:
            lines.append(f"## Volume {volume[0]}: {volume[1]}")
            lines.append("")
            current_volume = volume
            current_chapter = None

        if chapter != current_chapter:
            lines.append(f"### {chapter[0]} {chapter[1]}")
            lines.append("")
            current_chapter = chapter

        full_path = workspace_path(task["path"])
        if full_path.exists():
            lines.append(body_without_frontmatter(full_path))
        else:
            lines.append(f"#### {task['id']} {task['section_title']}")
            lines.append("")
            lines.append("[MISSING CONTENT]")
        lines.append("")

    output_path = workspace_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    if args.mark_merged and not args.allow_incomplete:
        for task in tasks:
            task["status"] = "merged"
            task["updated_at"] = utc_now()
        manifest["updated_at"] = utc_now()
        save_manifest(manifest)

    print(f"Wrote {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default=str(DEFAULT_SOURCE),
        help="Source JSON path. Defaults to the root guide JSON.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect source JSON without writing files")
    inspect_parser.set_defaults(func=command_inspect)

    init_parser = subparsers.add_parser("init", help="Create manifest and empty section fragments")
    init_parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    init_parser.set_defaults(func=command_init)

    status_parser = subparsers.add_parser("status", help="Show progress summary")
    status_parser.set_defaults(func=command_status)

    progress_parser = subparsers.add_parser("progress", help="Show detailed progress and output state")
    progress_parser.set_defaults(func=command_progress)

    next_parser = subparsers.add_parser("next", help="Show the next task to work on")
    next_parser.add_argument(
        "--status",
        nargs="+",
        default=["pending"],
        choices=STATUSES,
        help="Statuses eligible for selection",
    )
    next_parser.add_argument("--mark-drafting", action="store_true", help="Mark selected task as drafting")
    next_parser.set_defaults(func=command_next)

    mark_parser = subparsers.add_parser("mark", help="Set progress status for a section")
    mark_parser.add_argument("section_id", help="Section ID, for example 1.1.1")
    mark_parser.add_argument("status", choices=STATUSES, help="New status")
    mark_parser.set_defaults(func=command_mark)

    validate_parser = subparsers.add_parser("validate", help="Validate section fragments")
    validate_parser.add_argument("--status", nargs="+", choices=STATUSES, help="Validate only these statuses")
    validate_parser.add_argument("--min-words", type=int, default=220, help="Minimum section body word count")
    validate_parser.add_argument("--max-errors", type=int, default=50, help="Maximum failed fragments to print")
    validate_parser.add_argument(
        "--promote",
        action="store_true",
        help="Promote reviewed fragments that pass validation to validated",
    )
    validate_parser.set_defaults(func=command_validate)

    merge_parser = subparsers.add_parser("merge", help="Merge fragments into final Markdown")
    merge_parser.add_argument("--output", default=str(DEFAULT_OUTPUT.relative_to(SCRIPT_DIR)), help="Output path under _codex")
    merge_parser.add_argument("--allow-reviewed", action="store_true", help="Allow reviewed fragments in merge")
    merge_parser.add_argument("--allow-incomplete", action="store_true", help="Allow incomplete preview merge")
    merge_parser.add_argument("--mark-merged", action="store_true", help="Mark tasks as merged after strict merge")
    merge_parser.add_argument("--max-errors", type=int, default=50, help="Maximum merge errors to print")
    merge_parser.set_defaults(func=command_merge)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
