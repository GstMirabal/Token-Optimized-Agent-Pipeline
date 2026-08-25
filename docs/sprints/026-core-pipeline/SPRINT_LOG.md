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

**Historical.** That suspend was NOT the Migration Gate. Hito 1 units through `P1`/`P1.1` and Bugbot follow-ups later landed under Cursor; see sections below. The 2026-08-24 brief is preserved for audit trail only.

### Correction to the record, made at suspension (2026-08-24)

The Hito 1 deferral rests on a measurement that claimed **exactly two** census files break at runtime. It was **three**: `scripts/install_claude.sh` execs the renamed script on its last line and was misclassified as a file being renamed rather than a caller. Corrected in commit `bf53b46`. The deferred prose files were re-checked against this and none of them executes — but whoever resumes should treat the deferral list as measured-once, not proven.

---

## Phase 6 — Hito 1 completion (sessions through 2026-08-25)

Hito 1 dispatch scope (minus human-deferred `⏳→H2` rows) completed on `ai-sprint/026` at HEAD `7bf2cb4`.

| Block | Units | Notes |
| :--- | :--- | :--- |
| H1.a | `P8`, `A1`, `P8.1`, `P2`, `P8.2`, `P2.1` | Day-one Cursor claim path |
| H1.b | `P3.0`, `P3.1`, `P3.1b`, `P3.2.1`, `P3.2.9`, `P10`, `P10.1` | Installer rename + locks; prose census deferred |
| H1.c | `P9`, `P9.1` | `P9.2` / `A4*` deferred → H2 |
| H1.d | `P6`, `P11`, `P5`, `P5.1`, `P5.2`, `P4.0`, `P4.0b`, `P4` | Cursor adapter + rule triggers |
| H1.e | `P1`, `P1.1` | Constitutional pipeline table + workflow map |

Post-gate Bugbot remediations (same Hito 1 surface): nucleus MCP path rewrite, nucleus git-hook trio on `--target cursor`, `bridge_check` `--target` wiring, host `.cursor/` gitignore entries (`7bf2cb4`).

---

## H1.f — Hito 1 gate (2026-08-25)

Executed under Cursor with `delegation_mode: sequential` (native 8-role fresh context unavailable in this harness; roles applied sequentially). Orchestrator transcribed both verdicts per `Design §D9`.

### G1.q — QA verdict

**APPROVED** (qa_agent → orchestrator).

| Check | Result |
| :--- | :--- |
| `make verify` at `7bf2cb4` | exit `0` |
| Constitutional units `P1`, `P5.2` | landed (`d55b828`, `30798e3`); both named in this gate |
| `scripts/scan_workflow_determinism.py .` | OK |
| `scripts/verify_references.py` | OK (check `(e)` + invocation coverage) |
| Naming / topology | no `TODO`/`FIXME`; English artifacts; Option B sprint paths |

Residual (accepted, deferred): `A4` RA-16 hooks-scan widening and `P9.2` tests remain `⏳→H2`; they do not block Hito 1 dispatch under the recorded human deferral.

### G1.t — Tester verdict

**APPROVED** (tester_agent → orchestrator).

| Check | Result |
| :--- | :--- |
| `pytest tests/ -q` | 432 passed |
| `bash tests/test_installer.sh` | host sandbox + nucleus self-bridge PASSED |
| Session protocol (`P8.1`) | covered inside the 432 |
| Installer `--target cursor` nucleus paths | MCP rewrite + git hooks asserted in installer suite |

---

## Migration Gate — observations `M1`–`M7`

Executed 2026-08-25 under Cursor. Sequence: `suspend` → `install.py --target cursor` → `claim --tool cursor`. **`release` was not used.** Install left `git status --porcelain` empty (`.cursor/` already gitignored); no empty bridge commit.

| # | Result | Evidence |
| :--- | :--- | :--- |
| M1 | **PASS** | Status after `suspend`: `SUSPENDED`. `claim --tool cursor` printed resume (`session #13`), not collision. Status after claim: `IN_PROGRESS`. |
| M2 | **PASS** | `session_id=20260825T043831Z-94095` (form `<ISO compact>-<PID>`), `session_tool=cursor`. |
| M3 | **PASS** | `delegation_mode=sequential`. Phase 2 treats this as configuration, not `delegation_conflict` incident (this session continued without halting). |
| M4 | **PASS** | `.cursor/commands/` = 13; `.cursor/rules/` = 12; `.cursor/mcp.json` present. |
| M5 | **PASS** | Asked: *Under `agents.md §2 jurisdictional_lock`, how many physical files may a single instantiated subagent task edit structurally?* Answer: **1**. Matches `agents.md §2` (*Limit structural editing to `1` single physical file…*). Constitution loaded via `.cursor/rules/00-constitution.mdc` / workspace always-on rules. |
| M6 | **PASS** | `.git/hooks/pre-push` installed by `install.py --target cursor`. Non-FF stdin to the hook exits `1` with `Rejected non-fast-forward… Force-push and history rewrite are blocked.`; FF control exits `0`. Note: `origin` had no `ai-sprint/026` (first push would be ZERO_SHA and allowed); rejection measured on the hook path `git push --force` uses when rewriting an existing tip — same `on_push.py` gate. |
| M7 | **PASS** | `resume_pointer.at=37d7adb0c8d6093d8effc95369aa7aa4b378b740` equals `HEAD`. `session_probe.py` reports no anchor-vs-branch mismatch (advisory graph staleness only). |

**Migration Gate: PASSED.** Hito 2 may proceed under Cursor with `delegation_mode: sequential`.

### M5 verbatim answer (gate observation)

> **1**

---

*Certified under conventional commit standard for Sprint 026 gate records.*
