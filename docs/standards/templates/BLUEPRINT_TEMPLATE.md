# 🏛️ Blueprint: {{MODULE}}
**File**: `docs/architecture/{{MODULE}}_BLUEPRINT.md` (J-06 Option B naming)
**Status**: `DRAFT | RATIFIED | SUPERSEDED`
**Sprint of origin**: #{{SPRINT_ID}}
**Last Audit Sprint**: #{{SPRINT_ID}}
**Last Audit Date**: {{ISO_DATE}}
**Last Audit Commit SHA**: {{COMMIT_SHA}}

---

arc42-lite (`rules/documentation_standard.md §5`) — Reference only. This document states current facts, verifiably; it never argues for them. Any decision behind this module's shape lives in a linked ADR, not here.

## 1. Introduction & Goals
One paragraph: what this module does, trimmed to scope — no rationale, no alternatives considered. (The "why" lives in the module's ADRs, listed in §7.)

## 2. Context & Scope
| Aspect | Value |
| :--- | :--- |
| **Upstream dependencies** | {{DEPENDS_ON}} |
| **Downstream consumers** | {{CONSUMED_BY}} |

## 3. Building Block View
| Aspect | Value |
| :--- | :--- |
| **Owns** | {{PATHS_OWNED}} |
| **Must not touch** | {{PATHS_FORBIDDEN}} |

Contracts (formal interfaces this module exposes):

| Interface | Type | Defined in |
| :--- | :--- | :--- |
| {{ENDPOINT_OR_API}} | REST / event / function | `docs/contracts/{{MODULE}}_CONTRACT.md` |

Data model (summary only — key entities and relations, one line each; full schemas belong in the contract):
- {{ENTITY}}: {{ONE_LINE_DESCRIPTION}}

## 4. Runtime View
Key flows through this module, as sequences — only the ones a reader actually needs to trace a bug or a change through. Not every code path.

1. {{FLOW_STEP}}

## 5. Crosscutting Concepts
Patterns used throughout this module (error handling, auth boundary, caching, etc.) that don't belong to any single block above.

## 6. Non-negotiable Constraints
Constraints the implementation may never violate (security, performance ceilings, invariants). Each row must be verifiable — not aspirational.

| Constraint | Verification |
| :--- | :--- |
| {{CONSTRAINT}} | {{HOW_TO_CHECK}} |

## 7. Decisions
This module's ADR log — link, don't restate:
- `docs/decisions/ADR-{{NUMBER}}-{{slug}}.md`: {{ONE_LINE_SUMMARY}}

## 8. Glossary
| Term | Meaning in this module |
| :--- | :--- |
| {{TERM}} | {{DEFINITION}} |

---
*A module without a ratified Blueprint cannot enter Monitored Execution (agents.md §0). C4 Level 3 (Component diagram) required here if this module qualifies per `rules/documentation_standard.md §2.1` — see `**C4 Level Override**` for a manually-justified exception.*
