"""Tests for scripts/upstream_outbox.py.

A gate proven only on a healthy tree proves nothing — each check below is first
shown failing on a fixture built to trip it.
"""

from __future__ import annotations

import copy
import json
import os
import re
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


# QA Gate 1 round 4, QA4-4: the duplicate-key check was quadratic
# (``keys.count`` per key; 32,000 keys took 5.56 s at boot on host input).
# Measured as a count of key comparisons, not wall-clock, so it cannot flake.
class _CountingKey(str):
    """A JSON key that counts how often it is compared for equality."""

    comparisons = 0
    __hash__ = str.__hash__

    def __eq__(self, other: object) -> bool:
        type(self).comparisons += 1
        return str.__eq__(self, other)


def test_duplicate_key_check_compares_keys_a_linear_number_of_times() -> None:
    size = 400
    pairs = [(_CountingKey(f"k{n}"), n) for n in range(size)]
    _CountingKey.comparisons = 0
    assert upstream_outbox._reject_duplicate_keys(pairs) == {f"k{n}": n for n in range(size)}
    assert _CountingKey.comparisons <= size


@pytest.mark.parametrize(
    ("pairs", "message"),
    [
        ([("b", 1), ("a", 2), ("b", 3), ("a", 4), ("a", 5), ("c", 6)], "duplicate key(s) a, b"),
        ([("x", 1), ("x", 2)], "duplicate key(s) x"),
    ],
)
def test_duplicate_key_message_lists_each_repeat_once_sorted(
    pairs: list[tuple[str, int]], message: str
) -> None:
    with pytest.raises(upstream_outbox.OutboxError) as raised:
        upstream_outbox._reject_duplicate_keys(pairs)
    assert str(raised.value) == message


def test_duplicate_key_check_keeps_order_and_values_without_repeats() -> None:
    pairs = [("z", 1), ("a", [2]), ("m", {"n": 3})]
    assert list(upstream_outbox._reject_duplicate_keys(pairs).items()) == pairs


def test_absent_or_malformed_outbox_exits_2(tmp_path: Path) -> None:
    assert _run("check", str(tmp_path / "absent.json")).returncode == 2
    path = tmp_path / "outbox.json"
    path.write_text("[]", encoding="utf-8")
    assert _run("check", str(path)).returncode == 2


# QA Gate 1 round 5 self-attack: a host controls what its outbox path names.
# A FIFO blocked the read forever and /dev/zero read until memory ran out, so
# each case runs in a subprocess with a timeout; on the unfixed tree the
# timeout is the observed failure. The cap is stated here, not imported, so the
# parent fails on behaviour rather than on a missing name.
READ_CAP = 4 * 1024 * 1024
READ_TIMEOUT = 10


def _check_within_timeout(path: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "check", str(path)],
            capture_output=True, text=True, check=False, timeout=READ_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"check on {path.name} did not finish within {READ_TIMEOUT} s")


def _fifo(tmp_path: Path) -> Path:
    path = tmp_path / "outbox.fifo"
    os.mkfifo(path)
    return path


def _over_cap(tmp_path: Path) -> Path:
    path = tmp_path / "big.json"
    path.write_bytes(b'{"entries": []}'.ljust(READ_CAP + 1))
    return path


def _symlink_to_fifo(tmp_path: Path) -> Path:
    link = tmp_path / "link.json"
    link.symlink_to(_fifo(tmp_path))
    return link


NOT_A_BOUNDED_REGULAR_FILE = {
    "fifo": _fifo,
    "symlink_to_fifo": _symlink_to_fifo,
    "char_device": lambda _tmp: Path("/dev/zero"),
    "directory": lambda tmp: tmp,
    "over_cap": _over_cap,
}


@pytest.mark.parametrize(
    "make", list(NOT_A_BOUNDED_REGULAR_FILE.values()), ids=list(NOT_A_BOUNDED_REGULAR_FILE)
)
def test_outbox_that_is_not_a_bounded_regular_file_exits_2_without_hanging(
    tmp_path: Path, make: Any
) -> None:
    path = make(tmp_path)
    if not path.exists():
        pytest.skip(f"{path} does not exist on this platform")
    result = _check_within_timeout(path)
    assert "Traceback" not in result.stderr
    assert result.returncode == 2
    assert result.stdout.startswith("[FAIL] ")


