# Implementation Plan: Sprint 028 — `self-improvement-unblock`

**Canonical path**: `docs/sprints/028-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/028` · **Base**: `main` at `0a175a2`
**Status**: `APPROVED` (Phase 5 Human OK 2026-08-25 — *"si"*)

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

**Objetivo (Apéndice Sprint 028 de `docs/roadmaps/core/pipeline/021-030-program-queue.md`, líneas 1209–1257):** desbloquear la auto-mejora del framework desde un host. Hoy la creación está bloqueada y la promoción no está auditada — el aprendizaje muere en scratchpads porque **no existen destinos del lado del host** para agentes y perfiles familiares, mientras `strict_rule` prohíbe escribir en el submódulo.

**Estado deseado:** *creación local y libre, promoción con gate* — análogo a lo que `skill_forge_workflow.md` Phase 0 `forge_destination` ya resolvió para skills.

**Por qué ahora.** Sprint 027 (`autonomy-posture`) desplegado `v4.10.0` (2026-08-25). El roadmap declara **Next: `028` (`self-improvement-unblock`)**. Los findings `F-026-A1` y `F-026-A3` cerraron en 027; `F-021-A2` y `F-026-A2` siguen abiertos pero **no son el objeto de este sprint** (ver Out of scope).

**Upstream leídos antes de planificar** (`agents.md §0 open_upstream_findings`):

| Ítem | Relación con 028 |
| :--- | :--- |
| S1–S6 (apéndice 028) | **Dentro** — tabla de evidencias del apéndice; unidades U1–U5 |
| `F-021-A2` | **Fuera** — rediseño del role-map implementer; no se resuelve dando destino a agentes |
| `F-026-A2` | **Parcial / fuera** — dormancia de `tier_escalation`; el apéndice 028 recomienda **no** crear un agente selector de modelo; ampliar el charter de `token_economy_agent` ya ocurrió en 022/026. Un gate determinista de tier en Phase 4.3 es candidato para 030, no bloqueante aquí |

**Mediciones contra `0a175a2` (reproducidas en esta sesión):**

| Hecho | Comando / observación |
| :--- | :--- |
| Deadlock agent creation | `agents/agent_orchestrator.md:22` — *"MUST author a new `.md` profile physically in `agents/`"* vs `strict_rule` desde host |
| Skills tienen `forge_destination` | `workflows/skill_forge_workflow.md` Phase 0 — tres destinos; default host `.claude/skills/` |
| Agents no tienen equivalente | `grep -n forge_destination agents/agent_orchestrator.md` → vacío |
| Perfil solo resuelve dentro del submódulo | `scripts/install.py:408` — `AGENTS_DIR / "profiles" / profile`; falla si el perfil real vive fuera (`RA-15`) |
| `RA-16` no audita `agents/*.md` | `scripts/verify_references.py` check (d) — corpus de `agents/` para referencias, no `invoked_by` en perfiles |
| Purga sin contrapeso de routing | `close_workflow.md` Phase 3 `memory_wipe` + `extract_workflow.md` Phase 4 `redundant_ki_purge` vs una sola vía manual de preservación (`constitutional_escalation`) |

**Qué es cierto cuando el sprint termina.**

1. Un host puede crear un agente nuevo en `.claude/agents/` (default) sin tocar el submódulo; la doctrina lo nombra en `agent_orchestrator.md` y Phase 4.1 lo registra en `agent_assignment.md`.
2. `install.py` acepta `--profile <path>` apuntando **fuera** del submódulo; `RA-15` / `agents.md §3` nombran la convención (`~/.agents-profiles/<name>/` o ruta explícita del host) en lugar de *"a private location"*.
3. El cierre no borra un ítem de memoria sin que `extract_workflow` haya clasificado su destino (host / profile / nucleus).
4. La promoción al núcleo queda documentada como gate de PR (`RA-15` + `RA-16`), no como paso previo en el host.
5. `make verify` sale `0` en la rama.

---

## Design

### D1 — Regla vinculante (del apéndice)

| Artefacto | Destino host-side | Estado hoy |
| :--- | :--- | :--- |
| Skill nuevo | `.claude/skills/` | **Existe** (`forge_destination` a) |
| Agent nuevo | `.claude/agents/` | **Falta** — descubrimiento nativo disponible, doctrina ausente |
| Perfil familiar | Ruta nombrada del host + `install.py --profile <path>` | **Falta** — imposible hoy |
| Memoria | `memory_index.json` en host | Existe, pero se purga sin escalar |

**Principio:** *creación local y libre, promoción con gate.*

### D2 — `agent_forge_destination` (espejo de skills)

Tres destinos, **host-only por default** (opción a):

