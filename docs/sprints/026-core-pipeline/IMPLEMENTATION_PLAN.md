# Implementation Plan: Sprint 026 — `tool-portability`

**Canonical path**: `docs/sprints/026-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/026` · **Base**: `main` at `b5bfb6a`
**Status**: `DRAFT` → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.
>
> **Revisión 2 (2026-08-24).** El eje de primer nivel deja de ser la dependencia
> técnica pura y pasa a ser **dos hitos separados por una migración de herramienta**,
> por directiva humana. Las mediciones de la revisión 1 se conservan sin cambios.

---

## Context

**Objetivo acordado (Apéndice `026` de `docs/roadmaps/core/pipeline/021-030-program-queue.md`, líneas 924–1118):** *portabilidad* — el mismo repositorio se abre con Cursor o con Claude Code indistintamente, con estado coherente en ambos. **No** es concurrencia, **no** es handoff, y **no** hay llamadas a la Anthropic API (decisión humana registrada: *"for that I use Claude"*).

**Directiva humana de ordenación, 2026-08-24, que gobierna este plan por encima de la dependencia técnica:** *"antes de responder a todo eso, quiero reordenar el plan, de modo que lo primero que hagamos sea lo necesario para que Cursor pueda continuar este trabajo. Es decir: primero estructuramos todo, y una vez hecha la parte necesaria instalamos en Cursor y continuamos."*

De ahí la forma de este plan: **Hito 1** (bajo Claude Code) entrega el conjunto mínimo y completo que permite a una sesión de Cursor abrir este repositorio y ejecutar `workflows/start_workflow.md` de Phase 0 a Phase 2; la **Puerta de Migración** lo comprueba con observaciones nombradas; **Hito 2** ejecuta el resto bajo Cursor.

**Prerrequisito consumido.** `config/artifact_registry.json` (unidad `C0.2` del Sprint 023) existe en el árbol y declara 13 artefactos con `filename`, `phase`, `role`, `scope`, `host_path`, `nucleus_path` y `required`. Su propio `_why_it_matters` nombra a este sprint. Limitación medida que este plan respeta: `required` **solo se aplica hoy para `scope == "sprint"`** (7 artefactos); en `scope == "repository"` es declarativo y ningún consumidor lo filtra.

**Lectura obligatoria de `agents.md §0 open_upstream_findings`, ejecutada.** Se leyó `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`:

| Ítem | Línea | Relación con este sprint |
| :--- | :--- | :--- |
| `F-023-S4` | 559 | **Fuera de alcance por decisión humana**, con coste restado bajo la nueva ordenación (abajo) |
| `F-021-A2` | 511 | **No se cierra aquí.** `P1` lo roza y declara explícitamente que no lo resuelve (`Design §D4`) |
| `C5` (ID de finding de un host, no la unidad `C5` del Sprint 023) | 699 | **Es el objeto de `P7`.** El apéndice cita "`C5`'s question" sin desambiguar entre dos objetos homónimos; queda resuelto: es el finding del host en la línea 699 |

**Lectura del bloque `F8` / `F-023-S4` (líneas 55–88 del roadmap), ejecutada — y su coste aumenta bajo la nueva ordenación.** La disposición del 2026-08-24 enruta ese defecto a un `RA-03 HOTFIX_FLAT` con destino `docs/hotfixes/[H-ID]-secrets.md`, ejecutado después de `026`. El párrafo de la línea 80 pide que quien abra `026` lo lea antes de decidir si el orden se sostiene. Se leyó. **Lo que la revisión 1 no podía decir y esta sí:** el Hito 2 se ejecuta bajo Cursor, y bajo Cursor **la única guarda de secretos que existe es exactamente el mismo `hooks/on_commit.py` medido como ciego** — `permissions.deny` y `sandbox.credentials.files` de Claude Code no se leen allí (roadmap líneas 1176–1180). Es decir: la mitad del sprint que corre bajo Cursor corre con una superficie de protección de secretos **estrictamente menor** que la mitad que corre bajo Claude Code, y el diferencial es precisamente el defecto abierto. Esto no cambia la decisión — la decisión es del humano — pero cambia su coste.

**Qué es cierto cuando el sprint termina.** El criterio del apéndice (línea 1089): el mismo repositorio, abierto con cualquiera de las dos herramientas, produce **el mismo conjunto de artefactos con los mismos nombres y rutas**, y `close_workflow.md` Phase 2.6 sella o rechaza sin poder distinguir cuál lo generó.

**Bloqueador de día uno, medido en el árbol actual.** `scripts/session_state.py:194` declara `claim_parser.add_argument("--session-id", required=True)`, y `workflows/start_workflow.md:20` (`state_claim`, Phase 0.5) lo invoca con el UID que entrega el harness de Claude Code. Cursor no expone ningún UID de sesión.

**Residuo de estado, medido.** `docs/active_state.json` declara `current_sprint.id: 23` y `resume_pointer.branch: "ai-sprint/023"`, rama que ya no existe. `workflows/start_workflow.md:21` explica por qué sobrevive: *"opening a sprint writes no field of the anchor and no script does"*. Se corrige como unidad nombrada (`A1`).

**Decisiones humanas ya cerradas, incorporadas como hechos y no como propuestas:**

| # | Decisión | Consecuencia en este plan |
| :--- | :--- | :--- |
| 1 | Cursor **está instalado** en la máquina de trabajo | `P4.0` es ejecutable: se produce y se lee un `.mdc` real. `P4.2` puede abrir `state.vscdb`. **Nada se difiere por falta de Cursor** |
| 2 | `scripts/install_claude.sh` **permanece** como shim de deprecación de dos líneas; `scripts/install_claude.py` **se elimina** por `git mv` | `P3.1b` es una unidad entregable, no una opción |
| 3 | El contenido del núcleo alcanzado por symlink queda **FUERA** del alcance de las puertas documentales del host | `P7` escribe ese veredicto, no lo propone |

**Línea base verde, medida por `devops_agent` en `b5bfb6a`** (Phase 2 del pipeline), antes de que exista ninguna unidad de este plan:

- `make verify` sale `0` y ese único comando ya cubre **428 tests pasados** (0 fallidos, 0 omitidos) más `tests/test_installer.sh`.
- `python3 scripts/session_state.py claim --help` imprime `usage: session_state.py claim [-h] --session-id SESSION_ID [--takeover]` — el bloqueador de día uno, confirmado en su forma literal.
- `hooks/` contiene `__init__.py`, `on_commit.py`, `on_commit_msg.py`, `on_init.py`, `state_mirror.py`, `telemetry.py`. Ningún `on_push.py`.
- `find . -name ".cursor" -type d` no devuelve nada.
- `python3` y `venv_skillopt/bin/python3` son ambos **3.13.13**. Sin riesgo de intérpretes cruzados para el trabajo de `sqlite3` y `argparse`.
- Sin configuración de Docker en el núcleo; las cadenas "Docker" del árbol son fixtures de la puerta de escaneo de secretos.

La columna "¿Falla contra el árbol actual?" de la tabla de `Tests`, más abajo, descansa por tanto en una medición, no en una afirmación.

---

## Design

### D0 — El eje: dos hitos y una puerta, y por qué el corte cae donde cae

El Hito 1 no es "lo importante" ni "lo grande": es **exactamente lo que `workflows/start_workflow.md` necesita para completarse bajo Cursor**, derivado paso a paso de sus nueve pasos. Una unidad indebidamente excluida del Hito 1 no se descubre como una funcionalidad ausente sino como **una sesión de Cursor muerta**, así que el corte se deriva del workflow y no de la intuición:

| Paso de `start_workflow.md` | ¿Qué necesita de este sprint? | Unidad |
| :--- | :--- | :--- |
| 0 `read_anchor` | Un ancla que no apunte a un sprint sellado ni a una rama inexistente | **`A1`** |
| 0 `read_ruleset` | `agents.md` cargado por Cursor. Requiere `.cursor/rules/00-constitution.mdc` con `alwaysApply` | **`P4`**, y `P4.0`/`P4.0b` que lo condicionan |
| 0 `pip_setup`, `read_graph` | Nada. Python plano y `graphify`, ya portables | — |
| 0.4 `drift_check` | Nada. `scripts/detect_drift.py` es Python plano | — |
| **0.5 `state_claim`** | `claim` sin `--session-id`, con `session_tool` | **`P8`** — bloqueador de día uno |
| 0.6 `readiness_probe` | Que la comparación ancla-vs-rama no dispare en falso | **`A1`** |
| 0.7 `platform_probe` | Nada. `gh`, ya portable | — |
| 1 `session_lock_check` | Que la guarda de colisión siga armada con UIDs generados | **`P8.1`** lo prueba |
| 1 `lightweight_sync` | Nada. Git plano | — |
| **1.5 `bridge_check`** | Un lock por target y un instalador con target, y el texto del paso que sepa cuál leer | **`P3.0`, `P10`, `P10.1`, `P8.2`** |
| **2 `pipeline_invocation`** | Los protocolos presentes como comandos de Cursor | **`P4`** (13 ficheros de `commands/`) |
| **2 `delegation_conflict`** | Que el modo secuencial sea configuración leída y no un incidente que dispara **todas** las sesiones por construcción | **`P2`, `P2.1`** |

A eso se añaden cuatro unidades que no aparecen en la tabla porque no son pasos del workflow sino **precondiciones de que esos pasos no destruyan algo**:

| Unidad | Por qué es precondición y no trabajo posterior |
| :--- | :--- |
| **`P6`** | Si `P4` corriera antes de derogar `workflows/standardization_workflow.md:45`, el protocolo de estandarización propondría archivar la configuración que `P4` acaba de crear |
| **`P11`** | Si `.gitignore` no cubre `.cursor/` antes de generarlo, artefactos generados entran al índice; se ignora lo generado y se versiona lo editado a mano, espejando el criterio de `.claude/` en la línea 101 |
| **`P5`, `P5.1`, `P5.2`** | `P4` deriva los `globs:` de los `.mdc` de las condiciones de carga. Sin `P5` esas condiciones siguen siendo prosa y los 11 ficheros de `rules/` llegarían a Cursor sin disparador: o siempre aplicados (ruina de tokens) o nunca aplicados (pérdida de gobernanza). **El Hito 2 se ejecuta bajo Cursor y es mayoritariamente documentación y gobernanza**, exactamente lo que `rules/documentation_standard.md` y `rules/code_craft.md` gobiernan |
| **`P9`, `P9.1`, `P9.2`** | **Reclasificada.** En la revisión 1 era una guarda posterior. Bajo la nueva ordenación, el Hito 2 **commitea y empuja desde Cursor**, donde las cuatro reglas `permissions.deny` de Claude Code no se leen. Las tres denegaciones de git quedarían descubiertas justo durante la mitad del sprint que corre bajo la herramienta menos protegida. Es precondición de la migración, no consecuencia de ella |

