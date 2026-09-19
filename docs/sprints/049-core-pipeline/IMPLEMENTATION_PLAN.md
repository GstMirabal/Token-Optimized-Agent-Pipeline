# Implementation Plan: Sprint 049 — `cursor-bridge-100`

**Canonical path**: `docs/sprints/049-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/049` · **Base**: `main` at `c0f5904`
**Status**: `DRAFT`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

**Objetivo declarado por el humano:** que la ejecución bajo `session_tool: cursor`
sea efectiva al 100%, no que sus huecos queden declarados. Esa distinción decidió
el alcance de este sprint: en dos puntos de la negociación se ofreció la opción
mínima (rechazar en voz alta / declarar el hueco) y fue rechazada explícitamente.

**Estado de partida medido contra `c0f5904`** (todo reproducido en la sesión de
Fase 1, no recordado):

| Hecho | Comando / observación |
| :--- | :--- |
| Tests cursor en verde | `./venv_skillopt/bin/python -m pytest tests/test_cursor_adapter.py tests/test_audit_cursor_models.py tests/test_audit_cursor_era.py tests/test_cursor_phase1.py tests/test_bridge_state.py -q` → `32 passed` |
| Celdas de tier cursor pobladas | `--resolve mechanical\|gate\|qa_agent\|tester_agent\|author` → exit `0`, modelId real en los cinco |
| Catálogo de modelos es vivo, no estático | `make cursor-tiers` → `Catalogue source: ~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`, 38 modelos |
| Paridad `rule_triggers.json` ↔ `rules/*.md` | 11/11 |
| Skills del framework | 34 totales · 23 con `scripts/` · 11 solo conocimiento |

Los seis defectos de abajo conviven con ese verde. Ninguno es detectable por
`make verify` ni por la suite: viven exactamente donde no hay cobertura.

| ID | Sev | Defecto | Reproducción |
| :--- | :--- | :--- | :--- |
| `F-049-1` | ALTA | `install.py --target cursor` con `--profile`/`--profile-path` descarta el perfil entero en silencio: exit `0`, cuatro mensajes de éxito, cero artefactos del perfil | Sandbox: host falso + `install.py --target cursor --profile example-project`; `.cursor/agents/` = 14 agentes del framework, `domain_specialist_example` ausente; `.claude/` ausente; `CLAUDE.md` ausente |
| `F-049-2` | ALTA | `bridge_stale(cursor)` no detecta un espejo incompleto: borrados los 13 `.cursor/rules/*.mdc` (incluido `00-constitution.mdc`), 13 de 14 agentes y `mcp.json` → `False` | Sandbox: `mirror_missing(cursor)=False` y `bridge_stale(cursor)=False` tras el borrado; mismo daño en `claude` → `True` |
| `F-049-3` | MEDIA | El censo está congelado en 026–033; los sprints **034–040** declaran `` tool `cursor` `` en su `SPRINT_LOG.md` y quedan fuera | Bucle sobre `docs/sprints/0*/SPRINT_LOG.md` extrayendo `` tool `…` ``: cursor en 027–040, sin línea desde 041 |
| `F-049-4` | BAJA | La deriva entre el mapa de tiers y el modelo aplicado se imprime pero no se gatea | `make cursor-tiers` → `Applied model (discrepancy): grok-4.6 — differs from map author glm-5.2` **y exit `0`** |
| `F-049-5` | BAJA | `RA-18` no tiene enforcement en runtime; los 4 casos de `test_cursor_phase1.py` son aserciones de presencia de string sobre markdown | `grep -rn "RA-18\|SwitchMode" scripts/ hooks/ tests/` → ninguna ocurrencia ejecutable |
| `F-049-6` | MEDIA | Seis skills declaradas `model-invoked` **tienen `scripts/` ejecutables con entrada CLI**. Bajo Cursor nada las presenta al modelo: son código muerto, y cuatro filas de `agents.md §1` se quedan sin instrumento | `config/invocation_exceptions.json:53,58` + `skills/python-quality-auditor/scripts/python_quality_auditor.py` y `skills/js-standardizer/scripts/js_standardizer.py`, ambos con `__main__` |

**Qué es verdad cuando este sprint termina:** un host que instala con `--target
cursor` recibe su perfil; un espejo `.cursor/` incompleto se detecta en el arranque;
el censo cubre la ventana Cursor medida; la deriva de tier falla en vez de avisar;
existe un test que demuestra que el fallo de `RA-18` se captura; y las cuatro filas
de `agents.md §1` que dependían de que un modelo se fijara en una skill tienen un
invocador determinista que corre bajo los dos arneses.

