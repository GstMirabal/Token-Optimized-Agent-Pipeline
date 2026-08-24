# 📝 Sprint Log: #022 — `model-tiering`

**Session Tracker**: `25b16540-e1d3-4edb-98ee-c6ccba98ce12`
**Role Active**: Principal Agent (sequential — see `agent_assignment.md`)

---

## 🚦 Session Metadata

| Parameter | Value |
| :--- | :--- |
| **Active Layer** | `core` / `pipeline` |
| **Strategic Goal** | Role class decides model, and two gates keep the map true |
| **Intelligence State** | `CERTIFIED` — `make verify` green, 161 tests |
| **Base** | `main` at `2d5f056` (`v4.6.0`) |

---

## 🏁 Sprint Progression

- [x] **T1**: the 13 profiles declare `model:` and `tier:`
- [x] **T2**: `config/model_tiers.json` — the map, with the durable catalogue snapshot
- [x] **T3**: `detect_new_models.py` — structural parser over the bundled catalogue
- [x] **T4**: the severity ladder, wired to the snapshot so it fires in CI
- [x] **T5**: `check_model_tiers.py` — two guards, both in `make verify`
- [x] **T6**: `token_economy_agent` owns the map, the escalation path, and the rejection

---

## 🧠 Rule Amendments & Heuristic Harvest

| Friction Point | Resolution | KI ID |
| :--- | :--- | :--- |
| The tier table was about to be written **from memory** | The `claude-api` reference trigger caught it, and the table changed materially: Fable 5 costs **twice** Opus, not being a cheap top tier | `F-022-T0` |
| A parser scanning whole rows read one model's retirement as another's — `claude-sonnet-5` came out `Retired` | Structural discriminator: a catalogue row has the alias **alone in its second cell**. **With the ladder wired, that false verdict would have failed the build over a healthy tier** | `F-022-T1` |
| The bundled catalogue lives in a temp directory CI never has | The gate reads the **committed snapshot**; the bundled file is the opportunistic refresh. Without this the gate was an ornament in CI — `RA-16`, inside the sprint building it | `F-022-T2` |
| The module docstring described the parser it had replaced | Corrected. `RA-14` drift inside a file written minutes earlier | `F-022-T3` |
| `__import__('os')` inline and `/private/tmp` hardcoded | Normal imports; temp roots derived per platform and filtered by existence | `F-022-T4` |
| Tier-only declaration was considered | Rejected with its reason recorded: the harness ignores unknown frontmatter keys, so the file would claim one tier while the subagent ran on the session default | `F-022-T5` |

**Harvest**: two of the six were design defects, not typos, and **both were found
by verifying rather than reviewing** — one by parsing the real catalogue instead
of an invented fixture, the other by asking where that file actually lives. The
hermetic test now reproduces the phrasing table deliberately: without it, the
broken parser passes.

---

## ⚓ Documentation Entry Point Seal

**Strategic Lock**: `CLOSED`
**Next Phase**: Sprint `023` (`upstream-findings`) — eleven units, and the one that
gives the Implementation Plan its gate.

**Not yet integrated**: `ai-sprint/022` is unmerged. Integration is
`deployment_workflow.md`'s job (`RA-12`).

*Certified under conventional commit standard: `feat(scope): message #022`*
