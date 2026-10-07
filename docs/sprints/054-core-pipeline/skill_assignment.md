# Skill Assignment — Sprint 054 (host-intake-gates-and-sprint-state)

Source: `docs/sprints/054-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/054-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

State the outcome of each rung. A ladder that terminates at an early rung says
so and leaves the rest as `not reached`.

The question put to the ladder, once per new mechanism of the plan: **does an existing skill or script already do this?** Two mechanisms are new: `scripts/check_fix_reproduces.py` (red/green replay of `fix(` commits in a temporary git worktree, unit A03) and `scripts/install_lock.py` (SHA-256 lock over a requirements set, unit B04).

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | no match for either mechanism | 34 entries read, name and description of each. Nearest candidates and why they do not cover it are in §4. `ls skills/*/scripts` has no file named for replay, repro, lock or fix |
| P2 | `autoskills-3rd` | no match | `skills/autoskills-3rd/` ships `scripts/__init__.py` only (the discovery binary lives in an unprovisioned `node_modules/`, which is not committed); its `SKILL.md` describes a scan of the local arsenal, which is the P1 list already read |
| P3 | `https://skills.sh/` (WebSearch/WebFetch; simulated JSON allowed in tests) | no match | Two WebSearch queries on 2026-10-04: (a) skill that replays a `fix` commit's test on the parent commit in a git worktree → results were issue reports about agent skills that misbehave inside worktrees, none is a replay tool; (b) skill that locks a requirement set by SHA-256 → results were lockfiles for the **skills themselves** (`skills-lock`, `skills.lock`), which hash installed skill directories, not a `requirements-*.txt` set |
| P4 | Three-File Standard at Destination | not reached | Both mechanisms are framework scripts under `scripts/`, authored by `implementer_agent` in units A03 and B04. Neither is a skill: each has a fixed command-line contract and a declared `invoked_by:` (`RA-16`), and neither needs model-invoked guidance. No Three-File skill folder is created |

No skill was forged in this phase. The plan's Mechanisms table already names an
`invoked_by:` for each script, so the invocation coverage check
(`scripts/verify_references.py` check (d)) is satisfied without a skill registration.

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

Legend: `none` means no skill is invoked and the assignee works with its native
file tools and the sanctioned scripts named in the row. `Destination` is `N/A`
on every row: nothing is built outside the files the plan already names.

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| W01 | none (native file edit; `rules/documentation_standard.md`; `RA-15` genericization by hand) | N/A | P1 no match → ladder ends, not needed |
| W02 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |
| A01 | none; verification with `venv_skillopt/bin/python -m pytest tests/test_quality_audit.py` and `make quality-audit` | N/A | P1 no match → ladder ends, not needed |
| A02 | none; `hooks/on_commit.py` is the subject, pytest is the check | N/A | P1 no match → ladder ends, not needed |
| A03 | none; new framework script authored by `implementer_agent` (stdlib `subprocess`, `tempfile`, `git worktree`). Existing-tool check: no skill or script covers it (§1, §4) | N/A | P1, P2, P3 no match; P4 not reached (script, not skill) |
| A04 | none (native file edit of `agents/qa_agent.md`) | N/A | P1 no match → ladder ends, not needed |
| A05 | none; `compliance-checker` MAY be run over the edited rule as a read-only check | N/A | P1 hit for the optional check only |
| A06 | none; same optional `compliance-checker` read | N/A | P1 hit for the optional check only |
| A07 | none (template edit); consumer check is A08's `audit_plan.py` | N/A | P1 no match → ladder ends, not needed |
| A08 | `token-saver-auditor` — it is the **subject** (`skills/token-saver-auditor/scripts/audit_plan.py` is modified), not a tool applied to other work | N/A | P1 hit (existing skill, extended in place) |
| A09 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |
| A10 | none (template creation); `readme-standardizer` rejected, §4 | N/A | P1 no match → ladder ends, not needed |
| A11 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |
| A12 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |
| B01 | none; pytest | N/A | P1 no match → ladder ends, not needed |
| B02 | none; pytest | N/A | P1 no match → ladder ends, not needed |
| B03 | none; pytest | N/A | P1 no match → ladder ends, not needed |
| B04 | none; new framework script authored by `implementer_agent` (stdlib `hashlib`). Existing-tool check: no skill or script covers it (§1, §4) | N/A | P1, P2, P3 no match; P4 not reached (script, not skill) |
| B05 | none; pytest | N/A | P1 no match → ladder ends, not needed |
| B06 | none (native file edit; `tests/test_cursor_adapter.py` as regression guard) | N/A | P1 no match → ladder ends, not needed |
| B07 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |
| B08 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |
| C01 | none (native file edit); `env-shielding-auditor` rejected, §4 | N/A | P1 no match → ladder ends, not needed |
| C02 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |
| Z01 | none (template-based create) | N/A | P1 no match → ladder ends, not needed |
| Z02 | none (native file edit; each entry cites a short SHA, `agents.md §0`) | N/A | P1 no match → ladder ends, not needed |
| Z03 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |
| Z04 | none (native file edit) | N/A | P1 no match → ladder ends, not needed |

Cross-cutting tools used by every code unit (A01-A03, A08, B01-B05), not repeated per row:
`omni-context-minimizer` before any read of a file above 200 lines (`agents.md §2 ast_skeleton`;
`scripts/session_state.py`, `hooks/on_commit.py` and `scripts/quality_audit.py` qualify), and
`make verify` (which already runs `ruff`, `make quality-audit` and the Three-File auditor) at each wave's end.

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `token-saver-auditor` | Unit A08 modifies its `audit_plan.py`; it is also the Phase 1/Phase 5 plan check named in the plan's Verification table |
| `omni-context-minimizer` | Structural skeleton of `scripts/session_state.py`, `hooks/on_commit.py`, `scripts/quality_audit.py` before targeted reads (A01, A02, B01-B03, B05) |
| `compliance-checker` | Optional read-only pass over the rule edits A05, A06 and C01 (optional: no unit depends on it) |
| `graphify` | `graph_sync` after the code units (`venv_skillopt/bin/python -m graphify update .`), per `agents.md §2` |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `python-quality-auditor` | Shells to `ruff`/`mypy`/`bandit`/`radon`; never replays a test against a parent commit. `make verify` already gates `ruff` directly |
| `django-tdd-3rd`, `django-verification-3rd` | Django-specific TDD and verification loops; they describe running a suite, not proving that a test is red on the parent tree. Third-party and immutable (`skills_and_integrations.md §3`) |
| `topology-monitor` | Audits pipeline health and the Three-File Standard; no replay and no hash of requirements |
| `mass-standardizer` | Regenerates `skills/manifest_skills.json`; unrelated to either script |
| `env-shielding-auditor` | Scans for hardcoded secrets; C01 edits a package-manager configuration rule, not secrets handling |
| `readme-standardizer` | A10 creates a template under `docs/standards/templates/`, not a README |
| `js-standardizer`, `nodejs-best-practices`, `nodejs-backend-patterns` | C01 documents `pnpm-workspace.yaml` keys in a governance rule; no JS/TS code is written |
| `sprint-architect`, `skill-creator`, `skillopt` | Planning is finished, no skill is created, no prompt optimization is in scope |
| Existing scripts as partial matches for the two new mechanisms | `scripts/check_venv_relocatable.py` mentions `installed.lock` only in its docstring and neither writes nor checks it. `hashlib.sha256` appears in `scripts/loop_guard.py` and `scripts/cursor_adapter.py` for unrelated digests (pattern reference, not reusable). Hotfix `H-006` replayed one test in a detached worktree **by hand**; no script resulted. `pip --require-hashes` hashes downloaded distributions and needs a fully pinned file, so it cannot detect that the requirement **set** changed (`KI-053-1`) |
| External P3 results (`skills-lock` family) | Lock the installed *skills*, not a Python requirement set; adopting one would add an `npx` dependency, which `skills_and_integrations.md §2` prohibits |

## 5. Gaps

**Existing-tool finding: none.** No existing skill or script covers
`scripts/check_fix_reproduces.py` or `scripts/install_lock.py`; the plan stands
as written, and units A03 and B04 are justified as new framework scripts. The two
closest existing artefacts are in §4 (`H-006` manual replay, `check_venv_relocatable.py`
docstring) and neither is reusable.

No skill gap. The only open point is not a tool gap: A03 and B04 add `invoked_by:`
declarations that `scripts/verify_references.py` check (d) will read, so those
module docstrings are part of the units' done-criterion.
