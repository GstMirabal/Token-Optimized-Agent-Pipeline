"""Deterministic documentation freshness and integrity checks.

Implements rules/documentation_standard.md §2.1 (C4 Level 3 density),
§4 (bold-key metadata parsing, freshness-gate threshold, and the five
documentation-integrity sub-checks). Invoked via `make docs-freshness-check`
from close_workflow.md Phase 1 — never re-derives what a script can
already compute, per the same discipline the rest of the framework holds
itself to.

Exit codes: 0 always in WARN-only rollout; the caller (close_workflow.md)
decides whether a non-empty BLOCK list actually halts the session, based
on which cycle this host is on (see §4.2).
"""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

GRAPH_JSON = Path("graphify-out/graph.json")
DENYLIST_LANGUAGES = {"python", "js", "go"}
METADATA_FIELD_RE = re.compile(r"^\*\*([^*]+)\*\*:\s*(.+)$", re.MULTILINE)
C4_OVERRIDE_RE = re.compile(r"C4 Level Override.*?justification:\s*(ADR-\d{4})")
SUPERSEDED_RE = re.compile(r"Superseded by\s+(ADR-\d{4})")
ADR_ID_RE = re.compile(r"^ADR-(\d{4})-")
ADR_STATUS_SUPERSEDED_RE = re.compile(r"^\s*Status:\s*Superseded", re.MULTILINE)

ADR_DIR = Path("docs/decisions")
BLUEPRINT_GLOB = "docs/**/*_BLUEPRINT.md"
SPRINTS_DIR = Path("docs/sprints")
DENYLIST_DIR = Path(".agents/scripts/denylists")
GRAPH_STATS_WINDOW = 10
BOOTSTRAP_MIN_DELTAS = 5


@dataclass
class Finding:
    """One check outcome.

    Attributes:
        level: "WARN" or "BLOCK".
        message: Human-readable description, includes the offending path.
    """
    level: str
    message: str


@dataclass
class FreshnessReport:
    """Aggregated outcome of a full run."""
    findings: list[Finding] = field(default_factory=list)

    def warn(self, message: str) -> None:
        self.findings.append(Finding(level="WARN", message=message))

    def block(self, message: str) -> None:
        self.findings.append(Finding(level="BLOCK", message=message))

    @property
    def has_block(self) -> bool:
        return any(f.level == "BLOCK" for f in self.findings)

    def print_summary(self) -> None:
        if not self.findings:
            print("[OK] docs-freshness-check: no findings")
            return
        for f in self.findings:
            print(f"[{f.level}] {f.message}")


def metadata_region(text: str) -> str:
    """Return the slice between the H1 and the first '---' rule.

    Every real template places its bold-key metadata block there —
    anchoring the parse prevents a field name that merely appears in
    body prose from being mistaken for metadata.
    """
    marker = text.find("\n---")
    return text[:marker] if marker != -1 else text


def parse_metadata_fields(text: str) -> dict[str, str]:
    """Extract '**Field**: value' pairs from a document's metadata block."""
    region = metadata_region(text)
    return {name.strip(): value.strip() for name, value in METADATA_FIELD_RE.findall(region)}


def find_duplicate_metadata_fields(text: str) -> list[str]:
    """Return field names repeated inside the metadata block."""
    region = metadata_region(text)
    names = [name.strip() for name, _ in METADATA_FIELD_RE.findall(region)]
    seen: set[str] = set()
    duplicates: list[str] = []
    for name in names:
        if name in seen and name not in duplicates:
            duplicates.append(name)
        seen.add(name)
    return duplicates


def check_metadata_duplicates(report: FreshnessReport, blueprint_paths: list[Path]) -> None:
    """§4.1: flag repeated metadata fields inside any Blueprint's block."""
    for path in blueprint_paths:
        duplicates = find_duplicate_metadata_fields(path.read_text(encoding="utf-8"))
        for field_name in duplicates:
            report.warn(f"{path}: metadata field '{field_name}' repeated in its block")


def adr_files(repo_root: Path) -> list[Path]:
    """All real ADR files on disk, empty list if the directory doesn't exist yet."""
    adr_dir = repo_root / ADR_DIR
    if not adr_dir.is_dir():
        return []
    return sorted(adr_dir.glob("ADR-*.md"))