Y una unidad que sube al Hito 1 por una razón constitucional, no técnica: **`P1`** — ver `D4b`.

### D1 — El bloqueador de día uno fija el interior del Hito 1

`P8` va primero dentro del Hito 1. Si `session_state.py claim` no acepta la ausencia de `--session-id`, Phase 0.5 aborta bajo Cursor y la Puerta de Migración no puede ni intentarse.

El apéndice (línea 1011) fija la relación con el `M6` del Sprint 021: `P8` cambia *cómo se identifica una sesión*, `M6` *qué estados puede sostener*. Son ortogonales y en ese orden. `P8` no toca la máquina de estados — **y la usa**, ver `D0b`.

**Forma del UID generado, decidida aquí y no en implementación:** `<UTC ISO-8601 compacto>-<PID>`, p. ej. `20260824T094910Z-48213`. Razón: la guarda de colisión de `workflows/start_workflow.md:23` compara UIDs como cadenas opacas, nunca su procedencia, así que cualquier cadena única la satisface; y un timestamp con PID es legible en forense sin herramienta. **Alternativa rechazada:** `uuid4()` — es único pero no dice cuándo ni qué proceso, y la ganancia forense que el apéndice pide (*"which of the two tools left a session open"*) se apoya en el nuevo campo `session_tool`.

### D0b — La migración es un `suspend`, no un cierre — y este plan es lo que la sesión de Cursor lee primero

Este es el mecanismo concreto que ningún documento nombraba. En el momento de migrar, la sesión de Claude Code tiene el ancla en `status: IN_PROGRESS` con su UID. Si Cursor ejecutara `claim`, la guarda de colisión de `workflows/start_workflow.md:23` saldría `2` y la migración fracasaría.

La secuencia correcta usa el estado `SUSPENDED` del `M6` del Sprint 021, que existe exactamente para esto (`start_workflow.md:23`: *"`SUSPENDED` is not a collision — it is a resume… `suspend` ends the session without sealing the sprint, and `claim` over that state proceeds, reports the resume and increments `session_count`"*):

1. Claude Code: `python3 scripts/session_state.py suspend`.
2. Claude Code: `python3 scripts/install.py --target cursor`.
3. Cursor: `python3 scripts/session_state.py claim --tool cursor`.

**`release` está PROHIBIDO en este punto.** `release` sella el *sprint* y escribiría un `last_close_commit` falso que cegaría a `scripts/detect_drift.py` — el mismo razonamiento que el apéndice del Sprint 027 aplica al hook `SessionEnd` (roadmap línea 1157).

Y una consecuencia que cierra el círculo del `triple_lock`: la misma línea 23 obliga a que, en un resume, lo primero que se lea sea **el Implementation Plan, `task_scope.md` y `resume_pointer`**, porque *"the conversation did not survive the boundary, the record did"*. Bajo esta ordenación esa frase deja de ser doctrina y pasa a ser el mecanismo operativo del sprint: **la conversación literalmente no cruza la frontera**, y este fichero es lo que la sesión de Cursor lee para continuar. Es la justificación más concreta que ha tenido `agents.md §0 implementation_plan` desde que se escribió.

### D2 — `P3` es un renombrado, y un renombrado es propagación (`RA-14`)

`RA-14 PATCH_PROPAGATION` es explícito: un parche aplicado solo donde alguien miró, mientras la misma referencia deriva sin corregir en otro punto, **no es una corrección — es una inconsistencia nueva**. El enunciado nombraba dos llamadores. La medición completa, hecha con `grep -rl "install_claude" . --exclude-dir=.git --exclude-dir=venv_skillopt --exclude-dir=graphify-out` sobre todo el árbol, devuelve **40 ficheros** (**88 ocurrencias de línea**), en dos clases: **32 de Clase A** y **8 de Clase B**. La Clase A se descompone en **29 ficheros que referencian el instalador** (enumerados en la tabla de `P3.2`) + **2 ficheros que `P3.0`/`P3.1` renombran** (`scripts/install_claude.py`, `scripts/install_claude.sh`) + **`docs/roadmaps/core/pipeline/021-030-program-queue.md`**, que contiene la cadena y se gestiona en `P3.3`, no en la tabla de `P3.2`.

**El censo entero va al Hito 1, y no es relleno.** Se consideró y se rechaza partirlo: dejar la mitad documental para el Hito 2 significaría **propagar un renombrado a caballo de una frontera de herramienta y de contexto**, con la segunda mitad ejecutada por un agente que no vivió la primera. Esa es literalmente la forma que `RA-14` describe. Además hace comprobable la Puerta de Migración: su criterio incluye un `grep` que debe devolver exactamente una línea.

**Clase A — llamadores vivos y contratos (SE ACTUALIZAN, 32 ficheros: 29 en la tabla de `P3.2` + 2 renombrados por `P3.0`/`P3.1` + 1 gestionado por `P3.3`).** Incluye tres que el enunciado no nombró y que rompen en ejecución, no en prosa: `hooks/on_init.py:16` (`INSTALL_SCRIPT = Path(".agents/scripts/install_claude.py")` — una constante, no una mención), `claude/settings.hooks.json:16` (el mensaje de fallback de `SessionStart`) y `tests/test_installer.sh` (5 invocaciones: líneas 31, 67, 83, 93, 112).

**Clase B — registro histórico (NO SE TOCA, 8 ficheros).** `CHANGELOG.md`, `docs/sprints/023-core-pipeline/SPRINT_LOG.md`, `docs/sprints/023-core-pipeline/task_scope.md`, `docs/sprints/025-core-pipeline/IMPLEMENTATION_PLAN.md`, y los roadmaps `014`, `015`, `018`, `019`. `workflows/standardization_workflow.md:43` fija la doctrina: *"History is never rewritten."* **Evidencia de que esto no rompe la verificación**: `CHANGELOG.md:96` ya menciona `scripts/migrate_docs_v3.py`, un fichero eliminado, y `make verify` pasa hoy — luego las menciones históricas a rutas retiradas no fallan la construcción.

**Un caso que no es ninguna de las dos.** `docs/roadmaps/core/pipeline/021-030-program-queue.md:1284` declara una unidad del **Sprint 029** cuyo contenido es: *"`README.md` line 60 — cites `scripts/install_claude.sh`, which Sprint 026 (`P3`) renames"*. Si `026` corrige `README.md:60`, esa unidad de `029` queda vacía. La cola se actualiza en `P3.3`. La línea 1238 (`U3`, Sprint 030) **no se toca**: describe trabajo futuro sobre el fichero renombrado y sigue siendo válida.

### D3 — Compatibilidad hacia atrás: decidida

Adoptada la recomendación de la revisión 1. `scripts/install.sh` + `scripts/install.py` son los nombres nuevos; `scripts/install_claude.sh` permanece como shim de dos líneas que hace `exec` sobre `install.sh` e imprime a `stderr` una línea de deprecación con fecha de retirada. Coste: un fichero muerto en el árbol. Coste de no hacerlo: cada host con pin anterior rompe su bridge en el bump. `scripts/install_claude.py` se elimina por `git mv`, porque todos sus llamadores son internos y están enumerados.

### D4 — `P1` roza `F-021-A2` y no lo cierra — hay que decirlo dentro del artefacto

`P1` convierte el rol en **columna advisory** y el artefacto en el contrato. `F-021-A2` dice que de los 13 perfiles en `agents/`, 8 tienen `Write`/`Edit` y ninguno es implementador.

**Reduce la urgencia de `F-021-A2`** — si la fase se define por el artefacto que deja, un pipeline puede satisfacerse sin el perfil implementador que falta. `config/artifact_registry.json:12` ya lo dice del campo `role`: *"Advisory because the artifact is the contract; the role is who usually writes it."*

**Y crea un riesgo que este plan nombra antes de que ocurra.** «Rol advisory» se puede leer como licencia para no despachar nunca, que es el precedente del Obstáculo 2 (roadmap líneas 974–978): un host que ejecutó un sprint entero en un solo agente, Fases 4 y 7 nunca corrieron, `task_scope.md` no se produjo, y eso deshabilitó en silencio `jurisdictional_lock` y `no_interference` en ~30 ediciones; cuando las puertas finalmente corrieron, ambas rechazaron la rama por defectos de la clase exacta que el sprint existía para eliminar. Por tanto **`P1` debe escribir literalmente en `workflows/pipeline_workflow.md` que «advisory» rige *qué perfil* redacta, y jamás *si las fases de puerta corren en contexto fresco*.** Y `P1` **no** marca `F-021-A2` como cerrado: su casilla se queda sin marcar.

### D4b — `P1` sube al Hito 1, porque es lo que hace legal la mitad bajo Cursor

Razón, no preferencia. `agents.md §6` manda 8 roles; Cursor no puede instanciarlos. Si el Hito 2 se ejecutara bajo Cursor **antes** de que `P1` aterrice, esa ejecución estaría en contradicción viva con la constitución que la propia sesión de Cursor tiene siempre cargada — el Obstáculo 2 del apéndice, *"structural instead of policy… it would fire every session by construction"* (líneas 965–967). `P2` declara el modo en el estado; **`P1` es lo que declara que ese modo es admisible**. Uno sin el otro deja al Hito 2 corriendo con permiso de configuración y sin permiso constitucional.

Consecuencia secundaria y deseable: `P1` es una edición constitucional de alto riesgo y, al estar en el Hito 1, recibe su puerta en contexto fresco nativo de 8 roles, que es la forma más fuerte disponible.

### D4c — Contexto fresco para las puertas del Hito 2 bajo Cursor

La pregunta es legítima y la respuesta tiene dos mitades, porque las unidades del Hito 2 no son homogéneas.

**Lo que Cursor sí ofrece.** El valor de la puerta, según la propia tabla del apéndice (línea 972), **no es el rol: es el contexto independiente** — *"The value is not the role: it is the independent context"*. Un chat nuevo de Cursor, abierto sin conversación previa, cargando únicamente la constitución (`.cursor/rules/00-constitution.mdc`), el `.mdc` del rol de puerta y el diff bajo revisión, **es** contexto independiente en el sentido que esa frase define. Eso no es una concesión: es la lectura literal del criterio.

