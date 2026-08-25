# Task Scope — Sprint 027 (`autonomy-posture`)

**Branch**: `ai-sprint/027` · **Base**: `main` at `980f149`
**Plan**: `docs/sprints/027-core-pipeline/IMPLEMENTATION_PLAN.md`, committed `d874d7a`
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Status`

**Status legend.** `⏳` pending Phase 5; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

---

## Failure analysis — Model/Effort draft of 2026-08-25 (corrected this commit)

| What went wrong | Evidence | Correct owner / mechanism |
| :--- | :--- | :--- |
| **Wrong agent** filled Model/Effort | `agent_orchestrator` only assigns profiles (`agents/agent_orchestrator.md`: *"Designate, assign, or create subagent profiles"*). It never owns tiers. | **`token_economy_agent`** proposes via `tier_escalation` / `tier_ownership`; **`rule_validator`** transcribes into this file (Sprint 026 precedent: *"issuing agent decides, rule_validator transcribes"* — `token_economy` has no `Write`/`Edit`) |
| **Wrong tool column** used | Values were Claude Code aliases (`haiku` / `sonnet` / `opus` / effort low\|medium\|high from `config/model_tiers.json` → `claude_code`) | Session tool is **Cursor**. Sprint 026 shipped `scripts/audit_cursor_models.py` + `make cursor-tiers` for the Cursor catalogue |
| **Shipped Cursor mechanism not run** | `config/model_tiers.json` `cursor.*.model` is still `null` for all three tiers (by Design §D7 until a human accepts a proposal). The draft ignored that and invented Claude names anyway | Run `make cursor-tiers` (re-run 2026-08-25 this session: exit 0; 35 models; proposals printed; config **not** written) |
| **`F-026-A2` put out of plan scope, then the same gap re-opened by hand** | Plan Out of scope sent `tier_escalation` dormant → `028`/`030`. Asking for model/effort without that mechanism is exactly the dormancy the finding names | Declaring Cursor model/effort **is** exercising `tier_escalation` under Cursor; it belongs in this `task_scope`, owned by `token_economy_agent`, not as a silent Principal fill |

**Measured Cursor state (this session):**

```text
make cursor-tiers   # → python3 scripts/audit_cursor_models.py
Catalogue: 35 models (supportsAgent, degradationStatus==0)
Applied model: grok-4.6  (effort=high, fast=false)  # state.vscdb
Proposed author (≤1, cold start): grok-4.6
Proposed mechanical (no depth lever): composer-2.5, gemini-3.1-pro, gemini-3-flash,
  gemini-3.5-flash, gpt-5-mini
