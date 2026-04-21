---
name: slash-commander
description: Bridges Matrix workflows to Claude Code Slash Commands.
version: 1.0.0
category: core/governance
dependencies:
  - python3
  - mtx_mapper_01
  - devops_sentinel_01
---

# ☄️ Skill: Slash Commander

## 1. Procedural Workflow
The **Slash Commander** operates through an atomic generation cycle triggered by the **DevOps Sentinel**:

1.  **Workflow Discovery**: Scan `workflows/*.md` for valid entry points.
2.  **Metadata Extraction**: Identify `@description` and `version` from the workflow frontmatter.
3.  **Command Blueprinting**: Generate a TypeScript skill manifest (`.ts`) that:
    *   Defines the slash command name (from the filename).
    *   Maps the command handler to the execution of the Markdown workflow.
4.  **Local Injection**: Write the generated `.ts` files to the local `.claude.code/skills/` directory.

## 2. Command Mapping Logic
| Workflow | Output Command | Logic |
| :--- | :--- | :--- |
| `start_workflow.md` | `/start` | Triggers the Matrix Initiation Protocol. |
| `close_workflow.md` | `/close` | Triggers the Session Liquidation and Memory Purge. |
| `*` | `/[name]` | Generalized mapping for any secondary workflow. |

## 3. Constitutional Constraints
- **Isolation**: The generator MUST NOT modify existing user skills in `.claude.code/skills/` unless they are explicitly tagged as `origin: agents_matrix`.
- **Mirroring**: Any change in the physical `.md` workflow MUST trigger an automatic re-generation of the corresponding slash command.

## 4. Error Handling
- **Collision Detection**: If a command name already exists in the user's local configuration, the Sentinel MUST issue a **Manual Correction Alert** and skip the injection.
- **Dependency Missing**: If the `.claude.code/` directory is not found, the skill defaults to "Documentation-Only" mode.

---
*Optimized for Universal-Agents Rule 113.*
