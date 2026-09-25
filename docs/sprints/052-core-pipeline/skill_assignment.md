# Skill Assignment — Sprint 052 (core-pipeline)

Source: `docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/052-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

State the outcome of each rung. A ladder that terminates at an early rung says
so and leaves the rest as `not reached`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | Hit | Every tool this sprint's 67 units require already exists and is registered: `omni-context-minimizer` (manifest line 199), `token-saver-auditor` (line 310), `python-quality-auditor` (line 210), `topology-monitor` (line 321), `mass-standardizer` (line 155), plus `scripts/quality_audit.py` (not a skill; deterministic project script named directly by the plan's own `D1`/`D8`/`D13`). Section 2 below resolves each unit against this rung. No unit surfaced a gap the manifest could not close |
| P2 | `autoskills-3rd` | Not reached | Ladder terminated at P1; no unit's need survived to this rung |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | Not reached | Ladder terminated at P1 |
| P4 | Three-File Standard at Destination | Not reached | Ladder terminated at P1; no gap remained to evaluate this rung |

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

**Outcome of this sprint's ladder run**: this sprint adds no dependency and forges
no skill. Every unit resolved at P1. Rungs P2–P4 are recorded `not reached` above
per `rules/skills_and_integrations.md §1`; no skill name or `SKILL.md` path is
claimed anywhere in this document.

---

## 2. Per-unit tool resolution

`Destination` is `N/A` for every row — no unit forges a skill this sprint, so no
row carries a forged-skill destination. Line counts below are `git`-tracked source
lines at `ca70bfa` (the plan's measurement commit); the `>200` threshold is
`agents.md §2 ast_skeleton` / `omni-context-minimizer`'s own trigger.

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| U1 | `omni-context-minimizer` (structural pass over 1702-line `021-030-program-queue.md` before the targeted edit) | N/A | P1 hit |
| U2, U5 | `omni-context-minimizer` (518-line `session_start.py`, 620-line `test_session_start.py`, both >200) | N/A | P1 hit |
| U3, U4 | `omni-context-minimizer` (497-line `session_state.py`, 225-line `test_session_state.py`, both >200) | N/A | P1 hit |
| U6, U7 | None — `start_workflow.md` (40 lines) and `commands/start.md` (8 lines) are under the 200-line trigger; direct targeted `Read`/`Edit` | N/A | P1 hit (no gap; native tools suffice) |
| U8, U14 | None — new-file creation (`ADR-0015`, `ADR-0016`); nothing pre-existing to structurally map | N/A | P1 hit (no gap) |
| U9 | None — `artifact_registry.json` (164 lines) and its test (110 lines) are under the trigger | N/A | P1 hit (no gap) |
| U10 | None — `pipeline_workflow.md` (42 lines) is under the trigger | N/A | P1 hit (no gap) |
| U11 | `omni-context-minimizer` (287-line `check_role_artifact.py` >200; its 166-line test is under) | N/A | P1 hit |
| U12, U13 | None — `graph_reconcile.py`/its test are new files; `Makefile` (149 lines) is under the trigger | N/A | P1 hit (no gap) |
| U15 | None — `agents.md` restated section is under the trigger and already held in session context (`§2 anti_amnesia`) | N/A | P1 hit (no gap) |
| U16 | `omni-context-minimizer` (904-line `on_commit.py`, 607-line test, both >200) | N/A | P1 hit |
| U17, U18 | None — `agents/qa_agent.md` (20 lines), `agents/tester_agent.md` (21 lines) are under the trigger | N/A | P1 hit (no gap) |
| U19 | `omni-context-minimizer` (554-line `verify_references.py`, 247-line test, both >200) | N/A | P1 hit |
| U20, U21 | None — `invocation_exceptions.json` (73 lines) and the new `quality_audit_exclusions.json` are under/absent | N/A | P1 hit (no gap) |
| U22 | `omni-context-minimizer` (367-line `quality_audit.py`, 257-line test, both >200) + `scripts/quality_audit.py` itself (the instrument under construction; self-measurement per `D8`) | N/A | P1 hit |
| U23, U26, U27, U29, U32, U33, U34, U35, U36, U37, U38, U39, U42, U43, U44, U45, U46, U47, U48, U53, U56, U57, U63, U64 (Wave 6, target file >200 lines) | `omni-context-minimizer` (structural pass before the targeted function edit) + `scripts/quality_audit.py` (measures the named functions back to compliance, `D1`/`D8`) | N/A | P1 hit |
| U24, U25, U28, U30, U31, U40, U41, U49, U50, U51, U52, U54, U55, U58, U59, U60, U61, U62 (Wave 6, target file ≤200 lines) | `scripts/quality_audit.py` only — target file already fits a direct targeted `Read`, `omni-context-minimizer` adds no discovery value under its own trigger | N/A | P1 hit |
| U65 | None — `agents.md` restated rows are under the trigger | N/A | P1 hit (no gap) |
| U66 | None — `Makefile` (149 lines) is under the trigger; wiring references `scripts/quality_audit.py`, already resolved at U22 | N/A | P1 hit (no gap) |
| U67 | `omni-context-minimizer` (1480-line `UPSTREAM_FINDINGS_FROM_HOSTS.md` >200) | N/A | P1 hit |
| K1..Kn (contingency, `D2`) | Same shape as the matching Wave 6 row above by the triggered file's own line count (`skill-creator/{scripts,eval-viewer}/*.py`); not yet measured — rows added to `task_scope.md` only if `D2` triggers | N/A | P1 hit (conditional; re-resolved if triggered) |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `omni-context-minimizer` | Mandatory structural pass (`agents.md §2 ast_skeleton`, `skills/omni-context-minimizer/SKILL.md`) before any targeted `Read` on the 200+-line files this sprint touches: `021-030-program-queue.md`, `session_start.py`/its test, `session_state.py`/its test, `check_role_artifact.py`, `on_commit.py`/its test, `verify_references.py`/its test, `quality_audit.py`/its test, the >200-line Wave 6 subjects, and `UPSTREAM_FINDINGS_FROM_HOSTS.md` |
| `scripts/quality_audit.py` (project script, not a skill — listed by name in the task's candidate set) | The sprint's own deliverable instrument: read for its current behaviour at U22, extended for exclusions/decorators at U22, and run against every Wave 6 function to confirm the named unit reaches compliance (`D1`, `D8`; Verification row `python3 scripts/quality_audit.py .; echo $?` → `0`) |
| `token-saver-auditor` | Sprint-level, not per-unit: runs against `IMPLEMENTATION_PLAN.md` before Phase 5 approval and at `make verify`, per the plan's own Verification table (`python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` → `0`) |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `python-quality-auditor` | Shells to `ruff`/`mypy`/`bandit`/`radon` and computes no score (`F-049-7`, corrected `config/invocation_exceptions.json:53`). This sprint's Out-of-scope table routes the `ruff` baseline, pin, and config to Sprint 054; no unit in 052 needs a `ruff`/`mypy`/`bandit` pass. The function-length/nesting instrument this sprint targets is `scripts/quality_audit.py`, already resolved above |
| `topology-monitor` | Its three scripts (`coverage_auditor.py`, `legacy_app_auditor.py`, `task_auditor.py`) are Wave 6 refactor **subjects** (U59–U61), not an instrument invoked by other units. No unit needs pipeline-health or task-progress monitoring beyond what `Makefile verify`/`audit_workflow.md` already run outside this sprint's scope |
| `mass-standardizer` | Manifest regeneration (`generate_manifest.py`) triggers on `SKILL.md` frontmatter (`name`/`description`/`category`/`tags`/`path`) drift. Wave 6's `R` units, including U52/U53 which refactor `mass-standardizer`'s own two scripts, are behaviour-preserving and touch no `SKILL.md` frontmatter anywhere — `skills/manifest_skills.json` needs no regeneration this sprint |
| `graphify` | `D5`'s `graph_reconcile.py` reads `graphify-out/graph.json` and `git ls-files` directly with the standard library, by the plan's own design record — no `graphify` skill/CLI invocation is part of that mechanism |
| `skill-creator` | No new skill is forged this sprint (P4 not reached). `skill-creator`'s own vendored files are the subject of provenance verification (`D2`, `U21`) and the contingency refactor wave (`K1..Kn`), never an invoked tool |
| `js-standardizer` | `js_standardizer.py` is a Wave 6 refactor subject (`U51`, complexity only, `D13`: `E722` kept unchanged in behaviour). No JS/TS lint work is in scope this sprint — routed to Sprint 053 (`KI-050-6`) |
| `env-shielding-auditor`, `compliance-checker` | Their scripts are Wave 6 refactor subjects only (`U50`, `U49`); no secret-scanning or rule-synthesis unit exists in this sprint's Work tables |
| `autoskills-3rd` (P2), `https://skills.sh/` (P3) | Ladder rungs not reached — every unit resolved at P1 |

## 5. Gaps

None. This sprint adds no dependency (`## Dependencies`: "None — `tree-sitter` is
Sprint 053's, `graph_reconcile.py` reads JSON and `git ls-files` with the stdlib").
Every unit resolved at rung P1 (§1, §2), so no skill is forged this sprint and the
external-lookup rung (`https://skills.sh/`) is recorded `not reached` rather than
attempted — the forge-ladder trail that rung would otherwise require does not
apply to a ladder that never reached it.
