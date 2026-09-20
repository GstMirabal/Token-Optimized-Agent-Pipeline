"""Tests for scripts/cursor_adapter.py (Sprint 039 C2 + Sprint 040 I2)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import cursor_adapter as ca  # noqa: E402


def test_commands_stale_true_when_dest_digest_mismatch(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    cmds = root / "commands"
    dest = root / ".cursor" / "commands"
    cmds.mkdir(parents=True)
    dest.mkdir(parents=True)
    src_body = "---\ndescription: test\n---\nRun `foo`.\n"
    (cmds / "start.md").write_text(src_body, encoding="utf-8")
    (dest / "start.md").write_text("stale content\n", encoding="utf-8")
    assert ca.commands_stale(root, nucleus=True) is True


def test_commands_stale_false_after_expected_render(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    cmds = root / "commands"
    dest = root / ".cursor" / "commands"
    cmds.mkdir(parents=True)
    dest.mkdir(parents=True)
    src_body = "---\ndescription: test\n---\nRun `foo`.\n"
    (cmds / "start.md").write_text(src_body, encoding="utf-8")
    rendered = ca.expected_cursor_command_text(src_body, nucleus=True)
    (dest / "start.md").write_text(rendered, encoding="utf-8")
    assert ca.commands_stale(root, nucleus=True) is False


def test_prune_dir_removes_orphan_keeps_expected(tmp_path: Path) -> None:
    directory = tmp_path / "commands"
    directory.mkdir()
    keep = directory / "keep.md"
    orphan = directory / "orphan.md"
    keep.write_text("ok\n", encoding="utf-8")
    orphan.write_text("gone\n", encoding="utf-8")
    ca._prune_dir(directory, expected_names={"keep.md"}, suffix=".md")
    assert keep.is_file()
    assert not orphan.exists()


def test_install_cursor_bridge_preserves_cursor_root_sentinel(
    tmp_path: Path,
) -> None:
    """Incremental install must not rmtree ``.cursor/`` (Sprint 040)."""
    root = tmp_path / "repo"
    cursor = root / ".cursor"
    cursor.mkdir(parents=True)
    sentinel = cursor / "SENTINEL"
    sentinel.write_text("keep\n", encoding="utf-8")
    orphan = cursor / "commands" / "orphan_should_go.md"
    orphan.parent.mkdir(parents=True)
    orphan.write_text("orphan\n", encoding="utf-8")
    ca.install_cursor_bridge(root, nucleus=True)
    assert sentinel.is_file()
    assert sentinel.read_text(encoding="utf-8") == "keep\n"
    assert not orphan.exists()
    assert (cursor / "commands").is_dir()


def test_install_permission_error_uses_stable_prefix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def boom(_cursor_dir: Path, *, nucleus: bool) -> set[str]:
        raise PermissionError("simulated")

    monkeypatch.setattr(ca, "_write_commands", boom)
    with pytest.raises(PermissionError) as excinfo:
        ca.install_cursor_bridge(tmp_path / "repo", nucleus=True)
    assert str(excinfo.value).startswith("bridge: permission denied on .cursor")


def test_render_rewrites_the_tool_token_for_cursor() -> None:
    """The Cursor copy claims the anchor as Cursor; the source is for Claude.

    `commands/` is one source mirrored asymmetrically - Claude symlinks it,
    Cursor gets a rendered copy - so the harness-specific value is produced
    here. Before Sprint 041 the source hardcoded `--tool cursor` and both
    harnesses read it, so a Claude Code session claimed the anchor as Cursor.
    """
    src = "---\nd: x\n---\nRun `session_start.py --boot --tool claude-code`.\n"
    rendered = ca.expected_cursor_command_text(src, nucleus=True)
    assert "--tool cursor" in rendered
    assert "--tool claude-code" not in rendered


def test_render_leaves_other_tool_values_alone() -> None:
    """Only the Claude token is rewritten; terminal and cursor pass through."""
    for value in ("--tool terminal", "--tool cursor"):
        src = f"---\nd: x\n---\nRun `session_start.py --boot {value}`.\n"
        assert value in ca.expected_cursor_command_text(src, nucleus=True)


def test_shipped_start_command_carries_the_claude_token() -> None:
    """The source of record must be the Claude form, or the symlink is wrong.

    Claude reads `commands/start.md` through a symlink, so whatever the source
    says is what a Claude session runs. There is no render step on that side.
    """
    src = (SCRIPTS.parent / "commands" / "start.md").read_text(encoding="utf-8")
    assert "--tool claude-code" in src
    assert "--tool cursor" in ca.expected_cursor_command_text(src, nucleus=True)


# --- F-049-1: profile parity under Cursor (D2/D3) -----------------------


def _make_profile(
    root: Path, *, rule_triggers: bool = True, rule_frontmatter: bool = False
) -> Path:
    """A minimal profile pack: one agent, one rule, one unmirrorable skill."""
    profile = root / "profile"
    agents = profile / "agents"
    agents.mkdir(parents=True)
    (agents / "domain_specialist_example.md").write_text(
        "---\nname: domain_specialist_example\ndescription: Example domain agent\n"
        "tools: Read, Grep\n---\nDomain specialist prompt body.\n",
        encoding="utf-8",
    )
    rules = profile / "rules"
    rules.mkdir(parents=True)
    if rule_frontmatter:
        (rules / "domain_example_standard.md").write_text(
            "---\ndescription: fallback trigger\nglobs: **/*.py\n---\n"
            "# Rule: Domain Example Standard\nBody text.\n",
            encoding="utf-8",
        )
    else:
        (rules / "domain_example_standard.md").write_text(
            "# Rule: Domain Example Standard\nBody text.\n", encoding="utf-8"
        )
    if rule_triggers:
        (profile / "rule_triggers.json").write_text(
            json.dumps(
                {
                    "rules": [
                        {
                            "path": "rules/domain_example_standard.md",
                            "globs": ["**/*.py"],
                            "trigger_prose": "Domain example trigger.",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
    skills = profile / "skills" / "example-api-bridge-3rd"
    skills.mkdir(parents=True)
    (skills / "SKILL.md").write_text("skill body\n", encoding="utf-8")
    return profile


def test_write_agents_default_source_still_renders_core_agents(
    tmp_path: Path,
) -> None:
    """The no-arg call still renders the nucleus's own agents/, not a profile's."""
    cursor_dir = tmp_path / "repo" / ".cursor"
    names = ca._write_agents(cursor_dir)
    assert "principal-agent.md" in names
    assert "domain_specialist_example.md" not in names


def test_write_agents_reads_from_override_source(tmp_path: Path) -> None:
    profile = _make_profile(tmp_path)
    cursor_dir = tmp_path / "repo" / ".cursor"
    names = ca._write_agents(cursor_dir, agents_src=profile / "agents")
    assert names == {"domain_specialist_example.md"}
    assert (cursor_dir / "agents" / "domain_specialist_example.md").is_file()


def test_write_profile_rules_primary_uses_own_rule_triggers_json(
    tmp_path: Path,
) -> None:
    profile = _make_profile(tmp_path, rule_triggers=True)
    cursor_dir = tmp_path / "repo" / ".cursor"
    names = ca._write_profile_rules(cursor_dir, profile)
    assert names == {"domain_example_standard.mdc"}
    rendered = (cursor_dir / "rules" / "domain_example_standard.mdc").read_text(
        encoding="utf-8"
    )
    assert "description: Domain example trigger." in rendered
    assert "globs: **/*.py" in rendered
    assert "alwaysApply: false" in rendered


def test_write_profile_rules_fallback_uses_rule_frontmatter(
    tmp_path: Path,
) -> None:
    """No rule_triggers.json: description/globs come from the rule file itself."""
    profile = _make_profile(tmp_path, rule_triggers=False, rule_frontmatter=True)
    cursor_dir = tmp_path / "repo" / ".cursor"
    names = ca._write_profile_rules(cursor_dir, profile)
    assert names == {"domain_example_standard.mdc"}
    rendered = (cursor_dir / "rules" / "domain_example_standard.mdc").read_text(
        encoding="utf-8"
    )
    assert "description: fallback trigger" in rendered
    assert "globs: **/*.py" in rendered
    assert "Body text." in rendered


def test_write_profile_rules_raises_named_error_when_neither_source_exists(
    tmp_path: Path,
) -> None:
    """Neither rule_triggers.json nor frontmatter: a named error, never a bare KeyError."""
    profile = _make_profile(tmp_path, rule_triggers=False, rule_frontmatter=False)
    cursor_dir = tmp_path / "repo" / ".cursor"
    with pytest.raises(ca.ProfileRuleTriggerError) as excinfo:
        ca._write_profile_rules(cursor_dir, profile)
    assert "domain_example_standard.md" in str(excinfo.value)


def test_write_profile_rules_never_defaults_to_always_apply_true(
    tmp_path: Path,
) -> None:
    """token_saver: a missing trigger must not fall back to loading every turn."""
    profile = _make_profile(tmp_path, rule_triggers=True)
    cursor_dir = tmp_path / "repo" / ".cursor"
    ca._write_profile_rules(cursor_dir, profile)
    rendered = (cursor_dir / "rules" / "domain_example_standard.mdc").read_text(
        encoding="utf-8"
    )
    assert "alwaysApply: true" not in rendered


def test_profile_skill_names_returns_sorted_directory_names(tmp_path: Path) -> None:
    profile = _make_profile(tmp_path)
    assert ca._profile_skill_names(profile) == ["example-api-bridge-3rd"]


def test_profile_skill_names_empty_when_no_skills_dir(tmp_path: Path) -> None:
    profile = tmp_path / "profile"
    profile.mkdir()
    assert ca._profile_skill_names(profile) == []


def test_install_cursor_bridge_with_profile_renders_agent_and_rule(
    tmp_path: Path,
) -> None:
    """F-049-1 regression: --target cursor + a profile must not drop it silently."""
    profile = _make_profile(tmp_path)
    host = tmp_path / "host"
    ca.install_cursor_bridge(host, nucleus=False, profile_dir=profile)
    assert (host / ".cursor" / "agents" / "domain_specialist_example.md").is_file()
    assert (host / ".cursor" / "rules" / "domain_example_standard.mdc").is_file()


def test_install_cursor_bridge_with_profile_prints_unmirrored_skills(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Skills have no Cursor destination: named on stdout, not dropped without a trace."""
    profile = _make_profile(tmp_path)
    host = tmp_path / "host"
    ca.install_cursor_bridge(host, nucleus=False, profile_dir=profile)
    captured = capsys.readouterr()
    assert "example-api-bridge-3rd" in captured.out
    assert "no skills/ destination" in captured.out


