# Knowledge Item: KI-026 - Standardized Hierarchy Parity

## 📍 Summary
Establishment of the mandatory standardized documentation hierarchy within the root `/docs/` directory and the migration of the governance `task/` ecosystem from the `.agents` submodule to the parent project.

## 🏛️ Context
Previously, documentation and task tracking were fragmented between the submodule and the root `/docs/` folder, often leading to "Sovereignty Divergence" (Rule #36). This protocol consolidates the "Technical Bible" in the project root while maintaining the submodule as a pure governance engine.

## 🛡️ Implementation Rules
1. **Directory Guardianship**:
    - **Architecture**: `docs/architecture/` stores topology maps, flows, and blueprints.
    - **Contracts**: `docs/contracts/` stores API specifications and data model overviews.
    - **Governance**: `docs/roadmaps/` and `docs/sprints/` store the operational history.
2. **Linguistic Sovereignty**:
    - All files MUST adhere to **Technical English** (Rule #1).
3. **Trigger Gate**:
    - The `start_workflow.md` now includes a mandatory check for this hierarchy, triggering the `standardization_workflow.md` if drift is detected.

## ✅ Verification
- **Command**: `ls -R docs/`
- **Expected**: Absence of loose `.md` files in the root of `/docs/` and existence of standardized sub-folders.

---
*Added during Sprint 026 - Audit of Structural Sovereignty.*
