---
description: "Master Session Close and Transactional Settlement Protocol (V 1.0.0)"
version: 1.0.0
---

# 🛡️ Workflow: Session Close and Transactional Settlement (MANDATORY)

Master closure protocol to ensure intelligence distillation, state purge, and governance sovereignty.

## 1. Intelligence Extraction (Rule 74 & 75)
The Agent MUST fulfill the knowledge distillation cycle before state destruction:
- **Action:** Mandatory execution of **`workflow_knowledge_extractor.md`**.
- **Certification:** Must receive the signature **`EXTRACTION_COMPLETE: INTELLIGENCE_DESTILLED`**.
- **Intelligence Guard:** If the extractor triggers a "Governance Reform Debate" (Rule 35), the Agente Principal must resolve it before proceeding.

## 2. Roadmap Liquidation Protocol (Rule 31 Refined)
Strategic settlement of the current phase:
- **Milestone Audit:** Check if the active Sprint or Phase has reached 100% completion.
- **Liquidation:** If criteria met, update the Roadmap status to **`COMPLETED (100%)`** and apply the final Principal UID signature.
- **Master Index Sync:** Reflect the completion in the root **`task/task.md`**.
- **2.1 Strategic Freeze:** Set `Strategic Lock: LOCKED` in `task/task.md` to ensure the next session requires fresh authorization (Rule 29).

## 3. High-Value Mirroring (Rule 55 - EXCLUSIVE)
Ensure historical traceability for human users by mirroring only high-level strategic assets:
- **Synchronization:** Transfer only the **Master Index**, **Topology Map**, and **Finalized Strategic Roadmaps** to the root `/docs/` folder.
- **Sanitization (MANDATORY):** Prohibited mirroring of the `sprints/` folder, individual implementation plans, or ephemeral agent-state context. These tactical artifacts MUST reside only in the `.agents/task/` internal repository.

## 4. Atomic Commitment & Git Sovereignty (Rules 32, 33 & 68)
Finalize the session's transactional record:
- **Verification:** Confirm the current branch is **`ai-sprint/taskID`**.
- **Dual Synchronization (Rule 32 - MANDATORY):** Execute atomic commits in BOTH the submodule and the parent repository if governance, roadmaps, or knowledge items are updated.
- **Commit Standard (Rule 33):** Execute the final commit using the conventional standard: `feat(id): session distillation and roadmap liquidation #XXX`.

## 5. Black Box Closure & Physical Amnesia (Rule 74)
Termination of the session's physical presence:
- **Metadata Update:** Atomically update **`.agents/.agent_state/session_metadata.json`** to:
  - `status: "CLOSED_SUCCESSFULLY"`
  - `intelligence_certified: "PASSED"`
- **The Great Purge:** Physically destroy the ephemeral directory **`.agent_state/session_{UID}/`**. All session-specific context MUST be annihilated.

## 6. Final Lock Handover
Formal declaration of session termination:
- **Sovereignty Seal:** Declare the Matrix as **LOCKED**. No further actions are permitted without a new **`workflow_start.md`** gatekeeper validation.

---
*Certified under Roadmap 008 - Matrix Strategic Intelligence*
