# Implementation Plan: Sprint 035 — core-pipeline (C/E/H/F)

**Canonical path**: `docs/sprints/035-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/035` · **Base**: `main` at `c93e851`
**Status**: `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`. Spanish permitted here
> (`agents.md §1 user_chat`). Hereda Design D3/D5/D10/D12/D13/D15/D16 del plan
> sellado de 034 (`docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md`); este
> documento no reabre esas decisiones — las ejecuta.

---

## Context

Sprint **034** desplegó `v4.17.0` (PR #66) con A/B/P/I/K/J/N. El programa
**034–038** deja a **035** los tracks **C E H F** (17 unidades). Estado medido
en `main` @ `c93e851` (2026-08-26):

| Hecho | Comando / evidencia |
| :--- | :--- |
| `gate.cursor.model` es `null` (hereda el picker) | `python3 -c "import json; print(json.load(open('config/model_tiers.json'))['tiers']['gate']['cursor'])"` → `{'model': None, 'family': None}` |
| `--check` **afirma lo contrario** de D13: falla si `gate` tiene filas | `scripts/audit_cursor_models.py:269-271` + docstring L25–26 |
| `make cursor-tiers` **no** pasa `--check` (`RA-16`) | `Makefile:101` → `python3 scripts/audit_cursor_models.py` sin flag |
| No existe briefing de start | `test -f scripts/session_start.py` → ausente |
| `start_workflow.md` sigue siendo ensayo largo | `wc -c workflows/start_workflow.md` → **18446** (criterio C2: **&lt; 8000**) |
| Coste de releer anexos en start | `WORKFLOWS_STEP_MAP_GUIDE.md` 13085 B; `UPSTREAM_FINDINGS_FROM_HOSTS.md` 77266 B |
| Perfil token-economy sigue diciendo «13 profiles» | `rg -n '13 profiles' agents/token_economy_agent.md` → hit en `tier_ownership` (mapa tiene 14 desde 033) |
| Hosts: primer re-enable = pin manual a `v4.17.0`; desde **035** `/start` auto-pincha | Track P ya en 034; cola en `021-030-program-queue.md` Status |

**Hecho cuando 035 cierra:** `/start` imprime briefing ≤80 líneas; `Task` aplica
el mapa vía `--resolve`; `gate.cursor` fijo por techo estructural (familia ≠
`author`); `make verify` incluye check `(f)`; `token_economy_agent` declara
propuesta Model/Effort + 14 perfiles.

---

## Design

Sin decisiones nuevas. Referencias normativas (no copiar el debate):

| ID | Qué ejecuta 035 |
| :--- | :--- |
| **D3** | Track C — `session_start.py` + workflow corto |
| **D5 / ADR-0010** | Track E — `--resolve` + Phase 7/`Task` |
| **D10 / D12** | Track F — selector puro + cadencia en el perfil |
| **D13 / ADR-0011** | Track H — techo estructural; supersede solo la cláusula `null` de ADR-0003 |
| **D15** | H3 check `(f)` — perfil `tier:`/`model:` vs mapa Claude |
| **D16** | E0 documenta gate-replay; **ejecución = 038** |

**DAG (sin condicionales):**

```
E0 → E1 → E2 → E3 → E4 → E5 → E6 → C5
                              ↘ H2 (tras E6; H1 antes)
C1 → C4
C2 → C3   (C2 no reabre lightweight_sync / P3)
F3 paralelo tras E0 (sin dependencia de archivo con E/H/C)
H1 → H2 → H3 → H4
```

Misma regla de 034: E2/E5/E6 son commits secuenciales del mismo archivo;
C5 es el **primer** toque del `Makefile` en este programa (L3 en 036 será el
segundo). P3 ya tocó `start_workflow.md`; C2 es el siguiente toque y **no**
reabre la celda `lightweight_sync`.

---

## Work

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E0 | `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | modify | medium | `doc_orchestrator` | ⏳ |
| E1 | `docs/decisions/ADR-0010-cursor-task-applies-tier-map.md` | create | high | `doc_orchestrator` | ⏳ |
| E2 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | ⏳ |
| E3 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | ⏳ |
| E4 | `tests/test_audit_cursor_models.py` | create | medium | `implementer_agent` | ⏳ |
| E5 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | ⏳ |
| E6 | `scripts/audit_cursor_models.py` | modify | high | `implementer_agent` | ⏳ |
| C1 | `scripts/session_start.py` | create | high | `implementer_agent` | ⏳ |
| C2 | `workflows/start_workflow.md` | modify | high | `orchestrator` | ⏳ |
| C3 | `commands/start.md` | modify | low | `orchestrator` | ⏳ |
| C4 | `tests/test_session_start.py` | create | medium | `implementer_agent` | ⏳ |
| C5 | `Makefile` | modify | medium | `implementer_agent` | ⏳ |
| H1 | `docs/decisions/ADR-0011-gate-cell-by-structural-ceiling.md` | create | high | `doc_orchestrator` | ⏳ |
| H2 | `config/model_tiers.json` | modify | high | `rule_validator` | ⏳ |
| H3 | `scripts/verify_references.py` | modify | high | `implementer_agent` | ⏳ |
| H4 | `tests/test_verify_references.py` | modify | medium | `implementer_agent` | ⏳ |
| F3 | `agents/token_economy_agent.md` | modify | medium | `agent_orchestrator` | ⏳ |

### Criterios de hecho por unidad (extracto operativo)

| # | Done-criterion |
| :--- | :--- |
| E0 | Guía nombra ledger como evidencia + protocolo gate-replay (vocabulario ADR-0008); **no** ejecuta el trial |
| E1 | ADR-0010 existe; supersede solo el *contexto* «sin primitiva» de ADR-0007; prohibición API intacta |
| E2 | `--resolve mechanical\|author\|gate\|<profile>` imprime `(modelId, effort)`; `gate` null → `session` |
| E3 | Phase 7 y unidades mechanical Cursor mandan `Task` con `model` = `--resolve` (o Model escalado) |
| E4 | Pytest cubre resolve + propuesta author/gate según E2/E5/E6 |
| E5 | Con applied ≠ mapa, `make cursor-tiers` propone celda del mapa; applied = discrepancia |
| E6 | Tabla `gate` no vacía; ninguna fila de familia `author`; `--check` falla si `gate` vacío o catálogo `None`; borra cita `§D7` obsoleta. **No** toca `Makefile` (eso es C5) |
| C1 | Exit 0; briefing ≤80 líneas; conteo findings, no dump UPSTREAM |
| C2 | `wc -c workflows/start_workflow.md` **&lt; 8000**; invoca C1; no reabre `lightweight_sync` |
| C3 | `commands/start.md` apunta al flujo briefing→Principal |
| C4 | Pytest de C1 (exit, tope de líneas, sin dump) |
| C5 | Tres targets en un commit, orden: `session-start`, `model-ledger` (stub para 037), `cursor-tiers` **con** `--check` |
| H1 | ADR-0011 supersede **solo** la cláusula `null` de ADR-0003; no abarata gate |
| H2 | `gate.cursor.model` no null; `family != author.family`; `effort` = máximo de `parameterDefinitions` del modelo (no literal `high` de Claude); `_comment` con fecha+#035 |
| H3 | Check `(f)` en `verify_references.py`: perfil `model:` == `model_tiers[tier].claude_code.model` |
| H4 | Alterar `agents/qa_agent.md` model → `make verify` ≠ 0 citando `(f)`; revertir → 0 |
| F3 | `task_scope_model_proposal` + D10/D12; `tier_ownership` dice 14 (no «13 profiles»); sin `prior_ownership` |

---

## Dependencies

None

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Briefing `/start` | script `session_start.py` | `workflows/start_workflow.md` + `make session-start` (C5) |
| Resolve tier → model | script `audit_cursor_models.py --resolve` | `pipeline_workflow.md` Phase 6/7 (E3); `make cursor-tiers` |
| Guard tabla `gate` | `--check` invertido (E6) | `make cursor-tiers` (C5 cablea el flag) |
| Celda `gate.cursor` | techo estructural (H2); no ranking | humano aprueba plan; `rule_validator` escribe JSON |
| Check `(f)` perfil↔mapa | script en `verify_references.py` | `make verify` |
| Stub `model-ledger` | target Makefile vacío de cuerpo útil hasta 037 | `make model-ledger` (G1 lo implementa) |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | **17** | Filas Work arriba |
| Subagents dispatched | `0` | Cursor `sequential` — roles advisory; gates en contexto fresco obligatorios |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` → `measurable: false` |

Orden de commits (Cost DAG): `E0 → E1 → E2 → E3 → E4 → E5 → E6 → C5` y en
paralelo lógico `C1 → C4`, `C2 → C3`, `H1 → H2 → H3 → H4`, `F3` — con la
restricción dura **H2 y C5 después de E6**.

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `test -f scripts/session_start.py` | **Yes** — ausente (C1) |
| `wc -c workflows/start_workflow.md` &lt; 8000 | **Yes** — 18446 (C2) |
| `python3 scripts/audit_cursor_models.py --resolve mechanical` | **Yes** — flag inexistente (E2) |
| `make cursor-tiers` emite filas `## Gate` | **Yes** — `propose_tiers` deja `gate` vacío (E6) |
| `python3 scripts/audit_cursor_models.py --check; echo $?` tras E6 | Hoy exit 0 con gate vacío; tras E6 debe fallar si vacío — **Yes** el sentido del guard está invertido |
| `json gate.cursor.model is not None` | **Yes** — `None` (H2) |
| Alterar `qa_agent` model a `sonnet` → `make verify` cita `(f)` | **Yes** — check `(f)` ausente (H3) |
| `rg -n '13 profiles' agents/token_economy_agent.md; echo $?` | **Yes** — exit 0 / hit (F3); esperado post-F3: exit 1 |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 scripts/session_start.py; echo $?` | `0`; briefing &lt; 80 líneas; sin dump completo de UPSTREAM |
| `wc -c workflows/start_workflow.md` | **&lt; 8000** |
| `python3 scripts/audit_cursor_models.py --resolve mechanical; echo $?` | `0`; imprime `composer-2.5` (o slug mapa mechanical) |
| `python3 scripts/audit_cursor_models.py --resolve gate; echo $?` | `0`; tras H2 imprime celda; si vacía → `session` sin inventar id |
| `python3 scripts/audit_cursor_models.py \| rg -A3 '## Gate'` | ≥1 fila; ninguna familia de `author` |
| `python3 -c "import json; t=json.load(open('config/model_tiers.json'))['tiers']; print(t['gate']['cursor'], t['author']['cursor'])"` | `gate.model` no null; `gate.family != author.family` |
| `make cursor-tiers; echo $?` | `0` con `--check` (gate no vacío) |
| `make verify; echo $?` | `0`; con `agents/qa_agent.md` model=`sonnet` ≠0 citando `(f)` |
| `rg -n '13 profiles' agents/token_economy_agent.md; echo $?` | `1` |
| `python3 -m pytest tests/test_session_start.py tests/test_audit_cursor_models.py tests/test_verify_references.py -q; echo $?` | `0` |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `docs/sprints/035-core-pipeline/IMPLEMENTATION_PLAN.md` | Este plan |
| `scripts/session_start.py` / `tests/test_session_start.py` | Briefing `/start` |
| `workflows/start_workflow.md` / `commands/start.md` | Flujo briefing→Principal; tope de tamaño |
| `scripts/audit_cursor_models.py` / `tests/test_audit_cursor_models.py` | `--resolve`, E5 mirror, E6 techo + `--check` invertido |
| `workflows/pipeline_workflow.md` | Task + resolve en mechanical / Phase 7 |
| `docs/decisions/ADR-0010-*.md` / `ADR-0011-*.md` | Runtime mapa; supersede cláusula null ADR-0003 |
| `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` | Ledger + protocolo replay (D16) |
| `config/model_tiers.json` | `tiers.gate.cursor` relleno |
| `Makefile` | `session-start`, `model-ledger`, `cursor-tiers --check` |
| `scripts/verify_references.py` / tests | Check `(f)` |
| `agents/token_economy_agent.md` | D10/D12 + 14 perfiles |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Status: 035 in flight → closed al close |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Regenerado por `make verify` si cambian celdas write |
| `CHANGELOG.md` | Entrada `[Unreleased]` al close |

---

## Out of scope

| Exclusion | Destino |
| :--- | :--- |
| Tracks M/L (instructing gates, censo era, forge ladder) | **036** |
| Track G (`model_ledger.py`) | **037** (C5 solo deja el target) |
| Family-trial / promoción Opus·GLM a `cursor.author` | **038** |
| Ejecutar gate-replay (D16) | **038**; E0 solo documenta |
| Abaratar `gate` con historial de ledger | Fuera 034–038; ADR-0003 en coste |
| Segundo toque `Makefile` (`cursor-era-audit`) | **036** L3 |
| Reabrir `lightweight_sync` / pin policy | Hecho en 034 P3 |
| Dar `Write` a gates o `principal_agent` | Prohibido (F-026-A1 / M9) |
| Scores o $/1M en `model_tiers.json` | ADR-0005 |

---

## Abort criterion

- Runtime elige el modelo «mejor» del catálogo en lugar de `--resolve` → revertir E1–E4.
- Gate `Task` inventa un slug mientras `cursor.gate.model` es null → revertir E3.
- `propose_tiers` sigue devolviendo el modelo aplicado como propuesta → revertir E5.
- `--check` sigue fallando cuando `gate` tiene filas (sentido pre-E6) → revertir E6.
- `H2` rellena `gate` con la misma familia que `author` → revertir H2.
- `H1` termina abaratando el gate → revertir H1+H2; prevalece ADR-0003.
- `H2` copia `effort: high` de Claude en vez del máximo expuesto → corregir celda.
- `C2` reabre o deshace `lightweight_sync` de P3 → revertir C2.
- `start_workflow` elimina un paso que `session_start.py` no ejecuta → revertir C1+C2.
- `C5` cablea `--check` **antes** de E6 (guard afirmaría gate vacío) → revertir orden; E6 primero.
- Gate-replay se ejecuta en 035 → parar; solo E0 documenta; trial = 038.
- Cualquier doc afirma que una familia es mejor que otra → borrar; D13 lo prohíbe.
- `session_start.py` hace red (salvo lo ya permitido en pin sync ajeno a C1) → revertir C1.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo (chat: «phase 5 ok») |
| **Date** | 2026-08-26 |
| **Plan commit at approval** | `7bcd12b` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop`. Phases 6–8 only if the human arms `loop_guard.py start` first
(`rules/loop_governance.md`).*
