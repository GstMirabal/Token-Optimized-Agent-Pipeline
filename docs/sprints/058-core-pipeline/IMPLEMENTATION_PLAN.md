# Implementation Plan: Sprint 058 — upstream-channel-and-reproduce-first

**Canonical path**: `docs/sprints/058-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/058` · **Base**: `main` at `f0b11f8` (`v4.40.0`)
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
> Fuentes: (1) el `Out of scope` de `docs/sprints/057-core-pipeline/IMPLEMENTATION_PLAN.md:316-326`;
> (2) el borrador de 057 (`docs/plans/057-upstream-intake-and-backlog-DRAFT.md`, nunca
> commiteado y borrado en la Phase 5 de 057), reconstruido el 2026-10-28 desde la última
> lectura completa en las transcripciones de sesión y contrastado con la reconstrucción
> por sus llamadas Write/Edit (ambas idénticas, 242 líneas); (3) los dos mensajes del
> informe upstream del host H1 (2026-10-22, pin `v4.38.0`), recuperados de la misma
> fuente. Este plan copia de ellos lo que 058 necesita: lo que quede solo en las
> transcripciones se pierde.

---

## Context

057 dejó tres bloques con destino 058 (`057 IMPLEMENTATION_PLAN.md:320-321` y la nota
de proyecto del 2026-10-28):

| Bloque | Problema medido |
| :--- | :--- |
| Canal upstream host → nucleus | `agents.md §4 feedback_upstream` dice *quién* puede escribir, pero no *cómo viaja* un hallazgo, *dónde espera*, *quién lo triagea* ni *cómo se cierra*. El host H1 midió 9 hallazgos de clase framework de un sprint con 0 menciones en `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` semanas después, 15 documentos de handoff libres sin estado y una regla propia de 10 puntos (R-1..R-10) que divergió de la copia del nucleus. Los 43 veredictos de 057 tampoco constan en el registro del nucleus: `rg -c "host H1" docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` no imprime nada |
| Reglas reproduce-first | R-4, R-5/C-6, R-6 (= `KI-054-1`), R-8, R-9/A-2, R-10, A-1 y A-3 (= `KI-054-2`) aceptadas el 2026-10-22 y sin publicar; el host las mantiene como delta local hasta el pin que las traiga |
| PRs de Dependabot | #88 `claude-agent-sdk` `0.2.88` → hoy `0.2.174` (`pip index versions claude-agent-sdk`); #89 `graphifyy` `0.8.30` → hoy `0.9.97` (`pip index versions graphifyy`). Desde `0.9.70` graphify deja fuera del grafo el JSON de datos: 55 ficheros, entre ellos todo `config/*.json` y `claude/settings.hooks.json` |

Más tres KI de 057 que el humano incluyó el 2026-10-28: `KI-057-3`, `KI-057-4` y `KI-057-6`
(`docs/roadmaps/core/pipeline/021-030-program-queue.md:397-399`).

Cuando 058 termine debe cumplirse lo siguiente:

| Resultado | Medida |
| :--- | :--- |
| Un hallazgo del host viaja con schema y estado | `python3 scripts/upstream_outbox.py check <outbox>` valida el template y rechaza (exit `2`) una entrada `genericized: false` que se pretenda enviar |
| El nucleus ve la cola de intake | `--boot` lista las entradas pendientes de los hosts registrados (canal A) |
| Un issue `host-finding` se filtra sin agente | `.github/workflows/host-finding-intake.yml` etiqueta el issue sin interpolar el texto del issue en ningún `run:` |
| Reglas R-4, R-5, R-8, R-9, R-10 y A-1 publicadas con instrumento | cada una nombra su check determinista (sección Mechanisms) |
| Replay para JS/TS | `scripts/check_fix_reproduces.py` replays a vitest test id instead of reporting `UNREPLAYED` |
| Los comandos de Phase 7 resuelven en un host | `agents.md §0` declara la forma host y la forma nucleus una sola vez |
| Dependencias | #88 integrado; #89 integrado o cerrado según la medición D-02 |

---

## Design

### D1 — Canal upstream: ampliación de `agents.md §4`, sin `RA-20` (decidido 2026-10-22/23)

Se amplía `§4 feedback_upstream`. No se crea un `RA-20`, porque un RA aparte repetiría la
regla (`RA-14`). Decisiones confirmadas en el debate de 057 (borrador, sección «Canal upstream»):

| # | Decisión |
| :--- | :--- |
| Q1 | El schema del outbox es del nucleus: template `docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json` + validador `scripts/upstream_outbox.py` |
| Q3 | Entrada `drafted` envejecida: advisory (exit `0`, una línea por entrada). Pasa a gate (exit `2`) solo con datos de varios sprints, en un sprint posterior |
| Q4 | El triage de intake es obligatorio en la Phase 1 de cada sprint nucleus; `--boot` lista la cola |
| Q5 | El outbox sustituye a los documentos de handoff libres. Un documento libre de un tercero no se triagea: se devuelve con la instrucción de rellenar el schema. Los documentos antiguos de un host son del host; su cierre los señala como advisory |
| Q6 | Ampliar `§4`; sin `RA-20` |
| Genericización | El validador comprueba `genericized` y busca rutas absolutas, emails y patrones de secreto **en el host, antes de cualquier transporte**. El filtro del nucleus es la segunda línea |