**Lo que Cursor no ofrece, y no se disimula.** Tres cosas, y todas son de *prueba*, no de *capacidad*:

| Falta | Consecuencia |
| :--- | :--- |
| No hay primitiva que **obligue** a abrir el chat nuevo | La puerta pasa de forzada a atendida. Nada impide seguir en el mismo chat |
| Nada **registra** que se abrió | Sin registro, la puerta es indistinguible de no haber corrido — el patrón exacto que este programa persigue (roadmap línea 1184: *"a control whose verdict depends on how it was run"*) |
| No hay `SubagentStop` ni equivalente posible | La verificación del artefacto al terminar el rol no existe bajo Cursor (roadmap línea 1180) |

**Mitigación de las dos primeras, mecánica y verificable.** Toda puerta del Hito 2 deja en `docs/sprints/026-core-pipeline/SPRINT_LOG.md` una fila con cuatro campos: unidad, veredicto, herramienta, y **el modelo que la ejecutó leído de disco**, no atestiguado — con `python3 -c` sobre `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`, clave `cursor/applicationOpenModelAppliedConfig`, que el apéndice ya verificó que contiene el modelo seleccionado con sus parámetros (líneas 1041, 1050: *"Auditing which model ran the gate is mechanical, not human attestation"*). Sin esa fila, el paso 4 del test de aceptación no está cubierto y el sprint no cierra.

**DEROGACIÓN POR DECISIÓN HUMANA (2026-08-24).** La revisión 2 proponía además una regla reservando las unidades constitucionales (`agents.md`, `workflows/pipeline_workflow.md`) para puertas bajo Claude Code. El humano la derogó: *"da igual dónde se ejecute, si la secuencia es correcta se puede comitear"*. Consecuencia: **`P7` se puerta bajo Cursor como cualquier otra unidad del Hito 2**, con la secuencia escribir → puerta en chat nuevo → commit y el registro mecánico de herramienta y modelo. La limitación que sobrevive — nada bajo Cursor *obliga* a abrir el chat nuevo, el registro lo prueba a posteriori — **aplica uniformemente a todas las unidades del Hito 2** en lugar de singularizar a `P7`. Efecto sobre el test de aceptación: el paso 4 pasa de *"parcial y declarado"* a **cubierto**, porque `P7` era el único carve-out.

### D5 — El esquema `.mdc` se confirma midiendo, con artefacto nombrado

El apéndice (línea 1019) lo condiciona: *"The exact `.mdc` format is confirmed at implementation."* Verificado en el árbol: `.cursor/` no existe en este repositorio (glob sobre `.cursor/**` devuelve cero entradas). **Con Cursor confirmado como instalado, `P4.0` es ejecutable y no tiene rama de contingencia por indisponibilidad.** El plan no afirma ningún esquema. `P4.0` es un paso de verificación con artefacto nombrado y salida escrita:

1. Crear una regla desde la propia UI de Cursor (`Cursor Settings → Rules → New Rule`).
2. Leer de disco el fichero resultante bajo `.cursor/rules/` con `Read`.
3. Registrar las claves de frontmatter **observadas** en `docs/sprints/026-core-pipeline/cursor_mdc_schema.md`, con la versión de Cursor que las produjo y la fecha.

**Prohibido escribir en el generador una clave que no se leyó de un fichero real.** Es criterio de aborto (`Abort criterion §4`).

### D6 — `AGENTS.md` no puede existir en el núcleo, medido: el sistema de ficheros es insensible a mayúsculas

El apéndice (línea 937) apoya la portabilidad de la constitución en que `AGENTS.md` es un symlink a `agents.md` *"in a real host"*. En un host funciona: `AGENTS.md` en la raíz del host, `agents.md` dentro de `.agents/` — directorios distintos. **En el núcleo ambos caerían en el mismo directorio.** Medido: el glob sobre `{AGENTS.md,agents.md}` en la raíz devuelve **solo** `agents.md`, y la sonda de `P4.0b` (`python3 -c "import pathlib,os; p=pathlib.Path('.git/AGENTS_case_probe'); p.write_text('x'); print(pathlib.Path('.git/agents_case_probe').exists()); p.unlink()"`) devuelve **`True`** en esta máquina: **el sistema de ficheros es insensible a mayúsculas.**

Consecuencia, sin rama: `AGENTS.md` y `agents.md` son la misma ruta en la raíz del núcleo. El punto de entrada de Cursor **en el núcleo** es `.cursor/rules/00-constitution.mdc` con `alwaysApply` apuntando a `agents.md`. No se crea `AGENTS.md` en la raíz del núcleo. En hosts sí, porque allí no hay colisión.

`P4.0b` se mantiene como unidad registrada — el plan no debe afirmar una propiedad del sistema de ficheros que no comprobó, y ahora la medición existe y su salida literal se anexa a `docs/sprints/026-core-pipeline/cursor_mdc_schema.md`. **Bajo la nueva ordenación esta unidad es crítica y no cosmética**: si el punto de entrada de Cursor no carga `agents.md`, la sesión de Cursor arranca sin constitución y el Hito 2 se ejecuta sin gobernanza.

### D7 — `audit_cursor_models.py` llega antes que los datos que necesita, y la nueva ordenación mejora eso ligeramente

El apéndice diseña una escalera de promoción (línea 1074) cuyo peldaño de medición es *"cost per accepted unit = tokens spent ÷ work that passed the gates"*, producido por el medidor del Sprint 021. **El apéndice reconoce el arranque en frío como el límite honesto para un modelo recién descubierto — pero el arranque en frío aplica a los 36, no solo a los nuevos**, porque ningún sprint ha corrido nunca bajo Cursor.

**Lo que cambia con la reordenación**: si `P4.2` se sitúa **al final del Hito 2**, para entonces el Hito 2 entero habrá corrido bajo Cursor y habrá producido las **primeras** mediciones de coste por unidad aceptada bajo esa herramienta. Expectativa medida, no aspiracional:

| Mitad del script | Estado el día de la entrega |
| :--- | :--- |
| Filtros duros (`supportsAgent`, `degradationStatus`, palanca de profundidad) y derivación de `family` por prefijo | **Funcionan.** Son mecánicos y no admiten juicio |
| Ranking para el tier `author` | **Un candidato como mucho**: el modelo que ejecutó el Hito 2 |
| Ranking para el tier `gate` | **Ninguno.** La regla exige historial probado y familia distinta de la de `author`; media docena de unidades no es historial probado. `config/model_tiers.json` líneas 24–27 conservan `"model": null` |

Esto no invalida la unidad; fija su lugar (última) y su expectativa.

### D8 — `P5` alimenta a `P4`, y por eso va antes

`P4` deriva los `globs:` de los `.mdc` de las condiciones de carga de las reglas. Hoy son prosa en la tabla *Rule Contexts* de `agents.md §0` (11 filas, una por fichero en `rules/`; verificado: `rules/` contiene exactamente 11 `.md`). Un generador que parsee esa prosa sería un parser de lenguaje natural sobre un documento de gobernanza — frágil por construcción. `P5` la convierte en `config/rule_triggers.json` y `P4` lee ese fichero.

**Decisión sobre el consumidor de validación:** `config/rule_triggers.json` **no** recibe script validador propio. Se añade una comprobación dentro de `scripts/verify_references.py`, que ya está en el target `verify` del `Makefile` (línea 52) y ya declara `invoked_by: Makefile 'verify' target` (línea 16). Un script nuevo exigiría invocador nuevo bajo `RA-16`; una comprobación dentro de un verificador existente hereda invocador y cuesta cero.

### D9 — Reparto de roles, y el hueco que lo condiciona

Se planifica para el pipeline nativo de 8 roles (`agents.md §6`) **durante el Hito 1**, autorizado por el humano. Durante el Hito 2 el modo es `sequential` y rige `D4c`.

| Tipo de fichero | Rol | Base |
| :--- | :--- | :--- |
| `scripts/`, `hooks/` en raíz del framework | `devops_agent` | `agents.md §6`: tenedor **único** de `Write`/`Edit` sobre esos dos árboles (`F-086-A1`) |
| `agents.md`, `rules/`, `config/` de gobernanza | `rule_validator` | Auditor de reglas; el cambio es normativo |
| `workflows/`, `docs/roadmaps/` | `orchestrator` | Autor de roadmap y jerarquía |
| `tests/` | `devops_agent` **(desviación de este sprint, ver abajo)** | `tester_agent` no tiene `Write`/`Edit`; no existe perfil implementador (`F-021-A2`) |
| `docs/sprints/026-core-pipeline/` | `principal_agent` / `orchestrator` según artefacto | `config/artifact_registry.json`, columnas `role` |
| Puertas post-ejecución | `qa_agent` + `tester_agent` **emiten el veredicto**; `orchestrator` lo **transcribe** a `SPRINT_LOG.md` | Doble puerta, contexto fresco. Bajo Cursor: `D4c` |

**Corrección sobre autoridad de puerta, medida.** `agents/qa_agent.md` y `agents/tester_agent.md` declaran ambos `tools: Read, Glob, Grep, Bash` — sin `Write`/`Edit` — y `config/artifact_registry.json` nombra el `role` de `SPRINT_LOG.md` como **Orchestrator**. Una fila que asignara a las propias puertas la escritura de su veredicto sería, por tanto, inejecutable. La corrección es una ruta de transcripción, no una queja de permisos: **la puerta emite el veredicto; `orchestrator` lo transcribe a `SPRINT_LOG.md`.** La concesión de solo lectura de las puertas es deliberada y este sprint no la toca — una puerta que puede editar lo que juzga deja de ser una puerta. Esta misma corrección se aplica en `G1.q`, `G1.t` y `A3` donde nombran quién escribe.

**Desviación registrada, no constitucional.** El humano decidió, para este sprint, que `tests/` se asigna a `devops_agent`: `tester_agent` no puede escribir y no existe perfil implementador (`F-021-A2`). **`agents.md §6` no se enmienda** por esta decisión — la desviación vive en este registro de sprint, no en la constitución.

**`F-021-A2` es visible en esta tabla y se declara, no se disimula:** no hay perfil implementador, así que `devops_agent` absorbe todo el código de este sprint — incluidos sus tests, por la desviación registrada arriba — por ser el único con `Write` sobre `scripts/`, `hooks/` y, para este sprint, `tests/`. Es la misma consecuencia que el finding midió sobre el Sprint 023. No se resuelve aquí (rediseñar el mapa de roles no cabe montado sobre un sprint de portabilidad — argumento de la línea 532 del fichero de findings).

