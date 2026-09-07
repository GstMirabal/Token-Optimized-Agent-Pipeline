# Task Scope — Sprint 045 (nucleus-ruleset-mechanism-audit)

Phase 4.3 of `workflows/pipeline_workflow.md`. Rule audit of the Roadmap against
current `rules/`. `jurisdictional_lock` and `no_interference` are both applied by
reading this file.

Mode: **claude-code**, `delegation_mode: native`. Model/Effort from
`config/model_tiers.json` `tiers.author.claude_code` (`sonnet` / `medium`) for
every unit — all four are documentation authorship (audit reports), no code, no
mechanical-tier profile, and `rule_validator` is not in `tiers.gate.profiles`.
No `tier_escalation`.

Check: `python3 scripts/check_task_scope.py --sprint-dir docs/sprints/045-core-pipeline`

---

## Work

| # | File | Operation | Risk | Assignee | Model | Effort | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `docs/audits/NUCLEUS_RULESET_AUDIT_REPORT-045.md` | create | low | `rule_validator` | sonnet | medium | ⏳ |
| 2 | `docs/audits/NUCLEUS_WORKFLOW_AUDIT_REPORT-045.md` | create | low | `rule_validator` | sonnet | medium | ⏳ |
| 3 | `docs/audits/NUCLEUS_MECHANISM_AUDIT_REPORT-045.md` | create | low | `rule_validator` | sonnet | medium | ⏳ |
| 4 | `docs/audits/NUCLEUS_AUDIT_SYNTHESIS-045.md` | create | medium | `rule_validator` | sonnet | medium | ⏳ |

Wave 1 = units 1–3 (parallel, disjoint targets). Wave 2 = unit 4 (after 1–3).

---

## Rule audit

| Rule | Unit(s) | Finding |
| :--- | :--- | :--- |
| `agents.md §2 jurisdictional_lock` | all | One physical file per unit. No file listed twice. Each is `create` of a new path under `docs/audits/`. PASS. |
| `agents.md §2 no_interference` | 1, 2, 3 | Three disjoint target files, dispatched in parallel — no shared target, so a concurrent dispatch cannot collide. Unit 4 starts only after 1–3 land. PASS. |
| `agents.md §1` (Language `code_logic`) | 1, 2, 3, 4 | The four audit reports are artifacts under `docs/` → **English only**. Spanish is confined to chat and `IMPLEMENTATION_PLAN.md` (`§1 user_chat`). |
| `agents.md §1 unambiguous_action` | all | Every finding row must state the norm by name, the verdict (`VIGENTE`/`OBSOLETA`/`MEJORAR`), and the reproducing command or citation. No `review`/`evaluate`/`clean` as a verdict without its proof. |
| `agents.md §1 technical_clarity` | all | Markdown tables, no Mermaid/ASCII, no redundant greetings. |
| `agents.md §3 strict_rule` / `D1` of the plan | 1–4 | The reports **redactan** enmiendas as proposed text inside the report. They MUST NOT edit `agents.md` or any `rules/*.md`. Verification asserts `git status --porcelain -- agents.md rules/` is empty. |
| `agents.md §3 nucleus_neutrality` | all | Nucleus session: no automatic structural scaffolding. Only the four named files are created. PASS. |
| `agents.md §5 mandatory_topology` | all | Sprint dir `docs/sprints/045-core-pipeline/` (`[ID]-[Stack]-[Layer]`). Reports live in `docs/audits/` following precedent `PIPELINE_AUDIT_REPORT-042.md`. PASS. |
| `RA-06 IDENTITY_NAMING` | 1–4 | File names follow `<SCOPE>_AUDIT_REPORT-045.md` / `NUCLEUS_AUDIT_SYNTHESIS-045.md` — the `-045` suffix matches the `-042` precedent, not a violation of Option B (`docs/audits/` convention). |
| `RA-16 INVOCATION_COVERAGE` | all | No new mechanism, script, hook, skill or workflow is created. `verify_references.py` check (d) unaffected. |
| `RA-14 PATCH_PROPAGATION` | 4 | The synthesis is a multi-input consolidation: every norm marked `OBSOLETA`/`MEJORAR` in units 1–3 must appear in the synthesis register, and every cross-reference to `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` must be grepped to confirm no open finding already owns the same defect. |
| `rules/documentation_standard.md` | 1–4 | Drafted from `docs/standards/templates/AUDIT_REPORT_TEMPLATE.md`. Metadata / timestamp block stamped. Diátaxis class: Reference (audit record). |
| `rules/qa_and_testing.md` | Phase 7 | Gate 1 (`qa_agent`) checks structure: template adherence, English-only, every `agents.md` `§`/`RA-NN` present in unit 1's classification, table shape. Gate 2 (`tester_agent`) re-runs the plan Verification table and confirms `make verify` parity + no write to `agents.md`/`rules/`. |
| `RA-12 BRANCH_DISCIPLINE` | all | Execution on `ai-sprint/045` (cut from `main` @ `e0189a3` before the plan commit). No commit to `main`. |
| `RA-08 COMMIT_SQUASH` | all | Atomic local commits, one per unit, each carrying `#045`. Squash & push at `close_workflow.md` Phase 5. |

## Capability check

Assignee `rule_validator` holds `Read`, `Glob`, `Grep`, `Write`, `Edit` — it can
perform the `create` operation on all four units. No mechanical-tier profile in
the table, so `check_task_scope.py`'s mechanical-high rule does not engage. Shape
`# | File | Operation | Risk | Assignee | Model | Effort | Status` present on the
Work table.

## Out of scope (from the plan, restated for the auditor)

- Applying any amendment (editing `agents.md` / `rules/` / deleting a mechanism) →
  the execution sprint recommended inside `NUCLEUS_AUDIT_SYNTHESIS-045.md`.
- Row-by-row triage of `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md` → nucleus
  planning input; the synthesis only cross-checks against it.
- `profiles/` packs → `RA-15`, host-controlled path, never the public nucleus.
- Non-normative `docs/` freshness → already owned by `docs-freshness-check`.