**Schema de una entrada** (Q1, con los campos de la propuesta del host H1 más `recurs` y `channel`):
`id`, `title`, `defect`, `evidence` (`command` + `output`), `nucleus_artifact`,
`proposed_change`, `pin`, `genericized` (bool), `channel` (`A` | `B` | `C`), `recurs`
(opcional, id de un hallazgo cerrado del nucleus) y `status` (`drafted` → `sent:<ref>` →
`triaged:<verdict>` → `shipped:<version>` | `rejected:<reason>`).

**El escaneo de genericización es un denylist de patrones** y no hace afirmación de cobertura
(`agents.md §1 fail_closed_claims`). Comprueba exactamente tres familias, que su docstring
enumera: rutas absolutas POSIX y Windows, direcciones de email y las formas de asignación de
secreto `SECRET_ASSIGNMENT` y `UNQUOTED_ASSIGNMENT` de `hooks/on_commit.py`, importadas y no
copiadas, para que no haya dos listas que diverjan. El control real es `genericized: true`,
que firma el humano del host. El escaneo es un tope que reduce errores, no una garantía.

### D2 — Transporte por canal (Q2)

| Canal | Para | Mecanismo |
| :--- | :--- | :--- |
| A | Hosts del mismo maintainer | Pull desde `--boot`: `scripts/upstream_intake.py` lee los outboxes listados en `.upstream_hosts.json`, en la raíz del nucleus. Ese fichero está en gitignore y nunca se commitea (`RA-15`). Cada lado escribe solo en su repo; el host lee los veredictos en `UPSTREAM_FINDINGS_FROM_HOSTS.md`. Las sesiones del nucleus no corren con sandbox, así que leer fuera del working directory funciona (borrador 057, medición de transcripts: 0 Bash sin sandbox en 26 sesiones porque no hay sandbox) |
| B | Terceros, hallazgos no sensibles | `upstream_outbox.py export --id <id>` escribe el cuerpo del issue y el comando exacto `gh issue create --template host-finding.yml --body-file <file> --label host-finding`; el humano ejecuta esa única acción y el agente marca `sent:#N` |
| C | Todo lo que toque `RA-09`/`RA-19`, secretos, hooks o sandbox | Private Vulnerability Reporting. `export` se niega (exit `2`) con `channel: C`; un issue público está prohibido |

**Superficie S0 del canal A.** El texto del host es dato no confiable que entra en el contexto
de una sesión del nucleus. `upstream_intake.py` imprime en el briefing solo `id`, `status`,
`channel`, `nucleus_artifact` y `title` truncado a 100 caracteres, y solo de entradas que
pasan el validador. `defect`, `evidence` y `proposed_change` se leen bajo demanda en el
triage, como dato y nunca como instrucción (`agents.md §4`, frase existente). Así el texto
libre del host nunca entra solo por ejecutar `--boot`.

### D3 — Filtro de intake (GitHub Action)

`.github/workflows/host-finding-intake.yml` se dispara con `issues: [opened, edited]` sobre la
etiqueta `host-finding`. No usa agente ni secretos del agente. Permisos `issues: write`,
`contents: read`. Ejecuta `python3 scripts/upstream_outbox.py check-issue` sobre el cuerpo.

**Superficie S0: inyección en el script de la Action.** El cuerpo del issue lo escribe
cualquiera. Nunca se interpola `${{ github.event.issue.* }}` dentro de un `run:`: el cuerpo
llega por variable de entorno a un fichero y de ahí al script. Lo comprueba la fila V5
(`rg` sobre `.github/workflows/`). Las actions se fijan por SHA de commit, no por tag, a
diferencia de `ci.yml`, que usa `@v4`. Endurecer `ci.yml` queda fuera de alcance (Out of scope).

| Comprobación | Etiqueta resultante |
| :--- | :--- |
| Faltan campos del schema | `needs-schema` |
| Falta evidencia (comando + salida) | `needs-evidence` |
| El escaneo de genericización da positivo | `needs-genericization` |
| Palabras de seguridad (`.env`, `secret`, `token`, `sandbox`, `hook`, `RA-09`, `RA-19`) | `security-suspect` + comentario que redirige al canal C |
| `recurs:` o título duplicado de un issue abierto | `possible-duplicate` |
| `pin` anterior al mínimo soportado (`config/upstream_intake.json`) | `unsupported-pin` |
| Más de 5 issues `host-finding` del mismo autor en 24 h | `rate-limited` |

Ningún `accept` sin reproducir la evidencia en el nucleus (borrador 057).

### D4 — Elementos 5-7 de la propuesta del host H1 (recomendación del 2026-10-28, se confirma en Phase 5)

