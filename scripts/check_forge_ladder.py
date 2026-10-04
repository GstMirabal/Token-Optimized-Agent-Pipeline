"""Deterministic check of Phase 4.1/4.2 agent and skill forge fallback.

Parses ``agent_assignment.md`` and ``skill_assignment.md`` under ``--sprint-dir``.
Forge rows must land on the legal destination for the session mode
(``_mode.is_nucleus``): host → ``host:.claude/agents/`` (or host skills);
nucleus create → ``nucleus:PR`` under ``agents/``. P3 skill lookup is a
simulated artifact registration only — this script never opens a network
client.

invoked_by: workflows/pipeline_workflow.md Phases 4.1 and 4.2.

Usage:
    python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/033-core-pipeline

Exit codes:
    0 — no forge-relevant rows, or every forge row has a legal destination
        and the forged file exists on disk
    2 — empty destination, submodule contamination, missing forged file,
        host destination on nucleus without ``.claude/agents/``, or a skill
        forge claim without a P3 miss trail (RA-11: only 2 blocks)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mode import is_nucleus
from _root import agents_root

FORGE_HOST = "host:.claude/agents/"
FORGE_NUCLEUS = "nucleus:PR"
AGENT_TARGET_RE = re.compile(
    r"(?:^|/)(?:\.agents/)?(?:\.claude/)?agents/([^/]+\.md)$"
)
P3_MISS_RE = re.compile(
    r"\{[^{}]*source\s*[:=]\s*skills\.sh[^{}]*hit\s*[:=]\s*false[^{}]*\}"
    r"|\{[^{}]*\"source\"\s*:\s*\"skills\.sh\"[^{}]*\"hit\"\s*:\s*false[^{}]*\}",
    re.IGNORECASE | re.DOTALL,
)
NO_SKILL_FORGED_RE = re.compile(
    r"No skill was forged|No new skill forged", re.IGNORECASE
)
SKILL_PATH_RE = re.compile(
    r"(?:\.claude|\.agents)/skills/([A-Za-z0-9_-]+)/(?:SKILL\.md)?"
)
P_MISS_TRAIL_RE = re.compile(
    r"\bP[1-4]\b[^\n]{0,80}\bmiss\b|\bmiss\b[^\n]{0,80}\bP[1-4]\b",
    re.IGNORECASE,
)


def _cells(line: str) -> list[str]:
    return [part.strip().strip("`") for part in line.strip().strip("|").split("|")]


def _is_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and set(stripped) <= set("|:- ")


def _is_table_start(line: str) -> bool:
    """True when `line` opens a markdown table (a pipe row, not a separator).

    Args:
        line: One raw line from the source document.
    """
    return line.strip().startswith("|") and not _is_separator(line)


def _collect_rows(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    """Collect table body rows from `lines[start]`, skipping separator lines.

    Args:
        lines: full document, split into lines.
        start: index of the first line to consider as a body row.

    Returns:
        tuple: `(rows, next_index)` — `next_index` is the first line index
            after the last consecutive `|`-prefixed line.
    """
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        if not _is_separator(lines[index]):
            rows.append(_cells(lines[index]))
        index += 1
    return rows, index


def _parse_table_at(
    lines: list[str], index: int
) -> tuple[tuple[list[str], list[list[str]]], int]:
    """Parse one table starting at `lines[index]` (already confirmed a start).

    Args:
        lines: full document, split into lines.
        index: index of the table's header line.

    Returns:
        tuple: `((header, rows), next_index)` — `next_index` is where the
            caller should resume scanning after this table.
    """
    header = _cells(lines[index])
    index += 1
    if index < len(lines) and _is_separator(lines[index]):
        index += 1
    rows, index = _collect_rows(lines, index)
    return (header, rows), index


def _tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    tables: list[tuple[list[str], list[list[str]]]] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if _is_table_start(lines[index]):
            table, index = _parse_table_at(lines, index)
            tables.append(table)
            continue
        index += 1
    return tables


def _col(header: list[str], row: list[str], name: str) -> str:
    if name not in header:
        return ""
    idx = header.index(name)
    return row[idx] if idx < len(row) else ""


def host_root() -> Path:
    """Host project root: parent of the submodule, or the nucleus itself."""
    root = agents_root()
    return root if is_nucleus() else root.parent


def _agent_basename(target: str) -> str | None:
    match = AGENT_TARGET_RE.search(target.replace("\\", "/"))
    return match.group(1) if match else None


def _is_forge_destination(dest: str) -> bool:
    cleaned = dest.strip()
    if not cleaned or cleaned.upper() == "N/A":
        return False
    return cleaned in {FORGE_HOST, FORGE_NUCLEUS} or cleaned.startswith("profile:")


def _is_agent_forge_row(header: list[str], row: list[str]) -> bool:
    if "Destination" not in header or "Target" not in header:
        return False
    dest = _col(header, row, "Destination")
    target = _col(header, row, "Target")
    operation = _col(header, row, "Operation").lower()
    if _is_forge_destination(dest):
        return True
    return "create" in operation and _agent_basename(target) is not None


def _profile_path(dest: str) -> Path | None:
    if not dest.startswith("profile:"):
        return None
    rel = dest.split(":", 1)[1].strip()
    if not rel:
        return None
    return host_root() / rel


def _check_nucleus_agent(unit: str, name: str, dest: str) -> str | None:
    if not dest or dest.upper() == "N/A":
        return f"Unit {unit}: agent forge Destination is empty"
    if dest == FORGE_HOST:
        tree = host_root() / ".claude" / "agents"
        if not tree.is_dir():
            return f"Unit {unit}: {FORGE_HOST} on nucleus without .claude/agents/"
        if not (tree / name).is_file():
            return f"Unit {unit}: missing {tree / name}"
        return None
    if dest == FORGE_NUCLEUS:
        path = agents_root() / "agents" / name
        if not path.is_file():
            return f"Unit {unit}: nucleus:PR missing {path.relative_to(agents_root())}"
        return None
    profile = _profile_path(dest)
    if profile is not None:
        candidate = profile if profile.suffix == ".md" else profile / name
        if not candidate.is_file():
            return f"Unit {unit}: missing profile forge file {candidate}"
        return None
    return f"Unit {unit}: unsupported Destination {dest!r} on nucleus"


def _check_host_agent(unit: str, name: str, dest: str) -> str | None:
    host_file = host_root() / ".claude" / "agents" / name
    sub_file = agents_root() / "agents" / name
    if not dest or dest.upper() == "N/A":
        return f"Unit {unit}: agent forge Destination is empty"
    if sub_file.is_file() and not host_file.is_file():
        return f"Unit {unit}: agent forged under .agents/agents/ (contamination)"
    if dest == FORGE_HOST:
        if not host_file.is_file():
            return f"Unit {unit}: missing host forge file {host_file}"
        return None
    profile = _profile_path(dest)
    if profile is not None:
        candidate = profile if profile.suffix == ".md" else profile / name
        if not candidate.is_file():
            return f"Unit {unit}: missing profile forge file {candidate}"
        return None
    if dest == FORGE_NUCLEUS or sub_file.is_file():
        return f"Unit {unit}: agent forged under .agents/agents/ (contamination)"
    return f"Unit {unit}: host forge requires {FORGE_HOST}, got {dest!r}"


def _check_agent_row(header: list[str], row: list[str], nucleus: bool) -> str | None:
    """Validate one row already confirmed to be an agent-forge row.

    Args:
        header: table header cells.
        row: table row cells.
        nucleus: True when this session is in nucleus mode.

    Returns:
        str | None: a finding message, or None when the row is compliant.
    """
    unit = _col(header, row, "#") or "?"
    target = _col(header, row, "Target")
    dest = _col(header, row, "Destination")
    name = _agent_basename(target)
    if name is None:
        return f"Unit {unit}: forge row Target is not an agent .md"
    check = _check_nucleus_agent if nucleus else _check_host_agent
    return check(unit, name, dest)


def _findings_for_table(
    header: list[str], rows: list[list[str]], nucleus: bool
) -> list[str]:
    """Findings for every agent-forge row in one table.

    Args:
        header: table header cells.
        rows: table body rows.
        nucleus: True when this session is in nucleus mode.

    Returns:
        list[str]: one finding per non-compliant forge row.
    """
    findings: list[str] = []
    for row in rows:
        if not _is_agent_forge_row(header, row):
            continue
        finding = _check_agent_row(header, row, nucleus)
        if finding:
            findings.append(finding)
    return findings


def check_agent_assignment(text: str) -> list[str]:
    """Validate forge-relevant rows in agent_assignment.md."""
    findings: list[str] = []
    nucleus = is_nucleus()
    for header, rows in _tables(text):
        if "Destination" not in header:
            continue
        findings.extend(_findings_for_table(header, rows, nucleus))
    return findings


def _p3_miss(text: str) -> bool:
    if P3_MISS_RE.search(text):
        return True
    if P_MISS_TRAIL_RE.search(text) and "P3" in text:
        return True
    for match in re.finditer(r"\{[^{}]+\}", text):
        blob = match.group(0)
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            continue
        source = str(data.get("source", "")).lower()
        if "skills.sh" in source and data.get("hit") is False:
            return True
    return False


def _skill_names(text: str) -> list[str]:
    return list(dict.fromkeys(SKILL_PATH_RE.findall(text)))


def _skill_forge_claimed(text: str) -> bool:
    if _p3_miss(text):
        return True
    if _skill_names(text):
        return True
    return bool(re.search(r"\bP4\b[^\n]{0,60}\bforg", text, re.IGNORECASE))


def check_skill_assignment(text: str) -> list[str]:
    """Validate skill forge claims; no-op when no forge is claimed."""
    if not _skill_forge_claimed(text):
        return []
    findings: list[str] = []
    if NO_SKILL_FORGED_RE.search(text) and not _p3_miss(text):
        findings.append(
            "skill forge claimed but «No skill was forged» without P3 miss trail"
        )
        return findings
    if not _p3_miss(text):
        findings.append("skill forge claimed without P3 miss registration")
        return findings
    names = _skill_names(text)
    if not names:
        findings.append("P3 miss recorded but no skill name / SKILL.md path found")
        return findings
    for name in names:
        host_skill = host_root() / ".claude" / "skills" / name / "SKILL.md"
        sub_skill = agents_root() / "skills" / name / "SKILL.md"
        if sub_skill.is_file() and not host_skill.is_file():
            findings.append(
                f"skill {name!r} forged under .agents/skills/ (contamination)"
            )
            continue
        if not host_skill.is_file():
            findings.append(f"missing host skill file {host_skill}")
    return findings


def check(sprint_dir: Path) -> int:
    """Audit one sprint directory. Returns the process exit code."""
    agent_path = sprint_dir / "agent_assignment.md"
    skill_path = sprint_dir / "skill_assignment.md"
    findings: list[str] = []
    if agent_path.is_file():
        findings.extend(check_agent_assignment(agent_path.read_text(encoding="utf-8")))
    if skill_path.is_file():
        findings.extend(check_skill_assignment(skill_path.read_text(encoding="utf-8")))
    if not findings:
        print(f"[OK] check_forge_ladder: {sprint_dir}")
        return 0
    print(f"❌ check_forge_ladder: {sprint_dir}", file=sys.stderr)
    for item in findings:
        print(f"   • {item}", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--sprint-dir",
        type=Path,
        required=True,
        help="Canonical sprint directory holding agent/skill assignment artifacts",
    )
    args = parser.parse_args()
    sprint_dir = args.sprint_dir
    if not sprint_dir.is_absolute():
        sprint_dir = Path.cwd() / sprint_dir
    return check(sprint_dir.resolve())


if __name__ == "__main__":
    sys.exit(main())
