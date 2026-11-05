# Implementation Plan: Sprint 059 — efficiency-and-sandbox-regime

**Canonical path**: `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/059` · **Base**: `main` at `08c669c`
**Status**: `DRAFT` → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

Sprint 059 nació como el sprint del régimen de sandbox, en el orden decidido el
2026-10-22 (`docs/sprints/057-core-pipeline/IMPLEMENTATION_PLAN.md:322-323`,
`docs/sprints/058-core-pipeline/IMPLEMENTATION_PLAN.md:383-387`). El 2026-11-02 el
humano amplió el alcance a la cola completa y le sumó la eficiencia del propio
framework, con este principio: **el núcleo es la matriz que se adhiere a cualquier
módulo; el framework existe para optimizar la gestión, y su propio coste es un
defecto de definición.** El orden de las waves sigue ese principio: primero lo que
abarata y acelera todo lo que viene después.

**Intake triage (Phase 1, `agents.md §4 feedback_upstream`).**

| Canal | Resultado | Comando | Exit |
| :--- | :--- | :--- | :--- |
| A | vacío: no hay `.upstream_hosts.json` registrado | `python3 scripts/session_start.py --boot --tool claude-code --session-id <id>` | 0 |
| B | vacío: ningún issue `host-finding` abierto | `gh issue list --label host-finding --state open` (sin sandbox: `HTTPS_PROXY` sin definir) | 0 |
| `F-116-N1` | **accept** (reproducido) — 11 de 33 transcripts del núcleo tienen `first_turn` = 0 en el ciclo 1, así que `ratio` es `None` | bucle de `python3 -I scripts/session_cost.py --session <id> --json` sobre `~/.claude/projects/-Users-gstmirabal-Developer--agents/*.jsonl` | 0 por sesión; recuento `sessions=33 first_turn_zero_cycle1=11` |
| `F-116-N2` | **accept** (reproducido) — ningún hook invoca `session_cost.py` ni `session_probe.py` | `grep -rn -e session_cost -e session_probe hooks/` | 1 (sin salida) |

**Problemas medidos, agrupados por lo que cuestan.**

| # | Problema | Medida |
| :--- | :--- | :--- |
| P1 | `agents.md` se carga en cada petición, también en cada subagente | `wc -c agents.md` → 53.907 bytes (~12k tokens); 14 filas suman 25.736 bytes, casi todo historia y precedentes |
| P2 | `qa-agent` corre en `opus` y es la primera recomendación de ahorro de `/usage` | `agents/qa_agent.md:5` `model: opus`; despachado en 13 sesiones de un host y 10 del núcleo (`grep -rl '"subagent_type":"qa-agent"'` sobre los transcripts) |
| P3 | Phase 6 ejecuta las unidades de una en una aunque `jurisdictional_lock` ya garantiza archivos disjuntos | `workflows/pipeline_workflow.md` Phase 6 no nombra paralelismo; `task_scope.md` no tiene columna de dependencias |
| P4 | Autorizaciones de Bash constantes en el núcleo: el núcleo no tiene la plantilla de sandbox con `autoAllowBashIfSandboxed` que sí reciben los hosts | `.claude/` del núcleo solo tiene `settings.local.json` con 7 permisos sueltos; `claude/settings.hooks.json:45` tiene `autoAllowBashIfSandboxed: true` solo para hosts; `scripts/install.py` `install_nucleus_bridge` no instala sandbox |
| P5 | `/clear` no suspende la sesión en el núcleo: el hook `SessionEnd` ejecuta `.agents/scripts/session_end_hook.py`, ruta que solo existe en un host | `claude/settings.hooks.json:129` |
| P6 | La cota §3.1 se mide contra una baseline 0 en un tercio de las sesiones y nadie la mide mientras la sesión corre (`F-116-N1`, `F-116-N2`, `KI-058-3`); el ecosistema token-saver solo mide al arrancar | sesión previa `7204cadc` a **9.2×** sin señal (`python3 -I scripts/session_cost.py --from-anchor --json`, exit 0) |
| P7 | Régimen de sandbox: `KI-056-1` (absorbe D-1, D-3, D-12, `KI-054-5`), `KI-056-6` (absorbe D-8), `F-055-N1`, `KI-057-1` (TCP a `127.0.0.1` denegado), D-4, D-10 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:2137-2151`, `docs/roadmaps/core/pipeline/021-030-program-queue.md:380-395` |
| P8 | `KI-057-2`: `SessionEnd` puede suspender otra sesión | `docs/roadmaps/core/pipeline/021-030-program-queue.md:396` |
| P9 | MCP de GitHub remoto con OAuth; actions de `ci.yml` con tags móviles | `.github/workflows/ci.yml:24`, `:28`, `:39` (`@v4`, `@v5`, `@v2`) |
| P10 | C-7: la separación owner/writer (`ADR-0017`) cuesta un dispatch por paso trivial | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:2137` |
| P11 | Residuos del 058 (decisión humana 2026-11-02: cerrar en este sprint todo lo que depende del núcleo): `KI-058-1` (`check_absolute_paths.py` solo mira archivos trackeados), `KI-058-4` (`read_text_file` sin chequeo de archivo regular), `KI-058-5` (cuatro residuos S3), y los puntos 3-5 de la propuesta E — su texto no está en el repositorio; decisión humana 2026-11-02 en Phase 5: se enruta a un `KI-059-n` (Z-02) con condición de desbloqueo "recuperar su texto" | `docs/roadmaps/core/pipeline/021-030-program-queue.md:407-411`; `scripts/upstream_outbox.py:94` (`PIN_PATTERN`), `:136` (`read_regular_bytes`), `:197` (`read_text_file`) |