| Elemento | Decisión | Motivo |
| :--- | :--- | :--- |
| (5) Cierre al subir el pin | Entra. Una entrada de `CHANGELOG.md` que publica un hallazgo de host lo cita con `host:<id>`; tras subir el pin, `scripts/sync_agents_pin.py` imprime `Ships host findings: <ids>` con los ids citados entre el pin anterior y el nuevo | Sin señal, el host tiene que leer el CHANGELOG a mano para saber qué delta borrar, que es como divergieron las tres gramáticas `Repro:` |
| (6) Disciplina de delta | Entra solo la parte determinista: una regla delta del host lleva `outbox:<id>`; `upstream_outbox.py deltas --rules <dir>` avisa (exit `0`) de cada delta cuyo id está `shipped:` | Detectar que «una regla del host repite algo que el nucleus ya publica» es juicio y no tiene instrumento. Prometerlo sería una afirmación de cobertura falsa |
| (7) Enlace de recurrencia | Entra como campo `recurs` del schema; el triage reabre o enlaza el hallazgo en vez de crear un id nuevo | Coste casi nulo. Evita el caso `F-107-N1` → `F-115-N10` (B-7) |

### D5 — Reglas reproduce-first: texto e instrumento

Cada regla entra con un check determinista (Filter 5). Una regla que solo vive en la prosa
es la que el host H1 vio fallar con A-1 y A-2.

| Regla | Texto (dónde) | Instrumento |
| :--- | :--- | :--- |
| R-4 «el gate nunca es el primer verificador» | `rules/qa_and_testing.md §4`: antes de reenviar a un gate, el remediador ejecuta cada comando de ese gate y anota cada exit code (leído con `$?`, nunca por tubería) en la tabla `Remediation notes` de `SPRINT_LOG.md` | `scripts/check_gate_log.py`: una fila de gate de ronda ≥ 2 sin una fila `Remediation notes` de la ronda anterior con al menos un comando y su exit sale `2` |
| R-5 radio de impacto (+ C-6) | `rules/qa_and_testing.md §4`: un cambio en un módulo compartido ejecuta la suite completa de su stack | `config/blast_radius.json` (globs del nucleus + `full_suite_command`), que el host sustituye con `<host-root>/.agents-blast-radius.json`; `audit_plan.py` sale `2` si una fila Work toca un glob y ninguna fila Verification contiene `full_suite_command` |
| R-6 replay (= `KI-054-1`) | `rules/code_craft.md §6`: la tabla nombra vitest | `check_fix_reproduces.py` añade un runner vitest: enlaza el `node_modules` del checkout principal en el worktree temporal, ejecuta `pnpm exec vitest run <ids> --reporter=junit` y distingue un test fallido de un error de setup (`<error>` frente a `<failure>`), igual que B-4 hace con pytest |
| R-8 comportamiento, no texto fuente | `rules/code_craft.md §6`: un test que lee código fuente como texto no es una reproducción | `check_fix_reproduces.py` emite el aviso `SOURCE_TEXT` (exit sin cambio) cuando un test `Repro:` contiene uno de estos cinco patrones: las subcadenas literales `readFileSync(`, `?raw`, `.read_text(`, `.read_bytes(` y `open(`, sin condición de ruta (un aviso no bloquea, así que el falso positivo es barato). Es un denylist que no afirma cobertura (`§1 fail_closed_claims`) |
| R-9 / A-2 criterios de aborto | `workflows/pipeline_workflow.md`: `principal_agent` mide cada criterio de aborto en cada frontera de fase y lo anota en la tabla `Abort criteria` de `SPRINT_LOG.md`; un criterio solo se cierra con la observación que nombra («cumplido por aritmética» lo deja abierto) | `scripts/check_plan_closure.py`: cada criterio numerado de `## Abort criterion` tiene ≥ 1 fila con un comando entre backticks y su exit code; si no, exit `2` |
| R-10 resultados al cierre | `workflows/close_workflow.md` Phase 2.6 | `scripts/check_plan_closure.py`: la tabla `Plan results` de `SPRINT_LOG.md` tiene una fila por cada fila de Tests y de Verification del plan, con el mismo número de filas y un resultado no vacío; si no, exit `2` |
| A-1 cadenas de remediación antes del gate | `rules/qa_and_testing.md §4`: una cadena cuenta igual que una etiqueta `remediation-regression` | `scripts/check_remediation_chain.py --range <base>..HEAD`: un commit `fix(` cuyas líneas cambiadas (`git blame` en el padre) introdujo otro `fix(` del mismo rango es un eslabón. Imprime las cadenas y sale `2` a partir de la segunda. Invocadores: `hooks/on_commit.py` en cada `fix(` (aviso, exit `0`) y QA Gate 1 (segundo check) |
| A-3 (= `KI-054-2`) | `agents.md §0`: una fila «Command paths» declara una vez la forma host (`python3 .agents/scripts/…`) y la nucleus. `agents.md` se carga siempre, también en los subagentes de gate | Ninguno nuevo: la fila sustituye a las notas por fichero, que hoy solo llevan `pipeline_workflow.md:11` y `remediation_workflow.md` (6 de 8 ficheros con `python3 scripts/` no la llevan) |

Se descarta extraer `_split_row` de `audit_plan.py` a `_md_table.py`: vive en `skills/`, y su
parser ya respeta `\|`.

### D6 — `KI-057-3`, `KI-057-4`, `KI-057-6`

