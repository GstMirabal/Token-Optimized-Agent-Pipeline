# Skill Assignment — Sprint 053 (quality-instruments-and-seal-defects)

Source: `docs/sprints/053-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/053-core-pipeline`
(exit `2` rejects an empty build destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

State the outcome of each rung. A ladder that terminates at an early rung says
so and leaves the rest as `not reached`.

The sprint's one genuine new-capability question is Wave B (`KI-050-6`, unit
`B3`): a deterministic JS/TS complexity measurement, the only unit that asks
for a function not native to the standard library. Waves A, C and D are
direct bugfixes, a pinned-CLI wiring job, and governance-doc edits — none of
them ask the search protocol a question, so the ladder below is walked once,
for `B3`, and its outcome is read across to Wave C's `ruff` wiring in §3-§4.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | No compliant match | The manifest lists `python-quality-auditor` (Ruff/Mypy/Bandit wrapper) and `js-standardizer` (ESLint/Prettier/JSDoc alignment). Neither performs AST-based executable-line-count or block-nesting-depth measurement. `agents.md §1` already records that `python-quality-auditor` computes no numeric score and never exits non-zero, and that `js-standardizer` checks only for lint-config-file presence plus a single repo-wide boolean `@param`/`@returns` substring test — confirmed by reading `skills/js-standardizer/scripts/js_standardizer.py` and `skills/python-quality-auditor/scripts/python_quality_auditor.py` directly, 2026-09-27. |
| P2 | `autoskills-3rd` | Bridge not usable | `skills/autoskills-3rd/scripts/` holds only an empty `__init__.py`; no `node_modules/` and no `.bin/autoskills` are provisioned (`ls skills/autoskills-3rd/scripts/`, 2026-09-27), so the discovery engine described in its `SKILL.md` cannot run without a `pnpm install` step this sprint does not need. |
| P3 | `https://skills.sh/` (WebSearch, 2026-09-27) | No compliant listing found | Queries `site:skills.sh tree-sitter javascript typescript complexity linter skill` and `skills.sh ruff python lint skill marketplace` returned generic TypeScript/lint-config skills on skills.sh (e.g. `skills.sh/sickn33/antigravity-awesome-skills/lint-and-validate`, `skills.sh/ofershap/typescript-best-practices`) and `ruff`-wrapper skills hosted on other marketplaces (LobeHub, Smithery, mcpmarket) — none on skills.sh itself, and none of the returned listings perform the `D3` ancestor-node executable-line/block-nesting-depth measurement or the `ruff.toml` ↔ exclusions-file parity check Wave C needs. |
| P4 | Three-File Standard at Destination | Not applicable | Design `D3`-`D5` of the approved Implementation Plan already route the capability into the existing core script `scripts/quality_audit.py` as a pinned library dependency (`tree-sitter`, `tree-sitter-javascript`, `tree-sitter-typescript`, listed in `requirements-quality.txt`), authored by `implementer_agent` per `agents.md §6`. No new skill under `skills/` was built for this sprint. |

**When this sprint builds nothing, change none of the wording above.** It is
written the way it is on purpose. `scripts/check_forge_ladder.py` decides whether
a build is being claimed by pattern-matching this file's prose, so a template
that *describes* the claim in the claim's own words is read as *making* it —
and the check then demands a skill name a blank template cannot carry.

> Until Sprint 041 this section's header column and its fourth row did exactly
> that, and the template copied unedited failed the Phase 4.2 gate that consumes
> it (`exit 2`). Two further attempts to document the repair re-broke it, by
> quoting the offending strings and by pasting a literal example trail. Hence the
> abstractions above: describe the shape, never spell out an instance.
>
> The detector is correct and is not relaxed. What changed is that the template
> stopped announcing work that had not happened.

---

## 2. Per-unit tool resolution

