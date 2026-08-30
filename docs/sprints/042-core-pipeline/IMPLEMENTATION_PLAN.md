# Implementation Plan: Sprint 042 — template-gate-parity

**Canonical path**: `docs/sprints/042-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/042` · **Base**: `main` at `e29ac98`
**Status**: `DRAFT` → `APPROVED` → **`EXECUTING`** → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

Este sprint construye el instrumento que el Sprint 041 midió y deliberadamente no
construyó, y corrige una sección de prosa obsoleta que ya indujo a error a esta
misma sesión de planificación.

### 1. La divergencia plantilla↔gate

El Sprint 041 chocó **tres** instancias del mismo defecto mientras ejecutaba sus
propias Fases 1, 4.2 y 4.3: seguir la instrucción de un artefacto versionado
producía un gate bloqueado.

| Artefacto | Gate que falló | Reparado como |
| :--- | :--- | :--- |
| `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | `audit_plan.py` Filtro 6 | `041` U10 |
| `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | `check_forge_ladder.py` | `041` U11 |
| `workflows/pipeline_workflow.md` Fase 4.3 | `check_task_scope.py` | `041` U12 |

El caso `IMPLEMENTATION_PLAN_TEMPLATE.md` es el que fija la severidad: **todo plan
escrito fielmente desde la plantilla oficial era rechazado por el gate obligatorio
de la Fase 1**, y los únicos planes que pasaban eran los que habían descartado el
pie de página de la plantilla. La plantilla enseñaba a fallar.

**Las tres instancias están reparadas; nada impide la cuarta.** Esa es la propuesta:
no más reparaciones, sino el instrumento. Medición del árbol actual, 2026-08-30,
renderizando cada plantilla en un directorio scratch y corriendo su gate consumidor
(reproducible con el bloque de la sección Tests):

| Par medido | Salida | Exit |
| :--- | :--- | :--- |
| `IMPLEMENTATION_PLAN_TEMPLATE.md` → `audit_plan.py` | `[OK] audit_plan` | `0` |
| `AGENT_ASSIGNMENT_TEMPLATE.md` + `SKILL_ASSIGNMENT_TEMPLATE.md` → `check_forge_ladder.py` | `[OK] check_forge_ladder` | `0` |
| `SPRINT_LOG_TEMPLATE.md` → `check_gate_log.py` | `[OK] check_gate_log` | `0` |

Verde hoy porque `041` los reparó hace un commit. Sin instrumento, la próxima
edición de cualquiera de estos ficheros vuelve a quedar sin medir hasta que un
sprint tropiece con ella en su propia Fase 1 — que es exactamente cómo se
descubrieron las tres.

### 2. La prosa obsoleta de `F8` / `F-023-S4`

`docs/roadmaps/core/pipeline/021-030-program-queue.md`, sección *«Carried out of
`023` — routed to a hotfix, scheduled after `026`»*, sigue describiendo `F8` como
*«routed, unowned»*, *«has now survived four sessions»* y **«the highest-severity
open item this program carries»**.

`F8` está **cerrado desde el 2026-08-25** por el hotfix `H-002-secrets`. Re-medido
sobre el árbol actual en esta Fase 1, no leído del registro:

```
python3 -c "import sys; sys.path.insert(0,'hooks'); import on_commit as o; from pathlib import Path;
print(o.is_forbidden_secret_file(Path('.env')),
      o.is_forbidden_secret_file(Path('.env.production')),
      o.is_forbidden_secret_file(Path('.env.example')),
      o.find_hardcoded_secret('API_KEY=sk-a93jf0waldkfj2093ruz', Path('settings.py')))"
# True True False API_KEY
```

`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:685` lo tiene tildado cerrado y
`session_start.py --boot` reporta `0` hallazgos abiertos. La cola de programa es
el único documento que aún lo declara abierto — y es el documento que ordena qué
se trabaja a continuación.

**Coste medido, no hipotético**: esta sesión propuso `F8` como alcance del Sprint
042 leyendo esa sección, y la propuesta sólo cayó al re-medir contra el código.
Cinco sprints de prosa obsoleta en el documento de ordenación consumieron una
ronda completa de planificación.

