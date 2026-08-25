"""Tests for scripts/check_task_scope.py.

A gate proven only on a healthy tree proves nothing — fixtures must fail.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHECK = REPO / "scripts" / "check_task_scope.py"


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), *args],
        cwd=cwd or REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _scope(tmp_path: Path, body: str) -> Path:
    sprint = tmp_path / "docs" / "sprints" / "030-core-pipeline"
    sprint.mkdir(parents=True)
    path = sprint / "task_scope.md"
    path.write_text(body, encoding="utf-8")
    return sprint


SHAPE = "# | File | Operation | Risk | Assignee | Model | Effort | Status"

OLD = """# Task Scope

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | high | `devops_agent` | ⏳ |
"""

CURSOR_NO_MODEL = f"""# Task Scope

**Mode.** Cursor `delegation_mode: sequential`.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | high | `devops_agent` | | | ⏳ |
"""

# Header claims Model/Effort but the table omits them.
MISSING_COLUMNS = """# Task Scope

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Mode.** Cursor `delegation_mode: sequential`.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | high | `devops_agent` | ⏳ |
"""

MECHANICAL_HIGH = f"""# Task Scope

**Mode.** Cursor.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | high | `devops_agent` | `composer-2.5` | N/A | ⏳ |
"""

ESCALATED = f"""# Task Scope

**Mode.** Cursor.

| {SHAPE} |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| X | `a.py` | modify | high | `devops_agent` — escalated | `grok-4.6` | `high` | ⏳ |
"""


def test_historical_024_is_skipped() -> None:
    """Sprints before Model/Effort columns must not fail the close."""
    result = _run("--sprint-dir", "docs/sprints/024-core-pipeline")
    assert result.returncode == 0, result.stderr


def test_cursor_scope_without_model_columns_fails(tmp_path: Path) -> None:
    sprint = _scope(tmp_path, MISSING_COLUMNS)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "Model" in result.stderr or "Effort" in result.stderr


def test_mechanical_high_without_keep_or_escalation_fails(tmp_path: Path) -> None:
    sprint = _scope(tmp_path, MECHANICAL_HIGH)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 2
    assert "mechanical" in result.stderr.lower() or "escalat" in result.stderr.lower()


def test_escalated_mechanical_high_passes(tmp_path: Path) -> None:
    sprint = _scope(tmp_path, ESCALATED)
    result = _run("--sprint-dir", str(sprint))
    assert result.returncode == 0, result.stderr


def test_current_sprint_skips_when_anchor_absent(tmp_path: Path) -> None:
    result = _run("--current-sprint", cwd=tmp_path)
    assert result.returncode == 0
