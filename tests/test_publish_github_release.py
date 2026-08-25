"""Tests for scripts/publish_github_release.py.

What these pin is that a GitHub Release is the CHANGELOG section, not the
tag annotation. `--notes-from-tag` is how the landing page would diverge
from the ledger; `--verify-tag` is how `gh` is stopped from minting a tag
out of `main`. No test in this file reaches the network.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import publish_github_release as pgr

SAMPLE = """# Changelog

## [Unreleased]

## [4.9.1] - 2026-08-25

### Fixed
- hotfix notes

## [4.4.0] - 2026-08-03

### Added
- older notes

## [4.3.0] - 2026-07-30

### Added
- backfill
"""


def _ok(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(cmd, 0, "", "")


def test_extract_notes_stops_at_the_next_section():
    notes = pgr.extract_notes(SAMPLE, "4.9.1")
    assert notes is not None
    assert "hotfix notes" in notes
    assert "older notes" not in notes
    assert "## [4.9.1]" not in notes


def test_extract_notes_returns_none_when_the_section_is_missing():
    assert pgr.extract_notes(SAMPLE, "4.8.0") is None


def test_extract_notes_returns_none_when_the_section_is_empty():
    text = "## [1.0.0] - 2026-01-01\n\n## [0.9.0] - 2026-01-01\n\n- x\n"
    assert pgr.extract_notes(text, "1.0.0") is None


def test_normalize_strips_a_leading_v():
    assert pgr.normalize("v4.9.1") == "4.9.1"
    assert pgr.normalize("4.9.1") == "4.9.1"


def test_unreleased_is_not_a_sealed_version():
    assert pgr.sealed_versions(SAMPLE) == ["4.9.1", "4.4.0", "4.3.0"]


def test_only_the_newest_sealed_section_is_latest():
    sealed = pgr.sealed_versions(SAMPLE)
    assert pgr.is_newest("4.9.1", sealed) is True
    assert pgr.is_newest("4.4.0", sealed) is False


def test_origin_slug_parses_ssh_and_https():
    assert pgr.origin_slug("git@github.com:Acme/Repo.git") == "Acme/Repo"
    assert pgr.origin_slug("https://github.com/Acme/Repo.git") == "Acme/Repo"
    assert pgr.origin_slug("https://example.com/Acme/Repo.git") is None


def test_release_body_appends_the_ledger_footer_once():
    body = pgr.release_body("### Fixed\n- x", "Acme/Repo")
    assert body.count("Full history:") == 1
    assert "github.com/Acme/Repo/blob/main/CHANGELOG.md" in body
    again = pgr.release_body(body, "Acme/Repo")
    assert again.count("Full history:") == 1


def test_create_release_never_uses_notes_from_tag(monkeypatch):
    captured: list[list[str]] = []

    def fake_run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
        captured.append(cmd)
        return _ok(cmd)

    monkeypatch.setattr(pgr, "run", fake_run)
    pgr.create_release("v4.9.1", "body\n", latest=True)
    pgr.create_release("v4.4.0", "body\n", latest=False)
    assert "--notes-from-tag" not in captured[0]
    assert "--verify-tag" in captured[0]
    assert "--latest" in captured[0]
    assert "--latest=false" in captured[1]


def test_publish_one_refuses_a_tag_with_no_section():
    assert pgr.publish_one("4.8.0", SAMPLE, "Acme/Repo", notes_only=True) == 2


def test_publish_one_is_idempotent_when_the_release_exists(monkeypatch, capsys):
    monkeypatch.setattr(pgr, "release_exists", lambda tag: True)
    assert pgr.publish_one("4.9.1", SAMPLE, "Acme/Repo", notes_only=False) == 0
    assert "already exists" in capsys.readouterr().out


def test_missing_versions_are_oldest_first():
    assert pgr.missing_versions(SAMPLE, {"4.9.1", "4.4.0"}) == ["4.4.0", "4.9.1"]


def test_main_notes_only_prints_one_section(tmp_path, monkeypatch, capsys):
    (tmp_path / "CHANGELOG.md").write_text(SAMPLE, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "v4.9.1", "--notes-only"])
    monkeypatch.setattr(
        pgr, "git_remote_url", lambda: "git@github.com:Acme/Repo.git"
    )
    assert pgr.main() == 0
    out = capsys.readouterr().out
    assert "hotfix notes" in out
    assert "older notes" not in out
    assert "Acme/Repo" in out


def test_main_rejects_neither_or_both_selectors(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog"])
    assert pgr.main() == 2
    monkeypatch.setattr(sys, "argv", ["prog", "v4.9.1", "--missing"])
    assert pgr.main() == 2


def test_the_gate_declares_its_invoker():
    assert "invoked_by: deployment_workflow.md#github_release" in (pgr.__doc__ or "")


def test_the_workflow_phase_that_declares_it_actually_names_the_script():
    workflow = (ROOT / "workflows" / "deployment_workflow.md").read_text(
        encoding="utf-8"
    )
    assert "publish_github_release.py" in workflow
    assert "github_release" in workflow
    assert "--notes-from-tag" in workflow
