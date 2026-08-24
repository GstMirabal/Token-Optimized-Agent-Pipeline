"""Generate the Cursor bridge from framework sources.

Imported by scripts/install.py when ``--target`` is ``cursor`` or ``both``.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCRIPT_DIR.parent
RULE_TRIGGERS_PATH = AGENTS_DIR / "config" / "rule_triggers.json"
MCP_TEMPLATE = AGENTS_DIR / "claude" / "mcp.json"
CONSTITUTION_RULE = "00-constitution.mdc"


def _load_rule_triggers() -> dict[str, dict]:
    data = json.loads(RULE_TRIGGERS_PATH.read_text(encoding="utf-8"))
    return {entry["path"]: entry for entry in data["rules"]}


def _globs_for_mdc(patterns: list[str]) -> str:
    return ", ".join(patterns)


def _constitution_import(*, nucleus: bool) -> str:
    return "@agents.md" if nucleus else "@.agents/agents.md"


def _rewrite_command_body(body: str, *, nucleus: bool) -> str:
    if nucleus:
        return body.replace("@.agents/", "@")
    return body


def _write_commands(cursor_dir: Path, *, nucleus: bool) -> None:
    commands_dir = cursor_dir / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted((AGENTS_DIR / "commands").glob("*.md")):
        text = src.read_text(encoding="utf-8")
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                front = parts[1]
                body = _rewrite_command_body(parts[2].lstrip("\n"), nucleus=nucleus)
                text = f"---{front}---\n{body}"
        (commands_dir / src.name).write_text(text, encoding="utf-8")


def _write_rules(cursor_dir: Path) -> None:
    rules_dir = cursor_dir / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    triggers = _load_rule_triggers()
    for src in sorted((AGENTS_DIR / "rules").glob("*.md")):
        key = f"rules/{src.name}"
        trigger = triggers[key]
        body = src.read_text(encoding="utf-8")
        description = trigger["trigger_prose"].replace('"', "'")
        globs = _globs_for_mdc(trigger["globs"])
        frontmatter = (
            "---\n"
            f"description: {description}\n"
            f"globs: {globs}\n"
            "alwaysApply: false\n"
            "---\n"
        )
        (rules_dir / f"{src.stem}.mdc").write_text(frontmatter + body, encoding="utf-8")


def _write_constitution(cursor_dir: Path, *, nucleus: bool) -> None:
    rules_dir = cursor_dir / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    import_line = _constitution_import(nucleus=nucleus)
    text = (
        "---\n"
        "alwaysApply: true\n"
        "---\n\n"
        f"Follow the framework constitution at {import_line} for every session.\n"
    )
    (rules_dir / CONSTITUTION_RULE).write_text(text, encoding="utf-8")


def _write_mcp(cursor_dir: Path) -> None:
    cursor_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(MCP_TEMPLATE, cursor_dir / "mcp.json")


def install_cursor_bridge(host_dir: Path, *, nucleus: bool) -> None:
    """Materialize ``.cursor/`` for ``host_dir`` (nucleus or host checkout).

    Args:
        host_dir: Repository root receiving ``.cursor/``.
        nucleus: When True, rewrite ``@.agents/`` paths for the nucleus layout.
    """
    cursor_dir = host_dir / ".cursor"
    if cursor_dir.exists():
        shutil.rmtree(cursor_dir)
    _write_commands(cursor_dir, nucleus=nucleus)
    _write_rules(cursor_dir)
    _write_constitution(cursor_dir, nucleus=nucleus)
    _write_mcp(cursor_dir)
    print(f"✅ Cursor bridge written under {cursor_dir}")
