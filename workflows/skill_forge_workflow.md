---
description: "Arsenal Constructor and Skill Forge Protocol (Keyword: forge)"
version: 2.0.0
---

# 🛡️ Workflow: Skill Forge (The Quartermaster)

An isolated protocol for manufacturing, benchmarking, and registering native tools into the `skills/` flat arsenal.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Isolation** | `role_lock` | Led by `Skill Architect` and `Tester Agent`. No app code modifications allowed. |
| **0. Isolation** | `forge_destination` | Choose where the skill lives BEFORE scaffolding: **(a) host-only** → forge directly in the host's `.claude/skills/` (native discovery, no submodule change — default for project-specific tools); **(b) project-family** → `.agents/profiles/[name]/skills/` (requires the nucleus PR flow); **(c) framework-wide** → `.agents/skills/` (nucleus PR flow + new tag; hosts receive it via pin update). Options (b)/(c) modify the submodule and are PROHIBITED from a host session without going through the nucleus branch→PR→tag pipeline (`strict_rule`). |
| **1. Scaffolding** | `blueprint` | Define exact I/O payload. Generate the (dual) Trinity Standard: `SKILL.md` with `name`/`description` frontmatter always; `README.md` + `scripts/` with `__init__.py` if executable. |
| **2. Benchmarking**| `sterile_dev` | Develop deterministic logic locally bounded. No global OS modules. |
| **2. Benchmarking**| `skillopt_run` | Optimize new `SKILL.md` via `train_runner.py` (requires explicit authorization). |
| **2. Benchmarking**| `smoke_test` | `Tester Agent` executes isolated test in `/tmp/` or `:memory:`. Must return exit code 0. |
| **3. Registration**| `manifest_update` | For framework-wide skills: run `python3 .agents/skills/mass-standardizer/scripts/generate_manifest.py` — `manifest_skills.json` is **generated from SKILL.md frontmatter, never hand-edited** (CI enforces this). MCP servers register in `.agents/claude/mcp.json` (or the profile's `mcp/registry.json`). Host-only skills need no registration: Claude Code discovers them natively from `.claude/skills/`. |
| **4. Golden Gate** | `authorization` | Explicitly prompt human: *"Do you authorize the formal integration of this tool?"* |

---
*Optimized for Matrix V2 Deterministic Expansion & Tabular Density (v2.0.0).*
