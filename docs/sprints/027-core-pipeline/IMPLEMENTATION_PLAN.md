# Implementation Plan: Sprint 027 — `autonomy-posture`

**Canonical path**: `docs/sprints/027-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/027` · **Base**: `main` at `980f149`
**Status**: `DRAFT` (Phase 3 extracted · awaiting Phase 5 Human OK)

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

**Objetivo (Apéndice Sprint 027 de `docs/roadmaps/core/pipeline/021-030-program-queue.md`, líneas 1122–1205):** sustituir el modo *bypass* por una postura de autonomía que gestione cuatro ejes — **efectividad, seguridad, memoria, drift** — sin colapsarlos en "todo permitido". Criterio de cierre del apéndice: *lo que debe valer bajo Claude Code y bajo Cursor vive en git hooks o en scripts que el protocolo invoca; lo que vive solo en `settings.json` es aceleración, nunca la única instancia de la garantía.*

**Por qué ahora.** `021`–`026` y hotfixes `H-002`/`H-003` cerraron la cola previa. El roadmap declara **Next: `027` (`autonomy-posture`)**. `F-023-S4` ya no bloquea (cerrado en `H-002`). Sprint `026` dejó el `pre-push` portable (`hooks/on_push.py`) y el bridge Cursor; este sprint construye encima, no lo reabre.

**Upstream leídos antes de planificar** (`agents.md §0 open_upstream_findings`):

| Ítem | Relación con 027 |
| :--- | :--- |
| `F-026-A1` | **Dentro.** Gates con grant read-only a los que se asignan writes / description que afirma write |
| `F-026-A3` | **Dentro.** `hooks/on_init.py` paths host-hardcoded; verificación en raíz núcleo dio falso verde |
| `F-026-A2` | **Fuera.** `tier_escalation` dormido → destino `028`/`030` (disciplina de `task_scope`, no postura de autonomía) |
| `F-021-A2` | **Fuera.** Rediseño de role-map (implementer) — declarado abierto a propósito desde `023` |

**Mediciones contra `980f149` (reproducidas en esta sesión):**

| Hecho | Comando / observación |
| :--- | :--- |
| `tester_agent` afirma write y no tiene `Write`/`Edit` | `tools: Read, Glob, Grep, Bash` + description *"to write and execute … tests"* |
| `qa_agent` grant idéntico; description ya niega write funcional | Mismo `tools:`; *"Does not write functional logic or tests"* |
| `pipeline_workflow.md` Phase 7 ya nombra transcripción por Orchestrator | Gates emit; Orchestrator escribe `SPRINT_LOG.md` |
| `claude/settings.hooks.json` solo tiene `SessionStart`, `PreToolUse`, `Stop` | Ausentes: `PreCompact`, `PostCompact`, `SubagentStop`, `SessionEnd` |
| Sin `defaultMode` / `autoMode` / `sandbox` / `disableBypassPermissionsMode` | Solo `permissions.deny` (4 reglas) + `plansDirectory` |
| `on_init.py` no importa `_root`/`_mode`; 5 constantes `Path("…")` host-relativas | Reproduce el bloque *How to reproduce* de `F-026-A3` |
| `hooks/on_push.py` ya existe (026) | Portable security parcial ya entregada |

**Qué es cierto cuando el sprint termina.**

1. Bajo Claude Code: `defaultMode: auto`, `hard_deny`/`soft_deny` enumerados, `disableBypassPermissionsMode` cerrado, sandbox+credentials, hooks de compact/session/subagent cableados al template.
2. Bajo Cursor (y en general): cada riesgo de la columna Claude tiene **contraparte portable** (script o git hook) nombrada y con `invoked_by:` (`RA-16`), o queda **declarada** como no portable (eje Effectiveness).
3. `F-026-A1` y `F-026-A3` ticked en `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` con commit y prueba de re-medición.
4. `make verify` sale `0` en la rama.

---

## Design

### D1 — Regla vinculante (del apéndice, no negociable aquí)

| Eje | Capa portable (obligatoria) | Aceleración Claude Code |
| :--- | :--- | :--- |
| Security | `pre-push` (ya 026), `pre-commit`, `commit-msg`, `submodule_purity` | `hard_deny`, sandbox, credentials |
| Memory | Plan canónico en sprint dir (`C0`); ancla; `session_state.py` | `PreCompact`/`PostCompact`, `plansDirectory`, checkpointing |
| Drift | `artifact_registry` + close Phase 2.6 + `make verify` | `SubagentStop` |
| Effectiveness | **Ninguna** (propiedad del harness) | `auto` + `autoAllowBashIfSandboxed` |

