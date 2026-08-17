# Phase Register — Sprint 021 (`cost-instrumentation`)

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory, `6276a50` |
| 2 · Environment | `venv_skillopt/` present | ✅ verified |
| 3 · Roadmap Drafting | `021-cost-instrumentation.md` + branch `ai-sprint/021` | ✅ `6276a50`, `RA-12` |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory |
| 5 · Approval Gate | Human authorisation | ✅ granted per commit, attended throughout |
| 6 · Execution | 5 commits on `ai-sprint/021` (`RA-08`) | ✅ `6276a50` → `862d6b7` |
| 7 · Quality Gate | `make verify` green | ✅ 151 tests, installer sandbox, self-bridge |
| 8 · Closeout | `CHANGELOG.md`, records, anchor | ✅ this commit |

## Gate rounds

| Gate | Round | Verdict |
| :--- | :--- | :--- |
| **QA Agent** (structural, `make verify`) | 1 | **REJECTED** — `map_workflows.py --check`: the generated step map went stale when two workflows were edited |
| **QA Agent** (structural, `make verify`) | 2 | **PASSED** — regenerated in the same commit, since the check compares byte for byte |
| **Tester Agent** (functional, `pytest`) | 1 | **PASSED** — 151/151 across the suite, 14 new in this sprint |

## The abort criteria that did not fire

Two were declared, and both were tested rather than assumed:

- **The segmenter must reproduce the four cycles of the drafting session.** It does — 38.3x, 44.9x, 14.0x, 30.0x. Had it not, everything above it rested on it and the sprint reverted.
- **`suspend` must not launder unrecorded work.** `test_suspend_does_not_launder_unrecorded_work` proves it hermetically: after suspending, `detect_drift` still reports the drift. Had it passed clean, the new state would have broken the detector Sprint `024` repaired.

## Deviation

Delegation forbidden by session configuration; reported before Phase 1 and
authorised. Phases 4.1–4.3 produced their artifacts under the governing
profiles' rulesets rather than by dispatch. See `agent_assignment.md`.
