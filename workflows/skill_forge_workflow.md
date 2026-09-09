---
description: "Skill Registration Protocol (Keyword: forge)"
version: 2.0.0
invoked_by: human:/agents:skill-forge, rules/skills_and_integrations.md
---

# 🛡️ Workflow: Skill Forge (Tool Registration)

An isolated protocol for manufacturing, benchmarking, and registering native tools into the `skills/` flat skill library.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Isolation** | `role_lock` | Led by `Skill Architect` and `Tester Agent`. No app code modifications allowed. |
| **0. Isolation** | `forge_destination` | Choose where the skill lives BEFORE scaffolding: **(a) host-only** → forge directly in the host's `.claude/skills/` (native discovery, no submodule change — default for project-specific tools); **(b) project-family** → for a real project, the host-controlled profile path installed with `scripts/install.py --profile-path <path>` (`RA-15`, Sprint 028); `.agents/profiles/[name]/skills/` inside the public nucleus is for **illustrative packs only** and still requires the nucleus PR flow; **(c) framework-wide** → `.agents/skills/` (nucleus PR flow + new tag; hosts receive it via pin update). Options (b)/(c) that modify the submodule are PROHIBITED from a host session without going through the nucleus branch→PR→tag pipeline (`strict_rule`). |
| **1. Scaffolding** | `blueprint` | Define exact I/O payload. Generate the Three-File Skill Standard: `SKILL.md` with `name`/`description` frontmatter always; `README.md` + `scripts/` with `__init__.py` if executable. |
| **2. Benchmarking**| `sterile_dev` | Develop deterministic logic locally bounded. No global OS modules. |
| **2. Benchmarking**| `skillopt_run` | Optimize new `SKILL.md`: run the SkillOpt evaluation pass per `rules/skills_and_integrations.md §3 "SkillOpt train_runner.py — Canonical Invocation"`, with `<target>` = the freshly forged `SKILL.md`. Done-criterion: exit `0` (command form, authorization gate, and skip-string are defined in the referenced block — not restated here, `RA-14`). |
| **2. Benchmarking**| `smoke_test` | `Tester Agent` executes isolated test in `/tmp/` or `:memory:`. Must return exit code 0. |
| **3. Registration**| `manifest_update` | For framework-wide skills: run `python3 .agents/skills/mass-standardizer/scripts/generate_manifest.py` — `manifest_skills.json` is **generated from SKILL.md frontmatter, never hand-edited** (CI enforces this). MCP servers register in `.agents/claude/mcp.json` (or the profile's `mcp/registry.json`). Host-only skills need no registration: Claude Code discovers them natively from `.claude/skills/`. |
| **4. Approval Gate** | `authorization` | Explicitly prompt human: *"Do you authorize the formal integration of this tool?"* |

---
*Optimized for Pipeline Deterministic Expansion & Tabular Density (v2.0.0).*
