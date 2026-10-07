# Phase Register — Sprint 054 (`host-intake-gates-and-sprint-state`)

No `PHASE_REGISTER_TEMPLATE.md` exists in `docs/standards/templates/` — still open as
`KI-052-8`, not invented for this file. Built from `config/artifact_registry.json`
(entry `PHASE_REGISTER.md`: Phase 8, writer `doc_orchestrator`, `required: false`) and
from `SPRINT_LOG.md`, `IMPLEMENTATION_PLAN.md` and `task_scope.md` of this directory,
following only the section shape of `docs/sprints/053-core-pipeline/PHASE_REGISTER.md`.
Commit range of the sprint: `d848302..1d39380` (67 commits, branch `ai-sprint/054`).

| Phase | Deliverable | Evidence (path / SHA) | Verdict / Status | Deviations |
| :--- | :--- | :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | `docs/sprints/054-core-pipeline/IMPLEMENTATION_PLAN.md`, drafted `a796992`, committed before Phase 5; scope chosen by the human (GstMirabal) on 2026-10-04: blocks A, B, C in, block D (sandbox) to Sprint 055, block E (nucleus residue) to Sprint 056 | Complete | A host handoff was checked against `v4.35.0` while the nucleus had sealed `v4.36.0`; every finding id re-measured against `d848302` before planning, all still open except `F-103-N1` (already closed by `F-BOOT-2`) |
| 2 · Environment Readiness | none (precondition) | No dedicated `devops_agent` entry in `SPRINT_LOG.md`; the precondition is evidenced by Phase 6 (`make verify` exit `0` at `dde2088`) and Phase 7 | Satisfied | No explicit Phase 2 line in `SPRINT_LOG.md` |
| 3 · Roadmap Drafting | `SPRINT_LOG.md` + branch `ai-sprint/054` | `SPRINT_LOG.md` opened from the template `139e693`; branch `ai-sprint/054` cut from `main` (`RA-12`); intake records `225aaee` (host intake, measured against `v4.36.0`) and `903b04e` (blocks D and E routed to Sprints 055 and 056) | Complete | None recorded |
| 4.1 · Agent Assignment | `agent_assignment.md` | `83caf76` | Complete | Phase 4.1 and 4.3 subagents held no `Bash`; the parent session ran `check_forge_ladder.py` and `check_task_scope.py` and read exit `0` for both |
| 4.2 · Skill Assignment | `skill_assignment.md` | `c2951eb` | Complete | None recorded |
| 4.3 · Rule Audit | `task_scope.md` | `ad61cf6`; rule-audit findings applied to the plan `5d1b8da`; `scripts/check_task_scope.py` exit `0` (parent session) | Compliant after the plan fix | Ten small edit units (A04, A06, C01, C02, A13, B06, B07, B08, C03, C04) staffed to Bash-less or doc profiles were executed by the parent session under that profile's ruleset, one single-subject commit each, as `pipeline_workflow.md` Phase 4.1 requires when a writer is not dispatched |
| 5 · Approval Gate | none (human authorization) | Approved by GstMirabal against plan commit `5d1b8da`; recorded `dc9f740` | `APPROVED` — `triple_lock` lock 1 | Single attended invocation. Later human decisions: the `F2` deviation acknowledgement and the option A re-plan (see Human decisions) |
| 6 · Execution | Atomic commits on `ai-sprint/054` | Wave A `46d07cf`..`9d2c1ef` (gates that pass without measuring); `bcdb4ac` (README count). Wave B `23b8b48`..`590fb6a` (session and sprint state). Wave C `d01045b`..`dde2088` (supply chain, step map). Records `062b02f`, `65bf38b`. Outcome: `make verify` exit `0` at `dde2088`; full suite 992 passed after Wave A, 1024 passed at head | Complete | A14 (`bcdb4ac`) and `f0e829d` added unplanned README script-count bumps because `check_readme_counts.py` (inside `make verify`) failed after `check_fix_reproduces.py` and `install_lock.py` were added; A02 (`8f13941`) gave six fixtures in `tests/test_code_craft_gates.py` a `Repro:` trailer in the same commit; `make verify` was red only on the stale step map between Wave A and `C04`, as expected |
| 7 · Quality Gate | Five rows in `SPRINT_LOG.md` (`Gate \| Round \| Verdict \| Class \| Notes`) | See Gate history below | QA Gate 1 `REJECTED` x3 then `RECORD` (`testifying`) at R4; Tester Gate 2 `RECORD` (`testifying`) at R1 | Third consecutive `REJECTED` with a second `remediation-regression` label: the block was stopped for a human-approved re-plan instead of `remediation_workflow.md` (`KI-054-3`). Tester Gate 2 was resumed once after an API rate-limit cut, no verdict lost |
| 8 · Sprint Closeout | `PHASE_REGISTER.md` (Z01 `38879bb`), `CHANGELOG.md` `[Unreleased]` (Z02 `798fa31`), host findings ticked on re-measurement (Z03 `c606577`), `KI-053-1`/`KI-053-4` delivered (Z04 `592a4eb`) | `close_workflow.md`: footers aligned (`3bd6103`, `ee86ded`); `graph_stats.json` 12841/17475/1037 (`51ec80f`); `docs-freshness-check` exit 0 (3 pre-existing WARN); model ledger regenerated (`9fe2046`); `repo_docs_check` — `CONTRIBUTING.md` updated for the `Repro:` gate (`b1e6d94`), `SECURITY.md` unchanged, `NOTICE.md` applies (vendored skills) and unchanged; `rules_optimization` skipped: skillopt stack absent; extract candidates human-confirmed and routed (`3a68d8a`), `memory_index.json` stamped (`4104b7c`); `memory_wipe` no-op (no `memory/` in the nucleus); Phase 2.6 `check_task_scope` 0, `check_gate_log` 0; platform recheck clean | Complete | — |

