"""Generate the workflow step map and the artifact x workflow matrix.

A hand-maintained map of eleven protocols drifts at the first edit — the exact
failure this phase exists to repair — so it is generated and then verified by
regenerating and comparing (`make verify`). A stale map fails the build instead
of lying quietly.

Three table shapes exist in `workflows/` (`Phase | Step | Action`,
`Phase | Action | Gate`, `Phase | Item | When`), and the ad-hoc extractor used
while planning this phase silently produced nothing for two of them. That is
why the parser is shape-tolerant. A step whose verb the heuristic recognises is
labelled `read`, `write` or `verify`; one it cannot is labelled `ambiguous`
(a real step id) or `prose` (a `**Bold sentence.**` with no verb-plus-object)
rather than guessed — a script that feigns certainty about prose is the PR #28
defect wearing different clothes. A table immediately preceded by a line reading
`<!-- map_workflows:skip-table -->` is a reference table, not a step list, and
is excluded from the map entirely.

The matrix columns come from `config/artifact_registry.json` (Sprint 023
`C0.2`). They were a fixed table of six state artifacts and zero documentary
ones, matched against workflow prose by literal filename — so a deliverable a
protocol described in words instead of naming was invisible to this map by
construction, and the producer of `task_scope.md` registered as its consumer.

invoked_by: Makefile `verify` target (regenerate-and-compare).

Usage:
    python3 scripts/map_workflows.py            # write the guide
    python3 scripts/map_workflows.py --check    # fail if the guide is stale

Exit codes:
    0 — guide written, or already current under --check
    1 — under --check, the guide on disk differs from the generated one
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root

WORKFLOWS = Path("workflows")
OUTPUT = Path("docs/guides/WORKFLOWS_STEP_MAP_GUIDE.md")
# Absolute even though `main()` sets the cwd, because `ARTIFACTS` below is
# evaluated at import — before any entry point runs.
ARTIFACT_REGISTRY = agents_root() / "config" / "artifact_registry.json"


def load_artifacts(registry: Path = ARTIFACT_REGISTRY) -> dict[str, str]:
    """Artifact filename -> the phase that produces it, for the matrix columns.

    The columns used to be a fixed table of six state artifacts and zero
    documentary ones, so a protocol's real deliverables — the plan, the sprint
    log, the two assignment records — were invisible to the map by construction.
    They come from `config/artifact_registry.json` now, which is the same list
    the freshness gate and the close gate read.

    Args:
        registry (Path): Path to `config/artifact_registry.json`.

    Returns:
        dict[str, str]: filename -> producing phase, in registry order.

    Raises:
        FileNotFoundError: The registry is absent. Deliberately fatal: a matrix
            silently built with no columns would read as "no workflow touches
            any artifact", which is a false green rather than a missing file.
    """
    data = json.loads(registry.read_text(encoding="utf-8"))
    return {entry["filename"]: entry["phase"] for entry in data["artifacts"]}


ARTIFACTS = load_artifacts()

WRITE_VERBS = ("update", "write", "append", "create", "instantiate", "record",
               "generate", "stamp", "persist", "refresh", "sync", "delete",
               "purge", "rename", "commit", "claim", "release")
READ_VERBS = ("read", "extract", "load", "query", "consult", "parse")
CHECK_VERBS = ("verify", "check", "audit", "validate", "ensure", "confirm",
               "abort", "reject", "scan", "gate")

ROW = re.compile(r"^\|\s*(\*\*)?([^|]+?)(\*\*)?\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")

# A line equal to this (after stripping) immediately before a table removes that
# whole table from step parsing — for reference tables such as
# `standardization_workflow.md`'s Legacy Routing Table (`S045-27`).
SKIP_MARKER = "<!-- map_workflows:skip-table -->"


def classify(action: str) -> str:
    """read / write / verify, from the action's own verb.

    First match wins by precedence: a step that writes is recorded as a writer
    even when it also reads, because the map exists to expose who writes.
    """
    lowered = action.lower()
    for verbs, label in ((WRITE_VERBS, "write"), (CHECK_VERBS, "verify"), (READ_VERBS, "read")):
        if any(re.search(rf"\b{verb}", lowered) for verb in verbs):
            return label
    return "?"


def _is_prose(step_cell: str) -> bool:
    """Whether a step cell reads as a bold sentence rather than a step id.

    A real step cell is a lone code span (`` `state_claim` ``) or a short bold
    label (`**Option B**`). Prose is a `**Bold sentence.**`, optionally preceded
    by an HTML anchor and trailed by further sentence text.

    Args:
        step_cell (str): The raw second column of a table row.

    Returns:
        bool: True when the cell is prose, False when it is a step identifier.
    """
    text = re.sub(r"<[^>]+>", "", step_cell).strip()
    if re.fullmatch(r"`[^`]+`", text) or re.fullmatch(r"\*\*[^*.]+\*\*", text):
        return False
    return "**" in text


def _effect(step_cell: str, action: str) -> str:
    """The Section 2 effect label for one step row.

    Args:
        step_cell (str): The raw second column, used to tell prose from a step id.
        action (str): The effect/gate column handed to `classify`.

    Returns:
        str: `read` / `write` / `verify` when the verb is recognised; otherwise
        `prose` for a bold sentence or `ambiguous` for an unrecognised verb.
    """
    verdict = classify(action)
    if verdict != "?":
        return verdict
    return "prose" if _is_prose(step_cell) else "ambiguous"


def _is_separator_row(line: str) -> bool:
    """True for a Markdown header underline such as `| :--- | :--- |`."""
    stripped = line.strip()
    return bool(stripped) and set(stripped) <= set("|:- ")


def _take_table_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """Collect the run of consecutive table rows beginning at `start`.

    Args:
        lines (list[str]): The file's lines.
        start (int): Index of the first table-row line.

    Returns:
        tuple[list[str], int]: The block's lines and the index just past it.
    """
    index = start
    while index < len(lines) and ROW.match(lines[index]):
        index += 1
    return lines[start:index], index


def _group_tables(lines: list[str]) -> list[tuple[str, list[str]]]:
    """Split file lines into contiguous table blocks with their preceding line.

    Args:
        lines (list[str]): The workflow file's lines, terminators removed.

    Returns:
        list[tuple[str, list[str]]]: One `(preceding, block)` pair per maximal
        run of table rows. `preceding` is the last non-blank line before the
        block, stripped, so a caller can honour `SKIP_MARKER`.
    """
    tables: list[tuple[str, list[str]]] = []
    preceding = ""
    index = 0
    while index < len(lines):
        if ROW.match(lines[index]):
            block, index = _take_table_block(lines, index)
            tables.append((preceding, block))
            continue
        stripped = lines[index].strip()
        if stripped:
            preceding = stripped
        index += 1
    return tables


def _rows_from_block(block: list[str]) -> list[tuple[str, str, str, str]]:
    """(phase, step, action, effect) tuples for one table block.

    The header row and its `:---` separator are dropped when present; a row
    whose phase cell is a dash run or the literal `phase` is skipped as a second
    safety net against non-step rows.

    Args:
        block (list[str]): Consecutive table-row lines from one table.

    Returns:
        list[tuple[str, str, str, str]]: One tuple per real step row.
    """
    body = block[2:] if len(block) >= 2 and _is_separator_row(block[1]) else block
    rows: list[tuple[str, str, str, str]] = []
    for line in body:
        match = ROW.match(line)
        if not match:
            continue
        phase, second, third = match.group(2).strip(), match.group(4).strip(), match.group(5).strip()
        if set(phase) <= set(": -") or phase.lower() == "phase":
            continue
        step = second.strip("`* ")
        rows.append((phase.strip("* "), step, third, _effect(second, third)))
    return rows


def parse(path: Path) -> list[tuple[str, str, str, str]]:
    """(phase, step, action, effect) rows from a workflow's step tables.

    A table immediately preceded by a line equal to `SKIP_MARKER` is a reference
    table, not a step list, and contributes no rows.

    Args:
        path (Path): A workflow file under `workflows/`.

    Returns:
        list[tuple[str, str, str, str]]: Every real step row, in file order.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: list[tuple[str, str, str, str]] = []
    for preceding, block in _group_tables(lines):
        if preceding == SKIP_MARKER:
            continue
        rows.extend(_rows_from_block(block))
    return rows


