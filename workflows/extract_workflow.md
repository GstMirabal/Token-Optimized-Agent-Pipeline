---
description: "Knowledge Extractor and Intelligence Distillation Protocol (Keyword: extract)"
version: 4.0.0
invoked_by: human:/agents:extract, close_workflow.md#extract_handoff
---

# 🛡️ Workflow: Extract (Knowledge Distillation)

Heuristic distillation and index-only memory update. Distinct from `close_workflow.md`: this protocol governs *what* gets kept as knowledge and *how* it is indexed — `close_workflow.md` governs the session's final purge and lockdown. Normative basis: `agents.md §4 (Memory Management and Feedback Loop)`.

## Execution Flow

| Phase | Step | Action / Constraint |
| :--- | :--- | :--- |
| **0. Zero-Memory Initialization** | `read_ruleset` | `Governance Learner` verifies `agents.md §4` is in context (auto-imported); full re-read only after compaction (`anti_amnesia`). |
| **1. Strategic Extraction** | `signal_scan` | Run `python3 .agents/skills/compliance-checker/scripts/distill.py` — frequency analysis over `memory/telemetry/raw_errors.json` (gracefully silent if no telemetry exists). Complement with session-log review for friction the hooks couldn't see, distinguishing "High-Signal" heuristics from one-off noise. |
| **1. Strategic Extraction** | `amnesia_test` | Apply the Amnesia Test: would a fresh-context subagent, with zero memory of this session, repeat the same mistake without this knowledge? If no, discard it. |
| **2. Rule Integration Check** | `rule_vs_ki` | If the surviving knowledge is "almost a rule" (recurs across sprints rather than being sprint-specific), route it to `Rule Validator` as a governance amendment proposal instead of a Knowledge Item — do not double-record it. |
| **2. Rule Integration Check** | `upstream_feedback` | Apply the three-tier living flow (`agents.md §4 feedback_upstream`): **host-class** → `memory_index.json`; **project-family-class** → draft into the host's profile path (`--profile-path`, not the submodule); **framework-class** (any lesson that would improve every host — a workflow gap, a phantom reference, a broken assumption) → draft a rule amendment or fix proposal for the `.agents` repo and surface it to the human. A framework-class lesson dying in a local index is a violation, not tidiness. **Every candidate KI MUST carry `routing_class`** (`host` \| `profile` \| `nucleus` \| `discard`) before it may be indexed — an unclassified candidate is escalated in `close_handoff`, not silently dropped. How-to for host-side creation and promotion: `docs/guides/SELF_IMPROVEMENT_GUIDE.md`. |
| **3. Semantic Indexing** | `routing_gate` | Reject `index_update` for any candidate whose `routing_class` is absent or `discard`. `discard` entries are not written to `memory_index.json`. `nucleus`-class items MUST also have an upstream draft started (`feedback_upstream`); indexing alone does not satisfy routing. |
| **3. Semantic Indexing** | `index_update` | For genuine sprint-scoped knowledge with `routing_class: host`, append one entry to `memory_index.json` (`id`, `summary`, `routing_class`) following the current flat schema and the `single_line_breakdown` rule — one sentence per entry, no nested domain subfolders. |
| **3. Semantic Indexing** | `last_update` | Refresh `last_update` and `sprint_id` at the top of `memory_index.json`. |
| **4. Absolute Purge** | `redundant_ki_purge` | Delete any `memory_index.json` entry superseded by a newer one on the same failure class (`definitive_amnesia` — no accumulation of duplicate KIs). |
| **5. Handoff** | `close_handoff` | Return control to `DevOps Agent` / `close_workflow.md` for the physical `/memory/` wipe — this workflow only decides *what* survives into the index, it never itself performs the destructive purge. |

---
*Reconstructed for the Pipeline — restores the component listed in `docs/architecture/topology_map.md` ("Heuristic distillation and domain-isolated memory update") using the current §4 memory rules and the current flat `memory_index.json` schema (v4.0.0).*