## Gate history (Phase 7)

| Gate | Round | Verdict | Class | Range | Evidence | What the round changed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| QA Agent (Gate 1) | 1 | `REJECTED` | `charter` | `d848302..65bf38b` | Transcribed `097b4f3`; ruff 0, quality_audit 0, make verify 0. Findings F1 (high) through F8 | F1: replay read a missing pytest as a red parent (`d64fb37`, `d93471a`, `f6ebfb0`); F2: unsatisfiable `npmrc` Verification row (`1a79a2a`, `e3f5483`); F3: nucleus-only fix hints (`c56bc88`, `9c78f26`); F4-F6, F8 (`d9035fe`, `44fa69b`, `cfeada3`); F7 (`e78ec2b`) |
| QA Agent (Gate 1) | 2 | `REJECTED` | `instructing` | `d848302..e3f5483` | Transcribed `cf7e7b7`; replay 7/7 OK, ruff 0, quality_audit 0, make verify 0 (1022 passed). `R2-1` carries label `remediation-regression` (1st) | `5a6488b`, `240043f` (`R2-1`); `a5872e6` (`R2-2`); `R2-3` accepted as duplication (`a0bc8ca`); `R2-4` opened as `KI-054-2` (`15a005e`) |
| QA Agent (Gate 1) | 3 | `REJECTED` | `instructing` | `d848302..a0bc8ca` | Transcribed `de13418`; replay 8/8 OK, make verify 0 (1024 passed). `R3-1` carries label `remediation-regression` (2nd) | Third consecutive `REJECTED` and second label: escalated to the human, re-plan recorded `12e0f9c` |
| QA Agent (Gate 1) | 4 | `RECORD` | `testifying` | `d848302..0c7d9b1` | Transcribed `706031e`; replay 8/8 OK, ruff 0, quality_audit 0, make verify 0 (1024 passed); verdict sentence byte-identical in three files | Re-plan commits `d3d1e10`, `242657f`, `f300a9f`, `e169375`, `0c7d9b1`; `R4-1` fixed by `9d8b7f6` (`KI-054-3` list completed) |
| Tester Agent (Gate 2) | 1 | `RECORD` | `testifying` | `d848302..9d8b7f6` | Transcribed `48aaad2`; full suite 1024 passed, make verify 0; base suite in a worktree 945 passed + 1 known worktree-only failure (`KI-052-4`); replay 8/8 OK plus an independent `PASSES_ON_PARENT` negative control | `T2-1` addressed after the verdict by the test-only commit `ac37f3e` (11 failed with `scripts/install_lock.py` moved away, 11 passed restored; no source change, no re-gate); Phase 7 closed `1d39380` |

## Human decisions

| Date | Decision | Where recorded |
| :--- | :--- | :--- |
| 2026-10-04 | Scope: blocks A, B, C in this sprint; block D to Sprint 055; block E to Sprint 056 (E decided 2026-10-05 in the program queue) | `903b04e`, `IMPLEMENTATION_PLAN.md` `## Out of scope` |
| Phase 5 (date not recorded in the sprint directory) | Approval of the plan at commit `5d1b8da` | `dc9f740` |
| 2026-10-05 | Acknowledged the approved-plan deviation from QA Gate 1 `F2`: the Verification row `git grep -n "npmrc" -- agents.md rules workflows` restated from "no output" to "every hit states that `.npmrc` does not carry the §8 keys" | `1a79a2a`, `e3f5483` |
| 2026-10-05 | Option A at QA Gate 1 round 3: re-plan the replay instruction block instead of entering `remediation_workflow.md`'s `TERMINAL_REMEDIATION_LOOP` | `12e0f9c` |

## Known items opened (extract candidates)

All three are transcribed in `docs/roadmaps/core/pipeline/021-030-program-queue.md`
(section *Still open for a later program — routed out of Sprint 054*).

| KI | Finding | `routing_class` | Opened by |
| :--- | :--- | :--- | :--- |
| `KI-054-1` | `scripts/check_fix_reproduces.py` replays `pytest` only; a staged test file with no runner (`.ts`, `.js`) is `UNREPLAYED` (exit `2`) unless the commit carries `Repro: manual — <SPRINT_LOG section>`; a JS/TS host has no automated replay | `nucleus` | Plan Design `D3` (`0747911`) |
| `KI-054-2` | Phase 7 gate commands are written only in nucleus form in `agents/qa_agent.md`, `workflows/pipeline_workflow.md` Phase 7 and `rules/code_craft.md` §6; from a host root the paths do not resolve | `nucleus` | QA Gate 1 round 2 `R2-4` (`15a005e`) |
| `KI-054-3` | Two escalation thresholds for one rejection count: `pipeline_workflow.md` Phase 7 escalates at the third `REJECTED`, `remediation_workflow.md` Phase 0 triggers at `>3`; further variants in `rules/qa_and_testing.md:12`, `workflows/reconciliation_workflow.md:15`, `agents/principal_agent.md:24`, `agents.md:150`, `agents.md:27` | `nucleus` | QA Gate 1 round 3 (`e169375`), list completed at round 4 `R4-1` (`9d8b7f6`) |

Friction recorded for `extract_workflow.md` without a KI: a gate that must run under an
edited agent profile is dispatched from a session started after that edit is committed
(QA Gate 1 round 4 `R4-2`; a session loads agent definitions once).
