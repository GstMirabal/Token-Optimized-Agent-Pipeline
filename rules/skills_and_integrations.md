# Rule Context: Skills and Integrations

This document asserts the governance laws when researching, registering, or escalating new operational tools or libraries within the host project.

## 1. Skill Discovery Escalation 
Agents requiring functions not natively available in standard language libraries must strictly follow this search protocol:
- **Priority 1 (Manifest Check)**: Query `skills/manifest_skills.json` locally to check if a previously approved script exists.
- **Priority 2 (The Local Bridge)**: Evaluate the locally downloaded bridge `skills/autoskills-3rd/` before going outside the workspace.
- **Priority 3 (External Discovery)**: If local tools fail, agents must query `https://skills.sh/`. Explicit human authorization under technical debate is mandatory before registering any new external elements.
- **Priority 4 (Creation Protocol)**: If the required function is fundamentally untraceable across the first three steps, the `Skill Architect` MUST forge the skill under the dual **Trinity Standard**, choosing the destination per `skill_forge_workflow.md` (`forge_destination`): host `.claude/skills/` for project-specific tools (default), `profiles/[name]/skills/` for project-family tools, or the flat `.agents/skills/` for framework-wide tools — the latter two only through the nucleus branch→PR→tag flow.

## 2. Contamination Safeguards
- **Prohibited Installations**: Utilizing volatile dependency bridges at the root (e.g., executing `npx -y` outside isolated environments) is radically **PROHIBITED** to preserve deterministic operations and prevent root contamination. 
- **Domain Coupling Constraint**: If an introduced skill strictly serves the current project and not the entire global `.agents` capability matrix, it must permanently reside mapped directly inside the unified `skills/` directory, rejecting any sub-folder grouping or `/.local_skills/` unstandardized folders.

## 3. Third-party Immutability & Topology
- **Nomenclature Mandate**: Any third-party tool, vendor library, or external fork imported into the Arsenal MUST be explicitly identifiable via the `-3rd` string suffix appended to its directory name (e.g., `django-expert-3rd`).
- **Skill Documentation Veto**: Modifying, standardizing, or refactoring native README files or technical specifications of an imported external skill living in `skills/` is strictly prohibited. The upstream integrity of vendor technical instructions must remain completely virgin.
