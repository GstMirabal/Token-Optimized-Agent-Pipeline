# Implementation Plan: Sprint 037 — core-pipeline (Track G + rider S)

**Canonical path**: `docs/sprints/037-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/037` · **Base**: `main` at `6a87cf0` (`v4.19.0`)
**Status**: `DRAFT`

> Authored at Phase 1 (Planning) by `principal_agent`. Under `session_tool: cursor`,
> `SwitchMode` to plan is PROHIBITED (`RA-18`). Committed before Phase 5
> (`agents.md §2 triple_lock`). Spanish permitted in this document (`agents.md §1 user_chat`).

---

## Context

Sprint **037** follows sealed **036** (`v4.19.0`, PR #68): Track **G** (derived
model/gate ledger, Design **D11** from Sprint 034) plus rider **S** (Cursor
**agent sandbox** false reds measured 2026-08-26 on `ai-sprint/036` — not O5
census rows).

| Fact | Measurement | Reproduce |
| :--- | :--- | :--- |
| `scripts/model_ledger.py` | absent | `test -f scripts/model_ledger.py; echo $?` → `1` |
| `docs/audits/MODEL_LEDGER.md` | absent | `test -f docs/audits/MODEL_LEDGER.md; echo $?` → `1` |
| `make model-ledger` | stub only | `make model-ledger` prints `deferred to Sprint 037` while script missing |
| `make verify` py_compile | uses `xargs` | `rg -n 'xargs python3 -m py_compile' Makefile` → line present |
| Sandbox `xargs` / `ARG_MAX` | fails under agent sandbox | In Cursor agent sandbox: `find . -name '*.py' -not -path '*/venv_skillopt/*' \| head -3 \| xargs python3 -m py_compile; echo $?` → `1`. Unrestricted shell → `0` (`getconf ARG_MAX` → `1048576`) |
| Nucleus `.bridge_cursor.lock` | missing after cursor install | `bash scripts/install.sh --target cursor` then `test -f .bridge_cursor.lock; echo $?` → `1` (code: nucleus `cursor`/`both` `return 0` before `write_bridge_locks`) |
| Formal UPSTREAM open set | empty since Sprint 033 | Status table at Sprint 033: `*(none in this file's open set)*` |
| Briefing «Still open» count | **5** (false positive) | `python3 scripts/session_start.py` counts historical `\| **Still open** \|` rows — **out of scope** for 037 |

**Done when:** `make model-ledger` exits `0` and writes `docs/audits/MODEL_LEDGER.md` with rows for **032** and **033**; `make verify` py_compile does not call `xargs` / does not require `os.sysconf('SC_ARG_MAX')`; nucleus `--target cursor` (and `both`) writes `.bridge_cursor.lock`; paired tests fail on current tree then pass after the fix.

**Inherits (do not re-open):** D11/D12/D9 from `docs/sprints/034-core-pipeline/IMPLEMENTATION_PLAN.md`; Makefile stub from 035 C5; era audit / forge from 036. Family-trial remains **038**.

**Phase 1 defaults (Human OK 2026-08-26 — proceed after 036 close clarification):**

| # | Decision |
| :--- | :--- |
| Q1 S1 | `find … -exec python3 -m py_compile {} +` in `Makefile` (no new script) |
| Q2 G3 | Include — wire `make model-ledger` in `close_workflow.md` |
| Q3 S3/C6 | Invert nucleus Cursor lock assert (`lock` must exist after `--target cursor`) |
| Q4 Ledger artifact | Commit generated `MODEL_LEDGER.md` (032/033 required rows) |
| Q5 Still-open counter | Out of scope |
| Q6 Pre-031 | Omit sprints `< 031` and sprints without gate table |
| Q7 038 gate | First usable ledger row post-037 + baseline 032/033 is enough |

---

## Design

