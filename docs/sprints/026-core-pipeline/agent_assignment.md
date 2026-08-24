# Agent Assignment — Sprint 026 (`tool-portability`)

Source: `docs/sprints/026-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`, `Design §D9`).
Precedent format: `docs/sprints/025-core-pipeline/agent_assignment.md`.

This sprint is the first to carry both cases in one run. **HITO 1** runs under
Claude Code, `agents.md §6`'s native 8-role pipeline: the `Assignee` column below
names a profile Claude Code can dispatch as a subagent, tool-restricted by that
profile's `tools:` frontmatter. **HITO 2** runs under Cursor,
`delegation_mode: sequential` (`Design §D4c`): no subagent is spawned, so the
`Assignee` column instead names **which profile's ruleset a single Cursor agent
adopts** for that write — the same distinction `workflows/pipeline_workflow.md`
Phase 4.1 requires when a session cannot dispatch subagents. The `Mode` column
makes that difference visible per row rather than leaving it to prose.

## Declared condition — `F-021-A2` (not a normal assignment)

`agents.md §6` names 8 core roles; `F-021-A2` (open upstream finding) measures that
none of them is a code-implementer role and that `devops_agent` is the only profile
holding `Write`/`Edit` on `scripts/` and `hooks/` (`F-086-A1`, `agents.md §6
devops_agent`). `Design §D9` states the consequence: `devops_agent` absorbs **every**
code-bearing unit of this sprint under those two trees, not because it is the
correct owner but because it is the only holder. Every row below marked
`devops_agent` for a `scripts/` or `hooks/` target is that consequence, restated
per-unit rather than resolved. This artifact does not attempt to close `F-021-A2`;
the plan puts that out of scope (`Design §D9`, citing `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:532`).

---

## HITO 1 — Claude Code, native 8-role pipeline

### H1.a — State and session

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `docs/active_state.json` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P8 | `scripts/session_state.py` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P8.1 | `tests/test_session_protocol.py` | modify | Claude Code, subagent dispatch | `tester_agent` | `agents/tester_agent.md` |
| P2 | `scripts/session_state.py` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P8.2 | `workflows/start_workflow.md` | modify | Claude Code, subagent dispatch | `orchestrator` | `agents/orchestrator.md` |
| P2.1 | `workflows/start_workflow.md` | modify | Claude Code, subagent dispatch | `orchestrator` | `agents/orchestrator.md` |

### H1.b — Installer and the reference census

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P3.0 | `scripts/install.py` (from `scripts/install_claude.py`) | create (`git mv`) | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P3.1 | `scripts/install.sh` (from `scripts/install_claude.sh`) | create (`git mv`) | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P3.1b | `scripts/install_claude.sh` | create (shim) | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P3.3 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | Claude Code, subagent dispatch | `orchestrator` | `agents/orchestrator.md` |
| P10 | `scripts/install.py` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P10.1 | `.gitignore` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |

**P3.2 — 29 files, one subtask per physical file (`jurisdictional_lock` precedent
of Sprint 023 `C0.3`), resolved here from "por jurisdicción" to a named assignee
per file, mirroring the plan's own census table:**

| Target | Assignee | Ruleset file |
| :--- | :--- | :--- |
| `hooks/on_init.py:16` | `devops_agent` | `agents/devops_agent.md` |
| `hooks/on_commit_msg.py:14` | `devops_agent` | `agents/devops_agent.md` |
| `scripts/merge_json.py:4` | `devops_agent` | `agents/devops_agent.md` |
| `scripts/_root.py:71` | `devops_agent` | `agents/devops_agent.md` |
| `scripts/_mode.py:4,26` | `devops_agent` | `agents/devops_agent.md` |
| `scripts/render_readme.py:3,66,113` | `devops_agent` | `agents/devops_agent.md` |
| `scripts/verify_references.py:160` | `devops_agent` | `agents/devops_agent.md` |
| `skills/compliance-checker/scripts/distill.py:10` | `skill_architect` | `agents/skill_architect.md` |
| `tests/test_installer.sh:31,67,83,93,112` | `tester_agent` | `agents/tester_agent.md` |
| `tests/test_mass_standardizer.py:297` | `tester_agent` | `agents/tester_agent.md` |
| `tests/test_invocation_coverage.py:70` | `tester_agent` | `agents/tester_agent.md` |
| `tests/test_root_resolution.py:57` | `tester_agent` | `agents/tester_agent.md` |
| `claude/settings.hooks.json:16` | `devops_agent` | `agents/devops_agent.md` |
| `config/invocation_exceptions.json:55` | `devops_agent` | `agents/devops_agent.md` |
| `.gitignore:100` | `devops_agent` | `agents/devops_agent.md` |
| `agents.md:77,83,110,163` | `rule_validator` | `agents/rule_validator.md` |
| `workflows/start_workflow.md:23,25` | `orchestrator` | `agents/orchestrator.md` |
| `workflows/audit_workflow.md:18` | `orchestrator` | `agents/orchestrator.md` |
| `README.md:60,101,107,123,164,198` | `orchestrator` | `agents/orchestrator.md` |
| `SECURITY.md:17` | `orchestrator` | `agents/orchestrator.md` |
| `.github/ISSUE_TEMPLATE/bug_report.yml:26` | `orchestrator` | `agents/orchestrator.md` |
| `docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md:41` | `orchestrator` | `agents/orchestrator.md` |
| `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md:12,21,70,81,83` | `orchestrator` | `agents/orchestrator.md` |
| `docs/architecture/global_topology.md:53` | `orchestrator` | `agents/orchestrator.md` |
| `docs/architecture/topology_map.md:17,21` | `orchestrator` | `agents/orchestrator.md` |
| `docs/plans/README.md:51` | `orchestrator` | `agents/orchestrator.md` |
| `skills/slash-commander/SKILL.md:12,30` | `skill_architect` | `agents/skill_architect.md` |
| `skills/slash-commander/README.md:49` | `skill_architect` | `agents/skill_architect.md` |
| `profiles/example-project/README.md:18` | `skill_architect` | `agents/skill_architect.md` |

