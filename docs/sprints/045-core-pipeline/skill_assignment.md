# Skill Assignment — Sprint 045 (nucleus-ruleset-mechanism-audit)

Source: `docs/sprints/045-core-pipeline/IMPLEMENTATION_PLAN.md`.
Phase 4.2 of `workflows/pipeline_workflow.md`. Drafted from this template.

Mode: **claude-code**, `delegation_mode: native`.

After writing this file, run:
`python3 scripts/check_forge_ladder.py --sprint-dir docs/sprints/045-core-pipeline`
(exit `2` rejects an empty forge destination or submodule contamination).

---

## 1. Priority ladder (record every rung)

`rules/skills_and_integrations.md §1`:

| Rung | Source | Result | Evidence |
| :--- | :--- | :--- | :--- |
| P1 | `skills/manifest_skills.json` | HIT — existing skills cover the whole sprint | `audit_workflow.md` tooling: `scripts/verify_references.py`, `scripts/map_workflows.py`, `scripts/scan_workflow_determinism.py`, `skills/topology-monitor/scripts/legacy_app_auditor.py`, `skills/slash-commander/scripts/verify_commands.py`, `skills/token-saver-auditor/scripts/audit_plan.py` |
| P2 | `autoskills-3rd` | not reached | P1 satisfied the need |
| P3 | `https://skills.sh/` | not reached | P1 satisfied the need |
| P4 | Three-File Standard at Destination | not reached | no skill is forged this sprint |

This sprint **builds no new skill**. It is a read-only audit that runs
already-present deterministic tools and adds semantic classification on top.
No machine-readable `skills.sh` trail is required because no build is claimed.

---

## 2. Per-unit tool resolution

| Unit | Skill / tool | Destination | P1–P4 trail |
| :--- | :--- | :--- | :--- |
| 1 | `scripts/verify_references.py`, `rules/LEGACY_RULE_CONCORDANCE.md`, `grep` | N/A | P1 HIT |
| 2 | `scripts/map_workflows.py`, `scripts/scan_workflow_determinism.py`, `scripts/verify_references.py`, `skills/slash-commander/scripts/verify_commands.py` | N/A | P1 HIT |
| 3 | `scripts/verify_references.py` (check d), `skills/topology-monitor/scripts/legacy_app_auditor.py`, `grep -rl` | N/A | P1 HIT |
| 4 | none (synthesis of units 1–3 + cross-check against `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`) | N/A | P1 HIT |

---

## 3. Skills used

| Skill | Why |
| :--- | :--- |
| `topology-monitor` (`legacy_app_auditor.py`) | Three-File Skill Standard verification for unit 3 |
| `slash-commander` (`verify_commands.py`) | Command↔workflow link integrity for unit 2 |
| `token-saver-auditor` (`audit_plan.py`) | Phase 1/5 plan gate (already run, exit 0) |

## 4. Skills considered and rejected

| Candidate | Why rejected |
| :--- | :--- |
| `mass-standardizer` | Rewrites artifacts to Option B; this sprint classifies only, applies nothing (`IMPLEMENTATION_PLAN.md` `D1`) |
| `graphify` | Graph is already current (`session_probe` clean); no rebuild needed for a read-only textual audit |
| `skillopt` | Prompt-optimization training; irrelevant to a governance audit |

## 5. Gaps

None. Every unit's tooling resolves at P1.
