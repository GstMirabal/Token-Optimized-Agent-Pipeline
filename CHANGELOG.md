# Changelog

All notable changes to the Universal-Agents framework. Format: [Keep a Changelog](https://keepachangelog.com/), versioning: [SemVer](https://semver.org/). Hosts should pin to a tag (see README §Getting Started) rather than tracking `main`.

## [Unreleased]

### Fixed
- **Stale bridge lock desync**: `hooks/on_init.py sync_commands` trusted `.claude_bridge.lock` matching the submodule's commit hash as proof the linked `.claude/` bridge (commands/agents/skills) still existed on disk. A `git clean -fd` or manual deletion of the host's untracked `.claude/` tree — `git clean` skips submodules by default, so the lock (inside `.agents`) survives untouched — desynced the lock from reality, leaving `/agents:*` commands silently unrecognized until someone noticed and manually re-ran the installer. Added a cheap sentinel-file existence check (`bridge_intact`, two `Path.exists()` calls) before trusting the lock; missing artifacts now force a re-link regardless of commit-hash match. Field report from a host session where the bridge had to be diagnosed and manually reinstalled.

## [3.3.1] - 2026-07-20

### Fixed
- **Phantom config**: `skillopt/configs/agents_opt.yaml` declared `model.backend: azure_openai` but `train_runner.py` read the flat key `model_backend` (never present) — the config's stated intent was silently ignored, always defaulting to Gemini. Added the real flat `model_backend` selector (documented, now reaches the existing Claude-optimizer code path too) and clarified in-file why `model.backend: azure_openai` must stay as-is (vendor monkeypatch anchor, not a live selector). Documented in `skillopt/SKILL.md` why `requirements-freeze.txt` carries unused `azure-*` transitive deps.

### Added
- `rules/graphify.md`: documented graph coverage gaps found during a full audit (`.yaml`/`.yml` never indexed; one observed extractor anomaly on a specific `.md` file) so "absent from the graph" is never read as "doesn't exist."

## [3.3.0] - 2026-07-20

### Added
- **Nucleus self-bridge**: running the installer inside the nucleus repo no longer refuses — it installs a minimal bridge (`.claude/commands/agents/*` + `.claude/agents/*` symlinks + `@agents.md` import in a nucleus `CLAUDE.md`) so `/agents:*` commands work while developing the framework itself. No hooks/skills/MCP/scaffolding (`nucleus_neutrality` governs structure, not tooling access); profile installs into the nucleus remain refused. Covered by a new sandbox test scenario.

### Fixed
- **Hotfix H-001**: `generate_manifest.py` stamped `updated_at` with the current date unconditionally, turning CI's regenerate-and-diff check into a midnight time bomb (first red CI on `main`, sprint #081 merge). Now deterministic: the date only advances when the skill payload changes.
- **J-13 SEQUENTIAL_GATES** (new jurisprudence from the same incident): a verification gate and the irreversible action it guards must be separate observed invocations — the #081 merge chained `sleep && merge` in one script, voiding the CI gate. `deployment_workflow pr_flow` now mandates `gh pr checks --watch` as its own step before `gh pr merge`.

## [3.2.1] - 2026-07-20

### Fixed
- Field report from a fresh host session (living feedback loop in action): hook commands in `claude/settings.hooks.json` are now guarded — an uninitialized `.agents` submodule degrades to a clear instruction (`git submodule update --init`) instead of a cryptic "file not found"; `merge_json.py` prunes deprecated hook commands on re-install so template upgrades replace instead of duplicating (host-owned hooks untouched, covered by 3 new tests); stale `.agent_state/mirror.json` no longer reads as a collision — `start_workflow read_anchor` documents mirror reconciliation (anchor wins, resync, continue; mirror is only authoritative for crash recovery) and `close_workflow state_sync` refreshes the mirror at every close.

## [3.2.0] - 2026-07-19

### Added
- `agents.md §4 feedback_upstream` + `extract_workflow upstream_feedback`: learning codified as a LIVING three-tier flow (host → profile → nucleus) — every host session is a sensor for the shared brain; framework-class lessons must be drafted as nucleus contributions, never left to die in a local index.
- `remediation_workflow reversibility`: mandatory `git stash push -u` snapshot before the state nuke (Reversibility Gate doctrine now covers the Panic Button too).

### Changed
- Token-economy pass over all workflows (live-fire tested): constitution re-read replaced with presence-verification in `close`/`extract`/`matrix`/`audit` (auto-imported via `CLAUDE.md`; re-read only after compaction); Onboarding Scenario Matrix moved from the every-session `start_workflow` to `standardization_workflow` Phase 6 (one-time routing, lazy-loaded); `verify_references.py` excludes generated/vendored runtime dirs (`venv_skillopt/`, `graphify-out/`, `.claude/`).

### Fixed
- Live-fire findings from running `/agents:start` in nucleus mode: `habitability_check` prohibition narrowed to Phase 1.5 only (Phase 0 + `lightweight_sync` are legal in the nucleus, with `.agents/`-prefixed paths resolving to the repo root); `lightweight_sync` nucleus nuance (commit offset past a tag is not drift); `pip_setup` lock content specified; `close_workflow state_sync` explicitly applies in nucleus mode (stale-anchor prevention).
- Live-fire findings from executing every workflow: `federation_audit` gains nucleus-mode skip (was unconditionally failing in the nucleus); empty `mass-standardizer/assets/` purged (J-07 violation in our own tree); `remediation` extraction order documented (git-ignored telemetry survives the nuke by design).

## [3.1.0] - 2026-07-19

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
