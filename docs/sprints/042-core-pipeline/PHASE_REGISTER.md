# Phase Register — Sprint 042 (`template-gate-parity`)

What `close_workflow.md` Phase 2.6 `double_gate_evidence` reads to answer the
one question no other control asks: **did this phase actually happen?**

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory, committed `adc4162` **before** Phase 5 approved it (`triple_lock` lock 1). `audit_plan.py` exit `0` at Phase 1 and again after the Phase 3.5 Cost update |
| 2 · Environment | `venv_skillopt/` present | ✅ Python 3.13.13, pytest 9.1.1. No Docker/DB in scope; `.env` never read (`RA-09`) |
| 3 · Roadmap Drafting | `SPRINT_LOG.md` + branch `ai-sprint/042` | ✅ this directory; branch cut from `main` at `e29ac98` before any commit (`RA-12`), later rebased onto `hotfix/H-006` |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory; `check_forge_ladder.py` exit `0` |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory; ladder terminates at P1, no skill forged |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory; `check_task_scope.py` exit `0` with Model/Effort |
| 5 · Approval Gate | Human authorisation, attended | ✅ GstMirabal, 2026-08-31, over plan commit `adc4162`. Fresh-context Phase 7 gates authorised as a **standing** preference, not per sprint |
| 6 · Execution | Atomic commits on `ai-sprint/042` (`RA-08`) | ✅ 9 units + 3 remediation commits; every message carries `#042` |
| 7 · Quality Gate | QA row + Tester row in `SPRINT_LOG.md` | ✅ 4 rounds. `check_gate_log.py` and `check_role_artifact.py` (both roles) exit `0` |
| 8 · Closeout | Ledger, roadmap, audit, anchor, `graph_stats.json` | ✅ this close |

## Units and gate rounds

Seven units planned; **nine executed**. U8/U9 were opened by a Phase 7 scope
amendment recorded in `task_scope.md` before either file was touched — `ADR-0012`
superseded rather than edited, because `rules/documentation_standard.md §3`
forbids an in-place edit of an Accepted ADR.

| Unit | File | Commit |
| :--- | :--- | :--- |
| U1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | `f84dd3c` |
| U2 | `config/template_gates.json` | `57f184a` |
| U3 | `scripts/check_template_gates.py` | `1c2e88c` |
| U4 | `Makefile` | `0fb5f03` |
| U5 | `tests/test_check_template_gates.py` | `63a4c6f` |
| U6 | `README.md` | `4a60e93` |
| U7 | `docs/decisions/ADR-0012-template-gate-parity.md` | `5181761` |
| U8 | `docs/decisions/ADR-0013-declaration-containment.md` | `d7022c2` |
| U9 | `ADR-0012` `Status` line | `81d2adf` |
| — | Gate 1 remediation, rounds 1 and 2 | `3cefba8`, `c763d41` |
| — | Gate 2 remediation | `799a2d7` |

**Four gate rounds, not two.** Two of them found the sprint's real defects:

| Gate | Round | Verdict | What it cost, and what it bought |
| :--- | :--- | :--- | :--- |
| QA | 1 | `REJECTED` | A name-prefix test standing in for containment, and an unvalidated render map. The bypass was the **documented** `<host-root>/.agents-profile/` layout |
| QA | 2 | `REJECTED` | The anchor of the containment check was itself unvalidated input, so the target guard passed vacuously |
| QA | 3 | `RECORD` | Boundary held under constructed attack; two residuals left open **with stated reasons** |
| Tester | 1 | `RECORD` | All 11 guards mutation-proven; pre-041 templates reconstructed and the instrument caught the historical defects verbatim; `gate_exceptions` found inert |

The sprint was **green through rounds 1 and 2** — `make verify` exit `0`, full
suite passing, `ruff` clean, its own abort criterion satisfied. Those instruments
measure what the shipped declaration asks for; both defects lived in what the
checker would have permitted. That asymmetry is now written into
`rules/qa_and_testing.md §3.1`.

## Opened and closed inside this sprint, on its own branch

**Hotfix `H-006`** (`docs/hotfixes/H-006-tests.md`). `make verify` and CI went red
on `main` on 2026-09-01 with nothing committed: a test fixture written as an
absolute instant, tested against a 7-day relative TTL. Repaired on `hotfix/H-006`
(`ebcc15b` `dd9f2db` `8e05f00`), **not folded into this sprint as a rider**;
`ai-sprint/042` was rebased onto it. Both Double-Gate agents had measured
`make verify` at exit `0` earlier and were right when they measured.

## The close's own findings

| Event | Disposition |
| :--- | :--- |
| `docs_freshness_check` `BLOCK` at Phase 1 (delta `2662` vs p90 `2433`) | `/agents:audit` actually run — `docs/audits/PIPELINE_AUDIT_REPORT-042.md` — rather than incrementing `last_audit_sprint`, which no workflow owns. The nucleus asymmetry is routed as `T4` |
| Hard token bound crossed (`15.3×`, cycle 4) | `IMPLEMENTATION_PLAN.md` `## Cost` updated before the close continued, as that section required of itself |
| `docs/walkthroughs/` absent in the nucleus | Accepted gap recorded in `docs/active_state.json` `acknowledged_gaps.walkthroughs`, human-accepted 2026-09-02 |
| Six Knowledge Items, all `nucleus`-class | Four written into `rules/` (`9e7c39c`); `K3` embodied in `ADR-0013`; `K6` drafted as `T4`. No `memory_index.json` entry — `index_update` indexes `host`-class only |
