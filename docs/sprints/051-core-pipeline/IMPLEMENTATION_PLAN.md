# Implementation Plan: Sprint 051 — Host-reported defects and a register that stopped tracking them

**Canonical path**: `docs/sprints/051-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/051` · **Base**: `main` at `753fbe1`
**Mode**: nucleus (`.git` is a real directory — `scripts/_mode.py`)

> **Base note.** Sprint 050 is in progress and unpushed (`git ls-remote --heads origin`
> lists no `ai-sprint/050`). This sprint bases on `main` because that is the only state
> verifiable from here, and **rebases onto 050 once it lands**. The overlap is one
> finding, deliberately excluded — see Out of scope.

---

## Context

A host (`routing_class: nucleus`, genericized per `RA-15`) swept every framework-class
finding it had recorded and re-verified each against `v4.32.0` rather than against the
registers. Both registers were stale: the host's inventory measures `v4.4.0` from
2026-08-16, and `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` has not been updated since
2026-08-26.

The sweep returned 26 findings: **14 already closed** upstream and never marked as such,
**9 open and reproducible**, 3 needing a nucleus-side check. One of the nine belongs to
Sprint 050, leaving 8 here.

The register's own boot summary is the proof it stopped tracking:

```
## Open upstream findings
file lines: 1354 — do not load full UPSTREAM at start
| **Still open** | rows (non-empty): 0
```

Zero, against eight reproducible defects. A register reporting nothing open is worse than
no register: `agents.md §0` tells every nucleus session to read it before planning, so it
actively misdirects the sessions that obey.

**One defect is why this sprint exists at all.** `detect_drift.py` stopped that host's
boot on its own in-flight sprint work, and the `/start` briefing — where `agents.md §0`
delivers the Documentation Entry Point — runs *after* the drift gate. The host planned a
whole session without the anchor documents the ruleset mandates, and found the
contradictions between them only by reading them by hand.

---

## Design

### D-1 — Drift is judged against the integration branch, not against HEAD

`classify()` (`scripts/detect_drift.py:196`) evaluates `last_close_commit..HEAD`. On
`ai-sprint/[ID]`, which `RA-12` makes mandatory for all execution, every commit of the
sprint in progress is by definition absent from any release tag. Once `[Unreleased]` is
non-empty, verdict `A` (`:223-224`) fires and `--boot` exits `2`.

But `agents.md §0 Master Ledger` and `RA-05` place a sprint's ledger entry at **Sprint
Closeout**. A sprint stopped earlier is *correctly* unrecorded, so the reconciliation it
is forced into must reconstruct nothing — and `reconciliation_workflow.md` Phase 3
prohibits inventing an entry for work that has not closed.

The fix splits the range at the merge-base with the integration branch:

| Half | Rule |
| :--- | :--- |
| `baseline..merge-base(<integration>, HEAD)` | Landed work. Must be ledger-covered. Current logic unchanged, including exit `2` |
| `merge-base(<integration>, HEAD)..HEAD` | In-flight sprint work. **Listed, never blocking.** Its entry is due at close, and `close_workflow.md` already gates that |

`<integration>` resolves from the anchor, not assumed to be `main`. The in-flight half
stays enumerated so a branch that never merges does not become a blind spot — and the
failure this check was built against (`PRs #26-#30`) was unrecorded work *on the
integration branch*, which half one still catches.

Rejected: suppressing verdict `A` whenever the checked-out branch matches
`current_sprint.branch`. That keys on the anchor agreeing with reality, which is exactly
what drift detection cannot assume.

### D-2 — A submodule that ships a test suite must pin its own rootdir

This repository carries `tests/` and a `make verify` that runs it, and declares no pytest
configuration: no `pytest.ini`, no `pyproject.toml`, no `setup.cfg`, no `tox.ini`. In
nucleus mode that is invisible — rootdir discovery finds nothing above the clone and
settles here.

In **submodule** mode it escapes: pytest walks up from `tests/` into the host repository,
finds the host's `pyproject.toml`, fixes rootdir there, and collects the host's whole
tree. In the reporting host that meant `stat()` on a sandbox-denied `.env` and a
`PermissionError` before a single test ran — `make verify` unrunnable in every host whose
root carries a Python project file.

Measured there: pinning rootdir and confcutdir on the command line took the suite from
*0 collected* to **776 passed**. A `pytest.ini` makes that the default rather than
something each host rediscovers.

### D-3 — A test that names `/private/tmp` cannot run under a sandbox

