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

No agent profile is authored in Phase 4.1: all 102 Work rows are staffed from the 14 existing profiles in `agents/`, and forging a profile is decided after O-09 records its evidence, by this file and `skill_assignment.md` under D17 (`## Candidates`, RV-20). Every `Destination` is `N/A`. The `fix` operations of the plan (B-01, G-01, G-02) are recorded as `modify`; the `rename` operations of I-01…I-09 (`git mv`) are recorded as `modify` with the pre-rename path as Target.

---

## Staffing

### Wave A — GitHub App broker

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/decisions/ADR-0025-github-app-broker.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-02 | `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-03 | `scripts/github_broker.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-09 | `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-04 | `scripts/install_broker.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-05 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-06 | `config/allowed_signers` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-07 | `scripts/sync_agents_pin.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-08 | `scripts/install.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-10 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A-11 | `workflows/deployment_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-12 | `agents/devops_agent.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-13 | `rules/project_topology.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-14 | `workflows/repository_hardening_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| A-15 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave B — Model detector

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B-01 | `scripts/detect_new_models.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B-02 | `config/model_tiers.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave K — graphifyy pin

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| K-01 | `requirements-core.txt` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave N — Session transcript read (D16)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| N-01 | `docs/decisions/ADR-0027-session-transcript-read.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| N-02 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| N-03 | `scripts/install.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| N-04 | `docs/sprints/060-core-pipeline/TRANSCRIPT_READ_MEASUREMENT.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

Ordering: N-02 runs after A-05 and before L-04, O-11 and M-14 (same file); N-03 runs after A-08 (same file). N-02 is a `claude/` file on the same code-adjacent basis as A-05; the plan proposal stands for all four rows.

### Wave M — Graph as brain (D14)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M-01 | `scripts/graph_battery.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-02 | `docs/audits/GRAPH_USAGE_AUDIT_REPORT-060.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-03 | `scripts/graph_query.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-04 | `scripts/graph_mcp.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-05 | `claude/mcp.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-06 | `rules/graphify.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-07 | `agents/principal_agent.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-08 | `agents/rule_validator.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-09 | `agents/qa_agent.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-10 | `agents/implementer_agent.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-11 | `agents/doc_orchestrator.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-12 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-13 | `hooks/graph_usage_log.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-14 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-15 | `scripts/check_graph_usage.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-16 | `docs/sprints/060-core-pipeline/GRAPH_AB_MEASUREMENT.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| M-17 | `workflows/close_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| M-18 | `scripts/install_broker.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

Ordering: M-17 adds the step that invokes `scripts/check_graph_usage.py` (M-15) and its commit includes the regenerated `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (RV-19, RV-29); M-18 runs after A-04 and M-04 (same file as A-04; RV-28). M-14 runs after A-05, N-02, L-04 and O-11 (same file).

### Wave O — Forge trigger and capability evaluation (D17)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| O-01 | `docs/decisions/ADR-0028-forge-trigger.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| O-02 | `rules/skills_and_integrations.md` | modify | sequential | `rule_validator` | N/A | `agents/rule_validator.md` |
| O-03 | `agents/agent_orchestrator.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| O-04 | `agents/skill_architect.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| O-05 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| O-06 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| O-07 | `scripts/check_forge_ladder.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| O-08 | `scripts/capability_usage.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| O-09 | `docs/audits/CAPABILITY_EVALUATION_REPORT-060.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| O-10 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| O-11 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| O-12 | `agents/implementer_agent.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| O-13 | `docs/sprints/060-core-pipeline/agent_assignment.md` | modify | sequential | `agent_orchestrator` | N/A | `agents/agent_orchestrator.md` |
| O-14 | `docs/sprints/060-core-pipeline/skill_assignment.md` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |

Ordering O-09 → O-13 → O-14: O-13 writes the forge/reuse decision per agent candidate from the O-09 evidence, and O-14 does the same for skill candidates; the two are reconciled on `claude/settings.hooks.json` (RV-39). M-18 runs before M-05 and M-16 (RV-35).

