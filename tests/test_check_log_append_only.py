"""Tests for scripts/check_log_append_only.py (plan D34) on throwaway git repos."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
CHECK = SCRIPTS / "check_log_append_only.py"
sys.path.insert(0, str(SCRIPTS))
import check_log_append_only as module

SPRINT = "docs/sprints/060-core-pipeline"
ROW = "| Friction words here | Resolution words there | KI-060-1 |\n"
MINING = "Record `error_mining` origin: first sentence names the file. Second sentence names the cause.\n"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com",
         "-c", "commit.gpgsign=false", *args],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _commit(repo: Path, name: str, text: str | None, message: str = "docs: change") -> None:
    path = repo / SPRINT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if text is None:
        path.unlink()
    else:
        path.write_text(text)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)


def _run(repo: Path, rng: str = "base..HEAD") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), "--sprint-dir", SPRINT, "--range", rng],
        cwd=repo, capture_output=True, text=True, check=False,
    )


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    _commit(tmp_path, "SPRINT_LOG.md", ROW + MINING)
    _commit(tmp_path, "IMPLEMENTATION_PLAN.md", "| D1 | **One** | none |\n")
    _git(tmp_path, "tag", "base")
    return tmp_path


def test_appended_prose_exits_0(repo: Path) -> None:
    grown = ROW.replace("there |", "there, annotated later |") + MINING + "New line.\n"
    _commit(repo, "SPRINT_LOG.md", grown)
    result = _run(repo)
    assert result.returncode == 0, result.stdout
    assert "0 violation(s)" in result.stdout


def test_lost_ki_word_exits_2(repo: Path) -> None:
    _commit(repo, "SPRINT_LOG.md", ROW.replace("there ", "") + MINING)
    result = _run(repo)
    assert result.returncode == 2
    assert "KI-060-1: lost 1 of" in result.stdout


def test_removed_ki_row_exits_2(repo: Path) -> None:
    _commit(repo, "SPRINT_LOG.md", MINING)
    assert _run(repo).returncode == 2


def test_lost_mining_sentence_exits_2(repo: Path) -> None:
    _commit(repo, "SPRINT_LOG.md", ROW + MINING.replace(" Second sentence names the cause.", ""))
    result = _run(repo)
    assert result.returncode == 2
    assert "error_mining sentence gone" in result.stdout


def test_mining_sentence_moved_verbatim_exits_0(repo: Path) -> None:
    moved = "Other: first sentence names the file. Second sentence names the cause.\n"
    _commit(repo, "SPRINT_LOG.md", ROW + "Record `error_mining` origin: first sentence names the file.\n" + moved)
    assert _run(repo).returncode == 0


def test_waiver_trailer_prints_and_exits_0(repo: Path) -> None:
    message = "docs: remove host data\n\nLog-Rewrite: RA-15 host data"
    _commit(repo, "SPRINT_LOG.md", MINING, message)
    result = _run(repo)
    assert result.returncode == 0, result.stdout
    assert "WAIVED" in result.stdout
    assert "RA-15 host data" in result.stdout


def test_empty_waiver_reason_waives_nothing(repo: Path) -> None:
    _commit(repo, "SPRINT_LOG.md", MINING, "docs: remove\n\nLog-Rewrite:")
    assert _run(repo).returncode == 2


def test_waiver_covers_only_its_own_commit(repo: Path) -> None:
    _commit(repo, "SPRINT_LOG.md", MINING, "docs: remove\n\nLog-Rewrite: reason")
    _commit(repo, "SPRINT_LOG.md", "Empty now.\n")
    result = _run(repo)
    assert result.returncode == 2
    assert "error_mining sentence gone" in result.stdout


def test_deleted_log_exits_2(repo: Path) -> None:
    _commit(repo, "SPRINT_LOG.md", None)
    assert _run(repo).returncode == 2


def test_commit_outside_range_is_not_judged(repo: Path) -> None:
    _commit(repo, "SPRINT_LOG.md", MINING)
    _git(repo, "tag", "after-loss")
    _commit(repo, "SPRINT_LOG.md", MINING + "More.\n")
    assert _run(repo, "after-loss..HEAD").returncode == 0


def test_reordered_words_are_a_declared_limit(repo: Path) -> None:
    _commit(repo, "SPRINT_LOG.md", ROW.replace("Friction words here", "here words Friction") + MINING)
    assert _run(repo).returncode == 0


@pytest.mark.parametrize("mark", ["Sustituida por D2.", "Ampliada por D2."])
def test_marked_decision_exits_0(repo: Path, mark: str) -> None:
    plan = f"| D1 | **{mark}** **One** | none |\n| D2 | **Two**: sustituye a D1 | none |\n"
    _commit(repo, "IMPLEMENTATION_PLAN.md", plan)
    assert _run(repo).returncode == 0


@pytest.mark.parametrize("verb", ["sustituye a D1", "Sustituyen a `D1`"])
def test_unmarked_decision_exits_2(repo: Path, verb: str) -> None:
    plan = f"| D1 | **One** | none |\n| D2 | **Two**: {verb} | none |\n"
    _commit(repo, "IMPLEMENTATION_PLAN.md", plan)
    result = _run(repo)
    assert result.returncode == 2
    assert "D1: superseded by D2" in result.stdout


def test_superseding_a_missing_decision_exits_2(repo: Path) -> None:
    _commit(repo, "IMPLEMENTATION_PLAN.md", "| D2 | **Two**: sustituye a D1 | none |\n")
    assert _run(repo).returncode == 2


def test_other_wording_is_a_declared_limit(repo: Path) -> None:
    plan = "| D1 | **One** | none |\n| D2 | **Two**: supersedes D1 | none |\n"
    _commit(repo, "IMPLEMENTATION_PLAN.md", plan)
    assert _run(repo).returncode == 0


def test_absent_records_are_skipped_without_require_records(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert module.check(repo, "docs/sprints/999-none", "base..HEAD") == 0
    out = capsys.readouterr().out
    assert "zone 3 skipped" in out
    assert "zones 1 and 2 skipped" in out


def test_absent_record_by_hand_exits_2(repo: Path) -> None:
    (repo / "docs" / "sprints" / "061-empty").mkdir(parents=True)
    result = subprocess.run(
        [sys.executable, str(CHECK), "--sprint-dir", "docs/sprints/061-empty", "--range", "base..HEAD"],
        cwd=repo, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 2
    assert "no SPRINT_LOG.md at HEAD" in result.stdout


def _lost_word_run(repo: Path, cwd: Path, sprint_dir: str) -> subprocess.CompletedProcess[str]:
    _commit(repo, "SPRINT_LOG.md", ROW.replace("there ", "") + MINING)
    return subprocess.run(
        [sys.executable, str(CHECK), "--sprint-dir", sprint_dir, "--range", "base..HEAD"],
        cwd=cwd, capture_output=True, text=True, check=False,
    )


def test_sprint_dir_relative_to_a_subdirectory_is_judged(repo: Path) -> None:
    result = _lost_word_run(repo, repo / "docs", "sprints/060-core-pipeline")
    assert result.returncode == 2
    assert "KI-060-1: lost 1 of" in result.stdout


def test_absolute_sprint_dir_is_judged(repo: Path) -> None:
    result = _lost_word_run(repo, repo, str(repo / SPRINT))
    assert result.returncode == 2
    assert "KI-060-1: lost 1 of" in result.stdout


def test_missing_sprint_dir_fails_closed(repo: Path) -> None:
    result = _lost_word_run(repo, repo, SPRINT[:-1])
    assert result.returncode == 2
    assert "no such sprint directory" in result.stderr


def test_sprint_dir_outside_the_repository_fails_closed(repo: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
    outside = tmp_path_factory.mktemp("outside")
    assert _lost_word_run(repo, repo, str(outside)).returncode == 2


def test_bad_revision_fails_closed(repo: Path) -> None:
    result = _run(repo, "nope..HEAD")
    assert result.returncode == 2
    assert "error:" in result.stderr


@pytest.mark.parametrize("rng", ["HEAD", "base...HEAD", "..HEAD"])
def test_malformed_range_fails_closed(repo: Path, rng: str) -> None:
    assert _run(repo, rng).returncode == 2


def _anchor(root: Path, sprint_id: int, **extra: str) -> None:
    (root / "docs" / "sprints" / f"{sprint_id:03d}-core-pipeline").mkdir(parents=True)
    state = {"current_sprint": {"id": sprint_id}, **extra}
    (root / "docs" / "active_state.json").write_text(json.dumps(state))


def test_current_sprint_below_enforcement_is_out_of_scope(tmp_path: Path) -> None:
    _anchor(tmp_path, module.ENFORCED_FROM - 1, last_close_commit="abc")
    assert module._current_sprint_target(tmp_path) is None


def test_current_sprint_at_enforcement_uses_the_last_close(tmp_path: Path) -> None:
    _anchor(tmp_path, module.ENFORCED_FROM, last_close_commit="abc")
    assert module._current_sprint_target(tmp_path) == (
        f"docs/sprints/{module.ENFORCED_FROM:03d}-core-pipeline", "abc..HEAD",
    )


def test_current_sprint_without_last_close_exits_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _anchor(tmp_path, module.ENFORCED_FROM)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["check", "--current-sprint"])
    assert module.main() == 2


def test_current_sprint_from_a_host_root_audits_the_host(repo: Path) -> None:
    (repo / "docs" / "active_state.json").write_text(json.dumps({
        "current_sprint": {"id": 60}, "last_close_commit": _git(repo, "rev-parse", "base"),
    }))
    _commit(repo, "SPRINT_LOG.md", ROW.replace("there ", "") + MINING)
    result = subprocess.run(
        [sys.executable, str(CHECK), "--current-sprint"],
        cwd=repo, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 2
    assert "KI-060-1: lost 1 of" in result.stdout


def test_current_sprint_from_the_framework_root_uses_agents_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    framework = tmp_path / "framework"
    (framework / "docs").mkdir(parents=True)
    (framework / "scripts").mkdir()
    (framework / "scripts" / "check_log_append_only.py").write_text("")
    _anchor(framework, module.ENFORCED_FROM - 1)
    monkeypatch.chdir(framework)
    monkeypatch.setattr(module, "agents_root", lambda: framework)
    monkeypatch.setattr(sys, "argv", ["check", "--current-sprint"])
    assert module.main() == 0
    assert "(skip)" in capsys.readouterr().out
