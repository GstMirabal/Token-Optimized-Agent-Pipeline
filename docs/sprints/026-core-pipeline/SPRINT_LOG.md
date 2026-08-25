# Sprint Log — 026 (`tool-portability`)

**Branch**: `ai-sprint/026` from `main` at `b5bfb6a`
**Status**: open. Hito 1, Migration Gate, and Hito 2 Work through **A3** complete. A3 blind partition **failed** portability affirmation (`cursor_mdc_schema.md`). Closeout must **not** claim indistinguishability until the human chooses follow-up unit or declared limitation.

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
| `P7` | APPROVED (done-criteria greps + verify_references) | Cursor | Composer (sequential session) |
| `P7.1` | APPROVED (open `[ ]` findings 10→9) | Cursor | Composer (sequential session) |
| `A2` | APPROVED — commit exit 1; hook named `Dockerfile` / `API_KEY` | Cursor | Composer (sequential session) |
| `P4.2` | APPROVED — catalogue+filters; gate proposals empty | Cursor | Composer (sequential) |
| `P4.3` | APPROVED — `make cursor-tiers` | Cursor | Composer (sequential) |
| `P4.4` | APPROVED — `_comment` contains not proven history | Cursor | Composer (sequential) |

---

## Rule Amendments & Heuristic Harvest

| ID | Finding | Injection |
| :--- | :--- | :--- |
| H-026-A2 | A2 first attempt used `ENV API_KEY="…test…"` and the commit passed: `PLACEHOLDER_MARKERS` includes `"test"`, so the quoted Dockerfile form was waived. Opaque non-placeholder values are required for a real violation exercise. | Recorded here; do not “fix” the marker list for A2 — the filter is load-bearing against false positives. |

---

## Next Phase

Phases 0–6 Work complete through A3. **Human decision required** before Sprint Closeout claims portability: remediate `cursor_mdc_schema.md` fingerprint, or close declaring portability unproven with that file named (A3 / Abort §3).

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

---

## A3 — Hito 2 gate (2026-08-25)

Executed under Cursor with `delegation_mode: sequential`. Orchestrator transcribed the `qa_agent` verdict per `Design §D9`.

### Phase 2.6 — required sprint artifacts

| Artifact | Present |
| :--- | :--- |
| `IMPLEMENTATION_PLAN.md` | yes |
| `SPRINT_LOG.md` | yes |
| `agent_assignment.md` | yes |
| `skill_assignment.md` | yes |
| `task_scope.md` | yes |
| QA verdict (G1.q) | APPROVED (recorded above) |
| Tester verdict (G1.t) | APPROVED (recorded above) |

`python3 scripts/docs_freshness_check.py . 026` completed with advisory WARN only (prior sprints 024/025 missing `graph_stats.json` inside the populated range; `code_containers` undeclared). Sprint `026` snapshot written: `graph_stats.json` → **5216 nodes, 5947 edges, 567 communities**.

### Blind partition — portability verdict

Fresh `qa_agent` context received `/tmp/a3-blind-026/` (full sprint directory copy with the Hito 2 gate table's **Tool** column removed; Model column retained). Asked to bucket each of seven artifacts as Claude Code / Cursor / Mixed|cannot tell.

| Artifact | Blind bucket | Ground-truth producer (orchestrator) |
| :--- | :--- | :--- |
| `IMPLEMENTATION_PLAN.md` | Claude Code | Claude Code (Phase 1) |
| `agent_assignment.md` | Claude Code | Claude Code (Phase 4.1) |
| `skill_assignment.md` | Claude Code | Claude Code (Phase 4.2) |
| `SPRINT_LOG.md` | Mixed\|cannot tell | Mixed (correct) |
| `task_scope.md` | Mixed\|cannot tell | Mixed (correct) |
| `graph_stats.json` | Mixed\|cannot tell | Cursor (A3) — unlabeled; judge did not ID |
| `cursor_mdc_schema.md` | **Cursor** | **Cursor (P4.0)** |

**Result: the judge correctly identified a Cursor-produced artifact.** Per `IMPLEMENTATION_PLAN.md` A3 / Abort criterion §3: **portability has not been achieved** for closeout claims. The delating file is named:

- **`docs/sprints/026-core-pipeline/cursor_mdc_schema.md`**

Strongest blind signal cited: live Cursor `.mdc` key probe (`description` / `globs` / `alwaysApply`) from `.cursor/rules/`.

**Sprint disposition:** Hito 2 Work units through A3 are complete. The sprint **does not close affirming portability**. Options for the human (plan Abort §3): (1) add a follow-up unit that removes or genericizes the fingerprint, or (2) close declaring portability **unproven** / limited, with this file named as the difference.

---

*Certified under conventional commit standard for Sprint 026 gate records.*
