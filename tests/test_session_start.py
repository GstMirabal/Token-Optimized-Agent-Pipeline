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
    monkeypatch.setattr(session_start, "is_nucleus", lambda: True)
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
            "### - [ ] `F-999` — a fixture finding",
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
    assert "open entries (### - [ ]): 1" in text
    assert marker not in text


def test_upstream_open_entries_counts_the_canonical_marker(
    session_start, tmp_path: Path
) -> None:
    """S052-3: count `### - [ ]` headings, not `| **Still open**` table rows.

    Fixture: 6 open (`### - [ ]`) entries and one `| **Still open**` row that
    names all six in a single cell (Sprint 051's shape) → briefing must
    report `6`, not `1`. Fails against the pre-fix Still-open-row counter.
    """
    body = (
        "**Status at Sprint 051 (2026-09-23).**\n"
        "\n"
        "| | |\n"
        "| :--- | :--- |\n"
        "| **Still open** | Six, each with its own entry below: "
        "F-1, F-2, F-3, F-4, F-5, F-6 |\n"
        "\n"
        "### - [ ] `F-1` — open finding one\n"
        "### - [ ] `F-2` — open finding two\n"
        "### - [ ] `F-3` — open finding three\n"
        "### - [ ] `F-4` — open finding four\n"
        "### - [ ] `F-5` — open finding five\n"
        "### - [ ] `F-6` — open finding six"
    )
    root = _write_minimal_root(tmp_path / "repo", upstream_body=body)
    section = "\n".join(session_start.section_upstream(root))
    assert "open entries (### - [ ]): 6" in section


def test_upstream_open_entries_excludes_closed_markers(
    session_start, tmp_path: Path
) -> None:
    """`### - [x]` (closed) entries must not inflate the open count."""
    body = (
        "### - [ ] `F-1` — open finding\n"
        "### - [x] `F-2` — closed finding\n"
        "### - [x] `F-3` — closed finding"
    )
    root = _write_minimal_root(tmp_path / "repo", upstream_body=body)
    section = "\n".join(session_start.section_upstream(root))
    assert "open entries (### - [ ]): 1" in section


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

    def mock_run_script(
        root_path: Path, relative: str, *args: str, **kwargs: object
    ) -> int:
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

    def mock_run_script(
        root_path: Path, relative: str, *args: str, **kwargs: object
    ) -> int:
        calls.append((relative, args))
        return 0

    monkeypatch.setattr(session_start, "_run_script", mock_run_script)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: False)
    monkeypatch.setattr(session_start, "_commands_body_stale", lambda *a, **k: False)

    assert session_start.main(["--boot", "--tool", "cursor"]) == 0
    assert (
        "scripts/session_state.py",
        ("claim", "--tool", "cursor", "--entry-point", "boot"),
    ) in calls


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


def test_bridge_permission_denied_recognizes_claude_mirror(session_start) -> None:
    """F-BOOT-1: a raw PermissionError naming .claude is a permission denial.

    Fails against the pre-Sprint-044 tree, where the predicate took no target
    and matched `.cursor` alone: a denied `claude`-target install then fell
    through to the hard-stop branch.
    """
    denied = (
        "PermissionError: [Errno 13] Permission denied: "
        "'/host/.claude/settings.json'"
    )
    assert session_start._bridge_permission_denied(denied, "claude") is True
    # The rendered line shape is recognised too.
    rendered = "bridge: permission denied on .claude (Errno 13)"
    assert session_start._bridge_permission_denied(rendered, "claude") is True
    # Marker isolation: a .cursor denial is not this target's, and an unknown
    # target never reports a denial.
    cursor_denied = "PermissionError: ... '/host/.cursor/mcp.json'"
    assert session_start._bridge_permission_denied(cursor_denied, "claude") is False
    assert session_start._bridge_permission_denied(denied, "terminal") is False
    # A non-permission failure is still not a denial.
    assert session_start._bridge_permission_denied("some other failure", "claude") is False


