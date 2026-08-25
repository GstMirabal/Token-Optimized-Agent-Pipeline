# Implementation Plan: Sprint 032 — author-tier-trial

**Canonical path**: `docs/sprints/032-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/032` · **Base**: `main` at `0429f03` (`v4.14.0`)
**Status**: `EXECUTING`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

Sprint 030 escribió el protocolo de trial; Sprint 031 lo destaged a **032**
porque mezclar clases de veredicto y un `author` más barato impide atribuir las
rondas a ninguno de los dos. `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` ya nombra
032 como primer trial. Este sprint **ejecuta** ese protocolo, no lo vuelve a
inventar.

Medido contra `0429f03` (`v4.14.0`) el 2026-08-25, sesión Cursor
`20260825T162044Z-31194`:

| Claim | Resultado | Reproduce |
| :--- | :--- | :--- |
| `cursor.author` vigente | `grok-4.6` / `high` | `python3 -c "import json; a=json.load(open('config/model_tiers.json'))['tiers']['author']['cursor']; print(a['model'], a['effort'])"` |
| Candidato en catálogo (depth lever) | `grok-4.5` aparece; `applied` = `grok-4.6` | `python3 scripts/audit_cursor_models.py` (35 modelos tras filtros; `Applied model: grok-4.6`) |
| Gates 031 (baseline) | QA ronda 1 `APPROVED`; Tester ronda 1 `APPROVED`; `RECORD` no usado | `grep -n 'Round' docs/sprints/031-core-pipeline/SPRINT_LOG.md` |
| `last_platform_probe` writer | **cero escrituras** en Python; una lectura | `rg -n last_platform_probe --glob '*.py'` → `scripts/session_probe.py:12` (docstring) y `:494` (`state.get`) |
| Clave en el ancla tras `/start` | ausente | `python3 -c "import json; print(json.load(open('docs/active_state.json')).get('last_platform_probe'))"` → `None` |
| ADR-0003 | `qa_agent` / `tester_agent` / `principal_agent` no bajan de `gate` | `docs/decisions/ADR-0003-gates-never-drop-tier.md` |
| `detect_new_models.py --check` | exit `0`; sin catálogo bundled en esta máquina | `python3 scripts/detect_new_models.py --check; echo $?` |

El payload de autoría (para que el trial tenga rondas que comparar, no un
JSON solo) es el hallazgo **sin rutar** de Sprint 023: el cache de 7 días del
platform probe está declarado en `start_workflow.md` Phase 0.7 y nunca se
escribe. 030 lo excluyó (“Sprint 023, not token-economy”). Sigue siendo cierto
en este HEAD.

Hecho cuando 032 cierre: `cursor.author` se promueve a `grok-4.5` **o** se
revierte a `grok-4.6` con Human OK explícito; `session_probe.py` deja
`last_platform_probe` en el ancla y el espejo tras una interrogación real;
`SPRINT_LOG.md` registra cada `Gate N, round R — APPROVED|REJECTED|RECORD` con
clase; `F-021-A2` sigue abierto.

El fichero `docs/sprints/core/pipeline/032_implementation_plan.md` es un plan
*topological flattening* ya cerrado, ruta antigua. No es este sprint.

---

## Design

**D1 — Una variable experimental: generación `author` en Cursor, no effort ni familia ni gates.**

Candidato: `cursor.author.model` = `grok-4.5`, `effort` = `high` (igual que
hoy). Misma familia `xai`, generation anterior en el catálogo de esta sesión.
`cursor.mechanical` sigue `composer-2.5`. `cursor.gate.model` sigue `null`
(ADR-0003 + Design §D7 de 026: sin historia medida). `claude_code.author`
sigue `sonnet` — esta sesión es Cursor; un trial Claude sin ejecución Claude
no produce evidencia.

Rechazado: `grok-4.6` + `effort` `medium` (cambia la palanca, no el modelo);
`composer-2.5` como author (sin depth lever; es mechanical); cambiar de
familia (Gemini/GPT/Claude) en el primer trial (segunda variable); bajar
gates.

**D2 — Evidencia del modelo de autoría: medidor global **o** atestación humana.**

`config/model_tiers.json` no cambia el modelo del chat.
`scripts/audit_cursor_models.py` lee solo
`cursor/applicationOpenModelAppliedConfig` (default global). Un override
**por chat** a `Cursor Grok 4.5` no escribe ese key — medido 2026-08-25:
tras selección manual del chat, el key seguía `grok-4.6` y cero filas con
`modelId: "grok-4.5"`.

