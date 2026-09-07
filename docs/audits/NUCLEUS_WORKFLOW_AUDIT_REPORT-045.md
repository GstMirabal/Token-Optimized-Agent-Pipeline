# 🏛️ Nucleus Workflow Audit Report

**Audit ID**: #A045-7f3c
**Auditor**: rule_validator
**Date**: 2026-09-07
**Sprint**: 045 (nucleus-ruleset-mechanism-audit) — Phase 6, Unit 2
**Mode**: NUCLEUS
**Branch**: ai-sprint/045
**Scope**: the 12 files in `workflows/`
**Nature**: classification + drafted amendments only. This report **applies nothing** (`IMPLEMENTATION_PLAN.md` decision D1). No `workflows/*.md`, `agents.md`, or `rules/*.md` file was edited.

---

## 🚦 Executive Summary

| Verdict | Count | Workflows |
| :--- | :--- | :--- |
| **VIGENTE** | 6 | `close_workflow`, `deployment_workflow`, `extract_workflow`, `pipeline_workflow`, `reconciliation_workflow`, `start_workflow` |
| **MEJORAR** | 6 | `audit_workflow`, `remediation_workflow`, `repository_hardening_workflow`, `reverse_documentation_workflow`, `skill_forge_workflow`, `standardization_workflow` |
| **OBSOLETA** | 0 | — |

No workflow is wholly superseded; every one has a live, distinct purpose and at least one resolving invoker. The six `MEJORAR` verdicts are driven by dead sub-references, non-canonical artifact names, and steps whose verbs do not state an operation (`agents.md §1 unambiguous_action`).

| Metric | Score | Status |
| :--- | :--- | :--- |
| Frontmatter `invoked_by:` present (RA-16) | 12/12 | 🟢 |
| Frontmatter `invoked_by:` fully resolves (file + anchor) | 11/12 | 🟡 |
| Script / skill / `make` targets cited resolve on disk | all but the `precision_audit` "dry-run mode" claim | 🟡 |
| `§` / `RA-NN` citations resolve | all resolve | 🟢 |
| Step verbs classifiable by `map_workflows.py` | 49 of ~150 unclassified (`?`) | 🟡 |

---

## Method

1. Full read of all 12 `workflows/*.md` (partial reads not needed; largest is `close_workflow.md` at 39 lines of table but wide cells — read whole).
2. Every `§`, `RA-NN`, `Rule NN`, file path, script name and `make` target cross-checked with `Glob`/`Grep` against the tree:
   - `Glob scripts/*.py` (39 files), `Glob skills/*/scripts/*.py`, `Glob hooks/*.py`, `Glob commands/*.md` (13), `Glob config/*.json` (7), `Glob rules/*.md` (11), `Glob docs/guides/*.md` (5), `Glob docs/architecture/*.md` (2), `Glob docs/audits/*.md` (7), `Glob docs/roadmaps/core/pipeline/*.md`.
   - `Grep` for section anchors in `rules/documentation_standard.md` (`§2.1`, `§3.1`, `§4.1` confirmed present), `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` (`§3.2` confirmed present), `rules/qa_and_testing.md` (`functional_lock` — **not found**), `Makefile` (`model-ledger`, `cursor-tiers`, `docs-freshness-check`, `graphify-update`, `graphify-rebuild`, `verify`, `role-artifacts`, `session-start` — all present).
   - `Read` of `skills/skillopt/scripts/train_runner.py` (lines 1-199) to establish what the cited `train_runner.py` actually does.
