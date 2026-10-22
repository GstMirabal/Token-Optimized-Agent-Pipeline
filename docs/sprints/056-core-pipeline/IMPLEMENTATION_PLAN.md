# Implementation Plan: Sprint 056 — sandbox-enumeration-and-instrument-residue

**Canonical path**: `docs/sprints/056-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/056` · **Base**: `main` at `d88593c`
**Status**: `APPROVED` (2026-10-12) → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

El Sprint 056 ejecuta lo que la hoja de ruta ya le asignó
(`docs/roadmaps/core/pipeline/021-030-program-queue.md`): el **bloque E**, que son
restos de instrumentos decididos el 2026-10-05 (`KI-052-1`, `KI-052-3`, `KI-052-4`,
`KI-052-7` y `KI-053-2`), y los **ocho ítems enrutados en el cierre y el despliegue
del Sprint 055** (`KI-055-1`..`KI-055-8`). El alcance de 13 ítems en dos olas lo
confirmó el humano el 2026-10-12.

Mediciones en la base `d88593c`. Cada cifra lleva el comando que la reproduce; las
sondas usan fixtures en el scratchpad y no modifican el árbol:

| Ítem | Defecto medido en la base | Comando |
| :--- | :--- | :--- |
| `KI-052-1` | `is_adr_superseded()` devuelve `False` para una ADR con `**Status**: \`Superseded by ADR-0017\``, que es el formato real de `docs/decisions/ADR-0012` y `ADR-0015` | `python3 -I -c "import sys; sys.path.insert(0,'scripts'); from pathlib import Path; import docs_freshness_check as d; print(d.is_adr_superseded(Path('docs/decisions/ADR-0015-artifact-owner-writer-separation.md')))"` → `False` |
| `KI-052-3` `NF-2` | Un fichero cuyo único `invoked_by:` está en prosa queda resuelto: `_skill_script_directly_resolved` → `True`, mientras que `_invoked_by_line` → `''`. Las comprobaciones por subcadena están en `scripts/verify_references.py:547`, `:659` y `:698` | Sonda de fixture (Tests, fila 2) |
| `KI-052-3` `NF-1` | `_token_present` acepta `/` como frontera, así que `otra-skill/scripts/env.py` en un README satisface el `scripts/env.py` de otra skill (`scripts/verify_references.py:411`, `:435`) | Sonda de fixture (Tests, fila 3) |
| `KI-052-4` | `tests/test_root_resolution.py:69` falla en un worktree enlazado del núcleo: exit `1` y `AssertionError` | Tests, fila 4 |
| `KI-052-7` | `skills/env-shielding-auditor/README.md:41` nombra `scripts/shield_audit.sh`, que no existe; el script real es `scripts/env_shielding_auditor.py` | `grep -n shield_audit.sh skills/env-shielding-auditor/README.md` → 1 hit |
| `KI-053-2` (a) | En JS, `outer()` cuyo cuerpo es un `forEach(function…)` de 5 filas mide `lines=5`; el callback se mide aparte, `lines=3`. Sus filas cuentan dos veces | `quality_audit.py --report <fixture nested.js>` |
| `KI-053-2` (b) | Un `def f()` de Python con un literal de diccionario que contiene una fila de solo comentario y una fila en blanco mide `lines=7`. Con la regla de `agents.md §1` deberían ser 5 | `quality_audit.py --report <fixture comments.py>` |
| `KI-055-1` | Siete vectores sin sandbox siguen siendo escribibles (`F-055-N1`: `Q1`-`Q5`, `Q7`, `Q11`). No existe la enumeración medida que exige `RA-19`. Los write-denies `config` y `venv_skillopt` nunca se midieron (`PIPELINE_AUDIT_REPORT-055.md` `F4`) | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md:1990-2020` |
| `KI-055-2` | `scripts/install.py` conserva en silencio un `sandbox.excludedCommands` añadido por el host, aunque `RA-09` prohíbe cualquier entrada | `scripts/install.py:197` |
| `KI-055-3` `Q9` | `RENDER_OWNED_RE` no casa una ruta de host con espacios: `False` | Sonda (Tests, fila 7) |
| `KI-055-3` `Q10` | `prune_rendered_exclusions` sobre un `settings.local.json` que no es un dict lanza `AttributeError: 'list' object has no attribute 'get'`. `tests/test_template_sandbox.py` no fija `Edit(/.agents/venv_skillopt/**)` (0 hits). `tests/test_install_with_env_render.py:20` no tiene tipo de retorno | Tests, filas 8-10 |
| `KI-055-3` `T2-1` | El docstring de `scripts/install.py:176-181` dice que las exclusiones del host quedan intactas, pero `RENDER_OWNED_RE` también poda una línea `python3 -I .agents/scripts/with_env.py <name>` escrita por el host | Lectura de `scripts/install.py:60` y `:176-181` |
| `KI-055-4` | `rules/project_topology.md` §4 no menciona `branch_sovereignty.py`, `ci_gate.py` ni `session_probe.py`, aunque los tres llaman a `gh` | `grep -c -e branch_sovereignty.py -e ci_gate.py -e session_probe.py rules/project_topology.md` → `0` |
| `KI-055-5` | `R7-4` (`workflows/pipeline_workflow.md:16`, `docs/standards/templates/README_TEMPLATE.md:91`), `R7-5` (`agents/devops_agent.md:16`), `PIPELINE_AUDIT_REPORT-055.md` `F1`-`F4` | Lectura de esas líneas |
| `KI-055-6` | `RA-19` prohíbe afirmar un límite, pero no prohíbe prescribir un procedimiento de seguridad sin la enumeración (por ejemplo, la comprobación previa con `git -C .agents status` que ejecutó un `core.fsmonitor` puesto por el agente) | `agents.md` `RA-19` |
| `KI-055-7` | Ningún script escribe `current_sprint.last_audit_sprint`; `session_state.py --help` no tiene ningún subcomando que lo haga | `python3 scripts/session_state.py --help` |
| `KI-055-8` | `agents.md` `RA-09`, `workflows/deployment_workflow.md:31` y `rules/project_topology.md:39` dicen que todo `gh` lo ejecuta el humano, sin la condición que lo justifica (bajo el sandbox) | Lectura de esas líneas |

Estado de la base: `make verify` exit `0` y 1081 tests pasan
(`venv_skillopt/bin/python -m pytest -q` vía `make verify`). Esta sesión corre **sin
el sandbox de la plantilla**: no hay ninguna variable `*proxy*` en el entorno
(`env | grep -i -c proxy` → `0`), igual que en la sesión de despliegue del 055.

Al terminar: los cinco instrumentos del bloque E miden lo que dicen, la enumeración
de `RA-19` existe y cada fila está medida, los vectores que se pueden cerrar con un
deny de plantilla quedan cerrados y medidos de nuevo, y ningún documento prescribe
una regla sin la condición que la justifica.

---

## Design

| ID | Decisión | Alternativa rechazada | Motivo |
| :--- | :--- | :--- | :--- |
| `D1` | **Dos olas en orden.** La Ola A (bloque E, `KI-055-3`, `-5`, `-7` y `-8`) es determinista y de bajo riesgo, y va primero. La Ola B (`KI-055-1`, `-2`, `-4` y `-6`) es el bloque del sandbox. | Un orden único por fichero, o separar la Ola B en el Sprint 057 | Así lo decidió el humano el 2026-10-12. Si la Ola B se atasca, la Ola A ya está en la rama y no se pierde (Abort criterion). |
| `D2` | `KI-052-1`: el regex acepta las dos formas de Status, `Status: Superseded` y `**Status**: \`Superseded…\``, con la regla anclada al inicio de línea. | Normalizar el formato de las 17 ADR | El regex lee la forma que las ADR usan de verdad; reescribir registros sellados no corrige el instrumento. |
| `D3` | `KI-052-3` `NF-2`: las tres comprobaciones por subcadena de `invoked_by:` (`:547`, `:659`, `:698`) pasan a usar `_invoked_by_line(text) != ""`. Esa función ya existe y ya distingue declaración de prosa. `NF-1`: un token de ruta precedido por `/` solo cuenta si el segmento anterior es el directorio de la propia skill. El token `scripts.<stem>` en forma de punto exige que no le preceda `.`/`\w`, con la frontera que ya tiene. | Un parser nuevo de declaraciones | La función correcta ya existe en el mismo fichero. Dos unidades, porque son dos defectos con dos tests. |
| `D4` | `KI-052-4`: el test compara con `_mode.is_nucleus()`, que ya entiende los worktrees, contra el valor esperado por forma de checkout (`.git` es un directorio, o un fichero `gitdir:` que apunta a `.git/worktrees/`). No lo compara con el predicado ingenuo `.git` is_dir. | Saltar el test dentro de un worktree | Saltarlo ocultaría precisamente el caso que `scripts/_mode.py:52-76` existe para cubrir. |
| `D5` | `KI-052-7`: el README pasa a nombrar el script real, `python3 .agents/skills/env-shielding-auditor/scripts/env_shielding_auditor.py`. | Escribir `shield_audit.sh` | Un shell nuevo duplicaría el `.py` y sería un mecanismo más que necesita un invocador (`RA-16`). |
| `D6` | `KI-053-2`, **definición decidida**. (a) En JS/TS, una función anidada dentro de una expresión es una frontera, igual que un `def` anidado en Python: en la unidad que la encierra cuentan solo las filas de la sentencia que la contiene, nunca su cuerpo. (b) En los dos caminos se excluyen las filas en blanco y las de solo comentario, también dentro de una sentencia de varias filas. Python las detecta con stdlib `tokenize` (filas con `COMMENT`/`NL` y ningún token significativo), y JS/TS con los nodos `comment` de tree-sitter y las filas vacías. `agents.md §1` `max_lines_per_func` declara las dos reglas. | Mantener el doble conteo y documentarlo | La regla de `agents.md §1` ya excluye las filas de solo comentario. Los dos cambios solo reducen el conteo, así que no pueden convertir una unidad conforme en una violación (`KI-053-2`, "over-count only"), y `make quality-audit` sigue en 0. |
| `D7` | `KI-055-3`: `RENDER_OWNED_RE` acepta rutas con espacios, anclado al sufijo `-I <ruta>/scripts/with_env.py <name>`. `prune_rendered_exclusions` sale sin escribir cuando el JSON raíz no es un dict, igual que cuando `sandbox` no lo es. El docstring dice lo que poda de verdad, incluida una línea `with_env.py` escrita por el host (`T2-1`, en la dirección segura según `D12` del 055). | Ampliar el regex a cualquier línea que contenga `with_env` | Mantiene el anclaje. Un regex más amplio podaría líneas del host sin relación. |
| `D8` | `KI-055-2`: si encuentra una entrada de `sandbox.excludedCommands` que no sea render-owned, `scripts/install.py` **rechaza** la instalación con exit `2` y nombra cada entrada y el motivo `N1`. No toca el fichero. El humano retira la entrada y vuelve a correr la instalación. | Aviso no bloqueante | `RA-09` prohíbe *cualquier* entrada, añadida por el framework o por el host. Un aviso que deja la instalación en verde acepta la puerta de escape que la regla prohíbe. Riesgo: un host con una entrada heredada ve fallar la instalación. Esa es la intención, y el mensaje le da el arreglo exacto. |
| `D9` | `KI-055-7`: subcomando nuevo `python3 scripts/session_state.py mark-audited --report docs/audits/PIPELINE_AUDIT_REPORT-<NNN>.md`. Comprueba que el informe existe y que su `<NNN>` es el `current_sprint.id` o uno anterior, y después escribe `current_sprint.last_audit_sprint = NNN`. Si no, exit `2`. Lo invoca `workflows/audit_workflow.md` en su último paso. | Seguir editando el ancla a mano | El campo lo lee `docs_freshness_check.py:614`, y un campo que lee un gate no se escribe a mano (`RA-16`; carrera de `F5` desde el Sprint 042). |
| `D10` | `KI-055-8`: la frase pasa a ser "**bajo el sandbox de la plantilla** todo `gh` lo ejecuta el humano (falla con `x509`, `S-5`, y no puede haber ninguna exclusión, `N1`)". Una sesión sin sandbox puede ejecutar `gh` el agente, con dos condiciones: lo comprueba antes de cada llamada (`env` sin `HTTPS_PROXY`) y conserva `RA-13` (el gate se observa antes de la acción). La redacción canónica va en `rules/project_topology.md` §4, y `RA-09` y `deployment_workflow.md` la referencian (`RA-14`). | Mantener la regla incondicional | La regla bloquea un despliegue seguro sin ninguna razón que se aplique. El 055 lo tuvo que resolver como desviación humana. |
| `D11` | **`KI-055-1`, enumeración.** `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` lista cada punto de entrada que Claude Code ejecuta fuera del sandbox en un host: los 7 hooks de `claude/settings.hooks.json` y todo lo que importan (raíces de `sys.path` e intérprete), los 2 lanzadores de `claude/mcp.json`, los `hooks:` de subagente (`.claude/agents` → `.agents/agents`), las recetas de `make` que ejecuta el humano, el `git` sin sandbox (`core.fsmonitor`, `.git/hooks` del host y del submódulo) y los ficheros de settings de usuario y de proyecto. Por entrada registra *qué ejecuta* y *si el agente con sandbox puede escribirlo*, con la misma medición del 055 (`claude -p` headless, CLI 2.1.119, fixture de host con `.env` de valor de fixture, `allowUnsandboxedCommands: false`, cada caso en su propia llamada). Incluye los trees `config` y `venv_skillopt` (`F4`). | Enumerar desde la documentación sin medir | `RA-19` exige medición, y la ronda 5 del 055 midió que una comprobación prescrita era ella misma un vector. |
| `D12` | **`KI-055-1`, remedio principal**: en la plantilla, el deny de escritura de seis subárboles se sustituye por uno de todo el submódulo, `./.agents` (y `Edit(/.agents/**)` en `permissions.deny`). En modo host la sesión ya **debe** dejar `git -C .agents status --porcelain` vacío (`§3 jurisdiction`), así que no se le quita ninguna escritura legítima. De una vez cierra `Q1` (`.agents/_mode.py` en `sys.path`), `Q3` (`mcp_servers/`), `Q4` (`agents/`), `Q5` (`Makefile`) y la parte de `Q11` dentro de `.agents`. Para `Q2` se añaden denies de `./.git/modules/.agents/config`, `./.git/config` y `./.git/hooks`, **solo si** la medición de `D11` muestra que el sandbox no los protege ya y que denegarlos no rompe `git commit`/`git push` del agente. Cada vector cerrado se mide de nuevo y se anota en la enumeración. | Parchear vector a vector (`sys.path` en cuatro hooks, `-I` en MCP, etc.) | Un solo deny cubre la clase entera. Parchear vector a vector es justo lo que `RA-19` prohíbe ("cerrar solo el vector medido"). `-I` en el lanzador `graphify` de `claude/mcp.json` se añade aparte (`Q3`), porque el paquete `graphify/` en la raíz del host queda fuera de `./.agents`. |
| `D13` | **Lo que queda abierto se declara.** `Q7` (`python3` de `PATH` con un venv del host activo) y lo que la enumeración encuentre fuera del alcance de la plantilla quedan como filas abiertas, con propietario. `F-055-N1` se marca como cerrado **solo** si todas las filas de la enumeración quedan "no escribible por el agente". Si no, sigue abierto con la enumeración enlazada, y la redacción "reduce la exposición, no es un límite" no cambia. | Marcar `F-055-N1` como cerrado al entregar la enumeración | El defecto son los vectores, no la falta de una lista. |
| `D14` | `KI-055-6`: `RA-19` añade una prohibición: ningún documento prescribe un procedimiento de seguridad (una comprobación previa, una ruta "endurecida", una secuencia "segura") que ejecute algo que el agente puede escribir, salvo que la enumeración de `D11` cubra esa ejecución. La enmienda la redacta `rule_validator`. | Prohibición aparte, `RA-20` | Es el mismo defecto que `RA-19` en otra forma, y `RA-05`..`RA-19` no se renumeran. |
| `D15` | `KI-055-4`: tres filas en la tabla de §4 de `rules/project_topology.md`, una por script (`scripts/branch_sovereignty.py`, `scripts/ci_gate.py`, `scripts/session_probe.py`). Cada una indica el `gh` que lanza, su firma bajo el sandbox (heredada de `S-5`: `x509`) y quién lo ejecuta según `D10`. | Medir de nuevo cada script bajo el sandbox | Los tres lanzan `gh` como subproceso, con el mismo binario y la misma pila TLS que `S-5`. La fila cita `S-5` como evidencia y dice que es una derivación, no una medición nueva. |
| `D16` | `KI-055-5`: `R7-4`/`R7-5`/`F1`: las tres frases dejan de reformular la regla. Pasan a ser un puntero a la fila `S-3` de §4 que nombra al actor (el humano). Así se reduce también `F3`. `F2`: el registro `F-055-N1` añade una línea de correspondencia (`Q6`, `Q8`-`Q10` del `SPRINT_LOG.md` del 055 → `KI-055-2`/`KI-055-3`). No se editan los registros sellados del 055. `F4`: queda cubierto por `D11`. | Renombrar los `Q` del `SPRINT_LOG.md` sellado del 055 | Un registro sellado no se reescribe. |
| `D17` | **Disparador de la nueva medición** (rechazo de Filter 5 de `token_economy_agent`, decidido por el humano el 2026-10-12): `scripts/session_start.py --boot` lee la versión de la fila `Measuring CLI` de `rules/project_topology.md` §4 y la compara con `claude --version`. Si no coinciden, emite un hallazgo de readiness *advisory* que nombra la matriz que hay que volver a medir. Si no hay binario `claude` (CI, Cursor), lo dice y no emite nada más. | Texto en *Re-measure trigger* sin detector, o exit `2` en el boot | Un disparador en prosa no tiene invocador (`RA-16`). Bloquear el boot tras cada actualización del CLI pararía toda sesión, incluso las que no tocan el sandbox; el aviso sigue el mismo patrón que el de higiene del ancla. |

---

## Work

**Ola A**: determinista, de bajo riesgo.

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `A1` | `scripts/docs_freshness_check.py` (+ `tests/test_docs_freshness_check.py`, `fix(`) | modify: `ADR_STATUS_SUPERSEDED_RE` acepta `**Status**: \`Superseded` (`D2`, `KI-052-1`) | low | `implementer_agent` | ✅ `7f0f926` |
| `A2` | `scripts/verify_references.py` (+ `tests/test_verify_references.py`, `fix(`) | modify: las tres comprobaciones por subcadena de `invoked_by:` usan `_invoked_by_line` (`D3`, `NF-2`) | medium | `implementer_agent` | ✅ `a740f88` |
| `A3` | `scripts/verify_references.py` (+ `tests/test_verify_references.py`, `fix(`) | modify: frontera de token entre rutas en `_skill_doc_names_script` (`D3`, `NF-1`) | medium | `implementer_agent` | ✅ `b083715` |
| `A4` | `tests/test_root_resolution.py` | modify: aserción por forma de checkout, válida en worktrees (`D4`, `KI-052-4`); commit `test(` | low | `implementer_agent` | ✅ `eccb6ea` |
| `A5` | `skills/env-shielding-auditor/README.md` | modify: nombrar `scripts/env_shielding_auditor.py` (`D5`, `KI-052-7`) | low | `doc_orchestrator` | ✅ `77eb3c4` |
| `A6` | `scripts/quality_audit.py` (+ `tests/test_quality_audit.py`, `fix(`) | modify: frontera de función anidada en JS/TS (`D6` a) | medium | `implementer_agent` | ✅ `2e4487c` |
| `A7` | `scripts/quality_audit.py` (+ `tests/test_quality_audit.py`, `fix(`) | modify: excluir filas en blanco y de solo comentario dentro de sentencias de varias filas, en Python y en JS/TS (`D6` b) | medium | `implementer_agent` | ✅ `9f02419` |
| `A8` | `agents.md` | modify: `§1` `max_lines_per_func` y la fila JS/TS de `linter_command` declaran las dos reglas de `D6` | low | `rule_validator` | ✅ `d40f3da` |
| `A9` | `scripts/install.py` (+ `tests/test_install_with_env_render.py`, `fix(`) | modify: `RENDER_OWNED_RE` con rutas con espacios y docstring alineado con `T2-1` (`D7`, `Q9`) | low | `implementer_agent` | ✅ `b2bf703` |
| `A10` | `scripts/install.py` (+ `tests/test_install_with_env_render.py`, `fix(`) | modify: sin crash cuando la raíz no es un dict (`D7`, `Q10`) | low | `implementer_agent` | ✅ `8dba69b` |
| `A11` | `tests/test_template_sandbox.py` | modify: fijar `Edit(/.agents/venv_skillopt/**)` (`Q10`); commit `test(` | low | `implementer_agent` | ✅ `40b2ffc` |
| `A12` | `tests/test_install_with_env_render.py` | modify: tipos de retorno y docstrings (`Q10`); commit `test(` | low | `implementer_agent` | ✅ `2016dad` |
| `A13` | `scripts/session_state.py` (+ `tests/test_session_state.py`) | modify: subcomando `mark-audited` (`D9`, `KI-055-7`); commit `feat(` | medium | `implementer_agent` | ✅ `46059d8, 076145c` |
| `A14` | `workflows/audit_workflow.md` (+ `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` regenerada con `python3 scripts/map_workflows.py`, compañero generado que `make verify` exige) | modify: el último paso invoca `session_state.py mark-audited` (`D9`, `RA-16`) | low | `doc_orchestrator` | ✅ `8035aea` |
| `A15` | `rules/project_topology.md` | modify: fila `gh` de §4 con la condición "bajo el sandbox" (`D10`, `KI-055-8`) | medium | `rule_validator` | ✅ `45743dd, c025350` |
| `A16` | `agents.md` | modify: `RA-09` referencia la condición de `A15` (`D10`) | medium | `rule_validator` | ✅ `d40f3da` |
| `A17` | `workflows/deployment_workflow.md` (+ `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` regenerada con `python3 scripts/map_workflows.py`, compañero generado que `make verify` exige) | modify: `pr_flow`, `github_release` y la nota de la línea 31 con la condición (`D10`) | medium | `doc_orchestrator` | ✅ `d2c3aa4` |
| `A18` | `rules/qa_and_testing.md` | modify: `§5`, la frase de `with_env.py` nombra al actor y apunta a `S-3` (`D16`, `F1`) | low | `rule_validator` | ✅ `a86570f` |
| `A19` | `workflows/pipeline_workflow.md` (+ `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` regenerada con `python3 scripts/map_workflows.py`, compañero generado que `make verify` exige) | modify: Phase 2 apunta a `S-3` y nombra al humano (`D16`, `R7-4`) | low | `doc_orchestrator` | ✅ `29781aa` |
| `A20` | `docs/standards/templates/README_TEMPLATE.md` | modify: línea 91 (`D16`, `R7-4`) | low | `doc_orchestrator` | ✅ `6f1cc0c` |
| `A21` | `agents/devops_agent.md` | modify: línea 16 cita la fila de riesgo residual (`D16`, `R7-5`) | low | `doc_orchestrator` | ✅ `be7c041` |
| `A22` | `workflows/repository_hardening_workflow.md` | modify: la nota de `gh` (línea 44) apunta a la fila `gh` de §4 con la condición de sandbox (`D10`). **Unidad descubierta en la Fase 6** por el grep de propagación `RA-14` de `D10`; no estaba en el plan aprobado | low | `doc_orchestrator` | ✅ `3d8fe3f` |

**Ola B**: sandbox.

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `B1` | `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` | create: enumeración medida en la base (`D11`, `KI-055-1`, `F4`) | high | `doc_orchestrator` (escritura; la medición `claude -p` la ejecuta la sesión padre, porque `principal_agent` no tiene `Bash` ni `Write`) | ✅ `c7c0701` |
| `B2` | `claude/settings.hooks.json` (+ `tests/test_template_sandbox.py`, `fix(`) | modify: deny de escritura de `./.agents` completo y `Edit(/.agents/**)`; denies de `.git` solo si `B1` los justifica (`D12`) | high | `implementer_agent` | ✅ `d70d00c` |
| `B3` | `claude/mcp.json` (+ `tests/test_mcp_template.py`, nuevo, `fix(`) | modify: `-I` en el lanzador `graphify` (`D12`, `Q3`) | medium | `implementer_agent` | ✅ `05c74a6` |
| `B4` | `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` | modify: nueva medición de cada vector tras `B2`/`B3` (`D12`, `D13`) | high | `doc_orchestrator` (escritura; medición en la sesión padre) | ✅ `6fd75ec` |
| `B5` | `scripts/install.py` (+ `tests/test_install_with_env_render.py`, `fix(`) | modify: rechazo con exit `2` de un `excludedCommands` del host (`D8`, `KI-055-2`) | medium | `implementer_agent` | ✅ `3bfa1d9` |
| `B6` | `rules/project_topology.md` | modify: filas `N3` y de riesgo residual según la enumeración; tres filas de scripts `gh` (`D13`, `D15`, `KI-055-4`) | medium | `rule_validator` | ✅ `9171740` |
| `B7` | `agents.md` | modify: `RA-19` amplía la prohibición a procedimientos prescritos (`D14`, `KI-055-6`); lista de trees de `RA-09` según `B2` | high | `rule_validator` | ✅ `5083e70` |
| `B8` | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify: estado de `F-055-N1` según `D13` y correspondencia de `Q` (`D16`, `F2`) | low | `doc_orchestrator` | ✅ `50b5281` |
| `B9` | `scripts/session_start.py` (+ `tests/test_session_start.py`) | modify: aviso de readiness del boot cuando `claude --version` no coincide con la fila `Measuring CLI` de `rules/project_topology.md` §4; no bloquea (`D17`); commit `feat(` | medium | `implementer_agent` | ✅ `8bb0d1a` |

Los ficheros de cierre del directorio del sprint (`SPRINT_LOG.md`, `task_scope.md`,
`agent_assignment.md`, `skill_assignment.md`) los producen las Fases 3 y 4. No son
filas de trabajo.

---

## Dependencies

None.

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `session_state.py mark-audited` (por sprint auditado) | script | `workflows/audit_workflow.md`, último paso (`A14`) |
| Rechazo de `excludedCommands` del host en la instalación | script | `scripts/install.py` `main` (existente, invocado por `scripts/install.sh` y por el humano) |
| Enumeración de `RA-19` (se repite cuando cambia la versión del CLI) | agent judgment, medición con `claude -p` headless: no hay alternativa determinista, porque la medición necesita una sesión de Claude Code con sandbox | El disparador es determinista: `scripts/session_start.py --boot` avisa cuando `claude --version` no coincide con la fila `Measuring CLI` (`B9`, `D17`) |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 31 | Count of rows in Work tables (22 + 9; `A22` discovered in Phase 6) |
| Subagents dispatched | Estimación, no medida: 30 unidades en lotes por perfil (≈ 8 despachos de autor: `implementer_agent` ×3 lotes, `rule_validator` ×2, `doc_orchestrator` ×2, `skill_architect` ×1) + Gate 1 + Gate 2 + 4 ya despachados en Fases 3-5 (`orchestrator`, `agent_orchestrator`, `skill_architect`, `rule_validator`, `token_economy_agent`) | Conteo de despachos en `SPRINT_LOG.md` al cierre |
| Prior session ratio | 4.4 (sesión de esta planificación, `ea40fe66-042d-489e-b92d-80131c56f749`, medido 2026-10-12 durante la Fase 1: pico 115942 / primer turno 26278). No es un sprint anterior: la sesión del 055 no está en el ancla | `python3 scripts/session_cost.py --from-anchor --json` |
| Mediciones `claude -p` de la Ola B | Presupuesto: ≤ 40 llamadas headless entre `B1` y `B4` (≈ 15 entradas de la enumeración × 2 rondas + controles). Si se supera, el exceso se registra en `SPRINT_LOG.md` y se vuelve a este Cost antes de seguir | Conteo de ejecuciones en `SANDBOX_ENUMERATION.md` §Method |

---

## Tests

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| `is_adr_superseded` sobre una ADR con `**Status**: \`Superseded by ADR-0017\`` devuelve `True` (`A1`) | **Yes**: this is the defect | Sonda `python3 -I -c` con fixture → `KI-052-1 superseded detected: False`, exit `0` |
| Un fichero con `invoked_by:` solo en prosa no queda resuelto (`A2`) | **Yes**: this is the defect | Sonda con fixture `orphan.py` → `_skill_script_directly_resolved` `True`, `_invoked_by_line` `''`, exit `0` |
| `otra/scripts/env.py` en un README no resuelve el `scripts/env.py` de otra skill (`A3`) | **Yes**: this is the defect | unverified: la sonda la escribe `A3` como test. El regex (`scripts/verify_references.py:411`) acepta `/` como frontera por diseño, según su docstring |
| `test_mode_detection_still_answers_through_the_shared_root` pasa en un worktree enlazado (`A4`) | **Yes**: this is the defect | `git worktree add --detach <scratch>/wt056 HEAD` + `pytest tests/test_root_resolution.py -k mode_detection` → exit `1`, `AssertionError` en `:69` |
| `outer()` con un callback anidado mide solo sus filas propias (`A6`) | **Yes**: this is the defect | `venv_skillopt/bin/python -I scripts/quality_audit.py --report <fixture nested.js>` → `outer lines=5`, exit `0` (esperado tras el arreglo: `1`) |
| Las filas de comentario y en blanco dentro de un literal de varias filas no cuentan (`A7`) | **Yes**: this is the defect | La misma orden sobre `<fixture comments.py>` → `f lines=7`, exit `0` (esperado: `5`) |
| `RENDER_OWNED_RE` casa una ruta de host con espacios (`A9`) | **Yes**: this is the defect | Sonda `python3 -I -c` → `Q9 spaced path matched: False`, exit `0` |
| `prune_rendered_exclusions` sobre un `settings.local.json` `[]` no lanza excepción (`A10`) | **Yes**: this is the defect | Sonda → `AttributeError 'list' object has no attribute 'get'`, exit `0` (excepción capturada por la sonda) |
| `tests/test_template_sandbox.py` fija `Edit(/.agents/venv_skillopt/**)` (`A11`) | **Yes**: this is the defect | `grep -c 'venv_skillopt/\*\*' tests/test_template_sandbox.py` → `0`, exit `1` |
| `session_state.py mark-audited` escribe `last_audit_sprint` y rechaza un informe inexistente (`A13`) | **Yes**: this is the defect | `python3 scripts/session_state.py --help` lista `claim`..`open-sprint` y ningún `mark-audited` (0 hits), exit `0` |
| `install.py` rechaza con exit `2` un `excludedCommands` del host (`B5`) | **Yes**: this is the defect | unverified: la llamada se conserva en `scripts/install.py:197`. La firma del exit la mide el test de `B5` contra la base antes del arreglo (`KI-053-4`) |
| El boot avisa cuando la versión del CLI no coincide con la fila `Measuring CLI` (`B9`) | **Yes**: this is the defect | `grep -c 'Measuring CLI' scripts/session_start.py` → `0`, exit `1` |
| La plantilla deniega escritura en `./.agents` (`B2`) | **Yes**: this is the defect | `grep -c '"./.agents"' claude/settings.hooks.json` → `0` (solo subárboles, líneas 62-72) |
| Suite completa y gates (`make verify`) | **No**: this is a regression to protect | `make verify` → exit `0`, `1081 passed`, ruff `All checks passed!` |
| Los siete ficheros de test que toca el sprint | **No**: this is a regression to protect | `pytest -q` sobre esos siete ficheros → `204 passed`, exit `0` |

---

## Verification

| Command | Expected | Dry run | Positive control |
| :--- | :--- | :--- | :--- |
| `make verify` | exit `0` | exit `0`, `1081 passed` | n/a (expected is not "no output") |
| `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider tests/test_docs_freshness_check.py tests/test_verify_references.py tests/test_quality_audit.py tests/test_install_with_env_render.py tests/test_template_sandbox.py tests/test_session_state.py tests/test_root_resolution.py` | exit `0` | exit `0`, `204 passed` | n/a |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/056-core-pipeline/IMPLEMENTATION_PLAN.md` | exit `0` | exit `0` (`[OK]`) tras corregir una tubería escapada en Tests (primera ejecución: exit `2`) | n/a |
| `grep -c -i 'unsandboxed session' rules/project_topology.md` (fila canónica de `D10`); `RA-09` y `deployment_workflow.md` la citan en lugar de reformularla (`RA-14`, hallazgo 6 de Phase 4.3) | `≥ 1` | `0`, exit `1`: el defecto está presente | n/a |
| `python3 scripts/check_fix_reproduces.py --range d88593c..HEAD` | exit `0` | run at close: necesita los commits `fix(` del sprint en `ai-sprint/056`, que todavía no existen | n/a |
| `grep -rn -i -e 'is the boundary' -e 'boundary is that' -e 'framework-level boundary' -e 'has no secret path' -e 'no autonomous secret path' agents.md agents rules workflows docs/standards config scripts/with_env.py Makefile` | sin salida, exit `1` | sin salida, exit `1` | `grep -rn -i -e 'is the boundary' <scratch>/pc.md` sobre un fichero con `the write-deny is the boundary` → 1 hit, exit `0` |
| `grep -n shield_audit.sh skills/env-shielding-auditor/README.md` | sin salida, exit `1` | 1 hit, exit `0`: el defecto está presente, y la misma ejecución sirve de control positivo | El dry run de esta misma fila (1 hit) |
| `grep -c -e branch_sovereignty.py -e ci_gate.py -e session_probe.py rules/project_topology.md` | `≥ 3` | `0`, exit `1` | n/a |
| `git worktree add --detach <scratch>/wt056 HEAD` y después `venv_skillopt/bin/python -m pytest -q tests/test_root_resolution.py` dentro del worktree | exit `0` | exit `1` (`mode_detection` falla) | n/a |
| `python3 scripts/session_state.py mark-audited --report docs/audits/PIPELINE_AUDIT_REPORT-999.md` | exit `2` (el informe no existe) | run at close: el subcomando no existe en la base (`--help` → `0` hits) | n/a |
| Cada fila de `SANDBOX_ENUMERATION.md` tiene `Writable by agent` con valor `yes`/`no` y una evidencia | 0 filas sin valor | run at close: el documento no existe hasta `B1` | n/a |
| `venv_skillopt/bin/python -m graphify update .` | exit `0` | run at close: reescribe `graphify-out/` y forma parte del gate de commit (`§2 graph_sync`) | n/a |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | `§1` `max_lines_per_func` y la fila JS/TS (`A8`); `RA-09` con la condición de sandbox (`A16`) y su lista de trees (`B7`); `RA-19` con la prohibición de procedimientos prescritos (`B7`) |
| `rules/project_topology.md` | §4: fila `gh` (`A15`), filas `N3` y de riesgo residual (`B6`), tres filas de scripts `gh` (`B6`) |
| `rules/qa_and_testing.md` | `§5`, frase de `with_env.py` (`A18`) |
| `workflows/audit_workflow.md` | Último paso: `mark-audited` (`A14`) |
| `workflows/deployment_workflow.md` | `pr_flow`, `github_release` y la nota de sandbox (`A17`) |
| `workflows/pipeline_workflow.md` | Phase 2 (`A19`) |
| `agents/devops_agent.md` | `secret_sovereignty` (`A21`) |
| `docs/standards/templates/README_TEMPLATE.md` | Línea 91 (`A20`) |
| `skills/env-shielding-auditor/README.md` | Uso (`A5`) |
| `claude/settings.hooks.json`, `claude/mcp.json` | Denies y lanzador MCP (`B2`, `B3`) |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | `F-055-N1` (`B8`) |
| `docs/sprints/056-core-pipeline/SANDBOX_ENUMERATION.md` | Nuevo (`B1`, `B4`) |
| `scripts/session_start.py` | Aviso de readiness por versión del CLI (`B9`) |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Se regenera con `scripts/map_workflows.py` si cambian `audit_workflow.md`/`deployment_workflow.md`/`pipeline_workflow.md`. No se edita a mano. |
| `CHANGELOG.md`, `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Entrada del sprint y estado de los 13 ítems (cierre, `RA-05`) |

**Measured figures.** Cada número de Context, Design y Verification lleva su comando en
la misma fila o en la tabla de mediciones de Context.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `F3` completo: consolidar en `§4` las reformulaciones de `agents.md` `RA-09` y de `rules/graphify.md:24-25` | `RA-09` es la propia regla y sigue siendo canónica. `rules/graphify.md` queda para `/agents:extract` en el cierre, como recomendó `PIPELINE_AUDIT_REPORT-055.md` |
| `Q7` (intérprete `python3` de `PATH` en los hooks) | Depende del entorno del humano, no de la plantilla. Queda como fila abierta de la enumeración, con propietario (`D13`) |
| `KI-054-1`..`KI-054-6` y el resto de la cola | No están asignados al 056 en la hoja de ruta. Siguen en su sección de `021-030-program-queue.md` |
| Medir otra versión del CLI que no sea 2.1.119 | La enumeración mide la versión instalada. La regla de nueva medición ya existe (`rules/project_topology.md` §4) |

---

## Abort criterion

1. **Remediación en la Ola B.** Si una unidad de la Ola B provoca `remediation_workflow.md`
   Phase 0 (más de 3 `REJECTED` consecutivos sobre el mismo bloque), las unidades de
   la Ola B que no hayan pasado el Gate 1 se revierten en `ai-sprint/056`. El sprint
   se cierra con la Ola A y con `B1` (la enumeración en la base, que es una medición
   y no cambia comportamiento), y el resto se enruta a un sprint propio.
2. **`B2` rompe el flujo del agente en el host.** Si la medición de `B4` muestra que el
   deny de `./.agents` impide algo que el host necesita, por ejemplo que el agente
   con sandbox haga `git commit` en el host o que se carguen los hooks, `B2` se
   revierte y `D12` vuelve a la Phase 1 con la medición adjunta. No se ensancha la
   excepción sin un plan.
3. **`D6` hace que `make quality-audit` deje de dar 0.** Es imposible por construcción
   (solo reduce el conteo). Si ocurre, la unidad tiene un defecto y se revierte.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal (human, attended chat approval) |
| **Date** | 2026-10-12 |
| **Plan commit at approval** | `2d5504e` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
