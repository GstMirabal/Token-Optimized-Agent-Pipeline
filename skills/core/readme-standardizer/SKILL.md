---
name: readme-standardizer
description: Use this Skill ALWAYS whenever you are asked to create, generate, standardize, or update a project's README.md. Never generate a README from scratch with an improvised structure.
---

# 📝 Skill: README Gold Standardizer

## ⚠️ When to Trigger this Skill?
If the Director (user) asks to **"create the readme"**, **"update the readme"**, or **"apply the template to the project"**:
1. You are PROHIBITED from inventing the Markdown structure.
2. You MUST mandatory execute this process using the master architectural template hosted in this Submodule.

## 🛠️ How it Works (Instructions)

**Step 1: Project Understanding (Brain Drain)**
Before blindly generating text, analyze the context of the current repository:
- What languages does it use? (To fill in `{{TECH_STACK_BADGES}}`).
- What are the execution steps? (Docker, npm, venv) for `{{INSTALLATION_xx}}`.
- What is the project name and expected GitHub URL? (Usually `https://github.com/GstMirabal/[Directory-Name]`).

**Step 2: Read Master Template**
Open and read the static template file using your base tool:
`[submodule-root-directory]/.agents/skills/readme-standardizer/assets/template.md`

**Step 3: Fusion and Overwriting (Render)**
Mentally replace all `{{UPPERCASE_VARIABLES}}` delimiters in the template with the actual project information you extracted in Step 1.
Keep the HTML structure, `<p align="center">`, shields (Shields.io), navigation anchors (`<a name="readme-top"></a>`), and the "Contact" section at the end ABSOLUTELY intact.

**Step 4: Injection**
- If the `README.md` does not exist in the local project root, create it using the processed content.
- If the `README.md` already exists, **OVERWRITE** its content completely by applying the new template first and moving any useful old information to the "About the Project" or "Usage" sections.

> **Note for the Token-Saver:** Writing the README with the `write_to_file` or `replace_file_content` tool is an approved and mandatory operation.
