"""Tests for scripts/session_start.py briefing caps (Sprint 035 C4)."""

from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


@pytest.fixture()
def session_start(monkeypatch: pytest.MonkeyPatch):
    """Import session_start with scripts/ on sys.path."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("session_start", None)
    return importlib.import_module("session_start")


def _write_minimal_root(root: Path, *, upstream_body: str | None = None) -> Path:
    """Scaffold a fake repo root with anchor + optional UPSTREAM file."""
    docs = root / "docs"
    docs.mkdir(parents=True)
    (docs / "active_state.json").write_text(
        json.dumps(
            {
                "status": "IN_PROGRESS",
                "session_id": "test-sess-035",
                "current_sprint": {"id": 35, "layer": "core", "app": "pipeline"},
                "session_tool": "cursor",
                "delegation_mode": "sequential",
            }
        ),
        encoding="utf-8",
    )
    (root / "scripts").mkdir(exist_ok=True)
    (root / "config").mkdir(exist_ok=True)
    (root / "config" / "model_tiers.json").write_text(
        json.dumps({"tiers": {"author": {"cursor": {"model": "test-model"}}}}),
        encoding="utf-8",
    )
    if upstream_body is not None:
        audits = docs / "audits"
        audits.mkdir(parents=True)
        (audits / "UPSTREAM_FINDINGS_FROM_HOSTS.md").write_text(
            upstream_body, encoding="utf-8"
        )
    return root


def test_main_exits_zero_and_respects_line_cap(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    assert session_start.main([]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert len(lines) <= session_start.LINE_CAP
    assert lines[0] == "# /start briefing"
    assert "test-sess-035" in out


def test_upstream_section_reports_size_not_full_dump(
    session_start, tmp_path: Path
) -> None:
    marker = "UNIQUE_UPSTREAM_PAYLOAD_SHOULD_NOT_APPEAR"
    huge = "\n".join(
        [f"# dump line {i} {marker}" for i in range(500)]
        + [
            "**Status at Sprint 033 (test).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | F-999 |",
        ]
    )
    root = _write_minimal_root(tmp_path / "repo", upstream_body=huge)
    briefing = session_start.apply_line_cap(session_start.build_briefing(root))
    text = "\n".join(briefing)
    assert len(briefing) <= session_start.LINE_CAP
    assert "file lines:" in text
    assert "do not load full UPSTREAM" in text
    assert "rows (non-empty):" in text
    assert marker not in text
    assert text.count("| **Still open** |") <= 1


def test_upstream_still_open_uses_highest_sprint_status_only(
    session_start, tmp_path: Path
) -> None:
    """Sprint 038 M1: historical Status snapshots must not inflate the count.

    Fixture: Sprint 027 Still open non-empty + Sprint 033 *(none…)* → expect 0.
    Fails against the pre-M1 counter that summed every Still-open row.
    """
    body = "\n".join(
        [
            "**Status at Sprint 027 (2026-08-25).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | **`F-021-A2`**, **`F-026-A2`** |",
            "",
            "**Status at Sprint 033 (2026-08-25, `ai-sprint/033`).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | *(none in this file's open set)* |",
        ]
    )
    root = _write_minimal_root(tmp_path / "repo", upstream_body=body)
    section = "\n".join(session_start.section_upstream(root))
    assert "rows (non-empty): 0" in section


def test_upstream_still_open_counts_latest_nonempty_status(
    session_start, tmp_path: Path
) -> None:
    """When the highest Status sprint still lists opens, count that row only."""
    body = "\n".join(
        [
            "**Status at Sprint 027 (2026-08-25).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | **`F-021-A2`**, **`F-026-A2`** |",
            "",
            "**Status at Sprint 030 (2026-08-25).**",
            "",
            "| | |",
            "| :--- | :--- |",
            "| **Still open** | **`F-021-A2`** |",
        ]
    )
    root = _write_minimal_root(tmp_path / "repo", upstream_body=body)
    section = "\n".join(session_start.section_upstream(root))
    assert "rows (non-empty): 1" in section


def test_cli_against_real_repo_stays_under_line_cap() -> None:
    """Integration: real checkout still exits 0 and never dumps UPSTREAM path body."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "session_start.py")],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    lines = proc.stdout.splitlines()
    assert len(lines) <= 80
    assert "UPSTREAM_FINDINGS_FROM_HOSTS.md" in proc.stdout or "file lines:" in proc.stdout
    # Full dump would be hundreds of lines; cap already enforces this.
    assert "Framework-class findings under" not in proc.stdout


