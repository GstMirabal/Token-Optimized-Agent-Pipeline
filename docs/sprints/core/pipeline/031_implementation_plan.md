# ♟️ Implementation Plan: Sprint 031 - Refined Telemetry & Redundancy

## 🎯 Goal
Establish a "Heuristic Pulse" gate for session closures and implement a local redundancy mirror for the `active_state.json` to ensure high-integrity knowledge extraction and state recovery.

## 🧱 Components (Work Breakdown Structure)

### Component 1: Telemetry & Heuristic Pulse
- **Target**: `workflows/close_workflow.md`, `workflows/extract_workflow.md`, `memory/telemetry/`
- **Dependencies**: None.
- **Verification Gate**: `close_workflow.md` must contain an explicit mandatory human verification step for extracted KIs prior to physical commitment. The telemetry directory (`memory/telemetry/raw_errors.json`) must be formally structured.

### Component 2: Mirror Protocol (Redundancy)
- **Target**: `hooks/on_commit.py` or a dedicated state hook, `.agent_state/mirror.json`, `workflows/start_workflow.md`.
- **Dependencies**: None.
- **Verification Gate**: `start_workflow.md` must possess robust recovery logic via `.agent_state/mirror.json`, and state-changing events must physically sync the shadow copy.

### Component 3: Knowledge Consolidation
- **Target**: `memory/memory_index.json`
- **Dependencies**: None.
- **Verification Gate**: `memory_index.json` is audited, parsed, and defunct KI references removed to maintain amnesia integrity.

## 📋 Task Breakdown

| Task ID | Component | Description | Assignee Role | Status |
| :--- | :--- | :--- | :--- | :--- |
| `031-1` | Heuristic Pulse | Refactor `close_workflow.md` to add a specific user approval step for each generated KI prior to amnesia. | Orchestrator | COMPLETED |
| `031-2` | Telemetry Node | Consolidate the telemetry harvester in `memory/telemetry/raw_errors.json` via hook enhancements. | Orchestrator | COMPLETED |
| `031-3` | State Mirroring | Implement logic in `hooks/` to mirror `docs/active_state.json` into `.agent_state/mirror.json` on execution. | Orchestrator | COMPLETED |
| `031-4` | Recovery Logic | Audit and enhance `start_workflow.md` instructions for recovering corrupt `active_state.json` from the mirror. | Orchestrator | COMPLETED |
| `031-5` | Orphan Audit | Script or manually audit `memory_index.json` to prune defunct indices. | Governance Sentinel | COMPLETED |

## 🧪 Verification Plan
- Simulation of a missing `active_state.json` recovering from `.agent_state/mirror.json`.
- Manual inspection of `memory_index.json` to guarantee all specified IDs point to existing `.md` files in `memory/core/`.
- Review of `.agents/hooks/` execution paths to ensure the mirror is synchronized.
