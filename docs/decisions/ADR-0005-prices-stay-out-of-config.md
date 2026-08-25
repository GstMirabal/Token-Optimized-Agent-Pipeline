# 📜 ADR-0005: Prices stay out of config

**Status**: `Accepted`
**Date**: 2026-08-25
**Triggers**: 4 (`rules/documentation_standard.md §3.1`)

**Last Audit Sprint**: 029
**Last Audit Date**: 2026-08-25

---

## 1. Context

Sprint 022 needed family cost ratios to compare tiers. The instinct is to copy
vendor price tables into `config/model_tiers.json`.

Measured constraints when the decision was made
(`docs/roadmaps/core/pipeline/021-030-program-queue.md`, "Keeping it current"):

| Fact | Command / observation |
| :--- | :--- |
| Config holds tier aliases, not dollar prices | `python3 -c "import json; print('price' in json.dumps(json.load(open('config/model_tiers.json'))).lower())"` → expect no live price table |
| `/v1/models` returns no prices | Anthropic models endpoint exposes token limits/capabilities, not $/1M |
| Admitting `anthropic` SDK for a rare check | `rules/code_craft.md §4` — dependency for a few comparisons per year |

Copying prices into config is the same defect class as hand-maintained README
counts: a claim that looks live and is not.

## 2. Decision

**Prices, context-window marketing figures, and dollar ratios do not live in
`config/model_tiers.json`.** They live in dated decision/roadmap prose (or an
agent verification action that records `verified_at`).

`config/model_tiers.json` holds: tier → tool aliases, exclusions with reasons,
catalog snapshots for detectors, and freshness metadata — never a price column
treated as current.

## 3. Consequences

**Easier**: config cannot silently quote yesterday's list price; detectors
(`detect_new_models.py`, `audit_cursor_models.py`) stay dependency-free for what
they can see on disk.

**Harder**: anyone comparing dollars must re-verify against the vendor reference
and date the claim (T5: figure + command). Sprint 021 meters **tokens**, not
dollars, for the same reason.

---
*Immutable once Accepted — a changed decision gets a new ADR that supersedes this one, never an in-place edit (`rules/documentation_standard.md §3`). File lives at `docs/decisions/ADR-0005-prices-stay-out-of-config.md`.*