**Hecho en Phase 1, fuera de los repositorios.** Los symlinks
`.claude/commands/agents/` (ignorados por git, recreables con `install.py`) se
borraron en WhatsApp-Chat-Extractor, Django-Users-App y Django-Pro-Template: 0
sesiones con `/agents:` en sus transcripts. Cryptobot (24 sesiones) y el núcleo (19)
los conservan.

**Hecho cuando**: `agents.md` ≤ 20.000 bytes; `qa_agent` en `sonnet` con criterio de
vuelta; Phase 6 despacha lotes paralelos calculados por script; el núcleo trabaja con
sandbox y `autoAllowBashIfSandboxed`, con un recuento de autorizaciones antes y
después; la cota §3.1 tiene baseline no nula y un invocador en sesión decidido por
ADR; la enumeración `RA-19` está re-medida; cada ítem restante está entregado o
enrutado con destino nombrado.

---

## Design

| ID | Decisión | Alternativa rechazada y por qué |
| :--- | :--- | :--- |
| D0 | **Orden por apalancamiento**: las waves 1-2 abaratan (P1, P2) y aceleran (P3, P4, P5) todo lo que viene después; por eso van antes que el resto aunque el sprint se llamara "régimen de sandbox" | Orden de la cola original (sandbox primero): cada wave posterior pagaría el `agents.md` de 54 KB, las autorizaciones y la ejecución en serie |
| D1 | Baseline del ciclo = tamaño de contexto del primer turno: `cache_read + cache_creation + input` (`F-116-N1`, decidido en triage) | Mínimo `cache_read` no nulo (propuesta del host): descarta el turno real de arranque |
| D2 | El medidor en sesión es un **paso de workflow** en Phase 6 (decisión humana 2026-11-02). **Provisional**: ADR-0018 (A-07) puede sustituirlo por el método del debate (D8); si el debate no cierra, D2 se implementa tal cual | Hook periódico: corre fuera del sandbox y obliga a re-medir `RA-19` |
| D3 | En hard (15×) el medidor **solo avisa** (exit 0) mientras la calibración sea n=1 (decisión humana 2026-11-02) | Exit 2 en hard: con n=1 el riesgo de bloqueo falso es alto |
| D4 | Las autorizaciones se cuentan **desde transcripts** con un script determinista antes de cambiar `RA-09` o la configuración del núcleo | Revisar por impresión: es lo que produjo 055/056 |
| D5 | `make verify` deja de escribir dentro de `./.agents`: compilar en memoria y comparar el manifiesto sin reescribirlo | Excluir esos pasos en host: deja el host sin verificar |
| D6 | Cualquier cambio a `RA-09`/`RA-19` (D-12, `KI-057-1`) y la instalación de hooks en el núcleo se deciden por ADR-0019 **después** de la re-medición C-01 | Amendment directo: `RA-19` prohíbe afirmar límites sin enumeración medida |
| D7 | C-7 se resuelve con ADR-0020 que enmienda `ADR-0017`; la implementación del registro solo si el ADR se aprueba | Implementar sin ADR: C-7 se aceptó "para debate" |
| D8 | Estudio → debate → ADR antes de tocar el instrumental token-saver: A-00 inventaría qué mide cada pieza (`skills/token-saver-auditor`, `skills/omni-context-minimizer`, `scripts/session_probe.py`, `scripts/session_cost.py`) y **cuándo**, y los mecanismos de Claude Code (auto-compact y `/compact`, `/context`, `statusLine`, hooks `PostToolUse`/`PreCompact`/`Stop`, subagentes como aislamiento de contexto, carga progresiva de skills y `rules/`, prompt caching), cada uno con coste, dentro o fuera del sandbox y si es determinista; incluye si `install.py` debe instalar los comandos `agents:*` solo por opt-in | Implementar `--bound` directamente: resuelve el síntoma de `F-116-N2` y deja sin estudiar el ecosistema |
| D9 | `qa_agent` pasa al tier `author` (`sonnet`) como **prueba** con criterio de vuelta (abort 4). `tester_agent` y `principal_agent` siguen en `opus` | Bajar también a Tester: deja el sprint sin revisor `opus`; el `basis` del tier `gate` documenta que los defectos centrales los halló un gate |
| D10 | `agents.md` queda como índice: una o dos frases por fila más un puntero; medición, historia y precedentes se mueven a archivos que ya se cargan bajo demanda. Objetivo ≤ 20.000 bytes. Destinos primero, recorte después, `make verify` por fila | Borrar la historia: los precedentes son la razón de cada regla y `RA-14` exige rastrearlos |
| D11 | **Paralelismo en Phase 6**: `task_scope.md` gana la columna `Depends on`; `scripts/check_task_scope.py` calcula los lotes (unidades cuyas dependencias aterrizaron y cuyos archivos son disjuntos); cada lote se despacha en paralelo, **máximo 4 subagentes**, cada uno con `isolation: "worktree"`; el orchestrator integra los commits en el orden de la tabla. Los gates de Phase 7 siguen en serie al final de cada wave (`RA-13`); Phase 5 sigue siendo manual | Paralelismo por criterio del agente: no es reproducible ni auditable. Más de 4: la integración cuesta más de lo que ahorra, y el límite se puede subir en `/config` |
| D12 | **Autonomía en el núcleo sin abrir una vía fuera del sandbox**: B-06 instala en el núcleo solo el bloque `sandbox` con `autoAllowBashIfSandboxed: true`, sin hooks; los hooks del núcleo (que corren fuera del sandbox código que el agente puede escribir, clase `F-055-N1` `Q1`) esperan a ADR-0019 (E-01b). Coste conocido: bajo sandbox, `gh` falla por TLS (D-3) y pasa al humano | Instalar la plantilla completa de host en el núcleo: en el núcleo `scripts/` y `hooks/` no tienen write-deny, así que cada hook ejecutaría fuera del sandbox código escribible por el agente |
| D14 | **Presupuesto por unidad y puntos de suspend planificados**: `task_scope.md` gana dos columnas: `Est. cost` (tokens estimados de la unidad, según su tipo y su riesgo) y `Suspend after` (`yes` en la unidad tras la cual se suspende). La tabla de estimación sale de lo medido en A-00: coste real por unidad de sprints anteriores, cruzando los commits `✅ <sha>` de cada `task_scope.md` con los turnos de `session_cost.py`. `check_task_scope.py` acumula `Est. cost` en orden de ejecución y exige un `Suspend after: yes` antes de que el acumulado proyecte el ciclo por encima de soft (5×) sobre la baseline D1; una wave más grande que eso se parte en la planificación, no a mitad de la ejecución | Suspender solo por la medición en sesión (D2): avisa cuando el ciclo ya creció. Con el presupuesto, la sesión larga se evita al planificar, y la medición en sesión sirve para comprobar la estimación |
| D15 | **Destino para la historia sin dueño** (decisión humana 2026-11-02, Phase 6 wave 1): A-13 crea `docs/guides/RULE_PRECEDENTS_GUIDE.md` porque llegar a 20.000 bytes exige ~51 de 131 filas en ≤ 200 bytes y ~40 de ellas no tenían destino para su historia | Bajar la meta a ~30.000 (solo los 9 términos planificados): deja `agents.md` en ~12k→~7k tokens en vez de ~5k. Repartir en los archivos existentes: 6-10 unidades más en la wave 1 |
| D16 | **Desviación registrada, no decisión de diseño** (2026-11-04, Phase 6 wave 1): el orchestrator despachó A-11, A-13, A-08 y A-01 a la vez tras leer como orden una pregunta del humano sobre paralelismo; `agent_assignment.md` declaraba la wave 1 en serie y ninguna norma lo permitía. El humano lo detuvo y decidió conservar el trabajo tras comprobarlo y volver al orden aprobado. **No es precedente**: A-12 y la wave 2 van en serie, y los lotes solo existen desde la wave 3 con G-01 y G-02 (D11). Los agentes no tocaron git; el orchestrator comprobó cada unidad y la integró una a una | Descartar el trabajo y repetirlo en serie: mismo resultado en archivos independientes, con más coste |
| D17 | **La prueba D9 necesita un ADR que sustituya a `ADR-0003`** (decisión humana 2026-11-04, Phase 6 wave 1): `ADR-0003` prohíbe mover `qa_agent` del tier `gate` sin un ADR nuevo que lo sustituya, y ni este plan ni la auditoría de Phase 4 lo nombraron. A-14 crea `ADR-0021`, que sustituye solo esa cláusula para `qa_agent` durante la prueba, con el criterio de vuelta del abort 4; `tester_agent` y `principal_agent` siguen bajo `ADR-0003` | Descartar A-08: `qa_agent` sigue en `opus` y se pierde el ahorro de D9 |
| D18 | **Reparto de `agents.md` por riesgo** (decisión humana 2026-11-04, Phase 6 wave 1): regla con script que bloquea: una línea; general sin script: completa en `agents.md`; de una tarea concreta sin script: en un archivo `rules/` con disparador (A-15, A-16, A-17); historia y precedentes: `RULE_PRECEDENTS_GUIDE.md`. Objetivo sin cambios: ≤ 20.000 bytes. Límite asumido: un disparador lo sigue el agente, no bloquea; los scripts para reglas sin instrumento pasan a `KI-059-5` | Autosuficiente en ~29.000 bytes: revierte D15 por ~2.000 tokens por carga. Índice sin disparador: reglas vigentes en un archivo que nada obliga a leer |
| D13 | `/clear` es el gesto de fin de sesión; `suspend` ocurre solo por `SessionEnd`. Requiere E-01 (suspender solo la sesión que termina) y E-01b (el hook en el núcleo). Hasta entonces, en el núcleo `suspend` se corre a mano antes de `/clear` | Cambiar la naturaleza de `suspend`: `/clear` libera contexto y `suspend` registra estado en el ancla; son dos funciones distintas y hacen falta las dos |

