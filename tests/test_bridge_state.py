"""Tests for scripts/bridge_state.py — bridge integrity, per target (Sprint 041).

Every check here fails against the tree before Sprint 041, where the predicate
did not exist and the portable boot asked only whether the lock matched HEAD.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


@pytest.fixture()
def bridge_state(monkeypatch: pytest.MonkeyPatch):
    """Import bridge_state with scripts/ on sys.path."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    sys.modules.pop("bridge_state", None)
    return importlib.import_module("bridge_state")


def _sources(root: Path) -> None:
    """Scaffold the source trees a mirror is built from."""
    (root / "commands").mkdir(parents=True, exist_ok=True)
    (root / "commands" / "start.md").write_text("---\nx: 1\n---\nbody\n", encoding="utf-8")
    (root / "agents").mkdir(parents=True, exist_ok=True)
    (root / "agents" / "principal_agent.md").write_text("profile\n", encoding="utf-8")


def _claude_mirror(root: Path) -> None:
    """Scaffold a complete Claude mirror mapping every source file."""
    commands = root / ".claude" / "commands" / "agents"
    commands.mkdir(parents=True, exist_ok=True)
    (commands / "start.md").write_text("linked\n", encoding="utf-8")
    agents = root / ".claude" / "agents"
    agents.mkdir(parents=True, exist_ok=True)
    (agents / "principal_agent.md").write_text("linked\n", encoding="utf-8")


def _cursor_mirror(root: Path) -> None:
    """Scaffold the Cursor mirror directories."""
    (root / ".cursor" / "commands").mkdir(parents=True, exist_ok=True)
    (root / ".cursor" / "agents").mkdir(parents=True, exist_ok=True)


def test_claude_mirror_absent_is_stale(bridge_state, tmp_path: Path) -> None:
    """A checkout with no .claude/ at all needs an install, lock notwithstanding."""
    _sources(tmp_path)
    assert bridge_state.mirror_missing(tmp_path, "claude") is True
    assert bridge_state.bridge_stale(tmp_path, "claude", nucleus=True) is True


def test_claude_mirror_complete_is_fresh(bridge_state, tmp_path: Path) -> None:
    """A complete mirror is not stale — the lock-only triage stays reachable."""
    _sources(tmp_path)
    _claude_mirror(tmp_path)
    assert bridge_state.mirror_missing(tmp_path, "claude") is False
    assert bridge_state.bridge_stale(tmp_path, "claude", nucleus=True) is False


def test_claude_missing_one_command_is_stale(bridge_state, tmp_path: Path) -> None:
    """A command added to commands/ but absent from the mirror is drift."""
    _sources(tmp_path)
    _claude_mirror(tmp_path)
    (tmp_path / "commands" / "close.md").write_text("---\nx: 1\n---\nb\n", encoding="utf-8")
    assert bridge_state.mirror_missing(tmp_path, "claude") is True


def test_claude_broken_symlink_is_stale(bridge_state, tmp_path: Path) -> None:
    """An anchor whose link target vanished counts as missing, not as present."""
    _sources(tmp_path)
    _claude_mirror(tmp_path)
    anchor = tmp_path / ".claude" / "agents" / "principal_agent.md"
    anchor.unlink()
    anchor.symlink_to(tmp_path / "does_not_exist.md")
    assert bridge_state.mirror_missing(tmp_path, "claude") is True


def test_lock_matching_head_does_not_prove_the_mirror(
    bridge_state, tmp_path: Path
) -> None:
    """The defect this module exists for: a fresh lock over an absent mirror.

    Before Sprint 041 the boot consulted the lock alone and reported the bridge
    fresh in exactly this state, then never retried because the lock matched.
    """
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    _sources(tmp_path)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "seed", "--no-verify"], cwd=tmp_path, check=True
    )
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    bridge_state.lock_path(tmp_path, "claude").write_text(head + "\n", encoding="utf-8")

    assert bridge_state.lock_stale(tmp_path, "claude") is False
    assert bridge_state.bridge_stale(tmp_path, "claude", nucleus=True) is True


def test_targets_are_independent(bridge_state, tmp_path: Path) -> None:
    """Asking about one target never reports on the other's tree.

    This is the bi-harness guarantee: a repository worked from both harnesses
    has each mirror judged on its own.
    """
    _sources(tmp_path)
    _claude_mirror(tmp_path)
    assert bridge_state.mirror_missing(tmp_path, "claude") is False
    assert bridge_state.mirror_missing(tmp_path, "cursor") is True

    _cursor_mirror(tmp_path)
    assert bridge_state.mirror_missing(tmp_path, "cursor") is False
    assert bridge_state.mirror_missing(tmp_path, "claude") is False


def test_unknown_target_is_never_claimed_stale(bridge_state, tmp_path: Path) -> None:
    """The module does not speak for a bridge it does not implement."""
    _sources(tmp_path)
    assert bridge_state.mirror_missing(tmp_path, "zed") is False
    assert bridge_state.bridge_stale(tmp_path, "zed", nucleus=True) is False


def test_claude_content_is_membership_only(bridge_state, tmp_path: Path) -> None:
    """Claude's mirror is symlinks, so content cannot drift while links resolve."""
    _sources(tmp_path)
    _claude_mirror(tmp_path)
    assert bridge_state.content_stale(tmp_path, "claude", nucleus=True) is False


def test_host_mode_separates_mirror_root_from_framework_root(
    bridge_state, tmp_path: Path
) -> None:
    """In a host, `.claude/` sits at the project root and sources in .agents/."""
    host = tmp_path / "host"
    framework = host / ".agents"
    framework.mkdir(parents=True)
    _sources(framework)
    assert bridge_state.mirror_missing(host, "claude", framework_root=framework) is True

    _claude_mirror(host)
    assert bridge_state.mirror_missing(host, "claude", framework_root=framework) is False