Units are grouped by identical resolution (`agents.md §2 token_saver`) rather
than repeated 67 times with the same answer; every unit of Sprint 053 is
covered by exactly one row below.

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| A1–A4 | None — direct bugfix on governed core files (seal vocabulary, deploy-unlock path) | N/A | Ladder not asked a question: the search protocol (`rules/skills_and_integrations.md §1`) triggers on a capability absent from the standard library; these are logic corrections in already-owned scripts. |
| B1–B2 | None — dependency-manifest edits (`requirements-quality.txt`, `requirements-core.txt`) | N/A | Not triggered. |
| B3 | `tree-sitter` + `tree-sitter-javascript` + `tree-sitter-typescript` (pinned library dependency, `D3`-`D5`) — not a skill | N/A (core script `scripts/quality_audit.py`) | Full climb recorded in §1: P1 no compliant match, P2 bridge not usable, P3 no compliant listing found, P4 not applicable (delivered as a core-script dependency, no skill built). |
| B4–B5 | None — test fixtures and CI wiring | N/A | Not triggered. |
| C01–C03 | None — `ruff.toml` config, its parity test, and a doc-ordering fix | N/A | See §3-§4 for why `python-quality-auditor` does not cover `ruff.toml` authoring or `make verify` wiring. |
| C04–C55 | `ruff` `0.16.3` (pinned CLI dependency, `D6`) — direct binary invocation on each named file, not a skill | N/A | P1 considered `python-quality-auditor` (shells to the same `ruff` binary) and rejected it — see §4. P2/P3 as recorded in §1 (a generic wrapper skill would not satisfy `D8`'s file-by-file, behaviour-preserving remediation or the `≤10 noqa` cap). P4 not applicable: each unit is a direct code edit, verified by `ruff check <file>` exiting `0`. |
| C56 | None — `Makefile` wiring (`ruff check .`, `quality_audit.py`) | N/A | Not triggered. |
| D01–D02 | None — governance-doc and roadmap edits | N/A | Not triggered. |

`Destination` for a built skill: `host:.claude/skills/<name>/` (default),
`profile:<path>`, or `nucleus:PR`. Writing under `.agents/skills/` from a
host session is PROHIBITED (`strict_rule`). No row above needs a `Destination`
value, because no row builds a skill.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` | Its structural gate (`skills/token-saver-auditor/scripts/audit_plan.py`) is already wired into this sprint's own Verification table against `IMPLEMENTATION_PLAN.md`, and the plan's Cost section pre-empts its Filter 3 concern (monolithic-plan) by splitting the 67-unit sprint into per-wave subagent batches with a stated session-cost checkpoint. Listed here as a governance gate on the plan, not as a Work-unit execution tool — no Work unit in §2 invokes it. |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `python-quality-auditor` | Reading `skills/python-quality-auditor/scripts/python_quality_auditor.py` confirms it shells to `ruff check .`, `mypy .`, `bandit -r .` and `radon cc . -a` via `subprocess.run(..., shell=True)` and only prints a pass/fail line per tool — it computes no numeric score and the process never calls `sys.exit` with a non-zero code (`agents.md §1`, `F-049-7`). Wave C needs a deterministic exit-code gate (`ruff check .` exits `0`, wired into `make verify`), which `C56` delivers directly via the `Makefile` and a pinned `ruff.toml`, not through this skill. |
| `js-standardizer` | Reading `skills/js-standardizer/scripts/js_standardizer.py` confirms it walks the tree for `.js`/`.ts` files and checks only for the substring `@param` or `@returns` anywhere in each file — a repo-wide boolean, not per-function JSDoc coverage, and no AST parsing at all. It cannot produce the executable-line count or block-nesting depth `D3` requires, and the nucleus ships no JS/TS of its own for it to standardize (Out of scope, Implementation Plan: *"JS/TS `pnpm run lint` — A host concern. The nucleus ships no JS/TS."*). |
| `omni-context-minimizer` | Considered for the Wave C 52-file remediation pass. Not assigned as a mandatory step because `jurisdictional_lock`/`D8` already scope each `C`-unit to one named file with its finding count pre-measured (`ruff check <file> --output-format concise`), so `implementer_agent` reads the flagged lines directly rather than performing whole-file structural discovery on an unfamiliar codebase — the case this skill targets. It remains available per `agents.md §2 ast_skeleton` for any individual file over 200 lines that needs a full skeleton before an edit. |
| `topology-monitor` | Its `legacy_app_auditor.py` is the enforcement auditor for Three-File-Standard adherence on newly scaffolded skills/apps (`agents.md §3 enforcement`). Sprint 053 builds no skill and adds no app; `C25`-`C39` only clear lint findings inside already-compliant `skills/*/scripts/*.py` files, so there is no topology change to audit. |
| `mass-standardizer` | Regenerates `skills/manifest_skills.json` when a skill's file set changes. No unit in this sprint adds, removes, or renames a skill file, so the manifest stays correct as-is. |
| `autoskills-3rd` (P2 rung) | Covered in §1: the bridge is present but unprovisioned, and the sprint's `tree-sitter` need was resolved by a pinned dependency in an existing core script before a P2/P3 external-tool answer was needed for anything else. |

## 5. Gaps

None. The sprint's two genuine tool needs — a JS/TS complexity measurement
(Wave B) and a Python lint gate (Wave C) — are both delivered as pinned
dependencies wired directly into existing core mechanisms (`scripts/quality_audit.py`,
`Makefile`), owned by `implementer_agent`/`rule_validator` per `agents.md §6`,
not through `skills/`. No skill was built for Sprint 053, and no unit in
Waves A-D is left without a stated tool resolution.
