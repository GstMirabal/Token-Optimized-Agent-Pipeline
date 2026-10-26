"""The one grammar of the ``Repro:`` trailer of a ``fix(`` commit.

invoked_by: hooks/on_commit.py `audit_regression_test`, scripts/check_fix_reproduces.py `parse_trailers`

Two grammars existed (Sprint 057, defect A-4/B-1): the commit hook accepted a
strict form and the replayer a loose one, so a trailer one parsed could be
refused by the other. This module holds the strict grammar of the hook; both
consumers import it. Pure stdlib, no I/O.

The same split existed for which staged paths are tests and which are source
(Gate 1 round 1, QA1-3): the hook used a suffix allowlist and the replayer a
documentation denylist, so a JSON-only ``fix(`` passed the hook and failed the
replay. ``is_test_path`` and ``is_source_path`` are the one definition both use.

Accepted forms (the separator is an em dash or ``--``):

* ``Repro: <path>[::<id>] — fails at <7-40 hex sha>``
* ``Repro: manual — <text>``
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath

REPRO_TEST = re.compile(
    r"^Repro:[ \t]+(?P<path>[^\s:]+)(?:::(?P<id>\S+))?[ \t]+(?:—|--)[ \t]+fails at[ \t]+"
    r"(?P<sha>[0-9a-fA-F]{7,40})[ \t]*$",
    re.MULTILINE,
)
NON_SOURCE_SUFFIXES = frozenset({".md", ".rst", ".txt", ".yml", ".yaml", ".toml"})
TEST_DIRS = frozenset({"tests", "test", "__tests__"})
REPRO_MANUAL = re.compile(
    r"^Repro:[ \t]+manual[ \t]+(?:—|--)[ \t]+(?P<text>\S.*?)[ \t]*$", re.MULTILINE
)


@dataclass(frozen=True)
class ReproClaim:
    """One parsed ``Repro:`` trailer.

    Attributes:
        kind: ``"test"`` for a test-id trailer, ``"manual"`` for ``Repro: manual``.
        path: Test file path (``"test"`` only, else ``""``).
        test_id: Part after ``::`` (``"test"`` only; ``""`` when absent).
        parent_sha: Short or full SHA after ``fails at`` (``"test"`` only).
        text: Free text after the separator (``"manual"`` only).
    """

    kind: str
    path: str = ""
    test_id: str = ""
    parent_sha: str = ""
    text: str = ""

    @property
    def claim(self) -> str:
        """Left-hand side of the trailer: ``path[::id]`` or ``manual``."""
        if self.kind == "manual":
            return "manual"
        return f"{self.path}::{self.test_id}" if self.test_id else self.path


def parse_trailers(message: str) -> list[ReproClaim]:
    """Parse every well-formed ``Repro:`` trailer of a commit message, in order.

    A line that fits neither form is ignored. A line fitting both
    (``Repro: manual — fails at abc1234``) is ``manual``, as the hook decides.

    Args:
        message: Full commit message.

    Returns:
        The claims in message order; empty when there is no well-formed trailer.
    """
    found: list[tuple[int, ReproClaim]] = []
    manual_starts: set[int] = set()
    for m in REPRO_MANUAL.finditer(message):
        manual_starts.add(m.start())
        found.append((m.start(), ReproClaim(kind="manual", text=m.group("text"))))
    for m in REPRO_TEST.finditer(message):
        if m.start() in manual_starts:
            continue
        claim = ReproClaim(
            kind="test",
            path=m.group("path"),
            test_id=m.group("id") or "",
            parent_sha=m.group("sha"),
        )
        found.append((m.start(), claim))
    return [claim for _, claim in sorted(found, key=lambda pair: pair[0])]


def is_test_path(path: str) -> bool:
    """Tell whether a repository path is a test file.

    Args:
        path: Repository-relative path.

    Returns:
        bool: True for files under a ``tests``/``test``/``__tests__`` directory,
            named ``test_*`` or ``tests.py``, or whose stem ends in ``_test``,
            ``.test`` or ``.spec``.
    """
    p = PurePosixPath(path)
    return (
        bool(TEST_DIRS & set(p.parts[:-1]))
        or p.name.startswith("test_")
        or p.name == "tests.py"
        or p.stem.endswith(("_test", ".test", ".spec"))
    )


def is_source_path(path: str) -> bool:
    """Tell whether a repository path is source a ``fix(`` must prove with a test.

    Source is every path that is neither a test nor a documentation file: a
    denylist of ``NON_SOURCE_SUFFIXES``, so configuration (``.json``), shell and
    suffixless files such as ``Makefile`` count as source.

    Args:
        path: Repository-relative path.

    Returns:
        bool: True when ``path`` is not a test and its suffix is not in
            ``NON_SOURCE_SUFFIXES``.
    """
    return not is_test_path(path) and PurePosixPath(path).suffix not in NON_SOURCE_SUFFIXES
