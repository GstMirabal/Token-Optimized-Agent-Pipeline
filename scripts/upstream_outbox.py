"""Validate, export and age a host's upstream outbox (agents.md §4 feedback_upstream).

A host records each framework-class finding as one entry of an outbox file
whose shape is ``docs/standards/templates/UPSTREAM_OUTBOX_TEMPLATE.json``
(Sprint 058, plan D1). Until this script existed a finding travelled as a
free-form handoff document with no state, and nine of one host's findings sat
unrecorded in the nucleus weeks later.

invoked_by: workflows/extract_workflow.md, workflows/close_workflow.md,
.github/workflows/host-finding-intake.yml.

Subcommands:
    check <outbox>          validate every entry; exit 2 on any defect
    check-issue --body-file F [--open-titles-file T] [--author-recent-count N]
                            print the intake labels of a ``host-finding`` issue
                            body, one per line (channel B filter, plan D3)
    export <outbox> --id ID --out F
                            write a channel B issue body and print the one
                            ``gh`` command the human runs; refuses channel A/C
    aged <outbox>           advisory: list ``drafted`` entries older than
                            ``aged_after_sprints`` sprints (plan Q3)
    deltas <outbox> --rules DIR
                            advisory: list host rule deltas tagged
                            ``outbox:<id>`` whose entry is ``shipped:``

**The genericization scan is a pattern denylist and makes no coverage claim**
(``agents.md §1 fail_closed_claims``). It checks exactly three families over
the string fields ``title``, ``defect``, ``evidence.command``,
``evidence.output``, ``nucleus_artifact`` and ``proposed_change`` (an issue
body is scanned whole):

1. absolute paths: POSIX (``/`` + at least two path segments, not preceded by
   a word character, ``.``, ``~``, ``/``, ``:`` or ``-``) and Windows (a drive
   letter, ``:\\``, then a non-space);
2. email addresses;
3. the secret assignment forms ``SECRET_ASSIGNMENT`` and
   ``UNQUOTED_ASSIGNMENT`` of ``hooks/on_commit.py``, imported rather than
   copied so the two lists cannot diverge.

The control is ``genericized: true``, which the host's human signs (``RA-15``).
A finding reports the family and the field, never the matched text.

Exit codes:
    0 — pass, or an advisory subcommand ran
    2 — malformed outbox, config or issue body file, an invalid entry, or a
        refused export (RA-11)
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _root import agents_root

from hooks.on_commit import SECRET_ASSIGNMENT, UNQUOTED_ASSIGNMENT

CONFIG_PATH = Path("config/upstream_intake.json")
IDENTITY_PATH = Path("config/framework_identity.json")
FIELDS = (
    "id",
    "title",
    "defect",
    "evidence",
    "nucleus_artifact",
    "proposed_change",
    "pin",
    "genericized",
    "channel",
    "recurs",
    "status",
)
TEXT_FIELDS = ("title", "defect", "nucleus_artifact", "proposed_change", "pin")
SCANNED_FIELDS = ("title", "defect", "nucleus_artifact", "proposed_change")
CHANNELS = ("A", "B", "C")
# Applied with ``fullmatch``: ``$`` also matches before a trailing newline (QA2-1).
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
STATUS_PATTERN = re.compile(r"(?:drafted|(?:sent|triaged|shipped|rejected):\S.*)")
PIN_PATTERN = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")
SPRINT_SUFFIX = re.compile(r"#(\d+)\s*$")
DELTA_TAG = re.compile(r"outbox:([A-Za-z0-9][A-Za-z0-9._-]*)")
SCAN_FAMILIES = (
    ("posix-path", re.compile(r"(?<![\w.~/:-])/[A-Za-z0-9._-]+/\S*")),
    ("windows-path", re.compile(r"(?<![A-Za-z])[A-Za-z]:\\\S")),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")),
    ("secret-assignment", SECRET_ASSIGNMENT),
    ("secret-assignment", UNQUOTED_ASSIGNMENT),
)
ISSUE_HEADING = re.compile(r"^###\s+(\S.*?)\s*$", re.MULTILINE)
NO_RESPONSE = "_No response_"
CHECKED_BOX = re.compile(r"^- \[[xX]\]", re.MULTILINE)
ISSUE_REQUIRED = ("id", "title", "defect", "nucleus_artifact", "proposed_change", "pin", "channel")
GENERICIZED_LINE = "- [X] Every host-identifying string is genericized (RA-15)"


class OutboxError(Exception):
    """An input the script cannot evaluate: absent, unparseable or misshapen."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build a JSON object, refusing a key that appears twice.

    Args:
        pairs: Key/value pairs in document order, from ``json.load``.

    Returns:
        dict[str, Any]: The object.

    Raises:
        OutboxError: When a key repeats; the last copy would silently win.
    """
    keys = [key for key, _ in pairs]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        raise OutboxError(f"duplicate key(s) {', '.join(duplicates)}")
    return dict(pairs)


def load_json(path: Path) -> Any:
    """Read a JSON file with duplicate keys rejected.

    Args:
        path: File to read.

    Returns:
        Any: The decoded document.

    Raises:
        OutboxError: When the file is absent or cannot be decoded: not UTF-8,
            not valid JSON, an integer over the int-string limit (each a
            ``ValueError``), nested beyond the recursion limit, or holding a
            string with a lone surrogate escape, which no UTF-8 output can
            print (``UnicodeEncodeError``, a ``ValueError``).
    """
    try:
        text = path.read_text(encoding="utf-8")
        document = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
        json.dumps(document, ensure_ascii=False).encode("utf-8")
        return document
    except (OSError, ValueError, RecursionError) as exc:
        raise OutboxError(f"{path}: {exc}") from exc


def read_text_file(path: Path) -> str:
    """Read a UTF-8 text file that is not JSON (issue body, titles, rule file).

    Args:
        path: File to read.

    Returns:
        str: The file's text.

    Raises:
        OutboxError: When the file is absent or unreadable (``OSError``) or
            not UTF-8 (``UnicodeDecodeError``, a ``ValueError``).
    """
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        raise OutboxError(f"{path}: {exc}") from exc


def load_entries(path: Path) -> list[dict[str, Any]]:
    """Read an outbox and return its entries.

    Args:
        path: The outbox file.

    Returns:
        list[dict[str, Any]]: Entries in file order.

    Raises:
        OutboxError: When the top level is not ``{"entries": [object, ...]}``.
    """
    document = load_json(path)
    if not isinstance(document, dict) or set(document) != {"entries"}:
        raise OutboxError(f'{path}: top level must be exactly {{"entries": [...]}}')
    entries = document["entries"]
    if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):
        raise OutboxError(f"{path}: `entries` must be a list of objects")
    return entries


def load_config(root: Path) -> dict[str, Any]:
    """Read the intake thresholds from ``config/upstream_intake.json``.

    Args:
        root: Framework root.

    Returns:
        dict[str, Any]: The config, with every key this script reads present.

    Raises:
        OutboxError: When a key is missing or has the wrong type.
    """
    config = load_json(root / CONFIG_PATH)
    expected = {
        "min_pin": str,
        "aged_after_sprints": int,
        "rate_limit_per_day": int,
        "security_words": list,
    }
    for key, kind in expected.items():
        if not isinstance(config.get(key), kind):
            raise OutboxError(f"{CONFIG_PATH}: `{key}` missing or not {kind.__name__}")
    if parse_pin(config["min_pin"]) is None:
        raise OutboxError(f"{CONFIG_PATH}: `min_pin` is not vX.Y.Z")
    return config


def parse_pin(pin: str) -> tuple[int, int, int] | None:
    """Parse ``vX.Y.Z`` (or ``X.Y.Z``) into a comparable tuple.

    Args:
        pin: Version text.

    Returns:
        tuple[int, int, int] | None: The version, or None when it is not one.
    """
    match = PIN_PATTERN.fullmatch(pin)
    if match is None:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def scan_text(text: str) -> list[str]:
    """Return the genericization families that match ``text``.

    Args:
        text: Free text written by a host.

    Returns:
        list[str]: Family names, deduplicated, in declaration order.
    """
    hits: list[str] = []
    for family, pattern in SCAN_FAMILIES:
        if family not in hits and pattern.search(text):
            hits.append(family)
    return hits


def scan_entry(entry: dict[str, Any]) -> list[str]:
    """Scan the free-text fields of one entry.

    Args:
        entry: An outbox entry that passed ``entry_errors``.

    Returns:
        list[str]: ``<field>: <family>`` per hit.
    """
    fields = {name: entry[name] for name in SCANNED_FIELDS}
    fields["evidence.command"] = entry["evidence"]["command"]
    fields["evidence.output"] = entry["evidence"]["output"]
    return [f"{name}: {family}" for name, text in fields.items() for family in scan_text(text)]


def _shape_errors(entry: dict[str, Any]) -> list[str]:
    """Report missing, unknown and mistyped keys of one entry.

    Args:
        entry: A raw outbox entry.

    Returns:
        list[str]: One message per shape defect.
    """
    errors = [f"missing `{key}`" for key in FIELDS if key not in entry]
    errors += [f"unknown key `{key}`" for key in entry if key not in FIELDS]
    errors += [
        f"`{key}` must be a non-empty string"
        for key in (*TEXT_FIELDS, "id", "status")
        if key in entry and not (isinstance(entry[key], str) and entry[key].strip())
    ]
    evidence = entry.get("evidence")
    if "evidence" in entry and not (
        isinstance(evidence, dict)
        and set(evidence) == {"command", "output"}
        and all(isinstance(v, str) and v.strip() for v in evidence.values())
    ):
        errors.append("`evidence` must be exactly {command, output}, both non-empty strings")
    if "genericized" in entry and not isinstance(entry["genericized"], bool):
        errors.append("`genericized` must be true or false")
    recurs = entry.get("recurs")
    if recurs is not None and not (isinstance(recurs, str) and recurs.strip()):
        errors.append("`recurs` must be null or a non-empty string")
    return errors


def entry_errors(entry: dict[str, Any]) -> list[str]:
    """Validate one entry against the D1 schema.

    Args:
        entry: A raw outbox entry.

    Returns:
        list[str]: One message per defect; empty when the entry is valid.
    """
    errors = _shape_errors(entry)
    if errors:
        return errors
    if not ID_PATTERN.fullmatch(entry["id"]):
        errors.append("`id` must match [A-Za-z0-9][A-Za-z0-9._-]*")
    if entry["channel"] not in CHANNELS:
        errors.append("`channel` must be A, B or C")
    if not STATUS_PATTERN.fullmatch(entry["status"]):
        errors.append("`status` must be drafted, or sent:/triaged:/shipped:/rejected: + text")
    if parse_pin(entry["pin"]) is None:
        errors.append("`pin` must be vX.Y.Z")
    if entry["status"] != "drafted" and not entry["genericized"]:
        errors.append("left `drafted` with `genericized: false`")
    if entry["genericized"]:
        errors += [f"`genericized: true` but {hit}" for hit in scan_entry(entry)]
    return errors


def check_outbox(entries: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    """Validate every entry of an outbox.

    Args:
        entries: Entries from ``load_entries``.

    Returns:
        tuple[list[str], list[str]]: Errors (exit 2) and notes (advisory): an
        ungenericized ``drafted`` entry that matches the scan is a note, since
        nothing has been sent yet.
    """
    errors: list[str] = []
    notes: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        label = entry.get("id") if isinstance(entry.get("id"), str) else f"#{index}"
        problems = entry_errors(entry)
        errors += [f"{label}: {problem}" for problem in problems]
        if label in seen:
            errors.append(f"{label}: duplicate id")
        seen.add(label)
        if not problems and not entry["genericized"]:
            notes += [f"{label}: {hit}; genericize before export" for hit in scan_entry(entry)]
    return errors, notes


def cmd_check(args: argparse.Namespace) -> int:
    """Run ``check``: validate an outbox file.

    Args:
        args: Parsed arguments with ``outbox``.

    Returns:
        int: 0 when valid, 2 otherwise.
    """
    entries = load_entries(Path(args.outbox))
    errors, notes = check_outbox(entries)
    for note in notes:
        print(f"[NOTE] {note}")
    for error in errors:
        print(f"[FAIL] {error}")
    if errors:
        return 2
    print(f"[OK] {args.outbox}: {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} valid")
    return 0


def parse_issue_body(text: str) -> dict[str, str]:
    """Split a GitHub Issue Form body into ``{label: value}``.

    A form renders each field as ``### <label>`` followed by its value; an
    empty optional field renders as ``_No response_``. A value fenced by a
    ``render:`` textarea loses its fence lines.

    Args:
        text: The issue body.

    Returns:
        dict[str, str]: Field label to stripped value; empty for no response.
    """
    fields: dict[str, str] = {}
    headings = list(ISSUE_HEADING.finditer(text))
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        value = text[heading.end() : end].strip()
        if value.startswith("```") and value.endswith("```") and "\n" in value:
            value = value.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        fields[heading.group(1)] = "" if value == NO_RESPONSE else value
    return fields


def _content_labels(fields: dict[str, str], body: str, config: dict[str, Any]) -> list[str]:
    """Labels decided by the issue's own text (schema, evidence, scan, words, pin).

    Args:
        fields: Parsed form fields.
        body: The whole issue body.
        config: Intake thresholds.

    Returns:
        list[str]: Labels in plan D3 order.
    """
    labels: list[str] = []
    if any(not fields.get(key) for key in ISSUE_REQUIRED):
        labels.append("needs-schema")
    if not (fields.get("evidence_command") and fields.get("evidence_output")):
        labels.append("needs-evidence")
    if scan_text(body) or not CHECKED_BOX.search(fields.get("genericized", "")):
        labels.append("needs-genericization")
    lowered = body.lower()
    words = [str(word).lower() for word in config["security_words"]]
    if fields.get("channel") == "C" or any(word in lowered for word in words):
        labels.append("security-suspect")
    return labels


def issue_labels(
    body: str, config: dict[str, Any], open_titles: list[str], author_recent: int
) -> list[str]:
    """Compute the intake labels of one ``host-finding`` issue (plan D3).

    Args:
        body: The issue body.
        config: Intake thresholds.
        open_titles: Titles of the other open ``host-finding`` issues.
        author_recent: ``host-finding`` issues the author opened in 24 hours,
            this one included.

    Returns:
        list[str]: Labels to apply; empty when the issue passes every check.
    """
    fields = parse_issue_body(body)
    labels = _content_labels(fields, body, config)
    title = fields.get("title", "").strip().lower()
    duplicate_title = bool(title) and title in {t.strip().lower() for t in open_titles}
    if fields.get("recurs") or duplicate_title:
        labels.append("possible-duplicate")
    pin = parse_pin(fields.get("pin", ""))
    if pin is None or pin < parse_pin(config["min_pin"]):
        labels.append("unsupported-pin")
    if author_recent > config["rate_limit_per_day"]:
        labels.append("rate-limited")
    return labels


def cmd_check_issue(args: argparse.Namespace) -> int:
    """Run ``check-issue``: print one intake label per line.

    Args:
        args: Parsed arguments.

    Returns:
        int: 0 once the labels are printed.
    """
    config = load_config(agents_root())
    body = read_text_file(Path(args.body_file))
    titles_text = read_text_file(Path(args.open_titles_file)) if args.open_titles_file else ""
    titles = [line for line in titles_text.splitlines() if line.strip()]
    for label in issue_labels(body, config, titles, args.author_recent_count):
        print(label)
    return 0


def render_issue_body(entry: dict[str, Any]) -> str:
    """Render an entry as the body of the ``host-finding`` Issue Form.

    Args:
        entry: A valid, genericized channel B entry.

    Returns:
        str: The body, in the shape ``parse_issue_body`` reads back.
    """
    sections = [
        ("id", entry["id"]),
        ("title", entry["title"]),
        ("defect", entry["defect"]),
        ("evidence_command", f"```shell\n{entry['evidence']['command']}\n```"),
        ("evidence_output", f"```shell\n{entry['evidence']['output']}\n```"),
        ("nucleus_artifact", entry["nucleus_artifact"]),
        ("proposed_change", entry["proposed_change"]),
        ("pin", entry["pin"]),
        ("channel", entry["channel"]),
        ("recurs", entry["recurs"] or NO_RESPONSE),
        ("genericized", GENERICIZED_LINE),
    ]
    return "\n\n".join(f"### {label}\n\n{value}" for label, value in sections) + "\n"


def export_refusal(entry: dict[str, Any]) -> str:
    """Return why an entry may not leave the host as a public issue.

    Args:
        entry: An outbox entry.

    Returns:
        str: The refusal, or an empty string when the export may proceed.
    """
    problems = entry_errors(entry)
    if problems:
        return "; ".join(problems)
    if entry["channel"] == "C":
        return "channel C goes through Private Vulnerability Reporting (SECURITY.md); a public issue is prohibited"
    if entry["channel"] == "A":
        return "channel A is pulled by the nucleus from this outbox; there is nothing to export"
    if not entry["genericized"]:
        return "`genericized` is false; the host's human signs it after genericizing (RA-15)"
    if entry["status"] != "drafted":
        return f"status is `{entry['status']}`, not `drafted`"
    return ""


def cmd_export(args: argparse.Namespace) -> int:
    """Run ``export``: write a channel B issue body and print the ``gh`` command.

    Args:
        args: Parsed arguments with ``outbox``, ``id`` and ``out``.

    Returns:
        int: 0 when the body was written, 2 when the export is refused.
    """
    matches = [e for e in load_entries(Path(args.outbox)) if e.get("id") == args.id]
    if len(matches) != 1:
        print(f"[FAIL] {args.id}: {len(matches)} entries carry this id, expected 1")
        return 2
    refusal = export_refusal(matches[0])
    if refusal:
        print(f"[FAIL] {args.id}: export refused — {refusal}")
        return 2
    out = Path(args.out)
    out.write_text(render_issue_body(matches[0]), encoding="utf-8")
    slug = load_json(agents_root() / IDENTITY_PATH)["framework_repo_slug"]
    command = [
        "gh", "issue", "create", "--repo", slug, "--title", matches[0]["title"],
        "--body-file", str(out), "--label", "host-finding",
    ]
    print(f"[OK] {args.id}: issue body written to {out}. The human runs:")
    print(shlex.join(command))
    print(f"Then set `status` to `sent:#<issue number>` for {args.id}.")
    return 0


def _git(repo: Path, *argv: str) -> str | None:
    """Run ``git -C repo argv`` and return stdout, or None when git fails.

    Args:
        repo: Directory inside the host repository.
        *argv: Git arguments.

    Returns:
        str | None: Standard output, or None on a non-zero exit, when git
            cannot run (``OSError``) or when its output is not UTF-8 (a
            ``ValueError``, e.g. under ``i18n.logOutputEncoding``).
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *argv], capture_output=True, text=True,
            encoding="utf-8", check=False,
        )
    except (OSError, ValueError):
        return None
    return result.stdout if result.returncode == 0 else None


