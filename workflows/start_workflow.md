---
description: "Session-Start Protocol (Keyword: start)"
version: 5.0.0
---

# 🛡️ Workflow: Start (Matrix Initiation V2)

Master entry protocol optimized to minimize token consumption and strictly invoke the execution pipeline.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Amnestic Anchor** | `read_anchor` | Subagents MUST initialize with **Zero-Memory**. The absolute first operation is to extract the topology map from `docs/active_state.json`. |
| **0. Amnestic Anchor** | `read_constitution` | Immediately after the anchor, read `agents.md` to adopt current governance. |
| **1. Collision Guard** | `habitability_check` | Abort if `IN_PROGRESS` exists with a different session UID. Initialization is PROHIBITED if the workspace is the `.agents` nucleus. |
| **1. Collision Guard** | `lightweight_sync` | Perform a lightweight git check (`git fetch` & `git status`) on both project and submodule to ensure no remote drift. Do NOT perform heavy topology scans. |
| **2. Legacy Onboarding** | `audit_trigger` | If a mature project exists without Matrix topology, hand off to `Orchestrator` to execute `legacy_onboarding` (Sprint 0). |
| **3. Pipeline Handoff** | `matrix_invocation` | If constitution and state are validated, explicitly hand command to the `Principal Agent` to initiate Phase 0 of the Core Workflow. |

---
*Optimized for Matrix V2 Chain of Command (v5.0.0).*
