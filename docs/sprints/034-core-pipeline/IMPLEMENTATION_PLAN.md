# Implementation Plan: Sprint 034 — close, graph, gates, Cursor agents

**Canonical path**: `docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/034` (existe; Lock 1 del plan está comiteado) · **Base**: `main` en `76ae9b3` (`v4.16.0`)
**Status**: `EXECUTING` — Phase 5 autorizada por Gustavo 2026-08-26 («ok, comenzamos»). DAG: `A → B → P → I → K → J → N`.

> Redactado en Phase 1 (Planning) por `principal_agent`. Español permitido aquí
> (`agents.md §1 user_chat`). El resto de artefactos del pipeline sigue en inglés.
>
> Este archivo es la superficie de reanudación de la siguiente sesión. **No**
> tratar un resumen cortés como Phase 5 OK. Las decisiones humanas abiertas van
> primero.

---

## Context

Sprint de protocolo sobre el núcleo Cursor (026–033 ya migraron; 034 no
promueve author). El problema: close no encadena deploy, el graph probe miente
por mtime, `/start` vuelca workflows, el mapa de tiers no se aplica en Task, el
gate Cursor sigue `null`, y varios gates de artefacto aprobaban ausencia.
**Hecho cuando 034 cierre:** tracks A, B, I, K, J, N, P ✅, close+deploy publica un
tag; los **hosts** pueden pinchar ese tag y volver a trabajar con el submódulo.
Cada `/start` posterior pingea origin y pincha el tag `v*` más nuevo.
**No** hecho en 034: C/E/H/F (035), M/L (036), G (037), trial de familia
(**038**), abaratar `gate`, ni `ruff` en `verify`.

Cifras vigentes (reproducir en Evidence): `start_workflow.md` ≈ 18 794 B;
`cursor.author` = `grok-4.5`; `cursor.gate.model` = `null`; pytest núcleo
`553 passed` fuera de sandbox; 14 perfiles en `agents/` y en `.cursor/agents/`
(worktree N, gitignored).

---

## Open decisions (reanudar aquí)

Las decisiones de diseño de esta tabla están **cerradas** (O1–O3, O5, O6). O4
pertenece a **038**. Phase 5 **autorizada** 2026-08-26. Lo que queda es ejecutar
las filas ⏳ de 034.

| # | Decisión | Opciones sobre la mesa | Estado / bloqueado hasta |
| :--- | :--- | :--- | :--- |
| O1 | Canal del prior público | (A) API de Artificial Analysis · (B) vals.ai · (C) mirrors · (D) bake-off local | **CERRADA: el benchmark sale del plan.** Humano, 2026-08-25. No es decisión nueva — `docs/roadmaps/core/pipeline/021-030-program-queue.md:1095-1098` ya lo había rechazado con esta razón. Track F pierde F1/F2/F4/F5; F5 nunca llega a existir |
| O2 | Objetivo de la promoción | Humano: **una combinación** | **CERRADA**. Formalizada en D12 como coste mínimo bajo suelo de calidad. Ventana de línea base: **2 sprints** (032, 033), propuesta por el Principal por ser la única que funciona desde el primer día y **confirmada por el humano el 2026-08-25** |
| O3 | Partición trial vs protocolo | (a) ningún family-trial en el protocolo · (b) bake-off dentro de 034 | **CERRADA en (a)**. El trial no mezcla instrumento y medido. Destino del trial: **038** (tras ledger 037). O6 parte el protocolo en varios sprints |
| O4 | Primer candidato de family-trial | Solo tras primera fila de ledger (037) + normas D6 | **038**. Escribir `cursor.author` |
| O5 | Hallazgos nuevos del censo 026–033 | (a) entran como unidades al momento · (b) se clasifican y se reordenan al final | **CERRADA en (b)**. Track L vive en **036**; el triaje es al close de 036 |
| O6 | Cadencia submódulo / cuántos sprints | Un 034 de 55 unidades vs varios closes que pinchan hosts | **CERRADA 2026-08-26 (humano):** cada close actualiza el submódulo. **Cinco** sprints (034–038). Hosts reanudan **tras el deploy de 034**. `/start` auto-pincha tags `v*` (Track P) |

**Postura humana (2026-08-25, chat):** rechaza el prior como «foto muerta» y
después **elimina el benchmark del plan**. Quiere normas de promoción
(calidad/coste según necesidad), no un veto por marca. Elige el **ledger**
(Track G), el arreglo del espejo de `propose_tiers` (E5) y fijar la celda `gate`
por techo estructural (Track H). Misma sesión, más tarde: auditar **toda la
ejecución desde la migración a Cursor** (026–033) para ver errores de
ejecución — D18 / Track L. Los «errores comentados» de la suite pytest se
midieron otra vez: eran el sandbox, no el árbol (CE-5). Último: el fallback
de `agent_orchestrator` / `skill_architect` (buscar → API/web → crear) no se
ha disparado nunca y el grueso es host-submódulo — D19 / Track M. Misma
petición, censo de los 14 perfiles con profundidad en qa / tester /
principal / orchestrator (fases de gate).

**Postura humana (2026-08-26):** reordenar por urgencia de **hosts**. Cada
close debe pinchar el submódulo. Definir cuántos sprints y desde cuál se
vuelve a trabajar en hosts — O6. Misma sesión: `/start` debe **pingear**
origin y **actualizar el submódulo automáticamente** si el pin no está al día
(Track P; revoca la espera de autorización en `lightweight_sync`).

**Falla de postura del Principal (esta sesión):** dos, ambas registradas.
Primero empujó hacia Phase 3 / «¿OK?» mientras fuente y objetivo del prior
seguían abiertos. Segundo, y más grave: dedicó la mitad del debate a diseñar un
canal de prior público que **el program queue ya había rechazado por escrito**
(`021-030-program-queue.md:1095-1098`), sin haberlo leído. El plan de un sprint
del núcleo debe partir del roadmap del programa; no lo hizo.

---

## Programa: 5 sprints, submódulo desde 034 deploy

Los hosts pinchan `.agents` a un **tag**. Hasta que 034 no haga close+deploy
siguen en `v4.16.0` (033). El trabajo en `ai-sprint/034` no actualiza un
host. **Reanudar hosts = primer tag posterior a 033.**

| Orden | Sprint | Tracks (unidades) | Por qué este primero | ¿Hosts pinchan y siguen? |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **034** (este plan) | A B I K J N P (**27**: 8 ya ✅, 6 N worktree, 3 P worktree, 10 ⏳) | **A** publica. **P** hace que el siguiente `/start` pinche solo. **N** despacha los 14 perfiles. **I/K** cierran gates de ausencia. **B** deja de mentir el grafo. **J** corrige la constitución | **Sí: primer re-enable** (pin manual a 034). Desde 035, `/start` auto-pincha |
| 2 | **035** | C E H F (**17**) | Cada sesión host: `/start` barato + Task aplica el mapa + celda `gate` | Sí, segundo pin |
| 3 | **036** | M L (**12**) | Forja host-submódulo + censo 026–033 | Sí |
| 4 | **037** | G (**2**) | Ledger de gate rounds; insumo de O4 | Sí |
| 5 | **038** | family-trial (plan propio) | O3/O4: no mezclar instrumento y author. Tras 037 | Sí |

DAG **dentro de 034:** `A → B → P → I → K → J → N` (A primero: sin deploy el resto no llega a hosts). P va en este tag para que 035+ se pinchen solos. N emite los 14 perfiles *tal cual están*; M7–M9 en 036 corrige instructing de gate. Dependencias **entre** sprints: C5 y H2 en 035 tras E6; L3 en 036 tras C5 de 035; M5 en 036 tras E3 de 035.

El ID **035 deja de significar** family-trial; ese trabajo es **038**.

---

## Evidence snapshot (2026-08-25, sesión `20260825T182539Z-96538`)

Reproducir cada fila antes de tratarla como vigente en una sesión posterior.

| Afirmación | Resultado | Reproducir |
| :--- | :--- | :--- |
| Close no ejecuta deploy solo | Instrucción + escape hatch; logs 031–033 dicen «awaiting `/agents:deployment`» | `rg -n 'awaiting.*deployment' docs/sprints/03{1,2,3}-core-pipeline/SPRINT_LOG.md` |
| Grafo «behind» tras close | El probe usa **mtime vs `git log %ct`**, ignora `built_at_commit`. Grafo `adbe0b8`; HEAD `76ae9b3` | `python3 scripts/session_probe.py`; `python3 -c "import json; print(json.load(open('graphify-out/graph.json')).get('built_at_commit'))"` |
| `/start` es caro en tokens | `workflows/start_workflow.md` ≈ **18 794 B**, 32 líneas, línea máx. ≈ 2 569 | `wc -c workflows/start_workflow.md` |
| Chat ≠ mapa | Chat aplicado fue `grok-4.6`; mapa `cursor.author` = `grok-4.5` / `high`; `cursor.gate.model` = `null`; mechanical = `composer-2.5` | `make cursor-tiers`; `python3 -c "import json; t=json.load(open('config/model_tiers.json'))['tiers']; print(t['author']['cursor'], t['mechanical']['cursor'], t['gate']['cursor'])"` |
| Tamaño del catálogo | **35** modelos agent-capable tras hard filters | `make cursor-tiers` |
| **El benchmark ya estaba rechazado** | El program queue dice que el catálogo lleva capacidades, «not quality or price», y que los benchmarks miden capacidad genérica, no *«passes this framework's gates on this code»*. Declara una única señal válida: `cost per accepted unit = tokens spent ÷ work that passed the gates` | `rg -n 'Benchmarks were rejected' docs/roadmaps/core/pipeline/021-030-program-queue.md` |
| Benchmark público, medición única del 2026-08-25 | Frontera saturada: clúster ≥95% en SWE-Verified con ~3 puntos entre el 1.º y el 7.º; y los nombres no son slugs Cursor (GLM-**5.3** en el agregador ≠ `glm-5.2` en el catálogo). Se conserva como razón documentada del descarte, **no** como mecanismo consultable | Medición histórica; no reproducible sin red y ya no se usa |
| Historial Double-Gate aquí | 032/033: QA+Tester ronda 1 `APPROVED` bajo trial Grok author / sprint implementer | `docs/sprints/032-core-pipeline/SPRINT_LOG.md`, `033` |
| Contador de coste Cursor | `session_cost.py --from-anchor` → `measurable: false` | `python3 scripts/session_cost.py --from-anchor --json` |
| Upstream open set | Vacío tras 033 cerrar `F-021-A2` | Tablas de estado en `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` |
| **`propose_tiers` es un espejo, no un selector** | `author = [fila cuyo name == applied_model_id]`. El tier author se propone a sí mismo: la herramienta **nunca** puede sugerir un cambio, solo ratificar el statu quo | `scripts/audit_cursor_models.py` líneas 179–184 |
| **`gate` es inalcanzable por construcción** | `load_proven_families()` hace `return set()` fijo, y sin familias probadas el bucle de `gate` no emite ninguna fila. Depende de un medidor que en Cursor devuelve `measurable: false` — bucle cerrado sin salida | `scripts/audit_cursor_models.py` líneas 136–143 y 188–198 |
| **`mechanical` se elige por corte arbitrario** | `[row for row in rows if row["depth"] == "no"][:5]` — los primeros cinco sin palanca de profundidad, sin base de coste ni de calidad | `scripts/audit_cursor_models.py` línea 186 |
| **El medidor está ciego al chat** | La sesión corre en Claude Opus 5 y la herramienta reporta `grok-4.6`: lee `applicationOpenModelAppliedConfig`, que un override por chat no escribe | `python3 scripts/audit_cursor_models.py \| head -3` |
| **Los gate rounds YA son parseables** | `SPRINT_LOG.md` de 033 lleva tabla `\| Gate \| Round \| Verdict \| Class \| Notes \|`, y `check_gate_log.py` ya tiene el parser (`gate_tables`) | `rg -n 'Gate .*Round .*Verdict' docs/sprints/033-core-pipeline/SPRINT_LOG.md` |
| **`task_scope.md` es versionado y lleva Model/Effort** | 033 tiene `task_scope.md` en el directorio de sprint con cabecera `# \| File \| Operation \| Risk \| Assignee \| Model \| Effort \| Status`; `check_task_scope.py` ya la parsea | `rg -n 'Model .*Effort' docs/sprints/033-core-pipeline/task_scope.md` |
| **`check_role_artifact.py` aprueba un directorio vacío** | **Histórico (pre-K1, 2026-08-25).** Tras `9e8c0d3`: `--role rule_validator` sobre dir vacío → exit `2` (`missing: task_scope.md`) | `python3 scripts/check_role_artifact.py --role rule_validator --sprint-dir <dir-vacío>` |
| **Ningún rol de gate deja artefacto requerido** | **Histórico (pre-K2).** `gate_evidence` está en `config/artifact_registry.json`; QA/Tester sin fila de gate en `SPRINT_LOG.md` → exit `2` | `python3 -c "import json; print(json.load(open('config/artifact_registry.json')).get('gate_evidence'))"` |
| **El único invocador automático es ciego en Cursor** | `check_role_artifact.py --from-hook` cuelga de `SubagentStop` en `claude/settings.hooks.json:115`, y `start_workflow.md:27` dice literalmente «**Cursor does not read that file**» | `rg -n 'check_role_artifact' claude/settings.hooks.json workflows/start_workflow.md` |
| **Era Cursor = sprints 026–033** | Los ocho `SPRINT_LOG.md` declaran `session_tool: cursor` y `delegation_mode: sequential`. 026 es la Puerta de Migración (`M1`–`M7` PASSED) | `rg -l 'delegation_mode: sequential' docs/sprints/02{6,7,8,9}-core-pipeline/SPRINT_LOG.md docs/sprints/03{0,1,2,3}-core-pipeline/SPRINT_LOG.md` |
| **La suite pytest del núcleo está verde** | `553 passed` fuera del sandbox. Lo que se midió antes como `20 failed, 56 errors` era `git init` denegado por el sandbox de Cursor, no un test rojo | `./venv_skillopt/bin/python3 -m pytest tests/ -q` con permisos de git; repetir *dentro* del sandbox y comparar |
| **Tester de 033 aprobó un subconjunto** | `pytest tests/test_implementer_role.py` 4 passed; el `make verify` de esa sesión citó 543. El Double-Gate funcional no corrió la suite que el estructural invocó | `rg -n 'test_implementer_role' docs/sprints/033-core-pipeline/SPRINT_LOG.md` |
| **`ruff check .` sigue fuera de `make verify`** | 177 errores hoy; 032 y 033 lo dejaron como exclusión de migración | `./venv_skillopt/bin/python3 -m ruff check . --statistics \| tail -3` |
| **El fallback de forja no tiene tests** | 0 coincidencias de `forge_destination`/`agent_creation`/`skill_search` en `tests/`. El único host-submódulo es `tests/test_installer.sh` (instalador, no Phase 4.1/4.2) | `rg -n 'forge_destination|agent_creation|skill_search' tests/` |
| **P2/P3/P4 de skills no se ejecutaron en 021–033** | «No skill was forged» salvo 030 (cuerpo de un skill ya existente). `autoskills-3rd` «not escalated». Ningún `skill_assignment.md` cita `skills.sh` | `rg -n 'No skill was forged|not escalated|skills.sh' docs/sprints/*/skill_assignment.md` |
| **Crear agente por «no hay perfil» no ocurrió** | Solo 033 A1, y era unidad Work (`nucleus:PR`), no fallback | `rg -n 'creates an agent|No unit creates' docs/sprints/*/agent_assignment.md` |
| **`skill.sh` no existe** | El perfil lo nombra; P3 real es `https://skills.sh/` | `find . -name skill.sh; rg -n 'skill.sh' agents/skill_architect.md` |
| **Puente Cursor no instalaba perfiles en `.cursor/agents/`** | **Histórico (pre-N).** Formato: https://cursor.com/docs/subagents. Worktree 2026-08-26: **14** ficheros en `.cursor/agents/` (gitignored). El adaptador emite `name`/`description`/`model: inherit`/`readonly` | `ls .claude/agents \| wc -l`; `ls .cursor/agents \| wc -l` |
| **Task omite `implementer-agent`** | Enum de esta sesión: 13 perfiles núcleo; falta el creado en 033 | Medición de sesión; no hay fichero en repo que liste el enum |
| **`check_task_scope.py` también aprueba la ausencia** | Directorio sin `task_scope.md` → `[OK] … (skip)`, exit `0`, pese a que `pipeline_workflow.md:20` advierte que saltarse Phase 4.3 desactiva `jurisdictional_lock` y `no_interference` «while they still appear enforced» | `python3 scripts/check_task_scope.py --sprint-dir /tmp/vacio` |
| **La columna Risk existe y no elige nada** | `check_task_scope.py` lee `Risk` solo para rechazar una fila mechanical de riesgo `high` sin nota; ninguna ruta la usa para *seleccionar* modelo | `scripts/check_task_scope.py` líneas 36 y 141–153 |