3. Deterministic evidence supplied by the dispatching agent taken as given: `make verify` green except `check_task_scope.py --current-sprint` (Sprint 045's own mid-build scaffold — ignored); `scan_workflow_determinism.py` no candidates; `verify_commands.py` 13 commands resolve.
4. Every finding row cites its reproducing `Grep`/`Glob` or a `file:line`.

---

## Table 1 — Per-workflow verdict

| Workflow | Verdict | Step-level findings (count) | Proposed amendment (drafted, NOT applied) |
| :--- | :--- | :--- | :--- |
| `audit_workflow.md` | **MEJORAR** | 5 | Replace `precision_audit`'s bare `train_runner.py` "dry-run mode" with a real command + config path or delete the step; correct `nomenclature`'s decommissioned `[Stack]/[Layer]/[Sprint_ID]` structure to the canonical `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/` (`agents.md §5 mandatory_topology`); rename output artifact `pipeline_audit_report.md` → `docs/audits/PIPELINE_AUDIT_REPORT-[Sprint_ID].md` (RA-06 Option B, matches the existing `PIPELINE_AUDIT_REPORT-042.md`); make the two Phase-1/2 script paths consistent (`skill_standard_check` uses `.agents/skills/…`, `link_audit` uses `skills/…` in the same protocol) and add the nucleus path form as every other workflow does. |
| `close_workflow.md` | **VIGENTE** | 1 | In `rules_optimization`, state the exact `train_runner.py` invocation (config file, `--skill`/eval flag) and its done-criterion, or mark the step advisory; today it is "Optimize rules via … if failures or governance rule changes occur (requires explicit authorization)" with no command. All other references resolve and the nucleus/host asymmetry is handled explicitly. |
| `deployment_workflow.md` | **VIGENTE** | 1 | `production_bridge` ("Map/mount production environment variables securely. Apply pending `.sql` migrations.") states no operation, no tool, no done-criterion and is host/stack-specific; scope it "host-only, project-defined" and reference the host's own deployment runbook, or give it a check. Every script, `RA-NN` and gate citation resolves. |
| `extract_workflow.md` | **VIGENTE** | 0 (2 classifier false-positives) | None required. `amnesia_test` and `upstream_feedback` are flagged `?` by `map_workflows.py` because their verbs are "Apply the …"; the cell content is precise and gated. Optionally rename to an operation verb to clear the heuristic. |
| `pipeline_workflow.md` | **VIGENTE** | 0 | None. All 8 phases name a deliverable, a canonical path, a check script (`check_task_scope.py`, `check_gate_log.py`, `check_role_artifact.py`, `check_forge_ladder.py`, `audit_plan.py`, `loop_guard.py` — all present) and a done-criterion. No `?` steps. |
| `reconciliation_workflow.md` | **VIGENTE** | 0 | None. 8 phases, each a named operation with a closed input range; `detect_drift.py`, `graphify update`, `make verify`, `.agent_state/mirror.json` all resolve. |
| `remediation_workflow.md` | **MEJORAR** | 4 | Frontmatter `invoked_by: … rules/qa_and_testing.md#functional_lock` — **the `#functional_lock` anchor does not exist** in that file (`Grep functional_lock rules/qa_and_testing.md` → no matches). Repoint to `rules/qa_and_testing.md §4` (RA-17 verdict classes — the real trigger: 3rd consecutive `REJECTED`). Give `state_nuke` / `roadmap_tag` a scripted command or explicit manual done-criterion. Reconcile `negative_ki` ("Inject logic tag into `agents.md` via Governance Learner … No memory logs are kept") with `agents.md §4 constitutional_escalation` ordering — an emergency mid-loop write to `agents.md` needs the escalation path named. |
| `repository_hardening_workflow.md` | **MEJORAR** | 8 (all steps) | All 8 Execution-Flow rows are prose sentences ("Secret scanning, push protection, private vulnerability reporting", "Dependabot alerts and security updates", …), not named operations — `map_workflows.py` classifies every one `?`. Give each a step id + an operation verb + a verify command (the `gh api` calls already in the phase bodies). Add a nucleus/host mode line: RA-16 precedent records this protocol "shipped in PR #29 and was never run against this repository"; state whether it applies to the nucleus and, if so, wire its result into `platform_probe`. |
| `reverse_documentation_workflow.md` | **MEJORAR** | 11 | Phases 2, 3, 4.5, 5, 6, 6.5, 6.7, 7, 8, 9, 9.5 are `**Bold sentence.**` prose, not named operations (11 of ~13 steps `?`). Fractional numbering is deliberately frozen (RA-14, stated in-file) so **do not renumber**; instead add a parenthetical step id to each row (`Phase 5 (correct_false)`, `Phase 6 (write_contracts)` …) so the map can classify. Frontmatter invoker `audit_workflow.md#findings-handoff` resolves only loosely — Phase 9.5 is titled "Findings handoff", not slugged `findings-handoff`; align the anchor. |
| `skill_forge_workflow.md` | **MEJORAR** | 3 | `skillopt_run` cites bare `train_runner.py` — use the full path `skills/skillopt/scripts/train_runner.py` (the file resolves nowhere else; `close_workflow.md` already spells this out and explains why). `forge_destination` option (b) says `.agents/profiles/[name]/skills/` but omits the real-project path — add `scripts/install.py --profile-path <host path>` per `agents.md §3 topological_order` / `RA-15` (production profiles never committed to the public nucleus). Steps `role_lock`, `sterile_dev`, `smoke_test`, `authorization` also `?` — add operation verbs. |
| `standardization_workflow.md` | **MEJORAR** | 3 | Phase 6 "All scenarios end with: … `docs/0_SYSTEM_OVERVIEW.md` materialized …" names only the one anchor, but `agents.md §0` and `close_workflow.md` `history_sync` both assume this workflow also scaffolds the **sibling anchor `0_SYSTEM_ARCHITECTURE.md`** (`rules/documentation_standard.md §2` places C4 Level 2 there). Add `0_SYSTEM_ARCHITECTURE.md` to the Phase 6 end-state list. `condition_check` is passive ("Triggered if … are detected") — state who runs the detection and with what. Phases 3 / routing table use bare `/docs/` `/backend/` paths and `/backend/` is host-only with no nucleus note. |
| `start_workflow.md` | **VIGENTE** | 0 | None. Most cross-referenced protocol in the corpus; every script (`session_start.py`, `detect_drift.py`, `session_state.py`, `session_probe.py`, `sync_agents_pin.py`, `bridge_state.py`, `check_venv_relocatable.py`, `state_mirror.py`, `persist_session_context.py`) resolves, nucleus path forms are given throughout, no `?` steps. |

---

## Table 2 — Step-level findings register

| Workflow | Step | Issue | Verdict | Evidence | Proposed fix |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `audit_workflow.md` | `precision_audit` | "Evaluate rules in dry-run mode via `train_runner.py` (requires explicit authorization)" — no command, no config path, and no `--dry-run` mode exists. The only `train_runner.py` is `skills/skillopt/scripts/train_runner.py`, whose eval path is gated on `--skill` and pulls `scripts.train` / `scripts.eval_only` from the SkillOpt PyPI package (`Read train_runner.py:161-196`). Verb "Evaluate … in dry-run mode" is not an executable instruction. | MEJORAR (broken/ambiguous reference) | `workflows/audit_workflow.md:20`; `Glob skills/*/scripts/*.py` → single `train_runner.py`; `Read skills/skillopt/scripts/train_runner.py:1-6,161-196` | Replace with an exact invocation (`.agents/venv_skillopt/bin/python skills/skillopt/scripts/train_runner.py --skill … --config …`) and a done-criterion, or delete the step and fold rule/ruleset consistency checking into `rule_introspection`. |
| `audit_workflow.md` | `nomenclature` | Cites the `[Stack]/[Layer]/[Sprint_ID]` "dictionary structure". `agents.md §5 mandatory_topology` records this as one of four decommissioned forms; canonical is `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`. Also "forcibly auto-corrects any file evading" is a destructive verb with no dry-run / approval gate (`agents.md §2 destructive_flags`). | MEJORAR (dead reference + destructive verb) | `workflows/audit_workflow.md:19`; `agents.md §5 mandatory_topology` | Use the canonical path string; change "forcibly auto-corrects" to "reports … as a rename candidate for human approval". |
| `audit_workflow.md` | `report` | Output artifact named `pipeline_audit_report.md` — lowercase, no directory, no sprint suffix. Violates RA-06 Option B; the live convention is `docs/audits/PIPELINE_AUDIT_REPORT-[ID].md`. | MEJORAR (naming) | `workflows/audit_workflow.md:22`; `Glob docs/audits/*.md` → `PIPELINE_AUDIT_REPORT-042.md` | Rename to `docs/audits/PIPELINE_AUDIT_REPORT-[Sprint_ID].md`. |
| `audit_workflow.md` | `skill_standard_check` vs `link_audit` | Same protocol, inconsistent path form: `skill_standard_check` runs `.agents/skills/topology-monitor/scripts/legacy_app_auditor.py` (host prefix, breaks in nucleus); `link_audit` runs `skills/slash-commander/scripts/verify_commands.py` (nucleus form). | MEJORAR (nucleus parity) | `workflows/audit_workflow.md:17` and `:21`; both scripts confirmed present via `Glob skills/*/scripts/*.py` | State both path forms per step as `start_workflow.md` / `close_workflow.md` do. |
| `audit_workflow.md` | `rule_introspection` | Verb "Cross-reference `rules/` against `agents.md` to highlight overlaps or contradictions" has no output artifact and no done-criterion; `map_workflows.py` marks it `?`. | MEJORAR (ambiguous_action) | `workflows/audit_workflow.md:16`; `WORKFLOWS_STEP_MAP_GUIDE.md` line `audit_workflow: rule_introspection … ?` | Name the output (append to the `report` artifact) and a done-criterion ("every overlap listed with both citations"). |
| `close_workflow.md` | `rules_optimization` | "Optimize rules via `skills/skillopt/scripts/train_runner.py` if failures or governance rule changes occur (requires explicit authorization)" — conditional, no command args, no done-criterion; `?` in the map. Path itself resolves. | VIGENTE (workflow) / step is MEJORAR | `workflows/close_workflow.md:17`; `WORKFLOWS_STEP_MAP_GUIDE.md` line `close_workflow: rules_optimization … ?` | Give the exact invocation and exit-code done-criterion, or mark it advisory-only. |
| `close_workflow.md` | `history_sync` | Requires stamping `0_SYSTEM_ARCHITECTURE.md` on structural sprints, but no onboarding workflow is shown to create it (see `standardization_workflow.md` finding). Correctly marks both Entry Point anchors host-only. | VIGENTE (cross-workflow gap, owned by `standardization_workflow.md`) | `workflows/close_workflow.md:20`; `workflows/standardization_workflow.md:50` | Fix in `standardization_workflow.md` Phase 6 end-state list (below). |
| `close_workflow.md` | `session_lock` | `?` in the map, but cell content ("Output the official seal: `SESSION LOCKED`") is unambiguous. | VIGENTE (classifier false-positive) | `WORKFLOWS_STEP_MAP_GUIDE.md` line `close_workflow: … session_lock … ?` | No change needed; heuristic limitation noted in Meta-findings. |
| `deployment_workflow.md` | `production_bridge` | "Map/mount production environment variables securely. Apply pending `.sql` migrations." — no operation verb, no tool, no done-criterion, host/stack-specific. `?` in the map. | MEJORAR (ambiguous_action) | `workflows/deployment_workflow.md:20`; `WORKFLOWS_STEP_MAP_GUIDE.md` line `deployment_workflow: … production_bridge … ?` | Scope explicitly "host-only, project-defined"; point to the host's deployment runbook; or supply a check. |
| `deployment_workflow.md` | `git_state_gate` | `?` in the map; cell ("`DevOps Agent` halts execution if `git status --porcelain` detects uncommitted changes") is a clear condition but phrased as a state, not an operation. | VIGENTE (near-classifier false-positive) | `workflows/deployment_workflow.md:16` | Rephrase "Run `git status --porcelain`; exit 2 if non-empty". |
| `extract_workflow.md` | `amnesia_test`, `upstream_feedback` | `?` in the map; both cells are precise, gated procedures. | VIGENTE (classifier false-positive) | `WORKFLOWS_STEP_MAP_GUIDE.md` lines `extract_workflow: amnesia_test, upstream_feedback` | Optional verb rename only. |
| `remediation_workflow.md` | frontmatter `invoked_by` | Second invoker `rules/qa_and_testing.md#functional_lock` — anchor does not exist. `Grep functional_lock rules/qa_and_testing.md` → no matches. The real trigger lives in that file's §4 (RA-17 verdict classes) and `pipeline_workflow.md` Phase 7. | MEJORAR (dead reference — RA-16) | `workflows/remediation_workflow.md:4`; `Grep functional_lock rules/qa_and_testing.md` → "No matches found" | Repoint to `rules/qa_and_testing.md §4` (or `#4-…` slug) and `pipeline_workflow.md#7-quality-gate`. |
| `remediation_workflow.md` | `state_nuke`, `error_mining`, `negative_ki`, `session_lock` | All `?` in the map. `error_mining` cites `memory/telemetry/raw_errors.json` (consistent with `extract_workflow.md` / `hooks/telemetry.py`). `state_nuke` runs `git restore . && git clean -fd` — destructive, gated by `reversibility` above it (good), but no explicit done-criterion. `negative_ki` writes `agents.md` mid-emergency with "No memory logs are kept" — tension with `agents.md §4 constitutional_escalation` which routes systemic changes through indexing before purge. | MEJORAR (ambiguous_action + governance-ordering) | `workflows/remediation_workflow.md:16-21`; `WORKFLOWS_STEP_MAP_GUIDE.md` `remediation_workflow: state_nuke, error_mining, negative_ki, session_lock` | Add per-step done-criteria; name the `constitutional_escalation` path that `negative_ki` uses even under emergency. |
| `repository_hardening_workflow.md` | all 8 phases | Execution-Flow rows are prose sentences, not named operations — every one `?`. No step id, no operation verb, no verify command in the table (commands live only in the phase prose below). | MEJORAR (ambiguous_action, systemic) | `workflows/repository_hardening_workflow.md:22-31`; `WORKFLOWS_STEP_MAP_GUIDE.md` `repository_hardening_workflow: ALL 8 steps` | Add `| Phase | Step id | Operation | Verify |` shape; lift the `gh api` verify calls from the prose into the table. |
| `repository_hardening_workflow.md` | protocol execution status | RA-16 precedent: "`/agents:harden` shipped in PR #29 and was never run against this repository — five platform controls sat disabled for weeks". No nucleus/host applicability line; no recorded run against the nucleus. | MEJORAR (never-executed protocol) | `agents.md §7 RA-16`; `workflows/repository_hardening_workflow.md` has no mode section | State nucleus applicability; if it applies, feed its outcome into `start_workflow.md` `platform_probe` so a never-run state is visible. |
| `reverse_documentation_workflow.md` | phases 2,3,4.5,5,6,6.5,6.7,7,8,9,9.5 | `**Bold sentence.**` prose steps, not named operations — 11 of ~13 `?`. Fractional numbering is intentionally frozen (RA-14, stated in-file line 51) so renumbering is prohibited. | MEJORAR (ambiguous_action, structural) | `workflows/reverse_documentation_workflow.md:35-48`; `WORKFLOWS_STEP_MAP_GUIDE.md` `reverse_documentation_workflow: steps 2,3,4.5,5,6,6.7,7,8,9,9.5,10` | Add a parenthetical step id per row without changing phase numbers (`Phase 5 (correct_false)` …). |
| `reverse_documentation_workflow.md` | frontmatter `invoked_by` | `audit_workflow.md#findings-handoff` and the reciprocal in `audit_workflow.md` — Phase 9.5 is titled "Findings handoff", not slugged `findings-handoff`; anchor resolves only by intent. | MEJORAR (loose anchor) | `workflows/audit_workflow.md:4`; `workflows/reverse_documentation_workflow.md:47` | Align the slug or add an explicit `<a id="findings-handoff">`. |
| `skill_forge_workflow.md` | `skillopt_run` | Bare `train_runner.py` with no path; "(requires explicit authorization)"; `?` in the map. File resolves only at `skills/skillopt/scripts/train_runner.py`. | MEJORAR (citation) | `workflows/skill_forge_workflow.md:19`; `Glob skills/*/scripts/*.py` | Use the full path (as `close_workflow.md:17` does) and an exit-code done-criterion. |
| `skill_forge_workflow.md` | `forge_destination` | Option (b) names `.agents/profiles/[name]/skills/` only; omits the real-project host-controlled path installed via `scripts/install.py --profile-path` (`agents.md §3 topological_order`, `RA-15`, Sprint 028). | MEJORAR (incomplete routing) | `workflows/skill_forge_workflow.md:16`; `agents.md §3 topological_order`, `§7 RA-15` | Add the `--profile-path` real-project route; keep `profiles/[name]/` for illustrative packs only. |
| `skill_forge_workflow.md` | `role_lock`, `sterile_dev`, `smoke_test`, `authorization` | `?` in the map — verbs are noun-phrases or "Led by …". `smoke_test` and `authorization` cells are otherwise clear. | MEJORAR (ambiguous_action, minor) | `WORKFLOWS_STEP_MAP_GUIDE.md` `skill_forge_workflow: role_lock, sterile_dev, skillopt_run, smoke_test, authorization` | Operation-verb rename. |
| `standardization_workflow.md` | Phase 6 end-state list | "All scenarios end with: … `docs/0_SYSTEM_OVERVIEW.md` materialized …" — omits `0_SYSTEM_ARCHITECTURE.md`, which `agents.md §0`, `close_workflow.md` `history_sync` and `rules/documentation_standard.md §2` all treat as a scaffolded sibling anchor. | MEJORAR (cross-workflow gap) | `workflows/standardization_workflow.md:50`; `workflows/close_workflow.md:20`; `rules/documentation_standard.md:22`; `Grep 0_SYSTEM_ARCHITECTURE` → present in `close_workflow.md`, `documentation_standard.md`, 12 PHASE_REGISTERs, never in `standardization_workflow.md` | Add `docs/0_SYSTEM_ARCHITECTURE.md` (from its template) to the Phase 6 end-state list. |
| `standardization_workflow.md` | `condition_check` | "Triggered if naming drift, empty folders, or asymmetric roadmaps are detected." — passive, no actor, no detection tool. `?` in the map. | MEJORAR (ambiguous_action) | `workflows/standardization_workflow.md:15`; `WORKFLOWS_STEP_MAP_GUIDE.md` `standardization_workflow: condition_check …` | State who runs detection and with which script (`legacy_app_auditor.py` / `noise_purge`). |
| `standardization_workflow.md` | Phase 3 / Legacy Routing Table | Bare `/docs/` and `/backend/` paths; `/backend/` is host-only and has no nucleus note; several routing-table and Scenario-Matrix rows are misparsed as steps by `map_workflows.py` (the `+ 7 table-row artifacts` in the `?` list). | MEJORAR (nucleus parity + map noise) | `workflows/standardization_workflow.md:18,35-46`; `WORKFLOWS_STEP_MAP_GUIDE.md` `standardization_workflow: … + 7 table-row artifacts` | Mark `/backend/` host-only; consider moving the routing table out of the step-parsed section or tagging rows so `map_workflows.py` skips them. |
| `pipeline_workflow.md` | — | No step-level defect found. All phases name deliverable + canonical path + check + done-criterion. | VIGENTE | `workflows/pipeline_workflow.md:13-24`; every cited script present in `Glob scripts/*.py` | None. |
| `reconciliation_workflow.md` | — | No step-level defect found. | VIGENTE | `workflows/reconciliation_workflow.md:39-47`; `detect_drift.py` present | None. |
| `start_workflow.md` | — | No step-level defect found; nucleus path forms supplied per step. | VIGENTE | `workflows/start_workflow.md:22-37`; all cited scripts present | None. |

---

## Broken / dead-reference list (the OBSOLETA-class citations)

No workflow *file* is OBSOLETA, but these individual references are dead or non-resolving and must be corrected before the next `verify_references.py` extension:

1. **`remediation_workflow.md:4`** — frontmatter `invoked_by: … rules/qa_and_testing.md#functional_lock`. The `#functional_lock` anchor does not exist (`Grep functional_lock rules/qa_and_testing.md` → no matches). `verify_references.py` / `make verify` do not currently validate `invoked_by` sub-anchors, so this passed the gate.
2. **`audit_workflow.md:20`** — `precision_audit` "Evaluate rules in dry-run mode via `train_runner.py`". No `--dry-run` mode exists; the sole `train_runner.py` (`skills/skillopt/scripts/train_runner.py`) is a SkillOpt training/eval runner needing `--skill` + `--config` and the SkillOpt PyPI `scripts.train` module. Instruction is not executable as written.
3. **`audit_workflow.md:19`** — `nomenclature` cites the decommissioned `[Stack]/[Layer]/[Sprint_ID]` topology (`agents.md §5 mandatory_topology` lists it among four superseded forms; canonical is `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`).
4. **`audit_workflow.md:22`** — `report` output `pipeline_audit_report.md` is not RA-06 Option B and does not match the live `docs/audits/PIPELINE_AUDIT_REPORT-042.md` convention.
5. **`standardization_workflow.md:50` vs `close_workflow.md:20` / `rules/documentation_standard.md:22`** — `0_SYSTEM_ARCHITECTURE.md` is consumed (stamped at close, hosts C4 Level 2) but never listed as produced by the onboarding workflow.
6. **`audit_workflow.md:17`** — `.agents/skills/…` host-prefixed path in a nucleus-aware protocol whose sibling step uses the bare `skills/…` form; breaks under nucleus resolution.
7. **`reverse_documentation_workflow.md:47` / `audit_workflow.md:4`** — reciprocal `#findings-handoff` anchor is a title, not a slug/id.

---

## Worst step-ambiguity clusters (`unambiguous_action`)

| Rank | Workflow | Unclassified steps | Character |
| :--- | :--- | :--- | :--- |
| 1 | `repository_hardening_workflow.md` | 8 of 8 | Entire Execution-Flow table is prose sentences; no step ids at all. |
| 2 | `reverse_documentation_workflow.md` | 11 of ~13 | `**Bold sentence.**` phases; renumber-locked by RA-14, so needs parenthetical ids. |
| 3 | `standardization_workflow.md` | `condition_check`, `Gate`, `human_ok`, `absorb` + ~7 routing/scenario rows misparsed as steps | Mix of real passive-voice steps and table-row noise the map cannot skip. |
| 4 | `skill_forge_workflow.md` | 5 of 8 (`role_lock`, `sterile_dev`, `skillopt_run`, `smoke_test`, `authorization`) | Noun-phrase and "Led by …" verbs. |
| 5 | `remediation_workflow.md` | 4 of 7 (`state_nuke`, `error_mining`, `negative_ki`, `session_lock`) | Emergency steps with destructive verbs but no per-step done-criteria. |

Genuine classifier false-positives (content is unambiguous; `map_workflows.py` heuristic limitation, not a workflow defect): `close_workflow.md` `session_lock`, `deployment_workflow.md` `git_state_gate`, `extract_workflow.md` `amnesia_test` / `upstream_feedback`.

---

## Duplication (RA-14 spirit)

- **The SkillOpt `train_runner.py` mechanism is cited three ways in three workflows** with no shared definition: `audit_workflow.md` `precision_audit` (bare name, "dry-run mode"), `close_workflow.md` `rules_optimization` (full path, "Optimize rules … if failures occur"), `skill_forge_workflow.md` `skillopt_run` (bare name, "Optimize new `SKILL.md`"). Each carries its own "(requires explicit authorization)". Propose: one canonical invocation block (path, args, config, done-criterion, authorization gate) in `rules/skills_and_integrations.md` or `rules/token_economy.md`, referenced — not restated — by the three steps.
- **Zero-Memory Initialization** boilerplate ("subagents start with zero memory; the governance ruleset arrives auto-imported; re-read only after compaction — `anti_amnesia`") is restated verbatim in `audit_workflow.md` `init_check`, `close_workflow.md` `read_ruleset`, `extract_workflow.md` `read_ruleset`, `pipeline_workflow.md` Standards block, `start_workflow.md` `read_ruleset`. This one is arguably acceptable (each workflow is loaded independently) but is a candidate for a single referenced clause.
- **`docs/sprints/[Sprint_ID]-[Stack]-[Layer]/` canonical path** is correctly referenced (not restated) by `pipeline_workflow.md` and `close_workflow.md` per `agents.md §5` — the intended pattern. `audit_workflow.md` `nomenclature` is the one place that restated it and drifted (finding 3 above).

---

## Meta-findings (not workflow defects, but they let defects through)

1. **`invoked_by:` sub-anchor validation gap.** `make verify` / `scripts/verify_references.py` check (d) confirms a workflow *has* an invoker and that filename mentions resolve, but does not resolve `#anchor` fragments inside `invoked_by:`. That is why `remediation_workflow.md#functional_lock` passed. Propose extending check (d) to resolve `file.md#anchor` against the target file's headings/step ids.
2. **`map_workflows.py` step-verb heuristic.** 49 `?` classifications conflate three distinct causes: (a) genuine ambiguous verbs (`repository_hardening`, `standardization` `condition_check`), (b) prose-sentence step rows with real content (`reverse_documentation`), (c) non-step table rows misparsed as steps (`standardization` routing table). The generated guide already says it leaves `?` visible rather than guessing — correct — but a downstream reader cannot tell (a) from (c). Propose a second column or a skip-marker for non-step tables.
3. **Never-executed protocol visibility.** `repository_hardening_workflow.md` has no mechanism to record whether it has ever run against a given repository; `start_workflow.md` `platform_probe` only *proposes* it. RA-16's own precedent is this workflow. Propose a `last_harden_run` field alongside `last_platform_probe` in `docs/active_state.json`.

---

## Proposed amendments (drafted — NOT applied)

Per `IMPLEMENTATION_PLAN.md` D1 this sprint applies nothing. The following are the drafted texts for a later sprint to apply.

**A1 — `workflows/remediation_workflow.md` frontmatter**
```
invoked_by: human:/agents:remediation, rules/qa_and_testing.md#4-verdict-classes, pipeline_workflow.md#7-quality-gate
```
(replace `rules/qa_and_testing.md#functional_lock`; use the actual slug of the §4 verdict-classes heading.)

**A2 — `workflows/audit_workflow.md` `precision_audit` row**
```
| **2. Doc Purity** | `precision_audit` | Run the SkillOpt rules-consistency pass ONLY on explicit human authorization:
`.agents/venv_skillopt/bin/python skills/skillopt/scripts/train_runner.py --skill agents.md --config <path> --eval-only`
(nucleus: `venv_skillopt/bin/python skills/skillopt/scripts/train_runner.py …`). Done-criterion: exit 0 and a
written diff of proposed edits — no edit is applied in this step. If SkillOpt is not installed, record
"precision_audit skipped: skillopt stack absent" and continue. |
```

**A3 — `workflows/audit_workflow.md` `nomenclature` and `report` rows**
- `nomenclature`: replace `[Stack]/[Layer]/[Sprint_ID]` with `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`; change "forcibly auto-corrects any file evading" to "lists every file outside … as a rename candidate for human approval (`agents.md §2 destructive_flags`)".
- `report`: output artifact `docs/audits/PIPELINE_AUDIT_REPORT-[Sprint_ID].md` (RA-06 Option B).

**A4 — `workflows/standardization_workflow.md` Phase 6 end-state sentence**
```
All scenarios end with: `docs/` tree instantiated, `docs/0_SYSTEM_OVERVIEW.md` AND `docs/0_SYSTEM_ARCHITECTURE.md`
materialized from their templates, initial `docs/active_state.json`, and the Master Ledger (`CHANGELOG.md`) present
at the host root …
```

**A5 — `workflows/skill_forge_workflow.md` `skillopt_run` + `forge_destination`**
- `skillopt_run`: `skills/skillopt/scripts/train_runner.py` (full path) + exit-0 done-criterion.
- `forge_destination` option (b): add "for a real project, the host-controlled profile path installed with `scripts/install.py --profile-path <path>` (`RA-15`, Sprint 028) — never `profiles/[name]/` inside the public nucleus, which is for illustrative packs only".

**A6 — `workflows/repository_hardening_workflow.md`**
- Re-shape the Execution-Flow table to `| Phase | Step id | Operation | Verify |`, lifting the `gh api` verify calls from the phase prose.
- Add a "Mode" line: state nucleus applicability; on apply, write `last_harden_run` to `docs/active_state.json` and surface it in `start_workflow.md` `platform_probe`.

**A7 — `workflows/reverse_documentation_workflow.md`**
- Add parenthetical step ids to phases 2–10 without renumbering (RA-14).
- Add `<a id="findings-handoff"></a>` at Phase 9.5 (or align the frontmatter slug).

---

## 🛡️ Certification

**Certified by rule_validator under Pipeline Methodology v4.27.0 (Sprint 045, Phase 6, Unit 2).**
*Timestamp: 2026-09-07*
*Audit ID: #A045-7f3c*
*Deliverable lock: this is the single physical file authored by this subtask (`agents.md §2 jurisdictional_lock`). No `workflows/*.md`, `agents.md`, or `rules/*.md` file was modified.*
