# Implementation Plan: Sprint 041 — bi-harness-bridge-parity

**Canonical path**: `docs/sprints/041-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/041` · **Base**: `main` at `d258b43`
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

Este repositorio se trabaja **desde dos harnesses**: Claude Code y Cursor, de forma
alternada sobre el mismo árbol. El Sprint 040 (`cursor-bridge-incremental`) dejó la
rama Cursor del arranque completa. La rama Claude **no se implementó**, y el arranque
reporta éxito igualmente.

### La frase que lo diagnostica está en el propio código

`hooks/on_init.py:5-7` declara su contraparte:

> *"`SessionStart` does not run in the nucleus — portable counterpart is
> `workflows/start_workflow.md` Phase 1.5 `bridge_check` (`F-026-A3`)."*

Esa contraparte portable es `scripts/session_start.py --boot`. `on_init.py` tiene
`bridge_intact()` (línea 82) — verifica que los artefactos enlazados sobrevivan en
disco, **independientemente del lock**. `session_start.py` no lo tiene ni lo importa.
El mecanismo existe; nunca se cableó al arranque portable.

### Medición — mismo commit, mismo comando, solo cambia `--tool`

Reproducido 2026-08-30 sobre un clon limpio en `$SCRATCH/repro` (`d258b43`), sin
`.claude/` ni `.cursor/` (ambos están en `.gitignore`):

```
git clone -q /Users/gstmirabal/Developer/.agents "$SCRATCH/repro"
cd "$SCRATCH/repro" && python3 scripts/session_start.py --boot --tool claude-code
```

| `--tool` | Salida decisiva | Mirror tras el boot | Git hooks instalados | Exit |
| :--- | :--- | :--- | :--- | ---: |
| `claude-code` | `boot: bridge lock refreshed to d258b43e1ce7 (content fresh).` | **`.claude/` inexistente** | **ninguno** | `0` |
| `cursor` | `✅ Cursor bridge written under …/.cursor` | `.cursor/` completo | `pre-commit`, `commit-msg`, `pre-push` | `0` |

El boot Claude declaró *"content fresh"* sobre un checkout **sin directorio `.claude/`
en absoluto**. Y como `_refresh_bridge_lock` deja el lock igual a `HEAD`,
`_lock_stale()` devuelve `False` en todo arranque posterior hasta que el tip se mueva:
**no reintenta nunca**. Es un verde falso que se autosella.

El daño no se limita al bridge. `scripts/install.sh` es quien instala los git hooks
— el escáner de secretos, el gate `#[Sprint_ID]` y el bloqueo de force-push. En un
checkout arrancado solo desde Claude **no se instala ninguno**, con el arranque
saliendo `0`. Es un control de seguridad reportando conforme, la misma clase de
defecto que `F-087-P1` (*ausente ≠ deshabilitado*).

### Causa mecánica

`scripts/session_start.py:245-251`:

```python
def _commands_body_stale(root: Path, target: str) -> bool:
    if target != "cursor":
        return False        # Claude nunca puede estar "stale"
```

Con `target="claude"` la única rama alcanzable en `run_boot` es
`elif lock_stale: _refresh_bridge_lock(...)`, que escribe el lock y no mira el disco.
`workflows/start_workflow.md:33` promete otra cosa: *"cuando los artefactos enlazados
bajo `.claude/` / `.cursor/` han desaparecido … (b) commands stale **o mirror missing**
→ `install.sh --target …`"*. La condición *mirror missing* no está implementada para
**ningún** target; para Claude tampoco lo está *commands stale*.

### Segundo defecto, de contaminación de ancla

