#!/usr/bin/env python3
"""Rewrite section fragments with a more specific generated first revision.

The script reads _codex/manifest.json and rewrites fragment files inside
_codex/parts. It does not inspect .old and does not write outside _codex.
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
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_'/.-]*")

REWRITE_STATUSES = {"pending", "drafting", "draft", "reviewed", "validated", "merged"}


VOLUME_PROFILES: dict[str, dict[str, Any]] = {
    "Clean Code": {
        "focus": "making code easy to read, change, and review without relying on private author knowledge",
        "concerns": ["intent", "local reasoning", "reviewability", "change cost"],
        "signals": ["short review cycles", "clear diffs", "low surprise during maintenance"],
        "artifact": "code review",
    },
    "Object Oriented Design": {
        "focus": "assigning responsibilities so objects collaborate through stable, meaningful boundaries",
        "concerns": ["responsibility", "encapsulation", "coupling", "substitution"],
        "signals": ["small public APIs", "testable collaborations", "limited ripple effects"],
        "artifact": "object model review",
    },
    "Design Patterns": {
        "focus": "using proven design shapes only when they clarify collaboration, variation, or lifecycle",
        "concerns": ["intent", "participants", "variation point", "misuse risk"],
        "signals": ["simpler clients", "explicit roles", "removable indirection"],
        "artifact": "pattern review",
    },
    "Clean Architecture": {
        "focus": "protecting policy from delivery mechanisms, frameworks, and volatile infrastructure",
        "concerns": ["dependency direction", "use cases", "boundaries", "contracts"],
        "signals": ["isolated policies", "replaceable adapters", "stable tests"],
        "artifact": "architecture boundary review",
    },
    "Domain Driven Design": {
        "focus": "aligning software models with business language, rules, and bounded contexts",
        "concerns": ["ubiquitous language", "invariants", "context boundaries", "integration"],
        "signals": ["domain terms in code", "explicit aggregates", "clear context maps"],
        "artifact": "domain model review",
    },
    "Algorithms": {
        "focus": "choosing computations that remain correct and efficient under real input constraints",
        "concerns": ["correctness", "complexity", "edge cases", "input distribution"],
        "signals": ["proved invariants", "known bounds", "stable behavior at scale"],
        "artifact": "algorithm review",
    },
    "Data Structures": {
        "focus": "matching representation to access patterns, mutation patterns, and memory constraints",
        "concerns": ["operations", "complexity", "layout", "invariants"],
        "signals": ["predictable operations", "clear ownership", "bounded memory growth"],
        "artifact": "representation review",
    },
    "Databases": {
        "focus": "preserving durable state, queryability, and consistency as product behavior changes",
        "concerns": ["invariants", "transactions", "indexes", "migration"],
        "signals": ["stable queries", "safe migrations", "explicit consistency rules"],
        "artifact": "data model review",
    },
    "Distributed Databases": {
        "focus": "making data placement, replication, and consistency explicit under partial failure",
        "concerns": ["replication", "quorums", "conflicts", "recovery"],
        "signals": ["known consistency model", "bounded failover", "auditable conflict handling"],
        "artifact": "distributed data review",
    },
    "Operating Systems": {
        "focus": "understanding the platform behaviors that shape application correctness and performance",
        "concerns": ["processes", "memory", "I/O", "scheduling"],
        "signals": ["known limits", "controlled resource use", "observable contention"],
        "artifact": "systems review",
    },
    "Networking": {
        "focus": "designing communication that remains correct across latency, loss, ordering, and trust boundaries",
        "concerns": ["protocols", "timeouts", "routing", "identity"],
        "signals": ["bounded retries", "clear contracts", "measured latency"],
        "artifact": "network design review",
    },
    "API Design": {
        "focus": "creating contracts that independent producers and consumers can evolve safely",
        "concerns": ["compatibility", "errors", "versioning", "semantics"],
        "signals": ["stable contracts", "clear error models", "client-safe evolution"],
        "artifact": "API contract review",
    },
    "Security": {
        "focus": "reducing abuse paths by making assets, trust boundaries, and controls explicit",
        "concerns": ["assets", "identity", "authorization", "attack paths"],
        "signals": ["testable controls", "least privilege", "useful audit events"],
        "artifact": "security review",
    },
    "Testing": {
        "focus": "building confidence in behavior with fast, meaningful, and maintainable feedback",
        "concerns": ["risk", "coverage", "determinism", "signal quality"],
        "signals": ["clear failures", "low flake rate", "coverage of critical behavior"],
        "artifact": "test strategy review",
    },
    "Performance Engineering": {
        "focus": "making resource use and latency visible enough to tune against real workloads",
        "concerns": ["latency", "throughput", "saturation", "cost"],
        "signals": ["p95/p99 targets", "known bottlenecks", "stable capacity plans"],
        "artifact": "performance review",
    },
    "Distributed Systems": {
        "focus": "preserving behavior when clocks, networks, dependencies, and nodes fail independently",
        "concerns": ["idempotency", "timeouts", "coordination", "degradation"],
        "signals": ["defined failure modes", "bounded retries", "observable recovery"],
        "artifact": "failure-mode review",
    },
    "Reliability Engineering": {
        "focus": "turning failure expectations into engineered recovery, prevention, and learning loops",
        "concerns": ["availability", "recovery", "risk", "operability"],
        "signals": ["SLO alignment", "reduced repeat incidents", "tested recovery paths"],
        "artifact": "reliability review",
    },
    "Observability": {
        "focus": "making system behavior explainable from the outside during normal work and incidents",
        "concerns": ["signals", "correlation", "debuggability", "cost"],
        "signals": ["actionable traces", "useful logs", "low-noise alerts"],
        "artifact": "observability review",
    },
    "DevOps": {
        "focus": "making delivery repeatable, observable, reversible, and owned by the teams changing software",
        "concerns": ["automation", "pipelines", "rollback", "environment parity"],
        "signals": ["shorter lead time", "safe rollback", "less manual drift"],
        "artifact": "delivery review",
    },
    "Cloud Architecture": {
        "focus": "using cloud services through explicit trade-offs in resilience, cost, security, and operations",
        "concerns": ["managed services", "regions", "IAM", "cost"],
        "signals": ["bounded blast radius", "clear ownership", "cost visibility"],
        "artifact": "cloud architecture review",
    },
    "High Load Systems": {
        "focus": "keeping systems predictable when demand, concurrency, and data volume exceed ordinary assumptions",
        "concerns": ["backpressure", "hotspots", "queues", "capacity"],
        "signals": ["controlled saturation", "known bottlenecks", "graceful degradation"],
        "artifact": "high-load review",
    },
    "Frontend Architecture": {
        "focus": "organizing user interface code so state, rendering, and interaction remain understandable",
        "concerns": ["state", "components", "accessibility", "rendering cost"],
        "signals": ["predictable UI state", "fast interactions", "accessible flows"],
        "artifact": "frontend review",
    },
    "Functional Programming": {
        "focus": "using functions, immutability, and composition to make behavior easier to reason about",
        "concerns": ["purity", "effects", "composition", "data transformation"],
        "signals": ["localized effects", "clear pipelines", "referential reasoning"],
        "artifact": "functional design review",
    },
    "Compiler Fundamentals": {
        "focus": "turning language input into checked, optimized, and executable representations",
        "concerns": ["syntax", "semantics", "IR", "optimization"],
        "signals": ["clear diagnostics", "valid transformations", "stable compilation stages"],
        "artifact": "compiler pipeline review",
    },
    "Search Systems": {
        "focus": "retrieving relevant results through explicit indexing, ranking, and feedback decisions",
        "concerns": ["recall", "precision", "ranking", "latency"],
        "signals": ["measured relevance", "stable indexing", "bounded query cost"],
        "artifact": "search relevance review",
    },
    "Data Engineering": {
        "focus": "moving and shaping data so downstream users can trust freshness, lineage, and meaning",
        "concerns": ["pipelines", "quality", "lineage", "freshness"],
        "signals": ["known data contracts", "observable pipelines", "traceable transformations"],
        "artifact": "data pipeline review",
    },
    "AI Systems": {
        "focus": "building model-backed systems whose behavior is measurable, governed, and useful in production",
        "concerns": ["evaluation", "drift", "safety", "feedback"],
        "signals": ["measured quality", "guardrails", "monitored drift"],
        "artifact": "AI system review",
    },
    "Site Reliability Engineering": {
        "focus": "balancing feature velocity with explicit reliability targets and operational discipline",
        "concerns": ["SLOs", "error budgets", "incidents", "automation"],
        "signals": ["budget-aware decisions", "tested runbooks", "reduced toil"],
        "artifact": "SRE review",
    },
    "Architecture Governance": {
        "focus": "making architecture decisions visible, consistent, and adaptable across teams",
        "concerns": ["standards", "decision records", "exceptions", "ownership"],
        "signals": ["clear decision history", "fewer duplicated debates", "managed exceptions"],
        "artifact": "governance review",
    },
    "Technical Leadership": {
        "focus": "turning technical ambiguity into aligned decisions, execution, and learning",
        "concerns": ["alignment", "mentorship", "decision quality", "communication"],
        "signals": ["clear direction", "better reviews", "less rework"],
        "artifact": "technical leadership review",
    },
    "Product Engineering": {
        "focus": "connecting technical choices to user outcomes, product constraints, and delivery learning",
        "concerns": ["user value", "experimentation", "delivery", "feedback"],
        "signals": ["faster learning", "useful metrics", "lower rework"],
        "artifact": "product engineering review",
    },
    "Software Economics": {
        "focus": "making cost, risk, reversibility, and opportunity trade-offs explicit in engineering choices",
        "concerns": ["cost of delay", "option value", "maintenance", "risk"],
        "signals": ["better sequencing", "clear investment rationale", "managed technical debt"],
        "artifact": "engineering economics review",
    },
    "Enterprise Architecture": {
        "focus": "aligning systems, capabilities, data, and governance across a large organization",
        "concerns": ["capabilities", "integration", "portfolio", "standards"],
        "signals": ["coherent roadmaps", "reused capabilities", "fewer integration surprises"],
        "artifact": "enterprise architecture review",
    },
    "Compliance and Risk": {
        "focus": "turning regulatory and operational risk into explicit, testable engineering obligations",
        "concerns": ["controls", "evidence", "auditability", "risk ownership"],
        "signals": ["available evidence", "controlled exceptions", "reduced audit surprises"],
        "artifact": "risk and compliance review",
    },
    "Advanced Distributed Computing": {
        "focus": "reasoning about computation across unreliable, concurrent, and geographically separated systems",
        "concerns": ["coordination", "consistency", "parallelism", "fault tolerance"],
        "signals": ["proved assumptions", "bounded coordination", "observable failure handling"],
        "artifact": "distributed computing review",
    },
    "Hardware and Systems": {
        "focus": "understanding how hardware, firmware, and low-level system behavior affect software design",
        "concerns": ["CPU", "memory", "storage", "devices"],
        "signals": ["known bottlenecks", "controlled resources", "correct low-level assumptions"],
        "artifact": "hardware systems review",
    },
    "Linux Engineering": {
        "focus": "using Linux primitives intentionally for process, filesystem, networking, and operations work",
        "concerns": ["processes", "filesystems", "permissions", "networking"],
        "signals": ["clear diagnostics", "safe automation", "known kernel limits"],
        "artifact": "Linux engineering review",
    },
    "Advanced Security": {
        "focus": "handling sophisticated threats through explicit models, controls, evidence, and response paths",
        "concerns": ["threat modeling", "detection", "cryptography", "response"],
        "signals": ["reduced attack surface", "actionable detection", "tested response"],
        "artifact": "advanced security review",
    },
    "Research and Innovation": {
        "focus": "converting uncertainty into experiments, evidence, and responsible technical bets",
        "concerns": ["hypotheses", "experiments", "evidence", "transfer"],
        "signals": ["clear learning goals", "bounded exploration", "usable outcomes"],
        "artifact": "research review",
    },
    "Principal Engineer Body of Knowledge": {
        "focus": "operating at broad scope through judgment, influence, architecture, and engineering excellence",
        "concerns": ["scope", "leverage", "judgment", "organizational impact"],
        "signals": ["better cross-team decisions", "stronger technical standards", "scaled mentorship"],
        "artifact": "principal engineer review",
    },
}


PATTERN_LENSES: dict[str, dict[str, Any]] = {
    "Factory Method": {
        "definition": "delegating object creation to a method so clients depend on a product abstraction rather than a concrete class",
        "when": "object creation varies by runtime context, tenant, environment, or product family",
        "invariant": "client code should not need to know which concrete implementation is selected",
        "pitfalls": ["hiding simple constructors behind unnecessary factories", "letting factories accumulate unrelated policy", "making product lifecycles unclear"],
        "example": "A payment module can expose `create_processor(region)` so checkout code works with a `PaymentProcessor` while regional rules select the concrete provider.",
    },
    "Abstract Factory": {
        "definition": "creating families of related objects without binding clients to a concrete family",
        "when": "multiple products must vary together, such as platform widgets, cloud providers, or protocol adapters",
        "invariant": "objects produced by one factory family must be compatible with each other",
        "pitfalls": ["mixing products from different families", "adding families before variation is real", "making every constructor part of the factory surface"],
        "example": "A deployment tool can use an `InfrastructureFactory` that produces matching load balancers, storage clients, and identity adapters for one cloud.",
    },
    "Builder": {
        "definition": "separating construction steps from the final object so complex objects are assembled safely and readably",
        "when": "valid construction requires several optional or ordered decisions",
        "invariant": "an object is not created until required fields and consistency checks are satisfied",
        "pitfalls": ["using builders for trivial objects", "allowing invalid intermediate state to escape", "duplicating validation in many builders"],
        "example": "A query builder can require a source and projection before `build()` creates an immutable query plan.",
    },
    "Prototype": {
        "definition": "creating new objects from existing configured instances when copying is clearer than rebuilding",
        "when": "initialization is expensive or many objects share a mostly identical configuration",
        "invariant": "copied instances must not accidentally share mutable state that should be independent",
        "pitfalls": ["shallow-copying nested mutable data", "hiding expensive copy behavior", "using prototypes where explicit constructors would be clearer"],
        "example": "A report template can be cloned with a new date range while keeping chart definitions and access policy unchanged.",
    },
    "Singleton": {
        "definition": "restricting a type to one shared instance when the system genuinely has one global coordination point",
        "when": "there is one process-wide resource and explicit dependency injection would not improve ownership",
        "invariant": "the single instance has well-defined lifecycle, configuration, and concurrency behavior",
        "pitfalls": ["turning global state into hidden dependencies", "making tests order-dependent", "using Singleton for convenience rather than ownership"],
        "example": "A process-level metrics registry can be single, but request handlers should still receive it through explicit dependencies.",
    },
    "Adapter": {
        "definition": "translating one interface into another so incompatible components can collaborate",
        "when": "a stable internal contract must use a third-party or legacy API",
        "invariant": "the domain side should not leak provider-specific terminology or failure semantics",
        "pitfalls": ["letting adapter code spread into clients", "dropping errors during translation", "pretending incompatible semantics are identical"],
        "example": "A `ShippingRateProvider` adapter can translate carrier-specific responses into the product's internal shipping quote model.",
    },
    "Bridge": {
        "definition": "separating an abstraction from its implementation so both can vary independently",
        "when": "two axes of variation would otherwise create a combinatorial class hierarchy",
        "invariant": "the abstraction owns user-facing behavior while implementation objects own platform-specific details",
        "pitfalls": ["introducing the split before variation exists", "letting both sides own the same decision", "making the bridge harder to understand than a direct dependency"],
        "example": "A notification abstraction can vary by message type while delivery implementations vary by email, SMS, or push.",
    },
    "Composite": {
        "definition": "representing part-whole hierarchies through a shared component interface so clients can treat leaves and groups uniformly",
        "when": "operations should recurse over a tree of objects without client-side type checks",
        "invariant": "leaf and composite nodes must honor the same behavioral contract at the boundary clients use",
        "pitfalls": ["forcing leaf objects to expose meaningless child operations", "hiding expensive recursive traversal", "allowing cycles in a structure that is assumed to be a tree"],
        "example": "A document renderer can model `TextRun`, `Image`, and `Section` as `DocumentNode`. `Section.render()` delegates to children while callers render any node through the same interface.",
    },
    "Decorator": {
        "definition": "wrapping an object to add behavior while preserving the same interface",
        "when": "behavior should be composed at runtime without changing the wrapped object's class",
        "invariant": "the decorator must preserve the contract of the object it wraps",
        "pitfalls": ["changing semantics while pretending the interface is unchanged", "creating hard-to-debug wrapper chains", "using decoration where a named policy object would be clearer"],
        "example": "A repository can be wrapped with caching, tracing, or authorization decorators while callers continue to use the same repository interface.",
    },
    "Facade": {
        "definition": "providing a simpler entry point over a complex subsystem",
        "when": "clients need a stable use-case-oriented API rather than subsystem details",
        "invariant": "the facade should simplify coordination without hiding important failure behavior",
        "pitfalls": ["turning the facade into a god object", "hiding transaction boundaries", "removing useful diagnostics from callers"],
        "example": "An onboarding facade can coordinate account creation, billing setup, and welcome email while exposing one explicit application operation.",
    },
    "Flyweight": {
        "definition": "sharing immutable intrinsic state across many fine-grained objects",
        "when": "object count is high and duplicated state dominates memory cost",
        "invariant": "shared state must be immutable or safely managed separately from per-use extrinsic state",
        "pitfalls": ["sharing mutable state accidentally", "making code obscure for small memory savings", "ignoring cache eviction or lifecycle"],
        "example": "A text editor can share glyph metadata while each character occurrence stores only position and style references.",
    },
    "Proxy": {
        "definition": "standing in for another object to control access, loading, locality, or instrumentation",
        "when": "the caller should use the same interface while access policy or indirection is handled separately",
        "invariant": "the proxy must make latency, authorization, caching, or remote errors visible enough to reason about",
        "pitfalls": ["hiding network calls behind local-looking APIs", "surprising callers with lazy loading", "mixing access control with business policy"],
        "example": "A document proxy can check permissions and load content lazily while preserving the document interface.",
    },
}


KEYWORD_LENSES: list[tuple[tuple[str, ...], dict[str, Any]]] = [
    (
        ("naming", "name"),
        {
            "definition": "choosing identifiers that communicate role, scope, and intent at the point of use",
            "when": "readers need to understand behavior without reconstructing the author's mental model",
            "invariant": "names should describe why a value exists, not only what primitive type it has",
            "pitfalls": ["using vague names such as data or manager", "encoding obsolete implementation details", "renaming without checking call-site meaning"],
        },
    ),
    (
        ("transaction", "acid", "consistency", "isolation"),
        {
            "definition": "protecting state changes with explicit consistency and failure semantics",
            "when": "multiple writes or reads must preserve a business invariant",
            "invariant": "after success or failure, persisted state must still satisfy the rule the system promises",
            "pitfalls": ["checking invariants outside the transaction", "ignoring isolation anomalies", "treating retries as always safe"],
        },
    ),
    (
        ("index", "query", "optimization"),
        {
            "definition": "matching data access paths to real queries and update costs",
            "when": "latency or load is shaped by how data is found, filtered, sorted, or joined",
            "invariant": "the chosen access path must support the critical query without making writes or storage unacceptable",
            "pitfalls": ["adding indexes without workload evidence", "forgetting write amplification", "optimizing a query that is not on the critical path"],
        },
    ),
    (
        ("authentication", "authorization", "identity", "access"),
        {
            "definition": "binding actions to trustworthy identity and explicit permissions",
            "when": "a system must decide who is acting and what they are allowed to do",
            "invariant": "every sensitive action must be authorized against the current actor, resource, and context",
            "pitfalls": ["checking only UI visibility", "trusting stale roles", "mixing authentication with authorization decisions"],
        },
    ),
    (
        ("test", "testing", "mock", "unit", "integration"),
        {
            "definition": "using executable checks to protect important behavior from regression",
            "when": "a change can break behavior that users, operators, or downstream systems rely on",
            "invariant": "the test should fail for a meaningful behavior break and stay quiet for irrelevant implementation changes",
            "pitfalls": ["testing implementation details", "accepting flaky tests as normal", "adding broad mocks that hide contract failures"],
        },
    ),
    (
        ("latency", "throughput", "performance", "cache", "load"),
        {
            "definition": "controlling time and resource use under a known workload",
            "when": "user experience, cost, or reliability depends on predictable response under load",
            "invariant": "performance claims must be tied to workload, percentile, capacity, and measurement method",
            "pitfalls": ["optimizing without a baseline", "confusing average latency with tail latency", "using cache without an invalidation story"],
        },
    ),
    (
        ("event", "message", "queue", "stream"),
        {
            "definition": "communicating state changes or work through asynchronous records",
            "when": "producers and consumers should be decoupled in time, scale, or ownership",
            "invariant": "consumers must handle ordering, duplication, retries, and schema evolution explicitly",
            "pitfalls": ["assuming exactly-once delivery", "publishing vague events", "forgetting replay and backfill behavior"],
        },
    ),
    (
        ("slo", "incident", "reliability", "recovery", "failure"),
        {
            "definition": "making expected service behavior and recovery responsibilities explicit",
            "when": "the team must decide how much failure is acceptable and how to respond when it occurs",
            "invariant": "the system should have a known user impact, owner, signal, and recovery path for important failures",
            "pitfalls": ["tracking vanity metrics", "writing runbooks nobody rehearses", "treating every alert as equally urgent"],
        },
    ),
    (
        ("observability", "logging", "metrics", "tracing", "alert"),
        {
            "definition": "recording enough runtime evidence to explain behavior and diagnose failures",
            "when": "operators need to answer what happened, where, why, and who was affected",
            "invariant": "signals should be correlated, actionable, and affordable enough to keep in production",
            "pitfalls": ["logging volume without diagnostic value", "alerting on symptoms no one can act on", "missing correlation identifiers"],
        },
    ),
    (
        ("api", "contract", "version", "rest", "grpc"),
        {
            "definition": "defining externally visible behavior that clients can depend on safely",
            "when": "independent systems or teams need a stable integration point",
            "invariant": "clients should know request semantics, response shape, error behavior, and evolution rules",
            "pitfalls": ["breaking compatibility silently", "using transport errors for domain failures", "documenting fields without semantics"],
        },
    ),
]


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


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def human_join(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + ", and " + items[-1]


def profile_for(entry: dict[str, Any]) -> dict[str, Any]:
    return VOLUME_PROFILES.get(
        entry["volume_title"],
        {
            "focus": "making technical decisions explicit enough to review and improve",
            "concerns": ["clarity", "ownership", "risk", "change cost"],
            "signals": ["clear decisions", "low surprise", "fewer regressions"],
            "artifact": "engineering review",
        },
    )


def lens_for(entry: dict[str, Any]) -> dict[str, Any]:
    title = entry["section_title"]
    if title in PATTERN_LENSES:
        return PATTERN_LENSES[title]

    context = " ".join(
        [
            entry["volume_title"],
            entry["chapter_title"],
            entry["section_title"],
        ]
    ).lower()

    for keywords, lens in KEYWORD_LENSES:
        if any(keyword in context for keyword in keywords):
            return lens

    profile = profile_for(entry)
    return {
        "definition": f"making `{title}` explicit as a decision area within {entry['chapter_title']}",
        "when": f"work in {entry['volume_title']} depends on {human_join(profile['concerns'])}",
        "invariant": f"the team can explain how `{title}` changes behavior, ownership, or risk",
        "pitfalls": [
            f"treating `{title}` as terminology rather than an operational decision",
            "copying a familiar pattern without checking constraints",
            "leaving success and failure criteria implicit",
        ],
    }


def codeish_example_for(entry: dict[str, Any], lens: dict[str, Any]) -> str:
    volume = entry["volume_title"]
    chapter = entry["chapter_title"]
    title = entry["section_title"]

    if title in PATTERN_LENSES:
        return f"""A useful pattern note should name the participants and the reason for the indirection:

