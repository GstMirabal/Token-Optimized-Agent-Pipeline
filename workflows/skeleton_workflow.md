---
description: "Context Compression and AST Skeleton Extraction (Keyword: skeleton)"
version: 1.0.0
---

# 🛡️ Workflow: Skeleton (Context Optimizer)

Master protocol for reducing token consumption by extracting high-level architectural summaries from massive source files (>200 lines).

## 0. Trigger Condition
- **Efficiency Override:** Automatically invoked by the **Orchestrator** or manually by the **Human User** when facing files that threaten the active context window.

## 1. Physical Extraction (@skill_architect)
- **Tool Invocation:** The Agent MUST execute the native command: `python3 .agents/skills/omni-context-minimizer/scripts/omni_minimizer.py [target_path]`.
- **Output Handling:** The resulting AST skeleton (classes, function signatures, and decorators) is captured while stripping out the implementation logic.

## 2. Context Ingestion
- **Verification:** The Agent replaces the full-file read attempt with the extracted skeleton.
- **Goal:** Ensure the AI understands the **What** (Interfaces/API) without wasting tokens on the **How** (Logic Bloat).

---
*Certified under Matrix V2 Efficiency Standards*
