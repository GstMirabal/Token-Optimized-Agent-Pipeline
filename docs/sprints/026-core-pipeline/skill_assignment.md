# Skill Assignment — Sprint 026 (`tool-portability`)

Phase 4.2 of `workflows/pipeline_workflow.md`. Implementation Plan committed at
`c07bc46` (`docs/sprints/026-core-pipeline/IMPLEMENTATION_PLAN.md`).

A tool that was considered and rejected is a decision, a tool that was never
seen is a gap. Both halves are recorded below.

---

## 1. Priority-1 search performed first

`rules/skills_and_integrations.md §1` orders discovery: Priority 1 is
`skills/manifest_skills.json` (34 entries, read in full). Priority 2 is
`skills/autoskills-3rd/` — **not escalated to**: its `node_modules/` is
unprovisioned, and every unit below resolved against the manifest without a
gap that would justify provisioning it. See §4 for the explicit rejection.

`git status --porcelain` was not touched by this search — read-only.

---

## 2. Per-unit tool resolution

Every unit in `## Work` is one of three classes: (a) covered by an existing
skill already wired into `make verify` or a QA/Tester gate, (b) a
framework-root `scripts/`/`hooks/` artifact under `devops_agent`/`rule_validator`
jurisdiction (`agents.md §6`, `F-086-A1`) for which no skill applies by
design, or (c) a plain documentation/config edit needing no computational
tool at all. None resolve to class (d) "skill does not exist and a unit
cannot proceed without one."

### HITO 1

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| `A1` | `docs/active_state.json` | Class (c). Verified by existing `scripts/session_probe.py`. No skill. |
| `P8`, `P8.1`, `P2` | `scripts/session_state.py` (211 lines), `tests/test_session_protocol.py` | Class (b). `omni-context-minimizer` (Used, §3) for structural discovery before the partial edit — `agents.md §2 ast_skeleton` applies at 211 lines. No skill performs the UID-generation/collision-guard logic itself; it is `devops_agent`'s code. |
| `P8.2`, `P2.1` | `workflows/start_workflow.md` | Class (c) for the edit; `slash-commander` (Used, §3) audits the resulting commands↔workflows link at gate time. |
| `P3.0`, `P3.1`, `P3.1b`, `P9.1`, `P10`, `P10.1` | `scripts/install_claude.py`→`scripts/install.py` (349 lines), `scripts/install.sh`, `.gitignore` | Class (b). `omni-context-minimizer` for the 349-line file (three separate commits touch it: `P3.0`, `P10`, `P9.1`). No skill generates an installer; it is `devops_agent`'s code by `F-086-A1`. |
| `P3.2` (32 files: 29 tabulated + 2 renamed + 1 handled by `P3.3`) | see plan `Design §D2` table | Class (c), grep-driven single-string replacement per file. `mass-standardizer` (Used, §3) re-checked at gate because two of the 29 are first-party skill files (`skills/slash-commander/SKILL.md`, `skills/slash-commander/README.md`) and one is `skills/compliance-checker/scripts/distill.py` — manifest parity must hold after those specific edits. |
| `P3.3` | `docs/roadmaps/core/pipeline/021-030-program-queue.md` | Class (c). |
| `P9`, `P9.2` | `hooks/on_push.py` (new), `tests/test_on_push.py` (new) | Class (b). See §5 — no existing script or skill rejects a force-push; `hooks/on_commit.py` is the sibling pattern followed, not a tool that already does this job. |
| `P6`, `P11` | `workflows/standardization_workflow.md`, `.gitignore` | Class (c). |
| `P5` | `config/rule_triggers.json` (new) | Class (c). Structured extraction from the `agents.md §0` *Rule Contexts* prose table; no skill parses governance prose into JSON, and the plan does not propose one — it is a one-time hand-authored config file, 11 entries. |
| `P5.1` | `scripts/verify_references.py` (236 lines) | Class (b). `omni-context-minimizer` for the 236-line file before adding check `(e)`. |
| `P5.2`, `P1`, `P1.1` | `agents.md`, `workflows/pipeline_workflow.md`, `docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md` | Class (c) for the governance edits; `scripts/map_workflows.py --check` (existing framework script, not a skill) is the regeneration gate for `P1.1`. |
| `P4.0`, `P4.0b` | `docs/sprints/026-core-pipeline/cursor_mdc_schema.md` (new) | See §6 — dedicated analysis, plan's classification affirmed. |
| `P4`, `P4.1` | `scripts/cursor_adapter.py` (new), `tests/test_installer.sh` | Class (b). See §5 — `slash-commander` and `skills/mcp-registry` both checked and rejected as substitutes (§4). No skill generates Cursor-format artifacts. |
| `G1.q`, `G1.t` (Hito 1 gate) | — | `python-quality-auditor` (Used, §3) is the QA instrument for every Python file this hito touches; `mass-standardizer` + `slash-commander` + `topology-monitor` run automatically inside `make verify`, which the gate's done-criterion requires at `0`. |

