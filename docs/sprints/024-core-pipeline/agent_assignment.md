# Agent Assignment — Sprint 024 (`close-machinery-verdicts`)

Produced by Phase 4.1. Names the artifact it leaves, per `C0.2`'s principle that
a phase is defined by what it writes rather than by who was invoked.

## The conflict this file has to be honest about

`agents.md §6` requires eight roles per pipeline pass. **This session could not
spawn subagents**, and `start_workflow.md` Phase 2 `delegation_conflict` requires
reporting that to the human before Phase 1 rather than resolving it silently. It
was reported and the human authorised sequential execution.

So this is **not** a record of eight agents that ran. It is a record of which
profile's ruleset governed each write, executed by the lead agent. Writing it as
if eight roles had been dispatched would be the fiction the delegation-conflict
precedent exists to prevent: a host once let that conflict resolve itself, Phases
4 and 7 never ran, and nothing detected it for twelve commits.

| Ruleset applied | Artifacts | Why that profile |
| :--- | :--- | :--- |
| `principal_agent` | `IMPLEMENTATION_PLAN.md` | Owns the Phase 1 deliverable and the Approval Gate |
| `orchestrator` | this sprint directory, `task_scope.md`, `PHASE_REGISTER.md` | Owns sprint hierarchy instantiation |
| `doc_orchestrator` | roadmap, `ADR-0002`, both workflows, `CHANGELOG.md` | Owns documentation and contracts |
| `rule_validator` | `agents.md` §5 amendment | Constitutional edits are its jurisdiction |
| `devops_agent` | `scripts/detect_drift.py`, `scripts/branch_sovereignty.py`, `.gitignore`, `Makefile` | Closest owner of tooling and environment. **`F-021-A2` is the real reason this is a workaround**: no profile holds `Write` for `scripts/` or `hooks/`, so there is no correct assignee to name |
| `tester_agent` | `tests/test_session_protocol.py` | Owns test authorship and the second gate |
| `qa_agent` | — | Structural verification ran as `make verify` (127 tests, ruff-equivalent compile checks, reference integrity), not as a dispatched role |

## Structural gap this sprint did not close

`F-021-A2`: seven profiles hold `Write`/`Edit` and all seven are documentation,
governance or skill roles. **For `scripts/` and `hooks/` there is no owner at
all.** Sprint `023` `C5` widens `devops_agent`; splitting a code-implementer
profile is a redesign of the role map and is out of scope here. Declared, not
resolved.
