# Skill Assignment — Sprint 050 (deterministic-quality-instrument)

Source: `docs/sprints/050-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code** (nucleus), `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/050-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

State the outcome of each rung. A ladder that terminates at an early rung says
so and leaves the rest as `not reached`. This sprint's two computational units
(`U2` — `scripts/quality_audit.py`; `U6` — `scripts/session_state.py
set-topology`) are both `D3`-typed as `scripts/` instruments, not `skills/`
entries, so the ladder's question is answered as "no skill-forge is the
correct outcome" rather than assumed from the plan's own wording — the rungs
below were actually run, not deferred to `D3`.

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | No entry computes this capability; ladder terminates here regardless | 34 skills registered (`skills/manifest_skills.json` `version: 1.3.0`). None computes function length or block-nesting depth from an AST. The two nearest-named candidates, `skills/python-quality-auditor` and `skills/js-standardizer`, were read in full (`scripts/python_quality_auditor.py`, `scripts/js_standardizer.py`) — see §4 for why neither qualifies and neither is repurposed in place |
| P2 | `autoskills-3rd` | not reached | `node_modules/` is unprovisioned (`ls skills/autoskills-3rd/node_modules` → "No such file or directory"); the P1 outcome stands regardless because `D3` already fixes the target class as `scripts/`, which this rung (a skill-discovery bridge) cannot resolve regardless of its contents |
| P3 | `https://skills.sh/` (WebSearch) | Checked, no qualifying entry found | Two searches run: `python function length nesting depth ast audit` and `code complexity nesting depth deterministic linter skill`. Third-party complexity tools exist on adjacent registries (e.g. `pycleancode` — AST-powered nesting detection; `Code-Complexity-Scanner` on `terminalskills.io`), but none is an installable `skills.sh` entry that satisfies `D1`'s executable-line definition, `D2`'s AST-ancestor nesting definition, `D4`'s dual Python+JS/TS stdlib-only scan, or `RA-16`'s declared `invoked_by:` contract against `Makefile` `quality-audit`. None is a `.agents`-shaped skill; adopting one would still leave the `scripts/` vs `skills/` jurisdiction question open, which `D3` already closes |
| P4 | Three-File Standard at Destination | not applicable | `D3` names the target as a `scripts/` instrument with a declared `invoked_by:`, not a `skills/[name]/` directory; no skill is forged this sprint |

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
| U1 | None — `Edit` on `agents.md` `§1` rows (prose: unit of measure) | N/A | P1 |
| U2 | None — new `scripts/quality_audit.py`, stdlib `ast` (`D3`, `D4`); no skill computes this (§1, §4) | N/A | P1 |
| U3 | None — `Makefile` target addition | N/A | P1 |
| U4 | None — `config/invocation_exceptions.json` prose correction | N/A | P1 |
| U5 | None — `Edit` on `agents.md` `§1` rows, naming `scripts/quality_audit.py` | N/A | P1 |
| U6 | None — modifies existing `scripts/session_state.py`, adds `set-topology` subcommand (`D7`); not a skill target under `D3` | N/A | P1 |
| U7 | None — `Edit` on `workflows/close_workflow.md` prose | N/A | P1 |
| U8 | None — `Edit` on `workflows/deployment_workflow.md` prose | N/A | P1 |
| U9 | None — `Edit`/`capsys` assertions in an existing test file | N/A | P1 |
| U10 | None — regenerated by `python3 scripts/map_workflows.py`, never hand-edited | N/A | P1 |

