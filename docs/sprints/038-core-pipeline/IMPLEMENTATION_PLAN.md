# Implementation Plan: Sprint 038 — family-trial

**Canonical path**: `docs/sprints/038-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/038` · **Base**: `main` at `171531a` (`v4.20.0` + reconcile `#037`)
**Status**: `APPROVED`

> Authored at Phase 1 (Planning) by `principal_agent`. Under `session_tool: cursor`,
> `SwitchMode` to plan is PROHIBITED (`RA-18`). Committed before Phase 5
> (`agents.md §2 triple_lock`). Spanish permitted in this document (`agents.md §1 user_chat`).

---

## Context

Sprint **038** is the program-queue slot that 034 O3/O4 and 035 parked: **family
trial of `cursor.author`** plus **execution of gate-replay (D16)**. Protocol
sprints 034–037 are deployed (`v4.17.0`–`v4.20.0`). 037 Q7: first usable ledger
row + baseline 032/033 is enough to start. Ledger exists.

Medido 2026-08-26, sesión Cursor `20260826T100341Z-67664`, `HEAD` `171531a`:

| Fact | Measurement | Reproduce |
| :--- | :--- | :--- |
| Incumbente `cursor.author` | `grok-4.5` / `xai` / `high` | `python3 -c "import json; a=json.load(open('config/model_tiers.json'))['tiers']['author']['cursor']; print(a)"` |
| `cursor.gate` (no tocar) | `claude-opus-5` / `anthropic` / `max` | same for `tiers.gate.cursor` |
| `cursor.mechanical` (no tocar) | `composer-2.5` / `cursor` | same for `tiers.mechanical.cursor` |
| Catálogo Cursor | **35** modelos tras filtros duros; `glm-5.2` presente (`zhipu`, depth lever yes) | `make cursor-tiers` |
| Applied vs mapa | Applied `grok-4.6` ≠ mapa `grok-4.5` | `make cursor-tiers` línea `Applied model` |
| Ledger 032–037 | 032–037 todos Gate1/Gate2 **1** ronda, veredicto `APPROVED` (035 añade `RECORD:testifying`) | `make model-ledger`; `docs/audits/MODEL_LEDGER.md` |
| Línea base D12 (2 sprints incumbente) | 036 y 037 (no 032/033: esos son el corpus de **replay**, no la línea base viva) | mismas filas ledger `36`,`37` vs `32`,`33` |
| Briefing «Still open» | **5** (falso: set formal vacío desde 033) | `python3 scripts/session_start.py` |
| Set formal UPSTREAM | `*(none in this file's open set)*` en Status **033** | `rg -n 'Status at Sprint 033' -A6 docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` |
| `--resolve author` / `gate` | `grok-4.5`/`high` · `claude-opus-5`/`max` | `python3 scripts/audit_cursor_models.py --resolve author` (resp. `gate`) |
| Coste sesión | n/a (Cursor / sin transcript Claude) | `python3 scripts/session_cost.py --from-anchor --json` |

**Hecho cuando 038 cierre:** `cursor.author` se **promueve** al candidato de
familia (D6-P6 + Human OK) **o** se **revierte** C1 al incumbente `grok-4.5`;
gate-replay de 032 y 033 queda registrado con vocabulario ADR-0008; el briefing
de `/start` reporta el set abierto del Status de sprint **más alto**, no la
suma de snapshots históricos.

**Hereda (no reabrir):** D4/D6/D7/D12/D13/D15/D16 de
`docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md`; protocolo en
`docs/guides/MODEL_TIER_TRIAL_GUIDE.md` (E0 / 035); ledger G / 037. Cadencia
author: **una** por ciclo de release (D12).

### Phase 1 — defaults (Human OK 2026-08-26 — «ok»)

| # | Pregunta | Decisión | Por qué |
| :--- | :--- | :--- | :--- |
| **Q1** | Candidato `cursor.author` (O4) | **`glm-5.2`** / familia `zhipu` / effort **`high`** | Slug exacto en catálogo (D6-P2). **No** `claude-opus-5`: D15 exige familia gate ≠ author y el gate ya es `anthropic`. Una variable: familia, no effort (032 D1). 034/035 nombraron Opus·GLM; Opus queda fuera por D15 |
| **Q2** | ¿Gate-replay D16 en el mismo sprint? | **Sí**, track R, offline sobre diffs 032 y 033, con el **gate vivo** (`claude-opus-5` / `max`) | D16: replay no mezcla instrumento y medido (diff inmutable). No es un segundo family-trial de gate |
| **Q3** | Payload de autoría | Arreglar el contador «Still open» de `session_start.py` (037 Q5) | Defecto medido hoy; tamaño comparable a 032 (no CE-5, no abaratar gate) |
| **Q4** | Applied `grok-4.6` vs mapa | Opción B 032: atestación en `SPRINT_LOG.md` de que la autoría de 038 corre en **`glm-5.2`**. No abortar por la clave global | `audit_cursor_models.py` solo lee `applicationOpenModelAppliedConfig` |

