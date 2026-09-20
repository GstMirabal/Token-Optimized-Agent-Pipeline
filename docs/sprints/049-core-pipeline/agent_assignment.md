# Agent Assignment — Sprint 049 (cursor-bridge-100)

Source: `docs/sprints/049-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

**No unit in this sprint creates an agent profile.** Every `Destination` cell is
`N/A` for that reason, not for want of a decision.

---

## Staffing

One table per wave. Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave 1 — `F-049-1` profile parity under Cursor

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/cursor_adapter.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U2 | `scripts/install.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U3 | `profiles/example-project/rule_triggers.json` | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 2 — `F-049-2` mirror integrity

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U4 | `scripts/bridge_state.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U12 | `Makefile` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 3 — `F-049-3` census window

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U5 | `scripts/audit_cursor_era.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U6 | `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 4 — `F-049-4` and `F-049-5` gates and proof

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U7 | `scripts/audit_cursor_models.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U8 | `tests/test_cursor_phase1.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 5 — `F-049-6` / `F-049-7` governance record (no instrument is built here)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ~~U9~~ | ~~`Makefile`~~ | **WITHDRAWN** at the Phase 5 pre-approval audit (`F-049-7`) | — | — | — | — |
| U10 | `config/invocation_exceptions.json` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| U11 | `agents.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |

---

## Ordering constraints carried from the plan

| Constraint | Reason |
| :--- | :--- |
| U1 lands before U2 | U2 calls the signature U1 introduces on `install_cursor_bridge` |
| U5 lands before U6 | U6 is the regenerated output of the generator U5 changes; hand-editing it is prohibited by its own header |
| U10 and U11 keep the literal skill-path strings | `U10` no longer withdraws the `model-invoked` exceptions — it corrects their notes. `RA-16` safety rests on `agents.md` retaining the strings `python-quality-auditor` and `js-standardizer`, because `verify_references.py check_invocation_coverage` excludes the `Makefile` from its corpus |

---

## Disagreements with the plan

| Unit | Plan proposal | Recorded assignee | Reason |
| :--- | :--- | :--- | :--- |
| U12 | `implementer_agent` | `implementer_agent` (**stands, recorded as a judgment call**) | `agents/implementer_agent.md` names framework-root `scripts/`, `hooks/` and `tests/` — not `Makefile`. `devops_agent` is the other candidate by subject matter but holds no `Write`/`Edit` for framework-root tooling (`ADR-0009`, Sprint 033), so it cannot author the target. `implementer_agent` is the only profile with both the grant and the code-authorship charter. Recorded here because the charter does not name the file type, not because the proposal was overwritten. |

Every other row: the plan's `Assignee (proposed)` stands unchanged.
