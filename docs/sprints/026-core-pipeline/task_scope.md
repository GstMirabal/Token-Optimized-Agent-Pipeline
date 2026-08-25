# Task Scope — Sprint 026 (`tool-portability`)

**Branch**: `ai-sprint/026` · **Base**: `main` at `b5bfb6a`
**Plan**: `docs/sprints/026-core-pipeline/IMPLEMENTATION_PLAN.md`, committed `c07bc46`
**Phase**: 4.3 (Rule Audit) — produced after `agent_assignment.md` (4.1) and
`skill_assignment.md` (4.2). Every unit below is one commit whose structural
subject is one physical file (`agents.md §2 jurisdictional_lock`), reproduced
from `## Work`. **Status legend, current as of the 2026-08-24 suspension**:
`⏳` pending; `⏳→H2` deferred out of Hito 1's dispatch scope by human decision;
`✅ <sha>` executed and committed, with the commit that carries it. Phase 5's
approval was recorded on 2026-08-24 over the plan text at `1da9641`, so
`agents.md §2 triple_lock` no longer blocks execution. **Nine rows are `✅`** —
`A1`, `P8`, `P8.1`, `P2`, `P8.2`, `P2.1`, `P3.0`, `P3.2.1`, `P3.2.9`. `A1` carries
no SHA because `docs/active_state.json` is deliberately not versioned
(`.gitignore`, Sprint 024: the file mixes durable and volatile lifetimes, and
tracking it would ship the nucleus's live session into every host checkout). See
**Declared deferral** below.

**Patched after `c07bc46`.** `IMPLEMENTATION_PLAN.md §H1.c` gained three
units (`A4.1`, `A4.2`, `A4`) repairing the `RA-16` hooks-coverage gap this
artifact measured at the original Phase 4.3 pass — see `H1.c` and `RA-16`
below. This artifact is updated to match; no other section of the plan this
artifact already audited changed in a way that alters a prior row.

**Table shape.** One recurring table (`# | File | Operation | Risk | Assignee |
Status`), sectioned by Hito to mirror `## Work`'s own subsections (`H1.a`…`H1.f`,
Migration Gate, HITO 2) — the same sectioning convention `agent_assignment.md`
and `skill_assignment.md` already used for this sprint. No column is invented
beyond the five the format fixes.

---

## Declared deviations — settled by human decision, applied here, not reopened

**1. `tests/` writes reassigned to `devops_agent`.** `agents/tester_agent.md`
declares `tools: Read, Glob, Grep, Bash` — no `Write`/`Edit` — so it cannot
create or modify a test file (`F-021-A2`: no implementer role exists).
`devops_agent` already holds `Write`/`Edit` on `scripts/` and `hooks/`
(`F-086-A1`); `tests/` is treated as its sibling tree for this sprint only.
**`agents.md §6` is not amended.** Every affected row's `Assignee` column
below reads `devops_agent — deviation (tests/, tester_agent has no
Write/Edit)`, visible per row rather than only here. Affected: `P8.1`, `P9.2`,
`P4.1`, `A2`, and the four `tests/` rows inside `P3.2`'s census
(`P3.2.9`–`P3.2.12`).

**2. Gate verdicts: the gate issues, `orchestrator` transcribes.** `qa_agent`
and `agents/tester_agent.md` hold no `Write`/`Edit`, and
`config/artifact_registry.json` names `SPRINT_LOG.md`'s `role` as
**Orchestrator** — verified by reading that file. The gate remaining
read-only is correct design, not changed here. Affected: `G1.q`, `G1.t`,
`A3`. Their `Assignee` column reads `<gate role> (verdict) → orchestrator
(transcribes to SPRINT_LOG.md)`.