| Opción | Ruta | Cuándo |
| :--- | :--- | :--- |
| **(a) host-only** | `.claude/agents/<name>.md` | Default — herramienta específica del proyecto; sin cambio al submódulo |
| **(b) project-family** | `<profile>/agents/<name>.md` | Perfil familiar del host (ruta privada, no en el núcleo público) |
| **(c) framework-wide** | `.agents/agents/<name>.md` | Solo flujo núcleo branch→PR→tag; **PROHIBIDO** desde sesión host (`strict_rule`) |

Reescribir `agent_orchestrator.md` Phase 2 `agent_creation`: dejar de ordenar *"physically in `agents/`"* como única vía; exigir elección explícita antes de escribir.

### D3 — Perfil instalable por ruta (`U3`)

- `--profile <name>` sigue resolviendo `profiles/<name>` **dentro** del submódulo (compatibilidad con `example-project`).
- Nuevo: `--profile-path <absolute-or-relative-path>` (o `--profile @path` — decidir en U3.1) cuando el directorio no vive bajo `.agents/profiles/`.
- Convención documentada en `agents.md §3` / `RA-15`: perfiles de producción en `<host>/.agents-profile/` o `~/.agents-profiles/<name>/` — el host elige; el framework exige **ruta explícita en el install**, no un string mágico.
- `profiles/example-project/README.md` actualizado con el segundo modo de instalación.

### D4 — Contrapeso de preservación (`U4`)

Antes de `memory_wipe` (close Phase 3) y `redundant_ki_purge` (extract Phase 4):

- Cada KI candidato a supervivencia debe llevar `routing_class`: `host` | `profile` | `nucleus` | `discard`.
- `extract_workflow.md` Phase 2 `upstream_feedback` ya describe el flujo; este sprint lo hace **obligatorio y verificable** — un ítem sin clase no entra al índice y **no se purga** hasta clasificado (Heuristic Pulse Gate + regla escrita).
- Close Phase 2.5 ya presenta candidatos al humano; añadir columna/criterio de routing en la lista presentada.

### D5 — Gate de promoción (`U5`)

Promover agent/skill al núcleo **solo en el PR** al repositorio `.agents`:

- `RA-15`: genericizar strings identificadores del host.
- `RA-16`: `invoked_by:` en workflows/scripts tocados; excepciones tipadas en `config/invocation_exceptions.json` si aplica.
- Documentar en `docs/guides/` o en `extract_workflow.md` — no nuevo script salvo que `token_economy_agent` audite que hace falta.

### D6 — No crear agente selector de modelo

Recomendación explícita del apéndice 028: `token_economy_agent` ya posee `tier_escalation`; un subagente por tarea **gasta lo que intenta ahorrar**. Las excepciones siguen siendo **declaraciones en `task_scope.md`**.

### D7 — Orden de olas

| Ola | Nombre | Por qué este orden |
| :--- | :--- | :--- |
| **0** | Doctrina agente (`U1`, `U2`) | Desbloquear creación antes de tocar installer |
| **1** | Installer + convención perfil (`U3`) | Destino addressable para tier familiar |
| **2** | Memoria / extract / close (`U4`) | Contrapeso a la purga |
| **3** | Promoción + cierre documental (`U5`, roadmap, ledger) | Tras verify verde |

---

## Work

Una fila = un commit atómico (`RA-08`) con **un fichero sujeto** (`jurisdictional_lock`). Assignees son rulesets bajo `delegation_mode: sequential` (Cursor).

### Ola 0 — Doctrina agente

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/agent_orchestrator.md` | modify | medium | `agent_orchestrator` | ⏳ |
| A2 | `workflows/pipeline_workflow.md` | modify | medium | `doc_orchestrator` | ⏳ |

**Operaciones:**

- **A1** — Añadir fila `agent_forge_destination` (tres opciones a/b/c, default a); reescribir `agent_creation` para exigir destino elegido **antes** de escribir; prohibir opción c desde host. Done: `grep agent_forge_destination agents/agent_orchestrator.md` no vacío; línea 22 ya no ordena solo `agents/`.
- **A2** — Phase 4.1 done-criterion: `agent_assignment.md` incluye columna o fila `Destination` por unidad que cree agente (`host:.claude/agents/` | `profile:<path>` | `nucleus:PR`). Done: Phase 4.1 menciona el campo explícitamente.

### Ola 1 — Perfil instalable

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/install.py` | modify | high | `devops_agent` | ⏳ |
| P1.1 | `tests/test_installer.sh` o `tests/test_install_profile_path.py` | modify/create | medium | `devops_agent` (desviación tests/) | ⏳ |
| P2 | `agents.md` | modify | medium | `governance_learner` | ⏳ |
| P2.1 | `profiles/example-project/README.md` | modify | low | `doc_orchestrator` | ⏳ |

