# SkillOpt: Self-Evolving Markdown Instructions Optimizer (Dynamic Edition)

This skill integrates Microsoft's **SkillOpt** text-space optimization framework into the `.agents` submodule without modifying the core PyPI package code. It registers custom environments and backends dynamically in memory at runtime.

---

## 🎯 Key Features
- **Double Venv Isolation**: Runs in `.agents/venv_skillopt/` to prevent package version conflicts with the main Django backend.
- **Dynamic Registry**: Injects the `agents_opt` benchmark adapter and Gemini model backends at execution time.
- **Native Gemini Support**: Redirects standard OpenAI calls to the official Google GenAI client using `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
- **Zero Cost at Inference**: Instructions are optimized offline; outputs are clean markdown files with no runtime token overhead.

---

## 🛠️ How it Works
1. **Runner Init**: `train_runner.py` intercepts `openai_chat` calls and redirects them to `gemini_backend.py`.
2. **Benchmark Registration**: Binds `AgentsOptEnv` (which runs linters, graph updates, etc.) and `AgentsOptDataLoader` into SkillOpt's registry.
3. **Training Loop**: Runs rollouts of target rules on mock scenarios, reflects on execution logs, proposes bounded text edits, and commits changes only if they pass validation gating.

---

## 🚀 Commands & Usage
Execute the optimizer inside the isolated virtual environment:
```bash
.agents/venv_skillopt/bin/python .agents/skills/skillopt/scripts/train_runner.py --config .agents/skills/skillopt/configs/agents_opt.yaml
```