---

## Work

Una fila por unidad. Una unidad es un commit atómico (`RA-08`) cuyo sujeto estructural es **un fichero físico** (`agents.md §2 jurisdictional_lock`). Todo commit lleva el sufijo `#026` (`agents.md §5 historical_log`).

---

### HITO 1 — Bootstrap, ejecutado bajo Claude Code, pipeline nativo de 8 roles

**Criterio de finalización del hito:** la Puerta de Migración pasa entera.

#### H1.a — Estado y sesión

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `docs/active_state.json` | modify | low | `devops_agent` | ⏳ |
| P8 | `scripts/session_state.py` | modify | **high** | `devops_agent` | ⏳ |
| P8.1 | `tests/test_session_protocol.py` | modify | medium | `tester_agent` | ⏳ |
| P2 | `scripts/session_state.py` | modify | medium | `devops_agent` | ⏳ |
| P8.2 | `workflows/start_workflow.md` | modify | medium | `orchestrator` | ⏳ |
| P2.1 | `workflows/start_workflow.md` | modify | medium | `orchestrator` | ⏳ |

- **A1** — Operación: fijar cuatro campos de `docs/active_state.json`: `current_sprint.id: 26`, `current_sprint.last_audit_sprint: 23`, `resume_pointer.branch: "ai-sprint/026"`, `resume_pointer.at: <SHA del primer commit de la rama>`. `current_sprint` no tiene escritor por `start_workflow.md:21`, así que se edita a mano; el resto por script donde el script lo posea. **Done-criterion**: `python3 scripts/session_probe.py` no emite el aviso de desajuste ancla-vs-rama, y `python3 -c "import json;d=json.load(open('docs/active_state.json'));assert d['current_sprint']['id']==26 and d['resume_pointer']['branch']=='ai-sprint/026'"` sale `0`. Se ejecuta **después** de crear `ai-sprint/026` en Phase 3, porque `resume_pointer.at` necesita un SHA que aún no existe.
- **P8** — Operación: en `scripts/session_state.py:194` cambiar `required=True` por `required=False, default=None`; en `claim()` generar un UID con forma `<UTC ISO-8601 compacto>-<PID>` cuando el argumento llegue `None`; añadir `--tool` con opciones `claude-code|cursor|terminal` y defecto `terminal`; escribir `session_tool` junto a `session_id` (hoy línea 149). **Done-criterion**: `python3 scripts/session_state.py claim` sin argumentos sale `0` y deja `session_id` no vacío y `session_tool` presente; dos `claim` consecutivos con UIDs distintos y sin `--takeover` siguen saliendo `2`.
- **P8.1** — Operación: añadir a `tests/test_session_protocol.py` cuatro tests nombrados: `test_claim_without_session_id_generates_uid`, `test_claim_records_session_tool`, `test_collision_guard_holds_for_generated_uids`, `test_claim_over_suspended_state_resumes`. El cuarto protege el mecanismo de `D0b`, del que depende la migración entera. **Done-criterion**: los cuatro fallan contra `b5bfb6a` y pasan tras `P8`; `python3 -m pytest tests/test_session_protocol.py -q` sale `0`.
- **P2** — Operación: añadir el campo `delegation_mode` con valores `native|sequential`, escrito por `claim` a partir de `--delegation-mode`, cuyo defecto se deriva de `--tool` (`cursor` → `sequential`, resto → `native`). **Done-criterion**: `python3 scripts/session_state.py claim --tool cursor` deja `delegation_mode: "sequential"` en `docs/active_state.json`. Commit separado de `P8` sobre el mismo fichero físico (`RA-08`).
- **P8.2** — Operación: reescribir la celda `state_claim` de `workflows/start_workflow.md:20` para documentar el argumento opcional, `--tool`, y qué valor pasar bajo cada herramienta; y la celda `bridge_check` (línea 25) para que nombre el lock por target que `P10` introduce. **Done-criterion**: `python3 scripts/scan_workflow_determinism.py .` sale `0`; `python3 scripts/map_workflows.py --check` sale `0` tras `P1.1`.
- **P2.1** — Operación: reescribir la celda `delegation_conflict` de `workflows/start_workflow.md:28` para que lea `delegation_mode` del ancla y trate `sequential` como configuración leída y no como incidente, **conservando** la obligación de reportar al humano cuando el modo declarado y la capacidad real difieran. **Done-criterion**: la celda nombra `delegation_mode` y `docs/active_state.json` por ruta, y contiene la frase literal "reports the mismatch to the human" como mecanismo de aviso — `grep -c "reports the mismatch to the human" workflows/start_workflow.md` devuelve al menos `1` dentro de la celda `delegation_conflict`, preservando así el precedente del Obstáculo 2 (roadmap líneas 974–978: la fase de puerta que nunca corrió y nadie reportó). Commit separado de `P8.2` sobre el mismo fichero físico.

#### H1.b — Instalador y el censo de referencias

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P3.0 | `scripts/install.py` | create (`git mv` desde `scripts/install_claude.py`) | **high** | `devops_agent` | ⏳ |
| P3.1 | `scripts/install.sh` | create (`git mv` desde `scripts/install_claude.sh`) | medium | `devops_agent` | ⏳ |
| P3.1b | `scripts/install_claude.sh` | create (shim de deprecación) | low | `devops_agent` | ⏳ |
| P3.2 | 29 ficheros de Clase A, enumerados abajo | modify | **high** | por jurisdicción | ⏳ |
| P3.3 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | ⏳ |
| P10 | `scripts/install.py` | modify | medium | `devops_agent` | ⏳ |
| P10.1 | `.gitignore` | modify | low | `devops_agent` | ⏳ |

- **P3.0** — Operación: `git mv scripts/install_claude.py scripts/install.py`; añadir `--target` con opciones `claude|cursor|both` y defecto `claude`; actualizar su docstring `invoked_by:` (línea 3) y las dos cabeceras que el script escribe en ficheros generados (líneas 207 y 251). **Done-criterion**: `python3 scripts/install.py --help` lista `--target` con las tres opciones; `python3 scripts/install.py --target claude` en el sandbox produce el mismo árbol `.claude/` que `b5bfb6a`, verificado con `diff -r`.
- **P3.1b** — Operación: dejar `scripts/install_claude.sh` con dos líneas: un `echo` a **`stderr`** con el texto de deprecación y la fecha de retirada, y `exec` sobre `scripts/install.sh` pasando `"$@"`. A `stderr` y no a `stdout`, que rompería a cualquier consumidor que parsee la salida. **Done-criterion**: `bash scripts/install_claude.sh --help` sale `0` y emite la línea de deprecación en `stderr`.
- **P3.2 — censo completo, medido con `grep` sobre todo el árbol.** Clase A, **32 ficheros** (29 enumerados en la tabla que sigue + 2 renombrados por `P3.0`/`P3.1` + 1 gestionado por `P3.3`):

  | Jurisdicción | Ficheros y líneas | Rol |
  | :--- | :--- | :--- |
  | Código ejecutable | `hooks/on_init.py:16` · `hooks/on_commit_msg.py:14` · `scripts/merge_json.py:4` · `scripts/_root.py:71` · `scripts/_mode.py:4,26` · `scripts/render_readme.py:3,66,113` · `scripts/verify_references.py:160` · `skills/compliance-checker/scripts/distill.py:10` | `devops_agent`; el último, `skill_architect` |
  | Tests | `tests/test_installer.sh:31,67,83,93,112` · `tests/test_mass_standardizer.py:297` · `tests/test_invocation_coverage.py:70` · `tests/test_root_resolution.py:57` | `tester_agent` |
  | Configuración | `claude/settings.hooks.json:16` · `config/invocation_exceptions.json:55` · `.gitignore:100` | `devops_agent` |
  | Gobernanza | `agents.md:77,83,110,163` | `rule_validator` |
  | Workflows | `workflows/start_workflow.md:23,25` · `workflows/audit_workflow.md:18` | `orchestrator` |
  | Documentación pública | `README.md:60,101,107,123,164,198` · `SECURITY.md:17` · `.github/ISSUE_TEMPLATE/bug_report.yml:26` | `orchestrator` |
  | Documentación interna | `docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md:41` · `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md:12,21,70,81,83` · `docs/architecture/global_topology.md:53` · `docs/architecture/topology_map.md:17,21` · `docs/plans/README.md:51` | `orchestrator` |
  | Skills de primera parte | `skills/slash-commander/SKILL.md:12,30` · `skills/slash-commander/README.md:49` · `profiles/example-project/README.md:18` | `skill_architect` |

  **`skills/slash-commander/` es editable**: `rules/skills_and_integrations.md §3 Skill Documentation Veto` prohíbe modificar documentación de *skills externas importadas*; `slash-commander` es de primera parte y no lleva sufijo `-3rd`. Verificado leyendo la regla.

  **Clase B — NO SE TOCA** (8 ficheros): `CHANGELOG.md` · `docs/sprints/023-core-pipeline/task_scope.md`, `SPRINT_LOG.md` · `docs/sprints/025-core-pipeline/IMPLEMENTATION_PLAN.md` · `docs/roadmaps/core/pipeline/014-…`, `015-…`, `018-…`, `019-…`.

  **Mitigación de `jurisdictional_lock`, por precedente.** Los **29 ficheros** de la tabla exceden el límite de un fichero por subtarea. Se aplica el patrón que la línea 920 del roadmap registra para `C0.3` del Sprint 023: `P3.0` se entrega y se prueba primero, y después **cada fichero es una subtarea independiente de un fichero**, despachadas por jurisdicción. **Done-criterion de `P3.2`**: `grep -rn "install_claude" . --include='*' | grep -v -e CHANGELOG.md -e docs/sprints/ -e 'docs/roadmaps/core/pipeline/01'` devuelve **exactamente una línea**: la del shim `scripts/install_claude.sh`.
