# Implementation Plan: Sprint 044 — session-start-drift-cigate-host-parity

**Canonical path**: `docs/sprints/044-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/044` · **Base**: `main` at `2bbfa60`
**Status**: `DRAFT` → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

Six `routing_class: nucleus` defects in the session-start / drift / CI-gate path.
Four (`F-BOOT-1..4`) were reported from a Claude Code host session (`.agents`
pinned v4.25.0→v4.26.0) during `/agents:start` → `/agents:reconcile`; host-
identifying strings genericized per `RA-15` (`<host-root>` = the real host
checkout). Two (`C5`, `C6`) were left `_extract_` at the Sprint 043 close and
backfilled into `memory_index.json` on 2026-09-06 as `nucleus`-class, their
upstream draft being this plan (`extract_workflow.md` `routing_gate`).

What is true when the sprint is done:

- A submodule-mode `--boot` denied write access to `<host-root>/.claude/settings.json`
  exits `0` with the PermissionError advisory, not `2`
  (`F-BOOT-1`).
- A submodule-mode `--boot` writes the session claim to `<host-root>/docs/active_state.json`
  and does not create `.agents/docs/active_state.json` (`F-BOOT-2`).
- `ci_gate.py` against a repository whose protection and rulesets endpoints both
  return HTTP 403 exits `0` with a `RECORD`-class line, not `2` (`F-BOOT-3`).
  *(Corrected from "403/404" at Phase 7 Gate 1, QA finding C-2: the both-sources
  branch is only reachable via `FORBIDDEN`; a `NOT_FOUND` on either endpoint is
  already handled as "nothing required". See the `task_scope.md` deviation row
  and `ADR-0014`.)*
- On a repository whose only commits since `last_close_commit` touch just
  `docs/active_state.json`, `detect_drift.py` exits `0` (`F-BOOT-4`).
- `make -f .agents/Makefile graphify-rebuild` with `GEMINI_API_KEY` unset
  completes without an API-key error (`C5`).
- `check_venv_relocatable.py`'s `command`-line match no longer accepts a raw
  relative `--venv` argument as a location reference (`C6`).