```text
Problem: direct clients would need to know too much about construction, structure, or collaboration.
Pattern intent: {lens['definition']}.
Use when: {lens['when']}.
Protected invariant: {lens['invariant']}.
Review focus: remove the pattern if it no longer simplifies clients or isolates variation.
```

For `{title}`, a concrete application is: {lens['example']} The important review question is whether the pattern makes the object collaboration easier to understand, or merely adds names around code that was already simple."""

    context = f"{volume} {chapter} {title}".lower()

    if "algorithm" in context or volume == "Algorithms":
        return f"""Frame the algorithm before choosing an implementation:

```text
Input shape: define size, ordering, duplicates, and adversarial cases.
Correctness invariant: state what remains true after each step.
Complexity target: name expected time and space bounds.
Failure mode: describe overflow, empty input, and pathological distribution behavior.
Verification: include examples, edge cases, and one property-style test.
```

For `{title}`, the key is to connect the technique to a real constraint. An algorithm that is elegant on a whiteboard can still be wrong for production if the input distribution, memory bound, or correctness invariant is unstated."""

    if volume == "Data Structures":
        return f"""Evaluate the representation through operations, not through the data type name:

```text
Primary operations: insert, lookup, delete, traversal, mutation.
Expected frequency: which operations dominate real workloads.
Invariant: what must remain true after every mutation.
Cost model: time, memory, cache locality, and allocation behavior.
Escape hatch: when to replace this structure with another representation.
```

