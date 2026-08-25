"""Tests for scripts/session_end_hook.py (Sprint 027 P3)."""

from __future__ import annotations

import importlib
import json
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
    assert calls[0][-1] == "suspend"
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
