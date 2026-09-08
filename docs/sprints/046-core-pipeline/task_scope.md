# Task Scope — Sprint 046 (nucleus-audit-mechanical-remediation)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Roadmap against
current `rules/`. `jurisdictional_lock` and `no_interference` are both applied by
reading this file.

Mode: **claude-code**, `delegation_mode: native`. Model/Effort from
`config/model_tiers.json` `tiers.author.claude_code` (`sonnet` / `medium`) for
every unit — all three assignees (`rule_validator`, `doc_orchestrator`,
`implementer_agent`) declare `tier: author`, none is in `tiers.gate.profiles`,
and no unit is mechanical-tier work. Every unit is a drafted-text edit (no new
logic, no new dependency). No `tier_escalation`.

Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/046-core-pipeline`

---

## Work

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U01 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 727fb24 |
| U02 | `agents.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 4ddddaa |
| U03 | `agents.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 28d6a11 |
| U04 | `agents.md` | modify | low | `rule_validator` | sonnet | medium | ✅ ef233ff |
| U05 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 4d97196 |
| U06 | `agents.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 509624a |
| U07 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 22c6010 |
| U08 | `rules/token_economy.md` | modify | low | `rule_validator` | sonnet | medium | ✅ d4ebef6 |
| U09 | `workflows/pipeline_workflow.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ 538c53d |
| U10 | `rules/LEGACY_RULE_CONCORDANCE.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 617300c |
| U11 | `docs/standards/templates/README_TEMPLATE.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ 30d3835 |
| U12 | `rules/frontend_modular_standard.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ 263614e |
| U13 | `rules/project_topology.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 6cc2eef |
| U14 | `workflows/remediation_workflow.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ 6e8c00e |
| U15 | `workflows/standardization_workflow.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ d790f8d |
| U16 | `workflows/skill_forge_workflow.md` | modify | low | `doc_orchestrator` | sonnet | medium | ✅ 56fc793 |
| U17 | `hooks/state_mirror.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ 56f86cb |
| U18 | `scripts/check_gate_log.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ 0e30517 |
| U19 | `hooks/on_commit.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ b74fba3 |
| U20 | `scripts/merge_json.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ 2b422c4 |
| U21 | `scripts/cursor_adapter.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ efc8406 |
| U22 | `scripts/audit_cursor_era.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ 08b07ce |
| U23 | `config/invocation_exceptions.json` | modify | low | `implementer_agent` | sonnet | medium | ✅ 1054b10 |
| U24 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ 807c5cf |
| U25 | `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 37d070d |
| U26 | `docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 351f5b2 |
| U27 | `docs/audits/NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md` | modify | low | `rule_validator` | sonnet | medium | ✅ 6dc9a8b |
| U28 | `docs/audits/NUCLEUS_MECHANISM_AUDIT_REPORT-045.md` | modify | low | `rule_validator` | sonnet | medium | ✅ f867f1d |
| U29 | `tests/test_state_mirror.py` | create | low | `implementer_agent` | sonnet | medium | ✅ 7bb3cdf |

Wave 1 = `U01`–`U07` (**strictly serial** — one shared target `agents.md`,
`no_interference`). Wave 2 = `U08`–`U16` (disjoint targets; starts after Wave 1
because `U08`/`U09`/`U10`/`U11` propagate `U04`/`U06`/`U07` under `RA-14`).
Wave 3 = `U17`–`U23` (disjoint; parallel-safe). Wave 4 = `U24`–`U28` (after
Waves 1–3; `U25`–`U28` disjoint among themselves). `U29` (`tests/test_state_mirror.py`)
was added at Phase 7 to close Gate 2 finding `T-046-1` — the sprint's one
behavioural change (`hooks/state_mirror.py`, `U17`) had no suite coverage.

---

## Rule audit

### Rules consulted

| Rule file | Bearing on this sprint |
| :--- | :--- |
| `rules/code_craft.md` | `U17`–`U23` touch Python. Edits are docstring / one-line stderr / JSON-entry only — type hints, ≤50-line functions and ≤3 indentation levels are unaffected; no `TODO`/`FIXME`; English only. |
| `rules/documentation_standard.md` | `U11`, `U12`, `U14`–`U16`, `U24` touch `docs/` / templates. `§4.1` metadata block required on `frontend_modular_standard.md` (`U12`). `docs_freshness` handled at close. |
| `rules/token_economy.md` | `U08` edits this file (path fix). Plan `## Cost` present; `audit_plan.py` exit 0. |
| `rules/skills_and_integrations.md` | `§1` ladder recorded in `skill_assignment.md`; no skill forged. `U16` edits `skill_forge_workflow.md` prose only. |
| `rules/qa_and_testing.md` | `§4` verdict vocabulary (`RA-17`) is the source for the `U24` stub comment and the Phase 7 gate rows. |
| `rules/loop_governance.md` | No `/loop` planned for Execution; if used for Phases 6–8, `loop_guard.py start` governs (named in the plan footer). |
| `rules/LEGACY_RULE_CONCORDANCE.md` | `U10` edits this file; `U01`/`U05`/`U12` must keep the `RA-04` / `RA-10` / `Rule 41` concordance rows resolvable. |

### `jurisdictional_lock` / `no_interference`

Every unit names exactly one physical file as its structural subject. The only
shared target is `agents.md` (`U01`–`U07`), resolved by strict serialisation in
Wave 1 — no two `agents.md` units are ever in progress at once. All other units
carry disjoint targets within their wave. No unit in this sprint appears in any
other in-progress `task_scope.md`.

### Missing rules

None. No new rule file is required — this sprint applies amendments drafted by
the Sprint 045 audit against existing rules and mechanisms.