**`Design §D9` — resolved at this patch, no longer an open discrepancy.**
At the original Phase 4.3 pass, `Design §D9`'s role table assigned "Puertas
post-ejecución" to `qa_agent` + `tester_agent` with no separate mention of
who performs the write into `SPRINT_LOG.md`, read plainly as implying the
gate profiles write their own verdicts — inexecutable, since neither
profile's `tools:` grant includes `Write`/`Edit`. **`IMPLEMENTATION_PLAN.md`
now carries the correction directly**: `Design §D9`'s role table reads
"`qa_agent` + `tester_agent` **emiten el veredicto**; `orchestrator` lo
**transcribe** a `SPRINT_LOG.md`," followed by an explicit paragraph —
"**Corrección sobre autoridad de puerta, medida**" — naming the same
`config/artifact_registry.json` evidence this artifact already cited, and
stating the same rule this artifact already recorded: "la puerta emite el
veredicto; `orchestrator` lo transcribe." `G1.q`, `G1.t` and `A3` in `##
Work` all carry the corrected `Assignee` form. This artifact's own rows
below (`G1.q`, `G1.t`, `A3`) already matched that form before this patch and
require no change; only this note is updated, from flagging the discrepancy
to naming the correction.

**3. A new upstream finding — dispatched separately, referenced here only by
subject for record coherence.** `agents/tester_agent.md`'s `description` line
states it is used "to write and execute unit/integration tests," while its
own `tools:` frontmatter grants no `Write`/`Edit` — a profile asserting a
capability its own grant refuses. Distinct from `F-021-A2` ("no implementer
role exists" — a map-coverage gap): this is a **self-contradicting profile**.
Not recorded in this file; routed through `agents.md §4 feedback_upstream`
outside Phase 4.3.

---

## Declared escalations — `token_economy_agent` audit, transcribed per its `tier_escalation` charter row

**Assignee and jurisdiction are unchanged for every row below.** `devops_agent`
remains the owner of each file under `agents.md §6` / `F-086-A1`; each entry
here is a **model escalation for one task**, not a reassignment.
`token_economy_agent` (owner of the tier map, `agents/token_economy_agent.md`
`tier_ownership`) holds no `Write`/`Edit` and cannot write this artifact
itself — the same pattern already used above for gate verdicts (`Declared
deviations`, item 2): the issuing agent decides, `rule_validator`
transcribes. This is a one-time static audit of Sprint 026's own
unit-to-tier map, the alternative `no_selector_agent` names in place of a
per-task model selector, which that rule prohibits.

**1. Five per-unit model escalations.**

| Unit | File | From | To | Why |
| :--- | :--- | :--- | :--- | :--- |
| `P8` | `scripts/session_state.py` | mechanical/haiku | **author/sonnet, effort medium** | Inventing a UID scheme and claim-collision semantics is protocol design, not transcription; the Migration Gate's correctness rests on it |
| `P4` | `scripts/cursor_adapter.py` | mechanical/haiku | **author/sonnet** | First-of-its-kind generator across three output formats; the done-criterion counts files and key sets and would not catch a subtly malformed individual `.mdc` |
| `P9` | `hooks/on_push.py` | mechanical/haiku | **author/sonnet** | Novel force-push and history-rewrite detection; a false negative is a security regression the four named `P9.2` tests may not cover |
| `P4.2` | `scripts/audit_cursor_models.py` | mechanical/haiku | **author/sonnet** | Interprets an undocumented third-party SQLite schema and feeds `config/model_tiers.json`'s `cursor` column |
| `P4.0` | `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` | mechanical/haiku | **author/sonnet** | `IMPLEMENTATION_PLAN.md`'s own `## Mechanisms` table already classifies this unit as "juicio de agente, deliberado y de una sola vez… no existe alternativa determinista" — it was declared judgment and assigned the cheapest tier |

Affected rows' `Assignee` cells below read `devops_agent — escalated
(mechanical/haiku → author/sonnet[, effort medium]; see Declared
escalations)`, the same inline-annotation convention `Declared deviations`
already established, applied here rather than invented fresh.

**2. Not escalated — 22 of 67 rows are high-risk `devops_agent` work; only
the five above escalate.** Measured against the full table, not asserted:
`devops_agent` carries **high** risk on `P8`, `P3.0`, `P3.2.1`–`P3.2.7`,
`P3.2.9`–`P3.2.15` (14 rows), `P9`, `A4`, `P4.0`, `P4`, `A2`, `P4.2` — 22 in
total. Named individually so the 17 that stay `mechanical` are not later
mistaken for an oversight:

- **`A4` (`scripts/verify_references.py`) stays `mechanical`** despite
  **high** risk. The risk is blast radius — it widens a check that gates
  `make verify` for the whole repository — not implementation difficulty:
  widening one glob loop (`Path("hooks").glob("*.py")`) in an existing,
  well-understood check is deterministically observable by running `make
  verify` before and after and diffing the exit code.
- **The 14 `P3.2` census substitutions stay `mechanical`.** Each is a
  literal call-site replacement (e.g. `scripts/install_claude.py` →
  `scripts/install.py`) with an exact-match grep done-criterion per row —
  transcription, not judgment.
- **`P3.0` (`scripts/install.py`, `git mv`) stays `mechanical` — Match**,
  `token_economy_agent`'s own verdict: *"Rename, verified by one command
  (`--help` lists `--target`)."*
- **`A2` (`tests/fixtures/` sandbox, deviation-tagged) stays `mechanical` —
  Match**, `token_economy_agent`'s own verdict: *"Fully prescribed steps
  (exact Dockerfile form, prohibited forms named), verified by `$?`."*

**All 17 non-escalated high-risk rows now carry a stated, audited
rationale.** None rests on extrapolation: every one of the 22 high-risk
`devops_agent` rows — the 17 above and the 5 escalated in item 1 — was
adjudicated by `token_economy_agent`, not merely left unescalated by
omission.

**3. Framework gap — referenced here only for record coherence, dispatched
separately.** `tier_escalation` (`agents/token_economy_agent.md`) shipped in
Sprint 022 (`v4.7.0`) and produced no declaration in `023`, `024`, or `025`
— confirmed by reading all three prior `task_scope.md` files — nor in `026`
until this patch. **This is the first declaration the mechanism has ever
produced.** The gap itself (three sprints where an escalation-capable
mechanism escalated nothing) is a framework-class finding, routed through
`agents.md §4 feedback_upstream` outside Phase 4.3. **Not recorded in this
file** — dispatched to another instance, matching the treatment `Declared
deviations` item 3 already gave the `tester_agent` self-contradiction.

---

## Declared deferral — Hito 1 scope reduction, human decision (2026-08-24)

**Decision.** To reach the Migration Gate sooner, the human deferred a subset
of `## Work` from Hito 1 to Hito 2 (executed under Cursor). This is a
deviation from `IMPLEMENTATION_PLAN.md` as approved. Recorded here per this
sprint's own `Declared deviations`/`Declared escalations` convention — not
reopened, not argued. The deferred units are prose and documentation
propagation; none is inspected by the Migration Gate's observations `M1`–`M7`
(audited below). `IMPLEMENTATION_PLAN.md` itself is not edited by this patch.

**Deferred units, by ID.**