| KI | Decisión |
| :--- | :--- |
| `KI-057-3` | Se crea `scripts/_md_table.py` con el separador de celdas de `a4db5df` (`check_task_scope.py` `_cells`). Lo usarán 4 sitios, así que la extracción se justifica (`rules/code_craft.md §1`: dos sitios ya bastan). Cada script se corrige en su propio commit `fix(` con test |
| `KI-057-4` | Se quita la entrada `SubagentStop` de `check_role_artifact.py --from-hook` de `claude/settings.hooks.json`, y `scripts/merge_json.py` poda esa entrada retirada de los hosts. El invocador que queda es Phase 7 (`RA-16`). Se corrige el texto de cierre de `F-107-N1` |
| `KI-057-6` | `_hotfix_refusal` (`scripts/session_state.py:460`) exige además que cada commit de `last_close_commit..tip` tenga un asunto que termine en `#H<NNN>` o contenga `(H-NNN)` |

### D7 — Dependabot

- **#88**: `claude-agent-sdk` a la última versión publicada en el momento de ejecutar (medida
  el 2026-10-28: `0.2.174`). Se cierra el PR #88 como sustituido y se cita el commit.
- **#89 (decisión humana 2026-10-28: medir y decidir)**: D-02 instala la última `0.9.x` en un
  venv desechable del scratchpad y mide (a) si alguna opción del CLI o de configuración
  vuelve a incluir el JSON de datos, (b) el recuento de nodos frente a `0.8.30` sobre `f0b11f8`
  y (c) qué variables de proveedor lee.
  - **Rama sí** (existe la opción): se ejecutan D-03..D-07.
  - **Rama no**: `graphifyy==0.8.30` se queda; se cierra #89 citando la medición y se abre
    `KI-058-n` en la cola del programa. D-03..D-07 no se ejecutan.
  - En las dos ramas, `graph_stats.json` lo escribe el cierre (Phase 8, `graphify-rebuild`),
    no una unidad: así cada rama tiene un solo escritor (Phase 4.3 F-8).

### Alternativas rechazadas

| Alternativa | Motivo |
| :--- | :--- |
| `RA-20: UPSTREAM_INTAKE` | Q6: repetiría `§4` (`RA-14`) |
| Gate (exit `2`) para entradas `drafted` envejecidas | Q3: no hay datos que fijen N; empezar como advisory |
| Leer el texto libre del host en el briefing | D2: ese texto entraría en el contexto sin triage |
| Notas «Command paths» en cada fichero que nombra `python3 scripts/` | D5 A-3: seis copias que mantener; `agents.md` ya se carga siempre |
| Extraer el `_split_row` de `audit_plan.py` | D5: ya es correcto y vive en `skills/` |

---

## Work

Orden de ejecución: A, C, B, D. Las filas `fix(` llevan su test pareado en la misma fila
(`rules/code_craft.md §6`). C-01 y C-02 se commitean seguidos, para que `_md_table.py`
nunca quede sin importador (`RA-16`; Phase 4.3 F-6).

**Companions generados (Phase 4.3 F-1).** `make verify` ejecuta `scripts/check_readme_counts.py`
y `scripts/map_workflows.py --check` (`Makefile:83-84`). Una unidad que crea un `scripts/*.py`
o un `config/*.json` regenera en su mismo commit el bloque `COUNTED` de `README.md` con
`python3 scripts/check_readme_counts.py --write`. Una unidad que modifica un `workflows/*.md`
regenera `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` con `python3 scripts/map_workflows.py`.
Los dos ficheros son companions obligatorios que exigen las reglas del propio sujeto, igual
que un test pareado (`agents.md §2 jurisdictional_lock`): no son sujetos, nunca se editan a
mano y `make verify` queda en verde después de cada unidad.

