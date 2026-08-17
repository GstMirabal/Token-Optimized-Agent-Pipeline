# Phase Register — Sprint 024 (`close-machinery-verdicts`)

What `close_workflow.md` Phase 2.6 `double_gate_evidence` reads to answer the
one question no other control asks: **did this phase actually happen?**

The precedent is in `CHANGELOG.md [4.4.0]`: a host ran a whole sprint without
Phase 4 and Phase 7, `task_scope.md` was never produced, and nothing raised it
across twelve commits — because every existing control inspected the *content*
of what was written, never whether the phase responsible for it ran.

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory, `30d2fa6` |
| 2 · Environment | `venv_skillopt/` present, `installed.lock` read | ✅ verified, `requirements-core.txt` |
| 3 · Roadmap Drafting | `docs/roadmaps/core/pipeline/024-close-machinery-verdicts.md` + branch `ai-sprint/024` | ✅ `30d2fa6`, `RA-12` |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory |
| 5 · Approval Gate | Human authorisation, attended | ✅ granted before execution; re-granted for the commit-5 scope change |
| 6 · Execution | 5 atomic commits on `ai-sprint/024` (`RA-08`) | ✅ `30d2fa6` → commit `5` |
| 7 · Quality Gate | `make verify` green | ✅ 127 tests, installer sandbox, nucleus self-bridge, reference integrity |
| 8 · Closeout | `CHANGELOG.md` `[Unreleased]`, roadmap sealed, anchor synced | ✅ `abc0ec2` + commit `5` |

## Gate rounds

| Gate | Round | Verdict |
| :--- | :--- | :--- |
| **QA Agent** (structural, `make verify`) | 1 | **REJECTED** — `map_workflows.py --check`: the generated step map went stale when two workflows were edited |
| **QA Agent** (structural, `make verify`) | 2 | **PASSED** — guide regenerated in the same commit, since the check compares byte for byte |
| **Tester Agent** (functional, `pytest`) | 1 | **REJECTED** — 9 failures. Two causes, both worth recording |
| **Tester Agent** (functional, `pytest`) | 2 | **REJECTED** — 1 failure: an assertion that could not fail (`"unsealed work"` contains `"sealed work"`) |
| **Tester Agent** (functional, `pytest`) | 3 | **PASSED** — 23/23, then 127/127 across the suite |

**The first test round is the one that mattered.** Among the nine failures was
`test_commits_after_the_sealed_close_are_drift` — a Phase 019 test, written long
before this sprint — and it **refuted the design**: the `R` verdict was specified
to exit `0` on the grounds that nothing was measurable, which would have passed a
repository with commits after the baseline and no releases at all. That is the
Phase 018 scenario in its early form. `R` now exits `2`.

Recorded as `F-024-D5`: the anti-whitewash principle catching the author of the
anti-whitewash test. A gate proven only on a healthy tree proves nothing — the
lesson `PR #28` left behind, and the reason that test existed to fire.

## Deviation

Delegation was forbidden by session configuration; reported before Phase 1 and
authorised. Phases 4.1–4.3 produced their artifacts under the governing profiles'
rulesets rather than by dispatch. See `agent_assignment.md`.
