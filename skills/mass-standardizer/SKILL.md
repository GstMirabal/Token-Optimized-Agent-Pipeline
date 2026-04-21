# Sub-Role Skill: Mass Standardizer

## Base Profile
**Name**: `mass-standardizer`
**Category**: Infrastructure / Automation
**Description**: Automotive engine for the batch normalization of the matrix arsenal following the `skill-creator` standard.

## Technical Logic
This skill implements a **Template-Driven Scaffolding** pattern. It scans the matrix for structural gaps (missing `README.md`, `SKILL.md`, or `/scripts/` folders) and surgically injects the required artifacts using institutional templates and manifest metadata.

## Procedures

### 1. Gap Analysis (Arsenal Audit)
- **Scanning**: Iterate through `core/` and `local/` directories.
- **Detection**: Identify folders that lack the mandatory "Trinity":
    - `README.md`
    - `SKILL.md`
    - `/scripts/` folder + `__init__.py`

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
