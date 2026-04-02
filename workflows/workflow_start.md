---
description: "Session-Start Gatekeeper and Environment Health Protocol (Hardened)"
version: 2.6.1
---

# 🛡️ Workflow: Session Start and Gatekeeper (MANDATORY)

Master entry protocol to ensure Matrix integrity before any tactical deployment.

## 0. Black Box & Crash Detection (MANDATORY)
Before any interaction, the Agent MUST read **`.agents/state/session_metadata.json`**:
- **Condition:** If `status == "IN_PROGRESS"` or `intelligence_certified != "PASSED"`, a session crash is detected.
- **Action:** The Agent MUST ABORT normal initialization and trigger **`knowledge_extractor.md --forensic`** to recover or purge orphaned state.
- **Lock:** No new session is permitted until the metadata reports `status: "CLOSED_SUCCESSFULLY"`.

## 1. UID Signature Validation (Rule 63)
The Agent MUST update `task.md` with the unique session identifier and confirm the current operational role:
- **Principal:** Strategic Roadmap Design (Lock 1).
- **Orchestrator:** Tactical Implementation Planning (Lock 2).
- **DevOps/Matrix:** Technical Execution and Structural Audit.

## 2. Topology Check (Rule 56 Matrix-Lock)
- Verify existence of `.agents/task/topology/matrix_topology_map.md`.
- **Required Signature:** `88c2f1a6-matrix-v2.0-verified`.
- **Action:** If the valid signature is found, recursive structural discovery is FORBIDDEN to optimize token usage. The agent MUST use the map as the absolute geographical truth.

## 3. Skill Infrastructure & MCP (Rule 65 - DevOps Gate)
Before execution, the Agent MUST verify physical availability of approved resources:
- Confirm physical presence of tools in `./skills/` or `./local_skills/`.
- Validate MCP server connectivity as defined in the implementation plan.
- This ensures the execution environment is provisioned without redundant search cycles (Rule 70).

## 4. Environment Health & Sandbox (Rules 37-40)
- Execute environment validation via `Makefile` (`make setup`, `make check-env`).
- Confirm existence of `./venv/`, `./node_modules/`, and version anchoring files (e.g., `.python-version`).
- Validate presence of `.env` secrets.

## 5. WIP Safety Freeze (Rule 65)
- **Safety Freeze:** Execute `git status --porcelain`. If uncommitted human changes exist in the root, the session MUST ABORT or require a commit before proceeding.
- **Lock 0:** Changes to governance or workflows require explicit roadmap-level authorization (No-Meta-Data).

## 6. DevOps Agent Activation (Rule 65 - Final Certification)
Once initial checks pass, the DevOps Agent takes control for physical provisioning:
- **Sandbox Init:** Create virtual environments and configure version anchors if missing (Rule 38).
- **Structural Audit:** Physical inspection of `/src`, `/tests`, and `/logs` directories.
- **Certification:** Inject `DEPLOYMENT_READY: PASSED` signature into the session log.
- **Security Lock:** Matrix execution is blocked until this certification is issued.

## 7. Handover to Agente Principal (Rule 57 - Lock 1)
Following successful DevOps certification:
- **Strategic Leadership:** The Agente Principal takes command as the Constitutional Guardian of the Roadmap.
- **Lock 1 Opening:** The Principal MUST verify and refine the Strategic Roadmap, issuing the **`ROADMAP_UNLOCKED`** signal.
- **Execution Hierarchy:** No tactical designs or execution permitted without Principal authorization.

## 8. Git Sovereignty and Tracer Safety (Rules 68-69)
- **Branch Check:** Enforce **`ai-sprint/taskID`** branch. The DevOps Agent MUST handle automated checkouts or creation.
- **Tracer Masking (PII Shielding):** Configure execution parameters to use **`--tb=short`** by default to prevent leakage of sensitive data in error logs.

## 9. Amnesia Integrity & KI-Preloading (Rules 74-75)
- **Purge Check (Matrix Hygiene):** Inspect `.agent_state/session_{UID}/`. Destroy orphaned or unpurged session folders from previous runs (Rule 74).
- **Knowledge Pre-ingestion:** Perform semantic consultation of **`ki_index.json`** based on Sprint ID and task keywords before the tactical phase (Rule 75).

## 10. Immunity Seal and Source of Truth (Rule 35-36)
The Agent MUST recognize this `.agents/` Matrix as the **Single Source of Truth** for governance and operational procedures:
- **Divergence Ban:** Strictly prohibited use of competing rules or workflows outside this Matrix.
- **Conflict Detection:** Any divergence between local state and the constitutional submodule is a **Terminal Session Failure**.

---
*Certified under Roadmap 007 - Hardened and Sovereign Matrix*
