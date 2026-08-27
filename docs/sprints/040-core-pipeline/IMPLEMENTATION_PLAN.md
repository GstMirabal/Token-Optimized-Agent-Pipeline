# Implementation Plan: Sprint 040 — cursor-bridge-incremental

**Canonical path**: `docs/sprints/040-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/040` · **Base**: `main` at `8268fc1` (`v4.22.0`)
**Status**: `APPROVED` (Phase 1 Human OK 2026-08-27 — «ok»; Q1–Q4 defaults)

> Authored at Phase 1 (Planning) by `principal_agent`. Under `session_tool: cursor`,
> `SwitchMode` to plan is PROHIBITED (`RA-18`). Committed before Phase 5
> (`agents.md §2 triple_lock`). Spanish permitted in this document (`agents.md §1 user_chat`).

---

## Context

Sprint **039** (`v4.22.0`) hizo que `/start --boot` reinstale el bridge Cursor
cuando el lock ≠ HEAD **o** los digests de `commands/` divergen (`commands_stale`).
La reparación sigue siendo **wipe-and-rebuild**: `shutil.rmtree(.cursor)` antes
de reescribir. Bajo el **agent sandbox de Cursor** ese `rmtree` falla; el boot
ya reclamó la sesión y aun así sale exit `2`.

Medido 2026-08-27, sesión Cursor `20260827T140724Z-10725`, `HEAD` `8268fc1`
(`v4.22.0`), agent sandbox activo:

| Fact | Measurement | Reproduce |
| :--- | :--- | :--- |
| `.bridge_cursor.lock` | `147868f…` | `cat .bridge_cursor.lock` |
| `HEAD` | `8268fc1…` | `git rev-parse HEAD` |
| Lock stale | **True** | compare lock text ≠ `git rev-parse HEAD` |
| `commands_stale` | **True** | `python3 -c "from pathlib import Path; import sys; sys.path.insert(0,'scripts'); from cursor_adapter import commands_stale; print(commands_stale(Path('.'), nucleus=True))"` |
| `os.access('.cursor', W_OK)` | **False** | `python3 -c "import os; print(os.access('.cursor', os.W_OK))"` |
| Write+unlink file under `.cursor/commands/` | **OK** | create/unlink probe file in that dir (sandbox) |
| `install_cursor_bridge` path | `rmtree` then rewrite | `rg -n 'rmtree' scripts/cursor_adapter.py` |
| Boot on bridge fail | exit `2` after claim | `rg -n 'bridge install' scripts/session_start.py` |
| Upstream Still-open | **0** | briefing `/start` o tabla Status en `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` |
| Coste sesión | n/a (Cursor / sin transcript Claude) | `python3 scripts/session_cost.py --from-anchor --json` |

**Hecho cuando 040 cierre:** el camino feliz de bridge **no** llama `rmtree` del
directorio `.cursor/`; tip nuevo con contenido fresco solo refresca el lock;
contenido stale se reescribe archivo-a-archivo (y poda huérfanos); `PermissionError`
en install no tumba un boot cuyo claim ya pasó (advisory en briefing);
post-deploy el lock puede alinearse al tip sin forzar wipe; rider **R** limpia
`resume_pointer` al sellar close para no dejar advisory falso en el siguiente
`/start` en `main`.

**Hereda (no reabrir):** `--boot` / drift→claim→probe→sync→bridge (039);
`commands_stale` (039 C1/C2); nucleus `write_bridge_locks` (037 S3); py_compile
sandbox-safe (037 S1); ADR-0002 baseline refresh (039).

### Phase 1 — defaults (Human OK 2026-08-27 — «ok»)

| # | Pregunta | Decisión | Por qué |
| :--- | :--- | :--- | :--- |
| **Q1** | ¿Rider **R** (`resume_pointer` clear en `release`)? | **Sí** — una unidad en `session_state.py` | 039 OoS rechazó auto-clear en *claim*; clear en *close/release* no destruye resume mid-sprint y elimina el advisory post-deploy en `main` |
| **Q2** | Fallo bridge en sandbox | **Advisory** (boot exit `0` + línea en briefing) si el error es `PermissionError` / errno 1 sobre `.cursor`; otros fallos de install siguen exit `2` | Drift/claim siguen hard; espejo IDE no debe invalidar sesión ya reclamada |
| **Q3** | ¿ADR nuevo? | **No** | Cambio de estrategia de install + severidad de boot; documentar en workflow + docstring; no cambia contrato de veredictos drift |
| **Q4** | Freshness más allá de `commands/` | **No en 040** — lock-only usa `commands_stale` existente; install incremental reescribe commands/rules/agents/mcp como hoy | Ampliar digests a rules/agents es otro sprint; no bloquea el fallo medido |

---

## Design