---

## Work

Una tabla por wave, en orden de ejecución. `tras X` en Operation es la dependencia
que G-01 convierte en la columna `Depends on` de `task_scope.md`. Desde la wave 3,
las unidades sin dependencia pendiente van en lotes paralelos (D11). La wave 1 registra una desviación: D16.

### Wave 1 — Palancas de coste (abaratan cada petición posterior)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A-05 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — veredictos de triage de esta Context (`F-116-N1`, `F-116-N2`: `accept` con su comando y exit); el cierre de ambos lo marca C-02 | low | `doc_orchestrator` | ✅ `1dbe533` |
| A-09 | `rules/code_craft.md` | modify — recibe medición e historia de `linter_command` (Python, JS/TS), `max_indentation`, `max_lines_per_func`, `fail_closed_claims`, `exception_handling` (D10) | medium | `rule_validator` | ✅ `0c7a9b2` |
| A-10 | `rules/project_topology.md` | modify — recibe historia y precedentes de `RA-09`, `RA-19`, `jurisdiction` (D10) | medium | `rule_validator` | ✅ `a694ffe` |
| A-11 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify — recibe transporte, canales, triage y cierre de `feedback_upstream` (D10) | low | `doc_orchestrator` | ✅ `72ac88b` |
| A-13 | `docs/guides/RULE_PRECEDENTS_GUIDE.md` | create — recibe la historia, la medición y los precedentes de cada fila de `agents.md` que A-12 recorta y cuyo detalle no reciben A-09, A-10 ni A-11, indexados por sección y clave de la regla (D10); texto movido literal, sin reescribir | medium | `doc_orchestrator` | ✅ `a014f4f` |
| A-15 | `rules/skills_and_integrations.md` | modify — recibe literal `three_file_standard`, `topological_order`, `enforcement` desde `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: la guía deja un puntero en su lugar | low | `rule_validator` | ✅ `18b692e` |
| A-16 | `rules/qa_and_testing.md` | modify — recibe literal `local_testing` desde `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: la guía deja un puntero en su lugar | low | `rule_validator` | ✅ `9b8db89` |
| A-17 | `rules/project_topology.md` | modify — recibe literal `min_release_age`, `only_built_deps`, `config_file` desde `docs/guides/RULE_PRECEDENTS_GUIDE.md` (D18); companion: la guía deja un puntero y `config/rule_triggers.json` añade `pnpm-workspace.yaml`, `package.json` y `.npmrc` a los `globs` de ese archivo | low | `rule_validator` | ✅ `d133bc2` |
| A-12 | `agents.md` | modify — tras A-09, A-10, A-11, A-13, A-15, A-16, A-17, con el reparto D18: filas recortadas a regla + puntero, ≤ 20.000 bytes; `make verify` exit 0. Antes de recortar, `grep -n "agents.md" tests/*.py` lista las cadenas que un test fija en `agents.md` (p. ej. `RA-18` en `tests/test_cursor_phase1.py`, la línea `EMITTED` de `tests/test_gate_row_wording.py`, la fila `Command paths`) y cada una se conserva. `RA-14`: por cada término cuyo detalle se mueve (`feedback_upstream`, `jurisdiction`, `RA-09`, `RA-19`, `linter_command`, `max_indentation`, `max_lines_per_func`, `fail_closed_claims`, `exception_handling`), `grep -rn "<término>" agents.md rules/ workflows/ docs/guides/ docs/standards/ scripts/ hooks/ tests/` y cada cita que apunte al texto movido se actualiza al nuevo destino en el mismo commit | high | `rule_validator` | ✅ `d6f5756` |
| A-14 | `docs/decisions/ADR-0021-qa-agent-tier-trial.md` | create — tras A-12: sustituye la cláusula de `ADR-0003` solo para `qa_agent` durante la prueba D9, con el criterio de vuelta del abort 4 (D17); `ADR-0003` no se edita; companion obligatorio `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` (`:19`, que repite la regla, y `:140`) | medium | `doc_orchestrator` | ✅ `ed96115` |
| A-08 | `agents/qa_agent.md` | modify — tras A-14: `model: sonnet`, `tier: author` (D9); companion obligatorio `config/model_tiers.json` (mover `qa_agent` a `author.profiles`; añadir al `basis` de `gate` la prueba y su criterio de vuelta), porque `scripts/check_model_tiers.py` exige que coincidan; companion `tests/test_agent_profile_census.py` (fija la lista `gate` y mantiene a `qa_agent` sin `Write`/`Edit`) | medium | `implementer_agent` | ✅ `80518b4` |
| A-01 | `scripts/session_cost.py` | modify — `fix(`: baseline D1 en `cycle_summary`; paired test `tests/test_session_cost.py` (nuevo) con un turno `cache_read` 0 / `cache_creation` > 0 | medium | `implementer_agent` | ✅ `ef490cd` |

