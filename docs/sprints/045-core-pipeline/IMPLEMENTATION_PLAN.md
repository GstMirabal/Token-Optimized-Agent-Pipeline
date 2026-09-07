# Implementation Plan: Sprint 045 — nucleus-ruleset-mechanism-audit

**Canonical path**: `docs/sprints/045-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/045` · **Base**: `main` at `e0189a360d927d7200bb33d175f002dc0dec7b8a`
**Status**: `DRAFT` → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English — los cuatro informes de `docs/audits/` se redactan
> en inglés (`agents.md §1 code_logic` + `rules/documentation_standard.md`).

---

## Context

**Modo**: núcleo (`scripts/_mode.py` → `.git` es un directorio real; `session_tool: claude-code`, `delegation_mode: native`).

El corpus normativo del framework ha crecido 44 sprints sin una revisión sistemática de
obsolescencia. Los controles deterministas existentes verifican **forma**, no **vigencia semántica**:

| Control existente | Qué verifica | Qué NO verifica |
| :--- | :--- | :--- |
| `make verify` | Escaneo estructural (determinismo de workflows, paridad de plantillas, referencias) | Si una regla describe un mecanismo ya retirado |
| `scripts/verify_references.py` | Rutas y citas `file:line` resuelven; `config/rule_triggers.json` ↔ `agents.md`; imports Python (`RA-16` check d) | Si el trigger sigue teniendo sentido |
| `scripts/map_workflows.py` → `WORKFLOWS_STEP_MAP_GUIDE.md` | Cada paso de workflow mapeado; marca `?` los verbos no clasificables | Si un paso `?` es genuinamente ambiguo o simplemente mal redactado |
| `skills/topology-monitor/scripts/legacy_app_auditor.py` | Three-File Skill Standard | Si la skill sigue siendo invocada por algo |

Reproducción del tamaño del corpus (baseline, ejecutado en `e0189a3`):

| Figura | Comando | Valor observado |
| :--- | :--- | :--- |
| Líneas de `agents.md` | `wc -l agents.md` | 169 |
| Enmiendas `RA-*` | `grep -oE 'RA-[0-9]{2}' agents.md \| sort -u \| wc -l` | 18 (RA-01..RA-18) |
| Archivos de regla de dominio | `ls rules/*.md \| wc -l` | 11 |
| Workflows | `ls workflows/*.md \| wc -l` | 12 |
| Scripts | `ls scripts/*.py \| wc -l` | (medido en Phase 6, unidad 3) |

**Verdadero al cerrar**: existe `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` con **cada** regla de
`agents.md` (§0–§8 + RA-01..RA-18), **cada** `rules/*.md`, **cada** `workflows/*.md` y **cada**
mecanismo `scripts/`/`hooks/`/`skills/` clasificado como `VIGENTE` | `OBSOLETA` | `MEJORAR`, con
la evidencia (comando o cita) que sostiene el veredicto y — para `OBSOLETA`/`MEJORAR` — una
enmienda **redactada pero NO aplicada** y un `routing_class` (`nucleus` en su práctica totalidad).
`make verify` sigue en verde: este sprint no modifica ningún mecanismo.

---

## Design

### D1 — Sprint de análisis, no de ejecución

Decisión: el sprint entrega **informe + enmiendas propuestas**; NO retira ni reescribe ninguna
regla. Rechazado: auditar y aplicar en el mismo sprint. Razón: `agents.md` se carga en **cada
sesión de cada subagente** (`J1` del program queue); reescribir la constitución en el mismo pase
que la audita impide que un humano revise el diff de cambios normativos con la cabeza fría, y
mezcla evidencia (el informe) con acción (la enmienda) en un solo Approval Gate. La ejecución de
las enmiendas aprobadas va a un sprint posterior (recomendado en la síntesis, unidad 4).

### D2 — Descomposición por dominio, un archivo físico por unidad

`agents.md §2 jurisdictional_lock` — un subagente estructura **un** archivo físico. El corpus se
parte en tres informes de dominio + una síntesis:

| Informe | Objeto auditado | Detecta |
| :--- | :--- | :--- |
| `NUCLEUS_RULESET_AUDIT_REPORT-045.md` | `agents.md` §0–§8, RA-01..RA-18, los 11 `rules/*.md` | Solapamientos `agents.md` ↔ `rules/`, contradicciones internas, enmiendas superseded, reglas que describen mecanismos retirados, triggers sin sentido |
| `NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md` | los 12 `workflows/*.md` | Citas `Rule NN` / `RA-NN` / `§` que ya no resuelven, pasos huérfanos, referencias de ruta muertas, cobertura `invoked_by:` vs `RA-16`, pasos `?` en el step map |
| `NUCLEUS_MECHANISM_AUDIT_REPORT-045.md` | `scripts/*.py`, `hooks/*.py`, `skills/` | Cobertura de invocador `RA-16` (invocador declarado o excepción tipada en `config/invocation_exceptions.json`), hooks que deben bloquear con `sys.exit(2)` (`RA-11`), gates que pueden terminar sin clase de veredicto (`RA-17`), Three-File Skill Standard, mecanismos que nada importa ni llama |
| `NUCLEUS_AUDIT_SYNTHESIS-045.md` | los tres anteriores | Registro único rankeado con enmienda redactada y sprint de ejecución recomendado por ítem |