def adr_ids_in_dir(repo_root: Path) -> dict[str, Path]:
    """Map ADR numeric ID -> its file path, for existence/duplicate checks."""
    ids: dict[str, Path] = {}
    for path in adr_files(repo_root):
        match = ADR_ID_RE.match(path.name)
        if match:
            ids.setdefault(match.group(1), path)
    return ids


def check_duplicate_adr_ids(report: FreshnessReport, repo_root: Path) -> None:
    """§4.4(c): no two ADR files may share the same numeric ID."""
    seen: dict[str, list[Path]] = {}
    for path in adr_files(repo_root):
        match = ADR_ID_RE.match(path.name)
        if not match:
            continue
        seen.setdefault(match.group(1), []).append(path)
    for adr_id, paths in seen.items():
        if len(paths) > 1:
            names = ", ".join(str(p) for p in paths)
            report.warn(f"Duplicate ADR-{adr_id} across: {names}")


def is_adr_superseded(path: Path) -> bool:
    """True if the ADR's own Status line marks it Superseded."""
    return bool(ADR_STATUS_SUPERSEDED_RE.search(path.read_text(encoding="utf-8")))


def check_c4_override_pointers(report: FreshnessReport, blueprint_paths: list[Path], repo_root: Path) -> None:
    """§4.4(a): every C4 Level Override justification resolves to a real, live ADR."""
    known_ids = adr_ids_in_dir(repo_root)
    for path in blueprint_paths:
        text = path.read_text(encoding="utf-8")
        for adr_ref in C4_OVERRIDE_RE.findall(text):
            adr_id = adr_ref.removeprefix("ADR-")
            if adr_id not in known_ids:
                report.warn(f"{path}: C4 Level Override cites {adr_ref}, which does not exist")
            elif is_adr_superseded(known_ids[adr_id]):
                report.warn(f"{path}: C4 Level Override cites {adr_ref}, which is superseded")


def check_superseded_chains(report: FreshnessReport, repo_root: Path) -> None:
    """§4.4(b): every 'Superseded by ADR-XXXX' reference resolves to a real ADR."""
    known_ids = adr_ids_in_dir(repo_root)
    for path in adr_files(repo_root):
        text = path.read_text(encoding="utf-8")
        for adr_ref in SUPERSEDED_RE.findall(text):
            adr_id = adr_ref.removeprefix("ADR-")
            if adr_id not in known_ids:
                report.warn(f"{path}: 'Superseded by {adr_ref}' does not resolve to a real ADR")


def load_active_state(repo_root: Path) -> dict:
    """Read the host's docs/active_state.json, empty dict if absent."""
    state_path = repo_root / "docs" / "active_state.json"
    if not state_path.is_file():
        return {}
    return json.loads(state_path.read_text(encoding="utf-8"))


def check_code_containers_roots(report: FreshnessReport, repo_root: Path, state: dict) -> None:
    """§4.4(d): every declared code_containers root must exist on disk."""
    for entry in state.get("code_containers", []):
        root = entry.get("root", "")
        if root and not (repo_root / root).is_dir():
            report.warn(f"code_containers root '{root}' (stack={entry.get('stack')}) does not exist")


def load_denylist(denylist_dir: Path, language: str) -> set[str]:
    """Load one language's primitive denylist; empty set if not shipped/declared.

    Per §2.1.3: a stack whose language has no denylist stays advisory rather
    than silently running the filter empty (callers check emptiness).
    """
    path = denylist_dir / f"{language}.txt"
    if not path.is_file():
        return set()
    lines = path.read_text(encoding="utf-8").splitlines()
    return {line.strip() for line in lines if line.strip() and not line.startswith("#")}


def container_for_source(source_file: str, containers: list[dict]) -> tuple[str, str] | None:
    """Map a node's source_file to its (stack, container) tuple, per §2.1.2.

    A file directly under a declared root with no subdirectory of its own
    (e.g. 'apps/__init__.py') is deliberately excluded — it would otherwise
    register as a phantom zero-density container.
    """
    for entry in containers:
        root = entry.get("root", "")
        if not root or not source_file.startswith(root):
            continue
        remainder = source_file[len(root):].split("/", 1)
        if len(remainder) < 2:
            continue
        return entry.get("stack", ""), remainder[0]
    return None


