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
        "_valid_exception_reasons": ["no-automated-gate", "phase-mismatch"],
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


def test_sibling_directory_extending_the_root_name_is_outside_it(tmp_path: Path, module) -> None:
    """Containment, not a name prefix.

    The first implementation compared strings with `startswith`, so
    `<root>-anything/` read as inside `<root>/`. That is not hypothetical here:
    `agents.md §3 topological_order` puts host profiles at `<host-root>/.agents-profile/`
    beside the `<host-root>/.agents` submodule, so the bypass was the documented
    convention. Found by Gate 1 of Sprint 042, after the easy `../outside.py` case
    above had passed.
    """
    root = _root(tmp_path, "# Spec\n")
    sibling = root.parent / f"{root.name}-evil"
    sibling.mkdir()
    (sibling / "pwn.py").write_text("", encoding="utf-8")
    finding = module.check_command(root, ["python3", f"../{sibling.name}/pwn.py"])
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


# --- The render map is data that reaches the filesystem -------------------


def test_render_source_outside_the_templates_directory_is_refused(
    tmp_path: Path, module, capsys
) -> None:
    """A declaration may not read an arbitrary file.

    The first implementation guarded the argument vector only, so this copied a
    file from anywhere the process could read. Found by Gate 1 of Sprint 042.
    """
    root = _root(tmp_path, "# Spec\n")
    secret = tmp_path / "secret.txt"
    secret.write_text("credentials", encoding="utf-8")
    spec = _spec(root)
    spec["cases"][0]["render"] = {"../../../../secret.txt": "SPEC.md"}
    spec["exceptions"] = [
        {"template": "SPEC_TEMPLATE.md", "reason": "no-automated-gate", "note": "unpaired here"}
    ]
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 2
    assert "render source" in capsys.readouterr().err


def test_render_target_may_not_escape_the_scratch_directory(
    tmp_path: Path, module, capsys
) -> None:
    """A declaration may not overwrite an arbitrary file."""
    victim = tmp_path / "victim.md"
    victim.write_text("original", encoding="utf-8")
    root = _root(tmp_path, "# Spec\n")
    spec = _spec(root)
    spec["cases"][0]["render"] = {"SPEC_TEMPLATE.md": "../../../../victim.md"}
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 2
    assert "escapes the scratch directory" in capsys.readouterr().err
    assert victim.read_text(encoding="utf-8") == "original"


def test_case_id_may_not_escape_the_temporary_directory(tmp_path: Path, module, capsys) -> None:
    """The scratch anchor is verified, not just the fields joined onto it.

    `sprint_dir` is `scratch / case["id"] / scratch_sprint_dir`. Validating only
    the last component left the middle one free, and target containment is then
    measured against an anchor the declaration chose — satisfied by construction,
    so the run exited 0 while writing outside the temporary directory. Found by
    Gate 1 round 2 of Sprint 042. This asserts the anchor, not the field, so a
    fourth component joined onto that expression is contained without a new test.
    """
    root = _root(tmp_path, "# Spec\n")
    escape = tmp_path / "outside_scratch"
    spec = _spec(root)
    spec["cases"][0]["id"] = f"../../../../../..{escape}"
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 2
    assert "escapes the temporary directory" in capsys.readouterr().err
    assert not escape.exists()


def test_scratch_directory_name_must_be_one_component(tmp_path: Path, module, capsys) -> None:
    """A traversing scratch name wrote outside the temporary directory."""
    root = _root(tmp_path, "# Spec\n")
    spec = _spec(root)
    spec["scratch_sprint_dir"] = "../../../../escaped_sprint"
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 2
    assert "single relative path component" in capsys.readouterr().err
    assert not (tmp_path / "escaped_sprint").exists()


# --- Exemptions must be typed ---------------------------------------------


