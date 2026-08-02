---
description: "Protocol Integrity — invocation coverage, start/close symmetry, drift recovery (Phase 19)"
status: "IN_PROGRESS"
version: 1.0.0
---

# Roadmap: Phase 19 - Protocol Integrity

## Status
- **Strategy Lock:** `OPEN`
- **Completion:** 4 of 6 pull requests
- **Sprint ID:** `019` — next sequential number after Phase 18 (`018-post-publication-field-hardening.md`, `COMPLETED`).
- **Branch:** `ai-sprint/019` (`RA-12`). This is the first phase in this repository to actually use the branch convention `RA-12` mandates: `git log --all` records no prior `ai-sprint/*` reference.

## Objective
Repair defects **confirmed with evidence** in the framework's own protocols. Three independent inputs converged: five external publications on loop and graph engineering (which mostly restated capabilities this framework already has, often in stronger form), a symptom reported by the repository owner (`start` and `close` do not update everything), and an invocation audit of the tree that found published mechanisms nothing calls.

Capability work — loop stop-conditions, code-craft rules, tool-result pruning, parallel fan-out — is deliberately deferred to Phase `020`, so that a failure in something new cannot block the repair of something broken.

## Work Breakdown

| PR | Track | Scope | Status |
| :--- | :--- | :--- | :--- |
| 1 | **I** | Invocation coverage (`RA-16`), `make verify` ≡ CI, orphan remediation | ✅ **Merged into the branch** |
| 2 | **J** | Missing edges in the workflow graph (Phase 4 agents named, `close` → `deployment`, onboarding order, external-plan entry) | ✅ **Merged into the branch** |
| 3 | **E** | `start`/`close` symmetry, readiness and platform probes, branch sovereignty, generated workflow map | ✅ **Merged into the branch** |
| 4 | **H** | Protocol-failure detection (`last_close_commit`) and `/agents:reconcile` | ✅ **Merged into the branch** |
| 5 | **G** | Documentary closeout: README counts as a build failure, repo docs review | Pending |
| 6 | **F** | Complete `revdoc`: C4, Blueprints, ADR recovery, metadata stamping, findings destination | Pending |

## PR 1 — Track I (complete)

### What the detector found before anything was fixed
Running `check_invocation_coverage()` against the unmodified tree produced **28 findings**: 12 workflows, 5 scripts and 11 executable skills with no declared caller. Running it first was the point — a detector demonstrated only against a tree already cleaned proves nothing.

| Finding | Disposition |
| :--- | :--- |
| `make verify` and `ci.yml` asymmetric **in both directions** | `ci.yml` now invokes `make verify`. Divergence became impossible rather than policed |
| `skeleton_workflow.md` bypassed by its own governance | Retired, with `commands/skeleton.md`. `omni_minimizer.py` untouched |
| `remediation_workflow.md` named by nobody | Named in `rules/qa_and_testing.md §4` and `agents/principal_agent.md` |
| `contract-writer` unwired from the phase it was built for | `revdoc` Phase 6 now names it |
| `migrate_docs_v3.py` orphaned | Removed |
| `merge_json.py` **apparently** orphaned | **Kept** — `install_claude.py` imports it as a module |
| 11 workflows, 4 scripts, 10 skills | Invoker declared, or typed exception recorded |

### Findings recorded

| Finding | Consequence |
| :--- | :--- |
| **A filename-based orphan scan produces false positives that delete working code.** `merge_json.py` is imported as `from merge_json import merge`, so a scan for `merge_json.py` finds nothing. | Deleting it would have broken the bridge installer — the sanctioned path into a host's `.claude/`. The checker now resolves Python imports via AST, and a test fails if that regresses. |
| **A gate that lives only in CI is not a gate for the person deciding to push.** | Made local, the RA-15 path scan immediately rejected two literals written during this very PR: one in the Phase 018 roadmap, one in the new scanner's own docstring. Both would have failed only after push. |
| **Cost was measured, not assumed.** | The full `make verify`, including 75 tests and the installer sandbox, runs in **1.7 s**. The usual argument for splitting a verify target into fast and slow halves — which is how the asymmetry would return — does not apply here. |
| **The phase practised what it legislates.** | `RA-16` landed in PR 1 precisely so the five mechanisms the remaining PRs introduce (`map_workflows.py`, `check_readme_counts.py`, `reconciliation_workflow.md`, and the two probes) cannot be born orphaned. |

## PR 2 — Track J (complete)

Four missing edges closed. **A fifth, `platform_recheck` in `close`, was deliberately moved to PR 3**: it reuses the platform probe that PR 3 builds, and writing a step that calls a mechanism which does not yet exist is precisely what `RA-16` — merged one PR earlier — forbids. The sequencing error was caught by the rule this phase had just introduced.

