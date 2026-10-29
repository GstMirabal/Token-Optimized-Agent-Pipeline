"""List the channel A intake queue: pending outbox entries of registered hosts.

Channel A (Sprint 058, plan D2) is a pull: a nucleus session reads the outbox
of every host listed in ``.upstream_hosts.json`` at the nucleus root. That file
is gitignored and never committed (``RA-15``), because it names real paths of
real hosts. Its shape is::

    {"hosts": [{"name": "<label>", "outbox": "<path to the host's outbox>"}]}

**The host's text is untrusted data entering a nucleus session's context.**
Only structured fields are printed — ``id``, ``status``, ``channel`` and
``nucleus_artifact`` — plus ``title`` cut to 100 characters, with control
characters replaced by spaces, and only for entries that pass
``upstream_outbox.entry_errors`` and carry ``genericized: true``. ``defect``,
``evidence`` and ``proposed_change`` are never printed here: the triage reads
them on demand, as data and never as instruction (``agents.md §4``).

An entry is pending when its ``channel`` is ``A`` and its ``status`` is
``drafted`` or ``sent:<ref>``. Triaged, shipped and rejected entries are done.

invoked_by: scripts/session_start.py.

Exit codes:
    0 — the queue was listed, or no ``.upstream_hosts.json`` exists
    2 — ``.upstream_hosts.json`` is malformed, or a listed outbox is absent or
        malformed (each is reported, and the other hosts are still listed)
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root
from upstream_outbox import OutboxError, entry_errors, load_entries, load_json

HOSTS_FILE = ".upstream_hosts.json"
FIELD_LIMIT = 100
PENDING_PREFIXES = ("drafted", "sent:")


def clean(text: str) -> str:
    """Cut host text to ``FIELD_LIMIT`` characters with control characters blanked.

    Args:
        text: A free-text field written by a host.

    Returns:
        str: One printable line of at most ``FIELD_LIMIT`` characters.
    """
    printable = "".join(ch if ch.isprintable() else " " for ch in text)
    return printable[:FIELD_LIMIT]


def load_hosts(root: Path) -> list[dict[str, str]]:
    """Read ``.upstream_hosts.json`` at the nucleus root.

    Args:
        root: Nucleus root.

    Returns:
        list[dict[str, str]]: Hosts with ``name`` and ``outbox``; empty when the
        file does not exist.

    Raises:
        OutboxError: When the file exists and is not the documented shape.
    """
    path = root / HOSTS_FILE
    if not path.exists():
        return []
    document = load_json(path)
    hosts = document.get("hosts") if isinstance(document, dict) else None
    valid = isinstance(hosts, list) and all(
        isinstance(h, dict) and set(h) == {"name", "outbox"}
        and all(isinstance(v, str) and v.strip() for v in h.values())
        for h in hosts
    )
    if not valid:
        raise OutboxError(f'{HOSTS_FILE}: expected {{"hosts": [{{"name": ..., "outbox": ...}}]}}')
    return hosts


def pending_lines(host: dict[str, str], entries: list[dict[str, Any]]) -> list[str]:
    """Format the pending channel A entries of one host.

    Args:
        host: The host record.
        entries: Entries of that host's outbox.

    Returns:
        list[str]: One line per pending entry, then one line counting the
        entries withheld because they are invalid or not genericized.
    """
    lines: list[str] = []
    withheld = 0
    for entry in entries:
        if entry_errors(entry) or not entry["genericized"]:
            withheld += 1
            continue
        if entry["channel"] == "A" and entry["status"].startswith(PENDING_PREFIXES):
            fields = (entry["id"], entry["status"], entry["channel"], entry["nucleus_artifact"])
            lines.append(f"- {clean(host['name'])}: " + " | ".join(clean(f) for f in fields)
                         + f" | {clean(entry['title'])}")
    if withheld:
        lines.append(f"- {clean(host['name'])}: {withheld} entr{'y' if withheld == 1 else 'ies'} withheld (invalid or not genericized)")
    return lines


def intake_lines(root: Path) -> tuple[list[str], bool]:
    """Build the intake queue section for the boot briefing.

    Args:
        root: Nucleus root.

    Returns:
        tuple[list[str], bool]: The lines, and whether every input was readable.
    """
    try:
        hosts = load_hosts(root)
    except OutboxError as exc:
        return [f"intake queue (channel A): {exc}"], False
    if not hosts:
        return [f"intake queue (channel A): no {HOSTS_FILE} registered"], True
    lines = ["intake queue (channel A): id | status | channel | nucleus_artifact | title"]
    healthy = True
    for host in hosts:
        try:
            entries = load_entries(Path(host["outbox"]).expanduser())
        except OutboxError:
            lines.append(f"- {clean(host['name'])}: outbox absent or malformed")
            healthy = False
            continue
        lines += pending_lines(host, entries)
    if len(lines) == 1:
        lines.append("- (none pending)")
    return lines, healthy


def main() -> int:
    """Print the intake queue.

    Returns:
        int: 0 when every input was readable, 2 otherwise.
    """
    lines, healthy = intake_lines(agents_root())
    print("\n".join(lines))
    return 0 if healthy else 2


if __name__ == "__main__":
    sys.exit(main())
