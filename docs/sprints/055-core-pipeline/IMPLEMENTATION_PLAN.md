# Implementation Plan: Sprint 055 — sandbox-restrictions-and-secret-path

**Canonical path**: `docs/sprints/055-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/055` · **Base**: `main` at `16c3cca`
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

Los hosts que corren dentro del sandbox que el nucleus envía (`claude/settings.hooks.json`)
pierden tiempo en los mismos fallos. `F-115-N2` (`docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:1600`)
los consolida como `S-1`..`S-8`, **reportados por un host y sin medir en el nucleus**. El humano
añade en la sesión de apertura de este sprint tres frentes:

1. **Chromium no arranca bajo el sandbox** (`S-7`, observado también por el humano).
2. **Revisión de todas las restricciones del sandbox**, no solo de las ocho reportadas.
3. **graphify no lee la API key del LLM si el entorno no se exportó antes de lanzar la sesión.**

Medido en `16c3cca`:

| Hecho | Comando que lo reproduce | Resultado |
| :--- | :--- | :--- |
| La plantilla deniega `./.env.*`, que incluye el `.env.example` versionado (`S-2`) | `jq -e 'any(.sandbox.filesystem.denyRead[]; . == "./.env.*")' claude/settings.hooks.json` | exit `0` |
| `merge_json.merge` solo añade a las listas: quitar `./.env.*` de la plantilla **no** lo quita de un host ya instalado | snippet de `T5` (Tests) | exit `1` |
| `install.merge_into` hace traceback sobre un `settings.json` no escribible (`S-1`) | snippet de `T6` (Tests) | `PermissionError: [Errno 13]`, exit `1` |
| El advisory del bridge nombra la ruta del nucleus en un host | `grep -n 'bash scripts/install.sh' scripts/session_start.py` | `489`, exit `0` |
| El paquete `graphifyy 0.8.30` no carga `.env`: lee las keys solo de `os.environ` | `grep -rln load_dotenv venv_skillopt/lib/python3.13/site-packages/graphify` | sin salida |
| El paquete lee 7 variables de key; `skills/graphify/SKILL.md:238` afirma que solo 2 | `grep -rhoE '[A-Z_]+_API_KEY' venv_skillopt/lib/python3.13/site-packages/graphify` | 7 nombres distintos: `ANTHROPIC`, `DEEPSEEK`, `GEMINI`, `GOOGLE`, `MOONSHOT`, `OLLAMA`, `OPENAI` |
| `make graphify-update` usa el console-script que `rules/graphify.md` prohíbe (`bad interpreter`) | `grep -n 'venv_skillopt/bin/graphify$' Makefile` | `16`, exit `0` |
| No existe ninguna tabla de fallos de sandbox en las rules (`S-8`) | `grep -c -i sandbox rules/project_topology.md` | `0` |
| El nucleus no corre con la plantilla: no tiene `.claude/settings.json` | `ls .claude/` | solo `settings.local.json`, sin bloque `sandbox` |
| CLI instalada | `claude --version` | `2.1.119` |

**Causa raíz de graphify.** No es un defecto de graphify: la key vive en `.env`, la plantilla
deniega leer `.env` dentro del sandbox, y `RA-09` prohíbe al agente cargarlo en su contexto.
`RA-09` prescribe `Makefile`/`source .env` en un subshell, pero el subshell también está
sandboxeado. **El mecanismo que prescribe la regla está bloqueado por la plantilla que envía
el propio nucleus** (`S-3`). graphify es el primer consumidor que lo hace visible.

**Restricciones que la plantilla no trata** (documentación oficial de Claude Code,
`code.claude.com/docs/en/sandboxing`, sección Troubleshooting, leída el 2026-10-07):
`network.allowMachLookup` (cita literal: Playwright/iOS Simulator), `filesystem.allowWrite`
(store de pnpm, `S-6`), `excludedCommands` (`docker`, y CLIs en Go como `gh` con TLS roto bajo
Seatbelt, `S-5`), `network.allowLocalBinding` (dev servers en localhost), `allowAppleEvents`
(`open`/`osascript`, error `-600`; solo se honra desde user settings), `watchman` (`jest
--no-watchman`) y `allowUnsandboxedCommands`.