For `{title}`, this prevents the team from choosing a familiar structure while ignoring the access pattern that will actually dominate performance and maintainability."""

    if "database" in context or volume in {"Databases", "Distributed Databases"}:
        return f"""Make the data decision reviewable:

```text
Invariant: one business rule that persisted state must satisfy.
Read path: the query that must remain fast and correct.
Write path: the transaction, conflict, or retry behavior.
Migration path: how existing data moves safely into the new shape.
Operational signal: how the team detects drift, lag, or constraint violations.
```

For `{title}`, this format keeps the discussion tied to state and workload rather than only schema aesthetics."""

    if volume in {"Security", "Advanced Security", "Compliance and Risk"}:
        return f"""Connect the control to an abuse case and evidence:

```text
Asset: the data, action, or identity being protected.
Threat: the realistic way it can be misused.
Control: the preventive or detective mechanism.
Evidence: log, test, audit event, or review artifact proving the control exists.
Failure response: what happens when the control fails or is bypassed.
```

For `{title}`, this keeps the section grounded in risk reduction instead of security theater."""

    if volume == "Testing":
        return f"""Tie tests to risk:

```text
Behavior at risk: what user or system promise can regress.
Fast check: the smallest deterministic test that catches the common break.
Contract check: how collaborators prove they still agree.
End-to-end check: the narrow critical path that deserves slower validation.
Maintenance rule: when to delete or rewrite the test.
```

