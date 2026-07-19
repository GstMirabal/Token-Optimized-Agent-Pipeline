---
description: "Constitutional Matrix Audit Protocol (Keyword: audit)"
version: 2.0.0
---

# 🛡️ Workflow: Audit (The Inquisitor Protocol)

A non-tactical governance protocol engineered to verify structural, topological, and legal integrity across the Matrix environment. No business logic or product features are developed during this workflow.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Amnestic Anchor** | `init_check` | All executing subagents MUST initialize with absolute zero memory. Coordinator is `Rule Validator`. |
| **1. Topo Sweep** | `rule_introspection`| Cross-reference `rules/` against `agents.md` to highlight overlaps or contradictions. |
| **1. Topo Sweep** | `arsenal_check`| Verify all skills in `skills/` legally adhere to the (dual) Trinity Standard — run `python3 .agents/skills/matrix-monitor/scripts/legacy_app_auditor.py`. |
| **1. Topo Sweep** | `federation_audit`| Verify `.agents` is **pinned to a release tag** (`git -C .agents describe --exact-match --tags` succeeds; floating on a branch is a drift risk), that `.claude_bridge.lock` matches `git -C .agents rev-parse HEAD`, and that `git -C .agents status --porcelain` is clean (`strict_rule`). |
| **2. Doc Purity** | `nomenclature` | `Doc Orchestrator` forcibly auto-corrects any file evading the `[Stack]/[Layer]/[Sprint_ID]` dictionary structure. |
| **2. Doc Purity** | `precision_audit` | Evaluate rules in dry-run mode via `train_runner.py` (requires explicit authorization). |
| **2. Doc Purity** | `link_audit` | Ensure no internal `.md` file points to eradicated paths. |
| **3. Verdict** | `report` | Generate a conclusive `matrix_audit_report.md` artifact detailing discrepancies neutralized. |

---
*Optimized for Matrix V2 Preventative Maintenance & Tabular Density (v2.0.0).*
