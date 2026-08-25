# Hotfix: H-003-deployment
**File**: `docs/hotfixes/H-003-deployment.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `HIGH`
**Detected**: 2026-08-25 · **Resolved**: 2026-08-25

---

## 1. Symptom

After `/agents:deployment` for Hotfix H-002 / seal `4.9.1`, two closure gaps were observed on a tree that had already passed `ci_gate` and tagged `v4.9.1`:

1. GitHub Releases: Latest stayed on `v4.3.0`. Tags `v4.4.0`…`v4.9.1` had no Release landing page while the README promised one per tag.
2. Branch prune: local and origin heads `hotfix/H-002` and `release/4.9.1` survived squash-merges of PRs `#51` and `#52`.

## 2. Root Cause

Two independent protocol holes; neither is a squash-blindness bug in `git cherry`.

| # | Mechanism | Evidence |
| :--- | :--- | :--- |
| 1 | `deployment_workflow.md` Phase 4 named only `release_tagging` (`git tag -a`). No step created a GitHub Release. | `[4.3.0]` backfilled Releases once; Latest never moved. `gh release list` showed Latest `v4.3.0` while `git tag` listed `v4.9.1`. |
| 2 | `close_workflow.md` 5.5 `local_prune` runs **before** `gh pr merge --squash`. Deployment never re-invoked prune. `prune` also only deleted the local ref (`git branch -D` + `git remote prune origin`), which cannot delete a live origin head. | `git cherry main hotfix/H-002` prints `- f52a60a` (integrated). `gh api … --jq .delete_branch_on_merge` is `false`. |

A branch named `fix/…` was opened for this work and abandoned: RA-03 requires `hotfix/H-00N` and `docs/hotfixes/`.

## 3. Fix Applied

| File | Change |
| :--- | :--- |
| `workflows/deployment_workflow.md` | Phase 4 `github_release` after `release_tagging`; Phase 4 `local_prune` after the Release |
| `scripts/publish_github_release.py` | Notes from `## [X.Y.Z]`; `--verify-tag`; `--missing` backfill; never `--notes-from-tag` |
| `tests/test_publish_github_release.py` | Pins section extraction, missing-section refusal, `--missing` selection |
| `scripts/branch_sovereignty.py` | `prune` deletes proven-integrated `origin` heads before local `-D` |
| `tests/test_session_protocol.py` | Pins origin-head deletion on prune |
| `workflows/close_workflow.md` | States that post-merge prune is invoked from deployment |

Branch/commit: `hotfix/H-003` (SHA recorded by git; do not hand-edit).

Operational backfill (not inventing notes): `publish_github_release.py --missing` published `v4.4.0`…`v4.9.1` from their sealed ledger sections on 2026-08-25; Latest is `v4.9.1`.

## 4. Verification

```
./venv_skillopt/bin/python -m pytest tests/test_publish_github_release.py tests/test_session_protocol.py -q --tb=line
python3 scripts/map_workflows.py --check
gh release list --limit 8   # Latest must be v4.9.1; v4.4.0…v4.9.0 present
```

After this hotfix merges: `python3 scripts/branch_sovereignty.py prune` must delete leftover `hotfix/H-002` / `release/4.9.1` when they remain proven-integrated and are not `HEAD`.

## 5. Rule Amendment Check

- [x] Systemic process pattern? Yes — (a) closure steps that existed only as README/close handoff without a named deployment invoker (`RA-16`); (b) `RA-03` named the hotfix *doc* path but not the *branch* prefix, so an agent opened `fix/github-release-in-deploy`. `RA-03` amended 2026-08-25 to require `hotfix/[H-ID]`. Link: `agents.md` RA-03
- [x] New architectural choice? No. Releases still come from the sealed ledger; prune still requires proven integration. ADR: `N/A`
- [x] Master Ledger entry added under `[Unreleased]`.
- [x] Protocol-loss lesson indexed: `memory_index.json` `F-20260825-H003` (raw: `memory/H-003-protocol-loss.md`, ephemeral).