**Hecho cuando**: cada fallo de la matriz (`S-1`..`S-8`, Chromium, graphify y las restricciones
de arriba) tiene una forma sancionada, medida dentro de una sesión sandboxeada con la plantilla.
Esa forma está escrita en `rules/project_topology.md`, y `F-115-N2` está cerrado con el SHA de
cada fila.

---

## Design

| ID | Decisión | Elegida sobre | Razón |
| :--- | :--- | :--- | :--- |
| `D1` | **Medir antes de corregir.** `U01` reproduce la matriz completa en una sesión lanzada por el humano con `claude --settings claude/settings.hooks.json` desde el nucleus, y registra por fila: comando, exit, firma del error. Ninguna unidad de corrección empieza antes de que `U01` esté commiteada | Corregir según el reporte del host | Lo exige `F-115-N2` y varias filas son inferencias sobre la causa, no reproducciones. Además el nucleus no corre con su propia plantilla, así que sin `--settings` no hay sandbox que medir |
| `D2` | **Vía sancionada para secretos (`S-3`, graphify): wrapper cerrado `scripts/with_env.py`** (decisión del humano, 2026-10-07; **revisada** tras QA Gate 1 rondas 1 y 2, decisión del humano 2026-10-10). Lee `.env` en su propio proceso, nunca lo imprime, acepta **un solo nombre** de la allowlist (`config/with_env_allowlist.json`, nunca un argv), exige `-I` y sale con `2` ante cualquier otra cosa. Enmascara con `***` las copias exactas de valores de 4 o más caracteres en stdout/stderr del hijo, y eso **no es una frontera** (`e68ac72`). La exclusión del sandbox **no** va en la plantilla con ruta relativa: `install.py` renderiza en `.claude/settings.local.json` la línea **absoluta** (`<python3 absoluto> -I <ruta absoluta del wrapper> <name>`) y el `denyWrite` absoluto que la protege (`D2-R`, sección *Enmienda*). Motivo: una ruta relativa al directorio actual ejecuta cualquier `.agents/scripts/with_env.py` que el agente escriba en un subdirectorio (R2-1, medido) | (b) siempre humano; (c) `credentials.envVars` en modo `mask` | (b) bloquea la autonomía en cada `graphify --mode deep`. (c) solo se honra desde user settings, exige `network.tlsTerminate` (experimental) y una versión de Claude Code que no está medida, así que la plantilla del nucleus no podría enviarlo |
| `D3` | **Allowlist mínima y solo del nucleus** (revisada, decisión del humano 2026-10-10): tres nombres de graphify (`graphify-extract`, `graphify-extract-deep`, `graphify-label`). **Un host no la amplía**: vive dentro de `.agents/`, la plantilla la protege contra escritura y `§3 jurisdiction` / `submodule_purity` prohíben escribir ahí. Un host que necesite otro comando con secreto lo ejecuta como humano o lo propone al nucleus por `§4 feedback_upstream`. El flag `--allowlist <path>` de la versión original no existe (`e68ac72`) | Incluir `pytest` por defecto | Un comando excluido corre **sin sandbox**. `pytest` ejecuta código que escribió el agente, así que meterlo por defecto convierte el wrapper en una salida general del sandbox. graphify `update` solo parsea el AST, y `--mode deep` solo envía contenido al proveedor que elija el humano |
| `D4` | **`S-2`** (revisada en ejecución tras la medición en sesión sandboxeada, `SPRINT_LOG.md` U04): **mantener** `./.env` y `./.env.*` en `denyRead` y reabrir `./.env.example`, `./.env.sample` y `./.env.template` con `filesystem.allowRead`; la regla más estrecha gana, y la medición lo confirmó. Ningún valor de la plantilla se retira, así que la poda dirigida en `merge_json.py` que preveía la versión original no hace falta (`U04` omitida). El mecanismo general de valores retirados queda en `U22`, con `RETIRED_VALUES` vacío | Sustituir `./.env.*` por patrones de nombres con secretos, más la poda (versión original de esta fila); dejar que el host lo sobrescriba | Un `allowRead` estrecho reabre solo las plantillas sin secretos y deja negado todo lo demás, incluidos nombres de `.env.*` que nadie listó. Sustituir el patrón por una lista de nombres habría abierto cualquier variante no listada (`.env.prod`, `.env.staging2`). Sobrescribir en el host no sirve: `merge` solo añade a las listas y `install.py` re-mergea en cada boot |
| `D5` | **`S-1`**: `merge_into` comprueba la escritura antes de intentarla. Ante un `PermissionError` imprime el comando humano exacto **en forma host** (`bash .agents/scripts/install.sh --target claude`) y sale con un código documentado, sin traceback. `session_start.py:489` pasa a usar la forma según el modo | Permitir la ruta en la plantilla | La documentación lo prohíbe por diseño: `.claude/settings.json` es una *protected path* que no admite excepción |
| `D6` | **Chromium (`S-7`)**: la decisión depende de `U01`. **Rama A**: si `network.allowMachLookup` existe en la CLI medida y Chromium arranca con ella (registrando su forma real, booleano o lista de servicios), se documenta como **opt-in** en `rules/qa_and_testing.md` y no va en la plantilla, porque amplía la superficie del sandbox para todos los hosts. **Rama B**: si no basta, se usa el protocolo humano de `S-7`: el agente prepara el comando y el resultado esperado, el humano lo ejecuta y el agente registra la salida como evidencia | Activarlo por defecto en la plantilla | La documentación no dice qué servicios Mach expone ni si la CLI `2.1.119` lo soporta; activarlo sin medir sería afirmar algo que nadie comprobó |
| `D7` | **`S-5`/`S-6` y el resto de la revisión**: cada fila de la matriz recibe una de cuatro formas, sin otras: `allowWrite`/`allowedDomains` (sigue sandboxeado), `excludedCommands` con patrón estrecho, opt-in del humano en user settings, o ejecución humana. Se prefiere siempre la que mantiene el comando sandboxeado | `excludedCommands` amplios (`git *`, `pnpm *`) | Un patrón amplio cubre todo lo que puede hacer la herramienta (advertencia de la documentación) |
| `D8` | **`S-8`**: una sola tabla en `rules/project_topology.md` (que se carga al "ejecutar comandos locales") con: comando, firma en sandbox, forma sancionada y fila de `U01` que la prueba. Las demás rules y workflows **referencian** la tabla y no la repiten (`RA-14`) | Una nota en cada workflow | Si cada workflow repite su nota, se desalinean (precedente `RA-14`) |
| `D9` | **Drift de graphify**: `Makefile:16` pasa a la forma `-m graphify`. Se añade el target `graphify-deep`, que invoca `with_env.py`. La lista de keys de `SKILL.md:238` se corrige a las 7 medidas **si** el fichero no está vendorizado (`U12` lo comprueba primero). Si lo está, la corrección va solo en `rules/graphify.md` | Dejarlo para otro sprint | Es la misma causa que el humano reportó |