def sprints_since_drafted(outbox: Path, entry_id: str) -> int | None:
    """Count distinct sprints committed since an entry entered the outbox.

    The entry's introducing commit is the oldest commit whose diff adds or
    removes ``"id": "<entry_id>"`` in the outbox. Sprints are the distinct
    ``#<digits>`` subject suffixes (``agents.md §5 historical_log``) of the
    commits after it.

    Args:
        outbox: The outbox file, tracked in the host repository.
        entry_id: The entry id.

    Returns:
        int | None: The count, or None when the history cannot be read.
    """
    pattern = f'"id": *"{re.escape(entry_id)}"'
    log = _git(outbox.parent, "log", "--format=%H", "-G", pattern, "--", outbox.name)
    if not log or not log.split():
        return None
    subjects = _git(outbox.parent, "log", "--format=%s", f"{log.split()[-1]}..HEAD")
    if subjects is None:
        return None
    matches = (SPRINT_SUFFIX.search(line) for line in subjects.splitlines())
    return len({match.group(1) for match in matches if match})


def cmd_aged(args: argparse.Namespace) -> int:
    """Run ``aged``: list ``drafted`` entries older than the configured sprints.

    Args:
        args: Parsed arguments with ``outbox``.

    Returns:
        int: 0 always once the outbox parses (advisory, plan Q3).
    """
    limit = load_config(agents_root())["aged_after_sprints"]
    outbox = Path(args.outbox).resolve()
    drafted = [e for e in load_entries(outbox) if e.get("status") == "drafted"]
    for entry in drafted:
        line = aged_line(str(entry.get("id")), sprints_since_drafted(outbox, str(entry.get("id"))), limit)
        if line:
            print(line)
    return 0


