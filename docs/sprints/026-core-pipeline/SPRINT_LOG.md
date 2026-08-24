# Sprint Log — 026 (`tool-portability`)

**Branch**: `ai-sprint/026` from `main` at `b5bfb6a`
**Status**: open. Phases 0–3 complete. No unit of `Work` has started — `agents.md §2 triple_lock` blocks execution until Phase 5 records a human approval.

---

## Phase 0 — Anchor and drift check

- Session anchor claimed at `docs/active_state.json`. Drift verdict: `S` (stale-but-safe — `current_sprint.id` read `23` against a checked-out `ai-sprint/023` branch that no longer exists; corrected by unit `A1` in `IMPLEMENTATION_PLAN.md`, not yet executed).
- Knowledge graph rebuilt: **4963 nodes, 5598 edges**.
- Claude Code bridge verified intact: **13 of 13 symlinks**, zero dangling.

## Phase 1 — Planning

- `principal_agent` authored the Implementation Plan for Sprint `026` (`tool-portability`), covering the full appendix at `docs/roadmaps/core/pipeline/021-030-program-queue.md` lines 924–1118.
- The plan was **revised once**, on a human reordering directive. Revision 2 is the version extracted at Phase 3.

## Phase 2 — Green baseline

Measured by `devops_agent` at `main` `b5bfb6a`, before any unit of Sprint `026` exists:

| Check | Result |
| :--- | :--- |
| `make verify` | exits `0`. Single command covers **428 tests passed, 0 failed, 0 skipped**, plus `tests/test_installer.sh` |
| `python3` interpreter | `3.13.13` |
| `venv_skillopt/bin/python3` interpreter | `3.13.13` — no cross-interpreter risk |
| Docker | No Docker configuration in the nucleus; Docker strings in the tree are secret-scanning gate fixtures |

## Phase 3 — Roadmap extraction (this record)

- `IMPLEMENTATION_PLAN.md` extracted to the canonical path `docs/sprints/026-core-pipeline/IMPLEMENTATION_PLAN.md`, from revision 2 — the `HITO 1` / `PUERTA DE MIGRACIÓN` (`M1`–`M7`) / `HITO 2` structure that replaced revision 1's `Ola 0`–`Ola 5` decomposition per the human's reordering directive. Corrections applied at extraction, since revision 2 had not incorporated them either: the `install_claude.*` reference census fixed to `40` files (`32` Class A, `8` Class B — not the `31`/`26`/`5` revision 2 still carried), `Design §D6` rewritten to state its case-sensitivity probe result (`True` — case-insensitive) instead of branching on it, and the missing `P9.2` operation bullet written (four named tests, by symmetry with `P8.1`).
- `SPRINT_LOG.md` opened at this same path.
- Neither the Hito 1 gate (`H1.f`) nor the Migration Gate (`M1`–`M7`) has run — both are downstream of Phase 5 approval and no unit of `Work` has started.
- **Approval is pending.** The `Approval` table in `IMPLEMENTATION_PLAN.md` carries no signature, date, or commit SHA — Phase 5 has not run.

---

## Settled human decisions

| # | Decision | Effect on the plan |
| :--- | :--- | :--- |
| 1 | Cursor is available on a test machine for this sprint | `P4.0`'s UI-derived `.mdc` schema step is reachable; not deferred at approval |
| 2 | `scripts/install_claude.sh` is kept as a two-line deprecation shim (`Design §D3`) | `P3.1b` ships; `scripts/install_claude.py` is still removed via `git mv` |
| 3 | Symlinked nucleus content (`AGENTS.md` → `.agents/agents.md`) is declared **out** of host gate scope (`P7`) | `agents.md §3` gains the exclusion row and the mechanism name; `strict_rule` is not asked to gate what it forbids touching |
| 4 | Scope: option (a) — all eleven units execute across Hito 1 + Puerta de Migración + Hito 2, `P4.2`–`P4.4` last in Hito 2 | `Recomendación de alcance` section retires revision 1's Corte A and records options (a)/(b) with cost |
| 5 | `F-023-S4` ordering holds: `RA-03` hotfix runs after `026`, not before | `Out of scope` keeps the raised-cost paragraph; Abort criterion 2 stays armed for the full sprint |
| 6 | `Design §D4c`'s constitutional carve-out is repealed: *"it does not matter where it runs, if the sequence is correct it can be committed"* | Every Hito 2 unit (`P7`, `P7.1`, `A2`, `P4.2`, `P4.3`, `P4.4`) gates under Cursor with the same write → fresh-chat gate → commit sequence — none is reserved for Claude-Code-only gating |
| 7 | Migration Gate failure policy confirmed: if any of `M1`–`M7` fails, Hito 2 continues under Claude Code and the sprint closes declaring portability **unproven** ("no demostrada"), not aborted | Confirms the plan's Abort criterion 1's migration clause and the paragraph beneath `M1`–`M7`; no plan edit required |

---

## Gate registration — Hito 2 units (`Design §D4c`)

