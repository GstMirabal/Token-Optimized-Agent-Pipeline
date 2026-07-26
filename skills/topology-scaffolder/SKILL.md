---
name: topology-scaffolder
description: Scaffolds the mandatory docs/ tree (roadmaps, sprints, architecture, contracts) and keeps active_state.json's Documentation Entry Point topology in sync. The only skill authorized to physically write project topology, on behalf of the Topology Mapper agent.
---

# 🛠️ Local Skill: Topology Scaffolder (v1.0.0)

## Domain
- **Category:** Architecture / Scaffolding / State Tracking
- **Origin:** Custom synthesis for automated project topology initialization.
- **Status:** `ACTIVE_LOCAL`
- **Sovereignty:** `local` (Project-Specific)

## Technical Logic
This skill provides the **Blueprint Engine** for the framework. It handles the structural injection of the mandatory `/docs/` tree and the surgical synchronization of the "Documentation Entry Point" (`active_state.json`) to ensure total project traceability.

## Procedures

### 1. Mandatory Tree Injection (Hook Protocol)
- **Scaffolding Logic**: Automatically creates the directory hierarchy:
  - `/docs/roadmaps/[layer]/[app]/`
  - `/docs/sprints/[layer]/[app]/`
  - `/docs/architecture/`
  - `/docs/walkthroughs/`
  - `/docs/contracts/`
- **Sovereignty**: Overwrites or migrates legacy documentation structures to comply with the `.agents` standard.

### 2. State Synchronization (Coordinate Tracking)
- **Documentation Entry Point Update**: Surgically modifies `active_state.json` to update:
  - `active_layer`: Current focus of the pipeline.
  - `active_app`: Target application under development.
  - `current_sprint_id`: The authoritative ID for the active session.

### 3. ASCII Infrastructure Mapping
- **Render Engine**: Generates high-fidelity directory trees using ASCII characters.
- **Constraint**: Must avoid Mermaid for folder structures to prevent rendering collapse in complex trees.
- **Optimization**: Minimalist output to preserve token space while maintaining visual clarity.

## Governance Audit
- **Blueprint Policy:** Only the `Topology Mapper` agent is authorized to invoke this skill's write procedures.
- **Language Guard:** All structural labels and state metadata MUST be in Technical English.
