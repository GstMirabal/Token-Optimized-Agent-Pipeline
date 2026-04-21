# 🌌 Skills Samples

Welcome to the **Skills Samples** repository! This project is designed to centralize, manage, and refine the capabilities (skills) of **Universal-Agents**, your next-generation AI governance assistant.

## 🚀 What is this project?

This repository serves as a knowledge and tool base to extend the functionalities of Universal-Agents through **Skills**. Each skill defines a workflow, a set of rules, or a specific tool that allows the assistant to interact more intelligently and efficiently with the user's code and environment.

## 🛠️ Available Skills

Currently, the repository features the following capabilities:

### 1. 🤖 [Skill Creator](file:///skills/skill-creator/SKILL.md)
The crown jewel. This skill is a meta-system designed to **create, test, and mitigate errors in other skills**.
- **Purpose:** Automate the skill development lifecycle (design, drafting, evals, benchmarking, and optimization).
- **Features:** Includes an evaluation viewer (`eval-viewer`), validation scripts, packaging, and description optimization for better activation (triggering).

### 2. ✍️ [Commiter](file:///skills/commiter/SKILL.md)
Standardizes communication in version control.
- **Purpose:** Guide the assistant to create commit messages following the **Conventional Commits** specification.
- **Features:** Use of emojis (✨, 🐛, 📝, etc.) and clear structures to maintain a professional and readable Git history.

## 📂 Project Structure

```bash
.
├── skills/           # Main skills directory
│   ├── commiter/     # Skill for standardized commits
│   └── skill-creator/# Skill for developing new skills
└── skills-lock.json  # Version and source management for skills
```

## 🧪 How to Start Contributing

If you wish to create a new skill or improve existing ones:

1. **Use the Skill Creator:** It is specifically designed to guide you through this process.
2. **Follow the Rules:** Consult the `commiter` skill to ensure your changes in the repository follow the established standards.
3. **Test and Evaluate:** Use the tools integrated in `skill-creator/scripts` to run benchmarks and validate your skills' performance.

---
> [!TIP]
> Keep your skills focused and modular. The best skills are those that solve a specific problem exceptionally.

---
*Developed with ❤️ to empower productivity with Universal-Agents.*