---

## Work

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `U01` | `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` | create — matriz `S-1`..`S-8` + Chromium/Playwright + graphify (`update` y `--mode deep` con key) + `docker`, `gh`, `git push`, `pnpm install`, `jest` con watchman, dev server en localhost, `open`, `allowMachLookup`; medida en una sesión lanzada por el humano con `claude --settings claude/settings.hooks.json`, con comando, exit y firma por fila | medium | `doc_orchestrator` (lanza el humano) | ⏳ |
| `U02` | `scripts/with_env.py` | create (`feat(`) + `tests/test_with_env.py`: un nombre de la allowlist (nunca argv), `-I` obligatorio, exit `2` en cualquier rechazo, enmascarado de copias exactas (no es frontera), sin `.env` → error explícito, `invoked_by:` en el docstring (forma revisada en `e68ac72`) | high | `implementer_agent` | ⏳ |
| `U03` | `config/with_env_allowlist.json` | create — solo `graphify` (`D3`) | medium | `implementer_agent` | ⏳ |
| `U04` | `scripts/merge_json.py` | **omitida en ejecución** (la medición mostró que basta `allowRead` estrecho, ver `D4` en `SPRINT_LOG.md`) — modify (`fix(`) + `tests/test_merge_json.py`: poda dirigida de valores retirados de la plantilla (`D4`, `T5`) | medium | `implementer_agent` | ⏳ |
| `U05` | `scripts/install.py` | modify (`fix(`) + `tests/test_install_permission.py`: sondeo de escritura, sin traceback, comando humano en forma host, exit documentado (`D5`, `T6`) | medium | `implementer_agent` | ⏳ |
| `U06` | `scripts/session_start.py` | modify (`fix(`) + `tests/test_session_start.py`: advisory del bridge según el modo (`T7`) | low | `implementer_agent` | ⏳ |
| `U07` | `claude/settings.hooks.json` | modify — `denyRead`/`allowRead` (`D4`), `excludedCommands` del wrapper (`D2`) y las formas que salgan de `U01` (`D7`) | high | `implementer_agent` | ⏳ |
| `U08` | `Makefile` | modify (`fix(`) + `tests/test_makefile_graphify.py`: `-m graphify` en `graphify-update` y nuevo `graphify-deep` vía `with_env.py` (`D9`) | low | `implementer_agent` | ⏳ |
| `U09` | `rules/project_topology.md` | modify — tabla de sandbox (`D8`) | medium | `doc_orchestrator` | ⏳ |
| `U10` | `rules/qa_and_testing.md` | modify — verificación con navegador, rama A o B (`D6`) | medium | `doc_orchestrator` | ⏳ |
| `U11` | `rules/graphify.md` | modify — key por `with_env.py`, `S-4` (walkers que fallan con `stat()`), lista de keys medida | low | `doc_orchestrator` | ⏳ |
| `U12` | `skills/graphify/SKILL.md` | **omitida** (Fase 4.2: vendorizado, import `cde6a71`, línea 747 del autor upstream) — corregir la línea 238 a las 7 keys; **se omite** si el fichero está vendorizado (`rules/skills_and_integrations.md §3`), dejando constancia en `SPRINT_LOG.md` | low | `skill_architect` | ⏳ |
| `U13` | `agents.md` | modify — reescribir `RA-09` y `§3 secret_sovereignty` con `with_env.py` como vía sancionada (`D2`) | high | `rule_validator` | ⏳ |
| `U14` | `workflows/pipeline_workflow.md` | modify — Phase 2: "export `.env`" pasa a `with_env.py` | low | `doc_orchestrator` | ⏳ |
| `U15` | `workflows/deployment_workflow.md` | modify — los pasos no sandboxeados se refieren a la tabla de `U09` (`S-5`) | low | `doc_orchestrator` | ⏳ |
| `U16` | `workflows/repository_hardening_workflow.md` | modify — lo mismo para las llamadas a `gh` (`S-5`) | low | `doc_orchestrator` | ⏳ |
| `U17` | `rules/LEGACY_RULE_CONCORDANCE.md` | modify — la fila de `Rule 66` sigue el nuevo texto de `RA-09` (`RA-14`) | low | `doc_orchestrator` | ⏳ |
| `U18` | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — cerrar `F-115-N2` con fila→SHA, reproducido en `U01` | low | `doc_orchestrator` | ⏳ |
| `U19` | `CHANGELOG.md` | modify — entrada en `[Unreleased]` con SHAs | low | `doc_orchestrator` | ⏳ |
| `U20` | `agents/devops_agent.md` | modify — `secret_sovereignty` (línea 16) y el texto de "`.env` export" pasan a `scripts/with_env.py` (`RA-14`, hallazgo de la Fase 4.3) | low | `agent_orchestrator` | ⏳ |
| `U21` | `README.md` | modify — recuento de *At a Glance* (44 scripts, 9 registros JSON) tras `U02`/`U03`; lo exige el check de deriva del README en `make verify` | low | `doc_orchestrator` | ⏳ |
| `U22` | `scripts/merge_json.py` | modify (`feat(`) + `tests/test_merge_json.py` — lista explícita de valores retirados (`RETIRED_VALUES`, vacía hoy) que `install.py` poda al fusionar: solo cadenas exactas que el framework publicó y retiró, nunca entradas del host; mismo patrón que `prune_deprecated_hooks`. Añadida por el humano el 2026-10-07 tras la omisión de `U04`: sin ella, una entrada peligrosa retirada de una plantilla publicada sobrevive para siempre en cada host | medium | `implementer_agent` | ⏳ |