**Measured baseline** (reproduce): `.agents/venv_skillopt/bin/python -m pytest tests/ -q`
→ `688 passed` (Sprint 043 `PHASE_REGISTER.md:42`); `python3 scripts/session_start.py --boot --tool claude-code`
→ exit `0` in nucleus mode (this session's `/agents:start`).

---

## Design

| Decision | Chosen | Over | Why |
| :--- | :--- | :--- | :--- |
| `F-BOOT-1` scope of the predicate | Widen `_bridge_permission_denied` to take the `target` and match `permissionerror` together with that target's own mirror marker (`.cursor` for `cursor`, `.claude` for `claude`) or the rendered `permission denied on <mirror>` line | A blanket `"permissionerror" in lowered` with no marker | A markerless match would swallow an unrelated `PermissionError` from a different failure and report a bridge advisory for it. Sprint 041 generalised `_commands_body_stale` to every target and left this predicate Cursor-only; this closes the same gap in the same shape. |
| `F-BOOT-2` where anchor-writing sub-scripts run | In `_run_script`, run `session_state.py` and `session_probe.py` with `cwd = agents_root().parent` when `is_nucleus()` is `False`; unchanged (`cwd = root`) in nucleus mode | Capturing `Path.cwd()` at process entry | `agents_root().parent` is deterministic and does not depend on where the operator invoked the command from. `session_state.py:51` resolves `Path("docs/active_state.json")` against cwd (it is host-scoped, like `detect_drift.py`), so forcing `cwd = agents_root()` made it claim the nucleus anchor inside a host. |
| `F-BOOT-2` `detect_drift.py` / `sync_agents_pin.py` cwd | Left at the framework checkout for this sprint | Moving them too | The reported finding scopes the cwd fix to the claim/probe pair. Whether `detect_drift.py` should also run from the host root in submodule mode is a separate question — recorded in **Out of scope**. |
| `F-BOOT-3` verdict for an unreadable protection API | Classify an HTTP 403 (`FORBIDDEN`) on **both** the protection and rulesets endpoints as `protection-not-inspectable-on-plan` and emit a `RECORD`-class result (exit `0`) that names the manual substitute: an observed `gh pr checks <N>` all-green step run as a separate invocation before merge (`RA-13` preserved) | Passing silently; keeping exit `2` | Exit `2` makes the `RA-13` CI gate inoperable for every private repo on the GitHub free plan. A silent pass removes the gate. `RECORD` (`RA-17`) is the existing vocabulary for "observed, not a pass, not a block". The half-readable case (`_from_one_source`) is untouched — this only covers **both** sources returning HTTP 403. A `NOT_FOUND` never reaches this branch: `required_from_protection` / `required_from_rulesets` map it to "nothing required" upstream. |
| `F-BOOT-3` documentation of the new verdict path | New ADR under `docs/decisions/` recording that `ci_gate.py` (a script, not a Phase 7 gate) emits a `RECORD` result and why | Inlining the rationale in the docstring only | `rules/documentation_standard.md §3.1` triggers an ADR when a script adopts a governance vocabulary (`RA-17` classes) outside its original locus. |
| `F-BOOT-4` how routine state commits leave the drift range | In `detect_drift.py`, exclude a commit from the range when its diff touches only `docs/active_state.json` **and** its subject matches `^docs\(state\)` | Advancing `last_close_commit` to the trailing state commit | Advancing the baseline is a write to the anchor from a read-only check. A diff-and-subject filter keeps `detect_drift.py` non-mutating and matches the `ADR-0002` principle that the verdict follows the action required. Both conditions are required so a substantive commit mis-subjected `docs(state)` is still counted. |
| `C5` how `graphify-rebuild` avoids the API-key failure | Change the recipe to `$(AGENTS_DIR)/venv_skillopt/bin/python -m graphify update . --force` | Passing `--mode deep` conditionally on `GEMINI_API_KEY` | `close_workflow.md` Phase 5 `graph_rebuild` and this sprint's own closeout run offline. `-m graphify update . --force` is the invocation Sprint 043 already used by hand for the same reason (`SPRINT_LOG.md:36`). Deep semantic rebuild stays available as `graphify-update`'s manual escalation, documented in the recipe comment. |
| `C6` the lax disjunct | Drop `str(venv) in line`; keep only `str(expected) in line` where `expected = venv.resolve()` | Guarding with `if venv.is_absolute()` | The real invoker (`start_workflow.md:25`) passes an absolute default, so `str(venv.resolve())` already covers it; the raw disjunct only ever added reach for a relative arg the shipped path never sends. Removing it is the narrower change. The whitespace/symlink handling from Sprint 043 (`96e3303`) is not touched. |

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) touching **one physical
file** as its structural subject (`agents.md §2 jurisdictional_lock`).

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/session_start.py` | modify | medium | `implementer_agent` | ⏳ |
| U2 | `tests/test_session_start.py` | modify | low | `implementer_agent` | ⏳ |
| U3 | `scripts/session_start.py` | modify | high | `implementer_agent` | ⏳ |
| U4 | `tests/test_session_protocol.py` | modify | medium | `implementer_agent` | ⏳ |
| U5 | `scripts/ci_gate.py` | modify | medium | `implementer_agent` | ⏳ |
| U6 | `tests/test_ci_gate.py` | modify | low | `implementer_agent` | ⏳ |
| U7 | `scripts/detect_drift.py` | modify | medium | `implementer_agent` | ⏳ |
| U8 | `tests/test_detect_drift.py` | create | low | `implementer_agent` | ⏳ |
| U9 | `Makefile` | modify | medium | `implementer_agent` | ⏳ |
| U10 | `scripts/check_venv_relocatable.py` | modify | low | `implementer_agent` | ⏳ |
| U11 | `tests/test_check_venv_relocatable.py` | modify | low | `implementer_agent` | ⏳ |
| U12 | `docs/decisions/ADR-0014-ci-gate-record-on-uninspectable-protection.md` | create | low | `doc_orchestrator` | ⏳ |

`U1` and `U3` share `scripts/session_start.py`: sequential, `U1` lands before
`U3` opens, two commits, one physical file each (`jurisdictional_lock` holds —
the constraint is one file per commit, not one commit per file). `U3` is `high`
because the cwd change is on the path that claimed this very session's anchor;
its abort criterion is called out below.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | Every unit edits an existing script, its test, the `Makefile`, or an ADR. No import added. |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| None added | — | All six fixes repair scripts already invoked: `session_start.py` (`start_workflow.md#read_graph` / `#pip_setup`, `commands/start.md`), `ci_gate.py` (`deployment_workflow.md` Phase 1 `test_audit`, `RA-13`), `detect_drift.py` (`start_workflow.md#drift_check`, `session_start.py#run_boot`), `Makefile graphify-rebuild` (`close_workflow.md` Phase 5 `graph_rebuild`), `check_venv_relocatable.py` (`start_workflow.md#pip_setup`). No new cadence. |