1. **`P3.2` prose subset — 27 of the 29 census rows** (`H1.b`): `P3.2.2`–
   `P3.2.8`, `P3.2.10`–`P3.2.29`. Docstrings, comments, `README.md`
   (`P3.2.19`), `SECURITY.md` (`P3.2.20`), `docs/` (`P3.2.22`–`P3.2.26`),
   `skills/slash-commander/` (`P3.2.27`, `P3.2.28`),
   `profiles/example-project/README.md` (`P3.2.29`), and governance/workflow
   prose (`agents.md` `P3.2.16`, `workflows/start_workflow.md` `P3.2.17`,
   `workflows/audit_workflow.md` `P3.2.18`). **Kept in Hito 1**: `P3.2.1`
   (`hooks/on_init.py:16`) and `P3.2.9` (`tests/test_installer.sh:31,67,83,
   93,112`) — the two files measured to break at runtime (below).
2. **`P3.3`** (`H1.b`, `docs/roadmaps/core/pipeline/021-030-program-queue.md:1284`).
3. **`P9.2`** (`H1.c`, `tests/test_on_push.py`).
4. **`P4.1`** (`H1.d`, `tests/test_installer.sh` — the `--target cursor`/
   `--target both` block; a distinct unit from `P3.2.9` on the same file,
   sequenced after it per **Isolation** below).
5. **`A4`, `A4.1`, `A4.2`** (`H1.c`, the `RA-16` hooks-blindness repair:
   `scripts/verify_references.py`, `hooks/on_commit.py`, `hooks/on_init.py`).

**33 rows total** carry the deferral marker in `## Work` below: 27 + 1 + 1 +
1 + 3.

**The measurement that justifies keeping exactly two `P3.2` files in Hito 1
— load-bearing.** Measured against the tree at `977c9f2`: of the 32 Class A
census files `Design §D2` names, exactly two break at runtime once `P3.0`
performs `git mv scripts/install_claude.py scripts/install.py`:

- `hooks/on_init.py:16` — `INSTALL_SCRIPT =
  Path(".agents/scripts/install_claude.py")` is a live constant, not a
  mention.
- `tests/test_installer.sh:83, 93, 112` — three direct
  `python3 .../install_claude.py` invocations. `tests/test_installer.sh`
  runs inside `make verify`, so leaving these stale turns the build red.

Verified safe to defer: `tests/test_installer.sh:31, 67` invoke
`install_claude.sh`, preserved by `P3.1b` as a deprecation shim;
`claude/settings.hooks.json:16` also names the `.sh` form;
`config/invocation_exceptions.json:55` carries the string inside a `note`
field, not a `path`.

**The plan's own objection — recorded, not softened.**
`IMPLEMENTATION_PLAN.md Design §D2` explicitly considered and rejected this
split: *"Se consideró y se rechaza partirlo: dejar la mitad documental para
el Hito 2 significaría propagar un renombrado a caballo de una frontera de
herramienta y de contexto, con la segunda mitad ejecutada por un agente que
no vivió la primera. Esa es literalmente la forma que RA-14 describe."* The
human overrode this knowingly, on 2026-08-24. **Mitigation, stated plainly
and not oversold**: `Design §D2`'s objection is against an *implicit*
handover; the deferred set is enumerated by filename in this artifact (item
1 above) before any of it is deferred, so the Hito 2 agent under Cursor
inherits a list, not a memory. This reduces the `RA-14` risk. **It does not
eliminate it.**

**Consequence for `P3.2`'s done-criterion — moved, not silently dropped.**
`P3.2`'s done-criterion (`grep -rn "install_claude"` filtered of
`Design §D2`'s Class B history, returning exactly one line — the shim) is
**not satisfiable at the Migration Gate** under this decision: 27 of 29
census rows remain unexecuted at that point. It becomes a **Hito 2 closing
condition** instead, to be checked at `A3` (the Hito 2 gate) rather than at
`H1.f`.

**`P1`/`P1.1` — considered for deferral, deliberately kept in Hito 1.**
`Design §D4b`: without `P1`, the Hito 2 units would run under Cursor in live
contradiction with `agents.md §6`'s eight-role mandate — Cursor cannot
instantiate 8 roles, so leaving `P1` unlanded would let Hito 2 run without
constitutional permission for its own execution mode. Keeping `P1` (and its
dependent regeneration, `P1.1`) in Hito 1 is what gives that constitutional
edit a native eight-role gate (`H1.f`) rather than a Cursor-context one.

**Audit — Migration Gate coverage, checked against `M1`–`M7`
(`IMPLEMENTATION_PLAN.md` lines 381–387).** `M1`/`M7` read
`docs/active_state.json` and `resume_pointer`; `M2` reads `session_id`/
`session_tool` (`P8`, kept in Hito 1); `M3` reads `delegation_mode` (`P2`,
kept); `M4` counts `.cursor/commands`/`.cursor/rules`/`mcp.json` (`P4`,
kept); `M5` questions the Cursor session on `agents.md §2
jurisdictional_lock`, loaded via `P5`/`P4` (both kept) — not via any
deferred `P3.2` prose row; `M6` runs `git push --force` against the hook
installed by `P9`/`P9.1` (both kept — `P9.2` is a test file for that hook,
not the hook itself, and is not read by `M6`). **Conclusion: no unit in the
deferred set is inspected by the Migration Gate.**

One adjacent effect, flagged for the record though outside this section's
mandate to fix: deferring `A4` means `H1.f`'s `make verify` no longer
proves `RA-16` compliance for `hooks/on_push.py` — this artifact's own
`RA-16 INVOCATION_COVERAGE` section above states that guarantee depends on
`A4` landing before `H1.f`. That guarantee now lands with Hito 2 instead.
**This does not affect `M1`–`M7`**, which check the hook's live behavior
directly (`M6`), not `make verify`'s exit code.

