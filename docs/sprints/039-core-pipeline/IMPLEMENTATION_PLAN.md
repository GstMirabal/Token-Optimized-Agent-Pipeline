# Implementation Plan: Sprint 039 — start-close-lifecycle

**Canonical path**: `docs/sprints/039-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/039` · **Base**: `main` at `147868f` (`v4.21.0`)
**Status**: `DRAFT` (Phase 1 Human OK 2026-08-27 — pending Phase 5)

> Authored at Phase 1 (Planning) by `principal_agent`. Under `session_tool: cursor`,
> `SwitchMode` to plan is PROHIBITED (`RA-18`). Committed before Phase 5
> (`agents.md §2 triple_lock`). Spanish permitted in this document (`agents.md §1 user_chat`).

---

## Context

Program **034–038** is deployed (`v4.17.0`–`v4.21.0`). Cada sprint de protocolo
tocó una pieza de `/start` o `/close`, y al abrir la sesión siguiente **siempre**
queda algo desactualizado. La causa no es “olvidar un doc”: es **asimetría de
ciclo de vida** entre tres capas (comando fino → workflow → scripts) y un
baseline que el deploy squash **huérfana por construcción**.

Medido 2026-08-26, sesión Cursor `20260826T165545Z-2268`, `HEAD` `147868f`
(`v4.21.0`):

| Fact | Measurement | Reproduce |
| :--- | :--- | :--- |
| `last_close_commit` | `caf3cc4` | `python3 -c "import json; print(json.load(open('docs/active_state.json'))['last_close_commit'][:12])"` |
| Ancestro de `HEAD`? | **No** (exit 1) | `git merge-base --is-ancestor caf3cc4 HEAD; echo $?` |
| Drift | exit `0`, veredicto S, aviso de baseline huérfano + merge-base `d969fec` | `python3 scripts/detect_drift.py; echo $?` |
| Tags en mensaje S | lista empieza `v3.0.0, v3.1.0, v3.2.0` aunque el rango lo cubre `v4.21.0` | misma salida; `scripts/detect_drift.py` `report_sealed` usa `tags[:3]` |
| `commands/start.md` | 2 pasos: briefing + handoff; **sin** claim/probes/sync/bridge | `wc -c commands/start.md`; leer cuerpo |
| `session_start.py` | siempre `return 0` (no propaga drift 2) | `rg -n 'return 0' scripts/session_start.py` |
| Anchor tras claim | `IN_PROGRESS` + `current_sprint.status=CLOSED` + `resume_pointer.branch=ai-sprint/038` en checkout `main` | `docs/active_state.json`; `git branch --show-current` |
| Registry `graph.json` phase | `close_workflow.md Phase 1 (graph_rebuild)` | `rg -n 'graph_rebuild' config/artifact_registry.json` |
| Close workflow real | `graph_rebuild` **después** de `atomic_commit` (Phase 5) | `rg -n 'graph_rebuild' workflows/close_workflow.md` |
| ADR-0002 | S debe **proponer** refrescar baseline; deploy no escribe `last_close_commit` | `docs/decisions/ADR-0002-drift-verdict-exit-codes.md` §2–§3 |
| Coste sesión | n/a (Cursor / sin transcript Claude) | `python3 scripts/session_cost.py --from-anchor --json` |

**Hecho cuando 039 cierre:** un solo comando `/agents:start` ejecuta
drift→claim→probe→sync→bridge (y propaga exit `2`); tras squash+tag de deploy,
`last_close_commit` apunta al tip integrado en `main` (sin peaje huérfano en el
siguiente `/start`); el mapa/registry nombra la fase correcta de
`graph_rebuild`; el probe avisa higiene de anchor; el bridge no se declara
fresco solo por lock==HEAD si el body de comandos diverge.

**Hereda (no reabrir):** briefing ≤80 líneas / Still-open (035/038); pin sync
(034); model ledger (037); family-trial / gate-replay (038); ADR-0002 veredictos
S/M/U/A/R (solo cablear el refresh que el ADR ya nombra).

### Phase 1 — defaults (Human OK 2026-08-27 — «ok»)