**Hecho cuando 034 cierre:** tras `release`, close continúa
`deployment_workflow.md` en el mismo turno (salvo stop explícito / suspend);
el probe de grafo deja de mentir vía mtime; I/K cierran gates que aprobaban
ausencia; J1 retira la cláusula falsa del ancla; N emite `.cursor/agents/` y
la regla de título de chat; `/start` pingea origin y pincha el tag `v*` más
nuevo (`sync_agents_pin.py`). Un tag nuevo deja a los **hosts** pinchar el
submódulo. **No** hecho en 034: briefing de `/start`, aplicar el mapa en
`Task`, celda `gate`, ledger, censo 026–033, forja host, ni family-trial
(035–038).

---

## Design

Los IDs `D1`–`D19` son del debate, no el orden de ejecución. El DAG está en
**Cost**. `D16` aparece antes que `D15` porque se cerró antes en la sesión.

### D1 — Close → deploy es el siguiente protocolo nombrado (no gates fusionados)

`deployment_handoff` ya nombra deploy. Modo de fallo: `commands/close.md` solo
carga close, y la celda permite «wait for deploy now» (camino de 031–033).

Cambio: tras `SESSION LOCKED` + `release` en `ai-sprint/[ID]` sin merge,
`commands/close.md` exige continuar `@workflows/deployment_workflow.md` **en el
mismo turno**. Espera humana solo con stop explícito antes del handoff, o
`SUSPENDED` (`require-released` ya rechaza deploy).

Rechazado: un proceso que encadena `ci_gate.py && gh pr merge` (`RA-13`).
Rechazado: SessionEnd hook de Cursor como cadena (el núcleo no instala hooks).

### D2 — El desajuste del grafo es el comparador, no dos grafos

Close reconstruye temprano; commits posteriores (squash, sello de changelog)
dejan el mtime del JSON más viejo que el `%ct` de HEAD. Start solo aconseja.

Cambio: `probe_graph` usa `built_at_commit` + ancestría; campo ausente → no
afirmar «behind» solo por mtime. Mover `graph_rebuild` a después de
`atomic_commit`. El briefing de start puede ejecutar `make graphify-update`
cuando esté behind (Filter 5: script, no consejo ignorado).

Rechazado: trackear `graphify-out/` (el `graph_stats.json` del sprint es lo
durable).

### D3 — `/start` es un script de briefing, no un ensayo

Las Phases 0–1.5 ya son scripts. El coste es releer ≈18 KB de racional más
docs opcionales de 13 KB / 77 KB.

Cambio: `scripts/session_start.py` orquesta herramientas existentes e imprime
un briefing ≤80 líneas (estado, drift, **conteo** de findings abiertos, chat vs
mapa). `start_workflow.md` pasa a: ejecutar script → leer briefing → Principal.
No cargar `WORKFLOWS_STEP_MAP_GUIDE.md` ni `UPSTREAM_FINDINGS` completo al start.

Rechazado: editar packs always-applied de Vercel `AGENTS.md` (config Cursor del
host, fuera de jurisdicción).

### D4 — Eficiencia = modelo más barato que aún pase Double-Gate

Aplica a `author` y `mechanical` únicamente. El tier `gate` se rige por D13.

| Caso de uso | Tier | Default Cursor hoy | Cómo mejora |
| :--- | :--- | :--- | :--- |
| Scripts / probes deterministas | `mechanical` | `composer-2.5` | Aplicar vía `Task` (dejar de usar Grok del chat) |
| Autoría | `author` | `grok-4.5` / `high` (**incumbente**, no ganador probado) | Siguiente trial de **familia** (**038**), no otra generación Grok |
| QA / Tester / Principal / **debate de planificación** | `gate` | `null` → hereda el picker del humano | Fijar por **techo estructural** en `H2` (D13). Nunca por coste (`ADR-0003`) |
| Más duro que el default del rol | escalation | Columna Model/Effort | `F-026-A2` |

Rechazado: agente selector por tarea (`ADR-0004`). Rechazado: Cursor Auto como
eficiencia del framework. Rechazado: elegir Opus porque el catálogo lo lista.

### D5 — El runtime aplica el mapa (`ADR-0010`, Cursor `Task` + `model:`)

`task_scope` escribe Model/Effort; el chat secuencial ignoraba la columna.
Cursor `Task` ahora acepta slugs `model` (no API Anthropic — la prohibición de
API de `ADR-0007` se mantiene; el contexto «no hay primitiva de subagente»
queda supersedido por ADR-0010).

1. `audit_cursor_models.py --resolve <tier|profile>` → `modelId` + `effort`
   desde `config/model_tiers.json`. Mientras `gate` siga `null` devuelve
   `modelId=session`; tras `H2` devuelve la celda fijada por D13.
2. Unidades mechanical → `Task` con el slug resuelto.
3. Author → padre y/o `Task` con mapa o columna Model escalada.
4. Phase 7 → siempre `Task` con contexto fresco; nunca inventar un slug de gate
   «mejor».
5. `delegation_mode` del padre sigue `sequential`; Task aplica la columna, no
   cambia a fan-out nativo de ocho roles estilo Claude.

El script resuelve; el agente no rankea 35 modelos.

### D6 — Normas de promoción (no veto a Opus/GLM)

«No Opus ni GLM en el mapa *hoy*» es **estado de evidencia** (2026-08-25), no
norma permanente. El mapa cambia cuando un candidato cumple las reglas; el ritmo
de releases lo absorbe el catálogo de Cursor, que ya trae los modelos nuevos con
su slug real, no un ban por marca.

| Norma | Criterio ejecutable |
| :--- | :--- |
| P1 — Necesidad | Default = mapa. Escalación / trial solo si la unidad lo pide (`tier_escalation`) o hay Human OK para family trial |
| P2 — Existe en el catálogo | Candidato debe salir de `make cursor-tiers` por su **slug Cursor** exacto y pasar los filtros duros (`supportsAgent`, `degradationStatus == 0`). Nunca un nombre de marketing: GLM-5.3 del agregador no era `glm-5.2` del catálogo |
| P3 — Objetivo O2 | **Cerrada**: la fórmula está en D12 (dos restricciones duras del vocabulario `ADR-0008`, optimización por coste, desempate por rondas, línea base de 2 sprints). El plan del trial la cita, no la redefine |
| P4 — Medir aquí | Promover a `cursor.author` solo tras Double-Gate en **author** (mismo harness de sprint), con la evidencia leída del **ledger derivado** (D11), no de prosa recordada. Es la única señal que el program queue reconoce |
| P5 — Gate nunca por coste | Un candidato **más barato** no entra en `cursor.gate` sin historial de author (nadie atrapa al revisor). No confundir con fijar la celda en el techo, que no abarata nada y va por D13 / `H1` |
| P6 — Calidad que ahorra | Si en trial el candidato **gasta menos** (tokens/coste o rondas) a calidad de gate ≥ incumbente → **debe** entrar al mapa (Human OK al close del trial). Eso es D4 aplicado, no excepcional |

Estado real de evidencia local, que es la única que estas normas admiten:
`claude-opus-5` y `glm-5.2` tienen **0** rondas de Double-Gate en este repo, y
`grok-4.5` solo tiene historial intra-familia `xai` desde 032. Nadie está
descartado; nadie está medido.

### D7 — Sin prior público: el benchmark queda fuera del plan

El benchmark no entra, y no por una preferencia de esta sesión. El program queue
ya lo había rechazado con la razón exacta que este debate volvió a derivar desde
cero: el catálogo lleva capacidades, «**not quality or price**», y los benchmarks
miden capacidad genérica, no *«passes this framework's gates on this code»*.
Declara además una única señal válida, que es literalmente lo que el ledger de
D11 calcula:

```
cost per accepted unit = tokens spent ÷ work that passed the gates
```

| Lo que se elimina | Por qué |
| :--- | :--- |
| `MODEL_PRIOR_TEMPLATE.md`, `check_model_prior.py`, su test y `refresh_model_prior.py` | Mecanismo entero de un input que el roadmap no reconoce |
| TTL de frescura del prior | No hay prior al que ponerle edad |
| Fuentes externas como criterio | Nombres de marketing no son slugs Cursor; y arriba el bench está saturado, así que no distingue donde más se le pedía |

Lo que **queda** de Track F es `F3`: el ownership de Phase 4.3 en el perfil de
`token_economy_agent`, que no dependía del prior.

Y queda el reconocimiento del límite, también literal del roadmap: **cold
start** — un modelo recién descubierto no tiene historial y no se puede rankear.
La respuesta del roadmap es la misma que D12 y D13 formalizan: se puede probar
sin historial en `author` o `mechanical` «because the gate catches bad output»,
y no en `gate`, «because there nothing catches anything».

Coste de esta corrección de rumbo, registrado: la mitad del debate de esta
sesión se gastó diseñando un canal de prior contra una decisión ya tomada, por
no haber leído el roadmap del programa antes de planificar.

Rechazado: scrape en el camino crítico de `/start` o por fila de `task_scope`
(no determinista; el mismo plan propondría modelos distintos en días distintos).

### D10 — El selector es una función pura de tres entradas

`ADR-0004` prohíbe un **agente** selector: «launching a subagent per task to
pick a model is PROHIBITED». No prohíbe seleccionar. Un selector determinista es
precisamente el «deterministic alternative» que `token_economy_agent`
`burden_of_proof` exige nombrar. Este diseño no supersede ADR-0004: lo cumple.

```
select(rol, riesgo_de_unidad, herramienta) → (model_id, effort)
```

Las tres entradas ya existen y ninguna cuesta una llamada a un modelo:

| Entrada | De dónde sale hoy | Qué aporta |
| :--- | :--- | :--- |
| `rol` | `config/model_tiers.json` `tiers[*].profiles` | Tier por defecto |
| `riesgo_de_unidad` | Columna `Risk` de la tabla Work, ya parseada por `check_task_scope.py` | Escalación declarada sin juicio nuevo |
| `herramienta` | `session_tool` en `docs/active_state.json` | Columna `cursor` vs `claude_code` |

Casos y ahorro esperado:

| Caso | Señal | Tier | Ahorro |
| :--- | :--- | :--- | :--- |
| Tests, `Makefile`, probes deterministas | Risk `low`/`medium`, ruta bajo `tests/` | `mechanical` | Real: hoy corren en el modelo del chat |
| Autoría de workflow, ADR, doc | Rol author, Risk `medium`/`high` | `author` | Moderado |
| QA / Tester / Principal | Phase 7 | `gate` | Ninguno, deliberado (`ADR-0003`) |
| Unidad dura en rol mechanical | Risk `high` + tier `mechanical` | escalación declarada | Negativo, y correcto |

En el Work de este mismo plan, seis unidades (`B2`, `C4`, `E4`, `G2`, `H4`, `I5`) son
tests y hoy correrían sobre el modelo de sesión, el techo del catálogo. No se
declara un porcentaje de ahorro porque el medidor de Cursor devuelve
`measurable: false`; se declara el conteo.

### D11 — El ledger es derivado, no un archivo de estado nuevo

`state_homologation` prohíbe crear archivos de seguimiento de estado fuera de
`docs/active_state.json`. El ledger no lo infringe porque **no se mantiene: se
genera**, igual que `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` lo genera
`scripts/map_workflows.py`. Nadie recuerda anexar nada al cerrar.

Ambas fuentes ya son estructuradas, versionadas y tienen parser escrito:

| Fuente | Forma | Parser existente |
| :--- | :--- | :--- |
| `docs/sprints/*/SPRINT_LOG.md` | Tabla `\| Gate \| Round \| Verdict \| Class \| Notes \|` | `check_gate_log.py` `gate_tables()` |
| `docs/sprints/*/task_scope.md` | Tabla `\| # \| File \| Operation \| Risk \| Assignee \| Model \| Effort \| Status \|` | `check_task_scope.py` |

`scripts/model_ledger.py` hace el **join** de las dos y emite
`docs/audits/MODEL_LEDGER.md` con una fila por sprint: `sprint_id`, `tier`,
`model_id`, `effort`, unidades, rondas de Gate 1 y Gate 2, clases de veredicto.

Eso es el «cost per accepted unit» que `load_proven_families()` lleva esperando
desde que se escribió con `return set()`. Con el ledger, D6-P6 pasa de
aspiración a comprobación, y `gate` deja de ser inalcanzable por construcción.

**Fuera de 034:** que `load_proven_families()` lea el ledger para **abaratar**
`gate`. Eso exige historial de más de un sprint y sigue sujeto a `ADR-0003` y
D6-P5. Fijar la celda por techo estructural es otra pregunta: D13.

### D12 — La función objetivo es por tier, y la cadencia también

«El modelo más barato que aún pase el Double-Gate» (D4) nunca fue una regla
global. Los perfiles del tier `gate` son `qa_agent`, `tester_agent` y
`principal_agent`: revisión adversarial y **planificación**. Optimizar coste ahí
es lo que `ADR-0003` prohíbe por escrito. El ahorro vive en `author` y
`mechanical`, que es donde está el volumen.

**Objetivo de promoción para `author` y `mechanical` (cierra O2).** Elegir el
modelo más barato cuya calidad de gate no se degrade respecto al incumbente:

| Componente | Criterio ejecutable |
| :--- | :--- |
| Restricción dura 1 | Cero `REJECTED` de clase `charter`. Un fallo de fondo descalifica; no se promedia |
| Restricción dura 2 | Rondas `REJECTED` de clase `instructing` ≤ las del incumbente en la línea base |
| No penaliza | `RECORD` / `testifying`: `ADR-0008` lo define como veredicto **completado** que no incrementa el contador de rechazos |
| Optimización | Entre los que cumplen, menor coste |
| Desempate | Menos rondas totales |
| Línea base | Los **2** sprints cerrados más recientes del incumbente (hoy 032 y 033) |

El vocabulario es el de `ADR-0008` y las columnas ya existen en la tabla de gate
de `SPRINT_LOG.md`, así que el ledger de D11 lo evalúa sin campos nuevos.

**Cadencia de trial, distinta por tier.** A un trial por ciclo de release,
recorrer 35 modelos tarda décadas. La salida no es acelerar los trials de
`author`, es reconocer que `mechanical` es un banco de pruebas mucho más barato:
su propio `basis` en `config/model_tiers.json` dice «Deterministic, verifiable
results. A wrong answer fails at the next command».

| Tier | Cadencia | Por qué |
| :--- | :--- | :--- |
| `mechanical` | Cada sprint, rotación libre | El fallo es inmediato, local y no depende de que un revisor lo vea; el ledger crece rápido |
| `author` | Una por ciclo de release | El error es sutil y solo lo detecta un gate |
| `gate` | Nunca por coste | `ADR-0003`; solo se fija por techo (D13) |

La evidencia de `mechanical` es más débil que la de `author` — editar bien un
`Makefile` no predice redactar bien un ADR — pero es local, sobre este harness,
y elimina barato a cualquier candidato que no sepa seguir instrucciones.

### D13 — El tier `gate` se fija por techo estructural, no se selecciona

El fallo de un gate es **invisible por construcción**: un falso verde no emite
señal. No se puede optimizar lo que no se observa, y por eso la pregunta del
gate es distinta en especie, no solo en dirección.

Dos señales locales sí lo miden, y ninguna necesita benchmark:

