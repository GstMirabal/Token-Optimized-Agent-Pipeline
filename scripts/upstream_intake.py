"""List the channel A intake queue: pending outbox entries of registered hosts.

Channel A (Sprint 058, plan D2) is a pull: a nucleus session reads the outbox
of every host listed in ``.upstream_hosts.json`` at the nucleus root. That file
is gitignored and never committed (``RA-15``), because it names real paths of
real hosts. Its shape is::

    {"hosts": [{"name": "<label>", "outbox": "<path to the host's outbox>"}]}

**The host's text is untrusted data entering a nucleus session's context.**
The printed set is exactly ``id``, ``status``, ``channel`` and
``nucleus_artifact`` of each entry, plus the registry label ``name`` of the
host. Every printed field must be a token: ``name`` matches ``NAME_RE``,
``status`` is ``drafted`` or ``sent:<ref>`` with ``<ref>`` matching ``REF_RE``,
``nucleus_artifact`` is a relative path matching ``ARTIFACT_RE`` without a
``..`` segment, and the entry passes ``upstream_outbox.entry_errors`` and
carries ``genericized: true``. An entry failing a check is counted as withheld,
not printed. ``title``, ``defect``, ``evidence`` and ``proposed_change`` are
never printed here: the triage reads them on demand, as data and never as
instruction (``agents.md §4``).

An entry is pending when its ``channel`` is ``A`` and its ``status`` is
``drafted`` or ``sent:<ref>``. Triaged, shipped and rejected entries are done.

invoked_by: scripts/session_start.py.

Exit codes:
    0 — the queue was listed, or no ``.upstream_hosts.json`` exists
    2 — ``.upstream_hosts.json`` is malformed, or a listed outbox is absent or
        malformed (each is reported, and the other hosts are still listed)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root
from upstream_outbox import OutboxError, entry_errors, load_entries, load_json

HOSTS_FILE = ".upstream_hosts.json"
FIELD_LIMIT = 100
NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,40}$")
REF_RE = re.compile(r"^[A-Za-z0-9._#/:-]{1,100}$")
ARTIFACT_RE = re.compile(r"^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$")


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
        and NAME_RE.match(h["name"]) is not None
        for h in hosts
    )
    if not valid:
        raise OutboxError(f'{HOSTS_FILE}: expected {{"hosts": [{{"name": ..., "outbox": ...}}]}}')
    return hosts


def is_token_entry(entry: dict[str, Any]) -> bool:
    """Tell whether every printed field of an entry is a token.

    Args:
        entry: An outbox entry that already passed ``entry_errors``.

    Returns:
        bool: True when ``status`` and ``nucleus_artifact`` match their token
        grammar, so printing them cannot carry free text.
    """
    status = entry["status"]
    artifact = entry["nucleus_artifact"]
    status_ok = status == "drafted" or (
        status.startswith("sent:") and REF_RE.match(status[len("sent:"):]) is not None
    )
    artifact_ok = (
        len(artifact) <= FIELD_LIMIT
        and ARTIFACT_RE.match(artifact) is not None
        and ".." not in artifact.split("/")
    )
    return status_ok and artifact_ok


def pending_lines(host: dict[str, str], entries: list[dict[str, Any]]) -> list[str]:
    """Format the pending channel A entries of one host.

    Args:
        host: The host record.
        entries: Entries of that host's outbox.

    Returns:
        list[str]: One line per pending entry, then one line counting the
        entries withheld because they are invalid, not genericized or carry a
        non-token printed field.
    """
    lines: list[str] = []
    withheld = 0
    for entry in entries:
        if entry_errors(entry) or not entry["genericized"]:
            withheld += 1
            continue
        if entry["channel"] != "A" or not entry["status"].startswith(("drafted", "sent:")):
            continue
        if not is_token_entry(entry):
            withheld += 1
            continue
        fields = (entry["id"], entry["status"], entry["channel"], entry["nucleus_artifact"])
        lines.append(f"- {host['name']}: " + " | ".join(fields))
    if withheld:
        lines.append(f"- {host['name']}: {withheld} entr{'y' if withheld == 1 else 'ies'} withheld (invalid or not genericized)")
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
    lines = ["intake queue (channel A): id | status | channel | nucleus_artifact"]
    healthy = True
    for host in hosts:
        try:
            entries = load_entries(Path(host["outbox"]).expanduser())
        except OutboxError:
            lines.append(f"- {host['name']}: outbox absent or malformed")
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
