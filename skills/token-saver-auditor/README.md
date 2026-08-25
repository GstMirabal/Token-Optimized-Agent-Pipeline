# Token-Saver Auditor (CFO)

## About The Project

The **Token-Saver Auditor** is the pipeline's structural cost gate for
Implementation Plans. It enforces `rules/token_economy.md` before Phase 5
approval: anti-patterns in the plan fail with exit `2`.

Filter 5 (script vs agent judgment on recurring workflow steps) lives in
`scripts/scan_workflow_determinism.py` (`make verify`). This skill owns Filters
1–4 and 6 plus the Cost / Mechanisms checks on the plan artifact.

### Built With

Governance logic · Three-File Skill Standard (`agents.md §3`)

## Getting Started

### Prerequisites

* Token-Optimized Agent Pipeline core (`agents.md` + `rules/`)

### Installation

Located at `skills/token-saver-auditor/` (Three-File: `README.md`, `SKILL.md`,
`scripts/`).

## Usage

```bash
# Audit a specific plan (exit 2 = reject)
python3 skills/token-saver-auditor/scripts/audit_plan.py \
  docs/sprints/030-core-pipeline/IMPLEMENTATION_PLAN.md

# Current sprint only (skips when sprint id < 30 or no plan)
python3 skills/token-saver-auditor/scripts/audit_plan.py --current-sprint
```

Invoked by `workflows/pipeline_workflow.md` Phases 1 and 5, and by
`Makefile` `verify` via `--current-sprint`.

## Contributing

1. Fork the Project
2. Create your Feature Branch
3. Pull Request
