# 🪙 Skill: Omni Context Minimizer

## Purpose
This skill was designed to solve the **Context Bloat** problem. It extracts the structural skeleton of large source code files (over 200 lines) using an Abstract Syntax Tree (AST) approach, allowing the AI to understand the project's topology without consuming a massive amount of tokens.

## Files
- `SKILL.md`: Tactical instructions for the AI agents.
- `scripts/omni_minimizer.py`: The Python engine that performs the extraction.

## Usage
Triggered automatically by the **Token-Saver Auditor** when a file exceeds the 200-line threshold.

---
*Part of the Universal-Agents Core Intelligence.*
