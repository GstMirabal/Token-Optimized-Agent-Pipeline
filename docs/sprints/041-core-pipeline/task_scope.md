# Task Scope — Sprint 041 (bi-harness-bridge-parity)

Source: `docs/sprints/041-core-pipeline/IMPLEMENTATION_PLAN.md` (`## Work`) and
`agent_assignment.md` (Phase 4.1, the staffing authority).
Phase 4.3 of `workflows/pipeline_workflow.md`, audited by `rule_validator`.

This file is what `agents.md §2 jurisdictional_lock` and `no_interference` are
applied by **reading**. A unit not listed here has no claim on any file.

---

## Work

Shape: `# | File | Operation | Risk | Assignee | Model | Effort | Status`

`Model` / `Effort` are **required from Sprint 28 onward for every harness**, not
only under Cursor — `scripts/check_task_scope.py:38,119` (`MODEL_FROM_SPRINT = 28`).
Both assignees declare `tier: author` (`agents/implementer_agent.md:5-6`,
`agents/doc_orchestrator.md:5-6`), which `config/model_tiers.json` maps to
`sonnet` / `medium` on this harness. Family aliases only — a dated model ID in
this column is prohibited (`agents.md §7 RA-16` precedent, Sprint 022 `D1`).

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `scripts/bridge_state.py` | create | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U2 | `scripts/session_start.py` | modify | high | `implementer_agent` | opus | high | ⏳ |
| U3 | `hooks/on_init.py` | modify | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U4 | `scripts/cursor_adapter.py` | modify | medium | `implementer_agent` | sonnet | medium | ⏳ |
| U5 | `commands/start.md` | modify | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U6 | `workflows/start_workflow.md` | modify | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U7 | `workflows/deployment_workflow.md` | modify | medium | `doc_orchestrator` | sonnet | medium | ⏳ |
| U8 | `tests/test_bridge_state.py` | create | low | `implementer_agent` | sonnet | medium | ⏳ |
| U9 | `tests/test_session_start.py` | modify | low | `implementer_agent` | sonnet | medium | ⏳ |
| U10 | `docs/standards/templates/IMPLEMENTATION_PLAN_TEMPLATE.md` | modify | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U11 | `docs/standards/templates/SKILL_ASSIGNMENT_TEMPLATE.md` | modify | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U12 | `workflows/pipeline_workflow.md` | modify | low | `doc_orchestrator` | sonnet | medium | ⏳ |
| U13 | `scripts/install.py` | modify | **high** | `implementer_agent` | opus | high | ⏳ |
| U14 | `tests/test_installer.sh` | modify | medium | `implementer_agent` | sonnet | medium | ⏳ |

**Fourteen units, fourteen distinct physical files.** No file appears twice, so
`jurisdictional_lock` (one structural subject per task) and `no_interference`
(no file claimed by two in-flight subtasks) both hold by construction. Verify
with `awk -F'|' '/^\| U/ {print $3}' task_scope.md | sort | uniq -d` → empty.

### Tier escalation proposed — U2 only

`agents.md §6` routes a divergence between a task's difficulty and its role's
default tier through this file, recorded so the human sees it — never through a
selector agent, which would spend the unit of cost tiering exists to reduce.

| Unit | Default | Proposed | Reason |
| :--- | :--- | :--- | :--- |
| U2 | `sonnet` / `medium` (`author`) | **`opus` / `high`** | `scripts/session_start.py` is the arrival path of **both** harnesses. A regression here is not caught by a later command failing — it is caught by nobody, which is precisely the defect this sprint repairs |
| U13 | `sonnet` / `medium` (`author`) | **`opus` / `high`** | `scripts/install.py` installs the git hooks that gate secrets and commit messages. A regression here disables those gates silently, which is the same failure class the sprint exists to close |

Every other unit keeps its role default. Neither assignee is a `mechanical`
profile, so no `mechanical`-at-`high` escalation note is owed
(`scripts/check_task_scope.py:207-225`).

---

## Rule audit

Findings from auditing the roadmap against `rules/` and `agents.md`.

