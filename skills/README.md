# 🛠️ AI AI-Ops Skills Matrix

This directory contains the universal tactical arsenal of **Universal-Agents**. These are autonomous or semi-autonomous tools designed to be invoked by the **Orchestrator** to solve specific engineering problems.

## 🧬 The Triangle of Sovereignty (Topological Governance)

To maintain order and security, all skills are strictly divided into three distinct layers:

1.  **`core/` (The Kernel):** Foundational skills that define the agent framework and infrastructure (e.g., `skill-creator`, `token-saver`). Essential for matrix stability.
2.  **`local/` (Sovereignty Propia):** Custom tools synthesized specifically for this project or domain (e.g., `contract-writer`). These are internally developed/owned.
3.  **`3rd/` (External Arsenal):** Downloaded or 3rd-party tools (e.g., `autoskills`, `django-expert`). Use for specialized external expertise.

## 📋 The Manifest (Dynamic Discovery)

To minimize token consumption and reduce discovery time (Zero-Scanning Policy), the framework uses **`manifest_skills.json`** as the single source of truth.

The Orchestrator and the **Skill Architect** query this manifest FIRST to identify capability, category, and tactical tags.

> [!IMPORTANT]
> **Subagents are FORBIDDEN** from scanning directories recursively to look for scripts. They must reference the manifest to ensure they are using the sanctioned "Armory".

## 🚀 Adding New Skills

1.  **Jurisdiction:** New skills must be sanctioned by the [Skill Architect](../agents/skill_architect.md).
2.  **Synthesis:** Use the `skill-creator` workflow to automate the boilerplate (Rule 71).
3.  **Registration:** Every new skill **MANDATORY** must be registered in `manifest_skills.json` with a clear description, correct path, and relevant tags.

Every tool must comply with **Rule 1** (Python PEP 8 / JS camelCase) and provide structural documentation via JSDoc or Google Style docstrings.
