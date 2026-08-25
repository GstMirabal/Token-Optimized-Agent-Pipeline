# Task Scope — Sprint 029 (`documentation-truth`)

**Branch**: `ai-sprint/029` · **Base**: `main` at `84201d2`
**Plan**: `docs/sprints/029-core-pipeline/IMPLEMENTATION_PLAN.md` (committed `2f7ec90`)
**Phase**: 4.3 (Rule Audit) — after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2).

**Table shape (Work units).** `# | File | Operation | Risk | Assignee | Model | Effort | Status`

**Status legend.** `⏳` pending Phase 6; `✅ <sha>` after execution.

**Mode.** Cursor `delegation_mode: sequential`.

---

## Ownership map (who does what)

| Concern | Decides | Writes the artifact | Source of truth |
| :--- | :--- | :--- | :--- |
| Profile per unit | `agent_orchestrator` | `agent_assignment.md` | Phase 4.1 |
| File lock / risk / status | `rule_validator` | this file (Work tables) | Phase 4.3 |
| Tier escalation + Cursor model/effort | `token_economy_agent` | transcribed here by `rule_validator` | `tier_escalation` + Sprint 027 accepted Cursor column |
| Accept Cursor model into `config/model_tiers.json` | **Human** | `config/model_tiers.json` (separate unit if approved) | Sprint 027 Design §D7 — script proposes only |

---

## Measured Cursor state (this session, 2026-08-25)

Carried from Sprint 027/028 (human-accepted). `make cursor-tiers` was not
re-run this extraction: the accepted column is unchanged and `F-026-A2` requires
the declaration, not a new catalogue.

Config already human-accepted Sprint 027: `cursor.mechanical=composer-2.5`,
`cursor.author=grok-4.6` (effort `high`). `cursor.gate.model` stays **`null`**.

| Intent (phase) | Claude Code (reference only) | Cursor (accepted) | Effort / depth |
| :--- | :--- | :--- | :--- |
| `mechanical` | `haiku` / `low` | **`composer-2.5`** | **N/A** |
| `author` | `sonnet` / `medium` | **`grok-4.6`** | **`high`** |
| `gate` | `opus` / `high` | **`null` in config** | Operational: log applied model from disk at gate time |

---

## Agent assignment map (profiles only)

From `agent_assignment.md`. Model/Effort → § Declared escalations and Work tables.

