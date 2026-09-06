# Task Scope — Sprint 043 (submodule-runtime-parity)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Roadmap against
current `rules/`. `jurisdictional_lock` and `no_interference` are both applied by
reading this file.

Mode: **claude-code**, `delegation_mode: native`. Model/Effort from
`config/model_tiers.json` `tiers.author.claude_code` (all six assignees are
`author`-tier profiles) — `sonnet` / `medium`.

Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/043-core-pipeline`

---

## Work

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `workflows/start_workflow.md` | modify | medium | `orchestrator` | sonnet | medium | ⏳ |
| A2 | `rules/graphify.md` | modify | low | `rule_validator` | sonnet | medium | ⏳ |
| D1 | `scripts/check_venv_relocatable.py` | create | medium | `implementer_agent` | sonnet | medium | ⏳ |
| D2 | `tests/test_venv_relocatable.py` | create | low | `implementer_agent` | sonnet | medium | ⏳ |
| C1 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ⏳ |
| C2 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify | low | `doc_orchestrator` | sonnet | medium | ⏳ |

---

## Rule audit

| Rule | Unit(s) | Finding |
| :--- | :--- | :--- |
| `agents.md §2 jurisdictional_lock` | all | One physical file per unit. No file listed twice. PASS. |
| `agents.md §2 no_interference` | all | No file in this table is claimed by another in-progress subtask. PASS. |
| `RA-16 INVOCATION_COVERAGE` | D1 | `check_venv_relocatable.py` docstring MUST carry `invoked_by: workflows/start_workflow.md#pip_setup`; A1 MUST name the script in `pip_setup`. `verify_references.py` check (d) resolves it. Enforced in Verification. |
| `agents.md §1` (Python) | D1 | `snake_case`, mandatory type hints, ≤ 50 lines/func, ≤ 3 indent levels, Google-style docstring, no `TODO`/`FIXME`, English only, relative paths only. |
| `agents.md §1` (linter) | D1, D2 | `ruff check .` exit 0 on the new files (repo-wide ruff is a known migration exclusion; the two new files must be clean). |
| `RA-14 PATCH_PROPAGATION` | C1 | Before closing C1, `grep -n` the full `agents.md` for `feedback_upstream`, `strict_rule`, `jurisdiction`, `three-tier`/`tres niveles` and reconcile every hit with the new canonical §4 block. |
| `agents.md §3 nucleus_neutrality` | all | Nucleus session: no automatic structural scaffolding. Only the six named files are touched. PASS. |
| `agents.md §0` (step map) | A1 | `pip_setup` / `read_graph` step **keys** unchanged → `WORKFLOWS_STEP_MAP_GUIDE.md` regen is expected no-op; `make verify` confirms in Phase 8. |
| `rules/documentation_standard.md §4.1` | A1, A2, C1, C2 | Stamp/refresh the metadata block on every doc touched where the doc type carries one. |
| `ADR-0009` | D1, D2 | `scripts/` and `tests/` are `implementer_agent`'s exclusive authorship. PASS. |

## Capability check

Every assignee holds `Write`/`Edit` (`orchestrator`, `rule_validator`,
`doc_orchestrator`, `implementer_agent`) → each can perform its `create`/`modify`
operation. No mechanical-tier row. `check_task_scope.py` shape:
`# | File | Operation | Risk | Assignee | Model | Effort | Status` — present.

## Out of scope (from the plan, restated for the auditor)

Sandbox auto-retry override, the `§6`/`§2` concurrency contradiction (ADR-0001),
`install.sh` venv relocation, skillopt heavy-stack automation, parallel fan-out.