---

## Design

| ID | Decision | Why (rejected alternative) |
| :--- | :--- | :--- |
| **D-T1** | Una variable experimental: **familia** de `cursor.author`. Effort permanece `high`. `cursor.gate` y `cursor.mechanical` no se tocan. `claude_code.*` no se toca | Rechazado: otra generación Grok (D4); Opus como author (rompe D15); bajar effort a la vez; trial mid-sprint |
| **D-T2** | Candidato = `glm-5.2` (Q1). Promoción solo al close con D12 sobre ledger 038 vs línea base **036+037**: cero `REJECTED` `charter`; `instructing` ≤ incumbente; empate → menos rondas; Human OK (D6-P4/P6) | Rechazado: promover por anuncio, benchmark o replay limpio (D7) |
| **D-T3** | Evidencia de autoría = mapa C1 **más** atestación humana si el medidor global no coincide (Q4) | Igual que 032 D2. El mapa no cambia el modelo del chat |
| **D-T4** | Payload = `section_upstream` lee **solo** la tabla `**Status at Sprint NNN**` con N máximo; reporta esa celda Still open. Historial no suma | Rechazado: reescribir UPSTREAM; contar hallazgos sueltos en prosa (línea 288) |
| **D-R1** | Replay = pasar `cursor.gate` vivo sobre el merge range de **032** (`d5fd1e9` vs base) y **033** (`05556f1` vs base). Registrar cada hallazgo `APPROVED` \| `REJECTED` \| `RECORD` + clase. Un replay limpio **no** prueba superioridad (guía §5.1) | Rechazado: replay de un candidato de gate más barato en 038 (segunda variable; abaratar gate está fuera de 034–038) |
| **D-R2** | Artefacto `docs/sprints/038-core-pipeline/GATE_REPLAY.md` (no editar `SPRINT_LOG` de 032/033). `SPRINT_LOG` de 038 apunta a ese fichero | Rechazado: reescribir logs cerrados; afirmar calidad interfamiliar |

---

## Work

Una unidad = un fichero = un commit (`RA-08`, `jurisdictional_lock`). **C1
primero** para que T1/M1/D\* se autoríen bajo el candidato. Assignee propuesto
— Phase 4.1 puede sobrescribir. Cursor `sequential`: la sesión padre ejecuta.

### Track T — family trial (`cursor.author`)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `config/model_tiers.json` | modify | medium | `implementer_agent` | ⏳ |
| T1 | `tests/test_session_start.py` | modify | medium | `implementer_agent` | ⏳ |
| M1 | `scripts/session_start.py` | modify | high | `implementer_agent` | ⏳ |
| D1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | low | `doc_orchestrator` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | ⏳ |

C1: `cursor.author` → `model: glm-5.2`, `family: zhipu`, `effort: high`; comentario de trial 038. No tocar gate/mechanical/claude_code. Phase 8: Human OK para dejar o revertir **el mismo fichero**. `token_economy_agent` propone la celda (sin `Write`); `implementer_agent` aplica (`check_task_scope` exige Write/Edit).

T1 (`RA-13`): fixture con Status 027 (Still open no vacío) **y** Status 033 (`*(none…)*`) → el briefing debe reportar **0** (N máximo = 033), no 1+. Falla hasta M1. Conservar caps 035 C4.

M1: `section_upstream` parsea tablas `Status at Sprint NNN`, elige max N, emite esa celda. `*(none*` → 0. Sin red.

D1: candidato 038 = `glm-5.2`; abort si la autoría no es ese slug (atestación Q4). D2: 038 in flight; next TBD at close.

### Track R — gate-replay (D16)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `docs/sprints/038-core-pipeline/GATE_REPLAY.md` | create | medium | `orchestrator` | ⏳ |

R1: dos pasadas (032, 033). Diff = merge range del PR de ese sprint vs su base. Vocabulario ADR-0008. No rankear familias. `qa_agent` emite vía `Task` + `--resolve gate` (`ADR-0010`); `orchestrator` transcribe (`F-026-A1`).

**DAG:** C1 → (T1 → M1) y D1/D2. R1 independiente de T (diff histórico). Preferir C1 antes de cualquier autoría.

**Closeout (Phase 8, no Work):** `CHANGELOG.md` `[Unreleased]`; promover o revertir C1; `make model-ledger`; `PHASE_REGISTER.md` / `graph_stats.json`; program-queue Status.

---

## Dependencies

None.

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Catálogo / `--resolve` / `--check` | script | `Makefile` `cursor-tiers`; `pipeline_workflow.md` Phase 4.3 |
| Ledger de gate rounds | script | `Makefile` `model-ledger`; `close_workflow.md` at close |
| Contador UPSTREAM del briefing | script | `scripts/session_start.py` ← `start_workflow.md` operator path |
| Comparar 038 vs 036+037 y promover C1 | agent judgment (Filter 5: semántica D12, sin equivalente determinista) | Phase 8 de este plan; Human OK |
| Gate-replay D16 | agent judgment (revisión adversarial sobre diff histórico) | Phase 6: `qa_agent` Task emite; `orchestrator` escribe `GATE_REPLAY.md` |
| Clasificación charter / instructing / testifying | agent judgment | `qa_agent` / `tester_agent` emiten; Orchestrator transcribe |

