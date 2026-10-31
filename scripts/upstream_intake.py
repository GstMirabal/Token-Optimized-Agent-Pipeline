"""List the channel A intake queue: pending outbox entries of registered hosts.

Channel A (Sprint 058, plan D2) is a pull: a nucleus session reads the outbox
of every host listed in ``.upstream_hosts.json`` at the nucleus root. That file
is gitignored and never committed (``RA-15``), because it names real paths of
real hosts. Its shape is::

    {"hosts": [{"name": "<label>", "outbox": "<path to the host's outbox>"}]}

**The host's text is untrusted data entering a nucleus session's context.**
The printed set is exactly ``id``, ``status``, ``channel`` and
``nucleus_artifact`` of each entry, plus the registry label ``name`` of the
host. A field is printed only when it is a token: each value checked against a
grammar below is a ``str`` of at most ``FIELD_LIMIT`` characters that the
grammar fully matches (``re.fullmatch``, so a trailing newline is not a
match): ``name`` matches ``NAME_RE``, ``id`` matches
``ID_RE``, ``status`` is ``drafted`` or ``sent:<ref>`` with ``<ref>`` matching
``REF_RE``, ``channel`` is ``A``, and ``nucleus_artifact`` matches
``ARTIFACT_RE`` and has no ``..`` segment. A token can still carry words the
host chose; the triage reads it as data. A host whose ``name`` is not a token
makes ``.upstream_hosts.json`` malformed. An entry that fails
``upstream_outbox.entry_errors`` or lacks ``genericized: true`` is counted as
withheld (invalid or not genericized). A pending entry whose ``id`` is not a
token is counted as withheld (non-token fields); one whose ``id`` is a token
but whose ``status`` or ``nucleus_artifact`` is not is withheld on its own line
naming its ``id``. ``title``, ``defect``, ``evidence`` and ``proposed_change``
are never printed here: the triage reads them on demand, as data and never as
instruction (``agents.md §4``).

An entry is pending when its ``channel`` is ``A`` and its ``status`` starts
with ``drafted`` or ``sent:``. Triaged, shipped and rejected entries are done.

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
# Applied through ``is_token`` only: ``fullmatch``, because ``$`` also matches
# before a trailing newline, and a length bound of ``FIELD_LIMIT`` characters.
NAME_RE = re.compile(r"[A-Za-z0-9._-]{1,40}")
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
REF_RE = re.compile(r"[A-Za-z0-9._#/:-]+")
ARTIFACT_RE = re.compile(r"[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*")


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
        and is_token(h["name"], NAME_RE)
        for h in hosts
    )
    if not valid:
        raise OutboxError(f'{HOSTS_FILE}: expected {{"hosts": [{{"name": ..., "outbox": ...}}]}}')
    return hosts


def is_token(value: object, pattern: re.Pattern[str]) -> bool:
    """Tell whether a value is a bounded string that fully matches a grammar.

    Args:
        value: The candidate field value, of any type.
        pattern: The token grammar.

    Returns:
        bool: True when ``value`` is a ``str`` of at most ``FIELD_LIMIT``
        characters and ``pattern.fullmatch`` accepts all of it.
    """
    return (
        isinstance(value, str)
        and len(value) <= FIELD_LIMIT
        and pattern.fullmatch(value) is not None
    )


def is_token_entry(entry: dict[str, Any]) -> bool:
    """Tell whether ``status`` and ``nucleus_artifact`` of an entry are tokens.

    Args:
        entry: An outbox entry that already passed ``entry_errors``.

    Returns:
        bool: True when ``status`` and ``nucleus_artifact`` fully match their
        token grammar. Only such fields are printed; a token can still carry
        words the host chose, and the triage reads it as data.
    """
    status = entry["status"]
    artifact = entry["nucleus_artifact"]
    status_ok = status == "drafted" or (
        isinstance(status, str)
        and status.startswith("sent:")
        and is_token(status[len("sent:"):], REF_RE)
    )
    artifact_ok = is_token(artifact, ARTIFACT_RE) and ".." not in artifact.split("/")
    return status_ok and artifact_ok


def _plural(count: int) -> str:
    """Return ``entry`` or ``entries`` for a count.

    Args:
        count: Number of entries.

    Returns:
        str: The count followed by the noun.
    """
    return f"{count} entr{'y' if count == 1 else 'ies'}"


def classify(entry: dict[str, Any]) -> str:
    """Sort one outbox entry into the bucket that decides how it is reported.

    Args:
        entry: A raw outbox entry.

    Returns:
        str: ``invalid`` (fails ``entry_errors`` or not genericized), ``done``
        (not a pending channel A entry), ``non_token`` (its ``id`` is not a
        token), ``withheld`` (its ``status`` or ``nucleus_artifact`` is not a
        token) or ``print``.
    """
    if entry_errors(entry) or entry["genericized"] is not True:
        return "invalid"
    if entry["channel"] != "A" or not entry["status"].startswith(("drafted", "sent:")):
        return "done"
    if not is_token(entry["id"], ID_RE):
        return "non_token"
    return "print" if is_token_entry(entry) else "withheld"


def entry_line(host: dict[str, str], entry: dict[str, Any], kind: str) -> str | None:
    """Format the line an entry gets on its own, when it gets one.

    Args:
        host: The host record.
        entry: The outbox entry.
        kind: The bucket ``classify`` returned for it.

    Returns:
        str | None: The fields line for ``print``, the ``id`` and cause for
        ``withheld``, and None for the counted or done buckets.
    """
    if kind == "print":
        fields = (entry["id"], entry["status"], "A", entry["nucleus_artifact"])
        return f"- {host['name']}: " + " | ".join(fields)
    if kind == "withheld":
        return f"- {host['name']}: {entry['id']} withheld (non-token status or nucleus_artifact)"
    return None


def pending_lines(host: dict[str, str], entries: list[dict[str, Any]]) -> list[str]:
    """Format the pending channel A entries of one host.

    Args:
        host: The host record.
        entries: Entries of that host's outbox.

    Returns:
        list[str]: One line per pending entry, either its fields or, when its
        ``status`` or ``nucleus_artifact`` is not a token, its ``id`` and the
        cause; then one line counting entries invalid or not genericized, and
        one counting pending entries whose ``id`` is not a token.
    """
    lines: list[str] = []
    counts = {"invalid": 0, "non_token": 0}
    for entry in entries:
        kind = classify(entry)
        if kind in counts:
            counts[kind] += 1
        line = entry_line(host, entry, kind)
        if line is not None:
            lines.append(line)
    causes = {"invalid": "invalid or not genericized", "non_token": "non-token fields"}
    lines += [
        f"- {host['name']}: {_plural(count)} withheld ({causes[kind]})"
        for kind, count in counts.items() if count
    ]
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
