---
description: "Knowledge Extractor and Intelligence Distillation Protocol (V 3.4.0)"
version: 3.4.0
---

# 🧠 Workflow: Knowledge Extractor & Intelligence Distillation

Master protocol for heuristic extraction, Matrix memory update, and ephemeral state purge before session destruction. Aligned with Phase 13.

## 1. Phase 1: Brain Drain & Forensic Audit
Retrospectively audit the session logs and telemetry nodes to identify high-value intelligence:
- **Normal Close:** 
    - Scan the current session's terminal outputs and implementation logs.
    - **MANDATORY SCAN:** Analyze `core/memory/telemetry/raw_errors.json` for persistent friction points recorded by the DevOps Sentinel.
- **Forensic Mode:** 
    - Triggered if orphaned `docs/sprints/` folders are found at session-start.
    - **Nuclear Mirror Sync:** The agent MUST verify the last known good state via `.agent_state/mirror.json` to contextualize orphaned logs.
- **Targets:** Exotic workarounds (e.g., environment-specific library hangs), non-obvious logic bug-fixes, and strategic orchestration heuristics.

## 2. Phase 2: Knowledge Hardening & Redundancy Filter (Rule 74 Pt 4)
Filter the distilled intelligence to maintain context-density:
- **Agnostic Validation:** Knowledge MUST be transferable and project-independent (Rule 34).
- **Constitutional Synchronization:** Compare findings against **Global Rules (1-114+)**. If the lesson is already codified in governance or Phase 13 roadmaps, the extraction project for this item is **ABORTED**.
- **PII Shielding:** Ensure absolute sanitization of secrets, credentials, and user data before indexing.

## 3. Phase 3: Domain-Based Indexing (Rule 75)
Persist the knowledge in a structured and scalable format:
- **Domain Persistence:** Save the item into its categorical subfolder in `core/memory/`.
- **Semantic Update:** Perform an atomic update of `core/memory/core/memory_index.json` (v1.4.1+) with 1-line metadata.

## 4. Phase 4: Amnesia Certification & Handover
Formal conclusion of the intelligence lifecycle:
- **Signature:** Issue the **`EXTRACTION_COMPLETE: INTELLIGENCE_DESTILLED`** seal in the session log.
- **Handover:** This certification is a **REQUIRED** prerequisite for the "Heuristic Pulse Audit" blocking gate in `close_workflow.md`. Failure to certify will result in a **FAILED_CONSTITUTIONAL_AUDIT** closure.

---
*Certified under Roadmap 013 - Refined Telemetry & Redundancy*
