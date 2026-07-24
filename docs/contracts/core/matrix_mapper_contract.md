# 📄 Contract: Matrix Mapper Interface (mtx_mapper_01)

This contract defines the technical interface and I/O expectations for the **Matrix Mapper** agent. It standardizes the scaffolding and state-synchronization handover.

| Phase | Input | Action | Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Initiation** | `agents.md` | Constitutional Audit | Alignment Signature | MANDATORY |
| **Scaffolding** | Root Path | `topology-scaffolder` | `/docs/` Tree | MANDATORY |
| **Sovereignty** | Legacy Docs | Homologation | Optimized History | OPTIONAL |
| **Anchoring** | Session Metadata | JSON Injection | `active_state.json` | MANDATORY |

## 1. Zero Coordinate Payload (active_state.json)

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `active_layer` | String | Yes | The current functional tier of the Matrix. |
| `active_app` | String | Yes | The target application under development. |
| `current_sprint_id` | String | Yes | Authoritative ID of the active sprint. |
| `session_id` | String | Yes | Unique UID of the active interaction. |
| `status` | Enum | Yes | `ACTIVE`, `IN_PROGRESS`, `CLOSED_SUCCESSFULLY`. |

**Extensibility guarantee**: this table is not exhaustive. Root keys not listed here — e.g. `code_containers`, `adr_autoescalate_triggers` (`rules/documentation_standard.md §2.1`/`§3.2`) — are valid and MUST be preserved by any writer of this file. A writer that parses this JSON and re-serializes only the fields it recognizes silently drops unknown keys; verified as of this rule's introduction that `hooks/state_mirror.py` is a byte-for-byte file copy (safe by construction, never re-serializes), but any *future* writer that reconstructs the JSON must round-trip unknown keys through unchanged.

## 2. Structural Signatures
The Matrix Mapper MUST issue a high-fidelity signature in the `matrix_topology_map.md` to trigger the **Discovery Lock (Sync-Lock)**.
- **Format**: `ef3c429d-matrix-v3.0-verified`
- **Constraint**: No other subagent is authorized to modify this signature.