### D3 — Evidencia determinista antes que juicio de agente

Cada informe **ejecuta primero** las herramientas existentes y cita su salida; el juicio del
agente se limita a lo que ninguna herramienta cubre (obsolescencia semántica). Herramientas por
informe:

- Ruleset: `grep` de cada `§`/`RA` en `rules/` y `workflows/`; `scripts/verify_references.py`;
  `rules/LEGACY_RULE_CONCORDANCE.md` para cada cita `Rule NN`.
- Workflows: `python3 scripts/map_workflows.py` (regenera y compara), `scripts/verify_references.py`,
  `scripts/scan_workflow_determinism.py`, `python3 skills/slash-commander/scripts/verify_commands.py`.
- Mecanismos: `python3 scripts/verify_references.py` (check d, imports), `legacy_app_auditor.py`,
  `grep -rl` de cada nombre de script en `workflows/`, `hooks/`, `Makefile`, `config/`.

### D4 — El protocolo `/agents:audit` es una herramienta de la Phase 6, no el sprint

`workflows/audit_workflow.md` (v2.0.0) cubre Topo Sweep + Doc Purity + Verdict. Se invoca **dentro**
de la ejecución (unidad 2 y 3 lo usan como checklist), pero el sprint entrega los cuatro informes
`-045`, no el `pipeline_audit_report.md` genérico del protocolo.

### D5 — `UPSTREAM_FINDINGS_FROM_HOSTS.md` queda fuera del objeto, dentro de la referencia cruzada

El archivo (1354 líneas, 0 filas abiertas al arranque) NO se audita fila por fila — es input de
planificación de núcleo, no objeto de esta auditoría. La síntesis **sí** cruza cada `OBSOLETA`/
`MEJORAR` contra ese archivo para no proponer una enmienda que ya tiene un hallazgo upstream.

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) touching **one physical file**.

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md` | create | low | `rule-validator` | ⏳ |
| 2 | `docs/audits/NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md` | create | low | `rule-validator` | ⏳ |
| 3 | `docs/audits/NUCLEUS_MECHANISM_AUDIT_REPORT-045.md` | create | low | `rule-validator` | ⏳ |
| 4 | `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | create | medium | `rule-validator` | ⏳ |

Notas de riesgo:
- Unidades 1–3 son `low`: crean un archivo nuevo bajo `docs/audits/`, no tocan ningún mecanismo,
  no hay ruta de regresión sobre código ejecutable.
- Unidad 4 es `medium`: consolida y redacta enmiendas a `agents.md`/`rules/`. La enmienda se
  **redacta como texto propuesto dentro del informe**, nunca se aplica al archivo real en este
  sprint (`D1`). El riesgo es de calidad de recomendación, no de rotura.

Todas las unidades usan el template `docs/standards/templates/AUDIT_REPORT_TEMPLATE.md` y siguen la
nomenclatura precedente `PIPELINE_AUDIT_REPORT-042.md` (`<SCOPE>_AUDIT_REPORT-<sprint>.md`).

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | El sprint solo lee el árbol y ejecuta herramientas ya presentes (`make verify`, `scripts/*.py`, `skills/*/scripts/*.py`). No añade código ejecutable ni imports. |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Auditoría del corpus de núcleo (este sprint) | Auditoría de una sola vez — **sin cadencia recurrente** | `human:/agents:pipeline` — Sprint 045, invocación única |

Este plan **no** propone ningún mecanismo recurrente (per-sprint ni per-commit). Si la síntesis
recomienda un chequeo periódico de frescura del ruleset, se registra como **enmienda propuesta**
dentro de `NUCLEUS_AUDIT_SYNTHESIS-045.md` con su clasificación determinista/juicio pendiente para
el sprint de ejecución — no se instala aquí (`token_economy_agent` `pre_approval_audit`, Filter 5).

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 4 | Count of rows in Work table |
| Subagents dispatched | 4 ejecución (uno por unidad, contexto fresco) + 2 gates (`qa_agent`, `tester_agent`) = 6 | `agents.md §6`; gates en Phase 7 |
| Prior session ratio | n/a (sprint nuevo tras el cierre de 044; sin transcript previo del sprint) | `python3 scripts/session_cost.py --from-anchor --json` — sesión actual `ratio: 3.2` a la fecha del plan |

Umbrales soft (5×) / hard (15×) obligan a actualizar esta sección antes de continuar. Los cuatro
informes son de lectura + `grep`/herramienta; el consumo dominante será tool-results de lecturas
parciales (`token_saver`: archivos >200 líneas nunca se vuelcan enteros).

---

## Tests

**Reproduce before repairing.** Este es un sprint de auditoría: el "defecto" que produce es el
conjunto de veredictos `OBSOLETA`/`MEJORAR`, no una rotura de código.

