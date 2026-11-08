"""Resolve the anchor's current sprint directory for every ``--current-sprint`` check.

Each check resolved it on its own, and each read "nothing resolved" as "nothing
to check": a subdirectory working directory, a zero-padded string id, a deleted
sprint directory and a truncated anchor all printed ``[OK] ... (skip)`` and exited
``0`` (Sprint 059 QA Gate 1 rounds 10 to 12). Here only two inputs skip: no
anchor file, and an anchor with no ``current_sprint`` block. Every other failure
raises ``CurrentSprintError``, which the caller turns into exit ``2``.

The root is the nearest ancestor of the working directory, itself included, that
holds a ``.git`` entry (directory or file), so a check run from a subdirectory
reads the same anchor as one run from the repository root. With no such ancestor
the working directory is the root, as before.

invoked_by: scripts/check_task_scope.py, scripts/check_gate_log.py,
skills/token-saver-auditor/scripts/audit_plan.py, scripts/check_sprint_refs.py.

Usage:
    from _current_sprint import CurrentSprintError, current_sprint_dir, project_root
"""

from __future__ import annotations

import json
from pathlib import Path

ANCHOR = Path("docs") / "active_state.json"


class CurrentSprintError(Exception):
    """The anchor exists but does not name a sprint directory that exists."""


def project_root(cwd: Path | None = None) -> Path:
    """The nearest ancestor of ``cwd`` holding ``.git``, else ``cwd`` itself.

    Args:
        cwd: Starting directory; the process working directory when None.

    Returns:
        Path: The directory whose ``docs/active_state.json`` is the anchor.
    """
    start = (cwd or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


def _read_anchor(anchor: Path) -> dict:
    """Parse the anchor file, raising on any unreadable or malformed content.

    Args:
        anchor: Path to ``docs/active_state.json``.

    Returns:
        dict: The parsed anchor.

    Raises:
        CurrentSprintError: The file cannot be read, is not JSON, or is not an object.
    """
    try:
        data = json.loads(anchor.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CurrentSprintError(f"{anchor} is unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise CurrentSprintError(f"{anchor} is not a JSON object")
    return data


def sprint_number(raw: object) -> int:
    """Convert ``current_sprint.id`` to an integer.

    Args:
        raw: The id as stored: an integer or a string of digits such as ``"059"``.

    Returns:
        int: The sprint number.

    Raises:
        CurrentSprintError: The id is missing, a boolean, or not all digits.
    """
    if isinstance(raw, bool) or not isinstance(raw, (int, str)):
        raise CurrentSprintError(f"current_sprint.id is not a sprint number: {raw!r}")
    text = str(raw).strip()
    if not text.isdigit():
        raise CurrentSprintError(f"current_sprint.id is not a sprint number: {raw!r}")
    return int(text)


def current_sprint_dir(root: Path) -> Path | None:
    """The canonical sprint directory the anchor names under ``root``.

    Args:
        root: Repository root holding ``docs/active_state.json``.

    Returns:
        Path | None: The sprint directory; None only when the anchor file is
            absent or has no ``current_sprint`` block.

    Raises:
        CurrentSprintError: The anchor is unreadable, its id is unusable, or no
            ``docs/sprints/NNN-*`` directory exists for it.
    """
    anchor = root / ANCHOR
    if not anchor.is_file():
        return None
    sprint = _read_anchor(anchor).get("current_sprint")
    if sprint is None:
        return None
    if not isinstance(sprint, dict):
        raise CurrentSprintError(f"{anchor}: current_sprint is not an object")
    number = sprint_number(sprint.get("id"))
    matches = sorted((root / "docs" / "sprints").glob(f"{number:03d}-*"))
    dirs = [path for path in matches if path.is_dir()]
    if not dirs:
        raise CurrentSprintError(f"{anchor} names sprint {number:03d}, which has no directory")
    return dirs[0]
