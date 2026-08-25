---
description: "Structural & Rule Compliance Audit Protocol (Keyword: audit)"
version: 2.0.0
invoked_by: human:/agents:audit, reverse_documentation_workflow.md#findings-handoff
---

# 🛡️ Workflow: Audit (Standards Sweep)

A non-tactical governance protocol engineered to verify structural, topological, and legal integrity across the pipeline environment. No business logic or product features are developed during this workflow.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Zero-Memory Initialization** | `init_check` | All executing subagents initialize with zero memory; the governance ruleset arrives auto-imported (no re-read — `anti_amnesia`). Coordinator is `Rule Validator`. |
| **1. Topo Sweep** | `rule_introspection`| Cross-reference `rules/` against `agents.md` to highlight overlaps or contradictions. |
| **1. Topo Sweep** | `skill_standard_check`| Verify all skills in `skills/` legally adhere to the Three-File Skill Standard — run `python3 .agents/skills/topology-monitor/scripts/legacy_app_auditor.py`. |
| **1. Topo Sweep** | `federation_audit`| **Host mode only**: verify `.agents` is pinned to a release tag (`git -C .agents describe --exact-match --tags` succeeds; floating on a branch is a drift risk), that `.claude_bridge.lock` matches `git -C .agents rev-parse HEAD`, that the linked `.claude/` artifacts actually exist on disk (a matching lock is not proof — see `hooks/on_init.py bridge_intact`), and that `git -C .agents status --porcelain` is clean (`strict_rule`). *Nucleus mode: skip the tag, lock and submodule-cleanliness checks — no `.claude_bridge.lock` exists here and the nucleus deliberately floats on `main`. **It does have a bridge**: `scripts/install.py install_nucleus_bridge()` links commands and agents, deliberately without hooks, skills, MCP or settings. The one check that does apply — that the linked artifacts exist on disk — belongs to `start_workflow.md bridge_check`, which runs every session in nucleus mode and is more precise than an occasional audit. This row previously claimed the nucleus "has no bridge", which was already false when written (Sprint 023 `C6`).* |
| **2. Doc Purity** | `nomenclature` | `Doc Orchestrator` forcibly auto-corrects any file evading the `[Stack]/[Layer]/[Sprint_ID]` dictionary structure. |
| **2. Doc Purity** | `precision_audit` | Evaluate rules in dry-run mode via `train_runner.py` (requires explicit authorization). |
| **2. Doc Purity** | `link_audit` | Ensure no internal `.md` file points to eradicated paths. |
| **3. Verdict** | `report` | Generate a conclusive `pipeline_audit_report.md` artifact detailing discrepancies neutralized. |

---
*Optimized for Pipeline Preventative Maintenance & Tabular Density (v2.0.0).*