### Qué es cierto cuando esto termina

`make verify` falla cuando una plantilla versionada no puede pasar el gate que la
consume, y ninguna plantilla nueva puede añadirse sin un par declarado o una
excepción tipada. La cola de programa no declara abierto ningún hallazgo cerrado.

---

## Design

### D1 — Script propio, no un check dentro de `verify_references.py`

`verify_references.py` ya tiene `check_templates_exist` (línea 122), que verifica
**existencia** de plantillas. La tentación es añadir allí el check (g).

**Rechazado.** `verify_references.py` es un analizador estático de corpus: lee
texto y no ejecuta nada. Este instrumento lanza subprocesos y escribe directorios
scratch — otro modo de fallo, otra superficie. La topología existente ya separa un
gate por fichero (`check_task_scope.py`, `check_gate_log.py`, `check_forge_ladder.py`,
`check_readme_counts.py`), y este es un gate más. Se llama
`scripts/check_template_gates.py`.

### D2 — Copia renderizada en scratch, nunca lint en sitio

Impuesto por la medición de `041` al reparar U11: `check_forge_ladder.py` decide
por coincidencia de patrones sobre prosa, de modo que (a) documentar la reparación
*con las palabras de las cadenas ofensoras* la volvió a romper, dos veces, y (b) un
rastro de ejemplo literal es en sí mismo un disparador. Un check que linte la
plantilla en su sitio tropieza con su propio texto explicativo.

El renderizado es **copia verbatim** a un directorio scratch con nombre de sprint
(`999-core-pipeline`, medido funcionando con los cuatro gates), bajo el nombre de
artefacto que el gate espera.

### D3 — Sin sustitución de `{{PLACEHOLDER}}`

Las tres plantillas medidas pasan sus gates **con los `{{…}}` intactos**. Sustituirlos
exigiría inventar contenido de ejemplo, y entonces el check mediría la calidad de la
fixture y no la de la plantilla: una plantilla rota podría pasar porque la sustitución
la arregló. Se copia verbatim. Si algún día un gate exigiera un valor real, eso es una
divergencia legítima que este check debe **reportar**, no ocultar.

### D4 — El caso es un conjunto de ficheros y un comando, no un par 1:1

`check_forge_ladder.py` lee `agent_assignment.md` **y** `skill_assignment.md` del
mismo directorio; un mapeo plantilla→gate 1:1 no puede expresarlo. La unidad
declarada en `config/template_gates.json` es un **caso**: un mapa de
`plantilla → nombre de artefacto` más un comando de gate.

### D5 — El comando sale de un fichero de datos: restricciones explícitas

Ejecutar comandos declarados en JSON es ejecución desde datos. Restricciones
codificadas en el script, no confiadas al autor del config:

| Restricción | Razón |
| :--- | :--- |
| Sin shell (`shell=False`, lista de argumentos) | Ninguna interpolación de shell |
| `argv[0]` debe ser `python3` | El conjunto de gates es Python; nada más se ejecuta |
| La ruta del script debe existir y resolverse **dentro** del repositorio | Un config no alcanza binarios del sistema |
| Único token expandible: `{sprint_dir}` | Sin plantillado general |

### D6 — Completitud: una plantilla sin par es un fallo, no un silencio

Es la forma de `RA-16` aplicada a plantillas. Toda entrada de
`docs/standards/templates/` debe aparecer en el mapa de renderizado de algún caso
**o** en `exceptions` con una razón tipada. Añadir una plantilla nueva sin decidir
qué gate la consume falla el build. Sin esto, el instrumento cubre cuatro ficheros
para siempre y la próxima divergencia nace fuera de su alcance.