| Señal | Dónde vive | Qué indica |
| :--- | :--- | :--- |
| Desacuerdo entre gates | Filas `Gate`/`Verdict` separadas de QA y Tester en `SPRINT_LOG.md` | Un candidato que nunca discrepa es un sello de goma. Familias distintas no comparten puntos ciegos |
| Defectos que escaparon | `docs/hotfixes/[H-ID]-[Layer].md` (`RA-03`) | Única verdad de terreno sobre lo que un gate no vio. Lenta y escasa, pero real |

**Prohibida toda afirmación de calidad interfamiliar** (decisión humana
2026-08-25). Una versión anterior de este apartado justificaba la elección del
techo diciendo que «el benchmark está saturado arriba» — apoyándose en la misma
medición que D7 acababa de declarar inadmisible. Era incoherente y queda
retirado. La celda se determina en tres capas, ninguna de las cuales afirma que
una familia sea mejor que otra:

| Capa | Criterio | ¿Necesita evidencia? |
| :--- | :--- | :--- |
| Elegibilidad | `supportsAgent`, `degradationStatus == 0`, palanca de profundidad presente (`effort` / `thinking` / `reasoning`) | No: son campos del catálogo |
| Familia | **Distinta** de la de `author` — modos de fallo no correlacionados | No: es una restricción de diversidad, no un ranking |

**Base epistémica de la regla de diversidad, escrita porque es lo que la hace
sobrevivir sin benchmark.** La regla no supone que una familia sea mejor; supone
que **fallan distinto**, y eso se sigue de tener datos de entrenamiento y
post-entrenamiento distintos. Es un supuesto mucho más barato: no requiere
ranking, no requiere medición externa y no caduca con el siguiente release —a
diferencia de «familia X es la buena en Y», que es la compresión narrativa de
una foto de leaderboard. Es el mismo argumento que hace útil un segundo par de
ojos sin necesidad de saber cuál de los dos revisores es mejor.

Corolario operativo: las **capacidades** (búsqueda web, ventana, palanca de
profundidad, multimodalidad) no se resuelven eligiendo familia sino eligiendo
**agente**, porque las herramientas se declaran en el perfil —
`agents/skill_architect.md:4` tiene `WebSearch, WebFetch`. Confundir capacidad
con aptitud es lo que lleva a elegir modelo por reputación de dominio.
| Peldaño dentro de la familia | El más alto que el proveedor exponga, `effort` al máximo | No: la ordenación intrafamiliar la declara y tarifa el propio proveedor |

Eso es exactamente lo que `gate.claude_code = opus` significa hoy y conviene
decirlo en voz alta: **no** es «Opus supera a GLM», es «dentro de la escalera de
Anthropic, opus es el peldaño alto». Nadie vende su modelo grande como peor que
su pequeño, así que esa ordenación no hay que medirla. La interfamiliar sí, y no
la tenemos: `claude-opus-5` y `glm-5.2` tienen **cero** rondas de Double-Gate
aquí.

**Desempate entre familias elegibles.** Tiene que ser un criterio declarado y no
cualitativo. Propuesto por el Principal y **confirmado por el humano en la
sesión del 2026-08-25**, igual que la ventana de D12: primero la misma familia
que sirve `gate.claude_code`
—continuidad del rol de gate entre herramientas, no superioridad—, y si empata,
mayor ventana de contexto. Ninguno de los dos afirma calidad.

**Posición epistémica, sin adornos.** Optimizamos coste con evidencia y elegimos
calidad sin ella. Lo que lo hace aceptable es la asimetría del error: como el
gate nunca se abarata (`ADR-0003`), una elección equivocada ahí cuesta dinero, no
detección. El modo de fallo es gastar de más, nunca revisar de menos.

**El agujero que esto cierra.** `cursor.gate.model` es `null`, o sea «modelo de
sesión», y el snapshot mide que el instrumento no puede ni ver el modelo de
sesión. Hoy el tier gate es lo que el humano dejó en el picker: un accidente, no
una política. Y `propose_tiers` no puede proponer **ningún** gate — tampoco uno
del techo — porque su condición es `load_proven_families()`, un criterio de
coste. Se colapsaron dos preguntas: *«¿puedo abaratar el gate?»* (necesita
historial; `ADR-0003` dice que no) y *«¿puedo fijarlo en el techo en vez de
heredar el picker?»* (no necesita historial ninguno).

**Conflicto declarado, no esquivado.** `ADR-0003` dice que `cursor.gate.model`
«remains null until proven history exists», aunque su preocupación explícita es
«not inventing a **cheaper** gate cell». Rellenarla con un modelo del techo no
es lo que persigue, pero contradice la letra. Por eso `H1` es un ADR que
supersede esa cláusula concreta, no una edición silenciosa de la celda.

### D14 — Quién asigna agentes: propone el Principal, decide Phase 4.1

**Dueño del árbol `agents/`: `agent_orchestrator`.** Es el único perfil que lo
declara (`agents/agent_orchestrator.md:18` «Exclusive jurisdiction is agent
staffing»; `:23` nombra `.agents/agents/<name>.md` como destino de forja) y la
doctrina ya estaba fijada en `docs/sprints/033-core-pipeline/IMPLEMENTATION_PLAN.md:90`.

**Tres convenciones estaban en circulación para la misma pregunta, y una es
imposible de ejecutar:**

| Convención | Sprints | Estado |
| :--- | :--- | :--- |
| `agent_orchestrator` | 022, 023, 027, 028, 033 | Doctrina declarada |
| El perfil se asigna a sí mismo | 030 (`F2`, `F3`), 031 (`R2`, `R3`) | **Imposible**: `qa_agent`, `tester_agent` y `token_economy_agent` declaran `tools: Read, Glob, Grep, Bash` — sin `Write`. Filas marcadas ✅ con commit |
| `rule_validator` | 034 `F3`, antes de esta corrección | Extrapolación de una cláusula sobre `task_scope.md` |

La segunda no es un asignatario mal escrito: el registro afirma una ejecución
que el perfil nombrado no podía realizar. Eso es lo que va a `H-005`.

**Contradicción de plantilla, no del plan.** `IMPLEMENTATION_PLAN_TEMPLATE.md:42`
pone `Assignee` en la tabla Work y `:7-8` atribuye el documento al
`principal_agent` en Phase 1; pero el staffing es exclusiva de
`agent_orchestrator` en Phase 4.1 (`workflows/pipeline_workflow.md:18`). La
plantilla ordena en Phase 1 lo que Phase 4.1 reserva a otro rol — `agents.md:115`
llama a eso role usurpation. Decisión humana (2026-08-25): la columna del plan
es **propuesta**; Phase 4.1 es la autoridad y puede sobrescribir.

**Trampa medida, que condiciona cómo se implementa.** `work_tables()` empareja
cabeceras por **igualdad exacta de celda**:

```83:83:scripts/check_task_scope.py
            if all(key in header for key in WORK_KEYS):
```

`header` es la lista de celdas, así que una celda `Assignee (proposed)` no
coincide con `"Assignee"`, la tabla deja de reconocerse como tabla Work y el
script imprime `[OK]` — **falso verde, no fallo**. Por eso el renombrado se
limita a la plantilla del Implementation Plan; `task_scope.md` conserva
`Assignee` literal. El script solo lee `task_scope.md`
(`scripts/check_task_scope.py:160`), nunca el plan, así que el renombrado no lo
alcanza — pero la asimetría queda escrita aquí para que nadie la «arregle».

**Reparto propone / escribe, generalizado.** Ya existía para Model/Effort
(`token_economy_agent` propone, `rule_validator` escribe) y para el staffing
(`agent_orchestrator.md:19` prohíbe Model/Effort en `agent_assignment.md`).
`F3` de este plan aplica el mismo patrón: contenido de `token_economy_agent`,
archivo escrito por `agent_orchestrator`.

### D16 — Gate replay: el único banco de pruebas local del tier `gate`

D13 declara medible el desacuerdo entre gates, pero lo dejaba dependiendo de que
ocurriera espontáneamente en un sprint vivo. El replay lo provoca sin arriesgar
nada: **pasar un candidato por el diff de un sprint ya cerrado**.

032 y 033 cerraron con QA y Tester aprobando en ronda 1. Cualquier cosa que un
candidato encuentre ahí es informativa por construcción:

| Resultado del replay | Lectura |
| :--- | :--- |
| Defecto real que el gate original aprobó | Evidencia dura de defecto escapado — la señal que, si no, hay que esperar meses a que aparezca como hotfix |
| Nada | Concuerda con el gate original. Ni prueba ni refuta, pero descarta que sea alarmista |
| Hallazgos que no son defectos | Ruido medible, que es precisamente lo que hay que saber de un revisor |

Propiedades que lo hacen admisible donde un trial normal no lo sería: es
**offline** (trabajo ya aprobado, `main` intacto), su coste está acotado a dos
pasadas de gate por candidato, y no cambia el instrumento y lo medido a la vez
—el defecto que cerró O3 en (a)—, porque el diff es histórico e inmutable.

Lo que **no** hace: demostrar superioridad. Un replay limpio no prueba que el
candidato sea mejor, solo que no es peor en ese diff. Sigue vigente que la
calidad de un gate no es observable (D13).

**Alcance del protocolo:** se documenta en
`docs/guides/MODEL_TIER_TRIAL_GUIDE.md` (unidad `E0`, sprint **035**) — cómo se
selecciona el diff, cómo se registra cada hallazgo y cómo se clasifica con el
vocabulario de `ADR-0008`. La **ejecución** del trial es **038**, coherente con
O3/O4.

### D15 — El perfil declara `tier`; el mapa declara modelo

Pregunta cerrada: **¿qué modelo lleva siempre `principal_agent`?** El tier
`gate`, sin excepción, igual que `qa_agent` y `tester_agent` (`ADR-0003`). El
slug depende de la herramienta:

| Herramienta | Modelo del gate | Estado |
| :--- | :--- | :--- |
| Claude Code | `opus`, `effort: high` | Declarado y coherente: `agents/principal_agent.md:5` y `gate.claude_code` del mapa dicen lo mismo |
| Cursor | `gate.cursor` = `{"model": null, "family": null}` → modelo de sesión | **No declarado.** Lo rellena `H2` |

**El slug no se escribe en el perfil ni en prosa.** Rotan dentro de un mismo
sprint: el mapa dice `grok-4.5` mientras el aplicado medido fue `grok-4.6`. El
perfil lleva `tier:`; el slug vive en una sola celda del mapa.

**Dos fuentes de verdad para Claude, cero para Cursor.** El frontmatter
`model: opus` y `gate.claude_code.model` coinciden hoy y **nada las ata**: si una
cambia sin la otra, divergen en silencio. Del lado Cursor el frontmatter no dice
nada, porque `model:` es un campo del esquema de subagentes de Claude Code y
`opus` no es un slug de Cursor. `H3` cierra el primer caso; el segundo es
correcto por diseño — el mapa es la única fuente.

**Restricción decidible sin el script:** `family` del gate ≠ `family` del author.
El author es `grok-4.5`, familia `xai`, así que el gate **no puede ser de familia
grok**. `effort`: el máximo que el modelo exponga (decisión humana 2026-08-25),
no un literal copiado de la celda de Claude.

**Incidente registrado.** Durante parte de la planificación de este mismo sprint
la sesión corría `grok-4.6` aplicado — el Principal en la misma familia que el
tier author, es decir el que planifica y el que redacta compartiendo puntos
ciegos. Es justo lo que la regla de diversidad de familia existe para impedir, y
pasó en el sprint que la está escribiendo. Al cambiar de herramienta la
restricción se cumplió, pero por accidente: nada la comprobaba. `H2` la convierte
en política y `E6` la hace verificable.

### D8 — Quién rellena Model/Effort: `token_economy_agent`

Sin perfil selector nuevo — el selector es el script de D10. Phase 4.3:

1. `audit_cursor_models.py --resolve <tier>` da el par `(model_id, effort)` por
   defecto de cada rol.
2. `token_economy_agent` **propone** cada Model/Effort aplicando D10: default
   del mapa, más escalación declarada cuando la columna `Risk` de la fila lo
   pide (`tier_escalation`), más los candidatos de trial que permita **la
   cadencia por tier de D12** — no un número fijo: `mechanical` admite rotación
   por sprint, `author` una por ciclo de release, `gate` ninguna hasta que
   exista historial de author.
3. Sin ledger utilizable → mapa y escalaciones declaradas, nada más.
4. `token_economy_agent` no tiene `Write`, así que quien **escribe**
   `task_scope.md` es `rule_validator` — que sí lo tiene
   (`agents/rule_validator.md:4`).
5. Runtime aplica vía D5.

Extiende `tier_ownership` / `tier_escalation`; no anula `no_selector_agent`.

### D9 — Frescura de cada insumo

| Insumo | Cuándo se refresca | Si falta o está viejo |
| :--- | :--- | :--- |
| Ledger (`MODEL_LEDGER.md`) | `make model-ledger`, al cerrar cada sprint | Phase 4.3 usa mapa + escalaciones; ninguna promoción |
| Catálogo Cursor | `make cursor-tiers` en cada Phase 4.3 | Hoy **no pasa nada**: éxito silencioso. Lo arregla E6 |

Quedan **dos** insumos, no tres: O1 eliminó el prior público, así que no hay TTL
que ajustar ni archivo cuya edad vigilar.

**Corrección de esta sesión.** La celda anterior afirmaba que «el propio script
falla si no encuentra la base». Es falso y se comprobó ejecutándolo:
`open_catalogue` devuelve `None` cuando el fichero no existe
(`scripts/audit_cursor_models.py:97`), `main` nunca mira ese `None`
(`scripts/audit_cursor_models.py:268`) y el proceso sale `0`. Un catálogo
ausente era, hasta este párrafo, un verde. Es el mismo patrón que veníamos
persiguiendo todo el sprint —la comprobación existe en la prosa, no en el
código— y esta vez estaba dentro del propio plan que lo persigue.

Prohibido en camino crítico: red por fila de `task_scope`, o dentro de
`session_start.py` sin flag explícito. La cadencia de trials **no se declara
aquí**: la fija D12 por tier, y este apartado solo la referencia para no volver
a tener dos números distintos en dos secciones.

### D17 — La ausencia se aprueba: por qué los gates dejaban pasar trabajo roto

Abierta por el humano el 2026-08-25 al preguntar por qué, si D1–D5 estaban bien
descritas, sus ejecuciones en Cursor fallaban igual. Señaló tres síntomas que no
estaban en ninguna sección: subagentes que no se lanzaban, gates que aprobaban
cosas que no funcionaban, y artefactos que el workflow daba por escritos sin
existir. **No son tres problemas. Son tres caras del mismo defecto**, y los tres
se reproducen con un comando.

**1. El verificador de artefactos compara vocabularios distintos.**
`scripts/check_role_artifact.py:59` filtra con `entry.get("role") != role`, una
comparación literal contra el campo `role` del registro. El registro escribe
`Rule Validator`; el framework entero —`agents.md §6`, la columna `Assignee` de
`task_scope.md`, los nombres de fichero de `agents/`— escribe `rule_validator`.
Cero coincidencias, y cero coincidencias es exit `0` por diseño documentado
(línea 16: «*or none required for the role*»). Medido sobre un directorio vacío:

| Invocación | Resultado |
| :--- | :--- |
| `--role rule_validator` (el nombre que usa el framework) | `✅ required artifacts present`, exit `0` |
| `--role 'Rule Validator'` (el nombre que usa el registro) | `❌ missing: task_scope.md`, exit `2` |

El ejemplo del `Makefile:105` usa `ROLE='Orchestrator'`, Title Case: la única
invocación documentada funciona, y cualquiera que use el vocabulario canónico
del framework no.

**2. Los dos roles del Double-Gate no tienen artefacto requerido.** Los cinco
roles con `required` + `scope: sprint` son `Agent Orchestrator`, `Orchestrator`,
`Principal Agent`, `Rule Validator` y `Skill Architect`. `QA Agent` y
`Tester Agent` **no aparecen**. Aun arreglando el punto 1, un gate que no corrió
y un gate que revisó a fondo son indistinguibles para toda comprobación
automática, porque ninguno debe dejar nada.

