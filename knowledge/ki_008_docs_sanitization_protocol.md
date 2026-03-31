# 🧠 Knowledge Item: Docs Sanitization & Mirrored Roadmap Protocol

## 🚦 Context: Duplication and Out-of-Place Files
In multi-phase projects, documents like roadmaps often drift between the framework's local tracking (`.agents/task/roadmaps/`) and the project's official documentation (`docs/`).

## ⚠️ The Blockage: Drift and Confusion
Having a roadmap in `docs/` and another in `.agents/` leads to double-tracking and outdated information. Furthermore, legacy implementation plans in `docs/archived/` clutter the master repository.

## ✅ The Solution: The 1-Source Mirroring Rule
1.  **Single Source of Truth**: Active roadmaps reside in `.agents/task/roadmaps/`.
2.  **Archiving**: Legacy plans and audit reports should be moved to `.agents/task/history/` to keep `docs/` focused on architecture/API.
3.  **Mirrored Delivery**: Only at the *end* of a phase, the final state of the roadmap is mirrored to `docs/` as a permanent record. Until then, delete redundant copies in `docs/` to avoid confusion.

---
`Governance Standard: Scaffolding Retrofitting Phase 5`
