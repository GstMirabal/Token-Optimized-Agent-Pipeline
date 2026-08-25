---
description: "Deployment and Production Release Protocol (Keyword: deploy)"
version: 3.2.0
invoked_by: human:/agents:deployment | close_workflow.md#deployment_handoff
---

# 🛡️ Workflow: Deploy (Deployment Protocol)

The terminal sequence for graduating verified pipeline code from the localized sandbox into production/main branch.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Sprint Seal Gate** | `sprint_seal_gate` | Run `python3 .agents/scripts/session_state.py require-released` (nucleus: `python3 scripts/session_state.py require-released`). **Exits `2` and deployment stops** when `status` is `SUSPENDED` (session ended with the sprint still open — never publish that tip) or when the ref tip is not exactly `last_close_commit` (no `release` sealed this tip). Pass `--branch ai-sprint/[ID]` when `HEAD` has already moved to a newer claim. A live `IN_PROGRESS` session on an *unsealed* tip is the same refuse. This gate is what makes `close` → auto-deploy safe and `suspend` → deploy impossible. |
| **0. Git State Gate** | `git_state_gate` | `DevOps Agent` halts execution if `git status --porcelain` detects uncommitted changes. |
| **1. Branch Merge**| `test_audit` | Ensure the Phase 4 `Tester Agent` signature exists (100% passed coverage). |
| **1. Branch Merge**| `pr_flow` | **Default (GitHub remote exists)**: open a Pull Request from `ai-sprint/[ID]` into `main` via `gh pr create`, then run `python3 .agents/scripts/ci_gate.py [N]` and **observe it exit `0` as a separate invocation BEFORE issuing** `gh pr merge --squash` (RA-13 Sequential Gates — never chain wait-and-merge in one script). Direct local merge to `main` is only the fallback when no GitHub remote is configured (RA-12 Branch Discipline). **This step named `gh pr checks [N] --watch` until Sprint 023 `C10`, and that command cannot gate a merge**: it waits for the checks GitHub has already registered, so a required check not yet registered is not waited for at all. Measured on PR `#45` — created `16:12:37`, `--watch` returned at roughly `16:13` having seen only `audit`, while `Analyze (python)` completed `16:16:21`. Two of three required checks had not reported when the gate went green; what actually blocked that merge was GitHub branch protection, **not this protocol**, and `/agents:harden` is optional, so on a host without it the merge would have landed unverified. `ci_gate.py` inverts the question — it reads what the base branch *requires* (branch protection **and** rulesets, since neither endpoint reports the other) and confirms each one reported and passed, treating an unregistered required check as pending and **a branch declaring no required check as a failure**, because an unprotected repository is not a verified one. |
| **1. Branch Merge**| `deploy_unlock` | For the local-fallback push only: `touch .agents/.deploy_unlock` immediately before the sanctioned `git push origin main`, and **delete it right after** — the `on_commit.py` push guard blocks any push to `main` while this marker is absent. |
| **2. Environment** | `production_bridge`| Map/mount production environment variables securely. Apply pending `.sql` migrations. |
| **3. Remote Sync** | `ci_cd_handover` | Run local health checks. Confirm the merge landed on origin and remote pipelines triggered. |
| **4. Closure** | `ledger_seal` | Seal the Master Ledger: rename `CHANGELOG.md`'s `[Unreleased]` section to `[vX.Y.Z] - date` (leaving a fresh empty `[Unreleased]`). This commit lands with the release. |
| **4. Closure** | `release_tagging` | Assign a semantic `git tag -a vX.Y.Z` identifying the sprint release — the tag must match the ledger section just sealed. Push the tag (`git push origin vX.Y.Z`). Do not create the GitHub Release in this step. |
| **4. Closure** | `github_release` | After `release_tagging` has pushed tag `vX.Y.Z`, run `python3 .agents/scripts/publish_github_release.py vX.Y.Z` and observe exit `0` as a **separate invocation** (RA-13 — never chain tag-and-release). The script creates the GitHub Release from `CHANGELOG.md`'s `## [X.Y.Z]` section, failing if that section is missing (never `--notes-from-tag`), and passes `--verify-tag` so `gh` cannot mint a tag from `main`. `--latest` is set only when that section is the newest sealed version. A tag with no ledger section is not a release. To fill tags that predate this step: `python3 .agents/scripts/publish_github_release.py --missing`. |
| **4. Closure** | `local_prune` | After the seal and Release land, run `python3 .agents/scripts/branch_sovereignty.py prune` as a **separate invocation**. `close_workflow.md` 5.5 already ran prune **before** `gh pr merge --squash`, so it could not delete the branch just published (`HEAD`, still unmerged). This is the post-merge call: it deletes proven-integrated local heads **and** their `origin` heads when still present. GitHub `delete_branch_on_merge` is independent and may be `false`. |

---
*Optimized for Pipeline Production Integrity — PR-based merge with CI gate (v3.2.0); Hotfix H-003 wires `github_release` and post-merge `local_prune`; Sprint 029 adds `sprint_seal_gate` so suspend never chains into deploy.*