**3. En Cursor no hay invocador automático.** El único es `SubagentStop` en
`claude/settings.hooks.json:115`, y `workflows/start_workflow.md:27` dice
literalmente que **Cursor no lee ese fichero**. El sustituto es un
`make role-artifacts` manual — es decir, el mismo comando del punto 1.

El patrón se repite fuera de este script: `check_task_scope.py` sobre un
directorio sin `task_scope.md` imprime `[OK] … (skip)` y sale `0`, mientras
`pipeline_workflow.md:20` ya advierte que saltarse Phase 4.3 desactiva
`jurisdictional_lock` y `no_interference` «while they still appear enforced». Y
`audit_cursor_models.py` sale `0` sin catálogo (D9). Tres scripts distintos,
misma regla implícita: **si el objeto no está, se aprueba**.

**Consecuencia para este sprint, y es seria.** D12 define el objetivo como
«modelo más barato que aún pase el Double-Gate». Si pasar el Double-Gate no es
verificable, D12 optimiza el modelo más barato que **burla** un gate cuya
ejecución nadie puede probar. La línea base que cita —032 y 033 con
`QA+Tester ronda 1 APPROVED`— hereda exactamente la misma duda, y es la línea
base de la que cuelga Track G entero.

Esto reordena una prioridad: medir la calidad de los modelos por veredicto de
gate exige primero que el veredicto signifique algo.

### D18 — Censo de ejecución de la era Cursor (026–033)

Abierta por el humano el 2026-08-25: además de los errores ya en el plan,
auditar **todo lo ejecutado desde la migración a Cursor**, porque los defectos
que esta sesión midió (ausencia que aprueba, asignatario sin `Write`, gate que
no deja rastro) no nacieron en 034 — nacieron mientras el pipeline corría bajo
Cursor en modo secuencial.

**Ventana.** Inclusiva: `docs/sprints/026-core-pipeline/` (Puerta de Migración
`M1`–`M7` PASSED) hasta `docs/sprints/033-core-pipeline/` (último sprint
cerrado). 034 es el auditor, no el sujeto. 021–025 quedan fuera: el asignatario
se llama `lead` y no hay columnas `Model`/`Effort`; no son comparables.

**Objeto.** Error de ejecución = el registro afirma que X corrió o pasó, y el
instrumento dice que X no pudo haber corrido o no midió lo que nombra. No es
«releer los logs a ojo». Lista cerrada de clases; una clase que no tenga
comando de reproducción no entra.

| # | Clase | Cómo se mide | Ya en 034 |
| :--- | :--- | :--- | :--- |
| CE-1 | Asignatario sin `Write`/`Edit` en una operación que muta | `check_task_scope.py --sprint-dir docs/sprints/NNN-core-pipeline` (I4) | H-005: 32 filas en 028–032 |
| CE-2 | Artefacto requerido ausente | `check_role_artifact.py --role <perfil> --sprint-dir …` (K1) | Track K |
| CE-3 | Rol de gate sin fila `Gate` | el mismo comando sobre `qa_agent` / `tester_agent` (K2) | Track K |
| CE-4 | Gate funcional que nombra pytest pero no la suite | `Notes` de la fila Tester contienen `pytest` y no contienen `tests/` como ruta | **nueva**: 033 Tester citó `tests/test_implementer_role.py` (4) frente a `make verify` (543) |
| CE-5 | Medición confundida por el sandbox de Cursor | la misma invocación de pytest, con y sin permiso de `git init` | **nueva, y retracta un falso hallazgo de esta sesión**: 20 failed + 56 errors era `git init` denegado; fuera del sandbox `553 passed` |
| CE-6 | Check que habría fallado en el árbol sellado con los instrumentos de hoy | el script de Track L corre CE-1–CE-4 sobre cada sprint de la ventana y tabula | el propio censo (**036**) |

**Fuera de esta lista a propósito.**

| Tentación | Por qué no es clase de este censo |
| :--- | :--- |
| «Los subagentes no se lanzaban» | 026 `M3` PASSED: `delegation_mode=sequential` es la configuración de la era, no un fallo. Un censo que lo marque como defecto reescribe la decisión de migración |
| `ruff check .` con 177 errores | 032 y 033 lo excluyeron como migración. Reabrirlo aquí mezclaría lint legado con errores de ejecución |
| Reescribir `SPRINT_LOG.md` / `task_scope.md` cerrados | Igual que H-005: el censo documenta; no lava el registro |
| Suite pytest «roja» como unidad de arreglo | **Retirada.** Era CE-5. Meterla como Track de tests habría sido el mismo género de falso verde/rojo que D17 persigue |

**Producto.** `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md`, derivado (D11: no es
un archivo de estado nuevo). Una fila por sprint de la ventana, columnas
CE-1–CE-4, más un bloque CE-5 que registra el protocolo sandbox/no-sandbox.
El script sale `0` siempre: es un censo, no un gate. `make verify` **no** lo
invoca — si lo hiciera, 028–032 volverían rojo el verify del núcleo por
hallazgos históricos que I4 ya no debe aplicar a `--current-sprint`.

**Triaje (O5).** Cada fila del censo se etiqueta `already-in-034` / `fixed` /
`deferred` / `new`. Las `new` no se convierten en unidades hasta el reorden al
final del sprint, que es lo que el humano pidió.

### D19 — Forjar agente y skill es prosa: el fallback nunca se ha podido fallar

Abierta por el humano el 2026-08-25: `agent_orchestrator` y `skill_architect`
tienen capacidad de creación; si no hay perfil deben forjarlo, y si no hay
skill deben buscar (manifiesto → puente local → API/web → crear). Desde que
existen, **no han creado nunca nada por ese fallback**. El grueso de ese
trabajo vive cuando `.agents` es submódulo de un host, no en el núcleo.

**Qué declaran hoy.**

| Rol | Escalera escrita | Dónde |
| :--- | :--- | :--- |
| `agent_orchestrator` | Si un paso no tiene perfil, **MUST** autorar `.md` en el destino de `agent_forge_destination`. Default en host: `.claude/agents/`. Escribir dentro del submódulo desde una sesión host está **PROHIBIDO** (`strict_rule`) | `agents/agent_orchestrator.md` `agent_creation` / `agent_forge_destination` |
| `skill_architect` | P1 manifiesto → P2 `autoskills-3rd` → P3 `https://skills.sh/` → P4 Three-File Standard en `.claude/skills/` (default host) | `rules/skills_and_integrations.md` §1; `workflows/skill_forge_workflow.md` `forge_destination` |

**Qué se ha medido.**

| Afirmación | Resultado |
| :--- | :--- |
| Fallback de agente disparado por «no hay perfil» | **Nunca.** 033 A1 creó `implementer_agent.md` porque era una unidad Work, destino `nucleus:PR`, no porque Phase 4.1 no encontrara asignatario |
| Skill forjado por P4 tras un miss de P3 | **Nunca.** 021–033 dicen «No skill was forged». 030 añadió `scripts/audit_plan.py` a un skill que ya existía (conocimiento → ejecutable), que no es P4 |
| P2 (`autoskills`) corrido | **Nunca.** Todos los `skill_assignment.md` de 026–033 dicen «not escalated» |
| P3 (`skills.sh` o WebSearch) registrado | **Nunca.** Ningún `skill_assignment.md` cita una consulta a esa URL |
| Tests del fallback | **Cero.** `tests/` no menciona `forge_destination`, `agent_creation` ni `skill_search`. `tests/test_installer.sh` finge el host-submódulo y solo cubre `install.sh` |
| El comando que el perfil nombra | `skill.sh` **no existe** en el árbol. P3 real es `https://skills.sh/` más `WebSearch`/`WebFetch` que el perfil ya declara y nadie obliga a usar |

**Por qué el artefacto no basta.** `check_role_artifact.py` (K1) exige que
`agent_assignment.md` y `skill_assignment.md` *existan*. Un archivo que dice
«ningún skill forjado / ningún agente creado» cumple. Es D17 otra vez: la
ausencia del fallback se lee como éxito. Phase 4.2 (`pipeline_workflow.md:19`)
da por hecho «every step has tools resolved» sin pedir el rastro P1–P4.

**Por qué el fixture tiene que ser un host.** `forge_destination` (a) es el
default y es el único legal desde una sesión host. Los sprints 026–033 se
ejecutaron **en el núcleo**, donde crear bajo `agents/` está permitido (033).
Un test que forje en `agents/` del núcleo no cubre el caso que el humano
nombra. El layout es el de `tests/test_installer.sh`: árbol host, `.agents/`
con `gitdir:` pointer, `.claude/agents/` y `.claude/skills/` del host. Desde
ese layout, escribir `.agents/agents/` o `.agents/skills/` es el fallo.

**Qué testea Track M (y qué no).** No lanza un LLM. Fija un chequeo
determinista sobre los dos artefactos y sobre ficheros en disco, con HTTP de
P3 **simulado** (nada de red en `make verify`). Un agente que en Phase 4.1/4.2
omita el fallback falla el chequeo; uno que forje en el destino host pasa.
Forjar un skill o un agente *de verdad* en el núcleo, contra un hueco inventado,
queda fuera: contaminaría el árbol. El fixture de test (M2, **036**) es el hueco.

**Relación con I7.** La plantilla de `agent_assignment.md` ya lleva
`Destination`. D19 añade que si `Operation` es `create` (perfil nuevo), el
fichero nombrado en `Destination` **debe existir** al cerrar Phase 4.1. I7
escribe la forma; M1 la hace fallar cuando el destino está vacío.

**Censo de los 14 perfiles (2026-08-26).** `agents/*.md` menos el ejemplo de
`profiles/`. `check_model_tiers.py` ya exige `model:` + `tier:` alineados con
el mapa (14/14). Eso no es «creación correcta»: no mira herramientas, fase, ni
si el runtime puede despacharlos.

| Perfil | Core/Aux | Fases | `Write`/`Edit` | `model` / `tier` |
| :--- | :--- | :--- | :--- | :--- |
| `principal_agent` | Core | 1, 5, 8 | no (`TodoWrite`) | `opus` / `gate` |
| `qa_agent` | Core | 7 Gate-1 | no | `opus` / `gate` |
| `tester_agent` | Core | 7 Gate-2 | no | `opus` / `gate` |
| `orchestrator` | Core | 3; transcribe 7 | sí | `sonnet` / `author` |
| `agent_orchestrator` | Core | 4.1 | sí | `sonnet` / `author` |
| `skill_architect` | Core | 4.2 | sí | `sonnet` / `author` |
| `rule_validator` | Core | 4.3 | sí | `sonnet` / `author` |
| `devops_agent` | Core | entorno | no | `haiku` / `mechanical` |
| `implementer_agent` | Aux | `scripts/` `hooks/` `tests/` | sí | `sonnet` / `author` |
| `doc_orchestrator` | Aux | docs | sí | `sonnet` / `author` |
| `governance_learner` | Aux | close | sí | `sonnet` / `author` |
| `token_economy_agent` | Aux | 4.3 (propone) | no | `sonnet` / `author` |
| `git_sync_agent` | Aux | git | no | `haiku` / `mechanical` |
| `topology_mapper` | Aux | topología | sí | `haiku` / `mechanical` |

**Mapa de fase interno vs pipeline (pre-019).** Los perfiles numeran
fases como si Approval + Double-Gate fueran un solo «Phase 4» y Assignment
fuera «Phase 2». El pipeline vigente es 1 plan → 2 entorno → 3 roadmap →
4.1–4.3 assignment → **5 Approval** → 6 execution → **7 Quality** → 8 close.
Eso no invalida el frontmatter (`name`/`tools`/`model`/`tier`); es instructing.

| Perfil | Etiqueta en el `.md` | Fase real del pipeline |
| :--- | :--- | :--- |
| `qa_agent` / `tester_agent` | Phase 4 `double_gate_review` | **7** |
| `principal_agent` | Phase 0 `consensus_loop`; Phase 3 `approval_gate`; Phase 4 `execution` | **1**, **5**, **6**. Phase **8** closeout no aparece en el perfil |
| `orchestrator` | Phase 1 `roadmap_drafting`; Phase 2 `definitive_sprints` | **3** (roadmap); `gate_transcription` ya dice Phase 7 |
| `agent_orchestrator` / `skill_architect` / `rule_validator` | Phase 2 | **4.1 / 4.2 / 4.3** |
| `devops_agent` | Workflows start/close, sin número de pipeline | **2** (entorno) |
| Auxiliares (`doc_orchestrator`, `git_sync_agent`, `governance_learner`, `implementer_agent`, `token_economy_agent`, `topology_mapper`) | Phase 0 + dominio | No son filas del pipeline de 8 fases; creación OK |

034 corrige instructing **solo en los perfiles de gate** (M7–M9). El
cluster 4.1–4.3 y el Orchestrator de Phase 3 quedan nombrados aquí; no se
abren unidades extra (O5 / fuera de alcance).

**Profundidad: los que intervienen en fases de gate.**

| Perfil | Qué tiene que hacer | Creación: qué está bien | Creación: qué no |
| :--- | :--- | :--- | :--- |
| `qa_agent` | Emitir Gate-1; no escribir lo que juzga (`F-026-A1`, `ADR-0008`) | `tools:` sin `Write`/`Edit`; `tier: gate`; `verdict_routing` nombra al Orchestrator | El perfil sigue diciendo **Phase 4** `double_gate_review`; el pipeline es Phase 7. La `description` dice «after Definitive Sprints» (Phase 3); el gate corre **después de Phase 6**. Instructing (`F-093-G1`) |
| `tester_agent` | Emitir Gate-2; correr la suite; no crear tests | Igual: read-only + `Bash` + `testing_environment` `:memory:` | Misma etiqueta Phase 4. CE-4: 033 aprobó un subconjunto, no `tests/` |
| `principal_agent` | Phase 1 (plan), Phase 5 (humano OK), Phase 8 (closeout) | `tier: gate`; sin `Write` — el subagente no reescribe el árbol que el gate autoriza | (1) `consensus_loop` **ordena escribir** `IMPLEMENTATION_PLAN.md` y `tools:` no incluye `Write`. (2) `approval_gate` está etiquetado Phase 3 (es **5**). (3) `execution` está etiquetado Phase 4 (es **6**). (4) Phase **8** no existe en el perfil, y el pipeline le asigna `PHASE_REGISTER.md` / `CHANGELOG.md` — otra vez el padre con `Write`, no el subagente. El perfil se crea como si subagente y sesión fueran el mismo runtime |
| `orchestrator` | Transcribir veredictos a `SPRINT_LOG.md` | Tiene `Write`/`Edit` y `gate_transcription`. Sin él el gate emite al vacío | No es emisor. Un test que le dé `APPROVED` como si fuera QA mezcla los dos roles. `roadmap_drafting` sigue en Phase 1 (es **3**) — instructing, no defecto de `tools:` |

**Descubrimiento ≠ fichero.** El formato **existe** y está documentado:
https://cursor.com/docs/subagents — proyecto `.cursor/agents/*.md` (también
lee `.claude/agents/` por compatibilidad). Contrato: `name`, `description`,
`model`, `readonly`, `is_background`. No hay campo `tools:` (eso es Claude).
`.claude/agents/` del núcleo ya tiene los **14** perfiles (incluido
`implementer_agent.md`). `.cursor/agents/` estaba vacío porque
`cursor_adapter.py` no lo escribía. Track N emite el contrato Cursor
(`model: inherit`, `readonly` según Write/Edit) para que Task no dependa del
fallback Claude. El enum de esta sesión (13, sin `implementer-agent`) queda
como evidencia de que el fallback no basta. El comentario de
`config/model_tiers.json` («Cursor has no subagents») sigue siendo falso
respecto a Task — H2/E6 lo retiran al tocar ese archivo.

**Qué añade esto a Track M.** M1–M5 cubren el fallback host. M6–M9 cubren
que un perfil de gate *ya existente* esté bien creado: herramientas, fase
nombrada, y que el censo de los 14 se pinne. No se forja un `qa_agent` nuevo.
Track N es el puente Cursor del mismo censo.

---

## Work

