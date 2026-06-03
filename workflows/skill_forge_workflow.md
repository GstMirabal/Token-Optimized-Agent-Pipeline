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
| **1. Scaffolding** | `blueprint` | Define exact I/O payload. Generate Trinity Standard: `README.md`, `SKILL.md`, `scripts/`. |
| **2. Benchmarking**| `sterile_dev` | Develop deterministic logic locally bounded. No global OS modules. |
| **2. Benchmarking**| `skillopt_run` | Optimize new `SKILL.md` via `train_runner.py` (requires explicit authorization). |
| **2. Benchmarking**| `smoke_test` | `Tester Agent` executes isolated test in `/tmp/` or `:memory:`. Must return exit code 0. |
| **3. Registration**| `manifest_update` | Update `skills/manifest_skills.json` or `mcp-config.json` with new tool path and capabilities. |
| **4. Golden Gate** | `authorization` | Explicitly prompt human: *"Do you authorize the formal integration of this tool?"* |

---
*Optimized for Matrix V2 Deterministic Expansion & Tabular Density (v2.0.0).*
