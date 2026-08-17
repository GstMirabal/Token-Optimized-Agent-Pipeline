# 📝 Sprint Log: #025 — `jurisdiction`

**Session Tracker**: `25b16540-e1d3-4edb-98ee-c6ccba98ce12`
**Role Active**: Principal Agent (sequential — see `agent_assignment.md`)

---

## 🚦 Session Metadata

| Parameter | Value |
| :--- | :--- |
| **Active Layer** | `core` / `pipeline` |
| **Strategic Goal** | A host session's work can never land inside the framework submodule, and the rule is enforced rather than remembered |
| **Intelligence State** | `CERTIFIED` — `make verify` green, 137 tests |
| **Base** | `ai-sprint/024` — not `main`, because the guard is blind without that sprint's `.gitignore` change |

---

## 🏁 Sprint Progression

- [x] **Objective 1**: the discriminator is extracted, not reinvented a third time
    - `[x]` `scripts/_mode.py` — `is_nucleus()` from git's own layout
    - `[x]` `session_probe.py` delegates instead of duplicating
- [x] **Objective 2**: the rule becomes a mechanism
    - `[x]` `scripts/submodule_purity.py`, exit `2` per `RA-11`
    - `[x]` Classifies untracked records vs edits to tracked files — different remedies
    - `[x]` No-op in nucleus mode, with the `D7` mirror as its regression test
- [x] **Objective 3**: it fires where it can still help
    - `[x]` `hooks/on_commit.py` at commit time, not only at close
    - `[x]` `close_workflow.md` Phase 5 invokes the script instead of describing a command
- [x] **Objective 4**: the rule written where it is governed
    - `[x]` `agents.md §3 jurisdiction`

---

## 🧠 Rule Amendments & Heuristic Harvest

| Friction Point | Resolution | KI ID |
| :--- | :--- | :--- |
| The only protection against a host dirtying `.agents` was one prose line, flagged by the repository's own determinism scanner in every `make verify` run and never actioned | Script with a declared invoker; the standing warning disappearing is the proof | `F-024-D8` |
| `git status --porcelain` collapses an untracked tree to its top directory, so the guard would have reported `?? docs/` and told the operator nothing actionable | `-uall`. **Caught by its own test**, not by review | `F-025-J1` |
| `agents.md §3` stated the doctrine (`strict_rule`, `federation`) and named no enforcement for it | New `jurisdiction` row naming both invocation points | `F-025-J2` |

**Harvest**: `F-025-J1` is the sprint's own instance of the pattern both sprints
chase — a check that returns the right verdict and a useless message is a check
nobody acts on. The verdict was correct either way; only the test exercised what
a human would actually read.

---

## ⚓ Documentation Entry Point Seal

**Strategic Lock**: `CLOSED`
**Next Phase**: Sprint `021` (`cost-instrumentation`) — the session-cost meter,
the session-length bound, and the `SUSPENDED` anchor state.

**Not yet integrated**: `ai-sprint/025` stacks on `ai-sprint/024`; both are
unmerged. Integration is `deployment_workflow.md`'s job (`RA-12`), and `024`
merges first.

*Certified under conventional commit standard: `feat(scope): message #025`*
