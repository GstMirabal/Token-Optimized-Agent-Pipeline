# Implementation Plan: Sprint 057 — s0-lane-and-defect-block

**Canonical path**: `docs/sprints/057-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/057` · **Base**: `main` at `5851b18` (`v4.39.1`)
**Status**: `DRAFT`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English. Host identifiers are genericized (`RA-15`): the
> reporting host is "host H1".
>
> Fuente: el borrador sin trackear `docs/plans/057-upstream-intake-and-backlog-DRAFT.md`
> (debate 2026-10-22/24, triage de 43 ítems del host H1, orden 057-060 confirmado por el
> humano). Este plan extrae de él el alcance de 057; los bloques de 058-060 quedan en
> `Out of scope` con destino. El borrador se borra en Phase 5, cuando este plan queda
> aprobado y commiteado.

---

## Context

Sprint 057 abre el programa 057-060 decidido en la sesión 2026-10-22/24. Tres fuentes:

1. Informe upstream del host H1 (pin `v4.38.0`, 43 ítems): veredictos confirmados por el
   humano el 2026-10-22 (tabla del borrador, sección "Veredictos del informe del host H1").
2. Hallazgos enrutados desde Sprint 056: `KI-056-2`..`KI-056-8`
   (`docs/roadmaps/core/pipeline/021-030-program-queue.md:380-387`).
3. Dirección humana 2026-10-23: escala de severidad S0–S3 y criterios de prompting
   Opus 5.5, escritos al principio para aplicarlos a todo texto nuevo de 057-059.

Qué es verdad al terminar:

| Resultado | Medida |
| :--- | :--- |
| Carril S0 medido | `SANDBOX_DB_MEASUREMENT.md` registra, en sesiones headless `claude -p` con el template, si el sandbox permite TCP a `localhost`, leer `./.env.agent` y escribir `.git/worktrees/` |
| Tests con BD sin secretos reales | Si la medición lo permite: `.env.agent` legible desde el sandbox, con `denyWrite` en el template, comprobado contra `.env` por el hook `SessionStart` (higiene, D2), y sondeo de BD antes de ejecutar |
| Hotfix publicable sin declarar un gate "no aplicable" | `session_state.py require-released --hotfix H-NNN` sale `0` sobre una punta de hotfix registrada (hoy `H-004`, `H-007`, `H-008` se publicaron declarando Phase 0 no aplicable: `git log --oneline -3 5851b18`) |
| Defectos del bloque 1 corregidos | Cada fila `fix(` lleva su test pareado, que falla en `5851b18` y pasa en la punta |
| Escala S0–S3 vigente | Definición única en `rules/qa_and_testing.md §4`; columna `Severity` en `SPRINT_LOG_TEMPLATE.md`; `check_gate_log.py` cuenta `escape` |

Confirmado en código en `5851b18` (no heredado del borrador, que medía `v4.39.0`):

| Ítem | Evidencia en la base |
| :--- | :--- |
| Hotfix sin ruta | `workflows/deployment_workflow.md:15`: `require-released` sale `2` cuando la punta no es `last_close_commit` |
| B-9 / E | `scripts/session_state.py:193-218` `suspend()` escribe `SUSPENDED` sin mirar `current_sprint.status`; `scripts/session_end_hook.py` no lee stdin. El boot de esta sesión dijo "Resuming a suspended sprint" sobre el 056 sellado |
| C-3 / D-6 | `scripts/py_compile_tree.py:41` `py_compile.compile(str(path), doraise=True)` sin `cfile` |
| A-4 / B-1 | Dos gramáticas `Repro:`: `hooks/on_commit.py:776,780` y `scripts/check_fix_reproduces.py:50` |
| B-2 / B-6 | `hooks/on_commit.py:764` `TEST_PATH` no casa `src/a.spec.ts` ni `app/tests.py` (comando en Tests) |
| B-3 | `scripts/check_task_scope.py:109` parte `` `a\|b` `` en dos celdas (comando en Tests) |
| `KI-056-2` | `scripts/check_fix_reproduces.py:49` lista `.json` en `NON_SOURCE_SUFFIXES` |
| Remediación | `workflows/remediation_workflow.md:18` lee `memory/telemetry/raw_errors.json`, inexistente; `:20` pide `BLOCKED` sin instrumento |
| QA-H007-9 | `skills/mcp-registry/registry.json:3,17` prescribe `pnpm dlx` sin versión |
| R6-1 | `tests/test_mcp_template.py:20` "while its dependencies are not" |
| R6-2 | `memory_index.json:169` usa "fail-closed" en sentido de cobertura (`agents.md §1 fail_closed_claims`) |

