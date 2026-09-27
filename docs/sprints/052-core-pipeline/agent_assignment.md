# Agent Assignment — Sprint 052 (core-pipeline)

Source: `docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code** (nucleus), `delegation_mode: native` — the `Assignee`
column names which profile's ruleset governs each write. This artifact does
not carry Model/Effort tiers — those are `token_economy_agent` → `rule_validator`
territory, transcribed into `task_scope.md` at Phase 4.3
(`agents.md §6 agent_orchestrator` `no_model_columns`).

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Model / effort (`task_scope.md`, Phase 4.3) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

**No unit in this sprint creates a new agent profile.** Every U1–U67 (and the
`K1..Kn` contingency slot) assigns an existing core or auxiliary role
(`doc_orchestrator`, `implementer_agent`, `rule_validator`, `skill_architect`).
`Destination` is `N/A` on every row and `check_forge_ladder.py` has no forge
row to validate — confirmed: no row has a `create` operation whose Target
matches an `agents/*.md` path, and no row's Destination is a forge
destination (`host:.claude/agents/`, `nucleus:PR`, or `profile:`).

---

## Staffing

Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave 1 — Records

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 2 — Session and anchor defects

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U2 | `scripts/session_start.py` (subject) + paired `tests/test_session_start.py` | fix( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U3 | `scripts/session_state.py` (subject) + paired `tests/test_session_state.py` | fix( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U4 | `scripts/session_state.py` (subject) + paired `tests/test_session_state.py` | feat( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U5 | `scripts/session_start.py` (subject) + paired `tests/test_session_start.py` | fix( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U6 | `workflows/start_workflow.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U7 | `commands/start.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 3 — Upstream findings

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U8 | `docs/decisions/ADR-0015-artifact-owner-writer-separation.md` | create | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U9 | `config/artifact_registry.json` (subject) + paired `tests/test_artifact_registry.py` | feat( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U10 | `workflows/pipeline_workflow.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U11 | `scripts/check_role_artifact.py` (subject) + paired `tests/test_check_role_artifact.py` | fix( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U12 | `scripts/graph_reconcile.py` (subject) + paired `tests/test_graph_reconcile.py` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U13 | `Makefile` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U14 | `docs/decisions/ADR-0016-test-database-isolation.md` | create | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U15 | `agents.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| U16 | `hooks/on_commit.py` (subject) + paired `tests/test_on_commit.py` | feat( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U17 | `agents/qa_agent.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| U18 | `agents/tester_agent.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |

### Wave 4 — Invocation coverage (`KI-048-1`)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U19 | `scripts/verify_references.py` (subject) + paired `tests/test_verify_references.py` | feat( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U20 | `config/invocation_exceptions.json` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |

### Wave 5 — Quality-audit scope

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U21 | `config/quality_audit_exclusions.json` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U22 | `scripts/quality_audit.py` (subject) + paired `tests/test_quality_audit.py` | feat( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 6 — Refactor to zero (`R`, one file per unit)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U23 | `hooks/on_commit.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U24 | `hooks/on_init.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U25 | `hooks/state_mirror.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U26 | `scripts/audit_cursor_era.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U27 | `scripts/branch_sovereignty.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U28 | `scripts/check_absolute_paths.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U29 | `scripts/check_forge_ladder.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U30 | `scripts/check_gate_log.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U31 | `scripts/check_model_tiers.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U32 | `scripts/check_task_scope.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U33 | `scripts/check_template_gates.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U34 | `scripts/ci_gate.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U35 | `scripts/cursor_adapter.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U36 | `scripts/detect_drift.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U37 | `scripts/detect_new_models.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U38 | `scripts/docs_freshness_check.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U39 | `scripts/install.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U40 | `scripts/merge_json.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U41 | `scripts/model_ledger.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U42 | `scripts/quality_audit.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U43 | `scripts/session_cost.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U44 | `scripts/session_probe.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U45 | `scripts/session_start.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U46 | `scripts/session_state.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U47 | `scripts/sync_agents_pin.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U48 | `scripts/verify_references.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U49 | `skills/compliance-checker/scripts/distill.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U50 | `skills/env-shielding-auditor/scripts/env_shielding_auditor.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U51 | `skills/js-standardizer/scripts/js_standardizer.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U52 | `skills/mass-standardizer/scripts/generate_manifest.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U53 | `skills/mass-standardizer/scripts/mass_standardizer.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U54 | `skills/omni-context-minimizer/scripts/omni_minimizer.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U55 | `skills/skillopt/scripts/dataloader.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U56 | `skills/skillopt/scripts/env.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U57 | `skills/skillopt/scripts/gemini_backend.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U58 | `skills/skillopt/scripts/train_runner.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U59 | `skills/topology-monitor/scripts/coverage_auditor.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U60 | `skills/topology-monitor/scripts/legacy_app_auditor.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U61 | `skills/topology-monitor/scripts/task_auditor.py` | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| U62 | `tests/test_artifact_registry.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U63 | `tests/test_ci_gate.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U64 | `tests/test_session_protocol.py` | R | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| K1..Kn | `skills/skill-creator/{scripts,eval-viewer}/*.py` whose provenance U21 cannot verify (contingency — up to 20 units in 11 files, `D2`; rows added to `task_scope.md` only if triggered) | R | native | `skill_architect` | N/A | `agents/skill_architect.md` |

### Wave 7 — Wiring and records

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U65 | `agents.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| U66 | `Makefile` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U67 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

---

## Tool-sufficiency check (this artifact's mechanical verification)

Every unit in this sprint is a `modify`, `create`, `fix(`, `feat(`, or `R`
(refactor) operation, requiring `Write` and `Edit` at minimum; every
`implementer_agent` and `skill_architect` unit that pairs a script/test change
additionally requires `Bash` to run the paired suite.

| Assignee | `tools:` (frontmatter) | Profile file exists at declared destination |
| :--- | :--- | :--- |
| `doc_orchestrator` | `Read, Glob, Grep, Write, Edit` | `agents/doc_orchestrator.md` — verified |
| `implementer_agent` | `Read, Glob, Grep, Write, Edit, Bash` | `agents/implementer_agent.md` — verified |
| `rule_validator` | `Read, Glob, Grep, Write, Edit` | `agents/rule_validator.md` — verified |
| `skill_architect` | `Read, Glob, Grep, Write, Edit, Bash, WebSearch, WebFetch` | `agents/skill_architect.md` — verified |

All four destinations are the nucleus `agents/` roster (this is a nucleus
session on `ai-sprint/052`; no host `.claude/agents/` or profile-path lookup
applies here). None hold `principal_agent` (`Read, Glob, Grep, TodoWrite` —
no `Write`/`Edit`, `F-051-R1`) and none hold `devops_agent` (`Read, Glob,
Grep, Bash` — no `Write`/`Edit` after `ADR-0009`); neither is a legal
assignee for any unit in this table, and neither was proposed by the plan.

---

## Assignee breakdown

| Assignee | Units | Count |
| :--- | :--- | :--- |
| `implementer_agent` | U2, U3, U4, U5, U9, U11, U12, U13, U16, U19, U21, U22, U23–U48, U62, U63, U64, U66 | 42 |
| `doc_orchestrator` | U1, U6, U7, U8, U10, U14, U67 | 7 |
| `rule_validator` | U15, U17, U18, U20, U65 | 5 |
| `skill_architect` | U49–U61, K1..Kn (1 contingency row) | 13 (+ contingency) |
| **Total** | U1–U67 + K1..Kn | **67** (+ up to 11 contingency files) |

---

## Disagreements with the plan

| Unit | Plan proposal | Recorded assignee | Reason |
| :--- | :--- | :--- | :--- |
| U20 | `implementer_agent` | `rule_validator` | `config/invocation_exceptions.json` is the `RA-16` invocation-exceptions registry, not framework-root `scripts/`, `hooks/`, or `tests/` — outside `implementer_agent`'s declared `write_scope` (`agents/implementer_agent.md`: "Holds `Write`/`Edit` for the framework-root `scripts/`, `hooks/`, and `tests/` trees"). This exact file, with the identical class of edit (adding typed residue entries), was assigned `rule_validator` in the three most recent sprints that touched it: `docs/sprints/047-core-pipeline/agent_assignment.md:96` (`U24`), `docs/sprints/049-core-pipeline/agent_assignment.md:67` (`U10`), and `docs/sprints/050-core-pipeline/agent_assignment.md:60` (`U4`, with a recorded disagreement of its own reasoning this exact point). `rule_validator`'s indexing/rule-auditing charter is the direct fit; `implementer_agent` has no grant over `config/`. |

Every other row (`U1`–`U19`, `U21`–`U67`, `K1..Kn`): the plan's
`Assignee (proposed)` stands unchanged. Two judgment calls recorded although
not overwrites:

- `U13`, `U66` (`Makefile`) → `implementer_agent` confirmed as a judgment
  call, not a literal `write_scope` match (`Makefile` is not `scripts/`,
  `hooks/`, or `tests/`): `devops_agent` is the closer subject-matter
  candidate but holds no `Write`/`Edit` for framework-root tooling after
  Sprint 033 (`ADR-0009`), and `implementer_agent` is the only profile
  holding both the grant and the code-authorship charter. Same judgment call
  recorded at `docs/sprints/050-core-pipeline/agent_assignment.md:144` (`U3`)
  and `docs/sprints/049-core-pipeline/agent_assignment.md:86` (`U12`).
- `U21` (`config/quality_audit_exclusions.json`, **create**) → `implementer_agent`
  confirmed and deliberately **not** aligned with the `U20` reasoning above:
  this file is a newly authored declaration consumed by the instrument built
  in the same wave (`U22` `scripts/quality_audit.py`), not an amendment to a
  pre-existing governance registry. Direct precedent:
  `docs/sprints/042-core-pipeline/agent_assignment.md:37` (`U2`,
  `config/template_gates.json`, created alongside
  `scripts/check_template_gates.py`) — "machine-read input to the script,
  not documentation. Its correctness is decided by the script that parses
  it." `config/invocation_exceptions.json` (`U20`) differs: it is an
  **existing** `RA-16` registry receiving compliance entries, which is
  `rule_validator`'s indexing charter, not a new instrument's declaration
  file.
- `U17`, `U18` (`agents/qa_agent.md`, `agents/tester_agent.md`) →
  `rule_validator` confirmed: these are governance-rule additions to an
  existing profile's ruleset (`D12` — "a profile rule is the only lever on
  the agent's output"), the same class of edit as `agents.md` itself
  (`U15`, `U65`). Most recent precedent for this exact class:
  `docs/sprints/048-core-pipeline/agent_assignment.md:50,52` (`U4`, `U7`,
  `rule_validator` editing `agents/implementer_agent.md` and
  `agents/rule_validator.md`). Earlier sprints (027, 028, 033–036) staffed
  agent-profile edits to `agent_orchestrator` itself; that older pattern is
  not followed here because `agent_orchestrator`'s restriction is staffing,
  not authoring rule content (`agents.md §6`: "Never evaluates code logic or
  tactical sequences. Exclusive jurisdiction is agent staffing"), and the
  more recent (048) precedent routes rule-content edits to `rule_validator`.

## Delegation note

`delegation_mode` is `native` (Claude Code can dispatch all eight core roles
plus the auxiliary roles used here). Units U1–U67 and the `K1..Kn`
contingency slot are executed under the named profile's ruleset once
Phase 6 (Execution) opens; `Mode` reads `native` on every row, matching
`docs/active_state.json` `delegation_mode` and the two most recent sprints
(`049`, `050`).
