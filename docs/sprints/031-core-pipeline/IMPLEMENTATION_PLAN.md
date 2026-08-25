# Implementation Plan: Sprint 031 — gate-verdict-classes

**Canonical path**: `docs/sprints/031-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/031` · **Base**: `main` at `85f338e` (`v4.13.1`)
**Status**: `APPROVED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

`F-093-G1`: el Double-Gate no tiene clase de severidad, así que un tope de
rondas no puede disparar. Reproducido contra `85f338e` (`v4.13.1`) con los
mismos comandos que el hallazgo contra `84201d2`.

| Check | Resultado |
| :--- | :--- |
| `grep -nE 'APPROVED\|REJECTED\|RECORD\|CARRY' rules/qa_and_testing.md` | **vacío** — §4 nombra Structural Halt y Functional Lock, luego el bucle de remediación; no nombra un conjunto de veredictos |
| `grep -n rejection_trigger agents/qa_agent.md agents/tester_agent.md` | `qa_agent.md:20` y `tester_agent.md:21` — *"forcefully rejects"*; bounce binario, sin tercera clase |
| `grep -n consecutive workflows/pipeline_workflow.md workflows/remediation_workflow.md` | Phase 7 y Phase 0 disparan al **mismo bloque de lógica** tres veces, no por clase |
| `grep -n 'instruct; annotate' agents.md rules/qa_and_testing.md` | **vacío** en ambos |
| `grep -n 'documents that instruct' docs/sprints/023-core-pipeline/task_scope.md` | dos hits, líneas 714 y 817 — C6 no tiene casa en `agents.md` §7 ni en `qa_and_testing.md` |

Hecho cuando 031 cierre: `rules/qa_and_testing.md` §4 nombra las tres clases;
ambos perfiles de gate emiten `APPROVED` \| `REJECTED` \| `RECORD`; un sprint
cuyos hallazgos restantes sean todos `testifying` puede cerrar tras la ronda 1
sin remediación; `F-093-G1` se tilda contra ese commit.

**Decisión humana (2026-08-25):** el primer trial de modelo `author` **no** entra
en 031. Mezclar clases de veredicto y un author más barato impide atribuir las
rondas a ninguno de los dos. Destino: **032**. La guía de trial se corrige en
este sprint (documento que instruye; si sigue diciendo 031, miente).

El fichero `docs/sprints/core/pipeline/031_implementation_plan.md` es un plan
*telemetry/mirror* ya cerrado, ruta antigua. No es este sprint.

---

## Design

**D1 — Tres clases, tres veredictos emitibles (no cuatro, no un tope de rondas).**

- `APPROVED` — sin hallazgos.
- `REJECTED` — clase `charter` (plan/ADR incumplido, suite funcional en rojo,
  secreto, falta `task_scope.md`) **o** clase `instructing` (un fichero que le
  dice a un agente qué hacer afirma un procedimiento falso: `agents.md`,
  `rules/`, `workflows/`, skill `SKILL.md`). Bounce hasta corregirlo.
- `RECORD` — solo clase `testifying` (logs de sprint, comentarios, observaciones
  de Makefile, afirmaciones sobre un mecanismo que ya funciona). Anotar y
  embarcar. **No** incrementa el contador de rechazos del mismo bloque. **No**
  invoca remediación.

Rechazado: alias `CARRY`; “máximo N rondas” (el host que reportó ya tenía N=2 y
no disparó); subir el umbral de three-strikes (instrumento equivocado para un
comentario obsoleto).

**D2 — C6 pasa a ser la regla, no una línea de log.** La tabla operativa vive
en `qa_and_testing.md` §4 (carga perezosa). `agents.md` §7 recibe **RA-17** como
índice de una línea que apunta a esa sección. Techo J1: `wc -l agents.md` sigue
`≤ 200` (hoy 175; `wc -l agents.md`). Si la fila no cabe, solo se embarca §4 y
RA-17 se aborta hacia el fichero de regla.

**D3 — Pin determinista, solo el sprint actual.** Solo prosa es como murió C6.
`scripts/check_gate_log.py` sigue el patrón de `scripts/check_task_scope.py`:

- Omitir sprint id menor que 31 (los `SPRINT_LOG` históricos son
  `APPROVED`/`REJECTED` sin clase; 030 es el espécimen).
- Desde 031: cada fila Gate-1 y Gate-2 emite uno de `APPROVED` \| `REJECTED` \|
  `RECORD`; `REJECTED` exige clase `charter` o `instructing`; `RECORD` exige
  clase `testifying`; las filas `RECORD` se excluyen del recuento de rechazos
  consecutivos.
- Exit `2` si viola (RA-11).
- Invocadores (`RA-16`): `close_workflow.md` Phase 2.6, `pipeline_workflow.md`
  Phase 7, `Makefile` `verify`.

**D4 — ADR-0008 (Nygard).** Trigger 2: cambia el contrato que cada sprint de
host consume en Phase 7. No MADR (un solo trigger, no 1/3/5/7). `RECORD` es un
veredicto de Phase 7 **completado**: el close (“un veredicto QA y un veredicto
Tester”) lo acepta; no es un gate ausente.

**D5 — `F-021-A2` no se toca.** No hay implementer. Las escrituras siguen el
ruleset del assignee nombrado; bajo Cursor `sequential` la misma sesión las
autoría. `devops_agent` posee `scripts/` y `Makefile` (`F-086-A1`).

**D6 — Colisión de ID.** No borrar
`docs/sprints/core/pipeline/031_implementation_plan.md`. El 031 canónico es
`docs/sprints/031-core-pipeline/`.

---

## Work

Una unidad = un fichero = un commit (`RA-08`, `jurisdictional_lock`).

### Ola 0 — Tests (`RA-13`: que falle contra el árbol actual primero)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | `tests/test_check_gate_log.py` | create | medium | `devops_agent` | ⏳ |

Fixtures de T1: log anterior a 031 omitido exit 0; 031 `REJECTED` sin clase
exit 2; `RECORD`+`testifying` exit 0; tres filas `RECORD` no cuentan como
disparo de remediación; el `qa_and_testing.md` vivo debe nombrar `RECORD` en §4
(falla hasta R1).

### Ola 1 — Documentos que instruyen

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `rules/qa_and_testing.md` | modify | high | `governance_learner` | ⏳ |
| R2 | `agents/qa_agent.md` | modify | high | `qa_agent` | ⏳ |
| R3 | `agents/tester_agent.md` | modify | high | `tester_agent` | ⏳ |
| R4 | `workflows/pipeline_workflow.md` | modify | high | `governance_learner` | ⏳ |
| R5 | `workflows/remediation_workflow.md` | modify | high | `governance_learner` | ⏳ |
| R6 | `agents/orchestrator.md` | modify | medium | `orchestrator` | ⏳ |
| R7 | `agents.md` | modify | high | `governance_learner` | ⏳ |

R1: tabla clase/veredicto en §4; `RECORD` fuera del recuento de rechazos
consecutivos. R2/R3: `rejection_trigger` + `verdict_routing` emiten el trío.
R4: Phase 7 conjunto emitible + invocador del checker. R5: Phase 0 solo
`REJECTED` consecutivos del mismo bloque; `RECORD` no cuenta. R6: formato de
`gate_transcription` (`Verdict` + `Class`). R7: `RA-17` índice de una línea;
abortar esa unidad si `wc -l agents.md` superaría 200.

### Ola 2 — Mecanismo

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/check_gate_log.py` | create | high | `devops_agent` | ⏳ |
| M2 | `Makefile` | modify | medium | `devops_agent` | ⏳ |
| M3 | `workflows/close_workflow.md` | modify | high | `governance_learner` | ⏳ |

