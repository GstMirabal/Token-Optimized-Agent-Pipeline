# Agent Assignment — Sprint 053 (core-pipeline)

Source: `docs/sprints/053-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work
row is not closed until it appears here.

Mode: **claude-code** (nucleus), `delegation_mode: native` — the `Assignee`
column names which profile's ruleset governs each write. This artifact does
not carry Model/Effort/tier columns — those are `token_economy_agent` →
`rule_validator` territory, transcribed into `task_scope.md` at Phase 4.3
(`agents.md §6 agent_orchestrator` `no_model_columns`).

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`, Phase 4.3) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

**No unit in this sprint creates a new agent profile.** Every A1–A4, B1–B5,
C01–C56 and D01–D02 assigns an existing core or auxiliary role
(`doc_orchestrator`, `implementer_agent`, `rule_validator`, `skill_architect`).
`Destination` is therefore `N/A` on every row. Confirmed against
`scripts/check_forge_ladder.py`: no row's Operation is `create` on a Target
matching `agents/*.md`, and no row's Destination is a forge destination
(`host:.claude/agents/`, `nucleus:PR`, or `profile:`).

## Root-level build/config files

`requirements-quality.txt` (B1), `requirements-core.txt` (B2),
`.github/workflows/ci.yml` (B5), `ruff.toml` (C01) and `Makefile` (C56) sit
outside every profile's *literal* write-scope text:

- `implementer_agent`'s `write_scope` names the framework-root `scripts/`,
  `hooks/`, and `tests/` **trees** (`agents/implementer_agent.md`), not
  root-level dependency/lint/CI manifests.
- `skill_architect` owns `skills/[name]/scripts/` only (`agents.md §3
  topological_order`) — none of these five files sit there.
- `doc_orchestrator`'s `language_guard` scopes it to "technical
  documentation" content, not build/dependency/CI configuration.