`RA-16 INVOCATION_COVERAGE`: no workflow, script, executable skill, hook or gate
merges without a declared, verifiable invoker, or a typed exception in
`config/invocation_exceptions.json` stating why it has none.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 12 | Count of rows in the Work table |
| Subagents dispatched | ~16 projected (12 execution + QA + Tester + agent/skill/rule assignment) | tallied at close from `SPRINT_LOG.md` |
| Prior session ratio | 4.3–5.2 (this session, planning + extract) | `python3 scripts/session_cost.py --from-anchor --json` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues — they are not observational-only once a measurable Claude
transcript exists for this tool.

---

## Tests

**Reproduce before repairing.** A test that passes against the current tree proves
nothing about a defect claimed to exist in it.

| Check | Fails against the current tree? |
| :--- | :--- |
| `_bridge_permission_denied("PermissionError: [Errno 13] ... '<root>/.claude/settings.json'")` returns `True` | **Yes** — this is `F-BOOT-1`; returns `False` today (predicate is `.cursor`-only) |
| `_bridge_triage` returns `(0, [note])` for a `claude`-target permission denial | **Yes** — `F-BOOT-1`; returns `(2, [])` today |
| Submodule-mode `--boot` writes `status: IN_PROGRESS` to the host anchor and creates no nucleus anchor | **Yes** — this is `F-BOOT-2` |
| `ci_gate.py` with both protection endpoints stubbed to HTTP 403 exits `0` with a `RECORD` line | **Yes** — this is `F-BOOT-3`; exits `2` today (`resolve_inputs` line 568) |
| `detect_drift.py` on a fixture repo with one `docs(state)`-only commit past `last_close_commit` and empty `[Unreleased]` exits `0` | **Yes** — this is `F-BOOT-4`; exits `2` (verdict `U`) today |
| `make graphify-rebuild` with `GEMINI_API_KEY` unset exits `0` | **Yes** — this is `C5`; `--mode deep` demands the key today |
| `_command_line_mismatch` with a relative `--venv` whose resolved form is absent from `pyvenv.cfg` returns a mismatch string | **Yes** — this is `C6`; returns `None` today via the `str(venv)` disjunct |
| `.agents/venv_skillopt/bin/python -m pytest tests/ -q` → `688 passed` unchanged for every test not listed above | **No** — regression guard; baseline is `688` |
| `make verify` → exit `0` | **No** — regression guard |

Mutation checks (`rules/qa_and_testing.md`): reverting each predicate/filter
widening must re-red its new case; U8's new file is mutation-checked by removing
the exclusion.

---

## Verification

