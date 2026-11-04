# Rule Context: Skills and Integrations

This document asserts the governance laws when researching, registering, or escalating new operational tools or libraries within the host project.

## 1. Skill Discovery Escalation 
Agents requiring functions not natively available in standard language libraries must strictly follow this search protocol:
- **Priority 1 (Manifest Check)**: Query `skills/manifest_skills.json` locally to check if a previously approved script exists.
- **Priority 2 (The Local Bridge)**: Evaluate the locally downloaded bridge `skills/autoskills-3rd/` before going outside the workspace.
- **Priority 3 (External Discovery)**: If local tools fail, agents must query `https://skills.sh/`. Explicit human authorization under technical debate is mandatory before registering any new external elements.
- **Priority 4 (Creation Protocol)**: If the required function is fundamentally untraceable across the first three steps, the `Skill Architect` MUST forge the skill under the **Three-File Skill Standard**, choosing the destination per `skill_forge_workflow.md` (`forge_destination`): host `.claude/skills/` for project-specific tools (default), `profiles/[name]/skills/` for project-family tools, or the flat `.agents/skills/` for framework-wide tools — the latter two only through the nucleus branch→PR→tag flow.

## 2. Contamination Safeguards
- **Prohibited Installations**: Utilizing volatile dependency bridges at the root (e.g., executing `npx -y` outside isolated environments) is radically **PROHIBITED** to preserve deterministic operations and prevent root contamination. 
- **Domain Coupling Constraint**: If an introduced skill strictly serves the current project and not the entire global `.agents` capability matrix, it must permanently reside mapped directly inside the unified `skills/` directory, rejecting any sub-folder grouping or `/.local_skills/` unstandardized folders.

## 3. Third-party Immutability & Topology
- **Nomenclature Mandate**: Any third-party tool, vendor library, or external fork imported into the skill library MUST be explicitly identifiable via the `-3rd` string suffix appended to its directory name (e.g., `django-expert-3rd`).
- **Skill Documentation Veto**: Modifying, standardizing, or refactoring native README files or technical specifications of an imported external skill living in `skills/` is strictly prohibited. The upstream integrity of vendor technical instructions must remain completely virgin.

### SkillOpt `train_runner.py` — Canonical Invocation

`skills/skillopt/scripts/train_runner.py` is the single entry point of the vendored `skillopt` optimizer (Microsoft Research concept, isolated in `venv_skillopt/`). Three workflow steps invoke it — `workflows/audit_workflow.md` (`precision_audit`), `workflows/close_workflow.md` (`rules_optimization`), and `workflows/skill_forge_workflow.md` (`skillopt_run`). Those three steps **reference this subsection and do not restate the command** (`agents.md RA-14` spirit); each step supplies only its own trigger condition and its `<target>`.

- **Invocation form** (full path — never a bare `train_runner.py`, which resolves in no well-known directory): nucleus mode — `venv_skillopt/bin/python skills/skillopt/scripts/train_runner.py --skill <target> --config skills/skillopt/configs/agents_opt.yaml`; host session — `.agents/venv_skillopt/bin/python .agents/skills/skillopt/scripts/train_runner.py --skill <target> --config .agents/skills/skillopt/configs/agents_opt.yaml`. This mirrors the pathed-interpreter model of `rules/graphify.md` (`venv_skillopt/bin/python`, never the console-script).
- **Real arguments** (confirmed against `skills/skillopt/scripts/train_runner.py` on 2026-09-09): `--skill <target>` — the instruction/rules file under evaluation (`agents.md`, a `rules/*.md` file, or a freshly forged `SKILL.md`); `--config <path>` — the SkillOpt YAML config, canonically `skills/skillopt/configs/agents_opt.yaml`. `train_runner.py` reads only these two tokens directly; any further flags belong to the vendored `skillopt` PyPI modules (`scripts.train`, `scripts.eval_only`), which must be provisioned first (`skills/skillopt/SKILL.md` "Provisioning").
- **No dry-run mode exists.** There is no `--dry-run` flag and no `--eval-only` flag. The read-only path is the presence of `--skill`: `train_runner.py` sets `is_eval = "--skill" in sys.argv` and runs SkillOpt in "Evaluation-Only mode", which scores `<target>` and reports proposed edits instead of entering the rule-rewriting training loop. Omitting `--skill` starts the training loop, which **overwrites** `<target>` — that form is PROHIBITED for an audit or close pass.
- **Done-criterion**: exit code `0` **and** a written diff of the proposed edits recorded on the invoking step. The pass applies no edit itself; a human applies or rejects the diff afterwards. If the `skillopt` stack is not provisioned, record `<step-id> skipped: skillopt stack absent` and continue — absence is not a failure.
- **Authorization gate**: the command runs **only on explicit human authorization for that specific run** — chat approval or the Claude Code permission prompt (`agents.md §2 destructive_flags`; `skills/skillopt/SKILL.md` "Explicit Authorization"). It MUST NOT be issued inside an unattended `/loop` or `/schedule`.

## 4. Skill rules of agents.md (detail)

`agents.md §3` keeps each rule in brief and this section keeps the full text, moved in Sprint 059 (D18).

### three_file_standard

**Executable skills** (they ship a `/scripts/` folder) MUST adhere to the full Three-File Standard: 1. `README.md`, 2. `SKILL.md`, 3. `/scripts/` with `__init__.py`. **Knowledge skills** (pure guidance, no scripts) only require a `SKILL.md` with valid `name`/`description` frontmatter — padding them with empty scaffolding is PROHIBITED noise.

### topological_order

Skills flat inside `skills/`. Sub-layers (`core/`, `local/`) PROHIBITED. Illustrative project-family packs live under `profiles/[name]/` inside the submodule (e.g. `profiles/example-project/`). **Production profiles are never committed to the public nucleus** (`RA-15`): they live at a **host-controlled path** — convention `<host-root>/.agents-profile/` or a private directory the host names — and are linked via `scripts/install.py --profile-path <path>` (Sprint 028). The legacy `--profile <name>` flag resolves only `profiles/<name>` inside the submodule.

### enforcement

The official auditor for Three-File-Standard adherence is `skills/topology-monitor/scripts/legacy_app_auditor.py` (`workflows/audit_workflow.md` `skill_standard_check`, `Makefile` `verify`). `mass-standardizer` regenerates `skills/manifest_skills.json` — it is the manifest generator, not the adherence auditor.
