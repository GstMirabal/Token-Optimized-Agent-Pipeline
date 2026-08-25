"""Pin Sprint 033 close of F-021-A2 (implementer role).

The finding's own recipe must be used: Write/Edit as whole tools-list
items. Substring ``grep Write`` falsely counts ``TodoWrite`` on
``principal_agent``.

invoked_by: Makefile verify via pytest tests/.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
TOOLS_LINE = re.compile(r"^tools:\s*(.+)$", re.MULTILINE)
# Word-boundary form from docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md F-021-A2.
WRITE_OR_EDIT_ITEM = re.compile(r"(^|[ ,])(Write|Edit)([ ,]|$)")


def _tools_line(path: Path) -> str:
    match = TOOLS_LINE.search(path.read_text(encoding="utf-8"))
    assert match is not None, f"{path.name}: missing tools: frontmatter"
    return match.group(1)


def _write_holders() -> list[str]:
    holders: list[str] = []
    for path in sorted(AGENTS.glob("*.md")):
        if WRITE_OR_EDIT_ITEM.search(_tools_line(path)):
            holders.append(path.name)
    return holders


def test_implementer_profile_exists_with_write_item() -> None:
    path = AGENTS / "implementer_agent.md"
    assert path.is_file(), "implementer_agent.md must exist (F-021-A2 close)"
    tools = _tools_line(path)
    assert WRITE_OR_EDIT_ITEM.search(tools), tools
    text = path.read_text(encoding="utf-8")
    assert re.search(r"^name:\s*implementer-agent\s*$", text, re.MULTILINE)
    assert re.search(r"^tier:\s*author\s*$", text, re.MULTILINE)
    assert re.search(r"^model:\s*sonnet\s*$", text, re.MULTILINE)


def test_devops_tools_have_no_write_or_edit_item() -> None:
    tools = _tools_line(AGENTS / "devops_agent.md")
    assert not WRITE_OR_EDIT_ITEM.search(tools), tools
    assert re.search(r"(^|[ ,])Bash([ ,]|$)", tools), tools


def test_f021_a2_recipe_includes_implementer_excludes_devops() -> None:
    holders = _write_holders()
    assert "implementer_agent.md" in holders
    assert "devops_agent.md" not in holders
    assert len(holders) == 8, holders


def test_substring_grep_write_is_not_the_recipe() -> None:
    """Document the false-positive forms the finding warns against."""
    # TodoWrite on principal must not satisfy WRITE_OR_EDIT_ITEM.
    tools = _tools_line(AGENTS / "principal_agent.md")
    assert "TodoWrite" in tools
    assert not WRITE_OR_EDIT_ITEM.search(tools)