### Wave 2 — Ritmo y autonomía (aceleran el resto del sprint)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G-01 | `scripts/check_task_scope.py` | modify — columna `Depends on` y subcomando que imprime los lotes paralelos (dependencias aterrizadas, archivos disjuntos, máximo 4); tests en `tests/test_check_task_scope.py` | medium | `implementer_agent` | ⏳ |
| G-02 | `workflows/pipeline_workflow.md` | modify — tras G-01: Phase 6 despacha cada lote en paralelo con `isolation: "worktree"` e integra en orden; Phase 7 sigue en serie por wave (D11). Tras integrar cada lote, el orchestrator borra cada worktree y su rama (`git worktree remove <path>`, `git branch -D <rama>`) antes del lote siguiente, porque `scripts/branch_sovereignty.py` niega el sello de cierre con una rama sin integrar; y re-ejecuta sobre `ai-sprint/[ID]` las comprobaciones de `hooks/on_commit.py` que el commit en el worktree no vio (`python3 scripts/check_task_scope.py --sprint-dir <dir>`), exit 0 antes del lote siguiente | medium | `orchestrator` | ⏳ |
| B-01 | `scripts/prompt_count.py` | create — cuenta autorizaciones por sesión desde transcripts, `--json`; test `tests/test_prompt_count.py` | medium | `implementer_agent` | ⏳ |
| B-02 | `docs/sprints/059-core-pipeline/PROMPT_MEASUREMENT.md` | create — tras B-01: recuento base de una sesión real de núcleo y una de host (genericizada, `RA-15`); re-medición tras B-06 | low | `doc_orchestrator` | ⏳ |
| B-07 | `workflows/close_workflow.md` | modify — tras B-01: paso advisory que corre `python3 scripts/prompt_count.py --session <id> --json` sobre la sesión que cierra e imprime el recuento; es el invocador `RA-16` de B-01 | low | `orchestrator` | ⏳ |
| B-06 | `scripts/install.py` | modify — tras B-02: `install_nucleus_bridge` instala el bloque `sandbox` con `autoAllowBashIfSandboxed: true`, sin hooks y sin `excludedCommands` (D12); test nuevo `tests/test_install_nucleus_sandbox.py` | high | `implementer_agent` | ⏳ |
| E-01 | `scripts/session_state.py` | modify — `fix(`: `suspend` desde `SessionEnd` solo actúa si el `session_id` del hook coincide con el del anchor (`KI-057-2`); paired test `tests/test_session_end_hook.py`. Reproducir primero; si no se reproduce, `RECORD` | medium | `implementer_agent` | ⏳ |
| E-01c | `scripts/session_state.py` | modify — tras E-01: `fix(` del hueco medido en Phase 1: entre sprints (sprint sellado, sesión `IN_PROGRESS`) `suspend` imprime "Sprint is sealed — nothing was suspended", exit 0, y deja el lock tomado, así que el boot siguiente sale 2 y exige `--takeover`; `suspend` libera el lock de la sesión sin tocar el sprint sellado; paired test en `tests/test_session_state.py` | medium | `implementer_agent` | ⏳ |