def aged_line(entry_id: str, count: int | None, limit: int) -> str:
    """Format the ``aged`` report line of one ``drafted`` entry.

    Args:
        entry_id: The entry id.
        count: Sprints since the entry was drafted; None when unmeasured.
        limit: ``aged_after_sprints``.

    Returns:
        str: The line, or an empty string when the entry is not aged.
    """
    if count is None:
        return f"[AGED?] {entry_id}: age unmeasured (outbox history unreadable)"
    if count >= limit:
        return f"[AGED] {entry_id}: drafted {count} sprints ago (limit {limit}); send or discard it"
    return ""


def cmd_deltas(args: argparse.Namespace) -> int:
    """Run ``deltas``: list host rule deltas whose outbox entry has shipped.

    Args:
        args: Parsed arguments with ``outbox`` and ``rules``.

    Returns:
        int: 0 always once the outbox parses (advisory, plan D4 element 6).
    """
    status = {e.get("id"): str(e.get("status")) for e in load_entries(Path(args.outbox))}
    for where, entry_id in delta_tags(Path(args.rules)):
        state = status.get(entry_id)
        if state is None or state.startswith("shipped:"):
            verdict = f"is {state}; delete the host delta" if state else "names no outbox entry"
            print(f"[DELTA] {where}: outbox:{entry_id} {verdict}")
    return 0


