"""Tests for `scripts/_mode.py` `is_nucleus()` linked-worktree recognition.

Sprint 047 unit U21, paired with U16's `fix(` for `scripts/_mode.py`.

U16 taught `is_nucleus()` to accept a linked git worktree of the nucleus: a
worktree keeps `.git` as a *file* whose `gitdir:` leads into the nucleus's own
`<root>/.git/worktrees/<name>/`, whose `commondir` resolves back to a real
`.git` directory whose parent carries the framework markers (`agents.md`,
`workflows/`, `scripts/_mode.py`). A submodule pointer (`gitdir:` into
`.git/modules/`) and any malformed `.git` file stay classified as a host.

Against `HEAD`'s `_mode.py` (`is_nucleus()` is `(agents_root() / ".git").is_dir()`)
the two worktree cases below — `test_nucleus_worktree_absolute_pointer_is_nucleus`
and `test_relative_gitdir_pointer_into_worktree_is_nucleus` — FAIL, because a
`.git` file is not a directory. The other four cases pass on both revisions and
stand as regression guards.

invoked_by: Makefile verify via pytest tests/.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import _mode  # noqa: E402


def _make_nucleus(root: Path, *, markers: bool = True, worktree: str = "w1") -> Path:
    """Build a nucleus-shaped tree: framework markers plus a real `.git/`.

    Args:
        root: Directory to populate as the nucleus checkout.
        markers: When True, write `agents.md`, `workflows/` and
            `scripts/_mode.py` so `_is_framework_dir` recognises `root`.
        worktree: Name of the linked-worktree subdirectory created under
            `<root>/.git/worktrees/`, carrying a `commondir` of `../..`.

    Returns:
        Path: The populated `root`.
    """
    root.mkdir(parents=True, exist_ok=True)
    if markers:
        (root / "agents.md").write_text("# agents\n", encoding="utf-8")
        (root / "workflows").mkdir(exist_ok=True)
        (root / "scripts").mkdir(exist_ok=True)
        (root / "scripts" / "_mode.py").write_text("", encoding="utf-8")
    private = root / ".git" / "worktrees" / worktree
    private.mkdir(parents=True)
    (private / "commondir").write_text("../..\n", encoding="utf-8")
    return root


def _make_checkout(checkout: Path, pointer: str) -> Path:
    """Build a checkout whose `.git` is a pointer file.

    Args:
        checkout: Directory to populate; its `.git` becomes a file.
        pointer: Value written after `gitdir: ` in the `.git` file.

    Returns:
        Path: The populated `checkout`.
    """
    checkout.mkdir(parents=True, exist_ok=True)
    (checkout / ".git").write_text(f"gitdir: {pointer}\n", encoding="utf-8")
    return checkout


def test_plain_clone_with_real_git_dir_is_nucleus(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`.git` a real directory: the unchanged plain-clone path. Passes on HEAD."""
    root = tmp_path / "clone"
    (root / ".git").mkdir(parents=True)
    monkeypatch.setattr(_mode, "agents_root", lambda: root)
    assert _mode.is_nucleus() is True


def test_nucleus_worktree_absolute_pointer_is_nucleus(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Linked worktree with an absolute `gitdir:` into the nucleus. Fails on HEAD."""
    nucleus = _make_nucleus(tmp_path / "nucleus")
    checkout = _make_checkout(
        tmp_path / "wt", str(nucleus / ".git" / "worktrees" / "w1")
    )
    monkeypatch.setattr(_mode, "agents_root", lambda: checkout)
    assert _mode.is_nucleus() is True


def test_relative_gitdir_pointer_into_worktree_is_nucleus(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Linked worktree with a relative `gitdir: ../.git/worktrees/w1`. Fails on HEAD."""
    _make_nucleus(tmp_path)
    checkout = _make_checkout(tmp_path / "wt", "../.git/worktrees/w1")
    monkeypatch.setattr(_mode, "agents_root", lambda: checkout)
    assert _mode.is_nucleus() is True


def test_submodule_pointer_is_not_nucleus(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`gitdir:` into a superproject `.git/modules/` stays a host. Passes on HEAD."""
    modules = tmp_path / "super" / ".git" / "modules" / ".agents"
    modules.mkdir(parents=True)
    checkout = _make_checkout(tmp_path / "host", str(modules))
    monkeypatch.setattr(_mode, "agents_root", lambda: checkout)
    assert _mode.is_nucleus() is False


def test_malformed_git_file_without_gitdir_line_is_not_nucleus(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A `.git` file carrying no `gitdir:` line stays a host. Passes on HEAD."""
    checkout = tmp_path / "broken"
    checkout.mkdir()
    (checkout / ".git").write_text("not a pointer file\n", encoding="utf-8")
    monkeypatch.setattr(_mode, "agents_root", lambda: checkout)
    assert _mode.is_nucleus() is False


def test_worktree_pointer_without_framework_markers_is_not_nucleus(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Well-formed worktree pointer whose common parent lacks the markers.

    Guards U16's `_is_framework_dir` gate. Passes on HEAD (also False).
    """
    bare = _make_nucleus(tmp_path / "bare", markers=False)
    checkout = _make_checkout(
        tmp_path / "wt", str(bare / ".git" / "worktrees" / "w1")
    )
    monkeypatch.setattr(_mode, "agents_root", lambda: checkout)
    assert _mode.is_nucleus() is False