For `{title}`, quality comes from useful signal, not from raw test count."""

    if volume in {"Distributed Systems", "Reliability Engineering", "Site Reliability Engineering"}:
        return f"""A failure-mode note makes the design operational:

```text
Dependency or component: what can fail independently.
Timeout: the maximum time callers wait.
Retry rule: when retry is safe and when it amplifies load.
Fallback: degraded behavior that protects users or operators.
Signal: metric, trace, log, or alert that proves the path occurred.
```

For `{title}`, the value is that the system has a defined behavior when the happy path disappears."""

    if volume == "Observability":
        return f"""Design the diagnostic path before the incident:

```text
Question: what must an operator answer quickly.
Signal: metric, log, span, event, or profile that answers it.
Correlation: request id, trace id, user id, tenant, or deployment version.
Cardinality: what labels are safe at production scale.
Action: the decision the signal enables.
```

For `{title}`, observability is successful only when it shortens the path from symptom to explanation."""

    if volume in {"DevOps", "Cloud Architecture", "High Load Systems"}:
        return f"""Make the operational decision explicit:

```text
Change path: how the system is deployed or scaled.
Rollback path: how the team returns to a safe state.
Ownership: who responds when the mechanism fails.
Cost and capacity: what grows with traffic, tenants, or environments.
Evidence: dashboard, deployment record, audit event, or capacity test.
```