Orden: `U01` → (`U02`, `U03`) → `U04`..`U08` → `U09`..`U17` → `U18`, `U19`. Si `U01` refuta una
fila del host, la unidad que la corrige se reduce a documentarla y la decisión queda en `SPRINT_LOG.md`.

---

## Dependencies

None. `scripts/with_env.py` parsea `.env` con la librería estándar (`KEY=VALUE`, comillas y
comentarios); no se añade `python-dotenv`.

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `scripts/with_env.py` (cada comando que necesita un secreto) | script | `Makefile` `graphify-deep`; `rules/project_topology.md` tabla de sandbox; `agents.md RA-09` |
| Poda de valores retirados en `merge_json.py` (en cada `install.py`) | script | `scripts/install.py` → `merge_into` (ya invocado por `session_start.py --boot`) |
| Sondeo de escritura en `install.py` (en cada boot) | script | `scripts/session_start.py` bridge step |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 29 (`U04` y `U12` omitidas; `U23`..`U29` de la Enmienda) | Count of rows in Work tables |
| Subagents dispatched | 19 units + 2 gates | `agent_assignment.md` |
| Prior session ratio | **5.0 (umbral blando alcanzado)** — esta sesión de Planning: primer turno 23264, pico 116084 | `python3 scripts/session_cost.py --from-anchor --json` |

