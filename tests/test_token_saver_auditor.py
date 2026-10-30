"""Tests for skills/token-saver-auditor/scripts/audit_plan.py.

Every case asserts the auditor FAILS where it must. A gate proven only on a
healthy tree proves nothing.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDIT = REPO / "skills" / "token-saver-auditor" / "scripts" / "audit_plan.py"


def _run(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(AUDIT), str(path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _plan(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "IMPLEMENTATION_PLAN.md"
    path.write_text(body, encoding="utf-8")
    return path


MECHANISMS = """
## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| example | script | Makefile verify |
"""

COST = """
## Cost

| Field | Value |
| :--- | :--- |
| Work units | 1 |
"""


def test_audit_plan_script_exists() -> None:
    """The auditor must be a real script, not an empty scripts/ stub."""
    assert AUDIT.is_file()


def test_029_plan_fails_without_cost_section() -> None:
    """Sprint 029 plans predate the Cost section — that is the defect."""
    target = REPO / "docs" / "sprints" / "029-core-pipeline" / "IMPLEMENTATION_PLAN.md"
    result = _run(target)
    assert result.returncode == 2
    assert "Cost" in result.stderr


def test_clean_plan_passes(tmp_path: Path) -> None:
    body = "# Plan\n" + MECHANISMS + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 0, result.stderr


def test_review_the_whole_system_is_rejected(tmp_path: Path) -> None:
    body = "# Plan\nreview the whole system\n" + MECHANISMS + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 2
    assert "whole system" in result.stderr.lower()


def test_raw_json_dump_is_rejected(tmp_path: Path) -> None:
    body = "# Plan\nraw JSON dump into the chat\n" + MECHANISMS + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 2
    assert "JSON" in result.stderr or "CSV" in result.stderr


def test_loop_without_guard_is_rejected(tmp_path: Path) -> None:
    body = "# Plan\nWrap phases in `/loop`.\n" + MECHANISMS + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 2
    assert "loop_guard" in result.stderr


def test_mechanisms_without_invoker_column_is_rejected(tmp_path: Path) -> None:
    body = "# Plan\n## Mechanisms\n\n| Mechanism | Kind |\n| :--- | :--- |\n| x | script |\n" + COST
    result = _run(_plan(tmp_path, body))
    assert result.returncode == 2
    assert "Invoker" in result.stderr


def test_missing_mechanisms_section_is_rejected(tmp_path: Path) -> None:
    result = _run(_plan(tmp_path, "# Plan\n" + COST))
    assert result.returncode == 2
    assert "Mechanisms" in result.stderr


def test_current_sprint_skips_when_anchor_absent(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(AUDIT), "--current-sprint"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0


# --- Sprint 054 D6/D7: measured plan checks, header-gated -----------------

TEMPLATE = REPO / "docs" / "standards" / "templates" / "IMPLEMENTATION_PLAN_TEMPLATE.md"
BASE_PLAN = "# Plan\n" + MECHANISMS + COST


def _verification(rows: str, header: str = "| Command | Expected | Dry run | Positive control |") -> str:
    sep = "| :--- | :--- | :--- | :--- |"
    return f"\n## Verification\n\n{header}\n{sep}\n{rows}\n"


def _tests(rows: str, header: str = "| Check | Fails against the current tree? | Observed at base |") -> str:
    return f"\n## Tests\n\n{header}\n| :--- | :--- | :--- |\n{rows}\n"


def test_escaped_pipe_in_backticked_command_is_rejected(tmp_path: Path) -> None:
    rows = '| `rg "a\\|b" x` | output | exit `0` | — |'
    result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows)))
    assert result.returncode == 2
    assert "escaped pipe" in result.stderr


def test_bare_escaped_pipe_mention_is_not_a_command(tmp_path: Path) -> None:
    rows = "| `ls` | an escaped `\\|` is a mention | exit `0` | — |"
    result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows)))
    assert result.returncode == 0, result.stderr


def test_no_output_without_positive_control_is_rejected(tmp_path: Path) -> None:
    for control in ("", "—", "-"):
        rows = f"| `rg x y` | no output | exit `1` | {control} |"
        result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows)))
        assert result.returncode == 2, control
        assert "Positive control" in result.stderr


def test_zero_hits_without_positive_control_is_rejected(tmp_path: Path) -> None:
    rows = "| `rg x y` | `0` hits | exit `1` | — |"
    result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows)))
    assert result.returncode == 2
    assert "Positive control" in result.stderr


def test_no_output_with_positive_control_passes(tmp_path: Path) -> None:
    rows = "| `rg x y` | No output | exit `1` | `rg x z` printed a hit |"
    result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows)))
    assert result.returncode == 0, result.stderr


def test_exit_code_zero_with_echo_is_not_a_no_output_claim(tmp_path: Path) -> None:
    rows = "| `make verify; echo $?` | `0` | exit `0` | — |"
    result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows)))
    assert result.returncode == 0, result.stderr


def test_empty_dry_run_is_rejected(tmp_path: Path) -> None:
    rows = "| `ls` | exit `0` |  | — |"
    result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows)))
    assert result.returncode == 2
    assert "Dry run" in result.stderr


def test_dry_run_header_is_matched_by_prefix(tmp_path: Path) -> None:
    header = "| Command | Expected | Dry run at `d848302` | Positive control |"
    rows = "| `ls` | exit `0` |  | — |"
    result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows, header)))
    assert result.returncode == 2
    assert "Dry run" in result.stderr


def test_yes_row_without_observed_at_base_is_rejected(tmp_path: Path) -> None:
    rows = "| a check | **Yes** — the defect |  |"
    result = _run(_plan(tmp_path, BASE_PLAN + _tests(rows)))
    assert result.returncode == 2
    assert "Observed at base" in result.stderr


def test_yes_row_with_observed_at_base_passes(tmp_path: Path) -> None:
    rows = "| a check | **Yes** — the defect | exit `0` at base |\n| b | **No** — protect |  |"
    result = _run(_plan(tmp_path, BASE_PLAN + _tests(rows)))
    assert result.returncode == 0, result.stderr


def test_old_shape_plan_is_not_checked_for_new_columns(tmp_path: Path) -> None:
    ver = "\n## Verification\n\n| Command | Expected |\n| :--- | :--- |\n| `rg x y` | no output |\n"
    tests = "\n## Tests\n\n| Check | Fails against the current tree? |\n| :--- | :--- |\n| c | **Yes** |\n"
    result = _run(_plan(tmp_path, BASE_PLAN + ver + tests))
    assert result.returncode == 0, result.stderr


def test_pipe_inside_backticks_does_not_split_a_cell(tmp_path: Path) -> None:
    rows = "| `rg -e a \\| b` | no output | exit `1` | control fired |"
    result = _run(_plan(tmp_path, BASE_PLAN + _verification(rows)))
    assert "Positive control" not in result.stderr
    assert "Dry run" not in result.stderr


def test_filled_template_passes(tmp_path: Path) -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    filled = re.sub(r"\{\{[A-Z_]+\}\}", "`value`", text)
    result = _run(_plan(tmp_path, filled))
    assert "Dry run" not in result.stderr
    assert "Observed at base" not in result.stderr
    assert "Positive control" not in result.stderr
    assert "escaped pipe" not in result.stderr


def test_sprint_054_plan_passes_the_new_checks() -> None:
    target = REPO / "docs" / "sprints" / "054-core-pipeline" / "IMPLEMENTATION_PLAN.md"
    result = _run(target)
    # The 054 plan predates R-5 (Sprint 058); only that rule may flag it.
    findings = [ln for ln in result.stderr.splitlines() if ln.lstrip().startswith("•")]
    assert all("R-5" in ln for ln in findings), result.stderr


# --- R-5 blast radius (Sprint 058, B-08) ---------------------------------

SUITE = "venv_skillopt/bin/python -m pytest -q -p no:cacheprovider"
SHARED = "scripts/_root.py"


def _blast_plan(tmp_path: Path, file_cell: str, command: str) -> Path:
    body = (
        MECHANISMS
        + "\n## Cost\n\nx\n"
        + f"\n## Work\n\n| # | File | Operation |\n| :--- | :--- | :--- |\n| A-1 | {file_cell} | modify |\n"
        + "\n## Verification\n\n| Command | Expected | Dry run | Positive control |\n"
        + "| :--- | :--- | :--- | :--- |\n"
        + f"| {command} | exit `0` | exit `0` | n/a |\n"
    )
    return _plan(tmp_path, body)


def _run_in(path: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(AUDIT), str(path)], cwd=cwd, capture_output=True, text=True, check=False
    )


def test_shared_file_with_full_suite_row_passes(tmp_path: Path) -> None:
    result = _run(_blast_plan(tmp_path, f"`{SHARED}`", f"`{SUITE}` (full suite)"))
    assert "R-5" not in result.stderr


def test_shared_file_without_full_suite_row_exits_2(tmp_path: Path) -> None:
    result = _run(_blast_plan(tmp_path, f"`{SHARED}`", "`make verify`"))
    assert result.returncode == 2
    assert "R-5" in result.stderr


def test_unshared_file_needs_no_full_suite_row(tmp_path: Path) -> None:
    result = _run(_blast_plan(tmp_path, "`docs/foo.md`", "`make verify`"))
    assert "R-5" not in result.stderr


def test_host_override_replaces_nucleus_list(tmp_path: Path) -> None:
    host = tmp_path / "host"
    host.mkdir()
    (host / ".agents-blast-radius.json").write_text(
        json.dumps({"full_suite_command": "make test", "shared_globs": ["app/*.py"]}), encoding="utf-8"
    )
    plan = _blast_plan(tmp_path, f"`{SHARED}`", "`make verify`")
    assert "R-5" not in _run_in(plan, host).stderr  # nucleus glob no longer applies
    plan = _blast_plan(tmp_path, "`app/core.py`", "`make verify`")
    assert _run_in(plan, host).returncode == 2


def test_malformed_list_exits_2(tmp_path: Path) -> None:
    host = tmp_path / "host"
    host.mkdir()
    plan = _blast_plan(tmp_path, "`docs/foo.md`", "`make verify`")
    for content in ("{not json", json.dumps({"shared_globs": []})):
        (host / ".agents-blast-radius.json").write_text(content, encoding="utf-8")
        result = _run_in(plan, host)
        assert result.returncode == 2
        assert "malformed" in result.stderr


def test_missing_list_skips_with_note(tmp_path: Path) -> None:
    sys.path.insert(0, str(AUDIT.parent))
    try:
        import audit_plan
    finally:
        sys.path.remove(str(AUDIT.parent))
    assert audit_plan.load_blast_radius(tmp_path, tmp_path / "absent.json") is None


def test_sprint_058_plan_exits_0() -> None:
    target = REPO / "docs" / "sprints" / "058-core-pipeline" / "IMPLEMENTATION_PLAN.md"
    result = _run(target)
    assert result.returncode == 0, result.stderr
