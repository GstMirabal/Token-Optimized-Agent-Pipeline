# Task Scope — Sprint 054 (core-pipeline)

Source: `docs/sprints/054-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`, 31 units) and
`docs/sprints/054-core-pipeline/agent_assignment.md` (authoritative `Assignee`; its one
override is C04 `orchestrator` -> `implementer_agent`, because the unit is a script run
and `orchestrator` holds no `Bash`). Phase 4.3 of
`workflows/pipeline_workflow.md`. Table shape mandated by `scripts/check_task_scope.py`.

## Model/Effort derivation (transcribed, not invented)

`session_tool` is `claude-code` (`docs/active_state.json`), so the `make cursor-tiers`
obligation does not apply. Sprint id `54 >= 28` (`scripts/check_task_scope.py:38`
`MODEL_FROM_SPRINT`), so Model/Effort are mandatory. Source: the `claude_code` column of
`config/model_tiers.json`, matched by profile name against `tiers.*.profiles`.

| Assignee (profile) | Tier bucket | Model | Effort |
| :--- | :--- | :--- | :--- |
| `implementer_agent`, `doc_orchestrator`, `orchestrator`, `rule_validator`, `skill_architect`, `agent_orchestrator` | `author` | `sonnet` | `medium` |

No assignee is a `mechanical` profile (`MECHANICAL_PROFILES` high-risk check not triggered)
or a `gate` profile.

## Declared escalations

| Unit | Change | Basis |
| :--- | :--- | :--- |
| A03 | Effort `medium` -> `high` (model stays `sonnet`) | Only `high`-risk unit in the sprint; Abort criterion 1 hangs on it. **Phase 4.3 proposal, not a `token_economy_agent` verdict** — `check_task_scope.py` enforces escalation only for mechanical profiles, so this is not script-required. Revert to `medium` if `token_economy_agent` declines. |

