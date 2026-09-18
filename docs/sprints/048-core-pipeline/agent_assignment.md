# Agent Assignment — Sprint 048 (jurisdictional-lock-reconciliation-and-047-residue)

Source: `docs/sprints/048-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`).
Phase 4.1 of `workflows/pipeline_workflow.md`. This file is the staffing
authority: it may overwrite the plan's `Assignee (proposed)` column. A Work row
is not closed until it appears here.

Mode: **claude-code** (nucleus), `delegation_mode: native` — the `Assignee`
column names which profile's ruleset governs each write.

## Scope of this artifact (Phase 4.1 only)

| Owns | Does **not** own |
| :--- | :--- |
| Which ruleset governs each unit | Model / effort (`task_scope.md`, Phase 4.3) |
| Agent-forge destination on units that create agents | `tier_escalation` proposals |

**No unit in this sprint creates a new agent profile.** U4 and U7 *modify*
existing agent profile files (`agents/implementer_agent.md`,
`agents/rule_validator.md`) as governance-prose propagation targets of the
`jurisdictional_lock` restatement (`D2`, `D6`) — they do not instantiate a new
agent, so no `agent_forge_destination` choice applies. `Destination` is `N/A`
on every row and `check_forge_ladder.py` has no forge row to validate.

---

## Staffing

Shape is mandatory:

`# | Target | Operation | Mode | Assignee | Destination | Ruleset file`

### Wave 1 — root restatement + propagation (`agents.md`, template, workflows, agent-profile prose, `rules/code_craft.md`); gate: `make verify`

U1 restates `agents.md §2 jurisdictional_lock` as its invariant (`D1`). U2-U5,
U7, U12 are the closed propagation set established by full-corpus grep
(`D2`, `D6`) — each a distinct physical file, `no_interference` satisfied by
construction. `rule-validator`'s profile responsibility ("Audits `/rules` over
the Roadmap. Creates and indexes structural norms") is the direct fit: this
wave *is* a rule restated at its root and mechanically propagated to every
derived statement, which is the same shape as Sprint 047 Wave 1 (`agent_assignment.md`
U1-U10) rather than general documentation authorship (`doc-orchestrator`) or
roadmap drafting (`orchestrator`).

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U2 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U3 | `workflows/pipeline_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U4 | `agents/implementer_agent.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U5 | `rules/code_craft.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U7 | `agents/rule_validator.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |
| U12 | `workflows/repository_hardening_workflow.md` | modify | ruleset | `rule-validator` | N/A | `agents/rule_validator.md` |

Note on U7: `rule-validator` edits its own profile file. This is not
self-staffing by this artifact — `agent_orchestrator` (this profile) assigns
the unit; `rule-validator` is the executing role for a one-line Model/Effort
wording alignment (`D6`), the same governance-prose class as its sibling rows.
No tooling or approval bypass results: the write still passes through
`jurisdictional_lock`/`no_interference` and Phase 5-8 gates like any other row.

### Wave 2 — `memory_index.json` superseded-entry purge (`extract_workflow.md` Phase 3-4)

`D3` requires replacing, not merely leaving, the stale "sanctioned exception"
entry at `memory_index.json:89`. `index_update`, `last_update`, and
`redundant_ki_purge` are owned by `Governance Learner` in
`workflows/extract_workflow.md` Phase 3 ("Semantic Indexing") and Phase 4
("Absolute Purge") — this is that role's declared jurisdiction over
`memory_index.json`, distinct from `rule-validator`'s `/rules` and `agents.md`
scope. Matches the plan's proposal.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U6 | `memory_index.json` | modify | ruleset | `governance-learner` | N/A | `agents/governance_learner.md` |

### Wave 3 — framework-root `scripts/` and `tests/` (`ADR-0009`, Sprint 033)

