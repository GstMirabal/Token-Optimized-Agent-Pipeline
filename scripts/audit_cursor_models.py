"""Propose Cursor model-tier assignments from the on-disk catalogue.

Reads ``~/Library/Application Support/Cursor/User/globalStorage/state.vscdb``
in **read-only** mode (stdlib ``sqlite3`` only). Zero network, zero credentials.
Proposes and never writes ``config/model_tiers.json``.

Hard filters (mechanical, no judgment):
  * ``supportsAgent is True``
  * ``degradationStatus == 0``
  * for the ``gate`` tier only: a depth lever in ``parameterDefinitions``
    (``effort``, ``thinking``, or ``reasoning``)

``family`` is derived from the model ``name`` prefix. Promotion to ``gate``
also requires proven meter history and a family distinct from ``author``'s —
Design §D7 measures that no Cursor sprint has that history yet, so **this
script never proposes a ``gate`` model**.

``--resolve`` reads ``config/model_tiers.json`` (and optionally
``agents/<profile>.md`` frontmatter) without opening the Cursor DB.

invoked_by: Makefile 'cursor-tiers' target.

Usage:
    python3 scripts/audit_cursor_models.py
    python3 scripts/audit_cursor_models.py --check
    python3 scripts/audit_cursor_models.py --resolve mechanical|author|gate|<profile>

Exit codes:
    0 — report printed; ``--check`` confirms no ``gate`` proposal;
        ``--resolve`` printed modelId/effort
    2 — ``--check`` found a ``gate`` proposal (must not happen);
        ``--resolve`` profile missing or has no ``tier:`` field
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

APPLICATION_USER_KEY = (
    "src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl"
    ".persistentStorage.applicationUser"
)
APPLIED_CONFIG_KEY = "cursor/applicationOpenModelAppliedConfig"
DEPTH_LEVERS = frozenset({"effort", "thinking", "reasoning"})
TIER_NAMES = frozenset({"mechanical", "author", "gate"})
REPO_ROOT = Path(__file__).resolve().parent.parent
MODEL_TIERS_PATH = REPO_ROOT / "config" / "model_tiers.json"
AGENTS_DIR = REPO_ROOT / "agents"

FAMILY_PREFIXES: tuple[tuple[str, str], ...] = (
    ("claude-", "anthropic"),
    ("gpt-", "openai"),
    ("gemini-", "google"),
    ("grok-", "xai"),
    ("composer-", "cursor"),
    ("kimi-", "moonshot"),
    ("glm-", "zhipu"),
    ("local-", "local"),
)


def default_vscdb_path() -> Path:
    """Cursor's global state DB on this machine (macOS path from the appendix)."""
    return (
        Path.home()
        / "Library"
        / "Application Support"
        / "Cursor"
        / "User"
        / "globalStorage"
        / "state.vscdb"
    )


def derive_family(name: str) -> str:
    """Map a catalogue ``name`` to a provider family via its prefix."""
    lowered = name.lower()
    if lowered == "default":
        return "cursor"
    for prefix, family in FAMILY_PREFIXES:
        if lowered.startswith(prefix):
            return family
    return "unknown"


def parameter_ids(model: dict[str, Any]) -> list[str]:
    """Collect ``id`` values from ``parameterDefinitions``."""
    ids: list[str] = []
    for entry in model.get("parameterDefinitions") or []:
        if isinstance(entry, dict) and entry.get("id"):
            ids.append(str(entry["id"]))
    return ids


def has_depth_lever(model: dict[str, Any]) -> bool:
    """True when the model exposes effort/thinking/reasoning."""
    return bool(DEPTH_LEVERS.intersection(parameter_ids(model)))