def delta_tags(rules: Path) -> list[tuple[str, str]]:
    """Find every ``outbox:<id>`` tag in the Markdown files under ``rules``.

    Args:
        rules: The host's rule directory.

    Returns:
        list[tuple[str, str]]: ``(<file>:<line>, <id>)`` in file and line order.
    """
    tags: list[tuple[str, str]] = []
    for path in sorted(rules.rglob("*.md")):
        lines = read_text_file(path).splitlines()
        tags += [
            (f"{path}:{number}", entry_id)
            for number, line in enumerate(lines, start=1)
            for entry_id in DELTA_TAG.findall(line)
        ]
    return tags


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    Returns:
        argparse.ArgumentParser: Parser with the five subcommands.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("outbox")
    issue = sub.add_parser("check-issue")
    issue.add_argument("--body-file", required=True)
    issue.add_argument("--open-titles-file")
    issue.add_argument("--author-recent-count", type=int, default=0)
    export = sub.add_parser("export")
    export.add_argument("outbox")
    export.add_argument("--id", required=True)
    export.add_argument("--out", required=True)
    aged = sub.add_parser("aged")
    aged.add_argument("outbox")
    deltas = sub.add_parser("deltas")
    deltas.add_argument("outbox")
    deltas.add_argument("--rules", required=True)
    return parser


COMMANDS = {
    "check": cmd_check,
    "check-issue": cmd_check_issue,
    "export": cmd_export,
    "aged": cmd_aged,
    "deltas": cmd_deltas,
}


def main(argv: list[str] | None = None) -> int:
    """Dispatch a subcommand.

    Args:
        argv: Arguments without the program name; None reads ``sys.argv``.

    Returns:
        int: Process exit code.
    """
    args = build_parser().parse_args(argv)
    try:
        return COMMANDS[args.command](args)
    except OutboxError as exc:
        print(f"[FAIL] {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
