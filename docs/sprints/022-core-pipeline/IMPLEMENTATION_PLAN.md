---
description: "Implementation Plan — Sprint 022 model tiering"
status: "APPROVED"
version: 1.0.0
approved_by: human
approved_at: "2026-08-17"
---

# Implementation Plan: Sprint 022 - Model Tiering

**Branch:** `ai-sprint/022`, from `main` at `2d5f056` (`v4.6.0`)

## Context

Upstream finding `#12`, routed by a host and adopted nowhere: **0 of 13 profiles
declared a model**, so every role ran at the session's top tier — the
deterministic ones included. `rules/token_economy.md §2` governs what a
subagent's prompt contains; nothing governed which model it ran on.

Sprint `021` made this measurable. The queue put tiering second for that reason:
without the meter, any claim about what tiering saves is unfalsifiable.

## Design

**Two fields, not one.** A profile declares `model:` (a family alias, which the
harness applies natively) and `tier:` (the intent). Tier-only was rejected:
Claude Code ignores frontmatter keys it does not know, so the file would claim
one thing while the subagent ran on the session default — the most expensive
tier. Both exist precisely so they can disagree, and `check_model_tiers.py` is
what notices.

**Family aliases, never dated IDs.** `opus` absorbs version bumps; a pinned
`claude-opus-4-1-20250805` would need editing in thirteen files on every bump.

| Tier | Profiles | Claude Code | Basis |
| :--- | :--- | :--- | :--- |
| `gate` | `qa_agent`, `tester_agent`, `principal_agent` | `opus` + `high` | Across four host sprints every central defect was found by a gate and nothing else, several after surviving their author's verification |
| `author` | 7 profiles | `sonnet` + `medium` | Structured authorship against a stated rule; downstream gates catch errors |
| `mechanical` | `devops_agent`, `git_sync_agent`, `topology_mapper` | `haiku` + `low` | Deterministic results; a wrong answer fails at the next command |

**Fable 5 excluded with its reason** — 2× the cost of Opus and 30-day retention,
so it does not work under ZDR. **Haiku 4.5's 200K ceiling is declared**, since
`mechanical` inherits it.

## Verification

| Check | Result |
| :--- | :--- |
| 13 profiles agree with the map | ✅ `check_model_tiers.py` |
| Bridge needs no reinstall | ✅ `.claude/agents/*.md` are symlinks |
| Parser survives the phrasing table | ✅ hermetic fixture reproduces it |
| Gate blocks on a retired tier | ✅ exit 2, naming the tier |
| Gate reads the snapshot, not the temp file | ✅ same verdict in CI |
| `make verify` | ✅ **161 tests** |

## Abort criterion

If a subagent fails to start on the new frontmatter, revert before touching
anything else: thirteen broken profiles would leave the pipeline with no roles.
**Did not fire** — 13/13 parse with all five keys.

## Out of scope

`audit_cursor_models.py` (Sprint `026`), `tools:` changes (`C5` of Sprint `023`),
price detection (not on disk — declared, not faked), and a model-selector agent
(rejected by `token_economy_agent`'s own `burden_of_proof`).