Este plan **ejecuta** solo las filas de 034 (A B I K J N P). Las filas `⏭`
quedan aquí como inventario del programa (un artefacto, Lock 1) y se copian
al `IMPLEMENTATION_PLAN.md` del sprint dueño al abrirlo.

Una fila = un archivo estructural (`jurisdictional_lock`). Un commit atómico
(`RA-08`) puede cubrir **dos filas** cuando el hook `fix(` exige test: la fila
de test dice `commit con Xn`. Varios `modify` del mismo path (E2/E5/E6,
E3/I2/K6/M5, C5 luego L3) son **unidades sucesivas**, no un commit. E3/K6/I2
siguen siendo toques sucesivos del mismo workflow **aunque I2/K6 sean 034 y
E3/M5 vivan en 035/036**.

| Commit compartido | Filas |
| :--- | :--- |
| `fix(` + test | B1+B2, C1+C4, E2+E4, G1+G2, H3+H4, I4+K3+K5, K1+K4, L1+L2, M1+M2, N1+N2, N4+N5, P1+P2 |
| Solo documental/guía del puente | N1 y N6 no se fusionan: N6 es su propio commit |
| Pin-sync + workflow | P3 es su propio commit (mismo path que C2 en 035: toques sucesivos) |

Los assignees son rulesets bajo `delegation_mode: sequential`.

### Track A — close encadena deploy (**034**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `commands/close.md` | modify | medium | `orchestrator` | ✅ `c15b4f5` |
| A2 | `workflows/close_workflow.md` | modify | high | `orchestrator` | ✅ `611da90` |

A1: tras seal + `release`, exigir `@workflows/deployment_workflow.md` en el
mismo turno.
A2: quitar el default «wait for deploy now»; mover `graph_rebuild` tras
`atomic_commit`; `RA-14` sobre redacción invoke/awaiting.

### Track B — verdad del graph probe (**034**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `scripts/session_probe.py` | modify | high | `implementer_agent` | ✅ `c2fc750` |
| B2 | `tests/test_session_probe.py` | create | medium | `implementer_agent` | ✅ `c2fc750` |

B1: `built_at_commit` + ancestría. B2: mtime viejo + campo de commit actual →
sin false behind.

### Track P — ping y auto-pin del submódulo en `/start` (**034**)

O6: cada close publica un tag. `lightweight_sync` **esperaba** autorización
(doctrina 2026-08, analogía RA-10). Humano 2026-08-26: ping + actualizar si
el pin no está al día, **de forma automática**. Solo tags `vX.Y.Z` (producto
de deploy), nunca `main`. Origin inalcanzable → degrada y `/start` sigue.
Árbol `.agents` sucio y atrás → exit `2`, no pisa. Núcleo: no-op.

P3 toca `start_workflow.md` **antes** de C2 (035). C2 no reabre la celda
`lightweight_sync`; solo acorta el resto de la tabla.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/sync_agents_pin.py` | create | high | `implementer_agent` | ✅ `25b48af` |
| P2 | `tests/test_sync_agents_pin.py` | create | medium | `implementer_agent` | ✅ `25b48af` (con P1) |
| P3 | `workflows/start_workflow.md` | modify | high | `orchestrator` | ✅ `06a532a` |

Criterio de hecho: `python3 scripts/sync_agents_pin.py; echo $?` en núcleo es
`0` y imprime `nucleus: skip`. En host, un tag `v*` más nuevo que
`describe --tags --abbrev=0` hace `checkout --detach` de ese tag. `rg -n
'sync_agents_pin.py' workflows/start_workflow.md` ≥1. `rg -n 'await explicit
authorization' workflows/start_workflow.md; echo $?` es `1`.

### Track C — briefing de `/start` (**035**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/session_start.py` | create | high | `implementer_agent` | ⏭ 035 |
| C2 | `workflows/start_workflow.md` | modify | high | `orchestrator` | ⏭ 035 |
| C3 | `commands/start.md` | modify | low | `orchestrator` | ⏭ 035 |
| C4 | `tests/test_session_start.py` | create | medium | `implementer_agent` | ⏭ 035 |
| C5 | `Makefile` | modify | medium | `implementer_agent` | ⏭ 035 |

C1: orquestar scripts existentes; briefing ≤80 líneas; chat vs mapa; conteo de
findings. C2: tabla operativa corta. **No** reabre `lightweight_sync` (P3).
C5 es el **único** primer toque del `Makefile` y va **después de E6**. Añade
tres targets, en este orden, en un solo commit: (1) `session-start`, (2)
`model-ledger` (Track G lo invocará; el target existe antes que G1), (3)
`cursor-tiers` con `--check` (`Makefile:101`). Cablear `--check` antes de
invertir E6 dejaría el guard afirmando que `gate` debe seguir vacío.
L3 (**036**) es el **segundo** toque del mismo archivo (después de C5 en
035): solo añade `cursor-era-audit`, **no** encadenado a `verify`. No hay rama
«si C5 aún no corrió».
Riesgo de C5 `medium`: este target puede tumbar la verificación.
Criterio de hecho C2: `wc -c workflows/start_workflow.md` **&lt; 8 000**.

### Track E — aplicar mapa en runtime (`ADR-0010`) (**035**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E0 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | medium | `doc_orchestrator` | ⏭ 035 |
| E1 | `docs/decisions/ADR-0010-cursor-task-applies-tier-map.md` | create | high | `doc_orchestrator` | ⏭ 035 |
| E2 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | ⏭ 035 |
| E3 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | ⏭ 035 |
| E4 | `tests/test_audit_cursor_models.py` | create | medium | `implementer_agent` | ⏭ 035 |
| E5 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | ⏭ 035 |
| E6 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | ⏭ 035 |

E0 se llamaba `D1` y colisionaba con la sección Design D1; renombrada aquí.
Carga dos cosas, ambas en el mismo archivo: el ledger como evidencia de
promoción, y el **protocolo de gate replay** de D16 — selección del diff
histórico, registro de cada hallazgo y clasificación con el vocabulario de
`ADR-0008`. Solo el protocolo; la ejecución del trial es **038** (O3/O4). Riesgo
sube de `low` a `medium` por ese segundo alcance.
E2: añadir `--resolve mechanical|author|gate|<profile>`, que imprime el par
`(modelId, effort)` de `config/model_tiers.json` y devuelve `session` cuando la
celda es `null`. E3: unidades mechanical de Cursor y gates de Phase 7 vía `Task`
con `model` = salida de `--resolve` (o columna Model si hay escalación).
E1: supersede solo el *contexto* de ADR-0007; la prohibición de API permanece.

E5 corrige el espejo medido en el snapshot: `propose_tiers` deja de devolver el
modelo aplicado como propuesta de `author`. Pasa a devolver la celda vigente del
mapa, marcando aparte el modelo aplicado como `applied` para que el desajuste
chat-vs-mapa sea visible en lugar de convertirse en la propuesta.
Criterio de hecho: con `applicationOpenModelAppliedConfig` en un modelo que no
está en el mapa, `make cursor-tiers` imprime la celda del mapa como propuesta y
el aplicado como discrepancia. E5 va **después** de E2 (mismo archivo, commits
secuenciales; `jurisdictional_lock` se cumple porque no concurren).

E6 separa las dos preguntas que `propose_tiers` colapsó (D13): la propuesta de
`gate` deja de depender de `load_proven_families()` y pasa a derivarse de los
cuatro criterios estructurales — `supportsAgent`, `degradationStatus == 0`,
palanca de profundidad, y `family` distinta de la de `author`.
`load_proven_families()` queda reservada a la pregunta de **abaratar**, que sigue
fuera de 034. Criterio de hecho: `make cursor-tiers` emite al menos una fila en
la tabla `gate`, y ninguna de ellas es de la familia de `author`. E6 va después
de E5.

E6 carga además el guard `--check`, porque hoy **afirma lo contrario de lo que
E6 implementa**: falla cuando `proposals["gate"]` no está vacío, citando un
«Design §D7» que es el D7 de un sprint anterior, no el de este plan
(`scripts/audit_cursor_models.py:269-271`). Tres obligaciones, todas en el
mismo archivo y por tanto en esta unidad:

| Obligación | Estado hoy |
| :--- | :--- |
| Invertir el guard: fallar cuando la tabla `gate` está **vacía** o el catálogo es `None` | Falla cuando está llena — exactamente al revés |
| Borrar la cita `§D7`, que apuntará a la sección equivocada de este plan | Cita cruzada obsoleta entre sprints |
| Cablear `--check` en `make cursor-tiers` | `Makefile:101` invoca el script **sin** el flag, así que el único `return 2` del archivo no lo ejecuta nadie (`RA-16`). **Esta tercera va en C5, no aquí** — `Makefile` es otro archivo y `jurisdictional_lock` es de un archivo por tarea |

Sin esto, E6 entrega un script cuya única aserción contradice su propósito, y la
entrega igual, porque nada la ejecuta.

### Track F — ownership Phase 4.3 (**035**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F3 | `agents/token_economy_agent.md` | modify | medium | `agent_orchestrator` | ⏭ 035 |

Añadir `task_scope_model_proposal` al perfil, con la regla D10 explícita y la
cadencia por tier de D12. En la misma pasada, `tier_ownership` deja de decir
«13 profiles» (033 añadió `implementer_agent`; `check_model_tiers.py` cuenta
14). **No** añadir `prior_ownership`: O1 cerró eliminando el prior. El **contenido** lo propone `token_economy_agent`; el **archivo** lo
escribe `agent_orchestrator`, que es el único perfil con jurisdicción declarada
sobre el árbol `agents/` (`agents/agent_orchestrator.md:18`, `:23`) y la doctrina
que el plan de 033 ya fijó (`docs/sprints/033-core-pipeline/IMPLEMENTATION_PLAN.md:90`).

Corrección registrada de esta misma sesión: el Principal asignó primero `F3` a
`rule_validator` extrapolando la cláusula «`rule_validator` writes the file» de
`tier_escalation`, que habla de `task_scope.md` y no de perfiles de agente. Era
la tercera convención distinta para la misma pregunta (ver D14).

Los IDs `F1`, `F2`, `F4` y `F5` quedan **retirados**, no reasignados: el número
seguiría citado en el debate de esta sesión y reutilizarlo produciría dos
referencias distintas al mismo identificador.

### Track G — ledger derivado de gate rounds (`D11`) (**037**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1 | `scripts/model_ledger.py` | create | high | `implementer_agent` | ⏭ 037 |
| G2 | `tests/test_model_ledger.py` | create | medium | `implementer_agent` | ⏭ 037 |

G1 importa `gate_tables()` de `check_gate_log.py` y el lector de tablas Work de
`check_task_scope.py` — no escribe parsers nuevos. Recorre
`docs/sprints/*/SPRINT_LOG.md` y el `task_scope.md` hermano, y emite
`docs/audits/MODEL_LEDGER.md` con una fila por sprint: `sprint_id`, `tier`,
`model_id`, `effort`, unidades, rondas de Gate 1, rondas de Gate 2, clases de
veredicto. Sin red. Un sprint sin tabla de gate se omite con nota, no rompe.
Criterio de hecho: `make model-ledger` sale `0` y el archivo contiene fila para
032 y 033, los dos sprints con tabla de veredictos.

G2 cubre: sprint sin `SPRINT_LOG.md` (omitido), sprint anterior a 031
(vocabulario histórico, omitido), y sprint con Gate 1 en dos rondas (la segunda
ronda cuenta).

### Track H — fijar el tier `gate` por techo estructural (`D13`) (**035**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| H1 | `docs/decisions/ADR-0011-gate-cell-by-structural-ceiling.md` | create | high | `doc_orchestrator` | ⏭ 035 |
| H2 | `config/model_tiers.json` | modify | high | `rule_validator` | ⏭ 035 |
| H3 | `scripts/verify_references.py` | modify | high | `implementer_agent` | ⏭ 035 |
| H4 | `tests/test_verify_references.py` | modify | medium | `implementer_agent` | ⏭ 035 |

H1 supersede **solo** la cláusula de `ADR-0003` que mantiene
`cursor.gate.model` en `null` hasta que exista historial probado. Deja intacto
lo demás de ese ADR: `qa_agent`, `tester_agent` y `principal_agent` siguen en
`gate` y nadie los baja de tier. Debe registrar por qué el historial no aplica
aquí: es el criterio para **abaratar**, y fijar el techo no abarata nada.

H2 rellena `tiers.gate.cursor` con el `modelId` y la `family` que emita
`make cursor-tiers` tras E6, y el `effort` **máximo que el modelo exponga en
`parameterDefinitions`** — no el literal `high` copiado de la celda de Claude
(decisión humana 2026-08-25). Más una línea en `_comment` con la fecha y el
sprint. No entra ningún precio ni score (`ADR-0005`).
Criterio de hecho: `python3 -c "import json; print(json.load(open('config/model_tiers.json'))['tiers']['gate']['cursor'])"`
imprime un `model` no nulo cuya `family` difiere de la de `author`.

H3 añade el check **(f)** a `verify_references.py`, que ya lleva (a)–(e) y
corre desde `make verify` — así el mecanismo nace con invoker declarado
(`RA-16`) en vez de ser un script nuevo que nadie llama. Para cada
`agents/*.md`: leer `tier:` y `model:` del frontmatter y exigir
`model == model_tiers[tier].claude_code.model`. **Límite explícito:** el check
cubre solo el lado Claude Code, porque `model:` es un campo de ese esquema y no
existe equivalente de Cursor en el perfil (D15). Criterio de hecho: cambiar
`agents/qa_agent.md:5` a `sonnet` hace que `make verify` salga distinto de `0`
citando `(f)`; revertirlo lo devuelve a `0`.

**Vacío de jurisdicción detectado.** Ningún perfil declara el árbol `config/`:
`implementer_agent` cubre `scripts/`, `hooks/` y `tests/`; `devops_agent` no
tiene `Write`; `token_economy_agent` «owns» `config/model_tiers.json` en su
`tier_ownership` pero tampoco tiene `Write`. H2 se asigna a `rule_validator`
porque declara `Write, Edit` y ya escribe artefactos de política
(`agents/rule_validator.md:21`, `agents.md` al close) — **no** por
`tier_escalation`, que habla de `task_scope.md`: esa extrapolación es
exactamente el error que D14 corrige en `F3`, y repetirla aquí habría sido la
misma falta con otro archivo. El vacío se registra como candidato
`feedback_upstream` en lugar de resolverse de tapadillo, y `I4` no lo detecta
porque el check de ruta contra jurisdicción queda fuera de 034 por diseño.