- **P3.3** — Operación: reescribir la línea 1284 de `docs/roadmaps/core/pipeline/021-030-program-queue.md` para marcar como ya resuelta por `026` la unidad del Sprint 029 sobre `README.md:60`. **Done-criterion**: la línea 1284 ya no propone trabajo sobre `README.md:60`; la línea 1238 (`U3`, Sprint 030) permanece sin cambios salvo el nombre del fichero.
- **P10** — Operación: en `scripts/install.py`, sustituir el nombre único de lock por `.bridge_claude.lock` y `.bridge_cursor.lock`, escritos según `--target`. **Done-criterion**: `--target both` deja los dos ficheros; `--target cursor` deja solo `.bridge_cursor.lock`; el comparador de `bridge_check` lee el lock de su target y `bash tests/test_installer.sh` sale `0`.
- **P10.1** — Operación: sustituir `.gitignore:75` (`.claude_bridge.lock`) por las dos entradas nuevas. **Done-criterion**: `git status --porcelain` vacío tras `python3 scripts/install.py --target both`.

#### H1.c — Guardas portables (precondición de la migración, no consecuencia)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P9 | `hooks/on_push.py` | create | **high** | `devops_agent` | ⏳ |
| P9.1 | `scripts/install.py` | modify | medium | `devops_agent` | ⏳ |
| P9.2 | `tests/test_on_push.py` | create | medium | `tester_agent` | ⏳ |
| A4.1 | `hooks/on_commit.py` | modify | low | `devops_agent` | ⏳ |
| A4.2 | `hooks/on_init.py` | modify | low | `devops_agent` | ⏳ |
| A4 | `scripts/verify_references.py` | modify | **high** | `devops_agent` | ⏳ |

- **P9** — Operación: crear `hooks/on_push.py` con docstring `invoked_by: .git/hooks/pre-push, installed by scripts/install.py.` (forma idéntica a `hooks/on_commit_msg.py:14`), que rechace `git push --force`, `git push -f` y todo push que reescriba historia sobre una referencia existente. **Sale con `sys.exit(1)`, no `2`**: `RA-11` gobierna los hooks `PreToolUse` de Claude Code; este es un hook de git, donde bloquea cualquier valor distinto de cero y `2` no tiene significado especial. Se declara en el docstring para que nadie lo "corrija" a `2` por analogía. `rm -rf /` **no se cubre** y el docstring lo declara guardarraíl exclusivo de Claude Code (roadmap línea 984). **Done-criterion**: en un remoto de sandbox, `git push --force` sale distinto de `0` con el hook instalado y `git push` normal sale `0`.
- **P9.1** — Operación: instalar `hooks/on_push.py` como `.git/hooks/pre-push` desde `scripts/install.py`, por el mismo camino que ya instala `pre-commit` y `commit-msg`. **Done-criterion**: tras `python3 scripts/install.py --target cursor` en el sandbox, `.git/hooks/pre-push` existe y es ejecutable. Tercer commit sobre `scripts/install.py`, separado de `P3.0` y `P10`.
- **P9.2** — Operación: crear `tests/test_on_push.py` con cuatro tests nombrados, por simetría con `P8.1`: `test_force_push_long_flag_rejected` (`git push --force`), `test_force_push_short_flag_rejected` (`git push -f`), `test_history_rewrite_push_rejected` (push que reescribe historia sobre una referencia existente), y `test_normal_push_allowed` (regresión: un push que no reescribe historia debe seguir saliendo `0`). Cada test invoca `hooks/on_push.py` directamente sobre un remoto de sandbox bajo `/private/tmp` y lee `$?`, sin tubería. **Done-criterion**: los cuatro fallan contra `b5bfb6a` (`hooks/on_push.py` no existe) y pasan tras `P9`; `python3 -m pytest tests/test_on_push.py -q` sale `0`. La redacción de las aserciones internas de cada test es trabajo de `tester_agent` en Phase 6, no de esta unidad de plan.

**Ceguera de puerta medida en el propio `RA-16`, y por qué se repara aquí.** `scripts/verify_references.py:194` recorre `[*sorted(Path("workflows").glob("*.md")), *sorted(Path("scripts").glob("*.py"))]` para la comprobación `(d)`. `hooks/` está ausente de ese bucle, así que `(d)` nunca inspecciona un hook para su propia declaración de `invoked_by:` — el comentario que lo precede, *"Workflows and scripts are framework-owned: they declare their own invoker"*, no menciona `hooks/` en absoluto. `hooks/*.py` sí se recorre en `imported_modules()` (línea 164), pero solo para detectar qué otros ficheros importan un hook, nunca para exigirle su propia declaración. `RA-16 INVOCATION_COVERAGE` nombra explícitamente a los hooks (*"No mechanism — workflow, script, executable skill, **hook** or gate — merges without a declared, verifiable invoker"*), y medido en `b5bfb6a`: de los seis ficheros de `hooks/`, tres no declaran `invoked_by:` — `hooks/on_commit.py`, `hooks/on_init.py`, `hooks/__init__.py` — y `make verify` sale `0` hoy. Es la misma firma de fallo que este programa viene persiguiendo — una puerta que reporta verde sobre un dominio que nunca inspeccionó — y ocurre dentro del mismo mecanismo que `RA-16` creó para impedirlo. Se descubrió porque `P9` crea `hooks/on_push.py` y una versión anterior de este plan daba por hecho que `scripts/verify_references.py` probaría su cumplimiento de `RA-16`. No lo habría hecho: `hooks/on_push.py` habría caído en el mismo punto ciego que los tres ficheros ya medidos.

**Orden de aterrizaje, obligatorio.** `A4.1` y `A4.2` aterrizan **antes** que `A4`. Si `A4` aterrizara primero, `make verify` saldría en rojo en el mismo commit, porque `hooks/on_commit.py` y `hooks/on_init.py` seguirían sin `invoked_by:` en el momento en que la comprobación empezara a exigirlo.

- **A4.1** — Operación: añadir al docstring del módulo `hooks/on_commit.py` una línea `invoked_by:`, en la misma forma que `hooks/on_commit_msg.py:14`, nombrando su invocador real. **Done-criterion**: `grep -c 'invoked_by' hooks/on_commit.py` devuelve al menos `1` y el invocador nombrado existe en el árbol. Aterriza antes que `A4`.
- **A4.2** — Operación: añadir al docstring del módulo `hooks/on_init.py` una línea `invoked_by:`, en la misma forma que `hooks/on_commit_msg.py:14`, nombrando su invocador real. **Done-criterion**: `grep -c 'invoked_by' hooks/on_init.py` devuelve al menos `1` y el invocador nombrado existe en el árbol. Aterriza antes que `A4`.
- **A4** — Operación: en `scripts/verify_references.py`, añadir `Path("hooks").glob("*.py")` al bucle de la comprobación `(d)` (línea 194) y reescribir el comentario que lo precede para que nombre los tres árboles (`workflows/`, `scripts/`, `hooks/`) en lugar de solo dos. `hooks/__init__.py` se excluye por la propia lógica de la comprobación — un filtro por nombre de fichero (`path.name != "__init__.py"`) junto al filtro ya existente sobre `path.stem in modules` — porque un marcador de paquete Python no es un mecanismo con invocador propio, y ninguna de las cuatro categorías de `VALID_EXCEPTION_REASONS` (`model-invoked`, `vendored-reference`, `human-entry-point`, `one-time`) lo describe con precisión. **Done-criterion**: la comprobación falla cuando un fichero bajo `hooks/` carece de `invoked_by:` y no tiene entrada en `config/invocation_exceptions.json`; `hooks/__init__.py` no la hace fallar; `python3 scripts/verify_references.py` sale `0` solo **después** de que `A4.1` y `A4.2` hayan aterrizado.

#### H1.d — Adaptador de Cursor

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P6 | `workflows/standardization_workflow.md` | modify | low | `orchestrator` | ⏳ |
| P11 | `.gitignore` | modify | low | `devops_agent` | ⏳ |
| P5 | `config/rule_triggers.json` | create | medium | `rule_validator` | ⏳ |
| P5.1 | `scripts/verify_references.py` | modify | medium | `devops_agent` | ⏳ |
| P5.2 | `agents.md` | modify | medium | `rule_validator` | ⏳ |
| P4.0 | `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` | create | **high** | `devops_agent` | ⏳ |
| P4.0b | `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` | modify | low | `devops_agent` | ⏳ |
| P4 | `scripts/cursor_adapter.py` | create | **high** | `devops_agent` | ⏳ |
| P4.1 | `tests/test_installer.sh` | modify | medium | `tester_agent` | ⏳ |

- **P6** — Operación: reescribir la fila de `workflows/standardization_workflow.md:45` para que `.cursor/rules` deje de estar entre *"Other frameworks' files"* propuestos para archivado, y declare que `.cursor/` es un árbol generado por `scripts/install.py --target cursor` y nunca se archiva. `.windsurfrules` y el resto de la fila permanecen. **Done-criterion**: `grep -n "\.cursor" workflows/standardization_workflow.md` devuelve la fila nueva y ninguna que proponga archivarla.
- **P11** — Operación: añadir a `.gitignore` las entradas `.cursor/commands/`, `.cursor/rules/`, `.cursor/mcp.json`, espejando el criterio de `.claude/` de la línea 101. **Done-criterion**: tras `python3 scripts/install.py --target cursor` en el núcleo, `git status --porcelain` está vacío. Commit separado de `P10.1` sobre el mismo fichero físico.
- **P5** — Operación: crear `config/rule_triggers.json` con una entrada por cada uno de los 11 ficheros de `rules/`, cada una con `path`, `globs` (lista de patrones) y `trigger_prose` (la frase actual de la tabla *Rule Contexts* de `agents.md §0`, copiada literal). **Done-criterion**: `python3 -c "import json,glob;d=json.load(open('config/rule_triggers.json'));assert {e['path'] for e in d['rules']}==set(glob.glob('rules/*.md'))"` sale `0`.
- **P5.1** — Operación: añadir a `scripts/verify_references.py` una comprobación `(e)` que falle si el conjunto de `path` en `config/rule_triggers.json` difiere del contenido de `rules/*.md` en cualquiera de los dos sentidos. **Done-criterion**: falla si se borra una entrada del JSON y falla si se añade un fichero a `rules/` sin entrada; `make verify` sale `0` con el árbol correcto.
- **P5.2** — Operación: añadir a la tabla *Rule Contexts* de `agents.md §0` una frase que nombre `config/rule_triggers.json` como la forma legible por máquina de esa misma tabla y declare que la comprobación `(e)` las mantiene sincronizadas. **Done-criterion**: `grep -c "config/rule_triggers.json" agents.md` devuelve al menos `1` dentro de la tabla *Rule Contexts*, probando que la frase fue escrita y no solo que el fichero sigue siendo válido; y `python3 scripts/verify_references.py` sale `0`.
- **P4.0** — Operación: producir una regla desde la UI de Cursor, leer el fichero resultante bajo `.cursor/rules/`, y escribir en `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` las claves de frontmatter observadas, la versión de Cursor y la fecha. **Done-criterion**: el fichero existe y cada clave documentada va acompañada del fragmento literal leído de disco.
- **P4.0b** — Operación: ejecutar la sonda de sensibilidad a mayúsculas de `Design §D6` y anexar su salida literal al mismo fichero, con la decisión que se sigue de ella. **Done-criterion**: el fichero contiene la salida del comando y la decisión.
- **P4** — Operación: crear `scripts/cursor_adapter.py`, importado por `scripts/install.py`, que genere `.cursor/commands/*.md` desde `commands/*.md` (13 ficheros, medido), `.cursor/rules/*.mdc` desde `rules/*.md` (11 ficheros) usando los `globs` de `config/rule_triggers.json` y **únicamente** las claves registradas en `P4.0`, `.cursor/rules/00-constitution.mdc` con `alwaysApply` apuntando a `agents.md`, y `.cursor/mcp.json` desde `claude/mcp.json`. **Done-criterion**: `python3 scripts/install.py --target cursor` deja 13 ficheros en `.cursor/commands/`, **12 en `.cursor/rules/` (11 reglas + la constitución)** y `.cursor/mcp.json` con el mismo conjunto de claves de servidor que `claude/mcp.json`, verificado con `python3 -c` comparando conjuntos. **Invocador (`RA-16`)**: `scripts/install.py` lo importa como módulo — la comprobación `(d)` de `scripts/verify_references.py` resuelve imports de Python, precedente registrado en su propia línea 160 sobre `scripts/merge_json.py`.
- **P4.1** — Operación: añadir a `tests/test_installer.sh` un bloque que ejecute `--target cursor` y `--target both` en el sandbox y verifique los tres árboles y el `pre-push`. **Done-criterion**: el bloque falla contra `b5bfb6a` y pasa tras `P4` y `P9.1`; `bash tests/test_installer.sh` sale `0`.

