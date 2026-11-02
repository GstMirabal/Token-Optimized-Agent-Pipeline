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
makes ``.upstream_hosts.json`` malformed. An entry that is not pending (below)
is skipped before any counting, whatever its shape. A pending entry that fails
``upstream_outbox.entry_errors`` or lacks ``genericized: true`` is counted as
withheld (invalid or not genericized); that includes a channel A ``drafted``
entry the host's human has not yet signed, which is pending but not printable.
A pending entry whose ``id`` is not a
token is counted as withheld (non-token fields); one whose ``id`` is a token
but whose ``status`` or ``nucleus_artifact`` is not is withheld on its own line
naming its ``id``. ``title``, ``defect``, ``evidence`` and ``proposed_change``
are never printed here: the triage reads them on demand, as data and never as
instruction (``agents.md §4``).

An entry is pending when its ``channel`` is ``A`` and its ``status`` starts
with ``drafted`` or ``sent:``. Triaged, shipped and rejected entries are done.

invoked_by: scripts/session_start.py.

**Per-host wall-clock budget (QA5-1).** The work of one host (resolving its
outbox path, reading it, building its lines) runs in a child interpreter
(``python -I``) that the parent kills after ``HOST_BUDGET_SECONDS`` of wall
clock. That bounds the time one host can take for any delay the child can be
killed out of: a user-space loop, a regex, an interruptible wait. A thread or
``signal.alarm`` cannot interrupt a C-level regex, a killed process can.
**Exception**: after ``kill()``, ``subprocess.run`` calls ``wait()`` with no
timeout, so a child in uninterruptible kernel sleep (for example a read from
a hard-mounted network filesystem) is not bounded. The budget bounds time
only: it claims nothing about memory or output size. The child prints one JSON object
``{"lines": [...]}`` on stdout; the parent re-validates its shape. A child
that times out yields ``- <name>: outbox timed out``; a child that exits
non-zero or prints a malformed object yields
``- <name>: outbox unreadable or unprocessable (<ExcType>)``, a label that
does not blame the host, because the failing step may be nucleus code
(QA5 note O5). ``<ExcType>`` is an exception type name, never a message; the
child reports it as a bounded identifier the parent re-validates. The child's
stdout and stderr are never echoed, because they can quote host text.

Exit codes:
    0 — the queue was listed, or no ``.upstream_hosts.json`` exists
    2 — ``.upstream_hosts.json`` is malformed, or a listed outbox could not be
        read or processed (a fault in the child, the nucleus's own code
        included), or exceeded its budget (each is reported, and the other
        hosts are still listed)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _root import agents_root
from upstream_outbox import OutboxError, entry_errors, load_entries, load_json

HOSTS_FILE = ".upstream_hosts.json"
# Wall-clock budget of one host's work, in seconds. A healthy host takes well
# under one second (child start-up included); 5 s keeps the boot usable while
# a registry of several hosts stays within a bounded worst case.
HOST_BUDGET_SECONDS = 5.0
CHILD_FLAG = "--host-child"
TYPE_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,60}")
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
        str: ``done`` (not a pending channel A entry, decided first so it is
        never counted), ``invalid`` (pending, but fails ``entry_errors`` or is
        not genericized), ``non_token`` (its ``id`` is not a token),
        ``withheld`` (its ``status`` or ``nucleus_artifact`` is not a token) or
        ``print``.
    """
    status = entry.get("status")
    pending = isinstance(status, str) and status.startswith(("drafted", "sent:"))
    if entry.get("channel") != "A" or not pending:
        return "done"
    if entry_errors(entry) or entry["genericized"] is not True:
        return "invalid"
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
        cause; then one line counting pending entries invalid or not
        genericized (an entry that is not pending is never counted), and
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


def host_work(host: dict[str, str]) -> list[str]:
    """Do the work of one host in this process: resolve, read, build lines.

    Args:
        host: The host record, already validated by ``load_hosts``.

    Returns:
        list[str]: That host's pending lines.

    Raises:
        Exception: Whatever resolving or reading the outbox raised.
    """
    return pending_lines(host, load_entries(Path(host["outbox"]).expanduser()))


def child_command() -> list[str]:
    """Return the argv of the child interpreter that runs one host's work.

    Returns:
        list[str]: Isolated interpreter, this script and ``CHILD_FLAG``.
    """
    return [sys.executable, "-I", str(Path(__file__).resolve()), CHILD_FLAG]


class ChildError(Exception):
    """A host's child failed; ``type_name`` is a validated exception type name."""

    def __init__(self, type_name: str) -> None:
        super().__init__(type_name)
        self.type_name = type_name