M1: `invoked_by` en el docstring del módulo. M2: `verify` llama
`--current-sprint` después de `check_task_scope.py`. M3: Phase 2.6 ejecuta el
checker; `RECORD` cuenta como veredicto declarado.

### Ola 3 — Documental (no el ledger de closeout)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/decisions/ADR-0008-gate-verdict-classes.md` | create | medium | `doc_orchestrator` | ⏳ |
| D2 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | medium | `doc_orchestrator` | ⏳ |
| D3 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | ⏳ |

D2: primer trial = **032**. D3: 031 en vuelo; destino del trial 032.

Cierre (Phase 8, no estas filas): tildar `F-093-G1` en
`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`; entrada `[Unreleased]` en
`CHANGELOG.md`.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | El sprint no añade dependencias |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `scripts/check_gate_log.py` | script | `workflows/close_workflow.md` Phase 2.6; `workflows/pipeline_workflow.md` Phase 7; `Makefile` `verify` |
| Clasificación charter / instructing / testifying | agent judgment (Filter 5: semántica, sin equivalente determinista) | `agents/qa_agent.md` / `agents/tester_agent.md` emiten; `agents/orchestrator.md` transcribe |

La clase la declara el gate en el `SPRINT_LOG.md`. El script no clasifica
hallazgos: comprueba vocabulario, omisión de sprints con id menor que 31, y que `RECORD`
no cuente hacia remediación.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | 14 | Count of rows in Work tables (T1 + R1–R7 + M1–M3 + D1–D3) |
| Subagents dispatched | 0 | Cursor `sequential` |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` |

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `qa_and_testing.md` nombra `RECORD` en §4 | **Yes** — este es el defecto (`grep` vacío) |
| Fixture de log 031 `REJECTED` sin clase | **Yes** — el checker aún no existe; T1 se escribe primero |
| `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/030-core-pipeline` | **No** — regresión a proteger (skip exit 0) |

---

## Verification

Leer exit codes con `$?` directamente; nunca a través de un pipe.

| Command | Expected |
| :--- | :--- |
| `python3 scripts/check_gate_log.py --sprint-dir docs/sprints/030-core-pipeline; echo $?` | `0` (skip histórico) |
| Fixture 031 `REJECTED` sin clase; `echo $?` | `2` |
| Fixture 031 `RECORD` + `testifying`; `echo $?` | `0` |
| `grep -n RECORD rules/qa_and_testing.md agents/qa_agent.md agents/tester_agent.md` | hits en los tres |
| `grep -n 'instruct; annotate' rules/qa_and_testing.md` | hit |
| `wc -l agents.md` | `≤ 200` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/031-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `make verify; echo $?` | `0` |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `rules/qa_and_testing.md` | §4 nombra clases y veredictos; `RECORD` fuera del recuento de remediación |
| `agents/qa_agent.md`, `agents/tester_agent.md` | emiten `APPROVED` \| `REJECTED` \| `RECORD` + clase |
| `agents/orchestrator.md` | transcribe `Verdict` + `Class` |
| `workflows/pipeline_workflow.md` | Phase 7 conjunto emitible + invocador |
| `workflows/remediation_workflow.md` | Phase 0 ignora `RECORD` |
| `workflows/close_workflow.md` | Phase 2.6 corre el checker; `RECORD` es veredicto válido |
| `Makefile` | `verify` invoca `check_gate_log.py --current-sprint` |
| `scripts/check_gate_log.py`, `tests/test_check_gate_log.py` | pin determinista |
| `agents.md` | `RA-17` índice de una línea, si el techo de 200 lo permite |
| `docs/decisions/ADR-0008-gate-verdict-classes.md` | por qué existe `RECORD` |
| `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | primer trial = 032 |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | 031 en vuelo; trial → 032 |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | tildar `F-093-G1` en Phase 8 |
| `CHANGELOG.md` | entrada `[Unreleased]` en Phase 8 |

