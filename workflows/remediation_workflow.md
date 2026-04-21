---
description: "Emergency Rollback and Remediation Protocol (Keyword: remediation)"
version: 1.0.0
---

# 🛡️ Workflow: Remediation (The Panic Button)

A critical emergency protocol designed to intercept infinite hallucination loops, cascading logic failures, or Double-Gate stalemates. Its sole purpose is to nuke corrupted state, extract negative-heuristics natively, and return the system to safety without Human intervention.

## 0. Trigger Conditions (Automatic or Manual)
- **Automatic Invocation (Rule 67):** Triggered automatically by the `matrix_workflow.md` if the `QA Agent` or `Tester Agent` forcefully reject the exact same logic execution block **more than 3 consecutive times** (The Kill Switch).
- **Manual Invocation:** Triggered explicitly by the Human User detecting an Agent spinning out of context.

## 1. Deadlock Termination (The Kill Switch)
- **Immediate Execution Halt:** All active tactical design (`Orchestrator`) and physical implementations (`Executing Node`) are rigorously terminated. The `task_scope.md` is locked.
- **State Nuke:** The workspace is forcibly sanitized via `git restore . && git clean -fd`. The environment is returned identically to its Pre-Sprint pristine status.

## 2. Negative-Heuristic Extraction (The Post-Mortem)
- **Error Mining:** The terminal telemetry regarding WHY the cycle failed (e.g. Circular import, incorrect standard library assumption, syntax mismatch) is scraped from `memory/telemetry/raw_errors.json`.
- **Negative Knowledge Item (N-KI):** An explicit ephemeral file is created within the namespace memory (`/memory/[namespace]/ki_FAILED_...`).
- **Logic Tagging:** The N-KI explicitly logs: *"Attempting [X] with pattern [Y] systematically collapsed the Double-Gate review. DO NOT ATTEMPT THIS PATTERN AGAIN in current context."*

## 3. Sprint Rollback & Notification
- **Roadmap Tagging:** The active roadmap in `docs/active_state.json` is updated with a `BLOCKED: TERMINAL_REMEDIATION_LOOP` signature instead of `COMPLETED`.
- **Human Handshake:** The system must definitively alert the user: *"CRITICAL: Remediation Protocol was triggered. Deadlock achieved on execution. Negative-heuristic logged. Branch returned to zero-state. Awaiting strategic human pivot."*
- Exit and **SESSION LOCKED**.

---
*Optimized for Matrix V2 Failsafe Constraints*
