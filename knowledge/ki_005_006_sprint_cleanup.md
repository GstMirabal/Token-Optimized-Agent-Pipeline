# 🛡️ KI 005: Search-Before-Build Protocol (Efficiency Rule 21.1)

## Context
When an agent or developer decides to expand the framework's capabilities (Phase 4), there is a tendency to create new native skills immediately.

## The Problem
Developing native code for common tasks (e.g., linting, security audits) can be redundant if a high-quality, pre-tested version already exists in the master community repository (`skills.sh`). This leads to unnecessary token expenditure and maintenance overhead.

## The Solution (V1.7.6 Implementation)
We established **Rule 21.1: Search-Before-Build**:
1.  **Mandatory Search:** The Agent must query `https://skills.sh/trending` BEFORE proposing a new skill.
2.  **Audit & Compare:** If a third-party (`3rd-`) skill exists, it must be analyzed.
3.  **Justified Creation:** A Native skill is only built if the third-party version lacks integration with the framework's core governance (Phase 1 rules).

## Tags
`governance`, `efficiency`, `skills.sh`, `reuse`, `token-saver`
---
# 🏷️ KI 006: Native vs 3rd-Party Naming Standard (Rule 22 Refinement)

## Context
To ensure clear auditability of code origins within the `.agents/skills/` matrix.

## The Standard
1.  **Prefix `3rd-`**: RESERVED for any skill or tool downloaded/integrated from external sources (e.g., `skills.sh`).
2.  **No Prefix (Native)**: Any skill developed, designed, and implemented by the Human-AI pair within the session is **Native**.

## Benefit
This prevents "Attribution Hallucinations" and allows the Orchestrator to prioritize native tools that are pre-aligned with constitutional standards.

## Tags
`nomenclatura`, `architecture`, `governance`, `skills`