**Figuras medidas.** Cada número de Context / Design / Verification lleva el
comando que lo reproduce (T5). `wc -l agents.md` → 175 en este HEAD; techo 200
es J1 de `021-030-program-queue.md`.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Trial de modelo `author` | Confunde evidencia de rondas; destino **032** |
| Rol implementer (`F-021-A2`) | Rediseño del mapa de roles; sigue abierto |
| Tope de N rondas | El hallazgo lo prohíbe |
| Clasificar logs 021–030 | Skip, no reescritura |
| Borrar `docs/sprints/core/pipeline/031_implementation_plan.md` | Plan histórico distinto; no es este 031 |
| `gh auth refresh` / platform probe | Operación de sesión, no este sprint |

---

## Abort criterion

1. El checker marca un `SPRINT_LOG` histórico (021–030) → revertir el script,
   conservar la omisión.
2. Un hallazgo `RECORD` es un secreto, una suite funcional en rojo, o un
   procedimiento instructor falso → revertir la regla de clasificación, no el
   sprint del host.
3. `wc -l agents.md` > 200 en cualquier commit del sprint → revertir ese
   commit; el texto se queda en `rules/`.
4. La calidad del gate se hunde porque todo se marca `RECORD` → abortar;
   restaurar el bounce binario; dejar el ADR como rechazado.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo (Human OK: "ok") |
| **Date** | 2026-08-25 |
| **Plan commit at approval** | `61581b6` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).*
*Filter 6: cualquier `/loop` de Phases 6–8 se arma con `python3 scripts/loop_guard.py start`.*
