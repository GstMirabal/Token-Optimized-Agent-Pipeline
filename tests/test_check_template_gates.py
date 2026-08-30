"""Tests for scripts/check_template_gates.py — template/gate parity (Sprint 042).

Every check here fails against the tree before Sprint 042, where no mechanism
compared a versioned template against the check that consumes what an author
writes from it. Sprint 041 found three such divergences by tripping over them
during its own phases; nothing detected them.

Fixtures build a synthetic framework root in tmp_path — never the real
docs/standards/templates/. A check that decides by pattern-matching prose trips
over explanatory text, which is how the real repair was broken twice while it was
being documented (Sprint 041 U11).
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

PLACEHOLDER = "{{SPRINT_ID}}"
MARKER = "the string a gate refuses"


@pytest.fixture()
def module(monkeypatch: pytest.MonkeyPatch):
    """Import check_template_gates with scripts/ on sys.path."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("check_template_gates", None)
    return importlib.import_module("check_template_gates")


def _fake_gate(root: Path, name: str, body: str) -> str:
    """Write a stand-in gate script and return its repo-relative path."""
    path = root / "scripts" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return f"scripts/{name}"


REFUSES_MARKER = f'''import sys
from pathlib import Path
text = Path(sys.argv[1]).read_text()
sys.exit(2 if {MARKER!r} in text else 0)
'''

REQUIRES_PLACEHOLDER = f'''import sys
from pathlib import Path
text = Path(sys.argv[1]).read_text()
sys.exit(0 if {PLACEHOLDER!r} in text else 2)
'''


def _root(tmp_path: Path, template_body: str, gate_body: str = REFUSES_MARKER) -> Path:
    """Build a synthetic framework root with one template and one gate."""
    root = tmp_path / "framework"
    templates = root / "docs" / "standards" / "templates"
    templates.mkdir(parents=True)
    (templates / "SPEC_TEMPLATE.md").write_text(template_body, encoding="utf-8")
    gate = _fake_gate(root, "fake_gate.py", gate_body)
    spec = {
        "scratch_sprint_dir": "999-core-pipeline",
        "cases": [
            {
                "id": "spec",
                "render": {"SPEC_TEMPLATE.md": "SPEC.md"},
                "command": ["python3", gate, "{sprint_dir}/SPEC.md"],
            }
        ],
        "exceptions": [],
    }
    (root / "config").mkdir()
    (root / "config" / "template_gates.json").write_text(json.dumps(spec), encoding="utf-8")
    return root


def _spec(root: Path) -> dict:
    return json.loads((root / "config" / "template_gates.json").read_text(encoding="utf-8"))


def _write_spec(root: Path, spec: dict) -> None:
    (root / "config" / "template_gates.json").write_text(json.dumps(spec), encoding="utf-8")


# --- The real declaration -------------------------------------------------


def test_real_repository_passes(module) -> None:
    """The shipped pairing is green: the guard guards something that holds."""
    assert module.check(REPO, module.CONFIG) == 0


def test_real_declaration_covers_every_template(module) -> None:
    """Completeness holds against the real templates directory."""
    spec = module.load_config(REPO, module.CONFIG)
    assert module.check_completeness(REPO, spec) == []


def test_run_leaves_no_scratch_directory_in_the_repository(module) -> None:
    """Rendering happens in a temporary directory, never in the tree."""
    module.check(REPO, module.CONFIG)
    spec = module.load_config(REPO, module.CONFIG)
    assert not (REPO / spec["scratch_sprint_dir"]).exists()
    assert not (REPO / "docs" / "sprints" / spec["scratch_sprint_dir"]).exists()


# --- The defect this sprint exists to catch -------------------------------


def test_divergent_template_is_rejected(tmp_path: Path, module, capsys) -> None:
    """A template its own gate refuses fails the build.

    This is the Sprint 041 class: an author copying the template would produce an
    artifact the mandatory gate rejects.
    """
    root = _root(tmp_path, f"# Spec\n\n{MARKER}\n")
    assert module.check(root, module.CONFIG) == 2
    assert "spec:" in capsys.readouterr().err


def test_conforming_template_passes(tmp_path: Path, module) -> None:
    root = _root(tmp_path, "# Spec\n\nnothing objectionable\n")
    assert module.check(root, module.CONFIG) == 0


# --- Verbatim rendering (no placeholder substitution) ---------------------


