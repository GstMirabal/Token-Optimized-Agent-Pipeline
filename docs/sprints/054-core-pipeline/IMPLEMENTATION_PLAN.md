# Implementation Plan: Sprint 054 — host-intake-gates-and-sprint-state

**Canonical path**: `docs/sprints/054-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/054` · **Base**: `main` at `d848302` (`v4.36.0` sealed)
**Status**: `DRAFT`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

On 2026-10-04 a host session handed this nucleus every framework-class finding the
host had pending (`agents.md §4 feedback_upstream`). The host checked each id against
`v4.35.0`. This plan re-measured each id against `v4.36.0` (`d848302`):
`git grep -l <id>` over the nucleus tree returns no file for any of `F-115-N1`,
`F-115-N2`, `F-115-N3`, `F-114-N1`..`N8` or `F-103-N1`. None of them is
recorded in the nucleus.

The human approved the scope on 2026-10-04: blocks **A** (gates that pass without
measuring), **B** (session and sprint state) and **C** (supply chain). Block **D**
(sandbox) goes to Sprint 055 and block **E** (the nucleus's own residue) goes to
Sprint 056. Both are routed in the Work and Out of scope sections below.

Every defect in scope was reproduced at `d848302` before this plan was written:

| Finding | Observed at base | Command |
| :--- | :--- | :--- |
| `F-114-N5` | `[OK] quality_audit: 0 unit(s) scanned`, exit `0`, for a nonexistent path, for an empty directory, and for a directory whose path contains `node_modules` | `venv_skillopt/bin/python scripts/quality_audit.py does/not/exist; echo $?` |
| `F-114-N2` | `Refusing open-sprint: sprint 7 is not sealed (current_sprint.status='DEPLOYED')`, exit `2` | scratch anchor `{"current_sprint":{"id":7,"status":"DEPLOYED",...}}`, then `python3 scripts/session_state.py open-sprint --id 8` |
| `F-114-N3` | After `open-sprint --id 8` the anchor reads `{'id': 8, 'status': 'OPEN', 'name': 'old-name', 'path': 'docs/sprints/007-core-pipeline'}`: name and path still point at sprint 7 | the same scratch anchor, previous status `CLOSED_SUCCESSFULLY` |
| `F-114-N1` | `audit_regression_test('fix(x): y #054', ['scripts/a.py','tests/test_a.py'])` returns `None` (pass) with no evidence that the test ever failed | `venv_skillopt/bin/python -c "from hooks.on_commit import audit_regression_test as a; print(a(...))"` |
| `F-114-N7` / `KI-053-4` | A plan whose Verification row is `` `rg "a\|b" x` `` → `no output` passes `audit_plan.py`, exit `0` | `python3 skills/token-saver-auditor/scripts/audit_plan.py <scratch plan>; echo $?` |
| `F-114-N8` | `NOTICE` appears in `workflows/close_workflow.md:22` and nowhere in `scripts/` or `docs/standards/templates/` | `git grep -n NOTICE -- scripts docs/standards workflows` |
| `F-115-N3` / `F-114-N4` | `commands/start.md:5` gives the path `python3 scripts/session_start.py`. In a host that file is at `.agents/scripts/session_start.py`. The same host-blind path is in `scripts/session_state.py:214` (`retry_hint`) and `workflows/start_workflow.md:13` | `git grep -n "python3 scripts/session_start.py"` |
| `KI-053-1` | `pip_setup` reinstalls only when `installed.lock` is **missing** (`workflows/start_workflow.md:25`), and no script writes or checks the lock | `git grep -n installed.lock -- scripts Makefile` → only a docstring in `check_venv_relocatable.py` |
| `F-115-N1` | With **pnpm 11.23.0**, setting `minimum-release-age=1440` and `ignore-scripts=true` in `.npmrc` gives `pnpm config get minimumReleaseAge` → `undefined` and `ignore-scripts` → `undefined`. Moving them to `pnpm-workspace.yaml` (`minimumReleaseAge: 1440`, `ignoreScripts: true`, `onlyBuiltDependencies: [...]`) gives `1440`, `true` and the list. `agents.md §8` names `.npmrc`, so a host that follows it has the 24 h floor **off** | scratch directory with `package.json`, then `pnpm config get <key>` |
| `F-103-N1` | **Not reproduced: already closed.** `scripts/session_start.py:61` `anchor_root()` returns the host root in submodule mode (`F-BOOT-2`, Sprint 044). The host's session #33 boot wrote the host anchor | `sed -n 56,81p scripts/session_start.py` |

Done means: every row above has a test or command that now gives the opposite
result; the intake is recorded in `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` with
`RA-15` genericization; blocks D and E are routed with an owner and a target sprint.

---

## Design

| # | Decision | Chosen over | Why |
| :--- | :--- | :--- | :--- |
| D1 | `quality_audit.py` exits `2` when the scan finds `0` files, and when any given path is neither a file nor a directory. `DEFAULT_EXCLUDE_DIRS` applies only to path components **below** each given root. The `[OK]` line prints the file count | Resolving relative paths against the repository root | The tool has no repository-root concept, and resolving silently would hide the operator's mistake rather than report it (`F-114-N5` restriction). `--report` is not exempt: it printed `0/0` as if the register were clean |
| D2 | **Watch-it-fail is enforced in two places.** At commit time, `audit_regression_test` requires one `Repro: <test id> — fails at <sha>` trailer, or `Repro: manual — <SPRINT_LOG section>`, on every `fix(` commit that stages source. At the gate, a new `scripts/check_fix_reproduces.py --range <base>..HEAD` replays each `fix(` commit: its staged test files must exit **exactly `1`** on the parent tree and `0` at the commit | A per-commit replay hook | A replay runs the suite twice per commit, which is too slow for a hook. The trailer is only a claim; the replay is what observes it (`F-114-N1` restriction) |
| D3 | The replay runs **pytest only** in Sprint 054. A staged test file with no runner (`.ts`, `.js`, ...) is reported as `UNREPLAYED` and exits `2`, unless the commit carries `Repro: manual` | Exit `0` with a warning for unsupported suffixes | A warning would be silent compliance, the class this sprint removes. A host's JS/TS runner is routed out as `KI-054-1` (Out of scope) |
| D4 | The replay applies the host's measured design lessons: exit exactly `1` on the parent; `PYTHONDONTWRITEBYTECODE=1`; `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` and framework-settings variables stripped from child processes; the parent SHA derived and never validated against the trailer; a temporary worktree removed in `finally`, then `git worktree prune` | Discovering them again | Each lesson came from a replay that failed, or passed wrongly, in a host |
| D5 | `remediation-regression` is a **label** inside a `charter` row (`rules/qa_and_testing.md §4`). At the second label in one sprint, that logic block stops and is re-planned with the human | A new verdict or class | `RA-17` stays as written (`F-114-N1` restriction) |
| D6 | **Plan checks are measured before approval.** The template's Tests table gains `Observed at base`: the command and its exit code, or `unverified`. Verification gains `Dry run` and `Positive control`. Phase 5 refuses a plan whose read-only rows have no dry-run result. `audit_plan.py` flags, mechanically: an escaped `\|` inside a backticked command; a `no output` / `0` expectation with an empty control cell; and a Tests `Yes` row with an empty `Observed at base` cell | Pure prose in the workflow | The prose route is what `KI-053-4` already shows failing. The syntax-level recurrences can be checked by a script, so they are not left to judgment (Filter 5) |
| D7 | `audit_plan.py` reads the new columns **only when the plan's header carries them**. Plans sealed before Sprint 054 keep passing | Retroactive enforcement | Plans that are already sealed cannot be amended; the same no-retroactivity pattern as the Cost section (`Sprint 030`) |
| D8 | `NOTICE.md` is **conditional**: `close_workflow.md` `repo_docs_check` records `not applicable` when the host vendors no third-party content. A new `NOTICE_TEMPLATE.md` exists, and the `standardization_workflow.md` census names it when vendored content is found | Adding `NOTICE.md` unconditionally to `session_probe.py`'s tuple | An unconditional probe would report a defect in every host that has nothing to disclose. Attribution text is a legal statement, so it is never generated (`F-114-N8` restriction) |
| D9 | `SEALED_STATUSES` gains `DEPLOYED`. The nucleus does not write it; hosts do, after a merge and tag | Refusing an unknown status | `DEPLOYED` comes later in the lifecycle than `CLOSED_SUCCESSFULLY`. Refusing it reverses the guard's purpose, which is to stop a sprint opening over an *unfinished* one. The sealed check itself stays |
| D10 | `open-sprint` gains `--layer`, `--app` and `--name`. It **always** writes `path = docs/sprints/{id:03d}-{layer}-{app}` (the same formula as `check_role_artifact.py:297` and `persist_session_context.py:38`) and `branch = ai-sprint/{id:03d}`. It **drops** a stale `name` when `--name` is absent. `layer`/`app` default to the anchor's current values | Writing `path` from the cwd; or making `loop_guard.py` explain the missing key (`F-114-N3` proposal c) | The `F-114-N3` restriction forbids a cwd-derived path. With the writer fixed, a better error message in the reader is no longer needed |
| D11 | The start command is written in both forms: `python3 .agents/scripts/session_start.py` from a host root, `python3 scripts/session_start.py` in the nucleus. `retry_hint` chooses the form with `_mode.is_nucleus()` | A Makefile target | A host-root `make` runs the **host's** Makefile, so the indirection would move the same defect rather than remove it |
| D12 | `scripts/install_lock.py` hashes the requirement set (`requirements-core.txt` plus every `-r` include, recursively) with SHA-256. `write` stores the hash in `installed.lock`; `check` exits `2` when the lock is absent or its hash differs. `pip_setup` runs `check`; `session_start.py --boot` reports it as an advisory | Testing that the lock is present | A presence test cannot see that the requirement set changed, which is exactly `KI-053-1` |
| D13 | `agents.md §8` names `pnpm-workspace.yaml` (`minimumReleaseAge: 1440`, `ignoreScripts: true`, `onlyBuiltDependencies`) and the check `pnpm config get <key>`. `RA-10` stays a pointer | Keeping `.npmrc` | Measured above: `.npmrc` is ignored by pnpm 11.23.0, so the control is not in effect |

---

## Work

One row per unit. One unit is one atomic commit (`RA-08`) with **one physical file as
its structural subject** (`agents.md §2 jurisdictional_lock`). A `fix(` row names its
paired test in the same row (`rules/code_craft.md §6`). Several units take the same
subject in sequence, never at the same time (`no_interference`).

### Wave 0 — intake records (first, so the findings outlive this session)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| W01 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — new section *Reported by a host — Sprint 054 intake (measured against `v4.36.0`)*: one `### - [ ]` entry each for `F-115-N1`, `F-115-N2` (S-1..S-8, absorbs `F-114-N6`, routed to 055), `F-115-N3` (`F-114-N4` is the same defect), `F-114-N1`, `F-114-N2`, `F-114-N3`, `F-114-N5`, `F-114-N7`, `F-114-N8`; `F-103-N1` recorded as closed (re-measured, `F-BOOT-2`); a status block. Every host string genericized (`RA-15`) | low | `doc_orchestrator` | ⏳ |
| W02 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — new section *Routed out of Sprint 054*: block D → Sprint 055 (`F-115-N2` S-1..S-8, `F-114-N6`); block E → Sprint 056 (`KI-053-2`, `KI-052-1`, `KI-052-3`, `KI-052-4`, `KI-052-7`); `KI-053-1` and `KI-053-4` marked as taken by Sprint 054 | low | `doc_orchestrator` | ⏳ |

### Wave A — gates that pass without measuring

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A01 | `scripts/quality_audit.py` | `fix(` — D1. Paired test: `tests/test_quality_audit.py` (nonexistent path → `2`; empty directory → `2`; root under `node_modules/` scans its files; `--report` on `0` files → `2`) | medium | `implementer_agent` | ⏳ |
| A02 | `hooks/on_commit.py` | `feat(` — D2 commit half: `audit_regression_test` requires a `Repro:` trailer. Paired test: `tests/test_on_commit.py` (missing trailer → refusal message naming the form; `Repro: manual — <section>` accepted; non-`fix(` unaffected) | medium | `implementer_agent` | ⏳ |
| A03 | `scripts/check_fix_reproduces.py` | create — D2 gate half, D3, D4; `invoked_by:` `agents/qa_agent.md`. Paired test: `tests/test_check_fix_reproduces.py` (a fixture repository built in `tmp_path`: a real red→green pair → `0`; a test that passes on the parent → `2`; a collection error on the parent (exit `2`/`4`/`5`) → `2`; a `.ts` test → `UNREPLAYED`, `2`; `Repro: manual` → skipped, `0`; worktree removed after an exception) | high | `implementer_agent` | ⏳ |
| A04 | `agents/qa_agent.md` | modify — Gate 1's first check is `python3 scripts/check_fix_reproduces.py --range <base>..HEAD`; its exit code is reported in the verdict register | low | `agent_orchestrator` | ⏳ |
| A05 | `rules/qa_and_testing.md` | modify — §4: the `remediation-regression` label and the second-label stop (D5); a Tests/Verification row whose expectation contradicts the plan's own deliverable is an `instructing` finding at Phase 4 (`F-114-N7` c) | medium | `rule_validator` | ⏳ |
| A06 | `rules/code_craft.md` | modify — §6 names what enforces "watch it fail": the `Repro:` trailer (commit) and `check_fix_reproduces.py` (Gate 1) | low | `rule_validator` | ⏳ |
| A07 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify — D6 columns: Tests `Observed at base`; Verification `Dry run` and `Positive control`; the dry-run rule stated above the tables | low | `doc_orchestrator` | ⏳ |
| A08 | `skills/token-saver-auditor/scripts/audit_plan.py` | `feat(` — D6 mechanical checks, D7 header-gated. Paired test: `tests/test_token_saver_auditor.py` (escaped `\|` in a backticked Verification cell → `2`; `no output` with empty control → `2`; Tests `Yes` with empty `Observed at base` → `2`; a plan without the new columns → unchanged; the A07 template itself → `0` once placeholders are filled) | medium | `skill_architect` | ⏳ |
| A09 | `workflows/pipeline_workflow.md` | modify — Phase 5: dry run of every read-only Tests/Verification row before the Human OK; Phase 7: Gate 1 runs `check_fix_reproduces.py` first | medium | `orchestrator` | ⏳ |
| A10 | `docs/standards/templates/NOTICE_TEMPLATE.md` | create — D8; the nucleus's own `NOTICE.md` as the worked example | low | `doc_orchestrator` | ⏳ |
| A11 | `workflows/close_workflow.md` | modify — `repo_docs_check`: `NOTICE.md` is required only when the host vendors third-party content; otherwise record `not applicable`; names `NOTICE_TEMPLATE.md` | low | `orchestrator` | ⏳ |
| A12 | `workflows/standardization_workflow.md` | modify — the legacy census names `NOTICE_TEMPLATE.md` when it finds vendored content | low | `orchestrator` | ⏳ |

### Wave B — session and sprint state

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B01 | `scripts/session_state.py` | `fix(` — D9: `SEALED_STATUSES` gains `DEPLOYED`. Paired test: `tests/test_session_state.py` (`open-sprint` over `DEPLOYED` → `0`; over `OPEN` → still `2`) | medium | `implementer_agent` | ⏳ |
| B02 | `scripts/session_state.py` | `fix(` — D10: `open-sprint --layer/--app/--name`; writes `path` and `branch`; drops a stale `name`. Paired test: `tests/test_session_state.py` (the exact base observation above now yields `path: docs/sprints/008-core-pipeline`, `branch: ai-sprint/008`, no `name`) | medium | `implementer_agent` | ⏳ |
| B03 | `scripts/session_state.py` | `fix(` — D11: `retry_hint` is mode-aware. Paired test: `tests/test_session_state.py` (submodule mode → `.agents/scripts/session_start.py`; nucleus → `scripts/session_start.py`; the existing assertions at `tests/test_session_state.py:229`, `:249`, `:299` updated to the nucleus form) | low | `implementer_agent` | ⏳ |
| B04 | `scripts/install_lock.py` | create — D12 (`check`, `write`); `invoked_by:` `workflows/start_workflow.md#pip_setup`, `scripts/session_start.py`. Paired test: `tests/test_install_lock.py` (absent lock → `2`; matching hash → `0`; an edited `-r` include → `2`; recursive includes followed; a cycle in includes does not hang) | medium | `implementer_agent` | ⏳ |
| B05 | `scripts/session_start.py` | `feat(` — the boot readiness reports `install_lock.py check` as an advisory, without changing the exit code. Paired test: `tests/test_session_start.py` | low | `implementer_agent` | ⏳ |
| B06 | `commands/start.md` | modify — D11, both forms. `tests/test_cursor_adapter.py` keeps passing: its rewrite targets `--tool claude-code`, which this unit leaves unchanged | low | `orchestrator` | ⏳ |
| B07 | `workflows/start_workflow.md` | modify — step 1 in both forms; `pip_setup` runs `install_lock.py check` and reinstalls on exit `2`, then `install_lock.py write` | low | `orchestrator` | ⏳ |
| B08 | `workflows/pipeline_workflow.md` | modify — Phase 3's `open-sprint` cell: new flags; writes `path`/`branch`; `DEPLOYED` accepted as sealed | low | `orchestrator` | ⏳ |

### Wave C — supply chain

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| C01 | `agents.md` | modify — D13: the three `§8` rows name `pnpm-workspace.yaml` keys and the `pnpm config get <key>` check; `RA-10` pointer text matches | medium | `rule_validator` | ⏳ |
| C02 | `rules/code_craft.md` | modify — line 37 quotes the `§8` key names; updated to the `pnpm-workspace.yaml` spelling (`RA-14` propagation of C01) | low | `rule_validator` | ⏳ |

### Wave Z — sprint records (Phase 8)

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Z01 | `docs/sprints/054-core-pipeline/PHASE_REGISTER.md` | create | low | `doc_orchestrator` | ⏳ |
| Z02 | `CHANGELOG.md` | modify — `[Unreleased]` entry citing each commit by short SHA | low | `doc_orchestrator` | ⏳ |
| Z03 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify — tick each delivered entry, citing the re-measurement and the closing commit | low | `doc_orchestrator` | ⏳ |
| Z04 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify — mark Sprint 054 delivered | low | `doc_orchestrator` | ⏳ |

Wave order: `0` → `A` → `B` → `C` → `Z`. Inside Wave A, A07 lands before A08, so the
template already passes the check that consumes it (the Sprint 041 Filter 6
precedent). A09 and B08 both take `workflows/pipeline_workflow.md`, in sequence.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | `check_fix_reproduces.py` uses `subprocess`, `tempfile` and `git worktree`; `install_lock.py` uses `hashlib`; pytest is already pinned in the test requirements |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| `Repro:` trailer check on `fix(` commits | script (`hooks/on_commit.py`) | git `commit-msg` hook, every commit |
| Red→green replay of `fix(` commits | script (`scripts/check_fix_reproduces.py`) | `agents/qa_agent.md` Gate 1, first check |
| Plan-table syntax and control checks | script (`audit_plan.py`) | `pipeline_workflow.md` Phase 1 and Phase 5 |
| Dry run of read-only plan rows | agent: running the commands is mechanical, but choosing a plausible expectation per row is judgment, which is why the recorded result is checked by A08 and not by a person | `pipeline_workflow.md` Phase 5 |
| Requirement-set lock check | script (`scripts/install_lock.py`) | `start_workflow.md#pip_setup`; `session_start.py --boot` |
| `NOTICE.md` relevance | agent judgment, kept deliberately: whether to disclose is a legal judgment (`close_workflow.md:22` already says presence is checkable and relevance is not) | `close_workflow.md` Phase 2 `repo_docs_check` |

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 28 (Wave 0: 2 · A: 12 · B: 8 · C: 2 · Z: 4), one commit each | Count of rows in Work tables |
| Subagents dispatched | ≈ 10: Phase 4.1/4.2/4.3 (3), `implementer_agent` batches by wave (≈ 4), Gate 1 and Gate 2 (2, fresh context), Phase 8 `doc_orchestrator` (1) | Phase 4.1 `agent_assignment.md` |
| Prior session ratio | n/a — Sprint 053 closed in a previous session; measure this one at close | `python3 scripts/session_cost.py --from-anchor --json` |

Soft (5×) / hard (15×) thresholds force an update to this section before new
work continues.

---

## Tests

**Reproduce before repairing.** Every `Yes` row below was **observed at `d848302`**
in this planning session (the Context table gives the command). This applies
`KI-053-4` to this plan before A07 makes it a template rule.

| Check | Fails against the current tree? | Observed at base |
| :--- | :--- | :--- |
| `quality_audit.py` on a nonexistent path / empty directory / `node_modules` root exits `2` | **Yes** — the defect | exit `0`, `0 unit(s) scanned`, three runs |
| `open-sprint` over `DEPLOYED` exits `0` | **Yes** | exit `2`, `Refusing open-sprint` |
| `open-sprint` writes `path`/`branch` for the new id and drops a stale `name` | **Yes** | `path: docs/sprints/007-core-pipeline`, `name: old-name` kept |
| `audit_regression_test` refuses a `fix(` without `Repro:` | **Yes** | returned `None` |
| `audit_plan.py` rejects an escaped `\|` in a backticked Verification command | **Yes** | exit `0`, `[OK] audit_plan` |
| `check_fix_reproduces.py` exists and rejects a test that passes on the parent | **Yes** | file absent (`ls scripts/check_fix_reproduces.py` → no such file) |
| `install_lock.py check` exits `2` after a requirement edit | **Yes** | file absent; no lock checker exists |
| `retry_hint` names the host path in submodule mode | **Yes** | `session_state.py:214` hardcodes `python3 scripts/session_start.py` |
| `open-sprint` still refuses over `OPEN` | **No** — a regression to protect | `tests/test_session_state.py` existing case |
| `tests/test_cursor_adapter.py` rewrite of `--tool claude-code` | **No** — a regression to protect | passes at base |
| `make verify` | **No** — a regression to protect | exit `0` at `d848302` (Sprint 053 close) |

---

## Verification

| Command | Expected | Dry run at `d848302` | Positive control |
| :--- | :--- | :--- | :--- |
| `venv_skillopt/bin/python -m pytest tests/test_quality_audit.py tests/test_on_commit.py tests/test_check_fix_reproduces.py tests/test_token_saver_auditor.py tests/test_session_state.py tests/test_install_lock.py tests/test_session_start.py tests/test_cursor_adapter.py -q` | exit `0` | run at close (two of the files do not exist yet) | — |
| `venv_skillopt/bin/python scripts/quality_audit.py does/not/exist; echo $?` | `2` | `0` (the defect) | the same command is the control |
| `python3 scripts/check_fix_reproduces.py --range d848302..HEAD; echo $?` | `0` — every `fix(` of this sprint reproduces red→green | not runnable (file absent) | its own test fixture with a non-reproducing fix exits `2` |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/054-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` | run at Phase 1 and Phase 5 | the scratch plan from the Context table exits `2` after A08 |
| `git grep -n "python3 scripts/session_start.py" -- commands workflows scripts` | each hit is either the nucleus form next to the host form, or a docstring that says it describes the nucleus | 3 host-blind hits (Context) | — |
| `git grep -n "npmrc" -- agents.md rules workflows` | no output | 1 hit (`agents.md:174`) | the same command at `d848302` prints that hit |
| `make verify; echo $?` | `0` | `0` at `d848302` | — |

Exit codes are read with `$?` directly, **never through a pipe**.

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | `§8` rows name `pnpm-workspace.yaml` and the check command (C01) |
| `rules/qa_and_testing.md` | `§4` label `remediation-regression`; unsatisfiable rows are `instructing` (A05) |
| `rules/code_craft.md` | `§6` names its enforcement; line 37 key spelling (A06, C02) |
| `workflows/pipeline_workflow.md` | Phase 3 `open-sprint` flags; Phase 5 dry run; Phase 7 replay first (A09, B08) |
| `workflows/close_workflow.md`, `workflows/standardization_workflow.md` | Conditional `NOTICE.md` and its template (A11, A12) |
| `workflows/start_workflow.md`, `commands/start.md` | Host and nucleus forms of the start command; lock check (B06, B07) |
| `docs/standards/templates/` | `IMPLEMENTATION_PLAN_TEMPLATE.md` columns; new `NOTICE_TEMPLATE.md` (A07, A10) |
| `agents/qa_agent.md` | Gate 1's first check (A04) |
| `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | Sprint 054 intake section; ticks at close (W01, Z03) |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Routing of blocks D and E; Sprint 054 delivered (W02, Z04) |
| `CHANGELOG.md` | `[Unreleased]` entry (Z02) |

**Measured figures.** Every figure in Context comes with the command that reproduces it.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `F-115-N2` S-1..S-8 and `F-114-N6` (sandbox template, installer, `RA-09` mechanism, tree walkers, TLS proxy, pnpm store, browser, sandbox failure table) | Block D. It changes the `RA-09` secrets contract, which is a design decision with competing options, and it has to be measured inside the real sandbox. **Sprint 055**, routed by W02 |
| `KI-053-2`, `KI-052-1`, `KI-052-3`, `KI-052-4`, `KI-052-7` | Block E, the nucleus's own instrument residue. **Sprint 056**, routed by W02 |
| `KI-052-5`, `KI-052-6`, `KI-052-8`, `KI-048-1`, `KI-053-3` | Already routed in the programme queue, outside the scope approved on 2026-10-04; their routing is unchanged |
| A JS/TS runner for `check_fix_reproduces.py` | D3. Opened as **`KI-054-1`** at W02. Until it lands, a host replays non-Python fixes with `Repro: manual` or with its own replay script |
| `loop_guard.py` naming the missing `current_sprint` key (`F-114-N3` proposal c) | Rejected in D10: once B02 lands, the reader no longer needs the better error message |
| Adding `NOTICE.md` to `session_probe.py`'s tuple | Rejected in D8 |
| `F-051-R1`, `F-051-R3`, `ADR-0006`, `ADR-0007`, `#13`, `REVDOC-G1` and the items the host lists as closed | Already in the register or closed; W01 does not file them again |

---

## Abort criterion

Decided before execution:

1. If A03 (`check_fix_reproduces.py`) cannot pass its own fixture test (a real
   red→green pair → `0`, a parent-passing test → `2`) after **three** implementer
   rounds, A03, A04, A06 and the Phase 7 half of A09 are withdrawn together and
   `F-114-N1` returns to the register as open with what was learned. A02
   (the trailer) ships alone only if Gate 1 agrees that a claim with no replay is
   still worth requiring.
2. If any Wave B change makes `make verify` or the `open-sprint` regression case
   fail and the cause is not understood within one round, the sprint stops at the
   last green commit and Wave B is re-planned with the human.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | _pending Phase 5_ |
| **Date** | _pending_ |
| **Plan commit at approval** | _pending_ |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*
