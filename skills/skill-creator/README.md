# Skill Creator

Assists in the creation of new atomic skills following global governance rules.

## About The Project

The **Skill Creator** is the scaffolding and automation tool for expanding the Matrix arsenal. It ensures every new atomic skill inherits the institutional security, efficiency, and documentation protocols, in compliance with the flat `skills/` topology (`agents.md §3`).

**Key Features:**
*   **Atomic Scaffolding:** Automatic generation of `scripts/` directories and `SKILL.md` / `README.md` files.
*   **Audit Integration:** Automatically links the new tool with the `python-quality-auditor`.
*   **Governance Guard:** Validates that the skill's name and category comply with the framework's official taxonomy.

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Automation](https://img.shields.io/badge/Automation-Project-blue)

## Getting Started

### Prerequisites

*   **Universal-Agents Submodule**: Access to the framework's global scaffolding templates is required.

### Installation & Configuration

1. **Integrated in Core**
   Located at `.agents/skills/skill-creator/`.

2. **Template access**
   Uses the master templates defined in the framework assets to inject the atomized rules into each new skill.

## Usage

Invoked when the **Orchestrator** or the user identifies the need for a new technical capability that must be persisted into the Matrix:

```bash
# Example: creating a new atomic scraping skill
python .agents/skills/skill-creator/scripts/create_skill.py "web-scraper" "Expertise"
```