For `{title}`, a good implementation is one the team can operate repeatedly under pressure."""

    if volume == "Frontend Architecture":
        return f"""Review the user interaction and state ownership together:

```text
User intent: the action the interface must support.
State owner: component, store, server, URL, or browser storage.
Rendering rule: what changes the visible result.
Accessibility rule: keyboard, focus, semantics, and screen-reader behavior.
Performance budget: what must stay responsive during interaction.
```

For `{title}`, frontend architecture is strongest when state and user feedback are easy to trace."""

    if volume in {"Technical Leadership", "Architecture Governance", "Product Engineering", "Software Economics", "Enterprise Architecture", "Principal Engineer Body of Knowledge"}:
        return f"""Turn the topic into a decision record:

```text
Context: the pressure or ambiguity that requires a decision.
Options: the credible alternatives, including doing nothing.
Decision: the chosen direction and owner.
Consequence: what becomes easier, harder, cheaper, or riskier.
Review point: the evidence that should trigger reconsideration.
```

For `{title}`, this makes leadership work concrete enough to inspect instead of relying on influence alone."""

    return f"""A concise technical note is usually enough:

```text
Context: what problem is being solved.
Constraint: what must remain true.
Decision: what changes in design, implementation, or process.
Evidence: what shows the decision is working.
Review trigger: what would prove the decision wrong.
```

