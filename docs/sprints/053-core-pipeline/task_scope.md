# Task Scope — Sprint 053 (core-pipeline)

Source: `docs/sprints/053-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`) and
`docs/sprints/053-core-pipeline/agent_assignment.md` (authoritative `Assignee`
— no overwrites recorded for this sprint, so File/Operation/Risk/Assignee below
transcribe the plan verbatim). Phase 4.3 of `workflows/pipeline_workflow.md`.
Table shape mandated by `scripts/check_task_scope.py` (the authority on shape,
not `docs/sprints/052-core-pipeline/task_scope.md`, consulted only as an
example of filled content).

## Model/Effort derivation (preamble, not invented)

`session_tool` is **`claude-code`**, not `cursor` (`docs/active_state.json`,
`delegation_mode: native`). Sprint id `53 >= 28`
(`scripts/check_task_scope.py:38 MODEL_FROM_SPRINT`), so Model/Effort are
mandatory on every row under this harness too — not only under
`session_tool: cursor`. Because the session tool is `claude_code`, the
`tier_transcription` obligation to run `make cursor-tiers` before writing
these columns does **not** apply here; that obligation is scoped to Cursor
sessions specifically. The binding source for this sprint is instead
`config/model_tiers.json`'s `claude_code` column, read directly — never
invented — by matching each assignee's profile name against the `profiles`
array of each tier bucket:

| Assignee (profile) | Tier bucket | `claude_code.model` | `claude_code.effort` |
| :--- | :--- | :--- | :--- |
| `implementer_agent` | `author` | `sonnet` | `medium` |
| `doc_orchestrator` | `author` | `sonnet` | `medium` |
| `rule_validator` | `author` | `sonnet` | `medium` |
| `skill_architect` | `author` | `sonnet` | `medium` |

All four profiles used as a `Work`-row `Assignee` in this sprint resolve to
the `author` tier bucket (`config/model_tiers.json` `tiers.author.profiles`),
so every row below carries `Model: sonnet`, `Effort: medium`. No `Work`-row
assignee this sprint is a `mechanical` profile (`devops_agent`,
`git_sync_agent`, `topology_mapper`) or a `gate` profile (`qa_agent`,
`tester_agent`, `principal_agent`) — confirmed against `agent_assignment.md`'s
Assignee breakdown table (`implementer_agent` 46, `doc_orchestrator` 3,
`rule_validator` 1, `skill_architect` 15 = 67), so the `MECHANICAL_PROFILES`
high-risk-escalation check (`scripts/check_task_scope.py
_mechanical_high_findings`) has no row to fire on.

## Same-file ordering (jurisdictional_lock, sequential claim)

Four files are claimed by two Work rows each — a Wave A `fix(` unit (subject
+ paired test) and a later Wave C `style(lint)` unit on the same subject file.
Per `agents.md §2 jurisdictional_lock`, this caps **concurrent** claim, not
lifetime touches: a later row may take the same subject once the earlier one
has landed. Each later row's Operation cell states the dependency explicitly,
transcribed from the plan (`D9`):

| Subject file | Earlier claim | Later claim |
| :--- | :--- | :--- |
| `scripts/session_state.py` | A1 (`fix(state)`) | C24 (`style(lint)`, "after A1") |
| `scripts/session_probe.py` | A2 (`fix(probe)`) | C23 (`style(lint)`, "after A2") |
| `hooks/on_commit.py` | A3 (`fix(hooks)`) | C04 (`style(lint)`, "after A3") |
| `tests/test_session_state.py` | A1 paired test | C54 (`style(lint)`, "after A1") |
| `tests/test_on_commit.py` | A3 paired test | C49 (`style(lint)`, "after A3") |

No other file is claimed by two Work rows across A1–D02 (verified by
comparing every `File` cell in the Work tables of `IMPLEMENTATION_PLAN.md`).

---

