"""Tests for verify_references.py check (d) — RA-16 INVOCATION_COVERAGE.

The bar these tests exist to clear is the one PR #28 failed: a gate whose only
exit was an unconditional success, computed on every run and consulted on none.
So every case below asserts the checker FAILS when it should, not merely that
it passes on a healthy tree.
"""
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import verify_references as vr  # noqa: E402


@pytest.fixture
def tree(tmp_path, monkeypatch):
    """A minimal framework tree the checker can run against."""
    for name in ("workflows", "scripts", "skills", "rules", "agents", "config", "commands"):
        (tmp_path / name).mkdir()
    (tmp_path / "agents.md").write_text("# governance\n", encoding="utf-8")
    (tmp_path / "config" / "invocation_exceptions.json").write_text(
        json.dumps({"exceptions": []}), encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)
    return tmp_path


def write_exceptions(tree: Path, entries: list[dict]) -> None:
    (tree / "config" / "invocation_exceptions.json").write_text(
        json.dumps({"exceptions": entries}), encoding="utf-8"
    )


# --- the checker must be able to fail ---------------------------------

def test_workflow_without_invoker_is_reported(tree):
    (tree / "workflows" / "orphan_workflow.md").write_text("---\nversion: 1\n---\n", encoding="utf-8")
    errors = vr.check_invocation_coverage("")
    assert any("orphan_workflow.md" in e for e in errors)


def test_workflow_with_declared_invoker_passes(tree):
    (tree / "workflows" / "wired_workflow.md").write_text(
        "---\ninvoked_by: human:/agents:wired\n---\n", encoding="utf-8"
    )
    assert vr.check_invocation_coverage("") == []


def test_executable_skill_without_invoker_is_reported(tree):
    (tree / "skills" / "lonely-skill" / "scripts").mkdir(parents=True)
    errors = vr.check_invocation_coverage("")
    assert any("lonely-skill" in e for e in errors)


def test_skill_named_by_governance_passes(tree):
    (tree / "skills" / "named-skill" / "scripts").mkdir(parents=True)
    assert vr.check_invocation_coverage("uses the named-skill for this phase") == []


# --- imports count as invocation (the merge_json false positive) ------

def test_module_imported_by_another_script_is_not_orphan(tree):
    """A script imported as a module has an invoker even though its filename
    appears nowhere. Missing this nearly deleted `merge_json.py`, which
    `install_claude.py` imports and the bridge installer depends on."""
    (tree / "scripts" / "helper.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tree / "scripts" / "caller.py").write_text(
        '"""invoked_by: Makefile."""\nfrom helper import VALUE\n', encoding="utf-8"
    )
    assert vr.check_invocation_coverage("") == []


def test_script_neither_imported_nor_declared_is_reported(tree):
    (tree / "scripts" / "dead.py").write_text("VALUE = 1\n", encoding="utf-8")
    errors = vr.check_invocation_coverage("")
    assert any("dead.py" in e for e in errors)


# --- the exception registry must not rot ------------------------------

def test_exception_for_missing_path_is_reported(tree):
    """A stale exemption silently excuses the next artifact to take that name."""
    write_exceptions(tree, [{"path": "skills/deleted-skill", "reason": "model-invoked"}])
    errors = vr.check_invocation_coverage("")
    assert any("stale exemption" in e for e in errors)


def test_untyped_exception_reason_is_reported(tree):
    (tree / "skills" / "excused" / "scripts").mkdir(parents=True)
    write_exceptions(tree, [{"path": "skills/excused", "reason": "because I said so"}])
    errors = vr.check_invocation_coverage("")
    assert any("not one of" in e for e in errors)


def test_typed_exception_silences_the_finding(tree):
    (tree / "skills" / "excused" / "scripts").mkdir(parents=True)
    write_exceptions(tree, [{"path": "skills/excused", "reason": "vendored-reference"}])
    assert vr.check_invocation_coverage("") == []


def test_missing_registry_is_reported(tree):
    os.remove(tree / "config" / "invocation_exceptions.json")
    errors = vr.check_invocation_coverage("")
    assert any("cannot be evaluated" in e for e in errors)
