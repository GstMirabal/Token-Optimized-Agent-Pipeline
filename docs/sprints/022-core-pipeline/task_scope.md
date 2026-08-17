# Task Scope — Sprint 022 (`model-tiering`)

**Branch**: `ai-sprint/022` · **Base**: `main` at `2d5f056` (`v4.6.0`)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `agents/*.md` (13) | modify | medium — every role reads these | lead · `agent_orchestrator` ruleset | ✅ T1 |
| 2 | `config/model_tiers.json` | create | medium | lead · `token_economy_agent` ruleset | ✅ T2 |
| 3 | `scripts/detect_new_models.py` | create | **high** — a gate | lead · `devops_agent` ruleset | ✅ T3/T4 |
| 4 | `scripts/check_model_tiers.py` | create | **high** — a gate | lead · `devops_agent` ruleset | ✅ T5 |
| 5 | `Makefile` | modify | **high** — wires both gates | lead · `devops_agent` ruleset | ✅ |
| 6 | `agents/token_economy_agent.md` | modify | medium — charter | lead · `rule_validator` ruleset | ✅ T6 |
| 7 | `tests/test_session_protocol.py` | modify | medium | lead · `tester_agent` ruleset | ✅ 10 tests |
| 8 | `docs/roadmaps/…/022-model-tiering.md`, this directory | create | low | lead · `orchestrator` ruleset | ✅ |
| 9 | `CHANGELOG.md` | modify | low | lead · `doc_orchestrator` ruleset | ⏳ |

## Declared deviation — delegation

Unchanged: subagent spawning forbidden by session configuration, reported before
Phase 1 and authorised. `F-021-A2` makes it unavoidable for `scripts/` regardless.

## Isolation

Single-session, single-branch. `no_interference` has no competing subtask.
