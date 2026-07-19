# 🏛️ Blueprint: {{MODULE}}
**File**: `docs/architecture/{{MODULE}}_BLUEPRINT.md` (J-06 Option B naming)
**Status**: `DRAFT | RATIFIED | SUPERSEDED`
**Sprint of origin**: #{{SPRINT_ID}}

---

## 1. Purpose
One paragraph: what this module does and why it exists. No implementation detail.

## 2. Boundaries & Jurisdiction
| Aspect | Value |
| :--- | :--- |
| **Owns** | {{PATHS_OWNED}} |
| **Must not touch** | {{PATHS_FORBIDDEN}} |
| **Upstream dependencies** | {{DEPENDS_ON}} |
| **Downstream consumers** | {{CONSUMED_BY}} |

## 3. Contracts
| Interface | Type | Defined in |
| :--- | :--- | :--- |
| {{ENDPOINT_OR_API}} | REST / event / function | `docs/contracts/{{MODULE}}_CONTRACT.md` |

## 4. Data Model (summary)
Key entities and relations only — one line each. Full schemas belong in the contract, not here.

## 5. Non-negotiable Constraints
Constraints the implementation may never violate (security, performance ceilings, invariants). Each row must be verifiable.

| Constraint | Verification |
| :--- | :--- |
| {{CONSTRAINT}} | {{HOW_TO_CHECK}} |

---
*A module without a ratified Blueprint cannot enter Monitored Execution (agents.md §0).*
