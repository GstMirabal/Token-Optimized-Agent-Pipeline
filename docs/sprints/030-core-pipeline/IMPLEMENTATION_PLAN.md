# Implementation Plan: Sprint 030 — token-economy-enforcement

**Canonical path**: `docs/sprints/030-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/030` · **Base**: `main` at `65dbaaf`
**Status**: `APPROVED` — Phase 5 Human OK 2026-08-25 (`triple_lock` lock 1)

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

El apéndice 030 de `docs/roadmaps/core/pipeline/021-030-program-queue.md` pide
tres cosas: un auditor de tokens con cuerpo, un disparo de la regla por
**consumo** (no por intención), y un protocolo de trial de modelos. 029 aparcó
`F-026-A2` aquí.

**Qué deja de ser cierto al medir contra `65dbaaf` (comandos en Verification):**

| Claim del apéndice | Medido |
| :--- | :--- |
| `skills/token-saver-auditor/scripts/` solo `__init__.py` | El directorio **no existe** (`ls skills/token-saver-auditor/` → `README.md` `SKILL.md`) |
| `model:` en 0 de 13 perfiles | **13/13** tienen `model:` |
| Columnas Model/Effort ausentes | Ya están en `pipeline_workflow.md` Fase 4.3 y en `task_scope` 028/029; el hueco es que **nada falla** si se omiten |
| Detector de modelos nuevos | `scripts/detect_new_models.py` ya existe; falta el protocolo de trial |

`session_cost.py` lee solo `~/.claude/projects/`. `probe_cost` puede atribuir
una sesión Claude a un start Cursor, y en Claude mide la sesión viva (hallazgo
023, sin rutar).

Hecho cuando 030 cierra: `audit_plan.py` invocable; globs de
`token_economy.md` ya no son `**/*`; `check_task_scope.py` cierra `F-026-A2`;
el primer trial de author más barato queda **declarado para 031**.

---

## Design

**D1 — Cuerpo real, no retiro.** Un skill knowledge-only sin invocador es la
misma clase que `F-026-A2`. Un `__init__.py` vacío está prohibido (`C4` / `§3`).
`audit_plan.py` rechaza anti-patrones estructurales del plan. Filter 5 no se
reimplementa: sigue en `scan_workflow_determinism.py`.

**D2 — Carga por consumo.** `config/rule_triggers.json` deja de usar `**/*`.
La sección Cost del plan es la mitad portable (Cursor no expone `cache_read`).
`measure_previous` excluye el `session_id` vivo y no reporta jsonl Claude
cuando `session_tool` es `cursor`.

**D3 — Trial = 031.** 030 escribe la guía. Ejecutar el trial aquí confunde
evidencia (mecanismo + cambio de author a la vez). Gates no bajan (ADR-0003).

**D4 — `F-026-A2`.** `check_task_scope.py` mira solo el sprint actual (o un
`--sprint-dir` que declare Cursor / Model|Effort). Históricos 021–027: skip
exit 0. `make verify` no apunta `audit_plan.py` a planes < 030.

---

## Work

Una unidad = un fichero = un commit (`RA-08`, `jurisdictional_lock`).

### Ola 0 — Tests

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A0 | `tests/test_token_saver_auditor.py` | create | medium | `devops_agent` | ⏳ |
| T0 | `tests/test_check_task_scope.py` | create | medium | `devops_agent` | ⏳ |
| C0 | `tests/test_session_protocol.py` | modify | medium | `devops_agent` | ⏳ |

### Ola 1 — Auditor

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `skills/token-saver-auditor/scripts/__init__.py` | create | low | `skill_architect` | ⏳ |
| A2 | `skills/token-saver-auditor/scripts/audit_plan.py` | create | high | `devops_agent` | ⏳ |
| A3 | `skills/token-saver-auditor/SKILL.md` | modify | medium | `token_economy_agent` | ⏳ |
| A4 | `skills/token-saver-auditor/README.md` | modify | low | `skill_architect` | ⏳ |

### Ola 2 — Consumo

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/session_cost.py` | modify | high | `devops_agent` | ⏳ |
| C2 | `scripts/session_probe.py` | modify | high | `devops_agent` | ⏳ |
| C3 | `config/rule_triggers.json` | modify | medium | `devops_agent` | ⏳ |
| C4 | `rules/token_economy.md` | modify | medium | `token_economy_agent` | ⏳ |
| C5 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | medium | `governance_learner` | ⏳ |
| C6 | `agents.md` | modify | high | `governance_learner` | ⏳ |

C6: una línea en la tabla §0. `wc -l agents.md` debe seguir `≤ 200`.

### Ola 3 — F-026-A2

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F1 | `scripts/check_task_scope.py` | create | high | `devops_agent` | ⏳ |
| F2 | `agents/rule_validator.md` | modify | medium | `rule_validator` | ⏳ |
| F3 | `agents/token_economy_agent.md` | modify | medium | `token_economy_agent` | ⏳ |
| F4 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | ⏳ |

### Ola 4 — Invocadores

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `workflows/pipeline_workflow.md` | modify | medium | `orchestrator` | ⏳ |
| I2 | `workflows/close_workflow.md` | modify | medium | `orchestrator` | ⏳ |
| I3 | `Makefile` | modify | medium | `devops_agent` | ⏳ |

Tras I1/I2: `python3 scripts/map_workflows.py` regenera
`docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (generado, no unidad aparte).

