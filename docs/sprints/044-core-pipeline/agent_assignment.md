# Agent Assignment — Sprint 044 (session-start-drift-cigate-host-parity)

Source: `docs/sprints/044-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority.

Mode: **claude-code**, `delegation_mode: native` — the `Assignee` column names
which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

No unit in this sprint creates an agent profile → `Destination` is `N/A` on
every row.

---

## Staffing

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/session_start.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U2 | `tests/test_session_start.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U3 | `scripts/session_start.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U4 | `tests/test_session_protocol.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U5 | `scripts/ci_gate.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U6 | `tests/test_ci_gate.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U7 | `scripts/detect_drift.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U8 | `tests/test_detect_drift.py` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U9 | `Makefile` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U10 | `scripts/check_venv_relocatable.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U11 | `tests/test_check_venv_relocatable.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U12 | `docs/decisions/ADR-0014-ci-gate-record-on-uninspectable-protection.md` | create | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

## Disagreements with the plan

None. The plan's `Assignee (proposed)` column stands for all twelve units:

- U1–U11 are framework-root `scripts/`, `tests/` and the `Makefile` →
  `implementer_agent` holds `Write`/`Edit` on exactly those trees, including the
  framework-root `Makefile` (`ADR-0009`, Sprint 033; the same call recorded in
  `docs/sprints/042-core-pipeline/agent_assignment.md:69` for its `Makefile`
  unit). `devops_agent` retains `Bash` for environment routines, not authorship,
  and holds no `Write`/`Edit` on these trees.
- U12 is an ADR under `docs/decisions/` → `doc_orchestrator` (documentation and
  ADR authorship). `rules/documentation_standard.md §3` governs the supersede /
  metadata rules it must follow.
- Every docstring edit named in the plan's Documentary-impact table
  (`session_start.py`, `ci_gate.py`, `detect_drift.py`) rides inside its code
  unit's single-file commit — not a separate unit.

## Sequencing note (not a staffing disagreement)

`U1` and `U3` share `scripts/session_start.py`. `jurisdictional_lock` is one
physical file per commit, not one commit per file: `U1` lands and is committed
before `U3` opens the file. They MUST NOT be dispatched concurrently
(`no_interference` reads `task_scope.md`).