`commands/start.md:5` fija `--tool cursor` sin condicional, mientras
`workflows/start_workflow.md:13` sí declara la variante (*"Claude: `--tool
claude-code`"*). El comando slash perdió el paréntesis que el workflow sí tiene.
`commands/start.md` se espeja a **ambos** harnesses, así que una sesión de Claude Code
que ejecuta `/agents:start` reclama el ancla como Cursor.

Verificado en vivo esta sesión: el arranque escribió `session_tool: cursor` ·
`delegation_mode: sequential` bajo Claude Code. Consumidores afectados:

| Consumidor | Efecto del mislabel bajo Claude |
| :--- | :--- |
| `RA-18` / `pipeline_workflow.md:15` | Prohíbe `SwitchMode` a plan sin causa |
| `pipeline_workflow.md:22` Fase 6 | Exige despacho vía Cursor `Task` con `modelId` — inejecutable |
| `pipeline_workflow.md:23` Fase 7 | Exige gates vía `audit_cursor_models.py --resolve` — inejecutable |
| `scripts/session_cost.py:192` | `return None`: **el medidor del Sprint 021 queda a oscuras** |
| `derive_delegation_mode` | `sequential`: desactiva el fan-out de 8 roles que Claude sí puede |

`delegation_conflict` no lo reporta: solo avisa cuando el modo *declarado* diverge de
la capacidad, y aquí el ancla declara `sequential` y calla.

**Demostración del coste**: corregidos los dos campos del ancla a mano,
`python3 scripts/session_cost.py --from-anchor --json` pasó de no medir a
`"measurable": true`, `ratio 5.3`. La misma sesión, el mismo transcript.

### Por qué sobrevivió al Sprint 040

`tests/test_session_start.py` tiene 10 tests, incluidos
`test_boot_lock_only_when_commands_fresh`, `test_boot_permission_error_is_advisory` y
`test_boot_generic_install_failure_still_exits_2`. **Ninguno pasa `--tool
claude-code`**: los diez son de forma Cursor. El gate estaba verde sobre una rama que
nadie ejercitaba.

### Qué es verdad cuando esto cierra

Arrancar en cualquiera de los dos harnesses, sobre un checkout con el mirror borrado,
instala el mirror y los git hooks de **ese** harness, y no toca el del otro.

---

## Design

### D1 — La corrección es cablear un mecanismo existente, no inventar uno

`bridge_intact()` ya existe en `hooks/on_init.py:82` y ya es la comprobación correcta
(artefactos en disco, independiente del lock). Se extrae a un módulo compartido
parametrizado por target, y lo consumen los **dos** invocadores: `on_init.py` (host
Claude, hook `SessionStart`) y `session_start.py --boot` (núcleo, cualquier tool).

**Rechazado**: duplicar la lógica dentro de `session_start.py`. Dos copias de un
predicado de integridad divergen — es exactamente cómo `workflows/start_workflow.md:33`
acabó prometiendo una condición que el script no implementa.

### D2 — El predicado de staleness pasa a ser agnóstico de target

`bridge_stale(root, target)` = **mirror ausente o incompleto** `OR` **contenido
divergente**. Para `cursor` el segundo término es el `commands_stale()` que ya existe.
Para `claude` es la integridad de los symlinks (`.claude/commands/agents/start.md`,
`.claude/agents/principal_agent.md` y el conjunto completo de `commands/*.md`).

El triaje de `run_boot` no cambia de forma — sigue siendo (a) lock-only, (b) install
incremental, (c) `PermissionError` advisory. Cambia **quién puede llegar a (b)**.

### D3 — Bi-harness: el arranque mantiene su target y nunca daña al otro

Restricción declarada por el humano: este árbol se comparte con Cursor.

| Decisión | Razón |
| :--- | :--- |
| El boot mantiene **solo** su propio target | Barato, y el otro harness repara el suyo en su siguiente arranque. Los locks ya son independientes por target (`start_workflow.md:33`) |
| Ningún paso borra el árbol del otro | Verificado: `grep -n rmtree scripts/install.py` → **cero coincidencias** (el Sprint 040 ya lo eliminó). Se protege como regresión |
| `deployment_workflow.md` Fase 4 refresca **ambos** locks | Un deploy mueve el tip e invalida los dos. Hoy la celda `bridge_lock_refresh` está condicionada a *"If `session_tool`/operators use Cursor"* y solo toca `.bridge_cursor.lock` |
| Un lock solo se refresca si **su** mirror está íntegro | Refrescar el lock de un target cuyo mirror está roto reproduce F2 desde el deploy. La regla es: mirror sucio → dejar el lock viejo para que el próximo boot instale |

### D4 — El tool correcto se resuelve en el render, no en tiempo de ejecución

`commands/start.md` es fuente única espejada a los dos harnesses, pero de forma
asimétrica: la copia Claude es un **symlink** al fuente (sin reescritura posible), la
copia Cursor es un **fichero renderizado** por `_rewrite_command_body()`
(`scripts/cursor_adapter.py:76-85`), que ya reescribe rutas `@.agents/`.

Por tanto: **el fuente dice `--tool claude-code`** (que es lo que el symlink Claude
necesita literalmente) y el renderer Cursor lo reescribe a `--tool cursor`.

**Rechazado — autodetección del harness en tiempo de ejecución** (variables de
entorno, ficheros centinela): introduce una heurística que falla en silencio hacia
un default, que es el defecto que este sprint repara. El render ya es determinista y
ya está cubierto por `commands_stale()`.

### D5 — Defaults que no eligen un IDE por el operador

`session_start.py:376` tiene `--tool` con `default="cursor"`; `session_state.py:369`
usa `default="terminal"`. Un `--boot` sin `--tool` reclama Cursor en silencio. Se
homologa a `terminal`, que es el default neutro que el workflow ya declara.

La sección `## Chat vs map (Cursor tiers)` del briefing se imprime
incondicionalmente — apareció bajo `--tool claude-code` en el clon. Se condiciona al
tool, porque propone `make cursor-tiers` a quien no usa Cursor.

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) touching **one physical
file** as its structural subject (`agents.md §2 jurisdictional_lock`).

The Work column `Assignee (proposed)` is a staffing proposal from Phase 1. Phase
4.1 (`agent_orchestrator`) is the authority that records the assignee.

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/bridge_state.py` | create | medium | `implementer_agent` | ⏳ |
| U2 | `scripts/session_start.py` | modify | **high** | `implementer_agent` | ⏳ |
| U3 | `hooks/on_init.py` | modify | medium | `implementer_agent` | ⏳ |
| U4 | `scripts/cursor_adapter.py` | modify | medium | `implementer_agent` | ⏳ |
| U5 | `commands/start.md` | modify | low | `doc_orchestrator` | ⏳ |
| U6 | `workflows/start_workflow.md` | modify | low | `doc_orchestrator` | ⏳ |
| U7 | `workflows/deployment_workflow.md` | modify | medium | `doc_orchestrator` | ⏳ |
| U8 | `tests/test_bridge_state.py` | create | low | `implementer_agent` | ⏳ |
| U9 | `tests/test_session_start.py` | modify | low | `implementer_agent` | ⏳ |
| U10 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | low | `doc_orchestrator` | ⏳ |
| U11 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | modify | low | `doc_orchestrator` | ⏳ |
| U12 | `workflows/pipeline_workflow.md` | modify | low | `doc_orchestrator` | ⏳ |

**Orden obligatorio**: U1 → (U2, U3, U4) → U5 → (U6, U7) → (U8, U9). U2 y U3 importan
U1; U5 depende de que U4 sepa reescribir el token. **U10, U11 y U12 son independientes
y pueden ir primero.**

### U10 — la plantilla oficial suspende su propio gate obligatorio

Hallazgo abierto al ejecutar la Fase 1 de este mismo sprint, no antes:

```
python3 skills/token-saver-auditor/scripts/audit_plan.py \
  docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md; echo $?
# ❌ Filter 6: `/loop` without `loop_guard.py start.`   → 2
```

`pipeline_workflow.md:15` hace ese auditor obligatorio en Fase 1 y declara que
*"exit `2` rechaza"*. `audit_plan.py:76` exige que todo plan que mencione `/loop`
nombre también `loop_guard.py`. El pie de la sección **Approval** de la plantilla
menciona `/loop` — como **prohibición** — y no nombra el guard. Consecuencia: **todo
plan redactado fielmente desde la plantilla es rechazado por el gate.**

`docs/sprints/040-core-pipeline/IMPLEMENTATION_PLAN.md` pasa (`exit 0`) sólo porque
su autor no arrastró ese pie. Es decir: el gate premia apartarse de la plantilla.

**Fix elegido — corregir la plantilla, no el filtro.** El filtro está haciendo su
trabajo: obliga a que todo plan que nombre `/loop` reconozca el guard que lo gobierna.
Relajarlo a base de detectar negaciones sería heurística frágil sobre prosa. El pie de
la plantilla pasa a nombrar `scripts/loop_guard.py start`, lo que además es gobernanza
**más** completa que la actual, no menos.

### U11 — segunda instancia de la misma clase, hallada en la Fase 4.2

Reproducido copiando las plantillas **sin editar** a un directorio de sprint vacío:

```
cp docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md  "$T/sprint/skill_assignment.md"
cp docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md  "$T/sprint/agent_assignment.md"
python3 scripts/check_forge_ladder.py --sprint-dir "$T/sprint"; echo $?
# ❌ P3 miss recorded but no skill name / SKILL.md path found   → 2
```

`pipeline_workflow.md` Fase 4.2 hace ese check obligatorio y declara *"exit `2`
rejects"*. Dos cadenas de la plantilla lo disparan:

| Cadena de la plantilla | Regex que la captura | Efecto |
| :--- | :--- | :--- |
| `| P4 | Three-File forge at Destination |` | `\bP4\b[^\n]{0,60}\bforg` (línea 229) | Registra **forja reclamada** |
| `Result (hit / miss / skipped)` | `P_MISS_TRAIL_RE` (línea 51-54) | Registra **P3 miss** |

Con ambos activos, `check_skill_assignment` exige un nombre de skill que la plantilla
no puede tener, y suspende. Es decir: **la plantilla oficial de la Fase 4.2 no puede
pasar el gate de la Fase 4.2.**

**Fix elegido — corregir la plantilla, no el regex.** Igual que en U10: el detector
está bien calibrado para su propósito (una reclamación de forja debe llevar rastro), y
relajarlo abriría el hueco que existe para cerrar. La plantilla reescribe la columna
`Result` sin la palabra `miss` y la fila `P4` sin la palabra `forge`, y añade una línea
que declara que la escalera termina en la primera rung alcanzada. Verificado en este
sprint: con esa redacción, `check_forge_ladder.py` sale `0`.

### U12 — tercera instancia, hallada en la Fase 4.3

`workflows/pipeline_workflow.md` Fase 4.3 declara la forma de `task_scope.md` como
`# | File | Operation | Risk | Assignee | Model | Effort | Status` **"when
`session_tool: cursor`"**, y la forma corta en caso contrario. El script que lo
aplica dice otra cosa:

```
scripts/check_task_scope.py:38    MODEL_FROM_SPRINT = 28
scripts/check_task_scope.py:119   if sprint_id is not None and sprint_id >= MODEL_FROM_SPRINT: return True
```

`Model`/`Effort` son obligatorias **desde el Sprint 28 en todo harness**; la condición
por herramienta es un disparador secundario para sprints anteriores. Medido en este
sprint: el `task_scope.md` se escribió en la forma que el workflow prescribe para una
sesión no-Cursor y el gate lo rechazó, `exit 2`.

**Fix elegido — corregir la prosa, no el script.** `MODEL_FROM_SPRINT = 28` es la
autoridad y es regresión a proteger. `close_workflow.md` Fase 2.6 ya resuelve esta
clase de desacuerdo igual: decide el artefacto que se ejecuta.

### Las tres instancias comparten causa

Un artefacto versionado (plantilla o prosa de workflow) y el gate que lo consume
evolucionaron por separado, y nada compara uno contra el otro. **Las tres se hallaron
ejecutando las Fases 1, 4.2 y 4.3 de este mismo sprint** — no auditando: seguir la
instrucción produjo un gate bloqueado, tres veces. El instrumento que impediría una
cuarta queda **fuera de alcance** y enrutado — ver la tabla `Out of scope`.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | Todo el trabajo es `pathlib`, `hashlib` y `subprocess`, ya en uso en los ficheros tocados |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `bridge_stale(root, target)` — integridad de mirror + digest | **script** (`scripts/bridge_state.py`) | `scripts/session_start.py --boot`, `hooks/on_init.py` |
| Refresco de ambos locks post-deploy | **script**, invocado desde el workflow | `workflows/deployment_workflow.md` Fase 4 `bridge_lock_refresh` |
| Reescritura del token `--tool` en el render Cursor | **script** (`_rewrite_command_body`) | `scripts/cursor_adapter.py` vía `install.sh --target cursor` |

Ningún mecanismo nuevo se delega a juicio de agente: los tres son comparaciones de
disco, deterministas y verificables (`token_economy_agent` Filtro 5).

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 12 | Count of rows in Work tables |
| Subagents dispatched | 0 (previsto) | El humano no ha solicitado despacho a subagentes; se ejecuta en sesión |
| Prior session ratio | **5.3** (ciclo 1, `first_turn` 21 682 → `peak` 115 914) | `python3 scripts/session_cost.py --from-anchor --json` |

**Nota de umbral**: 5.3 cruza el umbral **soft** (5×), que por diseño del Sprint 021
es puramente observacional. El umbral **hard** (15×) sigue lejos. Esta medición solo
fue posible tras corregir `session_tool` en el ancla — antes devolvía `None`.

---

## Tests

**Reproduce before repairing.**

| Check | Fails against the current tree? |
| :--- | :--- |
| `--boot --tool claude-code` sobre un checkout sin `.claude/` instala el mirror | **Yes** — es el defecto F2 |
| `--boot --tool claude-code` sobre un checkout sin `.claude/` instala los git hooks | **Yes** — hoy no instala ninguno |
| `bridge_stale(root, "claude")` es `True` cuando falta `.claude/commands/agents/start.md` | **Yes** — el predicado no existe fuera de `on_init.py` |
| `bridge_stale(root, "claude")` es `True` cuando el lock iguala `HEAD` pero el mirror falta | **Yes** — hoy el lock manda y el disco no se mira |
| Con lock fresco y mirror íntegro, `--tool claude-code` **no** reinstala (solo lock) | No — regresión a proteger (triaje (a)) |
| `commands/start.md` renderizado a Cursor contiene `--tool cursor`; el fuente contiene `--tool claude-code` | **Yes** — hoy ambos dicen `cursor` |
| `commands_stale()` sigue detectando divergencia tras añadir la reescritura del token | No — regresión a proteger |
| `install.sh --target claude` no borra ni modifica `.cursor/`, y viceversa | No — regresión a proteger (bi-harness) |
| `--boot` sin `--tool` reclama `terminal`, no `cursor` | **Yes** — hoy el default es `cursor` |
| El briefing omite `## Chat vs map (Cursor tiers)` cuando el tool no es `cursor` | **Yes** — hoy es incondicional |
| `session_cost.py --from-anchor` mide cuando `session_tool` es `claude-code` | No — regresión a proteger |
| `audit_plan.py` sobre `IMPLEMENTATION_PLAN_TEMPLATE.md` sale `0` | **Yes** — hoy sale `2` (U10) |
| `audit_plan.py` sigue rechazando un plan que propone `/loop` sin nombrar `loop_guard.py` | No — regresión a proteger: el Filtro 6 no se relaja |
| `check_forge_ladder.py` sobre `SKILL_ASSIGNMENT_TEMPLATE.md` copiada sin editar sale `0` | **Yes** — hoy sale `2` (U11) |
| `check_forge_ladder.py` sigue rechazando una forja reclamada sin rastro P3 | No — regresión a proteger: el detector no se relaja |
| `pipeline_workflow.md` Fase 4.3 describe la forma con `Model`/`Effort` sin condicionarla a Cursor | **Yes** — hoy la condiciona (U12) |
| `check_task_scope.py` sigue exigiendo `Model`/`Effort` en todo sprint ≥ 28 | No — regresión a proteger: `MODEL_FROM_SPRINT` no se toca |

---

## Verification

Exit codes read with `$?` directly, **never through a pipe**.

| Command | Expected |
| :--- | :--- |
| `python3 -m pytest tests/test_bridge_state.py tests/test_session_start.py -q; echo $?` | `0` |
| `python3 -m pytest tests/test_cursor_adapter.py tests/test_on_init.py -q; echo $?` | `0` (paridad Cursor intacta) |
| `bash tests/test_installer.sh; echo $?` | `0` |
| `make verify; echo $?` | `0` |
| `ruff check .; echo $?` | `0` |
| En clon limpio: `python3 scripts/session_start.py --boot --tool claude-code; echo $?` → `test -d .claude/commands/agents; echo $?` | `0` y `0` |
| En clon limpio: `test -f .git/hooks/pre-commit; echo $?` tras el boot Claude | `0` |
| `grep -c "tool cursor" commands/start.md` | `0` |
| `grep -c "tool cursor" .cursor/commands/start.md` tras `install.sh --target cursor` | `1` |
| `grep -n rmtree scripts/install.py` | sin salida |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md; echo $?` | `0` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/041-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| Plantillas copiadas sin editar a un sprint-dir vacío + `python3 scripts/check_forge_ladder.py --sprint-dir <dir>; echo $?` | `0` |
| `grep -c 'when `session_tool: cursor`' workflows/pipeline_workflow.md` en la celda de Fase 4.3 | `0` |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `workflows/start_workflow.md` | La celda `bridge_check` (1.5) deja de prometer *mirror missing* sin implementarlo: describe el predicado agnóstico de target y nombra `scripts/bridge_state.py` |
| `workflows/deployment_workflow.md` | `bridge_lock_refresh` (Fase 4) pasa de Cursor-only a ambos targets, con la regla «mirror sucio → no refrescar el lock» |
| `commands/start.md` | El token de `--tool` deja de ser Cursor fijo |
| `README.md` | Cuenta de `scripts/*.py` +1 (`bridge_state.py`) — bloque `COUNTED_START`, refrescable con `check_readme_counts.py --write` |
| `CHANGELOG.md` | Entrada del sprint bajo `[Unreleased]` referenciando `#041` |
| `config/invocation_exceptions.json` | Sin cambio: `bridge_state.py` declara `invoked_by:` en su docstring |
| `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | El pie de **Approval** nombra `scripts/loop_guard.py start`, de modo que un plan fiel a la plantilla pasa el gate de Fase 1 (U10) |
| `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | La columna `Result` y la fila `P4` de la escalera se reescriben para no registrar una forja inexistente; pasa el gate de Fase 4.2 (U11) |
| `workflows/pipeline_workflow.md` | La celda de Fase 4.3 deja de condicionar `Model`/`Effort` a Cursor y cita `MODEL_FROM_SPRINT = 28` (U12) |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Fila «Next / in flight» pasa a nombrar `041` |

**Measured figures.** Cada cifra de Context / Design / Verification lleva su comando.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Autodetección del harness en tiempo de ejecución | Rechazada en `D4`: heurística que falla hacia un default silencioso. Si alguna vez se quiere, es un sprint propio con su propia medición |
| Cambiar la semántica de `install.sh --target both` | Funciona; este sprint no la toca. El boot sigue siendo por-target (`D3`) |
| Revisar la sustancia de `RA-18` (plan mode bajo Cursor) | La regla es correcta; el defecto es que se aplicaba con el ancla mal etiquetada. Si `RA-18` necesita revisión, va por `agents.md §7` con su propia evidencia |
| Que `docs/active_state.json` esté en `.gitignore` (un clon limpio no tiene ancla) | Observado al reproducir. Es una decisión de aislamiento host/núcleo con razones propias (`RA-15`); se registra en `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` como hallazgo abierto, no se toca aquí |
| **Un check en `make verify` que pase toda plantilla versionada por el gate que la consume** | Es el instrumento que impediría una cuarta instancia de la clase U10/U11/U12, y es una preocupación distinta de la paridad de bridge. **Destino**: fila propia en `docs/roadmaps/core/pipeline/021-030-program-queue.md` como candidato del siguiente programa, redactada en la Fase 8 de este sprint con U10 y U11 como evidencia medida |
| Migrar `hooks/on_init.py` a target-paramétrico para Cursor | `SessionStart` es un hook de Claude Code; Cursor no tiene contraparte. U3 solo lo hace consumir U1 |

---

## Abort criterion

**Si `tests/test_cursor_adapter.py`, `tests/test_on_init.py` o `tests/test_installer.sh`
quedan en rojo por U1–U4 y no se reparan dentro del mismo sprint, se revierte la rama
completa a `d258b43` y el sprint se cierra sin entregar.**

Escrito antes de ejecutar y por la restricción explícita del humano: este árbol se
comparte con Cursor. La paridad Claude **no** se compra rompiendo el arranque de
Cursor, que hoy funciona. Un arranque Claude roto es el estado actual y es tolerable
una semana más; un arranque Cursor roto detiene el trabajo que sí está corriendo.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal (human, attended) |
| **Date** | 2026-08-30 |
| **Plan commit at approval** | `3ec3d80` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
**Este sprint no ejecuta ningún `/loop`**; si alguna fase llegara a envolverse, queda
gobernada por `scripts/loop_guard.py start`, que falla cerrado.*