---

## Design

### D1 — `F-049-6` no es un hueco de Cursor: es una infracción del Filtro 5

`rules/token_economy.md` Filtro 5 (citado en la sección **Mechanisms** de la
plantilla): *un mecanismo recurrente delegado a juicio de agente cuando existe una
alternativa determinista se rechaza, y la alternativa debe nombrarse.*
`python-quality-auditor` y `js-standardizer` **son** la alternativa determinista —
scripts con entrada CLI dentro de la propia skill — y están declaradas
`model-invoked`. Bajo Claude Code eso funciona por accidente (el modelo ve la skill);
bajo Cursor no funciona en absoluto.

Por eso la remediación no es documental. Se les da un invocador determinista y se
retira la excepción `RA-16` que ya no les corresponde. Esto es jurisdicción de
`token_economy_agent` (*owns whether a proposed recurring mechanism should be a
deterministic script or an agent judgment call, before it lands in an Implementation
Plan*), que debe firmar antes de la Puerta de Aprobación.

**Alternativa rechazada:** declarar el hueco en `AUTONOMY_POSTURE_GUIDE.md` y dejar
las skills como están. Rechazada explícitamente por el humano en Fase 1: deja en pie
la infracción del Filtro 5 y mantiene los scripts muertos bajo Cursor.

### D2 — Paridad de perfil: se espeja lo que Cursor tiene, se nombra lo que no

Cursor tiene concepto de subagentes y de reglas; no tiene concepto de *skills* en
este puente (`install_cursor_bridge` materializa `commands`, `rules`, `agents`,
`mcp.json` — nunca `skills`). El perfil se espeja así:

| Clase | Destino | Nota |
| :--- | :--- | :--- |
| `agents/` | `.cursor/agents/<name>.md` | Mismo renderizador que los 14 del núcleo |
| `rules/` | `.cursor/rules/<stem>.mdc` | Metadatos según `D3` |
| `skills/` | — | Sin destino en el puente. El instalador **nombra cada skill no espejada**, con exit distinto de `0` sólo si el perfil no trae nada más |

Las 23 skills con `scripts/` siguen siendo invocables por ruta bajo Cursor: ahí no
hay defecto, y `D1` convierte en determinista justo a las que dependían del modelo.

### D3 — Metadatos de trigger de una regla de perfil: primario + respaldo, nunca caída silenciosa ni fallo duro

`_write_rules` hace hoy `triggers[key]` — un índice directo contra
`config/rule_triggers.json`, que sólo lista las 11 reglas del núcleo. Una regla de
perfil ahí es un `KeyError` que rompe la instalación entera.

Resolución en cascada, decidida por el humano en Fase 1 contra la opción de fallar:

1. **Primario** — el perfil trae `rule_triggers.json` con el mismo esquema que el
   núcleo. Simétrico, verificable, no inventa metadatos.
2. **Respaldo** — si ese fichero no existe, se leen `description`/`globs` del
   frontmatter de la propia `rules/*.md` del perfil.
3. **Error nombrado** — sólo si faltan los dos. Nunca un `KeyError` crudo, nunca
   `alwaysApply: true` por defecto (violaría `agents.md §2 token_saver`: las reglas
   de dominio se cargan bajo trigger, jamás precargadas).

`profiles/example-project/` recibe su `rule_triggers.json` para que el mecanismo
tenga fixture — hoy tiene `rules/domain_example_standard.md` sin metadato alguno.

### D4 — `F-049-2` se arregla por simetría, no por parche

`_claude_mirror_missing` compara **nombres**: cada `.md` de `commands/` y `agents/`
debe tener contraparte. `_cursor_mirror_missing` sólo pregunta `is_dir()` por dos
directorios. La corrección es darle al lado Cursor la misma prueba de pertenencia,
extendida a lo que el lado Claude no tiene: `rules/` (incluido `00-constitution.mdc`,
el único `alwaysApply: true` que importa `agents.md`) y `mcp.json`.

### D5 — La ventana del censo se deriva, no se vuelve a fijar a mano

`ERA_START`/`ERA_END` se escribieron en Sprint 036, cuando 034 y 035 ya habían
corrido bajo Cursor: la ventana nació equivocada y Sprint 046 la reafirmó sin volver
a medir. Sustituir `33` por `40` repetiría el mismo modo de fallo en el próximo
sprint Cursor. La ventana se deriva de los `SPRINT_LOG.md` que declaran
`` tool `cursor` ``, que es el dato que define la era.

