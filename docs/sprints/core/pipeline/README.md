# Recovered sprint records — pre-renumbering

Two Implementation Plans from April 2026, under the numbering that preceded the
phase renumbering:

| File | Then | Now |
| :--- | :--- | :--- |
| `031_implementation_plan.md` | Sprint 031 — Refined Telemetry & Redundancy | `docs/roadmaps/core/pipeline/013-refined-telemetry-and-redundancy.md` |
| `032_implementation_plan.md` | Sprint 032 — Topological Flattening | `docs/roadmaps/core/pipeline/016-folder-topology-migration.md` |

## Why they are committed here rather than deleted or moved

They are the evidence for `F-024-D4`. Until Sprint `024` they sat on one
machine, **untracked**, because `.gitignore` excluded `docs/sprints/` — they had
survived four months by accident and were absent from every clone. Deleting them
would destroy the demonstration; renaming them into the current convention would
rewrite a record of what the layout actually was.

They are kept **as found**, in the path they were found in — one of the four
sprint-path forms `agents.md §5` records as having been in circulation before
Phase 019 declared a single canonical one.

## Not the canonical path

New sprints use `docs/sprints/[Sprint_ID]-[Stack]-[Layer]/`
(`agents.md §5 mandatory_topology`). `024-core-pipeline/` is the first.