def test_install_cursor_bridge_without_profile_prints_nothing_about_skills(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The default call (no profile_dir) is unaffected — no skills message at all."""
    host = tmp_path / "host"
    ca.install_cursor_bridge(host, nucleus=True)
    captured = capsys.readouterr()
    assert "skills/ destination" not in captured.out


def test_install_cursor_bridge_core_agents_survive_a_profile_install(
    tmp_path: Path,
) -> None:
    """Profile agents are additive: the core 14 framework agents are not pruned."""
    profile = _make_profile(tmp_path)
    host = tmp_path / "host"
    ca.install_cursor_bridge(host, nucleus=True, profile_dir=profile)
    core_agent = host / ".cursor" / "agents" / "principal-agent.md"
    assert core_agent.is_file()
    assert (host / ".cursor" / "agents" / "domain_specialist_example.md").is_file()


def test_example_project_profile_fixture_matches_the_primary_cascade_rung(
    tmp_path: Path,
) -> None:
    """profiles/example-project/rule_triggers.json (U3) must satisfy the primary D3 rung."""
    real_profile = SCRIPTS.parent / "profiles" / "example-project"
    cursor_dir = tmp_path / "repo" / ".cursor"
    names = ca._write_profile_rules(cursor_dir, real_profile)
    assert names == {"domain_example_standard.mdc"}
    rendered = (cursor_dir / "rules" / "domain_example_standard.mdc").read_text(
        encoding="utf-8"
    )
    assert "alwaysApply: false" in rendered
