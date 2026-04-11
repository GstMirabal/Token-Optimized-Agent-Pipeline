---
description: "Knowledge Extractor and Intelligence Distillation Protocol (V 3.1.0)"
version: 3.1.0
---

# 🧠 Workflow: Knowledge Extractor & Intelligence Distillation

Master protocol for heuristic extraction, Matrix memory update, and ephemeral state purge before session destruction.

## 1. Phase 1: Brain Drain & Forensic Audit
Retrospectively audit the session logs to identify high-value intelligence:
- **Normal Close:** Scan the current session's terminal outputs and implementation logs.
- **Forensic Mode:** If orphaned `docs/sprints/` folders are found at session-start, the agent MUST perform an emergency extraction scan of the remaining assets.
- **Targets:** Exotic workarounds (e.g., environment-specific library hangs), non-obvious logic bug-fixes, and strategic orchestration heuristics.

## 2. Phase 2: Knowledge Hardening & Redundancy Filter (Rule 74 Pt 4)
Filter the distilled intelligence to maintain context-density:
- **Agnostic Validation:** Knowledge MUST be transferable and project-independent (Rule 34).
- **Rule Synchronization:** Compare the finding against **Global Rules (1-78)**. If the lesson is already codified in governance, the extraction project for this item is **ABORTED** to prevent redundant noise.
- **PII Shielding:** Ensure absolute sanitization of secrets, credentials, and user data.

## 3. Phase 3: Domain-Based Indexing (Rule 75)
Persist the knowledge in a structured and scalable format:
- **Domain Persistence:** Save the item into its categorical subfolder (e.g., `knowledge/crypto/ki_{ID}_{name}.md`).
- **Semantic Update:** Perform an atomic update of `.agents/knowledge/ki_index.json` with 1-line metadata including description and tags.

## 4. Phase 4: Amnesia Certification & Handover
Formal conclusion of the intelligence lifecycle:
- **Signature:** Issue the **`EXTRACTION_COMPLETE: INTELLIGENCE_DESTILLED`** seal in the session log.
- **Handover:** This certification authorizes the transition to physical state destruction (Amnesia) in the session closing workflow.

---
*Certified under Roadmap 008 - Matrix Strategic Intelligence*