**Status marker.** Rows deferred by this decision carry `⏳→H2` in the
`Status` column below, in place of the plain `⏳` used elsewhere in this
document. Meaning: pending, not executed, **and** out of Hito 1's dispatch
scope by this human decision (2026-08-24) — to be dispatched in Hito 2,
under Cursor, `delegation_mode: sequential`. Rows without this suffix keep
the file's original `⏳` meaning: pending, awaiting Phase 5 approval, still
scoped to their originally-assigned Hito.

---

## HITO 1 — Bootstrap, under Claude Code, native 8-role pipeline

### H1.a — State and session

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | `docs/active_state.json` | modify | low | `devops_agent` |✅ `—` |
| P8 | `scripts/session_state.py` | modify | **high** | `devops_agent` — escalated (mechanical/haiku → author/sonnet, effort medium; see Declared escalations) |✅ `cce4f90` |
| P8.1 | `tests/test_session_protocol.py` | modify | medium | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) |✅ `c16cd4b` |
| P2 | `scripts/session_state.py` | modify | medium | `devops_agent` |✅ `832d2a1` |
| P8.2 | `workflows/start_workflow.md` | modify | medium | `orchestrator` |✅ `6b9c3e3` |
| P2.1 | `workflows/start_workflow.md` | modify | medium | `orchestrator` |✅ `977c9f2` |

`scripts/session_state.py` (`P8`, `P2`) and `workflows/start_workflow.md`
(`P8.2`, `P2.1`) are each the structural subject of two rows here — see
**Isolation** below for the full cross-Hito accounting; both pairs are
sequenced, not concurrent.

### H1.b — Installer and the reference census

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P3.0 | `scripts/install.py` (`git mv` from `scripts/install_claude.py`) | create | **high** | `devops_agent` |✅ `a107b36` |
| P3.1 | `scripts/install.sh` (`git mv` from `scripts/install_claude.sh`) | create | medium | `devops_agent` |✅ `26b6532` |
| P3.1b | `scripts/install_claude.sh` | create (deprecation shim) | low | `devops_agent` |✅ `3e6a243` |
| P3.3 | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | modify | low | `orchestrator` | ✅ `60d9364` |
| P10 | `scripts/install.py` | modify | medium | `devops_agent` |✅ `30cc63e` |
| P10.1 | `.gitignore` | modify | low | `devops_agent` |✅ `aa35b78` |

**`P3.2` — 29 files, expanded one row per physical file
(`jurisdictional_lock`).** The plan's own mitigation — `P3.0` lands and is
tested first, then each file is an independent single-file subtask,
dispatched by jurisdiction — is reflected here as 29 rows rather than left as
prose, mirroring `agent_assignment.md`'s own per-file resolution of the same
census. Batch risk (**high**, `RA-14` census) is carried per row rather than
re-graded, because the plan's own risk statement is at the batch level (a
single miss breaks the unit's exactly-one-line done-criterion) and this audit
does not substitute its own judgment for that.

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P3.2.1 | `hooks/on_init.py:16` | modify | **high** — RA-14 census (P3.2) | `devops_agent` |✅ `88a1e65` |
| P3.2.2 | `hooks/on_commit_msg.py:14` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `ab220ac` |
| P3.2.3 | `scripts/merge_json.py:4` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `5c554d3` |
| P3.2.4 | `scripts/_root.py:71` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `969fd6d` |
| P3.2.5 | `scripts/_mode.py:4,26` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `ff4740a` |
| P3.2.6 | `scripts/render_readme.py:3,66,113` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `53850e4` |
| P3.2.7 | `scripts/verify_references.py:160` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `436f1b1` |
| P3.2.8 | `skills/compliance-checker/scripts/distill.py:10` | modify | **high** — RA-14 census (P3.2) | `skill_architect` | ✅ `1cf8611` |
| P3.2.9 | `tests/test_installer.sh:31,67,83,93,112` | modify | **high** — RA-14 census (P3.2) | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) |✅ `bf53b46` |
| P3.2.10 | `tests/test_mass_standardizer.py:297` | modify | **high** — RA-14 census (P3.2) | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) | ✅ `76c01fa` |
| P3.2.11 | `tests/test_invocation_coverage.py:70` | modify | **high** — RA-14 census (P3.2) | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) | ✅ `87c1fca` |
| P3.2.12 | `tests/test_root_resolution.py:57` | modify | **high** — RA-14 census (P3.2) | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) | ✅ `a046187` |
| P3.2.13 | `claude/settings.hooks.json:16` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `7c14973` |
| P3.2.14 | `config/invocation_exceptions.json:55` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `96bcfeb` |
| P3.2.15 | `.gitignore:100` | modify | **high** — RA-14 census (P3.2) | `devops_agent` | ✅ `0bd8dee` |
| P3.2.16 | `agents.md:77,83,110,163` | modify | **high** — RA-14 census (P3.2) | `rule_validator` | ✅ `dcf1ed7` |
| P3.2.17 | `workflows/start_workflow.md:23,25` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `020e0d3` |
| P3.2.18 | `workflows/audit_workflow.md:18` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `efb2d40` |
| P3.2.19 | `README.md:60,101,107,123,164,198` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `9a3d57f` |
| P3.2.20 | `SECURITY.md:17` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `1339ed0` |
| P3.2.21 | `.github/ISSUE_TEMPLATE/bug_report.yml:26` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `29c12f6` |
| P3.2.22 | `docs/standards/templates/SYSTEM_OVERVIEW_TEMPLATE.md:41` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `969eee5` |
| P3.2.23 | `docs/guides/AGENTS_SLASH_COMMANDS_GUIDE.md:12,21,70,81,83` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `1ef8bc6` |
| P3.2.24 | `docs/architecture/global_topology.md:53` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `f9aa38a` |
| P3.2.25 | `docs/architecture/topology_map.md:17,21` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `8f30f5d` |
| P3.2.26 | `docs/plans/README.md:51` | modify | **high** — RA-14 census (P3.2) | `orchestrator` | ✅ `986c34b` |
| P3.2.27 | `skills/slash-commander/SKILL.md:12,30` | modify | **high** — RA-14 census (P3.2) | `skill_architect` | ✅ `4b82663` |
| P3.2.28 | `skills/slash-commander/README.md:49` | modify | **high** — RA-14 census (P3.2) | `skill_architect` | ✅ `9b81306` |
| P3.2.29 | `profiles/example-project/README.md:18` | modify | **high** — RA-14 census (P3.2) | `skill_architect` | ✅ `eba5a1c` |

