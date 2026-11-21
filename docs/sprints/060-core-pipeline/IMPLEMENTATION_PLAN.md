# Implementation Plan: Sprint 060 — github-broker-and-059-residue

**Canonical path**: `docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/060` · **Base**: `main` at `a6bddaa` (más `fb64486` y `0e08ee1` de `deploy-notes/059`)
**Status**: `DRAFT` (pending Phase 5)

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

Sprint 059 se desplegó como `v4.42.0` (PR #95 `1e90d6b`, sello PR #96 `a6bddaa`).
El sandbox obliga aún al humano a ejecutar `gh`, `git push` y la limpieza de
worktrees (`ADR-0019` D2). Decisión humana 2026-11-21: la primera unidad de 060 es
el broker de GitHub App (plan de 059, decisión 55). Decisión humana 2026-11-21 (esta sesión):
alcance = las 9 entradas que la roadmap asigna a 060, más el detector de modelos,
que va **después** del broker.

| Hecho | Medida | Reproducir |
| :--- | :--- | :--- |
| `gh` no corre bajo el sandbox | `failed to read configuration: open ~/.config/gh/config.yml: operation not permitted` | `gh issue list --label host-finding --state open` |
| El detector de modelos está ciego y falla abierto | `No bundled catalogue on this machine`, exit `0`; `/private/tmp/claude-501/bundled-skills` no existe con CLI 2.1.311 | `python3 scripts/detect_new_models.py --check; echo $?` |
| El snapshot de modelos está atrasado | 12 alias capturados con CLI 2.1.233 el 2026-08-17; faltan `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-fable-5-2` | `python3 -c "import json;print(json.load(open('config/model_tiers.json'))['catalog_snapshot']['cli_version'])"` |
| `agents.md` está en el tope | 20000 bytes | `wc -c < agents.md` |
| `unit_cost.py` falla sobre 059 | exit `2`, `unresolved SHA 27267601 of unit R-24` | `python3 scripts/unit_cost.py --sprint-dir docs/sprints/059-core-pipeline; echo $?` |
| `prompt_count.py` falla bajo el sandbox | exit `2`, `Operation not permitted` sobre `~/.claude/projects/…jsonl` | `python3 scripts/prompt_count.py --session <id> --json; echo $?` |
| CLI de medición distinta | sesión en 2.1.311; `rules/project_topology.md:26` nombra 2.1.119 | `claude --version`; `sed -n 26p rules/project_topology.md` |
| Base verde | `make verify` exit `0` (103 s) | `make verify; echo $?` |

**Intake triage.** Canal A: sin `.upstream_hosts.json` registrado (salida de `--boot`).
Canal B: vacío — `gh issue list --label host-finding --state open`, ejecutado por el
humano (`RA-09`) el 2026-11-21: `no issues match your search`. Hallazgo abierto
`F-055-N1` (puntos de entrada sin sandbox escribibles por el agente): este sprint no
lo cierra; D2 instala el broker fuera de todo árbol escribible para no añadir un
punto de entrada nuevo a ese hallazgo.

**Dependabot alert #28** (moderada, `main`), pegada por el humano el 2026-11-21:
`graphifyy` (`requirements-core.txt`), GHSA-pcc4-rvhr-2pr8, rango `>= 0.7.2, < 0.9.70`,
corregido en 0.9.70; el pin es 0.8.30 (`requirements-core.txt:11`). Unidad `K-01` (D12).

Hecho cuando: una sesión con sandbox empuja `ai-sprint/060`, abre y fusiona el PR,
empuja el tag firmado `v4.43.0` y publica la Release sin que el humano ejecute `gh`
ni `git push`; y las unidades B a J están cerradas con su comando de verificación.

---

## Design

| ID | Decision | Rejected alternative and why | Check |
| :--- | :--- | :--- | :--- |
| D1 | El broker es un servidor MCP stdio que **ejecuta** una lista cerrada de operaciones de GitHub; el token de instalación (1 h) nunca sale del proceso del broker. Claude Code lo lanza por stdio, así que no existe socket que autenticar (`ADR-0019` D6 criterio 2, F-17) | Daemon launchd con socket que entrega tokens: el token entraría al sandbox 1 h y la autenticación del socket habría que diseñarla y medirla (decisión humana 2026-11-21) | `BROKER_MEASUREMENT.md` M3: ningún proceso del sandbox obtiene un token (`env`, `ps`, archivos del broker) → 0 hallazgos |
| D2 | El broker se instala en `~/.config/agents-broker/` y se registra a nivel de usuario (`claude mcp add --scope user`), **nunca** en `.mcp.json` del proyecto ni en `claude/mcp.json`, que son escribibles por el agente (`F-055-N1`) | Registrarlo en `claude/mcp.json`: `install.py` lo inyectaría en cada host y su código quedaría bajo `./`, escribible | `grep -c agents-broker claude/mcp.json` → `0` |
| D3 | Claves (clave privada de la App, clave SSH de firma de tags) en `~/.config/agents-broker/keys/`, en `sandbox.filesystem.denyRead` y con `permissions.deny` `Read`/`Edit`/`Write` sobre `~/.config/agents-broker/**` y `~/.claude.json` (`ADR-0019` D6 criterio 1, F-05) | Llavero de macOS: el `python3` del sandbox es el mismo binario que el del broker, así que una ACL por binario no los separa, y `KI-059-21` midió el servicio del llavero alcanzable (decisión humana 2026-11-21) | `BROKER_MEASUREMENT.md` M1, M2: `cat`, `Read`, `Edit` desde el sandbox → denegados |
| D4 | Operaciones permitidas: `push_branch` (solo `ai-sprint/*`, `hotfix/*`, `deploy-notes/*`; nunca `main`, nunca `--force`), `open_pr`, `merge_pr` (head `ai-sprint/*` o `hotfix/*`, base `main`, los 3 checks requeridos en `success`), `push_tag` (`vX.Y.Z` sobre un commit de `main`, firmado SSH por el broker), `create_release`, `pr_status`. Cualquier otra operación → error. Permisos de la App: Contents RW, Pull requests RW, Metadata R; sin Administration | Merge con aprobación humana: contradice el criterio del 2026-11-21 (decisión humana 2026-11-21) | `pytest tests/test_github_broker.py` → exit `0` con un caso de rechazo por operación |
| D5 | El código del broker vive en el nucleus (`scripts/github_broker.py`, versionado y con tests) y lo instala **el humano** con `scripts/install_broker.py --tag vX.Y.Z`, que copia el archivo desde `git show <tag>:` (no desde el árbol de trabajo) tras verificar la firma del tag; el primer bootstrap (`v4.43.0` aún no existe) copia desde un commit de `main` que el humano nombra. Así la instalación no ejecuta contenido escribible por el agente (`RA-19` (3)) | Instalar desde el árbol de trabajo: el agente podría alterar el broker antes de que el humano lo instale | `pytest tests/test_install_broker.py` → exit `0`, incluido el caso «árbol de trabajo modificado no se instala» |
| D6 | Verificación de firma de tags con `git verify-tag` contra `config/allowed_signers` en `scripts/sync_agents_pin.py` y `scripts/install.py`; un tag sin firma válida → exit `2` (`KI-059-26`) | Confiar en el ruleset `version-tags`: protege la creación en GitHub pero no lo que el host hace checkout | `pytest tests/test_sync_agents_pin.py tests/test_install.py` → exit `0` con caso «tag sin firma» |
| D7 | `ledger_seal` sella `[Unreleased]` en `ai-sprint/[ID]` antes del PR del sprint, con `require-released` y `--owner-commit` re-ejecutados en esa punta (`KI-059-35`) | Un segundo PR para el sello: doble espera de CI, como #96 | `grep -n ledger_seal workflows/deployment_workflow.md` muestra la rama `ai-sprint/[ID]` |
| D8 | El detector de modelos falla cerrado (exit `2`) con `session_tool: claude-code` y sin catálogo; la fuente nueva del catálogo se busca en la CLI 2.1.311 en Phase 6; si no hay fuente en disco, el snapshot lo refresca un paso atendido y el resultado se escribe «not measurable» con su criterio | Mantener exit `0` sin catálogo: `make verify` pasa sin comparar nada | `python3 scripts/detect_new_models.py --check; echo $?` → `2` sin catálogo bajo `claude-code` |
| D9 | El escáner de nombres de host compara el SHA-256 de cada token normalizado contra `config/host_term_hashes.json`; el texto plano nunca entra al repositorio (`RA-15`). El humano genera los hashes con un comando local | Lista en texto plano: publicaría el nombre que el escáner protege | `python3 scripts/check_host_terms.py --history origin/main; echo $?` |
| D10 | Los 9 renombres `RA-06` (auditoría 059 A5, R1-R9) son una unidad cada uno; el humano aprobó los 9 con los nombres propuestos el 2026-11-21, R8 con el tipo `REGISTER` (`THIRD_PARTY_PROVENANCE_REGISTER.md`) | Un solo commit de renombres: impide aprobar uno y rechazar otro | `git log --oneline -- <ruta nueva>` por renombre |
| D12 | `graphifyy` sube a ≥ 0.9.70 por GHSA-pcc4-rvhr-2pr8 (Dependabot #28, moderada: lectura de archivos del host al indexar un repo no confiable, rango `>= 0.7.2, < 0.9.70`). Se mantiene `--require-hashes` y el método de la cabecera de `requirements-core.txt`; si 0.9.x vuelve innecesario o rompe el rodeo de `graph_update.py`, el mismo commit lo ajusta | Quedarse en 0.8.30: sigue en el rango vulnerable; desactivar el extractor de Fortran: no lo permite la API pública de `graphifyy` sin un rodeo nuevo | `grep -c '^graphifyy==0.8' requirements-core.txt` → `0`; `venv_skillopt/bin/python -m pip install --require-hashes -r requirements-core.txt; echo $?` → `0`; `venv_skillopt/bin/python -I scripts/graph_update.py; echo $?` → `0` |
| D11 | Las auditorías de prompts y de motivos en prosa miden primero (bytes y tokens por archivo cargado en cada sesión) y cada hallazgo S0-S2 se cierra en este sprint con código o borrado | Auditar sin medición previa (roadmap: «needs a prior measurement») | `PROMPT_AUDIT_REPORT-060.md` lista el comando de cada cifra |

---

## Work

Orden de ejecución: Wave A (broker) → Wave B (detector de modelos) → K (`graphifyy`) → C → D → E → F → G → H → I → J → Z.

| # | File | Operation | Risk | Assignee (proposed) |
| :--- | :--- | :--- | :--- | :--- |
| A-01 | `docs/decisions/ADR-0025-github-app-broker.md` | create — D1-D6; reemplaza `ADR-0019` D2 y D6 | medium | `doc_orchestrator` |
| A-02 | `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` | create — desde `BLUEPRINT_TEMPLATE.md` | low | `doc_orchestrator` |
| A-03 | `scripts/github_broker.py` | create — servidor MCP stdio con las operaciones de D4; test `tests/test_github_broker.py` en el mismo commit | high | `implementer_agent` |
| A-04 | `scripts/install_broker.py` | create — instalación desde tag firmado o commit de `main` (D5); test `tests/test_install_broker.py` | high | `implementer_agent` |
| A-05 | `claude/settings.hooks.json` | modify — `denyRead` y `permissions.deny` de D3 | medium | `implementer_agent` |
| A-06 | `config/allowed_signers` | create — clave pública de firma que entrega el humano | low | `implementer_agent` |
| A-07 | `scripts/sync_agents_pin.py` | modify — `verify-tag` (D6); test `tests/test_sync_agents_pin.py` | medium | `implementer_agent` |
| A-08 | `scripts/install.py` | modify — `verify-tag` (D6); test `tests/test_install.py` | medium | `implementer_agent` |
| A-09 | `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` | create — pasos humanos: crear la App, permisos de D4, instalarla solo en el nucleus, claves, `install_broker.py`, `claude mcp add --scope user` | low | `doc_orchestrator` |
| A-10 | `docs/sprints/060-core-pipeline/BROKER_MEASUREMENT.md` | create — M1 claves ilegibles, M2 broker instalado no editable, M3 ningún token en el sandbox, M4 rechazos de D4 en vivo, M5 extremo a extremo en el despliegue de 060 | high | `devops_agent` |
| A-11 | `workflows/deployment_workflow.md` | modify — push, PR, merge, tag y Release por el broker | medium | `doc_orchestrator` |
| A-12 | `agents/devops_agent.md` | modify — usa las herramientas del broker; ya no prepara `gh` para el humano | low | `agent_orchestrator` |
| A-13 | `rules/project_topology.md` | modify — fila `gh`/credencial: broker (`KI-059-21`, `-22`, `-24`) | medium | `doc_orchestrator` |
| A-14 | `workflows/repository_hardening_workflow.md` | modify — estado medido de `ADR-0019` D7 y la instalación de la App | low | `doc_orchestrator` |
| B-01 | `scripts/detect_new_models.py` | fix — fallo cerrado y fuente nueva (D8); test `tests/test_detect_new_models.py` | medium | `implementer_agent` |
| B-02 | `config/model_tiers.json` | modify — `catalog_snapshot`, `context_limits.haiku`, `excluded` (`claude-fable-5-2`), `verified_at` | low | `token_economy_agent` |
| K-01 | `requirements-core.txt` | modify — `graphifyy` 0.8.30 → la versión más nueva ≥ 0.9.70 publicada hace ≥ 24 h, closure transitivo y hashes regenerados por el método de la cabecera; revisión del rodeo de `scripts/graph_update.py` en el mismo commit (D12) | high | `implementer_agent` |
| C-01 | `workflows/deployment_workflow.md` | modify — `ledger_seal` en `ai-sprint/[ID]` (D7, `KI-059-35`) | medium | `doc_orchestrator` |
| D-01 | `scripts/check_host_terms.py` | create — escáner por hash (D9); test `tests/test_check_host_terms.py` | medium | `implementer_agent` |
| D-02 | `config/host_term_hashes.json` | create — hashes que genera el humano | low | `implementer_agent` |
| D-03 | `tests/test_profile_references.py` | modify — usa `check_host_terms.py` (`KI-059-14`) | low | `implementer_agent` |
| D-04 | `docs/sprints/060-core-pipeline/HISTORY_REVIEW_REPORT.md` | create — escaneo de `origin/main`; reescribir historia lo decide el humano (`KI-059-12`) | medium | `devops_agent` |
| E-01 | `scripts/check_gate_log.py` | modify — una fila de Gate findings por hallazgo S0-S2 (hallazgo 1 de la ronda 20 de QA de 059); test `tests/test_check_gate_log.py` | medium | `implementer_agent` |
| F-01 | `agents.md` | modify — recorte bajo 20000 bytes; redacción de `mass-standardizer` (`KI-059-32`); `RA-09`/`§6 devops_agent` con el broker | high | `rule_validator` |
| F-02 | `rules/skills_and_integrations.md` | modify — redacción de `mass-standardizer` (`KI-059-32`) | low | `rule_validator` |
| G-01 | `scripts/unit_cost.py` | fix — solo SHAs entre comillas invertidas que resuelven como commit (`KI-059-34`); test `tests/test_unit_cost.py` | low | `implementer_agent` |
| G-02 | `scripts/prompt_count.py` | fix — `EPERM` sobre la transcripción imprime el comando para el humano y exit `2` documentado (`KI-059-34`); test `tests/test_prompt_count.py` | low | `implementer_agent` |
| H-01 | `docs/sprints/060-core-pipeline/SANDBOX_REMEASUREMENT.md` | create — matrices de 055 y 056 en una CLI fija (`KI-059-31`) | high | `devops_agent` |
| H-02 | `rules/project_topology.md` | modify — fila `Measuring CLI` y filas afectadas por H-01 | medium | `doc_orchestrator` |
| I-01 | `docs/architecture/global_topology.md` | rename → `GLOBAL_TOPOLOGY_MAP.md` (R1); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| I-02 | `docs/architecture/topology_map.md` | rename → `TOPOLOGY_MAP.md` (R2); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| I-03 | `docs/contracts/core/doc_orchestrator_contract.md` | rename → `DOC_ORCHESTRATOR_CONTRACT.md` (R3); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| I-04 | `docs/contracts/core/topology_mapper_contract.md` | rename → `TOPOLOGY_MAPPER_CONTRACT.md` (R4); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| I-05 | `docs/contracts/core/topology_scaffolder_contract.md` | rename → `TOPOLOGY_SCAFFOLDER_CONTRACT.md` (R5); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| I-06 | `docs/audits/TOKEN_ECONOMY_AUDIT-documentation-standard.md` | rename → `TOKEN_ECONOMY_DOCUMENTATION_STANDARD_AUDIT.md` (R6); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| I-07 | `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md` | rename → `SKILLOPT_TRANSITIVE_CLOSURE_AUDIT.md` (R7); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| I-08 | `docs/audits/THIRD_PARTY_PROVENANCE_TODO.md` | rename → `THIRD_PARTY_PROVENANCE_REGISTER.md` (R8); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| I-09 | `docs/plans/027-autonomy-posture-DRAFT.md` | rename → `AUTONOMY_POSTURE_PLAN.md` (R9); `git mv` + grep `RA-14` de la ruta vieja → 0 aciertos fuera de registros sellados (D10) | low | `doc_orchestrator` |
| J-01 | `docs/audits/PROMPT_AUDIT_REPORT-060.md` | create — medición y hallazgos (D11) | medium | `token_economy_agent` |
| J-02 | `docs/audits/PROSE_MOTIVES_AUDIT_REPORT-060.md` | create — motivos en prosa en documentos normativos (D11) | medium | `rule_validator` |
| Z-01 | `docs/sprints/060-core-pipeline/SPRINT_LOG.md` | create — Phase 3 | low | `orchestrator` |
| Z-02 | `docs/sprints/060-core-pipeline/task_scope.md` | create — Phase 4.2 | low | `rule_validator` |
| Z-03 | `docs/sprints/060-core-pipeline/agent_assignment.md` | create — Phase 4.1 | low | `agent_orchestrator` |
| Z-04 | `docs/walkthroughs/core/pipeline/060_WALKTHROUGH.md` | create — closeout `RA-05` | low | `doc_orchestrator` |
| Z-05 | `CHANGELOG.md` | modify — `[Unreleased]` | low | `doc_orchestrator` |
| Z-06 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — KI routed → closed | low | `orchestrator` |

Los hallazgos de J-01 y J-02 entran como filas nuevas `J-NN` de una línea al cerrarse cada auditoría.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | El broker usa `urllib.request` y `json` de la stdlib para la API de GitHub, firma el JWT de la App con `openssl` (binario del sistema) y firma los tags con `git` + `ssh-keygen`; el protocolo MCP stdio es JSON-RPC por líneas, implementable con la stdlib. Si Phase 6 mide que no lo es, la dependencia entra por una fila de re-plan con su `Dependency:` trailer |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `scripts/github_broker.py` | script | `claude mcp add --scope user` (registro del humano, A-09); `workflows/deployment_workflow.md` |
| `scripts/install_broker.py` | script | `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` (humano) |
| `scripts/check_host_terms.py` | script | `Makefile#verify` |
| `verify-tag` en `sync_agents_pin.py` / `install.py` | script | `scripts/session_start.py`; `scripts/install.py` |
| `check_gate_log.py` fila por hallazgo | script | `Makefile#verify` (ya invocado) |
| `detect_new_models.py --check` fallo cerrado | script | `Makefile#verify` (ya invocado) |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 46 | Count of rows in Work tables |
| Subagents dispatched | 45 + gates | una dispatch por unidad; gates QA y Tester por ronda |
| Prior session ratio | n/a (no prior Claude transcript: `~/.claude/projects` en `denyRead`) | `python3 scripts/session_cost.py --from-anchor --json` |

---

## Tests

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| `python3 scripts/detect_new_models.py --check` sin catálogo bajo `claude-code` sale con `2` | **Yes** — this is the defect | exit `0` (`No bundled catalogue on this machine`), 2026-11-21 |
| `python3 scripts/unit_cost.py --sprint-dir docs/sprints/059-core-pipeline` sale con `0` | **Yes** — this is the defect | exit `2` (`unresolved SHA 27267601 of unit R-24`) |
| `python3 scripts/prompt_count.py --session <id> --json` bajo el sandbox imprime el comando para el humano | **Yes** — this is the defect | exit `2`, `Cannot read transcript: [Errno 1] Operation not permitted` sin comando |
| `grep -c '^graphifyy==0.8' requirements-core.txt` → `0` | **Yes** — this is the defect | `1` (`graphifyy==0.8.30`) |
| `wc -c < agents.md` < 20000 | **Yes** — this is the defect | `20000` |
| `make verify` | **No** — this is a regression to protect | exit `0`, 103 s |
| `tests/test_github_broker.py`, `tests/test_install_broker.py`, `tests/test_check_host_terms.py` | **Yes** — los archivos no existen | unverified: los tests se crean en A-03, A-04, D-01 |

---

## Verification

| Command | Expected | Dry run | Positive control |
| :--- | :--- | :--- | :--- |
| `make verify; echo $?` | `0` | exit `0` | n/a (expected is not "no output") |
| `python3 scripts/detect_new_models.py --check; echo $?` | `2` sin catálogo bajo `claude-code`; `0` con snapshot al día | exit `0` (defect) | n/a |
| `python3 scripts/unit_cost.py --sprint-dir docs/sprints/059-core-pipeline; echo $?` | `0` | exit `2` (defect) | n/a |
| `wc -c < agents.md` | < 20000 | `20000` | n/a |
| `grep -c agents-broker claude/mcp.json` | `0` | `0` | `grep -c mcpServers claude/mcp.json` → ≥ 1, prueba que el grep lee el archivo |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/060-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` | run at close of Phase 3: el archivo se extrae ahí | n/a |
| `python3 scripts/check_sprint_refs.py --current-sprint; echo $?` | `0` | run at close of Phase 3: el directorio del sprint no existe aún | n/a |
| `BROKER_MEASUREMENT.md` M5 (push, PR, merge, tag, Release por el agente) | 5 operaciones con el ID de GitHub de cada una | run at close: ocurre en el despliegue de 060 | M4: `push_branch main` rechazado |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `docs/decisions/ADR-0025-github-app-broker.md` | nuevo; reemplaza `ADR-0019` D2 y D6 |
| `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` | nuevo |
| `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` | nuevo |
| `workflows/deployment_workflow.md` | broker; `ledger_seal` en la rama del sprint |
| `workflows/repository_hardening_workflow.md` | estado medido y la App |
| `rules/project_topology.md` | credencial por broker; `Measuring CLI` |
| `agents.md`, `rules/skills_and_integrations.md` | recorte; `mass-standardizer`; `RA-09` |
| `agents/devops_agent.md` | herramientas del broker |
| `config/model_tiers.json` | snapshot y límites |
| `requirements-core.txt` | `graphifyy` ≥ 0.9.70, closure y hashes |
| Rutas R1-R9 | renombradas |
| `docs/audits/PROMPT_AUDIT_REPORT-060.md`, `PROSE_MOTIVES_AUDIT_REPORT-060.md` | nuevos |

**Measured figures.** Cada cifra de Context lleva su comando en la columna `Reproducir`.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `F-055-N1` (hooks y MCP del proyecto escribibles) | No lo cierra el broker; sigue abierto en `UPSTREAM_FINDINGS_FROM_HOSTS.md` |
| Reescritura del historial público | Destructiva; decisión humana con la evidencia de D-04 |
| Las 21 filas provisionales de `ADR-0023` y A1-d (`KI-059-28`) | Siguen abiertas; necesitan un archivo de settings de ámbito managed |
| Limpieza de worktrees por el agente | `.git/worktrees` es de solo lectura en el sandbox y el broker solo cubre GitHub; queda con el humano |

---

## Abort criterion

Decisión humana 2026-11-21: el criterio es la ejecución del broker al 100%.

1. Se cumple cuando `BROKER_MEASUREMENT.md` registra M1 a M5 en verde: M1 clave ilegible desde el
sandbox, M2 broker instalado no editable, M3 ningún token alcanzable, M4 cada rechazo
de D4 observado, M5 las cinco operaciones (push, PR, merge, tag firmado, Release)
ejecutadas por el agente con el ID de GitHub de cada una.

Si una de M1 a M5 falla, la ejecución se detiene y el sprint **vuelve a Phase 1**: el
plan se rehace con la medición que falló como entrada, y pasa otra vez por Phases 3 a
5 antes de continuar. No se revierte a `gh` con el humano ni se cierra el sprint con el
broker parcial.

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
