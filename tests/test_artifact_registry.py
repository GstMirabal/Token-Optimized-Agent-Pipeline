"""Tests for config/artifact_registry.json and the consumers that read it.

Sprint 023 `C0.2`. The registry is the coordination matrix: a phase is defined
by the artifact it leaves, not by the agent that produces it. Three consumers
read it, so a malformed entry breaks a documentation gate, a close gate and the
generated step map at once — the same criticality bar as the gates themselves.

What these tests protect is not the file's syntax but its two contracts:
every entry declares the fields consumers index into, and every filename is
named literally in a workflow, because `map_workflows.py` matches prose by
literal filename and a deliverable described in words is invisible to it.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import map_workflows  # noqa: E402

REGISTRY_PATH = ROOT / "config" / "artifact_registry.json"
REGISTRY = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
ARTIFACTS = REGISTRY["artifacts"]
DECLARED_FIELDS = {
    "filename", "phase", "role", "scope", "host_path", "nucleus_path", "required",
}
SPRINT_PLACEHOLDER = "docs/sprints/[Sprint_ID]-[Stack]-[Layer]/"


def test_every_entry_declares_every_field_a_consumer_indexes():
    """Consumers index with `entry["filename"]`, not `.get`. A missing key is a
    crash in a gate rather than a warning, so the shape is pinned here."""
    for entry in ARTIFACTS:
        missing = DECLARED_FIELDS - set(entry)
        assert not missing, f"{entry.get('filename')} is missing {sorted(missing)}"


def test_scope_is_one_of_the_two_values_consumers_filter_on():
    """Both gates filter `scope == "sprint"`. A third value would silently drop
    the entry from every check while still appearing in the file."""
    assert {entry["scope"] for entry in ARTIFACTS} <= {"sprint", "repository"}


def test_sprint_scoped_paths_use_the_canonical_sprint_directory():
    """`agents.md §5 mandatory_topology` declares the path once. Four different
    forms of it were in circulation until Phase 019, which is how a file was
    persisted to a path no other document recognised."""
    for entry in ARTIFACTS:
        if entry["scope"] != "sprint":
            continue
        for field in ("host_path", "nucleus_path"):
            assert entry[field].startswith(SPRINT_PLACEHOLDER), (
                f"{entry['filename']}.{field} does not start with the canonical path"
            )


def test_a_path_ends_with_the_filename_it_declares():
    """A registry whose path and filename disagree would make one consumer look
    in the right place while another reports the wrong name."""
    for entry in ARTIFACTS:
        for field in ("host_path", "nucleus_path"):
            if entry[field] is None:
                continue
            assert entry[field].endswith(entry["filename"])


def test_filenames_are_unique():
    """Both gates build a dict keyed by filename: a duplicate would not be
    rejected, it would be silently overwritten by whichever came last."""
    names = [entry["filename"] for entry in ARTIFACTS]
    assert len(names) == len(set(names))


def test_every_artifact_is_named_by_filename_in_some_workflow():
    """The `R2` guarantee, pinned so it cannot silently regress.

    `map_workflows.py` matches workflow prose by literal filename, so a phase
    that describes its deliverable instead of naming it produces an empty
    matrix column. That is not hypothetical: Phase 4.1 said "every step has a
    named assignee" and Phase 4.2 "every step has its tools resolved", and
    `agent_assignment.md` and `skill_assignment.md` were invisible to the map
    while four sprints were producing them.
    """
    prose = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted((ROOT / "workflows").glob("*.md"))
    )
    for entry in ARTIFACTS:
        assert entry["filename"] in prose, (
            f"{entry['filename']} is in the registry but no workflow names it, so its "
            "matrix column is empty by construction"
        )


def test_the_matrix_columns_are_every_registry_entry_in_order():
    """The columns were a fixed table of six state artifacts and zero
    documentary ones. Order is part of the contract: the registry is ordered by
    phase so the generated guide reads in execution order."""
    assert list(map_workflows.load_artifacts()) == [e["filename"] for e in ARTIFACTS]


def test_a_missing_registry_fails_loudly_in_the_map(tmp_path):
    """A matrix built from an unreadable registry would have no columns and
    would read as "no workflow touches any artifact" — a false green. The map
    raises instead, which is the opposite failure direction from the freshness
    gate on purpose: one generates a document, the other reports findings."""
    try:
        map_workflows.load_artifacts(tmp_path / "absent.json")
    except FileNotFoundError:
        return
    raise AssertionError("load_artifacts accepted a missing registry")
