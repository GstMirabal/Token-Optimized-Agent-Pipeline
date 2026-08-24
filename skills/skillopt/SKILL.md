---
name: skillopt
description: Runs Microsoft SkillOpt training/optimization for agent skill prompts inside the isolated .agents/venv_skillopt/ environment. Every optimizer run requires explicit human authorization.
---

# 🛠️ Skill: SkillOpt (Rule 71 Compliance)

## Domain
- **Category:** Infrastructure / Optimization
- **Origin:** Third-Party Concept Integration (Microsoft Research)
- **Status:** `ACTIVE_LOCAL`

## Technical Logic
This tool integrates Microsoft's SkillOpt using a separate isolated virtual environment (`.agents/venv_skillopt/`) and runtime monkeypatching. It registers the `agents_opt` benchmark adapter and routes model generation to `gemini_backend.py` without mutating PyPI package binaries.

## Provisioning (on demand)
The session bootstrap only installs the lean core (`requirements-core.txt`). Before the FIRST training run in an environment, install this skill's heavy stack:
```bash
.agents/venv_skillopt/bin/pip install -r .agents/requirements-skillopt.txt
```
This transitively pulls in `azure-*` packages (recorded in `docs/audits/SKILLOPT_TRANSITIVE_CLOSURE.md`, which replaced `requirements-freeze.txt` in Sprint 023 `C7` so that a scanner stops reading an optional closure as this framework's own manifest) — the vendored `skillopt` package ships an `azure_openai` backend module by default. It is never called: `train_runner.py apply_monkeypatches()` imports that module only as a patch target and overwrites its functions to route to `gemini_backend.py` (or the Claude Agent SDK, via `model_backend: claude` in the config — see `configs/agents_opt.yaml`). Do not "clean up" the azure packages; they are a real, if unused, transitive dependency of the pinned `skillopt` version.

## Commands
```bash
# Execute optimization using configs
.agents/venv_skillopt/bin/python .agents/skills/skillopt/scripts/train_runner.py --config .agents/skills/skillopt/configs/agents_opt.yaml
```

## Governance Audit
- **Rule 71 Compliance (Flat Mapping):** Replaced nested folder clones with PyPI dependencies and flat scripts under `.agents/skills/skillopt/`.
- **Double Venv Isolation:** Mandated to run commands exclusively within `.agents/venv_skillopt/` to protect Django dependencies.
- **Explicit Authorization:** Every execution of the optimizer train loop must be approved by the human operator.