| ID | Decision | Why (rejected alternative) |
| :--- | :--- | :--- |
| **D-G1** | Ledger is **generated**, never hand-edited (`state_homologation`) | Same pattern as `WORKFLOWS_STEP_MAP_GUIDE.md` / era audit. Rejected: maintaining a second state file |
| **D-G2** | Import `gate_tables()` from `check_gate_log.py` and `work_tables()` from `check_task_scope.py` — **no new parsers** | Abort if G1 invents parsers (034 abort criterion). Rejected: copy-paste markdown scraping |
| **D-G3** | Emit one row per sprint with gate table: `sprint_id`, `tier`, `model_id`, `effort`, units, Gate-1 rounds, Gate-2 rounds, verdict classes. Sprint without gate table → omit with note, exit `0`. Sprint id `< 031` → omit (historical vocabulary) | Matches G2 fixtures in 034. Rejected: rewriting closed `SPRINT_LOG`s |
| **D-G4** | Invoker: `Makefile` target `model-ledger` (already exists) + **G3** wires `close_workflow.md` to run it at close (`RA-16`, 034 Mechanisms). **Not** added to `make verify` (same class as `cursor-era-audit`) | Rejected: verify-blocking historical gaps |
| **D-G5** | Out of 037: `load_proven_families()` reading the ledger to cheapen `gate`; promoting `cursor.author` (038); Cursor token meter | ADR-0003 / D6-P5; program queue order |
| **D-S1** | Replace `find … \| xargs python3 -m py_compile` with `find … -exec python3 -m py_compile {} +` in `Makefile`. Still invoked only by `make verify` | Rejected: wrapping every Bash call in `required_permissions: ["all"]`; changing Cursor product sandbox policy; new `scripts/py_compile_tree.py` (Q1 chose Makefile `-exec`) |
| **D-S2** | S1 is the **third** Makefile touch in the 034–038 program (after C5, L3). Fold stub-message cleanup (`deferred to Sprint 037`) into S1. G1 does **not** edit Makefile | Avoid jurisdictional collision |
| **D-S3** | Nucleus `cursor` / `both` paths call `write_bridge_locks` before return. Document that Cursor install needs **unrestricted FS** when `.cursor` is non-writable under sandbox (`PermissionError` on `rmtree`) — code gap is missing lock write, not sandbox policy | Flip nucleus Cursor lock assertion in `tests/test_installer.sh` (today: must write **no** cursor lock — Sprint 023 C6). Keep Claude-default nucleus path without locks if `bridge_check` still keys Claude on symlinks |
| **D-S4** | Rider S is session measurement, not UPSTREAM formal open set | Do not invent F-IDs for S1–S3 |

---

## Work

One row = one atomic commit (`RA-08`) with one structural subject (`jurisdictional_lock`).
`Assignee (proposed)` — Phase 4.1 may overwrite. Under Cursor `sequential`, the parent session executes.

### Track G — derived ledger (D11)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1 | `scripts/model_ledger.py` | create | high | `implementer_agent` | ⏳ |
| G2 | `tests/test_model_ledger.py` | create | medium | `implementer_agent` | ⏳ (same commit as G1) |
| G3 | `workflows/close_workflow.md` | modify | medium | `orchestrator` | ⏳ |

G1: walk `docs/sprints/*/SPRINT_LOG.md` + sibling `task_scope.md`; join via existing parsers; write `docs/audits/MODEL_LEDGER.md`. No network.

G2: (1) sprint without `SPRINT_LOG.md` → omitted; (2) sprint id `< 031` → omitted; (3) Gate 1 with two rounds → second round counted.

G3: name `make model-ledger` (or `python3 scripts/model_ledger.py`) in the close phase that already persists derived audits, with done-criterion that the file is regenerated before seal. **RA-16.**

### Track S — Cursor agent sandbox false reds

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| S1 | `Makefile` | modify | high | `implementer_agent` | ⏳ |
| S2 | `tests/test_verify_py_compile.py` | create | medium | `implementer_agent` | ⏳ (same commit as S1) |
| S3 | `scripts/install.py` | modify | high | `implementer_agent` | ⏳ |
| S4 | `tests/test_installer.sh` | modify | medium | `implementer_agent` | ⏳ (same commit as S3) |

S1: remove `xargs` from verify py_compile; cleanup of `model-ledger` stub else-branch text once G1 exists (or leave harmless if-file guard).

S2: assert verify compile step does not invoke `xargs` / does not require `SC_ARG_MAX` (fixture or subprocess over Makefile recipe / helper).

S3: before nucleus `return 0` on `cursor`/`both`, call `write_bridge_locks(args.target)`.

S4: after nucleus `--target cursor`, assert `.bridge_cursor.lock` **exists**; reconcile comments that claim nucleus writes none (C6) with `start_workflow.md` `bridge_check`. Default Claude nucleus install may still assert no `.bridge_claude.lock` if unchanged.

**DAG:** G1+G2 before G3. S1+S2 independent of G. S3+S4 independent of G. Prefer S before or after G freely.

**Closeout (Phase 8, not Work rows):** `CHANGELOG.md` `[Unreleased]`; program-queue Status → 038; regenerate `MODEL_LEDGER.md`; `PHASE_REGISTER.md` / `graph_stats.json`.

---

## Dependencies