| Rule | Verdict | Note |
| :--- | :--- | :--- |
| `agents.md §2 jurisdictional_lock` | ✅ | One physical file per unit; fourteen distinct paths — **except U13+U14, paired by an explicit gate**: `.git/hooks/commit-msg` refuses a `fix(` commit that stages no test (`rules/code_craft.md §6`), so the installer fix and its assertions land together. A gate demanding the pairing outranks the one-file convention |
| `agents.md §2 no_interference` | ✅ | No duplicate target across in-flight units |
| `agents.md §2 pre_shielding` | ✅ | `git status --porcelain` was clean before the branch was cut; the only prior untracked path was this sprint's own directory |
| `agents.md §3 strict_rule` / `jurisdiction` | ✅ | Nucleus mode (`scripts/_mode.py`): `.git` is a real directory, so the framework **is** the work and these records belong at `docs/sprints/` here. No submodule to contaminate |
| `agents.md §5 mandatory_topology` | ✅ | Canonical path `docs/sprints/041-core-pipeline/` |
| `agents.md §5 historical_log` | ✅ | Every commit carries `#041` and Conventional Commits; enforced by `.git/hooks/commit-msg` |
| `RA-08 COMMIT_SQUASH` | ✅ | Atomic local commits, one per unit; squash happens at close |
| `RA-12 BRANCH_DISCIPLINE` | ✅ | `ai-sprint/041` created at Phase 3 from `main` at `d258b43`, before any commit |
| `RA-16 INVOCATION_COVERAGE` | ⚠️ **binding on U1** | `scripts/bridge_state.py` is a new mechanism. Its module docstring MUST declare `invoked_by: scripts/session_start.py, hooks/on_init.py`, and `scripts/verify_references.py` check (d) must resolve **Python imports**, not filename mentions — the precedent `RA-16` records is `merge_json.py`, which looked orphaned to a filename-only scan |
| `rules/code_craft.md §7` | ✅ | No new dependency. `IMPLEMENTATION_PLAN.md` `## Dependencies` says `None` explicitly |
| `rules/code_craft.md` complexity | ⚠️ **binding on U2** | `run_boot` is already the longest function in `session_start.py`. Adding the target-agnostic branch MUST NOT push it past 50 lines or 3 indentation levels (`agents.md §1`). If it would, the triage moves into a helper in U1's module rather than growing `run_boot` |
| `rules/qa_and_testing.md` | ⚠️ **binding on U8/U9** | Every check in the plan's `## Tests` marked **Yes** must be shown failing against `d258b43` before its repair lands (*reproduce before repairing*) |
| `agents.md §1` `ephemeral` markers | ✅ | No `TODO`/`FIXME` may enter any unit; `make verify` rejects them |
| `agents.md §1` `code_logic` | ✅ | All fourteen files are English. Spanish is confined to `IMPLEMENTATION_PLAN.md`, which `agents.md §1 user_chat` permits |

---

## Risk concentration

| Unit | Why it is the risk | Containment |
| :--- | :--- | :--- |
| **U2** `scripts/session_start.py` | It is the boot itself. A regression here breaks the arrival path of **both** harnesses, not just the one being repaired | Land U2 only after U1 and its tests (U8) are green. `tests/test_session_start.py` keeps its ten existing Cursor-shaped cases as regressions to protect |
| **U4** `scripts/cursor_adapter.py` | Changing the render changes `commands_stale()` digests, which is the freshness signal Sprint 039 built | U9 asserts `commands_stale()` still detects divergence after the rewrite is added; `tests/test_cursor_adapter.py` must stay green |
| **U7** `workflows/deployment_workflow.md` | A lock refreshed over a broken mirror reproduces the sprint's own defect from the deploy path | The plan's `D3` rule is explicit: refresh a lock only when that target's mirror is intact |

---

## Out of jurisdiction

Files an executing role may **not** touch under this scope, with where the
concern goes instead.

