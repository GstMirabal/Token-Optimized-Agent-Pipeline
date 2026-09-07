# Phase Register — Sprint 044 (`session-start-drift-cigate-host-parity`)

What `close_workflow.md` Phase 2.6 `double_gate_evidence` reads to answer the
one question no other control asks: **did this phase actually happen?**

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory, committed `9ae69aa` **before** Phase 5 approved it (`triple_lock` lock 1). `audit_plan.py` exit `0` at Phase 1, again after the Gate-1 C-2 edit (`2baa07c`), again at Phase 5 |
| 2 · Environment | `venv_skillopt/` present | ✅ Python 3.13.13; `pytest` 688 baseline. No Docker/DB in scope; no `.env` present (`RA-09` moot) |
| 3 · Roadmap Drafting | `SPRINT_LOG.md` + branch `ai-sprint/044` | ✅ this directory; branch cut from `main` at `2bbfa60` before any commit (`RA-12`). Extract backfill for 042/043 committed `881943c` |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory; `check_forge_ladder.py` exit `0`; no agent forged |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory; ladder terminates at P1, no skill forged |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory; `check_task_scope.py` exit `0` with Model/Effort (`sonnet`/`medium`; U3 `opus`/`high` by `tier_escalation`). Two plan deviations recorded |
| 5 · Approval Gate | Human authorisation, attended | ✅ GstMirabal, 2026-09-06, over plan commit `9ae69aa`. Fresh-context Phase 7 gates dispatched clean (standing preference) |
| 6 · Execution | Atomic commits on `ai-sprint/044` (`RA-08`) | ✅ 12 units in 8 unit commits (`fix(` units paired code+test per `rules/code_craft.md §6`; `build(` for the Makefile) + bookkeeping; every message carries `#044` |
| 7 · Quality Gate | QA row + Tester row in `SPRINT_LOG.md` | ✅ QA rounds 1–2 (`REJECTED`/`charter` → `RECORD`/`testifying`), Tester round 1 (`RECORD`/`testifying`). `check_gate_log.py` and `check_role_artifact.py` (both roles) exit `0` |
| 8 · Closeout | Ledger, roadmap, anchor, graph | ✅ this close |

## Units and gate rounds

Twelve units planned; **twelve executed** (no scope amendment; two recorded plan
deviations, both documentary).

| Unit | File | Commit |
| :--- | :--- | :--- |
| U1 + U2 | `scripts/session_start.py` + `tests/test_session_start.py` (F-BOOT-1) | `a0cf769` |
| U3 + U4 | `scripts/session_start.py` + `tests/test_session_start.py` (F-BOOT-2) | `a2fcdbb` |
| U5 + U6 | `scripts/ci_gate.py` + `tests/test_ci_gate.py` (F-BOOT-3) | `53786db` |
| U12 | `docs/decisions/ADR-0014-...md` | `8de8eb7` |
| U7 + U8 | `scripts/detect_drift.py` + `tests/test_detect_drift.py` (F-BOOT-4) | `502b5a9` |
| U9 | `Makefile` (C5) | `aa69f08` |
| U10 + U11 | `scripts/check_venv_relocatable.py` + `tests/test_check_venv_relocatable.py` (C6) | `44e0e65` |
| — | Bookkeeping (task_scope ✅, SPRINT_LOG progression + harvest) | `44b26fe` |
| — | Gate-1 C-1 remediation (`refactor`: extract `_record_not_inspectable`, `resolve_inputs` 53 → 47 lines) | `daa40ed` |
| — | Gate-1 C-2 remediation (plan / task_scope / ADR reconciled to HTTP 403) | `2baa07c` |
| — | Gate verdict transcriptions + last F-BOOT-3 label fix (`skill_assignment.md`) | `7d0c331`, `eac3852`, `3f1120e` |

## Gate rounds

| Gate | Round | Verdict | Class | What it cost, and what it bought |
| :--- | :--- | :--- | :--- | :--- |
| QA | 1 | `REJECTED` | `charter` | **C-1**: `resolve_inputs` grew to 53 lines — `ci_gate.py`'s first breach of `agents.md §1 max_lines_per_func` (50). **C-2** (`RA-14`): the approved plan said "403/404" at three acceptance-bearing sites while implementation, tests and `ADR-0014` were HTTP-403-only. Both structural; no logic change implied |
| QA | 2 | `RECORD` | `testifying` | Both findings independently verified resolved (AST: `resolve_inputs` 47 lines; plan carries zero `404` acceptance claims; `task_scope.md` deviation row present). One residual: `skill_assignment.md:38` still read "403/404" in a unit *label* — fixed `eac3852`. `RECORD` does not bounce (`RA-17`) |
| Tester | 1 | `RECORD` | `testifying` | Own worktree at `2bbfa60`: 10/13 new tests red (3 are F-BOOT-4 negative controls, correctly green pre-fix). F-BOOT-2 additionally proven with a real `git submodule add` fixture. **11/11 mutations caught**, 5 of them over-broad (`rules/qa_and_testing.md §3.1`). Suite 688 → 701, `git diff main...HEAD -- tests/` removes only 3 mock-signature lines forced by the new `cwd` kwarg. C5 verified by execution. One `testifying` finding → Sprint 045 |

Not a third consecutive `REJECTED` of any block; `remediation_workflow.md` not
invoked.

## The close's own findings

| Event | Disposition |
| :--- | :--- |
| Anchor `current_sprint.status = CLOSED` while session `IN_PROGRESS` | Advisory at `/agents:start`; `current_sprint` opened to Sprint 044 / `IN_PROGRESS` at Phase 3 (untracked local state, `.gitignore:55`) |
| **`session_start.py:56` `load_anchor` still reads the framework anchor for the briefing in submodule mode** | Sprint 045 candidate. F-BOOT-2 fixed the *write* (claim/probe now host-scoped); the *read* is one function over. Post-fix `/agents:start` in a host prints "docs/active_state.json: absent or unreadable" over a live host anchor. Plan pre-authorised this exact routing (`task_scope.md` Out-of-scope). Recorded in `docs/roadmaps/core/pipeline/021-030-program-queue.md` |
| `detect_drift.py` runs from the framework checkout in submodule mode | Sprint 045 candidate, same family as the `load_anchor` read — folded into the one unit above |
| `scripts/_mode.is_nucleus()` returns `False` inside a linked git worktree of the nucleus (a worktree's `.git` is a file) | Pre-existing, untouched by this sprint. Recorded for a framework developer who works in a worktree; queued alongside the Sprint 045 item |
| `ci_gate.py` `_reduce_runs` is 48 lines; `detect_drift.py:75` carries a pre-existing `PLW1510` in the un-edited `git()` helper; `test_session_start.py:102/126` FLY002 | Pre-existing repo-wide ruff debt (193 findings, no on-disk config, not gated by `make verify`) — the Sprint 043 migration exclusion. Not this sprint's to fix |
| `_MIRROR_MARKER` defined mid-file in `session_start.py` rather than the constants block; `Makefile:39` hardcodes the python path where `VENV_PY` exists | Gate-1 testifying style notes; not remediated (testifying does not bounce). Cheap cleanup for a future touch of those files |
| `docs/walkthroughs/` and per-module Blueprints absent in the nucleus | Accepted gaps in `docs/active_state.json` `acknowledged_gaps` — no new member to inaugurate the hierarchy |
