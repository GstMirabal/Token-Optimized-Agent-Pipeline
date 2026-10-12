"""Guards the sandbox invariants of the template claude/settings.hooks.json
(Sprint 055, R2-9). The template is merged into every host's Claude Code
configuration by install.py, so a loosened sandbox entry ships to all hosts.

Pinned invariants (Sprint 055, Amendment 2, D12/D13; Sprint 056, D12): no
sandbox.excludedCommands entry at all; the whole .agents submodule and .env are
write-denied both in the sandbox filesystem and in permissions.deny, by one
whole-tree entry each rather than per-subtree entries; .env stays unreadable;
no allowMachLookup."""
import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "claude" / "settings.hooks.json"


@pytest.fixture(scope="module")
def template() -> dict[str, Any]:
    """Load the settings template.

    Returns:
        The parsed JSON of claude/settings.hooks.json.
    """
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def _excluded(template: dict[str, Any]) -> list[str]:
    """Return the sandbox.excludedCommands entries of the template.

    Args:
        template: Parsed settings template.

    Returns:
        The list of excluded command patterns.
    """
    return template["sandbox"].get("excludedCommands", [])


def _fs(template: dict[str, Any]) -> dict[str, list[str]]:
    """Return the sandbox.filesystem block of the template.

    Args:
        template: Parsed settings template.

    Returns:
        The filesystem mapping.
    """
    return template["sandbox"]["filesystem"]


def test_excluded_commands_absent_or_empty(template: dict[str, Any]) -> None:
    """sandbox.excludedCommands must be absent or empty.

    On CLI 2.1.119 a compound command whose first part matches any excluded
    entry runs wholly unsandboxed, so one entry exempts everything chained
    after it (QA Gate 1 round 3, N1). This single invariant replaces the
    per-entry with_env / gh-create / broad-pattern checks.
    """
    assert _excluded(template) == []


def test_deny_write_is_whole_submodule_and_env(template: dict[str, Any]) -> None:
    """denyWrite is exactly the whole submodule plus .env (Sprint 056, D12).

    The per-subtree list left `.agents/_mode.py`, `mcp_servers/`, `agents/` and
    the `Makefile` writable although hooks and MCP launchers load them outside
    the sandbox (SANDBOX_ENUMERATION.md Q1, Q3, Q4, Q5); one `./.agents` entry
    closes the class instead of one vector.
    """
    assert _fs(template)["denyWrite"] == ["./.agents", "./.env"]


def test_no_narrower_agents_deny_write(template: dict[str, Any]) -> None:
    """No `./.agents/...` subtree entry remains: `./.agents` subsumes it, so it is dead and misleading."""
    narrower = [p for p in _fs(template)["denyWrite"] if p.startswith("./.agents/")]
    assert narrower == []


@pytest.mark.parametrize("rule", ["Edit(/.agents/**)", "Edit(/.env)", "Read(/.env)"])
def test_permissions_deny_rules(template: dict[str, Any], rule: str) -> None:
    """The permissions.deny rules guarding the submodule and .env stay present.

    Hooks run outside the sandbox and execute or merge files of the submodule,
    so an agent able to Edit them could run arbitrary code unsandboxed (N3).
    """
    assert rule in template["permissions"]["deny"]


def test_no_narrower_agents_edit_deny(template: dict[str, Any]) -> None:
    """Only `Edit(/.agents/**)` names the submodule; per-subtree Edit rules are subsumed and dead."""
    edits = [r for r in template["permissions"]["deny"] if r.startswith("Edit(/.agents/")]
    assert edits == ["Edit(/.agents/**)"]


@pytest.mark.parametrize("path", ["./.env", "./.env.*"])
def test_deny_read_env(template: dict[str, Any], path: str) -> None:
    """.env and its variants stay unreadable inside the sandbox."""
    assert path in _fs(template)["denyRead"]


@pytest.mark.parametrize("path", ["./.env.example", "./.env.sample", "./.env.template"])
def test_allow_read_env_templates(template: dict[str, Any], path: str) -> None:
    """Non-secret .env templates stay readable (revised D4)."""
    assert path in _fs(template)["allowRead"]


def test_no_allow_mach_lookup(template: dict[str, Any]) -> None:
    """allowMachLookup fails open on CLI 2.1.119 (SANDBOX_MEASUREMENT.md section 4)."""
    assert "allowMachLookup" not in template["sandbox"].get("network", {})
