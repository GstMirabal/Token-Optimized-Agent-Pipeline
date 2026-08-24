"""Two mechanical guards over the tier declarations, run by `make verify`.

`config/model_tiers.json` is only useful if the profiles actually agree with it,
and if nothing pins a model that a version bump will silently outdate. Neither
property is provable by reading, so both are checked.

**Guard 1 — the two fields must agree.** A profile declares `model:` (a family
alias, which the harness applies natively) and `tier:` (the intent). Declaring
only the tier was rejected during design for a reason worth restating here:
Claude Code ignores frontmatter keys it does not know, so a tier-only profile
would run on the session default — the most expensive tier — while the file
claimed otherwise. Both fields exist precisely so they can disagree, and this is
what notices when they do.

**Guard 2 — no dated model IDs.** `claude-opus-5` is a family alias and absorbs
version bumps; `claude-opus-4-1-20250805` pins one release and rots. Thirteen
profiles pinned that way would each need editing on every bump, which is the
maintenance cost the alias layer exists to remove.

invoked_by: Makefile#verify.

Usage:
    python3 scripts/check_model_tiers.py

Exit codes:
    0 — profiles and map agree, no dated IDs
    2 — a mismatch or a pinned ID (RA-11: only 2 blocks)
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root  # noqa: E402

TIERS_FILE = agents_root() / "config" / "model_tiers.json"
PROFILES = agents_root() / "agents"

FIELD = re.compile(r"^(model|tier): *(\S+) *$", re.MULTILINE)
# A family alias has no date; a pinned release ends in one. The {6,} is what
# separates `claude-opus-4-1` (a legitimate alias) from `...-20250805`.
DATED_ID = re.compile(r"claude-[a-z]+-[0-9]+(-[0-9]+)*-[0-9]{6,}")


def declared() -> dict[str, dict[str, str]]:
    """profile stem → {"model": ..., "tier": ...} as written in the frontmatter."""
    found = {}
    for path in sorted(PROFILES.glob("*.md")):
        fields = dict(
            (key, value) for key, value, *_ in
            ((m.group(1), m.group(2)) for m in FIELD.finditer(path.read_text(encoding="utf-8")))
        )
        found[path.stem] = fields
    return found


def check_agreement(tiers: dict, profiles: dict[str, dict[str, str]]) -> list[str]:
    """Every profile the map claims must declare that tier and that model."""
    problems = []
    for tier, spec in tiers.get("tiers", {}).items():
        expected = spec["claude_code"]["model"]
        for name in spec.get("profiles", []):
            fields = profiles.get(name)
            if fields is None:
                problems.append(f"{name}: named in tier `{tier}` but no such profile exists")
                continue
            if fields.get("tier") != tier:
                problems.append(f"{name}: declares tier `{fields.get('tier', '<none>')}`, "
                                f"map says `{tier}`")
            if fields.get("model") != expected:
                problems.append(f"{name}: declares model `{fields.get('model', '<none>')}`, "
                                f"tier `{tier}` maps to `{expected}`")
    mapped = {n for spec in tiers.get("tiers", {}).values() for n in spec.get("profiles", [])}
    for name, fields in profiles.items():
        if name not in mapped and (fields.get("tier") or fields.get("model")):
            problems.append(f"{name}: declares a tier/model but the map does not list it")
        if name not in mapped and not fields:
            problems.append(f"{name}: declares no tier — every profile runs on some model, "
                            f"and an undeclared one runs on the session default")
    return problems


def check_no_dated_ids() -> list[str]:
    """A pinned release in a profile or in the map is a maintenance trap."""
    problems = []
    targets = list(PROFILES.glob("*.md"))
    if TIERS_FILE.exists():
        targets.append(TIERS_FILE)
    for path in targets:
        for match in DATED_ID.finditer(path.read_text(encoding="utf-8")):
            problems.append(f"{path.name}: pins `{match.group(0)}` — use the family alias, "
                            f"which absorbs version bumps")
    return problems


def main() -> int:
    """Verify the tier declarations against their map."""
    if not TIERS_FILE.exists():
        print(f"ℹ️  {TIERS_FILE.name} does not exist; nothing to check.")
        return 0

    tiers = json.loads(TIERS_FILE.read_text(encoding="utf-8"))
    problems = check_agreement(tiers, declared()) + check_no_dated_ids()

    if problems:
        print(f"\n❌ {len(problems)} tier declaration problem(s):", file=sys.stderr)
        for problem in problems:
            print(f"   • {problem}", file=sys.stderr)
        print("\n   A profile whose `tier:` and `model:` disagree with the map is not a "
              "typo: the harness reads `model:` and ignores `tier:`, so the file would "
              "claim one thing and the subagent do another.", file=sys.stderr)
        return 2

    counted = sum(len(s.get("profiles", [])) for s in tiers.get("tiers", {}).values())
    print(f"✅ Model tiers OK — {counted} profile(s) agree with the map, no pinned IDs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