| ID | Decision | Why (rejected alternative) |
| :--- | :--- | :--- |
| **D-I1** | `install_cursor_bridge`: **upsert** (mkdir + overwrite files) + **prune orphans** under known subtrees (`commands/`, `rules/`, `agents/`). **No** `rmtree` del directorio `.cursor/` en el camino feliz. Fallback documentado: solo si un flag explícito / recovery path lo pide (default off) | Rechazado: seguir wipe total; pedir `required_permissions: ["all"]` en cada start |
| **D-S1** | Boot bridge triage: (a) lock fresca y `not commands_stale` → noop; (b) lock stale y `not commands_stale` → **solo** `write_bridge_locks` (sin install); (c) `commands_stale` o lock ausente / artifacts missing → install incremental; (d) install lanza `PermissionError` (o exit del installer que lo señalice) → briefing advisory, boot **exit 0** | Rechazado: cualquier fallo de install = exit 2 (039 D-C1, demasiado ancho bajo sandbox) |
| **D-S2** | Installer / adapter: si un write falla por permiso, propagar código distinto de 0 **y** mensaje estable `bridge: permission denied on .cursor` para que boot clasifique (d) | Rechazado: tragar el error en silencio |
| **D-D1** | `deployment_workflow` tras `baseline_refresh`: celda `bridge_lock_refresh` — si Cursor target aplica y `not commands_stale`, escribir lock al HEAD; si stale, invocar `install.sh --target cursor` (incremental). Invocación **separada** de baseline (`RA-13`) | Rechazado: esperar al próximo `/start` para descubrir tip nuevo |
| **D-R1** | En `session_state.py` path de `release` (sello CLOSED): limpiar `resume_pointer` (objeto vacío o ausencia documentada). Claim **no** auto-clear (039 D-P1 intacto) | Rechazado: auto-clear en claim; dejar advisory eterno post-close |

---

## Work

Una unidad = un fichero = un commit (`RA-08`, `jurisdictional_lock`). **Orden:**
I1 antes de I2/S1; S1 después de I1 (triage asume install incremental); D1 y W1
después de S1 (prosa = comportamiento real); R1 independiente tras I1 o en
paralelo lógico (otro fichero). Assignee propuesto — Phase 4.1 puede sobrescribir.
Cursor `sequential`: la sesión padre ejecuta.

### Track I — install incremental

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| I1 | `scripts/cursor_adapter.py` | modify | high | `implementer_agent` | ⏳ |
| I2 | `tests/test_cursor_adapter.py` | modify | medium | `implementer_agent` | ⏳ |

I1: eliminar `shutil.rmtree(cursor_dir)` del camino feliz; `_write_*` upsert;
función de prune de nombres no esperados en `commands/` / `rules/` / `agents/`;
docstring: measured sandbox — file write OK, directory `rmtree` denied.
Opcional interno: helper `content_fresh` reutilizando `commands_stale` (no
duplicar lógica de digest).

I2: test que tras primer install, segundo install **no** requiere borrar el
directorio raíz `.cursor` (spy/mock de `rmtree` no llamado, o assert dir inode /
existencia continua); test prune de command huérfano; tests 039 `commands_stale`
siguen verdes.

### Track S — boot triage + soft-fail

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| S1 | `scripts/session_start.py` | modify | high | `implementer_agent` | ⏳ |
| S2 | `tests/test_session_start.py` | modify | medium | `implementer_agent` | ⏳ |

S1: implementar D-S1 (a–d); path lock-only llama `write_bridge_locks` vía
`install.py` (subprocess o import estable) **sin** `install_cursor_bridge`;
briefing imprime una línea si (d).

S2: (b) lock stale + `commands_stale` False → no llama install, lock actualizado;
(d) install que simula PermissionError → `run_boot` exit `0` y briefing contiene
aviso; drift 2 / claim 2 siguen exit `2`.

### Track W / D — protocolos

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| W1 | `workflows/start_workflow.md` | modify | medium | `implementer_agent` | ⏳ |
| D1 | `workflows/deployment_workflow.md` | modify | medium | `implementer_agent` | ⏳ |

W1: celda `bridge_check` — lock-only vs install incremental; PermissionError =
advisory en boot (no hard stop). Bump versión workflow acorde.

D1: celda `bridge_lock_refresh` tras `baseline_refresh` (D-D1). Bump versión.

### Track R — rider resume_pointer (Q1)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `scripts/session_state.py` | modify | medium | `implementer_agent` | ⏳ |
| R2 | `tests/test_session_protocol.py` | modify | low | `implementer_agent` | ⏳ |

R1: en `release`, clear `resume_pointer`; docstring cita 039 D-P1 (claim no clear).

R2: release deja `resume_pointer` vacío / ausente; claim mid-sprint con resume
sigue intacto.