Una unidad que solo toque la columna derecha sin dejar contraparte izquierda (o declaración explícita de no-portabilidad) **se rechaza en Approval Gate**.

### D2 — `F-026-A1`: no otorgar `Write` a los gates

Resolución **#2** del finding (ya esbozada en `pipeline_workflow.md` Phase 7 y en el registry):

- Los gates **verifican y emiten veredicto**; no escriben artefactos de sprint ni ficheros de test en el árbol.
- Quien escribe tests en Phase 6 es el perfil con `Write` que el `task_scope` nombre (desviación documentada si el assignee ideal es `tester_agent`).
- Quien transcribe veredictos a `SPRINT_LOG.md` es **Orchestrator**.

**Prohibido** cerrar el finding añadiendo `Write, Edit` a `qa_agent` / `tester_agent`.

### D3 — `F-026-A3`: lectura elegida

Elegimos la **lectura 1 ampliada**, no la 2 completa:

1. El hook es **host-scoped** (cwd = proyecto anfitrión). El docstring lo declara como `scripts/_root.py` exige para scripts host-scoped.
2. Las rutas del *framework* (`INSTALL_SCRIPT`, lock del bridge) se resuelven con `agents_root()` para no mentir cuando alguien inspecciona desde el núcleo.
3. Las rutas del *host* (`.env`, anchors `.claude/…`) siguen siendo relativas al cwd — correcto en el único contexto donde `SessionStart` dispara.
4. **No** se registra `SessionStart` en el núcleo en este sprint (`nucleus_neutrality` + `install_nucleus_bridge` no instala hooks a propósito). La contraparte portable sigue siendo `start_workflow.md` Phase 1.5 `bridge_check`.

Lectura 2 completa (automatizar SessionStart en núcleo) → **fuera de alcance**, destino posible `028` si el puente núcleo vuelve a pudrirse.

### D4 — `SessionEnd` → `suspend`, nunca `release`

Wiring a `session_state.py suspend`. `release` sella el sprint y escribiría un `last_close_commit` falso (mismo razonamiento que el apéndice 027 y el plan 026).

### D5 — `SubagentStop` es aceleración; el script es la garantía

`scripts/check_role_artifact.py` (nombre provisional en Work) consulta `config/artifact_registry.json` y falla si el rol que termina no dejó el artefacto que el registry le asigna para la fase en curso. Invocado por:

- Claude: hook `SubagentStop` en el template
- Cursor / sequential: `pipeline_workflow` Phase 4.x / close 2.6 ya verifican artefactos; el script se añade como invoker explícito desde close o `make verify` (unidad P2 decide el cableado mínimo sin duplicar Phase 2.6)

### D6 — Orden de olas

| Ola | Nombre | Por qué este orden |
| :--- | :--- | :--- |
| **0** | Contradicciones heredadas (`F-026-A1`, `F-026-A3`) | No construir postura sobre perfiles/hooks que mienten |
| **1** | Capa portable (scripts + invokers) | La garantía debe existir antes de la aceleración |
| **2** | Template Claude Code (`settings.hooks.json`) | Aceleración cableada a scripts de la Ola 1 |
| **3** | Cierre documental (upstream ticks, roadmap, ledger) | Solo tras verde de verify |

---

## Work

Una fila = un commit atómico (`RA-08`) con **un fichero sujeto** (`jurisdictional_lock`). Assignees son rulesets bajo `delegation_mode: sequential` (Cursor): el mismo agente escribe, gobernado por el perfil nombrado.

### Ola 0 — Contradicciones

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `agents/tester_agent.md` | modify | medium | `agent_orchestrator` | ⏳ |
| A1.1 | `agents/qa_agent.md` | modify | low | `agent_orchestrator` | ⏳ |
| A1.2 | `agents/orchestrator.md` | modify | low | `agent_orchestrator` | ⏳ |
| A3 | `hooks/on_init.py` | modify | high | `devops_agent` | ⏳ |
| A3.1 | `tests/test_on_init.py` | create | medium | `devops_agent` (desviación: tests/; `tester_agent` sin Write — alineado con A1) | ⏳ |

**Operaciones:**

