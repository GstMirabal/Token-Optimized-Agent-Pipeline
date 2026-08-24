---
description: "Model tiering — role class decides model, and two gates keep the map true (Sprint 022)"
status: "COMPLETED"
version: 1.0.0
---

# Roadmap: Sprint 022 - Model Tiering

## Status
- **Strategy Lock:** `CLOSED`
- **Sprint ID:** `022` · **Branch:** `ai-sprint/022`, from `main` at `2d5f056` (`v4.6.0`)
- **`RA-06` deviation, declared:** `[NNN]-[slug].md`, this directory's standing convention since `000-`.

## Objective

Adopt upstream finding `#12`: 0 of 13 profiles declared a model, so every role —
including the deterministic ones — ran at the session's top tier. Usage reports
attribute **100% of spend to subagent-heavy sessions**, and `agents.md §6`
mandates eight roles per pipeline pass.

## Work Breakdown

| Commit | Track | Scope | Status |
| :--- | :--- | :--- | :--- |
| 0 | **Tiers declared** | 13 profiles + `config/model_tiers.json` | ✅ |
| 1 | **The detector** | `detect_new_models.py`, structural parser, severity ladder | ✅ |
| 2 | **The guards** | `check_model_tiers.py`, both wired into `make verify` | ✅ |
| 3 | **Charter + ledger** | `token_economy_agent` owns the map; sprint records | ✅ |

## Two design corrections found by verifying, not reviewing

### The parser read one model's retirement as another's

The bundled catalogue holds a second table mapping user phrasing to suggested
models — `| "sonnet 3.7" | Retired — suggest \`claude-sonnet-5\` |`. A parser
scanning each row for any alias and any status word recorded **Sonnet 5 as
Retired**, and with the severity ladder wired that fails the build over a tier
that is perfectly current.

The discriminator is structural: a catalogue row has the alias **alone in its
second cell**. The phrasing table is rejected by construction rather than by a
denylist. The fixture in `tests/` reproduces that table deliberately — without
it, the broken parser passes.

### The gate would never have fired in CI

The bundled catalogue lives in a per-user temp directory the system clears and
CI never has. A gate reading it directly is a mechanism wired where it cannot
run (`RA-16`) — and this sprint was building exactly that.

`catalog_snapshot` in `config/model_tiers.json` is therefore the **durable,
committed copy and the gate's only source**, so `--check` returns the same
verdict on a laptop and in CI. Reading the bundled file is the opportunistic
half that proposes refreshing the snapshot, and it says so when absent instead
of implying the map was checked against something newer.

## The severity ladder

| Finding | Response | Why |
| :--- | :--- | :--- |
| New alias | **Propose** | A model is not adopted for existing |
| Tier model `Deprecated` | Propose **with its retirement date** | Room, but the clock is running |
| Tier model `Retired` | **Build fails, exit 2** | Not a judgment call: a retired model returns 404 |

## Scope limit

`audit_cursor_models.py` and the `cursor` column belong to Sprint `026`; this
sprint fixes the semantics of the three tiers and leaves that column null.
**Price detection is not implemented and not faked** — prices exist on no disk
here, so `verified_at` makes the gap age visibly instead of rotting quietly.

## Delegation

Sequential; the conflict is reported per `start_workflow.md` Phase 2 and
authorised. See `agent_assignment.md`.
