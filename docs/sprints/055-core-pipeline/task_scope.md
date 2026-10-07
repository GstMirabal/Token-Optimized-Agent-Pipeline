# Task Scope — Sprint 055 (core-pipeline)

Source: `docs/sprints/055-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`, 19 units) and
`docs/sprints/055-core-pipeline/agent_assignment.md` (authoritative `Assignee`; it overrides
nothing in the plan). Phase 4.3 of `workflows/pipeline_workflow.md`. Table shape mandated by
`scripts/check_task_scope.py`.

## Model/Effort derivation (transcribed, not invented)

`session_tool` is `claude-code` (`docs/active_state.json`), so the `make cursor-tiers`
obligation does not apply. Sprint id `55 >= 28` (`scripts/check_task_scope.py:38`
`MODEL_FROM_SPRINT`), so Model/Effort are mandatory. Source: the `claude_code` column of
`config/model_tiers.json`, matched by profile name against `tiers.*.profiles`.

| Assignee (profile) | Tier bucket | Model | Effort |
| :--- | :--- | :--- | :--- |
| `implementer_agent`, `doc_orchestrator`, `rule_validator`, `skill_architect` | `author` | `sonnet` | `medium` |

No assignee is a `mechanical` profile (`MECHANICAL_PROFILES` high-risk check not triggered)
or a `gate` profile.

## Declared escalations

| Unit | Change | Basis |
| :--- | :--- | :--- |
| U02, U07, U13 | Effort `medium` -> `high` (model stays `sonnet`) | The three `high`-risk units: U02 is the secret-handling wrapper (Abort criterion 2 hangs on it), U07 changes the sandbox boundary every host inherits, U13 rewrites a constitutional rule. **Phase 4.3 proposal, not a `token_economy_agent` verdict** — `check_task_scope.py` enforces escalation only for mechanical profiles, so this is not script-required. Revert to `medium` if `token_economy_agent` declines. |

## Work

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U01 | `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` | create (transcribe human-reported matrix: command, exit, error signature per row; the human runs the commands in a `claude --settings claude/settings.hooks.json` session) | medium | `doc_orchestrator` | sonnet | medium | ✅ 27210b1 |
| U02 | `scripts/with_env.py` | create: `feat(` D2/D3 wrapper; companion `tests/test_with_env.py` (allowlist, exit `2` off-allowlist, redaction, missing `.env` explicit error, `invoked_by:` docstring) | high | `implementer_agent` | sonnet | high | ⏳ |
| U03 | `config/with_env_allowlist.json` | create (only `graphify`, D3) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U04 | `scripts/merge_json.py` | modify: `fix(` D4 targeted prune of retired template values; companion `tests/test_merge_json.py` | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U05 | `scripts/install.py` | modify: `fix(` D5 write probe, no traceback, host-form human command; companion `tests/test_install_permission.py` | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U06 | `scripts/session_start.py` | modify: `fix(` bridge advisory by mode; companion `tests/test_session_start.py` | low | `implementer_agent` | sonnet | medium | ⏳ |
| U07 | `claude/settings.hooks.json` | modify (`denyRead`/`allowRead` D4, wrapper in `excludedCommands` D2, forms from U01 per D7) | high | `implementer_agent` | sonnet | high | ⏳ |
| U08 | `Makefile` | modify: `fix(` D9 `-m graphify` in `graphify-update`, new `graphify-deep` via `with_env.py`; companion `tests/test_makefile_graphify.py` | low | `implementer_agent` | sonnet | medium | ⏳ |
| U09 | `rules/project_topology.md` | modify (sandbox table, D8) | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| U10 | `rules/qa_and_testing.md` | modify (browser verification under sandbox, branch A or B, D6) | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| U11 | `rules/graphify.md` | modify (key via `with_env.py`, `S-4`, measured 7-key list; carries the correction the omitted U12 would have made) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U12 | `skills/graphify/SKILL.md` | OMITTED: judged vendored upstream material (`skill_assignment.md` §6; `rules/skills_and_integrations.md §3`); no file is touched, see note 1 below | low | `skill_architect` | sonnet | medium | ⏳ omitted |
| U13 | `agents.md` | modify (`RA-09` and `§3 secret_sovereignty` name `with_env.py` as the sanctioned path, D2) | high | `rule_validator` | sonnet | high | ⏳ |
| U14 | `workflows/pipeline_workflow.md` | modify (Phase 2 row: "export `.env`" -> `with_env.py`) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U15 | `workflows/deployment_workflow.md` | modify (unsandboxed steps reference the U09 table, `S-5`) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U16 | `workflows/repository_hardening_workflow.md` | modify (`gh` calls reference the U09 table, `S-5`) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U17 | `rules/LEGACY_RULE_CONCORDANCE.md` | modify (`Rule 66` row follows new `RA-09` text, `RA-14`) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U18 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify (close `F-115-N2`, row -> SHA, reproduced in U01) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U19 | `CHANGELOG.md` | modify (`[Unreleased]` entry naming each commit by short SHA) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U20 | `agents/devops_agent.md` | modify (`secret_sovereignty` row and `.env` export wording point to `scripts/with_env.py`; RA-14 propagation of U13) | low | `agent_orchestrator` | sonnet | medium | ⏳ |

Note 1 (U12): `check_task_scope.py` reads only `File`, `Operation`, `Risk`, `Assignee`,
`Model`, `Effort`; it does not parse `Status`, so the row is kept with an Operation that
carries no mutating verb. The omission must be recorded in `SPRINT_LOG.md` (plan row U12).
If the human rules the file native, the row reverts to `modify` and the key list at
`skills/graphify/SKILL.md:238` is corrected there as well.

