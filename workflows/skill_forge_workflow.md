---
description: "Arsenal Constructor and Skill Forge Protocol (Keyword: forge)"
version: 1.0.0
---

# 🛡️ Workflow: Skill Forge (The Quartermaster)

An isolated, specialized protocol exclusively designed for manufacturing, benchmarking, and registering native Matrix tools into the `skills/` flat arsenal, completely decoupled from business operations logic.

## 0. Jurisdictional Isolation
- **Role Isolation:** The **[Skill Architect](../agents/skill_architect.md)** leads this operation, paired strictly with the **[Tester Agent](../agents/tester_agent.md)**.
- **Prohibition:** No modifications to the host application's backend or frontend code are permitted in this cycle.

## 1. Specification & Scaffolding
- **Blueprint Mapping:** The `Skill Architect` defines the exact `I/O payload` and terminal signature of the required tool.
- **Trinity Generation:** Create exactly 1 directory inside `skills/[tool_name]/`. Generate the strict structural trifecta: `README.md`, `SKILL.md` (YAML Frontmatter), and the `scripts/` folder containing the executable logic.

## 2. Sterile Development & Benchmarking
- **Executable Construction:** The core Python/Bash/JS files are fleshed out with deterministic logic. Use of global OS modules is barred; all dependencies must be locally bounded.
- **Double-Gate Bypass Test:** The `Tester Agent` receives the script and executes an isolated smoke-test inside `/tmp/` or using `sqlite:///:memory:` contexts. The script MUST return `exit code 0` to proceed.

## 3. Matrix Registration & Manifest Update
- **Manifest Injection:** Automatically update the root `skills/manifest_skills.json` or `mcp-config.json` registering the new tool, its exact path, and capabilities array.
- **Golden Gate Handshake:** Explicitly prompt the user: *"Do you authorize the formal baptism and integration of this tool into the Matrix Arsenal?"*

## 4. Closure & Amnesty
- **Execution:** End the process. No `close_workflow.md` telemetry extraction is strictly required unless the forging process crashed.
- **SESSION LOCKED**.

---
*Optimized for Deterministic Arsenal Expansion*
