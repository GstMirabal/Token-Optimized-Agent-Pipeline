---
description: "Vanguard Deployment and Production Release Protocol (Keyword: deploy)"
version: 3.0.0
---

# 🛡️ Workflow: Deploy (The Vanguard Protocol)

The terminal sequence for graduating verified Matrix code from the localized sandbox into production/main branch.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Zero Anchor** | `git_state_gate` | `DevOps Sentinel` halts execution if `git status --porcelain` detects uncommitted changes. |
| **1. Branch Merge**| `test_audit` | Ensure the Phase 4 `Tester Agent` signature exists (100% passed coverage). |
| **1. Branch Merge**| `pr_flow` | **Default (GitHub remote exists)**: open a Pull Request from `ai-sprint/[ID]` into `main` via `gh pr create`, wait for CI to pass, and merge via `gh pr merge --squash`. Direct local merge to `main` is only the fallback when no GitHub remote is configured (J-12 Branch Discipline). |
| **1. Branch Merge**| `deploy_unlock` | For the local-fallback push only: `touch .agents/.deploy_unlock` immediately before the sanctioned `git push origin main`, and **delete it right after** — the `on_commit.py` push guard blocks any push to `main` while this marker is absent. |
| **2. Environment** | `production_bridge`| Map/mount production environment variables securely. Apply pending `.sql` migrations. |
| **3. Remote Sync** | `ci_cd_handover` | Run local health checks. Confirm the merge landed on origin and remote pipelines triggered. |
| **4. Closure** | `release_tagging` | Assign a semantic `git tag -a vX.Y.Z` identifying the sprint release. |

---
*Optimized for Matrix V3 Production Integrity — PR-based merge with CI gate (v3.0.0).*
