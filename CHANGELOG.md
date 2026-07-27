# Changelog

All notable changes to the Token-Optimized Agent Pipeline framework. Format: [Keep a Changelog](https://keepachangelog.com/), versioning: [SemVer](https://semver.org/). Hosts should pin to a tag (see README §Getting Started) rather than tracking `main`.

## [Unreleased]

### Security
- **Pre-publication hardening (Phase 017)**: audited the repo before making it public. `profiles/crypto-django/` (a real, identifiable production trading-bot blueprint — Django app inventory, business thresholds, KYC/vault handling, Polymarket integration) removed from the tracked tree and replaced with a fully illustrative `profiles/example-project/`; the corresponding `git filter-repo` history purge (it was present in every commit since `bb8e30d` and all tags `v3.0.0`-`v4.1.0`) is executed as a separate, explicitly-confirmed operation immediately after this merges. `skills/skillopt/data/scenarios.json` had a real absolute path leaking a real macOS username and a real host project name (`Cryptobot`, a casing variant the Phase 015 sweep missed) — replaced with a generic placeholder. `.env`/`.env.template` retired (confirmed unused); `mcp_servers/github_mcp/` mechanism kept, its setup docs no longer depend on the removed template. New `RA-15: HOST_CONTENT_GENERICIZATION` amendment (`agents.md §7`) and a new CI gate scanning for real-looking local developer paths, so this class of leak is caught automatically going forward instead of only at a pre-publication audit.

### Added
- **`NOTICE.md`**: discloses the 3 confirmed vendored skills under a license other than this repo's MIT (`frontend-design`, `skill-creator`: Apache-2.0; `django-expert-3rd`: MIT/Vinta Software).
- **`docs/audits/THIRD_PARTY_PROVENANCE_TODO.md`**: tracks 11 vendored skills with unverified license/origin — not a publish blocker, flagged for future review.
- **`CODE_OF_CONDUCT.md`**, **`SECURITY.md`**, **`CONTRIBUTING.md`**: standard community files for a public repo; `CONTRIBUTING.md` is repo-specific (branch discipline, skill creation flow, what never belongs in a PR here).

## [4.1.0] - 2026-07-26

### Added
- **Heuristic Pulse Gate (Phase 013 closure)**: `workflows/close_workflow.md` (v6.2.0) gains a new "2.5 Heuristic Pulse Gate" phase between `extract_handoff` and `memory_wipe` — presents the human with the exact candidate KI list before the destructive purge, applying the same `RA-13 SEQUENTIAL_GATES` principle to `memory_wipe` as already applies to merges. Skips (log-only) when the session runs under `/loop`, since `pipeline_workflow.md` allows `/loop` to wrap Sprint Closeout unattended and a hard block there would stall multi-sprint automation.

### Fixed
- **Phase 013 roadmap staleness**: `docs/roadmaps/core/pipeline/013-refined-telemetry-and-redundancy.md` had sat at `IN_PROGRESS`/0% while 3 of its 5 tasks (Telemetry Node Hardening, State Mirroring, Recovery Logic) were actually completed under other, later sprints (`#032`, `#078`/`#079`, `#081`) that never closed this tracking file. Closed for real now, with evidence citations, plus a fresh `memory_index.json` orphan audit (0 entries pruned — all 6 current entries are distinct).

## [4.0.0] - 2026-07-26

### Changed
- **Terminology & Nomenclature Hardening (Phase 015)**: replaced the framework's institutional/militarized register with plain, industry-standard vocabulary, starting with the project's own title — `Universal-Agents` → **Token-Optimized Agent Pipeline** (`README.md`, `config/framework_identity.json`, `README_TEMPLATE.md`, and the banner SVG, whose terminal-mockup prompt/branch/version were also refreshed). The core pipeline codename `Matrix`/`Matrix V3` is retired in favor of `Pipeline`: `workflows/matrix_workflow.md` → `pipeline_workflow.md`, `commands/matrix.md` → `pipeline.md` (`/agents:pipeline`), `agents/matrix_mapper.md` → `topology_mapper.md`, `skills/matrix-monitor/` → `topology-monitor/`, `docs/architecture/matrix_topology_map.md` → `topology_map.md`, `docs/contracts/core/matrix_mapper_contract.md` → `topology_mapper_contract.md`. The 8-phase pipeline is renamed accordingly: Strategic Genesis → Planning, Tactical Blueprint → Roadmap Drafting, Master Assembly → Roadmap Review, Golden Gate → Approval Gate, Monitored Execution → Execution, Tactical Liquidation → Sprint Closeout. Per-agent flavor titles lose their theatrics while keeping their real function (`devops_sentinel.md` → `devops_agent.md`, `github_sentinel.md` → `git_sync_agent.md`, "Supreme Coordinator" → "Lead Agent", "Arsenal Synthesizer" → "Skill Builder", "Governance Sentinel" → "Rule Auditor", etc. — see `agents.md §6`). `agents.md §7` "Jurisprudence" becomes **"Rule Amendments"**, and every `J-01..J-14` citation repo-wide becomes `RA-01..RA-14`. `skills/governance-sentinel/` → `compliance-checker/` (including its `apply_jurisprudence.py` script → `apply_rule_amendments.py`, updated in lockstep with `distill.py`'s clause-generation regex). "Trinity Standard" → "Three-File Skill Standard" (`agents.md §3` key `trinity_standard` → `three_file_standard`); "Arsenal" (skills library) and "Constitutional"/"the Constitution" (→ "governance rules"/"ruleset") retired throughout. `docs/roadmaps/core/matrix/` and `docs/sprints/core/matrix/` folder paths were initially deferred pending Phase 013 (see Phase 016 below, which carried out the move). "Nucleus" (standalone/non-submodule mode) is kept as-is — already a reasonable technical metaphor, not militarized. Historical record is untouched by design: past `CHANGELOG.md` entries and closed roadmap phases `000-014` keep their original vocabulary, since rewriting the past would falsify the record. Full naming-migration table and execution waves: `docs/roadmaps/core/pipeline/015-terminology-and-nomenclature-hardening.md`.
- **Folder Topology Migration (Phase 016)**: completed the deferred half of Phase 015 — `docs/roadmaps/core/matrix/` → `docs/roadmaps/core/pipeline/` and `docs/sprints/core/matrix/` → `docs/sprints/core/pipeline/` (the latter held two untracked, never-committed implementation-plan files, moved with plain `mv` rather than `git mv`), plus `docs/active_state.json`'s `active_app: "matrix"` → `"pipeline"` to match. Historical phase files `000-014` moved with the folder but were not edited — their content, including phase 12's own `sentinel`-named filename, remains an accurate snapshot of what existed when each was written. Also closed three follow-up findings flagged at Phase 015's close: deleted the orphaned `skills/skill-creator-3rd/` (untracked `__pycache__`-only debris left over from the `v3.5.1` rename to `skill-creator`), scrubbed a hardcoded host project name (`CryptoBot`) out of `skills/compliance-checker/scripts/kill_switch.sh`'s header comment, and rewrote `skills/README.md`'s topology section, which still documented an obsolete `core/`/`local/`/`3rd/` sub-layer structure contradicting the current flat `skills/` rule (`agents.md §3 topological_order`) — while fixing that, also caught and replaced two more institutional-register strays the earlier case-insensitive sweep missed ("tactical tags" and "the sanctioned Armory").

### Fixed
- **`skills/compliance-checker/scripts/distill.py`** (renamed from `governance-sentinel` in Phase 015, above) **never found real telemetry on any host**: `ROOT` was an unconditional 4-parent climb from the script, which lands inside `.agents/` for a normal host install instead of the host root — `memory/telemetry/raw_errors.json` was never checked at the path that actually holds it (`.agents/memory/` doesn't exist and never has, `submodule_purity`). Now mode-aware, same detection `install_claude.py`/`render_readme.py` already use (`AGENTS_ROOT/.git` real directory ⇒ nucleus, `ROOT = AGENTS_ROOT`; otherwise a host submodule, `ROOT = AGENTS_ROOT.parent`). Found by actually running the distiller during a session close and getting a suspicious "no telemetry" on a host with 7 recorded errors.
- **`hooks/on_commit.py`'s commit-message extraction false-positives on the `-m "$(cat <<'EOF' ... EOF)"` heredoc idiom**: the PreToolUse hook only ever sees the raw, unresolved bash command text, so the naive quoted-string regex stopped at the first embedded `"` instead of the heredoc's real content, flagging perfectly valid Conventional Commit messages as violations. `extract_commit_message()` now recognizes the heredoc pattern explicitly and pulls the real body out before falling back to the plain-quote case. Confirmed via the same host's telemetry: this exact false positive fired 7 times in one session.

## [3.5.1] - 2026-07-26

### Fixed
- **`skills/skill-creator-3rd` mislabel**: the `-3rd` suffix never reflected reality — `SKILL.md`'s own frontmatter already named it `skill-creator`, `manifest_skills.json` already had a mismatched `name`/`path` pair, and its content is native institutional boilerplate self-referencing this framework's own rule numbers (a real vendor fork wouldn't). Renamed to `skills/skill-creator/`, which lifts the Skill Documentation Veto (`skills_and_integrations.md §3`) that blocked closing its personal-brand leak during Phase 14 (`v3.5.0`) — footer now stripped, consistent with the other 9 skills. Hosts on `v3.5.0` should re-run `install_claude.py` after bumping to relink `.claude/skills/skill-creator-3rd`, which the rename leaves as a dangling symlink.

## [3.5.0] - 2026-07-26

### Added
- **`rules/documentation_standard.md`**: new framework-class rule consolidating Diátaxis (reader-intent classification), C4 (architecture zoom levels, with a per-stack density formula for Level 3 eligibility), ADR (decision records with trigger-based Nygard/MADR scaling), and a deterministic freshness gate (`make docs-freshness-check`) that replaces trust-based doc updates with scripted verification at sprint close — including five documentation-integrity sub-checks and the C4 density computation. Root cause: a host's Zero Coordinate anchors went stale for 34 sprints because `close_workflow.md`'s `history_sync` step never named them explicitly and nothing verified it happened.
- **`token_economy_agent`**: new auxiliary agent, owns Filter 5 (`token-saver-auditor`) and a structural `make verify` scanner that flags recurring mechanisms delegated to agent judgment where a deterministic script would do.
- **`ADR_TEMPLATE.md`**, **`GUIDE_TEMPLATE.md`**: new templates (`docs/standards/templates/`).
- **J-14 PATCH_PROPAGATION** (`agents.md §7`): a long-lived planning document revised across sessions must be grepped in full for other mentions of a term before a patch is considered closed.
- **Config-driven identity system** (`config/framework_identity.json`, `docs/standards/templates/IDENTITY_TEMPLATE.json`, `scripts/render_readme.py`): two-tier README branding — a fixed FRAMEWORK config (this repo's own author identity, used for the framework-credit line and this repo's own README) and a per-project HOST config (`identity.config.json`, scaffolded non-destructively by `install_claude.py` on first install, auto-filling `repo_slug` from `git remote get-url origin`) that `render_readme.py` (stdlib-only, no new dependencies) resolves against `README_TEMPLATE.md`'s tags. Nucleus mode is auto-detected the same way `install_claude.py` already does (`(AGENTS_DIR / ".git").is_dir()`), never a manual flag, closing a leak vector where a mistyped flag could have exposed the framework author's personal fields to a third-party render. `README_TEMPLATE.md` itself is genericized: no more hardcoded owner contact, banner is conditional (`<!-- BANNER_START/END -->`, omitted when unset), version badge, "why" hook, and an optional `{{GOVERNED_BY_AGENTS}}` tag for hosts that want to show they're governed by this framework.
- **`docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md`**: first guide under the `documentation_standard.md` How-to convention (`docs/guides/[MODULE]_[TASK]_GUIDE.md`) — extracts the full `/agents:*` command reference out of `README.md`, which now keeps only the three most-used commands inline plus a link out (README drifting into exhaustive-reference territory was exactly what `documentation_standard.md` warns against).
- **`docs/assets/logo/agents_banner.svg`**: new banner for this repo's own `README.md` — terminal/node-graph aesthetic (this repo's own visual identity, deliberately distinct from the framework author's personal developer brand, which is a separate, not-yet-started track).

### Changed
- **`BLUEPRINT_TEMPLATE.md`**: restructured to arc42-lite (Introduction & Goals / Context & Scope / Building Block View / Runtime View / Crosscutting Concepts / Constraints / Decisions-links-ADRs / Glossary); adds the freshness-gate metadata block.
- **`SYSTEM_OVERVIEW_TEMPLATE.md`**: adds a metadata block (had none) and a C4 Level 1-2 diagram slot.
- **`WALKTHROUGH_TEMPLATE.md`**, **`HOTFIX_TEMPLATE.md`**: link ADRs instead of restating rationale inline.
- **`close_workflow.md`**: Phase 1 wires the freshness gate; Phase 2 (`history_sync`) now names the Zero Coordinate anchors explicitly.
- **`standardization_workflow.md`**: routes pre-arc42-lite Blueprints as migration candidates (never auto-rewritten); Scenario A and C both prompt for `code_containers`.
- **`start_workflow.md`**: `lightweight_sync` surfaces a one-time notice when an authorized pin-bump introduces a new rule.
- **`docs/contracts/core/matrix_mapper_contract.md`**: documents that unknown `active_state.json` root keys (e.g. `code_containers`, `adr_autoescalate_triggers`) must be preserved by any writer.

### Fixed
- **Personal-brand leak across 10 distributed skill `README.md`/asset files**: `token-saver-auditor`, `omni-context-minimizer`, `python-quality-auditor`, `readme-standardizer` (+ its `assets/template.md`), `mcp-registry`, `js-standardizer`, `env-shielding-auditor`, and `slash-commander` each carried a full copy-pasted project-boilerplate footer (badges row, ToC, `## Contact` with the framework author's real email/LinkedIn/X) that `install_claude.py` symlinks unchanged into every host that installs this framework. Stripped the boilerplate from all nine, keeping each skill's actual functional documentation intact.
- **`skills/readme-standardizer` actively propagated the framework author's identity as a rendering payload**, not just static text: `SKILL.md` instructed the executing agent to assume every consuming project's owner is `GstMirabal` and to keep the `Contact` section of `assets/template.md` "ABSOLUTELY intact" — meaning any third-party host running this skill would stamp the framework author's personal contact info into their own project's README. Both files now use `{{OWNER_NAME}}`/`{{OWNER_EMAIL}}`/`{{OWNER_LINKEDIN_URL}}`/`{{OWNER_X_URL}}`/`{{OWNER_GITHUB_USERNAME}}` placeholders that the executing agent fills from the actual consuming project's real context.
- **`skill-creator-3rd/README.md` intentionally left out of this closure**: `rules/skills_and_integrations.md §3`'s Skill Documentation Veto prohibits modifying README files of `-3rd`-suffixed skills, even though this particular directory's content is native institutional boilerplate rather than genuine upstream vendor documentation — a topological mislabel, not (yet) authorization to override the Veto. Flagged as a follow-up: either correct the mislabel (drop the `-3rd` suffix) or obtain an explicit human exception, before this file's leak can be closed.
- **Two unused draft banner images purged** (`docs/assets/logo/Imagen.png`, `institutional_banner111.png`) and the retired `institutional_banner.png` removed after every reference (`README.md`, `skills/slash-commander/README.md`) was repointed to the new SVG — caught a broken image link in this repo's own `README.md` at Quality Gate 1 that the initial pass missed (the WBS gave `slash-commander` a dedicated repoint task but not this repo's own README).

## [3.3.2] - 2026-07-21

### Fixed
- **Stale bridge lock desync**: `hooks/on_init.py sync_commands` trusted `.claude_bridge.lock` matching the submodule's commit hash as proof the linked `.claude/` bridge (commands/agents/skills) still existed on disk. A `git clean -fd` or manual deletion of the host's untracked `.claude/` tree — `git clean` skips submodules by default, so the lock (inside `.agents`) survives untouched — desynced the lock from reality, leaving `/agents:*` commands silently unrecognized until someone noticed and manually re-ran the installer. Added a cheap sentinel-file existence check (`bridge_intact`, two `Path.exists()` calls) before trusting the lock; missing artifacts now force a re-link regardless of commit-hash match. Field report from a host session where the bridge had to be diagnosed and manually reinstalled.
- **Host `.gitignore` never hardened against the bridge/graphify output**: the same live host had a pre-existing bare `settings.json` rule that accidentally swallowed `.claude/settings.json` (which must stay tracked so `SessionStart` can bootstrap a fresh clone) while leaving the actual bridge mirror (`.claude/agents|commands|skills`, root `CLAUDE.md`) merely untracked-but-not-ignored — vulnerable to both an accidental `git add -A` commit and a `git clean -fd` wipe. Separately, `graphify-out/` (recommended by `skills/graphify/SKILL.md`'s own git-hook integration) had silently accumulated 23MB across 20 commits with no pruning, since nothing ever told the host to ignore it. `install_claude.py` now has `ensure_gitignore_entries()`, called from `main()` on every (non-nucleus) install: idempotently appends the bridge + `graphify-out/` entries to the host's root `.gitignore` if missing, never touching existing lines. Every future host gets this hygiene automatically instead of rediscovering it the hard way.

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
