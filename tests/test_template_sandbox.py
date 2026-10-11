"""Guards the sandbox invariants of the template claude/settings.hooks.json
(Sprint 055, R2-9). The template is merged into every host's Claude Code
configuration by install.py, so a loosened sandbox entry ships to all hosts.

Pinned invariants (Sprint 055, Amendment 2, D12/D13): no sandbox.excludedCommands
entry at all; framework trees and the secret files are write-denied both in the
sandbox filesystem and in permissions.deny; .env stays unreadable; no
allowMachLookup."""
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


@pytest.mark.parametrize(
    "path",
    [
        "./.agents/hooks",
        "./.agents/scripts",
        "./.agents/config",
        "./.agents/skills",
        "./.agents/claude",
        "./.agents/venv_skillopt",
        "./.agents/scripts/with_env.py",
        "./.agents/config/with_env_allowlist.json",
        "./.env",
    ],
)
def test_deny_write_paths(template: dict[str, Any], path: str) -> None:
    """Framework trees, the wrapper, its allowlist, the venv and .env stay write-denied."""
    assert path in _fs(template)["denyWrite"]


@pytest.mark.parametrize(
    "rule",
    [
        "Edit(/.agents/hooks/**)",
        "Edit(/.agents/scripts/**)",
        "Edit(/.agents/config/**)",
        "Edit(/.agents/skills/**)",
        "Edit(/.agents/claude/**)",
        "Edit(/.agents/scripts/with_env.py)",
        "Edit(/.agents/config/with_env_allowlist.json)",
        "Edit(/.env)",
        "Read(/.env)",
    ],
)
def test_permissions_deny_rules(template: dict[str, Any], rule: str) -> None:
    """The permissions.deny rules guarding framework trees and .env stay present.

    Hooks run outside the sandbox and execute or merge these trees, so an
    agent able to Edit them could run arbitrary code unsandboxed (N3).
    """
    assert rule in template["permissions"]["deny"]


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
