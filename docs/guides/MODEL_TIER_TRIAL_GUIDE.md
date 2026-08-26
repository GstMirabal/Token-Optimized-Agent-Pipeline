# How-to: Run a model-tier trial

**File**: `docs/guides/MODEL_TIER_TRIAL_GUIDE.md` (RA-06 Option B naming)
**Module**: model-tiers

---

## 1. Goal

Adopt or reject a cheaper `author`-tier model for one release cycle using gate
round evidence — never by announcement alone. After Sprint 037 creates the
derived ledger, that evidence base is `make model-ledger` /
`docs/audits/MODEL_LEDGER.md`, not prose in chat.

## 2. Prerequisites

- `config/model_tiers.json` and `scripts/detect_new_models.py` are current
  (`make verify` includes `--check`).
- ADR-0003: `qa_agent`, `tester_agent`, and `principal_agent` stay at the
  `gate` tier — a trial must not move them.
- ADR-0004: no model-selector agent; defaults stay in the static map.
- **Ledger (from Sprint 037 onward):** `scripts/model_ledger.py` exists and
  `make model-ledger` regenerates `docs/audits/MODEL_LEDGER.md` from gate
  rounds in `SPRINT_LOG.md` joined with Model/Effort in `task_scope.md`. This
  guide documents how to **use** that file once it exists; Sprint 037 owns
  creating the generator. Do not invent ledger rows by hand.

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
5. After close, regenerate the ledger (`make model-ledger`) when the Sprint 037
   tool exists, then compare ledger rows (gate rounds and verdict classes)
   against the previous release. Promote the candidate into
   `config/model_tiers.json` only with explicit Human OK and ledger (or
   pre-037 SPRINT_LOG) evidence; otherwise revert the trial map and leave the
   alias as candidate.

**If Cursor `session_tool`:** use `make cursor-tiers` as the binding catalogue;
do not copy `claude_code` aliases into `task_scope.md`.

**First trial (declared in Sprint 030, destaged in 031):** Sprint **032**.
Candidate: Cursor **`grok-4.5`** / effort **`high`** (prior map: `grok-4.6` /
`high`). Mixing verdict classes and a cheaper `author` in 031 would prevent
attributing gate rounds to either change. Sprint 030 shipped this guide; 031
retargets it.

**Second trial — family (Sprint 038):** Cursor **`glm-5.2`** / family **`zhipu`**
/ effort **`high`** (incumbent map: `grok-4.5` / `xai` / `high`). One variable:
author **family**, not generation and not effort. Do **not** set `cursor.author`
to `claude-opus-5` while `cursor.gate` is anthropic (`D15` family diversity).
Gate-replay (D16) executes in the same sprint; record findings in
`docs/sprints/038-core-pipeline/GATE_REPLAY.md` — a clean replay does not prove
superiority and must not rank families.

**Abort (chat vs global medidor).** `make cursor-tiers` reads only
`applicationOpenModelAppliedConfig`. A per-chat override to the trial slug may
leave that key on another model. Sprint 032 option B (also 038 Q4): record human
attestation in `SPRINT_LOG.md` and proceed; do not treat a stale global key alone
as abort. Abort if the human withdraws the attestation or gate quality collapses
(restore prior `author` map — for 038 that is `grok-4.5` / `xai` / `high`).

## 4. Ledger as promotion evidence

| Question | Answer |
| :--- | :--- |
| What is the ledger? | Derived markdown at `docs/audits/MODEL_LEDGER.md` — one row per sprint with gate rounds and Model/Effort from `task_scope.md` |
| How is it produced? | `make model-ledger` (Sprint **037** implements the script; earlier sprints have no usable file) |
| What may it support? | Promoting a cheaper `author` candidate after a trial sprint, with Human OK |
| What must it not replace? | Announcement, marketing names, or a public benchmark score |

Until 037 ships, fall back to the Double-Gate tables in each trial sprint's
`SPRINT_LOG.md` (same raw evidence the ledger will join). Do not claim any
model family is better than another from ledger rows alone.

## 5. Gate-replay protocol (D16)

Protocol authored in Sprint 035 (E0). **Execution** is Sprint **038**
(`docs/sprints/038-core-pipeline/GATE_REPLAY.md`) after the first ledger row
exists (037). Do not re-run gate-replay inside sprints 034–037.

| Aspect | Rule |
| :--- | :--- |
| **Purpose** | Offline second pass of a gate candidate over a **historical closed sprint diff** without touching `main` |
| **Preferred corpus** | Sprints **032** and **033** (both APPROVED on Double-Gate round 1) |
| **Selection** | Pick a closed sprint whose `SPRINT_LOG.md` has a Double-Gate table; the diff is that sprint's merge range versus its base branch |
| **Recording** | Log every finding with ADR-0008 vocabulary: verdict `APPROVED` \| `REJECTED` \| `RECORD`, plus class `charter` \| `instructing` \| `testifying` |
| **Ownership** | Protocol text lives here (E0 / Sprint 035); **execution** is Sprint 038 (`GATE_REPLAY.md`) |

### 5.1 Classification of replay outcomes (informative only)

| Replay outcome | Reading |
| :--- | :--- |
| **Defect escaped** | Real defect the original gate approved — hard signal of an escaped defect |
| **Clean** | Nothing found; agrees with the original gate. Neither proves nor refutes superiority; only shows the candidate is not alarmist on that diff |
| **Noise** | Findings that are not defects — measurable reviewer noise |

A clean replay does **not** prove the candidate is better than the incumbent.
Do not rank families from replay results.

## 6. Verify it worked

```bash
python3 scripts/detect_new_models.py --check; echo $?
grep -n "Gate .* round" docs/sprints/[ID]-*/SPRINT_LOG.md
# After Sprint 037:
make model-ledger; test -f docs/audits/MODEL_LEDGER.md && echo LEDGER_OK
```

Expected: exit `0` from `--check` (no retired tier models); SPRINT_LOG carries
round outcomes for the trial sprint; after 037, `MODEL_LEDGER.md` exists and
lists the trial sprint row used for the promotion decision.

## 7. If something goes wrong

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Gate quality collapses | Author tier too cheap for the work | Abort trial; restore prior `author` map; keep gates at `gate` |
| Cursor rows show `haiku`/`sonnet` | Copied Claude aliases | Re-run `make cursor-tiers`; re-transcribe |
| Trial mid-sprint | Cadence broken | Finish or suspend; trial starts on next sprint only |
| `make cursor-tiers` still shows prior author while chat is on candidate | Per-chat override not written to global applied config | Attest in `SPRINT_LOG` (032 option B) or set the agent **default** so the medidor matches |
| Promote from announcement / no ledger row | Skipping evidence base | After 037: regenerate ledger; refuse promotion without a trial row + Human OK |
| Gate-replay started in 034–037 | Wrong sprint ownership | Stop; wait for Sprint 038 after first ledger row |
| Gate-replay used to rank families | Violates D7 / D13 | Record findings only; never promote gate from replay alone |
| Author trial sets Opus while gate is anthropic | Violates D15 | Use a non-anthropic author slug (038: `glm-5.2`) |

---
*See also: `docs/decisions/ADR-0003-gates-never-drop-tier.md` ·
`docs/decisions/ADR-0004-no-model-selector-agent.md` ·
`docs/decisions/ADR-0008-gate-verdict-classes.md` ·
`config/model_tiers.json`.*
