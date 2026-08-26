# Phase Register — Sprint 038 (`core-pipeline` / family-trial)

What `close_workflow.md` Phase 2.6 `double_gate_evidence` reads: **did this phase actually happen?**

| Phase | Artifact it must leave | Status |
| :--- | :--- | :--- |
| 1 · Planning | `IMPLEMENTATION_PLAN.md` | ✅ this directory (Lock 1 `05b4d7b` before Approval Gate) |
| 2 · Environment | `venv_skillopt/` present | ✅ verified (`make verify` 615 pytest + installer) |
| 3 · Roadmap Drafting | branch `ai-sprint/038` + this sprint dir | ✅ `RA-12` from `main` `171531a` (`v4.20.0` + reconcile) |
| 4.1 · Agent Assignment | `agent_assignment.md` | ✅ this directory |
| 4.2 · Skill Assignment | `skill_assignment.md` | ✅ this directory |
| 4.3 · Rule Audit | `task_scope.md` | ✅ this directory (Model/Effort; T1 mechanical) |
| 5 · Approval Gate | Human authorisation | ✅ 2026-08-26 over plan at `05b4d7b` («ok») |
| 6 · Execution | DAG `C1 → (T1 → M1)` ∥ `D1` ∥ `D2` ∥ `R1` | ✅ 6/6 SHAs on `task_scope.md` |
| 7 · Quality Gate | Gate table in `SPRINT_LOG.md` | ✅ both `APPROVED` (round 1; in-session after Other Models limit) |
| 8 · Closeout | `CHANGELOG.md` `[Unreleased]`, roadmap, this register | ✅ promote sealed this session; formal `/agents:close` + deploy pending |

## Gate rounds

| Gate | Verdict | Class |
| :--- | :--- | :--- |
| **QA** | **APPROVED** — transcribed in `SPRINT_LOG.md` | *(none)* |
| **Tester** | **APPROVED** — transcribed in `SPRINT_LOG.md` | *(none)* |

## Promote decision (D12 + Human OK)

| Fact | Value |
| :--- | :--- |
| Decision | **Promote** `cursor.author` = `glm-5.2` / `zhipu` / `high` |
| Human OK | 2026-08-26 («promover») |
| Baseline | Ledger rows 036 + 037 (Gate1/Gate2 round 1 `APPROVED`) |
| Trial row | Ledger 038 Gate1/Gate2 round 1 `APPROVED`; zero `REJECTED` `charter` |

## Walkthroughs / Entry Point anchors

Nucleus mode: no per-module Walkthroughs and no host `0_SYSTEM_OVERVIEW.md` /
`0_SYSTEM_ARCHITECTURE.md`. Close updates Master Ledger + Global Roadmap only.

## Heuristic pulse (Phase 2.5) — draft for close

| Candidate | routing_class |
| :--- | :--- |
| `memory/` empty this session (no raw_errors) | `discard` |
| Other Models usage limit blocked Opus `Task` gates | `discard` — same posture as 037; in-session Double-Gate recorded |
| Applied medidor `grok-4.6` ≠ map after promote | `discard` — 038 Q4 attestation path; map is source of truth for tiers |
| No new host-class KI | — |

Human OK on `/agents:close` must cover this pulse.
