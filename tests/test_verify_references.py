"""Tests for verify_references.py checks (f) file:line and (g) model↔tier."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


@pytest.fixture()
def verify_mod(monkeypatch: pytest.MonkeyPatch) -> object:
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("verify_references", None)
    return importlib.import_module("verify_references")


def test_out_of_range_file_line_in_guides_is_rejected(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """J6.0: a citation like README.md:99999 under living docs/ must fail."""
    root = tmp_path
    (root / "docs" / "guides").mkdir(parents=True)
    (root / "docs" / "decisions").mkdir(parents=True)
    (root / "docs" / "audits").mkdir(parents=True)
    (root / "README.md").write_text("# one\n", encoding="utf-8")
    (root / "docs" / "guides" / "SAMPLE_GUIDE.md").write_text(
        "See `README.md:99999` for details.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(verify_mod, "agents_root", lambda: root)
    monkeypatch.chdir(root)
    errors = verify_mod.check_file_line_citations()
    assert errors, "expected out-of-range citation to be rejected"
    assert any("README.md:99999" in e for e in errors)


def test_in_range_file_line_passes(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path
    (root / "docs" / "guides").mkdir(parents=True)
    (root / "docs" / "decisions").mkdir(parents=True)
    (root / "docs" / "audits").mkdir(parents=True)
    (root / "README.md").write_text("# one\n# two\n", encoding="utf-8")
    (root / "docs" / "guides" / "SAMPLE_GUIDE.md").write_text(
        "See `README.md:2` for details.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(verify_mod, "agents_root", lambda: root)
    monkeypatch.chdir(root)
    assert verify_mod.check_file_line_citations() == []


def test_sprint_records_are_not_scanned(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Abort criterion 3: historical sprint prose must not trip the check."""
    root = tmp_path
    (root / "docs" / "guides").mkdir(parents=True)
    (root / "docs" / "decisions").mkdir(parents=True)
    (root / "docs" / "audits").mkdir(parents=True)
    (root / "docs" / "sprints" / "023-core-pipeline").mkdir(parents=True)
    (root / "README.md").write_text("# one\n", encoding="utf-8")
    (root / "docs" / "sprints" / "023-core-pipeline" / "task_scope.md").write_text(
        "bogus `README.md:99999`\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(verify_mod, "agents_root", lambda: root)
    monkeypatch.chdir(root)
    assert verify_mod.check_file_line_citations() == []


def _write_tier_map(root: Path, *, claude_model: str) -> None:
    (root / "config").mkdir(parents=True, exist_ok=True)
    (root / "config" / "model_tiers.json").write_text(
        json.dumps(
            {
                "tiers": {
                    "gate": {
                        "claude_code": {"model": claude_model},
                    }
                }
            }
        ),
        encoding="utf-8",
    )


def _write_agent_profile(root: Path, *, model: str, tier: str) -> None:
    (root / "agents").mkdir(parents=True, exist_ok=True)
    (root / "agents" / "qa_agent.md").write_text(
        f"---\nname: qa-agent\nmodel: {model}\ntier: {tier}\n---\n# stub\n",
        encoding="utf-8",
    )


def test_agents_model_mismatch_vs_tier_map_cites_g(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(g): frontmatter model must equal model_tiers[tier].claude_code.model."""
    root = tmp_path
    _write_tier_map(root, claude_model="opus")
    _write_agent_profile(root, model="sonnet", tier="gate")
    monkeypatch.chdir(root)
    errors = verify_mod.check_agents_model_tier_map()
    assert errors, "expected model≠map mismatch to be rejected"
    assert any("(g)" in e for e in errors)
    assert any("sonnet" in e and "opus" in e for e in errors)


def test_agents_model_matching_tier_map_passes(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(g): agreeing model/tier produces no (g) error."""
    root = tmp_path
    _write_tier_map(root, claude_model="opus")
    _write_agent_profile(root, model="opus", tier="gate")
    monkeypatch.chdir(root)
    errors = verify_mod.check_agents_model_tier_map()
    assert errors == []
    assert not any("(g)" in e for e in errors)
