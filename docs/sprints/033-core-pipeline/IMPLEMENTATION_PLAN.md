# Implementation Plan: Sprint 033 — implementer-role

**Canonical path**: `docs/sprints/033-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/033` · **Base**: `main` at `8b3fb6d` (`v4.15.0`)
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

`F-021-A2` es el único hallazgo de `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`
que sigue abierto tras Sprint 032. Sprint 023 `C5` le dio dueño a `scripts/` y
`hooks/` (`devops_agent`, `F-086-A1`) y **declaró** el vacío: ese dueño es un
rol de entorno `mechanical`/`haiku`, no un implementer. Cada sprint desde
entonces lo ha excluido como «rediseño del mapa de roles».

Medido contra `8b3fb6d` (`v4.15.0`) el 2026-08-25, sesión Cursor
`20260825T173616Z-60236`:

| Claim | Resultado | Reproduce |
| :--- | :--- | :--- |
| Perfiles con `Write`/`Edit` (ítem de lista, no substring) | **8**, ninguno implementer | el bucle de `F-021-A2` (abajo) |
| `devops_agent` tier / model | `mechanical` / `haiku` | `grep -E '^(tier\|model):' agents/devops_agent.md` |
| `principal_agent` tools | `Read, Glob, Grep, TodoWrite` (sin Write) | `grep -m1 '^tools:' agents/principal_agent.md` |
| Core vs auxiliary | 8 core, 5 auxiliary, **13** ficheros | `ls agents/*.md \| wc -l`; `README.md` fila Subagents |
| Hallazgo abierto | checkbox `- [ ]` | `rg -n 'F-021-A2' docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` |

Receta (la forma con frontera de palabra; las otras dos fallan por `TodoWrite`):

```bash
for f in agents/*.md; do
  grep -m1 '^tools:' "$f" | grep -qE '(^|[ ,])(Write|Edit)([ ,]|$)' && basename "$f"
done
```

Devuelve: `agent_orchestrator.md`, `devops_agent.md`, `doc_orchestrator.md`,
`governance_learner.md`, `orchestrator.md`, `rule_validator.md`,
`skill_architect.md`, `topology_mapper.md`.

Hecho cuando 033 cierre: existe un perfil cuya **identidad** es implementar
código, con `Write`/`Edit`, `tier: author`; `scripts/`, `hooks/` y `tests/` se
asignan a ese perfil; `devops_agent` deja de ser el tapón de autoría; el
checkbox de `F-021-A2` está ticked con re-medida, no con el relato del sprint.

---

## Design

**D1 — Un perfil nuevo, auxiliar, no un noveno rol core.**

Nombre: `agents/implementer_agent.md`, frontmatter `name: implementer-agent`.
`tier: author`, `model: sonnet` (alias de familia; Cursor aplica
`config/model_tiers.json` `cursor.author` = `grok-4.5` / `high`).
`tools: Read, Glob, Grep, Write, Edit, Bash`.

Auxiliar: se invoca cuando `task_scope.md` tiene unidades de código o tests.
No entra en el ciclo obligatorio de 8. Rechazado: 9º core (despacho vacío en
sprints de solo docs); rechazado: promover `devops_agent` a `author` (sigue
siendo rol de entorno; `F-021-A2` pide identidad de implementer, no un
upgrade de tier).

**D2 — Transferir la autoría de `scripts/` y `hooks/`; no duplicarla.**

`F-086-A1` permanece cerrado: esos árboles tienen dueño. El dueño pasa de
`devops_agent` a `implementer_agent`. `devops_agent` **pierde** `Write`/`Edit`
y **conserva** `Bash` (venv, export de `.env`, Docker, purge, git de close).
`token_economy_agent` pide cambios a `check_model_tiers.py` /
`detect_new_models.py` / `scan_workflow_determinism.py` **a través de
`implementer_agent`**.

Rechazado: dos dueños `Write` sobre el mismo árbol (el assignment vuelve a
`devops` por hábito). Rechazado: dejar `Write` en devops y añadir implementer
solo para «todo lo demás» — en el núcleo «lo demás» de producto es
`scripts/`/`hooks/`/`tests/`; el hallazgo no se cerraría.

**D3 — Jurisdicción del implementer.**

