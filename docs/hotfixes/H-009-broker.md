# 🚑 Hotfix: H-009-broker
**File**: `docs/hotfixes/H-009-broker.md` (RA-03 emergency naming — sanctioned exception to RA-06)
**Severity**: `HIGH`
**Detected**: 2026-11-24 · **Resolved**: pending — merge of hotfix/H009

---

## 1. Symptom

Sprint 060 builds a GitHub App broker (`scripts/github_broker.py`, an MCP stdio server; decision
`ADR-0025`). `ADR-0025` D5 installs the broker only from a signed tag or a commit on `main`, with
`scripts/install_broker.py --commit <40-hex main sha>`. The script copies `scripts/github_broker.py`
out of that commit with `git show`. On 2026-11-24, `git log main -- scripts/github_broker.py` listed
0 commits. The file existed only on the sprint branch `ai-sprint/060`, and the last tag was
`v4.42.0`. The deployment that would bring it to `main` runs through the broker itself (Sprint 060
unit A-15). The first bootstrap was therefore unreachable, and the live broker measurement (unit
A-10) and the 060 deployment were blocked. Recorded as `KI-060-10` in
`docs/sprints/060-core-pipeline/SPRINT_LOG.md`.

## 2. Root Cause

`ADR-0025` D5 makes `main` the trust anchor for installing the broker, but the broker's only path to
`main` is a deployment that needs an installed broker. That is a circular bootstrap dependency. D5
itself stays unchanged: human decision 2026-11-24, option A, takes an `RA-03` hotfix that brings the
broker to `main`, merged by the human with `gh`.

## 3. Fix Applied

Every file except `README.md` and `tests/test_installer.sh` is a byte-for-byte copy from sprint commit `8fc9cba`.

| File | Change |
| :--- | :--- |
| `docs/decisions/ADR-0025-github-app-broker.md` | The decision, with its two `Superseded by ADR-0025` lines in `docs/decisions/ADR-0019-sandbox-regime.md` |
| `docs/architecture/GITHUB_BROKER_BLUEPRINT.md` | The Blueprint, which precedes the code (`agents.md` §0 Traceability) |
| `docs/guides/GITHUB_BROKER_SETUP_GUIDE.md` | The `RA-16` `invoked_by:` target of the broker |
| `scripts/github_broker.py` | The broker, an MCP stdio server |
| `tests/test_github_broker.py` | The tests that pin the broker's behaviour, copied with the broker |
| `README.md` | The counted block refreshed by `python3 scripts/check_readme_counts.py --write` (one more script) |
| `tests/test_installer.sh` | The test exports `maintenance.auto=false` and `gc.auto=0` through `GIT_CONFIG_*`. The seed `git commit` of its `nucleus_claude_only` repo spawned `git maintenance run --auto --detach`, whose detached `git repack` wrote `.git/info/refs` and `.git/objects/info/packs` while the EXIT trap `rm -rf "$WORK"` deleted the tree, so the cleanup failed in 2 of 3 runs in a fresh clone. It belongs to this hotfix because the branch check (`make verify` in a fresh clone of `hotfix/H009`) runs this test, so the hotfix cannot pass its own verification without it. Five consecutive runs in a fresh clone exit `0` and leave no `$TMPDIR/agents-installer.*`. Commit `d08c234`, `Repro: manual` (`KI-060-13`) |

Branch/commit: `hotfix/H009` → the commits are the output of `git log --oneline a6bddaa..hotfix/H009`, squash-merged to `main` as a single commit, as with H-008 `c3cfdfe` (hotfixes may merge outside the sprint cycle, but never unreviewed). **Branch prefix is mandatory (`agents.md` RA-03)** — `fix/`, `feat/`, and `chore/` branch names are protocol loss even when the Conventional Commits message type is `fix`.

## 4. Verification

- After each copy, `git diff 8fc9cba HEAD -- <file>` prints nothing.
- `make verify` exits `0` in a fresh clone of `hotfix/H009`, which, like CI, has no `docs/active_state.json`.
- After the merge, `git log origin/main --oneline -- scripts/github_broker.py` lists at least one
  commit. This is the defect check.
- The pinning test is `tests/test_github_broker.py`, which arrives with the broker. It pins the
  broker's behaviour. The defect itself, the broker being absent from `main`, is pinned by the
  `git log` check above.
- `qa_agent` and `tester_agent` review the branch before the merge.

## 5. Rule Amendment Check
- [ ] Is this failure class systemic? No escalation. The bootstrap gap is specific to `ADR-0025` D5 and is recorded as `KI-060-10`: N/A — KI-060-10
- [ ] Does the root cause reveal a design decision worth recording? No new ADR. D5 stands unchanged by human decision: N/A
- [ ] Master Ledger entry added under `[Unreleased]`: deferred to the Sprint 060 closeout entry; `hotfix/H009` does not edit `CHANGELOG.md`.