**Decisión humana (Phase 6, opción B, 2026-08-25):** el trial sigue en este
hilo bajo atestación humana de que la autoría corre en **Cursor Grok 4.5**.
Evidencia: fila en `SPRINT_LOG.md` + C1 en el mapa. El medidor global puede
seguir mostrando `grok-4.6` sin invalidar el trial. Las fases de gate no usan
ese modelo (ADR-0003). Planificación Phase 1 bajo `grok-4.6` no contamina.

**D3 — Payload: writer de `last_platform_probe`, no más RA-16.**

Tras una interrogación de plataforma que **sí corre** (no skip por `gh`
ausente, remoto no GitHub, `acknowledged_gaps.platform`, ni TTL fresco),
`session_probe.py` escribe `last_platform_probe` en ISO-8601
`%Y-%m-%dT%H:%M:%SZ` vía `session_state.save_state` (ya refresca el espejo).
Los skips no crean ni actualizan la clave. `--force-platform` escribe después
de correr. `session_state.py claim` ya preserva claves extra (`state.update`);
no se toca.

Rechazado: ampliar `verify_references.py` a `skills/*/scripts/` (20 scripts
sin `invoked_by` romperían `make verify` y ahogarían el trial); encender
`ruff` (176 errores; migración, no trial); `F-021-A2`.

**D4 — Evidencia = tabla de rondas 032 vs 031, no un script de causalidad.**

031: ambas puertas `APPROVED` en ronda 1. 032 copia el mismo formato de
`SPRINT_LOG.md` (Phase 7, `check_gate_log.py`). Promoción de `grok-4.5` es
Human OK en Phase 8, no un default. Un script no puede atribuir un
`REJECTED` al modelo vs al payload.

**D5 — `F-021-A2` no se toca.** Las escrituras siguen el ruleset del assignee;
bajo Cursor `sequential` la misma sesión las autoría. `devops_agent` posee
`scripts/` (`F-086-A1`).

**D6 — Colisión de ID.** No borrar
`docs/sprints/core/pipeline/032_implementation_plan.md`. El 032 canónico es
`docs/sprints/032-core-pipeline/`.

---

## Work

Una unidad = un fichero = un commit (`RA-08`, `jurisdictional_lock`). C1 va
primero en ejecución para que T1/M1/D* se autoríen bajo el candidato.

### Ola 0 — Mapa de trial

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `config/model_tiers.json` | modify | medium | `token_economy_agent` | ⏳ |

`cursor.author.model` → `grok-4.5`; `effort` permanece `high`; comentario de
sprint 032 trial. No tocar `claude_code.*` ni `cursor.gate`. Phase 8: Human OK
para dejarlo o revertir C1 en el mismo fichero.

### Ola 1 — Tests (`RA-13`: que falle contra el árbol actual primero)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | `tests/test_session_protocol.py` | modify | medium | `devops_agent` | ⏳ |

Casos: interrogación mockeada con `gh` deja `last_platform_probe` en el ancla
del tmp; skip `which("gh") is None` deja la clave ausente; TTL fresco no
reescribe el timestamp. Falla hasta M1.

### Ola 2 — Mecanismo

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/session_probe.py` | modify | high | `devops_agent` | ⏳ |

Writer en `probe_platform` / `main` tras interrogación real; persistencia con
`session_state.save_state`. Docstring `invoked_by` ya nombra
`start_workflow.md` Phase 0.7.

### Ola 3 — Documental (no el ledger de closeout)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | medium | `doc_orchestrator` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | ⏳ |

D1: candidato 032 = `grok-4.5`; abort si el modelo aplicado en autoría no es
ese. D2: 032 en vuelo; `F-021-A2` sigue abierto.

Cierre (Phase 8, no estas filas): entrada `[Unreleased]` en `CHANGELOG.md`;
promover o revertir C1; comparar rondas con 031.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | El sprint no añade dependencias |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Writer + TTL de `last_platform_probe` | script | `workflows/start_workflow.md` Phase 0.7; `workflows/close_workflow.md` Phase 3.5 (`--force-platform`) |
| Catálogo Cursor (`make cursor-tiers`) | script | `Makefile` `cursor-tiers`; `workflows/pipeline_workflow.md` Phase 4.3 |
| Comparar rondas 032 vs 031 y promover el mapa | agent judgment (Filter 5: semántica, sin equivalente determinista) | Phase 8 de este plan; Human OK |
| Clasificación charter / instructing / testifying | agent judgment | `agents/qa_agent.md` / `agents/tester_agent.md` emiten; `agents/orchestrator.md` transcribe |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | 5 | Count of rows in Work tables (C1 + T1 + M1 + D1 + D2) |
| Subagents dispatched | 0 | Cursor `sequential` |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` |
| Author trial | `grok-4.5` / `high` | `python3 scripts/audit_cursor_models.py` (candidato); mapa en C1 |

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| Tras `session_probe.py` (plataforma interrogada), el ancla tiene `last_platform_probe` | **Yes** — este es el defecto (`get` → `None` tras el `/start` de esta sesión) |
| `rg -n last_platform_probe --glob '*.py'` muestra un `save_state` / write | **Yes** — solo lectura en `:494` |
| `python3 scripts/check_model_tiers.py; echo $?` | **No** — regresión a proteger (C1 no toca `claude_code`) |
| `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/031-core-pipeline; echo $?` | **No** — baseline 031 |

