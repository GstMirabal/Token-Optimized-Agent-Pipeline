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


def test_check_invoked_by_anchors_covers_skills_scripts_and_tests_trees(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sprint 048 U8 (KI-047-3): the anchor-resolution tree list now also scans
    ``skills/*/scripts/*.py`` and ``tests/*.py`` — the coverage half of check
    (d), ``check_invocation_coverage``, is deliberately left untouched (a
    separate, larger sweep).

    A fixture script under ``skills/sample-skill/scripts/`` and a fixture test
    under ``tests/`` each declare an ``invoked_by:`` token whose ``#fragment``
    does not resolve in the target file; both must be reported.
    """
    (tmp_path / "skills" / "sample-skill" / "scripts").mkdir(parents=True)
    (tmp_path / "skills" / "sample-skill" / "scripts" / "run.py").write_text(
        '"""\ninvoked_by: other.md#missing-anchor\n"""\n', encoding="utf-8"
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_fixture.py").write_text(
        '"""\ninvoked_by: other.md#missing-anchor\n"""\n', encoding="utf-8"
    )
    other = tmp_path / "other.md"
    other.write_text("# Other\n\nBody text with no anchor.\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    errors = verify_mod.check_invoked_by_anchors()
    assert len(errors) == 2, f"expected one error per fixture file, got: {errors}"
    assert any("skills/sample-skill/scripts/run.py" in e for e in errors)
    assert any("tests/test_fixture.py" in e for e in errors)

    other.write_text(
        '# Other\n\n<a id="missing-anchor"></a>\n\nBody text.\n', encoding="utf-8"
    )
    assert verify_mod.check_invoked_by_anchors() == []


# --- Sprint 052 U19 (KI-048-1 D9): check (d) coverage over skills/*/scripts/*.py
# and tests/*.py, with typed per-tree rules rather than a blanket exception.
# `check_invocation_coverage` glob'd only workflows/, scripts/, hooks/ before this
# unit; these prove the two added trees actually fail the checker when nothing
# invokes them, not merely that a healthy tree stays quiet.


def _base_tree(root: Path) -> None:
    """Scaffold the minimal directories `check_invocation_coverage` reads."""
    for name in (
        "workflows", "scripts", "hooks", "skills",
        "rules", "agents", "config", "commands", "tests",
    ):
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "agents.md").write_text("# governance\n", encoding="utf-8")
    (root / "config" / "invocation_exceptions.json").write_text(
        json.dumps({"exceptions": []}), encoding="utf-8"
    )


def _write_pytest_makefile(root: Path) -> None:
    """A `verify:` recipe that collects `tests/` via pytest, like the real one."""
    (root / "Makefile").write_text(
        "verify:\n\tpython3 scripts/py_compile_tree.py\n\t$(PY) -m pytest tests/ -q\n",
        encoding="utf-8",
    )


def test_uninvoked_skill_script_is_flagged(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9: a skills/<s>/scripts/*.py named by nothing and imported by nothing fails."""
    root = tmp_path
    _base_tree(root)
    (root / "skills" / "x" / "scripts").mkdir(parents=True)
    (root / "skills" / "x" / "scripts" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert any("skills/x/scripts/helper.py" in e for e in errors)


def test_skill_script_named_in_makefile_recipe_passes(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9 coordinator extension: a Makefile recipe line (any target, not just
    `verify`) naming the script's repo-relative path resolves it."""
    root = tmp_path
    _base_tree(root)
    (root / "skills" / "x" / "scripts").mkdir(parents=True)
    (root / "skills" / "x" / "scripts" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "Makefile").write_text(
        "other-target:\n\tpython3 skills/x/scripts/helper.py\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert not any("skills/x/scripts/helper.py" in e for e in errors)


def test_skill_script_declaring_invoked_by_passes(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9 coordinator extension: the script's own `invoked_by:` docstring
    resolves it — the same mechanism scripts/ and hooks/ already use."""
    root = tmp_path
    _base_tree(root)
    (root / "skills" / "x" / "scripts").mkdir(parents=True)
    (root / "skills" / "x" / "scripts" / "helper.py").write_text(
        '"""\ninvoked_by: human-entry-point.\n"""\nVALUE = 1\n', encoding="utf-8"
    )
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert not any("skills/x/scripts/helper.py" in e for e in errors)


def test_skill_script_mentioned_only_in_makefile_comment_is_still_flagged(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9 coordinator extension: a mention that lives only in a Makefile
    comment — top-level `#` line or a `#`-led line inside a recipe — is not a
    real invocation and must not silence the finding."""
    root = tmp_path
    _base_tree(root)
    (root / "skills" / "x" / "scripts").mkdir(parents=True)
    (root / "skills" / "x" / "scripts" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "Makefile").write_text(
        "# See skills/x/scripts/helper.py for the procedure.\n"
        "other-target:\n"
        "\t# skills/x/scripts/helper.py is documented, not run, here.\n"
        "\ttrue\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert any("skills/x/scripts/helper.py" in e for e in errors)


def test_skill_script_named_in_skill_md_passes(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9: naming the script in SKILL.md resolves it."""
    root = tmp_path
    _base_tree(root)
    (root / "skills" / "x" / "scripts").mkdir(parents=True)
    (root / "skills" / "x" / "scripts" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "skills" / "x" / "SKILL.md").write_text(
        "---\nname: x\ndescription: stub\n---\nRun `helper.py` to do the thing.\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert not any("skills/x/scripts/helper.py" in e for e in errors)


def test_skill_script_named_as_dotted_module_in_skill_md_passes(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9: `python -m scripts.helper` in SKILL.md resolves `scripts/helper.py`."""
    root = tmp_path
    _base_tree(root)
    (root / "skills" / "x" / "scripts").mkdir(parents=True)
    (root / "skills" / "x" / "scripts" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "skills" / "x" / "SKILL.md").write_text(
        "---\nname: x\ndescription: stub\n---\nRun `python -m scripts.helper` to do the thing.\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert not any("skills/x/scripts/helper.py" in e for e in errors)


def test_skill_script_dotted_module_prefix_of_longer_name_does_not_pass(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9: `scripts.helper_extra` must not resolve `scripts/helper.py` — a
    dotted-module mention that is only a prefix of a longer module name is
    not a whole-token match."""
    root = tmp_path
    _base_tree(root)
    (root / "skills" / "x" / "scripts").mkdir(parents=True)
    (root / "skills" / "x" / "scripts" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "skills" / "x" / "SKILL.md").write_text(
        "---\nname: x\ndescription: stub\n---\nRun `python -m scripts.helper_extra` instead.\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert any("skills/x/scripts/helper.py" in e for e in errors)


def test_skill_script_imported_by_named_script_passes(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9: a helper imported by a resolved sibling script resolves via the import scan."""
    root = tmp_path
    _base_tree(root)
    (root / "skills" / "x" / "scripts").mkdir(parents=True)
    (root / "skills" / "x" / "scripts" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "skills" / "x" / "scripts" / "run.py").write_text(
        '"""\ninvoked_by: human-entry-point.\n"""\nfrom helper import VALUE\n',
        encoding="utf-8",
    )
    (root / "skills" / "x" / "SKILL.md").write_text(
        "---\nname: x\ndescription: stub\n---\nRun `run.py`.\n", encoding="utf-8"
    )
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert not any("skills/x/scripts/helper.py" in e for e in errors)


def test_test_file_passes_via_pytest_collection_with_no_invoked_by(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9: tests/test_*.py needs no invoked_by — make verify's pytest step covers it."""
    root = tmp_path
    _base_tree(root)
    _write_pytest_makefile(root)
    (root / "tests" / "test_foo.py").write_text(
        "def test_x():\n    assert True\n", encoding="utf-8"
    )
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert not any("tests/test_foo.py" in e for e in errors)


def test_uninvoked_test_helper_is_flagged(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9: tests/_util.py imported by nothing and declaring no invoked_by fails."""
    root = tmp_path
    _base_tree(root)
    _write_pytest_makefile(root)
    (root / "tests" / "_util.py").write_text("VALUE = 1\n", encoding="utf-8")
    monkeypatch.chdir(root)
    errors = verify_mod.check_invocation_coverage("")
    assert any("tests/_util.py" in e for e in errors)


def test_skill_scripts_naming_import_and_cycle_bypasses_are_closed(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """F-1: doc-token, import-path, and mutual-import bypasses are closed.

    Reproduces the gate's five-file fixture: a SKILL.md containing the
    unrelated word "environment" must not resolve `env.py` (bug a); a
    stdlib `import json` in an unrelated `scripts/tool.py` must not resolve
    `skills/foo/scripts/json.py`, since `tool.py` is not a sibling in that
    directory (bug c); and two mutually-importing orphans (`cyc_a.py` /
    `cyc_b.py`), neither directly resolved, must not resolve each other
    (bug b). `orphan_helper.py` has no resolution path at all and stays
    flagged as a control.
    """
    root = tmp_path
    _base_tree(root)
    skill_scripts = root / "skills" / "foo" / "scripts"
    skill_scripts.mkdir(parents=True)
    for name, body in (
        ("json.py", "VALUE = 1\n"),
        ("env.py", "VALUE = 1\n"),
        ("cyc_a.py", "import cyc_b\n"),
        ("cyc_b.py", "import cyc_a\n"),
        ("orphan_helper.py", "VALUE = 1\n"),
    ):
        (skill_scripts / name).write_text(body, encoding="utf-8")
    (root / "skills" / "foo" / "SKILL.md").write_text(
        "---\nname: foo\ndescription: stub\n---\nRuns in this environment.\n",
        encoding="utf-8",
    )
    (root / "scripts" / "tool.py").write_text("import json\n", encoding="utf-8")
    monkeypatch.chdir(root)

    errors = verify_mod.check_invocation_coverage("")
    for expected in ("json.py", "env.py", "cyc_a.py", "cyc_b.py", "orphan_helper.py"):
        assert any(f"skills/foo/scripts/{expected}" in e for e in errors), (
            f"expected {expected} to be flagged, got: {errors}"
        )


def test_script_imported_only_by_its_test_file_is_still_flagged(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """F-2 regression (vs `ca70bfa`): a test importing production code does
    not invoke it. `scripts/orphan.py`, imported only by
    `tests/test_orphan.py`, must stay flagged — Sprint 052 U19 widened
    `imported_modules()` to also scan `tests/`, and the scripts/hooks
    invocation loop reused that same widened set, so this passed silently."""
    root = tmp_path
    _base_tree(root)
    _write_pytest_makefile(root)
    (root / "scripts" / "orphan.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "tests" / "test_orphan.py").write_text(
        "from orphan import VALUE\n\ndef test_x():\n    assert VALUE == 1\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(root)

    errors = verify_mod.check_invocation_coverage("")
    assert any("scripts/orphan.py" in e for e in errors), (
        f"expected scripts/orphan.py to be flagged, got: {errors}"
    )


def test_pytest_coverage_claim_is_derived_from_makefile_not_hardcoded(
    verify_mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D9: if `verify:` stops running pytest, a bare test_*.py must be flagged
    again rather than staying silently exempt on a hard-coded assumption."""
    root = tmp_path
    _base_tree(root)
    (root / "Makefile").write_text(
        "verify:\n\tpython3 scripts/py_compile_tree.py\n", encoding="utf-8"
    )
    (root / "tests" / "test_foo.py").write_text(
        "def test_x():\n    assert True\n", encoding="utf-8"
    )
    monkeypatch.chdir(root)
    assert verify_mod._pytest_covers_tests_dir() is False
    errors = verify_mod.check_invocation_coverage("")
    assert any("tests/test_foo.py" in e for e in errors)