`tests/test_on_push.py:33` sets `base = Path("/private/tmp")` and passes it to
`mkdtemp(dir=...)`. The docstring says "when possible", but the call raises before any
fallback runs. Four tests fail under any sandbox that does not grant that exact path,
including the default macOS Seatbelt profile Claude Code applies.

`TMPDIR` is the mechanism the platform already provides. Dropping `dir=` honours it, and
isolation is preserved because `mkdtemp` still creates a fresh directory.

### D-4 — `.get(key, default)` is not a null guard

`node_delta` (`scripts/docs_freshness_check.py:379`) computes
`current.get("communities", 0) - previous.get("communities", 0)`. When a snapshot stores
`"communities": null` the key **is present**, so `.get` returns `None` and the subtraction
raises `TypeError`. The default never applies.

Reported from a host close against a real `graph_stats.json` carrying that value. Unchanged
since it was reported, because nothing in the register said it was open.

### D-5 — Two relative paths that cannot both resolve from one `cwd`

`scripts/loop_guard.py:41-42` declares `ACTIVE_STATE = Path("docs/active_state.json")`
(repository-root relative) and `TASK_SCOPE = Path("task_scope.md")` (bare relative). In a
host whose sprint directory is nested — `docs/sprints/[ID]-[Stack]-[Layer]/task_scope.md`,
the canonical path `agents.md §5` declares — no single working directory satisfies both.

Its siblings already solved this: `check_task_scope.py` and `check_forge_ladder.py` take
`--sprint-dir` / `--current-sprint`. `loop_guard.py` was left behind, and it already reads
the anchor, so `current_sprint.path` is in hand.

The reporting host's workaround was a transient repository-root symlink created before each
call and removed after, so it never landed in a commit. That a host had to invent that is
the measure of the defect.

### D-6 — An IDE-generated branch prefix satisfies no branch rule

`RA-03` requires `hotfix/[H-ID]` and `RA-12` requires `ai-sprint/[ID]`. Editors offering
"create branch and commit" generate their own prefixes — the reporting host got
`<user>/fix-...` — and no document states such a branch satisfies neither. `RA-18`
addresses a different Cursor problem (plan mode) and does not cover this.

Stated where the branch is created, not only where it is checked: the rename must happen
**before** the first substantive commit, or the commit-message gate has already accepted a
suffix against the wrong branch.

### D-7 — An approval names exactly one sprint

`pipeline_workflow.md` Phase 5 requires explicit Human OK and forbids wrapping it in an
unattended `/loop`. It does not say the approval is **scoped to one `Sprint_ID`**. The
reporting host opened `ai-sprint/[ID+1]` and began execution while the previous sprint was
unclosed; nothing refused it, because nothing said an approval does not generalise.

### D-8 — `Path("skills")` is a bet on the caller's `cwd`

`scripts/check_readme_counts.py:78` counts `Path("skills").iterdir()`. The `Makefile`
invokes it after `cd $(AGENTS_DIR)`, so `make verify` passes and the defect stays latent —
but `close_workflow.md` Phase 2 invokes it as a mandatory step from the host root, where it
raises `FileNotFoundError` and exits `1` without counting anything. The workflow documents
it as exiting `2` on drift; in a host it has never passed. Line 48 already resolves
`Path(__file__)` for `sys.path`, so the pattern is present in the same file.

### D-9 — The register is repaired by annotation, never by deletion

`UPSTREAM_FINDINGS_FROM_HOSTS.md` gets a status per finding. **No row is removed.** The
document says so itself: *"a finding that vanishes from an inventory is indistinguishable
from one nobody read."* Each of the 14 closures names the sprint or commit that closed it,
so the next host sweep starts from a register that is true rather than re-deriving it.

---

## Work

One structural subject per unit (`agents.md §2 jurisdictional_lock`). A `fix(` commit
carries its paired test as a mandatory companion (`rules/code_craft.md §6`).

### Phase A — Blocking defects (the boot and the gate)