Razones tipadas previstas: `no-automated-gate` (`CHANGELOG_TEMPLATE.md`,
`HOTFIX_TEMPLATE.md`, `BLUEPRINT_TEMPLATE.md`, `WALKTHROUGH_TEMPLATE.md`,
`ADR_TEMPLATE.md`, `AUDIT_REPORT_TEMPLATE.md`, `GUIDE_TEMPLATE.md`,
`README_TEMPLATE.md`, `SYSTEM_OVERVIEW_TEMPLATE.md`, `IDENTITY_TEMPLATE.json`),
`phase-mismatch` (ver D7).

### D7 — `check_role_artifact.py` no se empareja con `SPRINT_LOG_TEMPLATE.md`

Medido: `check_role_artifact.py --role "QA Agent"` sale `2` contra la plantilla
(*«missing: 'QA' row»*). **No es una divergencia**: `SPRINT_LOG_TEMPLATE.md` se
instancia en Fase 3 y las filas de veredicto las escriben los gates en Fase 7. Una
plantilla sólo debe pasar el gate que la consume **en la fase en que se autora**.
Se registra como excepción `phase-mismatch` con esta razón, no se «repara»
añadiendo filas de veredicto falsas a la plantilla — eso enseñaría a fabricar
veredictos.

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) touching **one physical
file** as its structural subject (`agents.md §2 jurisdictional_lock`).

The Work column `Assignee (proposed)` is a staffing proposal from Phase 1. Phase
4.1 (`agent_orchestrator`) is the authority that records the assignee; it may
overwrite this proposal. A Work row is not closed until `agent_assignment.md`
records it. Do not rename columns on existing `task_scope.md` files to match
this heading.

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | ⏳ |
| U2 | `config/template_gates.json` | create | low | `implementer_agent` | ⏳ |
| U3 | `scripts/check_template_gates.py` | create | medium | `implementer_agent` | ⏳ |
| U4 | `Makefile` | modify | medium | `implementer_agent` | ⏳ |
| U5 | `tests/test_check_template_gates.py` | create | medium | `implementer_agent` | ⏳ |
| U6 | `README.md` | modify | low | `doc_orchestrator` | ⏳ |
| U7 | `docs/decisions/ADR-0012-template-gate-parity.md` | create | low | `doc_orchestrator` | ⏳ |

**Done-criterion por unidad**

| # | Done-criterion |
| :--- | :--- |
| U1 | La sección *«Carried out of `023`»* declara `F8` cerrado por `H-002-secrets` el 2026-08-25, con el comando de re-medición. **`RA-14`**: antes de cerrar la unidad, `grep -rn "F-023-S4\|F8" docs/ rules/ workflows/ agents.md` y corregir toda otra prosa que lo declare abierto **fuera de** `docs/sprints/*` y `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`, que son historia y no se reescriben |
| U2 | Declara los 3 casos medidos y una `exceptions` que cubre las 10 plantillas restantes más el `phase-mismatch` de D7. `python3 -c "import json;json.load(open('config/template_gates.json'))"` sale `0` |
| U3 | Módulo con docstring que declara `invoked_by: Makefile#verify`. Renderiza en scratch, ejecuta cada caso, imprime una línea por caso, sale `2` si cualquier gate no sale `0` **o** si falla la completitud de D6. Ninguna función supera 50 líneas ni 3 niveles de indentación (`agents.md §1`) |
| U4 | Línea `cd $(AGENTS_DIR) && python3 scripts/check_template_gates.py` dentro del target `verify`, situada junto a los demás gates de sprint. `make verify` sale `0` |
| U5 | Cubre: los 3 casos verdes; una plantilla divergente sintética rechazada con exit `2`; una plantilla no declarada rechazada por D6; las 4 restricciones de D5 |
| U6 | Los contadores `scripts/*.py` y `config/*.json` del bloque `COUNTED` reflejan los dos ficheros nuevos. `python3 scripts/check_readme_counts.py` sale `0` |
| U7 | `ADR-0012` registra D1, D2, D3 y D7 con la alternativa rechazada de cada uno, desde `docs/standards/templates/ADR_TEMPLATE.md` |

---

## Dependencies