Phase 5 nunca bajo `/loop`. Phases 6–8 solo si el humano arma `loop_guard.py start` (`rules/loop_governance.md`).

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | **6** (C1, T1, M1, D1, D2, R1) | Count of Work table rows |
| Subagents dispatched | `0` under Cursor `sequential` | parent session executes; R1 may use `Task` + `--resolve gate` (ADR-0010) without changing `delegation_mode` |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` |
| Author trial | `glm-5.2` / `high` (Q1) | `make cursor-tiers`; C1 |
| Mechanical-eligible | T1 | map `mechanical` |

Soft (5×) / hard (15×) apply when a measurable Claude transcript exists for this tool — not this session.

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| Briefing «Still open» rows = 5 con set formal vacío | **Yes** — M1 |
| Fixture 027-open + 033-none reporta 0 | **Yes** — no test yet (T1) |
| `cursor.author.model` is `glm-5.2` | **Yes** — still `grok-4.5` (C1) |
| `GATE_REPLAY.md` exists with 032 and 033 sections | **Yes** — file absent (R1) |
| `audit_plan.py` on this plan | **No** — protect |

---

## Verification

Leer `$?` directamente (nunca a través de un pipe).

| Command | Expected |
| :--- | :--- |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/038-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` before Phase 5 |
| `python3 -c "import json; print(json.load(open('config/model_tiers.json'))['tiers']['author']['cursor']['model'])"` | `glm-5.2` after C1; `grok-4.5` if Phase 8 reverts |
| `python3 scripts/audit_cursor_models.py --check; echo $?` | `0` (gate family ≠ author family after C1: anthropic ≠ zhipu) |
| `python3 scripts/session_start.py` | `rows (non-empty): 0` (Status 033) |
| `python3 -m pytest tests/test_session_start.py -q; echo $?` | `0` |
| `test -f docs/sprints/038-core-pipeline/GATE_REPLAY.md; echo $?` | `0` after R1; file names 032 and 033 |
| `make model-ledger; echo $?` | `0`; 038 row present at close |
| `make verify; echo $?` | `0` outside sandbox |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `config/model_tiers.json` | C1 trial `cursor.author` → `glm-5.2` / `zhipu` / `high` (revertible al close) |
| `tests/test_session_start.py` | T1 — Status table de sprint máximo |
| `scripts/session_start.py` | M1 — deja de sumar snapshots históricos |
| `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | D1 — candidato 038 |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | D2 — 038 in flight |
| `docs/sprints/038-core-pipeline/GATE_REPLAY.md` | R1 — create |
| `docs/sprints/038-core-pipeline/*` | plan, scope, log, register, graph_stats |
| `docs/audits/MODEL_LEDGER.md` | regenerado al close (no a mano) |
| `CHANGELOG.md` | `[Unreleased]` Sprint 038 (Phase 8) |

**Measured figures** above carry reproduce commands (J6 / T5).

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `claude-opus-5` como `cursor.author` | D15: gate ya es anthropic |
| Abaratar `cursor.gate` / `load_proven_families()` | Fuera 034–038; ADR-0003 cláusula coste |
| CE-5 pytest/`git init` sandbox | Deferred 036 O5; distinto de rider S |
| Otra generación Grok (`grok-4.6` applied) | D4: este ciclo es **familia**, no generación |
| Scores o $/1M en `model_tiers.json` | ADR-0005 |
| Reescribir `SPRINT_LOG` 026–037 | Census/ledger; replay escribe artefacto nuevo |
| Afirmar que una familia es mejor que otra | D13 / D7 |
| `ruff` en `verify` | Fuera de este programa |

---

## Abort criterion

Stop and revert the offending unit (do not ship a partial trial as "promoted") if:

1. C1 escribe `claude-opus-5` (u otra familia `anthropic`) en `cursor.author` mientras `cursor.gate` sigue anthropic; or
2. Tras C1, `python3 scripts/audit_cursor_models.py --check` sale ≠ 0; or
3. El trial cambia `cursor.gate` o `cursor.mechanical`; or
4. Gate-replay se usa para **rankear** familias o para promover el mapa de gate; or
5. Gate quality collapses (D12 restricción dura 1: `REJECTED` `charter`) — revertir C1 a `grok-4.5`; or
6. El humano retira la atestación Q4 y el chat no corre `glm-5.2`; or
7. `session_start.py` vuelve a sumar filas históricas de Still open después de M1.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo |
| **Date** | 2026-08-26 |
| **Plan commit at approval** | `05b4d7b` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop`. Phases 6–8 only if the human arms `loop_guard.py start` first
(`rules/loop_governance.md`).*
