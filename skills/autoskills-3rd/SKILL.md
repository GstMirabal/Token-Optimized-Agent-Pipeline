---
name: autoskills
description: Third-party dynamic skill-discovery engine (Priority #2 escalation after skills/manifest_skills.json) — scans the local Arsenal Bridge for existing tools before a new skill is forged from scratch.
---

# 🛠️ Skill: Autoskills (Rule 70)

## Domain
- **Category:** Infrastructure / Automation
- **Origin:** Third-Party Local Arsenal
- **Status:** `ACTIVE_LOCAL`

## Technical Logic
This tool is the Matrix's dynamic discovery engine. Despite being an external (3rd-party) dependency, `autoskills` runs from a local installation inside the project environment to guarantee sovereignty over executed code. It lets subagents search the external arsenal when the local `manifest_skills.json` is insufficient.

## Provisioning
`node_modules/` is NOT committed (industry standard). The DevOps Sentinel provisions it on demand:
```bash
pnpm install --dir .agents/skills/autoskills-3rd
```

## Commands
```bash
# Run discovery from the local installation
.agents/skills/autoskills-3rd/node_modules/.bin/autoskills --scan . --output .agents/skills/discovery.json
```

## Governance Audit
- **Rule 70 Compliance (Priority #2):** This tool is the second escalation level after `manifest_skills.json`.
- **Sovereignty Policy:** `npx -y` is prohibited (agents.md §8). The tool must be locally installed via `pnpm install` inside `skills/autoskills-3rd/` and provisioned by the DevOps Sentinel.
