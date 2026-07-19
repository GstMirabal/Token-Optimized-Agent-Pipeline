# Changelog

All notable changes to the Universal-Agents framework. Format: [Keep a Changelog](https://keepachangelog.com/), versioning: [SemVer](https://semver.org/). Hosts should pin to a tag (see README §Getting Started) rather than tracking `main`.

## [3.0.0] - Unreleased

Complete adaptation to real Claude Code conventions plus a governance-hardening overhaul. **Breaking**: commands are now namespaced (`/agents:start`, not `/start`); the fictional `@claudecode/skills` TypeScript bridge is gone.

### Added
- `scripts/install_claude.sh` + `scripts/install_claude.py`: idempotent bridge installer (symlinks into host `.claude/`, non-destructive JSON merge into `settings.json`/`.mcp.json`, `@.agents/agents.md` import into host `CLAUDE.md`, opt-in `--profile` packs).
- `profiles/crypto-django/`: first project profile (rules, specialist agents, Polymarket skill, market-data MCP registry, apps manifest) — preserves project self-learning without contaminating other hosts.
- Real Claude Code assets: frontmatter on all 12 core agents and 34 skills; 11 `.md` slash commands; `claude/settings.hooks.json` (SessionStart / PreToolUse / Stop hooks + permission denials); `claude/mcp.json`.
- Mechanical governance: J-12 push guard + Conventional Commit `#[Sprint_ID]` validation in `hooks/on_commit.py`; `.deploy_unlock` marker for the sanctioned deployment fallback.
- `workflows/extract_workflow.md` (restored), `rules/token_economy.md`, `Makefile`, `LICENSE.txt`, `docs/standards/templates/{BLUEPRINT,WALKTHROUGH,SYSTEM_OVERVIEW}_TEMPLATE.md`.
- `tests/`: unit suite for `merge_json` and `on_commit` + installer sandbox test, wired into CI.
- CI (`.github/workflows/ci.yml`): syntax, JSON, command↔workflow links, manifest parity/generation, structural audit, tests.

### Changed
- Constitution (`agents.md`): J-11 (hook blocking semantics), J-12 (branch discipline), dual Trinity Standard (executable vs knowledge skills), `architecture/` hierarchy fix, `pnpm` mandate coherence, relaxed `anti_amnesia` (once per session), profiles doctrine.
- `deployment_workflow.md` v3: PR-based merge via `gh` with CI gate as the default.
- `matrix_workflow.md` v3.6: sprint branch creation in Phase 3; `/loop` boundary (never wraps the Golden Gate).
- `memory_index.json`: summary-only Knowledge Items (no pointers to purged files).
- All skill docs translated to Technical English; stale `skills/core|3rd|local` paths flattened.

### Removed
- Fictional `commands/*.ts` stubs and `generate_commands.py` generation (replaced by `verify_commands.py` lint).
- `agents/agents_registry.json` (drifted duplicate of agent frontmatter).
- `mcp-config.json` (superseded by `claude/mcp.json`).
- Tracked `node_modules/` and machine-local `installed.lock` from version control.
