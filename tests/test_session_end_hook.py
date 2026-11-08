"""Tests for scripts/session_end_hook.py (Sprint 027 P3)."""

from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def test_hook_invokes_suspend_never_release(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("session_end_hook", None)
    hook = importlib.import_module("session_end_hook")
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], check: bool = False) -> object:
        calls.append(list(cmd))

        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr(hook.subprocess, "run", fake_run)
    assert hook.main() == 0
    assert len(calls) == 1
    assert "suspend" in calls[0]
    assert "release" not in calls[0]


def test_suspend_preserves_last_close_commit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Integration: suspend must not rewrite last_close_commit (Design §D4)."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs").mkdir()
    baseline = "abc123deadbeef00000000000000000000000000"
    (tmp_path / "docs" / "active_state.json").write_text(
        json.dumps(
            {
                "session_id": "s1",
                "status": "IN_PROGRESS",
                "last_close_commit": baseline,
                "session_count": 1,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(SCRIPTS))
    monkeypatch.syspath_prepend(str(REPO))
    sys.modules.pop("session_state", None)
    ss = importlib.import_module("session_state")
    monkeypatch.setattr(ss, "ACTIVE_STATE", Path("docs/active_state.json"))
    monkeypatch.setattr(ss, "mirror_active_state", lambda: None)
    assert ss.suspend() == 0
    after = json.loads(
        (tmp_path / "docs" / "active_state.json").read_text(encoding="utf-8")
    )
    assert after["status"] == "SUSPENDED"
    assert after["last_close_commit"] == baseline


def _run_hook(cwd: Path, stdin_text: str) -> subprocess.CompletedProcess[str]:
    """Run the real hook script in `cwd` with `stdin_text` as the SessionEnd payload."""
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "session_end_hook.py")],
        input=stdin_text,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def _anchor(root: Path, holder: str = "session-A") -> dict:
    (root / "docs").mkdir(exist_ok=True)
    state = {
        "session_id": holder,
        "status": "IN_PROGRESS",
        "current_sprint": {"id": 59, "status": "OPEN"},
    }
    (root / "docs" / "active_state.json").write_text(json.dumps(state), encoding="utf-8")
    return state


def _read_anchor(root: Path) -> dict:
    return json.loads((root / "docs" / "active_state.json").read_text(encoding="utf-8"))


def test_session_end_of_another_session_leaves_the_anchor_untouched(tmp_path: Path) -> None:
    """KI-057-2: the anchor holds session A, the payload names session B."""
    before = _anchor(tmp_path)
    result = _run_hook(tmp_path, json.dumps({"session_id": "session-B"}))
    assert result.returncode == 0
    assert _read_anchor(tmp_path) == before
    assert "session-B" in result.stdout and "session-A" in result.stdout


def test_session_end_of_the_holder_suspends(tmp_path: Path) -> None:
    _anchor(tmp_path)
    result = _run_hook(tmp_path, json.dumps({"session_id": "session-A"}))
    assert result.returncode == 0
    assert _read_anchor(tmp_path)["status"] == "SUSPENDED"


@pytest.mark.parametrize(
    "payload", ["", "not json", "[]", "{}", '{"session_id": ""}', '{"session_id": 7}']
)
def test_session_end_without_a_usable_id_suspends_nothing(
    tmp_path: Path, payload: str
) -> None:
    before = _anchor(tmp_path)
    result = _run_hook(tmp_path, payload)
    assert result.returncode == 0
    assert _read_anchor(tmp_path) == before