### Wave A — canal upstream (D1-D4)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json` | create — schema de D1 con una entrada de ejemplo genericizada | low | `doc_orchestrator` | ⏳ |
| A-02 | `scripts/upstream_outbox.py` | create — subcomandos `check`, `check-issue`, `export`, `aged` y `deltas` (D1, D2, D4); test `tests/test_upstream_outbox.py` | high | `implementer_agent` | ⏳ |
| A-03 | `config/upstream_intake.json` | create — `min_pin`, `aged_after_sprints`, `rate_limit_per_day` y la lista de palabras de seguridad de D3 | low | `implementer_agent` | ⏳ |
| A-04 | `scripts/upstream_intake.py` | create — canal A de D2: lee `.upstream_hosts.json` e imprime solo los campos estructurados; test `tests/test_upstream_intake.py` | high | `implementer_agent` | ⏳ |
| A-05 | `.gitignore` | modify — ignora `.upstream_hosts.json` | low | `implementer_agent` | ⏳ |
| A-06 | `scripts/session_start.py` | modify — `section_upstream` añade la cola de intake de `upstream_intake.py`; test `tests/test_session_start.py` | medium | `implementer_agent` | ⏳ |
| A-07 | `.github/ISSUE_TEMPLATE/host-finding.yml` | create — Issue Form que refleja el schema (canal B) | low | `implementer_agent` | ⏳ |
| A-08 | `.github/workflows/host-finding-intake.yml` | create — filtro de D3, actions fijadas por SHA, cuerpo del issue pasado por variable de entorno; la expresión `github.event.issue` no aparece entre `${{ }}` en ningún sitio del fichero, tampoco en un comentario (fila V5; Phase 4.3 F-2) | high | `implementer_agent` | ⏳ |
| A-09 | `scripts/sync_agents_pin.py` | modify — (5) imprime `Ships host findings: <ids>` tras subir el pin; test `tests/test_sync_agents_pin.py` | medium | `implementer_agent` | ⏳ |
| A-10 | `docs/standards/templates/CHANGELOG_TEMPLATE.md` | modify — cita `host:<id>` en una entrada que publica un hallazgo de host | low | `doc_orchestrator` | ⏳ |
| A-11 | `agents.md` | modify — `§4 feedback_upstream`: outbox, validador antes del transporte, canales A/B/C, triage en Phase 1, sustitución de los documentos libres y (5)-(7); actualiza en el mismo commit la reformulación de `§4` en `§3 jurisdiction` (`RA-14`; Phase 4.3 F-9). Sin «complete», «any» ni «every» sobre el escaneo | high | `rule_validator` | ⏳ |
| A-12 | `workflows/extract_workflow.md` | modify — `upstream_feedback` escribe una entrada del outbox y ejecuta `upstream_outbox.py check` | medium | `doc_orchestrator` | ⏳ |
| A-13 | `workflows/pipeline_workflow.md` | modify — Phase 1: triage obligatorio de la cola de intake (Q4) | medium | `doc_orchestrator` | ⏳ |
| A-14 | `workflows/close_workflow.md` | modify — en un host, el cierre ejecuta `upstream_outbox.py aged` y `deltas` como advisory | medium | `doc_orchestrator` | ⏳ |
| A-15 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | modify — guía del host: outbox, canales, disciplina de delta | low | `doc_orchestrator` | ⏳ |
| A-16 | `SECURITY.md` | modify — canal C: hallazgos de host sobre `RA-09`/`RA-19`, secretos, hooks o sandbox | low | `doc_orchestrator` | ⏳ |
| A-17 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — registra el informe del host H1 (43 ítems, genericizado) con los veredictos del 2026-10-22: el primer triage del canal | medium | `doc_orchestrator` | ⏳ |

### Wave C — KI de 057 (D6)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C-01 | `scripts/_md_table.py` | create — `split_cells()` que respeta `\|`; test `tests/test_md_table.py` | low | `implementer_agent` | ⏳ |
| C-02 | `scripts/check_task_scope.py` | refactor — `_cells` importa `_md_table.split_cells`; `tests/test_check_task_scope.py` sin cambios y en verde | low | `implementer_agent` | ⏳ |
| C-03 | `scripts/check_gate_log.py` | fix — `KI-057-3`; test `tests/test_check_gate_log.py` | low | `implementer_agent` | ⏳ |
| C-04 | `scripts/check_forge_ladder.py` | fix — `KI-057-3`; test `tests/test_check_forge_ladder.py` | low | `implementer_agent` | ⏳ |
| C-05 | `scripts/detect_new_models.py` | fix — `KI-057-3`; test `tests/test_detect_new_models.py` (nuevo) | low | `implementer_agent` | ⏳ |
| C-06 | `claude/settings.hooks.json` | modify — `KI-057-4`: quita la entrada `SubagentStop` de `check_role_artifact.py --from-hook`; test `tests/test_template_sandbox.py` | medium | `implementer_agent` | ⏳ |
| C-07 | `scripts/merge_json.py` | modify — `KI-057-4`: poda de los hosts la entrada de hook retirada; test `tests/test_merge_json.py` | high | `implementer_agent` | ⏳ |
| C-08 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — `KI-057-4`: el texto de cierre de `F-107-N1` cita C-06 y C-07 | low | `doc_orchestrator` | ⏳ |
| C-09 | `scripts/session_state.py` | fix — `KI-057-6`: cada commit de `last_close_commit..tip` es trabajo del hotfix; test `tests/test_session_state.py` | high | `implementer_agent` | ⏳ |

