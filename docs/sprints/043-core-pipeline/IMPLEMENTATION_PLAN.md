# Implementation Plan: Sprint 043 — submodule-runtime-parity

**Canonical path**: `docs/sprints/043-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/043` · **Base**: `main` at `d7b0d779b81d27bbbcaef4fefa8d818badf8b0e1`
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

El operador reportó cuatro fallos al trabajar con `.agents` **instalado como
submódulo** dentro de un host. Investigación en el checkout núcleo
(`d7b0d77`, 2026-09-06):

### C-1 · graphify no arranca — shebang absoluto del console-script

`head -1 venv_skillopt/bin/graphify` →
`#!/Users/gstmirabal/Developer/.agents/venv_skillopt/bin/python3.13`.
`head -1 venv_skillopt/bin/pip` → misma línea. Un venv de Python **no es
relocatable**: todos los console-scripts (`graphify`, `pip`, `ruff`, …) son
ficheros con shebang **absoluto** a `<build-path>/venv_skillopt/bin/python3.13`.
Cuando `.agents` vive en `<host-root>/.agents/`, ese intérprete no existe →
`bad interpreter: No such file or directory`. En cambio
`venv_skillopt/bin/python` → `python3.13` →
`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`
(symlink **absoluto al intérprete del sistema**, sobrevive a la reubicación),
de modo que `venv_skillopt/bin/python -m graphify` **sí** funciona reubicado.

### C-2 · invocación inconsistente de graphify en los workflows

`grep -rn "graphify" workflows/`:
- `workflows/start_workflow.md:24` (`read_graph`) usa
  `.agents/venv_skillopt/bin/graphify update .` — console-script, frágil (C-1).
- `workflows/reverse_documentation_workflow.md:77` usa
  `.agents/venv_skillopt/bin/python -m graphify update . --force` — forma módulo,
  robusta.
- `claude/mcp.json` usa `.agents/venv_skillopt/bin/python -m graphify.serve` —
  forma módulo, correcta.

`rules/graphify.md` documenta `graphify query`, `graphify path`, `graphify update .`
— todas en forma console-script.

### C-3 · `.graphify_root` con ruta absoluta baked-in

`cat graphify-out/.graphify_root` → `/Users/gstmirabal/Developer/.agents`.
En otro checkout esa raíz no coincide; graphify puede rechazar el grafo o
reindexar sin avisar.

### C-4 · el sandbox mata graphify en silencio

`claude/settings.hooks.json` trae `sandbox.enabled: true` +
`autoAllowBashIfSandboxed: true`. Bash sandboxeado = sin red y con escritura
restringida al workspace. `graphify update` escribe en `graphify-out/cache/`
(dentro de `.agents/`) y en modo no-AST toca red → el sandbox lo deniega
**sin prompt** (corre auto-sandboxeado). Patrón ya registrado en el repo:
`docs/roadmaps/core/pipeline/021-030-program-queue.md:121`
(`xargs: sysconf(_SC_ARG_MAX) failed`), `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md`
CE-5 (`git init` denegado), múltiples `SPRINT_LOG.md` («sandbox blocked rsync»).
`read_graph` no distingue «grafo no disponible» de «grafo consultado» y degrada
a grep recursivo sin declararlo.

### C-5 · `venv_skillopt` no carga en submódulo

Misma raíz que C-1. `venv_skillopt/pyvenv.cfg`:
`command = … -m venv /Users/gstmirabal/Developer/.agents/venv_skillopt`.
`workflows/start_workflow.md:23` (`pip_setup`) sólo reconstruye el venv
**si `.agents/installed.lock` falta**. Un checkout con lock presente y venv
construido para otra ruta (copia, rename del núcleo, host reusado) **nunca se
revalida** → los console-scripts y `pip` quedan rotos y nada lo detecta.

### C-6 · el flujo de aprendizaje se lee como contradicción

