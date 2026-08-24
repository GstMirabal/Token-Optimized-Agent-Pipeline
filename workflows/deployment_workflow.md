---
description: "Deployment and Production Release Protocol (Keyword: deploy)"
version: 3.0.0
invoked_by: human:/agents:deployment
---

# 🛡️ Workflow: Deploy (Deployment Protocol)

The terminal sequence for graduating verified pipeline code from the localized sandbox into production/main branch.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Git State Gate** | `git_state_gate` | `DevOps Agent` halts execution if `git status --porcelain` detects uncommitted changes. |
| **1. Branch Merge**| `test_audit` | Ensure the Phase 4 `Tester Agent` signature exists (100% passed coverage). |
| **1. Branch Merge**| `pr_flow` | **Default (GitHub remote exists)**: open a Pull Request from `ai-sprint/[ID]` into `main` via `gh pr create`, then run `python3 .agents/scripts/ci_gate.py [N]` and **observe it exit `0` as a separate invocation BEFORE issuing** `gh pr merge --squash` (RA-13 Sequential Gates — never chain wait-and-merge in one script). Direct local merge to `main` is only the fallback when no GitHub remote is configured (RA-12 Branch Discipline). **This step named `gh pr checks [N] --watch` until Sprint 023 `C10`, and that command cannot gate a merge**: it waits for the checks GitHub has already registered, so a required check not yet registered is not waited for at all. Measured on PR `#45` — created `16:12:37`, `--watch` returned at roughly `16:13` having seen only `audit`, while `Analyze (python)` completed `16:16:21`. Two of three required checks had not reported when the gate went green; what actually blocked that merge was GitHub branch protection, **not this protocol**, and `/agents:harden` is optional, so on a host without it the merge would have landed unverified. `ci_gate.py` inverts the question — it reads what the base branch *requires* (branch protection **and** rulesets, since neither endpoint reports the other) and confirms each one reported and passed, treating an unregistered required check as pending and **a branch declaring no required check as a failure**, because an unprotected repository is not a verified one. |
| **1. Branch Merge**| `deploy_unlock` | For the local-fallback push only: `touch .agents/.deploy_unlock` immediately before the sanctioned `git push origin main`, and **delete it right after** — the `on_commit.py` push guard blocks any push to `main` while this marker is absent. |
| **2. Environment** | `production_bridge`| Map/mount production environment variables securely. Apply pending `.sql` migrations. |
| **3. Remote Sync** | `ci_cd_handover` | Run local health checks. Confirm the merge landed on origin and remote pipelines triggered. |
| **4. Closure** | `ledger_seal` | Seal the Master Ledger: rename `CHANGELOG.md`'s `[Unreleased]` section to `[vX.Y.Z] - date` (leaving a fresh empty `[Unreleased]`). This commit lands with the release. |
| **4. Closure** | `release_tagging` | Assign a semantic `git tag -a vX.Y.Z` identifying the sprint release — the tag must match the ledger section just sealed. |

---
*Optimized for Pipeline Production Integrity — PR-based merge with CI gate (v3.0.0).*