def test_outbox_at_the_read_cap_is_still_read(tmp_path: Path) -> None:
    path = tmp_path / "at_cap.json"
    path.write_bytes(b'{"entries": []}'.ljust(READ_CAP))
    result = _check_within_timeout(path)
    assert (result.returncode, "[FAIL]" in result.stdout) == (0, False)
    assert upstream_outbox.MAX_READ_BYTES == READ_CAP


def test_intake_reports_a_fifo_outbox_and_lists_the_other_host(tmp_path: Path) -> None:
    fifo = _fifo(tmp_path)
    good = _outbox(tmp_path, _entry(channel="A"))
    root = tmp_path / "nucleus"
    root.mkdir()
    hosts = {"hosts": [{"name": "bad", "outbox": str(fifo)}, {"name": "ok", "outbox": str(good)}]}
    (root / ".upstream_hosts.json").write_text(json.dumps(hosts), encoding="utf-8")
    code = (
        f"import sys; sys.path.insert(0, {str(REPO / 'scripts')!r})\n"
        "from pathlib import Path\nimport upstream_intake\n"
        f"upstream_intake.agents_root = lambda: Path({str(root)!r})\n"
        "sys.exit(upstream_intake.main())\n"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-I", "-c", code],
            capture_output=True, text=True, check=False, timeout=READ_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"intake did not finish within {READ_TIMEOUT} s on a FIFO outbox")
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    lines = result.stdout.splitlines()
    assert re.fullmatch(r"- bad: outbox unreadable or unprocessable \(\w+\)", lines[1])
    assert lines[2:] == ["- ok: H-7 | drafted | A | scripts/check_gate_log.py"]


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


# QA Gate 1 round 4, QA4-2: an outbox that parses but carries an unhashable
# ``id`` crashed ``deltas`` with TypeError. Every non-string id is skipped and
# reported by position; the other entries are still evaluated.
@pytest.mark.parametrize("bad_id", [["H-7"], {"x": 1}, 7, None], ids=["list", "dict", "int", "null"])
def test_deltas_skips_a_non_string_id_and_still_evaluates_the_rest(
    tmp_path: Path, bad_id: Any
) -> None:
    outbox = _outbox(tmp_path, _entry(id=bad_id), _entry(status="shipped:v4.41.0"))
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "local.md").write_text("Rule A outbox:H-7\n", encoding="utf-8")
    result = _run("deltas", str(outbox), "--rules", str(rules))
    assert "Traceback" not in result.stdout + result.stderr
    assert result.returncode == 0
    assert result.stdout.splitlines() == [
        "[SKIP] entry 1: id is not a string",
        f"[DELTA] {rules / 'local.md'}:1: outbox:H-7 is shipped:v4.41.0; delete the host delta",
    ]


# Pre-emptive QA Gate 1 round 4, U12: every file the script reads fails closed
# on decode. The outbox, config and identity files go through load_json
# (QA3-1); the issue body, the open titles file, the rule files of `deltas` and
# the git history of `aged` were read outside it.
NOT_UTF8 = b"### id\n\nH-7 outbox:H-7 \xff\n"


def _read_sites(tmp_path: Path) -> dict[str, tuple[list[str], Path]]:
    bad = tmp_path / "bad.md"
    bad.write_bytes(NOT_UTF8)
    raw = tmp_path / "raw.json"
    raw.write_bytes(UNDECODABLE["non_utf8"])
    body = tmp_path / "body.md"
    body.write_text(_issue(), encoding="utf-8")
    outbox = _outbox(tmp_path, _entry())
    rules = tmp_path / "rules"
    rules.mkdir()
    (rules / "local.md").write_bytes(NOT_UTF8)
    folder = tmp_path / "folder"
    (folder / "dir.md").mkdir(parents=True)
    return {
        "check-outbox": (["check", str(raw)], raw),
        "check-issue-body": (["check-issue", "--body-file", str(bad)], bad),
        "check-issue-open-titles": (
            ["check-issue", "--body-file", str(body), "--open-titles-file", str(bad)], bad
        ),
        "export-outbox": (["export", str(raw), "--id", "H-7", "--out", str(tmp_path / "o.md")], raw),
        "aged-outbox": (["aged", str(raw)], raw),
        "deltas-outbox": (["deltas", str(raw), "--rules", str(rules)], raw),
        "deltas-rule-file": (["deltas", str(outbox), "--rules", str(rules)], rules / "local.md"),
        "deltas-rule-is-dir": (["deltas", str(outbox), "--rules", str(folder)], folder / "dir.md"),
    }


