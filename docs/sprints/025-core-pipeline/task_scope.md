# Task Scope — Sprint 025 (`jurisdiction`)

**Branch**: `ai-sprint/025`, from `ai-sprint/024` — the guard is blind without
that sprint's `.gitignore` change, so building it on `main` would produce a check
that passes on a dirty tree.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `docs/sprints/025-core-pipeline/IMPLEMENTATION_PLAN.md` | create | low | lead · `principal_agent` ruleset | ✅ |
| 2 | `scripts/_mode.py` | create | medium | lead · `devops_agent` ruleset | ✅ `J1` |
| 3 | `scripts/session_probe.py` | modify | low | lead · `devops_agent` ruleset | ✅ `J1` — delegates instead of duplicating |
| 4 | `scripts/submodule_purity.py` | create | **high** — a gate | lead · `devops_agent` ruleset | ✅ `J2` |
| 5 | `workflows/close_workflow.md` | modify | low | lead · `doc_orchestrator` ruleset | ✅ `J3` |
| 6 | `hooks/on_commit.py` | modify | **high** — blocks commits | lead · `devops_agent` ruleset | ✅ `J4` |
| 7 | `agents.md` §3 | modify | **high** — constitutional | lead · `rule_validator` ruleset | ✅ `J5` |
| 8 | `tests/test_session_protocol.py` | modify | medium | lead · `tester_agent` ruleset | ✅ 7 tests |
| 9 | `CHANGELOG.md`, sprint records | modify | low | lead · `doc_orchestrator` ruleset | ⏳ |

## Declared deviation — delegation

Unchanged from Sprint `024`: the session configuration forbids spawning
subagents, reported before Phase 1 per `start_workflow.md` `delegation_conflict`
and authorised. Writes are emitted under the ruleset of the profile that governs
each artifact. `F-021-A2` makes this unavoidable for `scripts/` and `hooks/`,
which no profile owns.

## Isolation

Single-session, single-branch. `no_interference` has no competing subtask.
