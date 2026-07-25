# Token-Saver Auditor (CFO)

## About The Project

The **Token-Saver Auditor (CFO)** acts as the Matrix's financial supervisor. It is an economic "Kill Switch" that analyzes implementation plans to guarantee minimal token consumption, prioritizing the `omni-context-minimizer` and preventing redundant context scans (enforces `rules/token_economy.md`).

**Key Features:**
*   **Economic Oversight:** Cost analysis before any massive task execution.
*   **Context Optimization:** Forces AST skeletons on large files.
*   **Budget Guard:** Prevents infinite reasoning loops that drain API quotas.

### Built With

![Governance](https://img.shields.io/badge/governance-logic-blue)
![CFO](https://img.shields.io/badge/CFO-audit-orange)

## Getting Started

### Prerequisites

*   **Universal-Agents Core**: Requires the governance rules (`agents.md` + `rules/`) to be active.

### Installation & Configuration

1. **Submodule Integration**
   Located at `.agents/skills/token-saver-auditor/`.

2. **Activation**
   Activates automatically during the tactical planning phase (Orchestration Phase).

## Usage

The Auditor reviews every **Orchestrator** proposal before the **DevOps Sentinel** may execute physical changes. If the plan is inefficient (e.g. recursive scan without the minimizer), the Auditor blocks execution.

```bash
# Example: activating the Auditor during the debate phase
Principal Agent: "The Auditor must certify this Phase 2 plan before proceeding."
```

## Contributing

1. Fork the Project
2. Create your Feature Branch
3. Pull Request