Four of the 29 (`P3.2.7`, `P3.2.15`, `P3.2.16`, `P3.2.17`) are additional
multi-unit files not named in the task's own four examples — see
**Isolation** below.

### H1.c — Portable guards (precondition of the migration)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P9 | `hooks/on_push.py` | create | **high** | `devops_agent` — escalated (mechanical/haiku → author/sonnet; see Declared escalations) |✅ `e00f81e` |
| P9.1 | `scripts/install.py` | modify | medium | `devops_agent` |✅ `b3b0e9a` |
| P9.2 | `tests/test_on_push.py` | create | medium | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) | ✅ `e1591d1` |
| A4.1 | `hooks/on_commit.py` | modify | low | `devops_agent` | ✅ `5837e3e` |
| A4.2 | `hooks/on_init.py` | modify | low | `devops_agent` | ✅ `e3be78a` |
| A4 | `scripts/verify_references.py` | modify | **high** | `devops_agent` | ✅ `768cf56` |

`scripts/install.py` is now the structural subject of three rows across this
sprint (`P3.0`, `P10`, `P9.1`) — see **Isolation**.

**`A4.1`, `A4.2`, `A4` — new since this artifact's original Phase 4.3 draft,
promoted from a Phase 4.3 finding to sprint work.** These three repair the
`RA-16` gate blindness this audit measured (below, **`RA-16`
INVOCATION_COVERAGE**): check `(d)` in `scripts/verify_references.py` never
iterated `hooks/*.py`, so no hook's `invoked_by:` line was ever mechanically
verified. `IMPLEMENTATION_PLAN.md §H1.c` states the landing order as
mandatory — **`A4.1` and `A4.2` land before `A4`** — reproduced in that order
in the table above, not left to prose: `A4` widens check `(d)`'s scan loop to
`hooks/*.py`, and the moment it lands, every hook still lacking
`invoked_by:` fails `make verify`. `hooks/on_commit.py` and
`hooks/on_init.py` are the two hooks measured without a declaration at
`b5bfb6a` (`hooks/__init__.py` is the third and is not repaired by
declaration — see `RA-16` below for why). Two jurisdiction consequences,
detailed under **Isolation**: `hooks/on_init.py` is now a second-touch file
(`P3.2.1` already modifies it in `H1.b`), and `scripts/verify_references.py`
is now a third-touch file (`P3.2.7`, `P5.1`, `A4`).

### H1.d — Cursor adapter

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P6 | `workflows/standardization_workflow.md` | modify | low | `orchestrator` |✅ `7528467` |
| P11 | `.gitignore` | modify | low | `devops_agent` |✅ `ed22923` |
| P5 | `config/rule_triggers.json` | create | medium | `rule_validator` |✅ `b6b4c25` |
| P5.1 | `scripts/verify_references.py` | modify | medium | `devops_agent` |✅ `8d3cc3a` |
| P5.2 | `agents.md` | modify | medium | `rule_validator` |✅ `30798e3` |
| P4.0 | `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` | create | **high** | `devops_agent` — escalated (mechanical/haiku → author/sonnet; see Declared escalations) |✅ `9cacb4a` |
| P4.0b | `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` | modify | low | `devops_agent` |✅ `9cacb4a` |
| P4 | `scripts/cursor_adapter.py` | create | **high** | `devops_agent` — escalated (mechanical/haiku → author/sonnet; see Declared escalations) |✅ `7a18145` |
| P4.1 | `tests/test_installer.sh` | modify | medium | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) | ✅ `7ec83a6` |

`.gitignore` (`P10.1`, `P11`, and `P3.2.15`), `scripts/verify_references.py`
(`P5.1` and `P3.2.7`), `agents.md` (`P5.2`, and `P3.2.16`, and `P7` in HITO 2),
and `tests/test_installer.sh` (`P4.1` and `P3.2.9`) are each touched by more
than the two units the task's brief named — full accounting in **Isolation**.
`docs/sprints/026-core-pipeline/cursor_mdc_schema.md` (`P4.0` create, `P4.0b`
modify) is also multi-unit, trivially sequential (create then append,
adjacent rows).

