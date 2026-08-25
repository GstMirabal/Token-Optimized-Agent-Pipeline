# How-to: Run a model-tier trial

**File**: `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` (RA-06 Option B naming)
**Module**: model-tiers

---

## 1. Goal

Adopt or reject a cheaper `author`-tier model for one release cycle using gate
round evidence — never by announcement alone.

## 2. Prerequisites

- `config/model_tiers.json` and `scripts/detect_new_models.py` are current
  (`make verify` includes `--check`).
- ADR-0003: `qa_agent`, `tester_agent`, and `principal_agent` stay at the
  `gate` tier — a trial must not move them.
- ADR-0004: no model-selector agent; defaults stay in the static map.

## 3. Steps

1. Treat a new catalogue alias from `detect_new_models.py` as a **candidate**,
   not a change. Record it in the sprint Implementation Plan Cost / Design
   section with the command that listed it.
2. Schedule at most **one** trial per release cycle. Never start a trial
   mid-sprint on an open `ai-sprint/[ID]` branch.
3. For the trial sprint only, set `author`-tier profiles one step cheaper than
   the current map (Claude Code: e.g. `sonnet` → `haiku` where the map allows;
   Cursor: the next cheaper `modelId` from `make cursor-tiers`). Leave
   `gate` and `mechanical` unchanged unless a separate ADR says otherwise.
4. Run the full pipeline. In `SPRINT_LOG.md`, record every Double-Gate round
   (`Gate N, round R — REJECTED|APPROVED`). That variation is the evidence.
5. After close, compare gate rounds and defect classes against the previous
   release. Promote the candidate into `config/model_tiers.json` only with
   explicit Human OK; otherwise revert the trial map and leave the alias as
   candidate.

**If Cursor `session_tool`:** use `make cursor-tiers` as the binding catalogue;
do not copy `claude_code` aliases into `task_scope.md`.

**First trial (declared in Sprint 030, destaged in 031):** Sprint **032**.
Candidate: Cursor **`grok-4.5`** / effort **`high`** (prior map: `grok-4.6` /
`high`). Mixing verdict classes and a cheaper `author` in 031 would prevent
attributing gate rounds to either change. Sprint 030 shipped this guide; 031
retargets it.

**Abort (chat vs global medidor).** `make cursor-tiers` reads only
`applicationOpenModelAppliedConfig`. A per-chat override to Cursor Grok 4.5 may
leave that key on `grok-4.6`. Sprint 032 option B: record human attestation in
`SPRINT_LOG.md` and proceed; do not treat a stale global key alone as abort.
Abort if the human withdraws the attestation or gate quality collapses
(restore prior `author` map).

## 4. Verify it worked

```bash
python3 scripts/detect_new_models.py --check; echo $?
grep -n "Gate .* round" docs/sprints/[ID]-*/SPRINT_LOG.md
```

Expected: exit `0` from `--check` (no retired tier models); SPRINT_LOG carries
round outcomes for the trial sprint.

## 5. If something goes wrong

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Gate quality collapses | Author tier too cheap for the work | Abort trial; restore prior `author` map; keep gates at `gate` |
| Cursor rows show `haiku`/`sonnet` | Copied Claude aliases | Re-run `make cursor-tiers`; re-transcribe |
| Trial mid-sprint | Cadence broken | Finish or suspend; trial starts on next sprint only |
| `make cursor-tiers` still shows prior author while chat is on candidate | Per-chat override not written to global applied config | Attest in `SPRINT_LOG` (032 option B) or set the agent **default** so the medidor matches |

---
*See also: `docs/decisions/ADR-0003-gates-never-drop-tier.md` ·
`docs/decisions/ADR-0004-no-model-selector-agent.md` ·
`config/model_tiers.json`.*