| # | File | Op | Done-criterion |
| :--- | :--- | :--- | :--- |
| **W-01** | `scripts/detect_drift.py` | modify | `classify()` takes the merge-base split of D-1; on a branch with commits absent from the integration branch and a non-empty `[Unreleased]`, exit is `0` and the in-flight commits are listed. Landed-but-unrecorded work still exits `2`. Companion: `tests/test_detect_drift.py` |
| **W-02** | `tests/test_detect_drift.py` | modify | Asserts both halves: a fixture repository with in-flight branch commits exits `0`; the same fixture with an unrecorded commit on the integration branch exits `2` |
| **W-03** | `pytest.ini` | create | `[pytest]` with `testpaths = tests`. `python3 -m pytest -q` from the clone root collects `tests/` with no `--rootdir` and no `--confcutdir`. Verified additionally from a parent directory containing a `pyproject.toml` |
| **W-04** | `tests/test_on_push.py` | modify | `mkdtemp()` without `dir=`; `grep -c '/private/tmp' tests/test_on_push.py` returns `0` including the module docstring; the 4 tests pass under a sandbox denying `/private/tmp` |

### Phase B — Reported defects that were never actioned

| # | File | Op | Done-criterion |
| :--- | :--- | :--- | :--- |
| **W-05** | `scripts/docs_freshness_check.py` | modify | `node_delta` coalesces `None` to `0` for all three keys, not only `communities`. Companion test asserts a snapshot pair with `"communities": null` returns an int and does not raise |
| **W-06** | `tests/test_docs_freshness.py` | modify | The null-snapshot regression above. New file if absent |
| **W-07** | `scripts/loop_guard.py` | modify | Accepts `--sprint-dir` and `--current-sprint` like its siblings; with neither, derives the sprint path from the anchor's `current_sprint.path`. Both paths resolve from the repository root in one invocation. Companion test |
| **W-08** | `tests/test_loop_guard.py` | modify | Asserts a nested sprint directory resolves without a repository-root symlink. New file if absent |
| **W-09** | `scripts/check_readme_counts.py` | modify | `Path("skills")` resolves from `Path(__file__).resolve().parent.parent`; the script exits `0` invoked from a directory that is not `AGENTS_DIR`, and `make verify` still passes |

### Phase C — Governance gaps

| # | File | Op | Done-criterion |
| :--- | :--- | :--- | :--- |
| **W-10** | `agents.md` | modify | `RA-03` and `RA-12` each state that an IDE-generated branch prefix satisfies neither, and that the rename happens before the first substantive commit. `RA-01`..`RA-18` **not** renumbered |
| **W-11** | `workflows/pipeline_workflow.md` | modify | Phase 5 states the Human OK names exactly one `Sprint_ID`, and that creating `ai-sprint/[ID+1]` or starting Execution on another sprint before `close_workflow.md` `release` is a hard abort |

### Phase D — The register

| # | File | Op | Done-criterion |
| :--- | :--- | :--- | :--- |
| **W-12** | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | Each of the 14 closed findings carries the sprint or commit that closed it; each of the 8 open ones carries `open` and this sprint; the Sprint 050 overlap carries `owned-by-050`; the 3 unverified carry `needs-check`. **Row count does not decrease.** The boot summary's "Still open" count reports a non-zero number matching the register |

### Phase E — Checks owed before close

| # | Subject | Done-criterion |
| :--- | :--- | :--- |
| **W-13** | `REVDOC-G1` | Reproduce or refute: does the graph drop unprocessable files without recording it? Record the verdict in `W-12`'s register row either way |
| **W-14** | `agents/principal_agent.md` | Reproduce or refute: the closeout `CHANGELOG` row is assigned to a profile holding no `Write`. If confirmed, one line naming `doc_orchestrator` as its author |

---

## Dependencies

| Package | Version | Why the standard library and existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | Every unit uses `pathlib`, `re`, `subprocess` and `tempfile`, all already imported across `scripts/` |

---

## Mechanisms

| Mechanism | Invoker | Declared where |
| :--- | :--- | :--- |
| `scripts/detect_drift.py` | `start_workflow.md#drift_check`, `workflows/reconciliation_workflow.md` | module docstring `invoked_by:` (existing) |
| `pytest.ini` | `Makefile` `verify`; any bare `pytest` in this repository | Configuration, not a mechanism under `RA-16` — no invoker declaration required |
| `scripts/docs_freshness_check.py` | `close_workflow.md` Phase 2 | module docstring `invoked_by:` (existing) |
| `scripts/loop_guard.py` | `rules/loop_governance.md`, `/loop` wrappers | module docstring `invoked_by:` (existing) |
| `scripts/check_readme_counts.py` | `Makefile` `verify`, `close_workflow.md` Phase 2 | module docstring `invoked_by:` (existing) |

