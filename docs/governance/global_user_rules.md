# Universal-Agents Global User Rules
Syntax, Quality, and Communication Rules.

## 1. Code and Dialect
- **Rule 1: Standard Nomenclature:** Use PEP 8 for Python (`snake_case` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants) and native standards for JS/TS (`camelCase` for functions/variables).
- **Rule 2: Linters and Formatters:** Mandatory use of `ruff` (Python) and `eslint/prettier` (JS/TS).
- **Rule 3: Strict Typing:** Mandatory typing (`Type Hinting`, TypeScript).
- **Rule 4: Code Documentation:** Mandatory use of *Google Style Docstrings* for Python (`Args:`, `Returns:`) and *JSDoc* for JS/TS (`@param`, `@returns`).
- **Rule 5: Dynamic Paths:** Prohibited use of absolute paths (hardcoded). Use dynamic `pathlib`.
- **Rule 6: Exception Handling:** Prohibited generic captures (`except Exception:`). Forcibly instantiate specific exceptions at the source (e.g., `except ValueError:`). No silencing errors with `pass`.
- **Rule 7: Native Output:** Use native `logging` (`INFO`, `ERROR`). Prohibited use of `print()` in production or automated operations.
- **Rule 8: Cognitive Complexity:** The Agent MUST trigger a "Refactoring Alert" if nesting depth is > 3 or functions exceed 50 lines.
- **Rule 9: Modularity (DRY):** Extract repetitive code into generic functions/classes.
- **Rule 10: Context Refresh Protocol (Anti-Amnesia):** If the conversation history exceeds 10 messages or 5,000 tokens, the Agent **MUST** re-read `global_user_rules.md` and `task.md`. Upon completion, it must state: *"Governance verified and aligned (Rule 10)"*.
- **Rule 11: Conciseness Protocol (No-Meta-Chat):** Prohibited use of excessive courtesy, filler phrases (e.g., "I'm here to help", "I understand"), and redundant confirmations. Reports MUST be 100% technical and concise.
- **Rule 12: No-Placeholders Policy:** Prohibited use of `TODO`, `FIXME`, or placeholder code blocks in final implementations.

## 2. Autonomy, Efficiency, and Zero-Trust
- **Rule 13: Language Standards:** Code/Commits: Technical English (No-Meta-Data). Debate/Discussion: Spanish.
- **Rule 14: Mentor Role & Quarantine:** Phase 1 Debate is architectural. Prohibited code blocks > 10 lines during discussion. Mandatory execution roadmap. **STRICT LOCK:** Express user authorization required to transition from Roadmap to Execution.
- **Rule 15: Tactical Delegation:** Destructive/massive mutations blocked. Require authorized `// turbo` flag or dedicated Workflow.
- **Rule 16: Token Efficiency:** Prohibited raw reading of files > 200 lines. Mandatory `omni-context-minimizer` skeleton extraction. Mandatory reporting of % tokens saved.
- **Rule 17: Mandatory Certification:** Sprints/phases require Audit Workflow certification before closure. Agent MUST select and deploy context-appropriate audit tools.
- **Rule 18: Secrets & Environment:** Native Std Lib priority. Mandatory `.env`. Guessing missing variables prohibited; manual user input mandatory.
- **Rule 19: Artifacts & Scalability:** Root: `.agents/task/`. Mandatory hierarchical sub-folders (Phase/Module) for large-scale projects to avoid flat-file pollution.
- **Rule 20: Master Index:** Root `task.md` MUST remain a clean TOC pointing to the active sprint.

## 3. Governance & Directory Structure
- **Rule 21: Persistent Metadata:** Global Framework Roadmaps and constitutional rules MUST be stored in `.agents/governance/`. Operational project roadmaps reside in the local task directory.
- **Rule 22: Audit Exclusion:** The `.agents/governance/` directory is EXCLUDED from automated code audits.
- **Rule 23: Project Topology:** Mandatory compliance with directory taxonomy defined in `@project_mapping_and_context.md`. Prohibited usage of non-authorized paths for state persistence.
- **Rule 24: Sprint Nomenclature:** Mandatory naming: `XXX-sprint-name.md` (e.g., `001-retrofitting.md`).
- **Rule 25: Deliverable Persistence:** Mandatory mirroring of finalized architectural designs and strategic roadmaps to the primary versioning areas defined in the project topology.

## 4. Roadmap Maturity & Execution Control
- **Rule 26: Triple Security Lock:** Mandatory execution block until: (1) Phase Roadmap is finalized/unlocked, (2) Discovery Audit is complete, and (3) Technical Workflow is human-authorized.
- **Rule 27: Tech-Debt Tracking:** Mandatory tagging of workarounds/architectural deviations as `:tech-debt:` in `task.md`.
- **Rule 28: Discovery Requirement:** Phase execution prohibited until all Milestones (M0, M1, etc.) and deliverables are fully defined in `.agents/task/roadmaps/`.
- **Rule 29: Lock Override:** Roadmap safety lock transition to `READY_FOR_EXECUTION` requires comprehensive High-Integrity Audit and explicit user authorization.

## 5. Session Closing & Atomic Commit Protocol
- **Rule 30: Atomic Close:** Mandatory atomic commit of all validated changes before session conclusion.
- **Rule 31: Closing Cycle:** Follow complete cycle (Amnesia Extraction, Indexing, and Final Commit) as defined in the global closing workflow.
- **Rule 32: Dual Synchronization:** Mandatory Parent/Submodule dual-sync if governance, roadmaps, or knowledge items are updated.
- **Rule 33: Traceability:** Conventional Commits standard mandatory. Every commit message MUST include the Task or Sprint ID (Ref: #XXX).