### Wave 3 — Token economy en sesión (estudio, debate, decisión)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A-00 | `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | create — estudio D8: tabla por pieza y por mecanismo con fuente; crecimiento de contexto boot→cierre en las sesiones del núcleo (`session_cost.py --json`); **coste real por unidad** en los sprints 056-058 (commits `✅ <sha>` de `task_scope.md` cruzados con turnos del transcript), agrupado por operación (create/modify, script/doc/rule) y riesgo, como base de la tabla de estimación D14; 2-4 métodos candidatos | medium | `token_economy_agent` | ⏳ |
| A-06 | `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md` | modify — tras A-00: sección `Debate` con opciones, objeciones y decisión del humano | low | `doc_orchestrator` | ⏳ |
| A-07 | `docs/decisions/ADR-0018-in-session-token-economy.md` | create — tras A-06: método elegido; confirma o sustituye D2; lo que no entra pasa a `KI-059-n` | medium | `principal_agent` (owner) / `doc_orchestrator` (writer) | ⏳ |
| A-02 | `scripts/session_cost.py` | modify — tras A-01, A-07: `feat(` flag `--bound` (`OK`/`SOFT`/`HARD`, exit 0, D3) o la forma que fije ADR-0018; test en `tests/test_session_cost.py` | medium | `implementer_agent` | ⏳ |
| A-03 | `rules/token_economy.md` | modify — tras A-07: §3.1 nueva unidad (D1), invocador en sesión y el presupuesto por unidad con puntos de suspend planificados (D14) | low | `rule_validator` | ⏳ |
| H-01 | `config/unit_cost_estimates.json` | create — tras A-07: tabla de estimación por tipo de unidad y riesgo, con la fuente de cada cifra (A-00) y su `measured_at` | low | `token_economy_agent` | ⏳ |
| H-02 | `scripts/check_task_scope.py` | modify — tras G-01, H-01: columnas `Est. cost` y `Suspend after`; acumula el coste en orden y sale 2 si el acumulado proyecta el ciclo por encima de soft (5×) sin un `Suspend after: yes` previo (D14); tests en `tests/test_check_task_scope.py` | medium | `implementer_agent` | ⏳ |
| H-03 | `workflows/close_workflow.md` | modify — tras H-01, B-07: paso advisory que compara el coste medido de cada unidad del sprint (`session_cost.py --json`) con su `Est. cost` e imprime la diferencia; es el invocador `RA-16` de la recalibración de `config/unit_cost_estimates.json`, que `token_economy_agent` aplica en el sprint siguiente | low | `orchestrator` | ⏳ |
| A-04 | `workflows/pipeline_workflow.md` | modify — tras G-02, A-02, H-02: Phase 4.3 rellena `Est. cost`/`Suspend after`; Phase 6 corre la medición en cada unidad (invocador `RA-16` de A-02), compara lo medido con `Est. cost` y ejecuta `session_state.py suspend` en cada `Suspend after: yes` | low | `orchestrator` | ⏳ |

### Wave 4 — Medición del sandbox

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B-03 | `scripts/py_compile_tree.py` | modify — compilar sin escribir `.pyc` (D5); test en `tests/test_verify_py_compile.py` | medium | `implementer_agent` | ⏳ |
| B-04 | `skills/mass-standardizer/scripts/generate_manifest.py` | modify — modo `--check` que compara sin reescribir `skills/manifest_skills.json` (D5): exit 0 si coincide, exit 2 si difiere, y el archivo queda con el mismo hash; test en `tests/test_mass_standardizer.py` | medium | `skill_architect` | ⏳ |
| B-05 | `Makefile` | modify — tras B-03, B-04: `verify` usa ambos modos sin escritura | low | `implementer_agent` | ⏳ |
| C-01 | `docs/sprints/059-core-pipeline/SANDBOX_ENUMERATION.md` | create — re-medición `RA-19` para el CLI actual: miembros `E16` sin probar, subárboles inferidos por contención, `Edit(/.git/modules/.agents/**)`, D-8; incluye el núcleo con el sandbox de B-06. `devops_agent` mide con `model: sonnet` (escalado desde `mechanical` por riesgo high) y entrega la salida literal; `doc_orchestrator` escribe | high | `devops_agent` | ⏳ |
| C-02 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — tras C-01, A-02: `F-055-N1` pasa a cerrado si C-01 mide su vector sin punto escribible por el agente, o queda abierto con la medida de C-01 citada; `F-116-N1` se marca cerrado citando el commit de A-01 y `F-116-N2` citando el de A-02 | low | `doc_orchestrator` | ⏳ |