def test_placeholders_reach_the_gate_untouched(tmp_path: Path, module) -> None:
    """The copy is verbatim.

    Substituting {{...}} would measure the fixture that replaced them rather than
    the template, and a broken template could pass because the substitution fixed
    it. The gate here exits 0 only while the placeholder survives.
    """
    root = _root(tmp_path, f"# Spec {PLACEHOLDER}\n", gate_body=REQUIRES_PLACEHOLDER)
    assert module.check(root, module.CONFIG) == 0


# --- Completeness (a template with no case and no exception) --------------


def test_undeclared_template_fails(tmp_path: Path, module, capsys) -> None:
    root = _root(tmp_path, "# Spec\n")
    (root / "docs" / "standards" / "templates" / "ORPHAN_TEMPLATE.md").write_text("x", encoding="utf-8")
    assert module.check(root, module.CONFIG) == 2
    assert "ORPHAN_TEMPLATE.md" in capsys.readouterr().err


def test_typed_exception_satisfies_completeness(tmp_path: Path, module) -> None:
    root = _root(tmp_path, "# Spec\n")
    (root / "docs" / "standards" / "templates" / "ORPHAN_TEMPLATE.md").write_text("x", encoding="utf-8")
    spec = _spec(root)
    spec["exceptions"] = [
        {"template": "ORPHAN_TEMPLATE.md", "reason": "no-automated-gate", "note": "read by humans"}
    ]
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 0


def test_exception_for_a_deleted_template_fails(tmp_path: Path, module, capsys) -> None:
    """A stale exemption silently excuses the next file to take that name."""
    root = _root(tmp_path, "# Spec\n")
    spec = _spec(root)
    spec["exceptions"] = [
        {"template": "GONE_TEMPLATE.md", "reason": "no-automated-gate", "note": "removed"}
    ]
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 2
    assert "GONE_TEMPLATE.md" in capsys.readouterr().err


# --- The command contract: this declaration is executed -------------------


def test_interpreter_is_pinned(tmp_path: Path, module) -> None:
    root = _root(tmp_path, "# Spec\n")
    assert module.check_command(root, ["bash", "scripts/fake_gate.py"]) is not None
    assert module.check_command(root, ["python3", "scripts/fake_gate.py"]) is None


def test_script_may_not_escape_the_framework_root(tmp_path: Path, module) -> None:
    root = _root(tmp_path, "# Spec\n")
    outside = tmp_path / "outside.py"
    outside.write_text("", encoding="utf-8")
    finding = module.check_command(root, ["python3", "../outside.py"])
    assert finding is not None
    assert "escapes" in finding


def test_missing_script_is_reported(tmp_path: Path, module) -> None:
    root = _root(tmp_path, "# Spec\n")
    finding = module.check_command(root, ["python3", "scripts/absent.py"])
    assert finding is not None
    assert "does not exist" in finding


def test_bare_command_is_rejected(tmp_path: Path, module) -> None:
    root = _root(tmp_path, "# Spec\n")
    assert module.check_command(root, ["python3"]) is not None


def test_forbidden_command_fails_the_run(tmp_path: Path, module, capsys) -> None:
    """A refused command fails the build instead of being skipped."""
    root = _root(tmp_path, "# Spec\n")
    spec = _spec(root)
    spec["cases"][0]["command"] = ["sh", "-c", "true"]
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 2
    assert "python3" in capsys.readouterr().err


def test_only_the_sprint_dir_token_is_expanded(tmp_path: Path, module) -> None:
    """No general templating: any other brace token reaches the gate literally."""
    root = _root(tmp_path, "# Spec\n")
    echo = _fake_gate(
        root,
        "echo_gate.py",
        'import sys\nsys.exit(0 if sys.argv[1] == "{root}" and "999" in sys.argv[2] else 2)\n',
    )
    spec = _spec(root)
    spec["cases"][0]["command"] = ["python3", echo, "{root}", "{sprint_dir}"]
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 0


# --- The instrument must not become a second copy of the gates ------------


def test_no_gate_is_named_in_the_source() -> None:
    """The abort criterion of the sprint, as an assertion.

    A checker that branches on which gate it is running is a second copy of the
    gates, and the second copy drifts — the defect this sprint closes, one level
    up. Gate names belong in config/template_gates.json.
    """
    source = (SCRIPTS / "check_template_gates.py").read_text(encoding="utf-8")
    for name in ("audit_plan", "forge_ladder", "gate_log", "role_artifact", "task_scope"):
        assert name not in source