SITES = (
    "check-outbox", "check-issue-body", "check-issue-open-titles", "export-outbox",
    "aged-outbox", "deltas-outbox", "deltas-rule-file", "deltas-rule-is-dir", "aged-git-log",
)


def _aged_with_undecodable_log(tmp_path: Path) -> list[str]:
    outbox = _repo_with_outbox(tmp_path, 1)
    (outbox.parent / "g").write_text("x", encoding="utf-8")
    _git(outbox.parent, "add", "g")
    _git(outbox.parent, "commit", "-q", "-m", "feat: café #003")
    _git(outbox.parent, "config", "i18n.logOutputEncoding", "latin1")
    return ["aged", str(outbox)]


@pytest.mark.parametrize("site", SITES)
def test_every_read_fails_closed_without_traceback(tmp_path: Path, site: str) -> None:
    if site == "aged-git-log":
        argv, expected, marker = _aged_with_undecodable_log(tmp_path), 0, "[AGED?] H-7"
    else:
        argv, named = _read_sites(tmp_path)[site]
        expected, marker = 2, str(named)
    result = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), *argv],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == expected, result.stderr
    assert "Traceback" not in result.stderr
    assert marker in result.stdout


@pytest.mark.parametrize("subcommand", ["check-issue", "aged", "export"])
def test_config_and_identity_reads_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], subcommand: str
) -> None:
    """The framework config and identity files are read through load_json too."""
    root = tmp_path / "root"
    (root / "config").mkdir(parents=True)
    for name in (upstream_outbox.CONFIG_PATH, upstream_outbox.IDENTITY_PATH):
        (root / name).write_bytes(UNDECODABLE["non_utf8"])
    monkeypatch.setattr(upstream_outbox, "agents_root", lambda: root)
    body = tmp_path / "body.md"
    body.write_text(_issue(), encoding="utf-8")
    outbox = str(_outbox(tmp_path, _entry()))
    argv = {
        "check-issue": ["check-issue", "--body-file", str(body)],
        "aged": ["aged", outbox],
        "export": ["export", outbox, "--id", "H-7", "--out", str(tmp_path / "o.md")],
    }[subcommand]
    assert upstream_outbox.main(argv) == 2
    assert str(root / "config") in capsys.readouterr().out


STATUS_ERROR = "`status` must be drafted, or sent:/triaged:/shipped:/rejected: + text"


@pytest.mark.parametrize(
    ("status", "valid"),
    [
        ("drafted", True),
        ("sent:#4 by mail", True),
        ("triaged:accept", True),
        ("shipped:v4.41.0", True),
        ("rejected:dup of H-1", True),
        ("drafted\n", False),
        ("sent:x\n", False),
        ("shipped:v4.41.0\n", False),
        ("sent:x\ny", False),
        ("sent:", False),
    ],
)
def test_status_is_full_matched(status: str, valid: bool) -> None:
    """U13: ``$`` matches before a trailing newline; the status check must not."""
    assert (STATUS_ERROR not in upstream_outbox.entry_errors(_entry(status=status))) is valid


@pytest.mark.parametrize("pin", ["v4.40.0\n", "4.40.0\n", " v4.40.0", "v4.40.0 "])
def test_pin_is_full_matched(pin: str) -> None:
    """U13: ``parse_pin`` stripped its input, so a newline-padded pin validated."""
    assert upstream_outbox.parse_pin(pin) is None
    assert "`pin` must be vX.Y.Z" in upstream_outbox.entry_errors(_entry(pin=pin))
    assert upstream_outbox.parse_pin(pin.strip()) == (4, 40, 0)
