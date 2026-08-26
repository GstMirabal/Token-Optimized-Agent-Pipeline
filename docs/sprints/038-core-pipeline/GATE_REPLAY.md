# Gate replay — Sprint 038 (D16)

**Sprint**: `038-core-pipeline` · **Branch**: `ai-sprint/038`
**Gate model (live map)**: `claude-opus-5` / `anthropic` / `max`
(`python3 scripts/audit_cursor_models.py --resolve gate`)
**Protocol**: `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` §5 · Design **D16** (Sprint 034)
**Constraint**: Findings use ADR-0008 vocabulary only. A clean replay does **not**
prove superiority and must **not** rank families (D7 / D13).

Emitted by `qa_agent` posture (fresh-context review of historical diffs);
transcribed by `orchestrator` into this file (`F-026-A1`).

---

## Corpus 032 — author-tier-trial

| Field | Value |
| :--- | :--- |
| Merge / tip | `d5fd1e9` — `Sprint 032: author-tier-trial (promote grok-4.5) (#64)` |
| Base (parent) | `0429f03` (`v4.14.0`) |
| Original Double-Gate | QA round 1 **APPROVED**; Tester round 1 **APPROVED** (`docs/sprints/032-core-pipeline/SPRINT_LOG.md`) |
| Functional delta reviewed | `scripts/session_probe.py` (`stamp_last_platform_probe`) + `tests/test_session_protocol.py` |

### Findings

| # | Verdict | Class | Finding |
| :--- | :--- | :--- | :--- |
| 032-1 | **APPROVED** | | `stamp_last_platform_probe` runs only after a completed interrogation path; documented skips must not stamp. Tests stub the stamp on legacy cases that share `probe_platform`. Matches plan D2/D3 and RA-16 invokers (`start` 0.7 / close 3.5). |
| 032-2 | **RECORD** | `testifying` | Squash-merge tip is a rollup of many sprint commits; replay scope is the tip tree vs parent, not each intermediate SHA. Original gate already saw the landed tree. Not a defect. |

### Replay outcome (032)

**Clean** (plus one `RECORD`/`testifying`). Agrees with the original gate on the
functional payload. No escaped `charter` / `instructing` defect found on this
diff.

---

## Corpus 033 — implementer-role

| Field | Value |
| :--- | :--- |
| Merge / tip | `05556f1` — `Sprint 033: implementer-role (close F-021-A2) (#65)` |
| Base (parent) | `8b3fb6d` (`v4.15.0` seal) |
| Original Double-Gate | QA round 1 **APPROVED**; Tester round 1 **APPROVED** (`docs/sprints/033-core-pipeline/SPRINT_LOG.md`) |
| Functional delta reviewed | `agents/implementer_agent.md`, `agents/devops_agent.md` tools drop, `tests/test_implementer_role.py`, ADR-0009 |

### Findings

| # | Verdict | Class | Finding |
| :--- | :--- | :--- | :--- |
| 033-1 | **APPROVED** | | `implementer_agent` holds `Write`/`Edit` for framework-root `scripts/`/`hooks/`/`tests/`; `devops_agent` retains `Bash` only. Word-boundary recipe in `tests/test_implementer_role.py` matches `F-021-A2` (avoids `TodoWrite` false positive). |
| 033-2 | **APPROVED** | | ADR-0009 accepted; map lists `implementer_agent` on author tier; `check_model_tiers` coherence is the companion gate the original sprint already ran. |

### Replay outcome (033)

**Clean**. Agrees with the original gate. No escaped defect found on this diff.

---

## Summary (do not promote from this table)

| Corpus | Replay outcome | Escaped defect? | Noise / RECORD? |
| :--- | :--- | :--- | :--- |
| 032 | Clean | No | 1× `RECORD`/`testifying` (squash scope) |
| 033 | Clean | No | No |

**Not claimed:** that `claude-opus-5` (or any family) is better than another.
Replay here exercised the **live** `cursor.gate` cell as the offline reviewer
on frozen diffs only. Gate map unchanged. Author trial **promoted** at Phase 8
Human OK 2026-08-26: `cursor.author` = `glm-5.2` / `zhipu` / `high`.