`agents.md §3 strict_rule` prohíbe que una sesión host altere `.agents` in place.
`agents.md §4 feedback_upstream` obliga a que los hallazgos framework-class
lleguen al núcleo. Ambas encajan (el host **detecta y redacta**; el PR al núcleo
se hace desde un **clon separado**, nunca escribiendo en el árbol del submódulo),
pero la regla está dispersa entre §3 `jurisdiction`, §3 `strict_rule`, §4
`feedback_upstream` y `docs/guides/SELF_IMPROVEMENT_GUIDE.md`, sin un punto
canónico que lo diga entero. `scripts/_mode.py` ya implementa el criterio
(`.git` directorio = núcleo; fichero = submódulo) pero su docstring es el único
sitio donde el flujo se narra completo.

**Estado esperado al cierre**: `venv_skillopt/bin/python -m graphify --version`
sale `0` bajo cualquier ruta; `grep -rn "bin/graphify " workflows/ rules/` no
tiene coincidencias; `scripts/check_venv_relocatable.py` existe y sale `2` sobre
un venv reubicado roto y `0` sobre uno recién construido; `read_graph` reporta el
fallo de sandbox en vez de degradar callado; `agents.md §4` tiene un bloque
canónico único del flujo de tres niveles y `§3` lo referencia sin repetirlo.

---

## Design

### D-1 · Preferir `python -m graphify` sobre el console-script `graphify`, en todas partes

`venv_skillopt/bin/python` resuelve al intérprete del sistema por symlink
absoluto y sobrevive a la reubicación; el console-script no. Se convierten todas
las invocaciones de gobernanza a `venv_skillopt/bin/python -m graphify …`.

- **Rechazado**: parchear los shebangs tras cada `pip install` (frágil; hay que
  re-ejecutarlo en cada rebuild; `install.sh` necesitaría una pasada de
  relocation).
- **Rechazado**: convertir `bin/graphify` en un wrapper `sh` (nuevo artefacto
  mantenido, `RA-16`).
- La forma módulo no requiere mantenimiento y ya funciona reubicada.

### D-2 · La comprobación de relocatabilidad corre cada sesión, independiente de `installed.lock`

`scripts/check_venv_relocatable.py` (nuevo): lee `venv_skillopt/pyvenv.cfg`
línea `command = … -m venv <PATH>` y un shebang de console-script
(`venv_skillopt/bin/pip`), y compara el prefijo de ruta contra
`_root.agents_root()`. Divergencia → exit `2`. `pip_setup` invoca la
comprobación **antes** de decidir; exit `2` fuerza
`python3 -m venv --clear venv_skillopt && … pip install -r requirements-core.txt`
y reescribe `installed.lock`.

- **Rechazado**: invalidar `installed.lock` al cambiar de ruta — el lock registra
  el conjunto de requirements y un timestamp, no una ruta; sobrecargarlo es
  incorrecto.
- **Rechazado**: reconstruir el venv incondicionalmente cada sesión — lento y
  redundante. La comprobación son 2 lecturas de fichero.

### D-3 · `.graphify_root` obsoleto ⇒ rebuild forzado, no edición

`.graphify_root` vive dentro de `graphify-out/` (git-ignored, regenerable).
`read_graph` compara su contenido con `agents_root()`; si difiere,
`venv_skillopt/bin/python -m graphify update . --force`. Regenerar es canónico;
editar el fichero a mano no.

### D-4 · El fallo de sandbox se reporta, nunca se degrada en silencio

`read_graph`: si `graphify update` sale distinto de `0`, emitir al humano
`⚠️ graph unavailable (sandbox/venv) — esta sesión procede sin graph sovereignty`
y registrarlo; **no** caer a grep recursivo como si nada. Éste es el alcance
mínimo de la parte «sandbox» — la recuperación completa (retry fuera del
sandbox) queda fuera (§ Out of scope).

### D-5 · Consolidar el flujo de aprendizaje en un bloque canónico único en `agents.md §4`

`§4 feedback_upstream` pasa a contener el bloque entero de tres niveles
(host-class → `memory_index.json`; project-family → `--profile-path`;
framework-class → **branch + PR desde un clon separado del núcleo**, jamás un
write al árbol del submódulo). `§3 jurisdiction` y `§3 strict_rule` lo
**referencian** en vez de reformularlo. `RA-14 PATCH_PROPAGATION`: al parchear
`agents.md` se hace `grep -n` completo de `feedback_upstream`, `strict_rule`,
`jurisdiction`, `three-tier`/`tres niveles` en el propio fichero antes de cerrar
la unidad.