#### H1.e — La habilitación constitucional de la mitad bajo Cursor

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `workflows/pipeline_workflow.md` | modify | **high** | `orchestrator` | ⏳ |
| P1.1 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerate | low | `devops_agent` | ⏳ |

- **P1** — Operación: reescribir la tabla de las 8 fases de `workflows/pipeline_workflow.md` para que cada fila declare **artefacto, ruta y done-criterion** tomados de `config/artifact_registry.json`, y la columna de rol pase a rotularse `Role (advisory)`. Añadir el párrafo obligatorio de `Design §D4`: «advisory» rige qué perfil redacta, **nunca** si las fases de puerta corren en contexto fresco, obligatorio bajo ambas herramientas. **Done-criterion**: cada fila que produce un artefacto de `scope: sprint` cita el `filename` exacto del registro (7 artefactos, medido); el párrafo sobre las puertas está presente y cita las líneas 974–978 del roadmap; `python3 scripts/map_workflows.py --check` sale `0` tras `P1.1`.
- **P1.1** — Operación: regenerar `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` con `python3 scripts/map_workflows.py`. **Nunca editar a mano** (`agents.md §0`). **Done-criterion**: `python3 scripts/map_workflows.py --check` sale `0`.

#### H1.f — Puerta del Hito 1 (contexto fresco nativo, 8 roles, bajo Claude Code)

| # | Deliverable | Assignee |
| :--- | :--- | :--- |
| G1.q | Veredicto QA sobre las unidades del Hito 1, emitido por `qa_agent` y transcrito por `orchestrator` a `docs/sprints/026-core-pipeline/SPRINT_LOG.md` (`Design §D9`: las puertas no tienen `Write`/`Edit`) | `qa_agent` (veredicto) / `orchestrator` (transcripción) |
| G1.t | Veredicto Tester sobre las mismas unidades, emitido por `tester_agent` y transcrito por `orchestrator` al mismo fichero | `tester_agent` (veredicto) / `orchestrator` (transcripción) |

**Done-criterion**: ambos veredictos son `APPROVED`, `make verify` sale `0`, y ninguna unidad constitucional (`P1`, `P5.2`) queda sin veredicto. Un rechazo entra en `remediation_loop`; al tercer rechazo consecutivo del mismo bloque lógico, escala a `workflows/remediation_workflow.md`.

---

### PUERTA DE MIGRACIÓN — nombrada, observable, y con salida por rechazo

No es un momento: es una secuencia de comandos y **siete observaciones**, cada una con lo que prueba. Se ejecuta después de `G1.q`/`G1.t` y antes de cualquier unidad del Hito 2.

**Secuencia de comandos, en este orden exacto:**

```
# 1 — bajo Claude Code
python3 scripts/session_state.py suspend
python3 scripts/install.py --target cursor
git add -A && git commit -m "chore(bridge): install the Cursor target before the migration #026"
# 2 — cerrar Claude Code, abrir Cursor sobre el mismo directorio
# 3 — bajo Cursor
python3 scripts/session_state.py claim --tool cursor
```

`suspend` y no `release`: `release` sellaría el sprint y escribiría un `last_close_commit` falso que cegaría a `scripts/detect_drift.py` (`Design §D0b`).

| # | Observación | Comando | Qué prueba |
| :--- | :--- | :--- | :--- |
| M1 | El ancla queda `SUSPENDED` tras `suspend` y el `claim` de Cursor la reporta como *resume*, no como colisión | `python3 -c "import json;print(json.load(open('docs/active_state.json'))['status'])"` antes y después | Que la frontera de herramienta usa el `M6` del Sprint 021 y no una toma forzada. Cubre el paso 2 del test de aceptación |
| M2 | `session_id` es un UID generado con forma `<ISO>-<PID>` y `session_tool == "cursor"` | `python3 -c "import json;d=json.load(open('docs/active_state.json'));print(d['session_id'],d['session_tool'])"` | `P8`. **Sin esto no hay sesión de Cursor**: es el bloqueador de día uno, medido en vivo |
| M3 | `delegation_mode == "sequential"` y `start_workflow.md` Phase 2 no reporta `delegation_conflict` como incidente | Lectura del ancla + ejecución de Phase 2 | `P2`/`P2.1`. Prueba que el conflicto estructural es configuración leída y no un alto en cada sesión |
| M4 | `.cursor/commands/` tiene 13 ficheros, `.cursor/rules/` tiene 12, `.cursor/mcp.json` existe | `ls .cursor/commands \| wc -l`, `ls .cursor/rules \| wc -l` | `P4`. Cubre el paso 1 del test de aceptación en modo núcleo |
| M5 | Preguntada, sin que la regla esté en el prompt de la sesión, *"Under `agents.md §2 jurisdictional_lock`, how many physical files may a single instantiated subagent task edit structurally?"*, la sesión de Cursor responde **"one"** o **"1"** — ningún otro número ni una paráfrasis que evada la cifra cuenta como correcta | Pregunta literal en el chat de Cursor, respuesta contrastada carácter a carácter contra el valor de la regla (`agents.md §2`: *"Limit structural editing to `1` single physical file per instantiated subagent task"*) | Que `.cursor/rules/00-constitution.mdc` **realmente** carga la constitución. Una respuesta que no cite `1` es un fallo directo de esta observación, no un matiz de redacción. Sin esto el Hito 2 correría sin gobernanza y nada lo señalaría |
| M6 | `git push --force origin ai-sprint/026` **es rechazado** desde Cursor | El comando, con `$?` leído directamente | `P9`. Cubre el paso 6 del test de aceptación **bajo la herramienta que carece de `permissions.deny`**, que es donde importa |
| M7 | `resume_pointer.at` apunta al último commit del Hito 1 y `python3 scripts/session_probe.py` no señala desajuste | El comando | Que la sesión de Cursor sabe dónde continuar. Junto a `M1`, cierra `A1` |

**Si cualquiera de M1–M7 falla, la migración NO ocurre.** El Hito 2 continúa bajo Claude Code, el fallo se registra con su comando y su salida en `docs/sprints/026-core-pipeline/SPRINT_LOG.md`, y el sprint se cierra declarando la portabilidad **no demostrada** en lugar de declararla lograda. El sprint no se aborta por esto: el Hito 1 sigue siendo trabajo entregable y verificado. Lo que no se hace en ningún caso es cerrar afirmando una propiedad que una observación nombrada negó.

---

### HITO 2 — el resto, ejecutado bajo Cursor

**Modo:** `delegation_mode: sequential`. Las puertas obtienen contexto fresco según `Design §D4c`: chat nuevo de Cursor, con registro obligatorio de herramienta y modelo leído de disco.

| # | File | Operation | Risk | Assignee | Puerta | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P7 | `agents.md` | modify | medium | `rule_validator` | Cursor, chat nuevo | ⏳ |
| P7.1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `rule_validator` | Cursor, chat nuevo | ⏳ |
| A2 | `tests/fixtures/` (sandbox) | create + delete | **high** | `tester_agent` | Cursor, chat nuevo | ⏳ |
| P4.2 | `scripts/audit_cursor_models.py` | create | **high** | `devops_agent` | Cursor, chat nuevo | ⏳ |
| P4.3 | `Makefile` | modify | low | `devops_agent` | Cursor, chat nuevo | ⏳ |
| P4.4 | `config/model_tiers.json` | modify | medium | `rule_validator` | Cursor, chat nuevo | ⏳ |
| A3 | `docs/sprints/026-core-pipeline/SPRINT_LOG.md` | modify | medium | `orchestrator` (transcribe el veredicto de `qa_agent`; `Design §D9`) | — (es la puerta) | ⏳ |

