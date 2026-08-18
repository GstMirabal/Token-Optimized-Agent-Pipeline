# Agent Assignment — Sprint 023 (`upstream-findings`)

**Covers the sprint to date** (units `C9`, `C0`, `C0.2`). Eleven units remain and
this file is appended as they land, then finalised at Closeout.

**The delegation deviation ended mid-sprint, at unit `C2`.** Until then no role
was dispatched: the session configuration forbids spawning subagents unless the
human asks, a conflict reported before Phase 1 and authorised in this sprint and
in `022`. The human lifted it at `C2`, and `qa_agent` and `tester_agent` were
dispatched as actual subagents for the first time in this sprint — on the unit
where the framework's own tier basis says the value is highest, a security
report.

Units `C9`, `C0`, `C0.2`, `C0.3` and `C1` were therefore written *and* gated by
the same session. That is not a footnote: `config/model_tiers.json` records that
across four consecutive host sprints every central defect was found by a gate
and nothing else, several after surviving their author's own verification. The
verdicts on those five units are the author's, and this file says so rather than
letting a green result imply otherwise.

What follows records which profile's **ruleset** governed each write — which is
what this artifact is for, and why a declared solo session still owed it.

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

## The model that ran, which is not the model the tiers declare

| Ruleset | Tier it declares | Model that actually ran |
| :--- | :--- | :--- |
| `principal_agent`, `qa_agent`, `tester_agent` | `gate` — opus, effort high | Opus 5 (session model) — agrees by coincidence, not by dispatch |
| `orchestrator`, `rule_validator`, `skill_architect`, `agent_orchestrator` | `author` — sonnet, effort medium | **Opus 5** (session model) |
| `devops_agent` | `author` — sonnet | **Opus 5** (session model) |

No subagent was dispatched, so no profile's `model:` key was ever read by the
harness. `scripts/check_model_tiers.py` passes on every `make verify` and what it
proves is that two **declarations** agree — `config/model_tiers.json` and the 13
frontmatters — never that the declared model is the one that executed.

This matters for attribution rather than for cost: `C0.2`'s `Assignee` column was
added so a gate rejection could be traced to the role and tier that produced the
defect, and that trace is only true when the profile's model is the one that ran.
Recorded here, and in `task_scope.md`, as the standing gap. The durable fix —
requiring this statement of every sprint — is proposed against
`pipeline_workflow.md` Phase 4.1 and deliberately not applied in this commit.

## Unresolved

`F-021-A2` stands: **no profile in `agents/` holds `Write` for `scripts/`**, so
`devops_agent` is the closest owner of the script changes rather than the correct
one. Sprint `023` unit `C5` widens the role map; until it lands, every `scripts/`
write in this sprint is attributed to a profile that could not have performed it.