### PUERTA DE MIGRACIÓN

`M1`–`M7` are observation commands over artifacts `P8`, `P2`, `P4`, `P9`, `A1`
already produce — no additional tool. All seven read state with `python3 -c`
or `ls`/`git`, already named literally in the plan.

### HITO 2

| Unit(s) | File(s) | Resolution |
| :--- | :--- | :--- |
| `P7`, `P7.1` | `agents.md`, `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` | Class (c). |
| `A2` | sandbox under `/private/tmp` | See §7 — dedicated analysis. No new tool; exercises the existing `hooks/on_commit.py`. `env-shielding-auditor` and `mass-standardizer` both checked and rejected (§4). |
| `P4.2` | `scripts/audit_cursor_models.py` (new) | Class (b). See §5 — `scripts/detect_new_models.py` checked as the nearest precedent and rejected as a substitute (§4): different data source (Claude Code's bundled `shared/models.md`, not Cursor's `state.vscdb`). |
| `P4.3` | `Makefile` | Class (c). `RA-16` invoker satisfied by the docstring declaration; `scripts/verify_references.py` check `(d)` (existing) is the compliance instrument, not a skill. |
| `P4.4` | `config/model_tiers.json` | Class (c). Verified by the existing `scripts/check_model_tiers.py`, already in `make verify`. |
| `A3` (Hito 2 gate) | `docs/sprints/026-core-pipeline/SPRINT_LOG.md` | Existing `scripts/docs_freshness_check.py` covers the freshness half. The blind-partition exercise is deliberately un-tooled — see `## Mechanisms` in the plan: "a deterministic check here would be a `diff`, and `diff` is exactly what the reordering removes." No skill applies by the plan's own design. |

Every unit above resolves. None is blocked on a missing tool.

---

## 3. Used

| Skill / tool | Kind | Where |
| :--- | :--- | :--- |
| `slash-commander` | Skill | `make verify` (`verify_commands.py`) — audits `commands/*.md` ↔ `workflows/*.md` drift after `P8.2`, `P2.1`, `P6`, `P1` edit workflow files and `P4` generates `.cursor/commands/` from the same `commands/*.md` |
| `mass-standardizer` | Skill | `make verify` (`generate_manifest.py` + manifest diff) — baseline gate, and specifically re-checked because `P3.2` edits two `skills/slash-commander/` files and one `skills/compliance-checker/` file |
| `topology-monitor` | Skill | `make verify` (`legacy_app_auditor.py`) — baseline gate component |
| `python-quality-auditor` | Skill | QA gate instrument for `agents.md §1 python-doctor check --diff`, applied to every new/modified Python file: `scripts/session_state.py`, `scripts/install.py`, `scripts/cursor_adapter.py`, `hooks/on_push.py`, `scripts/audit_cursor_models.py`, `scripts/verify_references.py`, and the other Class-A Python files in `P3.2` |
| `omni-context-minimizer` | Skill | `agents.md §2 ast_skeleton` mandates it before any partial read on a file over 200 lines. Three files this sprint edits qualify: `scripts/session_state.py` (211), `scripts/install_claude.py`→`install.py` (349), `scripts/verify_references.py` (236) |

None of the five is forged or modified by this sprint — all pre-exist and are
invoked as designed.

---

## 4. Not used, deliberately