- **P7** — Operación: añadir a `agents.md §3` una fila que declare que el contenido del núcleo alcanzado por symlink (`AGENTS.md` en la raíz de un host apuntando a `.agents/agents.md`) queda **FUERA** del alcance de las puertas documentales del host, y que nombre el mecanismo de exclusión: el host excluye la ruta del symlink en la configuración de su propia puerta. Razón que la fila debe recoger: `agents.md §3 strict_rule` prohíbe al host modificar ese contenido, y una puerta que exige arreglar lo que la ley prohíbe tocar es un rojo insalvable (finding `C5`, línea 713 del fichero de findings). **Done-criterion**: `grep -c "AGENTS.md" agents.md` devuelve al menos `1` dentro de la fila nueva de `agents.md §3`, y esa misma fila contiene también la cadena "excludes the symlink path" (el mecanismo de exclusión nombrado) — probando que la fila fue escrita con su contenido exigido y no solo que el fichero pasa la sintaxis; `python3 scripts/verify_references.py` sale `0`.
- **P7.1** — Operación: marcar `C5` (línea 699) como cerrado en `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` con el commit que lo cierra, **conservando la entrada** (regla 3 de ese fichero). **`F-021-A2` y `F-023-S4` se dejan sin marcar.** **Done-criterion**: `grep -c '^### - \[ \]' docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` disminuye exactamente en 1.
- **A2 — el ejercicio de violación real (paso 5 del test de aceptación).** Operación: en un sandbox de git desechable creado bajo `/private/tmp`, escribir un `Dockerfile` con un secreto de prueba **en forma `ENV` con valor entrecomillado** — que es una forma que `hooks/on_commit.py` **sí** detecta según la medición de `F-023-S4` (`DOCKERFILE_SECRET` con valor entrecomillado) — e intentar el commit desde Cursor. **Done-criterion**: el commit es rechazado con `$?` distinto de `0` y el mensaje del hook nombra el fichero. El sandbox se destruye en la misma sesión. **PROHIBIDO** usar un fichero llamado `.env` o la forma `NAME=value` sin comillas: están medidos como no detectados (`F-023-S4`), el ejercicio pasaría por la razón equivocada y además dejaría un secreto de prueba sin guarda. Esta restricción es la razón por la que el ejercicio es una unidad y no una improvisación.
- **P4.2** — Operación: crear `scripts/audit_cursor_models.py` que abra en **solo lectura** `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb` con `sqlite3` de la biblioteca estándar, lea `…persistentStorage.applicationUser → availableDefaultModels2`, aplique los filtros duros (`supportsAgent == true`, `degradationStatus == 0`, y para el tier `gate` presencia de una palanca de profundidad en `parameterDefinitions`), derive `family` del prefijo del nombre, cruce con el historial del medidor del Sprint 021, y **proponga** asignaciones sin ejecutarlas. Cero red, cero credenciales. Sale `0` con mensaje explícito cuando el fichero SQLite no existe, igual que `platform_probe` se salta sin `gh`. **Done-criterion**: emite una tabla de modelos con su `family` derivada; **ningún modelo aparece propuesto para el tier `gate`**, porque la regla de promoción exige historial probado y `Design §D7` mide que no lo hay; `python3 scripts/audit_cursor_models.py --check` sale `0`. Cubre los pasos 6b y 6c del test de aceptación.
- **P4.3** — Operación: añadir un target `cursor-tiers` al `Makefile` que invoque `scripts/audit_cursor_models.py`. **Done-criterion (`RA-16`)**: el docstring del script declara `invoked_by: Makefile 'cursor-tiers' target.` y `python3 scripts/verify_references.py` sale `0` sin necesitar entrada en `config/invocation_exceptions.json`.
- **P4.4** — Operación: actualizar `config/model_tiers.json`: el bloque `_comment` declara que la columna `cursor` la deriva `scripts/audit_cursor_models.py`, y **por qué los tiers `gate` y `author` siguen con `"model": null`** — un hito de sprint no es historial probado. Se rellena únicamente lo que `P4.2` proponga y el humano acepte. **Done-criterion**: `python3 scripts/check_model_tiers.py` sale `0`; `python3 -c "import json;c=json.load(open('config/model_tiers.json'))['_comment'];assert 'not proven history' in c"` sale `0`, probando que el `_comment` contiene la causa medida (`Design §D7`: un hito de sprint no es historial probado) en lugar de dejar el `null` sin explicación.
- **A3 — el análogo del paso 7, y la puerta final del hito.** Operación: al terminar el Hito 2, ejecutar `python3 scripts/docs_freshness_check.py . 026` y la Phase 2.6 de `close_workflow.md` sobre `docs/sprints/026-core-pipeline/`. Después, la comprobación de indistinguibilidad: **un agente en contexto fresco (`qa_agent`) recibe el directorio del sprint con la columna `Tool` de `SPRINT_LOG.md` ocultada, y se le pide particionar los artefactos entre las dos herramientas.** `qa_agent` emite el veredicto de ambas comprobaciones; **`orchestrator` es quien escribe la fila resultante en `SPRINT_LOG.md`** (`Design §D9`: `qa_agent` no tiene `Write`/`Edit`). **Done-criterion**: el agente en contexto fresco identifica correctamente qué artefactos produjo Cursor, o no lo identifica correctamente — binario, sin margen de azar. **Si acierta, la portabilidad ha fallado**, la diferencia que la delató se nombra por fichero en `SPRINT_LOG.md`, y el sprint no se cierra afirmando portabilidad. Si no acierta, el resultado se registra literal y el sprint puede cerrar afirmándola. Es la formulación operativa de la línea 1094 (*"If the gate can notice the difference, portability has not been achieved"*) y coincide con `Abort criterion §3`, que ya la trata como binaria (*"si acierta"*).

---

## Test de aceptación — qué cubre la reordenación y qué no

La reordenación **elimina la necesidad de dos sprints de juguete y del host desechable**, porque el Hito 2 es una mitad de sprint real ejecutada por Cursor. Cobertura, sin sobreafirmar:

| Paso (roadmap 1102–1112) | Cubierto por | Grado |
| :--- | :--- | :--- |
| 1 — `install.py --target cursor` en un host limpio | `M4` (modo núcleo) + `P4.1` (sandbox de host automatizado en `tests/test_installer.sh`) | **Completo por dos vías distintas**, una de ellas automatizada y repetible |
| 2 — protocolo de arranque desde Cursor, ancla `IN_PROGRESS` con `session_tool` y UID generado | `M1`, `M2`, `M7` | **Completo, y con ejecución real en lugar de simulada** |
| 3 — las fases de autoría dejan cada artefacto del registro en su ruta | Hito 2 | **Parcial, y hay que decirlo.** Los artefactos de Phase 1 a 4.3 se producen **antes** de la migración, bajo Claude Code, porque `task_scope.md` debe existir antes de ejecutar. Cursor produce realmente: las entradas de `SPRINT_LOG.md`, `PHASE_REGISTER.md`, la entrada de `CHANGELOG.md`, `graph_stats.json` y sus propios commits. **Cobertura completa requiere un sprint cuyas Fases 1–4 corran bajo Cursor; destino nombrado: Sprint 027** |
| 4 — puertas en contexto fresco, y el registro lo prueba | Puertas del Hito 2 con el registro obligatorio de `D4c` | **Cubierto.** La derogación humana del carve-out constitucional elimina la única excepción; todas las unidades del Hito 2 se puertan igual |
| 5 — un commit que viola una puerta es rechazado, con una violación **real** | `A2` | **Completo**, y sigue siendo ejercicio deliberado |
| 6 — `git push --force` rechazado | `M6`, bajo Cursor | **Completo, y en el lugar correcto** — bajo la herramienta que no lee `permissions.deny` |
| 6b, 6c — familias derivadas y filtros duros | `P4.2` | **Completo** |
| 7 — los dos árboles son indistinguibles salvo `session_tool` | `A3` | **Sustituido, no cubierto literalmente.** Ya no hay dos árboles comparables: hay **uno** cuyas dos mitades produjeron herramientas distintas. `A3` prueba la misma propiedad por partición ciega en lugar de por `diff`. Más fuerte en realismo, más débil en simetría. Afirmar que `A3` es el paso 7 sería la clase de sobreafirmación que este sprint existe para eliminar |

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | `P4.2` usa `sqlite3` y `json` de la biblioteca estándar; `P4` usa `pathlib` y `json`; `P9` usa `subprocess` y `sys`. No se añade ninguna dependencia. |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Generación de `.cursor/` desde `commands/`, `rules/` y `claude/mcp.json` | script (`scripts/cursor_adapter.py`) | `scripts/install.py` lo importa como módulo — resuelto por la comprobación `(d)` de `scripts/verify_references.py`, que resuelve imports |
| Rechazo de `git push --force` bajo cualquier herramienta | git hook (`hooks/on_push.py`) | `.git/hooks/pre-push`, instalado por `scripts/install.py` — declarado en el docstring |
| Sincronía entre `config/rule_triggers.json` y `rules/*.md` | comprobación `(e)` dentro de `scripts/verify_references.py` | `Makefile 'verify' target`, ya declarado en ese fichero (línea 16) |
| Propuesta de tiers de Cursor | script (`scripts/audit_cursor_models.py`), **propone y no ejecuta** | `Makefile 'cursor-tiers' target` (`P4.3`) |
| Generación de UID de sesión sin harness | script (`scripts/session_state.py claim`) | `workflows/start_workflow.md` Phase 0.5 `state_claim`, ya declarado |
| Registro de la herramienta y el modelo que ejecutó cada puerta del Hito 2 | **determinista**: lectura por `python3 -c` de `cursor/applicationOpenModelAppliedConfig` en `state.vscdb`, escrita en `SPRINT_LOG.md` | Paso obligatorio de cada puerta del Hito 2 (`Design §D4c`). No es atestiguación humana |
| Verificación del esquema `.mdc` | **juicio de agente, deliberado y de una sola vez** | `P4.0`. **No es recurrente**: no existe alternativa determinista porque el esquema hay que leerlo de un fichero que Cursor produce; una vez registrado, el generador ya es determinista |
| Partición ciega de artefactos por herramienta (`A3`) | **juicio de agente, de una sola vez, y es el punto** | Puerta final del Hito 2. Una comprobación determinista aquí sería un `diff`, y `diff` es justamente lo que la reordenación deja de tener disponible |

---

## Tests

**Reproducir antes de reparar.** Un test que pasa contra el árbol actual no prueba nada sobre un defecto que se afirma presente en él.

**Línea base verde, medida por `devops_agent` en `b5bfb6a`** (Phase 2 del pipeline), antes de que exista ninguna unidad de este plan:

- `make verify` sale `0` y ese único comando ya cubre **428 tests pasados** (0 fallidos, 0 omitidos) más `tests/test_installer.sh`.
- `python3 scripts/session_state.py claim --help` imprime `usage: session_state.py claim [-h] --session-id SESSION_ID [--takeover]` — el bloqueador de día uno, confirmado en su forma literal.
- `hooks/` contiene `__init__.py`, `on_commit.py`, `on_commit_msg.py`, `on_init.py`, `state_mirror.py`, `telemetry.py`. Ningún `on_push.py`.
- `find . -name ".cursor" -type d` no devuelve nada.
- `python3` y `venv_skillopt/bin/python3` son ambos **3.13.13**. Sin riesgo de intérpretes cruzados para el trabajo de `sqlite3` y `argparse`.
- Sin configuración de Docker en el núcleo; las cadenas "Docker" del árbol son fixtures de la puerta de escaneo de secretos.

