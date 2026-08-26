"""Propose Cursor model-tier assignments from the on-disk catalogue.

Reads ``~/Library/Application Support/Cursor/User/globalStorage/state.vscdb``
in **read-only** mode (stdlib ``sqlite3`` only). Zero network, zero credentials.
Proposes and never writes ``config/model_tiers.json``.

Hard filters (mechanical, no judgment):
  * ``supportsAgent is True``
  * ``degradationStatus == 0``
  * for the ``gate`` tier only: a depth lever in ``parameterDefinitions``
    (``effort``, ``thinking``, or ``reasoning``)

``family`` is derived from the model ``name`` prefix. The **author** proposal
is the current ``config/model_tiers.json`` → ``tiers.author.cursor`` map cell
(mirrored from the filtered catalogue when present, else a synthetic row from
the map). The Cursor ``applicationOpenModelAppliedConfig`` model is reported
separately as agreement or discrepancy — it is never treated as the proposal.

``gate`` proposals use the structural ceiling (D13): depth lever present and
``family`` distinct from the **map** author cell's family. Among eligible
families, prefer the family of ``tiers.gate.claude_code``, else larger
``contextTokenLimit``. Proven meter history is not required to *propose* or
*fix* the ceiling — only to *cheapen* later (see ``load_proven_families``).

``--resolve`` reads ``config/model_tiers.json`` (and optionally
``agents/<profile>.md`` frontmatter) without opening the Cursor DB.

invoked_by: Makefile 'cursor-tiers' target.

Usage:
    python3 scripts/audit_cursor_models.py
    python3 scripts/audit_cursor_models.py --check
    python3 scripts/audit_cursor_models.py --resolve mechanical|author|gate|<profile>

Exit codes:
    0 — report printed; ``--check`` confirms ≥1 ``gate`` proposal;
        ``--resolve`` printed modelId/effort
    2 — ``--check``: ``gate`` empty or catalogue unavailable;
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
    """Stub reserved for future *cheapening* of the gate cell.

    Structural ceiling proposals (D13) do **not** call this. A Cursor
    cost-per-accepted-unit ledger would populate this set so a later sprint
    can narrow an already-fixed ceiling toward a cheaper family — never to
    decide whether a gate proposal may exist.
    """
    return set()


def family_from_claude_code_alias(model: str) -> str:
    """Map a Claude Code tier alias (``opus`` / ``sonnet`` / ``haiku``) to family."""
    lowered = model.lower()
    if lowered in {"opus", "sonnet", "haiku"} or lowered.startswith("claude-"):
        return "anthropic"
    return derive_family(model)


def context_token_limit(model: dict[str, Any]) -> int:
    """Best-effort context window from a catalogue row (0 when unknown)."""
    for key in ("contextTokenLimit", "contextTokenLimitForMaxMode"):
        value = model.get(key)
        if isinstance(value, (int, float)) and value > 0:
            return int(value)
    return 0


def read_map_author_cursor(
    tiers_path: Path = MODEL_TIERS_PATH,
) -> tuple[str | None, str | None]:
    """Return ``(model, family)`` from ``tiers.author.cursor`` in the tier map.

    Args:
        tiers_path: Path to ``config/model_tiers.json``.

    Returns:
        Model id and family strings, or ``(None, None)`` when the cell is empty.
    """
    payload = load_model_tiers(tiers_path)
    cursor = ((payload.get("tiers") or {}).get("author") or {}).get("cursor") or {}
    model = cursor.get("model")
    family = cursor.get("family")
    model_str = str(model) if model else None
    family_str = str(family) if family else None
    if model_str and not family_str:
        family_str = derive_family(model_str)
    return (model_str, family_str)


def read_map_gate_claude_family(
    tiers_path: Path = MODEL_TIERS_PATH,
) -> str | None:
    """Return the provider family of ``tiers.gate.claude_code.model``, if set."""
    payload = load_model_tiers(tiers_path)
    model = (
        ((payload.get("tiers") or {}).get("gate") or {}).get("claude_code") or {}
    ).get("model")
    if not model:
        return None
    return family_from_claude_code_alias(str(model))


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


def catalogue_rows(
    models: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], list[tuple[dict[str, str], int]]]:
    """Hard-filter catalogue into display rows and depth-lever (row, tokens) pairs."""
    rows: list[dict[str, str]] = []
    depth_models: list[tuple[dict[str, str], int]] = []
    for model in hard_filter(models):
        name = str(model.get("name") or "")
        if not name or name == "default":
            continue
        row = {
            "name": name,
            "family": derive_family(name),
            "depth": "yes" if has_depth_lever(model) else "no",
        }
        rows.append(row)
        if row["depth"] == "yes":
            depth_models.append((row, context_token_limit(model)))
    return rows, depth_models


def author_proposal_rows(
    rows: list[dict[str, str]],
    map_author_model: str | None,
    map_author_family: str | None,
) -> list[dict[str, str]]:
    """Mirror the map author cell into at most one proposal row."""
    if not map_author_model:
        return []
    for row in rows:
        if row["name"] == map_author_model:
            return [row]
    family = map_author_family or derive_family(map_author_model)
    return [{"name": map_author_model, "family": family, "depth": "unknown"}]


def map_author_family_for_diversity(
    map_author_model: str | None,
    map_author_family: str | None,
    author: list[dict[str, str]],
) -> str | None:
    """Author family for the gate diversity rule (map cell, not applied model)."""
    if map_author_family:
        return map_author_family
    if map_author_model:
        return derive_family(map_author_model)
    if author:
        return author[0]["family"]
    return None


def select_gate_rows(
    depth_models: list[tuple[dict[str, str], int]],
    *,
    author_family: str | None,
    preferred_gate_family: str | None,
) -> list[dict[str, str]]:
    """Pick gate proposal rows: depth + family diversity + D13 tie-break."""
    gate_candidates = [
        (row, tokens)
        for row, tokens in depth_models
        if not author_family or row["family"] != author_family
    ]
    if preferred_gate_family:
        preferred = [
            (row, tokens)
            for row, tokens in gate_candidates
            if row["family"] == preferred_gate_family
        ]
        if preferred:
            gate_candidates = preferred
    gate_candidates.sort(key=lambda item: (-item[1], item[0]["name"]))
    return [row for row, _tokens in gate_candidates]


def propose_tiers(
    models: list[dict[str, Any]],
    *,
    applied_model_id: str | None,
    proven_families: set[str] | None = None,
    map_author_model: str | None = None,
    map_author_family: str | None = None,
    preferred_gate_family: str | None = None,
) -> dict[str, list[dict[str, str]]]:
    """Build proposal lists. Author is the map cell; gate is structural (D13).

    ``applied_model_id`` is accepted for callers that still pass it (report /
    discrepancy lives in ``run_report``); it does not become the author proposal.
    ``proven_families`` is accepted for call-site compatibility but ignored —
    gate eligibility does not depend on proven history (reserved for cheapening).
    """
    del applied_model_id  # discrepancy is reported by run_report, not here
    del proven_families  # structural gate path; stub retained for cheapening API
    if map_author_model is None:
        map_author_model, map_author_family = read_map_author_cursor()
    if preferred_gate_family is None:
        preferred_gate_family = read_map_gate_claude_family()

    rows, depth_models = catalogue_rows(models)
    author = author_proposal_rows(rows, map_author_model, map_author_family)
    mechanical = [row for row in rows if row["depth"] == "no"][:5]
    author_family = map_author_family_for_diversity(
        map_author_model, map_author_family, author
    )
    gate = select_gate_rows(
        depth_models,
        author_family=author_family,
        preferred_gate_family=preferred_gate_family,
    )
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
    map_author_model, map_author_family = read_map_author_cursor()
    preferred_gate_family = read_map_gate_claude_family()
    proposals = propose_tiers(
        models,
        applied_model_id=applied,
        map_author_model=map_author_model,
        map_author_family=map_author_family,
        preferred_gate_family=preferred_gate_family,
    )
    print(f"Catalogue source: {db_path}")
    print(f"Models after hard filters (excl. default): {len(proposals['catalogue'])}")
    proposed_author = proposals["author"][0]["name"] if proposals["author"] else None
    if map_author_model:
        print(f"Map author cell: {map_author_model}")
    if applied:
        if proposed_author and applied == proposed_author:
            print(f"Applied model: {applied} (agrees with map author)")
        else:
            map_label = proposed_author or "(no map author)"
            print(
                f"Applied model (discrepancy): {applied} "
                f"— differs from map author {map_label}"
            )
    elif proposed_author:
        print(f"No applied model recorded (map author proposal: {proposed_author})")
    print()
    print_table("Catalogue (family derived)", proposals["catalogue"])
    print_table("Proposed author (map cell; at most one)", proposals["author"])
    print_table("Proposed mechanical (no depth lever)", proposals["mechanical"])
    print_table(
        "Proposed gate (structural ceiling; family ≠ map author)",
        proposals["gate"],
    )
    print(
        "Proposals only — config/model_tiers.json was not modified. "
        "Gate cell is filled separately by ADR-0011 / H2."
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
        help=(
            "Exit 2 when gate proposals are empty or the catalogue is "
            "unavailable; exit 0 when ≥1 gate row is proposed."
        ),
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
    if args.check and not proposals["gate"]:
        print(
            "❌ --check failed: gate proposals empty "
            "(catalogue unavailable or no eligible structural candidates).",
            file=sys.stderr,
        )
        return 2
    if args.check:
        print("✅ --check OK — gate proposals present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
