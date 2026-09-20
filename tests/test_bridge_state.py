"""Tests for scripts/bridge_state.py — bridge integrity, per target (Sprint 041).

Every check here fails against the tree before Sprint 041, where the predicate
did not exist and the portable boot asked only whether the lock matched HEAD.
"""

from __future__ import annotations

import importlib
import shutil
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
    (root / "agents" / "principal_agent.md").write_text(
        "---\nname: principal-agent\ndescription: Lead agent.\n---\nProfile body.\n",
        encoding="utf-8",
    )


def _claude_mirror(root: Path) -> None:
    """Scaffold a complete Claude mirror mapping every source file."""
    commands = root / ".claude" / "commands" / "agents"
    commands.mkdir(parents=True, exist_ok=True)
    (commands / "start.md").write_text("linked\n", encoding="utf-8")
    agents = root / ".claude" / "agents"
    agents.mkdir(parents=True, exist_ok=True)
    (agents / "principal_agent.md").write_text("linked\n", encoding="utf-8")


def _cursor_mirror(root: Path) -> None:
    """Scaffold a complete Cursor mirror mapping every source file (`D4`).

    ``rules/`` and ``mcp.json`` are part of this mirror's membership test even
    though `_sources` carries no ``rules/`` source dir — `expected_cursor_rule_names`
    treats an absent source as "only the two standing rules", so this fixture
    carries exactly those two.
    """
    commands = root / ".cursor" / "commands"
    commands.mkdir(parents=True, exist_ok=True)
    (commands / "start.md").write_text("rendered\n", encoding="utf-8")
    agents = root / ".cursor" / "agents"
    agents.mkdir(parents=True, exist_ok=True)
    (agents / "principal-agent.md").write_text("rendered\n", encoding="utf-8")
    rules = root / ".cursor" / "rules"
    rules.mkdir(parents=True, exist_ok=True)
    (rules / "00-constitution.mdc").write_text("constitution\n", encoding="utf-8")
    (rules / "01-chat-title.mdc").write_text("chat title\n", encoding="utf-8")
    (root / ".cursor" / "mcp.json").write_text("{}\n", encoding="utf-8")


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


# --- F-049-2: bridge_stale(cursor) must see an incomplete mirror ----------


def test_cursor_mirror_missing_rules_dir_is_stale(bridge_state, tmp_path: Path) -> None:
    """Before D4 this returned False — is_dir() checked only commands/ and agents/."""
    _sources(tmp_path)
    _cursor_mirror(tmp_path)
    shutil.rmtree(tmp_path / ".cursor" / "rules")
    assert bridge_state.mirror_missing(tmp_path, "cursor") is True


def test_cursor_mirror_missing_constitution_is_stale(bridge_state, tmp_path: Path) -> None:
    """The one alwaysApply: true rule that imports agents.md, gone, must be caught.

    This is the exact defect measured in Sprint 049 Phase 1: deleting every
    .cursor/rules/*.mdc left a Cursor session able to boot with zero
    governance rules loaded, undetected.
    """
    _sources(tmp_path)
    _cursor_mirror(tmp_path)
    (tmp_path / ".cursor" / "rules" / "00-constitution.mdc").unlink()
    assert bridge_state.mirror_missing(tmp_path, "cursor") is True


def test_cursor_mirror_missing_most_agents_is_stale(bridge_state, tmp_path: Path) -> None:
    """13 of 14 agents deleted (the measured Phase 1 repro) must not read as fresh."""
    _sources(tmp_path)
    _cursor_mirror(tmp_path)
    (tmp_path / ".cursor" / "agents" / "principal-agent.md").unlink()
    assert bridge_state.mirror_missing(tmp_path, "cursor") is True


def test_cursor_mirror_missing_mcp_json_is_stale(bridge_state, tmp_path: Path) -> None:
    _sources(tmp_path)
    _cursor_mirror(tmp_path)
    (tmp_path / ".cursor" / "mcp.json").unlink()
    assert bridge_state.mirror_missing(tmp_path, "cursor") is True


def test_cursor_mirror_complete_is_fresh(bridge_state, tmp_path: Path) -> None:
    """The positive case: a genuinely complete Cursor mirror is not stale."""
    _sources(tmp_path)
    _cursor_mirror(tmp_path)
    assert bridge_state.mirror_missing(tmp_path, "cursor") is False


def test_cursor_mirror_missing_one_rendered_rule_is_stale(
    bridge_state, tmp_path: Path
) -> None:
    """A rules/ source file with no rendered .mdc counterpart is drift, not noise."""
    (tmp_path / "commands").mkdir(parents=True, exist_ok=True)
    (tmp_path / "commands" / "start.md").write_text("---\nx: 1\n---\nb\n", encoding="utf-8")
    (tmp_path / "agents").mkdir(parents=True, exist_ok=True)
    (tmp_path / "agents" / "principal_agent.md").write_text(
        "---\nname: principal-agent\ndescription: Lead agent.\n---\nBody.\n",
        encoding="utf-8",
    )
    (tmp_path / "rules").mkdir(parents=True, exist_ok=True)
    (tmp_path / "rules" / "code_craft.md").write_text("# Rule\nBody.\n", encoding="utf-8")
    _cursor_mirror(tmp_path)
    assert bridge_state.mirror_missing(tmp_path, "cursor") is True