None.

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Model / gate ledger | script | `Makefile` `model-ledger` → `scripts/model_ledger.py`; `close_workflow.md` (G3) at close |
| Verify py_compile (sandbox-safe) | `make` / `find -exec` | `Makefile` `verify` only |
| Nucleus Cursor bridge lock | script | `scripts/install.py` ← `scripts/install.sh` ← `start_workflow.md` `bridge_check` |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `sequential` | `docs/active_state.json` `delegation_mode` |
| Work units | **7** (G1+G2, G3, S1+S2, S3+S4 — four commits if G1/G2 and S pairs share commits) | Count of Work table rows |
| Subagents dispatched | `0` under Cursor `sequential` | parent session executes |
| Prior session ratio | n/a (Cursor / no transcript) | `python3 scripts/session_cost.py --from-anchor --json` |
| Mechanical-eligible | G2, S2, S4 | map `mechanical` |

Soft (5×) / hard (15×) thresholds apply when a measurable Claude transcript exists for this tool — not this session.

---

## Tests

| Check | Fails against the current tree? |
| :--- | :--- |
| `python3 scripts/model_ledger.py` | **Yes** — script absent (G1) |
| Ledger contains rows for 032 and 033 | **Yes** — file absent (G1) |
| G2 fixtures (omit / pre-031 / two-round Gate 1) | **Yes** — no tests (G2) |
| Verify recipe uses `xargs` for py_compile | **Yes** — defect S1 |
| S2 assertion (no `xargs` / no `SC_ARG_MAX`) | **Yes** — no test yet; current recipe would fail the assertion |
| Nucleus `--target cursor` leaves `.bridge_cursor.lock` | **Yes** — early `return 0` (S3); installer test currently **requires absence** (S4 must flip) |

---

## Verification

| Command | Expected |
| :--- | :--- |
| `python3 scripts/model_ledger.py; echo $?` | `0`; writes `docs/audits/MODEL_LEDGER.md` |
| `rg -n '032\|033' docs/audits/MODEL_LEDGER.md` | both sprint ids present as data rows |
| `make model-ledger; echo $?` | `0`; no `deferred to Sprint 037` once script exists |
| `rg -n 'xargs python3 -m py_compile' Makefile; echo $?` | no match (exit `1` from rg) |
| `python3 -m pytest tests/test_model_ledger.py tests/test_verify_py_compile.py -q; echo $?` | `0` |
| `bash tests/test_installer.sh; echo $?` | `0` (includes nucleus cursor lock present) |
| `make verify; echo $?` | `0` outside sandbox; py_compile step must not fail with `sysconf(_SC_ARG_MAX)` **inside** agent sandbox after S1 |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/037-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` before Phase 5 |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `scripts/model_ledger.py` | create — join gate + task_scope → ledger |
| `tests/test_model_ledger.py` | create |
| `workflows/close_workflow.md` | G3 — invoke `make model-ledger` at close |
| `docs/audits/MODEL_LEDGER.md` | generated (never hand-edited); committed when regenerated |
| `Makefile` | S1 — sandbox-safe py_compile; stub cleanup |
| `tests/test_verify_py_compile.py` | create |
| `scripts/install.py` | S3 — nucleus cursor/both `write_bridge_locks` |
| `tests/test_installer.sh` | S4 — invert nucleus cursor lock expectation |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Status: 037 delivered → next 038 (closeout) |
| `CHANGELOG.md` | `[Unreleased]` Sprint 037 entry (Phase 8) |
| `docs/sprints/037-core-pipeline/*` | plan, scope, log, register, graph_stats |

**Measured figures** above carry reproduce commands (J6 / T5).

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Family-trial / write `cursor.author` | **038** after first usable ledger evidence + D6 |
| Cheapen `gate` via `load_proven_families()` + ledger | Post-038 / ADR-0003 cost clause |
| Cursor product sandbox policy; default `required_permissions: ["all"]` | Out of S (program queue) |
| CE-5 pytest/`git init` sandbox protocol | Deferred in 036 O5 triage; distinct from rider S |
| Rewrite closed 026–033 `SPRINT_LOG` / `task_scope` | Census documents; ledger omits |
| Fix `session_start` historical «Still open» false count | Out of scope (Q5) |
| Formal UPSTREAM F-ID intake for S1–S3 | Not census/host findings |

---

## Abort criterion

Stop and revert the offending unit (do not push partial G+S as "done") if:

1. `model_ledger.py` adds parsers instead of importing `gate_tables` / `work_tables`; or
2. After S1, py_compile under the agent sandbox still fails with `sysconf(_SC_ARG_MAX)` / `xargs` errors; or
3. S3 causes host `--target cursor` install to stop writing locks, or Claude-default nucleus install starts writing locks that break `bridge_check` without a matching `start_workflow.md` update; or
4. `make verify` regresses outside the sandbox (pytest / reference checks).

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | {{HUMAN}} |
| **Date** | {{ISO_DATE}} |
| **Plan commit at approval** | `{{COMMIT_SHA}}` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop`. Phases 6–8 only if the human arms `loop_guard.py start` first
(`rules/loop_governance.md`).*
