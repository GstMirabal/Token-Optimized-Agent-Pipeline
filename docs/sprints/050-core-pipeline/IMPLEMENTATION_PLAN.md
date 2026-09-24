# Implementation Plan: Sprint 050 — deterministic-quality-instrument

**Canonical path**: `docs/sprints/050-core-pipeline/IMPLEMENTATION_PLAN.md`
**Branch**: `ai-sprint/050` · **Base**: `main` at `753fbe1`
**Status**: `DRAFT` → `APPROVED` → `EXECUTING` → `CLOSED`

> Authored at Phase 1 (Planning) by `principal_agent`, extracted to this path at
> Phase 3, and **committed before Phase 5 approves it**: `agents.md §2 triple_lock`
> names the approved Implementation Plan as its first lock, and a lock cannot close
> over an artifact that does not exist.
>
> Spanish is permitted in this document (`agents.md §1 user_chat`). Every other
> pipeline artifact is English.

---

## Context

`agents.md §1` carries four rows that state a standard and name no instrument that
measures it: the Python style-score (`linter_command`), the JS/TS style-score
(`linter_command`), `max_indentation` (3 levels) and `max_lines_per_func` (50 lines).
Sprint 049 (`F-049-7`) measured that the two skills previously credited with
enforcing them compute nothing of the sort — `skills/python-quality-auditor/scripts/python_quality_auditor.py`
shells to `ruff`/`mypy`/`bandit`/`radon` and prints one pass/fail line per tool;
`skills/js-standardizer/scripts/js_standardizer.py` checks lint-config file presence
plus one repo-wide boolean. Neither computes a score, reads indentation depth,
measures function length, or exits non-zero. Sprint 049 corrected the governance
text to say so honestly and routed the real instrument here (`KI-049-4`,
`docs/roadmaps/core/pipeline/021-030-program-queue.md:297`).

Measured, with the command that reproduces each:

| Figure | Value | Reproduce |
| :--- | :--- | :--- |
| `make verify` steps checking indentation, function length or a style score | 0 | `grep -n 'ruff check\|pnpm run lint\|indent\|max_lines\|lines_per' Makefile` |
| First-party JS/TS source files in this repository | 0 | `find . \( -name '*.js' -o -name '*.ts' -o -name '*.jsx' -o -name '*.tsx' -o -name '*.mjs' -o -name '*.cjs' \) -not -path './venv_skillopt/*' -not -path './node_modules/*' -not -path './.git/*' \| wc -l` |
| `scripts/cursor_adapter.py:480 install_cursor_bridge` against the 50-line row | 56 raw / 28 executable | Sprint 049 Phase 7 round 2, recorded at `021-030-program-queue.md:302` |
| Instrument writing `topology_version` into `docs/active_state.json` | none | `grep -rn 'topology_version' scripts/ hooks/` |

When this sprint is done: `python3 scripts/quality_audit.py` exists, measures
function length and nesting depth deterministically for Python (stdlib `ast`) and
JS/TS, exits `2` on violation, and is reachable through `make quality-audit`;
`agents.md §1` states the unit each magnitude is measured in and names that
instrument; and `topology_version` is written by a command rather than by prose.

---

## Design

**D1 — `max_lines_per_func` is measured in executable lines, not raw span.**
Executable lines = statements in the function body, excluding blank lines,
comment-only lines and the docstring. **Decided (human, Phase 1): executable
lines.** Rejected alternative: raw span (last line − first line). Raw span
penalises the documentation `agents.md §1 python_style` mandates — Google-style
`Args:`/`Returns:` blocks — so one rule would red another. Evidence:
`install_cursor_bridge` is 56 raw / 28 executable and sat ambiguously against the
row for a full sprint because no unit was declared.

**D2 — `max_indentation` is measured as block-nesting depth from the module root,
counted over `ast` ancestors, not over columns.** A statement's level is the number
of block-introducing ancestors (`FunctionDef`, `AsyncFunctionDef`, `ClassDef`, `If`,
`For`, `While`, `With`, `Try`, `Match`) between it and the module. A module-level
`def` body is level 1; the limit of 3 is exceeded at level 4. Rejected alternative:
character columns ÷ 4, which reports a false violation on any continuation line or
non-4-space file.

