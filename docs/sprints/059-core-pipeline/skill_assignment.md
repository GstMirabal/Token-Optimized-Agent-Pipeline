# Skill Assignment — Sprint 059 (efficiency-and-sandbox-regime)

Source: `docs/sprints/059-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/059-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

The ladder terminates at the first rung. Every unit of the plan's Work tables is
served by a tool already present in `skills/`, by the Python standard library, by
`git`/`make`/`venv_skillopt/bin/python`, or by editing an existing file. The
plan's Dependencies table adds no package. Rungs two to four are `not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | hit — every unit resolved (section 2) | `skills/manifest_skills.json` lists `token-saver-auditor`, `omni-context-minimizer`, `mass-standardizer`, `graphify`, `topology-monitor` |
| P2 | `autoskills-3rd` | not reached | ladder terminated at P1 |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | not reached | ladder terminated at P1 |
| P4 | Three-File Standard at Destination | not reached | ladder terminated at P1 |

**When this sprint builds a new skill**, the third rung's outcome MUST be recorded
as a machine-readable trail — a JSON object carrying `source`, `query` and a
boolean `hit`, shaped `{"source": "skills.sh", "query": "<term>", "hit": <bool>}`
with `<bool>` replaced by the real value. No HTTP in `make verify`.
`scripts/check_forge_ladder.py` requires that trail beside a named skill and its
`SKILL.md` path, and exits `2` without it.

> **When this sprint builds nothing, change none of the wording above.** It is
> written the way it is on purpose. `scripts/check_forge_ladder.py` decides whether
> a build is being claimed by pattern-matching this file's prose, so a template
> that *describes* the claim in the claim's own words is read as *making* it —
> and the check then demands a skill name a blank template cannot carry.
>
> Until Sprint 041 this section's header column and its fourth row did exactly
> that, and **the template copied unedited failed the Phase 4.2 gate that consumes
> it** (`exit 2`). Two further attempts to document the repair re-broke it, by
> quoting the offending strings and by pasting a literal example trail. Hence the
> abstractions above: describe the shape, never spell out an instance.
>
> The detector is correct and is not relaxed. What changed is that the template
> stopped announcing work that had not happened.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| A-09, A-10, A-11, A-12, D-02, D-03 | `omni-context-minimizer` (`skills/omni-context-minimizer/scripts/omni_minimizer.py`) for the skeleton of `agents.md` and each receiving file before partial reads (`agents.md §2 ast_skeleton`); `wc -c` and `make verify` per row (plan D10) | N/A | P1 hit |
| A-05, A-11, B-02, A-00, A-06, A-07, C-01, C-02, D-01, F-01, Z-01, Z-02 | none — Markdown edits by `doc_orchestrator`; ADRs from `docs/standards/templates/ADR_TEMPLATE.md` | N/A | P1: no tool needed |
| A-08 | none — frontmatter edit; `scripts/check_model_tiers.py` verifies the companion `config/model_tiers.json` | N/A | P1: no tool needed |
| A-01, A-02 | `scripts/session_cost.py` (the subject); `venv_skillopt/bin/python -m pytest` | N/A | P1: no tool needed |
| G-01, H-02 | `scripts/check_task_scope.py` (the subject); stdlib only | N/A | P1: no tool needed |
| H-01 | `scripts/session_cost.py --json` (A-00 figures) | N/A | P1: no tool needed |
| G-02, A-04 | none — workflow edit; `scripts/map_workflows.py` regenerates `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` (`make verify` gates its staleness) | N/A | P1: no tool needed |
| A-03 | `token-saver-auditor` (`skills/token-saver-auditor/scripts/audit_plan.py`) to confirm the amended §3.1 still matches the plan audit | N/A | P1 hit |
| B-01 | stdlib JSONL reader over Claude Code transcripts | N/A | P1: no tool needed |
| B-06, D-04, E-01b, E-02 | `scripts/install.py`, `scripts/merge_json.py` (existing bridge) | N/A | P1: no tool needed |
| E-01 | `scripts/session_state.py` (the subject) | N/A | P1: no tool needed |
| B-03, B-05 | `scripts/py_compile_tree.py`, `Makefile` (the subjects) | N/A | P1: no tool needed |
| B-04 | `mass-standardizer` (`skills/mass-standardizer/scripts/generate_manifest.py`, the subject) | N/A | P1 hit |
| E-03 | `git ls-remote` to resolve each action tag to its commit SHA | N/A | P1: no tool needed |
| F-02 | `scripts/check_role_artifact.py` reads `config/artifact_registry.json` after the edit | N/A | P1: no tool needed |
| I-01..I-07 | `scripts/check_fix_reproduces.py` (Gate 1 first check) for every paired test | N/A | P1: no tool needed |
| All units | `graphify` (`graphify-out/graph.json`) before any recursive search (`agents.md §2 graph_sovereignty`); `topology-monitor` via `make verify` | N/A | P1 hit |

`Destination` for a forged skill: `host:.claude/skills/<name>/` (default),
`profile:<path>`, or `nucleus:PR`. Writing under `.agents/skills/` from a
host session is PROHIBITED (`strict_rule`).

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `omni-context-minimizer` | `agents.md` (53907 bytes) and the receiving rule files exceed 200 lines; skeleton first (`§2 ast_skeleton`) |
| `token-saver-auditor` | `audit_plan.py` gates the plan at Phase 1 and Phase 5; A-03 re-checks §3.1 against it |
| `mass-standardizer` | B-04 adds `--check` to its manifest generator |
| `graphify` | dependency discovery before recursive search (`§2 graph_sovereignty`); rebuilt at close (`§2 graph_sync`) |
| `topology-monitor` | Three-File Standard audit inside `make verify` |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `python-quality-auditor` | model-invoked and computes no score (`agents.md §1 linter_command`); `make verify` already gates `ruff` and `make quality-audit` |
| `sprint-architect` | the sprint directory and branch already exist (Phase 3 done by `session_state.py open-sprint`) |
| `skill-creator` | no skill is forged this sprint |
| `env-shielding-auditor` | C-01 measures sandbox entry points (`RA-19`), not `.env` handling; no unit reads `.env` |

## 5. Gaps

None.
