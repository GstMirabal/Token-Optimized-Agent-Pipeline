---
skill_id: governance-sentinel
name: Governance Sentinel Heuristic Engine
layer: local
jurisdiction: memory/telemetry/
trinity_standard: 1.0
---

# Logic Definition

The skill performs frequency analysis on telemetry nodes to detect recurring violations.

## Triggers
- **Manual**: Invoked by the Learner agent.
- **Event**: Post-sprint analysis.

## Core Commands
- `python3 scripts/distill.py`: Aggregates errors and generates a `proposal.md`.