| # | Pregunta | Decisión | Por qué |
| :--- | :--- | :--- | :--- |
| **Q1** | Forma del boot | Extender `session_start.py` con `--boot` (default desde `commands/start.md`); sin flag = solo briefing (compat `make session-start`) | Un script, dos superficies; evita `session_boot.py` paralelo |
| **Q2** | Cuándo refrescar baseline | Tras squash-merge + tag en `deployment_workflow` (`baseline_refresh`), **no** en `close` `release` | `require-released` sigue exigiendo tip del sprint == sello de close; el refresh es post-integración |
| **Q3** | Riders 3–5 | **Sí** en el mismo sprint: bridge freshness + registry phase + probe higiene + drift tag UX | Mismo tema lifecycle; tamaño comparable a un track 035 |
| **Q4** | ¿Nuevo ADR? | **No** — ADR-0002 ya exige el refresh; 039 lo mecaniza. Si la semántica de `last_close_commit` necesita dos roles (sprint tip vs integration tip), documentarlo en el workflow + comentario del script, no ADR nuevo salvo que Q2 cambie |

---

## Design

| ID | Decision | Why (rejected alternative) |
| :--- | :--- | :--- |
| **D-B1** | `python3 scripts/session_start.py --boot --tool cursor` ejecuta en orden: `detect_drift` (propaga exit `2`) → `session_state claim` → `session_probe` → `sync_agents_pin` → `bridge_check` (install si lock≠HEAD **o** body stale) → briefing. Sin `--boot`: solo briefing, exit 0 | Rechazado: dejar binding solo en prosa del workflow; segundo script `session_boot.py` |
| **D-B2** | `commands/start.md` invoca **solo** `--boot`; el workflow operator path = esa superficie (binding table sigue como especificación; el script es el invoker medible) | Rechazado: comando fino que “apunta” al workflow y espera memoria del agente |
| **D-L1** | Nuevo subcomando `session_state.py refresh-baseline [--sha HEX]` escribe `last_close_commit` (+ mirror). Invocado por `deployment_workflow` **después** de squash en `main` y tag `vX.Y.Z`, con SHA = `git rev-parse HEAD` del tip integrado | Rechazado: redefinir drift a “latest tag” sin tocar el anchor (silencia el síntoma); refrescar en `close` `release` (rompe `require-released` o vuelve a huérfano en squash) |
| **D-L2** | Tras refresh, `detect_drift` en `main` tip == baseline → `CLEAN` (no aviso huérfano). Mensaje S deja de decir “the next close refreshes it” | Ese texto es falso hoy: close vuelve a sellar un tip de rama |
| **D-L3** | `report_sealed`: listar tags de sellado que **contienen** commits del rango (o el tag más reciente que cubre), no `tags[:3]` del catálogo global | Rechazado: seguir mintiendo `v3.x` en un árbol `v4.21.0` |
| **D-C1** | Bridge freshness: comparar hash (o mtime+size) de `commands/*.md` vs `.cursor/commands/*.md` (y análogo Claude si lock existe). Stale → reinstall target; fallar `--boot` exit `2` si install falla | Rechazado: solo lock==HEAD (D6 post-038) |
| **D-R1** | `config/artifact_registry.json` phase de `graph.json` → `close_workflow.md Phase 5 (graph_rebuild)`; regenerar mapa (`make` / `map_workflows`) | Rechazado: editar a mano el guide generado |
| **D-P1** | `session_probe`: advisory si `status==IN_PROGRESS` y (`current_sprint.status==CLOSED` **o** `resume_pointer.branch` no es `HEAD`) | Rechazado: auto-clear del resume (destruye evidencia de resume real) |

---

## Work

Una unidad = un fichero = un commit (`RA-08`, `jurisdictional_lock`). **Orden:**
L1 antes de L2/L3 (API de refresh); B1 después de C1 si C1 añade helper importable
desde el mismo árbol — si no, B1 puede llamar install por subprocess. Assignee
propuesto — Phase 4.1 puede sobrescribir. Cursor `sequential`: la sesión padre
ejecuta.

### Track L — baseline post-deploy (núcleo)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| L1 | `scripts/session_state.py` | modify | high | `implementer_agent` | ⏳ |
| L2 | `workflows/deployment_workflow.md` | modify | medium | `implementer_agent` | ⏳ |
| L3 | `scripts/detect_drift.py` | modify | medium | `implementer_agent` | ⏳ |
| L4 | `tests/test_session_protocol.py` | modify | medium | `implementer_agent` | ⏳ |

L1: subcomando `refresh-baseline` (default SHA = `HEAD`); escribe
`last_close_commit`, `last_updated`, mirror. No cambia `status`. Docstring:
sprint tip lo escribe `release`; integration tip lo escribe deploy.

