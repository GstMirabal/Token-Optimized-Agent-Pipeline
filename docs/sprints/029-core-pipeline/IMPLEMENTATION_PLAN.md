# Implementation Plan: Sprint 029 — `documentation-truth`

**Canonical path**: `docs/sprints/029-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/029` · **Base**: `main` at `84201d2`
**Status**: `DRAFT` → Phase 5 Human OK after this file is committed (`triple_lock` lock 1)

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

**Objetivo (apéndice Sprint 029 de `docs/roadmaps/core/pipeline/021-030-program-queue.md`):** lo que ningún close individual puede hacer: narrativa transversal y **ampliar el conjunto contado**. El check de README verifica fielmente lo que cuenta, y lo que cuenta es incompleto.

**Por qué ahora.** Sprint 028 desplegado `v4.11.0` (2026-08-25). El roadmap declara **Next: `029` (`documentation-truth`)**. Esta cola se cierra aquí; `030` queda como segunda.

**Upstream leídos antes de planificar** (`agents.md §0 open_upstream_findings`):

| Ítem | Relación con 029 |
| :--- | :--- |
| T1–T5 (apéndice 029) | **Dentro** — unidades de este plan |
| `F-021-A2` | **Fuera** — rediseño del role-map implementer |
| `F-026-A2` | **Fuera** — `tier_escalation` automático; candidato 030 |
| `F-093-G1` | **Fuera** — Double-Gate sin clase de severidad; carried → `031` (`gate-verdict-classes`). Reproducido contra `84201d2` el 2026-08-25; **no parcheado**. Meterlo aquí sería el error de categoría de `F-023-S4` |

**Mediciones contra `84201d2` (reproducidas en la sesión de Planning):**

