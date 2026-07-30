# Deterministic entrypoints for the .agents framework (agents.md §3 `dependencies`).
#
# Works from either location — every path below is derived from THIS Makefile's
# own location, never from the caller's working directory:
#   from a HOST project root:  make -f .agents/Makefile <target>
#   from inside the nucleus:   make <target>
#
# Two classes of target, deliberately different about working directory:
#   - `verify` checks the FRAMEWORK, so it runs with the .agents root as its
#     CWD: its scripts resolve `commands/`, `workflows/` and `skills/` relative
#     to the working directory, and silently find nothing if it is wrong.
#   - `graphify-*` and `docs-freshness-check` analyse the SUBJECT project, so
#     they keep the caller's CWD — that is the tree they are meant to inspect.

AGENTS_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
GRAPHIFY := $(AGENTS_DIR)/venv_skillopt/bin/graphify
PY_EXCLUDES := -not -path "*/.git/*" -not -path "*/node_modules/*" -not -path "*/venv_skillopt/*"

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
	cd $(AGENTS_DIR) && python3 skills/slash-commander/scripts/verify_commands.py
	cd $(AGENTS_DIR) && find . -name "*.py" $(PY_EXCLUDES) | xargs python3 -m py_compile
	cd $(AGENTS_DIR) && python3 -c "import json, glob; \
	  [json.load(open(f)) for f in glob.glob('**/*.json', recursive=True) \
	   if not any(p in f for p in ('node_modules', '.git/', 'venv_skillopt'))]; print('JSON OK')"
	cd $(AGENTS_DIR) && python3 scripts/scan_workflow_determinism.py .

# Deterministic docs freshness + integrity gate (rules/documentation_standard.md §4).
# Inspects the CALLER's tree, so run it from the host project root.
docs-freshness-check:
	python3 $(AGENTS_DIR)/scripts/docs_freshness_check.py . $(SPRINT_ID)
