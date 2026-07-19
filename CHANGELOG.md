# Changelog

All notable changes to the Universal-Agents framework. Format: [Keep a Changelog](https://keepachangelog.com/), versioning: [SemVer](https://semver.org/). Hosts should pin to a tag (see README §Getting Started) rather than tracking `main`.

## [Unreleased]

### Added
- **Master Ledger doctrine**: the previously-undefined "Master Ledger" is now the host root `CHANGELOG.md` (agents.md §0, `CHANGELOG_TEMPLATE.md`) — sprint entries appended at close (`history_sync`), sealed as `[vX.Y.Z]` at deployment (`ledger_seal`), jurisdiction strictly separate from this file.
- **Onboarding Scenario Matrix** in `start_workflow` (`first_run_scaffold`): greenfield / prior-agents / mature-no-agents detection and routing, including submodule identity verification for pre-existing `.agents` checkouts.
- **Legacy Absorption Protocol** (`standardization_workflow` Phase 5): census → secret scan → reversibility snapshot (blocking gate) → reconciliation report → Human OK → migration (routing table for `task/`, `implementation_plan*`, `knowledge/`, per-domain `memory/`, numbered roadmaps, foreign framework files) → conservation/link integrity audit sealed as `docs/ONBOARDING_AUDIT.md`.
- Deliberate-update doctrine wired end-to-end: `start_workflow lightweight_sync` now detects newer `.agents` tags and asks the human (never auto-updates); `install_claude.py` records the installed submodule commit in `.claude_bridge.lock`; `hooks/on_init.py` re-links the bridge automatically after a deliberate pin update.
- `audit_workflow federation_audit`: verifies tag pinning, bridge-lock sync, and a clean submodule tree.
- `skill_forge_workflow forge_destination`: skills are forged in host `.claude/skills/` (default), `profiles/[name]/skills/`, or `.agents/skills/` — the latter two only via the nucleus branch→PR→tag flow.

- **Reference-integrity linter** (`scripts/verify_references.py`, CI-enforced): rules reachability, template existence, and `Rule NN` concordance — the "phantom reference" inconsistency class is now unmergeable. Found and mapped 3 additional phantom citations on its first run.
- `rules/LEGACY_RULE_CONCORDANCE.md`: resolves all surviving numbered "Rule NN" citations (the numbering was abolished by the tabular refactor); the only constitutionally legal fix for vendored `-3rd` docs (Skill Documentation Veto).
- **Rule Contexts lazy-load index** in `agents.md §0`: every `rules/*.md` now has a documented load trigger (previously 5 of 6 were unreachable dead letter).
- `HOTFIX_TEMPLATE.md`; J-03 emergency naming declared an explicit sanctioned exception to J-06.

### Changed
- `close_workflow submodule_purity`: host sessions must never commit into the `.agents` submodule; dirty submodule trees are surfaced to the human.
- `manifest_skills.json` registration path documented as generated-only in `skill_forge_workflow` and `rules/skills_and_integrations.md`.
- Hooks' docstrings now cite keyed rules (`trinity_standard`, `secret_sovereignty`, `state_anchor`) instead of abolished numbers; phantom paths fixed in `token-saver-auditor` (`.agent_state/session_{UID}/` → real state anchors) and `mass-standardizer` (flat `skills/` scan); `README_TEMPLATE` Federated Registry updated to keyed sections.

## [3.0.0] - 2026-07-19

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
