# Task Scope — Sprint 028 (`self-improvement-unblock`)

**Branch**: `ai-sprint/028` · **Base**: `main` at `0a175a2`
**Plan**: `docs/sprints/028-core-pipeline/IMPLEMENTATION_PLAN.md`, committed `e52e2b6`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

---

## Failure analysis — Model/Effort draft of 2026-08-25 (corrected this commit)

| What went wrong | Evidence | Correct owner / mechanism |
| :--- | :--- | :--- |
| **Principal filled tiers without audit section** | First `task_scope.md` on `e52e2b6` inlined a few Cursor names in `Assignee` and wrote *"All other units stay at their profile's default intent tier"* — no per-row `Model`/`Effort` columns, no `token_economy_agent` audit table | **`token_economy_agent`** proposes every row via `tier_escalation`; **`rule_validator`** transcribes into this file (`F-026-A2` / `F-20260825-027`) |
| **Ownership map absent** | Sprint 027 precedent requires the four-row map so Model/Effort jurisdiction is visible before the Work tables | Restored below |
| **`make cursor-tiers` not quoted in scope** | Mechanism exists; first draft cited config acceptance but not the live catalogue run for this session | Measured block below |

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + `make cursor-tiers` |
| Accept Cursor model into `model_tiers.json` | **Human** | `config/model_tiers.json` (separate unit if approved) | Design §D7 — script proposes only |

---

## Measured Cursor state (this session, 2026-08-25)

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py
Catalogue: 35 models (supportsAgent, degradationStatus==0)
Applied model: grok-4.6  (effort=high, fast=false)  # state.vscdb
Proposed author (≤1, cold start): grok-4.6
Proposed mechanical (no depth lever): composer-2.5, gemini-3.1-pro, gemini-3-flash,
  gemini-3.5-flash, gpt-5-mini
Proposed gate: (none) — Design §D7, not proven history
```

Config already human-accepted Sprint 027: `cursor.mechanical=composer-2.5`,
`cursor.author=grok-4.6` (effort `high`). `cursor.gate.model` stays **`null`**.

---

## Cursor tier map — **ACCEPTED** (Sprint 027, still binding)

| Intent (phase) | Claude Code (reference only) | Cursor (accepted) | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`grok-4.6`** | **`high`** |
| `gate` | `opus` / `high` | **`null` in config** | Operational: log applied model from disk at gate time; do not invent a config cell |

Select the `modelId` in the Cursor UI before each unit; re-read applied config
from `state.vscdb` into `SPRINT_LOG.md` when gating (026–027 pattern).

---

## Agent assignment map (profiles only)

From `agent_assignment.md`. Model/Effort → § Declared escalations and Work tables.

| # | File | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- |
| A1 | `agents/agent_orchestrator.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` |
| A2 | `workflows/pipeline_workflow.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| P1 | `scripts/install.py` | `devops_agent` | `agents/devops_agent.md` |
| P1.1 | `tests/test_installer.sh` or `tests/test_install_profile_path.py` | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| P2 | `agents.md` | `governance_learner` | `agents/governance_learner.md` |
| P2.1 | `profiles/example-project/README.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| M1 | `workflows/extract_workflow.md` | `governance_learner` | `agents/governance_learner.md` |
| M2 | `workflows/close_workflow.md` | `governance_learner` | `agents/governance_learner.md` |
| D1 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | `orchestrator` | `agents/orchestrator.md` |
| D3 | `CHANGELOG.md` | `principal_agent` | `agents/principal_agent.md` |
| G1.q / G1.t emit | `SPRINT_LOG.md` | `qa_agent` / `tester_agent` | gate profiles |
| G1.q / G1.t transcribe | `SPRINT_LOG.md` | `orchestrator` | `agents/orchestrator.md` |

---

## Declared escalations — `token_economy_agent` audit (Cursor), transcribed by `rule_validator`

**Assignee unchanged.** Escalation is **intent tier / model**, not profile swap.

Default by profile tier (`config/model_tiers.json` + accepted Cursor column):

| Profile | Default intent | Default Cursor model | Default effort |
| :--- | :--- | :--- | :--- |
| `devops_agent` | mechanical | `composer-2.5` | N/A |
| `agent_orchestrator`, `doc_orchestrator`, `governance_learner`, `orchestrator` | author | `grok-4.6` | `high` |
| `principal_agent`, `qa_agent`, `tester_agent` | gate | `null` (config) | log from disk |

**Escalations (mechanical → author for one task):**

| # | File | From | To | Cursor model | Effort | Why |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/install.py` | mechanical | **author** | `grok-4.6` | `high` | External profile path, symlink layout, nucleus/host mode split — regression surface beyond mechanical default |