### Wave Q — Phase 6 parallel batches without worktrees (KI-060-04)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Q-01 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Q-02 | `workflows/pipeline_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

Ordering O-12 → Q-01 → S-01 → Q-02 → Wave A: Q-01 runs after O-12 and before batch 2; Q-01 runs before M-12 and before O-10 (same file). Q-02 runs after S-01 and before Wave A batch 2 (A-11 regenerates the same `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` that the Q-02 commit includes regenerated), and before M-12 and O-10 (same file `workflows/pipeline_workflow.md`, also Q-01's). Q-01 and Q-02 edit Phase 6 text of a workflow (Q-02 adds the `check_readme_counts.py --write` step), which is documentation authoring, so `doc_orchestrator` stays as proposed for both.

### Wave S — skill dependencies declared and fail-closed (KI-060-05)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S-01 | `docs/sprints/060-core-pipeline/skill_assignment.md` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| S-02 | `requirements-quality.txt` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| S-03 | `skills/python-quality-auditor/scripts/python_quality_auditor.py` | modify | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| S-04 | `docs/sprints/060-core-pipeline/SKILL_DEPENDENCY_REPORT.md` | create | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| S-05 | `scripts/check_skill_dependencies.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

Ordering Q-01 → S-01 → Q-02 → Wave A batch 2; Wave A → S-02 → S-03 → S-04 → S-05 → Wave B: S-01 runs after Q-01 and before Wave A batch 2; S-02 to S-05 run after Wave A and before Wave B, in that order (S-03 needs the tools S-02 pins; S-04 measures the S-03 script; S-05 gates on what S-04 measures). S-01 is the same class of file as Z-07 (`skill_assignment.md`), so `skill_architect` stays. S-02 stays `skill_architect`: `agents/implementer_agent.md` `write_scope` names `requirements-core.txt` but not `requirements-quality.txt`, so `implementer_agent` has no listed claim on the file, while `skill_architect` has `Write`/`Edit`/`Bash` (`tools:` line) and no scope restriction; the regeneration of `requirements-core.txt` that S-02 allows is a same-commit companion write of the single structural subject `requirements-quality.txt`. Re-check after the 2e5abcf reword (companions `README.md:91`, `Makefile:23` and `requirements-core.txt` line 5 edited in the same commit): the conclusion is unchanged, because each is a companion of the one subject `requirements-quality.txt` (not under `scripts/`, `hooks/` or `tests/`, so `ADR-0009` does not apply) and `skill_architect` has no scope restriction, so S-02 stays `skill_architect` with no disagreement. S-03 stays `skill_architect`: its subject is under `skills/[name]/scripts/`, which `implementer_agent` `write_scope` and `scope_boundaries` PROHIBIT; `tests/test_python_quality_auditor.py` is the paired test of a `fix(` commit (`agents.md §2 jurisdictional_lock`, `rules/code_craft.md §6`), a companion and not a second subject, so the `ADR-0009` rule (a unit whose structural subject is under `tests/` MUST go to `implementer_agent`) does not apply. S-04 is a sprint-directory report on skills and stays `skill_architect` (it holds `Bash` for the measurements). S-05 stays `implementer_agent` (`ADR-0009`: framework-root `scripts/`); its `tests/test_check_skill_dependencies.py` and `Makefile` (named in `write_scope`) are companions, and the `README.md` counted block is regenerated by `scripts/check_readme_counts.py --write` rather than hand-edited. No row is a disagreement.

Ordering (plan execution order: O-12 → Q-01 → S-01 → Q-02 → A → S-02 → S-03 → S-04 → S-05 → B → K → N → L-04 → O-11 → M → O without O-02, O-09, O-11, O-12 → L without L-04 → C → D → E → P → F → O-02 → G → H → T → I → J → O-09 → O-13 → O-14 → Z): T-01 runs after H-01, T-02 after T-01, T-03 after T-02 and T-04 after T-03 (Wave T, KI-060-07); O-12 runs first in the sprint, widening the `write_scope` of `implementer_agent` before M-10 (same file) and before O-09; O-02 runs after F-02 (same file); O-08 runs after N-04; O-09 runs after O-12 and H-01; O-10 runs after M-12 (same file); Q-02 runs before M-12 and O-10 (same file) and before A-11 (same generated guide); L-04 runs before O-11 and O-11 before M-14 (same file). O-12 edits a profile's `write_scope` and amends `ADR-0009` in the same commit, which is documentation authoring on the A-12 basis, so `doc_orchestrator` stays as proposed. O-03 edits `agents/agent_orchestrator.md` and O-04 edits `agents/skill_architect.md`, both profile rules text, which is documentation authoring on the A-12 basis.

### Wave L — Dependency advisories

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| L-01 | `scripts/check_dependency_advisories.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-02 | `.github/workflows/ci.yml` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-03 | `scripts/session_start.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-04 | `claude/settings.hooks.json` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| L-05 | `docs/decisions/ADR-0026-dependency-advisory-check.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| L-06 | `.github/dependabot.yml` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave C — Ledger seal

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C-01 | `workflows/deployment_workflow.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave D — Host-term scanner

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `scripts/check_host_terms.py` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-02 | `config/host_term_hashes.json` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-03 | `tests/test_profile_references.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-04 | `docs/sprints/060-core-pipeline/HISTORY_REVIEW_REPORT.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| D-05 | `Makefile` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave E — Gate log

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E-01 | `scripts/check_gate_log.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave P — Task-scope parity check

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P-01 | `scripts/check_task_scope.py` | modify | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |

Ordering: P-01 runs after E-01 and before F-01. It is a `fix` (exit `2` when a plan Work id is missing from `task_scope.md` or the reverse; KI-060-02, RV-17), recorded as `modify`; `scripts/` falls under `ADR-0009`, so `implementer_agent`.

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

### Wave T — Local database route (KI-060-07)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T-01 | `docs/sprints/060-core-pipeline/DB_ROUTE_MEASUREMENT.md` | create | sequential | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| T-02 | `docs/decisions/ADR-0029-local-database-route.md` | create | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| T-03 | `rules/qa_and_testing.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| T-04 | `agents/tester_agent.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

Ordering H-01 → T-01 → T-02 → T-03 → T-04 → Wave I: T-01 runs after H-01 (same sandbox surface; H-01 fixes the measuring CLI, `KI-059-31`); T-02 runs after T-01 (it needs the T-01 evidence); T-03 runs after T-02 (it transcribes the T-02 decision); T-04 runs after T-03 (its line 18 repeats `local_testing` and reflects what T-03 writes in `rules/qa_and_testing.md` §7, RV-60). Same-file check, Grep of `qa_and_testing\.md|ADR-0019|021-030-program-queue|tester_agent` over the plan Work rows: `rules/qa_and_testing.md` is the subject of T-03 only (M-10 cites it inside `agents/implementer_agent.md` and does not edit it). `agents/tester_agent.md` is the subject of T-04 only (1 matching Work row; no other row edits it), so no record order between rows is needed beyond T-03 → T-04. `docs/decisions/ADR-0019-sandbox-regime.md` is not a subject row; it receives one-line companion edits from A-01 (`Superseded by ADR-0025`) and N-01 (`Amended by ADR-0027`), both in Waves A and N, which run before Wave T, and from T-02 (`Amended by ADR-0029`) after them, so no two edits are concurrent. O-01 amends `ADR-0024` (`Amended by ADR-0028`, egress `skills.sh`), not `ADR-0019` (RV-61). `docs/roadmaps/core/pipeline/021-030-program-queue.md` is the subject of Z-06 (Wave Z, last) only; T-02 does not edit it, and Z-06 updates the `KI-057-1` row from the T-02 result (RV-62). The `Amended by ADR-0029` line is a companion of the single subject `ADR-0029-local-database-route.md` (`agents.md §2 jurisdictional_lock`); T-02 branch 1 spawns `T-NN` implementation rows for `claude/settings.hooks.json` and `scripts/sandbox_probe.py`, which are staffed here when they land. `doc_orchestrator` holds `Write`/`Edit` and no scope restriction (`tools:` line).

T-01 stays `implementer_agent`, the plan proposal. `agents/implementer_agent.md` `write_scope` names sprint-directory `*_MEASUREMENT.md` files when a Work row assigns them, and the profile holds `Bash` and `Write`, so one profile runs the per-route measurements and writes the result, as for H-01 and A-10. `devops_agent` is the profile for Docker health and `.env` but holds `Bash` only (`tools:` line; `write_scope`: no `Write`/`Edit`), so it cannot create the file. The profile `restriction` that `implementer_agent` does not own Docker or `.env` is respected: the Docker and `.env` steps are prepared as exact commands with the expected result, the human runs them and pastes the output (`RA-09`, same as A-10 and `A-09`), and `implementer_agent` records the pasted output in the report and never reads `.env`. T-04 edits profile rules text, which is documentation authoring on the A-12 basis, so `doc_orchestrator` stays as proposed. T-02 and T-03 are an ADR and a `rules/` section, which is documentation authoring; `rule_validator` (proposed for `rules/` rows O-02, F-01, F-02) is not applied because T-03 transcribes a decision already made in T-02 and does not set new normative text. No disagreement.

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
| Z-07 | `docs/sprints/060-core-pipeline/skill_assignment.md` | create | sequential | `skill_architect` | N/A | `agents/skill_architect.md` |
| Z-05 | `CHANGELOG.md` | modify | sequential | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| Z-06 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | sequential | `orchestrator` | N/A | `agents/orchestrator.md` |

## Candidates

Decision D17 applied from the plan text (the template gains this table in O-05). Criterion (a): the same operation on the same class of subject appears in >= 3 plan units, or in >= 2 of the previous 5 sprints (`docs/sprints/055…059-core-pipeline/agent_assignment.md`). Criterion (b): the unit's subject is governed by a `rules/` file that the assigned profile in `agents/` does not cite. Decision values: `reuse` (the existing profile already holds the tools and scope; the gap, if any, is text in that profile) or `forge-pending-O-09` (O-09 records the evidence only; the `forge`/`reuse` decision for each candidate stays with this file and `skill_assignment.md` after O-09, RV-20; no profile is authored in Phase 4.1). The final decision for every candidate is written by O-13 (RV-37), not by this table; the `claude/settings.hooks.json` agent candidate and skill candidate C6 are reconciled in O-13 with O-14 (RV-39). Counts below are Grep line counts run over the plan Work rows (`^\| [A-Z]-\d\d \|` + the stated pattern) and over `docs/sprints/055…059-core-pipeline/agent_assignment.md`.

| Candidate | Units | Criterion (a/b) | Evidence | Decision | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Sandbox/security measurement agent | A-10, A-15, H-01, N-04, T-01 | a, b | (a) Work rows whose File matches `(MEASUREMENT\|REMEASUREMENT)\.md` under `docs/sprints/060-…`: 6 (these 5 plus M-16, which measures token cost and is governed by `rules/token_economy.md`, so it is not counted in this class); lines matching `MEASUREMENT\|REMEASUREMENT` in prior assignments: 055=4, 057=2, 058=1, 059=29, 056=0. (b) these units are governed by `rules/project_topology.md` (`RA-09`, `RA-19`); `agents/devops_agent.md` cites it but has no `Write`/`Edit`; `agents/implementer_agent.md` cites `rules/code_craft.md` only (Grep `rules/[a-z_]+\.md` over `agents/`) | `forge-pending-O-09` | 5 units in this class (>= 3; T-01 measures the `ADR-0019` D4 routes, governed by `rules/project_topology.md` `RA-19`) and the only profile that can write them does not cite the governing rule. O-09 records the A/B by `session_cost.py` (>= 30 % fewer `fresh` tokens), run by the agent under the sandbox after N-04 (D16, RV-24); the decision is written here and in `skill_assignment.md` afterwards (RV-20). Until then `implementer_agent` stays assignee. |
| `claude/settings.hooks.json` sandbox-config editor | A-05, N-02, L-04, O-11, M-14 (exactly 5 units, RV-23) | a, b | (a) Work rows whose File is `claude/settings.hooks.json`: 5; lines naming the file in prior assignments: 055=4, 056=2, 057=2, 058=1, 059=5 (5 of 5 sprints). (b) file content is the `denyRead`/`allowRead`/network regime governed by `rules/project_topology.md`, not cited by `implementer_agent` | `forge-pending-O-09` | Same governing rule and same uncited gap as the measurement candidate; O-09 records evidence for both together and the decision follows here (RV-20) because the units share the file and the subject class. |
| ADR author | A-01, N-01, L-05, O-01, T-02 | a | Work rows whose File matches `docs/decisions/ADR-` (Grep `^\| [A-Z]-\d\d \| \`docs/decisions/ADR-` over the plan): 5; lines naming `docs/decisions/ADR-` in prior assignments: 059=8, others 0 (1 of 5 sprints) | `reuse` | `doc_orchestrator` already holds `Write`/`Edit` (`tools:` line of `agents/doc_orchestrator.md`); no tool gap. |
| Documentation author under `rules/documentation_standard.md` | every `doc_orchestrator` row (A-01, A-02, A-09, A-11…A-14, N-01, M-06…M-12, O-01, O-03…O-06, O-10, L-05, C-01, H-02, I-01…I-09, M-17, O-12, Q-01, Q-02, T-02, T-03, T-04, Z-05) | b | `agents/doc_orchestrator.md` contains no `rules/` citation (Grep `rules/\|documentation_standard` over that file: 0); `rules/documentation_standard.md` governs any document under `docs/` or `rules/` | `reuse` | The gap is a missing citation, not a missing capability: the profile already owns documentation authoring. M-11 adds the missing `rules/documentation_standard.md` citation to `agents/doc_orchestrator.md` (RV-31); the fix is profile text, not a new profile. |
| Agent-profile text editor | A-12, M-07, M-08, M-09, M-10, M-11, O-03, O-04, O-12, T-04 | a | Work rows whose File matches `agents/` (Grep `^\| [A-Z]-\d\d \| \`agents/` over the plan): 10 | `reuse` | Editing profile rules text is documentation authoring (A-12 basis); `agent_orchestrator` has jurisdiction over staffing only and never edits profile content. |
| Workflow-text editor | A-11, A-14, C-01, M-12, M-17, O-10, Q-01, Q-02 | a | Work rows whose File matches `workflows/` (Grep `^\| [A-Z]-\d\d \| \`workflows/` over the plan): 8 | `reuse` | `doc_orchestrator` holds the tools; no governing `rules/` file is outside its scope beyond the documentation-standard row above. |
| Test-bearing script author | A-03, A-04, A-07, A-08, B-01, N-03, M-01, M-03, M-04, M-13, M-15, M-18, L-01, L-03, D-01, E-01, P-01, G-01, G-02, O-07, O-08, S-03, S-05 | a, b | Work rows matching `test \`tests/` (Grep `^\| [A-Z]-\d\d \|.*test \`tests/`): 23 (S-03 is staffed to `skill_architect`, its subject being under `skills/[name]/scripts/`, so 22 of the 23 are `implementer_agent` rows); `rules/qa_and_testing.md` governs tests and is not cited by `agents/implementer_agent.md` (Grep over that file: only `rules/code_craft.md`) | `reuse` | `ADR-0009` assigns `scripts/`, `hooks/`, `tests/` to `implementer_agent`; the citation gap is profile text, closed by M-10, which adds the `rules/qa_and_testing.md` citation to `agents/implementer_agent.md` (RV-31). Pairing a test with its script is one unit, so a second profile would split one claim. |

