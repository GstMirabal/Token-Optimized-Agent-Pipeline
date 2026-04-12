# 📄 Contract: Doc Orchestrator Interface (doc_orch_01)

This contract defines the technical interface and I/O expectations for the **Doc Orchestrator** agent. It standardizes the documentary reverse engineering and topological mapping process.

| Phase | Input | Action | Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Audit** | `agents.md` | Compliance Review | Audit Report | MANDATORY |
| **Reverse Eng.** | Source Code | `contract-writer` | `docs/contracts/` | MANDATORY |
| **Topography** | Infrastr. Logic | Mermaid Diagrams | `global_topology.md` | MANDATORY |
| **Manifesting** | Inventory Map | Data Aggregation | `PROJECT_MANIFEST.md` | OPTIONAL |

## 1. Documentation Standards

| Specification | Mandatory Format | Restriction |
| :--- | :--- | :--- |
| **Topologies** | `Mermaid` (flowchart) | Prohibited in contracts. |
| **Contracts** | `Markdown Tables` | Prohibited Mermaid/JSON. |
| **Language** | Technical English | No Spanish allowed. |

## 2. Interface Definitions (Markdown Tables)
All service-level or agent-level interfaces MUST be mapped using the internal Markdown Table standard:
- **Columns**: `Field`, `Type`, `Required`, `Description`.
- **Constraint**: Must be mechanically parsable by following subagents.
