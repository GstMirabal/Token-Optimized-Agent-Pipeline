# 📝 Sprint Log: #044
**Session Tracker**: 20260906T113929Z-1198
**Role Active**: Principal Agent → Orchestrator

---

## 🚦 Session Metadata
| Parameter | Value |
| :--- | :--- |
| **Active Layer** | core / pipeline |
| **Strategic Goal** | `session-start-drift-cigate-host-parity` — six `nucleus`-class defects on the `/agents:start` → drift → CI-gate path (`F-BOOT-1..4` from a host session, `C5`/`C6` backfilled from the Sprint 043 close) |
| **Intelligence State** | CERTIFIED (`intelligence_certified: YES`) |
| **Start Time** | 2026-09-06T11:39:29Z |
| **Base** | `main` @ `2bbfa60ff470ae5374819b9f19b95e4f4a40fa90` |
| **Branch** | `ai-sprint/044` |

---

## 🏁 Sprint Progression

- [x] **U1** — `scripts/session_start.py`: `_bridge_permission_denied` takes `target`, matches `permissionerror` + the target's mirror marker (`.claude`/`.cursor`) — `F-BOOT-1` (`a0cf769`)
- [x] **U2** — `tests/test_session_start.py`: `_bridge_permission_denied` / `_bridge_triage` cases for a `claude`-target permission denial (`a0cf769`)
- [x] **U3** — `scripts/session_start.py`: `_run_script` runs `session_state.py` / `session_probe.py` with `cwd = agents_root().parent` in submodule mode — `F-BOOT-2` (`a2fcdbb`)
- [x] **U4** — `tests/test_session_start.py`: submodule-mode `--boot` claims the host anchor, creates no nucleus anchor; nucleus mode unchanged (`a2fcdbb`)
- [x] **U5** — `scripts/ci_gate.py`: both protection endpoints HTTP 403 → `RECORD` (exit `0`) naming the `gh pr checks` substitute — `F-BOOT-3` (`53786db`)
- [x] **U6** — `tests/test_ci_gate.py`: stubbed 403 on both endpoints → exit `0`, `RECORD` line (`53786db`)
- [x] **U7** — `scripts/detect_drift.py`: exclude commits whose diff is only `docs/active_state.json` and whose subject matches `^docs\(state\)` — `F-BOOT-4` (`502b5a9`)
- [x] **U8** — `tests/test_detect_drift.py` (new): `docs(state)`-only commit past baseline → exit `0`; mutation-verified (`502b5a9`)
- [x] **U9** — `Makefile`: `graphify-rebuild` → `venv_skillopt/bin/python -m graphify update . --force` — `C5` (`aa69f08`)
- [x] **U10** — `scripts/check_venv_relocatable.py`: drop the `str(venv) in line` disjunct — `C6` (`44e0e65`)
- [x] **U11** — `tests/test_check_venv_relocatable.py`: relative `--venv` whose resolved form is absent from `pyvenv.cfg` returns a mismatch (`44e0e65`)
- [x] **U12** — `docs/decisions/ADR-0014-ci-gate-record-on-uninspectable-protection.md` (new) (`8de8eb7`)

---

## 🚦 Quality Gate Verdicts (Phase 7)

Transcribed by `orchestrator` from the verdicts the gates emit; gates do not write
this file (`config/artifact_registry.json`). Filled at Phase 7 — an empty table
here before that phase is the correct state, not a missing row.