**D3 — The instrument is a script under `scripts/`, not a skill.** `scripts/` holds
deterministic instruments with a declared `invoked_by:` (`RA-16`); `skills/` are
model-invoked (`config/invocation_exceptions.json`). The defect `F-049-7` found was
precisely a deterministic claim resting on a model-invoked call. The two existing
skills stay model-invoked helpers and are not deleted; only their exception notes
are corrected.

**D4 — No new dependency.** Python uses stdlib `ast`. JS/TS uses a deterministic
brace-depth and function-header scanner in stdlib Python. **Declared limit, written
into the script docstring and into `agents.md §1`**: the JS/TS path recognises
`function` declarations, class methods and arrow functions assigned to a binding; it
does not parse JSX, TypeScript type-level syntax, or decorators, and it reports
those files as `unparsed` rather than as compliant. A file counted as compliant
because the parser did not understand it is the `F-049-7` failure repeated.

**D5 — The verify-wiring is decided by measurement, and both branches are declared
here so neither is renegotiated under sunk cost.** After `U2` lands, run the
auditor over this repository. **Branch A** (violations = 0): `U3` adds
`quality-audit` to `make verify`. **Branch B** (violations > 0 but ≤ 20% of
first-party Python functions): **decided (human, Phase 1) — this is the path if
the baseline is not clean.** `U3` ships the standalone target only, the violating
units are listed in `SPRINT_LOG.md`, and their remediation is routed to Sprint 051 —
precedent for a deliberate non-`verify` target exists (`bridge-state`,
`cursor-era-audit`, each with its stated reason in `Makefile`). **Branch C**
(> 20%): `Abort criterion` applies.

**D6 — Test fixtures are inline source strings written to `tmp_path`, not committed
fixture files.** Matches the existing suite convention (`tests/test_audit_cursor_models.py`
uses `tmp_path` throughout) and avoids a fixture directory that `jurisdictional_lock`
would have to claim as a structural subject.

**D7 — `topology_version` gets a writer, not a hand-edit.** `docs/active_state.json`
is gitignored (`.gitignore:55`), so its value cannot be an atomic commit; the
committable defect is that no instrument writes the field and two workflows name it
only in prose. `U6` adds `session_state.py set-topology`, deriving the value from
the newest sealed `## [X.Y.Z]` section of `CHANGELOG.md` plus `current_sprint.id`
and `current_sprint.status`, in the documented format `X.Y.Z-NNN-<status>`. `U7`
and `U8` make `close_workflow.md` and `deployment_workflow.md` invoke it as separate
invocations (`RA-13`). The current wrong value (`4.31.0-049-closed`) is corrected by
running that command, and the correction is evidenced in `PHASE_REGISTER.md`.

**D8 — `agents.md` is the structural subject of two units, `U1` and `U5`, landing in
sequence.** `agents.md §2 jurisdictional_lock` caps *concurrent* claims on a subject,
never lifetime touches (Phase 014 `T21`/`T22` precedent; restated in Sprint 048).
`U1` writes the unit of measure, which is the contract `U2` implements; `U5` can only
be written after `U2` exists, because it replaces "**No instrument exists for this
row today**" with the instrument's name. Recorded here because the opposite reading
of this rule cost Sprint 046 a mislabelled commit and Sprint 047 a mid-execution
re-pairing.

---

## Work

| # | File | Operation | Risk | Assignee (proposed) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| U1 | `agents.md` | modify | medium | `doc_orchestrator` | ⏳ |
| U2 | `scripts/quality_audit.py` (+ paired `tests/test_quality_audit.py`, same commit) | create | high | `implementer_agent` | ⏳ |
| U3 | `Makefile` | modify | medium | `implementer_agent` | ⏳ |
| U4 | `config/invocation_exceptions.json` | modify | low | `implementer_agent` | ⏳ |
| U5 | `agents.md` | modify | medium | `doc_orchestrator` | ⏳ |
| U6 | `scripts/session_state.py` (+ paired `tests/test_session_state.py`, same commit) | modify | high | `implementer_agent` | ⏳ |
| U7 | `workflows/close_workflow.md` | modify | medium | `doc_orchestrator` | ⏳ |
| U8 | `workflows/deployment_workflow.md` | modify | medium | `doc_orchestrator` | ⏳ |
| U9 | `tests/test_audit_cursor_models.py` | modify | low | `implementer_agent` | ⏳ |
| U10 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | modify | low | `implementer_agent` | ⏳ |