`rules/code_craft.md §7` — every dependency is permanent code you do not control.
Before adding one, check the standard library, then what is already present. The
commit that adds it must also carry `Dependency: <name> — <reason>`.

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | `subprocess`, `shutil`, `tempfile`, `json` y `pathlib` cubren el instrumento entero |

---

## Mechanisms

Every recurring mechanism this plan proposes (per-sprint or per-commit cadence),
classified before the Approval Gate — `token_economy_agent` `pre_approval_audit`,
Filter 5. A recurring mechanism delegated to agent judgment when a deterministic
alternative exists is rejected, and the alternative must be **named**.

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Paridad plantilla↔gate en cada `make verify` | **script** (`scripts/check_template_gates.py`) | `Makefile#verify`, invocado a su vez por `.github/workflows/ci.yml` |
| Completitud del emparejamiento (D6) | **script** — misma invocación, no un paso aparte | `Makefile#verify` |

Coste por ejecución: 3 subprocesos de gate sobre un directorio temporal, sin red y
sin LLM. Ningún juicio de agente sustituible por script queda delegado a un agente.

`RA-16 INVOCATION_COVERAGE`: no workflow, script, executable skill, hook or gate
merges without a declared, verifiable invoker, or a typed exception in
`config/invocation_exceptions.json` stating why it has none.

---

## Cost

**Required from Sprint 030 onward** (`rules/token_economy.md` §3). Not retroactive
to plans sealed before 030. Enforced by
`skills/token-saver-auditor/scripts/audit_plan.py` (exit `2` if absent).

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 7 | Count of rows in Work tables |
| Subagents dispatched | 2 previstos — `qa_agent` y `tester_agent` en Fase 7, contexto fresco | `pipeline_workflow.md` Fase 7 nota: *«Fresh-context gate execution is required under both tools»*. Fases 1–6 se ejecutan en la sesión principal; **se confirma en la Fase 5** |
| Prior session ratio | `4.1` (esta sesión, 52 mensajes, primer turno `21 682` → pico `88 283`) | `python3 scripts/session_cost.py --from-anchor --json` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues — they are not observational-only once a measurable Claude
transcript exists for this tool.

`4.1` está bajo el umbral blando de `5×`. Si la Fase 6 lo cruza, esta sección se
actualiza antes de continuar.

---

## Tests

**Reproduce before repairing.** A test that passes against the current tree proves
nothing about a defect claimed to exist in it.

| Check | Fails against the current tree? |
| :--- | :--- | 
| Los 3 casos declarados pasan sus gates hoy | **No** — es la regresión a proteger; `041` los reparó y nada guarda la reparación |
| El checker rechaza (exit `2`) una copia divergente sintética de `IMPLEMENTATION_PLAN_TEMPLATE.md` cuyo pie nombra `/loop` sin `loop_guard.py` — el defecto exacto de `041` U10 | **Sí** — sin `U3` no existe nada que lo detecte |
| El checker rechaza una plantilla presente en `docs/standards/templates/` sin caso ni excepción (D6) | **Sí** — hoy una plantilla nueva nace sin gate en silencio |
| El checker rechaza un comando de caso cuyo `argv[0]` no es `python3` o cuya ruta escapa del repositorio (D5) | **Sí** — hoy no hay tal restricción porque no hay tal fichero |
| `021-030-program-queue.md` no declara `F8` abierto | **Sí** — `grep -n "highest-severity open item" docs/roadmaps/core/pipeline/021-030-program-queue.md` devuelve la línea hoy |

Trampa registrada para U5, heredada de `041` U11: las fixtures divergentes se
escriben en `tmp_path`, **nunca** editando la plantilla real, y el texto de la
fixture no se copia a la prosa de ningún documento versionado — es la forma en que
`check_forge_ladder.py` se rompió dos veces durante su propia reparación.

---

## Verification

The exact commands, and what each must return. Read exit codes with `$?` directly;
**never through a pipe**, which reports the exit code of the last command in it.

