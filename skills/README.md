# 🛠️ AI-Ops Skills Library

This directory contains the skill library of the **Token-Optimized Agent Pipeline**. These are autonomous or semi-autonomous tools designed to be invoked by the **Orchestrator** to solve specific engineering problems.

## 🧬 Flat Topology (Topological Governance)

To maintain order and security, `skills/` is strictly flat — no `core/`, `local/`, or `3rd/` sub-layers are permitted (`agents.md §3 topological_order`). Every skill is a top-level directory, and provenance is encoded in the directory name itself, not in nesting:

1.  **Native skills** (e.g. `skill-creator`, `token-saver-auditor`, `contract-writer`): internally developed and owned by this framework, named without a suffix.
2.  **Third-party skills** (e.g. `autoskills-3rd`, `django-expert-3rd`): downloaded or vendored tools, explicitly marked with the `-3rd` directory-name suffix. Their documentation is vendor content and is not edited by this framework's own standardization tooling (`rules/skills_and_integrations.md §3`).

Project-specific packs — as opposed to these framework-wide skills — live under `profiles/[name]/skills/` and are only linked into a host via `--profile [name]`.

## 📋 The Manifest (Dynamic Discovery)

To minimize token consumption and reduce discovery time (Zero-Scanning Policy), the framework uses **`manifest_skills.json`** as the single source of truth.

The Orchestrator and the **Skill Architect** query this manifest FIRST to identify capability, category, and relevant tags.

> [!IMPORTANT]
> **Subagents are FORBIDDEN** from scanning directories recursively to look for scripts. They must reference the manifest to ensure they are using the sanctioned skill library.

## 🚀 Adding New Skills

1.  **Jurisdiction:** New skills must be sanctioned by the [Skill Architect](../agents/skill_architect.md).
2.  **Synthesis:** Use the `skill-creator` workflow to automate the boilerplate (Rule 71).
3.  **Registration:** Every new skill **MANDATORY** must be registered in `manifest_skills.json` with a clear description, correct path, and relevant tags.

Every tool must comply with **Rule 1** (Python PEP 8 / JS camelCase) and provide structural documentation via JSDoc or Google Style docstrings.
