# Phase Register — Sprint 022 (`model-tiering`)

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory |
| 2 · Environment | `venv_skillopt/` present | ✅ verified |
| 3 · Roadmap Drafting | `022-model-tiering.md` + branch `ai-sprint/022` | ✅ `RA-12` |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory |
| 5 · Approval Gate | Human authorisation | ✅ granted per step, attended throughout |
| 6 · Execution | 4 commits on `ai-sprint/022` (`RA-08`) | ✅ |
| 7 · Quality Gate | `make verify` green | ✅ 161 tests, installer sandbox, self-bridge |
| 8 · Closeout | `CHANGELOG.md`, records, anchor | ✅ this commit |

## Gate rounds

| Gate | Round | Verdict |
| :--- | :--- | :--- |
| **QA Agent** (structural, `make verify`) | 1 | **PASSED** — reference integrity, determinism scan, manifest parity, both new gates |
| **Tester Agent** (functional, `pytest`) | 1 | **PASSED** — 161/161, 10 new in this sprint |

## The abort criterion that did not fire

**If a subagent failed to start on the new frontmatter, the sprint reverted** —
thirteen broken profiles would leave the pipeline with no roles. It did not fire:
13/13 parse with all five keys, and `.claude/agents/*.md` are symlinks, so no host
needs a bridge reinstall to pick the change up.

## Two design defects the gates did not catch, and verification did

Recording these because a clean gate run is not the same as a correct design:

1. **The parser attributed one model's retirement to another.** `make verify` would
   have passed on a *broken* map, because nothing compared the parse against the
   real file. Found by parsing the actual catalogue rather than a fixture I wrote.
2. **The gate would never have fired in CI.** Every check would have reported green,
   forever, because the file it read is absent there. Found by asking where that
   file actually lives — `RA-16`'s exact concern, inside the sprint building the gate.

Neither is visible to a passing test suite. Both are now covered: the hermetic
fixture reproduces the phrasing table, and the gate reads the committed snapshot.

## Deviation

Delegation forbidden by session configuration; reported before Phase 1 and
authorised. See `agent_assignment.md`.