### Track P — programa / cierre documental (Phase 8 escribe; Phase 1 nombra)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | ⏳ |

P1: Next / in flight = **040** (`cursor-bridge-incremental`); 039 marcado
entregado/desplegado `v4.22.0` si aún falta fila de estado (RA-14 en ese doc).

---

## Dependencies

None

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Bridge freshness + install / lock-only | script | `scripts/session_start.py --boot` ← `commands/start.md` / `start_workflow.md` |
| Incremental Cursor mirror | script | `scripts/install.py --target cursor` ← `install.sh` ← boot / deploy |
| Bridge lock refresh post-deploy | workflow step + script | `deployment_workflow.md` `bridge_lock_refresh` |
| `resume_pointer` clear on release | script | `session_state.py release` ← `close_workflow.md` |

No new per-commit agent judgment. Filter 5: deterministic.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | **10** (I1–I2, S1–S2, W1, D1, R1–R2, P1) | Count of Work rows |
| Subagents dispatched | `0` under Cursor `sequential` | parent session executes |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` |

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `rg -n 'rmtree' scripts/cursor_adapter.py` matches happy-path install | **Yes** — defect I1 |
| Lock stale + file-writable `.cursor/commands` + `rmtree` denied → boot exit 2 | **Yes** — defect S1/I1 (repro: `--boot` tras tip nuevo en sandbox) |
| `resume_pointer` survives CLOSED + `/start` on `main` | **Yes** — defect R1 (probe advisory hoy) |
| `commands_stale` false after matching render | **No** — regression 039 (keep) |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `rg -n 'rmtree' scripts/cursor_adapter.py` | no happy-path `rmtree` of `.cursor` (o solo detrás de flag recovery documentado) |
| `python3 -c "from pathlib import Path; import sys; sys.path.insert(0,'scripts'); from cursor_adapter import install_cursor_bridge; install_cursor_bridge(Path('.'), nucleus=True)"` under agent sandbox | exit 0; `.cursor/commands` updated; no PermissionError |
| Lock stale, force `commands_stale` False in test | lock-only path; install not called |
| Simulated PermissionError on install in `run_boot` | exit `0`; briefing warns |
| `python3 -m pytest tests/test_cursor_adapter.py tests/test_session_start.py -q; echo $?` | `0` |
| `bash tests/test_installer.sh; echo $?` | `0` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/040-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `make verify; echo $?` | `0` outside sandbox (CI posture) |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `scripts/cursor_adapter.py` | install incremental; sin `rmtree` feliz |
| `scripts/session_start.py` | triage lock-only / soft-fail PermissionError |
| `scripts/session_state.py` | clear `resume_pointer` en `release` |
| `tests/test_cursor_adapter.py` | cobertura incremental + prune |
| `tests/test_session_start.py` | lock-only + soft-fail |
| `tests/test_session_protocol.py` | release limpia resume |
| `workflows/start_workflow.md` | semántica bridge_check 040 |
| `workflows/deployment_workflow.md` | `bridge_lock_refresh` |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Next = 040 |
| `docs/sprints/040-core-pipeline/IMPLEMENTATION_PLAN.md` | este plan |
| `CHANGELOG.md` | entrada `[Unreleased]` al close |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerado si W1/D1 cambian frontmatter/celdas mapeadas |

**Measured figures.** Toda cifra en Context/Verification lleva comando (tabla
Context).

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Symlink `.cursor/commands` → `commands/` | 039 OoS; rompe contrato del adapter |
| Digests de freshness para `rules/` / `agents/` / `mcp.json` | Q4 = no; sprint siguiente si hace falta |
| Cambiar política sandbox del producto Cursor | Fuera del framework |
| CE-5 pytest / `git init` sandbox | Candidato E; distinto de bridge |
| Medidor `cache_read` Cursor | Candidato D; ADR-0006 |
| Triaje CodeQL en `main` | Candidato A |
| Auto-clear `resume_pointer` en **claim** | 039 D-P1; R1 solo en release |
| Reescribir celdas históricas largas de close no tocadas | Ruido RA-14 |

---

## Abort criterion

Si el install incremental deja **huérfanos** que Cursor sigue cargando como
comandos/reglas activos (prune incompleto) **o** si el soft-fail (d) oculta un
fallo de install que no es de permisos (regresión: tip con commands rotos y boot
exit 0 sin aviso accionable): **revertir** I1/S1 y no promover. Criterio
observable: test de prune falla en rojo antes del fix y pasa después; test de
boot con error genérico de install (no PermissionError) sigue exit `2`.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | _(pending Human OK)_ |
| **Date** | _(pending)_ |
| **Plan commit at approval** | _(Phase 3 commit SHA)_ |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop`. Phases 6–8 only if the human arms `loop_guard.py start` first
(`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).*