- `devops_agent` is the closest subject-matter label ("Environment Agent...
  manages venv") but its Jurisdiction row states plainly it "does **not**
  hold `Write`/`Edit`" since Sprint 033 (`ADR-0009`); its `tools:` frontmatter
  is `Read, Glob, Grep, Bash` only. It cannot author these files under the
  Edit/Write discipline agent-identity assignment requires, however close the
  domain label reads.

By elimination, `implementer_agent` is the only profile holding both a
`Write`/`Edit` grant and a code-authorship charter, and each of these five
files is build/lint/dependency/CI tooling that exists to gate or supply the
same `scripts/`/`tests/` trees this profile already authors: `Makefile`'s
`verify` target runs `ruff check .` and `scripts/quality_audit.py` over
`scripts/`/`hooks/`/`tests/` (C56); `ruff.toml` configures that same lint pass
(C01); `requirements-quality.txt`/`requirements-core.txt` supply the
dependencies `scripts/quality_audit.py` needs to parse JS/TS (B1, B2); and
`.github/workflows/ci.yml` installs those same dependencies to run `pytest`
against `tests/` (B5). This is a **judgment call, not a literal `write_scope`
match** — the identical call, on the identical file class, was recorded at
`docs/sprints/052-core-pipeline/agent_assignment.md` (`U13`, `U66`,
`Makefile`), `docs/sprints/050-core-pipeline/agent_assignment.md` (`U3`), and
`docs/sprints/049-core-pipeline/agent_assignment.md` (`U12`).

**No new agent profile is created for this file class.** Five root-level
config files in one sprint, each already covered by an existing profile's
tool grant and authorship charter, do not meet `agent_creation`'s "step lacks
a suitable profile" bar (`agents.md §6 agent_orchestrator`).

---

## Staffing

Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave A — seal vocabulary and deploy-unlock (`KI-052-2`, `KI-052-9`)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `scripts/session_state.py` (subject) + paired `tests/test_session_state.py` | fix( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A2 | `scripts/session_probe.py` (subject) + paired `tests/test_session_probe.py` | fix( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A3 | `hooks/on_commit.py` (subject) + paired `tests/test_on_commit.py` | fix( | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| A4 | `workflows/deployment_workflow.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave B — JS/TS complexity instrument (`KI-050-6`)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `requirements-quality.txt` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B2 | `requirements-core.txt` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B3 | `scripts/quality_audit.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B4 | `tests/test_quality_audit.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| B5 | `.github/workflows/ci.yml` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave C — ruff to exit `0` and into `make verify` (former Sprint 054)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C01 | `ruff.toml` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C02 | `tests/test_ruff_config.py` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C03 | `workflows/repository_hardening_workflow.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| C04 | `hooks/on_commit.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C05 | `hooks/on_commit_msg.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C06 | `hooks/telemetry.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C07 | `scripts/_mode.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C08 | `scripts/audit_cursor_era.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C09 | `scripts/branch_sovereignty.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C10 | `scripts/check_absolute_paths.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C11 | `scripts/check_forge_ladder.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C12 | `scripts/check_manifest_parity.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C13 | `scripts/check_model_tiers.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C14 | `scripts/check_task_scope.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C15 | `scripts/detect_drift.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C16 | `scripts/detect_new_models.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C17 | `scripts/docs_freshness_check.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C18 | `scripts/install.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C19 | `scripts/loop_guard.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C20 | `scripts/model_ledger.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C21 | `scripts/py_compile_tree.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C22 | `scripts/session_cost.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C23 | `scripts/session_probe.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C24 | `scripts/session_state.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C25 | `skills/compliance-checker/scripts/apply_rule_amendments.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C26 | `skills/compliance-checker/scripts/distill.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C27 | `skills/env-shielding-auditor/scripts/env_shielding_auditor.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C28 | `skills/js-standardizer/scripts/js_standardizer.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C29 | `skills/mass-standardizer/scripts/generate_manifest.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C30 | `skills/mass-standardizer/scripts/mass_standardizer.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C31 | `skills/omni-context-minimizer/scripts/omni_minimizer.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C32 | `skills/python-quality-auditor/scripts/python_quality_auditor.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C33 | `skills/skillopt/scripts/dataloader.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C34 | `skills/skillopt/scripts/env.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C35 | `skills/skillopt/scripts/gemini_backend.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C36 | `skills/skillopt/scripts/train_runner.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C37 | `skills/slash-commander/__init__.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C38 | `skills/slash-commander/scripts/__init__.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C39 | `skills/topology-monitor/scripts/legacy_app_auditor.py` | style(lint) | native | `skill_architect` | N/A | `agents/skill_architect.md` |
| C40 | `tests/test_artifact_registry.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C41 | `tests/test_audit_cursor_models.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C42 | `tests/test_check_forge_ladder.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C43 | `tests/test_ci_gate.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C44 | `tests/test_code_craft_gates.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C45 | `tests/test_cursor_adapter.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C46 | `tests/test_docs_freshness_check.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C47 | `tests/test_loop_guard.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C48 | `tests/test_mass_standardizer.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C49 | `tests/test_on_commit.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C50 | `tests/test_on_push.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C51 | `tests/test_root_resolution.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C52 | `tests/test_session_protocol.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C53 | `tests/test_session_start.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C54 | `tests/test_session_state.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C55 | `tests/test_token_saver_auditor.py` | style(lint) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| C56 | `Makefile` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave D — governance and records

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D01 | `agents.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| D02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

---

## Tool-sufficiency check (this artifact's mechanical verification)

| Assignee | `tools:` (frontmatter) | Profile file exists at declared destination |
| :--- | :--- | :--- |
| `doc_orchestrator` | `Read, Glob, Grep, Write, Edit` | `agents/doc_orchestrator.md` — verified |
| `implementer_agent` | `Read, Glob, Grep, Write, Edit, Bash` | `agents/implementer_agent.md` — verified |
| `rule_validator` | `Read, Glob, Grep, Write, Edit` | `agents/rule_validator.md` — verified |
| `skill_architect` | `Read, Glob, Grep, Write, Edit, Bash, WebSearch, WebFetch` | `agents/skill_architect.md` — verified |

All four destinations are the nucleus `agents/` roster (nucleus session on
`ai-sprint/053`; no host `.claude/agents/` or profile-path lookup applies).
Neither `principal_agent` (`Read, Glob, Grep, TodoWrite` — no `Write`/`Edit`)
nor `devops_agent` (`Read, Glob, Grep, Bash` — no `Write`/`Edit` after
`ADR-0009`) is a legal assignee for any unit in this table, and neither was
proposed by the plan.

## Assignee breakdown

| Assignee | Units | Count |
| :--- | :--- | :--- |
| `implementer_agent` | A1, A2, A3, B1, B2, B3, B4, B5, C01, C02, C04–C24, C40–C56 | 46 |
| `doc_orchestrator` | A4, C03, D02 | 3 |
| `rule_validator` | D01 | 1 |
| `skill_architect` | C25–C39 | 15 |
| **Total** | A1–A4, B1–B5, C01–C56, D01–D02 | **67** |

---

## Disagreements with the plan

None. Every row's `Assignee` stands exactly as the plan's `Assignee
(proposed)` column names it (A1–A4, B1–B5, C01–C56, D01–D02) — no overwrite
was warranted; the plan's own proposals already route framework-root
`scripts/`/`hooks/`/`tests/` to `implementer_agent` (`ADR-0009`), `skills/`
scripts to `skill_architect`, governance-rule content in `agents.md` to
`rule_validator`, and workflow/roadmap prose to `doc_orchestrator`.

Judgment calls recorded although not overwrites (`agents.md §6
agent_orchestrator staffing_injection`: "the proposal is input, not a lock"
— here it is confirmed, not relocked elsewhere):

- **B1, B2, B5, C01, C56** (`requirements-quality.txt`, `requirements-core.txt`,
  `.github/workflows/ci.yml`, `ruff.toml`, `Makefile`) → `implementer_agent`
  confirmed as a judgment call, not a literal `write_scope` match. See
  "Root-level build/config files" above for the full reasoning and the
  Sprint 052/050/049 precedents for the same call.

## Delegation note

`delegation_mode` is `native` (Claude Code can dispatch all eight core roles
plus the auxiliary roles used here). Every unit executes under the named
profile's ruleset once Phase 6 (Execution) opens; `Mode` reads `native` on
every row, matching `docs/active_state.json` `delegation_mode`.