---

## Design

### D1 — Orden: medir antes de cambiar el sandbox

El carril S0 empieza con una unidad de medición (W01) y ninguna unidad del carril
(W02-W06) se ejecuta antes de que W01 registre su resultado. Motivo: Sprint 055/056
demostró que las afirmaciones sobre el sandbox sin medición fueron falsas cuatro veces
(`RA-19`). Método: el de `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md:19`
(headless `claude -p --allowedTools Bash --output-format stream-json`, un caso por llamada
Bash, desde un fixture con el template), presupuesto ≤ 6 llamadas `claude -p`.

| Caso | Pregunta |
| :--- | :--- |
| M1 | ¿Un `python3 -c socket.create_connection(("127.0.0.1", <port>))` contra un listener local conecta desde el sandbox? |
| M2 | Con `./.env.agent` en `allowRead`, ¿el sandbox lo lee mientras `./.env` sigue denegado? |
| M3 | ¿El sandbox permite `git worktree add` (escritura en `.git/worktrees/`)? (B-5) |

Rechazado (debate 2026-10-23): ejecutar la suite fuera del sandbox con `.env` (S0: los
tests son código escribible por el agente); herramienta MCP que ejecute
`docker compose up` (el compose file es escribible y correría fuera del sandbox). Evidencia
de que la presión existe: el host H1 ejecutó 5 veces `source .env` + pytest fuera del
sandbox con aprobación humana (borrador, "Medición de prompts").

### D2 — `.env.agent`

Fichero de credenciales de test desechables. Template: `allowRead` y `denyWrite` de
`./.env.agent` (el agente lo lee, no lo escribe: un humano lo crea). Validador
`scripts/env_agent_check.py`: comprueba que ningún valor de `.env.agent` aparece en
`.env` e imprime solo nombres de variable, nunca valores (`RA-09`). Lo invoca el hook
`SessionStart`, nunca el agente: el template deniega `Read(./.env)` al agente, lo que
reduce exposición y no es una frontera (`RA-19`). El hook es la entrada `E1` de
`docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md:48`: en modo host `hooks/` y
`scripts/` de `./.agents` miden `denied (rule)`, pero los imports de la raíz vía
`sys.path` miden escribibles (`F-055-N1`, abierto). Por eso W03 y W05 citan `E1` y
`F-055-N1` y no llaman "seguro" ni "validado por un proceso no-agente" al validador: es
una comprobación de higiene contra el error humano de copiar un secreto real en
`.env.agent`, no un control contra un agente hostil. En el nucleus no hay `.env` y el
script sale `0` con aviso. Ningún texto de W02-W06, de `SANDBOX_DB_MEASUREMENT.md` ni del
CHANGELOG dice que el agente "no puede" leer `.env` (rule audit 4.3, S2).

El test de W02 (`tests/test_template_sandbox.py`) nombra las claves exactas que comprueba
(`sandbox.filesystem.allowRead`, `denyRead`, `denyWrite`) y no afirma cobertura sobre el
resto del objeto (`agents.md §1 fail_closed_claims`).

### D3 — Sondeo de BD

`scripts/db_probe.py` lee host y puerto de `DATABASE_URL` en `.env.agent` y abre un TCP
con timeout de 2 s. Sale `0` si conecta; sale `2` con un único mensaje agrupado para el
humano ("levanta la BD: `docker compose up -d <servicio>`") si no. No ejecuta nada.
Recomendación documentada al host: `restart: unless-stopped`.

### D4 — Ruta de hotfix en deployment

