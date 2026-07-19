---
description: "Standardized Hierarchy Alignment Protocol (SHAP)"
version: 5.0.0
---

# 🛡️ Workflow: Standardization (Alignment V3)

Governance protocol to enforce structural sovereignty, unique naming, and symmetric documentation.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Trigger** | `condition_check` | Triggered if naming drift, empty folders, or asymmetric roadmaps are detected. |
| **1. Naming Standard** | **Option B** | Force rename all docs to `[MODULE]_[TYPE].md`. Force rename sprint folders to `[ID]-[Stack]-[Layer]`. |
| **2. Symmetric Audit** | `roadmap_sync` | Ensure every Backend Roadmap has a corresponding Frontend Roadmap and vice-versa. |
| **3. Topological Purity** | `noise_purge` | Recursively delete all empty directories in `/docs/` and `/backend/` (J-07). |
| **4. Historical Capture**| `walkthrough_gen` | Generate or update `[MODULE]_WALKTHROUGH.md` for all operational modules. |

## Phase 5: Legacy Absorption Protocol (Onboarding Scenario B)

Invoked by `start_workflow first_run_scaffold` when prior agent-generated documentation is detected. The pipeline is strictly ordered — each gate blocks the next:

| Step | Gate | Action / Constraint |
| :--- | :--- | :--- |
| **5.1 Census** | `inventory` | Enumerate every legacy artifact (tracked AND untracked): `task/`, `implementation_plan*`, `knowledge/`, `memory/<domain>/`, `docs/active_task.md`, `.agent_state/`, numbered roadmaps, other frameworks' rule files. Record the full list with file counts. |
| **5.2 Secret Scan** | `shield_gate` | Run `env-shielding-auditor` + the `on_commit.py` secret patterns over ALL census material **before anything enters git**. Findings go to the reconciliation report for human redact/exclude decisions. Order is non-negotiable: scan → snapshot, never the reverse. |
| **5.3 Snapshot** | `reversibility_gate` | Create branch `archive/pre-agents-onboarding-[date]` committing every census artifact (`git add -f` for ignored/untracked ones, minus human-excluded secrets). **No migration or purge may execute unless this snapshot exists** — undoing the entire onboarding must always be one checkout away. |
| **5.4 Report** | `reconciliation_report` | Produce the migration manifest (source → destination → action, per the routing table below) + secret-scan findings + submodule identity check result. Present to the human. |
| **5.5 Golden Gate** | `human_ok` | Explicit human authorization of the manifest. Single attended invocation — never inside an unattended `/loop`. |
| **5.6 Migration** | `absorb` | Execute the manifest exactly. No improvisation beyond it. |
| **5.7 Integrity** | `conservation_audit` | Verify: (a) every census file is accounted for (destination + snapshot + authorized-purge lists must sum to the census count); (b) `link_audit` — no host `.md` references a migrated path; (c) seal the report with the result and store it as `docs/ONBOARDING_AUDIT.md` — the onboarding becomes its own auditable artifact. |

### Legacy Routing Table (5.4 manifest baseline)

| Legacy artifact | V3 destination | Action |
| :--- | :--- | :--- |
| `task/task.md`, `docs/active_task.md`, `.agent_state/session_metadata.json` | `docs/active_state.json` | Absorb any live state; archive the file (parallel state is PROHIBITED — `state_homologation`). |
| `task/sprints/`, `task/roadmaps/`, root `implementation_plan*` | `docs/sprints/[ID]-[Stack]-[Layer]/` | Relocate into the matching sprint; the internal WBS format (Goal → Components → Verification Gates) is kept as-is. |
| `knowledge/ki_*.md`, `memory/<domain>/ki_*.md` | Three-way triage | (a) "almost a rule" → amendment proposal via `constitutional_escalation`; (b) project-domain KIs → `profiles/[name]/`; (c) rest → one-line summary in `memory_index.json`, file purged (Amnesia Test first — `extract_workflow.md`). |
| `ki_index.json`, per-domain `memory_index.json` | Flat summary-only `memory_index.json` | Merge summaries; discard parallel indexes. |
| Numbered roadmaps (`NNN-title.md`) | Untouched if closed history; Option B rename (`[MODULE]_ROADMAP.md`) only for ACTIVE ones | History is never rewritten. |
| `violation_log.md`, `PROCEDURAL_DEVIATION_*.md` | `memory/telemetry/` → distillation → purge | Normal jurisprudence cycle. |
| Other frameworks' files (`.cursor/rules`, `.windsurfrules`, …) | Proposed for archive in the snapshot | Never deleted without explicit human OK — they may contain learning worth triaging. |

---
*Optimized for Matrix V3 Unique Naming, Symmetric Observability & Reversible Legacy Absorption (v5.0.0).*
