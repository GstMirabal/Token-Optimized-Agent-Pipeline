---
description: "Emergency Rollback and Remediation Protocol (Keyword: remediation)"
version: 2.0.0
---

# 🛡️ Workflow: Remediation (The Panic Button)

A critical emergency protocol designed to intercept infinite hallucination loops or Double-Gate stalemates. Its sole purpose is to nuke corrupted state, extract negative-heuristics natively, and return the system to safety.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Trigger** | `auto_invocation`| Triggered automatically if QA or Tester forcefully reject the exact same logic block **>3 consecutive times**. |
| **1. Deadlock Term**| `state_nuke` | Immediate execution halt. Workspace is forcibly sanitized (`git restore . && git clean -fd`) to Pre-Sprint pristine status. |
| **2. Extraction** | `error_mining` | Scrape telemetry for the failure origin (e.g. Circular import, syntax mismatch). |
| **2. Extraction** | `negative_ki` | Inject logic tag into `agents.md` via `Governance Learner` banning the failed pattern. No memory logs are kept. |
| **3. Rollback** | `roadmap_tag` | Update `docs/active_state.json` with `BLOCKED: TERMINAL_REMEDIATION_LOOP`. |
| **3. Rollback** | `session_lock` | Explicitly alert human user of deadlock. Exit and enforce **SESSION LOCKED**. |

---
*Optimized for Matrix V2 Failsafe Constraints & Tabular Density (v2.0.0).*