| Árbol | Dueño |
| :--- | :--- |
| framework-root `scripts/`, `hooks/`, `tests/` | `implementer_agent` |
| `skills/[name]/scripts/` | `skill_architect` (sin cambio) |
| `agents/*.md` | `agent_orchestrator` (sin cambio) |
| docs de sprint / blueprints / ADR | `orchestrator` / `doc_orchestrator` (sin cambio) |
| `docs/active_state.json` topology | `topology_mapper` (sin cambio) |

`tests/` entra aquí porque `tester_agent` es `tier: gate` y no tiene
`Write` (`F-026-A1`: el gate no escribe lo que juzga). El implementer
**escribe** el test; el tester **verifica**.

**D4 — ADR Nygard (trigger §3.1 #2).**

El mapa de roles es un contrato que consumen `pipeline_workflow.md`, el
installer (`agents/*.md` glob) y Cursor `subagent_type`. Un solo trigger
fuera de la clase immediate-harm → Nygard, no MADR.
`docs/decisions/ADR-0009-implementer-role.md`.

**D5 — El recuento de 8 escritores no es el criterio de cierre.**

Tras D2 el recuento sigue en **8** (devops sale, implementer entra). El
cierre es: `implementer-agent.md` está en esa lista **y** su `description`
declara implementación de código. Un test pina ambas cosas con la receta
de frontera de palabra, no con `grep Write`.

---

## Work

Unidad = un commit (`RA-08`) sobre **un** fichero sujeto
(`jurisdictional_lock`). Orden: ADR → perfiles → constitución → pin →
documentos que declaran el cierre.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A0 | `docs/decisions/ADR-0009-implementer-role.md` | create | high | `doc_orchestrator` | ⏳ |
| A1 | `agents/implementer_agent.md` | create | high | `agent_orchestrator` | ⏳ |
| A2 | `agents/devops_agent.md` | modify | high | `agent_orchestrator` | ⏳ |
| A3 | `agents.md` | modify | high | `agent_orchestrator` | ⏳ |
| A4 | `agents/agent_orchestrator.md` | modify | medium | `agent_orchestrator` | ⏳ |
| T1 | `tests/test_implementer_role.py` | create | medium | `implementer_agent` | ⏳ |
| R1 | `README.md` | modify | low | `doc_orchestrator` | ⏳ |
| F1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | medium | `doc_orchestrator` | ⏳ |
| Q1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | ⏳ |

A2: quitar `Write`/`Edit` de `tools:`; reescribir «Why this profile holds
Write» y el párrafo `F-021-A2` como **resuelto en 033**; `write_scope` pasa
a «pide cambios de `scripts/`/`hooks/` a `implementer_agent`».
A3: fila `devops_agent` deja de decir *sole holder*; la nota Core vs
Auxiliary añade `implementer_agent`. **No** se añade una 9ª fila core.
A4: heurística explícita — unidades cuyo sujeto es `scripts/`, `hooks/` o
`tests/` se asignan a `implementer_agent`, no a `devops_agent`.
T1: pin de la receta de `F-021-A2` + existencia del perfil + devops sin
`Write`/`Edit` como ítem. Entra en `pytest tests/` vía `make verify`.
R1: `13` → `14` role-segregated; `5` → `6` auxiliary. `check_readme_counts.py`
lo exige.
F1: ticked **después** de re-medir T1 en verde, no antes.
Cierre Phase 8 (no son filas de Work): `[Unreleased]` en `CHANGELOG.md`.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | El sprint no añade dependencias |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Pin de cierre `F-021-A2` (receta frontera de palabra + perfil implementer) | script (`pytest`) | `Makefile` `verify` → `$(PY) -m pytest tests/` |
| Asignación `scripts/`/`hooks/`/`tests/` → `implementer_agent` | agent judgment (Filter 5: semántica de staffing) | `workflows/pipeline_workflow.md` Phase 4.1; `agents/agent_orchestrator.md` |
| Conteos README ↔ árbol | script | `scripts/check_readme_counts.py` vía `Makefile` `verify` |
| `model:` / `tier:` del perfil nuevo | script | `scripts/check_model_tiers.py` vía `Makefile` `verify` |

No hay mecanismo recurrente nuevo por commit. Phase 5 no se envuelve en
`/loop`. Phases 6-8 solo si un humano arma `loop_guard.py start` antes de
la primera iteración (`rules/loop_governance.md`).

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | 9 | Count of rows in Work tables |
| Subagents dispatched | 0 | Cursor `sequential` |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` |

Soft (5×) / hard (15×) no aplican sin transcript Claude de este tool.

---

## Tests

**Reproduce before repairing.** Un test que pasa contra este HEAD no prueba
el defecto.

| Check | Fails against the current tree? |
| :--- | :--- |
| Existe `agents/implementer_agent.md` con `Write` o `Edit` como ítem de `tools:` | **Yes** — este es el defecto (`ls agents/implementer_agent.md` → no such file) |
| `devops_agent` `tools:` ya no lista `Write`/`Edit` como ítem | **Yes** — hoy los lista (`grep -m1 '^tools:' agents/devops_agent.md`) |
| Receta `F-021-A2` incluye `implementer_agent.md` | **Yes** — el fichero no existe |
| `python3 scripts/check_model_tiers.py; echo $?` | **No** — regresión a proteger (A1 debe declarar `model:` + `tier:`) |
| `python3 scripts/check_readme_counts.py; echo $?` | **No** hoy; **Yes** tras A1 si R1 no aterrizó — R1 y A1 son un par |

---

## Verification

Leer exit codes con `$?` directamente; nunca a través de un pipe.

| Command | Expected |
| :--- | :--- |
| Receta `F-021-A2` (frontera de palabra) | 8 nombres; **incluye** `implementer_agent.md`; **no incluye** `devops_agent.md` |
| `grep -m1 '^tools:' agents/devops_agent.md` | sin `Write` ni `Edit` como ítem; conserva `Bash` |
| `grep -E '^(name\|tier\|model):' agents/implementer_agent.md` | `implementer-agent` / `author` / `sonnet` |
| `python3 -m pytest tests/test_implementer_role.py -q; echo $?` | `0` |
| `python3 scripts/check_model_tiers.py; echo $?` | `0` |
| `python3 scripts/check_readme_counts.py; echo $?` | `0` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/033-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `make verify; echo $?` | `0` |
| `rg -n '^- \[x\] \`F-021-A2\`' docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | un match (cerrado) |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `docs/decisions/ADR-0009-implementer-role.md` | decisión D1–D3 |
| `agents/implementer_agent.md` | perfil nuevo |
| `agents/devops_agent.md` | `Write`/`Edit` fuera; `F-021-A2` resuelto |
| `agents.md` §6 | devops ya no *sole holder*; auxiliary lista `implementer_agent` |
| `agents/agent_orchestrator.md` | heurística de assignment |
| `tests/test_implementer_role.py` | pin |
| `README.md` | 14 agents, 6 auxiliary |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `F-021-A2` ticked |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | 033 en vuelo / entregado |
| `CHANGELOG.md` | `[Unreleased]` en Phase 8 |

**Figuras medidas.** 8 writers, 13 perfiles, `8b3fb6d`, receta de frontera de
palabra — comandos en Context.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Convertir `implementer_agent` en 9º rol core | D1; otro sprint si un ciclo sin código demuestra que el auxilio no se invoca |
| Devolver `Write` a `qa_agent` / `tester_agent` | `F-026-A1` cerrado a propósito: el gate no escribe |
| `cursor.gate.model` distinto de `null` | ADR-0003 |
| Trial de otra familia/modelo author | Sprint 032 acaba de promover `grok-4.5`; no mezclar variables |
| `ruff check .` en `make verify` | 176 errores; migración |
| `graphify update .` | Advisory del `/start` de esta sesión |
| Reescribir sprints 021–032 históricos | son historia; el pin vive en T1 |

---

## Abort criterion

1. El humano rechaza D2 (transferir `Write` fuera de devops) y no elige un
   sustituto que deje a `implementer-agent` en la receta de `F-021-A2` → no
   ejecutar; el hallazgo sigue abierto.
2. Tras A2, `devops_agent` pierde `Bash` o la jurisdicción de venv/`.env`/Docker
   → revertir A2; el rol de entorno no se vacía.
3. T1 usa `grep Write` sin frontera de palabra (vuelve a contar `TodoWrite`)
   → revertir T1; es el defecto que el propio hallazgo documenta.
4. `python3 scripts/check_model_tiers.py` exit `2` por A1 → revertir A1
   (el perfil nuevo debe declarar `model:` + `tier:`).
5. Se añade una 9ª fila a la tabla core de `agents.md` §6 → revertir A3;
   contradice D1.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo |
| **Date** | 2026-08-25 |
| **Plan commit at approval** | `b078360` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop`. Arm `loop_guard.py start` only if wrapping Phases 6-8
(`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).*