| Command | Expected |
| :--- | :--- |
| `.agents/venv_skillopt/bin/python -m pytest tests/ -q` | `≥ 688 + <new cases> passed`, `0 failed` |
| `python3 scripts/session_start.py --boot --tool claude-code` (nucleus, this repo) | exit `0`, briefing prints, nucleus anchor still claimed — `F-BOOT-2` did not regress nucleus mode |
| `venv_skillopt/bin/ruff check` on each changed `.py` | no **new** finding vs the `main` version of that file (repo-wide `ruff check .` carries ~193 pre-existing findings — a known migration exclusion since Sprint 043; `make verify` does not run ruff) |
| `.agents/venv_skillopt/bin/python -m graphify update . --force` (post-`C5`, `GEMINI_API_KEY` unset) | exit `0` |
| `make -f .agents/Makefile graphify-rebuild` (`GEMINI_API_KEY` unset) | exit `0` |
| `make verify` | exit `0` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/044-core-pipeline/IMPLEMENTATION_PLAN.md` | exit `0` |

Read exit codes with `$?` directly; never through a pipe.

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `scripts/session_start.py` (module docstring + `_bridge_triage` docstring) | State that outcome (c) — PermissionError advisory, exit `0` — is reachable for the `claude` mirror, not Cursor alone; note that claim/probe sub-scripts run from the host root in submodule mode |
| `scripts/ci_gate.py` (module docstring) | Add the both-sources-403 → `RECORD` path and the manual `gh pr checks` substitute it names |
| `scripts/detect_drift.py` (module docstring) | Add the `docs(state)`-only exclusion to the "A non-empty range is not drift by itself" paragraph |
| `docs/decisions/ADR-0014-ci-gate-record-on-uninspectable-protection.md` | New — records the `RECORD`-class verdict for an uninspectable protection API, its `RA-13` / `RA-17` basis, and `Consequences` |
| `docs/decisions/ADR-0002-drift-verdict-exit-codes.md` | Addendum paragraph: routine `docs(state)` commits are outside the drift range by construction |
| `Makefile` (`graphify-rebuild` recipe + comment) | New recipe line and a comment explaining the offline constraint and where deep semantic rebuild still lives |
| `docs/sprints/044-core-pipeline/SPRINT_LOG.md`, `PHASE_REGISTER.md`, `agent_assignment.md`, `skill_assignment.md`, `task_scope.md` | Created by Phases 3–4 |
| `CHANGELOG.md` `[Unreleased]` | Sprint 044 entry at closeout |
| `memory_index.json` | Already updated 2026-09-06 (extract backfill); no further change this sprint unless Phase 7 surfaces a new KI |

**Measured figures.** Every number in Context / Design / Verification carries the
command that reproduces it (`688 passed` → `pytest tests/ -q`; exit `0` nucleus
boot → the `/agents:start` run that opened this session).

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| Moving `detect_drift.py` to run from the host root in submodule mode | `detect_drift.py` is host-scoped and arguably should, but the `F-BOOT-2` report scopes the cwd fix to claim/probe. If the Tester gate finds submodule-mode drift detection points at the wrong repo, it becomes a Sprint 045 finding recorded in `PHASE_REGISTER.md`. |
| Generalising `RECORD` from `ci_gate.py` to other scripts that exit `2` on unreadable inputs | One instance does not establish the pattern; ADR-0014 records the single case. A second occurrence triggers a rule-amendment proposal via `governance_learner`. |
| A Makefile-target unit test for `C5` | No `tests/test_makefile_*.py` harness exists. `C5` is verified by the two `make`/`graphify` commands in the Verification table. If the Tester gate requires a guard test, it is added as an in-phase remediation commit against a new `tests/test_makefile_targets.py`. |
| Deep semantic graph rebuild (`--mode deep`) as the default | Requires `GEMINI_API_KEY`; kept as a documented manual escalation, not a `make` default. |

---

## Abort criterion

The sprint reverts to `main` at `2bbfa60` if **either**:

- `U3` (the `F-BOOT-2` cwd change) cannot be made to pass its submodule-mode
  reproduction test without regressing a currently-green test in
  `tests/test_session_start.py` or `tests/test_session_protocol.py` (baseline
  `688`), and the regression cannot be resolved without reintroducing the
  nucleus-anchor claim from the wrong directory; **or**
- three or more of the six defects (`F-BOOT-1..4`, `C5`, `C6`) hit the same
  wall — a reproduction test that cannot be satisfied without breaking an
  existing green test.

A single non-`U3` unit that hits the wall is reverted and re-scoped to Sprint
045 on its own; the sprint continues with the rest.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal |
| **Date** | 2026-09-06 |
| **Plan commit at approval** | `9ae69aa` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

**Status**: `APPROVED` (2026-09-06). Fresh-context Phase 7 gates authorized as a
standing preference, not per sprint.

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*

> **Do not delete the sentence above.** `audit_plan.py` Filter 6 rejects any plan
> that names `/loop` without also naming `loop_guard.py`, and this footer names
> both. Until Sprint 041 it named only `/loop`, so **every plan written faithfully
> from this template was rejected by the mandatory Phase 1 gate** — the template
> failed the check that consumes it, and the only passing plans were the ones that
> had dropped this footer. Replace `{{…}}` placeholders; leave this pairing intact.