| Path | Why excluded |
| :--- | :--- |
| `skills/token-saver-auditor/scripts/audit_plan.py` | U10 repairs the template, not the filter. The filter's behaviour is a regression to protect |
| `scripts/check_forge_ladder.py` | U11 repairs the template, not the detector. Same reasoning |
| `.claude/`, `.cursor/` | Generated bridge mirrors, both gitignored. They are **outputs** of the installer, never edited by hand |
| `docs/active_state.json` | Anchor. Written only by `scripts/session_state.py` and the close workflow (`state_homologation`) |
| `scripts/check_task_scope.py` | U12 corrects the workflow prose, not the enforcing script. `MODEL_FROM_SPRINT = 28` is the authority and is a regression to protect |
| `scripts/cursor_adapter.py` install path | U13 repairs the nucleus **claude** branch only. The `cursor` and `both` branches already call both helpers and are regressions to protect |
| `Makefile` | No unit adds a target. The generalized template-gate check is routed to the roadmap, not built here |

---

## Finding raised by this audit — U12

`workflows/pipeline_workflow.md` Phase 4.3 declares the table shape as
`# | File | Operation | Risk | Assignee | Model | Effort | Status` **"when
`session_tool: cursor`"**, and `# | File | Operation | Risk | Assignee | Status`
otherwise. The script that enforces it disagrees:

```
scripts/check_task_scope.py:38    MODEL_FROM_SPRINT = 28
scripts/check_task_scope.py:119   if sprint_id is not None and sprint_id >= MODEL_FROM_SPRINT: return True
```

Model/Effort are required for **every sprint from 28 onward on every harness**;
the tool condition below that line is a secondary trigger for older sprints.
Measured here: this file was first written in the shape the workflow prescribes
for a non-Cursor session and the gate rejected it, `exit 2`.

Following a document's instruction produced a blocked gate — the same shape as
U10 and U11, in a third artifact. **U12 corrects the prose to match the script**,
because the script is what runs (`close_workflow.md` Phase 2.6 settles this class
of disagreement the same way: the enforcing artifact decides).

---

## Scope amendment — U13, opened during Phase 6

U2's end-to-end verification installed the Claude mirror correctly (0 → 13
symlinks) and then exposed a defect one layer down: **no `.bridge_claude.lock`
was written and no git hook was installed**, on a boot that exited `0`.

`scripts/install.py:497-498`:

```python
if args.target == "claude":
    return install_nucleus_bridge()      # early return
```

That return skips `install_nucleus_git_hooks()` and `write_bridge_locks()`,
which the `cursor` branch (499-503) and the `both` branch (504-508) both run.
This is rider **S3** of `021-030-program-queue.md`, which was recorded against
`--target cursor` and repaired **only** for `cursor` and `both`.

Without the lock, the next boot finds it stale, reinstalls, and still writes no
lock — a repair that never converges. Without the hooks, a Claude-only nucleus
checkout has no secret scanner and no commit-message gate.

`scripts/install.py` was **not** in this scope, so it is added here before being
edited rather than touched outside jurisdiction. Risk `high`, tier escalated to
`opus`/`high` for the same reason U2 was.

### U14 — the test the repair invalidates, and the one it revives

`tests/test_installer.sh` **pinned the defect as intended behaviour**:

```sh
[ ! -e "$NUCLEUS/.bridge_claude.lock" ] || fail "nucleus: Claude default must write no bridge lock"
```

with the stated reason *"`start_workflow.md bridge_check` for Claude still keys
on symlink-per-source rather than a lock"*. **U2 made that premise false** — the
boot now keys on the lock *and* the mirror. The assertion is inverted and the
expired premise is recorded beside it, the same correction Sprint 021 applied to
`rules/loop_governance.md` once the meter existed (`RA-14`).

A second assertion, *"nucleus cursor: must not write Claude lock"*, is **kept and
strengthened**. It is the target-isolation guarantee this sprint's `D3` rests on.
It was passing without ever being exercised: the Claude install wrote no lock, so
the directory was incidentally clean. The lock is now cleared immediately before
the Cursor run, so a Claude lock found afterwards was written **by** that run.

The new end-to-end block runs in a checkout of its own with a real `git init`,
never the shared `$NUCLEUS`: asserting the Cursor mirror is absent is only
meaningful where no Cursor install has ever run.