| Gate | Round | Verdict | Class | Notes |
| :--- | :--- | :--- | :--- | :--- |
| QA Agent (structural) | 1 | REJECTED | charter | `verify_references` / `check_task_scope` / `check_forge_ladder` / `check_template_gates` / `make verify` all exit `0`; zero new ruff findings vs `main`. Two charter findings: **C-1** `resolve_inputs` grew to 53 lines (`agents.md §1` limit 50) — the file's first breach. **C-2** `RA-14`: the approved plan said "403/404" in three places while implementation, tests and `ADR-0014` were 403-only. Remediated `daa40ed` (extract `_record_not_inspectable`, `resolve_inputs` → 47) and `2baa07c` (plan/task_scope/ADR reconciled to HTTP 403; `task_scope.md` deviation row #2 added). Not a third consecutive REJECTED — no `remediation_workflow.md`. |
| QA Agent (structural) | 2 | RECORD | testifying | Both charter findings independently verified resolved (AST: `resolve_inputs` 47 lines, no function newly over 50; plan carries zero `404` acceptance claims, `task_scope.md` deviation row present). Full regression battery green (`ruff` 0, `pytest tests/test_ci_gate.py` 58, `verify_references` 0, `check_task_scope` 0, `audit_plan` 0, `make verify` 0 / 701 + installer). One testifying residual: `skill_assignment.md:38` still read "403/404" in a unit *label* (not an acceptance criterion) — fixed this commit. `RECORD` does not bounce (`RA-17`). Proceed to Gate 2. |
| Tester Agent (functional) | 1 | RECORD | testifying | Own worktree at `2bbfa60`: 10/13 new tests red (3 are F-BOOT-4 negative controls, correctly green pre-fix); F-BOOT-2 additionally proven with a real `git submodule add` fixture (`.git` file) — pre-fix `--boot` created `.agents/docs/active_state.json` and left the host anchor absent, and because that path is gitignored the stray anchor left `git -C .agents status --porcelain` empty (invisible to `submodule_purity`). Post-fix: host anchor `IN_PROGRESS`, no nucleus anchor. Nucleus mode (real clone) byte-equivalent — abort criterion (U3) cleared, no regression. **11/11 mutations caught**, including 5 over-broad (M6/M7 caught by the pre-existing `test_neither_source_readable_is_doubt_and_never_a_pass`; M4b/M4c prove both legs of the `docs(state)` filter). `pytest tests/` 701 (base 688 + 13), `git diff main...HEAD -- tests/` removes only 3 mock-signature lines forced by the new `cwd` kwarg — nothing weakened/inverted/skipped. C5 verified by execution (new recipe exit 0 offline; old `--mode deep` exit 1 without the key). `make verify` 0, tree clean. **One testifying finding** → Sprint 045: `session_start.py:56` `load_anchor` still reads the framework anchor for the *briefing* in submodule mode (claim now writes the host's, so `/agents:start` prints "absent" over a live host anchor). Plan pre-authorised this exact routing (`task_scope.md` Out-of-scope). Plus a pre-existing note: `_mode.is_nucleus()` returns `False` inside a linked git worktree. |

Emitible set: `APPROVED` \| `REJECTED` \| `RECORD`, each with class `charter` \|
`instructing` \| `testifying` (`RA-17`, `rules/qa_and_testing.md` §4).

---

## 🧠 Rule Amendments & Heuristic Harvest
Extraction of knowledge for the **Memory Purge Protocol**.

| Friction Point | Resolution / Workaround | KI ID |
| :--- | :--- | :--- |
| The `fix(` commit hook (`rules/code_craft.md §6`) rejects a code-only `fix(` commit; `jurisdictional_lock` "one physical file per commit" and "the proving test rides in the fix commit" are reconciled by committing code + its test together (2 files, the sanctioned exception — Sprint 043 `96e3303` precedent) | Paired every `fix(` unit with its test in one commit. `build(` used for the Makefile unit (no test harness for a `make` target) | _extract_ |
| `ruff check .` has ~193 pre-existing findings repo-wide (no ruff config on disk); `make verify` does not run ruff at all | New/changed lines kept ruff-clean; pre-existing debt untouched (`detect_drift.py:75` PLW1510 in the un-edited `git()` helper; `test_session_start.py:102/126` FLY002). Consistent with Sprint 043's "repo-wide ruff is a known migration exclusion" | _extract_ |
| `agents_root()` is already `.resolve()`d, so `str(venv)` and `str(venv.resolve())` are identical for `check_venv_relocatable.py`'s shipped invoker — the `str(venv)` disjunct only ever mattered for a manual relative `--venv` | Confirmed the bare drop (plan's choice) is behaviour-neutral for the real caller; no `is_absolute()` guard needed | _extract_ |
| A gitignored anchor (`docs/active_state.json`, `.gitignore:55`) makes a submodule-mode contamination invisible to `submodule_purity` — `git -C .agents status --porcelain` stays empty over a stray `.agents/docs/active_state.json` (Gate 2 measured this at `2bbfa60`). Same blindness `agents.md §5 mandatory_topology` already documents for `docs/sprints/` | F-BOOT-2 fixes the write; the read (`load_anchor`) is Sprint 045 | _extract_ |
| `RA-14` term-drift recurred **within one sprint**: "403/404" was reconciled in `IMPLEMENTATION_PLAN.md`/`task_scope.md`/`ADR-0014` (`2baa07c`) but `skill_assignment.md:38` kept a fourth spelling until Gate 1 round 2 caught it | A cross-artifact grep of the changed term (`grep -rn "403/404" docs/sprints/044-*`) belongs in the remediation step, not just the reviewer's spot-check (`RA-14`) | _extract_ |

---

## ⚓ Documentation Entry Point Seal
Closing the session state and certifying traceability.

**Strategic Lock**: `LOCKED`
**Next Phase**: Phase 8 — Sprint Closeout (`/agents:close`). Both gates `RECORD`/`testifying`; no bounce, no `remediation_workflow.md`.

*Certified under conventional commit standard: `fix(pipeline): message #044`*