El ratio blando se alcanzó en Planning por la lectura de la documentación del sandbox. Para
que la Execution no herede ese contexto, cada unidad se despacha a un subagente y el padre
solo transcribe estados en `task_scope.md`.

---

## Tests

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| `T1` `jq -e 'any(.sandbox.filesystem.allowRead[]?; . == "./.env.example")' claude/settings.hooks.json` (`D4` revisada: `./.env.*` sigue en `denyRead` y se reabre la plantilla con `allowRead`) | **Yes** — `S-2` | exit `1` en `16c3cca` (no hay `allowRead`) |
| `T2` `grep -q 'venv_skillopt/bin/graphify$' Makefile` | **Yes** — `D9` | exit `0` en `16c3cca` (línea 16) |
| `T3` `test -f scripts/with_env.py` | **Yes** — `S-3`/graphify, no hay vía sancionada | exit `1` en `16c3cca` |
| `T4` `grep -q -i sandbox rules/project_topology.md` | **Yes** — `S-8` | exit `1` en `16c3cca` |
| `T5` `venv_skillopt/bin/python -c` que llama a `merge(dest con un valor retirado, plantilla sin él)` y sale `0` si el valor desaparece y una entrada del host se conserva | **Yes** — `U22` (antes `D4`; con `D4` revisada `./.env.*` no se retira, así que el valor de prueba es uno inyectado en `RETIRED_VALUES` por el test) | exit `1` en `16c3cca` (el valor persiste: `merge` solo añade) |
| `T6` `venv_skillopt/bin/python -c` que llama a `install.merge_into` sobre un `settings.json` con `chmod 444` en el scratchpad | **Yes** — `S-1` | exit `1` en `16c3cca`, `PermissionError: [Errno 13]` con traceback |
| `T7` `grep -n 'bash scripts/install.sh' scripts/session_start.py` | **Yes** — advisory que no funciona en un host | exit `0` en `16c3cca` (línea 489) |
| `T8` `jq -e '.sandbox.network.allowMachLookup' claude/settings.hooks.json` | **Yes** — `S-7` sin tratar (rama A o B se decide en `U01`) | exit `1` en `16c3cca` |
| `T9` `make verify` | **No** — regresión a proteger | exit `0` en `16c3cca` |
| `T10` Matriz de `U01` en sesión sandboxeada | **Yes** — los fallos reportados | `unverified` — requiere que el humano lance una sesión con `claude --settings claude/settings.hooks.json`, lo que es en sí el entregable de `U01` |

---

## Verification