### H1.e — Constitutional enablement of the Cursor half

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P1 | `workflows/pipeline_workflow.md` | modify | **high** | `orchestrator` |✅ `d55b828` |
| P1.1 | `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | regenerate | low | `devops_agent` |✅ `d55b828` |

### H1.f — Hito 1 gate (fresh context, native 8-role, under Claude Code)

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G1.q | `docs/sprints/026-core-pipeline/SPRINT_LOG.md` | append (QA verdict) | **high** — gate, `triple_lock` lock 3 | `qa_agent` (verdict) → `orchestrator` (transcribes) |✅ `7bf2cb4` (verdict 2026-08-25) |
| G1.t | `docs/sprints/026-core-pipeline/SPRINT_LOG.md` | append (Tester verdict) | **high** — gate, `triple_lock` lock 3 | `tester_agent` (verdict) → `orchestrator` (transcribes) |✅ `7bf2cb4` (verdict 2026-08-25) |

**Migration Gate — not a row.** The three-command sequence (`suspend` →
`install.py --target cursor` → `claim --tool cursor`) and the recording of
observations `M1`–`M7` into `SPRINT_LOG.md` carry no `#` and no `Assignee` in
`## Work` — by the plan's own definition a unit is "a commit whose structural
subject is one physical file," and the Migration Gate is a procedure, not a
unit. Flagged, not resolved, matching `agent_assignment.md`'s own treatment:
no profile is named to run the commands or record `M1`–`M7`.

---

## HITO 2 — the rest, under Cursor, `delegation_mode: sequential`

| # | File | Operation | Risk | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| P7 | `agents.md` | modify | medium | `rule_validator` |✅ `435db07` |
| P7.1 | `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | modify | low | `rule_validator` |✅ `0d3a134` |
| A2 | `tests/fixtures/` (sandbox under `/private/tmp`) | create + delete | **high** | `devops_agent` — deviation (tests/, tester_agent has no Write/Edit) |✅ measured 2026-08-25 |
| P4.2 | `scripts/audit_cursor_models.py` | create | **high** | `devops_agent` — escalated (mechanical/haiku → author/sonnet; see Declared escalations) |✅ `27ce35f` |
| P4.3 | `Makefile` | modify | low | `devops_agent` |✅ `62db6b0` |
| P4.4 | `config/model_tiers.json` | modify | medium | `rule_validator` |✅ `8f8ff73` |
| A3 | `docs/sprints/026-core-pipeline/SPRINT_LOG.md` | modify (Hito 2 gate) | medium — gate, closes Hito 2 | `qa_agent` (verdict) → `orchestrator` (transcribes) | ✅ `3a92130` — blind judge ID'd `cursor_mdc_schema.md`; portability **not** affirmed |
| A3.1 | `scripts/cursor_adapter.py` (+ delete sprint `cursor_mdc_schema.md`; `tests/test_cursor_adapter.py`) | modify + delete + create | medium — remediates A3 delator | `devops_agent` | ✅ `3464d8a` / `25baebc` |
| A3.r | `docs/sprints/026-core-pipeline/SPRINT_LOG.md` | modify (A3 re-run) | medium — gate | `qa_agent` (verdict) → `orchestrator` (transcribes) | ⏳ |

`agents.md` here (`P7`) is the file's **third** touch this sprint, after
`P3.2.16` and `P5.2` — see **Isolation**.

---

## Isolation

### `jurisdictional_lock` — `P3.2`'s 29-file dispatch

`P3.2`'s 29 files exceed the one-file-per-subtask cap by construction, and
the plan's own mitigation is the precedent `C0.3` set in Sprint 023: `P3.0`
lands and is tested first, then every file becomes an independent single-file
subtask dispatched by jurisdiction (grouped by owning profile in the census
table). Rows `P3.2.1`–`P3.2.29` above are that mitigation applied, not left
as prose — each row's structural subject is one physical file, satisfying
`jurisdictional_lock` per row. `P3.0` (`H1.b`) must be delivered and verified
(`python3 scripts/install.py --help` lists `--target`) before any `P3.2.*`
row is dispatched, since several rows edit call sites of the renamed script.

### `no_interference` — every file touched by more than one unit

Confirmed sequenced (RA-08 atomic, separate commits), never concurrent. The
task's brief named four; the full count, measured against `## Work` in full
including the `H1.c` patch, is **nine**:

| File | Units, in execution order | Sequenced because |
| :--- | :--- | :--- |
| `scripts/session_state.py` | `P8` → `P2` | Same Hito (`H1.a`); plan text: "`P2` … Commit separado de `P8` sobre el mismo fichero físico (`RA-08`)" |
| `workflows/start_workflow.md` | `P8.2` → `P2.1` → `P3.2.17` | `P8.2`/`P2.1` are `H1.a` (executes first); `P3.2.17`'s census fix (lines 23,25) is `H1.b` (later). **Not named by the task's brief** — found by full enumeration of the census |
| `scripts/install.py` | `P3.0` → `P10` → `P9.1` | `H1.b` table order (`P3.0`, then `P10`) then `H1.c` (`P9.1`); plan text: "`P9.1` … Tercer commit sobre `scripts/install.py`, separado de `P3.0` y `P10`" |
| `.gitignore` | `P3.2.15` → `P10.1` → `P11` | `P3.2.15` and `P10.1` both `H1.b` (census before the table row, per table order); `P11` is `H1.d` (later). **Not named by the task's brief** |
| `hooks/on_init.py` | `P3.2.1` → `A4.2` | Census (`H1.b`, constant at line 16) precedes the `invoked_by:` repair (`H1.c`). **New at this patch** — `A4.2` did not exist at the original Phase 4.3 pass |
| `scripts/verify_references.py` | `P3.2.7` → `A4` → `P5.1` | **Measured, and this order corrects the one given in this patch's own instructions.** By Hito table position — the same method this audit already used for every other row in this table — `H1.b` (`P3.2.7`) precedes `H1.c` (`A4`) precedes `H1.d` (`P5.1`). The instruction that produced this patch stated the sequence as `P3.2.7 → P5.1 → A4`; that does not match `IMPLEMENTATION_PLAN.md`'s own Hito ordering, in which `A4` (`H1.c`) lands **before** `P5.1` (`H1.d`), not after. Recorded here as measured rather than silently conformed to the instruction — flagged in this report's summary for the delegating agent |
| `agents.md` | `P3.2.16` → `P5.2` → `P7` | Census (`H1.b`) → Rule Contexts sentence (`H1.d`) → symlink-exclusion row (HITO 2, after the Migration Gate). **Not named by the task's brief** — and the widest span, crossing the Hito boundary itself |
| `tests/test_installer.sh` | `P3.2.9` → `P4.1` | Census (`H1.b`) precedes the `--target cursor` test block (`H1.d`). **Not named by the task's brief** |
| `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` | `P4.0` → `P4.0b` | Adjacent rows, `H1.d`, create then modify by design (`Design §D6`) |

