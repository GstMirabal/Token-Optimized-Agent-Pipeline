# Agent Assignment — Sprint 060 (core-pipeline)

Source: `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code**, `delegation_mode: native` — the
`Assignee` column names which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

`Destination` is **required** on every unit that **creates** an agent profile.
Values: `host:.claude/agents/` (default), `profile:<path>`, `nucleus:PR`.
Units that do not create a profile use `N/A`.

No agent profile is created in Sprint 060: all 37 Work rows are staffed from the 14 existing profiles in `agents/`. Every `Destination` is `N/A`. The `fix` operations of the plan (B-01, G-01, G-02) are recorded as `modify`; the `rename` operations of I-01…I-09 (`git mv`) are recorded as `modify` with the pre-rename path as Target.

---

## Staffing

### Wave A — GitHub App broker

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/decisions/ADR-0025-github-app-broker.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-02 | `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-03 | `scripts/github_broker.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-04 | `scripts/install_broker.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-05 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-06 | `config/allowed_signers` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-07 | `scripts/sync_agents_pin.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-08 | `scripts/install.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-09 | `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-10 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-11 | `workflows/deployment_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-12 | `agents/devops_agent.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-13 | `rules/project_topology.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-14 | `workflows/repository_hardening_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave B — Model detector

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B-01 | `scripts/detect_new_models.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-02 | `config/model_tiers.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave C — Ledger seal

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| K-01 | `requirements-core.txt` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-01 | `scripts/check_dependency_advisories.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-02 | `.github/workflows/ci.yml` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-03 | `scripts/session_start.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-04 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-05 | `docs/decisions/ADR-0026-dependency-advisory-check.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| L-06 | `.github/dependabot.yml` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C-01 | `workflows/deployment_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave D — Host-term scanner

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `scripts/check_host_terms.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-02 | `config/host_term_hashes.json` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-03 | `tests/test_profile_references.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-04 | `docs/sprints/060-core-pipeline/HISTORY_REVIEW_REPORT.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave E — Gate log

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E-01 | `scripts/check_gate_log.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave F — Normative text

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-01 | `agents.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| F-02 | `rules/skills_and_integrations.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |

### Wave G — Measurement scripts

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G-01 | `scripts/unit_cost.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| G-02 | `scripts/prompt_count.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave H — Sandbox re-measurement

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| H-01 | `docs/sprints/060-core-pipeline/SANDBOX_REMEASUREMENT.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| H-02 | `rules/project_topology.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave I — RA-06 renames (D10, audit 059 R1-R9)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| I-01 | `docs/architecture/global_topology.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I-02 | `docs/architecture/topology_map.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I-03 | `docs/contracts/core/doc_orchestrator_contract.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I-04 | `docs/contracts/core/topology_mapper_contract.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I-05 | `docs/contracts/core/topology_scaffolder_contract.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I-06 | `docs/audits/TOKEN_ECONOMY_AUDIT-documentation-standard.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I-07 | `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I-08 | `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| I-09 | `docs/plans/027-autonomy-posture-DRAFT.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

New names (D10): I-01 `GLOBAL_TOPOLOGY_MAP.md`; I-02 `TOPOLOGY_MAP.md`; I-03 `DOC_ORCHESTRATOR_CONTRACT.md`; I-04 `TOPOLOGY_MAPPER_CONTRACT.md`; I-05 `TOPOLOGY_SCAFFOLDER_CONTRACT.md`; I-06 `TOKEN_ECONOMY_DOCUMENTATION_STANDARD_AUDIT.md`; I-07 `SKILLOPT_TRANSITIVE_CLOSURE_AUDIT.md`; I-08 `THIRD_PARTY_PROVENANCE_REGISTER.md`; I-09 `AUTONOMY_POSTURE_PLAN.md`.

### Wave J — Audits

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J-01 | `docs/audits/PROMPT_AUDIT_REPORT-060.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| J-02 | `docs/audits/PROSE_MOTIVES_AUDIT_REPORT-060.md` | create | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |

### Wave Z — Pipeline and closeout artifacts

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Z-01 | `docs/sprints/060-core-pipeline/SPRINT_LOG.md` | create | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |
| Z-02 | `docs/sprints/060-core-pipeline/task_scope.md` | create | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| Z-03 | `docs/sprints/060-core-pipeline/agent_assignment.md` | create | sequential | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| Z-04 | `docs/walkthroughs/core/pipeline/060_WALKTHROUGH.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Z-05 | `CHANGELOG.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Z-06 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |

## Disagreements with the plan

| Unit | Plan proposal | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| A-10 | `devops_agent` | `implementer_agent` | `devops_agent` holds `Bash` but no `Write`/`Edit` (`agents/devops_agent.md` `write_scope`), so it cannot write the report. `implementer_agent` holds `Bash` and `Write`, so one profile runs M1-M5 and records the output. Steps that need the human (App creation, `install_broker.py`, `claude mcp add`) stay human-run per `A-09`. |
| D-04 | `devops_agent` | `implementer_agent` | Same tool gap. The scan runs `scripts/check_host_terms.py` (authored in D-01 by this profile) over `origin/main`; rewriting history stays a human decision (`KI-059-12`). |
| H-01 | `devops_agent` | `implementer_agent` | Same tool gap. The 055 and 056 matrices are Bash measurements whose result must be written to `SANDBOX_REMEASUREMENT.md`; a runner/writer split would need two assignees on one row. |
| J-01 | `token_economy_agent` | `implementer_agent` | `token_economy_agent` holds `Bash` but no `Write`/`Edit` (`agents/token_economy_agent.md`, `task_scope_model_proposal`), so it cannot create the report. `implementer_agent` runs the byte and token measurements and writes the report. `token_economy_agent` stays accountable for classifying each finding at the Phase 5 plan audit and for `J-NN` rows. |
| B-02 | `token_economy_agent` | `implementer_agent` | `token_economy_agent` owns `config/model_tiers.json` (`tier_ownership`) but has no `Write`/`Edit`; the same profile staffs `config/` JSON in A-06 and D-02 and `B-01` (its sibling `detect_new_models.py`), per `agents/implementer_agent.md` `scope_boundaries` (changes requested through `implementer_agent`). The value choices come from `token_economy_agent`. |
| A-12 | `agent_orchestrator` | `doc_orchestrator` | `agent_orchestrator` has exclusive jurisdiction over agent staffing and never edits profile content (`restriction`); A-12 rewrites a profile's rules text, which is documentation authoring. `A-12` must also match the `A-11` deployment text. |

Notes, no change: A-05, A-06 and D-02 are `config/` or `claude/` files outside the literal `scripts/`, `hooks/`, `tests/` write scope of `implementer_agent`, but they are code-adjacent configuration with no other profile holding `Write` and a code role; the plan proposal stands. `A-06` and `D-02` content is supplied by the human. F-01, F-02 and J-02 stay with `rule_validator` as proposed.