| # | File | Assignee | Ruleset file |
| :--- | :--- | :--- | :--- |
| R0 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `governance_learner` | `agents/governance_learner.md` |
| R1 | `CHANGELOG.md` | `principal_agent` | `agents/principal_agent.md` |
| R2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | `orchestrator` | `agents/orchestrator.md` |
| T1.0 | `tests/test_check_readme_counts.py` | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| T1.1 | `scripts/check_readme_counts.py` | `devops_agent` | `agents/devops_agent.md` |
| T1.2 | `README.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| T1.3 | `workflows/close_workflow.md` | `governance_learner` | `agents/governance_learner.md` |
| G1 | `config/artifact_registry.json` | `devops_agent` | `agents/devops_agent.md` |
| G2 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| G3 | `skills/slash-commander/scripts/verify_commands.py` | `devops_agent` | `agents/devops_agent.md` |
| A3–A7 | `docs/decisions/ADR-0003`…`0007` | `doc_orchestrator` | `agents/doc_orchestrator.md` |
| P1 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | `governance_learner` | `agents/governance_learner.md` |
| P2 | `rules/documentation_standard.md` | `governance_learner` | `agents/governance_learner.md` |
| J6.0 | `tests/test_verify_references.py` | `devops_agent` — deviation (tests/) | `agents/devops_agent.md` |
| J6.1 | `scripts/verify_references.py` | `devops_agent` | `agents/devops_agent.md` |
| C1 | `CHANGELOG.md` | `principal_agent` | `agents/principal_agent.md` |
| G1.q / G1.t emit | `SPRINT_LOG.md` | `qa_agent` / `tester_agent` | gate profiles |
| G1.q / G1.t transcribe | `SPRINT_LOG.md` | `orchestrator` | `agents/orchestrator.md` |

---

## Declared escalations — `token_economy_agent` audit (Cursor), transcribed by `rule_validator`

**Assignee unchanged.** Escalation is **intent tier / model**, not profile swap.

Default by profile tier (`config/model_tiers.json` + accepted Cursor column):

| Profile | Default intent | Default Cursor model | Default effort |
| :--- | :--- | :--- | :--- |
| `devops_agent` | mechanical | `composer-2.5` | N/A |
| `doc_orchestrator`, `governance_learner`, `orchestrator` | author | `grok-4.6` | `high` |
| `principal_agent`, `qa_agent`, `tester_agent` | gate | `null` (config) | log from disk |

**Escalations (mechanical → author for one task):**

| # | File | From | To | Cursor model | Effort | Why |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1.1 | `scripts/check_readme_counts.py` | mechanical | **author** | `grok-4.6` | `high` | Writes a marked README region on the close path; abort criterion 1 if it rewrites outside the fence |
| J6.1 | `scripts/verify_references.py` | mechanical | **author** | `grok-4.6` | `high` | False-positive abort criterion 3; corpus exclude is load-bearing |

**Not escalated (stay on default row for assignee's tier):**

| # | File | Assignee | Cursor model | Effort | Why kept default |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R0 | findings register | `governance_learner` | `grok-4.6` | `high` | author-tier prose |
| R1, C1 | CHANGELOG | `principal_agent` | log from disk | N/A | gate tier; config cell null |
| R2 | program queue | `orchestrator` | `grok-4.6` | `high` | author-tier roadmap |
| T1.0, J6.0 | tests | `devops_agent` | `composer-2.5` | N/A | mechanical test harness |
| T1.2 | README | `doc_orchestrator` | `grok-4.6` | `high` | author-tier doc |
| T1.3 | close_workflow | `governance_learner` | `grok-4.6` | `high` | author-tier workflow cell |
| G1 | artifact_registry.json | `devops_agent` | `composer-2.5` | N/A | mechanical JSON row in an existing schema |
| G2 | slash-commands guide | `doc_orchestrator` | `grok-4.6` | `high` | author-tier how-to |
| G3 | `verify_commands.py` | `devops_agent` | `composer-2.5` | N/A | extend an existing filename-set check |
| A3–A7 | ADRs | `doc_orchestrator` | `grok-4.6` | `high` | author-tier ADRs |
| P1, P2 | template / documentation_standard | `governance_learner` | `grok-4.6` | `high` | author-tier rule/template |
| G1.q, G1.t emit | SPRINT_LOG | gate profiles | log from disk | N/A | gate tier |
| G1.q, G1.t transcribe | SPRINT_LOG | `orchestrator` | `grok-4.6` | `high` | author-tier transcription |

---

## Declared deviations

**1. `tests/` writes → `devops_agent`.** Affected: `T1.0`, `J6.0`. `F-026-A1`.

**2. Gate verdicts → Orchestrator transcription.** Registry precedent (027).

**3. `CHANGELOG.md` twice (R1 then C1).** Same file, two commits, two subjects (`84201d2` seal vs sprint 029 entry). `no_interference` allows sequential units on one file when the prior row is `✅`.

---

## Ola 0 — Intake

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R0 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | `grok-4.6` | `high` | ✅ `08dbdb4` |
| R1 | `CHANGELOG.md` | modify | low | `principal_agent` | log from disk | N/A | ✅ `8d55f25` |
| R2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | `grok-4.6` | `high` | ✅ `fb97de5` |

## Ola 1 — T1 counted set

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1.0 | `tests/test_check_readme_counts.py` | create | medium | `devops_agent` — deviation (tests/) | `composer-2.5` | N/A | ⏳ |
| T1.1 | `scripts/check_readme_counts.py` | modify | high | `devops_agent` | `grok-4.6` | `high` | ⏳ |
| T1.2 | `README.md` | modify | medium | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |
| T1.3 | `workflows/close_workflow.md` | modify | low | `governance_learner` | `grok-4.6` | `high` | ⏳ |

## Ola 2 — T3 guide + registry

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G1 | `config/artifact_registry.json` | modify | medium | `devops_agent` | `composer-2.5` | N/A | ⏳ |
| G2 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | modify | medium | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |
| G3 | `skills/slash-commander/scripts/verify_commands.py` | modify | medium | `devops_agent` | `composer-2.5` | N/A | ⏳ |

## Ola 3 — T4 ADRs

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A3 | `docs/decisions/ADR-0003-gates-never-drop-tier.md` | create | low | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |
| A4 | `docs/decisions/ADR-0004-no-model-selector-agent.md` | create | low | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |
| A5 | `docs/decisions/ADR-0005-prices-stay-out-of-config.md` | create | low | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |
| A6 | `docs/decisions/ADR-0006-session-bound-before-tiering.md` | create | low | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |
| A7 | `docs/decisions/ADR-0007-cursor-without-api-delegation.md` | create | low | `doc_orchestrator` | `grok-4.6` | `high` | ⏳ |

## Ola 4 — T5, J1, J6

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | medium | `governance_learner` | `grok-4.6` | `high` | ⏳ |
| P2 | `rules/documentation_standard.md` | modify | medium | `governance_learner` | `grok-4.6` | `high` | ⏳ |
| J6.0 | `tests/test_verify_references.py` | modify/create | medium | `devops_agent` — deviation (tests/) | `composer-2.5` | N/A | ⏳ |
| J6.1 | `scripts/verify_references.py` | modify | high | `devops_agent` | `grok-4.6` | `high` | ⏳ |

## Ola 5 — Close ledger

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `CHANGELOG.md` | modify | low | `principal_agent` | log from disk | N/A | ⏳ |
