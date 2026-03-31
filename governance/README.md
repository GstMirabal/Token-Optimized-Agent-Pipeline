# ⚖️ Universal-Agents Governance (LTM Constitution)

This directory contains the **Permanent Thinking Rules** (Long-Term Memory) of the Universal-Agents framework. These files define the behavioral and architectural boundaries that all AI agents MUST respect.

## 📁 Core Governance Components

| Component | Purpose | Use Case |
| :--- | :--- | :--- |
| **`global_user_rules.md`** | **The Constitution**: Standards for coding, naming, security, and token efficiency. | Mandatory for EVERY session initialization. |
| **`subagents_architecture.md`** | **The Operational Manual**: Defines the 6-Step Hierarchy (Mentor > Orchestrator > Auditor...). | Defines HOW subagents are deployed and rolled back. |
| **`agents_roadmap.md`** | **The Strategy**: Step-by-step master roadmap for configuring any repository. | Used to track structural configuration phases. |
| **`project_mapping_and_context.md`**| **The Topology**: Records the physical boundaries (Src-Layout, Docker, etc.). | Prevents agents from scanning the entire OS. |

## 🛡️ Zero-Trust Design Policy

*   **Immutable Metadata:** These files are Read-Only for standard tactical subagents. Only the **Constitutional Agent** has write permissions to modify global rules.
*   **Audit Exclusion:** Governance files are markdown-based and excluded from automated code linters to prevent API waste.

## 🚀 How to use this directory

When starting a new project or context window, the AI Orchestrator uses these files to "bootstrap" its reasoning. If a conflict arises between a specific user request and these rules, the framework defaults to the **Constitutional Supremacy** defined in `global_user_rules.md`.

Use the `/certification_audit` workflow to verify if a project adheres to these strategic standards.