# Static legend text for "## 1. Artifact x Workflow matrix" — hoisted out of
# `build()` so the function that assembles the guide stays under the
# per-function line cap (`agents.md §1 max_lines_per_func`) without changing
# what the legend says.
COLUMNS_LEGEND = [
    "",
    "**Columns**, from `config/artifact_registry.json` — the artifact and the phase",
    "that leaves it. A phase is defined by the artifact it leaves, which is what makes",
    "the matrix portable across tools rather than tied to one runner's agent names.",
    "",
]

# Static legend text for "## 2. Steps, by protocol" — same rationale as
# `COLUMNS_LEGEND` above.
EFFECT_LEGEND = [
    "---",
    "*The **Effect** column is `read`, `write` or `verify` when the step's verb",
    "is recognised. Two labels mark what the heuristic will not guess at, kept",
    "visible because an unclassified step is information while a wrongly",
    "classified one is a lie the next reader inherits:*",
    "",
    "- *`ambiguous` — a real step id whose verb the heuristic does not recognise.*",
    "- *`prose` — the step cell is a `**Bold sentence.**` rather than a verb plus object; it needs a step id and a done-criterion (`agents.md §1 unambiguous_action`).*",
    "",
    "*A table immediately preceded by a `<!-- map_workflows:skip-table -->` line is a reference table, not a step list, and is excluded from this map entirely.*",
    "",
]