| Skill | Considered for | Why not |
| :--- | :--- | :--- |
| `env-shielding-auditor` | `A2` | Wrong mechanism. Its only declared invoker is `workflows/standardization_workflow.md` Phase 5.2 (`shield_gate`), a one-time onboarding scan before artifacts enter git — not a live commit guard. `A2` tests a real commit against the actual pre-commit hook, `hooks/on_commit.py`, whose own `audit_secret_shielding()` / `DOCKERFILE_SECRET` pattern is what `F-023-S4` measured and what the plan requires (`ENV` with quoted value). Invoking a skill that never runs at commit time would test the wrong guard. |
| `mcp-registry` | `P4` | Governs adding/approving a **new** external MCP server, human-gated (`registry.json` §Security). `P4` performs a format transform of already-approved entries from `claude/mcp.json` into `.cursor/mcp.json` — no new server is registered, so the human-approval gate this skill exists to enforce does not apply. |
| `autoskills-3rd` | Priority-2 escalation, generally | Not escalated to. Priority 1 (`manifest_skills.json`) already resolved every unit in §2 without a gap; provisioning `node_modules/` (`pnpm install --dir skills/autoskills-3rd`) for a scan that manifest coverage already answered would violate `agents.md §2 token_saver`. |
| `compliance-checker` | Governance edits (`P1`, `P5.2`, `P7`) | Its governance-violation scan is a Phase 1 (Planning) instrument, applied before the plan reaches its `c07bc46` commit. Phase 4.2 resolves tools against an already-approved plan; re-running a plan-review skill here would be re-litigating Phase 1, not assigning tools. |
| `token-saver-auditor` | The plan's own token cost | Same reasoning: a Phase 1 instrument for auditing the plan/implementation cost, already exercised (or not) before this plan was committed. Not re-invoked at Phase 4.2. |
| `topology-scaffolder` | `docs/sprints/026-core-pipeline/` | No topology to scaffold — the directory and `IMPLEMENTATION_PLAN.md` already exist, committed at `c07bc46`. |
| `graphify` | General discovery across ~30 single-file units | Every unit in this plan is scoped to one physical file (`jurisdictional_lock`), enumerated line-by-line in `## Work` and `Design §D2`. Targeted reads (used throughout this assignment, per `agents.md §2 token_saver`) cost less than building or querying a knowledge graph for 30 already-named files. Same reasoning as Sprint 025's `skill_assignment.md`. |
| `skillopt` | — | Governs SkillOpt prompt training; no unit touches skill prompts. |
| `contract-writer` | — | No API contracts: the sprint's `Context` records the human decision "no calls to the Anthropic API," and no other API surface is created. |
| `js-standardizer`, `django-expert-3rd`, `django-patterns-3rd`, `django-security-3rd`, `django-tdd-3rd`, `django-verification-3rd`, `nodejs-backend-patterns`, `nodejs-best-practices`, `typescript-advanced-types`, `vercel-composition-patterns`, `vercel-react-best-practices`, `tailwind-css-patterns`, `vite`, `accessibility`, `seo`, `frontend-design`, `readme-standardizer` | — | Domain mismatch. This sprint's touched files are exclusively Python, Bash, Markdown, and JSON (`## Dependencies`: stdlib only). Zero JS/TS/Django/Node/frontend files are created or modified. |

---

## 5. Confirmed: no existing tool does the job of the three new scripts

Per the explicit instruction to check before any unit proposes building:

| New artifact | Unit | Existing candidate checked | Verdict |
| :--- | :--- | :--- | :--- |
| `scripts/cursor_adapter.py` | `P4` | `slash-commander` (audits, does not generate); `mcp-registry` (governs new-server approval, not format transform) | Neither does the job. No script under `scripts/` generates `.cursor/` artifacts from `commands/`, `rules/`, or `claude/mcp.json` — confirmed by `find . -name ".cursor" -type d` returning nothing in the plan's baseline measurement. New script required, owned by `devops_agent` (`F-086-A1`), not a skill. |
| `hooks/on_push.py` | `P9` | `hooks/on_commit.py` (secret/commit-msg/submodule-purity guards, no push hook); the plan's own baseline measurement: `hooks/` contains no `on_push.py` | No existing hook rejects `git push --force`. `hooks/on_commit.py` is the structural pattern followed (docstring form, `sys.exit` semantics), not a tool that already performs this job. New hook required, `devops_agent`, not a skill. |
| `scripts/audit_cursor_models.py` | `P4.2` | `scripts/detect_new_models.py` (existing, in `make verify`) | Does not do the job. It reads Claude Code's bundled `shared/models.md` catalogue — a different tool's different data source. `P4.2` reads Cursor's `state.vscdb` via `sqlite3`, which no existing script touches. Not a substitute; a structurally analogous precedent (severity-ladder pattern, `config/model_tiers.json` as the durable sink) worth following for consistency, but not a tool that already exists for Cursor. New script required, `devops_agent`, not a skill. |

