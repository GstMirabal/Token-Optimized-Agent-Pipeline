# 🛠️ Skill: SkillOpt (Rule 71 Compliance)

## Domain
- **Category:** Infrastructure / Optimization
- **Origin:** Third-Party Concept Integration (Microsoft Research)
- **Status:** `ACTIVE_LOCAL`

## Technical Logic
This tool integrates Microsoft's SkillOpt using a separate isolated virtual environment (`.agents/venv_skillopt/`) and runtime monkeypatching. It registers the `agents_opt` benchmark adapter and routes model generation to `gemini_backend.py` without mutating PyPI package binaries.

## Commands
```bash
# Execute optimization using configs
.agents/venv_skillopt/bin/python .agents/skills/skillopt/scripts/train_runner.py --config .agents/skills/skillopt/configs/agents_opt.yaml
```

## Governance Audit
- **Rule 71 Compliance (Flat Mapping):** Replaced nested folder clones with PyPI dependencies and flat scripts under `.agents/skills/skillopt/`.
- **Double Venv Isolation:** Mandated to run commands exclusively within `.agents/venv_skillopt/` to protect Django dependencies.
- **Explicit Authorization:** Every execution of the optimizer train loop must be approved by the human operator.