| Hecho | Comando / observación | Vs apéndice (stale) |
| :--- | :--- | :--- |
| 5 cifras del README coinciden con el árbol | `python3 scripts/check_readme_counts.py` → exit `0`: *11 rule contexts, 13 agents, 34 skills, 12 workflows, 13 slash commands* | Decía 10 rule contexts |
| `scripts/*.py` | `ls scripts/*.py \| wc -l` → **28** | Baseline v4.5.0: 17 |
| `config/*.json` | `ls config` → **6** | Baseline: 3 |
| README nombra Cursor | `grep -ci cursor README.md` → **7**; fila Integration ya cita `.cursor/` | T2 («el README no menciona Cursor») **ya no es cierto** |
| README cita `install.py` | `README.md:60,101` — `install.sh` es shim | T2/install.sh **ya hecho** en 026 |
| Guía slash commands sigue en `install.sh` + solo Claude | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md:12,21` | T3 **sigue abierto** |
| Guía **no** está en el registry | `grep AGENTS_SLASH config/artifact_registry.json` → vacío | T3 |
| `agents.md` | `wc -l agents.md` → **174** | Techo J1: 200 al cierre de 029 |
| Tabla *The queue* ponía 028 como `1st` | Corregido en R2 sobre este branch | Status ya decía 028 desplegado — `RA-14` |
| ADRs existentes | `ls docs/decisions/ADR-*.md` → **0001, 0002** | T4: faltan 0003–0007 |
| `F-093-G1` | `grep -nE 'APPROVED\|REJECTED\|RECORD\|CARRY' rules/qa_and_testing.md` → vacío; C6 sentence solo en `task_scope.md` de 023 | Abierto; no es unidad 029 |

**Qué es cierto cuando el sprint termina.**

1. «At a Glance» declara `scripts/` y `config/` con cifras que un script **genera o verifica** (J5: no a mano cada sprint).
2. La guía de slash commands describe las dos herramientas y `install.py`; el registry la nombra; `verify_commands.py` exige que §3.2 nombre cada `commands/*.md`.
3. Las cinco decisiones de programa tienen ADR (`0003`–`0007`).
4. El template de Implementation Plan obliga impacto documental + comando por cifra (T5/J4, desde 029).
5. `agents.md` ≤ 200 líneas.
6. `make verify` exit `0`.

---

## Design

**D1 — T2 reducido, no reescritura.** El apéndice prohíbe reescribir docs que otros sprints ya dejaron bien. El README ya es de dos herramientas. Lo que queda: badge «Built With» (solo Claude Code) y la guía. No hay sweep del README.

**D2 — T1 generado (J5), no número congelado.** `render_readme.py` no sirve: es identity-tags y **no** está en close (sobrescribiría el README a mano). Patrón de `generate_manifest.py`: el check **escribe** un bloque marcado en «At a Glance» y `make verify` falla si el bloque no coincide con el árbol.

Conteo pinneado en el test:

- `scripts/`: `scripts/*.py` (28 en `84201d2`). Fuera: `denylists/`, `install.sh`, `install_claude.sh`.
- `config/`: `config/*.json` (6 en `84201d2`).

**D3 — T5 vive en el template + `documentation_standard.md`, no en `agents.md`.** J1: este sprint no crece la constitución.

**D4 — Check `file:line` (J6) es barato y ciego a 4/4 de los fallos que lo motivaron.** Entra igual: coge citas **fuera de rango**. La mitigación real es T5 (cifra + comando). El check no se vende como si hubiera pillado aquellos cuatro. Escaneo: `docs/` vivo (guides, decisions, audits) — **no** `docs/sprints/` ni `docs/roadmaps/` históricos.

**D5 — ADRs 0003–0007**, uno por decisión del apéndice. No se reabren `F-021-A2`, `F-026-A2` ni `F-093-G1`.

**D6 — Intake de esta sesión en Ola 0.** El working tree traía el sello post-release `84201d2` y el registro de `F-093-G1`. Aterrizan en esta rama (RA-12: no a `main` durante Execution) como R0–R2, no como unidades de T1–T5.

---

## Work

Una fila = un commit atómico (`RA-08`) con **un fichero sujeto** (`jurisdictional_lock`). Assignees son rulesets bajo `delegation_mode: sequential` (Cursor).

### Ola 0 — Intake ya escrito (esta sesión)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R0 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | ✅ `08dbdb4` |
| R1 | `CHANGELOG.md` | modify | low | `principal_agent` | ✅ `8d55f25` |
| R2 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | ✅ `fb97de5` |

**Operaciones:**

- **R0** — Entrada `F-093-G1` bajo *Reported by a host*; status 2026-08-25. Done: `grep F-093-G1 docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` no vacío; checkbox abierto.
- **R1** — Asiento `[Unreleased]` del sello `84201d2`. Done: bullet nombra `84201d2` y PR #57/#58.
- **R2** — Línea Reconciled + carried `F-093-G1` → 031; tabla *The queue* marca 028 `✅` y 029 como **1st**. Done: fila 028 es `✅`; 029 no dice `3rd`.

### Ola 1 — T1 conjunto contado

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1.0 | `tests/test_check_readme_counts.py` | create | medium | `devops_agent` — deviation (tests/; `F-026-A1` gate is read-only) | ⏳ |
| T1.1 | `scripts/check_readme_counts.py` | modify | high | `devops_agent` | ⏳ |
| T1.2 | `README.md` | modify | medium | `doc_orchestrator` | ⏳ |
| T1.3 | `workflows/close_workflow.md` | modify | low | `governance_learner` | ⏳ |

- **T1.0** — Falla en `84201d2`: no hay check de `scripts/` ni `config/`.
- **T1.1** — Dos CHECKS más + modo que reescribe un bloque `<!-- COUNTED_START -->…<!-- COUNTED_END -->`. `make verify` sigue llamando el script; drift = exit `2`.
- **T1.2** — Insertar el bloque y badge Cursor en Built With (resto de T2).
- **T1.3** — Phase 2 `readme_counts`: el texto deja de decir que solo hay cinco cifras.

### Ola 2 — T3 guía + registry

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1 | `config/artifact_registry.json` | modify | medium | `devops_agent` | ⏳ |
| G2 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | modify | medium | `doc_orchestrator` | ⏳ |
| G3 | `skills/slash-commander/scripts/verify_commands.py` | modify | medium | `devops_agent` | ⏳ |

- **G1** — Entrada `AGENTS_SLASH_COMMANDS_GUIDE.md`, `scope: repository`, `required: false`.
- **G2** — `install.py --target {claude,cursor,both}`; Cursor `.cursor/commands/`; `install.sh` como shim.
- **G3** — El verificador de 13 comandos también exige que la tabla §3.2 nombre cada `commands/*.md`.

### Ola 3 — T4 ADRs

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A3 | `docs/decisions/ADR-0003-gates-never-drop-tier.md` | create | low | `doc_orchestrator` | ⏳ |
| A4 | `docs/decisions/ADR-0004-no-model-selector-agent.md` | create | low | `doc_orchestrator` | ⏳ |
| A5 | `docs/decisions/ADR-0005-prices-stay-out-of-config.md` | create | low | `doc_orchestrator` | ⏳ |
| A6 | `docs/decisions/ADR-0006-session-bound-before-tiering.md` | create | low | `doc_orchestrator` | ⏳ |
| A7 | `docs/decisions/ADR-0007-cursor-without-api-delegation.md` | create | low | `doc_orchestrator` | ⏳ |

Cada uno desde `ADR_TEMPLATE.md`. Citas con comando (T5). No reabrir 0001/0002.

### Ola 4 — T5, J1, J6

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | medium | `governance_learner` | ⏳ |
| P2 | `rules/documentation_standard.md` | modify | medium | `governance_learner` | ⏳ |
| J6.0 | `tests/test_verify_references.py` | modify/create | medium | `devops_agent` — deviation (tests/; `F-026-A1` gate is read-only) | ⏳ |
| J6.1 | `scripts/verify_references.py` | modify | high | `devops_agent` | ⏳ |

- **P1** — Sección obligatoria «Documentary impact» + «toda cifra lleva su comando».
- **P2** — T5 aplica **desde 029**; no retroactivo (J4).
- **J6.0** — Falla hoy: `` `README.md:99999` `` bajo `docs/` (guides/decisions/audits) no se rechaza.
- **J6.1** — Resolver `path:line` en ese corpus; fuera de rango → exit `2`.

### Ola 5 — Cierre documental

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | `CHANGELOG.md` | modify | low | `principal_agent` | ⏳ |

Entrada `[Unreleased]` del sprint 029 (distinta de R1).

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | This sprint adds no package |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Conteos README `scripts/` + `config/` | script | `make verify` + `close_workflow.md` Phase 2 `readme_counts` (ya invoca `check_readme_counts.py`) |
| `file:line` fuera de rango | script | `make verify` → `verify_references.py` |
| Guía ↔ 13 commands | script | `make verify` → `verify_commands.py` (ya invocado) |
| Fila T5 en cada plan | agent (Phase 1) | template P1; no hay script que lea planes en prosa |
| ADRs | agent, una vez | Phase 6; no recurrente |

Filter 5 (`token_economy_agent` `pre_approval_audit`): no se añade auditor-agente ni close-time `render_readme.py`.

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| T1.0: CHECKS no incluye scripts/config | **Yes** — this is the defect |
| G3: guía con `install.sh` como vía única | **Yes** — content; the name-count test is **No** (13 match) until G3 hardens it |
| J6.0: `README.md:99999` | **Yes** — the check does not exist |
| `check_readme_counts.py` de las 5 cifras | **No** — regression to protect |
| `make verify` | **No** — 500 passed at `/start` |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 scripts/check_readme_counts.py; echo $?` | `0`; imprime también scripts y config |
| `python3 skills/slash-commander/scripts/verify_commands.py; echo $?` | `0`; guía alineada |
| `python3 scripts/verify_references.py; echo $?` | `0` |
| `wc -l agents.md` | `≤ 200` |
| `make verify; echo $?` | `0` |
| `ls docs/decisions/ADR-000{3,4,5,6,7}-*.md` | 5 ficheros |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `README.md` | Bloque contado scripts/config; badge Cursor |
| `scripts/check_readme_counts.py` + test | 2 CHECKS + regeneración del bloque |
| `workflows/close_workflow.md` | Prosa de `readme_counts` |
| `config/artifact_registry.json` | Entrada de la guía |
| `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md` | Dos herramientas + `install.py` |
| `docs/decisions/ADR-0003`…`0007` | Cinco decisiones de programa |
| Template + `documentation_standard.md` | T5 obligatorio |
| `verify_references.py` | Check `file:line` |
| Cola 021-030 | Tabla de orden + carried `F-093-G1` |
| `CHANGELOG.md` | R1 (sello 028) + C1 (029) |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | R0 `F-093-G1` (intake, no el fix) |

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Reescritura general del README a dos herramientas | **Hecho** en 026/027 |
| `F-021-A2` implementer role | Sigue abierto; no es documental |
| `F-026-A2` `tier_escalation` automático | Candidato 030 |
| `F-093-G1` tres veredictos Double-Gate | Carried → `031` (`gate-verdict-classes`). No max-N-rounds, no subir three-strikes |
| Cuerpo de `token-saver-auditor` | 030 |
| 3 CodeQL en `main` | `repository_hardening_workflow` |
| Retro-T5 en planes 021–028 | J4: no |
| Crecer `agents.md` | J1; va a `rules/documentation_standard.md` |
| Semantic `graphify --update` de docs | Close Phase 1 |

---

## Abort criterion

1. T1.1 reescribe el README **fuera** del bloque marcado → revertir el commit (misma trampa que no cablear `render_readme.py` al close).
2. `wc -l agents.md` > 200 en cualquier commit del sprint → revertir ese commit; el texto va a `rules/`.
3. Un falso positivo de J6.1 que bloquee `make verify` en un sprint record histórico si el exclude falla → revertir J6.1, no hot-patch del scanner.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | *(Phase 5 — after this file is committed)* |
| **Date** | 2026-08-25 |
| **Plan commit at approval** | *(filled when Phase 5 runs)* |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

Human draft OK 2026-08-25: *"ok"*, then *"no, seguimos así. Continua"* (`F-093-G1` stays out of 029). Phase 5 still requires a second OK on the **committed** file.

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).*