def open_catalogue(db_path: Path) -> list[dict[str, Any]] | None:
    """Load ``availableDefaultModels2`` or return None when the DB is absent."""
    if not db_path.is_file():
        return None
    connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        row = connection.execute(
            "SELECT value FROM ItemTable WHERE key = ?",
            (APPLICATION_USER_KEY,),
        ).fetchone()
        if row is None:
            return []
        payload = json.loads(row[0])
        models = payload.get("availableDefaultModels2") or []
        return [m for m in models if isinstance(m, dict)]
    finally:
        connection.close()


def read_applied_model_id(db_path: Path) -> str | None:
    """Return the currently applied Cursor model id, if recorded."""
    if not db_path.is_file():
        return None
    connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        row = connection.execute(
            "SELECT value FROM ItemTable WHERE key = ?",
            (APPLIED_CONFIG_KEY,),
        ).fetchone()
        if row is None:
            return None
        payload = json.loads(row[0])
        selected = payload.get("selectedModels") or []
        if not selected or not isinstance(selected[0], dict):
            return None
        model_id = selected[0].get("modelId")
        return str(model_id) if model_id else None
    finally:
        connection.close()


def load_proven_families() -> set[str]:
    """Families with proven cost-per-accepted-unit history under Cursor.

    Sprint 021's meter covers Claude Code transcripts. No Cursor ledger exists
    yet (Design §D7 cold start), so this returns empty until a Cursor meter
    lands.
    """
    return set()


