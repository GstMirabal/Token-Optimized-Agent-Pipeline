---
description: "Standardized Hierarchy Alignment Protocol (SHAP)"
version: 2.0.0
---

# 🛡️ Workflow: Standardization (Alineación)

Governance protocol to enforce structural sovereignty and linguistic purity across the project.

## 0. Trigger Conditions
- **Missing Hierarchy**: If `docs/architecture/` or `docs/contracts/` are absent during session start.
- **Polluted Root**: If technical docs are found in the root of `/docs/` instead of their categorized domains.
- **Unstructured Naming**: If docs inside `docs/sprints/` or `docs/roadmaps/` are found lacking the strict `[layer]/[app]/` hierarchy dictation.
- **Linguistic Drift**: If non-English terms are detected in strategic artifacts.

## 1. Structural Scaffolding (@matrix_mapper)
1. **Instantiate Standard Tree**:
    - `mkdir -p docs/architecture docs/contracts docs/roadmaps docs/sprints`
2. **Purify Root**:
    - Move all loose `.md` and `.yml` files in the root of `/docs/` to their respective domains (Architecture/Contracts).

## 2. Technical Purification (@doc_orchestrator)
1. **Linguistic Sovereignty (Rule #1)**:
    - Auditor MUST convert all residuary Spanish text to **Technical English**.
2. **Nomenclature Refactoring (Matrix V2)**:
    - Automatically route flat files in `docs/sprints/` into the `[layer]/[app]/` physical mapping.
3. **Structural Formatting (Rule #3)**:
    - Auditor MUST convert all bulleted lists of variables, models, or endpoints into **Markdown Tables**.
4. **Topological Map**:
    - Update `docs/architecture/matrix_topology_map.md` and generate `global_topology.md` (Mermaid).

## 3. State Certification
- Update `docs/active_state.json` with the latest metadata.

---
*Certified by the Matrix Council - Protocol 0xSHAP-V2*