### Ola 5 — Protocolo y ledger

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | create | low | `doc_orchestrator` | ⏳ |
| E2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | ⏳ |
| L1 | `CHANGELOG.md` | modify | low | `principal_agent` | ⏳ |

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | This sprint adds no package |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `audit_plan.py` on the current sprint plan | script | `pipeline_workflow.md` Phases 1 and 5; `Makefile` `verify` (`--current-sprint`, skip if sprint id < 30 or no plan) |
| `check_task_scope.py` on the current sprint scope | script | `close_workflow.md` Phase 2.6; `pipeline_workflow.md` Phase 4.3; `Makefile` `verify` (`--current-sprint`, skip if no file) |
| Token-economy rule load | glob (not `**/*`) | `config/rule_triggers.json` → Cursor `.mdc` via `install.py --target cursor` |
| `session_cost.measure_previous` live-id / tool filter | script | `session_probe.py` `probe_cost` |
| Model-tier trial protocol | agent, once per release | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md`; first trial declared 031 |
| Unattended `/loop` of Phases 6-8 | script | `scripts/loop_guard.py start` before the first iteration; never wraps Phase 5 |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` (Cursor: one agent, eight phases) | `docs/active_state.json` `delegation_mode` |
| Work units | 24 rows in Work above | `grep -c '| ⏳ |' docs/sprints/030-core-pipeline/IMPLEMENTATION_PLAN.md` after Status still pending; after execution, count `#` rows in Work tables |
| Subagents dispatched | 0 (Cursor cannot instantiate the eight roles) | `delegation_mode` |
| `session_cost` this session | Not measurable (Cursor transcripts have no `cache_read`) | `python3 scripts/session_cost.py --from-anchor --json` must not name a Claude jsonl |
| Remaining-cost rule | Soft 5× / hard 15× still apply when a Claude transcript for **this** tool exists | `rules/token_economy.md` §3.1 |

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `audit_plan.py` on 029's plan (no Cost section) | **Yes** — this is the defect |
| `check_task_scope.py` on a Cursor fixture without Model/Effort | **Yes** — the check does not exist |
| `measure_previous` returns the live session id | **Yes** — 023 unrouted finding |
| `probe_cost` under `session_tool: cursor` reports a Claude jsonl | **Yes** — tool mismatch |
| `rule_triggers.json` token_economy globs contain `**/*` | **Yes** — this is the defect |
| `make verify` | **No** — regression to protect |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/029-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `2` (no Cost section) |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/030-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/024-core-pipeline; echo $?` | `0` (historical skip) |
| `python3 -c "import json; print(json.load(open('config/rule_triggers.json'))['rules'][2]['globs'])"` | list without `**/*` |
| `wc -l agents.md` | `≤ 200` |
| `make verify; echo $?` | `0` |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `skills/token-saver-auditor/` | Executable Three-File: `scripts/audit_plan.py` |
| `scripts/session_cost.py`, `scripts/session_probe.py` | Live-id exclusion; Cursor does not inherit Claude transcripts |
| `config/rule_triggers.json` + `rules/token_economy.md` + `agents.md` §0 | Consumption-scoped load |
| `IMPLEMENTATION_PLAN_TEMPLATE.md` | Mandatory Cost section from 030 |
| `scripts/check_task_scope.py` | Shape + high-risk mechanical note |
| `pipeline_workflow.md`, `close_workflow.md`, `Makefile` | Invokers |
| `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | Trial protocol; first trial = 031 |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | Close `F-026-A2` |
| `021-030-program-queue.md`, `CHANGELOG.md` | Sprint 030 record |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `F-021-A2` implementer role | Role-map redesign; stays open |
| `F-093-G1` Double-Gate severity | Carried → `031` `gate-verdict-classes` |
| Author-tier trial **inside** 030 | Confounds evidence; first trial = 031 |
| Parsing Cursor transcripts for `cache_read` | Not on disk here |
| `last_platform_probe` writer | Sprint 023, not token-economy |
| Growing `agents.md` past 200 lines | J1; trigger prose only |

---

## Abort criterion

1. Falso positivo de `audit_plan.py` o `check_task_scope.py` que bloquee un host o un sprint record histórico → revertir ese script, no hot-patch.
2. Glob tan estrecha que `token_economy.md` no carga al redactar un plan → revertir `config/rule_triggers.json`.
3. `wc -l agents.md` > 200 en cualquier commit del sprint → revertir ese commit; el texto va a `rules/`.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo |
| **Date** | 2026-08-25 |
| **Plan commit at approval** | 9d5ce94 |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

Human draft OK 2026-08-25: *"ok"* (plan attached). Phase 5 Human OK same day: *"ok"*.