### Wave 5 — Régimen (decisiones con las medidas en la mano)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `docs/decisions/ADR-0019-sandbox-regime.md` | create — tras B-02, C-01: `RA-09`, fila `gh`, D-12, ruta BD (`KI-057-1`) y hooks en el núcleo (D6, D12) | high | `principal_agent` (owner) / `doc_orchestrator` (writer) | ⏳ |
| D-02 | `agents.md` | modify — tras A-12, D-01: `RA-09` y `§2 graph_sync` (D-10); `wc -c agents.md` ≤ 20000 tras el cambio, y el detalle nuevo va a `rules/project_topology.md` (D-03), no a `agents.md` | high | `rule_validator` | ⏳ |
| D-03 | `rules/project_topology.md` | modify — tras A-10, D-01: §4 fila `gh` (D-3), D-1, D-4, coste de `git -C .agents fetch` (QA2-3) | medium | `rule_validator` | ⏳ |
| D-04 | `claude/settings.hooks.json` | modify — tras D-01: bloque `sandbox` (ruta BD local, `KI-057-1`) solo si ADR-0019 aprueba una ruta medida; si no, `RECORD` | high | `implementer_agent` | ⏳ |
| E-01b | `claude/settings.hooks.json` | modify — tras E-01, D-01, D-04 (mismo archivo que D-04, en serie): el comando `SessionEnd` resuelve la ruta en núcleo y en host, si ADR-0019 aprueba hooks en el núcleo (D13); si no, `RECORD` y `suspend` manual sigue documentado | medium | `implementer_agent` | ⏳ |

### Wave 6 — Endurecimiento, roles y residuos del 058

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E-02 | `claude/mcp.json` | modify — servidor MCP de GitHub remoto con OAuth (sin token en archivo) | medium | `implementer_agent` | ⏳ |
| E-03 | `.github/workflows/ci.yml` | modify — fijar `actions/checkout`, `actions/setup-python`, `errata-ai/vale-action` por SHA | low | `implementer_agent` | ⏳ |
| F-01 | `docs/decisions/ADR-0020-owner-writer-dispatch.md` | create — C-7: cuándo el owner escribe un artefacto trivial sin dispatch (enmienda `ADR-0017`) | medium | `principal_agent` (owner) / `doc_orchestrator` (writer) | ⏳ |
| F-02 | `config/artifact_registry.json` | modify — tras F-01: si ADR-0020 se aprueba, registra la excepción owner-escribe con la condición que fije el ADR y `python3 scripts/check_role_artifact.py` exit 0; si no se aprueba, `RECORD` sin cambio | medium | `implementer_agent` | ⏳ |
| I-01 | `scripts/check_absolute_paths.py` | modify — `fix(` `KI-058-1`: escanear también el índice y los archivos sin trackear; paired test nuevo `tests/test_check_absolute_paths.py` | low | `implementer_agent` | ⏳ |
| I-02 | `scripts/upstream_outbox.py` | modify — `fix(` `KI-058-4`: `read_text_file` pasa por `read_regular_bytes`, así un FIFO sale 2 en vez de colgarse; paired test con un FIFO en `tests/test_upstream_outbox.py` | low | `implementer_agent` | ⏳ |
| I-03 | `scripts/upstream_outbox.py` | modify — tras I-02: `fix(` `KI-058-5` a: `deltas` sale 2 con un directorio `--rules` inexistente; paired test en `tests/test_upstream_outbox.py` | low | `implementer_agent` | ⏳ |
| I-04 | `scripts/upstream_outbox.py` | modify — tras I-03: `fix(` `KI-058-5` b: `export --out` a un directorio inexistente sale 2 con mensaje en vez de traceback; paired test en `tests/test_upstream_outbox.py` | low | `implementer_agent` | ⏳ |
| I-05 | `scripts/upstream_outbox.py` | modify — tras I-04: `fix(` `KI-058-5` c: `PIN_PATTERN` solo acepta dígitos ASCII (`[0-9]`); paired test con dígitos no ASCII en `tests/test_upstream_outbox.py` | low | `implementer_agent` | ⏳ |
| I-06 | `hooks/on_commit.py` | modify — `fix(` `KI-058-5` d: un asunto `FIX:` en mayúsculas se trata como `fix(`; paired test en `tests/test_on_commit.py` | low | `implementer_agent` | ⏳ |
| I-07 | `scripts/check_fix_reproduces.py` | modify — `fix(` `KI-058-5` d: el mismo caso que I-06 en la reproducción; paired test en `tests/test_check_fix_reproduces.py` | low | `implementer_agent` | ⏳ |

