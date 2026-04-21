---
description: "Session-Start Protocol (Keyword: start)"
version: 4.0.0
---

# 🛡️ Workflow: Start (Matrix Initiation)

Master entry protocol optimized to ensure Matrix V2 integrity and strictly invoke the execution pipeline.

## 0. Constitutional Invocation (Phase 0 - Amnestic Anchor)
Before any operational logic, ALL subagents triggered in this session MUST strictly operate under **Zero-Memory** initialization.
- **Mandatory Action:** Perform a federated read of `agents.md` as the absolute first action to adopt current governance. Role usurpation is strictly prohibited.

## 1. Zero Coordinate & Collision Guard (Matrix V2)
Before mapping tasks or generating blueprints, determine session habitability:
- **Zero Coordinate Extraction:** Read the anchor point **`docs/active_state.json`** to collect global scope, App, Layer, and Sprint ID. Initialization is prohibited if the workspace is the `.agents` nucleus.
- **Nuclear Mirror Recovery:** If `docs/active_state.json` is missing or invalid, search for `.agent_state/mirror.json`. If it exists, mechanically restore its contents to the anchor.
- **Collision Action:** If status `IN_PROGRESS` exists with a different session UID, immediately abort and trigger forensic analysis.

## 2. Synchronization & Governance Sentinel
Invoke the **[GitHub Sentinel](../agents/github_sentinel.md)** to establish an upstream audit.
- **Action:** Sync audit via MCP to block drift. No execution is permitted if the local repository is trailing behind the remote origin.

## 3. Environment Shielding
Invoke the **[DevOps Sentinel](../agents/devops_sentinel.md)** to guarantee operational safety.
- **Action:** Enforce strict `.env` export protocols to the session terminal. Explicit parsing or memory-ingestion of `.env` strings by any agent is constitutionally banned.

## 4. Hook Protocol (Documentary Sovereignty)
Ensure the topography follows the `[layer]/[app]/` hierarchy.
- **Action:** Provide a topological scan to the **[Rule Validator](../agents/rule_validator.md)**. If sub-directories like `/contracts/` or `/sprints/` are missing, they must be synthetically instantiated.

## 5. Pipeline Handoff (V2 Initiation)
Once environment and constitution are verified safe, initiate the operational engine.
- **Action:** Trigger the **`matrix_workflow.md`** Protocol. Hand command explicitly to the Orchestrator for Phase 1. 

---
*Optimized for Matrix V2 Chain of Command (v4.0.0).*
