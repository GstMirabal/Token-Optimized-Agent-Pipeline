"""Guards the sandbox invariants of the template claude/settings.hooks.json
(Sprint 055, R2-9). The template is merged into every host's Claude Code
configuration by install.py, so a loosened sandbox entry ships to all hosts."""
import json
import re
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "claude" / "settings.hooks.json"

BROAD_EXCLUSIONS = {"gh *", "git *", "pnpm *"}


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


def test_no_with_env_exclusion_in_template(template: dict[str, Any]) -> None:
    """Absolute with_env.py exclusions are rendered per machine by install.py."""
    offenders = [e for e in _excluded(template) if "with_env.py" in e]
    assert offenders == []


def test_no_gh_create_exclusion(template: dict[str, Any]) -> None:
    """gh pr/release create read local files and must not run unsandboxed."""
    offenders = [e for e in _excluded(template) if re.match(r"^gh (pr|release) create", e)]
    assert offenders == []


def test_no_broad_tool_exclusions(template: dict[str, Any]) -> None:
    """No tool-wide exclusion and no bare wildcard after gh api (D7)."""
    entries = _excluded(template)
    broad = [e for e in entries if e.strip() in BROAD_EXCLUSIONS]
    gh_api_wild = [e for e in entries if e.startswith("gh api") and e.endswith("*")]
    assert broad == []
    assert gh_api_wild == []


@pytest.mark.parametrize(
    "path",
    [
        "./.agents/scripts/with_env.py",
        "./.agents/config/with_env_allowlist.json",
        "./.agents/venv_skillopt",
        "./.env",
    ],
)
def test_deny_write_paths(template: dict[str, Any], path: str) -> None:
    """The wrapper, its allowlist, the venv and .env stay write-denied."""
    assert path in _fs(template)["denyWrite"]


@pytest.mark.parametrize(
    "rule",
    [
        "Edit(/.agents/scripts/with_env.py)",
        "Edit(/.agents/config/with_env_allowlist.json)",
        "Edit(/.env)",
        "Read(/.env)",
    ],
)
def test_permissions_deny_rules(template: dict[str, Any], rule: str) -> None:
    """The permissions.deny rules guarding the wrapper and .env stay present."""
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
