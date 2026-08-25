"""Tests for scripts/merge_json.py — the non-destructive merge that touches
host users' .claude/settings.json and .mcp.json. A regression here corrupts
real user configuration, hence the coverage."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import merge_json
from merge_json import merge


def test_adds_missing_keys():
    dest = {}
    template = {"hooks": {"SessionStart": ["x"]}}
    assert merge(dest, template) == {"hooks": {"SessionStart": ["x"]}}


def test_never_overwrites_host_scalars():
    dest = {"model": "opus"}
    template = {"model": "sonnet"}
    assert merge(dest, template)["model"] == "opus"


def test_deep_merges_nested_dicts():
    dest = {"hooks": {"PreToolUse": ["host-hook"]}}
    template = {"hooks": {"SessionStart": ["ours"], "PreToolUse": ["ours"]}}
    result = merge(dest, template)
    assert result["hooks"]["SessionStart"] == ["ours"]
    # Host list preserved, template item appended without duplication logic clobbering it
    assert "host-hook" in result["hooks"]["PreToolUse"]


def test_appends_list_items_without_duplicates():
    dest = {"permissions": {"deny": ["Bash(rm -rf /:*)"]}}
    template = {"permissions": {"deny": ["Bash(rm -rf /:*)", "Bash(git push -f:*)"]}}
    result = merge(dest, template)
    assert result["permissions"]["deny"].count("Bash(rm -rf /:*)") == 1
    assert "Bash(git push -f:*)" in result["permissions"]["deny"]


def test_mcp_servers_merge_is_additive():
    dest = {"mcpServers": {"host-server": {"command": "x"}}}
    template = {"mcpServers": {"graphify": {"command": "y"}}}
    result = merge(dest, template)
    assert set(result["mcpServers"]) == {"host-server", "graphify"}


class TestDeprecatedHookPrune:
    """A template hook-command upgrade must replace old entries on re-install,
    never duplicate them, and never touch the host's own hooks."""

    def _old_host_settings(self):
        return {"hooks": {
            "SessionStart": [{"hooks": [
                {"type": "command", "command": "python3 .agents/hooks/on_init.py"}]}],
            "PreToolUse": [{"matcher": "Bash", "hooks": [
                {"type": "command", "command": "python3 .agents/hooks/on_commit.py"},
                {"type": "command", "command": "python3 my_own_hook.py"}]}],
        }}

    def test_deprecated_commands_are_pruned(self):
        dest = self._old_host_settings()
        merge_json.prune_deprecated_hooks(dest)
        cmds = [h["command"] for ms in dest["hooks"].values() for m in ms for h in m["hooks"]]
        assert cmds == ["python3 my_own_hook.py"]

    def test_empty_matchers_and_events_are_removed(self):
        dest = {"hooks": {"Stop": [{"hooks": [
            {"type": "command", "command": "python3 .agents/hooks/state_mirror.py"}]}]}}
        merge_json.prune_deprecated_hooks(dest)
        assert "Stop" not in dest["hooks"]

    def test_reinstall_upgrades_without_duplicates(self):
        import json as _json
        template = _json.loads(
            (Path(__file__).resolve().parent.parent / "claude" / "settings.hooks.json").read_text())
        dest = self._old_host_settings()
        merge_json.prune_deprecated_hooks(dest)
        merged = merge_json.merge(dest, template)
        session_start = merged["hooks"]["SessionStart"]
        assert len(session_start) == 1
        assert "if [ -f .agents/hooks/on_init.py ]" in session_start[0]["hooks"][0]["command"]
        pre_cmds = [h["command"] for m in merged["hooks"]["PreToolUse"] for h in m["hooks"]]
        assert "python3 my_own_hook.py" in pre_cmds


def test_merge_preserves_host_deny_and_adds_template_deny():
    """Abort criterion for Sprint 027 C1: re-install must not drop host deny rules."""
    dest = {
        "permissions": {
            "deny": [
                "Bash(git push --force:*)",
                "Bash(host-only-deny:*)",
            ]
        }
    }
    template = {
        "permissions": {
            "deny": [
                "Bash(git push --force:*)",
                "Bash(git push -f:*)",
                "Bash(rm -rf /:*)",
            ],
            "defaultMode": "auto",
        },
        "autoMode": {
            "hard_deny": ["$defaults", "Never force-push."],
        },
    }
    result = merge(dest, template)
    deny = result["permissions"]["deny"]
    assert "Bash(host-only-deny:*)" in deny
    assert "Bash(git push --force:*)" in deny
    assert deny.count("Bash(git push --force:*)") == 1
    assert "Bash(rm -rf /:*)" in deny
    assert result["permissions"]["defaultMode"] == "auto"
    assert result["autoMode"]["hard_deny"][0] == "$defaults"
