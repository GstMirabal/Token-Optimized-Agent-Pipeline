# KI-014: Unified State Architecture and Path Integrity

## Status
- **ID:** ki-014
- **Domain:** utility
- **Tactical Logic:** Centralization and Topology Enforcement (Rule 23, 52).
- **Rule Origin:** Phase 8 Refactoring (S009).

## The Problem
Fragmented session metadata across multiple directories (e.g., `state/` and `.agent_state/`) leads to "Topological Drift," where workflows reference non-authorized paths. This blocks efficient discovery and increases token consumption during recursive path scans.

## The Heuristic (Protocol)
1. **Mandatory Centralization:** All ephemeral session metadata (`session_metadata.json`) and context caches (`context.md`) MUST be unified in the `.agent_state/` HIDDEN directory.
2. **Directory Deletion:** Any non-authorized folder (like `state/`) used for persistence must be physically purged once its content is migrated to the authoritative cache (Rule 52).
3. **Workflow Sync:** All session-entry and close protocols MUST be updated atomically to ensure path integrity across the framework.

## Verification
- Confirm that `.agents/state/` no longer exists.
- Verify `start_workflow.md` points to `.agents/.agent_state/session_metadata.json`.

## Implementation History
- **Case #35d5e5a9:** Migration of legacy `state/` metadata to `.agent_state/` resolved structural drift and unified the LTM architecture for the Hardened Matrix.