def load_graph(repo_root: Path) -> dict:
    """Load graphify's output graph, empty structure if absent."""
    graph_path = repo_root / GRAPH_JSON
    if not graph_path.is_file():
        return {"nodes": [], "links": []}
    return json.loads(graph_path.read_text(encoding="utf-8"))


def compute_degrees(graph: dict) -> dict[str, int]:
    """Node id -> degree, counting both endpoints of every link (§2.1.4)."""
    degrees: dict[str, int] = {}
    for link in graph.get("links", []):
        degrees[link["source"]] = degrees.get(link["source"], 0) + 1
        degrees[link["target"]] = degrees.get(link["target"], 0) + 1
    return degrees


def compute_container_density(repo_root: Path, denylist_dir: Path, state: dict) -> dict[tuple[str, str], float]:
    """Average degree per (stack, container), primitives excluded — §2.1.3-4.

    Returns an empty dict (advisory mode) if code_containers isn't declared.
    """
    containers = state.get("code_containers", [])
    if not containers:
        return {}
    graph = load_graph(repo_root)
    degrees = compute_degrees(graph)
    denylists = {lang: load_denylist(denylist_dir, lang) for lang in DENYLIST_LANGUAGES}
    totals: dict[tuple[str, str], list[int]] = {}
    for node in graph.get("nodes", []):
        source_file = node.get("source_file", "")
        label = node.get("label", "")
        if any(label in denylist for denylist in denylists.values()):
            continue
        key = container_for_source(source_file, containers)
        if key is None:
            continue
        totals.setdefault(key, []).append(degrees.get(node["id"], 0))
    return {key: sum(values) / len(values) for key, values in totals.items() if values}


def percentile(sorted_values: list[float], pct: float) -> float:
    """Nearest-rank percentile over an already-sorted list."""
    if not sorted_values:
        return 0.0
    index = min(len(sorted_values) - 1, int(round((pct / 100) * (len(sorted_values) - 1))))
    return sorted_values[index]


def level3_qualifying_containers(densities: dict[tuple[str, str], float]) -> set[tuple[str, str]]:
    """Containers at/above the 75th density percentile, computed per stack (§2.1.5-6).

    Fewer than 5 containers in a stack degenerates the percentile — that
    stack's single highest-density container always qualifies instead.
    """
    by_stack: dict[str, list[tuple[str, float]]] = {}
    for (stack, container), density in densities.items():
        by_stack.setdefault(stack, []).append((container, density))

    qualifying: set[tuple[str, str]] = set()
    for stack, entries in by_stack.items():
        entries.sort(key=lambda pair: pair[1])
        values = [density for _, density in entries]
        if len(entries) < 5:
            best_container = max(entries, key=lambda pair: pair[1])[0]
            qualifying.add((stack, best_container))
            continue
        cutoff = percentile(values, 75)
        qualifying.update((stack, container) for container, density in entries if density >= cutoff)
    return qualifying


def graph_stats_snapshots(repo_root: Path) -> list[tuple[int, dict]]:
    """Load (sprint_id, stats) pairs from docs/sprints/*/graph_stats.json, sorted by sprint."""
    sprints_dir = repo_root / SPRINTS_DIR
    if not sprints_dir.is_dir():
        return []
    snapshots: list[tuple[int, dict]] = []
    for sprint_dir in sorted(sprints_dir.iterdir()):
        stats_file = sprint_dir / "graph_stats.json"
        if not stats_file.is_file():
            continue
        digits = "".join(ch for ch in sprint_dir.name.split("-")[0] if ch.isdigit())
        if digits:
            snapshots.append((int(digits), json.loads(stats_file.read_text(encoding="utf-8"))))
    return sorted(snapshots, key=lambda pair: pair[0])


