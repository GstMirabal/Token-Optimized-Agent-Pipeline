---
description: "Session-Close Protocol (Keyword: close)"
version: 1.2.0
---

# 🛡️ Workflow: Close (Atomic Liquidation)

Master closure protocol to ensure intelligence distillation, state purge, and governance sovereignty.

## 0. Governance & Constitutional Audit (Rule 1, 34, 57 - MANDATORY)
Before any transactional settlement, the Agent MUST read **`agents.md`** to ensure the final mirroring and commit logic is 100% compliant with Federated Governance constraints.

## 1. Intelligence Extraction (Rule 74 & 75)
The Agent MUST fulfill the knowledge distillation cycle before state destruction:
- **Action:** Mandatory execution of **`extract_workflow.md`**.
- **Certification:** Must receive the signature **`EXTRACTION_COMPLETE: INTELLIGENCE_DESTILLED`**.

### 1.1 Heuristic Pulse Audit (Rule 114 - LEARNING - BLOCKING)
Ensure the Matrix learns from this session's friction points:
- **Handshake:** The Agent **MUST** ask: *"¿Deseas realizar la destilación de telemetría de esta sesión para la base de conocimientos de gobernanza?"*
- **Rigorous Gate:** If the user denies or if distillation is skipped, the session is considered **FAILED_CONSTITUTIONAL_AUDIT** and cannot be closed as successful.
- **Execution:** Upon approval, invoke **`skills/local/governance-sentinel/scripts/distill.py`**.
- **Promotion:** If `proposals.md` contains formal clauses, prompt for constitutional update via **`apply_jurisprudence.py`**.

## 2. Roadmap Liquidation Protocol (Rule 31 Refined)
Strategic settlement of the current phase:
- **Milestone Audit:** Check if the active Sprint or Phase has reached 100% completion in `docs/active_state.json`.
- **Liquidation:** If criteria met, update the Roadmap status to **`COMPLETED (100%)`**.
- **Master Index Sync:** Reflect the completion in the root **`task.md`**.

## 3. High-Value Mirroring (Rule 55 - EXCLUSIVE)
Ensure historical traceability for human users by mirroring only high-level strategic assets:
- **Synchronization:** Transfer only the **Master Index**, **Topology Map**, and **Finalized Strategic Roadmaps** to the root `/docs/` folder.
- **Sanitization:** Prohibited mirroring of individual implementation plans or ephemeral agent-state context.

## 4. Atomic Commitment & Hook Sovereignty (Rule 114)
Finalize the session's transactional record:
- **Verification:** Confirm the current branch is calibrated for Sprint ID `#02x`.
- **Pre-Commit Handshake:** Execution of `git commit` WILL trigger the **`on_commit.py`** hook. The agent MUST NOT bypass this gate.
- **Dual Synchronization:** 
    1. **Submodule Commit:** Commit changes inside `.agents/` first.
    2. **Parent Update:** Update the submodule pointer in the parent repository.
- **Certification:** Report final commit hashes for BOTH the submodule and parent repository.

## 5. Black Box Closure & Physical Amnesia (Rule 74)
Termination of the session's physical presence:
- **Metadata Update:** Update **`docs/active_state.json`** to `status: "CLOSED_SUCCESSFULLY"`.
- **Nuclear Mirroring (Rule 52):** Immediately synchronize the finalized state to **`.agent_state/mirror.json`**.
- **The Great Purge (Rule 79):** Clear session-specific ephemeral telemetry in `core/memory/telemetry/raw_errors.json` IF jurisprudence was applied.

## 6. Final Lock Handover
Formal declaration of session termination:
- **Sovereignty Seal:** Declare the Matrix as **LOCKED**. No further actions are permitted without a new **`start_workflow.md`** gatekeeper validation.

---
*Certified under Roadmap 008 - Matrix Strategic Intelligence*
