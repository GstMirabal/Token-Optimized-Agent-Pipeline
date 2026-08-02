---
description: "Protocol Integrity — invocation coverage, start/close symmetry, drift recovery (Phase 19)"
status: "IN_PROGRESS"
version: 1.0.0
---

# Roadmap: Phase 19 - Protocol Integrity

## Status
- **Strategy Lock:** `OPEN`
- **Completion:** 1 of 6 pull requests
- **Sprint ID:** `019` — next sequential number after Phase 18 (`018-post-publication-field-hardening.md`, `COMPLETED`).
- **Branch:** `ai-sprint/019` (`RA-12`). This is the first phase in this repository to actually use the branch convention `RA-12` mandates: `git log --all` records no prior `ai-sprint/*` reference.

## Objective
Repair defects **confirmed with evidence** in the framework's own protocols. Three independent inputs converged: five external publications on loop and graph engineering (which mostly restated capabilities this framework already has, often in stronger form), a symptom reported by the repository owner (`start` and `close` do not update everything), and an invocation audit of the tree that found published mechanisms nothing calls.

Capability work — loop stop-conditions, code-craft rules, tool-result pruning, parallel fan-out — is deliberately deferred to Phase `020`, so that a failure in something new cannot block the repair of something broken.

## Work Breakdown

| PR | Track | Scope | Status |
| :--- | :--- | :--- | :--- |
| 1 | **I** | Invocation coverage (`RA-16`), `make verify` ≡ CI, orphan remediation | ✅ **Merged into the branch** |
| 2 | **J** | Missing edges in the workflow graph (Phase 4 agents named, `close` → `deployment`, onboarding order, platform re-check, external-plan entry) | Pending |
| 3 | **E** | `start`/`close` symmetry, readiness and platform probes, branch sovereignty, generated workflow map | Pending |
| 4 | **H** | Protocol-failure detection (`last_close_commit`) and `/agents:reconcile` | Pending |
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

### Certification
- [x] `make verify` green end to end (75 tests, installer sandbox, all scanners).
- [x] `check_invocation_coverage()` proven to fail: 28 findings on the pre-fix tree, 0 after.
- [x] 10 new tests, each asserting failure where failure is required.
- [x] Counts recomputed after the retirement: 11 workflows, 12 commands, 13 agents, 8 rule contexts, 34 skills.

---
*Opened 2026-08-02 on `ai-sprint/019`. Not released — ledger entries sit under `[Unreleased]`.*