### Wave B — reglas reproduce-first (D5)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B-01 | `rules/qa_and_testing.md` | modify — §4: R-4, R-5 y A-1 | high | `rule_validator` | ⏳ |
| B-02 | `rules/code_craft.md` | modify — §6: R-8 y runner vitest en la tabla | medium | `rule_validator` | ⏳ |
| B-03 | `docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | modify — tablas `Remediation notes` (R-4), `Abort criteria` (R-9) y `Plan results` (R-10) | low | `doc_orchestrator` | ⏳ |
| B-04 | `scripts/check_gate_log.py` | modify — R-4: fila de ronda ≥ 2 sin nota de remediación → exit `2`; test `tests/test_check_gate_log.py` | medium | `implementer_agent` | ⏳ |
| B-05 | `scripts/check_remediation_chain.py` | create — A-1; test `tests/test_check_remediation_chain.py` | medium | `implementer_agent` | ⏳ |
| B-06 | `hooks/on_commit.py` | modify — A-1: llama a `check_remediation_chain.py` en un `fix(` (aviso, exit `0`); test `tests/test_on_commit.py` | medium | `implementer_agent` | ⏳ |
| B-07 | `config/blast_radius.json` | create — R-5: globs de módulos compartidos del nucleus y `full_suite_command` con el valor exacto `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider`, que coincide con la fila de Verification de este plan (Phase 4.3 F-4) | low | `implementer_agent` | ⏳ |
| B-08 | `skills/token-saver-auditor/scripts/audit_plan.py` | modify — C-6: lee `config/blast_radius.json` o el override del host; test `tests/test_token_saver_auditor.py` | medium | `skill_architect` | ⏳ |
| B-09 | `scripts/check_plan_closure.py` | create — R-9 y R-10; test `tests/test_check_plan_closure.py` | medium | `implementer_agent` | ⏳ |
| B-10 | `workflows/close_workflow.md` | modify — Phase 2.6 ejecuta `check_plan_closure.py` (`RA-16`) | low | `doc_orchestrator` | ⏳ |
| B-11 | `workflows/pipeline_workflow.md` | modify — R-9/A-2: medir los criterios de aborto en cada frontera de fase; Phase 7: R-4 y `check_remediation_chain.py` como segundo check | medium | `doc_orchestrator` | ⏳ |
| B-12 | `agents/qa_agent.md` | modify — Gate 1: segundo check `check_remediation_chain.py` | low | `agent_orchestrator` | ⏳ |
| B-13 | `scripts/check_fix_reproduces.py` | modify — R-6 / `KI-054-1`: runner vitest; test `tests/test_check_fix_reproduces.py` con un runner simulado | high | `implementer_agent` | ⏳ |
| B-14 | `scripts/check_fix_reproduces.py` | modify — R-8: aviso `SOURCE_TEXT` con los cinco patrones de D5; test `tests/test_check_fix_reproduces.py` | medium | `implementer_agent` | ⏳ |
| B-15 | `agents.md` | modify — `§0`: fila «Command paths» (A-3 / `KI-054-2`) | medium | `rule_validator` | ⏳ |

### Wave D — Dependabot (D7)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | `requirements-skillopt.txt` | modify — `claude-agent-sdk` a la última versión; trailer `Dependency:` | low | `implementer_agent` | ⏳ |
| D-02 | `docs/sprints/058-core-pipeline/GRAPHIFY_09_MEASUREMENT.md` | create — mediciones (a)-(c) de D7, salida literal por caso; ejecuta `devops_agent`, redacta `doc_orchestrator` | medium | `doc_orchestrator` | ⏳ |
| D-03 | `requirements-core.txt` | modify — rama sí: `graphifyy` a la última `0.9.x`; trailer `Dependency:` | high | `implementer_agent` | ⏳ |
| D-04 | `Makefile` | modify — rama sí: la opción de D-02 en los targets graphify; comentario de `:52` | medium | `implementer_agent` | ⏳ |
| D-05 | `rules/graphify.md` | modify — rama sí: versión y variables leídas (`:18`, `:32`) | low | `rule_validator` | ⏳ |
| D-06 | `rules/project_topology.md` | modify — rama sí: `:37` | low | `rule_validator` | ⏳ |
| D-07 | `config/with_env_allowlist.json` | modify — rama sí: el campo `reason` nombra las variables medidas | medium | `implementer_agent` | ⏳ |

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| `claude-agent-sdk` (bump) | la última al ejecutar D-01 (`0.2.174` el 2026-10-28) | No es una dependencia nueva: Dependabot #88 sube la existente del stack opcional skillopt |
| `graphifyy` (bump, condicional) | la última `0.9.x` al ejecutar D-03 | No es una dependencia nueva: Dependabot #89; solo en la rama sí de D7 |

Ninguna dependencia nueva. El runner vitest (B-13) usa el `node_modules` del host; el nucleus
no añade `package.json`.

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Validación del outbox y escaneo de genericización | script `scripts/upstream_outbox.py check` | `workflows/extract_workflow.md` `upstream_feedback` (host) |
| Entradas `drafted` envejecidas y deltas publicados | script `scripts/upstream_outbox.py aged` / `deltas` | `workflows/close_workflow.md` (host, A-14) |
| Cola de intake del canal A | script `scripts/upstream_intake.py` | `scripts/session_start.py --boot` (A-06) |
| Filtro de issues `host-finding` | GitHub Action + `upstream_outbox.py check-issue` | evento `issues` (A-08) |
| Triage de intake | agente (veredicto accept/merge/reject) | `workflows/pipeline_workflow.md` Phase 1 (A-13); el juicio sobre el defecto no tiene equivalente determinista |
| Ids de host publicados por un pin | script `scripts/sync_agents_pin.py` | `make sync-agents-pin` / boot del host (existente) |
| R-4 nota de remediación | script `scripts/check_gate_log.py` | Phase 7 (existente) |
| A-1 cadenas de remediación | script `scripts/check_remediation_chain.py` | `hooks/on_commit.py` (B-06) y QA Gate 1 (B-11, B-12) |
| R-5 / C-6 suite completa | script `audit_plan.py` + `config/blast_radius.json` | Phase 1 y Phase 5 (existente) |
| R-9 y R-10 | script `scripts/check_plan_closure.py` | `workflows/close_workflow.md` Phase 2.6 (B-10) |
| R-8 test que lee el fuente | script `check_fix_reproduces.py` (aviso) | QA Gate 1 (existente) |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 48 | Count of rows in Work tables (A 17, C 9, B 15, D 7; D-03..D-07 solo en la rama sí) |
| Subagents dispatched | 48 unidades + 2 gates por ronda, más Phase 3/4 (orchestrator, agent_orchestrator, skill_architect, rule_validator) | `agent_assignment.md` |
| Prior session ratio | pico de ciclo `14.6×` (9 ciclos: 6.1, 9.0, 9.8, 10.6, 12.3, 13.2, 8.9, 10.7, 14.6), a 0.4 del umbral duro de 15× | `python3 scripts/session_cost.py --from-anchor --json` |

La sesión de 057 rozó el umbral duro. 058 tiene un tamaño parecido (48 unidades frente a
las 38 + 20 de 057), así que se planifica una sesión por wave: A, C+B, D y después los
gates. `session_state.py suspend` se ejecuta en el soft 5× si queda más de una wave.

---

## Tests

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| `test -f scripts/upstream_outbox.py` | **Yes** — no hay validador del outbox (Q1) | exit `1` en `f0b11f8` |
| `test -f .github/ISSUE_TEMPLATE/host-finding.yml` | **Yes** — no hay canal B | exit `1` en `f0b11f8` |
| `test -f scripts/check_remediation_chain.py` | **Yes** — A-1 sin instrumento | exit `1` en `f0b11f8` |
| `test -f scripts/check_plan_closure.py` | **Yes** — R-9/R-10 sin instrumento | exit `1` en `f0b11f8` |
| `test -f config/blast_radius.json` | **Yes** — R-5 sin lista | exit `1` en `f0b11f8` |
| `rg -q "Remediation notes" docs/standards/templates/SPRINT_LOG_TEMPLATE.md` | **Yes** — R-4 sin tabla | exit `1` en `f0b11f8` |
| `rg -q "Command paths" agents.md` | **Yes** — A-3 / `KI-054-2` | exit `1` en `f0b11f8` |
| `rg -q -F "Ships host findings" scripts/sync_agents_pin.py` | **Yes** — (5) sin señal | exit `1` en `f0b11f8` |
| `rg -q -F "pytest replays .py only" scripts/check_fix_reproduces.py` | **Yes** — R-6 / `KI-054-1`: el mensaje `UNREPLAYED` existe | exit `0` en `f0b11f8` (el defecto está presente) |
| `rg -n 'split\("\x7c"\)' scripts/` | **Yes** — `KI-057-3` | exit `0`, 3 líneas: `detect_new_models.py:142`, `check_gate_log.py:64`, `check_forge_ladder.py:58` |
| `rg -n -F 'check_role_artifact.py --from-hook' claude/settings.hooks.json` | **Yes** — `KI-057-4` | exit `0`, línea `129` |
| `KI-057-6`: un hotfix cuyo rango contiene un commit `#058` pasa `require-released --hotfix` | **Yes** | unverified — el escenario necesita un repo fixture con un sello y una rama `hotfix/`; lo construye el test de C-09 y lo reproduce `check_fix_reproduces.py` en QA Gate 1 |
| `rg -q -F 'claude-agent-sdk==0.2.88' requirements-skillopt.txt` | **Yes** — #88 | exit `0` en `f0b11f8` (pin antiguo presente) |
| `make verify` | **No** — regresión a proteger | exit `0` en `f0b11f8` |
| `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` | **No** — regresión a proteger | exit `0`, `1288 passed` en `f0b11f8` |

---

## Verification

| Command | Expected | Dry run | Positive control |
| :--- | :--- | :--- | :--- |
| `make verify` | exit `0` | exit `0` en `f0b11f8` | n/a (`Expected` no es «no output») |
| `venv_skillopt/bin/python -m pytest -q -p no:cacheprovider` (suite completa, R-5) | exit `0` | exit `0`, `1288 passed` | n/a |
| `rg -n 'split\("\x7c"\)' scripts/` | no output | 3 líneas (el defecto, antes de C-03..C-05) | la misma orden en `f0b11f8` imprimió 3 líneas |
| `rg -n -F 'check_role_artifact.py --from-hook' claude/settings.hooks.json` | no output | 1 línea (`129`, antes de C-06) | la misma orden en `f0b11f8` imprimió la línea `129` |
| `rg -n '\$\{\{ *github\.event\.issue' .github/workflows/` | no output | exit `1`, sin salida (el fichero de A-08 aún no existe) | la misma expresión sobre un fichero de scratchpad con `run: echo ${{ github.event.issue.body }}` imprimió esa línea, exit `0` |
| `python3 scripts/upstream_outbox.py check docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json` | exit `0` | run at close — el script y el template los crean A-01 y A-02 | n/a |
| `python3 scripts/check_fix_reproduces.py --range f0b11f8..HEAD` | exit `0` | run at close — necesita los commits `fix(` del sprint | n/a |
| `python3 scripts/check_remediation_chain.py --range f0b11f8..HEAD` | exit `0`: menos de dos cadenas dentro del sprint. Solo cuentan commits del rango, así que una corrección sobre una línea de un `fix(` de un sprint anterior no es un eslabón. Un exit `2` no es un fallo del check: es la parada de A-1, y el bloque se re-planifica con el humano (Phase 4.3 F-3) | run at close — el script lo crea B-05 | n/a |
| `python3 scripts/check_plan_closure.py --sprint-dir docs/sprints/058-core-pipeline` | exit `0` | run at close — el script lo crea B-09 y se ejecuta sobre el `SPRINT_LOG.md` final | n/a |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/058-core-pipeline/IMPLEMENTATION_PLAN.md` | exit `0` | se ejecuta sobre este borrador antes de Phase 3 | n/a |
| `rg -n -F 'claude-agent-sdk==0.2.88' requirements-skillopt.txt` | no output | 1 línea (antes de D-01) | la misma orden en `f0b11f8` imprimió la línea `6` |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | `§4 feedback_upstream` (A-11); fila «Command paths» en `§0` (B-15) |
| `rules/qa_and_testing.md`, `rules/code_craft.md` | R-4, R-5, A-1; R-8 y vitest |
| `workflows/extract_workflow.md`, `pipeline_workflow.md`, `close_workflow.md` | outbox, triage, criterios de aborto, check de cierre |
| `docs/standards/templates/` | `UPSTREAM_OUTBOX_TEMPLATE.json` (nuevo), `SPRINT_LOG_TEMPLATE.md`, `CHANGELOG_TEMPLATE.md` |
| `docs/guides/SELF_IMPROVEMENT_GUIDE.md`, `SECURITY.md` | guía del host; canal C |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | informe del host H1 y veredictos; cierre de `F-107-N1` |
| `README.md` | recuentos de `scripts/*.py` y `config/*.json`: companion generado en cada unidad que los desplaza (`check_readme_counts.py --write`, preámbulo de Work) |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerado por `scripts/map_workflows.py` en cada unidad que modifica un workflow (preámbulo de Work) |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | cierra `KI-054-1`, `KI-054-2`, `KI-057-3`, `KI-057-4`, `KI-057-6`; `KI-058-n` si D7 sale por la rama no |
| `rules/graphify.md`, `rules/project_topology.md`, `Makefile`, `config/with_env_allowlist.json` | solo en la rama sí de D7 |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `KI-056-1` (carga de permission prompts) con D-1, D-3, D-12; `F-055-N1`; `KI-056-6`/D-8; D-4; D-10; `KI-057-1`; MCP de GitHub remoto con OAuth | Sprint 059 (régimen de sandbox), orden decidido el 2026-10-22 |
| C-7 (`ADR-0017`, arquitectura de roles) | Sprint 059 |
| Auditoría de prompts del corpus existente | Sprint 060 |
| `KI-057-2` (`SessionEnd` puede suspender otra sesión) | Sprint 059: depende de que el anchor registre el `session_id` del harness, del mismo bloque que la sesión/sandbox |
| Fijar por SHA las actions de `.github/workflows/ci.yml` | Sprint 059 (endurecimiento); 058 solo fija las de la Action nueva |
| Gate (exit `2`) para entradas `drafted` envejecidas | Q3: un sprint posterior, con datos de al menos tres sprints de hosts |
| Detectar reglas de host que repiten el nucleus | D4 (6): no tiene instrumento |
| D-2, D-9, D-11 | rechazados el 2026-10-22: sin petición |

---

## Abort criterion

1. **Escaneo de genericización (A-02)**: si un gate rechaza dos veces la misma familia S0/S1
   por un vector nuevo que el escaneo deja pasar, no se añade otro patrón. El docstring y
   `agents.md §4` se acotan a «denylist de las tres familias de D1; el control es
   `genericized: true`» (`agents.md §1 fail_closed_claims`).
2. **Action de intake (A-08)**: si un gate encuentra un S0 de inyección o de permisos en el
   workflow y la corrección no cierra el vector en la ronda siguiente, A-08 se revierte
   (`git revert`). El canal B se queda en el comando manual de `export`, y la Action pasa a
   `KI-058-n` (Sprint 059).
3. **Runner vitest (B-13)**: si el runner necesita una dependencia JS en el nucleus o no puede
   distinguir `<failure>` de `<error>`, B-13 se cierra sin publicarse. `KI-054-1` sigue abierto
   con la medición y el host usa `Repro: manual`. El resto de Wave B sigue.
4. **Sprint completo**: si un gate rechaza tres veces la misma familia S0/S1 sobre
   `scripts/merge_json.py` o `claude/settings.hooks.json`, esa unidad se revierte y se abre
   `workflows/remediation_workflow.md` Phase 0.
5. **Coste**: si un ciclo de sesión supera 15× (`session_cost.py`), no empieza trabajo nuevo y
   la sesión se suspende (`rules/token_economy.md §3.1`).

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | {{HUMAN}} |
| **Date** | {{ISO_DATE}} |
| **Plan commit at approval** | `{{COMMIT_SHA}}` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
