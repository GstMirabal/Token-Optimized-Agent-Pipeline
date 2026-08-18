# Agent Assignment — Sprint 023 (`upstream-findings`)

**Covers the sprint to date** (units `C9`, `C0`, `C0.2`). Eleven units remain and
this file is appended as they land, then finalised at Closeout.

Eight roles were **not** dispatched: this session cannot spawn subagents, a
conflict reported before Phase 1 and authorised by the human in this session and
in `022`. What follows records which profile's **ruleset** governed each write —
which is what this artifact is for, and why a declared solo session still owes it.

| Ruleset applied | Artifacts |
| :--- | :--- |
| `principal_agent` | `IMPLEMENTATION_PLAN.md`, the Approval Gate held per unit |
| `orchestrator` | this directory and `SPRINT_LOG.md` |
| `devops_agent` | `scripts/branch_sovereignty.py` (`C9`), `scripts/docs_freshness_check.py`, `scripts/map_workflows.py`, `scripts/session_probe.py` (`C0.2`) |
| `rule_validator` | `agents.md`, `workflows/pipeline_workflow.md`, `workflows/close_workflow.md`, `agents/rule_validator.md`, `config/artifact_registry.json` (`C0`, `C0.2`) |
| `agent_orchestrator` | this file |
| `skill_architect` | `skill_assignment.md` |
| `tester_agent` | `tests/test_docs_freshness_check.py`, `tests/test_artifact_registry.py` |
| `qa_agent` | `make verify` — structural verification, not a dispatched role |

## The gap this file was itself found by

`C0.2` gave `config/artifact_registry.json` its first consumers, and the
freshness gate immediately reported this file and `skill_assignment.md` missing
from this directory — Phases 4.1 and 4.2 had left no artifact in sprint `023`
while sprints `021`, `022`, `024` and `025` all produced both. The hand-coded
map the gate read before `C0.2` listed three filenames and could not see them.

That is the unit working as designed on the sprint that built it, and it is
recorded here rather than quietly fixed.

## Unresolved

`F-021-A2` stands: **no profile in `agents/` holds `Write` for `scripts/`**, so
`devops_agent` is the closest owner of the script changes rather than the correct
one. Sprint `023` unit `C5` widens the role map; until it lands, every `scripts/`
write in this sprint is attributed to a profile that could not have performed it.
