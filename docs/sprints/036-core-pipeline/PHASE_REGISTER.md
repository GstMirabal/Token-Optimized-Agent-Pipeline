# Phase Register — Sprint 036 (`core-pipeline`)

What `close_workflow.md` Phase 2.6 `double_gate_evidence` reads: **did this phase actually happen?**

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory (Lock 1 `7ebf251` before Approval Gate) |
| 2 · Environment | `venv_skillopt/` present | ✅ verified (`make verify` 608 pytest + installer) |
| 3 · Roadmap Drafting | branch `ai-sprint/036` + this sprint dir | ✅ `RA-12` from `main` `ba80a55` (`v4.18.0`) |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory (Model/Effort; L2/M2/M6 mechanical) |
| 5 · Approval Gate | Human authorisation | ✅ 2026-08-26 over plan at `7ebf251` («ok») |
| 6 · Execution | DAG `L1+L2→L3` ∥ `M1+M2→M3…M9` | ✅ 12/12 SHAs on `task_scope.md` |
| 7 · Quality Gate | G1.q / G1.t in `SPRINT_LOG.md` | ✅ both `APPROVED` (round 1, `1b4f5ce`) |
| 8 · Closeout | `CHANGELOG.md` `[Unreleased]`, roadmap, this register | ✅ this close; same-turn `/agents:deployment` |

## Gate rounds

| Gate | Verdict | Class |
| :--- | :--- | :--- |
| **G1.q** (QA) | **APPROVED** — transcribed in `SPRINT_LOG.md` | *(none)* |
| **G1.t** (Tester) | **APPROVED** — transcribed in `SPRINT_LOG.md` | *(none)* |

## Walkthroughs / Entry Point anchors

Nucleus mode: no per-module Walkthroughs and no host `0_SYSTEM_OVERVIEW.md` /
`0_SYSTEM_ARCHITECTURE.md`. Close updates Master Ledger + Global Roadmap only.

## O5 triage — Cursor-era census (`CURSOR_ERA_EXECUTION_AUDIT.md`)

| Sprint | CE-1 | CE-2 | CE-3 | CE-4 | Label | Destination |
| :--- | ---: | ---: | ---: | ---: | :--- | :--- |
| 026–027 | high | 0 | 2 | 0 | `already-in-034` | Instruments I4/K landed in 034; history not rewritten |
| 028–032 | >0 | 0 | varies | 0 | `already-in-034` | H-005 + I4; census documents only |
| 033 | 0 | 0 | 0 | 0 | `fixed` | Clean baseline for CE-1 |
| CE-4 pattern (033 Tester notes) | — | — | — | counted in L1 | `deferred` | Do not rewrite closed `SPRINT_LOG`; G/038 may use as ledger input |
| CE-5 sandbox pytest | — | — | — | — | `deferred` | Protocol in audit; rider **S** (037) covers agent-sandbox `xargs`/`ARG_MAX` (distinct from CE-5) |
| New mid-sprint units from census | — | — | — | — | *(none)* | Rider **S** came from session measurement, already queued on **037** |

## Heuristic pulse (Phase 2.5)

| Candidate | routing_class |
| :--- | :--- |
| `memory/telemetry/` empty this session | `discard` — no raw_errors to distill |
| Agent sandbox `xargs`/`ARG_MAX` + missing nucleus `.bridge_cursor.lock` | `nucleus` — already queued as Track **S** on **037** (not a new KI) |
| Other Models quota blocked gate `Task` | `discard` — operational quota, not a framework defect to index |
| No new host-class KI | — |