L2: celda `baseline_refresh` tras squash en `main` + tag; comando
`python3 scripts/session_state.py refresh-baseline` (núcleo) /
`.agents/scripts/…` (host). Done: exit 0; anchor tip == `git rev-parse HEAD`.

L3: `report_sealed` tags que cubren el rango; texto S → “refresh at deploy
(`refresh-baseline`), not at close”.

L4: test refresh escribe SHA; test orphan→refresh→CLEAN; test S lista tag
cubridor (no solo `tags[:3]` ciegos).

### Track B — boot path (núcleo)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | `scripts/session_start.py` | modify | high | `implementer_agent` | ⏳ |
| B2 | `tests/test_session_start.py` | modify | medium | `implementer_agent` | ⏳ |
| B3 | `commands/start.md` | modify | low | `implementer_agent` | ⏳ |
| B4 | `workflows/start_workflow.md` | modify | medium | `implementer_agent` | ⏳ |

B1: `--boot [--tool cursor|claude-code|terminal]`; orden D-B1; drift 2 → no
claim; bridge vía `install.sh --target …` cuando D-C1 lo exija. Cap ≤80 líneas
del briefing se mantiene.

B2: `--boot` con drift mock exit 2 → exit 2 y sin claim; drift 0 → claim
invocado (mock). Conservar tests Still-open 038.

B3: único paso operativo = `python3 scripts/session_start.py --boot --tool cursor`
(o tool del entorno); handoff Principal.

B4: Operator path = script `--boot`; binding table = spec; versión bump 6.5.0.
Prosa “claim → probes…” incluye drift **antes** de claim (corrige D14).

### Track C — bridge freshness

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `scripts/cursor_adapter.py` | modify | medium | `implementer_agent` | ⏳ |
| C2 | `tests/test_cursor_adapter.py` | modify | medium | `implementer_agent` | ⏳ |

C1: función `commands_stale(agents_dir) -> bool` (hash de `commands/` vs
`.cursor/commands/`); `install_cursor_bridge` ya reescribe; B1 la consulta.
Si no existe test file, crear `tests/test_cursor_adapter.py` (entonces C2 =
create).

C2: fixture con copy desfasada → stale True; tras write → False.

### Track R — registry / mapa

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R1 | `config/artifact_registry.json` | modify | low | `implementer_agent` | ⏳ |

R1: phase `graph.json` → Phase 5. Regenerar guide en el mismo commit solo si el
script de mapa lo exige en el mismo fichero — **si** `map_workflows.py` escribe
otro path, unidad separada R2 sobre `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md`
vía el generador (no edición a mano). Preferir: R1 + `make` que el verify ya
gatea; si verify exige guide committed, añadir:

| R2 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | modify (generated) | low | `implementer_agent` | ⏳ |

### Track P — probe higiene

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `scripts/session_probe.py` | modify | medium | `implementer_agent` | ⏳ |
| P2 | `tests/test_session_protocol.py` | modify | low | `implementer_agent` | ⏳ |

P1: finding advisory `stale_resume_or_closed_sprint` (D-P1). No exit 2.

P2: fixture IN_PROGRESS+CLOSED → finding presente; IN_PROGRESS+OPEN en
`ai-sprint/039` → ausente. **Si L4 ya toca este fichero**, fusionar P2 en L4
(un solo commit al mismo path) — Phase 4.1 decide; no dos commits al mismo
file.

### Track D — docs de cierre de programa

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `doc_orchestrator` | ⏳ |
| D2 | `docs/decisions/ADR-0002-drift-verdict-exit-codes.md` | modify | low | `doc_orchestrator` | ⏳ |

D1: Status Next = 039 `start-close-lifecycle` in flight (o cerrar cola 034–038
y apuntar programa siguiente). D2: Consequences — refresh mecanizado en deploy
(`refresh-baseline`); close ya no es el refresco.

---

## Dependencies