**Operaciones:**

- **P1** — Aceptar ruta de perfil externa; resolver `agents/`, `skills/`, `rules/` del perfil vía symlink al host `.claude/`; rechazar perfil externo en modo núcleo (igual que hoy). Done: `install.py --help` documenta el flag; install desde fixture tmp con perfil fuera del submódulo enlaza ≥1 agente.
- **P1.1** — Test que falle en `0a175a2` (solo `profiles/<name>` interno) y pase tras P1 con directorio temporal como perfil.
- **P2** — En `§3 topological_order` y `RA-15`: nombrar convención de ruta (`--profile-path`) en lugar de *"private location"* sin dirección. Done: un host puede seguir el doc sin inferir.
- **P2.1** — Segundo bloque Installation con `--profile-path` apuntando al ejemplo ilustrativo.

### Ola 2 — Memoria

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | `workflows/extract_workflow.md` | modify | medium | `governance_learner` | ⏳ |
| M2 | `workflows/close_workflow.md` | modify | medium | `governance_learner` | ⏳ |

**Operaciones:**

- **M1** — Phase 2/3: `routing_class` obligatorio en cada KI antes de `index_update`; ítem sin clase → no indexar, escalar en handoff. Done: tabla de fases menciona el campo.
- **M2** — Phase 2.5 Heuristic Pulse: la lista al humano incluye `routing_class`; Phase 3 `memory_wipe` prohíbe borrar entradas de `/memory/` cuyo KI correspondiente en el índice candidato carezca de clase. Done: texto explícito *"deletion with no destination is loss"*.

### Ola 3 — Promoción y cierre

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/guides/SELF_IMPROVEMENT_GUIDE.md` | create | low | `doc_orchestrator` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | ⏳ |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent` | ⏳ |

**Operaciones:**

- **D1** — Guía how-to: crear agente en host, perfil externo, promover al núcleo (checklist RA-15/RA-16). Done: archivo existe; enlazado desde `extract_workflow.md` Phase 2.
- **D2** — Marcar 028 en curso/cerrado; Next → 029 cuando aplique.
- **D3** — Entrada `[Unreleased]` bajo Keep a Changelog.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | — |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Profile install by external path | script | `scripts/install.py` (`invoked_by:` docstring + `install.sh`) |
| Memory routing class gate | agent judgment at extract + human at close 2.5 | `extract_workflow.md` Phase 2/3; `close_workflow.md` Phase 2.5 |
| Promotion checklist (RA-15/RA-16) | agent judgment | `docs/guides/SELF_IMPROVEMENT_GUIDE.md`; human at nucleus PR |

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| Install links agents from profile dir outside `.agents/profiles/` | **Yes** — P1.1 target |
| `agent_orchestrator` still mandates only `agents/` path | **Yes** — grep línea 22 today |
| Extract workflow requires routing_class | **Yes** — field absent today |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `venv_skillopt/bin/python -m pytest tests/ -q` | 0 failed |
| `make verify` | exit 0 |
| `grep -c 'agent_forge_destination' agents/agent_orchestrator.md` | ≥ 1 |
| `venv_skillopt/bin/python scripts/install.py --help` | mentions external profile path |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `F-021-A2` — implementer role | Rediseño del role-map; no se parchea con destinos de agente | Backlog / sprint dedicado |
| `F-026-A2` — tier gate determinista en Phase 4.3 | Apéndice 028 no lo incluye; 026 ya ejerció escalación manualmente | Sprint 030 (`token-economy-enforcement`) o extensión de `rule_validator` |
| Agente selector de modelo | Rechazo explícito del apéndice | `token_economy_agent` + `task_scope.md` |
| `SessionStart` automático en núcleo | `nucleus_neutrality`; bridge manual en `start_workflow` | Re-evaluar solo si el bridge vuelve a pudrirse |
| Sprint 029 (`documentation-truth`) | Cierra la cola documental; no mezclar | 029 |
| Editar vendored `-3rd` skills | `rules/skills_and_integrations.md §3` | N/A |

---

## Abort criterion

Detener y revertir la rama si:

1. **`strict_rule` se relaja** — cualquier unidad que permita escribir en `.agents/` desde sesión host sin flujo PR.
2. **`make verify` rojo irrecuperable** tras dos rondas de remediación en la misma unidad.
3. **El installer enlaza paths absolutos del host real** en artefactos trackeados del núcleo (`RA-15` violation).

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo |
| **Date** | 2026-08-25 |
| **Plan commit at approval** | `e52e2b6` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 es una autorización humana única y atendida. NO debe envolverse en `/loop` desatendido.*
