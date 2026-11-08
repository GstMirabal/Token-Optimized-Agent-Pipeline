"""Family test for silent skips: no ``--current-sprint`` script exits 0 on a broken target.

Plan D37 M-05 (Sprint 059). The scripts are found by searching for an
``add_argument("--current-sprint"`` call, so a new script joins the matrix
without anyone listing it. Each runs against fixtures, every one of which
names a sprint that cannot be audited. An exit 0 is a silent pass. An argparse
usage error is also a failure, because it means the script's arguments for a
case are not mapped below.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
FLAG = re.compile(r"add_argument\(\s*[\"']--current-sprint[\"']")
SUBCOMMAND = {"loop_guard.py": ["check"]}
TYPO_DIR = "docs/sprints/059-typo"
MISSING_PATH_ARGS = {"audit_plan.py": [f"{TYPO_DIR}/IMPLEMENTATION_PLAN.md"]}
LOOP = {"iteration": 0, "max_iterations": 5, "success_condition": "tests pass"}
SPRINT = "docs/sprints/059-core-x"
BAD_LOG = (
    "| Gate | Round | Verdict | Class | Notes |\n| :--- | :--- | :--- | :--- | :--- |\n"
    "| QA Agent (Gate 1) | 1 | MAYBE | charter | x |\n"
)


def _scripts() -> list[Path]:
    """Every script under ``scripts/`` and ``skills/*/scripts/`` declaring the flag."""
    candidates = [*REPO.glob("scripts/*.py"), *REPO.glob("skills/*/scripts/*.py")]
    return sorted(p for p in candidates if FLAG.search(p.read_text(encoding="utf-8")))


def _fixture(root: Path, anchor: str, with_dir: bool) -> Path:
    """A repository whose anchor text is ``anchor``; ``with_dir`` adds a failing sprint."""
    (root / ".git").mkdir()
    (root / "docs" / "sprints").mkdir(parents=True)
    (root / "docs" / "active_state.json").write_text(anchor, encoding="utf-8")
    if with_dir:
        sprint = root / SPRINT
        sprint.mkdir()
        (sprint / "IMPLEMENTATION_PLAN.md").write_text("# empty plan\n", encoding="utf-8")
        (sprint / "SPRINT_LOG.md").write_text(BAD_LOG, encoding="utf-8")
    return root


def _anchor(sprint_id: object) -> str:
    return json.dumps({"current_sprint": {"id": sprint_id, "path": SPRINT}, "loop": LOOP})


CASES = {
    "subdirectory": (_anchor("059"), False, "docs", None),
    "string_id": (_anchor("059"), True, "", None),
    "deleted_directory": (_anchor(59), False, "", None),
    "truncated_anchor": ('{"current_sprint": {"id": 59', False, "", None),
    "missing_path": (_anchor(59), True, "", "missing"),
    "numbered_parent": (_anchor(59), True, "", None),
}


def test_the_search_finds_the_known_scripts() -> None:
    names = {p.name for p in _scripts()}
    assert {"check_task_scope.py", "check_gate_log.py", "audit_plan.py", "loop_guard.py"} <= names


@pytest.mark.parametrize("case", sorted(CASES))
@pytest.mark.parametrize("script", _scripts(), ids=lambda p: p.name)
def test_no_script_exits_0_on_a_broken_target(tmp_path: Path, script: Path, case: str) -> None:
    anchor, with_dir, subdir, mode = CASES[case]
    if case == "numbered_parent":
        tmp_path = tmp_path / "005-dir" / "repo"
        tmp_path.mkdir(parents=True)
    root = _fixture(tmp_path, anchor, with_dir)
    if mode == "missing":
        tail = MISSING_PATH_ARGS.get(script.name, ["--sprint-dir", TYPO_DIR])
    else:
        tail = ["--current-sprint"]
    argv = [sys.executable, str(script), *SUBCOMMAND.get(script.name, []), *tail]
    result = subprocess.run(
        argv, cwd=root / subdir, capture_output=True, text=True, check=False
    )
    assert "usage:" not in result.stderr, result.stderr
    assert result.returncode != 0, result.stdout