def check_graph_stats_gaps(report: FreshnessReport, repo_root: Path) -> None:
    """§4.4(e): a missing graph_stats.json inside an otherwise-populated
    sprint range is flagged — it may be corruption, not just absence.
    """
    snapshots = graph_stats_snapshots(repo_root)
    if len(snapshots) < 2:
        return
    ids = [sprint_id for sprint_id, _ in snapshots]
    for expected in range(ids[0], ids[-1] + 1):
        if expected not in ids:
            report.warn(f"docs/sprints/{expected:03d}*/graph_stats.json missing inside a populated range")


def node_delta(previous: dict, current: dict) -> int:
    """Absolute change in node/edge count plus any new community, per §4.3."""
    node_change = abs(current.get("nodes", 0) - previous.get("nodes", 0))
    edge_change = abs(current.get("edges", 0) - previous.get("edges", 0))
    community_change = max(0, current.get("communities", 0) - previous.get("communities", 0))
    return node_change + edge_change + (community_change * 100)


def structural_change_status(repo_root: Path, last_audit_sprint: int, current_sprint: int) -> tuple[bool, str]:
    """§4.3: does a structural-change delta exist since last_audit_sprint,
    and has enough history accumulated to allow BLOCK (vs. WARN-only)?

    Returns:
        (delta_exceeds_threshold, mode) where mode is "advisory" (bootstrap
        floor not met) or "enforced".
    """
    snapshots = graph_stats_snapshots(repo_root)
    if not snapshots:
        return False, "advisory"
    recent = [s for sid, s in snapshots if sid < current_sprint][-GRAPH_STATS_WINDOW:]
    if len(recent) < BOOTSTRAP_MIN_DELTAS:
        return False, "advisory"
    deltas = sorted(node_delta(recent[i - 1], recent[i]) for i in range(1, len(recent)))
    threshold = percentile(deltas, 90)
    last_snapshot = next((s for sid, s in snapshots if sid == last_audit_sprint), recent[0])
    current_snapshot = next((s for sid, s in snapshots if sid == current_sprint), recent[-1])
    exceeded = node_delta(last_snapshot, current_snapshot) > threshold
    return exceeded, "enforced"


def collect_blueprint_paths(repo_root: Path) -> list[Path]:
    return sorted(repo_root.glob(BLUEPRINT_GLOB))


def run(repo_root: Path, current_sprint: int, denylist_dir: Path = DENYLIST_DIR) -> FreshnessReport:
    """Run every check and return the aggregated report.

    Args:
        repo_root: host project root (where docs/active_state.json lives).
        current_sprint: the sprint ID being closed.
        denylist_dir: directory holding per-language primitive denylists.

    Returns:
        A FreshnessReport with every finding at its assigned level.
    """
    report = FreshnessReport()
    blueprint_paths = collect_blueprint_paths(repo_root)
    state = load_active_state(repo_root)

    check_metadata_duplicates(report, blueprint_paths)
    check_c4_override_pointers(report, blueprint_paths, repo_root)
    check_superseded_chains(report, repo_root)
    check_duplicate_adr_ids(report, repo_root)
    check_code_containers_roots(report, repo_root, state)
    check_graph_stats_gaps(report, repo_root)

    if state.get("code_containers"):
        densities = compute_container_density(repo_root, denylist_dir, state)
        qualifying = level3_qualifying_containers(densities)
        names = ", ".join(f"{stack}/{container}" for stack, container in sorted(qualifying))
        report.warn(f"C4 Level 3 required for: {names or '(none — advisory, insufficient graph data)'}")
    else:
        report.warn("code_containers not declared — C4 Level 3 stays advisory")

    last_audit_sprint = state.get("current_sprint", {}).get("last_audit_sprint")
    if last_audit_sprint is not None:
        exceeded, mode = structural_change_status(repo_root, int(last_audit_sprint), current_sprint)
        if exceeded and mode == "enforced":
            report.block("Structural change since last audit exceeds the p90 delta threshold — refresh anchors")
        elif exceeded:
            report.warn("Structural change detected, but <5 historical deltas — advisory only until baseline builds")

    return report


if __name__ == "__main__":
    import sys

    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    sprint_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    result = run(root, sprint_arg)
    result.print_summary()
    sys.exit(0)
