# Agent Assignment — Sprint 041 (bi-harness-bridge-parity)

Source: `docs/sprints/041-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code**, `delegation_mode: native` — the `Assignee` column names
which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

`Destination` is **required** on every unit that **creates** an agent profile.
**No unit in this sprint creates an agent profile**, so every row is `N/A`.

---

## Staffing

Shape: `# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave 1 — the shared predicate (blocks everything else)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/bridge_state.py` | create | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 2 — consumers of U1 (parallel-safe, distinct files)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U2 | `scripts/session_start.py` | modify | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U3 | `hooks/on_init.py` | modify | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U4 | `scripts/cursor_adapter.py` | modify | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U13 | `scripts/install.py` | modify | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 3 — the command source (depends on U4's rewrite)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U5 | `commands/start.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 4 — governance prose

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U6 | `workflows/start_workflow.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U7 | `workflows/deployment_workflow.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U10 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U11 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U12 | `workflows/pipeline_workflow.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U16 | `README.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 5 — tests

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U8 | `tests/test_bridge_state.py` | create | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U9 | `tests/test_session_start.py` | modify | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U14 | `tests/test_installer.sh` | modify | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U15 | `tests/test_cursor_adapter.py` | modify | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

---

## Disagreements with the plan

**None.** Every `Assignee (proposed)` from `IMPLEMENTATION_PLAN.md` stands.

Two staffing facts are recorded rather than left to inference:

| Fact | Why it is stated |
| :--- | :--- |
| `implementer_agent` owns `scripts/`, `hooks/` and `tests/`; `devops_agent` does **not** hold `Write`/`Edit` on those trees | `ADR-0009` (Sprint 033), `agents.md §6`. U3 modifies `hooks/on_init.py`, which reads like `devops_agent` territory and is not |
| `skill_architect` is absent from this table | No unit forges a skill. `skills/[name]/scripts/` is its tree and no unit touches it (`agents.md §3 three_file_standard`) |

## Delegation note

`delegation_mode` is `native` (Claude Code can dispatch the eight roles), but
**no subagents are dispatched this sprint** — `IMPLEMENTATION_PLAN.md` `## Cost`
declares `Subagents dispatched: 0`. The `Mode` column therefore reads `ruleset`
on every row: the named profile's ruleset governs the write, performed in this
session. This is a recorded configuration, not a `delegation_conflict`: the
declared mode and the harness capability agree (`start_workflow.md`
`delegation_conflict` fires only when they diverge).