### Track I — asignación verificable (`D14`) (**034**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | medium | `doc_orchestrator` | ✅ `306eba1` |
| I2 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | ✅ `53c596d` |
| I3 | `agents/agent_orchestrator.md` | modify | high | `agent_orchestrator` | ✅ `d3f284d` |
| I4 | `scripts/check_task_scope.py` | modify | high | `implementer_agent` | ✅ `3dc95db` (capacidad; transcripción pendiente de I7) |
| I5 | `tests/test_check_task_scope.py` | modify | medium | `implementer_agent` | ✅ `3dc95db` (con I4/K3/K5) |
| I6 | `docs/hotfixes/H-005-pipeline.md` | create | medium | `doc_orchestrator` | ✅ `18b78ab` |
| I7 | `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | create | medium | `doc_orchestrator` | ✅ `3182b00` |

I1: renombrar la columna a `Assignee (proposed)` **solo en esta plantilla** y
añadir una línea que nombre Phase 4.1 como autoridad. Criterio de hecho: la
plantilla no dice «Assignee» a secas en la tabla Work, y ninguna cabecera de
`task_scope.md` cambia.

I2: en Phase 4.1 declarar que `agent_orchestrator` **puede sobrescribir** la
propuesta del plan, que la fila no está cerrada hasta que lo haga, y **citar
`AGENT_ASSIGNMENT_TEMPLATE.md`** — sin esa cita el `I7` sería una plantilla que
nadie invoca. Va
**después de `E3`**: mismo archivo físico, commits secuenciales, y por eso
comparte asignatario `orchestrator` — dos perfiles distintos sobre un mismo
archivo violarían `jurisdictional_lock` aunque no concurrieran.

Corrección registrada: `I2` decía `governance_learner` citando el precedente de
031. El precedente existe, pero no es único —
`workflows/pipeline_workflow.md` lo han editado `orchestrator` (026 `P1`, 030
`I1`), `doc_orchestrator` (028 `A2`) y `governance_learner` (031 `R4`). Tres
dueños para un archivo, el mismo patrón que D14 encontró en `agents/` y Track H
en `config/`. Se unifica en `orchestrator` por ser el más frecuente y el ya
asignado a `E3`; el hecho de que hicieran falta tres greps para saberlo es la
prueba de que el mapa de jurisdicciones falta.

I3: `staffing_injection` dice hoy «Takes **unassigned** Initial Roadmap»
(`agents/agent_orchestrator.md:21`). Con I1 el roadmap llega pre-propuesto, así
que la regla queda falsa si no se toca. Auto-asignado y **legal**, a diferencia
de las 32 filas de 028–032: este perfil sí declara `Write, Edit`, y hay precedente en
`docs/sprints/028-core-pipeline/IMPLEMENTATION_PLAN.md:125`.

I4: nueva comprobación de **capacidad del asignatario**. Para cada fila con
`Operation` ∈ {`create`, `modify`, `delete`}, resolver el perfil, leer el
frontmatter `tools:` y rechazar con exit `2` si no declara `Write` ni `Edit`.
Criterio de hecho: un `task_scope.md` de prueba con
`agents/qa_agent.md | modify | … | qa_agent` sale `2`; el mismo con
`agent_orchestrator` sale `0`. Habría rechazado `F2`/`F3` de 030, `R2`/`R3` de
031 y la versión inicial de `F3` de este plan.

Tres defectos de la primera redacción de este criterio, corregidos aquí antes de
implementarlo:

| Defecto | Corrección |
| :--- | :--- |
| Resolvía solo `agents/<assignee>.md` | Buscar también en `profiles/*/agents/` — un asignatario legítimo puede vivir en un pack instalado (`profiles/example-project/agents/domain_specialist_example.md` existe hoy), y rechazarlo sería un falso positivo en cualquier host con perfil |
| No normalizaba la forma del nombre | El fichero es `agent_orchestrator.md`, el frontmatter dice `name: agent-orchestrator` y los planes escriben `agent_orchestrator`. Comparar normalizando `-` ↔ `_` |
| No decía qué hacer si el perfil no existe | Perfil inexistente ⇒ exit `2`. Es el caso más probable (nombre mal escrito, perfil renombrado) y el que más silenciosamente rompe la trazabilidad |

`I4` carga además el **check de transcripción**: unir `agent_assignment.md` y
`task_scope.md` por la columna `#` y exigir que el `Assignee` coincida. Es el
mismo script y el mismo archivo, así que no es unidad aparte. Dos detalles que
lo romperían si no se dicen: `agent_assignment.md` nombra su columna `Target`,
no `File` (`docs/sprints/033-core-pipeline/agent_assignment.md:28`), así que el
join va por `#` y no por ruta; y si el archivo no existe, el check **salta** sin
error, igual que ya hace con `task_scope.md` ausente
(`scripts/check_task_scope.py:162`). Precedente de que esta transcripción falla
de verdad: `F-20260825-027`, que obligó a poner la advertencia «never copy
`claude_code` aliases» en Phase 4.3.

**Qué significa el check bajo `delegation_mode: sequential`.** Hoy los assignees
son rulesets aplicados por la sesión padre, que tiene `Write` propio, así que el
`tools:` del perfil no *bloquea* nada. El check no verifica un permiso efectivo:
verifica que **el registro nombre a un perfil que podría haberlo hecho**. Sin
eso, la columna es prosa decorativa — que es exactamente lo que fue de 028 a 032
— y el día que `delegation_mode` pase a `subagent` las mismas filas fallarían de
verdad.

I6: hotfix `RA-03` por los registros que afirman ejecuciones imposibles.
Siguiente ID libre: existen `H-002`, `H-003`, `H-004`. **No** reescribe los logs
cerrados; documenta el defecto y apunta a I4 como remedio estructural.

**Corrección de alcance, medida al ejecutar I4.** El plan decía «030 y 031».
Con el check ya escrito, el recuento real sobre los sprints que llevan columnas
`Model`/`Effort` es de **32 filas en cinco sprints consecutivos, 028 a 032**, y
**033 limpio** — el sprint en que `ADR-0009` creó `implementer_agent`. Dos de
ellas son usurpación de rol en su propia cara: `qa_agent` y `tester_agent`
asignados a `modify` en 031, cuando `ADR-0008` le da a un gate un veredicto que
emitir y ningún fichero que escribir. Y `principal_agent` aparece con cuatro
mutaciones entre 028 y 030. El mismo patrón existe antes —026 tiene 44 filas y
027 tiene 20— pero ambos son anteriores a las columnas `Model`/`Effort` y el
check los salta por diseño; 021 a 025 llaman `lead` al asignatario, un
vocabulario anterior al árbol de perfiles, y no son comparables. Cifras en
`docs/hotfixes/H-005-pipeline.md §1`.

I7 cierra la inversión que destapó la auditoría de esta sesión: al hacer Phase
4.1 la autoridad, el artefacto que manda resultó ser el único de los tres sin
plantilla **ni** validador — ningún script, hook o target del `Makefile`
menciona `agent_assignment.md`. La plantilla codifica la forma más reciente en
uso, `# | Target | Operation | Mode | Assignee | Destination | Ruleset file`
(033), y `RA-06` fija el nombre del archivo. **D19:** si `Operation` es
`create` de un perfil, `Destination` no puede ser `N/A` y el path tiene que
existir al cerrar Phase 4.1 — eso lo hace fallar M1, no esta plantilla sola.

### Track K — hacer falsable que un gate corrió (`D17`) (**034**)

**Va antes de Track G.** Un ledger de veredictos de gate no mide nada mientras
la ejecución del gate no sea verificable.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| K1 | `scripts/check_role_artifact.py` | modify | high | `implementer_agent` | ✅ `9e8c0d3` |
| K2 | `config/artifact_registry.json` | modify | high | `rule_validator` | ✅ `ca203ce` |
| K3 | `scripts/check_task_scope.py` | modify | medium | `implementer_agent` | ✅ `3dc95db` (con I4) |
| K4 | `tests/test_check_role_artifact.py` | modify | medium | `implementer_agent` | ✅ `9e8c0d3` (con K1) |
| K5 | `tests/test_check_task_scope.py` | modify | medium | `implementer_agent` | ✅ `3dc95db` (con I4/K3) |
| K6 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | ⏳ |

**Corrección de granularidad, descubierta al ejecutar.** Separar el arreglo de
su test en dos unidades es **imposible**: `hooks/on_commit.py` rechaza todo
commit `fix(` que no traiga el test que prueba el bug (`rules/code_craft.md §6`),
y lo hizo con K1. Un arreglo y su test son una sola unidad. Afecta a los pares
ya escritos así en este plan: K1+K4 (ya fusionado), K3+K5, B1+B2, C1+C4, E2+E4 y
H3+H4. La tabla los mantiene como filas distintas porque son archivos distintos
—`jurisdictional_lock` sigue siendo por archivo— pero **comparten commit**.

Dos decisiones de implementación que se apartaron de lo escrito arriba, ambas
por evidencia encontrada al ejecutar:

| Escrito en el plan | Ejecutado | Motivo |
| :--- | :--- | :--- |
| K2 añade entradas `artifacts` requeridas para `QA Agent` y `Tester Agent` | K2 añade un bloque `gate_evidence` aparte | `scripts/map_workflows.py:70` construye su matriz como `{filename: phase}`; dos entradas más llamadas `SPRINT_LOG.md` habrían **sobrescrito en silencio** la columna del Orchestrator. Y la existencia del fichero es la aserción equivocada: el log existe desde Phase 3, antes de que ningún gate corra |
| K1 mata también el `if not role: return 0` de la ruta hook | Solo la ruta CLI es estricta; el hook avisa y sigue | Un payload de `SubagentStop` trae tipos de agente arbitrarios, incluidos los propios del runtime. Bloquearlos pararía subagentes que no tienen nada que ver. La intención de K1 se cumple igual: **en Cursor solo existe la ruta CLI** |

**El defecto es más pequeño y más grave de lo que parecía: la normalización ya
existe, y la ruta que Cursor usa no la llama.** `role_from_agent_type()`
(`scripts/check_role_artifact.py:69`) mapea `orchestrator` → `Orchestrator` y
está cubierta por tests. `main_from_hook` la invoca en la línea 127. Pero la
ruta CLI declara `--role` como «Registry role display name`
(`scripts/check_role_artifact.py:148`) y pasa la cadena cruda a la comparación
literal de la línea 59. En Cursor **solo existe la ruta CLI**, porque el hook
vive en `claude/settings.hooks.json` y `workflows/start_workflow.md:27` dice que
Cursor no lee ese fichero.

Y el propio código avisa: el fallback de la línea 76 fabrica `Qa Agent` a partir
de `qa-agent` con el comentario «*may miss registry*». Fabricar un nombre que no
está en el registro produce cero coincidencias, y cero coincidencias es exit
`0`. Es decir, incluso la ruta del hook aprueba en silencio a los dos roles de
gate.

K1: `--role` pasa por `role_from_agent_type()`, y un rol que **no resuelva a una
entrada real del registro** sale `2` en vez de `0` — eso mata a la vez el
fallback fabricador y el `if not role: return 0` de la línea 128. Criterio de
hecho: `--role rule_validator` sobre un directorio vacío pasa de `0` a `2`, y
`--role inventado` también.

K2 registra artefacto requerido para `QA Agent` y `Tester Agent`, hoy los dos
únicos roles del pipeline sin ninguno. El artefacto es `SPRINT_LOG.md`, pero la
existencia del fichero no prueba que el gate corriera, así que K1 exige además
**una fila de gate con ese rol**, reutilizando el parser `gate_tables` de
`scripts/check_gate_log.py` — el mismo que Track G ya reutiliza para el ledger.

K3: el directorio sin `task_scope.md` deja de imprimir `[OK] … (skip)` y sale
`2`. Va **después de I4**, mismo archivo. Con esto `pipeline_workflow.md:20`
deja de describir un agujero («skipping Phase 4.3 disables them while they still
appear enforced») y pasa a describir una comprobación.

K4 y K5 cubren lo que los tests actuales no podían ver: `tests/test_check_role_artifact.py`
invoca siempre en Title Case (`"Orchestrator"`, `"Principal Agent"`), que es la
única forma que funciona. Por eso el defecto sobrevivió con la suite en verde.

K6: Phase 7 declara qué deja cada gate y con qué comando se comprueba. Va
**después de I2**, mismo archivo.

### Track J — la constitución afirma que el ancla de estado no existe (**034**)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| J1 | `AGENTS.md` | modify | high | `rule_validator` | ⏳ |

`AGENTS.md:17` dice literalmente que «in nucleus mode `docs/active_state.json`
does not exist (by design, see `§5`)». Es falso, y lo desmienten tres fuentes
independientes frente a una:

| Fuente | Qué dice |
| :--- | :--- |
| El propio fichero | `docs/active_state.json` existe y contiene la sesión que escribe este plan — `status: IN_PROGRESS`, `role: Principal Agent`, `delegation_mode: sequential`, `session_tool: cursor` |
| `workflows/close_workflow.md` Phase 4 | «**Applies in nucleus mode too** — the nucleus keeps its own local anchor, and a stale anchor or mirror lies to the next session» |
| `workflows/start_workflow.md` Phase 1 | En modo núcleo la Phase 0 corre normal, y la Phase 0 es justo la que reclama y escribe el ancla |

Por qué es `high` y no una errata. La misma `AGENTS.md` ordena en la línea 65
(`anti_amnesia`) releer `active_state.json` una vez por sesión, y en la 108
(`state_anchor`) que el contexto **debe** extraerse de ahí. Así que el
documento manda leer un archivo y, catorce filas antes, dice que ese archivo no
existe. Y §0 declara que en el núcleo **este es el único fichero que una sesión
tiene garantizado leer**: una sesión que se crea la frase salta el ancla y
arranca sin coordenada, que es el fallo que `state_anchor` existe para impedir.

Alcance de J1: corregir esa cláusula. **No** tocar `§5` ni las reglas de
`state_homologation` — solo la afirmación de inexistencia. Asignatario
`rule_validator` porque es quien materialmente escribe en `AGENTS.md` según la
fila `escalation` de `agents/governance_learner.md:18`, que distingue entre
quien destila y quien indexa. Criterio de hecho: `rg -n 'does not exist'
AGENTS.md` no devuelve la cláusula del ancla, y `docs/0_SYSTEM_OVERVIEW.md`
sigue declarado inexistente porque eso sí es cierto (`F-093-N1`).

**Fuera de 034, con razón nombrada:** el check de **ruta contra jurisdicción**
(¿`agents/x.md` cae en el árbol del asignatario?). Exige un mapa de propiedad
legible por máquina que hoy no existe. Tres árboles sin dueño único, medidos en
esta sesión: `agents/` tenía tres convenciones (D14), `config/` no tiene ninguna
(Track H) y `workflows/` acumula tres asignatarios históricos distintos (`I2`).
La doctrina vive en prosa dispersa y en una tabla de un plan de sprint
(`033:90`). Construir ese mapa es un sprint propio; `I4` se limita a la
comprobación de herramientas, que es mecánica y completa por sí sola.

**No en Work de 034:** escribir Opus/GLM en `cursor.author` sin cumplir D6;
**abaratar** `gate` (`ADR-0003` sigue vigente en eso); que
`load_proven_families()` lea el ledger; medidor de tokens de Cursor; el check de
ruta contra jurisdicción.

### Track L — censo de ejecución 026–033 (`D18`) (**036**)

**Corre en 036**, después de que 034 haya cerrado I y K (CE-1–CE-3 son esos
instrumentos). **Antes de G (037)**, porque G toma 032/033 como línea base de
veredictos y CE-4 pregunta si esos veredictos midieron la suite.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| L1 | `scripts/audit_cursor_era.py` | create | high | `implementer_agent` | ⏭ 036 |
| L2 | `tests/test_audit_cursor_era.py` | create | medium | `implementer_agent` | ⏭ 036 (commit con L1) |
| L3 | `Makefile` | modify | medium | `implementer_agent` | ⏭ 036 |

L1 recorre `docs/sprints/{026..033}-core-pipeline/`. Por cada sprint aplica
CE-1–CE-4 con los parsers ya existentes (`check_task_scope.collect_findings`,
`check_role_artifact.missing_for_role` / `missing_gate_row`,
`check_gate_log.gate_tables`) — no escribe parsers nuevos. Emite
`docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` (derivado, como el ledger): una
fila por sprint, columnas CE-1–CE-4 con recuento, y un bloque CE-5 con los dos
números de pytest (sandbox vs no-sandbox) y el comando que los reproduce.
Criterio de hecho: `python3 scripts/audit_cursor_era.py; echo $?` imprime `0`,
el markdown existe, y la fila 028 muestra CE-1 > 0 (H-005 ya lo midió: 3).

Salida `0` siempre. Un censo que saliera `2` porque 028 tiene asignatarios
imposibles reintroduciría el falso rojo sobre historia cerrada, que es lo que
el abort de I4 prohíbe.

L2 cubre: directorio de sprint ausente (fila omitida, no crash); sprint 033
CE-1 = 0 (el único limpio de H-005); Notes de Tester que citan
`tests/test_implementer_role.py` y no `tests/` → CE-4 = 1; y que el markdown no
se considera fuente — borrarlo y re-ejecutar L1 lo regenera.

L3 añade el target `cursor-era-audit` que invoca L1. **No** lo encadena a
`verify`. **Siempre después de C5** (segundo toque del `Makefile`). Criterio
de hecho: `make cursor-era-audit; echo $?` es `0` y
`git diff -- docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` muestra solo el
derivado.

### Track M — fallback de forja falsable en host-submódulo (`D19`) (**036**)

**Corre en 036**, después de I7 en 034 (la plantilla de `agent_assignment.md`
es la forma que M1 parsea). **No bloquea G (037)**. Independiente de L. N
(034) emite los 14 perfiles *tal cual están*; M7–M9 corrige instructing de
gate en **036** (tercer pin).

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `scripts/check_forge_ladder.py` | create | high | `implementer_agent` | ⏭ 036 |
| M2 | `tests/test_check_forge_ladder.py` | create | medium | `implementer_agent` | ⏭ 036 (commit con M1) |
| M3 | `agents/skill_architect.md` | modify | high | `agent_orchestrator` | ⏭ 036 |
| M4 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | create | medium | `doc_orchestrator` | ⏭ 036 |
| M5 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | ⏭ 036 |
| M6 | `tests/test_agent_profile_census.py` | create | medium | `implementer_agent` | ⏭ 036 |
| M7 | `agents/qa_agent.md` | modify | high | `agent_orchestrator` | ⏭ 036 |
| M8 | `agents/tester_agent.md` | modify | high | `agent_orchestrator` | ⏭ 036 |
| M9 | `agents/principal_agent.md` | modify | high | `agent_orchestrator` | ⏭ 036 |

M1 es el chequeo, no un agente. Dos modos, detectados como `_mode.is_nucleus()`
(directorio `.git` vs fichero `gitdir:`):

| Caso | Pasa | Sale 2 |
| :--- | :--- | :--- |
| Host, paso cuyo Assignee no existe en `agents/` ni en `.claude/agents/` | `Destination` = `host:.claude/agents/` **y** el `.md` está en el host | destino vacío, o el `.md` escrito bajo `.agents/agents/` |
| Host, unidad cuyo tool no está en un manifiesto stub | `skill_assignment.md` registra P3 miss (cuerpo simulado) **y** existe `SKILL.md` bajo `.claude/skills/<name>/` | «No skill was forged» sin rastro P3, o el skill escrito bajo `.agents/skills/` |
| Núcleo, create de perfil | `Destination` = `nucleus:PR` y el fichero está en `agents/` | `host:.claude/agents/` en una sesión núcleo sin ese árbol |

P3 **no pega a la red**. M1 acepta un registro `{source: skills.sh, query, hit: false}`
en el artefacto, y los tests inyectan ese JSON. Un cliente HTTP real, si se
escribe, vive detrás de un flag y no entra en `make verify`.

Criterio de hecho: el fixture copia el layout de `tests/test_installer.sh`
(host + `.agents/.git` = `gitdir:`). Tres asserts: (1) host sin perfil y sin
archivo en `.claude/agents/` → exit 2; (2) el mismo host con el `.md` forjado
ahí → exit 0; (3) el mismo host con el `.md` bajo `.agents/agents/` → exit 2.
Simétrico para skills. `python3 -m pytest tests/test_check_forge_ladder.py -q`
sale `0`.

M3 sustituye `skill.sh` (no existe) por la escalera nombrable: P1
`skills/manifest_skills.json`, P2
`skills/autoskills-3rd/node_modules/.bin/autoskills` (tras `pnpm install --dir`
en ese árbol), P3 `https://skills.sh/` **y** `WebSearch`/`WebFetch` ya
declarados, P4 `skill_forge_workflow.md` destino (a) por defecto. Criterio de
hecho: `rg -n 'skill.sh' agents/skill_architect.md` no coincide; `rg -n
'skills.sh' agents/skill_architect.md` sí.

M4 es la plantilla que Phase 4.2 no tiene. Columnas mínimas: unidad, skill
resuelto o `none`, peldaño (P1–P4), evidencia (path del manifiesto / comando
autoskills / `{source, query, hit}` / path forjado), destino de forja si P4.
Criterio de hecho: `pipeline_workflow.md` Phase 4.2 cita el filename
`SKILL_ASSIGNMENT_TEMPLATE.md`.

M5 añade a Phase 4.1 y 4.2 el comando
`python3 scripts/check_forge_ladder.py --sprint-dir <dir>` — exit 2 rechaza.
**Mismo archivo que E3, I2 y K6**: va el último de los cuatro sobre
`workflows/pipeline_workflow.md`. Criterio de hecho: esas dos celdas nombran
`check_forge_ladder.py`.

M6 pinnea el censo de D19 contra `agents/*.md` (14 ficheros, no el ejemplo de
`profiles/`). **Criterio de hecho (cinco fallos, no el exit code a solas):**
el test sale `2` si ocurre cualquiera de (1) un perfil de `tiers.gate.profiles`
con `Write` o `Edit` como ítem; (2) `qa_agent` / `tester_agent` sin `Bash`;
(3) `orchestrator` sin `Write`; (4) `name:` kebab distinto del stem
(`qa_agent` → `qa-agent`); (5) recuento ≠ 14. `python3 -m pytest
tests/test_agent_profile_census.py -q` **codifica** esos cinco asserts; no
es el único done-criterion. Hoy el árbol cumple (1)–(5) y el test sale `0`;
poner `Write` en `qa_agent.md` debe ponerlo en `2`.

M7 y M8: en ambos perfiles, las filas `double_gate_review` / `rejection_trigger`
dicen **Phase 4**; el pipeline las corre en Phase 7. Sustituir la etiqueta de
fase. En `qa_agent.md`, la `description` «after Definitive Sprints» pasa a
«after Phase 6 Execution». No tocar `tools:` ni `verdict_routing`. Criterio de
hecho: `rg -n 'Phase 4' agents/qa_agent.md agents/tester_agent.md` no coincide
en esas claves; `rg -n 'Phase 7' agents/qa_agent.md agents/tester_agent.md` sí;
`rg -n 'Definitive Sprints' agents/qa_agent.md` no coincide en el frontmatter.

M9: (1) `consensus_loop` dice que la *sesión* que tiene `Write` materializa
`IMPLEMENTATION_PLAN.md` (Phase **1**), y que el subagente no declara `Write` a
propósito. (2) `approval_gate` se relabela Phase **5**. (3) `execution` /
`remediation_loop` se relabelan Phase **6**. (4) se añade una fila Phase **8**
que nombra `PHASE_REGISTER.md` / host `CHANGELOG.md` y deja la escritura en la
sesión, no en `tools:`. No se añade `Write` al perfil. Criterio de hecho: esas
cuatro claves coinciden con `workflows/pipeline_workflow.md`; `tools:` sigue
sin `Write`/`Edit`.

M7–M9 son tres ficheros, mismo asignatario (`agent_orchestrator` tiene
jurisdicción sobre `agents/`). Orden: M7, M8, M9. M6 no depende de ellos: los
invariantes de herramientas ya se cumplen; M7–M9 son instructing.

### Track N — puente Cursor de subagentes (docs.cursor.com/subagents) (**034**)

El formato no se inventa. `cursor_adapter.py` no lo emitía. Corre después de
M (el censo fija los 14) y no bloquea G. Independiente de L.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| N1 | `scripts/cursor_adapter.py` | modify | high | `implementer_agent` | ✅ `676b72a` |
| N2 | `tests/test_cursor_adapter.py` | modify | medium | `implementer_agent` | ✅ `676b72a` (con N1) |
| N3 | `.gitignore` | modify | low | `implementer_agent` | ✅ `89861df` |
| N4 | `scripts/install.py` | modify | medium | `implementer_agent` | ✅ `7fb98cf` |
| N5 | `tests/test_installer.sh` | modify | medium | `implementer_agent` | ✅ `7fb98cf` (con N4) |
| N6 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | modify | low | `doc_orchestrator` | ✅ `8978a56` |

N1 escribe `.cursor/rules/01-chat-title.mdc` (`alwaysApply: true`: el tab se
llama como las ramas sprint de la conversación) y `.cursor/agents/{name}.md`
con el contrato de https://cursor.com/docs/subagents. `model: inherit` (Task
aplica el mapa, ADR-0010). `readonly: true` si `tools:` no incluye `Write` ni
`Edit`. Cuerpo del perfil intacto. Criterio de hecho:
`ls .cursor/agents \| wc -l` = recuento de `agents/*.md`; existe
`implementer-agent.md`; `qa-agent.md` tiene `readonly: true` y no copia
`tools:`.

N3/N4: `.cursor/agents/` es generado (mismo criterio P11 que commands/rules).
N5: 13 reglas (12 + chat-title) y 14 subagentes en el fixture host.
N6: el bullet Cursor de la guía nombra `.cursor/agents/` (diff ya en worktree).
Criterio de hecho: `rg -n 'cursor/agents' docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md`
≥1.

`install.py --target cursor` hace `rmtree` de `.cursor/`: la regla de título
y los perfiles **tienen** que salir del adaptador, no de un `.mdc` escrito a
mano que el siguiente install borra.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | El sprint no añade paquetes |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Pin automático `.agents` en `/start` | script | `start_workflow.md#lightweight_sync` → `scripts/sync_agents_pin.py` |
| Frescura del grafo | script | `session_probe.py` + close post-`atomic_commit` |
| Close → deploy | el agente continúa el **siguiente protocolo nombrado** | `commands/close.md` + `close_workflow.md#deployment_handoff`; los gates internos de deploy siguen separados (`RA-13`) |
| Resolve tier → slug | script | `audit_cursor_models.py --resolve` |
| Proponer Model/Effort | juicio de `token_economy_agent` acotado por D10; escritura de `rule_validator` | `pipeline_workflow.md` Phase 4.3 |
| Aplicar Model en Cursor | `Task` + slug resuelto | `pipeline_workflow.md` Phases 4.3 / 7 |
| Ledger de gate rounds | script derivado (join de dos parsers existentes) | `Makefile` `model-ledger` → `scripts/model_ledger.py`; `close_workflow.md` al cerrar |
| Censo de ejecución 026–033 | script derivado (CE-1–CE-4 sobre parsers existentes) | `Makefile` `cursor-era-audit` → `scripts/audit_cursor_era.py`; **no** está en `verify` |
| Escalera de forja agente/skill | script (P3 simulado; sin red) | `pipeline_workflow.md` Phases 4.1 y 4.2; `python3 scripts/check_forge_ladder.py --sprint-dir …` |
| Proponer celda `gate` | script (cuatro filtros estructurales, sin juicio) | `audit_cursor_models.py` tras E6 |
| Rotación de candidatos `mechanical` | juicio de `token_economy_agent` acotado por la cadencia D12 | `pipeline_workflow.md` Phase 4.3 |

Phase 5 nunca bajo `/loop`. Phases 6–8 solo si el humano arma antes
`loop_guard.py start` (`rules/loop_governance.md`).

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | **27** este sprint (8 ✅, 6 N worktree, 3 P worktree, 10 ⏳) · **58** el programa | 034 ejecuta A B I K J N P. ⏭: C E H F = 035 (17); M L = 036 (12); G = 037 (2). 038 = family-trial, plan propio |
| Orden entre tracks | **034:** `A → B → P → I → K → J → N`. **Programa:** 034 → 035 (C E H F) → 036 (M L) → 037 (G) → 038 (trial) | **Sin condicionales.** P3 y C2 (035) son toques sucesivos de `start_workflow.md`. C5 (035) es el primer toque del `Makefile` y va después de E6. H2 (035) va después de E6. L3 (036) es el segundo toque del `Makefile` y va después de C5. M5 (036) es un toque de `pipeline_workflow.md` tras E3 (035); I2 y K6 (034) ya habrán tocado ese archivo. K3 tras I4; K6 tras I2. G (037) mide veredictos de gate (`D17`). N (034) no espera a M |
| Unidades elegibles a `mechanical` | 5 en 034 (`B2`, `I5` ✅, `N2`, `N5`, `P2`); 7 en 035–037 (`C4`, `E4`, `G2`, `H4`, `L2`, `M2`, `M6`) | tests, hoy sobre el modelo de sesión |
| Subagents dispatched | 4 lanzados / 2 veredictos | 2× Other Models (Claude+Gemini) cupo → 0 trabajo. 2× Composer: Tester y QA `REJECTED`/`charter` |
| Prior session ratio | n/a (Cursor / sin transcript) | `python3 scripts/session_cost.py --from-anchor --json` |

---

## Tests

Filas **Sí** de C/E/G/H/L/M son la línea base de **035–037**, no el criterio de
close de 034.

| Check | ¿Falla contra el árbol actual? |
| :--- | :--- |
| Graph probe reporta behind pese a `built_at_commit` ancestral + mtime viejo | **Sí** — B1 |
| `commands/close.md` no nombra `deployment_workflow.md` como siguiente obligatorio | **Sí** — A1 |
| Host `/start` espera autorización para un tag `v*` más nuevo | **No** — worktree P: `sync_agents_pin.py` auto-checkout; start_workflow nombra el script |
| `wc -c workflows/start_workflow.md` ≥ 18 000 | **Sí** — C2 |
| `audit_cursor_models.py --resolve mechanical` | **Sí** — E2 (flag ausente) |
| `propose_tiers` devuelve el modelo aplicado como propuesta de `author` | **Sí** — E5 |
| `make cursor-tiers` deja la tabla `gate` vacía siempre | **Sí** — E6 |
| `make cursor-tiers` sale `0` con la base ausente (éxito silencioso) | **Sí** — E6 |
| El guard `--check` afirma que `gate` debe estar vacío, y además no lo invoca nadie | **Sí** — E6 (invertir + cablear en `Makefile`) |
| `AGENTS.md:17` declara inexistente el ancla de estado del núcleo, que existe | **Sí** — J1 |
| `check_role_artifact.py` aprueba un directorio vacío con el nombre de rol que usa el framework | **No** — K1 `9e8c0d3`; `--role rule_validator` sobre dir vacío sale `2` |
| `QA Agent` y `Tester Agent` no deben dejar ningún artefacto | **No** — K2 `ca203ce`; `gate_evidence` en el registro |
| `check_task_scope.py` aprueba la ausencia del propio `task_scope.md` | **Sí** — K3 (dir ausente o vacío sigue `skip` / exit `0`) |
| `tiers.gate.cursor.model` es `null` | **Sí** — H2 |
| Coherencia `model:` del perfil vs celda del tier, los 14 perfiles | **Sí** — ensayo en seco de `(f)`: **0 divergencias** hoy. `H3` es protección de regresión, no arreglo: fija un estado correcto antes de que derive |
| `model_ledger.py` sobre 032 y 033 | **Sí** — G1 (script ausente) |
| `audit_cursor_era.py` sobre 026–033 | **Sí** — L1 (script ausente). CE-1 sobre 028 ya es medible hoy con I4: 3 filas |
| Tester 033 nombra un fichero de test, no `tests/` | **Sí** — CE-4 de D18; el censo lo cuenta, no lo reescribe |
| Tests del fallback de forja agente/skill | **Sí** — M1/M2 (cero cobertura hoy; ver D19) |
| `skill.sh` nombrado y ausente | **Sí** — M3 |
| `qa_agent.md` / `tester_agent.md` etiquetan el Double-Gate como Phase 4 | **Sí** — M7/M8 (el pipeline es Phase 7) |
| `principal_agent`: Phase 3/4 vs 5/6, `consensus_loop` vs `tools:`, Phase 8 ausente | **Sí** — M9 |
| Censo: gate con `Write`, o `name:` ≠ stem kebab | **No hoy** — M6 protege; `qa`/`tester`/`principal` ya son read-only |
| `.cursor/agents/` vacío pese a contrato Cursor documentado | **No** — worktree N: 14 ficheros (gitignored). N1–N5 siguen sin commit; un `install --target cursor` debe **regenerarlos** |
| `audit_plan.py` sobre este plan | **No** — proteger |

---

## Verification

Leer `$?` directamente (nunca a través de un pipe). Close de **034** solo
exige la primera tabla. La segunda es inventario de 035–037.

### Este sprint (034)

| Command | Expected |
| :--- | :--- |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `python3 scripts/session_probe.py; echo $?` | sin false graph-behind cuando el campo de commit está al día |
| `rg -n 'deployment_workflow' commands/close.md` | ≥1 |
| `rg -n 'active_state.json' AGENTS.md` | §0 **no** declara inexistente el ancla en el núcleo |
| `python3 -m pytest tests/test_session_probe.py tests/test_check_task_scope.py tests/test_check_role_artifact.py tests/test_cursor_adapter.py tests/test_sync_agents_pin.py -q; echo $?` | `0` |
| `rg -n 'sync_agents_pin.py' workflows/start_workflow.md` | ≥1 |
| `rg -n 'await explicit authorization' workflows/start_workflow.md; echo $?` | `1` |
| `ls .cursor/agents \| wc -l` | igual a `ls agents/*.md \| wc -l`; incluye `implementer-agent.md` |
| `rg -n '^readonly:' .cursor/agents/qa-agent.md .cursor/agents/implementer-agent.md` | `true` / `false` |
| `test -f .cursor/rules/01-chat-title.mdc && rg -n 'alwaysApply: true' .cursor/rules/01-chat-title.mdc` | coincide |
| `make verify; echo $?` | `0` (sin exigir aún el check `(f)` de H3) |

### Cola 035–037 (no es close de 034)

| Command | Sprint | Expected |
| :--- | :--- | :--- |
| `python3 scripts/session_start.py; echo $?` | 035 | `0`; briefing &lt; 80 líneas; sin dump completo de UPSTREAM |
| `python3 scripts/audit_cursor_models.py --resolve mechanical; echo $?` | 035 | `0`; imprime `composer-2.5` |
| `python3 scripts/audit_cursor_models.py --resolve gate; echo $?` | 035 | `0`; tras H2 imprime la celda; si estuviera vacía devuelve `session` sin inventar id |
| `python3 scripts/audit_cursor_models.py \| rg -A3 '## Gate'` | 035 | Al menos una fila, ninguna de la familia de `author` |
| `python3 -c "import json; t=json.load(open('config/model_tiers.json'))['tiers']; print(t['gate']['cursor'], t['author']['cursor'])"` | 035 | `gate.model` no nulo y `gate.family != author.family` |
| `make verify; echo $?` | 035 | `0`, y con `agents/qa_agent.md:5` alterado a `sonnet` sale distinto de `0` citando `(f)` |
| `python3 scripts/audit_cursor_models.py \| head -3` | 035 | La propuesta de `author` es la celda del mapa; el modelo aplicado aparece como discrepancia, no como propuesta |
| `wc -c workflows/start_workflow.md` | 035 | **&lt; 8 000** |
| `rg -n '13 profiles' agents/token_economy_agent.md; echo $?` | 035 | `1` (F3: el mapa tiene 14) |
| `python3 scripts/model_ledger.py; echo $?` | 037 | `0`; `docs/audits/MODEL_LEDGER.md` con fila para 032 y 033 |
| `python3 scripts/audit_cursor_era.py; echo $?` | 036 | `0`; `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` con 8 filas (026–033); fila 028 CE-1 > 0; fila 033 CE-1 = 0 |
| `make cursor-era-audit; echo $?` | 036 | `0`; el target no aparece como receta de `verify` |
| `python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/033-core-pipeline; echo $?` | 036 | `0` en núcleo (033 A1 tiene destino y fichero); un fixture host sin `.claude/agents/<nuevo>.md` sale `2` |
| `rg -n 'skill.sh' agents/skill_architect.md; echo $?` | 036 | `1` (sin coincidencias) |
| `python3 -m pytest tests/test_session_start.py tests/test_audit_cursor_models.py tests/test_model_ledger.py tests/test_verify_references.py tests/test_audit_cursor_era.py tests/test_check_forge_ladder.py tests/test_agent_profile_census.py -q; echo $?` | 035–037 | `0` |
| `rg -n 'Phase 4' agents/qa_agent.md agents/tester_agent.md` | 036 | sin `double_gate_review` / `rejection_trigger` en Phase 4 |
| `rg -n 'approval_gate' agents/principal_agent.md` | 036 | la fila nombra Phase 5 |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md` | Este plan |
| `commands/close.md` / `commands/start.md` | Siguiente protocolo nombrado |
| `workflows/close_workflow.md` / `start_workflow.md` / `pipeline_workflow.md` | Handoff, briefing, Task+resolve |
| `scripts/session_start.py` / `session_probe.py` / `audit_cursor_models.py` / `model_ledger.py` | Mecanismos nuevos o modificados |
| `docs/audits/MODEL_LEDGER.md` | Generado por `make model-ledger`; nunca editado a mano |
| `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` | Generado por `make cursor-era-audit`; nunca editado a mano |
| `docs/decisions/ADR-0010-cursor-task-applies-tier-map.md` | Task aplica el mapa |
| `docs/decisions/ADR-0011-gate-cell-by-structural-ceiling.md` | Supersede la cláusula `null` de ADR-0003 |
| `config/model_tiers.json` | Celda `tiers.gate.cursor` rellenada por techo estructural |
| `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | Columna `Assignee (proposed)` + autoridad de Phase 4.1 |
| `workflows/pipeline_workflow.md` | Phase 4.1 puede sobrescribir la propuesta |
| `agents/agent_orchestrator.md` | `staffing_injection` deja de decir «unassigned» |
| `docs/hotfixes/H-005-pipeline.md` | 32 filas de 028 a 032 con asignatario sin `Write` |
| `scripts/verify_references.py` | Check `(f)`: `model:` del perfil vs celda del tier |
| `docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md` | Forma de `agent_assignment.md`, citada desde Phase 4.1 |
| `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | Forma de `skill_assignment.md` con peldaños P1–P4, citada desde Phase 4.2 |
| `scripts/check_forge_ladder.py` | Fallback de forja en layout host-submódulo |
| `scripts/cursor_adapter.py` / `.cursor/agents/` | Contrato Cursor documentado; `01-chat-title.mdc` |
| `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | El puente Cursor nombra `.cursor/agents/` |
| `tests/test_agent_profile_census.py` | 14 perfiles: tools/fase/kebab; gates sin `Write` |
| `agents/qa_agent.md` / `tester_agent.md` / `principal_agent.md` | Phase 7; `consensus_loop` vs `tools:` |
| `AGENTS.md` | §0: retirar la cláusula que declara inexistente `docs/active_state.json` en el núcleo |
| `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | Padre vs Task; ledger como evidencia; protocolo de gate replay (D16) |
| `agents/token_economy_agent.md` | Regla D10 + propuesta task_scope + ledger |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Regenerado por `make verify` si cambian celdas write |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Una línea Status: 034–037 protocolo (IDs nuevos; no renumerar 021–033); 038 family-trial; hosts reanudan tras deploy 034 |
| `scripts/sync_agents_pin.py` / `workflows/start_workflow.md` | Ping + auto-checkout del tag `v*` más nuevo en `/start` |
| `README.md` / `agents/git_sync_agent.md` / `close_workflow.md` | RA-14: pin-bump ya no espera autorización humana |

---

## Out of scope

| Exclusión | Destino |
| :--- | :--- |
| Promover `claude-opus-5` / `glm-5.2` a `cursor.author` | Sprint **038** tras primera evidencia de ledger (037) + Double-Gate (D6) |
| **Abaratar** `gate` con historial de ledger | Fuera de 034–038: `ADR-0003` sigue vigente en eso. H1 solo supersede la cláusula `null` |
| Que `load_proven_families()` lea el ledger | Sprint posterior; queda reservada a la pregunta de coste |
| Medidor Cursor tokens ÷ unidades aceptadas | Sprint de instrumentación (path Cursor de `session_cost.py`). El ledger mide **rondas**, no tokens |
| Trackear `graphify-out/graph.json` | `graph_stats.json` del sprint |
| Reescribir `SPRINT_LOG.md` / `task_scope.md` de 026–033 | El censo (Track L) documenta; igual que H-005, no lava el registro |
| Encender `ruff check .` en `make verify` | 177 errores; 032 y 033 lo excluyeron como migración. D18 CE-5 no lo reabre |
| Tratar «subagentes que no se lanzan» como defecto de 026–033 | `M3` PASSED: sequential es la configuración de la era |
| Meter el censo en `make verify` | Volvería rojo el núcleo por hallazgos históricos de 028–032. El abort de I4 lo prohíbe |
| Forjar un skill o agente real en 034 para «demostrar» el fallback | Contaminaría el núcleo. El hueco vive en el fixture de M2 |
| Relabelar Phase 2→4.1/4.2/4.3 en `agent_orchestrator` / `skill_architect` / `rule_validator`, o Phase 1→3 en `orchestrator` | Instructing medido en D19; **036** toca perfiles de gate (M7–M9). 034 no relabela el cluster 4.1–4.3. Resto al reorden (O5) o sprint siguiente |
| Copiar `tools:` / `tier:` / alias Claude (`opus`) al frontmatter Cursor | El contrato documentado no los incluye; `model` es `inherit` |
| Dar `Write` a `principal_agent` para que el subagente escriba el plan | M9 aclara la sesión vs el perfil; no se abre el Approval Gate a edición de árbol |
| Pegar a `https://skills.sh/` desde `make verify` | P3 se simula. Un cliente HTTP, si existe, va detrás de un flag |
| Convertir filas `new` del censo en unidades antes del reorden | O5: al final |
| Fusionar `ci_gate` + `gh pr merge` | `RA-13` |
| Red dentro de `session_start.py` o por fila de `task_scope` | Ninguna unidad de 034 toca la red **salvo** `sync_agents_pin.py` (ping `git fetch --tags`, timeout 20s, degrada si falla). O1 retiró el canal de prior |
| Agente selector por unidad | `ADR-0004`; el selector es el script de D10 y el dueño sigue siendo `token_economy_agent` (D8) |
| Superseder `ADR-0004` | Innecesario: D10 es determinista, que es la alternativa que el propio ADR exige |

---

## Abort criterion

- Close hace merge sin observar `ci_gate` exit 0 por separado → revertir A1+A2.
- `sync_agents_pin.py` hace checkout de `main` o de un commit sin tag `v*` → revertir P1: el bump es solo el producto de deploy.
- `sync_agents_pin.py` pisa un árbol `.agents` sucio → revertir P1.
- `start_workflow` `lightweight_sync` vuelve a exigir autorización humana para un tag `v*` publicado → revertir P3.
- `start_workflow` elimina un paso que `session_start.py` no ejecuta → revertir C1+C2.
- Runtime elige el modelo «mejor» del catálogo en lugar de `--resolve` → revertir E1–E4.
- Gate `Task` inventa un slug mientras `cursor.gate.model` es null → revertir E3.
- `propose_tiers` sigue devolviendo el modelo aplicado como propuesta → revertir E5 y rehacerlo.
- `model_ledger.py` escribe parsers propios en vez de importar los de `check_gate_log.py` y `check_task_scope.py` → revertir G1.
- `MODEL_LEDGER.md` se edita a mano en lugar de regenerarse → revertir la edición.
- `H2` rellena `gate` con un modelo de la misma familia que `author` → revertir H2.
- `H1` termina abaratando el gate en vez de fijar el techo → revertir H1+H2; `ADR-0003` prevalece.
- `I1` renombra la columna dentro de un `task_scope.md` → revertir: `work_tables()` dejaría de ver la tabla y el check pasaría a falso verde.
- `H3` se «arregla» relajando el check para que acepte divergencias perfil↔mapa → revertir: el check existe precisamente para que una de las dos no cambie sola.
- `H2` copia `effort: high` de la celda de Claude en vez del máximo expuesto → corregir la celda, no el criterio.
- Cualquier documento del sprint afirma que una familia es mejor que otra → borrar la afirmación: D13 lo prohíbe y no hay base para sostenerla.
- El gate replay se ejecuta dentro de 034–037 → parar: O3 y D16 lo sitúan en **038**; E0 (035) solo escribe el protocolo.
- `I4` rechaza filas legítimas de sprints cerrados al correr sobre histórico → acotar el check al sprint en curso, no relajar el criterio.
- `L1` sale distinto de `0` porque 028–032 tienen CE-1 > 0 → revertir: el censo no es un gate.
- `L3` añade `cursor-era-audit` como receta de `verify` → revertir esa línea del `Makefile`.
- El censo se usa para reescribir un `SPRINT_LOG.md` cerrado → revertir la edición; H-005 y D18 documentan, no lavan.
- Una unidad de 034 «arregla» la suite pytest por los 20 failed del sandbox → parar: CE-5 lo retractó (`553 passed` fuera).
- `M1` da por válida una forja bajo `.agents/agents/` o `.agents/skills/` en un fixture cuyo `.git` es un pointer `gitdir:` → revertir: ese es el caso host y `strict_rule` lo prohíbe.
- `M1` pega a `skills.sh` en `make verify` → revertir la red; P3 es un registro simulado.
- `M6` deja pasar `Write` en `qa_agent.md` o `tester_agent.md` → revertir: un gate que edita lo que juzga es `F-026-A1`.
- Tests deja **Sí** en un fallo que Work ya marca ✅ (K1/K2) → revertir la fila Tests; el desfase es `charter` (Tester 2026-08-26).
- `M9` añade `Write` a `principal_agent` → revertir: ni Phase 1 ni Phase 8 abren el Approval Gate a edición de árbol.
- `M7`/`M8` cambian `tools:` o `verdict_routing` además de la etiqueta de fase → revertir lo que no sea el número de fase.
- `N1` copia `tools:`/`tier:` o pone `model: opus` en `.cursor/agents/` → revertir: el contrato Cursor es `inherit` + `readonly`.
- `N1` deja `01-chat-title.mdc` solo como fichero manual bajo `.cursor/rules/` → revertir: `install.py --target cursor` hace `rmtree` de `.cursor/` y lo borraría.
- Scores o $/1M llegan a `config/model_tiers.json` → revertir esa unidad (`ADR-0005`).
- Family trial ejecutado dentro de 034–037 → parar; O3/O4 lo sitúan en **038**.

---

## Double-Gate de este plan (antes de Phase 5)

Autor de la era: xAI/Grok. Cupo Other Models (Anthropic/Google) agotado en
esta sesión: los dos lanzamientos a Claude Opus y Gemini **no ejecutaron**.
Relanzado sobre Composer (familia Cursor ≠ xAI).

| Gate | Agente | Modelo | Veredicto | Clase |
| :--- | :--- | :--- | :--- | :--- |
| 1 | QA | Composer 2.5 | `REJECTED` | `charter` |
| 2 | Tester | Composer 2.5 | `REJECTED` | `charter` |

Tester: Tests/Evidence desfasados; `make verify` duplicado; M6 = solo pytest
exit 0. Parcheados.

QA: guía slash sin fila Work; DAG global incompleto; C5/L3 condicional;
RA-08 vs commits compartidos; sin `## Context`. Parcheados (N6, DAG de
programa `034 → 035 → 036 → 037 → 038` y DAG de 034 `A → B → I → K → J → N`,
L3 siempre tras C5, tabla de commits compartidos, sección Context).

Phase 5 **autorizada** 2026-08-26. Los `REJECTED` eran al plan, no a código
de producto; no arrancaron `remediation_workflow.md`. Hallazgos de charter
ya parcheados en este archivo.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo (chat, «ok, comenzamos»; confirmado «phase 5 ok» 2026-08-26) |
| **Date** | 2026-08-26 |
| **Plan commit at approval** | `ffd33e0` |
| **Remaining locks** | Active Sprint · QA + Tester · Human OK al close |

*Phase 5 es una única autorización humana atendida. Nunca envolver en `/loop`.*

---

## Cómo reanudar (siguiente sesión)

1. Releer este archivo (sobre todo **Open decisions** + **Evidence snapshot**).
2. Re-ejecutar los comandos Reproduce; sustituir cifras obsoletas.
3. O1–O3, O5 y **O6** están **cerradas**. O4 pertenece a **038**.
4. Los dos parámetros que rellenó el Principal están **confirmados por el
   humano el 2026-08-25**: ventana de línea base de D12 = **2 sprints**, y
   desempate de familia de D13 = misma que `gate.claude_code`, luego mayor
   ventana de contexto. No quedan huecos de decisión abiertos en el diseño.
5. Phase 5 **autorizada** 2026-08-26. Phases 3–4 se **backfillearon el mismo
   día** (`SPRINT_LOG.md`, `agent_assignment.md`, `skill_assignment.md`,
   `task_scope.md`) porque Phase 6 había arrancado sin ellos. Quedan **K6** y
   **J1** (⏳ en `task_scope.md`). No ejecutar filas `⏭`.
6. Tras A–N: close+deploy de 034. Primer pin de hosts a ese tag.
