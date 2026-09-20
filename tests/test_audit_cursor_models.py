"""Tests for scripts/audit_cursor_models.py --resolve (Sprint 035 E4)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import audit_cursor_models as acm  # noqa: E402

MINIMAL_TIERS: dict[str, Any] = {
    "tiers": {
        "mechanical": {
            "cursor": {"model": "composer-2.5", "family": "cursor"},
        },
        "author": {
            "cursor": {"model": "grok-4.5", "family": "xai", "effort": "high"},
        },
        "gate": {
            "cursor": {"model": None, "family": None},
        },
    },
}


def _write_tiers(path: Path, payload: dict[str, Any] | None = None) -> Path:
    path.write_text(json.dumps(payload or MINIMAL_TIERS), encoding="utf-8")
    return path


def _isolate_agents(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stem: str,
    body: str,
) -> Path:
    """Point AGENTS_DIR at a temp tree; rebind read_profile_tier default."""
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / f"{stem}.md").write_text(body, encoding="utf-8")
    monkeypatch.setattr(acm, "AGENTS_DIR", agents)
    original = acm.read_profile_tier

    def _read(stem_name: str, agents_dir: Path | None = None) -> str | None:
        return original(stem_name, agents if agents_dir is None else agents_dir)

    monkeypatch.setattr(acm, "read_profile_tier", _read)
    return agents


def test_resolve_mechanical_returns_fixture_model(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tiers = _write_tiers(tmp_path / "model_tiers.json")
    code = acm.run_resolve("mechanical", tiers_path=tiers)
    out = capsys.readouterr().out
    assert code == 0
    assert "modelId=composer-2.5" in out
    assert "effort=" in out


def test_resolve_gate_null_model_is_session(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tiers = _write_tiers(tmp_path / "model_tiers.json")
    code = acm.run_resolve("gate", tiers_path=tiers)
    out = capsys.readouterr().out
    assert code == 0
    assert "modelId=session" in out
    assert "effort=" in out


def test_resolve_profile_reads_tier_frontmatter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tiers = _write_tiers(tmp_path / "model_tiers.json")
    _isolate_agents(
        tmp_path,
        monkeypatch,
        "demo_agent",
        "---\nname: demo\ntier: mechanical\n---\n\n# Demo\n",
    )
    code = acm.run_resolve("demo_agent", tiers_path=tiers)
    out = capsys.readouterr().out
    assert code == 0
    assert "modelId=composer-2.5" in out


def test_resolve_unknown_profile_exits_2(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tiers = _write_tiers(tmp_path / "model_tiers.json")
    agents = tmp_path / "agents"
    agents.mkdir()
    monkeypatch.setattr(acm, "AGENTS_DIR", agents)
    code = acm.run_resolve("missing_profile", tiers_path=tiers)
    err = capsys.readouterr().err
    assert code == 2
    assert "not found" in err


def test_resolve_profile_missing_tier_exits_2(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    tiers = _write_tiers(tmp_path / "model_tiers.json")
    _isolate_agents(
        tmp_path,
        monkeypatch,
        "no_tier_agent",
        "---\nname: no-tier\n---\n\n# No tier\n",
    )
    code = acm.run_resolve("no_tier_agent", tiers_path=tiers)
    err = capsys.readouterr().err
    assert code == 2
    assert "no tier:" in err


def test_propose_tiers_gate_structural_ceiling_without_proven_families() -> None:
    """Regression: Design §D13 — gate fills via structural ceiling with empty proven history."""
    models = [
        {
            "name": "grok-4.5",
            "supportsAgent": True,
            "degradationStatus": 0,
            "parameterDefinitions": [{"id": "effort"}],
        },
        {
            "name": "claude-opus-4-6",
            "supportsAgent": True,
            "degradationStatus": 0,
            "parameterDefinitions": [{"id": "effort"}],
        },
        {
            "name": "composer-2.5",
            "supportsAgent": True,
            "degradationStatus": 0,
            "parameterDefinitions": [],
        },
    ]
    proposals = acm.propose_tiers(
        models,
        applied_model_id="composer-2.5",
        proven_families=set(),
        map_author_model="grok-4.5",
        map_author_family="xai",
        preferred_gate_family="anthropic",
    )
    assert proposals["gate"]
    assert all(row["family"] != "xai" for row in proposals["gate"])
    assert any(row["name"] == "claude-opus-4-6" for row in proposals["gate"])


def test_main_resolve_mechanical_via_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """CLI path: main --resolve uses run_resolve (no Cursor DB)."""
    tiers = _write_tiers(tmp_path / "model_tiers.json")
    original = acm.run_resolve

    def _resolve(target: str, tiers_path: Path | None = None) -> int:
        return original(target, tiers if tiers_path is None else tiers_path)

    monkeypatch.setattr(acm, "run_resolve", _resolve)
    code = acm.main(["--resolve", "mechanical"])
    out = capsys.readouterr().out
    assert code == 0
    assert "modelId=composer-2.5" in out


# --- F-049-4: applied-vs-map drift must fail --check, not just print it ----


def test_author_cell_discrepancy_true_when_both_known_and_differ() -> None:
    """Measured live: `make cursor-tiers` printed this exact pair and exited 0."""
    assert acm.author_cell_discrepancy("grok-4.6", "glm-5.2") is True


def test_author_cell_discrepancy_false_when_equal() -> None:
    assert acm.author_cell_discrepancy("glm-5.2", "glm-5.2") is False


def test_author_cell_discrepancy_false_when_either_side_unknown() -> None:
    assert acm.author_cell_discrepancy(None, "glm-5.2") is False
    assert acm.author_cell_discrepancy("glm-5.2", None) is False
    assert acm.author_cell_discrepancy(None, None) is False


def _stub_catalogue(monkeypatch: pytest.MonkeyPatch, models: list[dict[str, Any]]) -> None:
    monkeypatch.setattr(acm, "open_catalogue", lambda db_path: models)


def test_run_report_flags_author_discrepancy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_catalogue(
        monkeypatch,
        [
            {
                "name": "grok-4.6",
                "supportsAgent": True,
                "degradationStatus": 0,
                "parameterDefinitions": [{"id": "effort"}],
            }
        ],
    )
    monkeypatch.setattr(acm, "read_applied_model_id", lambda db_path: "grok-4.6")
    monkeypatch.setattr(acm, "read_map_author_cursor", lambda: ("glm-5.2", "zhipu"))
    monkeypatch.setattr(acm, "read_map_gate_claude_family", lambda: None)
    proposals = acm.run_report(tmp_path / "fake.vscdb")
    assert proposals["author_discrepancy"] is True


def test_run_report_no_discrepancy_when_applied_matches_map(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stub_catalogue(
        monkeypatch,
        [
            {
                "name": "glm-5.2",
                "supportsAgent": True,
                "degradationStatus": 0,
                "parameterDefinitions": [{"id": "effort"}],
            }
        ],
    )
    monkeypatch.setattr(acm, "read_applied_model_id", lambda db_path: "glm-5.2")
    monkeypatch.setattr(acm, "read_map_author_cursor", lambda: ("glm-5.2", "zhipu"))
    monkeypatch.setattr(acm, "read_map_gate_claude_family", lambda: None)
    proposals = acm.run_report(tmp_path / "fake.vscdb")
    assert proposals["author_discrepancy"] is False


def test_run_report_db_absent_no_discrepancy(tmp_path: Path) -> None:
    """`open_catalogue` returns None for a missing DB; nothing to compare."""
    proposals = acm.run_report(tmp_path / "does-not-exist.vscdb")
    assert proposals["author_discrepancy"] is False


def test_main_check_exits_2_on_author_discrepancy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI regression: before this fix, --check printed the mismatch and
    still exited 0 (measured: `make cursor-tiers` on this repository)."""
    _stub_catalogue(
        monkeypatch,
        [
            {
                "name": "grok-4.6",
                "supportsAgent": True,
                "degradationStatus": 0,
                "parameterDefinitions": [{"id": "effort"}],
            },
            {
                "name": "claude-opus-5",
                "supportsAgent": True,
                "degradationStatus": 0,
                "parameterDefinitions": [{"id": "effort"}],
            },
        ],
    )
    monkeypatch.setattr(acm, "read_applied_model_id", lambda db_path: "grok-4.6")
    monkeypatch.setattr(acm, "read_map_author_cursor", lambda: ("glm-5.2", "zhipu"))
    monkeypatch.setattr(acm, "read_map_gate_claude_family", lambda: "anthropic")
    fake_db = tmp_path / "fake.vscdb"
    fake_db.write_bytes(b"")
    code = acm.main(["--check", "--db", str(fake_db)])
    err = capsys.readouterr().err
    assert code == 2
    assert "differs from the tier map" in err


def test_main_check_passes_when_applied_matches_map(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _stub_catalogue(
        monkeypatch,
        [
            {
                "name": "glm-5.2",
                "supportsAgent": True,
                "degradationStatus": 0,
                "parameterDefinitions": [{"id": "effort"}],
            },
            {
                "name": "claude-opus-5",
                "supportsAgent": True,
                "degradationStatus": 0,
                "parameterDefinitions": [{"id": "effort"}],
            },
        ],
    )
    monkeypatch.setattr(acm, "read_applied_model_id", lambda db_path: "glm-5.2")
    monkeypatch.setattr(acm, "read_map_author_cursor", lambda: ("glm-5.2", "zhipu"))
    monkeypatch.setattr(acm, "read_map_gate_claude_family", lambda: "anthropic")
    fake_db = tmp_path / "fake.vscdb"
    fake_db.write_bytes(b"")
    code = acm.main(["--check", "--db", str(fake_db)])
    out = capsys.readouterr().out
    assert code == 0
    assert "gate proposals present, author cell matches applied model" in out