**`hooks/on_commit.py` checked and cleared.** Only `A4.1` names it as
structural subject anywhere in `## Work`; it is not in the `P3.2` census
(only `hooks/on_init.py:16` and `hooks/on_commit_msg.py:14` are) and appears
nowhere else. Single-unit, no `no_interference` entry required.

**Audit conclusion.** Every pair/triple above is sequenced by the plan's own
Hito/table ordering, not concurrent, so none is a `no_interference` abort
condition as things stand. **But the ordering that makes this true is only
implied by table layout** — `## Work` does not state anywhere that `H1.a`
must fully land before `H1.b` begins, or `H1.b` before `H1.d`, or `H1.b`
before `H1.c`. For a plan this dense in structural-subject repeats (9 files,
one spanning both Hitos),
that implicit assumption is worth making explicit rather than inferred: a
native 8-role dispatch that ran `P5.1` before `P3.2.7` landed, for example,
would still satisfy `jurisdictional_lock` (one file per subtask) while
violating the sequencing this audit just confirmed by reading table position
alone. Recommendation for Phase 6 (not actioned here): each Hito's opening
line should state "no unit of this Hito is dispatched before every unit of
the prior Hito is committed," turning an inferred order into a stated one.

---

## `RA-16 INVOCATION_COVERAGE` — the three new mechanisms

| Mechanism | Declared invoker (plan) | Resolvable by `verify_references.py` check `(d)`? |
| :--- | :--- | :--- |
| `scripts/cursor_adapter.py` (`P4`) | `scripts/install.py` imports it as a module | **Yes.** Check `(d)`'s `imported_modules()` walks `Import`/`ImportFrom` nodes across `scripts/*.py` **and** `hooks/*.py`, and a `scripts/*.py` file whose stem appears in that set is exempted from needing its own `invoked_by:` text. Confirmed precedent at `scripts/verify_references.py:160` (`scripts/merge_json.py`) |
| `scripts/audit_cursor_models.py` (`P4.2`) | `Makefile 'cursor-tiers' target`, added by `P4.3` | **Yes, mechanically — with a caveat.** `audit_cursor_models.py` is not imported anywhere, so check `(d)` falls to its text-presence branch: it passes once the docstring contains the literal substring `invoked_by:`. The check does **not** grep `Makefile` to confirm a `cursor-tiers` target actually exists there — it is a presence check, not a resolution check. Since `P4.3` genuinely adds that target in this same plan, the declared invoker is true in fact even though the check would pass regardless. This is an existing property of check `(d)` (the same is true of its own `invoked_by:` line), not a defect introduced by this sprint |
| `hooks/on_push.py` (`P9`) | `.git/hooks/pre-push, installed by scripts/install.py` (docstring form identical to `hooks/on_commit_msg.py:14`) | **Closed by dependency, not by an open gap — repaired at this patch.** `A4` (new, `H1.c`) widens check `(d)`'s scan loop to `Path("hooks").glob("*.py")`, so `hooks/on_push.py`'s `invoked_by:` line becomes mechanically resolvable **once `A4` lands**. **The dependency, stated explicitly**: `P9`'s `RA-16` claim is unverifiable by `make verify` until `A4` lands; `A4` is the last unit of `H1.c`, entirely inside Hito 1 and ahead of `H1.f` (the Hito 1 gate, whose done-criterion requires `make verify` to exit `0`) — so by the time `H1.f` runs, `A4` has landed and the claim is verified. `P9`'s own row precedes `A4`'s row in `H1.c`'s table, but that relative order is immaterial to this specific dependency: what is required is `A4` before `H1.f`, not `A4` before `P9`, and the plan satisfies that. **Residual note, carried from this audit's own Isolation caveat**: this reasoning still rests on the unstated assumption that no unit of one Hito dispatches before every unit of the prior Hito is committed — true of `H1.c` relative to `H1.f` by table position, not by an explicit rule in `## Work` |

