---
description: "Terminology & Nomenclature Hardening (Phase 15)"
status: "COMPLETED"
version: 1.0.0
---

# Roadmap: Phase 15 - Terminology & Nomenclature Hardening

## Status
- **Strategy Lock:** `CLOSED`
- **Completion:** 100% (9 waves executed: Wave 0 title/banner, Waves 1-6 vocabulary + runtime code, Wave 7 J-XX→RA-XX renumbering, Wave 8 closeout)
- **Source of Truth:** `~/.claude/plans/woolly-marinating-hollerith.md` (Golden Gate passed via Plan Mode, human-approved — naming migration table + execution waves + verification section)
- **Sprint ID:** `015` — next sequential number after Phase 14 (`014-identity-branding-hardening.md`, `COMPLETED`). Phase 13 (`013-refined-telemetry-and-redundancy.md`) remains `IN_PROGRESS` on an unrelated telemetry track in this same `docs/roadmaps/core/matrix/` folder — this Phase deliberately stays in the *old* `.../matrix/` path (see Objective) to avoid disturbing that concurrent work.
- **Quality Gates:** Structural — repo-wide case-insensitive grep sweep for every retired term returned zero hits outside declared non-goals and historical record (performed twice, the second pass catching ALL-CAPS runtime print strings the first case-sensitive sweep missed). Functional — full `pytest` suite (56 tests) green after every code-level rename (`hooks/on_commit.py` `audit_trinity_standard` → `audit_three_file_standard`, `tests/test_on_commit.py` updated in lockstep); CI-equivalent local runs of `verify_commands.py`, manifest parity check, `legacy_app_auditor.py`, and `verify_references.py` all green.

## Objective
Replace the framework's institutional/militarized register (`Matrix`, `Golden Gate`, `Tactical Liquidation`, `Sentinel`, `Arsenal`, `Jurisprudence`, `Constitutional`, workflow nicknames like "The Quartermaster"/"The Inquisitor Protocol"/"The Panic Button"/"The Vanguard Protocol") with plain, industry-standard technical nomenclature — starting with the project's own title (`Universal-Agents` → **Token-Optimized Agent Pipeline**) — while explicitly deferring the `docs/roadmaps/core/matrix/` and `docs/sprints/core/matrix/` folder-path rename to a future Phase 016, since Phase 13 is concurrently `IN_PROGRESS` in that same folder.

## Naming Migration Table
Full before/after table (pipeline core, phase names, per-agent flavor titles, vocabulary/section terms, non-goals) lives in the approved plan: `~/.claude/plans/woolly-marinating-hollerith.md`. Summary of the highest-impact renames:

| Category | Before | After |
| :--- | :--- | :--- |
| Project title | `Universal-Agents Framework (.agents)` | `Token-Optimized Agent Pipeline (.agents)` |
| Pipeline codename | `Matrix` / `Matrix V3` | `Pipeline` |
| Phase 1 | Strategic Genesis | Planning |
| Phase 3 | Tactical Blueprint | Roadmap Drafting |
| Phase 4 | Master Assembly / "Council" | Roadmap Review |
| Phase 5 | Golden Gate | Approval Gate |
| Phase 6 | Monitored Execution | Execution |
| Phase 8 | Tactical Liquidation | Sprint Closeout |
| §7 title | Jurisprudence (Heuristic Amendments) | Rule Amendments |
| Amendment codes | `J-01..J-14` | `RA-01..RA-14` |
| Skill package shape | (Dual) Trinity Standard | Three-File Skill Standard |
| `devops_sentinel.md` | Environment Shielding & Operations Security | `devops_agent.md` — Environment Agent |
| `github_sentinel.md` | Upstream Sync Auditor & Version Control Manager | `git_sync_agent.md` — Git Sync Auditor |
| `matrix_mapper.md` | (title kept) | `topology_mapper.md` |
| `skills/matrix-monitor/` | — | `skills/topology-monitor/` |
| `skills/governance-sentinel/` | — | `skills/compliance-checker/` (incl. `apply_jurisprudence.py` → `apply_rule_amendments.py`) |

## Work Breakdown Structure (waves executed, not a literal per-file WBS — this Phase ran as a single continuous session rather than a parallel multi-agent dispatch)

