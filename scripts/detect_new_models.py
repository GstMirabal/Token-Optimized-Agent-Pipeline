"""Notice a new, deprecated or retired model without asking the network.

`config/model_tiers.json` maps a role tier to a model family. A map is only as
good as its knowledge of what exists, and the obvious ways to keep it current all
fail here: copying a price table makes it stale the day it is written, and a
poller would need a dependency (`rules/code_craft.md §7`) plus credentials for a
check that matters a few times a year.

**There is an authoritative catalogue already on disk.** The `claude-api` skill
Claude Code bundles ships `shared/models.md` with alias, full ID, context window,
max output and **status** — `Active` / `Legacy` / `Deprecated` / `Retired`. Its
path encodes the CLI version, so the catalogue refreshes exactly when the tool
updates: nothing has to be polled, because the trigger is the tool's own update
cycle.

**Parsed structurally, because the obvious readings both fail.** The file holds
several tables with different column counts — the main one has six, others four
or five — so an index-based read of the status breaks. And it holds a *phrasing*
table whose rows embed an alias inside prose:

    | "sonnet 3.7" | Retired — suggest `claude-sonnet-5` |

so scanning a whole row for any status word attributes Sonnet 3.7's retirement to
Sonnet 5. A first version of this parser did exactly that and recorded
`claude-sonnet-5` as Retired, which with the severity ladder wired would have
failed the build over a perfectly healthy tier.

The discriminator is therefore structural: a catalogue row has the alias **alone
in its second cell**, and its status in the **last** cell. The retirement date
rides in that same cell, which is what lets the Deprecated rung carry a clock.

**The gate reads the committed snapshot, not this file.** The bundled catalogue
lives in a per-user temp directory the system clears and CI never has, so a gate
reading it directly would silently never fire there — a mechanism wired where it
cannot run (`RA-16`). `catalog_snapshot` in `config/model_tiers.json` is the
durable copy and the gate's only source; reading the bundled file is the
opportunistic half that proposes refreshing it.

**Severity is a ladder, not a switch**, and that is the whole point:

- a **new alias** is a candidate for the evidence protocol, not a change: nothing
  is adopted for existing, so this proposes.
- a tier's model turning **Deprecated** proposes *with its retirement date* —
  there is room, but the clock is running.
- a tier's model turning **Retired** **fails the build**. That is not a judgment
  call: a retired model returns 404, so the failure is deterministic and total.

Propose what needs judgment, block what is a guaranteed failure.

**What this does NOT detect: prices.** They are not on disk, only in the skill's
rendered prompt. Declared here rather than faked; `config/model_tiers.json`
carries `verified_at` so the gap is visible and ages loudly.

invoked_by: scripts/session_probe.py, Makefile#verify.

Usage:
    python3 scripts/detect_new_models.py            # report
    python3 scripts/detect_new_models.py --check    # exit 2 if a tier is retired

Exit codes:
    0 — nothing retired (new or deprecated models are reported, not blocked)
    2 — a tier names a retired model: the build must fail (RA-11)
"""

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _mode import agents_dir  # noqa: E402

TIERS_FILE = agents_dir() / "config" / "model_tiers.json"

# The alias cell of a catalogue row holds the alias and NOTHING else. That is the
# discriminator, and it is structural rather than a denylist: the file also has a
# phrasing table whose rows embed an alias inside prose —
#   | "sonnet 3.7" | Retired — suggest `claude-sonnet-5` |
# — which describes Sonnet 3.7's status, not Sonnet 5's. A first version of this
# parser scanned the whole row and recorded `claude-sonnet-5` as Retired, which
# with the severity ladder wired would have failed the build over a healthy tier.
ALIAS_CELL = re.compile(r"^`(claude-[a-z0-9.-]+)`$")
STATUS = re.compile(r"\b(Active|Legacy|Deprecated|Retired)\b")
RETIRES = re.compile(r"retires (\d{4}-\d{2}-\d{2})")


def catalogue_path() -> Path | None:
    """The bundled `models.md` from the newest CLI version present.

    Returns None when Claude Code is not installed here — a host on another tool
    is not a finding, and saying so beats guessing at a catalogue.
    """
    for root in _bundled_roots():
        found = sorted(root.glob("*/*/claude-api/shared/models.md"))
        if found:
            return found[-1]
    return None


def _bundled_roots() -> list[Path]:
    """Where Claude Code may have extracted its bundled skills, per platform.

    Derived rather than hardcoded: macOS resolves the system temp directory to
    `/private/tmp` while `/tmp` is a symlink to it, and Linux uses `/tmp`
    directly. Pinning either one makes this work on one platform and silently
    find nothing on the other — and finding nothing is indistinguishable from a
    clean catalogue unless it is stated.
    """
    uid = os.getuid()
    seen, roots = set(), []
    for base in (Path(tempfile.gettempdir()), Path("/tmp"), Path("/private/tmp")):
        candidate = base / f"claude-{uid}" / "bundled-skills"
        resolved = candidate.resolve()
        if resolved not in seen and candidate.is_dir():
            seen.add(resolved)
            roots.append(candidate)
    return roots


def parse_catalogue(path: Path) -> dict[str, dict]:
    """Alias → {status, retires} for every model row in the catalogue.

    A catalogue row is identified by its **second cell being nothing but a
    backticked alias**, and its status read from the **last** cell. Both halves
    matter: the tables do not share a column count, so an index-based read of the
    status fails, and the file's phrasing table embeds aliases inside prose, so
    scanning the whole row attributes one model's retirement to another.

    Args:
        path: the bundled `models.md`.

    Returns:
        dict: alias → {"status": str, "retires": str | None}.
    """
    models: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        alias = ALIAS_CELL.match(cells[1])
        if not alias:
            continue
        status = STATUS.search(cells[-1])
        if not status:
            continue
        retires = RETIRES.search(cells[-1])
        models[alias.group(1)] = {
            "status": status.group(1),
            "retires": retires.group(1) if retires else None,
        }
    return models