**Unit content**

- **U1** — `§1` rows `max_lines_per_func` and `max_indentation` state their unit of
  measure per `D1`/`D2`. Does not yet name an instrument.
- **U2** — the auditor. Python via stdlib `ast`; JS/TS via the scanner of `D4` with
  its limit in the module docstring. Declares `invoked_by: Makefile `quality-audit`
  target` (`RA-16` check (d) in `scripts/verify_references.py`). `sys.exit(2)` on any
  violation, `0` when clean; `--report` prints the register and exits `0`. Emits a
  compliance figure as `compliant_units / total_units`, with `unparsed` counted
  separately and never as compliant.
- **U3** — `quality-audit` target added to `.PHONY` and to the file, running with the
  `.agents` root as CWD like every other framework self-check. `verify` inclusion per
  `D5` branch.
- **U4** — the two skill notes currently end *"routed to Sprint 050"*, which this
  sprint makes false. Each note names `scripts/quality_audit.py` as the deterministic
  instrument and states that the skill remains a model-invoked helper.
- **U5** — `§1` rows `linter_command` (Python), `linter_command` (JS/TS),
  `max_indentation` and `max_lines_per_func` name `scripts/quality_audit.py` /
  `make quality-audit`, and carry the JS/TS limit of `D4`.
- **U6** — `session_state.py set-topology`, format and derivation per `D7`. New
  paired test file: no test currently covers `session_state.py` directly
  (`grep -rln 'session_state' tests/` → 3 files, none of them its own).
- **U7** — `close_workflow.md` Phase 4 `state_sync` replaces *"update sprint status
  and `topology_version`"* with the command and the documented format.
- **U8** — `deployment_workflow.md` Phase 4 invokes `set-topology` after
  `baseline_refresh`, as a separate invocation (`RA-13`). This is the write-back that
  never existed and is why the field trails a release.
- **U9** — the three `test_run_report_*` cases at
  `tests/test_audit_cursor_models.py:207,228,249` assert only
  `proposals["author_discrepancy"]`. Each gains one `capsys` assertion on the printed
  report, closing the gap Gate 2 of Sprint 049 had to cover by side-by-side execution.
- **U10** — regenerated by `python3 scripts/map_workflows.py`, never hand-edited
  (`agents.md §0`); `make verify` runs `map_workflows.py --check` and two workflow
  files change in this sprint. Generated output as its own unit follows the Sprint
  049 `U6` precedent.

---

## Dependencies

| Package | Version | Why the standard library and the existing dependencies do not suffice |
| :--- | :--- | :--- |
| None | — | — |

---

## Mechanisms

| Mechanism | Deterministic or agent judgment | Invoker (`RA-16`) |
| :--- | :--- | :--- |
| Python/JS-TS function length, nesting depth and compliance figure | script (`scripts/quality_audit.py`, `sys.exit(2)`) | `Makefile` `quality-audit` target; `Makefile` `verify` under `D5` branch A |
| `topology_version` write-back into the anchor | script (`scripts/session_state.py set-topology`) | `workflows/close_workflow.md` Phase 4 `state_sync`; `workflows/deployment_workflow.md` Phase 4, after `baseline_refresh` |

`RA-16 INVOCATION_COVERAGE`: no workflow, script, executable skill, hook or gate
merges without a declared, verifiable invoker, or a typed exception in
`config/invocation_exceptions.json` stating why it has none.

---

## Cost

| Field | Value | Reproduce |
| :--- | :--- | :--- |
| Delegation | `native` | `docs/active_state.json` `delegation_mode` |
| Work units | 10 | Count of rows in Work tables |
| Subagents dispatched | 10 planned (1 per unit) + 2 Phase 7 gates in fresh context | `agent_assignment.md` at Phase 4.1 |
| Prior session ratio | `2.9` (peak 107612 / first-turn 37002 tokens, session `5aead9ab`) | `python3 scripts/session_cost.py --from-anchor --json` |

