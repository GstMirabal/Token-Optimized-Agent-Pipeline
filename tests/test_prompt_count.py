"""Tests for scripts/prompt_count.py with synthetic transcripts only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import prompt_count as pc
import session_cost


def tool_use(message_id: str, use_id: str) -> dict:
    """An assistant record holding one tool_use block."""
    return {"type": "assistant", "message": {"id": message_id, "content": [
        {"type": "tool_use", "id": use_id, "name": "Bash"}]}}


def tool_result(use_id: str, decision: dict | None) -> dict:
    """A user record holding one tool_result and an optional decision."""
    record = {"type": "user", "message": {"content": [
        {"type": "tool_result", "tool_use_id": use_id, "content": "ok"}]}}
    if decision is not None:
        record["permissionDecision"] = decision
    return record


def write(path: Path, records: list[dict], extra: str = "") -> Path:
    """Write records as JSONL, plus raw trailing text."""
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n" + extra,
                    encoding="utf-8")
    return path


def test_counts_each_source(tmp_path: Path) -> None:
    records = [
        tool_use("m1", "t1"), tool_result("t1", {"decision": "accept", "source": "config"}),
        tool_use("m2", "t2"), tool_result("t2", {"decision": "accept", "source": "user_temporary"}),
        tool_use("m3", "t3"), tool_result("t3", {"decision": "accept", "source": "user_temporary",
                                                 "grantScope": "once"}),
        tool_use("m4", "t4"), tool_result("t4", {"decision": "accept", "source": "hook"}),
        tool_use("m5", "t5"), tool_result("t5", None),
    ]
    result = pc.count_transcript(write(tmp_path / "abc.jsonl", records))
    assert result == {
        "session": "abc", "tool_use_total": 5, "decisions_user_approved": 2,
        "decisions_user_approved_once": 1, "decisions_by_config": 1,
        "decisions_other_source": 1, "tool_uses_without_decision": 1,
    }


def test_repeated_message_id_is_not_counted_twice(tmp_path: Path) -> None:
    records = [tool_use("m1", "t1"), tool_use("m1", "t1"),
               tool_result("t1", {"decision": "accept", "source": "user_temporary"}),
               tool_result("t1", {"decision": "accept", "source": "user_temporary"})]
    result = pc.count_transcript(write(tmp_path / "s.jsonl", records))
    assert result["tool_use_total"] == 1
    assert result["decisions_user_approved"] == 1


def test_malformed_line_is_skipped(tmp_path: Path) -> None:
    path = write(tmp_path / "s.jsonl", [tool_use("m1", "t1")], extra="{not json\n[1]\n")
    assert pc.count_transcript(path)["tool_use_total"] == 1


def test_missing_transcript_exits_2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                    capsys: pytest.CaptureFixture) -> None:
    monkeypatch.setattr(session_cost, "PROJECTS", tmp_path)
    assert pc.main(["--session", "nope", "--project", str(tmp_path)]) == 2
    assert "No transcript found" in capsys.readouterr().err


def test_unreadable_transcript_exits_2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    directory = tmp_path / session_cost.project_slug(tmp_path)
    directory.mkdir()
    (directory / "bad.jsonl").mkdir()  # a directory cannot be read as a file
    monkeypatch.setattr(session_cost, "PROJECTS", tmp_path)
    assert pc.main(["--session", "bad", "--project", str(tmp_path)]) == 2


def test_json_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                     capsys: pytest.CaptureFixture) -> None:
    directory = tmp_path / session_cost.project_slug(tmp_path)
    directory.mkdir()
    write(directory / "ok.jsonl", [tool_use("m1", "t1")])
    monkeypatch.setattr(session_cost, "PROJECTS", tmp_path)
    assert pc.main(["--session", "ok", "--project", str(tmp_path), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["tool_use_total"] == 1


def approved(use_id: str) -> list[dict]:
    """A tool_use plus a user_temporary decision for it."""
    return [tool_use(f"m-{use_id}", use_id),
            tool_result(use_id, {"decision": "accept", "source": "user_temporary"})]


def test_subagent_transcripts_are_summed(tmp_path: Path) -> None:
    main = write(tmp_path / "abc.jsonl", approved("t1"))
    subagents = tmp_path / "abc" / "subagents"
    subagents.mkdir(parents=True)
    write(subagents / "agent-a.jsonl", approved("t2") + approved("t3"))
    write(subagents / "agent-b.jsonl", approved("t4"))
    result = pc.count_transcript(main)
    assert result["tool_use_total"] == 4
    assert result["decisions_user_approved"] == 4
    assert result["tool_uses_without_decision"] == 0


def test_tool_use_seen_in_main_and_subagent_counts_once(tmp_path: Path) -> None:
    main = write(tmp_path / "abc.jsonl", approved("t1"))
    subagents = tmp_path / "abc" / "subagents"
    subagents.mkdir(parents=True)
    write(subagents / "agent-a.jsonl", approved("t1") + approved("t2"))
    result = pc.count_transcript(main)
    assert result["tool_use_total"] == 2
    assert result["decisions_user_approved"] == 2


def test_session_without_subagents_directory_is_unchanged(tmp_path: Path) -> None:
    main = write(tmp_path / "abc.jsonl", approved("t1"))
    (tmp_path / "abc").mkdir()  # a session directory with no subagents/ inside
    result = pc.count_transcript(main)
    assert result["tool_use_total"] == 1
    assert result["decisions_user_approved"] == 1


def test_unreadable_subagent_transcript_exits_2(tmp_path: Path,
                                                monkeypatch: pytest.MonkeyPatch) -> None:
    directory = tmp_path / session_cost.project_slug(tmp_path)
    directory.mkdir()
    write(directory / "abc.jsonl", approved("t1"))
    (directory / "abc" / "subagents" / "bad.jsonl").mkdir(parents=True)
    monkeypatch.setattr(session_cost, "PROJECTS", tmp_path)
    assert pc.main(["--session", "abc", "--project", str(tmp_path)]) == 2