| Command | Expected | Dry run | Positive control |
| :--- | :--- | :--- | :--- |
| `make verify` | exit `0` | exit `0` en `16c3cca` | n/a (no es "no output") |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/055-core-pipeline/IMPLEMENTATION_PLAN.md` | exit `0` | `[OK]`, exit `0` sobre este borrador (2026-10-07) | n/a |
| `jq -e 'any(.sandbox.filesystem.denyRead[]; . == "./.env.*") and any(.sandbox.filesystem.allowRead[]?; . == "./.env.example")' claude/settings.hooks.json` (`D4` revisada) | `true`, exit `0` | `false`, exit `1` en `16c3cca` (`denyRead` presente, `allowRead` ausente) | n/a |
| `jq -e 'any(.sandbox.excludedCommands[]?; test("with_env.py"))' claude/settings.hooks.json` | `true`, exit `0` | `false`, exit `1` en `16c3cca` | n/a |
| `grep -n 'venv_skillopt/bin/graphify$' Makefile` | no output, exit `1` | `16:GRAPHIFY := …/bin/graphify`, exit `0` | el mismo comando en `16c3cca` imprime la línea 16: observado |
| `grep -n 'bash scripts/install.sh' scripts/session_start.py` | no output, exit `1` | `489`, exit `0` | el mismo comando en `16c3cca` imprime la línea 489: observado |
| `venv_skillopt/bin/python -m pytest tests/test_with_env.py tests/test_merge_json.py tests/test_install_permission.py tests/test_session_start.py tests/test_makefile_graphify.py -q` | exit `0` | run at close — `test_with_env.py`, `test_install_permission.py` y `test_makefile_graphify.py` no existen hasta `U02`/`U05`/`U08` | n/a |
| `python3 -I scripts/with_env.py curl` | exit `2`, `'curl' is not in config/with_env_allowlist.json` (forma revisada: sin `-I` el rechazo es `run as 'python3 -I …'`, también exit `2`) | run at close — el script no existe hasta `U02` | n/a |
| Re-ejecutar la matriz de `SANDBOX_MEASUREMENT.md` con la plantilla corregida | cada fila en su forma sancionada pasa | run at close — requiere una sesión sandboxeada lanzada por el humano tras `U07` | n/a |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | `RA-09` y `§3 secret_sovereignty`: `with_env.py` como vía sancionada |
| `rules/project_topology.md` | nueva tabla de sandbox (`S-8`) |
| `rules/qa_and_testing.md` | verificación con navegador bajo el sandbox |
| `rules/graphify.md` | keys vía `with_env.py`; `S-4`; lista de keys medida |
| `rules/LEGACY_RULE_CONCORDANCE.md` | la fila de `Rule 66` sigue a `RA-09` |
| `workflows/pipeline_workflow.md`, `deployment_workflow.md`, `repository_hardening_workflow.md` | se refieren a la tabla de sandbox |
| `skills/graphify/SKILL.md` | sin cambios: `U12` omitida (vendorizado) |
| `agents/devops_agent.md` | `secret_sovereignty` apunta a `with_env.py` (`U20`) |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `F-115-N2` cerrado |
| `CHANGELOG.md` | entrada en `[Unreleased]` |
| `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` | nuevo: la matriz medida |

**Measured figures.** Cada cifra de Context y Tests lleva al lado su comando.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `credentials.envVars` en modo `mask` (opción c de `S-3`) | Solo funciona desde user settings y con `tlsTerminate` experimental. Se registra en `rules/project_topology.md` como opt-in del humano, sin plantilla |
| `allowAppleEvents` | Solo se honra desde user/managed settings y quita el aislamiento de ejecución. Se documenta como opt-in humano en la tabla de `U09` |
| Actualizar la CLI `claude` desde `2.1.119` | Decisión del humano. Si `U01` muestra que hace falta una versión más reciente, se registra en `SPRINT_LOG.md` como precondición |
| Gate-commands host-blind (`KI-054-2`) | Sigue enrutado fuera; no es sandbox |

---

## Abort criterion

Se para y se revierte el sprint si ocurre cualquiera de estas cosas:
(1) `U01` no puede ejecutarse: el humano no puede lanzar una sesión con `--settings
claude/settings.hooks.json`, o la sesión arranca sin sandbox. Sin medición, `D1` prohíbe
corregir.
(2) `with_env.py` no logra que el comando de la allowlist lea la key bajo `excludedCommands`
en la sesión sandboxeada, o el valor del secreto aparece sin redactar en la salida del agente.
Eso refutaría `D2`, y la decisión vuelve al humano.

---

## Enmienda — QA Gate 1 ronda 2 (decisión del humano, 2026-10-10)

Veredicto de origen: `SPRINT_LOG.md` Quality Gate, QA ronda 2 (`REJECTED`, `charter`): R2-1, R2-2, R2-3 bloqueantes; R2-4..R2-9 registro.

| ID | Decisión | Elegida sobre | Razón |
| :--- | :--- | :--- | :--- |
| `D2-R` | `install.py` renderiza, en `<root>/.claude/settings.local.json` (no versionado, propio de la máquina), una línea de `sandbox.excludedCommands` por nombre de la allowlist con la forma `<python3 absoluto> -I <ruta absoluta del wrapper> <name>`, más `denyWrite` y `permissions.deny` `Edit` absolutos sobre lo que esa línea ejecuta. En host se protege **todo** `<host>/.agents` (el agente no escribe ahí por `§3 jurisdiction`). En nucleus se protegen el wrapper, la allowlist y `venv_skillopt`. Las tres líneas relativas salen de la plantilla | Quitar la exclusión (todo secreto lo ejecuta el humano); abortar el sprint | Una ruta absoluta protegida contra escritura no cambia con `cd`. Se conserva la autonomía de `graphify --mode deep` |
| `D2-N` | **Nucleus**: si `U25` muestra que renombrar un directorio padre (`mv scripts scripts_x` y recrear `scripts/with_env.py`) esquiva un `denyWrite` de fichero, el nucleus **no** recibe exclusión renderizada: los comandos con secreto los ejecuta el humano. El host no tiene ese problema si `denyWrite` sobre todo `.agents` bloquea el renombrado (`U25` lo mide) | Proteger todo `scripts/` del nucleus | En el nucleus el agente tiene que escribir en `scripts/`; protegerlo bloquearía el propio trabajo del sprint |
| `D3-R` | Ver `D3` revisada: allowlist solo del nucleus; el host no la amplía | Allowlist propia del host en ruta fija | Cierra la vía de escape, coherente con la lección de R2-1 |
| `D10` | `gh pr create *` y `gh release create *` salen de `excludedCommands`: crear PR o release lo hace el humano o el MCP de GitHub. Siguen excluidos `gh pr checks *`, `gh pr list *`, `gh repo view *`, `gh release view *`, `gh auth status` | Mantenerlos y confiar en el clasificador de permisos | `--body-file`, `--notes-file` y los assets leen cualquier fichero local fuera del sandbox y lo publican (R2-2); `RA-09` no nombra el clasificador como frontera |
| `D11` | Los cinco valores retirados (tres líneas relativas de `with_env.py` y los dos `gh … create`) entran en `RETIRED_VALUES` bajo `sandbox.excludedCommands`, para que salgan de cualquier host que instaló desde `ai-sprint/055`. Primer uso real de `U22`. R2-8 (un host que re-añade a propósito un valor retirado lo pierde en cada boot) queda documentado en el comentario de `RETIRED_VALUES` | No retirarlos porque ninguna release los publicó | Coste mínimo; cubre hosts instalados desde la rama |

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `U25` | `docs/sprints/055-core-pipeline/SANDBOX_MEASUREMENT.md` | medir **antes** de `U23` (`D1`), en fixture con forma de host y en fixture de nucleus, con `claude -p` sandboxeado: (a) sintaxis de ruta absoluta que honran `sandbox.filesystem.denyWrite` y `permissions.deny`; (b) si `sandbox.excludedCommands` de `settings.local.json` se suma al de `settings.json`; (c) la línea absoluta lee la key; (d) el impostor de R2-1 (`cd sub && <línea relativa>`) ya no corre fuera del sandbox; (e) renombrar el directorio padre del wrapper (host: `.agents`; nucleus: `scripts`) con `denyWrite` activo | medium | principal (como U01 y la sección 6) | ⏳ |
| `U23` | `scripts/install.py` | modify (`fix(`) + `tests/test_install_with_env_render.py`: render de `D2-R` en `settings.local.json` (merge no destructivo, idempotente), según el modo y el resultado de `U25` (`D2-N`) | high | `implementer_agent` | ⏳ |
| `U24` | `claude/settings.hooks.json` | modify — quitar las tres líneas relativas de `with_env.py` y `gh pr create *`, `gh release create *` (`D2-R`, `D10`) | high | `implementer_agent` | ⏳ |
| `U26` | `scripts/merge_json.py` | modify (`fix(`) + `tests/test_merge_json.py`: los cinco valores de `D11` en `RETIRED_VALUES`; comentario con R2-8 | medium | `implementer_agent` | ⏳ |
| `U27` | `tests/test_template_sandbox.py` | create — R2-9: la plantilla no tiene líneas relativas de `with_env.py` ni `gh * create`; `denyWrite` cubre wrapper, allowlist, venv y `.env` | low | `implementer_agent` | ⏳ |
| `U28` | `Makefile` | modify (`fix(`) + `tests/test_makefile_graphify.py`: `-I` en `GRAPHIFY` (R2-4) | low | `implementer_agent` | ⏳ |
| `U29` | `agents.md`, `agents/devops_agent.md`, `rules/project_topology.md`, `rules/graphify.md`, `workflows/pipeline_workflow.md`, `workflows/deployment_workflow.md`, `workflows/repository_hardening_workflow.md`, `docs/standards/templates/README_TEMPLATE.md`, `config/with_env_allowlist.json` (`_comment`), `scripts/with_env.py` (docstring), `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:1649`, `CHANGELOG.md` | modify, **un commit por fichero** (`RA-14`): la forma absoluta renderizada y dónde leerla (`.claude/settings.local.json`), allowlist solo del nucleus (`D3-R`), `gh … create` lo ejecuta el humano (`D10`), etiqueta `graphify extract . --mode deep` (R2-5), fila S-3 de la auditoría con `e68ac72`/`cfe7950` y los nuevos SHAs (R2-7) | medium | `rule_validator` (`agents.md`), `agent_orchestrator` (`agents/devops_agent.md`), `implementer_agent` (`config/`, `scripts/`), `doc_orchestrator` (resto) | ⏳ |

**`§1 path_type`.** Ningún fichero versionado guarda una ruta absoluta: `install.py` la calcula al instalar y la escribe solo en `.claude/settings.local.json`, que `ensure_gitignore_entries` ya excluye de git y es propio de la máquina. El código, la plantilla y la allowlist siguen en rutas relativas.

R2-6 (trailer de `1fa9608` con el padre equivocado) se registra en `SPRINT_LOG.md`; no se reescribe historia.

Orden: `U25` → `U24`, `U26`, `U27`, `U28` → `U23` → re-medición de `U25` (d) y (e) con el render real → `U29` → QA Gate 1 ronda 3 (agente nuevo) → Tester Gate 2.

| Verification (enmienda) | Expected |
| :--- | :--- |
| `jq -e '[.sandbox.excludedCommands[] \| select(test("with_env\\.py") or test("^gh (pr\|release) create"))] \| length == 0' claude/settings.hooks.json` | `true`, exit `0` |
| `venv_skillopt/bin/python -m pytest tests/test_install_with_env_render.py tests/test_template_sandbox.py tests/test_merge_json.py tests/test_makefile_graphify.py -q` | exit `0` |
| Caso impostor de R2-1 en sesión sandboxeada con el render real (`U25` d) | el impostor no lee `.env` (exit distinto de `0` o `PermissionError`) |
| `make verify` | exit `0` |

**Abort criterion 3.** Si `U25` muestra que ni la línea absoluta en `settings.local.json` se honra (b, c) ni hay una ruta absoluta que `denyWrite` respete (a), o que en host el renombrado de `.agents` esquiva el `denyWrite` (e), se aplica la alternativa descartada en `D2-R`: `with_env.py` sale de `excludedCommands` en todos los modos y todo comando con secreto lo ejecuta el humano. La decisión queda en `SPRINT_LOG.md` y no se vuelve a preguntar.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal (chat, Phase 5) |
| **Date** | 2026-10-07 |
| **Plan commit at approval** | `abf2928` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