---

## Tests

**Reproduce before repairing.**

| Check | Fails against the current tree? |
| :--- | :--- |
| `python3 scripts/quality_audit.py --report; echo $?` | **Yes** — the file does not exist; this is the defect |
| `make quality-audit` | **Yes** — no such target (`grep -n 'quality-audit' Makefile` → 0 hits) |
| `python3 scripts/session_state.py set-topology; echo $?` | **Yes** — no such subcommand; this is the defect |
| `grep -n 'capsys' tests/test_audit_cursor_models.py` shows a capture in each `test_run_report_*` | **Yes** — the three cases assert a return value only |
| `make verify; echo $?` → `0` | **No** — green today; this is the regression to protect |
| `venv_skillopt/bin/python3 -m pytest tests/ -q` → 780 passed | **No** — baseline to protect; new tests add to it |

---

## Verification

Read exit codes with `$?` directly; never through a pipe.

| Command | Expected |
| :--- | :--- |
| `venv_skillopt/bin/python3 -m pytest tests/ -q; echo $?` | `0`, count ≥ 780 + new cases |
| `make verify; echo $?` | `0` |
| `python3 scripts/quality_audit.py --report; echo $?` | `0`, register printed, `unparsed` listed separately |
| `python3 scripts/quality_audit.py scripts/; echo $?` | `0` under `D5` branch A, `2` under branch B with each violation named |
| `make quality-audit; echo $?` | matches the line above |
| `python3 scripts/verify_references.py; echo $?` | `0` — `quality_audit.py` resolves its `invoked_by:` |
| `python3 scripts/map_workflows.py --check; echo $?` | `0` after `U10` |
| `python3 scripts/session_state.py set-topology; echo $?` then `grep topology_version docs/active_state.json` | `0`, value `4.32.0-050-<status>` — the `4.31.0-049-closed` defect corrected by the instrument, not by hand |
| `python3 skills/token-saver-auditor/scripts/audit_plan.py docs/sprints/050-core-pipeline/IMPLEMENTATION_PLAN.md; echo $?` | `0` |
| `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/050-core-pipeline; echo $?` | `0` |

---

## Documentary impact (T5)

