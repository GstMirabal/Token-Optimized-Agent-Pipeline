# Universal-Agents Global User Rules
Syntax, Quality, and Communication Rules.

## 1. Code and Dialect
- **Standard Nomenclature:** Use PEP 8 for Python (`snake_case` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants) and native standards for JS/TS (`camelCase` for functions/variables).
- **Linters:** `ruff` (Python), `eslint/prettier` (JS/TS).
- **Typing:** Mandatory strict typing (`Type Hinting`, TypeScript).
- **Code Documentation:** Mandatory use of *Google Style Docstrings* for Python (`Args:`, `Returns:`) and *JSDoc* for JS/TS (`@param`, `@returns`).
- **Paths:** Prohibited use of absolute paths (hardcoded). Use dynamic `pathlib`.
- **Exception Handling:** Prohibited use of generic captures (`except Exception:`). Forcibly instantiate the specific exception at the source (e.g., `except ValueError:`). Prohibiting silencing errors with `pass`.
- **Output:** Use native `logging` (`INFO`, `ERROR`). Prohibited use of `print()` in production or automated operations.
- **Cognitive Complexity and Refactoring:** The Agent MUST trigger a "Refactoring Alert" in its report if it reviews a module whose code nesting depth is > 3 levels (`if` inside a `for` inside a `while`) or if functions exceed 50 lines.
- **Modularity (DRY):** Extract repetitive code into generic functions/classes.

## 2. Autonomy, Efficiency, and Zero-Trust
- **Imperative Token Saving (Raw Reading Prohibited):** It is **STRICTLY PROHIBITED** to read code files larger than 200 lines directly to understand their content. The agent **MUST** execute the universal `omni-context-minimizer` skill first to extract the structural skeleton, locate the exact line of interest in the terminal output, and only then proceed to isolate its reading to that segment. Ignoring this metric triggers an immediate tactical shutdown.
- **Code and Blackboard Language:** Technical English (variables, commits, `task.md`, `implementation_plan.md`).
- **Chat Language:** Spanish (explanations, debate with the user).
- **Mentor Role and Code Quarantine:** Phase 1 (Debate) is tactical and architectural. The Principal Agent is **prohibited** from injecting resolved code blocks larger than 10 lines into the chat during the discussion phase. Debate the ideas and submit a numbered list of steps to the user for execution.
- **Tactical Delegation:** Destructive operations (file deletion, database purging) or massive mutations are blocked. They require authorization or the explicit use of a *Workflow* with the `// turbo` flag.
- **External Skills Injection (`skills.sh`):** System acceleration is prioritized by integrating tools from the `skills.sh` master repository. **SECURITY LOCK:** Autonomous execution, download, or installation of any Skill by the Orchestrator is terminally prohibited. The AI must present the source link, the proposed content, and wait for the human to verify the source and manually authorize it.
- **Domain Audit (Global vs Local):** Every proposed new Skill MUST pass the *3-Variable Amnesia Test*: If the tool survives functionally to the total destruction of the current project, it will be saved in the universal matrix (`.agents/skills/`). If its code is heavily coupled to the business logic or native client databases, it will be isolated outside the submodule in a local project directory (e.g., `/.local_skills/`) to never contaminate the global matrix.
- **Dependencies and Secrets:** IMPERATIVE use of the native *"Standard Library"* of the language as the first and only initial option. It is prohibited to add third-party external libraries unless it is justified that manual refactoring exceeds the cost of the dependency. Prohibited to code keys or tokens in plain text (*hardcoded*). Exclusive use of `.env` or secret managers (`envtoml`).
