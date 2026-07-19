---
name: mass-standardizer
description: Batch-normalizes the flat skills/ arsenal — detects skills missing the Trinity Standard (README.md, SKILL.md, /scripts/) and injects the missing artifacts from templates, keeping manifest_skills.json in sync.
---

# Sub-Role Skill: Mass Standardizer

## Base Profile
**Name**: `mass-standardizer`
**Category**: Infrastructure / Automation
**Description**: Automotive engine for the batch normalization of the matrix arsenal following the `skill-creator` standard.

## Technical Logic
This skill implements a **Template-Driven Scaffolding** pattern. It scans the matrix for structural gaps (missing `README.md`, `SKILL.md`, or `/scripts/` folders) and surgically injects the required artifacts using institutional templates and manifest metadata.

## Procedures

### 1. Gap Analysis (Arsenal Audit)
- **Scanning**: Iterate through the flat `skills/` directory (and `profiles/*/skills/` when auditing profiles).
- **Detection**: Apply the dual Trinity Standard (`agents.md §3 trinity_standard`):
    - Every skill: `SKILL.md` with `name`/`description` frontmatter.
    - Executable skills (those shipping `/scripts/`): additionally `README.md` and `scripts/__init__.py`.

### 2. Context Extraction
- **Meta-Harvesting**: Read the corresponding entry in `manifest_skills.json` to extract the skill's official name, description, category, and tags.
- **Logic Mapping**: For `SKILL.md`, extract any existing procedural comments in the code to seed the "Technical Logic" section.

### 3. Template Injection
- **README Synthesis**: Apply the official `readme-standardizer/assets/template.md`.
- **SKILL Synthesis**: Generate the YAML frontmatter and standard sections (Base Profile, Cycles, Governance).
- **Structure Enforcement**: Instantiate the `/scripts/` directory and ensure a valid `__init__.py` exists for Python package compliance.

### 4. Manifest Synchronization
- **Strict Parity**: Verify that every standardized skill has its path, category, and tags correctly reflected in `manifest_skills.json`.

## Governance Audit
- **Jurisdiction**: This skill is exclusively operated by the **Skill Architect** or the **Orchestrator** during refactor phases.
- **Rule 1 Compliance**: All generated documents MUST be in Technical English and follow the kebab-case naming convention.
