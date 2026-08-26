# Implementation Plan: Sprint 036 — core-pipeline (M/L)

**Canonical path**: `docs/sprints/036-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/036` · **Base**: `main` at `ba80a55`
**Status**: `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`. Spanish permitted here
> (`agents.md §1 user_chat`). Hereda Design **D18** / **D19** del plan sellado
> de 034 (`docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md`); este
> documento no reabre esas decisiones — las ejecuta. Prerrequisitos de 035
> (C5 / E3) ya en `main` (`v4.18.0`).

---

## Context

Sprint **035** desplegó `v4.18.0` (PR #67) con C/E/H/F. El programa
**034–038** deja a **036** los tracks **M** (forja host-submódulo) + **L**
(censo era Cursor 026–033) — **12** unidades. Estado medido en `main` @
`ba80a55` (2026-08-26):

| Hecho | Comando / evidencia |
| :--- | :--- |
| `scripts/audit_cursor_era.py` ausente | `test -f scripts/audit_cursor_era.py; echo $?` → `1` |
| `scripts/check_forge_ladder.py` ausente | `test -f scripts/check_forge_ladder.py; echo $?` → `1` |
| `SKILL_ASSIGNMENT_TEMPLATE.md` ausente | `test -f docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md; echo $?` → `1` |
| `AGENT_ASSIGNMENT_TEMPLATE.md` existe (I7 / 034) | `test -f docs/standards/templates/AGENT_ASSIGNMENT_TEMPLATE.md; echo $?` → `0` |
| CE-1 vivo sobre historia: 028 falla I4 | `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/028-core-pipeline; echo $?` → `2` (3 filas: P1, P1.1, D3) |
| 033 limpio para CE-1 | mismo comando sobre `033-core-pipeline` → exit `0` |
| Ventana 026–033 presente | `for s in 026..033; test -d docs/sprints/${s}-core-pipeline` → 8/8 `ok` |
| `skill.sh` nombrado y ausente | `rg -n 'skill\.sh' agents/skill_architect.md` → hits L3 + L17; `find . -name skill.sh` vacío |
| QA/Tester etiquetan Double-Gate como Phase 4 | `rg -n 'Phase 4' agents/qa_agent.md agents/tester_agent.md` → `double_gate_review` / `rejection_trigger` |
| Principal: Approval = Phase 3; execution = Phase 4 | `rg -n 'approval_gate\|execution' agents/principal_agent.md` |
| `qa_agent` description: «after Definitive Sprints» | frontmatter L3 + fila `double_gate_review` |
| Censo tools: 14 perfiles | `ls agents/*.md \| wc -l` → `14` |
| C5 (035) ya tocó `Makefile` | targets `session-start`, `model-ledger`, `cursor-tiers`; **sin** `cursor-era-audit` |
| E3 (035) ya tocó `pipeline_workflow.md` | Task + `--resolve`; **sin** `check_forge_ladder.py` |
| Gate cell fijada (H2) | `gate.cursor.model=claude-opus-5`, `author=grok-4.5` |
| `/start` briefing ≤80 líneas | `wc -c workflows/start_workflow.md` → **6272**; `session_start.py` presente |
| Tests forge / era ausentes | `rg -n 'check_forge_ladder\|audit_cursor_era\|forge_destination' tests/` → vacío |

**Hecho cuando 036 cierra:** `make cursor-era-audit` genera
`docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` (8 filas; 028 CE-1 > 0; 033 CE-1 =
0; exit siempre `0`); `check_forge_ladder.py` falla el fallback vacío en
fixture host y pasa con destino forjado; `skill_architect` deja de citar
`skill.sh`; Phase 4.1/4.2 nombran el chequeo; perfiles gate (qa/tester/
principal) alinean instructing con Phases 7 / 5 / 6 / 8; censo de 14 perfiles
pinneado en pytest. **Triaje O5** de filas `new` del censo al close — no
unidades mid-sprint.

---

## Design

Sin decisiones nuevas. Referencias normativas (no copiar el debate):

| ID | Qué ejecuta 036 |
| :--- | :--- |
| **D18** | Track L — censo CE-1–CE-5 sobre parsers existentes; producto derivado; exit `0` siempre; **no** en `verify` |
| **D19** | Track M — escalera de forja falsable (host-submódulo); plantilla skill; instructing gate; censo tools |
| **O5** | Hallazgos `new` del censo → clasificar al **close** de 036; no abrir unidades mid-sprint |
| **D11** | `CURSOR_ERA_EXECUTION_AUDIT.md` es derivado (como ledger); nunca fuente editada a mano |

**DAG (sin condicionales):**

```
L1 → L2 (mismo commit) → L3
M1 → M2 (mismo commit)
M3 ∥ M4 ∥ M6   (tras M1 forma estable; M6 no espera M7–M9)
M5 tras E3 (035, ya en main)
M7 → M8 → M9
```

L ∥ M (independientes). **L3** = segundo toque del `Makefile` (después de C5).
**M5** = toque de `pipeline_workflow.md` después de E3/I2/K6.

---

## Work

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| L1 | `scripts/audit_cursor_era.py` | create | high | `implementer_agent` | ⏳ |
| L2 | `tests/test_audit_cursor_era.py` | create | medium | `implementer_agent` | ⏳ |
| L3 | `Makefile` | modify | medium | `implementer_agent` | ⏳ |
| M1 | `scripts/check_forge_ladder.py` | create | high | `implementer_agent` | ⏳ |
| M2 | `tests/test_check_forge_ladder.py` | create | medium | `implementer_agent` | ⏳ |
| M3 | `agents/skill_architect.md` | modify | high | `agent_orchestrator` | ⏳ |
| M4 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | create | medium | `doc_orchestrator` | ⏳ |
| M5 | `workflows/pipeline_workflow.md` | modify | high | `orchestrator` | ⏳ |
| M6 | `tests/test_agent_profile_census.py` | create | medium | `implementer_agent` | ⏳ |
| M7 | `agents/qa_agent.md` | modify | high | `agent_orchestrator` | ⏳ |
| M8 | `agents/tester_agent.md` | modify | high | `agent_orchestrator` | ⏳ |
| M9 | `agents/principal_agent.md` | modify | high | `agent_orchestrator` | ⏳ |

### Criterios de hecho por unidad

| # | Done-criterion |
| :--- | :--- |
| L1 | `python3 scripts/audit_cursor_era.py; echo $?` → `0`; escribe `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` con **8** filas (026–033); fila 028 CE-1 > 0; fila 033 CE-1 = 0; bloque CE-5 con protocolo sandbox vs no-sandbox + comandos reproducibles. Usa parsers existentes (`check_task_scope.collect_findings`, `check_role_artifact.missing_for_role` / `missing_gate_row`, `check_gate_log.gate_tables`) — **no** parsers nuevos. Exit **siempre** `0` (censo, no gate) |
| L2 | Pytest: dir ausente → fila omitida sin crash; 033 CE-1 = 0; Notes Tester con `tests/test_implementer_role.py` y sin `tests/` → CE-4 = 1; borrar el markdown y re-ejecutar L1 lo regenera (no es fuente) |
| L3 | Target `cursor-era-audit` invoca L1. **No** aparece como receta de `verify`. `make cursor-era-audit; echo $?` → `0` |
| M1 | Dos modos vía `_mode.is_nucleus()`. Host: Assignee sin perfil → `Destination=host:.claude/agents/` **y** `.md` en host pasa; destino vacío o escrito bajo `.agents/agents/` → exit `2`. Skill sin manifiesto: registro P3 miss + `SKILL.md` bajo `.claude/skills/<name>/` pasa; «No skill was forged» sin rastro P3 o skill bajo `.agents/skills/` → `2`. Núcleo create: `Destination=nucleus:PR` + fichero en `agents/` pasa. P3 **sin red** (JSON simulado). Fixture layout = `tests/test_installer.sh` |
| M2 | Tres asserts host (vacío→2, forjado en `.claude/agents/`→0, forjado en `.agents/agents/`→2) + simétrico skills; `pytest tests/test_check_forge_ladder.py -q` → `0` |
| M3 | Sustituye `skill.sh` por escalera nombrable: P1 `skills/manifest_skills.json` → P2 `autoskills-3rd` → P3 `https://skills.sh/` (+ WebSearch/WebFetch) → P4 Three-File en destino host. `rg -n 'skill\.sh' agents/skill_architect.md; echo $?` → `1` |
| M4 | Plantilla Phase 4.2: columnas mínimas unidad, skill, P1–P4 (hit/miss), Destination. Citada desde M5 |
| M5 | Phase 4.1 y 4.2 nombran `python3 scripts/check_forge_ladder.py --sprint-dir …`. `rg -n 'check_forge_ladder' workflows/pipeline_workflow.md` ≥1 en ambas celdas |
| M6 | Cinco asserts: (1) perfil en `tiers.gate.profiles` sin `Write`/`Edit`; (2) qa/tester con `Bash`; (3) orchestrator con `Write`; (4) `name:` kebab = stem; (5) recuento = 14. Alterar `qa_agent` con `Write` → test exit ≠ 0 |
| M7 | `double_gate_review` / `rejection_trigger` → Phase **7**; description «after Phase 6 Execution»; sin tocar `tools:` / `verdict_routing`. `rg -n 'Definitive Sprints' agents/qa_agent.md` sin hit en frontmatter de fase |
| M8 | Igual relabel Phase **7** en tester; sin tocar `tools:` |
| M9 | (1) `consensus_loop` aclara: la *sesión* con Write materializa el plan (Phase **1**); el subagente no declara Write. (2) `approval_gate` → Phase **5**. (3) `execution` / `remediation_loop` → Phase **6**. (4) fila Phase **8** nombra `PHASE_REGISTER.md` / host `CHANGELOG.md` (escritura en sesión). `tools:` sigue sin Write/Edit |

---

## Dependencies

None

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Censo era Cursor 026–033 | script `audit_cursor_era.py` | `Makefile` `cursor-era-audit` (**no** `verify`) |
| Escalera de forja agente/skill | script `check_forge_ladder.py` (P3 simulado) | `pipeline_workflow.md` Phases 4.1 y 4.2 |
| Censo 14 perfiles (tools/fase/kebab) | pytest | `make verify` vía suite / invocación Tester |
| Instructing gate Phase labels | agent edit de perfiles | Phase 6 unidades M7–M9 |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | **12** | Filas Work arriba |
| Subagents dispatched | `0` | Cursor `sequential` — roles advisory; gates en contexto fresco |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` → `measurable: false` |
| Elegibles `mechanical` | L2, M2, M6 | `Task` + `--resolve mechanical` (ADR-0010) |

Orden de commits: `L1+L2 → L3` ∥ `M1+M2 → M3 → M4 → M5 → M6 → M7 → M8 → M9`
(M3/M4/M6 pueden reordenarse tras M2 si no chocan archivos; M7→M8→M9 fijo).

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `test -f scripts/audit_cursor_era.py` | **Yes** — L1 |
| `test -f scripts/check_forge_ladder.py` | **Yes** — M1 |
| `test -f docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | **Yes** — M4 |
| `rg -n 'cursor-era-audit' Makefile; echo $?` | **Yes** — L3 (sin hit) |
| `rg -n 'check_forge_ladder' workflows/pipeline_workflow.md; echo $?` | **Yes** — M5 |
| `rg -n 'skill\.sh' agents/skill_architect.md; echo $?` | **Yes** — M3 (exit 0 hoy; post-M3 debe ser 1) |
| `rg -n 'Phase 4' agents/qa_agent.md agents/tester_agent.md` en `double_gate_review` | **Yes** — M7/M8 |
| `rg -n 'Phase 3' agents/principal_agent.md` en `approval_gate` | **Yes** — M9 (debe ser Phase 5) |
| `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/028-core-pipeline; echo $?` | **Yes** como dato de censo — CE-1 > 0 (L1 lo tabula; **no** reescribe 028) |
| `pytest tests/test_agent_profile_census.py` | **Yes** — archivo ausente (M6) |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/036-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `python3 scripts/audit_cursor_era.py; echo $?` | `0`; markdown con 8 filas; 028 CE-1 > 0; 033 CE-1 = 0 |
| `make cursor-era-audit; echo $?` | `0`; target **ausente** de la receta `verify` |
| `python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/033-core-pipeline; echo $?` | `0` en núcleo (033 A1 destino+fichero) |
| Fixture host sin `.claude/agents/<nuevo>.md` → `check_forge_ladder` | exit `2` |
| `rg -n 'skill\.sh' agents/skill_architect.md; echo $?` | `1` |
| `rg -n 'check_forge_ladder' workflows/pipeline_workflow.md` | ≥1 en Phase 4.1 y 4.2 |
| `rg -n 'Phase 4' agents/qa_agent.md agents/tester_agent.md` | sin `double_gate_review` / `rejection_trigger` en Phase 4 |
| `rg -n 'Phase 7' agents/qa_agent.md agents/tester_agent.md` | hits en esas claves |
| `rg -n 'approval_gate' agents/principal_agent.md` | fila nombra Phase 5 |
| `python3 -m pytest tests/test_audit_cursor_era.py tests/test_check_forge_ladder.py tests/test_agent_profile_census.py -q; echo $?` | `0` |
| `make verify; echo $?` | `0` |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `docs/sprints/036-core-pipeline/IMPLEMENTATION_PLAN.md` | Este plan |
| `scripts/audit_cursor_era.py` / `tests/test_audit_cursor_era.py` | Censo CE-1–CE-5 |
| `docs/audits/CURSOR_ERA_EXECUTION_AUDIT.md` | Generado por L1/L3; nunca editado a mano |
| `Makefile` | Target `cursor-era-audit` (segundo toque post-C5) |
| `scripts/check_forge_ladder.py` / `tests/test_check_forge_ladder.py` | Fallback forja host-submódulo |
| `agents/skill_architect.md` | Escalera P1–P4; sin `skill.sh` |
| `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | Forma Phase 4.2 |
| `workflows/pipeline_workflow.md` | 4.1/4.2 invocan `check_forge_ladder.py` |
| `tests/test_agent_profile_census.py` | Pin 14 perfiles |
| `agents/qa_agent.md` / `tester_agent.md` / `principal_agent.md` | Instructing Phase 7 / 5 / 6 / 8 |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Status: 036 in flight → closed al close |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Regenerado por `make verify` si cambian celdas write |
| `CHANGELOG.md` | Entrada `[Unreleased]` al close |

---

## Out of scope

| Exclusion | Destino |
| :--- | :--- |
| Track G (`model_ledger.py`) | **037** |
| Rider **S** — sandbox-safe `py_compile` + nucleus `.bridge_cursor.lock` | **037** (queued in `021-030-program-queue.md`; measured 2026-08-26 on `ai-sprint/036`) |
| Family-trial / promoción Opus·GLM a `cursor.author` | **038** |
| Relabel Phase 2→4.1/4.2/4.3 en orchestrator cluster | Reorden O5 o sprint posterior (034 Out of scope) |
| Meter censo en `make verify` | Prohibido (rojo histórico 028–032; abort I4) |
| Reescribir `SPRINT_LOG.md` / `task_scope.md` de 026–033 | Censo documenta; no lava |
| Convertir filas `new` del censo en unidades mid-sprint | O5: triaje al **close** |
| Forjar skill/agente real en núcleo «para demostrar» | Fixture M2 solamente |
| HTTP real a `skills.sh` en `make verify` | P3 simulado |
| Dar `Write` a gates o `principal_agent` | F-026-A1 / M9 |
| Encender `ruff check .` en verify | Exclusión migración 032/033 |
| Tratar sequential como defecto de 026–033 | M3 PASSED en 026 |

---

## Abort criterion

- `audit_cursor_era.py` sale `2` porque 028 tiene CE-1 > 0 → revertir L1 (censo no es gate).
- L3 añade `cursor-era-audit` como dependencia de `verify` → revertir L3.
- L1 reescribe `task_scope.md` / `SPRINT_LOG.md` históricos → revertir L1.
- Filas `new` del censo se convierten en Work mid-sprint sin reorden O5 → parar; triaje al close.
- `check_forge_ladder.py` acepta un `.md` bajo `.agents/agents/` desde fixture host → revertir M1.
- M1/M2 hacen HTTP real a `skills.sh` dentro de `make verify` → revertir.
- M3 deja `skill.sh` o inventa un binario local con ese nombre → revertir M3.
- M7/M8 añaden `Write`/`Edit` a qa/tester → revertir; prevalece F-026-A1.
- M9 añade `Write` a `principal_agent` → revertir.
- M6 pinnea recuento ≠ 14 o permite gate con Write → revertir M6.
- M5 omite el invocador en 4.1 o 4.2 → revertir M5 (`RA-16`).

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | Gustavo (chat: «ok») |
| **Date** | 2026-08-26 |
| **Plan commit at approval** | `7ebf251` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop`. Phases 6–8 only if the human arms `loop_guard.py start` first
(`rules/loop_governance.md`).*