| Command | Expected |
| :--- | :--- |
| `python3 scripts/check_template_gates.py; echo $?` | `0`, una línea `[OK]` por caso |
| `./venv_skillopt/bin/python -m pytest tests/test_check_template_gates.py -q; echo $?` | `0` |
| `./venv_skillopt/bin/python -m pytest tests/ -q; echo $?` | `0`, ≥ 647 tests (línea base de `041`), cero fallos |
| `make verify; echo $?` | `0`, 16 checks verdes (15 en `041` + este) |
| `python3 scripts/verify_references.py; echo $?` | `0` — `RA-16` check (d) resuelve el invocador de `check_template_gates.py` |
| `python3 scripts/check_readme_counts.py; echo $?` | `0` |
| `ruff check scripts/check_template_gates.py tests/test_check_template_gates.py; echo $?` | `0` — ficheros nuevos, sin deuda heredada |
| `grep -c "highest-severity open item" docs/roadmaps/core/pipeline/021-030-program-queue.md` | `0` |

---

## Documentary impact (T5)

**Applies from Sprint 029 onward** (`rules/documentation_standard.md` §6). Not
retroactive to plans already sealed.

| Artefacto | Qué cambia |
| :--- | :--- |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | `F8` pasa de «abierto, sin dueño» a cerrado por `H-002-secrets`; la sección «Candidate for the next program» se marca como ejecutada por este sprint |
| `README.md` | Contadores `scripts/*.py` y `config/*.json` +1 cada uno |
| `docs/decisions/ADR-0012-template-gate-parity.md` | Nuevo — D1/D2/D3/D7 con sus alternativas rechazadas |
| `CHANGELOG.md` `[Unreleased]` | Entrada del sprint en Fase 8 (`RA-05`) |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Regenerado por `scripts/map_workflows.py` si `make verify --check` lo exige; **nunca editado a mano** |

**Measured figures.** Every number in Context / Design / Verification carries
the command that reproduces it. A figure without its command is memory, not
evidence (`021-030-program-queue.md` J6 / T5).

---

## Out of scope

Named exclusions with their destination. A finding with no destination is a finding
that dies in this document.

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `check_task_scope.py` tiene gate pero **no existe** `TASK_SCOPE_TEMPLATE.md` — la divergencia inversa, que `041` U12 reparó en la prosa de `pipeline_workflow.md` | Este instrumento renderiza plantillas; no puede renderizar una que no existe. Destino: sección «Candidate for the next program» de `021-030-program-queue.md`, como propuesta de crear la plantilla |
| Emparejar prosa de workflow con su gate (el caso `pipeline_workflow.md` Fase 4.3) | Un workflow no es una plantilla renderizable: no produce un artefacto que un gate consuma. Destino: misma sección de la cola |
| Las 193 incidencias `ruff` repo-wide sobre 66 ficheros | `041` Fase 7 las registró como `RECORD testifying`; este sprint sólo exige `ruff` limpio en los **dos ficheros nuevos**. Destino: la cola de programa |
| Añadir filas de veredicto de ejemplo a `SPRINT_LOG_TEMPLATE.md` para satisfacer `check_role_artifact.py` | D7: enseñaría a fabricar veredictos. Destino: excepción `phase-mismatch` en `config/template_gates.json` |

---

## Abort criterion

The observation that stops this sprint and reverts it, decided **before** execution
starts. Written in advance so it is not renegotiated once the work is sunk cost.

**Se aborta y se revierte si `scripts/check_template_gates.py` necesita lógica que
sepa qué gate está ejecutando** — es decir, cualquier rama de código condicionada al
nombre de un gate o de una plantilla, más allá de la sustitución del único token
`{sprint_dir}` (D5). Observable: `grep -c "audit_plan\|forge_ladder\|gate_log" scripts/check_template_gates.py`
debe ser `0`; esos nombres viven en `config/template_gates.json`, no en el script.

Un checker que conoce a sus gates es una segunda copia de los gates, y la segunda
copia diverge — que es el defecto que este sprint existe para cerrar, reintroducido
un nivel más arriba.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal |
| **Date** | 2026-08-31 |
| **Plan commit at approval** | `adc4162` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