---

## Work

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/cursor_adapter.py` (+ par `tests/test_cursor_adapter.py`) | modify | high | `implementer_agent` | ⏳ |
| U2 | `scripts/install.py` (+ par `tests/test_installer.sh`) | modify | high | `implementer_agent` | ⏳ |
| U3 | `profiles/example-project/rule_triggers.json` | create | low | `implementer_agent` | ⏳ |
| U4 | `scripts/bridge_state.py` (+ par `tests/test_bridge_state.py`) | modify | high | `implementer_agent` | ⏳ |
| U5 | `scripts/audit_cursor_era.py` (+ par `tests/test_audit_cursor_era.py`) | modify | medium | `implementer_agent` | ⏳ |
| U6 | `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` | modify | low | `implementer_agent` | ⏳ |
| U7 | `scripts/audit_cursor_models.py` (+ par `tests/test_audit_cursor_models.py`) | modify | medium | `implementer_agent` | ⏳ |
| U8 | `tests/test_cursor_phase1.py` | modify | low | `implementer_agent` | ⏳ |
| U9 | `Makefile` — target `quality-audit` (`F-049-6`) | modify | medium | `implementer_agent` | ⏳ |
| U10 | `config/invocation_exceptions.json` | modify | medium | `rule_validator` | ⏳ |
| U11 | `agents.md` — filas `§1` de style-score y complejidad | modify | high | `rule_validator` | ⏳ |
| U12 | `Makefile` — target `bridge-state` (`F-049-2`) | modify | low | `implementer_agent` | ⏳ |

**Restricción de secuencia (`jurisdictional_lock`).** U9 y U12 comparten sujeto
estructural (`Makefile`). No pueden estar en curso a la vez: U12 toma el sujeto
sólo cuando U9 ha aterrizado (precedente Fase 014 `T21`/`T22`). U1 debe aterrizar
antes que U2: U2 llama a la firma que U1 introduce.

**Unidades `fix(` y su test pareado.** U1, U2, U4, U5, U7 serán commits `fix(`:
`rules/code_craft.md §6` exige el test en el mismo commit y `hooks/on_commit.py
audit_regression_test` lo verifica. El par va en la misma fila, no en una propia —
partirlos es lo que obligó a Sprint 047 a re-emparejar 7 unidades a mitad de
ejecución.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | Ninguna unidad añade dependencia: todo son `pathlib`/`json`/`subprocess` ya en uso |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Auditoría de calidad Python/JS (`F-049-6`) | **script** — deja de ser juicio de agente | `Makefile` target `quality-audit` |
| Integridad del espejo fuera del arranque (`F-049-2`) | **script** | `Makefile` target `bridge-state` |
| Gate de deriva de tier (`F-049-4`) | **script** | `make cursor-tiers` (`--check`, ya existente) |
| Censo de era Cursor (`F-049-3`) | **script** | `Makefile` target `cursor-era-audit` (ya existente) |

`token_economy_agent` debe auditar la fila 1 antes de la Puerta de Aprobación: es
una reclasificación de juicio-de-agente a determinista sobre una fila de `agents.md`,
exactamente su `pre_approval_audit` / Filtro 5.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 12 | Conteo de filas de la tabla Work |
| Subagents dispatched | 1 en Fase 1 (`Explore`, descartado y re-verificado a mano) | Transcripción de sesión |
| Prior session ratio | 4.5 (ciclo 1) · **5.05 (ciclo 2)** | `python3 scripts/session_cost.py --from-anchor --json` |

El ciclo 2 de la sesión de Fase 1 cruzó el umbral blando de 5×, empujado por la
verificación en sandbox de `F-049-1` y `F-049-2`. Se registra aquí en vez de
redondearse a la baja: la reproducción de los dos defectos ALTA es lo que costó, y
es lo que convirtió el sprint de documental a correctivo.

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| Host + `--target cursor --profile example-project` deja `domain_specialist_example` en `.cursor/agents/` | **Yes** — este es el defecto (`F-049-1`) |
| Host + `--target cursor` con perfil sale distinto de `0` o nombra lo no espejado | **Yes** — hoy exit `0` mudo (`F-049-1`) |
| `bridge_stale(cursor)` es `True` con `.cursor/rules/` borrado | **Yes** — este es el defecto (`F-049-2`) |
| `bridge_stale(cursor)` es `True` con 1 de 14 agentes presentes | **Yes** — este es el defecto (`F-049-2`) |
| El censo incluye los sprints 034–040 | **Yes** — este es el defecto (`F-049-3`) |
| `make cursor-tiers` sale `2` con el mapa en deriva | **Yes** — hoy sale `0` (`F-049-4`) |
| Fase 5 rechaza un plan que sólo existe bajo `~/.cursor/plans/` | **Yes** — el chequeo existe, ningún test lo demuestra (`F-049-5`) |
| `make quality-audit` corre sin que un modelo elija la skill | **Yes** — este es el defecto (`F-049-6`) |
| `bridge_stale(claude)` sigue detectando espejo vacío | **No** — regresión a proteger |
| Los 32 tests cursor siguen en verde | **No** — regresión a proteger |
| `--resolve` de los cinco targets sigue en exit `0` | **No** — regresión a proteger |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `./venv_skillopt/bin/python -m pytest tests/ -q; echo $?` | `0`, con ≥ 32 casos cursor y los nuevos pares |
| `make verify; echo $?` | `0` |
| `make quality-audit; echo $?` | `0` — nuevo target, corre sin intervención de modelo |
| `make bridge-state; echo $?` | `0` sobre el árbol limpio |
| `make cursor-tiers; echo $?` | `2` mientras `author` esté en deriva (`grok-4.6` vs `glm-5.2`); `0` una vez reconciliado |
| `make cursor-era-audit; echo $?` | `0`, y `CURSOR_ERA_EXECUTION_AUDIT.md` lista 027–040 |
| `bash tests/test_installer.sh; echo $?` | `0`, incluyendo el caso cursor+perfil |
| `python3 scripts/verify_references.py; echo $?` | `0` tras U10 (ninguna excepción apunta a ruta viva sin invocador) |

Los códigos de salida se leen con `$?` directo, nunca a través de una tubería.

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` `§1` | Las filas `linter_command` (Python y JS/TS), `max_indentation` y `max_lines_per_func` pasan de *"Verified by: QA-gate judgment, NOT `make verify`"* a nombrar el invocador determinista y su arnés |
| `config/invocation_exceptions.json` | Se retiran las excepciones `model-invoked` de `python-quality-auditor` y `js-standardizer`; las otras cuatro se re-anotan con el motivo vigente |
| `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` | Regenerado sobre la ventana derivada (artefacto derivado — nunca editado a mano) |
| `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | La tabla de contrapartes Cursor registra que las skills de perfil no tienen destino y que el instalador las nombra |
| `CHANGELOG.md` `[Unreleased]` | Entrada de Sprint 049 en el Closeout |
| `docs/decisions/` | ADR si `rule_validator` juzga que `D1` (reclasificación determinista) es decisión arquitectónica y no enmienda de fila |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Espejar `skills/` del framework o del perfil dentro de `.cursor/` | Cursor no tiene concepto de skills en este puente. `D1` resuelve el caso que importaba (las 6 ejecutables) dándoles invocador determinista; las 11 de sólo conocimiento quedan declaradas en `AUTONOMY_POSTURE_GUIDE.md` |
| `verify_references.py` check (g) sobre celdas Cursor | Hueco **declarado** (D15) en el docstring, no silencioso. Destino: `docs/roadmaps/core/pipeline/` como entrada propia |
| Reconciliar `author.cursor.model` (`glm-5.2` vs `grok-4.6` aplicado) | U7 construye el gate; *qué* modelo debe ganar es un ensayo de tier, jurisdicción de `MODEL_TIER_TRIAL_GUIDE.md`. El gate rojo es el resultado esperado del sprint, no un fallo |
| Interceptar `SwitchMode` en runtime | Es una función del IDE, fuera del alcance del framework. U8 cubre lo que sí es alcanzable: demostrar que la consecuencia se captura en Fase 5 |

---

## Abort criterion

Se aborta y revierte si la paridad de perfil bajo Cursor (`U1`+`U2`) exige cambiar
la forma en que el lado Claude instala perfiles. El puente Claude es el camino en
producción de todos los hosts actuales; un sprint que endurece Cursor rompiendo
Claude ha invertido su propio objetivo. Observación concreta que lo dispara:
`bash tests/test_installer.sh` falla en cualquiera de sus aserciones Claude
preexistentes (líneas 53–55) después de `U1` o `U2`.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | {{HUMAN}} |
| **Date** | {{ISO_DATE}} |
| **Plan commit at approval** | {{COMMIT_SHA}} |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