| Artefacto | Qué cambia |
| :--- | :--- |
| `agents.md` | `§1` gains the unit of measure for two magnitudes (`U1`) and names the real instrument in four rows (`U5`) |
| `config/invocation_exceptions.json` | Two notes stop saying "routed to Sprint 050" and name `scripts/quality_audit.py` (`U4`) |
| `Makefile` | New `quality-audit` target; `verify` extended under `D5` branch A (`U3`) |
| `workflows/close_workflow.md` | Phase 4 `state_sync` names a command instead of prose (`U7`) |
| `workflows/deployment_workflow.md` | Phase 4 gains the `topology_version` write-back (`U8`) |
| `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Regenerated after the two workflow edits (`U10`) |
| `docs/roadmaps/core/pipeline/021-030-program-queue.md` | At closeout: `KI-049-4` marked delivered; the `capsys` rider struck from the minor list; `D5` branch B residue recorded if it applies |
| `CHANGELOG.md` | Sprint 050 entry under `[Unreleased]` at closeout |
| `docs/sprints/050-core-pipeline/PHASE_REGISTER.md` | Written at closeout; records the `topology_version` correction as evidence |

**RA-14 propagation**: `grep -rn 'max_lines_per_func\|max_indentation\|python-quality-auditor\|js-standardizer' --include='*.md' --include='*.json' .`
returns 36 files. Closed sprint records (`docs/sprints/0??-core-pipeline/`) and the
`docs/audits/` reports are **history and are not rewritten**; the live surfaces are
the nine rows above. `skills/manifest_skills.json` is generated by
`skills/mass-standardizer/scripts/generate_manifest.py` under `make verify` and is
never hand-edited. Run this grep again at the remediation step, not only at the
reviewer's spot-check.

---

## Out of scope

| Exclusion | Why, and where it goes instead |
| :--- | :--- |
| `skills/python-quality-auditor/SKILL.md` and `skills/js-standardizer/SKILL.md` are unfilled scaffolding ("Define step-by-step logic here", "Document I/O contracts") citing legacy `Rule 1 & Rule 71` | Pre-existing documentation debt, not this sprint's subject, and 4 more files under `RA-14`. Route to a skill-documentation pass, recorded in `021-030-program-queue.md` at closeout |
| Wiring `ruff check .` / `pnpm run lint` into `make verify` | Both need a binary that `make verify` does not guarantee (`verify` is stdlib-only by design, `Makefile:20-24`). They stay QA-gate judgment, as `agents.md §1` now states. Destination: roadmap entry at closeout |
| Host-tunable thresholds in a `config/quality_thresholds.json` | Thresholds ship as module constants with CLI overrides; a config file is a second mechanism before the first has any user. Destination: roadmap entry at closeout |
| Remediating whatever violations the baseline shows | `D5` branch B routes them to Sprint 051. An instrument and a mass refactor in one sprint make a red gate unattributable |
| Splitting `docs/active_state.json` by lifetime (durable vs volatile) | Named as a separate concern by `.gitignore:49-50` and deliberately not invented here |

---

## Abort criterion

Two observations stop this sprint, decided before execution:

1. **The JS/TS path needs a runtime dependency.** If a correct-enough JS/TS
   function-boundary scan cannot be written in stdlib Python, stop — do not add a
   Node parser. `U2` ships Python-only, `U5` states the JS/TS rows remain
   instrument-less, and the JS/TS half is re-planned as its own sprint. `D4`'s whole
   point is that an over-credited parser is worse than a declared absence.
2. **`D5` branch C**: more than 20% of first-party Python functions violate `D1` or
   `D2` at baseline. Then the standard itself is in question, not the code, and a
   gate is not introduced over a tree that cannot pass it. `U3` withdraws the
   `verify` wiring, the target ships `--report`-only, and the threshold question goes
   to the human before any remediation is planned.

---

## Approval — `triple_lock` lock 1

| Field | Value |
| :--- | :--- |
| **Approved by** | GstMirabal (`gst.mirabal@gmail.com`) |
| **Date** | 2026-09-20 |
| **Plan commit at approval** | `532b508` |
| **Remaining locks** | Active Sprint · QA + Tester verdicts · Human OK at close |

The gate was held twice before this signature landed, and both holds are recorded
because an approval whose objections left no trace cannot be audited afterwards.
**Hold 1**: the Approval Gate was refused while `docs/sprints/050-core-pipeline/`
contained only `IMPLEMENTATION_PLAN.md` — Phases 2, 3, 4.1, 4.2 and 4.3 had not
produced their artifacts, and `task_scope.md` is the file by which
`jurisdictional_lock` and `no_interference` are applied. **Hold 2**: `audit_plan.py`
had last returned `0` against the plan as committed at `5f1b174`, but Phase 3
subsequently edited the `## Cost` table (`Prior session ratio` → `2.9`) in
`532b508`; the auditor was re-run against the current file and observed at exit `0`
before the authorization was requested, rather than inheriting the earlier result —
the same discipline Sprint 049 recorded (`audit_plan.py` exit `0` at draft, after
the mid-Phase-5 revision, and again at approval). A related record-integrity gap was
closed in the same round: `task_scope.md` now carries a provenance note (`943bcad`)
stating that its dispatched `rule_validator` was terminated by an account rate limit
after completing only the `no_interference` check, and that the session authored the
remainder under `agents/rule_validator.md`'s ruleset.

*Phase 5 is a single attended human authorization. It MUST NOT be wrapped inside an
unattended `/loop` (`workflows/pipeline_workflow.md`, `rules/loop_governance.md`).
Any `/loop` this sprint does run — Phases 6-8 only — is governed by
`scripts/loop_guard.py start`, which fails closed.*

> **Do not delete the sentence above.** `audit_plan.py` Filter 6 rejects any plan
> that names `/loop` without also naming `loop_guard.py`, and this footer names
> both. Until Sprint 041 it named only `/loop`, so **every plan written faithfully
> from this template was rejected by the mandatory Phase 1 gate** — the template
> failed the check that consumes it, and the only passing plans were the ones that
> had dropped this footer. Replace `{{…}}` placeholders; leave this pairing intact.
