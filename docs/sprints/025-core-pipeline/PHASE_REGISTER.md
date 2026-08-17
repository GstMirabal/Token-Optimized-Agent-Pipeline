# Phase Register — Sprint 025 (`jurisdiction`)

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory |
| 2 · Environment | `venv_skillopt/` present | ✅ verified |
| 3 · Roadmap Drafting | branch `ai-sprint/025` from `ai-sprint/024` | ✅ `RA-12` |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory |
| 5 · Approval Gate | Human authorisation | ✅ granted as an explicit scope choice: *"sprint propio, el siguiente"*, naming the script, the host hook, the `agents.md §3` rule and the determinism warning |
| 6 · Execution | `J1`-`J6` | ✅ |
| 7 · Quality Gate | `make verify` green | ✅ 137 tests, installer sandbox, self-bridge, determinism scan |
| 8 · Closeout | `CHANGELOG.md`, records, anchor | ⏳ |

## Gate rounds

| Gate | Round | Verdict |
| :--- | :--- | :--- |
| Test (`pytest`) | 1 | **REJECTED** — `test_host_sprint_records_written_into_the_submodule_are_refused`: the guard reported `?? docs/` instead of the offending file, because `--porcelain` collapses untracked trees |
| Test (`pytest`) | 2 | **PASSED** — 33/33 in this file, 137/137 across the suite |
| Structural (`make verify`) | 1 | **PASSED** |

**The single rejection is the one worth keeping.** The verdict was already
correct — exit `2` either way — and only the message was useless. A guard that
blocks correctly while telling the operator nothing actionable is a guard that
gets worked around, and no review pass would have caught it: the assertion had to
read what a human reads.

## Deviation

Delegation forbidden by session configuration; reported before Phase 1 and
authorised. See `agent_assignment.md`.
