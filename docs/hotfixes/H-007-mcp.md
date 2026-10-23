# 🚑 Hotfix: H-007-mcp
**File**: `docs/hotfixes/H-007-mcp.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `CRITICAL`
**Detected**: 2026-10-23 · **Resolved**: 2026-10-23

---

## 1. Symptom

The template `claude/mcp.json` ships an MCP server, `git-sync-agent`, whose launcher
`mcp_servers/github_mcp/scripts/start_mcp.sh` runs `pnpm dlx @modelcontextprotocol/server-github`
with no version pinned. Claude Code starts MCP servers outside the agent sandbox, and this
launcher requires `GITHUB_PERSONAL_ACCESS_TOKEN` in its environment. Any host that exports that
token runs whatever version of the package the registry serves, unsandboxed, with the token in
reach. The package belongs to the reference servers moved to `modelcontextprotocol/servers-archived`,
which states that archived servers receive no security updates. Blast radius: every host
bridged with `scripts/install.py` (the template is merged into the host `.mcp.json`, and
`scripts/cursor_adapter.py` writes it into `.cursor/mcp.json`).

Nothing uses the server: the workflows, rules and agent profiles name `gh` 28 times and this
MCP server in none of them, and the nucleus bridge omits MCP servers entirely.

## 2. Root Cause

`mcp_servers/github_mcp/scripts/start_mcp.sh` resolves its package by name only
(`pnpm dlx @modelcontextprotocol/server-github`). `agents.md §8` pins supply-chain settings for
installs, but a `dlx` of an unversioned name still takes the newest release that the age gate
admits, and the gate applies only where `dlx` reads `minimumReleaseAge`. No test inspected what
a template MCP server launches.

## 3. Fix Applied

| File | Change |
| :--- | :--- |
| `claude/mcp.json` | Remove the `git-sync-agent` server |
| `mcp_servers/github_mcp/` | Delete the launcher, its health check and its README/SKILL |
| `tests/test_mcp_template.py` | Pin that no template server, nor any launcher script it names, runs an unpinned `pnpm dlx`/`npx` package, and that every `.agents/` path a server names exists |
| `README.md`, `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md`, `docs/architecture/topology_map.md` | Drop the references to the deleted `mcp_servers/` directory |

Branch/commit: `hotfix/H007` → commit SHAs in the `[Unreleased]` entry of `CHANGELOG.md`.

Hosts bridged before this hotfix keep the `git-sync-agent` entry in their `.mcp.json`, because
the JSON merge is additive. After the pin bump the entry points at a launcher that no longer
exists, so the server fails to start instead of running the package. Pruning the stale entry is
routed to Sprint 057 with `KI-056-3` (retired template values are never pruned). GitHub access
over MCP returns in Sprint 059 as GitHub's maintained remote server, with no local launcher.

## 4. Verification

- `venv_skillopt/bin/python -m pytest tests/test_mcp_template.py` — the new test fails on the
  parent commit and passes at the fix (`Repro:` trailer on the fix commit).
- `make verify` exits `0`.

## 5. Rule Amendment Check
- [x] Is this failure class systemic? Partly: an unpinned package executed outside the sandbox. The pinning test is the guard. The rule question (MCP launchers in `RA-19` enumeration and `§8`) is routed to the Sprint 059 sandbox block: N/A here
- [ ] Does the root cause reveal a design decision worth recording? N/A
- [x] Master Ledger entry added under `[Unreleased]`.
