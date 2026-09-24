# Phase Register — Sprint 050 (`deterministic-quality-instrument`)

What `close_workflow.md` Phase 2.6 `double_gate_evidence` reads to answer the
one question no other control asks: **did this phase actually happen?**

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory, committed `5f1b174` before Phase 5. `audit_plan.py` exit `0` at draft and at approval |
| 2 · Environment | `venv_skillopt/` present | ✅ 780 tests pass at start; no dependency added (`Dependencies: None`) |
| 3 · Roadmap Drafting | `SPRINT_LOG.md` + branch `ai-sprint/050` | ✅ this directory; branch cut from `main` at `753fbe1` before any commit (`RA-12`) |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory; no agent forged |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory; no skill forged — a fresh script was the correct call, confirmed by ladder |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory; `check_task_scope.py` exit `0` |
| 5 · Approval Gate | Human authorisation, attended | ✅ GstMirabal (`gst.mirabal@gmail.com`), 2026-09-20, attended. Plan committed before approval; stamp on `35c3863` |
| 6 · Execution | Atomic commits on `ai-sprint/050` (`RA-08`) | ✅ 11 of 11 planned units (`U1`-`U10` + `U2a`) landed. `make verify` exit `0` throughout |
| 7 · Quality Gate | QA row + Tester row in `SPRINT_LOG.md` | ✅ Round 1: both `RECORD`/`testifying`. Rounds 2-3: both gates `REJECTED`/`charter` on the JS/TS scanner path — four consecutive rejections escalated to `workflows/remediation_workflow.md`. Human chose **Abort criterion 1** (pre-declared in the plan): JS/TS scanner withdrawn rather than shipped defective. Python path never rejected |
| 8 · Closeout | Ledger, roadmap, anchor, graph | ✅ this close |

## Outcome

**Delivered**: `scripts/quality_audit.py`, a deterministic function-length and
nesting-depth auditor for **Python**, closing the four `agents.md §1` rows
Sprint 049 found crediting two skills with a measurement they don't perform
(`F-049-7`). `scripts/session_state.py set-topology` gives `topology_version`
a real writer instead of leaving it to prose, invoked from both
`close_workflow.md` and `deployment_workflow.md`. `agents.md §1` now names
real, gate-verified instruments for Python and states plainly that none
exists for JS/TS.

**Not delivered**: the JS/TS half of the same instrument. Built, gated, and
withdrawn (`AB1`, `IMPLEMENTATION_PLAN.md`'s pre-declared Abort criterion 1)
after three remediation rounds each found a new silent-compliance defect
family in a stdlib-only brace-depth scanner — the last two present since the
instrument's first commit, not regressions from remediation. `quality-audit`
was never wired into `make verify` (`D5` Branch B), so no CI or gate path
depended on the withdrawn guarantee; what failed was a documentation claim,
corrected in the same act it was withdrawn.

**`make verify` exit `0` at HEAD; `pytest` 805 passed** (780 baseline + 25
net new, after the JS/TS test suite was added and then removed with the
scanner it tested).

**Recorded for Extract (Phase 8/`/agents:extract`), not applied here**, all
`routing_class: nucleus` proposals pending human confirmation at
`close_workflow.md` Phase 2.5:
- `KI-050-1`: `orchestrator`'s Phase 3 toolset can't run `session_cost.py` — the split-profile handoff (session completes what the profile can't) is the durable lesson.
- `KI-050-2`: `rule_validator`/`doc_orchestrator`'s declared toolset (`Read, Glob, Grep, Write, Edit`) can't commit or run `make verify` — seven dispatches across this sprint hit it. Either grant `Bash` or document the session-side handoff as the default.
- `KI-050-3`: this framework's own documents disagree on the remediation-escalation threshold ("third" vs. ">3" rejection).
- `KI-050-4`: `remediation_workflow.md`'s `state_nuke` promises "Pre-Sprint pristine" but its literal command only clears uncommitted changes.
- `KI-050-5`: `remediation_workflow.md` has no exit procedure once a human lifts the lock.
- `KI-050-6`: JS/TS complexity measurement, re-planned as its own sprint. The five failure families both gates found by hand (arrow over-detection, unenclosed module-level callbacks, nested-arrow depth loss, control-keyword method names, regex-literal masking desync) are that sprint's acceptance-test corpus — a stronger starting point than a fresh sprint would otherwise have.
- 91 pre-existing Python complexity violations, baseline measured at `80bb5e1..43e60b3` (`D5` Branch B), reproduced smaller (87) after the JS/TS withdrawal removed some of the scanner's own violating code.
