# Task Scope — Sprint 044 (session-start-drift-cigate-host-parity)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Roadmap against
current `rules/`. `jurisdictional_lock` and `no_interference` are both applied by
reading this file.

Mode: **claude-code**, `delegation_mode: native`. Model/Effort from
`config/model_tiers.json` `tiers.author.claude_code` (`sonnet` / `medium`) for
every unit except **U3**, escalated to `tiers.gate.claude_code` (`opus` / `high`)
by `tier_escalation` — it is the abort-criterion unit and edits the exact code
path that claimed this session's anchor.

Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/044-core-pipeline`

---

## Work

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/session_start.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ a0cf769 |
| U2 | `tests/test_session_start.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ a0cf769 |
| U3 | `scripts/session_start.py` | modify | high | `implementer_agent` | opus | high | ✅ a2fcdbb (tier_escalation) |
| U4 | `tests/test_session_start.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ a2fcdbb |
| U5 | `scripts/ci_gate.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ 53786db |
| U6 | `tests/test_ci_gate.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ 53786db |
| U7 | `scripts/detect_drift.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ 502b5a9 |
| U8 | `tests/test_detect_drift.py` | create | low | `implementer_agent` | sonnet | medium | ✅ 502b5a9 |
| U9 | `Makefile` | modify | medium | `implementer_agent` | sonnet | medium | ✅ aa69f08 |
| U10 | `scripts/check_venv_relocatable.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ 44e0e65 |
| U11 | `tests/test_check_venv_relocatable.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ 44e0e65 |
| U12 | `docs/decisions/ADR-0014-ci-gate-record-on-uninspectable-protection.md` | create | low | `doc_orchestrator` | sonnet | medium | ✅ 8de8eb7 |

**Plan deviations (recorded for `RA-14`):**

1. U4's target moved from `tests/test_session_protocol.py` to
   `tests/test_session_start.py` — the tests U3 forces (the `_run_script`
   cwd-kwarg mock updates) and the new F-BOOT-2 boot-path cases both belong
   beside the existing Claude-boot suite, and the `fix(` hook
   (`rules/code_craft.md §6`) requires the proving test in U3's own commit. U3
   and U4 committed together (`a2fcdbb`).

2. **F-BOOT-3 fires on HTTP 403 only, not "403/404"** (Phase 7 Gate 1, QA C-2).
   The plan bullet, Design row and Documentary-impact row said "403/404"; the
   Tests table (`:137`) said "403". The both-sources-unreadable branch in
   `required_checks` is only reachable with `FORBIDDEN` on both — a `NOT_FOUND`
   is mapped to "nothing required" by `required_from_protection` /
   `required_from_rulesets` before it can arrive there. Implementation, tests,
   `ADR-0014` and `SPRINT_LOG.md` were all 403-only; the plan prose was the sole
   drift and is corrected in place with a Phase-7 note. `ADR-0014` records a
   `404` revisit trigger should GitHub change the free-plan response shape.

---

## Rule audit

