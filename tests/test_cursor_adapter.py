"""Tests for scripts/cursor_adapter.py commands_stale (Sprint 039 C2)."""

from __future__ import annotations

import sys
from pathlib import Path

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