**Consequence for the Verification table — updated to match the plan's own
correction.** `IMPLEMENTATION_PLAN.md`'s `## Verification` table now states
this precisely, in the plan's own words: `python3 scripts/verify_references.py`
sale `0`; "`hooks/on_push.py` declara `invoked_by:` en su docstring (`P9`),
pero la comprobación `(d)` solo lo verifica **si `A4` ha aterrizado** —
antes de `A4` el bucle de `(d)` no recorre `hooks/`, y esta salida en `0` no
es evidencia de cumplimiento de `RA-16` para ningún fichero de `hooks/`."
This is the same finding this audit raised at the original Phase 4.3 pass,
now stated by the plan itself and closed as a **repair unit** (`A4`) rather
than left as a caveat with no remedy. **`hooks/__init__.py` stays excluded
by construction, decided in `A4`'s own operation text and recorded here so
a later reader does not re-open it**: the check filters it out by
`path.name != "__init__.py"` inside the check's own logic, **not** by a
`config/invocation_exceptions.json` entry — because none of the four
`VALID_EXCEPTION_REASONS` (`model-invoked`, `vendored-reference`,
`human-entry-point`, `one-time`) describes a Python package marker file.
`P9`'s docstring should still be written to the same convention as its
siblings — it is, and always was, the correct form — and after this patch
it is also the first hook whose declaration is mechanically checked, once
`A4` lands.

---

## Done-criteria — unexecutable as measured at the original Phase 4.3 pass, re-audited against the patched plan

Five of the six flagged rows were rewritten (`P2.1`, `P5.2`, `P7`, `P4.4`,
`M5`); `A3`'s was changed from a statistical formulation to a binary one.
Each is re-measured below against `IMPLEMENTATION_PLAN.md` as it stands now.
**Not softened**: where a rewrite still leaves a gap, it is named, not
absorbed into "fixed."

| Unit | Original finding (Phase 4.3) | Rewrite, measured | Verdict |
| :--- | :--- | :--- | :--- |
| `P2.1` | "…conserva el precedente de las líneas 974–978" had no grep pattern or quoted phrase — an adjective-shaped criterion with no check that proves it | Now: "la celda nombra `delegation_mode` y `docs/active_state.json` por ruta, y contiene la frase literal 'reports the mismatch to the human'… `grep -c` … devuelve al menos `1`". Confirmed by direct search: that literal phrase does not exist anywhere in `workflows/start_workflow.md` today, so the check is meaningful, not vacuously true | **Executable.** Residual, named rather than softened: the `grep -c` is a whole-file count, not scoped to the `delegation_conflict` cell specifically — a technically stray placement of the phrase elsewhere in the file would also satisfy it. Minor, not disqualifying |
| `P5.2` | Only command-checked half (`verify_references.py` exits `0`) did not test what `P5.2` actually adds | Now: `grep -c "config/rule_triggers.json" agents.md` must return ≥`1` inside the Rule Contexts table, "probando que la frase fue escrita y no solo que el fichero sigue siendo válido," plus the `verify_references.py` check retained. Confirmed: that string is absent from `agents.md` today | **Executable.** Same residual as `P2.1`: whole-file grep, not row-scoped |
| `P7` | Same pattern as `P5.2` — the row's real content requirement was prose-graded | Now: two greps, `"AGENTS.md"` and `"excludes the symlink path"`, both required present, plus `verify_references.py`. Confirmed: neither string exists in `agents.md` today | **Executable.** Same residual: the two greps are not required to land on the same table row, only somewhere in the file |
| `P4.4` | `check_model_tiers.py` validates schema, not the semantic content of `_comment`; the half that mattered for `Design §D7` had no command | Now: `python3 -c` asserts the literal substring `'not proven history'` is present inside `_comment`, in addition to the schema check | **Fully executable, no residual.** This is the one rewrite with no scoping gap — the check reads the exact field the operation writes |
| `A3` | "por encima del azar" named no sample size, no test, no chance rate, and directly conflicted with `Abort criterion §3`'s binary framing | Now: binary — "identifica correctamente… o no lo identifica correctamente — binario, sin margen de azar," explicitly aligned with `Abort criterion §3`'s "si acierta" | **Fully executable, no residual.** The self-contradiction this audit flagged is resolved by adopting one formulation across both places, not by picking a side and leaving the other unedited (`RA-14` would have flagged that) |
| `M5` | "la cita correctamente" had no reference text, no partial-match tolerance, no verbatim-vs-paraphrase distinction | Now: a literal question is specified, only "one" or "1" count as correct — "ningún otro número ni una paráfrasis que evada la cifra cuenta como correcta" — graded "carácter a carácter contra el valor de la regla" | **Fully executable, no residual.** This is the strongest of the five rewrites: it eliminates judgment from the grading step entirely, which is exactly what the original finding demanded |

---

## Rules consulted

`rules/code_craft.md` (Python/Markdown touched throughout both Hitos),
`rules/qa_and_testing.md` (Double-Gate Review Protocol — informs the gate
transcription correction above; §5 waiver marker, relevant to `A2`'s
Dockerfile exercise), `rules/documentation_standard.md` (governance and
`docs/` edits — `P1`, `P5.2`, `P6`, `P7`, `P8.2`, `P2.1`, `P3.3`),
`rules/skills_and_integrations.md §3` (confirms `skills/slash-commander/`
is first-party and editable — `P3.2.27`, `P3.2.28` — while
`skills/*-3rd/` stays untouched, matching `## Out of scope`'s own exclusion).

## Status

As of 2026-08-25 (post–Hito 2 deferred batch): Hito 1 + deferred census
(`P3.2.*`, `P3.3`), `A4*`, `P9.2`, `P4.1`, and named Hito 2 units through
`P4.4`, **`A3`**, and **`A3.1`** are `✅`. Remaining: **`A3.r`** (blind partition re-run after schema absorption).

Phase 5 approval: `1da9641`. Migration Gate: PASS. P3.2 done-criterion:
exactly one `install_claude` line outside excluded paths — the shim.
