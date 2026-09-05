# Agent Assignment — Sprint 042 (template-gate-parity)

Source: `docs/sprints/042-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
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

### Wave 1 — the stale record (independent of everything else)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 2 — the declaration (blocks the script)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U2 | `config/template_gates.json` | create | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 3 — the instrument

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U3 | `scripts/check_template_gates.py` | create | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 4 — invoker and tests (depend on U3)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U4 | `Makefile` | modify | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U5 | `tests/test_check_template_gates.py` | create | ruleset | `implementer_agent` | N/A | `agents/implementer_agent.md` |

### Wave 5 — governance prose (depends on the final file count)

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U6 | `README.md` | modify | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U7 | `docs/decisions/ADR-0012-template-gate-parity.md` | create | ruleset | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

---

## Disagreements with the plan

**None.** Every `Assignee (proposed)` from `IMPLEMENTATION_PLAN.md` stands.

Three staffing facts are recorded rather than left to inference:

| Fact | Why it is stated |
| :--- | :--- |
| `implementer_agent` owns `scripts/`, `tests/` and the framework-root `Makefile`; `devops_agent` does **not** hold `Write`/`Edit` on those trees | `ADR-0009` (Sprint 033), `agents.md §6`. U4 edits a build file, which reads like `devops_agent` territory and is not — `devops_agent` retains `Bash` for environment routines, not authorship |
| `skill_architect` is absent from this table | No unit forges a skill. `skills/[name]/scripts/` is its tree and no unit touches it (`agents.md §3 three_file_standard`) |
| U2 is staffed to `implementer_agent`, not `doc_orchestrator`, although its target is a `.json` file | `config/template_gates.json` is machine-read input to `scripts/check_template_gates.py`, not documentation. Its correctness is decided by the script that parses it |

## Delegation note

`delegation_mode` is `native` (Claude Code can dispatch the eight roles).
`IMPLEMENTATION_PLAN.md` `## Cost` declares **2 subagents dispatched** — `qa_agent`
and `tester_agent` at Phase 7, in fresh context, as `pipeline_workflow.md` requires
of both harnesses. Units U1–U7 are executed in this session under the named
profile's ruleset, so the `Mode` column reads `ruleset` on every row. This is a
recorded configuration, not a `delegation_conflict`: the declared mode and the
harness capability agree (`start_workflow.md` `delegation_conflict` fires only when
they diverge).
