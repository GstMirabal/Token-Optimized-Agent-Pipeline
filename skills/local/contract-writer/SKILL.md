# 🛠️ Local Skill: Contract Writer (v1.0.0)

## Domain
- **Category:** Documentation / Reverse Engineering
- **Origin:** Custom synthesis for AI-driven API contract generation.
- **Status:** `ACTIVE_LOCAL`

## Technical Logic
This skill provides the procedural protocol for **Documentary Reverse Engineering**. It enables a subagent to extract structured technical agreements (I/O, Payloads, Auth) directly from operated code files (`.py`, `.ts`, `.go`, etc.) without human intervention.

## Procedures

### 1. Payload Synthesis
- **Logic Extraction**: The agent must identify data classes (Pydantic, Interfaces, JSDoc) to reconstruct JSON request/response bodies.
- **Schema Mapping**: Map nested objects to flat Markdown descriptions for LLM readability.

### 2. Interface Normalization
- **Metadata Harvesting**: Extract Headers, Query Parameters, and HTTP Status Codes from the implementation logic.
- **Contract Format**: Force output into standardized Markdown tables:
  | Field | Type | Required | Description |
  | :--- | :--- | :--- | :--- |

### 3. Topological Sync
- **Diagram Alignment**: Ensure that any endpoint or service described in a contract is also reflected in the `global_topology.md` using Mermaid.

## Governance Audit
- **Compliance Rule:** No manual contract writing is allowed; all `.md` contracts must be generated using this protocol to ensure 1:1 parity with the codebase.
- **Language Isolation**: All generated documentation MUST be in Technical English.