| Rule | Unit(s) | Finding |
| :--- | :--- | :--- |
| `agents.md §2 jurisdictional_lock` | all | One physical file per unit. `scripts/session_start.py` appears twice (U1, U3) — permitted: one file per **commit**, U1 committed before U3 opens. No other file listed twice. PASS. |
| `agents.md §2 no_interference` | U1, U3 | Same target file — MUST NOT be dispatched concurrently. Sequenced U1 → commit → U3. Recorded here so `no_interference` catches a concurrent dispatch. |
| `agents.md §1` (Python) | U1, U3, U5, U7, U10 | `snake_case`, mandatory type hints on new/changed signatures, ≤ 50 lines/func, ≤ 3 indent levels, Google-style docstrings, no `TODO`/`FIXME`, English only, relative paths only. `_bridge_permission_denied` gains a `target` parameter → its type hint and the two call sites update together. |
| `agents.md §1` (linter) | all code units | `ruff check .` exit `0`. `python-doctor check --diff` warning-only. |
| `RA-16 INVOCATION_COVERAGE` | U5, U7, U9 | No new mechanism — every edited script keeps its existing `invoked_by:`. U9 changes the `graphify-rebuild` recipe body, not its name; `close_workflow.md` Phase 5 `graph_rebuild` still invokes `make graphify-rebuild`. `verify_references.py` check (d) must stay green. |
| `RA-17 GATE_VERDICT_CLASSES` | U5, U12 | U5 makes `ci_gate.py` emit a `RECORD`-class line for an uninspectable protection API. `RECORD` is Phase-7 vocabulary; extending it to a merge-time script is the decision U12's ADR records (`rules/documentation_standard.md §3.1` ADR trigger: a script adopting a governance vocabulary outside its origin). |
| `RA-13 SEQUENTIAL_GATES` | U5 | The `RECORD` path MUST name the manual substitute (`gh pr checks <N>` observed as a **separate** invocation before merge). The gate's guarantee is preserved by that separate observation, not voided. |
| `RA-14 PATCH_PROPAGATION` | U1, U3 | Before closing U3, `grep -n` the full `scripts/session_start.py` for `cwd`, `repo_root`, `root =` and reconcile every sub-script spawn with the submodule-mode cwd rule. Before closing U1, grep for `_bridge_permission_denied` — both call sites (`_bridge_triage`) plus the two tests. |
| `agents.md §3 jurisdiction` | U3 | `session_start.py` runs in both modes. U3 must resolve the host root via `scripts/_mode.is_nucleus()` + `scripts/_root.agents_root()` — nucleus mode behaviour (this session's) is unchanged; only submodule mode moves claim/probe to `agents_root().parent`. Regression guard in Verification. |
| `agents.md §3 nucleus_neutrality` | all | Nucleus session: no automatic structural scaffolding. Only the twelve named files (plus their in-file docstrings) are touched. PASS. |
| `agents.md §5 mandatory_topology` | all | Sprint dir `docs/sprints/044-core-pipeline/` (`[ID]-[Stack]-[Layer]`, versioned). PASS. |
| `rules/qa_and_testing.md §3.1` | U2, U4, U6, U8, U11 | Reproduce before repairing. Each test case must fail against the pre-fix tree and pass after; each is mutation-checked (revert the fix → new case reds). U8 is a new file following the `git init` in `tmp_path` pattern already in `test_detect_drift`-adjacent suites. |
| `rules/documentation_standard.md §3` | U12 | ADR-0014 from `ADR_TEMPLATE.md`, metadata block stamped, `Consequences` populated. Cross-references `ADR-0002` (drift verdict exit codes) and `RA-13`/`RA-17`. |
| `ADR-0009` | U1–U11 | `scripts/`, `tests/` and the framework-root `Makefile` are `implementer_agent`'s exclusive authorship. PASS. |
| `RA-12 BRANCH_DISCIPLINE` | all | Execution on `ai-sprint/044` (cut from `main` @ `2bbfa60` before the plan commit). No commit to `main` during Execution. |
| `RA-08 COMMIT_SQUASH` | all | Atomic local commits, one per unit, each carrying `#044`. Squash & push at `close_workflow.md` Phase 5. |

## Capability check

Every assignee holds `Write`/`Edit`: `implementer_agent` (U1–U11),
`doc_orchestrator` (U12). Each can perform its `create`/`modify` operation. No
mechanical-tier profile appears in the table, so `check_task_scope.py`'s
mechanical-high rule does not engage. Shape
`# | File | Operation | Risk | Assignee | Model | Effort | Status` — present on
the Work table.

## Out of scope (from the plan, restated for the auditor)

- `detect_drift.py` running from the host root in submodule mode (`F-BOOT-2`
  scopes the cwd fix to claim/probe only) → Sprint 045 finding if the Tester
  gate surfaces it.
- A standalone `ADR-0002` addendum edit — the `docs(state)` exclusion rationale
  rides in `detect_drift.py`'s docstring (U7) and ADR-0014 cross-references it.
  A separate `ADR-0002` edit is added only as in-phase remediation if Phase 7
  requires it.
- A `tests/test_makefile_targets.py` guard for `C5` — no such harness exists;
  `C5` is verified by the `make`/`graphify` commands in the plan's Verification
  table. Added as in-phase remediation only if the Tester gate requires it.
- Generalising `RECORD` from `ci_gate.py` to other exit-`2`-on-unreadable-input
  scripts → a rule-amendment proposal via `governance_learner` on a second
  occurrence.
