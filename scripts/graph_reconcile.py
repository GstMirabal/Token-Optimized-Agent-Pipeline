"""Reconciles tracked files against the knowledge graph's `source_file` set.

`graphify` (a third-party package, `Makefile` `graphify-update` /
`graphify-rebuild`) omits files it cannot process without recording that it
did (`REVDOC-G1`, `docs/audits/UPSTREAM_FINDINGS_FROM_HOSTS.md`). A consumer
of the graph cannot tell "not in the graph" from "not in the repository",
which matters because `agents.md §2 graph_sovereignty` mandates querying the
graph *before* any full-codebase research -- a silently incomplete graph
answers that query confidently. Sprint 051 measured that the cause is
upstream and not fixable here, so the nucleus owns the reconciliation instead
of the drop itself (`docs/sprints/052-core-pipeline/IMPLEMENTATION_PLAN.md`
`D5`).

This module compares `git ls-files` against every node's `source_file` in
`graphify-out/graph.json`, writes `graphify-out/unmapped_files.json` (sorted
paths, a count, and a per-extension breakdown) and prints the count.

**Advisory, not blocking**: files with no source-code meaning to the graph
(`.txt`, `.svg`, `.yml`, ...) are legitimately unmapped, so a nonzero count is
not itself a defect -- this script exits `0` in every case, including when
`graphify-out/graph.json` is absent (nothing has been graphed yet).

invoked_by: Makefile `graphify-update` and `graphify-rebuild` targets, run
immediately after the graph write those targets already perform.

Usage:
    python3 scripts/graph_reconcile.py [--root PATH] [--graph PATH]

    `--root` defaults to the current working directory (the tree `graphify`
    was pointed at); `--graph` defaults to `<root>/graphify-out/graph.json`.
    Both exist for testability against a throwaway repository.

Exit codes:
    0 -- always. Advisory only (see module docstring above).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_GRAPH_RELATIVE = Path("graphify-out") / "graph.json"
DEFAULT_REPORT_NAME = "unmapped_files.json"


def tracked_files(root: Path) -> set[str]:
    """Repo-relative paths `git` tracks under `root`.

    Args:
        root: Repository root to run `git ls-files` from.

    Returns:
        set[str]: POSIX-style, repo-relative tracked file paths.
    """
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return {line for line in result.stdout.splitlines() if line}


def normalize_source_file(source_file: str, root: Path) -> str:
    """Repo-relative, POSIX-style form of a graph node's `source_file`.

    Args:
        source_file: The raw value stored on a graph node. May already be
            repo-relative, or may be an absolute path.
        root: Repository root the graph was built against, resolved.

    Returns:
        str: The path relative to `root` using `/` separators. An absolute
            value outside `root` is returned unchanged (as POSIX) rather than
            raising, since it can never match a tracked file and should still
            surface for inspection rather than crash the reconciliation.
    """
    candidate = Path(source_file)
    if candidate.is_absolute():
        try:
            candidate = candidate.relative_to(root)
        except ValueError:
            return candidate.as_posix()
    return candidate.as_posix()


def mapped_files(graph_path: Path, root: Path) -> set[str]:
    """Normalised `source_file` values recorded across every graph node.

    Args:
        graph_path: Path to `graphify-out/graph.json`.
        root: Repository root the graph was built against, for normalisation.

    Returns:
        set[str]: Repo-relative source files the graph knows about.
    """
    with graph_path.open(encoding="utf-8") as handle:
        graph = json.load(handle)
    return {
        normalize_source_file(node["source_file"], root)
        for node in graph.get("nodes", [])
        if "source_file" in node
    }


def extension_breakdown(paths: list[str]) -> dict[str, int]:
    """Per-extension count over `paths`.

    Args:
        paths: File paths to bucket.

    Returns:
        dict[str, int]: Extension (including the leading dot, or the literal
            `"(none)"` for extensionless files) mapped to its occurrence
            count, sorted by extension.
    """
    counts: dict[str, int] = {}
    for path in paths:
        suffix = Path(path).suffix or "(none)"
        counts[suffix] = counts.get(suffix, 0) + 1
    return dict(sorted(counts.items()))


def build_report(root: Path, graph_path: Path) -> dict:
    """Computes the unmapped-file report for `root` against `graph_path`.

    Args:
        root: Repository root to compare `git ls-files` against. Resolved.
        graph_path: Path to the graph whose `source_file` set is the mapped
            side of the comparison.

    Returns:
        dict: `{"unmapped": [...], "count": int, "by_extension": {...}}`.
    """
    tracked = tracked_files(root)
    mapped = mapped_files(graph_path, root)
    unmapped = sorted(tracked - mapped)
    return {
        "unmapped": unmapped,
        "count": len(unmapped),
        "by_extension": extension_breakdown(unmapped),
    }


def write_report(report: dict, out_path: Path) -> None:
    """Writes `report` to `out_path` as indented JSON.

    Args:
        report: The report produced by `build_report`.
        out_path: Destination file; parent directories are created if absent.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parses `--root` and `--graph`.

    Args:
        argv: Argument vector, or `None` to read `sys.argv[1:]`.

    Returns:
        argparse.Namespace: Parsed `root` and `graph` (either may be `None`
            on `graph`, meaning "derive from `root`").
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path("."),
        help="Repository root to reconcile (default: current working directory).",
    )
    parser.add_argument(
        "--graph", type=Path, default=None,
        help="Path to graph.json (default: <root>/graphify-out/graph.json).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point: reconciles, writes the report, prints the count.

    Args:
        argv: Argument vector, or `None` to read `sys.argv[1:]`.

    Returns:
        int: Always `0` -- advisory, never blocking (see module docstring).
    """
    args = parse_args(argv)
    root = args.root.resolve()
    graph_path = (args.graph or (root / DEFAULT_GRAPH_RELATIVE)).resolve()

    if not graph_path.is_file():
        print(f"graph_reconcile: advisory -- no graph at {graph_path}, nothing to reconcile.")
        return 0

    report = build_report(root, graph_path)
    out_path = graph_path.parent / DEFAULT_REPORT_NAME
    write_report(report, out_path)
    print(f"graph_reconcile: {report['count']} tracked file(s) unmapped in the graph -- see {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