`Destination` for a forged skill: `host:.claude/skills/<name>/` (default),
`profile:<path>`, or `nucleus:PR`. Writing under `.agents/skills/` from a
host session is PROHIBITED (`strict_rule`). This is a nucleus session and
forges nothing, so no destination is claimed.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` | `scripts/audit_plan.py` is the mandatory Phase 1 plan gate and a `make verify` step. Already exercised on this sprint's plan (`## Verification` row of `IMPLEMENTATION_PLAN.md`) |
| `omni-context-minimizer` | `agents.md §2 ast_skeleton` — candidate for structural discovery on any touched file exceeding 200 lines before a partial read (`scripts/session_state.py`, `scripts/cursor_adapter.py`-adjacent files); applied at Phase 6 execution, not at this Phase 4.2 discovery step |
| `python-quality-auditor` | **Measured, not invoked as a tool.** Read in full to answer this Phase's charter: confirms it shells to `ruff`/`mypy`/`bandit`/`radon`, prints one pass/fail line per tool, and its `main()` never calls `sys.exit()` — it returns normally regardless of failures, so the process exit code is always `0`. Computes no score, reads no AST, measures neither function length nor nesting depth |
| `js-standardizer` | Same role: read in full. Confirms it checks four lint-tool config filenames for presence and one repo-wide boolean (`"@param" in content or "@returns" in content` across any `.js`/`.ts` file), also never calling `sys.exit()`. Computes no score, measures neither function length nor nesting depth |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `skill-creator` | Forges skills. This sprint forges none — `D3` types both computational units as `scripts/` |
| `mass-standardizer` | Regenerates `skills/manifest_skills.json`. No skill is added, removed or renamed this sprint |
| `topology-monitor` | Audits Three-File-Standard adherence on `skills/`. No skill's file layout changes |
| **`python-quality-auditor` — repurpose in place** | Rejected on two independent grounds. **(a) Computational gap, not a defect fix.** Its entire logic is "shell out to an external binary and report its exit code"; it contains no AST parsing, no line-counting, no depth-counting — implementing `D1`/`D2` inside it is not a repair of `F-049-7`, it is writing `scripts/quality_audit.py`'s logic from scratch and pasting it into a different file. There is no smaller patch available. **(b) Jurisdictional mismatch even if rewritten.** `D3` requires the instrument to be a deterministic `scripts/` entry with a declared `invoked_by:` (`RA-16`) reachable from `Makefile` `quality-audit` without depending on a model electing to load a skill; `config/invocation_exceptions.json` classifies this skill's own entry as `"reason": "model-invoked"` for exactly that reason. Rewriting its body while it stays under `skills/` would leave the new logic exactly as unreachable-by-`make` as the old logic — the defect `F-049-7` measured. Moving the rewritten file to `scripts/` is indistinguishable from `U2` as planned; the skill directory would then be dead weight duplicating it. The skill stays as the model-invoked linter-wrapper it already is (`U4` corrects its invocation-exception note only) |
| **`js-standardizer` — repurpose in place** | Same two grounds. **(a)** Its logic is a config-filename existence check plus a single repo-wide substring search; it has no notion of a function boundary, so it cannot report *which* function is 51 executable lines or nested 4 levels deep — the substrate `D1`/`D2` require does not exist in this file to extend. **(b)** Same `model-invoked` vs. `scripts/`-deterministic jurisdictional mismatch as above, compounded by `D4`'s declared JS/TS scope: the real instrument must recognize `function` declarations, class methods and bound arrow functions and mark JSX/TS-type-level/decorator syntax `unparsed` rather than silently-compliant — a declared-limits contract this skill's substring heuristic has no path to satisfying without becoming a different program. Stays as the model-invoked config/JSDoc-presence helper it already is (`U4` corrects its note only) |
| A `skills.sh` third-party complexity scanner (e.g. `pycleancode`, `Code-Complexity-Scanner`) | Considered at P3. Rejected: none ships as a `skills.sh`-installable entry meeting `D1`/`D2`'s exact definitions (executable-line count excluding docstrings/comments; AST-ancestor nesting depth) or `D4`'s stdlib-only, dual-language, `unparsed`-declaring contract, and adopting an external tool would still need to resolve the `scripts/` vs `skills/` jurisdiction `D3` already settled — importing one would trade a measured gap (`F-049-7`) for an unmeasured external dependency, which `D4` ("No new dependency") independently forecloses |

**Conclusion on the discovery step**: no existing skill — local (`manifest_skills.json`),
bridged (`autoskills-3rd`, unprovisioned), or external (`skills.sh`) — computes
`D1`/`D2`'s function-length or nesting-depth metrics, and the two skills closest
in name to this sprint's subject cannot be repurposed into the real instrument
without (a) rewriting their entire logic from nothing, which is authoring
`scripts/quality_audit.py` under a different path, and (b) leaving that logic
under the `skills/` model-invoked jurisdiction the instrument's own `RA-16`
`invoked_by:` requirement (a deterministic `Makefile` target, not a model's
choice to load a skill) forbids. **Building `scripts/quality_audit.py` fresh,
as `D3`/`U2` specify, is correct** — not deferred to the plan's authority, but
independently reached by running the ladder this Phase owns.

## 5. Gaps

None. The ladder terminated at P1 with every unit resolved to either no tool
(`Edit`/`Read`/`grep` on existing files) or a fresh `scripts/` instrument whose
jurisdiction `D3` already fixes outside `skills/`. No skill is forged; no
existing skill is repurposed; the two skills flagged by `F-049-7` are corrected
in prose only (`U4`) and remain what they already are — model-invoked helpers
that do not compute what `agents.md §1` will, after `U5`, correctly attribute
to `scripts/quality_audit.py` instead.
