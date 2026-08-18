"""Tests for scripts/docs_freshness_check.py -- the gate that can BLOCK a
sprint close (rules/documentation_standard.md §4). Same criticality class
as on_commit.py's push guard, so it gets the same test-coverage bar
(precedent: test_on_commit.py).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import docs_freshness_check as dfc  # noqa: E402


# --- metadata parsing --------------------------------------------------

def test_parse_metadata_fields_reads_bold_key_block():
    text = "# 🏛️ Blueprint: Foo\n**Last Audit Sprint**: 083\n**Last Audit Date**: 2026-07-21\n\n---\n\n## 1. Purpose\n"
    fields = dfc.parse_metadata_fields(text)
    assert fields == {"Last Audit Sprint": "083", "Last Audit Date": "2026-07-21"}


def test_metadata_region_stops_at_first_rule():
    text = "**A**: 1\n---\n**B**: 2\n"
    assert "B" not in dfc.parse_metadata_fields(text)


def test_duplicate_metadata_field_detected_inside_block():
    text = "**Last Audit Sprint**: 083\n**Last Audit Sprint**: 999\n\n---\nbody\n"
    assert dfc.find_duplicate_metadata_fields(text) == ["Last Audit Sprint"]


def test_bold_text_in_body_prose_is_not_mistaken_for_metadata():
    text = "**Status**: DRAFT\n\n---\n\nSee the **Owns** column below, not metadata.\n**Owns**: also not metadata\n"
    fields = dfc.parse_metadata_fields(text)
    assert fields == {"Status": "DRAFT"}


# --- ADR integrity (§4.4 a/b/c) -----------------------------------------

def _write_adr(repo: Path, adr_id: str, slug: str, status: str = "Accepted", body: str = "") -> Path:
    adr_dir = repo / "docs" / "decisions"
    adr_dir.mkdir(parents=True, exist_ok=True)
    path = adr_dir / f"ADR-{adr_id}-{slug}.md"
    path.write_text(f"# ADR-{adr_id}: {slug}\n\nStatus: {status}\n\n{body}\n", encoding="utf-8")
    return path


def test_c4_override_pointing_to_missing_adr_warns(tmp_path):
    report = dfc.FreshnessReport()
    blueprint = tmp_path / "FOO_BLUEPRINT.md"
    blueprint.write_text("**C4 Level Override**: 3 (justification: ADR-9999)\n", encoding="utf-8")
    dfc.check_c4_override_pointers(report, [blueprint], tmp_path)
    assert any("does not exist" in f.message for f in report.findings)


def test_c4_override_pointing_to_superseded_adr_warns(tmp_path):
    _write_adr(tmp_path, "0007", "old-decision", status="Superseded")
    report = dfc.FreshnessReport()
    blueprint = tmp_path / "FOO_BLUEPRINT.md"
    blueprint.write_text("**C4 Level Override**: 3 (justification: ADR-0007)\n", encoding="utf-8")
    dfc.check_c4_override_pointers(report, [blueprint], tmp_path)
    assert any("superseded" in f.message for f in report.findings)


def test_c4_override_pointing_to_live_adr_is_silent(tmp_path):
    _write_adr(tmp_path, "0007", "current-decision")
    report = dfc.FreshnessReport()
    blueprint = tmp_path / "FOO_BLUEPRINT.md"
    blueprint.write_text("**C4 Level Override**: 3 (justification: ADR-0007)\n", encoding="utf-8")
    dfc.check_c4_override_pointers(report, [blueprint], tmp_path)
    assert report.findings == []


def test_superseded_by_chain_resolves(tmp_path):
    _write_adr(tmp_path, "0001", "first")
    _write_adr(tmp_path, "0002", "second", body="Superseded by ADR-9999")
    report = dfc.FreshnessReport()
    dfc.check_superseded_chains(report, tmp_path)
    assert any("does not resolve" in f.message for f in report.findings)


def test_duplicate_adr_ids_detected(tmp_path):
    _write_adr(tmp_path, "0001", "first-slug")
    _write_adr(tmp_path, "0001", "second-slug")
    report = dfc.FreshnessReport()
    dfc.check_duplicate_adr_ids(report, tmp_path)
    assert any("Duplicate ADR-0001" in f.message for f in report.findings)


def test_no_adr_directory_yet_is_clean(tmp_path):
    report = dfc.FreshnessReport()
    dfc.check_duplicate_adr_ids(report, tmp_path)
    dfc.check_superseded_chains(report, tmp_path)
    assert report.findings == []


# --- code_containers integrity (§4.4 d) ---------------------------------

def test_missing_code_containers_root_warns(tmp_path):
    report = dfc.FreshnessReport()
    state = {"code_containers": [{"stack": "backend", "root": "backend/apps/"}]}
    dfc.check_code_containers_roots(report, tmp_path, state)
    assert any("does not exist" in f.message for f in report.findings)


def test_existing_code_containers_root_is_silent(tmp_path):
    (tmp_path / "backend" / "apps").mkdir(parents=True)
    report = dfc.FreshnessReport()
    state = {"code_containers": [{"stack": "backend", "root": "backend/apps/"}]}
    dfc.check_code_containers_roots(report, tmp_path, state)
    assert report.findings == []


# --- graph_stats.json series gaps (§4.4 e) ------------------------------

def _write_graph_stats(repo: Path, sprint_id: str, nodes: int, edges: int, communities: int = 1) -> None:
    sprint_dir = repo / "docs" / "sprints" / f"{sprint_id}-x"
    sprint_dir.mkdir(parents=True, exist_ok=True)
    (sprint_dir / "graph_stats.json").write_text(
        json.dumps({"nodes": nodes, "edges": edges, "communities": communities}), encoding="utf-8"
    )


def test_gap_in_sprint_range_is_flagged(tmp_path):
    _write_graph_stats(tmp_path, "001", 10, 20)
    _write_graph_stats(tmp_path, "003", 15, 25)  # 002 missing
    report = dfc.FreshnessReport()
    dfc.check_graph_stats_gaps(report, tmp_path)
    assert any("002" in f.message for f in report.findings)


def test_contiguous_sprints_have_no_gap(tmp_path):
    _write_graph_stats(tmp_path, "001", 10, 20)
    _write_graph_stats(tmp_path, "002", 12, 22)
    report = dfc.FreshnessReport()
    dfc.check_graph_stats_gaps(report, tmp_path)
    assert report.findings == []


# --- structural-change threshold (§4.3) ---------------------------------

def test_no_history_is_advisory_only(tmp_path):
    exceeded, mode = dfc.structural_change_status(tmp_path, last_audit_sprint=1, current_sprint=2)
    assert mode == "advisory"
    assert exceeded is False


def test_bootstrap_floor_requires_five_deltas(tmp_path):
    for i in range(1, 4):  # only 3 snapshots -> 2 deltas, below the floor of 5
        _write_graph_stats(tmp_path, f"{i:03d}", nodes=10 * i, edges=20 * i)
    exceeded, mode = dfc.structural_change_status(tmp_path, last_audit_sprint=1, current_sprint=3)
    assert mode == "advisory"


def test_enforced_once_bootstrap_floor_met(tmp_path):
    for i in range(1, 8):  # 7 snapshots -> 6 deltas, past the floor of 5
        _write_graph_stats(tmp_path, f"{i:03d}", nodes=10, edges=20, communities=1)
    _write_graph_stats(tmp_path, "008", nodes=500, edges=900, communities=5)  # big jump
    exceeded, mode = dfc.structural_change_status(tmp_path, last_audit_sprint=1, current_sprint=8)
    assert mode == "enforced"
    assert exceeded is True


# --- C4 density (§2.1) --------------------------------------------------

def _write_graph(repo: Path, nodes: list[dict], links: list[dict]) -> None:
    out_dir = repo / "graphify-out"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "graph.json").write_text(json.dumps({"nodes": nodes, "links": links}), encoding="utf-8")


def test_container_for_source_excludes_root_level_files():
    containers = [{"stack": "backend", "root": "backend/apps/"}]
    assert dfc.container_for_source("backend/apps/__init__.py", containers) is None


def test_container_for_source_maps_first_segment_after_root():
    containers = [{"stack": "backend", "root": "backend/apps/"}]
    assert dfc.container_for_source("backend/apps/datafeed/models.py", containers) == ("backend", "datafeed")


def test_density_excludes_denylisted_primitives(tmp_path):
    _write_graph(
        tmp_path,
        nodes=[
            {"id": "n1", "label": "Asset", "source_file": "backend/apps/datafeed/models.py"},
            {"id": "n2", "label": "Decimal", "source_file": "backend/apps/datafeed/models.py"},
        ],
        links=[{"source": "n1", "target": "n2"}],
    )
    denylist_dir = tmp_path / "denylists"
    denylist_dir.mkdir()
    (denylist_dir / "python.txt").write_text("Decimal\n", encoding="utf-8")
    state = {"code_containers": [{"stack": "backend", "root": "backend/apps/"}]}
    densities = dfc.compute_container_density(tmp_path, denylist_dir, state)
    assert ("backend", "datafeed") in densities
    # Only n1 (Asset) counted; Decimal excluded despite sharing the edge.
    assert densities[("backend", "datafeed")] == 1.0


def test_no_code_containers_yields_empty_densities(tmp_path):
    assert dfc.compute_container_density(tmp_path, tmp_path, {}) == {}


def test_qualifying_containers_computed_per_stack_not_crossed():
    # 6 backend containers, low density; 6 frontend containers, high density.
    # A cross-stack percentile would let frontend dominate; per-stack must not.
    densities = {("backend", f"b{i}"): 1.0 + i for i in range(6)}
    densities.update({("frontend", f"f{i}"): 10.0 + i for i in range(6)})
    qualifying = dfc.level3_qualifying_containers(densities)
    backend_qualifiers = [c for stack, c in qualifying if stack == "backend"]
    frontend_qualifiers = [c for stack, c in qualifying if stack == "frontend"]
    assert backend_qualifiers, "per-stack percentile must select from backend too, not just the denser stack"
    assert frontend_qualifiers


def test_small_stack_below_five_containers_uses_safety_floor():
    densities = {("backend", "a"): 1.0, ("backend", "b"): 5.0}
    qualifying = dfc.level3_qualifying_containers(densities)
    assert qualifying == {("backend", "b")}


# --- end-to-end smoke, empty repo ---------------------------------------

def test_run_on_empty_repo_produces_no_block(tmp_path):
    report = dfc.run(tmp_path, current_sprint=1, denylist_dir=tmp_path / "denylists")
    assert report.has_block is False


# ---------------------------------------------------------------------------
# The gate's own failure modes. Each of these was a live defect: the script
# computed a verdict and discarded it, skipped its only blocking check without
# saying so, and invented containers out of vendored tooling.
# ---------------------------------------------------------------------------


def test_a_block_makes_has_block_true():
    """`has_block` was computed on every run and consulted on none."""
    report = dfc.FreshnessReport()
    report.block("structural change exceeds the threshold")
    assert report.has_block is True


def test_a_warning_alone_does_not_block():
    """A gate that fails on advisory findings is one people switch off."""
    report = dfc.FreshnessReport()
    report.warn("advisory only")
    assert report.has_block is False


def test_tooling_paths_are_not_containers():
    """A repository rooted at '.' matched every hidden directory.

    The framework's own submodule was reported as a container of the host,
    needing a C4 Level 3 the host could not write.
    """
    assert dfc.is_tooling_path(".agents/hooks/on_commit.py") is True
    assert dfc.is_tooling_path(".claude/settings.json") is True
    assert dfc.is_tooling_path("users/views.py") is False
    # Extractors sometimes record an absolute path; it cannot be repo-relative,
    # and taken as a container it produced an entry with an empty name.
    assert dfc.is_tooling_path("/Users/developer/repo/.agents/x.py") is True


def test_hidden_paths_resolve_to_no_container():
    containers = [{"stack": "app", "root": "."}]
    assert dfc.container_for_source(".agents/scripts/x.py", containers) is None
    assert dfc.container_for_source("users/models/user.py", containers) == ("app", "users")


def test_unreadable_sprint_number_is_reported(tmp_path):
    """Skipping quietly disabled the only check capable of blocking.

    A host declaring `current_sprint_id` at the root instead of
    `current_sprint.last_audit_sprint` got no structural check and no word
    about it.
    """
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "active_state.json").write_text(
        json.dumps({"current_sprint_id": 4}), encoding="utf-8"
    )
    report = dfc.run(tmp_path, 4)
    messages = " ".join(f.message for f in report.findings)
    assert "last_audit_sprint" in messages


# --- phase artifacts (a phase that left no artifact did not run) --------
#
# check_phase_artifacts shipped in PR #37 with no direct test of its own.
# Sprint 023 C0 adds IMPLEMENTATION_PLAN.md to the map it reads, so the map
# stops being the only thing standing between a skipped phase and silence.

def _sprint_dir(repo: Path, sprint_id: int, *artifacts: str) -> Path:
    """Build docs/sprints/{NNN}-core-pipeline/ holding only `artifacts`."""
    path = repo / "docs" / "sprints" / f"{sprint_id:03d}-core-pipeline"
    path.mkdir(parents=True, exist_ok=True)
    for name in artifacts:
        (path / name).write_text("body\n", encoding="utf-8")
    return path


def test_a_missing_plan_names_the_phase_that_should_have_written_it(tmp_path):
    """Reporting by phase is the whole point: a filename tells you what is
    absent, a phase tells you which step to go run."""
    _sprint_dir(tmp_path, 23, "SPRINT_LOG.md", "task_scope.md")
    report = dfc.FreshnessReport()
    dfc.check_phase_artifacts(tmp_path, 23, report)
    messages = " ".join(f.message for f in report.findings)
    assert "IMPLEMENTATION_PLAN.md" in messages
    assert "Phase 1" in messages


def test_a_sprint_with_every_artifact_is_silent(tmp_path):
    _sprint_dir(tmp_path, 23, *dfc.load_phase_artifacts())
    report = dfc.FreshnessReport()
    dfc.check_phase_artifacts(tmp_path, 23, report)
    assert report.findings == []


def test_each_missing_artifact_is_reported_separately(tmp_path):
    """Skipped phases are separate problems with separate remedies, not one.

    The count is read from the registry rather than pinned to a literal: the
    literal `3` here was the same hand-maintained duplicate of the artifact list
    that `C0.2` removed from the script itself.
    """
    _sprint_dir(tmp_path, 23)
    report = dfc.FreshnessReport()
    dfc.check_phase_artifacts(tmp_path, 23, report)
    assert len(report.findings) == len(dfc.load_phase_artifacts())


def test_the_report_reads_in_phase_order(tmp_path):
    """The dict order is a contract, not an accident: a sprint that skipped
    several steps should be read in the order they should have run."""
    _sprint_dir(tmp_path, 23)
    report = dfc.FreshnessReport()
    dfc.check_phase_artifacts(tmp_path, 23, report)
    phases = [f.message.split(" — ")[1].split(" (")[0] for f in report.findings]
    assert phases == ["Phase 1", "Phase 3", "Phase 4.1", "Phase 4.2", "Phase 4.3"]


def test_a_sprint_with_no_directory_is_not_accused_of_a_missing_plan(tmp_path):
    """The cause is a different one — Phase 3 never instantiated the
    hierarchy — and naming the plan here would send the reader to the wrong
    phase."""
    (tmp_path / "docs" / "sprints").mkdir(parents=True)
    report = dfc.FreshnessReport()
    dfc.check_phase_artifacts(tmp_path, 23, report)
    messages = " ".join(f.message for f in report.findings)
    assert "Phase 3 instantiates" in messages
    assert "IMPLEMENTATION_PLAN.md" not in messages


def test_the_demanded_list_comes_from_the_registry(tmp_path):
    """`C0.2`: the artifact list is the registry's, not this script's.

    The script held its own copy of three filenames. Two consumers and a
    workflow held three more copies of overlapping lists, which is how
    `agent_assignment.md` and `skill_assignment.md` were produced by four
    sprints while no gate could see them.
    """
    registry = json.loads(
        (dfc.ARTIFACT_REGISTRY).read_text(encoding="utf-8")
    )
    expected = [
        entry["filename"]
        for entry in registry["artifacts"]
        if entry["scope"] == "sprint" and entry["required"]
    ]
    assert list(dfc.load_phase_artifacts()) == expected


def test_artifacts_written_during_the_close_are_not_demanded_before_it(tmp_path):
    """`PHASE_REGISTER.md` and `graph_stats.json` are sprint-scoped and real,
    and demanding them here would fail every sprint that is still open — which
    is every sprint at the moment this check fires."""
    demanded = dfc.load_phase_artifacts()
    assert "PHASE_REGISTER.md" not in demanded
    assert "graph_stats.json" not in demanded


def test_an_unreadable_registry_reports_doubt_instead_of_passing(tmp_path, monkeypatch):
    """The defect class this sprint exists to remove, one level up.

    With the list externalised, a missing registry would make the loop iterate
    over nothing and the gate report green on a sprint that left no artifact at
    all. Absence of evidence is reported as absence of evidence.
    """
    _sprint_dir(tmp_path, 23)
    monkeypatch.setattr(dfc, "ARTIFACT_REGISTRY", tmp_path / "no_such_registry.json")
    report = dfc.FreshnessReport()
    dfc.check_phase_artifacts(tmp_path, 23, report)
    messages = " ".join(f.message for f in report.findings)
    assert "did not run" in messages
    assert "IMPLEMENTATION_PLAN.md" not in messages


def test_sprint_zero_is_not_inspected(tmp_path):
    """`SPRINT_ID` unset used to fall back to 0, and this check returned on
    its first line — so it never ran from `make`, in any project. Pinning the
    early return keeps that failure visible as a deliberate boundary."""
    _sprint_dir(tmp_path, 0)
    report = dfc.FreshnessReport()
    dfc.check_phase_artifacts(tmp_path, 0, report)
    assert report.findings == []
