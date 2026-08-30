"""Tests for scripts/cursor_adapter.py (Sprint 039 C2 + Sprint 040 I2)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import cursor_adapter as ca  # noqa: E402


def test_commands_stale_true_when_dest_digest_mismatch(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    cmds = root / "commands"
    dest = root / ".cursor" / "commands"
    cmds.mkdir(parents=True)
    dest.mkdir(parents=True)
    src_body = "---\ndescription: test\n---\nRun `foo`.\n"
    (cmds / "start.md").write_text(src_body, encoding="utf-8")
    (dest / "start.md").write_text("stale content\n", encoding="utf-8")
    assert ca.commands_stale(root, nucleus=True) is True


def test_commands_stale_false_after_expected_render(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    cmds = root / "commands"
    dest = root / ".cursor" / "commands"
    cmds.mkdir(parents=True)
    dest.mkdir(parents=True)
    src_body = "---\ndescription: test\n---\nRun `foo`.\n"
    (cmds / "start.md").write_text(src_body, encoding="utf-8")
    rendered = ca.expected_cursor_command_text(src_body, nucleus=True)
    (dest / "start.md").write_text(rendered, encoding="utf-8")
    assert ca.commands_stale(root, nucleus=True) is False


def test_prune_dir_removes_orphan_keeps_expected(tmp_path: Path) -> None:
    directory = tmp_path / "commands"
    directory.mkdir()
    keep = directory / "keep.md"
    orphan = directory / "orphan.md"
    keep.write_text("ok\n", encoding="utf-8")
    orphan.write_text("gone\n", encoding="utf-8")
    ca._prune_dir(directory, expected_names={"keep.md"}, suffix=".md")
    assert keep.is_file()
    assert not orphan.exists()


def test_install_cursor_bridge_preserves_cursor_root_sentinel(
    tmp_path: Path,
) -> None:
    """Incremental install must not rmtree ``.cursor/`` (Sprint 040)."""
    root = tmp_path / "repo"
    cursor = root / ".cursor"
    cursor.mkdir(parents=True)
    sentinel = cursor / "SENTINEL"
    sentinel.write_text("keep\n", encoding="utf-8")
    orphan = cursor / "commands" / "orphan_should_go.md"
    orphan.parent.mkdir(parents=True)
    orphan.write_text("orphan\n", encoding="utf-8")
    ca.install_cursor_bridge(root, nucleus=True)
    assert sentinel.is_file()
    assert sentinel.read_text(encoding="utf-8") == "keep\n"
    assert not orphan.exists()
    assert (cursor / "commands").is_dir()


def test_install_permission_error_uses_stable_prefix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def boom(_cursor_dir: Path, *, nucleus: bool) -> set[str]:
        raise PermissionError("simulated")

    monkeypatch.setattr(ca, "_write_commands", boom)
    with pytest.raises(PermissionError) as excinfo:
        ca.install_cursor_bridge(tmp_path / "repo", nucleus=True)
    assert str(excinfo.value).startswith("bridge: permission denied on .cursor")


def test_render_rewrites_the_tool_token_for_cursor() -> None:
    """The Cursor copy claims the anchor as Cursor; the source is for Claude.

    `commands/` is one source mirrored asymmetrically - Claude symlinks it,
    Cursor gets a rendered copy - so the harness-specific value is produced
    here. Before Sprint 041 the source hardcoded `--tool cursor` and both
    harnesses read it, so a Claude Code session claimed the anchor as Cursor.
    """
    src = "---\nd: x\n---\nRun `session_start.py --boot --tool claude-code`.\n"
    rendered = ca.expected_cursor_command_text(src, nucleus=True)
    assert "--tool cursor" in rendered
    assert "--tool claude-code" not in rendered


def test_render_leaves_other_tool_values_alone() -> None:
    """Only the Claude token is rewritten; terminal and cursor pass through."""
    for value in ("--tool terminal", "--tool cursor"):
        src = f"---\nd: x\n---\nRun `session_start.py --boot {value}`.\n"
        assert value in ca.expected_cursor_command_text(src, nucleus=True)


def test_shipped_start_command_carries_the_claude_token() -> None:
    """The source of record must be the Claude form, or the symlink is wrong.

    Claude reads `commands/start.md` through a symlink, so whatever the source
    says is what a Claude session runs. There is no render step on that side.
    """
    src = (SCRIPTS.parent / "commands" / "start.md").read_text(encoding="utf-8")
    assert "--tool claude-code" in src
    assert "--tool cursor" in ca.expected_cursor_command_text(src, nucleus=True)
