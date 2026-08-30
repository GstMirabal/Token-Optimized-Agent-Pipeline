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

State the outcome of each rung. A ladder that terminates at an early rung says
so and leaves the rest as `not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | {{P1_RESULT}} | {{P1_EVIDENCE}} |
| P2 | `autoskills-3rd` | {{P2_RESULT}} | {{P2_EVIDENCE}} |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | {{P3_RESULT}} | {{P3_EVIDENCE}} |
| P4 | Three-File Standard at Destination | {{P4_RESULT}} | {{P4_EVIDENCE}} |

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
