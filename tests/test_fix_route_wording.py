"""Instructing texts name the `Repro: manual` route beside the `fix(` paired test.

Convergence rule 3 (`rules/qa_and_testing.md` §4) for the family found twice in
Sprint 057 Gate 1 (QA1-2, QA2-3): a text states the paired test of a `fix(`
commit unconditionally, omitting the `Repro: manual` route that
`hooks/on_commit.py audit_regression_test` accepts.

Exact coverage, and no more (`agents.md §1 fail_closed_claims`): every line of
the files in `SCANNED` that matches `FAMILY` must also contain `Repro: manual`.
A line that states the requirement in other words is not checked.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCANNED = (
    "agents.md",
    "agents/*.md",
    "rules/*.md",
    "workflows/*.md",
    "docs/standards/templates/*.md",
    "docs/guides/*.md",
    "memory_index.json",
)
FAMILY = re.compile(
    r"paired test|untestable|ships its (paired )?test|must stage the test"
    r"|stage[sd]? (a|the|its) test",
    re.IGNORECASE,
)
ROUTE = "Repro: manual"


def scanned_files(root: Path) -> list[Path]:
    """Resolve `SCANNED` under ``root``.

    Args:
        root: Framework root to scan.

    Returns:
        list[Path]: The matching files, pattern by pattern, each pattern sorted.
    """
    return [path for pattern in SCANNED for path in sorted(root.glob(pattern))]


def family_lines_without_route(root: Path) -> list[str]:
    """List every scanned line that matches the family but omits the route.

    Args:
        root: Framework root to scan.

    Returns:
        list[str]: ``<path>:<line>`` for each offending line, in scan order.
    """
    return [
        f"{path.relative_to(root)}:{number}"
        for path in scanned_files(root)
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if FAMILY.search(line) and ROUTE not in line
    ]


def test_every_paired_test_statement_names_the_manual_route() -> None:
    assert family_lines_without_route(ROOT) == []


def test_scanned_patterns_resolve_to_files() -> None:
    """A renamed directory would silently empty the scan."""
    for pattern in SCANNED:
        assert list(ROOT.glob(pattern)), pattern