## Ordering constraints (transcribed from the plan, plus audit additions)

| Constraint | Why |
| :--- | :--- |
| U01 committed before U02..U19 start | `D1`: no correction before measurement |
| U02 -> U03 -> U08 consecutive (audit addition) | `RA-16`: the declared invoker of `with_env.py` (`Makefile` `graphify-deep`) lands right after the script and its allowlist |
| U07 after U01, U02, U03 | Needs measured forms (`D7`) and the wrapper path it excludes |
| U09 before U15, U16 | They reference the table U09 creates (`D8`) |
| U13 before U14, U17 | `RA-14`: the rewritten `RA-09` text is the source the pointers follow |
| U18, U19 last | Cite SHAs of the units they close |

## Same-subject check (`no_interference`)

All 18 live rows name distinct structural subjects; no file appears twice, so no same-subject
sequence exists and no two rows can collide. U12 is omitted and claims nothing. Companion
test files are mandatory companions of their `fix(`/`feat(` subject, not subjects
(`jurisdictional_lock`).

## Rule-audit findings

| # | Finding | Severity | Action |
| :--- | :--- | :--- | :--- |
| F1 | `jurisdictional_lock` / `no_interference`: no violation. One subject per row, no repeated file | none | None |
| F2 | `code_craft.md §6`: the four `fix(` units (U04, U05, U06, U08) each name a paired test in Operation. `tests/test_install_permission.py` and `tests/test_makefile_graphify.py` are new files; `tests/test_merge_json.py` and `tests/test_session_start.py` are modified. U02 is `feat(` and its test is carried anyway | none | Each `fix(` commit must stage its test in the same commit; per Sprint 054 A02/A03, a `Repro:` trailer is mandatory on every `fix(` |
| F3 | `RA-14`, U13 reach. The plan's cited targets: `agents.md §3 secret_sovereignty` covered by U13; `rules/LEGACY_RULE_CONCORDANCE.md` Rule 66 covered by U17; `workflows/pipeline_workflow.md` Phase 2 (line 16) covered by U14; **`rules/qa_and_testing.md:87` is covered by U10 only incidentally**: line 87 merely cites the name `RA-09 SECRET_SOVEREIGNTY` and needs no rewrite unless the name changes | low | U10 must re-read lines 85-87 and leave them if the name is unchanged; the `.env`/`.env.example` wording at line 85 must agree with the U07 `denyRead`/`allowRead` change (D4) |
| F4 | **Gap: `agents/devops_agent.md:16` and `:20`** restate `RA-09` ("Must strictly use environment export commands", "`.env` export") and no unit touches them. After U13/U14 the profile still prescribes the export mechanism the sprint declares blocked (`S-3`). Same class as the `RA-14` precedent | medium | Add a unit (proposed `U20`, `agents/devops_agent.md`, `modify`, `agent_orchestrator`/`doc_orchestrator`, low) or record the exclusion in `SPRINT_LOG.md`. Not added here: the plan is the authority on Work rows and `agent_assignment.md` has no assignee for it |
| F5 | **Stale text in U17's target**: Rule 66 says "`§3 secret_sovereignty` is a pointer to `RA-09` since Sprint 046", while `agents.md §3` currently calls `RA-09` "canonical" and says `secret_sovereignty` "adds the Makefile / subshell mechanism" in the pointer direction. U13 and U17 must agree on one direction | low | U13 and U17 are consecutive in effect; U17 copies whatever `§3` and `RA-09` finally say. Verify with `grep -n 'secret_sovereignty\|RA-09' agents.md rules/LEGACY_RULE_CONCORDANCE.md` after both land |
| F6 | `§1 path_type` (relative only): `with_env.py --allowlist <path>` (D3) and the allowlist `command` entries must be stored and documented relative (`venv_skillopt/bin/python -m graphify`); no absolute host path in U03, U07 or U09 | low | Add as a QA check on U02/U03/U07/U09 |
| F7 | `§1 ephemeral markers`: the plan contains no `TODO`/`FIXME`. Units that write code (U02, U04, U05, U06) and prose must not introduce them | none | QA grep at Gate 1 |
| F8 | `§1 code_logic` language: the plan's Spanish is permitted only there (`user_chat`). U01, U09-U11, U13-U19 and all code, tests and commits MUST be English. Plan strings such as "a documentar" must not be copied into rules | low | Instruct `doc_orchestrator` and `rule_validator` at dispatch |
| F9 | `RA-16`: `with_env.py` declares invokers in the plan's Mechanisms table, but the first live invoker (`Makefile graphify-deep`, U08) is three rows after the script. Without the ordering constraint above, a commit could land the script with no invoker | low | Ordering constraint U02 -> U03 -> U08 added above; `invoked_by:` docstring is required by U02 |
| F10 | U07 `high` risk: the template change reaches every host through `install.py` re-merge. U04's prune only removes values on an explicit retired list | medium | U07 must not start before U04 lands (add to the QA checklist; the plan order `U04..U08` already implies it) |
| F11 | U03 has no companion test of its own | low | Acceptable: `tests/test_with_env.py` (U02) loads the real allowlist; U02's test must assert the shipped file parses and contains `graphify` only |
| F12 | `tier_transcription`: no Cursor tiers apply (`session_tool: claude-code`). Effort `high` on U02/U07/U13 is a Phase 4.3 proposal, declared above, not a `token_economy_agent` verdict | none | Revert to `medium` if declined |
| F13 | U01 is human-dependent (`T10 unverified`, Abort criterion 1). `doc_orchestrator` only transcribes; a row with no human-reported evidence must not be marked measured | medium | Phase 6 must not dispatch U02..U19 until the human has supplied the matrix |
