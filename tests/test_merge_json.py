"""Tests for scripts/merge_json.py — the non-destructive merge that touches
host users' .claude/settings.json and .mcp.json. A regression here corrupts
real user configuration, hence the coverage."""
import copy
import json
import sys
from pathlib import Path
from typing import ClassVar

import pytest

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


class TestRetiredValuePrune:
    """Values the framework once shipped and retired leave host lists on merge."""

    RETIRED: ClassVar[dict[str, frozenset[str]]] = {"sandbox.filesystem.denyRead": frozenset({"./old-secret"})}

    def test_retired_value_absent_from_template_is_removed(self):
        dest = {"sandbox": {"filesystem": {"denyRead": ["./old-secret", "./keep"]}}}
        template = {"sandbox": {"filesystem": {"denyRead": ["./new"]}}}
        result = merge(dest, template, retired=self.RETIRED)
        assert "./old-secret" not in result["sandbox"]["filesystem"]["denyRead"]

    def test_host_added_value_survives(self):
        dest = {"sandbox": {"filesystem": {"denyRead": ["./old-secret", "./host-own"]}}}
        template = {"sandbox": {"filesystem": {"denyRead": ["./new"]}}}
        deny = merge(dest, template, retired=self.RETIRED)["sandbox"]["filesystem"]["denyRead"]
        assert "./host-own" in deny and "./new" in deny

    def test_retired_value_still_in_template_is_kept(self):
        dest = {"sandbox": {"filesystem": {"denyRead": ["./old-secret"]}}}
        template = {"sandbox": {"filesystem": {"denyRead": ["./old-secret"]}}}
        deny = merge(dest, template, retired=self.RETIRED)["sandbox"]["filesystem"]["denyRead"]
        assert deny == ["./old-secret"]

    def test_empty_retired_mapping_changes_nothing(self):
        dest = {"a": {"b": ["x", "y"]}}
        assert merge(dest, {"a": {"b": ["z"]}}, retired={}) == {"a": {"b": ["x", "y", "z"]}}

    def test_missing_key_path_is_a_noop(self):
        dest = {"other": ["./old-secret"]}
        merge_json.prune_retired_values(dest, {}, self.RETIRED)
        assert dest == {"other": ["./old-secret"]}


RETIRED_EXCLUDED = frozenset({
    "python3 -I .agents/scripts/with_env.py graphify-extract",
    "python3 -I .agents/scripts/with_env.py graphify-extract-deep",
    "python3 -I .agents/scripts/with_env.py graphify-label",
    "gh pr create *",
    "gh release create *",
    "gh pr checks *",
    "gh pr list *",
    "gh repo view *",
    "gh release view *",
    "gh auth status",
})


class TestShippedRetiredValues:
    """The real RETIRED_VALUES applied against the real shipped template."""

    def test_retired_values_are_exactly_the_ten_excluded_commands(self):
        assert dict(merge_json.RETIRED_VALUES) == {"sandbox.excludedCommands": RETIRED_EXCLUDED}

    def test_real_template_merge_drops_retired_and_keeps_host_entry(self):
        template_path = Path(__file__).parent.parent / "claude" / "settings.hooks.json"
        template = json.loads(template_path.read_text(encoding="utf-8"))
        dest = {"sandbox": {"excludedCommands": [*sorted(RETIRED_EXCLUDED), "gh run list *"]}}
        excluded = merge(dest, template)["sandbox"]["excludedCommands"]
        assert not RETIRED_EXCLUDED & set(excluded)
        assert "gh run list *" in excluded


# MCP server entries the template has shipped, and the shapes the additive merge
# left in hosts bridged before `246cd20` (Hotfix H-008).
GRAPHIFY_PRE_246CD20 = {
    "command": ".agents/venv_skillopt/bin/python",
    "args": ["-m", "graphify.serve", "graphify-out/graph.json"],
    "description": "Graphify Knowledge Graph MCP Server",
}
RETIRED_LAUNCHER = ".agents/mcp_servers/github_mcp/scripts/start_mcp.sh"