Proposed gate: (none) — Design §D7, not proven history
```

Sprint 026 Hito 2 gates recorded **Composer** in `SPRINT_LOG.md` while leaving
`cursor.*.model` null in config — proposals were never human-accepted into the
JSON. That is why "the list from last sprint" exists as a **script + log**, not
as filled cells in `model_tiers.json`.

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + `make cursor-tiers` |
| Accept Cursor model into `model_tiers.json` | **Human** | `config/model_tiers.json` (separate unit if approved) | Design §D7 — script proposes only |

---

## Cursor tier map — **ACCEPTED** (human 2026-08-25)

Bindings written into `config/model_tiers.json` `cursor` column the same day.
Select the `modelId` in the Cursor UI before each unit; re-read applied config
from `state.vscdb` into `SPRINT_LOG.md` when gating (026 pattern).

| Intent (phase) | Claude Code default (reference only) | Cursor (accepted) | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** — no depth lever |
| `author` | `sonnet` / `medium` | **`grok-4.6`** | **`high`** |
| `gate` | `opus` / `high` | **`null` in config** (Design §D7) | Operational: may log Composer as 026; do not invent a config cell |

Anti-regression: `memory_index.json` `F-20260825-027`; durable rows on
`agent_orchestrator` (`no_model_columns`), `rule_validator` (`tier_transcription`),
`token_economy_agent` (`tier_escalation` Cursor clause).

---

## Agent assignment map (profiles only)

From `agent_assignment.md`. Model/effort → § Declared escalations (Cursor).

| # | File | Assignee | Ruleset file | Notes |
| :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | |
| A1.1 | `agents/qa_agent.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | |
| A1.2 | `agents/orchestrator.md` | `agent_orchestrator` | `agents/agent_orchestrator.md` | |
| A3 | `hooks/on_init.py` | `devops_agent` | `agents/devops_agent.md` | |
| A3.1 | `tests/test_on_init.py` | `devops_agent` | `agents/devops_agent.md` | Deviation tests/ |
| P1 | `scripts/persist_session_context.py` | `devops_agent` | `agents/devops_agent.md` | |
| P1.1 | `tests/test_persist_session_context.py` | `devops_agent` | `agents/devops_agent.md` | Deviation tests/ |
| P2 | `scripts/check_role_artifact.py` | `devops_agent` | `agents/devops_agent.md` | |
| P2.1 | `tests/test_check_role_artifact.py` | `devops_agent` | `agents/devops_agent.md` | Deviation tests/ |
| P2.2 | `Makefile` | `devops_agent` | `agents/devops_agent.md` | |
| P3 | `scripts/session_end_hook.py` | `devops_agent` | `agents/devops_agent.md` | |
| P3.1 | `tests/test_session_end_hook.py` | `devops_agent` | `agents/devops_agent.md` | Deviation tests/ |
| C1 | `claude/settings.hooks.json` | `devops_agent` | `agents/devops_agent.md` | |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` | |
| C3 | `workflows/start_workflow.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` | |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `governance_learner` | `agents/governance_learner.md` | |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | `orchestrator` | `agents/orchestrator.md` | |
| D3 | `CHANGELOG.md` | `principal_agent` | `agents/principal_agent.md` | |
| G1.q | `SPRINT_LOG.md` emit / write | `qa_agent` → `orchestrator` | gate + author profiles | |
| G1.t | `SPRINT_LOG.md` emit / write | `tester_agent` → `orchestrator` | gate + author profiles | |

---

## Declared deviations

**1. `tests/` writes → `devops_agent`.** `tester_agent` has no `Write`/`Edit`.
Affected: `A3.1`, `P1.1`, `P2.1`, `P3.1`.

**2. Gate verdicts → Orchestrator transcription.** Registry + Design §D2.

**3. `F-021-A2` unresolved.** `scripts/`/`hooks/` stay on `devops_agent`.

---

## Declared escalations — `token_economy_agent` audit (Cursor), transcribed by `rule_validator`

**Assignee unchanged.** Escalation is **intent tier** (mechanical → author), bound
to accepted Cursor models from § Cursor tier map.

Defaults for `devops_agent`: intent `mechanical` → Cursor **`composer-2.5`** (effort N/A).

| # | File | From (intent) | To (intent) | Cursor model | Effort | Why |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A3 | `hooks/on_init.py` | mechanical | **author** | `grok-4.6` | `high` | `F-026-A3` path/false-green class |
| P1 | `scripts/persist_session_context.py` | mechanical | **author** | `grok-4.6` | `high` | New session-memory protocol |
| P2 | `scripts/check_role_artifact.py` | mechanical | **author** | `grok-4.6` | `high` | Drift gate vs registry |
| P3 | `scripts/session_end_hook.py` | mechanical | **author** | `grok-4.6` | `high` | `suspend`≠`release` |
| C1 | `claude/settings.hooks.json` | mechanical | **author** | `grok-4.6` | `high` | `hard_deny`/sandbox; Abort on deny loss |

**Not escalated (stay mechanical → `composer-2.5`):** `P2.2`, all `tests/`
deviation rows. Profiles already on author/gate intent use the accepted Cursor
row for that intent (`A1`–`A1.2`, `C2`–`C3`, `D1`–`D2` → `grok-4.6`/`high`;
`D3` + gate emit → config `gate` null, log Composer if used).

**Work-table annotation:**  
`devops_agent — escalated (mechanical → author; Cursor grok-4.6, effort high; see Declared escalations)`.

---

## Ola 0 — Contradicciones

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | modify | medium | `agent_orchestrator`; Cursor `grok-4.6`, effort `high` | ✅ `ab521b7` |
| A1.1 | `agents/qa_agent.md` | modify | low | `agent_orchestrator`; Cursor `grok-4.6`, effort `high` | ✅ `bbdfe59` |
| A1.2 | `agents/orchestrator.md` | modify | low | `agent_orchestrator`; Cursor `grok-4.6`, effort `high` | ✅ `c524794` |
| A3 | `hooks/on_init.py` | modify | high | `devops_agent` — escalated (mechanical → author; Cursor `grok-4.6`, effort `high`; see Declared escalations) | ✅ `573660e` (with A3.1; `fix(`+test gate) |
| A3.1 | `tests/test_on_init.py` | create | medium | `devops_agent` — deviation (tests/); Cursor `composer-2.5` | ✅ `573660e` |

## Ola 1 — Portable

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/persist_session_context.py` | create | medium | `devops_agent` — escalated (mechanical → author; Cursor `grok-4.6`, effort `high`; see Declared escalations) | ✅ `3a630e3` |
| P1.1 | `tests/test_persist_session_context.py` | create | medium | `devops_agent` — deviation (tests/); Cursor `composer-2.5` | ✅ `5ae353e` |
| P2 | `scripts/check_role_artifact.py` | create | medium | `devops_agent` — escalated (mechanical → author; Cursor `grok-4.6`, effort `high`; see Declared escalations) | ✅ `9d5c68c` |
| P2.1 | `tests/test_check_role_artifact.py` | create | medium | `devops_agent` — deviation (tests/); Cursor `composer-2.5` | ✅ `7a80479` |
| P2.2 | `Makefile` | modify | medium | `devops_agent`; Cursor `composer-2.5` | ✅ `c30c3a0` |
| P3 | `scripts/session_end_hook.py` | create | medium | `devops_agent` — escalated (mechanical → author; Cursor `grok-4.6`, effort `high`; see Declared escalations) | ✅ `bbb48aa` |
| P3.1 | `tests/test_session_end_hook.py` | create | low | `devops_agent` — deviation (tests/); Cursor `composer-2.5` | ✅ `e499b71` |

## Ola 2 — Template Claude Code

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `claude/settings.hooks.json` | modify | high | `devops_agent` — escalated (mechanical → author; Cursor `grok-4.6`, effort `high`; see Declared escalations) | ✅ `eded4ef` |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | create | low | `doc_orchestrator`; Cursor `grok-4.6`, effort `high` | ✅ `eeb895f` |
| C3 | `workflows/start_workflow.md` | modify | medium | `doc_orchestrator`; Cursor `grok-4.6`, effort `high` | ✅ `3233536` |

## Ola 3 — Cierre

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner`; Cursor `grok-4.6`, effort `high` | ✅ `73f3658` |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator`; Cursor `grok-4.6`, effort `high` | ✅ `639e80e` |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent`; Cursor gate config `null` (log model from disk) | ✅ `9170dc5` |

## Phase 7 — Quality Gate (transcription)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `qa_agent`; Cursor gate config `null` (log model from disk) | ⏳ |
| G1.q | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |
| G1.t | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `tester_agent`; Cursor gate config `null` (log model from disk) | ⏳ |
| G1.t | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator`; Cursor `grok-4.6`, effort `high` | ⏳ |

---

## Isolation notes

- `A3` before `A3.1`. Ola 1 scripts before tests; `P2` before `P2.2`.
- Ola 2 `C1` after Ola 1. Ola 3 after `make verify` green.
- Cursor bindings accepted 2026-08-25 (`composer-2.5` / `grok-4.6`+`high` / gate null).

## RA-16

`P1`/`P2`/`P3` declare `invoked_by:` in docstrings. `make cursor-tiers` already
declares `invoked_by: Makefile 'cursor-tiers' target.`
