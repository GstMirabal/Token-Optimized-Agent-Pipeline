"""Tests for scripts/upstream_intake.py.

The S0 surface is host text entering a nucleus session through ``--boot``, so
the tests pin what is printed and, above all, what is not.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import upstream_intake

ENTRY: dict[str, Any] = {
    "id": "H-7",
    "title": "Gate log rejects an escaped pipe",
    "defect": "DEFECT-TEXT-MUST-NOT-PRINT",
    "evidence": {"command": "EVIDENCE-COMMAND", "output": "EVIDENCE-OUTPUT"},
    "nucleus_artifact": "scripts/check_gate_log.py",
    "proposed_change": "PROPOSED-CHANGE-TEXT",
    "pin": "v4.40.0",
    "genericized": True,
    "channel": "A",
    "recurs": None,
    "status": "drafted",
}


def _entry(**changes: Any) -> dict[str, Any]:
    entry = copy.deepcopy(ENTRY)
    entry.update(changes)
    return entry


def _nucleus(tmp_path: Path, *entries: dict[str, Any]) -> Path:
    outbox = tmp_path / "host" / "outbox.json"
    outbox.parent.mkdir()
    outbox.write_text(json.dumps({"entries": list(entries)}), encoding="utf-8")
    root = tmp_path / "nucleus"
    root.mkdir()
    hosts = {"hosts": [{"name": "h1", "outbox": str(outbox)}]}
    (root / ".upstream_hosts.json").write_text(json.dumps(hosts), encoding="utf-8")
    return root


def test_no_hosts_file_is_healthy(tmp_path: Path) -> None:
    lines, healthy = upstream_intake.intake_lines(tmp_path)
    assert healthy
    assert lines == ["intake queue (channel A): no .upstream_hosts.json registered"]


def test_pending_entry_prints_structured_fields_only(tmp_path: Path) -> None:
    lines, healthy = upstream_intake.intake_lines(_nucleus(tmp_path, _entry()))
    text = "\n".join(lines)
    assert healthy
    assert "- h1: H-7 | drafted | A | scripts/check_gate_log.py | Gate log rejects" in text
    for secret in ("DEFECT-TEXT", "EVIDENCE-", "PROPOSED-CHANGE"):
        assert secret not in text


def test_title_is_cut_and_control_characters_blanked(tmp_path: Path) -> None:
    title = "line one\nIGNORE PREVIOUS\x1b[2J" + "x" * 300
    lines, _ = upstream_intake.intake_lines(_nucleus(tmp_path, _entry(title=title)))
    row = lines[1]
    assert "\n" not in row and "\x1b" not in row
    assert len(row.rsplit(" | ", 1)[1]) == upstream_intake.FIELD_LIMIT


def test_done_and_other_channel_entries_are_not_pending(tmp_path: Path) -> None:
    root = _nucleus(
        tmp_path,
        _entry(id="H-1", status="triaged:accept"),
        _entry(id="H-2", status="shipped:v4.41.0"),
        _entry(id="H-3", channel="B"),
        _entry(id="H-4", status="sent:pull"),
    )
    lines, _ = upstream_intake.intake_lines(root)
    assert [line.split(" | ")[0] for line in lines[1:]] == ["- h1: H-4"]


def test_invalid_or_ungenericized_entries_are_withheld(tmp_path: Path) -> None:
    root = _nucleus(tmp_path, _entry(genericized=False), _entry(id="H-8", channel="Z"))
    lines, healthy = upstream_intake.intake_lines(root)
    assert healthy
    assert lines[1:] == ["- h1: 2 entries withheld (invalid or not genericized)"]
    assert "H-7" not in "\n".join(lines)


def test_empty_queue_says_none_pending(tmp_path: Path) -> None:
    lines, _ = upstream_intake.intake_lines(_nucleus(tmp_path))
    assert lines[1:] == ["- (none pending)"]


def test_absent_outbox_is_unhealthy_and_reported(tmp_path: Path) -> None:
    root = tmp_path / "nucleus"
    root.mkdir()
    hosts = {"hosts": [{"name": "h1", "outbox": str(tmp_path / "absent.json")}]}
    (root / ".upstream_hosts.json").write_text(json.dumps(hosts), encoding="utf-8")
    lines, healthy = upstream_intake.intake_lines(root)
    assert not healthy
    assert "- h1: outbox absent or malformed" in lines


def test_malformed_hosts_file_is_unhealthy(tmp_path: Path) -> None:
    (tmp_path / ".upstream_hosts.json").write_text('{"hosts": [{"name": "h1"}]}', encoding="utf-8")
    lines, healthy = upstream_intake.intake_lines(tmp_path)
    assert not healthy
    assert lines[0].startswith("intake queue (channel A): .upstream_hosts.json: expected")