All 29 rows: Claude Code, subagent dispatch (same `Mode` as the rest of H1.b).

### H1.c — Portable guards

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P9 | `hooks/on_push.py` | create | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P9.1 | `scripts/install.py` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P9.2 | `tests/test_on_push.py` | create | Claude Code, subagent dispatch | `tester_agent` | `agents/tester_agent.md` |

### H1.d — Cursor adapter

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P6 | `workflows/standardization_workflow.md` | modify | Claude Code, subagent dispatch | `orchestrator` | `agents/orchestrator.md` |
| P11 | `.gitignore` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P5 | `config/rule_triggers.json` | create | Claude Code, subagent dispatch | `rule_validator` | `agents/rule_validator.md` |
| P5.1 | `scripts/verify_references.py` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P5.2 | `agents.md` | modify | Claude Code, subagent dispatch | `rule_validator` | `agents/rule_validator.md` |
| P4.0 | `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` | create | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P4.0b | `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` | modify | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P4 | `scripts/cursor_adapter.py` | create | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |
| P4.1 | `tests/test_installer.sh` | modify | Claude Code, subagent dispatch | `tester_agent` | `agents/tester_agent.md` |

### H1.e — Constitutional enablement of the Cursor half

| # | Target | Operation | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `workflows/pipeline_workflow.md` | modify | Claude Code, subagent dispatch | `orchestrator` | `agents/orchestrator.md` |
| P1.1 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerate | Claude Code, subagent dispatch | `devops_agent` | `agents/devops_agent.md` |

### H1.f — Hito 1 gate (fresh context, native 8-role, under Claude Code)

| # | Deliverable | Mode | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- | :--- |
| G1.q | QA verdict on the Hito 1 units, recorded in `docs/sprints/026-core-pipeline/SPRINT_LOG.md` | Claude Code, subagent dispatch | `qa_agent` | `agents/qa_agent.md` |
| G1.t | Tester verdict on the same units, same file | Claude Code, subagent dispatch | `tester_agent` | `agents/tester_agent.md` |

---

## Migration Gate — not a Work-table unit, flagged rather than assigned