`require-released --hotfix H-NNN` acepta una punta que no es `last_close_commit` cuando se
cumplen las cuatro condiciones: existe `docs/hotfixes/H-NNN-*.md`; la rama actual es
`hotfix/H-NNN` o la punta es el squash de esa rama en `main`; `last_close_commit` es
ancestro de la punta; `status` no es `SUSPENDED`. Cualquier otra combinación sale `2`
como hoy. Alternativa rechazada: declarar Phase 0 no aplicable en el registro del hotfix
(práctica actual): un gate que se declara inaplicable a mano no es un gate.

### D5 — Una sola gramática `Repro:`

Nuevo módulo `scripts/_repro_grammar.py` con el regex y el parser. `hooks/on_commit.py`
ya importa desde `scripts/` (`hooks/on_commit.py:31-32`), así que los dos consumidores lo
importan y ninguno conserva su regex. Gramática: la de `on_commit.py:776,780` (estricta);
`check_fix_reproduces.py` deja de aceptar formas que el hook rechaza.

### D6 — Escala de severidad S0–S3

La tabla y las cinco reglas de convergencia del borrador ("Escala de severidad de
errores") pasan sin cambios a `rules/qa_and_testing.md §4`, junto a `RA-17`: severidad es
un eje ortogonal al veredicto. Instrumentos: columna `Severity` y marca `escape` en
`SPRINT_LOG_TEMPLATE.md`; regla 3 (segunda aparición de una familia → check determinista)
en `workflows/remediation_workflow.md`; `check_gate_log.py` cuenta las filas `escape` por
sprint y las imprime (advisory, exit `0`).

### D7 — Criterios de prompting Opus 5.5

Guía `docs/guides/PROMPT_CRITERIA_GUIDE.md`, escrita en la primera ola, a partir de la guía
de prompting vigente de Opus 5.5 cargada con la skill `claude-api`. Lista de comprobación
aplicable línea a línea: énfasis que sobreactiva (mayúsculas, "MUST" repetido), narrativa
histórica en texto siempre cargado, instrucción redundante con el comportamiento por
defecto, contradicción entre documentos. Se aplica a todo texto nuevo de 057; la auditoría
del corpus existente es Sprint 060. Rechazado: un `rules/*.md` nuevo, porque exigiría fila
en `agents.md §0` y `config/rule_triggers.json` antes de saber si el formato sirve.

### D8 — Ítems reproduce-first

B-4, B-5, B-7, C-1, C-2, C-5 y C-9 son `plausible` en el borrador. B-2 también:
`rules/code_craft.md:80` ya define `Repro: manual` como alternativa, así que W16 reproduce
primero que el hook exige un test staged con `Repro: manual` antes de cambiarlo. Su unidad empieza
ejecutando la reproducción contra `5851b18`. Si no reproduce, la unidad se cierra sin
commit de código con una fila `RECORD` en `SPRINT_LOG.md` que nombra el comando y su
salida, y el veredicto se comunica al host H1. Si reproduce, se corrige con test pareado.

W25 tiene dos ramas. Si C-9 se resuelve borrando prescripciones, cada fichero de
`workflows/`, `rules/` o `agents.md` que se edite es un sujeto estructural distinto: la
sesión para, añade una fila por fichero a este plan y a `task_scope.md`, y solo entonces
edita (`agents.md §2 jurisdictional_lock`).

---

## Work

Leyenda de riesgo: `high` toca un gate o el template del sandbox. Las unidades `fix(`
nombran su test pareado en la misma fila (`rules/code_craft.md §6`).

### Ola A — criterios y escala (primero: se aplican a todo texto posterior)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| W00 | `docs/guides/PROMPT_CRITERIA_GUIDE.md` | create — lista de comprobación de D7 | low | `doc_orchestrator` | ⏳ |
| W07 | `rules/qa_and_testing.md` | modify — §4 añade la escala S0–S3 y las 5 reglas de convergencia (D6) | medium | `rule_validator` | ⏳ |
| W08 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify — columna `Severity` y marca `escape` en la tabla de rondas de gate | low | `doc_orchestrator` | ⏳ |
| W09 | `scripts/check_gate_log.py` | modify — cuenta filas `escape` y las imprime, exit `0`; test `tests/test_check_gate_log.py` | low | `implementer_agent` | ⏳ |

### Ola B — carril S0 (W01 bloquea W02-W06)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| W01 | `docs/sprints/057-core-pipeline/SANDBOX_DB_MEASUREMENT.md` | create — casos M1-M3 de D1, ≤ 6 llamadas `claude -p`, salida literal por caso; `devops_agent` ejecuta las sesiones y `doc_orchestrator` escribe el fichero (`agent_assignment.md`: `devops_agent` no tiene Write) | high | `doc_orchestrator` | ⏳ |
| W02 | `claude/settings.hooks.json` | modify — `allowRead` y `denyWrite` de `./.env.agent`; test `tests/test_template_sandbox.py` | high | `implementer_agent` | ⏳ |
| W03 | `scripts/env_agent_check.py` | create — validador de D2; test `tests/test_env_agent_check.py` | high | `implementer_agent` | ⏳ |
| W04 | `scripts/db_probe.py` | create — sondeo de D3; test `tests/test_db_probe.py` | medium | `implementer_agent` | ⏳ |
| W05 | `rules/project_topology.md` | modify — sección de BD: `.env.agent`, sondeo, `restart: unless-stopped`, invocadores de W03/W04 | medium | `rule_validator` | ⏳ |
| W06 | `agents.md` | modify — `RA-09`: una frase que nombra `.env.agent` como única excepción de lectura y remite a `rules/project_topology.md` | high | `rule_validator` | ⏳ |

### Ola C — defectos del bloque 1

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| W10 | `scripts/session_state.py` | fix — `require-released --hotfix H-NNN` (D4); test `tests/test_session_state.py` | high | `implementer_agent` | ⏳ |
| W11 | `workflows/deployment_workflow.md` | modify — Phase 0 nombra la ruta `--hotfix`; C-5: el cuerpo del squash se fija con `gh pr merge --squash --body-file`, no con la configuración del repo | high | `doc_orchestrator` | ⏳ |
| W12 | `scripts/session_state.py` | fix — B-9: `suspend()` sale `0` sin escribir cuando `current_sprint.status` está sellado; test `tests/test_session_state.py` | high | `implementer_agent` | ⏳ |
| W13 | `scripts/session_end_hook.py` | fix — E: lee `session_id` de stdin y no suspende si no coincide con el del anchor; test `tests/test_session_end_hook.py` | medium | `implementer_agent` | ⏳ |
| W14 | `scripts/py_compile_tree.py` | fix — C-3: `cfile` en un `tempfile.TemporaryDirectory()`; test `tests/test_verify_py_compile.py` | medium | `implementer_agent` | ⏳ |
| W15 | `scripts/_repro_grammar.py` | create — gramática única de D5; test `tests/test_repro_grammar.py` | medium | `implementer_agent` | ⏳ |
| W16 | `hooks/on_commit.py` | fix — A-4: importa `_repro_grammar`; B-2 (reproduce-first, D8): `Repro: manual` pasa sin test staged; B-6: `TEST_PATH` casa `*.spec.*` y `tests.py`; test `tests/test_on_commit.py` | high | `implementer_agent` | ⏳ |
| W17 | `scripts/check_fix_reproduces.py` | fix — A-4: importa `_repro_grammar`; `KI-056-2`: quita `.json` de `NON_SOURCE_SUFFIXES`; test `tests/test_check_fix_reproduces.py` | medium | `implementer_agent` | ⏳ |
| W18 | `scripts/check_fix_reproduces.py` | reproduce-first (D8) — B-4: distinguir fallo de test de error de setup; B-5: ruta sin `git worktree` si M3 lo deniega; test `tests/test_check_fix_reproduces.py` | medium | `implementer_agent` | ⏳ |
| W19 | `scripts/check_task_scope.py` | fix — B-3: separador de celdas que respeta `\|` escapado; test `tests/test_check_task_scope.py` | low | `implementer_agent` | ⏳ |
| W20 | `scripts/model_ledger.py` | fix — B-8: ruta del ledger desde la raíz del host, no `agents_root()`; test `tests/test_model_ledger.py` | medium | `implementer_agent` | ⏳ |
| W21 | `scripts/detect_drift.py` | reproduce-first (D8) — C-1: commit rutinario de cierre que toca un fichero fuera de anchor + CHANGELOG; test `tests/test_detect_drift.py` | medium | `implementer_agent` | ⏳ |
| W22 | `workflows/reconciliation_workflow.md` | reproduce-first (D8) — C-2: Phase 4 escribe bajo `docs/roadmaps/` en modo host | low | `doc_orchestrator` | ⏳ |
| W23 | `scripts/session_start.py` | fix — C-4 / `KI-056-4`: un predicado de obsolescencia del bridge, y `PermissionError` de `_refresh_bridge_lock` capturado y reportado; test `tests/test_session_start.py` | medium | `implementer_agent` | ⏳ |
| W24 | `scripts/check_role_artifact.py` | reproduce-first (D8) — B-7: fila `Tester` exigida a `tester-agent`; test `tests/test_check_role_artifact.py` | medium | `implementer_agent` | ⏳ |
| W25 | `scripts/session_state.py` | reproduce-first (D8) — C-9: si un script lee `last_release`, `system_state` o `certification`, `release` los escribe; si ninguno, W25 borra cada prescripción de esos campos (grep en `workflows/ rules/ agents.md`) | low | `implementer_agent` | ⏳ |
| W26 | `scripts/extract_plan.py` | create — C-8: copia el plan de Phase 1 a la ruta canónica y sale `2` si ya existe distinto; test `tests/test_extract_plan.py`; invocador `pipeline_workflow.md` Phase 3 | medium | `implementer_agent` | ⏳ |
| W27 | `workflows/pipeline_workflow.md` | modify — Phase 3 invoca `scripts/extract_plan.py` (`RA-16`) | low | `doc_orchestrator` | ⏳ |
| W28 | `scripts/session_state.py` | modify — subcomando `block --reason` que escribe `current_sprint.status: BLOCKED`; test `tests/test_session_state.py` | medium | `implementer_agent` | ⏳ |
| W29 | `workflows/remediation_workflow.md` | modify — Phase 2 lee `SPRINT_LOG.md` y `git stash list` en vez de `raw_errors.json`; Phase 3 invoca `session_state.py block`; regla 3 de D6 | medium | `doc_orchestrator` | ⏳ |
| W30 | `scripts/merge_json.py` | fix — `KI-056-3` + residuo `H-007`: poda claves de mapa retiradas (`git-sync-agent` en `.mcp.json`) y denies por subárbol retirados; hooks duplicados por la fusión aditiva se deduplican; test `tests/test_merge_json.py` | high | `implementer_agent` | ⏳ |
| W31 | `scripts/check_changelog_tags.py` | create — `KI-056-8`: cada tag `vX.Y.Z` tiene `## [X.Y.Z]` y las versiones descienden, exit `2` si no; test `tests/test_check_changelog_tags.py` | medium | `implementer_agent` | ⏳ |
| W32 | `Makefile` | modify — `verify` ejecuta `scripts/check_changelog_tags.py` (`RA-16`) | low | `implementer_agent` | ⏳ |

### Ola D — residuos S3 y documentación

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| W33 | `skills/mcp-registry/registry.json` | modify — QA-H007-9: `_comment` y `example-local-mcp` exigen versión fijada (`pnpm dlx <pkg>@<x.y.z>`) | low | `skill_architect` | ⏳ |
| W34 | `tests/test_mcp_template.py` | modify — R6-1: docstring "not all pinned" | low | `implementer_agent` | ⏳ |
| W35 | `memory_index.json` | modify — R6-2: línea 169 sin sentido de cobertura para "fail-closed" | low | `governance_learner` | ⏳ |
| W36 | `scripts/install.py` | modify — `KI-056-5`: el mensaje `B5` sugiere `install.py`, no `install.sh` | low | `implementer_agent` | ⏳ |
| W37 | `skills/env-shielding-auditor/README.md` | modify — `KI-056-7`: badge "Built With: Python" | low | `skill_architect` | ⏳ |

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | W03, W04, W15, W26 y W31 usan solo stdlib (`socket`, `re`, `pathlib`, `subprocess`) |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Comprobación de higiene `.env.agent` contra `.env` (no es un control de seguridad, D2) | script `scripts/env_agent_check.py` | hook `SessionStart` (`claude/settings.hooks.json`; entrada `E1` de la enumeración 056) |
| Sondeo de BD antes de tests con BD | script `scripts/db_probe.py` | `rules/project_topology.md` sección de BD; `tester_agent` antes de pytest |
| Ruta de hotfix en Phase 0 | script `session_state.py require-released --hotfix` | `workflows/deployment_workflow.md` Phase 0 |
| No suspender un sprint sellado | script `session_state.py suspend` | hook `SessionEnd` (`scripts/session_end_hook.py`) |
| Contador de `escape` | script `scripts/check_gate_log.py` | `close_workflow.md` (invocador existente de `check_gate_log.py`) |
| Extracción del plan | script `scripts/extract_plan.py` | `workflows/pipeline_workflow.md` Phase 3 |
| Estado `BLOCKED` | script `session_state.py block` | `workflows/remediation_workflow.md` Phase 3 |
| Tags frente a CHANGELOG | script `scripts/check_changelog_tags.py` | `Makefile` `verify` |
| Clasificación de severidad por hallazgo | agent (juicio del gate; no hay alternativa determinista para clasificar un hallazgo) | `qa_agent` / `tester_agent` en Phase 7 |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 38 | Count of rows in Work tables (W00-W37) |
| Subagents dispatched | ≤ 44 (38 unidades + 2 gates × ≤ 3 rondas) | estimación de Phase 1 |
| Prior session ratio | 16.8× (sesión 2026-10-22/24, superó el hard bound de 15×; por eso esta sesión arrancó limpia) · esta sesión 1.8× al redactar | `python3 scripts/session_cost.py --from-anchor --json` |

38 unidades no caben en una sesión dentro del soft bound de 5×. Corte previsto por olas:
una sesión por ola, `session_state.py suspend` entre olas (`rules/token_economy.md §3.1`).

---

## Tests

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| B-6: `TEST_PATH` no casa `src/a.spec.ts` ni `app/tests.py` (`python3 -c` con el regex de `hooks/on_commit.py:764`, sale `0` si ninguno casa) | **Yes** — this is the defect | exit `0` en `5851b18` (ninguno casa) |
| C-3: `grep -q 'py_compile.compile(str(path), doraise=True)' scripts/py_compile_tree.py` | **Yes** — this is the defect | exit `0` en `5851b18` |
| `KI-056-2`: `sed -n 49p scripts/check_fix_reproduces.py` contiene `".json"` | **Yes** — this is the defect | exit `0` en `5851b18` |
| B-3: el split de `check_task_scope.py:109` sobre una fila de 3 celdas cuya segunda celda es un código con barra vertical escapada | **Yes** — this is the defect | 4 celdas en `5851b18` (la celda escapada se parte en dos), exit `0` |
| B-9, E, D4 hotfix, A-4, B-2, B-8, C-4, `KI-056-3`, `KI-056-8`, hooks duplicados | **Yes** — this is the defect | `unverified` — el test pareado de cada fila es la reproducción; se ejecuta contra `5851b18` antes del fix y su SHA va en el trailer `Repro:` (`rules/code_craft.md §6`) |
| B-4, B-5, B-7, C-1, C-2, C-5, C-9 | **Yes** — plausible, no confirmado | `unverified` — reproduce-first (D8) al inicio de su unidad |
| Suite existente | **No** — this is a regression to protect | `make verify` exit registrado en Verification |

---

## Verification

| Command | Expected | Dry run | Positive control |
| :--- | :--- | :--- | :--- |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/057-core-pipeline/IMPLEMENTATION_PLAN.md` | exit `0` | 2026-10-24: exit `0` (`[OK] audit_plan`) | quitar la sección `## Cost` hace salir `2` (`IMPLEMENTATION_PLAN_TEMPLATE.md:97`) |
| `make verify` | exit `0` | 2026-10-24 en Phase 1: exit `2`, solo por `check_task_scope: no task_scope.md under docs/sprints/057-core-pipeline` (lo crea Phase 4.3); `audit_plan --current-sprint` pasó antes. Tras Phase 4.3, 2026-10-24: exit `0` | run at close para la punta; en la base se registra el exit actual |
| `python3 scripts/check_changelog_tags.py` | exit `0`; en la base hay 45 tags `v4.*` (`git tag --list 'v4.*'`) y 45 cabeceras `## [4.` (`grep -c '^## \[4\.' CHANGELOG.md`) | run at close (W31 lo crea) | borrar una cabecera `## [4.38.0]` en una copia temporal hace salir `2` |
| `python3 scripts/session_state.py require-released --hotfix H-008` sobre un fixture de hotfix | exit `0` | run at close (W10 lo crea) | el mismo comando con `status: SUSPENDED` sale `2` |
| `python3 scripts/py_compile_tree.py` con `hooks/` en solo lectura | exit `0` y ningún `__pycache__` nuevo en `hooks/` | run at close (W14) | en la base el mismo comando escribe `hooks/__pycache__/` |
| `git -C . status --porcelain` tras cada unidad | solo los ficheros de la fila | por unidad | — |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `docs/guides/PROMPT_CRITERIA_GUIDE.md` | nuevo |
| `rules/qa_and_testing.md` | §4 escala S0–S3 |
| `rules/project_topology.md` | sección de BD con `.env.agent` y sondeo |
| `agents.md` | `RA-09`: excepción `.env.agent` |
| `workflows/deployment_workflow.md`, `pipeline_workflow.md`, `remediation_workflow.md`, `reconciliation_workflow.md` | ver W11, W27, W29, W22 |
| `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | columna `Severity` |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerado con `scripts/map_workflows.py` |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | `KI-056-2/3/4/5/7/8` cerrados; 057 registrado; 058-060 nombrados |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | veredicto por ítem del host H1 cerrado en 057 |
| `CHANGELOG.md` | entrada 057 bajo `[Unreleased]` con SHA por línea |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Canal upstream host → nucleus (Q1-Q6, canales A/B/C, filtro de intake) | Sprint 058, extensión de `agents.md §4` (decisiones en el borrador) |
| Reglas reproduce-first R-4, R-5/C-6, R-6, R-8, R-9/A-2, R-10, A-1, A-3 | Sprint 058 |
| `KI-056-1` (carga de permission prompts) con D-1, D-3, D-12; `F-055-N1`; `KI-056-6`/D-8; D-4; D-10; MCP de GitHub remoto con OAuth | Sprint 059 (régimen de sandbox). La parte de BD de D-12 sí entra en 057 (carril S0) |
| C-7 (`ADR-0017`, arquitectura de roles) | Sprint 059 |
| Auditoría de prompts del corpus existente | Sprint 060; 057 solo escribe los criterios (W00) |
| D-2, D-9, D-11 | rechazados el 2026-10-22: sin petición |

---

## Abort criterion

1. **Carril S0**: si W01 mide que el sandbox bloquea TCP a `localhost` (M1) o no puede
   leer `./.env.agent` con `allowRead` (M2), W02-W06 no se ejecutan; W01 se cierra con el
   bloqueo medido y la fila pasa a Sprint 059 como `KI-057-n`. El resto del sprint sigue.
2. **Sprint completo**: si un gate rechaza tres veces la misma familia S0/S1 sobre
   `claude/settings.hooks.json` o `scripts/merge_json.py`, esa unidad se revierte
   (`git revert`) y se abre `workflows/remediation_workflow.md` Phase 0; no se añade un
   cuarto vector a una enumeración (`agents.md §1 fail_closed_claims`).

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | pendiente |
| **Date** | pendiente |
| **Plan commit at approval** | pendiente |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