def test_untyped_exception_reason_is_refused(tmp_path: Path, module, capsys) -> None:
    root = _root(tmp_path, "# Spec\n")
    (root / "docs" / "standards" / "templates" / "ORPHAN_TEMPLATE.md").write_text("x", encoding="utf-8")
    spec = _spec(root)
    spec["exceptions"] = [{"template": "ORPHAN_TEMPLATE.md", "reason": "because"}]
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 2
    assert "is not one of" in capsys.readouterr().err


def test_declared_reason_set_must_match_the_enforced_one(tmp_path: Path, module, capsys) -> None:
    """Two sources of truth for the same set is the defect this sprint closes."""
    root = _root(tmp_path, "# Spec\n")
    spec = _spec(root)
    spec["_valid_exception_reasons"] = ["no-automated-gate"]
    _write_spec(root, spec)
    assert module.check(root, module.CONFIG) == 2
    assert "disagrees with" in capsys.readouterr().err


def test_real_declaration_mirrors_the_enforced_reason_set(module) -> None:
    spec = module.load_config(REPO, module.CONFIG)
    assert set(spec["_valid_exception_reasons"]) == set(module.VALID_EXCEPTION_REASONS)


# --- A recorded non-pairing is held to the same standard ------------------


def _with_gate_exception(root: Path, entry: dict) -> None:
    spec = _spec(root)
    spec["gate_exceptions"] = [entry]
    _write_spec(root, spec)


def test_gate_exception_naming_an_absent_check_is_refused(
    tmp_path: Path, module, capsys
) -> None:
    """Measured by Gate 2: this whole array passed unread.

    An entry naming a non-existent check, a non-existent template and an invented
    reason exited 0 with `[OK]` printed, while the sibling `exceptions` array had
    three guards against exactly that staleness.
    """
    root = _root(tmp_path, "# Spec\n")
    _with_gate_exception(
        root,
        {"gate": "scripts/absent.py", "template": "SPEC_TEMPLATE.md", "reason": "phase-mismatch"},
    )
    assert module.check(root, module.CONFIG) == 2
    assert "check that does not exist" in capsys.readouterr().err


def test_gate_exception_naming_an_absent_template_is_refused(
    tmp_path: Path, module, capsys
) -> None:
    root = _root(tmp_path, "# Spec\n")
    _with_gate_exception(
        root,
        {"gate": "scripts/fake_gate.py", "template": "GONE_TEMPLATE.md", "reason": "phase-mismatch"},
    )
    assert module.check(root, module.CONFIG) == 2
    assert "template that does not exist" in capsys.readouterr().err


def test_gate_exception_reason_must_be_typed(tmp_path: Path, module, capsys) -> None:
    root = _root(tmp_path, "# Spec\n")
    _with_gate_exception(
        root,
        {"gate": "scripts/fake_gate.py", "template": "SPEC_TEMPLATE.md", "reason": "made-up"},
    )
    assert module.check(root, module.CONFIG) == 2
    assert "is not typed" in capsys.readouterr().err


def test_valid_gate_exception_passes(tmp_path: Path, module) -> None:
    root = _root(tmp_path, "# Spec\n")
    _with_gate_exception(
        root,
        {"gate": "scripts/fake_gate.py", "template": "SPEC_TEMPLATE.md", "reason": "phase-mismatch"},
    )
    assert module.check(root, module.CONFIG) == 0


def test_shipped_gate_exceptions_resolve(module) -> None:
    """The real declaration's recorded non-pairing points at things that exist."""
    spec = module.load_config(REPO, module.CONFIG)
    assert spec["gate_exceptions"]
    assert module.check_gate_exceptions(REPO, spec) == []


# --- Editor droppings are not templates -----------------------------------


def test_dotfiles_are_not_counted_as_templates(tmp_path: Path, module) -> None:
    """A .DS_Store in the templates directory must not fail the build."""
    root = _root(tmp_path, "# Spec\n")
    (root / "docs" / "standards" / "templates" / ".DS_Store").write_text("", encoding="utf-8")
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