def hard_filter(models: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep agent-capable, non-degraded catalogue rows."""
    kept: list[dict[str, Any]] = []
    for model in models:
        if model.get("supportsAgent") is not True:
            continue
        if model.get("degradationStatus") != 0:
            continue
        kept.append(model)
    return kept


def propose_tiers(
    models: list[dict[str, Any]],
    *,
    applied_model_id: str | None,
    proven_families: set[str],
) -> dict[str, list[dict[str, str]]]:
    """Build proposal lists. ``gate`` is always empty without proven history."""
    eligible = hard_filter(models)
    rows: list[dict[str, str]] = []
    for model in eligible:
        name = str(model.get("name") or "")
        if not name or name == "default":
            continue
        rows.append(
            {
                "name": name,
                "family": derive_family(name),
                "depth": "yes" if has_depth_lever(model) else "no",
            }
        )

    author: list[dict[str, str]] = []
    if applied_model_id:
        for row in rows:
            if row["name"] == applied_model_id:
                author = [row]
                break

    mechanical = [row for row in rows if row["depth"] == "no"][:5]

    gate: list[dict[str, str]] = []
    author_family = author[0]["family"] if author else None
    if proven_families:
        for row in rows:
            if row["depth"] != "yes":
                continue
            if row["family"] not in proven_families:
                continue
            if author_family and row["family"] == author_family:
                continue
            gate.append(row)

    return {"catalogue": rows, "author": author, "mechanical": mechanical, "gate": gate}


def print_table(title: str, rows: list[dict[str, str]]) -> None:
    """Print a markdown-style proposal table."""
    print(f"## {title}")
    if not rows:
        print("(none)")
        print()
        return
    print("| name | family | depth_lever |")
    print("| :--- | :--- | :--- |")
    for row in rows:
        print(f"| {row['name']} | {row['family']} | {row['depth']} |")
    print()


def run_report(db_path: Path) -> dict[str, list[dict[str, str]]]:
    """Load catalogue, propose tiers, print tables. Returns the proposals."""
    models = open_catalogue(db_path)
    if models is None:
        print(
            f"ℹ️  Cursor state DB not found at {db_path} — "
            "skipping catalogue audit (same doctrine as platform_probe without gh)."
        )
        return {"catalogue": [], "author": [], "mechanical": [], "gate": []}

    applied = read_applied_model_id(db_path)
    proposals = propose_tiers(
        models,
        applied_model_id=applied,
        proven_families=load_proven_families(),
    )
    print(f"Catalogue source: {db_path}")
    print(f"Models after hard filters (excl. default): {len(proposals['catalogue'])}")
    if applied:
        print(f"Applied model (author cold-start candidate): {applied}")
    print()
    print_table("Catalogue (family derived)", proposals["catalogue"])
    print_table("Proposed author (at most one; cold start)", proposals["author"])
    print_table("Proposed mechanical (no depth lever)", proposals["mechanical"])
    print_table(
        "Proposed gate (requires proven history — Design §D7: none)",
        proposals["gate"],
    )
    print(
        "Proposals only — config/model_tiers.json was not modified. "
        "gate stays null until proven history exists (not proven history)."
    )
    return proposals


def load_model_tiers(path: Path = MODEL_TIERS_PATH) -> dict[str, Any]:
    """Load ``config/model_tiers.json`` from the repository root."""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_profile_tier(stem: str, agents_dir: Path = AGENTS_DIR) -> str | None:
    """Return the ``tier:`` value from ``agents/<stem>.md`` frontmatter, or None."""
    profile_path = agents_dir / f"{stem}.md"
    if not profile_path.is_file():
        return None
    text = profile_path.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if match is None:
        return None
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("tier:"):
            value = stripped.split(":", 1)[1].strip().strip("\"'")
            return value or None
    return None


def resolve_tier_cursor(
    tier_name: str,
    tiers_payload: dict[str, Any],
) -> tuple[str, str]:
    """Return ``(model_id, effort)`` for a named tier's ``cursor`` cell.

    When ``model`` is null or missing, returns ``(\"session\", \"\")`` — never
    invents a slug.
    """
    tiers = tiers_payload.get("tiers") or {}
    tier = tiers.get(tier_name) or {}
    cursor = tier.get("cursor") or {}
    model = cursor.get("model")
    if model is None:
        return ("session", "")
    effort = cursor.get("effort")
    effort_str = "" if effort is None else str(effort)
    return (str(model), effort_str)


def print_resolve(model_id: str, effort: str) -> None:
    """Print parseable ``modelId`` / ``effort`` lines."""
    print(f"modelId={model_id}")
    print(f"effort={effort}")


def run_resolve(target: str, tiers_path: Path = MODEL_TIERS_PATH) -> int:
    """Resolve a tier name or agent profile stem to Cursor modelId/effort."""
    tiers_payload = load_model_tiers(tiers_path)
    if target in TIER_NAMES:
        model_id, effort = resolve_tier_cursor(target, tiers_payload)
        print_resolve(model_id, effort)
        return 0

    profile_path = AGENTS_DIR / f"{target}.md"
    if not profile_path.is_file():
        print(
            f"❌ --resolve: agent profile not found: agents/{target}.md",
            file=sys.stderr,
        )
        return 2
    tier_name = read_profile_tier(target)
    if tier_name is None:
        print(
            f"❌ --resolve: no tier: field in agents/{target}.md frontmatter",
            file=sys.stderr,
        )
        return 2
    if tier_name not in TIER_NAMES:
        print(
            f"❌ --resolve: unknown tier {tier_name!r} in agents/{target}.md",
            file=sys.stderr,
        )
        return 2
    model_id, effort = resolve_tier_cursor(tier_name, tiers_payload)
    print_resolve(model_id, effort)
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry: report, ``--check``, or ``--resolve`` from the tier map."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 2 if any model is proposed for the gate tier.",
    )
    parser.add_argument(
        "--resolve",
        metavar="TARGET",
        default=None,
        help=(
            "Resolve mechanical|author|gate or an agents/<stem> profile "
            "to modelId/effort from config/model_tiers.json (no Cursor DB)."
        ),
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="Override path to state.vscdb (tests / non-macOS).",
    )
    args = parser.parse_args(argv)
    if args.resolve is not None:
        return run_resolve(args.resolve)
    db_path = args.db if args.db is not None else default_vscdb_path()
    proposals = run_report(db_path)
    if args.check and proposals["gate"]:
        print("❌ --check failed: gate proposals must stay empty (Design §D7).", file=sys.stderr)
        return 2
    if args.check:
        print("✅ --check OK — no gate proposals.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
