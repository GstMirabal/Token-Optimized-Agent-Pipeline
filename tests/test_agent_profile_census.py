"""Pin agent profile census against agents/*.md (Sprint 036 M6).

Five mechanical asserts over the 14 nucleus profiles (not profiles/ examples):
gate-tier profiles must not hold Write/Edit; qa/tester need Bash;
orchestrator needs Write; frontmatter ``name:`` kebab matches stem;
count equals 14.

invoked_by: pytest tests/.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
TIERS_FILE = ROOT / "config" / "model_tiers.json"
EXPECTED_PROFILE_COUNT = 14

WRITE_OR_EDIT_ITEM = re.compile(r"(^|[ ,])(Write|Edit)([ ,]|$)")
BASH_ITEM = re.compile(r"(^|[ ,])Bash([ ,]|$)")
WRITE_ITEM = re.compile(r"(^|[ ,])Write([ ,]|$)")


def _parse_frontmatter(path: Path) -> dict[str, str]:
    """Return key → value for YAML frontmatter between --- delimiters."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def load_gate_profiles() -> list[str]:
    """Gate-tier profile stems from ``config/model_tiers.json`` → ``tiers.gate.profiles``."""
    tiers = json.loads(TIERS_FILE.read_text(encoding="utf-8"))
    return list(tiers["tiers"]["gate"]["profiles"])


def agent_paths() -> list[Path]:
    return sorted(AGENTS.glob("*.md"))


def run_census(paths: list[Path] | None = None) -> list[str]:
    """Collect every census violation; empty list means pass."""
    problems: list[str] = []
    paths = paths if paths is not None else agent_paths()

    if len(paths) != EXPECTED_PROFILE_COUNT:
        problems.append(
            f"agents/*.md count is {len(paths)}, expected {EXPECTED_PROFILE_COUNT}"
        )

    profiles_by_stem = {path.stem: path for path in paths}
    gate_profiles = load_gate_profiles()

    for stem in gate_profiles:
        path = profiles_by_stem.get(stem)
        if path is None:
            problems.append(f"{stem}: listed in tiers.gate.profiles but no agents/{stem}.md")
            continue
        tools_line = _parse_frontmatter(path).get("tools", "")
        if WRITE_OR_EDIT_ITEM.search(tools_line):
            problems.append(f"{stem}: gate profile must not declare Write or Edit in tools")

    for stem in ("qa_agent", "tester_agent"):
        path = profiles_by_stem.get(stem)
        if path is None:
            continue
        tools_line = _parse_frontmatter(path).get("tools", "")
        if not BASH_ITEM.search(tools_line):
            problems.append(f"{stem}: qa/tester profiles must include Bash in tools")

    orchestrator = profiles_by_stem.get("orchestrator")
    if orchestrator is not None:
        tools_line = _parse_frontmatter(orchestrator).get("tools", "")
        if not WRITE_ITEM.search(tools_line):
            problems.append("orchestrator: author profile must include Write in tools")

    for path in paths:
        name = _parse_frontmatter(path).get("name")
        expected = path.stem.replace("_", "-")
        if name != expected:
            problems.append(
                f"{path.name}: frontmatter name `{name}` != kebab stem `{expected}`"
            )

    return problems


def test_agent_profile_count_is_fourteen() -> None:
    assert len(agent_paths()) == EXPECTED_PROFILE_COUNT


def test_gate_profiles_loaded_from_model_tiers() -> None:
    gate = load_gate_profiles()
    assert gate == ["qa_agent", "tester_agent", "principal_agent"]


def test_gate_profiles_have_no_write_or_edit() -> None:
    profiles_by_stem = {path.stem: path for path in agent_paths()}
    for stem in load_gate_profiles():
        path = profiles_by_stem[stem]
        tools_line = _parse_frontmatter(path).get("tools", "")
        assert not WRITE_OR_EDIT_ITEM.search(tools_line), (
            f"{stem} gate profile must not hold Write/Edit: {tools_line}"
        )


def test_qa_and_tester_have_bash() -> None:
    for stem in ("qa_agent", "tester_agent"):
        path = AGENTS / f"{stem}.md"
        tools_line = _parse_frontmatter(path).get("tools", "")
        assert BASH_ITEM.search(tools_line), f"{stem} must include Bash: {tools_line}"


def test_orchestrator_has_write() -> None:
    tools_line = _parse_frontmatter(AGENTS / "orchestrator.md").get("tools", "")
    assert WRITE_ITEM.search(tools_line), f"orchestrator must include Write: {tools_line}"


def test_frontmatter_name_kebab_matches_stem() -> None:
    for path in agent_paths():
        name = _parse_frontmatter(path).get("name")
        expected = path.stem.replace("_", "-")
        assert name == expected, f"{path.name}: name `{name}` != `{expected}`"


def test_census_passes() -> None:
    problems = run_census()
    assert problems == [], "\n".join(problems)


def test_write_on_qa_agent_would_fail_census(tmp_path: Path) -> None:
    """Regression guard: adding Write to qa_agent must fail the census."""
    fake_agents = tmp_path / "agents"
    fake_agents.mkdir()
    for path in agent_paths():
        (fake_agents / path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    qa_path = fake_agents / "qa_agent.md"
    text = qa_path.read_text(encoding="utf-8")
    qa_path.write_text(
        text.replace("tools: Read, Glob, Grep, Bash", "tools: Read, Glob, Grep, Bash, Write"),
        encoding="utf-8",
    )

    problems = run_census(sorted(fake_agents.glob("*.md")))
    assert any("qa_agent" in problem and "Write" in problem for problem in problems)