U8-U11, U13 change executable behaviour or pytest suites under framework-root
`scripts/` and `tests/`. Per `agents.md §6 code_unit_assignee`, those trees
MUST be assigned `implementer_agent`; assigning `devops_agent` is PROHIBITED
after Sprint 033. Targets are disjoint physical files. U8 is the sprint's one
planned paired row (subject `scripts/verify_references.py` + its mandatory
test `tests/test_verify_references.py`, `D4`/`D8`) — compliant by
construction under U1's restated invariant, and deliberately sequenced so
this sprint is the first consumer of its own rule change.

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U8 | `scripts/verify_references.py` (subject) + paired test `tests/test_verify_references.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U9 | *contingency* — files named by U8's first run (bounded to `scripts/`/`tests/`/`skills/*/scripts/` trees; abort at >10 defects, `Abort criterion 2`) | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U10 | `scripts/map_workflows.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U11 | `tests/test_mode.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |
| U13 | `tests/test_session_start.py` | modify | ruleset | `implementer-agent` | N/A | `agents/implementer_agent.md` |

### Wave 4 — roadmap document (`docs/roadmaps/`)

U14 corrects the "Six findings" count and the stale `KI-047-3` premise in the
core-pipeline roadmap queue. `orchestrator`'s declared responsibility
("Roadmap Author... draft the Initial Sprint Roadmap... compile the
Definitive Sprints") is the direct-fit ruleset for `docs/roadmaps/` content —
more specialized here than `doc-orchestrator` (general project documentation,
API contracts, architecture docs; no roadmap-specific mandate) or
`rule-validator` (`/rules` and `agents.md`, not the Future-hierarchy roadmap
tree, `agents.md §0 Hierarchy`).

| # | Target | Operation | Mode | Assignee | Destination | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U14 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | ruleset | `orchestrator` | N/A | `agents/orchestrator.md` |

## Tool-sufficiency check (this artifact's mechanical verification)

Every unit in this sprint is a `modify` operation, requiring `Write` and
`Edit` at minimum. All four assigned profiles declare both:

| Assignee | `tools:` (frontmatter) | Profile file exists at declared destination |
| :--- | :--- | :--- |
| `rule-validator` | `Read, Glob, Grep, Write, Edit` | `agents/rule_validator.md` — verified |
| `governance-learner` | `Read, Glob, Grep, Write, Edit` | `agents/governance_learner.md` — verified |
| `implementer-agent` | `Read, Glob, Grep, Write, Edit, Bash` | `agents/implementer_agent.md` — verified |
| `orchestrator` | `Read, Glob, Grep, Write, Edit` | `agents/orchestrator.md` — verified |

All four destinations are the nucleus `agents/` roster (this is a nucleus
session on `ai-sprint/048`; no host `.claude/agents/` or profile-path lookup
applies here).

## Assignee breakdown

| Assignee | Units | Count |
| :--- | :--- | :--- |
| `rule-validator` | U1, U2, U3, U4, U5, U7, U12 | 7 |
| `governance-learner` | U6 | 1 |
| `implementer-agent` | U8, U9, U10, U11, U13 | 5 |
| `orchestrator` | U14 | 1 |
| **Total** | U1-U14 | **14** |

## Disagreements with the plan

None. The plan's `Assignee (proposed)` column stands for every unit,
cross-checked against each candidate's declared `tools:` and domain:

- U1-U5, U7, U12 (`agents.md`, template, workflow, agent-profile, and
  `code_craft.md` prose restating/propagating `jurisdictional_lock`) →
  `rule-validator`. Confirmed over `doc-orchestrator` (general documentation,
  no rule-propagation mandate) — the same wave shape as Sprint 047's U1-U10.
- U6 (`memory_index.json` superseded-entry purge) → `governance-learner`.
  Confirmed against `workflows/extract_workflow.md` Phase 3-4, which names
  `Governance Learner` as owner of `index_update` / `redundant_ki_purge`.
- U8, U9, U10, U11, U13 (`scripts/`, `tests/`) → `implementer-agent`.
  Confirmed under `agents.md §6 code_unit_assignee` — `devops_agent` holds no
  `Write`/`Edit` for these trees after Sprint 033 (`ADR-0009`).
- U14 (`docs/roadmaps/core/pipeline/021-030-program-queue.md`) →
  `orchestrator`. Confirmed as the Roadmap-Author role over
  `doc-orchestrator` (general docs) and `rule-validator` (`/rules` scope,
  not the roadmap tree).
