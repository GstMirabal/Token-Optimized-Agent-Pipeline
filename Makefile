# Deterministic entrypoints for the .agents framework (agents.md §3 `dependencies`).
# Run from the HOST project root as: make -f .agents/Makefile <target>
# (or from inside .agents/ when working on the framework itself).

VENV := .agents/venv_skillopt
GRAPHIFY := $(VENV)/bin/graphify

.PHONY: graphify-update graphify-rebuild verify docs-freshness-check

# Incremental AST sync after code changes (close_workflow Phase 1, no LLM cost).
graphify-update:
	$(GRAPHIFY) update .

# Full semantic rebuild — required when documentation changed (close_workflow Phase 1).
graphify-rebuild:
	$(GRAPHIFY) . --mode deep

# Framework self-check: command<->workflow links, Python syntax, JSON validity,
# and (token_economy_agent) a structural scan for workflow steps that look
# like a recurring mechanism delegated to agent judgment where a script would do.
verify:
	python3 .agents/skills/slash-commander/scripts/verify_commands.py
	find .agents -name "*.py" -not -path "*/node_modules/*" -not -path "*/.git/*" | xargs python3 -m py_compile
	python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('.agents/**/*.json', recursive=True) if 'node_modules' not in f]; print('JSON OK')"
	python3 .agents/scripts/scan_workflow_determinism.py .agents

# Deterministic docs freshness + integrity gate (rules/documentation_standard.md §4).
# Run from the HOST project root, not from inside .agents/.
docs-freshness-check:
	python3 .agents/scripts/docs_freshness_check.py . $(SPRINT_ID)
