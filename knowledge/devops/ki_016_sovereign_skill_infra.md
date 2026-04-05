# 🧠 Knowledge Item: Sovereign Skill Infrastructure (Rule 70 Hardening)

- **KI ID**: `KI-016`
- **Domain**: Infrastructure / DevOps
- **Governance**: Rule 70, Rule 57
- **Date**: 2026-04-05

## 🎯 Intelligence Summary
This session identifies the protocol for transforming volatile dynamic-discovery tools into sovereign, locally-installed framework skills.

## 🏁 Heuristic Lessons
1.  **Bridge-to-Local Pivot**: To eliminate environment instability, "bridge" skills using `npx -y` must be refactored into physical installations (`npm install --prefix`) within `skills/3rd/`.
2.  **Architectural Traceability**: Rule 70 now mandates that any selected discovery tool must be explicitly represented in the **Mermaid diagrams** of the Implementation Plan to ensure structural auditability.
3.  **Sovereign Triggers**: Standardizing workflow activation keywords (`start`, `matrix`, `close`) across README and file headers ensures consistent execution and reduces operational ambiguity during session starts.

## 🛠️ Implementation Pattern
```bash
# Example: Local Skill Installation Protocol
mkdir -p skills/3rd/my-tool
npm install my-tool --prefix skills/3rd/my-tool
# Update manifest_skills.json and Rule 70 prioritization.
```

## 🛡️ Governance Guard
- **Mandatory Reading Protocol**: Rule 57 now applies to ALL agent roles (Orchestrator, Matrix, etc.) to ensure that constitutional constraints are prioritized after every role-switch.

---
*EXTRACTION_COMPLETE: INTELLIGENCE_DESTILLED*