| Wave | Scope | Notable files |
| :--- | :--- | :--- |
| 0 | Project title & banner | `README.md`, `config/framework_identity.json`, `docs/standards/templates/README_TEMPLATE.md`, `docs/assets/logo/agents_banner.svg` (prompt text, `aria-label`, stale `ai-sprint/014`/`v3.4.0` refreshed) |
| 1 | Constitutional core | `agents.md` (all sections), `workflows/*.md` (10 files, incl. `matrix_workflow.md` → `pipeline_workflow.md`) |
| 2 | Agent role files | `agents/*.md` (13 files, incl. 3 renames: `devops_agent.md`, `git_sync_agent.md`, `topology_mapper.md`) |
| 3 | Commands | `commands/matrix.md` → `pipeline.md`, `audit.md`/`deployment.md`/`skill-forge.md` descriptions |
| 4 | Skills | `matrix-monitor/` → `topology-monitor/`, `governance-sentinel/` → `compliance-checker/`, ~26 other skill READMEs/SKILL.md (excl. `-3rd`), `manifest_skills.json` regenerated twice via `generate_manifest.py` (category/tags manually restored where the rename broke the generator's name-match preservation) |
| 5 | Docs | `docs/architecture/matrix_topology_map.md` → `topology_map.md`, `global_topology.md` layer nicknames, `docs/contracts/core/*`, `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md`, `docs/standards/templates/*` (7 templates), `rules/*.md` (6 files) |
| 6 | Runtime/infra (real code, not just prose) | `hooks/on_init.py` (`BRIDGE_SENTINELS` → `BRIDGE_ANCHORS`, log prefixes), `hooks/on_commit.py` (`audit_trinity_standard` → `audit_three_file_standard`, log prefixes, RA-XX), `tests/test_on_commit.py` (updated in lockstep, 56 tests re-verified green), `mcp_servers/github_mcp/*`, `claude/mcp.json` (`github-sentinel` key → `git-sync-agent`), `.github/workflows/ci.yml` (hard CI path blocker fixed same-commit), `scripts/render_readme.py` (credit-line generator strings) |
| 7 | `J-XX` → `RA-XX` sweep | Repo-wide, including `profiles/crypto-django/agents/backend_identity_specialist.md` (a host-family profile citing `J-02`, kept in sync since it's living content, not historical) |
| 8 | Closeout | This file, `CHANGELOG.md` `[Unreleased]` entry, graph rebuild, bridge re-install |

## Certification Checklist (Tactical — er, Sprint Closeout gate)
- [x] Case-insensitive repo-wide grep for every retired term (two passes — the second catching ALL-CAPS runtime strings the first, case-sensitive pass missed, e.g. `hooks/on_commit.py`'s `[DEVOPS SENTINEL]` and `skills/topology-monitor/scripts/legacy_app_auditor.py`'s `ANALYZING MATRIX CORE NODES`) returns zero hits outside declared non-goals (`-3rd` vendored skills, `kill_switch.sh` filename, "Nucleus", the market-data "Matrix index" comment in `polymarket-gamma-3rd`, generic non-pipeline uses of the word "matrix" as a decision-table/grid — e.g. "Onboarding Scenario Matrix", "Execution Matrix" comment, `.agents` "capability matrix") and historical record (`CHANGELOG.md` past entries, `docs/roadmaps/core/matrix/000-014-*.md`, `docs/sprints/core/matrix/031-032-*.md`, `docs/audits/TOKEN_ECONOMY_AUDIT-documentation-standard.md`).
- [x] `pytest` suite (56 tests) green after `hooks/on_commit.py` and `tests/test_on_commit.py` renames.
- [x] `skills/slash-commander/scripts/verify_commands.py`, manifest↔skills parity check, `skills/topology-monitor/scripts/legacy_app_auditor.py`, `scripts/verify_references.py` all green locally (CI-equivalent).
- [x] Banner (`docs/assets/logo/agents_banner.svg`) rendered to PNG and visually inspected — new prompt text fits the canvas, cursor position adjusted.
- [x] `CHANGELOG.md` `[Unreleased]` entry added; this file's `status` flipped to `COMPLETED (100%)` at close.

## Known follow-ups (out of scope for this Sprint, not blocking)
- **Phase 016 (deferred folder rename)**: `docs/roadmaps/core/matrix/` → `.../pipeline/`, `docs/sprints/core/matrix/` → `.../pipeline/`, and `docs/active_state.json`'s `active_app: "matrix"` — blocked on Phase 13 closing first (same folder, unrelated `IN_PROGRESS` track).
- **`skills/skill-creator-3rd/` leftover directory**: exists on disk alongside the already-renamed `skills/skill-creator/` (per `v3.5.1`'s own changelog entry) and is missing a `SKILL.md`, which `manifest_skills.json` parity checks and `generate_manifest.py` both flag as a pre-existing warning. Predates this Phase; not caused by it; not fixed here (unrelated cleanup, not a naming/vocabulary issue).
- **`skills/compliance-checker/scripts/kill_switch.sh`**: its header comment hardcodes `# 🛡️ CryptoBot Kill Switch (Rule 67)` — a specific host project name leaked into a framework-shared skill script, structurally the same class of leak Phase 14 closed for personal contact info. Left untouched here since it's an identity/host-leak issue, not an institutional-vocabulary one — flagged for a future Phase in the same family as Phase 14.
- **Hosts already bridged to an older `.agents` pin**: after bumping to the commit that includes this Phase, `.claude/{agents,commands,skills}` will retain dangling symlinks under the old names (`matrix.md`, `matrix_mapper.md`, `devops_sentinel.md`, `github_sentinel.md`, `matrix-monitor/`, `governance-sentinel/`) until they re-run `install_claude.py` or clear those directories manually — no automatic migration exists (same caveat the pre-Phase bridge audit already flagged).
- **`skills/README.md`**: still documents a `core/`/`local/`/`3rd/` sub-layer topology that contradicts the current flat `skills/` rule (`agents.md §3 topological_order`) — pre-existing documentation staleness, unrelated to this Phase's vocabulary scope, left as a separate finding.

---
*Closed 2026-07-26, branch `ai-sprint/015`, pending PR against `GstMirabal/.agents`.*
