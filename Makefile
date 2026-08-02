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

# Prefer the framework venv when it exists (a local checkout, where pytest lives
# in venv_skillopt and not in the system interpreter), and fall back to the
# system python3 (CI, which installs pytest into it and creates no venv). Only
# the pytest step needs a third-party package; every other step is stdlib-only.
VENV_PY := $(AGENTS_DIR)/venv_skillopt/bin/python3
PY := $(if $(wildcard $(VENV_PY)),$(VENV_PY),python3)

.PHONY: graphify-update graphify-rebuild verify docs-freshness-check

# Incremental AST sync after code changes (close_workflow Phase 1, no LLM cost).
graphify-update:
	$(GRAPHIFY) update .

# Full semantic rebuild — required when documentation changed (close_workflow Phase 1).
graphify-rebuild:
	$(GRAPHIFY) . --mode deep

# Framework self-check. THIS is the full set: `.github/workflows/ci.yml` invokes
# this target rather than listing its own steps, so a green local run and a green
# CI run cannot disagree (Phase 019, I-1). Before that change each side ran 4-5
# checks the other did not, and `LEGACY_RULE_CONCORDANCE.md` claimed a CI-only
# guarantee that no local run could reproduce.
#
# The only CI step deliberately NOT here is the Vale prose lint: it is a GitHub
# Action, not a command. Anything requiring network or credentials stays out of
# this target by the same rule.
verify:
	cd $(AGENTS_DIR) && python3 skills/slash-commander/scripts/verify_commands.py
	cd $(AGENTS_DIR) && find . -name "*.py" $(PY_EXCLUDES) | xargs python3 -m py_compile
	cd $(AGENTS_DIR) && python3 -c "import json, glob; \
	  [json.load(open(f)) for f in glob.glob('**/*.json', recursive=True) \
	   if not any(p in f for p in ('node_modules', '.git/', 'venv_skillopt'))]; print('JSON OK')"
	cd $(AGENTS_DIR) && python3 scripts/scan_workflow_determinism.py .
	cd $(AGENTS_DIR) && python3 scripts/verify_references.py
	cd $(AGENTS_DIR) && python3 scripts/map_workflows.py --check
	cd $(AGENTS_DIR) && python3 scripts/check_readme_counts.py
	cd $(AGENTS_DIR) && python3 scripts/check_manifest_parity.py
	cd $(AGENTS_DIR) && python3 scripts/check_absolute_paths.py
	cd $(AGENTS_DIR) && python3 skills/topology-monitor/scripts/legacy_app_auditor.py
	cd $(AGENTS_DIR) && python3 skills/mass-standardizer/scripts/generate_manifest.py \
	  && git -C $(AGENTS_DIR) diff --exit-code skills/manifest_skills.json
	cd $(AGENTS_DIR) && $(PY) -m pytest tests/ -q
	cd $(AGENTS_DIR) && bash tests/test_installer.sh

# Deterministic docs freshness + integrity gate (rules/documentation_standard.md §4).
# Inspects the CALLER's tree, so run it from the host project root.
docs-freshness-check:
	python3 $(AGENTS_DIR)/scripts/docs_freshness_check.py . $(SPRINT_ID)
