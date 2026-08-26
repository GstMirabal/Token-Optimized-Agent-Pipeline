"""Generate the Cursor bridge from framework sources.

Imported by scripts/install.py when ``--target`` is ``cursor`` or ``both``.

Rule ``.mdc`` frontmatter contract (measured once in Sprint 026 ``P4.0``;
absorbed here by ``A3.1`` so the sprint directory carries no tool-probe
receipt). Only these keys are emitted:

* ``description`` — string (agent-selected rules)
* ``globs`` — comma-separated string, not a YAML list
* ``alwaysApply`` — lowercase boolean

Nucleus entry point: ``00-constitution.mdc`` with ``alwaysApply: true``
importing ``agents.md``. Do not add a root ``AGENTS.md`` beside
``agents.md`` on case-insensitive filesystems (``P4.0b``).

Subagent files under ``.cursor/agents/`` follow the Cursor contract
(https://cursor.com/docs/subagents): ``name``, ``description``, ``model``,
``readonly``, ``is_background``. ``model`` is always ``inherit`` — Task
applies ``config/model_tiers.json`` (ADR-0010). Claude-only keys
(``tools``, ``tier``) are not copied.
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
CHAT_TITLE_RULE = "01-chat-title.mdc"
# Keys emitted in rule frontmatter; keep in sync with the module docstring.
MDC_RULE_FRONTMATTER_KEYS = ("description", "globs", "alwaysApply")
CURSOR_AGENT_FRONTMATTER_KEYS = (
    "name",
    "description",
    "model",
    "readonly",
    "is_background",
)


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
        fields = {
            "description": description,
            "globs": globs,
            "alwaysApply": "false",
        }
        if tuple(fields) != MDC_RULE_FRONTMATTER_KEYS:
            raise RuntimeError("rule frontmatter keys drifted from MDC_RULE_FRONTMATTER_KEYS")
        frontmatter = (
            "---\n"
            + "".join(f"{key}: {value}\n" for key, value in fields.items())
            + "---\n"
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


def _write_chat_title_rule(cursor_dir: Path) -> None:
    """Emit the standing chat-tab rule. Regenerated on every Cursor install."""
    rules_dir = cursor_dir / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    text = (
        "---\n"
        "description: Rename the chat tab to the git branches that acted in this conversation\n"
        "alwaysApply: true\n"
        "---\n\n"
        "# Chat title = sprint branches\n\n"
        "Standing request for this repository: the chat tab MUST name the git "
        "branches that acted in the conversation. Treat that as an explicit "
        "`rename_chat` request at session start and after every checkout that "
        "changes `HEAD`.\n\n"
        "| When | Title |\n"
        "| :--- | :--- |\n"
        "| One sprint branch | that name (`ai-sprint/034`) |\n"
        "| Several sprint branches in this chat | join with ` · ` in first-seen order |\n"
        "| Generic titles (`Chat`, `Chat initialization`, New chat) | replace immediately |\n\n"
        "Do not put `main` in the title unless this conversation committed to "
        "`main`. Confirm the current name with `git branch --show-current`.\n"
    )
    (rules_dir / CHAT_TITLE_RULE).write_text(text, encoding="utf-8")


def _split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return YAML-ish keys from the first frontmatter block, plus the body."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, parts[2].lstrip("\n")


def _tools_allow_write(tools: str) -> bool:
    tokens = {item.strip() for item in tools.split(",") if item.strip()}
    return bool(tokens & {"Write", "Edit"})


def _cursor_agent_document(src_text: str) -> str:
    """Render one nucleus profile as a Cursor subagent file."""
    fields, body = _split_frontmatter(src_text)
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name or not description or not body.strip():
        raise ValueError(
            "Cursor subagents require name, description, and a non-empty prompt body"
        )
    readonly = "false" if _tools_allow_write(fields.get("tools", "")) else "true"
    emitted = {
        "name": name,
        "description": description,
        "model": "inherit",
        "readonly": readonly,
        "is_background": "false",
    }
    if tuple(emitted) != CURSOR_AGENT_FRONTMATTER_KEYS:
        raise RuntimeError("agent frontmatter keys drifted from CURSOR_AGENT_FRONTMATTER_KEYS")
    front = "---\n" + "".join(f"{key}: {value}\n" for key, value in emitted.items()) + "---\n"
    return f"{front}\n{body}"


def _write_agents(cursor_dir: Path) -> None:
    dest = cursor_dir / "agents"
    dest.mkdir(parents=True, exist_ok=True)
    for src in sorted((AGENTS_DIR / "agents").glob("*.md")):
        rendered = _cursor_agent_document(src.read_text(encoding="utf-8"))
        name = _split_frontmatter(rendered)[0]["name"]
        (dest / f"{name}.md").write_text(rendered, encoding="utf-8")


def _rewrite_mcp_value(value: str, *, nucleus: bool) -> str:
    if not nucleus:
        return value
    if value.startswith(".agents/"):
        return value[len(".agents/") :]
    return value


def _rewrite_mcp_config(data: dict, *, nucleus: bool) -> dict:
    if not nucleus:
        return data
    rewritten = json.loads(json.dumps(data))
    for server in rewritten.get("mcpServers", {}).values():
        if "command" in server:
            server["command"] = _rewrite_mcp_value(server["command"], nucleus=nucleus)
        if "args" in server:
            server["args"] = [
                _rewrite_mcp_value(arg, nucleus=nucleus) if isinstance(arg, str) else arg
                for arg in server["args"]
            ]
    return rewritten


def _write_mcp(cursor_dir: Path, *, nucleus: bool) -> None:
    cursor_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(MCP_TEMPLATE.read_text(encoding="utf-8"))
    data = _rewrite_mcp_config(data, nucleus=nucleus)
    (cursor_dir / "mcp.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


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
    _write_chat_title_rule(cursor_dir)
    _write_agents(cursor_dir)
    _write_mcp(cursor_dir, nucleus=nucleus)
    print(f"✅ Cursor bridge written under {cursor_dir}")