`config/rule_triggers.json` (`P5`) and `scripts/verify_references.py` check
`(e)` (`P5.1`): no existing config or check covers rule-trigger↔`rules/*.md`
parity; `Design §D8` explicitly rejects a standalone validator in favor of
extending the existing `verify_references.py`, which already has an invoker
(`Makefile 'verify' target`). Confirmed no gap requiring a new skill.

---

## 6. `P4.0` — dedicated analysis

**Agreement: the plan's classification is correct.** `## Mechanisms` in
`IMPLEMENTATION_PLAN.md` classifies `P4.0` as *"juicio de agente, deliberado y
de una sola vez"* because no deterministic alternative exists — the `.mdc`
frontmatter schema must be read from a file Cursor's own UI produces, and
Cursor's schema is not documented anywhere in this tree (`Design §D5`
confirms `.cursor/` does not exist pre-execution).

No skill or script is proposed as a substitute. The mechanism `P4.0` actually
uses is the `Read` tool over the file Cursor writes under `.cursor/rules/`
after `Cursor Settings → Rules → New Rule` is exercised in the UI — not a
script, because there is nothing to run: the schema is discovered by reading
one real file, once, and the discovery's own output (`cursor_mdc_schema.md`)
is what makes `scripts/cursor_adapter.py` (`P4`) deterministic afterward.
Proposing a tool here would mean writing a parser for a schema not yet known,
which is the exact inversion `Abort criterion §4` exists to block: a
generator key not read from a real file. The plan's prohibition is not
weakened by this assignment — no key is registered here that was not
observed in the `.mdc` file `P4.0` reads.

---

## 7. `A2` — dedicated analysis

`A2` requires a deliberate, real secret-form violation (`ENV` with a quoted
value in a `Dockerfile`, per `F-023-S4`'s measured detection boundary) to
prove the guard fires under Cursor. Two skills were evaluated as the
mechanism and both rejected:

- **`mass-standardizer`** — audits the Three-File Skill Standard over
  `skills/`. `A2`'s violation is a secret-scanning question, not a skill-
  structure question; irrelevant to this unit.
- **`env-shielding-auditor`** — scans for hardcoded secrets, but its only
  declared invoker (`workflows/standardization_workflow.md` Phase 5.2,
  `shield_gate`) is a one-time pre-migration onboarding scan, not a live
  git guard. Confirmed by `grep` across the tree: nothing wires it into
  `.git/hooks/` or `Makefile`.

The actual mechanism `A2` exercises is `hooks/on_commit.py`'s own
`audit_secret_shielding()` (with `DOCKERFILE_SECRET` among its patterns,
`hooks/on_commit.py:120`), installed as `.git/hooks/pre-commit` by
`scripts/install.py` — already present in the baseline tree and unmodified
by this sprint. `A2` needs no new tool and no skill; it is a verification
exercise against an existing, already-wired guard.

---

## 8. No skill was forged

Nothing in this sprint is a reusable computational tool for a host. The
three new artifacts (`scripts/cursor_adapter.py`, `hooks/on_push.py`,
`scripts/audit_cursor_models.py`) are framework-root `scripts/`/`hooks/`
artifacts under `devops_agent`'s sole `Write`/`Edit` jurisdiction
(`agents.md §6`, `F-086-A1`) — not `skills/[name]/scripts/`, and forging a
skill wrapper around any of them would be the exact confusion `agents.md §3
three_file_standard` and Sprint 023's `C4.2` finding warn against. Each
declares its invoker under `RA-16` (`P4` via `scripts/install.py`'s import,
`P9` via `.git/hooks/pre-push`, `P4.2` via the `Makefile 'cursor-tiers'`
target), so none is orphaned. No unit in `## Work` was blocked on a missing
skill; §5 confirms the three scripts have no existing substitute and are
correctly scoped as framework code rather than skill candidates.