def _graphify_host_shapes() -> dict[str, dict]:
    """Return the host `graphify` entries that a template merge must repair.

    Returns:
        Named host entries: the pre-`246cd20` shape, that shape after an
        additive re-merge appended `-I` at the end, and a host-changed command.
    """
    appended = copy.deepcopy(GRAPHIFY_PRE_246CD20)
    appended["args"].append("-I")
    changed = {**copy.deepcopy(GRAPHIFY_PRE_246CD20), "command": "python3"}
    return {"pre-246cd20": GRAPHIFY_PRE_246CD20, "appended -I": appended, "host command": changed}


def _real_mcp_template() -> dict:
    """Return the shipped `claude/mcp.json`.

    Returns:
        The parsed template.
    """
    path = Path(__file__).resolve().parent.parent / "claude" / "mcp.json"
    return json.loads(path.read_text(encoding="utf-8"))


class TestTemplateOwnedMcpServers:
    """A server the template defines is the template's entry after every merge (H-008)."""

    SHAPES: ClassVar[list[str]] = sorted(_graphify_host_shapes())

    @pytest.mark.parametrize("shape", SHAPES)
    def test_template_server_replaces_host_entry(self, shape: str) -> None:
        """Every historical host shape of a template server becomes the template entry."""
        template = _real_mcp_template()
        dest = {"mcpServers": {"graphify": copy.deepcopy(_graphify_host_shapes()[shape])}}
        assert merge(dest, template)["mcpServers"]["graphify"] == template["mcpServers"]["graphify"]

    def test_host_own_server_is_untouched(self) -> None:
        """A server the template does not define is left exactly as the host wrote it."""
        own = {"command": "node", "args": ["server.js"], "env": {"K": "v"}}
        result = merge({"mcpServers": {"host-server": copy.deepcopy(own)}}, _real_mcp_template())
        assert result["mcpServers"]["host-server"] == own

    def test_replacement_is_reported(self, capsys: pytest.CaptureFixture[str]) -> None:
        """A host entry that differed from the template is named on stderr."""
        merge({"mcpServers": {"graphify": copy.deepcopy(GRAPHIFY_PRE_246CD20)}}, _real_mcp_template())
        assert "graphify" in capsys.readouterr().err

    @pytest.mark.parametrize("host_servers", [["x"], None, "x"])
    def test_non_mapping_host_servers_are_reported(
        self, host_servers: object, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A host `mcpServers` that is not a mapping is left as is and named on stderr (QA-H008-R1-1)."""
        result = merge({"mcpServers": copy.deepcopy(host_servers)}, _real_mcp_template())
        assert result["mcpServers"] == host_servers
        assert "not a mapping" in capsys.readouterr().err

    @pytest.mark.parametrize("name", ["git-sync-agent", "github-sentinel"])
    def test_retired_server_with_shipped_launch_is_removed(self, name: str) -> None:
        """A retired server whose launch is the one the framework shipped is removed."""
        entry = {"command": "/bin/bash", "args": [RETIRED_LAUNCHER], "env": {"GITHUB_TOKEN": "x"}}
        template = {"mcpServers": {"graphify": GRAPHIFY_PRE_246CD20}}
        assert name not in merge({"mcpServers": {name: entry}}, template)["mcpServers"]

    def test_retired_name_with_host_launch_is_kept(self, capsys: pytest.CaptureFixture[str]) -> None:
        """A retired name the host relaunched differently is kept and reported."""
        entry = {"command": "node", "args": ["mine.js"]}
        template = {"mcpServers": {"graphify": GRAPHIFY_PRE_246CD20}}
        result = merge({"mcpServers": {"github-sentinel": copy.deepcopy(entry)}}, template)
        assert result["mcpServers"]["github-sentinel"] == entry
        assert "github-sentinel" in capsys.readouterr().err
