# Task Scope — Sprint 034 (`core-pipeline`)

**Branch**: `ai-sprint/034` · **Base**: `main` at `76ae9b3` (`v4.16.0`)
**Plan**: `docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md` (committed `ffd33e0`)
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

**Backfill.** This file was written 2026-08-26 after Phase 6 had already
committed tracks A, B, P, I (partial), K (partial), and N. `jurisdictional_lock`
could not be enforced on those writes. **No remaining 034 Work locks.** K6
`2a2dbc9`, J1 `c61dd89`. Out-of-sprint rows (C/E/H/F, M/L, G, 038) are absent
on purpose.

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + **`make cursor-tiers` run this session** |
| Accept Cursor model into `config/model_tiers.json` | **Human** | map already set by Sprint 032 | Sprint 027 Design §D7 |

---

## Measured Cursor state (this session, 2026-08-26)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py ; echo exit=$?
exit=0
Models after hard filters (excl. default): 35
Applied model (author cold-start candidate): grok-4.6
Proposed author (≤1, cold start): grok-4.6 (depth_lever yes)
Catalogue includes grok-4.5 (xai, depth_lever yes)
Proposed mechanical (no depth lever): composer-2.5, gemini-3.1-pro,
  gemini-3.5-flash, gpt-5-mini, gemini-2.5-flash
Proposed gate: (none) — Design §D7, not proven history
Proposals only — config/model_tiers.json was not modified
```

**Map in force (Sprint 032 promote).** `cursor.author` = `grok-4.5` / `high`;
`cursor.mechanical` = `composer-2.5`; `cursor.gate.model` = `null`. Reproduce:
`python3 -c "import json; a=json.load(open('config/model_tiers.json'))['tiers']['author']['cursor']; print(a['model'], a['effort'])"`.

Global medidor may still report `grok-4.6` (per-chat override invisible to
`applicationOpenModelAppliedConfig`). Work rows use the **map** (`grok-4.5` /
`high`), not the cold-start proposal string.

## Cursor tier map (post-032 promote)

| Intent (phase) | Claude Code (reference only) | Cursor | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`grok-4.5`** | **`high`** |
| `gate` | `opus` / `high` | **`null` in config** | Operational: log applied model from disk at gate time |

---

## Declared escalations — `token_economy_agent` audit, transcribed per `tier_escalation`

None. Every Work unit assignee is already `tier: author` (`orchestrator`,
`doc_orchestrator`, `implementer_agent`, `agent_orchestrator`, `rule_validator`).
No mechanical→author row.

---

## Track A — close chains deploy

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `commands/close.md` | modify | medium | `orchestrator` | `grok-4.5` | `high` | ✅ `c15b4f5` |
| A2 | `workflows/close_workflow.md` | modify | high | `orchestrator` | `grok-4.5` | `high` | ✅ `611da90` |

## Track B — graph probe truth

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `scripts/session_probe.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `c2fc750` |
| B2 | `tests/test_session_probe.py` | create | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `c2fc750` |

B1+B2 share one `fix(` commit (`hooks/on_commit.py` regression-test rule).

## Track P — auto-pin on `/start`

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/sync_agents_pin.py` | create | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `25b48af` |
| P2 | `tests/test_sync_agents_pin.py` | create | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `25b48af` |
| P3 | `workflows/start_workflow.md` | modify | high | `orchestrator` | `grok-4.5` | `high` | ✅ `06a532a` |

P1+P2 share one `fix(` commit.

## Track I — assignment authority

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | medium | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `306eba1` |
| I2 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | `grok-4.5` | `high` | ✅ `53c596d` |
| I3 | `agents/agent_orchestrator.md` | modify | high | `agent_orchestrator` | `grok-4.5` | `high` | ✅ `d3f284d` |
| I4 | `scripts/check_task_scope.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `3dc95db` |
| I5 | `tests/test_check_task_scope.py` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `3dc95db` |
| I6 | `docs/hotfixes/H-005-pipeline.md` | create | medium | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `18b78ab` |
| I7 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | create | medium | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `3182b00` |

I4+I5+K3+K5 share commit `3dc95db`. I2 precedes K6 on the same file.

## Track K — absence gates

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| K1 | `scripts/check_role_artifact.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `9e8c0d3` |
| K2 | `config/artifact_registry.json` | modify | high | `rule_validator` | `grok-4.5` | `high` | ✅ `ca203ce` |
| K3 | `scripts/check_task_scope.py` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `3dc95db` |
| K4 | `tests/test_check_role_artifact.py` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `9e8c0d3` |
| K5 | `tests/test_check_task_scope.py` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `3dc95db` |
| K6 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | `grok-4.5` | `high` | ✅ `2a2dbc9` |

K1+K4 share commit `9e8c0d3`.

## Track J — constitution anchor

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| J1 | `AGENTS.md` | modify | high | `rule_validator` | `grok-4.5` | `high` | ✅ `c61dd89` |

**J1 landed** `c61dd89` (`agents.md` on disk; same inode as `AGENTS.md`).

## Track N — Cursor agent emission

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| N1 | `scripts/cursor_adapter.py` | modify | high | `implementer_agent` | `grok-4.5` | `high` | ✅ `676b72a` |
| N2 | `tests/test_cursor_adapter.py` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `676b72a` |
| N3 | `.gitignore` | modify | low | `implementer_agent` | `grok-4.5` | `high` | ✅ `89861df` |
| N4 | `scripts/install.py` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `7fb98cf` |
| N5 | `tests/test_installer.sh` | modify | medium | `implementer_agent` | `grok-4.5` | `high` | ✅ `7fb98cf` |
| N6 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | modify | low | `doc_orchestrator` | `grok-4.5` | `high` | ✅ `8978a56` |

N1+N2 share commit `676b72a`. N4+N5 share commit `7fb98cf`.