### Cierre

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Z-01 | `CHANGELOG.md` | modify — entrada `[Unreleased]` del sprint; cita `host:F-116-N1` y `host:F-116-N2` (`agents.md §4 feedback_upstream`, cierre) | low | `doc_orchestrator` | ⏳ |
| Z-02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — cerrar o re-enrutar `KI-056-1`, `KI-056-6`, `KI-057-1`, `KI-057-2`, `KI-058-1`, `KI-058-3`, `KI-058-4`, `KI-058-5`; `KI-058-2` y los condicionados de Out of scope quedan con su condición de desbloqueo; nuevos `KI-059-n`, incluido uno para los puntos 3-5 de la propuesta E (P11) | low | `doc_orchestrator` | ⏳ |

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | — |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Cálculo de lotes paralelos (`check_task_scope.py`, G-01) | script | `workflows/pipeline_workflow.md` Phase 6 (G-02) |
| Presupuesto por unidad y puntos de suspend (`check_task_scope.py` con `config/unit_cost_estimates.json`, H-02) | script | `workflows/pipeline_workflow.md` Phase 4.3 (A-04); recalibración de la tabla: paso advisory en `workflows/close_workflow.md` (H-03) |
| Medición en sesión de la cota §3.1 (`session_cost.py --bound` o lo que fije ADR-0018) | script | `workflows/pipeline_workflow.md` Phase 6 (A-04) |
| Recuento de autorizaciones (`scripts/prompt_count.py`) | script | advisory en `workflows/close_workflow.md` (B-07); `PROMPT_MEASUREMENT.md` registra la medida, no la invoca |
| Comprobación del manifiesto sin escritura (`generate_manifest.py --check`) | script | `Makefile` `verify` (B-05) |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 52 | Count of rows in Work tables |
| Subagents dispatched | lotes de hasta 4 en paralelo desde la wave 3 (D11), más QA + Tester por wave | `agent_assignment.md` |
| Prior session ratio | **9.2×** (ciclo 2; ciclo 1 4.6×) — supera soft (5×). Coste restante declarado: 52 unidades en 6 waves más cierre, una wave por sesión, `suspend` entre waves | `python3 scripts/session_cost.py --from-anchor --json` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues — they are not observational-only once a measurable Claude
transcript exists for this tool.

---

## Tests

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| `tests/test_session_cost.py`: un ciclo cuyo primer turno tiene `cache_read` 0 y `cache_creation` > 0 devuelve `ratio` numérico | **Yes** — this is the defect | `unverified`: el test no existe todavía (A-01). Defecto observado en datos: `sessions=33 first_turn_zero_cycle1=11`, exit 0 |
| `check_task_scope.py` imprime lotes que respetan `Depends on` y archivos disjuntos | **Yes** — la columna no existe | `unverified`: funcionalidad nueva (G-01) |
| `install.py` en modo núcleo escribe `sandbox.autoAllowBashIfSandboxed: true` | **Yes** — `install_nucleus_bridge` no instala sandbox | `unverified`: se mide al abrir la wave 2 con un fixture de núcleo |
| `check_task_scope.py` sale 2 cuando el `Est. cost` acumulado supera soft sin un `Suspend after: yes` previo | **Yes** — las columnas no existen | `unverified`: funcionalidad nueva (H-02) |
| `session_cost.py --bound` imprime `HARD` y sale 0 en un ciclo de 16× | **Yes** — el flag no existe | `unverified`: flag nuevo (A-02) |
| `scripts/py_compile_tree.py` no crea `__pycache__` | **Yes** — escribe `.pyc` | `unverified`: se mide al abrir la wave 4 con `find` antes/después |
| `tests/test_session_end_hook.py`: `SessionEnd` de otra sesión no suspende | **Yes** según `KI-057-2` | `unverified`: `KI-057-2` dice "not reproducible as specified (W13)"; E-01 reproduce primero o se cierra como `RECORD` |
| `tests/test_session_state.py`: `suspend` con sprint sellado y sesión `IN_PROGRESS` libera el lock (E-01c) | **Yes** — deja el lock tomado | `unverified`: observado en Phase 1 (el boot siguiente salió 2 y exigió `--takeover`); el test se escribe y se ve fallar al abrir la wave 2 |
| `tests/test_mass_standardizer.py`: `generate_manifest.py --check` sale 2 ante un manifiesto distinto y no reescribe el archivo (B-04) | **Yes** — el flag no existe | `grep -c -- '--check' skills/mass-standardizer/scripts/generate_manifest.py` → 0, exit 1 |
| Paired tests de I-01..I-07 (`KI-058-1`, `KI-058-4`, `KI-058-5` a-d) | **Yes** — cada uno es un defecto registrado | `unverified`: cada test se escribe y se ve fallar en el padre al abrir la wave 6; `scripts/check_fix_reproduces.py` lo exige en Gate 1 |
| Suite completa `make verify` | **No** — regresión a proteger | `make verify` → exit 0 en `08c669c` |

---

## Verification

