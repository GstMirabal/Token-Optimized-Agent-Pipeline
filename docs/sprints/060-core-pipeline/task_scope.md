# Task Scope — Sprint 060 (core-pipeline)

Source: `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`, `## Design`, `## Mechanisms`, `## Abort criterion`), committed at `466044e`.
Staffing authority: `agent_assignment.md` (its Assignee column overrides the plan's `Assignee (proposed)`; the six overwrites A-10, D-04, H-01, J-01, B-02 and A-12 are listed in its "Disagreements with the plan" and are used verbatim here). `skill_assignment.md` was read: it assigns no skill that adds a Work row.
Phase 4.3 of `workflows/pipeline_workflow.md`. Enforced by `scripts/check_task_scope.py`.
Mode: `claude-code`, `delegation_mode: native`. Sprint id 60 >= `MODEL_FROM_SPRINT` (28) and >= `COST_FROM_SPRINT` (60), so Model, Effort, `Est. cost` and `Suspend after` are all required.

## Tier transcription

Model and Effort are transcribed from each assignee's `agents/<role>.md` frontmatter (`model:`, `tier:`) and the `claude_code` column of `config/model_tiers.json` (`tiers.author.claude_code` = `sonnet` / `medium`). No tier is invented and no dated model ID is written. `session_tool` is `claude-code`, so `make cursor-tiers` does not apply.

| Assignee | model | tier | effort |
| :--- | :--- | :--- | :--- |
| `doc_orchestrator` | sonnet | author | medium |
| `implementer_agent` | sonnet | author | medium |
| `rule_validator` | sonnet | author | medium |
| `orchestrator` | sonnet | author | medium |
| `agent_orchestrator` | sonnet | author | medium |

Declared escalations: none. No Work row is assigned to a `mechanical` profile (`agent_assignment.md` moved A-10, D-04 and H-01 from `devops_agent` to `implementer_agent`), so the mechanical-at-high-risk check does not apply. The high-risk rows (A-03, A-04, A-10, K-01, F-01, H-01) stay on the `author` tier: the adversarial check on them is the Phase 7 gate (`tier: gate`). No `token_economy_agent` verdict on tiers was produced for this sprint, so none is transcribed.

## Cost basis

`baseline_context` = 60612 (`config/unit_cost_estimates.json`); the segment ceiling is `baseline_context + sum <= 5 * baseline_context`, i.e. an accumulated `Est. cost` of at most 242448 between two `Suspend after: yes`. Group chosen per row: exact `operation/filetype/risk` group when it exists, else `operation/filetype`, else the `risk` group (config, YAML, `.txt`, `allowed_signers`). Rename rows (`git mv` plus reference edits) use `modify/doc/low`. `rules/*.md` and `agents.md` use `modify/rule`; `workflows/*.md`, `agents/*.md`, ADRs, guides and reports use `doc`.

| Segment closes at | Accumulated `Est. cost` | Why there |
| :--- | :--- | :--- |
| A-02 | 230708 | A-03 would reach 245817 |
| A-09 | 180488 | The human installs the broker and registers it (`A-09` guide) before A-10 can measure; A-10 would reach 295842 |
| B-02 | 147284 | End of the model-detector wave; K-01 begins a fresh segment |
| L-06 | 233153 | End of the `graphifyy` and advisory waves; C-01 and D-01 would reach 236906 and 270480 |
| G-02 | 235060 | Waves C, D, E, F, G; H-01 would reach 350414 |
| I-09 | 148403 | Waves H and I; J-01 would reach 263757 |
| J-02 | 230708 | Z-01 would reach 346062 |
| Z-02 | 230708 | Z-03 would reach 346062 |
| Z-04 | 230708 | Z-05 and Z-06 (5596) form the last segment |

The bound is on estimates (soft). A-10 and H-01 are the largest uncertainty (`create/doc` `max_fresh` 152885); if A-10 measures above 242448 alone the suspension must come earlier.

## Work

Status values: ⏳ pending, ✅ committed (short SHA). Risk is transcribed from the plan. `Depends on` records order only where one exists in the plan or where this audit found one (see "Same-file ordering"). Rows Z-01 and Z-03 already exist on disk (`4cb4570`, `024598e`) and Z-02 is this file; they are `pending` here because the Phase 4.3 contract sets `pending` on every unit and the closing commit stamps them.

### Wave A — GitHub App broker

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/decisions/ADR-0025-github-app-broker.md` | create: D1-D6; replaces `ADR-0019` D2 and D6 | medium | `doc_orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| A-02 | `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` | create: from `BLUEPRINT_TEMPLATE.md` | low | `doc_orchestrator` | sonnet | medium | 115354 | yes | A-01 | ⏳ pending |
| A-03 | `scripts/github_broker.py` | create: stdio MCP server with the D4 operations; companion `tests/test_github_broker.py` in the same commit | high | `implementer_agent` | sonnet | medium | 15109 | | A-01 | ⏳ pending |
| A-04 | `scripts/install_broker.py` | create: install from a signed tag or a named `main` commit (D5); companion `tests/test_install_broker.py` | high | `implementer_agent` | sonnet | medium | 15109 | | A-03 | ⏳ pending |
| A-05 | `claude/settings.hooks.json` | modify: `denyRead` and `permissions.deny` of D3 | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ⏳ pending |
| A-06 | `config/allowed_signers` | create: public signing key supplied by the human | low | `implementer_agent` | sonnet | medium | 4613 | | - | ⏳ pending |
| A-07 | `scripts/sync_agents_pin.py` | modify: `git verify-tag` (D6); companion `tests/test_sync_agents_pin.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | A-06 | ⏳ pending |
| A-08 | `scripts/install.py` | modify: `git verify-tag` (D6); companion `tests/test_install.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | A-06 | ⏳ pending |
| A-09 | `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` | create: human steps (create the App, D4 permissions, install on the nucleus only, keys, `install_broker.py`, `claude mcp add --scope user`) | low | `doc_orchestrator` | sonnet | medium | 115354 | yes | A-03, A-04 | ⏳ pending |
| A-10 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | create: M1 keys unreadable, M2 installed broker not editable, M3 no token in the sandbox, M4 live D4 rejections, M5 end to end at the 060 deployment | high | `implementer_agent` | sonnet | medium | 115354 | | A-03, A-04, A-05, A-09 | ⏳ pending |
| A-11 | `workflows/deployment_workflow.md` | modify: push, PR, merge, tag and Release through the broker | medium | `doc_orchestrator` | sonnet | medium | 3753 | | A-03 | ⏳ pending |
| A-12 | `agents/devops_agent.md` | modify: uses the broker tools; stops preparing `gh` for the human | low | `doc_orchestrator` | sonnet | medium | 2798 | | A-11 | ⏳ pending |
| A-13 | `rules/project_topology.md` | modify: `gh`/credential row now names the broker (`KI-059-21`, `-22`, `-24`) | medium | `doc_orchestrator` | sonnet | medium | 7867 | | A-11 | ⏳ pending |
| A-14 | `workflows/repository_hardening_workflow.md` | modify: measured state of `ADR-0019` D7 and the App installation | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |

### Wave B — Model detector

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B-01 | `scripts/detect_new_models.py` | modify: fail closed and new catalogue source (D8); companion `tests/test_detect_new_models.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ⏳ pending |
| B-02 | `config/model_tiers.json` | modify: `catalog_snapshot`, `context_limits.haiku`, `excluded` (`claude-fable-5-2`), `verified_at` | low | `implementer_agent` | sonnet | medium | 4613 | yes | B-01 | ⏳ pending |

### Wave K and L — `graphifyy` and dependency advisories

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| K-01 | `requirements-core.txt` | modify: `graphifyy` 0.8.30 to the newest version >= 0.9.70 published >= 24 h ago, closure and hashes regenerated; review `scripts/graph_update.py` workaround in the same commit (D12) | high | `implementer_agent` | sonnet | medium | 54797 | | - | ⏳ pending |
| L-01 | `scripts/check_dependency_advisories.py` | create: OSV `/v1/querybatch` (stdlib) per `requirements*.txt` pin, exit `2` on advisory or no network (D13); companion `tests/test_check_dependency_advisories.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | K-01 | ⏳ pending |
| L-02 | `.github/workflows/ci.yml` | modify: L-01 on every PR and a daily cron on `main` | medium | `implementer_agent` | sonnet | medium | 10101 | | L-01 | ⏳ pending |
| L-03 | `scripts/session_start.py` | modify: boot shows L-01 as a warning in nucleus and host (D13); companion `tests/test_session_start.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | L-01 | ⏳ pending |
| L-04 | `claude/settings.hooks.json` | modify: `api.osv.dev` in `sandbox.network.allowedDomains` (D13) | low | `implementer_agent` | sonnet | medium | 4613 | | A-05 | ⏳ pending |
| L-05 | `docs/decisions/ADR-0026-dependency-advisory-check.md` | create: D13 and the egress widening, amends `ADR-0024` | low | `doc_orchestrator` | sonnet | medium | 115354 | | L-01, L-04 | ⏳ pending |
| L-06 | `.github/dependabot.yml` | create: only if the alert #28 message shows the missing `pip` config blocked the PR; otherwise the row closes with the transcribed message (D13) | low | `implementer_agent` | sonnet | medium | 4613 | yes | - | ⏳ pending |

### Wave C — Ledger seal

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C-01 | `workflows/deployment_workflow.md` | modify: `ledger_seal` on `ai-sprint/[ID]` (D7, `KI-059-35`) | medium | `doc_orchestrator` | sonnet | medium | 3753 | | A-11 | ⏳ pending |

### Wave D — Host-term scanner

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `scripts/check_host_terms.py` | create: hash scanner (D9); companion `tests/test_check_host_terms.py` | medium | `implementer_agent` | sonnet | medium | 33574 | | - | ⏳ pending |
| D-02 | `config/host_term_hashes.json` | create: hashes the human generates | low | `implementer_agent` | sonnet | medium | 4613 | | - | ⏳ pending |
| D-03 | `tests/test_profile_references.py` | modify: use `check_host_terms.py` (`KI-059-14`) | low | `implementer_agent` | sonnet | medium | 4717 | | D-01 | ⏳ pending |
| D-04 | `docs/sprints/060-core-pipeline/HISTORY_REVIEW_REPORT.md` | create: scan of `origin/main`; rewriting history stays a human decision (`KI-059-12`) | medium | `implementer_agent` | sonnet | medium | 115354 | | D-01, D-02 | ⏳ pending |

### Wave E — Gate log

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E-01 | `scripts/check_gate_log.py` | modify: one Gate findings row per S0-S2 finding; companion `tests/test_check_gate_log.py` | medium | `implementer_agent` | sonnet | medium | 10101 | | - | ⏳ pending |

### Wave F — Normative text

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-01 | `agents.md` | modify: trim under 20000 bytes; `mass-standardizer` wording (`KI-059-32`); `RA-09` and `§6 devops_agent` name the broker | high | `rule_validator` | sonnet | medium | 49477 | | A-12 | ⏳ pending |
| F-02 | `rules/skills_and_integrations.md` | modify: `mass-standardizer` wording (`KI-059-32`) | low | `rule_validator` | sonnet | medium | 4037 | | - | ⏳ pending |

### Wave G — Measurement scripts

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G-01 | `scripts/unit_cost.py` | modify: only backticked SHAs that resolve as a commit (`KI-059-34`); companion `tests/test_unit_cost.py` | low | `implementer_agent` | sonnet | medium | 4717 | | - | ⏳ pending |
| G-02 | `scripts/prompt_count.py` | modify: `EPERM` on the transcript prints the human command and a documented exit `2` (`KI-059-34`); companion `tests/test_prompt_count.py` | low | `implementer_agent` | sonnet | medium | 4717 | yes | - | ⏳ pending |

### Wave H — Sandbox re-measurement

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| H-01 | `docs/sprints/060-core-pipeline/SANDBOX_REMEASUREMENT.md` | create: 055 and 056 matrices on one fixed CLI (`KI-059-31`) | high | `implementer_agent` | sonnet | medium | 115354 | | - | ⏳ pending |
| H-02 | `rules/project_topology.md` | modify: `Measuring CLI` row and the rows H-01 changes | medium | `doc_orchestrator` | sonnet | medium | 7867 | | A-13, H-01 | ⏳ pending |

### Wave I — `RA-06` renames (D10, audit 059 R1-R9)

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| I-01 | `docs/architecture/global_topology.md` | modify: rename to `GLOBAL_TOPOLOGY_MAP.md` (R1) with `git mv`; grep of the old path returns 0 outside sealed records | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-02 | `docs/architecture/topology_map.md` | modify: rename to `TOPOLOGY_MAP.md` (R2) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-03 | `docs/contracts/core/doc_orchestrator_contract.md` | modify: rename to `DOC_ORCHESTRATOR_CONTRACT.md` (R3) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-04 | `docs/contracts/core/topology_mapper_contract.md` | modify: rename to `TOPOLOGY_MAPPER_CONTRACT.md` (R4) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-05 | `docs/contracts/core/topology_scaffolder_contract.md` | modify: rename to `TOPOLOGY_SCAFFOLDER_CONTRACT.md` (R5) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-06 | `docs/audits/TOKEN_ECONOMY_AUDIT-documentation-standard.md` | modify: rename to `TOKEN_ECONOMY_DOCUMENTATION_STANDARD_AUDIT.md` (R6) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-07 | `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md` | modify: rename to `SKILLOPT_TRANSITIVE_CLOSURE_AUDIT.md` (R7) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-08 | `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` | modify: rename to `THIRD_PARTY_PROVENANCE_REGISTER.md` (R8) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| I-09 | `docs/plans/027-autonomy-posture-DRAFT.md` | modify: rename to `AUTONOMY_POSTURE_PLAN.md` (R9) with `git mv`; same grep | low | `doc_orchestrator` | sonnet | medium | 2798 | yes | - | ⏳ pending |

### Wave J — Audits

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J-01 | `docs/audits/PROMPT_AUDIT_REPORT-060.md` | create: measurement and findings (D11) | medium | `implementer_agent` | sonnet | medium | 115354 | | - | ⏳ pending |
| J-02 | `docs/audits/PROSE_MOTIVES_AUDIT_REPORT-060.md` | create: prose motives in normative documents (D11) | medium | `rule_validator` | sonnet | medium | 115354 | yes | - | ⏳ pending |

### Wave Z — Pipeline and closeout artifacts

| # | File | Operation | Risk | Assignee | Model | Effort | Est. cost | Suspend after | Depends on | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Z-01 | `docs/sprints/060-core-pipeline/SPRINT_LOG.md` | create: Phase 3 | low | `orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| Z-02 | `docs/sprints/060-core-pipeline/task_scope.md` | create: Phase 4.3 | low | `rule_validator` | sonnet | medium | 115354 | yes | - | ⏳ pending |
| Z-03 | `docs/sprints/060-core-pipeline/agent_assignment.md` | create: Phase 4.1 | low | `agent_orchestrator` | sonnet | medium | 115354 | | - | ⏳ pending |
| Z-04 | `docs/walkthroughs/core/pipeline/060_WALKTHROUGH.md` | create: closeout `RA-05` (see finding RV-12) | low | `doc_orchestrator` | sonnet | medium | 115354 | yes | - | ⏳ pending |
| Z-05 | `CHANGELOG.md` | modify: `[Unreleased]` | low | `doc_orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |
| Z-06 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify: KI routed to closed | low | `orchestrator` | sonnet | medium | 2798 | | - | ⏳ pending |

## Same-file ordering (`jurisdictional_lock`, `no_interference`)

Fifty-two rows, fifty-two distinct `File` cells except three pairs. No two rows are `in progress` at once: the plan executes sequentially (`agent_assignment.md` Mode column), and each pair is ordered by `Depends on`.

| File | First | Second | Order recorded |
| :--- | :--- | :--- | :--- |
| `workflows/deployment_workflow.md` | A-11 (broker steps) | C-01 (`ledger_seal` on the sprint branch) | C-01 `Depends on` A-11; C-01 rewrites the merge/seal sequence A-11 just wrote |
| `rules/project_topology.md` | A-13 (`gh`/credential row) | H-02 (`Measuring CLI` row) | H-02 `Depends on` A-13 and H-01; disjoint rows, so only the order matters for the merge |
| `claude/settings.hooks.json` | A-05 (`denyRead`, `permissions.deny`) | L-04 (`allowedDomains`) | L-04 `Depends on` A-05; both touch the sandbox block, A-05 first so L-04 edits the merged shape |

Companion files (not structural subjects, but two rows reach them): `tests/test_template_sandbox.py`, `tests/test_install_nucleus_sandbox.py` and `tests/test_merge_json.py` assert the `claude/settings.hooks.json` template, so A-05 and L-04 both touch them in sequence (same order). `tests/test_session_start.py` is reached by A-07 (new exit `2` from `verify-tag`) and L-03.

## Dependent files (graphify and reference graph)

`graphify-out/graph.json` was searched with `Grep` (1555 nodes carry a `source_file` under the seven touched scripts); `python3 -m graphify query` could not be run (this session has no shell). Importers and mentions below come from `Grep` over `scripts/ hooks/ tests/ workflows/ rules/ Makefile`, so they are measured but not a graph traversal.

| Unit | Dependent files the unit will touch or must re-check |
| :--- | :--- |
| A-05, L-04 | `tests/test_template_sandbox.py`, `tests/test_install_nucleus_sandbox.py`, `tests/test_merge_json.py` (assert the template); consumers `scripts/install.py`, `scripts/merge_json.py`, `scripts/with_env.py`, `scripts/session_end_hook.py`, `hooks/on_init.py`, `hooks/on_commit.py`, `hooks/state_mirror.py` |
| A-07 | `scripts/session_start.py` (calls it at lines 19, 453, 681; must handle the new exit `2`), `scripts/_root.py:58`, `scripts/_mode.py:37`, `workflows/start_workflow.md:32`, `workflows/close_workflow.md:35` |
| A-08 | `scripts/install_lock.py`, `scripts/merge_json.py`, `scripts/_mode.py`; `rules/project_topology.md` (`ADR-0019` x6) and `workflows/repository_hardening_workflow.md` cite `ADR-0019` D2/D6, which A-01 replaces |
| A-11, C-01 | `scripts/session_state.py`, `scripts/check_role_artifact.py`, `tests/test_session_state.py`, `tests/test_session_protocol.py` (all name `ledger_seal`/`require-released`); `workflows/close_workflow.md` |
| B-01, B-02 | `scripts/_root.py:55`, `scripts/_md_table.py:14`, `Makefile:84` (invoker), `tests/test_detect_new_models.py`; `config/model_tiers.json` is read by `scripts/audit_cursor_models.py` and the profile/tier check in `make verify` |
| K-01 | `scripts/graph_update.py`, `rules/graphify.md` (lines 18 and 32 state "graphifyy 0.8.30"), `rules/project_topology.md`, `tests/test_mcp_template.py` |
| L-01 .. L-03 | `scripts/session_start.py` (L-03 subject), `.github/workflows/ci.yml` (L-02 subject), `config/invocation_exceptions.json` only if the invoker is not a file |
| D-01 | `Makefile` `verify` (named invoker in `## Mechanisms`), `tests/test_profile_references.py` (D-03 subject) |
| E-01 | `scripts/check_plan_closure.py`, `scripts/check_role_artifact.py:360`, `scripts/model_ledger.py`, `scripts/audit_cursor_era.py`, `scripts/_current_sprint.py`, `scripts/_md_table.py`, `rules/qa_and_testing.md` (lines 71 and 99 describe the row format), `tests/test_check_gate_log.py`, `tests/test_gate_row_wording.py` |
| G-01 | `workflows/close_workflow.md:29`, `workflows/pipeline_workflow.md:22,24`, `scripts/check_task_scope.py` (cost columns), `tests/test_unit_cost.py` |
| G-02 | `workflows/close_workflow.md:25`, `tests/test_prompt_count.py` |
| F-01 | `tests/test_cursor_phase1.py` (pins `RA-18`), `tests/test_gate_row_wording.py` (the `EMITTED` line), the `Command paths` row; `config/rule_triggers.json` mirrors the `Rule Contexts` table |
| I-01 .. I-09 | Reference counts outside sealed sprint records, by old name: `THIRD_PARTY_PROVENANCE_TODO` in `SECURITY.md`, `NOTICE.md`, `README.md` (line 214 twice), `CONTRIBUTING.md`, `profiles/example-project/README.md`; `topology_map.md` in `rules/token_economy.md:22`, `workflows/extract_workflow.md:27`, `docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md` (lines 6 and 52), `docs/hotfixes/H-007-mcp.md:38`, `docs/contracts/core/topology_scaffolder_contract.md:22`, `docs/contracts/core/topology_mapper_contract.md:25`; `global_topology.md` in `docs/contracts/core/doc_orchestrator_contract.md:9`, `skills/contract-writer/SKILL.md:30`; `SKILLOPT_TRANSITIVE_CLOSURE.md` in `skills/skillopt/SKILL.md:21`, `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:680`, `docs/roadmaps/core/pipeline/021-030-program-queue.md:1321`; the roadmap entries `007`, `014`, `015`, `016`, `017`, `018` and `docs/audits/PIPELINE_AUDIT_REPORT-059.md` also name old paths |

## Rule audit findings

Severity follows `RA-17` (S0 to S3). Each finding is reported as unit, rule, finding, proposed fix. This audit did not edit the plan, `agent_assignment.md` or `skill_assignment.md`.

| ID | Unit | Rule | Finding | Proposed fix | Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RV-1 | I-01 .. I-09 | `RA-14`, `jurisdictional_lock` | Each rename leaves live references in files no row claims (list under "Dependent files"), among them `SECURITY.md`, `NOTICE.md`, `README.md`, `CONTRIBUTING.md`, `rules/token_economy.md`, `workflows/extract_workflow.md` and two `skills/*/SKILL.md`. The row's check (`grep` of the old path returns 0 outside sealed records) cannot pass unless those are edited; the plan does not say they are companion edits. `agents.md §2 jurisdictional_lock` permits companions the subject requires. | State in each I-row that reference edits are companions of the `git mv` commit. Vendored `skills/*/SKILL.md` are not edited (`rules/skills_and_integrations.md §3`): record those two hits as sealed or exempt before D10 is called closed. | S2 |
| RV-2 | D-01 | `RA-16` | `## Mechanisms` names `Makefile#verify` as the invoker of `scripts/check_host_terms.py`, but no Work row modifies the `Makefile`. `verify_references.py` (d) resolves `invoked_by:` tokens and fails on an unwired script. | Add a row `Makefile` / modify / low, or fold the edit into D-01 as its companion, in the plan. | S2 |
| RV-3 | A-04 | `RA-16` | `scripts/install_broker.py` names `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` as its invoker, which A-09 creates after A-04. `check_invoked_by_anchors` resolves the path at A-04's commit and finds nothing. | Order A-09 before A-04, or declare A-04's `invoked_by:` on `workflows/deployment_workflow.md` until A-09 lands. Same check for A-03 against A-11. | S2 |
| RV-4 | D-04 | `RA-15`, `RA-09` | `HISTORY_REVIEW_REPORT.md` is committed. A scan of `origin/main` that quotes the matching line would write the plaintext host name the hash list exists to keep out (D9). | Record commit SHA, file path and line number only; never the matched text. | S1 |
| RV-5 | A-10 | `RA-09` | M1 reads keys "from the sandbox" with `cat`, `Read` and `Edit`. If the deny fails, the key material enters the agent context. | Measure with exit codes only (`test -r`, `stat`, `wc -c` discarded to `/dev/null`) and never print content; record the exit code. | S1 |
| RV-6 | A-10 | `RA-19` (1) | M3 claims "no sandbox process obtains a token". `RA-19` forbids a boundary claim without a measured enumeration of every out-of-sandbox entry point, and `F-055-N1` (writable hooks and project MCP) stays open per the plan's Context. | List the entry points M3 enumerates (project `.mcp.json`, hooks, `claude/settings.hooks.json`, launchd) and measure each, or word M3 as "the enumerated set" with its criterion. | S1 |
| RV-7 | A-10 | Abort criterion, `pipeline_workflow.md` Phase 6 | M5 (five operations on GitHub) happens at the 060 deployment, after Phase 8. The row cannot be `committed` before QA gates, yet the Abort criterion requires M1-M5 green. | Split A-10 into A-10 (M1-M4, pre-gate) and a deploy-time row for M5, or state that M5 is written during deployment and gates read M1-M4. | S2 |
| RV-8 | B-01, G-01, G-02, E-01 | `rules/code_craft.md §6` | The plan's `## Tests` lists commands, not a test id, for the `fix(` units. `check_fix_reproduces.py` needs a `Repro: <test id>` that exits `1` on the parent tree and `0` at the commit. Companion test files are named in the rows, which satisfies the pairing. | Name the new test function in each row (for example `tests/test_unit_cost.py::<name>`), or use `Repro: manual` with its reason. A-07, A-08 and L-03 are `feat`, not `fix`. | S2 |
| RV-9 | K-01 | `agents.md §8` supply chain, `RA-14` | `rules/graphify.md` (lines 18 and 32) states "graphifyy 0.8.30" measured facts and `rules/project_topology.md` cites the pin; no row updates them after the bump. | Make the `rules/graphify.md` update a K-01 companion; `rules/project_topology.md` falls under A-13 or H-02 (in-order). | S2 |
| RV-10 | A-01 | `agents.md §4`, `RA-14` | ADR-0025 "replaces `ADR-0019` D2 and D6", but no row edits `ADR-0019`'s status, and `rules/project_topology.md` (6 hits), `workflows/repository_hardening_workflow.md` and `scripts/install.py` cite it. Likewise L-05 amends `ADR-0024`. | Add a companion edit to A-01 and L-05 marking the superseded or amended sections in the old ADR. | S2 |
| RV-11 | A-12, A-11, F-01 | `agents.md §6 devops_agent`, `ADR-0009` | `devops_agent` has `Bash` only, yet its profile (A-12) and the §6 row (F-01) are to say it uses broker tools that perform pushes. Assignments are correct (`doc_orchestrator`, `rule_validator`). Only the wording needs care: the broker, not `devops_agent`, holds write authority. | Word A-12 and F-01 so the broker operations are invoked through the MCP tools the profile lists, and verify with the profile's `tools:` line. | S3 |
| RV-12 | Z-04 | `active_state.json` `acknowledged_gaps.walkthroughs` | The nucleus accepted having no `docs/walkthroughs/` hierarchy (Sprint 042); `Glob docs/walkthroughs/**` finds none. Z-04 creates the first file, which the acknowledged gap says would "inaugurate a structure nothing else populates". | Remove Z-04 or have the plan record the human decision to end the acknowledged gap; do not create it silently. | S2 |
| RV-13 | Plan Cost, `agent_assignment.md` | `RA-14` | The plan says "52 work units" and "45 + gates"; `agent_assignment.md` states "all 37 Work rows". All 52 rows are in its tables, so the sentence is stale. | `agent_orchestrator` corrects "37" to "52"; headline counts need a reproducible command. | S3 |
| RV-14 | A-05, L-04 | `RA-19` (2) | L-04 widens egress (`api.osv.dev`) and A-05 narrows reads; nothing asserts that no `sandbox.excludedCommands` entry exists after either edit. | Add `grep -c excludedCommands claude/settings.hooks.json` expecting `0` to both rows' checks. | S3 |
| RV-15 | A-06, D-02 | `RA-09`, `RA-15` | Both files hold material the human supplies. The rows are `implementer_agent` creations with no stated source, so an agent could invent the content. | State in each row that the agent writes only after the human pastes the value, and does not fabricate keys or hashes. | S3 |

No finding against `RA-16` for `check_dependency_advisories.py` (invokers `.github/workflows/ci.yml` and `scripts/session_start.py` are rows L-02 and L-03, ordered after L-01) or for `detect_new_models.py` and `check_gate_log.py` (already invoked by `Makefile`: lines 79 and 84). No finding against `RA-09` for A-09: the guide prepares human steps only. No finding against `agents.md §6` role boundaries for F-01, F-02 and J-02 (`rule_validator` holds `Write` and `Edit`). `scripts/check_task_scope.py` capability check passes on every row: no row has a profile without `Write`/`Edit`.
