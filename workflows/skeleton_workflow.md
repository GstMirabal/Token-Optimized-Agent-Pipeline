---
description: "Context Compression and AST Skeleton Extraction (Keyword: skeleton)"
version: 2.0.0
---

# 🛡️ Workflow: Skeleton (Context Optimizer)

Master protocol for reducing token consumption by extracting high-level architectural summaries from massive source files (>200 lines).

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Trigger** | `efficiency_override`| Invoked automatically by Orchestrator or manually when facing files >200 lines. |
| **1. Extraction**| `omni_minimizer` | `Skill Architect` MUST execute `omni_minimizer.py [target_path]`. |
| **1. Extraction**| `output_handling` | AST skeleton (classes, function signatures, decorators) is captured; logic is stripped. |
| **2. Ingestion** | `context_swap` | Replace full-file read attempts with the extracted skeleton to save tokens. |

---
*Optimized for Matrix V2 Efficiency Standards & Tabular Density (v2.0.0).*