| Check | Fails against the current tree? |
| :--- | :--- |
| `test -f docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | **Yes** — el informe no existe; crearlo es el entregable |
| Cada `RA-NN` de `agents.md` aparece clasificado en `NUCLEUS_RULESET_AUDIT_REPORT-045.md` | **Yes** — no hay informe todavía |
| `make verify` | **No** — verde en `e0189a3`; baseline a proteger, el sprint no debe romperlo |
| `python3 scripts/verify_references.py` | **No** — pasa; el informe lee su salida, no la altera |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `test -f docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md; echo $?` | `0` |
| `test -f docs/audits/NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md; echo $?` | `0` |
| `test -f docs/audits/NUCLEUS_MECHANISM_AUDIT_REPORT-045.md; echo $?` | `0` |
| `test -f docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md; echo $?` | `0` |
| `count=$(grep -oE 'RA-[0-9]{2}' agents.md \| sort -u \| wc -l); rep=$(grep -oE 'RA-[0-9]{2}' docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md \| sort -u \| wc -l); [ "$count" -le "$rep" ]; echo $?` | `0` (todas las enmiendas clasificadas) |
| `grep -cE '^\| *(VIGENTE\|OBSOLETA\|MEJORAR)' docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | `≥ 41` (18 RA + §0–§8 + 11 rules + 12 workflows + mecanismos) |
| `make verify; echo $?` | `0` (ningún mecanismo modificado) |
| `python3 scripts/verify_references.py; echo $?` | `0` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/045-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/045-core-pipeline; echo $?` | `0` (Phase 4.3) |
| `git -C . status --porcelain -- agents.md rules/` | vacío — ninguna enmienda aplicada (`D1`) |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md` | Nuevo. Clasificación `agents.md` §0–§8 + RA-01..RA-18 + 11 `rules/*.md` |
| `docs/audits/NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md` | Nuevo. Clasificación de los 12 `workflows/*.md` |
| `docs/audits/NUCLEUS_MECHANISM_AUDIT_REPORT-045.md` | Nuevo. Cobertura `RA-16`/`RA-11`/`RA-17` + Three-File Standard sobre `scripts/`/`hooks/`/`skills/` |
| `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | Nuevo. Registro rankeado + enmiendas redactadas + sprint de ejecución recomendado. Entregable primario |
| `agents.md`, `rules/*.md` | **Sin cambios.** Las enmiendas se redactan dentro de la síntesis; se aplican en el sprint de ejecución posterior (`D1`, Out of scope) |
| `CHANGELOG.md` `[Unreleased]` | Entrada del Sprint 045 en Phase 8 (Sprint Closeout) |
| `docs/roadmaps/` (Global Roadmap), Walkthroughs, Blueprints, Master Ledger | Actualización de cierre `RA-05` en Phase 8 — la síntesis registra el sprint de ejecución recomendado |

**Measured figures.** Cada número de Context / Verification lleva su comando reproductor.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Aplicar cualquier enmienda (retirar/reescribir reglas, borrar mecanismos) | `D1` — mezcla evidencia y acción en un Gate. Va al **sprint de ejecución** recomendado en `NUCLEUS_AUDIT_SYNTHESIS-045.md` (Sprint 046+), gated por esta síntesis |
| `profiles/` (packs de familia de proyecto) | `RA-15` — nunca en el núcleo público; viven en ruta controlada por el host. No son objeto de esta auditoría |
| Comportamiento del bridge host `.claude/` en runtime | Lo cubre `start_workflow.md bridge_check` cada sesión; no es una norma del corpus |
| Triage fila por fila de `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `D5` — input de planificación de núcleo. La síntesis solo lo cruza para no duplicar hallazgos |
| Auditoría de `docs/` no normativa (guías, ADRs de contenido) más allá de referencias muertas | `rules/documentation_standard.md` `docs-freshness-check` ya la cubre; este sprint audita normas y mecanismos |

---

## Abort criterion

Se detiene y revierte el sprint si, **antes** de cerrar la primera unidad, se observa cualquiera de:

1. `make verify` sale distinto de `0` en `e0189a3` (baseline estructural roto). La auditoría razona
   sobre deriva **semántica** encima de una base estructural verde; auditar sobre una base rota
   produce hallazgos que en realidad son deuda de reconciliación → `/agents:reconcile` primero.
2. El conteo de reglas de `agents.md` no es enumerable de forma determinista
   (`grep -oE '(RA-[0-9]{2}|^## [0-9])' agents.md` devuelve un conjunto incoherente con §0–§8 +
   RA-01..RA-18) — corpus corrupto, es un incidente de integridad, no una auditoría.

Disparador formal: `workflows/remediation_workflow.md`.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | _(pendiente — Human OK en Phase 5)_ |
| **Date** | _(pendiente)_ |
| **Plan commit at approval** | _(pendiente — SHA del commit del plan en `ai-sprint/045`)_ |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*

> **Do not delete the sentence above.** `audit_plan.py` Filter 6 rejects any plan
> that names `/loop` without also naming `loop_guard.py`, and this footer names
> both. Replace `{{…}}` placeholders; leave this pairing intact.
