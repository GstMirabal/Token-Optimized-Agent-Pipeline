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

## Cursor tier map — proposals (PENDING HUMAN ACCEPTANCE)

Until the human accepts rows below, **do not** treat `haiku`/`sonnet`/`opus` as
Cursor session models. Select the accepted Cursor `modelId` in the UI before
each unit; record the applied id from disk in `SPRINT_LOG.md` (026 pattern).

| Intent (phase) | Claude Code default (reference only) | Cursor proposal (`make cursor-tiers`) | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** (first mechanical proposal; no depth lever) | **N/A** — no `effort`/`thinking`/`reasoning` parameter |
| `author` | `sonnet` / `medium` | **`grok-4.6`** (sole author cold-start proposal; currently applied) | Has `effort` lever — applied now: **`high`** (re-measure at unit start) |
| `gate` | `opus` / `high` | **`(none)`** — stays null until proven history | Under sequential Cursor, 026 used **Composer** for gates and logged it; config cell remains null |

**Human decision required before Phase 6:** accept / replace the three Cursor
proposals (especially whether gate stays Composer-as-logged vs remains unset).

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

**Assignee unchanged.** Escalation is **intent tier** (mechanical → author), then
bound to a **Cursor model** from § Cursor tier map once the human accepts it.

Defaults for `devops_agent` intent: `mechanical`. Cursor binding pending
acceptance: mechanical → `composer-2.5` (no effort lever).

| # | File | From (intent) | To (intent) | Cursor model (if proposals accepted) | Why |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A3 | `hooks/on_init.py` | mechanical | **author** | `grok-4.6` + effort lever | `F-026-A3` path/false-green class |
| P1 | `scripts/persist_session_context.py` | mechanical | **author** | `grok-4.6` + effort lever | New session-memory protocol |
| P2 | `scripts/check_role_artifact.py` | mechanical | **author** | `grok-4.6` + effort lever | Drift gate vs registry |
| P3 | `scripts/session_end_hook.py` | mechanical | **author** | `grok-4.6` + effort lever | `suspend`≠`release` |
| C1 | `claude/settings.hooks.json` | mechanical | **author** | `grok-4.6` + effort lever | `hard_deny`/sandbox; Abort on deny loss |

**Not escalated (stay mechanical → `composer-2.5` if accepted):** `P2.2`, all
`tests/` deviation rows, prose on profiles that are already `author`/`gate`
intent (`A1`–`A1.2`, `C2`–`C3`, `D1`–`D3`, gates).

**Work-table annotation** (after human accepts Cursor map):  
`devops_agent — escalated (mechanical → author; Cursor <modelId>[; effort <v>]; see Declared escalations)`.

Until acceptance, Assignee cells name **profile only** (no fake Claude model).

---

## Ola 0 — Contradicciones

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | modify | medium | `agent_orchestrator` | ⏳ |
| A1.1 | `agents/qa_agent.md` | modify | low | `agent_orchestrator` | ⏳ |
| A1.2 | `agents/orchestrator.md` | modify | low | `agent_orchestrator` | ⏳ |
| A3 | `hooks/on_init.py` | modify | high | `devops_agent` — escalated (intent author; Cursor model PENDING ACCEPTANCE) | ⏳ |
| A3.1 | `tests/test_on_init.py` | create | medium | `devops_agent` — deviation (tests/) | ⏳ |

## Ola 1 — Portable

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/persist_session_context.py` | create | medium | `devops_agent` — escalated (intent author; Cursor model PENDING ACCEPTANCE) | ⏳ |
| P1.1 | `tests/test_persist_session_context.py` | create | medium | `devops_agent` — deviation (tests/) | ⏳ |
| P2 | `scripts/check_role_artifact.py` | create | medium | `devops_agent` — escalated (intent author; Cursor model PENDING ACCEPTANCE) | ⏳ |
| P2.1 | `tests/test_check_role_artifact.py` | create | medium | `devops_agent` — deviation (tests/) | ⏳ |
| P2.2 | `Makefile` | modify | medium | `devops_agent` | ⏳ |
| P3 | `scripts/session_end_hook.py` | create | medium | `devops_agent` — escalated (intent author; Cursor model PENDING ACCEPTANCE) | ⏳ |
| P3.1 | `tests/test_session_end_hook.py` | create | low | `devops_agent` — deviation (tests/) | ⏳ |

## Ola 2 — Template Claude Code

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `claude/settings.hooks.json` | modify | high | `devops_agent` — escalated (intent author; Cursor model PENDING ACCEPTANCE) | ⏳ |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | create | low | `doc_orchestrator` | ⏳ |
| C3 | `workflows/start_workflow.md` | modify | medium | `doc_orchestrator` | ⏳ |

## Ola 3 — Cierre

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | ⏳ |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent` | ⏳ |

## Phase 7 — Quality Gate (transcription)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `qa_agent` | ⏳ |
| G1.q | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator` | ⏳ |
| G1.t | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | emit verdict | medium | `tester_agent` | ⏳ |
| G1.t | `docs/sprints/027-core-pipeline/SPRINT_LOG.md` | transcribe | medium | `orchestrator` | ⏳ |

---

## Isolation notes

- `A3` before `A3.1`. Ola 1 scripts before tests; `P2` before `P2.2`.
- Ola 2 `C1` after Ola 1. Ola 3 after `make verify` green.
- **Before Phase 6:** human accepts or replaces § Cursor tier map; then patch
  Assignee annotations with concrete `modelId` (+ effort when the model has a lever).

## RA-16

`P1`/`P2`/`P3` declare `invoked_by:` in docstrings. `make cursor-tiers` already
declares `invoked_by: Makefile 'cursor-tiers' target.`
