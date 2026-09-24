# Agent Assignment — Sprint 050 (deterministic-quality-instrument)

Source: `docs/sprints/050-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code** (nucleus), `delegation_mode: native` — the `Assignee`
column names which profile's ruleset governs each write. This artifact does
not carry Model/Effort tiers — those are `token_economy_agent` → `rule_validator`
territory, transcribed into `task_scope.md` at Phase 4.3
(`agents.md §6 agent_orchestrator` `no_model_columns`).

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Model / effort (`task_scope.md`, Phase 4.3) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

**No unit in this sprint creates a new agent profile.** Every U1–U10 assignee
is an existing core or auxiliary role (`rule_validator`, `implementer_agent`,
`doc_orchestrator`). `Destination` is `N/A` on every row and
`check_forge_ladder.py` has no forge row to validate.

**No unit in this sprint requires forging a new skill.** `IMPLEMENTATION_PLAN.md`
`D3` is explicit: the instrument built here (`scripts/quality_audit.py`) is a
script under `scripts/` with a declared `invoked_by:` (`RA-16`), not a
`skills/[name]/` entry — `skills/` is reserved for model-invoked tools
(`config/invocation_exceptions.json`). The two pre-existing skills
(`python-quality-auditor`, `js-standardizer`) stay as model-invoked helpers and
are only corrected in prose (`U4`); nothing in this sprint instantiates,
forges, or scaffolds a skill directory. Recorded here for Phase 4.2
(`skill_assignment.md`) dispatch: **all 10 units → skill-forge NOT required.**

---

## Staffing

Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave 1 — instrument definition, build and wiring (`D1`, `D2`, `D3`, `D5`, `D8`)

`agents.md` is the structural subject of `U1` and `U5`, landing in sequence,
never concurrently (`agents.md §2 jurisdictional_lock` caps concurrent claims,
not lifetime touches — `D8`). `U1` states the unit of measure (the contract);
`U2` builds the instrument against that contract; `U3` and `U4` wire and
document the instrument once it exists; `U5` names the instrument in
`agents.md`, which requires `U2` to exist first. Sequence within this wave:
**`U1` → `U2` → {`U3`, `U4`, `U5`}**, with `U5` additionally ordered after
`U1` closes (same-subject, non-concurrent).

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| U2 | `scripts/quality_audit.py` (subject) + paired `tests/test_quality_audit.py`, same commit | create | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U3 | `Makefile` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U4 | `config/invocation_exceptions.json` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |
| U5 | `agents.md` | modify | native | `rule_validator` | N/A | `agents/rule_validator.md` |

### Wave 2 — `topology_version` writer and its consumers (`D7`)

`U6` builds the writer; `U7` and `U8` are separate invocations (`RA-13`) that
name the command `U6` creates in workflow prose. Sequence: **`U6` → {`U7`,
`U8`}**.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U6 | `scripts/session_state.py` (subject) + paired `tests/test_session_state.py`, same commit | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U7 | `workflows/close_workflow.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |
| U8 | `workflows/deployment_workflow.md` | modify | native | `doc_orchestrator` | N/A | `agents/doc_orchestrator.md` |

### Wave 3 — test hardening and generated-guide regeneration

`U9` is independent of the other waves (closes a pre-existing `capsys` gap in
an unrelated test file). `U10` is the regenerated output of
`scripts/map_workflows.py` after `U7`/`U8` change their source workflow files
— ordered **{`U7`, `U8`} → `U10`**, following the Sprint 049 `U6` precedent
for generated-output units (never hand-edited).

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U9 | `tests/test_audit_cursor_models.py` | modify | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |
| U10 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | modify (generated, never hand-edited) | native | `implementer_agent` | N/A | `agents/implementer_agent.md` |

---

## Ordering constraints carried from the plan

| Constraint | Reason |
| :--- | :--- |
| `U1` before `U2` | `U2` implements the unit-of-measure contract `U1` states (`D1`, `D2`, `D8`) |
| `U2` before `U5` | `U5` replaces "No instrument exists for this row today" with the instrument's name; the name does not exist before `U2` lands (`D8`) |
| `U1` before `U5`, never concurrent | Both claim `agents.md` as structural subject; `jurisdictional_lock` caps concurrent claims, not lifetime touches (`D8`, Phase 014 `T21`/`T22` precedent) |
| `U2` before `U3` | `D5`'s branch decision (verify-wiring vs. standalone target) is made by running the auditor over the repository, which requires `U2` to exist |
| `U2` before `U4` | `U4`'s corrected skill notes name `scripts/quality_audit.py` as the real instrument; it must exist to be named accurately |
| `U6` before `U7` and `U8` | Both workflow edits invoke the `session_state.py set-topology` subcommand `U6` creates |
| `U7` and `U8` before `U10` | `U10` is the regenerated output of `scripts/map_workflows.py`; two workflow files change in this sprint and the guide is never hand-edited (`agents.md §0`) |

