"""Tests for scripts/upstream_outbox.py.

A gate proven only on a healthy tree proves nothing — each check below is first
shown failing on a fixture built to trip it.
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "upstream_outbox.py"
TEMPLATE = REPO / "docs" / "standards" / "templates" / "UPSTREAM_OUTBOX_TEMPLATE.json"
CONFIG = json.loads((REPO / "config" / "upstream_intake.json").read_text(encoding="utf-8"))

sys.path.insert(0, str(REPO / "scripts"))
import upstream_outbox

ENTRY: dict[str, Any] = {
    "id": "H-7",
    "title": "Gate log rejects an escaped pipe",
    "defect": "A Notes cell with an escaped pipe is split in two.",
    "evidence": {
        "command": "python3 .agents/scripts/check_gate_log.py --sprint-dir docs/sprints/042-x",
        "output": "[FAIL] gate row has 7 cells, expected 6",
    },
    "nucleus_artifact": "scripts/check_gate_log.py",
    "proposed_change": "Use the separator of check_task_scope.py.",
    "pin": CONFIG["min_pin"],
    "genericized": True,
    "channel": "B",
    "recurs": None,
    "status": "drafted",
}


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd or REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def _outbox(tmp_path: Path, *entries: dict[str, Any]) -> Path:
    path = tmp_path / "outbox.json"
    path.write_text(json.dumps({"entries": list(entries)}, indent=2), encoding="utf-8")
    return path


def _entry(**changes: Any) -> dict[str, Any]:
    entry = copy.deepcopy(ENTRY)
    entry.update(changes)
    return entry


def test_template_passes_check() -> None:
    result = _run("check", str(TEMPLATE))
    assert result.returncode == 0, result.stdout
    assert "[OK]" in result.stdout


def test_valid_entry_passes(tmp_path: Path) -> None:
    assert _run("check", str(_outbox(tmp_path, _entry()))).returncode == 0


@pytest.mark.parametrize(
    "changes",
    [
        {"status": "sent:#12", "genericized": False},
        {"status": "queued"},
        {"channel": "D"},
        {"pin": "latest"},
        {"id": "../escape"},
        {"recurs": ""},
        {"genericized": "yes"},
        {"evidence": {"command": "x"}},
        {"title": ""},
        {"surprise": 1},
    ],
)
def test_invalid_entry_exits_2(tmp_path: Path, changes: dict[str, Any]) -> None:
    result = _run("check", str(_outbox(tmp_path, _entry(**changes))))
    assert result.returncode == 2, result.stdout


def test_id_with_trailing_newline_is_invalid() -> None:
    """QA2-1: ``$`` matches before a trailing newline; the id check must not."""
    assert upstream_outbox.entry_errors(_entry()) == []
    assert "`id` must match [A-Za-z0-9][A-Za-z0-9._-]*" in upstream_outbox.entry_errors(
        _entry(id="H-2\n")
    )


def test_missing_key_exits_2(tmp_path: Path) -> None:
    entry = _entry()
    del entry["status"]
    assert _run("check", str(_outbox(tmp_path, entry))).returncode == 2


def test_duplicate_id_exits_2(tmp_path: Path) -> None:
    assert _run("check", str(_outbox(tmp_path, _entry(), _entry()))).returncode == 2


def test_duplicate_json_key_exits_2(tmp_path: Path) -> None:
    path = tmp_path / "outbox.json"
    path.write_text('{"entries": [], "entries": []}', encoding="utf-8")
    assert _run("check", str(path)).returncode == 2


def test_absent_or_malformed_outbox_exits_2(tmp_path: Path) -> None:
    assert _run("check", str(tmp_path / "absent.json")).returncode == 2
    path = tmp_path / "outbox.json"
    path.write_text("[]", encoding="utf-8")
    assert _run("check", str(path)).returncode == 2


# QA Gate 1 round 3, QA3-1: every decode-time failure is a malformed outbox.
UNDECODABLE = {
    "non_utf8": b'{"entries": [\xff]}',
    "deep_nesting": b'{"entries": [' + b"[" * 100000 + b"]" * 100000 + b"]}",
    "over_int_limit": b'{"entries": [{"x": ' + b"9" * 5000 + b"}]}",
    "lone_surrogate": b'{"entries": [{"id": "\\ud800"}]}',
}


@pytest.mark.parametrize("raw", list(UNDECODABLE.values()), ids=list(UNDECODABLE))
def test_undecodable_outbox_exits_2_without_traceback(tmp_path: Path, raw: bytes) -> None:
    path = tmp_path / "outbox.json"
    path.write_bytes(raw)
    result = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "check", str(path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2, result.stderr
    assert "Traceback" not in result.stderr
    assert str(path) in result.stdout + result.stderr


@pytest.mark.parametrize(
    ("text", "family"),
    [
        ("see /home/example/project/app.py", "posix-path"),
        (r"see C:\Users\someone\app.py", "windows-path"),
        ("mail owner@example.org", "email"),
        ('API_KEY = "abcd1234efgh"', "secret-assignment"),
        ("ACCESS_TOKEN=abcd1234efgh", "secret-assignment"),
    ],
)
def test_scan_families(text: str, family: str) -> None:
    assert family in upstream_outbox.scan_text(text)


@pytest.mark.parametrize(
    "text",
    [
        "python3 .agents/scripts/check_gate_log.py",
        "https://github.com/owner/repo/issues/3",
        "docs/sprints/042-x/SPRINT_LOG.md",
        "~/notes/file.md",
        "and/or the /verify step",
    ],
)
def test_scan_ignores_relative_text(text: str) -> None:
    assert upstream_outbox.scan_text(text) == []


def test_genericized_entry_with_path_fails_without_echoing_it(tmp_path: Path) -> None:
    entry = _entry(defect="Broke in /Users/example/hostproject/app.py")
    result = _run("check", str(_outbox(tmp_path, entry)))
    assert result.returncode == 2
    assert "defect: posix-path" in result.stdout
    assert "hostproject" not in result.stdout


def test_ungenericized_draft_is_a_note(tmp_path: Path) -> None:
    entry = _entry(genericized=False, defect="Broke in /Users/example/hostproject/app.py")
    result = _run("check", str(_outbox(tmp_path, entry)))
    assert result.returncode == 0, result.stdout
    assert "[NOTE] H-7: defect: posix-path" in result.stdout


@pytest.mark.parametrize(
    ("changes", "reason"),
    [
        ({"channel": "C"}, "Private Vulnerability Reporting"),
        ({"channel": "A"}, "pulled by the nucleus"),
        ({"genericized": False}, "`genericized` is false"),
        ({"status": "sent:#4"}, "not `drafted`"),
    ],
)
def test_export_refusals(tmp_path: Path, changes: dict[str, Any], reason: str) -> None:
    out = tmp_path / "body.md"
    result = _run("export", str(_outbox(tmp_path, _entry(**changes))), "--id", "H-7", "--out", str(out))
    assert result.returncode == 2
    assert reason in result.stdout
    assert not out.exists()


def test_export_unknown_id_exits_2(tmp_path: Path) -> None:
    out = tmp_path / "body.md"
    result = _run("export", str(_outbox(tmp_path, _entry())), "--id", "H-9", "--out", str(out))
    assert result.returncode == 2


def test_export_round_trips_through_check_issue(tmp_path: Path) -> None:
    out = tmp_path / "body.md"
    result = _run("export", str(_outbox(tmp_path, _entry())), "--id", "H-7", "--out", str(out))
    assert result.returncode == 0, result.stdout
    assert "gh issue create --repo" in result.stdout
    assert "--label host-finding" in result.stdout
    labels = _run("check-issue", "--body-file", str(out))
    assert labels.returncode == 0
    assert labels.stdout == ""


def _issue(**changes: Any) -> str:
    return upstream_outbox.render_issue_body(_entry(**changes))


@pytest.mark.parametrize(
    ("body", "label"),
    [
        (_issue().replace("### pin\n\n" + CONFIG["min_pin"], "### pin\n\n_No response_"), "needs-schema"),
        (_issue(evidence={"command": "x", "output": "x"}).replace("```shell\nx\n```", "_No response_"), "needs-evidence"),
        (_issue(defect="mail owner@example.org"), "needs-genericization"),
        (_issue().replace("- [X]", "- [ ]"), "needs-genericization"),
        (_issue(defect="the sandbox lets it through"), "security-suspect"),
        (_issue(channel="C"), "security-suspect"),
        (_issue(recurs="F-107-N1"), "possible-duplicate"),
        (_issue(pin="v1.0.0"), "unsupported-pin"),
    ],
)
def test_check_issue_labels(tmp_path: Path, body: str, label: str) -> None:
    path = tmp_path / "body.md"
    path.write_text(body, encoding="utf-8")
    result = _run("check-issue", "--body-file", str(path))
    assert result.returncode == 0
    assert label in result.stdout.splitlines()


def test_check_issue_duplicate_title_and_rate_limit(tmp_path: Path) -> None:
    body = tmp_path / "body.md"
    body.write_text(_issue(), encoding="utf-8")
    titles = tmp_path / "titles.txt"
    titles.write_text(ENTRY["title"].upper() + "\n", encoding="utf-8")
    over = str(CONFIG["rate_limit_per_day"] + 1)
    result = _run(
        "check-issue", "--body-file", str(body), "--open-titles-file", str(titles),
        "--author-recent-count", over,
    )
    assert result.stdout.splitlines() == ["possible-duplicate", "rate-limited"]
    at_limit = _run("check-issue", "--body-file", str(body), "--author-recent-count", str(CONFIG["rate_limit_per_day"]))
    assert at_limit.stdout == ""


def test_check_issue_absent_body_exits_2(tmp_path: Path) -> None:
    assert _run("check-issue", "--body-file", str(tmp_path / "absent.md")).returncode == 2


def _git(repo: Path, *argv: str) -> None:
    subprocess.run(["git", "-C", str(repo), *argv], check=True, capture_output=True)


def _repo_with_outbox(tmp_path: Path, later_sprints: int) -> Path:
    repo = tmp_path / "host"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    outbox = _outbox(repo, _entry())
    _git(repo, "add", outbox.name)
    _git(repo, "commit", "-q", "-m", "docs: draft H-7 #001")
    for sprint in range(2, 2 + later_sprints):
        (repo / f"f{sprint}").write_text("x", encoding="utf-8")
        _git(repo, "add", f"f{sprint}")
        _git(repo, "commit", "-q", "-m", f"feat: work #{sprint:03d}")
    return outbox


def test_aged_lists_old_draft(tmp_path: Path) -> None:
    outbox = _repo_with_outbox(tmp_path, CONFIG["aged_after_sprints"])
    result = _run("aged", str(outbox))
    assert result.returncode == 0
    assert result.stdout.startswith("[AGED] H-7:")


def test_aged_skips_young_draft(tmp_path: Path) -> None:
    outbox = _repo_with_outbox(tmp_path, CONFIG["aged_after_sprints"] - 1)
    result = _run("aged", str(outbox))
    assert (result.returncode, result.stdout) == (0, "")


def test_aged_untracked_outbox_is_unmeasured(tmp_path: Path) -> None:
    result = _run("aged", str(_outbox(tmp_path, _entry())))
    assert result.returncode == 0
    assert "[AGED?] H-7" in result.stdout


def test_deltas_lists_shipped_and_unknown(tmp_path: Path) -> None:
    outbox = _outbox(tmp_path, _entry(status="shipped:v4.41.0"))
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "local.md").write_text("Rule A outbox:H-7\nRule B outbox:H-8\n", encoding="utf-8")
    result = _run("deltas", str(outbox), "--rules", str(rules))
    assert result.returncode == 0
    assert "local.md:1: outbox:H-7 is shipped:v4.41.0" in result.stdout
    assert "local.md:2: outbox:H-8 names no outbox entry" in result.stdout


def test_deltas_silent_while_not_shipped(tmp_path: Path) -> None:
    outbox = _outbox(tmp_path, _entry(status="sent:#4"))
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "local.md").write_text("Rule A outbox:H-7\n", encoding="utf-8")
    assert _run("deltas", str(outbox), "--rules", str(rules)).stdout == ""