def build() -> str:
    lines = [
        "# Workflow Step Map",
        "",
        "> [!IMPORTANT]",
        "> **Generated by `scripts/map_workflows.py`. Do not edit by hand.**",
        "> `make verify` regenerates this file and fails if it differs from the tree.",
        "",
        "Every `/agents:*` protocol, its steps, and what each one does to the shared",
        "artifacts. The `write` column is the diagnostic one: an asymmetry between two",
        "protocols that should mirror each other shows up there first.",
        "",
        "## 1. Artifact x Workflow matrix",
        "",
        "| Workflow | " + " | ".join(ARTIFACTS) + " |",
        "| :--- | " + " | ".join([":---"] * len(ARTIFACTS)) + " |",
    ]

    parsed = {p: parse(p) for p in sorted(WORKFLOWS.glob("*.md"))}

    for path, rows in parsed.items():
        cells = []
        for artifact in ARTIFACTS:
            kinds = {classify(action) for _, _, action, _ in rows if artifact in action}
            cells.append("/".join(sorted(kinds)) if kinds else "—")
        lines.append(f"| `{path.stem}` | " + " | ".join(cells) + " |")

    lines += COLUMNS_LEGEND
    lines += [f"- `{artifact}` — {phase}" for artifact, phase in ARTIFACTS.items()]

    lines += ["", "## 2. Steps, by protocol", ""]
    for path, rows in parsed.items():
        lines += [f"### `{path.name}`", "", "| Phase | Step | Effect |", "| :--- | :--- | :--- |"]
        for phase, step, _, effect in rows:
            lines.append(f"| {phase} | `{step}` | {effect} |")
        lines.append("")

    lines += EFFECT_LEGEND
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true", help="Fail if the guide is stale.")
    args = parser.parse_args()

    # Framework-scoped: `workflows/` and the guide are this repository's, not the
    # caller's. See `scripts/_root.py` for why the cwd is set rather than each
    # path rewritten — every message below stays relative and unchanged.
    os.chdir(agents_root())

    generated = build()
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != generated:
            print(f"❌ {OUTPUT} is stale — regenerate with "
                  f"`python3 scripts/map_workflows.py`.", file=sys.stderr)
            return 1
        print(f"✅ {OUTPUT} is current.")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated, encoding="utf-8")
    print(f"✅ Wrote {OUTPUT}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