---

## Tool-sufficiency check (this artifact's mechanical verification)

Every unit in this sprint is a `modify` or `create` operation, requiring
`Write` and `Edit` at minimum; `U2`, `U3`, `U6`, `U9`, `U10` additionally
require running a script or test suite to produce/verify their target.

| Assignee | `tools:` (frontmatter) | Profile file exists at declared destination |
| :--- | :--- | :--- |
| `rule_validator` | `Read, Glob, Grep, Write, Edit` | `agents/rule_validator.md` — verified |
| `implementer_agent` | `Read, Glob, Grep, Write, Edit, Bash` | `agents/implementer_agent.md` — verified |
| `doc_orchestrator` | `Read, Glob, Grep, Write, Edit` | `agents/doc_orchestrator.md` — verified |

All three destinations are the nucleus `agents/` roster (this is a nucleus
session on `ai-sprint/050`; no host `.claude/agents/` or profile-path lookup
applies here).

---

## Assignee breakdown

| Assignee | Units | Count |
| :--- | :--- | :--- |
| `rule_validator` | U1, U4, U5 | 3 |
| `implementer_agent` | U2, U3, U6, U9, U10 | 5 |
| `doc_orchestrator` | U7, U8 | 2 |
| **Total** | U1–U10 | **10** |

---

## Disagreements with the plan

| Unit | Plan proposal | Recorded assignee | Reason |
| :--- | :--- | :--- | :--- |
| U1 | `doc_orchestrator` | `rule_validator` | `agents.md` is the constitution; every prior sprint that edited it assigned `rule_validator`, not `doc_orchestrator` — explicit precedent recorded at `docs/sprints/024-core-pipeline/agent_assignment.md:24` ("Constitutional edits are its jurisdiction") and repeated at Sprints 025, 026, 043, 046, 047, 048, 049. `rule_validator`'s declared `responsibility` ("Audits `/rules` over the Roadmap. Creates and indexes structural norms") is the direct-fit ruleset for a `§1` row edit; `doc_orchestrator`'s charter is general project documentation, API contracts and architecture docs, with no ruleset-authoring mandate. `governance_learner` was considered and rejected — its `agents.md §7` writes are sourced from `/memory/` sprint-close distillation (`escalation`), not from a Phase 1 plan's design decisions being executed directly, which is what `U1` is. |
| U4 | `implementer_agent` | `rule_validator` | `config/invocation_exceptions.json` is the `RA-16` invocation-exceptions registry, not framework-root `scripts/`, `hooks/`, or `tests/` — outside `implementer_agent`'s declared `write_scope` (`agents/implementer_agent.md`: "Holds `Write`/`Edit` for the framework-root `scripts/`, `hooks/`, and `tests/` trees"). The identical file, with the identical class of edit (correcting a skill note that named this sprint as a destination), was assigned `rule_validator` twice already: `docs/sprints/049-core-pipeline/agent_assignment.md:67` (`U10`) and `docs/sprints/047-core-pipeline/agent_assignment.md:96` (`U24`). `rule_validator`'s indexing/rule-auditing charter is the direct fit; `implementer_agent` has no grant over `config/`. |
| U5 | `doc_orchestrator` | `rule_validator` | Same reasoning as `U1` — same file, same constitutional-edit class, and `jurisdictional_lock` requires `U1` and `U5` to be non-concurrent claims on the same subject; splitting them across two different assignees would not change that requirement but would break the precedent that governs every other `agents.md` edit in this corpus. |

Every other row (`U2`, `U3`, `U6`, `U7`, `U8`, `U9`, `U10`): the plan's
`Assignee (proposed)` stands unchanged.

- `U3` (`Makefile`) → `implementer_agent` confirmed as a judgment call, not a
  literal `write_scope` match (`Makefile` is not `scripts/`, `hooks/`, or
  `tests/`): `devops_agent` is the closer subject-matter candidate but holds
  no `Write`/`Edit` for framework-root tooling after Sprint 033 (`ADR-0009`),
  and `implementer_agent` is the only profile holding both the grant and the
  code-authorship charter. Same judgment call recorded at
  `docs/sprints/049-core-pipeline/agent_assignment.md:86` (`U12`).
- `U10` (`docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`) → `implementer_agent`
  confirmed: the guide is regenerated by running `scripts/map_workflows.py`
  (requires `Bash`, which `doc_orchestrator` does not hold), following the
  Sprint 049 `U6` precedent for generated-output units cited in the plan's own
  `U10` unit-content note.
