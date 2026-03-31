# 🛠️ AI AI-Ops Skills Matrix

This directory contains the universal tactical arsenal of **Universal-Agents**. These are autonomous or semi-autonomous tools designed to be invoked by the **Orchestrator** to solve specific engineering problems.

## 📋 The Manifest (Dynamic Discovery)

To minimize token consumption and reduce discovery time (Zero-Scanning Policy), the framework uses a **`manifest.json`** file. 

The Orchestrator queries this manifest FIRST to identify:
1.  **Capability:** What each skill can actually do.
2.  **Category:** Security, Efficiency, QA, etc.
3.  **Tags:** Technical keywords for quick routing.

> [!IMPORTANT]
> **Subagents are FORBIDDEN** from scanning directories recursiveley to look for scripts. They must reference the manifest as the source of truth for tool availability.

## 🧬 Skill Structure

Each skill in this matrix follows a strict protocol:
*   **Documentation:** Every script must include *Google Style Docstrings* or *JSDoc*.
*   **Atomic Logic:** Each tool should solve ONE specific part of the engineering lifecycle (e.g., just the AST extraction, or just the security audit).
*   **Zero-Trust Output:** Tools must only return structural data or sanitized tracebacks (short-tb).

## 🚀 Adding New Skills

1.  Create a folder with a descriptive name (e.g., `3rd-rust-auditor`).
2.  Add your tactical scripts in `/scripts/`.
3.  **MANDATORY:** Register the new skill in the `manifest.json` with a clear description and tags.

Use the `/skill_creator` workflow to automate this process and ensure compliance with governance standards.
