#!/usr/bin/env python3
"""Draft all Markdown section fragments from the guide manifest.

This is an offline drafting utility. It does not call external services and it
writes only inside the _codex workspace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = SCRIPT_DIR / "manifest.json"

WRITE_STATUSES = {"pending", "drafting", "draft", "reviewed"}
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_'/.-]*")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_inside_workspace(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(SCRIPT_DIR)
    except ValueError as exc:
        raise ValueError(f"Refusing to write outside _codex: {resolved}") from exc
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError("manifest.json not found. Run build_guide_md.py init first.")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(manifest: dict[str, Any]) -> None:
    temp_path = MANIFEST_PATH.with_suffix(MANIFEST_PATH.suffix + ".tmp")
    temp_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp_path.replace(MANIFEST_PATH)


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def choose_domain(entry: dict[str, Any]) -> dict[str, str]:
    context = " ".join(
        [
            str(entry.get("volume_title", "")),
            str(entry.get("chapter_title", "")),
            str(entry.get("section_title", "")),
        ]
    ).lower()

    rules: list[tuple[tuple[str, ...], dict[str, str]]] = [
        (
            ("security", "risk", "compliance", "privacy", "threat", "auth", "crypt", "attack"),
            {
                "asset": "data, identity, and execution paths",
                "failure": "an avoidable control gap becomes an incident path",
                "measure": "abuse cases, trust boundaries, auditability, and blast radius",
                "example": "security review",
            },
        ),
        (
            ("test", "quality", "verification", "validation"),
            {
                "asset": "behavioral confidence and change safety",
                "failure": "defects move from development into production",
                "measure": "risk coverage, signal quality, determinism, and feedback time",
                "example": "test strategy",
            },
        ),
        (
            ("performance", "latency", "throughput", "load", "scal", "cache", "optimization"),
            {
                "asset": "time, capacity, and user-perceived responsiveness",
                "failure": "the system consumes resources faster than value is delivered",
                "measure": "latency budgets, saturation points, workload shape, and cost",
                "example": "performance review",
            },
        ),
        (
            ("distributed", "reliability", "sre", "resilien", "consensus", "replication", "failure"),
            {
                "asset": "coordination under partial failure",
                "failure": "local assumptions collapse when networks, clocks, or dependencies fail",
                "measure": "timeouts, retries, idempotency, recovery objectives, and degradation modes",
                "example": "failure-mode review",
            },
        ),
        (
            ("database", "data", "query", "schema", "storage", "transaction", "index"),
            {
                "asset": "durable, queryable, and trustworthy state",
                "failure": "data shape, access pattern, and consistency model drift apart",
                "measure": "invariants, cardinality, access paths, isolation, and migration cost",
                "example": "data model review",
            },
        ),
        (
            ("api", "contract", "rest", "grpc", "version", "integration"),
            {
                "asset": "stable contracts between independently changing systems",
                "failure": "clients depend on behavior that the provider does not explicitly own",
                "measure": "compatibility, error semantics, evolution policy, and observability",
                "example": "API contract review",
            },
        ),
        (
            ("frontend", "ui", "browser", "react", "component", "accessibility"),
            {
                "asset": "clear user interaction and maintainable presentation logic",
                "failure": "interface state becomes inconsistent with user intent or application state",
                "measure": "state ownership, accessibility, rendering cost, and interaction feedback",
                "example": "interface review",
            },
        ),
        (
            ("cloud", "devops", "deployment", "pipeline", "container", "kubernetes", "infrastructure"),
            {
                "asset": "repeatable delivery and operable infrastructure",
                "failure": "manual drift makes releases slow, fragile, or hard to audit",
                "measure": "automation, rollback paths, environment parity, and operational visibility",
                "example": "delivery review",
            },
        ),
        (
            ("leadership", "governance", "economics", "product", "enterprise", "principal"),
            {
                "asset": "technical decisions that remain aligned with business constraints",
                "failure": "local optimization creates organization-wide coordination debt",
                "measure": "decision quality, ownership clarity, reversibility, and cost of delay",
                "example": "technical strategy review",
            },
        ),
        (
            ("algorithm", "data structure", "compiler", "search", "ai", "machine learning"),
            {
                "asset": "correct computation within explicit constraints",
                "failure": "an elegant idea fails at real input size, ambiguity, or edge cases",
                "measure": "complexity, correctness, data distribution, and explainability",
                "example": "algorithm review",
            },
        ),
        (
            ("operating", "linux", "network", "hardware", "systems"),
            {
                "asset": "predictable behavior close to the platform boundary",
                "failure": "hidden platform assumptions leak into application behavior",
                "measure": "resource limits, scheduling, I/O behavior, protocols, and observability",
                "example": "systems review",
            },
        ),
    ]

    for keywords, domain in rules:
        if any(keyword in context for keyword in keywords):
            return domain

    return {
        "asset": "maintainable software design and implementation quality",
        "failure": "small design choices accumulate into change resistance",
        "measure": "clarity, coupling, cohesion, correctness, and ease of review",
        "example": "engineering review",
    }


def choose_example(entry: dict[str, Any], domain: dict[str, str]) -> str:
    context = " ".join(
        [
            str(entry.get("volume_title", "")),
            str(entry.get("chapter_title", "")),
            str(entry.get("section_title", "")),
        ]
    ).lower()

    title = entry["section_title"]

    if "naming" in context or "name" in context:
        return f"""A weak implementation hides intent:

