---
description: "Knowledge Extractor and Intelligence Distillation Protocol (V 4.0.0)"
version: 4.0.0
---

# 🧠 Workflow: Extract (Intelligence Distillation)

Master protocol for heuristic extraction, Matrix memory index updating, and ephemeral state management.

## 1. Forensic & Brain Drain Auditing
Retrospectively audit the session logs and telemetry nodes to identify high-value operational intelligence.
- **Normal Execution:** Scan the terminal outputs, debugging phases, and logic trails from the current session.
- **Telemetry Scan:** Interrogate paths like `memory/telemetry/raw_errors.json` to detect repeating logic friction points identified during the QA/Tester Remediation Loops.
- **Forensic Execution:** If orchestrated to scan from an aborted state (e.g., Collision Guard activation), rigorously analyze context via `.agent_state/mirror.json` to isolate the conflict origin.

## 2. Knowledge Hardening (Jurisprudence Loop)
To maintain pure context-density, intelligence MUST be vetted before serialization:
- **Agnostic Validation:** Isolated facts or specific variable names must NOT be stored. Generated intelligence must be abstract, strategic, or systemic.
- **Constitutional Cross-Check:** The generated insight MUST NOT already exist within `agents.md` governance or existing KIs. Duplicate patterns are automatically rejected.
- **Sovereign Shielding:** Immediate masking and purge of PII, API tokens, or physical host machine paths in the generated insights.

## 3. Topographical Index Integration
Knowledge artifacts must be systematically merged into the matrix.
- **Categorical Siloing:** Physical generation of the markdown artifact (`ki_xxx_name.md`) into its localized sub-layer inside `/memory/` (e.g. `/memory/cryptobot/ki_...`).
- **Semantic Descriptor:** Execute a 1-line metadata update inside the corresponding `memory/[namespace]/memory_index.json` bounding the new ID, summary, and its exact localized path.

## 4. Handover & Amnesia Certification
The intelligence generated must endure the Constitutional Handshake:
- **Approval Gate:** The intelligence queue generated here MUST be returned to the logic flow of `close_workflow.md` and await explicit user approval (The Extraction Handshake) before formal index commitment.
- **Completion Seal:** The seal `EXTRACTION_COMPLETE: INTELLIGENCE_DESTILLED` will only be logged following human sign-off.

---
*Optimized for Matrix V2 Memory Management (v4.0.0).*