- **Rechazado**: un ADR nuevo — no hay decisión nueva; el flujo de tres niveles
  ya está aceptado y en vigor. Esto es consolidación de prosa.
- **Fuera**: la contradicción real `§6` («proceso rígido secuencial») vs
  `§2 no_interference` (implica concurrencia) — `ADR-0001 §2` la deja sin
  corregir a propósito. No se toca (§ Out of scope).

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) touching **one physical
file** as its structural subject (`agents.md §2 jurisdictional_lock`).

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `workflows/start_workflow.md` | modify | medium | `orchestrator` | ⏳ |
| A2 | `rules/graphify.md` | modify | low | `rule_validator` | ⏳ |
| D1 | `scripts/check_venv_relocatable.py` | create | medium | `implementer_agent` | ⏳ |
| D2 | `tests/test_venv_relocatable.py` | create | low | `implementer_agent` | ⏳ |
| C1 | `agents.md` | modify | medium | `rule_validator` | ⏳ |
| C2 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify | low | `doc_orchestrator` | ⏳ |

**Unit notes**

- **A1** — `read_graph`: `graphify update .` → `venv_skillopt/bin/python -m graphify update .`;
  añadir chequeo de `.graphify_root` (D-3) y reporte no-silencioso de fallo de
  sandbox (D-4). `pip_setup`: invocar `scripts/check_venv_relocatable.py`
  **antes** del test de `installed.lock`; exit `2` fuerza `python3 -m venv --clear`.
  Los pasos conservan sus claves (`pip_setup`, `read_graph`) → `map_workflows.py`
  no cambia el step map.
- **A2** — ejemplos CLI a `venv_skillopt/bin/python -m graphify <cmd>`; añadir
  nota «modo submódulo: nunca el console-script `graphify`».
- **D1** — `invoked_by: workflows/start_workflow.md#pip_setup` en el docstring
  (`RA-16`). Import de `_root.agents_root`. Sin dependencias nuevas. ≤ 50 líneas,
  type hints, Google-style docstring (`agents.md §1`).
- **D2** — fixture: copia mínima de `pyvenv.cfg` + un `bin/pip` con shebang, en
  `tmp_path`, con ruta de build ≠ ruta actual → assert exit `2`; venv coherente
  → assert exit `0`.
- **C1** — ver D-5. Grep de propagación obligatorio antes de cerrar.
- **C2** — párrafo «Cómo aprende el framework de un host» apuntando al bloque
  canónico de `agents.md §4`.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | Track D usa sólo `pathlib`, `configparser`/parsing de texto y `_root.py` ya presente. |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `scripts/check_venv_relocatable.py` — compara la ruta de build del venv contra `agents_root()` | deterministic script | `workflows/start_workflow.md#pip_setup` (cadencia: cada sesión) |

`RA-16 INVOCATION_COVERAGE`: el `invoked_by:` va en el docstring del script y el
paso `pip_setup` de `start_workflow.md` lo nombra. `scripts/verify_references.py`
check (d) debe resolverlo.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 6 | Count of rows in Work table |
| Subagents dispatched | ~9 (principal, devops, orchestrator, agent_orchestrator, skill_architect, rule_validator, implementer, qa, tester) | pipeline roles, Phases 1–8 |
| Prior session ratio | 4.6 — cycle `first_turn` 24 651 → `peak` 112 199, bajo el soft 5× | `python3 scripts/session_cost.py --from-anchor --json` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues.

---

## Tests

**Reproduce before repairing.**

