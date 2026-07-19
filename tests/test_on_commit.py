"""Tests for hooks/on_commit.py — the PreToolUse gate that can block real
commits/pushes. Covers the J-12 push guard, commit message validation, and
the dual Trinity audit."""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from hooks import on_commit


# --- J-12 push guard -------------------------------------------------------

@pytest.mark.parametrize("command", [
    "git push origin main",
    "git push -u origin main",
    "git push origin master",
    "cd repo && git push origin main --tags",
])
def test_push_to_main_is_blocked(command, monkeypatch, tmp_path):
    monkeypatch.setattr(on_commit, "DEPLOY_UNLOCK", tmp_path / "absent")
    assert on_commit.is_blocked_push(command)


@pytest.mark.parametrize("command", [
    "git push origin ai-sprint/078",
    "git push origin feature/login",
    "git status",
    "git push origin main-backup",   # not the main branch
    "ls -la",
])
def test_other_commands_pass(command, monkeypatch, tmp_path):
    monkeypatch.setattr(on_commit, "DEPLOY_UNLOCK", tmp_path / "absent")
    assert not on_commit.is_blocked_push(command)


def test_deploy_unlock_marker_allows_sanctioned_push(monkeypatch, tmp_path):
    marker = tmp_path / ".deploy_unlock"
    marker.touch()
    monkeypatch.setattr(on_commit, "DEPLOY_UNLOCK", marker)
    assert not on_commit.is_blocked_push("git push origin main")


# --- Commit message validation (Conventional Commits + #[Sprint_ID]) -------

@pytest.mark.parametrize("message", [
    "feat(auth): add login flow #078",
    "fix: resolve circular import #02",
    "chore(close): memory purge #073",
    "refactor(topology)!: flatten skills #032",
])
def test_valid_messages(message):
    assert on_commit.is_valid_commit_message(message)


@pytest.mark.parametrize("message", [
    "add login flow",                      # no type
    "feat: add login flow",                # missing #ID suffix
    "feature(auth): add login #078",       # invalid type
    "feat(auth) add login #078",           # missing colon
    "",
])
def test_invalid_messages(message):
    assert not on_commit.is_valid_commit_message(message)


def test_extract_commit_message():
    assert on_commit.extract_commit_message(
        'git commit -m "feat: x #01"') == "feat: x #01"
    assert on_commit.extract_commit_message(
        "git commit -m 'fix: y #02'") == "fix: y #02"
    assert on_commit.extract_commit_message("git commit --amend") is None


# --- Dual Trinity audit ----------------------------------------------------

def _make_skill(root, name, *, frontmatter=True, scripts=False, readme=False, init=False):
    d = root / "skills" / name
    d.mkdir(parents=True)
    head = "---\nname: x\ndescription: y\n---\n" if frontmatter else ""
    (d / "SKILL.md").write_text(head + "# Skill\n")
    if scripts:
        (d / "scripts").mkdir()
        if init:
            (d / "scripts" / "__init__.py").touch()
    if readme:
        (d / "README.md").write_text("# readme\n")
    return d


def _audit_in(tmp_path, monkeypatch, staged):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(on_commit, "get_staged_files", lambda: staged)
    return on_commit.audit_trinity_standard()


def test_knowledge_skill_needs_only_frontmatter(tmp_path, monkeypatch):
    _make_skill(tmp_path, "guide-skill")
    assert _audit_in(tmp_path, monkeypatch, ["skills/guide-skill/SKILL.md"])


def test_knowledge_skill_without_frontmatter_fails(tmp_path, monkeypatch):
    _make_skill(tmp_path, "bad-skill", frontmatter=False)
    assert not _audit_in(tmp_path, monkeypatch, ["skills/bad-skill/SKILL.md"])


def test_executable_skill_requires_full_trinity(tmp_path, monkeypatch):
    _make_skill(tmp_path, "tool-skill", scripts=True)  # no README, no __init__
    assert not _audit_in(tmp_path, monkeypatch, ["skills/tool-skill/scripts/run.py"])


def test_executable_skill_full_trinity_passes(tmp_path, monkeypatch):
    _make_skill(tmp_path, "tool-skill", scripts=True, readme=True, init=True)
    assert _audit_in(tmp_path, monkeypatch, ["skills/tool-skill/scripts/run.py"])
