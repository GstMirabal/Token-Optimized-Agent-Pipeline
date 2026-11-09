# Task Scope — Sprint 059 (core-pipeline)

Source: `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`, `## Design`, `## Tests`, `## Verification`, `## Abort criterion`).
Staffing authority: `agent_assignment.md` (its Assignee column overrides the plan's `Assignee (proposed)` and is used verbatim; the six overwrites A-00, A-07, H-01, C-01, D-01, F-01 are listed in its "Disagreements with the plan"). Tools: no `skill_assignment.md` was read for this artifact.
Phase 4.3 of `workflows/pipeline_workflow.md`. Enforced by `scripts/check_task_scope.py`.
Mode: `claude-code`, `delegation_mode: native`. Sprint id 59 >= `MODEL_FROM_SPRINT` (28), so Model and Effort are required. No template for this artifact exists under `docs/standards/templates/`; the shape comes from `scripts/check_task_scope.py` (`WORK_KEYS`: File, Operation, Risk, Assignee, plus Model and Effort).

## Tier transcription

Model and Effort are transcribed from each assignee's `agents/<role>.md` frontmatter (`model:`, `tier:`) and the `claude_code` column of `config/model_tiers.json` (`tiers.author.claude_code` = `sonnet` / `medium`; `tiers.mechanical.claude_code` = `haiku` / `low`). No tier is invented and no dated model ID is written. `session_tool` is `claude-code`, so `make cursor-tiers` does not apply.

| Assignee | model | tier | effort |
| :--- | :--- | :--- | :--- |
| `doc_orchestrator` | sonnet | author | medium |
| `rule_validator` | sonnet | author | medium |
| `implementer_agent` | sonnet | author | medium |
| `orchestrator` | sonnet | author | medium |
| `skill_architect` | sonnet | author | medium |
| `token_economy_agent` (measures for A-00 and H-01; owns no row) | sonnet | author | medium |
| `devops_agent` (measures for C-01; owns no row) | haiku | mechanical | low |

Declared escalations: none. No Work row is assigned to a `mechanical` profile, so the mechanical-at-high-risk check of `check_task_scope.py` does not apply. High-risk rows stay on the `author` tier: the adversarial check on them is the Phase 7 gate (`tier: gate`), not the author. Plan D20 returned `qa_agent` to `opus` under abort criterion 4; it is a gate profile and owns no row here.

## Work

Status values: ⏳ pending, ✅ committed (short SHA). Risk is transcribed from the plan. `after X` in Operation is the plan's dependency; G-01 and H-02 add the `Depends on`, `Est. cost` and `Suspend after` columns later, so they are not written here. Execution order and unit count: the plan's `## Work` and `## Cost`. Rows D-04, E-01b and F-02 are conditional on an ADR decision (see findings F-1 and F-8).

### Wave 1 — Cost levers

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-05 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify: record the triage verdicts of the plan Context (`F-116-N1`, `F-116-N2`: accept, with command and exit); C-02 marks both closed | low | `doc_orchestrator` | sonnet | medium | ✅ `1dbe533` |
| A-09 | `rules/code_craft.md` | modify: receive the measurement and history of linter_command, max_indentation, max_lines_per_func, fail_closed_claims, exception_handling moved out of agents.md (D10) | medium | `rule_validator` | sonnet | medium | ✅ `0c7a9b2` |
| A-10 | `rules/project_topology.md` | modify: receive the history and precedents of RA-09, RA-19, jurisdiction moved out of agents.md (D10) | medium | `rule_validator` | sonnet | medium | ✅ `a694ffe` |
| A-11 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify: receive the transport, channels, triage and closure of feedback_upstream moved out of agents.md (D10) | low | `doc_orchestrator` | sonnet | medium | ✅ `72ac88b` |
| A-13 | `docs/guides/RULE_PRECEDENTS_GUIDE.md` | create: receive the history, measurement and precedents of every agents.md row that A-12 trims and that A-09, A-10 and A-11 do not receive, indexed by section and rule key, moved verbatim (D10, D15) | medium | `doc_orchestrator` | sonnet | medium | ✅ `a014f4f` |
| A-15 | `rules/skills_and_integrations.md` | modify: receive verbatim `three_file_standard`, `topological_order`, `enforcement` from `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: the guide keeps a pointer in their place | low | `rule_validator` | sonnet | medium | ✅ `18b692e` |
| A-16 | `rules/qa_and_testing.md` | modify: receive verbatim `local_testing` from `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: the guide keeps a pointer in its place | low | `rule_validator` | sonnet | medium | ✅ `9b8db89` |
| A-17 | `rules/project_topology.md` | modify: receive verbatim `min_release_age`, `only_built_deps`, `config_file` from `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: the guide keeps a pointer and `config/rule_triggers.json` adds `pnpm-workspace.yaml`, `package.json`, `.npmrc` to that file's `globs` | low | `rule_validator` | sonnet | medium | ✅ `d133bc2` |
| A-12 | `agents.md` | modify: after A-09, A-10, A-11, A-13, A-15, A-16 and A-17, with the D18 allocation, trim rows to rule plus pointer, at most 20000 bytes, `make verify` exit 0; keep every string a test pins in `agents.md` (`grep -n "agents.md" tests/*.py`: `RA-18` in `tests/test_cursor_phase1.py`, the `EMITTED` line of `tests/test_gate_row_wording.py`, the `Command paths` row); RA-14 grep of each moved term and every citation updated in the same commit | high | `rule_validator` | sonnet | medium | ✅ `d6f5756` |
| A-14 | `docs/decisions/ADR-0021-qa-agent-tier-trial.md` | create: after A-12, supersede the `ADR-0003` clause for `qa_agent` only, for the D9 trial, with the abort criterion 4 return condition (D17); `ADR-0003` is not edited; mandatory companion `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` (`:19`, `:140`) | medium | `doc_orchestrator` | sonnet | medium | ✅ `ed96115` |
| A-08 | `agents/qa_agent.md` | modify: after A-14, set model sonnet and tier author (D9); mandatory companion `config/model_tiers.json` (move qa_agent to author.profiles, add the trial and its return criterion to the gate basis); mandatory companion `tests/test_agent_profile_census.py` (pins the gate list, keeps `qa_agent` without `Write`/`Edit`) | medium | `implementer_agent` | sonnet | medium | ✅ `80518b4`, reverted `8e8a566` (D20) |
| A-01 | `scripts/session_cost.py` | modify: fix( cycle_summary baseline D1 and segment_cycles cuts on context size (D19); paired test `tests/test_session_cost.py` (new) with a turn of cache_read 0 and cache_creation above 0 | medium | `implementer_agent` | sonnet | medium | ✅ `ef490cd`, `919d4f2` |
| A-19 | `CHANGELOG.md` | modify: D22, replace the host name with `a host project`, annotated in place; `git grep -c -i` of the name over the file gives 0 | low | `doc_orchestrator` | sonnet | medium | ✅ `4fb09a9` |
| A-20 | `docs/roadmaps/core/pipeline/014-identity-branding-hardening.md` | modify: D22, same as A-19 | low | `doc_orchestrator` | sonnet | medium | ✅ `28242ff` |
| A-21 | `docs/roadmaps/core/pipeline/015-terminology-and-nomenclature-hardening.md` | modify: D22, same as A-19 | low | `doc_orchestrator` | sonnet | medium | ✅ `a3c5a14` |
| A-22 | `docs/roadmaps/core/pipeline/016-folder-topology-migration.md` | modify: D22, same as A-19 | low | `doc_orchestrator` | sonnet | medium | ✅ `f72983e` |
| A-23 | `docs/roadmaps/core/pipeline/017-pre-publication-hardening.md` | modify: D22, same as A-19 | low | `doc_orchestrator` | sonnet | medium | ✅ `b6adb90` |
| A-24 | `docs/sprints/023-core-pipeline/task_scope.md` | modify: D22, same as A-19 | low | `doc_orchestrator` | sonnet | medium | ✅ `ff69f15` |
| A-25 | `tests/test_token_economy_soft_bound.py` | create: D23, equality against a reviewed copy of the soft row and the calibration sentence of `rules/token_economy.md` §3.1, and `probe_cost` returns None for a cycle at 6x; fails with the text of `d192075` (N3) and of `7779e7f` (F1) | low | `implementer_agent` | sonnet | medium | ✅ `1e1deda`, reduced `d059aac` (D32) |
| A-26 | `CHANGELOG.md` | modify: D24: replace the profile slug on lines 800, 811 and 934 and the business domain on line 764, annotated | low | `doc_orchestrator` | sonnet | medium | ✅ `4e34b49` |
| A-27 | `docs/roadmaps/core/pipeline/015-terminology-and-nomenclature-hardening.md` | modify: D24: replace the profile slug on line 52, annotated | low | `doc_orchestrator` | sonnet | medium | ✅ `59e6950` |
| A-28 | `docs/roadmaps/core/pipeline/016-folder-topology-migration.md` | modify: D24: replace the profile slug on line 33 and make lines 33 and 38 readable (round 6 F6) | low | `doc_orchestrator` | sonnet | medium | ✅ `271ee11` |
| A-29 | `docs/roadmaps/core/pipeline/017-pre-publication-hardening.md` | modify: D24: replace the profile slug on lines 21, 29, 39 and 48, annotated | low | `doc_orchestrator` | sonnet | medium | ✅ `fe48d2f` |
| A-30 | `workflows/reverse_documentation_workflow.md` | modify: D24: replace the business domain on line 28 with a generic description | low | `doc_orchestrator` | sonnet | medium | ✅ `af55026` |
| A-31 | `tests/test_profile_references.py` | create: D24: every tracked `profiles/<slug>` reference resolves to a real directory or a reviewed placeholder; fails at `d06c939` for each of the 4 files; states that it does not detect bare names | low | `implementer_agent` | sonnet | medium | ✅ `dbe243a` |
| A-32 | `rules/qa_and_testing.md` | modify: D25: the `RA-19` re-run after an S0 happens before the merge of the sprint that remediates it | low | `rule_validator` | sonnet | medium | ✅ `9382b80`, replaced `022924f` (D30) |
| A-33 | `agents/governance_learner.md` | modify: D26: learning destination table; remove the fixed `agents.md` Section 7 destination | low | `rule_validator` | sonnet | medium | ✅ `2d0d39b` |
| A-34 | `agents/rule_validator.md` | modify: D26: audit the destination `governance_learner` gives; remove the fixed `agents.md` destination | low | `rule_validator` | sonnet | medium | ✅ `24de04e` |
| A-35 | `workflows/remediation_workflow.md` | modify: D26: `negative_ki` routes by the `governance_learner` table instead of injecting into `agents.md` | low | `rule_validator` | sonnet | medium | ✅ `f052ea9` |
| A-36 | `agents.md` | modify: D26: `constitutional_escalation` routes through `governance_learner`; `wc -c agents.md` at most 20000 | low | `rule_validator` | sonnet | medium | ✅ `dc53642` |
| A-37 | `rules/documentation_standard.md` | modify: D26: `negative_ki` of this deadlock: do not describe conduct no instrument performs; if the table gives another destination, amend this row before writing | low | `rule_validator` | sonnet | medium | ✅ `d6b388c` |
| A-38 | `config/rule_triggers.json` | modify: D28: add `rules/*.md` to the globs of `rules/documentation_standard.md` | low | `rule_validator` | sonnet | medium | ✅ `408ad02` |
| A-39 | `agents.md` | modify: D28: section 0 row of `rules/documentation_standard.md`: `Editing any document under docs/ or rules/`; `wc -c agents.md` at most 20000 | low | `rule_validator` | sonnet | medium | ✅ `de19dad` |
| A-40 | `docs/roadmaps/core/pipeline/018-post-publication-field-hardening.md` | modify: D29: replace the business domain on line 36, annotated | low | `doc_orchestrator` | sonnet | medium | ✅ `6256efd` |
| A-41 | `skills/skillopt/data/scenarios.json` | modify: D29: replace the business domain on lines 58 and 59 | low | `doc_orchestrator` | sonnet | medium | ✅ `e6f27cb` |
| A-42 | `docs/roadmaps/core/pipeline/008-session-close-governance.md` | modify: D29: replace the domain on line 23, annotated | low | `doc_orchestrator` | sonnet | medium | ✅ `4bdcc49` |
| A-43 | `skills/mcp-registry/README.md` | modify: D29: replace the domain example on line 5 | low | `doc_orchestrator` | sonnet | medium | ✅ `f4d20dd` |
| A-44 | `profiles/example-project/mcp/registry.json` | modify: D29: replace the domain example on line 7 | low | `doc_orchestrator` | sonnet | medium | ✅ `66a4438` |
| A-45 | `docs/guides/RULE_PRECEDENTS_GUIDE.md` | modify: D29: replace the roles inherited from a host on line 205 | low | `doc_orchestrator` | sonnet | medium | ✅ `699eac3` |
| A-46 | `docs/standards/templates/HOTFIX_TEMPLATE.md` | modify: D33: route through `constitutional_escalation` on line 25 and link the assigned destination, no fixed `RA-XX` (N1) | low | `doc_orchestrator` | sonnet | medium | ✅ `05a6dab` |
| A-47 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify: D33: annotate the D23 and D25 Documentary impact rows (N2), mark D24 (N3), remove the figure from the `7a037351` session cost row (N5) | low | `doc_orchestrator` | sonnet | medium | ✅ `1473570` |
| A-48 | `tests/test_profile_references.py` | modify: D33: docstring (N4): narrow the claim to what the test checks and state the skipped files; no logic change | low | `implementer_agent` | sonnet | medium | ✅ `8923501` |
| A-49 | `scripts/check_log_append_only.py` | create: D34: exit 2 at `10c88f4` (N3), `1dbb43e` (F6) and `60383e3` (D24); exit 0 on `60383e3..HEAD` after A-47 | low | `implementer_agent` | sonnet | medium | ✅ `251717d`, reverted `120860b` (D35) |
| A-50 | `tests/test_check_log_append_only.py` | create: D34: throwaway git repositories for each zone, the trailer, its limits and the errors | low | `implementer_agent` | sonnet | medium | ✅ `3368dc5`, reverted `2c55575` (D35) |
| A-51 | `Makefile` | modify: D34: `verify` runs `check_log_append_only.py --current-sprint` | low | `implementer_agent` | sonnet | medium | ✅ `de239b7`, reverted `a4493b8` (D35) |
| A-52 | `rules/documentation_standard.md` | modify: D34: name the instrument and its limits beside the `annotated in place` row | low | `rule_validator` | sonnet | medium | ✅ `d40183d`, reverted `f328923` (D35) |
| A-53 | `scripts/check_log_append_only.py` | modify: D35: `fix(` with paired `tests/test_check_log_append_only.py`: `--current-sprint` root as in `check_gate_log.py`; `--sprint-dir` resolved from the git root; exit 2 on a missing directory, an empty range base or an absent record by hand; `Repro:` fails on the parent | low | `implementer_agent` | sonnet | medium | ✅ `f273f93`, reverted `873fb1e` (D35) |
| A-54 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify: D35: mark D23 and D26 as narrowed by D32 (R9-3) | low | `doc_orchestrator` | sonnet | medium | ✅ `822c047` |

### Wave 1b — Method (plan D37)

Operation: the plan row of the same id (plan D37).

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M-01 | `scripts/_current_sprint.py` | create: plan M-01 (D37) | medium | `implementer_agent` | sonnet | medium | ✅ `62bbce8` |
| M-02 | `scripts/check_task_scope.py` | modify: plan M-02 (D37) | low | `implementer_agent` | sonnet | medium | ✅ `80c5184` |
| M-03 | `scripts/check_gate_log.py` | modify: plan M-03 (D37) | low | `implementer_agent` | sonnet | medium | ✅ `7c9115c` |
| M-04 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify: plan M-04 (D37) | low | `skill_architect` | sonnet | medium | ✅ `e393405` |
| M-12 | `scripts/loop_guard.py` | modify: plan M-12 (D37) | low | `implementer_agent` | sonnet | medium | ✅ `d74a969` |
| M-05 | `tests/test_current_sprint_matrix.py` | create: plan M-05 (D37) | low | `implementer_agent` | sonnet | medium | ✅ `74eb9d7` |
| M-06 | `scripts/check_sprint_refs.py` | create: plan M-06 (D37) | medium | `implementer_agent` | sonnet | medium | ✅ `e15d86e`, `cc4f009` |
| M-07 | `Makefile` | modify: plan M-07 (D37) | low | `implementer_agent` | sonnet | medium | ✅ `a97991d` |
| M-08 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify: plan M-08 (D37) | low | `doc_orchestrator` | sonnet | medium | ✅ `1196fea` |
| M-09 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify: plan M-09 (D37) | low | `doc_orchestrator` | sonnet | medium | ✅ `2979326` |
| M-10 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | modify: plan M-10 (D37) | low | `doc_orchestrator` | sonnet | medium | ✅ `0e1cf6c` |
| M-11 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify: plan M-11 (D37) | low | `orchestrator` | sonnet | medium | ✅ `d988528` |
| M-13 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify: plan M-13 | low | `skill_architect` | sonnet | medium | ✅ `851a15d`, `1b84de0` |
| M-14 | `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | modify: plan M-14 | low | `orchestrator` | sonnet | medium | ✅ `17171a8` |
| M-15 | `scripts/_current_sprint.py` | modify: plan M-15 | low | `implementer_agent` | sonnet | medium | ✅ `e0185d8` |
| M-16 | `scripts/check_task_scope.py` | modify: plan M-16 | low | `implementer_agent` | sonnet | medium | ✅ `4f4ce82` |

### Wave 2 — Pace and autonomy

| # | File | Operation | Risk | Assignee | Model | Effort | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M-17 | `scripts/_current_sprint.py` | modify: plan M-17 | low | `implementer_agent` | sonnet | medium | - | ✅ `92bb5e7` |
| G-01 | `scripts/check_task_scope.py` | modify: add the `Depends on` column and a subcommand printing parallel batches (dependencies landed, disjoint files, at most 4); tests in `tests/test_check_task_scope.py` | medium | `implementer_agent` | sonnet | medium | - | ✅ `21080e9` |
| G-02 | `workflows/pipeline_workflow.md` | modify: after G-01, Phase 6 dispatches each batch in parallel with `isolation: "worktree"` and integrates in table order; after each batch the orchestrator removes every worktree and its branch (`git worktree remove`, `git branch -D`) and re-runs `check_task_scope.py` on `ai-sprint/[ID]`, exit 0, before the next batch; Phase 7 stays serial per wave (D11) | medium | `orchestrator` | sonnet | medium | G-01 | ✅ `808d098` |
| B-01 | `scripts/prompt_count.py` | create: count authorizations per session from transcripts, `--json`; test `tests/test_prompt_count.py` | medium | `implementer_agent` | sonnet | medium | - | ✅ `4952195` |
| B-07 | `workflows/close_workflow.md` | modify: after B-01, advisory step running `python3 scripts/prompt_count.py --session <id> --json` on the closing session; RA-16 invoker of B-01 | low | `orchestrator` | sonnet | medium | B-01 | ✅ `2d40946` |
| B-02 | `docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` | create: after B-01, baseline count for one real nucleus session and one genericized host session (RA-15) | low | `doc_orchestrator` | sonnet | medium | B-01 | ✅ `7fc8ae5` |
| B-06 | `scripts/install.py` | modify: after B-02, `install_nucleus_bridge` installs the `sandbox` block with `autoAllowBashIfSandboxed: true`, no hooks and no `excludedCommands` (D12); new test `tests/test_install_nucleus_sandbox.py` | high | `implementer_agent` | sonnet | medium | B-02 | ✅ `92fddf8` |
| E-01 | `scripts/session_state.py` | modify: fix( SessionEnd `suspend` acts only when the hook session_id matches the anchor (KI-057-2); paired test `tests/test_session_end_hook.py`; reproduce first or RECORD | medium | `implementer_agent` | sonnet | medium | - | ✅ `c10f8bd` |
| E-01c | `scripts/session_state.py` | modify: after E-01, fix( `suspend` between sprints (sealed sprint, session `IN_PROGRESS`) releases the session lock without touching the sealed sprint; paired test in `tests/test_session_state.py` | medium | `implementer_agent` | sonnet | medium | E-01 | ✅ `3a3136b` |
| M-18 | `scripts/check_task_scope.py` | modify: plan M-18 | low | `implementer_agent` | sonnet | medium | - | ✅ `c5fbf5f` |
| M-19 | `scripts/prompt_count.py` | modify: plan M-19 | medium | `implementer_agent` | sonnet | medium | - | ✅ `d534c04` |
| M-20 | `scripts/prompt_count.py` | modify: plan M-20 | low | `implementer_agent` | sonnet | medium | M-19 | ✅ `10c8e1a` |
| M-21 | `docs/plans/README.md` | modify: plan M-21 | low | `doc_orchestrator` | sonnet | medium | - | ✅ `e6caffc` |
| B-08 | `docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` | modify: plan B-08 | medium | `doc_orchestrator` | sonnet | medium | M-20, B-06 | ✅ `9e55888` |
| B-09 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify: plan B-09 | low | `orchestrator` | sonnet | medium | - | ✅ `0cbf261` |
| M-22 | `scripts/check_task_scope.py` | modify: plan M-22 | low | `implementer_agent` | sonnet | medium | - | ✅ `639fd05` |
| M-23 | `scripts/install.py` | modify: plan M-23 | low | `implementer_agent` | sonnet | medium | - | ✅ `104467f` |
| B-10 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify: plan B-10 | low | `orchestrator` | sonnet | medium | - | ✅ `1b99872` |
| M-24 | `scripts/check_task_scope.py` | modify: plan M-24 | low | `implementer_agent` | sonnet | medium | - | ✅ `16b1dc6` |
| B-11 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify: plan B-11 | low | `orchestrator` | sonnet | medium | - | ✅ `f6f5bb8` |
| M-25 | `workflows/pipeline_workflow.md` | modify: plan M-25 | low | `orchestrator` | sonnet | medium | - | ✅ `18f5736` |
| B-12 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify: plan B-12 | low | `orchestrator` | sonnet | medium | - | ✅ `f2e3188` |
| M-26 | `workflows/pipeline_workflow.md` | modify: plan M-26 | low | `orchestrator` | sonnet | medium | - | ✅ `74adc6e` |
| M-27 | `scripts/check_task_scope.py` | modify: plan M-27 | low | `implementer_agent` | sonnet | medium | - | ✅ `39f243c` |
| B-13 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify: plan B-13 | low | `orchestrator` | sonnet | medium | - | ✅ `40b0f1d` |
| B-14 | `docs/sprints/059-core-pipeline/SPRINT_LOG.md` | modify: plan B-14 | low | `orchestrator` | sonnet | medium | - | ✅ `3fca54b` |
| B-15 | `docs/sprints/059-core-pipeline/task_scope.md` | modify: plan B-15 | low | `orchestrator` | sonnet | medium | - | ✅ `32199c3` |
| M-28 | `agents/rule_validator.md` | modify: plan M-28 | low | `rule_validator` | sonnet | medium | - | ✅ `72b9a98` |
| M-29 | `rules/project_topology.md` | modify: plan M-29 | low | `rule_validator` | sonnet | medium | - | ✅ `445fc2c` |
| M-30 | `rules/django_backend_standard.md` | modify: plan M-30 | low | `rule_validator` | sonnet | medium | - | ✅ `ce5adcb` |
| M-31 | `rules/code_craft.md` | modify: plan M-31 | low | `rule_validator` | sonnet | medium | - | ✅ `3acb3bd` |
| M-32 | `rules/graphify.md` | modify: plan M-32 | low | `rule_validator` | sonnet | medium | - | ✅ `3391032` |

### Wave 3 — In-session token economy

| # | File | Operation | Risk | Assignee | Model | Effort | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-18 | `scripts/session_cost.py` | modify: after A-01, before A-00, fix( `read_turns` counts each `message.id` once (D21); paired test in `tests/test_session_cost.py`, which also adds the missing type hints; `ratio` and cuts do not change over the real transcripts | medium | `implementer_agent` | sonnet | medium | A-01 | ✅ `40b2da1` |
| A-00 | `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | create: D8 study with one table per piece and per mechanism with sources, context growth boot to close, real cost per unit for Sprints 056-058, whether the 15x hard bound stays valid with the baseline on context size (KI-059-9), 2-4 candidate methods (figures supplied by `token_economy_agent`) | medium | `doc_orchestrator` | sonnet | medium | A-18 | ✅ `9b5488c` |
| A-06 | `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | modify: after A-00, add a `Debate` section with options, objections and the human's decision, including the one on the 15x hard bound (KI-059-9) | low | `doc_orchestrator` | sonnet | medium | A-00 | ✅ `6d6e469` |
| A-07 | `docs/decisions/ADR-0018-in-session-token-economy.md` | create: after A-06, the chosen method, confirming or replacing D2; leftovers go to KI-059-n | medium | `doc_orchestrator` | sonnet | medium | A-06 | ✅ `33ac3ad` |
| A-02 | `scripts/session_cost.py` | modify: after A-01 and A-07, feat( flag `--bound` (OK, SOFT, HARD, exit 0, D3) or the form ADR-0018 sets; test in `tests/test_session_cost.py` | medium | `implementer_agent` | sonnet | medium | A-01, A-07 | ✅ `5c5e0a3`, `ad7cd48` |
| A-55 | `scripts/session_probe.py` | modify: after A-02, `HARD_RATIO = 15` is replaced in `probe_cost` by the ADR-0018 absolute bound of 550,000 tokens; paired test | low | `implementer_agent` | sonnet | medium | A-02 | ⏳ |
| A-56 | `scripts/check_task_scope.py` | modify: fix( a `task_scope.md` with no work rows exits non-zero (measured 2026-11-09: an empty file gave `OK`); paired test in `tests/test_check_task_scope.py` | medium | `implementer_agent` | sonnet | medium | - | ⏳ |
| A-03 | `rules/token_economy.md` | modify: after A-07, section 3.1 in-session invoker (the D1 and D19 unit was corrected in the QA Gate 1 round 3 remediation) and the per-unit budget with planned suspend points (D14) | low | `rule_validator` | sonnet | medium | A-07 | ⏳ |
| H-01 | `config/unit_cost_estimates.json` | create: after A-07, estimate table by unit type and risk with the A-00 source and `measured_at` per figure (figures supplied by `token_economy_agent`) | low | `implementer_agent` | sonnet | medium | A-07 | ⏳ |
| H-02 | `scripts/check_task_scope.py` | modify: after G-01 and H-01, add `Est. cost` and `Suspend after` columns; accumulate cost in order and exit 2 when the cumulative projection passes soft (5x) with no earlier `Suspend after: yes` (D14); tests in `tests/test_check_task_scope.py` | medium | `implementer_agent` | sonnet | medium | G-01, H-01 | ⏳ |
| H-03 | `workflows/close_workflow.md` | modify: after H-01 and B-07, advisory step comparing each unit's measured cost (`session_cost.py --json`) with its `Est. cost`; RA-16 invoker of the `config/unit_cost_estimates.json` recalibration | low | `orchestrator` | sonnet | medium | H-01, B-07 | ⏳ |
| A-04 | `workflows/pipeline_workflow.md` | modify: after G-02, A-02 and H-02, Phase 4.3 fills `Est. cost` and `Suspend after`; Phase 6 runs the measurement per unit (RA-16 invoker of A-02), compares it with `Est. cost`, and runs `session_state.py suspend` at each `Suspend after: yes`; Phase 6 step 2 requires each worktree to run `git merge --ff-only ai-sprint/[ID]` and check its base before the first edit (KI-059-16, plan D38) | low | `orchestrator` | sonnet | medium | G-02, A-02, H-02 | ⏳ |

### Wave 4 — Sandbox measurement

| # | File | Operation | Risk | Assignee | Model | Effort | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B-03 | `scripts/py_compile_tree.py` | modify: compile without writing `.pyc` (D5); test in `tests/test_verify_py_compile.py` | medium | `implementer_agent` | sonnet | medium | - | ⏳ |
| B-04 | `skills/mass-standardizer/scripts/generate_manifest.py` | modify: add `--check` (exit 0 on match, exit 2 on drift, `skills/manifest_skills.json` bytes unchanged) (D5); test in `tests/test_mass_standardizer.py` | medium | `skill_architect` | sonnet | medium | - | ⏳ |
| B-05 | `Makefile` | modify: after B-03 and B-04, `verify` uses both no-write modes | low | `implementer_agent` | sonnet | medium | B-03, B-04 | ⏳ |
| C-01 | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` | create: RA-19 re-measurement for the current CLI (untested E16 members, subtrees inferred by containment, `Edit(/.git/modules/.agents/**)`, D-8), including the nucleus with the B-06 sandbox and whether `devops_agent` can run `gh` under the sandbox with no `excludedCommands` entry and no other out-of-sandbox path (`RA-09`, `RA-19`), using read-only `gh` commands and their literal output, plus whether Phase 6 step 4 `git worktree remove` and `git branch -D` work under the sandbox (KI-059-17, plan D38); `devops_agent` measures dispatched with `model: sonnet` (escalated from mechanical for high risk) and hands over literal output | high | `doc_orchestrator` | sonnet | medium | - | ⏳ |
| C-02 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify: after C-01 and A-02, `F-055-N1` closed if C-01 measures its vector with no agent-writable entry point, otherwise open citing the C-01 measurement; `F-116-N1` marked closed citing the A-01 commits (`ef490cd`, `919d4f2`) and `F-116-N2` citing the A-02 commit | low | `doc_orchestrator` | sonnet | medium | C-01, A-02 | ⏳ |

### Wave 5 — Regime

| # | File | Operation | Risk | Assignee | Model | Effort | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `docs/decisions/ADR-0019-sandbox-regime.md` | create: after B-02 and C-01, decide RA-09, the gh row, D-12, the local DB route (KI-057-1) and hooks in the nucleus (D6, D12); requirement (human decision 2026-11-08): `devops_agent` runs `gh` instead of the human if C-01 measures that possible with no out-of-sandbox path, otherwise the ADR records the measurement and `gh` stays with the human | high | `doc_orchestrator` | sonnet | medium | B-02, C-01 | ⏳ |
| D-02 | `agents.md` | modify: after A-12 and D-01, amend RA-09 and section 2 graph_sync (D-10); `wc -c agents.md` at most 20000 after the change, new detail goes to `rules/project_topology.md` (D-03) | high | `rule_validator` | sonnet | medium | A-12, D-01 | ⏳ |
| D-03 | `rules/project_topology.md` | modify: after A-10 and D-01, section 4 gh row (D-3), D-1, D-4, cost of `git -C .agents fetch` (QA2-3) | medium | `rule_validator` | sonnet | medium | A-10, D-01 | ⏳ |
| D-04 | `claude/settings.hooks.json` | modify: after D-01, `sandbox` block local DB route (KI-057-1) only if ADR-0019 approves a measured route, otherwise RECORD | high | `implementer_agent` | sonnet | medium | D-01 | ⏳ |
| E-01b | `claude/settings.hooks.json` | modify: after E-01, D-01 and D-04 (same file as D-04, serial), the SessionEnd command resolves its path in nucleus and host if ADR-0019 approves hooks in the nucleus (D13), otherwise RECORD and manual `suspend` stays documented | medium | `implementer_agent` | sonnet | medium | E-01, D-01, D-04 | ⏳ |

### Wave 6 — Hardening, roles and Sprint 058 residues

| # | File | Operation | Risk | Assignee | Model | Effort | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E-02 | `claude/mcp.json` | modify: remote GitHub MCP server with OAuth, no token in a file | medium | `implementer_agent` | sonnet | medium | - | ⏳ |
| E-03 | `.github/workflows/ci.yml` | modify: pin `actions/checkout`, `actions/setup-python`, `errata-ai/vale-action` by SHA | low | `implementer_agent` | sonnet | medium | - | ⏳ |
| F-01 | `docs/decisions/ADR-0020-owner-writer-dispatch.md` | create: C-7, when the owner writes a trivial artifact without a dispatch (amends ADR-0017) | medium | `doc_orchestrator` | sonnet | medium | - | ⏳ |
| F-02 | `config/artifact_registry.json` | modify: after F-01, if ADR-0020 is approved register the owner-writes exception with the condition the ADR sets and `check_role_artifact.py` exit 0; otherwise RECORD with no change | medium | `implementer_agent` | sonnet | medium | F-01 | ⏳ |
| I-01 | `scripts/check_absolute_paths.py` | modify: fix( KI-058-1, also scan the index and untracked files; new paired test `tests/test_check_absolute_paths.py` | low | `implementer_agent` | sonnet | medium | - | ⏳ |
| I-02 | `scripts/upstream_outbox.py` | modify: fix( KI-058-4, `read_text_file` goes through `read_regular_bytes` so a FIFO exits 2; paired test with a FIFO in `tests/test_upstream_outbox.py` | low | `implementer_agent` | sonnet | medium | - | ⏳ |
| I-03 | `scripts/upstream_outbox.py` | modify: after I-02, fix( KI-058-5 a, `deltas` exits 2 on a missing `--rules` directory; paired test in `tests/test_upstream_outbox.py` | low | `implementer_agent` | sonnet | medium | I-02 | ⏳ |
| I-04 | `scripts/upstream_outbox.py` | modify: after I-03, fix( KI-058-5 b, `export --out` to a missing directory exits 2 with a message; paired test in `tests/test_upstream_outbox.py` | low | `implementer_agent` | sonnet | medium | I-03 | ⏳ |
| I-05 | `scripts/upstream_outbox.py` | modify: after I-04, fix( KI-058-5 c, `PIN_PATTERN` accepts ASCII digits only; paired test with non-ASCII digits in `tests/test_upstream_outbox.py` | low | `implementer_agent` | sonnet | medium | I-04 | ⏳ |
| I-06 | `hooks/on_commit.py` | modify: fix( KI-058-5 d, an uppercase `FIX:` subject is treated as `fix(`; paired test in `tests/test_on_commit.py` | low | `implementer_agent` | sonnet | medium | - | ⏳ |
| I-07 | `scripts/check_fix_reproduces.py` | modify: fix( KI-058-5 d, same uppercase `FIX:` case in the reproduction check; paired test in `tests/test_check_fix_reproduces.py` | low | `implementer_agent` | sonnet | medium | - | ⏳ |
| K-01 | `config/invocation_exceptions.json` | modify: plan K-01 (KI-059-6) | low | `implementer_agent` | sonnet | medium | - | ⏳ |
| K-02 | `scripts/detect_drift.py` | modify: plan K-02 (KI-059-6) | low | `implementer_agent` | sonnet | medium | - | ⏳ |
| K-03 | `tests/test_detect_drift.py` | modify: plan K-03 (KI-059-6) | low | `implementer_agent` | sonnet | medium | - | ⏳ |
| K-04 | `agents.md` | modify: plan K-04 (KI-059-6) | low | `rule_validator` | sonnet | medium | - | ⏳ |
| L-01 | `scripts/graph_update.py` | create: D39: run the graphify AST rebuild sequentially, with optional `--force`; non-zero exit if the rebuild fails or graphify no longer exposes `_PARALLEL_THRESHOLD` or `_rebuild_code`; paired test `tests/test_graph_update.py` | medium | `implementer_agent` | sonnet | medium | - | ✅ `7ff0c66` |
| L-02 | `Makefile` | modify: D39: `graphify-update` invokes `scripts/graph_update.py` and `graphify-rebuild` the same with `--force`; companion: `tests/test_makefile_graphify.py` keeps requiring `-I` | low | `implementer_agent` | sonnet | medium | L-01 | ✅ `cd57745` |
| L-03 | `rules/graphify.md` | modify: D39: the agent form of `graphify update .` becomes `scripts/graph_update.py`; the `graph unavailable` notice remains only for a non-zero exit of that script | low | `rule_validator` | sonnet | medium | L-01 | ✅ `62b7729` |
| L-04 | `rules/project_topology.md` | modify: D39: section 4 adds the `SC_SEM_NSEMS_MAX` failure row with its sanctioned form | low | `rule_validator` | sonnet | medium | L-01 | ✅ `d570ec7` |
| L-05 | `agents.md` | modify: D39: `graph_sync` names `scripts/graph_update.py`; `wc -c agents.md` <= 20000 | low | `rule_validator` | sonnet | medium | L-03 | ✅ `32bcd7f` |
| I-08 | `scripts/check_task_scope.py` | modify: fix( D36: `--current-sprint` exits 2 when the anchor names a sprint whose directory is missing; `current_sprint_dir` separates that case from an absent anchor; paired test in `tests/test_check_task_scope.py` | low | `implementer_agent` | sonnet | medium | - | replaced by M-02 (D37) |
| I-09 | `scripts/check_gate_log.py` | modify: after I-08: fix( D36: exit 2 on a missing `--sprint-dir` and on the I-08 case under `--current-sprint`; paired test in `tests/test_check_gate_log.py` | low | `implementer_agent` | sonnet | medium | - | replaced by M-03 (D37) |
| I-10 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify: after I-08: fix( D36: the I-08 case under `--current-sprint` exits 2; paired test beside the `audit_plan.py` tests | low | `skill_architect` | sonnet | medium | - | replaced by M-04 (D37) |

### Close

| # | File | Operation | Risk | Assignee | Model | Effort | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Z-01 | `CHANGELOG.md` | modify: add the sprint entry under `[Unreleased]`, citing `host:F-116-N1` and `host:F-116-N2` | low | `doc_orchestrator` | sonnet | medium | - | ⏳ |
| Z-02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify: close or re-route KI-056-1, KI-056-6, KI-057-1, KI-057-2, KI-058-1, KI-058-3, KI-058-4, KI-058-5; keep KI-058-2 and the conditional Out of scope items with their unblock condition; add new KI-059-n, including one for proposal E points 3-5 (P11); route or close with evidence each KI-059-n row of the `SPRINT_LOG.md` table that stays open; that table is the list (plan D36) | low | `doc_orchestrator` | sonnet | medium | - | ⏳ |

## Jurisdiction check (serial or concurrent)

`python3 scripts/check_task_scope.py --sprint-dir docs/sprints/059-core-pipeline --batches` puts no two units with the same `File` cell in one batch.

## Rule audit findings

Severity per `rules/qa_and_testing.md` section 4 (S0-S3). Class per the same file (`instructing` or `testifying`).

| ID | Severity | Class | Evidence | Concrete plan change |
| :--- | :--- | :--- | :--- | :--- |
| F-1 | S2 | instructing | `IMPLEMENTATION_PLAN.md:149` makes D-04 modify `claude/settings.json`, and `:44` cites `claude/settings.json:45`. `claude/` holds only `mcp.json` and `settings.hooks.json` (Glob). `claude/settings.hooks.json:45` holds `autoAllowBashIfSandboxed` and `:124-129` holds the `SessionEnd` command that E-01b (`IMPLEMENTATION_PLAN.md:150`) edits. D-04 and E-01b are therefore one structural subject, both after D-01 only, both `parallel` in `agent_assignment.md:86-87`. `jurisdictional_lock` and `no_interference` (`agents.md §2`) forbid concurrent claim; D11 batching would place them in one batch. | Change D-04 target to `claude/settings.hooks.json`; add `after E-01b` to D-04 (or the reverse) and set both to `sequential` in `agent_assignment.md`; correct the `:44` citation. |
| F-2 | S2 | instructing | D11 (`IMPLEMENTATION_PLAN.md:83`) dispatches each unit with `isolation: "worktree"` and the orchestrator "integra los commits". `scripts/branch_sovereignty.py:141-142` audits every local branch except the base and the checked-out one, and `:238-241` calls a branch integrated only when `git cherry <base> <branch>` shows no `+` against `main`; sprint commits are never on `main` before deployment, so any leftover worktree branch is reported unintegrated and the close seal exits 2 (`:293-296`). `hooks/on_commit.py:1011-1014` also returns `None` for a branch that is not `ai-sprint/N`, so commits made on a worktree branch skip the `task_scope.md` guard. Abort criterion 6 (`:288-289`) covers only a git conflict. | Add to G-02 Operation: each worktree branch is deleted after its commits are integrated onto `ai-sprint/059`, and `branch_sovereignty.py audit` is run before close. Add the leftover-branch case to abort criterion 6. |
| F-3 | S2 | instructing | `RA-16` (`agents.md §7`) requires a declared, verifiable invoker. The Mechanisms table (`IMPLEMENTATION_PLAN.md:192`) gives `scripts/prompt_count.py` the invoker `PROMPT_MEASUREMENT.md` (a frozen sprint record) plus an advisory in `close_workflow.md` "decidir en B-01", and `:190` leaves the recalibration in `close_workflow.md` "decidir en H-01". Work has no unit that modifies `workflows/close_workflow.md` or `config/invocation_exceptions.json`. | Decide now: add a unit modifying `workflows/close_workflow.md` (advisory step naming `prompt_count.py`, and the `unit_cost_estimates.json` recalibration), or add a unit for a typed exception in `config/invocation_exceptions.json`. B-01 declares `invoked_by:` accordingly. |
| F-4 | S2 | instructing | A-05 (`IMPLEMENTATION_PLAN.md:100`) is Wave 1 and must "marcar F-116-N1/N2 al aterrizar", but F-116-N1 lands with A-01 (`:106`, Wave 1) and F-116-N2 lands with A-02 and A-04 (`:126`, `:130`, Wave 3). The marking cannot happen in Wave 1 and no later unit does it; C-02 (`:140`) touches the same file for `F-055-N1` only, and Z-02 (`:173`) does not touch it. | Limit A-05 to the triage verdicts; add the `F-116-N1`/`F-116-N2` landed marking to C-02 (Wave 4, after A-04). |
| F-5 | S2 | instructing | E-01 (`IMPLEMENTATION_PLAN.md:117`) bundles three subjects in one `modify` of `scripts/session_state.py`: the KI-057-2 fix, the sealed-sprint lock release (a second defect with no paired test named; only `tests/test_session_end_hook.py` is named), and a write to `SPRINT_LOG.md`. It also depends on "los puntos 3-5 de la propuesta E", an artifact that `Grep` finds only in the plan itself (`:51`, `:117`). `agents.md §1 unambiguous_action` forbids an undefined referent and a step whose decision is hidden ("implementar como unidad nueva o descartar con motivo"). | Split E-01 into one unit per defect, each with its named paired test (`fix(` unit, `rules/qa_and_testing.md`); move the `SPRINT_LOG.md` entry to the orchestrator's log duty; replace "propuesta E" with the file and line where points 3-5 are written, or list them. |
| F-6 | S2 | instructing | D-02 (`IMPLEMENTATION_PLAN.md:147`) re-edits `agents.md` in Wave 5 but its Operation carries no byte cap; the cap exists only in A-12 (`:104`) and in the "Hecho cuando" line (`:59`), and `make verify` does not measure `agents.md` size (no Makefile step references it). The 20,000-byte result can regress silently after A-12. | Add "at most 20,000 bytes (`wc -c agents.md`)" to D-02, and add a size assertion to a test or to `make verify` as the deterministic check. |
| F-7 | S3 | testifying | A-12 target is constrained by content that must stay in `agents.md`: `tests/test_cursor_phase1.py:48-51` asserts `RA-18` and `CURSOR_PHASE1_NO_PLAN_MODE` in `agents.md`; `tests/test_gate_row_wording.py:108-114` requires an `EMITTED` line (RECORD with class and severity) in `agents.md`; `agents.md §0` Command paths row says it is kept there because the file is always loaded. None conflicts with the 20,000-byte target, but the plan names none of them. | Add the three retention constraints to A-12 Operation so the trim does not rediscover them through `make verify`. |
| F-8 | S2 | instructing | The `agents.md §4 feedback_upstream` row declares itself the canonical statement and requires a grep of `§3 jurisdiction` and `workflows/extract_workflow.md` on every patch (`RA-14`). A-11 (`IMPLEMENTATION_PLAN.md:103`) moves its transport, channels, triage and closure to `docs/guides/SELF_IMPROVEMENT_GUIDE.md`, and the term is cited in 16 files (Grep count: `workflows/close_workflow.md`, `workflows/pipeline_workflow.md`, `workflows/extract_workflow.md`, `config/upstream_intake.json`, `scripts/upstream_outbox.py` among them). No Work unit updates those citations. | Add the `RA-14` grep for `feedback_upstream` as a done-criterion of A-12, and either name the citing files as units or state that the row keeps the pointer text they depend on. |
| F-9 | S2 | instructing | B-06 (`IMPLEMENTATION_PLAN.md:116`, Wave 2) enables `autoAllowBashIfSandboxed` in the nucleus (`claude/settings.hooks.json:45` shows the block) before C-01 (`:139`, Wave 4) re-measures `RA-19` including that nucleus sandbox. D12 (`:84`) admits the nucleus has no write-deny on `scripts/` and `hooks/`. Abort criterion 1 (`:276-278`) stops only wave 5 changes and does not revert B-06; criterion 5 (`:286-287`) reverts B-06 only on a `make verify` or Phase 6 failure. `RA-19` (`agents.md §7`) bars asserting a boundary without a measured enumeration. | Add to abort criterion 1: if C-01 finds an agent-writable unsandboxed entry point, B-06 is reverted. Keep the B-06 Operation free of any "boundary" wording. D-04 and E-01b (conditional on ADR-0019) need no change for `RA-19`. |
| F-10 | S2 | instructing | Tests are not named by file in G-01 (`IMPLEMENTATION_PLAN.md:112`), H-02 (`:129`), B-03 (`:136`), B-06 (`:116`) and I-01..I-07 (`:160-166`: "paired test en `tests/`"). `agents.md §1 unambiguous_action` requires the target by name, and `no_interference` cannot be applied to G-01 and H-02, which probably write the same test file. | Name each test file in the Operation (for example the existing test of `check_task_scope.py` for G-01 and H-02, `tests/test_upstream_outbox.py` for I-02..I-05). |
| F-11 | S2 | instructing | F-02 (`IMPLEMENTATION_PLAN.md:159`) says "modify, tras F-01, solo si se aprueba": no operation is stated and, unlike D-04 and E-01b (`:149-150`), no `RECORD` branch. C-02 (`:140`) says "estado de F-055-N1": no operation or done-criterion. `unambiguous_action` requires operation, target and done-criterion. | State F-02's change (which registry entry) and add "otherwise RECORD"; rewrite C-02 as the exact status value written. |
| F-12 | S2 | instructing | B-04 (`IMPLEMENTATION_PLAN.md:137`) adds `--check` to `skills/mass-standardizer/scripts/generate_manifest.py` with no test, and the Tests table (`:214-223`) has no row for it, though B-05 relies on it inside `make verify`. `rules/qa_and_testing.md` section 4 treats an edge case without a test as S2. | Add a named test to B-04 and a Tests row (manifest unchanged and exit 0 on match, exit 2 on drift, file bytes untouched). |
| F-13 | S3 | testifying | Z-01 (`IMPLEMENTATION_PLAN.md:172`) does not say the entry cites `host:F-116-N1` and `host:F-116-N2`, which `agents.md §4 feedback_upstream` (Closure) requires for a nucleus `CHANGELOG.md` entry that ships a finding. | Add the `host:<id>` citations to Z-01 Operation. |
| F-14 | S3 | testifying | C-01 is `high` risk (`IMPLEMENTATION_PLAN.md:139`) and its measurements run on `devops_agent`, tier `mechanical` (`config/model_tiers.json:85` basis: "a wrong answer fails at the next command"), but an incomplete `RA-19` enumeration does not fail at the next command. | Record in `SPRINT_LOG.md` that C-01 measurements are re-checked at the Phase 7 gate, or run the measuring step on an `author` profile. |

## Resolution of the findings

Applied to `IMPLEMENTATION_PLAN.md` (and mirrored in the Work tables above and in `agent_assignment.md`) before Phase 5. Plan Work units: 44 → 47 (B-07, E-01c, H-03 added). Phase 6 Wave 1 added A-13 (plan D15): 47 → 48, A-14 (plan D17): 48 → 49, A-15, A-16, A-17 (plan D18): 49 → 52, and A-18 (plan D21): 52 → 53. After QA Gate 1 round 5, A-19 to A-24 (plan D22) and A-25 (plan D23): 53 → 60. After QA Gate 1 round 6, A-26 to A-37 (plan D24 to D26): 60 → 72, and A-38, A-39 (plan D28): 72 → 74. After QA Gate 1 round 7, A-40 to A-45 (plan D29): 74 → 80. After QA Gate 1 round 8, A-46 to A-52 (plan D33, D34): 80 → 87. After QA Gate 1 round 9, A-53, A-54 (plan D35): 87 → 89. After QA Gate 1 round 11, I-08 to I-10 (plan D36): 89 → 92, an estimate fixed at the opening of Wave 6. After QA Gate 1 round 12, M-01 to M-11 (plan D37): 92 → 103; I-08 to I-10 stay counted as replaced. After QA Gate 1 round 13, M-12: 103 → 104.

| ID | Resolution |
| :--- | :--- |
| F-1 | D-04 targets `claude/settings.hooks.json`; E-01b runs after D-04; both `sequential`; P4 citation corrected to `claude/settings.hooks.json:45`. |
| F-2 | G-02 Operation: each worktree and its branch are removed after integration, and `check_task_scope.py` re-runs on `ai-sprint/[ID]` before the next batch. |
| F-3 | New units B-07 (`close_workflow.md` advisory running `prompt_count.py`) and H-03 (`close_workflow.md` advisory recalibration); Mechanisms table names both invokers. |
| F-4 | A-05 limited to triage verdicts; C-02 marks `F-116-N1` (A-01) and `F-116-N2` (A-02) closed. |
| F-5 | E-01 split into E-01 (`KI-057-2`, `tests/test_session_end_hook.py`) and E-01c (sealed-sprint lock release, `tests/test_session_state.py`). The "proposal E points 3-5" decision is removed from E-01; its source is not in the repository and the human decides its destination at Phase 5 (decided at Phase 5: Z-02 routes it, plan P11). |
| F-6 | D-02 carries `wc -c agents.md` ≤ 20000; the plan Verification row `wc -c agents.md` measures it at close. |
| F-7 | A-12 Operation names the three pinned strings and the `grep -n "agents.md" tests/*.py` pre-check. |
| F-8 | A-12 Operation carries the `RA-14` grep for every moved term, with citations updated in the same commit. |
| F-9 | Abort criterion 1 reverts B-06 when the entry point C-01 finds is opened by its `sandbox` block. |
| F-10 | Each test file named: G-01/H-02 `tests/test_check_task_scope.py`, B-03 `tests/test_verify_py_compile.py`, B-06 `tests/test_install_nucleus_sandbox.py`, I-01 `tests/test_check_absolute_paths.py`, I-02..I-05 `tests/test_upstream_outbox.py`, I-06 `tests/test_on_commit.py`, I-07 `tests/test_check_fix_reproduces.py`. |
| F-11 | F-02 states the registry change and a `RECORD` branch; C-02 states each status value. |
| F-12 | B-04 names `tests/test_mass_standardizer.py`; a Tests row was added with its observed base. |
| F-13 | Z-01 cites `host:F-116-N1` and `host:F-116-N2`. |
| F-14 | C-01 measurements dispatched with `model: sonnet` (escalated from `mechanical`). |
