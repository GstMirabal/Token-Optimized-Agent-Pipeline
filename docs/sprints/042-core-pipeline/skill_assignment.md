# Skill Assignment — Sprint 042 (template-gate-parity)

Source: `docs/sprints/042-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/042-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

State the outcome of each rung. A ladder that terminates at an early rung says
so and leaves the rest as `not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | Terminates here — nothing to build | 34 registered entries enumerated; none renders a versioned template into a scratch directory and runs the gate that consumes it. The nearest neighbours are `token-saver-auditor` (owns one of the gates under test) and `mass-standardizer` (audits the Three-File Standard, whose object is a skill directory, not a template) |
| P2 | `autoskills-3rd` | not reached | Ladder terminated at P1 |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | not reached | Ladder terminated at P1 |
| P4 | Three-File Standard at Destination | not reached | Ladder terminated at P1 |

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
| U1 | None — targeted partial reads and `grep` over one document | N/A | Ladder terminated at P1 |
| U2 | None — stdlib `json` | N/A | Ladder terminated at P1 |
| U3 | None — stdlib `subprocess`, `shutil`, `tempfile`, `pathlib` | N/A | Ladder terminated at P1 |
| U4 | None — one line added to an existing target | N/A | Ladder terminated at P1 |
| U5 | `pytest` from `venv_skillopt/` (`agents.md §3 dependencies`) | N/A | Ladder terminated at P1 |
| U6 | `scripts/check_readme_counts.py --write` rewrites the counted block; the script is the authority over the numbers | N/A | Ladder terminated at P1 |
| U7 | None — authored from `docs/standards/templates/ADR_TEMPLATE.md` | N/A | Ladder terminated at P1 |

`Destination` for a forged skill: `host:.claude/skills/<name>/` (default),
`profile:<path>`, or `nucleus:PR`. Writing under `.agents/skills/` from a
host session is PROHIBITED (`strict_rule`).

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` | Its `scripts/audit_plan.py` is the Phase 1 and Phase 5 gate, and is also one of the three gates this sprint's instrument runs against a rendered template |
| `omni-context-minimizer` | `agents.md §2 ast_skeleton` — reserved for structural discovery on the files over 200 lines this sprint reads (`check_forge_ladder.py`, 296 lines; `check_task_scope.py`, 271). Phase 1 used targeted `grep` on argparse and artifact names instead of a full dump |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `mass-standardizer` | The official auditor of the Three-File Standard (`agents.md §3 enforcement`). Its object is a skill directory; this sprint's object is a template file and the gate that consumes it. No overlap |
| `sprint-architect` | Scaffolds sprint hierarchies. The `042` directory already exists from Phase 1 and the artifacts are authored from their own templates |
| `python-quality-auditor` | `ruff` is invoked directly per `agents.md §1 linter_command`; the Verification table names the exact command and its expected exit code |

## 5. Gaps

**None.** Every unit resolves to stdlib, an existing gate, or an existing script.
The one capability this sprint does not have — rendering a *workflow's prose*
against the gate that consumes it (the `pipeline_workflow.md` Phase 4.3 case from
Sprint 041) — is declared `Out of scope` in the plan with its destination, not
left as an unmet tool need.