---

## Verification

Leer exit codes con `$?` directamente; nunca a través de un pipe.

| Command | Expected |
| :--- | :--- |
| `python3 scripts/audit_cursor_models.py` (antes de cada unidad de autoría) | Informativo. Tras decisión B: el default global puede seguir `grok-4.6`; evidencia de trial = atestación en `SPRINT_LOG` |
| `python3 -c "import json; print(json.load(open('config/model_tiers.json'))['tiers']['author']['cursor']['model'])"` | `grok-4.5` mientras el trial está en vuelo |
| Fixture: `probe_platform` mockeado con `gh`; `echo $?` del test | `last_platform_probe` presente, formato `%Y-%m-%dT%H:%M:%SZ` |
| Fixture: `which("gh")` → `None` | clave ausente |
| `python3 scripts/check_model_tiers.py; echo $?` | `0` |
| `grep -nE 'Gate \| Round' docs/sprints/032-core-pipeline/SPRINT_LOG.md` | filas QA y Tester con `APPROVED` \| `REJECTED` \| `RECORD` + clase si no `APPROVED` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/032-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `make verify; echo $?` | `0` |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `config/model_tiers.json` | `cursor.author` = `grok-4.5` durante el trial; Phase 8 confirma o revierte |
| `scripts/session_probe.py` | escribe `last_platform_probe` tras interrogación real |
| `tests/test_session_protocol.py` | pin del writer y de los skips |
| `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | candidato 032 nombrado; abort de modelo aplicado |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | 032 en vuelo |
| `CHANGELOG.md` | entrada `[Unreleased]` en Phase 8 |
| `docs/sprints/032-core-pipeline/SPRINT_LOG.md` | rondas de gate (Phase 7) |

**Figuras medidas.** Cada número de Context / Design / Verification lleva el
comando que lo reproduce (T5). Catálogo Cursor: 35 modelos tras hard filters,
sesión 2026-08-25. Baseline 031: 2 veredictos, ronda 1, ambos `APPROVED`.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Rol implementer (`F-021-A2`) | Rediseño del mapa de roles; sigue abierto |
| Trial `claude_code.author` `sonnet` → `haiku` | Sin ejecución Claude en esta sesión; otro ciclo |
| Poner valor en `cursor.gate.model` | ADR-0003 + §D7 de 026; sin historia medida |
| Ampliar `verify_references.py` a `skills/*/scripts/` | 20 scripts sin `invoked_by`; sprint propio |
| Encender `ruff check .` en `make verify` | 176 errores; migración, no trial |
| `graphify update .` | Advisory del probe de esta sesión; operación de sesión |
| Borrar `docs/sprints/core/pipeline/032_implementation_plan.md` | Plan histórico distinto; no es este 032 |
| Parser de transcripts Cursor para `cache_read` | No está en disco aquí |

---

## Abort criterion

1. El humano retira la atestación de `Cursor Grok 4.5` en este hilo, o se
   demuestra que la autoría no fue 4.5 → no contar unidades posteriores;
   revertir C1 si ya aterrizó. (El medidor global en `grok-4.6` **no** dispara
   este abort tras la decisión B de Phase 6.)
2. La calidad del gate se hunde (p. ej. `REJECTED` `instructing` en ronda 2+
   que 031 no tuvo en trabajo comparable) → abortar el trial; revertir C1;
   dejar `grok-4.5` como candidato, no como mapa.
3. Un skip (`gh` ausente / no GitHub / TTL) escribe `last_platform_probe` →
   revertir M1; el cache falso es peor que el cache ausente.
4. `cursor.gate.model` deja de ser `null` → revertir ese commit.
5. `python3 scripts/check_model_tiers.py` exit `2` por C1 → revertir C1
   (C1 no debe tocar el lado Claude).

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo (Human OK: "ok") |
| **Date** | 2026-08-25 |
| **Plan commit at approval** | `35f2331` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).*
*Filter 6: cualquier `/loop` de Phases 6–8 se arma con `python3 scripts/loop_guard.py start`.*
