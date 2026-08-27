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
