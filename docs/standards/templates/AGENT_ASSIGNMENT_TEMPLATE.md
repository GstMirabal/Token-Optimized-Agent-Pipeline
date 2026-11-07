# Agent Assignment — Sprint {{SPRINT_ID}} ({{SPRINT_SLUG}})

Source: `docs/sprints/{{SPRINT_ID}}-{{STACK}}-{{LAYER}}/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **{{SESSION_TOOL}}**, `delegation_mode: {{DELEGATION_MODE}}` — the
`Assignee` column names which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Cursor model / effort (`task_scope.md`) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

`Destination` is **required** on every unit that **creates** an agent profile.
Values: `host:.claude/agents/` (default), `profile:<path>`, `nucleus:PR`.
Units that do not create a profile use `N/A`.

---

## Staffing

One table per wave. Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

Target is the plan row's File and Operation holds only its verb
(`create`, `modify`, `delete`): `scripts/check_forge_ladder.py` reads both. The
plan's Operation text is not copied here; the unit id cites it.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| {{ID}} | `{{PATH}}` | create/modify/delete | sequential / ruleset | `{{ROLE}}` | {{DESTINATION}} | `agents/{{ROLE}}.md` |

## Disagreements with the plan

Record every overwrite of `Assignee (proposed)` here, with the reason. Write
`None` when the plan proposal stands.

{{DISAGREEMENTS}}