| Command | Expected | Dry run | Positive control |
| :--- | :--- | :--- | :--- |
| `wc -c agents.md` | ≤ 20000 | exit 0; 53907 | la propia corrida de base es el control positivo |
| `grep -n "^model:" agents/qa_agent.md` | `model: sonnet` | exit 0; `model: opus` | la propia corrida de base es el control positivo |
| `python3 -I scripts/session_cost.py --from-anchor --json` | exit 0, todos los `ratio` numéricos | exit 0; ratios 4.6 y 9.2 (esta sesión no tiene ciclo frío) | bucle sobre los 33 transcripts: 11 con `first_turn` 0 |
| `grep -rn -e session_cost -e session_probe hooks/` | sin salida (D2: el invocador es un workflow, no un hook) | exit 1, sin salida | `grep -n -e session_cost -e session_probe scripts/session_start.py` → líneas 444, 679, exit 0 |
| `grep -n "isolation" workflows/pipeline_workflow.md` | una línea en Phase 6 (G-02) | exit 1 (aún no existe) | n/a: la salida esperada no es vacía |
| `make verify` | exit 0 | exit 0 en `08c669c` | n/a |
| `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | exit 0 | exit 0 en `08c669c`; 1527 passed | n/a |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md` | exit 0 | run at close: se ejecuta sobre el borrador antes de Phase 5 | n/a |
| `grep -n "@v[0-9]" .github/workflows/ci.yml` | sin salida tras E-03 | exit 0, líneas 24, 28, 39 | la propia corrida de base es el control positivo |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | recortado a índice de reglas (D10); `RA-09`, `graph_sync` según ADR-0019 |
| `rules/code_craft.md`, `rules/project_topology.md`, `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | reciben el detalle movido desde `agents.md`; §4 de `project_topology.md` según ADR-0019 |
| `agents/qa_agent.md`, `config/model_tiers.json` | `qa_agent` a `sonnet` / tier `author` (prueba D9) |
| `workflows/pipeline_workflow.md` | Phase 6: lotes paralelos (D11) y paso de medición |
| `rules/token_economy.md` | §3.1 unidad y invocador |
| `docs/guides/RULE_PRECEDENTS_GUIDE.md` | nuevo: historia y precedentes de las filas de `agents.md` sin otro destino (A-13) |
| `docs/decisions/ADR-0021-qa-agent-tier-trial.md`, `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | nuevo ADR de la prueba D9 y su cita en la guía (A-14) |
| `rules/skills_and_integrations.md`, `rules/qa_and_testing.md`, `config/rule_triggers.json` | reciben reglas de una tarea concreta desde la guía de precedentes (A-15, A-16, A-17) |
| `docs/sprints/059-core-pipeline/TOKEN_ECONOMY_STUDY.md`, `PROMPT_MEASUREMENT.md`, `SANDBOX_ENUMERATION.md` | nuevos |
| `config/unit_cost_estimates.json` | nuevo: tabla de estimación de coste por unidad |
| `docs/decisions/ADR-0018-*`, `ADR-0019-*`, `ADR-0020-*` | nuevos: token economy en sesión, régimen de sandbox, owner/writer |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | triage y estado de `F-116-N1/N2`, `F-055-N1` |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | cierre/re-enrutado de KIs, incluidos `KI-058-1`, `KI-058-4`, `KI-058-5` |
| `CHANGELOG.md` | entrada `[Unreleased]` |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `KI-058-2` (bump de `graphifyy`) | Condicionado: espera a un release upstream con `--include-json` |
| Auditoría de prompts | Sprint 060 completo: depende del recorte de `agents.md` y del resultado de `qa_agent` en `sonnet`, y meterla aquí retrasaría el despliegue del ahorro de la wave 1 a los hosts |
| Bloquear en hard (exit 2) | Cuando la calibración de §3.1 tenga n > 1 (D3) |
| `install.py` instala los comandos `agents:*` en todo host sin preguntar, así que el borrado de Phase 1 se revierte al reinstalar | Pregunta del estudio A-00 (comandos opt-in por host); si no se decide, `KI-059-n` |
| Más de 4 subagentes en paralelo | Se reevalúa con la medición de integración de la wave 3; el límite vive en `/config` |

---

## Abort criterion

1. Si C-01 mide un punto de entrada sin sandbox escribible por el agente que no
   estaba en `SANDBOX_ENUMERATION.md` (056), la wave 5 no cambia `RA-09`/`RA-19` ni
   instala hooks en el núcleo: la fila pasa a `KI-059-n` y el resto sigue. Si ese
   punto lo abre el bloque `sandbox` que instaló B-06 (adelantado a la wave 2 antes
   de esta medición), B-06 se revierte en el mismo paso.
2. Si B-02 no puede contar autorizaciones desde transcripts, ninguna regla se relaja
   por "menos autorizaciones" y el instrumento se re-planifica con el humano.
3. Si el debate de A-06 no cierra una decisión en la sesión de la wave 3, A-02..A-04
   se implementan con D2/D3 tal como están y el método pasa a `KI-059-n`.
4. Si un gate posterior encuentra un defecto que QA Gate 1 en `sonnet` debía haber
   visto, A-08 se revierte (`qa_agent` vuelve a `opus`) y se registra en
   `SPRINT_LOG.md`.
5. Si con B-06 aplicado `make verify` o un paso de Phase 6 falla en el núcleo por el
   sandbox, B-06 se revierte y el bloqueo medido pasa a C-01.
6. Si integrar un lote paralelo produce un conflicto de git, ese lote se re-ejecuta
   en serie y G-02 se revisa antes del siguiente lote.
7. Si A-00 no puede atribuir coste a unidades (los transcripts no permiten cruzar
   turnos con commits), H-01 arranca con estimaciones marcadas `unmeasured`,
   H-02 solo avisa (exit 0) y la calibración pasa a `KI-059-n`.
8. Más de 3 `REJECTED` consecutivos del mismo bloque → `remediation_workflow.md`.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal («Aprobado», Phase 5, session `b1572a48`) |
| **Date** | 2026-11-02 |
| **Plan commit at approval** | `65c86d3` (this block and the P11/Z-02 routing of proposal E were added after approval, as recorded) |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