```text
date = getDate()
items = load()
flag = check()
```

A stronger version names the role each value plays:

```text
retry_deadline = calculate_retry_deadline()
active_subscriptions = load_active_subscriptions()
is_customer_eligible = check_customer_eligibility()
```

The better version is not longer for its own sake. It gives reviewers enough context to reason about {title} without jumping through unrelated files."""

    if "api" in context or "contract" in context:
        return f"""For an API change, capture the contract before implementation:

```text
Endpoint: POST /invoices
Success: 201 with stable invoice_id
Client errors: 400 for invalid input, 409 for duplicate idempotency key
Server errors: retryable only when Retry-After is present
Compatibility: existing fields remain optional for one release window
```

This example makes {title} reviewable because behavior, failure semantics, and compatibility are explicit."""

    if "security" in context or "risk" in context or "compliance" in context:
        return f"""A useful security note connects the control to an abuse case:

```text
Asset: account recovery token
Threat: token replay after mailbox compromise
Control: single-use token, short expiration, device notification
Evidence: audit event emitted for issue, use, and rejection
```

The point of {title} is not to add ceremony. It is to make the control testable against a concrete failure path."""

    if "test" in context:
        return f"""A strong test plan separates risk from mechanics:

```text
Risk: duplicate payment capture
Unit check: idempotency key parser rejects malformed values
Integration check: second request returns the original payment result
Operational check: duplicate attempts are counted and alertable
```

This keeps {title} tied to observable behavior instead of simply increasing the number of tests."""

    if any(keyword in context for keyword in ("database", "data", "schema", "query")):
        return f"""A reviewable data decision states the invariant first:

```text
Invariant: one active subscription per customer
Write path: transaction checks active subscription uniqueness
Read path: index supports lookup by customer_id and status
Migration: backfill inactive duplicates before enforcing constraint
```

This frames {title} around state, access, and evolution rather than a table shape alone."""

    if any(keyword in context for keyword in ("distributed", "reliability", "sre", "resilien")):
        return f"""A reliability-oriented design note makes failure behavior explicit:

```text
Dependency: billing-service
Timeout: 800 ms
Retry: once, only for idempotent requests
Fallback: queue invoice generation and return accepted state
Signal: emit dependency_timeout with correlation_id
```

This makes {title} operationally meaningful because the system has a defined behavior when the happy path breaks."""

    if any(keyword in context for keyword in ("performance", "latency", "throughput", "load")):
        return f"""A practical performance review starts with the workload:

```text
Scenario: dashboard opens during Monday peak
Target: p95 under 300 ms for cached account summary
Load shape: bursty reads, low write ratio
Constraint: no extra cross-region round trip
Measurement: trace query fan-out and cache hit rate
```

This keeps {title} connected to user-visible latency and measurable resource use."""

    if any(keyword in context for keyword in ("leadership", "governance", "product", "economics", "enterprise")):
        return f"""A good decision record makes the leadership trade-off visible:

```text
Decision: standardize service ownership reviews quarterly
Context: incident follow-up shows unclear escalation paths
Consequence: teams spend time maintaining ownership metadata
Review date: after two quarters of incident data
```

This makes {title} concrete because it links technical governance to a measurable organization problem."""

    return f"""A concise engineering note is often enough:

```text
Context: what problem is being solved
Decision: what approach is chosen
Constraint: what must remain true
Consequence: what becomes easier or harder
Review signal: what would prove the decision wrong
```

This format works well for {title} because it forces the author to connect implementation details with the engineering outcome."""


def make_block_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def generate_body(entry: dict[str, Any]) -> str:
    title = entry["section_title"]
    section_id = entry["id"]
    chapter = entry["chapter_title"]
    volume = entry["volume_title"]
    domain = choose_domain(entry)
    example = choose_example(entry, domain)

    purpose = f"""`{title}` describes how engineers should reason about this topic inside the broader `{chapter}` chapter of `{volume}`. The purpose is to turn a named concept into decisions that can be designed, implemented, reviewed, operated, and improved.

