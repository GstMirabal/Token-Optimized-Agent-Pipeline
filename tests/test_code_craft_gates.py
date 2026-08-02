"""Tests for the two code-craft gates in hooks/on_commit.py (Phase 020).

Both were calibrated against this repository's own 156-commit history before
being wired in, following the PR #27 lesson: a gate that blocks the legitimate
case is worse than no gate, because it gets removed rather than satisfied.
That run rejected the first version of the dependency gate, which fired on any
touch of a manifest — including version bumps, removals, and package.json files
vendored inside node_modules/.
"""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import hooks.on_commit_msg as ocm  # noqa: E402
from hooks.on_commit import (  # noqa: E402
    audit_dependency_justification,
    audit_regression_test,
)


# --- regression test gate (rules/code_craft.md §6) ---------------------

def test_fix_touching_source_without_a_test_is_blocked():
    assert audit_regression_test("fix(auth): reject expired tokens #020", ["src/auth.py"])


def test_fix_shipping_a_test_passes():
    assert audit_regression_test(
        "fix(auth): reject expired tokens #020", ["src/auth.py", "tests/test_auth.py"]
    ) is None


@pytest.mark.parametrize("path", [
    "tests/test_auth.py", "src/__tests__/auth.js", "src/auth_test.go", "src/auth.test.ts",
])
def test_test_paths_are_recognised_across_languages(path):
    assert audit_regression_test("fix(x): y #020", ["src/a.py", path]) is None


def test_fix_touching_no_source_needs_no_test():
    """A documentation or workflow fix has nothing to write a test against."""
    assert audit_regression_test(
        "fix(docs): correct the retrofit order #020", ["README.md", "workflows/x.md"]
    ) is None


def test_non_fix_commits_are_not_subject_to_the_gate():
    assert audit_regression_test("feat(auth): add login #020", ["src/auth.py"]) is None


# --- dependency gate (rules/code_craft.md §7) --------------------------

@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True)
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "T")
    Path("requirements.txt").write_text("existing==1.0.0\n")
    run("add", "-A")
    run("commit", "-qm", "base")
    return tmp_path


def stage(path: str, content: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content)
    subprocess.run(["git", "add", path], check=True)


def test_new_dependency_without_justification_is_blocked(repo):
    stage("requirements.txt", "existing==1.0.0\nbrand-new==2.0.0\n")
    assert audit_dependency_justification("feat(x): add thing #020", ["requirements.txt"])


def test_new_dependency_with_justification_passes(repo):
    stage("requirements.txt", "existing==1.0.0\nbrand-new==2.0.0\n")
    message = "feat(x): add thing #020\n\nDependency: brand-new — parses the vendor's feed format."
    assert audit_dependency_justification(message, ["requirements.txt"]) is None


def test_version_bump_is_not_an_admission(repo):
    """The first version of this gate blocked bumps, where a justification
    line is nonsense. Verified against 156 real commits."""
    stage("requirements.txt", "existing==2.0.0\n")
    assert audit_dependency_justification("feat(x): bump #020", ["requirements.txt"]) is None


def test_removing_a_dependency_is_not_an_admission(repo):
    stage("requirements.txt", "")
    assert audit_dependency_justification("refactor(x): drop it #020", ["requirements.txt"]) is None


def test_vendored_manifest_is_ignored(repo):
    """Two real commits were flagged for package.json files under node_modules/
    inside a vendored -3rd skill — nothing the author chose or controls."""
    stage("skills/autoskills-3rd/node_modules/autoskills/package.json",
          '{"dependencies": {"whatever": "1.0.0"}}')
    assert audit_dependency_justification(
        "chore(skills): vendor update #020",
        ["skills/autoskills-3rd/node_modules/autoskills/package.json"],
    ) is None


def test_chore_deps_is_exempt(repo):
    stage("requirements.txt", "existing==1.0.0\nbrand-new==2.0.0\n")
    assert audit_dependency_justification("chore(deps): weekly bump #020", ["requirements.txt"]) is None


# --- native commit-msg hook (closes the pre-commit coverage hole) ------

def test_strip_comments_drops_git_commentary():
    raw = "feat(x): thing #020\n\n# Please enter the commit message\n# On branch main\n"
    assert ocm.strip_comments(raw) == "feat(x): thing #020"


def test_message_file_gates_a_fix_without_a_test(repo, monkeypatch):
    stage("app.py", "def f(): pass\n")
    msg = repo / "MSG"
    msg.write_text("fix(app): correct it #020\n")
    monkeypatch.setattr(sys, "argv", ["on_commit_msg.py", str(msg)])
    assert ocm.main() == 1


def test_message_file_passes_when_the_test_is_staged(repo, monkeypatch):
    stage("app.py", "def f(): pass\n")
    stage("tests/test_app.py", "def test_f(): pass\n")
    msg = repo / "MSG"
    msg.write_text("fix(app): correct it #020\n")
    monkeypatch.setattr(sys, "argv", ["on_commit_msg.py", str(msg)])
    assert ocm.main() == 0


def test_missing_message_file_does_not_crash(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["on_commit_msg.py", str(tmp_path / "absent")])
    assert ocm.main() == 0