Not candidates (neither criterion met): the graph structural-query skill over M-03 named in O-09 (one unit on that subject, 1 < 3; skills are evaluated in `skill_assignment.md`); `config/` JSON (A-06, B-02, D-02: 3 units but the class differs per file and no `rules/` file is uncited); renames I-01…I-09 (one operation, already `doc_orchestrator`, covered by the documentation-author row).

## Disagreements with the plan

| Unit | Plan proposal | Assigned | Reason |
| :--- | :--- | :--- | :--- |
| A-10 | `devops_agent` | `implementer_agent` | `devops_agent` holds `Bash` but no `Write`/`Edit` (`agents/devops_agent.md` `write_scope`), so it cannot write the report. `implementer_agent` holds `Bash` and `Write`, so one profile runs M1-M5 and records the output. Steps that need the human (App creation, `install_broker.py`, `claude mcp add`) stay human-run per `A-09`. |
| D-04 | `devops_agent` | `implementer_agent` | Same tool gap. The scan runs `scripts/check_host_terms.py` (authored in D-01 by this profile) over `origin/main`; rewriting history stays a human decision (`KI-059-12`). |
| H-01 | `devops_agent` | `implementer_agent` | Same tool gap. The 055 and 056 matrices are Bash measurements whose result must be written to `SANDBOX_REMEASUREMENT.md`; a runner/writer split would need two assignees on one row. |
| J-01 | `token_economy_agent` | `implementer_agent` | `token_economy_agent` holds `Bash` but no `Write`/`Edit` (`agents/token_economy_agent.md`, `task_scope_model_proposal`), so it cannot create the report. `implementer_agent` runs the byte and token measurements and writes the report. `token_economy_agent` stays accountable for classifying each finding at the Phase 5 plan audit and for `J-NN` rows. |
| B-02 | `token_economy_agent` | `implementer_agent` | `token_economy_agent` owns `config/model_tiers.json` (`tier_ownership`) but has no `Write`/`Edit`; the same profile staffs `config/` JSON in A-06 and D-02 and `B-01` (its sibling `detect_new_models.py`), per `agents/implementer_agent.md` `scope_boundaries` (changes requested through `implementer_agent`). The value choices come from `token_economy_agent`. |
| A-12 | `agent_orchestrator` | `doc_orchestrator` | `agent_orchestrator` has exclusive jurisdiction over agent staffing and never edits profile content (`restriction`); A-12 rewrites a profile's rules text, which is documentation authoring. `A-12` must also match the `A-11` deployment text. |