None.

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `/agents:start` boot | script `session_start.py --boot` | `commands/start.md`, `workflows/start_workflow.md` |
| Baseline post-deploy | script `session_state.py refresh-baseline` | `workflows/deployment_workflow.md` `baseline_refresh` |
| Bridge stale check | función en `cursor_adapter` + install | `session_start.py --boot` |
| Drift S tag list | `detect_drift.py` | `session_start.py`, `start_workflow` `drift_check` |
| Anchor hygiene | `session_probe.py` advisory | `session_start.py --boot`, `start_workflow` probes |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | **14** (L1–L4, B1–B4, C1–C2, R1[+R2], P1[+P2→L4], D1–D2) | Count Work rows; R2/P2 solo si Phase 4 confirma path separado |
| Subagents dispatched | `0` | Cursor `sequential` |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` |

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `git merge-base --is-ancestor $(python3 -c "import json;print(json.load(open('docs/active_state.json'))['last_close_commit'])") HEAD` | **Yes** — baseline huérfano post-deploy (defecto L) |
| `python3 scripts/session_start.py --boot --tool cursor; echo $?` con drift forzado 2 | **Yes** hasta B1 — hoy no existe `--boot` / no propaga |
| `rg 'Phase 1 \\(graph_rebuild\\)' config/artifact_registry.json` | **Yes** — fase incorrecta (defecto R) |
| Probe sobre anchor actual (IN_PROGRESS + CLOSED + resume 038) | **Yes** hasta P1 — hoy silencio |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 scripts/session_state.py refresh-baseline; python3 -c "import json; print(json.load(open('docs/active_state.json'))['last_close_commit'][:12])"; git rev-parse --short HEAD` | mismos 12 chars; exit 0 |
| `python3 scripts/detect_drift.py; echo $?` (tras refresh en tip limpio) | `0`; sin aviso huérfano; si hay S, tags cubridores incluyen `v4.21.0` o el tag actual |
| `python3 scripts/session_start.py --boot --tool cursor; echo $?` | `0` en árbol sano; briefing ≤80 líneas |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/039-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `rg 'Phase 5 \\(graph_rebuild\\)' config/artifact_registry.json` | match |
| `make verify` | exit `0` |
| `venv_skillopt/bin/python -m pytest tests/test_session_start.py tests/test_session_protocol.py -q` | passed (y `test_cursor_adapter` si C2) |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `scripts/session_state.py` | `refresh-baseline` |
| `scripts/session_start.py` | `--boot` + propagación drift |
| `scripts/detect_drift.py` | tags cubridores + texto S |
| `scripts/session_probe.py` | higiene anchor |
| `scripts/cursor_adapter.py` | `commands_stale` |
| `commands/start.md` | invoca `--boot` |
| `workflows/start_workflow.md` | v6.5.0; operator = script |
| `workflows/deployment_workflow.md` | `baseline_refresh` |
| `config/artifact_registry.json` | phase graph_rebuild |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerado si R2 |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Next 039 |
| `docs/decisions/ADR-0002-drift-verdict-exit-codes.md` | refresh en deploy |
| `tests/test_session_*.py` / `test_cursor_adapter.py` | cobertura L/B/C/P |
| `CHANGELOG.md` | entrada `[Unreleased]` al close |

**Measured figures.** Toda cifra en Context/Verification lleva comando (tabla
Context).

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Reescribir celdas históricas largas de `close_workflow.md` | Ruido RA-14; solo tocar deployment + start + scripts |
| `load_proven_families()` / abaratar gate | Fuera 034–038; ADR-0003; no es lifecycle start/close |
| Medidor tokens Cursor (`cache_read`) | No hay transcript en disco; ADR-0006 mitad portable = Cost section |
| CE-5 / política sandbox Cursor product | 036/037 OoS; distinto de bridge freshness |
| Symlink `.cursor/commands` → `commands/` en nucleus | Cambiaría el contrato del adapter; C1 hash basta |
| Auto-clear `resume_pointer` en claim | P1 solo advisory |
| `/agents:reconcile` rewrite | Solo deja de ser peaje falso post-deploy |

---

## Abort criterion

Si `refresh-baseline` hace que `require-released` pase en un tip **no** sellado
por `close` (rompe el gate de deploy), o si `--boot` escribe el anchor sin que
drift exit 2 pueda impedir el claim: **revertir** L1/B1 y no promover. Criterio
observable: test que `require-released` en `ai-sprint/*` tras solo `release`
sigue pasando, y que drift 2 en boot no deja `status: IN_PROGRESS` nuevo.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | _(pending Human OK)_ |
| **Date** | |
| **Plan commit at approval** | _(Phase 3 commit SHA)_ |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop`. Phases 6–8 only if the human arms `loop_guard.py start` first
(`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).*