- **A1** — Reescribir `description` y fila `responsibility` para: verificar y ejecutar la suite existente / emitir veredicto; **prohibido** crear o editar ficheros de test. Done: `grep -i write agents/tester_agent.md` no afirma autoría de artefactos; `tools:` sigue sin `Write`/`Edit`.
- **A1.1** — Añadir en Profile Rules fila explícita `verdict_routing`: emite veredicto; Orchestrator transcribe a `SPRINT_LOG.md`. Done: no contradice `tools:`.
- **A1.2** — Fila Profile Rules: Phase 7 transcription ownership (registry + pipeline). Done: el perfil dueño del write queda nombrado en el perfil Orchestrator, no solo en el workflow.
- **A3** — Docstring host-scoped; `agents_root()` para `INSTALL_SCRIPT` y `BRIDGE_LOCK`; cwd-relative para `.env` y anchors; comentario obsoleto de `install.py` eliminado. Done: `grep _root hooks/on_init.py` no vacío; reproduce del finding deja de aplicar.
- **A3.1** — Tests que fallen en `980f149` y pasen tras A3: resolución de rutas framework; rechazo de falso verde si se simula inspección solo con `Path.exists()` desde un cwd incorrecto sin usar el resolver.

### Ola 1 — Portable

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/persist_session_context.py` | create | medium | `devops_agent` | ⏳ |
| P1.1 | `tests/test_persist_session_context.py` | create | medium | `devops_agent` (desviación tests/) | ⏳ |
| P2 | `scripts/check_role_artifact.py` | create | medium | `devops_agent` | ⏳ |
| P2.1 | `tests/test_check_role_artifact.py` | create | medium | `devops_agent` (desviación tests/) | ⏳ |
| P2.2 | `Makefile` o `scripts/verify_references.py` / target verify | modify | medium | `devops_agent` | ⏳ |
| P3 | `scripts/session_end_hook.py` | create | medium | `devops_agent` | ⏳ |
| P3.1 | `tests/test_session_end_hook.py` | create | low | `devops_agent` (desviación tests/) | ⏳ |

**Operaciones:**

- **P1** — Persiste ancla + punta a `task_scope.md` del sprint corriente (lectura de `active_state.json`); invocable sin Claude. `invoked_by:` en docstring → template PreCompact + (documentado) uso manual post-compact bajo Cursor. Done: dry-run escribe/actualiza mirror o log determinista sin sellar sprint.
- **P2** — Dado rol + sprint dir, consulta `config/artifact_registry.json`; exit `2` si falta el artefacto `required` de esa fase/rol. Done: contra fixture sin `task_scope.md` sale `2`; con él sale `0`.
- **P2.2** — Cablear P2 al menos a un invoker de cierre o `make verify` sin duplicar la semántica de close 2.6 (si ya cubre lo mismo, el invoker es el docstring del script + excepción tipada o mención en close Phase 2.6). Done: `RA-16` satisfecho.
- **P3** — Wrapper que llama `session_state.py suspend` (no `release`). Done: test de integración en tmp dir demuestra status `SUSPENDED` y `last_close_commit` intacto.

### Ola 2 — Template Claude Code

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `claude/settings.hooks.json` | modify | **high** | `devops_agent` | ⏳ |
| C2 | `docs/guides/AUTONOMY_POSTURE_GUIDE.md` | create | low | `doc_orchestrator` | ⏳ |
| C3 | `workflows/start_workflow.md` o `pipeline_workflow.md` | modify | medium | `doc_orchestrator` | ⏳ |

**Operaciones:**

- **C1** — En el template (host recibe merge no destructivo vía `install.py`):
  - `permissions.defaultMode: "auto"`
  - `autoMode.hard_deny` / `soft_deny` según apéndice (force-push, reset duro, exfiltración; soft: `git clean`, `docker compose down -v`, …)
  - `disableBypassPermissionsMode: "disable"`
  - `sandbox.enabled` + `autoAllowBashIfSandboxed` + `credentials.files` deny para `.env`
  - `fileCheckpointingEnabled: true`
  - Ampliar `allow` con `cd` y utilidades del apéndice (lista cerrada en el commit)
  - Hooks: `PreCompact`→P1, `PostCompact`→re-read ancla (comando mínimo), `SubagentStop`→P2, `SessionEnd`→P3
  - Conservar `plansDirectory`, `SessionStart`, `PreToolUse`, `Stop` existentes
  - Done: `python3 -c "json.load(...)"` ok; claves presentes; merge installer no pisa deny del host (probar o documentar semántica actual de merge)
- **C2** — How-to: qué es portable vs Claude-only; cómo un host aplica el template; qué hace Cursor en su lugar. Diátaxis how-to.
- **C3** — Una celda que apunte la contraparte Cursor (P1 manual / Phase 2.6 / bridge_check) para no dejar el eje Memory/Drift como si `settings.json` bastara.

### Ola 3 — Cierre

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | ⏳ |
| D2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | ⏳ |
| D3 | `CHANGELOG.md` | modify | low | `principal_agent` | ⏳ |

- **D1** — Tick `F-026-A1` y `F-026-A3` con commit + re-medida (regla del propio fichero).
- **D2** — Marcar 027 delivered / Next → 028 cuando el close lo selle (puede aplazarse a close_workflow).
- **D3** — Entrada `[Unreleased]` Keep a Changelog.

---

## Dependencies

None.

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Persist context on compact | script `persist_session_context.py` | `claude/settings.hooks.json` PreCompact; documented manual under Cursor |
| Role artifact check | script `check_role_artifact.py` | SubagentStop + close/verify wiring (P2.2) |
| Session end → suspend | script `session_end_hook.py` | `claude/settings.hooks.json` SessionEnd |
| Force-push block | already `hooks/on_push.py` | `.git/hooks/pre-push` (026) |
| Auto-mode classification | harness (Claude) | N/A — acceleration only |
| Bypass disabled | settings key | template C1; no Cursor equivalent — declared in C2 |

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `tester_agent` description no longer claims write of test files | **Yes** — current description claims write |
| `on_init` imports `agents_root` / resolves framework paths | **Yes** — no `_root` import |
| `persist_session_context.py` exists and runs | **Yes** — file absent |
| `check_role_artifact.py` exit 2 on missing required artifact | **Yes** — file absent |
| `session_end_hook` leaves `SUSPENDED` without touching `last_close_commit` | **Yes** — file absent |
| settings template contains `SubagentStop` and `disableBypassPermissionsMode` | **Yes** — keys absent |
| `make verify` | Baseline: rerun on Phase 2; sandbox `xargs` noise no cuenta como rojo del árbol |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 -m pytest tests/test_on_init.py tests/test_persist_session_context.py tests/test_check_role_artifact.py tests/test_session_end_hook.py -q` | exit `0` |
| `python3 -c "import json; json.load(open('claude/settings.hooks.json'))"` | exit `0` |
| `python3 -c "import json; h=json.load(open('claude/settings.hooks.json')); assert 'SubagentStop' in h['hooks'] and h.get('disableBypassPermissionsMode')=='disable'"` | exit `0` (ajustar si la clave anida bajo `permissions`) |
| `make verify` | exit `0` |
| Re-medida `F-026-A1` / `F-026-A3` según bloques *How to reproduce* del audit | ya no reproducen el defecto |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `F-021-A2` (implementer role) | Role-map redesign → sprint propio o `028` |
| `F-026-A2` (`tier_escalation` dormant) | Disciplina `task_scope` → `028`/`030` |
| Nucleus `SessionStart` automation | Lectura 2 completa → backlog si el bridge núcleo vuelve a pudrirse |
| Effectiveness under Cursor | Declarado imposible en apéndice; solo documentar en C2 |
| Host real `allowedDomains` / sandbox paths | `RA-15` — plantilla genérica; el host mide los suyos |
| Reabrir `026` / `on_push` | Ya entregado |

---

## Abort criterion

Parar y revertir la Ola 2 (C1) si el merge no destructivo de `install.py` **borra o debilita** `permissions.deny` / `hard_deny` de un host al reinstalar el bridge — medido con un fixture de merge antes de declarar C1 done. Si no hay forma de probar el merge sin host real, C1 se limita a template + test unitario del merger y el abort se dispara si el test de merge muestra pérdida de reglas.

Parar el sprint entero si A1 se "resuelve" otorgando `Write` a un gate (viola D2).

---

## Approval

**Phase 5** pide OK humano explícito sobre este documento **después** de Phase 3 (directorio + branch `ai-sprint/027` + plan committed).

Decisiones que este DRAFT ya fija y que el humano confirma al aprobar:

1. Alcance = `autonomy-posture` + `F-026-A1` + `F-026-A3` (no `F-021-A2`, no `F-026-A2`).
2. Gates sin `Write` (D2).
3. `on_init` host-scoped con `agents_root` para rutas framework (D3).
4. `SessionEnd` → `suspend` (D4).

---
*Sprint 027 Phase 1 draft — Principal Agent — session `20260825T062801Z-24754`*
