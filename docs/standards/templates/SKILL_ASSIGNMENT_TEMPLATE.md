# Skill Assignment — Sprint {{SPRINT_ID}} ({{SPRINT_SLUG}})

Source: `docs/sprints/{{SPRINT_ID}}-{{STACK}}-{{LAYER}}/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **{{SESSION_TOOL}}**, `delegation_mode: {{DELEGATION_MODE}}`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/{{SPRINT_ID}}-{{STACK}}-{{LAYER}}`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

| Rung | Source | Result (hit / miss / skipped) | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | {{P1_RESULT}} | {{P1_EVIDENCE}} |
| P2 | `autoskills-3rd` | {{P2_RESULT}} | {{P2_EVIDENCE}} |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | {{P3_RESULT}} | {{P3_EVIDENCE}} |
| P4 | Three-File forge at Destination | {{P4_RESULT}} | {{P4_EVIDENCE}} |

A simulated P3 miss for deterministic checks may be recorded as JSON, e.g.
`{"source":"skills.sh","query":"<term>","hit":false}` — no HTTP in `make verify`.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| {{ID}} | {{SKILL_OR_NONE}} | {{DESTINATION_OR_N/A}} | {{TRAIL}} |

`Destination` for a forged skill: `host:.claude/skills/<name>/` (default),
`profile:<path>`, or `nucleus:PR`. Writing under `.agents/skills/` from a
host session is PROHIBITED (`strict_rule`).

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| {{NAME}} | {{REASON}} |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| {{NAME}} | {{REASON}} |

## 5. Gaps

{{GAPS_OR_NONE}}
