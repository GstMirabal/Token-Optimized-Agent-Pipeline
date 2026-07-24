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