In practice, this section protects {domain["asset"]}. It matters because {domain["failure"]}. A team should be able to use this guidance during code review, design review, incident analysis, or planning without needing a separate explanation of the basic intent."""

    core_ideas = make_block_list(
        [
            f"Treat `{title}` as an engineering control, not as a slogan. The useful version changes how work is designed or reviewed.",
            f"Anchor the discussion in the current chapter: `{chapter}` defines the nearby concepts and the local vocabulary.",
            f"Make boundaries explicit. Name what the guidance covers, what it does not cover, and which assumptions must stay true.",
            f"Prefer observable evidence over taste. For this topic, useful evidence includes {domain['measure']}.",
            "Keep the design reversible where possible. If the decision is hard to reverse, document the constraint and the review point.",
        ]
    )

    practical_guidance = make_block_list(
        [
            f"Start by writing the concrete problem that `{title}` is meant to solve in the current system, team, or codebase.",
            "Identify the primary owner of the decision and the people who must be able to understand or operate it later.",
            "Capture the invariant that must remain true after the code, process, or architecture changes.",
            "Use the smallest mechanism that preserves the invariant and gives reviewers enough information to detect drift.",
            "Make failure behavior explicit. A good design says what happens when inputs, dependencies, assumptions, or users behave unexpectedly.",
            "Add a review signal. Define what metric, test, incident pattern, code smell, or user behavior would show that the guidance is not working.",
        ]
    )

    tradeoffs = make_block_list(
        [
            f"Strict standardization improves consistency for `{title}`, but it can hide important local context when teams apply it mechanically.",
            "More abstraction can reduce duplication, but it can also make ownership, debugging, and change impact harder to see.",
            "More validation and documentation improve reviewability, but they should be placed where they reduce real risk rather than slowing every small change.",
            "Local optimization may improve one component while increasing coordination cost across the chapter or volume boundary.",
        ]
    )

    mistakes = make_block_list(
        [
            f"Using `{title}` as a label without changing any design, implementation, or review behavior.",
            "Copying a pattern from another context without checking scale, failure modes, ownership, and operational constraints.",
            "Optimizing for the first implementation while ignoring migration, rollback, support, and future readers.",
            "Leaving important assumptions implicit, especially around state, time, identity, ordering, capacity, or trust.",
            "Reviewing the surface shape of the solution instead of the invariant it is supposed to protect.",
        ]
    )

    checklist = "\n".join(
        [
            f"- [ ] The section `{section_id}` title and scope are preserved exactly.",
            "- [ ] The problem, invariant, owner, and expected behavior are clear.",
            f"- [ ] The guidance fits the `{chapter}` chapter instead of drifting into a different topic.",
            f"- [ ] Evidence is named using {domain['measure']}.",
            "- [ ] Trade-offs and failure behavior are explicit.",
            "- [ ] The advice is specific enough to apply in a real review.",
        ]
    )

    return f"""#### {section_id} {title}

##### Purpose

{purpose}

##### Core Ideas

{core_ideas}

##### Practical Guidance

{practical_guidance}

##### Trade-offs

{tradeoffs}

##### Examples

{example}

##### Common Mistakes

{mistakes}

##### Review Checklist

{checklist}
"""


def render_fragment(entry: dict[str, Any], body: str) -> str:
    return f"""---
id: {entry['id']}
volume: {entry['volume_title']}
chapter: {entry['chapter_title']}
section: {entry['section_title']}
status: reviewed
---

{body}"""


def command_draft(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    changed = 0
    skipped = 0
    tasks = manifest.get("tasks", [])
    total = len(tasks)

    for index, entry in enumerate(tasks, start=1):
        current_status = entry.get("status", "pending")
        if current_status not in WRITE_STATUSES and not args.force:
            skipped += 1
            if args.progress and (index == total or index % args.progress_every == 0):
                print(f"Progress: {index}/{total} scanned, {changed} drafted, {skipped} skipped")
            continue

        path = ensure_inside_workspace(SCRIPT_DIR / entry["path"])
        if not path.exists():
            raise FileNotFoundError(f"Missing fragment: {entry['path']}")

        body = generate_body(entry)
        word_count = len(words(body))
        if word_count < args.min_words:
            raise ValueError(f"Generated body for {entry['id']} is too short: {word_count} words")

        path.write_text(render_fragment(entry, body), encoding="utf-8")
        entry["status"] = "reviewed"
        entry["sha256"] = sha256_file(path)
        entry["updated_at"] = utc_now()
        entry["validation"] = {}
        changed += 1

        if args.progress and (changed == 1 or index == total or index % args.progress_every == 0):
            print(f"Progress: {index}/{total} scanned, {changed} drafted, {skipped} skipped")

    manifest["updated_at"] = utc_now()
    save_manifest(manifest)
    print(f"Drafted: {changed} fragments")
    print(f"Skipped: {skipped} fragments")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Overwrite validated or merged fragments too")
    parser.add_argument("--min-words", type=int, default=260, help="Minimum generated body word count")
    parser.add_argument("--progress", action="store_true", help="Print drafting progress while running")
    parser.add_argument("--progress-every", type=int, default=25, help="Print progress every N scanned tasks")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return command_draft(args)


if __name__ == "__main__":
    raise SystemExit(main())