def test_boot_returns_2_on_drift_and_skips_claim(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    claim_called: list[tuple[str, tuple[str, ...]]] = []

    def mock_run_script(root_path: Path, relative: str, *args: str) -> int:
        if relative == "scripts/detect_drift.py":
            return 2
        if relative == "scripts/session_state.py" and args[:1] == ("claim",):
            claim_called.append((relative, args))
        return 0

    monkeypatch.setattr(session_start, "_run_script", mock_run_script)
    assert session_start.main(["--boot", "--tool", "cursor"]) == 2
    assert not claim_called


def test_boot_claims_when_drift_is_clean(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    calls: list[tuple[str, tuple[str, ...]]] = []

    def mock_run_script(root_path: Path, relative: str, *args: str) -> int:
        calls.append((relative, args))
        return 0

    monkeypatch.setattr(session_start, "_run_script", mock_run_script)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: False)
    monkeypatch.setattr(session_start, "_commands_body_stale", lambda *a, **k: False)

    assert session_start.main(["--boot", "--tool", "cursor"]) == 0
    assert ("scripts/session_state.py", ("claim", "--tool", "cursor")) in calls


def test_boot_lock_only_when_commands_fresh(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: True)
    monkeypatch.setattr(session_start, "_commands_body_stale", lambda *a, **k: False)
    install_calls: list[str] = []

    def mock_install(root_path: Path, target: str) -> tuple[int, str]:
        install_calls.append(target)
        return 1, "should not run"

    refresh_calls: list[str] = []

    def mock_refresh(root_path: Path, target: str) -> int:
        refresh_calls.append(target)
        return 0

    monkeypatch.setattr(session_start, "_run_bridge_install", mock_install)
    monkeypatch.setattr(session_start, "_refresh_bridge_lock", mock_refresh)
    assert session_start.main(["--boot", "--tool", "cursor"]) == 0
    assert not install_calls
    assert refresh_calls == ["cursor"]


def test_boot_permission_error_is_advisory(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: True)
    monkeypatch.setattr(session_start, "_commands_body_stale", lambda *a, **k: True)

    def mock_install(root_path: Path, target: str) -> tuple[int, str]:
        return 1, "PermissionError: bridge: permission denied on .cursor (x)"

    monkeypatch.setattr(session_start, "_run_bridge_install", mock_install)
    assert session_start.main(["--boot", "--tool", "cursor"]) == 0
    out = capsys.readouterr().out
    assert "PermissionError on `.cursor/`" in out or "agent sandbox" in out


def test_boot_generic_install_failure_still_exits_2(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: False)
    monkeypatch.setattr(session_start, "_commands_body_stale", lambda *a, **k: True)

    def mock_install(root_path: Path, target: str) -> tuple[int, str]:
        return 1, "some other install failure"

    monkeypatch.setattr(session_start, "_run_bridge_install", mock_install)
    assert session_start.main(["--boot", "--tool", "cursor"]) == 2


# ---------------------------------------------------------------------------
# Claude Code boot path (Sprint 041). Every case below fails against the tree
# before this sprint, where _commands_body_stale returned False for every
# target but cursor, so the claude path could only ever refresh the lock.
# ---------------------------------------------------------------------------


def test_boot_claude_installs_when_the_mirror_is_missing(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A wiped .claude/ reaches the install branch, not the lock-only branch.

    This is the defect: the boot printed 'content fresh' over a checkout with
    no mirror, exited 0, and never retried because the lock then matched HEAD.
    """
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: False)
    install_calls: list[str] = []
    refresh_calls: list[str] = []

    def mock_install(root_path: Path, target: str) -> tuple[int, str]:
        install_calls.append(target)
        return 0, ""

    monkeypatch.setattr(session_start, "_run_bridge_install", mock_install)
    monkeypatch.setattr(
        session_start,
        "_refresh_bridge_lock",
        lambda root_path, target: refresh_calls.append(target) or 0,
    )

    assert session_start.main(["--boot", "--tool", "claude-code"]) == 0
    assert install_calls == ["claude"]
    assert not refresh_calls


def test_boot_claude_is_lock_only_when_the_mirror_is_intact(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Triage (a) stays reachable for Claude: no needless reinstall."""
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: True)
    monkeypatch.setattr(session_start, "_commands_body_stale", lambda *a, **k: False)
    install_calls: list[str] = []
    refresh_calls: list[str] = []
    monkeypatch.setattr(
        session_start,
        "_run_bridge_install",
        lambda root_path, target: (install_calls.append(target), (1, "no"))[1],
    )
    monkeypatch.setattr(
        session_start,
        "_refresh_bridge_lock",
        lambda root_path, target: refresh_calls.append(target) or 0,
    )

    assert session_start.main(["--boot", "--tool", "claude-code"]) == 0
    assert not install_calls
    assert refresh_calls == ["claude"]


def test_boot_claude_never_touches_the_cursor_bridge(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The bi-harness guarantee: one boot repairs one target."""
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: True)
    monkeypatch.setattr(session_start, "_commands_body_stale", lambda *a, **k: True)
    targets: list[str] = []
    monkeypatch.setattr(
        session_start,
        "_run_bridge_install",
        lambda root_path, target: (targets.append(target), (0, ""))[1],
    )

    assert session_start.main(["--boot", "--tool", "claude-code"]) == 0
    assert targets == ["claude"]
    assert "cursor" not in targets


def test_boot_terminal_has_no_bridge_and_still_succeeds(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A terminal session claims the anchor but owns no mirror."""
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    targets: list[str] = []
    monkeypatch.setattr(
        session_start,
        "_run_bridge_install",
        lambda root_path, target: (targets.append(target), (0, ""))[1],
    )

    assert session_start.main(["--boot", "--tool", "terminal"]) == 0
    assert not targets


def test_tool_defaults_to_terminal_not_an_ide(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A bare --boot must not claim the anchor as an IDE nobody named."""
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    calls: list[tuple[str, tuple[str, ...]]] = []
    monkeypatch.setattr(
        session_start,
        "_run_script",
        lambda root_path, relative, *args: calls.append((relative, args)) or 0,
    )

    assert session_start.main(["--boot"]) == 0
    assert ("scripts/session_state.py", ("claim", "--tool", "terminal")) in calls


def test_cursor_tiers_section_is_for_cursor_sessions_only(
    session_start, tmp_path: Path
) -> None:
    """`make cursor-tiers` is a Cursor instrument, not briefing furniture."""
    root = _write_minimal_root(tmp_path / "repo")
    claude = "\n".join(session_start.build_briefing(root, "claude-code"))
    cursor = "\n".join(session_start.build_briefing(root, "cursor"))
    assert "Chat vs map (Cursor tiers)" not in claude
    assert "Chat vs map (Cursor tiers)" in cursor


def test_briefing_without_a_tool_falls_back_to_the_anchor(
    session_start, tmp_path: Path
) -> None:
    """A briefing-only run reads session_tool rather than guessing."""
    root = _write_minimal_root(tmp_path / "repo")  # anchor says cursor
    assert "Chat vs map (Cursor tiers)" in "\n".join(session_start.build_briefing(root))