def _child_failure(stdout: str) -> ChildError:
    """Build the error for a child that exited non-zero.

    Args:
        stdout: The child's stdout, untrusted.

    Returns:
        ChildError: Carrying the type name the child reported when it is a
        bounded identifier, else ``ChildExit``. Nothing else of ``stdout`` is kept.
    """
    try:
        name = json.loads(stdout).get("error")
    except Exception:  # noqa: BLE001 - any unparseable output is just ``ChildExit``
        name = None
    return ChildError(name if is_token(name, TYPE_NAME_RE) else "ChildExit")


def run_host(host: dict[str, str]) -> list[str]:
    """Run one host's work in a child killed after ``HOST_BUDGET_SECONDS``.

    Args:
        host: The host record, already validated by ``load_hosts``.

    Returns:
        list[str]: The lines the child printed, shape re-validated.

    Raises:
        subprocess.TimeoutExpired: The child exceeded the budget (it is killed).
        ChildError: The child exited non-zero or printed a malformed object.
    """
    done = subprocess.run(
        child_command(),
        input=json.dumps(host),
        capture_output=True,
        text=True,
        timeout=HOST_BUDGET_SECONDS,
        check=False,
    )
    if done.returncode != 0:
        raise _child_failure(done.stdout)
    document = json.loads(done.stdout)
    lines = document.get("lines") if isinstance(document, dict) else None
    shaped = isinstance(lines, list) and set(document) == {"lines"}
    if not shaped or not all(isinstance(line, str) for line in lines):
        raise ChildError("ChildOutputMalformed")
    return lines


def host_lines(host: dict[str, str]) -> tuple[list[str], bool]:
    """Build the lines of one host behind a total fault boundary and a budget.

    Every step of one host sits inside ``run_host`` (a child process) under a
    single ``except Exception``. The boundary is deliberately not a list of
    exception types: QA3-1 (a decode error) and QA4-1 (``Path.expanduser``
    raising ``RuntimeError``) were two members of one family, "one host
    aborts or stalls every host", and QA5-1 (a quadratic regex) a third; a
    list of causes closes only the members already found. The budget is
    cause-independent for the same reason.

    Args:
        host: The host record, already validated by ``load_hosts``.

    Returns:
        tuple[list[str], bool]: That host's lines, and False when the host
        failed, in which case the only line is ``- <name>: outbox timed out``
        (budget exceeded) or
        ``- <name>: outbox unreadable or unprocessable (<ExcType>)``. The
        cause class, never a message (which can quote host text), is logged
        to stderr.
    """
    try:
        return run_host(host), True
    except subprocess.TimeoutExpired:
        print(f"upstream_intake: host {host['name']}: timeout", file=sys.stderr)
        return [f"- {host['name']}: outbox timed out"], False
    except Exception as exc:  # noqa: BLE001 - the per-host boundary is total by design
        kind = exc.type_name if isinstance(exc, ChildError) else type(exc).__name__
        print(f"upstream_intake: host {host['name']}: {kind}", file=sys.stderr)
        return [f"- {host['name']}: outbox unreadable or unprocessable ({kind})"], False


def child_main() -> int:
    """Run one host's work as the child: host JSON on stdin, result on stdout.

    Returns:
        int: 0 after printing ``{"lines": [...]}``, 1 on any exception after
        printing ``{"error": "<ExcType>"}`` (a type name, never a message).
    """
    try:
        host = json.loads(sys.stdin.read())
        print(json.dumps({"lines": host_work(host)}))
    except Exception as exc:  # noqa: BLE001 - total; the parent maps any failure to one line
        print(json.dumps({"error": type(exc).__name__}))
        return 1
    return 0


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
    except Exception as exc:  # noqa: BLE001 - total, like the per-host boundary
        # The type name only: the message of an unexpected error can quote host text.
        return [f"intake queue (channel A): {HOSTS_FILE} unreadable ({type(exc).__name__})"], False
    if not hosts:
        return [f"intake queue (channel A): no {HOSTS_FILE} registered"], True
    lines = ["intake queue (channel A): id | status | channel | nucleus_artifact"]
    healthy = True
    for host in hosts:
        own, ok = host_lines(host)
        lines += own
        healthy = healthy and ok
    if len(lines) == 1:
        lines.append("- (none pending)")
    return lines, healthy


def main() -> int:
    """Print the intake queue.

    Returns:
        int: 0 when every input was readable, 2 otherwise; under
        ``CHILD_FLAG`` the exit code of ``child_main``.
    """
    if sys.argv[1:] == [CHILD_FLAG]:
        return child_main()
    lines, healthy = intake_lines(agents_root())
    print("\n".join(lines))
    return 0 if healthy else 2


if __name__ == "__main__":
    sys.exit(main())
