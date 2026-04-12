---
description: "Standardized Hierarchy Alignment Protocol (SHAP)"
version: 1.0.0
---

# 🛡️ Workflow: Standardization (Alineación)

Governance protocol to enforce structural sovereignty and linguistic purity across the project.

## 0. Trigger Conditions
- **Missing Hierarchy**: If `docs/architecture/` or `docs/contracts/` are absent during session start.
- **Polluted Root**: If technical docs are found in the root of `/docs/` instead of their categorized domains.
- **Linguistic Drift**: If non-English terms are detected in strategic artifacts.

## 1. Structural Scaffolding (@matrix_mapper)
1. **Instantiate Standard Tree**:
    - `mkdir -p docs/architecture docs/contracts docs/roadmaps docs/sprints`
2. **Transfer Logic (Submodule Migration)**:
    - Transfer `task/` content from `.agents/` to root `docs/` (matching subfolders).
3. **Purify Root**:
    - Move all loose `.md` and `.yml` files in the root of `/docs/` to their respective domains (Architecture/Contracts).

## 2. Technical Purification (@doc_orchestrator)
1. **Linguistic Sovereignty (Rule #1)**:
    - Auditor MUST convert all residuary Spanish text to **Technical English**.
2. **Structural Formatting (Rule #3)**:
    - Auditor MUST convert all bulleted lists of variables, models, or endpoints into **Markdown Tables**.
3. **Topological Map**:
    - Update `docs/architecture/MATRIX_TOPOLOGY_MAP.md` and generate `global_topology.md` (Mermaid).

## 3. State Certification
- Update `docs/active_state.json` with the latest metadata.
- Re-index `docs/MASTER_INDEX.md`.

---
*Certified by the Matrix Council - Protocol 0xSHAP-V1*