The plan's own definition (`## Work`, opening line) makes a unit "a commit whose
structural subject is one physical file." The Migration Gate section (three
commands executed under Claude Code, then `session_state.py claim --tool cursor`
under Cursor, then observations `M1`–`M7`) carries no `#` and no `Assignee` column
in the plan — it is a procedure, not a unit. It is named here rather than silently
folded into HITO 1 or HITO 2: **no profile is assigned to run the three commands or
to record `M1`–`M7` in `SPRINT_LOG.md`.** This is not treated as an unassigned unit
of the deliverable (it is not a unit by the plan's own vocabulary), but it is the
same class of write — into `SPRINT_LOG.md` — flagged below alongside `G1.q`/`G1.t`/`A3`.

---

## HITO 2 — Cursor, `delegation_mode: sequential`

No subagent is instantiated. Each row names the profile whose ruleset the single
Cursor agent adopts for that write, per `Design §D4c`: new Cursor chat per gate,
tool and model read from disk and recorded, never human attestation.

| # | Target | Operation | Mode | Ruleset adopted | Ruleset file |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P7 | `agents.md` | modify | Cursor, sequential (ruleset adoption) | `rule_validator` | `agents/rule_validator.md` |
| P7.1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | Cursor, sequential (ruleset adoption) | `rule_validator` | `agents/rule_validator.md` |
| A2 | `tests/fixtures/` (sandbox under `/private/tmp`) | create + delete | Cursor, sequential (ruleset adoption) | `tester_agent` | `agents/tester_agent.md` |
| P4.2 | `scripts/audit_cursor_models.py` | create | Cursor, sequential (ruleset adoption) | `devops_agent` | `agents/devops_agent.md` |
| P4.3 | `Makefile` | modify | Cursor, sequential (ruleset adoption) | `devops_agent` | `agents/devops_agent.md` |
| P4.4 | `config/model_tiers.json` | modify | Cursor, sequential (ruleset adoption) | `rule_validator` | `agents/rule_validator.md` |
| A3 | `docs/sprints/026-core-pipeline/SPRINT_LOG.md` | modify (this is the Hito 2 gate) | Cursor, sequential (ruleset adoption) | `qa_agent` | `agents/qa_agent.md` |

---

## Disagreements found — `Design §D9` vs. profile `tools:` frontmatter (not resolved)

Both flagged per the task's instruction: an assignment the harness would silently
refuse to execute is worse than an unassigned unit, because it looks assigned.

### 1. `tests/` writes assigned to `tester_agent`, whose `tools:` frontmatter has no `Write`/`Edit`

`agents/tester_agent.md` declares `tools: Read, Glob, Grep, Bash` (no `Write`,
no `Edit`), even though its own `description` line says it is used "to write and
execute unit/integration tests." `Design §D9`'s row `tests/ → tester_agent` inherits
that gap into every unit that targets `tests/`:

- `P8.1` (`tests/test_session_protocol.py`, HITO 1 — real subagent dispatch)
- `P9.2` (`tests/test_on_push.py`, HITO 1)
- `P4.1` (`tests/test_installer.sh`, HITO 1)
- The four "Tests" rows of `P3.2`'s census (`tests/test_installer.sh`,
  `tests/test_mass_standardizer.py`, `tests/test_invocation_coverage.py`,
  `tests/test_root_resolution.py`, HITO 1)
- `A2` (`tests/fixtures/`, HITO 2)

This is most consequential for the HITO 1 rows: those are real Claude Code
subagent dispatches, and a subagent whose `tools:` frontmatter omits `Write`/`Edit`
cannot perform the operation its row names. Under HITO 2 (`A2`) the mechanical
block does not apply the same way — Cursor's single-agent session is not
tool-gated per adopted ruleset the way a Claude Code subagent is — but the
inconsistency between profile description and profile frontmatter is the same
document defect either way.

### 2. `SPRINT_LOG.md` verdict writes assigned to `qa_agent`/`tester_agent`, neither holding `Write`/`Edit` — and contradicting `Design §D9`'s own cited authority

`agents/qa_agent.md` and `agents/tester_agent.md` both declare
`tools: Read, Glob, Grep, Bash`. `G1.q`, `G1.t` (HITO 1) and `A3` (HITO 2) all
require a verdict to be **recorded** — written — into
`docs/sprints/026-core-pipeline/SPRINT_LOG.md`. Neither assigned profile can
perform that write under its own frontmatter.

This also contradicts `Design §D9`'s own stated basis for `docs/sprints/026-core-pipeline/`:
the table there reads `principal_agent / orchestrator según artefacto —
config/artifact_registry.json, columnas role`. `config/artifact_registry.json`
names `SPRINT_LOG.md`'s `role` as **Orchestrator** (`agents/orchestrator.md`,
which does hold `Write`/`Edit`), not `qa_agent` or `tester_agent`. The Work-table
assignments for `G1.q`, `G1.t`, and `A3` diverge from the authority `Design §D9`
itself names for that file.

---

## Coverage summary

- 35 top-level plan units carry a named assignee directly from `## Work` (34
  file-operation rows + `P3.2` as one row before expansion), plus the 2 `H1.f` gate
  deliverables and the `A3` HITO 2 gate deliverable, all resolved above.
- `P3.2`'s "por jurisdicción" placeholder is resolved into 29 named file-level
  assignments (table above), mirroring the plan's own census — zero of the 29 left
  unassigned.
- Total assigned line items: 34 non-`P3.2` units + 29 `P3.2` files + `G1.q` + `G1.t`
  = 65, plus HITO 2's 7 units already counted in the 34. No unit from `## Work` is
  without a named assignee.
- No new profile was authored. Every assignee above is an existing file under
  `agents/`, confirmed present before assignment.
- The Migration Gate's three commands and `M1`–`M7` recording carry no assignee in
  the plan and are flagged, not resolved, above — they are not a `## Work` unit by
  the plan's own definition, so their absence does not count against "every unit
  has a named assignee."