Adopted by the plan in 241fc29 (no longer a disagreement): O-09 is now proposed as `implementer_agent` after O-12 widens its `write_scope`. `implementer_agent` runs `capability_usage.py` and the A/B `session_cost.py` runs under the sandbox after N-04 (D16, RV-24) and records evidence only; the `forge`/`reuse` decision for each candidate stays with this file and `skill_assignment.md` after O-09 (RV-20). `token_economy_agent` stays accountable for the threshold judgment at the Phase 5 plan audit.

Notes, no change (amendment: O-12, P-01, M-17, M-18 added in 241fc29; A-15, D-05, M-01…M-16 added, Z-04 deleted per D15, A-09 moved before A-04): A-15 is a `modify` of the A-10 report; the push, PR, merge, tag and Release calls of M5 go through the broker MCP tools, which `implementer_agent` (`tools: Read, Glob, Grep, Write, Edit, Bash`) does not list, so the lead session issues those calls and `implementer_agent` records each GitHub ID in the report. M-07…M-11 edit other profiles' rules text, which is documentation authoring (same basis as the A-12 override), so `doc_orchestrator` stays; M-11 edits its own profile and M-10 edits the profile of the Wave M code author, with no concurrent claim on either file. M-05, M-14 and D-05 (`claude/mcp.json`, `claude/settings.hooks.json`, `Makefile`) sit outside the literal `scripts/`, `hooks/`, `tests/` scope on the same code-adjacent basis as A-05; `devops_agent` has no `Write`/`Edit`. M-16 needs `session_cost.py`, run by `implementer_agent` under the sandbox after N-04 (D16, RV-24), which writes the output into the report. Earlier note: A-05, A-06 and D-02 are `config/` or `claude/` files outside the literal `scripts/`, `hooks/`, `tests/` write scope of `implementer_agent`, but they are code-adjacent configuration with no other profile holding `Write` and a code role; the plan proposal stands. `A-06` and `D-02` content is supplied by the human. F-01, F-02 and J-02 stay with `rule_validator` as proposed.
