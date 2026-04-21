---
description: "Vanguard Deployment and Production Release Protocol (Keyword: deploy)"
version: 1.0.0
---

# 🛡️ Workflow: Deploy (The Vanguard Protocol)

The terminal operational sequence for graduating verified Matrix code from the localized sandbox environment into production, CI/CD pipelines, or the upstream `main` git branch safely.

## 0. Zero Coordinate & Gateway Verification
- **Amnesia State:** Agent initializes with Zero Memory.
- **Role Isolation:** The **[DevOps Sentinel](../agents/devops_sentinel.md)** drives this mission. No application code files may be logically modified during deployment.
- **Git State Gate:** Execution immediately halts if `git status --porcelain` detects uncommitted or untracked changes in the active `ai-sprint/` branch.

## 1. Branch Aggregation and Merge Audit
- **Integration Test Suite Validation:** Ensure the Phase 4 `Tester Agent` signature exists, marking the active branch as mathematically sound (100% passed coverage).
- **Merge Action:** Execute atomic merge from the localized `ai-sprint/taskID` branch into the unified parent `main` (or upstream target) branch.

## 2. Environment Variables & Production Bridge
- **Production Pre-Flight:** Map external services and database secrets. Explicitly swap or mount the production variables securely (bypassing local `.env` mock parameters).
- **Migration Sweep:** Directly apply pending database `.sql` schema migrations via the ORM strictly to the staging/production instance. 

## 3. Remote Synchronization (CI/CD Handover)
- **Containerization Verification:** Run local `docker build` health checks to prove deterministic output prior to remote shipment.
- **Trigger/Push:** Execute atomic `git push` to origin, allowing remote pipelines (GitHub Actions, Docker Registry, Vercel/AWS) to capture the hook.

## 4. Release Tagging & Closure
- **Semantic Tagging:** Assign a `git tag -a vX.Y.Z` identifying the completed sprint payload release.
- **Golden Gate Notification:** Notify the User: *"Production Merge and Upstream Push completed successfully. Matrix operations transition back to Development mode."*
- **SESSION LOCKED**.

---
*Optimized for Matrix V2 Production Integrity*
