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

.PHONY: graphify-update graphify-rebuild verify docs-freshness-check session-start model-ledger cursor-tiers role-artifacts


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
	cd $(AGENTS_DIR) && python3 skills/token-saver-auditor/scripts/audit_plan.py --current-sprint
	cd $(AGENTS_DIR) && python3 scripts/check_task_scope.py --current-sprint
	cd $(AGENTS_DIR) && python3 scripts/check_gate_log.py --current-sprint
	cd $(AGENTS_DIR) && python3 scripts/verify_references.py
	cd $(AGENTS_DIR) && $(PY) scripts/check_model_tiers.py
	cd $(AGENTS_DIR) && $(PY) scripts/detect_new_models.py --check
	cd $(AGENTS_DIR) && python3 scripts/map_workflows.py --check
	cd $(AGENTS_DIR) && python3 scripts/check_readme_counts.py
	cd $(AGENTS_DIR) && python3 scripts/check_manifest_parity.py
	cd $(AGENTS_DIR) && python3 scripts/check_absolute_paths.py
	cd $(AGENTS_DIR) && python3 skills/topology-monitor/scripts/legacy_app_auditor.py
	cd $(AGENTS_DIR) && python3 skills/mass-standardizer/scripts/generate_manifest.py \
	  && git -C $(AGENTS_DIR) diff --exit-code skills/manifest_skills.json
# A test must not leave the tracked tree changed. Once `C0.3` anchored
# `branch_sovereignty.WAIVERS` to the framework root, a test that had been
# writing into its own tmp_path started overwriting the real
# `config/abandoned_branches.json`, destroying the three keys that document it —
# and the suite passed green throughout. The damage was found by reading a
# commit's diff. This is the assertion that was missing.
#
# Compared BEFORE against AFTER the suite, never against HEAD: uncommitted work
# in progress is the normal state of a development run, and a guard that fires
# on it is a guard that gets disabled rather than satisfied. Measured — the
# first version of this check compared against HEAD and failed on its own
# author's unstaged edits.
	cd $(AGENTS_DIR) && before=$$(git diff -- config/ hooks/ scripts/); \
	  $(PY) -m pytest tests/ -q || exit 1; \
	  bash tests/test_installer.sh || exit 1; \
	  after=$$(git diff -- config/ hooks/ scripts/); \
	  if [ "$$before" != "$$after" ]; then \
	    echo "❌ The test suite modified tracked files under config/, hooks/ or scripts/:"; \
	    git diff -- config/ hooks/ scripts/; \
	    exit 1; \
	  fi

# Deterministic docs freshness + integrity gate (rules/documentation_standard.md §4).
# Inspects the CALLER's tree, so run it from the host project root.
# SPRINT_ID defaults to the anchor's current_sprint.id. It used to default to
# empty, so the script fell back to sprint 0 and check_phase_artifacts returned
# immediately: the phase-artifact check never ran from make, in any project.
SPRINT_ID ?= $(shell python3 -c "import json;print(json.load(open('docs/active_state.json')).get('current_sprint',{}).get('id',0))" 2>/dev/null || echo 0)
docs-freshness-check:
	python3 $(AGENTS_DIR)/scripts/docs_freshness_check.py . $(SPRINT_ID)

# Session briefing for the active sprint (Sprint 035).
session-start:
	cd $(AGENTS_DIR) && python3 scripts/session_start.py

# Model ledger report (Sprint 037). Stub until scripts/model_ledger.py exists.
model-ledger:
	cd $(AGENTS_DIR) && if [ -f scripts/model_ledger.py ]; then \
	  python3 scripts/model_ledger.py; \
	else \
	  echo "model-ledger: deferred to Sprint 037"; \
	fi

# Propose Cursor model↔tier assignments from the on-disk catalogue (Sprint 026).
# Proposes only — never writes config/model_tiers.json. Design §D7: gate stays
# empty until proven history exists. --check (Sprint 035) fails if the gate is empty.
cursor-tiers:
	cd $(AGENTS_DIR) && python3 scripts/audit_cursor_models.py --check

# Sprint 027: verify a role left its required sprint-scoped artifacts (portable
# SubagentStop counterpart). SPRINT_DIR must be the canonical sprint path.
# Example: make role-artifacts ROLE='Orchestrator' SPRINT_DIR=docs/sprints/027-core-pipeline
ROLE ?=
SPRINT_DIR ?=
role-artifacts:
	@test -n "$(ROLE)" || (echo "ROLE= is required (registry role display name)"; exit 2)
	@test -n "$(SPRINT_DIR)" || (echo "SPRINT_DIR= is required"; exit 2)
	cd $(AGENTS_DIR) && python3 scripts/check_role_artifact.py --role "$(ROLE)" --sprint-dir "$(SPRINT_DIR)"