No new mechanism is introduced, so `RA-16` coverage is unchanged. `verify_references.py`
is run at Verification to prove it.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | **14** | Count of rows in the Work tables (`W-01`..`W-14`) |
| Files modified | 10 | 4 scripts, 4 test files, `agents.md`, `pipeline_workflow.md`, `pytest.ini`, the register |
| Subagents dispatched | 0 at Phase 1 | Phase 4.1 `agent_assignment.md` records the authority |
| Prior session ratio | not yet measured — run at Phase 5 | `python3 scripts/session_cost.py --from-anchor --json` |

Phase A alone unblocks the reporting host, which is why the Abort criterion is written
against a phase boundary rather than the whole sprint.

---

## Tests

Every `fix(` commit carries its paired test in the same commit (`rules/code_craft.md §6`,
enforced by `hooks/on_commit.py audit_regression_test`). New or extended:
`test_detect_drift.py`, `test_docs_freshness.py`, `test_loop_guard.py`, plus the existing
`test_on_push.py`.

Baseline to establish before `W-01`: `python3 -m pytest tests -q` on this tree, recorded
in `SPRINT_LOG.md`. Every "suite passes" done-criterion is measured against it.

---

## Verification

| # | Command | Expected |
| :--- | :--- | :--- |
| 1 | `python3 -m pytest -q` from the clone root, **no flags** | Suite passes. This is `W-03`'s whole point |
| 2 | `python3 -m pytest -q` with the clone nested under a directory holding a `pyproject.toml` | Same result — proves rootdir no longer escapes |
| 3 | `make verify` | exit `0` |
| 4 | `detect_drift.py` on a fixture branch with in-flight commits and a non-empty `[Unreleased]` | exit `0`, in-flight commits listed |
| 5 | `detect_drift.py` on a fixture with an unrecorded commit on the integration branch | exit `2` |
| 6 | `docs_freshness_check.py` against a snapshot pair carrying `"communities": null` | No `TypeError` |
| 7 | `loop_guard.py --current-sprint` from the repository root with a nested sprint directory | Resolves both paths, no symlink |
| 8 | `python3 scripts/verify_references.py` | exit `0` |
| 9 | Boot briefing "Still open" count | Non-zero, equal to the open rows in `W-12`'s register |

---

## Out of scope

| Exclusion | Why, and where it goes |
| :--- | :--- |
| `max_lines_per_func` — its unit and its instrument | `agents.md §1 Complexity` routes it to **Sprint 050**, which is in progress. Doing it here would collide on `agents.md`, `rules/code_craft.md`, `check_function_size.py` and `Makefile`. Recorded in the register as `owned-by-050` — **not as closed** — and verified when 050 lands |
| `max_indentation` instrument and the numeric style-score | Same routing, same owner |
| `ADR-0006` / `ADR-0007` from the host sweep | Declared host deviations, not framework defects. Recorded as `not-a-defect` with that reasoning, not silently dropped |
| The reporting host's own documentation contradictions | Host jurisdiction (`§3`). This sprint fixes only why its boot could not reach them |
| Restructuring `UPSTREAM_FINDINGS_FROM_HOSTS.md` | `W-12` annotates status. Restructuring a 1354-line register is a separate act with its own risk |

---

## Abort criterion

Decided before execution, so it is not renegotiated once the work is sunk cost.

**Primary.** If `W-01`'s merge-base split cannot satisfy verification rows 4 **and** 5
together — that is, if suppressing the in-flight false positive also suppresses a real
unrecorded commit on the integration branch — **stop and ship Phase A without `W-01`**.
`W-03` and `W-04` alone restore `make verify` in every host, which is most of the unblock.
A drift detector that has stopped catching drift is worse than one that cries wolf, and
the `PRs #26-#30` precedent is exactly that failure.

**Secondary.** If the rebase onto Sprint 050 conflicts on `agents.md` in more than
`W-10`'s two rows, **stop and re-plan the rebase** rather than resolving by hand. `W-10`
touches `RA-03` and `RA-12`; anything wider means 050 changed the amendment table and the
two sprints disagree about its shape.

**Phase boundary.** Phases A, B, C, D and E are independently landable. An abort in C
keeps A and B: the reporting host's boot and gate are fixed and two long-open defects are
closed.

---

## Approval — `triple_lock` lock 1

This plan is committed before Phase 5 requests Human OK (`agents.md §2 triple_lock`,
`pipeline_workflow.md` Phase 5). The approval names exactly one `Sprint_ID` — which
`W-11` is about to make a written rule.