La columna "¿Falla contra el árbol actual?" de la tabla siguiente descansa por tanto en una medición, no en una afirmación.

| Check | Fails against the current tree? |
| :--- | :--- |
| `python3 scripts/session_state.py claim` sin `--session-id` sale `0` | **Sí — este es el defecto.** Hoy sale `2` con `error: the following arguments are required: --session-id` (`scripts/session_state.py:194`) |
| `docs/active_state.json` contiene `session_tool` | **Sí — este es el defecto.** El campo no existe |
| `docs/active_state.json` contiene `delegation_mode` | **Sí — este es el defecto.** El campo no existe |
| `python3 scripts/install.py --target cursor` sale `0` | **Sí — este es el defecto.** `scripts/install.py` no existe |
| `grep -rn "install_claude" README.md agents.md SECURITY.md` no devuelve nada | **Sí — este es el defecto.** Devuelve 11 líneas |
| `.cursor/commands/` contiene 13 ficheros tras instalar | **Sí — este es el defecto.** `.cursor/` no existe (glob medido) |
| `git push --force` es rechazado por un hook de git | **Sí — este es el defecto.** `hooks/` no contiene `on_push.py` |
| `config/rule_triggers.json` existe y cubre los 11 ficheros de `rules/` | **Sí — este es el defecto.** El fichero no existe |
| `workflows/standardization_workflow.md` no propone archivar `.cursor/rules` | **Sí — este es el defecto.** La línea 45 lo propone |
| `docs/active_state.json` declara `current_sprint.id: 26` | **Sí — este es el defecto.** Declara `23` |
| `claim` sobre un ancla `SUSPENDED` procede y reporta un resume | **No — es una regresión que proteger.** Funciona hoy (`start_workflow.md:23`) y `P8` no debe degradarlo. **De ello depende la migración entera** |
| `claim --session-id X` seguido de `--session-id Y` sin `--takeover` sale `2` | **No — es una regresión que proteger.** La guarda de colisión funciona hoy |
| `python3 scripts/install.py --target claude` produce el mismo árbol `.claude/` que `b5bfb6a` | **No — es una regresión que proteger.** El renombrado no debe cambiar el comportamiento por defecto |
| `bash tests/test_installer.sh` sale `0` | **No — es una regresión que proteger.** Pasa hoy y debe seguir pasando tras `P3`, `P9.1` y `P10` |
| `python3 scripts/check_readme_counts.py` sale `0` | **No — es una regresión que proteger.** Cuenta `commands/*.md`, `agents/*.md`, `rules/*.md` y directorios de `skills/`; ninguna unidad añade o quita ficheros ahí, y si alguna lo hiciera este check lo delataría |

---

## Verification

Códigos de salida leídos con `$?` directamente, **nunca a través de una tubería**, que reporta el código del último comando de la tubería. **No existe target `make test`**: los cuatro targets declarados en el `Makefile` son `graphify-update` (línea 29), `graphify-rebuild` (33), `verify` (45) y `docs-freshness-check` (90); `pytest` y `tests/test_installer.sh` corren dentro de `verify`.

| Command | Expected | Cuándo |
| :--- | :--- | :--- |
| `make verify` | `0` | Puerta del Hito 1 y cierre |
| `python3 scripts/verify_references.py` | `0`. `RA-16`: `scripts/cursor_adapter.py` y `scripts/audit_cursor_models.py` declaran invocador. `hooks/on_push.py` declara `invoked_by:` en su docstring (`P9`), pero la comprobación `(d)` solo lo verifica **si `A4` ha aterrizado** — antes de `A4` el bucle de `(d)` no recorre `hooks/`, y esta salida en `0` no es evidencia de cumplimiento de `RA-16` para ningún fichero de `hooks/` | Puerta del Hito 1 y cierre |
| `python3 scripts/map_workflows.py --check` | `0` tras regenerar. `P1`, `P2.1`, `P6` y `P8.2` modifican workflows | Puerta del Hito 1 |
| `grep -rn "install_claude" . --include='*' \| grep -v -e CHANGELOG.md -e docs/sprints/ -e 'docs/roadmaps/core/pipeline/01'` | Exactamente **1** línea: el shim | Puerta del Hito 1 |
| `python3 scripts/install.py --target both && ls .bridge_claude.lock .bridge_cursor.lock` | Ambos presentes; `git status --porcelain` vacío después | Puerta del Hito 1 |
| **Observaciones `M1`–`M7`** | Cada una con su salida registrada en `SPRINT_LOG.md` | **Puerta de Migración** |
| `python3 scripts/docs_freshness_check.py . 026` | `0` | `A3` y cierre |
| `python3 scripts/submodule_purity.py` | `0`. Sesión de núcleo: la jurisdicción es este repositorio (`agents.md §3 jurisdiction`) | Cada commit y cierre |
| `git status --porcelain` | Vacío al cierre | Cierre |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `F-023-S4` — el `.env` literal que pasa `hooks/on_commit.py` | Decisión humana del 2026-08-24 (roadmap líneas 64–88): `RA-03 HOTFIX_FLAT` **después** de `026`. Destino: `docs/hotfixes/[H-ID]-secrets.md`. **Coste aumentado bajo esta ordenación**: el Hito 2 corre bajo Cursor, donde esa puerta ciega es la única que existe |
| `F-021-A2` — 8 perfiles con `Write` y ningún implementador | Rediseño del mapa de roles; no cabe montado sobre un sprint de portabilidad. `P1` lo roza y declara que no lo cierra. Destino: sprint propio, a proponer tras `030` |
| Skills bajo `.cursor/` | Cursor no tiene primitiva equivalente y su contenido es prosa legible (roadmap línea 1016) |
| Cobertura de `rm -rf /` bajo Cursor | No cubrible por un hook de git. Declarado guardarraíl exclusivo de Claude Code en el docstring de `hooks/on_push.py` (roadmap línea 984) |
| Refresco del espejo del ancla a mitad de sesión bajo Cursor | `claim`/`release` lo refrescan en los bordes, no en medio (roadmap línea 987). Destino: Sprint 027 |
| `settings.json` de Claude Code | Sprint 027 (`autonomy-posture`) |
| Cobertura completa del paso 3 del test de aceptación (Fases 1–4 bajo Cursor) | Imposible en este sprint: `task_scope.md` debe existir antes de ejecutar. Destino nombrado: **Sprint 027** |
| `install.py --profile <path>` fuera del submódulo | Unidad `U3` del Sprint 030 (roadmap línea 1238) |
| Reescritura de menciones históricas a `install_claude.*` | `workflows/standardization_workflow.md:43`: *"History is never rewritten"* |
| Ediciones a `skills/*-3rd/` | `rules/skills_and_integrations.md §3 Skill Documentation Veto` |

---

## Abort criterion

Las cuatro observaciones que detienen este sprint, decididas **antes** de que empiece la ejecución.

**1. El bloqueador de día uno no se resuelve.** Si tras `P8` el comando `python3 scripts/session_state.py claim` sin `--session-id` no sale `0`, o sale `0` pero degrada la guarda de colisión, **o si `claim` sobre un ancla `SUSPENDED` deja de reportar un resume**, el sprint se detiene. Sin eso no hay Phase 0.5 bajo Cursor ni migración posible. Se revierte la rama completa y se replantea `P8` antes de tocar nada más.

**2. Se escribe un fichero con forma `NAME=value` sin comillas, en cualquier unidad y bajo cualquier herramienta.** `F-023-S4` está medido y abierto durante todo este sprint, y bajo Cursor la puerta ciega es la única guarda que existe. Si una unidad necesita un fichero de ejemplo con esa forma, el sprint se detiene y el hotfix `RA-03` se adelanta por delante de `026`, invirtiendo la decisión del 2026-08-24 con su razón registrada. `A2` está escrita específicamente para no caer en esto.

**3. `A3` identifica la partición por herramienta.** Si el agente en contexto fresco acierta qué artefactos produjo Cursor sin consultar la columna `Tool`, el sprint **no se revierte** pero **no se cierra**: la diferencia se mide, se nombra el fichero que la produce, y se decide con el humano si es una unidad más o una limitación declarada.

**4. Alguna unidad escribe un esquema de frontmatter `.mdc` que no se leyó de un fichero producido por Cursor.** Aborto inmediato de esa unidad y revisión de las demás. Con Cursor disponible ya no hay excusa de indisponibilidad.

---

## Recomendación de alcance

El **Corte A** de la revisión 1 (diferir `P4.2`–`P4.4`) **se retira**: bajo la nueva ordenación esas tres unidades caen al final del Hito 2, ejecutadas bajo la propia herramienta cuyo catálogo leen, y después de que el Hito 2 haya producido las primeras mediciones de coste por unidad aceptada bajo Cursor. Sacarlas a un sprint aparte las alejaría de sus datos.

`Design §D7` sigue en pie sin atenuar: el día de la entrega la mitad de ranking no podrá proponer **ningún** modelo para el tier `gate`. Lo que sí cambia es que `P4.4` deja escrita **la causa medida** de ese `null`.

| Opción | Contenido | Coste |
| :--- | :--- | :--- |
| **(a) Ejecutar las once unidades** | Hito 1 + Puerta de Migración + Hito 2 completo, `P4.2`–`P4.4` al final | El sprint es largo. `P4.2` se entrega con su mitad de ranking casi inerte, **declarado y con la causa escrita** |
| **(b) Diferir `P4.2`–`P4.4`** | Hito 2 termina en `A3` | `config/model_tiers.json` conserva su columna `cursor` en `null` **sin explicación escrita**, que es el estado actual |

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Human operator, autorización atendida única en Phase 5 |
| **Date** | 2026-08-24 |
| **Plan commit at approval** | `1da9641` en `ai-sprint/026`. El texto aprobado es el de ese commit, no el de `c07bc46`, que precede al parche de `A4`, `A3`, los cinco done-criteria y `Design §D9` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 es una única autorización humana atendida. NO DEBE envolverse en un `/loop` desatendido. Bajo esta ordenación, la aprobación cubre **ambos** hitos y la Puerta de Migración; no se abre una segunda puerta de aprobación al migrar, porque la migración es una observación verificable y no una renegociación del alcance.*
