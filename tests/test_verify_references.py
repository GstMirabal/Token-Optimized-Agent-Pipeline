"""Tests for verify_references.py: check (d) invoked_by anchor fragments,
(f) file:line range, and (g) model↔tier map."""

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


# --- Sprint 047 U18 (S045-22): check (d) invoked_by `#fragment` resolution ---
# Unit tests for the pure functions U11 added to verify_references.py plus one
# integration pair proving the pre-U11 defect. Every case asserts the checker
# reports what it must, not merely that it stays quiet on a healthy tree.


def test_github_heading_slug_strips_punctuation_lowercases_and_hyphenates(
    verify_mod,
) -> None:
    """A heading's text maps to its GitHub anchor slug (case 1)."""
    slug = verify_mod.github_heading_slug
    # Leading `#` markers survive the caller un-stripped and are still dropped.
    assert slug("## 4. The Double-Gate Review Protocol") == (
        "4-the-double-gate-review-protocol"
    )
    # Same input with the `#` markers already removed by the caller.
    assert slug("4. The Double-Gate Review Protocol") == (
        "4-the-double-gate-review-protocol"
    )
    # Lowercasing and space -> single hyphen.
    assert slug("UPPER Case") == "upper-case"
    # Punctuation strip and whitespace-run collapse.
    assert slug("Foo: Bar,  Baz!") == "foo-bar-baz"


def test_fragment_resolves_accepts_every_anchor_form(verify_mod) -> None:
    """True for each recognised anchor form (case 2)."""
    fragment_resolves = verify_mod.fragment_resolves
    assert fragment_resolves("## Hello World\n", "hello-world") is True
    assert fragment_resolves('<a id="target"></a>\n', "target") is True
    assert fragment_resolves('<a name="target">\n', "target") is True
    assert fragment_resolves("see the `step_id` token\n", "step_id") is True
    assert fragment_resolves("run step (step_id) next\n", "step_id") is True
    assert fragment_resolves("verify:\n\tcmd\n", "verify") is True


def test_fragment_resolves_false_for_absent_fragment(verify_mod) -> None:
    """False when no anchor form matches (case 2, negative)."""
    assert verify_mod.fragment_resolves("## Hello World\n", "missing") is False


def test_resolve_invoker_path_root_relative_bare_and_missing(
    verify_mod, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Root-relative, bare-basename, Makefile, and unresolvable tokens (case 3)."""
    monkeypatch.chdir(REPO)
    resolve = verify_mod.resolve_invoker_path
    assert resolve("rules/qa_and_testing.md") == Path("rules/qa_and_testing.md")
    assert resolve("close_workflow.md") == Path("workflows/close_workflow.md")
    assert resolve("Makefile") == Path("Makefile")
    assert resolve("nope/none.md") is None


def test_check_invoked_by_anchors_flags_then_clears_missing_fragment(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Integration proving the defect (case 4).

    A ``workflows/w.md`` declaring ``invoked_by: other.md#missing-anchor`` where
    ``other.md`` carries no such anchor must produce an error naming
    ``#missing-anchor``; adding ``<a id="missing-anchor"></a>`` must clear it.

    This pair FAILS against HEAD: HEAD's verify_references.py has no
    ``check_invoked_by_anchors`` function, so ``verify_mod`` has no such
    attribute and both assertions raise ``AttributeError``.
    """
    (tmp_path / "workflows").mkdir()
    (tmp_path / "workflows" / "w.md").write_text(
        "---\ninvoked_by: other.md#missing-anchor\n---\n", encoding="utf-8"
    )
    other = tmp_path / "other.md"
    other.write_text("# Other\n\nBody text with no anchor.\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    errors = verify_mod.check_invoked_by_anchors()
    assert errors, "expected the unresolvable #fragment to be reported"
    assert any("#missing-anchor" in e for e in errors)

    other.write_text(
        '# Other\n\n<a id="missing-anchor"></a>\n\nBody text.\n', encoding="utf-8"
    )
    assert verify_mod.check_invoked_by_anchors() == []
