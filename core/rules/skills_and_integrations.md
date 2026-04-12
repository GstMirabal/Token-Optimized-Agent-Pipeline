# Rule Context: Skills and Integrations

This document asserts the governance laws when researching, registering, or escalating new operational tools or libraries within the host project.

## 1. Skill Discovery Escalation 
Agents requiring functions not natively available in standard language libraries must strictly follow this search protocol:
- **Priority 1 (Manifest Check)**: Query `skills/manifest.json` locally to check if a previously approved script exists.
- **Priority 2 (The Local Bridge)**: Evaluate the locally downloaded bridge `skills/3rd/autoskills/` before going outside the workspace.
- **Priority 3 (External Discovery)**: If local tools fail, agents must query `https://skills.sh/`. Explicit human authorization under technical debate is mandatory before registering any new external elements.

## 2. Contamination Safeguards
- **Prohibited Installations**: Utilizing volatile dependency bridges at the root (e.g., executing `npx -y` outside isolated environments) is radically **PROHIBITED** to preserve deterministic operations and prevent root contamination. 
- **Domain Coupling Constraint**: If an introduced skill strictly serves the current project and not the entire global `.agents` capability matrix, it must permanently reside walled inside the local `/.local_skills/` directory.

## 3. Third-party Immutability
- **Skill Documentation Veto**: Modifying, standardizing, or refactoring native README files or technical specifications of an imported skill living in `skills/3rd/` is strictly prohibited. The upstream integrity of vendor technical instructions must remain completely virgin.