**Not escalated (stay on default row for assignee's tier):**

| # | File | Assignee | Cursor model | Effort | Why kept default |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/agent_orchestrator.md` | `agent_orchestrator` | `grok-4.6` | `high` | author-tier governance prose |
| A2 | `workflows/pipeline_workflow.md` | `doc_orchestrator` | `grok-4.6` | `high` | author-tier workflow cell |
| P1.1 | tests (deviation) | `devops_agent` | `composer-2.5` | N/A | mechanical test harness |
| P2 | `agents.md` | `governance_learner` | `grok-4.6` | `high` | author-tier amendment |
| P2.1 | profile README | `doc_orchestrator` | `grok-4.6` | `high` | author-tier doc |
| M1, M2 | extract/close workflows | `governance_learner` | `grok-4.6` | `high` | author-tier workflow prose |
| D1 | new guide | `doc_orchestrator` | `grok-4.6` | `high` | author-tier how-to |
| D2 | roadmap | `orchestrator` | `grok-4.6` | `high` | author-tier roadmap |
| D3 | CHANGELOG | `principal_agent` | log from disk | N/A | gate tier; config cell null |
| G1.q, G1.t emit | SPRINT_LOG | gate profiles | log from disk | N/A | gate tier; config cell null |
| G1.q, G1.t transcribe | SPRINT_LOG | `orchestrator` | `grok-4.6` | `high` | author-tier transcription |

---

## Declared deviations

**1. `tests/` writes → `devops_agent`.** Affected: `P1.1`.

**2. Gate verdicts → Orchestrator transcription.** Registry precedent (027).

---

## Ola 0 — Doctrina agente

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/agent_orchestrator.md` | modify | medium | `agent_orchestrator` | `grok-4.6` | `high` | ⏳ |
| A2 | `workflows/pipeline_workflow.md` | modify | medium | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |

## Ola 1 — Perfil instalable

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/install.py` | modify | high | `devops_agent` | `grok-4.6` | `high` | ⏳ |
| P1.1 | `tests/test_installer.sh` or `tests/test_install_profile_path.py` | modify/create | medium | `devops_agent` — deviation (tests/) | `composer-2.5` | N/A | ⏳ |
| P2 | `agents.md` | modify | medium | `governance_learner` | `grok-4.6` | `high` | ⏳ |
| P2.1 | `profiles/example-project/README.md` | modify | low | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |

## Ola 2 — Memoria

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `workflows/extract_workflow.md` | modify | medium | `governance_learner` | `grok-4.6` | `high` | ⏳ |
| M2 | `workflows/close_workflow.md` | modify | medium | `governance_learner` | `grok-4.6` | `high` | ⏳ |

## Ola 3 — Promoción y cierre

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | create | low | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | `grok-4.6` | `high` | ⏳ |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent` | log from disk | N/A | ⏳ |

## Phase 7 — Quality Gate (transcription)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | `docs/sprints/028-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `qa_agent` | log from disk | N/A | ⏳ |
| G1.q | `docs/sprints/028-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator` | `grok-4.6` | `high` | ⏳ |
| G1.t | `docs/sprints/028-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `tester_agent` | log from disk | N/A | ⏳ |
| G1.t | `docs/sprints/028-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator` | `grok-4.6` | `high` | ⏳ |

---

## Isolation notes

- Ola 0 before Ola 1 (doctrine before installer).
- `P1` before `P1.1`.
- Ola 2 after Ola 1; Ola 3 after `make verify` green.

## RA-16

`P1` retains/extends `invoked_by:` in module docstring. New guide `D1` names
invokers in prose only (knowledge artifact — no script).