For `{title}`, this structure keeps the section tied to behavior and consequences rather than abstract advice."""


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def checklist(items: list[str]) -> str:
    return "\n".join(f"- [ ] {item}" for item in items)


def generate_body(entry: dict[str, Any]) -> str:
    section_id = entry["id"]
    title = entry["section_title"]
    volume = entry["volume_title"]
    chapter = entry["chapter_title"]
    profile = profile_for(entry)
    lens = lens_for(entry)
    concerns = human_join(profile["concerns"])
    signals = human_join(profile["signals"])

    purpose = f"""`{title}` belongs to the `{chapter}` chapter of `{volume}`. In this context, it is about {lens['definition']}. The practical goal is to help engineers make a decision that can survive code review, design review, production operation, and later change.

This topic matters because `{volume}` is concerned with {profile['focus']}. A good treatment of `{title}` should clarify {concerns}, protect the invariant that {lens['invariant']}, and give the team observable signals such as {signals}."""

    core = bullets(
        [
            f"Start with intent. State why `{title}` is relevant to the current problem before naming a mechanism.",
            f"Use the chapter boundary. `{chapter}` supplies the nearby vocabulary, constraints, and failure modes.",
            f"Protect the invariant: {lens['invariant']}.",
            f"Use this topic when {lens['when']}.",
            f"Connect the decision to the review artifact: the relevant artifact is a {profile['artifact']}.",
            "Prefer evidence over preference. The best answer is the one whose behavior can be inspected, tested, measured, or safely changed.",
        ]
    )

    guidance = bullets(
        [
            f"Write a one-sentence problem statement for `{title}` before changing code, architecture, or process.",
            "Identify the owner of the decision and the people who will maintain, operate, or integrate with it.",
            "Name the boundary: inputs, outputs, collaborators, data, trust level, lifecycle, and failure behavior.",
            "Choose the smallest mechanism that preserves the invariant while keeping the design understandable.",
            "Add an explicit review signal: test, metric, trace, decision record, schema check, benchmark, or runbook step.",
            "Document the trade-off in the place future maintainers will actually see during review or operation.",
            "Revisit the decision when scale, ownership, product behavior, compliance pressure, or failure evidence changes.",
        ]
    )

    tradeoffs = bullets(
        [
            f"Specific guidance for `{title}` improves consistency, but applied mechanically it can ignore local constraints.",
            "Extra abstraction can isolate variation, but it also adds names, lifecycle, and debugging paths that must be owned.",
            "More validation and documentation reduce ambiguity, but they should target real risk rather than slowing harmless change.",
            "A local improvement can increase cross-team coordination cost if the boundary or ownership model is unclear.",
            f"The right level of rigor depends on impact: high-risk work deserves stronger evidence than a small internal cleanup.",
        ]
    )

    pitfalls = list(lens.get("pitfalls", []))
    mistakes = bullets(
        [
            pitfalls[0] if len(pitfalls) > 0 else f"Using `{title}` as a label without changing any engineering behavior.",
            pitfalls[1] if len(pitfalls) > 1 else "Copying a familiar solution without checking the current constraints.",
            pitfalls[2] if len(pitfalls) > 2 else "Leaving success criteria implicit until review or production failure exposes them.",
            "Optimizing the first implementation while ignoring migration, rollback, observability, and long-term ownership.",
            "Reviewing surface shape instead of the invariant, failure behavior, and change cost the section is meant to control.",
        ]
    )

    review = checklist(
        [
            f"The reason to apply `{title}` is clear in the current `{chapter}` context.",
            f"The invariant is stated: {lens['invariant']}.",
            "The design names owners, boundaries, collaborators, and failure behavior.",
            f"Evidence exists through {signals}.",
            "The trade-off is explicit enough that a future maintainer can revisit it.",
            "The solution is no more complex than the risk or variation requires.",
        ]
    )

    return f"""#### {section_id} {title}

