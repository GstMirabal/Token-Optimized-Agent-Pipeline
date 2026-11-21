"""Tests for scripts/unit_cost.py (Sprint 059 unit H-04).

Every case builds a synthetic git repository and synthetic transcripts under
`tmp_path`; the real `~/.claude` is never read. Commit times are set through
`GIT_COMMITTER_DATE` and turn times through the record timestamps, so the
interval `(ct[k-1], ct[k]]` of rule C is exercised exactly at its edges.
"""

from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import unit_cost as uc

T0 = 1_700_000_000
HEADER = "| # | File | Operation | Risk | Assignee | Est. cost | Status |\n"
SEPARATOR = "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"


def git(repo: Path, *args: str, when: int | None = None) -> str:
    """Run git in `repo`, committing at epoch `when` when given."""
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    if when is not None:
        stamp = f"{when} +0000"
        env.update(GIT_COMMITTER_DATE=stamp, GIT_AUTHOR_DATE=stamp)
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          env=env, check=True)
    return done.stdout.strip()


def make_repo(tmp_path: Path, commits: list[tuple[str, int]]) -> tuple[Path, dict[str, str]]:
    """A repo with a `main` base commit at T0 - 100 and the named sprint commits on top.

    Args:
        tmp_path: pytest temporary directory.
        commits: (name, commit time offset from T0) in creation order.

    Returns:
        tuple: (repo path, name to short SHA).
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.email", "t@example.org")
    git(repo, "config", "user.name", "t")
    git(repo, "config", "commit.gpgsign", "false")
    (repo / "base.txt").write_text("base")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "base", when=T0 - 100)
    git(repo, "switch", "-c", "sprint")
    shas = {}
    for name, offset in commits:
        (repo / f"{name}.txt").write_text(name)
        git(repo, "add", ".")
        git(repo, "commit", "-m", name, when=T0 + offset)
        shas[name] = git(repo, "rev-parse", "--short", "HEAD")
    return repo, shas


def iso(offset: int) -> str:
    """ISO timestamp, as in a transcript record, for epoch T0 + offset."""
    moment = datetime.datetime.fromtimestamp(T0 + offset, tz=datetime.timezone.utc)
    return moment.isoformat().replace("+00:00", "Z")


def record(offset: int, ident: str, model: str = "m", **usage: int) -> dict:
    """One transcript record with a usage block."""
    return {"timestamp": iso(offset), "message": {"id": ident, "model": model, "usage": usage}}


def write_transcripts(projects: Path, repo: Path, name: str, records: list[dict],
                      subagent: bool = False) -> Path:
    """Write records as a main transcript, or as a subagent transcript of session `s`."""
    directory = projects / uc.project_slug(repo)
    if subagent:
        directory = directory / "s" / "subagents"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name}.jsonl"
    path.write_text("\n".join(json.dumps(item) for item in records) + "\n")
    return path


def write_scope(sprint: Path, rows: list[tuple[str, str, str]]) -> Path:
    """A task_scope.md with rows (id, Est. cost, Status)."""
    sprint.mkdir(parents=True, exist_ok=True)
    body = "".join(f"| {uid} | `f.py` | modify | low | a | {est} | {status} |\n"
                   for uid, est, status in rows)
    path = sprint / "task_scope.md"
    path.write_text(HEADER + SEPARATOR + body)
    return path


def run(repo: Path, tmp_path: Path, *extra: str,
        monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> tuple[int, str, str]:
    """Run `main()` against the synthetic project; (exit code, stdout, stderr)."""
    argv = ["unit_cost.py", "--sprint-dir", str(tmp_path / "sprint"), "--project", str(repo),
            "--projects-dir", str(tmp_path / "projects"), *extra]
    monkeypatch.setattr(sys, "argv", argv)
    code = uc.main()
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def scenario(tmp_path: Path, commits: list[tuple[str, int]], rows: dict[str, tuple[str, str]],
             records: list[dict]) -> Path:
    """Repo, task_scope.md and one main transcript. `rows` maps unit id to (est, commit name)."""
    repo, shas = make_repo(tmp_path, commits)
    write_scope(tmp_path / "sprint",
                [(uid, est, f"✅ `{shas[name]}`") for uid, (est, name) in rows.items()])
    write_transcripts(tmp_path / "projects", repo, "main", records)
    return repo


def test_turns_at_interval_edges_and_outside_the_unit_range(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo = scenario(
        tmp_path,
        [("s", 50), ("a", 100), ("b", 200), ("z", 300)],
        {"U1": ("-", "a"), "U2": ("-", "b")},
        [
            record(50, "before-first", input_tokens=1000),
            record(51, "a-low", input_tokens=1),
            record(100, "a-high", input_tokens=2),
            record(101, "b-low", input_tokens=4),
            record(200, "b-high", input_tokens=8),
            record(201, "after-last-unit", input_tokens=16),
            record(250, "tail-non-unit", input_tokens=32),
        ],
    )
    code, out, _ = run(repo, tmp_path, "--json", monkeypatch=monkeypatch, capsys=capsys)
    report = json.loads(out)
    by_id = {row["id"]: row for row in report["units"]}
    assert code == 0
    assert (by_id["U1"]["fresh"], by_id["U1"]["turns"]) == (3, 2)
    assert (by_id["U2"]["fresh"], by_id["U2"]["turns"]) == (12, 2)
    assert report["totals"]["excluded_turns"] == 3
    assert report["totals"]["overhead_turns"] == 0


def test_batch_of_two_units_splits_the_next_interval_evenly(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo = scenario(
        tmp_path,
        [("s", 50), ("a", 50), ("b", 100)],
        {"U1": ("-", "a"), "U2": ("-", "b")},
        [record(70, "t1", input_tokens=1000), record(90, "t2", output_tokens=3000)],
    )
    code, out, _ = run(repo, tmp_path, "--json", monkeypatch=monkeypatch, capsys=capsys)
    rows = {row["id"]: row for row in json.loads(out)["units"]}
    assert code == 0
    assert (rows["U1"]["fresh"], rows["U1"]["turns"]) == (2000, 1)
    assert (rows["U2"]["fresh"], rows["U2"]["turns"]) == (2000, 1)


def test_turn_on_a_non_unit_commit_is_overhead(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo = scenario(
        tmp_path,
        [("s", 50), ("a", 100), ("n", 200), ("b", 300)],
        {"U1": ("-", "a"), "U2": ("-", "b")},
        [record(80, "u1", input_tokens=5), record(150, "over", input_tokens=700),
         record(250, "u2", input_tokens=9)],
    )
    code, out, _ = run(repo, tmp_path, "--json", monkeypatch=monkeypatch, capsys=capsys)
    report = json.loads(out)
    rows = {row["id"]: row for row in report["units"]}
    assert code == 0
    assert (rows["U1"]["fresh"], rows["U2"]["fresh"]) == (5, 9)
    assert (report["totals"]["overhead_fresh"], report["totals"]["overhead_turns"]) == (700, 1)


def test_pending_batch_absorbs_a_following_non_unit_commit(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """The limit of study 6.7: the cost of the non-unit commit is charged to the batch."""
    repo = scenario(
        tmp_path,
        [("s", 50), ("a", 50), ("n", 200), ("b", 300)],
        {"U1": ("-", "a"), "U2": ("-", "b")},
        [record(150, "n-turn", input_tokens=700), record(250, "b-turn", input_tokens=9)],
    )
    code, out, _ = run(repo, tmp_path, "--json", monkeypatch=monkeypatch, capsys=capsys)
    report = json.loads(out)
    rows = {row["id"]: row["fresh"] for row in report["units"]}
    assert code == 0
    assert rows == {"U1": 700, "U2": 9}
    assert report["totals"]["overhead_fresh"] == 0


def test_fresh_excludes_cache_read_and_turns_are_deduplicated(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo = scenario(
        tmp_path,
        [("s", 50), ("a", 100)],
        {"U1": ("-", "a")},
        [
            record(60, "m1", input_tokens=1, output_tokens=2, cache_creation_input_tokens=4,
                   cache_read_input_tokens=1_000_000),
            record(65, "m1", input_tokens=1, output_tokens=2, cache_creation_input_tokens=4,
                   cache_read_input_tokens=1_000_000),
            record(70, "syn", model="<synthetic>", input_tokens=999),
        ],
    )
    write_transcripts(tmp_path / "projects", repo, "agent-1",
                      [record(80, "sub1", output_tokens=10)], subagent=True)
    code, out, _ = run(repo, tmp_path, "--json", monkeypatch=monkeypatch, capsys=capsys)
    row = json.loads(out)["units"][0]
    assert code == 0
    assert (row["fresh"], row["turns"]) == (17, 2)


def test_json_fields_and_est_cost_difference(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo = scenario(
        tmp_path,
        [("s", 50), ("a", 100), ("b", 200)],
        {"U1": ("1000", "a"), "U2": ("-", "b")},
        [record(60, "u1", input_tokens=1500), record(150, "u2", input_tokens=40)],
    )
    code, out, _ = run(repo, tmp_path, "--json", monkeypatch=monkeypatch, capsys=capsys)
    report = json.loads(out)
    assert code == 0
    assert set(report) == {"units", "unattributed", "totals"}
    assert set(report["totals"]) == {"fresh", "turns", "overhead_fresh", "overhead_turns",
                                     "excluded_turns"}
    assert report["units"][0] == {"id": "U1", "fresh": 1500, "turns": 1, "est_cost": 1000,
                                  "diff": 500}
    assert report["units"][1] == {"id": "U2", "fresh": 40, "turns": 1, "est_cost": None,
                                  "diff": None}
    assert report["unattributed"] == []


def test_text_output_has_one_line_per_unit_a_totals_line_and_the_unattributed_count(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo = scenario(
        tmp_path,
        [("s", 50), ("a", 100), ("b", 200)],
        {"U1": ("1000", "a"), "U2": ("-", "b")},
        [record(60, "u1", input_tokens=1500)],
    )
    code, out, _ = run(repo, tmp_path, monkeypatch=monkeypatch, capsys=capsys)
    lines = out.splitlines()
    assert code == 0
    assert lines[0] == "U1  fresh=1500  turns=1  est=1000  diff=+500"
    assert lines[1].startswith("total  fresh=1500  turns=1")
    assert lines[2] == "unattributed=1  ids=U2"


def test_unit_outside_the_tip_chain_is_listed_and_not_fatal(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo, shas = make_repo(tmp_path, [("s", 50), ("a", 100)])
    base = git(repo, "rev-parse", "--short", "main")
    write_scope(tmp_path / "sprint", [("U1", "-", f"✅ `{shas['a']}`"),
                                      ("U2", "-", f"✅ `{base}`")])
    write_transcripts(tmp_path / "projects", repo, "main", [record(70, "t", input_tokens=3)])
    code, out, _ = run(repo, tmp_path, "--json", monkeypatch=monkeypatch, capsys=capsys)
    report = json.loads(out)
    assert code == 0
    assert report["unattributed"] == ["U2"]
    assert report["units"][0]["id"] == "U1"


def test_no_task_scope_is_an_error(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo, _ = make_repo(tmp_path, [("a", 100)])
    (tmp_path / "sprint").mkdir()
    code, out, err = run(repo, tmp_path, monkeypatch=monkeypatch, capsys=capsys)
    assert (code, out) == (2, "")
    assert err.startswith("unit_cost: error: no task_scope.md") and err.count("\n") == 1


def test_no_work_units_is_an_error(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo, _ = make_repo(tmp_path, [("a", 100)])
    (tmp_path / "sprint").mkdir()
    (tmp_path / "sprint" / "task_scope.md").write_text("# Scope\n\nNo table.\n")
    code, _, err = run(repo, tmp_path, monkeypatch=monkeypatch, capsys=capsys)
    assert code == 2
    assert "no work units" in err and err.count("\n") == 1


def test_no_committed_unit_is_an_error(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo, _ = make_repo(tmp_path, [("a", 100)])
    write_scope(tmp_path / "sprint", [("U1", "-", "⏳")])
    code, _, err = run(repo, tmp_path, monkeypatch=monkeypatch, capsys=capsys)
    assert code == 2
    assert "no committed unit" in err and err.count("\n") == 1


def test_unresolved_sha_is_an_error(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo, _ = make_repo(tmp_path, [("a", 100)])
    write_scope(tmp_path / "sprint", [("U1", "-", "✅ `deadbee`")])
    write_transcripts(tmp_path / "projects", repo, "main", [record(70, "t", input_tokens=3)])
    code, _, err = run(repo, tmp_path, monkeypatch=monkeypatch, capsys=capsys)
    assert code == 2
    assert "unresolved SHA deadbee of unit U1" in err and err.count("\n") == 1


def test_unresolved_base_is_a_git_failure(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo = scenario(tmp_path, [("a", 100)], {"U1": ("-", "a")}, [record(70, "t", input_tokens=3)])
    code, _, err = run(repo, tmp_path, "--base", "no-such-ref", monkeypatch=monkeypatch,
                       capsys=capsys)
    assert code == 2
    assert "git rev-list failed" in err and err.count("\n") == 1


def test_missing_transcript_directory_is_an_error(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo, shas = make_repo(tmp_path, [("a", 100)])
    write_scope(tmp_path / "sprint", [("U1", "-", f"✅ `{shas['a']}`")])
    code, _, err = run(repo, tmp_path, monkeypatch=monkeypatch, capsys=capsys)
    assert code == 2
    assert "no transcript directory" in err and err.count("\n") == 1


def test_no_attributable_unit_is_an_error(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo = scenario(tmp_path, [("s", 50), ("a", 100)], {"U1": ("-", "a")},
                    [record(40, "early", input_tokens=3)])
    code, out, err = run(repo, tmp_path, monkeypatch=monkeypatch, capsys=capsys)
    assert (code, out) == (2, "")
    assert err == "unit_cost: error: no unit could be attributed\n"


def test_unreadable_transcript_is_reported_and_skipped(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    class Unforeseen(Exception):
        """An exception type no handler enumerates."""

    projects = tmp_path / "projects"
    directory = projects / "d"
    directory.mkdir(parents=True)
    (directory / "dir.jsonl").mkdir()
    (directory / "good.jsonl").write_text(json.dumps(record(5, "g", input_tokens=7)) + "\n")
    (directory / "bad.jsonl").write_text("x")
    real = uc._file_turns

    def failing(path: Path):  # type: ignore[no-untyped-def]
        if path.name == "bad.jsonl":
            raise Unforeseen("boom")
        return real(path)

    monkeypatch.setattr(uc, "_file_turns", failing)
    turns = uc.read_turns(directory)
    err = capsys.readouterr().err
    assert turns == [(T0 + 5, 7)]
    assert "skipped dir.jsonl" in err and "skipped bad.jsonl: boom" in err
