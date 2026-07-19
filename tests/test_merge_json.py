"""Tests for scripts/merge_json.py — the non-destructive merge that touches
host users' .claude/settings.json and .mcp.json. A regression here corrupts
real user configuration, hence the coverage."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
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