## Work

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W01 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify (Sprint 054 intake section, RA-15 genericized) | low | `doc_orchestrator` | sonnet | medium | ✅ `225aaee` |
| W02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify (route blocks D and E) | low | `doc_orchestrator` | sonnet | medium | ✅ `903b04e` |
| A01 | `scripts/quality_audit.py` | modify: `fix(` D1; companion `tests/test_quality_audit.py` | medium | `implementer_agent` | sonnet | medium | ✅ `46d07cf` |
| A02 | `hooks/on_commit.py` | modify: `feat(` D2 trailer; companion `tests/test_on_commit.py` | medium | `implementer_agent` | sonnet | medium | ✅ `8f13941` |
| A03 | `scripts/check_fix_reproduces.py` | create: D2 gate half, D3, D4; companion `tests/test_check_fix_reproduces.py` | high | `implementer_agent` | sonnet | high | ✅ `0747911` |
| A04 | `agents/qa_agent.md` | modify (Gate 1 first check) | low | `agent_orchestrator` | sonnet | medium | ✅ `cd225c4` |
| A05 | `rules/qa_and_testing.md` | modify (§4 label, instructing finding) | medium | `rule_validator` | sonnet | medium | ✅ `12769c6` |
| A06 | `rules/code_craft.md` | modify (§6 names enforcement) | low | `rule_validator` | sonnet | medium | ✅ `9d2c1ef` |
| A07 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify (D6 columns) | low | `doc_orchestrator` | sonnet | medium | ✅ `7fb1572` |
| A08 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify: `feat(` D6/D7; companion `tests/test_token_saver_auditor.py` | medium | `skill_architect` | sonnet | medium | ✅ `b6b554e` |
| A09 | `workflows/pipeline_workflow.md` | modify (Phase 5 dry run, Phase 7 replay) | medium | `orchestrator` | sonnet | medium | ✅ `38548e4` |
| A10 | `docs/standards/templates/NOTICE_TEMPLATE.md` | create (D8) | low | `doc_orchestrator` | sonnet | medium | ✅ `4ec95bd` |
| A11 | `workflows/close_workflow.md` | modify (`repo_docs_check` conditional NOTICE) | low | `orchestrator` | sonnet | medium | ✅ `ff3a904` |
| A12 | `workflows/standardization_workflow.md` | modify (census names NOTICE_TEMPLATE) | low | `orchestrator` | sonnet | medium | ✅ `737cea6` |
| A13 | `config/template_gates.json` | modify (`exceptions` entry for `NOTICE_TEMPLATE.md`; lands right after A10) | low | `orchestrator` | sonnet | medium | ✅ `2f22aea` |
| A14 | `README.md` | modify (script count 41→42, mandatory companion of A03: `check_readme_counts.py` in `make verify`; unplanned, recorded at `SPRINT_LOG.md` frictions; QA Gate 1 round 1 F8) | low | `doc_orchestrator` | sonnet | medium | ✅ `bcdb4ac` |
| B01 | `scripts/session_state.py` | modify: `fix(` D9; companions `tests/test_session_state.py` and `tests/test_session_probe.py` | medium | `implementer_agent` | sonnet | medium | ✅ `23b8b48` |
| B02 | `scripts/session_state.py` | modify: `fix(` D10; companion `tests/test_session_state.py` | medium | `implementer_agent` | sonnet | medium | ✅ `d86f521` |
| B03 | `scripts/session_state.py` | modify: `fix(` D11; companion `tests/test_session_state.py` | low | `implementer_agent` | sonnet | medium | ✅ `09642e9` |
| B04 | `scripts/install_lock.py` | create (D12); companion `tests/test_install_lock.py` | medium | `implementer_agent` | sonnet | medium | ✅ `3b012d4` |
| B05 | `scripts/session_start.py` | modify: `feat(` boot advisory; companion `tests/test_session_start.py` | low | `implementer_agent` | sonnet | medium | ✅ `b2a42ef` |
| B06 | `commands/start.md` | modify (D11 both forms) | low | `orchestrator` | sonnet | medium | ✅ `f16bdd4` |
| B07 | `workflows/start_workflow.md` | modify (step 1 forms, pip_setup lock) | low | `orchestrator` | sonnet | medium | ✅ `cac68ec` |
| B08 | `workflows/pipeline_workflow.md` | modify (Phase 3 open-sprint cell) | low | `orchestrator` | sonnet | medium | ✅ `590fb6a` |
| C01 | `agents.md` | modify (§8 rows, RA-10 pointer) | medium | `rule_validator` | sonnet | medium | ✅ `d01045b` |
| C02 | `rules/code_craft.md` | modify (line 37 key spelling) | low | `rule_validator` | sonnet | medium | ✅ `c9f9c79` |
| C03 | `README.md` | modify (line 92 key spelling, matches C01) | low | `doc_orchestrator` | sonnet | medium | ✅ `f0e829d` |
| C04 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | modify (regenerate via `scripts/map_workflows.py`, never hand-edited; after A09, A11, A12, B07, B08) | low | `implementer_agent` | sonnet | medium | ✅ `dde2088` |
| Z01 | `docs/sprints/054-core-pipeline/PHASE_REGISTER.md` | create | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| Z02 | `CHANGELOG.md` | modify (`[Unreleased]` entry, SHA per commit) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| Z03 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify (tick delivered entries) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| Z04 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify (mark Sprint 054 delivered) | low | `doc_orchestrator` | sonnet | medium | ⏳ |

## Ordering constraints (transcribed from the plan's table)

| Constraint | Why |
| :--- | :--- |
| A07 before A08 | Template passes the check that consumes it |
| A03 -> A04, B04 -> B05 -> B07 consecutive | Declared invoker lands right after its script (`RA-16`) |
| A10 -> A13 consecutive | Template must be in `render` or `exceptions` |
| C01 before C03 | `RA-14` propagation of the `§8` key spelling |
| C04 after A09, A11, A12, B07, B08 | Generated step map reads the final workflow text |
| Every `fix(` after A02 (B01, B02, B03) carries a `Repro:` trailer | A02 makes it mandatory; A01 precedes it |

## Same-subject sequences (`no_interference`)

Never concurrent; each later unit starts only after the earlier one has landed.

| Subject | Units, in order |
| :--- | :--- |
| `scripts/session_state.py` (+ companions `tests/test_session_state.py`, `tests/test_session_probe.py`) | B01 -> B02 -> B03 |
| `workflows/pipeline_workflow.md` | A09 -> B08 |
| `rules/code_craft.md` | A06 -> C02 |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | W01 -> Z03 |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | W02 -> Z04 |