def load_tiers() -> dict:
    """The tier map, or {} when it does not exist yet."""
    if not TIERS_FILE.exists():
        return {}
    return json.loads(TIERS_FILE.read_text(encoding="utf-8"))


def tier_models(tiers: dict) -> dict[str, str]:
    """tier → the Claude Code family alias it resolves to."""
    return {name: spec["claude_code"]["model"]
            for name, spec in tiers.get("tiers", {}).items()}


def resolve(family: str, catalogue: dict[str, dict]) -> tuple[str, dict] | None:
    """The newest catalogue entry a family alias stands for.

    Profiles declare `opus`, never `claude-opus-5`: the alias absorbs version
    bumps without touching thirteen files. So a family is matched against every
    catalogue alias that starts with it, and the newest wins.
    """
    matches = {a: m for a, m in catalogue.items() if a.startswith(f"claude-{family}")}
    if not matches:
        return None
    newest = sorted(matches)[-1]
    return newest, matches[newest]


def snapshot_catalogue(tiers: dict) -> dict[str, dict]:
    """The committed snapshot, in the same shape the bundled parser returns.

    **This is what the gate reads.** The bundled catalogue is not available in CI
    or after a temp sweep, so a gate reading it directly would pass silently
    wherever it matters most — a mechanism wired where it cannot run (`RA-16`).
    """
    aliases = tiers.get("catalog_snapshot", {}).get("aliases", {})
    return {alias: {"status": status, "retires": None} for alias, status in aliases.items()}


def tier_status(tiers: dict, catalogue: dict[str, dict]) -> tuple[list[str], list[str]]:
    """Which tiers name a retired or deprecated model, per the given catalogue.

    Returns:
        tuple: (retired — blocking, deprecated — proposed with a date when known).
    """
    retired, deprecated = [], []
    for tier, family in tier_models(tiers).items():
        found = resolve(family, catalogue)
        if not found:
            continue
        alias, entry = found
        if entry["status"] == "Retired":
            retired.append(f"tier `{tier}` resolves to {alias}, which is RETIRED "
                           f"— a retired model returns 404")
        elif entry["status"] == "Deprecated":
            when = f", retires {entry['retires']}" if entry["retires"] else ""
            deprecated.append(f"tier `{tier}` resolves to {alias}, now Deprecated{when}")
    return retired, deprecated


def refresh_findings(tiers: dict, bundled: dict[str, dict]) -> tuple[list[str], list[str]]:
    """What the bundled catalogue knows that the committed snapshot does not.

    The opportunistic half: only runs when the bundled file is present, and only
    ever proposes. Adopting a model for existing is what the evidence protocol
    exists to prevent.

    Returns:
        tuple: (new Active aliases, status transitions since the snapshot).
    """
    snapshot = tiers.get("catalog_snapshot", {}).get("aliases", {})
    fresh = [a for a, m in sorted(bundled.items())
             if a not in snapshot and m["status"] == "Active"]
    moved = [f"{a}: {snapshot[a]} → {m['status']}"
             for a, m in sorted(bundled.items())
             if a in snapshot and snapshot[a] != m["status"]]
    return fresh, moved


def main() -> int:
    """Report catalogue drift; fail the build only for a retired tier model."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true",
                        help="Exit 2 when a tier names a retired model.")
    args = parser.parse_args()

    tiers = load_tiers()
    if not tiers:
        print(f"ℹ️  {TIERS_FILE.name} does not exist yet; nothing to check.")
        return 0

    # The gate reads the committed snapshot, so it returns the same verdict on a
    # laptop and in CI. Reading the bundled file here instead would make --check
    # a no-op exactly where nobody is watching.
    retired, deprecated = tier_status(tiers, snapshot_catalogue(tiers))
    for note in deprecated:
        print(f"⏳ {note}. There is room, but the clock is running: plan the migration.")

    # The refresh is opportunistic: the bundled catalogue lives in a temp
    # directory that CI never has and the system periodically clears.
    path = catalogue_path()
    if path is None:
        print("ℹ️  No bundled catalogue on this machine — the snapshot cannot be "
              "refreshed here. Saying so rather than implying the map was checked "
              "against anything newer.")
    else:
        fresh, moved = refresh_findings(tiers, parse_catalogue(path))
        if fresh:
            print(f"🆕 {len(fresh)} model(s) absent from the snapshot: {', '.join(fresh)}")
            print("   Proposed as candidates, not adopted — a model is not taken up "
                  "for existing. Refresh `catalog_snapshot` to record them.")
        for note in moved:
            print(f"🔄 status moved since the snapshot — {note}")
        if not (fresh or moved or retired or deprecated):
            print("✅ Tier map matches the bundled catalogue; nothing retired, "
                  "deprecated or new.")

    if retired:
        for note in retired:
            print(f"\n❌ {note}.", file=sys.stderr)
        print("\n   This blocks rather than proposes, because it is not a judgment "
              "call: the failure is deterministic. Update `config/model_tiers.json`.",
              file=sys.stderr)
        return 2 if args.check else 0

    print(f"\n   Prices are NOT checked — they are not on disk. "
          f"`verified_at`: {tiers.get('verified_at', 'unset')}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