`Design §D4c` makes this table the evidence that a Hito 2 gate ran at all: under Cursor nothing forces the fresh chat to open before gating, so the mechanical registration below is what proves it happened, read after the fact from `state.vscdb`'s `cursor/applicationOpenModelAppliedConfig` key.

| Unit | Verdict | Tool | Model (read from disk) |
| :--- | :--- | :--- | :--- |
| `P7` | | | |
| `P7.1` | | | |
| `A2` | | | |
| `P4.2` | | | |
| `P4.3` | | | |
| `P4.4` | | | |

---

## Rule Amendments & Heuristic Harvest

*Empty — no unit has executed. `agents.md §4 zero_tolerance` applies once a friction point is found during Work.*

---

## Next Phase

Phases 4 and 5 are complete. Phase 5's human approval was recorded on 2026-08-24 over the plan text at commit `1da9641`. Phase 6 (Execution) is in progress on Hito 1.

---

## Session handoff — suspended 2026-08-24, resuming under Cursor

**This is a `suspend`, NOT the Migration Gate.** The gate has not been attempted and cannot pass yet: `scripts/cursor_adapter.py` (unit `P4`) does not exist, `.cursor/` does not exist, and `scripts/install.py --target cursor` exits `1` by design until `P4` lands. Observations `M4`, `M5` and `M6` are therefore unobservable. Do not record any gate result.

`release` was NOT used and must not be: it seals the sprint and writes a false `last_close_commit` that blinds `scripts/detect_drift.py` (`Design §D0b`).

### First actions for the resuming session

1. `python3 scripts/session_state.py claim --tool cursor` — the anchor is `SUSPENDED`, so this reports a resume and increments `session_count`. It does not need `--session-id`: unit `P8` made it optional and mints `<compact UTC ISO-8601>-<PID>` when omitted. `delegation_mode` derives to `sequential` from `--tool cursor`.
2. **Read `agents.md` in full, explicitly.** Governance is NOT auto-loaded: `.cursor/rules/00-constitution.mdc` is unit `P4`'s output and `P4` has not run. This is the single largest difference from a Claude Code session and it is a consequence of suspending before `P4`, not a defect.
3. Read `docs/sprints/026-core-pipeline/IMPLEMENTATION_PLAN.md`, then `task_scope.md` — in particular its `Declared deviations`, `Declared escalations` and `Declared deferral` sections.
4. Read `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (the nucleus substitute for `docs/0_SYSTEM_OVERVIEW.md`, which does not exist here by design).

### State at suspension

| | |
| :--- | :--- |
| Branch | `ai-sprint/026`, 13 commits, tree clean |
| HEAD | `bf53b46` |
| `make verify` | exits `0`; 432 tests pass; both installer sub-tests pass |
| Base | `main` at `b5bfb6a`, unchanged |
| Pushed | **No.** `RA-12` puts the push in `close_workflow.md` Phase 5 |

### Delivered in Phase 6 so far

`H1.a` complete — `P8`, `A1`, `P8.1`, `P2`, `P8.2`, `P2.1`. The day-one blocker is closed end to end: a session can claim the anchor without a harness UID, record `session_tool`, declare `delegation_mode`, and find the per-harness invocation written out in `workflows/start_workflow.md` without inferring it.

`H1.b` partial — `P3.0` (`install_claude.py` → `install.py`, `--target claude|cursor|both`, `diff -r` proving the `claude` target unchanged), `P3.2.1` (`hooks/on_init.py`), `P3.2.9` (`tests/test_installer.sh`), and the `install_claude.sh` exec line.

### Remaining before the Migration Gate can be attempted

In dependency order: `P3.1` (`git mv install.sh`), `P3.1b` (the two-line deprecation shim with its `stderr` notice — **only the exec target has been fixed so far, the deprecation notice is not written**), `P10` (per-target lock), `P10.1` and `P11` (`.gitignore`), `P6` (repeal `standardization_workflow.md:45` — **must precede `P4`** or the standardization protocol proposes archiving what `P4` just created), `P5`/`P5.1`/`P5.2` (`config/rule_triggers.json`, which feeds `P4`'s `globs:`), `P4.0` and `P4.0b` (measure the real `.mdc` schema — `Abort criterion §4` aborts any unit that writes a frontmatter key not read from a file Cursor produced), `P4` (the adapter), `P9`/`P9.1` (`pre-push`), `P1`/`P1.1` (the constitutional enablement; `Design §D4b` requires `P1` before any Hito 2 unit runs under Cursor).

### Correction to the record, made at suspension

The Hito 1 deferral rests on a measurement that claimed **exactly two** census files break at runtime. It was **three**: `scripts/install_claude.sh` execs the renamed script on its last line and was misclassified as a file being renamed rather than a caller. Corrected in commit `bf53b46`. The 28 deferred prose files were re-checked against this and none of them executes — but whoever resumes should treat the deferral list as measured-once, not proven.

*Certified under conventional commit standard: `docs(sprint): open Sprint 026 roadmap #026`*