| Check | Fails against the current tree? |
| :--- | :--- |
| `venv_skillopt/bin/graphify --version` ejecutado con `venv_skillopt` en una ruta ≠ ruta de build | **Yes** — `bad interpreter` (defecto C-1) |
| `grep -rn "bin/graphify " workflows/ rules/` | **Yes** — forma console-script presente (defecto C-2) |
| `python3 scripts/check_venv_relocatable.py` sobre un venv reubicado roto | **Yes** — el script no existe aún (Track D) |
| `venv_skillopt/bin/python -m graphify --version` | **No** — funciona reubicado; regresión a proteger |
| `venv_skillopt/bin/python -m pytest tests/ -q` | **No** — suite verde actual; regresión a proteger |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 scripts/check_venv_relocatable.py; echo $?` | `0` sobre el venv correctamente ubicado |
| `venv_skillopt/bin/python -m graphify --version; echo $?` | `0` |
| `grep -rn "bin/graphify " workflows/ rules/; echo $?` | `1` (sin coincidencias) |
| `venv_skillopt/bin/python -m pytest tests/test_venv_relocatable.py -q; echo $?` | `0` |
| `python3 scripts/verify_references.py; echo $?` | `0` (check (d) resuelve el nuevo `invoked_by`) |
| `make verify` | pass (pytest + installer + step map fresco) |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/043-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `grep -n "feedback_upstream\|strict_rule\|jurisdiction" agents.md` | el flujo de tres niveles aparece completo una sola vez (§4); §3 referencia, no repite |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `workflows/start_workflow.md` | `pip_setup` invoca `check_venv_relocatable.py` y reconstruye con `--clear` si exit `2`; `read_graph` pasa a `python -m graphify`, chequea `.graphify_root` y reporta fallo de sandbox sin degradar callado |
| `rules/graphify.md` | ejemplos CLI a `venv_skillopt/bin/python -m graphify <cmd>`; nota de modo submódulo |
| `agents.md` | §4 `feedback_upstream` consolidado en un bloque canónico del flujo de tres niveles; §3 `jurisdiction`/`strict_rule` lo referencian |
| `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | párrafo explícito «cómo aprende el framework de un host» apuntando a `agents.md §4` |
| `scripts/check_venv_relocatable.py` | **nuevo** — gate determinista de relocatabilidad del venv |
| `tests/test_venv_relocatable.py` | **nuevo** — cobertura del gate |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerado en Phase 8 (`make verify`); esperado no-op (claves de paso sin cambio) |
| `CHANGELOG.md` (`.agents`) | entrada `[Unreleased]` en Sprint Closeout |
| `docs/sprints/043-core-pipeline/PHASE_REGISTER.md` | **nuevo** en Sprint Closeout |

**Measured figures.** Toda cifra en Context / Cost lleva su comando reproductor
(`head -1`, `cat`, `grep -rn`, `session_cost.py --from-anchor --json`).

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Recuperación completa del fallo de sandbox (retry automático fuera del sandbox, override de `permissions`) | Claude Code es dueño del sandbox; sólo podemos detectar y reportar. → sprint futuro de integración con el harness si reincide |
| Contradicción `§6` «rigid sequential» vs `§2 no_interference` | `ADR-0001 §2` la deja sin corregir a propósito; reabrir exige una medición donde dominen los pares de ficheros disjuntos. → permanece en `ADR-0001` |
| Reescribir `install.sh` para reubicar un venv existente | `venv_skillopt/` es git-ignored y se reconstruye por checkout; soportar relocation es peso muerto. → no se persigue |
| Automatizar el install de la stack pesada `requirements-skillopt.txt` | On-demand por diseño (`skills/skillopt/SKILL.md`); sólo la relocatabilidad del venv core está en alcance. → sin cambio |
| Fan-out paralelo | `ADR-0001` |

---

## Abort criterion

Si `check_venv_relocatable.py` no puede distinguir un venv válidamente reubicado
(misma máquina, ruta movida, `bin/python` aún resolviendo) de uno roto **sin
falsos positivos sobre un venv recién creado por un `pip_setup` limpio** — es
decir, si dispararía en cada onboarding normal — el gate es incorrecto: Track D
(D1, D2, y el cableado de `pip_setup` en A1) se revierte y Tracks A (resto) y C
proceden por separado.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | _pending_ |
| **Date** | _pending_ |
| **Plan commit at approval** | _pending_ |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*

> **Do not delete the sentence above.** `audit_plan.py` Filter 6 rejects any plan
> that names `/loop` without also naming `loop_guard.py`, and this footer names
> both.
