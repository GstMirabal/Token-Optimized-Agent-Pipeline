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
import hooks.on_commit_msg as ocm
from hooks.on_commit import (
    audit_dependency_justification,
    audit_regression_test,
)

# --- regression test gate (rules/code_craft.md §6) ---------------------

def test_fix_touching_source_without_a_test_is_blocked():
    assert audit_regression_test("fix(auth): reject expired tokens #020", ["src/auth.py"])


def test_fix_shipping_a_test_passes():
    assert audit_regression_test(
        "fix(auth): reject expired tokens #020\n\n"
        "Repro: tests/test_auth.py — fails at abc1234\n",
        ["src/auth.py", "tests/test_auth.py"],
    ) is None


@pytest.mark.parametrize("path", [
    "tests/test_auth.py", "src/__tests__/auth.js", "src/auth_test.go", "src/auth.test.ts",
])
def test_test_paths_are_recognised_across_languages(path):
    message = f"fix(x): y #020\n\nRepro: {path} — fails at abc1234\n"
    assert audit_regression_test(message, ["src/a.py", path]) is None


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
    msg.write_text(
        "fix(app): correct it #020\n\nRepro: tests/test_app.py — fails at abc1234\n"
    )
    monkeypatch.setattr(sys, "argv", ["on_commit_msg.py", str(msg)])
    assert ocm.main() == 0


def test_missing_message_file_does_not_crash(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["on_commit_msg.py", str(tmp_path / "absent")])
    assert ocm.main() == 0


# --- commit-msg sees files staged by the same command (Sprint 057 QA3-1) ---

HOOK_SCRIPT = Path(__file__).resolve().parent.parent / "hooks" / "on_commit_msg.py"


def _install_commit_msg_hook(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Point `root`'s commit-msg hook at this repository's `on_commit_msg.py`.

    Global, system and environment-injected git config (`GIT_CONFIG_COUNT`,
    `GIT_CONFIG_PARAMETERS`) are dropped for the rest of the test, so a
    developer's `core.hooksPath` cannot route git away from this hook.

    Args:
        root: The scratch repository.
        monkeypatch: Fixture that scopes the git environment to the test.
    """
    empty = root / ".empty_gitconfig"
    empty.write_text("")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(empty))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)
    monkeypatch.delenv("GIT_CONFIG_PARAMETERS", raising=False)
    hook = root / ".git" / "hooks" / "commit-msg"
    hook.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{HOOK_SCRIPT}" "$1"\n')
    hook.chmod(0o755)


def _shell(command: str) -> subprocess.CompletedProcess[str]:
    """Run one shell command line in the current directory.

    Args:
        command: The command line, run with `shell=True` so `&&` chains apply.

    Returns:
        subprocess.CompletedProcess[str]: The finished process, never raising.
    """
    return subprocess.run(command, shell=True, capture_output=True, text=True, check=False)


def test_commit_msg_hook_judges_files_added_in_the_same_command(
    repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`git add x && git commit` stages after any PreToolUse check ran."""
    _install_commit_msg_hook(repo, monkeypatch)
    Path("app.py").write_text("def f(): pass\n")
    result = _shell('git add app.py && git commit -q -m "fix(app): correct it #057"')
    assert result.returncode != 0
    assert "must stage the test" in result.stderr


def test_commit_msg_hook_judges_files_staged_by_commit_all(
    repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`git commit -a` stages tracked changes inside the commit itself."""
    _install_commit_msg_hook(repo, monkeypatch)
    Path("cfg.json").write_text("{}\n")
    subprocess.run(["git", "add", "cfg.json"], check=True)
    subprocess.run(["git", "commit", "-q", "--no-verify", "-m", "chore: seed #057"], check=True)
    Path("cfg.json").write_text('{"a": 1}\n')
    result = _shell('git commit -a -q -m "fix(cfg): correct it #057"')
    assert result.returncode != 0
    assert "must stage the test" in result.stderr


# --- commit-msg runs Guard 5, the task_scope precondition (Sprint 057 QA5-1) ---

def test_message_file_refuses_sprint_commit_outside_dir_without_scope(repo, monkeypatch):
    subprocess.run(["git", "checkout", "-q", "-b", "ai-sprint/052"], check=True)
    stage("app.py", "def f(): pass\n")
    msg = repo / "MSG"
    msg.write_text("feat(app): add f #052\n")
    monkeypatch.setattr(sys, "argv", ["on_commit_msg.py", str(msg)])
    assert ocm.main() == 1


def test_message_file_passes_sprint_commit_when_scope_exists(repo, monkeypatch):
    subprocess.run(["git", "checkout", "-q", "-b", "ai-sprint/052"], check=True)
    scope = repo / "docs" / "sprints" / "052-core-pipeline"
    scope.mkdir(parents=True)
    (scope / "task_scope.md").write_text("# scope\n")
    stage("app.py", "def f(): pass\n")
    msg = repo / "MSG"
    msg.write_text("feat(app): add f #052\n")
    monkeypatch.setattr(sys, "argv", ["on_commit_msg.py", str(msg)])
    assert ocm.main() == 0


# --- one list of message audits for both hooks (Sprint 057 convergence rule 3) ---
# Family QA2-4, QA3-1, QA4-1, QA5-1: prose misstated which hook runs which
# message guard. Exact coverage of these two tests, and no more: (1) every
# module-level `audit_*` function of `hooks/on_commit.py` whose parameters are
# exactly `(message, staged)` is in `MESSAGE_AUDITS`; (2) `hooks/on_commit_msg.py`
# imports `MESSAGE_AUDITS` and no `audit_*` name.

def test_every_message_audit_is_in_message_audits() -> None:
    import inspect

    import hooks.on_commit as oc

    declared = {
        fn for name, fn in inspect.getmembers(oc, inspect.isfunction)
        if fn.__module__ == oc.__name__ and name.startswith("audit_")
        and list(inspect.signature(fn).parameters) == ["message", "staged"]
    }
    assert declared == {audit for audit, _code in oc.MESSAGE_AUDITS}


def test_commit_msg_hook_imports_the_list_not_single_audits() -> None:
    import ast

    tree = ast.parse(HOOK_SCRIPT.read_text(encoding="utf-8"))
    imported = {
        alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    assert "MESSAGE_AUDITS" in imported
    assert not {name for name in imported if name.startswith("audit_")}
