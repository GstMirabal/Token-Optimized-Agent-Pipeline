"""Texts that describe the Phase 7 gate row name its Severity cell.

Convergence rule 3 (`rules/qa_and_testing.md` §4) for the family found twice in
Sprint 057 (closeout audit A1, Gate 1 round 8 QA8-1): a profile or workflow
describes the gate row or verdict register as Verdict plus Class, omitting the
`Severity` cell that `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` requires.

Exact coverage, and no more (`agents.md §1 fail_closed_claims`): every line of
the files in `SCANNED` that matches `FIELDS` and `ROW_CONTEXT` must also contain
`Severity`, and every line that matches `EMITTED` (Gate 1 round 9, QA9-3) must
name severity in any case. A line that describes the row or the emitted verdict
in other words is not checked.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCANNED = (
    "agents.md",
    "agents/*.md",
    "rules/*.md",
    "workflows/*.md",
    "commands/*.md",
    "docs/standards/templates/*.md",
    "docs/guides/*.md",
)
FIELDS = re.compile(r"\bVerdict\b.*\bClass\b|\bClass\b.*\bVerdict\b")
ROW_CONTEXT = re.compile(r"\brows?\b|register|transcrib|Gate \\?\| Round", re.IGNORECASE)
REQUIRED = "Severity"
EMITTED = re.compile(r"RECORD`?[^.]{0,30}\b(plus|with) class\b", re.IGNORECASE)
EMITTED_REQUIRED = re.compile(r"severity", re.IGNORECASE)


def scanned_files(root: Path) -> list[Path]:
    """Resolve `SCANNED` under ``root``.

    Args:
        root: Framework root to scan.

    Returns:
        list[Path]: The matching files, pattern by pattern, each pattern sorted.
    """
    return [path for pattern in SCANNED for path in sorted(root.glob(pattern))]


def row_lines_without_severity(root: Path) -> list[str]:
    """List every scanned gate-row line that omits the Severity cell.

    Args:
        root: Framework root to scan.

    Returns:
        list[str]: ``<path>:<line>`` for each offending line, in scan order.
    """
    return [
        f"{path.relative_to(root)}:{number}"
        for path in scanned_files(root)
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if FIELDS.search(line) and ROW_CONTEXT.search(line) and REQUIRED not in line
    ]


def emitted_lines_without_severity(root: Path) -> list[str]:
    """List every scanned line stating the emitted verdict and class but no severity.

    Args:
        root: Framework root to scan.

    Returns:
        list[str]: ``<path>:<line>`` for each offending line, in scan order.
    """
    return [
        f"{path.relative_to(root)}:{number}"
        for path in scanned_files(root)
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        if EMITTED.search(line) and not EMITTED_REQUIRED.search(line)
    ]


def test_every_gate_row_description_names_severity() -> None:
    assert row_lines_without_severity(ROOT) == []


def test_every_emitted_verdict_statement_names_severity() -> None:
    assert emitted_lines_without_severity(ROOT) == []


def test_scanned_patterns_resolve_to_files() -> None:
    """A renamed directory would silently empty the scan."""
    for pattern in SCANNED:
        assert list(ROOT.glob(pattern)), pattern


def test_family_matches_the_known_row_descriptions() -> None:
    """The patterns still select the texts that define the row.

    A rewording that dropped them out of `FIELDS` or `ROW_CONTEXT` would turn
    the scan into a check of nothing.
    """
    known = ("agents/orchestrator.md", "agents/qa_agent.md", "agents/tester_agent.md",
             "workflows/pipeline_workflow.md", "docs/standards/templates/SPRINT_LOG_TEMPLATE.md")
    for name in known:
        lines = (ROOT / name).read_text(encoding="utf-8").splitlines()
        assert any(FIELDS.search(line) and ROW_CONTEXT.search(line) for line in lines), name


def test_emitted_pattern_matches_the_known_statements() -> None:
    """`EMITTED` still selects the four QA9-3 lines; see the test above."""
    known = ("agents.md", "agents/qa_agent.md", "agents/tester_agent.md",
             "docs/guides/MODEL_TIER_TRIAL_GUIDE.md")
    for name in known:
        lines = (ROOT / name).read_text(encoding="utf-8").splitlines()
        assert any(EMITTED.search(line) for line in lines), name
