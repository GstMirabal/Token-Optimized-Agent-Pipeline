# Prompt Measurement — Sprint 059

## Instrument

Command: `python3 scripts/prompt_count.py --session <id> [--project <path>] --json`, at commit `10c8e1a`.

| Output key | Meaning |
| :--- | :--- |
| `tool_use_total` | Distinct `tool_use` block ids |
| `decisions_user_approved` | Decisions with `source == "user_temporary"`; a human approved a prompt |
| `decisions_user_approved_once` | Subset with `grantScope == "once"`; older records have no `grantScope` |
| `decisions_by_config` | Decisions with `source == "config"`; an allow rule or the permission mode answered |
| `decisions_other_source` | Decisions with any other source |
| `tool_uses_without_decision` | Tool uses with no recorded decision; upper bound on rejections plus unresolved calls |

Transcripts record approvals only, so no rejected count exists.

## Baseline

Measured 2026-11-08.

| Session type | Session | `tool_use_total` | `decisions_user_approved` | `decisions_user_approved_once` | `decisions_by_config` | `decisions_other_source` | `tool_uses_without_decision` |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Nucleus | `e9a7a9bf` | 178 | 99 | 99 | 78 | 0 | 1 |
| Host (host project) | — | 156 | 25 | 25 | 131 | 0 | 0 |

The two sessions differ in length and task, so the rows are not comparable as a rate between them.

## Re-measurement after B-06

| Session type | Session | `tool_use_total` | `decisions_user_approved` | `decisions_user_approved_once` | `decisions_by_config` | `decisions_other_source` | `tool_uses_without_decision` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Nucleus (under sandbox) | `a84488fd` | 10 | 6 | 6 | 3 | 0 | 1 |

The session had 10 tool uses when measured, so the row is not usable as a rate against the baseline.