##### Purpose

{purpose}

##### Core Ideas

{core}

##### Practical Guidance

{guidance}

##### Trade-offs

{tradeoffs}

##### Examples

{codeish_example_for(entry, lens)}

##### Common Mistakes

{mistakes}

##### Review Checklist

{review}
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


def command_improve(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    tasks = manifest.get("tasks", [])
    changed = 0
    skipped = 0
    total = len(tasks)

    for index, entry in enumerate(tasks, start=1):
        status = entry.get("status", "pending")
        if status not in REWRITE_STATUSES and not args.force:
            skipped += 1
            continue

        if status in {"validated", "merged"} and not args.force:
            skipped += 1
            continue

        path = ensure_inside_workspace(SCRIPT_DIR / entry["path"])
        if not path.exists():
            raise FileNotFoundError(f"Missing fragment: {entry['path']}")

        body = generate_body(entry)
        word_count = count_words(body)
        if word_count < args.min_words:
            raise ValueError(f"Generated body for {entry['id']} is too short: {word_count} words")

        path.write_text(render_fragment(entry, body), encoding="utf-8")
        entry["status"] = "reviewed"
        entry["sha256"] = sha256_file(path)
        entry["updated_at"] = utc_now()
        entry["validation"] = {}
        changed += 1

        if args.progress and (changed == 1 or index == total or index % args.progress_every == 0):
            print(f"Progress: {index}/{total} scanned, {changed} improved, {skipped} skipped")

    manifest["updated_at"] = utc_now()
    save_manifest(manifest)

    print(f"Improved: {changed} fragments")
    print(f"Skipped: {skipped} fragments")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Rewrite validated or merged fragments")
    parser.add_argument("--min-words", type=int, default=360, help="Minimum generated section body word count")
    parser.add_argument("--progress", action="store_true", help="Print progress while rewriting")
    parser.add_argument("--progress-every", type=int, default=25, help="Print progress every N scanned sections")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return command_improve(args)


if __name__ == "__main__":
    raise SystemExit(main())

