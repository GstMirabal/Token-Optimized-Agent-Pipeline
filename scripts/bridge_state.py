"""Bridge mirror integrity and staleness, for every harness and every boot path.

The bridge is the mirror a harness reads: ``.claude/`` (symlinks) or
``.cursor/`` (rendered copies). Two independent things can be wrong with it,
and a lock file proves neither:

* the mirror is **missing or incomplete** — wiped by ``git clean``, a manual
  deletion, or simply never installed on a fresh checkout;
* the mirror is **present but divergent** — its content no longer matches
  ``commands/`` and ``agents/``.

Before Sprint 041 the portable boot asked only whether ``.bridge_<target>.lock``
matched ``HEAD``, and for every target but ``cursor`` it could not detect either
condition. ``scripts/session_start.py --boot --tool claude-code`` therefore
printed ``content fresh`` on a checkout with no ``.claude/`` directory at all,
exit ``0``, and then never retried, because refreshing the lock made it match
``HEAD`` from that point on. ``hooks/on_init.py`` already held the correct
predicate (``bridge_intact``) and its own docstring named the portable boot as
its counterpart; it was never wired in. This module is that wiring, so the two
callers cannot drift apart again.

**Targets are independent.** Asking about one never inspects, installs or
removes the other: a repository worked from both harnesses has each mirror
repaired by whichever boot arrives first, and neither boot damages the other's
tree.

invoked_by: scripts/session_start.py, hooks/on_init.py

Usage:
    from bridge_state import bridge_stale, lock_stale, mirror_missing

    if bridge_stale(root, "claude", nucleus=True):
        ...  # run scripts/install.sh --target claude
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TARGETS: tuple[str, ...] = ("claude", "cursor")

# Relative to the directory that holds the mirror. A broken symlink fails
# `Path.exists()`, so these cover a link whose destination vanished too.
CLAUDE_ANCHORS: tuple[Path, ...] = (
    Path(".claude/commands/agents/start.md"),
    Path(".claude/agents/principal_agent.md"),
)


def lock_path(root: Path, target: str) -> Path:
    """Path of the bridge lock for one target.

    Args:
        root: Framework checkout that holds the lock files.
        target: ``claude`` or ``cursor``.

    Returns:
        Path: ``<root>/.bridge_<target>.lock``, whether or not it exists.
    """
    return root / f".bridge_{target}.lock"


def lock_stale(root: Path, target: str) -> bool:
    """True when the lock is absent or does not record the current ``HEAD``.

    A fresh lock is **not** proof the mirror is intact — that is the defect
    this module exists for. Callers pair this with `bridge_stale`.

    Args:
        root: Framework checkout, used both for the lock and for ``git``.
        target: ``claude`` or ``cursor``.

    Returns:
        bool: True when the lock is missing, unreadable, or behind ``HEAD``.
    """
    lock = lock_path(root, target)
    if not lock.is_file():
        return True
    try:
        recorded = lock.read_text(encoding="utf-8").strip()
    except OSError:
        return True
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return True
    return recorded != proc.stdout.strip()


def _names(directory: Path) -> set[str]:
    """Markdown file names directly under ``directory`` (empty when absent)."""
    if not directory.is_dir():
        return set()
    return {path.name for path in directory.glob("*.md")}


def _claude_mirror_missing(host_dir: Path, framework_root: Path) -> bool:
    """True when the Claude mirror is absent, incomplete, or broken."""
    if any(not (host_dir / anchor).exists() for anchor in CLAUDE_ANCHORS):
        return True
    commands_missing = _names(framework_root / "commands") - _names(
        host_dir / ".claude" / "commands" / "agents"
    )
    agents_missing = _names(framework_root / "agents") - _names(
        host_dir / ".claude" / "agents"
    )
    return bool(commands_missing or agents_missing)


def _cursor_mirror_missing(host_dir: Path) -> bool:
    """True when the Cursor mirror directories are absent."""
    cursor = host_dir / ".cursor"
    return not (cursor / "commands").is_dir() or not (cursor / "agents").is_dir()


def mirror_missing(
    host_dir: Path, target: str, *, framework_root: Path | None = None
) -> bool:
    """True when this target's mirror is absent or incomplete on disk.

    Args:
        host_dir: Directory that holds ``.claude/`` / ``.cursor/``. In the
            nucleus this is the framework checkout; in a host it is the host
            project root.
        target: ``claude`` or ``cursor``.
        framework_root: Checkout holding ``commands/`` and ``agents/``.
            Defaults to ``host_dir`` (the nucleus case).

    Returns:
        bool: True when an install is needed. Unknown targets return False —
        this module never speaks for a bridge it does not implement.
    """
    root = framework_root if framework_root is not None else host_dir
    if target == "claude":
        return _claude_mirror_missing(host_dir, root)
    if target == "cursor":
        return _cursor_mirror_missing(host_dir)
    return False


def content_stale(host_dir: Path, target: str, *, nucleus: bool) -> bool:
    """True when a present mirror's content diverges from its source.

    Claude's mirror is built from symlinks, so its content cannot drift while
    the links resolve — membership is the only failure mode, and
    `mirror_missing` already covers it. Cursor's mirror is rendered copies,
    which can drift after the lock was written (Sprint 039).

    Args:
        host_dir: Directory that holds the mirror.
        target: ``claude`` or ``cursor``.
        nucleus: Same flag the Cursor renderer uses for its path rewrite.

    Returns:
        bool: True when the rendered copies no longer match their source.
    """
    if target != "cursor":
        return False
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from cursor_adapter import commands_stale

    return bool(commands_stale(host_dir, nucleus=nucleus))


def bridge_stale(
    host_dir: Path,
    target: str,
    *,
    nucleus: bool,
    framework_root: Path | None = None,
) -> bool:
    """True when this target's bridge needs reinstalling.

    The union of both failure modes, which is what `workflows/start_workflow.md`
    Phase 1.5 has always promised and what no code implemented before Sprint 041.

    Args:
        host_dir: Directory that holds ``.claude/`` / ``.cursor/``.
        target: ``claude`` or ``cursor``.
        nucleus: Same flag the Cursor renderer uses for its path rewrite.
        framework_root: Checkout holding ``commands/`` and ``agents/``.
            Defaults to ``host_dir``.

    Returns:
        bool: True when ``install.sh --target <target>`` must run.
    """
    if mirror_missing(host_dir, target, framework_root=framework_root):
        return True
    return content_stale(host_dir, target, nucleus=nucleus)