def test_boot_claude_permission_error_is_advisory(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    """F-BOOT-1: a sandbox-denied `.claude` install is advisory, exit 0.

    Against the pre-Sprint-044 tree this exits 2 (`_bridge_permission_denied`
    returned False for the `.claude` string), so the host session was never
    claimed.
    """
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    monkeypatch.setattr(session_start, "_lock_stale", lambda *a, **k: True)
    monkeypatch.setattr(session_start, "_commands_body_stale", lambda *a, **k: True)

    def mock_install(root_path: Path, target: str) -> tuple[int, str]:
        return 1, (
            "PermissionError: [Errno 13] Permission denied: "
            "'/host/.claude/settings.json'"
        )

    monkeypatch.setattr(session_start, "_run_bridge_install", mock_install)
    assert session_start.main(["--boot", "--tool", "claude-code"]) == 0
    combined = capsys.readouterr()
    out = combined.out + combined.err
    assert "claude" in out and ("agent sandbox" in out or "PermissionError" in out)


def test_anchor_cwd_is_the_host_root_in_submodule_mode(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """F-BOOT-2: submodule mode → the anchor lives one level above .agents/."""
    root = tmp_path / "host" / ".agents"
    monkeypatch.setattr(session_start, "is_nucleus", lambda: False)
    assert session_start._anchor_cwd(root) == root.parent
    monkeypatch.setattr(session_start, "is_nucleus", lambda: True)
    assert session_start._anchor_cwd(root) == root


def test_boot_runs_claim_and_probe_from_the_host_root_in_submodule_mode(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """F-BOOT-2 / D8: claim, probe and drift resolve their paths against the host.

    Against the pre-Sprint-044 tree every sub-script ran with cwd = the .agents
    checkout, so `session_state.py claim` wrote the gitignored nucleus anchor and
    the host session was never claimed. Sprint 047 (D8) extends the same scoping
    to detect_drift.py, so it measures drift against the host's git history. Only
    sync_agents_pin stays at the framework checkout — it pins the .agents
    submodule.
    """
    root = _write_minimal_root(tmp_path / "host" / ".agents")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "is_nucleus", lambda: False)
    monkeypatch.setattr(session_start, "_bridge_triage", lambda *a, **k: (0, []))
    seen: dict[str, Path | None] = {}

    def mock_run_script(
        root_path: Path, relative: str, *args: str, cwd: Path | None = None
    ) -> int:
        seen[relative] = cwd
        return 0

    monkeypatch.setattr(session_start, "_run_script", mock_run_script)
    assert session_start.main(["--boot", "--tool", "claude-code"]) == 0
    assert seen["scripts/session_state.py"] == root.parent
    assert seen["scripts/session_probe.py"] == root.parent
    assert seen["scripts/detect_drift.py"] == root.parent  # D8: host-scoped
    assert seen["scripts/detect_drift.py"] == seen["scripts/session_state.py"]
    assert seen["scripts/sync_agents_pin.py"] is None  # framework-scoped (pins .agents)


def test_boot_keeps_claim_at_root_in_nucleus_mode(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """F-BOOT-2 regression guard: nucleus mode is unchanged (this session's path)."""
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "is_nucleus", lambda: True)
    monkeypatch.setattr(session_start, "_bridge_triage", lambda *a, **k: (0, []))
    seen: dict[str, Path | None] = {}

    def mock_run_script(
        root_path: Path, relative: str, *args: str, cwd: Path | None = None
    ) -> int:
        seen[relative] = cwd
        return 0

    monkeypatch.setattr(session_start, "_run_script", mock_run_script)
    assert session_start.main(["--boot", "--tool", "claude-code"]) == 0
    # nucleus: _anchor_cwd returns root itself, passed explicitly.
    assert seen["scripts/session_state.py"] == root
    assert seen["scripts/session_probe.py"] == root
    # D8: drift stays framework-scoped when is_nucleus() is True.
    assert seen["scripts/detect_drift.py"] == root


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
        lambda root_path, relative, *args, **kwargs: calls.append(
            (relative, args)
        )
        or 0,
    )

    assert session_start.main(["--boot"]) == 0
    assert (
        "scripts/session_state.py",
        ("claim", "--tool", "terminal", "--entry-point", "boot"),
    ) in calls


def test_claim_args_defaults_omit_only_session_id_and_takeover(
    session_start,
) -> None:
    """S052-1/S052-2 (D10): omitting --session-id/--takeover leaves the rest
    of the boot claim invocation unchanged; --entry-point boot is always
    forwarded from the boot path so the refusal message names --boot
    (`session_state.py` `retry_hint`).
    """
    assert session_start._claim_args("cursor", None, False) == [
        "claim", "--tool", "cursor", "--entry-point", "boot",
    ]


def test_repeat_boot_with_same_session_id_reclaims_instead_of_refusing(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """S052-1: --boot must forward --session-id, so a second boot in the same
    session re-claims (exit 0) instead of minting a fresh UID and refusing
    itself against its own prior claim.
    """
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    holder: dict[str, str | None] = {"session_id": None}
    seen_session_ids: list[str | None] = []

    def mock_run_script(
        root_path: Path, relative: str, *args: str, cwd: Path | None = None
    ) -> int:
        if relative != "scripts/session_state.py":
            return 0
        session_id = (
            args[args.index("--session-id") + 1]
            if "--session-id" in args
            else None
        )
        seen_session_ids.append(session_id)
        if holder["session_id"] in (None, session_id):
            holder["session_id"] = session_id
            return 0
        return 2

    monkeypatch.setattr(session_start, "_run_script", mock_run_script)
    assert session_start.main(["--boot", "--session-id", "SAME-UID"]) == 0
    assert session_start.main(["--boot", "--session-id", "SAME-UID"]) == 0
    assert seen_session_ids == ["SAME-UID", "SAME-UID"]


def test_boot_takeover_flag_parses_and_forwards_to_claim(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """S052-2: session_start.py must accept --takeover (the flag the claim
    refusal message recommends) and forward it to `session_state.py claim`.
    """
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    calls: list[tuple[str, tuple[str, ...]]] = []
    monkeypatch.setattr(
        session_start,
        "_run_script",
        lambda root_path, relative, *args, **kwargs: calls.append(
            (relative, args)
        )
        or 0,
    )

    assert session_start.main(["--boot", "--takeover"]) == 0
    assert (
        "scripts/session_state.py",
        ("claim", "--tool", "terminal", "--entry-point", "boot", "--takeover"),
    ) in calls


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
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A briefing-only run reads session_tool rather than guessing."""
    root = _write_minimal_root(tmp_path / "repo")  # anchor says cursor
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "is_nucleus", lambda: True)
    assert "Chat vs map (Cursor tiers)" in "\n".join(session_start.build_briefing(root))


def test_anchor_root_is_repo_root_in_nucleus_mode(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """D8: nucleus mode anchors the briefing read on the framework checkout."""
    root = tmp_path / "repo"
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "is_nucleus", lambda: True)
    assert session_start.anchor_root() == root


def test_anchor_root_is_the_host_root_in_submodule_mode(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """D8: submodule mode anchors one level above the .agents checkout."""
    root = tmp_path / "host" / ".agents"
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "is_nucleus", lambda: False)
    assert session_start.anchor_root() == root.parent


def test_briefing_reads_the_host_anchor_in_submodule_mode(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """D8: a host briefing reports ``<host>/docs/active_state.json``, not the copy.

    Fails against HEAD: there ``build_briefing`` calls ``load_anchor(root)`` with
    no ``anchor_root()`` seam, so it reports the framework-side anchor at
    ``root/docs/active_state.json`` — ``HOST-ANCHOR-SENTINEL`` never appears and
    ``test-sess-035`` does.
    """
    agents_root = _write_minimal_root(tmp_path / "host" / ".agents")
    host_docs = agents_root.parent / "docs"
    host_docs.mkdir(parents=True)
    (host_docs / "active_state.json").write_text(
        json.dumps(
            {
                "status": "IN_PROGRESS",
                "session_id": "HOST-ANCHOR-SENTINEL",
                "current_sprint": {"id": 47, "layer": "core", "app": "pipeline"},
                "session_tool": "claude-code",
                "delegation_mode": "native",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(session_start, "repo_root", lambda: agents_root)
    monkeypatch.setattr(session_start, "is_nucleus", lambda: False)

    briefing = "\n".join(session_start.build_briefing(agents_root))

    assert "HOST-ANCHOR-SENTINEL" in briefing
    assert "test-sess-035" not in briefing


def test_section_drift_spawns_detect_drift_from_the_anchor_cwd(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """D8: the briefing-only drift probe runs detect_drift.py at the anchor cwd.

    ``section_drift`` spawns ``scripts/detect_drift.py`` with cwd at
    ``_anchor_cwd(root)`` — the host root one level above ``.agents`` in
    submodule mode, the framework checkout in nucleus mode. The submodule case
    fails against HEAD, where ``section_drift`` passed ``cwd=str(root)`` and so
    measured drift against the framework's git history.
    """
    root = tmp_path / "host" / ".agents"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "detect_drift.py").write_text("", encoding="utf-8")
    seen: dict[str, str | None] = {}

    def mock_run(
        *args: object, cwd: str | None = None, **kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        seen["cwd"] = cwd
        return subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )

    monkeypatch.setattr(session_start.subprocess, "run", mock_run)
    monkeypatch.setattr(session_start, "repo_root", lambda: root)

    monkeypatch.setattr(session_start, "is_nucleus", lambda: False)
    session_start.section_drift(root)
    assert seen["cwd"] == str(root.parent)

    monkeypatch.setattr(session_start, "is_nucleus", lambda: True)
    session_start.section_drift(root)
    assert seen["cwd"] == str(root)


def _boot_with_install_lock(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, lock_rc: int
) -> tuple[int, str]:
    root = _write_minimal_root(tmp_path / "repo")
    monkeypatch.setattr(session_start, "repo_root", lambda: root)
    monkeypatch.setattr(session_start, "_run_script", lambda *a, **k: 0)
    monkeypatch.setattr(session_start, "_run_install_lock", lambda r: lock_rc)
    rc = session_start.main(["--boot", "--tool", "terminal"])
    return rc, ""


def test_boot_stale_install_lock_is_advisory_and_keeps_exit_code(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    """B05 (D12): a stale installed.lock adds a finding, never a hard stop."""
    rc, _ = _boot_with_install_lock(session_start, monkeypatch, tmp_path, 2)
    out = capsys.readouterr().out
    assert rc == 0
    assert "install_lock.py write" in out
    assert "pip install -r requirements-core.txt" in out


def test_boot_matching_install_lock_adds_no_advisory(
    session_start, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys
) -> None:
    rc, _ = _boot_with_install_lock(session_start, monkeypatch, tmp_path, 0)
    out = capsys.readouterr().out
    assert rc == 0
    assert "install_lock" not in out
