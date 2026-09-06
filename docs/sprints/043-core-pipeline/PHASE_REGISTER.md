# Phase Register — Sprint 043 (`submodule-runtime-parity`)

What `close_workflow.md` Phase 2.6 `double_gate_evidence` reads to answer the
one question no other control asks: **did this phase actually happen?**

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory, committed `82e9644` **before** Phase 5 approved it (`triple_lock` lock 1). `audit_plan.py` exit `0` at Phase 1 and again at Phase 5 (`bf3ef04`) |
| 2 · Environment | `venv_skillopt/` present | ✅ Python 3.13.13; `venv_skillopt/bin/python -m graphify` exit `0`. No Docker/DB in scope; no `.env` present (`RA-09` moot) |
| 3 · Roadmap Drafting | `SPRINT_LOG.md` + branch `ai-sprint/043` | ✅ this directory; branch cut from `main` at `d7b0d77` before any commit (`RA-12`) |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory; `check_forge_ladder.py` exit `0`; no agent forged |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory; ladder terminates at P1, no skill forged |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory; `check_task_scope.py` exit `0` with Model/Effort (`sonnet`/`medium`, all six units `author`-tier) |
| 5 · Approval Gate | Human authorisation, attended | ✅ GstMirabal, 2026-09-06, over plan commit `82e9644`. Fresh-context Phase 7 gates dispatched clean (standing preference) |
| 6 · Execution | Atomic commits on `ai-sprint/043` (`RA-08`) | ✅ 6 planned units + bookkeeping + 1 Gate-2 remediation commit; every message carries `#043` |
| 7 · Quality Gate | QA row + Tester row in `SPRINT_LOG.md` | ✅ QA round 1 + Tester rounds 1–2. `check_gate_log.py` and `check_role_artifact.py` (both roles) exit `0` |
| 8 · Closeout | Ledger, roadmap, anchor, graph | ✅ this close |

## Units and gate rounds

Six units planned; **six executed** (no scope amendment).

| Unit | File | Commit |
| :--- | :--- | :--- |
| D1 | `scripts/check_venv_relocatable.py` | `1f89eb4` |
| D2 | `tests/test_check_venv_relocatable.py` | `410eba3` |
| A2 | `rules/graphify.md` | `caa8bfc` |
| A1 | `workflows/start_workflow.md` | `8abffe2` |
| C1 | `agents.md` | `d3227f4` |
| C2 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | `06e376c` |
| — | Phase 5 approval record | `76c5e4c` |
| — | Bookkeeping (task_scope ✅, test rename, README 38→39, path genericization) | `f3be5f3`, `da2d158` |
| — | QA-043-1 fix (`agents.md` §4 self-reference accuracy) | `422efd0` |
| — | Gate-2 round-1 remediation (`check_venv_relocatable.py` + test, one atomic `fix(` commit) | `96e3303` |

## Gate rounds

| Gate | Round | Verdict | Class | What it cost, and what it bought |
| :--- | :--- | :--- | :--- | :--- |
| QA | 1 | `RECORD` | `testifying` | 9/9 structural checks green. Finding QA-043-1: `agents.md:99` claimed `§3 strict_rule` pointed to §4 (it does not) and that `§3 jurisdiction` / `extract_workflow.md` did not restate (they do). Fixed in-sprint at `422efd0`. `RECORD` does not bounce (`RA-17`) |
| Tester | 1 | `REJECTED` | `charter` | `check_venv_relocatable.py` false-positived a correctly-located fresh venv whenever the checkout path contains whitespace; the printed `python3 -m venv --clear` remedy regenerated the failing condition — an infinite loop at `start_workflow.md` Phase 0. Suite was green (684) and the sprint's own abort criterion held **for this checkout** — the defect lived in what the check would accept, not in what it was given (`rules/qa_and_testing.md §3.1`) |
| Tester | 2 | `APPROVED` | — | Fix `96e3303` verified at origin: round-1 scenario re-run from scratch — spaced venv exit `0`, genuine relocation at a spaced path exit `2`, remedy converges. `pytest tests/` 688 passed; `make verify` exit `0`; `test_installer.sh` 6/6 |

Two Tester rounds, not one; round 1 found the sprint's real defect. Not the third
consecutive `REJECTED` of the same block, so no escalation to
`remediation_workflow.md`.

## The close's own findings

| Event | Disposition |
| :--- | :--- |
| Anchor `current_sprint.status = CLOSED` while session `IN_PROGRESS` | Advisory at `/agents:start`; `current_sprint` fields moved to Sprint 043 at this close's State Sync (`close_workflow.md` Phase 4) |
| `make verify` `--current-sprint` gates resolved to Sprint **042** (anchor still `id: 42` during execution) | Compensated by running `check_gate_log` / `check_task_scope` / `audit_plan` against `--sprint-dir docs/sprints/043-core-pipeline` explicitly — all exit `0`. Pre-existing framework behaviour (`session_probe.py` flags it advisory), not a 043 regression |
| `check_venv_relocatable.py:75` `str(venv)` disjunct is loose under a relative `--venv` | Unreachable from the shipped invoker (`start_workflow.md:25`, absolute default); `_console_script_problem` covers the gap. Recorded in `SPRINT_LOG.md` and the roadmap as a `/agents:extract` candidate |
| `docs/walkthroughs/` and per-module Blueprints absent in the nucleus | Accepted gaps in `docs/active_state.json` `acknowledged_gaps` — no new member to inaugurate the hierarchy |
