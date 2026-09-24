# Task Scope — Sprint 051 (host-reported defects and a register that stopped tracking them)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Plan against current
`rules/`. `jurisdictional_lock` and `no_interference` are both applied by reading this
file; `scripts/loop_guard.py` measures progress from it; `workflows/close_workflow.md`
Phase 2.6 demands it as phase evidence.

> **Produced after Phase 6, not before it. Recorded as a deviation, not presented as
> order.** The session executed all five phases in-session and wrote this file at
> Closeout. `pipeline_workflow.md:27` names that exact shape as its cited precedent —
> a host ran the pipeline in a single agent, Phase 4 never ran, `task_scope.md` was not
> produced, and `jurisdictional_lock` was silently disabled across ~30 edits.
>
> What limits the damage here, and what does not. **Does**: every unit below landed as
> its own commit with one structural subject, and the two `agents.md` claims (`W-10`,
> `W-17`) were sequential and never concurrent, so the invariant the file enforces held
> — by the author's discipline rather than by the file, which is the difference this
> note exists to record. **Does not**: nothing external checked it while the work ran.
> `no_interference` was vacuous because no concurrent task existed to collide with.
> The Phase 7 gates below therefore run in **fresh context**, which
> `pipeline_workflow.md:27` makes non-negotiable under both tools and which the same
> precedent proves is where defects of this class actually surface.

Mode: **claude-code** (nucleus), `delegation_mode: native`, `session_tool: claude-code`
(`docs/active_state.json`). **Model/Effort columns are required regardless of tool**:
`scripts/check_task_scope.py:38` `MODEL_FROM_SPRINT = 28` fires for any sprint numbered
≥ 28 — Sprint 51 qualifies.

Model/Effort source: `config/model_tiers.json` `tiers.author.claude_code`
(`model: sonnet`, `effort: medium`). Assignee is the profile whose charter covers the
subject (`agents.md §6`); execution was in-session, per the note above.

---

## Phase A — Blocking defects (the boot and the gate)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W-01 | `scripts/detect_drift.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ `db4dd3e` |
| W-02 | `tests/test_detect_drift.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ `db4dd3e` |
| W-03 | `pytest.ini` | create | medium | `implementer_agent` | sonnet | medium | ✅ `662fcf7` |
| W-04 | `tests/test_on_push.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ `13a1b87` |

`W-01` and `W-02` share one commit: the paired test of a `fix(` commit is a mandatory
companion, not a second structural subject (`agents.md §2 jurisdictional_lock`,
`rules/code_craft.md §6`).

## Phase A2 — Approved extension (verdict `A` on landed work)

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W-15 | `scripts/detect_drift.py` | modify | high | `implementer_agent` | sonnet | medium | ✅ `d342811` |
| W-16 | `tests/test_detect_drift.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ `d342811` |
| W-17 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ `470666a` |
| W-18 | `tests/test_installer.sh` | modify | low | `implementer_agent` | sonnet | medium | ✅ `db077a1` |

`W-15` is the **second sequential claim** on `scripts/detect_drift.py` after `W-01`, and
`W-17` the second on `agents.md` after `W-10`. Sequential is permitted and concurrent is
not (`jurisdictional_lock`, Phase 014 `T21`/`T22` precedent); both landed after their
predecessor. `W-17` precedes `W-15` in commit order because the rule must exist before
the code that reads it.

## Phase B — Reported defects that were never actioned

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W-05 | `scripts/docs_freshness_check.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ `40bdac5` |
| W-06 | `tests/test_docs_freshness_check.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ `40bdac5` |
| W-07 | `scripts/loop_guard.py` | modify | medium | `implementer_agent` | sonnet | medium | ✅ `56e7085` |
| W-08 | `tests/test_loop_guard.py` | modify | low | `implementer_agent` | sonnet | medium | ✅ `56e7085` |
| W-09 | `scripts/check_readme_counts.py` | modify | low | `implementer_agent` | sonnet | medium | ⬜ withdrawn |

`W-09` is **withdrawn, not skipped**: the defect does not exist at `v4.32.0`.
`main()` calls `os.chdir(agents_root())` before counting, verified by running the script
from `/` and from a home directory — exit `0` and correct counts from both. The sweep
that reported it read the symptom line without following the call path. Identifier
retained (`RA-14`); recorded as closed in `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`.

## Phase C — Governance gaps

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W-10 | `agents.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ `3042a80` |
| W-11 | `workflows/pipeline_workflow.md` | modify | medium | `rule_validator` | sonnet | medium | ✅ `3042a80` |

## Phase D — The register

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W-12 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | medium | `governance_learner` | sonnet | medium | ✅ `9cb1d0b` |

## Phase E — Verdicts owed before close

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| W-13 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | sonnet | medium | ✅ `9cb1d0b` |
| W-14 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `governance_learner` | sonnet | medium | ✅ `9cb1d0b` |

`W-13` and `W-14` were reproduce-or-refute checks whose only deliverable is a verdict in
the register, so all three Phase D/E units share `9cb1d0b` — one structural subject, one
commit. `W-14` is confirmed and **wider than reported**, opened as `F-051-R1` and
deliberately not patched: choosing between giving `principal_agent` `Write` and naming a
separate writer redraws a role boundary, which `§9`'s principle keeps out of a sprint
that did not plan it. `W-13` changes verdict rather than closing — the graph drop is
third-party behaviour, while the risk stays the nucleus's under `§2 graph_sovereignty`.

---

## Rule audit — findings against current `rules/`

| # | Finding | Disposition |
| :--- | :--- | :--- |
| 1 | This file was written after Phase 6 | **Deviation, recorded above rather than normalised.** The invariant held; the mechanism that should have enforced it did not run |
| 2 | `W-01`/`W-15` and `W-10`/`W-17` each claim one file twice | **Not a violation.** `jurisdictional_lock` caps *concurrent* claims, never lifetime touches; both pairs are sequential with the predecessor landed |
| 3 | Four commits stage two files | **Not a violation.** Each is a `fix(` commit with its paired test, a mandatory companion under `rules/code_craft.md §6`, enforced by `hooks/on_commit.py audit_regression_test` |
| 4 | `W-18` was added on discovery, not by the approved plan | **Recorded in the plan's Amendment 1.** `make verify` could not reach green without it; the alternative was reporting a green gate that had not run |
| 5 | `max_lines_per_func` (`#13`) is in range of this sprint's findings | **Out of scope, owned by Sprint 050.** `agents.md §1` routes it there and `CHANGELOG.md` `[4.32.0]` records `KI-049-4` as sized for 050. Recorded `owned-by-050` in the register, **not** as closed |