| Edge | Before | After |
| :--- | :--- | :--- |
| Phase 4 | One cell: *"Summon Agent Orch, Skill Arch, and Rule Val"* | `4.1`/`4.2`/`4.3`, proper names, deliverables named including `task_scope.md` |
| External plan → Phase 1 | Undeclared | An approved external plan is an **input** to Phase 1 and does not skip Phases 3-5 |
| `close` → `deployment` | Jurisdiction only (*"exclusively deployment's job"*) | `deployment_handoff` step names the protocol and why the merge lives there |
| Onboarding order | Three entry points, no sequence; the README omitted `standardization` | Declared once in `agents.md §6`; README and guide reference it |

## PR 3 — Track E (complete)

Four mechanisms, each of them a script rather than an instruction, because all four run once per session and `token_economy_agent`'s Filter 5 rejects a recurring mechanism delegated to agent judgment when a deterministic equivalent exists.

| Mechanism | What it replaced |
| :--- | :--- |
| `scripts/session_state.py` | A workflow that wrote nothing and a collision guard nothing armed |
| `scripts/session_probe.py` | Three checks that did not exist: graph freshness, documentation presence, platform controls |
| `scripts/branch_sovereignty.py` | A close that pushed a branch and never asked whether it was integrated |
| `scripts/map_workflows.py` | A step map that would have drifted at the first edit |

### The finding worth keeping

**Neither obvious instrument works for detecting an unintegrated branch here.** `git branch --merged` fails outright: `deployment` merges with `gh pr merge --squash`, and a squash commit is not a descendant of the branch, so the branch never appears as merged however completely its work landed. Verified — `git log --all --merges` after `v4.3.0` shows zero merge commits for five integrated pull requests. `git cherry` is better but still misses a multi-commit branch collapsed into one, since it compares per-commit patch-ids. Merged-PR state is the authoritative signal for a squash workflow; `git cherry` is the offline fallback; anything neither can prove is reported rather than assumed, and a false positive is answered with a recorded waiver instead of by weakening the check.

The audit is deliberately **not** scoped to `ai-sprint/*`: `git log --all` records no such reference anywhere in this repository's history. A check scoped to a naming convention the repository does not follow reports clean on a dirty tree — the same defect `revdoc` Phase 4 documents for path prefixes.

### Verification observed
- The lock refused a second session with exit `2`, then refused the restoration attempt of the session that owned it — correct behaviour, resolved with the explicit `--takeover`.
- The probes reported, unprompted, exactly the five disabled platform controls and the two missing documentation artifacts that had been found by hand during planning.
- The branch audit exits `2` on `ai-sprint/019` itself, which is genuinely unintegrated.
- The generated map shows `start_workflow` moving from `—` to `read/write` on the state anchor: the symmetry is machine-visible, not asserted.

## PR 4 — Track H (complete)

The drift this phase opened by repairing now has a detector and a protocol. `last_close_commit` is the whole mechanism: one field, stamped at close, against which `HEAD` can be compared. Its absence is why the `v4.3.0` drift went unnoticed for a week — there was nothing to compare against, so no amount of diligence would have surfaced it.

**Verified by replaying the real event.** Pointed at the commit preceding pull requests `#27`-`#30`, the detector lists them and exits `2`. That is the same drift that was reconciled by hand at the start of this session; `workflows/reconciliation_workflow.md` is the transcript of that recovery rather than a design sketch.

**Two boundaries recorded explicitly**, because both are destructive if crossed:
- `reconcile` **reverts nothing**. `remediation_workflow.md` revokes bad work with `git restore .`; here the work is good and only its record is missing. Confusing them would destroy exactly what needs documenting.
- The check runs **before** `state_claim`. Claiming the lock writes `IN_PROGRESS`, so a status-keyed check placed after it would be reading its own side effect. The detector is status-agnostic for the same reason: it compares commits, not labels.

With no baseline recorded, it reports that fact and passes, rather than passing silently. Silence about an unmeasurable state is precisely what allowed the original drift.

## Certification
- [x] `make verify` green end to end (88 tests, installer sandbox, all scanners).
- [x] `check_invocation_coverage()` proven to fail: 28 findings on the pre-fix tree, 0 after.
- [x] 10 new tests, each asserting failure where failure is required.
- [x] Counts recomputed after the retirement: 11 workflows, 12 commands, 13 agents, 8 rule contexts, 34 skills.

---
*Opened 2026-08-02 on `ai-sprint/019`. Not released — ledger entries sit under `[Unreleased]`.*