## Work

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `scripts/session_state.py` | modify — `fix(state)`: `SEALED_STATUSES` (legacy `"CLOSED"` accepted); `open_sprint` refusal names `release`; docstrings say `CLOSED_SUCCESSFULLY` (`D1`). Paired test: `tests/test_session_state.py` | medium | `implementer_agent` | sonnet | medium | ✅ `c90dcea` |
| A2 | `scripts/session_probe.py` | modify — `fix(probe)`: hygiene check compares against `SEALED_STATUSES` (`D1`). Paired test: `tests/test_session_probe.py` | low | `implementer_agent` | sonnet | medium | ✅ `41c8554` |
| A3 | `hooks/on_commit.py` | modify — `fix(hooks)`: deploy-unlock marker resolved through `scripts/_mode.py` at call time; blocked-push message names the mode's path (`D2`). Paired test: `tests/test_on_commit.py` | medium | `implementer_agent` | sonnet | medium | ✅ `954182c` |
| A4 | `workflows/deployment_workflow.md` | modify — `docs(deploy)`: `deploy_unlock` names both paths (nucleus `./.deploy_unlock`, host `.agents/.deploy_unlock`) | low | `doc_orchestrator` | sonnet | medium | ✅ `bdf64ca` |
| B1 | `requirements-quality.txt` | create — `build(deps)`: four pins (Dependencies table) (`D5`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| B2 | `requirements-core.txt` | modify — `build(deps)`: `-r requirements-quality.txt` (`D5`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| B3 | `scripts/quality_audit.py` | modify — `feat(quality)`: tree-sitter JS/TS scanner, fail closed (`D3`, `D4`); the Python path unchanged and stdlib-only | high | `implementer_agent` | sonnet | medium | ⏳ |
| B4 | `tests/test_quality_audit.py` | modify — `test(quality)`: the five Sprint 050 failure families, the fail-closed import path, `UNPARSED` on parse error, `.ts`/`.tsx` grammar selection, and threshold boundaries (50/51 lines, depth 3/4) | high | `implementer_agent` | sonnet | medium | ⏳ |
| B5 | `.github/workflows/ci.yml` | modify — `ci`: `pip install -q pytest -r requirements-quality.txt` | low | `implementer_agent` | sonnet | medium | ⏳ |
| C01 | `ruff.toml` | create — `build(lint)`: `required-version`, explicit `select`, `extend-exclude` = 10 vendored paths (`D6`, `D7`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| C02 | `tests/test_ruff_config.py` | create — `test(lint)`: `ruff.toml` `extend-exclude` equals the `config/quality_audit_exclusions.json` path set; `invoked_by:` docstring (`RA-16`) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C03 | `workflows/repository_hardening_workflow.md` | modify — `docs(harden)`: restore the Phase 4 ordering note (*before any history decision*) that the `S045-19` reshape dropped (`KI-047-5` second half) | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| C04 | `hooks/on_commit.py` | modify — `style(lint)`: clear 7 finding(s) — after A3 | low | `implementer_agent` | sonnet | medium | ⏳ |
| C05 | `hooks/on_commit_msg.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C06 | `hooks/telemetry.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C07 | `scripts/_mode.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C08 | `scripts/audit_cursor_era.py` | modify — `style(lint)`: clear 4 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C09 | `scripts/branch_sovereignty.py` | modify — `style(lint)`: clear 9 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C10 | `scripts/check_absolute_paths.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C11 | `scripts/check_forge_ladder.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C12 | `scripts/check_manifest_parity.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C13 | `scripts/check_model_tiers.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C14 | `scripts/check_task_scope.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C15 | `scripts/detect_drift.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C16 | `scripts/detect_new_models.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C17 | `scripts/docs_freshness_check.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C18 | `scripts/install.py` | modify — `style(lint)`: clear 4 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C19 | `scripts/loop_guard.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C20 | `scripts/model_ledger.py` | modify — `style(lint)`: clear 4 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C21 | `scripts/py_compile_tree.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C22 | `scripts/session_cost.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C23 | `scripts/session_probe.py` | modify — `style(lint)`: clear 8 finding(s) — after A2 | low | `implementer_agent` | sonnet | medium | ⏳ |
| C24 | `scripts/session_state.py` | modify — `style(lint)`: clear 4 finding(s) — after A1 | low | `implementer_agent` | sonnet | medium | ⏳ |
| C25 | `skills/compliance-checker/scripts/apply_rule_amendments.py` | modify — `style(lint)`: clear 2 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C26 | `skills/compliance-checker/scripts/distill.py` | modify — `style(lint)`: clear 4 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C27 | `skills/env-shielding-auditor/scripts/env_shielding_auditor.py` | modify — `style(lint)`: clear 4 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C28 | `skills/js-standardizer/scripts/js_standardizer.py` | modify — `style(lint)`: clear 7 finding(s) (includes `E722` bare `except: pass`, `D8`) | low | `skill_architect` | sonnet | medium | ⏳ |
| C29 | `skills/mass-standardizer/scripts/generate_manifest.py` | modify — `style(lint)`: clear 3 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C30 | `skills/mass-standardizer/scripts/mass_standardizer.py` | modify — `style(lint)`: clear 2 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C31 | `skills/omni-context-minimizer/scripts/omni_minimizer.py` | modify — `style(lint)`: clear 4 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C32 | `skills/python-quality-auditor/scripts/python_quality_auditor.py` | modify — `style(lint)`: clear 3 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C33 | `skills/skillopt/scripts/dataloader.py` | modify — `style(lint)`: clear 2 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C34 | `skills/skillopt/scripts/env.py` | modify — `style(lint)`: clear 7 finding(s) (includes `F821` on an annotation under `from __future__ import annotations`, cleared with a `TYPE_CHECKING` import) | low | `skill_architect` | sonnet | medium | ⏳ |
| C35 | `skills/skillopt/scripts/gemini_backend.py` | modify — `style(lint)`: clear 5 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C36 | `skills/skillopt/scripts/train_runner.py` | modify — `style(lint)`: clear 4 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C37 | `skills/slash-commander/__init__.py` | modify — `style(lint)`: clear 1 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C38 | `skills/slash-commander/scripts/__init__.py` | modify — `style(lint)`: clear 1 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C39 | `skills/topology-monitor/scripts/legacy_app_auditor.py` | modify — `style(lint)`: clear 3 finding(s) | low | `skill_architect` | sonnet | medium | ⏳ |
| C40 | `tests/test_artifact_registry.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C41 | `tests/test_audit_cursor_models.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C42 | `tests/test_check_forge_ladder.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C43 | `tests/test_ci_gate.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C44 | `tests/test_code_craft_gates.py` | modify — `style(lint)`: clear 3 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C45 | `tests/test_cursor_adapter.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C46 | `tests/test_docs_freshness_check.py` | modify — `style(lint)`: clear 3 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C47 | `tests/test_loop_guard.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C48 | `tests/test_mass_standardizer.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C49 | `tests/test_on_commit.py` | modify — `style(lint)`: clear 1 finding(s) — after A3 | low | `implementer_agent` | sonnet | medium | ⏳ |
| C50 | `tests/test_on_push.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C51 | `tests/test_root_resolution.py` | modify — `style(lint)`: clear 6 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C52 | `tests/test_session_protocol.py` | modify — `style(lint)`: clear 18 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C53 | `tests/test_session_start.py` | modify — `style(lint)`: clear 2 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C54 | `tests/test_session_state.py` | modify — `style(lint)`: clear 2 finding(s) — after A1 | low | `implementer_agent` | sonnet | medium | ⏳ |
| C55 | `tests/test_token_saver_auditor.py` | modify — `style(lint)`: clear 1 finding(s) | low | `implementer_agent` | sonnet | medium | ⏳ |
| C56 | `Makefile` | modify — `build(verify)`: `verify` runs `$(PY) -m ruff check .` and `$(PY) scripts/quality_audit.py .`; the comment at lines 19-22 (*"every other step is stdlib-only"*) restated (`D9`) | medium | `implementer_agent` | sonnet | medium | ⏳ |
| D01 | `agents.md` | modify — `docs(governance)`: `§1` Python `linter_command` → verified by `make verify`; JS/TS `linter_command`, `max_indentation`, `max_lines_per_func` → JS/TS instrument delivered (`D3`), prohibition clause kept and satisfied by a real lexer | medium | `rule_validator` | sonnet | medium | ⏳ |
| D02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — `docs(roadmap)`: Status bullet (054 merged into 053); `KI-050-6`, `KI-052-2`, `KI-052-9`, `KI-047-5`, `T3`/`T-046-2` marked delivered with commit citations; new rows for this sprint's routed findings | low | `doc_orchestrator` | sonnet | medium | ⏳ |

67 rows (A 4 · B 5 · C 56 · D 2), matching the plan's Cost section unit count.
